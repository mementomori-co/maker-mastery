# Retopology and UV workflow in Blender 5.2 LTS

Applies to: any printer (mesh preparation) - Blender 5.2 LTS manual (pinned `/manual/en/5.2/` pages)
Verified: 2026-10-03

## Facts

### Retopology overlay and tools
- The Retopology overlay (Overlays > Mesh Edit Mode > Shading > Retopology) is an Edit Mode overlay that makes the edited mesh see-through, with an Offset Distance that moves it towards the camera. - [Overlays](https://docs.blender.org/manual/en/5.2/editors/3dview/display/overlays.html)
- It lets you see the original mesh through the new one without the back-side clutter of X-Ray; the manual's workflow pairs it with Poly Build and Snapping. - [Retopology](https://docs.blender.org/manual/en/5.2/modeling/meshes/retopology.html)
- Poly Build (Edit Mode) combines add, delete, move and extrude in one tool and is aimed at retopology. Create Quads dissolves a shared edge so a new triangle becomes a quad. The manual recommends Snapping plus Auto Merge while tweaking vertices. - [Poly Build](https://docs.blender.org/manual/en/5.2/modeling/meshes/tools/poly_build.html)
- Snap Target Face snaps to the surface under the cursor and is called useful for retopology. For individual elements there are Face Project (along view depth, cannot reach hidden geometry) and Face Nearest (closest face, can reach hidden geometry). - [Snapping](https://docs.blender.org/manual/en/5.2/editors/3dview/controls/snapping.html)
- Quadriflow Remesh (Edit Mode, Mesh > Quadriflow Remesh) targets detail by Ratio, Edge Length or Faces, with Use Mesh Symmetry, Preserve Sharp, Preserve Mesh Boundary, Preserve Attributes, Smooth Normals and a Seed. The manual says it is not recommended for cleaning a mesh for sculpting or 3D printing (use the Voxel remesher) or for final animation topology. - [Retopology](https://docs.blender.org/manual/en/5.2/modeling/meshes/retopology.html)

### Shrinkwrap modifier
- Nearest Surface Point snaps each vertex to the closest point on the target surface. - [Shrinkwrap](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html)
- Project moves vertices along a chosen axis until they hit the target (vertices that never hit stay put), with Limit, Subdivision Levels, Negative/Positive, Face Cull, Invert Cull and an Auxiliary Target. - [Shrinkwrap](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html)
- Snap Mode Above Surface is like On Surface but offset along the target's smooth normal; Outside Surface, Inside and Outside also exist. - [Shrinkwrap](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html)
- Nearest Vertex snaps to the closest target vertex and has no Snap Mode. Target Normal Project is smoother than Nearest Surface Point but much slower. - [Shrinkwrap](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html)

### Decimate modifier
- Decimate reduces vertex and face count with minimal shape change and, unlike most modifiers, has no Edit Mode preview. - [Decimate](https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/decimate.html)
- Collapse Ratio is the fraction of faces kept (1.0 unchanged, 0.5 half, 0.0 none), counted in triangles, not quads. - [Decimate](https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/decimate.html)
- Un-Subdivide reverses subdivision (2 iterations is about 1 subdivide level, so use even numbers). Planar reduces detail on flat-ish areas with an Angle Limit and Delimit options (Normal, Material, Seam, Sharp, UVs, All Boundaries). - [Decimate](https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/decimate.html)

### UV unwrapping
- UV > Mark Seam / Clear Seam set seams in Edit Mode; UV > Seams from Islands adds seams at existing island borders. - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- Unwrap (U) methods: Angle Based (ABF, good general result), Conformal (LSCM, faster on simple objects, less accurate) and Minimum Stretch (SLIM, minimises area and angle distortion, with Iterations, No Flip and Importance Weights). - [UV unwrap](https://docs.blender.org/manual/en/5.2/modeling/meshes/editing/uv.html)
- Unwrap options: Fill Holes, Use Subdivision Surface, Original Bounds, Correct Aspect (needs a selected Image Texture node on the material in the Shader Editor), Margin Method and Margin. - [UV unwrap](https://docs.blender.org/manual/en/5.2/modeling/meshes/editing/uv.html)
- Smart UV Project (UV > Unwrap > Smart UV Project) cuts along sharp angles and projects each face group along its average normal; the manual suggests it for mechanical objects and architecture. Options: Angle Limit, Margin Method, Rotation Method, Island Margin, Area Weight, Correct Aspect, Scale to Bounds. - [UV unwrap](https://docs.blender.org/manual/en/5.2/modeling/meshes/editing/uv.html)
- Blender 5.2 added an original-bounding-box option to the Unwrap operator. - [5.2 modeling release notes](https://developer.blender.org/docs/release_notes/5.2/modeling/)

### UV island packing
- Pack Islands Rotation Method: Any, Axis-aligned, or Cardinal (90 deg turns only). - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- Margin Method: Scaled, Add, or Fraction (exact fraction of the UV square, slower). - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- Pack To: Closest UDIM, Active UDIM, Original bounding box, or Custom Region (needs Set User Region). - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- Shape Method: Exact Shape (Concave), Boundary Shape (Convex), Bounding Box. Bounding Box with Add margin is the fastest pair; Fraction margin can take up to 10x longer than Add or Scaled for some layouts. - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- 5.2 UV additions include Select by Winding (Select > Select All by Trait > Winding, catches flipped faces), delimit options on Select Linked, axis options on Copy Mirrored UV Coordinates, island support in Select Overlap and snap points in the UV editor. - [5.2 modeling release notes](https://developer.blender.org/docs/release_notes/5.2/modeling/), [UV selecting](https://docs.blender.org/manual/en/5.2/editors/uv/selecting.html)

### UV stretch overlay
- The UV editor's Display Stretch overlay colours distortion (blue low, red high), by Angle or Area, with an Opacity control. - [UV overlays](https://docs.blender.org/manual/en/5.2/editors/uv/overlays.html)

### Texel density
- No built-in texel-density tool was found on the four manual pages checked (UV editing, unwrap operators, UV overlays, UV layout); this is not a whole-manual search. - [UV editing](https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html)
- Texel Density Checker is a third-party add-on on the official Blender Extensions platform, listed for Blender 4.2 LTS and newer under GPL-3.0-or-later. It is a convenience; manual UV scaling also works. - [Texel Density Checker](https://extensions.blender.org/add-ons/texel-density-checker/)

## In practice
- For a 3D-print cleanup pass, use the Voxel remesher, not Quadriflow.
- A Decimate Collapse Ratio of 0.5 on a quad mesh keeps half the triangles, not half the quads.
- Set up a material with a selected Image Texture node before unwrapping, or Correct Aspect does nothing.
- For texel density, use the Texel Density Checker extension rather than looking for a built-in panel.

## Not verified / open questions
- Whether "Project Individual Elements" is an older name for Face Project was not checked against older manuals.
- The manual does not document a single pipeline linking Snapping, Poly Build, Shrinkwrap and the Retopology overlay: the retopology page links the overlay, Poly Build and Snapping but not Shrinkwrap. Do not cite one.
- No manual page states outright that Blender lacks a built-in texel-density feature.

Sources:
- https://docs.blender.org/manual/en/5.2/editors/3dview/display/overlays.html - Retopology overlay
- https://docs.blender.org/manual/en/5.2/modeling/meshes/retopology.html - retopology workflow, Quadriflow and its print exclusion
- https://docs.blender.org/manual/en/5.2/editors/3dview/controls/snapping.html - Snap Target Face, Face Project, Face Nearest
- https://docs.blender.org/manual/en/5.2/modeling/meshes/tools/poly_build.html - Poly Build
- https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html - Shrinkwrap modes
- https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/decimate.html - Decimate modes
- https://docs.blender.org/manual/en/5.2/modeling/meshes/uv/editing.html - seams and Pack Islands
- https://docs.blender.org/manual/en/5.2/modeling/meshes/editing/uv.html - unwrap methods, options, Smart UV Project
- https://docs.blender.org/manual/en/5.2/editors/uv/overlays.html - Display Stretch overlay
- https://docs.blender.org/manual/en/5.2/editors/uv/selecting.html - Select by Winding
- https://developer.blender.org/docs/release_notes/5.2/modeling/ - 5.2 UV and modeling changes
- https://extensions.blender.org/add-ons/texel-density-checker/ - Texel Density Checker listing
