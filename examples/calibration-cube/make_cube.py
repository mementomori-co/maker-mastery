r"""make_cube.py - write a 20 mm calibration cube STL, then run the two geometry gates on it.

What it does:
  1. Builds a 20 x 20 x 20 mm cube with trimesh (manifold3d is used when trimesh is missing) and writes it as a binary STL,
     its lowest face on z = 0.
  2. Runs tools\overhang_gate.py on it (expected: no overhang, no islands -> OK).
  3. Runs tools\stability_check.py on it (expected: the centre of mass sits in the middle of a 20 x 20 mm footprint -> it
     cannot tip; the only WARN is that the mass comes from a uniform density, because no slicer grams were given).
Nothing is sliced, sent or printed. Slicing and printing are steps YOU take in Bambu Studio (see README.md).

Inputs: none. Output: the STL (default: cube_20mm.stl beside this script) and the two reports on screen.
Usage:   .venv\Scripts\python.exe -B examples\calibration-cube\make_cube.py [--size 20] [--out PATH]
Example: .venv\Scripts\python.exe -B examples\calibration-cube\make_cube.py
Exit code: the worst of the two gates (0 OK, 1 WARN, 2 FAIL), or 3 if the STL could not be written. The one expected
stability WARN (uniform-density mass) counts as OK and prints "WARN is expected for a cube (see README)"; any other
WARN or FAIL keeps its exit code.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(REPO, "tools")


def write_cube(path: str, size: float) -> None:
    """A watertight cube of edge `size` mm, centred on x/y = 0, standing on z = 0."""
    try:
        import trimesh
        mesh = trimesh.creation.box(extents=(size, size, size))
        mesh.apply_translation((0.0, 0.0, size / 2.0))
        mesh.export(path)
        return
    except ImportError:
        pass
    import manifold3d  # fallback when trimesh is not installed
    import numpy as np
    m = manifold3d.Manifold.cube((size, size, size), center=False).translate((-size / 2.0, -size / 2.0, 0.0)).to_mesh()
    v = np.asarray(m.vert_properties)[:, :3]
    f = np.asarray(m.tri_verts)
    with open(path, "wb") as fh:   # binary STL: 80-byte header, count, then normal + 3 vertices + attribute per triangle
        fh.write(b"calibration cube".ljust(80, b" "))
        fh.write(np.uint32(len(f)).tobytes())
        for a, b, c in f:
            n = np.cross(v[b] - v[a], v[c] - v[a])
            n = n / (np.linalg.norm(n) or 1.0)
            fh.write(np.array([*n, *v[a], *v[b], *v[c]], dtype=np.float32).tobytes() + b"\0\0")


def run_gate(script: str, *args: str) -> tuple[int, str]:
    """Run one gate, show its report, and return (exit code, report text)."""
    cmd = [sys.executable, "-B", os.path.join(TOOLS, script), *args]
    print(f"\n--- {script} " + "-" * max(0, 70 - len(script)), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.stdout.flush()
    return r.returncode, r.stdout


EXPECTED_WARN = "from uniform density"  # the mass assumption: no slicer grams exist before you slice


def only_expected_warn(report: str) -> bool:
    """True when every flag in a stability_check report is a WARN about the uniform-density mass assumption."""
    flags = [ln.strip() for ln in report.splitlines() if ln.strip().startswith(("- WARN", "- FAIL"))]
    return bool(flags) and all(f.startswith("- WARN") and EXPECTED_WARN in f for f in flags)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=float, default=20.0, help="cube edge in mm (default 20)")
    ap.add_argument("--out", default=os.path.join(HERE, "cube_20mm.stl"), help="STL path to write")
    a = ap.parse_args(argv)
    try:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        write_cube(a.out, a.size)
    except Exception as e:  # noqa: BLE001
        print(f"could not write the STL: {e}", file=sys.stderr)
        return 3
    print(f"wrote {a.out} ({a.size:g} mm cube)", flush=True)
    rc1, _ = run_gate("overhang_gate.py", a.out)
    rc2, report = run_gate("stability_check.py", a.out)
    print(f"\noverhang_gate exit {rc1}, stability_check exit {rc2}.")
    if rc2 == 1 and only_expected_warn(report):
        print("WARN is expected for a cube (see README): the mass is a uniform-density estimate until you slice it.")
        rc2 = 0
    print("Next: open the STL in Bambu Studio (README.md). You press Print; the AI never does.")
    return max(rc1, rc2)


if __name__ == "__main__":
    sys.exit(main())
