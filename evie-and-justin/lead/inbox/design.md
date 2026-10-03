# Design team → Lead inbox
Updated by the design team session. Branch `claude/evie-justin-design` (no PR). Nothing here is canon until you approve.

## Status
| # | Work item | Status | File(s) |
|---|---|---|---|
| 1 | Style guide v1.0 (palette, Blender light rig, cameras, safe areas, shape language) | ✅ drafted, **proposed – awaiting approval** | `design/STYLE_GUIDE.md` |
| 2 | Character sheets (Evie, Justin, Cotton, Toffee + COMMON + template) | ✅ drafted, hexes sampled from the reference PNGs | `design/character-sheets/` |
| 3 | Meshy prompts, settings, QA checklist, rigging plan | ✅ drafted, **untested** (no image tool / Meshy access in the cloud) | `design/meshy/MESHY_PROMPTS.md` |
| 4 | 7 background briefs (web-checked, ⚠ = unverified) | ✅ drafted | `design/backgrounds/` |
| 5 | Branding (logo, banner, thumbnail, end card, lower third, title card) + SVG mockups | ✅ drafted, SVGs are layout mockups only | `design/BRANDING.md`, `design/branding/` |
| 6 | 3D models | ❌ not produced and not claimed; needs Tommie's hardware/Meshy | — |

## QUESTIONS for the lead (recommendation first)
1. **Q-01 Evie's collar colour.** The reference is a deep **raspberry** (sampled `#AA1E37`), not pastel pink. Options: (a) keep raspberry `#B3203C` and update the word to "raspberry-pink" in CHARACTERS.md *(recommended: matches the art, reads well on white fur)*; (b) lighten to true pink `#E88FB4`; (c) regenerate reference art.
2. **Q-02 Which input images first?** (a) Evie then Justin front view, test one full Meshy round on Evie *(recommended)*; (b) all four at once; (c) both cats' front+side+3/4 before any Meshy run.
3. **Q-03 Eyes and mouth in the 3D model.** (a) Replace the baked eyes with Blender eyes + eyelid shape keys, mouth via jaw bone and texture swap in Ep.1, full visemes from Ep.2 *(recommended: fastest to a working Ep.1)*; (b) full shape keys from the start; (c) keep Meshy faces as is (no blinking).
4. **Q-04 Lamb scale.** (a) lambs 1.3× kitten size, shoulder 0.30 m *(recommended: matches how they look in the reference)*; (b) same size as kittens; (c) lambs much bigger (1.6×).
5. **Q-05 Lock the palette per episode?** (a) approve STYLE_GUIDE 2.2 as is *(recommended)*; (b) approve everything except named episodes; (c) revisit after the first Blender test renders.
6. **Q-06 Model format in `build_shot.py`.** (a) append the rigged collection from `.blend` files instead of importing GLB *(recommended: keeps shape-key drivers and constraints; the current example shot uses `.glb`)*; (b) export GLB and re-add drivers in code; (c) FBX.
7. **Q-07 Logo style.** (a) round badge avatar + wordmark, as mocked *(recommended)*; (b) wordmark only; (c) include the lambs from the start.
8. **Q-08 Fonts.** (a) Fredoka + Nunito (free, OFL) *(recommended)*; (b) a paid/custom font; (c) hand-lettered title.
9. **Q-09 Schokland "shoreline poles/markers".** I couldn't confirm that real markers outline the old shore (only the retaining wall at Middelbuurt, lighthouse foundations and ruins). (a) keep a stylised pole line as a **design device** and have the writers verify before claiming it's real *(recommended)*; (b) drop it; (c) writers check on-site info first.

## Notes for the script writers / lead (found while researching)
- Ep.1 research table says the monument/statue is "at Breezanddijk". Sources place the Dudok monument tower and Lely statue **between Breezanddijk and Den Oever** (Vlietermonument area). Please verify.
- Stevin locks (Den Oever) / Lorentz locks (Kornwerderzand) naming: from memory, not confirmed by my searches.
- Unconfirmed items are marked ⚠ in each background brief (route poles on the Wadden mudflats, colour of the Delta Works piers/gates, heather bloom timing).
- Hunebedden: avoid kittens standing on the capstones (protected site, Bible rule 3).

## Blockers
- No image generator, Meshy or Blender in this cloud session, so no images or models were produced. All prompts are untested.
- Reference art has a transparent background and warm light: colours are sampled **lit**; albedo hexes are estimates until compared with a Meshy output.

## Needed from Tommie tomorrow (his hardware)
1. Run `tools/hardware_check.sh` (already requested by lead) and note the Blender version.
2. Crop **Evie** from the reference and generate her **neutral front view** with the master prompt + Evie block (`design/meshy/MESHY_PROMPTS.md`), 4 variants; pick one with the on-/off-model checklist. Then **side** and **3/4**.
3. Run **Evie only** through Meshy image-to-3D with the settings table; **record plan/licence date** in `pipeline/meshy/LICENCE_NOTES.md`; download GLB to `pipeline/meshy/evie/raw/`.
4. Open in Blender, run the QA checklist (section 4), render `wide_two` / `medium_single` / `close_up` with the lighting rig values from STYLE_GUIDE 3 and send screenshots. Time one 1080p EEVEE frame.
5. Then Justin, with the brighter-light note on his sheet.
