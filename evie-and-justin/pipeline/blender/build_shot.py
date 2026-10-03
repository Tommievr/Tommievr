"""Build and render one shot from a JSON spec. Run inside Blender:

blender -b scene.blend --python pipeline/blender/build_shot.py -- shot.json
"""
import json
import math
import sys

import bpy

ASPECTS = {"16:9": (1920, 1080), "9:16": (1080, 1920)}


def load_spec():
    argv = sys.argv
    path = argv[argv.index("--") + 1]
    with open(path) as f:
        return json.load(f)


def import_character(c, fps, duration_s):
    bpy.ops.import_scene.gltf(filepath=c["model"])
    root = bpy.context.selected_objects[0]
    root.name = c["name"]
    root.location = c["pos"]
    if c.get("anim") == "walk":
        add_walk_bob(root, fps, duration_s)
    return root


def add_walk_bob(obj, fps, duration_s):
    """Placeholder motion: bounce + sway so shots can be previewed before real rigs exist."""
    base = obj.location.z
    frames = int(fps * duration_s)
    for f in range(0, frames + 1, max(1, fps // 6)):
        t = f / fps
        obj.location.z = base + 0.05 * abs(math.sin(t * math.pi * 3))
        obj.rotation_euler[1] = 0.05 * math.sin(t * math.pi * 3)
        obj.keyframe_insert("location", index=2, frame=f)
        obj.keyframe_insert("rotation_euler", index=1, frame=f)


def setup_camera(cam_spec):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = cam_spec["lens_mm"]
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = cam_spec["pos"]
    bpy.ops.object.empty_add(location=cam_spec["look_at"])
    target = bpy.context.active_object
    track = cam.constraints.new("TRACK_TO")
    track.target = target
    track.track_axis = "TRACK_NEGATIVE_Z"
    track.up_axis = "UP_Y"
    bpy.context.scene.camera = cam


def main():
    spec = load_spec()
    scene = bpy.context.scene
    w, h = ASPECTS[spec["aspect"]]
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.fps = spec["fps"]
    scene.frame_start, scene.frame_end = 1, int(spec["fps"] * spec["duration_s"])
    for c in spec["characters"]:
        import_character(c, spec["fps"], spec["duration_s"])
    setup_camera(spec["camera"])
    scene.render.filepath = spec["out"]
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    bpy.ops.render.render(animation=True)


main()
