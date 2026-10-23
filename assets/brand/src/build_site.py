"""Build the website-style brand images (standard library only).

The look follows the Memento Mori websites: condensed bold caps (Oswald), an
outline (stroke-only) second line, one word in house red #D21F3C, a small red
letter-spaced eyebrow, an italic serif tagline (Playfair Display), near-black
#0A0A0A to #141414 with a fine grain, and a red marquee strip.

Every piece of text is converted to SVG paths with ttf_outlines.py, so the SVGs
render the same everywhere and no font file is referenced or shipped.

Writes
  ../banner-dark.svg, ../banner-light.svg      hero banner, option B, live (1600x420)
  ../banner-dark_optA.svg                      hero banner, option A, alternate
  src/render-*.html                            pages Chrome turns into the PNGs
                                               (banner B/A, social preview B/A)
  ../headers/<slug>.svg                        one header strip per README section
  ../headers/ticker.svg                        red marquee divider
  ../headers/why-*.svg                         the three "Why" cards
  ../headers/domains-*.svg                     domain group headers
  ../headers/tiles/NN.svg                      one tile per domain

Usage:
    python build_site.py --fonts FONT_DIR
FONT_DIR holds Oswald-Bold.ttf, Oswald-SemiBold.ttf, Oswald-Medium.ttf
(https://github.com/googlefonts/OswaldFont, fonts/ttf) and
PlayfairDisplay-Italic.ttf (https://github.com/google/fonts, ofl/playfairdisplay,
the variable italic file; its default instance, weight 400, is used).
All four are SIL Open Font License 1.1 and are never shipped.
"""
import argparse
import base64
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ttf_outlines import Font  # noqa: E402

# ---- the websites' colour system (CSS custom properties of the site design) ----
VOID = "#0A0A0A"
PANEL = "#141414"
RULE = "#262626"
BONE = "#F2EFEA"
DIM = "#9A958E"
SUB = "#CFCAC2"   # italic tagline colour
RED = "#D21F3C"
WHITE = "#FFFFFF"

FONTS = {}
BRAND = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load_fonts(d):
    for key, fn in (("bold", "Oswald-Bold.ttf"), ("semi", "Oswald-SemiBold.ttf"),
                    ("med", "Oswald-Medium.ttf"), ("serif", "PlayfairDisplay-Italic.ttf")):
        FONTS[key] = Font(os.path.join(d, fn))


def esc(s):
    return html.escape(s, quote=True)


def width(font, text, size, track=0.0):
    return FONTS[font].measure(text, size, track)


def text(font, s, x, y, size, fill=None, track=0.0, stroke=None, sw=0.0, opacity=None):
    d, _ = FONTS[font].text_path(s, x, y, size, track)
    attrs = 'fill="%s"' % (fill or "none")
    if stroke:
        attrs += ' stroke="%s" stroke-width="%.2f" stroke-linejoin="round"' % (stroke, sw)
    if opacity is not None:
        attrs += ' opacity="%.2f"' % opacity
    return '<path %s d="%s"/>\n' % (attrs, d)


def outline_w(size):
    return max(1.4, size * 0.016)


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def png_size(path):
    import struct
    with open(path, "rb") as f:
        h = f.read(24)
    return struct.unpack(">II", h[16:24])


def defs(W, H, glow=None, uid=""):
    """Background gradient, grain filter and optional red glow (cx, cy, r)."""
    g = ('<defs>'
         '<linearGradient id="bg%(u)s" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="%(v)s"/><stop offset="1" stop-color="%(p)s"/></linearGradient>'
         '<filter id="gr%(u)s" filterUnits="userSpaceOnUse" x="0" y="0" width="%(W)d" height="%(H)d">'
         '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch" seed="7"/>'
         '<feColorMatrix type="saturate" values="0"/></filter>'
         % dict(u=uid, v=VOID, p=PANEL, W=W, H=H))
    if glow:
        g += ('<radialGradient id="gl%s" gradientUnits="userSpaceOnUse" cx="%.1f" cy="%.1f" r="%.1f">'
              '<stop offset="0" stop-color="%s" stop-opacity=".34"/>'
              '<stop offset=".55" stop-color="%s" stop-opacity=".10"/>'
              '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
              % (uid, glow[0], glow[1], glow[2], RED, RED, RED))
    g += '</defs>\n'
    g += '<rect width="%d" height="%d" fill="url(#bg%s)"/>\n' % (W, H, uid)
    if glow:
        g += '<rect width="%d" height="%d" fill="url(#gl%s)"/>\n' % (W, H, uid)
    g += '<rect width="%d" height="%d" filter="url(#gr%s)" opacity=".09"/>\n' % (W, H, uid)
    return g


