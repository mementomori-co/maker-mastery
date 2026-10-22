r"""log_run.py - Claude Code SubagentStop hook (matcher: .*).

What it does: appends one JSON line per finished subagent to <repo>\work\agent-runs.log (work\ is git-ignored), so silent
failures are visible: timestamp, event, agent_type, session_id, cwd, stop_hook_active. Exit 0 always (never blocks).
Input: the hook JSON on stdin. Output: the log line (the MM_RUN_LOG environment variable overrides the log path).
Doc: https://code.claude.com/docs/en/hooks
Example (manual run, PowerShell): '{"agent_type": "print-qa"}' | .venv\Scripts\python.exe -B tools\hooks\log_run.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

LOG = os.environ.get("MM_RUN_LOG") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "work", "agent-runs.log")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        payload = {}
    line = {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "event": payload.get("hook_event_name"),
        "agent_type": payload.get("agent_type") or payload.get("agent_name"),
        "session_id": payload.get("session_id"),
        "cwd": payload.get("cwd"),
        "stop_hook_active": payload.get("stop_hook_active"),
    }
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
