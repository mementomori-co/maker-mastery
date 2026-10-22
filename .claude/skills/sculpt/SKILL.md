---
name: sculpt
description: Use when an organic shape (skull, character, flowing form) must be built or made printable in Blender headless (watertight, minimum wall, remeshed, split only at natural boundaries). Runs the organic-modeler in a fresh context and writes STL, script and report to the named folder.
argument-hint: "<output folder> | <description, size, min wall>"
context: fork
agent: organic-modeler
---
## Overview
Input: $ARGUMENTS as `<output folder> | <brief>`. Output: `<folder>\<name>.stl`, the Blender script beside it, and `report.md` (watertight, bounds, min wall, overhang map, split proposal).

Blender comes from `config\paths.yaml` (`blender_exe`) through `tools\mm_config.py`. If it is empty, stop and say Blender is not configured.

## When to use
Organic geometry. Not for hard-surface parts (`/cad-build`) and not for cleaning AI or scanned meshes (`/ai-mesh-clean`).

## Steps
1. Build in Blender headless (`<blender_exe> -b -P <script>`); voxel remesh; make watertight; thicken to the minimum wall.
2. Verify with `.venv\Scripts\python.exe` and trimesh (`is_watertight`, `is_volume`, bounds); estimate min wall by ray casting; overhang map per orientation against the overhang threshold in `knowledge\02-bambu-studio\support-settings.md`.
3. If no orientation prints clean, propose a split ONLY at natural part boundaries (separate characters, accessories, bases), with keyed joints (pins, sockets, pockets) and clearances from a printed coupon. Never a plane cut through a sculpture, a face, hair or the main body.
4. Save the script beside the STL; write `report.md`; return the path and numbers.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "It looks closed in the viewport." | Only `is_watertight` and `is_volume` count. |
| "1.2 mm is the usual minimum." | Minimum wall depends on material and nozzle; label it ASSUMED until a coupon measures it. |
| "A flat cut through the middle avoids all support." | Plane cuts through the sculpture are rejected. Split at natural boundaries or reorient. |

## Red flags
- Min wall stated without a method.
- Blender GUI steps instead of a saved script.
- A proposed split plane crossing the main body, a face or hair.

## Verification
- [ ] STL watertight and `is_volume`; height within 0.1 mm of spec.
- [ ] Min wall and overhang table in `report.md`.
- [ ] Any split is at a natural boundary with keyed joints.
