r"""gcode_paths.py - parse a Bambu Studio plate G-code into per-layer, per-feature extrusion polylines, with G2/G3 arcs
interpolated to chords.

Why: with Quality > Precision > Arc fitting on (label not verified), Bambu Studio writes curved walls as G2/G3 moves. A
reader that skips them loses whole wall loops; a reader that treats them as straight lines under-counts path length.

What it reads (conventions seen in Bambu Studio 02.08 plate G-code):
  "; CHANGE_LAYER" then "; Z_HEIGHT: z" / "; LAYER_HEIGHT: h" starts a layer; "; FEATURE: <name>"; "; LINE_WIDTH: w";
  "; WIPE_START" .. "; WIPE_END" (moves inside are never extrusion paths); "; OBJECT_ID: n";
  "; start printing object, unique label id: n" / "; stop printing object ..."; T<n> tool lines;
  G0/G1 lines; G2 (clockwise) / G3 (counter-clockwise) with I/J centre offsets from the start point, or the R form
  (R > 0: the arc of 180 deg or less, R < 0: the larger arc); a G2/G3 with no X/Y (or end = start) is a full circle;
  G90/G91 absolute/relative XY(Z); M82/M83 absolute/relative E (M82/M83 overrides G90/G91 for E, as in Marlin; before
  either is seen, G91 means relative E and G90 follows `e_relative_default`, True = relative); G92 sets positions.
  Bambu firmware's own E-mode rules are not verified; the slices read so far send M83 before the first layer and their
  E values are only consistent with relative E.
Path rule: a path is a maximal run of consecutive extruding moves (E increase > 0, XY changes, outside a WIPE block)
inside one FEATURE block, one layer, one object and one tool. A non-extruding move with an X or Y word ends the path
(travel); pure-E moves (prime / unretract) and Z-only moves do not.
Arc interpolation: chord count n = ceil(|sweep| / step), step = min(MAX_STEP, 2 acos(1 - chord_tol / r)), so the sagitta of
every chord is <= chord_tol (default 0.02 mm) AND the chord polyline is within 0.1 % of the arc length (MAX_STEP 0.15 rad:
1 - sin(h)/h <= h^2/6 = 0.00094 at h = 0.075). The last point of an arc is the G-code end point itself.
Path.length is exact: straight parts + r * |sweep| for arcs (r = distance start -> centre, as Marlin uses);
Path.chord_length is the polyline length.

Not interpreted: the P word (number of extra turns) - in the slices read so far it occurs only on non-extruding spiral-lift
arcs ("G3 Z.6 I.. J.. P1"), which never become paths; it is counted in stats["arcs_with_p"]. What Bambu firmware does with P
is not verified. G2/G3 with the R form did not occur in any Bambu G-code read so far; it is implemented from the common
G-code convention and covered by the synthetic tests only.
Planes other than XY (G18/G19) are not supported (stats["non_xy_plane"] counts G18/G19 lines).

API:
  read_lines(path, plate=1)   lines of a .gcode file, or of Metadata/plate_<plate>.gcode inside a .3mf
  arc_geometry(x0, y0, x1, y1, cw, i=None, j=None, r=None) -> (cx, cy, radius, a0, sweep)   sweep < 0 = clockwise
  arc_points(x0, y0, x1, y1, cw, i, j, r, chord_tol, max_step) -> (points after the start, exact length, chord length)
  parse(path_or_lines, arcs="interpolate"|"chord"|"ignore", chord_tol=0.02, ...) -> Parsed
       arcs="chord" = arc as a straight line to its end point; arcs="ignore" = G2/G3 lines skipped entirely
       (position not updated). Both exist to compare with older readers.
Read-only; writes nothing; nothing here talks to a printer.
Usage (summary): .venv\Scripts\python.exe -B tools\gcode_paths.py <plate.gcode | file.3mf> [--plate N] [--arcs interpolate]
Example: .venv\Scripts\python.exe -B tools\gcode_paths.py work\slice\cube\plate_1.gcode
"""
from __future__ import annotations

import argparse
import collections
import math
import re
import sys
import zipfile
from dataclasses import dataclass, field

