# Rigging plan: quadruped armature, blink and mouth shape keys
Code: `pipeline/blender/rig_quadruped.py` (armature + binding + eyes), `evg/characters.py` (expressions, blink, lip-sync by name). Tested on placeholders; real Meshy bodies will need bone nudging.

## 1. Naming contract (identical for all four characters)
- Armature object `<name>_rig`; everything in one collection `<name>`; body mesh `<name>_body`; separate `<name>_collar`, `<name>_tag` (cats) / `<name>_bell` (lambs).
- Bones: `root, pelvis, spine.01, chest, neck.01, head, jaw, ear.L/R.01-03, upper_arm.L/R, forearm.L/R, paw_front.L/R, thigh.L/R, shin.L/R, paw_hind.L/R, ik_paw_front/hind.L/R, tail.01-05, collar_root, tag.01, look_target`. `.L` = the character's left = **+X**; characters face **-Y**.
- Shape keys on the body/head mesh: `expr_happy expr_curious expr_surprised expr_scared_but_brave expr_sleepy expr_laughing`, `vis_X vis_A ... vis_H`, `blink_L blink_R`.
- Actions: `idle_breathe walk run hop look_around point_at sit sleep_curl happy_bounce tail_wag` (+ lambs: `skip ear_flop bell_swing`).
The shot script finds things only by these names, so a missing one is skipped with a note, never a crash.

## 2. Build the rig (10 minutes per character)
1. Cleaned model in `pipeline/meshy/<name>/clean/<name>.blend` (`SETUP.md` section 3): body joined into `<name>_body` (head included), collar/tag/bell separate, feet on z=0, facing -Y.
2. Run:
```
blender pipeline/meshy/evie/clean/evie.blend --python pipeline/blender/rig_quadruped.py -- \
  --kind cat --mesh evie_body --collar evie_collar --tag evie_tag --eyes --iris "#1E7FD6" --out pipeline/meshy/evie/rigged/evie.blend
```
(`--kind lamb` for Cotton/Toffee: 3-bone floppy ears, pom tail; iris `#1E7FD6` Cotton, `#5CC236` Toffee, `#3FB52A` Justin. Omit `--eyes` to keep Meshy's eyes. Open without `-b` so you can look afterwards.)
3. It builds ~35 bones from the bounding box, parents the body with **automatic weights**, parents collar/tag to bones, adds leg IK and two toon eyes on the head bone. Bone positions are a first guess:
4. **Nudge bones** (select the armature → Tab into Edit mode → side view `Numpad 3`, front `Numpad 1`): knees/elbows/hips/neck/ears/tail root into the joints. Then re-bind: select body, `Ctrl+click` armature, `Ctrl+P` → **With Automatic Weights**.
5. **Weight check:** Pose mode → rotate `head`, `ear.L.01`, `tail.01`, `thigh.L`; fix with Weight Paint (Smooth). Collar/tag/eyes are rigid (bone parents), no weights.
6. Make test poses → record them as Actions (`idle_breathe` first: chest/head up-down 1 cm, 2 s loop; then `walk`).
Rigify alternative: Add → Armature → Animals → **Cat** (kittens) / Basic Quadruped (lambs) if you prefer a full control rig (more work, better IK). The contract names above must still exist (rename or add helper bones).

## 3. Eyes and blinking
- Meshy eyes are painted into the texture, so **replace them**: `--eyes` adds, per side, white + iris + pupil + shine objects (toon, no shadow), parented to `head`. Place them (Move) on the face; keep eye size **big** (character sheet).
- **Blink (tier T1):** `evg.characters.blink_track` squashes the eye objects in Z (works with no shape keys). Better (T2): eyelid shells with `blink_L/R` shape keys; the same function uses those keys when they exist.
- **Look:** later, `eye.L/R` Damped Track to `look_target`. Keep the pupils centred in `neutral`.

## 4. Face shape keys (T2, sculpted in Blender, 30-60 min per character because the face is simple)
Select the body, Object Data → Shape Keys → `+` (Basis first). Make **each key by moving the mouth/brow/lid vertices** (Sculpt: Grab, or Edit Mode + proportional edit `O`). Mouth = simple shapes, so each viseme is a few vertex moves.
| Group | Keys | Notes |
|---|---|---|
| Blink | `blink_L`, `blink_R` | lids close fully |
| Expressions | `expr_happy ... expr_laughing` | eyes/brows/cheeks/ears only, mouth part is separate, see `character-sheets/COMMON.md` |
| Visemes | `vis_X` (rest) `vis_A ... vis_H` | A closed; B teeth wide; C medium; D widest; E rounded; F small round; G upper teeth on lip; H tongue up |
Minimum for Ep.1 (T1): `jaw` bone open/close from audio amplitude + mouth **texture/mesh swap** (X, A, D, F) + eye-squash blink. Add keys over time; the shot script picks them up automatically.

## 5. Lip-sync (audio → mouth)
1. Kokoro (or any TTS) → WAV per line.
2. **Rhubarb Lip Sync** (free, open source; ⚠ verify licence and CLI on the day): `rhubarb -f json -o line.json line.wav` (give it the transcript with `-d` for better results).
3. In the shot spec: `"lipsync": "pipeline/renders/audio/line.json"` on that character. `build_shot.py` calls `characters.read_rhubarb` + `apply_lipsync`, keyframing `vis_*` by name (TSV output also works).
4. Without `vis_*` keys: skipped with a note (jaw tier is manual for now).

## 5b. Tag and bell (the safety signal needs them)
Cats: delete Meshy's tag; build `fx.make_tag_disc("<name>", location, radius=0.012, parent=<rig>, parent_bone="tag.01")` (plain gold disc + `<name>_tag_face` anchor). The paw symbol, ✓/✕ glyphs and rings are created by `fx.tag_state` (`FX_GLOW.md` section 8). Lambs: keep the bell as a separate object named `<name>_bell` on `tag.01` (heart slot visible); its glow is `fx.bell_glow` (section 9, Ep.7 spoiler).

## 6. Expressions and animation from the shot spec
`"expression": "happy"` sets `expr_happy` (others zero). Animate over time from Python: `characters.apply_expression(root, "surprised", 1.0, frame=48)` (keyframes). Actions: `"anim": "idle_breathe"` assigns the Action to the armature; missing = placeholder bob.
Tail wag, ear flop, bell swing: secondary motion: add Damped Track/Copy Rotation constraints on `tail.0n`, `ear.*.0n`, `tag.01` later (T3). Bell sound is triggered by the audio team, not by Blender.

## 7. Tiers
| Tier | What | When |
|---|---|---|
| T0 | Meshy GLB + placeholder bob (`build_shot.py` does it by itself) | Day 1 |
| T1 | rig script + idle/walk/hop actions + eye-squash blink + jaw/mouth swap | Ep.1 |
| T2 | sculpted `expr_*`, `vis_*`, `blink_*` + Rhubarb | from Ep.2 |
| T3 | secondary motion, cloth-free physics tricks, polish | later |

## 8. Deliverables per character
`pipeline/meshy/<name>/rigged/<name>.blend` (collection `<name>`, actions, shape keys) + `QA.md` + one test render (`medium_single`, `close_up`, 9:16).
Append from `.blend`, not GLB: GLB keeps shape keys as morph targets but loses actions/IK constraints in many setups.
