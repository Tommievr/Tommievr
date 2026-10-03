# Toon shading recipe (EEVEE)
Look: **2 flat tones** (light and plum-tinted shadow), thin warm rim, flat saturated base colour, no texture noise. One material per colour area (fur, ears, collar, ...). Implemented in `pipeline/blender/evg/toon.py`; this is the same thing by hand.

## One-line script version
```python
from evg import toon
mat = toon.make_toon_material("evie_fur", "#FFF6EC")                    # base colour, default plum shadow, soft edge
gold = toon.gold_material()                                              # tag / bell: highlight band
dark = toon.make_toon_material("justin_fur", "#352B3D", rim_strength=0.5) # dark fur gets a stronger rim so it reads
toon.convert_to_toon(obj)                                                # convert all slots of an imported mesh (keeps image textures)
```
Parameters: `threshold` (0.45; light→shadow position; ground at low sun 0.2), `softness` (0.05: edge softness, less flicker), `shade_tint` (`#B8A4D8`), `highlight` (0 = none; 0.9 = lighter band), `rim_strength` (0.35; 0 = off), `rim_width` (0.62).

## By hand (Shading workspace, material per part)
Delete the Principled BSDF. Build:
1. **Diffuse BSDF** (Color white) → **Shader to RGB** → **Color Ramp**
   - Interpolation **Linear**; stop A at `0.40` = colour `#B8A4D8` (plum tint, the shadow); stop B at `0.50` = white. (Closer stops = harder edge.)
2. **Mix Color** (Blend **Multiply**, Factor 1): A = **base colour** (RGB node with the hex, or the Meshy **Image Texture**), B = the Color Ramp output.
3. **Rim:** **Layer Weight** (Blend 0.35) → output **Facing** → **Color Ramp** (Constant: black at 0, white at 0.62) → **Mix Color** (Multiply) with colour `#FFD9A8` × 0.35 → **Mix Color** (Blend **Add**, Factor 1) with the result of step 2.
4. → **Emission** (Strength 1) → **Material Output → Surface**.
Material Settings: leave defaults. Render engine **EEVEE** (*Shader to RGB* is EEVEE-only).

## Why emission?
The look is fully defined by the material, so it survives light changes and stays flat and clean; the diffuse term only decides where the shadow step falls. The rig's lights still matter: sun direction = shadow direction; rim lights separate characters from the world.

## Tips
- **Standard** view transform: AgX/Filmic desaturate flat colours (tested).
- **World lighting** is dimmed for lighting and full for the camera (`evg.lights.set_world_gradient`) or the sky fills every shadow and the step disappears.
- Dark fur: base `#352B3D` (not black), rim 0.5, a **cream** rim colour `#FFE9C4` makes the silhouette pop.
- Noise/flicker in the shadow edge: raise `softness` (0.08) and samples (64+).
- Painted markings (Evie's patch, Toffee's socks): keep a small flat base-colour texture or separate material slots; `convert_to_toon` keeps it.
- Eyes: **no rim, no shadow** (`rim_strength=0`, `threshold=0`) so they always look bright; the white + iris + pupil + 2 shine objects come from `rig_quadruped.py --eyes`.
