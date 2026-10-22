"""Set RGB to 0 under fully transparent pixels of an RGBA PNG (standard library only).

Image editors often leave the old background colour hidden under pixels whose
alpha is 0. It is invisible in browsers but shows in viewers that ignore alpha
and makes the file larger. This rewrites the PNG with RGB = 0 wherever
alpha == 0, then checks that every pixel with alpha > 0 is byte-identical to
the input. Only IHDR, IDAT and IEND are written (no metadata chunks).

Usage:
    python clear_transparent_rgb.py IN.png OUT.png     (OUT may equal IN)
"""
import argparse
import struct
import sys
import zlib

SIG = b"\x89PNG\r\n\x1a\n"


def decode(path):
    data = open(path, "rb").read()
    if data[:8] != SIG:
        raise ValueError("not a PNG: %s" % path)
    pos, idat, ihdr = 8, [], None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        t = data[pos + 4:pos + 8]
        if t == b"IHDR":
            ihdr = data[pos + 8:pos + 8 + ln]
        elif t == b"IDAT":
            idat.append(data[pos + 8:pos + 8 + ln])
        elif t == b"IEND":
            break
        pos += 12 + ln
    w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", ihdr)
    if bd != 8 or ct != 6 or il:
        raise ValueError("expected 8-bit RGBA non-interlaced PNG: %s" % path)
    raw = zlib.decompress(b"".join(idat))
    stride, bpp = w * 4, 4
    prev = bytearray(stride)
    rows, p = [], 0
    for _ in range(h):
        f = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        rows.append(line)
        prev = line
    return w, h, rows


def _paeth(a, b, c):
    pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def encode(path, w, h, rows):
    """Write RGBA rows choosing, per row, the filter with the smallest sum of absolute values."""
    bpp = 4
    stride = w * 4
    prev = bytearray(stride)
    out = bytearray()
    for line in rows:
        cands = []
        f0 = bytes(line)
        f1 = bytes(line[:bpp]) + bytes((line[i] - line[i - bpp]) & 255 for i in range(bpp, stride))
        f2 = bytes((line[i] - prev[i]) & 255 for i in range(stride))
        f4 = bytes((line[i] - _paeth(line[i - bpp] if i >= bpp else 0, prev[i],
                                     prev[i - bpp] if i >= bpp else 0)) & 255 for i in range(stride))
        for ft, body in ((0, f0), (1, f1), (2, f2), (4, f4)):
            cost = sum(v if v < 128 else 256 - v for v in body)
            cands.append((cost, ft, body))
        _, ft, body = min(cands)
        out.append(ft)
        out += body
        prev = line

    def chunk(t, b):
        return struct.pack(">I", len(b)) + t + b + struct.pack(">I", zlib.crc32(t + b) & 0xFFFFFFFF)
    png = SIG + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(out), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("dest")
    args = ap.parse_args(argv)
    w, h, rows = decode(args.src)
    cleared = 0
    new_rows = []
    for line in rows:
        nl = bytearray(line)
        for i in range(0, len(nl), 4):
            if nl[i + 3] == 0 and (nl[i] or nl[i + 1] or nl[i + 2]):
                nl[i] = nl[i + 1] = nl[i + 2] = 0
                cleared += 1
        new_rows.append(nl)
    encode(args.dest, w, h, new_rows)
    # verify: same size, same alpha everywhere, alpha>0 pixels byte-identical, alpha==0 pixels all zero
    w2, h2, rows2 = decode(args.dest)
    assert (w2, h2) == (w, h)
    for a_row, b_row in zip(rows, rows2):
        for i in range(0, len(a_row), 4):
            if a_row[i + 3]:
                assert a_row[i:i + 4] == b_row[i:i + 4], "visible pixel changed"
            else:
                assert b_row[i:i + 4] == b"\x00\x00\x00\x00", "transparent pixel not cleared"
    print("%s: %dx%d, %d hidden pixels cleared, visible pixels identical" % (args.dest, w, h, cleared))
    return 0


if __name__ == "__main__":
    sys.exit(main())
