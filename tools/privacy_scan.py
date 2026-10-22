#!/usr/bin/env python3
"""privacy_scan.py - find personal data before you publish a folder or a fork.

Standard library only (Python 3.12+). Nothing is changed on disk.

Usage:
    python tools/privacy_scan.py ROOT --denylist FILE [--json OUT]
                                 [--exclude-dir NAME ...] [--no-builtin]

What is scanned (every file under ROOT except the excluded folders, the file passed
as --denylist and ROOT/config/denylist.example.txt, which are skipped by default):
  (a) text file contents (UTF-8, undecodable bytes replaced; UTF-16 with BOM)
  (b) file and folder names (the repo-relative path)
  (c) PNG tEXt / zTXt / iTXt / eXIf chunks (and any other ancillary chunk)
  (d) JPEG APPn segments (APP1 EXIF / XMP, APP13 IPTC, ...) and COM segments
  (e) ZIP-based files (.zip .3mf .docx .xlsx ...): member names and member
      contents, recursively (a ZIP inside a ZIP is opened too)
  (f) PDF metadata: /Author /Creator /Producer /Title /Subject /Keywords
      and XMP packets, also inside Flate-compressed streams
  (g) any other binary file: ASCII and UTF-16LE strings of 4+ characters

Denylist file format (one entry per line):
    # comment                       ignored
    plain text                      case-insensitive substring
    re:<python regex>               case-insensitive regular expression
    allow: <repo-relative path> | <exact phrase>
                                    the exact phrase is allowed in that one
                                    file (or archive); everything else in the
                                    file is still checked

Built-in rules (turn them all off with --no-builtin):
    userpath      Windows and macOS user-profile paths: a drive letter (any drive)
                  or a slash, then the Users folder, then a name
    email         e-mail addresses, except @users.noreply.github.com and
                  the reserved example.com / example.org / example.net and
                  the reserved top-level names .example and .invalid (RFC 2606)
    private-ip    IPv4 in 10/8, 172.16/12, 192.168/16 and CGNAT 100.64/10
    secret        long hex / base64 values near key, token, secret,
                  password or access_code (values are always masked)
    printer-serial  HEURISTIC: 15-character upper-case serials in the style
                  of Bambu Lab printers. The 15-character length comes from
                  https://wiki.bambulab.com/en/general/find-sn ; the exact
                  per-model prefix scheme is not published, so this rule
                  can miss serials and can flag other 15-character codes.

Output: one line per hit, "path:line: [rule] context", then a summary.
Exit code: 0 clean, 1 hits found, 2 errors (scan incomplete).
Full secret values are never printed: secret-looking values are masked in
every context line and in the JSON report.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import io
import json
import os
import re
import struct
import sys
import zipfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_EXCLUDES = (".git", ".venv", "work", "dist")
CONTEXT_WIDTH = 120
MAX_FILE_BYTES = 1 << 30          # files larger than this are reported as errors
MAX_MEMBER_BYTES = 512 << 20      # per ZIP member
MAX_ZIP_DEPTH = 6
MIN_STRING = 4

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PNG_SKIP_CHUNKS = {b"IHDR", b"PLTE", b"IDAT", b"IEND"}
TEXT_EXTS = {
    ".txt", ".md", ".markdown", ".rst", ".py", ".pyw", ".ps1", ".psm1", ".bat", ".cmd",
    ".sh", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".config", ".xml", ".model", ".rels", ".html", ".htm", ".css", ".js", ".mjs",
    ".ts", ".csv", ".tsv", ".svg", ".gcode", ".log", ".gitignore", ".gitattributes",
    ".scad", ".obj", ".mtl", ".tex", ".ipynb", ".lua",
}


# ----------------------------------------------------------------------------
# rules
# ----------------------------------------------------------------------------
@dataclass
class Rule:
    name: str
    regex: re.Pattern
    secret: bool = False                     # mask the whole match
    check: object = None                     # optional callable(match) -> bool


@dataclass
class Allow:
    path: str
    phrase: str


@dataclass
class Hit:
    path: str
    line: int
    rule: str
    context: str
    col: int = 0


@dataclass
class State:
    rules: list
    allows: list
    hits: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    files: int = 0
    surfaces: dict = field(default_factory=dict)


_EMAIL_OK = re.compile(
    r"@(?:[a-z0-9-]+\.)*(?:users\.noreply\.github\.com|example\.(?:com|org|net)|example|invalid)$", re.I)


_FILE_TLDS = {
    "json", "png", "jpg", "jpeg", "gif", "webp", "svg", "md", "txt", "py", "js", "css", "html",
    "htm", "yaml", "yml", "xml", "stl", "3mf", "step", "stp", "obj", "gcode", "pdf", "zip", "csv",
    "ini", "cfg", "toml", "ps1", "bat", "exe", "dll", "model", "config", "png2x",
}


def _email_ok(m: re.Match) -> bool:
    s = m.group(0)
    local, _, domain = s.partition("@")
    if domain.rsplit(".", 1)[-1].lower() in _FILE_TLDS:   # e.g. "Name%20@base.json", "icon@2x.png"
        return False
    if re.fullmatch(r"(?:%[0-9A-Fa-f]{2})+", local):       # URL-encoded space before an @ in a link
        return False
    return not _EMAIL_OK.search(s)


def _serial_ok(m: re.Match) -> bool:
    s = m.group(0)
    digits = sum(c.isdigit() for c in s)
    letters = sum(c.isalpha() for c in s)
    return 7 <= digits <= 14 and letters >= 1


def _ip_ok(m: re.Match) -> bool:
    try:
        return all(0 <= int(p) <= 255 for p in m.group(0).split("."))
    except ValueError:
        return False


_SECRET_VALUE = r"(?:[A-Fa-f0-9]{16,}|[A-Za-z0-9+/_\-]{20,}={0,2})"
_SECRET_WORD = r"(?:api[_ -]?key|private[_ -]?key|key|token|secret|passw(?:or)?d|pwd|access[_ -]?code)"
_SECRET_RE = re.compile(
    _SECRET_WORD + r"[\"']?[^\S\n]{0,3}[:=][^\S\n]{0,3}[\"']?(" + _SECRET_VALUE + r")"
    r"|" + _SECRET_WORD + r"[^\n]{0,40}?[\s\"'=:](" + _SECRET_VALUE + r")(?![A-Za-z0-9+/=_\-])"
    r"|access[_ -]?code[\"']?[^\S\n]{0,3}[:=][^\S\n]{0,3}[\"']?([A-Za-z0-9]{6,})",
    re.I)


def _looks_secret(v: str, min_len: int = 20) -> bool:
    """Heuristic: random-looking hex or base64, not a word or snake_case name."""
    if re.fullmatch(r"[A-Fa-f0-9]{16,}", v) and sum(c.isdigit() for c in v) >= 3:
        return True
    if len(v) < min_len:
        return False
    digits = sum(c.isdigit() for c in v)
    upper = sum(c.isupper() for c in v)
    lower = sum(c.islower() for c in v)
    seps = sum(c in "/_-." for c in v)
    return digits >= 2 and upper >= 2 and lower >= 2 and seps / len(v) < 0.1


def _secret_ok(m: re.Match) -> bool:
    if m.group(3):  # access_code = <6+ alphanumerics>
        return any(c.isdigit() for c in m.group(3))
    v = m.group(1) or m.group(2)
    return _looks_secret(v)


def builtin_rules() -> list:
    return [
        Rule("userpath", re.compile(
            r"(?:\b[A-Za-z]:)?(?:\\\\|\\|/){1,2}Users(?:\\\\|\\|/){1,2}"
            r"(?!(?:Public|Default|All Users|Default User)(?:[\\/\"'\s]|$))"
            r"[A-Za-z0-9._\-][A-Za-z0-9._ \-]{0,63}", re.I)),
        Rule("email", re.compile(
            r"(?<![A-Za-z0-9._%+\-])[A-Za-z0-9._%+\-]{1,64}@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,24}\b"),
            check=_email_ok),
        Rule("private-ip", re.compile(
            r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            r"|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}"
            r"|192\.168\.\d{1,3}\.\d{1,3}"
            r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3})(?![\d]|\.\d)"),
            check=_ip_ok),
        Rule("secret", _SECRET_RE, secret=True, check=_secret_ok),
        Rule("printer-serial", re.compile(r"(?<![A-Za-z0-9])0[0-9A-Z]{14}(?![A-Za-z0-9])"),
             check=_serial_ok),
    ]


def load_denylist(path: Path) -> tuple[list, list]:
    rules, allows = [], []
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("allow:"):
            body = line[6:]
            if "|" not in body:
                raise ValueError(f"denylist line {n}: allow needs 'path | phrase'")
            p, phrase = body.split("|", 1)
            p, phrase = p.strip().replace("\\", "/").lstrip("./"), phrase.strip()
            if not p or not phrase:
                raise ValueError(f"denylist line {n}: empty path or phrase in allow")
            allows.append(Allow(p, phrase))
        elif line.startswith("re:"):
            try:
                rx = re.compile(line[3:], re.I)
            except re.error as e:
                raise ValueError(f"denylist line {n}: bad regex: {e}") from None
            rules.append(Rule(f"deny:L{n}", rx))
        else:
            # plain substring: keep the raw line (minus surrounding spaces)
            rules.append(Rule(f"deny:L{n}", re.compile(re.escape(line), re.I)))
    return rules, allows


# ----------------------------------------------------------------------------
# masking and context
# ----------------------------------------------------------------------------
_LONG_TOKEN = re.compile(r"(?<![A-Za-z0-9+/_\-])[A-Za-z0-9+/_\-]{24,}={0,2}")


def _mask_value(v: str) -> str:
    return (v[:2] + "*" * 6 + f"[masked {len(v)} chars]") if len(v) > 4 else "****"


def mask_text(s: str) -> str:
    """Mask every secret-looking value in s (used on every context line)."""
    def sec(m: re.Match) -> str:
        if not _secret_ok(m):
            return m.group(0)
        out = m.group(0)
        for g in m.groups():
            if g:
                out = out.replace(g, _mask_value(g))
        return out
    s = _SECRET_RE.sub(sec, s)

    def tok(m: re.Match) -> str:
        v = m.group(0)
        return _mask_value(v) if _looks_secret(v, 24) else v
    return _LONG_TOKEN.sub(tok, s)


def make_context(line: str, start: int, end: int) -> str:
    clean = "".join(c if (c.isprintable() and c not in "\r\n") else " " for c in line)
    if len(clean) > CONTEXT_WIDTH:
        mid = (start + end) // 2
        lo = max(0, min(mid - CONTEXT_WIDTH // 2, len(clean) - CONTEXT_WIDTH))
        clean = clean[lo:lo + CONTEXT_WIDTH]
        if lo > 0:
            clean = "..." + clean[3:]
        if lo + CONTEXT_WIDTH < len(line):
            clean = clean[:-3] + "..."
    return mask_text(clean.strip())


# ----------------------------------------------------------------------------
# core matching
# ----------------------------------------------------------------------------
def _allowed_for(state: State, relpath: str) -> list:
    base = relpath.split("!", 1)[0].split("#", 1)[0]
    return [a.phrase for a in state.allows if a.path in (relpath, base)]


def scan_text(state: State, relpath: str, text: str, first_line: int = 1) -> None:
    allowed = _allowed_for(state, relpath)
    for i, line in enumerate(text.splitlines() or [""], first_line):
        if not line:
            continue
        work = line
        for phrase in allowed:
            if phrase in work:
                work = work.replace(phrase, " " * len(phrase))
        for rule in state.rules:
            for m in rule.regex.finditer(work):
                if m.end() == m.start():
                    continue
                if rule.check and not rule.check(m):
                    continue
                if rule.secret:
                    g = next((k for k in range(1, (m.re.groups or 0) + 1) if m.group(k)), 0)
                    gs, ge = m.span(g)
                    ctx_line = line[:gs] + _mask_value(m.group(g)) + line[ge:]
                    ctx = make_context(ctx_line, m.start(), gs + 20)
                else:
                    ctx = make_context(line, m.start(), m.end())
                state.hits.append(Hit(relpath, i, rule.name, ctx, m.start()))


def _count(state: State, surface: str) -> None:
    state.surfaces[surface] = state.surfaces.get(surface, 0) + 1


def extract_strings(data: bytes, minimum: int = MIN_STRING) -> list[str]:
    out = [m.group(0).decode("ascii")
           for m in re.finditer(rb"[\x20-\x7e\t]{%d,}" % minimum, data)]
    out += [m.group(0).decode("utf-16-le", "replace")
            for m in re.finditer(rb"(?:[\x20-\x7e\t]\x00){%d,}" % minimum, data)]
    return out


def scan_strings(state: State, relpath: str, data: bytes) -> None:
    strs = extract_strings(data)
    if strs:
        scan_text(state, relpath, "\n".join(strs))


def is_text(name: str, data: bytes) -> bool:
    if data[:2] in (b"\xff\xfe", b"\xfe\xff") or data[:3] == b"\xef\xbb\xbf":
        return True
    ext = os.path.splitext(name)[1].lower()
    sample = data[:8192]
    if b"\x00" in sample:
        return False
    if ext in TEXT_EXTS:
        return True
    if not sample:
        return True
    bad = sum(1 for b in sample if b < 9 or (13 < b < 32))
    return bad / len(sample) < 0.01


def decode_text(data: bytes) -> str:
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", errors="replace")
    return data.decode("utf-8-sig", errors="replace")


# ----------------------------------------------------------------------------
# format handlers
# ----------------------------------------------------------------------------
def scan_png(state: State, relpath: str, data: bytes) -> None:
    pos = 8
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        label = f"{relpath}#{ctype.decode('latin-1', 'replace')}"
        try:
            if ctype == b"tEXt":
                k, _, v = body.partition(b"\x00")
                scan_text(state, label, k.decode("latin-1") + "\n" + v.decode("latin-1"))
            elif ctype == b"zTXt":
                k, _, rest = body.partition(b"\x00")
                v = zlib.decompress(rest[1:])
                scan_text(state, label, k.decode("latin-1") + "\n" + v.decode("latin-1"))
            elif ctype == b"iTXt":
                k, _, rest = body.partition(b"\x00")
                flag, _method = rest[0], rest[1]
                lang, _, rest = rest[2:].partition(b"\x00")
                tkey, _, txt = rest.partition(b"\x00")
                if flag:
                    txt = zlib.decompress(txt)
                scan_text(state, label, "\n".join([
                    k.decode("latin-1"), lang.decode("latin-1", "replace"),
                    tkey.decode("utf-8", "replace"), txt.decode("utf-8", "replace")]))
            elif ctype not in PNG_SKIP_CHUNKS:
                # eXIf and every other ancillary chunk (iCCP, private chunks)
                if ctype == b"iCCP":
                    name, _, rest = body.partition(b"\x00")
                    scan_text(state, label, name.decode("latin-1"))
                    try:
                        body = zlib.decompress(rest[1:])
                    except zlib.error:
                        pass
                scan_strings(state, label, body)
        except (zlib.error, IndexError, UnicodeDecodeError) as e:
            state.errors.append(f"{label}: cannot decode chunk ({e})")
        if ctype == b"IEND":
            break
    if pos < len(data):  # data appended after IEND
        scan_strings(state, f"{relpath}#after-IEND", data[pos:])


def scan_jpeg(state: State, relpath: str, data: bytes) -> None:
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            break
        marker = data[pos + 1]
        if marker == 0xFF:
            pos += 1
            continue
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        if marker == 0xD9:
            break
        seglen = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        body = data[pos + 4:pos + 2 + seglen]
        if marker == 0xDA:  # start of scan: image data follows
            break
        if 0xE0 <= marker <= 0xEF:
            tag = body[:12].split(b"\x00", 1)[0].decode("latin-1", "replace")[:20] or "?"
            tag = re.sub(r"[^A-Za-z0-9:/._-]", "", tag)
            label = f"{relpath}#APP{marker - 0xE0}-{tag}"
            if b"<x:xmpmeta" in body or b"<?xpacket" in body:
                label = f"{relpath}#APP{marker - 0xE0}-XMP"
                scan_text(state, label, body.decode("utf-8", "replace"))
            else:
                scan_strings(state, label, body)
        elif marker == 0xFE:
            scan_text(state, f"{relpath}#COM", body.decode("utf-8", "replace"))
        pos += 2 + seglen
    # trailer after EOI (some tools append data)
    eoi = data.rfind(b"\xff\xd9")
    if eoi != -1 and eoi + 2 < len(data):
        scan_strings(state, f"{relpath}#after-EOI", data[eoi + 2:])


_PDF_KEYS = (b"Author", b"Creator", b"Producer", b"Title", b"Subject", b"Keywords")
_PDF_KEY_RE = re.compile(rb"/(" + b"|".join(_PDF_KEYS) + rb")\s*(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]*>)", re.S)


def _pdf_string(tok: bytes) -> str:
    if tok.startswith(b"<"):
        hexs = re.sub(rb"\s", b"", tok[1:-1]).decode("ascii")
        raw = bytes.fromhex(hexs + ("0" if len(hexs) % 2 else ""))
    else:
        body = tok[1:-1]
        out = bytearray()
        i = 0
        esc = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f"}
        while i < len(body):
            c = body[i:i + 1]
            if c == b"\\" and i + 1 < len(body):
                nxt = body[i + 1:i + 2]
                if nxt in esc:
                    out += esc[nxt]; i += 2
                elif nxt.isdigit():
                    j = i + 1
                    while j < len(body) and j < i + 4 and body[j:j + 1].isdigit():
                        j += 1
                    out.append(int(body[i + 1:j], 8) & 0xFF); i = j
                else:
                    out += nxt; i += 2
            else:
                out += c; i += 1
        raw = bytes(out)
    if raw[:2] == b"\xfe\xff":
        return raw[2:].decode("utf-16-be", "replace")
    return raw.decode("latin-1")


def _pdf_meta(state: State, label: str, blob: bytes) -> None:
    for m in _PDF_KEY_RE.finditer(blob):
        scan_text(state, f"{label}/{m.group(1).decode()}", _pdf_string(m.group(2)))
    for m in re.finditer(rb"<x:xmpmeta.*?</x:xmpmeta>", blob, re.S):
        scan_text(state, f"{label}/XMP", m.group(0).decode("utf-8", "replace"))


def scan_pdf(state: State, relpath: str, data: bytes) -> None:
    _pdf_meta(state, f"{relpath}#pdf", data)
    for m in re.finditer(rb"stream\r?\n", data):
        start = m.end()
        end = data.find(b"endstream", start)
        if end == -1:
            continue
        chunk = data[start:end]
        try:
            dec = zlib.decompressobj().decompress(chunk, MAX_MEMBER_BYTES)
        except zlib.error:
            continue
        if dec:
            _pdf_meta(state, f"{relpath}#pdf-stream", dec)
    # catch-all: readable strings anywhere in the raw file
    scan_strings(state, f"{relpath}#pdf-strings", data)


def scan_zip(state: State, relpath: str, data: bytes, depth: int) -> None:
    if depth > MAX_ZIP_DEPTH:
        state.errors.append(f"{relpath}: ZIP nesting deeper than {MAX_ZIP_DEPTH}")
        return
    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except (zipfile.BadZipFile, OSError, ValueError) as e:
        state.errors.append(f"{relpath}: bad ZIP ({e}); scanned as binary")
        scan_strings(state, relpath, data)
        return
    with zf:
        if zf.comment:
            scan_text(state, f"{relpath}#zip-comment", zf.comment.decode("utf-8", "replace"))
        for info in zf.infolist():
            mpath = f"{relpath}!{info.filename}"
            scan_text(state, f"{mpath}#name", info.filename)
            if info.is_dir():
                continue
            if info.file_size > MAX_MEMBER_BYTES:
                state.errors.append(f"{mpath}: member larger than {MAX_MEMBER_BYTES} bytes, not scanned")
                continue
            try:
                blob = zf.read(info)
            except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError, zlib.error) as e:
                state.errors.append(f"{mpath}: cannot read member ({e})")
                continue
            scan_blob(state, mpath, info.filename, blob, depth + 1)


_DATA_URI = re.compile(r"data:([\w.+\-]+/[\w.+\-]+)?(?:;[\w\-]+=[\w\-.]+)*;base64,([A-Za-z0-9+/=\s]{16,})")


def _scan_data_uris(state: State, relpath: str, text: str, depth: int) -> str:
    """Decode base64 data: URIs (images embedded in SVG / HTML / Markdown) and scan the
    payload as its own file; return the text with the base64 body blanked so random
    base64 letters do not raise false hits."""
    if "base64," not in text:
        return text
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        try:
            blob = base64.b64decode(re.sub(r"\s", "", m.group(2)) + "===", validate=False)
        except (binascii.Error, ValueError) as e:
            state.errors.append(f"{relpath}: cannot decode data URI {n} ({e})")
            return m.group(0)
        ext = {"image/png": ".png", "image/jpeg": ".jpg", "application/pdf": ".pdf"}.get(m.group(1) or "", ".bin")
        if depth <= MAX_ZIP_DEPTH:
            scan_blob(state, f"{relpath}#data-uri-{n}", f"embedded{ext}", blob, depth + 1)
        body = m.group(2)
        return m.group(0)[: len(m.group(0)) - len(body)] + re.sub(r"[^\n]", " ", body)
    return _DATA_URI.sub(repl, text)


def scan_blob(state: State, relpath: str, name: str, data: bytes, depth: int = 0) -> None:
    if data.startswith(PNG_SIG):
        _count(state, "png"); scan_png(state, relpath, data)
    elif data[:3] == b"\xff\xd8\xff":
        _count(state, "jpeg"); scan_jpeg(state, relpath, data)
    elif data[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
        _count(state, "zip"); scan_zip(state, relpath, data, depth)
    elif data[:5] == b"%PDF-":
        _count(state, "pdf"); scan_pdf(state, relpath, data)
    elif is_text(name, data):
        _count(state, "text")
        scan_text(state, relpath, _scan_data_uris(state, relpath, decode_text(data), depth))
    else:
        _count(state, "binary"); scan_strings(state, relpath, data)


# ----------------------------------------------------------------------------
# walk
# ----------------------------------------------------------------------------
def walk(root: Path, excludes: list, skip_files: set):
    names = {e for e in excludes if "/" not in e.replace("\\", "/")}
    rels = {e.replace("\\", "/").strip("/") for e in excludes if "/" in e.replace("\\", "/")}
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        keep = []
        for dn in sorted(dirnames):
            rel = (d / dn).relative_to(root).as_posix()
            if dn in names or rel in rels:
                continue
            keep.append(dn)
            yield "dir", d / dn, rel
        dirnames[:] = keep
        for fn in sorted(filenames):
            p = d / fn
            try:
                if p.resolve() in skip_files:
                    continue
            except OSError:
                pass
            yield "file", p, p.relative_to(root).as_posix()


def run(root: Path, rules: list, allows: list, excludes: list, skip_files: set) -> State:
    st = State(rules=rules, allows=allows)
    for kind, p, rel in walk(root, excludes, skip_files):
        scan_text(st, f"{rel}#name", p.name)
        if kind == "dir":
            continue
        st.files += 1
        try:
            size = p.stat().st_size
            if size > MAX_FILE_BYTES:
                st.errors.append(f"{rel}: larger than {MAX_FILE_BYTES} bytes, not scanned")
                continue
            data = p.read_bytes()
        except OSError as e:
            st.errors.append(f"{rel}: cannot read ({e.strerror or e})")
            continue
        try:
            scan_blob(st, rel, p.name, data)
        except Exception as e:  # never let one odd file stop the scan
            st.errors.append(f"{rel}: scanner error {type(e).__name__}: {e}")
    return st


def _dedupe(hits: list) -> list:
    seen, out = set(), []
    for h in hits:
        k = (h.path, h.line, h.rule, h.col, h.context)
        if k not in seen:
            seen.add(k); out.append(h)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Scan a folder for personal data before publishing it.")
    ap.add_argument("root", type=Path, help="folder to scan")
    ap.add_argument("--denylist", type=Path, required=True, help="denylist file (see config/denylist.example.txt)")
    ap.add_argument("--json", type=Path, help="also write a JSON report here (values masked)")
    ap.add_argument("--exclude-dir", action="append", default=[], metavar="NAME",
                    help="folder name to skip at any depth, or a repo-relative path with '/'; "
                         "added to the defaults " + ", ".join(DEFAULT_EXCLUDES))
    ap.add_argument("--no-builtin", action="store_true", help="turn off the built-in rules")
    a = ap.parse_args(argv)

    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError):
            pass

    root = a.root.resolve()
    if not root.is_dir():
        print(f"error: {a.root} is not a folder", file=sys.stderr)
        return 2
    try:
        rules, allows = load_denylist(a.denylist)
    except (OSError, ValueError) as e:
        print(f"error: denylist: {e}", file=sys.stderr)
        return 2
    if not a.no_builtin:
        rules += builtin_rules()
    # never scan the denylist itself, nor the shipped example denylist (its sample lines are placeholders by design)
    skip = {a.denylist.resolve(), (root / "config" / "denylist.example.txt").resolve()}
    if a.json:
        skip.add(a.json.resolve())

    st = run(root, rules, allows, list(DEFAULT_EXCLUDES) + a.exclude_dir, skip)
    hits = _dedupe(st.hits)

    for h in hits:
        print(f"{h.path}:{h.line}: [{h.rule}] {h.context}")
    for e in st.errors:
        print(f"ERROR {mask_text(e)}", file=sys.stderr)

    per_rule: dict = {}
    for h in hits:
        per_rule[h.rule] = per_rule.get(h.rule, 0) + 1
    print("---")
    print(f"files scanned: {st.files}")
    print("surfaces: " + (", ".join(f"{k}={v}" for k, v in sorted(st.surfaces.items())) or "none"))
    print("hits per rule: " + (", ".join(f"{k}={v}" for k, v in sorted(per_rule.items())) or "none"))
    print(f"errors: {len(st.errors)}")
    verdict = "HITS" if hits else ("ERRORS" if st.errors else "CLEAN")
    print(f"VERDICT {verdict}")

    if a.json:
        report = {
            "root": root.name, "files_scanned": st.files, "surfaces": st.surfaces,
            "hits_per_rule": per_rule, "errors": [mask_text(e) for e in st.errors],
            "verdict": verdict,
            "hits": [{"path": h.path, "line": h.line, "rule": h.rule, "context": h.context} for h in hits],
        }
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if st.errors:
        return 2
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
