r"""stability_check.py - standing stability check for any display piece (does it tip over?).

Each STL is one printed part. The tool computes, per part standing alone and for the assembly as placed:
  volume, mass, centre of mass (CoM), the support polygon (convex hull of the lowest down-facing faces within
  --band mm of the floor), its area and the lowest-contact area (layer-1 contact), the CoM's horizontal margin to
  the hull edge (min perpendicular, and per direction), tip angle per direction in 10 deg steps
  (theta = atan(margin_in_that_direction / CoM_height)), the "knock" force at the top of the piece that starts
  tipping (F = m*g*margin / H_top, moment balance about the tipping edge), and a top-heavy index
  (CoM_height / smallest hull half-width).

Flags (thresholds are PROPOSED, NOT VERIFIED; confirm every prediction with a physical tilt test):
  FAIL  CoM outside the support polygon (or the polygon is degenerate)
  WARN  minimum tip angle < 15 deg
  WARN  layer-1 contact (lowest-contact area) < 25 % of the hull area (made-up example: 100 of 500 mm2 under two small feet)
  WARN  mass from uniform density (a mesh assumption: the print has walls, infill, glue, supports removed)
  WARN  mesh not watertight (volume and CoM approximate)

Mass per part: --mass NAME=GRAMS (the slicer's result.json grams for that object; the number to use),
else uniform density --density g/cm3 (default 1.24). --gcode NAME=plate.gcode measures the support / brim / skirt
grams from the G-code extrusion by "; FEATURE:" tag and subtracts them (result.json carries no per-feature grams).

Inputs: STL files (read-only), optional plate G-code. Outputs: Markdown report on stdout (and --out), optional --json,
optional renders. Read-only on the inputs; nothing printed or sent.
Usage:
  .venv\Scripts\python.exe tools\stability_check.py <part.stl> [more.stl ...]
      [--mass NAME=GRAMS ...] [--gcode NAME=plate.gcode ...]
      [--transform NAME=json4x4 ...] [--place NAME=dx,dy,dz ...] [--level NAME ...|--level all]
      [--floor z] [--band 0.3] [--density 1.24] [--out report.md] [--json report.json] [--render prefix]
Example: .venv\Scripts\python.exe tools\stability_check.py examples\calibration-cube\cube_20mm.stl --mass cube_20mm=9.5
NAME = the STL file stem (my_base for my_base.stl); the basename or full path also match.
--level rests that part on its own fitted bottom plane for the STANDALONE analysis only (assembly keeps the pose).
Direction convention: 0 deg = +X, 90 deg = +Y.
Exit code: 0 no flags, 1 WARN only, 2 FAIL, 3 usage / load error.
Render: Blender headless (blender_exe in config\paths.yaml) with tools\stability_render.py (front, side, top orthographic,
CoM marked, hull drawn as a slab under the floor); skipped with a note when blender_exe is empty or missing.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
import trimesh
from shapely.geometry import LineString, MultiPoint, Point
from shapely.ops import nearest_points

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_config  # noqa: E402

TOOL_NAME = "stability_check.py"
TOOL_VERSION = "1.0.0"  # written into every report instead of the tool's path and the run time
G = 9.81  # m/s^2
try:
    _bl = mm_config.optional_path("blender_exe")
except Exception:  # noqa: BLE001
    _bl = None
BLENDER = str(_bl) if _bl is not None else ""   # empty = Blender features disabled (set blender_exe in config\\paths.yaml)
RENDER_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stability_render.py")
TIP_WARN_DEG = 15.0  # proposed, not verified
CONTACT_WARN_FRAC = 0.25  # proposed, not verified
DOWN_NZ = -0.7  # a face counts as "down-facing" when its unit normal z < -0.7 (within 45 deg of straight down)
REMOVED_FEATURES = ("Support", "Support interface", "Support transition", "Brim", "Skirt", "Prime tower", "Wipe tower", "Flush")


# ----------------------------------------------------------------------------- helpers
def key_of(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def match_name(name: str, parts: list[dict]) -> dict:
    for p in parts:
        if name in (p["name"], os.path.basename(p["path"]), p["path"], os.path.normpath(p["path"])):
            return p
    raise SystemExit(f"usage: no part named {name!r}; parts are {[p['name'] for p in parts]}")


def parse_kv(items: list[str] | None, what: str) -> list[tuple[str, str]]:
    out = []
    for it in items or []:
        if "=" not in it:
            raise SystemExit(f"usage: --{what} expects NAME=VALUE, got {it!r}")
        k, v = it.split("=", 1)
        out.append((k, v))
    return out


def rotation_to_minus_z(n: np.ndarray) -> np.ndarray:
    """4x4 rotation taking unit vector n to (0,0,-1)."""
    n = n / np.linalg.norm(n)
    tgt = np.array([0.0, 0.0, -1.0])
    axis = np.cross(n, tgt)
    s = np.linalg.norm(axis)
    c = float(np.dot(n, tgt))
    if s < 1e-12:
        return np.eye(4) if c > 0 else trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0])
    return trimesh.transformations.rotation_matrix(math.atan2(s, c), axis / s)


def hull_min_width(hull) -> float:
    pts = np.asarray(hull.exterior.coords)[:-1]
    n = len(pts)
    if n < 3:
        return 0.0
    best = math.inf
    for i in range(n):
        e = pts[(i + 1) % n] - pts[i]
        ln = np.linalg.norm(e)
        if ln < 1e-12:
            continue
        nrm = np.array([-e[1], e[0]]) / ln
        proj = pts @ nrm
        best = min(best, float(proj.max() - proj.min()))
    return best if best < math.inf else 0.0


def ray_margin(hull, cxy: np.ndarray, phi_deg: float) -> float:
    """Distance from an interior point to the hull boundary along direction phi (0 = +X, 90 = +Y)."""
    d = np.array([math.cos(math.radians(phi_deg)), math.sin(math.radians(phi_deg))])
    minx, miny, maxx, maxy = hull.bounds
    L = 4.0 * (abs(maxx - minx) + abs(maxy - miny)) + 1.0
    seg = LineString([cxy, cxy + d * L])
    inter = seg.intersection(hull.exterior)
    if inter.is_empty:
        return float("nan")
    pts = [inter] if inter.geom_type == "Point" else [g for g in getattr(inter, "geoms", []) if g.geom_type == "Point"]
    if not pts:
        return float("nan")
    return min(float(np.linalg.norm(np.array(p.coords[0]) - cxy)) for p in pts)


def section_area(mesh: trimesh.Trimesh, z: float) -> float:
    s = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if s is None:
        return 0.0
    p2, _T = s.to_2D()
    return float(sum(p.area for p in p2.polygons_full))  # polygons_full keep their holes


# ----------------------------------------------------------------------------- G-code grams by feature
def gcode_grams(path: str) -> dict:
    """Sum relative extrusion (E>0 on XY moves) per '; FEATURE:' tag; convert with the header's filament diameter and density.
    Moves counted: G0/G1 with X or Y, and G2/G3 arcs with X, Y, I or J (an extruding full circle may omit X/Y). Arc moves
    matter: with arc fitting on they can carry a large share of the extrusion (42.5 % on one measured plate)."""
    feat = "Custom"
    length: dict[str, float] = {}
    header = {"density": None, "diameter": None, "total_g": None, "total_mm": None}
    re_e = re.compile(r"\bE(-?\d*\.?\d+)")
    re_xy = re.compile(r"\b[XY]-?\d")
    re_xyij = re.compile(r"\b[XYIJ]-?\.?\d")
    relative = None
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("; FEATURE:"):
                feat = line.split(":", 1)[1].strip()
                continue
            if line.startswith(("G1 ", "G0 ", "G2 ", "G3 ")):
                code = line.split(";")[0]
                if " E" not in code or not (re_xyij if line[1] in "23" else re_xy).search(code):
                    continue
                m = re_e.search(line)
                if m:
                    e = float(m.group(1))
                    if e > 0:
                        length[feat] = length.get(feat, 0.0) + e
                continue
            if line.startswith("M83"):
                relative = True
            elif line.startswith("M82"):
                relative = False
            elif line.startswith(";"):
                low = line.lower()
                if "filament_density" in low and header["density"] is None:
                    mm = re.search(r"filament_density\s*[:=]\s*([\d.]+)", low)
                    if mm:
                        header["density"] = float(mm.group(1))
                elif "filament_diameter" in low and header["diameter"] is None:
                    mm = re.search(r"filament_diameter\s*[:=]\s*([\d.]+)", low)
                    if mm:
                        header["diameter"] = float(mm.group(1))
                elif "total filament weight [g]" in low:
                    header["total_g"] = float(low.split(":")[-1])
                elif "total filament length [mm]" in low:
                    header["total_mm"] = float(low.split(":")[-1])
    dens = header["density"] or 1.24
    dia = header["diameter"] or 1.75
    area = math.pi * (dia / 2) ** 2  # mm2
    grams = {k: v * area * dens / 1000.0 for k, v in length.items()}
    total_g = sum(grams.values())
    removed = {k: v for k, v in grams.items() if k in REMOVED_FEATURES}
    return {
        "path": path, "relative_e": relative, "density_g_cm3": dens, "diameter_mm": dia,
        "header_total_g": header["total_g"], "header_total_mm": header["total_mm"],
        "summed_mm": sum(length.values()), "summed_g": total_g,
        "grams_by_feature": grams, "removed_g": sum(removed.values()), "removed_by_feature": removed,
        "model_g": total_g - sum(removed.values()),
    }


# ----------------------------------------------------------------------------- analysis
def analyse(meshes: list[trimesh.Trimesh], masses: list[float], floor: float | None, band: float, label: str) -> dict:
    allv = np.vstack([m.vertices for m in meshes])
    zmin = float(allv[:, 2].min())
    zmax = float(allv[:, 2].max())
    floor_z = zmin if floor is None else float(floor)
    mass = float(sum(masses))
    com = sum(np.asarray(m.center_mass) * mm for m, mm in zip(meshes, masses)) / mass
    volume = float(sum(m.volume for m in meshes))
    # contact faces: down-facing, centroid within band of the floor
    pts2, contact_area, n_faces, contact_zmax = [], 0.0, 0, None
    for m in meshes:
        c = m.triangles_center
        n = m.face_normals
        sel = (n[:, 2] < DOWN_NZ) & (c[:, 2] <= floor_z + band) & (c[:, 2] >= floor_z - band)
        if sel.any():
            contact_area += float((m.area_faces[sel] * (-n[sel, 2])).sum())
            n_faces += int(sel.sum())
            fv = m.vertices[m.faces[sel]].reshape(-1, 3)
            pts2.append(fv[:, :2])
            zz = float(c[sel, 2].max())
            contact_zmax = zz if contact_zmax is None else max(contact_zmax, zz)
    out = {
        "label": label, "floor_z": floor_z, "band_mm": band, "z_min": zmin, "z_max": zmax, "height_mm": zmax - floor_z,
        "volume_mm3": volume, "mass_g": mass, "com": [float(x) for x in com], "com_height_mm": float(com[2] - floor_z),
        "contact_faces": n_faces, "contact_area_mm2": contact_area, "contact_zmax": contact_zmax,
        "layer1_section_area_mm2": float(sum(section_area(m, floor_z + 0.1) for m in meshes)),
        "flags": [],
    }
    if not pts2:
        out["flags"].append(("FAIL", f"{label}: no down-facing faces within {band} mm of the floor z {floor_z:.3f} (wrong --floor or part floating)"))
        out["hull"] = None
        return out
    P = np.vstack(pts2)
    hull = MultiPoint([tuple(p) for p in np.unique(np.round(P, 5), axis=0)]).convex_hull
    if hull.geom_type != "Polygon" or hull.area < 1e-6:
        out["flags"].append(("FAIL", f"{label}: support polygon is degenerate (area {hull.area:.4f} mm2): knife-edge or point contact"))
        out["hull"] = None
        out["hull_area_mm2"] = float(hull.area)
        return out
    cxy = np.asarray(com[:2], float)
    pc = Point(cxy)
    inside = bool(hull.contains(pc))
    perp = float(hull.exterior.distance(pc))
    near = nearest_points(pc, hull.exterior)[1]
    vec = np.array(near.coords[0]) - cxy
    worst_dir = math.degrees(math.atan2(vec[1], vec[0])) % 360.0 if np.linalg.norm(vec) > 1e-9 else float("nan")
    minw = hull_min_width(hull)
    h = out["com_height_mm"]
    H = out["height_mm"]
    table = []
    for phi in range(0, 360, 10):
        mg = ray_margin(hull, cxy, phi) if inside else float("nan")
        th = math.degrees(math.atan2(mg, h)) if inside and not math.isnan(mg) else float("nan")
        table.append({"dir_deg": phi, "margin_mm": mg, "tip_deg": th})
    valid = [t for t in table if not math.isnan(t["tip_deg"])]
    tmin = min(valid, key=lambda t: t["tip_deg"]) if valid else None
    margin_signed = perp if inside else -perp
    tip_exact = math.degrees(math.atan2(margin_signed, h)) if h > 0 else float("nan")
    knock_N = (mass / 1000.0) * G * (margin_signed / 1000.0) / (H / 1000.0) if H > 0 else float("nan")
    out.update({
        "hull": [list(map(float, c)) for c in hull.exterior.coords],
        "hull_area_mm2": float(hull.area), "hull_min_width_mm": minw,
        "hull_bounds": [float(x) for x in hull.bounds],
        "contact_fraction": contact_area / hull.area if hull.area > 0 else float("nan"),
        "com_inside": inside, "margin_min_mm": margin_signed, "margin_worst_dir_deg": worst_dir,
        "tip_table": table,
        "tip_min_table_deg": tmin["tip_deg"] if tmin else float("nan"),
        "tip_min_table_dir_deg": tmin["dir_deg"] if tmin else float("nan"),
        "tip_min_exact_deg": tip_exact,
        "knock_force_N": knock_N, "knock_force_gf": knock_N / G * 1000.0 if not math.isnan(knock_N) else float("nan"),
        "top_heavy_index": h / (minw / 2.0) if minw > 0 else float("inf"),
    })
    if not inside:
        out["flags"].append(("FAIL", f"{label}: CoM ({cxy[0]:.2f}, {cxy[1]:.2f}) is OUTSIDE the support polygon by {perp:.2f} mm (towards {worst_dir:.0f} deg): it falls over"))
    elif tip_exact < TIP_WARN_DEG:
        out["flags"].append(("WARN", f"{label}: minimum tip angle {tip_exact:.2f} deg < {TIP_WARN_DEG:.0f} deg (proposed threshold, not verified), worst direction {worst_dir:.0f} deg"))
    if out["contact_fraction"] < CONTACT_WARN_FRAC:
        out["flags"].append(("WARN", f"{label}: layer-1 contact {contact_area:.1f} mm2 is {100*out['contact_fraction']:.1f} % of the hull area {hull.area:.1f} mm2 (< {100*CONTACT_WARN_FRAC:.0f} % proposed, not verified)"))
    return out


def level_mesh(mesh: trimesh.Trimesh, fit_band: float, flat_nz: float = -0.995) -> tuple[trimesh.Trimesh, dict]:
    """Rotate a copy so its bottom plane is horizontal. Plane = area-weighted mean normal of the near-flat (normal z < flat_nz,
    i.e. within ~5.7 deg of flat) down-facing faces within a band of the lowest point; the band shrinks
    (fit_band, /2, /4, 0.08, 0.05 mm) so remnants of a higher surface (e.g. the original sole above a 0.4 mm cut) drop out
    of the fit as the true bottom plane comes level. Made-up illustration: a part whose flat base was cut 1 deg off
    level is rotated so that base lies on the floor before the support polygon is measured."""
    m2 = mesh.copy()
    total = np.eye(4)
    used = 0
    bands = [fit_band, fit_band / 2, fit_band / 4, 0.08, 0.05]
    for band in bands:
        for _ in range(2):
            c = m2.triangles_center
            n = m2.face_normals
            zmin = float(m2.bounds[0][2])
            sel = (n[:, 2] < flat_nz) & (c[:, 2] <= zmin + band)
            if not sel.any():
                sel = (n[:, 2] < DOWN_NZ) & (c[:, 2] <= zmin + band)
            if not sel.any():
                break
            a = m2.area_faces[sel]
            nbar = (n[sel] * a[:, None]).sum(0)
            nbar /= np.linalg.norm(nbar)
            tilt = math.degrees(math.acos(max(-1.0, min(1.0, -nbar[2]))))
            used = int(sel.sum())
            if tilt < 0.005:
                break
            R = rotation_to_minus_z(nbar)
            cen = (c[sel] * a[:, None]).sum(0) / a.sum()
            T = trimesh.transformations.translation_matrix(cen) @ R @ trimesh.transformations.translation_matrix(-cen)
            m2.apply_transform(T)
            total = T @ total
    if used == 0:
        return mesh, {"applied": False, "reason": "no down-facing faces near the bottom"}
    n0 = total[:3, :3].T @ np.array([0.0, 0.0, -1.0])
    tilt_total = math.degrees(math.acos(max(-1.0, min(1.0, -n0[2]))))
    return m2, {"applied": True, "tilt_deg": tilt_total, "fit_band_mm": fit_band, "fitted_faces_last": used, "flat_nz": flat_nz, "matrix": total.tolist()}


# ----------------------------------------------------------------------------- report
def f(x, nd=2):
    if x is None:
        return "n/a"
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return "n/a" if math.isnan(x) else "inf"
    return f"{x:,.{nd}f}" if isinstance(x, (int, float)) else str(x)


def block(a: dict) -> list[str]:
    L = [f"### {a['label']}", "",
         f"- floor z {f(a['floor_z'],3)} mm; height above floor {f(a['height_mm'])} mm; band {a['band_mm']} mm",
         f"- volume {f(a['volume_mm3'],1)} mm3; mass {f(a['mass_g'])} g; CoM x {f(a['com'][0])} y {f(a['com'][1])} z {f(a['com'][2])} mm; CoM height {f(a['com_height_mm'])} mm"]
    if a.get("hull") is None:
        L.append(f"- support polygon: NONE / degenerate (contact faces {a['contact_faces']}, contact area {f(a['contact_area_mm2'],1)} mm2)")
        return L
    L += [
        f"- support polygon (convex hull of {a['contact_faces']} down-facing faces within {a['band_mm']} mm of the floor): area {f(a['hull_area_mm2'],1)} mm2, "
        f"bounds x {f(a['hull_bounds'][0])}..{f(a['hull_bounds'][2])} y {f(a['hull_bounds'][1])}..{f(a['hull_bounds'][3])}, smallest width {f(a['hull_min_width_mm'])} mm",
        f"- lowest-contact area (projected, same faces) {f(a['contact_area_mm2'],1)} mm2 = {f(100*a['contact_fraction'],1)} % of the hull; section at floor + 0.10 mm {f(a['layer1_section_area_mm2'],1)} mm2",
        f"- CoM {'INSIDE' if a['com_inside'] else 'OUTSIDE'} the hull; margin to the nearest edge {f(a['margin_min_mm'])} mm towards {f(a['margin_worst_dir_deg'],0)} deg (0 = +X, 90 = +Y)",
        f"- tip angle: exact minimum {f(a['tip_min_exact_deg'])} deg (atan(margin / CoM height)); 10-deg table minimum {f(a['tip_min_table_deg'])} deg at {f(a['tip_min_table_dir_deg'],0)} deg",
        f"- knock force at the top (F = m*g*margin / H_top = {f(a['mass_g'])} g * 9.81 m/s2 * {f(a['margin_min_mm'])} mm / {f(a['height_mm'])} mm): {f(a['knock_force_N'],3)} N = {f(a['knock_force_gf'],1)} gf",
        f"- top-heavy index (CoM height / smallest hull half-width) {f(a['top_heavy_index'])}",
        "",
        "| dir deg | " + " | ".join(str(t["dir_deg"]) for t in a["tip_table"][:18]) + " |",
        "|---|" + "---|" * 18,
        "| margin mm | " + " | ".join(f(t["margin_mm"], 1) for t in a["tip_table"][:18]) + " |",
        "| tip deg | " + " | ".join(f(t["tip_deg"], 1) for t in a["tip_table"][:18]) + " |",
        "",
        "| dir deg | " + " | ".join(str(t["dir_deg"]) for t in a["tip_table"][18:]) + " |",
        "|---|" + "---|" * 18,
        "| margin mm | " + " | ".join(f(t["margin_mm"], 1) for t in a["tip_table"][18:]) + " |",
        "| tip deg | " + " | ".join(f(t["tip_deg"], 1) for t in a["tip_table"][18:]) + " |",
    ]
    return L


def render(parts: list[dict], asm: dict, prefix: str) -> list[str]:
    if not BLENDER:
        return ["render skipped: blender_exe is empty in config\\paths.yaml (Blender features are disabled)"]
    if not os.path.isfile(BLENDER):
        return [f"render skipped: Blender not found at {BLENDER} (check blender_exe in config\\paths.yaml)"]
    if asm.get("hull") is None:
        return ["render skipped: no support polygon for the assembly"]
    tmp = tempfile.mkdtemp(prefix="stability_")
    objs = []
    for i, p in enumerate(parts):
        if np.allclose(p["matrix"], np.eye(4)):
            path = p["path"]
        else:
            path = os.path.join(tmp, p["name"] + ".stl")
            p["mesh"].export(path)
        objs.append({"path": path, "color": [[0.80, 0.80, 0.82], [0.85, 0.72, 0.55], [0.6, 0.75, 0.85], [0.75, 0.85, 0.6]][i % 4]})
    from shapely.geometry import Polygon as _Poly
    hull_draw = [list(map(float, c)) for c in _Poly(asm["hull"]).buffer(1.0, join_style=2).exterior.coords]  # drawn 1 mm outside the hull so the outline shows in the top view
    job = {"objects": objs, "hull": hull_draw, "floor_z": asm["floor_z"], "com": asm["com"],
           "bbox": [[float(min(p["mesh"].bounds[0][k] for p in parts)) for k in range(3)], [float(max(p["mesh"].bounds[1][k] for p in parts)) for k in range(3)]],
           "out_prefix": prefix}
    os.makedirs(os.path.dirname(os.path.abspath(prefix)) or ".", exist_ok=True)
    jp = os.path.join(tmp, "job.json")
    with open(jp, "w", encoding="utf-8") as fh:
        json.dump(job, fh)
    cmd = [BLENDER, "--background", "--factory-startup", "-noaudio", "--python-exit-code", "1", "--python", RENDER_PY, "--", jp]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    except Exception as e:  # noqa: BLE001
        return [f"render failed to launch Blender: {e}"]
    outs = [prefix + s for s in ("-front.png", "-side.png", "-top.png")]
    lines = []
    for o in outs:
        lines.append(f"render {'written' if os.path.isfile(o) else 'MISSING'}: {os.path.abspath(o)}")
    if r.returncode != 0:
        lines.append("Blender exit code %d; last output: %s" % (r.returncode, (r.stdout + r.stderr)[-600:].strip()))
    return lines


# ----------------------------------------------------------------------------- main
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Standing stability check for display pieces (see module docstring).")
    ap.add_argument("stl", nargs="+")
    ap.add_argument("--mass", action="append", help="NAME=GRAMS (slicer result.json grams for that object)")
    ap.add_argument("--gcode", action="append", help="NAME=plate.gcode: subtract support/brim/skirt grams measured from the G-code")
    ap.add_argument("--transform", action="append", help="NAME=json 4x4 row-major")
    ap.add_argument("--place", action="append", help="NAME=dx,dy,dz translation")
    ap.add_argument("--level", action="append", help="NAME or 'all': rest the part on its fitted bottom plane for the standalone analysis")
    ap.add_argument("--floor", type=float, default=None, help="floor plane z for the assembly (default: lowest vertex)")
    ap.add_argument("--band", type=float, default=0.3, help="contact band above the floor, mm (default 0.3)")
    ap.add_argument("--density", type=float, default=1.24, help="uniform density g/cm3 when no --mass (default 1.24)")
    ap.add_argument("--out", help="markdown report path")
    ap.add_argument("--json", help="JSON report path")
    ap.add_argument("--render", help="PNG prefix: writes <prefix>-front.png, -side.png, -top.png via Blender (blender_exe in config\\paths.yaml)")
    a = ap.parse_args(argv)

    notes: list[str] = []
    flags: list[tuple[str, str]] = []
    parts: list[dict] = []
    for p in a.stl:
        if not os.path.isfile(p):
            print(f"ERROR: not a file: {p}")
            return 3
        m = trimesh.load(p, process=True, force="mesh")  # process=True merges STL vertices (an unmerged STL is not watertight)
        parts.append({"name": key_of(p), "path": os.path.abspath(p), "mesh": m, "matrix": np.eye(4), "mass": None,
                      "mass_source": None, "watertight": bool(m.is_watertight), "bodies": int(len(m.split(only_watertight=False)))})
    for k, v in parse_kv(a.transform, "transform"):
        M = np.array(json.loads(v), float).reshape(4, 4)
        match_name(k, parts)["matrix"] = M
    for k, v in parse_kv(a.place, "place"):
        d = [float(x) for x in v.split(",")]
        if len(d) != 3:
            raise SystemExit("usage: --place NAME=dx,dy,dz")
        match_name(k, parts)["matrix"] = trimesh.transformations.translation_matrix(d)
    for p in parts:
        if not np.allclose(p["matrix"], np.eye(4)):
            p["mesh"].apply_transform(p["matrix"])
        if not p["watertight"]:
            flags.append(("WARN", f"{p['name']}: mesh not watertight ({p['bodies']} bodies): volume and CoM are approximate"))
    for k, v in parse_kv(a.mass, "mass"):
        pp = match_name(k, parts)
        pp["mass"] = float(v)
        pp["mass_source"] = f"--mass {v} g (slicer grams)"
    gstats: dict[str, dict] = {}
    for k, v in parse_kv(a.gcode, "gcode"):
        pp = match_name(k, parts)
        if not os.path.isfile(v):
            print(f"ERROR: G-code not a file: {v}")
            return 3
        gs = gcode_grams(v)
        gstats[pp["name"]] = gs
        total = pp["mass"] if pp["mass"] is not None else gs["summed_g"]
        pp["mass"] = total - gs["removed_g"]
        rm = ", ".join(f"{kk} {vv:.2f} g" for kk, vv in sorted(gs["removed_by_feature"].items()))
        pp["mass_source"] = f"{total:.2f} g minus removed features from G-code ({rm or 'none'}) = {pp['mass']:.2f} g"
        if gs["header_total_g"] is not None:
            dev = gs["summed_g"] - gs["header_total_g"]
            notes.append(f"{pp['name']}: G-code {v}: summed extrusion {gs['summed_mm']:.0f} mm = {gs['summed_g']:.2f} g vs header total {gs['header_total_g']:.2f} g (diff {dev:+.2f} g); "
                         f"filament_diameter {gs['diameter_mm']} mm, filament_density {gs['density_g_cm3']} g/cm3 from the header; relative E {gs['relative_e']}")
    for p in parts:
        if p["mass"] is None:
            p["mass"] = p["mesh"].volume / 1000.0 * a.density
            p["mass_source"] = f"uniform solid {a.density} g/cm3 x {p['mesh'].volume:.1f} mm3 (assumed)"
            flags.append(("WARN", f"{p['name']}: mass {p['mass']:.2f} g from uniform density {a.density} g/cm3 is a mesh assumption; the printed part has walls, infill and (removed) supports: use the slicer grams (--mass)"))

    level_names = set()
    for k in a.level or []:
        if k == "all":
            level_names.update(p["name"] for p in parts)
        else:
            level_names.add(match_name(k, parts)["name"])

    standalone = []
    for p in parts:
        mesh = p["mesh"]
        lev = {"applied": False}
        if p["name"] in level_names:
            mesh, lev = level_mesh(mesh, fit_band=max(0.6, 2 * a.band))
        else:
            _m2, probe = level_mesh(mesh, fit_band=max(0.6, 2 * a.band))
            if probe.get("applied") and probe["tilt_deg"] > 0.2:
                notes.append(f"{p['name']}: bottom faces are tilted {probe['tilt_deg']:.2f} deg from the floor in this pose; the standalone numbers use the pose as given (use --level {p['name']} to rest it on its bottom plane)")
        r = analyse([mesh], [p["mass"]], None, a.band, f"{p['name']} standing alone" + (f" (levelled by {lev['tilt_deg']:.2f} deg)" if lev.get("applied") else ""))
        r["level"] = {k: v for k, v in lev.items() if k != "matrix"}
        standalone.append(r)
        flags += r["flags"]
    asm = None
    show_asm = len(parts) > 1 or a.floor is not None or standalone[0]["level"].get("applied")
    if show_asm:
        asm = analyse([p["mesh"] for p in parts], [p["mass"] for p in parts], a.floor, a.band, "assembly as placed" + (" (single part, pose as given)" if len(parts) == 1 else ""))
        flags += asm["flags"]
    else:
        asm = standalone[0]  # one part, no floor, no levelling: the assembly IS the standalone result

    render_lines = render(parts, asm, a.render) if a.render else []

    L = ["# Stability check", "",
         f"Tool: {TOOL_NAME} {TOOL_VERSION}", "",
         f"Thresholds (PROPOSED, NOT VERIFIED - confirm with a physical tilt test): FAIL CoM outside the support polygon; "
         f"WARN minimum tip angle < {TIP_WARN_DEG:.0f} deg; WARN layer-1 contact < {100*CONTACT_WARN_FRAC:.0f} % of the hull area (example: 100 of 500 mm2 is 20 %, which warns). "
         f"Formulas: tip angle = atan(margin / CoM height); knock force F = m*g*margin / H_top (moment balance about the tipping edge, g = {G} m/s2); "
         f"top-heavy index = CoM height / smallest hull half-width. Direction convention: 0 deg = +X, 90 deg = +Y. "
         f"Support polygon = convex hull of down-facing faces (normal z < {DOWN_NZ}) within {a.band} mm of the floor; lowest-contact area = their projected area.",
         "", "## Parts", "",
         "| part | file | watertight | bodies | volume mm3 | mass g | mass source | CoM x, y, z (mm, as placed) | transform |",
         "|---|---|---|---|---|---|---|---|---|"]
    for p in parts:
        tr = "identity" if np.allclose(p["matrix"], np.eye(4)) else ("translate " + ", ".join(f"{x:+.4f}" for x in p["matrix"][:3, 3]) if np.allclose(p["matrix"][:3, :3], np.eye(3)) else "4x4 " + json.dumps(np.round(p["matrix"], 6).tolist()))
        c = p["mesh"].center_mass
        L.append(f"| {p['name']} | {p['path']} | {p['watertight']} | {p['bodies']} | {f(p['mesh'].volume,1)} | {f(p['mass'])} | {p['mass_source']} | {f(c[0])}, {f(c[1])}, {f(c[2])} | {tr} |")
    if gstats:
        L += ["", "### G-code grams by feature", ""]
        for name, gs in gstats.items():
            L.append(f"- {name}: {gs['path']}")
            L.append("  - " + "; ".join(f"{k} {v:.2f} g" for k, v in sorted(gs["grams_by_feature"].items(), key=lambda kv: -kv[1])))
            L.append(f"  - removed (support / brim / skirt / tower): {gs['removed_g']:.2f} g -> model {gs['model_g']:.2f} g of {gs['summed_g']:.2f} g summed (header {f(gs['header_total_g'])} g)")
    L += ["", "## Standalone (each part on its own lowest faces)", ""]
    for r in standalone:
        L += block(r) + [""]
    if show_asm:
        L += ["## Assembly", ""] + block(asm) + [""]
    else:
        L += ["## Assembly", "", "- single part, no --floor, no --level: the assembly result is the standalone block above", ""]
    if notes:
        L += ["## Notes", ""] + [f"- {n}" for n in notes] + [""]
    if render_lines:
        L += ["## Renders", ""] + [f"- {n}" for n in render_lines] + [""]
    L += ["## Flags", ""]
    seen = set()
    uniq = []
    for lvl, msg in flags:
        if (lvl, msg) not in seen:
            seen.add((lvl, msg))
            uniq.append((lvl, msg))
    if not uniq:
        L.append("- PASS: no flags")
    for lvl, msg in uniq:
        L.append(f"- {lvl}: {msg}")
    worst = 2 if any(l == "FAIL" for l, _ in uniq) else (1 if uniq else 0)
    L.append("")
    L.append(f"Result: {'FAIL' if worst == 2 else ('WARN' if worst == 1 else 'PASS')} (exit {worst}). Nothing printed or sent.")
    text = "\n".join(L)
    print(text)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    if a.json:
        def clean(o):
            if isinstance(o, dict):
                return {k: clean(v) for k, v in o.items() if k != "mesh"}
            if isinstance(o, (list, tuple)):
                return [clean(x) for x in o]
            if isinstance(o, np.ndarray):
                return clean(o.tolist())
            if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
                return None
            if isinstance(o, (np.floating, np.integer)):
                return o.item()
            return o
        rep = {"tool": TOOL_NAME, "version": TOOL_VERSION, "thresholds": {"tip_warn_deg": TIP_WARN_DEG, "contact_warn_frac": CONTACT_WARN_FRAC, "status": "proposed, not verified"},
               "parts": [{k: v for k, v in p.items() if k != "mesh"} | {"volume_mm3": float(p["mesh"].volume), "com": [float(x) for x in p["mesh"].center_mass], "matrix": p["matrix"].tolist()} for p in parts],
               "gcode": gstats, "standalone": standalone, "assembly": asm, "notes": notes, "renders": render_lines, "flags": [list(x) for x in uniq],
               "result": "FAIL" if worst == 2 else ("WARN" if worst == 1 else "PASS")}
        os.makedirs(os.path.dirname(os.path.abspath(a.json)) or ".", exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(clean(rep), fh, indent=1)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
