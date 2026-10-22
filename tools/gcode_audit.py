r"""gcode_audit.py - audit a Bambu Studio plate G-code for the things result.json does not show.

What it does: reads one plate G-code (read-only) and reports, per plate:
  - per-feature extrusion extents (xmin/xmax/ymin/ymax) and total extruded path length, per tool (T0/T1)
  - extrusion points outside an allowed X range (default 25..325 = H2C shared area; pass --xmin/--xmax)
  - support present? (any "Support" feature extrusion) and on which objects
  - tool changes (T lines) and the header lines "; filament used [g]", "; filament_map =", "; filament_map_mode ="
  - objects seen (from "; start printing object, unique label id: N" markers) with their XY bounds
  - arc segments: extruding G2/G3 moves and their summed length. Path lengths count an arc as r * |sweep|
    (tools\gcode_paths.py arc_points: I/J or R form, end = start -> full circle). Extents (x/y min/max) and
    outside-X points use the arc END points only (an arc bulging past its end points is not in the extents).
  - bridge rows: per "; FEATURE: Bridge" layer (keyed by the "; Z_HEIGHT:" block) the path length, the longest printed
    bridge LINE (an upper bound on the span crossed: lines run anchor to anchor on a two-sided bridge but parallel to
    the anchor on a one-sided lip), the XY extents, and "supported_below" = the fraction of 1 mm samples along the bridge
    lines with extrusion of the immediately preceding Z_HEIGHT block within about 1 mm (0.5 mm cells, 3x3; arcs sampled
    along the arc). Information only: Bambu Studio 02.08 has a single bridge role (ExtrusionEntity.cpp v02.08.02.61 L627
    maps erBridgeInfill -> "Bridge"; no "Internal Bridge" label), so the first solid layer over sparse infill is also
    "Bridge", and the fraction does not separate the two. Whether a row is a visible ceiling comes from the geometry
    (tools\overhang_gate.py). WARN while no measured clean-span limit exists; with --bridge-limit <mm> (a coupon row for
    this printer / material / profile) FAIL when the longest line of any Bridge row exceeds it.
Exit 0 = no findings, 1 = warnings (support present, points outside range, bridges without a limit), 2 = FAIL (bridge over
the limit), 3 = unreadable input.

Input: a plate G-code file. Output: text report (or --json).
Usage: .venv\Scripts\python.exe tools\gcode_audit.py <plate.gcode> [--xmin 25 --xmax 325] [--json] [--bridge-limit MM]
Example: .venv\Scripts\python.exe tools\gcode_audit.py work\slice\cube\plate_1.gcode --xmin 0 --xmax 256
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gcode_paths import arc_points  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

RX = re.compile(r"([XYZE])(-?\d*\.?\d+)")
RX_ARC = re.compile(r"([IJR])(-?\d*\.?\d+)")
OBJ_START = re.compile(r"^; start printing object, unique label id: (\d+)")
OBJ_STOP = re.compile(r"^; stop printing object, unique label id: (\d+)")


def audit(path: str, xmin: float, xmax: float, bridge_limit: float | None = None) -> dict:
    feat = "?"
    tool = None
    x = y = None
    z = 0.0
    cur_obj = None
    stats = collections.defaultdict(lambda: [1e9, -1e9, 1e9, -1e9, 0.0])  # (feature, tool) -> xmin xmax ymin ymax length
    objects = collections.defaultdict(lambda: {"xmin": 1e9, "xmax": -1e9, "ymin": 1e9, "ymax": -1e9, "points": 0, "features": set()})
    outside = collections.Counter()
    tool_changes = 0
    custom_outside = 0
    support_objs = set()
    header = {}
    arc_segments = 0
    arc_length = 0.0
    # bridge spans per layer. A "; FEATURE:Bridge" extrusion is an unsupported span (Bambu's bridge infill is laid along
    # the span, so the longest single extruding segment of a layer approximates the span it crosses); "Internal Bridge" is tracked apart.
    bridges = collections.defaultdict(lambda: {"length_mm": 0.0, "longest_line_mm": 0.0, "segments": 0, "xmin": 1e9, "xmax": -1e9, "ymin": 1e9, "ymax": -1e9,
                                               "pts": [], "supported": None})
    # This slicer version has ONE bridge role: ExtrusionEntity.cpp v02.08.02.61 L627 maps erBridgeInfill -> "Bridge" and nothing maps to an
    # "Internal Bridge" label, so the first solid layer over sparse infill is also "Bridge". "supported_below" = the fraction of 1 mm samples
    # along the bridge lines with extrusion of the IMMEDIATELY PRECEDING "; Z_HEIGHT:" block within one 0.5 mm cell (3x3, <= ~1.1 mm).
    # Only that block is kept, so in by-object sequencing the comparison is against the other object's last layer; the fraction is per
    # sample, not per mm of path. Rows are keyed by the layer z of the "; Z_HEIGHT:" block. Arcs (G2/G3) are
    # sampled along the arc, not the chord.
    CELL = 0.5
    prev_cells: set = set()
    cur_cells: set = set()
    layer_z = None

    def cells_along_pts(pts, step=1.0):
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / step))
            out.extend((int((x0 + (x1 - x0) * k / n) // CELL), int((y0 + (y1 - y0) * k / n) // CELL)) for k in range(n + 1))
        return out

    def near(cell, cells):
        cx, cy = cell
        return any((cx + dx, cy + dy) in cells for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    def close_layer():
        nonlocal prev_cells, cur_cells
        for (f, zz), b in bridges.items():
            if zz == layer_z and b["pts"] and b["supported"] is None:
                b["supported"] = round(sum(1 for c in b["pts"] if near(c, prev_cells)) / len(b["pts"]), 3)
                b["pts"] = []
        prev_cells, cur_cells = cur_cells, set()
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if line.startswith(";"):
                if line.startswith("; FEATURE:"):
                    feat = line.split(":", 1)[1].strip()
                elif line.startswith("; Z_HEIGHT:"):
                    try:
                        z = float(line.split(":")[1])
                    except ValueError:
                        pass
                    if layer_z is None or abs(z - layer_z) > 1e-6:
                        if layer_z is not None:
                            close_layer()
                        layer_z = z
                elif (line.startswith("; filament used [g]") or line.startswith("; total filament used [g]") or line.startswith("; estimated printing time")
                      or line.startswith("; filament_map =") or line.startswith("; filament_map_mode =")):
                    # filament_map / filament_map_mode: the sliced grouping, the only proof of which extruder each filament used
                    # (2 = RIGHT, 1 = LEFT on the H2C)
                    k, _, v = line[2:].partition("=")
                    header[k.strip()] = v.strip()
                else:
                    m = OBJ_START.match(line)
                    if m:
                        cur_obj = m.group(1)
                    elif OBJ_STOP.match(line):
                        cur_obj = None
                continue
            if line.startswith("T") and line[1:].strip().isdigit():
                tool = int(line[1:])
                tool_changes += 1
                continue
            if not line.startswith(("G1 ", "G0 ", "G2 ", "G3 ")):
                continue
            d = {k: float(v) for k, v in RX.findall(line.split(";")[0])}
            nx, ny = d.get("X", x), d.get("Y", y)
            if "Z" in d:
                z = d["Z"]
            if d.get("E", 0) > 0 and ("X" in d or "Y" in d) and nx is not None and ny is not None:
                s = stats[(feat, tool)]
                s[0] = min(s[0], nx); s[1] = max(s[1], nx); s[2] = min(s[2], ny); s[3] = max(s[3], ny)
                if x is not None and y is not None:
                    path_pts = [(x, y), (nx, ny)]
                    if line.startswith(("G2 ", "G3 ")):
                        a = {k: float(v) for k, v in RX_ARC.findall(line.split(";")[0])}
                        try:
                            pts, seg, _chord = arc_points(x, y, nx, ny, line.startswith("G2 "), a.get("I"), a.get("J"), a.get("R"), max_step=0.5)
                            path_pts = [(x, y)] + list(pts)
                        except ValueError:  # malformed arc (no I/J/R): fall back to the chord
                            seg = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
                        arc_segments += 1
                        arc_length += seg
                    else:
                        seg = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
                    s[4] += seg
                    if feat != "Custom":
                        cur_cells.update(cells_along_pts(path_pts))
                    if feat in ("Bridge", "Internal Bridge"):
                        b = bridges[(feat, round(layer_z if layer_z is not None else z, 2))]
                        b["length_mm"] += seg
                        b["segments"] += 1
                        b["longest_line_mm"] = max(b["longest_line_mm"], seg)
                        b["xmin"] = min(b["xmin"], x, nx); b["xmax"] = max(b["xmax"], x, nx)
                        b["ymin"] = min(b["ymin"], y, ny); b["ymax"] = max(b["ymax"], y, ny)
                        b["pts"].extend(cells_along_pts(path_pts))
                if (nx < xmin or nx > xmax) and feat != "Custom":
                    outside[(feat, tool, round(nx), round(ny), round(z, 1))] += 1
                elif (nx < xmin or nx > xmax):
                    custom_outside += 1
                if feat != "Custom":
                    o = objects[cur_obj if cur_obj is not None else "untagged"]
                    o["xmin"] = min(o["xmin"], nx); o["xmax"] = max(o["xmax"], nx)
                    o["ymin"] = min(o["ymin"], ny); o["ymax"] = max(o["ymax"], ny)
                    o["points"] += 1
                    o["features"].add(feat)
                    if "Support" in feat:
                        support_objs.add(cur_obj if cur_obj is not None else "untagged")
            x, y = nx, ny
    features = {f"{k[0]} | T{k[1]}": {"xmin": round(v[0], 1), "xmax": round(v[1], 1), "ymin": round(v[2], 1), "ymax": round(v[3], 1), "length_mm": round(v[4])} for k, v in stats.items()}
    support_len = sum(v["length_mm"] for k, v in features.items() if k.startswith("Support"))
    objs = {k: {**{kk: (round(vv, 1) if isinstance(vv, float) else vv) for kk, vv in v.items() if kk != "features"}, "features": sorted(v["features"])} for k, v in objects.items()}
    findings = []
    if support_len > 0:
        findings.append({"level": "WARN", "msg": f"support extrusion present: {support_len} mm of path on objects {sorted(support_objs) or ['(untagged)']}"})
    if outside:
        findings.append({"level": "WARN", "msg": f"{sum(outside.values())} extrusion points outside X {xmin}..{xmax}; worst: {outside.most_common(3)}"})
    close_layer()
    # bridge report: one row per (feature, layer z), longest line first. longest_line_mm is the longest printed bridge LINE: it equals the
    # gap crossed only when lines run anchor to anchor; on a one-sided lip Bambu lays them parallel to the anchor (27 mm lines measured
    # over a 2.3 mm deep strip), so it is an UPPER bound on the span and fails safe against a limit.
    bridge_rows = sorted(
        [{"feature": k[0], "z": k[1], "length_mm": round(v["length_mm"], 1), "longest_line_mm": round(v["longest_line_mm"], 2), "segments": v["segments"],
          "supported_below": v["supported"],
          "xmin": round(v["xmin"], 1), "xmax": round(v["xmax"], 1), "ymin": round(v["ymin"], 1), "ymax": round(v["ymax"], 1)} for k, v in bridges.items()],
        key=lambda r: (-r["longest_line_mm"], r["z"]))
    ext_rows = [r for r in bridge_rows if r["feature"] == "Bridge"]
    if ext_rows:
        worst = ext_rows[0]
        total = round(sum(r["length_mm"] for r in ext_rows), 1)
        where = f"{len(ext_rows)} layer(s), {total} mm of Bridge path; longest bridge line {worst['longest_line_mm']} mm at z {worst['z']} (x {worst['xmin']}..{worst['xmax']}, y {worst['ymin']}..{worst['ymax']}; an upper bound on the span crossed)"
        if bridge_limit is None:
            findings.append({"level": "WARN", "msg": f"bridge spans present (checklist item 11, not items 5/6): {where}. This slicer labels bridging over sparse infill 'Bridge' too "
                                                     f"(one role, ExtrusionEntity.cpp v02.08.02.61 L627), and the layer-below test does not separate the two (measured: 0.57 over "
                                                     f"15 % infill vs 0.65 on a 2 mm open-air lip), so which rows are visible ceilings is decided by the geometry (overhang_gate.py "
                                                     f"down-facing area at that z). No measured clean-span limit for this printer/material/profile was given: a bridge on a visible "
                                                     f"face is not accepted on belief - pass --bridge-limit <mm> from a printed coupon row, chamfer the ceiling, or write the prediction"})
        elif worst["longest_line_mm"] > bridge_limit:
            findings.append({"level": "FAIL", "msg": f"bridge line {worst['longest_line_mm']} mm at z {worst['z']} exceeds the measured clean limit {bridge_limit} mm (item 11); {where}"})
        else:
            findings.append({"level": "OK", "msg": f"bridge lines within the measured clean limit {bridge_limit} mm: {where}"})
    return {
        "file": path, "header": header, "tool_changes": tool_changes, "features": features,
        "objects": objs, "support_length_mm": support_len, "outside_points": sum(outside.values()), "custom_outside_points": custom_outside,
        "arc_segments": arc_segments, "arc_length_mm": round(arc_length, 1),
        "bridges": bridge_rows, "bridge_limit_mm": bridge_limit,
        "findings": findings, "verdict": ("FAIL" if any(f["level"] == "FAIL" for f in findings) else ("WARN" if any(f["level"] == "WARN" for f in findings) else "OK")),
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--xmin", type=float, default=25.0)
    ap.add_argument("--xmax", type=float, default=325.0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--bridge-limit", type=float, default=None,
                    help="measured clean bridge span in mm from a coupon row for this printer/material/profile; without it, bridges are reported as WARN 'not verified'")
    a = ap.parse_args(argv[1:])
    try:
        r = audit(a.path, a.xmin, a.xmax, a.bridge_limit)
    except OSError as e:
        print(f"cannot read {a.path}: {e}", file=sys.stderr)
        return 3   # unreadable / usage, distinct from the verdict codes 0/1/2 (overhang_gate.py uses 3 the same way)
    if a.json:
        print(json.dumps(r, indent=1))
    else:
        print(f"G-code audit: {a.path}")
        for k, v in r["header"].items():
            print(f"  {k} = {v}")
        print(f"  tool changes: {r['tool_changes']}  objects: {len(r['objects'])}  support path: {r['support_length_mm']} mm  outside X {a.xmin}..{a.xmax}: {r['outside_points']} pts (+{r['custom_outside_points']} in start/end G-code 'Custom', ignored)")
        print(f"  arc segments: {r['arc_segments']}, arc length: {r['arc_length_mm']:.1f} mm")
        for k, v in sorted(r["features"].items()):
            print(f"  {k:28s} x {v['xmin']:7.1f}..{v['xmax']:7.1f}  y {v['ymin']:7.1f}..{v['ymax']:7.1f}  {v['length_mm']:>9} mm")
        if r["bridges"]:
            print(f"  bridge layers (longest segment first; limit {r['bridge_limit_mm']}):")
            for b in r["bridges"][:12]:
                print(f"    {b['feature']:16s} z {b['z']:7.2f}  path {b['length_mm']:8.1f} mm  longest line {b['longest_line_mm']:6.2f} mm  ({b['segments']} segs)  "
                      f"supported below {b['supported_below']}  x {b['xmin']}..{b['xmax']}  y {b['ymin']}..{b['ymax']}")
            if len(r["bridges"]) > 12:
                print(f"    ... {len(r['bridges']) - 12} more layer rows in --json")
        for f in r["findings"]:
            print(f"  [{f['level']}] {f['msg']}")
        print(f"VERDICT: {r['verdict']}")
    return {"OK": 0, "WARN": 1, "FAIL": 2}[r["verdict"]]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
