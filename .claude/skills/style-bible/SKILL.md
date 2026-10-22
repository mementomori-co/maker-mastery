---
name: style-bible
description: Use when your brand's style bible must be created or revised (motifs, palette, typography, references, do/don't) or a sibling brand needs its section. Runs the creative-director in a fresh context and writes a versioned manual in the NASA 1976 standards-manual structure, with every fact routed to /verify.
argument-hint: <section | "v0.1" | "revise <section>"> | <brand-slug> [brand folder]
context: fork
agent: creative-director
---
## Overview
Build or revise: $ARGUMENTS

Output on disk, in your brand folder (default `work\brand\<brand-slug>\`, or the folder you name): `style-bible.md`, its `references.md`, one rendered moodboard with its script under `moodboards\`, and a claims table for `/verify`.

## When to use
A brand needs its visual law written down, or a shipped product exposed a gap in it. Not for voice and tone (a separate guide from the creative-director), not for a single product's art direction (write a brief under `<brand folder>\briefs\`), not for garment print files (`/tech-pack`).

## Steps
1. Read the existing `style-bible.md` if present; merge, never duplicate. Link facts from `knowledge\` instead of restating them.
2. Divergent pass: at least 20 motif or direction candidates in `<brand folder>\ideation\YYYY-MM-DD-<section>.md`, the chosen set marked with one line of reasoning each.
3. Write the manual in the structure of the 1976 NASA Graphics Standards Manual (https://www.nasa.gov/wp-content/uploads/2015/01/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf): 1 Identity (motifs, mark language, lockups, clear space); 2 Reproduction art (palette: hex, RGB, CMYK; Pantone only via an official Pantone source); 3 Typography (typefaces, each with licence URL and allowed uses: web, print, embossed, 3D-printed glyphs); 4 Packaging; 5 Publications and social; plus Mood, References (20 or more), Do/Don't, Changelog.
4. Every fact becomes a row in `research\inbox\brand\style-bible-<section>.md` (researcher table format), with the page to check: font licences https://helpx.adobe.com/fonts/web/font-licensing/font-licensing.html and https://openfontlicense.org/ofl-faq/; Pantone in Adobe apps https://helpx.adobe.com/illustrator/kb/pantone-color-books-illustrator.html; contrast https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html. In the manual, mark each such value `[pending /verify]` until a `research\verified\brand\...` path replaces the tag.
5. `references.md`: one row per reference with creator, URL, licence, fetched date. No credit, no row.
6. Render one moodboard headless: `<blender_exe> --background --python <brand folder>\moodboards\<slug>.py` (Blender from `config\paths.yaml`); open the PNG. If Blender is not configured, compose the board with Python instead and say so.
7. Append a dated `## Changelog` line. Return paths, the claims-table path for `/verify`, numbered NEEDS MAKER questions.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I know this font is open-licensed." | Fetch the licence page or tag it `[pending /verify]`. Recalled facts are where errors come from. |
| "Hex is enough; CMYK and Pantone can come later." | A palette without its reproduction values is not a standards manual. Fill every column or mark it open. |
| "Ten motifs are already great, skip the pass." | The divergent pass is the deliverable. Twenty candidates, then choose. |
| "The moodboard script is a detail." | Without the script beside it the board cannot be regenerated. |

## Red flags (stop and fix)
- A value in the manual with neither a `research\verified\` path nor a `[pending /verify]` tag.
- A reference row missing creator, URL, licence or date.
- A moodboard PNG that was not opened, or with no script beside it.
- A changed value with no changelog line.

## Verification
- [ ] `style-bible.md` exists in the brand folder with all NASA-structure sections and a `## Changelog` line for this run.
- [ ] Ideation file lists 20 or more candidates with the chosen ones marked.
- [ ] `references.md` has 20 or more rows, each with creator, URL, licence, fetched date.
- [ ] Moodboard PNG and its script exist side by side; the PNG was opened.
- [ ] Claims table written under `research\inbox\brand\` and its path returned.
