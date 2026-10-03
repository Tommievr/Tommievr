# Production Plan (hardware day)

## Goal
Get 7 episodes + 21 shorts through a repeatable pipeline.

## Pipeline (3D, decided)
1. **Script** (writers) → lead approval
2. **Characters:** reference art → **Meshy** (image-to-3D) → clean, rig, test (see `../design/meshy/MESHY_BRIEF.md`)
3. **Environments:** modular cartoony 3D sets per location (Meshy props + Blender), see `../design/STYLE_GUIDE.md`
4. **Shot spec** in `../pipeline/shots/*.json` (character poses, camera, lines of dialogue, audio)
5. **Python builds the shot in Blender (bpy):** import models, apply animation/walk cycles/lip-sync, camera, lighting, render
6. **Voices:** Kokoro TTS → audio drives lip-sync timing
7. **Edit/assemble** (music, ambience), then **shorts** reframed to 9:16 (camera is shot-spec controlled, so re-render vertical rather than crop)
8. **QA:** facts, character consistency, kid-safety, ≤10:00

## Decisions made
- **Hardware:** strong (confirm specs with `tools/hardware_check.sh`).
- **3D:** characters via Meshy, animated/rendered by Python in Blender.
- **World:** fully generated, cartoony (see `../design/STYLE_GUIDE.md`).
- **Design team:** `../design/` — cats on-model, better backgrounds. Channel name/logo: TBD.
- **Voices:** free/open options only for now (see `VOICES_AND_HARDWARE.md`).

## Open decisions
- Meshy plan/licence: confirm the paid tier gives commercial rights to generated models (free-tier output may require attribution/not allow commercial use — verify on meshy.ai).
- Hardware specs: run `../tools/hardware_check.sh` and share the output.
- Final voice choice after listening tests.
- Channel name, logo, upload account.

## Suggested order
Do Episode 1 end-to-end first as the pipeline proof, then batch the rest.
