# Setup Guide — Evie & Justin's Little Adventures
Prepared 2026-10-04. Prices were checked on the web on this date but change often: **always confirm on the vendor's own page before paying.**

## 0. The friend's PC: ground rules
- Ask the owner first, and agree how long you may use it and how much disk space you may fill.
- Make a **separate Windows/macOS user account** (or at least a separate folder) for this project.
- **Never save passwords in the browser** and **sign out of every account** when you are done (GitHub, Google, Meshy). Remove saved tokens.
- Keep project files on an **external drive/USB or cloud** so nothing is stuck on the friend's PC. Models and renders get big (tens of GB).
- Do not install anything the owner doesn't want. Everything below can be uninstalled.

## 1. Accounts you need
| # | Account | Why | Who | Cost |
|---|---|---|---|---|
| 1 | **Google account** (new one for the channel is cleaner) | YouTube channel, Google Drive for backup | Tommie | Free |
| 2 | **YouTube channel** (can be a Brand Account) | Publishing episodes + shorts | Tommie | Free |
| 3 | **GitHub** (you already have `tommievr`) | Download all scripts/prompts/code from the repo | Tommie | Free |
| 4 | **Meshy** (meshy.ai) | Make the 3D characters | Tommie | Free tier, or paid (section 4) |
| 5 | **An image generator** (only if you use Day-1 step "restyle reference → turnaround images") | Neutral-pose images of each character as Meshy input | Tommie | Depends on tool; many have a free tier. Choose one on the day. |
| 6 | **Email for the channel** (business/brand email, optional but wise) | So the channel isn't tied to a personal inbox | Tommie | Free |
Not needed: any account for Blender, Kokoro or DaVinci Resolve (just downloads).

**Age/identity note:** to run a YouTube channel and a monetised one, the account holder must be of age; YouTube may ask for phone verification. Confirm who legally owns the channel.

## 2. Software to install on the PC (all free)
| Software | Purpose | Cost | Notes |
|---|---|---|---|
| **Blender** (blender.org) | Build, rig, light and render the shots | Free, any use incl. commercial | Install the version the design team wrote against (4.2 LTS or 5.x; check `design/blender/`) |
| **Python 3** | Run helper scripts and Kokoro | Free | Blender has its own Python; this one is for Kokoro/tools |
| **Git** (+ optional GitHub Desktop) | Get the repo | Free | `git clone https://github.com/tommievr/tommievr` |
| **FFmpeg** | Encode video | Free | Some scripts fall back to PNG sequences without it |
| **Kokoro TTS** | The voices (Evie, Justin, Cotton, Toffee, narrator) | Free (Apache 2.0, commercial use allowed) | Re-check the licence on the day |
| **Rhubarb Lip Sync** | Mouth shapes from audio | Free | Check its licence on the day |
| **DaVinci Resolve (free)** or Shotcut | Assemble episodes, music, subtitles | Free | |
| **Audacity** (optional) | Voice clean-up | Free | |

## 3. Step by step

### Phase A — Prep (before you touch the PC)
1. Create/confirm the **Google + YouTube accounts** and **Meshy account** on your own device (so you don't type passwords on the friend's PC more than needed).
2. Get the repo link ready: branch `claude/youtube-channel-evie-justin-64thoj`, folder `evie-and-justin/`.
3. Print or open `design/DAY1_CHECKLIST.md` on your phone.

### Phase B — Set up the PC (about 1–2 hours)
1. Create the separate user/folder. Check free disk space (aim for 100 GB+).
2. Install Blender, Python, Git, FFmpeg.
3. Run `evie-and-justin/tools/hardware_check.sh` (or screenshot Task Manager → Performance, GPU). **Send me the result.**
4. Clone the repo and check out the branch.
5. Install Kokoro (see `lead/VOICES_AND_HARDWARE.md`). Generate one test sentence for each character voice.
6. Run the **no-model test render** from the Day-1 checklist. Note the time per frame and the Blender version. Send me both.

### Phase C — Characters (Day 1)
1. Follow `design/DAY1_CHECKLIST.md`: **Evie first**. Send me the images, the QA render and the printout before starting Justin.
2. Meshy workflow: `design/meshy/MESHY_PROMPTS.md` (copy-paste prompts, settings, negatives) and `design/meshy/QA_AND_FIXES.md` (fixing bad generations).
3. Then Justin, Cotton, Toffee. Then props: Moondew Blossom, Evie's pouch (Blender-built), flower crown.
4. Record plan name, date and licence wording in `pipeline/meshy/LICENCE_NOTES.md`.