def svg_open(W, H, label):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'role="img" aria-label="%s">\n<title>%s</title>\n' % (W, H, W, H, esc(label), esc(label)))


def marquee(W, y, h, phrases, size):
    """Red strip with white condensed caps, repeated to fill the width."""
    out = '<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>\n' % (y, W, h, RED)
    base = y + h / 2 + size * 0.36
    x = 18.0
    track = 0.12
    gap = size * 1.6
    i = 0
    while x < W:
        p = phrases[i % len(phrases)]
        out += text("semi", p, x, base, size, WHITE, track)
        x += width("semi", p, size, track) + gap / 2
        # small diamond separator, like the sites' marquee
        r = size * 0.16
        cx, cy = x, y + h / 2
        out += '<path fill="%s" opacity=".75" d="M%.1f %.1fL%.1f %.1fL%.1f %.1fL%.1f %.1fZ"/>\n' % (
            WHITE, cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy)
        x += gap / 2
        i += 1
    return out


def eyebrow(x, y, s, size):
    out = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>\n' % (x, y - size * 0.36, size * 2.6, max(1.2, size * 0.09), RED)
    out += text("med", s, x + size * 3.6, y, size, RED, 0.32)
    return out


def headline_line(x, y, size, parts):
    """parts: list of (text, style) with style 'fill', 'red' or 'out'. Returns (svg, width)."""
    out, cx = "", x
    for i, (s, style) in enumerate(parts):
        if style == "red":
            out += text("bold", s, cx, y, size, RED)
        elif style == "fill":
            out += text("bold", s, cx, y, size, BONE)
        else:
            out += text("bold", s, cx, y, size, None, 0, BONE, outline_w(size))
        cx += width("bold", s, size)
    return out, cx - x


def line_w(size, parts):
    return sum(width("bold", s, size) for s, _ in parts)


HEADLINES = {
    "A": ([("BUILD WITH", "fill")], [("AI. ", "red"), ("PRINT BY HAND.", "out")]),
    "B": ([("TIME IS ", "fill"), ("SHORT.", "red")], [("MAKE IT COUNT.", "out")]),
}
LIVE, ALT = "B", "A"  # B is the live hero; A is kept as the _optA alternate
EYEBROW = "MEMENTO MORI · MAKER MASTERY"
TAGLINE = ("A Claude Code operating system for makers —",
           "research-backed, AI-checked, human-built.")
TICKER = ["AI CHECKS", "YOU BUILD", "MAKE", "STREAM", "CREATE", "RESEARCH-BACKED", "HUMAN-BUILT"]