CHORD_TOL = 0.02          # mm, max sagitta of an interpolated chord
MAX_STEP = 0.15           # rad, max angle per chord (keeps the chord polyline within 0.1 % of the arc length)
TWO_PI = 2.0 * math.pi
_CMD = re.compile(r"^([GMT])(\d+)(?:\.(\d+))?")
_WORD = re.compile(r"([A-Z])\s*([-+]?(?:\d+\.?\d*|\.\d+))")
_OBJ_START = re.compile(r"^; start printing object, unique label id: (\d+)")
_OBJ_STOP = re.compile(r"^; stop printing object, unique label id: (\d+)")


@dataclass
class Path:
    layer: int                       # index into Parsed.layers; -1 = before the first "; CHANGE_LAYER"
    z: float | None                  # "; Z_HEIGHT" of the layer
    feature: str | None
    object_id: int | None            # "; OBJECT_ID:" marker
    label_id: int | None             # "; start printing object, unique label id:" marker
    tool: int | None
    width: float | None              # "; LINE_WIDTH" at the first move of the path
    pts: list = field(default_factory=list)   # [(x, y), ...] start point first
    length: float = 0.0              # exact: lines + r * |sweep|
    chord_length: float = 0.0        # polyline length
    arc_length: float = 0.0          # exact length of the arc parts only
    n_arcs: int = 0                  # G2/G3 moves in the path

    def closed(self, tol: float) -> bool:
        return len(self.pts) >= 2 and math.hypot(self.pts[-1][0] - self.pts[0][0], self.pts[-1][1] - self.pts[0][1]) <= tol


@dataclass
class Layer:
    index: int
    z: float | None
    height: float | None
    paths: list = field(default_factory=list)


@dataclass
class Parsed:
    header: dict
    preamble: Layer
    layers: list
    stats: dict


def read_lines(path: str, plate: int = 1):
    """Yield the lines of a G-code file, or of Metadata/plate_<plate>.gcode inside a .3mf (no extraction to disk)."""
    if path.lower().endswith(".3mf"):
        with zipfile.ZipFile(path) as zf:
            data = zf.read(f"Metadata/plate_{plate}.gcode").decode("utf-8", errors="replace")
        for line in data.splitlines(keepends=True):
            yield line
    else:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                yield line


def arc_geometry(x0: float, y0: float, x1: float, y1: float, cw: bool, i=None, j=None, r=None):
    """Centre, radius, start angle and signed sweep (rad; negative = clockwise) of a G2 (cw=True) / G3 arc.
    I/J form: centre = start + (I, J). R form: R > 0 = arc <= 180 deg, R < 0 = arc > 180 deg. End = start: full circle."""
    if i is not None or j is not None:
        cx, cy = x0 + (i or 0.0), y0 + (j or 0.0)
        rad = math.hypot(x0 - cx, y0 - cy)
    elif r is not None:
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy)
        if d == 0.0:
            raise ValueError("R-form arc with end point = start point is undefined")
        rad = abs(r)
        h = math.sqrt(max(rad * rad - d * d / 4.0, 0.0))     # R shorter than half the chord: clamp to a half circle
        side = 1.0 if cw else -1.0                           # short clockwise arc: centre right of start -> end
        if r < 0:
            side = -side
        cx = (x0 + x1) / 2.0 + side * h * dy / d
        cy = (y0 + y1) / 2.0 - side * h * dx / d
    else:
        raise ValueError("G2/G3 needs I/J or R")
    a0 = math.atan2(y0 - cy, x0 - cx)
    if math.hypot(x1 - x0, y1 - y0) < 1e-9:
        sweep = -TWO_PI if cw else TWO_PI
    else:
        a1 = math.atan2(y1 - cy, x1 - cx)
        if cw:
            sweep = -((a0 - a1) % TWO_PI)
        else:
            sweep = (a1 - a0) % TWO_PI
    return cx, cy, rad, a0, sweep


