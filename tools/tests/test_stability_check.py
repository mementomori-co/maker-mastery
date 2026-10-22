r"""test_stability_check.py - unit tests for tools\stability_check.py on synthetic solids and a hand-written G-code.

Cases (meshes generated here with trimesh; nothing printed or sent; the Blender render is never invoked):
  box 20 x 20 x 100: tip angle atan(10/50) = 11.31 deg -> WARN; hull = contact = 400 mm2; top-heavy 5.0; knock force;
      uniform-density WARN; exit 1. With --mass the density WARN goes and the knock force scales with the mass.
  tipping L (a cantilever arm whose CoM lies outside the foot): FAIL, exit 2.
  plate on four small feet: contact 4 % of the hull -> contact WARN.
  two parts with --place: an assembly block is reported.
  box tilted 2 deg, --level: the tilt is recovered and the tip angle returns to 11.31 deg.
  gcode_grams on a hand-written G-code with G2/G3 arcs: Outer wall 3.0 mm, Support 3.5 mm, Brim 0.25 mm of E; a retract
      without XY and an "E" inside a comment are not counted.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_stability_check.py" -v
"""
from __future__ import annotations

import contextlib
import io
import json
import math
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import numpy as np
    import shapely  # noqa: F401
    import trimesh
    import stability_check as sc
    MISSING = None
except ImportError as e:   # pragma: no cover
    MISSING = f"optional dependency missing ({e}); install requirements.txt into .venv"

G = 9.81
G_PER_MM = math.pi * (1.75 / 2) ** 2 * 1.24 / 1000.0

ARC_GCODE = """; filament_diameter = 1.75
; filament_density = 1.24
M83
; FEATURE: Outer wall
G1 X10 Y10 F600
G1 X20 Y10 E1
G3 X30 Y10 I5 J0 E2
G1 E-1
G1 E1
; a comment that mentions E9 and X5 is not a move
; FEATURE: Support
G1 X50 Y50
G2 X60 Y50 I5 J0 E3
G3 I5 J0 E.5
G3 Z.6 I1 J0 P1
; FEATURE: Brim
G0 X70 Y50 E.25
"""


def box(size, centre):
    b = trimesh.creation.box(size)
    b.apply_translation(centre)
    return b


