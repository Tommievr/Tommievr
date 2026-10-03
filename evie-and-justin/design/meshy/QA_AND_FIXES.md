# QA checklist and fix-it guide for Meshy models (v1.1)
Run `blender -b --python pipeline/blender/qa_model.py -- <model.glb> --shot qa.png` first (prints counts, loose parts, non-manifold edges, scale, shape keys; renders a toon preview). Then check by eye in Blender, orbiting all around. Record the result in `pipeline/meshy/<name>/QA.md` (PASS / FIX list / REJECT).

## 1. Checklist
**Style (new)**
- [ ] Reads as a **simple, chunky, smooth toy** (no fur strands, no fuzzy halo, no hair-card mess, no photoreal detail)
- [ ] Lambs: wool = **a few big clumps**, not curls
**Identity (character sheet checklist)**
- [ ] Eye colour right, eyes big and symmetric · [ ] collar colour right · [ ] tag/bell present, right shape (paw print / heart slot)
- [ ] Markings right (Evie: one patch top-left of head; Toffee: cream socks + chest)
- [ ] Ears right (cats rounded upright; lambs floppy sideways) · [ ] silhouette passes the solid-black test (front, side, 3/4)
**Geometry**
- [ ] Exactly 4 legs, 4 paws, 1 tail, 2 ears; no floating bits, no fused legs
- [ ] No holes; few non-manifold edges; <= ~12 loose parts (separate eyes/collar/tag are fine)
- [ ] Mouth **closed**; face symmetric; legs separated enough to rig
- [ ] 15k-50k triangles
- [ ] Origin at the feet, facing -Y, Z up, scale sensible (shoulder 0.22 m cat / 0.30 m lamb after scaling)
**Texture**
- [ ] Flat colours matching the base hexes; no baked shadow/golden tint; no noisy texture
- [ ] No visible seams across the face
**Render test**
- [ ] Looks right with the toon material (`../blender/SHADING.md`) + rig `golden` in `medium_single` and `close_up`
- [ ] Face readable (Justin: eyes, ear backs, tag visible on dark fur)

## 2. Fix-it table (problem → what to do, cheapest first)
| Problem | Likely cause | Fix |
|---|---|---|
| Looks furry/realistic, noisy surface | prompt/image had fur words or fur detail | re-make the input image with "smooth plastic toy"; add the negative prompt; or in Blender: Sculpt mode **Smooth** brush / **Remesh (Voxel, 0.003-0.005 m)** then Shrinkwrap to a smooth copy |
| Fuzzy halo / floating strands as geometry | halo in the input image | delete loose parts (Edit mode: Select Linked → Delete), or regenerate from a cleaner image (crop out the halo, pure plain background) |
| 5 legs / 3 ears / 2 tails | generation error | re-roll (new seed); if it is one small extra, **delete the extra geometry** (select linked, delete) and fill the hole; do not try to fix badly broken ones |
| Legs merged into the belly or each other | legs overlapped in the input | re-make the input image with legs apart (prompt says "separated"); or Blender: Sculpt **Grab/Snake Hook** to separate; or accept and rig with extra weight painting |
| Tail glued to the body | tail hugging the body in the image | re-make the image with the tail raised and clear of the body |
| Mouth open / teeth baked in | open mouth in the image | re-make the image with a closed mouth; Blender: sculpt/Smooth the mouth shut, add mouth shapes as separate meshes |
| Eyes baked flat in the texture | normal for image-to-3D | **replace the eyes**: delete the eye area texture detail, add eye objects (`RIGGING.md` section 3, helper `evg.characters`), or paint the eye region flat colour |
| Colours wrong (e.g. collar green instead of pink) | texture drift | **Retexture** with section D; or in Blender fix the **material colour/HSV**: Shading workspace → Hue/Saturation node after the image texture (Hue 0.5 = no change) for global shifts; **Texture Paint** (flat brush, exact hex) for a part (collar, patch); or split the collar to its own material (Edit mode: select collar faces, `Ctrl+L`, `P` Separate, new material with the hex) |
| Baked shadows / golden tint in the texture | light in the image | de-light option in Meshy; or flatten: HSV node value up + saturation up; or repaint flat; re-make the input image with neutral light |
| Black fur is a flat black blob (Justin) | input too dark | re-make the image brighter, even light, base `#352B3D`; or in Blender set the material base colour to `#352B3D` (flat) |
| Heart slot / paw print missing on tag/bell | too small for Meshy | model the tag and bell yourself in Blender (a disc + paw/heart cut) and delete Meshy's; they are separate objects anyway |
| Model is huge/tiny or sideways or below the floor | export scale | select all → apply scale; `evg` `height_m` rescales on load; Rotate/Move, set origin to the feet (`Object → Set Origin → Origin to 3D Cursor` with the cursor at the feet) |
| Too many polygons (>80k) | high setting or noisy mesh | Decimate modifier (Collapse 0.4) or Voxel remesh + shrinkwrap; or Meshy remesh at 30k |
| Holes / non-manifold | generation artefact | Edit mode: Select → All by Trait → Non Manifold; `Mesh → Clean Up → Fill Holes`; Merge by Distance 0.0005 |
| Asymmetric face by accident | generation | Edit mode **Mirror modifier** workflow: delete the worse half, Mirror (X) with Clipping; Evie's patch is a texture so it is unaffected |
| Ears wrong (pointed on lambs / floppy on cats) | prompt drift | re-roll with the ear sentence emphasised; or sculpt; or model ears as separate meshes in Blender (they are rigged separately anyway) |
| Lamb wool is curly mush | "wool" interpreted as curls | prompt "big simple rounded cloud clumps, smooth, no curls"; negative "curly wool, curls"; or Smooth + Voxel remesh in Blender |
| Texture too blurry at close-up | low resolution | not needed for flat colours: replace the texture by flat materials / vertex colours; keep only the markings texture |

## 3. When to give up and rebuild
If after 4 re-rolls + a different input image the **legs/tail/ears are still wrong**, use **text-to-3D (section C of the character file)** or **build the body in Blender from primitives** (the placeholder in `evg/characters.py` is a start) and use Meshy only for the head. A chunky toy shape is easy to model by hand. Eyes, collar, tag/bell are modelled in Blender regardless.
