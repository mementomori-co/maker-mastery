r"""mm_config.py - the one place every tool reads machine-specific paths from.

What it does: loads config\paths.yaml (your copy) and resolves the paths in it. Every other tool imports this module
instead of hard-coding a drive letter, a user folder or an install path.

Inputs:
  config\paths.yaml          your settings (copy config\paths.example.yaml to start; tools\setup.ps1 does it for you)
  config\paths.example.yaml  used when paths.yaml does not exist yet, so a fresh clone still runs
  MM_CONFIG (environment)    optional: full path of another YAML file to load instead (the unit tests use it)

Outputs (API):
  repo_root() -> pathlib.Path           the repository folder (the parent of tools\)
  load() -> dict                        every key, built-in defaults overlaid with the YAML file
  path(key) -> pathlib.Path             one path key resolved against the repo root; raises MMConfigError naming
                                        config\paths.yaml when the key is missing or empty
  optional_path(key) -> Path | None     the same, but None when the key is empty (for optional tools such as Blender)
  path_list(key) -> list[pathlib.Path]  a list key (allowed_roots, protected_roots) resolved against the repo root
  bambu_profile_roots() -> list[Path]   folders that hold Bambu Studio's BBL\ profile tree, in search order
  bambu_install_dir() -> Path | None    the folder that holds bambu-studio.exe

YAML: PyYAML is used when it is installed (it is in requirements.txt). Without it a small built-in reader handles the
flat "key: value" / "key: [a, b]" form that config\paths.example.yaml uses, so the self-test can still run.
Windows paths: forward slashes, or single quotes. A double-quoted value with a backslash is refused with a plain message,
with or without PyYAML (PyYAML would turn \b, \t, \n into control characters and \x41 silently into "A"), and so is any
loaded value that holds a control character. The file is read as UTF-8 (a BOM is allowed); another encoding is refused
with a message. Every value must be text or a list of text (a number, true/false or a mapping is refused).
Not detectable: a path whose backslashes were dropped before it reached the file ("C:Program FilesBambu Studio") is
plain text; mm_config.py prints "[does not exist]" next to it, which is the hint to fix it.

Example:
  .venv\Scripts\python.exe tools\mm_config.py          prints the resolved configuration
"""
from __future__ import annotations

import os
import pathlib
import re
import sys

DEFAULTS: dict = {
    "bambu_studio_exe": "C:/Program Files/Bambu Studio/bambu-studio.exe",
    "bambu_profiles_dir": "",
    "blender_exe": "",
    "slice_workdir": "work/slice",
    "allowed_roots": ["."],
    "protected_roots": [],
}
LIST_KEYS = ("allowed_roots", "protected_roots")


class MMConfigError(RuntimeError):
    """A required setting is missing or empty in config\\paths.yaml."""


def repo_root() -> pathlib.Path:
    """The repository folder: the parent of the tools\\ folder this file lives in."""
    return pathlib.Path(__file__).resolve().parent.parent


def config_file() -> pathlib.Path:
    """The YAML file load() reads: MM_CONFIG if set, else config\\paths.yaml, else config\\paths.example.yaml."""
    env = os.environ.get("MM_CONFIG", "").strip()
    if env:
        return pathlib.Path(env)
    user = repo_root() / "config" / "paths.yaml"
    if user.is_file():
        return user
    return repo_root() / "config" / "paths.example.yaml"


def _scalar(v: str):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.lower() in ("null", "~"):
        return ""
    return v


