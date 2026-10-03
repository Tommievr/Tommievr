# Meshy Prompts, Settings, QA and Rigging Plan (proposed v1.0)

Companion to `MESHY_BRIEF.md` (lead) and `../character-sheets/`. **I could not run any image tool or Meshy from the cloud session: nothing here is tested yet.** Treat prompts as a first draft; log every accepted result (tool, settings, seed) in `pipeline/meshy/<name>/raw/LOG.md`.
Meshy's UI and model names change often: **check option names on the day** (marked ⚠ below).

## 0. Order of work
1. **Evie** front → side → 3/4 (Section 1, check with Section 2).
2. **Justin** front → side → 3/4.
3. Run Meshy on Evie only. Do QA (Section 4). Fix the pipeline before spending credits on the rest.
4. Justin in Meshy. Then Cotton and Toffee (needed before Ep.5, not tomorrow).

## 1. Two-step image generation
**Step A: neutral-pose reference images** with any image generator that accepts reference images (ChatGPT image generation, Gemini image, Midjourney `--cref/--oref`, Flux Kontext, etc.). Upload `assets/characters/evie-and-justin-reference.png` (crop to the one character first, so the model does not mix them) and use the prompt below.
**Step B: Meshy** image-to-3D with the generated front (+ side, back-less) images.

### Master prompt (paste first, then the character block, then the view block)
```
Character turnaround reference sheet photo, single character, full body, neutral standing pose, cartoony 3D
storybook style (Pixar-like soft fur shading), clean readable outline, soft even neutral studio lighting,
no strong shadows, no rim glow, no golden light, plain flat light-grey background (#EDEDED), centered, full
body visible with margin, square 1:1, high detail, consistent proportions. Mouth CLOSED with a tiny relaxed
smile. Eyes open, looking at the camera, symmetrical. Four legs standing straight and separated so all four
paws are clearly visible. No props, no text, no extra characters, no motion blur, no depth of field.
```
### Negative / avoid (for tools with a negative prompt; otherwise add as "Avoid: …")
```
open mouth, teeth, tongue, action pose, running, jumping, sitting, lying down, tail wrapped around body,
legs overlapping, crossed legs, cropped paws, golden hour tint, rim light halo, glowing outline, flyaway
hair strands, long whiskers, photo-realistic cat, realistic proportions, 2D flat drawing, hard black outlines,
background scenery, floor shadow, text, watermark, multiple characters, wide-angle distortion, blur
```

### Character blocks
**Evie**
```
EVIE: a fluffy white kitten with a single black patch on the top-left of her head (seen from the front) over
the base of her left ear, big round BLUE eyes with two highlights, soft pink inner ears, tiny pink nose,
rosy cheeks, a thin RASPBERRY PINK collar (#B3203C) with tiny gold dots and a round GOLD paw-print tag hanging
at the front centre. Long fluffy white tail curling gently upward, away from the body. Warm-white fur (#F5EFE9),
chunky short legs with pale pink toe pads. Chibi proportions: head as wide as the body.
```
**Justin**
```
JUSTIN: a fluffy dark kitten with very dark warm brown-black fur (#2A1A14, soft readable form, not flat black),
big round GREEN eyes with visible white of the eye and two highlights, ears with pink insides and cream-white fuzzy
backs, dark rose nose, pale thin whiskers, a thin plain near-black leather collar with a round GOLD paw-print
tag hanging at the front centre. Short plump fluffy tail curling up over his back. Slightly stockier and fuller
cheeked than a normal kitten, chibi proportions: head as wide as the body. Lit brightly and evenly so the fur form
and the face are clearly visible.
```
**Cotton**
```
COTTON: a cute baby lamb with soft curly CREAM wool (#F7EBD9, scalloped cloud-like outline), a smooth short cream face,
big round BLUE eyes with two highlights, large floppy ears hanging out sideways with pink insides, small pink nose,
a thin LIGHT-BLUE collar (#8FB6DB) with a round gold sleigh bell with a HEART-shaped slot hanging at the front
centre, slim legs with dark brown hooves (#4A332C), a small round wool pom tail. Gentle, shy, sweet look.
```
**Toffee**
```
TOFFEE: a cute baby lamb with soft curly CHESTNUT-BROWN wool (#6A3418), a cream face with a brown wool crown over the
forehead, brown floppy ears hanging out sideways with pink insides, a cream chest blaze and cream lower legs
("socks"), dark hooves (#3A2620), big round GREEN eyes with two highlights, small pink nose, a thin LEAF-GREEN
collar (#4F7F2E) with a round gold sleigh bell with a HEART-shaped slot at the front centre, a small round brown
wool pom tail. Bold, bouncy, mischievous look. Background plain light-grey (#EDEDED) so the brown wool separates.
```

