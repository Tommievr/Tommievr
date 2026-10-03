"""Character loading, placeholders, expressions, blink, lip-sync.

Naming contract (design/character-sheets/COMMON.md, design/blender/RIGGING.md):
  shape keys  expr_<name>, vis_X..vis_H, blink_L, blink_R   (on the head/face mesh)
  actions     idle_breathe, walk, run, hop, look_around, ...
Everything degrades gracefully: a missing shape key or action is skipped with a printed warning, never a crash.
"""
import json
import math
import os
import random

import bpy
from mathutils import Vector

from . import toon
from .palette import CHARACTERS, GOLD

VISEMES = "XABCDEFGH"
EXPRESSIONS = ("neutral", "happy", "curious", "surprised", "scared_but_brave", "sleepy", "laughing")


# ---------------------------------------------------------------- loading
def _bbox_world(objs):
    pts = []
    for o in objs:
        if o.type == "MESH":
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    if not pts:
        return Vector((0, 0, 0)), Vector((0, 0, 0))
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def load_character(spec):
    """Load a character per shot-spec entry. Returns the root object (an Empty that parents everything).

    spec keys: name, model (.blend | .glb | .gltf | None), pos [x,y,z], rot_z (degrees), height_m (optional: rescale so the
    model's bounding box is this tall), collection (for .blend: collection name to append, default = name),
    shade (True = convert materials to toon), anim (action name), expression.
    A missing model gives a toon placeholder in the character's colours so shots can be tested on day 0.
    """
    name = spec["name"]
    before = set(bpy.data.objects)
    model = spec.get("model")
    if model and os.path.exists(model):
        ext = os.path.splitext(model)[1].lower()
        if ext == ".blend":
            coll_name = spec.get("collection", name)
            with bpy.data.libraries.load(model, link=False) as (src, dst):
                if coll_name not in src.collections:
                    raise RuntimeError(f"{model}: no collection '{coll_name}' (has {src.collections})")
                dst.collections = [coll_name]
            coll = dst.collections[0]
            bpy.context.scene.collection.children.link(coll)
        else:
            bpy.ops.import_scene.gltf(filepath=model)
    else:
        if model:
            print(f"[evg] WARNING: {model} not found, using placeholder for {name}")
        make_placeholder(name)
    new = [o for o in bpy.data.objects if o not in before]

    root = bpy.data.objects.new(f"{name}_root", None)
    bpy.context.scene.collection.objects.link(root)
    for o in new:
        if o.parent is None:
            o.parent = root
    bpy.context.view_layer.update()

    if spec.get("height_m"):
        lo, hi = _bbox_world(new)
        h = hi.z - lo.z
        if h > 1e-6:
            root.scale = (spec["height_m"] / h,) * 3
    bpy.context.view_layer.update()
    lo, _ = _bbox_world(new)
    root.location = (spec["pos"][0], spec["pos"][1], spec["pos"][2] - lo.z * root.scale.z)  # feet on pos.z
    root.rotation_euler[2] = math.radians(spec.get("rot_z", 0))

    # character collection (used for light linking)
    cc = bpy.data.collections.get("CHARACTERS") or bpy.data.collections.new("CHARACTERS")
    if cc.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(cc)
    for o in [root] + new:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        cc.objects.link(o)

    if spec.get("shade", True) and model and os.path.exists(model):
        for o in new:
            if o.type == "MESH" and not o.name.startswith("PLACEHOLDER"):
                toon.convert_to_toon(o)
    if spec.get("expression"):
        apply_expression(root, spec["expression"])
    if spec.get("anim"):
        play_action(root, spec["anim"])
    return root


def children_meshes(root):
    return [o for o in root.children_recursive if o.type == "MESH"]


# ---------------------------------------------------------------- placeholder
def _prim(kind, name, loc, scale, mat, parent=None, rot=None, **kw):
    if kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=loc)
    elif kind == "cone":
        bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1, depth=2, location=loc)
    elif kind == "cyl":
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, location=loc)
    elif kind == "torus":
        bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=kw.get("minor", 0.12), location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    if rot:
        o.rotation_euler = rot
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    if parent:
        o.parent = parent
    return o


