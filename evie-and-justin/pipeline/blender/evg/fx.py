"""Glow and sparkle effects: the special-drink prop, paw-tag / bell 'discovery' glow, sparkle bursts.

All effects are keyframed from Python (no particle system), so they render identically in EEVEE and are easy to re-time.
See design/props/SPECIAL_DRINK.md and design/blender/FX_GLOW.md.
Spec (in a shot JSON):  "fx": [
  {"type": "tag_glow",  "characters": ["evie", "justin"], "frame": 12, "length": 48, "peak": 2.6},
  {"type": "sparkles",  "pos": [0, -0.3, 0.2], "frame": 12, "count": 36, "color": "#FFE08A"},
  {"type": "drink",     "pos": [0, -0.4, 0.0], "option": "blossom", "frame": 1},
  {"type": "tag_state", "characters": ["evie", "justin"], "state": "safe",   "frame": 12, "length": 72},
  {"type": "tag_state", "characters": ["evie"],           "state": "unsafe", "frame": 12, "length": 72},
  {"type": "pouch_peek", "characters": ["evie"], "frame": 12, "length": 72},            # faint lilac glow from Evie's pouch (Ep.4, Ep.7 opening)
  {"type": "pouch_open", "characters": ["evie"], "frame": 12, "length": 72},            # Ep.7: pouch opened for the lambs (SPOILER)
  {"type": "bell_glow", "characters": ["cotton", "toffee"], "frame": 12, "length": 72}      # Ep.7 spoiler: never in Shorts before release
]
"""
import math
import random

import bpy

from . import toon
from .palette import BELL_DRINK, DRINK, GOLD, POUCH, TAG_STATE, hex_to_linear_rgba


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


# ---------------------------------------------------------------- paw symbol + safety state (green / red)
PAW_BASE = "#C77F0E"   # darker gold: the embossed paw on the gold tag when no state is active
def _poly(name, polys):
    """Flat polygons (list of vertex lists, XY plane, normal +Z) -> one mesh."""
    me = bpy.data.meshes.new(name)
    verts, faces = [], []
    for poly in polys:
        i = len(verts)
        verts += [(x, y, 0.0) for x, y in poly]
        faces.append(tuple(range(i, i + len(poly))))
    me.from_pydata(verts, [], faces)
    me.update()
    return me


def _ellipse(cx, cy, rx, ry, n=20):
    return [(cx + math.cos(i * math.tau / n) * rx, cy + math.sin(i * math.tau / n) * ry) for i in range(n)]


def _stroke(p0, p1, w):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]


def paw_mesh():
    """Paw print (big pad + 4 toes), unit size ~ 1.0 wide, normal +Z."""
    return _poly("evg_paw", [_ellipse(0, -0.18, 0.30, 0.24), _ellipse(-0.36, 0.14, 0.12, 0.16), _ellipse(-0.13, 0.36, 0.12, 0.17),
                             _ellipse(0.13, 0.36, 0.12, 0.17), _ellipse(0.36, 0.14, 0.12, 0.16)])


def check_mesh():
    return _poly("evg_check", [_stroke((-0.34, -0.02), (-0.10, -0.28), 0.17), _stroke((-0.10, -0.28), (0.36, 0.30), 0.17)])


def cross_mesh():
    return _poly("evg_cross", [_stroke((-0.30, 0.30), (0.30, -0.30), 0.17), _stroke((0.30, 0.30), (-0.30, -0.30), 0.17)])


def ring_mesh(segments=1, gap=0.0, r_in=0.92, r_out=1.12, n=48):
    """Ring around the tag. segments=1, gap=0 -> solid ring (SAFE). segments=8, gap=0.4 -> dashed ring (UNSAFE)."""
    polys = []
    per = n // segments
    on = max(1, int(per * (1 - gap)))
    for sgm in range(segments):
        a0 = sgm * per
        pts_o = [(math.cos((a0 + i) * math.tau / n) * r_out, math.sin((a0 + i) * math.tau / n) * r_out) for i in range(on + 1)]
        pts_i = [(math.cos((a0 + i) * math.tau / n) * r_in, math.sin((a0 + i) * math.tau / n) * r_in) for i in range(on, -1, -1)]
        polys.append(pts_o + pts_i)
    return _poly(f"evg_ring_{segments}_{int(gap * 100)}", polys)


