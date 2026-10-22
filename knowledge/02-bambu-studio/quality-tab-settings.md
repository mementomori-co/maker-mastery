# Quality tab: every setting (Process preset)
Applies to: both (H2C, P1S) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61). Values below are read from the H2C chain `0.20mm Standard @BBL H2C` -> `fdm_process_dual_0.20_nozzle_0.4` -> `fdm_process_dual_common` -> `fdm_process_common`; the keys themselves are Process-preset settings, not printer-specific.
Verified: 2026-10-04

Abbreviations: PC = [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); TAB = [Tab.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp). "Preset" = the value in the Bambu system profile chain at this tag. "Not set" = no chain file sets the key, so the code default applies (see [others-tab-settings.md](others-tab-settings.md) for why that is never "null").

## Facts
The Quality page has 7 sections in this order: Layer height, Line width, Seam, Precision, Ironing, Wall generator, Advanced. -- [TAB](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3199-3283

### Layer height
- Layer height `layer_height`: preset **0.2 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1030; [Layer height wiki](https://wiki.bambulab.com/en/software/bambu-studio/layer-height)
- Initial layer height `initial_layer_print_height`: preset **0.2 mm**; the tooltip says a slightly thicker first layer can improve plate adhesion. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3361
- Mixed color sublayer: not set -> **false**; no wiki help link. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6045

### Line width (preset values; code default for `line_width` is 0.4 mm)
- Default `line_width` **0.42 mm** (L2360); Initial layer `initial_layer_line_width` **0.5 mm** (L3352); Outer wall `outer_wall_line_width` **0.42 mm** (L2150); Inner wall `inner_wall_line_width` **0.45 mm** (L4576); Top surface `top_surface_line_width` **0.42 mm** (L5935); Sparse infill `sparse_infill_line_width` **0.45 mm** (L3944); Internal solid infill `internal_solid_infill_line_width` **0.42 mm** (L5261); Support `support_line_width` **0.42 mm** (L5536). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [Line width wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/line-width)

### Seam
- Seam position `seam_position` (Nearest / Aligned / Back / Random): preset **Aligned**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5043; [Seam wiki](https://wiki.bambulab.com/en/software/bambu-studio/Seam)
- Seam placement away from overhangs (experimental): preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5059
- Seam gap `seam_gap` (percent): not set -> **15 %**. Develop mode only: hidden unless Develop mode is on in Preferences. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5066
- Smart scarf seam application: not set -> **true**. Scarf application angle threshold `scarf_angle_threshold`: preset **155 deg**. Scarf around entire wall: preset **false**. Scarf steps: preset **10**. Scarf joint for inner walls: preset **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5075-5107
- Override filament scarf seam setting: preset **false** (the shipped tooltip has the typo "Overrider"). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5114
- Scarf seam type `seam_slope_type` (None / Contour / Contour and hole): preset **None**. Scarf start height `seam_slope_start_height` **10 %**; Scarf slope gap `seam_slope_gap` **0**; Scarf length `seam_slope_min_length` **10 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5121-5155
- Wipe speed `wipe_speed` (percent): not set -> **80 %**; Develop mode only. Role-based wipe speed: not set -> **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5164-5173

### Precision
- Slice gap closing radius: preset **0.049 mm**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5375
- Resolution `resolution`: preset **0.012 mm** (code default 0.01 mm). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4703; [Arc move wiki](https://wiki.bambulab.com/en/software/bambu-studio/acr-move)
- Arc fitting `enable_arc_fitting`: preset **true**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3564
- X-Y hole compensation `xy_hole_compensation` and X-Y contour compensation `xy_contour_compensation`: preset **0 mm** each. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6335-6345; [XY compensation wiki](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation)
- Auto circle contour-hole compensation `enable_circle_compensation`: preset **false**. The tooltip limits it to: "PLA Basic, PLA CF, PET CF, PETG CF and PETG HF". User Customized Offset: preset **0 mm**, and the row only shows while circle compensation is on. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6066-6074; [ConfigManipulation.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp) L1112
- Elephant foot compensation `elefant_foot_compensation`: `fdm_process_dual_0.20_nozzle_0.4` sets **0.15 mm**, overriding 0 in the common file. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [Elephant foot wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot)
- Precise wall: not set -> **false**; Develop mode only. Precise Z height: not set -> **false**; the tooltip calls it experimental. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3537-3555

### Ironing
See also [ironing-and-top-surface-pattern.md](ironing-and-top-surface-pattern.md).
- Ironing Type `ironing_type` (No ironing / Top surfaces / Topmost surface / All solid surfaces): preset **No ironing**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4069; [Ironing wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing Pattern `ironing_pattern`: two options in this version, Concentric and Rectilinear, default **Rectilinear**. The ironing wiki page lists three patterns (Lines, Concentric, Archimedean Spiral), which describes a different app version; do not use it for this version's list. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4086; [Ironing wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing speed `ironing_speed`: preset **30 mm/s** (code default 20). Ironing flow `ironing_flow`: the leaf H2C process sets **15 %** (common file 10 %). Ironing line spacing `ironing_spacing` **0.15 mm**. Ironing inset `ironing_inset` **0.21 mm** (introduced in Bambu Studio 1.10 per the wiki). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [Ironing wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing direction `ironing_angle`: not set -> **45 deg**; Develop mode only. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4138

### Wall generator
- Wall generator `wall_generator` (Classic / Arachne): preset **Classic** (code default Arachne). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6355; [Wall generator wiki](https://wiki.bambulab.com/en/software/bambu-studio/wall-generator)
- Order of walls (`wall_sequence`, effective **Inner/Outer**): set through a legacy key. `fdm_process_common` sets `wall_infill_order` to inner wall / outer wall / infill, and `handle_legacy` maps that to `wall_sequence`. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L7324; [Quality advanced wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings)
- Arachne sub-settings (preset values; each has a section on the wall-generator wiki page even where Tab.cpp gives no help link): Wall transitioning threshold angle **10 deg**, Wall transitioning filter margin **25 %**, Wall transition length **100 %**, Wall distribution count **1**, Minimum wall width **85 %**, Minimum feature size **25 %**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6369-6429; [Wall generator wiki](https://wiki.bambulab.com/en/software/bambu-studio/wall-generator)

### Advanced
- Print infill first: preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2208
- Bridge flow `bridge_flow`: the H2C 0.20 process sets **1** (common file 0.95). -- [Bridge wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)
- Thick bridges: not set -> **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1984
- Bridge counterbore holes: default **None**. The tooltip lists three modes: None (no bridge), Partially Bridged (only part of the unsupported area is bridged), Sacrificial Layer (a full sacrificial bridge layer). The linked bridge wiki page has no counterbore section. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [Bridge wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)
- Top surface flow ratio `top_solid_infill_flow_ratio`: preset **1**; Develop mode only. Initial layer flow ratio: not set -> **1**; Develop mode only. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1504-1515
- Only one wall on top surfaces `only_one_wall_top`: not set -> **Top surfaces**. Top area threshold: not set -> **200 %**; Develop mode only. Only one wall on first layer: not set -> **false** (its wiki help link has no matching section). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1524-1546
- Detect overhang wall `detect_overhang_wall`: preset **true**; Develop mode only. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- Smooth speed discontinuity area: not set -> **true**. Smooth coefficient `smooth_coefficient`: `fdm_process_dual_common` sets **4** (common file 80). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4549
- Avoid crossing wall `reduce_crossing_wall`: preset **false**. Max detour length `max_travel_detour_distance`: preset **0**. Includes support: preset **false**. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1164-1190
- Smoothing wall speed along Z (experimental) `z_direction_outwall_speed_continuous`: `fdm_process_dual_common` sets **true** (common file false). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)

## In practice
- Several Quality rows are Develop-mode only and will not show unless you turn on Develop mode in Preferences: Seam gap, Wipe speed, Precise wall, Ironing direction, Top surface flow ratio, Initial layer flow ratio, Top area threshold, Detect overhang wall, and Object flow ratio. The wiki confirms some parameters only appear with Developer mode on. -- [Quality advanced wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings)
- A "not set" row falls back to the PrintConfig.cpp default, never to "off".
- For this version's ironing pattern list, trust the source (2 patterns), not the wiki (3).
- "Order of walls" shows Inner/Outer through a legacy key. Check `handle_legacy` before assuming an unset modern key means a fallback.
- Profile bundles update independently of the app; compare the process JSON files in `%APPDATA%\BambuStudio\system\BBL\process\` with the tag files before trusting the preset values here.

## Not verified / open questions
- Object flow ratio `print_flow_ratio`: Tab.cpp gives no help link and the quality-advanced wiki page has no section for it; no correct source found. Develop mode only.
- Max detour length = 0: the PrintConfig.cpp tooltip says zero disables it, while the wiki says 0 means no limit on the detour. They disagree. Test with a controlled slice on your printer before relying on it.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- labels, tooltips, defaults, modes
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- section order and help links
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ConfigManipulation.cpp -- User Customized Offset visibility
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Preset.cpp -- missing keys fall back to code defaults
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_common.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json
- https://wiki.bambulab.com/en/software/bambu-studio/layer-height
- https://wiki.bambulab.com/en/software/bambu-studio/Seam
- https://wiki.bambulab.com/en/software/bambu-studio/acr-move
- https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing
- https://wiki.bambulab.com/en/software/bambu-studio/wall-generator
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/line-width
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings
