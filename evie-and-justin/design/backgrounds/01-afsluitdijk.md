# Ep.1: Afsluitdijk — "The Land Below the Sea"
> **v1.1 style update (lead direction):** backgrounds are **simple, bold, clean 3D cartoon**: big flat colour shapes, 3-5 hero props, chunky bevelled forms, no texture noise, no normal-map grit, no fine detail. Facts/sources below are unchanged. Copy-paste prompts: `prompt-packs/01-afsluitdijk.md`.

**Accent:** sea teal `#3FA7A6` (palette row 1). **Hero silhouette:** one long straight dike + the tall monument tower.
**Mood:** huge, calm, windy, the world is wide open; the kittens are tiny. Water on **both** sides.

## What is true (and what we keep)
| Real element | Cartoon version |
|---|---|
| Straight dike, ~32 km long, ~90 m wide, tops out ~7 m above sea level, sloped both sides ([Wikipedia](https://en.wikipedia.org/wiki/Afsluitdijk), [ZJA](https://www.zja.nl/en/De-nieuwe-Afsluitdijk)) | a long straight road + cycle path line running to a vanishing point; slopes with grass (lake side) and stone blocks (sea side) ⚠ |
| Wadden Sea (salt, tidal) on the north-west side, IJsselmeer (fresh lake) on the south-east ([Wikipedia](https://en.wikipedia.org/wiki/Afsluitdijk)) | **sea side = silvery teal, choppier; lake side = brighter, calmer** (matches the Ep.1 script note) |
| Monument tower (architect Willem Dudok, built 1933): a vertical stair tower with viewing platform over the dike, contrasting with the horizontal dike; Lely statue (Mari Andriessen, 1954) stands nearby ([Archello](https://archello.com/project/the-afsluitdijk-visual-master-plan), [Historisch Nieuwsblad](https://www.historischnieuwsblad.nl/stille-getuigen-het-standbeeld-van-cornelis-lely/)) | **tall slim cream concrete tower** with a visible glass/stair slot and a platform; small bronze statue of a man on a plinth beside it |
| Sluice complexes at both ends: rows of concrete machine towers with steel gates between them (architect Roosenburg) ([Archello](https://archello.com/project/the-afsluitdijk-visual-master-plan)) | row of 6-8 chunky towers with gates between, boats waiting; Den Oever = Stevin locks, Kornwerderzand = Lorentz locks ⚠ verify |
| Renewed entrance "Gates of Light" with monumental floodgates ([ZJA](https://www.zja.nl/en/De-nieuwe-Afsluitdijk)) | optional; only if we show the Kornwerderzand end |
Note for the scriptwriters: the monument site is **between Breezanddijk and Den Oever** (Vlieter monument area), the research note says "Breezanddijk"; check ([Tripadvisor listing](https://www.tripadvisor.com/Attraction_Review-g2305673-d14977121-Reviews-Vlietermonument-Den_Oever_North_Holland_Province.html)).

## Layered set
| Layer | Content | Style notes |
|---|---|---|
| **SKY** | huge, 50 % of frame; big cumulus, long streaky clouds low on the horizon | painted plate, soft gradient `#8EC8F0 → #FFE3B0` |
| **FAR** | thin land line (Friesland/Wieringen) far away on the lake side; a faint distant barge; wind-turbine silhouettes optional ⚠ | 2-3 flat values, hazy `#9DB5C9` |
| **MID** | the dike road receding to the vanishing point; guard rail posts; the monument tower on the right third; the stone-block seaside slope | chunky, simplified; road `#B9B1A6` with warm centre line |
| **GROUND** | the cycle path/lay-by where the kittens stand; short grass tufts; warm concrete | clean, bright, empty |
| **FG** | blurred sea-grass, a bollard, a signpost shape (no text), a seagull | blurred, 1-2 items, low |

## Key props to model (Meshy first, then clean)
1. **Monument tower** (Dudok-style, simplified) — hero. Text-to-3D prompt: `chunky stylized cream concrete observation tower, tall slim, glass stair slot, flat viewing platform on top, cartoon storybook, no text`
2. **Lely statue + plinth** (generic bronze figure on a block; do **not** try to match the sculpture, no likeness needed)
3. **Sluice tower row** (6 towers + steel gates)
4. **Stone-block slope / basalt-like wall** (tileable)
5. **Road + guard rail + lamp posts** (Blender, modular 10 m piece)
6. Small boat / barge at the lock; seagulls (low-poly flock, 3 poses)

## Time-of-day variants
| Variant | Look |
|---|---|
| Day | bright blue, white clouds, sea teal vivid; long cast shadows short |
| **Golden hour (default)** | sun low over the Wadden side, dike road glows peach, monument rim-lit; **lake side calm mirror of the sky** |
| Dusk | indigo top, apricot horizon, dike lamp posts on (small warm glows), lights in the sluice towers; the sea silver-violet |

## 9:16 notes
- Vertical frame shows **more sky and more road**: put the vanishing point at the centre column, horizon at the lower third, and keep the tower **centre-right** (not on the far right, where the Shorts buttons sit).
- The "water on both sides" read works as two thin horizontal bands left and right of the road: widen both slightly and keep the road perfectly straight (the straightness is the point).
- Hero shorts shot: `low_hero` with the tower behind.

## Prompt starter (for painted sky/far plates)
`Cartoony 3D storybook background, Afsluitdijk, long straight dike road to the horizon, sea on one side and calm lake on the other, slim cream concrete monument tower, huge sky with fluffy clouds, warm golden-hour light, flat clean colours, no texture noise, no characters, no text, empty lower third, wide 16:9.`
