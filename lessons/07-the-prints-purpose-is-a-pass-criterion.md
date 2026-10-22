# Lesson 07: a print's purpose is a pass criterion

Area: slicing and print gating

| What happened | Root cause | Rule now |
|---|---|---|
| A gate that optimises one metric can pass a print that fails its purpose. Example: support tuning that maximises support-interface coverage can end in a dense tree-support cage that passes every printability check, while the print was meant to be seen as it builds and the cage hides the part from start to finish. | The gates measured support quality and printability, never the print's purpose. The optimised metric was inherited by the independent checks. A goal that lives only in the requester's head never becomes a pass criterion. | Every print brief and print sheet states what the print is for, and the gate carries a check for that purpose. For a print that will be watched or displayed while printing: a visible-part ratio check (share of the part's outer surface not hidden by support, per layer and at the end), with front and isometric renders. A metric that is maximised (coverage, scar count, grams) is never the only gate: a second check states what it must not destroy. |
| The gated time and grams did not survive a re-slice in the GUI; the GUI changed the arc-fitting state. | The CLI and the GUI did not apply the same arc-fitting setting to the project, and the tolerance assumed they would agree. | A file that depends on a setting the GUI may change carries that setting explicitly, and the print sheet says what the GUI is expected to show. A GUI re-slice outside the stated tolerance is a stop, not "print anyway". |

How to check: open the print sheet and find the stated purpose; confirm the gate report has a row that tests it (for a watched print, the visible-part ratio and renders).

Tool reference: a visible-part ratio helper in `tools/` if your copy ships one; otherwise compute it from a support-preview render.
