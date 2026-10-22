r"""Tests for mm_config.py, resolve_profile.py, slice_cli.py (guards and lock only; Bambu Studio is never run),
check_note.py, check_skill.py and build_indexes.py. Synthetic inputs only, written to temp folders.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p test_config_and_cli.py -v
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
REPO = os.path.dirname(TOOLS)
PY = sys.executable

import mm_config  # noqa: E402


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path: str, text: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def run_tool(script: str, *args, env_extra: dict | None = None, stdin: str | None = None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run([PY, "-I", "-B", os.path.join(TOOLS, script), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env, input=stdin if stdin is not None else "", timeout=300)


class MMConfigTests(unittest.TestCase):
    def setUp(self):
        # forward slashes: a mkdtemp path has backslashes, which YAML double quotes would turn into escapes
        self.td = pathlib.Path(tempfile.mkdtemp(prefix="mm_cfg_")).as_posix()

    def cfg(self, text: str) -> dict:
        p = write(os.path.join(self.td, "c.yaml"), text)
        return {"MM_CONFIG": p}

    def test_repo_root_is_parent_of_tools(self):
        self.assertEqual(str(mm_config.repo_root()), REPO)

    def test_example_file_parses_with_both_readers(self):
        text = read(os.path.join(REPO, "config", "paths.example.yaml"))
        mini = mm_config._mini_yaml(text)
        self.assertEqual(mini["slice_workdir"], "work/slice")
        self.assertEqual(mini["allowed_roots"], ["."])
        self.assertEqual(mini["protected_roots"], [])
        self.assertEqual(mini["blender_exe"], "")
        self.assertEqual(set(mini), set(mm_config.DEFAULTS))
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not installed: only the built-in reader was checked")
        self.assertEqual(mm_config._parse(text), {k: (v if v is not None else "") for k, v in mini.items()})

    def test_relative_and_absolute_paths(self):
        with mock.patch.dict(os.environ, self.cfg(f'slice_workdir: "work/x"\nblender_exe: "{self.td}/b.exe"\n'
                                                  f'allowed_roots: [".", "{self.td}"]\nprotected_roots:\n  - "{self.td}/p"\n')):
            self.assertEqual(mm_config.path("slice_workdir"), mm_config.repo_root() / "work" / "x")
            self.assertEqual(str(mm_config.path("blender_exe")).replace("\\", "/"), f"{self.td}/b.exe".replace("\\", "/"))
            self.assertEqual(len(mm_config.path_list("allowed_roots")), 2)
            self.assertEqual(mm_config.path_list("protected_roots")[0].name, "p")

    def test_missing_key_error_names_paths_yaml(self):
        with mock.patch.dict(os.environ, self.cfg('blender_exe: ""\n')):
            self.assertIsNone(mm_config.optional_path("blender_exe"))
            with self.assertRaises(mm_config.MMConfigError) as cm:
                mm_config.path("blender_exe")
            self.assertIn("config\\paths.yaml", str(cm.exception))

    def test_missing_file_uses_defaults(self):
        with mock.patch.dict(os.environ, {"MM_CONFIG": os.path.join(self.td, "nope.yaml")}):
            c = mm_config.load()
            self.assertEqual(c["slice_workdir"], "work/slice")
            self.assertIn("defaults", c["_source"])

    def test_profile_roots_order(self):
        with mock.patch.dict(os.environ, {**self.cfg('bambu_studio_exe: "C:/BS/bambu-studio.exe"\nbambu_profiles_dir: ""\n'),
                                          "APPDATA": self.td}):
            roots = [str(r).replace("\\", "/") for r in mm_config.bambu_profile_roots()]
            self.assertTrue(roots[0].endswith("BambuStudio/system"))
            self.assertTrue(roots[1].endswith("BS/resources/profiles"))
        with mock.patch.dict(os.environ, self.cfg(f'bambu_profiles_dir: "{self.td}/own"\n')):
            self.assertEqual([r.name for r in mm_config.bambu_profile_roots()], ["own"])

    def test_bad_line_raises_in_builtin_reader(self):
        with self.assertRaises(mm_config.MMConfigError):
            mm_config._mini_yaml("just text\n")

    def test_double_quoted_backslash_path_gives_plain_message(self):
        # what File Explorer's "Copy as path" pastes; with PyYAML \A is a ScannerError and \b a control character
        for value in ('"E:\\Apps\\Bambu Studio\\bambu-studio.exe"', '"D:\\bambu\\bambu-studio.exe"'):
            with mock.patch.dict(os.environ, self.cfg(f"slice_workdir: work/slice\nbambu_studio_exe: {value}\n")):
                with self.assertRaises(mm_config.MMConfigError) as cm:
                    mm_config.load()
                msg = str(cm.exception)
                self.assertIn("config\\paths.yaml", msg)
                self.assertIn("line 2", msg)
                self.assertIn("forward slashes", msg)
                self.assertIn("single quotes", msg)

    def test_single_quotes_and_forward_slashes_work(self):
        with mock.patch.dict(os.environ, self.cfg("bambu_studio_exe: 'E:\\Apps\\Bambu Studio\\bambu-studio.exe'\n"
                                                  'blender_exe: "E:/Apps/Blender/blender.exe"\n')):
            c = mm_config.load()
            self.assertEqual(c["bambu_studio_exe"], "E:\\Apps\\Bambu Studio\\bambu-studio.exe")
            self.assertEqual(c["blender_exe"], "E:/Apps/Blender/blender.exe")

    def test_control_character_in_value_is_refused(self):
        # a literal TAB inside single quotes reaches the value with both readers; the loader must catch it
        with mock.patch.dict(os.environ, self.cfg("blender_exe: 'E:\tools/blender.exe'\n")):
            with self.assertRaises(mm_config.MMConfigError) as cm:
                mm_config.load()
            self.assertIn("control character", str(cm.exception))

    def test_silent_escapes_in_double_quotes_are_refused(self):
        # with PyYAML "\x41" decodes silently to "A" and "\\" to one backslash; both forms are refused up front
        for value in ('"E:\\x41pps/blender.exe"', '"E:\\u00e9/blender.exe"', '"E:\\\\Apps\\\\blender.exe"'):
            with self.subTest(value=value), mock.patch.dict(os.environ, self.cfg(f"blender_exe: {value}\n")):
                with self.assertRaises(mm_config.MMConfigError) as cm:
                    mm_config.load()
                self.assertIn("double-quoted value contains a backslash", str(cm.exception))
        # a double quote inside a single-quoted value next to a backslash is fine
        with mock.patch.dict(os.environ, self.cfg("blender_exe: 'E:\\Apps\\\"x\"\\blender.exe'\n")):
            self.assertEqual(mm_config.load()["blender_exe"], 'E:\\Apps\\"x"\\blender.exe')

    def test_utf8_bom_is_accepted_and_other_encodings_refused(self):
        p = os.path.join(self.td, "bom.yaml")
        with open(p, "wb") as fh:
            fh.write(b"\xef\xbb\xbfslice_workdir: 'work/bom'\n")
        with mock.patch.dict(os.environ, {"MM_CONFIG": p}):
            self.assertEqual(mm_config.load()["slice_workdir"], "work/bom")
        with open(p, "wb") as fh:
            fh.write("blender_exe: 'E:/Pr\u00f6gramme/blender.exe'\n".encode("cp1252"))
        with mock.patch.dict(os.environ, {"MM_CONFIG": p}):
            with self.assertRaises(mm_config.MMConfigError) as cm:
                mm_config.load()
            self.assertIn("as UTF-8", str(cm.exception))
            self.assertIn("config\\paths.yaml", str(cm.exception))

    def test_unclosed_list_refused_by_builtin_reader(self):
        with self.assertRaises(mm_config.MMConfigError):
            mm_config._mini_yaml("protected_roots: [\n")

    def test_values_must_be_text_or_list_of_text(self):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not installed: the built-in reader reads every value as text")
        for text in ("slice_workdir: 5\n", "blender_exe: true\n", "allowed_roots: [1, 2]\n",
                     "protected_roots: {a: b}\n"):
            with self.subTest(text=text), mock.patch.dict(os.environ, self.cfg(text)):
                with self.assertRaises(mm_config.MMConfigError) as cm:
                    mm_config.load()
                self.assertIn("must be text or a list of text", str(cm.exception))

    def test_cli_reports_bad_config_and_space_warning(self):
        bad = self.cfg('bambu_studio_exe: "E:\\Apps\\bambu-studio.exe"\n')
        r = run_tool("mm_config.py", env_extra=bad)
        self.assertEqual(r.returncode, 2)
        self.assertIn("config\\paths.yaml cannot be read", r.stderr)
        spaced = self.cfg('slice_workdir: "work/my slices"\n')
        r = run_tool("mm_config.py", env_extra=spaced)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("contains a space", r.stderr)


class ResolveProfileTests(unittest.TestCase):
    """A synthetic three-level process chain with an include template."""

    @classmethod
    def setUpClass(cls):
        cls.root = tempfile.mkdtemp(prefix="mm_prof_")
        d = os.path.join(cls.root, "process")
        write(os.path.join(d, "common.json"), json.dumps({"name": "common", "max_bridge_length": "0", "wall_loops": "2", "x": "base"}))
        write(os.path.join(d, "mid.json"), json.dumps({"name": "mid", "inherits": "common", "wall_loops": "3"}))
        write(os.path.join(d, "tmpl.json"), json.dumps({"name": "tmpl", "x": "from-include", "y": "inc"}))
        write(os.path.join(d, "leaf.json"), json.dumps({"name": "Test Leaf", "inherits": "mid", "include": ["tmpl"], "y": "leaf"}))
        write(os.path.join(d, "nested.json"), json.dumps({"name": "nested", "inherits": "common"}))
        write(os.path.join(d, "bad.json"), json.dumps({"name": "Bad Leaf", "include": "nested"}))

    def run_rp(self, *args):
        return run_tool("resolve_profile.py", "--root", self.root, *args)

    def test_merge_order_and_set_in(self):
        r = self.run_rp("--kind", "process", "Test Leaf", "--keys", "max_bridge_length", "wall_loops", "x", "y", "nope", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        p = json.loads(r.stdout)["profiles"]["Test Leaf"]
        self.assertEqual(p["chain"], ["Test Leaf", "include:tmpl", "mid", "common"])
        v = p["values"]
        self.assertEqual(v["max_bridge_length"], {"value": "0", "set_in": "common"})
        self.assertEqual(v["wall_loops"], {"value": "3", "set_in": "mid"})
        self.assertEqual(v["x"], {"value": "from-include", "set_in": "include:tmpl"})   # include beats parents
        self.assertEqual(v["y"], {"value": "leaf", "set_in": "Test Leaf"})               # own keys beat includes
        self.assertEqual(v["nope"], {"value": None, "set_in": None})

    def test_not_found_and_nested_include(self):
        self.assertEqual(self.run_rp("--kind", "process", "Missing").returncode, 1)
        r = self.run_rp("--kind", "process", "Bad Leaf")
        self.assertEqual(r.returncode, 1)
        self.assertIn("nested include not supported", r.stderr)

    def test_list(self):
        r = self.run_rp("--list", "process", "leaf")
        self.assertEqual(r.stdout.split(), ["Bad", "Leaf", "Test", "Leaf"])

    def test_no_root_message(self):
        cfg = write(os.path.join(self.root, "empty.yaml"), 'bambu_studio_exe: ""\nbambu_profiles_dir: ""\n')
        r = run_tool("resolve_profile.py", "--list", "process", "x", env_extra={"MM_CONFIG": cfg, "APPDATA": ""})
        self.assertEqual(r.returncode, 1)
        self.assertIn("config\\paths.yaml", r.stderr)


class SliceCliTests(unittest.TestCase):
    """Only the guards and the lock: the slicer is never launched."""

    def setUp(self):
        import slice_cli
        self.sc = slice_cli
        self.td = tempfile.mkdtemp(prefix="mm_slice_")

    def test_gated_patterns(self):
        self.assertTrue(self.sc.is_gated_sliced(os.path.join(self.td, "projects", "a", "print", "x_SLICED.3mf")))
        self.assertFalse(self.sc.is_gated_sliced(os.path.join(self.td, "work", "x_SLICED.3mf")))

    def test_guard_refuses_existing_gated_output(self):
        wd = os.path.join(self.td, "projects", "p", "print")
        write(os.path.join(wd, "out.3mf"), "x")
        reason = self.sc.gated_overwrite(wd)
        self.assertIsNotNone(reason)
        self.assertIn("--allow-overwrite", reason)
        r = run_tool("slice_cli.py", os.path.join(self.td, "in.3mf"), "--outdir", wd, "--exe", os.path.join(self.td, "none.exe"))
        self.assertEqual(r.returncode, 3)
        self.assertIsNone(self.sc.gated_overwrite(os.path.join(self.td, "work")))

    def test_missing_exe_names_config(self):
        r = run_tool("slice_cli.py", os.path.join(self.td, "in.3mf"), "--outdir", os.path.join(self.td, "w"),
                     "--exe", os.path.join(self.td, "none.exe"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("bambu_studio_exe", r.stderr)

    def test_lock_live_dead_and_release(self):
        wd = os.path.join(self.td, "w2")
        os.makedirs(wd)
        lock, note = self.sc.acquire_lock(wd, "a.3mf")
        self.assertIsNotNone(lock)
        self.assertEqual(note, "")
        held, msg = self.sc.acquire_lock(wd, "b.3mf")        # same live PID holds it
        self.assertIsNone(held)
        self.assertIn("--outdir", msg)
        self.sc.release_lock(lock)
        self.assertFalse(os.path.exists(lock))
        write(os.path.join(wd, self.sc.LOCK_NAME), json.dumps({"pid": 999999, "time": 1.0, "input": "old"}))
        lock2, note2 = self.sc.acquire_lock(wd, "c.3mf")      # dead PID: taken over
        self.assertIsNotNone(lock2)
        self.assertIn("stale lock", note2)
        self.sc.release_lock(lock2)

    def test_never_asks_the_slicer_to_print(self):
        src = read(os.path.join(TOOLS, "slice_cli.py"))
        for word in ("--send", "--upload", "--print", "start_print"):
            self.assertNotIn(word, src)


class CheckNoteTests(unittest.TestCase):
    GOOD = ("# Note\n\nApplies to: H2C · Bambu Studio 02.08\nVerified: 2026-01-02\n\n## Facts\n"
            "- A fact (https://wiki.bambulab.com/en/x)\n- Measured on a coupon: measured\n- HDT 55 C at 0.45 MPa (https://example.org/tds)\n\n"
            "## In practice\n- free text\n\nSources:\n- https://wiki.bambulab.com/en/x\n")

    def setUp(self):
        self.td = tempfile.mkdtemp(prefix="mm_note_")

    def test_good_and_bad_notes(self):
        good = write(os.path.join(self.td, "good.md"), self.GOOD)
        bad = write(os.path.join(self.td, "bad.md"), "# Bad\n\n## Facts\n- no source here\n- HDT 55 C\n")
        r = run_tool("check_note.py", good)
        self.assertEqual(r.returncode, 0, r.stdout)
        r = run_tool("check_note.py", bad)
        self.assertEqual(r.returncode, 2)
        for msg in ("Applies to", "Verified", "Sources", "fact bullet without", "HDT without load"):
            self.assertIn(msg, r.stdout)

    def test_hook_mode_scope(self):
        outside = json.dumps({"tool_input": {"file_path": os.path.join(self.td, "bad.md")}})
        write(os.path.join(self.td, "bad.md"), "# x\n")
        self.assertEqual(run_tool("check_note.py", stdin=outside).returncode, 0)          # outside the repo: no-op
        index = json.dumps({"tool_input": {"file_path": os.path.join(REPO, "knowledge", "02-bambu-studio", "index.md")}})
        self.assertEqual(run_tool("check_note.py", stdin=index).returncode, 0)            # index files are skipped
        self.assertEqual(run_tool("check_note.py", stdin="not json").returncode, 0)

    def test_hook_mode_blocks_bad_knowledge_note(self):
        bad = os.path.join(REPO, "knowledge", "_selftest_bad_note.md")   # temporary, removed below
        with open(bad, "w", encoding="utf-8") as f:
            f.write("# Bad note\nApplies to: both\nVerified: YYYY-MM-DD\n\n## Facts\n- no source here\n")
        try:
            r = run_tool("check_note.py", stdin=json.dumps({"tool_input": {"file_path": bad}}))
            self.assertEqual(r.returncode, 2)      # placeholder date and missing Sources must block
            self.assertIn("Verified", r.stderr)
        finally:
            os.remove(bad)

    def test_hook_mode_skips_gear_records(self):
        tmpl = os.path.join(REPO, "knowledge", "00-gear-inventory", "current-load.md")
        r = run_tool("check_note.py", stdin=json.dumps({"tool_input": {"file_path": tmpl}}))
        self.assertEqual(r.returncode, 0)          # your own load record is not a cited note

    def test_label_backref_note_link_and_hdt_rules(self):
        import check_note
        head = "# N\nApplies to: both\nVerified: 2026-01-02\n\n## Facts\n"
        tail = "\nSources:\n- https://example.org/a\n"
        cases = {
            "- Unsourced claim. Not verified (no public source).\n": True,          # labelled
            "- Unsourced claim.\n": False,
            "- A (https://example.org/a)\n- B - same source p. 3\n": True,          # back-reference under a URL
            "- B - same source p. 3\n": False,                                     # back-reference with nothing above
            "### One\n- A (https://example.org/a)\n### Two\n- B - same TDS\n": False,  # URL is in another subsection
            "- See [other.md](other.md) for the details.\n": True,                  # pointer to another checked note
            "- See [gone.md](gone.md#x) for the details.\n": False,                 # link target does not exist
            "- Set Quality > Seam > Position (label not verified).\n": False,      # UI-label tag is not a source label
            "- Set Quality > Seam (label not verified); value not verified.\n": True,
            "- HDT and Vicat N/A (too soft) - https://example.org/t\n": True,
            "- HDT 70 / 75 C - https://example.org/t\n": False,                    # pair without its loads
            "- HDT 173 / 215 °C (1.8 / 0.45 MPa) - https://example.org/t\n": True,
            "- HDT 68 °C; tensile 50 MPa; elongation 4 % at a long distance of text; HDT 70 °C - https://example.org/t\n": False,
            "- HDT 68 °C at both loads, see the TDS table on page two for the 0.45 and 1.80 MPa rows - https://example.org/t\n": False,
            "- Tg 80 °C, Vicat and HDT N/A - https://example.org/t; tensile 30 MPa\n": True,
        }
        write(os.path.join(self.td, "other.md"), "# other\n")
        for body, ok in cases.items():
            p = write(os.path.join(self.td, "case.md"), head + body + tail)
            self.assertEqual(check_note.check(pathlib.Path(p)) == [], ok, body)


class ShippedNotesTests(unittest.TestCase):
    """Every shipped knowledge note passes check_note (index.md, README.md and 00-gear-inventory are records, not notes)."""

    def test_every_shipped_note_passes(self):
        import check_note
        root = pathlib.Path(REPO) / "knowledge"
        notes = [p for p in sorted(root.rglob("*.md"))
                 if p.name.lower() not in ("index.md", "readme.md") and "00-gear-inventory" not in p.parts]
        self.assertTrue(notes, "no knowledge notes found")
        failures = {str(p.relative_to(root)): probs for p in notes if (probs := check_note.check(p))}
        self.assertEqual(failures, {}, f"{len(failures)} of {len(notes)} notes fail check_note")


class CheckSkillTests(unittest.TestCase):
    BODY = ("\n## Overview\nx\n## When to use\nx\n## Common rationalizations\n| Rationalization | Reality |\n|---|---|\n| a | b |\n"
            "## Red flags\nx\n## Verification\n- [ ] done\n")

    def setUp(self):
        self.td = tempfile.mkdtemp(prefix="mm_skill_")

    def test_skill_pass_and_fail(self):
        good = write(os.path.join(self.td, "skills", "good-one", "SKILL.md"),
                     "---\nname: good-one\ndescription: Use when testing.\n---\n" + self.BODY)
        bad = write(os.path.join(self.td, "skills", "bad", "SKILL.md"), "---\nname: Other\ndescription: does things\nfoo: 1\n---\nbody\n")
        self.assertEqual(run_tool("check_skill.py", good).returncode, 0)
        r = run_tool("check_skill.py", bad)
        self.assertEqual(r.returncode, 2)
        for code in ("S1", "S2", "S3", "S4"):
            self.assertIn(code, r.stdout)

    def test_agent_rules(self):
        good = write(os.path.join(self.td, "agents", "my-agent.md"),
                     "---\nname: my-agent\ndescription: Checks things. Use it often.\nmodel: sonnet\n---\n" + self.BODY)
        bad = write(os.path.join(self.td, "agents", "other.md"), "---\nname: other\ndescription: One. Two. Three.\n---\nbody\n")
        self.assertEqual(run_tool("check_skill.py", good).returncode, 0)
        r = run_tool("check_skill.py", bad)
        self.assertEqual(r.returncode, 2)
        self.assertIn("model: missing", r.stdout)
        self.assertIn("A3", r.stdout)

    def test_help_and_shipped_agents_and_skills(self):
        r = run_tool("check_skill.py", "--help")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("usage: check_skill.py", r.stdout)
        r = run_tool("check_skill.py", os.path.join(REPO, ".claude", "agents"), os.path.join(REPO, ".claude", "skills"))
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])

    def test_license_text_kept(self):
        src = read(os.path.join(TOOLS, "check_skill.py"))
        self.assertIn("addyosmani/agent-skills", src)
        self.assertIn("Permission is hereby granted, free of charge", src)


class BuildIndexesTests(unittest.TestCase):
    def test_indexes_written_relative_and_idempotent(self):
        root = tempfile.mkdtemp(prefix="mm_idx_")
        write(os.path.join(root, "knowledge", "01-printers", "index.md"), "# Printers\n")
        write(os.path.join(root, "knowledge", "01-printers", "a-note.md"), "# A\n")
        os.makedirs(os.path.join(root, "knowledge", "02-empty"))
        write(os.path.join(root, "lessons", "2026-01-01-thing.md"), "# A lesson title\n")
        for _ in range(2):
            r = run_tool("build_indexes.py", "--root", root)
            self.assertEqual(r.returncode, 0, r.stderr)
        k = read(os.path.join(root, "knowledge", "INDEX.md"))
        lz = read(os.path.join(root, "lessons", "INDEX.md"))
        self.assertIn("- `knowledge/01-printers/` - 1 note(s): a-note.md", k)
        self.assertIn("- `knowledge/02-empty/` - 0 note(s) (empty)", k)
        self.assertIn("- `lessons/2026-01-01-thing.md` - A lesson title", lz)
        self.assertNotIn(":\\", k + lz)


if __name__ == "__main__":
    unittest.main()
