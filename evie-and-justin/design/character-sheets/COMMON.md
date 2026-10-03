# Common character specs (proposed v1.1: stylised, simple fur)

Applies to all four characters and new ones unless a sheet overrides. Style source of truth: `../STYLE_GUIDE.md` section 2.

## 1. Style in one paragraph
Chunky, toy-like **stylised 3D cartoon**. Smooth short matte fur (or simple cloud-clump wool), bold rounded forms, short stubby legs, head as wide as the body, **big glossy expressive eyes**, flat saturated colours, soft two-tone toon shading, thin warm rim. Fur is suggested by **3-6 chunky tufts** only (cheek ruff, chest tuft, tail tip, ear tuft). No strands, no fuzz halo, no fur texture, no outlines.

## 2. Shared build specs
| Item | Spec |
|---|---|
| Polycount (final, rigged) | 15,000-40,000 triangles per character |
| Surfaces | smooth, soft-bevelled shapes; no fine geometry; small parts (collar, tag/bell, eyes) may be separate objects |
| Textures | **flat colours** via one small base-colour texture (or vertex/material colours); no normal map needed; markings painted flat (Evie's patch, Toffee's socks) |
| Eyes | **separate eye objects** (white + iris + big pupil + 2 catchlights) so they can blink and look; eyes are the detail focus |
| Whiskers | 3 short thick cheek lines per side, simple geometry or a flat texture; optional |
| Tail | thick, chunky, simple curl; lambs: round pom |
| Toon material | `blender/SHADING.md` (base colour × plum shadow tint, thin rim) |

## 3. Expressions (6 + neutral)
Names are shape-key / swap names (`expr_<name>`). With simple faces these are cheap: eyelids, brows (as simple shapes), mouth shape, ears.

| # | Name | Eyes | Brows | Mouth | Ears | Used for |
|---|---|---|---|---|---|---|
| 0 | `neutral` | open, relaxed, looking at camera | level | closed, tiny smile | upright / relaxed | rig default, Meshy input |
| 1 | `happy` | wide, bright, slightly squinted lower lids | slightly raised | open smile | up, forward | default mood |
| 2 | `curious` | wide, large pupils | one up, one level | small "o" or closed | one forward, one back | questions, noticing |
| 3 | `surprised` | huge, round, small pupils | high | open round "O" | straight up / flared (lambs) | discoveries |
| 4 | `scared_but_brave` | wide, large pupils, chin up | angled up-inward | tight line, corners up | flat sideways / back | tension (always safe) |
| 5 | `sleepy` | half-lidded | low, relaxed | small closed smile / tiny yawn | drooped | goodnight beat |
| 6 | `laughing` | closed upturned arcs | high | wide open | back, shaking | jokes, victories |
Blink: `blink_L`, `blink_R` (eyelid shells or eye-squash fallback, `evg/characters.py`). Interval 3-5 s, 0.15 s long. No blink in `laughing`/`sleepy`.

## 4. Visemes (lip sync)
9 mouth shapes of the free **Rhubarb Lip Sync** tool (A-H + X) so audio drives the mouth (see `../blender/RIGGING.md`; verify Rhubarb's licence/output on the day). Shape keys `vis_X ... vis_H`.

| Key | Sounds | Mouth |
|---|---|---|
| `vis_X` | silence | closed, relaxed |
| `vis_A` | P B M | lips pressed |
| `vis_B` | K S T EE | slightly open, wide |
| `vis_C` | EH AE | open, medium |
| `vis_D` | AA | widest open |
| `vis_E` | AO ER | rounded, medium |
| `vis_F` | UW OW W | small round |
| `vis_G` | F V | top teeth/gum on lower lip |
| `vis_H` | L | open, tongue tip up |
The cartoon mouth is a **simple dark shape with a pink tongue**; cats get 2 tiny fangs in `vis_G`/`laughing`; lambs have none. Cheapest fallback (Ep.1): jaw open/close + 4 mouth swaps X/A/D/F (tier T1, `../blender/RIGGING.md`).

## 5. Neutral pose requirements for Meshy input images
These are for image-to-3D only, not animation poses.
1. **Standing on four legs**, weight even, legs slightly apart: **all four legs and paws visible and separated**.
2. Views: **front** (head and chest toward camera), **side** (exact profile, head turned to camera), **3/4** (45 degrees). Orthographic-like, no wide-angle distortion.
3. Head level, looking at camera, **eyes open, symmetrical, pupils centred**.
4. **Mouth closed**, tiny relaxed smile (open mouths bake teeth/tongue into the mesh).
5. Ears neutral: cats upright symmetrical; lambs relaxed, floppy, horizontal.
6. **Tail** raised and clear of the body (cats); lambs' pom visible from side/back.
7. **Collar and tag/bell** fully visible, hanging straight, facing the camera.
8. **Background plain** flat light grey `#EDEDED` (or white for Toffee/Justin if grey fights the colour; see sheets). No floor, no shadow, nothing else.
9. **Lighting soft, even, neutral white.** No golden tint, no rim glow, no hard shadows (they bake into the texture).
10. Single character, full body, ~10 % margin, square 1:1, >= 1536 px.
11. Same proportions and colours across all views (generate side/3/4 from the front image).
12. **Clean smooth outline: NO fur strands, no fuzz halo, no fine texture**, simple shapes (this is what keeps Meshy geometry clean).
13. No props, text, extra characters, motion blur or depth blur.

## 6. On-model vs off-model method
Check in this order: **1 silhouette** (solid black still reads?) → **2 colours** (vs the base hexes) → **3 face** (eye colour, eye size, markings) → **4 accessories** (collar colour, tag/bell shape) → **5 proportions** (chunky, big head) → **6 expressions** (all six readable) → **7 style** (smooth, simple, no fur detail). Record in `pipeline/meshy/<name>/QA.md`.

## 7. Sampling method (reference traceability)
`tools/sample_colours.py`: median RGB of pixels (alpha > 200) in hand-picked rectangles of the 1774x887 reference PNGs, with hue filters for irises, collars and metal. Needs Pillow; run from `evie-and-justin/`.
