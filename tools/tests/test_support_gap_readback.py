r"""test_support_gap_readback.py - unit tests for tools\support_gap_readback.py on hand-written plate G-code.

Fixture: two Support interface layers (z 3.8 and 4.0) under an object wall layer at z 4.4 with LAYER_HEIGHT 0.2, so the last
interface sees the object 0.2 mm above it; the lower interface is "not the last" one. A Support block printed after the
object at LAYER_HEIGHT 0.28 must not change the object layer height. A 3MF built by the test carries the same G-code.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_support_gap_readback.py" -v
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
TOOL = os.path.join(TOOLS, "support_gap_readback.py")

try:
    import numpy  # noqa: F401
    import scipy  # noqa: F401
    import support_gap_readback as sgr
    MISSING = None
except ImportError as e:   # pragma: no cover
    MISSING = f"optional dependency missing ({e}); install requirements.txt into .venv"


def iface(z, lh="0.2"):
    return [f"; Z_HEIGHT: {z}", f"; LAYER_HEIGHT: {lh}", "; LINE_WIDTH: 0.42", "; FEATURE:Support interface",
            f"G1 X0 Y10 Z{z} E0", "G1 X20 Y10 E2", "G1 X0 Y10.2 E0", "G1 X20 Y10.2 E2", "G1 X0 Y10.4 E0", "G1 X20 Y10.4 E2"]


GCODE = "\n".join(
    ["; CONFIG_BLOCK_START", "; support_top_z_distance = 0.2", "; enable_support = 1", "; support_style = tree_hybrid", "; CONFIG_BLOCK_END"]
    + iface(3.8) + iface(4.0, "0.28")
    + ["; Z_HEIGHT: 4.4", "; LAYER_HEIGHT: 0.2", "; start printing object, unique label id: 5", "; FEATURE:Outer wall",
       "G1 X0 Y10 Z4.4 E0", "G1 X20 Y10 E2", "G1 X20 Y10.2 E0.2", "G1 X0 Y10.2 E2", "G1 X0 Y10.4 E0.2", "G1 X20 Y10.4 E2",
       "; stop printing object, unique label id: 5",
       "; LAYER_HEIGHT: 0.28", "; FEATURE:Support", "G1 X40 Y40 E0", "G1 X50 Y40 E1"]) + "\n"

NO_SUPPORT = "; Z_HEIGHT: 0.2\n; LAYER_HEIGHT: 0.2\n; FEATURE:Outer wall\nG1 X0 Y0 Z0.2 E0\nG1 X20 Y0 E1\n"

MODEL_SETTINGS = """<?xml version="1.0" encoding="UTF-8"?>
<config><object id="1"><metadata key="name" value="bracket"/><metadata key="support_top_z_distance" value="0.12"/></object></config>"""
SLICE_INFO = """<?xml version="1.0" encoding="UTF-8"?>
<config><plate><metadata key="index" value="1"/><object identify_id="5" name="bracket" skipped="false"/></plate></config>"""


def run(*args):
    with tempfile.TemporaryDirectory() as td:
        js = os.path.join(td, "r.json")
        p = subprocess.run([sys.executable, "-I", "-B", TOOL, *args, "--json", js], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        data = {}
        if os.path.exists(js):
            with open(js, encoding="utf-8") as fh:
                data = json.load(fh)
    return p.returncode, data


@unittest.skipIf(MISSING, MISSING or "")
class SupportGapReadbackTest(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.g = os.path.join(self.td.name, "plate_1.gcode")
        with open(self.g, "w", encoding="utf-8") as fh:
            fh.write(GCODE)

    def tearDown(self):
        self.td.cleanup()

    def test_predicted_gaps_stacking_rule(self):
        self.assertEqual(sgr.predicted_gaps(0.2, 0.12), {"stacked": 0.24, "exact": 0.2, "n_layers": 2})
        self.assertEqual(sgr.predicted_gaps(0.2, 0.2), {"stacked": 0.2, "exact": 0.2, "n_layers": 1})
        self.assertEqual(sgr.predicted_gaps(0.2, None)["stacked"], None)

    def test_mode_equals_typed_top_z(self):
        rc, j = run(self.g)
        self.assertEqual(rc, 0, j.get("findings"))
        self.assertEqual(j["typed_top_z"], 0.2)
        self.assertEqual(j["object_layer_heights"], [0.2])            # the Support block's 0.28 is not the object layer height
        self.assertEqual(j["by_layer_height"]["0.2"]["mode"], 0.2)
        self.assertGreater(j["not_last_interface"], 0)                  # the z 3.8 interface lies under the z 4.0 one
        self.assertEqual(j["by_object"]["5"]["mode"], 0.2)

    def test_typed_value_differs_warns(self):
        rc, j = run(self.g, "--top-z", "0.12")
        self.assertEqual(rc, 1)
        self.assertTrue(any(f["level"] == "WARN" and "printed Top Z mode 0.2" in f["msg"] for f in j["findings"]))

    def test_3mf_plate_and_per_object_override(self):
        p3 = os.path.join(self.td.name, "sliced.3mf")
        with zipfile.ZipFile(p3, "w") as z:
            z.writestr("Metadata/plate_1.gcode", GCODE)
            z.writestr("Metadata/model_settings.config", MODEL_SETTINGS)
            z.writestr("Metadata/slice_info.config", SLICE_INFO)
        rc, j = run("--3mf", p3, "--plate", "1")
        self.assertEqual(j["by_object"]["5"]["name"], "bracket")
        self.assertEqual(j["by_object"]["5"]["typed_top_z"], 0.12)    # the object override beats the header's 0.2
        self.assertEqual(rc, 1)

    def test_no_interface_plate(self):
        g = os.path.join(self.td.name, "plain.gcode")
        with open(g, "w", encoding="utf-8") as fh:
            fh.write(NO_SUPPORT)
        rc, j = run(g)
        self.assertEqual(rc, 0)
        self.assertEqual(j["n_interface_samples"], 0)
        self.assertTrue(j["findings"][0]["msg"].startswith("no Support interface"))

    def test_usage_errors_exit_3(self):
        self.assertEqual(run(os.path.join(self.td.name, "missing.gcode"))[0], 3)
        self.assertEqual(run(self.g, "--box", "1,2,3")[0], 3)
        self.assertEqual(run()[0], 3)


if __name__ == "__main__":
    unittest.main()
