r"""test_tower.py - unit tests for tools\tower_bounds.py, tools\tower_clearance.py and tools\mcp\tower_clearance_3mf.py.

Synthetic plate G-code: a 20 x 20 prime tower whose first layer carries a 5 mm brim, and one labelled object placed at a
chosen distance from it. A sliced 3MF is a zip built by the test that holds only Metadata/plate_1.gcode.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_tower.py" -v
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
import tower_bounds as tb  # noqa: E402

try:
    import shapely  # noqa: F401
    import tower_clearance as tc
    MISSING = None
except ImportError as e:   # pragma: no cover
    MISSING = f"optional dependency missing ({e}); install requirements.txt into .venv"


def square(x0, y0, x1, y1):
    return [f"G1 X{x0} Y{y0} E0", f"G1 X{x1} Y{y0} E1", f"G1 X{x1} Y{y1} E1", f"G1 X{x0} Y{y1} E1", f"G1 X{x0} Y{y0} E1"]


def plate(obj_x0: float, with_tower: bool = True, labelled: bool = True) -> str:
    """tower body x 200..220, y 200..220; first-layer brim 195..225; object a 20 x 20 square starting at obj_x0, y 200..220."""
    L = ["; HEADER", "M83", "; FEATURE: Custom", "G1 X0 Y0 E0", "G1 X100 Y0 E5"]   # start purge line: excluded
    for z in (0.2, 0.4, 0.6):
        L.append(f"; Z_HEIGHT: {z}")
        if labelled:
            L.append("; start printing object, unique label id: 3")
        L += ["; FEATURE: Outer wall"] + square(obj_x0, 200, obj_x0 + 20, 220)
        if labelled:
            L.append("; stop printing object, unique label id: 3")
        if with_tower:
            L += ["; FEATURE: Prime tower"] + square(200, 200, 220, 220)
            if z == 0.2:
                L += square(195, 195, 225, 225)
    return "\n".join(L) + "\n"


class TowerBoundsTest(unittest.TestCase):
    def test_bounds_body_and_first_layer(self):
        with tempfile.TemporaryDirectory() as td:
            g = os.path.join(td, "plate_1.gcode")
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(plate(100))
            r = tb.measure(g, 0.25)
        self.assertTrue(r["prime_tower"])
        self.assertEqual(r["layers_with_tower"], 3)
        self.assertEqual((r["first_layer"]["xmin"], r["first_layer"]["xmax"]), (195.0, 225.0))
        self.assertEqual(r["first_layer"]["width"], 30.0)
        self.assertGreaterEqual(r["all_layers"]["xmin"], 195.0)

    def test_no_tower(self):
        with tempfile.TemporaryDirectory() as td:
            g = os.path.join(td, "plate_1.gcode")
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(plate(100, with_tower=False))
            self.assertEqual(tb.measure(g, 0.25), {"file": g, "prime_tower": False})


@unittest.skipIf(MISSING, MISSING or "")
class TowerClearanceTest(unittest.TestCase):
    def check(self, obj_x0, **kw):
        with tempfile.TemporaryDirectory() as td:
            g = os.path.join(td, "plate_1.gcode")
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(plate(obj_x0, **kw))
            return tc.check(g, 8.0, 0.25)

    def test_far_object_ok(self):
        r = self.check(100)            # object x 100..120; the all-layer tower hull includes the brim (x 195): gap 75 mm
        self.assertEqual(r["verdict"], "OK")
        self.assertEqual(r["objects"][0]["object_label"], "3")
        self.assertAlmostEqual(r["objects"][0]["gap_to_tower_body_mm"], 75.0, places=6)

    def test_close_object_warns(self):
        r = self.check(176)            # object x 176..196 overlaps the brim at x 195..196 -> FAIL
        self.assertEqual(r["verdict"], "FAIL")
        r2 = self.check(174)           # object x 174..194: 1 mm from the brim, under the 8 mm rule -> WARN
        self.assertEqual(r2["verdict"], "WARN")
        self.assertAlmostEqual(r2["objects"][0]["gap_to_tower_first_layer_mm"], 1.0, places=6)
        self.assertFalse(r2["objects"][0]["intersects_first_layer"])

    def test_untagged_single_object_and_no_tower(self):
        r = self.check(100, labelled=False)
        self.assertEqual(r["objects"][0]["object_label"], "untagged")
        r2 = self.check(100, with_tower=False)
        self.assertEqual((r2["prime_tower"], r2["verdict"]), (False, "OK"))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            g = os.path.join(td, "plate_1.gcode")
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(plate(174))
            p = subprocess.run([sys.executable, "-I", "-B", os.path.join(TOOLS, "tower_clearance.py"), g, "--json"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)[0]["verdict"], "WARN")

    def test_3mf_helper_reads_in_memory(self):
        helper = os.path.join(TOOLS, "mcp", "tower_clearance_3mf.py")
        with tempfile.TemporaryDirectory() as td:
            p3 = os.path.join(td, "sliced.3mf")
            with zipfile.ZipFile(p3, "w") as z:
                z.writestr("Metadata/plate_1.gcode", plate(176))
                z.writestr("Metadata/plate_2.gcode", plate(100))
            before = sorted(os.listdir(td))
            p = subprocess.run([sys.executable, "-I", "-B", helper, p3], capture_output=True, text=True, encoding="utf-8", errors="replace")
            after = sorted(os.listdir(td))
            empty = os.path.join(td, "unsliced.3mf")
            with zipfile.ZipFile(empty, "w") as z:
                z.writestr("Metadata/project_settings.config", "{}")
            p4 = subprocess.run([sys.executable, "-I", "-B", helper, empty], capture_output=True, text=True, encoding="utf-8", errors="replace")
            bad = os.path.join(td, "bad.3mf")
            with open(bad, "w", encoding="utf-8") as fh:
                fh.write("not a zip")
            p5 = subprocess.run([sys.executable, "-I", "-B", helper, bad], capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(p.returncode, 2, p.stderr)
        data = json.loads(p.stdout)
        self.assertEqual([d["verdict"] for d in data], ["FAIL", "OK"])
        self.assertTrue(data[0]["file"].endswith("!Metadata/plate_1.gcode"))
        self.assertEqual(before, after)          # nothing extracted
        self.assertEqual(p4.returncode, 4)
        self.assertEqual(p5.returncode, 5)


if __name__ == "__main__":
    unittest.main()
