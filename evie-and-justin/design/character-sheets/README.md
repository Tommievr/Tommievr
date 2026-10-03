# Character sheets (proposed v1.0 — awaiting lead approval)

| File | What |
|---|---|
| `COMMON.md` | Shared specs: expressions, visemes, neutral-pose rules for Meshy, on-/off-model method, how the colours were sampled |
| `evie.md` | Evie (white kitten) |
| `justin.md` | Justin (black kitten) |
| `cotton.md` | Cotton (cream lamb, working name) |
| `toffee.md` | Toffee (brown lamb, working name) |
| `_TEMPLATE.md` | Copy this for every new character |

## About the hex values (read once)
Colours were **sampled by script from `assets/characters/*.png`** (median of pixels in hand-picked regions, so the numbers are repeatable).
The reference art is rendered in **warm golden-hour light**, so sampled values are already tinted warm and some are in shadow.
Each sheet therefore lists:
- **Sampled (lit)**: what the reference pixels actually are.
- **Albedo (proposed)**: the de-lit base colour to use for the Meshy texture and Blender material. It is an **estimate by eye** that keeps the hue of the reference. Lock after Tommie compares the first Meshy output.
Rule of thumb: Blender material = albedo, the rig (see STYLE_GUIDE section 3) puts the golden light back on.
