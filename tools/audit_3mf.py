r"""audit_3mf.py - read a Bambu Studio 3MF and report the settings that most often cause failed prints.

What it does: opens the 3MF as a zip (read-only), reads the project, plate, slice and mesh records, and prints one
OK / WARN / FAIL line per check with the evidence. It never slices, sends, uploads or prints anything.
Slicer source references (bbs_3mf.cpp, PrintConfig.cpp, Print.cpp ...) are to https://github.com/bambulab/BambuStudio
at tag v02.08.02.61; "L123" is a line number in that file.

Inputs, read inside the 3MF:
  Metadata/project_settings.config  (JSON: global process/filament/printer settings)
  Metadata/model_settings.config    (XML: objects, parts, plates; per-plate filament_map_mode / filament_maps)
  Metadata/plate_N.json             (sliced 3MFs: bbox_objects per plate, filament ids, bed type)
  Metadata/slice_info.config, Metadata/plate_N.gcode(.md5)   (sliced 3MFs)
  Metadata/layer_config_ranges.xml  (Height range Modifiers), 3D/3dmodel.model + 3D/Objects/*.model (meshes)
Other inputs:
  knowledge\00-gear-inventory\current-load.md  your physical load record for C7 (--load-note to use another file;
                                                its header documents the table format)
  Bambu Studio's installed profiles and filament colour catalogue (C7, C8; located through config\paths.yaml)

Output: one line per finding (or --json); exit 0 = all OK, 1 = warnings, 2 = fails, 64 = a malformed --approve-swap.

Checks:
  C1 grouping: filament_map_mode per plate (plate metadata first, then global). With >= 2 filaments on a plate and
     mode "Auto For Flush" (Filament-Saving) or "Auto For Match" (Convenience) -> WARN: the slicer may put a filament
     on the LEFT extruder (on an H2C fed by an AMS on the right inlet, the left extruder takes an external spool only).
     "Manual" (Custom) -> OK.
  C2 filament_maps: lists which extruder each filament is bound to per plate (1-based index as stored). A sliced 3MF
     also stores the plate map in Metadata/slice_info.config, which the importer applies AFTER model_settings.config
     (bbs_3mf.cpp L1678-1682, L4666-4675), so that is the map the CLI slices: FAIL when the two files disagree; C7 L6
     judges the effective (slice_info) map. The proof of a grouping is the sliced G-code's "; filament_map =" line
     (gcode_audit.py prints it from the header).
  C3 max_bridge_length == 0 -> WARN "every bridge gets support" (Bambu profiles ship 0).
  C4 enable_support and support_threshold_angle reported.
  C5 object bboxes vs printable X range per plate: FAIL if any object leaves 25..325 mm (shared area) when two
     extruders are used, or the single-extruder area (left 0..325, right 25..330) when one is used.
     Areas default to the H2C machine profile values; override with --area-left/--area-right for another printer.
  C6 prime tower: enable_prime_tower, prime_tower_rib_wall, prime_tower_width, wipe_tower_x/y per plate. Clearance
     against objects is NOT computed here: run tools\tower_clearance.py on the sliced G-code.
  C7 physical load: compares the project with your load record (--load-note, default
     knowledge\00-gear-inventory\current-load.md), one [OK]/[WARN]/[FAIL] line per rule with the load row quoted.
     L1 FAIL if the note is missing, unreadable or has no "Verified: YYYY-MM-DD"; WARN if older than --load-max-age-days
        (default 7, a house choice) or in the future.
     L2 FAIL if the printer has no AMS/spool row. Rows are found by the printer model at the start of the first cell
        ("H2C - AMS 2 Pro slot 1 (RIGHT inlet)"); the model comes from printer_settings_id ("Bambu Lab H2C 0.4 nozzle"
        -> H2C). Each slot row is classified and reported: empty (OK), unknown ("not reported"/"unknown"/"?": WARN),
        loaded Bambu "**Bambu <product>, <colour>**" (OK, says which filament uses it), loaded third-party
        "**<Vendor> <product>, <colour>**" (WARN), loaded but not parsable (WARN).
     L5 FAIL if project filaments outnumber loaded (occupied) positions.
     L3 per filament: FAIL if no loaded row has its product (preset name without "@..."; third-party rows also match on
        filament_vendor + filament_type); Bambu rows: filament_ids must equal the line's fila_id in Bambu Studio's
        resources/profiles/BBL/filament/filaments_color_codes.json (WARN if the line is not in the catalogue).
     L4 colour (alpha FF ignored): OK if a catalogue colour of the loaded colour name; FAIL if it is the catalogue colour
        of a different colour name of the same line (a different spool was sliced); WARN otherwise (custom hex,
        third-party spool). Each filament takes a distinct loaded position.
     L6 (H2C) per-plate filament_maps = the matched slot's side (RIGHT = 2, LEFT = 1, read from "RIGHT" / "LEFT" in the
        row's first cell); mode must be Manual (then project filament_map must match too). A plate key that is not
        Manual while the project is Manual is re-read from the plate's G-code "; filament_map_mode =" (a CLI quirk).
        A non-Manual mode is FAIL, or WARN when a LEFT spool is recorded. Filaments without a load row are named as
        not checked.
     L7 curr_bed_type must match the start of the printer's plate-row content (FAIL otherwise); WARN when the row is not
        a physical check ("not re-confirmed", "not a today's check", "gear list") or the printer has no plate row.
  C8 filament profile vs printer/nozzle: each filament_settings_id's `compatible_printers` (installed system or user
     profile JSON) must contain the project's printer_settings_id; with two extruders the filament's extruder (filament_maps)
     must carry a nozzle_diameter the profile lists. FAIL if incompatible, WARN if the profile file is not found locally.
  C9 bed type vs filament (replicates Bambu Studio's validate(): Print.cpp L1674-1689 raises
     "Plate %d: %s does not support filament %s" when the filament's <bed>_temp for curr_bed_type is 0 -> FAIL);
     WARN when the bed temperature is outside the per-material plate range from the Bambu Lab wiki plate tables
     or at/above the filament's temperature_vitrification (GUI warning). On an H2 series printer (H2C/H2D/H2S) with a
     PLA/TPU filament that line is [OK] when cooling mode M145 P0 + chamber exhaust M106 P3 (they open the automatic top
     vent and rear grille; H2C user manual V1.0 p.13, https://wiki.bambulab.com/en/h2/manual/cooling-fan-system) are in
     the executable start section (after CONFIG_BLOCK_END, before MACHINE_START_GCODE_END) of every embedded plate
     G-code, else WARN; an unsliced 3MF (no plate G-code) is WARN "not verified: slice and re-audit". Other printers
     (P1S/X1/A1) and other materials keep the door/glass WARN unchanged.
  C10 sparse infill 100 % with a pattern Bambu Studio refuses at 100 % (PrintConfig.cpp L9528-9531; allowed: concentric,
     zig-zag, alignedrectilinear, hilbertcurve, archimedeanchords, octagramspiral) -> FAIL, resolved part > object > project
     (normal_part / modifier_part metadata in model_settings.config) and, for a Height range Modifier (Metadata/layer_config_ranges.xml),
     range > normal part > object > project (PrintObject.cpp L3105-3122 applies the range config after the volume's) while a
     modifier part's own key beats the range (PrintApply.cpp L797-799: a modifier starts from its parent region).
     The range file's object id is the 1-based build-item index of 3D/3dmodel.model (bbs_3mf.cpp L4171-4185, L4361-4372,
     L2210-2213, writer L7882-7890); an id without a build item -> WARN "not resolved".
  C11 source assignment (--source ORIGINAL.3mf): every printing part's filament line / type / colour vs the same part in
     the design-intent file (matched by part uuid, then object + part name, then part name); FAIL on an unapproved swap (line, type or
     catalogue colour name), WARN on a dropped source part or an unresolvable colour hex; --approve-swap "KEY=N:who/when" records
     the maker's approval per part (KEY = part uuid, part name or object name; N = filament index in the print file). Skipped (OK)
     without --source.
  C12 flat tops vs Ironing Type / Top surface pattern: the 3MF meshes are read (3D/3dmodel.model + 3D/Objects/*.model) and
     per object the up-facing flat area of its normal parts (normal within 5 deg of +Z) is measured with the topmost level and the flat area
     below it; the effective ironing_type / top_surface_pattern (object > project) is reported. A flat area >= --flat-top-min (400 mm2, a
     house value) with no --top-coupon-row cited -> WARN (state Ironing Type and Top surface pattern with a reason);
     'topmost' with flat area below the top level -> WARN (Fill.cpp L973 irons only the object's last layer). Negative parts
     are not subtracted. --no-geometry skips the mesh read (about 10 s on a 3 M-face file).
  C13 support Top Z: with support on, reports Top Z distance, top interface layers / spacing / filament, support_type / style and the
     style the slicer resolves (Default -> Tree Organic unless variable layer height or soluble; SupportParameters.hpp L136-156), the
     effective independent-support-layer-height (a prime tower with >= 2 filaments forces it off), per-object Top Z overrides, and the
     PREDICTED printed gap per layer height (Organic round(); Hybrid independent ON exact on flat ceilings / stacked to the grid inside a
     Height range Modifier; OFF accumulated; normal exact / rounded). WARN "NOT VERIFIED" until a scored support-removal coupon row is
     cited with --top-z-coupon-row (a Top Z is a measured value); the printed gap of a sliced plate is read back by
     tools\support_gap_readback.py.
  C14 one material family per object (house rule "one material per part unless multi-material is the point"; PLA and PETG
     bond weakly to each other): every printing part (normal_part, modifier_part) resolved to its filament (part > object > 1) plus the
     per-feature filament keys (wall / sparse infill / solid infill, PrintObject.cpp L3122-3147), mapped to filament_type families (PLA,
     PETG, TPU ...; the part before the first '-', so PLA-CF is PLA and PETG-HF is PETG), plus a Height range Modifier's `extruder` /
     per-feature keys for that object's normal parts. Objects are keyed by id. WARN when one object prints in more than one family
     (PLA + PETG named as the weak-bond pair); colour painting (paint_color in the object's mesh; seam painting is paint_seam,
     bbs_3mf.cpp L316-319) adds a WARN that painted filaments are not resolved here. Support and support-interface filaments (object
     keys support_filament / support_interface_filament) are left out on purpose: a support interface in another material is meant to
     separate from the part.
  C15 process preset (house rule "start from the printer's 0.20mm Standard preset; justify every deviation"): the expected preset is the
     printer's own default_print_profile recorded in the 3MF (0.20mm Standard @BBL H2C on the H2C; it follows the nozzle: 0.30mm
     Standard on an H2C 0.6, 0.10mm Standard on a 0.2). WARN when print_settings_id differs, or when the project layer_height differs
     from the layer height in the preset's name (every BBL system process name starts with its layer height; a 0.20mm Standard preset
     edited to 0.16 mm is not always listed in different_settings_to_system), or when an object, a Height range Modifier or a
     variable-layer-height profile sets another layer height; --process-reason "TEXT" records the sourced justification and turns those
     WARNs into OK lines (blank text counts as none).
  C16 stale slice: per plate of Metadata/slice_info.config, the embedded plate_N.gcode exists and matches its .md5, the
     slice_info prediction / weight equal the G-code HEADER's total estimated time / total filament weight, 22 project keys (preset, layer
     heights, filaments, support, infill, walls, shells, ironing, seam, brim, nozzle; keys the slicer normalises at slice time are left out)
     equal the G-code CONFIG block, slice_info filaments equal the project's filament table, the sliced objects (identify_id) equal the plate's
     instances, and no object is skipped / outside / supported without support. WARN on any disagreement: the other checks read the project,
     the printer runs the G-code. An unsliced 3MF is OK (nothing to compare). Not detected (the G-code CONFIG block is global only, GCode.cpp
     L2484-2515): object / part / Height range Modifier / painting edits made after slicing, and project keys outside the 22.

Usage: .venv\Scripts\python.exe tools\audit_3mf.py <file.3mf> [--json]
       [--load-note PATH] [--today YYYY-MM-DD] [--load-max-age-days N]
       [--source ORIGINAL.3mf] [--approve-swap "KEY=N:who/when" ...] [--process-reason "TEXT"] [--coupon-root DIR]
Example: .venv\Scripts\python.exe tools\audit_3mf.py work\slice\cube\out.3mf
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
import zipfile
import hashlib   # C16 md5 of the embedded plate G-code (P21)
import xml.etree.ElementTree as ET
import math
import numpy as np   # C12 geometry; the venv has numpy

H2C_LEFT = (0.0, 325.0)
H2C_RIGHT = (25.0, 330.0)
H2C_SHARED = (25.0, 325.0)
# C8/C9 data ------------------------------------------------------------------------------------------------------
import os  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_config  # noqa: E402


def _profile_roots() -> list[str]:
    """Installed filament profile folders in search order: system BBL, user presets, install folder (config\\paths.yaml)."""
    try:
        roots = [str(r / "BBL" / "filament") for r in mm_config.bambu_profile_roots()]
        user = mm_config.bambu_user_presets_dir()
    except Exception:  # noqa: BLE001  (a broken config must not stop the other checks; C8 then WARNs "not found")
        return []
    if user is not None:
        roots.insert(1, str(user))
    return roots


PROFILE_ROOTS = _profile_roots()
# curr_bed_type -> project key prefix (PrintConfig.cpp BedType enum names; Print.cpp get_bed_temp_key)
BED_KEY = [
    ("supertack", "supertack_plate_temp"), ("textured cool", "cool_plate_temp"), ("cool", "cool_plate_temp"),
    ("engineering", "eng_plate_temp"), ("high temp", "hot_plate_temp"), ("smooth pei", "hot_plate_temp"),
    ("textured", "textured_plate_temp"),
]
# per-material bed-temperature ranges by plate family, from the Bambu Lab wiki plate tables
PLATE_RANGE = {
    "pei": {"PLA": (45, 65), "PETG": (60, 80), "ABS": (90, 100), "ASA": (90, 100), "PC": (100, 120), "PA": (100, 120)},
    "cool": {"PLA": (35, 45), "PETG": None},  # None = not recommended on this plate
    "supertack": {"PLA": (40, 40), "PETG": (55, 65)},
}


# C10: sparse infill patterns Bambu Studio accepts at 100 % density (config values; PrintConfig.cpp v02.08.02.61 L9528-9531;
# wiki "Only the following pattern types support 100% density fill"): Concentric, Rectilinear (stored "zig-zag"), Aligned Rectilinear,
# Hilbert Curve, Archimedean Chords, Octagram Spiral.
SOLID_OK_PATTERNS = {"concentric", "zig-zag", "alignedrectilinear", "hilbertcurve", "archimedeanchords", "octagramspiral"}
C10_PART_SUBTYPES = {"normal_part", "modifier_part"}   # part subtypes whose own sparse_infill_* keys print infill (others carry none)


def bed_family(bed: str) -> str:
    b = (bed or "").lower()
    if "supertack" in b:
        return "supertack"
    if "cool" in b and "textured" not in b:
        return "cool"
    return "pei"


def bed_temp_key(bed: str) -> str | None:
    b = (bed or "").lower()
    for needle, key in BED_KEY:
        if needle in b:
            return key
    return None


def find_filament_profile(name: str) -> dict | None:
    """Locate an installed filament profile JSON by its name (system BBL, then user presets, then the install folder)."""
    for root in PROFILE_ROOTS:
        if not root or not os.path.isdir(root):
            continue
        for dirpath, _d, files in os.walk(root):
            for fn in files:
                if fn.lower() == (name + ".json").lower():
                    try:
                        with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
                            j = json.load(f)
                        j["__path__"] = os.path.join(dirpath, fn)
                        return j
                    except Exception:  # noqa: BLE001
                        return None
    return None


def resolve_compatible_printers(name: str, depth: int = 0) -> tuple[list[str] | None, str | None]:
    j = find_filament_profile(name)
    if j is None:
        return None, None
    cp = j.get("compatible_printers")
    if cp:
        return list(cp), j["__path__"]
    if depth < 6 and j.get("inherits"):
        return resolve_compatible_printers(j["inherits"], depth + 1)
    return [], j["__path__"]


MODE_LABEL = {
    "Auto For Flush": "Filament-Saving Mode",
    "Auto For Match": "Convenience Mode",
    "Manual": "Custom",
    "Nozzle Manual": "Nozzle Manual",
    "Auto For Quality": "Quality Mode",
    None: "(absent = Default)",
}


# C7 data ---------------------------------------------------------------------------------------------------------
import datetime as _dt  # noqa: E402

LOAD_NOTE = str(mm_config.repo_root() / "knowledge" / "00-gear-inventory" / "current-load.md")


def _color_codes_path() -> str:
    """Bambu Studio's filament colour catalogue: bambu_profiles_dir if set, else the install folder (config\\paths.yaml)."""
    rel = ("BBL", "filament", "filaments_color_codes.json")
    try:
        own = mm_config.optional_path("bambu_profiles_dir")
        if own is not None:
            return str(own.joinpath(*rel))
        inst = mm_config.bambu_install_dir()
    except Exception:  # noqa: BLE001
        inst = None
    return str(inst.joinpath("resources", "profiles", *rel)) if inst is not None else ""


