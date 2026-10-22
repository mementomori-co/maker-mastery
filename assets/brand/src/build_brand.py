"""Build the brand banner sources (standard library only).

Writes, from one layout:
  src/banner-dark.html, src/banner-light.html, src/social-preview.html
      HTML pages that headless Chrome renders to the PNGs. Text uses @font-face
      with relative paths to src/fonts/ (the font files are NOT shipped; see
      src/README.md for where to get them).
  banner-dark.svg, banner-light.svg
      Self-contained SVGs: text converted to outlines, crest embedded as a
      base64 PNG. No font files are referenced.

Usage:
    python build_brand.py --fonts FONT_DIR [--brand-dir ..]

FONT_DIR must hold Oswald-VariableFont_wght.ttf, IBMPlexMono-Medium.ttf and
IBMPlexMono-SemiBold.ttf (all SIL OFL 1.1, Google Fonts / IBM Plex).
"""
import argparse
import base64
import html
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ttf_outlines import Font  # noqa: E402

BLACK = "#0A0A0A"
BONE = "#ECE6DA"
RED = "#D21F3C"
# Gold sampled from crest-printing-1024.png (median of warm, saturated opaque pixels):
GOLD_LIGHT = "#C1A07B"  # highlight gold, used on the dark background
GOLD_DARK = "#917254"   # body gold, used on the bone background

TITLE_A = "MEMENTO MORI"
TITLE_SEP = "·"
TITLE_B = "MAKER MASTERY"
# Subtitle (one sentence, set on two lines):
# "A Claude Code operating system for makers — 3D printing, CAD, electronics, rendering,
#  game dev and more. Research-backed, AI-checked, human-built."
TAG1 = "A Claude Code operating system for makers — 3D printing, CAD, electronics,"
TAG2A = "rendering, game dev and more. Research-backed, AI-checked, "
TAG2B = "human-built."

FONT_FILES = {
    "oswald": ("Oswald", "Oswald-VariableFont_wght.ttf", 400),
    "plex": ("IBM Plex Mono", "IBMPlexMono-Medium.ttf", 500),
    "plexsb": ("IBM Plex Mono", "IBMPlexMono-SemiBold.ttf", 600),
}

THEMES = {
    "dark": dict(bg=BLACK, glow="#1C1515", fg=BONE, fg2="#CFC8BB", gold=GOLD_LIGHT, red=RED, em=GOLD_LIGHT),
    "light": dict(bg=BONE, glow="#F7F3EB", fg=BLACK, fg2="#2A2724", gold=GOLD_DARK, red=RED, em=BLACK),
}


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


class Run:
    def __init__(self, text, font, size, color, x, y, tracking=0.0):
        self.text, self.font, self.size, self.color = text, font, size, color
        self.x, self.y, self.tracking = x, y, tracking


