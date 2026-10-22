r"""test_overhang_gate.py - unit tests for tools\overhang_gate.py on synthetic solids built here with manifold3d / trimesh.

Covers: the angle convention, the pose and plate offset, a 45 deg chamfer at the threshold, a new groove against a reference
(new overhang + new cantilever = FAIL), an enclosed cavity roof, a corner-touching island, a moved ceiling, a non-watertight
mesh, the same table upright vs flipped, and the usage exit codes. Temporary files only; nothing is sliced or printed.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_overhang_gate.py" -v
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
    import manifold3d
    import shapely  # noqa: F401
    import trimesh
    import overhang_gate as og
    MISSING = None
except ImportError as e:   # pragma: no cover
    MISSING = f"optional dependency missing ({e}); install requirements.txt into .venv"


def write_stl(man, path: str) -> None:
    m = man.to_mesh()
    trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3], np.asarray(m.tri_verts), process=True).export(path)


def run(*args: str):
    """Run og.main in-process with a JSON report in a temp file -> (exit code, report)."""
    with tempfile.TemporaryDirectory() as td:
        js = os.path.join(td, "r.json")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = og.main(["overhang_gate.py", *args, "--json", js])
        data = {}
        if os.path.exists(js):
            with open(js, encoding="utf-8") as fh:
                data = json.load(fh)
    return rc, data


def levels(part):
    return [f[0] for f in part["flags"]]


@unittest.skipIf(MISSING, MISSING or "")
class OverhangGateTest(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.M = manifold3d.Manifold

    def tearDown(self):
        self.td.cleanup()

    def p(self, name):
        return os.path.join(self.td.name, name)

    def test_angle_convention(self):
        n = np.array([[0, 0, -1], [1, 0, 0], [0, 0, 1], [math.sqrt(0.5), 0, -math.sqrt(0.5)]])
        self.assertTrue(np.allclose(og.overhang_angle_deg(n), [0.0, 90.0, 180.0, 45.0], atol=1e-6))

    def test_pose_flip_and_place(self):
        m = trimesh.creation.box(extents=(10, 10, 4))
        m.apply_translation((0, 0, 2))
        m.vertices[m.vertices[:, 2] > 3, 0] *= 0.5   # taper the top
        p = og.posed(m, (180.0, 0.0, 0.0))
        self.assertAlmostEqual(p.bounds[0][2], 0.0, places=9)
        self.assertAlmostEqual(float(np.ptp(p.vertices[p.vertices[:, 2] > 3.9][:, 0])), 10.0, places=6)
        q = og.posed(m, (0.0, 0.0, 0.0), (100.0, 50.0, 0.0))
        self.assertAlmostEqual(q.bounds[0][0], 95.0, places=9)

    def test_chamfer_at_threshold_is_not_overhang(self):
        wedge = self.M.cube((20, 20, 20)).trim_by_plane((0.0, -1.0, 1.0), 0.0)
        write_stl(wedge, self.p("wedge.stl"))
        _, j45 = run(self.p("wedge.stl"), "--threshold", "45")
        _, j46 = run(self.p("wedge.stl"), "--threshold", "45.1")
        self.assertEqual(j45["parts"][0]["overhang_below_threshold_mm2"], 0.0)
        self.assertAlmostEqual(j46["parts"][0]["overhang_below_threshold_mm2"], 400 * math.sqrt(2), delta=0.5)

    def test_new_groove_against_reference_fails(self):
        ref = self.M.cube((40, 40, 20))
        new = ref - self.M.cube((5, 10, 4)).translate((35, 15, 8))
        write_stl(ref, self.p("ref.stl"))
        write_stl(new, self.p("new.stl"))
        rc, j = run(self.p("new.stl"), "--ref", f"new={self.p('ref.stl')}")
        part = j["parts"][0]
        self.assertAlmostEqual(part["new_overhang_mm2"], 50.0, delta=0.5)
        self.assertEqual(part["removed_overhang_mm2"], 0.0)
        self.assertAlmostEqual(part["new_cantilever_mm"], 5.0, delta=0.25)
        self.assertEqual((rc, j["verdict"]), (2, "FAIL"))
        self.assertEqual(levels(part), ["FAIL", "FAIL"])
        rc0, j0 = run(self.p("ref.stl"))
        self.assertEqual(rc0, 0)
        self.assertEqual(j0["parts"][0]["max_cantilever_mm"], 0.0)

    def test_enclosed_cavity_roof(self):
        blk = self.M.cube((30, 30, 20)) - self.M.cube((10, 10, 4)).translate((10, 10, 6))
        write_stl(blk, self.p("cavity.stl"))
        rc, j = run(self.p("cavity.stl"))
        part = j["parts"][0]
        self.assertAlmostEqual(part["overhang_below_threshold_mm2"], 100.0, delta=0.5)
        self.assertAlmostEqual(part["max_cantilever_mm"], 5.0, delta=0.05)
        self.assertEqual(rc, 1)

    def test_corner_touching_block_is_island(self):
        body = self.M.cube((5, 5, 5)) + self.M.cube((5, 5, 5)).translate((5, 5, 5))
        write_stl(body, self.p("corner.stl"))
        rc, j = run(self.p("corner.stl"))
        isl = j["parts"][0]["islands"]
        self.assertEqual(len(isl), 1)
        self.assertAlmostEqual(isl[0]["area_mm2"], 25.0, delta=0.5)
        self.assertEqual(rc, 1)

    def test_moved_ceiling_reads_as_move(self):
        blk = self.M.cube((30, 30, 20))
        write_stl(blk - self.M.cube((10, 10, 4)).translate((10, 10, 6)), self.p("ref.stl"))
        write_stl(blk - self.M.cube((10, 10, 4)).translate((10, 10, 6.3)), self.p("new.stl"))
        _, j = run(self.p("new.stl"), "--ref", f"new={self.p('ref.stl')}")
        part = j["parts"][0]
        self.assertAlmostEqual(part["net_overhang_delta_mm2"], 0.0, delta=0.5)
        fails = [f[1] for f in part["flags"] if f[0] == "FAIL" and "new overhang" in f[1]]
        self.assertEqual(len(fails), 1)
        self.assertIn("moved ceiling", fails[0])

    def test_non_watertight_flagged(self):
        m = trimesh.creation.box(extents=(20, 20, 10))
        m.apply_translation((0, 0, 5))
        trimesh.Trimesh(m.vertices, m.faces[1:], process=False).export(self.p("holey.stl"))
        rc, j = run(self.p("holey.stl"))
        self.assertFalse(j["parts"][0]["watertight"])
        self.assertTrue(any("not watertight" in f[1] for f in j["parts"][0]["flags"]))
        self.assertGreaterEqual(rc, 1)

    def test_table_upright_vs_flipped(self):
        legs = [self.M.cube((3, 3, 10)).translate((x, y, 0)) for x in (0, 27) for y in (0, 27)]
        table = self.M.cube((30, 30, 3)).translate((0, 0, 10)) + self.M.batch_boolean(legs, manifold3d.OpType.Add)
        write_stl(table, self.p("table.stl"))
        rc_up, j_up = run(self.p("table.stl"))
        rc_fl, j_fl = run(self.p("table.stl"), "--pose", "table=180,0,0")
        self.assertAlmostEqual(j_up["parts"][0]["overhang_below_threshold_mm2"], 900.0 - 36.0, delta=0.5)
        self.assertEqual(j_fl["parts"][0]["overhang_below_threshold_mm2"], 0.0)
        self.assertEqual((rc_up, rc_fl), (1, 0))

    def test_usage_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(og.main(["overhang_gate.py", "--help"]), 0)
            self.assertEqual(og.main(["overhang_gate.py", self.p("missing.stl")]), 3)
            write_stl(self.M.cube((5, 5, 5)), self.p("c.stl"))
            self.assertEqual(og.main(["overhang_gate.py", self.p("c.stl"), "--pose", "nosuch=1,2,3"]), 3)


if __name__ == "__main__":
    unittest.main()
