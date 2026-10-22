# 07 - Tools reference

Every tool in [`tools/`](../tools/): what it does, what it reads, what it writes, an example command and a sample of
its output. Next: [08 - Customize](08-customize.md).

How to run a tool: in the VS Code terminal (**Terminal > New Terminal**), from the project folder, with the project's
Python:

```powershell
.venv\Scripts\python.exe -B tools\<tool>.py <arguments>
```

`-B` stops Python writing `__pycache__` folders. Every tool prints its full help with `--help`, and every file starts
with a docstring that explains it in detail. Usually you do not run these yourself: Claude and the agents run them and
quote the output to you.

**Exit codes** follow one pattern in the checking tools: `0` OK, `1` WARN (look at it), `2` FAIL (do not print),
`3` unreadable input or bad arguments. Exceptions are noted per tool.

**Samples:** the outputs below were produced by running the shipped tools on small synthetic files (no Bambu Studio, no
printer). Long outputs are cut; the full samples are in [tool-sample-outputs.md](tool-sample-outputs.md). `<tmp>`,
`<repo>` and `<fixture-tmp>` stand for the folders used in that run. The dates in the samples are test values.

No tool here starts, sends, uploads or queues a print.

## Overview

| Tool | Area | One line |
|---|---|---|
| [setup.ps1](#setupps1) | setup | Creates `.venv`, installs the requirements, copies the config, runs the self-test |
| [selftest.py](#selftestpy) | setup | Runs every unit test and says, tool by tool, whether it works on this PC |
| [mm_config.py](#mm_configpy) | setup | Reads `config\paths.yaml`; prints the resolved paths |
| [slice_cli.py](#slice_clipy) | slicing | Slices a 3MF with your installed Bambu Studio command line |
| [audit_3mf.py](#audit_3mfpy) | 3MF | Checks a 3MF's settings, grouping, load and freshness (C1-C16) |
| [resolve_profile.py](#resolve_profilepy) | profiles | Resolves a Bambu Studio profile's inheritance and prints effective values |
| [gcode_paths.py](#gcode_pathspy) | G-code | Reads plate G-code into paths per layer and feature, arcs included |
| [gcode_audit.py](#gcode_auditpy) | G-code | Extents, tool changes, support and bridge report |
| [tower_bounds.py](#tower_boundspy) | G-code | Measures the prime tower footprint |
| [tower_clearance.py](#tower_clearancepy) | G-code | Gap between the prime tower and every object |
| [support_gap_readback.py](#support_gap_readbackpy) | G-code | The support Top Z gap actually sliced |
| [interface_coverage.py](#interface_coveragepy) | G-code | How much of each overhang has support under it |
| [visible_ratio.py](#visible_ratiopy) | G-code | How much of a display print the support hides |
| [overhang_gate.py](#overhang_gatepy) | STL | Overhang area, cantilever and floating islands per part |
| [stability_check.py](#stability_checkpy) | STL | Does a display piece tip over |
| [stability_render.py](#stability_renderpy) | STL | Blender helper for the stability check's pictures |
| [render_critic.py](#render_criticpy) | images | Scored critique of a still render |
| [check_note.py](#check_notepy) | knowledge | Validates a knowledge note's format (also a hook) |
| [check_skill.py](#check_skillpy) | agents | Lints skill and agent files |
| [build_indexes.py](#build_indexespy) | knowledge | Regenerates `knowledge\INDEX.md` and `lessons\INDEX.md` |
| [privacy_scan.py](#privacy_scanpy) | sharing | Finds personal data before you publish |
| [strip_metadata.py](#strip_metadatapy) | sharing | Removes personal metadata from images and 3MF files |
| [hooks\session_start.py](#hookssession_startpy) | hook | Loads the lessons at session start |
| [hooks\guard_paths.py](#hooksguard_pathspy) | hook | Blocks writes into protected folders |
| [hooks\log_run.py](#hookslog_runpy) | hook | Logs finished subagents to `work\agent-runs.log` |
| [mcp\mm_audit_server.py](#mcpmm_audit_serverpy) | MCP | Read-only audit server for Claude Code (optional) |
| [mcp\tower_clearance_3mf.py](#mcptower_clearance_3mfpy) | MCP | Tower clearance read from inside a sliced 3MF |

---

## Setup

### setup.ps1

- **What it does:** one-time setup. Finds Python 3.12 or newer (`py -3.12`, then `py -3`, then `python`), creates
  `.venv` in the project and installs `requirements.txt` into it after asking Y/N (with `-c constraints.txt`, which
  fixes every package, transitive ones too, to the versions of a tested fresh install), copies `config\paths.example.yaml` to
  `config\paths.yaml` if you have none, looks for Bambu Studio (read-only), and runs `selftest.py`. It changes nothing
  outside the project folder.
- **Inputs:** `-Yes` answers the install question; `-Optional` also installs `requirements-optional.txt` (open3d).
  `requirements-optional.txt` pins open3d itself (`open3d==0.20.0`), but `constraints.txt` does not list open3d or the
  packages open3d pulls in, so those extra packages are not pinned: pip picks their versions on the day you install.
- **Outputs:** `.venv\`, `config\paths.yaml`, the self-test table. Exit code: the self-test's.
- **Example:** `powershell -ExecutionPolicy Bypass -File .\tools\setup.ps1` (why this form: [04 - First run](04-first-run.md#step-4-run-the-setup-script)).

### selftest.py

- **What it does:** runs each `tools\tests\test_*.py` file (15 files, 229 checks) in its own process and prints one line
  per tool: PASS, FAIL or SKIPPED (an optional package is missing). No test needs Bambu Studio, Blender or the internet.
- **Inputs:** none; `--verbose` prints the full test output.
- **Outputs:** the table; exit 0 when nothing failed, 1 when a test failed.
- **Example:** `.venv\Scripts\python.exe -B tools\selftest.py`

```text
Self-test: 15 test files, Python 3.12.10 at <repo>\.venv\Scripts\python.exe
Nothing here prints, slices or sends anything.

  PASS    audit_3mf.py - slicer-setting checks C1-C16  (41 checks, 0.8 s)
  PASS    audit_3mf.py - load check against your current-load.md (C7)  (25 checks, 0.4 s)
  PASS    mm_config.py, resolve_profile.py, slice_cli.py guards, check_note.py, check_skill.py, build_indexes.py  (35 checks, 1.7 s)
  PASS    gcode_audit.py - extents, support and bridge report  (9 checks, 1.0 s)
  PASS    gcode_paths.py - G-code reader with arcs  (14 checks, 0.1 s)
  PASS    hooks\guard_paths.py, hooks\session_start.py, hooks\log_run.py - Claude Code hooks  (17 checks, 5.7 s)
  PASS    interface_coverage.py - support under visible overhangs  (9 checks, 9.8 s)
  PASS    mcp\mm_audit_server.py - read-only audit MCP server  (2 checks, 2.6 s)
  PASS    overhang_gate.py - overhangs, cantilever and islands  (10 checks, 4.7 s)
  PASS    privacy_scan.py - personal-data scan  (24 checks, 0.3 s)
  PASS    render_critic.py - render critique (needs optional open3d)  (12 checks, 11 skipped, 2.7 s)
  PASS    stability_check.py - does a display piece tip over  (9 checks, 1.0 s)
  PASS    support_gap_readback.py - printed support Top Z gap  (6 checks, 3.5 s)
  PASS    tower_bounds.py, tower_clearance.py, mcp\tower_clearance_3mf.py - prime tower  (7 checks, 0.9 s)
  PASS    visible_ratio.py - how much of the part support hides  (9 checks, 1.7 s)

RESULT: PASS - every tool that could be tested works on this PC.
```

(Captured from a full fresh install by `tools\setup.ps1`, answering `y`, without `-Optional`: PyYAML is installed, so
the third line runs all 35 checks, and open3d is not, so the render_critic line skips 11 of its 12 checks.) With
open3d installed (`-Optional`), the render_critic line runs all its checks, for example:

```text
  PASS    render_critic.py - render critique (needs optional open3d)  (12 checks, 19.1 s)
```

On a Python without PyYAML the third line reads `(35 checks, 2 skipped, ...)`: the 2 skipped checks are the
PyYAML-only config tests. Times vary from PC to PC.

Before the packages are installed (you answered N in setup), most lines read `SKIPPED`, for example
`SKIPPED audit_3mf.py - slicer-setting checks C1-C16  (1 checks, 1 skipped, 0.2 s)`, and the result is still `PASS`.

### mm_config.py

- **What it does:** the one place every tool reads machine paths from. Run on its own, it prints the resolved
  configuration and marks paths that do not exist.
- **Inputs:** `config\paths.yaml` (or `config\paths.example.yaml` if you have no copy yet); the `MM_CONFIG` environment
  variable can point to another file. Uses PyYAML when installed, else a small built-in reader for the simple format.
- **Outputs:** text; other tools import its functions (`repo_root()`, `load()`, `path()`, and more).
- **Example:** `.venv\Scripts\python.exe -B tools\mm_config.py`

```text
config: <fixture-tmp>\paths.yaml
repo_root: <repo>
bambu_studio_exe: <fixture-tmp>\no-such-dir\bambu-studio.exe  [does not exist]
bambu_profiles_dir: <fixture-tmp>\profiles
blender_exe: (empty)
slice_workdir: <repo>\work\slice  [does not exist]
allowed_roots: ['<repo>']
protected_roots: []
bambu profile roots: ['<fixture-tmp>\\profiles']
```

## Slicing and profiles

### slice_cli.py

- **What it does:** copies your 3MF to `work\slice\<name>\in.3mf`, runs the Bambu Studio command line
  (`--slice 0 --export-3mf out.3mf --outputdir <dir>`), and summarises `result.json` per plate. It only slices. A lock
  stops two runs from sharing a folder, and it refuses to overwrite gated print files.
- **Inputs:** a 3MF; `bambu_studio_exe` and `slice_workdir` from `config\paths.yaml` (or `--exe`, `--outdir`);
  `--debug`, `--timeout`, `--json`, `--allow-overwrite`.
- **Outputs:** `out.3mf`, `plate_N.gcode`, `result.json`, `cli.log` in the work folder; a summary. Exit 0 clean,
  1 warnings found, 2 slice failed or Bambu Studio not found, 3 gated-file guard fired.
- **Important:** some slicer warnings never reach `result.json`, and the command line's own log can be lost on Windows,
  so a clean run is not a pass: run the audits too.
- **Example:** `.venv\Scripts\python.exe -B tools\slice_cli.py work\bracket\bracket.3mf`

What you see when Bambu Studio is not where the config says:

```text
bambu-studio.exe not found at '<fixture-tmp>\\no-such-dir\\bambu-studio.exe': set bambu_studio_exe in config\paths.yaml or pass --exe
(exit code 2)
```

### resolve_profile.py

- **What it does:** Bambu Studio's profiles inherit from parents and templates, so the leaf file rarely holds the value
  you care about. This prints the effective value of each key and which file set it.
- **Inputs:** `--kind process|machine|filament`, a profile name, `--keys`; profiles from `bambu_profiles_dir` or the
  installed copies (`--root` overrides). Read-only.
- **Outputs:** the chain and values (or `--json`). Exit 0, or 1 when a profile is not found.
- **Example:** `.venv\Scripts\python.exe -B tools\resolve_profile.py --kind process "0.20mm Standard @BBL H2C" --keys max_bridge_length support_threshold_angle`

```text
=== Sample 0.20mm
  chain: Sample 0.20mm -> Sample Common
  max_bridge_length = '0'   (set in: Sample Common)
  wall_loops = '3'   (set in: Sample 0.20mm)
```

## 3MF audit

### audit_3mf.py

- **What it does:** opens a Bambu Studio 3MF read-only and prints one OK / WARN / FAIL line per check: filament grouping
  (C1, C2), bridges and support (C3, C4), the prime tower (C6), your physical load (C7), filament-printer compatibility
  (C8), bed temperature for the plate (C9), 100 % infill (C10), changes against the source 3MF (C11), ironing and top
  pattern (C12), support Top Z (C13), one material per object (C14), the process preset (C15) and whether the sliced
  G-code matches the project (C16).
- **Inputs:** a 3MF; `knowledge\00-gear-inventory\current-load.md` (or `--load-note`); the installed Bambu Studio
  profiles; options `--json`, `--today`, `--load-max-age-days`, `--source`, `--process-reason` and others (see `--help`).
- **Outputs:** the report; exit 0 all OK, 1 warnings, 2 fails (64 for a malformed `--approve-swap`).
- **Example:** `.venv\Scripts\python.exe -B tools\audit_3mf.py work\slice\bracket\out.3mf`

Against the shipped, empty load template (C7 fails on purpose until you record your load):

```text
3MF audit: part.3mf
  printer=Bambu Lab H2C 0.4 nozzle  process=0.20mm Standard @BBL H2C  bed=Textured PEI Plate
  filament 1: GFA00 PLA #000000FF (Bambu PLA Basic @BBL H2C)
  [OK] C3: max_bridge_length = 10
  [FAIL] C7: L1: load_template.md has no valid 'Verified: YYYY-MM-DD' (MISSING) - undated load = unknown load
  [FAIL] C7: L3: filament 1 'Bambu PLA Basic @BBL H2C' (GFA00, #000000): product 'Bambu PLA Basic' is not loaded on 'H2C' (loaded: nothing parsed)
  [OK] C14: one material family per object (1 object(s) checked: parts, modifiers and per-feature filament keys)
  [OK] C15: process preset '0.20mm Standard @BBL H2C' = the printer's default, layer_height 0.2; no process key modified
VERDICT: FAIL
(exit code 2)
```

The same file against a filled-in load record:

```text
  [OK] C7: L1: load_filled.md Verified: 2026-01-08 (2 day(s) before 2026-01-10)
  [OK] C7: L3: filament 1 'Bambu PLA Basic @BBL H2C' filament_ids 'GFA00' vs 'GFA00' for Bambu PLA Basic; load row | H2C - AMS 2 Pro slot 1 (RIGHT inlet) | **Bambu PLA Basic, Black** | looked at the AMS screen |
  [OK] C7: L7: curr_bed_type 'Textured PEI Plate' vs load row | H2C - plate on the bed | Textured PEI | looked at the bed |
  [WARN] C8: filament 1 profile 'Bambu PLA Basic @BBL H2C' not found in the installed profiles (checked system BBL, user presets, install folder) - compatibility unproven
VERDICT: WARN
(exit code 1)
```

(The C8 WARN appears because the sample run had no Bambu Studio profiles installed.)

## G-code tools

All of these read a `plate_N.gcode` that `slice_cli.py` wrote; several also read it straight from a sliced 3MF with
`--3mf FILE --plate N`. All are read-only.

### gcode_paths.py

- **What it does:** the G-code reader the other tools share. It turns a plate into paths per layer, feature, object and
  tool, and interpolates G2/G3 arcs (a reader that skips arcs loses whole wall loops).
- **Inputs:** a plate G-code or a 3MF with `--plate N`. **Outputs:** a summary per feature. Exit 0.
- **Example:** `.venv\Scripts\python.exe -B tools\gcode_paths.py work\slice\bracket\plate_1.gcode`

```text
gcode_paths: plate_1.gcode (plate 1, arcs interpolate); layers 6; stats {'m83': 1, 'g1': 71, 'g2': 1, 'arcs_ij_form': 1, 'extruding_arcs': 1, 'max_arc_end_radius_mismatch_mm': 0.0}
  Bridge                       paths       2  length         30.0 mm  of which arcs         0.0 mm in 0 arc moves
  Outer wall                   paths       7  length        495.7 mm  of which arcs        15.7 mm in 1 arc moves
  Prime tower                  paths       6  length        360.0 mm  of which arcs         0.0 mm in 0 arc moves
```

### gcode_audit.py

- **What it does:** reports what `result.json` does not show: extents per feature and tool, points outside an allowed X
  range, support and which objects carry it, tool changes, the filament map from the header, arcs, and bridge rows.
- **Inputs:** a plate G-code; `--xmin`/`--xmax` (default 25..325, set it to your printer's bed), `--bridge-limit MM`
  (from a printed coupon), `--json`.
- **Outputs:** the report; exit 0 no findings, 1 warnings, 2 a bridge over the limit, 3 unreadable.
- **Example:** `.venv\Scripts\python.exe -B tools\gcode_audit.py work\slice\bracket\plate_1.gcode --xmin 0 --xmax 256`

```text
G-code audit: plate_1.gcode
  filament_map = 2
  tool changes: 1  objects: 2  support path: 30 mm  outside X 0.0..256.0: 0 pts (+0 in start/end G-code 'Custom', ignored)
  arc segments: 1, arc length: 15.7 mm
  [WARN] support extrusion present: 30 mm of path on objects ['1']
VERDICT: WARN
(exit code 1)
```

### tower_bounds.py

- **What it does:** measures the prime tower's footprint from the G-code, for all layers and for the first layer with
  its brim (the wider one, which is what collides).
- **Inputs:** one or more plate G-code files; `--first-layer-z`, `--json`. **Outputs:** text; exit 0.
- **Example:** `.venv\Scripts\python.exe -B tools\tower_bounds.py work\slice\two_colour\plate_1.gcode`

```text
plate_1.gcode: tower body x 200.0..215.0 y 200.0..215.0 (15.0×15.0 mm, 6 layers)
    first layer (incl. brim) x 200.0..215.0 y 200.0..215.0 (15.0×15.0 mm)
```

### tower_clearance.py

- **What it does:** the GUI's "Prime Tower is too close to others" check, which the command line does not report,
  replicated on the real G-code: the gap from the tower (body and first layer) to every object.
- **Inputs:** plate G-code files; `--min-gap` (the checklist uses 8 mm, a house rule), `--json`.
- **Outputs:** exit 0 OK, 1 WARN (gap below the rule), 2 FAIL (an object touches the tower's first layer), 3 shapely
  missing.
- **Example:** `.venv\Scripts\python.exe -B tools\tower_clearance.py work\slice\two_colour\plate_1.gcode --min-gap 8`

```text
plate_1.gcode: tower all-layers [200.0, 200.0, 215.0, 215.0] first-layer [200.0, 200.0, 215.0, 215.0] (rule: gap >= 8.0 mm)
  [OK] object 1: bounds [100.0, 100.0, 136.0, 120.0] gap body 113.14 mm, first-layer 113.14 mm
  VERDICT: OK
```

### support_gap_readback.py

- **What it does:** the support Top Z distance you type is not always the gap that gets sliced. This measures the
  printed gap under every support interface and compares it with the typed value.
- **Inputs:** a plate G-code (or `--3mf FILE --plate N`); `--top-z`, sampling options, `--json`.
- **Outputs:** histogram and verdict; exit 0 the gaps equal the typed value (or support is off), 1 WARN, 3 unreadable.
- **Example:** `.venv\Scripts\python.exe -B tools\support_gap_readback.py --3mf work\slice\bracket\out.3mf --plate 1`

```text
support_gap_readback: plate_1.gcode
  typed Top Z 0.2  style default  type normal(auto)  independent None  prime tower 1  object layer heights [0.2]
  [WARN] object 1 None: printed Top Z mode 0.0 mm on 100% of 42 samples vs typed 0.2 mm (layer heights [0.2]; stacking rule predicts [0.2]; histogram [{'gap_mm': 0.0, 'n': 42, 'share': 1.0}])
VERDICT: WARN
```

### interface_coverage.py

- **What it does:** for every overhanging region of the part, how much of it actually has support under it, per side
  (front, right, back, left). It catches a visible ledge that prints with only part of its lip supported.
- **Inputs:** a plate G-code (or `--3mf FILE --plate N`); thresholds such as `--min-mm`, `--cover-fail`; `--json`.
- **Outputs:** regions and verdict; exit 0 no FAIL, 1 WARN, 2 a visible region under the coverage threshold, 3 unreadable.
- **Example:** `.venv\Scripts\python.exe -B tools\interface_coverage.py --3mf work\slice\bracket\out.3mf --plate 1`

```text
interface_coverage: plate_1.gcode  window z [None, None]  support OFF  critical_only 0  remove_small_overhang 0  walls-only True  radius 0.60 mm from support_line_width 0.42 + support_interface_spacing 0.5
  right (+X) 315-45      {'mm': 42.4, 'depth_p50': 7.7, 'depth_p90': 13.88, 'depth_max': 15.9, 'supported_pct': 50.9, 'features': {'Bridge': 150, 'Outer wall': 62}}
  [OK] 3 overhanging region(s), 3 visible candidate(s) (>= 10 mm, depth p90 > 1 mm), none under 90 % coverage
VERDICT: OK
```

### visible_ratio.py

- **What it does:** for a display print, how much of the part a viewer can still see through the support, from the
  front and from an angle, at 25, 50, 75 and 100 % of the height. It also draws two pictures: grey = visible part,
  BLUE = part hidden behind support, RED = support.
- **Inputs:** a plate G-code; `--out-prefix`, `--face-mask`, camera options.
- **Outputs:** two PNGs and a JSON in `work\visible_ratio\` by default; exit 0 OK, 1 WARN (below 0.80), 2 FAIL (below
  0.60), 3 unreadable. The thresholds are proposed, not verified.
- **Example:** `.venv\Scripts\python.exe -B tools\visible_ratio.py work\slice\figure\plate_1.gcode --out-prefix work\visible_ratio\figure-plate1`

```text
visible_ratio: plate_1.gcode plate 1: 6 layers, z top 1.2 mm, 0.0 s
  front visible ratio by height: 25% (z 0.4) 1.0  50% (z 0.6) 1.0  75% (z 1.0) 1.0  100% (z 1.2) 1.0
        image vr\plate1-front.png  (grey = visible part, BLUE = part hidden behind support, RED = support)
visible_ratio verdict: OK (FAIL < 0.6, WARN < 0.8; proposed thresholds)
```

## Mesh tools

### overhang_gate.py

- **What it does:** per part in its print pose: the area of faces steeper than the support threshold (angle measured
  from straight down, as Bambu Studio does), the largest per-layer cantilever, and floating islands. With `--ref` it
  reports only the overhang a change introduced.
- **Inputs:** STL files; `--pose`, `--place`, `--threshold` (default 30), `--layer`, `--ref`, `--json`.
- **Outputs:** report; exit 0 no flags, 1 WARN, 2 FAIL, 3 load error.
- **Example:** `.venv\Scripts\python.exe -B tools\overhang_gate.py examples\calibration-cube\cube_20mm.stl`

```text
cube_20mm  pose (0.0, 0.0, 0.0)  place (0.0, 0.0, 0.0) (model-centred posed frame)  watertight  12 faces  posed bbox [[-10.0, -10.0, 0.0], [10.0, 10.0, 20.0]]
  overhang below 30 deg: 0.0 mm2 (min angle None; bbox None); 30-45: 0.0 mm2; 45-60: 0.0 mm2
  [OK] no flags

t_shape  pose (0.0, 0.0, 0.0)  place (0.0, 0.0, 0.0) (model-centred posed frame)  watertight  24 faces  posed bbox [[-15.0, -5.0, 0.0], [15.0, 5.0, 24.0]]
  overhang below 30 deg: 300.0 mm2 (min angle 0.0; bbox [[-15.0, -5.0, 20.0], [15.0, 5.0, 20.0]]); 30-45: 0.0 mm2; 45-60: 0.0 mm2
  [WARN] per-layer cantilever 10.00 mm at posed z 20.10 (1 layer(s) over 0.5 mm, the --cantilever-warn acceptance value; project value, not a general rule)

VERDICT: WARN
```

### stability_check.py

- **What it does:** for a piece that stands on its own: centre of mass, the footprint it stands on, the tip angle in
  every direction, the push at the top that starts it tipping, and the first-layer contact. Thresholds are proposed, not
  verified: confirm with a tilt test of the printed piece.
- **Inputs:** STL files; `--mass NAME=GRAMS` (use the slicer's grams), `--gcode NAME=plate.gcode` (subtracts support
  grams), placement options, `--out`, `--json`, `--render` (needs `blender_exe` in the config).
- **Outputs:** a Markdown report; exit 0 PASS, 1 WARN, 2 FAIL.
- **Example:** `.venv\Scripts\python.exe -B tools\stability_check.py examples\calibration-cube\cube_20mm.stl --mass cube_20mm=9.5`

```text
- CoM INSIDE the hull; margin to the nearest edge 10.00 mm towards 180 deg (0 = +X, 90 = +Y)
- tip angle: exact minimum 45.00 deg (atan(margin / CoM height)); 10-deg table minimum 45.00 deg at 0 deg
- knock force at the top (F = m*g*margin / H_top = 9.50 g * 9.81 m/s2 * 10.00 mm / 20.00 mm): 0.047 N = 4.8 gf

Result: PASS (exit 0). Nothing printed or sent.
```

### stability_render.py

- **What it does:** runs inside Blender, started by `stability_check.py --render`, and renders front, side and top views
  with the centre of mass (red) and the footprint (blue). You do not run it directly.
- **Inputs:** a job file from `stability_check.py`; `blender_exe` in `config\paths.yaml` (empty = render skipped with a
  message). Written for the Blender 5.x Python API; not tested on older versions.
- **Outputs:** `<prefix>-front.png`, `-side.png`, `-top.png`. No sample: Blender was not part of the sample run.

## Images

### render_critic.py

- **What it does:** a scored critique of a still render (0-100): value structure, focal point, the squint test, edge
  separation, text legibility at a small size. It measures; it has no taste, and it is a proxy for a human review.
- **Inputs:** PNG or JPG images; `--subject-box` or `--subject-mask`, `--text-box`, `--refs`, `--out`. Needs the optional
  open3d package (exit 3 with a message without it).
- **Outputs:** `<name>_critic.md`, `_critic.json` and three helper images in `work\render_critic\` (or `--out`);
  exit 0 PASS, 1 WARN, 2 FAIL, 3 unreadable.
- **Example:** `.venv\Scripts\python.exe -B tools\render_critic.py work\renders\front.png`

```text
PASS 100.0  render.png  (0.52 s) -> critic\render_critic.md
```

## Knowledge and agent files

### check_note.py

- **What it does:** checks a knowledge note against [templates/note.md](../templates/note.md): an `Applies to:` line, a
  `Verified: YYYY-MM-DD` line with real digits, a `Sources:` section with a URL, a source on every fact bullet, and a
  load (MPa) on every HDT value. A fact bullet's source can be its own URL, the word "measured", a "not verified" label
  (the UI-label tag "(label not verified)" alone does not count), a link to another note that exists, or a back-reference such as "same source" when a bullet above it in the same subsection has a
  URL. The self-test runs it over every shipped note. It also runs as a hook right after Claude writes a file under `knowledge\`.
- **Inputs:** note files (or the hook's JSON). **Outputs:** PASS/FAIL per file; exit 0 all pass, 2 otherwise.
- **Example:** `.venv\Scripts\python.exe -B tools\check_note.py knowledge\01-printers\p1s-vs-h2c-specs.md knowledge\01-printers\my-draft-note.md`
  (`my-draft-note.md` stands for a draft of yours whose line 6 has no source)

```text
PASS knowledge\01-printers\p1s-vs-h2c-specs.md
FAIL knowledge\01-printers\my-draft-note.md
  - line 6: fact bullet without URL / local path / 'measured' / 'not verified' (or a 'same source' back-reference with a URL earlier in the same subsection, or a link to a note that exists)
(exit code 2)
```

### check_skill.py

- **What it does:** lints `.claude\skills\<name>\SKILL.md` and `.claude\agents\*.md`: frontmatter keys, a "Use when"
  description, required sections, a rationalizations table and a verification checklist. Adapted from an MIT-licensed
  linter (credit in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)).
- **Inputs:** files or folders. **Outputs:** PASS/FAIL per file; exit 0 or 2.
- **Example:** `.venv\Scripts\python.exe -B tools\check_skill.py .claude\skills .claude\agents`

```text
FAIL skills\sample-skill\SKILL.md
  - S3 description must say 'Use when' (or use before/after/during)
  - S4 missing section '## When to use'
  - S4 Verification must contain checkboxes
(exit code 2)
```

### build_indexes.py

- **What it does:** regenerates `knowledge\INDEX.md` (one line per category) and `lessons\INDEX.md` (one line per lesson)
  from the files on disk.
- **Caution:** the shipped indexes are written by hand with summaries and headings. Running this tool replaces them with
  the plain generated form. Use it in your own copy only if you prefer generated indexes.
- **Inputs:** `--root DIR` (default: the project). **Outputs:** the two files; exit 0.
- **Example:** `.venv\Scripts\python.exe -B tools\build_indexes.py`

```text
knowledge/INDEX.md: 1 categories; lessons/INDEX.md: 1 lessons
```

(The sample ran in a small temporary copy.)

## Sharing safely

### privacy_scan.py

- **What it does:** looks for personal data before you publish a folder or a fork: your own denylist words, user-profile
  paths, e-mail addresses, private IP addresses, secret-looking values (always masked), printer-serial-like codes, and
  metadata inside PNG, JPEG, PDF and ZIP or 3MF files. Standard library only; it changes nothing.
- **Inputs:** a folder; `--denylist FILE` (start from [config/denylist.example.txt](../config/denylist.example.txt) and
  keep your copy outside the project), `--exclude-dir`, `--json`, `--no-builtin`.
- **Outputs:** one line per hit, `path:line: [rule] context`, then a summary; exit 0 clean, 1 hits, 2 scan incomplete.
- **Example:** `.venv\Scripts\python.exe -B tools\privacy_scan.py . --denylist C:\Private\my-denylist.txt --exclude-dir __pycache__`

```text
---
files scanned: 300
surfaces: png=8, text=294
hits per rule: none
errors: 0
VERDICT CLEAN
```

(Captured on this project before release.)

### strip_metadata.py

- **What it does:** removes personal metadata: text, time and EXIF chunks from PNG; EXIF, XMP, IPTC and comments from
  JPEG; designer, title, dates and absolute paths inside 3MF files (and strips their thumbnails). Image data and geometry
  are untouched.
- **Inputs:** files; `--dry-run` (list only), `--in-place`, `-o OUT`.
- **Outputs:** `<name>.stripped<ext>` beside the input unless `--in-place`; exit 0 done or nothing to strip, 2 errors.
- **Example:** `.venv\Scripts\python.exe -B tools\strip_metadata.py my_print.3mf --dry-run`

```text
assets\brand\crest-printing-512.png: nothing to strip
(exit code 0)
```

## Hooks (run by Claude Code, set in `.claude\settings.json`)

All hooks run with `.venv\Scripts\python.exe`, which is why setup must run before you open Claude Code.

### hooks\session_start.py

- **What it does:** at session start, prints `lessons\INDEX.md` so the lessons enter Claude's context. Never blocks.
- **Example (manual):** `.venv\Scripts\python.exe -B tools\hooks\session_start.py < NUL` in Command Prompt; in
  PowerShell use `$null | .venv\Scripts\python.exe -B tools\hooks\session_start.py`.

```text
[Maker Mastery] lessons\INDEX.md (read the lesson files for root causes):
# Lessons index (generated; one line per post-mortem - read the file for root cause and rule)

- `lessons/2026-01-01-first-layer.md` - First layer lifted on a dusty plate
[Maker Mastery] Rules: CLAUDE.md. No AI ever starts, sends, uploads or queues a print.
```

### hooks\guard_paths.py

- **What it does:** before Claude writes a file or runs a shell command, blocks it if it targets a folder under
  `protected_roots` in `config\paths.yaml`. It also blocks a bare `python`, `py` or `pip` command, so Claude always uses
  `.venv\Scripts\python.exe`. Exit 2 blocks and tells Claude why.
- **Example (manual):** `'{"tool_input": {"file_path": "D:/Finished/x.txt"}}' | .venv\Scripts\python.exe tools\hooks\guard_paths.py`

```text
BLOCKED by tools\hooks\guard_paths.py: '<tmp>\finished\a.txt' resolves under the protected root '<tmp>\finished' (protected_roots in config\paths.yaml). Claude reads this folder only. Copy the file into the repository instead, or remove the root from config\paths.yaml yourself.
(exit code 2)
```

### hooks\log_run.py

- **What it does:** appends one line per finished subagent to `work\agent-runs.log`, so silent failures show up. Never
  blocks. It is switched **on** as a `SubagentStop` hook in `.claude\settings.json`; the log lives in the git-ignored
  `work\` folder. To switch it off, remove the `SubagentStop` block from `.claude\settings.json`.
- No sample output was captured.

## MCP (optional)

### mcp\mm_audit_server.py

- **What it does:** a read-only MCP server named `mm-audit` with three tools, `audit_3mf`, `resolve_profile` and
  `tower_clearance`, each running the matching script. It reads only under `allowed_roots` in `config\paths.yaml`, never
  writes, never uses the network and never talks to a printer.
- **Turn it on:** see [.mcp.json.example.md](../.mcp.json.example.md). Off by default.
- No sample output: it speaks the MCP protocol, not text.

### mcp\tower_clearance_3mf.py

- **What it does:** the tower clearance check run on the G-code inside a sliced 3MF, in memory, without extracting files.
  Used by the MCP server; you can run it directly.
- **Outputs:** JSON per plate; exit 0 OK, 1 WARN, 2 FAIL, 3 shapely missing, 4 not a sliced 3MF, 5 unreadable.
- **Example:** `.venv\Scripts\python.exe -B tools\mcp\tower_clearance_3mf.py work\slice\two_colour\out.3mf`

```text
[
 {
  "file": "sliced.3mf!Metadata/plate_1.gcode",
  "prime_tower": true,
  "min_gap_rule_mm": 8.0,
  "verdict": "OK"
 }
]
```

(Cut to four keys; the full sample is in [tool-sample-outputs.md](tool-sample-outputs.md).)

## The example generator

`examples\calibration-cube\make_cube.py` writes a 20 mm cube STL and runs `overhang_gate.py` and
`stability_check.py` on it. Walk-through: [examples/calibration-cube/README.md](../examples/calibration-cube/README.md).

Next: [08 - Customize](08-customize.md).