def layout(kind, fonts, theme, crest_aspect):
    """Return (W, H, crest_box, runs, rects)."""
    t = THEMES[theme]
    runs, rects = [], []
    if kind == "banner":
        W, H = 1600, 420
        ch = 352
        cw = ch * crest_aspect
        crest = (44, (H - ch) / 2, cw, ch)
        x0 = 44 + cw + 48
        avail = W - x0 - 56
        title_tr = 0.035
        size = 76
        sep_gap = 0.42  # em of space either side of the middle dot

        def title_w(sz):
            o = fonts["oswald"]
            return (o.measure(TITLE_A, sz, title_tr) + o.measure(TITLE_B, sz, title_tr)
                    + o.measure(TITLE_SEP, sz) + 2 * sep_gap * sz)
        while title_w(size) > avail and size > 40:
            size -= 1
        ty = 186
        _title_runs(runs, rects, fonts, t, x0, ty, size, title_tr, sep_gap)
        tw = title_w(size)
        rule_y = ty + 30
        rects.append((x0, rule_y, tw, 2, t["gold"]))
        rects.append((x0, rule_y - 2, 64, 6, t["red"]))
        tag = 25
        while max(fonts["plex"].measure(TAG1, tag),
                  fonts["plex"].measure(TAG2A, tag) + fonts["plexsb"].measure(TAG2B, tag)) > avail and tag > 14:
            tag -= 1
        y1 = rule_y + 58
        runs.append(Run(TAG1, "plex", tag, t["fg2"], x0, y1))
        y2 = y1 + tag * 1.6
        runs.append(Run(TAG2A, "plex", tag, t["fg2"], x0, y2))
        runs.append(Run(TAG2B, "plexsb", tag, t["em"], x0 + fonts["plex"].measure(TAG2A, tag), y2))
        return W, H, crest, runs, rects
    # social preview, 1280x640, everything centred inside an 80 px safe margin
    W, H = 1280, 640
    ch = 270
    cw = ch * crest_aspect
    top = 90  # content block is about 460 px tall: centred vertically in 640
    crest = ((W - cw) / 2, top, cw, ch)
    size, title_tr, sep_gap = 60, 0.035, 0.42
    o = fonts["oswald"]
    tw = (o.measure(TITLE_A, size, title_tr) + o.measure(TITLE_B, size, title_tr)
          + o.measure(TITLE_SEP, size) + 2 * sep_gap * size)
    x0 = (W - tw) / 2
    ty = top + ch + 76
    _title_runs(runs, rects, fonts, t, x0, ty, size, title_tr, sep_gap)
    rule_y = ty + 24
    rects.append(((W - tw) / 2, rule_y, tw, 2, t["gold"]))
    rects.append(((W - 64) / 2, rule_y - 2, 64, 6, t["red"]))
    tag = 23
    p, psb = fonts["plex"], fonts["plexsb"]
    while max(p.measure(TAG1, tag), p.measure(TAG2A, tag) + psb.measure(TAG2B, tag)) > W - 160 and tag > 14:
        tag -= 1
    w1 = p.measure(TAG1, tag)
    y1 = rule_y + 50
    runs.append(Run(TAG1, "plex", tag, t["fg2"], (W - w1) / 2, y1))
    w2 = p.measure(TAG2A, tag) + psb.measure(TAG2B, tag)
    x2 = (W - w2) / 2
    y2 = y1 + tag * 1.6
    runs.append(Run(TAG2A, "plex", tag, t["fg2"], x2, y2))
    runs.append(Run(TAG2B, "plexsb", tag, t["em"], x2 + p.measure(TAG2A, tag), y2))
    return W, H, crest, runs, rects


def _title_runs(runs, rects, fonts, t, x0, ty, size, tr, gap):
    o = fonts["oswald"]
    runs.append(Run(TITLE_A, "oswald", size, t["fg"], x0, ty, tr))
    x = x0 + o.measure(TITLE_A, size, tr) + gap * size
    runs.append(Run(TITLE_SEP, "oswald", size, t["gold"], x, ty))
    x += o.measure(TITLE_SEP, size) + gap * size
    runs.append(Run(TITLE_B, "oswald", size, t["fg"], x, ty, tr))


def svg_shell(W, H, theme, crest_href, crest, inner):
    t = THEMES[theme]
    cx = crest[0] + crest[2] / 2
    cy = crest[1] + crest[3] / 2
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
        'aria-label="Memento Mori · Maker Mastery. %s %s%s">\n'
        '<defs><radialGradient id="g" gradientUnits="userSpaceOnUse" cx="%.1f" cy="%.1f" r="%.1f">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
        '<filter id="halo" x="-5%%" y="-5%%" width="110%%" height="110%%" color-interpolation-filters="sRGB">'
        '<feMorphology in="SourceAlpha" operator="dilate" radius="2.5" result="d"/>'
        '<feGaussianBlur in="d" stdDeviation="1.2" result="b"/>'
        '<feFlood flood-color="#0A0A0A" flood-opacity="0.9"/>'
        '<feComposite in2="b" operator="in" result="h"/>'
        '<feMerge><feMergeNode in="h"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>\n'
        '<rect width="%d" height="%d" fill="%s"/>\n'
        '<rect width="%d" height="%d" fill="url(#g)"/>\n'
        '<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" href="%s"%s/>\n'
        "%s</svg>\n"
    ) % (W, H, W, H, html.escape(TAG1), html.escape(TAG2A), html.escape(TAG2B),
         cx, cy, max(crest[2], crest[3]) * 0.75, t["glow"], t["bg"],
         W, H, t["bg"], W, H,
         crest[0], crest[1], crest[2], crest[3], crest_href,
         # light theme: thin dark outline so the crest's white lettering reads on bone
         ' filter="url(#halo)"' if theme == "light" else "", inner)


