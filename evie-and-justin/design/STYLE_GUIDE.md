# Style Guide v1.0 — PROPOSED, awaiting lead approval

> Status: **proposed – awaiting lead approval.** Nothing here is canon until the lead locks it (see `README.md`).
> Replaces the v0.1 draft. Everything from v0.1 is kept; v1.0 adds palette hexes, a Blender lighting rig, camera presets and shape language.
> Character colours referenced here are defined in `character-sheets/`. Location detail lives in `backgrounds/`.

**One-line direction:** cartoony 3D storybook, warm golden hour, the characters are the brightest, most detailed and most saturated thing in every frame, worlds are simpler and painterly.

---

## 1. The rules that never change (carried over from v0.1)
1. **Contrast rule:** characters = highest detail, highest local contrast, highest saturation. Worlds stay about 25–30 % lower in saturation and a little lower in detail.
2. **Consistency lock:** Evie = white, black patch top-left of head, BLUE eyes, PINK (raspberry) collar. Justin = black, GREEN eyes, DARK collar. Both: gold paw tag. Cotton = cream wool, blue eyes, light-blue collar, gold heart bell. Toffee = chestnut wool, green eyes, green collar, gold heart bell.
3. **Scale:** world is slightly oversized so the characters feel small and adventurous (see section 5).
4. **No** photoreal backgrounds, **no** text baked into images, **no** real people or brands.
5. **Dutch sky = about 50 % of every wide shot.** Big, fluffy, layered clouds.

---

## 2. Palette

### 2.1 Master golden-hour palette (used in every episode)
| Role | Name | Hex |
|---|---|---|
| Sun / key light | Golden sun | `#FFC76B` |
| Highlight | Warm cream | `#FFF1D6` |
| Warm bounce | Apricot | `#F7B58A` |
| Sky top (day) | Sky blue | `#8EC8F0` |
| Sky horizon (golden hour) | Peach cloud | `#FFD9A8` |
| Cloud shadow | Dusk rose | `#F2A5A0` |
| Shadow tint (never use pure black) | Plum shadow | `#5B4A6B` |
| Deep shadow (dusk, night outro) | Evening indigo | `#2B2D52` |
| Gold UI / tags / badge | Tag gold | `#EBA02B` |

Shadows are **tinted plum/indigo, not grey or black**. Whites in the world are **cream** (`#FFF1D6`), never `#FFFFFF`, so Evie (near-white) still reads as the brightest thing in frame.

### 2.2 Per-episode palette (one accent each, as in v0.1)
Each episode has 8 swatches: sky-top / sky-horizon / ground / secondary / **ACCENT** / structure / shadow / highlight. The accent is used for ~10–15 % of the frame (props, water, flowers) and in the episode's thumbnail border and title card.

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

### 2.3 Time-of-day variants (all locations)
| Variant | Use | Sky | Sun colour | Mood |
|---|---|---|---|---|
| **Day** | opening question, energetic exploring | bright blue, white-cream clouds | `#FFE9C4` | clear, cheerful |
| **Golden hour** (default hero look) | discovery moments, concept explanation, thumbnails | peach/gold horizon, blue top | `#FFC76B` | warm, storybook |
| **Dusk** | recap, "where next?", bedtime outro | indigo top → rose/apricot horizon | `#F2A5A0` (low, soft) | calm, goodnight beat |

Rule: the **outro is always dusk**; it is the brand link to the bedtime stories.

---

## 3. Lighting rig for Blender (build once, reuse in every shot)

Build the rig as a collection `RIG_Golden` appended into every scene by `build_shot.py`. Values are starting points for **EEVEE (Next)**; Blender 4.2+, AgX view transform. All values are tweakable per time-of-day variant (table below).

### 3.1 Lights
| Light | Type | Role | Colour | Strength (start) | Placement |
|---|---|---|---|---|---|
| **KEY_sun** | Sun | golden-hour sun, casts the shadow | `#FFC76B` (golden) | 3.5 | elevation 14–20° above horizon, azimuth 35–50° to the side of the camera, slightly in front of subjects (3/4 front-side key). Angle (softness) 4–6°. |
| **FILL_sky** | Area, large (size ≈ 8 m) | cool sky bounce into the shadow side | `#9EC5FF` | ≈ 0.3 × key (key:fill about 3:1 to 4:1) | opposite the key, camera height, soft. No shadows or very soft. |
| **RIM_L / RIM_R** | Area or Spot, size ≈ 1.5 m | **rim glow on fur** and the "fuzz halo" seen in the reference art | `#FFD9A8` (warm) | 6–10 (rim must be bright; check it is 2× key at the edge) | behind and above each character, 120–150° from the camera axis, aimed at the head/shoulder line. |
| **KICK_ground** | Area, low | warm ground bounce, lifts belly/chin | `#F7B58A` | ≈ 0.15 × key | low, in front, pointing up. |
| **TAG_glow** (optional) | Point, tiny | paw-tag "adventure badge" glow at discovery moments | `#FFC76B` emissive | animated 0 → 40 → 0 W | at the tag, 2 cm in front. Pair with emission strength on the tag material. |

