---
name: retopo
description: Use when a high-poly or scanned mesh needs clean quad-dominant topology for texturing, rigging or rendering. Runs the surfacing-artist in a fresh context, retopologises headless in Blender with Shrinkwrap to the source, and reports face counts and deviation in mm.
argument-hint: "<high-poly mesh path> | <target face count> | <use: render | game | texture> [project folder]"
context: fork
agent: surfacing-artist
---
## Overview
Retopologise: $ARGUMENTS

Output on disk, in the project folder you name (see `templates\project\`), or `work\retopo\<model-stem>\` if none is given: `<model-stem>_lo.obj` (plus `.blend`), `retopo.py` beside it, and `retopo.md` with the before/after table and deviation.

Blender comes from `config\paths.yaml` (`blender_exe`) through `tools\mm_config.py`. If it is empty, stop and say Blender is not configured.

## When to use
The mesh will be textured, rigged or rendered and its topology is noisy (sculpt, scan, AI output). Not when the goal is a print: watertightness and minimum wall matter there, not quads; use `/ai-mesh-clean`. Not for a reference sheet (`/ortho-sheet`).

## Steps
1. Before stats with `.venv\Scripts\python.exe` and `trimesh`: faces, tri/quad/ngon counts, components, `is_watertight`, bbox in mm. If the "use" field says print, stop and return "use /ai-mesh-clean".
2. Write `retopo.py` for `<blender_exe> --background --python retopo.py -- <hi path> <target faces> <out dir>`. Method per https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html: build the low-poly (remesh to a quad-dominant base, then reduce to the target), Shrinkwrap it to the high-poly, apply, recalculate normals. Record every parameter the script uses in `retopo.md`.
3. Deviation: sample the low-poly vertices against the high-poly surface with `trimesh.proximity.closest_point`; report max and mean distance in mm and the percentage of samples above 0.5 % of the bbox diagonal.
4. After stats, same columns as step 1, plus quad %, non-manifold edge count, UV status (none, or unwrapped with seams noted).
5. Render one shaded view of lo and hi side by side (headless; script beside the PNG) and open the PNG.
6. Write `retopo.md`; return paths, the before/after table, deviation numbers and anything the target could not meet.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Decimate to the target count and ship it." | Decimate leaves triangles and no loops. Report face-type counts; the target is quad-dominant topology, not a face count. |
| "Shrinkwrap applied, so it matches the source." | Measure it. Max and mean deviation in mm, or the report is an opinion. |
| "I'll tweak it in the Blender GUI." | GUI edits leave no record; `retopo.py` is the record. A model whose source script was lost cannot be rebuilt. |
| "The comparison render ran, no need to look." | Open the PNG. A preview you did not look at has misled builds before. |

## Red flags (stop and fix)
- A report with a face count but no tri/quad/ngon split.
- Deviation missing or given without unit.
- Output written into a folder listed in `protected_roots` (the guard hook blocks it).
- A PNG never opened.

## Verification
- [ ] `retopo.md` has before/after rows: faces by type, components, watertight, bbox mm, quad %, non-manifold edges.
- [ ] Max and mean deviation in mm reported from `trimesh.proximity.closest_point`.
- [ ] `retopo.py` beside the outputs and run this session with the parameters listed.
- [ ] Comparison PNG exists, was opened, and is described in one line.
- [ ] Paths returned.
