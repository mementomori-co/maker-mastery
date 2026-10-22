"""Build the crest-family render pages (standard library only).

Writes HTML render pages into src/ for:
  family-strip-dark.html / family-strip-light.html  four crests + one-word captions,
                                                    transparent background, 2x export
  org-avatar-500.html                               parent crest centred on #0A0A0A
  crest-parent-sign-off.html                        parent crest, 2x of 160 px display
  crest-streaming-icon.html / crest-apparel-icon.html  2x of 40 px display

Headless Chrome turns each page into a PNG (see README.md in this folder);
strip_png_metadata.py then copies it into assets/brand/.

Usage:
    python build_family.py --fonts FONT_DIR [--brand-dir ..]
"""
import argparse
import math
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ttf_outlines import Font  # noqa: E402
from build_brand import BLACK, BONE, FONT_FILES, Run, text_svg, png_size  # noqa: E402

# 2x export scale for README images (display size = pixel size / SCALE)
SCALE = 2

FAMILY = [  # (crest file stem, caption)
    ("crest-printing", "MAKE"),
    ("crest-streaming", "STREAM"),
    ("crest-apparel", "CREATE"),
    ("crest-parent", "MEMENTO MORI"),
]
CAPTION_COLOUR = {"dark": BONE, "light": BLACK}

PAGE = """<!doctype html>
<!-- Render source for %(png)s (%(W)dx%(H)d px). Built by build_family.py; edit that, not this file.
     %(note)s
     Render: chrome --headless=new --hide-scrollbars --force-device-scale-factor=1
             --default-background-color=00000000 --window-size=%(W)d,%(H)d --screenshot=%(png)s %(name)s -->
<html><head><meta charset="utf-8"><title>%(png)s source</title>
<style>
@font-face{font-family:'Oswald';src:url('fonts/Oswald-VariableFont_wght.ttf') format('truetype');font-weight:200 700}
html,body{margin:0;padding:0;background:%(bg)s;overflow:hidden}
svg{display:block}
</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="%(W)d" height="%(H)d" viewBox="0 0 %(W)d %(H)d">
<defs><filter id="halo" x="-5%%" y="-5%%" width="110%%" height="110%%" color-interpolation-filters="sRGB">
<feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d"/>
<feGaussianBlur in="d" stdDeviation="1.5" result="b"/>
<feFlood flood-color="#0A0A0A" flood-opacity="0.9"/>
<feComposite in2="b" operator="in" result="h"/>
<feMerge><feMergeNode in="h"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
%(inner)s</svg>
</body></html>
"""


def image(href, x, y, w, h, halo=False):
    """halo=True draws a thin dark outline behind the crest (filter #halo) so its white
    lettering stays readable on a white page; on a dark page the outline is invisible."""
    f = ' filter="url(#halo)"' if halo else ""
    return '<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" href="%s"%s/>\n' % (x, y, w, h, href, f)


