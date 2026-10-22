---
name: promo-plan
description: Use when a product or brand needs a video promo plan (shot list, After Effects motion spec, Premiere sequence and export matrix, rights log and disclosure placement). Runs the media-producer in a fresh context and writes to the media folder of the project you name.
argument-hint: <project folder> | <product> | <length in seconds> | <platforms>
context: fork
agent: media-producer
---
## Overview
Plan: $ARGUMENTS (project folder, product, target length, platforms such as YouTube, Shorts, Instagram, Etsy listing, email). Outputs: `<project folder>\media\promo-plan.md` and `rights-log.md`. Every Adobe step is written as manual steps with exact labels; no Adobe automation is assumed.

## When to use
A promo, launch video, Short or listing video for one of your products. Not for still product photos alone (ask media-producer for `photo-recipes.md`), not for brand look decisions (creative-director), not for licence interpretation (ip-researcher).

## Steps
1. Read `lessons\` and any motion, video or marketing notes in `knowledge\`. Ask the lead for your style bible and motion sheet paths; if none exist, mark motion values "proposal".
2. Shot list: one row per shot with purpose, framing, duration, source (render, photo, AI, stock, screen capture) and rights status. Total duration must equal the target length.
3. After Effects spec: per element class (logo sting, lower third, product reveal, end card), give duration, easing and a reduced-motion variant; reference the motion sheet or label "proposal".
4. Premiere: sequence settings matched to the source frame rate; export matrix rows per platform (16:9 master, 9:16, 4:5) with codec, resolution, frame rate, bitrate. Each number carries its platform, resolution, frame rate and fetch date from https://support.google.com/youtube/answer/1722171, https://support.google.com/youtube/answer/10059070, https://help.instagram.com/1631821640426723, https://help.etsy.com/hc/en-us/articles/115015663347. Every UI label is copied from https://helpx.adobe.com/premiere/desktop/render-and-export/export-files/export-video.html this run or marked "(label not verified)".
5. Rights log: one row per clip, image, track, font and AI asset with source, licence URL and allowed use; AI rows add tool, prompt, seed and terms URL. Any interpretation question becomes a numbered NEEDS MAKER item naming `ip-researcher`.
6. Disclosure: where "#ad" or an AI-content label sits, with a short quote from https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking and the platform's own disclosure page.
7. Facts fetched this run go to `research\inbox\<topic-slug>\<question-slug>.md` for `/verify`. Return both paths, inbox paths, NEEDS MAKER list, one next step.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I'll script Premiere through some plugin." | Manual steps with exact labels are reproducible by anyone; automation is your separate decision. |
| "1080p at 8 Mbps is the YouTube number." | Numbers carry their condition and fetch date, or they are wrong by default. |
| "The track is royalty-free, no row needed." | "Royalty-free" is a licence with terms. Row with URL, or the asset is cut. |
| "Disclosure can go in the description." | The FTC page warns that disclosures in easy-to-miss places do not work; quote it and place it accordingly. |

## Red flags
- Shot durations that do not sum to the target length.
- A rights log with fewer rows than assets in the shot list.
- A UI label without the helpx URL or the "(label not verified)" mark.

## Verification
- [ ] `promo-plan.md` and `rights-log.md` exist under `<project folder>\media\`.
- [ ] Shot durations sum to the target; every shot has a rights row.
- [ ] Every export number carries platform, resolution, frame rate, fetch date and URL.
- [ ] Disclosure placement quoted from the FTC page.
- [ ] Inbox paths returned; nothing written under `knowledge\`.
