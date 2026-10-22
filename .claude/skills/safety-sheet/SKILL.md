---
name: safety-sheet
description: Use before you execute any plan that involves a laser, resin, urethane, silicone, solvent, wood dust, mains electricity or printer fumes. Runs the safety-officer in a fresh context and returns a PASS/FAIL safety sheet built from the exact SDS and official safety pages; the lead files it.
argument-hint: <activity> | <materials and equipment, exact product names> | <plan file path>
context: fork
agent: safety-officer
---
## Overview
Review: $ARGUMENTS (activity, exact materials and equipment, plan path). The safety-officer has no Write, Edit or Bash tool; it returns the sheet as text and the lead saves it to `<project folder>\safety\<activity>-safety-sheet.md`. The verdict is PASS or FAIL; a FAIL stops the plan.

## When to use
Any plan touching these hazard classes: a laser module, silicone or urethane casting, resin, solvents, sanding or cutting wood, mains wiring, or printing filaments with fume warnings. Not for low-voltage LED wiring alone (electronics-engineer, systems-engineer), not for print-file checks (`/preprint-check`).

## Steps
1. Read `lessons\` and the notes in `knowledge\44-safety\`, then the plan file. If a material or device is not named exactly, item 1 is FAIL "not named" and the review stops (never assume a product).
2. Per material: fetch the manufacturer's SDS for that exact product. Quote Section 8 (gloves by material, eye, respiratory, ventilation) and Section 4 (first aid); section layout per https://www.osha.gov/sites/default/files/publications/OSHA3514.pdf.
3. Per device: fetch the maker's safety page. Laser modules: quote the system class, the module class and the interlock statement from the manufacturer's product page and manual; FAIL any step that opens the enclosure or defeats an interlock while the laser can fire.
4. Wood dust: cite the page used at https://www.osha.gov/etools/woodworking. Fumes: cite the filament maker's page or SDS for the exact material; none found = "not verified" = FAIL.
5. Electrical: low-voltage items checked against the plan's datasheet rows (fusing, gauge, common ground); any mains-voltage item is NEEDS MAKER (a qualified person), never PASS.
6. Return the sheet in the safety-officer's output format: table (hazard, requirement, short quote, URL fetched, PASS/FAIL, one fix), emergency step, SDS-on-file list with the target path `<project folder>\safety\sds\<product>.pdf` (the SDS stays in your project, it is not committed to a public repo), verdict. One next step; questions numbered NEEDS MAKER.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Class 1 laser, nothing to review." | A laser system is Class 1 only with the enclosure and interlocks intact; the module inside is often Class 4. Quote both. |
| "Nitrile covers every resin." | Glove material comes from Section 8 of the exact SDS; conditions matter. |
| "I'll soften it to PASS with notes." | A gate returns PASS or FAIL. `print-qa` is not argued down and neither is this. |
| "The sibling product's SDS is close enough." | Exact product, or "not verified". |

## Red flags
- A PPE line without an SDS quote and a URL fetched this run.
- Mains work marked PASS.
- A verdict other than PASS or FAIL.
- The agent attempting to write a file.

## Verification
- [ ] Every item has quote, fetched URL, PASS/FAIL, one fix.
- [ ] Laser items quote system class, module class and interlock statement.
- [ ] Emergency step quoted from SDS Section 4 or the device manual.
- [ ] Mains items are NEEDS MAKER.
- [ ] Sheet returned as text with the target path for the lead; nothing written by the agent.
