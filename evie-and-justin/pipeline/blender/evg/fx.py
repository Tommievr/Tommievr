"""Glow and sparkle effects: the special-drink prop, paw-tag / bell 'discovery' glow, sparkle bursts.

All effects are keyframed from Python (no particle system), so they render identically in EEVEE and are easy to re-time.
See design/props/SPECIAL_DRINK.md and design/blender/FX_GLOW.md.
Spec (in a shot JSON):  "fx": [
  {"type": "tag_glow",  "characters": ["evie", "justin"], "frame": 12, "length": 48, "peak": 2.6},
  {"type": "sparkles",  "pos": [0, -0.3, 0.2], "frame": 12, "count": 36, "color": "#FFE08A"},
  {"type": "drink",     "pos": [0, -0.4, 0.0], "option": "blossom", "frame": 1}
]
"""
import math
import random

import bpy

from . import toon
from .palette import DRINK, GOLD, hex_to_linear_rgba


# ---------------------------------------------------------------- emission helpers
def glow_material(name, hex_color, strength=1.5):
    """Pure emissive material (flat colour, no shading): for the liquid, sparkles, orbs.
    Keep strength <= ~2.5 with the Standard view transform: higher values clip to white and lose the colour; get the bloom from the
    compositor Glare node / a point light instead (design/blender/FX_GLOW.md)."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = hex_to_linear_rgba(hex_color)
    em.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def _emission_input(mat):
    for n in mat.node_tree.nodes:
        if n.type == "EMISSION":
            return n.inputs["Strength"]
    return None


def animate_emission(mat, keys):
    """keys = [(frame, strength), ...] keyframes the material's Emission strength."""
    sock = _emission_input(mat)
    if sock is None:
        return False
    for f, v in keys:
        sock.default_value = v
        sock.keyframe_insert("default_value", frame=f)
    return True


# ---------------------------------------------------------------- tag / bell discovery glow
def find_tags(root):
    """Objects under a character root that look like the gold paw tag or bell."""
    return [o for o in root.children_recursive if o.type == "MESH" and any(t in o.name.lower() for t in ("_tag", "_bell"))]


def tag_glow(root, frame=12, length=48, peak=2.6, color_hex=DRINK["sparkle"], light_peak=40.0):
    """The 'adventure badge' pulse: tag/bell emission 1 -> peak -> 1 and a warm point light 0 -> light_peak -> 0.
    Peak at frame + length * 0.25; ease out slowly. Each tag gets its own material copy so characters glow independently."""
    f0, f1, f2 = frame, frame + max(2, int(length * 0.25)), frame + length
    n = 0
    for tag in find_tags(root):
        if not tag.material_slots:
            continue
        mat = tag.material_slots[0].material.copy()
        mat.name = f"{tag.name}_glow"
        tag.material_slots[0].material = mat
        # make sure there is an emission node to animate: toon materials end in Emission(strength 1)
        if animate_emission(mat, [(f0, 1.0), (f1, peak), (f2, 1.0)]):
            n += 1
        data = bpy.data.lights.new(f"TAG_glow_{tag.name}", "POINT")
        data.color = hex_to_linear_rgba(color_hex)[:3]
        data.shadow_soft_size = 0.01
        lo = bpy.data.objects.new(f"TAG_glow_{tag.name}", data)
        lo.parent = tag
        lo.location = (0, -0.03, 0)
        bpy.context.scene.collection.objects.link(lo)
        for f, v in ((f0, 0.0), (f1, light_peak), (f2, 0.0)):
            data.energy = v
            data.keyframe_insert("energy", frame=f)
    return n


# ---------------------------------------------------------------- sparkles
def _star_mesh(name="evg_sparkle", r=0.012):
    """4-point star (two crossed thin diamonds) as one flat mesh facing -Y."""
    me = bpy.data.meshes.get(name)
    if me:
        return me
    me = bpy.data.meshes.new(name)
    pts = [(0, 0, r), (r * 0.28, 0, r * 0.28), (r, 0, 0), (r * 0.28, 0, -r * 0.28), (0, 0, -r), (-r * 0.28, 0, -r * 0.28),
           (-r, 0, 0), (-r * 0.28, 0, r * 0.28)]
    me.from_pydata(pts, [], [tuple(range(8))])
    me.update()
    return me


