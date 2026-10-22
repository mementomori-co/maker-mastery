# Others tab: every setting (Process preset)
Applies to: both (H2C, P1S) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61). Values below are read from the H2C chain `0.20mm Standard @BBL H2C` -> `fdm_process_dual_0.20_nozzle_0.4` -> `fdm_process_dual_common` -> `fdm_process_common`; the keys themselves are Process-preset settings, not printer-specific.
Verified: 2026-10-04

Abbreviations: PC = [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); TAB = [Tab.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp); H2C = [0.20mm Standard @BBL H2C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json); FPC = [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json).

"Preset value" means the value in the Bambu system profile chain at this tag. "Not set in chain" means no file in the chain sets the key, so the code default applies.

## Facts
- **A key missing from a profile's JSON is not "null": it falls back to the code default.** The root preset starts from `default_preset.config` and the JSON is applied on top, so every row marked "not set in chain" still has a real effective value from PrintConfig.cpp. -- [Preset.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Preset.cpp) L1468-1469

### Bed adhesion
- Skirt loops `skirt_loops` (integer, 0-10): zero disables the skirt; code default 1, preset **0**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5224
- Skirt height (integer, layers, max 10000): number of skirt layers; preset **1**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5198
- Skirt distance (0-55 mm, Develop mode only): gap from skirt to brim or object; preset **2 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5182
- Brim type `brim_type` (6 options): not set in the H2C chain, so the effective value is the code default `btAutoBrim` = **Auto**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1705-1729; [Auto brim wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim)
- Brim width (0-100 mm): preset **5 mm**. The GUI help link points at anchor `auto-brim#manual`, but the wiki page's real headings are `manual-brim` and `brim-width`. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1695; [Auto brim wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim)
- Brim-object gap (0-2 mm; help anchor `#brim-object-gap` is correct): preset **0.1 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1734; [Auto brim wiki](https://wiki.bambulab.com/en/software/bambu-studio/auto-brim)

### Prime tower
- Enable `enable_prime_tower`: code default false, preset **true** (set in FPC). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6054-6056; [Prime tower wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower)
- Skip points: not set in chain -> code default **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6273-6275
- Internal ribs `prime_tower_enable_framework`: preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6062; [Prime tower wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower)
- Width `prime_tower_width` (min 2 mm, code default 35 mm): the H2C process profile sets **60 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6215; [H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json)
- Max speed (min 10 mm/s): preset **90 mm/s**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6230; [Prime tower wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower)
- Tower brim width `prime_tower_brim_width` (-1 = Auto, code default 3): the H2C profile sets **-1 (Auto)**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6243-6250; [H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json)
- Infill gap (percent, min 100 %): not set -> code default **150 %**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6296-6300
- Rib wall: not set -> code default **true**. Extra rib length (max 300 mm): not set -> **0 mm**. Rib width (0-300 mm): not set -> **8 mm**. Fillet wall: not set -> **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6260-6292
- The Extra rib length tooltip is two C++ string literals joined without a space, so the GUI shows "size.However"; cosmetic only. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6260
- Enable tower interface features `enable_tower_interface_features` (Develop mode, code default false): the H2C profile sets **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2998-2999; [H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json)
- No sparse layers (experimental) `no_sparse_layers` (Develop mode): preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5368-5372

### Flush options
- Flush into objects' infill `flush_into_infill`: not set -> **false**. Flush into this object `flush_into_objects`: not set -> **false**. Flush into objects' support: code default **true** (L6317). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6305-6325; [Reduce waste wiki](https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change)
- The three help anchors in Tab.cpp (`#wipe-into-infill`, `#wipe-into-object`, `#wipe-into-support-enabled-by-default`) are stale; the wiki's real heading ids start with `flush-into-`. -- [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp); [Reduce waste wiki](https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change)

### Special mode
- Slicing Mode `slicing_mode` (3 options): not set -> **Regular**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5388-5397; [Special slicing modes wiki](https://wiki.bambulab.com/en/software/bambu-studio/special-slicing-modes)
- Print sequence `print_sequence` (by layer / by object): preset **by layer**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1799-1804; [Print by object wiki](https://wiki.bambulab.com/en/software/bambu-studio/sequent-print)
- Spiral vase `spiral_mode`: preset **false**. Smooth Spiral `spiral_mode_smooth`: not set -> **false**. Max XY Smoothing `spiral_mode_max_xy_smoothing` (percent, 0-1000): not set -> **200 % of nozzle diameter**. The help anchors `spiral-vase#smooth` and `#max-xy-smoothing` do not exist on the wiki page. The Smooth Spiral tooltip has a joined-string typo ("wellresulting"). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5282-5305; [Spiral vase wiki](https://wiki.bambulab.com/en/software/bambu-studio/spiral-vase)
- Timelapse `timelapse_type` (0 = Traditional, 1 = Smooth): not set -> **Traditional**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5309-5322; [Timelapse wiki](https://wiki.bambulab.com/en/software/bambu-studio/Timelapse)

### Fuzzy skin
- Fuzzy Skin `fuzzy_skin` (5 options): preset **none**. Preset sub-values: generator mode displacement, noise type classic, point distance 0.8 mm (0-5), thickness 0.3 mm (0-1; the tooltip says to keep it below the outer wall line width), feature size `fuzzy_skin_scale` 1.0, noise octaves 4, noise persistence 0.5, apply to first layer false. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3419-3526; [Fuzzy skin wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/fuzzy-skin)

### Advanced
- Enable clumping detection: preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3593-3594; [Clumping detection wiki](https://wiki.bambulab.com/en/software/bambu-studio/nozzle-clumping-detection-by-probing)
- Order-independent overlap carving (Develop mode): not set -> **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3600-3602
- Interlocking: Use beam interlocking -> **false**; depth of a segmented region -> **0 mm** (disabled); beam width -> **0.8 mm**; direction -> **22.5 deg**; beam layers -> **2**; depth -> **2 cells**; boundary avoidance -> **2 cells** (all not set in chain, code defaults). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4012-4067
- Filament for features: Sparse infill filament, Solid infill filament and Walls filament: preset **0** for all three (reading 0 as "use the object's own filament" is an interpretation, not verified). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3936-3939, L5253-5256, L4568-4571

### G-code output
- Reduce infill retraction (Disabled / Auto / Enabled): preset **Auto**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4511-4522
- Add line number (Develop mode): not set -> **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3573-3575
- Exclude objects: not set -> code default **true** (L3758). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3756-3758
- Filename format (Develop mode; code default `[input_filename_base].gcode`): preset `{input_filename_base}_{filament_type[0]}_{print_time}.gcode`. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4536-4538; [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3534-3536
- Post-processing Scripts: not set -> empty. Notes > Process notes: not set -> empty. Tab.cpp enlarges both text boxes over the PrintConfig heights. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2344, L4618-4621; [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3541-3550

## In practice
- A row that reads "null" or is missing in a resolved profile JSON is never a real "off" state. Look up the code default in PrintConfig.cpp before trusting it.
- Several help links on this tab land at the top of the wiki page instead of the section (stale anchors listed above). The Prime tower anchors (`#internal-ribs`, `#max-speed`, `#infill-gap`, `#rib-wall`) and Brim `#brim-object-gap` are correct.
- Profile bundles update independently of the app. Before trusting any preset value above on your install, open `%APPDATA%\BambuStudio\system\BBL.json`, read its `"version"`, and compare the process JSON files there with the tag files linked here.
- Leave the two tooltip typos as they are when quoting them; the meaning is unchanged.

## Not verified / open questions
- Preset values were checked against one profile bundle; a newer bundle may change them. Verify on your own install.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- labels, ranges, defaults, modes for every Others-tab option
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- page layout, help anchors, text-box sizes
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Preset.cpp -- missing keys fall back to the code default
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json -- H2C prime tower width, tower brim, tower interface
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json -- common process preset values
- https://wiki.bambulab.com/en/software/bambu-studio/auto-brim
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/prime-tower
- https://wiki.bambulab.com/en/software/bambu-studio/reduce-wasting-during-filament-change
- https://wiki.bambulab.com/en/software/bambu-studio/special-slicing-modes
- https://wiki.bambulab.com/en/software/bambu-studio/sequent-print
- https://wiki.bambulab.com/en/software/bambu-studio/spiral-vase
- https://wiki.bambulab.com/en/software/bambu-studio/Timelapse
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/fuzzy-skin
- https://wiki.bambulab.com/en/software/bambu-studio/nozzle-clumping-detection-by-probing
