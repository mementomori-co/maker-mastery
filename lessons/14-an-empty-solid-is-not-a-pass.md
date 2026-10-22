# Lesson 14: an empty solid is not a pass

Area: code-CAD (manifold3d, trimesh)

| What happened | Root cause | Rule now |
|---|---|---|
| An interference check between assembled parts reported 0 mm3 overlap for every pair, in a fraction of a second. The STLs had been loaded with `trimesh.load(path, process=False)`, and `manifold3d.Manifold` built from those arrays returned an empty, non-manifold solid for each part, so every boolean intersection was empty and the check "passed". | STL triangles do not share vertices until a load with `process=True` merges duplicates. The unmerged mesh is non-manifold, and Manifold returns an empty solid instead of raising an error. A zero result looked like success. | Every mesh-based check loads with `process=True` and asserts, per part, that `Manifold.status()` is `NoError` and `volume()` is clearly above zero before any boolean. Say the load mode in the report. Add a positive control: one pair known to intersect must report a non-zero volume in the same run. A run where every check passes almost instantly is re-read, not reported. |

How to check: print each part's status and volume right after building the Manifold; any empty or error status stops the check.

Docs: manifold3d Python bindings, https://github.com/elalish/manifold ; trimesh load and `process`, https://trimesh.org/
