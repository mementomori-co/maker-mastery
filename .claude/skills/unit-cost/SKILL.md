---
name: unit-cost
description: Use when a printed SKU needs a unit-cost sheet (filament grams x price, machine time, labour, packaging, fees, shipping) before pricing. Runs the business-strategist in a fresh context and writes a reproducible cost script, table and CSV with a source and date on every input.
argument-hint: <sku-slug> | <path to result.json or sliced .3mf> | <filament preset or product name> [project folder]
context: fork
agent: business-strategist
---
## Overview
Cost: $ARGUMENTS

Output on disk, in the project folder you name (default `work\costing\<sku-slug>\`): `unit-cost.md`, `unit-cost.py`, `unit-cost.csv`, and (if any input could not be fetched) `research\inbox\business\unit-cost-<sku-slug>.md`.

## When to use
Before any price is quoted or listed for a printed part. Not for garments (POD quotes belong in `/tech-pack`), not for MakerWorld earnings (`/makerworld-publish`).

## Steps
1. Locate the slice. If the argument is a `.3mf`, slice it with `.venv\Scripts\python.exe tools\slice_cli.py <file.3mf>` as described in `knowledge\02-bambu-studio\cli-slicing.md` and read `work\slice\<stem>\result.json`. No `result.json`, no sheet: stop and return "NEEDS: slice" with the exact command.
2. From `result.json` take grams per filament and print time; record the 3MF path, profile name and printer model (from `knowledge\00-gear-inventory\`) as the condition on those numbers.
3. Material price: fetch the filament's product page (https://us.store.bambulab.com/ or your regional Bambu store, or the vendor page for third-party spools) this run; record price per spool and net weight with the fetch date. Compute price per gram in the script, not by hand.
4. Machine time: inputs are printer purchase price, assumed service hours, maintenance per hour and electricity (printer draw x rate). Each is a fetched value with URL or a `NEEDS MAKER` placeholder in the inputs dict; never a silent default. Structure follows https://formlabs.com/blog/how-to-calculate-3d-printer-cost/.
5. Labour (rate `NEEDS MAKER`, minutes per unit from the batch plan), consumables, packaging (box, filler, label with vendor URL), shipping (fetch your carrier's service page, with weight and zone as the condition), channel fees (fetch https://www.etsy.com/legal/fees, https://www.shopify.com/pricing, or the MakerWorld terms pages).
6. Write `unit-cost.py`: an `INPUTS` dict where every entry carries `value`, `unit`, `condition`, `source_url`, `fetched`; functions per bucket; a margin table at three candidate prices after fees and shipping. Run it with `.venv\Scripts\python.exe`; it writes `unit-cost.md` and `unit-cost.csv`.
7. Any input marked "not verified" goes as a row into `research\inbox\business\unit-cost-<sku-slug>.md` for `/verify`. Return paths, the script's printed output, and numbered NEEDS MAKER questions.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Forty grams is a fair guess for a part this size." | Grams come from `result.json`. A guessed size can hide a print many times longer than planned. |
| "I know the spool price." | Prices change; fetch the product page this run and record the date. |
| "Labour at zero keeps it simple." | It hides the margin. Use a named `NEEDS MAKER` rate. |
| "I'll type the numbers into the table directly." | Every number in `unit-cost.md` is produced by `unit-cost.py`; otherwise it cannot be reproduced or audited. |

## Red flags (stop and fix)
- A number in the table that the script did not print.
- An input without URL and fetch date that is not marked `NEEDS MAKER` or "not verified".
- Grams or hours with no `result.json` path.
- A margin that omits fees or shipping.

## Verification
- [ ] `result.json` path and 3MF path recorded in `unit-cost.md`.
- [ ] `.venv\Scripts\python.exe <output folder>\unit-cost.py` runs clean; output pasted in the return.
- [ ] Every `INPUTS` entry has `source_url` and `fetched`, or is `NEEDS MAKER` / "not verified".
- [ ] Margin table shows three prices after fees and shipping.
- [ ] Inbox claims file written if anything is "not verified"; paths returned.
