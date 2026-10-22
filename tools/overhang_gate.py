r"""overhang_gate.py - part-level geometry gate: overhang area, new-vs-reference overhang, per-layer cantilever and islands, per PART in
its PRINT POSE.

CONVENTION (Bambu Studio's support_threshold_angle tooltip, PrintConfig.cpp, https://github.com/bambulab/BambuStudio:
"Support will be generated for overhangs whose slope angle is below the threshold"):
  overhang angle = angle between the face normal and straight DOWN (-Z). A horizontal downward face is 0 deg, a vertical wall is 90 deg,
  an upward face is > 90 deg. A face is an OVERHANG when its angle is strictly BELOW the threshold (support_threshold_angle: 30 in
  "0.20mm Standard @BBL H2C", 25 in "0.16mm High Quality @BBL H2C"). Faces whose centroid is at or below --floor-eps (default layer/2,
  the first slice plane) count as the first layer on the plate, not as overhangs.

Per part (always the whole part, never a zone):
  overhang        area of faces below the threshold, the threshold-45 and 45-60 deg bands for information, the minimum angle and the
                  bounding box of the below-threshold faces in the posed frame.
  new / removed   with a reference (the previous round's STL, posed the same way): the below-threshold faces of the part that lie farther
  overhang        than --new-eps from the reference surface = overhang the change introduced (FAIL: the gate's rule is "0 new overhang per
                  part"); the reference's below-threshold faces farther than --new-eps from the new surface = overhang the change removed;
                  both are measured on faces subdivided to <= 1 mm edges, so a newly exposed ceiling that trimesh merged into a large
                  coplanar triangle is still seen; the net delta is printed so a MOVED ceiling reads as a move.
  cantilever      per layer (mid-layer sections every --layer mm): the farthest point of the layer's region outside the layer below
                  (boundary samples every 0.2 mm, then a bisection on the layer-below buffer for interior maxima, so an enclosed cavity roof
                  is measured too). Reported as the maximum with its z. With a reference the NEW cantilever = the overhanging region
                  minus the reference's own overhanging region at that z; NEW cantilever above --cantilever-warn is FAIL (default 0.5 mm:
                  a project acceptance value, not a general rule). Without a reference the whole-part cantilever above the value is WARN.
  islands         a layer piece overlapping the layer below by less than 0.01 mm2 (touching does not count) -> WARN, listed with z
                  and area (also with a reference). NEW island = an island not covered (>= 50 % of its area) by the reference's OWN islands
                  at that z -> FAIL with a reference.
  sections        built from the 3D section loops with even-odd combination; a plane through modelled vertices can return open loops, so
                  such a plane is re-cut at z + 0.001 then z - 0.001 before any polygon is built.

Pose: --pose NAME=rx,ry,rz (degrees, rotations about the fixed model x, then y, then z axes, then the part is dropped so its lowest point
is z = 0), or --pose-all rx,ry,rz; a part printed upside down is 180,0,0. --place NAME=dx,dy,dz adds a plate offset after the drop, so
reported boxes can be read in plate coordinates (otherwise they are in the model-centred posed frame). NAME = the STL file stem; the
basename or full path also match.
References: --ref NAME=reference.stl per part, or --ref-dir DIR [--ref-strip-prefix P] (reference = DIR\<stem minus prefix>.stl; a part
with no reference file is WARN "no reference" and gets the whole-part figures only).

Inputs: STL files (read-only). Output: text report, optional --json report file.
Usage:
  .venv\Scripts\python.exe tools\overhang_gate.py <part.stl> [more.stl ...]
      [--ref NAME=reference.stl ...] [--ref-dir DIR] [--ref-strip-prefix P] [--pose NAME=rx,ry,rz ...] [--pose-all rx,ry,rz]
      [--place NAME=dx,dy,dz ...] [--threshold 30] [--layer 0.2] [--floor-eps layer/2] [--new-eps 0.05] [--cantilever-warn 0.5]
      [--json report.json]
Example: .venv\Scripts\python.exe tools\overhang_gate.py examples\calibration-cube\cube_20mm.stl
Exit code: 0 no flags, 1 WARN only, 2 FAIL, 3 usage / load error (--help exits 0). Read-only on the inputs.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np
import shapely
import trimesh
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

CONVENTION = ("overhang angle = angle(face normal, -Z): horizontal down face 0 deg, wall 90 deg; overhang when angle < threshold "
              "(support_threshold_angle; 30 in 0.20mm Standard @BBL H2C)")
SAMPLE_STEP = 0.2      # mm between boundary sample points
SUBDIV_EDGE = 1.0      # mm: below-threshold faces are subdivided to this edge length before the new/removed distance test
ISLAND_MIN_OVERLAP = 0.01   # mm2: a piece overlapping the layer below by less than this is an island
NUDGE = 0.001          # mm: re-cut offset for a plane that returns open loops


# ----------------------------------------------------------------------------- geometry helpers
def overhang_angle_deg(normals: np.ndarray) -> np.ndarray:
    """Angle in degrees between each (unit) face normal and straight down (0, 0, -1). 0 = horizontal down face, 90 = wall, 180 = up."""
    n = np.asarray(normals, dtype=float).reshape(-1, 3)
    nz = n[:, 2] / np.maximum(np.linalg.norm(n, axis=1), 1e-12)
    return np.degrees(np.arccos(np.clip(-nz, -1.0, 1.0)))


def pose_matrix(rx: float, ry: float, rz: float) -> np.ndarray:
    """4x4 rotation: about x by rx, then y by ry, then z by rz (degrees, right-handed, fixed model axes)."""
    mx = trimesh.transformations.rotation_matrix(math.radians(rx), (1, 0, 0))
    my = trimesh.transformations.rotation_matrix(math.radians(ry), (0, 1, 0))
    mz = trimesh.transformations.rotation_matrix(math.radians(rz), (0, 0, 1))
    return mz @ my @ mx


def posed(mesh: trimesh.Trimesh, rot: tuple[float, float, float], place: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> trimesh.Trimesh:
    m = mesh.copy()
    if any(abs(v) > 1e-12 for v in rot):
        m.apply_transform(pose_matrix(*rot))
    m.apply_translation((0.0, 0.0, -m.bounds[0][2]))   # drop onto z = 0
    if any(abs(v) > 1e-12 for v in place):
        m.apply_translation(place)
    return m


def _loops_closed(loops) -> bool:
    for loop in loops:
        pts = np.asarray(loop, dtype=float)
        if len(pts) < 3 or np.linalg.norm(pts[0] - pts[-1]) > 1e-6:
            return False
    return True


def section_union(mesh: trimesh.Trimesh, z: float) -> tuple:
    """Shapely (Multi)Polygon of the mesh section at height z, and the z actually cut. Built from the 3D section loops directly (x, y stay
    plate coordinates in every layer; Path3D.to_2D() is NOT used, it re-fits a frame per section). Nested loops are holes: even-odd
    combination. A plane through modelled vertices can return OPEN loops; such a plane is re-cut at z + NUDGE, then z - NUDGE,
    and an open loop is never handed to Polygon() silently."""
    for zz in (z, z + NUDGE, z - NUDGE):
        sec = mesh.section(plane_origin=(0, 0, zz), plane_normal=(0, 0, 1))
        if sec is None:
            return Polygon(), zz, True
        try:
            loops = sec.discrete
        except Exception:  # noqa: BLE001
            continue
        if _loops_closed(loops):
            break
    else:
        return Polygon(), z, False   # still open after both nudges: report an empty layer rather than a wrong polygon
    shp = Polygon()
    for loop in loops:
        pts = np.asarray(loop, dtype=float)
        poly = Polygon(pts[:, :2]).buffer(0)
        if poly.is_empty or poly.area <= 1e-9:
            continue
        shp = shp.symmetric_difference(poly)
    return (shp.buffer(0) if not shp.is_valid else shp), zz, True


def pieces(geom) -> list:
    if geom is None or geom.is_empty:
        return []
    if isinstance(geom, MultiPolygon):
        return [g for g in geom.geoms if g.area > 1e-9]
    if isinstance(geom, Polygon):
        return [geom] if geom.area > 1e-9 else []
    return [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon) and g.area > 1e-9]


def boundary_points(geom) -> np.ndarray:
    pts = []
    for g in pieces(shapely.segmentize(geom, SAMPLE_STEP)):   # re-split: segmentize may return a MultiPolygon
        pts.extend(g.exterior.coords)
        for i in g.interiors:
            pts.extend(i.coords)
    return np.asarray(pts, dtype=float).reshape(-1, 2)


def farthest_from(region, prev) -> float:
    """Farthest any point of `region` lies from `prev` (0 when empty). Boundary samples first; then, because the maximum of an enclosed
    region (a cavity roof) lies in its interior, a bisection on prev.buffer(r) confirms or raises the value."""
    if region is None or region.is_empty or prev is None or prev.is_empty:
        return 0.0
    pts = boundary_points(region)
    lo = float(np.max(shapely.distance(shapely.points(pts), prev))) if len(pts) else 0.0
    minx, miny, maxx, maxy = region.bounds
    hi = max(lo, math.hypot(maxx - minx, maxy - miny))
    if hi - lo <= 0.02:
        return lo
    local = prev.intersection(shapely.box(minx - hi, miny - hi, maxx + hi, maxy + hi))
    if local.is_empty:
        return hi
    if region.difference(local.buffer(lo + 0.02)).is_empty:   # the usual case: nothing lies farther than the boundary maximum
        return lo
    for _ in range(40):
        if hi - lo <= 0.02:
            break
        mid = 0.5 * (lo + hi)
        if region.difference(local.buffer(mid)).is_empty:
            hi = mid
        else:
            lo = mid
    return lo


def islands_of(cur, prev) -> list:
    """Pieces of `cur` that overlap the layer below by less than ISLAND_MIN_OVERLAP mm2 (touching at a corner is not support)."""
    out = []
    for pc in pieces(cur):
        ov = pc.intersection(prev).area if (prev is not None and not prev.is_empty) else 0.0
        if ov < ISLAND_MIN_OVERLAP:
            out.append(pc)
    return out


def subdivided_overhang(mesh: trimesh.Trimesh, mask: np.ndarray):
    """(centroids, areas, angles) of the masked faces after subdivision to <= SUBDIV_EDGE mm edges."""
    if not mask.any():
        return np.zeros((0, 3)), np.zeros(0), np.zeros(0)
    sub = trimesh.Trimesh(mesh.vertices, mesh.faces[mask], process=False)
    v, f = trimesh.remesh.subdivide_to_size(sub.vertices, sub.faces, max_edge=SUBDIV_EDGE, max_iter=12)
    s2 = trimesh.Trimesh(v, f, process=False)
    return s2.triangles_center, s2.area_faces, overhang_angle_deg(s2.face_normals)


# ----------------------------------------------------------------------------- per-part analysis
def analyse(mesh: trimesh.Trimesh, threshold: float, layer: float, floor_eps: float, ref: trimesh.Trimesh | None, new_eps: float,
            cantilever_warn: float) -> dict:
    ang = overhang_angle_deg(mesh.face_normals)
    cz = mesh.triangles_center[:, 2]
    above_floor = cz > floor_eps
    area = mesh.area_faces
    below = (ang < threshold) & above_floor
    band1 = (ang >= threshold) & (ang < 45.0) & above_floor
    band2 = (ang >= 45.0) & (ang < 60.0) & above_floor
    out = {
        "watertight": bool(mesh.is_watertight), "faces": int(len(mesh.faces)),
        "bbox_posed": [[round(float(v), 3) for v in mesh.bounds[0]], [round(float(v), 3) for v in mesh.bounds[1]]],
        "overhang_below_threshold_mm2": round(float(area[below].sum()), 3),
        "band_threshold_to_45_mm2": round(float(area[band1].sum()), 3),
        "band_45_to_60_mm2": round(float(area[band2].sum()), 3),
        "min_angle_deg": round(float(ang[below].min()), 2) if below.any() else None,
        "overhang_bbox_posed": None,
        "new_overhang_mm2": None, "new_overhang_bbox_posed": None, "new_overhang_min_angle_deg": None,
        "removed_overhang_mm2": None, "net_overhang_delta_mm2": None, "ref_overhang_below_threshold_mm2": None,
        "max_cantilever_mm": 0.0, "max_cantilever_z": None, "layers_over_cantilever_warn": 0,
        "islands": [], "new_islands": None, "ref_islands": None, "layers": 0, "nudged_layers": 0, "open_layers": 0, "flags": [],
    }
    if below.any():
        tri = mesh.triangles[below].reshape(-1, 3)
        out["overhang_bbox_posed"] = [[round(float(v), 2) for v in tri.min(axis=0)], [round(float(v), 2) for v in tri.max(axis=0)]]
    if ref is not None:
        rang = overhang_angle_deg(ref.face_normals)
        rbelow = (rang < threshold) & (ref.triangles_center[:, 2] > floor_eps)
        out["ref_overhang_below_threshold_mm2"] = round(float(ref.area_faces[rbelow].sum()), 3)
        # new: subdivided below-threshold faces of the part farther than new_eps from the reference surface
        c, a, an = subdivided_overhang(mesh, below)
        if len(c):
            _cp, dist, _tid = trimesh.proximity.closest_point(ref, c)
            new = dist > new_eps
            out["new_overhang_mm2"] = round(float(a[new].sum()), 3)
            if new.any():
                lo, hi = c[new].min(axis=0), c[new].max(axis=0)
                out["new_overhang_bbox_posed"] = [[round(float(v), 2) for v in lo], [round(float(v), 2) for v in hi]]
                out["new_overhang_min_angle_deg"] = round(float(an[new].min()), 2)
        else:
            out["new_overhang_mm2"] = 0.0
        # removed: subdivided below-threshold faces of the reference farther than new_eps from the new surface
        rc_, ra, _ran = subdivided_overhang(ref, rbelow)
        if len(rc_):
            _cp, rdist, _tid = trimesh.proximity.closest_point(mesh, rc_)
            out["removed_overhang_mm2"] = round(float(ra[rdist > new_eps].sum()), 3)
        else:
            out["removed_overhang_mm2"] = 0.0
        out["net_overhang_delta_mm2"] = round(out["new_overhang_mm2"] - out["removed_overhang_mm2"], 3)
        out["new_islands"], out["ref_islands"] = [], []
    # per-layer sections
    zmax = float(mesh.bounds[1][2])
    zs = np.arange(layer / 2.0, zmax, layer)
    prev, prev_r = None, None
    worst, worst_z, n_over = 0.0, None, 0
    nworst, nworst_z, n_new_over = 0.0, None, 0
    for z in zs:
        cur, zcut, closed = section_union(mesh, float(z))
        out["layers"] += 1
        if abs(zcut - z) > 1e-9:
            out["nudged_layers"] += 1
        if not closed:
            out["open_layers"] += 1
        cur_r = None
        if ref is not None:
            cur_r, _zr, _cl = section_union(ref, float(z))
        if prev is not None and not cur.is_empty:
            diff_new = cur.difference(prev)
            c = farthest_from(diff_new, prev) if not diff_new.is_empty else 0.0
            if c > worst:
                worst, worst_z = c, float(z)
            if c > cantilever_warn:
                n_over += 1
            isl_here = islands_of(cur, prev)
            for pc in isl_here:
                out["islands"].append({"z": round(float(z), 3), "area_mm2": round(float(pc.area), 3)})
            if ref is not None and prev_r is not None:
                diff_ref = cur_r.difference(prev_r) if (cur_r is not None and not cur_r.is_empty) else Polygon()
                region = diff_new.difference(diff_ref.buffer(0.02)) if not diff_ref.is_empty else diff_new
                region = unary_union([g for g in pieces(region) if g.area > 0.01]) if not region.is_empty else region
                if not region.is_empty:
                    cn = farthest_from(region, prev)
                    if cn > nworst:
                        nworst, nworst_z = cn, float(z)
                    if cn > cantilever_warn:
                        n_new_over += 1
                ref_isl = islands_of(cur_r, prev_r) if cur_r is not None else []
                for pc in ref_isl:
                    out["ref_islands"].append({"z": round(float(z), 3), "area_mm2": round(float(pc.area), 3)})
                ref_isl_u = unary_union(ref_isl) if ref_isl else Polygon()
                for pc in isl_here:
                    covered = pc.intersection(ref_isl_u).area if not ref_isl_u.is_empty else 0.0
                    if covered < 0.5 * pc.area:
                        out["new_islands"].append({"z": round(float(z), 3), "area_mm2": round(float(pc.area), 3)})
        prev, prev_r = cur, cur_r
    out["max_cantilever_mm"] = round(worst, 3)
    out["max_cantilever_z"] = round(worst_z, 3) if worst_z is not None else None
    out["layers_over_cantilever_warn"] = n_over
    if ref is not None:
        out["new_cantilever_mm"] = round(nworst, 3)
        out["new_cantilever_z"] = round(nworst_z, 3) if nworst_z is not None else None
        out["new_layers_over_cantilever_warn"] = n_new_over
    # flags
    if not mesh.is_watertight:
        out["flags"].append(("WARN", "mesh not watertight: areas computed on the faces as given, sections may be open"))
    if out["open_layers"]:
        out["flags"].append(("WARN", f"{out['open_layers']} layer plane(s) returned open loops even after the +-{NUDGE} mm re-cut and were skipped"))
    if ref is not None:
        if (out["new_overhang_mm2"] or 0) > 0:
            out["flags"].append(("FAIL", f"new overhang below {threshold:g} deg: {out['new_overhang_mm2']} mm2 not on the reference surface "
                                         f"(min angle {out['new_overhang_min_angle_deg']} deg, posed bbox {out['new_overhang_bbox_posed']}); removed "
                                         f"{out['removed_overhang_mm2']} mm2, net {out['net_overhang_delta_mm2']:+} mm2"
                                         + (" - a moved ceiling, not a new one" if abs(out["net_overhang_delta_mm2"]) < 0.05 * max(out["new_overhang_mm2"], 1e-9) else "")
                                         + "; the gate wants 0 new"))
        if nworst > cantilever_warn:
            out["flags"].append(("FAIL", f"NEW per-layer cantilever {nworst:.2f} mm at posed z {nworst_z:.2f} ({n_new_over} layer(s) over {cantilever_warn:g} mm, "
                                         f"the --cantilever-warn acceptance value; project value, not a general rule); whole part {worst:.2f} mm at z {worst_z if worst_z is None else round(worst_z, 2)}"))
        if out["new_islands"]:
            out["flags"].append(("FAIL", f"{len(out['new_islands'])} NEW island layer piece(s) with nothing below and not in the reference: {out['new_islands'][:5]}"))
        if out["islands"]:
            out["flags"].append(("WARN", f"{len(out['islands'])} island layer piece(s) in the part (reference has {len(out['ref_islands'])}): {out['islands'][:5]}"))
    else:
        if worst > cantilever_warn:
            out["flags"].append(("WARN", f"per-layer cantilever {worst:.2f} mm at posed z {worst_z:.2f} ({n_over} layer(s) over {cantilever_warn:g} mm, "
                                         f"the --cantilever-warn acceptance value; project value, not a general rule)"))
        if out["islands"]:
            out["flags"].append(("WARN", f"{len(out['islands'])} island layer piece(s) with nothing below: {out['islands'][:5]}"))
    return out


# ----------------------------------------------------------------------------- CLI
def key_of(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def parse_vec(s: str, what: str) -> tuple[float, float, float]:
    try:
        v = [float(x) for x in s.split(",")]
        assert len(v) == 3
        return v[0], v[1], v[2]
    except Exception:  # noqa: BLE001
        raise SystemExit(f"usage: {what} expects three comma-separated numbers, got {s!r}") from None


def match(name: str, paths: list[str]) -> str:
    for p in paths:
        if name in (key_of(p), os.path.basename(p), p, os.path.normpath(p)):
            return p
    raise SystemExit(f"usage: no part named {name!r}; parts are {[key_of(p) for p in paths]}")


def load_mesh(path: str) -> trimesh.Trimesh:
    try:
        m = trimesh.load(path, force="mesh", process=True)
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"load error: {path}: {e}") from None
    if not isinstance(m, trimesh.Trimesh) or len(m.faces) == 0:
        raise SystemExit(f"load error: {path}: not a triangle mesh")
    return m


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("parts", nargs="+")
    ap.add_argument("--ref", action="append", default=[], metavar="NAME=reference.stl")
    ap.add_argument("--ref-dir", default=None, metavar="DIR", help="reference STL per part = DIR\\<stem minus --ref-strip-prefix>.stl")
    ap.add_argument("--ref-strip-prefix", default="", metavar="P")
    ap.add_argument("--pose", action="append", default=[], metavar="NAME=rx,ry,rz")
    ap.add_argument("--pose-all", default=None, metavar="rx,ry,rz")
    ap.add_argument("--place", action="append", default=[], metavar="NAME=dx,dy,dz", help="plate offset after the pose (reported boxes then read in plate coordinates)")
    ap.add_argument("--threshold", type=float, default=30.0, help="support_threshold_angle in degrees (default 30, 0.20mm Standard @BBL H2C)")
    ap.add_argument("--layer", type=float, default=0.2)
    ap.add_argument("--floor-eps", type=float, default=None, help="faces with centroid z <= this are first-layer plate contact (default layer/2)")
    ap.add_argument("--new-eps", type=float, default=0.05)
    ap.add_argument("--cantilever-warn", type=float, default=0.5)
    ap.add_argument("--json", default=None)
    try:
        a = ap.parse_args(argv[1:])
    except SystemExit as e:
        return 0 if e.code == 0 else 3
    try:
        floor_eps = a.floor_eps if a.floor_eps is not None else a.layer / 2.0
        poses, places, refs = {}, {}, {}
        if a.pose_all:
            poses = {key_of(p): parse_vec(a.pose_all, "--pose-all") for p in a.parts}
        for it in a.pose:
            if "=" not in it:
                raise SystemExit(f"usage: --pose expects NAME=rx,ry,rz, got {it!r}")
            n, r = it.split("=", 1)
            poses[key_of(match(n, a.parts))] = parse_vec(r, "--pose")
        for it in a.place:
            if "=" not in it:
                raise SystemExit(f"usage: --place expects NAME=dx,dy,dz, got {it!r}")
            n, r = it.split("=", 1)
            places[key_of(match(n, a.parts))] = parse_vec(r, "--place")
        for it in a.ref:
            if "=" not in it:
                raise SystemExit(f"usage: --ref expects NAME=reference.stl, got {it!r}")
            n, r = it.split("=", 1)
            refs[key_of(match(n, a.parts))] = r
        no_ref = []
        if a.ref_dir:
            for p in a.parts:
                k = key_of(p)
                if k in refs:
                    continue
                stem = k[len(a.ref_strip_prefix):] if a.ref_strip_prefix and k.startswith(a.ref_strip_prefix) else k
                cand = os.path.join(a.ref_dir, stem + ".stl")
                if os.path.isfile(cand):
                    refs[k] = cand
                else:
                    no_ref.append((k, cand))
        print(f"overhang_gate: {CONVENTION}")
        print(f"  threshold {a.threshold:g} deg, layer {a.layer:g} mm, floor-eps {floor_eps:g}, new-eps {a.new_eps:g}, cantilever-warn {a.cantilever_warn:g} mm (project value)")
        report = {"convention": CONVENTION, "threshold_deg": a.threshold, "layer_mm": a.layer, "floor_eps_mm": floor_eps, "parts": []}
        lvl = {"OK": 0, "WARN": 1, "FAIL": 2}
        worst = 0
        for p in a.parts:
            name = key_of(p)
            rot = poses.get(name, (0.0, 0.0, 0.0))
            plc = places.get(name, (0.0, 0.0, 0.0))
            mesh = posed(load_mesh(p), rot, plc)
            ref = posed(load_mesh(refs[name]), rot, plc) if name in refs else None
            r = analyse(mesh, a.threshold, a.layer, floor_eps, ref, a.new_eps, a.cantilever_warn)
            r.update({"name": name, "path": p, "pose_deg": list(rot), "place_mm": list(plc), "ref": refs.get(name)})
            miss = [c for k, c in no_ref if k == name]
            if miss:
                r["flags"].append(("WARN", f"no reference found for this part ({miss[0]}); whole-part figures only"))
            report["parts"].append(r)
            part_worst = max([lvl[f[0]] for f in r["flags"]] or [0])
            worst = max(worst, part_worst)
            frame = "plate coordinates" if any(abs(v) > 1e-12 for v in plc) else "model-centred posed frame"
            print(f"\n{name}  pose {rot}  place {plc} ({frame})  {'watertight' if r['watertight'] else 'NOT watertight'}  {r['faces']} faces  posed bbox {r['bbox_posed']}")
            print(f"  overhang below {a.threshold:g} deg: {r['overhang_below_threshold_mm2']} mm2 (min angle {r['min_angle_deg']}; bbox {r['overhang_bbox_posed']}); "
                  f"{a.threshold:g}-45: {r['band_threshold_to_45_mm2']} mm2; 45-60: {r['band_45_to_60_mm2']} mm2")
            if ref is not None:
                print(f"  reference {refs[name]}: overhang below {a.threshold:g} deg {r['ref_overhang_below_threshold_mm2']} mm2; "
                      f"NEW {r['new_overhang_mm2']} mm2 (faces > {a.new_eps:g} mm off the reference surface; bbox {r['new_overhang_bbox_posed']}), "
                      f"REMOVED {r['removed_overhang_mm2']} mm2, net {r['net_overhang_delta_mm2']:+} mm2")
            print(f"  per-layer cantilever max {r['max_cantilever_mm']} mm at z {r['max_cantilever_z']} ({r['layers']} layers, {r['nudged_layers']} re-cut; "
                  f"{r['layers_over_cantilever_warn']} over {a.cantilever_warn:g}); islands {len(r['islands'])}")
            if ref is not None:
                print(f"  NEW vs reference: cantilever {r['new_cantilever_mm']} mm at z {r['new_cantilever_z']} ({r['new_layers_over_cantilever_warn']} layer(s) over {a.cantilever_warn:g}); "
                      f"new islands {len(r['new_islands'])} (reference islands {len(r['ref_islands'])})")
            for lv, msg in r["flags"]:
                print(f"  [{lv}] {msg}")
            if not r["flags"]:
                print("  [OK] no flags")
        report["verdict"] = ["OK", "WARN", "FAIL"][worst]
        print(f"\nVERDICT: {report['verdict']}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=1)
        return worst
    except SystemExit as e:
        if isinstance(e.code, int):
            return e.code
        print(str(e.code), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
