# Keyed joints and Bambu Studio Cut-tool connectors

Applies to: any printer in Bambu Studio (code read at tag v02.08.02.61; profile values checked for the H2C 0.4 mm chain) - Bambu Studio 02.08.02.61
Verified: 2026-10-05

Short names, all at tag v02.08.02.61 of the official repository: GZ = [GLGizmoAdvancedCut.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp), CU = [CutUtils.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp), MC = [Model.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp), TM = [TriangleMesh.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleMesh.cpp), PC = [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp).

## Facts

### The panel (Cut tool > Add connectors)
- Row labels: Type, Style, Shape, Depth ratio, Size. Type order: Plug, Dowel, Snap, Thread. Style: "Prizm" (spelled that way) and "Frustum". Shape: Triangle, Square, Hexagon, Circle. - [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- Style is greyed for Dowel, Snap and Thread (Dowel forces Prizm). Shape is greyed and forced to Circle for Snap and Thread. Thread is new code and may change. - [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- So a keyed (non-round) joint means Type = Plug or Dowel with Shape = Square, Hexagon or Triangle. Snap and Thread cannot be keyed. - derived from [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- The Cut-tool wiki lists only Plug, Dowel and Snap and has no tolerance text; it lags the code. - [Bambu wiki: Cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool)
- Defaults: Depth ratio 3 mm, Size 2.5 mm, both tolerances 0.1 (`CUT_TOLERANCE = 0.1f`). Size is a diameter, minimum 1 mm, maximum (X+Y+Z)/2 of the object's bounding box. - [GLGizmoAdvancedCut.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp), [CutUtils.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.hpp), [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- Tolerance sliders: 0 to 2 mm, drag step 0.05, tooltip "Tolerance". The Size-row tolerance maps to `radius_tolerance`, the Depth-row tolerance to `height_tolerance`. - [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp), [ImGuiWrapper.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ImGuiWrapper.hpp)
- Snap: Gap 10-50 % (default 30 %), Bulge from 5 % up to the Gap value (default 15 %). Thread has no parameters of its own. - [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp), [GLGizmoAdvancedCut.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp)
- Edge case: the Size tolerance resets to 0 only after several connectors with different tolerances are selected and then all unselected; new connectors use 0.1. - [GZ](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)

### Which side gets the tolerance
- `apply_tolerance()` enlarges only the hole (a negative volume): radius widens by `radius_tolerance`, depth by `height_tolerance`. The peg stays nominal. - [CU](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp)
- Plug: the enlarged hole is in object `_A` (upper); the peg belongs to `_B` (lower). - [CU](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp)
- The hole diameter grows by 2 x the Size tolerance (Size 6 mm, t 0.1 mm gives a 6.2 mm hole; derived from code, not measured), the same "twice the value" convention as XY Hole Compensation. - [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp), [Bambu wiki: XY hole compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation)
- Depth: for Plug and Snap the hole is also shifted by t/2 - 0.05 mm, so the usable extra depth at the bottom is about t - 0.05 mm (0.05 mm at the default 0.1). Derived from code, assuming the rotation normal equals the plane normal; not measured. - [CU](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp), [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp)
- Dowel: the dowel is nominal; both halves get enlarged-radius holes, but all of the depth tolerance lands in one half and the other hole is exactly the nominal depth. Derived from code. - [CU](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp)
- A public issue reporting a dowel hole 0.1 mm shallower than expected was closed as not a bug; the Bambu reply said the tolerance sits in the other cut object. This matches the one-half depth tolerance. - [issue #11148](https://github.com/bambulab/BambuStudio/issues/11148)
- Dowels become separate objects named `<object>-Dowel-<connector>`, placed beside the halves. - [CU](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp)
- Shapes: Triangle/Square/Hexagon have 3/4/6 sides, Circle 360; vertices sit on the radius, so Size is the vertex-to-vertex diameter. - [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp), [TM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleMesh.cpp)
- Thread geometry: pitch about 0.2 x connector height; radial thread depth about 0.08 x connector radius. - [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp), [TM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleMesh.cpp)

### Rotation lock (Square and Hexagon keys)
- The hole is the same polygon scaled by (r + t)/r, so a polygon peg can spin free once t >= r x (1/cos(pi/n) - 1), n = number of sides. At Size 2.5 mm (r = 1.25 mm): Hexagon 0.193 mm, Square 0.518 mm, Triangle 1.250 mm. Geometry only (derived from [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp) and [TM](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleMesh.cpp)); nozzle corner rounding shrinks the real margin.
- Because Size is vertex-to-vertex, a 2.5 mm peg is 2.165 mm across flats as a hexagon and 1.768 mm as a square: the square locks better but is the thinner peg. Backlash starts well before free spin. - same derivation

### Compensation settings that interact
- `xy_hole_compensation` defaults to 0 (positive makes holes bigger) and is not overridden in the `0.20mm Standard @BBL H2C` chain; it acts on closed paths only. - [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp), [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- `0.20mm Standard @BBL H2C` inherits `fdm_process_dual_0.20_nozzle_0.4`, which sets `elefant_foot_compensation` 0.15. - [0.20mm Standard @BBL H2C.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json), [fdm_process_dual_0.20_nozzle_0.4.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json)
- Auto circle compensation covers only complete horizontal circles and a short list of Bambu filaments (PLA Basic, PLA CF, PET CF, PETG CF, PETG HF); it is off by default (`enable_circle_compensation` 0). - [Bambu wiki: auto circle compensation](https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation), [PC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp)
- User Customized Offset: follow the wiki (positive = looser). The English tooltip in Studio says the opposite; a Bambu contributor confirmed the tooltip is wrong (issue still open at 02.08.02.61). - [Bambu wiki: auto circle compensation](https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation), [issue #8873](https://github.com/bambulab/BambuStudio/issues/8873)
- The wiki recommends XY Hole and XY Contour Compensation when parts must fit screws, pins, magnets or other printed parts. - [Bambu wiki: XY hole compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation)

### File storage and slicing
- In the 3MF, plug holes are `negative_part` volumes in A and pegs are `normal_part` in B; `Metadata/cut_information.xml` stores type, radius, height and both tolerances. - [MC](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp), [bbs_3mf.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp)
- A slicer code comment says negative volumes are always subtracted. Code only; CLI behaviour not measured. - [PrintObjectSlice.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp)

### Outside references (labelled)
- Prusa (other printer): no universal clearance value; at least 0.3 mm as a first try for moving parts. - [Prusa Help](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
- Community forum thread: users report the 0.1 default, and some use 0.2 on both tolerances for square frustum plugs (advice, not verified). - [Bambu forum thread 35745](https://forum.bambulab.com/t/35745)

## In practice
- Sourced: a keyed joint is Plug or Dowel with Square, Hexagon or Triangle; the Plug peg is nominal in `_B` and the enlarged hole is in `_A`; the default 0.1 tolerance adds about 0.2 mm to the hole diameter.
- Engineering judgement (not verified, measure with a printed clearance-ladder coupon):
  - Square locks rotation with the most tolerance margin but is the weaker peg; Hexagon is stronger but spins free at a small tolerance.
  - If a Plug peg bottoms out, raise the Depth tolerance: at the default the usable extra depth is only about 0.05 mm.
  - With a Dowel, expect the end play on one side only.
  - Check whether elephant-foot compensation (0.15 mm in the H2C chain) changes the first layers of a hole near the plate.
  - Slice a cut 3MF and read the hole in the G-code before printing a large part.
- No source gives a minimum key size.

## Not verified / open questions
- No coupon results are part of this note; a hand-insertable, rotation-locking tolerance for your printer and filament must be measured.
- What the "Middle of geometry" checkbox does was not traced.
- Whether a 360-sided Circle connector hole counts as a circle for Auto circle compensation.
- How negative parts in a cut 3MF behave in a CLI slice; how Thread connectors actually print.
- On-screen layout of the two tolerance sliders (labels checked in code only).

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp - panel labels, type/style/shape rules, slider ranges
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.hpp - default sizes, tolerances, snap proportions
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/ImGuiWrapper.hpp - slider tooltip
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp - apply_tolerance, plug/dowel handling, naming
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.hpp - CUT_TOLERANCE 0.1
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp - connector meshes, scaling, volume types
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleMesh.cpp - polygon vertices on radius, thread depth
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp - cut_information.xml
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintObjectSlice.cpp - negative volumes subtracted
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp - compensation keys and tooltips
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json - compensation defaults
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20H2C.json - H2C process chain
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_dual_0.20_nozzle_0.4.json - elefant_foot_compensation 0.15
- https://wiki.bambulab.com/en/software/bambu-studio/cut-tool - wiki connector list
- https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation - twice-the-value rule, closed paths
- https://wiki.bambulab.com/en/software/bambu-studio/manual/auto-circle-contour-compensation - circle-only, positive = looser
- https://github.com/bambulab/BambuStudio/issues/8873 - tooltip sign error
- https://github.com/bambulab/BambuStudio/issues/11148 - dowel depth tolerance in the other object
- https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135 - Prusa clearance (other printer)
- https://forum.bambulab.com/t/35745 - community connector advice
