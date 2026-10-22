"""Tests for tools/privacy_scan.py and tools/strip_metadata.py (unittest, stdlib only).

Run:  python -m unittest discover -s tools/tests -v
Every fixture is synthetic and built in a temporary folder.
"""
from __future__ import annotations

import contextlib
import io
import struct
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import privacy_scan  # noqa: E402
import strip_metadata  # noqa: E402

TERM = "zorblaxquent"          # synthetic private word used by every fixture
SECRET = "Q7xK2mP9" + "vL4tR8wN3bZ6yH1cF5"  # synthetic secret, must never be printed in full


def u(s: str) -> str:
    """Fixture strings carry a ~ so this source file stays clean under the scanner."""
    return s.replace("~", "")


def png_chunk(ctype: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF)


def make_png(extra: list[bytes]) -> bytes:
    ihdr = png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
    idat = png_chunk(b"IDAT", zlib.compress(b"\x00\x00"))
    return privacy_scan.PNG_SIG + ihdr + b"".join(extra) + idat + png_chunk(b"IEND", b"")


def make_jpeg(segments: list[tuple[int, bytes]]) -> bytes:
    out = b"\xff\xd8"
    for marker, body in segments:
        out += bytes([0xFF, marker]) + struct.pack(">H", len(body) + 2) + body
    sos = b"\xff\xda" + struct.pack(">H", 8) + b"\x01\x01\x00\x00\x3f\x00"
    return out + sos + b"\x12\x34\x56" + b"\xff\xd9"


