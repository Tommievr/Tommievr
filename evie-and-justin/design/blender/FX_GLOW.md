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

---
# 8. Green / red paw (series mechanic): `tag_state`
Lead/Tommie: the gold **paw symbol on the cats' tags turns GREEN when something is safe and RED when it is unsafe** (Ep.1: green over the Moondew Blossom = safe for them; recurring later for tide, mud, heights). Code: `fx.tag_state`, `fx.ensure_tag_symbols`, `fx.make_tag_disc`. Render: `example_tag_states.png` (left safe, right unsafe, both close-ups of placeholder tags).
```json
"fx": [
  {"type": "tag_state", "characters": ["evie", "justin"], "state": "safe",   "frame": 12, "length": 72},
  {"type": "tag_state", "characters": ["evie"],            "state": "unsafe", "frame": 12, "length": 72},
  {"type": "tag_state", "characters": ["evie"],            "state": "off",    "frame": 100}
]
```
Test shot: `pipeline/shots/example_tag_state_placeholder.json` (Evie safe, Justin unsafe at the same time).

## 8.1 Colours (colour-blind safe)
| State | Hex | Why |
|---|---|---|
| neutral (at rest) | tag gold `#FFB520`, paw emboss `#C77F0E` | unchanged look |
| **SAFE** | **mint-aqua `#4DFFC4`** (relative luminance 0.77) | light, blue-leaning green: stays separate from red for green-weak viewers |
| **UNSAFE** | **deep red `#D81B2A`** (luminance 0.16) | dark and saturated |
Checked by colour-vision-deficiency simulation (Machado 2009, severity 1.0, CIELAB ΔE between safe and unsafe): normal 137, **deuteranopia 52, protanopia 58**, tritanopia 147. A plain `#2ECC40` / `#FF4136` pair collapses to **ΔE 9** under deuteranopia, which is why it is not used. Brightness gap (0.77 vs 0.16) carries the difference even in greyscale. Emission strength is kept ≤ 1.7 so the hue survives (higher clips to white/cyan).

## 8.2 Non-colour cues (every state shows ALL of them)
| Cue | SAFE | UNSAFE |
|---|---|---|
| **Glyph on the paw** (white, large) | **check mark ✓** | **X ✕** |
| **Ring around the tag** | **solid, closed ring** | **dashed ring (8 segments), slowly rotating** |
| **Pulse rhythm** | **slow smooth swell** (one per 1.5 s) | **fast, hard three-flash pattern** (flash every 4 frames x3, then a pause; 0.75 s cycle), step changes, no easing |
| **Pop-in** | glyph + ring scale up with a soft overshoot | same, then flicker |
| **Light** | soft mint point light on the fur (0 → 30 W) | red point light, same strength |
| **Sound** (below) | soft rising chime | low soft hum / three low "bonks" |
| **Subtitle/caption** | "[soft chime]" | "[low hum]" |
Shape + rhythm + sound work in greyscale, for viewers with colour-vision differences, and without sound (on-screen glyph). **Rule for shots:** when the tag state matters, frame it (`extreme_close_tag` or a clear `close_up`) for at least 1.5 s; never show only the colour.
The glyph appears on the **paw pad**, centred: the paw stays recognisably a paw (state colour) with the check/X on top.

