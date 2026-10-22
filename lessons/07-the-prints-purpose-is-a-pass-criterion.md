# Lesson 07: a print's purpose is a pass criterion

Area: slicing and print gating

| What happened | Root cause | Rule now |
|---|---|---|
| Several rounds of support tuning on a display sculpture maximised support-interface coverage. The final file, a dense tree-support cage around the whole figure, passed every print-qa item and two render reviews. The print was meant to be watched while it printed, and the cage hid the sculpture from start to finish. The maker rejected it on sight. | The gates measured support quality and printability, never the print's purpose. Coverage was the metric being optimised, and the independent checks inherited it. A goal that lived only in the requester's head was never turned into a pass criterion. | Every print brief and print sheet states what the print is for, and the gate carries a check for that purpose. For a print that will be watched or displayed while printing: a visible-part ratio check (share of the part's outer surface not hidden by support, per layer and at the end), with front and isometric renders. A metric that is maximised (coverage, scar count, grams) is never the only gate: a second check states what it must not destroy. |
| The gated time and grams did not survive a re-slice in the GUI; the GUI changed the arc-fitting state. | The CLI and the GUI did not apply the same arc-fitting setting to the project, and the tolerance assumed they would agree. | A file that depends on a setting the GUI may change carries that setting explicitly, and the print sheet says what the GUI is expected to show. A GUI re-slice outside the stated tolerance is a stop, not "print anyway". |

How to check: open the print sheet and find the stated purpose; confirm the gate report has a row that tests it (for a watched print, the visible-part ratio and renders).

Tool reference: a visible-part ratio helper in `tools/` if your copy ships one; otherwise compute it from a support-preview render.
