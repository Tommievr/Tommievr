#!/usr/bin/env python3
"""Generates design/meshy/characters/<name>.md (copy-paste prompt packs). Edit CHARS / templates here, then run:
    python3 design/meshy/tools/build_prompt_packs.py
Also checks every text-to-3D prompt against the ~600-character limit (verify the current limit in Meshy)."""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "characters")
LIMIT = 600

STYLE = ("stylized 3D cartoon character, chunky toy-like vinyl figure, smooth short matte fur, simple rounded shapes, "
         "very big glossy eyes, clean flat bright saturated colors, soft toon shading")
NEG_COMMON = ("realistic fur, fur strands, hair, fluffy, fuzzy, fuzz halo, photorealistic, Pixar fur, detailed texture, noise, grain, "
              "open mouth, teeth, tongue, sitting, lying, running, jumping, action pose, tail wrapped around body, legs overlapping, "
              "extra legs, extra ears, extra tail, deformed, melted, multiple characters, background, floor, shadow, text, watermark, "
              "blurry, low quality, wide-angle distortion")

CHARS = {
 "evie": dict(
   title="Evie", species="kitten", bg="light grey #EDEDED",
   looks=("a cute chibi kitten with smooth short warm-white fur, one black patch on the top-left of the head (as seen from the front) over the base of the left ear, "
          "very big round glossy BLUE eyes, small rounded pink-inner ears, tiny pink nose, rosy cheeks, thin RASPBERRY PINK collar (#D01F4B) with a round chunky GOLD paw-print tag "
          "hanging at the front centre, short stubby legs with round paws, a thick fat tail curling upward"),
   text=("Cute chibi kitten, stylized 3D cartoon character, chunky toy-like figure, smooth short white fur, simple rounded shapes, one black patch on top-left of head, "
         "huge round glossy blue eyes, small pink inner ears, tiny pink nose, closed mouth, tiny smile, thin raspberry pink collar with round gold paw-print tag, "
         "short stubby legs, fat upward-curled tail, standing on four legs, neutral pose, matte clean flat colors, game-ready"),
   retex=("clean flat colors, warm white fur #FFF6EC, black patch #2A2030 on top-left of head, blue eyes #1E7FD6, pink ears #FFA9A0, raspberry collar #D01F4B, gold tag #FFB520, "
          "matte, no fur texture, no baked shadows, no noise"),
   side="Show the character's LEFT side (the side with the black patch).",
   ref_crop="the LEFT white kitten (Evie)",
   restyle_keep="white fur, the black patch on top-left of the head, blue eyes, pink collar with gold paw-print tag, pink ears and nose",
 ),
 "justin": dict(
   title="Justin", species="kitten", bg="white #FFFFFF or light grey #EDEDED",
   looks=("a cute chibi kitten with smooth short plum-black fur (#352B3D, clearly lit so the form is visible, NOT flat black), very big round glossy GREEN eyes with big white eye-whites, "
          "rounded ears with cream-white backs and pink insides, small dark-rose nose, full chubby cheeks, thin plain near-black collar with a round chunky GOLD paw-print tag at the front centre, "
          "short stubby legs with round paws, a short plump tail curled over the back"),
   text=("Cute chibi kitten, stylized 3D cartoon character, chunky toy-like figure, smooth short dark plum-black fur, simple rounded shapes, full chubby cheeks, "
         "huge round glossy green eyes with white eye-whites, rounded ears with cream backs and pink insides, small dark rose nose, closed mouth, tiny smile, "
         "thin plain dark collar with round gold paw-print tag, short stubby legs, short plump tail curled over back, standing on four legs, neutral pose, matte clean flat colors, game-ready"),
   retex=("clean flat colors, plum-black fur #352B3D, green eyes #3FB52A with white eye-whites, pink ears #FF9FA0 with cream backs #FFEBDD, dark collar #17121C, gold tag #FFB520, "
          "matte, no fur texture, no baked shadows, no noise"),
   side="Show either side (he has no markings).",
   ref_crop="the RIGHT black kitten (Justin)",
   restyle_keep="dark fur (lift it slightly so form is visible), green eyes with white eye-whites, cream-white ear backs, dark collar with gold paw-print tag",
 ),
 "cotton": dict(
   title="Cotton", species="lamb", bg="light grey #EDEDED",
   looks=("a cute baby lamb with soft cream wool made of 12-20 big simple rounded cloud-like clumps (NO curls, NO strands), a smooth short cream face, very big round glossy BLUE eyes, "
          "large floppy ears hanging out sideways with pink insides, small pink nose, thin LIGHT-BLUE collar (#7FB8F0) with a round gold sleigh bell with a HEART-shaped slot at the front centre, "
          "slim legs with chunky dark rounded hooves, a small round wool pom tail, a gentle shy look"),
   text=("Cute baby lamb, stylized 3D cartoon character, chunky toy-like figure, cream wool made of big simple rounded cloud clumps, smooth cream face, "
         "huge round glossy blue eyes, large floppy ears pink inside, small pink nose, closed mouth, tiny smile, thin light blue collar with round gold bell with heart-shaped slot, "
         "slim legs with dark chunky hooves, small round pom tail, standing on four legs, neutral pose, matte clean flat colors, game-ready"),
   retex=("clean flat colors, cream wool #FFF3DF, cream face #FFE7CF, blue eyes #1E7FD6, pink ears #FFA8A0, light blue collar #7FB8F0, gold bell #FFB520, dark hooves #5A4040, "
          "matte, no wool texture, no baked shadows, no noise"),
   side="Show either side.",
   ref_crop="the LEFT cream lamb (Cotton)",
   restyle_keep="cream wool (as big simple cloud clumps), blue eyes, floppy pink-inside ears, light-blue collar, gold heart bell, dark hooves",
 ),
 "toffee": dict(
   title="Toffee", species="lamb", bg="light grey #EDEDED",
   looks=("a cute baby lamb with chestnut-brown wool made of 12-20 big simple rounded cloud-like clumps (NO curls, NO strands), a smooth short cream face with a brown wool crown over the forehead, "
          "brown floppy ears hanging out sideways with pink insides, a cream chest blaze and cream lower legs like socks, very big round glossy GREEN eyes, small pink nose, "
          "thin LEAF-GREEN collar (#43A047) with a round gold sleigh bell with a HEART-shaped slot at the front centre, slim legs with chunky dark rounded hooves, a small round brown wool pom tail, a bold mischievous look"),
   text=("Cute baby lamb, stylized 3D cartoon character, chunky toy-like figure, chestnut brown wool made of big simple rounded cloud clumps, smooth cream face with brown crown, "
         "cream chest and cream socks, huge round glossy green eyes, brown floppy ears pink inside, closed mouth, tiny smile, thin leaf green collar with round gold bell with heart-shaped slot, "
         "slim legs dark chunky hooves, small round brown pom tail, standing on four legs, neutral pose, matte clean flat colors, game-ready"),
   retex=("clean flat colors, chestnut wool #9C4A1C, cream chest and socks and face #FFE9CF, green eyes #5CC236, brown ears #7A3A16 pink inside, leaf green collar #43A047, gold bell #FFB520, "
          "dark hooves #4A2E26, matte, no wool texture, no baked shadows, no noise"),
   side="Show either side. Cream socks and chest must be visible.",
   ref_crop="the RIGHT brown lamb (Toffee)",
   restyle_keep="chestnut wool (as big simple cloud clumps), cream chest and cream socks, cream face, green eyes, brown floppy ears, green collar, gold heart bell, dark hooves",
 ),
}

