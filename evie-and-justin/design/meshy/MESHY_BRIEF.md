# Meshy Brief — 3D character production

## Characters to build (priority order)
1. Evie  2. Justin  3. Cotton (from Ep.4)  4. Toffee  (more later)
References: `../../assets/characters/`

## Input images for Meshy (image-to-3D)
Meshy works best from a clean image: single character, neutral pose, plain background, full body.
Needed per character:
- Front view, **A-pose / neutral standing**, 4 legs visible, tail visible.
- Optional: side and 3/4 views for multi-view input.
The current reference images are in action poses, so first generate **neutral-pose turnaround images** (design team) before sending to Meshy.

## Export & checks
- Export **GLB** (or FBX) with textures. Keep originals in `pipeline/meshy/<name>/raw/`.
- Check: eye colour correct, collar colour correct, tag/bell present, ears intact, no extra limbs, symmetrical face.
- **Rigging:** try Meshy auto-rig for quadrupeds if available; otherwise rig in Blender (simple quadruped armature + shape keys for blink/mouth).
- Needed expressions as shape keys or swappable textures: blink, smile, open mouth (A/E/O/M visemes), surprised, sleepy.

## Fur/wool strategy
Keep fur as texture + normal map, not real hair, so renders stay fast and consistent. Add subtle rim light in Blender for the glow.

## Licence
Confirm Meshy plan gives commercial rights for YouTube monetisation before final assets are published. Record plan and date in `pipeline/meshy/LICENCE_NOTES.md`.

## Folder convention
`pipeline/meshy/<character>/raw/` → `clean/` → `rigged/<name>.blend`
