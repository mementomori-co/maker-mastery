r"""support_gap_readback.py - the printed support Top Z gap, read back from a sliced plate G-code.

Why: the number typed as Support > Advanced > Top Z distance (label not verified) is not always the gap printed. Tree Organic
rounds it to whole object layers, Tree Hybrid prints it exactly only where one support layer can be exactly that thick under a
flat ceiling, and inside a Height range Modifier the support layers snap to the object's layer grid and stack until they EXCEED
Top Z (TreeSupport.cpp v02.08.02.61 plan_layer_heights L4062-4088, https://github.com/bambulab/BambuStudio). This tool measures
what was sliced.

Method (a containment test):
  1. Every extruding move is kept per layer block ("; Z_HEIGHT:" = top of the extrusion, "; LAYER_HEIGHT:" = its thickness, "; FEATURE:",
     "; LINE_WIDTH:", object markers "; start/stop printing object, unique label id: N"); arcs are interpolated (tools\gcode_paths.py).
  2. Along every "Support interface" line, a sample every --sample mm. For each sample the layers above are walked in z order: if a layer
     within the continuity radius (default 0.6 x the MEASURED top-interface line pitch, floor 0.5 mm: Rectilinear Interlaced interface lines
     of the next layer lie half a pitch beside this layer's, about 0.37-0.45 mm at the 0.74-0.89 mm pitches measured so far, under the
     0.5 mm floor; --cont overrides) has Support / Support interface / Support transition at that XY, the sample is not the LAST
     interface and is dropped; else the first layer whose OBJECT material CONTAINS the sample (exact point-to-segment distance
     <= line width / 2; segments split to <= 1 mm and found through a KD-tree of their midpoints) gives the printed gap = (that layer's
     Z_HEIGHT - the matched segment's LAYER_HEIGHT) - the interface Z_HEIGHT. Nothing within --lookahead mm (3.0) = "no object above":
     normally the interface patch's own perimeter ring beyond the object footprint (a few percent; TreeSupport.cpp v02.08.02.61 L1805),
     reported as information, WARN above --no-object-warn.
     Known sensitivity: the shares of each gap value depend on the continuity radius AND the object-match tolerance. A tighter
     radius (for example --cont 0.21) misses the offset lines of the next interface layer and reads some gaps one interface layer
     too large; compare runs with the same settings only.
  3. Histogram of the gaps (0.001 mm bins) per object and per object layer height (the "range" the sample landed in), with the mode.
  4. Predicted modal gap from the stacking rule: the smallest whole number of object layers (of that layer height) whose summed height
     reaches Top Z (n*h >= Top Z - 1e-6 -> n*h). Exact-typed is also possible where Tree Hybrid + independent support layer height can make
     one support layer exactly Top Z thick. Both are printed.
  5. WARN when the measured mode differs from the typed Top Z by more than --tol (0.02 mm); the typed value comes from the G-code header
     ("; support_top_z_distance = ") or --top-z; per-object overrides from a --3mf's model_settings.config (support_top_z_distance).

Inputs: a plate G-code, or a sliced 3MF with --plate. Output: text report, optional --json file.
Usage:
  .venv\Scripts\python.exe tools\support_gap_readback.py <plate_N.gcode> [--3mf FILE.3mf] [--top-z 0.2]
      [--sample 0.5] [--cont 0.5] [--lookahead 3.0] [--tol 0.02] [--json out.json]
  or  ... --3mf FILE.3mf --plate N          (reads Metadata/plate_N.gcode from inside the 3MF; read-only)
Example: .venv\Scripts\python.exe tools\support_gap_readback.py --3mf work\slice\bracket\out.3mf --plate 1
Exit 0 = modes equal the typed Top Z (or support off), 1 = WARN (a mode differs, or no object above some interface), 3 = unreadable / usage.
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
import xml.etree.ElementTree as ET

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
DEFAULT_WIDTH = 0.42
SEG_MAX = 1.0        # mm: segments are split to this length so a KD-tree of midpoints bounds the exact point-to-segment search


def split_segment(ax, ay, bx, by, extra: tuple) -> list:
    n = max(1, int(math.ceil(math.hypot(bx - ax, by - ay) / SEG_MAX)))
    return [(ax + (bx - ax) * k / n, ay + (by - ay) * k / n, ax + (bx - ax) * (k + 1) / n, ay + (by - ay) * (k + 1) / n) + extra for k in range(n)]


class SegIndex:
    """Exact nearest point-to-segment distance for one layer's segments (split to <= SEG_MAX), via a KD-tree of midpoints."""

    def __init__(self, segs: list):
        self.seg = np.array([s[:4] for s in segs], dtype=float).reshape(-1, 4)
        self.extra = [s[4:] for s in segs]
        mid = np.c_[(self.seg[:, 0] + self.seg[:, 2]) / 2, (self.seg[:, 1] + self.seg[:, 3]) / 2]
        self.tree = cKDTree(mid)

    def nearest(self, q, radius: float):
        """(distance, index) of the nearest segment with its midpoint within radius + SEG_MAX/2 of q; (inf, -1) when none."""
        idx = self.tree.query_ball_point(q, radius + SEG_MAX / 2.0)
        if not idx:
            return float("inf"), -1
        s = self.seg[idx]
        vx, vy = s[:, 2] - s[:, 0], s[:, 3] - s[:, 1]
        L2 = vx * vx + vy * vy
        t = np.clip(((q[0] - s[:, 0]) * vx + (q[1] - s[:, 1]) * vy) / np.where(L2 > 0, L2, 1.0), 0.0, 1.0)
        d = np.hypot(s[:, 0] + t * vx - q[0], s[:, 1] + t * vy - q[1])
        k = int(np.argmin(d))
        return float(d[k]), idx[k]


