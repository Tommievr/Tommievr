# Common character specs (proposed v1.0)

Applies to all four characters (and new ones, unless a sheet overrides).

## 1. Expressions (6 + neutral)
Names are the shape-key / texture-swap names used in Blender (`expr_<name>`). Every character needs all six; the per-character sheet adds character-specific notes.

| # | Name | Eyes | Brows (soft fur marks) | Mouth | Ears | Used for |
|---|---|---|---|---|---|---|
| 0 | `neutral` | open, relaxed, looking at camera | level | closed, tiny smile | upright/relaxed | rig default, Meshy input |
| 1 | `happy` | wide, bright, slightly squinted lower lids | raised a little | open smile, small teeth (cats) / tongue tip (lambs) | up, forward | default adventuring mood |
| 2 | `curious` | wide, pupils large, one brow higher | one up, one level | small "o" or closed, head tilt (done by the rig) | one ear forward, one back | questions, noticing details |
| 3 | `surprised` | huge, round, pupils pinprick-small | high | open round "O" | straight up / flared out (lambs) | discoveries, "whoa!" |
| 4 | `scared_but_brave` | wide, pupils large, bright, chin raised | angled up inward | tight line, corners slightly up | flattened sideways (cats) / back (lambs) | tension beats (always safe, never dark) |
| 5 | `sleepy` | half-lidded, slow | relaxed low | small closed smile or tiny yawn | drooped | outro goodnight beat |
| 6 | `laughing` | closed upturned arcs (happy-crescents), maybe a tear | high | wide open, tongue visible | back, shaking | jokes, Justin's mock-drama, victories |

Blink: separate shape key pair `blink_L`, `blink_R` (eyelid mesh closes fully). Blink interval 3–5 s random, 0.15 s long; no blink in `laughing` and `sleepy` (already closed).

## 2. Visemes (lip sync)
Mouth set follows the 9 shapes of the free **Rhubarb Lip Sync** tool (A–H + X) so we can drive the mouth from the Kokoro audio (see `lead/VOICES_AND_HARDWARE.md`). Shape keys: `vis_X … vis_H`. *(Verify Rhubarb's current licence/output format on the day, before relying on it.)*

| Key | Sounds | Mouth |
|---|---|---|
| `vis_X` | silence / rest | closed, relaxed (= neutral mouth) |
| `vis_A` | P, B, M | lips pressed |
| `vis_B` | K, S, T, EE, most consonants | slightly open, teeth/upper-jaw visible, wide |
| `vis_C` | EH, AE | open, medium |
| `vis_D` | AA ("ah") | widest open |
| `vis_E` | AO, ER | rounded, medium |
| `vis_F` | UW, OW, W ("oo") | small tight round |
| `vis_G` | F, V | upper teeth on lower lip (cats: tiny fangs; lambs: top gum) |
| `vis_H` | L (long) | open, tongue tip up |

Mixing rule: viseme keys are driven 0–1 with 2–3 frame easing; expression keys are **additive** below the mouth (eyes/brows/ears), and the mouth key of the expression is multiplied by `(1 − viseme_weight)` while speaking so smiles do not fight the visemes.
Cheapest viable fallback (Ep.1): jaw bone open/close driven by audio amplitude + A/D/F/X mouth texture swap. See `meshy/MESHY_PROMPTS.md` section 5.

## 3. Neutral pose requirements for Meshy input images
These images are **not** the animation poses. They are for image-to-3D only.
1. **Standing, four legs down**, weight even, legs slightly apart so **all four legs and paws are visible and separated** (no overlap with belly/other legs). Front paws parallel, hind paws parallel.
2. Body **perfectly side-on** (side view) / **head-and-chest facing the camera** (front view) / **3/4 view at 45°**. No perspective extremes (use ≈ 85 mm-equivalent look, no wide-angle distortion).
3. **Head level, looking straight at camera** (front and 3/4); in the side view the head turns to look at the camera.
4. **Eyes open, neutral, same size both sides**, pupils centred, no side-glance.
5. **Mouth closed, relaxed, tiny smile.** (Open mouths bake teeth/tongue into the mesh and make the visemes impossible.)
6. **Ears neutral:** cats upright and symmetrical; lambs relaxed, floppy ears horizontal-down, symmetrical.
7. **Tail:** cats: raised in a gentle upward curl, **away from the body** so the silhouette is clear. Lambs: small pom visible from behind/side, not hidden by the body.
8. **Collar and tag/bell:** collar fully visible, tag/bell hanging straight down, facing camera, centred.
9. **Background:** plain, flat neutral (`#FFFFFF` or a light grey `#EDEDED`), no floor, no shadow (or at most a faint contact shadow), nothing else in frame.
10. **Lighting:** **soft, even, neutral white.** No golden-hour tint, no strong rim glow, no hard shadows (those get baked into the texture). The warm glow is added later in Blender.
11. **Framing:** single character, full body inside the frame with ~10 % margin, character centred, square 1:1, ≥ 1536×1536 px.
12. **Consistency across views:** same proportions, colours and markings in every view (generate all views from the front image as reference).
13. **No props, no text, no extra characters, no motion blur, no depth-of-field blur.**
14. **Fur/wool:** soft but with a **clean readable outline**; avoid long flyaway strands and glow halo (they become floating geometry).

## 4. On-model vs off-model method
Each sheet has a character checklist. For any generated image/model, check in this order:
1. **Silhouette** (fill solid black: still reads as that character?)
2. **Colours** (compare to the albedo hexes; within a visible tolerance)
3. **Face** (eye colour, eye size/spacing, markings)
4. **Accessories** (collar colour, tag/bell shape)
5. **Proportions** (head:body ratio, leg length)
6. **Expression range** (all six readable)
Record result in `pipeline/meshy/<name>/QA.md` (pass / fail + screenshot).

## 5. Sampling method (reproducible)
Median RGB of pixels with alpha > 200 in hand-picked rectangles on the reference PNGs (1774×887), with hue filters for irises, collars and metal. Script: `tools/sample_colours.py` (needs Pillow; run from the `evie-and-justin/` folder). If the lead supplies new reference art, re-sample.
