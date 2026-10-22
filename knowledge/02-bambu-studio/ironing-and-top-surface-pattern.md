# Ironing and top surface pattern
Applies to: both (H2C and P1S) · Bambu Studio 02.08.02.61
Verified: 2026-10-05

Abbreviations: PC = [PrintConfig.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); FILL = [Fill.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp); WI = [ironing wiki](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing); WF = [fill-patterns wiki](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns).

## Facts
### Ironing settings (Quality > Ironing)
- Quality > Ironing > Ironing Type: No ironing / Top surfaces / Topmost surface / All solid layer (values `no ironing`, `top`, `topmost`, `solid`). Code default No ironing, and the H2C presets keep it. — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4069-4084, [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Top surfaces irons every top surface; Topmost surface irons only the object's last (highest) layer. In code, topmost ironing requires the layer to have no layer above it. — [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing); [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L973
- All solid layer is rarely used: the wiki says it may not give good results and adds a lot of time. Ironing needs top shell layers > 0, except All solid. — [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing); [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L969-973
- Wiki cautions: ironing only helps flat tops, not curved ones; large top areas add a lot of time; there is a heat-creep clog risk especially for low-softening materials such as PLA, PETG and TPU; a part not firmly stuck to the plate may come off; bad settings give over-extrusion or uneven smoothness. — [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Quality > Ironing > Ironing Pattern at this tag: Concentric and Rectilinear (values `concentric`, `zig-zag`), default Rectilinear; the H2C presets do not set it. — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4086-4095
- Version gap: the wiki lists three ironing patterns (Lines, Concentric, Archimedean Spiral). The third first appears at v02.08.03.65 (label "Archimedean Chords"); the wiki calls Rectilinear "Lines". — [PrintConfig.cpp v02.08.03.65](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.03.65/src/libslic3r/PrintConfig.cpp); [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Wiki on patterns: Lines suits most flat tops; Concentric suits round, elliptical, polygonal or rounded-corner tops. — [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing values in the H2C 0.4 mm presets (code defaults: flow 10 %, spacing 0.1 mm, speed 20 mm/s, inset 0 mm): — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process) (bundle 02.08.00.05); defaults [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4097-4136

| Preset | Ironing flow | Ironing line spacing | Ironing speed | Ironing inset |
|---|---|---|---|---|
| 0.20mm Standard @BBL H2C | 15 % | 0.15 mm | 30 mm/s | 0.21 mm |
| 0.16mm High Quality @BBL H2C | 25 % | 0.15 mm | 20 mm/s | 0.21 mm |
| 0.12mm High Quality @BBL H2C | 10 % | 0.15 mm | 30 mm/s | 0.21 mm |

- Ironing flow is a percentage of the object's layer-height flow: extruded volume per mm = layer_height x flow % x spacing, using the object's `layer_height`. Inset 0 means half the nozzle diameter. — [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L1078, L1083, L1086-1088
- Wiki tuning advice: too much flow over-extrudes, too little leaves the surface rough; spacing is usually smaller than the nozzle diameter; slower speed usually irons better. — [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing direction is Developer-mode only (default 45 degrees), so it does not show without Developer mode; the wiki says 45 degrees usually works better. — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L4138-4146; [WI](https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing)
- Ironing fan speed (filament Cooling page) defaults to -1 (disabled). — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1400-1409

### Top surface pattern and shells (Strength > Top/bottom shells)
- Strength > Top/bottom shells > Top surface pattern: Concentric, Rectilinear, Monotonic, Monotonic line, Aligned Rectilinear, Hilbert Curve, Archimedean Chords, Octagram Spiral. Code default Rectilinear; the H2C presets use Monotonic line (`monotonicline`). — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L2074-2095, [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- Wiki per pattern (paraphrased): Monotonic for large flat tops needing smoothness; Monotonic line avoids edge transitions on the outer contour, with possible visible seams but no excess material at joins; Hilbert Curve is commonly used for tops; Archimedean Chords for uniform appearance, simpler and faster than Hilbert; Octagram Spiral is decorative. — [WF](https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns)
- Silk PLA guide: select Archimedean Chords or Concentric as top surface pattern, and use 0.16 mm layers for curved or sloped surfaces. — [Silk guide](https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments)
- Top shell layers / thickness per preset: 0.20 Standard 5 / 1.0 mm; 0.16 HQ 6 / 1.0 mm (6 x 0.16 = 0.96 mm, so per the tooltip the slicer should raise it to 7 layers; derived, not sliced); 0.12 HQ 9 / 0.8 mm. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process); tooltip [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L5954-5973
- Top surface speed 200 mm/s (0.20 Standard) or 150 mm/s (0.16 HQ, 0.12 HQ); top surface acceleration 2000 mm/s2 in all three; top surface line width 0.42 mm, density 100 %. — [BBL process profiles](https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process)
- `only_one_wall_top` is obsolete; its replacement `top_one_wall_type` (Quality > Advanced > Only one wall on top surfaces: Not apply / Top surfaces / Topmost surface) defaults to Top surfaces. — [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp) L1524-1535, L7383-7400
- Sub-top surface pattern does not exist at v02.08.02.61; it is present from v02.08.03.65. — [PrintConfig.cpp v02.08.03.65](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.03.65/src/libslic3r/PrintConfig.cpp)
- Too high a flow rate shows as over-extrusion and uneven lines on top layers. — [flow-rate tuning](https://wiki.bambulab.com/en/x1/manual/manual-flow-rate-tuning)

### Per-object availability
- In the GUI, `ironing_type`, `ironing_flow`, `ironing_spacing`, `ironing_inset`, `ironing_speed`, `ironing_direction` and `top_surface_pattern` can be added per object. `ironing_pattern` is not in that list, so it cannot be set per object in the GUI, although a 3MF can carry it. — [GUI_Factories.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_Factories.cpp) L102, L107
- Per-object values apply at slice time: the object's config is applied over the region config, which the ironing code reads. — [PrintObject.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObject.cpp) L3105-3111; [FILL](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp) L967-990

## In practice
- A flat top that sits below a higher feature on the same object is NOT ironed by "Topmost surface"; use "Top surfaces" for that case. (Follows from the topmost-layer condition above; confirm in the sliced preview by looking for Ironing blocks at that height.)
- To compare finishes, slice a small test plate with several tiles, each with its own per-object Ironing Type and Top surface pattern, and check the G-code `; FEATURE: Ironing` blocks and `result.json` Ironing time before printing it on your own printer.
- Ironing costs real time and scales roughly with ironed area / (spacing x speed) (a derivation, not a stated fact); read the Ironing entry in `result.json` `feature_type_times`.
- For display pieces with a large flat visible top, decide Ironing Type and Top surface pattern on purpose and write down why.
- For Concentric ironing per object, the key has to be written into the 3MF directly.

## Not verified / open questions
- Which combination looks best on a real print: print a test plate on your own printer and judge.
- Whether travel moves mark finished flat tops.
- Why ironing can skip areas the slicer labels as top surface (candidate: `top_area_threshold`).
- Whether a per-object `ironing_pattern` written into a 3MF is honoured.

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp — ironing and top-surface enums, labels, defaults, tooltips
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Fill/Fill.cpp — topmost condition, flow/inset/spacing code
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/GUI_Factories.cpp — per-object settings lists
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObject.cpp — per-object config applied to regions
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.03.65/src/libslic3r/PrintConfig.cpp — third ironing pattern and sub-top pattern
- https://github.com/bambulab/BambuStudio/tree/master/resources/profiles/BBL/process — H2C preset values
- https://wiki.bambulab.com/en/software/bambu-studio/parameter/ironing — ironing meanings, cautions, tuning
- https://wiki.bambulab.com/en/software/bambu-studio/fill-patterns — top surface pattern wording
- https://wiki.bambulab.com/en/x1/manual/printing-with-silk-filaments — Silk PLA advice
- https://wiki.bambulab.com/en/x1/manual/manual-flow-rate-tuning — over-extrusion on top layers
