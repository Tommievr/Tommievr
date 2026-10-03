"""Simple toon shading for EEVEE: Diffuse -> Shader to RGB -> hard colour ramp -> multiply base colour -> emission (+ rim).

Look: 2 flat tones (light + plum-tinted shadow), optional highlight band, thin warm rim. No textures needed;
if the Meshy model has a base-colour image it is reused (keep_texture=True) so painted markings survive.
Shader to RGB works in EEVEE only (not Cycles).
"""
import bpy

from .palette import GOLD, SHADE_TINT, hex_to_linear_rgba


def _ramp(nodes, positions_colors, interpolation="CONSTANT"):
    n = nodes.new("ShaderNodeValToRGB")
    n.color_ramp.interpolation = interpolation
    ramp = n.color_ramp
    # a ColorRamp starts with 2 elements: reuse them, add extras
    while len(ramp.elements) < len(positions_colors):
        ramp.elements.new(0.5)
    for el, (pos, col) in zip(ramp.elements, positions_colors):
        el.position = pos
        el.color = col
    return n


def _mix(nodes, blend, a=None, b=None, factor=1.0):
    n = nodes.new("ShaderNodeMix")
    n.data_type = "RGBA"
    n.blend_type = blend
    n.inputs[0].default_value = factor
    if a is not None:
        n.inputs[6].default_value = a
    if b is not None:
        n.inputs[7].default_value = b
    return n


def make_toon_material(name, base_hex, shade_tint=SHADE_TINT, threshold=0.45, highlight=0.0, softness=0.05,
                       rim_hex="#FFD9A8", rim_strength=0.35, rim_width=0.62, image=None, emission_boost=0.0, base_rgba=None):
    """Create (or rebuild) a toon material.

    base_hex     colour of the lit area. image: optional bpy.types.Image used instead of a flat colour.
    shade_tint   multiplied into the base in the shadow step (plum/violet; STYLE_GUIDE section 3.3).
    threshold    where light turns to shadow (0..1 of the diffuse lighting). Lower = less shadow. Ground at low sun: ~0.2.
    softness     half-width of the light/shadow edge (0 = razor sharp, 0.05 = soft-toon, less flicker/noise).
    highlight    0 = none; e.g. 0.92 adds a lighter band where light is strongest (good for gold parts).
    base_rgba    linear RGBA override of base_hex (used when converting existing materials).
    rim_strength 0 disables the rim. rim_width = Layer Weight facing cutoff (higher = thinner rim).
    """
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links

    out = N.new("ShaderNodeOutputMaterial")
    out.location = (1200, 0)
    diffuse = N.new("ShaderNodeBsdfDiffuse")
    diffuse.location = (-600, 0)
    diffuse.inputs["Color"].default_value = (1, 1, 1, 1)
    to_rgb = N.new("ShaderNodeShaderToRGB")
    to_rgb.location = (-400, 0)
    L.new(diffuse.outputs["BSDF"], to_rgb.inputs["Shader"])

    tint = hex_to_linear_rgba(shade_tint)
    lo, hi = max(0.0, threshold - softness), min(1.0, threshold + softness)
    stops = [(lo, tint), (hi, (1, 1, 1, 1))]
    if highlight:
        stops.append((highlight, (1.25, 1.25, 1.25, 1)))
        stops.append((min(1.0, highlight + 0.03), (1.25, 1.25, 1.25, 1)))
    ramp = _ramp(N, stops, "LINEAR")
    ramp.location = (-200, 0)
    L.new(to_rgb.outputs["Color"], ramp.inputs["Fac"])

    if image is not None:
        tex = N.new("ShaderNodeTexImage")
        tex.image = image
        tex.interpolation = "Linear"
        tex.location = (-200, -300)
        base_out = tex.outputs["Color"]
        shaded = _mix(N, "MULTIPLY")
        L.new(base_out, shaded.inputs[6])
    else:
        shaded = _mix(N, "MULTIPLY", a=base_rgba or hex_to_linear_rgba(base_hex))
    shaded.location = (100, 0)
    # multiply: A = base colour, B = ramp (light/shadow tint)
    L.new(ramp.outputs["Color"], shaded.inputs[7])
    last = shaded.outputs[2]

    if rim_strength > 0:
        lw = N.new("ShaderNodeLayerWeight")
        lw.inputs["Blend"].default_value = 0.35
        lw.location = (-400, 350)
        rim_ramp = _ramp(N, [(0.0, (0, 0, 0, 1)), (rim_width, (1, 1, 1, 1))])
        rim_ramp.location = (-200, 350)
        L.new(lw.outputs["Facing"], rim_ramp.inputs["Fac"])
        # ramp value (0 or 1) x rim colour*strength: a gentle uniform edge glow
        rim_col = _mix(N, "MULTIPLY", factor=1.0)
        rim_col.location = (100, 350)
        L.new(rim_ramp.outputs["Color"], rim_col.inputs[6])
        r, g, b, _a = hex_to_linear_rgba(rim_hex)
        rim_col.inputs[7].default_value = (r * rim_strength, g * rim_strength, b * rim_strength, 1)
        add = _mix(N, "ADD", factor=1.0)
        add.location = (400, 150)
        L.new(last, add.inputs[6])
        L.new(rim_col.outputs[2], add.inputs[7])
        last = add.outputs[2]

    emit = N.new("ShaderNodeEmission")
    emit.location = (800, 0)
    emit.inputs["Strength"].default_value = 1.0 + emission_boost
    L.new(last, emit.inputs["Color"])
    L.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat


def _is_toon(mat):
    return bool(mat and mat.use_nodes and any(n.type == "SHADERTORGB" for n in mat.node_tree.nodes))


def _principled_info(mat):
    """(image or None, linear rgba) of a material's base colour."""
    img, rgba = None, (0.8, 0.8, 0.8, 1.0)
    if not (mat and mat.use_nodes):
        return (None, tuple(mat.diffuse_color) if mat else rgba)
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            sock = n.inputs["Base Color"]
            rgba = tuple(sock.default_value)
            for link in sock.links:
                if link.from_node.type == "TEX_IMAGE" and link.from_node.image:
                    img = link.from_node.image
            break
    if img is None:
        for n in mat.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image and not any(t in n.image.name.lower() for t in ("normal", "rough", "metal")):
                img = n.image
                break
    return img, rgba


def convert_to_toon(obj, keep_texture=True, **kw):
    """Convert every material slot of a mesh to toon, one by one: each keeps its own base colour or base-colour image.
    Materials that are already toon (made by evg or the rig script) are left alone. Returns the list of new materials."""
    out = []
    if not obj.material_slots:
        m = make_toon_material(f"toon_{obj.name}", "#CCCCCC", **kw)
        obj.data.materials.append(m)
        return [m]
    for i, slot in enumerate(obj.material_slots):
        m = slot.material
        if m is None or _is_toon(m):
            continue
        img, rgba = _principled_info(m)
        new = make_toon_material(f"toon_{m.name}", "#CCCCCC", image=img if keep_texture else None, base_rgba=rgba, **kw)
        obj.data.materials[i] = new
        out.append(new)
    return out


def gold_material(name="toon_gold"):
    """Gold tag / bell: strong highlight band, brighter rim."""
    return make_toon_material(name, GOLD, shade_tint="#C98A3A", threshold=0.4, highlight=0.9,
                              rim_hex="#FFF1D6", rim_strength=0.5, rim_width=0.55)


def simple_material(name, hex_color, **kw):
    return make_toon_material(name, hex_color, **kw)
