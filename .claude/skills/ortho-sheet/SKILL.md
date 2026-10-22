---
name: ortho-sheet
description: Use when a model needs a dimensioned orthographic reference sheet or turnaround (front/back/left/right/top/bottom) that can be loaded as Blender Image Empties or handed to a factory. Runs the surfacing-artist in a fresh context, renders headless at a stated mm-per-pixel scale and measures the deviation.
argument-hint: "<model path> | <views: 4 | 6> | <sheet width px> [project folder]"
context: fork
agent: surfacing-artist
---
## Overview
Orthographic sheet for: $ARGUMENTS

Output on disk, in the project folder you name (see `templates\project\`), or `work\ortho\<model-stem>\` if none is given: `<model-stem>_ortho.png`, the per-view PNGs, `ortho.py` beside them, and `ortho.md` (scale, views, bar deviation, Image Empty load notes).

Blender comes from `config\paths.yaml` (`blender_exe`) through `tools\mm_config.py`. If it is empty, stop and say Blender is not configured.

## When to use
A model exists (STL/OBJ/GLB/.blend) and someone needs true proportions: a modeler, a factory, a tech pack, a CAD rebuild. Not for a look-dev or hero render (surfacing-artist render output), not when the model must first be made watertight (`/ai-mesh-clean`).

## Steps
1. Measure the model with `.venv\Scripts\python.exe` and `trimesh`: bounding box in mm (NEEDS MAKER if the unit is unknown), centroid, face count. Folders listed in `protected_roots` in `config\paths.yaml` are read only.
2. Write `ortho.py` for `<blender_exe> --background --python ortho.py -- <model> <views> <width px> <out dir>`: import, centre, one orthographic camera per view with `ortho_scale` = largest bbox extent for that view + 10 % margin, flat neutral material and even lighting, a dimension bar object of known length (for example 50 mm) in frame, transparent or white background. Compute and print mm-per-pixel = `ortho_scale / width px`.
3. Render each view; composite the sheet (Blender compositor or a second headless pass) with view labels, the mm-per-pixel value and the bar length printed on the sheet.
4. Verify scale: read the bar's pixel length from the rendered PNG, convert with the stated mm-per-pixel, report deviation %. The bar is 2 % or less (house target).
5. Open the sheet PNG with the Read tool. Write `ortho.md`: scale, views, bar deviation, and how to load each view as an Image Empty with matching size per https://docs.blender.org/manual/en/latest/modeling/empties.html.
6. Return paths, the deviation %, and one line describing what the sheet shows.

## Common rationalizations
| Rationalization | Reality |
|---|---|
| "A far perspective camera is close enough." | Perspective foreshortens; a sheet without an orthographic camera and a stated mm-per-pixel cannot be loaded at 2 % deviation or less. |
| "The scale is right by construction, skip the bar." | Measure the bar in pixels. A scale you have not measured is a claim, not a fact. |
| "The model is roughly 120 mm." | Read the bbox from trimesh and state the unit. Eyeballed counts and sizes are how numbers go wrong. |
| "Render ran, sheet done." | Open the PNG. A preview you did not look at has misled builds before. |

## Red flags (stop and fix)
- No dimension bar in frame, or its measured deviation not reported.
- mm-per-pixel missing from the sheet or `ortho.md`.
- Output written into a protected root.
- Sheet PNG never opened.

## Verification
- [ ] `ortho.md` states bbox mm, mm-per-pixel, views rendered and bar deviation % (2 % or less, or the failure stated).
- [ ] Sheet PNG and per-view PNGs exist beside `ortho.py`; the script was run this session.
- [ ] Sheet PNG opened and described in one line.
- [ ] Image Empty load notes present with the manual URL.
- [ ] Paths returned.
