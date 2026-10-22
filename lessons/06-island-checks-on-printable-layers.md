# Lesson 06: run island and empty-layer checks on what the slicer actually prints

Area: design for FDM checks

| What happened | Root cause | Rule now |
|---|---|---|
| A geometric island probe reported 0 floating regions on a textured face, while Bambu Studio kept warning about floating regions. A separate probe found many sub-line-width slivers at the tips of the texture. Two design rounds had been judged on the first probe. | The probe compared raw mesh sections layer to layer. A thin slanted sliver overlaps itself on every layer, so it never looks floating, but the slicer drops anything narrower than one outer-wall line, and the first printed layer above it starts on air. | Island checks model what the slicer prints: open (erode then dilate) each section by half the outer-wall line width before comparing layers. A geometry PASS is not a print PASS until a real slice shows an empty `warning_message` in `result.json`. |
| A small test coupon cropped from a larger part passed a design re-check ("islands kept"). The slicer refused it with an empty-layer error: at some heights the whole cross-section was tip slivers narrower than one line, so nothing printed and everything above sat on an empty layer. The full part slices only because the rest of it keeps those layers non-empty. | The probe compared each layer with the raw layer below, so slivers counted as support, and it never asked whether every layer had printable area. A crop changes a part's layer census; the probe was written for whole parts. | 1. Per layer, in the print pose, report the minimum printable area and the minimum printable area connected to the layer below, measured on opened sections. Any layer with 0 printable area between the first and last layer is a FAIL; a connected width under three line widths is a WARN. 2. A crop or coupon cut from a larger part re-runs the full census as a new part; "it slices in the real part" is not evidence. 3. Reproduce the slicer's refusal in the probe first, so the fix has a positive control. |

How to check: run the probe on a known-bad crop (it must flag the empty layers the slicer refuses), then on the fixed part (it must report 0), then slice and read `result.json`.

Source: the empty-layer refusal in Bambu Studio's G-code generator, https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/GCode.cpp