def rects_svg(rects):
    return "".join('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>\n' % r for r in rects)


def text_svg(runs):
    out = []
    for r in runs:
        fam, _, wght = FONT_FILES[r.font]
        out.append(
            '<text x="%.2f" y="%.2f" fill="%s" style="font-family:\'%s\';font-weight:%d;'
            "font-size:%spx;letter-spacing:%.3fpx;font-kerning:none;font-variant-ligatures:none;"
            'font-variation-settings:\'wght\' %d">%s</text>\n'
            % (r.x, r.y, r.color, fam, wght, r.size, r.tracking * r.size, wght, html.escape(r.text)))
    return "".join(out)


def outline_svg(runs, fonts):
    out = []
    for r in runs:
        d, _ = fonts[r.font].text_path(r.text, r.x, r.y, r.size, r.tracking)
        out.append('<path fill="%s" d="%s"/>\n' % (r.color, d))
    return "".join(out)


HTML = """<!doctype html>
<!-- Render source for %(png)s (%(W)dx%(H)d). Built by build_brand.py; edit that, not this file.
     Fonts: place the SIL OFL font files in a fonts/ folder beside this page (not shipped):
     Oswald-VariableFont_wght.ttf, IBMPlexMono-Medium.ttf, IBMPlexMono-SemiBold.ttf.
     Render: chrome --headless=new --hide-scrollbars --force-device-scale-factor=1
             --window-size=%(W)d,%(H)d --screenshot=%(png)s %(name)s -->
<html><head><meta charset="utf-8"><title>%(png)s source</title>
<style>
@font-face{font-family:'Oswald';src:url('fonts/Oswald-VariableFont_wght.ttf') format('truetype');font-weight:200 700}
@font-face{font-family:'IBM Plex Mono';src:url('fonts/IBMPlexMono-Medium.ttf') format('truetype');font-weight:500}
@font-face{font-family:'IBM Plex Mono';src:url('fonts/IBMPlexMono-SemiBold.ttf') format('truetype');font-weight:600}
html,body{margin:0;padding:0;background:%(bg)s;overflow:hidden}
svg{display:block}
</style></head><body>
%(svg)s</body></html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build brand banner HTML sources and outlined SVGs.")
    ap.add_argument("--fonts", required=True, help="folder holding the three OFL font files")
    ap.add_argument("--brand-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    args = ap.parse_args(argv)
    brand = os.path.abspath(args.brand_dir)
    src = os.path.join(brand, "src")
    fonts = {k: Font(os.path.join(args.fonts, v[1])) for k, v in FONT_FILES.items()}
    # Hero = the parent crest (the master logo with the MEMENTO MORI lettering)
    crest_big = os.path.join(brand, "crest-parent-1024.png")
    crest_small = os.path.join(brand, "crest-parent-512.png")
    w, h = png_size(crest_big)
    aspect = w / h
    with open(crest_small, "rb") as f:
        data_uri = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
    jobs = [("banner", "dark", "banner-dark"), ("banner", "light", "banner-light"),
            ("social", "dark", "social-preview")]
    for kind, theme, name in jobs:
        W, H, crest, runs, rects = layout(kind, fonts, theme, aspect)
        inner_html = rects_svg(rects) + text_svg(runs)
        page = HTML % dict(png=name + ".png", name=name + ".html", W=W, H=H, bg=THEMES[theme]["bg"],
                           svg=svg_shell(W, H, theme, "../crest-parent-1024.png", crest, inner_html))
        with open(os.path.join(src, name + ".html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
        if kind == "banner":
            svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_shell(
                W, H, theme, data_uri, crest, rects_svg(rects) + outline_svg(runs, fonts))
            out = os.path.join(brand, name + ".svg")
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
            print("%s %d bytes" % (out, os.path.getsize(out)))
        print("%s.html written" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
