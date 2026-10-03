# Style Guide v1.1 — APPROVED by lead

> Status: **approved v1.1** (lead decisions: Q-01, Q-04, Q-05, Q-07, Q-10 to Q-14 accepted). v1.1 replaces v1.0 after the lead's direction change:
> **Tommie does not like the realistic/Pixar-fur look of the reference images. New direction = STYLISED 3D CARTOON with SIMPLE fur.**
> The reference images in `assets/characters/` are now **colour and markings reference only, NOT the rendering style.**
> Colour hexes: `character-sheets/`. Locations: `backgrounds/`. Copy-paste prompts: `meshy/`. Blender recipes: `blender/`.

**One-line direction:** chunky, toy-like 3D cartoon characters with smooth short fur (or simple cloud-wool shapes), big expressive eyes, clean bright saturated colours and soft two-tone toon shading, in simple, bold, clean 3D worlds lit by warm golden hour.

---

## 1. The rules that never change
1. **Contrast rule:** characters = the brightest, most saturated, highest-contrast thing in frame. Worlds are simpler, a little less saturated (about 20-25 % lower), with fewer shapes.
2. **Consistency lock:** Evie = white, black patch top-left of head, BLUE eyes, PINK (raspberry) collar. Justin = black, GREEN eyes, DARK collar. Both: gold paw tag. Cotton = cream wool, blue eyes, light-blue collar, gold heart bell. Toffee = chestnut wool, green eyes, green collar, gold heart bell.
3. **Readable silhouettes:** each character recognisable as a solid black shape at 64 px.
4. **Scale:** world slightly oversized so the characters feel small and adventurous (section 6).
5. **No** photoreal anything, no fur strands, no texture noise, no text baked into images, no real people or brands.
6. **Dutch sky = about 50 % of every wide shot:** big, with a few big simple clouds.

---