COLOR_CODES = _color_codes_path()
# used only if COLOR_CODES is unreadable: PLA Basic Black, code 10101, fila_id GFA00, #000000FF (same JSON)
COLOR_FALLBACK = {"pla basic": ("GFA00", {"black": {"#000000"}})}
_color_index: dict | None = None
BOLD_FIL = re.compile(r"\*\*([^*,]+?),\s*([^*]+?)\*\*")
PLAIN_BAMBU = re.compile(r"(Bambu [A-Z][A-Za-z0-9+ \-]*?),\s*([A-Z][A-Za-z]*(?: [A-Z][A-Za-z]*)*)")
EMPTY_RX = re.compile(r"^(empty|no filament|none)\b", re.I)
UNKNOWN_RX = re.compile(r"not reported|unknown|^\?|\?$", re.I)
UNCONFIRMED_RX = re.compile(r"not re-confirmed|not a today.s check|gear list", re.I)


def norm_colour(c: str) -> str:
    c = (c or "").strip().upper()
    return c[:7] if len(c) == 9 and c.endswith("FF") else c


def colour_index() -> dict:
    """fila_type lower -> (fila_id, {English colour name lower: {normalised hex}}) from Bambu Studio's catalogue."""
    global _color_index
    if _color_index is None:
        idx: dict = {}
        try:
            with open(COLOR_CODES, encoding="utf-8") as f:
                for e in json.load(f).get("data", []):
                    t = (e.get("fila_type") or "").lower()
                    name = ((e.get("fila_color_name") or {}).get("en") or "").lower()
                    _fid, names = idx.setdefault(t, (e.get("fila_id"), {}))
                    names.setdefault(name, set()).update(norm_colour(c) for c in e.get("fila_color") or [])
        except Exception:  # noqa: BLE001
            idx = {k: (v[0], {n: set(s) for n, s in v[1].items()}) for k, v in COLOR_FALLBACK.items()}
        _color_index = idx
    return _color_index


def iso_date(s: str):
    try:
        return _dt.date.fromisoformat(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {s!r}") from None


def classify_row(content: str) -> dict:
    """empty / unknown / loaded (parsed Bambu, parsed third-party, or not parsed)."""
    plain = content.replace("**", "").strip()
    m = BOLD_FIL.search(content)  # a bold "Product, Colour" is a load statement even if the row adds "unknown"/"?"
    if not m and EMPTY_RX.match(plain):
        return {"state": "empty"}
    if not m and UNKNOWN_RX.search(plain):
        return {"state": "unknown"}
    m = m or PLAIN_BAMBU.search(content)
    if not m:
        return {"state": "loaded", "parsed": False}
    product, colour = m.group(1).strip(), m.group(2).strip()
    bambu = product.lower().startswith("bambu ")
    return {"state": "loaded", "parsed": True, "product": product, "colour": colour, "bambu": bambu,
            "vendor": "Bambu Lab" if bambu else product.split()[0]}


def gcode_map(z, plate_no: int) -> list[str] | None:
    """'; filament_map = 2,1' from a sliced plate's G-code inside the 3MF -> ['2', '1'] (None if not sliced / not found). The sliced
    header is the only proof of the grouping."""
    try:
        with z.open(f"Metadata/plate_{plate_no}.gcode") as g:
            for ln in g:
                if ln.startswith(b"; filament_map = "):
                    return [v.strip() for v in ln.split(b"=", 1)[1].decode("utf-8", "replace").split(",") if v.strip()]
                if ln.startswith(b"; EXECUTABLE_BLOCK_START"):   # the CONFIG block (lines 17-585 on a Bambu plate) is before the moves; stop there
                    break
    except KeyError:
        return None
    return None


def gcode_map_mode(z, plate_no: int) -> str | None:
    """'; filament_map_mode = X' from a sliced plate's G-code inside the 3MF (None if not sliced / not found)."""
    try:
        with z.open(f"Metadata/plate_{plate_no}.gcode") as g:
            for ln in g:
                if ln.startswith(b"; filament_map_mode = "):
                    return ln.split(b"=", 1)[1].strip().decode("utf-8", "replace")
    except KeyError:
        return None
    return None


def check_load(ps: dict, plates: list, note_path: str, today, max_age: int, add, z=None) -> None:
    """C7: compare the project's filaments, grouping and bed with the physical load note (rules L1-L7)."""
    if not os.path.isfile(note_path):
        add("FAIL", "C7", f"L1: load note {note_path} MISSING - no filament can be confirmed loaded", rule="L1")
        return
    try:
        with open(note_path, encoding="utf-8") as f:
            note = f.read()
    except Exception as e:  # noqa: BLE001
        add("FAIL", "C7", f"L1: load note {note_path} unreadable ({type(e).__name__}) - no filament can be confirmed loaded", rule="L1")
        return
    m = re.search(r"Verified:\s*(\d{4}-\d{2}-\d{2})", note)
    vdate = None
    if m:
        try:
            vdate = _dt.date.fromisoformat(m.group(1))
        except ValueError:
            vdate = None
    if vdate is None:
        add("FAIL", "C7", f"L1: {note_path} has no valid 'Verified: YYYY-MM-DD' ({m.group(1) if m else 'MISSING'}) - undated load = unknown load", rule="L1")
    else:
        age = (today - vdate).days
        if age < 0:
            add("WARN", "C7", f"L1: {note_path} Verified: {vdate} is in the future relative to {today}", rule="L1")
        elif age > max_age:
            add("WARN", "C7", f"L1: {note_path} Verified: {vdate} is {age} days old (> {max_age}); re-check what is loaded and update the note", rule="L1")
        else:
            add("OK", "C7", f"L1: {note_path} Verified: {vdate} ({age} day(s) before {today})", rule="L1")

    printer = ps.get("printer_settings_id") or ""
    key = printer_key(printer)
    rows = []  # [position, content, how known, raw]
    for ln in note.splitlines():
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2:
                rows.append((cells[0], cells[1], cells[2] if len(cells) > 2 else "", ln.strip()))
    fil_rows = [r for r in rows if key and _row_is(r[0], key)
                and re.search(r"AMS|spool", r[0]) and not re.search(r"Vortek|hotend|plate", r[0], re.I)]
    if not fil_rows:
        add("FAIL", "C7", f"L2: printer {printer!r}: no filament-position row for {key or 'this printer'} in the load table", rule="L2")
    slots = []
    for pos, content, _how, raw in fil_rows:
        d = classify_row(content)
        d.update(pos=pos, row=raw, ext=2 if "RIGHT" in pos else (1 if "LEFT" in pos else None))
        slots.append(d)
    loaded = [d for d in slots if d["state"] == "loaded"]  # parsed or not: an occupied position
    parsed = [d for d in loaded if d["parsed"]]

    fset = ps.get("filament_settings_id") or []
    fids = ps.get("filament_ids") or []
    fcol = ps.get("filament_colour") or []
    ftypes = ps.get("filament_type") or []
    fvend = ps.get("filament_vendor") or []
    n = len(fset)
    add("OK" if 1 <= n <= len(loaded) else "FAIL", "C7",
        f"L5: {n} filament(s) in project {fset}; {len(loaded)} loaded position(s) on {key or printer!r}", rule="L5")

    idx = colour_index()

    def line(d):
        t = d["product"].lower()
        return idx.get(t[6:] if t.startswith("bambu ") else t)

    def hexes(d):
        e = line(d)
        return e[1].get(d["colour"].lower(), set()) if e else set()

    used: set[int] = set()
    matched: dict[int, dict] = {}
    for i, prof in enumerate(fset):
        product = re.sub(r"\s*@.*$", "", prof or "").strip()
        fid = fids[i] if i < len(fids) else None
        col = norm_colour(fcol[i]) if i < len(fcol) else ""
        ftype = (ftypes[i] if i < len(ftypes) else "") or ""
        vendor = (fvend[i] if i < len(fvend) else "") or ""

        def fits(d):
            if d["product"].lower() == product.lower():
                return True
            if d["bambu"]:
                return False
            return (bool(vendor) and vendor.lower() == d["vendor"].lower() and bool(ftype)
                    and re.search(rf"\b{re.escape(ftype)}\b", d["product"], re.I) is not None)
        cands = [j for j, d in enumerate(parsed) if j not in used and fits(d)]
        if not cands:
            unparsed = [d["pos"] for d in loaded if not d["parsed"]]
            add("FAIL", "C7", f"L3: filament {i + 1} {prof!r} ({fid}, {col}): product {product!r} is not loaded on {key or printer!r} "
                f"(loaded: {[d['product'] + ', ' + d['colour'] + ' @ ' + d['pos'] for d in parsed] or 'nothing parsed'}"
                + (f"; unparsed loaded rows {unparsed} cannot confirm it" if unparsed else "") + ")", rule="L3", filament=i + 1)
            add("FAIL", "C7", f"L4: filament {i + 1} colour {col}: no load row to compare with", rule="L4", filament=i + 1)
            continue
        j = next((j for j in cands if col in hexes(parsed[j])), cands[0])
        d = parsed[j]
        used.add(j)
        matched[i] = d
        if not d["bambu"]:
            add("OK", "C7", f"L3: filament {i + 1} {prof!r} third-party: filament_vendor {vendor!r} / filament_type {ftype!r} "
                f"match load row {d['row']} (no catalogue filament_ids for non-Bambu spools)", rule="L3", filament=i + 1)
            add("WARN", "C7", f"L4: filament {i + 1} colour {col} vs {d['colour']}: third-party spool, no catalogue colour; "
                "identity rests on L3; confirm the AMS mapping by eye", rule="L4", filament=i + 1)
            continue
        e = line(d)
        if e is None:
            add("WARN", "C7", f"L3: filament {i + 1} {prof!r}: product line {d['product']!r} not in {COLOR_CODES}; filament_ids {fid!r} unprovable; load row {d['row']}", rule="L3", filament=i + 1)
        else:
            add("OK" if fid == e[0] else "FAIL", "C7",
                f"L3: filament {i + 1} {prof!r} filament_ids {fid!r} vs {e[0]!r} for {d['product']}; load row {d['row']}", rule="L3", filament=i + 1)
        want = hexes(d)
        other = sorted(nm for nm, s in (e[1].items() if e else []) if nm != d["colour"].lower() and col in s)
        if col in want:
            add("OK", "C7", f"L4: filament {i + 1} filament_colour {col} is a catalogue colour of {d['product']} {d['colour']} {sorted(want)}", rule="L4", filament=i + 1)
        elif other:
            add("FAIL", "C7", f"L4: filament {i + 1} filament_colour {col} is the catalogue colour of {d['product']} {other}, "
                f"not the loaded {d['colour']} {sorted(want)} - a different spool was sliced", rule="L4", filament=i + 1)
        else:
            add("WARN", "C7", f"L4: filament {i + 1} colour {col} is not a catalogue colour of {d['product']} {d['colour']} {sorted(want)}; "
                "identity rests on L3 (filament_ids); confirm the AMS mapping by eye", rule="L4", filament=i + 1)

    # one row per load-table slot (print-qa item 1-2: "slot by slot")
    users = {id(d): i for i, d in matched.items()}
    for d in slots:
        if d["state"] == "empty":
            add("OK", "C7", f"L2: slot {d['pos']}: empty; load row {d['row']}", rule="L2")
        elif d["state"] == "unknown":
            add("WARN", "C7", f"L2: slot {d['pos']}: unknown (row says: {d['row']})", rule="L2")
        elif not d["parsed"]:
            add("WARN", "C7", f"L2: slot {d['pos']}: loaded, not parsed (non-Bambu or free text); confirm by hand; load row {d['row']}", rule="L2")
        else:
            use = (f"used by filament {users[id(d)] + 1} {fset[users[id(d)]]!r}" if id(d) in users else "loaded, not used by this project")
            tp = "" if d["bambu"] else " (third-party: identity by vendor/type only)"
            add("OK" if d["bambu"] else "WARN", "C7", f"L2: slot {d['pos']}: {use}{tp}; load row {d['row']}", rule="L2")

    if key == "H2C":
        gmode = ps.get("filament_map_mode")
        gmap = [str(x) for x in (ps.get("filament_map") or [])]
        bad, warn, notes = [], [], []
        pmodes, pmaps = [], []
        for k, p in enumerate(plates, 1):
            pm = p["meta"].get("filament_map_mode")
            if pm is not None and pm != "Manual" and gmode == "Manual" and z is not None:
                gm = gcode_map_mode(z, k)  # CLI quirk: plate key Auto For Flush, G-code Manual
                if gm == "Manual":
                    notes.append(f"plate {k}: key {pm!r} but G-code filament_map_mode = Manual (CLI quirk)")
                    pm = "Manual"
            if pm is not None:
                pmodes.append(pm)
            eff = p.get("effective_maps", p["meta"].get("filament_maps"))   # slice_info.config overrides model_settings on import
            if eff is not None:
                pmaps.append(eff)
        manual = gmode == "Manual" and all(v == "Manual" for v in pmodes)
        if not manual:
            if any(d["ext"] == 1 for d in loaded):  # grouping rule: Auto For Flush only with a left spool recorded
                warn.append("mode not Manual (Custom); acceptable only because a LEFT spool is recorded - per-plate maps checked")
            else:
                bad.append("mode not Manual (Custom) and no LEFT spool recorded")
        if not pmaps:
            bad.append("no plate filament_maps")
        for i, d in matched.items():
            want = str(d["ext"]) if d["ext"] else None
            if want is None:
                bad.append(f"filament {i + 1}: side of {d['pos']!r} unknown")
                continue
            # project-level filament_map is only the stored default outside Manual mode
            if manual and (gmap[i] if i < len(gmap) else None) != want:
                bad.append(f"filament {i + 1}: project filament_map {gmap[i] if i < len(gmap) else None!r} != {want}")
            for k, v in enumerate(pmaps):
                vv = v.split()
                if (vv[i] if i < len(vv) else None) != want:
                    bad.append(f"filament {i + 1}: plate map #{k + 1} {v!r} != {want}")
            # the sliced G-code header is the proof; FAIL when it names another side than the load
            if z is not None:
                for k in range(1, len(plates) + 1):
                    gm = gcode_map(z, k)
                    if gm is not None and (gm[i] if i < len(gm) else None) != want:
                        bad.append(f"filament {i + 1}: plate {k} G-code '; filament_map = {','.join(gm)}' != {want} (the sliced grouping, not the input file's)")
        skipped = [i + 1 for i in range(n) if i not in matched]
        add("FAIL" if bad else ("WARN" if warn else "OK"), "C7",
            f"L6: filament_map_mode={gmode!r} plates={pmodes} filament_map={gmap} plate filament_maps={pmaps}; expected "
            f"{ {i + 1: d['ext'] for i, d in matched.items()} } (2 = RIGHT = AMS 2 Pro inlet, 1 = LEFT external spool)"
            + (f"; not checked (no load row, see L3): filament(s) {skipped}" if skipped else "")
            + (f"; {notes}" if notes else "") + (f"; problems: {bad + warn}" if bad or warn else ""), rule="L6")

    bed = ps.get("curr_bed_type") or ""
    prow = next((r for r in rows if key and _row_is(r[0], key) and "plate" in r[0].lower()), None)
    if prow is None:
        add("WARN", "C7", f"L7: curr_bed_type {bed!r}; the load note has no plate row for {key or printer!r}", rule="L7")
    else:
        name = re.sub(r"\s*Plate$", "", bed).strip().lower()
        plain = prow[1].replace("**", "").strip().lower()
        if not name or not re.match(rf"{re.escape(name)}\b", plain):
            add("FAIL", "C7", f"L7: curr_bed_type {bed!r} but the plate row names another plate: {prow[3]}", rule="L7")
        elif UNCONFIRMED_RX.search(prow[1] + " " + prow[2]):
            add("WARN", "C7", f"L7: curr_bed_type {bed!r} matches {prow[3]}, but the plate was not physically confirmed", rule="L7")
        else:
            add("OK", "C7", f"L7: curr_bed_type {bed!r} vs load row {prow[3]}", rule="L7")


# C9 printer split (H2C user manual V1.0 p.13; https://wiki.bambulab.com/en/h2/manual/cooling-fan-system) ----------------


def printer_key(printer: str) -> str | None:
    """Printer model used to find its rows in the load note: 'H2C' and 'P1S' as before; any other Bambu printer from
    'Bambu Lab <model> 0.4 nozzle' (e.g. 'X1C', 'A1 mini'). None when the name has neither form."""
    if "H2C" in printer:
        return "H2C"
    if "P1S" in printer:
        return "P1S"
    m = re.match(r"^Bambu Lab (.+?) \d+(?:\.\d+)? nozzle", printer or "")
    return m.group(1).strip() if m else None


def _row_is(pos: str, key: str) -> bool:
    """True when a load-table position cell starts with the printer model and a separator: 'H2C - AMS ...' or 'H2C · AMS ...'."""
    return re.match(rf"^{re.escape(key)}\s*[·:\-]\s", pos) is not None
H2_SERIES = re.compile(r"\bH2[CDS]\b")
COOLING_TYPES = ("PLA", "TPU")  # "low heat resistance, such as PLA/TPU" (wiki.bambulab.com/en/h2/manual/cooling-fan-system)


def start_cooling_cmds(z) -> dict[int, tuple[bool, bool]]:
    """plate -> (M145 P0 found, M106 P3 S>0 found) in the executable start section of each embedded plate G-code
    (after '; CONFIG_BLOCK_END', up to '; MACHINE_START_GCODE_END'; comment lines and the config block are ignored)."""
    out: dict[int, tuple[bool, bool]] = {}
    if z is None:
        return out
    for name in z.namelist():
        mm = re.match(r"Metadata/plate_(\d+)\.gcode$", name)
        if not mm:
            continue
        m145 = m106 = False
        started = False
        with z.open(name) as g:
            for raw in g:
                ln = raw.strip()
                if not started:
                    started = ln.startswith(b"; CONFIG_BLOCK_END")
                    continue
                if ln.startswith(b"; MACHINE_START_GCODE_END"):
                    break
                if ln.startswith(b";"):
                    continue
                code = ln.split(b";", 1)[0].split()
                if code[:2] == [b"M145", b"P0"]:
                    m145 = True
                if code[:2] == [b"M106", b"P3"] and any(t.startswith(b"S") and t[1:] not in (b"0", b"") for t in code[2:]):
                    m106 = True
        out[int(mm.group(1))] = (m145, m106)
    return out


def read_json(z: zipfile.ZipFile, name: str):
    try:
        return json.loads(z.read(name).decode("utf-8"))
    except KeyError:
        return None


def parse_model_settings(z: zipfile.ZipFile):
    try:
        xml = z.read("Metadata/model_settings.config")
    except KeyError:
        return [], []
    root = ET.fromstring(xml)
    objects = []
    for obj in root.iter("object"):
        name = None
        meta = {}
        for md in obj.findall("metadata"):   # object-level overrides (direct children of <object>)
            k = md.get("key")
            if k is None:
                continue
            meta[k] = md.get("value")
            if k == "name":
                name = md.get("value")
        parts = []   # part-level overrides (bbs_3mf.cpp v02.08.02.61 L8291-8292 writes volume->config as <metadata> inside <part>); read for C10
        for pt in obj.findall("part"):
            pmeta = {md.get("key"): md.get("value") for md in pt.findall("metadata") if md.get("key") is not None}
            parts.append({"id": pt.get("id"), "subtype": pt.get("subtype") or "normal_part", "name": pmeta.get("name"), "meta": pmeta,
                          "uuid": pt.get("uuid")})   # part guid: bbs_3mf.cpp v02.08.02.61 L8240-8241 writes, L4510/L5464 read; kept on Split (Model.cpp L2766-2776),
                                                     # regenerated on the set_mesh repair path (Model.cpp L3697). C11 matches on it
        objects.append({"id": obj.get("id"), "name": name, "meta": meta, "parts": parts})
    plates = []
    for n, pl in enumerate(root.iter("plate"), 1):
        meta = {md.get("key"): md.get("value") for md in pl.findall("metadata")}
        inst = []
        for i in pl.findall("model_instance"):   # Bambu writes the ids as <metadata key="object_id" value="N"/> children, not attributes
            md = {m.get("key"): m.get("value") for m in i.findall("metadata") if m.get("key")}
            inst.append({"object_id": md.get("object_id", i.get("object_id")), "instance_id": md.get("instance_id", i.get("instance_id")), "identify_id": md.get("identify_id")})
        try:
            pid = int(meta.get("plater_id", n))   # the importer keys plates by plater_id (bbs_3mf.cpp v02.08.02.61 L4614-4616, L4979), not by position
        except ValueError:
            pid = n
        plates.append({"meta": meta, "instances": inst, "plater_id": pid, "position": n})
    return objects, plates


# C12 geometry: flat up-facing area per object from the 3MF meshes --------------------------------------------------------------
FLAT_UP_DEG = 5.0          # house value: a face counts as a flat top when its normal is within 5 deg of +Z; no slicer source
FLAT_TOP_MIN_MM2 = 400.0   # house value: proposed threshold for "a large flat visible top"; no slicer source
FLAT_LEVELS_N = 5          # how many flat levels (by area) are reported per object


def _xf(s: str | None) -> tuple[np.ndarray, str | None]:
    """3MF transform attribute (12 numbers, row-vector convention m00 m01 m02 m10 .. m22 m30 m31 m32; core spec 3.3; Bambu reads it the same way,
    bbs_3mf.cpp v02.08.02.61 L593-619) -> (4x4 column-vector matrix, warning or None). A malformed string gives identity + a warning, as the
    slicer itself falls back to identity (L608)."""
    T = np.eye(4)
    if not s:
        return T, None
    try:
        v = [float(x) for x in s.split()]
    except ValueError:
        return T, f"transform {s!r} is not numeric: identity used"
    if len(v) != 12:
        return T, f"transform has {len(v)} numbers, not 12: identity used"
    T[:3, :3] = np.array(v[:9]).reshape(3, 3).T
    T[:3, 3] = v[9:12]
    return T, None


def _tag(e) -> str:
    return e.tag.split("}", 1)[-1]


def parse_geometry(z: zipfile.ZipFile, keep: dict[str, set] | None = None) -> tuple[dict[str, list[dict]], list[str]]:
    """({build object id: [{"part_id", "verts" (N,3) in plate coordinates, "faces" (M,3)}]}, warnings) from 3D/3dmodel.model (build items,
    components with p:path) and 3D/Objects/*.model (meshes). Bambu writes one mesh per part (component objectid = model_settings <part id>);
    world = T_item @ T_component @ v (bbs_3mf.cpp v02.08.02.61 L5398). `keep` = {object id: {part ids to parse}} skips
    the other meshes (a large negative part need not be read). A nested component (an object of components inside a component;
    legal 3MF, never written by Bambu) is skipped with a warning. Parsed with ElementTree (no lxml in the venv). Empty when the file has no
    3D/3dmodel.model."""
    warnings: list[str] = []
    try:
        root = ET.fromstring(z.read("3D/3dmodel.model"))
    except KeyError:
        return {}, warnings
    cache: dict[str, dict] = {}

    def meshes_of(path: str) -> dict:
        if path not in cache:
            d = {}
            try:
                r = ET.fromstring(z.read(path))
            except KeyError:
                cache[path] = d
                return d
            for obj in r.iter():
                if _tag(obj) != "object":
                    continue
                mesh = next((c for c in obj if _tag(c) == "mesh"), None)
                if mesh is None:
                    continue
                vs = [(float(v.get("x")), float(v.get("y")), float(v.get("z"))) for v in mesh.iter() if _tag(v) == "vertex"]
                ts = [(int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))) for t in mesh.iter() if _tag(t) == "triangle"]
                d[obj.get("id")] = (np.array(vs, dtype=float).reshape(-1, 3), np.array(ts, dtype=np.int64).reshape(-1, 3))
            cache[path] = d
        return cache[path]

    objects = {o.get("id"): o for o in root.iter() if _tag(o) == "object"}
    out: dict[str, list[dict]] = {}
    for it in root.iter():
        if _tag(it) != "item":
            continue
        oid = it.get("objectid")
        T_item, w = _xf(it.get("transform"))
        if w:
            warnings.append(f"build item {oid}: {w}")
        obj = objects.get(oid)
        if obj is None:
            continue
        parts = []
        comps = next((c for c in obj if _tag(c) == "components"), None)
        if comps is not None:
            for c in comps:
                if _tag(c) != "component":
                    continue
                pid = c.get("objectid")
                if keep is not None and pid not in keep.get(oid, set()):
                    continue
                path = (c.get("{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}path") or c.get("path") or "/3D/3dmodel.model").lstrip("/")
                m = meshes_of(path).get(pid)
                if m is None:
                    sub_obj = objects.get(pid) if path == "3D/3dmodel.model" else None
                    if sub_obj is not None and next((cc for cc in sub_obj if _tag(cc) == "components"), None) is not None:
                        warnings.append(f"object {oid} component {pid}: nested component (an object of components) skipped; its faces are not measured")
                    continue
                T_c, wc = _xf(c.get("transform"))
                if wc:
                    warnings.append(f"object {oid} component {pid}: {wc}")
                V, F = m
                Vh = np.c_[V, np.ones(len(V))] @ (T_item @ T_c).T
                parts.append({"part_id": pid, "verts": Vh[:, :3], "faces": F})
        else:
            mesh = next((c for c in obj if _tag(c) == "mesh"), None)
            if mesh is not None and (keep is None or oid in keep.get(oid, {oid})):
                m = meshes_of("3D/3dmodel.model").get(oid)
                if m is not None:
                    V, F = m
                    Vh = np.c_[V, np.ones(len(V))] @ T_item.T
                    parts.append({"part_id": oid, "verts": Vh[:, :3], "faces": F})
        out[oid] = parts
    return out, warnings