def hero(kind, opt, crest_href):
    """kind 'banner' (1600x420) or 'social' (1280x640)."""
    if kind == "banner":
        W, H, mq, mq_size, x0 = 1600, 420, 32, 13, 72
        ch = 352
        crest_right = 64
        hl_max, ey_size, tg_size = 104, 15, 25
    else:
        W, H, mq, mq_size, x0 = 1280, 640, 44, 17, 72
        ch = 380
        crest_right = 56
        hl_max, ey_size, tg_size = 110, 18, 28
    cw_, chh_ = png_size(os.path.join(BRAND, "crest-parent-1024.png"))
    cw = ch * cw_ / chh_
    cx = W - crest_right - cw
    cy = mq + (H - mq - ch) / 2
    glow = (cx + cw / 2, cy + ch / 2, ch * 0.95)
    l1, l2 = HEADLINES[opt]
    avail = cx - x0 - 36
    size = hl_max
    while max(line_w(size, l1), line_w(size, l2)) > avail and size > 40:
        size -= 1
    # vertical rhythm, as on the site: eyebrow, h1 (line-height .98), italic sub
    block = ey_size + 22 + size * 0.80 + size * 0.98 + 30 + tg_size * 1.0 + tg_size * 1.4
    top = mq + (H - mq - block) / 2
    ey_y = top + ey_size * 0.8
    y1 = ey_y + 22 + size * 0.80
    y2 = y1 + size * 0.98
    t1 = y2 + 30 + tg_size * 1.0
    t2 = t1 + tg_size * 1.4
    label = "Memento Mori · Maker Mastery. %s %s. %s %s" % (
        "".join(s for s, _ in l1), "".join(s for s, _ in l2), TAGLINE[0], TAGLINE[1])
    out = svg_open(W, H, label) + defs(W, H, glow)
    out += '<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" href="%s"/>\n' % (cx, cy, cw, ch, crest_href)
    out += marquee(W, 0, mq, TICKER, mq_size)
    out += eyebrow(x0, ey_y, EYEBROW, ey_size)
    out += headline_line(x0, y1, size, l1)[0]
    out += headline_line(x0, y2, size, l2)[0]
    out += text("serif", TAGLINE[0], x0, t1, tg_size, SUB)
    out += text("serif", TAGLINE[1], x0, t2, tg_size, SUB)
    out += "</svg>\n"
    return W, H, out


# ---- README section headers ----
SECTIONS = [  # (slug, eyebrow, [(text, style)])
    ("contents", "INDEX", [("CONTENTS", "red")]),
    ("what-is-this", "THE PROJECT", [("WHAT IS ", "out"), ("THIS", "red")]),
    ("why", "THE PRINCIPLES", [("WHY", "red")]),
    ("preview", "REAL OUTPUT", [("PRE", "out"), ("VIEW", "red")]),
    ("domains", "THE LIBRARY", [("DOMAINS", "red")]),
    ("how-it-works", "THE SYSTEM", [("HOW IT ", "out"), ("WORKS", "red")]),
    ("quick-start", "EIGHT STEPS", [("QUICK ", "out"), ("START", "red")]),
    ("guides", "THE MANUAL", [("GUIDES", "red")]),
    ("faq", "ANSWERS", [("FAQ", "red")]),
    ("roadmap", "WHAT COMES NEXT", [("ROAD", "out"), ("MAP", "red")]),
    ("contributing", "JOIN IN", [("CONTRI", "out"), ("BUTING", "red")]),
    ("credits", "THE MAKER", [("CREDITS", "red")]),
    ("license", "THE FINE PRINT", [("LICENSE", "red")]),
]
SECTION_ALT = {
    "contents": "Contents", "what-is-this": "What is this", "why": "Why", "preview": "Preview",
    "domains": "Domains", "how-it-works": "How it works", "quick-start": "Quick Start",
    "guides": "Guides", "faq": "FAQ", "roadmap": "Roadmap", "contributing": "Contributing",
    "credits": "Credits", "license": "License",
}


def header(i, slug, eb, parts):
    W, H = 1600, 180
    x0, size = 48, 92
    out = svg_open(W, H, SECTION_ALT[slug]) + defs(W, H, (W - 180, H / 2, 260), "")
    num = "%02d" % i
    nsize = 150
    nw = width("bold", num, nsize)
    out += text("bold", num, W - 56 - nw, H / 2 + nsize * 0.40, nsize, None, 0, BONE, 1.6, 0.22)
    out += eyebrow(x0, 50, "%s · %s" % (num, eb), 16)
    out += headline_line(x0, 52 + size * 0.88, size, parts)[0]
    out += '<rect x="0" y="%d" width="%d" height="3" fill="%s"/>\n' % (H - 3, W, RED)
    return out + "</svg>\n"


