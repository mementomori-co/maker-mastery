r"""test_visible_ratio.py - unit tests of tools\visible_ratio.py with synthetic G-code written to a temp folder.

Part = a square tube (Outer wall) x 100..125, y 80..105, z 0..8 (0.4 mm layers); the viewer stands at -Y.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p test_visible_ratio.py -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zlib

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)

try:
    import numpy as np
    import visible_ratio as vr
    HAVE = True
    WHY = ""
except ImportError as e:  # pragma: no cover
    HAVE, WHY = False, f"visible_ratio needs numpy: {e}"

STEP = 0.4
X0, X1, Y0, Y1 = 100.0, 125.0, 80.0, 105.0


def gcode(part_top=8.0, wall_y=None, wall_top=0.0, wall_from=0.0, circle=False):
    out = ["M83", "G90"]
    n = int(round(max(part_top, wall_top) / STEP))
    for i in range(1, n + 1):
        z = round(i * STEP, 3)
        out += ["; CHANGE_LAYER", f"; Z_HEIGHT: {z}", f"; LAYER_HEIGHT: {STEP}", f"G1 Z{z} F600"]
        if z <= part_top + 1e-9:
            out += ["; FEATURE: Outer wall", "; LINE_WIDTH: 0.42"]
            if circle:
                out += [f"G1 X{X0} Y{Y0 + 12} F3000", f"G2 X{X0} Y{Y0 + 12} I12 J0 E1.5"]
            else:
                out += [f"G1 X{X0} Y{Y0} F3000", f"G1 X{X1} Y{Y0} E1", f"G1 X{X1} Y{Y1} E1", f"G1 X{X0} Y{Y1} E1", f"G1 X{X0} Y{Y0} E1"]
        if wall_y is not None and wall_from < z <= wall_top + 1e-9:
            out += ["; FEATURE: Support", "; LINE_WIDTH: 0.42"]
            for dy in (0.0, 0.45, 0.9):
                out += [f"G1 X60 Y{wall_y + dy} F3000", f"G1 X170 Y{wall_y + dy} E1"]
    return "\n".join(out) + "\n"


def png_pixels(path):
    with open(path, "rb") as fh:
        d = fh.read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, w, h = 8, b"", 0, 0
    while pos < len(d):
        ln = int.from_bytes(d[pos:pos + 4], "big")
        tag, body = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + ln]
        if tag == b"IHDR":
            w, h = int.from_bytes(body[:4], "big"), int.from_bytes(body[4:8], "big")
        elif tag == b"IDAT":
            idat += body
        pos += 12 + ln
    raw = zlib.decompress(idat)
    return np.stack([np.frombuffer(raw[r * (w * 3 + 1) + 1:(r + 1) * (w * 3 + 1)], dtype=np.uint8).reshape(w, 3) for r in range(h)])


@unittest.skipUnless(HAVE, WHY)
class VisibleRatioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="mm_visible_ratio_")

    def write(self, name, text):
        p = os.path.join(self.tmp, name + ".gcode")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return p

    def analyse(self, name, text, **kw):
        return vr.analyse(self.write(name, text), **kw)

    def cli(self, args):
        p = subprocess.run([sys.executable, "-I", "-B", os.path.join(TOOLS, "visible_ratio.py")] + args,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        return p.returncode, (p.stdout or "") + (p.stderr or "")

    @staticmethod
    def final(res, view):
        return res["views"][view]["final_visible_ratio"]

    def test_tall_wall_in_front_hides_part(self):
        res = self.analyse("wall", gcode(8.0, 70.0, 40.0))
        self.assertLess(self.final(res, "front"), 0.05)
        self.assertLess(self.final(res, "iso"), 0.10)

    def test_no_support_is_fully_visible(self):
        res = self.analyse("nosup", gcode(8.0))
        self.assertEqual(self.final(res, "front"), 1.0)
        self.assertEqual(self.final(res, "iso"), 1.0)
        self.assertGreater(res["views"]["front"]["checkpoints"][-1]["part_px"], 3000)

    def test_wall_behind_part_hides_nothing(self):
        res = self.analyse("behind", gcode(8.0, 130.0, 30.0))
        self.assertGreaterEqual(self.final(res, "front"), 0.99)

    def test_low_wall_ratio_grows_with_height(self):
        res = self.analyse("low", gcode(8.0, 50.0, 4.0), views=("front",))
        cp = res["views"]["front"]["checkpoints"]
        self.assertEqual([c["fraction"] for c in cp], [0.25, 0.5, 0.75, 1.0])
        got = [c["visible_ratio"] for c in cp]
        self.assertLess(got[0], 0.05)                       # below the wall top: all hidden
        self.assertEqual(got, sorted(got))                  # cumulative stack: never decreases
        self.assertAlmostEqual(got[-1], 0.5, delta=0.06)    # wall covers z 0..4 of an 8 mm part

    def test_face_masks(self):
        mp = os.path.join(self.tmp, "mask.json")
        with open(mp, "w", encoding="utf-8") as fh:
            json.dump({"masks": [
                {"name": "upper", "box": {"min": [X0 - 1, Y0 - 1, 4.5], "max": [X1 + 1, Y1 + 1, 8.1]}},
                {"name": "lower", "box": {"min": [X0 - 1, Y0 - 1, 0.0], "max": [X1 + 1, Y1 + 1, 3.9]}},
                {"name": "poly-upper", "view": "front", "polygon": [[X0 - 2, 4.8], [X1 + 2, 4.8], [X1 + 2, 9], [X0 - 2, 9]]},
                {"name": "off-part", "box": {"min": [0, 0, 0], "max": [5, 5, 5]}},
            ]}, fh)
        res = self.analyse("low2", gcode(8.0, 50.0, 4.0), views=("front",), masks=vr.load_masks(mp))
        f = {x["name"]: x for x in res["views"]["front"]["face"]}
        self.assertGreaterEqual(f["upper"]["visible_ratio"], 0.97)
        self.assertLessEqual(f["lower"]["visible_ratio"], 0.03)
        self.assertGreaterEqual(f["poly-upper"]["visible_ratio"], 0.95)
        self.assertIsNone(f["off-part"]["visible_ratio"])
        self.assertEqual(f["off-part"]["face_px"], 0)
        v, reasons = vr.verdict_of(res, 0.6, 0.8, 0.6, 0.8)
        self.assertEqual(v, "FAIL")
        self.assertTrue(any("'lower'" in r for r in reasons), reasons)

    def test_full_circle_arc_is_read(self):
        res = self.analyse("circle", gcode(8.0, circle=True), views=("front",))
        px = res["views"]["front"]["checkpoints"][-1]["part_px"]
        want = 24.4 * 7.8 * 25     # diameter 24 + line width, z 0.2..8 at 5 px/mm
        self.assertLess(abs(px - want) / want, 0.12, px)
        self.assertEqual(res["gcode_paths_stats"].get("extruding_arcs", 0), 20)

    def test_cumulative_stack_late_wall(self):
        res = self.analyse("late", gcode(8.0, 50.0, 24.0, wall_from=6.0), views=("front",))
        cp = res["views"]["front"]["checkpoints"]
        self.assertEqual(cp[0]["visible_ratio"], 1.0)       # 25 % of z 24 = 6.0: no wall yet
        self.assertGreater(cp[-1]["visible_ratio"], 0.6)
        self.assertLess(cp[-1]["visible_ratio"], 0.85)      # the wall hides the part above about z 6

    def test_cli_exit_codes_and_json(self):
        wall = self.write("cwall", gcode(8.0, 70.0, 40.0))
        low = self.write("clow", gcode(8.0, 50.0, 4.0))
        nosup = self.write("cnosup", gcode(8.0))
        o = lambda n: ["--out-prefix", os.path.join(self.tmp, "cli_" + n), "--views", "front"]  # noqa: E731
        rc, out = self.cli([wall] + o("wall"))
        self.assertEqual(rc, 2, out[-300:])
        self.assertIn("verdict: FAIL", out)
        rc, out = self.cli([low] + o("low") + ["--fail", "0.3", "--warn", "0.6"])
        self.assertEqual(rc, 1, out[-300:])
        rc, out = self.cli([nosup] + o("nosup"))
        self.assertEqual(rc, 0, out[-300:])
        rc, _ = self.cli([os.path.join(self.tmp, "missing.gcode")] + o("missing"))
        self.assertEqual(rc, 3)
        rc, _ = self.cli([nosup, "--fail", "0.9", "--warn", "0.5"] + o("bad"))
        self.assertEqual(rc, 3)
        with open(os.path.join(self.tmp, "cli_wall.json"), encoding="utf-8") as fh:
            j = json.load(fh)
        self.assertEqual(j["verdict"], "FAIL")
        self.assertEqual(j["thresholds"]["fail"], 0.6)
        self.assertIn("limits", j)

    def test_png_colours(self):
        for name, text, hidden in (("pwall", gcode(8.0, 70.0, 40.0), True), ("pnosup", gcode(8.0), False)):
            g = self.write(name, text)
            rc, out = self.cli([g, "--out-prefix", os.path.join(self.tmp, "png_" + name)])
            self.assertIn(rc, (0, 2), out[-300:])
            for view in ("front", "iso"):
                img = png_pixels(os.path.join(self.tmp, f"png_{name}-{view}.png"))
                blue = int(np.all(img == (30, 80, 230), axis=2).sum())
                red = int(np.all(img == (220, 40, 40), axis=2).sum())
                self.assertEqual(blue > 500, hidden, (name, view, blue))
                self.assertEqual(red > 500, hidden, (name, view, red))


if __name__ == "__main__":
    unittest.main()
