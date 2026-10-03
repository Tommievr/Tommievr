#!/usr/bin/env python3
"""Generates design/backgrounds/prompt-packs/NN-<location>.md. Edit LOCS here, then:  python3 design/backgrounds/tools/build_prompt_packs.py
Checks every Meshy prop prompt is <= 600 characters (verify Meshy's current limit)."""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt-packs")
LIMIT = 600
STYLE = "stylized 3D cartoon, simple bold shapes, chunky toy-like, smooth, flat clean saturated colors, minimal detail, no texture noise"
PROP_SUFFIX = ", " + STYLE + ", single object, game-ready low poly"
PROP_NEG = ("realistic, photorealistic, detailed texture, noise, tiny details, thin parts, text, letters, logo, watermark, people, characters, "
            "multiple objects, background, ground, floor, blurry, low quality, broken, floating parts")

VARIANTS = {
    "DAY": "bright clear blue sky, white-cream clouds, clean daylight, short shadows",
    "GOLDEN HOUR (default hero look)": "warm golden-hour light, low sun, peach horizon, long soft plum shadows, glowing rim on shapes",
    "DUSK": "dusk, indigo sky fading to apricot and rose at the horizon, calm, a few tiny warm lights, soft violet shadows",
}

LOCS = [
 dict(n="01", slug="afsluitdijk", title="Afsluitdijk (Ep.1)", accent="sea teal #3FA7A6", pal="sky #8EC8F0 > #FFE3B0, grass #8CBF6A, concrete #E8DCC8, road #B9B1A6",
      scene="a very long straight dike road with a cycle path running to the vanishing point, silvery-teal sea on the left and calm bright lake on the right, one slim cream concrete monument tower on the right third, huge sky with a few big simple clouds",
      far="thin flat land line far away on the lake side, a tiny barge, hazy blue-grey, 2-3 flat tones",
      props=[("Monument tower (hero)", "Tall slim stylized observation tower, cream concrete, flat viewing platform on top, narrow glass stair slot down the side, simple geometric, tapered base"),
             ("Statue on plinth", "Small generic bronze statue of a standing man on a chunky square stone plinth, simple smooth shapes, no face detail"),
             ("Sluice tower row", "Row of six chunky cream concrete machine towers with flat steel gate panels between them, simple blocky shapes, shared base"),
             ("Barge", "Simple chunky cargo barge, flat low hull, small blue cabin, rounded edges, toy-like"),
             ("Seagull", "Cute simple seagull with wings spread in flight, white body, grey wing tips, orange beak, smooth low poly")],
      hand="road + guard-rail + lamp-post modules (Blender, 10 m piece), stone-block slope tile, sea/lake water planes (flat toon, teal / bright blue, 1 soft wave band)"),
 dict(n="02", slug="schokland", title="Schokland (Ep.2)", accent="field gold #E3B93C", pal="sky #A9D3F0 > #FFE0A8, grass #9CC657, church #F3EBD8, houses blue #5E8FB5 / green #6FA37A",
      scene="a low grassy rise like a little island in a sea of flat fields in gold and green stripes, a small simple white church with a tiny bell tower and a few small blue and green timber houses on top, a low stone wall along the edge, a row of short wooden posts tracing the old shoreline into the fields, a small lighthouse far in the distance, long low wave-like clouds",
      far="flat field bands in gold and green stripes, thin tree line, faint ship-shaped cloud, 3 flat tones",
      props=[("Church (hero)", "Small simple old church, cream white walls, steep red tile roof, tiny square bell tower, arched door, chunky rounded shapes"),
             ("Timber house, blue", "Small chunky wooden cottage, blue painted planks, steep brown roof, tiny door and two windows, simple"),
             ("Timber house, green", "Small chunky wooden cottage, green painted planks, steep brown roof, tiny door and two windows, simple"),
             ("Lighthouse + keeper house", "Small chunky lighthouse tower, cream with a grey top, attached low keeper cottage with red roof, simple shapes"),
             ("Shoreline post (hero prop)", "Short chunky wooden post, rounded top with a painted blue band, slightly weathered, simple, toy-like")],
      hand="retaining-wall segment (tileable, grey stone + timber cap), field stripes as flat planes, mound as a smooth displaced plane"),
 dict(n="03", slug="giethoorn", title="Giethoorn (Ep.3)", accent="canal green #4FA37A", pal="sky #9AD0E8 > #FFD9B0, grass #7DB86A, thatch #C9A24B, brick #B5533C, water #3F8A8C",
      scene="a narrow calm canal as the leading line, chunky thatched-roof farmhouses on small grassy islands, small arched wooden footbridges, a moored open boat, big round willow trees leaning over the water, reeds, lily pads, warm light through the leaves",
      far="rows of rounded poplar and willow shapes, a glimmer of lake, soft hazy green, 3 flat tones",
      props=[("Thatched farmhouse (hero)", "Chunky Dutch farmhouse, very thick rounded golden thatch roof, red brick walls, small shuttered windows, simple toy-like shapes"),
             ("Arched wooden footbridge (hero)", "Small arched wooden footbridge, chunky planks, simple handrail, rounded arch, brown wood"),
             ("Whisper boat", "Low flat open boat, cream hull with green trim, two simple benches, rounded edges, toy-like"),
             ("Willow tree", "Big round willow tree, short thick trunk, drooping rounded green foliage clumps, simple smooth shapes"),
             ("Mooring post and flower box", "Chunky wooden mooring post with a rope loop, next to a small wooden flower box with pink and white flower blobs")],
      hand="canal water plane (flat toon teal, soft reflection optional), peat banks (dark brown), reed clumps as repeated cones"),
 dict(n="04", slug="hunebedden", title="Hunebedden, Drenthe (Ep.4)", accent="stone grey-purple #8B8499", pal="sky #9CB8DC > #F4CBB0, moss #6E8F4E, stone #A29BB0, heather #8E6BA8, mist #CFC6DA",
      scene="a forest clearing with a long low table of huge rounded grey-purple stones (big flat capstones on thick upright stones, moss on top), a few birch and oak trunks framing, purple heather and a soft mist band behind, low golden light slanting through the trees, empty path in the foreground",
      far="purple heath hill, dark tree line, soft pale mist band, 3 flat tones",
      props=[("Capstone (modular, make 3 variants)", "Huge flat rounded boulder slab, grey-purple stone with a green moss patch on top, smooth lumpy shapes, simple"),
             ("Upright support stone (make 3 variants)", "Thick rounded upright standing stone, grey-purple, smooth lumpy shape, slightly leaning, simple"),
             ("Single mossy boulder", "Big rounded mossy boulder, grey-purple with green moss patches, smooth, simple chunky shape"),
             ("Birch tree", "Stylized birch tree, white trunk with a few dark marks, rounded light-green foliage clumps, chunky simple shapes"),
             ("Oak tree", "Stylized oak tree, thick brown trunk, big rounded dark-green foliage clumps, chunky simple shapes")],
      hand="assemble the hunebed from stones in Blender (6 capstones, ~16 uprights, entrance gap), heather clumps (instanced purple blobs), mist = a flat translucent gradient plane or volume. Do NOT invent carvings."),
 dict(n="05", slug="kootwijkerzand", title="Kootwijkerzand (Ep.5)", accent="sand orange #E8A55B + heather purple #9A5FB0", pal="sky #9FD0F0 > #FFD8A0, sand #E8A55B / #F2D29B, pine #3F6B4A, heather #9A5FB0",
      scene="rolling pale-orange sand dunes with soft ripples, a wind-bent twisted Scots pine with a flat umbrella crown and some exposed roots on a dune crest, patches of purple heather, a dark green pine forest edge in the distance, a low wooden marker post, long stretched wind-streak clouds, a few drifting sand streaks",
      far="dune ridges in peach, pale orange and lilac, dark green forest edge, purple heath band, 3 flat tones",
      props=[("Wind-bent pine (hero, make 3)", "Stylized wind-bent Scots pine, twisted reddish trunk, flat umbrella crown of rounded dark-green clumps, a few exposed roots, chunky simple shapes"),
             ("Heather clump", "Small clump of purple heather, rounded bush made of simple purple blobs on short green stems, chunky"),
             ("Wooden marker post", "Short chunky wooden marker post with a flat top and a painted orange band, simple, toy-like"),
             ("Grass tuft", "Small tuft of pale dune grass, simple pointed blades in a rounded cluster, chunky"),
             ("Pine cone (set dressing)", "Big chunky pine cone, brown rounded scales, simple smooth shape")],
      hand="dunes as smooth displaced planes with a soft ripple (flat toon, no normal map), wind-swirl ribbons (animated translucent cream curves), sand-streak particles"),
 dict(n="06", slug="delta-works", title="Delta Works / Neeltje Jans (Ep.6)", accent="steel blue #4C7FB0", pal="sky #7DB8E8 > #FFD4A8, concrete #D5DADF, sea #3C8FC8, gates #4C7FB0, buoy red #E0553C",
      scene="a long row of giant light-grey concrete piers standing in calm blue water receding into the haze, steel-blue gates between them, a thin road deck on top, a simple gantry crane, a concrete island apron with a yellow safety line and railing in the foreground, towering simple clouds, red and white buoys",
      far="the pier row fading into haze, a distant ship, flat coast line, 3 flat tones",
      props=[("Pier (hero, repeat with Array)", "Tall tapered concrete pier of a storm surge barrier, light grey, vertical slot for a gate, flat top with a thin road deck, chunky simple geometry"),
             ("Gate panel (make 3 states)", "Huge flat steel-blue gate panel with simple horizontal ribs, rounded edges, chunky, stylized"),
             ("Gantry crane", "Simple chunky gantry crane, yellow-orange frame on four legs, flat top beam, toy-like"),
             ("Railing and bollard kit", "Chunky safety railing section in white, plus a short yellow-black striped bollard, simple, toy-like"),
             ("Fishing boat", "Small chunky fishing boat, white hull with a blue stripe, red cabin, rounded edges, toy-like"),
             ("Buoy", "Chunky round buoy, red and white bands, small ring on top, simple smooth shape")],
      hand="flat toon sea plane with a soft foam ring at the pier bases, island apron slabs + yellow line (Blender), arrays of piers"),
 dict(n="07", slug="wadden-sea", title="Wadden Sea mudflats (Ep.7)", accent="silver-pink #E7C6CF", pal="sky #B5CCE6 > #F6D3CC, sand #B79A94, wet sand mirror #F3D9D2, channels #9CC4D0",
      scene="an endless flat expanse of glossy wet sand mirroring a huge pastel sky, a few branching light-blue tidal channels, a line of thin wooden poles receding, a seal pup resting on a sandbank, a pair of oystercatchers, a flock of gulls, a very thin silver line of sea on the horizon",
      far="thin silver sea line, a tiny far island dune, 2 flat tones",
      props=[("Oystercatcher (hero)", "Cute stylized oystercatcher bird standing, black and white plumage, long orange beak, pink legs, chunky simple shapes"),
             ("Seal pup", "Cute stylized grey seal pup resting, big dark eyes, smooth round body, chunky simple shapes"),
             ("Gull", "Cute simple seagull standing, white body, grey wings, yellow beak, smooth low poly"),
             ("Route pole", "Thin-ish chunky wooden pole with a painted colour band near the top, slightly leaning, simple"),
             ("Cockle shell", "Big chunky cockle shell, cream with soft ridges, simple smooth shape"),
             ("Salt-marsh grass tuft", "Small tuft of green-grey salt-marsh grass, simple pointed blades in a rounded cluster, chunky")],
      hand="the wet-sand floor: flat toon material + glossy reflective plane (EEVEE reflection / Cycles for hero frames), animated tide water plane that slowly fills channels, channels as light-blue ribbons"),
]

