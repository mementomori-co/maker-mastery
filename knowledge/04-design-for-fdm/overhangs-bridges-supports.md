# Overhangs, bridges and supports (Bambu Studio, 0.4 mm nozzle)

Applies to: H2C | P1S | both · Bambu Studio 2.8.02.61 (code identical at `master` and tag `v02.08.02.61` when checked)
Verified: 2026-10-03

## Facts

**Threshold angle (when auto-support starts)**
- `support_threshold_angle` (Process > Support > Threshold angle): support is generated for overhangs whose slope is below this angle; a larger angle means more support. Range 1-90 degrees, measured from horizontal, code default 30 degrees. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support); [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6005
- H2C presets: `support_threshold_angle = 30` in `0.20mm Standard @BBL H2C` and 25 in `0.16mm High Quality @BBL H2C` (set in `fdm_process_common` and `fdm_process_dual_0.16_nozzle_0.4`). -- [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- The wiki gives two different numbers, both official. The support page calls 30 degrees from horizontal a safe angle without support; the overhang troubleshooting page recommends supports below 45 degrees and none above. Both are measured from the bed. Use the number for the context you are in, not one rule of thumb. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support); [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)
- The wiki treats "overhang angle" (slope of the surface against the bed) and "overhang threshold" (share of a line's width that is unsupported) as different things, even though both are called "overhang". -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)
- Raising the threshold angle gives more support, not less (the wiki shows a 5 vs 85 degree comparison). -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)

**Support type and style**
- Normal support projects overhangs straight down to the bed. Tree support samples overhangs into nodes, carries them down, and may grow or move nodes away from the model for strength and clearance. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- `support_type` values: normal(auto), tree(auto), normal(manual), tree(manual). Manual modes only generate support at enforcers. Code default `normal(auto)`. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5604
- The H2C presets ship with Support > Enable support off (`enable_support = 0`), `support_type = tree(auto)` and `support_style = default`; full detail is in [support-settings.md](../02-bambu-studio/support-settings.md). Consequence for design: threshold angle, tree type and bridge settings do nothing until Enable support is switched on. -- [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- `support_style` values: default, grid, snug, tree_slim, tree_strong, tree_hybrid, tree_organic. Per the tooltip, Default means organic tree in most cases, and hybrid tree with adaptive layer height or a soluble interface. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5959
- Normal-support styles: Grid expands the support region into rectangles (the default for normal support); Snug keeps the region tight to the overhang. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- With Style = Default the slicer uses Tree Organic, switching to Tree Hybrid only when a support-filament interface or adaptive layer height is on (Tree Organic does not support adaptive layer height). The wiki says tree support has "three styles" but then lists four (Slim, Strong, Organic, Hybrid). -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)

**Bridges**
- `max_bridge_length` (Max bridge length): the longest bridge that needs no support. 0 supports every bridge; a very large value supports none. Code default 10 mm; it only applies once supports are enabled. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2065
- Per the wiki, a rectangular overhang counts as a bridge. A short bridge prints fine because both ends are anchored; a bridge longer than Max bridge length is split into equal segments and only the contact points are supported. For tree support, Max bridge length replaces "Don't support bridges". -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support), section "Tree Support-Only Options"
- `thick_bridges` (Thick bridges): enabled makes bridges more reliable over longer spans but rougher-looking; disabled looks better but only holds for shorter spans. Code default false, and the H2C presets do not set it. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2057; [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- A thick bridge extrudes at nozzle diameter (for example a 0.4 mm line from a 0.4 mm nozzle). The setting affects external bridges only; internal bridges, such as over sparse infill, always print thick. -- [Bambu wiki, bridge parameter](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)
- `bridge_speed` (Bridge speed): code default 25 mm/s, Advanced mode, set per nozzle. The H2C Standard and High Quality presets set 50 mm/s in all 5 slots. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1755; [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- Slower bridges give the filament more time to cool, but slower is not always better; the wiki says to tune bridge speed per machine and filament. A speed change applies only to the selected nozzle. -- [Bambu wiki, bridge parameter](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)
- Bridge flow: the wiki's one test print found Bridge Flow 1.5 at 30-40 mm/s and 1.6 at 10-20 mm/s both acceptable (one unnamed filament and machine, not a general rule). The page gives 1.4-1.7 as the common range for materials such as PLA. -- [Bambu wiki, bridge parameter](https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge)

**Overhang-wall slowdown (a separate feature from bridges)**
- Slow down for overhangs is on by default; a speed of 0 mm/s means no slowdown. Overhang degree runs from 0% (no overhang) to 100% (a fully overhanging wall, i.e. a bridge). Wall lines are grouped by overhang degree and mapped to speeds, with smooth transitions since Bambu Studio 1.9.1. -- [Bambu wiki, slow down for overhang](https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang)
- The wiki's "10-60 mm/s" overhang speed range is troubleshooting advice for slowing further, not a default range. -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)
- Detect overhang wall applies bridge speed once a wall reaches 100% overhang. Its smoothing option (added in 1.9.4) is on by default, with a smoothing coefficient usually set between 1 and 200. -- [Bambu wiki, quality advance settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings)
- Wall order Inner/outer (the default) helps overhangs: the inner wall prints first and supports the outer wall's overhang, reducing curl and collapse on that surface. -- [Bambu wiki, quality advance settings](https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings)

**Overhang failure: cause and fix**
- Cause: the extruded filament does not cool in time on the overhanging surface, so it droops. -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang) (page updated 2026-06-24)
- Fix besides supports, for PLA only: lower the nozzle temperature for later layers to about 205 C and raise the overhang fan to 100%. -- [Bambu wiki, overhang](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang)

**Bridging failure: cause and fix**
- Cause: unsupported filament keeps a round cross-section instead of flattening, so with default Bridge Flow the lines can be narrower than their spacing and gaps appear. -- [Bambu wiki, bridging](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/bridging) (page updated 2026-04-14)
- Fix order: tune bridge flow first (Quality tab), then bridge speed (Speed tab), testing 1.4-1.7 Bridge Flow for materials such as PLA. The wiki credits this method to a MakerWorld creator. -- [Bambu wiki, bridging](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/bridging)

**Support filament pairing**
- PLA Basic or PLA-CF main filament: pair with Bambu Support for PLA, Support for PLA/PETG, PVA, or another suitable support filament. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- PETG Basic, PETG HF or PETG-CF main filament: pair with Support for PLA/PETG or another suitable support filament. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- Do not mismatch (for example Support for PLA under ABS/ASA/PC/PAHT-CF, or Support for PA/PET under PLA/PETG): it risks clogging the extruder or nozzle. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- For most jobs, use support filament only for the support interface and the main filament for the support body, to save time. All-support-filament structures are for special cases, because thin, tall ones may deform or collapse. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- `support_interface_filament` defaults to 0 ("Default": no dedicated interface filament; the current filament is used). -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5750
- With 0 interface layers, the first support layer under the model prints as lines that can sag; with 3 interface layers, a stable flat platform forms. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)
- Top Z distance can be 0 only when the interface is a dedicated support filament (Support for PLA, PLA/PETG or PA/PET). If the interface is the body filament, Bambu recommends about 0.2 instead (unit not stated, presumably mm), or the support is hard to remove. -- [Bambu wiki, support](https://wiki.bambulab.com/en/software/bambu-studio/support)

**Standard vs High Quality on the H2C (0.4 mm nozzle)**
- `0.20mm Standard @BBL H2C`: 0.2 mm layers, 5 top / 3 bottom shells, faster outer and inner wall speeds, threshold 30 degrees. `0.16mm High Quality @BBL H2C`: 0.16 mm layers, 6 top / 4 bottom shells, outer wall 60 mm/s, inner wall 150 mm/s, threshold 25 degrees. Both use line width 0.42 mm, 2 wall loops, bridge speed 50 and supports off. Full table in [h2c-process-presets.md](../02-bambu-studio/h2c-process-presets.md). -- [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)

## In practice
- Supports are off in the H2C presets. Switching on Support > Enable support is what makes the threshold angle, tree type and Max bridge length take effect at all.
- Design the geometry first: keep overhangs above about 45 degrees from horizontal (overhang troubleshooting page), or expect support below 30 or 25 degrees once supports are on.
- For short bridges without supports, the levers are bridge speed, bridge flow and Thick bridges, not the threshold angle. Bridges still need well-anchored ends.
- Match support filament to the main filament's temperature family.
- For removable supports, use a dedicated support filament for the interface with Top Z distance 0. If the interface is body filament, start near 0.2 and measure. For how a typed Top Z is rounded in each support style, see [support-top-z-same-filament.md](../02-bambu-studio/support-top-z-same-filament.md). Verify removal on your own printer with a test coupon.

## Not verified / open questions
- Whether the 2.8.02.61 GUI shows a "Hybrid (auto)" support type. The wiki lists one, but the code's `support_type` has only normal/tree x auto/manual; hybrid exists as a tree style. Not checked in the running GUI.
- Which of the 5 per-slot wall speed values maps to which H2C nozzle variant is covered in [speed-tab-settings.md](../02-bambu-studio/speed-tab-settings.md), not here.
- The unit of the "about 0.2" Top Z recommendation; the wiki never states mm.

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/support -- support types and styles, threshold angle, max bridge length, filament pairing, interface layers, Top Z distance
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/overhang -- overhang angle vs threshold, 45 degree advice, troubleshooting
- https://wiki.bambulab.com/en/filament-acc/filament/print-quality/bridging -- bridging failure cause and fix order
- https://wiki.bambulab.com/en/software/bambu-studio/slow-down-for-overhang -- overhang slowdown
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/quality-advance-settings -- detect overhang wall, wall order
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/bridge -- thick bridges, bridge speed and flow
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- setting keys, defaults, tooltips
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process -- H2C preset values
