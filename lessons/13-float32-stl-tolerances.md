# Lesson 13: STL is float32, so tolerances on STL-derived numbers must be relative

Area: code-CAD (manifold3d, trimesh)

| What happened | Root cause | Rule now |
|---|---|---|
| A check compared an exported part's volume with its analytic formula using an absolute tolerance of 1e-3 mm3 and failed, by a few thousandths of a mm3 on a part of several thousand mm3. Every other comparison passed. | manifold3d computes the solid in double precision, but its exported mesh vertices are float32 and STL stores float32 too, so a coordinate such as 56.4 becomes 56.400001525878906. The exported mesh's volume carries about 1e-6 relative noise; the absolute tolerance was tighter than the file format. | Compare analytic values against `Manifold.volume()` and `Manifold.bounding_box()` (double precision) while the solid is still in memory, and report the float32 mesh offset as its own number. Any tolerance on an STL-derived quantity is relative (at least 1e-5), or in absolute terms at least 1e-6 times the magnitude. STL coordinates are good to about 1 part in 1e7, so quote bounds to 4 decimals at most. |

How to check: in your CAD script, print both `Manifold.volume()` and the reloaded STL's volume; the difference should be tiny and relative, and your tolerance must be wider than it.

Source: STL stores IEEE 754 single-precision floats, https://en.wikipedia.org/wiki/STL_(file_format)
