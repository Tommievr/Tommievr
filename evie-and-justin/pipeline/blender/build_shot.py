"""Build and render one shot from a JSON spec (stylised toon look, EEVEE).

Run inside Blender (4.2 LTS or newer):
  blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/ep01_s01_001.json
Options (after the spec path):
  --still N        render only frame N as PNG (fast look-dev)
  --no-render      build the scene only (use with --save-blend)
  --save-blend P   save the built scene to P so you can open it in Blender
  --aspect 9:16    override the spec's aspect (re-render the same shot vertical for a Short)
  --variant dusk   override the light variant (day | golden | dusk)

Spec: see pipeline/shots/example_shot.json and design/blender/SETUP.md. A missing model/background gives a toon placeholder.
"""
import json
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evg import cameras, characters, fx, lights, scene  # noqa: E402
from evg.palette import VARIANTS  # noqa: E402


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    opts = {"spec": argv[0], "still": None, "render": True, "save_blend": None, "aspect": None, "variant": None}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--still":
            opts["still"] = int(argv[i + 1]); i += 1
        elif a == "--no-render":
            opts["render"] = False
        elif a == "--save-blend":
            opts["save_blend"] = argv[i + 1]; i += 1
        elif a == "--aspect":
            opts["aspect"] = argv[i + 1]; i += 1
        elif a == "--variant":
            opts["variant"] = argv[i + 1]; i += 1
        i += 1
    return opts


def build(spec, aspect=None, variant=None):
    aspect = aspect or spec.get("aspect", "16:9")
    variant = variant or spec.get("variant", "golden")
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {list(VARIANTS)}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    r = spec.get("render", {})
    sc = scene.setup_render(spec.get("fps", 24), spec["duration_s"], r.get("samples", 64), r.get("engine"))

    scene.load_background(spec.get("background", "placeholder"), variant)

    roots = [characters.load_character(c) for c in spec["characters"]]
    cc = bpy.data.collections.get("CHARACTERS")
    centre = (sum(rt.location.x for rt in roots) / len(roots), sum(rt.location.y for rt in roots) / len(roots), 0.12) if roots else (0, 0, 0.12)

    cam_spec = spec["camera"]
    lamb_scale = 1.3 if any(c["name"] in ("cotton", "toffee") for c in spec["characters"]) else 1.0
    subject = tuple(cam_spec.get("subject", centre))
    lights.build_rig(variant, target=(subject[0], subject[1], 0.15), char_collection=cc, camera_yaw_deg=cam_spec.get("yaw", 0.0))
    if "preset" in cam_spec:
        cameras.place_camera(cam_spec["preset"], subject=subject, yaw_deg=cam_spec.get("yaw", 0.0), aspect=aspect,
                             distance_scale=cam_spec.get("distance_scale", lamb_scale), look_offset=tuple(cam_spec.get("look_offset", (0, 0, 0))),
                             tilt_deg=cam_spec.get("tilt_deg"))
    else:  # legacy raw camera
        cameras.place_raw_camera(cam_spec["pos"], cam_spec["look_at"], cam_spec.get("lens_mm", 45), aspect)

    for c, rt in zip(spec["characters"], roots):
        if spec.get("blink", True):
            characters.blink_track(rt, spec.get("fps", 24), spec["duration_s"], seed=hash(c["name"]) % 1000)
        if c.get("lipsync") and os.path.exists(c["lipsync"]):
            n = characters.apply_lipsync(rt, characters.read_rhubarb(c["lipsync"]), spec.get("fps", 24), c.get("lipsync_offset_s", 0.0))
            print(f"[evg] lip-sync: {n} cues for {c['name']}")
    if spec.get("spoiler"):
        msg = f"this shot is a SPOILER for {spec['spoiler']}"
        print(f"[evg] WARNING: {msg}" + (": do NOT publish it as a Short/thumbnail before release!" if aspect == "9:16" else ""))
    if aspect == "9:16" and any(f.get("type") in ("pouch_peek", "pouch_open") for f in spec.get("fx", [])):
        print("[evg] WARNING: pouch glow in a Short: only if the script marks this frame as spoiler-safe (pouch_open = Ep.7 reveal)")
    fx.apply_fx(spec.get("fx"), {c["name"]: rt for c, rt in zip(spec["characters"], roots)}, spec.get("fps", 24))
    if spec.get("tag_glow"):
        g = spec["tag_glow"]
        lights.add_tag_glow(tuple(g["pos"]), frame_in=g.get("frame_in", 1), frame_peak=g.get("frame_peak", 12), frame_out=g.get("frame_out", 36),
                            char_collection=cc)
    sc.render.resolution_percentage = r.get("percent", 100)  # e.g. 40 for quick look-dev
    sc.render.filepath = spec["out"]
    return sc


def main():
    opts = parse_args()
    with open(opts["spec"]) as f:
        spec = json.load(f)
    sc = build(spec, opts["aspect"], opts["variant"])
    if opts["save_blend"]:
        scene.save_debug_blend(opts["save_blend"])
    if not opts["render"]:
        return
    out_dir = os.path.dirname(spec["out"]) or "."
    os.makedirs(out_dir, exist_ok=True)
    if opts["still"] is not None:
        sc.frame_set(opts["still"])
        sc.render.image_settings.file_format = "PNG"
        sc.render.filepath = f"{spec['out']}_f{opts['still']:04d}.png"
        bpy.ops.render.render(write_still=True)
    else:
        try:
            sc.render.image_settings.file_format = "FFMPEG"
            sc.render.ffmpeg.format = "MPEG4"
            sc.render.ffmpeg.codec = "H264"
        except TypeError:  # Blender build without FFmpeg (e.g. the pip 'bpy' module): PNG sequence instead
            print("[evg] note: FFMPEG not available, writing a PNG sequence (assemble with ffmpeg later)")
            sc.render.image_settings.file_format = "PNG"
            sc.render.filepath = spec["out"] + "_"
        bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()
