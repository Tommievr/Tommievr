# Blender setup and workflow (copy-paste)

## 1. Install
1. Blender **4.2 LTS or newer** from blender.org (5.x fine). Open it once, then close.
2. Enable add-ons (Edit → Preferences → Add-ons): **Rigify** (optional), glTF importer is built in.
3. Clone/open the repo. Folder `pipeline/` layout:
```
pipeline/
  meshy/<name>/raw/      # Meshy downloads + LOG.md  (GLB, input images)
  meshy/<name>/clean/    # cleaned .blend (parts separated, materials, scale)
  meshy/<name>/rigged/   # <name>.blend with a collection called <name>
  scenes/<location>.blend# background scenes: collection(s) named <LOCATION>_FG/_GROUND/_MID/_FAR/_SKY
  shots/*.json           # shot specs
  renders/               # outputs (git-ignored)
  blender/               # evg helpers + scripts
```
4. Check the engine works: Blender → Render Properties → Render Engine **EEVEE**. (Toon shading needs EEVEE; *Shader to RGB* does not work in Cycles.)

## 2. First test in 10 minutes (no models needed)
```
blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/example_shot_placeholder.json --still 1 --save-blend test.blend
```
You get `pipeline/renders/test_placeholder_f0001.png` (two toon placeholder cats on a green plane, golden light) and `test.blend` to open and play with. Vertical Short version of the same shot:
```
blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/example_shot_placeholder.json --aspect 9:16 --variant dusk --still 1
```
Look-dev is fast: set `"render": {"samples": 24, "percent": 40}` in the spec. Final: 64 samples, 100 %.
Windows: use the full path to `blender.exe` (`"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" -b --python ...`). If Blender is on a machine without a GPU/display, `-b` still works.

## 3. Import a Meshy GLB and clean it (per character, once)
1. **File → New → General**, delete the default cube/camera/light. Save as `pipeline/meshy/evie/clean/evie.blend`.
2. **File → Import → glTF 2.0 (.glb)** → `pipeline/meshy/evie/raw/evie_v1.glb`.
3. Run the automatic check first (terminal): `blender -b --python pipeline/blender/qa_model.py -- <glb> --shot qa.png`, then work through `design/meshy/QA_AND_FIXES.md`.
4. **Orientation/scale:** model should face **-Y**, stand on z = 0, Z up. Select it → `Ctrl+A` → **All Transforms**. Move/rotate until feet are on the grid and the face looks at the front view (`Numpad 1`). **Object → Set Origin → Origin to 3D Cursor** with the cursor at the feet centre (`Shift+C` then place).
5. **Smooth it:** Object → **Shade Smooth** (or Shade Auto Smooth 40°). Edit mode: `A`, **Mesh → Clean Up → Merge by Distance**. If bumpy: Sculpt mode, **Smooth** brush at 0.5; or Object → Remesh modifier (Voxel 0.004 m) + Shrinkwrap.
6. **Separate parts** you need to animate (Edit mode → select faces → `P` → Selection): `evie_collar`, `evie_tag` (cats) / `cotton_bell` (lambs). Name the body `<name>_body`.
7. **Eyes:** easiest = let the rig script add toon eyes (`--eyes`); first flatten the Meshy eye region to the fur/face colour (Texture Paint, flat brush) or hide it under the new eyes.
8. **Materials:** run the toon conversion: in Blender's Python console (Scripting tab):
```python
import sys; sys.path.insert(0, "/path/to/evie-and-justin/pipeline/blender")
from evg import toon
for o in bpy.context.selected_objects:
    if o.type == "MESH": toon.convert_to_toon(o)
```
(It reuses Meshy's base-colour texture so markings survive.) Gold parts: `o.data.materials[0] = toon.gold_material()`.
9. Scale: **select everything → scale so shoulder height = 0.22 m (cats) / 0.30 m (lambs)**; the shot runner can also rescale with `"height_m"`.
10. **Rig:** `RIGGING.md`. Output: `pipeline/meshy/evie/rigged/evie.blend` with everything inside a collection named `evie`.

## 4. Build backgrounds
Make `pipeline/scenes/<location>.blend` with collections `<LOCATION>_SKY`, `_FAR`, `_MID`, `_GROUND`, `_FG` (uppercase location name; see `design/backgrounds/`). Flat toon materials: `toon.simple_material("name", "#hex", rim_strength=0)`; ground: `threshold=0.2`. Shots reference it with `"background": "<location>"`. Without it you get a green placeholder ground.

## 5. Shot spec (JSON)
```json
{
  "shot_id": "ep01_s01_001", "duration_s": 4.0, "fps": 24, "aspect": "16:9", "variant": "golden",
  "background": "afsluitdijk",
  "characters": [
    {"name": "evie", "model": "pipeline/meshy/evie/rigged/evie.blend", "collection": "evie", "pos": [-0.35,0,0], "rot_z": 15,
     "height_m": 0.22, "anim": "idle_breathe", "expression": "happy", "lipsync": "pipeline/renders/audio/evie_001.json"}
  ],
  "camera": {"preset": "medium_two", "yaw": 0},
  "render": {"samples": 64, "percent": 100},
  "out": "pipeline/renders/ep01_s01_001"
}
```
`model: null` = placeholder. `model` may be `.blend` (recommended: keeps shape keys, actions, constraints) or `.glb`. Camera may also be the legacy `{"pos":[..],"look_at":[..],"lens_mm":45}`. Options: `--still N`, `--aspect 9:16`, `--variant day|golden|dusk`, `--no-render --save-blend file.blend`.
Missing action/shape key/lip-sync file never crashes: it prints a `[evg] note:` and continues (placeholder bob for missing actions).

## 6. Render checklist
- [ ] Engine EEVEE, **Standard** view transform (AgX/Filmic wash out flat toon colours)
- [ ] 64 samples, motion blur off, DOF on
- [ ] 16:9: 1920x1080; 9:16: 1080x1920 (the runner sets both; re-render, do not crop)
- [ ] Output MP4 (H.264) or PNG sequence; audio is added in the edit
- [ ] Time one 1080p frame on Tommie's hardware and write it in `pipeline/README.md`