# ----------------------------------------------------------------------------- G-code
def parse_gcode(fh) -> tuple[dict, dict]:
    """-> (header, layers). layers: {z_top: {"h": the block's OBJECT layer height (most common LAYER_HEIGHT of its non-Bridge object features; a
    Bridge block reports 0.4 = the nozzle diameter and Support blocks their own flow height), "obj": [(x0,y0,x1,y1, width, label, h_seg)],
    "sup": [(x0,y0,x1,y1)], "iface": [(x0, y0, x1, y1, label)], "pitch_pts": interface line sample points}}. header: the CONFIG block."""
    header: dict = {}
    layers: dict = collections.defaultdict(lambda: {"h": None, "hs": collections.Counter(), "obj": [], "sup": [], "iface": []})
    x = y = None
    z = None
    lh = None
    width = DEFAULT_WIDTH
    feat = None
    label = None
    in_config = False
    for line in fh:
        if line.startswith(";"):
            if line.startswith("; FEATURE:"):
                feat = line.split(":", 1)[1].strip()
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
            elif line.startswith("; LINE_WIDTH:"):
                try:
                    width = float(line.split(":", 1)[1])
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
        if d.get("E", 0) > 0 and ("X" in d or "Y" in d) and x is not None and y is not None and z is not None and feat not in (None, "Custom"):
            pts = [(x, y), (nx, ny)]
            if line.startswith(("G2 ", "G3 ")):
                try:
                    arc, _l, _c = arc_points(x, y, nx, ny, line.startswith("G2 "), d.get("I"), d.get("J"), d.get("R"), max_step=0.3)
                    pts = [(x, y)] + list(arc)
                except ValueError:
                    pass
            L = layers[z]
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                if feat in SUPPORT_FEATS:
                    L["sup"].extend(split_segment(ax, ay, bx, by, ()))
                    if feat == "Support interface":
                        L["iface"].append((ax, ay, bx, by, label))
                elif feat not in NON_OBJECT:
                    L["obj"].extend(split_segment(ax, ay, bx, by, (width, label, lh)))
                    if lh is not None and feat != "Bridge":          # Bridge blocks carry LAYER_HEIGHT 0.4 (nozzle diameter), not the layer
                        L["hs"][lh] += 1
        x, y = nx, ny
    for L in layers.values():
        L["h"] = L["hs"].most_common(1)[0][0] if L["hs"] else None
    return header, layers


def predicted_gaps(top_z: float, h: float) -> dict:
    """The stacking rule (TreeSupport.cpp v02.08.02.61 L4077-4086): support layers of the object's layer height accumulate until they
    reach Top Z -> n*h; plus the exact typed value where one support layer can be exactly Top Z thick (Tree Hybrid, independent layer height)."""
    if h is None or h <= 0:
        return {"stacked": None, "exact": round(top_z, 3), "n_layers": None}
    n = max(1, int(math.ceil(top_z / h - 1e-6)))
    return {"stacked": round(n * h, 3), "exact": round(top_z, 3), "n_layers": n}


