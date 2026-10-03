# Free voices & a "not-so-strong device" plan

## Free voices (verify each licence for **commercial/monetised** YouTube use before final choice)
| Option | Type | Notes |
|---|---|---|
| **Kokoro TTS** | open-source, runs locally, light | Apache-2.0, good quality, runs on CPU. Strong first pick |
| **Piper** | open-source, local, very light | Fast, runs on weak hardware; quality is plainer |
| **F5-TTS / XTTS-style cloning** | open-source, heavier | Can give distinct character voices; check model licence (some are non-commercial) |
| **Edge/Windows/Google free TTS** | cloud/free tier | Easy, but check terms and limits |
| **Volunteer/human voices** | real people | Free only if someone agrees in writing; get a simple voice-release for monetisation |

Plan: give Evie a higher, softer voice and Justin a lower, cheekier one; pitch-shift/EQ to separate them; test with the Ep.1 script.

## If the device is weak: low-compute animation
Fully generated video per shot is GPU-heavy. A cheaper way that still looks great and suits cartoon bedtime-story style:
1. Generate **still images** (cats in poses/expressions on layered backgrounds).
2. Animate with **parallax, camera moves, blinks/mouth swaps, bounce** in a free editor (e.g. DaVinci Resolve free, Blender, or Shotcut).
3. Use short generated clips only for hero moments.
Many successful kids' channels work this way; 7 × 10 min is realistic.

If the device can't even generate stills: use free cloud GPU tiers/colab-style notebooks for generation only and edit locally.
