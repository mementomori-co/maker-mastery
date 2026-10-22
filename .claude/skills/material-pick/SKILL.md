---
name: material-pick
description: Use when a part needs a filament choice with the numbers that justify it (HDT at both loads, drying, bed temperature, compatibility). Runs the materials-scientist in a fresh context and returns the recommendation with URLs; the lead saves it beside the part spec.
argument-hint: "<part and its environment>"
context: fork
agent: materials-scientist
---
## Overview
Input: $ARGUMENTS: the part and where it lives (heat, load, outdoors, contact with electronics). Output: a recommendation table in the reply (materials-scientist has no Write tool).

## When to use
Before a material is written into a part spec or a 3MF; whenever an environment changes.

## Steps
1. Read `knowledge\03-materials\` (the PLA vs PETG, HDT/Vicat and drying notes) and cite the notes and their URLs.
2. For anything missing, fetch the TDS or wiki page (Bash only for `curl -sL -A "Mozilla/5.0"` on HTTP 402/403) and queue the new fact to `/research-one`.
3. Table per candidate: HDT at 1.8 / 0.45 MPa (test condition), Vicat, the drying row for your AMS or dryer, bed temperature for your plate (`knowledge\00-gear-inventory\`), temperature class (low/high), verdict.
4. Recommend one material, named exactly (brand, line, colour where it matters) as a requirement; never assume it is loaded or owned. List alternatives with their costs and a "Not verified" list.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "69 C is the HDT." | Without the load it is PARTIAL; TDS values are for annealed or standard specimens, not your print. |
| "PLA is fine, it's indoors." | Check the vendor's softening figure; a closed enclosure with electronics inside is not room air. |

## Red flags
- A number without unit, load or URL.
- Mixing low-temp and high-temp classes in one job.

## Verification
- [ ] Every candidate row sourced.
- [ ] AMS or dryer limit and drying rows cited.
- [ ] One recommendation, alternatives, Not verified list.
