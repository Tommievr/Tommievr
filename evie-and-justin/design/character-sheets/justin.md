# Justin — character sheet (proposed v1.0)
Canon: `lead/CHARACTERS.md`. Reference: `assets/characters/evie-and-justin-reference.png` (right kitten). Shared specs: `COMMON.md`.

**Role/personality in one line:** the explorer/skeptic; bold, funny, a little dramatic, secretly loves facts.
**Acting notes:** cheeky smirks, raised single brow, big dramatic reactions, mock-grumbles; slightly bigger, bouncier movements than Evie.

## Colours
| Part | Sampled (lit) | Albedo (proposed) | Notes |
|---|---|---|---|
| Fur, main (black) | `#221614` – `#2C1810` | **`#2A1A14`** very dark warm brown-black | not pure `#000000`; in golden light the rim turns warm brown-orange |
| Fur, rim glow tips (render only) | — | `#7A4A30` | via the rim light, not a texture colour |
| Fur, chest/belly | `#1C0F0C` | `#241610` | slightly deeper |
| Ear inner (white-pink) | `#E99B81` (lit) / `#7D2D23` (in shadow) | **`#EBA591`** pink with **cream-white fur edge `#F6E3DA`** | the lead's "white-pink inner ears": the **back/outer rim of the ear has white-cream fuzz**; the inside is pink |
| Nose | `#B34C40` | **`#B9564A`** dark rose | rounded triangle |
| **Iris (GREEN)** | `#2E6E14` (median) / `#5C9F0C` (lit) | **outer `#2F7A1A` → inner `#6FB82A`** | radial gradient, darker rim |
| Pupil | — | `#05080C` | large and round, 2 catchlights |
| Eye white | `#F8DFD7` (lit) | `#FBF4EE` | Justin's eye whites are visible and big; Evie's irises dominate |
| Brow marks | — | `#4A3328` | soft brown marks above the eyes |
| Whiskers | — | `#F2EDE6` at 85 % | long, thin, curved, brighter than the fur |
| Paw pads | — | `#5A3A33` (estimated) | warm dark pink-brown |
| **Collar** | `#1C0E06` / lit `#281A14` | **`#22160F`** near-black brown, subtle leather sheen | thin, plain (no dots) |
| **Tag** | `#F1A01A` / lit `#FBB42E` | **`#EBA02B`**, paw emboss `#B8700A` | same disc as Evie's |

## Markings
- **None** (solid dark). The white-pink back of the ear is the only light accent.
- Face is lit by rim glow; make sure the **eyes + whiskers + tag** keep the face readable on dark fur (see checklist).

## Proportions (head-units, 1 HU = head width)
| Measure | Value |
|---|---|
| Body length, nose to rump | ≈ 2.4 HU (slightly stockier than Evie) |
| Standing height to top of head | ≈ 1.9 HU |
| Shoulder height | ≈ 1.2 HU |
| Head | round, fuller cheeks than Evie, ≈ 0.85 : 1 |
| Eyes | ≈ 0.26 HU each (a touch bigger than Evie's); gap ≈ 0.8 eye widths; visible white of the eye on the outer side |
| Ears | ≈ 0.42 HU, wide base, rounded tips; tilted outward |
| Muzzle | short, small dark nose; broad "w" mouth |
| Legs | short, chunky, large front paws with dark toe pads |
| Tail | **shorter and plumper than Evie's** (≈ 0.8 × body length), curls over his back; fuzzy brush |
| Fur | slightly denser/fluffier than Evie; thick cheek ruff; fine fuzz halo |
In metres: shoulder height 0.22, body length 0.35, head width 0.145.

## Silhouette
Same family as Evie (round head, two ears, fluffy tail) but **stockier, plumper tail curled over the back**, fuller cheeks. Both silhouettes must be distinguishable at 64 px.

## Collar / tag details
- Collar thin, near-black brown leather, plain; sits low on the neck so it **contrasts with the fur only through sheen**: add a slight spec highlight along the collar.
- Gold paw-print tag identical to Evie's; **the gold is the main visible accent on his chest**, so keep it bright.

## Expressions (`COMMON.md`) — Justin notes
| Expression | Justin-specific note |
|---|---|
| happy | cheeky half-smirk, one corner higher, tiny fang |
| curious | single raised brow (left or right, pick one and keep it), head forward |
| surprised | dramatic: eyes huge, whites clearly visible all round, mouth wide |
| scared_but_brave | puffed cheeks, tail bristled, jaw set; humour always on top |
| sleepy | grumbly half-lids, slow yawn |
| laughing | big, head thrown back, eyes closed arcs |
| extra (optional) | `grumble`: flat mouth, brows down, ears slightly back (mock-annoyed; used in jokes) |

## Neutral input pose (Meshy)
Follow `COMMON.md` section 3. Justin specifics: use **soft, brighter fill** on the input image, and **do not underexpose** (dark fur loses form and Meshy returns a blob). Keep the whites of the eyes and the pink ear backs clearly visible; whiskers white and short in this input image (long whiskers become geometry noise; add whiskers back in Blender as curves).

## On-model / off-model checklist
**ON-MODEL ✔**
- [ ] Fur dark brown-black, with soft form (not a flat black blob)
- [ ] **Green** eyes, big, with visible eye whites and 2 catchlights
- [ ] Ear backs cream-white/pink, ear insides pink
- [ ] Collar dark, **plain**; tag **gold paw-print disc**
- [ ] Nose dark rose; whiskers pale and visible
- [ ] Tail shorter/plumper than Evie's, curled over his back
- [ ] Slightly stockier than Evie; fuller cheeks

**OFF-MODEL ✘**
- [ ] Blue/yellow/brown eyes
- [ ] Pure `#000000` fur (no form), or grey/brown tabby stripes, or white patches
- [ ] Collar coloured (pink/red/blue) or with dots; tag missing or not gold
- [ ] Looks like Evie recoloured (same tail, same patch)
- [ ] Realistic or slim proportions; long muzzle
- [ ] Outlined/flat 2D look
- [ ] Extra/missing limbs
