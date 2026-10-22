# Lesson 15: converting a cross-section to polygons must keep its holes

Area: code-CAD (manifold3d, shapely)

| What happened | Root cause | Rule now |
|---|---|---|
| A wall-thickness check on a part with an internal pocket found no wall in any direction, and a removed-area figure read as the whole pocket. | The helper built the section with `unary_union([Polygon(c) for c in cross_section.to_polygons()])`, which treats every contour as solid, so holes (the pocket, the gaps in a lattice) were filled in. | Never union raw contours. Convert a manifold3d `CrossSection` by an even-odd XOR of its contours (a `symmetric_difference` chain, largest first) and assert the result's area equals `CrossSection.area()` within 1e-3 relative. Keep one tested helper and reuse it; do not rewrite it per script. |
| A second attempt classified contours as holes by testing whether each polygon's representative point lay inside another contour, and lost most of the area. | A shell polygon's representative point can fall inside one of its own holes, so an outer contour was counted as nested inside a hole. | Any nesting test uses a point on the ring or an exact area assertion; the XOR route needs neither. |
| Stacked small offsets of a section reloaded from STL as non-watertight. | Sub-micron contour segments from `CrossSection.offset` collapse in float32. | Simplify after offsetting (for example `simplify(0.001)`), snap to float32, merge vertices and drop degenerate faces before export; the reload check reports the count. |

How to check: for every section you convert, assert `abs(polygon.area - cross_section.area()) / cross_section.area() < 1e-3`.