def readback(header: dict, layers: dict, sample: float, cont: float, lookahead: float, box: tuple | None = None) -> dict:
    """box = (xmin, xmax, ymin, ymax) keeps only interface samples inside it (to compare with a zone-scoped project analysis); default whole plate."""
    zs = sorted(layers)
    obj_tree = {}
    sup_tree = {}
    for z in zs:
        L = layers[z]
        if L["obj"]:
            obj_tree[z] = SegIndex(L["obj"])
        if L["sup"]:
            sup_tree[z] = SegIndex(L["sup"])
    gaps = []          # (gap, h_above, label_iface, label_obj, z_iface, z_above)
    no_object = 0
    not_last = 0
    n_samples = 0
    for zi, z in enumerate(zs):
        L = layers[z]
        if not L["iface"]:
            continue
        for (ax, ay, bx, by, lab) in L["iface"]:
            n = max(1, int(math.hypot(bx - ax, by - ay) / sample))
            for k in range(n + 1):
                q = (ax + (bx - ax) * k / n, ay + (by - ay) * k / n)
                if box is not None and not (box[0] <= q[0] <= box[1] and box[2] <= q[1] <= box[3]):
                    continue
                n_samples += 1
                found = None
                for z2 in zs[zi + 1:]:
                    if z2 - z > lookahead:
                        break
                    if z2 in sup_tree and sup_tree[z2].nearest(q, cont)[0] <= cont:
                        found = "not_last"
                        break
                    if z2 in obj_tree:
                        dist, idx = obj_tree[z2].nearest(q, DEFAULT_WIDTH)
                        if idx >= 0 and dist <= obj_tree[z2].extra[idx][0] / 2.0:
                            seg_h = obj_tree[z2].extra[idx][2]
                            # the matched segment's own LAYER_HEIGHT, except a Bridge (0.4 = nozzle diameter) -> the block's object layer height
                            h2 = seg_h if (seg_h is not None and abs(seg_h - 0.4) > 1e-9) else layers[z2]["h"]
                            gaps.append((round((z2 - (h2 or 0.0)) - z, 3), h2, lab, obj_tree[z2].extra[idx][1], z, z2))
                            found = "gap"
                            break
                if found == "not_last":
                    not_last += 1
                elif found is None:
                    no_object += 1
    return {"gaps": gaps, "n_samples": n_samples, "not_last": not_last, "no_object_above": no_object,
            "object_layer_heights": sorted({L["h"] for L in layers.values() if L["h"] is not None})}


def interface_pitch(layers: dict) -> float | None:
    """Median perpendicular pitch of parallel Support interface lines (nearest neighbour on each side, same direction), over the top interface
    layers. None when there is no interface."""
    vals = []
    for z in sorted(layers, reverse=True):
        I = layers[z]["iface"]
        if len(I) < 4:
            continue
        S = np.array([(s[0], s[1], s[2], s[3]) for s in I], dtype=float)
        d = S[:, 2:4] - S[:, :2]
        L = np.hypot(d[:, 0], d[:, 1])
        keep = L > 1.0
        if keep.sum() < 4:
            continue
        S, d, L = S[keep], d[keep], L[keep]
        u = d / L[:, None]
        mid = (S[:, :2] + S[:, 2:4]) / 2.0
        tree = cKDTree(mid)
        for k in range(len(mid)):
            idx = [j for j in tree.query_ball_point(mid[k], 3.0) if j != k and abs(float(u[j] @ u[k])) > 0.95]
            if not idx:
                continue
            nrm = np.array([-u[k][1], u[k][0]])
            off = np.abs((mid[idx] - mid[k]) @ nrm)
            off = off[off > 0.1]
            if len(off):
                vals.append(float(off.min()))
        if len(vals) >= 200:
            break
    return round(float(np.median(vals)), 3) if vals else None


def histogram(vals: list) -> list:
    c = collections.Counter(vals)
    n = sum(c.values()) or 1
    return [{"gap_mm": g, "n": k, "share": round(k / n, 3)} for g, k in sorted(c.items(), key=lambda kv: -kv[1])]


