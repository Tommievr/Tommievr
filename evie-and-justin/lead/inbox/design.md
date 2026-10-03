# Design team → Lead inbox
Branch `claude/evie-justin-design` (no PR). Updated after the lead's answers (Q-10 to Q-14 + earlier defaults accepted) and the **special drink** request.

## Latest (round 4): lead answers Q-15..17 applied
- **Q-15 locked:** Moondew Blossom; `design/props/SPECIAL_DRINK.md` marked approved (origin: found by the cats).
- **Green/red paw tag (Q-16 replaced)** → `design/blender/FX_GLOW.md` section 8 + `evg/fx.py` `tag_state` (`safe` / `unsafe` / `off`). **Tested** (render `design/blender/example_tag_states.png`). Colours: **SAFE mint-aqua `#4DFFC4`, UNSAFE deep red `#D81B2A`** (colour-blind check by CVD simulation: deuteranopia ΔE 52, protanopia 58; plain green/red would be ΔE 9). **Non-colour cues, always all together:** white **check mark ✓ vs X ✕** on the paw, **solid vs dashed rotating ring**, **slow smooth pulse vs fast hard 3-flash pulse**, soft light, captions. **Sound table for audio** (soft rising chime vs low hum + 3 low bonks; calm, never a siren) is in section 8.3.
- **How the tag is built so it can switch state** (Meshy/Blender note): Meshy's baked paw can't change, so each tag is rebuilt as a plain gold disc + separate paw symbol (`fx.make_tag_disc`); documented in FX_GLOW 8.4, RIGGING 5b, QA_AND_FIXES. **Green/red paw sections added to the Evie and Justin sheets.**
- **Q-17 applied:** lambs get the drink in **Ep.7**: `fx.bell_glow` (lilac/gold bell swell, 3 lilac rings, lilac+gold sparkles; render `example_bell_glow.png`; recipe FX_GLOW section 9). **Spoiler guard:** shot specs can carry `"spoiler": "ep07"`; `build_shot.py` warns, loudly for 9:16 Shorts. Bell sections added to Cotton/Toffee sheets.
- Day 1 checklist updated (tag discs, greyscale check of the safety signal, Ep.7 bell test as later/spoiler).
- Fixed while testing: tag shots need focus on the tag and f/22 (`extreme_close_tag`), glow strengths ≤ ~1.7 so mint/red don't clip to cyan/white, bell ring parented under a non-uniformly scaled bell shrank to invisible (now constraint-follow).
- **New questions:** **Q-18** safety-signal timing in the edit: (a) hold the tag close-up ≥ 1.5 s with caption "[soft chime]/[low hum]" every time *(recommended)*; (b) shorter, sound only; (c) icon-only HUD overlay instead of tag glow. **Q-19** do the cats' tags go green/red in Shorts too (9:16 framing: tag close-up needed): (a) yes, always with the close-up *(recommended)*; (b) only in episodes. **Q-20** lamb birthday visual (writers/lead): flower crown + lilac bell glow *(suggested)*, cake, or just music.

## Round 3 (kept for reference)
- **Approved v1.1 marked** in `design/STYLE_GUIDE.md` and `design/character-sheets/` (design files only).
- **Special drink designed** → `design/props/SPECIAL_DRINK.md`: 3 options, **recommended A: "Moondew Blossom"** (pale-lilac flower cup holding a floating glowing lilac droplet with a gold star: no bottle, so the least like alcohol/medicine). B Star Acorn Cup, C Dewdrop Flask (closest to a potion bottle: not recommended). Colours: glow `#B9A2FF`, sparkles `#FFE08A`. Safety rules, Meshy prompts (≤600 chars, cup only; glow is a Blender sphere) and negatives included.
- **Glow/sparkle recipe + paw-tag discovery moment** → `design/blender/FX_GLOW.md` + code `pipeline/blender/evg/fx.py` (`"fx"` list in the shot JSON: `drink`, `tag_glow`, `sparkles`). **Tested headless**: tags pulse gold, blossom lights the ground, 4-point sparkle burst; render `design/blender/example_discovery.png`. Bloom = compositor Glare (manual, 2 min).
- **Day 1 checklist**: drink added as optional section 4b, after Evie and Justin.
- Found/fixed while testing: emission > ~2.5 clips to white under Standard view (kept glow strengths low), prop child offsets double-applied (fixed).

## Open questions for lead/writers (drink)
1. **Q-15** Drink option: (a) A Moondew Blossom *(recommended)*; (b) B Star Acorn Cup; (c) C Dewdrop Flask (needs the safety rules strictly).
2. **Q-16** Script handling: (a) kittens discover, tag glow, taste one drop in-story with a light "only works in stories" beat *(recommended, kid-safe)*; (b) discovery only, never tasted on screen; (c) full drinking scene (writers must keep it clearly fantasy).
3. **Q-17** Do Cotton and Toffee (join Ep.5) get affected by the drink (bells glow too)? (a) decide later, the code already handles bells *(recommended)*; (b) yes, they stay lambs forever; (c) no.

## Earlier status (style change)