def arc_points(x0, y0, x1, y1, cw, i=None, j=None, r=None, chord_tol=None, max_step=None):
    """-> (points after the start point, ending exactly at (x1, y1); exact arc length r*|sweep|; chord polyline length).
    chord_tol / max_step None = the module values CHORD_TOL / MAX_STEP read at call time (not bound as default arguments,
    so a caller that changes the module values is honoured)."""
    chord_tol = CHORD_TOL if chord_tol is None else chord_tol
    max_step = MAX_STEP if max_step is None else max_step
    cx, cy, rad, a0, sweep = arc_geometry(x0, y0, x1, y1, cw, i, j, r)
    step = max_step
    if rad > chord_tol:
        step = min(step, 2.0 * math.acos(1.0 - chord_tol / rad))
    n = max(1, int(math.ceil(abs(sweep) / step - 1e-12)))
    pts = [(cx + rad * math.cos(a0 + sweep * k / n), cy + rad * math.sin(a0 + sweep * k / n)) for k in range(1, n)]
    pts.append((x1, y1))
    chord = 0.0
    px, py = x0, y0
    for qx, qy in pts:
        chord += math.hypot(qx - px, qy - py)
        px, py = qx, qy
    return pts, rad * abs(sweep), chord


def _words(code: str) -> dict:
    return {k: float(v) for k, v in _WORD.findall(code.upper())}


