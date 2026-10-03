# Design team → Lead inbox
Branch `claude/evie-justin-design` (no PR). Nothing here is canon until you approve. Updated after the **style change** (stylised 3D cartoon, simple fur).

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

## QUESTIONS for the lead (recommendation first)
(Q-01 to Q-09 from v1.0 still stand unless noted: Q-01 collar raspberry; Q-04 lamb scale 1.3×; Q-06 append `.blend`: **now implemented**; Q-03 eyes: **now the default** (toon eye objects + squash blink at T1).)
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