**Light linking (Blender 4.0+):** link `RIM_*`, `KICK_ground` and `TAG_glow` to the **character collection only**, so rim light never washes the background. Key and fill light everything.

### 3.2 World / sky
- Default: **Sky Texture (Nishita)** with sun elevation matching the key (14–20° golden hour; 45° day; 3–6° dusk), air density 1.0–1.3, dust 0.5, ozone 1.0. Set `KEY_sun` to the same direction (drive both from one empty).
- If a painted sky plate is used (preferred for the "painterly" look): an emissive background sphere with the sky image, plus a Nishita world at low strength (0.3) only to light the characters.
- Painted skies/backgrounds are baked **flat and unlit** (emission only) so the rig does not double-light them.

### 3.3 Fur / wool shading for the glow
- Principled BSDF: roughness 0.6–0.7, **Sheen weight 0.5–0.8** (tint = fur colour lightened), Sheen roughness 0.35, Subsurface 0.05–0.1 (tint: warm pink for white fur, tint = base for dark fur). Specular tint low.
- **Fuzz halo trick:** add a Layer-Weight (Fresnel, blend 0.3) → ColorRamp → Mix into emission at ≈ 0.05–0.12 strength, tinted `#FFD9A8`. It gives the soft rim "fuzz" glow even with a flat key.
- Normal map for fur grain (no real hair), as in `meshy/MESHY_BRIEF.md`.
- Eyes: glossy cornea layer + 2 catchlights (one big upper-left matching the key, one small lower-right matching fill).

### 3.4 Render settings (start values)
| Setting | Value |
|---|---|
| Engine | EEVEE Next (fast). Cycles + OpenImageDenoise only for hero stills/thumbnails. |
| Resolution | 1920×1080 (16:9) and 1080×1920 (9:16), 24 fps |
| Samples | EEVEE 64 render samples, shadows soft, raytracing on for reflections |
| View transform | AgX, look "Medium Contrast" (check the cream whites do not clip) |
| Film | Filter 1.5 px, transparent off |
| Depth of field | f/2.8 close, f/4 medium, f/8 wide. Background gets gentle blur. |
| Atmosphere | Mist/volume fog with a cool tint grows with distance (far layers shift toward sky colour) |
| Outline | none (3D storybook, no ink lines) |

### 3.5 Variant table for the rig
| Parameter | Day | Golden hour | Dusk |
|---|---|---|---|
| Sun elevation | 45° | 14–20° | 3–6° |
| KEY colour / strength | `#FFE9C4` / 4.0 | `#FFC76B` / 3.5 | `#F2A5A0` / 1.6 |
| FILL colour / strength | `#9EC5FF` / 1.4 | `#9EC5FF` / 1.0 | `#7C8FD8` / 0.8 |
| RIM strength | 5 | 8 | 6 (warmer, `#FFB48A`) |
| World | blue gradient | peach→blue | indigo→apricot |
| Fog tint | `#CFE6F8` | `#FFD9A8` | `#9A86B8` |

---

## 4. Camera presets
Sensor 36 mm wide (full frame). The `lens_mm` field in `pipeline/shots/*.json` takes the values below. Camera position is in metres relative to the subject in **storybook scale** (kitten shoulder height ≈ 0.22 m, see section 5).

| Preset | Lens | Camera height | Distance to subject | Tilt | Use | Subject height in frame |
|---|---|---|---|---|---|---|
| `wide_establish` | 24 mm | 1.0–1.6 m | 8–15 m | level to slight down | arrival, place reveal; cats tiny, sky 50 % | 5–10 % |
| `wide_two` | 28 mm | 0.35 m | 3–4 m | level | walking, travelling beats | 20–25 % |
| `medium_two` | 40 mm | 0.25 m | 1.6–2.0 m | level | dialogue between Evie and Justin | 45–55 % |
| `medium_single` | 50 mm | 0.22 m | 1.1–1.4 m | level | one speaker | 55–65 % |
| `close_up` | 85 mm | 0.2 m (eye level) | 0.7–0.9 m | level | emotion, reaction, expressions | head fills 60–70 % |
| `extreme_close_tag` | 100 mm | 0.15 m | 0.4 m | level | glowing paw tag/bell discovery | tag ≈ 30 % |
| `low_hero` | 28 mm | 0.08 m | 1.2 m | tilt up 8–12° | brave moments, big landmark behind | 60 % |
| `over_shoulder` | 50 mm | 0.25 m | 1.0 m | level | "look at that!" reveal of the place | foreground 30 % |

