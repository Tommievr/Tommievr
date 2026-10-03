# Character sheets (proposed v1.1 — stylised, simple fur; awaiting lead approval)

| File | What |
|---|---|
| `COMMON.md` | Shared specs: style, expressions, visemes, neutral-pose rules for Meshy, on-/off-model method |
| `evie.md`, `justin.md`, `cotton.md`, `toffee.md` | The four characters |
| `_TEMPLATE.md` | Copy for every new character |
| `tools/sample_colours.py` | The script used to sample the reference PNGs |

## The reference images are COLOUR AND MARKINGS REFERENCE ONLY
`assets/characters/*.png` show the **right colours, eye colours, collars, tags/bells and markings**. They do **NOT** show the rendering style: Tommie does not want the realistic/Pixar fur look. The new style is **stylised 3D cartoon with simple fur** (see `../STYLE_GUIDE.md` section 2). Never copy the fur detail, fuzz halo, lighting or texture from the references.

## About the hex values
- The v1.0 hexes were **sampled from the references**; those were warm-lit and shaded, so they were dull. They stay in each sheet as **"Reference (sampled)"** for traceability.
- v1.1 **"Base"** hexes are what we use now: the same hues, **cleaner, brighter and more saturated** for flat toon shading. Toon shading adds a plum-tinted shadow by multiplying `#B8A4D8` into the base (`blender/SHADING.md`), so there is no separate "shade" hex.
- Base hexes live in code too: `pipeline/blender/evg/palette.py`. If you change one, change both.
- Pure black is avoided (Justin = plum-black `#352B3D`) because a toon shadow step cannot show on black. See Q-10.
