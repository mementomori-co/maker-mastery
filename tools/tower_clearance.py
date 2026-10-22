r"""tower_clearance.py - the GUI "Prime Tower is too close to others" check, replicated on the real G-code.

Why: Bambu Studio's `layered_print_cleareance_valid` (src/libslic3r/Print.cpp L949-1055, https://github.com/bambulab/BambuStudio)
intersects the 2D convex hull of every object with a rectangle built from wipe_tower_x/y, prime_tower_width and the computed
depth (width = depth when rib wall is on). It is a non-fatal warning that the Windows CLI does not write to result.json.
Whether the tower BRIM is inside that rectangle is an open question (the measured first layer extends about 5 mm past the
body), so this tool measures the real printed footprints from the G-code and applies a conservative gap rule.

Method (shapely): per plate G-code, collect extrusion XY per object (markers "; start/stop printing object, unique label id")
and for the prime tower ("; FEATURE: Prime tower"); build convex hulls of (a) the tower body (all layers) and (b) the tower
first layer incl. brim; compute the minimum distance from each hull to every object hull.
  FAIL  if any object hull intersects the first-layer (brim) hull.
  WARN  if the gap body -> object < --min-gap (default 8 mm, a house rule).
  OK    otherwise. Objects' own brims are included in their hulls because they are extruded under the object marker.
Plates with a single object carry no object markers in Bambu G-code; all non-tower, non-Custom extrusion is then bucketed
as object "untagged". The start-G-code purge line (feature Custom) is excluded.

Input: plate G-code files. Output: text (or --json). Exit 0 OK, 1 WARN, 2 FAIL (3 if shapely missing).
Usage: .venv\Scripts\python.exe tools\tower_clearance.py <plate.gcode> [...] [--min-gap 8] [--json]
Example: .venv\Scripts\python.exe tools\tower_clearance.py work\slice\two_colour\plate_1.gcode
"""
from __future__ import annotations

import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

try:
    from shapely.geometry import MultiPoint
except Exception:  # noqa: BLE001
    MultiPoint = None

RX = re.compile(r"([XYZE])(-?\d*\.?\d+)")
OBJ_START = re.compile(r"^; start printing object, unique label id: (\d+)")
OBJ_STOP = re.compile(r"^; stop printing object, unique label id: (\d+)")
OBJ_NAME = re.compile(r"^; object_label_id: (\d+)\s*$|^; printing object (.+?) id:(\d+)")


def collect(path: str, first_layer_z: float):
    feat = None
    x = y = None
    z = 0.0
    cur = None
    objs: dict[str, list[tuple[float, float]]] = {}
    tower_all: list[tuple[float, float]] = []
    tower_first: list[tuple[float, float]] = []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if line.startswith(";"):
                if line.startswith("; FEATURE:"):
                    feat = line[10:].strip()
                elif line.startswith("; Z_HEIGHT:"):
                    try:
                        z = float(line.split(":")[1])
                    except ValueError:
                        pass
                else:
                    m = OBJ_START.match(line)
                    if m:
                        cur = m.group(1)
                    elif OBJ_STOP.match(line):
                        cur = None
                continue
            if not line.startswith(("G1 ", "G2 ", "G3 ")):
                continue
            d = {k: float(v) for k, v in RX.findall(line.split(";")[0])}
            nx, ny = d.get("X", x), d.get("Y", y)
            if d.get("E", 0) > 0 and nx is not None and ny is not None and ("X" in d or "Y" in d):
                if feat == "Prime tower":
                    tower_all.append((nx, ny))
                    if z < first_layer_z:
                        tower_first.append((nx, ny))
                elif feat not in ("Custom", None):
                    objs.setdefault(cur if cur is not None else "untagged", []).append((nx, ny))
            x, y = nx, ny
    return objs, tower_all, tower_first


def hull(points):
    if len(points) < 3:
        return None
    step = max(1, len(points) // 20000)  # subsample very large point sets; hull is unaffected in practice
    return MultiPoint(points[::step]).convex_hull


def check(path: str, min_gap: float, first_layer_z: float) -> dict:
    objs, tower_all, tower_first = collect(path, first_layer_z)
    if not tower_all:
        return {"file": path, "prime_tower": False, "verdict": "OK", "msg": "no prime tower on this plate"}
    h_body = hull(tower_all)
    h_first = hull(tower_first) if tower_first else h_body
    rows = []
    worst = "OK"
    for oid, pts in objs.items():
        h = hull(pts)
        if h is None:
            continue
        gap_body = h_body.distance(h)
        gap_first = h_first.distance(h)
        intersects = h_first.intersects(h)
        level = "FAIL" if intersects else ("WARN" if gap_body < min_gap else "OK")
        if level == "FAIL" or (level == "WARN" and worst != "FAIL"):
            worst = level
        bx = h.bounds
        rows.append({"object_label": oid, "points": len(pts), "bounds": [round(v, 1) for v in bx],
                     "gap_to_tower_body_mm": round(gap_body, 2), "gap_to_tower_first_layer_mm": round(gap_first, 2),
                     "intersects_first_layer": intersects, "level": level})
    b = h_body.bounds
    f = h_first.bounds
    return {
        "file": path, "prime_tower": True,
        "tower_all_layers_bounds": [round(v, 1) for v in b], "tower_first_layer_bounds": [round(v, 1) for v in f],
        "min_gap_rule_mm": min_gap, "objects": rows, "verdict": worst,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--min-gap", type=float, default=8.0)
    ap.add_argument("--first-layer-z", type=float, default=0.25)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])
    if MultiPoint is None:
        print("shapely is required: run with the repository's .venv\\Scripts\\python.exe (tools\\setup.ps1 installs it)", file=sys.stderr)
        return 3
    results = [check(p, a.min_gap, a.first_layer_z) for p in a.paths]
    rc = 0
    for r in results:
        rc = max(rc, {"OK": 0, "WARN": 1, "FAIL": 2}[r["verdict"]])
        if a.json:
            continue
        if not r["prime_tower"]:
            print(f"{r['file']}: {r['msg']}")
            continue
        print(f"{r['file']}: tower all-layers {r['tower_all_layers_bounds']} first-layer {r['tower_first_layer_bounds']} (rule: gap >= {r['min_gap_rule_mm']} mm)")
        for o in r["objects"]:
            print(f"  [{o['level']}] object {o['object_label']}: bounds {o['bounds']} gap body {o['gap_to_tower_body_mm']} mm, first-layer {o['gap_to_tower_first_layer_mm']} mm" + (" INTERSECTS" if o["intersects_first_layer"] else ""))
        print(f"  VERDICT: {r['verdict']}")
    if a.json:
        print(json.dumps(results, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