### Phase D — Pilot episode (Ep.1 end to end)
1. Backgrounds from `design/backgrounds/prompt-packs/` (Afsluitdijk).
2. Voices with Kokoro from `scriptwriters/scripts/ep01-afsluitdijk.md`.
3. Shots via `pipeline/blender/build_shot.py` (shot JSON files).
4. Assemble in DaVinci Resolve, add music, captions (the paw signal captions are required: [soft chime]/[low hum]).
5. Render the 3 Ep.1 shorts (vertical re-render, not crop).
6. Send me the result and time spent so we can plan episodes 2–7.

### Phase E — Publish
1. YouTube Studio → upload the episode. **Audience setting: decide "Made for kids" (see section 5)**.
2. Follow the 28-day plan in `scriptwriters/shorts/RELEASE_CALENDAR.md` (shorts 16:30, episodes 18:30).
3. Add an AI-content disclosure where YouTube asks for it (realistic synthetic voices/visuals; check the current form).

### Phase F — Clean-up on the friend's PC
Sign out everywhere, remove saved passwords, copy all files to your drive, delete the project folder if agreed, return the PC.

## 4. Costs (checked 2026-10-04)
| Item | Cost | Notes |
|---|---|---|
| Blender, Kokoro, Rhubarb*, DaVinci Resolve free, Shotcut, Audacity, Git, FFmpeg, Python | **€0** | *check licence on the day |
| Google/YouTube/GitHub accounts | **€0** | |
| **Meshy Free** | **€0** | 100 credits/month. Models made on Free are **CC BY 4.0**: commercial use is allowed but **you must credit Meshy**. Not enough credits for 4 characters + props with retries. |
| **Meshy Pro** | **about $20/month** ($16/month yearly) | 1,000 credits/month, **private licence, you own the output**. Recommended for the production month (cancel after). ([Meshy pricing](https://docs.meshy.ai/en/webapp/pricing), [overview](https://costbench.com/software/ai-3d-generation/meshy/)) |
| Meshy higher plans | Studio / $40 / $100 tiers exist | Only needed if you run out of credits |
| Image generator for turnaround images | €0 to ~€20/month | Depends on the tool; many have free tiers. Pick on the day. |
| Music/sound effects | €0 to a few euros | YouTube Audio Library is free; check each track's licence |
| Electricity (PC rendering) | a few euros | Offer to cover it for your friend |
| Domain/website, trademark | optional | Not needed to start |
| **Realistic total to make the 7 episodes** | **~€0–€40** | Mostly one month of Meshy Pro (+ maybe an image tool) |

Meshy credits per model depend on settings (texture, retopology, rigging). The credit cost per model is not confirmed here: check Meshy's pricing page when you pick settings, and test one character before buying more credits.

## 5. Decision to make before uploading: "Made for kids"
Content aimed at children must normally be marked **Made for Kids** (US COPPA rules). Consequences ([overview](https://vidiq.com/blog/post/make-money-kids-youtube-channel/)):
- You **can** still join the YouTube Partner Programme, but ads are contextual only, so **revenue is lower**.
- **Comments, notifications, memberships, Super Chat, end screens/cards are turned off** on those videos.
- Partner Programme needs roughly 1,000 subscribers plus 4,000 public watch hours, or 10M Shorts views in 90 days. Check YouTube's current thresholds.
- Don't pick the wrong label to get comments or better ads; YouTube and the FTC penalise wrong labelling. If unsure, ask YouTube's help page or a professional.

## 6. Hardware notes
- **Meshy runs in the cloud:** the PC's GPU doesn't matter for making models.
- **Blender/EEVEE** needs a reasonably modern GPU with up-to-date drivers; the render-time test in Phase B tells us whether episode rendering is realistic (target: ≤ a few seconds per frame).
- **Kokoro** runs fine on CPU.
- If the PC is too slow: lower resolution/samples, render in batches overnight, or fall back to the still-image + parallax plan in `lead/VOICES_AND_HARDWARE.md`.

## 7. Safety/legal checklist
- ☐ Meshy plan + licence recorded (`pipeline/meshy/LICENCE_NOTES.md`)
- ☐ Voice tool licence checked (Kokoro: Apache 2.0)
- ☐ Music licences saved per track
- ☐ Facts spot-checked on an open network (rows marked ☐ in `scriptwriters/research/`)
- ☐ "Made for kids" decision made
- ☐ AI/synthetic-content disclosure completed on upload
- ☐ Nothing on screen shows real people or brands
- ☐ Real children never taste things they find: safety line kept in Ep.1 and Ep.7