def ticker():
    W, H = 1600, 44
    out = svg_open(W, H, "AI checks, you build: make, stream, create")
    out += marquee(W, 0, H, TICKER, 19)
    return out + "</svg>\n"


# ---- Why cards ----
WHY = [
    ("crest-parent-card.png", "FACTS, NOT ", "GUESSES.",
     "Every fact links its public source. A fact-checker that never sees the researcher's "
     "reasoning re-derives each claim; anything unchecked is labelled “not verified”."),
    ("crest-printing-card.png", "GATES ON THE ", "REAL SLICE.",
     "Print files are judged from the sliced G-code and the 3MF itself, by tools with their own "
     "tests, so a clean-looking preview cannot hide a bad plate."),
    ("crest-apparel-card.png", "YOU STAY IN ", "CHARGE.",
     "Nothing is installed, deleted or printed without you. A hook guards the folders you protect, "
     "and the print rule is enforced in settings as well as in the rules."),
]


def wrap(font, s, size, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if width(font, t, size) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def why_card(n, crest, t_out, t_red, body):
    W, H = 560, 520  # 2x export of a 280x260 card
    pad = 40
    out = svg_open(W, H, "%s%s %s" % (t_out, t_red, body)) + defs(W, H, (W - 90, 110, 220), "")
    out += '<rect x="1" y="1" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2"/>\n' % (W - 2, H - 2, RULE)
    out += '<rect x="0" y="0" width="%d" height="6" fill="%s"/>\n' % (W, RED)
    cw_, ch_ = png_size(os.path.join(BRAND, crest))
    iw = 132
    ih = iw * ch_ / cw_
    out += '<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" href="%s"/>\n' % (W - pad - iw + 10, 34, iw, ih, data_uri(os.path.join(BRAND, crest)))
    out += eyebrow(pad, 70, "%02d" % n, 16)
    size = 46
    out += text("bold", t_out.strip(), pad, 170, size, BONE)
    out += text("bold", t_red, pad, 170 + size * 1.0, size, RED)
    y = 170 + size * 1.0 + 64
    for ln in wrap("serif", body, 27, W - 2 * pad):
        out += text("serif", ln, pad, y, 27, SUB)
        y += 40
    return out + "</svg>\n"


# ---- Domains ----
GROUPS = [
    ("making", "crest-printing-card.png", "MAKE", [("MAKING", "red")], [
        ("00", "Your gear (template)", "knowledge/00-gear-inventory/README.md", "tpl"),
        ("01", "Printers", "knowledge/01-printers/index.md", "v10"),
        ("02", "Bambu Studio", "knowledge/02-bambu-studio/index.md", "v10"),
        ("03", "Materials", "knowledge/03-materials/index.md", "v10"),
        ("04", "Design for FDM", "knowledge/04-design-for-fdm/index.md", "v10"),
        ("05", "CAD, hard surface", "knowledge/05-cad-hard-surface/index.md", "v10"),
        ("06", "Organic modeling", "knowledge/06-organic-modeling/index.md", "v10"),
        ("07", "Engineering", "knowledge/07-engineering/index.md", "v10"),
        ("08", "Electronics and lighting", "knowledge/08-electronics-lighting/index.md", "v10"),
        ("09", "Finishing", None, "v11"),
        ("10", "Workflows", None, "v11"),
        ("11", "Calibration and testing", None, "v11"),
        ("12", "Failure diagnosis", "knowledge/12-failure-diagnosis/index.md", "v10"),
        ("13", "Project ops", None, "v11"),
    ]),
    ("creative", "crest-apparel-card.png", "CREATE", [("CREATIVE, BUSINESS ", "out"), ("& DESIGN", "red")], [
        ("14", "Creative mindset", None, "v11"),
        ("17", "Creative direction", None, "v11"),
        ("18", "Selling 3D prints", None, "v11"),
        ("20", "Woodworking", None, "v11"),
        ("21", "MakerWorld", None, "v11"),
        ("22", "IP and licensing", None, "v11"),
        ("24", "Surfacing and rendering", "knowledge/24-surfacing-and-rendering/index.md", "v10"),
        ("25", "Reference sheets", None, "v11"),
        ("26", "AI to 3D", "knowledge/26-ai-to-3d/index.md", "v10"),
        ("27", "Scanning and photogrammetry", None, "v11"),
    ]),
    ("games-tech", "crest-streaming-card.png", "STREAM", [("GAMES, MEDIA, AI, ", "out"), ("TECH & SAFETY", "red")], [
        ("28", "Game design", None, "v11"),
        ("29", "Game development", None, "v11"),
        ("30", "Visual pre-production", None, "v11"),
        ("31", "Retro arcade", None, "v11"),
        ("32", "Audio and sound", None, "v11"),
        ("33", "Animation and motion", None, "v11"),
        ("34", "Video editing", None, "v11"),
        ("35", "AI image and video", None, "v11"),
        ("37", "Photography", None, "v11"),
        ("39", "Raspberry Pi and microcontrollers", "knowledge/39-raspberry-pi-and-microcontrollers/index.md", "v10"),
        ("40", "Bambu ecosystem", "knowledge/40-bambu-ecosystem/index.md", "v10"),
        ("41", "MCP", "knowledge/41-mcp/index.md", "v10"),
        ("42", "Agent engineering", "knowledge/42-agent-engineering/index.md", "v10"),
        ("43", "Data and backups", None, "v11"),
        ("44", "Safety", "knowledge/44-safety/index.md", "v10"),
    ]),
]
GROUP_ALT = {"making": "Making", "creative": "Creative, business and design",
             "games-tech": "Games, media, AI, tech and safety"}
STATUS_TEXT = {"v10": "V1.0", "tpl": "V1.0 · TEMPLATE", "v11": "V1.1"}
STATUS_ALT = {"v10": "shipped in v1.0", "tpl": "shipped in v1.0 (template)", "v11": "coming in v1.1"}


def group_header(slug, crest, word, parts):
    W, H = 1600, 140
    out = svg_open(W, H, GROUP_ALT[slug]) + defs(W, H, (150, H / 2, 200), "")
    cw_, ch_ = png_size(os.path.join(BRAND, crest))
    ih = 112
    iw = ih * cw_ / ch_
    out += '<image x="32" y="%.1f" width="%.1f" height="%.1f" href="%s"/>\n' % ((H - ih) / 2, iw, ih, data_uri(os.path.join(BRAND, crest)))
    x = 32 + iw + 28
    out += eyebrow(x, 44, word, 15)
    size = 64
    avail = W - x - 40
    while line_w(size, parts) > avail:
        size -= 1
    out += headline_line(x, 44 + 20 + size * 0.82, size, parts)[0]
    out += '<rect x="0" y="%d" width="%d" height="2" fill="%s"/>\n' % (H - 2, W, RED)
    return out + "</svg>\n"


def check_mark(x, y, s):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>'
            '<path d="M%.1f %.1fL%.1f %.1fL%.1f %.1f" fill="none" stroke="%s" stroke-width="%.1f" '
            'stroke-linecap="round" stroke-linejoin="round"/>\n'
            % (x, y, s, s, s * 0.18, RED, x + s * .24, y + s * .52, x + s * .43, y + s * .72,
               x + s * .78, y + s * .30, BONE, s * 0.13))