def _mini_yaml(text: str) -> dict:
    """Reader for the flat subset used by paths.example.yaml: comments, `key: value`, `key: [a, "b"]`, and a block list
    (`key:` followed by `  - item` lines). Anything else raises MMConfigError."""
    out: dict = {}
    cur_list = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split(" #", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and cur_list is not None:
            out[cur_list].append(_scalar(line.lstrip()[2:]))
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            raise MMConfigError(f"config line {n} is not 'key: value': {raw!r} (install PyYAML for full YAML)")
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        cur_list = None
        if v == "":
            out[k] = []
            cur_list = k
        elif v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            out[k] = [_scalar(x) for x in inner.split(",")] if inner else []
        elif v.startswith(("[", "{")):
            raise MMConfigError(f"config line {n}: unclosed list or mapping: {raw!r}")
        else:
            out[k] = _scalar(v)
    return out


PATH_ADVICE = ("Write Windows paths with forward slashes (\"C:/Program Files/Bambu Studio/bambu-studio.exe\") or in "
               "single quotes ('C:\\Program Files\\Bambu Studio\\bambu-studio.exe'); never put backslashes inside double "
               "quotes, because YAML reads \\b, \\t, \\n and similar as control characters. See docs\\09-troubleshooting.md, "
               "section 6.")


def _bad_config(f: pathlib.Path, line: int | None, problem: str) -> MMConfigError:
    where = f"line {line}" if line else "a value"
    return MMConfigError(f"config\\paths.yaml cannot be read ({f}, {where}): {problem}. {PATH_ADVICE}")


def _parse(text: str, f: pathlib.Path | None = None) -> dict:
    f = f or config_file()
    try:
        import yaml  # PyYAML
    except ImportError:
        # load() has already refused backslashes in double quotes (the mini reader keeps them literally, PyYAML does
        # not), so a file that works now does not break later when PyYAML is installed.
        _refuse_backslash_in_double_quotes(text, f)
        return _mini_yaml(text)
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
        line = (mark.line + 1) if mark is not None else None
        problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
        raise _bad_config(f, line, f"YAML error: {problem}") from None
    return data if isinstance(data, dict) else {}


def _control_chars(value) -> bool:
    """True when a loaded string (or a string in a list) holds a control character: the sign of a mangled path."""
    items = value if isinstance(value, list) else [value]
    # also the characters YAML makes of \N, \_, \L and \P inside double quotes
    odd = {0x7f, 0x85, 0xa0, 0x2028, 0x2029}
    return any(isinstance(s, str) and any(ord(c) < 0x20 or ord(c) in odd for c in s) for s in items)


def _str_or_str_list(v) -> bool:
    """None (an empty value), a string, or a list of strings. Numbers, booleans and mappings are refused."""
    if v is None or isinstance(v, str):
        return True
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _refuse_backslash_in_double_quotes(text: str, f: pathlib.Path) -> None:
    """Refuse any backslash inside a double-quoted value, before either reader sees it. With PyYAML most such escapes
    fail or become control characters (caught later), but some decode silently into a wrong path: "\\x41" -> "A",
    "\\u00e9" -> "e-acute", "\\e" -> ESC, and a correctly doubled "\\\\" is kept here as well for one simple rule. Single
    quotes and forward slashes are the two supported forms."""
    for n, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith("#"):
            continue
        body = re.sub(r"'[^']*'", "''", raw)  # a single-quoted value may hold " and \ freely
        body = body.split(" #", 1)[0]
        for m in re.finditer(r'"([^"]*)"', body):
            if "\\" in m.group(1):
                raise _bad_config(f, n, "a double-quoted value contains a backslash")


def _line_of(text: str, key: str) -> int | None:
    for n, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith(key + ":"):
            return n
    return None


def warnings(cfg: dict | None = None) -> list[str]:
    """Non-fatal problems in the loaded configuration (printed by `tools\\mm_config.py`)."""
    cfg = cfg if cfg is not None else load()
    out = []
    sw = cfg.get("slice_workdir")
    if isinstance(sw, str) and " " in sw:
        out.append(f"WARNING: slice_workdir '{sw}' contains a space; the Bambu Studio command line is more reliable "
                   "with a path that has no spaces (the default is work/slice).")
    return out


def load() -> dict:
    """Built-in defaults overlaid with the YAML file. Never raises for a missing file (the defaults are used)."""
    cfg = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULTS.items()}
    f = config_file()
    try:
        text = f.read_text(encoding="utf-8-sig")  # -sig: Notepad's "UTF-8 with BOM" reads the same as plain UTF-8
    except UnicodeDecodeError as exc:
        raise MMConfigError(f"config\\paths.yaml cannot be read ({f}): it is not UTF-8 ({exc.reason} at byte "
                            f"{exc.start}). Save config\\paths.yaml as UTF-8 (VS Code: the encoding button in the "
                            f"status bar > Save with Encoding > UTF-8).") from None
    except OSError:
        cfg["_source"] = "built-in defaults (no config file found)"
        return cfg
    _refuse_backslash_in_double_quotes(text, f)
    data = _parse(text, f)
    for k, v in data.items():
        if not _str_or_str_list(v):
            raise _bad_config(f, _line_of(text, str(k)), f"'{k}' must be text or a list of text, not "
                                                         f"{type(v).__name__} ({v!r})")
        if _control_chars(v):
            raise _bad_config(f, _line_of(text, str(k)), f"'{k}' contains a control character (a mangled Windows path)")
        if k in LIST_KEYS and v in (None, ""):
            v = []
        if k in LIST_KEYS and isinstance(v, str):
            v = [v]
        cfg[k] = "" if v is None else v
    cfg["_source"] = str(f)
    return cfg


