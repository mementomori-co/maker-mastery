"""Copy a PNG while dropping metadata chunks (standard library only).

Removes text (tEXt, zTXt, iTXt), time (tIME) and EXIF (eXIf) chunks, so no
creation tool, timestamp or camera data ships with the brand images. Pixel
data is copied byte for byte.

Usage:
    python strip_png_metadata.py SOURCE.png DEST.png [--list]
"""
import argparse
import struct
import sys
import zlib

PNG_SIG = b"\x89PNG\r\n\x1a\n"
DROP = {b"tEXt", b"zTXt", b"iTXt", b"tIME", b"eXIf"}


def read_chunks(data):
    if data[:8] != PNG_SIG:
        raise ValueError("not a PNG file")
    pos = 8
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        (crc,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise ValueError("bad CRC in chunk %r" % ctype)
        yield ctype, body
        pos += 12 + length
        if ctype == b"IEND":
            break


def write_chunk(out, ctype, body):
    out.write(struct.pack(">I", len(body)))
    out.write(ctype)
    out.write(body)
    out.write(struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source")
    ap.add_argument("dest")
    ap.add_argument("--list", action="store_true", help="print kept and dropped chunk types")
    args = ap.parse_args(argv)
    with open(args.source, "rb") as f:
        data = f.read()
    kept, dropped = [], []
    with open(args.dest, "wb") as out:
        out.write(PNG_SIG)
        for ctype, body in read_chunks(data):
            if ctype in DROP:
                dropped.append(ctype.decode("ascii"))
                continue
            kept.append(ctype.decode("ascii"))
            write_chunk(out, ctype, body)
    if args.list:
        print("kept:", " ".join(sorted(set(kept))))
        print("dropped:", " ".join(dropped) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
