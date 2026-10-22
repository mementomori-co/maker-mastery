---
name: tech-pack
description: Use when a garment design for your apparel line must become a factory- or POD-ready tech pack (artwork files, placements, colourways, BOM, labels, size spec, QC points). Runs the creative-director in a fresh context and writes the pack with provider file specs and FTC label elements quoted from fetched pages.
argument-hint: "<garment-slug> | <design file path> | <method: pod | cut-and-sew | undecided> [brand folder]"
context: fork
agent: creative-director
---
## Overview
Tech pack for: $ARGUMENTS

Output on disk, in your brand folder (default `work\brand\<brand-slug>\`): `tech-packs\<garment-slug>\tech-pack.md`, an `artwork\` folder with print files at the fetched spec, `check_artwork.py` beside them, and a claims table `research\inbox\apparel\tech-pack-<garment-slug>.md` for `/verify`.

## When to use
A garment is leaving the sketch stage for a POD provider or a cut-and-sew factory. Not for the brand's visual law (`/style-bible`), not for the garment's cost or channel (`business-strategist`), not for IP clearance of the artwork (`/ip-check` first).

## Steps
1. Read the brand's `style-bible.md` and voice guide if present, and any apparel notes in `knowledge\` (link, do not restate). Existing material you point to is read only.
2. Fetch this run: Printful file guidelines https://help.printful.com/hc/en-us/articles/50264019148177; the Printify print-file requirements page under https://help.printify.com/ (record the exact URL fetched); the FTC textile labelling guide https://www.ftc.gov/business-guidance/resources/threading-your-way-through-labeling-requirements-under-textile-wool-acts. Record format, colour space, DPI, pixel dimensions per placement and the required label elements, each with page date (short quotes, paraphrase the rest).
3. Print-method section: DTG vs screen vs embroidery, with the conditions each fetched page states (minimums, fabric, colour limits, minimum text size). Undecided becomes numbered NEEDS MAKER (quantity, blank, budget).
4. Pack structure: cover (brand, style number, season); flats front and back (from `/ortho-sheet` if a 3D garment exists, else vector flats); placements with dimensions in mm and inches from named garment reference points; colourways (hex from the style bible plus ink or thread references); BOM (blank SKU, vendor URL, label stock); label artwork and placement with the FTC elements marked "facts, not legal advice"; size spec table; packaging; QC points.
5. Artwork files: export to `artwork\` at the recorded spec. Write `check_artwork.py` (run with `.venv\Scripts\python.exe`) that reads each PNG's width, height and bit depth from the IHDR chunk and compares against the spec table; paste its output in the pack.
6. Facts (specs, label elements, method limits) also go into the claims table for `/verify`; mark them `[pending /verify]` in the pack until a `research\verified\apparel\...` path exists.
7. Return paths, `check_artwork.py` output, claims-table path, NEEDS MAKER questions.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "300 DPI is the universal rule." | Each provider states its own spec per product and placement. Cite the fetched page with date. |
| "The label just needs the brand name." | Record the FTC elements from the fetched guide; what is missing is a fact with a URL, and the decision is yours (and your attorney's). |
| "I can eyeball the placement." | Placements are dimensions in mm and inches from named reference points, or the factory guesses. |
| "The PNG exported, it must match the spec." | Run `check_artwork.py`. Exported-but-wrong files pass a glance and fail at the printer. |

## Red flags (stop and fix)
- A spec or label element without a fetched URL and date.
- Artwork in `artwork\` that `check_artwork.py` flags or that was never checked.
- A placement without numeric dimensions.
- Hex values that are not in the style bible and not marked as a new colourway proposal.

## Verification
- [ ] Printful, Printify and FTC pages fetched this run; URLs and dates in the pack.
- [ ] `check_artwork.py` run; every file in `artwork\` passes or is listed as failing with the reason.
- [ ] Every placement has mm and inch dimensions from a named reference point.
- [ ] Claims table written under `research\inbox\apparel\`; path returned.
- [ ] NEEDS MAKER questions numbered.
