# Lesson 09: a G-code reader must handle arc moves

Area: slicing proofs and G-code tools

| What happened | Root cause | Rule now |
|---|---|---|
| A one-off script rendered close-up proof images from sliced G-code. It parsed only G0/G1 and silently skipped millions of G2/G3 arc moves, so every image showed long straight streaks across the part. The builder looked at a few images and wrote "seen" claims; an independent render review found the streaks and voided every image. | The parser was written for one job with no positive control: no frame was compared against the slicer's own preview, and its move-type coverage was never listed. The slices had arc fitting on. | Any G-code reader used for a proof states which move types it handles and passes a positive control before its output is used: overlay one rendered layer on the slicer's own preview, or count moves per type and show the unhandled count is 0. G2/G3 are interpolated (I/J centre form) whenever arc fitting is on. A proof image that fails the control is never shown. |

How to check: count G0, G1, G2 and G3 lines in the file (for example with a short script), then confirm your reader's handled count equals the total.

Related setting: arc fitting, config key `enable_arc_fitting`. If you want the G-code to contain no arcs, slice with it off and confirm by counting G2/G3 lines.
