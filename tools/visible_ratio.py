r"""visible_ratio.py - "visible-part ratio by layer": how much of a sliced print's part can still be SEEN through its support.

Why: a tree-support cage can pass every coverage, scar and grams check and still hide the whole sculpture from a viewer (one
measured case: about 312 g of support around a 628 g part). A print's purpose is a pass criterion; for a display or stream
print this ratio is that criterion.

What it does (read-only on the G-code, nothing is printed or sent anywhere):
  1. Reads the plate G-code with tools\gcode_paths.py (arc-aware: G2/G3 interpolated; a reader that skips arcs loses
     whole wall loops). Per layer: z from "; Z_HEIGHT", height from "; LAYER_HEIGHT" (else the z step).
  2. PART = features Outer wall, Overhang wall, Inner wall (+ Floating vertical shell, the slicer's thin-wall role);
     SUPPORT = features Support, Support interface, Support transition. Everything else (infill, brim, skirt, tower, travel)
     is ignored. Both lists can be changed with --part-features / --support-features.
  3. Rasterises the layer stack with a z-buffer, ORTHOGRAPHIC camera, 5 px/mm (--px-per-mm). Every extrusion segment is
     sampled every 0.15 mm along its length, at 3 lateral offsets (-w/2, 0, +w/2, w = LINE_WIDTH, default 0.42) and 2 heights
     inside the layer (z - 0.25 h, z - 0.75 h); each sample is a 3D point, projected to the screen, its depth along the view
     axis written into one z-buffer for the part and one for the support (nearest = largest depth).
  4. A part pixel is HIDDEN when the support z-buffer is closer to the camera than the part's nearest sample by more than
     --eps-mm (0.2 mm). Visible ratio = part pixels not hidden / part pixels (a pixel counts once, however many walls cover it).
  5. The stack is cumulative: at a checkpoint only layers up to that z exist, so the ratio at 25/50/75 % height is what a viewer
     sees WHILE the print grows (checkpoint = the first layer with z >= fraction x top z; the last checkpoint is the final layer).
  6. Cameras (right-handed, looking at the print; c = direction from the print to the camera, depth = p . c):
       front: c = (0, -1, 0)  screen right = +X, up = +Z   (the printer front; the viewer stands at -Y)
       iso:   c = (sin az cos el, -cos az cos el, sin el), right = (cos az, sin az, 0), up = (-sin az sin el, cos az sin el, cos el)
              with --az 35 --el 30 degrees (front-right-above). G-code X/Y are the plate frame.
  7. --face-mask FILE.json restricts a second ratio to a face region:
       {"masks": [{"name": "face", "box": {"min": [x, y, z], "max": [x, y, z]}},
                  {"name": "face-front", "view": "front", "polygon": [[u, v], [u, v], ...]}]}
     "box" is a box in G-code (plate) coordinates in mm: the face pixels of a view are the pixels whose NEAREST part sample lies
     inside the box (a face behind the rest of the part is not counted). "polygon" is in screen millimetres of the named view
     (front: u = X, v = Z); its face pixels are the part pixels inside it. The face ratio uses the same checkpoints.
  8. Verdict: FAIL when the final visible ratio of any view (or any face mask) is below --fail (default 0.60), WARN when below
     --warn (default 0.80), else OK. The worst view decides. The thresholds are PROPOSED defaults, calibrated on one heavy
     tree-support cage and one support-free plate, not verified limits.
Exit codes: 0 OK, 1 WARN, 2 FAIL, 3 unreadable input / no part pixels / bad arguments.

Outputs: <out-prefix>-front.png, <out-prefix>-iso.png (white background; part visible = grey, part hidden behind support =
BLUE, support that covers no part pixel = RED) and <out-prefix>.json (all numbers). Default out-prefix
<repo>\work\visible_ratio\<gcode stem>-plate<N> (override with --out-prefix; --json FILE sets the JSON path alone).

Known limits (also printed in the JSON "limits"):
  - Only extrusion lines are drawn (a 3D box per line sampled as points, not a mesh): a part pixel with no wall sample counts
    as "no part" even if the printed object has a top surface or infill there.
  - Interior walls that are never visible still count as part pixels when no outer wall is in front of them in the same pixel;
    the pixel is then covered by the part anyway, so it is a part pixel, not an error.
  - Support is judged by depth only; thin or sparse support that a viewer can look through is counted as a full block
    (the rasterisation fills every line to its width): a see-through lattice reads as hidden at its line pitch only where
    its lines touch, which is the physically visible case at 5 px/mm.
  - Brim, skirt, raft and prime tower are ignored on purpose.
CLI: .venv\Scripts\python.exe -B tools\visible_ratio.py <plate.gcode | file.3mf> [--plate N] [options]
Example: .venv\Scripts\python.exe -B tools\visible_ratio.py work\slice\figure\plate_1.gcode --out-prefix work\visible_ratio\figure-plate1
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import struct
import sys
import time
import zlib

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gcode_paths  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the repository folder
PART_FEATURES = ("Outer wall", "Overhang wall", "Inner wall", "Floating vertical shell")
SUPPORT_FEATURES = ("Support", "Support interface", "Support transition")
DEFAULT_WIDTH = 0.42
SAMPLE_STEP = 0.15           # mm along a segment
LATERAL = (-0.5, 0.0, 0.5)   # fractions of the line width
VERTICAL = (0.25, 0.75)      # depth below the layer top, fractions of the layer height
NEG = np.float32(-1e30)
LIMITS = [
    "Only extrusion lines are rasterised (point samples of each line's box), not a mesh.",
    "Brim, skirt, raft, prime tower, infill, bridge and surfaces are ignored.",
    "Support is judged by depth only, filled to its line width.",
    "Thresholds are proposed defaults, not verified limits.",
]


class InputError(Exception):
    pass


# ---------------------------------------------------------------- reading
def _flatten(paths, default_h):
    """-> (P0 (n,2), P1 (n,2), width (n,)) for all segments of the paths, or None."""
    paths = [p for p in paths if len(p.pts) >= 2]
    if not paths:
        return None
    pts = np.array(list(itertools.chain.from_iterable(p.pts for p in paths)), dtype=np.float64)
    lens = np.array([len(p.pts) for p in paths])
    starts = np.cumsum(lens) - lens
    valid = np.ones(len(pts) - 1, dtype=bool)
    valid[starts[1:] - 1] = False
    widths = np.repeat(np.array([(p.width or DEFAULT_WIDTH) for p in paths], dtype=np.float64), lens)[:-1]
    return pts[:-1][valid], pts[1:][valid], widths[valid]


def load_stack(src, plate, part_feats, sup_feats):
    """-> list of layers [{z, h, part: (P0,P1,w)|None, sup: (P0,P1,w)|None}] ascending by z, plus the parse stats."""
    try:
        parsed = gcode_paths.parse(src, arcs="interpolate", plate=plate)
    except (OSError, KeyError, ValueError) as e:
        raise InputError(f"cannot read {src}: {e}") from e
    part_set, sup_set = set(part_feats), set(sup_feats)
    layers = []
    prev_z = 0.0
    for L in parsed.layers:
        if L.z is None:
            continue
        h = L.height if (L.height and L.height > 0) else (L.z - prev_z if L.z > prev_z else 0.2)
        part = [p for p in L.paths if p.feature in part_set]
        sup = [p for p in L.paths if p.feature in sup_set]
        layers.append({"z": float(L.z), "h": float(h), "part": _flatten(part, h), "sup": _flatten(sup, h)})
        prev_z = L.z
    stats = dict(parsed.stats)
    n_layers = len(parsed.layers)
    del parsed
    if not layers:
        raise InputError(f"{src}: no layers with a Z_HEIGHT found")
    return layers, stats, n_layers


# ---------------------------------------------------------------- cameras
def camera(name, az_deg, el_deg):
    if name == "front":
        c, r, u = (0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)
    elif name == "iso":
        az, el = math.radians(az_deg), math.radians(el_deg)
        c = (math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))
        r = (math.cos(az), math.sin(az), 0.0)
        u = (-math.sin(az) * math.sin(el), math.cos(az) * math.sin(el), math.cos(el))
    else:
        raise InputError(f"unknown view {name!r} (front, iso)")
    return {"name": name, "c": np.array(c), "r": np.array(r), "u": np.array(u)}


class View:
    def __init__(self, cam, bbox, px_per_mm, margin):
        self.cam, self.S = cam, px_per_mm
        (x0, y0, z0), (x1, y1, z1) = bbox
        corners = np.array([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)])
        us, vs = corners @ cam["r"], corners @ cam["u"]
        self.u0, self.v0 = us.min() - margin, vs.min() - margin
        self.W = int(math.ceil((us.max() + margin - self.u0) * px_per_mm)) + 1
        self.H = int(math.ceil((vs.max() + margin - self.v0) * px_per_mm)) + 1
        if self.W * self.H > 80_000_000:
            raise InputError(f"raster {self.W} x {self.H} px is too large; lower --px-per-mm")
        self.dpart = np.full(self.H * self.W, NEG, dtype=np.float32)
        self.dsup = np.full(self.H * self.W, NEG, dtype=np.float32)
        self.dface = {}                     # mask name -> z-buffer of part samples inside the box

    def project(self, pts):
        cam = self.cam
        iu = np.floor((pts @ cam["r"] - self.u0) * self.S).astype(np.int64)
        iv = np.floor((pts @ cam["u"] - self.v0) * self.S).astype(np.int64)
        np.clip(iu, 0, self.W - 1, out=iu)
        np.clip(iv, 0, self.H - 1, out=iv)
        return iv * self.W + iu, (pts @ cam["c"]).astype(np.float32)


def stamp(view, seg, z, h, buf, boxes=None, block=60000):
    """Write the nearest depth of every sample of the segments into buf (and into the face buffers for boxes)."""
    P0, P1, w = seg
    for b0 in range(0, len(P0), block):
        a0, a1, ww = P0[b0:b0 + block], P1[b0:b0 + block], w[b0:b0 + block]
        d = a1 - a0
        ln = np.hypot(d[:, 0], d[:, 1])
        n = np.maximum(1, np.ceil(ln / SAMPLE_STEP).astype(np.int64))
        seg_i = np.repeat(np.arange(len(a0)), n)
        k = np.arange(n.sum()) - np.repeat(np.cumsum(n) - n, n)
        t = (k + 0.5) / n[seg_i]
        q = a0[seg_i] + d[seg_i] * t[:, None]
        with np.errstate(invalid="ignore", divide="ignore"):
            nx = np.where(ln[seg_i] > 0, -d[seg_i, 1] / ln[seg_i], 0.0)
            ny = np.where(ln[seg_i] > 0, d[seg_i, 0] / ln[seg_i], 0.0)
        wi = ww[seg_i]
        for lat in LATERAL:
            px = q[:, 0] + lat * wi * nx
            py = q[:, 1] + lat * wi * ny
            for vf in VERTICAL:
                pts = np.stack([px, py, np.full(len(px), z - vf * h)], axis=1)
                pix, dep = view.project(pts)
                np.maximum.at(buf, pix, dep)
                if boxes:
                    for name, (lo, hi) in boxes.items():
                        inside = np.all((pts >= lo) & (pts <= hi), axis=1)
                        if inside.any():
                            np.maximum.at(view.dface[name], pix[inside], dep[inside])


# ---------------------------------------------------------------- masks
def load_masks(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as e:
        raise InputError(f"cannot read face mask {path}: {e}") from e
    masks = []
    for i, m in enumerate(data.get("masks", [])):
        name = str(m.get("name", f"mask{i + 1}"))
        if "box" in m:
            lo, hi = m["box"]["min"], m["box"]["max"]
            if len(lo) != 3 or len(hi) != 3 or any(a > b for a, b in zip(lo, hi)):
                raise InputError(f"mask {name}: box min/max must be 3 numbers each with min <= max")
            masks.append({"name": name, "kind": "box", "lo": np.array(lo, float), "hi": np.array(hi, float)})
        elif "polygon" in m:
            poly = np.array(m["polygon"], float)
            if poly.ndim != 2 or poly.shape[1] != 2 or len(poly) < 3:
                raise InputError(f"mask {name}: polygon needs >= 3 [u, v] points")
            masks.append({"name": name, "kind": "polygon", "view": m.get("view"), "poly": poly})
        else:
            raise InputError(f"mask {name}: needs 'box' or 'polygon'")
    if not masks:
        raise InputError(f"face mask {path}: no masks")
    return masks


def polygon_pixels(view, poly):
    """Boolean raster (H*W) of the pixels whose centre lies inside the polygon (screen mm of the view; even-odd rule)."""
    mask = np.zeros(view.H * view.W, dtype=bool)
    ix0 = max(0, int(math.floor((poly[:, 0].min() - view.u0) * view.S)))
    ix1 = min(view.W - 1, int(math.ceil((poly[:, 0].max() - view.u0) * view.S)))
    iy0 = max(0, int(math.floor((poly[:, 1].min() - view.v0) * view.S)))
    iy1 = min(view.H - 1, int(math.ceil((poly[:, 1].max() - view.v0) * view.S)))
    if ix1 < ix0 or iy1 < iy0:
        return mask
    xs = view.u0 + (np.arange(ix0, ix1 + 1) + 0.5) / view.S
    ys = view.v0 + (np.arange(iy0, iy1 + 1) + 0.5) / view.S
    gx, gy = np.meshgrid(xs, ys)
    inside = np.zeros(gx.shape, dtype=bool)
    n = len(poly)
    for i in range(n):
        xa, ya = poly[i]
        xb, yb = poly[(i + 1) % n]
        if ya == yb:
            continue
        cond = (ya > gy) != (yb > gy)
        xint = xa + (gy - ya) * (xb - xa) / (yb - ya)
        inside ^= cond & (gx < xint)
    full = np.zeros((view.H, view.W), dtype=bool)
    full[iy0:iy1 + 1, ix0:ix1 + 1] = inside
    return full.reshape(-1)


# ---------------------------------------------------------------- measuring
def measure(view, eps, masks):
    pp = view.dpart > NEG
    hid = pp & (view.dsup > view.dpart + np.float32(eps))
    n_part = int(pp.sum())
    out = {"part_px": n_part, "hidden_px": int(hid.sum()),
           "visible_ratio": None if n_part == 0 else round(1.0 - hid.sum() / n_part, 4), "faces": []}
    for m in masks:
        if m["kind"] == "box":
            df = view.dface[m["name"]]
            fm = pp & (df > NEG) & (df >= view.dpart - np.float32(0.05))
        else:
            if m.get("view") not in (None, view.cam["name"]):
                continue
            fm = pp & polygon_pixels(view, m["poly"])
        nf = int(fm.sum())
        nh = int((fm & hid).sum())
        out["faces"].append({"name": m["name"], "face_px": nf, "hidden_px": nh,
                             "visible_ratio": None if nf == 0 else round(1.0 - nh / nf, 4)})
    return out


def write_png(path, rgb):
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + rgb[r].tobytes() for r in range(h))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(png)


def image_of(view, eps):
    pp = (view.dpart > NEG).reshape(view.H, view.W)
    sp = (view.dsup > NEG).reshape(view.H, view.W)
    hid = (pp.reshape(-1) & (view.dsup > view.dpart + np.float32(eps))).reshape(view.H, view.W)
    img = np.full((view.H, view.W, 3), 255, dtype=np.uint8)
    img[pp] = (150, 150, 150)
    img[sp] = (220, 40, 40)
    img[hid] = (30, 80, 230)
    return np.ascontiguousarray(img[::-1])        # v up -> row 0 at the top


# ---------------------------------------------------------------- main run
def analyse(src, plate=1, views=("front", "iso"), px_per_mm=5.0, fractions=(0.25, 0.5, 0.75), eps=0.2,
            az=35.0, el=30.0, masks=None, part_feats=PART_FEATURES, sup_feats=SUPPORT_FEATURES,
            out_prefix=None, progress=False):
    t0 = time.time()
    layers, stats, n_layer_markers = load_stack(src, plate, part_feats, sup_feats)
    if progress:
        print(f"visible_ratio: parsed {len(layers)} layers in {time.time() - t0:.0f} s", file=sys.stderr)
    xy = [np.concatenate([s[0], s[1]]) for L in layers for s in (L["part"], L["sup"]) if s is not None]
    if not xy or all(L["part"] is None for L in layers):
        raise InputError(f"{src}: no part extrusion (features {', '.join(part_feats)}) found")
    xy = np.concatenate(xy)
    ztop = max(L["z"] for L in layers)
    bbox = ((xy[:, 0].min() - 1.0, xy[:, 1].min() - 1.0, 0.0), (xy[:, 0].max() + 1.0, xy[:, 1].max() + 1.0, ztop))
    cps = []
    for f in fractions:
        idx = next((i for i, L in enumerate(layers) if L["z"] >= f * ztop - 1e-6), len(layers) - 1)
        cps.append((f, idx))
    cps.append((1.0, len(layers) - 1))
    cp_at = {}
    for f, idx in cps:
        cp_at.setdefault(idx, []).append(f)
    boxes_def = {m["name"]: (m["lo"], m["hi"]) for m in (masks or []) if m["kind"] == "box"}
    result = {"gcode": src, "plate": plate, "layers": len(layers), "layer_change_markers": n_layer_markers,
              "z_top_mm": round(ztop, 3), "px_per_mm": px_per_mm, "eps_mm": eps,
              "part_features": list(part_feats), "support_features": list(sup_feats),
              "camera": {"front": "c=(0,-1,0)", "iso": f"az={az} el={el} deg"}, "views": {}, "limits": LIMITS,
              "gcode_paths_stats": {k: v for k, v in stats.items() if k.startswith("arcs") or k.startswith("extruding_arcs")}}
    for vname in views:
        view = View(camera(vname, az, el), bbox, px_per_mm, margin=1.0)
        for name in boxes_def:
            view.dface[name] = np.full(view.H * view.W, NEG, dtype=np.float32)
        checkpoints = []
        for i, L in enumerate(layers):
            if L["part"] is not None:
                stamp(view, L["part"], L["z"], L["h"], view.dpart, boxes_def)
            if L["sup"] is not None:
                stamp(view, L["sup"], L["z"], L["h"], view.dsup)
            for f in cp_at.get(i, []):
                m = measure(view, eps, masks or [])
                m.update({"fraction": f, "layer_index": i, "z_mm": round(L["z"], 3)})
                checkpoints.append(m)
            if progress and i % 200 == 0:
                print(f"visible_ratio: {vname} layer {i}/{len(layers)} ({time.time() - t0:.0f} s)", file=sys.stderr)
        checkpoints.sort(key=lambda c: c["fraction"])
        final = checkpoints[-1]
        if final["part_px"] == 0:
            raise InputError(f"{src}: no part pixels in the {vname} view")
        entry = {"final_visible_ratio": final["visible_ratio"], "checkpoints": checkpoints,
                 "face": final["faces"], "image": None}
        if out_prefix:
            p = f"{out_prefix}-{vname}.png"
            write_png(p, image_of(view, eps))
            entry["image"] = p
        result["views"][vname] = entry
    result["elapsed_s"] = round(time.time() - t0, 1)
    return result


def verdict_of(result, fail, warn, face_fail, face_warn):
    level, reasons = 0, []
    for vname, v in result["views"].items():
        r = v["final_visible_ratio"]
        if r < fail:
            level = max(level, 2); reasons.append(f"{vname}: final visible ratio {r} < FAIL {fail}")
        elif r < warn:
            level = max(level, 1); reasons.append(f"{vname}: final visible ratio {r} < WARN {warn}")
        for f in v["face"]:
            fr = f["visible_ratio"]
            if fr is None:
                level = max(level, 1); reasons.append(f"{vname}: face '{f['name']}' has no part pixels (mask misses the part)")
            elif fr < face_fail:
                level = max(level, 2); reasons.append(f"{vname}: face '{f['name']}' visible ratio {fr} < FAIL {face_fail}")
            elif fr < face_warn:
                level = max(level, 1); reasons.append(f"{vname}: face '{f['name']}' visible ratio {fr} < WARN {face_warn}")
    return ("OK", "WARN", "FAIL")[level], reasons


def main(argv):
    ap = argparse.ArgumentParser(description="Share of the part's outer-wall pixels not hidden behind support, per layer height.")
    ap.add_argument("gcode", help="plate_N.gcode or a sliced .3mf")
    ap.add_argument("--plate", type=int, default=1)
    ap.add_argument("--views", default="front,iso")
    ap.add_argument("--px-per-mm", type=float, default=5.0)
    ap.add_argument("--fractions", default="0.25,0.5,0.75")
    ap.add_argument("--eps-mm", type=float, default=0.2)
    ap.add_argument("--az", type=float, default=35.0)
    ap.add_argument("--el", type=float, default=30.0)
    ap.add_argument("--fail", type=float, default=0.60, help="FAIL below this final visible ratio (proposed default)")
    ap.add_argument("--warn", type=float, default=0.80, help="WARN below this final visible ratio (proposed default)")
    ap.add_argument("--face-mask", default=None, help="JSON file of face boxes / polygons (see the docstring)")
    ap.add_argument("--face-fail", type=float, default=None, help="default = --fail")
    ap.add_argument("--face-warn", type=float, default=None, help="default = --warn")
    ap.add_argument("--part-features", default=",".join(PART_FEATURES))
    ap.add_argument("--support-features", default=",".join(SUPPORT_FEATURES))
    ap.add_argument("--out-prefix", default=None, help=r"default <repo>\work\visible_ratio\<stem>-plate<N>")
    ap.add_argument("--json", default=None, help="JSON path (default <out-prefix>.json)")
    ap.add_argument("--no-png", action="store_true")
    try:
        a = ap.parse_args(argv[1:])
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    try:
        if not (0.0 <= a.fail <= a.warn <= 1.0):
            raise InputError("need 0 <= --fail <= --warn <= 1")
        views = tuple(v.strip() for v in a.views.split(",") if v.strip())
        fractions = tuple(float(f) for f in a.fractions.split(",") if f.strip())
        stem = os.path.splitext(os.path.basename(a.gcode))[0]
        prefix = a.out_prefix or os.path.join(BRAIN, "work", "visible_ratio", f"{stem}-plate{a.plate}")
        masks = load_masks(a.face_mask) if a.face_mask else None
        res = analyse(a.gcode, a.plate, views, a.px_per_mm, fractions, a.eps_mm, a.az, a.el, masks,
                      tuple(s.strip() for s in a.part_features.split(",") if s.strip()),
                      tuple(s.strip() for s in a.support_features.split(",") if s.strip()),
                      None if a.no_png else prefix, progress=True)
    except (InputError, ValueError) as e:
        print(f"visible_ratio: INPUT ERROR: {e}", file=sys.stderr)
        return 3
    ff = a.face_fail if a.face_fail is not None else a.fail
    fw = a.face_warn if a.face_warn is not None else a.warn
    verdict, reasons = verdict_of(res, a.fail, a.warn, ff, fw)
    res["thresholds"] = {"fail": a.fail, "warn": a.warn, "face_fail": ff, "face_warn": fw}
    res["verdict"], res["reasons"] = verdict, reasons
    jpath = a.json or f"{prefix}.json"
    os.makedirs(os.path.dirname(os.path.abspath(jpath)), exist_ok=True)
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print(f"visible_ratio: {a.gcode} plate {a.plate}: {res['layers']} layers, z top {res['z_top_mm']} mm, {res['elapsed_s']} s")
    for vname, v in res["views"].items():
        cps = "  ".join(f"{int(c['fraction'] * 100)}% (z {c['z_mm']}) {c['visible_ratio']}" for c in v["checkpoints"])
        print(f"  {vname:5s} visible ratio by height: {cps}")
        for f in v["face"]:
            print(f"        face '{f['name']}': final {f['visible_ratio']} ({f['face_px']} px)")
        if v["image"]:
            print(f"        image {v['image']}  (grey = visible part, BLUE = part hidden behind support, RED = support)")
    print(f"  json {jpath}")
    for r in reasons:
        print(f"  {verdict}: {r}")
    print(f"visible_ratio verdict: {verdict} (FAIL < {a.fail}, WARN < {a.warn}; proposed thresholds)")
    return {"OK": 0, "WARN": 1, "FAIL": 2}[verdict]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
