"""Minimal TrueType reader: turns a line of text into SVG path data (standard library only).

Reads cmap (format 4), hmtx, loca/glyf (simple and composite glyphs). For a
variable font it uses the default instance only (no gvar deltas). No kerning,
no shaping: fine for short Latin brand lines rendered with font-kerning: none.
"""
import struct


class Font:
    def __init__(self, path):
        self.data = open(path, "rb").read()
        d = self.data
        num = struct.unpack(">H", d[4:6])[0]
        self.tables = {}
        for i in range(num):
            tag, _, off, ln = struct.unpack(">4sIII", d[12 + 16 * i:28 + 16 * i])
            self.tables[tag.decode("latin-1")] = (off, ln)
        off = self.tables["head"][0]
        self.upem = struct.unpack(">H", d[off + 18:off + 20])[0]
        self.loca_long = struct.unpack(">h", d[off + 50:off + 52])[0] == 1
        off = self.tables["maxp"][0]
        self.num_glyphs = struct.unpack(">H", d[off + 4:off + 6])[0]
        off = self.tables["hhea"][0]
        self.ascent, self.descent = struct.unpack(">hh", d[off + 4:off + 8])
        self.num_hmetrics = struct.unpack(">H", d[off + 34:off + 36])[0]
        self._cmap()
        self._loca()
        self.default_wght = self._fvar_default("wght")

    def _fvar_default(self, axis):
        if "fvar" not in self.tables:
            return None
        off = self.tables["fvar"][0]
        d = self.data
        axes_off, _, axis_count, axis_size = struct.unpack(">HHHH", d[off + 4:off + 12])
        for i in range(axis_count):
            a = off + axes_off + i * axis_size
            tag = d[a:a + 4].decode("latin-1")
            mn, df, mx = (v / 65536 for v in struct.unpack(">iii", d[a + 4:a + 16]))
            if tag == axis:
                return (mn, df, mx)
        return None

    def _cmap(self):
        d = self.data
        off = self.tables["cmap"][0]
        n = struct.unpack(">H", d[off + 2:off + 4])[0]
        sub = None
        for i in range(n):
            pid, eid, so = struct.unpack(">HHI", d[off + 4 + 8 * i:off + 12 + 8 * i])
            if (pid == 3 and eid == 1) or (pid == 0 and sub is None):
                if struct.unpack(">H", d[off + so:off + so + 2])[0] == 4:
                    sub = off + so
        if sub is None:
            raise ValueError("no cmap format 4 subtable")
        segx2 = struct.unpack(">H", d[sub + 6:sub + 8])[0]
        seg = segx2 // 2
        ends = struct.unpack(">%dH" % seg, d[sub + 14:sub + 14 + segx2])
        starts = struct.unpack(">%dH" % seg, d[sub + 16 + segx2:sub + 16 + 2 * segx2])
        deltas = struct.unpack(">%dh" % seg, d[sub + 16 + 2 * segx2:sub + 16 + 3 * segx2])
        ro_pos = sub + 16 + 3 * segx2
        ros = struct.unpack(">%dH" % seg, d[ro_pos:ro_pos + segx2])
        self.cmap = {}
        for i in range(seg):
            for c in range(starts[i], ends[i] + 1):
                if c == 0xFFFF:
                    continue
                if ros[i] == 0:
                    g = (c + deltas[i]) & 0xFFFF
                else:
                    p = ro_pos + 2 * i + ros[i] + 2 * (c - starts[i])
                    g = struct.unpack(">H", d[p:p + 2])[0]
                    if g:
                        g = (g + deltas[i]) & 0xFFFF
                self.cmap[c] = g

    def _loca(self):
        d = self.data
        off = self.tables["loca"][0]
        n = self.num_glyphs + 1
        if self.loca_long:
            self.loca = struct.unpack(">%dI" % n, d[off:off + 4 * n])
        else:
            self.loca = [v * 2 for v in struct.unpack(">%dH" % n, d[off:off + 2 * n])]

    def advance(self, gid):
        off = self.tables["hmtx"][0]
        i = min(gid, self.num_hmetrics - 1)
        return struct.unpack(">H", self.data[off + 4 * i:off + 4 * i + 2])[0]

    def contours(self, gid, depth=0):
        """Return list of contours; each is a list of (x, y, on_curve)."""
        d = self.data
        base = self.tables["glyf"][0]
        start, end = self.loca[gid], self.loca[gid + 1]
        if start == end:
            return []
        p = base + start
        nc = struct.unpack(">h", d[p:p + 2])[0]
        if nc < 0:
            return self._composite(p + 10, depth)
        end_pts = struct.unpack(">%dH" % nc, d[p + 10:p + 10 + 2 * nc])
        npts = end_pts[-1] + 1
        q = p + 10 + 2 * nc
        ilen = struct.unpack(">H", d[q:q + 2])[0]
        q += 2 + ilen
        flags = []
        while len(flags) < npts:
            f = d[q]; q += 1
            flags.append(f)
            if f & 8:
                r = d[q]; q += 1
                flags.extend([f] * r)
        xs, ys = [], []
        for coords, short_bit, same_bit in ((xs, 2, 16), (ys, 4, 32)):
            v = 0
            for f in flags[:npts]:
                if f & short_bit:
                    dv = d[q]; q += 1
                    v += dv if f & same_bit else -dv
                elif not f & same_bit:
                    v += struct.unpack(">h", d[q:q + 2])[0]; q += 2
                coords.append(v)
        out, s = [], 0
        for e in end_pts:
            out.append([(xs[i], ys[i], bool(flags[i] & 1)) for i in range(s, e + 1)])
            s = e + 1
        return out

    def _composite(self, p, depth):
        d = self.data
        out = []
        while True:
            flags, gi = struct.unpack(">HH", d[p:p + 4]); p += 4
            if flags & 1:
                a1, a2 = struct.unpack(">hh", d[p:p + 4]); p += 4
            else:
                a1, a2 = struct.unpack(">bb", d[p:p + 2]); p += 2
            if not flags & 2:
                raise ValueError("point-matched composites not supported")
            xx, xy, yx, yy = 1.0, 0.0, 0.0, 1.0
            if flags & 8:
                xx = yy = struct.unpack(">h", d[p:p + 2])[0] / 16384; p += 2
            elif flags & 0x40:
                xx, yy = (v / 16384 for v in struct.unpack(">hh", d[p:p + 4])); p += 4
            elif flags & 0x80:
                xx, xy, yx, yy = (v / 16384 for v in struct.unpack(">hhhh", d[p:p + 8])); p += 8
            for c in self.contours(gi, depth + 1):
                out.append([(x * xx + y * yx + a1, x * xy + y * yy + a2, on) for x, y, on in c])
            if not flags & 0x20:
                break
        return out

    def text_path(self, text, x, y, size, tracking_em=0.0):
        """SVG path 'd' for text with its baseline at (x, y). Returns (d, width_px)."""
        s = size / self.upem
        pen = 0.0
        parts = []
        for ch in text:
            gid = self.cmap.get(ord(ch), 0)
            for c in self.contours(gid):
                parts.append(_contour_d(c, x + pen * s, y, s))
            pen += self.advance(gid) + tracking_em * self.upem
        width = (pen - tracking_em * self.upem) * s if text else 0.0
        return " ".join(parts), width

    def measure(self, text, size, tracking_em=0.0):
        pen = sum(self.advance(self.cmap.get(ord(c), 0)) for c in text)
        pen += tracking_em * self.upem * max(len(text) - 1, 0)
        return pen * size / self.upem


