---
name: coupon
description: Use when a design number (clearance, bridge length, insert boss, wall, diffuser depth) is an assumption that a small print can measure. Runs test-coupon-designer in a fresh context and leaves coupon.py, coupon.stl and a blank measurement sheet under coupons\<slug>\ in the project folder.
argument-hint: <hypothesis with material, nozzle, process>
context: fork
agent: test-coupon-designer
---
## Overview
Design a coupon for: $ARGUMENTS

Output on disk, inside the project folder the maker names (default `work\coupons\<slug>\`): `coupon.py`, `coupon.stl`, `measurement-sheet.md`. The filled sheet later goes through `/verify` and `/file` into a calibration-and-testing note in `knowledge\`. This skill does not print, slice or file.

## When to use
Whenever `cad-engineer`, `dfm-engineer`, `organic-modeler` or `electronics-engineer` labels a value "assumed". Not for a value a TDS or wiki page states (use `/research-one`); not for flow or pressure-advance calibration (Bambu's own calibration pages on https://wiki.bambulab.com).

## Steps
1. Parse the hypothesis into variable, range and step, pass criterion, and constants (material, nozzle, process base `0.20mm Standard` for your printer unless stated, plate, orientation). If a constant is missing, ask it as a NEEDS MAKER question before writing geometry.
2. Glob the existing coupon folders for `coupon.py`; extend an existing coupon of the same variable instead of creating a second one.
3. Write `coupon.py` (parameters at the top, labelled steps, one body, STL export that prints bbox, volume, bodies, watertight) and run it with `.venv\Scripts\python.exe`.
4. Overhang check in the stated orientation against the threshold in `knowledge\02-bambu-studio\support-settings.md`; adjust geometry until self-supporting.
5. Write `measurement-sheet.md` with the constants header, the table `| step | nominal | measured | pass/fail | note |` and the filing path.
6. Return the three paths, the script's printed mesh stats and the hand-off line (`dfm-engineer`, then `bambu-studio-expert`, then `/preprint-check`). The maker prints it; no AI ever sends a print.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Measure clearance and bridge on one part." | Two variables, no filing. One coupon per variable. |
| "Skip /preprint-check for a 10-gram coupon." | Every print goes through the gate (`CLAUDE.md`). |
| "Write the expected result into the note now." | A number enters `knowledge\` only from a filled sheet via `/verify`. |

## Red flags
- A sheet missing a constant.
- Steps without embossed labels.
- An STL without `coupon.py` beside it.

## Verification
- [ ] `coupon.py`, `coupon.stl`, `measurement-sheet.md` exist in the coupon folder.
- [ ] Script output quoted: bbox, volume, bodies 1, watertight.
- [ ] Overhang check quoted against the profile threshold.
- [ ] Filing path and hand-off line in the reply.
