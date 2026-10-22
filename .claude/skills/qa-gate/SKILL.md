---
name: qa-gate
description: Use when a 3MF must be checked in code against the physical load record and the GUI-only slicer checks during a session (model-invocable variant of /preprint-check). Runs print-qa in a fresh context and returns the PASS/FAIL table; nothing prints on a FAIL.
argument-hint: "<path.3mf>"
context: fork
agent: print-qa
---
## Overview
Input: $ARGUMENTS, a 3MF path. Output: the PASS/FAIL table in the reply (print-qa has no Write tool); the lead saves it to `work\reports\proofs\` or the project's `_tests\` folder.

**No AI ever starts, sends, uploads or queues a print.** A PASS means the file may be shown to you; you press Print in Bambu Studio yourself.

## When to use
Before any 3MF is considered for printing, and when the lead needs the gate's verdict inside a running session. When you trigger the gate yourself, use `/preprint-check`; the two run the same agent and the same steps.

## Steps
1. Read `knowledge\00-gear-inventory\current-load.md`. If it is absent or has no `Verified:` date, the slots-recorded item FAILs and no filament item can PASS.
2. Read `templates\preprint-checklist.md` and count its items (15 in the shipped template).
3. Run, with `.venv\Scripts\python.exe` from the repo root: `tools\audit_3mf.py`, `tools\slice_cli.py` (or reuse a fresh slice in `work\slice\<stem>\` whose sha256 matches), then per plate `tools\gcode_audit.py`, `tools\tower_bounds.py`, `tools\tower_clearance.py --min-gap 8`; plus `tools\interface_coverage.py` on plates with support, `tools\stability_check.py` for display pieces and `tools\visible_ratio.py` for display or stream prints. Follow the full step list in `.claude\skills\preprint-check\SKILL.md`.
4. Fill the checklist item by item with the script line that proves each verdict and one fix per FAIL.
5. Return the table, the sha256 lines and the verdict.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "The GUI showed no warning." | The CLI does not surface every GUI warning (the prime-tower clearance warning never reaches `result.json`); only the scripts prove clearance. |
| "Nothing is loaded yet, skip the load item." | That item exists because a plate was once sliced for the wrong material. FAIL it. |
| "Another agent already checked this." | Independence is the point. Run the scripts yourself and quote them. |

## Red flags
- A PASS without a script line as evidence.
- Any write to the 3MF or to `knowledge\`.
- Any call that would send, upload or queue a print.

## Verification
- [ ] Every checklist item has PASS/FAIL plus evidence; row count equals the checklist's item count.
- [ ] Verdict stated; FAIL items each have one fix. Nothing prints on a FAIL.
