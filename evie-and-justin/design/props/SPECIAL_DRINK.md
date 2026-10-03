# The Special Drink (Ep.1 lore): prop design, proposed v1.1
Lore (lead): in Ep.1 the kittens find a **special drink that stops them ageing**. This is why Evie and Justin stay small forever. Needed: a clear **fantasy** prop, **kid-safe**, **not resembling real alcohol or medicine**, plus a glow that links to the **paw-tag discovery moment**.

## 1. Design rules (safety first)
- **No bottle-and-label look, no amber/red/green liquid, no dropper, spoon, pill, syringe, cross, skull, fizz like soda or champagne.** Those read as alcohol, medicine, poison or a soft drink.
- **Clearly magical and in-story:** it is a *found, glowing, natural thing* (flower, acorn cup), colour **lilac + gold** (the dusk/bedtime palette, `STYLE_GUIDE` 3.4), glowing and sparkling.
- **Nobody is shown drinking it as a model for kids:** the kittens *discover* it, sniff, tag glow, and (script decision) taste a drop in-world. Suggest the writers keep a light "it only works in stories" beat. No packaging, no brand, no text on it.
- Kitten-sized and cute: the prop is **tiny** (about 8-12 cm tall in the kittens' world), so it feels like a treasure, not a product.

## 2. Options (recommendation first)
| | Option | Look | Why / risk |
|---|---|---|---|
| **A (recommended)** | **Moondew Blossom** (`blossom`) | six pale-lilac petals open like a small cup on a short green stem, holding a **floating glowing droplet** of lilac light with a tiny gold star | **Least like alcohol or medicine** (no bottle at all), natural fantasy, cats can sniff/lap it, easy silhouette, ties to the Dutch landscape (flowers on the dike). Glow is a separate sphere, so it is easy to animate |
| B | **Star Acorn Cup** (`acorn`) | a big acorn cap used as a chalice, glowing lilac liquid, a gold star floating | Cute and nature-based; slightly reads as a "cup of drink", fine for a fantasy cup; harder to see liquid from the side |
| C | **Dewdrop Flask** (`flask`) | tiny round pale-blue glass flask with cork, glowing lilac liquid | Strongest read as "the potion", but **closest to a medicine/drink bottle**; only use with the safety rules above (no label, no dropper). Not recommended |
Placeholders of all three exist in code (`fx.make_drink_placeholder`, example `pipeline/shots/example_discovery_placeholder.json`, render `blender/example_discovery.png`).

## 3. Colours
| Part | Hex | Note |
|---|---|---|
| Glow / liquid (core) | `#B9A2FF` lilac | keep emission strength <= ~2.5 (Standard view clips white) |
| Glow deep / shadow | `#7A5FE0` | |
| Sparkles / star | `#FFE08A` pale gold | same hue family as the paw tags (`#FFB520`) so the tags "answer" the drink |
| Petals | `#E9D8FF` | toon material |
| Stem | `#6CC070` | |
| Acorn cap (B) | `#B9763A` | |
| Glass (C) | `#DDEBFF` | |
Also in `pipeline/blender/evg/palette.py` (`DRINK`).

## 4. Meshy prompts (text-to-3D, ≤ 600 chars each; settings as for props in `backgrounds/prompt-packs/`)
Settings ⚠: Art style **Cartoon**, Topology **Quad**, polycount **5,000-10,000**, Symmetry **On**, Pose none, Preview first then texture, export **GLB**.
Make the **cup/holder only**: the glowing liquid/droplet is **a separate Blender sphere** (Meshy bakes glow badly), see `blender/FX_GLOW.md`.

**Moondew Blossom (RECOMMENDED)**
```
Magical flower cup, stylized 3D cartoon prop, six chunky rounded pale lilac petals opening like a small cup on a short green stem, simple bold shapes, smooth, flat clean saturated colors, minimal detail, single object, game-ready low poly
```

**Star Acorn Cup**
```
Giant acorn cup used as a tiny chalice, stylized 3D cartoon prop, chunky rounded warm brown acorn cap with a short stubby foot, hollow open top, simple bold shapes, smooth, flat clean saturated colors, minimal detail, single object, game-ready low poly
```

**Dewdrop Flask**
```
Small round glass flask with a short neck and a cork stopper, stylized 3D cartoon prop, chunky rounded pale blue glass, simple bold shapes, smooth, flat clean colors, minimal detail, empty inside, single object, game-ready low poly
```

Negative prompt (all options):
```
realistic, photorealistic, detailed texture, noise, tiny details, text, letters, label, logo, watermark, cross, skull, syringe, pills, wine bottle, beer, cork screw, people, characters, background, ground, blurry, low quality
```
Then: `blender -b --python pipeline/blender/qa_model.py -- drink.glb --shot qa.png`; `toon.convert_to_toon(obj)`; add a sphere named `drink_glow` with `fx.glow_material("drink_liquid", "#B9A2FF", 1.5)`; save to `pipeline/props/drink.blend` (collection `DRINK`).
Image prompt for a concept check (any image tool): `Stylized 3D cartoon prop concept, a small pale lilac flower cup holding a floating glowing lilac droplet with a tiny gold star, simple bold shapes, flat clean saturated colors, soft toon shading, plain light grey background, no text, no bottle, no label.`

## 5. Hand-off
- Glow, sparkles and the **paw tags glow** discovery moment: `blender/FX_GLOW.md` (+ code `evg/fx.py`).
- Day 1: **optional, after Evie and Justin** (`DAY1_CHECKLIST.md` section 4b).
- Open script questions for the lead/writers: how the drink is introduced and tasted, whether Cotton and Toffee are also affected (lambs join later), and the "only in stories" beat.
