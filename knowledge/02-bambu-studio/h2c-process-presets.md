# H2C 0.4 mm process presets: the five presets compared, brim, seam, walls
Applies to: H2C (Bambu Lab H2C 0.4 nozzle) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61); profile bundle `BBL.json` 02.08.00.05
Verified: 2026-10-05

Every process preset resolves through a chain: leaf -> `fdm_process_dual_0.XX_nozzle_0.4` -> `fdm_process_dual_common` -> `fdm_process_common`. Values below were resolved over that chain. Speed arrays are indexed by `print_extruder_variant` (Direct Drive Standard, Direct Drive High Flow, Direct Drive E3D High Flow, then the second extruder's Standard and High Flow; see [speed-tab-settings.md](speed-tab-settings.md)). Speeds are mm/s, accelerations mm/s2. Profile values can change with each bundle update, so check them against your installed bundle.

## Facts

### Which presets exist
- The five main 0.4 mm H2C processes: `0.12mm High Quality @BBL H2C`, `0.16mm Standard @BBL H2C`, `0.16mm High Quality @BBL H2C`, `0.20mm Standard @BBL H2C`, `0.20mm High Quality @BBL H2C`. Also present: `0.08mm High Quality @BBL H2C` and `0.24mm Standard @BBL H2C`. Each lists `compatible_printers: ['Bambu Lab H2C 0.4 nozzle']`. No preset named "Fine" or "Optimal" exists for the H2C. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- The descriptions say the Standard presets prioritise speed and the High Quality presets prioritise print quality and strength; the 0.12 HQ preset has no description. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Machine preset `Bambu Lab H2C 0.4 nozzle`: default process `0.20mm Standard @BBL H2C`, default filament `Bambu PLA Basic @BBL H2C`. `Bambu Lab H2C`: default bed type Textured PEI Plate; Cool Plate and Smooth PEI / High Temp Plate are listed as not supported. — [BBL machine profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/machine)

### The keys that differ (0.12 HQ | 0.16 HQ | 0.16 Std | 0.20 HQ | 0.20 Std)
Source for every row: the five leaf JSONs and their parents in [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process) (bundle 02.08.00.05). Where a value has five entries it is the per-variant speed array.

| key | 0.12 HQ | 0.16 HQ | 0.16 Std | 0.20 HQ | 0.20 Std |
|---|---|---|---|---|---|
| layer_height (mm) | 0.12 | 0.16 | 0.16 | 0.2 | 0.2 |
| top_shell_layers | 9 | 6 | 6 | 6 | 5 |
| bottom_shell_layers | 7 | 4 | 4 | 4 | 3 |
| top_shell_thickness (mm) | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 |
| sparse_infill_pattern | gyroid | gyroid | grid | grid | grid |
| default_acceleration | 4000 | 4000 | 8000 | 4000 | 8000 |
| outer_wall_acceleration | 2000 | 2000 | 5000 | 2000 | 5000 |
| outer_wall_speed | 60 | 60 | 200 | 60 | 200,500,500,200,500 |
| inner_wall_speed | 120 | 150 | 300 | 150 | 300,600,600,300,600 |
| sparse_infill_speed | 100 | 180 | 350,600,600,350,600 | 200 | 350,600,600,350,600 |
| internal_solid_infill_speed | 150 | 180 | 250,300,300,250,300 | 200 | 250,600,600,250,600 |
| top_surface_speed | 150 | 150 | 200 | 150 | 200 |
| gap_infill_speed | 50 | 250 | 250 | 250 | 250,150,150,250,150 |
| initial_layer_speed | 40 | 50 | 50 | 50 | 50 |
| initial_layer_infill_speed | 70 | 105 | 105 | 105 | 105 |
| travel_speed | 500 | 500 | 1000 | 500 | 1000 |
| overhang_1_4_speed | 60 | 60 | 60 | 60 | 0 |
| overhang_2_4_speed | 30 | 30 | 30 | 30 | 50 |
| overhang_3_4_speed | 10 | 10 | 10 | 10 | 30 |
| support_top_z_distance (mm) | 0.12 | 0.16 | 0.16 | 0.2 | 0.2 |
| support_bottom_z_distance (mm) | 0.12 | 0.16 | 0.16 | 0.2 | 0.2 |
| support_threshold_angle (deg) | 20 | 25 | 25 | 30 | 30 |
| ironing_flow | 10% | 25% | 10% | 10% | 15% |
| ironing_speed | 30 | 20 | 30 | 30 | 30 |
| top_color_penetration_layers | 7 | 6 | 6 | 5 | 5 |
| bottom_color_penetration_layers | 5 | 4 | 4 | 3 | 3 |

- High Quality presets: outer wall 60 mm/s and outer-wall acceleration 2000 mm/s2. Standard: outer wall 200 mm/s (500 mm/s on High Flow variants of 0.20 Std) and 5000 mm/s2. Support threshold angle and Z gaps follow layer height. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Keys that do NOT differ across the five: wall_loops 2; wall_generator classic; sparse_infill_density 15%; line_width and outer_wall_line_width 0.42 mm; initial_layer_print_height 0.2 mm; elefant_foot_compensation 0.15 mm (set in each `fdm_process_dual_0.XX_nozzle_0.4`, overriding the common 0); only_one_wall_top 1; detect_thin_wall 0; seam_position aligned; brim_width 5 mm; brim_object_gap 0.1 mm; overhang_4_4_speed and overhang_totally_speed 10; bridge_speed 50; support_speed 150; support_interface_speed 80; enable_overhang_speed 1; z_direction_outwall_speed_continuous 1. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)

