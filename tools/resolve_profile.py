r"""resolve_profile.py - resolve the `inherits` chain AND the `include` templates of installed Bambu Studio system profiles.

Why: the leaf JSON (e.g. "0.20mm Standard @BBL H2C.json") rarely contains the key you care about; `max_bridge_length = 0`
lives three parents up in fdm_process_common.json. This prints the EFFECTIVE value and the chain it came through.
Merge order = the slicer's (PresetBundle.cpp v02.08.02.61 L4859 parent, L4885-4894 includes, L4908 own keys;
https://github.com/bambulab/BambuStudio): parent chain -> each `include` template in listed order (a later include wins
over an earlier one) -> the file's own keys, so a value the leaf sets wins over its include, and an include wins over the
parents (e.g. the H2C filament leaves include `fdm_filament_template_direct_dual_e3d`, which carries 3-variant arrays such
as filament_cooling_before_tower; the H2C machine leaf pulls its start G-code from
`Bambu Lab H2C 0.4 nozzle template machine_start_gcode`). `set_in` names the file or "include:<template>" that set the
final value.
Known approximation (documented, not a bug on the 02.08 profile bundle): the slicer applies only the include keys whose
value differs from the include's own type default (`apply_only(include, include.diff(default))`, Config.cpp L501-511; array
length counts, Config.hpp L729-735); this tool applies every value key of the include. The two outputs differ only when (a) an
include value equals the type default exactly (same length) while a parent sets something else - slicer keeps the parent, tool
reports the include - or (b) an include key is not a defined option - slicer drops it, tool reports it. A scan of every
installed template (4 filament, 89 machine) found no such case.
Nested includes (an include that itself has `inherits` or `include`) are refused with a clear error; none is installed.

Inputs: the installed profile JSON files (read-only). Default root: bambu_profiles_dir from config\paths.yaml, else
%APPDATA%\BambuStudio\system\BBL, else <Bambu Studio install>\resources\profiles\BBL.
Output: the chain and each key's effective value (or --json). Exit 0 on success, 1 if a profile name is not found.
Usage (run with .venv\Scripts\python.exe):
  tools\resolve_profile.py --kind process "0.20mm Standard @BBL H2C" --keys max_bridge_length support_threshold_angle
  tools\resolve_profile.py --kind machine  "Bambu Lab H2C 0.4 nozzle" --keys extruder_printable_area extruder_printable_height
  tools\resolve_profile.py --kind filament "Bambu PETG HF @BBL H2C" --all
  tools\resolve_profile.py --list process H2C          # list profile names containing H2C
Options:
  --root PATH   profile root (the folder that holds process\, machine\, filament\)
  --json        machine-readable output
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_config  # noqa: E402


def _default_roots() -> list[str]:
    """<root>\\BBL for each profile root from config\\paths.yaml (bambu_profiles_dir, or %APPDATA% then the install)."""
    try:
        return [str(r / "BBL") for r in mm_config.bambu_profile_roots()]
    except Exception:  # noqa: BLE001
        return []


DEFAULT_ROOTS = _default_roots()
KINDS = ("process", "machine", "filament")


def load_index(root: str, kind: str) -> dict[str, tuple[str, dict]]:
    idx: dict[str, tuple[str, dict]] = {}
    for f in glob.glob(os.path.join(root, kind, "**", "*.json"), recursive=True):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(d, dict) and "name" in d:
            idx[d["name"]] = (f, d)
    return idx


META_KEYS = ("inherits", "include")   # structural keys, never values


def resolve(idx: dict[str, tuple[str, dict]], name: str, chain: list[str], origins: dict[str, str] | None = None) -> dict:
    """Effective values of `name`, in the slicer's own merge order (PresetBundle.cpp):
    the `inherits` parent chain first, then each `include` template in the order listed, then the file's own keys. `chain` lists the
    files in leaf-first order with the templates as "include:<name>" after the file that pulls them in; `origins` (if given) records
    which file set each key's final value. Approximation (documented): the slicer applies only those include keys that differ
    from the include file's own type defaults; this tool applies every value key of the include, which is the same result whenever
    the include's value differs from the default."""
    if name not in idx:
        raise KeyError(name)
    path, d = idx[name]
    chain.append(name)
    i_leaf = len(chain) - 1
    parent = d.get("inherits")
    base = resolve(idx, parent, chain, origins) if parent else {}
    out = dict(base)
    n_inc = 0
    includes = d.get("include") or []
    if isinstance(includes, str):          # the slicer accepts a bare string too (PresetBundle.cpp L4863-4866)
        includes = [includes]
    for inc in includes:
        if inc not in idx:
            raise KeyError(f"{name}: include {inc!r} not found")
        inc_d = idx[inc][1]
        if any(k in inc_d for k in META_KEYS):
            raise KeyError(f"{name}: include {inc!r} carries its own inherits/include; nested include not supported")
        n_inc += 1
        chain.insert(i_leaf + n_inc, "include:" + inc)   # printed right after the file that pulls it in
        for k, v in inc_d.items():
            if k in META_KEYS:
                continue
            out[k] = v
            if origins is not None:
                origins[k] = "include:" + inc
    for k, v in d.items():
        if k in META_KEYS:
            continue
        out[k] = v
        if origins is not None:
            origins[k] = name
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", choices=KINDS)
    ap.add_argument("names", nargs="*")
    ap.add_argument("--keys", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", nargs=2, metavar=("KIND", "SUBSTRING"))
    ap.add_argument("--root")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv[1:])

    roots = [a.root] if a.root else [r for r in DEFAULT_ROOTS if os.path.isdir(r)]
    if not roots:
        print("no profile root found: set bambu_profiles_dir or bambu_studio_exe in config\\paths.yaml, or pass --root", file=sys.stderr)
        return 1
    root = roots[0]

    if a.list:
        kind, sub = a.list
        idx = load_index(root, kind)
        for n in sorted(idx):
            if sub.lower() in n.lower():
                print(n)
        return 0

    if not a.kind or not a.names:
        ap.print_help()
        return 1
    idx = load_index(root, a.kind)
    result = {"root": root, "kind": a.kind, "profiles": {}}
    rc = 0
    for name in a.names:
        chain: list[str] = []
        origins: dict[str, str] = {}
        try:
            eff = resolve(idx, name, chain, origins)
        except KeyError as e:
            print(f"NOT FOUND: {e.args[0]} (in {root}\\{a.kind})", file=sys.stderr)
            rc = 1
            continue
        keys = list(eff.keys()) if a.all else (a.keys or [])
        entry = {"chain": chain, "values": {}}
        for k in keys:
            if k in eff:
                entry["values"][k] = {"value": eff[k], "set_in": origins.get(k)}
            else:
                entry["values"][k] = {"value": None, "set_in": None}
        result["profiles"][name] = entry
        if not a.json:
            print(f"=== {name}")
            print("  chain: " + " -> ".join(chain))
            for k, v in entry["values"].items():
                print(f"  {k} = {v['value']!r}   (set in: {v['set_in']})")
    if a.json:
        print(json.dumps(result, indent=1, ensure_ascii=False))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
