# Backgrounds (v1.1: simple, bold, clean 3D cartoon)
One brief per episode location. Palette hexes come from `../STYLE_GUIDE.md` section 2.2; rig and cameras from sections 3-4.

**Prompt packs (copy-paste, per location): `prompt-packs/NN-*.md`** (background/sky/far image prompts for day/golden/dusk, Meshy prop prompts + settings, what to build by hand). Generator: `tools/build_prompt_packs.py`.

| File | Ep | Location |
|---|---|---|
| `01-afsluitdijk.md` | 1 | Afsluitdijk |
| `02-schokland.md` | 2 | Schokland |
| `03-giethoorn.md` | 3 | Giethoorn |
| `04-hunebedden.md` | 4 | Hunebedden, Drenthe |
| `05-kootwijkerzand.md` | 5 | Kootwijkerzand |
| `06-delta-works.md` | 6 | Neeltje Jans / Oosterscheldekering |
| `07-wadden-sea.md` | 7 | Wadden Sea mudflats |

## How each set is built (all locations)
- **Layers (front to back):** `FG` foreground (framing props, blurred) → `GROUND` (walkable strip where the characters stand, 3-6 m deep, simple and clean) → `MID` (hero props) → `FAR` (landscape bands, simplified) → `SKY` (painted plate / Nishita).
- **Parallax:** each layer is a separate collection (`<LOC>_FG`, `_GROUND`, `_MID`, `_FAR`, `_SKY`) so a slow camera slide gives cheap depth. 9:16 re-render uses the same collections.
- **Meshy props:** hero props are generated per brief (text-to-3D, then cleaned). Everything else is Blender primitives with bevels + flat toon materials (`evg.toon.simple_material`). Props follow style rules: chunky, bevelled, 1.5x world scale.
- **Image-generated layers** (sky, far bands) use the prompts in `prompt-packs/`; they are used flat (emission), unlit.
- **Characters' zone:** lower third, **clear and simple** ground, no clutter behind the heads (STYLE_GUIDE contrast rule).
- **Facts:** visual elements were web-checked (sources per brief). **Anything marked ⚠ is not confirmed and goes to the scriptwriters to verify** before it is spoken as a fact; the visuals are stylised anyway.
- **Variants:** Day / Golden hour (default) / Dusk. Dusk is the outro everywhere.
