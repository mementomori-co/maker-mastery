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

Example:
  .venv\Scripts\python.exe tools\mm_config.py          prints the resolved configuration
"""
from __future__ import annotations

import os
import pathlib
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
        else:
            out[k] = _scalar(v)
    return out


def _parse(text: str) -> dict:
    try:
        import yaml  # PyYAML
    except ImportError:
        return _mini_yaml(text)
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def load() -> dict:
    """Built-in defaults overlaid with the YAML file. Never raises for a missing file (the defaults are used)."""
    cfg = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULTS.items()}
    f = config_file()
    try:
        text = f.read_text(encoding="utf-8")
    except OSError:
        cfg["_source"] = "built-in defaults (no config file found)"
        return cfg
    data = _parse(text)
    for k, v in data.items():
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
    cfg = load()
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