MASTER = ("Stylized 3D cartoon character turnaround reference, single character, full body, neutral standing pose on four legs, chunky toy-like vinyl figure look, "
          "smooth short matte fur with simple rounded shapes, very big glossy eyes with two highlights, clean flat bright saturated colors, soft toon shading, "
          "soft even neutral studio light, plain flat {bg} background, centered, square 1:1, full body visible with margin. "
          "Mouth CLOSED with a tiny relaxed smile. Eyes open, looking at the camera, symmetrical. All four legs standing straight and separated so all four paws are clearly visible. "
          "Clean smooth outline. NO fur strands, NO fuzzy halo, NO realistic fur, NO photorealism, NO outlines, NO props, NO text, NO shadow, no motion blur, no depth of field.")

VIEWS = {
 "FRONT": "FRONT VIEW: body and head facing the camera straight on, both front paws side by side, face symmetric.",
 "SIDE": "SIDE VIEW (exact profile, facing right): whole body exactly side-on, head turned to look at the camera, all four legs and the tail visible. {side}",
 "THREE_QUARTER": "THREE-QUARTER VIEW: body turned 45 degrees to the camera's left, head turned to look at the camera, all four paws visible.",
 "BACK": "BACK VIEW: seen from behind, tail visible, collar visible from behind. (Only if Meshy multi-image accepts a back view.)",
}

