# <Name> — character sheet (proposed / locked vX.Y, stylised simple fur)
Canon entry: `lead/CHARACTERS.md` (add the character there first, **lead owns it**). Reference art (**colour/markings only, NOT the style**): `assets/characters/<file>.png`. Shared specs: `COMMON.md`.
Debuts in: Ep.<n>. Species / body plan: <kitten | lamb | other quadruped | biped>.

**Role/personality in one line:** <...>
**Acting notes:** <how they move, tempo, signature gestures, signature sound>

## Colours
| Part | Reference (sampled, lit) | **Base (use this: clean, bright, saturated)** | Notes |
|---|---|---|---|
| Fur/wool main | `#` | `#` | |
| Secondary fur/markings | `#` | `#` | where exactly (describe left/right as seen from the front) |
| Ear inner | `#` | `#` | |
| Nose | `#` | `#` | |
| **Iris** | `#` | outer `#` → inner `#` | |
| Pupil / lashes / brows | | | |
| Pads / hooves / feet | `#` | `#` | |
| **Collar / accessory** | `#` | `#` | |
| **Tag / bell / signature object** | `#` | `#` | metal? emissive? |
(Sample with `tools/sample_colours.py`; then pick a cleaner, brighter, more saturated Base of the same hue. Add the Base hex to `pipeline/blender/evg/palette.py`.)

## Markings (exact)
<What, where, how big (% of head width), asymmetry rules.>

## Proportions (head-units, 1 HU = head width)
| Measure | Value |
|---|---|
| Body length / standing height / shoulder height | |
| Head shape and ratio | |
| Eyes (size, gap, position) | |
| Ears | |
| Muzzle | |
| Legs | |
| Tail | |
| Fur/wool: smooth short matte + 3-6 chunky tufts, OR 12-20 cloud clumps. No strands. | |
In metres (STYLE_GUIDE section 5): shoulder height __, body length __, head width __.

## Silhouette
<One sentence + the dot test (what must still read at 64 px) + how it differs from the closest existing character.>

## Collar / tag / bell details
<Shape, size, attachment, rig notes (separate object? bone chain?), glow rule.>

## Expressions (COMMON.md section 3) — notes
| Expression | Note |
|---|---|
| happy / curious / surprised / scared_but_brave / sleepy / laughing | |
| optional extras | |
Visemes: COMMON.md section 4 (note any anatomical difference, e.g. no fangs, beak, tusks).

## Neutral input pose (Meshy)
COMMON.md section 5 + character-specific notes (background colour, what must be visible).

## On-model / off-model checklist
**ON-MODEL ✔**
- [ ] ... (always include: simple/chunky, no fur detail)

**OFF-MODEL ✘**
- [ ] ... (always include: fur strands, fuzz halo, photoreal/Pixar-fur look)

## Approval
| Date | Version | Approved by | Notes |
|---|---|---|---|
