r"""session_start.py - Claude Code SessionStart hook (matcher: startup|resume|clear).

What it does: prints lessons\INDEX.md to stdout so the lessons enter the session context. When there is no INDEX.md it
falls back to reading lessons\*.md and printing each file name, first heading and its "Rule now" cells (the third column
of the post-mortem table). Capped at 60 lines. Exit 0 always: the hook must never block or fail a session.
Inputs: the hook JSON on stdin (drained, not used); <repo>\lessons\ (or the folder in the MM_LESSONS environment variable).
Output: text on stdout (a SessionStart hook's stdout is added to Claude's context).
Doc: https://code.claude.com/docs/en/hooks
Example (manual run): .venv\Scripts\python.exe tools\hooks\session_start.py < NUL
"""
from __future__ import annotations

import glob
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

LESSONS = os.environ.get("MM_LESSONS") or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "lessons")
MAX_LINES = 60


def main() -> int:
    # A hook can fire in every project. It must never block or fail a session: no lessons folder -> print nothing;
    # any error -> exit 0 (see __main__).
    try:
        if not sys.stdin.isatty():
            sys.stdin.read()  # drain the hook JSON; nothing in it changes the output
    except Exception:  # noqa: BLE001
        pass
    if not os.path.isdir(LESSONS):
        return 0
    index = os.path.join(LESSONS, "INDEX.md")
    if os.path.isfile(index):
        lines = open(index, encoding="utf-8", errors="replace").read().splitlines()
        out = ["[Maker Mastery] lessons\\INDEX.md (read the lesson files for root causes):"] + lines[:MAX_LINES]
        if len(lines) > MAX_LINES:
            out.append("    (truncated; open lessons\\INDEX.md)")
        out.append("[Maker Mastery] Rules: CLAUDE.md. No AI ever starts, sends, uploads or queues a print.")
        sys.stdout.write("\n".join(out) + "\n")
        return 0
    files = sorted(glob.glob(os.path.join(LESSONS, "*.md")))
    out = [f"[Maker Mastery] {len(files)} lessons in {LESSONS} (rules extracted; read the files for root causes):"]
    for f in files:
        try:
            text = open(f, encoding="utf-8", errors="replace").read()
        except Exception:  # noqa: BLE001
            continue
        title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), os.path.basename(f))
        out.append(f"- {os.path.basename(f)} — {title}")
        for line in text.splitlines():
            if line.startswith("|") and not line.startswith("|---") and "Rule now" not in line and "What happened" not in line:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[2]:
                    rule = re.sub(r"\s+", " ", cells[2])
                    out.append(f"    rule: {rule[:220]}")
        if len(out) > MAX_LINES:
            out.append("    (truncated; open the lessons folder)")
            break
    out.append("[Maker Mastery] Rules: CLAUDE.md. No AI ever starts, sends, uploads or queues a print.")
    sys.stdout.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001
        sys.exit(0)
