# Code-CAD toolchain: manifold3d, trimesh and Blender for printable solids

Applies to: any printer (geometry tooling) · manifold3d and trimesh at the versions pinned in [requirements.txt](../../requirements.txt); Blender headless for heavy ray casts
Verified: 2026-10-04

## Facts
- trimesh `Trimesh.is_watertight` checks that every edge is shared by exactly two faces and returns a bool. - [trimesh.base docs](https://trimesh.org/trimesh.base.html)
- trimesh `Trimesh.is_volume` is stricter: the mesh must be watertight, consistently wound and have outward-facing normals to count as a valid volume rather than just a surface. - [trimesh.base docs](https://trimesh.org/trimesh.base.html)
- trimesh `Trimesh.fill_holes()` fills only single-triangle and single-quad holes and returns whether the mesh is watertight afterwards. - [trimesh.base docs](https://trimesh.org/trimesh.base.html)
- manifold describes itself as "a guaranteed-manifold mesh Boolean algorithm". Importing your own mesh data fails if it is not manifold. - [manifold README](https://raw.githubusercontent.com/elalish/manifold/master/README.md)
- manifold ships a `Merge` function for slightly non-manifold meshes; more damaged input needs an external repair tool of the kind made for 3D printing. - [manifold README](https://raw.githubusercontent.com/elalish/manifold/master/README.md)
- Binary STL stores each vertex coordinate as a 32-bit IEEE float, so a mesh exported from double-precision geometry is rounded on export. - [STL (file format), Wikipedia](https://en.wikipedia.org/wiki/STL_(file_format))
- Blender's Python API offers a BVH tree (`mathutils.bvhtree.BVHTree.FromPolygons`, then `ray_cast`) for ray queries against a mesh. - [Blender Python API: mathutils.bvhtree](https://docs.blender.org/api/current/mathutils.bvhtree.html)
- Other repair routes for meshes manifold rejects: Blender's 3D Print Toolbox Make Manifold (see [sculpt-to-printable.md](../06-organic-modeling/sculpt-to-printable.md)) and Bambu Studio's Fix Model (see [ai-mesh-repair-for-fdm.md](../26-ai-to-3d/ai-mesh-repair-for-fdm.md)).

## In practice
- Division of labour that works: manifold3d builds the solids and does exact Booleans in double precision (`Manifold.volume()`, `bounding_box()`); trimesh loads and saves STL, reports `is_watertight`, `is_volume`, bounds and face counts, and does per-face geometry such as overhang angles.
- Keep the analytic expectations (volume, bounds) in the generating script and assert them against the manifold values before export. Report the volume change caused by float32 STL rounding as its own number instead of hiding it inside a loose tolerance.
- Before any mesh pipeline, run one import probe for the optional engines (`scipy`, `networkx`, `rtree`, `manifold3d`) and design against what is actually present; several trimesh functions silently need one of them.
- Load STLs with `trimesh.load(path, process=True)` before making any topology statement, and say in your report that stats are "after duplicate-vertex merge".
- Keep the generating script beside every STL it produces, so the part can be regenerated and audited.
- Every CAD output then goes through the repo's slicing and audit tools: [slice_cli.py](../../tools/slice_cli.py), [audit_3mf.py](../../tools/audit_3mf.py), [tower_clearance.py](../../tools/tower_clearance.py) and [gcode_audit.py](../../tools/gcode_audit.py). The checks Bambu Studio only does in its GUI are listed in [gui-checks.md](../02-bambu-studio/gui-checks.md).
- Write multi-line scripts to a file and run them; do not paste Windows paths through shell heredocs, which can mangle backslashes.

## Not verified / open questions
- trimesh's built-in ray engine ran out of memory on a mesh of about 117k triangles in one local test, while Blender's BVH tree handled the same ray count; not verified (no public source). Benchmark on your own machine before choosing.
- A Fusion 360 to code-CAD STEP round-trip with a small volume difference has not been demonstrated.
- No shared helper library (bosses, tabs, fillets) is included; each script carries its own helpers.

Sources:
- https://trimesh.org/trimesh.base.html - `is_watertight`, `is_volume`, `fill_holes` behaviour
- https://raw.githubusercontent.com/elalish/manifold/master/README.md - manifold Boolean guarantee, `Merge`, external repair
- https://en.wikipedia.org/wiki/STL_(file_format) - binary STL uses 32-bit floats
- https://docs.blender.org/api/current/mathutils.bvhtree.html - BVHTree ray casting API
