# Fusion 360 parametric workflow and export

Applies to: any printer · Autodesk Fusion (rolling online help; no build number on any page, so re-check after a UI-changing update)
Verified: 2026-10-04

## Facts

### Parameters
- Menu path: Design workspace > Solid > Modify > Change Parameters (also reachable as Design > Modify > Change Parameters). - [Autodesk help: SLD-MODIFY-PARAMETERS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-PARAMETERS)
- User Parameters are created directly in the Parameters dialog and referenced elsewhere; Model Parameters are created automatically when you add timeline features or sketch dimensions. - [Autodesk help: SLD-MODIFY-PARAMETERS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-PARAMETERS)
- Add User Parameter fields: Name (unique), Expression (calculates the Value), Value (read-only, computed), optional Comment and a Unit type picker. Typing for example `Width=50` or `Length=Width*2` directly into a dimension also creates a named model parameter and adds it to Favorites. - [Autodesk help: SLD-MODIFY-CHANGE-PARAMETERS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-CHANGE-PARAMETERS)
- Editing a parameter updates every reference to it. Automatic Compute is on by default and updates the design live; uncheck it to pause updates while batch-editing. - [Autodesk help: SLD-MODIFY-PARAMETERS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-PARAMETERS)
- User Parameters can be exported to CSV, edited in a table editor and imported back. - [Autodesk help: SLD-MODIFY-PARAMETERS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-PARAMETERS)
- Expression syntax: `;` is the multi-argument delimiter (so decimal-comma locales do not break), for example `if(Height < 500mm; 2; 3)`; built-in constants exist (for example `Gravity` = 980.665 cm/s^2); parameter names may contain `_`, `"`, `$`, `°` and `µ`. - [Autodesk help: GUID-76272551](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-76272551-3275-46C4-AE4D-10D58B408C20)
- Every parameter has a unit type (length, angle and so on); No unit makes it unitless, and there is also a Text unit type. - [Autodesk help: DSN-REF-PARAMETERS-UNITS](https://help.autodesk.com/view/fusion360/ENU/?guid=DSN-REF-PARAMETERS-UNITS)

### Sketch constraints and dimensions
- The Sketch > Constraints panel has 12 tools: Horizontal/Vertical, Coincident, Tangent, Equal, Parallel, Perpendicular, Fix/UnFix, Midpoint, Concentric, Collinear, Symmetry and Curvature (Curvature forces G2 continuity between a spline and another curve). - [Autodesk help: SKT-CONSTRAINTS](https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-CONSTRAINTS)
- Sketch Dimension (Design > Sketch > Create > Sketch Dimension): the geometry you pick decides the type (linear, angular, diameter or radius), and the value field accepts expressions mixing numbers and parameters. - [Autodesk help: SKT-CREATE-DIMENSIONS](https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-CREATE-DIMENSIONS)
- Driving dimensions display black, write their value into the Parameters dialog and block over-constraining. Driven dimensions show a read-only value in parentheses. - [Autodesk help: SKT-SKETCH-CREATE-DIMENSIONS](https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-SKETCH-CREATE-DIMENSIONS)
- Caution: if a driven dimension's expression references only driving dimensions, toggling it to driven turns it into a static value that cannot be recovered by toggling back. - [Autodesk help: SKT-CREATE-DIMENSIONS](https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-CREATE-DIMENSIONS)

### Modeling modes, timeline, components
- Parametric Modeling Mode records features in the timeline; Direct Modeling Mode does not. Switching Parametric to Direct removes the timeline and its features, and Direct geometry cannot be turned back into parametric features. - [Autodesk help: ASM-DESIGN-MODELING-MODES](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-DESIGN-MODELING-MODES)
- Suppressing a timeline feature disables it (and its dependants) without deleting it. A feature cannot be reordered before a feature it depends on. A Base Feature (Solid > Create > Create Base Feature) is a timeline feature in which you edit geometry directly. - [Autodesk help: ASM-DESIGN-MODELING-MODES](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-DESIGN-MODELING-MODES)
- Imported formats that can still be captured in parametric history: STEP, STL, SLDPRT, IPT, X_T, IGES, SLDASM, CADPART, IAM. On a Personal Use seat SLDPRT/SLDASM and X_T are commercial-only formats (see [fusion-360-personal-use-licence.md](fusion-360-personal-use-licence.md)). - [Autodesk help: ASM-DESIGN-MODELING-MODES](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-DESIGN-MODELING-MODES)
- A Component holds sketches, construction geometry, bodies, joints, origins and other components, each with its own name, number and description for a parts list. Recommended order: create the component, activate it, then build geometry inside it. - [Autodesk help: ASM-COMPONENTS](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-COMPONENTS)
- A Body is one contiguous shape. A component can hold several bodies, but joints and motion between bodies of the same component are not possible; that needs separate components. Bodies never appear in drawings or a BOM; components do. - [Autodesk help: GUID-C1AB4941](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-C1AB4941-D7AD-4D27-A035-2FA9208635B6)
- Bodies of different types (solid, surface, mesh, sheet metal, T-spline) cannot interact until converted to one type; mesh bodies are mostly used as reference geometry. - [Autodesk help: GUID-C1AB4941](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-C1AB4941-D7AD-4D27-A035-2FA9208635B6)
- "Create Components from Bodies" leaves the original feature history in the Default Component, not in the new components; this workflow is for hybrid designs. - [Autodesk help: GUID-C1AB4941](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-C1AB4941-D7AD-4D27-A035-2FA9208635B6)

### File > Export (licence limits per format are in the licence note)
- File > Export lists: Fusion Design/Archive (f3d/f3z), 3MF, Inventor (ipt/iam), AutoCAD DWG, DXF, FBX, IGES, LMV (svf), OBJ, SAT, SketchUp (skp), SMT, SPD, STEP, STL and USD (usdz). An exported file loses associativity with the source design. This page does not filter by licence. - [Autodesk help: ASM-EXPORT-DESIGN](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-EXPORT-DESIGN)
- STEP export includes bodies, components, the browser tree, raw appearance colours and component-level material. It excludes sketches, construction geometry, canvases, decals, analysis results and full materials/appearances. (Page dated 2024; re-check.) - [Autodesk KB: What data exports on STEP export](https://www.autodesk.com/support/technical/article/What-data-exports-on-Step-Export-from-Fusion-360)
- A Configured Design only offers Fusion Archive (.f3z) by default. Workaround: switch the export dialog from "Configured Design" to "Active configuration", or right-click a body or component in the browser and export it directly. - [Autodesk KB: export STEP from a configured design](https://www.autodesk.com/support/technical/article/Unable-to-export-to-Step-file-from-a-configured-design-in-Fusion)

### 3D printing and mesh tools
- 3D Print tool: Design workspace > Utilities > Make > 3D Print. Preparation types: Manufacturing (Manufacture workspace, Additive tab), Export (writes 3MF, STL or OBJ) and Print Utility (sends to an installed printing app, or Custom). - [Autodesk help: SLD-3D-PRINT](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-3D-PRINT)
- 3MF carries vertices, faces, units, colours and textures; STL (binary or ASCII) and OBJ are unitless, so the dialog asks for a Unit Type for those two. - [Autodesk help: SLD-3D-PRINT](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-3D-PRINT)
- The 3D Print tool's Refinement Settings offer four presets, each defined as a maximum surface deviation; the page gives no numeric values. - [Autodesk help: SLD-3D-PRINT](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-3D-PRINT)
- Save As Mesh (right-click a body or component in the browser): 3MF, STL binary, STL ASCII or OBJ; units cm/mm/m/in/ft; One File or One Body Per File. It has no refinement option. - [Autodesk help: MESH-SAVE-AS-MESH](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-SAVE-AS-MESH), [Autodesk help: MESH-EXPORT-TOOLS](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-EXPORT-TOOLS)
- Tessellate (Create > Tessellate) sets mesh density: High/Medium/Low presets, or Custom with Surface Deviation, Normal Deviation, Maximum Edge Length, Aspect Ratio and Triangle Count. Create Quads produces a quad mesh that converts to a T-spline body. - [Autodesk help: MESH-TESSELLATE](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-TESSELLATE)
- Insert Mesh (Mesh tab > Create > Insert Mesh) imports STL, OBJ or 3MF with unit choice and Flip Up Direction, Center and Move To Ground options; it creates a Mesh Base Feature in the timeline. - [Autodesk help: MESH-INSERT-MESH](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-INSERT-MESH)
- Convert Mesh (Modify > Convert Mesh) has a parametric mode, a Faceted mode (one solid face per mesh face) and a Prismatic mode that merges coplanar groups into single faces. A watertight mesh becomes a solid body; an open mesh becomes a surface body. - [Autodesk help: MESH-CONVERT-TO-SOLID](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID)
- Prismatic mesh conversion needs a commercial subscription; a Personal Use seat does not have it. - [Autodesk KB: prismatic option missing](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/The-prismatic-option-is-missing-in-the-convert-mesh-menu-in-Fusion-360.html)
- Convert Mesh works best under about 10,000 facets; reduce the facet count first if conversion fails (guidance, not a hard limit). - [Autodesk KB: Convert a mesh to a BRep](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-Convert-a-Mesh-to-a-BRep-in-Fusion-360.html)
- Converting a mesh to an organic solid body is part of the Fusion Design Extension, an add-on separate from the base licence. - [Autodesk help: MESH-CONVERT-TO-SOLID](https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID)

### Canvas (reference images)
- Insert > Canvas places a PNG, JPG, JPEG, TIF or TIFF image on a face, with Display Through, Selectable, Renderable, Scale XY and flip options. - [Autodesk help: SLD-INSERT-CANVAS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-INSERT-CANVAS)
- Calibrate: Browser > Canvases > right-click the image > Calibrate, pick two points and enter their real distance. - [Autodesk help: SLD-SCALE-CANVAS](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-SCALE-CANVAS)

### Joints
- Joint positions components relative to each other and then defines motion (it usually moves the first-selected component onto the second). As-Built Joint defines motion between components that are already in place, without moving them. - [Autodesk help: ASM-JOINT-COMMAND](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-JOINT-COMMAND), [Autodesk help: ASM-AS-BUILT-JOINT](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-AS-BUILT-JOINT)
- As-Built Joint: Design > Solid > Assemble > As-Built Joint; modes Simple, Between Two Faces, Two Edge Intersection; limits Minimum, Maximum, Rest; Preview Motion and Animate Joint. - [Autodesk help: ASM-CREATE-AS-BUILT-JOINT](https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-CREATE-AS-BUILT-JOINT)
- There are 7 joint types: Rigid (0 DOF), Revolute (1 rotation), Slider (1 translation), Cylindrical and Pin-Slot (1 translation + 1 rotation), Planar and Ball. Each joint creates an editable parameter. - [Autodesk help: GUID-8818AE31](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-8818AE31-958A-4A59-989B-9875A174C67A)
- The same page's DOF lines for Planar and Ball both read "1 translation and 1 rotation", which contradicts its own prose (Planar: two translations and one rotation; Ball: three rotations, no translation). Treat those two DOF lines as a page error. - [Autodesk help: GUID-8818AE31](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-8818AE31-958A-4A59-989B-9875A174C67A)

## In practice
- Name and unit-type every parameter that drives a design; typing `Name=value` in a dimension is the fastest way to create one.
- Treat Direct Modeling Mode as a one-way door for the timeline: duplicate the design first if you are unsure.
- Create and activate a component before sketching inside it.
- For FDM, use Save As Mesh or the 3D Print tool's Export type; use Tessellate's Custom refinement if curved surfaces look faceted.
- Do not plan a workflow around Prismatic or organic mesh conversion without confirming the seat has them.
- STEP drops sketches, canvases, analysis and full appearances, so keep the native .f3d alongside it.

## Not verified / open questions
- STEP schema (AP214 vs AP242) is contradicted, not resolved. Autodesk's KB says Fusion exports AP214, but its own example `FILE_SCHEMA` line names the managed-model-based 3D engineering schema, which STEP Tools lists under AP242 (AP214's schema name is `AUTOMOTIVE_DESIGN`). Settle it by exporting one STEP and reading its `FILE_SCHEMA` line. - [Autodesk KB: STEP version](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-STEP-file-format-version-does-Autodesk-Fusion-export.html), [STEP Tools: AP242 e3](https://www.steptools.com/docs/stp_aim/notes_ap242e3.html), [STEP Tools: AP214](https://steptools.com/docs/stp_aim/notes_ap214.html)
- Whether a Personal Use seat can buy or use the Fusion Design Extension is not stated.
- Per-format Personal Use export rights are tracked in [fusion-360-personal-use-licence.md](fusion-360-personal-use-licence.md) and are still open.
- Autodesk help pages are undated rolling documents; the UI paths above were read from the pages, not checked on screen.

Sources:
- https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-PARAMETERS - parameters menu, user vs model, Automatic Compute, CSV
- https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-MODIFY-CHANGE-PARAMETERS - Add User Parameter fields, inline naming
- https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-76272551-3275-46C4-AE4D-10D58B408C20 - expression syntax
- https://help.autodesk.com/view/fusion360/ENU/?guid=DSN-REF-PARAMETERS-UNITS - parameter unit types
- https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-CONSTRAINTS - sketch constraints
- https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-CREATE-DIMENSIONS - Sketch Dimension, driven caution
- https://help.autodesk.com/view/fusion360/ENU/?guid=SKT-SKETCH-CREATE-DIMENSIONS - driving vs driven
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-DESIGN-MODELING-MODES - parametric vs direct, importable formats
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-EXPORT-DESIGN - File > Export formats
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-COMPONENTS - components
- https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-C1AB4941-D7AD-4D27-A035-2FA9208635B6 - bodies vs components
- https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-3D-PRINT - 3D Print tool
- https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-SAVE-AS-MESH - Save As Mesh
- https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-EXPORT-TOOLS - mesh export tool scope
- https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-TESSELLATE - Tessellate
- https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-INSERT-MESH - Insert Mesh
- https://help.autodesk.com/view/fusion360/ENU/?guid=MESH-CONVERT-TO-SOLID - Convert Mesh, Design Extension
- https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/The-prismatic-option-is-missing-in-the-convert-mesh-menu-in-Fusion-360.html - Prismatic needs commercial licence
- https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-Convert-a-Mesh-to-a-BRep-in-Fusion-360.html - 10,000-facet guidance
- https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-INSERT-CANVAS - Insert Canvas
- https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-SCALE-CANVAS - Calibrate Canvas
- https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/What-STEP-file-format-version-does-Autodesk-Fusion-export.html - STEP schema claim
- https://www.autodesk.com/support/technical/article/What-data-exports-on-Step-Export-from-Fusion-360 - STEP content
- https://www.autodesk.com/support/technical/article/Unable-to-export-to-Step-file-from-a-configured-design-in-Fusion - configured-design workaround
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-JOINT-COMMAND - Joint
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-AS-BUILT-JOINT - As-Built Joint
- https://help.autodesk.com/view/fusion360/ENU/?guid=ASM-CREATE-AS-BUILT-JOINT - As-Built Joint options
- https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-8818AE31-958A-4A59-989B-9875A174C67A - joint types and DOF page error
- https://www.steptools.com/docs/stp_aim/notes_ap242e3.html - AP242 schema name
- https://steptools.com/docs/stp_aim/notes_ap214.html - AP214 schema name
