"""Golden-hour light rig (STYLE_GUIDE section 3): key sun, cool fill, two rim lights, ground kick, optional tag glow.

build_rig() creates a collection 'RIG_Golden' and returns a dict of the objects. Rim and kick lights are
light-linked to the character collection (Blender 4.0+) so they never wash the background.
"""
import math

import bpy
from mathutils import Vector

from .palette import VARIANTS, hex_to_linear_rgba


def _aim(obj, target):
    """Rotate a light so its -Z axis points at target."""
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def _new_light(name, kind, color_hex, energy, location, target, coll, size=None):
    data = bpy.data.lights.new(name, kind)
    data.color = hex_to_linear_rgba(color_hex)[:3]
    data.energy = energy
    if kind == "SUN":
        data.angle = math.radians(5)
    elif kind == "AREA":
        data.shape = "DISK"
        data.size = size or 2.0
    obj = bpy.data.objects.new(name, data)
    obj.location = location
    coll.objects.link(obj)
    _aim(obj, target)
    return obj


def _link_to_collection(light_obj, receiver):
    """Light linking (Blender 4.0+). Silently skipped on older builds."""
    try:
        light_obj.light_linking.receiver_collection = receiver
    except Exception:
        pass


def set_world_gradient(top_hex, horizon_hex, strength=1.0, ambient=0.3):
    """Simple 2-colour sky gradient world. Camera sees it at full strength; lighting uses only `ambient` of it,
    so the toon shadow step stays visible (otherwise the sky fills the shadows and the look goes flat)."""
    world = bpy.context.scene.world or bpy.data.worlds.new("EVG_World")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    ramp = N.new("ShaderNodeValToRGB")
    bg = N.new("ShaderNodeBackground")
    out = N.new("ShaderNodeOutputWorld")
    ramp.color_ramp.elements[0].position = 0.48
    ramp.color_ramp.elements[0].color = hex_to_linear_rgba(horizon_hex)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = hex_to_linear_rgba(top_hex)
    lp = N.new("ShaderNodeLightPath")
    mad = N.new("ShaderNodeMath")
    mad.operation = "MULTIPLY_ADD"          # IsCameraRay * (1-ambient) + ambient
    mad.inputs[1].default_value = (1.0 - ambient) * strength
    mad.inputs[2].default_value = ambient * strength
    L.new(lp.outputs["Is Camera Ray"], mad.inputs[0])
    L.new(mad.outputs["Value"], bg.inputs["Strength"])
    L.new(tc.outputs["Generated"], sep.inputs["Vector"])
    L.new(sep.outputs["Z"], ramp.inputs["Fac"])
    L.new(ramp.outputs["Color"], bg.inputs["Color"])
    L.new(bg.outputs["Background"], out.inputs["Surface"])
    return world


def build_rig(variant="golden", target=(0, 0, 0.2), char_collection=None, camera_yaw_deg=0.0, scale=1.0, world=True):
    """Create the rig. camera_yaw_deg rotates the whole rig around Z to follow the camera side.

    Directions are relative to a camera looking along +Y from -Y: the key comes from front-right (azimuth +40 deg),
    rims from behind left/right. scale multiplies the light distances.
    """
    v = VARIANTS[variant]
    rig = bpy.data.collections.new("RIG_Golden")
    bpy.context.scene.collection.children.link(rig)
    t = Vector(target)

    def pos(az_deg, elev_deg, dist):
        az = math.radians(az_deg + camera_yaw_deg)
        el = math.radians(elev_deg)
        # azimuth 0 = camera side (-Y), +az swings to +X
        return t + Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))) * dist * scale

    objs = {}
    objs["key"] = _new_light("KEY_sun", "SUN", v["key"], v["key_w"], pos(v["sun_az"], v["sun_elev"], 20), t, rig)
    objs["fill"] = _new_light("FILL_sky", "AREA", v["fill"], v["fill_w"] * 120, pos(-50, 12, 4), t, rig, size=6 * scale)
    objs["rim_l"] = _new_light("RIM_L", "AREA", v["rim"], v["rim_w"] * 90, pos(-150, 28, 2.5), t, rig, size=1.5 * scale)
    objs["rim_r"] = _new_light("RIM_R", "AREA", v["rim"], v["rim_w"] * 90, pos(150, 28, 2.5), t, rig, size=1.5 * scale)
    objs["kick"] = _new_light("KICK_ground", "AREA", v["ground_bounce"], v["key_w"] * 10, pos(0, -8, 1.8), t, rig, size=2 * scale)
    if char_collection is not None:
        for k in ("rim_l", "rim_r", "kick"):
            _link_to_collection(objs[k], char_collection)
    if world:
        set_world_gradient(v["sky_top"], v["sky_horizon"], strength=1.0)
    return objs


def add_tag_glow(location, color_hex="#FFC76B", peak=40.0, frame_in=1, frame_peak=12, frame_out=36, char_collection=None):
    """Point light at a tag/bell that pulses 0 -> peak -> 0 (discovery moment)."""
    data = bpy.data.lights.new("TAG_glow", "POINT")
    data.color = hex_to_linear_rgba(color_hex)[:3]
    data.shadow_soft_size = 0.01
    obj = bpy.data.objects.new("TAG_glow", data)
    obj.location = location
    bpy.context.scene.collection.objects.link(obj)
    for f, val in ((frame_in, 0.0), (frame_peak, peak), (frame_out, 0.0)):
        data.energy = val
        data.keyframe_insert("energy", frame=f)
    if char_collection is not None:
        _link_to_collection(obj, char_collection)
    return obj