def _fmt(v):
    # one decimal is below a tenth of a pixel at every export size used here
    return ("%.1f" % v).rstrip("0").rstrip(".")


def _contour_d(c, ox, oy, s):
    pts = [(ox + px * s, oy - py * s, on) for px, py, on in c]
    n = len(pts)
    if n == 0:
        return ""
    # start on an on-curve point (or the midpoint of two off-curve points)
    k = next((i for i, p in enumerate(pts) if p[2]), None)
    if k is None:
        a, b = pts[0], pts[1]
        start = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, True)
        seq = pts[1:] + pts[:1]
    else:
        start = pts[k]
        seq = pts[k + 1:] + pts[:k]
    seq = seq + [start]
    d = ["M%s %s" % (_fmt(start[0]), _fmt(start[1]))]
    ctrl = None
    for p in seq:
        if p[2]:
            if ctrl is None:
                d.append("L%s %s" % (_fmt(p[0]), _fmt(p[1])))
            else:
                d.append("Q%s %s %s %s" % (_fmt(ctrl[0]), _fmt(ctrl[1]), _fmt(p[0]), _fmt(p[1])))
                ctrl = None
        else:
            if ctrl is not None:
                mx, my = (ctrl[0] + p[0]) / 2, (ctrl[1] + p[1]) / 2
                d.append("Q%s %s %s %s" % (_fmt(ctrl[0]), _fmt(ctrl[1]), _fmt(mx), _fmt(my)))
            ctrl = p
    d.append("Z")
    return "".join(d)
