"""Quick quadruped rig for a cleaned Meshy character (design/blender/RIGGING.md).

What it does (all steps optional via flags):
  1. builds an armature sized from the mesh bounding box (cat or lamb layout), named per the rigging contract
  2. parents the mesh with automatic weights (+ rigid parenting of collar/tag/bell objects to their bones)
  3. adds simple leg IK (no poles: good enough for walk/hop with the placeholder actions in evg.animation_presets if you add them)
  4. reports which contract shape keys (expr_*, vis_*, blink_*) exist; they are keyframed by name from the shot script (no drivers)
  5. optionally adds two toon eye objects (so blinking works even if the Meshy eyes are baked)

Run:
  blender -b pipeline/meshy/evie/clean/evie.blend --python pipeline/blender/rig_quadruped.py -- \
      --kind cat --mesh evie_body --collar evie_collar --tag evie_tag --eyes --iris "#1E7FD6" --out pipeline/meshy/evie/rigged/evie.blend
  --mesh NAME   the body mesh (head included). Join pieces first (Ctrl+J) except collar/tag/bell, eyes.
Bone placement is a first guess from proportions: after running, open the .blend, go to Edit mode on the armature and nudge bones
into the joints (rotate the view to side and front), then re-run only step 2 with --rebind.
Facing -Y, Z up, feet on z=0. Character's left = +X (bones end in .L).
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evg import toon  # noqa: E402
from evg.palette import hex_to_linear_rgba  # noqa: E402

EXPR = ("happy", "curious", "surprised", "scared_but_brave", "sleepy", "laughing")
VIS = "XABCDEFGH"

# layout: fractions of the bounding box. y: 0 = front (nose), 1 = back (rump). z: 0 = feet, 1 = top of head/ears.
LAYOUTS = {
    "cat": dict(chest_y=0.42, pelvis_y=0.78, hip_z=0.42, shoulder_z=0.42, neck_z=0.62, head_y=0.20, head_z=0.70, leg_x=0.30,
                fore_y=0.42, hind_y=0.80, tail_n=5, tail_z=0.55, ear_x=0.22, ear_z=0.90, ear_n=2),
    "lamb": dict(chest_y=0.40, pelvis_y=0.82, hip_z=0.52, shoulder_z=0.52, neck_z=0.74, head_y=0.14, head_z=0.82, leg_x=0.26,
                 fore_y=0.34, hind_y=0.84, tail_n=1, tail_z=0.60, ear_x=0.40, ear_z=0.80, ear_n=3),
}


def bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def build_armature(mesh, kind="cat", name=None, layout=None):
    lay = dict(LAYOUTS[kind], **(layout or {}))
    lo, hi = bbox(mesh)
    size = hi - lo
    cx = (lo.x + hi.x) / 2

    def P(x_frac_of_halfwidth, y_frac, z_frac):
        return Vector((cx + x_frac_of_halfwidth * size.x / 2, lo.y + y_frac * size.y, lo.z + z_frac * size.z))

    arm_data = bpy.data.armatures.new(f"{name or mesh.name}_armature")
    arm = bpy.data.objects.new(f"{name or mesh.name}_rig", arm_data)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = arm_data.edit_bones

    def bone(bname, head, tail, parent=None, connect=False, roll=0.0):
        b = eb.new(bname)
        b.head, b.tail = head, tail
        b.roll = roll
        if parent:
            b.parent = eb[parent]
            b.use_connect = connect
        return b

    cy, py, hz = lay["chest_y"], lay["pelvis_y"], lay["hip_z"]
    bone("root", P(0, py, 0), P(0, py, 0.12))
    bone("pelvis", P(0, py, hz), P(0, (py + cy) / 2, hz + 0.02), "root")
    bone("spine.01", P(0, (py + cy) / 2, hz + 0.02), P(0, cy, hz + 0.05), "pelvis", True)
    bone("chest", P(0, cy, hz + 0.05), P(0, cy - 0.05, lay["neck_z"]), "spine.01", True)
    bone("neck.01", P(0, cy - 0.05, lay["neck_z"]), P(0, lay["head_y"] + 0.08, lay["head_z"] - 0.04), "chest", True)
    bone("head", P(0, lay["head_y"] + 0.08, lay["head_z"] - 0.04), P(0, lay["head_y"] - 0.05, lay["head_z"] + 0.08), "neck.01", True)
    bone("jaw", P(0, lay["head_y"] + 0.02, lay["head_z"] - 0.05), P(0, lay["head_y"] - 0.08, lay["head_z"] - 0.07), "head")
    for side, sx in ((".L", 1), (".R", -1)):
        # ears
        prev, n = "head", lay["ear_n"]
        for i in range(n):
            a = P(sx * lay["ear_x"] * (1 + 0.5 * i), lay["head_y"] + 0.05, lay["ear_z"] - 0.04 * i)
            b = P(sx * lay["ear_x"] * (1.4 + 0.5 * i), lay["head_y"] + 0.05, lay["ear_z"] + 0.03 - 0.04 * i)
            bone(f"ear{side}.0{i + 1}", a, b, prev if i == 0 else f"ear{side}.0{i}", i > 0)
            prev = f"ear{side}.0{i + 1}"
        # front leg
        fy, hy, lx = lay["fore_y"], lay["hind_y"], lay["leg_x"]
        sh = lay["shoulder_z"]
        bone(f"upper_arm{side}", P(sx * lx, fy, sh), P(sx * lx, fy, sh * 0.55), "chest")
        bone(f"forearm{side}", P(sx * lx, fy, sh * 0.55), P(sx * lx, fy, 0.08), f"upper_arm{side}", True)
        bone(f"paw_front{side}", P(sx * lx, fy, 0.08), P(sx * lx, fy - 0.07, 0.0), f"forearm{side}", True)
        # hind leg
        bone(f"thigh{side}", P(sx * lx, hy, hz), P(sx * lx, hy + 0.02, hz * 0.55), "pelvis")
        bone(f"shin{side}", P(sx * lx, hy + 0.02, hz * 0.55), P(sx * lx, hy, 0.08), f"thigh{side}", True)
        bone(f"paw_hind{side}", P(sx * lx, hy, 0.08), P(sx * lx, hy - 0.07, 0.0), f"shin{side}", True)
        # IK targets (feet controls)
        bone(f"ik_paw_front{side}", P(sx * lx, fy - 0.03, 0.0), P(sx * lx, fy - 0.03, 0.05), "root")
        bone(f"ik_paw_hind{side}", P(sx * lx, hy - 0.03, 0.0), P(sx * lx, hy - 0.03, 0.05), "root")
    # tail chain
    prev = "pelvis"
    n = lay["tail_n"]
    for i in range(n):
        a = P(0, py + 0.03 + i * 0.045, lay["tail_z"] + i * 0.05)
        b = P(0, py + 0.03 + (i + 1) * 0.045, lay["tail_z"] + (i + 1) * 0.05)
        bone(f"tail.0{i + 1}", a, b, prev, i > 0)
        prev = f"tail.0{i + 1}"
    # collar / tag / bell chain
    cz = (lay["neck_z"] + lay["head_z"]) / 2 - 0.08
    bone("collar_root", P(0, cy - 0.02, cz), P(0, cy - 0.03, cz - 0.02), "neck.01")
    bone("tag.01", P(0, cy - 0.05, cz - 0.02), P(0, cy - 0.05, cz - 0.10), "collar_root")
    bone("look_target", P(0, -0.8, lay["head_z"]), P(0, -0.8, lay["head_z"] + 0.06))
    bpy.ops.object.mode_set(mode="OBJECT")
    arm_data.display_type = "OCTAHEDRAL"
    return arm


def bind(mesh, arm):
    """Automatic weights for the body mesh."""
    bpy.ops.object.select_all(action="DESELECT")
    mesh.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")


def parent_rigid(obj, arm, bone_name):
    """Collar / tag / bell: parent to a bone without deformation (keeps world transform)."""
    mw = obj.matrix_world.copy()
    obj.parent = arm
    obj.parent_type = "BONE"
    obj.parent_bone = bone_name
    obj.matrix_world = mw


def add_leg_ik(arm):
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="POSE")
    for side in (".L", ".R"):
        for lower, tgt, chain in ((f"forearm{side}", f"ik_paw_front{side}", 3), (f"shin{side}", f"ik_paw_hind{side}", 3)):
            pb = arm.pose.bones.get(lower)
            if pb is None:
                continue
            c = pb.constraints.new("IK")
            c.target, c.subtarget = arm, tgt
            c.chain_count = 2
    bpy.ops.object.mode_set(mode="OBJECT")


def report_shape_keys(mesh):
    """Shape keys are keyframed BY NAME by the shot script (evg.characters.set_key / apply_expression / apply_lipsync);
    no drivers needed. Print which of the contract names exist on the mesh so you know what is still missing."""
    keys = {kb.name for kb in (mesh.data.shape_keys.key_blocks if mesh.data.shape_keys else [])}
    wanted = [f"expr_{e}" for e in EXPR] + [f"vis_{v}" for v in VIS] + ["blink_L", "blink_R"]
    have = [k for k in wanted if k in keys]
    missing = [k for k in wanted if k not in keys]
    return have, missing


def add_eyes(arm, kind, iris_hex, eye_y=0.0, eye_x=0.30, eye_z=0.72, radius=0.10, mesh=None):
    """Two toon eyes (white, iris, pupil, catchlight) parented to the head bone. Positions are fractions of the bbox; tune after."""
    lo, hi = bbox(mesh) if mesh else (Vector((-0.1, -0.2, 0)), Vector((0.1, 0.2, 0.25)))
    size = hi - lo
    cx = (lo.x + hi.x) / 2
    r = radius * size.z * 0.5
    white = toon.simple_material("eye_white", "#FFFFFF", rim_strength=0)
    iris = toon.simple_material(f"eye_iris_{kind}", iris_hex, rim_strength=0)
    pupil = toon.simple_material("eye_pupil", "#0A0A12", rim_strength=0)
    shine = toon.simple_material("eye_shine", "#FFFFFF", rim_strength=0, threshold=0.0)
    made = []
    for side, sx in ((".L", 1), (".R", -1)):
        pos = Vector((cx + sx * eye_x * size.x / 2, lo.y + eye_y * size.y, lo.z + eye_z * size.z))
        parts = [
            ("EyeW", (r, r * 0.55, r * 1.1), (0, 0, 0), white),
            ("Iris", (r * 0.75, r * 0.3, r * 0.9), (0, -r * 0.45, 0), iris),
            ("Pupil", (r * 0.4, r * 0.2, r * 0.6), (0, -r * 0.68, 0), pupil),
            ("Shine", (r * 0.16, r * 0.1, r * 0.16), (r * 0.25, -r * 0.8, r * 0.3), shine),
        ]
        for pn, sc, off, mat in parts:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=pos + Vector(off))
            o = bpy.context.active_object
            o.name = f"eye{side}_{pn}"
            o.scale = sc
            bpy.ops.object.shade_smooth()
            o.data.materials.append(mat)
            parent_rigid(o, arm, "head")
            made.append(o)
    return made


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    opt = {"kind": "cat", "mesh": None, "collar": None, "tag": None, "eyes": False, "iris": "#1E7FD6", "out": None, "ik": True}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--kind", "--mesh", "--collar", "--tag", "--iris", "--out"):
            opt[a[2:]] = argv[i + 1]; i += 1
        elif a == "--eyes":
            opt["eyes"] = True
        elif a == "--no-ik":
            opt["ik"] = False
        i += 1
    mesh = bpy.data.objects[opt["mesh"]]
    arm = build_armature(mesh, opt["kind"], name=mesh.name.replace("_body", ""))
    bind(mesh, arm)
    for key in ("collar", "tag"):
        if opt[key] and opt[key] in bpy.data.objects:
            parent_rigid(bpy.data.objects[opt[key]], arm, "collar_root" if key == "collar" else "tag.01")
    if opt["ik"]:
        add_leg_ik(arm)
    if opt["eyes"]:
        add_eyes(arm, opt["kind"], opt["iris"], mesh=mesh)
    # everything into one collection named after the character so build_shot.py can append it ("collection": "<name>")
    cname = mesh.name.replace("_body", "")
    coll = bpy.data.collections.get(cname) or bpy.data.collections.new(cname)
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
    members = [mesh, arm] + [o for o in bpy.data.objects if o.parent == arm]
    for o in members:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
    have, missing = report_shape_keys(mesh)
    print(f"[rig] bones: {len(arm.data.bones)}; shape keys present: {have}")
    print(f"[rig] shape keys still to sculpt (tier T2): {missing}")
    if opt["out"]:
        os.makedirs(os.path.dirname(opt["out"]) or ".", exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=opt["out"])
        print("[rig] saved", opt["out"])


if __name__ == "__main__":
    main()