def hourglass(x, y, s):
    return ('<path d="M%.1f %.1fH%.1fL%.1f %.1fL%.1f %.1fH%.1fL%.1f %.1fZ" fill="none" stroke="%s" '
            'stroke-width="%.1f" stroke-linejoin="round"/>\n'
            % (x + s * .2, y, x + s * .8, x + s * .5, y + s * .5, x + s * .8, y + s, x + s * .2,
               x + s * .5, y + s * .5, DIM, s * 0.1))


def tile(num, label, status):
    W, H = 520, 150  # 2x of 260x75
    shipped = status != "v11"
    out = svg_open(W, H, "%s %s, %s" % (num, label, STATUS_ALT[status])) + defs(W, H, (W - 60, 20, 180) if shipped else None, "")
    out += '<rect x="1" y="1" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2"/>\n' % (W - 2, H - 2, RED if shipped else RULE)
    out += '<rect x="0" y="0" width="6" height="%d" fill="%s"/>\n' % (H, RED if shipped else RULE)
    nsize = 88
    out += text("bold", num, 26, 60 + nsize * 0.30, nsize, None, 0, BONE if shipped else DIM, 1.8, 0.85 if shipped else 0.5)
    x = 26 + width("bold", "00", nsize) + 22
    avail = W - x - 22
    size = 31
    lines = wrap("semi", label.upper(), size, avail)
    while len(lines) > 2:
        size -= 1
        lines = wrap("semi", label.upper(), size, avail)
    ly = 62 if len(lines) == 1 else 48
    for ln in lines:
        out += text("semi", ln, x, ly, size, BONE if shipped else DIM)
        ly += size * 1.12
    sy = H - 24
    st = STATUS_TEXT[status]
    if shipped:
        out += check_mark(x, sy - 22, 26)
        out += text("med", st, x + 36, sy, 21, RED, 0.18)
    else:
        out += hourglass(x + 2, sy - 22, 24)
        out += text("med", st, x + 36, sy, 21, DIM, 0.18)
    return out + "</svg>\n"


