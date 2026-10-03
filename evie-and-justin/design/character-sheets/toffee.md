# Toffee — character sheet (approved v1.1, stylised simple wool)
Working name. Debuts end of Ep.4, joins Ep.5. Colour/markings reference only (NOT the style): `assets/characters/lambs-reference.png`, right lamb. Shared: `COMMON.md`.
**Personality:** bouncy, silly, fearless but clumsy. **Acting:** big hops, overshoot stops, wobbly landings, head leads the body, faster timing than Cotton.

## Colours
| Part | Reference (sampled, lit) | **Base (use this)** | Notes |
|---|---|---|---|
| Wool (chestnut) | `#632E15` | **`#9C4A1C`** | brighter, warmer than the dark reference so toon shading shows |
| Cream chest blaze | `#CF9B74` (shaded) | **`#FFE9CF`** | between the front legs |
| Cream legs ("socks") | `#E5C0AF` | **`#FFE9CF`** | all four lower legs to the knee |
| Face (short cream) | `#ECC2A7` | **`#FFE9CF`** | brown wool crown over the forehead |
| Ears | outer brown | outer **`#7A3A16`**, inner **`#FF9C90`** | floppy |
| Nose | | `#FF9FA8` | |
| **Iris (GREEN)** | `#387128` / `#6B9832` | **`#5CC236`**, rim `#3FA02A`, inner `#8FE060` | slightly yellower than Justin's |
| **Hooves** | `#36221D` | **`#4A2E26`** | chunky |
| **Collar (green)** | `#334214` (shadow) | **`#43A047`** leaf green | clearly a collar green, not an eye green |
| **Bell** | `#E5912B` | **`#FFB520`** gold, heart cut-out `#3A2418` | same as Cotton's |
| Tail pom | | `#9C4A1C` | |

## Proportions
Same as Cotton (body 2.0 HU, height 2.2 HU, ears 0.55 HU, round pom) with: **head slightly more forward and eager**, eyes a touch more open, ears a little higher, **cream socks and chest blaze** (high contrast against the brown). Wool = 12-20 chunky clumps. Metres: shoulder 0.30, body length 0.40, head width 0.17.

## Silhouette
Cloud-clump body like Cotton but **darker and bouncier**; cream socks pop. Cotton vs Toffee differ in **tone** (light vs dark), not just collar colour.

## Collar / bell
Green collar. Gold heart bell, separate object, swings harder (more bounce).

## Expression notes
happy: huge grin, tongue tip, ears flapping · curious: head thrust forward · surprised: whole body pops up · scared_but_brave: wobble, chin out · sleepy: one ear down · laughing: head back, mouth huge. No fangs.

## Neutral input pose (Meshy)
`COMMON.md` section 5. Cream socks and chest visible in the front view; **plain light-grey `#EDEDED` or white background** so the brown separates; bell facing camera.

## On-model / off-model
**ON ✔** [ ] chestnut clump wool, **cream chest + cream socks** · [ ] cream face, brown crown, brown outer ears · [ ] GREEN eyes, very big · [ ] green collar + gold heart bell · [ ] dark chunky hooves · [ ] bouncy/mischievous · [ ] **simple clumps, no curl detail**
**OFF ✘** [ ] grey/black wool, no cream socks/chest · [ ] eyes not green · [ ] collar not green, bell missing/no heart · [ ] looks like Cotton recoloured · [ ] curly-wool detail, photoreal/Pixar-fur · [ ] realistic sheep proportions

## Bell glow (Ep.7, SPOILER)
The gold heart bell **glows lilac/gold when the lamb receives the Moondew Blossom drink in Ep.7**; keep this out of everything published before Ep.7. Recipe: `../blender/FX_GLOW.md` section 9. The bell is a separate object named `<name>_bell` (emissive-capable toon gold). Lambs do **not** use the green/red paw (that is the cats' tag mechanic).

## Birthday flower crown (Ep.7 and later birthdays; no cake)
Toffee wears a **chunky flower crown** on the wool crown: green vine ring + 7 flowers (cream `#FFF1D6`, sunny yellow `#FFD84D`, pink `#FFA8A0`, gold centres) with small leaves; sits on the clumps, **clear of the floppy ears**, pops in with the lilac bell glow (`birthday` FX). Spec, clipping checklist and build: `../props/FLOWER_CROWN.md`. Spoiler-safe only if the script allows; the glow part is an Ep.7 spoiler.