## Status
| # | Work item | Status | Where |
|---|---|---|---|
| 1 | **Prompt packs for Tommie** (Meshy, 4 characters): image prompts (restyle ref + front/side/3/4/back), negatives, image-to-3D + text-to-3D settings, retexture prompt, step-by-step "what to click" | ✅ ready, **untested** (no Meshy/image tool in cloud) | `design/meshy/` (`MESHY_PROMPTS.md`, `characters/*.md`) |
| 2 | QA checklist + fix-it guide for bad generations | ✅ | `design/meshy/QA_AND_FIXES.md` |
| 3 | Blender: setup, GLB import/clean, toon shading recipe, light rig, camera presets 16:9 + 9:16, rigging plan | ✅ docs + code **tested headless** (bpy 5.0.1) on toon placeholders: builds, lights, rigs, renders stills 16:9/9:16, PNG sequence | `design/blender/`, `pipeline/blender/` (`evg/`, `build_shot.py`, `rig_quadruped.py`, `qa_model.py`) |
| 4 | Background + prop prompt packs ×7 (sky/far/concept prompts day/golden/dusk, Meshy prop prompts, hand-build list) | ✅ untested prompts | `design/backgrounds/prompt-packs/` |
| 5 | **Day 1 checklist** | ✅ one page | `design/DAY1_CHECKLIST.md` |
| 6 | Style guide v1.1, character sheets, background briefs re-done for the new style; references now "colour/markings only" | ✅ proposed – awaiting your approval | `design/STYLE_GUIDE.md`, `character-sheets/`, `backgrounds/` |
| 7 | Branding (logo, banner, thumbnail, end card, lower third, title card) + SVG mockups | ✅ (flat cartoon heads already fit the new style) | `design/BRANDING.md` |
| 8 | Real 3D models / generated images | ❌ not produced, not claimed | needs Tommie's hardware |

What the code does today (proven by rendering): `build_shot.py` takes a JSON shot, builds toon placeholder characters (or loads rigged `.blend`/`.glb`), background (placeholder ground until `scenes/<loc>.blend` exists), golden/day/dusk light rig with light linking, camera preset, expression, blink, Rhubarb lip-sync by shape-key name; `--aspect 9:16` re-renders the same shot vertical. See `design/blender/example_*.png`.
Tested-and-fixed along the way: AgX washes out flat toon colours → **Standard** view transform; world light must be dimmed for lighting so toon shadows show; realistic f/2.8 close-ups blur half a kitten's face → high f-stops.

## ANSWERED by lead: Q-01, Q-04, Q-05, Q-07, Q-10, Q-11 (a), Q-12 (a), Q-13 (a), Q-14 (a) all accepted
(Original list kept for reference. Q-01 to Q-09 from v1.0 still stand unless noted: Q-01 collar raspberry; Q-04 lamb scale 1.3×; Q-06 append `.blend`: **now implemented**; Q-03 eyes: **now the default** (toon eye objects + squash blink at T1).)
1. **Q-10 Character colours: cleaner and brighter than the reference.** (a) Use the new base hexes: Justin plum-black `#352B3D` instead of true black (a toon shadow step can't show on black), Toffee brighter chestnut `#9C4A1C`, collars/eyes more saturated *(recommended)*; (b) keep the reference's darker, dull values; (c) pure black Justin with strong rim only.
2. **Q-11 Lamb wool.** (a) 12-20 big rounded cloud clumps, smooth *(recommended: reads as wool, rigs and renders cleanly)*; (b) fully smooth "toy lamb" with painted wool pattern; (c) small curls (risks the look Tommie dislikes).
3. **Q-12 Render look.** (a) EEVEE + emission-based toon shader, Standard view, rim lights *(recommended, tested)*; (b) EEVEE with Principled BSDF and a toon-ish ramp (more realistic light response); (c) Cycles (slow, not toon).
4. **Q-13 If Meshy bodies come out messy.** (a) re-roll 4× + fix the input image, then fall back to text-to-3D, then hand-built chunky bodies in Blender (Meshy for heads only) *(recommended)*; (b) always hand-build bodies; (c) keep re-rolling.
5. **Q-14 Rig depth for Ep.1.** (a) T1: auto-weighted rig, toon eyes with squash blink, jaw + mouth swap, idle/walk/hop *(recommended)*; (b) T2 from the start (sculpted expressions + all 9 visemes, +1-2 h per character); (c) no rig, bob only for Ep.1.
6. **Q-05** (approve per-episode palette `STYLE_GUIDE` 3.3) *recommended: approve as is.* **Q-07** logo: keep badge + wordmark *(recommended)*.

## Notes for scriptwriters/lead (unchanged)
Ep.1 research says monument/statue "at Breezanddijk"; sources place the Dudok tower and Lely statue between Breezanddijk and Den Oever (verify). Stevin/Lorentz lock names, Schokland shoreline poles, Wadden route poles, Delta Works colours, heather bloom timing are ⚠ unverified (marked in the briefs). Kittens never stand on the hunebed capstones.

## Blockers
- No Meshy, image generator or display in the cloud session: no images/models; all Meshy/image prompts are untested (ready to paste).
- Blender 4.2 LTS vs 5.x on Tommie's machine unknown; code detects the EEVEE engine name for both. FFmpeg export is used when available, else a PNG sequence.
- Rhubarb lip-sync and Meshy UI names/limits (⚠) are from memory, to verify on the day.

## Needed from Tommie (Day 1; see `design/DAY1_CHECKLIST.md`)
1. Run the no-model test render; send the time per frame and Blender version; `hardware_check.sh` output.
2. Evie only first: restyle reference → front/side/3/4 images → Meshy image-to-3D → QA script → **send images + QA render + printout before doing Justin**.
3. Record the Meshy plan and licence wording in `pipeline/meshy/LICENCE_NOTES.md`.