def block(name, d):
    img_prompts = []
    for k, v in VIEWS.items():
        img_prompts.append(f"**{k.replace('_', ' ')}**\n```\n{MASTER.format(bg=d['bg'])}\nCHARACTER: {d['title'].upper()}, {d['looks']}.\n{v.format(side=d['side'])}\n```")
    text = d["text"]
    assert len(text) <= LIMIT, f"{name}: text prompt is {len(text)} chars (> {LIMIT})"
    neg = NEG_COMMON + (", curly wool, curls, wool strands" if d["species"] == "lamb" else "")
    species_note = ("Two floppy ears out to the sides, hooves, pom tail; wool as big clumps." if d["species"] == "lamb"
                    else "Two upright rounded ears, fat tail raised; tufts only on cheeks, chest and tail tip.")
    md = f"""# Meshy prompt pack: {d['title']}
Generated by `design/meshy/tools/build_prompt_packs.py` (edit the script, not this file). Spec: `../../character-sheets/{name}.md`. Shared steps: `../MESHY_PROMPTS.md`. Fixes: `../QA_AND_FIXES.md`.
Style (decided): **stylised 3D cartoon, simple fur**. The reference PNG is **colour/markings reference only**.
Meshy UI names change: items marked ⚠ must be checked on the day. {species_note}

---
## A. Make the input images (do this first)
### A1. Restyle the reference (image-edit tools: ChatGPT/Gemini image edit, Flux Kontext, Midjourney with --oref/--cref)
Upload `assets/characters/{'evie-and-justin' if d['species']=='kitten' else 'lambs'}-reference.png` (crop it to {d['ref_crop']} first so the tool does not mix characters), then paste:
```
Use the attached image ONLY as a reference for colours and markings, NOT for the rendering style. Redraw {d['ref_crop']} as a stylized 3D cartoon character: chunky toy-like vinyl figure, smooth short matte fur (no fur strands, no fuzzy halo, no realistic fur, no Pixar-style fur), simple rounded shapes, very big glossy eyes, clean flat bright saturated colors, soft toon shading. Keep exactly: {d['restyle_keep']}. Neutral standing pose on four legs, mouth closed with a tiny smile, eyes open looking at the camera, soft even neutral light, plain flat {d['bg']} background, full body, centered, square.
```
### A2. Turnaround views (paste one per image; start with FRONT, then feed the best FRONT back in as the reference for the others)
{chr(10).join(img_prompts)}

**Negative prompt** (for tools with a negative field; otherwise append "Avoid: ..."):
```
{neg}
```
Pick the best of 4 variants per view with the on/off-model checklist in the character sheet. Save as `pipeline/meshy/{name}/raw/{name}_front.png`, `_side.png`, `_34.png` (and `_back.png`).

---
## B. Meshy image-to-3D (preferred)
| Setting ⚠ | Value |
|---|---|
| Mode | **Image to 3D**; if "multi-image" is offered upload FRONT + SIDE + 3/4 (+ BACK) |
| Model | newest available |
| Topology | **Quad** if offered, else Triangle |
| Target polycount | **30,000** (try 20,000 if it looks noisy; max 50,000) |
| Symmetry | **On** (Auto if On is not offered) |
| Pose option | **None / "as is"** (A/T-pose buttons are for humanoids) |
| Texture | **On**; PBR **off or ignore** (we only use base colour); if there is a "texture prompt", paste section D |
| Remove lighting / de-light ⚠ | **On** if offered |
| Export | **GLB** (also FBX if you want) |
Generate **4 times** (different seeds), keep the best two, write the seed in `LOG.md`.

## C. Meshy text-to-3D (fallback or comparison)
Prompt (≤ {LIMIT} characters: this one is {len(text)}):
```
{text}
```
Negative prompt:
```
{neg}
```
| Setting ⚠ | Value |
|---|---|
| Art style | **Cartoon** (not Realistic) |
| Pose | none; (the prompt already says neutral standing pose) |
| Symmetry | On |
| Topology / polycount | Quad, 30,000 |
| Flow | **Preview** first (geometry, check silhouette), then **Refine / texture** only if the preview is good |

## D. Texture / retexture prompt (use in Meshy "Retexture", or the texture-prompt field)
```
{d['retex']}
```
(Colour hexes are written into the prompt as hints. Expect to correct colours in Blender anyway: `../QA_AND_FIXES.md` section 3.)

## E. After Meshy (summary; details `../../blender/SETUP.md`)
1. Save to `pipeline/meshy/{name}/raw/` + `LOG.md` (date, plan, seed, settings, prompt).
2. `blender -b --python pipeline/blender/qa_model.py -- pipeline/meshy/{name}/raw/{name}.glb --shot qa.png`
3. Run the QA checklist (`../QA_AND_FIXES.md`). PASS → clean, separate parts (eyes, collar, tag/bell), toon material, rig.
"""
    return md

os.makedirs(OUT, exist_ok=True)
for n, d in CHARS.items():
    with open(os.path.join(OUT, f"{n}.md"), "w") as f:
        f.write(block(n, d))
    print("wrote", n, "text prompt chars:", len(d["text"]))