def make_placeholder(name):
    """Chunky toon cat/lamb made of primitives: for pipeline tests before real models exist. ~0.22 m (cat) / 0.30 m (lamb) shoulder."""
    col = CHARACTERS[name]
    lamb = name in ("cotton", "toffee")
    fur = col.get("wool" if lamb else "fur")
    body_m = toon.simple_material(f"PH_{name}_body", fur)
    face_m = toon.simple_material(f"PH_{name}_face", col.get("face", fur))
    ear_m = toon.simple_material(f"PH_{name}_ear", col["ear"])
    collar_m = toon.simple_material(f"PH_{name}_collar", col["collar"])
    gold = toon.gold_material()
    eye_w = toon.simple_material("PH_eye_white", "#FFFFFF", rim_strength=0)
    iris = toon.simple_material(f"PH_{name}_iris", col["iris"], rim_strength=0)
    pupil = toon.simple_material("PH_pupil", "#0A0A12", rim_strength=0)
    s = 1.3 if lamb else 1.0
    anchor = bpy.data.objects.new(f"PLACEHOLDER_{name}", None)
    bpy.context.scene.collection.objects.link(anchor)
    P = anchor
    _prim("sphere", f"PLACEHOLDER_{name}_body", (0, 0, 0.14 * s), (0.11 * s, 0.17 * s, 0.10 * s), body_m, P)
    head = _prim("sphere", f"PLACEHOLDER_{name}_head", (0, -0.17 * s, 0.24 * s), (0.10 * s, 0.09 * s, 0.085 * s), face_m, P)
    for sx in (-1, 1):
        if lamb:
            _prim("sphere", f"PLACEHOLDER_{name}_ear{sx}", (sx * 0.12 * s, -0.17 * s, 0.25 * s), (0.07 * s, 0.025 * s, 0.03 * s), ear_m, P,
                  rot=(0, 0, sx * 0.3))
        else:
            _prim("cone", f"PLACEHOLDER_{name}_ear{sx}", (sx * 0.06 * s, -0.16 * s, 0.33 * s), (0.035 * s, 0.025 * s, 0.035 * s), ear_m, P,
                  rot=(0, sx * 0.25, 0))
        for lx, ly in ((0.06, -0.09), (0.06, 0.09)):
            _prim("cyl", f"PLACEHOLDER_{name}_leg", (sx * lx * s, ly * 2 * s, 0.05 * s), (0.028 * s, 0.028 * s, 0.05 * s), body_m, P)
        # eyes: white + iris + pupil, facing -Y
        ex = sx * 0.04 * s
        _prim("sphere", f"PLACEHOLDER_{name}_eyeW", (ex, -0.245 * s, 0.255 * s), (0.026 * s, 0.012 * s, 0.03 * s), eye_w, P)
        _prim("sphere", f"PLACEHOLDER_{name}_iris", (ex, -0.254 * s, 0.255 * s), (0.017 * s, 0.006 * s, 0.021 * s), iris, P)
        _prim("sphere", f"PLACEHOLDER_{name}_pupil", (ex, -0.258 * s, 0.255 * s), (0.009 * s, 0.004 * s, 0.012 * s), pupil, P)
    _prim("torus", f"PLACEHOLDER_{name}_collar", (0, -0.15 * s, 0.19 * s), (0.075 * s, 0.075 * s, 0.075 * s), collar_m, P, minor=0.14)
    _prim("cyl", f"PLACEHOLDER_{name}_{'bell' if lamb else 'tag'}", (0, -0.23 * s, 0.17 * s), (0.016 * s, 0.016 * s, 0.004 * s), gold, P, rot=(math.pi / 2, 0, 0))
    if lamb:
        _prim("sphere", f"PLACEHOLDER_{name}_tail", (0, 0.2 * s, 0.17 * s), (0.04 * s,) * 3, body_m, P)
    else:
        _prim("cyl", f"PLACEHOLDER_{name}_tail", (0, 0.22 * s, 0.26 * s), (0.02 * s, 0.02 * s, 0.1 * s), body_m, P, rot=(0.5, 0, 0))
    if name == "evie":
        _prim("sphere", f"PLACEHOLDER_{name}_patch", (-0.05, -0.2, 0.30), (0.05, 0.02, 0.04),
              toon.simple_material("PH_patch", col["patch"]), P, rot=(0, 0, 0.4))
    if name == "toffee":
        for lx, ly in ((0.06, -0.09), (0.06, 0.09)):
            for sx in (-1, 1):
                _prim("cyl", f"PLACEHOLDER_{name}_sock", (sx * lx * s, ly * 2 * s, 0.02 * s), (0.03 * s, 0.03 * s, 0.025 * s),
                      toon.simple_material("PH_toffee_sock", col["cream"]), P)
    return anchor


# ---------------------------------------------------------------- shape keys
def _key_blocks(root):
    for o in children_meshes(root):
        sk = o.data.shape_keys
        if sk:
            for kb in sk.key_blocks:
                yield o, kb


def set_key(root, key_name, value, frame=None):
    """Set (and optionally keyframe) every shape key called key_name under root. Returns True if found."""
    found = False
    for o, kb in _key_blocks(root):
        if kb.name == key_name:
            kb.value = value
            if frame is not None:
                kb.keyframe_insert("value", frame=frame)
            found = True
    return found