def flat_up_faces(verts: np.ndarray, faces: np.ndarray) -> dict:
    """Up-facing flat faces (normal within FLAT_UP_DEG of +Z) of the stacked normal parts of ONE OBJECT, above the object's lowest 0.05 mm:
    total area, the topmost flat level and its area, the flat area below that level (what Ironing Type 'Topmost surface' would NOT iron,
    Fill.cpp v02.08.02.61 L973), and the largest flat levels by area (z rounded to 0.1 mm). Counted as printed top surfaces: recessed pocket
    floors and the covered tops of stacked normal parts are included, negative parts are not subtracted (a small error on typical
    parts); "visible" is not measurable here."""
    empty = {"flat_up_mm2": 0.0, "top_z": None, "top_flat_mm2": 0.0, "lower_flat_mm2": 0.0, "levels": [], "zmax": None}
    if len(faces) == 0:
        return empty
    a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    n = np.cross(b - a, c - a)
    twice = np.linalg.norm(n, axis=1)
    area = twice / 2.0
    nz = n[:, 2] / np.maximum(twice, 1e-12)
    zc = (a[:, 2] + b[:, 2] + c[:, 2]) / 3.0
    zmin = float(verts[:, 2].min())
    sel = (nz > math.cos(math.radians(FLAT_UP_DEG))) & (zc > zmin + 0.05)
    empty["zmax"] = round(float(verts[:, 2].max()), 3)
    if not sel.any():
        return empty
    top_z = float(zc[sel].max())
    at_top = sel & (np.abs(zc - top_z) < 0.05)
    lv: dict[float, float] = {}
    for zz, ar in zip(np.round(zc[sel], 1), area[sel]):
        lv[float(zz)] = lv.get(float(zz), 0.0) + float(ar)
    levels = sorted(((round(zz, 1), round(ar, 1)) for zz, ar in lv.items()), key=lambda t: -t[1])[:FLAT_LEVELS_N]
    return {"flat_up_mm2": round(float(area[sel].sum()), 1), "top_z": round(top_z, 2), "top_flat_mm2": round(float(area[at_top].sum()), 1),
            "lower_flat_mm2": round(float(area[sel & ~at_top].sum()), 1), "levels": [list(t) for t in levels], "zmax": round(float(verts[:, 2].max()), 3)}


def parse_slice_info(z: zipfile.ZipFile) -> dict[int, dict]:
    """Per-plate metadata of Metadata/slice_info.config (present in a sliced 3MF): {plate `index`: {key: value}}. The importer walks the zip
    entries in order (bbs_3mf.cpp v02.08.02.61 L1657) and parses model_settings.config (L1669-1673) and slice_info.config (L1678-1682) with
    the SAME handlers; `filament_maps` (L4666-4677) and `filament_map_mode` (L4657-4665) are not gated, so the LATER zip entry wins. Bambu
    writes model_settings first and slice_info later (L8547 / L8871), and its slice_info writer emits filament_maps and limit_filament_maps
    only, never filament_map_mode (L8690-8705); a hand-written mode there would override too. slice_info selects the plate by its `index`
    (L4745-4750), model_settings by `plater_id` (L4614-4616)."""
    try:
        xml = z.read("Metadata/slice_info.config")
    except KeyError:
        return {}
    out: dict[int, dict] = {}
    for n, pl in enumerate(ET.fromstring(xml).iter("plate"), 1):
        meta = {md.get("key"): md.get("value") for md in pl.findall("metadata") if md.get("key") is not None}
        try:
            idx = int(meta.get("index", n))
        except ValueError:
            idx = n
        out[idx] = meta
    return out


# C16 stale slice detector: a sliced 3MF carries three records of
# one slice - Metadata/slice_info.config (per plate: prediction, weight, filaments, objects, outside, support_used), Metadata/plate_N.gcode (its
# HEADER block and CONFIG block) and Metadata/plate_N.gcode.md5 - next to the editable project (project_settings.config, model_settings.config).
# Bambu Studio writes all of them in one save; a project edited after slicing, a G-code from another slice copied in, or a file assembled by
# a script can leave them disagreeing, and every other check of this audit reads the project, not the G-code that prints.
FRESH_KEYS = ("print_settings_id", "layer_height", "initial_layer_print_height", "filament_settings_id", "filament_type", "filament_colour",
              "enable_support", "support_type", "support_style", "support_top_z_distance", "support_interface_top_layers", "sparse_infill_density",
              "sparse_infill_pattern", "wall_loops", "top_shell_layers", "bottom_shell_layers", "ironing_type", "top_surface_pattern",
              "seam_position", "brim_type", "brim_width", "nozzle_diameter")
# Not compared: keys the slicer normalises at slice time (enable_prime_tower, independent_support_layer_height: normalize_fdm_2, PrintConfig.cpp
# v02.08.02.61 L7722-7768, measured: project enable_prime_tower 1 -> G-code 0 on single-filament plates) and per-run keys.