def _tag_frame(tag):
    """(parent, radius, z_offset): children are built as unit-size flat shapes in the +Z-facing frame of `parent`.
    Real models: create an Empty named '<tag.name>_face' at the tag centre, Z pointing out of the tag, parented to the tag/bone;
    custom property radius = tag radius in metres (default 0.012). Placeholders (unit disc scaled) use the tag itself."""
    face = bpy.data.objects.get(f"{tag.name}_face")
    if face is not None:
        r = float(face.get("radius", 0.012))
        return face, r, 0.0005
    return tag, 1.0, 1.06


def make_tag_disc(name, location=(0, 0, 0), radius=0.012, parent=None, parent_bone=None, facing=(0, -1, 0)):
    """Plain gold tag disc (toon gold, NO paw print) + '<name>_tag_face' Empty (Z out of the tag, custom prop radius).
    Use this for real models: delete the Meshy tag (its paw print is baked in the texture and cannot change state), build this one,
    parent it to the 'tag.01' bone (parent=<armature>, parent_bone='tag.01'). The paw symbol, glyphs and rings come from tag_state().
    facing = world direction the tag looks at when the character faces -Y."""
    from mathutils import Vector
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=radius * 0.25, location=location)
    disc = bpy.context.active_object
    disc.name = f"{name}_tag"
    bpy.ops.object.shade_smooth()
    disc.data.materials.append(toon.gold_material())
    disc.rotation_euler = Vector(facing).to_track_quat("Z", "Y").to_euler()
    face = bpy.data.objects.new(f"{disc.name}_face", None)
    face["radius"] = radius
    face.empty_display_type = "ARROWS"
    face.empty_display_size = radius
    bpy.context.scene.collection.objects.link(face)
    face.parent = disc
    face.location = (0, 0, radius * 0.125)   # on the front face
    if parent is not None:
        disc.parent = parent
        if parent_bone:
            disc.parent_type = "BONE"
            disc.parent_bone = parent_bone
    return disc


def ensure_tag_symbols(tag):
    """Create (once) the paw symbol, check, cross, solid ring and dashed ring as children of the tag. Returns a dict of the objects.
    All are emissive and hidden (scale 0) until a tag_state keyframes them."""
    key = "evg_tag_symbols"
    if tag.get(key):
        return {n: bpy.data.objects[tag[f"{key}_{n}"]] for n in ("paw", "check", "cross", "ring_safe", "ring_unsafe")}
    parent, r, z = _tag_frame(tag)
    gold = glow_material("tagsym_paw", PAW_BASE, 0.9)
    white = glow_material("tagsym_glyph", TAG_STATE["glyph"], 1.4)
    ringm = glow_material("tagsym_ring", GOLD, 1.0)
    meshes = {"paw": (paw_mesh(), gold, 0.78, 0.03), "check": (check_mesh(), white, 0.80, 0.06), "cross": (cross_mesh(), white, 0.80, 0.06),
              "ring_safe": (ring_mesh(1, 0.0), ringm, 1.0, 0.0), "ring_unsafe": (ring_mesh(8, 0.45), ringm, 1.0, 0.0)}
    out = {}
    for n, (me, mat, size, dz) in meshes.items():
        o = bpy.data.objects.new(f"{tag.name}_{n}", me)
        o.data.materials.append(mat if n != "ring_unsafe" else mat.copy())
        o.parent = parent
        o.location = (0, 0, z + dz * r)
        o.scale = (size * r,) * 3
        o["base_scale"] = size
        bpy.context.scene.collection.objects.link(o)
        tag[f"{key}_{n}"] = o.name
        out[n] = o
    tag[key] = True
    # paw is visible all the time (gold = neutral); glyph/rings appear only in a state
    for n in ("check", "cross", "ring_safe", "ring_unsafe"):
        out[n].hide_render = False
        _scale_key(out[n], 1, 0.0)
    return out