def apply_expression(root, name, weight=1.0, frame=None):
    """Zero all expr_* keys, then set expr_<name>. 'neutral' = all zero."""
    for _, kb in _key_blocks(root):
        if kb.name.startswith("expr_"):
            kb.value = 0.0
            if frame is not None:
                kb.keyframe_insert("value", frame=frame)
    if name != "neutral" and not set_key(root, f"expr_{name}", weight, frame):
        print(f"[evg] note: no shape key expr_{name} on {root.name} (rig tier T1: ignored)")


def blink_track(root, fps, duration_s, seed=1, min_gap=3.0, max_gap=5.0, length=0.15):
    """Random blinks via blink_L/blink_R shape keys, else by squashing eye objects named *eye* / *iris* / *pupil* in Z."""
    rng = random.Random(seed)
    has_keys = any(kb.name in ("blink_L", "blink_R") for _, kb in _key_blocks(root))
    eyes = [o for o in root.children_recursive if any(t in o.name.lower() for t in ("eyew", "_eye", "iris", "pupil"))]
    t = rng.uniform(1.0, max_gap)
    while t < duration_s:
        f0, f1, f2 = (int(t * fps) + 1, int((t + length / 2) * fps) + 1, int((t + length) * fps) + 1)
        if has_keys:
            for k in ("blink_L", "blink_R"):
                set_key(root, k, 0.0, f0)
                set_key(root, k, 1.0, f1)
                set_key(root, k, 0.0, f2)
        else:
            for o in eyes:
                z = o.scale.z
                for f, mul in ((f0, 1.0), (f1, 0.08), (f2, 1.0)):
                    o.scale.z = z * mul
                    o.keyframe_insert("scale", index=2, frame=f)
                o.scale.z = z
        t += rng.uniform(min_gap, max_gap)


def play_action(root, action_name):
    """Assign a Blender Action to the armature under root (looped by NLA/cyclic modifier is up to the .blend)."""
    arm = next((o for o in root.children_recursive if o.type == "ARMATURE"), None)
    act = bpy.data.actions.get(action_name)
    if arm is None or act is None:
        print(f"[evg] note: action '{action_name}' not applied (armature={bool(arm)}, action={bool(act)}) -> placeholder bob")
        add_walk_bob(root)
        return
    arm.animation_data_create().action = act


def add_walk_bob(root, fps=24, duration_s=4.0, rate=3.0, height=0.02):
    """Placeholder motion for models without a rig: hop + sway."""
    base_z = root.location.z
    for f in range(1, int(fps * duration_s) + 1, max(1, fps // 8)):
        t = f / fps
        root.location.z = base_z + height * abs(math.sin(t * math.pi * rate))
        root.rotation_euler[1] = 0.04 * math.sin(t * math.pi * rate)
        root.keyframe_insert("location", index=2, frame=f)
        root.keyframe_insert("rotation_euler", index=1, frame=f)


# ---------------------------------------------------------------- lip sync
def read_rhubarb(path):
    """Parse Rhubarb Lip Sync output (JSON {'mouthCues': [...]} or TSV 'seconds<TAB>shape'). Returns [(start, end, shape)]."""
    cues = []
    with open(path) as f:
        text = f.read().strip()
    if text.startswith("{"):
        for c in json.loads(text)["mouthCues"]:
            cues.append((c["start"], c["end"], c["value"]))
    else:
        rows = [ln.split("\t") for ln in text.splitlines() if ln.strip()]
        for (t0, v), nxt in zip(rows, rows[1:] + [[rows[-1][0], "X"]]):
            cues.append((float(t0), float(nxt[0]), v.strip()))
    return cues


def apply_lipsync(root, cues, fps, offset_s=0.0, ease_frames=2):
    """Keyframe vis_X..vis_H shape keys from cues. If a character has no vis_* keys, drive the jaw bone / 'mouth' scale instead (tier T1)."""
    have = {kb.name for _, kb in _key_blocks(root)}
    if not any(n.startswith("vis_") for n in have):
        jaw = next((o for o in root.children_recursive if o.type == "ARMATURE"), None)
        print(f"[evg] note: no vis_* shape keys on {root.name}; lip-sync skipped (jaw tier handled by rig; armature={bool(jaw)})")
        return 0
    n = 0
    for start, end, shape in cues:
        key = f"vis_{shape}"
        f_on = int((start + offset_s) * fps) + 1
        f_off = int((end + offset_s) * fps) + 1
        for v in VISEMES:
            kn = f"vis_{v}"
            if kn in have:
                set_key(root, kn, 0.0, max(1, f_on - ease_frames))
                set_key(root, kn, 1.0 if v == shape else 0.0, f_on)
        n += 1
    return n
