# Pipeline: Meshy → Blender → Python

```
pipeline/
  meshy/    # raw/clean/rigged character files (large files: use Git LFS or keep out of git)
  blender/  # python scripts run by Blender
  shots/    # JSON shot specs (one per shot)
  renders/  # output frames/videos (git-ignored)
```

## Run (headless)
```
blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/ep01_s01_001.json
```

## Shot spec
See `shots/example_shot.json`. Each shot declares characters, animation, camera, dialogue audio and duration,
so the same shot can be re-rendered in 16:9 (episode) and 9:16 (short).

Status (design team, v1.1): the helper package **`blender/evg/`** (toon shading, light rig, camera presets 16:9 + 9:16, characters, expressions, lip-sync), `build_shot.py`, `rig_quadruped.py` and `qa_model.py` were **tested headless with Blender's Python module (bpy 5.0.1)** on toon placeholder characters: build, light, rig, render stills in 16:9 and 9:16. Real Meshy models and real backgrounds are untested.
First job: `blender -b --python pipeline/blender/build_shot.py -- pipeline/shots/example_shot_placeholder.json --still 1` (needs no models). Docs: `design/blender/`.
Model format: shots append **rigged `.blend`** files (collection `<name>`), `.glb` also works. Missing models/backgrounds/actions fall back to placeholders with a printed note.
