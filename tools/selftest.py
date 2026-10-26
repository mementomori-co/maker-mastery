r"""selftest.py - run every unit test in tools\tests and say, tool by tool, whether it works on this PC.

What it does: runs each tools\tests\test_*.py file in its own process with this Python (unittest, no __pycache__ written),
then prints one plain-English line per tool: PASS, FAIL, or SKIPPED (an optional package is missing). No test needs
Bambu Studio, Blender or the internet, and nothing is printed, sliced or sent.
Inputs: none (the tests build their own small files in your temp folder).
Output: a PASS/FAIL table; exit 0 when nothing failed, 1 when a test failed.
Usage: .venv\Scripts\python.exe -B tools\selftest.py [--verbose]
Example: .venv\Scripts\python.exe -B tools\selftest.py
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(TOOLS, "tests")

# test file -> the tools it covers, in plain words
COVERS = {
    "test_audit_load.py": "audit_3mf.py - load check against your current-load.md (C7)",
    "test_audit_checks.py": "audit_3mf.py - slicer-setting checks C1-C16",
    "test_config_and_cli.py": "mm_config.py, resolve_profile.py, slice_cli.py guards, check_note.py, check_skill.py, build_indexes.py",
    "test_gcode_paths.py": "gcode_paths.py - G-code reader with arcs",
    "test_gcode_audit.py": "gcode_audit.py - extents, support and bridge report",
    "test_tower.py": "tower_bounds.py, tower_clearance.py, mcp\\tower_clearance_3mf.py - prime tower",
    "test_support_gap_readback.py": "support_gap_readback.py - printed support Top Z gap",
    "test_overhang_gate.py": "overhang_gate.py - overhangs, cantilever and islands",
    "test_stability_check.py": "stability_check.py - does a display piece tip over",
    "test_interface_coverage.py": "interface_coverage.py - support under visible overhangs",
    "test_visible_ratio.py": "visible_ratio.py - how much of the part support hides",
    "test_render_critic.py": "render_critic.py - render critique (needs optional open3d)",
    "test_hooks.py": "hooks\\guard_paths.py, hooks\\session_start.py, hooks\\log_run.py - Claude Code hooks",
    "test_mcp_audit_server.py": "mcp\\mm_audit_server.py - read-only audit MCP server",
    "test_privacy_scan.py": "privacy_scan.py - personal-data scan",
    "test_ollama_check.py": "ollama_check.py - Ollama mode readiness check (fake local server)",
}


def run_file(path: str) -> tuple[str, int, int, int, float, str]:
    """-> (verdict, ran, failed, skipped, seconds, output)."""
    t0 = time.time()
    p = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", TESTS, "-p", os.path.basename(path)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=TOOLS, timeout=1800)
    out = (p.stdout or "") + (p.stderr or "")
    ran = int((re.search(r"Ran (\d+) tests?", out) or [0, 0])[1])
    m = re.search(r"FAILED \(([^)]*)\)", out)
    failed = sum(int(x) for x in re.findall(r"(?:failures|errors)=(\d+)", m.group(1))) if m else 0
    skipped = int((re.search(r"skipped=(\d+)", out) or [0, 0])[1])
    if p.returncode != 0:
        verdict = "FAIL"
        failed = failed or 1
    elif ran and skipped == ran:
        verdict = "SKIPPED"
    else:
        verdict = "PASS"
    return verdict, ran, failed, skipped, time.time() - t0, out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true", help="print the full unittest output of every file")
    a = ap.parse_args(argv)
    files = sorted(glob.glob(os.path.join(TESTS, "test_*.py")))
    if not files:
        print("No tests found in tools\\tests.")
        return 1
    print(f"Self-test: {len(files)} test files, Python {sys.version.split()[0]} at {sys.executable}")
    print("Nothing here prints, slices or sends anything.\n")
    bad = 0
    for f in files:
        name = os.path.basename(f)
        verdict, ran, failed, skipped, secs, out = run_file(f)
        what = COVERS.get(name, name)
        extra = f"{ran} checks" + (f", {skipped} skipped" if skipped else "") + (f", {failed} failed" if failed else "")
        print(f"  {verdict:7s} {what}  ({extra}, {secs:.1f} s)")
        if verdict == "FAIL":
            bad += 1
        if a.verbose or verdict == "FAIL":
            print("\n".join("           " + ln for ln in out.strip().splitlines()[-25:]))
        if verdict == "SKIPPED" or (skipped and a.verbose):
            reasons = sorted(set(re.findall(r"skipped '([^']+)'", out)))
            for r in reasons[:3]:
                print(f"           skipped because: {r}")
    print()
    if bad:
        print(f"RESULT: FAIL - {bad} test file(s) failed. Read the lines above; nothing is broken on your printer.")
        return 1
    print("RESULT: PASS - every tool that could be tested works on this PC.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