def sparkle_burst(center, count=36, color_hex=DRINK["sparkle"], frame=12, duration=48, radius=0.18, rise=0.25,
                  size=1.0, seed=3, strength=2.5, camera_facing=True):
    """A burst of little 4-point stars that pop out, drift up and fade (scale to 0). Returns the parent empty."""
    rng = random.Random(seed)
    mat = glow_material(f"sparkle_{color_hex.strip('#')}", color_hex, strength)
    mesh = _star_mesh()
    parent = bpy.data.objects.new("SPARKLES", None)
    parent.location = center
    bpy.context.scene.collection.objects.link(parent)
    cam = bpy.context.scene.camera
    for i in range(count):
        o = bpy.data.objects.new(f"sparkle_{i:02d}", mesh)
        o.data.materials.clear()
        o.data.materials.append(mat)
        o.parent = parent
        bpy.context.scene.collection.objects.link(o)
        ang = rng.uniform(0, math.tau)
        rad = radius * math.sqrt(rng.random())
        start = (math.cos(ang) * rad * 0.2, math.sin(ang) * rad * 0.2, 0)
        end = (math.cos(ang) * rad, math.sin(ang) * rad * 0.6, rng.uniform(0.3, 1.0) * rise)
        t0 = frame + rng.randint(0, max(1, duration // 3))
        t1 = t0 + rng.randint(duration // 3, duration // 2 + 1)
        s = size * rng.uniform(0.6, 1.5)
        o.location, o.scale = start, (0, 0, 0)
        o.keyframe_insert("location", frame=t0)
        o.keyframe_insert("scale", frame=t0)
        o.location, o.scale = end, (s, s, s)
        o.keyframe_insert("location", frame=(t0 + t1) // 2)
        o.keyframe_insert("scale", frame=(t0 + t1) // 2)
        o.location, o.scale = (end[0], end[1], end[2] + rise * 0.5), (0, 0, 0)
        o.keyframe_insert("location", frame=t1)
        o.keyframe_insert("scale", frame=t1)
        o.rotation_euler[1] = rng.uniform(0, math.tau)  # spin a little around the facing axis
        if camera_facing and cam is not None:
            c = o.constraints.new("TRACK_TO")
            c.target = cam
            c.track_axis = "TRACK_Y"      # star lies in the XZ plane, so its normal (-Y) must face the camera
            c.up_axis = "UP_Z"
    return parent


# ---------------------------------------------------------------- the special drink prop
def make_drink_placeholder(option="blossom", pos=(0, 0, 0), scale=1.0, glow_strength=1.5, frame=1):
    """Toon placeholder of the special drink (until the Meshy prop exists). Options: blossom | acorn | flask.
    Returns the parent empty. The liquid/orb is a separate glowing object named 'drink_glow' (animate/scale it freely)."""
    D = DRINK
    parent = bpy.data.objects.new(f"DRINK_{option}", None)
    parent.location = pos
    parent.scale = (scale,) * 3
    bpy.context.scene.collection.objects.link(parent)

    def prim(kind, name, loc, sc, mat, rot=None):
        if kind == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=loc)
        elif kind == "cyl":
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, location=loc)
        elif kind == "cone":
            bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1, radius2=0.55, depth=2, location=loc)
        o = bpy.context.active_object
        o.name = name
        o.scale = sc
        if rot:
            o.rotation_euler = rot
        bpy.ops.object.shade_smooth()
        o.data.materials.append(mat)
        o.parent = parent
        return o

    petal = toon.simple_material("drink_petal", D["petal"])
    green = toon.simple_material("drink_stem", D["stem"])
    wood = toon.simple_material("drink_acorn", D["acorn"])
    glass = toon.simple_material("drink_glass", D["glass"], rim_strength=0.6)
    cork = toon.simple_material("drink_cork", D["cork"])
    liquid = glow_material("drink_liquid", D["liquid"], glow_strength)
    x, y, z = 0.0, 0.0, 0.0   # children are placed in the parent's local space (parent already sits at pos)
    if option == "blossom":
        prim("cyl", "drink_stem", (x, y, z + 0.035), (0.006, 0.006, 0.035), green)
        for i in range(6):   # petals open outward like a cup: tilt about X, then spin about Z; positioned on the same outward direction
            a = i * math.tau / 6
            prim("sphere", f"drink_petal{i}", (x + math.sin(a) * 0.03, y - math.cos(a) * 0.03, z + 0.08), (0.018, 0.006, 0.034), petal,
                 rot=(math.radians(32), 0, a))
        orb = prim("sphere", "drink_glow", (x, y, z + 0.085), (0.02, 0.02, 0.02), liquid)
    elif option == "acorn":
        prim("sphere", "drink_cup", (x, y, z + 0.04), (0.035, 0.035, 0.03), wood)
        orb = prim("sphere", "drink_glow", (x, y, z + 0.062), (0.026, 0.026, 0.012), liquid)
        prim("cyl", "drink_foot", (x, y, z + 0.01), (0.012, 0.012, 0.01), wood)
    else:  # flask
        prim("sphere", "drink_flask", (x, y, z + 0.04), (0.035, 0.035, 0.04), glass)
        orb = prim("sphere", "drink_glow", (x, y, z + 0.04), (0.027, 0.027, 0.031), liquid)
        prim("cyl", "drink_neck", (x, y, z + 0.09), (0.011, 0.011, 0.02), glass)
        prim("cyl", "drink_cork", (x, y, z + 0.115), (0.013, 0.013, 0.008), cork)
    # gentle pulse so it feels alive
    animate_emission(liquid, [(frame, glow_strength * 0.8), (frame + 24, glow_strength * 1.3), (frame + 48, glow_strength * 0.8)])
    light = bpy.data.lights.new(f"drink_light_{option}", "POINT")
    light.color = hex_to_linear_rgba(D["liquid"])[:3]
    light.energy = 6.0
    light.shadow_soft_size = 0.02
    lo = bpy.data.objects.new(f"drink_light_{option}", light)
    lo.location = (x, y - 0.05, z + 0.1)
    lo.parent = parent
    bpy.context.scene.collection.objects.link(lo)
    return parent


def apply_fx(spec_fx, roots_by_name, fps=24):
    """Apply the "fx" list of a shot spec."""
    for fx in spec_fx or []:
        t = fx.get("type")
        if t == "tag_glow":
            for n in fx.get("characters", list(roots_by_name)):
                if n in roots_by_name:
                    tag_glow(roots_by_name[n], fx.get("frame", 12), fx.get("length", 48), fx.get("peak", 2.6))
        elif t == "sparkles":
            sparkle_burst(tuple(fx["pos"]), fx.get("count", 36), fx.get("color", DRINK["sparkle"]), fx.get("frame", 12),
                          fx.get("length", 48), fx.get("radius", 0.18), fx.get("rise", 0.25))
        elif t == "drink":
            make_drink_placeholder(fx.get("option", "blossom"), tuple(fx.get("pos", (0, 0, 0))), fx.get("scale", 1.0), frame=fx.get("frame", 1))
        else:
            print(f"[evg] note: unknown fx type {t!r}")
