# Evie — character sheet (proposed v1.0)
Canon: `lead/CHARACTERS.md`. Reference: `assets/characters/evie-and-justin-reference.png` (left kitten). Shared specs: `COMMON.md`.

**Role/personality in one line:** the dreamer; wonders out loud, notices small beautiful details, soft and bright.
**Acting notes:** big wide-eyed wonder, head tilts, ears forward. Smaller, softer movements than Justin; never sarcastic.

## Colours
| Part | Sampled (lit) | Albedo (proposed) | Notes |
|---|---|---|---|
| Fur, main (white) | `#E4C3BB` – `#E7CDD0` | **`#F5EFE9`** warm white | never pure white; reads pink-cream in golden light |
| Fur, shadow side | `#D0B5B7` | `#E3D8D4` | only in render shading, not a texture colour |
| **Black patch** (top-left of head, over the left ear base) | `#170E0B` | **`#1A1412`** | see "marking" below |
| Ear inner | `#FA936D` | **`#F3A38F`** soft salmon-pink | fine white fuzz at the edge |
| Nose | `#F5967E` | **`#F2958A`** | small, rounded triangle |
| Cheek blush | `#F6BAA5` | `#F7C2B3` | very soft, low opacity |
| **Iris (BLUE)** | `#07659B` (median) / `#069AC7` (lit) | **outer `#0A67A0` → inner `#2FA3D8`** | radial gradient, darker rim |
| Pupil | — | `#05080C` | large, round, with 2 catchlights |
| Eyelash / lid line | — | `#1A1210` | thin dark upper lash, 3 small lashes at outer corner |
| Brow marks | — | `#8C7B78` | soft grey-brown fur marks above the eyes |
| Whiskers | — | `#FFFFFF` at 80 % | thin, mostly forward and slightly down |
| Paw pads | `#E5CBCA` (fur around) | `#EFC3BD` (estimated, pads are barely visible in the reference) | pale pink; toe beans visible |
| **Collar** | `#AA1E37` / lit `#BC283D` | **`#B3203C`** raspberry pink-red | **see Q-01: the reference is deeper raspberry than the word "pink" suggests.** Thin with tiny gold dots. |
| **Tag** (gold paw-print disc) | `#E78E0C` / lit `#F8AC12` | **`#EBA02B`**, paw emboss `#B8700A` | metallic 1.0, roughness 0.3; rounded disc ~ 2.5 cm; small ring on top |

### Marking (exact)
- A **single black patch** sits on the **top-left of the head**, as seen from the front (the character's own right side). It covers the ear base and runs back/up toward the crown: an irregular rounded blob, about **30 % of the head width**, with a soft ragged edge, slightly lighter at the border.
- No other black fur anywhere. The tail is white.
- Marking is **asymmetrical on purpose**: it is the quickest on-model check.

## Proportions (head-units, 1 HU = head width)
| Measure | Value |
|---|---|
| Body length, nose to rump | ≈ 2.5 HU |
| Standing height to top of head | ≈ 1.9 HU |
| Shoulder height | ≈ 1.2 HU |
| Head height : width | ≈ 0.85 : 1 (wide, round, short muzzle) |
| Eye width | ≈ 0.24 HU each; gap between eyes ≈ 0.8 of one eye width; eyes sit slightly below the head's midline |
| Ear height | ≈ 0.42 HU, wide base, **pointed but rounded tip**, tilted slightly outward |
| Muzzle | very short, tiny nose, mouth "w" shape |
| Legs | short and chunky, front paws large (about 0.35 HU wide); pads visible |
| Tail | ≈ 1.0 × body length, thick and fluffy, upward question-mark curl, tapered, fluffy tip |
| Fur | soft short-to-medium fluff, bushy cheeks and chest, "halo" of fine fuzz |
In metres (STYLE_GUIDE section 5): shoulder height 0.22, body length 0.36, head width 0.14.

## Silhouette
Round head wider than the neck, two pointed ears, big fluffy upturned tail, rounded chunky body on four short legs. Dot test: head + tail curl must be recognisable at 64 px. Evie vs Justin silhouettes differ by **ear tilt and tail**: Evie's tail is longer and curves up to the left, Justin's is shorter, plumper, and curls over his back.

## Collar / tag details
- Collar: thin band (≈ 6 mm), raspberry, sits at the base of the neck, tiny gold stud dots, small buckle at the back.
- Tag: **gold paw-print disc**, hangs at the front centre on a small ring, slightly tilted when she moves. Glows on discovery (`TAG_glow` in STYLE_GUIDE section 3.1).
- Matching tag with Justin = the "adventure badge". Same size, same print.

## Expressions (`COMMON.md` section 1) — Evie notes
| Expression | Evie-specific note |
|---|---|
| happy | big bright eyes, blush stronger, little fang pair |
| curious | head tilt toward the black-patch side; one ear forward |
| surprised | eyes huge, iris ring thin, ears straight up |
| scared_but_brave | ears flat, eyes watery-bright, a tiny upward chin |
| sleepy | slow half-lids, tail curled round the body |
| laughing | arcs closed, mouth wide, blush strongest |
Visemes: `COMMON.md` section 2. Evie's `vis_G` shows two tiny upper fangs.

## Neutral input pose (Meshy)
Follow `COMMON.md` section 3 exactly. Evie specifics: black patch visible on the front view; in the **side view show her left side** (the patched side) so the patch is in frame; collar and tag at the front centre.

## On-model / off-model checklist
**ON-MODEL ✔**
- [ ] Fur is white (warm white), never grey or cream-yellow
- [ ] **Exactly one** black patch, top-left of head (front view), over the ear base
- [ ] **Blue** eyes, big, round, with 2 catchlights
- [ ] Collar is **raspberry-pink**, tag is a **gold paw-print disc**
- [ ] Inner ears and nose salmon-pink; soft pink blush
- [ ] Head is big and round; muzzle very short
- [ ] Tail long, fluffy, upward curl, white
- [ ] 4 legs, 4 paws, chunky, toe beans visible

**OFF-MODEL ✘**
- [ ] Patch on the wrong side, two patches, patch on the body, or **no** patch
- [ ] Green/brown/yellow eyes, pupils slit-shaped, tiny eyes
- [ ] Collar blue, green, black, or tag missing/blank/not gold or different shape
- [ ] Grey/cream/yellow fur, visible stripes
- [ ] Realistic cat proportions (long muzzle, small head)
- [ ] Extra/missing/fused limbs, long thin legs
- [ ] Hard outlines or flat 2D look; photoreal fur
- [ ] Asymmetric eyes by accident (the patch is the only intended asymmetry)
