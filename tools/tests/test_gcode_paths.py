r"""test_gcode_paths.py - unit tests for tools\gcode_paths.py (G-code to extrusion paths, G2/G3 arcs interpolated).

Synthetic G-code with known geometry only: arcs of known centre and radius (I/J and R forms, G2 and G3, full circles),
a G1-only square, M82/M83 extrusion modes, G91 relative moves, WIPE blocks and the "chord" / "ignore" reader modes.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_gcode_paths.py" -v
"""
from __future__ import annotations

import math
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gcode_paths as gp  # noqa: E402

HEAD = "M83\nG90\n; CHANGE_LAYER\n; Z_HEIGHT: 0.2\n; LAYER_HEIGHT: 0.2\n"


def paths_of(text: str, **kw):
    p = gp.parse(text.splitlines(keepends=True), **kw)
    return p, [q for L in p.layers for q in L.paths]


class GcodePathsTest(unittest.TestCase):
    def check_arc_path(self, q, cx, cy, r, sweep_abs):
        """exact length = r*|sweep|; chord polyline within 0.1 %; every point on the circle; sagitta <= 0.02 mm."""
        analytic = r * sweep_abs
        self.assertLessEqual(abs(q.length - analytic), 1e-6 * max(1.0, analytic))
        self.assertLessEqual(abs(q.chord_length - analytic) / analytic, 0.001)
        for (x, y) in q.pts:
            self.assertLessEqual(abs(math.hypot(x - cx, y - cy) - r), 1e-6)
        for (ax, ay), (bx, by) in zip(q.pts, q.pts[1:]):
            self.assertLessEqual(r - math.hypot((ax + bx) / 2 - cx, (ay + by) / 2 - cy), 0.02 + 1e-9)

    def test_quarter_arc_g3_ij_known_length(self):
        _, qs = paths_of(HEAD + "; FEATURE: Outer wall\nG1 X110 Y100 F600\nG3 X100 Y110 I-10 J0 E1\n")
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0].n_arcs, 1)
        self.assertEqual(qs[0].feature, "Outer wall")
        self.check_arc_path(qs[0], 100, 100, 10, math.pi / 2)
        self.assertEqual(qs[0].pts[0], (110.0, 100.0))
        self.assertEqual(qs[0].pts[-1], (100.0, 110.0))

    def test_arc_radii_and_directions(self):
        for r in (0.3, 5.0, 1400.0):
            for deg in (30.0, 90.0, 200.0, 359.0):
                for cw in (True, False):
                    a1 = math.radians(-deg if cw else deg)
                    sx, sy = 150.0 + r, 150.0
                    ex, ey = 150.0 + r * math.cos(a1), 150.0 + r * math.sin(a1)
                    g = HEAD + f"; FEATURE: Inner wall\nG1 X{sx:.9f} Y{sy:.9f}\n{'G2' if cw else 'G3'} X{ex:.9f} Y{ey:.9f} I{-r:.9f} J0 E1\n"
                    _, qs = paths_of(g)
                    self.assertEqual(len(qs), 1)
                    self.check_arc_path(qs[0], 150.0, 150.0, r, math.radians(deg))
                    mid = qs[0].pts[len(qs[0].pts) // 2]
                    ang = math.degrees(math.atan2(mid[1] - 150.0, mid[0] - 150.0))
                    if deg <= 180:
                        self.assertEqual(ang < 0, cw, (r, deg, cw, ang))

    def test_full_circles(self):
        g = HEAD + "; FEATURE: Outer wall\nG1 X105 Y100\nG3 I-5 J0 E2\n; FEATURE: Inner wall\nG1 X120 Y100\nG2 X120 Y100 I-3 J0 E1\n"
        _, qs = paths_of(g)
        self.assertEqual([q.feature for q in qs], ["Outer wall", "Inner wall"])
        self.check_arc_path(qs[0], 100, 100, 5, 2 * math.pi)
        self.check_arc_path(qs[1], 117, 100, 3, 2 * math.pi)
        self.assertTrue(qs[0].closed(1e-9) and qs[1].closed(1e-9))

    def test_r_form_short_and_long_arc(self):
        cx, cy, rad, _, sw = gp.arc_geometry(0, 10, 10, 0, True, r=10)
        self.assertAlmostEqual(cx, 0, places=9)
        self.assertAlmostEqual(cy, 0, places=9)
        self.assertAlmostEqual(sw, -math.pi / 2, places=9)
        cx, cy, _, _, sw = gp.arc_geometry(0, 10, 10, 0, True, r=-10)
        self.assertAlmostEqual(cx, 10, places=9)
        self.assertAlmostEqual(sw, -1.5 * math.pi, places=9)
        cx, cy, _, _, sw = gp.arc_geometry(0, 10, 10, 0, False, r=10)
        self.assertAlmostEqual(cy, 10, places=9)
        self.assertAlmostEqual(sw, math.pi / 2, places=9)
        p, qs = paths_of(HEAD + "; FEATURE: Outer wall\nG1 X100 Y110\nG2 X110 Y100 R-10 E1\n")
        self.check_arc_path(qs[0], 110, 110, 10, 1.5 * math.pi)
        self.assertEqual(p.stats.get("arcs_r_form"), 1)

    def test_arc_without_ij_or_r_raises(self):
        with self.assertRaises(ValueError):
            gp.arc_geometry(0, 0, 10, 0, True)

    def test_g1_only_square_all_modes(self):
        g = HEAD + "; FEATURE: Outer wall\nG1 X100 Y100 F600\nG1 X120 Y100 E1\nG1 X120 Y120 E1\nG1 X100 Y120 E1\nG1 X100 Y100 E1\n"
        for mode in ("interpolate", "chord", "ignore"):
            p, qs = paths_of(g, arcs=mode)
            self.assertEqual(len(qs), 1, mode)
            self.assertEqual(len(qs[0].pts), 5)
            self.assertEqual(qs[0].n_arcs, 0)
            self.assertAlmostEqual(qs[0].length, 80.0, places=12)
            self.assertTrue(qs[0].closed(1e-9))

    def test_m83_relative_and_m82_absolute_e(self):
        body = ("; FEATURE: Outer wall\nG1 X100 Y100\nG1 X110 Y100 E.5\nG1 X120 Y100 E.5\n"
                "G1 X125 Y100 E-.8\nG1 E.8\nG1 X135 Y100 E.5\n")
        _, qs = paths_of(HEAD + body)
        self.assertEqual([len(q.pts) for q in qs], [3, 2])
        self.assertEqual(qs[1].pts, [(125.0, 100.0), (135.0, 100.0)])
        _, qs82 = paths_of(HEAD.replace("M83", "M82") + "G92 E0\n" + body)
        self.assertEqual([q.pts for q in qs82], [[(100.0, 100.0), (110.0, 100.0)]])

    def test_m82_with_g92_reset(self):
        g = HEAD.replace("M83", "M82") + "G92 E0\n; FEATURE: Outer wall\nG1 X100 Y100\nG1 X110 Y100 E1\nG1 X120 Y100 E2\nG92 E0\nG1 X130 Y100 E1\n"
        p, qs = paths_of(g)
        self.assertEqual(len(qs), 1)
        self.assertAlmostEqual(qs[0].length, 30.0, places=12)
        self.assertEqual(p.stats.get("m82"), 1)
        self.assertEqual(p.stats.get("g92"), 2)

    def test_g91_relative_xy(self):
        _, qs = paths_of(HEAD + "; FEATURE: Outer wall\nG1 X100 Y100\nG91\nG1 X10 E1\nG1 Y10 E1\nG90\nG1 X100 Y110 E1\n")
        self.assertEqual(qs[0].pts, [(100.0, 100.0), (110.0, 100.0), (110.0, 110.0), (100.0, 110.0)])

    def test_wipe_feature_and_layer_breaks(self):
        g = (HEAD + "; FEATURE: Outer wall\nG1 X100 Y100\nG1 X110 Y100 E1\n; WIPE_START\nG1 X115 Y100 E.2\n; WIPE_END\n"
             "G1 X100 Y100\nG1 X100 Y110 E1\n; FEATURE: Gap infill\nG1 X100 Y120 E1\n; CHANGE_LAYER\n; Z_HEIGHT: 0.4\nG1 X100 Y130 E1\n")
        p, qs = paths_of(g)
        self.assertEqual([(q.feature, q.z, len(q.pts)) for q in qs],
                         [("Outer wall", 0.2, 2), ("Outer wall", 0.2, 2), ("Gap infill", 0.2, 2), ("Gap infill", 0.4, 2)])
        self.assertEqual([L.z for L in p.layers], [0.2, 0.4])

    def test_chord_and_ignore_modes(self):
        g = HEAD + "; FEATURE: Outer wall\nG1 X100 Y100\nG1 X120 Y100 E1\nG3 X120 Y110 I0 J5 E1\nG1 X100 Y110 E1\nG3 X100 Y100 I0 J-5 E1\n"
        _, qi = paths_of(g)
        self.assertEqual(len(qi), 1)
        self.assertTrue(qi[0].closed(1e-9))
        self.assertAlmostEqual(qi[0].length, 40 + 2 * math.pi * 5, places=9)
        _, qc = paths_of(g, arcs="chord")
        self.assertAlmostEqual(qc[0].length, 60.0, places=9)
        p, qg = paths_of(g, arcs="ignore")
        self.assertEqual(p.stats.get("arcs_skipped"), 2)
        self.assertAlmostEqual(sum(q.length for q in qg), 20 + math.sqrt(500), places=9)

    def test_object_labels_and_header(self):
        g = ("; filament_map = 2,2\n" + HEAD + "; start printing object, unique label id: 7\n; FEATURE: Outer wall\n"
             "G1 X0 Y0\nG1 X10 Y0 E1\n; stop printing object, unique label id: 7\nT1\n; FEATURE: Outer wall\nG1 X20 Y0 E1\n")
        p, qs = paths_of(g)
        self.assertEqual(p.header.get("filament_map"), "2,2")
        self.assertEqual(qs[0].label_id, 7)
        self.assertIsNone(qs[1].label_id)
        self.assertEqual(qs[1].tool, 1)

    def test_read_lines_from_3mf(self):
        g = HEAD + "; FEATURE: Outer wall\nG1 X0 Y0\nG1 X10 Y0 E1\n"
        with tempfile.TemporaryDirectory() as td:
            p3 = os.path.join(td, "sliced.3mf")
            with zipfile.ZipFile(p3, "w") as z:
                z.writestr("Metadata/plate_2.gcode", g)
            p = gp.parse(p3, plate=2)
        self.assertEqual(sum(len(L.paths) for L in p.layers), 1)

    def test_bad_mode_raises(self):
        with self.assertRaises(ValueError):
            gp.parse([], arcs="spline")


if __name__ == "__main__":
    unittest.main()