RENDER = """<!doctype html>
<!-- Render source for %(png)s (%(W)dx%(H)d). Built by build_site.py; edit that, not this file.
     The text is already outlined: no fonts are needed. -->
<html><head><meta charset="utf-8"><title>%(png)s source</title>
<style>html,body{margin:0;padding:0;background:#0A0A0A;overflow:hidden}svg{display:block}</style>
</head><body>
%(svg)s</body></html>
"""


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    return os.path.getsize(path)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build website-style brand images.")
    ap.add_argument("--fonts", required=True)
    args = ap.parse_args(argv)
    load_fonts(args.fonts)
    src = os.path.join(BRAND, "src")
    hd = os.path.join(BRAND, "headers")
    sizes = {}
    small = data_uri(os.path.join(BRAND, "crest-parent-512.png"))
    for opt in (LIVE, ALT):
        suffix = "" if opt == LIVE else "_opt" + opt
        W, H, svg = hero("banner", opt, small)
        sizes["banner-dark%s.svg" % suffix] = write(os.path.join(BRAND, "banner-dark%s.svg" % suffix), svg)
        if opt == LIVE:
            sizes["banner-light.svg"] = write(os.path.join(BRAND, "banner-light.svg"), svg)
        for kind, name in (("banner", "banner-dark%s" % suffix), ("social", "social-preview%s" % suffix)):
            W, H, svg = hero(kind, opt, "../crest-parent-1024.png")
            write(os.path.join(src, "render-%s.html" % name), RENDER % dict(png=name + ".png", W=W, H=H, svg=svg))
    for i, (slug, eb, parts) in enumerate(SECTIONS):
        sizes["headers/%s.svg" % slug] = write(os.path.join(hd, slug + ".svg"), header(i, slug, eb, parts))
    sizes["headers/ticker.svg"] = write(os.path.join(hd, "ticker.svg"), ticker())
    for n, (crest, a, b, body) in enumerate(WHY, 1):
        sizes["headers/why-%d.svg" % n] = write(os.path.join(hd, "why-%d.svg" % n), why_card(n, crest, a, b, body))
    for slug, crest, word, parts, tiles in GROUPS:
        sizes["headers/domains-%s.svg" % slug] = write(os.path.join(hd, "domains-%s.svg" % slug), group_header(slug, crest, word, parts))
        for num, label, link, status in tiles:
            sizes["headers/tiles/%s.svg" % num] = write(os.path.join(hd, "tiles", num + ".svg"), tile(num, label, status))
    for k in sorted(sizes):
        print("%-40s %8d" % (k, sizes[k]))
    print("total svg bytes", sum(sizes.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
