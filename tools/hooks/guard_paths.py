r"""guard_paths.py - Claude Code PreToolUse hook (matchers: Write|Edit|MultiEdit|NotebookEdit and Bash|PowerShell).

What it does: blocks (exit 2, reason on stderr) any file-tool write under a protected root, and common shell writes into
one: once a command names a protected root (literally, or as a path that resolves under it), every pipeline segment must
be a read-only verb (cat, ls, grep, Get-Content, Get-ChildItem ...), a copy OUT of the root, or a segment that touches
only paths outside the roots; a redirect (> >> 2> *>, with or without spaces) may not land in a root. Verbs that can write
or run code through their arguments (find -delete/-exec, sort -o, uniq IN OUT, tree -o, xxd -r IN OUT, rg --pre,
ForEach-Object / Where-Object) count as read-only only in a segment that names no root, and a segment holding a script
block "{...}" is never read-only while a root is named.
It also blocks a bare `python` / `py` / `pip` command run from inside this repository: call .venv\Scripts\python.exe
explicitly so the repository's own environment is used.
Limits - a safety net, not a sandbox: a command that builds the root path at run time (string joins, variables set in an
earlier command, environment variables, encoded commands, code inside an interpreter) is not recognised, and an MCP
server's own write tools never pass through this hook. For hard isolation use NTFS permissions, a separate Windows user
or a VM. Emptying protected_roots in config\paths.yaml switches the protection off, so review every edit to that file.
Protected roots: protected_roots in config\paths.yaml, plus any in the MM_PROTECTED environment variable (semicolon-separated).
Fails closed: if the config file exists but cannot be read (YAML error, mangled path, wrong encoding), every file-tool
write is blocked except an edit of the config file itself, so it can be fixed, and a shell command passes only when every
segment starts with a strictly read-only verb (the conditional verbs above are refused), holds no script block and
nothing is redirected.
Canonicalisation: strips \\?\ and \\.\ prefixes, maps \\host\D$\ admin-share UNC paths to D:\, resolves 8.3 short names
through GetLongPathNameW on the longest existing prefix, follows junctions, normalises case and separators.
Input: the hook JSON on stdin. Output: exit 0 = no decision (normal permission flow applies), 2 = blocked (reason on stderr),
1 = hook JSON unreadable (non-blocking error). Never modifies files.
Doc: https://code.claude.com/docs/en/hooks  (exit code 2 blocks the action; stderr goes back to Claude).
Example (manual run, PowerShell):
  '{"tool_input": {"file_path": "D:/Finished/x.txt"}}' | .venv\Scripts\python.exe tools\hooks\guard_paths.py
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

TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
sys.path.insert(0, TOOLS_DIR)


CONFIG_UNREADABLE = ("BLOCKED by tools\\hooks\\guard_paths.py: config\\paths.yaml cannot be read; fix it (see "
                     "docs\\09-troubleshooting.md, section 6) before Claude can write files. Editing config\\paths.yaml "
                     "itself is still allowed. Details: ")


def _config_roots() -> tuple[list[str], str, str]:
    """(protected_roots, error, config file). Fails closed: when the config file exists but cannot be read, error is
    set and main() blocks every write except an edit of that config file, so protected roots never silently vanish."""
    cfg_file = ""
    try:
        import mm_config
        cfg_file = str(mm_config.config_file())
        return [str(p) for p in mm_config.path_list("protected_roots")], "", cfg_file
    except Exception as exc:  # noqa: BLE001
        if cfg_file and not os.path.isfile(cfg_file):
            return [], "", cfg_file  # no config file at all: the built-in defaults have no protected roots
        return [], f"{type(exc).__name__}: {exc}", cfg_file


DEFAULT_PROTECTED, CONFIG_ERROR, CONFIG_FILE = _config_roots()
# administrative share of ANY host, any case, forward or back slashes (\\host\d$\..., //HOST/D$/...).
UNC_LOCAL = re.compile(r"^[\\/]{2}[^\\/?.][^\\/]*[\\/]([A-Za-z])\$(?:[\\/](.*))?$", re.I)
WRITEISH = re.compile(
    r"(?:^|[\s;&|(])(?:rm|mv|cp|tee|touch|mkdir|rmdir|del|erase|move|copy|ren|rename|xcopy|robocopy|"
    r"set-content|add-content|out-file|copy-item|move-item|remove-item|new-item|rename-item|clear-content)\b"
    r"|(?<![-=<>])(?:\d|\*)?>>?(?![=>])\s*\S",  # shell redirect incl. a>b, 2>b, *>b; not -> => <> >=
    re.I,
)


def long_path(q: str) -> str:
    """Resolve 8.3 short names via Win32 on the longest existing prefix; return q unchanged if not on Windows."""
    try:
        import ctypes

        k32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        buf = ctypes.create_unicode_buffer(4096)
        if k32.GetLongPathNameW(q, buf, 4096):
            return buf.value
        head, tail = q, ""
        while head and not os.path.exists(head):
            head, t = os.path.split(head)
            if not t:
                break
            tail = os.path.join(t, tail) if tail else t
        if head and k32.GetLongPathNameW(head, buf, 4096):
            return os.path.join(buf.value, tail) if tail else buf.value
    except Exception:  # noqa: BLE001
        pass
    return q


def norm(p: str) -> str:
    q = p.strip().strip('"').strip("'")
    q = re.sub(r"^[\\/]{2}[?.][\\/]UNC[\\/]", r"\\\\", q, flags=re.I)  # \\?\UNC\host\share -> \\host\share
    q = re.sub(r"^[\\/]{2}[?.][\\/](?=[A-Za-z]:)", "", q)  # \\?\D:\x -> D:\x
    m = UNC_LOCAL.match(q)
    if m:
        q = m.group(1) + ":\\" + (m.group(2) or "")
    q = os.path.abspath(q)
    try:
        q = os.path.realpath(q)  # follow directory junctions / symlinks on the existing prefix
    except Exception:  # noqa: BLE001
        pass
    q = long_path(q)
    return os.path.normcase(os.path.normpath(q))


def roots() -> list[str]:
    extra = [r for r in os.environ.get("MM_PROTECTED", "").split(";") if r.strip()]
    return DEFAULT_PROTECTED + extra


def check_path(target: str) -> int:
    t = norm(target)
    for root in roots():
        r = norm(root)
        if t == r or t.startswith(r + os.sep):
            print(
                "BLOCKED by tools\\hooks\\guard_paths.py: '" + target + "' resolves under the protected root '"
                + root + "' (protected_roots in config\\paths.yaml). Claude reads this folder only. Copy the file into "
                "the repository instead, or remove the root from config\\paths.yaml yourself.",
                file=sys.stderr,
            )
            return 2
    return 0


# ---- shell-command guard ----------------------------------------------------------------------------------------
# Verbs that only read. When a protected root is named anywhere in the command, every pipeline segment must start with
# one of these (or be a copy whose destination is outside the roots), and no redirect may target a root.
READ_ONLY = {
    "cat", "ls", "dir", "grep", "egrep", "fgrep", "head", "tail", "wc", "stat", "file", "od",
    "md5sum", "sha1sum", "sha256sum", "sha512sum", "diff", "cmp", "less", "more", "echo", "printf", "test", "[", "pwd",
    "which", "type", "realpath", "readlink", "du", "cut", "tr", "strings", "basename", "dirname",
    "true", "false", "exit", "return",
    "get-content", "gc", "get-childitem", "gci", "get-item", "gi", "select-string", "sls", "test-path", "get-filehash",
    "measure-object", "get-itemproperty", "gp", "resolve-path", "rvpa", "write-output", "write-host", "compare-object",
    "out-string", "format-table", "ft", "format-list", "fl", "select-object", "select", "get-date",
}
# Verbs that usually read but can write or run code through their arguments (find -delete / -exec / -fprint, sort -o,
# uniq IN OUT, tree -o, xxd -r IN OUT, date -f, rg --pre, ForEach-Object / Where-Object script blocks). They count as
# read-only only in a segment that names no protected root; they are never read-only in fail-closed mode.
CONDITIONAL_READ = {"find", "sort", "uniq", "tree", "xxd", "date", "rg", "foreach-object", "%", "foreach",
                    "where-object", "where", "?", "sort-object", "group-object"}
COPY_VERBS = {"cp", "copy", "copy-item", "cpi", "xcopy", "robocopy", "rsync"}
CD_VERBS = {"cd", "pushd", "set-location", "sl", "chdir"}
# Bare interpreter names resolve through PATH (on Windows `python.exe` / `python3.exe` in WindowsApps can be the
# Microsoft Store redirector that opens an installer). Inside the repository only the venv interpreter is allowed.
# Checked only when cwd is under the repository folder.
BARE_PY = {"python", "python3", "py", "pip", "pip3", "python.exe", "python3.exe", "py.exe", "pip.exe"}
VENV_PY = os.path.normcase(os.path.join(REPO_ROOT, ".venv", "Scripts", "python.exe"))
BRAIN_ROOT = os.path.normcase(REPO_ROOT)
SEGMENT_SPLIT = re.compile(r"\|\|?|&&|;|\n|`|\$\(|\)")
TOKEN = re.compile(r'"([^"]*)"|\'([^\']*)\'|(\S+)')
# Shell redirect: > >> n> n>> *> with or without spaces (a>b, cat x>>"y"). Not the arrows -> and => (Python,
# PowerShell), not <> and not the comparison >=. Group 1 is the destination.
REDIRECT = re.compile(r"(?<![-=<>])(?:\d|\*)?>>?(?![=>])\s*(\"[^\"]*\"|'[^']*'|[^\s\"';|&<>]+)")
QUOTED = re.compile(r'"([^"]*)"|\'([^\']*)\'')
PATHLIKE = re.compile(r"^(?:[a-z]:\\|\\\\|\.\.?\\|\.\.?$|[^\s\\]*\\)")


HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[ \t]*\r?\n.*?\r?\n\1[ \t]*(?=\r?\n|$)", re.S)


def _normalise(cmd: str) -> str:
    cmd = HEREDOC.sub("<<HEREDOC_BODY_STRIPPED", cmd)  # heredoc bodies are data; the redirect target decides
    t = cmd.replace("\\\\", "\\").replace("/", "\\")
    t = t.replace('""', "").replace("''", "")  # adjacent-quote joins: "D:\Finished Pro""jects"
    return t.lower()


def _resolve(tok: str, cwd: str) -> str:
    tok = tok.strip().strip('"').strip("'")
    for sep in ("=", ":"):
        if sep in tok and not re.match(r"^[a-z]:\\", tok):
            right = tok.split(sep, 1)[1]
            if PATHLIKE.match(right) or right.startswith(".."):
                tok = right
    if re.match(r"^[a-z]:\\", tok) or tok.startswith("\\\\"):
        return norm(tok)
    return norm(os.path.join(cwd, tok))


def _under_root(resolved: str, roots_n: list[str]) -> bool:
    return any(resolved == r or resolved.startswith(r + os.sep) for r in roots_n)


def _path_tokens(segment: str) -> list[str]:
    out = []
    for m in TOKEN.finditer(segment):
        tok = m.group(1) if m.group(1) is not None else (m.group(2) if m.group(2) is not None else m.group(3))
        if tok and (PATHLIKE.match(tok) or tok.startswith("..") or "\\" in tok):
            out.append(tok)
    # quoted strings glued to other text (--output="x", a>"x") and redirect targets glued to the verb (a>x)
    extra = [a or b for a, b in QUOTED.findall(segment)] + [m.group(1) for m in REDIRECT.finditer(segment)]
    for tok in extra:
        tok = tok.strip('"').strip("'")
        if tok and tok not in out and (PATHLIKE.match(tok) or tok.startswith("..") or "\\" in tok):
            out.append(tok)
    return out


def check_command(cmd: str, cwd: str | None = None) -> int:
    cwd = cwd or os.getcwd()
    text = _normalise(cmd)
    if os.path.normcase(os.path.abspath(cwd)).startswith(BRAIN_ROOT):
        for sg in [x.strip() for x in SEGMENT_SPLIT.split(text) if x.strip()]:
            words = [w for w in sg.split() if not re.match(r"^\w+=\S*$", w) and w not in ("sudo", "nohup", "time", "&")]
            if words and words[0].strip('"').strip("'") in BARE_PY:
                print("BLOCKED by tools\\hooks\\guard_paths.py: bare '" + words[0] + "' resolves through PATH "
                      "(the WindowsApps alias can open the Microsoft Store installer). "
                      "Call " + VENV_PY + " explicitly (tools\\setup.ps1 creates it).", file=sys.stderr)
                return 2
    roots_n = [norm(r) for r in roots()]
    literal_hit = any(norm(r).lower() in text for r in roots())
    segments = [sg.strip() for sg in SEGMENT_SPLIT.split(text) if sg.strip()]
    # 1. any path-like token (absolute, UNC or relative to cwd) that resolves under a root?
    token_hit = False
    for sg in segments:
        for tok in _path_tokens(sg):
            try:
                if _under_root(_resolve(tok, cwd), roots_n):
                    token_hit = True
            except Exception:  # noqa: BLE001
                pass
    if not (literal_hit or token_hit):
        return 0
    # 2. the command names a protected root: every segment must be read-only
    for sg in segments:
        words = [w for w in sg.split() if not re.match(r"^\w+=\S*$", w) and w not in ("sudo", "nohup", "time", "&")]
        if not words:
            continue
        verb = os.path.basename(words[0].strip('"').strip("'")).removesuffix(".exe")
        paths = _path_tokens(sg)
        if verb in CD_VERBS:
            tgt = next((p for p in paths), None)
            if tgt is not None and _under_root(_resolve(tgt, cwd), roots_n):
                print("BLOCKED by tools\\hooks\\guard_paths.py: do not cd/pushd into a protected root "
                      "(protected_roots in config\\paths.yaml); use absolute paths and copy files INTO the repository instead.", file=sys.stderr)
                return 2
            continue
        # redirects: the target decides
        for rm in REDIRECT.finditer(sg):
            tgt = rm.group(1).strip('"').strip("'")
            if tgt in ("\\dev\\null", "nul") or tgt.startswith("&"):
                continue
            if _under_root(_resolve(tgt, cwd), roots_n):
                print("BLOCKED by tools\\hooks\\guard_paths.py: a shell redirect targets a protected root "
                      "(protected_roots in config\\paths.yaml). Write INTO the repository instead.", file=sys.stderr)
                return 2
        if verb in COPY_VERBS:
            dest = None
            mdest = re.search(r"-destination[:\s]+(\"[^\"]*\"|'[^']*'|\S+)", sg)
            if mdest:
                dest = mdest.group(1)
            elif paths:
                dest = paths[-1]
            if dest is None or _under_root(_resolve(dest, cwd), roots_n):
                print("BLOCKED by tools\\hooks\\guard_paths.py: copying INTO a protected root "
                      "(protected_roots in config\\paths.yaml) is not allowed. Copy out of it instead.", file=sys.stderr)
                return 2
            continue  # copy OUT of the root is a read
        seg_touches_root = any(norm(r).lower() in sg for r in roots()) or any(
            _under_root(_resolve(p, cwd), roots_n) for p in paths)
        script_block = "{" in sg  # a script block can run any command: never read-only while a root is named
        if not script_block and verb in READ_ONLY:
            continue
        if not script_block and verb in CONDITIONAL_READ and not seg_touches_root:
            continue
        # a segment that does not itself touch a root, names at least one explicit path outside the roots and uses no
        # shell variables is allowed (mkdir/rm/mv on repository paths chained with a read of the root) - variables are
        # blocked because `x="<root>"; rm -rf "$x"` would hide the root from this segment.
        if not seg_touches_root and paths and "$" not in sg and "%" not in sg and not script_block:
            continue
        print("BLOCKED by tools\\hooks\\guard_paths.py: the command names a protected root "
              "(protected_roots in config\\paths.yaml) and '" + verb + "' is not a read-only verb (allowed: cat ls dir find grep rg head "
              "tail wc stat md5sum Get-Content Get-ChildItem Select-String Test-Path ..., or cp/Copy-Item OUT of the root; "
              "find, sort, uniq, tree, xxd, rg and ForEach-Object/Where-Object may not name a protected path, and no "
              "script block { } is allowed). "
              "Interpreters (python, cmd, powershell, git, sed, tar) are blocked: copy the file INTO the repository first.", file=sys.stderr)
        return 2
    return 0


def _read_only_command(cmd: str) -> bool:
    """True when every pipeline segment starts with a READ_ONLY verb, no segment holds a script block and nothing is
    redirected. Used only in fail-closed mode (roots unknown), so CONDITIONAL_READ verbs are refused."""
    text = _normalise(cmd)
    if REDIRECT.search(text) or "<<" in text or "{" in text:
        return False
    for sg in [x.strip() for x in SEGMENT_SPLIT.split(text) if x.strip()]:
        words = [w for w in sg.split() if not re.match(r"^\w+=\S*$", w)]
        if not words:
            continue
        verb = os.path.basename(words[0].strip('"').strip("'")).removesuffix(".exe")
        if verb not in READ_ONLY:
            return False
    return True


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        # never silent. Raw scan: a protected root plus a write-ish token blocks; otherwise exit 1. With
        # "onFailure": "block" on this hook in .claude\settings.json (Claude Code v2.1.295 or later), exit 1 counts as a
        # hook failure and blocks the call; on older versions it is a non-blocking hook error shown in the transcript.
        low = raw.replace("\\\\", "\\").replace("/", "\\").lower()
        if any(norm(r).lower() in low for r in roots()) and WRITEISH.search(raw):
            print("BLOCKED by tools\\hooks\\guard_paths.py: hook JSON unparsable (" + str(exc) +
                  ") but the raw input names the protected root with a write token.", file=sys.stderr)
            return 2
        if CONFIG_ERROR:
            print(CONFIG_UNREADABLE + CONFIG_ERROR, file=sys.stderr)
            return 2
        print("guard_paths.py: could not parse hook JSON (" + str(exc) + "); no decision", file=sys.stderr)
        return 1
    ti = payload.get("tool_input") or {}
    target = ti.get("file_path") or ti.get("notebook_path")
    cmd = ti.get("command")
    if CONFIG_ERROR:
        # fail closed: protected roots are unknown. The one write allowed is a file-tool edit of the config file
        # itself, so it can be fixed; shell commands pass only when every segment is a read-only verb with no redirect.
        if target:
            if CONFIG_FILE and norm(target) == norm(CONFIG_FILE):
                return 0
            print(CONFIG_UNREADABLE + CONFIG_ERROR, file=sys.stderr)
            return 2
        if cmd:
            if _read_only_command(cmd):
                return 0
            print(CONFIG_UNREADABLE + CONFIG_ERROR, file=sys.stderr)
            return 2
        return 0
    if target:
        return check_path(target)
    if cmd:
        return check_command(cmd, payload.get("cwd") or None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