def parse_slice_info_full(z: zipfile.ZipFile) -> dict[int, dict]:
    """{plate index: {"meta": {...}, "objects": [{identify_id, name, skipped}], "filaments": [{id, type, color, used_g}]}} from slice_info.config."""
    try:
        xml = z.read("Metadata/slice_info.config")
    except KeyError:
        return {}
    out: dict[int, dict] = {}
    for n, pl in enumerate(ET.fromstring(xml).iter("plate"), 1):
        meta = {md.get("key"): md.get("value") for md in pl.findall("metadata") if md.get("key") is not None}
        try:
            idx = int(meta.get("index", n))
        except ValueError:
            idx = n
        out[idx] = {"meta": meta,
                    "objects": [{"identify_id": o.get("identify_id"), "name": o.get("name"), "skipped": o.get("skipped")} for o in pl.findall("object")],
                    "filaments": [{"id": f.get("id"), "type": f.get("type"), "color": f.get("color"), "used_g": f.get("used_g")} for f in pl.findall("filament")]}
    return out


def gcode_head(z: zipfile.ZipFile, plate_no: int) -> dict | None:
    """HEADER block items and CONFIG block keys of an embedded plate G-code (None when the plate has no G-code)."""
    try:
        g = z.open(f"Metadata/plate_{plate_no}.gcode")
    except KeyError:
        return None
    hdr, cfg = {}, {}
    with g:
        for raw in g:
            ln = raw.decode("utf-8", "replace").rstrip("\r\n")
            if ln.startswith("; EXECUTABLE_BLOCK_START"):
                break
            m = re.match(r"^; ([a-z0-9_]+) = (.*)$", ln)
            if m:
                cfg.setdefault(m.group(1), m.group(2).strip())
                continue
            m = re.match(r"^; model printing time: .*; total estimated time: (.+)$", ln)
            if m and "total_time_s" not in hdr:   # the first (Normal mode) line; a Stealth-mode line would follow (GCode.cpp v02.08.02.61 L2018)
                hdr["total_time_s"] = _hms(m.group(1))
            m = re.match(r"^; total filament weight \[g\] : ([0-9.,]+)", ln)
            if m:   # a per-filament list "%.2f,%.2f" (GCodeProcessor.cpp L655-665, L735); slice_info holds the sum
                vals = [float(v) for v in m.group(1).split(",") if v.strip()]
                hdr["weight_g"], hdr["weight_n"] = round(sum(vals), 4), len(vals)
    return {"header": hdr, "config": cfg}


def _hms(s: str) -> int | None:
    """'6h 22m 30s' / '23m 42s' / '1d 2h 3m 4s' -> seconds."""
    tot, ok = 0, False
    for v, u in re.findall(r"(\d+)\s*([dhms])", s):
        tot += int(v) * {"d": 86400, "h": 3600, "m": 60, "s": 1}[u]
        ok = True
    return tot if ok else None


