# Sculpt to printable (Blender 5.2)

Applies to: any printer · Blender 5.2 LTS manual (`/manual/en/latest/` path, read 2026-10-03); 3D Print Toolbox extension v1.4.1
Verified: 2026-10-04

## Facts

### Sculpt Mode Remesh (voxel)
- The Remesh operator's shortcut is Ctrl-R, not R; R only adjusts Voxel Size interactively once the Remesh panel is open. - [Blender Manual: Remesh (Sculpt Mode)](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html)
- Voxel Size (Sidebar > Tool > Remesh): lower values keep finer detail but make a much denser mesh. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html)
- Adaptivity above 0 reduces face count where detail is not needed, and disables Fix Poles. Fix Poles trades some speed for fewer poles and better flow. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html)
- Preserve Volume, Paint Mask, Face Sets and Color Attributes reproject those layers onto the new mesh; voxel remesh otherwise builds a new manifold mesh and drops other data layers. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html)
- Remesh acts only on the original mesh data (not modifier, shape-key or rig results) and does not work with the Multiresolution modifier. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html)

### Dyntopo
- Detail Size / Percentage / Resolution (Sidebar > Tool > Dyntopo); R previews detail density in the viewport. - [Blender Manual: Dyntopo](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html)
- Refine Method (Subdivide Edges, Collapse Edges, Subdivide Collapse) sets whether dyntopo adds, removes or both. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html)
- Detailing (Relative, Constant, Brush, Manual) changes how the detail size is computed. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html)
- Detail Flood Fill (Ctrl-R) re-fills the whole object to one detail level; only with Constant or Manual detailing. - [same page](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html)

### Remesh modifier (non-destructive)
- Modes: Blocks, Smooth, Sharp (with Sharpness) and Voxel (OpenVDB, a new manifold mesh that tries to keep volume). - [Blender Manual: Remesh Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html)
- Voxel mode options are Adaptivity and Smooth Shading; Octree Depth and Scale set resolution for the other modes. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html)
- Remove Disconnected (with Threshold) strips small loose pieces; a flat input needs a Solidify modifier above Remesh. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html)

### Multiresolution modifier
- Viewport / Sculpt / Render levels (Alt-1 and Alt-2 in Sculpt Mode); no numeric maximum is given. - [Blender Manual: Multiresolution](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html)
- Multiresolution cannot sit after any modifier that changes geometry or object data. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html)
- To reproject detail from another sculpt with Shrinkwrap, the manual uses Wrap Method Project, Snap Mode Above Surface, Negative on. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html)
- Delete Higher, Rebuild Subdivisions, Apply Base and Conform Base manage the base mesh vs stored levels. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html)

### Mesh prep (Bisect, Boolean, Solidify, Shrinkwrap)
- Bisect (Edit Mode: Mesh > Bisect) cuts with an infinite plane; options Flip, Fill, Clear Inner/Outer, Axis Threshold. Clear Inner/Outer can affect geometry outside the selection. - [Blender Manual: Bisect](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html)
- Boolean operations: Intersect, Union, Difference. Solvers: Float (fast, no overlaps), Exact (handles overlaps, slow), Manifold (usually fastest, manifold input only). Only manifold input is guaranteed correct. - [Blender Manual: Boolean](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)
- Exact's Self Intersection and Hole Tolerant options cost speed; use Hole Tolerant only when Exact shows errors on non-manifold input. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)
- Solidify: Thickness and Offset (-1 to 1); the manual says final wall thickness is not guaranteed. Simple fails where an edge has more than two faces; Complex always gives manifold output but is slower. - [Blender Manual: Solidify](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html)
- Solidify works in local coordinates, so non-uniform object scale gives uneven walls; apply scale first. - [same page](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html)
- Shrinkwrap moves each vertex to a target surface using one of four wrap methods; Project casts along an axis with Negative/Positive and an Above Surface offset. - [Blender Manual: Shrinkwrap](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html)