## 8.3 Sound cues for the audio team
| Event | Sound | Notes |
|---|---|---|
| SAFE onset (`frame`) | **soft rising two-note chime** (major third, e.g. C5 → E5, glassy/bell-like, ~0.6 s, gentle reverb) | friendly, never a "win" fanfare |
| SAFE hold | very quiet warm pad/hum, swells with each pulse (every 1.5 s) | fade under dialogue |
| UNSAFE onset | **low soft hum** (≈ 150-200 Hz, ~0.5 s, wooden/marimba-like) | calm, an "uh-oh", not a siren or buzzer |
| UNSAFE hold | **three short low "bonk-bonk-bonk"** in sync with the three flashes, repeat every 0.75 s | stops when the tag returns to gold |
| OFF (`state: off` or end) | soft downward "whoosh" / fade | tag returns to gold |
| Bell glow (lambs, Ep.7) | the **bell ring** (Cotton's signature sound) + a short shimmering harp glissando in lilac/gold register | see section 9 |
Keep all cues soft and kid-safe; the unsafe sound must feel like "careful", not "danger".

## 8.4 How the tag is built so it can switch state (Meshy / Blender note)
- **Do NOT use Meshy's tag.** Its paw print is baked into a texture and cannot change colour. Delete it (or ignore it) and build the tag in Blender: **`fx.make_tag_disc("evie", location, radius=0.012, parent=<rig>, parent_bone="tag.01")`** creates a plain gold toon disc `evie_tag` plus an Empty `evie_tag_face` (custom property `radius`, Z pointing out of the tag) as the anchor.
- `fx.ensure_tag_symbols(tag)` (called automatically by `tag_state`) adds, as children of the face anchor: **`paw`** (separate paw mesh, dark gold at rest, emissive material `tagsym_paw`), **`check`**, **`cross`** (white glyph meshes), **`ring_safe`** (solid), **`ring_unsafe`** (dashed). They start at scale 0 (hidden) except the paw; all use their own **emission-only materials** so the colour is keyframed directly on the Emission colour/strength.
- Each tag gets its own material copies, so Evie can be safe while Justin is unsafe in the same shot.
- Placeholder characters already get a tag the code can drive (`PLACEHOLDER_<name>_tag`). For Meshy characters, prompts keep "round gold tag" for the look; the paw is added in Blender.
- Quality check (see `meshy/QA_AND_FIXES.md`): the tag disc must be a **separate, rigid object** parented to a bone, flat face toward the camera at rest, about 2.5 cm diameter.

# 9. Lamb bells receive the drink (Ep.7, SPOILER): `bell_glow`
Lambs get the drink in the **last episode (Ep.7)**; they have birthdays (celebration without ageing). Cotton and Toffee's **gold heart bells glow lilac/gold** when they receive it. Code: `fx.bell_glow` (placeholder lambs name their bell `_bell`; real models must name the bell object `<name>_bell`). Render: `example_bell_glow.png`.
```json
{ "spoiler": "ep07", "fx": [
    {"type": "drink", "option": "blossom", "pos": [0, -0.4, 0]},
    {"type": "bell_glow", "characters": ["cotton", "toffee"], "frame": 12, "length": 72} ] }
```
## 9.1 Recipe (72 frames)
| Frames | What |
|---|---|
| 0-12 | the lambs approach the Blossom; bells ring softly (audio) |
| 12 | bell **emission swell** 1 → 2.8 (peak at +18), warm/lilac point light 0 → 35 W |
| 14, 28, 42 | **three expanding lilac rings** around each bell (facing the camera, radius 1 → 7.5 cm) |
| 14-50 | **sparkle bursts**: ~24 lilac (`#B9A2FF`) + ~14 gold (`#FFB520`) stars pop from each bell and rise 10 cm |
| 24+ | camera push to `extreme_close_tag` (bell, heart slot visible) |
| 72 | settles back to normal gold; the lambs look at each other: `expr_happy`; **birthday beat** (music, cake/flower crown optional, script decision) |
Palette: lilac `#B9A2FF` = the drink, gold `#FFB520` = the bell, so the bell visibly "drinks in" the lilac. No green/red paw for lambs (the safety mechanic is the cats' tags).
## 9.2 Spoiler discipline
- The Ep.7 reveal (lambs + drink + glowing bells) must **not** appear in any earlier Short, thumbnail or teaser. Mark shot specs with `"spoiler": "ep07"`; `build_shot.py` prints a **WARNING** when such a shot is rendered, and a louder one in 9:16 (Shorts).
- Ep.5-6 may foreshadow only through dialogue (lambs wanting to stay little / birthdays), not with the glow.
- Shorts for Ep.7 itself should use a cut **before** the bells glow (cliffhanger rule from the episode slate).

# 10. Evie's pouch: glow-peek and open
Full spec in `../props/EVIE_POUCH.md`. Code: `fx.make_pouch`, `fx.pouch_peek`, `fx.pouch_open`; render `example_pouch_peek.png`. Spec snippets:
```json
{"name": "evie", "pouch": true}                                        // on the character: builds the pouch beside the tag
{"type": "pouch_peek", "characters": ["evie"], "frame": 12, "length": 72}   // Ep.4 tease / Ep.7 opening beat: faint lilac glow + 6 tiny sparkles
{"type": "pouch_open", "characters": ["evie"], "frame": 12, "length": 72}   // Ep.7 SPOILER: loosens, glow 1.5, lilac+gold burst
```
Faint on purpose (emission ≤ 0.9, light ≤ 3 W). Never in Shorts unless the script allows it.
