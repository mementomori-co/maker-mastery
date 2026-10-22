---
name: preprint-check
description: Use when a 3MF is claimed ready to print and before you send it to the printer yourself. Runs print-qa in a fresh context, which reads your load record, audits the 3MF, slices with the installed Bambu Studio CLI, runs the G-code checks and returns PASS/FAIL per pre-print checklist item.
argument-hint: <path.3mf>
context: fork
agent: print-qa
disable-model-invocation: true
---
## Overview
Check: $ARGUMENTS

Gate one 3MF against the physical machine state and the GUI-only slicer checks, in code. The output is the PASS/FAIL table in the reply; artifacts land in `work\slice\<stem>\` (`result.json`, `cli.log`, `out.3mf`, `plate_N.gcode`). Nothing prints on a FAIL. This skill never writes to the 3MF or to `knowledge\`.

**No AI ever starts, sends, uploads or queues a print.** This skill and the print-qa agent only judge the file. You review the table and press Print in Bambu Studio yourself.

All commands use the project Python, `.venv\Scripts\python.exe` (created by `tools\setup.ps1`), run from the repo root. The Bambu Studio path comes from `config\paths.yaml` (`bambu_studio_exe`) through `tools\mm_config.py`.

## When to use
After `bambu-studio-expert` hands over a 3MF, and before you print it. Also for an existing file you want judged. Not for designing or fixing the file (that is `bambu-studio-expert`), not for recording what is loaded (edit `knowledge\00-gear-inventory\current-load.md` yourself), and not for a mid-session check the lead wants on its own (that is `/qa-gate`, same agent).

## Steps
1. Read `knowledge\00-gear-inventory\current-load.md`. Missing, or no `Verified: YYYY-MM-DD` line: the slots-recorded item FAILs and no filament item can PASS. Continue the audit so the rest is known, but the verdict is already FAIL.
2. Read `templates\preprint-checklist.md` and count its items (15 in the shipped template). The table gets exactly one row per item, in order.
3. `.venv\Scripts\python.exe tools\audit_3mf.py $ARGUMENTS`. Quote the check lines you rely on.
   - Filaments in the project vs `current-load.md`, slot by slot (the "project filaments = physical filaments" item).
   - Grouping mode and filament map per plate (the grouping item).
   - Object bounding boxes vs the printable area of the extruder in use.
   - Support and bridge settings vs what the part spec planned.
   - More than one material family in one object, or colour painting: FAIL the one-material item unless the part spec says multi-material is the point. PLA + PETG in one object is FAIL in every case (weak bond).
   - Process preset other than the printer's default (the 0.20mm Standard profile on a 0.4 mm nozzle), an edited layer height, a Height range Modifier or variable layer height: FAIL unless the print sheet states a sourced reason; re-run with `--process-reason "<reason>"` so the line quotes it.
   - Stale slice (slice info, embedded G-code, md5 and project disagree): always FAIL; the fix is a re-slice with the installed CLI and a re-audit. An OK does not cover object, part, modifier or painting edits made after slicing.
4. `.venv\Scripts\python.exe tools\slice_cli.py $ARGUMENTS --debug 2` writes `work\slice\<stem>\result.json`, `cli.log` and `plate_N.gcode`. Read `result.json` (status, `warning_message` per plate, Support seconds per plate). Any warning is a FAIL on the "Sliced with the installed CLI" item. Support seconds must equal the plan (0 s when the spec says "no supports"). On Windows the CLI's terminal output can be lost, so an empty `cli.log` proves nothing; `result.json` and the scripts are the evidence.
5. Per plate, each with `.venv\Scripts\python.exe`:
   - `tools\gcode_audit.py <plate_N.gcode>` (points outside the X range, support extrusion, tool changes);
   - `tools\tower_bounds.py <plate_N.gcode>`;
   - `tools\tower_clearance.py <plate_N.gcode> --min-gap 8` (a prime-tower brim hull touching an object, or a gap under 8 mm, is FAIL; the reason is in `knowledge\02-bambu-studio\grouping-and-purge.md`).
   Any FAIL or WARN fails the X-range or prime-tower item with the measured gap or coordinate quoted, with two exceptions:
   - `gcode_audit.py`'s "bridge spans present" WARN belongs to the display-piece overhang item. It fires on nearly every plate, because this slicer labels bridging over sparse infill "Bridge" too. Judge it with `tools\overhang_gate.py` (down-facing area below the threshold at that z on a visible face) and a coupon row or written prediction.
   - `audit_3mf.py`'s "NOT VERIFIED" WARN on support Top Z belongs to the Top Z line of the display-piece item: every Top Z is "not verified" until your support-removal coupon is scored. Quote the gap that `tools\support_gap_readback.py` reads back instead.
6. Every plate with support ON: `.venv\Scripts\python.exe tools\interface_coverage.py <plate_N.gcode>`. Exit 2 (a visible overhang face, or one side of it, under 90 % interface coverage) is a FAIL with the region's z, side and % quoted. Exit 1 (the critical-regions or small-overhang filter is on, but every candidate reads at least 90 %) is reported as "coverage not guaranteed by the filter: read-back is the proof", not a FAIL.
7. Display pieces (anything that stands on its own): `.venv\Scripts\python.exe tools\stability_check.py` with the slicer grams (`--gcode` for parts with supports). Centre of mass outside the support polygon is FAIL. The tip-angle and contact thresholds are proposed, not verified.
8. Purpose: read the print's PURPOSE line from the print sheet (display, stream, functional, coupon). None stated = FAIL on the visible-ratio item. For a display or stream print, run `.venv\Scripts\python.exe tools\visible_ratio.py <plate_N.gcode> --out-prefix work\visible_ratio\<stem>-plate<N>` on every plate with support extrusion, quote the front and iso final ratios and the 25 / 50 / 75 % ratios, and open both PNGs. Exit 2 (below 0.60, proposed default) = FAIL whatever the coverage says; exit 1 (below 0.80) = FAIL unless the sheet gives a written reason. Functional and coupon prints PASS with "not applicable: <purpose>".
9. Tree support: for any plate with tree support, report each trunk's diameter at the plate and at z 50 mm, and the Branch diameter and Branch diameter angle from the G-code header. A long trunk wider than 12 mm at the plate with no written reason = FAIL. No tree support = "not applicable".
10. Print sheet: it must tell you to print the gated `_SLICED.3mf` directly without re-slicing, say what to do if Bambu Studio forces a re-slice (compare time and grams against the gated numbers; stop on a mismatch), and carry those gated numbers from `result.json`. Missing instruction or numbers = FAIL on the re-slice item.
11. Hash line: state the full `sha256` of the gated `_SLICED.3mf` and of each `plate_N.gcode`, each on the same line as its path.
12. Fill one row per checklist item, in order. The plate-face and time-and-grams items may be NEEDS MAKER when only you can confirm. One fix per FAIL. Return the table, the verdict line and the artifact paths.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "result.json says Success, skip the G-code." | The CLI does not report the prime-tower clearance warning in `result.json` (`knowledge\02-bambu-studio\cli-slicing.md`). Only the scripts prove clearance. |
| "The maker said in chat what is loaded." | Not a dated `current-load.md` = FAIL. A guessed filament type gets the wrong temperatures; ask or read the load file. |
| "Lower the gap to 7 mm, it fits." | The 8 mm rule exists because the slicer's own check ignores the brim (`knowledge\02-bambu-studio\grouping-and-purge.md`). The bar does not move inside a check. |
| "Support coverage is 100 %, so it passes." | Maximising one metric is never the only gate. A support cage that hides the part fails the visible-ratio item. |

## Red flags
- A PASS row without a quoted script line.
- A skipped script.
- Any edit to the 3MF or to a file under `knowledge\`.
- Any attempt to send, upload or queue the file to a printer.

## Verification
- [ ] `current-load.md` status stated with its `Verified:` date, or ABSENT.
- [ ] `audit_3mf.py`, `slice_cli.py`, `gcode_audit.py`, `tower_bounds.py`, `tower_clearance.py` outputs quoted with their paths (plus `interface_coverage.py`, `stability_check.py` and `visible_ratio.py` where they apply).
- [ ] Row count equals the checklist's item count; each row PASS / FAIL / NEEDS MAKER (plate face and time-and-grams only); one fix per FAIL.
- [ ] sha256 lines present for the gated 3MF and each plate's G-code.
- [ ] Verdict line present; artifact paths under `work\slice\<stem>\` returned. Nothing prints on a FAIL.