# ----------------------------------------------------------------------------- 3MF helpers
def object_top_z_overrides(path3mf: str) -> tuple[dict, dict]:
    """{object name: support_top_z_distance override} from model_settings.config and {identify_id: name} from slice_info.config."""
    names, overrides = {}, {}
    try:
        with zipfile.ZipFile(path3mf) as z:
            try:
                si = ET.fromstring(z.read("Metadata/slice_info.config"))
                for o in si.iter("object"):
                    if o.get("identify_id") and o.get("name"):
                        names[int(o.get("identify_id"))] = o.get("name")
            except KeyError:
                pass
            ms = ET.fromstring(z.read("Metadata/model_settings.config"))
            for ob in ms.iter("object"):
                meta = {m.get("key"): m.get("value") for m in ob.findall("metadata") if m.get("key")}
                if "support_top_z_distance" in meta and meta.get("name"):
                    overrides[meta["name"]] = float(meta["support_top_z_distance"])
    except (KeyError, OSError, zipfile.BadZipFile, ET.ParseError):
        pass
    return overrides, names


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gcode", nargs="?", help="plate G-code file (or give --3mf with --plate)")
    ap.add_argument("--3mf", dest="three", default=None, help="sliced 3MF: per-object Top Z overrides and object names; with --plate also the G-code source")
    ap.add_argument("--plate", type=int, default=None)
    ap.add_argument("--top-z", type=float, default=None, help="typed Top Z (default: the G-code header's support_top_z_distance)")
    ap.add_argument("--sample", type=float, default=0.5)
    ap.add_argument("--cont", type=float, default=None, help="support continuity radius: a support line this close in a layer above means 'not the last interface'; default 0.6 x the measured top-interface pitch, floor 0.5 mm (at the 0.74-0.89 mm pitches measured so far the floor applies)")
    ap.add_argument("--no-object-warn", type=float, default=0.25, help="WARN when more than this share of last-interface samples has no object above (house value; the interface patch's own perimeter ring normally gives about 5 %%)")
    ap.add_argument("--lookahead", type=float, default=3.0)
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--box", default=None, metavar="xmin,xmax,ymin,ymax", help="only interface samples inside this plate-XY box (to compare with a zone-scoped analysis)")
    ap.add_argument("--json", default=None)
    try:
        a = ap.parse_args(argv[1:])
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    try:
        if a.gcode:
            with open(a.gcode, encoding="utf-8", errors="ignore") as fh:
                header, layers = parse_gcode(fh)
            src = a.gcode
        elif a.three and a.plate:
            with zipfile.ZipFile(a.three) as z:
                data = z.read(f"Metadata/plate_{a.plate}.gcode")
            header, layers = parse_gcode(io.StringIO(data.decode("utf-8", "ignore")))
            src = f"{a.three}::Metadata/plate_{a.plate}.gcode"
        else:
            print("usage: give a plate G-code, or --3mf FILE --plate N", file=sys.stderr)
            return 3
    except (OSError, KeyError, zipfile.BadZipFile) as e:
        print(f"cannot read the input: {e}", file=sys.stderr)
        return 3
    overrides, names = object_top_z_overrides(a.three) if a.three else ({}, {})
    try:
        top_z = a.top_z if a.top_z is not None else float(header.get("support_top_z_distance", "nan"))
    except ValueError:
        top_z = float("nan")
    box = None
    if a.box:
        try:
            box = tuple(float(v) for v in a.box.split(","))
            assert len(box) == 4
        except Exception:  # noqa: BLE001
            print("usage: --box expects xmin,xmax,ymin,ymax", file=sys.stderr)
            return 3
    # continuity radius: 0.6 x the measured top-interface line pitch, floor 0.5 mm, unless --cont is given explicitly
    pitch = interface_pitch(layers)
    cont = a.cont if a.cont is not None else (max(0.5, round(0.6 * pitch, 3)) if pitch else 0.5)
    rb = readback(header, layers, a.sample, cont, a.lookahead, box)
    gaps = rb["gaps"]
    report = {"file": src, "box": list(box) if box else None, "typed_top_z": top_z if not math.isnan(top_z) else None,
              "interface_pitch_mm": pitch, "continuity_radius_mm": cont, "continuity_source": "--cont" if a.cont is not None else "0.6 x measured interface pitch, floor 0.5",
              "header": {k: header.get(k) for k in ("support_top_z_distance", "support_interface_top_layers", "support_interface_spacing", "support_interface_filament",
                                                   "support_type", "support_style", "independent_support_layer_height", "enable_prime_tower", "layer_height",
                                                   "enable_support", "support_remove_small_overhang", "timelapse_type", "enable_wrapping_detection")},
              "n_interface_samples": rb["n_samples"], "not_last_interface": rb["not_last"], "no_object_above": rb["no_object_above"],
              "object_layer_heights": rb["object_layer_heights"], "overall": histogram([g[0] for g in gaps]), "by_layer_height": {}, "by_object": {}, "findings": []}

    def shares(vals: list, typed: float | None) -> dict:
        """tighter / at / looser than the typed value (+- tol): a two-humped histogram is not summarised by its mode alone."""
        if typed is None or math.isnan(typed) or not vals:
            return {}
        v = np.array(vals)
        return {"tighter": round(float((v < typed - a.tol).mean()), 3), "at_typed": round(float((np.abs(v - typed) <= a.tol).mean()), 3), "looser": round(float((v > typed + a.tol).mean()), 3)}

    for h in sorted({g[1] for g in gaps if g[1] is not None}):
        vals = [g[0] for g in gaps if g[1] == h]
        pred = predicted_gaps(top_z, h) if not math.isnan(top_z) else {"stacked": None, "exact": None, "n_layers": None}
        report["by_layer_height"][str(h)] = {"n": len(vals), "histogram": histogram(vals)[:8], "mode": histogram(vals)[0]["gap_mm"] if vals else None, "predicted": pred,
                                             "shares": shares(vals, top_z)}
    labels = sorted({g[3] for g in gaps if g[3] is not None} | {g[2] for g in gaps if g[2] is not None}, key=lambda v: (v is None, v))
    if gaps and not labels:
        # no "; start printing object" markers in this G-code (label objects off, or one object): judge the plate as one object
        labels = [-1]
        gaps = [(g[0], g[1], -1, -1, g[4], g[5]) for g in gaps]
        names = {-1: "(whole plate: no object labels in the G-code)"}
    for lab in labels:
        vals = [g[0] for g in gaps if g[3] == lab]
        if not vals:
            continue
        name = names.get(lab)
        typed = overrides.get(name, top_z) if name else top_z
        hist = histogram(vals)
        hs = sorted({g[1] for g in gaps if g[3] == lab and g[1] is not None})
        report["by_object"][str(lab)] = {"name": name, "typed_top_z": typed, "n": len(vals), "mode": hist[0]["gap_mm"], "histogram": hist[:6], "shares": shares(vals, typed),
                                         "layer_heights": hs, "predicted": {str(h): predicted_gaps(typed, h) for h in hs} if typed is not None and not math.isnan(typed) else {}}
        if typed is not None and not math.isnan(typed) and abs(hist[0]["gap_mm"] - typed) > a.tol:
            stacked = [predicted_gaps(typed, h)["stacked"] for h in hs]
            report["findings"].append({"level": "WARN", "msg": f"object {lab} {name!r}: printed Top Z mode {hist[0]['gap_mm']} mm on {hist[0]['share']:.0%} of {len(vals)} samples "
                                                               f"vs typed {typed} mm (layer heights {hs}; stacking rule predicts {stacked}; histogram {hist[:4]})"})
    if not gaps and rb["n_samples"] == 0:
        report["findings"].append({"level": "OK", "msg": "no Support interface in this plate (support off or nothing needed support)"})
    if rb["no_object_above"]:
        share = rb["no_object_above"] / max(rb["n_samples"], 1)
        txt = (f"{rb['no_object_above']} of {rb['n_samples']} last-interface samples ({share:.1%}) have no object material within {a.lookahead} mm above: the interface patch's own "
               f"perimeter ring beyond the object footprint (about one XY distance out; TreeSupport.cpp v02.08.02.61 L1805), normally a few percent")
        if share > a.no_object_warn:
            report["findings"].append({"level": "WARN", "msg": txt + f" - above the {a.no_object_warn:.0%} house threshold: support under nothing (tree tops, a dropped roof, brim contacts)?"})
        else:
            report["findings"].append({"level": "OK", "msg": txt})
    if gaps and not [f for f in report["findings"] if f["level"] == "WARN"]:
        report["findings"].append({"level": "OK", "msg": f"every object's printed Top Z mode equals its typed value within {a.tol} mm ({len(gaps)} samples)"})
    report["verdict"] = "WARN" if any(f["level"] == "WARN" for f in report["findings"]) else "OK"
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1)
    print(f"support_gap_readback: {src}")
    print(f"  typed Top Z {report['typed_top_z']}  style {header.get('support_style')}  type {header.get('support_type')}  independent {header.get('independent_support_layer_height')}  prime tower {header.get('enable_prime_tower')}  object layer heights {rb['object_layer_heights']}")
    print(f"  interface pitch {pitch} mm -> continuity radius {cont} mm ({report['continuity_source']})")
    print(f"  interface samples {rb['n_samples']}: {len(gaps)} with an object above, {rb['not_last']} not the last interface, {rb['no_object_above']} with nothing above")
    for h, v in report["by_layer_height"].items():
        print(f"  layer height {h}: mode {v['mode']} mm, shares {v['shares']}, predicted stacked {v['predicted']['stacked']} / exact {v['predicted']['exact']}; {v['histogram'][:5]}")
    for lab, v in report["by_object"].items():
        print(f"  object {lab} {v['name']!r}: typed {v['typed_top_z']} -> mode {v['mode']} mm ({v['n']} samples) shares {v['shares']} {v['histogram'][:4]}")
    for f in report["findings"]:
        print(f"  [{f['level']}] {f['msg']}")
    print(f"VERDICT: {report['verdict']}")
    return 1 if report["verdict"] == "WARN" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
