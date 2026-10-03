"""Scene + render setup, simple placeholder backgrounds, background loading."""
import os

import bpy

from . import toon
from .palette import VARIANTS

ENGINES = ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE")  # 4.2-4.5 / 5.x


def setup_render(fps=24, duration_s=4.0, samples=64, engine=None, view="Standard", look="None"):
    """EEVEE, Standard view transform (keeps flat toon hexes exact; AgX/Filmic wash them out), no outlines. Toon materials need EEVEE (Shader to RGB)."""
    sc = bpy.context.scene
    avail = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    sc.render.engine = engine if engine in avail else next(e for e in ENGINES if e in avail)
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 1, max(1, int(fps * duration_s))
    try:
        sc.eevee.taa_render_samples = samples
    except Exception:
        pass
    try:
        sc.view_settings.view_transform = view
        sc.view_settings.look = look
    except Exception:
        pass
    sc.render.film_transparent = False
    sc.render.use_motion_blur = False
    return sc


def placeholder_ground(variant="golden", size=60, hex_color="#8CBF6A"):
    """Flat toon ground so test shots have something under the feet."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    g = bpy.context.active_object
    g.name = "BG_placeholder_ground"
    g.data.materials.append(toon.simple_material("BG_ground", hex_color, rim_strength=0, threshold=0.2))
    return g


def load_background(name, variant="golden"):
    """Append collection <name> from scenes/<name>.blend (see design/blender/SETUP.md). Falls back to a placeholder ground."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pipeline/
    path = os.path.join(root, "scenes", f"{name}.blend")
    if not os.path.exists(path):
        print(f"[evg] note: {path} not found, using placeholder ground")
        return placeholder_ground(variant)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c.startswith(name.upper()) or c == name]
    for c in dst.collections:
        bpy.context.scene.collection.children.link(c)
    return dst.collections


def save_debug_blend(path):
    bpy.ops.wm.save_as_mainfile(filepath=path)