### Export for printing
- File > Export > Stl (.stl) options: Scale, Scene Unit, Forward/Up axes, Apply Modifiers, Properties (Viewport or Render, new in 5.2), ASCII, Batch, Selection Only. - [Blender Manual: STL](https://docs.blender.org/manual/en/latest/files/import_export/stl.html)
- The 5.2 STL exporter defaults to Render evaluation (`evaluation_mode='DAG_EVAL_RENDER'` in `bpy.ops.wm.stl_export`), so a Multires or Subdivision render level higher than the viewport level is exported silently. - [Blender Manual: STL](https://docs.blender.org/manual/en/latest/files/import_export/stl.html), [bpy.ops.wm](https://docs.blender.org/api/current/bpy.ops.wm.html)
- Blender 5.2 has no built-in 3MF import or export; the format index does not list it. - [Blender Manual: Import-Export](https://docs.blender.org/manual/en/latest/files/import_export/index.html)
- The 3D Print Toolbox extension (v1.4.1, GPL-3.0-or-later, Blender 4.2 LTS and newer) offers volume and area stats, bad-geometry checks, Make Manifold, Hollow, bed align, scale-to-fit and quick export. Its changelog notes the 5.2 STL render-settings default and a Hollow error with Python 3.14. - [extensions.blender.org: 3D Print Toolbox](https://extensions.blender.org/add-ons/print3d-toolbox/)
- Its Checks panel operators include `check_solid`, `check_intersect`, `check_degenerate`, `check_nonplanar`, `check_thick`, `check_sharp`, `check_overhang`, `check_shells` and `check_all`. - [extension source ui.py](https://projects.blender.org/extensions/print3d_toolbox/raw/branch/main/source/ui.py), [manifest](https://projects.blender.org/extensions/print3d_toolbox/raw/branch/main/source/blender_manifest.toml)
- The legacy manual describes Solid as a check for non-manifold and bad contiguous edges, and Make Manifold as fixing normals, filling holes and removing empty edges and faces. - [Blender Manual 4.1: 3D Print Toolbox](https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html)

## In practice
- Sculpt with Dyntopo or Multires, then use a voxel remesh to get a clean, manifold mesh before export.
- Before exporting STL from a model with Multires or Subdivision, set File > Export > Stl (.stl) > Geometry > Properties to Viewport if you want what you see (label path read from the manual, not checked on screen).
- Check for non-manifold geometry (Edit Mode: Select > All by Trait > Non Manifold, or the Toolbox's Check All) before Booleans or export.
- Apply object scale before Solidify.
- Export STL (or OBJ/PLY) and build the 3MF in Bambu Studio; there is no native 3MF path in 5.2.
- Running Blender headless: point the repo at your Blender install path, set in config\paths.yaml (`blender_exe`).

## Not verified / open questions
- Third-party 3MF add-ons for Blender were not checked.
- The `/manual/en/latest/` URLs will move to a newer manual after the next release; switch to `/manual/en/5.2/` when re-checking.

Sources:
- https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html - Sculpt Remesh
- https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/dyntopo.html - Dyntopo
- https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/remesh.html - Remesh modifier
- https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html - Multiresolution
- https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html - Solidify
- https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/bisect.html - Bisect
- https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html - Boolean
- https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/shrinkwrap.html - Shrinkwrap
- https://docs.blender.org/manual/en/latest/files/import_export/stl.html - STL export
- https://docs.blender.org/manual/en/latest/files/import_export/index.html - format list, no 3MF
- https://docs.blender.org/api/current/bpy.ops.wm.html - `wm.stl_export` default
- https://extensions.blender.org/add-ons/print3d-toolbox/ - 3D Print Toolbox listing and changelog
- https://projects.blender.org/extensions/print3d_toolbox/raw/branch/main/source/ui.py - Checks panel operators
- https://projects.blender.org/extensions/print3d_toolbox/raw/branch/main/source/blender_manifest.toml - version 1.4.1
- https://docs.blender.org/manual/en/4.1/addons/mesh/3d_print_toolbox.html - legacy check descriptions