def write_page(src, name, W, H, bg, inner, note):
    with open(os.path.join(src, name + ".html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(PAGE % dict(png=name + ".png", name=name + ".html", W=W, H=H, bg=bg, inner=inner, note=note))
    print("%s.html  %dx%d" % (name, W, H))


def alpha_mask(path, threshold=8):
    """Decode an 8-bit RGBA, non-interlaced PNG (stdlib) and return (w, h, rows of alpha>threshold)."""
    data = open(path, "rb").read()
    pos, idat, ihdr = 8, b"", None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        t = data[pos + 4:pos + 8]
        if t == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", data[pos + 8:pos + 21])
        elif t == b"IDAT":
            idat += data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
    w, h, bd, ct, _, _, il = ihdr
    if bd != 8 or ct != 6 or il:
        raise ValueError("expected 8-bit RGBA non-interlaced PNG")
    raw = zlib.decompress(idat)
    stride, bpp = w * 4, 4
    prev = bytearray(stride)
    rows, p = [], 0
    for _ in range(h):
        f = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                pr = a
            elif f == 2:
                pr = b
            elif f == 3:
                pr = (a + b) >> 1
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
            else:
                pr = 0
            line[i] = (line[i] + pr) & 255
        rows.append(bytes(line[3::4]))
        prev = line
    return w, h, [[v > threshold for v in r] for r in rows]


def max_radius(w, h, mask):
    """Largest distance from the image centre to any visible pixel corner, in source pixels."""
    cx, cy = w / 2, h / 2
    r2 = 0.0
    for y, row in enumerate(mask):
        for x, on in enumerate(row):
            if on:
                dx = max(abs(x - cx), abs(x + 1 - cx))
                dy = max(abs(y - cy), abs(y + 1 - cy))
                r2 = max(r2, dx * dx + dy * dy)
    return math.sqrt(r2)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build crest-family render pages.")
    ap.add_argument("--fonts", required=True, help="folder holding Oswald-VariableFont_wght.ttf")
    ap.add_argument("--brand-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = ap.parse_args(argv)
    brand = os.path.abspath(args.brand_dir)
    src = os.path.join(brand, "src")
    oswald = Font(os.path.join(args.fonts, FONT_FILES["oswald"][1]))

    # ---- family strip: 4 crests, 120 px display width each, exported at 2x ----
    cell = 120 * SCALE
    gap = 28 * SCALE
    pad = 4 * SCALE
    cap_size = 15 * SCALE
    cap_track = 0.12
    heights = []
    for stem, _ in FAMILY:
        w, h = png_size(os.path.join(brand, stem + "-1024.png"))
        heights.append(cell * h / w)
    crest_h = max(heights)
    W = 2 * pad + 4 * cell + 3 * gap
    base_y = pad + crest_h + 26 * SCALE  # caption baseline
    H = int(round(base_y + 6 * SCALE))
    for theme in ("dark", "light"):
        inner, runs = [], []
        for i, (stem, cap) in enumerate(FAMILY):
            x = pad + i * (cell + gap)
            ch = heights[i]
            inner.append(image("../%s-1024.png" % stem, x, pad + crest_h - ch, cell, ch, halo=True))
            cw = oswald.measure(cap, cap_size, cap_track)
            runs.append(Run(cap, "oswald", cap_size, CAPTION_COLOUR[theme], x + (cell - cw) / 2, base_y, cap_track))
        write_page(src, "family-strip-" + theme, W, H, "transparent", "".join(inner) + text_svg(runs),
                   "Display at %d px wide (2x export). Transparent background; captions for GitHub %s mode."
                   % (W // SCALE, theme))

    # ---- org avatar: whole parent crest inside the inscribed circle of a 500 px square ----
    S = 500
    margin = 10  # px between the crest's farthest pixel and the circle edge
    w, h, mask = alpha_mask(os.path.join(brand, "crest-parent-512.png"))
    rmax = max_radius(w, h, mask)
    k = (S / 2 - margin) / rmax
    cw, ch = w * k, h * k
    inner = '<rect width="%d" height="%d" fill="%s"/>\n' % (S, S, BLACK)
    inner += image("../crest-parent-1024.png", (S - cw) / 2, (S - ch) / 2, cw, ch)
    write_page(src, "org-avatar-500", S, S, BLACK, inner,
               "Crest scaled so its farthest visible pixel is %d px inside the inscribed circle "
               "(measured radius %.1f px at 512 wide; drawn %.0fx%.0f px)." % (margin, rmax, cw, ch))

    # ---- single crests for README use, transparent, 2x ----
    for name, stem, disp in (("crest-parent-sign-off", "crest-parent", 160),
                             ("crest-streaming-icon", "crest-streaming", 40),
                             ("crest-apparel-icon", "crest-apparel", 40)):
        w, h = png_size(os.path.join(brand, stem + "-1024.png"))
        PW = disp * SCALE
        # The sign-off gets the dark halo (white lettering on a white page) and a 4 px
        # inset so the halo is not clipped; the 40 px icons stay plain and full-bleed.
        halo = disp >= 100
        m = 4 if halo else 0
        cw = PW - 2 * m
        chh = cw * h / w
        PH = int(round(chh + 2 * m))
        write_page(src, name, PW, PH, "transparent",
                   image("../%s-1024.png" % stem, m, (PH - chh) / 2, cw, chh, halo),
                   "Display at %d px wide (2x export). Transparent background." % disp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