def _scale_key(o, frame, mult):
    r = 1.0
    if o.parent is not None and o.parent.name.endswith("_face"):
        r = float(o.parent.get("radius", 0.012))
    v = o["base_scale"] * r * mult
    o.scale = (v, v, v)
    o.keyframe_insert("scale", frame=frame)


def _color_keys(mat, keys):
    em = next(n for n in mat.node_tree.nodes if n.type == "EMISSION")
    for f, hexcol, strength in keys:
        em.inputs["Color"].default_value = hex_to_linear_rgba(hexcol)
        em.inputs["Strength"].default_value = strength
        em.inputs["Color"].keyframe_insert("default_value", frame=f)
        em.inputs["Strength"].keyframe_insert("default_value", frame=f)


def _hold(frame):
    return max(1, frame - 1)


def tag_state(root, state="safe", frame=12, length=72, light_peak=30.0):
    """Paw symbol on the tag: 'safe' -> MINT-AQUA, check-mark, solid ring, slow smooth pulse, soft light;
    'unsafe' -> DEEP RED, X, dashed ring, fast hard double-blink, red light; 'off' -> back to gold at `frame`.
    Cues never rely on colour alone (see design/blender/FX_GLOW.md section 8 and the sound table).
    Peak look is reached at frame + 6 and held to frame + length - 8; then returns to gold."""
    tags = [t for t in find_tags(root) if "_bell" not in t.name.lower()]
    n = 0
    for tag in tags:
        sym = ensure_tag_symbols(tag)
        # each tag gets its own materials so characters can differ
        for k in ("paw", "check", "cross", "ring_safe", "ring_unsafe"):
            o = sym[k]
            if not o.get("own_mats"):
                o.material_slots[0].material = o.material_slots[0].material.copy()
                o["own_mats"] = True
        paw_m, ring_s, ring_u = (sym["paw"].material_slots[0].material, sym["ring_safe"].material_slots[0].material,
                                 sym["ring_unsafe"].material_slots[0].material)
        f0, f_peak, f_end = frame, frame + 6, frame + length
        if state == "off":      # back to neutral gold at `frame`; glyph and rings disappear
            _color_keys(paw_m, [(f0, PAW_BASE, 0.9)])
            for k in ("check", "cross", "ring_safe", "ring_unsafe"):
                _scale_key(sym[k], f0, 0.0)
            n += 1
            continue
        col = TAG_STATE[state]
        glyph = sym["check"] if state == "safe" else sym["cross"]
        ring = sym["ring_safe"] if state == "safe" else sym["ring_unsafe"]
        ring_mat = ring_s if state == "safe" else ring_u
        # paw colour: gold -> state colour -> hold with pulse -> gold
        keys = [(_hold(f0), PAW_BASE, 0.9), (f_peak, col, 1.4)]
        if state == "safe":      # slow smooth pulse: one swell every 36 frames
            t = f_peak
            while t + 18 < f_end - 8:
                keys += [(t + 18, col, 1.0), (t + 36, col, 1.4)]
                t += 36
        else:                    # fast, hard, three-flash pattern every 18 frames then a pause (step keys: value jumps in one frame)
            t = f_peak
            while t + 18 < f_end - 8:
                for dt, v in ((0, 1.7), (3, 0.5), (4, 1.7), (7, 0.5), (8, 1.7), (11, 0.5)):
                    prev = keys[-1][2]
                    keys += [(t + dt - 1, col, prev), (t + dt, col, v)]
                t += 18
        keys = sorted(set(keys), key=lambda k: (k[0], k[2]))
        keys += [(f_end - 8, col, 1.2), (f_end, PAW_BASE, 0.9)]
        _color_keys(paw_m, keys)
        _color_keys(ring_mat, [(_hold(f0), col, 0.0), (f_peak, col, 1.3), (f_end - 8, col, 1.1), (f_end, col, 0.0)])
        # glyph + ring pop in
        for o, mult in ((glyph, 1.0), (ring, 1.0)):
            _scale_key(o, _hold(f0), 0.0)
            _scale_key(o, f_peak, mult * 1.15)
            _scale_key(o, f_peak + 4, mult)
            _scale_key(o, f_end - 8, mult)
            _scale_key(o, f_end, 0.0)
        if state == "unsafe":    # dashed ring slowly wobbles/rotates (extra non-colour cue)
            ring.rotation_euler = (0, 0, 0)
            ring.keyframe_insert("rotation_euler", frame=f_peak)
            ring.rotation_euler = (0, 0, math.radians(120))
            ring.keyframe_insert("rotation_euler", frame=f_end)
        # coloured light on the tag
        data = bpy.data.lights.new(f"TAGSTATE_{tag.name}", "POINT")
        data.color = hex_to_linear_rgba(col)[:3]
        data.shadow_soft_size = 0.01
        lo = bpy.data.objects.new(f"TAGSTATE_{tag.name}", data)
        lo.parent = tag
        lo.location = (0, -0.03, 0)
        bpy.context.scene.collection.objects.link(lo)
        for f, v in ((_hold(f0), 0.0), (f_peak, light_peak), (f_end - 8, light_peak * 0.7), (f_end, 0.0)):
            data.energy = v
            data.keyframe_insert("energy", frame=f)
        n += 1
    return n


