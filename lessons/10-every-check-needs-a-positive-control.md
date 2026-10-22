# Lesson 10: every check needs a positive control

Area: slicing checks and tools

| What happened | Root cause | Rule now |
|---|---|---|
| A slicing wrapper searched the Bambu Studio CLI's output for "got warnings", and the notes told agents to rely on it. On Windows the CLI wrote nothing to stdout or stderr, and `result.json` `warning_message` was empty on a plate whose prime tower sat too close to an object. The check passed by being empty, not by being clean. | The warning path was read from the source code and assumed to reach the terminal. On Windows the slicer is a windowed program and its log does not reach the terminal. Nobody ran the search against a plate known to warn. | A text search on tool output counts as a check only after a positive control: the same search must fire on an input known to trigger it, and that run is recorded beside the tool. Warnings that never reach `result.json` are replicated in code (prime-tower clearance, moves outside an extruder's range, grouping mode, per-object overrides). |
| A per-object 100 % sparse infill on the Grid pattern sliced through the CLI with no warning, yet the G-code layers were not solid. Bambu Studio's GUI refuses Grid at 100 %, but the CLI never ran that check. | A GUI-side config check that the CLI does not run, and no code replicated it. | 100 % infill is set only with a pattern the slicer allows at 100 %, and a slice that relies on 100 % infill proves one solid layer from the G-code before it is gated. |

How to check: for every check in your gate, keep one known-bad input that must make it FAIL. Run it after any change to the tool; a check that cannot fail is not a check.

Tool reference: the audit helpers in `tools/` (3MF audit, G-code audit, prime-tower clearance) and their self-tests. Bambu Studio's 100 % infill pattern check: https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp
