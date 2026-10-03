# Ep.7: Wadden Sea mudflats — "Walking on the Sea Floor"
> **v1.1 style update (lead direction):** backgrounds are **simple, bold, clean 3D cartoon**: big flat colour shapes, 3-5 hero props, chunky bevelled forms, no texture noise, no normal-map grit, no fine detail. Facts/sources below are unchanged. Copy-paste prompts: `prompt-packs/07-wadden-sea.md`.

**Accent:** silver-pink `#E7C6CF`. **Hero silhouette:** endless flat wet sand mirroring the sky with one thin line of tidal-channel water.
**Mood:** vast, quiet, shimmering, wonder; finale of the first season; the bedtime outro lives here: sunset reflections.

## What is true (and what we keep)
| Real element | Cartoon version |
|---|---|
| World's largest intertidal mudflat system, UNESCO World Heritage ([Wikipedia/overview via search](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/wadden-sea), [Visit Wadden](https://www.visitwadden.nl/en/story-lines/world-heritage)) | endless flat horizon, the horizon is **two-thirds ground** |
| Sandbanks criss-crossed with trenches and gullies, big to small; sandy near inlets, muddier near the coast ([ScienceDirect](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/wadden-sea)) | **branching tidal channels** as light-blue ribbons in silver-pink sand; a few flat ripple bands |
| At low tide shallows fall dry so people can walk across: **wadlopen** (mudflat walking) with guides; mud, channels, waist-high water ([Holland.com](https://www.holland.com/global/tourism/discover-the-netherlands/visit-the-regions/wadden-islands/mud-flat-walking)) | cartoon: shallow ankle-deep puddles; **no deep mud, no wading in channels for the kittens**; a "guide" is **not shown** (no real people; mention guide in dialogue only) |
| Birds: curlews, knots, oystercatchers, gulls, ducks, spoonbills; also seals ([Holland.com](https://www.holland.com/global/tourism/discover-the-netherlands/visit-the-regions/wadden-islands/mud-flat-walking), [Swallow's Notes](https://www.swallowsnotes.com/blog/the-wadden-sea-tidal-wilderness-at-the-countrys-edge)) | **oystercatchers** (black/white, orange beak) as hero birds, a gull flock, a **seal pup on a sandbank** (friendly, at a distance, never touched) |
| Route markers (poles/branches) ⚠ not confirmed by my searches; widely used to mark mudflat routes, verify the Dutch practice | simple **thin wooden poles** with a colour band, receding in a line; verify first |
| "Mirror" effect of wet sand under the sky | **wet sand with high gloss: sky reflection** in the lower frame (the signature look) |

## Layered set
| Layer | Content |
|---|---|
| **SKY** | huge pastel sky, silver-pink `#F6D3CC` at horizon, `#B5CCE6` above; layered stratus; sky is **mirrored** below |
| **FAR** | a very thin silver line: the far sea / a distant island dune (Wadden island) with a tiny lighthouse silhouette ⚠ pick a fictional-looking one, no real island landmark necessary |
| **MID** | channel junction with calm water, seal on a bank, bird flocks, poles |
| **GROUND** | wet sand in ripple patterns, **glossy**, sky reflections, tiny puddles; paw prints trailing behind |
| **FG** | blurred tufts of salt-marsh grass, shells (cockle shapes), a feather; one oystercatcher pair |

## Key props to model
1. **Oystercatcher** (hero bird, 2 poses: standing, walking): `chunky stylized oystercatcher bird, black and white plumage, long orange beak, pink legs, cartoon storybook, no text`
2. **Seal pup** (resting): `cute stylized grey harbour seal pup resting on sand, big dark eyes, cartoon storybook, no text`
3. **Gull** (flock kit), **curlew** (optional)
4. **Poles** with colour band (modular), **shell** kit, **salt-marsh grass**
5. **Wet sand floor material** (flat toon colour + glossy reflection plane in EEVEE, Cycles only for hero stills; no normal map)
6. **Tide visual:** an animated water plane that slowly **fills the channels** during the episode (concept: tides)
Safety: the tide must **never look threatening**: gentle water level change, the characters head back **with the "guide" off-screen** (no real people); no dangerous-behaviour modelling (Bible rule 3).

## Variants
| Variant | Look |
|---|---|
| Day | bright light, silver sand, strong blue channels |
| **Golden hour** | pink-gold mirrored sky, **long reflections of the characters** (tags glow in the reflection) |
| Dusk | indigo/rose mirror, a star or two, silver water ribbons; **the finale goodnight shot** |

## 9:16 notes
The vertical frame lets the **mirror** work beautifully: horizon at the **upper third**, reflection fills the middle, characters standing in reflection; channels as converging diagonal ribbons. Keep birds in the upper centre, away from the Shorts buttons (right 160 px).
