# Lesson 08: split a sculpture only at natural part boundaries

Area: design for FDM

| What happened | Root cause | Rule now |
|---|---|---|
| To reduce support, a search scored a very large number of cutting planes on support volume, seam length and visibility. The winning cut was a plane through the whole figure, across hair and body. The builder noted that the cut crossed details at random; the candidate was still chosen on its numbers. The maker rejected it: a figure maker separates characters, accessories and bases, but never slices the main body in half. | The brief allowed a plane through the main body to be a candidate at all, and optimised metrics instead of the craft rule a modeller applies first. "Best cut set" was read as licence for any plane. | Split only at natural part boundaries: separate characters, accessories and bases. Never a plane through a sculpture, a face, hair or the main body. A candidate that cuts the main body is not generated, so it cannot win on numbers. Joints are keyed (pins, sockets, pockets) with fit clearances taken from a printed coupon. A hard constraint the requester holds is written into the brief as a constraint; "best by the numbers" never overrides it. |

How to check: before scoring any split, list each cut and the boundary it follows (character, accessory, base). Any cut you cannot name that way is removed from the candidate set.
