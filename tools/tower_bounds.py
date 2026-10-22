r"""tower_bounds.py - measure the prime-tower footprint from Bambu Studio G-code.

What it does: reads `; FEATURE: Prime tower` extrusion moves (G1/G2/G3 with positive E) and reports the all-layer XY bounds
(0.5 / 99.5 percentile to ignore stray travel) and the first-layer bounds (Z < first_layer_z). The first layer includes the
tower brim, which is wider than the body: that is the footprint that collides. Measured on one H2C slice: body about
30 x 27 mm, first layer about 5 mm wider on every side than the body around wipe_tower_x/y.

Input: one or more plate G-code files. Output: text (or --json). Exit 0; a plate without a tower prints "no prime tower".
Usage: .venv\Scripts\python.exe tools\tower_bounds.py <plate.gcode> [...] [--json] [--first-layer-z 0.25]
Example: .venv\Scripts\python.exe tools\tower_bounds.py work\slice\two_colour\plate_1.gcode --json
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

RX = re.compile(r"([XYZE])(-?\d*\.?\d+)")


def pct(v: list[float], p: float) -> float:
    v = sorted(v)
    return v[min(len(v) - 1, int(p * len(v)))]


def measure(path: str, first_layer_z: float) -> dict:
    feat = None
    x = y = None
    z = 0.0
    xs: list[float] = []
    ys: list[float] = []
    x1: list[float] = []
    y1: list[float] = []
    layers = set()
    with open(path, errors="ignore") as fh:
        for line in fh:
            if line.startswith("; FEATURE:"):
                feat = line[10:].strip()
                continue
            if line.startswith("; Z_HEIGHT:"):
                try:
                    z = float(line.split(":")[1])
                except ValueError:
                    pass
                continue
            if not line.startswith(("G1 ", "G2 ", "G3 ")):
                continue
            d = {k: float(v) for k, v in RX.findall(line.split(";")[0])}
            nx, ny = d.get("X", x), d.get("Y", y)
            if feat == "Prime tower" and d.get("E", 0) > 0 and x is not None and ("X" in d or "Y" in d):
                xs.append(nx)
                ys.append(ny)
                layers.add(round(z, 2))
                if z < first_layer_z:
                    x1.append(nx)
                    y1.append(ny)
            x, y = nx, ny
    if not xs:
        return {"file": path, "prime_tower": False}
    out = {
        "file": path,
        "prime_tower": True,
        "layers_with_tower": len(layers),
        "all_layers": {"xmin": round(pct(xs, 0.005), 2), "xmax": round(pct(xs, 0.995), 2), "ymin": round(pct(ys, 0.005), 2), "ymax": round(pct(ys, 0.995), 2)},
    }
    if x1:
        out["first_layer"] = {"xmin": round(min(x1), 2), "xmax": round(pct(x1, 0.999), 2), "ymin": round(min(y1), 2), "ymax": round(pct(y1, 0.999), 2)}
        out["first_layer"]["width"] = round(out["first_layer"]["xmax"] - out["first_layer"]["xmin"], 2)
        out["first_layer"]["depth"] = round(out["first_layer"]["ymax"] - out["first_layer"]["ymin"], 2)
    a = out["all_layers"]
    a["width"] = round(a["xmax"] - a["xmin"], 2)
    a["depth"] = round(a["ymax"] - a["ymin"], 2)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--first-layer-z", type=float, default=0.25)
    a = ap.parse_args(argv[1:])
    results = [measure(p, a.first_layer_z) for p in a.paths]
    if a.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            if not r["prime_tower"]:
                print(f"{r['file']}: no prime tower")
                continue
            al = r["all_layers"]
            print(f"{r['file']}: tower body x {al['xmin']}..{al['xmax']} y {al['ymin']}..{al['ymax']} ({al['width']}×{al['depth']} mm, {r['layers_with_tower']} layers)")
            if "first_layer" in r:
                f = r["first_layer"]
                print(f"    first layer (incl. brim) x {f['xmin']}..{f['xmax']} y {f['ymin']}..{f['ymax']} ({f['width']}×{f['depth']} mm)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
