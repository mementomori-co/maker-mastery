---
name: ai-mesh-clean
description: Use when an AI-generated, scanned or sculpted mesh must become a printable STL (watertight, scaled, above min wall, split if needed) with a licence record. Runs the mesh-capture-specialist in a fresh context through import, remesh, decimate, thickness audit, split and export, reporting before/after stats.
argument-hint: <raw mesh path> | <target max dimension mm> | <min wall mm @ material, nozzle> [asset-slug]
context: fork
agent: mesh-capture-specialist
---
## Overview
Clean for print: $ARGUMENTS

Output on disk, inside the project folder the maker names (see `templates\project\`): `assets\<asset-slug>\clean\<asset>.stl` (one per print part), `clean.py` beside them, `assets\<asset-slug>\LICENCE.md`, and `assets\<asset-slug>\report.md` with the before/after table.

## When to use
Any mesh that did not come from code-CAD and is headed for one of your printers (`knowledge\00-gear-inventory\`): AI text- or image-to-3D output, a photogrammetry reconstruction, a Blender sculpt. Not for render topology (`/retopo`), not for the print orientation and support verdict (`dfm-engineer` after this), not for slicing (`bambu-studio-expert`, then `/preprint-check`).

## Steps
1. Licence gate. `LICENCE.md` must exist with service, tier, terms URL fetched this run and dated, prompt/inputs, job id. If the mesh was generated now, fetch the service's terms or pricing page first. Not fetchable: write `licence: not verified` in the file and add a row to `research\inbox\ai-to-3d\<asset-slug>.md`.
2. Min wall must arrive with its condition (material, nozzle) from `materials-scientist` or a note in `knowledge\03-materials\`. A bare number: stop and return `NEEDS: min wall @ material, nozzle`.
3. Before stats with `.venv\Scripts\python.exe` and `trimesh`: faces, components, `is_watertight`, `is_volume`, volume mm^3, bbox mm, unit assumption. Copy the raw file to `raw\` untouched.
4. Write `clean.py` for `<blender_exe> --background --python clean.py -- <raw> <target mm> <min wall mm> <out dir>` (`blender_exe` from `config\paths.yaml`; empty means Blender is not configured, so stop and say so). One function per step: scale to target, voxel remesh (voxel size chosen against the min wall and printed), decimate to a stated face budget, recalculate normals, 3D-Print Toolbox checks (solid, intersections, thickness at the min wall; https://extensions.blender.org/add-ons/print3d-toolbox/), split into parts if thickness fails or the part exceeds the plate, export STL per part.
5. After stats per part, same columns as step 3, plus min wall measured (state the method: Toolbox thickness check or trimesh ray-cast sampling) and faces below it. Every `clean\*.stl` must report `is_watertight == True` and `is_volume == True`.
6. Write `report.md`: before/after table, every parameter, licence status, a split and orientation proposal for `dfm-engineer`. Splits follow natural part boundaries only (separate characters, accessories, bases), never a plane through a face or main body. Slicer-side notes (Fix Model, Arc Fitting on noisy meshes) are links to `knowledge\02-bambu-studio\` or https://wiki.bambulab.com/en/software/bambu-studio/fix-model, not restated.
7. Return paths, the table, licence status and numbered NEEDS MAKER questions (including service authorisation if a generation service was requested).

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "Free tier means free to sell." | Terms say what is permitted. Fetch and quote them in `LICENCE.md` before touching the mesh. |
| "It looks closed in the viewport." | `is_watertight` and `is_volume` from trimesh plus the Toolbox check decide, not a screenshot. |
| "1.2 mm min wall is fine for everything." | Min wall depends on material and nozzle; a bare number is rejected. |
| "I'll patch the last hole in the GUI." | `clean.py` is the record; a GUI fix is lost the next time the part is regenerated. Add the step to the script and re-run. |
| "Components before equals parts after." | Separate numbers, separate sentences. |

## Red flags (stop and fix)
- No `LICENCE.md`, or one without fetched URL and date.
- A `clean\*.stl` with `is_watertight` false or `is_volume` false.
- Min wall reported without method, material and nozzle.
- Output written into a folder listed in `protected_roots` in `config\paths.yaml`.

## Verification
- [ ] `LICENCE.md` present with service, tier, terms URL (fetched, dated), inputs, job id.
- [ ] `report.md` before/after table: faces, components, watertight, volume mm^3, bbox mm, min wall mm (method), faces below min wall, per part.
- [ ] Every `clean\*.stl`: `is_watertight == True` and `is_volume == True` printed by the venv Python this session.
- [ ] `clean.py` beside the STLs, run this session, parameters listed.
- [ ] Paths returned; split/orientation proposal handed to `dfm-engineer`; NEEDS MAKER questions numbered.