def parse(src, arcs: str = "interpolate", chord_tol: float | None = None, max_step: float | None = None,
          e_relative_default: bool = True, plate: int = 1) -> Parsed:
    """src = a path (.gcode or .3mf) or an iterable of lines. See the module docstring for the rules.
    chord_tol / max_step None = CHORD_TOL / MAX_STEP at call time."""
    if arcs not in ("interpolate", "chord", "ignore"):
        raise ValueError(arcs)
    lines = read_lines(src, plate) if isinstance(src, str) else src
    header: dict = {}
    stats = collections.Counter()
    preamble = Layer(-1, None, None)
    layers: list = []
    cur = preamble
    feat = None
    width = None
    obj = None
    label = None
    tool = None
    in_wipe = False
    abs_xy = True
    e_mode = None            # None = follow G90/G91; "rel" / "abs" after M83 / M82
    x = y = None
    z = None
    e_pos = 0.0
    path: Path | None = None
    max_r_mismatch = 0.0

    def flush():
        nonlocal path
        if path is not None and len(path.pts) >= 2:
            cur.paths.append(path)
        path = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(";"):
            if line.startswith("; CHANGE_LAYER"):
                flush()
                cur = Layer(len(layers), None, None)
                layers.append(cur)
            elif line.startswith("; Z_HEIGHT:"):
                cur.z = float(line.split(":", 1)[1])
            elif line.startswith("; LAYER_HEIGHT:"):
                try:
                    cur.height = float(line.split(":", 1)[1])
                except ValueError:
                    pass
            elif line.startswith("; FEATURE:"):
                flush()
                feat = line.split(":", 1)[1].strip()
            elif line.startswith("; LINE_WIDTH:"):
                try:
                    width = float(line.split(":", 1)[1])
                except ValueError:
                    pass
            elif line.startswith("; WIPE_START"):
                flush()
                in_wipe = True
            elif line.startswith("; WIPE_END"):
                in_wipe = False
            elif line.startswith("; OBJECT_ID:"):
                flush()
                try:
                    obj = int(line.split(":", 1)[1])
                except ValueError:
                    obj = None
            else:
                m = _OBJ_START.match(line)
                if m:
                    flush()
                    label = int(m.group(1))
                elif _OBJ_STOP.match(line):
                    flush()
                    label = None
                elif line.startswith("; ") and " = " in line:
                    k, v = line[2:].split(" = ", 1)
                    header[k.strip()] = v.strip()
            continue
        code = line.split(";", 1)[0].strip()
        m = _CMD.match(code.upper())
        if not m:
            continue
        letter, num, sub = m.group(1), int(m.group(2)), m.group(3)
        if letter == "T":
            flush()
            tool = num
            continue
        if letter == "M":
            if num == 82:
                e_mode = "abs"; stats["m82"] += 1
            elif num == 83:
                e_mode = "rel"; stats["m83"] += 1
            continue
        if sub is not None:
            continue                                     # G90.1 / G91.1 etc.: not position modes
        if num == 90:
            abs_xy = True; stats["g90"] += 1
            continue
        if num == 91:
            abs_xy = False; stats["g91"] += 1
            continue
        if num in (18, 19):
            stats["non_xy_plane"] += 1
            continue
        w = _words(code[m.end():])
        if num == 92:
            if "E" in w:
                e_pos = w["E"]
            if "X" in w:
                x = w["X"]
            if "Y" in w:
                y = w["Y"]
            if "Z" in w:
                z = w["Z"]
            stats["g92"] += 1
            continue
        if num not in (0, 1, 2, 3):
            continue
        is_arc = num in (2, 3)
        stats[f"g{num}"] += 1
        if is_arc and arcs == "ignore":
            stats["arcs_skipped"] += 1
            continue
        if not abs_xy:
            stats["relative_moves"] += 1
        # target position
        if abs_xy:
            nx, ny = w.get("X", x), w.get("Y", y)
            nz = w.get("Z", z)
        else:
            nx = None if x is None else x + w.get("X", 0.0)      # relative move from an unknown position stays unknown
            ny = None if y is None else y + w.get("Y", 0.0)
            nz = None if z is None else z + w.get("Z", 0.0)
        # extrusion amount
        de = 0.0
        if "E" in w:
            rel_e = (e_mode == "rel") or (e_mode is None and (not abs_xy or e_relative_default))
            if rel_e:
                de = w["E"]
            else:
                de = w["E"] - e_pos
            e_pos = w["E"] if not rel_e else e_pos + w["E"]
        has_xy = "X" in w or "Y" in w
        if is_arc:
            has_xy = True                                 # an arc moves the nozzle even with no X/Y (full circle)
            if "P" in w:
                stats["arcs_with_p"] += 1
            if "R" in w and "I" not in w and "J" not in w:
                stats["arcs_r_form"] += 1
            else:
                stats["arcs_ij_form"] += 1
            if "Z" in w:
                stats["arcs_helical"] += 1
        extruding = (de > 0 and has_xy and not in_wipe and x is not None and y is not None
                     and nx is not None and ny is not None)
        if extruding:
            if path is None:
                path = Path(cur.index, cur.z, feat, obj, label, tool, width, [(x, y)])
            if is_arc and arcs == "interpolate":
                cw = num == 2
                if "P" in w:
                    stats["extruding_arcs_with_p"] += 1
                pts, exact, chord = arc_points(x, y, nx, ny, cw, w.get("I"), w.get("J"), w.get("R"), chord_tol, max_step)
                if "I" in w or "J" in w:
                    cx, cy = x + w.get("I", 0.0), y + w.get("J", 0.0)
                    max_r_mismatch = max(max_r_mismatch, abs(math.hypot(nx - cx, ny - cy) - math.hypot(x - cx, y - cy)))
                path.pts.extend(pts)
                path.length += exact
                path.arc_length += exact
                path.chord_length += chord
                path.n_arcs += 1
                stats["extruding_arcs"] += 1
            else:
                seg = math.hypot(nx - x, ny - y)
                path.pts.append((nx, ny))
                path.length += seg
                path.chord_length += seg
                if is_arc:
                    path.n_arcs += 1
                    stats["extruding_arcs"] += 1
        elif has_xy:
            flush()
        x, y, z = nx, ny, nz
    flush()
    stats = dict(stats)
    stats["max_arc_end_radius_mismatch_mm"] = round(max_r_mismatch, 6)
    return Parsed(header, preamble, layers, stats)


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description="Summary of a plate G-code read by gcode_paths (paths, arcs, lengths per feature).")
    ap.add_argument("path")
    ap.add_argument("--plate", type=int, default=1)
    ap.add_argument("--arcs", default="interpolate", choices=["interpolate", "chord", "ignore"])
    a = ap.parse_args(argv[1:])
    p = parse(a.path, arcs=a.arcs, plate=a.plate)
    feats = collections.defaultdict(lambda: [0, 0.0, 0.0, 0])
    for L in [p.preamble] + p.layers:
        for q in L.paths:
            f = feats[q.feature]
            f[0] += 1; f[1] += q.length; f[2] += q.arc_length; f[3] += q.n_arcs
    print(f"gcode_paths: {a.path} (plate {a.plate}, arcs {a.arcs}); layers {len(p.layers)}; stats {p.stats}")
    for k, (n, ln, al, na) in sorted(feats.items(), key=lambda kv: str(kv[0])):
        print(f"  {str(k):28s} paths {n:7d}  length {ln:12.1f} mm  of which arcs {al:11.1f} mm in {na} arc moves")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
