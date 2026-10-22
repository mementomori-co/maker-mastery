# Support enforcers, Support critical regions only, and Tree Hybrid tip rules
Applies to: both (H2C, P1S) · Bambu Studio 02.08.02.61 (source tag v02.08.02.61)
Verified: 2026-10-06

Scope: how a support enforcer, the "Support critical regions only" option and the Tree Hybrid tip and BigFlat thresholds behave in code. Condition for everything below: support type tree(auto), Tree Hybrid style, tag v02.08.02.61. Short links: TS = [TreeSupport.cpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp), SP = [SupportParameters.hpp](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp).

## Facts
- **Inside an enforcer, every outward step counts as overhang, with no threshold angle.** The overhang is this layer minus the layer below, intersected with the enforcer, with no lower-layer offset. In the tree(auto) branch the result is grown by 0.8 mm (the tree tip diameter) and the layer below is subtracted again. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L696-697, L938-949
- A source comment calls this a hack to make enforcers work on steep overhangs (internal ticket STUDIO-7538); it sits in the non-auto branch, and tree(auto) runs the same code. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L947-954
- **Support critical regions only, inside an enforcer layer:** every overhang intersected with the enforcer plus 0.8 mm is kept. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L1222, L1232-1233
- **Support critical regions only, outside an enforcer:** the layer's overhangs are cleared except cantilevers, which are added back; sharp tails are then added back too (support every 1 mm of height). -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L1216-1220, L1246-1257
- Painted Enforce facets are projected into the same per-layer enforcers, so they follow the same rules as an enforcer volume (mechanism from code; not tested in a slice). -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L890
- **BigFlat** (the Tree Hybrid flat-area fill) is set when the merged overhang cluster is larger than 10 x 10 mm = **100 mm2** (merged over its layers). -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L827; [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp) L320
- **Per-layer test:** a Hybrid leftover polygon goes to regular tree tips unless it passes a stability check and is at least 2 x 2 mm = **4 mm2** on that layer. The 100 mm2 and 4 mm2 numbers are different tests (cluster vs per-layer polygon). The stability check uses the layer's height, so a thin sliver high on a part fails it. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L650-657, L4244
- **Regular tips:** one at every corner sharper than about 135 deg, one every `tree_support_branch_distance` along each contour, plus inner grid points. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L4097, L4270-4314
- **Roofs are not merged when On build plate only is on**, because some nodes underneath may have been deleted. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L2430-2433
- **Double-wall threshold when `tree_support_wall_count` = -1:** the filament's `impact_strength_z` is used as a diameter, area = 0.25 x pi x d2. For example, impact_strength_z = 6.6 gives about 34.2 mm2 (check the value in your own filament profile). -- [SP](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp) L233-235
- Branch walls can also be doubled whenever a branch needs an extra wall (merged parents, large moves, tall branches near the top), whatever the area threshold says. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L1859-1861, L3816-3818

## In practice
- An enforcer volume around a gently curved underside makes the slicer start tips on nearly every thin layer, because each layer sticks out a little past the one below, and each sliver is far below 4 mm2, so no flat Hybrid fill appears. Prefer a small enforcer over only the area that needs support, or reshape the underside to 45 deg or steeper.
- Never read a "Support critical regions only" slice as "no support except where I asked": cantilevers and sharp tails still get support, and inside an enforcer everything does.
- To check on your own slice, open Preview with the Line Type view and look at the support inside the enforcer region layer by layer; short scattered tip segments mean the per-layer rule above is in effect.
- Check the actual roof gap under such tips as described in [support-top-z-same-filament.md](support-top-z-same-filament.md); the typed Top Z is not always the printed gap.

## Not verified / open questions
- Cantilever definition in code: the farthest point of the region is more than 3 mm from the base, or the contour floats completely (the base is the lower layer offset by about 0.5 mm); a sharp tail is a region that does not overlap the lower layer and is under 100 mm2. Which layers of a real part pass the 3 mm test cannot be traced without a debug log. -- [TS](https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp) L979-1045
- A G-code reading cannot tell a brim anchor ring from a forced double wall on a branch.
- Why a 0.24 mm Top Z on a 0.12 mm layer grid can print a larger gap: not traced (possibly the roof collision window, TS L2388-2393, unconfirmed).

Sources:
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/TreeSupport.cpp -- enforcer overhang rule, critical regions, BigFlat, per-layer 4 mm2, tip rules, roof merge
- https://raw.githubusercontent.com/bambulab/BambuStudio/v02.08.02.61/src/libslic3r/Support/SupportParameters.hpp -- big overhang threshold, double-wall area
