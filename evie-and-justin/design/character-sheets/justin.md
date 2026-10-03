# Justin — character sheet (approved v1.1, stylised simple fur)
Canon: `lead/CHARACTERS.md`. Colour/markings reference only (NOT the style): `assets/characters/evie-and-justin-reference.png`, right kitten. Shared: `COMMON.md`.
**Personality:** explorer/skeptic; bold, funny, a little dramatic, secretly loves facts. **Acting:** cheeky smirks, one raised brow, big dramatic reactions, mock-grumbles; bouncier than Evie.

## Colours
| Part | Reference (sampled, lit) | **Base (use this)** | Notes |
|---|---|---|---|
| Fur ("black") | `#221614` - `#2C1810` | **`#352B3D`** plum-black | lifted from true black so the toon shadow step and rim read; still reads "black" |
| Ear inner | `#E99B81` | **`#FF9FA0`** pink | |
| Ear back rim (white-pink) | `#E99B81` / cream | **`#FFEBDD`** cream-white | the lead's "white-pink inner ears": cream-white outer ear back and edge, pink inside |
| Nose | `#B34C40` | **`#E0707A`** | |
| **Iris (GREEN)** | `#2E6E14` / `#5C9F0C` | **`#3FB52A`**, rim `#2A8F1E`, inner glow `#7BDB3A` | big, simple radial gradient |
| Eye white | `#F8DFD7` | `#FFFFFF` | clearly visible white around the iris |
| Pupil | | `#0A0A12` | large, 2 catchlights |
| Whiskers | | `#F2EDE6` | 3 short cheek lines per side |
| Paw pads | | `#8F5B6E` | flat |
| **Collar** | `#1C0E06` | **`#17121C`** darkest value on the character | plain, no dots; must contrast the fur (fur is lighter than the collar) |
| **Tag** | `#F1A01A` | **`#FFB520`** gold | main bright accent on the dark chest |

## Markings
None (solid). The cream-white ear backs are the only light accent.

## Proportions (head-units)
| Measure | Value |
|---|---|
| Body length | ≈ 2.1 HU (stockier, plumper than Evie) |
| Height to top of head | ≈ 1.8 HU |
| Head | big, round, **fuller cheeks** (cheek tufts), ≈ 0.85 : 1 |
| Eyes | very big ≈ 0.30 HU each, visible whites |
| Ears | rounded triangles ≈ 0.4 HU, slightly more outward |
| Legs | short, stubby, big round paws |
| Tail | **shorter and plumper** than Evie's (≈ 0.7 x body), curled over his back |
| Fur | smooth short matte; tufts: 2 big cheek tufts, chest tuft, tail tip |
Metres: shoulder 0.22, body length 0.35, head width 0.145.

## Silhouette
Same family as Evie but **stockier, with fuller cheeks and a short plump tail curled over his back**.

## Collar / tag
Thin plain dark collar, low on the neck; add a **small highlight band** (toon spec) so it reads on dark fur. **Gold paw tag identical to Evie's** (the bright accent on his chest).

## Green / red paw (series mechanic, approved)
The gold paw symbol on Justin's tag turns **GREEN (safe) / RED (unsafe)**. Both cats' tags do it together or separately.
| State | Paw colour | Glyph on the paw | Ring | Pulse | Sound |
|---|---|---|---|---|---|
| rest | dark gold `#C77F0E` on the gold disc `#FFB520` | none | none | none | none |
| **SAFE** | mint-aqua `#4DFFC4` | white **check mark ✓** | **solid** ring `#4DFFC4` | slow smooth swell | soft rising chime |
| **UNSAFE** | deep red `#D81B2A` | white **X ✕** | **dashed** rotating ring `#D81B2A` | fast hard 3-flash | low hum / 3 low bonks |
Colours are chosen for colour-blind viewers (deuteranopia ΔE 52); **never colour alone**: glyph + ring + pulse + sound always accompany it. Recipe, code and sound table: `../blender/FX_GLOW.md` sections 8.1-8.3.
**Build note:** the tag must be a plain gold disc with a **separate paw symbol** (Meshy's baked paw print cannot change colour): `fx.make_tag_disc(...)`, details in `FX_GLOW.md` section 8.4. On-model check: at rest the tag looks like the reference (gold disc, darker gold paw print).

## Expression notes
happy: cheeky half-smirk, one corner higher · curious: single raised brow (always the same side) · surprised: dramatic, whites show all round, wide mouth · scared_but_brave: puffed cheeks, bristled tail tip, jaw set · sleepy: grumbly half-lids · laughing: head back, arcs · extra `grumble`: flat mouth, brows down.

## Neutral input pose (Meshy)
`COMMON.md` section 5. **Light the image brightly and evenly; do not underexpose**; keep eye whites and ear backs clear. Plain **white `#FFFFFF`** or light grey `#EDEDED` background (dark fur separates from either).

## On-model / off-model
**ON ✔** [ ] tag paw can show green ✓ / red ✕ states (separate paw symbol) · [ ] dark plum-black fur with visible form · [ ] GREEN eyes, very big, visible whites · [ ] cream-white ear backs, pink inside · [ ] plain dark collar + gold paw tag · [ ] short plump tail over back · [ ] stocky, full cheeks · [ ] **smooth, simple, chunky**
**OFF ✘** [ ] eyes not green / small · [ ] collar coloured or with dots, tag missing/not gold · [ ] pure flat black blob · [ ] stripes/white patches · [ ] looks like Evie recoloured · [ ] fur strands, fuzz halo, photoreal/Pixar-fur · [ ] extra/fused limbs
