# Lamb birthday flower crown (Ep.7): prop spec, proposed v1.1
Lead decision: **lamb birthday = flower crown + lilac bell glow, no cake.** A celebration, not ageing. Used in Ep.7 (and later birthdays). Simple, stylised, **built in Blender**, sits on the lamb's wool clumps and **never clips the floppy ears**. Reuses `bell_glow`.

## 1. Design
| Item | Spec |
|---|---|
| Shape | a thin **green vine ring** carrying **7 chunky flowers** (5 rounded petals + gold centre) with a **small leaf** between each pair; ring tilted ~8° forward so the front flowers face the camera |
| Size | ring radius ≈ **72 % of the head's half-width at crown height** (≈ 8.8 cm on the 1.3x lamb placeholder), flower ≈ 2 cm across (chunky, readable at `medium_two`); vine thickness ≈ 4-5 mm |
| Placement | sits **on the wool crown** (30 % of the vine sunk into the clumps), centred on the top of the head, **≥ 6 cm above the ear attachment** (ears are low on the sides) so it can't touch the floppy ears even when they flap |
| Colours | vine `#4F9A58`, leaves `#6CC070`, centres gold `#FFB520`. **Cotton:** petals pink `#FFA8A0`, cream `#FFF1D6`, lilac `#CDB8F2`. **Toffee:** cream `#FFF1D6`, sunny yellow `#FFD84D`, pink `#FFA8A0` (reads on chestnut wool). Hexes in `evg/palette.py` (`CROWN`) |
| Material | flat toon (`toon.simple_material`), thin rim; no petal texture; no cloth/flower simulation |
| No | no cake, no candles (decided); no real flower species detail; nothing text-like |
| Animation | pops in (scale 0 → 1.15 → 1 over 10 frames) when it is "placed"; gentle bounce follows the head bone; optional tiny sparkle at placement |

## 2. Build
`fx.make_flower_crown(root, scheme=None, n=7, frame=None)` builds it from primitives (tested on the placeholder lambs; render `blender/example_birthday.png`). For the real models:
1. Hand-build the vine ring (Torus, minor ≈ 0.045 of the major radius) and 7 flowers (5 flattened UV spheres + 1 centre sphere), or reuse the code positions.
2. Parent the anchor `<name>_crown` to the **head bone**; keep the ring radius so the vine sinks into the wool clumps and the flowers rest on them.
3. **Clipping checklist:** [ ] vine does not poke through the face/forehead (check `close_up`) · [ ] flowers clear the ears in `ear_flop` and `expr_surprised` (ears flare up and out) · [ ] stays on in `hop`/`skip` (it follows the head bone) · [ ] 9:16 framing: crown inside the top safe area (head centre y ≈ 800-1000 leaves room).
Shot spec: character key `"crown": true` (always on) or fx `{"type": "flower_crown", "characters": ["cotton"], "frame": 12}` (pops in).

## 3. Birthday FX (reuse `bell_glow`)
fx `{"type": "birthday", "characters": ["cotton", "toffee"], "frame": 12, "length": 72}` = crown pop-in at `frame` + `bell_glow` 4 frames later (bell swell, 3 lilac rings, lilac + gold sparkles; recipe in `blender/FX_GLOW.md` section 9). Palette link: lilac = the Blossom drink, gold = the bell.
Timeline: 0 lambs stand together · 12 crown pops on (soft chime) · 16 bells glow, rings and sparkles · 40 lambs look at each other (`expr_laughing`/`happy`) · 72 settle; music is the party (script/audio).
**Spoiler rule:** with the drink/bell glow it is an **Ep.7 spoiler** (`"spoiler": "ep07"`); the plain crown without glow is fine for Shorts only if the script allows.

## 4. Note for the lead/writers
The Ep.7 script has Toffee ask "can we still have birthdays? With cake?" (`scriptwriters/scripts/ep07-wadden-sea.md`). The visual decision is **no cake**: a spoken line is fine, but there should be no cake prop on screen (or flip the decision: cake is a very small extra prop, not designed).