def make_zip(members: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in members.items():
            z.writestr(name, data)
    return buf.getvalue()


def make_pdf(info: bytes, compressed_meta: bytes | None = None) -> bytes:
    objs = [b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
            b"2 0 obj << /Type /Pages /Kids [] /Count 0 >> endobj\n",
            b"3 0 obj " + info + b" endobj\n"]
    if compressed_meta is not None:
        z = zlib.compress(compressed_meta)
        objs.append(b"4 0 obj << /Length %d /Filter /FlateDecode >> stream\n" % len(z) + z + b"\nendstream endobj\n")
    return b"%PDF-1.7\n" + b"".join(objs) + b"trailer << /Root 1 0 R /Info 3 0 R >>\n%%EOF\n"


class ScanCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.root = base / "repo"
        self.root.mkdir()
        self.deny = base / "deny.txt"
        self.deny.write_text(f"# test list\n{TERM}\nre:\\bblorpville\\b\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel: str, data):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            p.write_text(data, encoding="utf-8")
        else:
            p.write_bytes(data)
        return p

    def scan(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = privacy_scan.main([str(self.root), "--denylist", str(self.deny), *extra])
        return code, out.getvalue(), err.getvalue()

    def hit_lines(self, text):
        return [l for l in text.splitlines() if ": [" in l]

    def assertCaught(self, prefix: str, rule: str = "deny:L2"):
        code, out, err = self.scan()
        lines = [l for l in self.hit_lines(out) if l.startswith(prefix) and f"[{rule}]" in l]
        self.assertTrue(lines, f"no [{rule}] hit starting with {prefix!r}\n{out}\n{err}")
        self.assertEqual(code, 1, out + err)
        self.assertIn("VERDICT HITS", out)
        return out

    # --- every scan surface ------------------------------------------------
    def test_text_contents(self):
        self.write("docs/a.md", f"line one\nmade by {TERM.upper()} here\n")
        out = self.assertCaught("docs/a.md:2:")
        self.assertIn("ZORBLAXQUENT", out)

    def test_regex_rule(self):
        self.write("b.txt", "lives in Blorpville now\n")
        self.assertCaught("b.txt:1:", "deny:L3")

    def test_utf16_text(self):
        self.write("u16.txt", ("\ufeffhello " + TERM).encode("utf-16-le"))
        self.assertCaught("u16.txt:1:")

    def test_file_name(self):
        self.write(f"photos/{TERM}_desk.txt", "nothing here\n")
        self.assertCaught(f"photos/{TERM}_desk.txt#name")

    def test_folder_name(self):
        self.write(f"{TERM}-stuff/x.txt", "nothing\n")
        self.assertCaught(f"{TERM}-stuff#name")

    def test_png_text_chunks(self):
        self.write("img/t.png", make_png([png_chunk(b"tEXt", b"Author\x00" + TERM.encode())]))
        self.write("img/z.png", make_png([png_chunk(b"zTXt", b"Comment\x00\x00" + zlib.compress(TERM.encode()))]))
        self.write("img/i.png", make_png([png_chunk(b"iTXt", b"Description\x00\x01\x00en\x00\x00" + zlib.compress(TERM.encode()))]))
        self.write("img/e.png", make_png([png_chunk(b"eXIf", b"MM\x00\x2a\x00\x00\x00\x08Artist " + TERM.encode() + b"\x00")]))
        code, out, _ = self.scan()
        for name, chunk in (("t", "tEXt"), ("z", "zTXt"), ("i", "iTXt"), ("e", "eXIf")):
            self.assertIn(f"img/{name}.png#{chunk}:", out, out)

    def test_jpeg_exif_xmp_com(self):
        exif = b"Exif\x00\x00MM\x00\x2a\x00\x00\x00\x08" + b"Artist\x00" + TERM.encode() + b"\x00"
        xp = b"Exif\x00\x00II\x2a\x00" + TERM.encode("utf-16-le") + b"\x00\x00"
        xmp = (b"http://ns.adobe.com/xap/1.0/\x00<x:xmpmeta><dc:creator>" + TERM.encode()
               + b"</dc:creator></x:xmpmeta>")
        self.write("a.jpg", make_jpeg([(0xE0, b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"), (0xE1, exif)]))
        self.write("b.jpg", make_jpeg([(0xE1, xp)]))
        self.write("c.jpg", make_jpeg([(0xE1, xmp)]))
        self.write("d.jpg", make_jpeg([(0xFE, b"shot by " + TERM.encode())]))
        code, out, _ = self.scan()
        self.assertIn("a.jpg#APP1-Exif:", out)
        self.assertIn("b.jpg#APP1-Exif:", out)   # UTF-16LE (Windows XP* tags)
        self.assertIn("c.jpg#APP1-XMP:", out)
        self.assertIn("d.jpg#COM:", out)

    def test_zip_3mf_members(self):
        model = f'<model><metadata name="Designer">{TERM}</metadata></model>'
        thumb = make_png([png_chunk(b"tEXt", b"Author\x00" + TERM.encode())])
        inner = make_zip({"deep/notes.txt": f"hello {TERM}"})
        self.write("p.3mf", make_zip({"3D/3dmodel.model": model, "Metadata/plate_1.png": thumb,
                                      f"Metadata/{TERM}.config": "x", "nested.zip": inner}))
        self.write("d.docx", make_zip({"docProps/core.xml": f"<dc:creator>{TERM}</dc:creator>"}))
        code, out, _ = self.scan()
        self.assertIn("p.3mf!3D/3dmodel.model:1:", out)
        self.assertIn("p.3mf!Metadata/plate_1.png#tEXt:", out)
        self.assertIn(f"p.3mf!Metadata/{TERM}.config#name:", out)
        self.assertIn("p.3mf!nested.zip!deep/notes.txt:1:", out)
        self.assertIn("d.docx!docProps/core.xml:1:", out)

    def test_pdf_metadata(self):
        hexname = TERM.encode().hex().upper().encode()
        self.write("a.pdf", make_pdf(b"<< /Author (" + TERM.encode() + b") /Producer (x) >>"))
        self.write("b.pdf", make_pdf(b"<< /Title <" + hexname + b"> >>"))
        self.write("c.pdf", make_pdf(b"<< /Producer (x) >>",
                                     b"<x:xmpmeta><rdf:li>" + TERM.encode() + b"</rdf:li></x:xmpmeta>"))
        code, out, _ = self.scan()
        self.assertIn("a.pdf#pdf/Author:", out)
        self.assertIn("b.pdf#pdf/Title:", out)
        self.assertIn("c.pdf#pdf-stream/XMP:", out)

    def test_binary_strings(self):
        self.write("blob.bin", b"\x00\x01\x02" + TERM.encode() + b"\x00\xff\x00" + ("x " + TERM).encode("utf-16-le") + b"\x00\x00\x9c")
        code, out, _ = self.scan()
        lines = [l for l in self.hit_lines(out) if l.startswith("blob.bin:")]
        self.assertEqual(len(lines), 2, out)  # one ASCII string, one UTF-16LE string

    def test_binary_stl_header(self):
        header = (b"solid " + TERM.encode()).ljust(80, b"\x00")
        self.write("part.stl", header + struct.pack("<I", 0))
        self.assertCaught("part.stl:")

    def test_svg_data_uri(self):
        import base64
        png = make_png([png_chunk(b"tEXt", b"Author\x00" + TERM.encode())])
        noise = base64.b64encode(bytes(range(256)) * 4).decode()
        self.write("logo.svg", '<svg><image href="data:image/png;base64,' + base64.b64encode(png).decode()
                   + '"/><image href="data:image/png;base64,' + noise + '"/></svg>\n')
        code, out, _ = self.scan()
        lines = self.hit_lines(out)
        self.assertTrue(any(l.startswith("logo.svg#data-uri-1#tEXt:") for l in lines), out)
        self.assertEqual(len(lines), 1, out)   # the base64 text itself raises nothing

    def test_email_false_positives(self):
        self.write("links.md", "see profiles/Bambu%20PLA%20Basic%20@base.json and icon@2x.png\n")
        code, out, _ = self.scan()
        self.assertEqual(code, 0, out)

    # --- built-in rules -----------------------------------------------------
    def test_builtin_rules(self):
        self.write("cfg.txt", u("\n".join([
            r"exe = C:\Us~ers\somebody\AppData\x.exe",
            "mac = /Us~ers/somebody/Desktop",
            "contact me at someone~@mailhost.net",
            "fine: dev~@example.com and 1234+me~@users.noreply.github.com",
            "printer at 192.168~.1.50 and cgnat 100.101~.5.6 and 172.20~.0.1",
            "public 8.8.8.8 is fine and version 10.2 is fine",
            f"api_key = {SECRET}",
            "access_code: 8642~9753",
            "serial 01P09C~123456789 found",
            r"placeholder C:\Us~ers\<you>\x is fine",
        ]) + "\n"))
        code, out, _ = self.scan()
        rules = {}
        for l in self.hit_lines(out):
            r = l.split("[", 1)[1].split("]", 1)[0]
            rules.setdefault(r, []).append(l)
        self.assertEqual(len(rules.get("userpath", [])), 2, out)
        self.assertEqual(len(rules.get("email", [])), 1, out)
        self.assertEqual(len(rules.get("private-ip", [])), 3, out)
        self.assertEqual(len(rules.get("secret", [])), 2, out)
        self.assertEqual(len(rules.get("printer-serial", [])), 1, out)
        self.assertNotIn(SECRET, out)
        self.assertNotIn("86429753", out)

    def test_secret_never_printed_in_json(self):
        self.write("s.env", f"TOKEN={SECRET}\n")
        rep = Path(self._tmp.name) / "rep.json"
        code, out, _ = self.scan("--json", str(rep))
        self.assertEqual(code, 1)
        self.assertNotIn(SECRET, out)
        self.assertNotIn(SECRET, rep.read_text(encoding="utf-8"))

    def test_no_builtin(self):
        self.write("x.txt", u("someone~@mailhost.net 192.168~.0.2\n"))
        code, out, _ = self.scan("--no-builtin")
        self.assertEqual(code, 0, out)

    # --- allow, excludes, clean ---------------------------------------------
    def test_allow_line(self):
        self.deny.write_text(f"{TERM}\nallow: README.md | Created by @{TERM}\n", encoding="utf-8")
        self.write("README.md", f"Credits\nCreated by @{TERM}\n")
        code, out, _ = self.scan()
        self.assertEqual(code, 0, out)
        self.assertIn("VERDICT CLEAN", out)
        # the same phrase in another file is still a hit
        self.write("other.md", f"Created by @{TERM}\n")
        code, out, _ = self.scan()
        self.assertEqual(code, 1, out)
        self.assertIn("other.md:1:", out)
        self.assertNotIn("README.md:", out)
        # and another mention in the allowed file is still a hit
        self.write("README.md", f"Created by @{TERM}\nalso {TERM}\n")
        code, out, _ = self.scan()
        self.assertIn("README.md:2:", out)
        self.assertNotIn("README.md:1:", out)

    def test_default_and_extra_excludes(self):
        for d in (".git", ".venv", "work", "dist", "private"):
            self.write(f"{d}/x.txt", TERM)
        code, out, _ = self.scan("--exclude-dir", "private")
        self.assertEqual(code, 0, out)

    def test_clean_tree_exit_zero(self):
        self.write("README.md", u("# A clean project\nUse C:\\Us~ers\\<you>\\ and you~@example.com.\n"))
        self.write("img/p.png", make_png([]))
        self.write("m.3mf", make_zip({"3D/3dmodel.model": "<model/>"}))
        code, out, err = self.scan()
        self.assertEqual(code, 0, out + err)
        self.assertIn("VERDICT CLEAN", out)

    def test_bad_regex_exit_two(self):
        self.deny.write_text("re:([unclosed\n", encoding="utf-8")
        code, _, err = self.scan()
        self.assertEqual(code, 2)
        self.assertIn("bad regex", err)


class StripCase(unittest.TestCase):
    def test_strip_png(self):
        src = make_png([png_chunk(b"tEXt", b"Author\x00" + TERM.encode()), png_chunk(b"tIME", b"\x07\xe0\x01\x01\x00\x00\x00")])
        new, removed = strip_metadata.strip_png(src)
        self.assertEqual(len(removed), 2)
        self.assertNotIn(TERM.encode(), new)
        self.assertIn(b"IDAT", new)

    def test_strip_jpeg(self):
        src = make_jpeg([(0xE0, b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"),
                         (0xE1, b"Exif\x00\x00" + TERM.encode()), (0xED, b"Photoshop 3.0\x00" + TERM.encode()),
                         (0xFE, TERM.encode()), (0xE2, b"ICC_PROFILE\x00keep")])
        new, removed = strip_metadata.strip_jpeg(src)
        self.assertEqual(len(removed), 3)
        self.assertNotIn(TERM.encode(), new)
        self.assertIn(b"ICC_PROFILE", new)
        self.assertTrue(new.endswith(b"\xff\xd9"))

    def test_strip_3mf_and_rescan(self):
        model = ('<model>\n <metadata name="Application">Slicer</metadata>\n'
                 f' <metadata name="Designer">{TERM}</metadata>\n'
                 ' <metadata name="CreationDate">2020-01-01</metadata>\n'
                 ' <resources/>\n</model>\n')
        cfg = u('<config><metadata key="source_file" value="C:\\Us~ers\\somebody\\parts\\cube.stl"/></config>')
        thumb = make_png([png_chunk(b"tEXt", b"Author\x00" + TERM.encode())])
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "repo"; root.mkdir()
            src = root / "cube.3mf"
            src.write_bytes(make_zip({"3D/3dmodel.model": model, "Metadata/model_settings.config": cfg,
                                      "Metadata/plate_1.png": thumb}))
            before = src.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(strip_metadata.main([str(src), "--dry-run"]), 0)
                self.assertFalse((root / "cube.stripped.3mf").exists())
                self.assertEqual(strip_metadata.main([str(src)]), 0)
            self.assertEqual(src.read_bytes(), before)          # input untouched
            out = root / "cube.stripped.3mf"
            with zipfile.ZipFile(out) as z:
                m = z.read("3D/3dmodel.model").decode()
                c = z.read("Metadata/model_settings.config").decode()
            self.assertIn("Application", m)
            self.assertNotIn("Designer", m)
            self.assertNotIn("CreationDate", m)
            self.assertIn('value="cube.stl"', c)
            src.rename(Path(t) / "orig.3mf")                     # keep only the stripped copy in the tree
            deny = Path(t) / "deny.txt"
            deny.write_text(TERM + "\n", encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                code = privacy_scan.main([str(root), "--denylist", str(deny)])
            self.assertEqual(code, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main()
