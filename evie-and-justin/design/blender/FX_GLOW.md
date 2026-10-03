# Glow, sparkles and the "paw tags glow" discovery moment
Code: `pipeline/blender/evg/fx.py` (tested headless; see `example_discovery.png`). Props: `../props/SPECIAL_DRINK.md`. Look: simple, bold, clean: **flat glowing colour + a few 4-point stars**, no volumetric smoke, no particle clutter.

## 1. The recipe in one shot spec
```json
"fx": [
  {"type": "drink",    "option": "blossom", "pos": [0, -0.35, 0]},
  {"type": "tag_glow", "characters": ["evie", "justin"], "frame": 12, "length": 48, "peak": 2.6},
  {"type": "sparkles", "pos": [0, -0.35, 0.12], "frame": 12, "count": 40, "radius": 0.2, "color": "#FFE08A"}
]
```
`python ... build_shot.py -- pipeline/shots/example_discovery_placeholder.json --still 14` (dusk variant, placeholder cats). Replace the placeholder drink by the Meshy prop: append `pipeline/props/drink.blend` (collection `DRINK`) and keep the `drink_glow` sphere.

## 2. Discovery timeline (24 fps; frame numbers relative to the cue)
| Frame | What |
|---|---|
| 0 | kittens look at the drink: `expr_curious`; camera `medium_two` |
| 0-12 | drink pulse slow (liquid emission 1.2 → 1.95 → 1.2 per 2 s); lilac point light pools on the ground |
| **12** | **tags start to glow**: tag/bell emission 1 → 2.6 (peak at +25 % of `length`) and a warm point light 0 → 40 W, then slowly back (length 48) |
| 12-30 | **sparkle burst** from the drink: 30-40 stars pop out, rise 25 cm and fade (scale to 0) |
| 18 | cut/push to `extreme_close_tag` (gold tag, lilac sparkles); `expr_surprised` |
| 30-48 | tags settle back to normal; kittens `happy` |
| audio | soft chime at frame 12, shimmer through the burst (audio team) |
Rule: **both tags glow together** (the matching "adventure badge"); Cotton/Toffee bells use the same function (`_bell` objects are found automatically).

## 3. Materials
| Thing | Recipe |
|---|---|
| Liquid / orb / sparkles | `fx.glow_material(name, hex, strength)`: a single **Emission** node, flat colour. **Strength ≤ ~2.5** with the Standard view transform (higher clips to white and loses the colour) |
| Tag / bell | `toon.gold_material()` (toon + highlight band); `fx.tag_glow` copies the material per tag and keyframes its Emission strength (toon materials end in an Emission node) |
| Halo | **Compositor Glare** (see 4) or just the point light; do not fake volumetrics |

## 4. Bloom (optional, 2 minutes, looks great)
EEVEE has no built-in bloom checkbox in Blender 4.2+. In the **Compositing** workspace: Use Nodes → **Render Layers → Glare** (type **Fog Glow**, Quality High, **Threshold 0.9**, Size 6, Mix 0) → Composite. Only emissive things above the threshold bloom (liquid, tags at peak, sparkles); the toon characters do not. *(The compositor node API changed in Blender 5.x; set it up once by hand in your template .blend instead of via script.)*

## 5. Sparkles two ways
- **Script (default, deterministic):** `fx.sparkle_burst(center, count, color, frame, duration, radius, rise)`: flat 4-point stars, camera-facing, keyframed pop → drift → fade. Re-time with `frame`/`duration`.
- **Particle system (manual alternative):** emitter = small sphere at the drink; Emission: count 40, lifetime 30, start frame 12 (burst: frame start = end); Velocity: normal 0.1, Z gravity -0.05 (negative = float up); Render As **Object** with a star mesh (`evg_sparkle`) + `glow_material`; Scale random 0.6-1.5, scale-over-lifetime via Size texture or fade by keyframes. Only needed if you want physics-y motion.

## 6. Lighting during the moment
Lower the key a little (dusk variant or ×0.7), keep rim lights; let the lilac drink light and the gold tag lights be the main colour accents (STYLE_GUIDE: gold tag + lilac = the discovery palette). Keep the characters brightest: do not let sparkles cover faces (spawn radius ≤ 0.2 m, centred on the drink).

## 7. Checks
- [ ] Tags visibly warm up and return to normal (render frames 1, 12, 24, 48)
- [ ] Liquid still reads **lilac**, not white
- [ ] Sparkles do not hide faces; 9:16 version (`--aspect 9:16`) keeps the drink in the safe area
- [ ] Looks "clearly fantasy": no bottle/label/medicine cues (design rule in SPECIAL_DRINK)
