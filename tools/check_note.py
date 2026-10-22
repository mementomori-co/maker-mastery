r"""check_note.py - validate a knowledge note against templates\note.md.

What it does: reads one or more Markdown notes and prints PASS or FAIL with the reasons.
Usage:
  .venv\Scripts\python.exe tools\check_note.py <note.md> [...]   -> PASS/FAIL per file; exit 0 if all pass, 2 otherwise
  As a Claude Code PostToolUse hook it reads the hook JSON on stdin, checks tool_input.file_path if it is a knowledge note
  under this repository, exits 2 with the reason on stderr to block, 0 otherwise. Files in knowledge\00-gear-inventory\
  (your own gear and load records) and README.md files are skipped in hook mode: they are records, not cited notes.
Example: .venv\Scripts\python.exe tools\check_note.py knowledge\02-bambu-studio\index.md

Rules checked:
  1. A line starting with "Applies to:" exists.
  2. A line containing "Verified: YYYY-MM-DD" exists.
  3. A "Sources:" line exists and at least one line after it contains a URL (http...) or a local path (C:\ or %APPDATA%).
  4. Every bullet under "## Facts" contains a URL, a local path, or the word "measured" (a fact needs a source).
  5. HDT values carry their load: a line with "HDT" must mention MPa.
"""
from __future__ import annotations

import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
from pathlib import Path

KNOWLEDGE_MARK = re.compile(r"[\\/]knowledge[\\/]", re.I)
GEAR_MARK = re.compile(r"[\\/]knowledge[\\/]00-gear-inventory[\\/]", re.I)
# Hook scope: a user-level hook fires in every project, so in hook mode this script is a no-op for any file outside
# <repo>\knowledge\ or <repo>\research\ (repo = parent of tools\).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK_SCOPE = tuple(os.path.normcase(os.path.join(REPO_ROOT, d)) for d in ("knowledge", "research"))


def in_hook_scope(fp: str) -> bool:
    try:
        q = os.path.normcase(os.path.normpath(os.path.abspath(fp.strip().strip('"'))))
    except Exception:  # noqa: BLE001
        return False
    return any(q == sc or q.startswith(sc + os.sep) for sc in HOOK_SCOPE)
URL = re.compile(r"https?://\S+")
LOCAL = re.compile(r"(?:[A-Za-z]:\\|%APPDATA%|%LOCALAPPDATA%)")
DATE = re.compile(r"Verified:\s*\d{4}-\d{2}-\d{2}")


def check(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        return [f"cannot read: {exc}"]
    lines = text.splitlines()
    if not any(l.startswith("Applies to:") or " Applies to:" in l for l in lines):
        problems.append("missing 'Applies to:' line")
    if not DATE.search(text):
        problems.append("missing 'Verified: YYYY-MM-DD'")
    src_idx = next((i for i, l in enumerate(lines) if l.strip().startswith("Sources:")), None)
    if src_idx is None:
        problems.append("missing 'Sources:' section")
    else:
        tail = "\n".join(lines[src_idx + 1 :])
        if not (URL.search(tail) or LOCAL.search(tail)):
            problems.append("'Sources:' has no URL or local path")
    # Facts bullets need a source
    in_facts = False
    for n, l in enumerate(lines, 1):
        if l.startswith("## "):
            in_facts = l.strip().lower().startswith("## facts")
            continue
        if in_facts and l.lstrip().startswith("- "):
            if not (URL.search(l) or LOCAL.search(l) or "measured" in l.lower() or "manual §" in l or "manual p." in l):
                problems.append(f"line {n}: fact bullet without URL / local path / 'measured'")
            if "HDT" in l and "MPa" not in l:
                problems.append(f"line {n}: HDT without load (MPa)")
    return problems


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    hook_mode = False
    if not paths and not sys.stdin.isatty():
        hook_mode = True
        try:
            payload = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0
        fp = (payload.get("tool_input") or {}).get("file_path") or ""
        if not fp or not isinstance(fp, str) or not in_hook_scope(fp):
            return 0  # outside <repo>\knowledge\ and \research\: never block work in another project
        if not KNOWLEDGE_MARK.search(fp) or not fp.lower().endswith(".md") or fp.lower().endswith("index.md"):
            return 0
        if GEAR_MARK.search(fp) or fp.lower().endswith("readme.md"):
            return 0  # your own gear records and folder READMEs are not cited notes; audit_3mf checks the load file

        paths = [Path(fp)]
    if not paths:
        print(__doc__)
        return 0
    failed = False
    for p in paths:
        probs = check(p)
        if probs:
            failed = True
            msg = f"FAIL {p}\n  - " + "\n  - ".join(probs)
            print(msg, file=sys.stderr if hook_mode else sys.stdout)
        else:
            if not hook_mode:
                print(f"PASS {p}")
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
