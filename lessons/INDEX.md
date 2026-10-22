# Lessons index

One line per lesson. Read the file for the full table. See [README.md](README.md) for the format and how to add your own.

## Slicing and print

- [01-overhang-angle-convention.md](01-overhang-angle-convention.md) - one shared definition of overhang angle, matching Bambu Studio's support threshold.
- [02-support-is-the-last-resort.md](02-support-is-the-last-resort.md) - design overhangs out first; same-filament support Top Z distance is a measured value.
- [03-check-a-rule-against-your-own-printer.md](03-check-a-rule-against-your-own-printer.md) - generic or other-model rules and features are verified on your own printer before use.
- [04-never-slice-over-a-gated-file.md](04-never-slice-over-a-gated-file.md) - gated print files are read-only; experiments use a work folder; the proof's hash is the truth.
- [05-slice-info-overrides-the-plate-map.md](05-slice-info-overrides-the-plate-map.md) - regrouping a sliced 3MF means editing slice_info.config too; trust only the G-code header.
- [06-island-checks-on-printable-layers.md](06-island-checks-on-printable-layers.md) - island and empty-layer checks run on sections opened by half a line width; crops re-run the census.
- [07-the-prints-purpose-is-a-pass-criterion.md](07-the-prints-purpose-is-a-pass-criterion.md) - state what a print is for and gate on it; a maximised metric is never the only gate.
- [08-split-only-at-natural-boundaries.md](08-split-only-at-natural-boundaries.md) - split sculptures at characters, accessories and bases, never with a plane through the body.
- [09-gcode-readers-must-handle-arcs.md](09-gcode-readers-must-handle-arcs.md) - a G-code reader states its move types and passes a control against the slicer preview.
- [10-every-check-needs-a-positive-control.md](10-every-check-needs-a-positive-control.md) - a check that has never fired on a known-bad input is not a check.
- [11-measure-the-exported-part-over-its-full-range.md](11-measure-the-exported-part-over-its-full-range.md) - gating metrics come from the exported STL and a scan range that covers the feature.
- [12-quote-the-clause-and-fix-every-copy.md](12-quote-the-clause-and-fix-every-copy.md) - a sourced fact quotes its source; a correction is applied to every copy.

## CAD

- [13-float32-stl-tolerances.md](13-float32-stl-tolerances.md) - STL is float32; tolerances on STL-derived numbers are relative.
- [14-an-empty-solid-is-not-a-pass.md](14-an-empty-solid-is-not-a-pass.md) - load meshes with process=True and assert a valid, non-empty Manifold before booleans.
- [15-section-to-polygon-keeps-holes.md](15-section-to-polygon-keeps-holes.md) - convert cross-sections by even-odd XOR and assert the area.

## Agent and tool hygiene

- [16-windows-paths-in-shell-and-string-text.md](16-windows-paths-in-shell-and-string-text.md) - Windows paths go through Write/Edit or raw strings only; scan for control characters.
- [17-agents-never-delete-files.md](17-agents-never-delete-files.md) - deleting is the maker's call, even for an agent's own files; rename to SUPERSEDED_ instead.
- [18-scratch-scripts-need-unique-names.md](18-scratch-scripts-need-unique-names.md) - task-specific scratch names; appends assert their target.
- [19-settings-backups-can-hold-secrets.md](19-settings-backups-can-hold-secrets.md) - never copy app profile or settings folders into a shared place.
- [20-no-personal-identifiers-in-requests.md](20-no-personal-identifiers-in-requests.md) - never put a personal identifier in a User-Agent or request header.
