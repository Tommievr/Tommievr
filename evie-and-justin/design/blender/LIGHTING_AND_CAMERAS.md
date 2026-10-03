# Lighting rig and camera presets (toon, EEVEE)
Code: `pipeline/blender/evg/lights.py`, `cameras.py`, `palette.py` (values). Style rules: `../STYLE_GUIDE.md` sections 4-5.

## 1. Lighting rig (automatic)
```python
from evg import lights, cameras
chars = bpy.data.collections["CHARACTERS"]               # light linking target
lights.build_rig("golden", target=(0, 0, 0.15), char_collection=chars)   # "day" | "golden" | "dusk"
```
`build_shot.py` does this for you (`"variant"` in the spec, `--variant` on the command line). Creates collection `RIG_Golden`:

| Light | Type | Colour | Golden strength | Where (relative to the camera looking along +Y from -Y) |
|---|---|---|---|---|
| `KEY_sun` | Sun, angle 5° | `#FFC76B` | 3.5 | elevation 17°, azimuth +40° (front-right) |
| `FILL_sky` | Area disk 6 m | `#9EC5FF` | ≈ 120 W | azimuth -50°, elevation 12°, 4 m |
| `RIM_L`, `RIM_R` | Area disk 1.5 m | `#FFD9A8` | ≈ 720 W | azimuth ∓150°, elevation 28°, 2.5 m (behind-left/right) |
| `KICK_ground` | Area disk 2 m | `#F7B58A` | ≈ 35 W | low, front |
| `TAG_glow` | Point (`lights.add_tag_glow`) | `#FFC76B` | 0 → 40 → 0 | at the tag/bell; pulses at discovery |
Rim, kick and tag glow are **light-linked to the `CHARACTERS` collection only** (Blender 4.0+), so they never wash the background. If your Blender lacks light linking they just light everything (fine for tests).

Variants (`palette.py VARIANTS`): **day** 45° `#FFE9C4` 4.0 · **golden** 17° `#FFC76B` 3.5 · **dusk** 5° `#F2A5A0` 1.6 (dusk rim `#FFB48A`). The world is a simple 2-colour sky gradient; the camera sees it at full strength, lighting uses only 30 % so toon shadows stay visible.
Tune by eye: if shadows vanish → lower the world `ambient` or raise the toon `threshold`; if characters look flat → raise rim strength 1.5×; if the ground is dark at low sun → ground material `threshold=0.2`.

## 2. Cameras
```python
cam = cameras.place_camera("medium_two", subject=(0, 0, 0.15), yaw_deg=0, aspect="16:9")   # or "9:16"
```
Presets (metres, storybook scale; `distance_scale` 1.3 is applied automatically for lambs):

| Preset | Lens 16:9 | Lens 9:16 | Height | Distance | f-stop | Use |
|---|---|---|---|---|---|---|
| `wide_establish` | 24 | 28 | 1.3 | 11 | 22 | arrival, place reveal, sky 50 % |
| `wide_two` | 28 | 40 | 0.35 | 3.5 | 16 | walking |
| `medium_two` | 40 | 60 | 0.25 | 1.8 | 11 | dialogue |
| `medium_single` | 50 | 70 | 0.22 | 1.25 | 11 | one speaker |
| `close_up` | 85 | 110 | 0.20 | 0.8 | 11 | emotion |
| `extreme_close_tag` | 100 | 135 | 0.15 | 0.4 | 8 | tag/bell glow |
| `low_hero` | 28 | 40 | 0.08 | 1.2 | 11 | brave moment, tilts up 10° |
| `over_shoulder` | 50 | 70 | 0.25 | 1.0 | 11 | reveal the place |
- Sensor 36 mm, **horizontal fit**: the same lens means the same width in both aspects; the 9:16 lenses are longer so characters stay big in vertical.
- **Why high f-stops:** a kitten is ~0.3 m deep; a "real" f/2.8 close-up blurs half the face (tested). Background softness comes from distance. Focus point = the face.
- Spec: `"camera": {"preset": "close_up", "yaw": 20, "distance_scale": 1.0, "look_offset": [0,0,0.05], "tilt_deg": null, "subject": [x,y,z]}`.
- Same shot, vertical Short: add `--aspect 9:16` (re-render; do not crop). Check the safe area below.

## 3. Safe areas (also `cameras.SAFE`, fractions of the frame)
| Aspect | Area | Rule |
|---|---|---|
| 16:9 1920×1080 | action 93 % (inset 67×38), title 90 % (inset 96×54) | faces in the central 70 % width |
| 16:9 | subtitle band y 800-980 | no faces behind subtitles |
| 9:16 1080×1920 | **content x 60-920, y 250-1400** | right ~160 px = buttons, top ~13 % = UI |
| 9:16 | caption band y 1400-1560 | head centre y ≈ 800-1000 |
*Check against the live Shorts UI before locking; it changes.* To see guides while framing: in the Camera data panel enable **Safe Areas** (Viewport Display → Safe Areas) and use the numbers above.

## 4. Horizon and composition
Horizon at the lower third for sky-heavy wides, middle for dialogue; never through a head. Characters bright, world a little duller (STYLE_GUIDE section 1).
