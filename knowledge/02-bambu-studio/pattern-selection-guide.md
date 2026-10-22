# Pattern selection guide (Top / Bottom / Internal solid / Sparse)
Applies to: H2C | P1S · Bambu Studio 02.08.02.61
Verified: 2026-10-06

Abbreviations: PC = [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); FILL = [Fill.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp); FPC = [fdm_process_common.json v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json); FP = [Fill patterns wiki](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns); SAS = [Strength advanced settings wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings); TP = [Transparent PETG wiki](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg).

Version warning: the FP and SAS wiki pages (as read for this note) document a Sub-top surface pattern that does not exist at 02.08.02.61. Their per-pattern descriptions still apply.

## Facts
### The four settings (Process preset, Strength tab)
- Strength > Top/bottom shells > Top surface pattern has 8 options: Concentric, Rectilinear, Monotonic, Monotonic line, Aligned Rectilinear, Hilbert Curve, Archimedean Chords, Octagram Spiral. Code default Rectilinear. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2074-2095
- Strength > Top/bottom shells > Bottom surface pattern has the same 8 options (it does not control bridge infill); code default Rectilinear. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2119-2126
- Strength > Infill > Internal solid infill pattern has the same 8 options; code default Rectilinear. Its tooltip says small areas switch to Concentric when narrow internal solid infill detection is on. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2141-2148
- Strength > Infill > Sparse infill pattern has 22 options, code default Cubic; code default density 20 %. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3085-3151
- Enum trap: the stored value `"zig-zag"` is **Rectilinear** (`ipRectilinear`), while `"zigzag"` is **Zig Zag** (`ipZigZag`). Other stored values: `monotonic`, `monotonicline`, `alignedrectilinear`, `3dhoneycomb`, `hilbertcurve`, `archimedeanchords`, `octagramspiral`. Hand-editing a 3MF with the wrong one silently gives the wrong pattern. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L221-240
- At 100 % sparse density the code rejects any sparse pattern that is not also a top-surface value; Monotonic and Monotonic line are not sparse options at all. What passes is Concentric, Rectilinear, Aligned Rectilinear, Hilbert Curve, Archimedean Chords, Octagram Spiral, which matches the wiki's list of patterns that support 100 % density. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L3107-3128, L9508-9531; [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Detect narrow internal solid infill: code default on; narrow areas then use Concentric. Not set in the H2C chain. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L6533-6540
- Top surface density: code and preset 100 %. Lower values give a textured top; at 0 % only the walls print on the top layer. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)

