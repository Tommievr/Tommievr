# Evie — character sheet (approved v1.1, stylised simple fur)
Canon: `lead/CHARACTERS.md`. Colour/markings reference only (NOT the style): `assets/characters/evie-and-justin-reference.png`, left kitten. Shared: `COMMON.md`.
**Personality:** the dreamer; wonders out loud, notices small beautiful details. **Acting:** wide-eyed wonder, head tilts, ears forward, softer smaller movements than Justin.

## Colours
| Part | Reference (sampled, lit) | **Base (use this)** | Notes |
|---|---|---|---|
| Fur (white) | `#E4C3BB` | **`#FFF6EC`** warm white | the brightest thing in frame; never pure white |
| **Black patch** | `#170E0B` | **`#2A2030`** plum-black | flat shape, see Markings |
| Ear inner | `#FA936D` | **`#FFA9A0`** | flat soft pink |
| Nose | `#F5967E` | **`#FF8FA0`** | tiny rounded triangle |
| Cheek blush | `#F6BAA5` | `#FFB7B0` | optional flat soft disc |
| **Iris (BLUE)** | `#07659B` / `#069AC7` | **`#1E7FD6`**, rim `#1566B8`, inner glow `#4DB5F5` | big, simple radial gradient |
| Pupil | | `#0A0A12` | large, round, 2 catchlights (white) |
| Paw pads | | `#FFB7B0` | flat |
| **Collar** | `#AA1E37` | **`#D01F4B`** raspberry pink | raspberry, approved (Q-01) |
| **Tag** | `#E78E0C` | **`#FFB520`** gold, emboss `#E0901A` | toon gold: highlight band, `evg.toon.gold_material` |

## Markings
- **One black patch, top-left of the head** (seen from the front), over the base of her left ear, about 30 % of head width, a soft rounded blob with a clean edge (flat colour shape). **The only asymmetry; the fastest on-model check.**
- No other dark fur; tail white.

## Proportions (head-units, 1 HU = head width)
| Measure | Value |
|---|---|
| Body length | ≈ 2.2 HU (plump bean) |
| Height to top of head | ≈ 1.8 HU |
| Head | **big, round**, ≈ as wide as the body; height:width ≈ 0.85 |
| Eyes | **very big**: ≈ 0.28 HU each, wide-set, below the head midline |
| Ears | rounded triangles, ≈ 0.4 HU, wide base, tilted slightly out |
| Muzzle | tiny, almost flat face; "w" mouth |
| Legs | **short and stubby**; paws are round chunky blobs |
| Tail | thick, ≈ 0.9 x body, upward curl with round tip |
| Fur | **smooth short matte**; chunky tufts: 2 cheek tufts, 1 chest tuft, 1 tail-tip tuft |
Metres: shoulder 0.22, body length 0.36, head width 0.14.

## Silhouette
Round head, two rounded-triangle ears, plump body, stubby legs, fat curled-up tail. Differs from Justin by **longer, thinner, upward-curling tail** and the patch.

## Collar / tag
Thin raspberry band at the neck, small gold stud dots (optional flat dots), buckle at the back. **Gold paw-print tag**: chunky round disc, ≈ 2.5 cm, hangs at the front centre; glows at discovery (`TAG_glow`). Matching tag with Justin = the adventure badge.

## Green / red paw (series mechanic, approved)
The gold paw symbol on Evie's tag turns **GREEN (safe) / RED (unsafe)**. Both cats' tags do it together or separately.
| State | Paw colour | Glyph on the paw | Ring | Pulse | Sound |
|---|---|---|---|---|---|
| rest | dark gold `#C77F0E` on the gold disc `#FFB520` | none | none | none | none |
| **SAFE** | mint-aqua `#4DFFC4` | white **check mark ✓** | **solid** ring `#4DFFC4` | slow smooth swell | soft rising chime |
| **UNSAFE** | deep red `#D81B2A` | white **X ✕** | **dashed** rotating ring `#D81B2A` | fast hard 3-flash | low hum / 3 low bonks |
Colours are chosen for colour-blind viewers (deuteranopia ΔE 52); **never colour alone**: glyph + ring + pulse + sound always accompany it. Recipe, code and sound table: `../blender/FX_GLOW.md` sections 8.1-8.3.
**Build note:** the tag must be a plain gold disc with a **separate paw symbol** (Meshy's baked paw print cannot change colour): `fx.make_tag_disc(...)`, details in `FX_GLOW.md` section 8.4. On-model check: at rest the tag looks like the reference (gold disc, darker gold paw print).

## Expression notes (`COMMON.md` section 3)
happy: big shining eyes, blush, tiny fangs · curious: head tilt to the patch side · surprised: huge eyes, thin iris ring · scared_but_brave: ears flat, shining eyes, little chin up · sleepy: slow lids, tail wrapped · laughing: arcs, wide mouth.

## Neutral input pose (Meshy)
`COMMON.md` section 5. Show the patch in the front view; the side view shows her **left (patch) side**. Background `#EDEDED`.

## On-model / off-model
**ON ✔** [ ] tag paw can show green ✓ / red ✕ states (separate paw symbol) · [ ] white fur · [ ] exactly one black patch top-left · [ ] BLUE eyes, very big, 2 catchlights · [ ] raspberry-pink collar + gold paw tag · [ ] pink ears/nose · [ ] big round head, stubby legs, fat curled tail · [ ] **smooth, simple, chunky: no fur detail**
**OFF ✘** [ ] patch missing/wrong side/two patches · [ ] eyes not blue or small · [ ] collar wrong colour, tag missing/not gold · [ ] grey/cream fur · [ ] long muzzle / realistic cat · [ ] fur strands, fuzz halo, photoreal or Pixar-fur look · [ ] extra/fused limbs
