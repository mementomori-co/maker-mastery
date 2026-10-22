r"""interface_coverage.py - support coverage of overhanging perimeter, per region and per sector, read back from a sliced plate G-code.

Why: with Support > Support critical regions only (label not verified) a visible ledge can print with only a fifth of its lip
supported (made-up example: a 300 mm2 ledge at 10 deg slope whose front lip is 20 % supported), and a review can mistake incidental
interface for support. The slicer filter's tests are > 3 mm cantilever (TreeSupport.cpp v02.08.02.61 L1043-1045,
https://github.com/bambulab/BambuStudio) and a floating sharp tail < 100 mm2 (L979-990), not attachment. This tool measures,
for any plate and any object, how much of each overhanging region actually has support under it:

  1. Every object extrusion line (features other than Support*, Brim, Skirt, Custom, Prime/Wipe tower, Flush) of every layer block is sampled
     every --step mm (0.2). A sample OVERHANGS by depth d when the nearest object extrusion of the PREVIOUS object layer is d > --depth-min
     mm (0.5, about a line width) away, centre to centre.
  2. An overhanging sample is SUPPORTED when any Support / Support interface / Support transition line lies within --radius mm XY in the
     --below mm (3.0) under it. Default radius = max(0.6, (support_line_width + support_interface_spacing) / 2 + 0.1) from the G-code header
     (interface line centres sit width + spacing apart, 0.92 mm at the stock 0.42 / 0.5). With support_interface_top_layers = 0
     the test reads against the sparser support body and says so.
  3. Overhanging samples are grouped into REGIONS: connected components over neighbours within --link mm XY (1.0) and 0.6 mm in z. Per region:
     mm of overhanging line, depth p50 / p90 / max, z range, XY box, supported %, features, the azimuth sector (front -Y / right +X / back +Y /
     left -X) and the supported % of each sector slice of the region. Sector centre: --center x,y for everything, else one object-sample
     centroid PER OBJECT (G-code label) over the window's layers, so a plate of eleven coupons gets eleven centres.
  4. Verdict rules (house values): with support ON, a region of >= --min-mm mm (10) whose depth p90 > --visible-depth mm
     (1.0) is a visible candidate; it is FAIL when its coverage is < --cover-fail (90 %) OR when any of its sector slices of >= --min-mm mm is
     (a region at 92 % overall can carry a whole bare side); when
     support_critical_regions_only = 1 or support_remove_small_overhang = 1, every such region is also listed as "not guaranteed support by the
     filter (its tests are > 3 mm cantilever and floating sharp tail, not attachment): verify coverage or paint". With
     support OFF the regions are reported as information (nothing could be supported). Internal overhangs (over sparse infill, inside the
     part) also show up as overhanging samples: the region's features say which lines they are (Sparse infill / Internal solid infill vs
     Outer wall / Overhang wall / Bridge); --walls-only (default on) keeps only wall and bridge features, the visible ones. A sample whose
     nearest line in the layer below is Sparse infill is the slicer's internal bridging over infill (labelled "Bridge" too, ExtrusionEntity.cpp
     v02.08.02.61 L627), and a REGION with no overhanging perimeter sample (Outer wall / Inner wall / Overhang wall) that touches such
     samples, or whose lines sit mostly over infill-side lines below, is ENCLOSED: its perimeter stands on the perimeter below and the span is
     the first solid layer over sparse infill (and the band of it next to the walls), not a visible face. Both are counted apart
     (internal_bridge_samples_excluded; the region share in enclosed_region_samples_excluded), not as overhangs; their spans belong to
     gcode_audit.py's bridge rows (checklist item 11). A perimeter-less region touching NO over-infill sample whose lines sit over WALLS below
     (>= 50 % of its samples) is a cavity ROOF SPAN, visible from below (a box printed open side down, a slot roof, the arch under a plaque): it
     stays a candidate, labelled "roof span". A lip, shelf, hem or ceiling always has its own perimeter over air. Known limit (by
     design): visible_depth 1.0 means a slope between about 11 deg (0.2 mm
     layers) and the 30 deg threshold is never a candidate, so a bare 15 deg slope the slicer should have supported does not FAIL here.

Usage:
  .venv\Scripts\python.exe tools\interface_coverage.py <plate_N.gcode> [--z lo,hi] [--center x,y] [--json out.json]
  or  ... --3mf FILE.3mf --plate N
  [--step 0.2] [--depth-min 0.5] [--radius MM] [--below 3.0] [--link 1.0] [--min-mm 10] [--visible-depth 1.0] [--cover-fail 90] [--all-features]
Exit 0 = no FAIL (OK or information), 1 = WARN (filter on, regions listed), 2 = FAIL (a visible region or one of its sides under the coverage
threshold), 3 = unreadable / usage / two inputs / --json not writable. print-qa runs it for
checklist item 5/6 (support coverage) on every plate with support ON.
Example: .venv\Scripts\python.exe tools\interface_coverage.py --3mf work\slice\bracket\out.3mf --plate 1
Read-only on the inputs; nothing printed or sent.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gcode_paths import arc_points  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

RX = re.compile(r"([XYZEIJR])(-?\d*\.?\d+)")
SUPPORT_FEATS = ("Support", "Support interface", "Support transition")
NON_OBJECT = SUPPORT_FEATS + ("Brim", "Skirt", "Custom", "Prime tower", "Wipe tower", "Flush")
WALL_FEATS = ("Outer wall", "Inner wall", "Overhang wall", "Bridge", "Floating vertical shell", "Gap infill", "Top surface", "Bottom surface")
PERIMETER_FEATS = ("Outer wall", "Inner wall", "Overhang wall")


def parse_gcode(fh, zlo: float, zhi: float):
    """-> header, {z: {"h": layer height, "obj": [(x0,y0,x1,y1,feat_idx,label)], "sup": [(x0,y0,x1,y1)]}}, feature names."""
    header: dict = {}
    feats: list[str] = []
    fidx: dict[str, int] = {}
    layers: dict = collections.defaultdict(lambda: {"h": None, "obj": [], "sup": []})
    x = y = None
    z = None
    lh = None
    feat = None
    label = None
    in_config = False
    for line in fh:
        if line.startswith(";"):
            if line.startswith("; FEATURE:"):
                feat = line.split(":", 1)[1].strip()
                if feat not in fidx:
                    fidx[feat] = len(feats)
                    feats.append(feat)
            elif line.startswith("; Z_HEIGHT:"):
                try:
                    z = round(float(line.split(":", 1)[1]), 3)
                except ValueError:
                    pass
            elif line.startswith("; LAYER_HEIGHT:"):
                try:
                    lh = round(float(line.split(":", 1)[1]), 3)
                except ValueError:
                    pass
            elif line.startswith("; start printing object, unique label id:"):
                label = int(line.rsplit(":", 1)[1])
            elif line.startswith("; stop printing object, unique label id:"):
                label = None
            elif line.startswith("; CONFIG_BLOCK_START"):
                in_config = True
            elif line.startswith("; CONFIG_BLOCK_END"):
                in_config = False
            elif in_config:
                m = re.match(r"^; ([A-Za-z0-9_]+) = (.*)$", line)
                if m and m.group(1) not in header:
                    header[m.group(1)] = m.group(2).strip()
            continue
        if not line.startswith(("G1 ", "G0 ", "G2 ", "G3 ")):
            continue
        d = {k: float(v) for k, v in RX.findall(line.split(";")[0])}
        nx, ny = d.get("X", x), d.get("Y", y)
        if (d.get("E", 0) > 0 and ("X" in d or "Y" in d) and x is not None and y is not None and z is not None and feat not in (None, "Custom")
                and zlo - 3.5 <= z <= zhi + 0.5):
            pts = [(x, y), (nx, ny)]
            if line.startswith(("G2 ", "G3 ")):
                try:
                    arc, _l, _c = arc_points(x, y, nx, ny, line.startswith("G2 "), d.get("I"), d.get("J"), d.get("R"), max_step=0.3)
                    pts = [(x, y)] + list(arc)
                except ValueError:
                    pass
            L = layers[z]
            if lh is not None:
                L["h"] = lh
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                if feat in SUPPORT_FEATS:
                    L["sup"].append((ax, ay, bx, by))
                elif feat not in NON_OBJECT:
                    L["obj"].append((ax, ay, bx, by, fidx[feat], label if label is not None else -1))
        x, y = nx, ny
    return header, layers, feats


def samples(segs: np.ndarray, step: float):
    """(points (N,2), segment index (N,)) sampled at mid-steps along each segment."""
    P, I = [], []
    for k, (ax, ay, bx, by) in enumerate(segs[:, :4]):
        n = max(int(math.hypot(bx - ax, by - ay) / step), 1)
        t = (np.arange(n) + 0.5) / n
        P.append(np.c_[ax + t * (bx - ax), ay + t * (by - ay)])
        I.append(np.full(n, k))
    return (np.concatenate(P), np.concatenate(I)) if P else (np.zeros((0, 2)), np.zeros(0, int))


def analyse(header, layers, feats, a, zlo, zhi) -> dict:
    zs = sorted(layers)
    obj_layers = [z for z in zs if layers[z]["obj"]]
    # support points with z
    SP = []
    for z in zs:
        if layers[z]["sup"]:
            P, _ = samples(np.array(layers[z]["sup"], dtype=float), 0.3)
            SP.append(np.c_[P, np.full(len(P), z)])
    SP = np.concatenate(SP) if SP else np.zeros((0, 3))
    st = cKDTree(SP[:, :2]) if len(SP) else None
    rows = []   # z, x, y, depth, feat_idx, supported, label, feat_idx of the nearest line below , over-sparse-infill flag
    prev, prev_feat = None, None
    wall_idx = {fidx for fidx, f in enumerate(feats) if f in WALL_FEATS}
    sparse_idx = {fidx for fidx, f in enumerate(feats) if f == "Sparse infill"}
    n_internal = 0   # every excluded sample (over sparse infill, or in an enclosed region); n_enclosed = the region-rule share of it
    cen_sum: dict[int, np.ndarray] = {}   # per object label: sum x, sum y, n over the window's object samples (sector centres)
    for z in obj_layers:
        segs = np.array(layers[z]["obj"], dtype=float)
        P, I = samples(segs, a.step)
        if zlo <= z <= zhi and len(P):
            labs = segs[I, 5].astype(int)
            for lab in np.unique(labs):
                m = labs == lab
                cen_sum.setdefault(int(lab), np.zeros(3))
                cen_sum[int(lab)] += (P[m, 0].sum(), P[m, 1].sum(), float(m.sum()))
        if prev is not None and zlo <= z <= zhi and len(P):
            d, nearest = prev.query(P)
            over = d > a.depth_min
            if a.walls_only:
                over &= np.isin(segs[I, 4].astype(int), list(wall_idx))
            # this slicer labels the first solid layer over sparse infill "Bridge" too (ExtrusionEntity.cpp v02.08.02.61 L627): a sample whose
            # nearest line in the layer below is Sparse infill is such an internal bridge, not a visible overhang -> counted apart
            below = prev_feat[nearest]
            internal = over & np.isin(below, list(sparse_idx))
            # (the second internal test, an ENCLOSED region without an overhanging perimeter line, is applied per region below: a geometric
            # "previous lines on both sides" test at 1.6 mm trimmed real ledge samples on curved folds and at 1.0 mm missed the coupon's
            # internal bridges whose nearest previous line was a Floating vertical shell, not the sparse infill 1-3 mm away). The flag rides
            # along in the rows so the region step knows which neighbours a perimeter-less region touches
            for (px, py), dd, k, bf, it in zip(P[over], d[over], I[over], below[over], internal[over]):
                sup = False
                if st is not None:
                    idx = st.query_ball_point((px, py), a.radius)
                    if idx:
                        zz = SP[idx, 2]
                        sup = bool(((zz < z) & (zz >= z - a.below)).any())
                rows.append((z, px, py, dd, int(segs[k, 4]), 1.0 if sup else 0.0, segs[k, 5], int(bf), 1.0 if it else 0.0))
        if len(P):
            prev, prev_feat = cKDTree(P), segs[I, 4].astype(int)
    R = np.array(rows, dtype=float).reshape(-1, 9)   # the over-sparse-infill samples stay in until the regions are known (they decide what their neighbours are)
    # regions: connected components of samples within link mm XY and 0.6 mm z, linked BEFORE the over-infill samples are dropped. Per region:
    #  - with an overhanging PERIMETER sample (Outer wall / Inner wall / Overhang wall): a visible face; its over-infill samples are dropped, the rest kept;
    #  - without one, touching over-infill samples or sitting mostly over infill-side lines (Sparse infill, Internal solid infill, Floating vertical
    #    shell, Gap infill: the nearest line below each sample): ENCLOSED, the first solid layer over sparse infill and the band of it next to the
    #    walls, counted apart (spans belong to gcode_audit.py's bridge rows, item 11);
    #  - without one, touching no over-infill sample and sitting over WALLS below (>= 50 % of the samples): a cavity ROOF SPAN - a box printed open
    #    side down, a slot or window roof, the arch under a plaque - visible from below, kept as a candidate (the first rule dropped
    #    every perimeter-less region; a wall-below test alone made the band next to the walls of an internal bridge a "roof").
    roots, n_enclosed = np.zeros(0, int), 0
    roof = np.zeros(0, bool)
    if len(R):
        pts3 = np.c_[R[:, 1], R[:, 2], R[:, 0] * (a.link / 0.6)]
        tree = cKDTree(pts3)
        pairs = tree.query_pairs(a.link, output_type="ndarray")
        parent = np.arange(len(R))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for i, j in pairs:
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
        roots = np.array([find(i) for i in range(len(R))])
        perim_idx = {fidx for fidx, f in enumerate(feats) if f in PERIMETER_FEATS}
        inter = R[:, 8] == 1.0
        keep = np.ones(len(R), bool)
        roof = np.zeros(len(R), bool)
        for r in np.unique(roots):
            m = roots == r
            if np.isin(R[m, 4].astype(int), list(perim_idx)).any():
                keep[m & inter] = False
            elif (m & inter).any() or np.isin(R[m, 7].astype(int), list(perim_idx)).mean() < 0.5:
                keep[m] = False
                n_enclosed += int((m & ~inter).sum())
            else:
                roof[m] = True
        n_internal = int((~keep).sum())
        R, roots, roof = R[keep], roots[keep], roof[keep]
    sup_on = str(header.get("enable_support", "0")) in ("1", "true", "True")
    crit = str(header.get("support_critical_regions_only", "0")) in ("1", "true", "True")
    rso = str(header.get("support_remove_small_overhang", "0")) in ("1", "true", "True")
    # sector centres: --center for every sample, else one object-sample centroid per object label over the window's layers
    # (a plate-wide centroid labelled eleven identical coupon shelves front/right/back/left by their position on the plate)
    centers = {lab: (float(s[0] / s[2]), float(s[1] / s[2])) for lab, s in cen_sum.items() if s[2] > 0}
    tot = np.sum(list(cen_sum.values()), axis=0) if cen_sum else np.zeros(3)
    overall = (float(tot[0] / tot[2]), float(tot[1] / tot[2])) if tot[2] > 0 else (0.0, 0.0)
    out = {"n_overhanging_samples": int(len(R)), "overhanging_mm": round(a.step * len(R), 1), "internal_bridge_samples_excluded": n_internal,
           "enclosed_region_samples_excluded": n_enclosed, "regions": [], "sectors": {}, "center": list(a.center) if a.center else None,
           "centers": {str(lab): [round(x, 2), round(y, 2)] for lab, (x, y) in sorted(centers.items())}, "support_on": sup_on,
           "filters": {"support_critical_regions_only": crit, "support_remove_small_overhang": rso}}
    if len(R) == 0:
        return out
    C = np.array([a.center if a.center else centers.get(int(lab), overall) for lab in R[:, 6]], dtype=float).reshape(-1, 2)
    az = (np.degrees(np.arctan2(R[:, 2] - C[:, 1], R[:, 1] - C[:, 0])) + 360.0) % 360.0
    sec_of = np.where((az >= 225) & (az < 315), "front", np.where((az >= 315) | (az < 45), "right", np.where((az >= 45) & (az < 135), "back", "left")))
    sector_names = {"front": "front (-Y) 225-315", "right": "right (+X) 315-45", "back": "back (+Y) 45-135", "left": "left (-X) 135-225"}
    for key, nm in sector_names.items():
        s = sec_of == key
        if s.any():
            H = R[s]
            out["sectors"][nm] = {"mm": round(a.step * len(H), 1), "depth_p50": round(float(np.median(H[:, 3])), 2), "depth_p90": round(float(np.percentile(H[:, 3], 90)), 2),
                                  "depth_max": round(float(H[:, 3].max()), 2), "supported_pct": round(100.0 * float(H[:, 5].mean()), 1),
                                  "features": dict(collections.Counter(feats[int(f)] for f in H[:, 4]))}
        else:
            out["sectors"][nm] = {"mm": 0.0}
    regs = []
    for r in np.unique(roots):
        m = roots == r
        H = R[m]
        mm = a.step * len(H)
        if mm < 1.0:
            continue
        sec = collections.Counter(sec_of[m].tolist())
        # per-sector slices of the region: a region at 92 % overall can carry a whole bare side; the slice with the lowest
        # coverage among those of >= min_mm mm decides with the region's own figure
        slices = {}
        for key in sector_names:
            sm = sec_of[m] == key
            if sm.any():
                slices[key] = {"mm": round(a.step * int(sm.sum()), 1), "supported_pct": round(100.0 * float(H[sm, 5].mean()), 1)}
        worst = min((dict(sector=k, **v) for k, v in slices.items() if v["mm"] >= a.min_mm), key=lambda v: v["supported_pct"], default=None)
        reg = {"mm": round(mm, 1), "depth_p50": round(float(np.median(H[:, 3])), 2), "depth_p90": round(float(np.percentile(H[:, 3], 90)), 2), "depth_max": round(float(H[:, 3].max()), 2),
               "z": [round(float(H[:, 0].min()), 2), round(float(H[:, 0].max()), 2)], "x": [round(float(H[:, 1].min()), 1), round(float(H[:, 1].max()), 1)],
               "y": [round(float(H[:, 2].min()), 1), round(float(H[:, 2].max()), 1)], "supported_pct": round(100.0 * float(H[:, 5].mean()), 1),
               "features": dict(collections.Counter(feats[int(f)] for f in H[:, 4])), "sector": sec.most_common(1)[0][0], "sectors": slices, "worst_sector": worst,
               "labels": sorted({int(v) for v in H[:, 6]}), "kind": "roof span" if roof[m].all() else "overhanging perimeter"}
        reg["visible_candidate"] = bool(mm >= a.min_mm and reg["depth_p90"] > a.visible_depth)
        regs.append(reg)
    regs.sort(key=lambda g: (-(g["visible_candidate"]), min(g["supported_pct"], (g["worst_sector"] or {}).get("supported_pct", 100.0)), -g["mm"]))
    out["regions"] = regs
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gcode", nargs="?")
    ap.add_argument("--3mf", dest="three", default=None)
    ap.add_argument("--plate", type=int, default=None)
    ap.add_argument("--z", default=None, metavar="lo,hi", help="object layer window (default: the whole plate)")
    ap.add_argument("--center", default=None, metavar="x,y", help="sector centre (default: object-sample centroid of the window's top layer)")
    ap.add_argument("--step", type=float, default=0.2)
    ap.add_argument("--depth-min", type=float, default=0.5)
    ap.add_argument("--radius", type=float, default=None, help="supported-test XY radius; default from the header: max(0.6, (support_line_width + support_interface_spacing) / 2 + 0.1)")
    ap.add_argument("--below", type=float, default=3.0)
    ap.add_argument("--link", type=float, default=1.0)
    ap.add_argument("--min-mm", type=float, default=10.0)
    ap.add_argument("--visible-depth", type=float, default=1.0)
    ap.add_argument("--cover-fail", type=float, default=90.0)
    ap.add_argument("--all-features", action="store_true", help="count infill overhangs too (default: walls, overhang walls, bridges, shells only)")
    ap.add_argument("--json", default=None)
    try:
        a = ap.parse_args(argv[1:])
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    a.walls_only = not a.all_features
    try:
        zlo, zhi = (-1e9, 1e9)
        if a.z:
            zlo, zhi = (float(v) for v in a.z.split(","))
        if a.center:
            a.center = tuple(float(v) for v in a.center.split(","))
            assert len(a.center) == 2
    except Exception:  # noqa: BLE001
        print("usage: --z expects lo,hi and --center expects x,y", file=sys.stderr)
        return 3
    if a.gcode and (a.three or a.plate):
        print("usage: give ONE input - a plate G-code, or --3mf FILE --plate N", file=sys.stderr)   # no silent precedence
        return 3
    try:
        if a.gcode:
            with open(a.gcode, encoding="utf-8", errors="ignore") as fh:
                header, layers, feats = parse_gcode(fh, zlo, zhi)
            src = a.gcode
        elif a.three and a.plate:
            with zipfile.ZipFile(a.three) as z:
                data = z.read(f"Metadata/plate_{a.plate}.gcode")
            header, layers, feats = parse_gcode(io.StringIO(data.decode("utf-8", "ignore")), zlo, zhi)
            src = f"{a.three}::Metadata/plate_{a.plate}.gcode"
        else:
            print("usage: give a plate G-code, or --3mf FILE --plate N", file=sys.stderr)
            return 3
    except (OSError, KeyError, zipfile.BadZipFile) as e:
        print(f"cannot read the input: {e}", file=sys.stderr)
        return 3
    def _hf(key: str) -> float | None:
        try:
            return float(str(header.get(key)).strip().rstrip("%"))
        except (TypeError, ValueError):
            return None
    radius_note = None
    if a.radius is None:
        # interface line centres sit support_line_width + support_interface_spacing apart (0.92 mm at the stock 0.42 / 0.5), so a
        # sample straight between two lines is half that away; 0.6 only covers the stock spacing. 0 = "use line_width" for the support width
        slw = _hf("support_line_width") or _hf("line_width") or 0.42
        sis = _hf("support_interface_spacing")
        sis = 0.5 if sis is None else sis
        a.radius = max(0.6, 0.5 * (slw + sis) + 0.1)
        radius_note = f"radius {a.radius:.2f} mm from support_line_width {slw:g} + support_interface_spacing {sis:g}"
    res = analyse(header, layers, feats, a, zlo, zhi)
    report = {"file": src, "window_z": [None if zlo == -1e9 else zlo, None if zhi == 1e9 else zhi], "walls_only": a.walls_only, "radius_mm": round(a.radius, 3),
              "header": {k: header.get(k) for k in ("enable_support", "support_type", "support_style", "support_critical_regions_only", "support_remove_small_overhang",
                                                   "support_threshold_angle", "support_top_z_distance", "layer_height", "support_line_width", "line_width",
                                                   "support_interface_spacing", "support_interface_top_layers")}, **res, "findings": []}
    sup_on = res.get("support_on", False)
    crit, rso = (res.get("filters") or {}).get("support_critical_regions_only", False), (res.get("filters") or {}).get("support_remove_small_overhang", False)
    if sup_on and _hf("support_interface_top_layers") == 0:
        report["findings"].append({"level": "OK", "msg": "support_interface_top_layers = 0: no interface layers, so coverage is read against the support body (its "
                                                         "pattern is sparser than an interface; a roofed face can read low) - information"})
    for g in res["regions"]:
        if not g["visible_candidate"]:
            continue
        ws = g.get("worst_sector")
        sector_bad = bool(ws and ws["supported_pct"] < a.cover_fail)
        where = (f"region {g['mm']} mm of {g['kind']} {'/'.join(sorted(g['features']))} at z {g['z']} x {g['x']} y {g['y']} ({g['sector']} sector), depth p50 {g['depth_p50']} / p90 {g['depth_p90']} / "
                 f"max {g['depth_max']} mm, supported {g['supported_pct']} %" + (f", its {ws['sector']} sector slice ({ws['mm']} mm) {ws['supported_pct']} %" if ws else ""))
        if sup_on and (g["supported_pct"] < a.cover_fail or sector_bad):
            report["findings"].append({"level": "FAIL", "msg": f"{where}: a visible overhang face{' (one side of it)' if sector_bad and g['supported_pct'] >= a.cover_fail else ''} under "
                                                                 f"{a.cover_fail:g} % support coverage with support ON (house rule; a lip that "
                                                                 f"is only about a quarter supported can fray)" + (" - the filter does not guarantee it: its tests are > 3 mm cantilever "
                                                                 f"(TreeSupport.cpp v02.08.02.61 L1043-1045) and floating sharp tail < 100 mm2 (L979-990), not attachment; verify coverage, paint "
                                                                 f"support, or turn the filter off" if (crit or rso) else " - chamfer the face, add an enforcer or paint support")})
        elif sup_on and (crit or rso):
            report["findings"].append({"level": "WARN", "msg": f"{where}: covered, but with support_critical_regions_only={int(crit)} / support_remove_small_overhang={int(rso)} coverage is not "
                                                                 f"guaranteed by the filter; the read-back above is the proof"})
        elif not sup_on:
            report["findings"].append({"level": "OK", "msg": f"{where}: support is OFF in this plate (information; the overhang prints unsupported by design or by omission)"})
    if not [f for f in report["findings"] if f["level"] != "OK" or "information" not in f["msg"]]:
        n_vis = sum(1 for g in res["regions"] if g["visible_candidate"])
        report["findings"].append({"level": "OK", "msg": f"{len(res['regions'])} overhanging region(s), {n_vis} visible candidate(s) (>= {a.min_mm:g} mm, depth p90 > {a.visible_depth:g} mm), "
                                                           f"none under {a.cover_fail:g} % coverage" if res["regions"] else "no overhanging perimeter samples in the window"})
    worst = max([{"OK": 0, "WARN": 1, "FAIL": 2}[f["level"]] for f in report["findings"]] or [0])
    report["verdict"] = ["OK", "WARN", "FAIL"][worst]
    if a.json:
        try:
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=1)
        except OSError as e:   # a failed write must not come back as exit 1 (= WARN)
            print(f"cannot write --json {a.json}: {e}", file=sys.stderr)
            return 3
    print(f"interface_coverage: {src}  window z {report['window_z']}  support {'ON' if sup_on else 'OFF'}  critical_only {int(crit)}  remove_small_overhang {int(rso)}  walls-only {a.walls_only}"
          f"  {radius_note or f'radius {a.radius:g} mm (given)'}")
    print(f"  overhanging samples {res['n_overhanging_samples']} = {res['overhanging_mm']} mm (depth > {a.depth_min:g} mm from the layer below; "
          f"{res['internal_bridge_samples_excluded']} internal-bridge samples excluded, {res.get('enclosed_region_samples_excluded', 0)} of them in "
          f"enclosed regions); sector centres {res.get('center') or res.get('centers')}")
    for nm, s in res.get("sectors", {}).items():
        print(f"  {nm:22s} {s}")
    for g in res["regions"][:12]:
        ws = g.get("worst_sector")
        worst_txt = f"  worst side {ws['sector']} {ws['supported_pct']} %" if ws else ""
        print(f"  region {g['mm']:7.1f} mm  z {g['z']}  {g['sector']:5s}  {g['kind']:21s} depth p50/p90/max {g['depth_p50']}/{g['depth_p90']}/{g['depth_max']}  supported {g['supported_pct']} %"
              f"{worst_txt}  {g['features']}{'  <- visible candidate' if g['visible_candidate'] else ''}")
    if len(res["regions"]) > 12:
        print(f"  ... {len(res['regions']) - 12} more regions in --json")
    for f in report["findings"]:
        print(f"  [{f['level']}] {f['msg']}")
    print(f"VERDICT: {report['verdict']}")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
