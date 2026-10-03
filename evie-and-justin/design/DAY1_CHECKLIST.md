# Day 1 checklist (Tommie): what to generate first, in order
Style (decided): **stylised 3D cartoon, simple fur.** The reference PNGs are colour/markings reference only. Everything below is copy-paste from the linked files. Tick as you go; write results in `pipeline/meshy/<name>/raw/LOG.md`.

## 0. Prep (15 min)
- [ ] `git pull`; run `tools/hardware_check.sh`, note the output
- [ ] Install **Blender 4.2 LTS or newer**; run the **no-model test** (`design/blender/SETUP.md` section 2): `blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/example_shot_placeholder.json --still 1`. You should get two toon placeholder cats. Time the render.
- [ ] Meshy: log in, **check the plan's commercial licence** and write plan + date in `pipeline/meshy/LICENCE_NOTES.md`

## 1. Evie: the proof (about 1.5 h)  → `design/meshy/characters/evie.md`
- [ ] **A1** restyle the cropped reference (4 variants) → pick the simplest chunky toy look → `evie_front.png`
- [ ] **A2 SIDE** and **THREE QUARTER** from that front image → `evie_side.png`, `evie_34.png`
- [ ] Image checklist (`design/meshy/MESHY_PROMPTS.md` section 4)
- [ ] Meshy **Image to 3D** with the settings table (Quad, 30k, Symmetry On, no pose) → 4 generations → keep 2
- [ ] Download **GLB** → `pipeline/meshy/evie/raw/evie_v1.glb`
- [ ] `blender -b --python pipeline/blender/qa_model.py -- pipeline/meshy/evie/raw/evie_v1.glb --shot pipeline/meshy/evie/raw/qa.png`; work through `design/meshy/QA_AND_FIXES.md`
- [ ] **STOP and send Claude** the 3 input images, the QA render and the QA printout. Decide go / adjust prompts before spending more credits.

## 2. Evie in Blender (about 1 h)
- [ ] Clean + toon materials (`design/blender/SETUP.md` section 3)
- [ ] Rig: `rig_quadruped.py --kind cat --eyes` (`design/blender/RIGGING.md` section 2); nudge bones; weight check
- [ ] Record `idle_breathe` (2 s loop) and a `walk`
- [ ] Render a shot: `"model"` = Evie's rigged `.blend`, preset `medium_single`, golden; then the same with `--aspect 9:16`. **Send screenshots.**

## 3. Justin (about 1 h; same recipe) → `design/meshy/characters/justin.md`
- [ ] Bright even light in the input image (dark fur!). Same steps as Evie, `--iris "#3FB52A"`
- [ ] **Shot with both kittens**: `medium_two`, golden, then `wide_two`

## 4. Backgrounds for Ep.1 (about 1.5 h) → `design/backgrounds/prompt-packs/01-afsluitdijk.md`
- [ ] Sky plate + concept image (golden hour, 16:9 and 9:16)
- [ ] Meshy props: **monument tower**, **sluice tower row**, statue, barge, seagull (5 generations, QA each)
- [ ] Blender: road/guard-rail modules, water planes → `pipeline/scenes/afsluitdijk.blend` (collections `AFSLUITDIJK_SKY/_FAR/_MID/_GROUND/_FG`)
- [ ] Render the **cold-open frame**: `wide_establish`, background `afsluitdijk`, both cats tiny, sky 50 %

## 4b. OPTIONAL, after Evie and Justin: the special drink (Ep.1 lore) → `design/props/SPECIAL_DRINK.md`
- [ ] Meshy prop: **Moondew Blossom** (recommended option A; cup only, glow is a Blender sphere) → QA → toon → `pipeline/props/drink.blend`
- [ ] Render the **discovery moment** with the recipe in `design/blender/FX_GLOW.md` (tags glow + sparkles); try `extreme_close_tag` and the 9:16 version

## 5. Later (not day 1)
- [ ] Cotton and Toffee (needed before Ep.5; same recipe, `--kind lamb`)
- [ ] Rhubarb lip-sync test with one Kokoro line (`design/blender/RIGGING.md` section 5)
- [ ] Sculpt face shape keys (tier T2) once Ep.1 is moving
- [ ] Backgrounds 02-07 (`design/backgrounds/prompt-packs/`)

## If something goes wrong
- Bad generation → `design/meshy/QA_AND_FIXES.md` fix-it table (re-roll cheap; fix the **input image**, not the 3D)
- Still furry/realistic → add "smooth plastic toy figure" to the image prompt and keep the negative prompt
- Colours wrong → Retexture prompt (section D of the character file) or HSV node / texture paint
- Blender script error → paste the printed `[evg]` lines; missing parts are skipped, not fatal
- Anything unclear → add a numbered question to `lead/inbox/design.md`
