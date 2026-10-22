# Seam painting (paint-on seam gizmo) and Seam position = Back
Applies to: both (slicer feature, Windows GUI) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61)
Verified: 2026-10-05

Short names, all at tag v02.08.02.61: GS = [GLGizmoSeam.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp), SP = [SeamPlacer.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp), 3MF = [bbs_3mf.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp).

## Facts

### GUI labels and keys
- The Bambu wiki says that when the automatic seam position is not ideal you can paint it manually, enabled from a toolbar button. -- [Seam wiki](https://wiki.bambulab.com/en/software/bambu-studio/seam)
- The gizmo is named "Seam painting"; toolbar tooltip "Seam painting [P]". It needs exactly one object selected, otherwise the button asks you to select a single object. -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp)
- Shortcut is plain **P**; Ctrl+P is Preferences. Pressing P again while the gizmo is open closes it. -- [KBShortcutsDialog.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/KBShortcutsDialog.cpp); [GLGizmosManager.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmosManager.cpp)
- Mouse: Left mouse button = "Enforce seam"; Right mouse button = "Block seam"; Shift + Left mouse button = "Erase"; a button "Erase all painting". -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp)
- Brush shapes: only Circle (key C) and Sphere (key S); no smart fill in the seam gizmo. "Brush size" = Ctrl + Mouse wheel (panel default 1.00). -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp)
- "Section view" = Alt + Mouse wheel; once the cut plane moves, a "Reset direction" button appears. -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp)
- Checkbox "Vertical" keeps a brush drag on a vertical screen line and is cleared each time the gizmo opens or closes. Checkbox "View: keep horizontal" enables the slider "Rotate horizontally" (-180 to 180 deg) and clears when the camera leaves the front view. Both rows are missing from the older wiki screenshot, so that screenshot predates this version. -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp); [GLGizmoPainterBase.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoPainterBase.cpp)
- A "Painting below the build plate is not allowed." warning appears only when the selected object sinks below Z = 0; the code that actually blocks painting was not found. -- [GS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp)
- Setting path: Process > Quality > Seam > Seam position (Nearest, Aligned, Back, Random; code default and BBL profile value Aligned). It sets the start point of each outer wall. -- [PrintConfig.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp); [Tab.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp); [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json)
- The wiki describes Back as placing the seam behind the model, good when you want a smooth front (it uses a mask as the example). It does not define "behind" in axis terms. -- [Seam wiki](https://wiki.bambulab.com/en/software/bambu-studio/seam)

### Paint priority (code reading)
- Per layer, the seam comparator checks paint type first (Enforced > Neutral > Blocked), then overhang and hidden-point checks, then, for Back, the larger Y. So Back means the candidate with the largest Y, the rear of the plate (+Y). -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp); [SeamPlacer.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.hpp)
- A point counts as painted if an enforcer or blocker triangle lies within one outer-wall line width; the blocker check runs last, so a blocker wins when both apply. -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp)
- Seam alignment runs for both Aligned and Back. It prefers a central enforcer point and blends enforced points toward a fitted spline, so under Back the seam is not guaranteed to sit at the strip's highest-Y edge; it can be pulled toward the patch centre. Keep painted strips narrow. -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp)
- Seam candidates come from outer walls only (all walls only for Random). Inner loops copy the seam of the closest outer-wall seam point. -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp)

### Storage in the 3MF and the CLI
- Seam paint is saved per triangle as the `paint_seam` attribute in the mesh file (`3D/Objects/object_N.model`) and rebuilt on load onto every volume that uses that mesh. -- [3MF](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp)
- Encoding of an unsplit triangle: hex digit "4" = enforcer, "8" = blocker (state shifted left by 2, with NONE = 0, ENFORCER = 1, BLOCKER = 2). Derived from the triangle selector serializer and the model string writer; not independently re-checked. -- [TriangleSelector.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleSelector.cpp); [Model.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp); [Model.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.hpp)
- The command-line slicer loads the model through the same `Model::read_from_file` path, and the seam placer reads `seam_facets`, so painted seams should apply to CLI slices too. -- [BambuStudio.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/BambuStudio.cpp); [Model.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp)

## In practice
GUI steps (Bambu Studio 02.08.02.61, Windows):
1. Prepare tab: click the object so only it is selected.
2. Open Seam painting with the toolbar button or **P**.
3. Pick Circle (C) or Sphere (S); set Brush size with the slider or Ctrl + Mouse wheel.
4. Turn the camera so the target strip faces you; optionally tick "View: keep horizontal".
5. Tick "Vertical" (it clears every time the gizmo opens).
6. Left drag = Enforce seam, Right drag = Block seam, Shift + Left = Erase.
7. Process > Quality > Seam > Seam position = Back, then save the project 3MF.
- Paint a narrow strip so every candidate position inside it is acceptable.
- Seams on closed hole loops (eye sockets, small concave pockets) are unlikely to move toward a strip they cannot reach.
- Check the result on your own slice: open the output 3MF, confirm the `paint_seam` attribute survived, and compare outer-wall start positions in the G-code (or the Preview seam markers) before and after painting. The print-time change from painting should be negligible.

## Not verified / open questions
- Community, conflicts with the source: GitHub issue #8036 reports that painting only affects outer walls while inner walls follow the global seam mode. Code reading says inner loops copy the nearest outer-wall seam. Read your G-code before relying on inner-wall placement. -- [issue #8036](https://github.com/bambulab/BambuStudio/issues/8036)
- A claim that Studio refuses a 3MF with a newer seam-paint version is contradicted: the version check is inside a commented-out block at this tag. -- [3MF](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp)
- Which code blocks painting below the build plate, and how the toolbar button closes the gizmo: not traced.
- The "4" / "8" encoding was read from source but not independently re-derived.

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/seam -- manual seam painting, Back definition
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoSeam.cpp -- labels, mouse actions, brush, checkboxes
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmosManager.cpp -- shortcut, toggle
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoPainterBase.cpp -- Vertical drag
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/KBShortcutsDialog.cpp -- P shortcut
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/PrintConfig.cpp -- Seam position options
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Tab.cpp -- Quality > Seam placement
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/resources/profiles/BBL/process/fdm_process_common.json -- seam_position aligned
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.cpp -- priority, Back = largest Y, alignment
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/GCode/SeamPlacer.hpp -- Enforced > Neutral > Blocked
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp -- paint_seam save/load
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/TriangleSelector.cpp -- paint state serialization
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.cpp -- read_from_file, triangle string
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Model.hpp -- EnforcerBlockerType
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/BambuStudio.cpp -- CLI load path
- https://github.com/bambulab/BambuStudio/issues/8036 -- community claim on inner walls
