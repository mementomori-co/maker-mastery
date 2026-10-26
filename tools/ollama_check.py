r"""ollama_check.py - check that the Ollama server on this PC is ready for Ollama mode, then print the settings to paste.

What it does: asks the Ollama server on this PC (http://localhost:11434 by default) five questions and prints one line per
check, the same OK / WARN / FAIL style as the audit tools:
  O1 the server answers, and which version it is (`/api/version`)
  O2 the model you named is installed (`/api/tags`)
  O3 the model can call tools (`/api/show` capabilities); Claude Code needs tool calling
  O4 the loaded model's context window is at least --context tokens (`/api/ps`); Ollama asks for at least 64000 for
     coding tools and agents
  O5 the Anthropic-compatible endpoint that Claude Code uses answers a one-token request (`/v1/messages`)
Then it prints the two VS Code user-settings keys and the PowerShell lines for docs\12-ollama-mode.md section 4, with your
model and the loaded context window filled in.
It only talks to the Ollama server on this PC: any other host is refused, proxies are ignored and redirects are not
followed, so nothing leaves the machine. It changes nothing and needs only the Python standard library. Ollama itself is
not part of this project.

Inputs: --model NAME (for example qwen3.8:27b or glm-5.3:cloud); optional --url, --context, --skip-messages, --timeout,
--json.
Output: the check lines, VERDICT OK / WARN / FAIL, then the settings to paste.
Exit codes: 0 OK or WARN, 2 FAIL (same as check_note.py), 1 bad arguments (for example a non-local --url).
Usage: .venv\Scripts\python.exe -B tools\ollama_check.py --model <name> [--context 64000] [--skip-messages] [--json]
Example: .venv\Scripts\python.exe -B tools\ollama_check.py --model qwen3.8:27b
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

DEFAULT_URL = "http://localhost:11434"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
DEFAULT_CONTEXT = 64000  # https://docs.ollama.com/context-length: "at least 64000 tokens" for agents and coding tools
TESTED_VERSION = "0.40.11"
EXIT_OK, EXIT_ARGS, EXIT_FAIL = 0, 1, 2


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # never follow a redirect to another host
        return None


# No ProxyHandler entries: HTTP(S)_PROXY and Windows proxy settings are ignored, so requests go straight to this PC.
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())


def local_url(url: str) -> str:
    """Return the URL without a trailing slash, or raise ValueError if it is not the Ollama server on this PC."""
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https") or (p.hostname or "") not in LOCAL_HOSTS:
        raise ValueError(f"refusing {url!r}: this tool only talks to the Ollama server on this PC "
                         f"(host must be one of {', '.join(sorted(LOCAL_HOSTS))})")
    try:
        p.port  # noqa: B018 - raises ValueError on a non-numeric or out-of-range port
    except ValueError:
        raise ValueError(f"refusing {url!r}: the port is not a number between 0 and 65535") from None
    if p.path not in ("", "/") or p.query or p.fragment or p.username or p.password:
        raise ValueError(f"refusing {url!r}: give only scheme, host and port, for example {DEFAULT_URL}")
    return url.rstrip("/")


def is_cloud(model: str) -> bool:
    """Ollama Cloud models carry the tag `cloud` or a tag ending in `-cloud` (for example `glm-5.3:cloud`)."""
    tag = model.split(":", 1)[1] if ":" in model else ""
    return tag == "cloud" or tag.endswith("-cloud")


def call(base: str, path: str, body: dict | None = None, timeout: float = 30.0) -> tuple[int, dict]:
    """GET (body None) or POST JSON; -> (HTTP status, parsed JSON or {}). Raises OSError on no answer."""
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if path.startswith("/v1/"):
        headers.update({"x-api-key": "ollama", "anthropic-version": "2023-06-01"})
    req = urllib.request.Request(base + path, data=data, headers=headers, method="GET" if body is None else "POST")
    try:
        with _OPENER.open(req, timeout=timeout) as r:  # noqa: S310 - host checked by local_url
            raw, status = r.read(), r.status
    except urllib.error.HTTPError as e:
        raw, status = e.read(), e.code
    try:
        js = json.loads(raw or b"{}")
    except ValueError:
        js = {}
    return status, js if isinstance(js, dict) else {}


def safe_call(base: str, path: str, body: dict | None, timeout: float) -> tuple[int, dict, str]:
    """call() that never raises: -> (status, json, error text or '')."""
    try:
        st, js = call(base, path, body, timeout)
        return st, js, ""
    except (urllib.error.URLError, OSError) as e:
        return 0, {}, str(getattr(e, "reason", e))


def same_model(a: str, b: str) -> bool:
    """Ollama lists `name:latest` for a pull of `name`."""
    norm = lambda s: s if ":" in s else s + ":latest"  # noqa: E731
    return norm(a) == norm(b)


def check(base: str, model: str, context: int, skip_messages: bool, timeout: float) -> tuple[list[tuple[str, str, str]], int | None]:
    """-> ([(id, level, message)], loaded context length or None). Levels OK / WARN / FAIL."""
    out: list[tuple[str, str, str]] = []
    loaded_ctx: int | None = None
    cloud = is_cloud(model)

    st, ver, err = safe_call(base, "/api/version", None, timeout)
    if err:
        out.append(("O1", "FAIL", f"no Ollama server at {base} ({err}). Start the Ollama app from the Start menu, then run "
                                  "this again."))
        return out, None
    if st != 200 or "version" not in ver:
        out.append(("O1", "FAIL", f"{base}/api/version answered HTTP {st}, not an Ollama version"))
        return out, None
    out.append(("O1", "OK", f"Ollama {ver['version']} answers at {base} (Ollama mode was tested on {TESTED_VERSION})"))

    st, tags, err = safe_call(base, "/api/tags", None, timeout)
    names = [m.get("name", "") for m in tags.get("models", [])]
    if err:
        out.append(("O2", "FAIL", f"/api/tags did not answer ({err})"))
        return out, None
    if any(same_model(n, model) for n in names):
        out.append(("O2", "OK", f"model {model} is installed"))
    elif cloud:
        out.append(("O2", "WARN", f"cloud model {model} is not in the local list yet; cloud models need no download, but "
                                  "you must be signed in to Ollama (ollama signin)"))
    else:
        out.append(("O2", "FAIL", f"model {model} is not installed. Run: ollama pull {model}"))
        return out, None

    st, show, err = safe_call(base, "/api/show", {"model": model}, timeout)
    caps = show.get("capabilities")
    if err or st != 200:
        out.append(("O3", "WARN", f"could not read the model card ({err or f'HTTP {st}'}); tool support not checked"))
    elif caps is None:
        out.append(("O3", "WARN", "this Ollama version does not report capabilities; tool support not checked"))
    elif "tools" in caps:
        out.append(("O3", "OK", f"{model} supports tool calling (capabilities: {', '.join(caps)})"))
    else:
        out.append(("O3", "FAIL", f"{model} does not support tool calling (capabilities: {', '.join(caps)}); Claude Code "
                                  "cannot read files or run tools with it. Pick a model tagged 'tools' on "
                                  "https://ollama.com/search?c=tools"))

    if skip_messages:
        out.append(("O5", "WARN", "skipped (--skip-messages): the /v1/messages endpoint was not tried"))
    else:
        body = {"model": model, "max_tokens": 1, "messages": [{"role": "user", "content": "."}]}
        st, msg, err = safe_call(base, "/v1/messages", body, max(timeout, 600.0))
        if err:
            out.append(("O5", "FAIL", f"/v1/messages did not answer ({err})"))
        elif st == 200 and msg.get("type") == "message":
            out.append(("O5", "OK", "the Anthropic-compatible endpoint /v1/messages answered (this is what Claude Code "
                                    "calls)"))
        else:
            e = msg.get("error")
            e = e.get("message") if isinstance(e, dict) else e
            out.append(("O5", "FAIL", f"/v1/messages answered HTTP {st}{': ' + str(e) if e else ''}"))
    if cloud:
        out.append(("O4", "OK", "cloud models run at their maximum context length by default"))
    else:
        st, ps, err = safe_call(base, "/api/ps", None, timeout)
        loaded = [m for m in ps.get("models", []) if same_model(m.get("name", ""), model)]
        if err:
            out.append(("O4", "WARN", f"/api/ps did not answer ({err}); context window not checked"))
        elif not loaded:
            out.append(("O4", "WARN", f"{model} is not loaded, so its context window is unknown. Run "
                                      f"'ollama run {model} hi' once, then run this check again"))
        else:
            ctx = loaded[0].get("context_length")
            if not isinstance(ctx, int):
                out.append(("O4", "WARN", "this Ollama version does not report the loaded context length"))
            elif ctx >= context:
                loaded_ctx = ctx
                out.append(("O4", "OK", f"loaded with a {ctx}-token context window (need {context}+)"))
            else:
                loaded_ctx = ctx
                out.append(("O4", "FAIL", f"loaded with only {ctx} tokens of context (need {context}+). In the Ollama "
                                          "app: Settings > Context length, then quit and restart Ollama"))

    out.sort(key=lambda r: r[0])  # O5 runs before O4 so the model is loaded when its context is read
    return out, loaded_ctx


def verdict(rows: list[tuple[str, str, str]]) -> str:
    levels = {r[1] for r in rows}
    return "FAIL" if "FAIL" in levels else "WARN" if "WARN" in levels else "OK"


def settings(base: str, model: str, context: int, cloud: bool) -> dict[str, str]:
    """The environment for Claude Code in Ollama mode (docs\\12-ollama-mode.md, section 4)."""
    env = {
        "ANTHROPIC_BASE_URL": base,
        "ANTHROPIC_AUTH_TOKEN": "ollama",
        "ANTHROPIC_API_KEY": "",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": model,
        "ANTHROPIC_DEFAULT_SONNET_MODEL": model,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": model,
        "CLAUDE_CODE_SUBAGENT_MODEL": model,
    }
    if not cloud:
        env["CLAUDE_CODE_MAX_CONTEXT_TOKENS"] = str(context)
    return env


def render_settings(env: dict[str, str], model: str) -> str:
    items = [{"name": k, "value": v} for k, v in env.items()]
    lines = ['"claudeCode.disableLoginPrompt": true,', '"claudeCode.environmentVariables": [']
    lines += [f"  {json.dumps(it)}{',' if i < len(items) - 1 else ''}" for i, it in enumerate(items)]
    lines.append("]")
    ps = "\n".join(f'$env:{k} = "{v}"' for k, v in env.items())
    return ("VS Code user settings (Ctrl+Shift+P > Preferences: Open User Settings (JSON)): paste these two keys inside the\n"
            "outer { }, and put a comma at the end of the line above them if it has none:\n"
            + "\n".join(lines)
            + f"\n\nOr, for one VS Code terminal, paste these lines, then run: claude --model {model}\n" + ps)


class _Parser(argparse.ArgumentParser):
    def error(self, message):  # usage errors exit 1, so exit 2 always means a FAIL verdict
        self.print_usage(sys.stderr)
        self.exit(EXIT_ARGS, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    ap = _Parser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="Ollama model name, for example qwen3.8:27b or glm-5.3:cloud")
    ap.add_argument("--url", default=DEFAULT_URL, help=f"Ollama server on this PC (default {DEFAULT_URL})")
    ap.add_argument("--context", type=int, default=DEFAULT_CONTEXT,
                    help=f"minimum context window in tokens (default {DEFAULT_CONTEXT})")
    ap.add_argument("--skip-messages", action="store_true", help="do not send the one-token /v1/messages test")
    ap.add_argument("--timeout", type=float, default=30.0, help="seconds per request (the /v1/messages test allows 600)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    a = ap.parse_args(argv)
    try:
        base = local_url(a.url)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return EXIT_ARGS
    rows, loaded_ctx = check(base, a.model, a.context, a.skip_messages, a.timeout)
    v = verdict(rows)
    cloud = is_cloud(a.model)
    env = settings(base, a.model, loaded_ctx if loaded_ctx and loaded_ctx >= a.context else a.context, cloud)
    if a.json:
        print(json.dumps({"url": base, "model": a.model, "checks": [dict(zip(("id", "level", "message"), r)) for r in rows],
                          "verdict": v, "loaded_context": loaded_ctx, "env": env}, indent=2))
    else:
        print(f"Ollama mode check: {a.model} at {base}")
        for cid, level, msg in rows:
            print(f"  [{level}] {cid}: {msg}")
        print(f"VERDICT: {v}")
        if v != "FAIL":
            print()
            print(render_settings(env, a.model))
    return EXIT_FAIL if v == "FAIL" else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
