r"""test_ollama_check.py - unit tests for tools\ollama_check.py.

A fake Ollama server on 127.0.0.1 (standard-library http.server in a thread) answers /api/version, /api/tags,
/api/show, /api/ps and /v1/messages. No real Ollama, no model and no internet is needed.
Run: .venv\Scripts\python.exe -I -B -m unittest discover -s tools\tests -p "test_ollama_check.py" -v
"""
from __future__ import annotations

import io
import json
import os
import sys
import threading
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import ollama_check as oc  # noqa: E402

STATE: dict = {}


class FakeOllama(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep test output quiet
        pass

    def reply(self, status: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path in STATE.get("slow", ()):
            time.sleep(1.5)
        if self.path == "/api/version":
            if STATE.get("redirect"):
                self.send_response(302)
                self.send_header("Location", "http://198.51.100.7/api/version")
                self.end_headers()
                return
            self.reply(200, {"version": "0.40.11"})
        elif self.path == "/api/tags":
            self.reply(200, {"models": [{"name": n} for n in STATE["installed"]]})
        elif self.path == "/api/ps":
            if STATE.get("ps_list"):
                raw = b"[]"
                self.send_response(200)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(raw)
                return
            self.reply(200, {"models": STATE["loaded"]})
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/show":
            if body.get("model") in STATE["caps"]:
                self.reply(200, {"capabilities": STATE["caps"][body["model"]]})
            else:
                self.reply(404, {"error": "model not found"})
        elif self.path == "/v1/messages":
            STATE["messages_headers"] = dict(self.headers)
            if STATE.get("messages_ok", True):
                self.reply(200, {"id": "msg_1", "type": "message", "content": [{"type": "text", "text": "."}]})
            else:
                self.reply(500, {"error": {"message": "boom"}})
        else:
            self.reply(404, {"error": "not found"})


class OllamaCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllama)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        STATE.clear()
        STATE.update({
            "installed": ["qwen3.8:27b", "embeddinggemma-2:latest"],
            "caps": {"qwen3.8:27b": ["completion", "vision", "tools", "thinking"],
                     "embeddinggemma-2": ["embedding"], "glm-5.3:cloud": ["completion", "tools", "thinking"],
                     "gpt-oss:120b-cloud": ["completion", "tools"]},
            "loaded": [{"name": "qwen3.8:27b", "context_length": 65536}],
        })

    def levels(self, model, **kw):
        rows, ctx = oc.check(self.base, model, kw.get("context", 64000), kw.get("skip", False), kw.get("timeout", 5.0))
        return {r[0]: r[1] for r in rows}, rows, ctx

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = oc.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_all_ok_and_loaded_context_reported(self):
        lv, rows, ctx = self.levels("qwen3.8:27b")
        self.assertEqual(lv, {"O1": "OK", "O2": "OK", "O3": "OK", "O4": "OK", "O5": "OK"})
        self.assertEqual(oc.verdict(rows), "OK")
        self.assertEqual(ctx, 65536)

    def test_64000_context_passes_default(self):
        STATE["loaded"] = [{"name": "qwen3.8:27b", "context_length": 64000}]
        lv, _, ctx = self.levels("qwen3.8:27b", skip=True)
        self.assertEqual(lv["O4"], "OK")
        self.assertEqual(ctx, 64000)

    def test_messages_request_carries_anthropic_headers(self):
        self.levels("qwen3.8:27b")
        h = {k.lower(): v for k, v in STATE["messages_headers"].items()}
        self.assertEqual(h.get("anthropic-version"), "2023-06-01")
        self.assertEqual(h.get("x-api-key"), "ollama")

    def test_missing_model_fails_with_pull_hint(self):
        lv, rows, _ = self.levels("qwen3.5:9b")
        self.assertEqual(lv["O2"], "FAIL")
        self.assertIn("ollama pull qwen3.5:9b", rows[-1][2])
        self.assertEqual(oc.verdict(rows), "FAIL")

    def test_latest_tag_matches_bare_name(self):
        lv, _, _ = self.levels("embeddinggemma-2", skip=True)
        self.assertEqual(lv["O2"], "OK")

    def test_model_without_tools_fails(self):
        lv, _, _ = self.levels("embeddinggemma-2", skip=True)
        self.assertEqual(lv["O3"], "FAIL")

    def test_small_context_fails(self):
        STATE["loaded"] = [{"name": "qwen3.8:27b", "context_length": 32768}]
        lv, rows, _ = self.levels("qwen3.8:27b", skip=True)
        self.assertEqual(lv["O4"], "FAIL")
        self.assertIn("Context length", dict((r[0], r[2]) for r in rows)["O4"])

    def test_not_loaded_warns(self):
        STATE["loaded"] = []
        lv, rows, ctx = self.levels("qwen3.8:27b", skip=True)
        self.assertEqual(lv["O4"], "WARN")
        self.assertEqual(oc.verdict(rows), "WARN")
        self.assertIsNone(ctx)

    def test_cloud_model_names(self):
        self.assertTrue(oc.is_cloud("glm-5.3:cloud"))
        self.assertTrue(oc.is_cloud("gpt-oss:120b-cloud"))
        self.assertFalse(oc.is_cloud("qwen3.8:27b"))
        self.assertFalse(oc.is_cloud("cloud-model:7b"))
        for m in ("glm-5.3:cloud", "gpt-oss:120b-cloud"):
            lv, rows, _ = self.levels(m, skip=True)
            self.assertEqual(lv["O2"], "WARN")
            self.assertEqual(lv["O4"], "OK")
            self.assertNotEqual(oc.verdict(rows), "FAIL")

    def test_messages_error_fails(self):
        STATE["messages_ok"] = False
        lv, rows, _ = self.levels("qwen3.8:27b")
        self.assertEqual(lv["O5"], "FAIL")
        self.assertIn("500", dict((r[0], r[2]) for r in rows)["O5"])

    def test_no_server_fails(self):
        rows, _ = oc.check("http://127.0.0.1:1", "qwen3.8:27b", 64000, True, 2.0)
        self.assertEqual(rows[0][:2], ("O1", "FAIL"))

    def test_timeout_on_later_call_is_reported_not_raised(self):
        STATE["slow"] = ("/api/ps",)
        lv, rows, _ = self.levels("qwen3.8:27b", skip=True, timeout=0.5)
        self.assertEqual(lv["O4"], "WARN")

    def test_redirect_is_not_followed(self):
        STATE["redirect"] = True
        lv, _, _ = self.levels("qwen3.8:27b", skip=True)
        self.assertEqual(lv["O1"], "FAIL")

    def test_proxy_settings_are_ignored(self):
        with mock.patch.dict(os.environ, {"HTTP_PROXY": "http://198.51.100.9:3128", "http_proxy": "http://198.51.100.9:3128",
                                          "NO_PROXY": "", "no_proxy": ""}):
            lv, _, _ = self.levels("qwen3.8:27b", skip=True, timeout=3.0)
        self.assertEqual(lv["O1"], "OK")

    def test_only_local_hosts_allowed(self):
        for ok in ("http://localhost:11434", "http://127.0.0.1:11434/", "http://[::1]:11434"):
            oc.local_url(ok)
        for bad in ("http://192.0.2.5:11434", "https://ollama.com", "http://localhost.evil.example:11434",
                    "file:///etc/passwd", "http://localhost:abc", "http://localhost:11434/api", "http://u:p@localhost:11434"):
            with self.assertRaises(ValueError, msg=bad):
                oc.local_url(bad)

    def test_settings_map_every_alias_and_context(self):
        env = oc.settings("http://localhost:11434", "qwen3.8:27b", 65536, cloud=False)
        for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL",
                  "CLAUDE_CODE_SUBAGENT_MODEL"):
            self.assertEqual(env[k], "qwen3.8:27b")
        self.assertEqual(env["ANTHROPIC_AUTH_TOKEN"], "ollama")
        self.assertEqual(env["ANTHROPIC_API_KEY"], "")
        self.assertEqual(env["CLAUDE_CODE_MAX_CONTEXT_TOKENS"], "65536")
        self.assertNotIn("CLAUDE_CODE_MAX_CONTEXT_TOKENS", oc.settings("http://localhost:11434", "glm-5.3:cloud", 65536, True))

    def test_printed_keys_are_valid_json_inside_braces(self):
        code, out, _ = self.run_main("--model", "qwen3.8:27b", "--url", self.base)
        self.assertEqual(code, oc.EXIT_OK)
        block = out.split("if it has none:\n", 1)[1].split("\n\nOr,", 1)[0]
        parsed = json.loads("{" + block + "}")
        names = {e["name"]: e["value"] for e in parsed["claudeCode.environmentVariables"]}
        self.assertTrue(parsed["claudeCode.disableLoginPrompt"])
        self.assertEqual(names["CLAUDE_CODE_MAX_CONTEXT_TOKENS"], "65536")  # the loaded window, not the minimum
        self.assertIn("claude --model qwen3.8:27b", out)

    def test_json_list_answer_is_handled(self):
        STATE["ps_list"] = True
        lv, _, _ = self.levels("qwen3.8:27b", skip=True)
        self.assertEqual(lv["O4"], "WARN")

    def test_usage_error_exits_1_not_2(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                oc.main([])
        self.assertEqual(cm.exception.code, oc.EXIT_ARGS)

    def test_exit_codes(self):
        self.assertEqual(self.run_main("--model", "qwen3.8:27b", "--url", self.base)[0], oc.EXIT_OK)
        code, out, _ = self.run_main("--model", "qwen3.5:9b", "--url", self.base, "--json")
        self.assertEqual(code, oc.EXIT_FAIL)
        self.assertEqual(json.loads(out)["verdict"], "FAIL")
        code, _, err = self.run_main("--model", "qwen3.8:27b", "--url", "http://198.51.100.2:11434")
        self.assertEqual(code, oc.EXIT_ARGS)
        self.assertIn("refusing", err)


if __name__ == "__main__":
    unittest.main()
