# Calibration cube: your first run through the tools

This walk-through takes a 20 mm cube from a script to a checked print file. It uses three tools: the cube generator,
Bambu Studio and the 3MF audit. It takes you up to the point of printing, and then you print it yourself.

> **You press Print. The AI never does.** No tool in this repository starts, sends, uploads or queues a print. Claude can
> generate, slice and check files. Pressing **Print** in Bambu Studio is always your step, after you have read the audit.

## Before you start

- You have run `tools\setup.ps1` once (it creates `.venv` and `config\paths.yaml`).
- Bambu Studio is installed. If it is not in the default folder, set `bambu_studio_exe` in `config\paths.yaml`.
- Filament: this example assumes one PLA spool. Before you trust the audit's load check (C7), write what is really
  loaded in `knowledge\00-gear-inventory\current-load.md`. While that file still says EMPTY, C7 fails on purpose.

About the labels below: a label marked **(wiki)** is quoted from the Bambu Lab wiki page
[Bambu Studio Quick Start Guide](https://wiki.bambulab.com/en/software/bambu-studio/studio-quick-start) (read 2026-10-22).
A label marked **(label not verified)** was not found on a Bambu Lab wiki page. Check it on your screen, because it
may be worded differently in your version.

## 1. Generate the cube

In VS Code, open a terminal in the repository folder (**Terminal > New Terminal** (label not verified)) and run:

```powershell
.venv\Scripts\python.exe -B examples\calibration-cube\make_cube.py
```

This writes `examples\calibration-cube\cube_20mm.stl` and runs two checks on it:

- `tools\overhang_gate.py` should say `VERDICT: OK` (a cube has no overhangs and no floating islands).
- `tools\stability_check.py` should say `Result: WARN (exit 1)`. The only flag is that the mass comes from a uniform
  density, not from slicer grams. A 20 mm cube cannot tip: its tip angle is 45 degrees.

## 2. Open it in Bambu Studio

1. Start Bambu Studio and click **New Project** (wiki).
2. Import `cube_20mm.stl` with the first icon on the top toolbar of the preview pane (wiki). You can also drag the
   file from File Explorer into the window (wiki).

## 3. Choose your printer, plate and process

1. Under **Printer** (wiki), pick your printer and nozzle from the drop-down list. The nozzle size is part of the
   printer entry.
2. Pick the plate that is on your printer from the plate type drop-down (label not verified), for example Textured PEI
   Plate (label not verified).
3. Under **Filament** (wiki), pick the filament that is really loaded, for example a PLA preset that matches your spool.
4. Under **Process** (wiki), pick **0.20mm Standard** for your printer. The wiki calls 0.20 mm "the norm" for most
   prints. Leave every other setting at its default for this cube.

## 4. Slice

Click **Slice** (wiki) at the top right. Bambu Studio switches to the **Preview** (wiki) pane. Look at it: the cube
should show walls, top and bottom layers, infill, and no support.

## 5. Export the 3MF

Use either of these:

- **The project file:** **File > Save Project As** (label not verified). Save it, for example, as
  `work\calibration-cube\cube.3mf`. This file holds the settings and the meshes.
- **The sliced file:** click the arrow to the left of **Print plate** (wiki) and choose **Export plate sliced file**
  (wiki). This file also holds the sliced G-code, so the audit can check that the slice is fresh (C16). Whether every
  key the audit reads is in this export is not verified. If the audit reports keys as missing, use the project file.

## 6. Audit the exported 3MF

```powershell
.venv\Scripts\python.exe -B tools\audit_3mf.py work\calibration-cube\cube.3mf
```

Read every line. `[OK]` passed. `[WARN]` asks you to look at something. `[FAIL]` means do not print yet. The last line
is `VERDICT: OK`, `WARN` or `FAIL`. For this cube you should expect:

- **C7 (load):** FAIL until `current-load.md` names the spool you loaded and has today's date in its `Verified:` line.
- **C8 (filament profile vs printer):** WARN if the audit cannot find your installed Bambu Studio profiles. Check
  `bambu_studio_exe` / `bambu_profiles_dir` in `config\paths.yaml`.
- **C15 (process preset):** OK when you kept the printer's 0.20mm Standard preset.

To check the slice itself, you can also run `tools\slice_cli.py` on the project file. It runs the Bambu Studio command
line and only slices; it never prints. Then run `tools\gcode_audit.py` on the `plate_1.gcode` it writes.

## 7. Print (your step)

When the audit has no FAIL and you have read every WARN, go back to Bambu Studio, check the preview once more, and
press **Print plate** (wiki) yourself. Then measure the cube with calipers: 20.0 mm on X, Y and Z. That measurement is a
real data point you can record.
