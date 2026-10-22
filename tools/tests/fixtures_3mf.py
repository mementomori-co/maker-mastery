r"""fixtures_3mf.py - synthetic Bambu-Studio-style 3MF files for the audit_3mf tests (test helper, not a tool).

Builds a minimal 3MF zip in a temporary folder holding only the members tools\audit_3mf.py reads:
Metadata/project_settings.config (JSON), Metadata/model_settings.config (XML), optional Metadata/slice_info.config,
Metadata/plate_N.json, Metadata/plate_N.gcode (+ .md5), Metadata/layer_config_ranges.xml and 3D/3dmodel.model (box meshes).
Nothing here is copied from Bambu Studio: every value is written by hand for the tests.

Importing this module ISOLATES the audit from the machine: it points MM_CONFIG at a temporary YAML whose Bambu Studio paths do
not exist except a synthetic colour catalogue, and APPDATA at an empty temporary folder. Import it BEFORE audit_3mf.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tempfile
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from xml.sax.saxutils import quoteattr

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
REPO = os.path.dirname(TOOLS)

WORK = tempfile.mkdtemp(prefix="mm_audit_tests_")
PROFILES = os.path.join(WORK, "profiles")
os.makedirs(os.path.join(PROFILES, "BBL", "filament"), exist_ok=True)
# synthetic colour catalogue (two colours of one line) in the shape audit_3mf.colour_index() reads
CATALOGUE = {"data": [
    {"fila_type": "PLA Basic", "fila_id": "GFA00", "fila_color_name": {"en": "Black"}, "fila_color": ["#000000FF"]},
    {"fila_type": "PLA Basic", "fila_id": "GFA00", "fila_color_name": {"en": "Jade White"}, "fila_color": ["#FFFFFFFF"]},
    {"fila_type": "PLA Matte", "fila_id": "GFA01", "fila_color_name": {"en": "Ivory White"}, "fila_color": ["#FFFFF0FF"]},
]}
with open(os.path.join(PROFILES, "BBL", "filament", "filaments_color_codes.json"), "w", encoding="utf-8") as _f:
    json.dump(CATALOGUE, _f)
_CFG = os.path.join(WORK, "paths.yaml")
with open(_CFG, "w", encoding="utf-8") as _f:
    _f.write('bambu_studio_exe: "' + os.path.join(WORK, "no-such-dir", "bambu-studio.exe").replace("\\", "/") + '"\n'
             'bambu_profiles_dir: "' + PROFILES.replace("\\", "/") + '"\n'
             'blender_exe: ""\nslice_workdir: "work/slice"\nallowed_roots: ["."]\nprotected_roots: []\n')
os.environ["MM_CONFIG"] = _CFG
_APPDATA = os.path.join(WORK, "appdata")
os.makedirs(_APPDATA, exist_ok=True)
os.environ["APPDATA"] = _APPDATA

TODAY = "2026-01-10"
VERIFIED = "2026-01-08"

BASE_PROJECT = {
    "printer_settings_id": "Bambu Lab H2C 0.4 nozzle", "printer_model": "Bambu Lab H2C",
    "print_settings_id": "0.20mm Standard @BBL H2C", "default_print_profile": "0.20mm Standard @BBL H2C",
    "layer_height": "0.2", "initial_layer_print_height": "0.2", "curr_bed_type": "Textured PEI Plate",
    "filament_settings_id": ["Bambu PLA Basic @BBL H2C"], "filament_ids": ["GFA00"], "filament_colour": ["#000000FF"],
    "filament_type": ["PLA"], "filament_vendor": ["Bambu Lab"], "filament_map_mode": "Manual", "filament_map": ["2"],
    "textured_plate_temp": ["55"], "textured_plate_temp_initial_layer": ["55"], "temperature_vitrification": ["70"],
    "max_bridge_length": "10", "enable_support": "0", "support_type": "normal(auto)", "support_style": "default",
    "support_top_z_distance": "0.2", "support_threshold_angle": "30", "sparse_infill_density": "15%",
    "sparse_infill_pattern": "grid", "wall_loops": "2", "top_shell_layers": "5", "bottom_shell_layers": "3",
    "nozzle_diameter": ["0.4", "0.4"], "enable_prime_tower": "0", "ironing_type": "no ironing",
    "top_surface_pattern": "monotonicline",
}


def project(**over) -> dict:
    p = json.loads(json.dumps(BASE_PROJECT))
    p.update(over)
    return p


def box(x0, y0, z0, x1, y1, z1):
    """8 vertices and 12 outward-facing triangles of an axis-aligned box."""
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (3, 7, 6), (3, 6, 2), (0, 4, 7), (0, 7, 3),
         (1, 2, 6), (1, 6, 5)]
    return v, f


def merge(*meshes):
    verts, faces = [], []
    for v, f in meshes:
        off = len(verts)
        verts += list(v)
        faces += [(a + off, b + off, c + off) for a, b, c in f]
    return verts, faces


def default_objects(name="test_block", ext="1", meta=None):
    return [{"id": "1", "name": name, "meta": {"extruder": ext, **(meta or {})},
             "parts": [{"id": "1", "subtype": "normal_part", "name": name, "meta": {}, "uuid": "00000001-0000-0000-0000-000000000001"}]}]


def default_plates(mode="Manual", maps="2", identify="101"):
    meta = {"plater_id": "1"}
    if mode is not None:
        meta["filament_map_mode"] = mode
    if maps is not None:
        meta["filament_maps"] = maps
    return [{"meta": meta, "instances": [{"object_id": "1", "instance_id": "0", "identify_id": identify}]}]


def _md(k, v):
    return f'<metadata key={quoteattr(str(k))} value={quoteattr(str(v))}/>'


def model_settings_xml(objects, plates) -> str:
    out = ['<?xml version="1.0" encoding="UTF-8"?>', "<config>"]
    for ob in objects:
        out.append(f'<object id="{ob["id"]}">')
        out.append(_md("name", ob["name"]))
        for k, v in (ob.get("meta") or {}).items():
            out.append(_md(k, v))
        for pt in ob.get("parts") or []:
            uu = f' uuid="{pt["uuid"]}"' if pt.get("uuid") else ""
            out.append(f'<part id="{pt["id"]}" subtype="{pt.get("subtype", "normal_part")}"{uu}>')
            out.append(_md("name", pt.get("name") or ""))
            for k, v in (pt.get("meta") or {}).items():
                out.append(_md(k, v))
            out.append("</part>")
        out.append("</object>")
    for pl in plates:
        out.append("<plate>")
        for k, v in pl["meta"].items():
            out.append(_md(k, v))
        for ins in pl.get("instances") or []:
            out.append("<model_instance>" + "".join(_md(k, v) for k, v in ins.items() if v is not None) + "</model_instance>")
        out.append("</plate>")
    out.append("</config>")
    return "\n".join(out)


def model_xml(meshes: dict, paint: bool = False) -> str:
    """meshes = {object id: (verts, faces)}; one build item per object, identity transform plus a plate offset."""
    ns = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
    out = [f'<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xmlns="{ns}"><resources>']
    for oid, (v, f) in meshes.items():
        out.append(f'<object id="{oid}" type="model"><mesh><vertices>')
        out += [f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in v]
        out.append("</vertices><triangles>")
        pa = ' paint_color="4"' if paint else ""
        out += [f'<triangle v1="{a}" v2="{b}" v3="{c}"{pa}/>' for a, b, c in f]
        out.append("</triangles></mesh></object>")
    out.append("</resources><build>")
    out += [f'<item objectid="{oid}" transform="1 0 0 0 1 0 0 0 1 100 100 0" printable="1"/>' for oid in meshes]
    out.append("</build></model>")
    return "".join(out)


def gcode(proj: dict, total="1m 40s", weight="1.50", fil_map="2", map_mode="Manual", start=(), config_over=None) -> str:
    """A tiny plate G-code: HEADER block, CONFIG block (fresh keys copied from the project), start section, one move."""
    cfg = dict(proj)
    cfg.update(config_over or {})
    lines = ["; HEADER_BLOCK_START", f"; model printing time: 1m 0s; total estimated time: {total}",
             f"; total filament weight [g] : {weight}", "; HEADER_BLOCK_END", "; CONFIG_BLOCK_START",
             f"; filament_map = {fil_map}", f"; filament_map_mode = {map_mode}"]
    for k, v in cfg.items():
        if k in ("filament_map", "filament_map_mode"):
            continue
        lines.append(f"; {k} = " + (";".join(map(str, v)) if isinstance(v, list) else str(v)))
    lines += ["; CONFIG_BLOCK_END", *start, "; MACHINE_START_GCODE_END", "; EXECUTABLE_BLOCK_START",
              "; FEATURE: Outer wall", "G1 X110 Y110 E1", "; EXECUTABLE_BLOCK_END"]
    return "\n".join(lines) + "\n"


def slice_info_xml(prediction="100", weight="1.50", maps="2", identify="101", fils=(("1", "PLA", "#000000"),), extra=None) -> str:
    meta = {"index": "1", "prediction": prediction, "weight": weight, "outside": "false", "support_used": "false"}
    if maps is not None:
        meta["filament_maps"] = maps
    meta.update(extra or {})
    out = ["<config><plate>"] + [_md(k, v) for k, v in meta.items()]
    out.append(f'<object identify_id="{identify}" name="test_block" skipped="false"/>')
    out += [f'<filament id="{i}" type="{t}" color="{c}" used_g="1.5"/>' for i, t, c in fils]
    out.append("</plate></config>")
    return "".join(out)


_count = [0]


def build(proj=None, objects=None, plates=None, meshes=None, slice_info=None, gcodes=None, md5=True, plate_json=None,
          ranges_xml=None, layer_profile=None, paint=False, name=None) -> str:
    """Write a 3MF and return its path. gcodes = {plate number: text}; md5 True writes the matching .md5, a string writes it."""
    _count[0] += 1
    path = os.path.join(WORK, (name or f"case_{_count[0]}") + ".3mf")
    proj = project() if proj is None else proj
    objects = default_objects() if objects is None else objects
    plates = default_plates() if plates is None else plates
    meshes = {"1": box(0, 0, 0, 10, 10, 10)} if meshes is None else meshes
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        if meshes:
            z.writestr("3D/3dmodel.model", model_xml(meshes, paint))
        z.writestr("Metadata/project_settings.config", json.dumps(proj))
        z.writestr("Metadata/model_settings.config", model_settings_xml(objects, plates))
        for n, pj in (plate_json or {}).items():
            z.writestr(f"Metadata/plate_{n}.json", json.dumps(pj))
        for n, text in (gcodes or {}).items():
            b = text.encode("utf-8")
            z.writestr(f"Metadata/plate_{n}.gcode", b)
            if md5 is True:
                z.writestr(f"Metadata/plate_{n}.gcode.md5", hashlib.md5(b).hexdigest().upper())
            elif isinstance(md5, str):
                z.writestr(f"Metadata/plate_{n}.gcode.md5", md5)
        if ranges_xml:
            z.writestr("Metadata/layer_config_ranges.xml", ranges_xml)
        if layer_profile:
            z.writestr("Metadata/layer_heights_profile.txt", layer_profile)
        if slice_info:
            z.writestr("Metadata/slice_info.config", slice_info)   # written after model_settings, as Bambu Studio does
    return path


GOOD_ROWS = [
    ("H2C - AMS 2 Pro slot 1 (RIGHT inlet)", "**Bambu PLA Basic, Black**", "looked at the AMS screen"),
    ("H2C - AMS 2 Pro slot 2 (RIGHT inlet)", "EMPTY", "looked"),
    ("H2C - LEFT external spool holder", "EMPTY", "looked"),
    ("H2C - plate on the bed", "Textured PEI", "looked at the bed"),
]


def load_note(rows=None, verified=VERIFIED, name=None) -> str:
    _count[0] += 1
    path = os.path.join(WORK, (name or f"load_{_count[0]}") + ".md")
    lines = ["# Current load (test)", "", "Applies to: test", ""]
    if verified is not None:
        lines.append(f"Verified: {verified}")
    lines += ["", "| Position | Content | How known |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in (GOOD_ROWS if rows is None else rows)]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def run(path: str, *args, note: str | None = None, today: str = TODAY, geometry: bool = True):
    """Run audit_3mf.main in-process with --json; returns (exit code, report dict)."""
    import audit_3mf
    argv = ["audit_3mf.py", path, "--json", "--today", today, "--load-note", note or load_note()]
    if not geometry:
        argv.append("--no-geometry")
    argv += list(args)
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = audit_3mf.main(argv)
    return rc, json.loads(out.getvalue())


def find(report: dict, check: str, rule: str | None = None) -> list:
    return [f for f in report["findings"] if f["check"] == check and (rule is None or f.get("rule") == rule)]


def levels(rows: list) -> set:
    return {f["level"] for f in rows}