### Preset values in the H2C 0.4 mm process chain
All three H2C 0.4 mm presets inherit `fdm_process_dual_0.xx_nozzle_0.4` -> `fdm_process_dual_common` -> `fdm_process_common`; no intermediate file sets a `*pattern` key.
- Top surface pattern = **Monotonic line** (`top_surface_pattern: monotonicline`, FPC L167). -- [FPC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- Bottom surface pattern = **Monotonic** (FPC L10). -- [FPC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- Internal solid infill pattern = **Rectilinear** by code default (no chain file sets it). It is used for every internal solid layer, including the layer directly under a top surface. -- [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2148; [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L234-235
- Sparse infill: **Grid, 15 %** on 0.20mm Standard @BBL H2C (FPC L111, L119; infill direction 45 deg at L39); **Gyroid, 15 %** on 0.16mm High Quality @BBL H2C (L77) and 0.12mm High Quality @BBL H2C (L89). -- [FPC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json); [0.16 HQ H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.16mm%20High%20Quality%20%40BBL%20H2C.json); [0.12 HQ H2C](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.12mm%20High%20Quality%20%40BBL%20H2C.json)
- Monotonic line travel extend `monotonic_travel_into_wall` is **45 %** in the H2C presets (set in `fdm_process_dual_common.json` L255, overriding 0 in FPC; code default 0 %). It is a Develop-mode option, only acts with Monotonic line, and Fill.cpp applies it whenever the top pattern is Monotonic line, so it is active on every H2C top surface at the preset pattern. -- [fdm_process_dual_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_common.json); [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L241; [SAS](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings)
- Infill direction rotates all infill types (top, bottom, sparse, internal solid) except external bridges; preset 45 deg. -- [SAS](https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings)

### What the wiki says about each pattern (paraphrased)
- Monotonic: uniform lines, smoother than plain rectilinear; suited to large flat tops. Monotonic line: no edge transition on the outer contour, so no extra material at the joins, though some seams may show. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Comparison table: Rectilinear and Aligned Rectilinear have edge transitions and can print in both directions; Monotonic has edge transitions and prints in one direction only; Monotonic line has no edge transition and prints in one direction only. Interlayer direction is perpendicular for all except Aligned Rectilinear (parallel). -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Rectilinear on top gives no visible effect because it is perpendicular to the layer below. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Concentric follows the model's contours and processes quickly; as sparse infill it is weak against horizontal loads. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Hilbert Curve is often used as a top pattern; as a bottom it is affected by the plate. The wiki sentence about Hilbert on a textured plate is garbled, so "a textured plate weakens a Hilbert bottom" is an interpretation, not a statement. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Archimedean Chords: for uniform appearance and finish on top; as a bottom it is affected by the plate and its curved path is prone to leakage. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Octagram Spiral: decorative on top; limited strength as a bottom and as sparse infill. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Transparent materials: if top/bottom is Aligned Rectilinear, the wiki recommends Aligned Rectilinear sparse too for appearance, at the cost of anisotropic strength. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Sparse patterns (qualitative, no density or test condition given): Grid is simple and fast but its crossings can build up material; Gyroid supports well in all directions with no same-layer crossings; Cubic is stable across X, Y and Z; Tri-hexagon is among the strongest under tension; Honeycomb uses about 25 % more material; Lightning suits decorative parts and its density only applies under the top surface; Rectilinear and Zig Zag suit low-load parts. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Locked Zag is meant for infill that forms the outer surface. -- [FP](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns); [Locked Zag wiki](https://wiki.bambulab.com/en/software/bambu-studio/manual/locked-zag)

### Transparent and Silk guides
- Transparent PETG guide (goal: see-through): top and bottom shells 0, rectilinear infill, 1 wall loop, 100 % sparse density, infill direction 0 or 90 deg, 0.1 mm layers, 0.5 mm line width, 20 mm/s on all speeds; a 0.8 mm nozzle is recommended although the examples use 0.4 mm values. -- [TP](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg)
- PETG is generally more transparent than PLA (amorphous vs semi-crystalline). Bambu's store page describes PLA Translucent as frosted and light-diffusing and PETG Translucent as more see-through; transparency varies with speed, nozzle temperature and infill density. -- [TP](https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg); [PLA Translucent store page](https://us.store.bambulab.com/products/pla-translucent)
- Silk guide (PLA Silk / Silk+, 0.2 and 0.4 mm nozzles): set Process > Strength > Top surface pattern to Archimedean Chords or Concentric for better top gloss and uniformity, with 0.16 mm layers; the guide notes the result depends on the sliced output. -- [Silk guide](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)

### Sub-top surface at this tag
- Sub-top surface pattern does not exist at v02.08.02.61 (no `sub_top` key, no sub-top surface type); it exists on the master branch (default Monotonic). At this tag the layer under the top prints with the Internal solid infill pattern (Rectilinear in the presets; Concentric in narrow areas); an internal bridge under the top prints Rectilinear unless the top pattern is Monotonic. -- [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L234-240; [Surface.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Surface.hpp); [master PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp)

## In practice
Guidance derived from the facts above; none of it is a measured print result. Print a small top-surface coupon on your own printer before committing a finish-critical part.

| Part type | Top surface | Bottom surface | Internal solid | Sparse | Why |
|---|---|---|---|---|---|
| Display figurine | Preset Monotonic line; consider Quality > Ironing > Ironing Type "Top surfaces"; Archimedean Chords or Concentric for Silk PLA | Preset Monotonic (on a textured plate avoid Hilbert / Archimedean bottoms) | Preset Rectilinear | Gyroid 15 % (as the HQ presets) or Lightning for purely decorative parts | Curved walls dominate and tops are small; Silk guide for gloss; Lightning for decorative parts (FP) |
| Flat display top | Monotonic line, Monotonic, or Concentric / Archimedean Chords for Silk gloss; add ironing if lines show | Preset Monotonic | Preset Rectilinear | Preset | FP Monotonic wording; Silk guide |
| Mechanical part | Rectilinear or Monotonic | Preset Monotonic | Preset Rectilinear | Grid (0.20 preset), Gyroid, Cubic or Tri-hexagon | FP qualitative strength notes |
| Translucent diffuser | Aligned Rectilinear, with Aligned Rectilinear sparse | Aligned Rectilinear | Preset Rectilinear | Aligned Rectilinear, or Rectilinear 100 % at 0/90 deg for see-through | FP transparency note; TP |

Rule of thumb: every print sheet should state and justify all four patterns (Top surface, Bottom surface, Internal solid infill, Sparse infill). Choose speed and pattern together; see [speed-quality-method.md](speed-quality-method.md).

## Not verified / open questions
- Which pattern gives the most even diffusion for a frosted glow diffuser: no Bambu source states it. Needs a lit coupon on your printer.
- The wiki's sparse-pattern strength claims carry no density or test condition; treat them as qualitative.
- The wiki's Hilbert-on-textured-plate sentence is garbled; the reading above is an interpretation.
- Sub-top surface pattern behaviour on newer builds is not covered here.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- enums, labels, defaults, 100 % density check
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp -- which pattern each surface type uses
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Surface.hpp -- no sub-top surface type at this tag
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/PrintConfig.cpp -- sub-top pattern on master only
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json -- top/bottom/sparse preset values
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_common.json -- Monotonic line travel extend 45 %
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.16mm%20High%20Quality%20%40BBL%20H2C.json -- Gyroid sparse
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.12mm%20High%20Quality%20%40BBL%20H2C.json -- Gyroid sparse
- https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/strength-advance-settings
- https://wiki.bambulab.com/en/software/bambu-studio/manual/locked-zag
- https://wiki.bambulab.com/en/knowledge-sharing/transparent-petg
- https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments
- https://us.store.bambulab.com/products/pla-translucent