### Seam
- `seam_position` (Quality > Seam > Seam position): Nearest, Aligned, Back, Random; code default Aligned, and all five presets resolve `aligned`. — [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- "Back" picks the candidate with the largest Y, i.e. the rear of the bed (+Y); the wiki says only "behind the model". See [seam-painting.md](seam-painting.md) for how painted seams interact. — [SeamPlacer.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp), [wiki: seam](https://wiki.bambulab.com/en/software/bambu-studio/Seam)
- Wiki: Nearest prefers concave non-overhang vertices first; Aligned uses the same candidates but chooses the one nearest the previous layer's start point; Random can leave "zits" on the surface. Seam gap defaults to 15 % of nozzle diameter (Developer mode); scarf seams came in Studio 1.9, with a per-filament switch since 1.10. — [wiki: seam](https://wiki.bambulab.com/en/software/bambu-studio/Seam), [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)

### Brim
- `brim_type`: Auto, Painted, Outer brim only, Inner brim only, Outer and inner brim, No-brim; default Auto. `brim_width` code default 0, profile 5 mm; `brim_object_gap` code default 0, profile 0.1 mm. — [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Wiki: taller parts with small footprints usually need a wider brim so the nozzle does not topple them; a smaller brim gap bonds more strongly, a larger gap is easier to remove; a gap that persists at 0 is usually caused by Elephant foot compensation. — [wiki: brim](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim)
- Painted brim ears need Brim type set to "Painted"; left-click adds, right-click deletes. — [wiki: auto brim](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim), [wiki: brim ears](https://wiki.bambulab.com/en/software/bambu-studio/brim-ears)
- Since Studio 1.10.0 you can paint supports on vertical surfaces, which the wiki recommends for tall thin parts to reduce collapse. — [wiki: support painting](https://wiki.bambulab.com/en/software/bambu-studio/support-painting)
- Community only: forum users suggest a 0 brim-object gap plus painted vertical support for tall thin parts, and Tree Slim / Tree Hybrid supports with a small support/object XY distance. — [forum: tall thin falling over](https://forum.bambulab.com/t/tall-thin-falling-over/164364), [forum: long thin components](https://forum.bambulab.com/t/best-way-to-support-long-thin-components/253625)

### Walls and wall speed
- `wall_loops` default 2. `wall_generator`: code default Arachne, but all five H2C presets resolve `classic`. `detect_thin_wall` default false. The `outer_wall_speed` tooltip says the outer wall is usually slower than the inner wall for better quality. — [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Wiki: wall speeds strongly affect surface quality, especially on overhangs, and lower wall speed is recommended for models with obvious overhangs; slow-down-for-overhang is on by default and 0 mm/s means no slowing. — [wiki: slow down for overhang](https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang)
- "Smoothing Wall Speed Along Z" (`z_direction_outwall_speed_continuous`) is aimed at models with high surface-quality needs such as figurines and display pieces, at the cost of overall speed; the H2C dual common profile turns it on. The default wall order (inner walls first, outer last) gives better quality on overhangs. — [wiki: quality advanced settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings), [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)

### PLA presets and H2 chamber rules (cross-reference)
- `Bambu PLA Basic @BBL H2C` and `Bambu PLA Matte @BBL H2C` both use nozzle 220 C, Textured PEI 55 C, Cool Plate 35 C. The PLA Basic TDS gives bed 35-45 C and nozzle 190-230 C, so the profile's 55 C Textured PEI value is above the TDS bed range. See [../03-materials/](../03-materials/) for the full comparison. — [BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament), [PLA Basic TDS](https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf)
- `filament_scarf_height` resolves to 10 % for PLA Basic (from `fdm_filament_common`) and 5 % for PLA Matte. — [BBL filament profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament)
- H2D/H2C rule: low heat-deflection filaments (PLA, PETG, TPU, PLA-CF and others) are prohibited when the chamber exceeds 45 C, high- and low-temperature filaments must not be printed together, and Bambu Studio enforces this while slicing. — [wiki: H2D/H2C multi-material guide](https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit)
- H2 air management is set automatically by filament type during slicing; cooling mode (for PLA/TPU) keeps the chamber heat circulation fan off and runs the exhaust fan at 30 % for PLA. — [wiki: H2 cooling fan system](https://wiki.bambulab.com/en/h2/manual/cooling-fan-system)
- H2C spec: active chamber heating up to 65 C, heatbed up to 120 C, Textured PEI Plate included, Textured PEI and Engineering plates supported. — [H2C specs](https://bambulab.com/en/h2c/specs)

## In practice
- Start from `0.20mm Standard @BBL H2C`. The main print-time lever between presets is outer-wall speed: 200/500 mm/s (Standard) versus 60 mm/s (High Quality).
- "Back" seam means +Y of the plate: rotate the part so its hidden face points to +Y before relying on it.
- Resolve profile values through the full chain, not the leaf JSON; the leaf rarely contains the key.

## Not verified / open questions
- Whether the AppData and Program Files copies of the profile bundle are identical after an update; check your own install.
- Values change with bundle updates; re-check the table after updating Bambu Studio.

Sources:
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process — the process presets and their parents
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/filament — PLA Basic / Matte H2C presets
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/machine — H2C machine presets
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp — tooltips, enums, defaults
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp — Back = largest Y
- https://wiki.bambulab.com/en/software/bambu-studio/Seam — seam options
- https://wiki.bambulab.com/en/software/bambu-studio/auto-brim — brim logic and gap
- https://wiki.bambulab.com/en/software/bambu-studio/brim-ears — painted brim
- https://wiki.bambulab.com/en/software/bambu-studio/support-painting — vertical-surface support painting
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings — Smoothing Wall Speed Along Z, wall order
- https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang — wall speed vs overhangs
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-filament-config-limit — low-temperature filament rule
- https://wiki.bambulab.com/en/h2/manual/cooling-fan-system — H2 air management
- https://bambulab.com/en/h2c/specs — H2C chamber and plate spec
- https://store.bblcdn.com/s1/default/58b85d0f3db94878854a28fdb8a0006e/Bambu_PLA_Basic_Technical_Data_Sheet.pdf — PLA Basic TDS
- https://forum.bambulab.com/t/tall-thin-falling-over/164364 — community
- https://forum.bambulab.com/t/best-way-to-support-long-thin-components/253625 — community
