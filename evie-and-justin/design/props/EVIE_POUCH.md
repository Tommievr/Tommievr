# Evie's pouch (Ep.1 prop, carried all season): design, proposed v1.1
Lead: in Ep.1 a petal holding **one glowing drop** goes into a small cloth **pouch tied to Evie's collar, next to her paw tag**. She carries it all season and **opens it in Ep.7 for the lambs**. Needed: pouch design, hand-built Blender version (recommended) or Meshy prompt, and a faint **glow-peek** for Ep.4 and the Ep.7 opening moment (no spoilers in Shorts).

## 1. Design
| Item | Spec |
|---|---|
| Shape | **plump little bag** (a squashed sphere), short **flared lip** at the top, **drawstring ring** cinching below the lip, two tiny string ends, a short **strap** up to the collar. Chunky and toy-like, readable at small size |
| Size | sack ≈ **3.4 cm wide x 3.8 cm tall** on a 22 cm cat (about the width of her gold tag, 3.2 cm); strap ≈ 2.7 cm; hangs **~2.5 cm below the collar** |
| Position | on Evie's collar **beside the paw tag**, on the **cat's left (+X)** side of the tag, centre ≈ 5 cm from the tag centre so it **never touches the tag (gap ≥ 1.5 cm)**; strap attached to the collar band, **not** to the neck fur; sits in front of the chest, clear of the front legs |
| Colour (RECOMMENDED) | **soft lilac cloth `#CDB8F2`**, cream drawstring `#FFF1D6`, raspberry strap `#D01F4B` (matches her collar), dark inside `#4A3A5A`. Lilac ties it to the Moondew Blossom and stands out against Evie's white fur (cream would vanish on white) |
| Alt | cream cloth `#F6EBD3` (low contrast on white fur; only if lilac fights a scene) |
| Material | toon (`toon.simple_material`), thin rim; flat colour, **no cloth texture**; no cloth simulation (a gentle swing from a bone/damped track is enough) |
| Glow | emissive lilac `#B9A2FF` disc/bulb **inside the opening**, hidden at rest (`<name>_pouch_glow`) |
| Safety/read | tiny and soft, no zip/buckle/medicine cues; obviously a little fabric bag |
| Silhouette check | at `medium_two` the pouch is a distinct lilac bump beside the gold tag; at `wide_two` it is allowed to disappear |

## 2. Build (recommended: hand-built in Blender, parented to the collar bone)
`fx.make_pouch(root)` builds it from primitives (placeholder or final), tested. Parts, all named `evie_pouch_*`: `sack` (UV sphere 17x15x19 mm radii), `lip` (flared cone), `inside` (dark disc), `string` (torus), `tassel-1/1` (two tiny ellipsoids), `strap` (thin cylinder), `glow` (hidden emissive bulb). Anchor Empty `evie_pouch` is the parent: for the real model parent it to the **`collar_root`** bone (`parent=<armature>`; set `parent_type = "BONE"`, `parent_bone = "collar_root"`) and add the usual Damped Track/Copy Rotation (weight 0.3) for a little swing (tier T3).
Clipping checklist: [ ] gap to the tag ≥ 1.5 cm in all idle poses · [ ] strap meets the collar band, not the neck mesh · [ ] pouch clears the chest fur in `walk`/`hop` (move the anchor 3-5 mm forward if needed) · [ ] pouch stays on the **left/+X** of the tag when Evie turns · [ ] no intersection with `tag` glyph rings (section FX_GLOW 8).
Shot spec: `"characters": [{"name": "evie", ..., "pouch": true}]` (or fx `{"type": "pouch"}`). Justin does **not** carry one.

## 3. Meshy alternative (not recommended: tiny prop, easy to hand-build and it must stay parent-able)
Text-to-3D ≤ 600 chars (this one is 325); settings ⚠: Art style **Cartoon**, Quad, **3,000-6,000** faces, Symmetry On, export GLB.
```
Tiny cloth drawstring pouch, stylized 3D cartoon prop, chunky plump soft lilac fabric bag with a short flared top gathered by a cream drawstring with two small string ends and a short red strap loop, simple bold shapes, smooth, flat clean saturated colors, minimal detail, no texture noise, single object, game-ready low poly
```
Negative:
```
realistic, photorealistic, cloth wrinkles, detailed texture, noise, tiny details, text, logo, buckle, zipper, pills, bottle, people, characters, background, ground, blurry, low quality
```
Then `qa_model.py`, `toon.convert_to_toon`, rename parts like section 2, scale to the sizes above.

## 4. Glow-peek FX (faint lilac glow from the pouch opening)
`fx.pouch_peek(root, frame, length, peak=0.9)` / shot spec `{"type": "pouch_peek", "characters": ["evie"], "frame": 12, "length": 72}`. Test: `pipeline/shots/example_pouch_placeholder.json`, render `blender/example_pouch_peek.png`.
| Layer | Value |
|---|---|
| Glow bulb | emission 0 → 0.9 → breath 0.65 → 0.9 → 0 over `length` (3 s), lilac `#B9A2FF` |
| Light | very soft lilac point light, ≤ 3 W at peak, on the collar fur |
| Sparkles | **6** tiny lilac stars drifting up (a hint, not a burst) |
| Camera | `extreme_close_tag` (f/22) or a `close_up` that includes the tag so the viewer sees the **tag and the pouch together** |
| Sound | very soft shimmer, a single quiet high chime |
| Use | **Ep.4** (a tease: the viewer may notice the glow, nothing explained); **Ep.7 opening beat** (before the pouch is opened) |
**`pouch_open`** (Ep.7 SPOILER): drawstring ring scales ×1.45, lip flares ×1.25, glow peak 1.5, lilac + gold sparkle burst rises out (22 + 12 stars); use with `"spoiler": "ep07"`.

## 5. Spoiler discipline
- Ep.1: the petal goes into the pouch (the pouch itself is shown plainly). Ep.4 peek and Ep.7 opening only inside the **episodes**.
- **Not in Shorts/thumbnails/teasers** unless the script marks the exact frame as safe; `build_shot.py` prints a note when `pouch_peek`/`pouch_open` is rendered in 9:16.
- Ep.7 Shorts cut **before** the pouch opens (the lambs' reveal).

## 6. Hand-off
Evie sheet: pouch section. Day 1: optional, after Evie and Justin (`../DAY1_CHECKLIST.md` 4c). Colours also in `pipeline/blender/evg/palette.py` (`POUCH`).
