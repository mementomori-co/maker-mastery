r"""test_gcode_audit.py - unit tests for tools\gcode_audit.py (per-feature extents, support, arcs, bridge rows, exit codes).

Synthetic plate G-code only, written to a temporary folder. The tool runs as a subprocess with this interpreter.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_gcode_audit.py" -v
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
TOOL = os.path.join(TOOLS, "gcode_audit.py")


def run(text: str | None, *extra: str, path: str | None = None, as_json: bool = True):
    with tempfile.TemporaryDirectory() as td:
        if path is None:
            path = os.path.join(td, "plate_1.gcode")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        args = [sys.executable, "-I", "-B", TOOL, path, *extra] + (["--json"] if as_json else [])
        p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (json.loads(p.stdout) if as_json and p.stdout.strip() else p.stdout)


class GcodeAuditTest(unittest.TestCase):
    def test_support_arc_length_and_text_lines(self):
        g = ("; FEATURE: Outer wall\nG1 X100 Y100 F600\n; start printing object, unique label id: 7\n; FEATURE: Support\n"
             "G1 X110 Y100 E1\nG2 X130 Y100 I10 J0 E2\n; stop printing object, unique label id: 7\n")
        rc, j = run(g)
        self.assertEqual(rc, 1)
        self.assertEqual(j["support_length_mm"], round(10 + 10 * math.pi))
        self.assertEqual(j["arc_segments"], 1)
        self.assertAlmostEqual(j["arc_length_mm"], 10 * math.pi, delta=0.05)
        self.assertIn("7", j["objects"])
        _, txt = run(g, as_json=False)
        lines = txt.splitlines()
        self.assertIn("  arc segments: 1, arc length: 31.4 mm", lines)
        for start in ("G-code audit:", "  tool changes:", "  [WARN] support extrusion present:", "VERDICT: WARN"):
            self.assertTrue(any(l.startswith(start) for l in lines), start)

    def test_outside_x_range_and_custom_ignored(self):
        g = ("; FEATURE: Custom\nG1 X5 Y5\nG1 X10 Y5 E1\n; FEATURE: Outer wall\nG1 X100 Y100\nG1 X330 Y100 E1\n")
        rc, j = run(g)
        self.assertEqual(j["outside_points"], 1)
        self.assertEqual(j["custom_outside_points"], 2 - 1)   # the Custom extrusion end point at X10 lies outside 25..325
        self.assertEqual(rc, 1)
        rc2, j2 = run(g, "--xmin", "0", "--xmax", "350")
        self.assertEqual(j2["outside_points"], 0)
        self.assertEqual(rc2, 0)

    def test_header_tool_changes_and_filament_map(self):
        g = "; filament_map = 2,1\n; filament_map_mode = Manual\nT0\n; FEATURE: Outer wall\nG1 X100 Y100\nG1 X120 Y100 E1\nT1\nG1 X140 Y100 E1\n"
        rc, j = run(g)
        self.assertEqual(j["header"].get("filament_map"), "2,1")
        self.assertEqual(j["header"].get("filament_map_mode"), "Manual")
        self.assertEqual(j["tool_changes"], 2)
        self.assertIn("Outer wall | T0", j["features"])
        self.assertIn("Outer wall | T1", j["features"])
        self.assertEqual(rc, 0)

    def test_no_bridges_no_bridge_finding(self):
        g = ("; Z_HEIGHT: 0.2\n; FEATURE:Outer wall\nG1 X100 Y100 Z0.2 E0\nG1 X120 Y100 E1\nG1 X120 Y120 E1\n"
             "; Z_HEIGHT: 0.4\n; FEATURE:Inner wall\nG1 X100 Y100 Z0.4 E0\nG1 X119 Y101 E1\n")
        rc, j = run(g)
        self.assertEqual(j["bridges"], [])
        self.assertFalse([x for x in j["findings"] if "bridge" in x["msg"].lower()])
        self.assertEqual(rc, 0)

    def _two_layer(self):
        lines = ["; Z_HEIGHT: 0.2", "; FEATURE:Internal solid infill", "G1 X30 Y30 Z0.2 E0"]
        for k in range(0, 21):   # a 20 x 20 solid raster, lines 1 mm apart, at X 30..50
            lines += [f"G1 X30 Y{30 + k} E0", f"G1 X50 Y{30 + k} E1"]
        lines += ["; Z_HEIGHT: 0.4", "; FEATURE:Bridge", "G1 X30 Y40 Z0.4 E0", "G1 X50 Y40 E1",   # over the raster
                  "G1 X80 Y40 E0", "G1 X100 Y40 E1"]                                             # over nothing
        return "\n".join(lines) + "\n"

    def test_bridge_row_supported_half_and_warn_without_limit(self):
        rc, j = run(self._two_layer())
        row = [r for r in j["bridges"] if r["feature"] == "Bridge"][0]
        self.assertEqual(row["segments"], 2)
        self.assertAlmostEqual(row["longest_line_mm"], 20.0, places=6)
        self.assertAlmostEqual(row["supported_below"], 0.5, delta=0.05)
        w = [f for f in j["findings"] if f["level"] == "WARN" and f["msg"].startswith("bridge spans present")]
        self.assertEqual(len(w), 1)
        self.assertIn("No measured clean-span limit", w[0]["msg"])
        self.assertIsNone(j["bridge_limit_mm"])
        self.assertEqual((rc, j["verdict"]), (1, "WARN"))

    def test_bridge_limit_fail_and_pass(self):
        rc_f, jf = run(self._two_layer(), "--bridge-limit", "1.0")
        self.assertEqual(rc_f, 2)
        self.assertTrue(any(x["level"] == "FAIL" and "exceeds the measured clean limit 1.0 mm" in x["msg"] for x in jf["findings"]))
        rc_ok, jo = run(self._two_layer(), "--bridge-limit", "100.0")
        self.assertEqual((rc_ok, jo["verdict"]), (0, "OK"))

    def test_arc_below_bridge_sampled_along_arc(self):
        g = ("; Z_HEIGHT: 0.2\n; FEATURE:Outer wall\nG1 X40 Y40 Z0.2 E0\nG3 X60 Y40 I10 J0 E2\n"
             "; Z_HEIGHT: 0.4\n; FEATURE:Bridge\nG1 X48 Y30 Z0.4 E0\nG1 X52 Y30 E1\n")
        _rc, j = run(g)
        row = [r for r in j["bridges"] if r["feature"] == "Bridge"][0]
        self.assertGreaterEqual(row["supported_below"], 0.6)

    def test_rows_keyed_by_z_height_block_after_z_hop(self):
        g = ("; Z_HEIGHT: 0.2\n; FEATURE:Outer wall\nG1 X30 Y30 Z0.2 E0\nG1 X50 Y30 E1\n"
             "; Z_HEIGHT: 0.4\n; FEATURE:Bridge\nG1 X30 Y30 Z0.4 E0\nG1 Z0.6\nG1 X30 Y30 Z0.4\nG1 X50 Y30 E1\n")
        _rc, j = run(g)
        rows = [r for r in j["bridges"] if r["feature"] == "Bridge"]
        self.assertEqual(len(rows), 1)
        self.assertAlmostEqual(rows[0]["z"], 0.4)
        self.assertEqual(rows[0]["supported_below"], 1.0)

    def test_unreadable_input_exits_3(self):
        with tempfile.TemporaryDirectory() as td:
            rc, _ = run(None, path=os.path.join(td, "no_such_plate.gcode"), as_json=False)
        self.assertEqual(rc, 3)


if __name__ == "__main__":
    unittest.main()
