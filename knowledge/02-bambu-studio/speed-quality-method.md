# Speed vs surface quality: the method (outer wall speed, acceleration, layer-time trap)
Applies to: H2C · Bambu Studio 02.08.02.61 · Bambu PLA Basic / PLA Matte @BBL H2C (0.4 mm nozzle)
Verified: 2026-10-06

Abbreviations: PC = [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), TAB = [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp), GC = [GCode.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp), GW = [GCodeWriter.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCodeWriter.cpp), all at tag v02.08.02.61. Preset values come from the BBL profile tree (`resources/profiles/BBL/` in the repo or your install). The 02.08.02.61 release notes say H-series presets were updated to fix abnormal values, so older installs may differ ([release notes](https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61)). H2C arrays are ordered Standard, High Flow, E3D High Flow, then the right-extruder pair; values below are the Standard entry unless stated.

## Facts

### Process > Speed > Other layers speed (0.4 mm presets)
- Outer wall: `0.20mm Standard @BBL H2C` = 200 mm/s (High Flow 500). `0.16mm High Quality`, `0.12mm High Quality` and `0.20mm High Quality @BBL H2C` = 60 mm/s on every entry. Code default 60; the tooltip says the outer wall is usually slower than the inner wall for quality. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2159-2168; [0.20 Standard H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json); [0.16 HQ H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.16mm%20High%20Quality%20%40BBL%20H2C.json); [0.12 HQ H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.12mm%20High%20Quality%20%40BBL%20H2C.json); [0.20 HQ H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20High%20Quality%20%40BBL%20H2C.json)
- Other speeds (Standard; 0.16 HQ; 0.12 HQ; 0.20 HQ, mm/s): Inner wall 300; 150; 120; 150. Sparse infill 350; 180; 100; 200. Internal solid infill 250; 180; 150; 200. Top surface 200; 150; 150; 150. Gap infill 250; 250; 50; 250. Support 150, support interface 80, bridge 50 and vertical shell 80 % in all four. -- same preset files as above
- Overhang speed table (10-25 / 25-50 / 50-75 / 75-100 / 100 %, mm/s): Standard 0 / 50 / 30 / 10 / 10; all three HQ presets 60 / 30 / 10 / 10 / 10; 0 means no slowdown. Slow down for overhang is on in all four. The smooth overhang transition is only available with the Classic wall generator, which all four use. -- [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3355; [Slow down for overhang wiki](https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang)
- "Slow down by height" is 7 lines: the checkbox `enable_height_slowdown` plus start/end height, speed and acceleration. -- [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3363-3369
- Filament > "Override overhang speed" is off for PLA Basic and PLA Matte @BBL H2C, so the Process overhang and bridge speeds apply. -- [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L6142-6147

### Small perimeters never applies on the H2C presets
- Small perimeters (50 % of outer wall) only triggers for loops shorter than 2 x pi x threshold. Every checked H2C preset has Small perimeter threshold = 0, so no loop qualifies. The threshold acts as a radius although its tooltip says "length". -- [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L6222-6233; [libslic3r.h](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/libslic3r.h) L71; [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2171-2192

### Acceleration
- `0.20mm Standard @BBL H2C`: default 8000, Outer wall 5000, Inner wall 0 (= normal), Top surface 2000, Sparse infill 100 %, Travel 10000, Short travel 250 mm/s2. The three High Quality presets: default 4000, Outer wall 2000, others the same. -- preset files above
- Outer wall acceleration: the tooltip says a lower value can improve quality. It is also applied to overhang perimeters because the code cannot tell whether an overhang perimeter is outer. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3244-3251; [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L7155-7159
- The H2C machine profile uses Marlin G-code flavour, so the writer clamps every `M204 S` to `machine_max_acceleration_extruding` (20000), not to the 9000 travel limit. Travel 10000 therefore reaches the G-code as `M204 S10000`. -- [GW](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCodeWriter.cpp) L62-65, L269-273; [H2C 0.4 machine profile](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json)
- To check on your own slice: count the `M204 S` values in a sliced H2C G-code; the preset values above (8000, 10000, 5000, 250) should all appear.

### Jerk
- Process > Speed > Jerk(XY) values are never written for a Bambu printer: every per-feature jerk use is guarded by `!is_BBL_Printer()`. Editing them does nothing on the H2C. -- [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L3115, L4749, L4776, L6329, L7174, L7718
- The G-code is not jerk-free: the machine-limits block writes one `M205` line (with `M201`/`M203`) from the machine profile. Look for it near the top of your G-code. -- [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L2664, L3882-3920

### Filament > Cooling (PLA Basic / PLA Matte @BBL H2C)
- "Slow printing down for better layer cooling" is on; Layer time `slow_down_layer_time` = 4 s; Min print speed `slow_down_min_speed` = 20 mm/s. A layer estimated under 4 s is slowed to reach 4 s, but never below 20 mm/s. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1808-1813, L5230-5238, L4450-4456; [Auto cooling wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-cooling)
- Fan: Min fan speed 60 % for layers shorter than 100 s, interpolated by layer time up to Max fan speed (80 % for PLA Basic, 100 % for PLA Matte) at the 4 s threshold. Keep fan always on = on. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2370-2384, L4377-4428; [PLA Basic H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40BBL%20H2C.json); [PLA Matte H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Matte%20%40BBL%20H2C.json)
- "Don't slow down outer walls" is off by default. Its tooltip gives three reasons to turn it on: avoid shine changes on glossy filaments, avoid outer-wall speed changes that look like Z banding, and avoid speeds that cause VFAs. The row is only enabled while slow-down for layer cooling is on. The wiki says it keeps outer-wall speed constant for quality. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1815-1823; [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L4911-4912; [Auto cooling wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-cooling)
- On a 2023 GitHub issue about variable outer-wall speed causing wall artifacts, a Bambu-assigned contributor suggested turning the cooling slowdown off for a constant outer-wall speed (developer comment, not documentation). -- [GitHub issue 1482](https://github.com/bambulab/BambuStudio/issues/1482)
- Develop mode only: "Cooling slowdown logic" (PLA = uniform; option "Consistent surface" keeps the external perimeter speed) and "Perimeter transition distance" (default 10; recommended 5-10 mm). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1826-1852; [Silk guide](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)
- Overhang cooling: Force cooling for overhang and bridge on; Fan speed for overhang 100 %; Cooling overhang threshold 50 % for PLA; Pre start fan time 2 s. The final speed is the lower of the overhang slowdown and the cooling slowdown. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1384-1445; [Auto cooling wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-cooling)

### Maximum volumetric speed caps outer wall speed
- Max volumetric speed for PLA Basic and PLA Matte @BBL H2C (0.4 mm): 25 mm3/s Standard, 40 High Flow, 25 E3D High Flow. Speed = min(set speed, volumetric limit / cross-section); a speed of 0 uses the limit. -- [GC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp) L7312-7356; filament preset files above
- The code models a line as a rectangle with rounded ends: area = h x (w - h x (1 - pi/4)). Worked out for w = 0.42 mm at 25 mm3/s: speed cap about 331 mm/s at 0.20 mm layers, 405 at 0.16, 528 at 0.12. So a 200 mm/s outer wall is not volumetric-limited on a Standard nozzle. -- [Flow.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Flow.cpp) (arithmetic is ours)

### Quality options tied to speed
- Smoothing wall speed along Z (experimental) is on in all four H2C presets (via `fdm_process_dual_common.json`, with `smooth_coefficient` 4); the tooltip warns print time increases. The wiki recommends it for tall smooth walls on figurines and display pieces and for banding from local cooling slowdowns, not for small models. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1171-1176; [Quality advanced wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings)
- Print sequence is By layer in all four presets; print-by-object needs object spacing above the extruder clearance radius, listed per printer on the wiki. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1797-1806; [Print by object wiki](https://wiki.bambulab.com/en/software/bambu-studio/sequent-print)

### Bambu's own guidance (paraphrased)
- Gloss bands: Bambu says matte-to-glossy changes usually come from slowdowns that leave filament longer in the hotend; it suggests printing several objects at once and notes 0.16 mm layers as a good balance. -- [Different gloss wiki](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/different-gloss)
- Silk PLA guide (X1 manual page): outer wall 40-60 mm/s, trying 50 first; turn on "Don't slow down outer walls"; set Cooling slowdown logic to Consistent Surface; 0.16 mm layers. Written for silk PLA, not PLA Basic or Matte. -- [Silk guide](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)
- Bambu says outer wall speed strongly affects surface quality, especially on overhangs, and that Bambu filaments print fast at good quality without cooling changes. -- [High speed print at quality wiki](https://wiki.bambulab.com/en/software/bambu-studio/high-speed-print-at-quality)

### Presets and pages that do not exist
- There is no `0.20mm Fine @BBL H2C`. The 0.4 mm H2C process presets are 0.08mm High Quality, 0.12mm High Quality, 0.16mm High Quality, 0.16mm Standard, 0.20mm High Quality, 0.20mm Standard, 0.24mm Standard. -- [BBL process folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- The old speed wiki page https://wiki.bambulab.com/en/software/bambu-studio/speed-settings returned HTTP 404 when checked; use the pages cited above.

### Community observation (cannot set a rule)
- On a 2023 Bambu forum thread (non-staff, printer not named), one poster reported belt-pattern artifacts roughly between 70 and 170 mm/s and stepper vibration between 30 and 70 mm/s, and said printing outer walls above about 180 or below 30 mm/s solved it. -- [Forum thread 13421](https://forum.bambulab.com/t/possible-fix-for-ghosting-vfa-artifacts-with-speed-adjustments/13421) (community)

## In practice
A method for choosing an outer-wall speed on a display piece. Bambu publishes no speed floor, so the final number has to be measured on your printer.
1. Know the presets: High Quality = outer wall 60 mm/s at 2000 mm/s2; Standard = 200 mm/s at 5000 mm/s2. Infill stays fast in all of them.
2. Two knobs only: Process > Speed > Other layers speed > Outer wall, and Process > Speed > Acceleration > Outer wall. Hold everything else fixed. Jerk(XY) and Small perimeters do nothing on these presets.
3. Layer-time trap: any layer under 4 s is slowed (down to 20 mm/s) whatever outer-wall speed you set, and the fan rises on short layers. A speed test coupon must keep every layer at 4 s or longer, or declare a deviation (Filament > Cooling > "Slow printing down for better layer cooling" off with a fixed fan, or "Don't slow down outer walls" on). Printing several copies per plate lengthens layers.
4. Print a speed ladder coupon, rank the walls, and pick the fastest speed whose rank matches the slowest one. Read the time cost per step from the slicer's estimate. A steady speed matters as much as a slow one: Bambu ties gloss bands and Z banding to speed changes.
5. Choose the four fill patterns together with the speed: see [pattern-selection-guide.md](pattern-selection-guide.md).
6. The fan values above are specific to Bambu PLA Basic and PLA Matte @BBL H2C; recheck the cooling tab for any other filament.

## Not verified / open questions
- Whether H2C firmware caps travel acceleration 10000 to 9000: the slicer writes 10000; only a printer-side measurement could answer it.
- The community speed bands come from two posters on one 2023 thread with no printer named; not a Bambu number.
- Whether outer-wall speeds below 40 mm/s improve the surface on the H2C with PLA Basic or Matte: no source.
- Preset values may differ on other profile bundles.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- speed, acceleration, cooling and smoothing options
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- Speed page rows, cooling-row toggles
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode.cpp -- small perimeters, jerk guards, volumetric cap, M205 block
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCodeWriter.cpp -- acceleration clamp
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/libslic3r.h -- small perimeter macro
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Flow.cpp -- cross-section formula
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.16mm%20High%20Quality%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.12mm%20High%20Quality%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20High%20Quality%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/filament/Bambu%20PLA%20Matte%20%40BBL%20H2C.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/machine/Bambu%20Lab%20H2C%200.4%20nozzle.json
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process
- https://github.com/bambulab/BambuStudio/releases/tag/v02.08.02.61
- https://github.com/bambulab/BambuStudio/issues/1482
- https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang
- https://wiki.bambulab.com/en/software/bambu-studio/auto-cooling
- https://wiki.bambulab.com/en/software/bambu-studio/sequent-print
- https://wiki.bambulab.com/en/software/bambu-studio/high-speed-print-at-quality
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/different-gloss
- https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments
- https://forum.bambulab.com/t/possible-fix-for-ghosting-vfa-artifacts-with-speed-adjustments/13421 -- community only
