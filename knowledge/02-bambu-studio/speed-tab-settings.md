# Speed tab: every setting (Process preset)
Applies to: both (H2C, P1S) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61). H2C values shown are the 5-element arrays of `0.20mm Standard @BBL H2C`; P1S profiles carry the same keys as single values.
Verified: 2026-10-04

Abbreviations: PC = [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); CM = [ConfigManipulation.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp); H2C = [0.20mm Standard @BBL H2C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json).

## Facts
- Speed is its own top-level Process tab, drawn just before the Support page. -- [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3341-3405
- On the H2C every Speed array has 5 numbers keyed by `print_extruder_id` [1,1,1,2,2] and `print_extruder_variant` (Direct Drive Standard, Direct Drive High Flow, Direct Drive E3D High Flow, Direct Drive Standard, Direct Drive High Flow). They are per nozzle **variant**, not per AMS slot or plate. Example: Outer wall [200,500,500,200,500] = 200 mm/s on a Standard nozzle, 500 on High Flow or E3D High Flow. -- [H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json)

### Speed values (0.20mm Standard @BBL H2C)
| UI label | key | value (Standard / High Flow) | source |
|---|---|---|---|
| Initial layer | `initial_layer_speed` | 50 mm/s all variants (excludes solid infill) | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3377 |
| Initial layer infill | `initial_layer_infill_speed` | 105 mm/s all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3386 |
| Outer wall | `outer_wall_speed` | 200 / 500 | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2159 |
| Inner wall | `inner_wall_speed` | 300 / 600 | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4585 |
| Small perimeters | `small_perimeter_speed`, `small_perimeter_threshold` | 50 % of outer wall; threshold 0 | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2171-2184 |
| Sparse infill | `sparse_infill_speed` | 350 / 600 | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3962 |
| Internal solid infill | `internal_solid_infill_speed` | 250 / 600 | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5270 |
| Vertical shell speed | `vertical_shell_speed` | 80 % of internal solid infill | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2043-2047 |
| Top surface | `top_surface_speed` | 200 all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5944 |
| Gap infill | `gap_infill_speed` | 250 on Standard, 150 on the High Flow variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3544 |
| Bridge | `bridge_speed` | 50 all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1682 |
| Support | `support_speed` | 150 all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5751 |
| Support interface | `support_interface_speed` | 80 all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5685 |
| Travel | `travel_speed` | 1000 all variants | [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5995 |

- The Small perimeters and Vertical shell speed tooltips are built from two string literals with no space between them, so the GUI shows run-together words ("onthe"); cosmetic only. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2171-2184, L2043-2047

### Overhang and height slowdown
- Slow down for overhang `enable_overhang_speed`: on for every variant. The wiki says it is on by default and that 0 mm/s means no slowdown. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1552; [Slow down for overhang wiki](https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang)
- Overhang speed steps (shown only while the line above is on): 10 % = 0 (no slowdown), 25 % = 50, 50 % = 30, 75 % = 10, 100 % = 10 mm/s, same on every variant. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1560-1606; [CM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp) L1054-1056
- Slow down by height: off. While off, the detail rows are hidden: Starting height 0 mm, Speed at starting height 1000 mm/s, Acceleration at starting height 100000 mm/s2, Ending height 400 mm, Speed at ending height 1000 mm/s, Acceleration at ending height 100000 mm/s2. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1617-1673; [CM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp) L1058-1060

### Acceleration (all variants)
- Normal printing `default_acceleration` 8000 mm/s2 (L1854); Travel 10000 (L1863); Initial layer travel 6000 (L1886); Initial layer 500 (L3272; tooltip typo "adhensive" is in the source); Outer wall 5000 (L3244); Inner wall 0 = use normal (L3253); Top surface 2000 (L3235); Sparse infill 100 % of default (L3262). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- Short travel acceleration: 250 mm/s2; ported from PrusaSlicer for VFA reduction; Develop mode only, so it is not drawn in Simple or Advanced mode. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1872-1884; [OptionsGroup.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/OptionsGroup.cpp) L842-854
- Enable accel_to_decel / accel_to_decel ratio: not shown on the H2C. They appear only when `gcode_flavor` is Klipper, and the H2C machine chain sets `marlin`. Effective (unused) defaults: false and 50 %. -- [CM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp) L1087-1092; [fdm_machine_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/fdm_machine_common.json)
- Jerk(XY) group (Default, Outer wall, Inner wall, Infill, Top surface, First layer, Travel): hidden for every Bambu-vendor printer, H2C and P1S alike. Unused code defaults: `default_jerk` 0, the other six 9 mm/s. The first-layer row is labelled "First layer". -- [CM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp) L934-936; [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3600; [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3296-3344

## In practice
- The 5 numbers in an H2C Speed array are per nozzle variant. Read `print_extruder_id` and `print_extruder_variant` in the same JSON before deciding which number applies to your toolhead.
- A Speed row that seems "missing" (Jerk group, accel_to_decel pair, height-slowdown detail rows, Short travel acceleration) is a visibility toggle for vendor, G-code flavour or UI mode. The row still has a real default.
- Profile bundles update independently of the app. Compare `%APPDATA%\BambuStudio\system\BBL\process\` with the tag files before trusting these numbers on your install.
- See [speed-quality-method.md](speed-quality-method.md) for how these settings affect surface quality (small perimeters and jerk never apply on these presets; one machine-limit `M205` line is still written; Slow down by height is 7 lines including the checkbox).

## Not verified / open questions
- Values were checked against one profile bundle; newer bundles may differ.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- labels, tooltips, defaults, modes
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- page order, BBL vendor flag
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp -- row visibility toggles
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/OptionsGroup.cpp -- Develop-mode row visibility
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json -- H2C arrays and variant mapping
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/fdm_machine_common.json -- gcode_flavor marlin
- https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang
