# Cotton — character sheet (proposed v1.0)
Working name (see `lead/CHARACTERS.md`). Debuts end of Ep.4 (bell mystery), joins from Ep.5. Reference: `assets/characters/lambs-reference.png` (left lamb). Shared specs: `COMMON.md`.

**Role/personality in one line:** gentle, a little shy, natural peacemaker; the local guide who knows the land. **Her bell ring is her signature sound** (design for a clearly visible, animatable bell).
**Acting notes:** soft, small movements; head dips when shy; skips and hops when happy; looks at others for reassurance.

## Colours
| Part | Sampled (lit) | Albedo (proposed) | Notes |
|---|---|---|---|
| Wool (cream) | `#E6BDA4` (med) / `#EAC4AE` (lit) | **`#F7EBD9`** cream | curly wool; shade colour in render `#E5CDB6` |
| Face fur (short, cream) | `#EBC4AB` | **`#F6E0CB`** | smooth, short, lighter than the wool |
| Ear inner (floppy, pink) | `#EA7E68` | **`#F29A8A`** | wide, big pink inside, cream fuzz edge |
| Nose | `#F89E8D` | **`#F5A092`** | small, pink, rounded |
| Blush | — | `#F7C4B4` | soft |
| **Iris (BLUE)** | `#076093` / lit `#0790C6` | **outer `#0A67A0` → inner `#2FA3D8`** | same blue family as Evie |
| Brow marks | — | `#9A8176` | soft grey-brown |
| Lashes | — | `#1A1210` | |
| **Hooves** (dark) | `#593A2F` / lit `#684330` | **`#4A332C`** | rounded, soft split |
| **Collar (light blue)** | `#5A6670` – `#63717D` (strongly shadowed in the reference) | **`#8FB6DB`** light blue | design intent: the reference collar is in shadow and reads dusty; use a clear soft light blue |
| **Bell** (gold, heart cut-out) | `#E48A19` / lit `#F4A32A` | **`#EBA02B`**, cut-out `#2A1B10` | round sleigh-bell shape, **heart-shaped slot**; metallic 1.0, roughness 0.3 |
| Tail pom | `#EFCBBB` | `#F7EBD9` | small round pom |

## Proportions (head-units, 1 HU = head width)
| Measure | Value |
|---|---|
| Body length | ≈ 2.2 HU |
| Standing height to top of head | ≈ 2.3 HU (lambs are leggier than kittens) |
| Shoulder height | ≈ 1.7 HU |
| Head | round, ≈ 1.0 : 1, wool crown of curls on top and sides, smooth short face |
| Eyes | ≈ 0.24 HU each, wide-set, same cartoon eye as the kittens |
| Ears | **large, floppy, horizontal**, each ≈ 0.55 HU long, attached low on the sides of the head, pink inside, droop slightly |
| Muzzle | short, small pink nose, soft mouth |
| Legs | **longer and slimmer than the kittens'**, slightly bent, ≈ 1.2 HU long, dark hooves |
| Tail | small round pom ≈ 0.3 HU |
| Wool | **curls as texture + normal map** (not geometry): clumped, scalloped silhouette; chest/belly the same wool |
In metres: shoulder height 0.30, body length 0.40, head width 0.17 (1.3 × kitten scale, proposal Q-04).

## Silhouette
Cloud-like scalloped body and head, two wide floppy ears out to the sides, slim legs with dark hooves, round pom tail. Dot test: **scalloped cloud + flopped ears**.

## Collar / bell details
- Collar: thin light-blue band, small stitch dots, sits low on the neck.
- Bell: gold round bell, hangs from a small ring, **heart-shaped slot** on its face (visible from the front), a small dark slit under it. The bell is a **separate object** in the rig (bone chain), so it can swing and ring in sync with audio.
- Bell glow at emotional beats: optional `TAG_glow` equivalent.

## Expressions (`COMMON.md`) — Cotton notes
| Expression | Note |
|---|---|
| happy | gentle smile, blush, head slightly tilted, ears bouncing |
| curious | head tilt, one ear lifts |
| surprised | ears fly out and up, round "o" |
| scared_but_brave | ears back, shoulders in, then chin up |
| sleepy | ears droop fully, slow blink |
| laughing | closed arcs, small tongue, ears bounce |
Visemes: `COMMON.md`; lambs have **no fangs**: `vis_G` shows the top gum/lip instead.

## Neutral input pose (Meshy)
`COMMON.md` section 3. Lamb specifics: **ears relaxed, horizontal** and symmetrical; **legs straight and clearly separated** (long legs make this easy); **bell hanging straight, heart slot facing the camera**; wool outline clean (no loose strands). Mouth closed.

## On-model / off-model checklist
**ON-MODEL ✔**
- [ ] Cream curly wool (scalloped silhouette) + smooth cream face
- [ ] **Blue** eyes, same big cartoon eye
- [ ] Big floppy ears, pink inside
- [ ] **Light-blue** collar + **gold bell with heart cut-out**
- [ ] Dark hooves, slim legs
- [ ] Small round pom tail
- [ ] Looks soft and gentle (shy-sweet), not bold

**OFF-MODEL ✘**
- [ ] White/grey/yellow wool, smooth (non-curly) body, or looks like a poodle/goat
- [ ] Green/brown eyes
- [ ] Collar not blue; bell missing, not gold, or heart slot missing (a plain bell, a star, etc.)
- [ ] Pink hooves, cat paws, extra limbs
- [ ] Upright pointed ears
- [ ] Realistic sheep proportions (long snout, thick legs)
