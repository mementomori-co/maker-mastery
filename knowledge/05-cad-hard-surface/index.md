# 05 CAD (hard surface) - index

Parametric and code-based CAD for printable parts: Fusion 360 workflow, its Personal Use licence limits, and a Python code-CAD toolchain. Every note lists public sources; licence terms and online help change, so re-check dated items before relying on them.

- [fusion-360-parametric-workflow-and-export.md](fusion-360-parametric-workflow-and-export.md) - parameters and expressions, sketch constraints, driving vs driven dimensions, parametric vs direct mode, components vs bodies, File > Export, mesh tools (3D Print, Save As Mesh, Tessellate, Convert Mesh), STEP export content, joints; open AP214 vs AP242 question.
- [fusion-360-personal-use-licence.md](fusion-360-personal-use-licence.md) - Personal Use eligibility (revenue OR commercial-project trigger), 3-year term and renewal window, per-format import/export table and its DXF counter-example, inactivity rule, dated document and CAM limits.
- [code-cad-toolchain.md](code-cad-toolchain.md) - manifold3d for exact Booleans, trimesh for STL I/O and validity checks (`is_watertight`, `is_volume`, `fill_holes`), float32 STL rounding, Blender BVH ray casts, and the hand-off to the repo's slicing and audit tools.
