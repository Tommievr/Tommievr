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
blender -b scenes/ep01.blend --python pipeline/blender/build_shot.py -- pipeline/shots/ep01_s01_001.json
```

## Shot spec
See `shots/example_shot.json`. Each shot declares characters, animation, camera, dialogue audio and duration,
so the same shot can be re-rendered in 16:9 (episode) and 9:16 (short).

Status: **scaffold, untested** (Blender isn't installed in this cloud session). First job tomorrow: run the example shot with a placeholder cube.
