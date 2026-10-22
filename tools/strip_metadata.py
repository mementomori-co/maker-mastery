#!/usr/bin/env python3
"""strip_metadata.py - remove personal metadata from images and 3MF/ZIP files.

Standard library only (Python 3.12+).

Usage:
    python tools/strip_metadata.py FILE [FILE ...] [--dry-run] [--in-place] [-o OUT]

PNG    removes tEXt, zTXt, iTXt, tIME and eXIf chunks. Image data is untouched.
JPEG   removes APP1 (EXIF / XMP), APP13 (IPTC / Photoshop) and COM segments.
       APP0 (JFIF) and APP2 (ICC colour profile) are kept.
ZIP / 3MF (.zip .3mf and any other ZIP container):
       in every 3D/*.model part (3D/3dmodel.model and 3D/Objects/*.model) the
       <metadata name="..."> entries Title, Designer, DesignerUserId,
       Description, Copyright, LicenseTerms, CreationDate and ModificationDate
       are removed; in Metadata/*.config every absolute path (drive-letter paths and
       macOS / Linux home-folder paths) is cut down to its last file or folder name; PNG and JPEG
       members (thumbnails) are stripped as above. Every other member is copied
       byte for byte.

Output: a new file "<name>.stripped<ext>" beside the input (or -o OUT).
The input file is only changed when --in-place is given.
--dry-run lists what would be removed and writes nothing.
Exit code: 0 done (or nothing to strip), 2 on errors.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"
PNG_DROP = {b"tEXt", b"zTXt", b"iTXt", b"tIME", b"eXIf"}
JPEG_DROP = {0xE1: "APP1", 0xED: "APP13", 0xFE: "COM"}
MODEL_KEYS = ("Title", "Designer", "DesignerUserId", "Description", "Copyright",
              "LicenseTerms", "CreationDate", "ModificationDate")
_MODEL_META_RE = re.compile(
    r"[ \t]*<metadata\b[^>]*\bname\s*=\s*[\"'](?:" + "|".join(MODEL_KEYS) + r")[\"'][^>]*?"
    r"(?:/>|>.*?</metadata\s*>)[ \t]*(?:\r?\n)?",
    re.S)
# Absolute paths inside config text (XML attributes, JSON strings, INI values).
# JSON-escaped (doubled) backslashes are covered as well.
_PATH_RE = re.compile(
    r"(?:\b[A-Za-z]:(?:\\\\|\\|/)|(?<![\w.])/(?:Users|home|mnt|Volumes|media)/)"
    r"[^\"'<>|\r\n,;]*")


def strip_png(data: bytes) -> tuple[bytes, list]:
    if not data.startswith(PNG_SIG):
        raise ValueError("not a PNG")
    out, removed, pos = bytearray(PNG_SIG), [], 8
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG chunk")
        if ctype in PNG_DROP:
            removed.append(f"PNG {ctype.decode('latin-1')} ({length} bytes)")
        else:
            out += data[pos:end]
        pos = end
        if ctype == b"IEND":
            break
    if pos < len(data):
        removed.append(f"PNG data after IEND ({len(data) - pos} bytes)")
    return bytes(out), removed


def strip_jpeg(data: bytes) -> tuple[bytes, list]:
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    out, removed, pos = bytearray(b"\xff\xd8"), [], 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"bad JPEG marker at byte {pos}")
        marker = data[pos + 1]
        if marker == 0xFF:          # fill byte
            pos += 1
            continue
        if 0xD0 <= marker <= 0xD7 or marker == 0x01:
            out += data[pos:pos + 2]; pos += 2
            continue
        if marker == 0xDA or marker == 0xD9:   # start of scan / end: copy the rest
            out += data[pos:]
            return bytes(out), removed
        seglen = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        end = pos + 2 + seglen
        if marker in JPEG_DROP:
            removed.append(f"JPEG {JPEG_DROP[marker]} ({seglen} bytes)")
        else:
            out += data[pos:end]
        pos = end
    out += data[pos:]
    return bytes(out), removed


def _shorten_path(m: re.Match) -> str:
    p = m.group(0).rstrip(" \\/")
    tail = re.split(r"(?:\\\\|\\|/)", p)[-1]
    return tail


def strip_member(name: str, data: bytes) -> tuple[bytes, list]:
    low = name.lower()
    if data.startswith(PNG_SIG):
        return strip_png(data)
    if data[:3] == b"\xff\xd8\xff":
        return strip_jpeg(data)
    if low.startswith("3d/") and low.endswith(".model"):
        text = data.decode("utf-8")
        found = [re.search(r"name\s*=\s*[\"']([^\"']+)", m.group(0)).group(1)
                 for m in _MODEL_META_RE.finditer(text)]
        if not found:
            return data, []
        return _MODEL_META_RE.sub("", text).encode("utf-8"), [f"metadata {k}" for k in found]
    if low.startswith("metadata/") and low.endswith(".config"):
        text = data.decode("utf-8", errors="surrogateescape")
        hits = len(_PATH_RE.findall(text))
        if not hits:
            return data, []
        new = _PATH_RE.sub(_shorten_path, text)
        return new.encode("utf-8", errors="surrogateescape"), [f"{hits} path(s) shortened"]
    return data, []


def strip_zip(data: bytes) -> tuple[bytes, list]:
    removed = []
    src = zipfile.ZipFile(io.BytesIO(data))
    buf = io.BytesIO()
    with src, zipfile.ZipFile(buf, "w") as dst:
        for info in src.infolist():
            blob = src.read(info)
            if not info.is_dir():
                new, what = strip_member(info.filename, blob)
                removed += [f"{info.filename}: {w}" for w in what]
                blob = new
            ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            ni.compress_type = info.compress_type
            ni.external_attr = info.external_attr
            ni.create_system = info.create_system
            dst.writestr(ni, blob)
        dst.comment = b""
        if src.comment:
            removed.append("ZIP archive comment")
    return buf.getvalue(), removed


def strip_bytes(data: bytes) -> tuple[bytes, list]:
    if data.startswith(PNG_SIG):
        return strip_png(data)
    if data[:3] == b"\xff\xd8\xff":
        return strip_jpeg(data)
    if data[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
        return strip_zip(data)
    raise ValueError("unsupported type (PNG, JPEG, ZIP/3MF only)")


def _atomic_write(path: Path, data: bytes) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Remove personal metadata from PNG, JPEG and ZIP/3MF files.")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("-o", "--output", type=Path, help="output file (only with one input)")
    ap.add_argument("--in-place", action="store_true", help="overwrite the input file")
    ap.add_argument("--dry-run", action="store_true", help="list what would be removed, write nothing")
    a = ap.parse_args(argv)
    if a.output and (len(a.files) != 1 or a.in_place):
        ap.error("-o needs exactly one input and cannot be combined with --in-place")
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="backslashreplace")
        except (AttributeError, ValueError):
            pass

    errors = 0
    for f in a.files:
        try:
            data = f.read_bytes()
            new, removed = strip_bytes(data)
        except (OSError, ValueError, zipfile.BadZipFile, UnicodeDecodeError) as e:
            print(f"ERROR {f}: {e}", file=sys.stderr)
            errors += 1
            continue
        for r in removed:
            print(f"{f}: remove {r}")
        if not removed:
            print(f"{f}: nothing to strip")
        if a.dry_run:
            continue
        if a.in_place:
            if removed:
                _atomic_write(f, new)
                print(f"{f}: rewritten in place")
            continue
        out = a.output or f.with_name(f"{f.stem}.stripped{f.suffix}")
        _atomic_write(out, new)
        print(f"{f}: wrote {out}")
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