@unittest.skipIf(MISSING, MISSING or "")
class StabilityCheckTest(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.td.cleanup()

    def p(self, name):
        return os.path.join(self.td.name, name)

    def run_tool(self, *args):
        js = self.p("r.json")
        with contextlib.redirect_stdout(io.StringIO()):
            rc = sc.main([*args, "--json", js])
        with open(js, encoding="utf-8") as fh:
            return rc, json.load(fh)

    @staticmethod
    def flags(rep, level, needle=""):
        return [m for l, m in rep["flags"] if l == level and needle in m]

    def test_tall_box_tip_angle_and_density_warn(self):
        box([20, 20, 100], [0, 0, 50]).export(self.p("box.stl"))
        rc, rep = self.run_tool(self.p("box.stl"))
        sa = rep["standalone"][0]
        self.assertAlmostEqual(sa["tip_min_exact_deg"], math.degrees(math.atan(10 / 50)), delta=0.02)
        self.assertAlmostEqual(sa["hull_area_mm2"], 400, delta=0.01)
        self.assertAlmostEqual(sa["contact_area_mm2"], 400, delta=0.01)
        self.assertAlmostEqual(sa["top_heavy_index"], 5.0, places=6)
        m = 40000 / 1000 * 1.24
        self.assertAlmostEqual(sa["mass_g"], m, places=6)
        self.assertAlmostEqual(sa["knock_force_N"], m / 1000 * G * 0.010 / 0.100, places=5)
        self.assertEqual(rc, 1)
        self.assertTrue(self.flags(rep, "WARN", "tip angle"))
        self.assertTrue(self.flags(rep, "WARN", "uniform density"))
        self.assertFalse(self.flags(rep, "FAIL"))
        self.assertEqual(rep["result"], "WARN")

    def test_mass_override(self):
        box([20, 20, 100], [0, 0, 50]).export(self.p("box.stl"))
        _rc, rep = self.run_tool(self.p("box.stl"), "--mass", "box=100")
        self.assertAlmostEqual(rep["standalone"][0]["knock_force_N"], 0.1 * G * 0.1, places=5)
        self.assertFalse(self.flags(rep, "WARN", "uniform density"))

    def test_tipping_l_fails(self):
        foot = box([20, 20, 10], [0, 0, 5])
        arm = box([60, 20, 10], [40, 0, 15])   # a long arm on top, sticking out to +X: CoM outside the 20 x 20 foot
        trimesh.util.concatenate([foot, arm]).export(self.p("ell.stl"))
        rc, rep = self.run_tool(self.p("ell.stl"))
        self.assertEqual(rc, 2)
        self.assertFalse(rep["standalone"][0]["com_inside"])
        self.assertTrue(self.flags(rep, "FAIL", "OUTSIDE"))

    def test_small_feet_contact_warn(self):
        parts = [box([40, 40, 10], [0, 0, 6])] + [box([4, 4, 1], [x, y, 0.5]) for x in (-18, 18) for y in (-18, 18)]
        trimesh.util.concatenate(parts).export(self.p("plate.stl"))
        _rc, rep = self.run_tool(self.p("plate.stl"))
        sa = rep["standalone"][0]
        self.assertAlmostEqual(sa["hull_area_mm2"], 1600, delta=0.5)
        self.assertAlmostEqual(sa["contact_area_mm2"], 64, delta=0.5)
        self.assertTrue(self.flags(rep, "WARN", "layer-1 contact"))

    def test_two_parts_placed(self):
        box([40, 40, 5], [0, 0, 2.5]).export(self.p("base.stl"))
        box([10, 10, 60], [0, 0, 30]).export(self.p("post.stl"))
        _rc, rep = self.run_tool(self.p("base.stl"), self.p("post.stl"), "--place", "post=10,0,5")
        asm = rep["assembly"]
        self.assertTrue(asm["com_inside"])
        self.assertGreater(asm["tip_min_exact_deg"], 30.0)
        self.assertEqual(len(rep["standalone"]), 2)

    def test_level_recovers_tilt(self):
        b = box([20, 20, 100], [0, 0, 50])
        b.apply_transform(trimesh.transformations.rotation_matrix(math.radians(2), [1, 0, 0]))
        b.export(self.p("tilt.stl"))
        _rc, rep = self.run_tool(self.p("tilt.stl"), "--level", "tilt")
        sa = rep["standalone"][0]
        self.assertAlmostEqual(sa["level"]["tilt_deg"], 2.0, delta=0.05)
        self.assertAlmostEqual(sa["tip_min_exact_deg"], math.degrees(math.atan(10 / 50)), delta=0.1)

    def test_gcode_grams_counts_arcs(self):
        with open(self.p("arcs.gcode"), "w", encoding="utf-8") as fh:
            fh.write(ARC_GCODE)
        g = sc.gcode_grams(self.p("arcs.gcode"))
        mm = {k: round(v / G_PER_MM, 9) for k, v in g["grams_by_feature"].items()}
        self.assertEqual(mm, {"Outer wall": 3.0, "Support": 3.5, "Brim": 0.25})
        self.assertAlmostEqual(g["removed_g"], 3.75 * G_PER_MM, places=12)
        self.assertAlmostEqual(g["model_g"], 3.0 * G_PER_MM, places=12)
        self.assertTrue(g["relative_e"])

    def test_render_without_blender_is_skipped(self):
        # never launches Blender: with blender_exe empty the render function returns a skip line
        old = sc.BLENDER
        try:
            sc.BLENDER = ""
            lines = sc.render([], {"hull": [[0, 0], [1, 0], [1, 1]]}, self.p("x"))
        finally:
            sc.BLENDER = old
        self.assertTrue(lines and lines[0].startswith("render skipped"))

    def test_missing_file_exits_3(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(sc.main([self.p("nope.stl")]), 3)


if __name__ == "__main__":
    unittest.main()
