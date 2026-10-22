# Support Top Z distance for same-filament support
Applies to: H2C | P1S · Bambu Studio 02.08.02.61 (tag v02.08.02.61)
Verified: 2026-10-07

Scope: what the support gap keys are called, what the H2C presets set, what Bambu's wiki says about a same-filament gap, and what a typed Top Z becomes in each support style. The gap values below come from reading the code; confirm them on your own slice with the read-back method in "In practice". Short links:
- PC = [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- SL = [Slicing.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Slicing.cpp)
- SM = [SupportMaterial.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportMaterial.cpp)
- TS = [TreeSupport.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp)
- TSC = [TreeSupportCommon.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupportCommon.hpp)
- TS3 = [TreeSupport3D.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport3D.cpp)
- SP = [SupportParameters.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp)
- PROC = [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- WIKI = [Support wiki](https://wiki.bambulab.com/en/software/bambu-studio/support)

## Facts

### The keys
- Support > Advanced > **Top Z distance** `support_top_z_distance` (mm): the gap between the top support interface and the object. Code default 0.2 mm, no min or max in code. Advanced mode. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5479-5495
- The "0 (soluble) / 0.1 (semi-detachable) / 0.2 (detachable)" drop-down labels for Top Z sit in an `#if 0` block and are not shown. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5486-5493
- Top Z = 0 makes the slicer treat the interface as soluble. -- [SL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Slicing.cpp) L77; [TS3](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport3D.cpp) L142-144
- A source comment says Top Z may be rounded to whole layers when independent support layer height is off. That comment is incomplete: Tree Organic rounds regardless (table below). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5477-5478
- Support > Advanced > **Top interface layers** `support_interface_top_layers`: 0 to 3, code default 3. **Top interface spacing** `support_interface_spacing`: 0 = solid interface (needed for support ironing), code default 0.5 mm. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5562-5602
- Support > **Support/raft interface** `support_interface_filament` and **Support/raft base** `support_filament`: 0 = "Default", meaning the current filament is used. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5520-5560
- Support > **Type**: normal(auto), tree(auto), normal(manual), tree(manual); there is no hybrid type, and a legacy `hybrid(auto)` is rewritten to tree(auto) on load. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5406-5421, L7303-7304
- Support > **Style**: Default, Grid, Snug, Tree Slim, Tree Strong, Tree Hybrid, Tree Organic. The tooltip says Default is organic tree for most cases and hybrid tree with adaptive layer height or a soluble interface. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5761-5788
- Support > Advanced > **Support critical regions only**: Advanced mode, default false; applies only to auto types and still keeps cantilevers. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5463-5468; [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L1212-1244
- `independent_support_layer_height` (default true): support layers use their own height so the Z gap can be customised; the tooltip says it is invalid when the prime tower is enabled. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5799-5805
- "Z overrides X/Y" `top_z_overrides_xy_distance` (default false) is only recommended with Hybrid tree; with it off the XY gap is min(XY distance, max(0.2, Top Z)). XY distance default 0.35 mm; a source comment warns that too small a spacing makes support touch the object. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5423-5432, L5790-5797; [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp) L92-94

### What the H2C presets set
- `0.20mm Standard @BBL H2C` and `0.16mm High Quality @BBL H2C` both inherit `fdm_process_dual_0.xx_nozzle_0.4` -> `fdm_process_dual_common` -> `fdm_process_common`. -- [PROC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- `fdm_process_common.json` sets Top Z 0.2, bottom Z 0.2, top and bottom interface layers 2, interface spacing 0.5 mm, interface and support filament Default, tree(auto), style Default, XY 0.35 mm, threshold 30 deg, support off, prime tower on, layer height 0.2 mm, adaptive layer height off. The 0.20 Standard leaf only changes support speeds. -- [PROC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- `0.16mm High Quality @BBL H2C` overrides: layer height 0.16, Top Z 0.16, bottom Z 0.16, threshold 25 deg. -- [fdm_process_dual_0.16_nozzle_0.4.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_0.16_nozzle_0.4.json)
- No BBL process file sets Support critical regions only or independent support layer height, so the code defaults apply (off and on). -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5468, L5805; [BBL process folder](https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process)
- A single-filament plate switches the prime tower off, which leaves independent layer height on. A prime tower that stays on forces it off. Smooth timelapse or wrapping detection keep the tower on even with one filament. `timelapse_type` (Traditional / Smooth) is a process setting at Others > Special mode > Timelapse, saved in the project and read at slice time; the send dialog only offers Timelapse on/off. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L7722-7749; [PrintApply.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintApply.cpp) L1205, L1866; [Preset.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Preset.cpp) L1070; [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp) L3467, L3503; [SelectMachine.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SelectMachine.cpp) L201-202, L652

### What the wiki says (paraphrased)
- Same filament: a gap is needed so support can be removed; with the same filament for support and part you trade easy removal against support-surface quality, and tuning cannot fully escape that. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- When the interface uses the body filament, the wiki advises about 0.2 for Top Z rather than 0, or the support will be very hard to remove (no unit or layer-height condition given). -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- Larger Top Z = easier removal, lower interface quality; smaller = the reverse. More top interface layers improve overhang quality for a little more material; 0 can sag; 3 gives a flat platform; no sag at all only when Top Z is also 0. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- The only interface-spacing advice on the page is for a concentric pattern with support material; there is no same-filament spacing guidance. Interlaced and grid interfaces may be harder to remove than plain rectilinear; Tree Strong branches can be hard to remove; larger branch distance or diameter improves the surface but makes removal harder. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- The page calls Tree Hybrid the current default style, but its own note and the code pick Tree Organic. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- Critical overhangs are small overhangs, cantilevers and sharp tails. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support)
- The 2-hour support-removal advice targets moisture-prone PA and PVA, not PLA; a print-finish page repeats it for PA carbon-fibre grades. -- [WIKI](https://wiki.bambulab.com/en/software/bambu-studio/support); [Print finish wiki](https://wiki.bambulab.com/en/filament-acc/acc/print-finish-adv)
- Same-material support bonds more strongly: Bambu's H2D page says PETG support on a PETG model is harder to remove and may mark the surface; it has no PLA-on-PLA example. -- [PLA and PETG mutual support wiki](https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support)

### What Default becomes, and what Top Z turns into (code reading)
- Style Default with a tree type resolves to **Tree Organic** when the object has no variable layer height and Top Z > 0; otherwise Tree Hybrid. Both H2C presets therefore give Tree Organic unless a height-range modifier or adaptive layers are used. -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp) L136-156
- Tree Organic runs its own generator. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L1983-1990
- Normal support with independent layers on puts the contact layer at bottom_z minus the gap; with them off it uses the nearest object layer, and Slicing.cpp rounds the gap to whole layers. -- [SM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportMaterial.cpp) L1686-1769; [SL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Slicing.cpp) L116-124; [PrintObject.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObject.cpp) L3716-3722
- Tree Organic converts Top Z to `round(Top Z / layer height)` whole object layers, whatever independent layer height says. -- [TSC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupportCommon.hpp) L48, L64, L280; [TS3](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport3D.cpp) L1136, L1189-1196
- Tree Hybrid / Slim / Strong: Top Z is floored at the minimum layer height. With independent layers on, the gap is the typed Top Z where one support layer can be exactly that thick under the contact (flat ceilings). With them off, object layers are stacked until they reach the gap (rounds up). -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L631-636, L3964-4086, L4198-4205
- On sloped or arched undersides, contacts sit on consecutive layers. Each contact adds support-layer bounds at its bottom_z and bottom_z minus Top Z, and a bound closer than the minimum layer height (0.08 mm) to its neighbour is dropped. When Top Z is not a multiple of the layer height, support layers snap to the object's grid and the gap becomes the smallest whole number of layers that exceeds Top Z. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L3987-4088
- `round_up_divide(...) + 1` near L4142 is not the gap; it only feeds a thin-object early exit. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L4132-4155

**What a typed Top Z of 0.2 mm becomes (code reading).** One filament, prime tower off, independent layer height on, unless the row says otherwise.

| Case | Path | 0.16 mm layers | 0.20 mm layers |
|---|---|---|---|
| (a) tree(auto) + Default = Tree Organic | round(Top Z / layer h) object layers, always | 1 layer = 0.16 mm | 1 layer = 0.20 mm |
| (b) Tree Hybrid, independent layers on | typed Top Z (flat ceilings) | 0.20 mm | 0.20 mm |
| (b') Tree Hybrid, independent layers off (prime tower on) | object layers until >= 0.2 | 2 layers = 0.32 mm | 0.20 mm |
| (c) normal, independent layers on | bottom_z - gap | 0.20 mm | 0.20 mm |
| (c') normal, independent layers off | rounded, then nearest object layer | 0.16 mm | 0.20 mm |

- The 0.16 High Quality preset already sets Top Z 0.16, so all five cases give 0.16 mm there. The snap only bites when 0.2 is typed into a 0.16 mm-layer process with Organic (or normal with independent layers off). -- [fdm_process_dual_0.16_nozzle_0.4.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_0.16_nozzle_0.4.json)

## In practice
- Design the overhang out first (45 deg roofs, chamfers, keels); same-filament support is the last resort. Treat any Top Z number as unverified until a support-removal coupon has been printed and scored on your printer. The wiki's "about 0.2" is a starting point.
- The number typed is not always the gap printed: with the presets' Default style (Tree Organic), 0.2 at 0.16 mm layers prints as one 0.16 mm layer.
- A Top Z test coupon should use Support > Style = Tree Hybrid, independent support layer height on, and the prime tower off (one filament, no Smooth timelapse, no wrapping detection). Otherwise Organic rounding or the forced independent-off path collapses different Top Z values onto the same layer count. Use flat ceilings so the gap can be exact.
- G-code read-back for any Top Z: in the plate G-code, find the Z of the last support-interface layer and the Z of the first object layer above it; the difference is the real gap. On sloped undersides, sample many points, since the gap varies.
- Remove small overhangs (default on) can leave a thin, shallow shelf with no support at all even when support is enabled. If a small lip needs support, give it a 45 deg underside, add an enforcer, or turn that option off and check the slice.
- Wrapping detection or Smooth timelapse turn the prime tower on and force independent layer height off: check both before reading any Top Z as exact.
- Enforcer, critical-region and tip rules: [support-enforcers-and-critical-regions.md](support-enforcers-and-critical-regions.md).

## Not verified / open questions
- The gap values in the table are derived from code; case (b) is the one most worth confirming first on a flat-ceiling coupon, and cases (a), (b'), (c), (c') each need a slice with the read-back above.
- No official numeric guidance exists for removal ease or surface scarring versus Top Z, interface layers or spacing for same-filament PLA; only a printed coupon can answer it.
- Why a 0.24 mm Top Z on a 0.12 mm layer grid can print a larger gap than 0.24 on sloped undersides: not traced.
- The wiki contradicts itself on the default style; the code decides (Tree Organic).

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- keys, tooltips, defaults, prime-tower rules
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Slicing.cpp -- soluble interface, gap rounding
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportMaterial.cpp -- normal support contact Z
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp -- Hybrid gap, layer planning, critical regions
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupportCommon.hpp -- Organic rounding
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport3D.cpp -- Organic tips
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp -- style resolution, XY gap
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObject.cpp -- normal support dispatch
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintApply.cpp -- timelapse type read at slice time
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Preset.cpp -- timelapse type is a process option
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- Others > Special mode > Timelapse
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/SelectMachine.cpp -- send dialog timelapse on/off
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_0.16_nozzle_0.4.json
- https://github.com/bambulab/BambuStudio/tree/v02.08.02.61/resources/profiles/BBL/process
- https://wiki.bambulab.com/en/software/bambu-studio/support
- https://wiki.bambulab.com/en/filament-acc/filament/h2d-pla-and-petg-mutual-support
- https://wiki.bambulab.com/en/filament-acc/acc/print-finish-adv
