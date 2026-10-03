"""Camera presets for 16:9 and 9:16 (STYLE_GUIDE section 4).

F-stops are high on purpose: a kitten is 0.3 m deep, so real f/2.8 close-ups would blur half the face. Background blur comes from distance.
Sensor fit is HORIZONTAL so a lens means the same thing in both aspects; 9:16 uses its own (longer) lens
so subjects stay big enough for Shorts. Distances/heights are metres in storybook scale (kitten shoulder ~0.22 m).
"""
import math

import bpy
from mathutils import Vector

# name: (lens_16x9, lens_9x16, height, distance, fstop, note)
PRESETS = {
    "wide_establish":    (24, 28, 1.3, 11.0, 22.0, "arrival / place reveal, characters tiny, sky 50%"),
    "wide_two":          (28, 40, 0.35, 3.5, 16.0, "walking / travelling"),
    "medium_two":        (40, 60, 0.25, 1.8, 11.0, "dialogue, two characters"),
    "medium_single":     (50, 70, 0.22, 1.25, 11.0, "one speaker"),
    "close_up":          (85, 110, 0.20, 0.8, 11.0, "emotion / reaction"),
    "extreme_close_tag": (100, 135, 0.15, 0.4, 22.0, "glowing tag / bell"),
    "low_hero":          (28, 40, 0.08, 1.2, 11.0, "brave moment, landmark behind (tilts up ~10 deg)"),
    "over_shoulder":     (50, 70, 0.25, 1.0, 11.0, "look at the place"),
}
ASPECTS = {"16:9": (1920, 1080), "9:16": (1080, 1920)}

# safe areas as fractions of the frame: (left, top, right, bottom)
SAFE = {
    "16:9": {"action": (0.035, 0.035, 0.965, 0.965), "title": (0.05, 0.05, 0.95, 0.95), "subtitle_band": (0.08, 0.74, 0.92, 0.91)},
    "9:16": {"content": (0.055, 0.13, 0.85, 0.73), "caption_band": (0.055, 0.73, 0.85, 0.81)},
}


def _set_resolution(aspect):
    w, h = ASPECTS[aspect]
    r = bpy.context.scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100


def place_camera(preset, subject=(0, 0, 0.15), yaw_deg=0.0, aspect="16:9", name="cam", dof=True,
                 distance_scale=1.0, look_offset=(0, 0, 0), tilt_deg=None):
    """Create the scene camera from a preset. yaw_deg orbits around the subject (0 = looking along +Y from -Y)."""
    lens16, lens9, height, dist, fstop, _ = PRESETS[preset]
    cam_data = bpy.data.cameras.new(name)
    cam_data.sensor_fit = "HORIZONTAL"
    cam_data.sensor_width = 36.0
    cam_data.lens = lens16 if aspect == "16:9" else lens9
    cam_data.clip_start = 0.02
    cam_data.clip_end = 2000.0
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)

    s = Vector(subject)
    yaw = math.radians(yaw_deg)
    d = dist * distance_scale
    cam.location = Vector((s.x + math.sin(yaw) * d, s.y - math.cos(yaw) * d, height))
    target = s + Vector(look_offset)
    if preset == "low_hero" or tilt_deg is not None:
        tilt = math.radians(10 if tilt_deg is None else tilt_deg)
        heading = math.atan2(target.x - cam.location.x, target.y - cam.location.y)
        cam.rotation_euler = (math.pi / 2 + tilt, 0, -heading)
    else:
        cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()

    if dof:
        cam_data.dof.use_dof = True
        focus = bpy.data.objects.new(f"{name}_focus", None)
        bpy.context.scene.collection.objects.link(focus)
        focus.location = target + (Vector((0, 0, 0)) if preset == "extreme_close_tag" else Vector((0, -0.08, 0.07)))  # on the face (tag shots: on the subject itself)
        cam_data.dof.focus_object = focus
        cam_data.dof.aperture_fstop = fstop
    bpy.context.scene.camera = cam
    _set_resolution(aspect)
    return cam


def place_raw_camera(pos, look_at, lens_mm=45, aspect="16:9", name="cam"):
    """Legacy shot-spec camera (pos / look_at / lens_mm)."""
    cam_data = bpy.data.cameras.new(name)
    cam_data.sensor_fit = "HORIZONTAL"
    cam_data.lens = lens_mm
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = pos
    cam.rotation_euler = (Vector(look_at) - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    _set_resolution(aspect)
    return cam
