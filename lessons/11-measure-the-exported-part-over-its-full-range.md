# Lesson 11: measure the exported part, over the feature's full range

Area: geometry checks

| What happened | Root cause | Rule now |
|---|---|---|
| A check reported a bond area and minimum widths for a small feature, and the results were relayed as a full pass. An independent reviewer measured the exported STL and found a clearly smaller bond area; the widths were design values too. | The check measured the generator's intermediate shapes, before a cleanup step that changed them, but the STL was built from the cleaned geometry. A later version copied the code and the error with it. | Every metric that gates a part is measured on the exported STL (or on the exact polygons that are extruded), never on a generator's intermediate shapes. Every check report names the file it measured. Widths are measured with an opening test or an inscribed-circle width, never with axis-aligned line scans, which misread slanted and rounded edges. A reviewer's finding is re-measured before it goes into another agent's brief. |
| A print-pose scan reported "bridge 0.0 mm" for a window feature and it was relayed as fixed. The scan stopped at the bottom of the outer outline, so the lowest part of the window was never scanned; scanning the window's own bounds found a real bridge. | The scan range was tied to other geometry, not to the feature under test, and had no positive control showing it reached the feature's lowest point. | Every geometric check states the range it scanned and asserts that it covers the bounds of the feature under test. An exact 0.0 on a changed feature is re-read before it is relayed. |

How to check: in each check report, find the line naming the measured file and the scanned range; confirm the file is the exported STL and the range covers the feature's bounding box.