## 2. What "stylised with simple fur" means (the look in 8 lines)
1. **Forms:** bold, rounded, chunky; head large (about as wide as the body); short legs; toy / vinyl-figure feel.
2. **Fur:** **smooth, short, matte.** No strands, no fuzz halo. Suggest fur only with 3-6 **chunky tufts** (cheek ruff, chest tuft, tail tip, ear tuft) as simple geometry shapes.
3. **Wool (lambs):** **12-20 big, soft, rounded clumps** (like clouds or popcorn) as low-poly bumps, not curls.
4. **Eyes:** very big, glossy, simple: white + coloured iris + big pupil + 2 catchlights. The main place for detail and the main carrier of emotion.
5. **Colour:** clean flat areas of bright saturated colour, 1 shadow tone per colour (plum-tinted), no gradients inside a colour area except a soft iris gradient.
6. **Shading:** soft **two-tone toon** (light + shadow step, with a soft-ish edge), thin warm rim light. No specular noise, no subsurface, no hair shaders.
7. **Texture:** flat colour (a tiny hand-painted marking texture is fine, e.g. Evie's patch). Minimal or no normal maps.
8. **Edges:** no black outlines; definition comes from value contrast and the rim light.

---

## 3. Palette

### 3.1 Master golden-hour palette
| Role | Name | Hex |
|---|---|---|
| Sun / key light | Golden sun | `#FFC76B` |
| Highlight / world white | Warm cream | `#FFF1D6` |
| Warm bounce | Apricot | `#F7B58A` |
| Sky top (day) | Sky blue | `#8EC8F0` |
| Sky horizon (golden hour) | Peach | `#FFD9A8` |
| Cloud shadow | Dusk rose | `#F2A5A0` |
| Toon shadow tint (multiply) | Plum | `#B8A4D8` (see `blender/SHADING.md`) |
| Deep shadow / night | Evening indigo | `#2B2D52` |
| Gold UI / tags / bells | Tag gold | `#FFB520` |

Shadows are **plum/violet, never grey or black**. World whites are **cream** (`#FFF1D6`), never `#FFFFFF`, so Evie (`#FFF6EC`) stays the brightest thing in frame.

### 3.2 Character base colours (clean, saturated; details in `character-sheets/`)
| Character | Main | Accent colours | Eyes | Collar | Gold |
|---|---|---|---|---|---|
| Evie | white `#FFF6EC` | black patch `#2A2030`, ears `#FFA9A0` | blue `#1E7FD6` | raspberry pink `#D01F4B` | `#FFB520` |
| Justin | plum-black `#352B3D` | ears `#FF9FA0`, ear backs `#FFEBDD` | green `#3FB52A` | dark `#17121C` | `#FFB520` |
| Cotton | cream `#FFF3DF` | ears `#FFA8A0`, hooves `#5A4040` | blue `#1E7FD6` | light blue `#7FB8F0` | `#FFB520` |
| Toffee | chestnut `#9C4A1C` | cream `#FFE9CF`, hooves `#4A2E26` | green `#5CC236` | leaf green `#43A047` | `#FFB520` |
These are **brighter and cleaner than the reference art** on purpose (toon shading needs room to show a shadow step; pure black cannot). Approved (Q-10).

### 3.3 Per-episode palette (one accent each)
Swatches: sky-top / sky-horizon / ground / secondary / **ACCENT** / structure / shadow / highlight. Accent covers ~10-15 % of the frame, plus thumbnail border and title card. All values are **flat colours** for simple materials.

| Ep | Place | Sky top | Sky horizon | Ground | Secondary | **ACCENT** | Structure | Shadow | Highlight |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Afsluitdijk | `#8EC8F0` | `#FFE3B0` | `#8CBF6A` | `#B9B1A6` | **`#3FA7A6`** sea teal | `#E8DCC8` | `#4F5B73` | `#FFF1D6` |
| 2 | Schokland | `#A9D3F0` | `#FFE0A8` | `#9CC657` | `#B8D77A` | **`#E3B93C`** field gold | `#F3EBD8` | `#6A5A5E` | `#FFF4D0` |
| 3 | Giethoorn | `#9AD0E8` | `#FFD9B0` | `#7DB86A` | `#C9A24B` | **`#4FA37A`** canal green | `#B5533C` | `#3F5A5C` | `#FFEFD0` |
| 4 | Hunebedden | `#9CB8DC` | `#F4CBB0` | `#6E8F4E` | `#6B4B38` | **`#8B8499`** stone grey-purple | `#A29BB0` | `#4A405C` | `#F6E6D6` |
| 5 | Kootwijkerzand | `#9FD0F0` | `#FFD8A0` | `#E8A55B` | `#3F6B4A` | **`#9A5FB0`** heather purple / sand orange | `#F2D29B` | `#5B4A6B` | `#FFF0D0` |
| 6 | Delta Works | `#7DB8E8` | `#FFD4A8` | `#BFC6CC` | `#3C8FC8` | **`#4C7FB0`** steel blue | `#D5DADF` | `#3F4F6E` | `#FFF1D6` |
| 7 | Wadden Sea | `#B5CCE6` | `#F6D3CC` | `#B79A94` | `#9CC4D0` | **`#E7C6CF`** silver-pink | `#F3D9D2` | `#6A5668` | `#FFF4EA` |
Swatch board: `branding/palette-board.svg`.

### 3.4 Time-of-day variants
| Variant | Use | Sky | Sun colour | Mood |
|---|---|---|---|---|
| **Day** | opening question, energetic exploring | bright blue, white clouds | `#FFE9C4` | clear, cheerful |
| **Golden hour** (default hero look) | discoveries, concept explanation, thumbnails | peach horizon, blue top | `#FFC76B` | warm, storybook |
| **Dusk** | recap, teaser, bedtime outro | indigo top, rose/apricot horizon | `#F2A5A0` (low, soft) | calm, goodnight beat |
The **outro is always dusk**.

---

## 4. Lighting rig for Blender (toon, EEVEE)
Implemented in `pipeline/blender/evg/lights.py` (`build_rig`). Full recipe in `blender/LIGHTING_AND_CAMERAS.md`. Rig collection `RIG_Golden`:

| Light | Type | Role | Colour | Strength (start) | Placement |
|---|---|---|---|---|---|
| **KEY_sun** | Sun (angle 5°) | golden-hour sun, hard-ish shadow | `#FFC76B` | 3.5 | elevation 14-20°, azimuth +40° from camera axis (front-right) |
| **FILL_sky** | Area disk, large | cool fill into the shadow side | `#9EC5FF` | ≈ 0.3 × key | opposite the key, low |
| **RIM_L / RIM_R** | Area disk, small | thin warm **rim light** that separates characters from the world | `#FFD9A8` | bright (≈ 2× key at the edge) | behind and above each side, ~150° from the camera axis |
| **KICK_ground** | Area disk, low | warm bounce under chin/belly | `#F7B58A` | ≈ 0.15 × key | low, front |
| **TAG_glow** | Point | gold glow on the paw tag/bell at discovery moments | `#FFC76B` | animated 0 → 40 → 0 | at the tag |
**Light linking:** rim, kick and tag-glow are linked to the character collection only. Key and fill light everything.
Toon materials already include a **thin material-side rim** so the look survives if lights are changed.

Variant table: `Day` sun 45° / `#FFE9C4` / 4.0; `Golden` 17° / `#FFC76B` / 3.5; `Dusk` 5° / `#F2A5A0` / 1.6 (values in `evg/palette.py`).

Render settings: **EEVEE** (toon needs *Shader to RGB*, EEVEE only), 1920×1080 or 1080×1920, 24 fps, 64 samples, **Standard** view transform (AgX/Filmic wash out flat toon colours; tested), no motion blur, no outlines. Depth of field: **f/8-f/22** (close f/11, wide f/22). A kitten is 0.3 m deep, so a realistic f/2.8 close-up blurs half the face (tested); background softness comes from distance. Focus point = the face.

---

## 5. Camera presets and safe areas
Implemented in `pipeline/blender/evg/cameras.py`. Sensor 36 mm, **horizontal fit** (same lens meaning in both aspects).

| Preset | Lens 16:9 | Lens 9:16 | Height | Distance | Use |
|---|---|---|---|---|---|
| `wide_establish` | 24 | 28 | 1.3 m | 11 m | arrival; characters tiny, sky 50 % |
| `wide_two` | 28 | 40 | 0.35 m | 3.5 m | walking/travelling |
| `medium_two` | 40 | 60 | 0.25 m | 1.8 m | two characters talking |
| `medium_single` | 50 | 70 | 0.22 m | 1.25 m | one speaker |
| `close_up` | 85 | 110 | 0.20 m | 0.8 m | emotion, reaction |
| `extreme_close_tag` | 100 | 135 | 0.15 m | 0.4 m (f/22, focus on the tag) | glowing tag/bell |
| `low_hero` | 28 | 40 | 0.08 m | 1.2 m (tilt up 10°) | brave moment, landmark behind |
| `over_shoulder` | 50 | 70 | 0.25 m | 1.0 m | "look at that" reveal |
Horizon at the lower third for sky-heavy wides, middle for dialogue. Never through a head.

**16:9 safe areas** (1920×1080): action 93 % (inset 67×38 px), title 90 % (inset 96×54 px). Faces in the central 70 % width. Subtitle band y 800-980: keep clear of faces.
**9:16 safe area** (1080×1920): content x 60-920, y 250-1400; caption band y 1400-1560; head centre y ≈ 800-1000. Right ~160 px (buttons) and top ~13 % are UI zones. *Check against the current Shorts UI before locking.* Re-render vertical with the 9:16 lenses; do not crop.

---

## 6. Scale
- Characters at real kitten scale: shoulder ≈ 0.22 m, body length ≈ 0.36 m, head width ≈ 0.14 m. Lambs 1.3× (shoulder ≈ 0.30 m). *(Q-04, approved)*
- World modelled at **1.5× real size** relative to the characters. 1 Blender unit = 1 m. Apply scale before export.

---

## 7. Shape language
| Element | Shapes | Notes |
|---|---|---|
| **Kittens** | big circle head, small rounded-triangle ears, plump bean body, short stubby legs, fat curled tail | silhouette = round head + 2 ears + tail curl |
| **Lambs** | cloud body made of rounded clumps, wide floppy ears, slim legs with chunky hooves, round pom tail | silhouette = cloud on 4 legs + flopped ears |
| **Landmarks** | bold simplified geometry: long horizontal (dike), slim tower, flat slabs (hunebed), repeated piers | one hero silhouette per location, nothing else competes |
| **Landscape** | big flat colour bands, rounded hills, simple soft clouds | flat Netherlands = calm horizontals + 1 vertical accent |
| **Props** | chunky, oversized, bevelled, tapered like toys, no tiny details | bevel ≥ 1.5 % of the object size |
| **Textures** | flat colour + 1 shadow tone; maybe one soft gradient on sky/ground | no photo textures, no noise, no normal-map grit |
| **Detail budget** | characters: eyes + tag/bell + a few tufts. World: 3-5 hero props per set. | fewer, bigger things |

### Value / focus (3-value rule)
1. Darkest + brightest + most saturated = characters and gold tags.
2. Mid values = ground and mid props.
3. Low contrast, cooler = far layers and sky.
Blur test: characters must still be the first thing seen.

---

## 8. Do / don't
| Do | Don't |
|---|---|
| Smooth short fur, chunky tufts, cloud-clump wool | Fur strands, fuzz halo, curl detail, photo textures |
| Two-tone toon shading, plum shadows | Grey/black shadows, soft realistic gradients |
| Big glossy eyes with catchlights | Small or realistic eyes |
| Flat saturated colours, one accent per episode | Rainbow palettes, noisy textures |
| Cream world whites | Pure white behind Evie |
| Rim light on characters only | Rim light on the whole scene |
| Same hexes in every shot (character sheets) | Re-colouring a character "to fit the scene" |

---

## 9. Change log
- **v1.1 (approved by lead):** direction change to stylised 3D cartoon with simple fur; toon shading recipe, cleaner saturated character colours, simpler worlds; references demoted to colour/markings only; lighting and cameras kept but toon-adapted.
- v1.0 (superseded): realistic soft-fur Pixar look.
- v0.1: initial direction (lead).
