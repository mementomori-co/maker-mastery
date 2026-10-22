r"""tower_clearance_3mf.py - run tools\tower_clearance.py's check() on the plate G-code inside a sliced 3MF, in memory.

Why: tower_clearance.py takes plate_N.gcode file paths. A sliced 3MF carries the same G-code as Metadata/plate_N.gcode
members. Extracting them to disk would be a write, and mm_audit_server.py is read-only, so this helper opens each member as
a text stream and hands it to the unchanged tower_clearance.check(): it rebinds the module-level name `open` inside
tower_clearance to a function that serves zip members. No file is created or modified.

Input: a sliced 3MF. Output: the same JSON list tower_clearance.py --json prints (one dict per plate); "file" reads
"<3mf>!Metadata/plate_N.gcode". Exit 0 OK, 1 WARN, 2 FAIL, 3 shapely missing, 4 no plate G-code in the 3MF (not a sliced
3MF), 5 unreadable 3MF.
Usage: .venv\Scripts\python.exe -B tools\mcp\tower_clearance_3mf.py <sliced.3mf> [--min-gap 8] [--first-layer-z 0.25]
Example: .venv\Scripts\python.exe -B tools\mcp\tower_clearance_3mf.py work\slice\two_colour\out.3mf
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import zipfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # <repo>\tools
import tower_clearance as tc  # noqa: E402

PLATE_RX = re.compile(r"^Metadata/plate_(\d+)\.gcode$")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--min-gap", type=float, default=8.0)
    ap.add_argument("--first-layer-z", type=float, default=0.25)
    a = ap.parse_args(argv[1:])
    if tc.MultiPoint is None:
        print("shapely is required: run with the repository's .venv\\Scripts\\python.exe (tools\\setup.ps1 installs it)", file=sys.stderr)
        return 3
    try:
        zf = zipfile.ZipFile(a.path)  # read mode
    except (OSError, zipfile.BadZipFile) as e:
        print(f"cannot read 3MF: {e}", file=sys.stderr)
        return 5
    with zf:
        members = sorted((int(m.group(1)), n) for n in zf.namelist() if (m := PLATE_RX.match(n)))
        if not members:
            print("no Metadata/plate_N.gcode in this 3MF: it is not a sliced 3MF (slice it first)", file=sys.stderr)
            return 4
        by_label = {f"{a.path}!{n}": n for _, n in members}

        def zip_open(label, *args, **kwargs):  # replaces tower_clearance's `open`; read-only by construction
            return io.TextIOWrapper(zf.open(by_label[label], "r"), encoding="utf-8", errors="ignore")

        tc.open = zip_open  # module global shadows the builtin inside tower_clearance.collect()
        results = [tc.check(label, a.min_gap, a.first_layer_z) for label in by_label]
    rc = 0
    for r in results:
        rc = max(rc, {"OK": 0, "WARN": 1, "FAIL": 2}[r["verdict"]])
    print(json.dumps(results, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