def _vals(v) -> list[str]:
    """A project value (str or list) or a G-code config value -> list of normalised strings (quotes dropped, ; or , split, colours normalised)."""
    items = v if isinstance(v, list) else re.split(r"[;,]", str(v))
    out = []
    for it in items:
        s = str(it).strip().strip('"').strip()
        if re.match(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$", s):
            s = norm_colour(s)
        else:
            try:
                f = float(s.rstrip("%"))
                s = f"{f:g}" + ("%" if s.endswith("%") else "")
            except ValueError:
                pass
        out.append(s)
    return out


def check_slice_freshness(z: zipfile.ZipFile, ps: dict, objects: list[dict], plates: list[dict], add) -> None:
    """C16: slice_info.config, the embedded plate G-code (header + config) and its md5 vs each other and vs the project."""
    si = parse_slice_info_full(z)
    if not si:
        add("OK", "C16", "no slice_info.config (unsliced project): nothing to compare")
        return
    by_pid = {pl["plater_id"]: pl for pl in plates}
    has_enforcer = any(p.get("subtype") == "support_enforcer" for ob in objects for p in (ob.get("parts") or []))
    nonprint = set()   # object ids whose every build item is printable="0"
    try:
        _items: dict[str, list] = {}
        for it in ET.fromstring(z.read("3D/3dmodel.model")).iter():
            if _tag(it) == "item" and it.get("objectid"):
                _items.setdefault(it.get("objectid"), []).append(str(it.get("printable", "1")).lower() in ("0", "false"))
        nonprint = {o for o, flags in _items.items() if flags and all(flags)}
    except KeyError:
        pass
    n_bad = 0
    for idx, rec in sorted(si.items()):
        meta, where = rec["meta"], f"plate {idx}"
        probs, notes = [], []
        gh = gcode_head(z, idx)
        if gh is None:
            add("WARN", "C16", f"{where}: slice_info.config describes this plate but Metadata/plate_{idx}.gcode is missing - the 3MF is not a complete sliced file")
            n_bad += 1
            continue
        # md5 written beside the G-code by the same save
        try:
            want = z.read(f"Metadata/plate_{idx}.gcode.md5").decode("ascii", "replace").strip().upper()
            with z.open(f"Metadata/plate_{idx}.gcode") as g:
                h = hashlib.md5()
                for chunk in iter(lambda: g.read(1 << 20), b""):
                    h.update(chunk)
            if not want:
                notes.append(f"empty plate_{idx}.gcode.md5")
            elif h.hexdigest().upper() != want:
                probs.append(f"plate_{idx}.gcode md5 {h.hexdigest().upper()} != plate_{idx}.gcode.md5 {want} (the G-code is not the one this file was saved with)")
        except KeyError:
            notes.append(f"no plate_{idx}.gcode.md5")
        # slice_info vs the G-code header (prediction = (int) Normal-mode time, PartPlate.cpp v02.08.02.61 L7179; weight = the sum over
        # filaments "%.2f", empty when 0, L7198). A value present but not a finite number is a problem, not a silent pass
        def _num(key):
            v = meta.get(key)
            if v in (None, ""):
                return None
            try:
                f = float(v)
            except ValueError:
                probs.append(f"slice_info {key} {v!r} is not a number")
                return None
            if not math.isfinite(f):
                probs.append(f"slice_info {key} {v!r} is not a finite number")
                return None
            return f
        pred = _num("prediction")
        t = gh["header"].get("total_time_s")
        if pred is not None and t is not None and abs(int(pred) - t) > 1:
            probs.append(f"slice_info prediction {int(pred)} s != G-code total estimated time {t} s")
        wt = _num("weight")
        gw = gh["header"].get("weight_g")
        if wt is not None and gw is not None and abs(wt - gw) > 0.006 * gh["header"].get("weight_n", 1) + 0.005:   # n rounded "%.2f" terms
            probs.append(f"slice_info weight {wt:g} g != G-code total filament weight {gw:g} g (sum of {gh['header'].get('weight_n', 1)} filament(s))")
        # the project now vs the G-code config it was sliced with
        drift, n_cmp = [], 0
        for k in FRESH_KEYS:
            if k in ps and k in gh["config"]:
                n_cmp += 1
            if k in ps and k in gh["config"] and _vals(ps[k]) != _vals(gh["config"][k]):
                drift.append(f"{k}: project {ps[k] if not isinstance(ps[k], list) else ','.join(map(str, ps[k]))!s} vs G-code {gh['config'][k]}")
        if drift:
            probs.append("project settings changed after slicing: " + "; ".join(drift[:8]) + (f" (+{len(drift) - 8} more)" if len(drift) > 8 else ""))
        if n_cmp < 10:
            probs.append(f"only {n_cmp} of {len(FRESH_KEYS)} keys found in both the project and the G-code CONFIG block (a G-code without its config, or a foreign file)")
        # slice_info filaments vs the project's filament table
        ft = filament_table(ps)
        for f in rec["filaments"]:
            try:
                fi = int(f["id"])
            except (TypeError, ValueError):
                continue
            pf = ft.get(fi) or {}
            if pf.get("type") and f.get("type") and f["type"] != pf["type"]:
                probs.append(f"slice_info filament {fi} type {f['type']} != project {pf['type']}")
            if pf.get("colour") and f.get("color") and norm_colour(f["color"]) != pf["colour"]:
                probs.append(f"slice_info filament {fi} colour {norm_colour(f['color'])} != project {pf['colour']}")
        # objects sliced vs objects on the plate now (identify_id)
        pl = by_pid.get(idx)
        plate_obj_ids = {str(i.get("object_id")) for i in (pl or {}).get("instances", [])}
        if pl is not None:
            # slice_info skips non-printable instances (bbs_3mf.cpp v02.08.02.61 L8722-8735), model_settings lists them (L8454-8482): leave out
            # the instances of objects whose build items are all printable="0"
            now = {str(i.get("identify_id")) for i in pl["instances"] if i.get("identify_id") and str(i.get("object_id")) not in nonprint}
            then = {str(o["identify_id"]) for o in rec["objects"] if o.get("identify_id")}
            if now and then and now != then:
                probs.append(f"objects sliced {sorted(then)} != instances on the plate now {sorted(now)} (identify_id)")
        for o in rec["objects"]:
            if str(o.get("skipped")).lower() == "true":
                probs.append(f"object '{o.get('name')}' was SKIPPED in the slice")
        if str(meta.get("outside")).lower() == "true":
            probs.append("slice_info outside = true: an object lies outside the printable area (C5's range check reads the project, this is the slicer's own flag)")
        # support_used = global enable_support OR any object's enable_support (PrintApply.cpp v02.08.02.61 L1213-1217, L2111)
        obj_support = any(str((ob.get("meta") or {}).get("enable_support", "")).lower() in ("1", "true")
                          for ob in objects if str(ob.get("id")) in plate_obj_ids or pl is None)
        if (str(meta.get("support_used")).lower() == "true" and str(gh["config"].get("enable_support", ps.get("enable_support"))) in ("0", "false")
                and not obj_support and not has_enforcer):
            probs.append("slice_info support_used = true with enable_support 0 on the project and on every object of the plate")
        if probs:
            n_bad += 1
            add("WARN", "C16", f"{where}: the sliced record disagrees with itself or with the project - {' | '.join(probs)}. Re-slice and re-audit before trusting the other checks "
                               f"(they read the project; the printer runs the G-code)")
        else:
            add("OK", "C16", f"{where}: slice_info, G-code header / config and md5 agree with each other and with the project "
                             f"({n_cmp} of {len(FRESH_KEYS)} keys compared, time {meta.get('prediction')} s, {meta.get('weight')} g)" + (f"; {', '.join(notes)}" if notes else ""))


def parse_layer_config_ranges(z: zipfile.ZipFile) -> list[dict]:
    """Height range Modifiers: Metadata/layer_config_ranges.xml (bbs_3mf.cpp v02.08.02.61 L180, writer L7885-7905):
    <objects><object id="N"><range min_z=".." max_z=".."><option opt_key="layer_height">0.12</option>...</range></object></objects>.
    The object id here is the writer's counter over model.objects (L7882-7890), which the importer builds in build-item order
    (_handle_start_item L4171-4185 -> _create_object_instance L4361-4372: object_index = objects.size() at first sight), and the reader
    maps it back as the 1-based model object index (L2210-2213). `model_object_id` = the 3dmodel.model / model_settings object id of
    build item N (build_item_order), None when the file has no such build item. A second <object> block with the same id
    is skipped as the slicer skips it. Limits (never produced by Bambu's writer): overlapping ranges are evaluated as written although the
    slicer trims the later one (PrintApply.cpp LayerRanges::assign L361-383); a build item with p:path is keyed by objectid only."""
    try:
        xml = z.read("Metadata/layer_config_ranges.xml")
    except KeyError:
        return []
    order = build_item_order(z)
    out = []
    seen: set[str] = set()
    for obj in ET.fromstring(xml).iter("object"):
        if obj.get("id") in seen:
            continue   # the slicer keeps the first block per id and drops the rest ("Found duplicated layer config range", L3074-3077; review P20 fix 3)
        seen.add(obj.get("id"))
        try:
            k = int(obj.get("id"))
        except (TypeError, ValueError):
            k = None
        mapped = order[k - 1] if k is not None and 1 <= k <= len(order) else None
        for rg in obj.findall("range"):
            opts = {o.get("opt_key"): (o.text or "").strip() for o in rg.findall("option") if o.get("opt_key")}
            out.append({"object_id": obj.get("id"), "model_object_id": mapped, "min_z": rg.get("min_z"), "max_z": rg.get("max_z"), "opts": opts})
    return out


def build_item_order(z: zipfile.ZipFile) -> list[str]:
    """Object ids of the 3D/3dmodel.model build items in document order, first occurrence only (a second instance of the same object finds
    the object already created, bbs_3mf.cpp v02.08.02.61 L4361-4362). Position N (1-based) is the object that layer_config_ranges.xml,
    layer_heights_profile.txt and brim_ear_points name as object id N (L2205-2217). Empty when the file has no 3D/3dmodel.model."""
    try:
        root = ET.fromstring(z.read("3D/3dmodel.model"))
    except KeyError:
        return []
    seen: set[str] = set()
    order: list[str] = []
    for it in root.iter():
        if _tag(it) != "item":
            continue
        oid = it.get("objectid")
        if oid is not None and oid not in seen:
            seen.add(oid)
            order.append(oid)
    return order


# C11 source assignment (house rule: the source file's per-object filament is the design intent; nothing is swapped without the
# maker's approval) --------------------------------------------------------------------------------------------------------------
BAMBU_LINE = re.compile(r"^Bambu (.+?)(?: @.*)?$")


def filament_table(ps: dict) -> dict[int, dict]:
    """1-based filament index -> profile, type, colour (normalised hex), catalogue id, from project_settings.config."""
    prof = ps.get("filament_settings_id") or []
    typ = ps.get("filament_type") or []
    col = ps.get("filament_colour") or []
    ids = ps.get("filament_ids") or []
    n = max(len(prof), len(typ), len(col), len(ids))
    return {i + 1: {"profile": prof[i] if i < len(prof) else None, "type": typ[i] if i < len(typ) else None,
                    "colour": norm_colour(col[i]) if i < len(col) else None, "id": ids[i] if i < len(ids) else None} for i in range(n)}


def bambu_line(profile: str | None) -> str | None:
    """'Bambu PLA Matte @BBL H2C' -> 'pla matte' (the catalogue's fila_type key, for the colour-name lookup); None for a non-Bambu profile."""
    m = BAMBU_LINE.match(profile or "")
    return m.group(1).strip().lower() if m else None


def profile_line(profile: str | None) -> str:
    """Any preset name without its printer/nozzle suffix: 'Generic PLA @BBL X1C' -> 'generic pla', 'Bambu PLA Basic @base' -> 'bambu pla basic'.
    The same preset saved on another printer profile is the same line."""
    return re.sub(r"\s*@.*$", "", profile or "").strip().lower()


FEATURE_FILAMENT_KEYS = ("wall_filament", "sparse_infill_filament", "solid_infill_filament")   # > 0 overrides `extruder` (PrintObject.cpp v02.08.02.61 L3122-3147)


def catalogue_colour_name(line: str | None, hexcol: str | None) -> str | None:
    """English catalogue colour name for a Bambu line + hex, or None when the hex is not in the catalogue for that line."""
    if not line or not hexcol:
        return None
    _fid, names = colour_index().get(line, (None, {}))
    for name, hexes in names.items():
        if hexcol in hexes:
            return name
    return None


def _ext(v, default: int) -> int:
    """model_settings 'extruder' value -> 1-based filament index; missing or '0' means 'inherit' (object value, else filament 1)."""
    try:
        n = int(str(v).strip())
    except (TypeError, ValueError):
        return default
    return n if n >= 1 else default


def printing_parts(objects: list[dict]) -> list[dict]:
    """Every part that lays down material (normal_part, modifier_part) with its resolved filament index (part > object > 1), keyed by the
    part uuid when the file has one, else 'obj:<object name>/part:<part name>'. An object without parts is one entry of its own."""
    def feature_keys(meta: dict) -> dict:
        hits = {}
        for k in FEATURE_FILAMENT_KEYS:
            if k in meta and _ext(meta.get(k), 0) >= 1:
                hits[k] = meta[k]
        return hits

    out = []
    for ob in objects:
        o_meta = ob.get("meta") or {}
        o_ext = _ext(o_meta.get("extruder"), 1)
        parts = [p for p in (ob.get("parts") or []) if p.get("subtype") in C10_PART_SUBTYPES]
        if not parts:
            out.append({"key": f"obj:{ob.get('name')}", "object": ob.get("name"), "object_id": ob.get("id"), "part": None, "subtype": None, "ext": o_ext,
                        "feature_keys": feature_keys(o_meta)})
        for p in parts:
            p_meta = p.get("meta") or {}
            # the volume's key wins when present, even "0" (then the feature falls back to `extruder`); else the object's
            # (PrintObject.cpp v02.08.02.61 L3125-3130)
            merged = {k: (p_meta[k] if k in p_meta else o_meta[k]) for k in FEATURE_FILAMENT_KEYS if k in p_meta or k in o_meta}
            out.append({"key": p.get("uuid") or f"obj:{ob.get('name')}/part:{p.get('name')}", "object": ob.get("name"), "object_id": ob.get("id"),
                        "part": p.get("name"), "subtype": p.get("subtype"), "ext": _ext(p_meta.get("extruder"), o_ext), "feature_keys": feature_keys(merged)})
    return out


def material_family(ftype: str | None) -> str | None:
    """filament_type -> family: the part before the first '-' or space, upper case ('PLA-CF' -> 'PLA', 'PETG-HF' -> 'PETG', 'PA6-CF' -> 'PA6')."""
    if not ftype:
        return None
    return re.split(r"[-\s]", str(ftype).strip(), maxsplit=1)[0].upper() or None


def check_material_families(ps: dict, objects: list[dict], painted: set, ranges: list[dict], add) -> None:
    """C14: one filament-type family per object; see the module docstring. Objects are keyed by id (two objects may share a name),
    and a Height range Modifier's `extruder` / per-feature filament keys count as uses by that object's normal parts (PrintObject.cpp
    v02.08.02.61 L3118-3122, L3131-3134)."""
    ft = filament_table(ps)
    by_obj: dict[tuple, dict] = {}

    def use(o, ext, where):
        t = (ft.get(ext) or {}).get("type")
        fam = material_family(t)
        if fam:
            o["fam"].setdefault(fam, []).append(f"{where}: filament {ext} {t}")

    for p in printing_parts(objects):
        o = by_obj.setdefault((str(p.get("object_id")), p["object"]), {"fam": {}, "painted": False})
        use(o, p["ext"], f"part '{p['part']}' ({p['subtype']})" if p["part"] else "object")
        for k, v in p["feature_keys"].items():
            use(o, _ext(v, 0), f"{k} of {'part ' + repr(p['part']) if p['part'] else 'the object'}")
    for rg in ranges:
        hit = {k: v for k, v in rg["opts"].items() if k in ("extruder",) + FEATURE_FILAMENT_KEYS and _ext(v, 0) >= 1}
        if not hit:
            continue
        span = f"height range {rg['min_z']}-{rg['max_z']} mm"
        key = next((k for k in by_obj if k[0] == str(rg.get("model_object_id"))), None) if rg.get("model_object_id") is not None else None
        if key is None:
            add("WARN", "C14", f"{span} (layer_config_ranges object {rg['object_id']}) sets {hit}: no matching object - not resolved; check its filament in Bambu Studio")
            continue
        for k, v in hit.items():
            use(by_obj[key], _ext(v, 0), f"{k} of the {span}")
    for ob in objects:
        k = (str(ob.get("id")), ob.get("name"))
        if str(ob.get("id")) in painted and k in by_obj:
            by_obj[k]["painted"] = True
    n_mixed = 0
    for (_oid, name), o in by_obj.items():
        if len(o["fam"]) > 1:
            n_mixed += 1
            fams = sorted(o["fam"])
            pair = {"PLA", "PETG"} <= set(fams)
            detail = "; ".join(f"{f}: {', '.join(sorted(set(v)))}" for f, v in sorted(o["fam"].items()))
            add("WARN", "C14", f"object '{name}' prints in {len(fams)} material families ({' + '.join(fams)}): {detail}. "
                               + ("PLA and PETG bond weakly to each other (Bambu Lab wiki, PLA and PETG mutual support): " if pair else "")
                               + "one material per part unless multi-material is the point (house rule); a clear part is a separate piece held mechanically")
        if o["painted"]:
            add("WARN", "C14", f"object '{name}' carries colour painting (paint_color in its mesh): the painted filaments are not resolved by C14; "
                               f"check their filament types in Bambu Studio's colour painting panel")
    if not n_mixed:
        add("OK", "C14", f"one material family per object ({len(by_obj)} object(s) checked: parts, modifiers and per-feature filament keys)")


def check_process_preset(ps: dict, objects: list[dict], reason: str | None, add, ranges: list[dict] | None = None, vlh_profile: bool = False) -> None:
    """C15: process preset vs the printer's default; see the module docstring."""
    reason = (reason or "").strip() or None   # a blank reason is no reason
    pid = ps.get("print_settings_id")
    expected = ps.get("default_print_profile")
    devs = []
    if expected:
        if pid != expected:
            devs.append(f"process preset {pid!r} is not the printer's default {expected!r}")
    elif not re.match(r"^0\.20mm Standard @BBL [A-Z0-9]+$", str(pid or "")):
        devs.append(f"process preset {pid!r} is not a 0.20mm Standard @BBL system preset (no default_print_profile recorded in the file)")
    m = re.match(r"^(\d+(?:\.\d+)?)mm\b", str(pid or ""))
    try:
        lh = float(str(ps.get("layer_height")).strip())
    except (TypeError, ValueError):
        lh = None
    diff_proc = ((ps.get("different_settings_to_system") or [""])[0] or "").split(";")
    if m and lh is not None and abs(float(m.group(1)) - lh) > 1e-6:
        devs.append(f"layer_height {lh:g} mm in a preset named {m.group(1)} mm (the preset was edited"
                    + ("" if "layer_height" in diff_proc else "; different_settings_to_system does not list layer_height") + ")")
    obj_lh = [f"'{ob.get('name')}' {ob['meta']['layer_height']}" for ob in objects if "layer_height" in (ob.get("meta") or {})]
    if obj_lh:
        devs.append(f"object layer_height override(s): {', '.join(obj_lh)}")
    # Height range Modifier layer heights and variable layer height
    rg_lh = []
    for rg in ranges or []:
        v = rg["opts"].get("layer_height")
        try:
            if v is not None and (lh is None or abs(float(v) - lh) > 1e-6):
                rg_lh.append(f"{rg['min_z']}-{rg['max_z']} mm at {v}")
        except ValueError:
            rg_lh.append(f"{rg['min_z']}-{rg['max_z']} mm at {v!r}")
    if rg_lh:
        devs.append(f"Height range Modifier layer height(s): {', '.join(rg_lh)}")
    if vlh_profile:
        devs.append("variable layer height (Metadata/layer_heights_profile.txt, bbs_3mf.cpp v02.08.02.61 L179)")
    mods = [k for k in diff_proc if k]
    tail = f"; modified process keys: {', '.join(mods)}" if mods else "; no process key modified"
    if not devs:
        same = "= the printer's default" if expected else "matches 0.20mm Standard @BBL (no default_print_profile in the file)"
        add("OK", "C15", f"process preset {pid!r} {same}, layer_height {ps.get('layer_height')}{tail}")
    elif reason:
        add("OK", "C15", f"deviation justified (--process-reason {reason!r}): {'; '.join(devs)}{tail}")
    else:
        add("WARN", "C15", f"{'; '.join(devs)}{tail}. House rule: start from {expected or '0.20mm Standard @BBL <printer>'} and justify every deviation with a sourced reason "
                           f"(a finer preset can multiply the print time); record it with --process-reason \"TEXT\"")


def painted_objects(z) -> set:
    """model_settings / build object ids whose mesh carries colour painting (the paint_color triangle attribute; seam painting is paint_seam)."""
    out = set()
    try:
        root = ET.fromstring(z.read("3D/3dmodel.model"))
    except KeyError:
        return out
    for obj in root.iter():
        if _tag(obj) != "object":
            continue
        comps = next((c for c in obj if _tag(c) == "components"), None)
        paths = set()
        if comps is not None:
            for c in comps:
                paths.add((c.get("{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}path") or c.get("path") or "/3D/3dmodel.model").lstrip("/"))
        else:
            paths.add("3D/3dmodel.model")
        for p in paths:
            try:
                if b"paint_color=" in z.read(p):
                    out.add(obj.get("id"))
                    break
            except KeyError:
                pass
    return out


def parse_approvals(items: list[str]) -> list[dict]:
    """--approve-swap 'KEY=N:who/when' -> KEY (part uuid, part name or object name), N (print filament index), note (free text, required)."""
    out = []
    for it in items or []:
        m = re.match(r"^(.+?)=(\d+):(.+)$", it.strip())
        if not m:
            print(f"--approve-swap needs 'KEY=N:who/when' (KEY = part uuid, part name or object name; N = filament index in the print file), got {it!r}",
                  file=sys.stderr)
            raise SystemExit(64)   # EX_USAGE, distinct from the verdict codes 0/1/2
        out.append({"key": m.group(1).strip(), "ext": int(m.group(2)), "note": m.group(3).strip()})
    return out


def check_source_assignment(src_path: str, ps: dict, objects: list[dict], approvals: list[dict], add) -> dict:
    """C11: compare every printing part's filament (preset line, type, colour) in the print file with the same part in the source file.
    Match by part uuid first, then by object name + part name, then by part name alone (a name that fits more than one part, or a print
    part already taken by another source part, is reported as ambiguous and not compared). The uuid is written and read by bbs_3mf.cpp
    v02.08.02.61 (L8240-8241 / L4510, L5464), kept on "Split to parts" (Model.cpp L2766-2776) and regenerated on the set_mesh repair path
    (Model.cpp L3697); a uuid match means the same DESIGN SLOT, not the same mesh (a part whose mesh was replaced can keep its uuid). FAIL on a different line/type, or on a different catalogue colour name, unless an --approve-swap names
    the part (uuid, part name, or object name: an object-name key approves every swapped part of that object that landed on index N)
    and the print filament index; WARN when a colour hex differs but one side is not in the catalogue; WARN for a source part the print
    file lacks; WARN for an approval that matched nothing. Resolution of the filament index: part > object > 1 (PrintObject.cpp
    v02.08.02.61 L3069-3080, L3042-3049; Model.cpp L3295-3306); an index above the filament count prints with filament 1
    (bbs_3mf.cpp L2383-2384). summary["warn"] counts every C11 WARN incl. the missing parts; "missing" counts those alone."""
    summary = {"source": src_path, "source_filaments": None, "matched": 0, "fail": 0, "warn": 0, "approved": 0, "missing": 0, "ambiguous": 0}
    try:
        with zipfile.ZipFile(src_path) as zs:
            sps = read_json(zs, "Metadata/project_settings.config") or {}
            sobjs, _ = parse_model_settings(zs)
    except (OSError, zipfile.BadZipFile, KeyError, ValueError, ET.ParseError) as e:
        summary["fail"] += 1
        summary["error"] = f"{type(e).__name__}: {e}"
        add("FAIL", "C11", f"source file not readable: {src_path} ({type(e).__name__}: {e}); the design-intent comparison did not run")
        return summary
    s_tab, p_tab = filament_table(sps), filament_table(ps)
    summary["source_filaments"] = s_tab
    s_parts, p_parts = printing_parts(sobjs), printing_parts(objects)
    by_key = {p["key"]: p for p in p_parts if not p["key"].startswith("obj:")}   # real part uuids only; synthetic name keys go through the candidate path
    by_pair: dict = {}
    by_part: dict = {}
    for p in p_parts:
        by_pair.setdefault((p["object"], p["part"]), []).append(p)
        by_part.setdefault(p["part"], []).append(p)
    used_appr: set = set()

    def approved_for(sp, pp):
        """(approval, how) for the first --approve-swap that names this part (uuid, part name or object name) with the print index."""
        for i, ap_ in enumerate(approvals):
            if ap_["ext"] != pp["ext"]:
                continue
            if ap_["key"] == sp["key"]:
                used_appr.add(i)
                return ap_, "by uuid/key"
            if sp["part"] and ap_["key"] == sp["part"]:
                used_appr.add(i)
                return ap_, "by part name"
            if ap_["key"] == sp["object"]:
                used_appr.add(i)
                return ap_, "by object name: covers every swapped part of this object on that index"
        return None, None

    def fil_desc(tab: dict, ext: int, who: str) -> tuple[dict, str, str | None]:
        """Filament row for an index; an index above the table prints as filament 1 (bbs_3mf.cpp L2383-2384, PrintObject.cpp L3044)."""
        if ext in tab:
            f = tab[ext]
            return f, f"{who} filament {ext} {f.get('profile')!r} {f.get('type')} {f.get('colour')}", None
        f = tab.get(1, {})
        note = f"{who} filament index {ext} is out of range ({len(tab)} filament(s)); the slicer prints it with filament 1"
        return f, f"{who} filament {ext} -> 1 {f.get('profile')!r} {f.get('type')} {f.get('colour')}", note

    used = set()
    for sp in s_parts:
        label = f"'{sp['object']}'" + (f" / part '{sp['part']}' ({sp['subtype']})" if sp["part"] else "")
        sf, s_desc, s_note = fil_desc(s_tab, sp["ext"], "source")
        pp = by_key.get(sp["key"]) if not sp["key"].startswith("obj:") else None
        if pp is None:
            cands = by_pair.get((sp["object"], sp["part"]), [])
            if not cands and sp["part"]:
                cands = by_part.get(sp["part"], [])
            cands = [c for c in cands if id(c) not in used]
            if len(cands) > 1:
                summary["ambiguous"] += 1
                summary["warn"] += 1
                add("WARN", "C11", f"{label}: {s_desc} - {len(cands)} print parts share the name, none has this uuid: ambiguous, not compared; "
                                   f"give the parts distinct names or keep the source uuids")
                continue
            pp = cands[0] if cands else None
        elif id(pp) in used:
            pp = None
        if pp is None:
            summary["missing"] += 1
            summary["warn"] += 1
            add("WARN", "C11", f"{label}: {s_desc} - part not found in the print file (dropped, or renamed without the same uuid, or its name already "
                               f"taken by another source part); a removed design part needs the maker's approval")
            continue
        used.add(id(pp))
        summary["matched"] += 1
        pf, p_desc, p_note = fil_desc(p_tab, pp["ext"], "print")
        for note in (s_note, p_note):
            if note:
                summary["warn"] += 1
                add("WARN", "C11", f"{label}: {note} (bbs_3mf.cpp v02.08.02.61 L2383-2384, PrintObject.cpp L3044)")
        if pp.get("feature_keys") or sp.get("feature_keys"):
            summary["warn"] += 1
            add("WARN", "C11", f"{label}: per-feature filament key(s) {pp.get('feature_keys') or sp.get('feature_keys')} override `extruder` "
                               f"(PrintObject.cpp v02.08.02.61 L3122-3147); C11 compares `extruder` only - check those features by eye")
        same_line = profile_line(sf.get("profile")) == profile_line(pf.get("profile"))
        same_type = (sf.get("type") or "") == (pf.get("type") or "")
        s_line, p_line = bambu_line(sf.get("profile")), bambu_line(pf.get("profile"))
        s_name, p_name = catalogue_colour_name(s_line, sf.get("colour")), catalogue_colour_name(p_line, pf.get("colour"))
        ap_, how = approved_for(sp, pp)
        hint = f"--approve-swap \"{sp['key']}={pp['ext']}:who/when\" (the uuid key names exactly this part)"
        if not (same_line and same_type):
            if ap_:
                summary["approved"] += 1
                add("OK", "C11", f"{label}: approved swap ({ap_['note']}; {how}): {s_desc} -> {p_desc}")
            else:
                summary["fail"] += 1
                add("FAIL", "C11", f"{label}: {s_desc} -> {p_desc}: material or line changed from the design intent; swap only with the maker's approval: {hint}")
            continue
        if (sf.get("colour") or "") == (pf.get("colour") or ""):
            add("OK", "C11", f"{label}: {p_desc} = source (same line, type and colour hex)")
        elif s_name and p_name and s_name != p_name:
            if ap_:
                summary["approved"] += 1
                add("OK", "C11", f"{label}: approved colour swap ({ap_['note']}; {how}): {s_desc} (catalogue {s_name}) -> {p_desc} (catalogue {p_name})")
            else:
                summary["fail"] += 1
                add("FAIL", "C11", f"{label}: {s_desc} (catalogue {s_name}) -> {p_desc} (catalogue {p_name}): colour changed from the design intent; "
                                   f"if the source hex is an AMS-tag hex of the same spool or you chose the colour, record it with {hint}")
        elif s_name and p_name:
            add("OK", "C11", f"{label}: {p_desc} = source colour {s_name} (hex differs, same catalogue name)")
        else:
            summary["warn"] += 1
            add("WARN", "C11", f"{label}: colour hex differs, {s_desc} (catalogue {s_name or 'unknown'}) vs {p_desc} (catalogue {p_name or 'unknown'}); "
                               f"same line and type; confirm the product colour name on the spool")
    extra = [p for p in p_parts if id(p) not in used]
    for pp in extra:
        pf = p_tab.get(pp["ext"], {})
        add("OK", "C11", f"'{pp['object']}'" + (f" / part '{pp['part']}' ({pp['subtype']})" if pp["part"] else "") +
            f": not in the source file (new part), print filament {pp['ext']} {pf.get('profile')!r} {pf.get('colour')}")
    for i, ap_ in enumerate(approvals):
        if i not in used_appr:
            summary["warn"] += 1
            add("WARN", "C11", f"approval \"{ap_['key']}={ap_['ext']}:{ap_['note']}\" matched no swapped part (typo in the key, or wrong filament index?) - not applied")
    if summary["matched"] == 0:
        summary["warn"] += 1
        add("WARN", "C11", f"no part of the source file {src_path} was found in the print file (no shared part uuid or name) - wrong --source?")
    return summary


COUPON_ROOT = str(mm_config.repo_root() / "work" / "coupons")   # where scored coupon measurement sheets live; --coupon-root overrides


def check_top_z_citation(text: str, top: float | None, per_obj: dict, layer_h: float, profiles: list) -> dict:
    r"""--top-z-coupon-row "<sheet.md> variant A03": the sheet must lie under COUPON_ROOT (--coupon-root), the row must exist, be SCORED (a non-empty pass/fail
    cell), and match THIS file's Top Z (project or every per-object value), layer height (plate letter A = 0.20, B = 0.16 per the sheet's Process
    base line) and material (the sheet's "Result table - <material>" heading vs the filament preset line)."""
    toks = text.split()
    md = next((t for t in toks if t.lower().endswith(".md")), None)
    if not md or not os.path.isfile(md):
        return {"ok": False, "detail": "no existing .md sheet in the citation"}
    if not os.path.normcase(os.path.realpath(md)).startswith(os.path.normcase(os.path.realpath(COUPON_ROOT)) + os.sep):
        return {"ok": False, "detail": f"the sheet must lie under {COUPON_ROOT}"}
    m = re.search(r"\b(?:variant|row|step)\s*([A-Za-z]?\d+)", text, re.I)
    if not m:
        return {"ok": False, "detail": "no variant / row token in the citation"}
    key = m.group(1).upper()
    try:
        lines = open(md, encoding="utf-8").read().split("\n")
    except OSError as e:
        return {"ok": False, "detail": f"sheet unreadable: {e}"}
    heading, row = None, None
    for ln in lines:
        if ln.startswith("## Result table"):
            heading = ln
        if ln.startswith("| ") and re.match(r"\|\s*" + re.escape(key) + r"\b", ln):
            row = ln
            break
    if row is None:
        return {"ok": False, "detail": f"variant {key} not found in {md}"}
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    # sheet layout: step | Top Z set | effective gap | interface layers | spacing | ease ceiling | ease shelf | sag | scars c | scars s | pass/fail | photos | note | who
    try:
        row_top = float(cells[1])
    except (IndexError, ValueError):
        return {"ok": False, "detail": f"row {key}: Top Z cell unreadable"}
    scored = len(cells) > 10 and bool(cells[10])
    if not scored:
        return {"ok": False, "detail": f"row {key} of {os.path.basename(md)} is not scored (pass/fail cell empty): the coupon has not been printed and judged"}
    tops = {float(v) for v in per_obj.values()} if per_obj else ({top} if top is not None else set())
    if any(abs(t - row_top) > 1e-6 for t in tops):
        return {"ok": False, "detail": f"row {key} is Top Z {row_top}; this file uses {sorted(tops)} - a citation covers one value"}
    plate_letter = key[0] if key[0].isalpha() else None
    plate_h = {"A": 0.2, "B": 0.16}.get(plate_letter)
    if plate_h is not None and abs(plate_h - layer_h) > 1e-6:
        return {"ok": False, "detail": f"row {key} is plate {plate_letter} ({plate_h} mm layers); this file prints {layer_h} mm layers"}
    mat = (heading or "").split("-", 1)[-1].strip().lower() if heading else ""
    prof = " ".join(profiles).lower()
    if mat and not any(w in prof for w in mat.replace(",", " ").split() if len(w) > 3 and w not in ("slot", "basic")):
        pass
    if mat and ("matte" in mat) != ("matte" in prof):
        return {"ok": False, "detail": f"row {key} sits under '{heading.strip()}'; this file's filament is {profiles}"}
    return {"ok": True, "detail": f"{os.path.basename(md)} {key}: Top Z {row_top}, plate {plate_letter} ({plate_h} mm), material '{mat}', scored '{cells[10]}'"}


def main(argv: list[str]) -> int:
    global COUPON_ROOT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--source", help="C11: the original (design-intent) 3MF; per-part filament line/type/colour must match it")
    ap.add_argument("--approve-swap", action="append", default=[], metavar="KEY=N:who/when",
                    help="C11: approve one swap: KEY = part uuid, part name or object name; N = filament index in the print file; who/when = who approved it and when")
    ap.add_argument("--process-reason", default=None, metavar="TEXT",
                    help="C15: the sourced reason for a process preset other than the printer's default (turns the C15 WARN into an OK that records it)")
    ap.add_argument("--no-geometry", action="store_true", help="C12: skip the mesh read (flat-top area per object)")
    ap.add_argument("--flat-top-min", type=float, default=FLAT_TOP_MIN_MM2, help="C12: flat up-facing area (mm2) from which an object counts as a large flat top")
    ap.add_argument("--top-coupon-row", default=None, metavar="TEXT",
                    help="C12: the top-surface coupon row (sheet path + row) the settings sheet cites for Ironing Type / Top surface pattern; turns the WARN into OK")
    ap.add_argument("--top-z-coupon-row", default=None, metavar="TEXT",
                    help="C13: the scored support-removal coupon row (sheet path + variant) that verifies the Top Z value; turns the WARN into OK")
    ap.add_argument("--area-left", nargs=2, type=float, default=H2C_LEFT, metavar=("XMIN", "XMAX"))
    ap.add_argument("--area-right", nargs=2, type=float, default=H2C_RIGHT, metavar=("XMIN", "XMAX"))
    ap.add_argument("--load-note", default=LOAD_NOTE, help="physical load note for C7 (default: current-load.md)")
    ap.add_argument("--today", type=iso_date, default=None, help="YYYY-MM-DD used for the C7 note-age check (default: the PC date)")
    ap.add_argument("--load-max-age-days", type=int, default=7)
    ap.add_argument("--coupon-root", default=None, metavar="DIR",
                    help=f"C13: folder that holds scored coupon measurement sheets (default {COUPON_ROOT})")
    a = ap.parse_args(argv[1:])
    if a.coupon_root:
        COUPON_ROOT = a.coupon_root

    z = zipfile.ZipFile(a.path)
    ps = read_json(z, "Metadata/project_settings.config") or {}
    objects, plates = parse_model_settings(z)
    ranges = parse_layer_config_ranges(z)
    slice_info = parse_slice_info(z)
    names = z.namelist()
    ms_pos = names.index("Metadata/model_settings.config") if "Metadata/model_settings.config" in names else None
    si_pos = names.index("Metadata/slice_info.config") if "Metadata/slice_info.config" in names else None
    slice_info_wins = si_pos is not None and (ms_pos is None or si_pos > ms_pos)   # the later zip entry is parsed last and wins (A2)
    matched_si = set()
    for pl in plates:   # joined on plater_id (the importer's key), not on position
        si = slice_info.get(pl["plater_id"], {})
        if si:
            matched_si.add(pl["plater_id"])
        pl["slice_info_maps"] = si.get("filament_maps")
        pl["slice_info_mode"] = si.get("filament_map_mode")
        if si.get("filament_maps") is not None and slice_info_wins:
            pl["effective_maps"] = si["filament_maps"]
        else:
            pl["effective_maps"] = pl["meta"].get("filament_maps")
    unmatched_si = sorted(set(slice_info) - matched_si)
    plate_jsons = {}
    for n in z.namelist():
        m = re.match(r"Metadata/plate_(\d+)\.json$", n)
        if m:
            plate_jsons[int(m.group(1))] = read_json(z, n)

    findings = []
    def add(level, code, msg, **ev):
        findings.append({"level": level, "check": code, "msg": msg, **ev})

    fil_ids = ps.get("filament_ids") or []
    fil_types = ps.get("filament_type") or []
    fil_cols = ps.get("filament_colour") or []
    g_mode = ps.get("filament_map_mode")
    g_map = ps.get("filament_map")
    report = {
        "file": a.path,
        "printer": ps.get("printer_settings_id"),
        "process": ps.get("print_settings_id"),
        "bed_type": ps.get("curr_bed_type"),
        "filaments": [
            {"index": i + 1, "id": fil_ids[i] if i < len(fil_ids) else None,
             "type": fil_types[i] if i < len(fil_types) else None,
             "colour": fil_cols[i] if i < len(fil_cols) else None,
             "profile": (ps.get("filament_settings_id") or [None] * 9)[i] if i < len(ps.get("filament_settings_id") or []) else None}
            for i in range(max(len(fil_ids), len(fil_types)))
        ],
        "global": {
            "filament_map_mode": g_mode, "filament_map_mode_label": MODE_LABEL.get(g_mode, g_mode),
            "filament_map": g_map,
            "max_bridge_length": ps.get("max_bridge_length"),
            "support_threshold_angle": ps.get("support_threshold_angle"),
            "enable_support": ps.get("enable_support"),
            "support_type": ps.get("support_type"),
            "enable_prime_tower": ps.get("enable_prime_tower"),
            "prime_tower_rib_wall": ps.get("prime_tower_rib_wall"),
            "prime_tower_width": ps.get("prime_tower_width"),
            "wipe_tower_x": ps.get("wipe_tower_x"), "wipe_tower_y": ps.get("wipe_tower_y"),
            "nozzle_diameter": ps.get("nozzle_diameter"),
        },
        "plates": [],
    }

    # C3 / C4
    mbl = ps.get("max_bridge_length")
    try:
        if mbl is not None and float(mbl) == 0:
            add("WARN", "C3", "max_bridge_length = 0: every bridge will be supported (Bambu profile default)", value=mbl)
        else:
            add("OK", "C3", f"max_bridge_length = {mbl}", value=mbl)
    except ValueError:
        add("WARN", "C3", f"max_bridge_length unreadable: {mbl!r}")
    add("OK", "C4", f"enable_support = {ps.get('enable_support')}, support_threshold_angle = {ps.get('support_threshold_angle')}, support_type = {ps.get('support_type')}")

    # C10: 100 % sparse infill with a pattern the slicer's own config check refuses (PrintConfig.cpp v02.08.02.61 L9528-9531
    # "<pattern> doesn't work at 100% density"). The GUI blocks the pair in its panels only (ConfigManipulation.cpp L671-702, called for the
    # process page and for the object / part / Height range Modifier panels by GUI_ObjectSettings.cpp L338-408), never at slice time, so a
    # pair created by inheritance after a panel was last shown reaches the slicer; the CLI validates the project level only and slices
    # 83-88 % covered (measured from the G-code of a calibration coupon). Checked at project level, per object and
    # per part (Metadata/model_settings.config; a level without its own key inherits the level above: part > object > project; only
    # normal_part and modifier_part carry infill of their own, so negative_part / support_enforcer / support_blocker are skipped).
    # Height range Modifiers (Metadata/layer_config_ranges.xml) that touch either key are resolved per range: the range
    # file's object id is the 1-based build-item index (parse_layer_config_ranges / build_item_order); inside the range a NORMAL part prints
    # range > part > object > project (PrintObject.cpp v02.08.02.61 L3105-3122: object config, then the volume's, then the layer range's,
    # last writer wins) and a MODIFIER part prints its own key > range > object > project (PrintApply.cpp L797-799: a modifier's region
    # starts from its parent region, which already carries the range; the parent normal part's own key is not resolved here, as at part
    # level). A range whose id has no build item is WARN "not resolved".
    # Allowed at 100 % (code and wiki agree): concentric, zig-zag (= Rectilinear), alignedrectilinear,
    # hilbertcurve, archimedeanchords, octagramspiral.
    def _density(v) -> float | None:
        try:
            return float(str(v).strip().rstrip("%"))
        except (TypeError, ValueError):
            return None
    g_dens = ps.get("sparse_infill_density")
    g_pat = ps.get("sparse_infill_pattern")
    pairs = [("project", g_dens, g_pat)]
    for ob in objects:
        m = ob.get("meta") or {}
        o_dens, o_pat = m.get("sparse_infill_density", g_dens), m.get("sparse_infill_pattern", g_pat)
        if "sparse_infill_density" in m or "sparse_infill_pattern" in m:
            pairs.append((f"object {ob.get('id')} '{ob.get('name')}'", o_dens, o_pat))
        for pt in ob.get("parts") or []:
            if pt.get("subtype") not in C10_PART_SUBTYPES:
                continue
            pm = pt.get("meta") or {}
            if "sparse_infill_density" in pm or "sparse_infill_pattern" in pm:
                pairs.append((f"part {pt.get('id')} '{pt.get('name')}' ({pt.get('subtype')}) of object {ob.get('id')}",
                              pm.get("sparse_infill_density", o_dens), pm.get("sparse_infill_pattern", o_pat)))
    n_range_pairs = 0
    for rg in ranges:
        hit = {k: v for k, v in rg["opts"].items() if k in ("sparse_infill_density", "sparse_infill_pattern")}
        if not hit:
            continue
        span = f"height range {rg['min_z']}-{rg['max_z']} mm"
        ob = next((o for o in objects if str(o.get("id")) == str(rg.get("model_object_id"))), None) if rg.get("model_object_id") is not None else None
        if ob is None:
            add("WARN", "C10", f"{span} (layer_config_ranges object {rg['object_id']}) overrides {hit}: build item #{rg['object_id']} of 3D/3dmodel.model "
                               f"{'is not a model_settings object' if rg.get('model_object_id') is not None else 'does not exist'} - not resolved; "
                               f"confirm the pair in Bambu Studio's Height range Modifier panel")
            continue
        m = ob.get("meta") or {}
        o_dens, o_pat = m.get("sparse_infill_density", g_dens), m.get("sparse_infill_pattern", g_pat)
        r_dens, r_pat = hit.get("sparse_infill_density", o_dens), hit.get("sparse_infill_pattern", o_pat)
        obj_txt = f"object {ob.get('id')} '{ob.get('name')}'"
        printing = [p for p in (ob.get("parts") or []) if p.get("subtype") in C10_PART_SUBTYPES]
        if not printing:
            pairs.append((f"{span} of {obj_txt}", r_dens, r_pat))
            n_range_pairs += 1
            continue
        grouped: dict[tuple, list[str]] = {}
        for pt in printing:
            pm = pt.get("meta") or {}
            if pt.get("subtype") == "normal_part":
                dens, pat = hit.get("sparse_infill_density", pm.get("sparse_infill_density", o_dens)), hit.get("sparse_infill_pattern", pm.get("sparse_infill_pattern", o_pat))
            else:
                if all(k in pm for k in hit):
                    continue   # the modifier owns every key the range sets: its pair is unchanged inside the range and already in `pairs`
                dens, pat = pm.get("sparse_infill_density", r_dens), pm.get("sparse_infill_pattern", r_pat)
            grouped.setdefault((str(dens), str(pat)), []).append(f"{'normal' if pt.get('subtype') == 'normal_part' else 'modifier'} part {pt.get('id')} '{pt.get('name')}'")
        for (dens, pat), names in grouped.items():
            pairs.append((f"{span} of {obj_txt}, {'; '.join(names)}", dens, pat))
            n_range_pairs += 1
    c10_bad = 0
    for where, dens, pat in pairs:
        d = _density(dens)
        if d is None:
            if dens is not None:
                add("WARN", "C10", f"{where}: sparse_infill_density unreadable: {dens!r}")
            continue
        if d >= 100 - 1e-9 and str(pat) not in SOLID_OK_PATTERNS:
            c10_bad += 1
            # the CLI validates only the global config (BambuStudio.cpp v02.08.02.61 L4125 -> PrintConfig.cpp L9528-9531, exit
            # CLI_INVALID_VALUES_IN_3MF); object, part and range pairs are never validated and slice with holes
            tail = ("the CLI refuses the whole file (CLI_INVALID_VALUES_IN_3MF)" if where == "project"
                    else "the CLI slices it with holes (only the project level is validated)")
            add("FAIL", "C10", f"{where}: sparse_infill_density {dens} with sparse_infill_pattern {pat!r} - Bambu Studio refuses this pair "
                               f"(\"doesn't work at 100% density\", PrintConfig.cpp L9528-9531); {tail}. Use one of {sorted(SOLID_OK_PATTERNS)}")
    if not c10_bad:
        n100 = sum(1 for _, dens, _ in pairs if (_density(dens) or 0) >= 100 - 1e-9)
        add("OK", "C10", f"sparse infill 100 % pairs checked: {n100} at 100 % (project + object + part + height-range overrides), all with an allowed pattern" if n100
            else f"no 100 % sparse infill (project {g_dens!r} {g_pat!r}; {len(pairs) - 1 - n_range_pairs} object/part override(s), {n_range_pairs} height-range pair(s))")

    # per plate
    for i, pl in enumerate(plates, 1):
        meta = pl["meta"]
        mode = meta.get("filament_map_mode", g_mode)
        maps = meta.get("filament_maps")
        pj = plate_jsons.get(i) or {}
        pj_fils = pj.get("filament_ids")
        n_fil = len(pj_fils) if isinstance(pj_fils, list) else None
        bbox = pj.get("bbox_objects") or []
        entry = {"plate": i, "filament_map_mode": mode, "label": MODE_LABEL.get(mode, mode), "filament_maps": maps,
                 "filament_ids_on_plate": pj_fils, "objects": [], "wipe_tower_x": None, "wipe_tower_y": None}
        wx, wy = ps.get("wipe_tower_x") or [], ps.get("wipe_tower_y") or []
        if i - 1 < len(wx):
            entry["wipe_tower_x"], entry["wipe_tower_y"] = wx[i - 1], (wy[i - 1] if i - 1 < len(wy) else None)
        # C1
        if n_fil is not None and n_fil >= 2 and mode in ("Auto For Flush", "Auto For Match", None):
            add("WARN", "C1", f"plate {i}: {n_fil} filaments with filament_map_mode {mode!r} ({MODE_LABEL.get(mode, mode)}) - slicer may assign a filament to the LEFT extruder; use Custom and bind AMS filaments to the RIGHT", plate=i)
        elif n_fil is not None and n_fil >= 2:
            add("OK", "C1", f"plate {i}: {n_fil} filaments, mode {mode!r} ({MODE_LABEL.get(mode, mode)})", plate=i)
        else:
            add("OK", "C1", f"plate {i}: {n_fil if n_fil is not None else '?'} filament(s), mode {mode!r}", plate=i)
        # C2 (a sliced 3MF also stores the plate map in Metadata/slice_info.config, parsed after model_settings.config by the same
        # handler, so IT is the map the CLI slices: bbs_3mf.cpp v02.08.02.61 L1678-1682, L4666-4675)
        si_maps = pl.get("slice_info_maps")
        si_mode = pl.get("slice_info_mode")
        entry["slice_info_filament_maps"] = si_maps
        entry["plater_id"] = pl.get("plater_id")
        order = f"zip entry {ms_pos} model_settings.config vs {si_pos} slice_info.config, parsed in that order (bbs_3mf.cpp v02.08.02.61 L1657)"
        if si_maps is not None and maps is not None and si_maps.split() != maps.split():
            winner, loser_name = (si_maps, "model_settings.config") if slice_info_wins else (maps, "slice_info.config")
            add("FAIL", "C2", f"plate {i} (plater_id {pl.get('plater_id')}): model_settings.config filament_maps = {maps!r} but slice_info.config filament_maps = {si_maps!r}; "
                              f"{order}: the later entry wins, so the CLI slices {winner!r} and ignores {loser_name} (L1669-1682, L4666-4677; a Bambu-written file has slice_info "
                              f"later). Re-save the file from Bambu Studio (or make BOTH files agree) and accept the grouping only "
                              f"from the sliced G-code '; filament_map =' line", plate=i)
            maps = winner
        elif si_maps is not None:
            add("OK", "C2", f"plate {i}: filament_maps = {maps!r} in model_settings.config and slice_info.config ({order}) (1-based extruder index per filament; 1 = LEFT, 2 = RIGHT on the H2C)", plate=i)
        else:
            add("OK", "C2", f"plate {i}: filament_maps = {maps!r} (model_settings.config; no slice_info.config entry for plater_id {pl.get('plater_id')} = not yet sliced, or the slice_info index does not match) (1-based extruder index per filament, from PrintConfig.cpp 'Filament map to extruder'; 1 = LEFT, 2 = RIGHT on the H2C)", plate=i)
        if si_mode is not None and si_mode != "Auto" and si_mode != mode:   # A4: a hand-written mode in slice_info overrides too (reader L4657-4665 is not gated; Bambu never writes it)
            add("FAIL", "C2", f"plate {i}: slice_info.config carries filament_map_mode {si_mode!r} (Bambu's writer never emits it, L8690-8705) while model_settings.config says {mode!r}; "
                              f"the later zip entry wins on import (L4657-4665): a hand-edited file - make the two agree", plate=i)
        entry["filament_maps_effective"] = maps
        # C5
        two_extruders = False
        if maps:
            try:
                two_extruders = len(set(maps.split())) > 1
            except Exception:  # noqa: BLE001
                two_extruders = False
        xmin_ok, xmax_ok = H2C_SHARED if two_extruders else (a.area_right if (maps and set(maps.split()) == {"2"}) else (a.area_left if (maps and set(maps.split()) == {"1"}) else H2C_SHARED))
        for ob in bbox:
            bb = ob.get("bbox") or []
            if len(bb) >= 4:
                x0, x1 = bb[0], bb[2]
                ok = x0 >= xmin_ok - 1e-6 and x1 <= xmax_ok + 1e-6
                entry["objects"].append({"name": ob.get("name"), "x": [round(x0, 1), round(x1, 1)], "within": ok})
                if not ok:
                    add("FAIL", "C5", f"plate {i}: '{ob.get('name')}' X {x0:.1f}..{x1:.1f} outside allowed {xmin_ok:.0f}..{xmax_ok:.0f} mm", plate=i)
        if bbox and all(o["within"] for o in entry["objects"]):
            add("OK", "C5", f"plate {i}: {len(bbox)} object(s) within X {xmin_ok:.0f}..{xmax_ok:.0f}", plate=i)
        report["plates"].append(entry)
    for idx in unmatched_si:
        add("WARN", "C2", f"slice_info.config plate index {idx} matches no model_settings.config plater_id ({[p['plater_id'] for p in plates]}); the importer ignores it silently "
                          f"(bbs_3mf.cpp v02.08.02.61 L4666 `if (m_curr_plater)`): a deleted or renumbered plate - re-save the file")

    # C8 filament profile vs printer / nozzle
    printer_id = ps.get("printer_settings_id") or ""
    model = ps.get("printer_model") or ""
    nozzles = ps.get("nozzle_diameter") or []
    fil_profiles = ps.get("filament_settings_id") or []
    gmap = [int(x) for x in (g_map or []) if str(x).isdigit()]
    for i, prof in enumerate(fil_profiles):
        cp, path = resolve_compatible_printers(prof)
        if cp is None:
            add("WARN", "C8", f"filament {i + 1} profile {prof!r} not found in the installed profiles (checked system BBL, user presets, install folder) - compatibility unproven")
            continue
        ext = gmap[i] if i < len(gmap) else None
        noz = nozzles[ext - 1] if ext and ext - 1 < len(nozzles) else (nozzles[0] if nozzles else None)
        expected = f"{model} {noz} nozzle" if model and noz else printer_id
        ok_printer = printer_id in cp
        ok_nozzle = expected in cp
        if ok_printer and ok_nozzle:
            add("OK", "C8", f"filament {i + 1} {prof!r}: compatible with {printer_id!r} (extruder {ext or '?'}, nozzle {noz}); profile {path}")
        elif ok_printer and not ok_nozzle:
            add("FAIL", "C8", f"filament {i + 1} {prof!r}: profile lists {printer_id!r} but not the nozzle of its extruder ({expected!r}); compatible_printers={cp}")
        else:
            add("FAIL", "C8", f"filament {i + 1} {prof!r}: {printer_id!r} not in compatible_printers={cp} (profile {path}) - the GUI would refuse this filament/nozzle pairing")

    # C9 bed type vs filament (Print.cpp v02.08.02.61 L1674-1689: temp 0 -> "Plate %d: %s does not support filament %s")
    bed = ps.get("curr_bed_type") or ""
    key = bed_temp_key(bed)
    fam = bed_family(bed)
    vit = ps.get("temperature_vitrification") or []
    if key is None:
        add("WARN", "C9", f"bed type {bed!r} not recognised - no bed-temperature check")
    else:
        temps = ps.get(key) or []
        temps0 = ps.get(key + "_initial_layer") or []
        for i, t in enumerate(temps):
            ftype = fil_types[i] if i < len(fil_types) else "?"
            try:
                tv = int(float(t))
            except Exception:  # noqa: BLE001
                add("WARN", "C9", f"filament {i + 1}: {key} unreadable: {t!r}")
                continue
            t0 = temps0[i] if i < len(temps0) else None
            if tv == 0:
                add("FAIL", "C9", f"filament {i + 1} ({ftype}): {key} = 0 -> Bambu Studio validate() error 'Plate N: {bed} does not support filament {i + 1}' (Print.cpp v02.08.02.61 L1674-1689)")
                continue
            rng = PLATE_RANGE.get(fam, {}).get(ftype.split("-")[0].upper(), "n/a")
            if rng is None:
                add("WARN", "C9", f"filament {i + 1} ({ftype}) on {bed}: plate table says 'not recommended' (Bambu Lab wiki plate table) although the profile sets {tv} C")
            elif rng == "n/a":
                add("OK", "C9", f"filament {i + 1} ({ftype}) on {bed}: bed {tv} C (first layer {t0}); no plate-table range for this material")
            elif rng[0] <= tv <= rng[1]:
                add("OK", "C9", f"filament {i + 1} ({ftype}) on {bed}: bed {tv} C (first layer {t0}) within plate table {rng[0]}-{rng[1]} C")
            else:
                add("WARN", "C9", f"filament {i + 1} ({ftype}) on {bed}: bed {tv} C outside plate table {rng[0]}-{rng[1]} C (Bambu Lab wiki plate table)")
            try:
                v = int(float(vit[i])) if i < len(vit) else None
            except Exception:  # noqa: BLE001
                v = None
            if v is not None and tv >= v and H2_SERIES.search(ps.get("printer_settings_id") or "") and ftype.split("-")[0].upper() in COOLING_TYPES:
                cmds = start_cooling_cmds(z)
                base = (f"filament {i + 1} ({ftype}): bed {tv} C >= temperature_vitrification {v} C on {ps.get('printer_settings_id')} -> "
                        "H2 cooling mode: M145 P0 + chamber exhaust (M106 P3) + automatic top vent open automatically "
                        "(H2C manual V1.0 p.13); door/glass not required")
                if not cmds:  # no proof, no OK
                    add("WARN", "C9", f"filament {i + 1} ({ftype}): bed {tv} C >= temperature_vitrification {v} C on {ps.get('printer_settings_id')}: "
                        "cooling-mode commands not verified: slice and re-audit (no plate G-code in this 3MF)")
                else:
                    missing = {k: [n for n, ok in zip(("M145 P0", "M106 P3"), v2) if not ok] for k, v2 in sorted(cmds.items()) if not all(v2)}
                    if missing:
                        add("WARN", "C9", f"filament {i + 1} ({ftype}): cooling-mode commands not found in plate G-code start section: {missing} - door/glass rule applies until resolved")
                    else:
                        add("OK", "C9", base + f"; M145 P0 and M106 P3 found in the start G-code of plate(s) {sorted(cmds)}")
            elif v is not None and tv >= v:
                add("WARN", "C9", f"filament {i + 1} ({ftype}): bed {tv} C >= temperature_vitrification {v} C -> house rule from the key's tooltip (PrintConfig.cpp v02.08.02.61 L3005: 'when the bed temperature is equal to or greater than it, it\'s highly recommended to open the front door and/or remove the upper glass to avoid cloggings'); Bambu Studio 02.08.02.61 itself does not emit this warning (GCodeProcessor.cpp L6351-6420)")

    # C6 / C7
    add("OK", "C6", f"prime tower: enable={ps.get('enable_prime_tower')} rib_wall={ps.get('prime_tower_rib_wall')} width={ps.get('prime_tower_width')} (clearance not computed here)")
    today = a.today or _dt.date.today()
    check_load(ps, plates, a.load_note, today, a.load_max_age_days, add, z)

    # C12 flat tops vs ironing / top pattern (pre-print checklist: visible tops). Per object: effective ironing_type / top_surface_pattern (part > object >
    # project; GUI_Factories.cpp v02.08.02.61 L102 / L107 allow both per object) and the up-facing flat area of its normal parts from the 3MF
    # meshes (negative parts are NOT subtracted; modifier/enforcer parts add no surface). A large flat top (>= --flat-top-min mm2) with no coupon
    # row cited is WARN: a visible top's settings are stated with a reason. Ironing Type topmost with flat area below the top level: WARN
    # (Fill.cpp L973 irons only the object's last layer).
    g_iron = ps.get("ironing_type")
    g_pat_top = ps.get("top_surface_pattern")
    report["objects_geometry"] = []
    report["top_coupon_row"] = a.top_coupon_row
    # a citation is accepted only when it names an existing .md sheet and a row/tile; any other text is "not resolvable"
    cite_ok = False
    if a.top_coupon_row:
        md_tok = next((t for t in a.top_coupon_row.split() if t.lower().endswith(".md")), None)
        cite_ok = bool(md_tok and os.path.isfile(md_tok) and re.search(r"\b(row|tile|step|variant)\s*[A-Za-z]?\d+", a.top_coupon_row, re.I))
        if not cite_ok:
            add("WARN", "C12", f"--top-coupon-row {a.top_coupon_row!r} is not resolvable (needs an existing .md sheet path and a row / tile number); treated as no citation")
    if a.no_geometry:
        add("OK", "C12", f"skipped (--no-geometry): project ironing_type {g_iron!r}, top_surface_pattern {g_pat_top!r}")
    else:
        keep = {str(ob.get("id")): {p.get("id") for p in (ob.get("parts") or []) if p.get("subtype") == "normal_part"} or {str(ob.get("id"))} for ob in objects}
        geom, gwarn = parse_geometry(z, keep)
        for w in gwarn:
            add("WARN", "C12", f"geometry: {w}")
        if not geom:
            add("WARN", "C12", f"no 3D/3dmodel.model in the file: flat tops not measured; project ironing_type {g_iron!r}, top_surface_pattern {g_pat_top!r}")
        for ob in objects:
            m = ob.get("meta") or {}
            normal_parts = [p for p in (ob.get("parts") or []) if p.get("subtype") == "normal_part"]
            # part > object > project (GUI_Factories.cpp v02.08.02.61 L101-102 / L107 list both keys for PARTS; PrintObject.cpp L3105-3115 applies volume config last)
            def eff(key, g_val):
                vals = {str(p.get("meta", {}).get(key)) for p in normal_parts if key in (p.get("meta") or {})}
                if vals:
                    return (sorted(vals)[0] if len(vals) == 1 else "mixed:" + "/".join(sorted(vals))), "part"
                if key in m:
                    return m[key], "object"
                return g_val, "project"
            o_iron, src_iron = eff("ironing_type", g_iron)
            o_pat, src_pat = eff("top_surface_pattern", g_pat_top)
            normal_ids = {p.get("id") for p in normal_parts}
            parts = [p for p in geom.get(str(ob.get("id")), []) if p["part_id"] in normal_ids or not normal_ids]
            if not parts:
                continue
            V = np.vstack([p["verts"] for p in parts])
            off, Fs = 0, []
            for p in parts:
                Fs.append(p["faces"] + off)
                off += len(p["verts"])
            fl = flat_up_faces(V, np.vstack(Fs))
            entry = {"object": ob.get("id"), "name": ob.get("name"), "ironing_type": o_iron, "ironing_type_source": src_iron,
                     "top_surface_pattern": o_pat, "top_surface_pattern_source": src_pat, **fl}
            report["objects_geometry"].append(entry)
            label = f"object {ob.get('id')} '{ob.get('name')}'"
            settings = f"ironing_type {o_iron!r} ({src_iron}), top_surface_pattern {o_pat!r} ({src_pat})"
            lv = "; ".join(f"z {zz}: {ar} mm2" for zz, ar in fl["levels"])
            if fl["flat_up_mm2"] >= a.flat_top_min:
                where = (f"flat up-facing area {fl['flat_up_mm2']} mm2 (largest levels {lv}; topmost z {fl['top_z']}: {fl['top_flat_mm2']} mm2; house thresholds {FLAT_UP_DEG:g} deg / "
                         f"{a.flat_top_min:g} mm2; pocket floors and covered faces count, negative parts not subtracted)")
                if cite_ok:
                    add("OK", "C12", f"{label}: {where}; {settings}; coupon row cited: {a.top_coupon_row}")
                else:
                    add("WARN", "C12", f"{label}: {where} with {settings}: if this top is visible, state Ironing Type and Top surface pattern with a reason "
                                       f"(pre-print checklist); cite a scored top-surface coupon row with "
                                       f"--top-coupon-row \"<sheet.md> tile N\", or write the prediction (no ironing with a Monotonic line top can show visible lines)")
                if str(o_iron) == "topmost" and fl["lower_flat_mm2"] >= a.flat_top_min:
                    add("WARN", "C12", f"{label}: Ironing Type 'Topmost surface' irons only the object's last layer (Fill.cpp v02.08.02.61 L973); {fl['lower_flat_mm2']} mm2 of flat top "
                                       f"below z {fl['top_z']} will not be ironed - use 'Top surfaces' if those faces are visible")
            else:
                add("OK", "C12", f"{label}: flat up-facing area {fl['flat_up_mm2']} mm2 < {a.flat_top_min:g} (house value); {settings}")

    # C13 support Top Z: the six keys, the style the slicer resolves, and what the typed Top Z becomes per the quantisation rules
    # (code reading, with the measured confirmations named). Every Top Z is "not verified" until a support-removal coupon row is
    # scored, unless --top-z-coupon-row cites a scored row for THIS Top Z, layer height and material. The printed
    # gap of a sliced plate is read back by tools/support_gap_readback.py.
    def _f(v, default=None):
        try:
            return float(str(v).strip().rstrip("%"))
        except (TypeError, ValueError):
            return default
    def _i(v, default=None):
        try:
            return int(float(str(v).strip()))
        except (TypeError, ValueError):
            return default
    def _round_half_away(x: float) -> int:   # std::round semantics (Python's round() is banker's)
        return int(math.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)
    sup_on = _i(ps.get("enable_support"), 0) == 1
    report["support_top_z"] = {"enable_support": sup_on, "coupon_row": a.top_z_coupon_row}
    if not sup_on:
        add("OK", "C13", f"support off (enable_support = {ps.get('enable_support')!r}); Top Z {ps.get('support_top_z_distance')!r} not in use")
    else:
        st, style = str(ps.get("support_type")), str(ps.get("support_style"))
        h = _f(ps.get("layer_height"), 0.2)
        top = _f(ps.get("support_top_z_distance"))
        range_hs = sorted({_f(r["opts"].get("layer_height")) for r in ranges if r["opts"].get("layer_height")} - {None})
        # variable layer height also comes from a per-object layer-heights profile (Metadata/layer_heights_profile.txt, bbs_3mf.cpp v02.08.02.61
        # L179 BBS_LAYER_HEIGHTS_PROFILE_FILE, read at L1999-2001); adaptive_layer_height is the process key
        try:
            lhp = z.read("Metadata/layer_heights_profile.txt").decode("utf-8", "replace").strip()
        except KeyError:
            lhp = ""
        variable_lh = bool(range_hs) or bool(lhp) or _i(ps.get("adaptive_layer_height"), 0) == 1
        # prime tower / independent layer height, the slicer's normalize_fdm_2 (PrintConfig.cpp v02.08.02.61 L7722-7768): the tower is
        # switched off when !smooth_timelapse && !wrapping && ((used_filaments == 1 && !mixed) || (ByObject && num_objects > 1)); a tower that stays on
        # forces independent_support_layer_height off. Used filaments = the plate's (slice_info <filament>), else the objects' extruder indices.
        indep_cfg = _i(ps.get("independent_support_layer_height"), 1) == 1
        tower_cfg = _i(ps.get("enable_prime_tower"), 0) == 1
        smooth = _i(ps.get("timelapse_type"), 0) == 1          # PrintConfig.hpp L227-230: tlTraditional = 0, tlSmooth = 1
        wrapping = _i(ps.get("enable_wrapping_detection"), 0) == 1
        by_object = str(ps.get("print_sequence", "")).lower().replace("_", " ") == "by object"
        used = set()
        try:
            si_xml = ET.fromstring(z.read("Metadata/slice_info.config"))
            for fil in si_xml.iter("filament"):
                if fil.get("id"):
                    used.add(str(fil.get("id")))
        except (KeyError, ET.ParseError):
            pass
        if not used:
            for ob in objects:
                used.add(str(_ext((ob.get("meta") or {}).get("extruder"), 1)))
                for p in ob.get("parts") or []:
                    if p.get("subtype") in C10_PART_SUBTYPES and "extruder" in (p.get("meta") or {}):
                        used.add(str(_ext(p["meta"]["extruder"], 1)))
        n_used = max(1, len(used))
        tower_on = tower_cfg and not ((not smooth and not wrapping) and ((n_used == 1) or (by_object and len(objects) > 1)))
        indep_eff = indep_cfg and not tower_on
        src_eff = "project settings + normalize_fdm_2 rule"
        # a sliced plate's header carries the post-normalize values: prefer them
        hdr = {}
        for k in range(1, len(plates) + 1):
            try:
                with z.open(f"Metadata/plate_{k}.gcode") as g:
                    for ln in g:
                        if ln.startswith(b"; enable_prime_tower = "):
                            hdr["tower"] = ln.split(b"=", 1)[1].strip().decode() == "1"
                        elif ln.startswith(b"; independent_support_layer_height = "):
                            hdr["indep"] = ln.split(b"=", 1)[1].strip().decode() == "1"
                        elif ln.startswith(b"; EXECUTABLE_BLOCK_START"):
                            break
            except KeyError:
                continue
            if hdr:
                break
        if hdr:
            tower_on = hdr.get("tower", tower_on)
            indep_eff = hdr.get("indep", indep_eff) and not tower_on if "indep" in hdr else indep_eff
            src_eff = "the sliced G-code header (post-normalize values)"
        if st.startswith("tree"):
            if style in ("default", "Default", "", "None"):
                resolved = "tree_organic" if (not variable_lh and (top or 0) > 0) else "tree_hybrid"   # SupportParameters.hpp L136-156; Print.cpp L1434-1443
                resolved_why = ("Default -> Tree Organic (no variable layer height, Top Z > 0; SupportParameters.hpp v02.08.02.61 L136-156)" if resolved == "tree_organic" else
                                "Default -> Tree Hybrid (variable layer height: a Height range Modifier layer height, a layer-heights profile or adaptive layers; or a soluble interface; SupportParameters.hpp L136-156, Print.cpp L1434-1443)")
            else:
                resolved, resolved_why = style, f"style {style!r} as set"
        else:
            resolved, resolved_why = "normal", f"support_type {st!r}"
        pred = {}
        hs = [h] + [x for x in range_hs if x and abs(x - h) > 1e-9]
        for hh in hs:
            if top is None or hh is None or hh <= 0:
                continue
            if resolved == "tree_organic":
                n = max(1, _round_half_away(top / hh))
                pred[str(hh)] = {"gap": round(n * hh, 3), "stacked": round(n * hh, 3), "rule": f"Tree Organic: round(Top Z / layer height) = {n} object layer(s) (TreeSupportCommon.hpp L280)"}
            elif resolved in ("tree_hybrid", "tree_slim", "tree_strong"):
                n = max(1, int(math.ceil(top / hh - 1e-6)))
                if indep_eff:
                    pred[str(hh)] = {"gap": round(top, 3), "stacked": round(n * hh, 3),
                                     "rule": f"Tree Hybrid, independent support layer height ON: exact typed value where one support layer can be Top Z thick (measured on flat ceilings of a support-removal coupon slice); "
                                             f"on sloped undersides or inside a Height range Modifier the support layers snap to the object grid and stack to {round(n * hh, 3)} mm ({n} x {hh}; TreeSupport.cpp L4062-4088, measured on a sliced plate)"}
                else:
                    pred[str(hh)] = {"gap": round(n * hh, 3), "stacked": round(n * hh, 3), "rule": f"Tree Hybrid, independent support layer height OFF (prime tower on): object layers accumulated until >= Top Z = {n} x {hh} (TreeSupport.cpp L3964-4086; code reading)"}
            else:
                if indep_eff:
                    pred[str(hh)] = {"gap": round(top, 3), "stacked": round(top, 3), "rule": "normal support, independent support layer height ON: print_z = bottom_z - gap, exact (SupportMaterial.cpp L1686-1769; code reading)"}
                else:
                    n = max(1, _round_half_away(top / hh + 1e-4))
                    pred[str(hh)] = {"gap": round(n * hh, 3), "stacked": round(n * hh, 3), "rule": f"normal support, independent OFF: round(gap / layer height) = {n} layer(s) (Slicing.cpp L116-124; code reading)"}
        per_obj = {}
        for ob in objects:
            m = ob.get("meta") or {}
            if "support_top_z_distance" in m:
                per_obj[f"{ob.get('id')} '{ob.get('name')}'"] = m["support_top_z_distance"]
        report["support_top_z"].update({"support_top_z_distance": top, "support_interface_top_layers": ps.get("support_interface_top_layers"),
                                        "support_interface_spacing": ps.get("support_interface_spacing"), "support_interface_filament": ps.get("support_interface_filament"),
                                        "support_type": st, "support_style": style, "resolved_style": resolved, "variable_layer_height": variable_lh,
                                        "independent_support_layer_height": indep_cfg, "independent_effective": indep_eff, "enable_prime_tower": tower_cfg, "prime_tower_effective": tower_on,
                                        "smooth_timelapse": smooth, "wrapping_detection": wrapping, "print_by_object": by_object, "filaments": len(ps.get("filament_settings_id") or []),
                                        "used_filaments": n_used, "effective_source": src_eff, "layer_heights": hs, "predicted": pred, "per_object_top_z": per_obj})
        if style == "tree_organic" and range_hs:
            add("WARN", "C13", "support_style tree_organic with a Height range Modifier layer height: the slicer refuses this combination (\"Variable layer height is not supported with Organic supports\", "
                               "Print.cpp v02.08.02.61 L1434-1443, return_code -51); the gap prediction below does not apply")
        same_fil = str(ps.get("support_interface_filament", "0")) in ("0", "0.0", "None")
        desc = (f"Top Z {top} mm, interface layers {ps.get('support_interface_top_layers')}, spacing {ps.get('support_interface_spacing')} mm, interface filament "
                f"{ps.get('support_interface_filament')!r}{' (= same filament as the part)' if same_fil else ''}; {st} / {style} -> {resolved} ({resolved_why}); "
                f"independent support layer height {'ON' if indep_eff else 'OFF'} (prime tower {'on' if tower_on else 'off'}, {n_used} used filament(s)"
                f"{', Smooth timelapse' if smooth else ''}{', wrapping detection' if wrapping else ''}{', by object' if by_object else ''}; {src_eff}); "
                f"layer heights {hs}; predicted printed gap {{{', '.join(f'{k}: {v['gap']}' + (f' exact on flat ceilings / {v['stacked']} grid-snapped' if v.get('stacked') not in (None, v['gap']) else '') for k, v in pred.items())}}}"
                + (f"; per-object Top Z {per_obj}" if per_obj else ""))
        # citation: the cited sheet row must be a SCORED row for this Top Z, layer height and material
        cite = check_top_z_citation(a.top_z_coupon_row, top, per_obj, h, ps.get("filament_settings_id") or []) if a.top_z_coupon_row else None
        report["support_top_z"]["citation"] = cite
        if cite and cite["ok"]:
            add("OK", "C13", f"{desc}; coupon row cited and matched: {cite['detail']}")
        else:
            if cite:
                add("WARN", "C13", f"--top-z-coupon-row {a.top_z_coupon_row!r}: {cite['detail']}; treated as no citation")
            add("WARN", "C13", f"{desc}. NOT VERIFIED (checklist Top Z line; not a print-qa FAIL on its own): a Top Z is a measured value - print a support-removal coupon, "
                               f"score it in a measurement sheet under {COUPON_ROOT} and cite the row with --top-z-coupon-row \"<sheet.md> variant A03\", "
                               f"and read the printed gap of this plate back with tools\\support_gap_readback.py --3mf <file> --plate N"
                               + ("; Height range Modifier present: inside it the gap snaps to the range's layer grid (TreeSupport.cpp L4062-4088)" if range_hs else ""))

    # C14 one material family per object and C15 process preset
    check_material_families(ps, objects, painted_objects(z), ranges, add)
    try:
        _vlh = bool(z.read("Metadata/layer_heights_profile.txt").strip())
    except KeyError:
        _vlh = False
    check_process_preset(ps, objects, a.process_reason, add, ranges=ranges, vlh_profile=_vlh)
    # C16 stale slice detector
    check_slice_freshness(z, ps, objects, plates, add)

    # C11 source assignment
    if a.source:
        report["source_assignment"] = check_source_assignment(a.source, ps, objects, parse_approvals(a.approve_swap), add)
    else:
        add("OK", "C11", "skipped: no --source given (the design-intent comparison needs the original 3MF; coupons generated by a script have none)")

    report["findings"] = findings
    worst = 0
    for f in findings:
        worst = max(worst, {"OK": 0, "WARN": 1, "FAIL": 2}[f["level"]])
    report["verdict"] = ["OK", "WARN", "FAIL"][worst]

    if a.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
    else:
        print(f"3MF audit: {a.path}")
        print(f"  printer={report['printer']}  process={report['process']}  bed={report['bed_type']}")
        for f in report["filaments"]:
            print(f"  filament {f['index']}: {f['id']} {f['type']} {f['colour']} ({f['profile']})")
        print(f"  global filament_map_mode={g_mode!r} ({MODE_LABEL.get(g_mode, g_mode)}), filament_map={g_map!r}")
        for fnd in findings:
            print(f"  [{fnd['level']}] {fnd['check']}: {fnd['msg']}")
        print(f"VERDICT: {report['verdict']}")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