def pack(L):
    img = ("Simple bold stylized 3D cartoon background, {t}: {s}. Flat clean saturated colors, big simple soft shapes, minimal detail, NO texture noise, "
           "NO realistic detail, NO characters, NO text, empty open lower third for characters, accent colour {a}, palette {p}.")
    base = img.format(t=L["title"].split(" (")[0], s=L["scene"], a=L["accent"], p=L["pal"])
    vtxt = "\n".join(f"**{k}**\n```\n{base} {v}. Wide 16:9.\n```" for k, v in VARIANTS.items())
    props = []
    for name, p in L["props"]:
        full = p + PROP_SUFFIX
        assert len(full) <= LIMIT, f"{L['slug']} / {name}: {len(full)} chars"
        props.append(f"**{name}**\n```\n{full}\n```")
    props_md = "\n".join(props)
    return f"""# Prompt pack: {L['title']}
Generated by `design/backgrounds/tools/build_prompt_packs.py` (edit the script). Brief: `../{L['n']}-{L['slug']}.md` (facts, sources, ⚠ unverified items). Style: `../../STYLE_GUIDE.md` (simple, bold, clean 3D cartoon).
**Accent:** {L['accent']} · **Palette:** {L['pal']}

## 1. Background image prompts (sky/far plates and concept reference)
Use for the **sky plate** (paint it flat/unlit as an emission backdrop) and as a concept guide for the 3D set. Tools: any image generator. Generate **16:9** and **9:16** (add "vertical 9:16, taller sky, centred composition" for the latter). Pick the simplest result; reject anything with fine detail, text or people.
{vtxt}

**Far-layer plate only** (transparent or plain-sky background if the tool allows; for parallax):
```
Simple bold stylized cartoon far-distance layer, {L['far']}, flat clean colors, no characters, no text, no foreground, wide 16:9, golden-hour light.
```
**Sky plate only:**
```
Simple stylized cartoon sky, big soft simple clouds in 2-3 flat tones, smooth simple gradient, sky colours {L['pal'].split(',')[0]}, warm peach at the horizon, no ground, no text, wide 16:9.
```
**Negative prompt** (if supported): `photorealistic, realistic textures, noise, grain, tiny details, text, letters, logo, watermark, people, characters, animals, blurry, low quality`

## 2. Meshy prop prompts (text-to-3D; one object per generation)
Each prompt is ≤ {LIMIT} characters. Settings ⚠ (check names on the day): **Art style: Cartoon** · **Topology: Quad** · **Target polycount: 5,000-15,000** (hero prop up to 20,000) · **Symmetry: On** (Off for trees/rocks) · Pose: none · Preview first, then Refine/texture only if the silhouette is good · Export **GLB**.
Negative prompt for all props:
```
{PROP_NEG}
```
{props_md}

After download: `blender -b --python pipeline/blender/qa_model.py -- prop.glb --shot prop_qa.png`; fix with `design/meshy/QA_AND_FIXES.md` (props are forgiving: re-roll cheap). Convert to toon (`toon.convert_to_toon(obj)`), scale to **1.5x real size** relative to the characters (`STYLE_GUIDE` section 6), save to `pipeline/scenes/{L['slug'].replace('-', '_')}.blend`.

## 3. What to build by hand in Blender (not Meshy)
{L['hand']}.

## 4. Scene collections (so shots and parallax work)
`{L['slug'].replace('-', '_').upper()}_SKY`, `_FAR`, `_MID`, `_GROUND`, `_FG` (see `../README.md`). Keep the characters' ground strip (3-6 m deep) clean and simple; 3-5 hero props per set.
"""

os.makedirs(OUT, exist_ok=True)
for L in LOCS:
    with open(os.path.join(OUT, f"{L['n']}-{L['slug']}.md"), "w") as f:
        f.write(pack(L))
    print("wrote", L["slug"], "props:", len(L["props"]))
