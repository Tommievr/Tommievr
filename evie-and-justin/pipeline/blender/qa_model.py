"""Automatic checks for a Meshy model (design/meshy/QA_AND_FIXES.md). Prints a PASS/WARN/FAIL report and writes JSON.

  blender -b --python pipeline/blender/qa_model.py -- pipeline/meshy/evie/raw/evie.glb [--json out.json] [--shot evie_qa.png]

Checks: face count, bounding box (height/length/width), loose parts, non-manifold edges, materials/textures, shape keys,
armature presence, scale/orientation (Z up, feet on ground), left-right symmetry of the silhouette.
"""
import json
import os
import sys

import bpy
import bmesh
from mathutils import Vector


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    out = {"model": argv[0], "json": None, "shot": None}
    for i, a in enumerate(argv):
        if a == "--json":
            out["json"] = argv[i + 1]
        if a == "--shot":
            out["shot"] = argv[i + 1]
    return out


def main():
    a = args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ext = os.path.splitext(a["model"])[1].lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=a["model"])
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=a["model"])
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=a["model"])
    else:
        raise SystemExit(f"unsupported: {ext}")
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    report, status = {}, {}

    def check(name, value, ok, warn=None):
        report[name] = value
        status[name] = "PASS" if ok else ("WARN" if warn else "FAIL")

    tris = faces = 0
    nonman = loose_parts = 0
    pts = []
    for o in meshes:
        me = o.data
        faces += len(me.polygons)
        tris += sum(len(p.vertices) - 2 for p in me.polygons)
        bm = bmesh.new()
        bm.from_mesh(me)
        nonman += sum(1 for e in bm.edges if not e.is_manifold)
        # loose parts = connected components
        seen, comps = set(), 0
        for v in bm.verts:
            if v.index in seen:
                continue
            comps += 1
            stack = [v]
            while stack:
                c = stack.pop()
                if c.index in seen:
                    continue
                seen.add(c.index)
                stack += [e.other_vert(c) for e in c.link_edges]
        loose_parts += comps
        bm.free()
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    size = hi - lo
    check("mesh_objects", len(meshes), len(meshes) >= 1)
    check("triangles", tris, 8000 <= tris <= 80000, warn=True)
    check("loose_parts", loose_parts, loose_parts <= 12, warn=True)
    check("non_manifold_edges", nonman, nonman == 0, warn=True)
    check("bbox_size_m", [round(size.x, 3), round(size.y, 3), round(size.z, 3)], max(size) > 0.01)
    check("feet_on_ground_z", round(lo.z, 3), abs(lo.z) < 0.02, warn=True)
    # symmetry: compare vertex counts left/right of x=centre
    cx = (lo.x + hi.x) / 2
    left = right = 0
    for o in meshes:
        for v in o.data.vertices:
            x = (o.matrix_world @ v.co).x
            left += x < cx
            right += x >= cx
    sym = min(left, right) / max(1, max(left, right))
    check("left_right_vertex_balance", round(sym, 2), sym > 0.8, warn=True)
    imgs = [i.name for i in bpy.data.images]
    check("textures", imgs, len(imgs) >= 1, warn=True)
    mats = [m.name for m in bpy.data.materials]
    check("materials", mats, len(mats) >= 1, warn=True)
    sk = sorted({k.name for o in meshes if o.data.shape_keys for k in o.data.shape_keys.key_blocks})
    check("shape_keys", sk, True)
    arm = [o.name for o in bpy.data.objects if o.type == "ARMATURE"]
    check("armature", arm, True)
    report["notes"] = [
        "Meshy output normally has NO armature and NO shape keys: rig and add keys per design/blender/RIGGING.md.",
        "Triangles: 8k-80k expected; fur is geometry-free so >80k means noise to clean up.",
    ]
    print("\n== MODEL QA ==", a["model"])
    for k in status:
        print(f"{status[k]:5s} {k}: {report[k]}")
    for n in report["notes"]:
        print("note:", n)
    report["status"] = status
    if a["json"]:
        with open(a["json"], "w") as f:
            json.dump(report, f, indent=2)
    if a["shot"]:
        from evg import cameras, lights, scene
        scene.setup_render(samples=16)
        lights.build_rig("golden", target=((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, size.z / 2))
        scene.placeholder_ground()
        cam = cameras.place_camera("medium_single", subject=((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, size.z / 2), distance_scale=max(1.0, size.z / 0.22))
        bpy.context.scene.render.resolution_percentage = 50
        bpy.context.scene.render.filepath = a["shot"]
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
