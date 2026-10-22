r"""test_interface_coverage.py - unit tests of tools\interface_coverage.py with synthetic plate G-code.

Fixtures (all written by the tests to a temp folder): a wall with a 2 mm lip one layer up, with and without support interface
under it; a lip whose interface is missing under one end; a closed box roof over walls vs over sparse infill; the filter
header keys; a sliced-3MF zip holding Metadata/plate_1.gcode; usage errors.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p test_interface_coverage.py -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
TOOL = os.path.join(TOOLS, "interface_coverage.py")

try:
    import numpy  # noqa: F401
    import scipy  # noqa: F401
    HAVE, WHY = True, ""
except ImportError as e:  # pragma: no cover
    HAVE, WHY = False, f"interface_coverage needs numpy and scipy: {e}"

OX, OY = 50.0, 60.0   # plate offset of the fixtures


def header(support=1, crit=0, rso=0):
    return ["; CONFIG_BLOCK_START", f"; enable_support = {support}", f"; support_critical_regions_only = {crit}",
            f"; support_remove_small_overhang = {rso}", "; support_line_width = 0.42", "; support_interface_spacing = 0.5",
            "; support_interface_top_layers = 3", "; CONFIG_BLOCK_END"]


def lip(length=20.0):
    """a wall at y 0..0.4 (z 5.0) and three Overhang wall lines at y 1.2 / 1.6 / 2.0 one layer up (z 5.2)"""
    L, x0, y = length, OX, OY
    return ["; Z_HEIGHT: 5.0", "; LAYER_HEIGHT: 0.2", "; FEATURE:Outer wall", f"G1 X{x0} Y{y} Z5.0 E0", f"G1 X{x0 + L} Y{y} E2",
            f"G1 X{x0 + L} Y{y + 0.4} E0.1", f"G1 X{x0} Y{y + 0.4} E2",
            "; Z_HEIGHT: 5.2", "; LAYER_HEIGHT: 0.2", "; FEATURE:Overhang wall", f"G1 X{x0} Y{y + 2.0} Z5.2 E0", f"G1 X{x0 + L} Y{y + 2.0} E2",
            f"G1 X{x0 + L} Y{y + 1.6} E0.1", f"G1 X{x0} Y{y + 1.6} E2", f"G1 X{x0} Y{y + 1.2} E0.1", f"G1 X{x0 + L} Y{y + 1.2} E2"]


def interface(x0, x1):
    out = ["; Z_HEIGHT: 4.8", "; LAYER_HEIGHT: 0.28", "; FEATURE:Support interface"]
    for y in (1.0, 1.5, 2.0):
        out += [f"G1 X{x0} Y{OY + y} Z4.8 E0", f"G1 X{x1} Y{OY + y} E2"]
    return out


def ring(z, feature, s=20.0):
    x0, y0, x1, y1 = OX, OY, OX + s, OY + s
    return [f"; FEATURE:{feature}", f"G1 X{x0} Y{y0} Z{z} E0", f"G1 X{x1} Y{y0} E2", f"G1 X{x1} Y{y1} E2", f"G1 X{x0} Y{y1} E2", f"G1 X{x0} Y{y0} E2"]


def bridge_lines():
    return ["; FEATURE:Bridge"] + [f"G1 X{OX + 0.6 + 0.5 * k:.2f} Y{OY + 0.4} E0\nG1 X{OX + 0.6 + 0.5 * k:.2f} Y{OY + 19.6} E2" for k in range(38)]


@unittest.skipUnless(HAVE, WHY)
class InterfaceCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="mm_interface_cov_")

    def write(self, name, lines):
        p = os.path.join(self.tmp, name + ".gcode")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        return p

    def run_tool(self, *args, json_out=True):
        cmd = [sys.executable, "-I", "-B", TOOL, *args]
        js = None
        if json_out:
            js = os.path.join(tempfile.mkdtemp(dir=self.tmp), "r.json")
            cmd += ["--json", js]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        data = {}
        if js and os.path.exists(js):
            with open(js, encoding="utf-8") as fh:
                data = json.load(fh)
        return p.returncode, data, (p.stdout or "") + (p.stderr or "")

    def test_unsupported_lip_fails(self):
        rc, j, out = self.run_tool(self.write("lip", header() + lip()))
        vis = [g for g in j["regions"] if g["visible_candidate"]]
        self.assertEqual(len(vis), 1, vis)
        self.assertEqual(vis[0]["supported_pct"], 0.0)
        self.assertTrue(1.0 < vis[0]["depth_max"] <= 1.7, vis[0])
        self.assertEqual(vis[0]["kind"], "overhanging perimeter")
        self.assertEqual((rc, j["verdict"]), (2, "FAIL"), out[-400:])
        self.assertAlmostEqual(j["radius_mm"], 0.6)
        self.assertTrue(j["support_on"])

    def test_supported_lip_is_ok(self):
        rc, j, out = self.run_tool(self.write("lip_sup", header() + interface(OX, OX + 20) + lip()))
        vis = [g for g in j["regions"] if g["visible_candidate"]]
        self.assertEqual(len(vis), 1, vis)
        self.assertGreaterEqual(vis[0]["supported_pct"], 90)
        self.assertEqual((rc, j["verdict"]), (0, "OK"), j["findings"])

    def test_filter_on_covered_lip_warns(self):
        rc, j, _ = self.run_tool(self.write("lip_crit", header(crit=1) + interface(OX, OX + 20) + lip()))
        self.assertEqual(j["filters"], {"support_critical_regions_only": True, "support_remove_small_overhang": False})
        self.assertEqual((rc, j["verdict"]), (1, "WARN"), j["findings"])

    def test_filter_on_bare_lip_fail_names_the_filter(self):
        rc, j, _ = self.run_tool(self.write("lip_rso", header(rso=1) + lip()))
        self.assertEqual(rc, 2)
        msg = [x["msg"] for x in j["findings"] if x["level"] == "FAIL"][0]
        self.assertIn("L1043-1045", msg)
        self.assertIn("filter does not guarantee", msg)

    def test_support_off_is_information_only(self):
        rc, j, _ = self.run_tool(self.write("lip_off", header(support=0) + lip()))
        self.assertFalse(j["support_on"])
        self.assertTrue(all(x["level"] == "OK" for x in j["findings"]), j["findings"])
        self.assertEqual(rc, 0)

    def test_one_bare_side_fails_on_the_sector_rule(self):
        lines = header() + ["; Z_HEIGHT: 4.8", "; LAYER_HEIGHT: 0.2", "; FEATURE:Support interface"]
        lines += [f"G1 X{OX + 8} Y{OY + y} Z4.8 E0\nG1 X{OX + 100} Y{OY + y} E9" for y in (1.0, 1.5, 2.0)]
        lines += lip(100.0)
        rc, j, _ = self.run_tool(self.write("lip_end", lines), "--center", f"{OX + 50},{OY + 10}")
        vis = [r for r in j["regions"] if r["visible_candidate"]]
        self.assertEqual(len(vis), 1, vis)
        self.assertTrue(90 <= vis[0]["supported_pct"] < 95, vis[0]["supported_pct"])
        ws = vis[0]["worst_sector"]
        self.assertEqual(ws["sector"], "left")
        self.assertLess(ws["supported_pct"], 90)
        self.assertGreaterEqual(ws["mm"], 10)
        self.assertEqual((rc, j["verdict"]), (2, "FAIL"))
        self.assertIn("(one side of it)", j["findings"][0]["msg"])
        self.assertIn("left sector slice", j["findings"][0]["msg"])

    def test_roof_span_over_walls_fails_and_over_infill_is_excluded(self):
        roof = header() + ["; Z_HEIGHT: 5.0", "; LAYER_HEIGHT: 0.2"] + ring(5.0, "Outer wall") + ["; Z_HEIGHT: 5.2", "; LAYER_HEIGHT: 0.2"]
        roof += ring(5.2, "Outer wall") + bridge_lines()
        rc, j, _ = self.run_tool(self.write("roof", roof))
        vis = [r for r in j["regions"] if r["visible_candidate"]]
        self.assertEqual(len(vis), 1, vis)
        self.assertEqual(vis[0]["kind"], "roof span")
        self.assertEqual(vis[0]["supported_pct"], 0.0)
        self.assertGreater(vis[0]["depth_max"], 9)
        self.assertEqual(j["enclosed_region_samples_excluded"], 0)
        self.assertEqual((rc, j["verdict"]), (2, "FAIL"))
        self.assertIn("roof span", j["findings"][0]["msg"])
        infill = header() + ["; Z_HEIGHT: 5.0", "; LAYER_HEIGHT: 0.2"] + ring(5.0, "Outer wall") + ["; FEATURE:Sparse infill"]
        infill += [f"G1 X{OX + x} Y{OY + 1} E0\nG1 X{OX + x} Y{OY + 19} E2" for x in (3, 7, 11, 15, 19)]
        infill += ["; Z_HEIGHT: 5.2", "; LAYER_HEIGHT: 0.2"] + ring(5.2, "Outer wall") + bridge_lines()
        rc2, j2, _ = self.run_tool(self.write("over_infill", infill))
        self.assertFalse([r for r in j2["regions"] if r["visible_candidate"]], j2["regions"][:2])
        self.assertGreater(j2["internal_bridge_samples_excluded"], 500)
        self.assertEqual(rc2, 0)

    def test_reads_plate_gcode_inside_a_3mf(self):
        p = os.path.join(self.tmp, "sliced.3mf")
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("Metadata/plate_1.gcode", "\n".join(header() + lip()) + "\n")
        rc, j, out = self.run_tool("--3mf", p, "--plate", "1")
        self.assertEqual((rc, j["verdict"]), (2, "FAIL"), out[-300:])

    def test_usage_exit_3(self):
        rc, _, _ = self.run_tool(os.path.join(self.tmp, "no_such.gcode"), json_out=False)
        self.assertEqual(rc, 3)
        g = self.write("u", header() + lip())
        rc, _, _ = self.run_tool(g, "--z", "bad", json_out=False)
        self.assertEqual(rc, 3)
        three = os.path.join(self.tmp, "u.3mf")
        with zipfile.ZipFile(three, "w") as z:
            z.writestr("Metadata/plate_1.gcode", "\n".join(header() + lip()) + "\n")
        rc, _, out = self.run_tool(g, "--3mf", three, "--plate", "1", json_out=False)
        self.assertEqual(rc, 3)
        self.assertIn("ONE input", out)
        rc, _, out = self.run_tool(g, "--json", os.path.join(self.tmp, "no_such_dir", "x.json"), json_out=False)
        self.assertEqual(rc, 3)
        self.assertIn("cannot write --json", out)


if __name__ == "__main__":
    unittest.main()
