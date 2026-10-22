r"""Tests for tools\mcp\mm_audit_server.py: starts the server over stdio with the mcp client and checks the three tools end
to end on a synthetic 3MF and G-code (no Bambu Studio needed: resolve_profile reads a synthetic profile tree).
Allowed and protected roots come from a temporary config passed as MM_CONFIG. Skipped when the mcp package is missing.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p test_mcp_audit_server.py -v
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
import zipfile

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.dirname(os.path.abspath(__file__))
for p in (TOOLS, TESTS):
    if p not in sys.path:
        sys.path.insert(0, p)
SERVER = os.path.join(TOOLS, "mcp", "mm_audit_server.py")

try:
    import anyio
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    HAVE_MCP = True
except ImportError:
    HAVE_MCP = False

GCODE = """; HEADER_BLOCK_START
; HEADER_BLOCK_END
; CHANGE_LAYER
; Z_HEIGHT: 0.2
; LAYER_HEIGHT: 0.2
; start printing object, unique label id: 1
; FEATURE: Outer wall
G1 X50 Y50 F3000
G1 X60 Y50 E1
G1 X60 Y60 E1
G1 X50 Y60 E1
G1 X50 Y50 E1
; stop printing object, unique label id: 1
; FEATURE: Prime tower
G1 X100 Y100
G1 X120 Y100 E1
G1 X120 Y120 E1
G1 X100 Y120 E1
G1 X100 Y100 E1
"""


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def text_of(res) -> str:
    return " ".join(getattr(c, "text", "") for c in res.content)


@unittest.skipUnless(HAVE_MCP, "the mcp package is not installed: pip install -r requirements.txt into .venv")
class MCPServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import fixtures_3mf as fx   # isolates the audit from the machine (MM_CONFIG, APPDATA)
        cls.fx = fx
        cls.root = tempfile.mkdtemp(prefix="mm_mcp_")
        cls.allowed = os.path.join(cls.root, "allowed")
        cls.prot = os.path.join(cls.root, "allowed", "protected")
        os.makedirs(cls.prot)
        prof = os.path.join(cls.root, "profiles", "BBL", "process")
        os.makedirs(prof)
        with open(os.path.join(prof, "base.json"), "w", encoding="utf-8") as fh:
            json.dump({"name": "Base Proc", "max_bridge_length": "0"}, fh)
        with open(os.path.join(prof, "leaf.json"), "w", encoding="utf-8") as fh:
            json.dump({"name": "Leaf Proc", "inherits": "Base Proc", "layer_height": "0.2"}, fh)
        fwd = lambda s: s.replace("\\", "/")  # noqa: E731
        cls.cfg = os.path.join(cls.root, "paths.yaml")
        with open(cls.cfg, "w", encoding="utf-8") as fh:
            fh.write(f'bambu_studio_exe: "{fwd(cls.root)}/none/bambu-studio.exe"\nbambu_profiles_dir: "{fwd(cls.root)}/profiles"\n'
                     f'allowed_roots: ["{fwd(cls.allowed)}"]\nprotected_roots: ["{fwd(cls.prot)}"]\n')
        src = fx.build(name="mcp_case")
        cls.three = os.path.join(cls.allowed, "part.3mf")
        with open(src, "rb") as a, open(cls.three, "wb") as b:
            b.write(a.read())
        cls.sliced = os.path.join(cls.allowed, "sliced.3mf")
        with zipfile.ZipFile(cls.sliced, "w") as z:
            z.writestr("Metadata/plate_1.gcode", GCODE)
        cls.gdir = os.path.join(cls.allowed, "g")
        os.makedirs(cls.gdir)
        cls.gfile = os.path.join(cls.gdir, "plate_1.gcode")
        with open(cls.gfile, "w", encoding="utf-8") as fh:
            fh.write(GCODE)
        cls.outside = os.path.join(cls.root, "outside.3mf")
        with open(cls.outside, "wb") as fh:
            fh.write(b"x")
        env = dict(os.environ)
        env["MM_CONFIG"] = cls.cfg
        cls.params = StdioServerParameters(command=sys.executable, args=["-B", SERVER], env=env, cwd=cls.root)

    def call_all(self, calls):
        async def go():
            out = {}
            async with Client(self.params) as c:
                out["tools"] = (await c.list_tools()).tools
                for key, name, args in calls:
                    out[key] = await c.call_tool(name, args)
            return out
        return anyio.run(go)

    def test_end_to_end(self):
        before = sha(self.three)
        r = self.call_all([
            ("audit", "audit_3mf", {"path": self.three, "geometry": False}),
            ("outside", "audit_3mf", {"path": self.outside}),
            ("protected", "audit_3mf", {"path": os.path.join(self.prot, "x.3mf")}),
            ("relative", "audit_3mf", {"path": "x.3mf"}),
            ("unc", "audit_3mf", {"path": r"\\localhost\c$\x.3mf"}),
            ("ext", "tower_clearance", {"gcode_dir_or_3mf": os.path.join(self.allowed, "x.json")}),
            ("rp", "resolve_profile", {"kind": "process", "name": "Leaf Proc", "keys": ["max_bridge_length"]}),
            ("rp_opt", "resolve_profile", {"kind": "process", "name": "--root"}),
            ("rp_missing", "resolve_profile", {"kind": "process", "name": "Nope"}),
            ("tc_3mf", "tower_clearance", {"gcode_dir_or_3mf": self.sliced}),
            ("tc_file", "tower_clearance", {"gcode_dir_or_3mf": self.gfile}),
            ("tc_dir", "tower_clearance", {"gcode_dir_or_3mf": self.gdir}),
        ])
        tools = r["tools"]
        self.assertEqual({t.name for t in tools}, {"audit_3mf", "resolve_profile", "tower_clearance"})
        for t in tools:
            a = t.annotations
            self.assertTrue(a.read_only_hint)
            self.assertFalse(a.destructive_hint)
            self.assertFalse(a.open_world_hint)
        sc = r["audit"].structured_content or {}
        self.assertFalse(r["audit"].is_error, text_of(r["audit"]))
        data = sc["data"]
        worst = max({"OK": 0, "WARN": 1, "FAIL": 2}[f["level"]] for f in data["findings"])
        self.assertEqual(sc["exit_code"], worst)
        self.assertIn("C7", {f["check"] for f in data["findings"]})
        self.assertTrue(r["outside"].is_error)
        self.assertIn("allowed roots", text_of(r["outside"]))
        self.assertTrue(r["protected"].is_error)
        self.assertIn("protected root", text_of(r["protected"]))
        self.assertIn("absolute", text_of(r["relative"]))
        self.assertIn("UNC", text_of(r["unc"]))
        self.assertIn("extension", text_of(r["ext"]))
        rp = (r["rp"].structured_content or {})["data"]["profiles"]["Leaf Proc"]
        self.assertEqual(rp["values"]["max_bridge_length"], {"value": "0", "set_in": "Base Proc"})
        self.assertIn("option", text_of(r["rp_opt"]))
        self.assertTrue(r["rp_missing"].is_error)
        self.assertIn("not found", text_of(r["rp_missing"]))
        strip = lambda d: {k: v for k, v in d.items() if k != "file"}  # noqa: E731
        p3 = (r["tc_3mf"].structured_content or {})["data"]
        pf = (r["tc_file"].structured_content or {})["data"]
        pd = (r["tc_dir"].structured_content or {})["data"]
        self.assertEqual(len(p3), 1)
        self.assertEqual(strip(p3[0]), strip(pf[0]))
        self.assertEqual(len(pd), 1)
        self.assertEqual(sha(self.three), before)
        self.assertFalse(os.path.exists(os.path.join(self.allowed, "__pycache__")))

    def test_source_has_no_network_printer_or_write_calls(self):
        src = "".join(read(os.path.join(TOOLS, "mcp", f))
                      for f in ("mm_audit_server.py", "tower_clearance_3mf.py"))
        for b in ("import socket", "import requests", "import urllib", "import http", "httpx", "mqtt", "ftplib",
                  ".write_text(", ".write_bytes(", "os.remove", "shutil."):
            self.assertNotIn(b, src)


if __name__ == "__main__":
    unittest.main()
