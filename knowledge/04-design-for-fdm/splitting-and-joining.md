# Splitting and joining FDM parts (cut tool, split tools, adhesives)

Applies to: H2C | P1S | both · Bambu Studio 2.8.02.61 / master
Verified: 2026-10-05 (connector-tolerance lines; the rest verified 2026-10-03)

Design rule first: split only at natural part boundaries (separate pieces, accessories, bases). A plane cut through the middle of a sculpture or a visible face leaves a seam that shows. Use the tools below at boundaries the design already has.

## Facts
- Bambu Studio has a planar Cut tool for fitting large models on the plate. You can rotate the cut plane to any angle and move it freely; the wiki also lists easier post-processing and fewer supports as benefits. -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool)
- Open the Cut tool by selecting an object and clicking its toolbar icon, or by pressing `C`. -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool)
- The Cut tool has two modes: Planar (the default, a straight cut) and Dovetail (an interlocking cut that helps align and hold the halves). -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool); [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- Dovetail mode has four parameters: Depth, Width, Flap Angle (slider 30-120 degrees) and Groove Angle (slider 0-15 degrees). -- [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- A dovetail cut can leave non-manifold edges; Bambu Studio then pops up a prompt to fix the model, which you should accept before slicing. -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool)
- The Cut tool offers four connector types: Plug, Dowel, Snap and Thread. The wiki lists only the first three, but the v02.08.02.61 source renders a Thread radio button too. Choosing Thread greys out Style and forces Shape to Circle. -- [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp); [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool) (lists 3, out of date)
- Connector tolerance in 02.08.02.61: two Tolerance sliders (Size row and Depth row), range 0-2 mm, step 0.05, both defaulting to 0.1 mm. Only the hole is enlarged (its diameter by 2 x the Size tolerance); a Plug peg stays nominal. For a Dowel both halves get the wider hole, but the Depth tolerance goes into one half only. The `Model.hpp` constructor default of 0 is not what the panel uses. More in [keyed-joints-and-connectors.md](../07-engineering/keyed-joints-and-connectors.md). -- [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp); [CutUtils.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp)
- Connector enums in `Model.hpp` (master): Style is Prizm or Frustum; Shape is Triangle, Square, Hexagon or Circle; cut mode is planar or tongue-and-groove. Snap defaults: `snap_space_proportion = 0.3`, `snap_bulge_proportion = 0.15`. In the UI, Dowel forces Style to Prizm, and Snap or Thread forces Shape to Circle. -- [Model.hpp (master)](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/Model.hpp); [GLGizmoAdvancedCut.cpp (master)](https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- A cut produces separate objects by default, or one multi-part object with the "Cut to parts" toggle. Dovetail mode turns Cut to parts off, and "Add connectors" is disabled while Cut to parts is on. -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool); [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- After a cut you can switch off Object A or Object B to discard a half (both kept by default). "Keep orientation", "Place on cut" and "Flip" reposition each half, and the Rotate tool (`R`) is available for more adjustment. -- [Bambu wiki, cut tool](https://wiki.bambulab.com/en/software/bambu-studio/cut-tool); [GLGizmoAdvancedCut.cpp v02.08.02.61](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp)
- Separate from the Cut tool, the top toolbar has Split to Objects and Split to Parts, which separate shells that already exist in a model (they do not cut solid geometry). Split to Objects is for models too large to print as one piece: the shells print separately and are assembled afterwards. Split to Parts keeps the shells under one object so each can get its own filament. -- [Bambu wiki, split to objects/parts](https://wiki.bambulab.com/en/software/bambu-studio/split-to-objects-parts)
- Loctite Super Glue Plastics Bonder (US, two-part cyanoacrylate with activator): rated for hard-to-bond plastics such as polyethylene, polypropylene and TPU. Tensile shear strength (ISO 4587, 12-24 h cure) is 2-20 N/mm2 depending on substrate, up to 6 N/mm2 on hard-to-bond substrates. Fixture time 5-30 s, cure 12-24 h, service up to 80 C. Not for flexible or gap-filling repairs. PLA and PETG are not named substrates. -- [Henkel TDS](https://datasheets.tdx.henkel.com/LOCTITE-Plastics-Bonding-System-en_US.pdf)
- Loctite SUPERGLUE All Plastics (UK/EU, same two-part system): initial adhesion in 5-30 s; 2-20 N/mm2 tensile shear (ISO 4587) after 12-24 h depending on substrate; ethyl cyanoacrylate. The sheet says never to use it on assemblies that will hold hot liquids. PLA and PETG are not named substrates. -- [Henkel TDS](https://datasheets.tdx.henkel.com/LOCTITE-SUPERGLUE-All-Plastics-en_GB.pdf)
- 3M Scotch-Weld DP8005 (10:1 two-part acrylic for low-surface-energy plastics): work life 2.5-3 min and full cure 8-24 h at 23 C. Overlap shear on HDPE is 1100 psi (ASTM D1002, 23 C, 1 x 0.5 in overlap, IPA wipe, at least 48 h cure, 2 in/min pull); ABS under the same test is 1525/1575 psi. PLA and PETG are not listed substrates. -- [3M TDS](https://multimedia.3m.com/mws/media/1235571O/dp8005-scotch-weld-technical-data-sheet.pdf)
- Gorilla Epoxy: application temperature 50-100 F, service temperature -10 to 180 F. The Gorilla Super Glue SDS gives storage at 5-25 C. Neither document gives a bond strength on plastics. -- [Gorilla Epoxy product page](https://gorillatough.com/product/gorilla-epoxy); [Gorilla Super Glue SDS](https://gorillatough.com/wp-content/uploads/Gorilla-Super-Glue-SDS.pdf)
- Community: a Plug is molded into one half, while a Dowel prints as a separate peg and leaves holes in both halves. -- [Bambu forum, thread 35745](https://forum.bambulab.com/t/35745) (community, post 18)

## In practice
- Use the Cut tool (`C`) to cut solid geometry to fit the plate or to make a flat face; use Split to Objects/Parts when the model already arrives as separate shells and you only need to separate or colour them.
- Dovetail mode gives self-aligning halves without separate connector objects; accept the model-fix prompt before slicing.
- For a joint that carries load or must resist twisting, add explicit connectors (Plug, Dowel, Snap or Thread) rather than relying on a dovetail. Set the tolerance from a printed clearance test, not from the default.
- None of the adhesive datasheets above names PLA or PETG as a tested substrate. Treat each as unproven for PLA/PETG until you have glued and pulled a test coupon of your own.
- Always carry the test conditions with a shear figure (for DP8005: 23 C, ASTM D1002, at least 48 h cure); it is not a universal number.
- A pocket or imprint that must match a part's outline prints its sloped walls as layer steps, so it will not trace the outline exactly. Give it a clearance that allows for the layer height and the wall steps, and decide beforehand how you will check the fit (feeler gauge, drop-in without force, shim). Verify on your own printer.

## Not verified / open questions
- The Cut to parts toggle and the post-cut Object A/B controls were checked against the v02.08.02.61 source, not in the running GUI.
- A second community quote about which connector suits repeated assembly could not be found in any source; do not use it.

Sources:
- https://wiki.bambulab.com/en/software/bambu-studio/cut-tool -- cut modes, dovetail, connectors (wiki lists 3), cut to parts, post-cut panel
- https://wiki.bambulab.com/en/software/bambu-studio/split-to-objects-parts -- Split to Objects vs Split to Parts
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp -- four connector types, dovetail ranges, tolerance sliders, cut-to-parts logic
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/CutUtils.cpp -- which half gets the tolerance
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/libslic3r/Model.hpp -- connector enums, snap defaults
- https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/Gizmos/GLGizmoAdvancedCut.cpp -- Thread button and Style/Shape forcing
- https://datasheets.tdx.henkel.com/LOCTITE-Plastics-Bonding-System-en_US.pdf -- Loctite Plastics Bonder
- https://datasheets.tdx.henkel.com/LOCTITE-SUPERGLUE-All-Plastics-en_GB.pdf -- Loctite SUPERGLUE All Plastics
- https://multimedia.3m.com/mws/media/1235571O/dp8005-scotch-weld-technical-data-sheet.pdf -- 3M DP8005
- https://gorillatough.com/product/gorilla-epoxy -- Gorilla Epoxy temperatures
- https://gorillatough.com/wp-content/uploads/Gorilla-Super-Glue-SDS.pdf -- Gorilla Super Glue storage
- https://forum.bambulab.com/t/35745 -- community note on Plug vs Dowel
