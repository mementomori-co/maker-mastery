# Lesson 02: support is the last resort, and Top Z distance is measured

Area: slicing and print

| What happened | Root cause | Rule now |
|---|---|---|
| After a flat ledge on a display piece sagged, the agents wrote a new standard: "every visible overhang or flat ceiling gets support or a 45 deg underside". That rule ignores the cost of support. Without a dedicated support filament, support is printed in the same filament as the part, and the support Top Z distance decides both the underside quality and how much damage removal does. Too close and removal can hurt the surface more than no support at all. | The rule treated support as a free fix. The only Top Z value in use came from a general wiki sentence, not from a scored print on that printer and filament. The rule was also written in the agents' own words, without asking how the maker actually supports parts. | 1. Design it out first: on visible faces prefer a chamfered or angled underside, a split at a natural part boundary with keyed joints, or a new orientation. 2. When support is unavoidable and the support is the same filament, the design review writes down why support scars beat sag on that face. 3. Top Z distance is a measured value: until a support-removal coupon has been printed and scored on your printer and filament, every Top Z value in a print sheet is labelled "not verified". 4. A making rule that changes how the maker prints is written from the maker's own practice; ask when it is not known. |

How to check: for every print sheet that uses support, confirm the Top Z distance either cites a scored coupon or carries the "not verified" label, and that the design review names why support was chosen over a design change.

Related: `Support > Support > Top Z distance` (config key `support_top_z_distance`) in Bambu Studio (label not verified). Bambu wiki support page: https://wiki.bambulab.com/en/software/bambu-studio/support
