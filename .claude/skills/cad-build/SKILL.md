---
name: cad-build
description: Use when a part must be built or regenerated in code-CAD (manifold3d/trimesh in the project venv, or Fusion 360) with its source saved beside the STL, geometric checks and a render. Runs the cad-engineer in a fresh context and writes to the project folder named in the arguments.
argument-hint: "<output folder> | <spec or reference STL (read-only)>"
context: fork
agent: cad-engineer
---
## Overview
Input: $ARGUMENTS, as `<output folder> | <spec>`. Output: `<folder>\<part>.py`, `<part>.stl`, `render.png`, `report.md` (measured vs regenerated, checks).

## When to use
New parts, regenerations from a spec, or fixes to a part whose source exists (read the source first; never write into a folder listed in `protected_roots` in `config\paths.yaml`). Not for organic shapes (`/sculpt`).

## Steps
1. If a reference STL or source is named, measure or read it first with `.venv\Scripts\python.exe` (trimesh). Parameters at the top of the script, one function per feature.
2. Export the STL. Checks: watertight, `is_volume`, bounds and volume against the reference, distinct generated points, interference / swing / slide-in where mating parts are given.
3. Render the real STL with Blender headless (`<blender_exe> -b -P <script> -- ...`, `blender_exe` from `config\paths.yaml`; if it is empty, say the render was not done).
4. Write `report.md`; return the folder path and check summary.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "I'll save the script later." | A part whose script was never saved cannot be regenerated or fixed. Script first, STL second. |
| "Nearest vertex is close enough." | Snapping to the nearest vertex can merge distinct features into pairs. Use the nearest point on the edge, then a uniqueness check. |

## Red flags
- An STL without a `.py` beside it.
- A boolean result that is not `is_volume`.

## Verification
- [ ] `.py`, `.stl`, `render.png`, `report.md` in the folder.
- [ ] Checks listed with numbers; any failed check named.