# ---------------------------------------------------------------- lamb bells receive the drink (Ep.7, SPOILER)
def bell_glow(root, frame=12, length=72, peak=2.8):
    """Gold heart bell glows lilac/gold: emission swell + lilac light + expanding lilac ring + sparkle burst at the bell.
    SPOILER asset for Ep.7: do not use in Shorts/thumbnails before the episode is released (shot spec: "spoiler": "ep07")."""
    n = 0
    bpy.context.view_layer.update()   # world matrices must be current to place the sparkles on the bell
    for bell in [b for b in find_tags(root) if "_bell" in b.name.lower()]:
        if bell.material_slots:
            mat = bell.material_slots[0].material.copy()
            mat.name = f"{bell.name}_glow"
            bell.material_slots[0].material = mat
            animate_emission(mat, [(frame, 1.0), (frame + length // 4, peak), (frame + length, 1.0)])
        data = bpy.data.lights.new(f"BELL_glow_{bell.name}", "POINT")
        data.color = hex_to_linear_rgba(BELL_DRINK["lilac"])[:3]
        data.shadow_soft_size = 0.01
        lo = bpy.data.objects.new(f"BELL_glow_{bell.name}", data)
        lo.parent = bell
        lo.location = (0, -0.03, 0)
        bpy.context.scene.collection.objects.link(lo)
        for f, v in ((frame, 0.0), (frame + length // 4, 35.0), (frame + length, 0.0)):
            data.energy = v
            data.keyframe_insert("energy", frame=f)
        # three expanding lilac rings, facing the camera; not parented (the bell's non-uniform scale would shrink them): follows the bell by constraint
        ring = bpy.data.objects.new(f"{bell.name}_pulse", ring_mesh(1, 0.0, 0.9, 1.0))
        ring.data.materials.append(glow_material(f"bell_pulse_{bell.name}", BELL_DRINK["lilac"], 1.3))
        bpy.context.scene.collection.objects.link(ring)
        cl = ring.constraints.new("COPY_LOCATION")
        cl.target = bell
        cam = bpy.context.scene.camera
        if cam is not None:
            c = ring.constraints.new("TRACK_TO")
            c.target, c.track_axis, c.up_axis = cam, "TRACK_Z", "UP_Y"
        for k in range(3):
            t0 = frame + 2 + k * 14
            for f, sc in ((t0 - 1, 0.0), (t0, 0.012), (t0 + 12, 0.075), (t0 + 13, 0.0)):
                ring.scale = (sc, sc, sc)
                ring.keyframe_insert("scale", frame=f)
        sparkle_burst(tuple(bell.matrix_world.translation), 24, BELL_DRINK["lilac"], frame + 2, length // 2, 0.07, 0.1, size=1.6, seed=7)
        sparkle_burst(tuple(bell.matrix_world.translation), 14, BELL_DRINK["gold"], frame + 6, length // 2, 0.06, 0.12, size=1.3, seed=9)
        n += 1
    return n


# ---------------------------------------------------------------- Evie's pouch
def make_pouch(root, cloth="lilac", offset=(0.05, -0.215, 0.145), scale=1.0, parent=None):
    """Tiny chunky cloth pouch on a short strap from Evie's collar, beside the paw tag (placeholder-sized: collar front at y -0.225, z 0.19).
    Parts (all named '<name>_pouch*'): sack, neck ring, lip (open top), inside (dark), drawstring ring, strap, glow (hidden until used).
    For real models: build it by hand the same way (see design/character-sheets/evie.md) and parent to the 'collar_root' bone:
    parent=<armature>, parent_bone is set by the caller. Keeps clear of the tag (>= 1.5 cm gap) and of the neck."""
    name = root.name.replace("_root", "")
    cloth_hex = POUCH["cloth"] if cloth == "lilac" else POUCH["cloth_cream"]
    m_cloth = toon.simple_material("pouch_cloth", cloth_hex, rim_strength=0.2)
    m_string = toon.simple_material("pouch_string", POUCH["string"], rim_strength=0.1)
    m_strap = toon.simple_material("pouch_strap", POUCH["strap"], rim_strength=0.1)
    m_in = toon.simple_material("pouch_inside", POUCH["inside"], rim_strength=0, threshold=0.0)
    s = scale
    ox, oy, oz = (offset[0] * s, offset[1] * s, offset[2] * s)
    anchor = bpy.data.objects.new(f"{name}_pouch", None)
    bpy.context.scene.collection.objects.link(anchor)
    anchor.parent = parent or root
    anchor.location = (ox, oy, oz)

    def prim(kind, nm, loc, sc, mat, rot=None, **kw):
        if kind == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=(0, 0, 0))
        elif kind == "cyl":
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=1, depth=2, location=(0, 0, 0))
        elif kind == "cone":
            bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=1, radius2=kw.get("r2", 0.6), depth=2, location=(0, 0, 0))
        elif kind == "torus":
            bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=kw.get("minor", 0.2), location=(0, 0, 0))
        o = bpy.context.active_object
        o.name = f"{name}_pouch_{nm}"
        o.parent = anchor
        o.location = tuple(c * s for c in loc)
        o.scale = tuple(c * s for c in sc)
        if rot:
            o.rotation_euler = rot
        bpy.ops.object.shade_smooth()
        o.data.materials.append(mat)
        return o

    prim("sphere", "sack", (0, 0, -0.012), (0.017, 0.015, 0.019), m_cloth)                       # plump bag
    prim("cone", "lip", (0, 0, 0.0115), (0.0105, 0.0105, 0.005), m_cloth, r2=0.8)               # short flared opening
    prim("cyl", "inside", (0, 0, 0.0162), (0.0078, 0.0078, 0.0004), m_in)                        # dark interior seen from above/front
    prim("torus", "string", (0, 0, 0.0075), (0.0097, 0.0097, 0.0097), m_string, minor=0.13)     # drawstring cinch
    for sx in (-1, 1):                                                                               # two tiny string ends
        prim("sphere", f"tassel{sx}", (sx * 0.006, -0.0105, 0.001), (0.0022, 0.0022, 0.0045), m_string)
    prim("cyl", "strap", (0, 0.004, 0.032), (0.0016, 0.0016, 0.0135), m_strap)                   # strap up to the collar
    glow = prim("sphere", "glow", (0, 0, 0.0185), (0.0074, 0.0074, 0.0048), glow_material(f"{name}_pouch_glow_mat", POUCH["glow"], 0.0))
    glow["peek"] = True
    return anchor


def _pouch_parts(root):
    p = {o.name.split("_pouch_")[-1]: o for o in root.children_recursive if "_pouch_" in o.name}
    return p


def pouch_peek(root, frame=12, length=72, peak=0.9, light_peak=3.0):
    """FAINT lilac glow from the pouch opening (Ep.4 tease, Ep.7 opening beat): glow disc emission 0 -> peak -> 0 with a slow breath,
    a very soft lilac light on the collar fur, and 6 tiny lilac sparkles drifting up. Deliberately subtle: a hint, not a reveal.
    Keep peak <= ~1.2 (Standard view), light_peak small. Spoiler rule: fine in episodes; check the script before using it in a Short."""
    parts = _pouch_parts(root)
    glow = parts.get("glow")
    if glow is None:
        print(f"[evg] note: no pouch on {root.name} (add \"pouch\": true to the character or fx type 'pouch')")
        return 0
    bpy.context.view_layer.update()
    mat = glow.material_slots[0].material
    f0, f1, f2 = frame, frame + length // 3, frame + length
    breath = [(f0, 0.0), (f1, peak), (f1 + length // 6, peak * 0.7), (f1 + length // 3, peak), (f2, 0.0)]
    animate_emission(mat, breath)
    data = bpy.data.lights.new(f"POUCH_glow_{root.name}", "POINT")
    data.color = hex_to_linear_rgba(POUCH["glow"])[:3]
    data.shadow_soft_size = 0.02
    lo = bpy.data.objects.new(f"POUCH_glow_{root.name}", data)
    lo.parent = glow
    lo.location = (0, -0.4, 0.6)
    bpy.context.scene.collection.objects.link(lo)
    for f, v in breath:
        data.energy = v / max(peak, 0.01) * light_peak
        data.keyframe_insert("energy", frame=f)
    sparkle_burst(tuple(glow.matrix_world.translation), 6, POUCH["glow"], f1, length // 2, 0.015, 0.05, size=0.5, seed=11, strength=1.6)
    return 1


def pouch_open(root, frame=12, length=72, peak=1.5):
    """Ep.7 opening moment (SPOILER): drawstring loosens (ring scales up, lip flares), glow rises, a petal's lilac+gold sparkle burst rises out."""
    parts = _pouch_parts(root)
    if "string" not in parts:
        print(f"[evg] note: no pouch on {root.name}")
        return 0
    bpy.context.view_layer.update()
    ring, lip = parts["string"], parts["lip"]
    for o, mult in ((ring, 1.45), (lip, 1.25)):
        base = tuple(o.scale)
        o.keyframe_insert("scale", frame=frame)
        o.scale = tuple(v * mult for v in base)
        o.keyframe_insert("scale", frame=frame + length // 4)
        o.keyframe_insert("scale", frame=frame + length - 6)
        o.scale = base
        o.keyframe_insert("scale", frame=frame + length)
    pouch_peek(root, frame, length, peak=peak, light_peak=8.0)
    top = tuple(parts["glow"].matrix_world.translation)
    sparkle_burst(top, 22, POUCH["glow"], frame + length // 4, length // 2, 0.04, 0.12, size=1.0, seed=21)
    sparkle_burst(top, 12, GOLD, frame + length // 4 + 4, length // 2, 0.035, 0.14, size=0.9, seed=23)
    return 1


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
        elif t == "tag_state":
            for n in fx.get("characters", list(roots_by_name)):
                if n in roots_by_name:
                    tag_state(roots_by_name[n], fx.get("state", "safe"), fx.get("frame", 12), fx.get("length", 72))
        elif t == "pouch":
            for n in fx.get("characters", list(roots_by_name)):
                if n in roots_by_name:
                    make_pouch(roots_by_name[n], fx.get("cloth", "lilac"))
        elif t == "pouch_peek":
            for n in fx.get("characters", ["evie"]):
                if n in roots_by_name:
                    pouch_peek(roots_by_name[n], fx.get("frame", 12), fx.get("length", 72), fx.get("peak", 0.9))
        elif t == "pouch_open":
            for n in fx.get("characters", ["evie"]):
                if n in roots_by_name:
                    pouch_open(roots_by_name[n], fx.get("frame", 12), fx.get("length", 72), fx.get("peak", 1.5))
        elif t == "bell_glow":
            for n in fx.get("characters", list(roots_by_name)):
                if n in roots_by_name:
                    bell_glow(roots_by_name[n], fx.get("frame", 12), fx.get("length", 72), fx.get("peak", 2.8))
        elif t == "drink":
            make_drink_placeholder(fx.get("option", "blossom"), tuple(fx.get("pos", (0, 0, 0))), fx.get("scale", 1.0), frame=fx.get("frame", 1))
        else:
            print(f"[evg] note: unknown fx type {t!r}")
