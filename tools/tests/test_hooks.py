r"""Tests for tools\hooks\guard_paths.py, session_start.py and log_run.py, called the way Claude Code calls them:
the interpreter with -B, the hook JSON on stdin. Protected roots come from a temporary config (MM_CONFIG).
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p test_hooks.py -v
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(TOOLS)
PY = sys.executable
HOOKS = os.path.join(TOOLS, "hooks")


def hook(script: str, payload, env_extra: dict | None = None):
    env = dict(os.environ)
    env.update(env_extra or {})
    data = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run([PY, "-B", os.path.join(HOOKS, script)], input=data, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env, timeout=60)


class GuardPathsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.td = tempfile.mkdtemp(prefix="mm_guard_")
        cls.prot = os.path.join(cls.td, "Finished Projects")
        os.makedirs(cls.prot)
        cls.cfg = os.path.join(cls.td, "paths.yaml")
        with open(cls.cfg, "w", encoding="utf-8") as fh:
            fh.write(f'protected_roots: ["{cls.prot.replace(chr(92), "/")}"]\n')
        cls.env = {"MM_CONFIG": cls.cfg, "MM_PROTECTED": ""}

    def run_guard(self, ti: dict, cwd: str | None = None):
        p = {"tool_name": "x", "tool_input": ti}
        if cwd:
            p["cwd"] = cwd
        return hook("guard_paths.py", p, self.env)

    def test_write_inside_protected_root_blocked(self):
        r = self.run_guard({"file_path": os.path.join(self.prot, "a.txt")})
        self.assertEqual(r.returncode, 2)
        self.assertIn("protected root", r.stderr)
        self.assertIn("config\\paths.yaml", r.stderr)

    def test_write_elsewhere_allowed_quietly(self):
        r = self.run_guard({"file_path": os.path.join(self.td, "other", "a.txt")})
        self.assertEqual((r.returncode, r.stderr), (0, ""))
        r = self.run_guard({"notebook_path": os.path.join(REPO, "work", "n.ipynb")})
        self.assertEqual(r.returncode, 0)

    def test_shell_commands(self):
        q = f'"{self.prot}'
        self.assertEqual(self.run_guard({"command": f'rm -rf {q}\\x"'}, cwd=self.td).returncode, 2)
        self.assertEqual(self.run_guard({"command": f'echo hi > {q}\\x.txt"'}, cwd=self.td).returncode, 2)
        self.assertEqual(self.run_guard({"command": f'cat {q}\\x.txt"'}, cwd=self.td).returncode, 0)
        self.assertEqual(self.run_guard({"command": f'cp {q}\\x.txt" "{self.td}\\y.txt"'}, cwd=self.td).returncode, 0)
        self.assertEqual(self.run_guard({"command": f'cp "{self.td}\\y.txt" {q}\\x.txt"'}, cwd=self.td).returncode, 2)
        self.assertEqual(self.run_guard({"command": f'cd {q}"'}, cwd=self.td).returncode, 2)
        self.assertEqual(self.run_guard({"command": "ls -la"}, cwd=self.td).returncode, 0)

    def bypasses(self) -> list[str]:
        """Write commands an independent audit found passing the guard (all must be blocked, both modes)."""
        p = self.prot
        return [
            f'find "{p}" -delete',
            f'find "{p}" -exec rm {{}} \\;',
            f'find "{p}" -name "*.txt" -execdir rm {{}} +',
            f'Get-ChildItem "{p}" | ForEach-Object {{ Remove-Item $_.FullName }}',
            f'gci "{p}" | % {{ ri $_.FullName }}',
            f'gci "{p}" | ? {{ ri $_ }}',
            f'sort -o "{p}\\f" a.txt',
            f'sort a.txt --output="{p}\\f"',
            f'uniq a.txt "{p}\\f"',
            f'tree -o "{p}\\f"',
            f'xxd -r a.txt "{p}\\f"',
            f'rg --pre rm x "{p}"',
            f'cat a.txt>"{p}\\f"',
            f'cat a.txt>>"{p}\\f"',
            f'echo x 1>"{p}\\f"',
            f'echo x 2>"{p}\\f"',
            f'Get-Content a.txt *>"{p}\\f"',
            f'ls "{p}" | Select-Object @{{n="x";e={{ri $_}}}}',
        ]

    def test_audit_bypasses_blocked_normal_mode(self):
        for cmd in self.bypasses():
            with self.subTest(cmd=cmd):
                self.assertEqual(self.run_guard({"command": cmd}, cwd=self.td).returncode, 2)

    def test_audit_bypasses_blocked_fail_closed(self):
        cfg = os.path.join(self.td, "broken_bp.yaml")
        with open(cfg, "w", encoding="utf-8") as fh:
            fh.write('protected_roots: [\n')   # unclosed list: a YAML error for PyYAML and the built-in reader
        env = {"MM_CONFIG": cfg, "MM_PROTECTED": ""}
        for cmd in self.bypasses():
            with self.subTest(cmd=cmd):
                r = hook("guard_paths.py", {"tool_input": {"command": cmd}, "cwd": self.td}, env)
                self.assertEqual(r.returncode, 2)
                self.assertIn("cannot be read", r.stderr)
        for cmd in ("cat a.txt | grep x", "Get-Content a.txt | Select-Object -First 3", "ls -la 2>&1"):
            with self.subTest(cmd=cmd):
                r = hook("guard_paths.py", {"tool_input": {"command": cmd}, "cwd": self.td}, env)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_reads_and_arrows_still_allowed(self):
        p, out = self.prot, os.path.join(self.td, "out.txt")
        for cmd in (
            f'ls "{p}" | sort',
            f'cat "{p}\\x.txt" | uniq -c',
            f'Get-ChildItem "{p}" | Where-Object Length -gt 0',
            f'gci "{p}" | % FullName',
            f'cat "{p}\\x.txt" > "{out}"',
            f'cat "{p}\\x.txt">"{out}"',
            f'cat "{p}\\x.txt" 2>&1',
            f'cat "{p}\\x.txt" 2>/dev/null',
            f'grep "->" "{p}\\x.txt"',
            f'grep "=>" "{p}\\x.txt"',
            f'grep ">=" "{p}\\x.txt"',
            f'find "{self.td}" -name "*.txt" -delete',   # no protected root named
        ):
            with self.subTest(cmd=cmd):
                r = self.run_guard({"command": cmd}, cwd=self.td)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_redirect_regex(self):
        sys.path.insert(0, HOOKS)
        import guard_paths
        hits = {"a>b": "b", "a>>b": "b", "1>b": "b", "2>b": "b", "*>b": "b", 'a > "c d"': '"c d"', "x 2>>log": "log"}
        for text, tgt in hits.items():
            with self.subTest(text=text):
                m = guard_paths.REDIRECT.search(text)
                self.assertIsNotNone(m)
                self.assertEqual(m.group(1), tgt)
        for text in ("def f() -> int", "$h = @{a => 1}", "if a >= b", "x <> y"):
            with self.subTest(text=text):
                self.assertIsNone(guard_paths.REDIRECT.search(text))

    def test_bare_python_inside_repo_only(self):
        r = self.run_guard({"command": "python tools/x.py"}, cwd=REPO)
        self.assertEqual(r.returncode, 2)
        self.assertIn(".venv", r.stderr)
        self.assertEqual(self.run_guard({"command": "python x.py"}, cwd=self.td).returncode, 0)
        self.assertEqual(self.run_guard({"command": ".venv/Scripts/python.exe -B tools/x.py"}, cwd=REPO).returncode, 0)

    def test_no_roots_configured_is_quiet(self):
        cfg = os.path.join(self.td, "empty.yaml")
        with open(cfg, "w", encoding="utf-8") as fh:
            fh.write("protected_roots: []\n")
        r = hook("guard_paths.py", {"tool_input": {"file_path": os.path.join(self.prot, "a.txt")}}, {"MM_CONFIG": cfg, "MM_PROTECTED": ""})
        self.assertEqual((r.returncode, r.stderr), (0, ""))

    def test_env_root_added(self):
        cfg = os.path.join(self.td, "empty2.yaml")
        with open(cfg, "w", encoding="utf-8") as fh:
            fh.write("protected_roots: []\n")
        r = hook("guard_paths.py", {"tool_input": {"file_path": os.path.join(self.prot, "a.txt")}}, {"MM_CONFIG": cfg, "MM_PROTECTED": self.prot})
        self.assertEqual(r.returncode, 2)

    def test_unreadable_config_fails_closed(self):
        cfg = os.path.join(self.td, "broken.yaml")
        with open(cfg, "w", encoding="utf-8") as fh:  # unreadable for both readers (PyYAML and the built-in one)
            fh.write('protected_roots: ["D:\\bad\\path"]\nthis is not yaml: [\n')
        env = {"MM_CONFIG": cfg, "MM_PROTECTED": ""}
        r = hook("guard_paths.py", {"tool_input": {"file_path": os.path.join(self.td, "elsewhere.txt")}}, env)
        self.assertEqual(r.returncode, 2)
        self.assertIn("config\\paths.yaml cannot be read", r.stderr)
        r = hook("guard_paths.py", {"tool_input": {"file_path": cfg}}, env)  # fixing the config itself is allowed
        self.assertEqual((r.returncode, r.stderr), (0, ""))
        r = hook("guard_paths.py", {"tool_input": {"command": "rm -rf somewhere"}, "cwd": self.td}, env)
        self.assertEqual(r.returncode, 2)
        r = hook("guard_paths.py", {"tool_input": {"command": "cat a.txt | grep x"}, "cwd": self.td}, env)
        self.assertEqual(r.returncode, 0)
        r = hook("guard_paths.py", {"tool_input": {"command": "cat a.txt > b.txt"}, "cwd": self.td}, env)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(hook("guard_paths.py", "{not json", env).returncode, 2)

    def test_missing_config_file_is_quiet(self):
        env = {"MM_CONFIG": os.path.join(self.td, "does-not-exist.yaml"), "MM_PROTECTED": ""}
        r = hook("guard_paths.py", {"tool_input": {"file_path": os.path.join(self.td, "a.txt")}}, env)
        self.assertEqual((r.returncode, r.stderr), (0, ""))

    def test_unparsable_json(self):
        r = hook("guard_paths.py", "{not json", self.env)
        self.assertEqual(r.returncode, 1)
        sys.path.insert(0, HOOKS)
        import guard_paths  # the raw scan compares the canonical (long, case-folded) form of the root
        r = hook("guard_paths.py", "{bad " + guard_paths.long_path(os.path.realpath(self.prot)) + " > x", self.env)
        self.assertEqual(r.returncode, 2)


class SessionStartTests(unittest.TestCase):
    def test_prints_index(self):
        td = tempfile.mkdtemp(prefix="mm_less_")
        with open(os.path.join(td, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("# Lessons index\n\n- `lessons/a.md` - A\n")
        r = hook("session_start.py", {"hook_event_name": "SessionStart", "source": "startup"}, {"MM_LESSONS": td})
        self.assertEqual(r.returncode, 0)
        self.assertIn("lessons/a.md", r.stdout)
        self.assertIn("No AI ever starts", r.stdout)

    def test_fallback_and_missing_folder(self):
        td = tempfile.mkdtemp(prefix="mm_less_")
        with open(os.path.join(td, "2026-01-01-x.md"), "w", encoding="utf-8") as fh:
            fh.write("# Title X\n\n| What happened | Root cause | Rule now |\n|---|---|---|\n| a | b | always check c |\n")
        r = hook("session_start.py", {}, {"MM_LESSONS": td})
        self.assertIn("Title X", r.stdout)
        self.assertIn("rule: always check c", r.stdout)
        r = hook("session_start.py", "garbage", {"MM_LESSONS": os.path.join(td, "nope")})
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_repo_lessons_default(self):
        r = hook("session_start.py", {"hook_event_name": "SessionStart"}, {"MM_LESSONS": ""})
        self.assertEqual(r.returncode, 0)


class LogRunTests(unittest.TestCase):
    def test_appends_json_line(self):
        log = os.path.join(tempfile.mkdtemp(prefix="mm_log_"), "sub", "runs.log")
        for _ in range(2):
            r = hook("log_run.py", {"hook_event_name": "SubagentStop", "agent_type": "print-qa", "session_id": "s1"}, {"MM_RUN_LOG": log})
            self.assertEqual(r.returncode, 0)
        r = hook("log_run.py", "not json", {"MM_RUN_LOG": log})
        self.assertEqual(r.returncode, 0)
        with open(log, encoding="utf-8") as fh:
            lines = [json.loads(x) for x in fh]
        self.assertEqual(len(lines), 3)
        self.assertEqual(lines[0]["agent_type"], "print-qa")


if __name__ == "__main__":
    unittest.main()