### View blocks (append one)
| View | Block |
|---|---|
| **Front** | `FRONT VIEW: body and head facing the camera straight on, both front paws visible side by side, face symmetric.` |
| **Side** | `SIDE VIEW (profile, facing right): the whole body exactly side-on, head turned to look at the camera, all four legs visible, tail visible. Show the character's LEFT side.` (Evie's patch side) |
| **3/4** | `THREE-QUARTER VIEW: body turned 45 degrees to the camera's left, head turned to look at the camera, all four paws visible.` |
| **Back (optional)** | `BACK VIEW: seen from behind, tail visible, collar visible from behind.` Only if Meshy multi-image supports it ⚠ |

### Workflow tips
- Generate the **front** first. Pick the best. Then give **that image + the character block** as the reference for side and 3/4, so colours and markings stay locked.
- Generate 4 variations per view, choose with the checklist in `../character-sheets/<name>.md` (on-model / off-model).
- Use a short **colour-fix pass** in any image editor if the hex drifts (Evie's collar and the green eyes are the usual drift). Do not "paint over" markings, regenerate instead.
- Save as PNG, 1536 px or larger, `pipeline/meshy/<name>/raw/<name>_front.png` etc.
- Remove the background (any background remover) only if Meshy asks for transparent PNG; otherwise keep the flat light-grey.

## 2. Input image checklist (per image, before uploading to Meshy)
- [ ] Single character, full body, centred, ≥ 10 % margin
- [ ] Mouth closed; eyes open and symmetric
- [ ] Four paws visible and separate; tail clearly visible
- [ ] Neutral, even light, no golden tint, no rim halo, no cast shadow
- [ ] Collar and tag/bell visible, centred, facing camera
- [ ] Colours match the sheet's albedo hexes (within a visible tolerance)
- [ ] Markings correct (Evie: one patch top-left; Toffee: cream socks/chest)
- [ ] No text, no props, no second character

## 3. Meshy 3D step: settings ⚠ (verify names in the UI)
| Setting | Proposed value | Why |
|---|---|---|
| Mode | **Image to 3D** (multi-image if available: front + side + 3/4, up to 4 images) | locks the 3D form |
| Model | newest available "latest" model | best quality |
| Pose / "A/T-pose" option | **off** (these controls are meant for humanoids; the image is already neutral) ⚠ | avoid it forcing a biped pose |
| Symmetry | **on** | symmetric face and body; the only intended asymmetry is Evie's patch, which is a texture |
| Topology | **Quad** if offered, else triangles + retopo in Blender | easier to rig and deform |
| Target polycount | **30,000–50,000** faces | enough for a fur silhouette, light for EEVEE |
| Texture | **on**, PBR maps on (base colour, normal, roughness, metallic) | we need the normal map for fur |
| Texture prompt (if retexture is used) | `soft fluffy fur, cartoony, clean, even colour, no baked lighting, no shadows` | avoid baked golden light |
| Export | **GLB** (textured) + keep the FBX if offered | `pipeline/meshy/<name>/raw/` |
| Seeds | note the seed shown for reproducibility | log in `LOG.md` |
Plan/licence: confirm commercial rights on the plan used and record in `pipeline/meshy/LICENCE_NOTES.md` **before** any asset is published.

### Fallback: text-to-3D prompt (if image-to-3D gives bad geometry)
```
cute chibi kitten, neutral standing pose on four legs, white fluffy fur with one black patch on top-left of head,
big blue eyes, closed mouth, pink collar with gold paw-print tag, stylized cartoon 3D character, clean topology,
PBR, no baked lighting
```
(Swap the colour words per character, use the character blocks above.)

## 4. QA checklist for the resulting 3D model
Open the GLB in Blender (or Meshy viewer), orbit all around, with a **neutral studio light** first, then with the golden rig.

**Identity (use the sheet's on-/off-model list)**
- [ ] Eye colour correct; eyes symmetric; both irises visible
- [ ] Collar colour correct; tag/bell present, correct shape (paw print / heart slot)
- [ ] Markings correct (Evie patch side, Toffee socks)
- [ ] Ears intact, correct shape (cats pointed, lambs floppy)
- [ ] Silhouette passes the "solid black" test from front, side and 3/4
**Geometry**
- [ ] 4 legs, 4 paws, 1 tail, no extra limbs, no fused legs, no floating bits
- [ ] No holes, no non-manifold edges (Blender: Select → All by Trait → Non Manifold)
- [ ] Face symmetric; mouth closed, lips not baked open
- [ ] Legs separated enough to rig (gap between inner legs)
- [ ] Face mesh dense enough around eyes/mouth for shape keys (≥ 1,000 faces on the head)
- [ ] Scale/orientation: Z up, facing -Y, origin at ground between the paws, applied scale
**Texture**
- [ ] No baked shadows or golden tint; albedo matches the hex table
- [ ] Normal map reads as soft fur (not noise); no visible seams on the face
- [ ] Collar/tag texture sharp enough at `close_up` (check at 85 mm, 1 m)
- [ ] Gold tag/bell: metallic 1.0 can be applied (separate material or mask)
**Render test**
- [ ] Render the 3 camera presets `wide_two`, `medium_single`, `close_up` with `RIG_Golden`: rim glow visible on fur edges, face readable (Justin!)
- [ ] 1080 p frame renders in < 30 s on Tommie's hardware (EEVEE); record the time
Result goes in `pipeline/meshy/<name>/QA.md`: PASS / FIX (list) / REJECT (regenerate).

## 5. Rigging plan for Blender
Goal: a rig that Python (`build_shot.py`) can drive by **named actions + shape keys**, built once per body plan (kitten, lamb).

### 5.1 Clean-up (per model)
1. Import GLB. Set scale/orientation (see QA). Name objects: `<name>_body`, `<name>_eyes`, `<name>_collar`, `<name>_tag` (or `_bell`).
2. **Separate parts:** collar, tag/bell, eyes, tail (optional), as separate objects (Meshy output is usually one mesh. Separate by selecting loops/faces → `P`). Tag/bell must be separate so they can swing.
3. **Eyes:** if Meshy baked the eyes into the head texture, **replace them** with Blender eyes (UV sphere ×2: cornea + iris/pupil texture using the iris hexes from the sheet), placed in the sockets, so blinking and eye-look work. This is the recommended path (more reliable than sculpting open/close on a baked eye).
4. **Mouth interior:** add small meshes (tongue, teeth for cats) hidden unless the mouth is open; or paint-in as texture swap in tier 1 below.
5. **Retopo** only if Meshy topology is unusable: Meshy quad option → Blender voxel remesh (0.004 m) → Shrinkwrap on the original, bake normals. Skip when possible.
6. Whiskers: thin curves (cats), added in Blender, 8 per side; not baked.

### 5.2 Armature
Use **Rigify** as a base (⚠ verify in your Blender version): `Add → Armature → Animals → Cat` for the kittens, `Basic Quadruped` for the lambs. Fit to the mesh, generate, then add custom bones. If Rigify is awkward, hand-make the simple armature below.

```
root
└─ pelvis
   ├─ spine.01 → spine.02 → chest
   │    ├─ shoulder.L/R → upper_arm.L/R → forearm.L/R → paw_front.L/R (+toe)
   │    └─ neck.01 → neck.02 → head
   │          ├─ jaw
   │          ├─ ear.L.01 → ear.L.02 (cats: 2 bones; lambs: 3 bones for floppy)  ear.R.*
   │          ├─ eye.L / eye.R   (aim at "look_target" with Damped Track)
   │          └─ whisker.L/R (optional)
   ├─ thigh.L/R → shin.L/R → foot.L/R → paw_hind.L/R (+toe)
   └─ tail.01 → tail.02 → tail.03 → tail.04 → tail.05
collar_root (child of neck.02) → tag.01 / bell.01 (+ tag.02 chain, swing via damped/copy rotation)
```
Controls: IK on all four legs with pole targets and foot-roll, `look_target` empty, `body_root` ctrl, tail FK chain with a "curl" custom property, ear FK, head FK/IK (neck follows).
Weights: **Automatic weights** then paint fixes at shoulders, hips, neck, ears, tail root. Lock the collar/tag/bell as separate objects parented by a bone (rigid), no weight painting.

### 5.3 Animation set (actions, named for `build_shot.py`)
`idle_breathe` (loop), `walk` (loop), `run` (loop), `hop`, `look_around`, `point_at` (paw), `sit`, `sleep_curl`, `happy_bounce`, `tail_wag`. Lambs add `skip`, `ear_flop`, `bell_swing`. Keep each as a separate Blender **Action** in the .blend and push to NLA; the shot JSON references the action name.

### 5.4 Shape keys (on the head/face mesh)
- **Blink:** `blink_L`, `blink_R` (needs an eyelid mesh or lid-loop deform; if eyes are replaced, use a lid shell that rotates, driven by one slider).
- **Expressions:** `expr_happy`, `expr_curious`, `expr_surprised`, `expr_scared_but_brave`, `expr_sleepy`, `expr_laughing` (eyes/brows/cheeks/ears; mouth part separate).
- **Visemes:** `vis_A … vis_H` (+`vis_X` as rest/zero). See `../character-sheets/COMMON.md` section 2.
- **Misc:** `brow_L_up`, `brow_R_up`, `cheek_puff`, `nose_scrunch`.
- Drivers: one Custom Property per key on the head bone (`pose.bones["head"]["vis_D"]`) so the shot script can keyframe by name.
Naming = `COMMON.md` names, identical across characters, so one lip-sync script drives all four.

### 5.5 Tiers (so Ep.1 is not blocked by perfect facial animation)
| Tier | What | When |
|---|---|---|
| **T0 placeholder** | untouched Meshy GLB + `add_walk_bob` (already in `build_shot.py`) | day one, to test the pipeline |
| **T1 minimum viable (Ep.1)** | simple armature, idle/walk/hop; jaw bone open/close from audio amplitude; mouth/eye **texture swap** (X, A, D, F + blink) | first episode |
| **T2 full** | all shape keys + Rhubarb visemes + expressions | from Ep.2 on |
| **T3 polish** | physics bits: tail secondary motion, ear flop, bell swing, fur shader tuning | later |
Fastest cheap look: stills + parallax backgrounds + mouth swap (consistent with the scriptwriters' shot notes for Ep.1).

### 5.6 Deliverables per character
`pipeline/meshy/<name>/raw/` (GLB, input images, LOG.md) → `clean/` (cleaned .blend) → `rigged/<name>.blend` (+ exported `<name>.glb` for `build_shot.py`) + `QA.md`.
Note: the example shot uses `.glb` paths: **exported GLB drops shape-key drivers and some constraints; prefer to append the rigged collection from the .blend** in `build_shot.py` (see Q-06 in `../../lead/inbox/design.md`).
