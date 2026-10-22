---
name: dfm-review
description: Use when an STL or part spec must be reviewed for FDM before slicing (orientation, plate face, overhangs, islands, bridges, material and assembly path). Runs the dfm-engineer in a fresh context and returns the review; the lead saves it beside the part.
argument-hint: "<stl path> [| mating part paths]"
context: fork
agent: dfm-engineer
---
## Overview
Input: $ARGUMENTS, an STL path, optionally mating-part paths. Output: the review in the reply (dfm-engineer has no Write tool), 50 lines or fewer.

## When to use
Every part before `/qa-gate` or `/preprint-check`, and after any geometry change from `cad-engineer` or `organic-modeler`.

## Steps
1. Measure with `.venv\Scripts\python.exe` plus trimesh/manifold3d: bounds, watertight, volume, bodies.
2. Overhang angle = angle between the face normal and -Z; a face is an overhang when it is **below** `support_threshold_angle` (read the value for your process profile from `knowledge\02-bambu-studio\support-settings.md` or with `tools\resolve_profile.py`). Table per candidate orientation; islands per layer; longest bridge. `tools\overhang_gate.py` can produce the per-z table.
3. Material pointer to `knowledge\03-materials\` (for example the HDT/Vicat table and the PLA vs PETG note). One material per part unless multi-material is the point. Assembly: interference at nominal and translation sweeps against mating parts; state the verdict. Splits only at natural part boundaries, with keyed joints.
4. Report: orientation, plate face and finish, supports (target none) with numbers, material, assembly, checks not run.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Another session already checked assembly." | No check counts without its script and output on disk. |
| "Slope or angle, same thing." | The convention is easy to invert; use the definition in step 2. |

## Red flags
- An orientation chosen without the overhang table.
- Writing into a folder listed in `protected_roots` in `config\paths.yaml`.

## Verification
- [ ] Numbers for overhang area, islands, bridges per orientation.
- [ ] Assembly verdict stated with the sweep that proves it.
- [ ] Checks not run listed.
