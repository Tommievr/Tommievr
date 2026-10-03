# Design Team Workspace

Third channel next to `lead/` and `scriptwriters/`. Job: **keep Evie & Justin exactly on-model, put them in better, fully generated cartoony worlds.**

## Deliverables (in order)
1. **Character sheets** (`character-sheets/`): front, 3/4, side, 6 expressions (happy, curious, surprised, scared-but-brave, sleepy, laughing), walk/run poses. Built from `../assets/characters/evie-and-justin-reference.png`.
2. **Style guide** (`STYLE_GUIDE.md`): palette, lighting, line/shape language.
3. **Backgrounds** (`backgrounds/`): one per episode location, 16:9 plus a 9:16 crop-safe version, layered where possible (sky / far / mid / ground / foreground) so we can do parallax animation cheaply.
4. **Prompt library** (`prompts/`): tested prompts/settings that reproduce the look.
5. **Thumbnails + end cards** for episodes and shorts.

## Approval
Design proposals → lead approval → locked in `STYLE_GUIDE.md`. Nothing is "canon" until locked.

## Update: 3D pipeline
Characters will be built as 3D models with Meshy and animated in Blender via Python. See `meshy/MESHY_BRIEF.md`. Lambs (Cotton, Toffee) join mid-season; their sheets use the same format.