Keep the horizon at the **lower third** for sky-heavy wide shots, at the **middle** for dialogue. Never put the horizon through a character's head.

### 4.1 Safe areas
**16:9 (1920×1080)**
- Action safe: 93 % (inset 67 px × 38 px). Title safe: 90 % (inset 96 px × 54 px).
- Character faces stay inside the central 70 % width.
- Subtitles/lower-third band: y 800–980 (bottom 17 %). Keep this band free of faces in dialogue shots.

**9:16 (1080×1920)** — the camera is re-rendered vertical, not cropped (see `lead/PRODUCTION_PLAN.md`), but compositions must still obey the shorts UI:
- Keep important content inside: **x 60–920** (right ~160 px reserved for the like/comment buttons), **y 250–1400** (top ~13 % for the title/search bar, bottom ~27 % for caption + channel name). *Check against the current Shorts UI before locking; it changes.*
- Characters: head centre at y ≈ 800–1000. Captions: y 1400–1560.
- Wide shots in 9:16: use `wide_two` with the camera ~30 % closer and a taller sky; the vertical frame shows more sky and foreground, less side-to-side landscape. Props that matter must sit near the centre column.

---

## 5. Scale
- **Characters at real kitten scale:** Evie and Justin shoulder height ≈ 0.22 m, body length ≈ 0.36 m, head width ≈ 0.14 m. Lambs are **1.3× kitten size** (shoulder ≈ 0.30 m). *Proposal: see Q-04 in `lead/inbox/design.md`.*
- **World modelled at 1.5× real size relative to the characters** (e.g. a door ≈ 3 m, a hunebed capstone feels huge). Do this by scaling the character collection to 0.67 against real-world-scaled sets, or scaling sets 1.5× — pick one and never mix.
- 1 Blender unit = 1 m. Apply scale before export.

---

## 6. Shape language
| Element | Shapes | Notes |
|---|---|---|
| **Kittens** | circles and soft rounded triangles; head ≈ as wide as the body; big round eyes; fluffy tail like a question mark | Silhouette must read as "kitten" filled solid black: round head + two ears + tail curl. |
| **Lambs** | scalloped / cloud-like outlines (curls), wide floppy ears, small round tail pom | Silhouette = cloud with legs and floppy ears. |
| **Landmarks** | strong geometric forms, simplified but recognisable: long horizontals (dike), vertical tower, flat slabs (hunebed), tall pier rows | One hero silhouette per location. |
| **Landscape** | long horizontal bands, rounded hills, soft clouds | The Netherlands is flat: use horizontals as calm, add rhythm with vertical props (poles, trees, towers). |
| **Props** | chunky, slightly oversized, bevelled edges (no hard sharp corners), slightly tapered like toys | Edge bevel ≥ 1 % of the object's size. |
| **Textures** | flat colour + soft gradient + subtle painterly noise; no photo textures; 2–3 value steps per surface | Detail density decreases from foreground to far layers. |
| **Lines** | no outlines; edge definition comes from value contrast and rim light | |

### Value / focus structure (3-value rule)
1. **Darkest + brightest + most saturated** = the characters and their gold tags.
2. **Mid values** = ground and mid-ground props.
3. **Low-contrast, cooler** = far layers and sky.
Test: blur the frame. The characters must still be the first thing you see.

---

## 7. Do / don't
| Do | Don't |
|---|---|
| Tinted plum/indigo shadows | Pure black or grey shadows |
| Cream whites in the world | Pure white backgrounds near Evie |
| Rim light on the characters | Rim light on the whole scene |
| Soft painterly textures | Photo textures, noisy detail behind characters |
| One accent colour per episode | Rainbow palettes |
| Same colour hexes every shot (see character sheets) | Re-colouring a character "to fit the scene" |
| Calm horizontals + one vertical landmark | Cluttered skylines |

---

## 8. Change log
- v1.0 (proposed): palette hexes per episode, Blender rig, camera presets, safe areas, shape language, scale.
- v0.1: initial direction (lead).