def _resolve(value: str) -> pathlib.Path:
    p = pathlib.Path(os.path.expandvars(str(value)))
    return p if p.is_absolute() else (repo_root() / p)


def optional_path(key: str) -> pathlib.Path | None:
    v = load().get(key, "")
    if v in (None, "") or isinstance(v, list):
        return None
    return _resolve(v)


def path(key: str) -> pathlib.Path:
    p = optional_path(key)
    if p is None:
        raise MMConfigError(f"'{key}' is missing or empty: set it in config\\paths.yaml (copy config\\paths.example.yaml "
                            f"to config\\paths.yaml first; tools\\setup.ps1 does that)")
    return p


def path_list(key: str) -> list[pathlib.Path]:
    v = load().get(key) or []
    if isinstance(v, str):
        v = [v]
    return [_resolve(x) for x in v if str(x).strip()]


def bambu_install_dir() -> pathlib.Path | None:
    exe = optional_path("bambu_studio_exe")
    return exe.parent if exe is not None else None


def bambu_profile_roots() -> list[pathlib.Path]:
    """Folders holding Bambu Studio's BBL\\ profile tree, in search order. bambu_profiles_dir if set; else the
    per-user copy (%APPDATA%\\BambuStudio\\system) then the install's resources\\profiles."""
    own = optional_path("bambu_profiles_dir")
    if own is not None:
        return [own]
    roots = []
    appdata = os.environ.get("APPDATA", "")
    if appdata:
        roots.append(pathlib.Path(appdata) / "BambuStudio" / "system")
    inst = bambu_install_dir()
    if inst is not None:
        roots.append(inst / "resources" / "profiles")
    return roots


def bambu_user_presets_dir() -> pathlib.Path | None:
    """%APPDATA%\\BambuStudio\\user (your saved presets), or None when APPDATA is not set."""
    appdata = os.environ.get("APPDATA", "")
    return pathlib.Path(appdata) / "BambuStudio" / "user" if appdata else None


def main() -> int:
    try:
        cfg = load()
    except MMConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for w in warnings(cfg):
        print(w, file=sys.stderr)
    print(f"config: {cfg.pop('_source')}")
    print(f"repo_root: {repo_root()}")
    for k, v in cfg.items():
        if k in LIST_KEYS:
            print(f"{k}: {[str(p) for p in path_list(k)]}")
        else:
            p = optional_path(k)
            print(f"{k}: {p if p is not None else '(empty)'}" + ("" if p is None or p.exists() else "  [does not exist]"))
    print(f"bambu profile roots: {[str(p) for p in bambu_profile_roots()]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
