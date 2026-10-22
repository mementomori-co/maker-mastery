# Lesson 01: one definition of "overhang angle"

Area: slicing and design for FDM

| What happened | Root cause | Rule now |
|---|---|---|
| A design-review agent produced an overhang table that measured slope as 90 deg minus the angle between the face normal and straight down. That is the inverse of what Bambu Studio means by its support threshold angle, so every face was classed the wrong way round. The agent caught it on a re-run, but the wrong table existed for one pass and could have been relayed. | Nothing in the knowledge base fixed what "overhang angle" means, so each agent and each script re-derived it, and two of them chose opposite conventions. | Overhang angle = the angle between the face normal and the -Z (down) direction. A face needs support when that angle is **below** `support_threshold_angle` (Bambu Studio tooltip: support is generated for overhangs whose slope angle is below the threshold). A flat ceiling is 0 deg; a vertical wall is 90 deg. Every geometry tool prints the convention it uses in its header. |

Related: an assembly or fit check counts only when its script and its output are saved beside the parts it checked. A note that says "checked" with no script on disk is a claim, not a check.

How to check: run your overhang script on a test solid with a known flat ceiling (expect 0 deg, flagged) and a vertical wall (expect 90 deg, not flagged) before trusting it on a real part.

Source: Bambu Studio `support_threshold_angle` definition and tooltip, https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp
