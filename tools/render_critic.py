r"""render_critic.py - an objective, scored critique of a still render (a proxy for an art review, never taste).

Why: renders can look bad while every agent calls them fine. This tool does not have taste. It measures what painters,
designers and photographers check by eye (value structure, focal point and hierarchy, the squint test, edge separation, text
legibility, distance to professional references), gives each a number, a pass/warn/fail band and one concrete fix sentence,
and rolls them into a 0-100 score. It is a PROXY for a human art review, never a replacement.
Optional dependency: open3d (image reading and writing; requirements-optional.txt). Without it the tool exits 3 with a message.

Sources (the short codes in thresholds and fix sentences; full list in SOURCE_URLS below):
  - Relative luminance and contrast ratio: WCAG 2.2, https://www.w3.org/TR/WCAG22/ (DF 1, DF 2).
  - 3:1 for edges/rims and graphics (SC 1.4.11, DF 5) and 4.5:1 for text (SC 1.4.3, DF 3, TR A14) are used here as a HOUSE
    RULE: WCAG exempts picture text and logotypes (DF 3, DF 7), and this tool measures rendered pixels, which is stricter than
    WCAG's source-colour method (DF 8).
  - Notan reads as 2, 3 or 4 values (DF 26 Dow, Composition; DF 27 community, "two, three or four values").
  - Squint test = "squint or apply a slight blur" (DF 11, NN/g); the blur radius used here is a parameter not sourced.
  - Hierarchy: "Limit how many elements are big to a maximum of 2" (DF 10, NN/g, written for UI design).
  - A single strong saliency peak is what Itti-Koch normalisation promotes (DF 23); using peak1 / competitor as a score is a
    derived use with no sourced threshold.
  - Text floor at the 320x180 test size: at least 4 samples (px) per character in each axis (Legge and Cheung 2004,
    "4x4 samples per character", TR A16, TR A19). A floor, never a pass: below it FAILs, at or above it scores nothing.
    320x180 is our test size, not a YouTube display size (TR A19 is arithmetic on A16).
  - Warm/cool is NOT used as a focal rule: the sources tie it to depth only (DF 37, DF 38) and tie hierarchy to value and
    saturation contrast (DF 9). The saliency colour channels are opponent-contrast terms, not a warmth score.
  - Fix sentences cite rim-light practice for dark subjects on dark grounds (PL 22, PL 23, PL 24) and Blender colour-management
    Exposure in stops (PL 13).
Every other threshold is marked "provisional, no source yet".

Inputs: PNG/JPG images (read-only). Outputs: see "Outputs" below. Example:
  .venv\Scripts\python.exe -B tools\render_critic.py work\renders\front.png --subject-box 400,200,800,900

Checks (all on the image only; nothing is rendered, sent or installed):
  1. value    sRGB -> linear -> relative luminance Y (WCAG 2.2, DF 1), then CIE 1976 lightness L* (0-100) from Y for everything
              perceptual (formula: CIE 15, not fetched this run). k-means on L* into 2, 3, 4 and 5 groups
              (scipy.cluster.vq.kmeans2, deterministic start evenly spaced between p1 and p99): group shares, centres, the
              smallest gap between occupied centres and R^2 (between-group / total variance; 1.0 = the picture IS its value
              groups). The notan metrics take the SMALLEST k in 2..4 that reaches the R^2 pass line (else the k in 2..4 with
              the best R^2): any of 2, 3 or 4 values can pass (DF 26, DF 27). Also the L* p2..p98 range, the midtone share
              (L* 30..70), clipped pixels (all three channels at 0, or at full scale) on the full-resolution file, and
              (reported, not scored: community-only rule DF 27) whether one value group covers more than half the frame.
  2. focal    Saliency proxy = mean of (a) spectral residual (Hou and Zhang, CVPR 2007; reference not fetched this run) and
              (b) centre-surround contrast of L* and two colour-opponent channels at 3 scales; both normalised, then smoothed.
              dominance = strongest peak / strongest point OUTSIDE the peak's blob (saliency >= half the peak, grown by 2 % of
              the short side). Hierarchy: number of big elements = foreground masses (blurred-L* Otsu class that does not own
              the frame border) of at least 1 % of the frame and at least 25 % of the largest one (the size cut-offs are
              provisional; the "at most 2" pass line is DF 10). Rule-of-thirds distance is reported, NOT scored. With a stated
              subject (--subject-box or --subject-mask): is the peak inside it, saliency lift (mean inside / mean of the frame),
              and does the subject hold the frame's strongest local contrast (p99.5 of local RMS L* inside vs outside).
  3. squint   The frame is resized to fit 320x180 and blurred (sigma = 1 % of its diagonal; parameter not sourced, DF 11 only
              says "a slight blur"), both in LINEAR light (all resizing here averages linear light, as an eye or lens does;
              sRGB-space averaging darkens fine detail). Reports the WCAG contrast ratio between the subject and a ring of
              background around it (mean Y), how much of the full-size subject/background contrast survives (log ratio), and
              how far the 3 value-group shares drift (L1) between full size and squint. With --subject-box: coherence = the
              share of the box that the refined silhouette (one value mass) fills.
  4. edge     Silhouette: --subject-mask as given; --subject-box refined to a silhouette (Otsu on blurred L* inside the box,
              the component with the most saliency); no subject: the same on the whole frame, keeping components of
              0.2 % .. 60 % of the frame that touch at most one frame edge; holes filled. WCAG contrast ratio of a thin band
              inside vs outside the edge (band = 0.6 % of the short side, skipping the 1-2 px next to the outline), the share
              of edge pixels whose local inside/outside ratio reaches 3:1, and the side (top, right, bottom, left) where the
              edge is most often lost.
  5. text     Only with --text-box x,y,w,h,chars (repeatable; original pixels; chars = characters on that line). Per box:
              WCAG contrast ratio between the two Otsu classes of the box (glyphs vs their ground, mean Y; house rule 4.5:1),
              and pixels per character at 320x180 in each axis (box height, box width / chars) against the 4 px floor. The
              tool does not find text by itself.
  6. refs     Optional (--refs DIR: PNG/JPG in DIR and its direct subfolders, treated as untrusted data: only image bytes are
              read, size-capped, nothing else in the folder is opened; only derived numbers and the file path reach the
              report, no reference pixels are copied or embedded). For each reference: Wasserstein distance between L*
              histograms (scipy.stats.wasserstein_distance), L1 between the dark / mid / light shares (fixed bands L* < 33,
              33..66, > 66), difference of RMS contrast (std L*) and of log dominance. Reports the nearest reference and the
              metric most off. Not scored when no reference image is readable (its weight is spread over the other checks).
  7. score    Each metric -> 0..100 (100 at or past "pass", 40 at "fail", linear between, falling to 0 one band past "fail").
              A check's score is the mean of its scored metrics; the overall score is the WEIGHTS-weighted mean. Verdict:
              FAIL below overall_score "fail" or when a floor (text px per character) is broken; WARN below "pass" or when
              any check fails or warns; else PASS. Fixes: failed metrics first (floor breaks at the top), then warns; within each
              group by weight x lost points.

Outputs in --out (default <repo>\work\render_critic): <stem>_critic.json, <stem>_critic.md, <stem>_320x180.png
(fitted inside 320x180, aspect kept), <stem>_squint.png, <stem>_values.png (posterised value-group map at working size, at the
notan k; red = the silhouette used by the squint and edge checks).
Exit codes: 0 PASS, 1 WARN, 2 FAIL, 3 unreadable input / bad arguments (the worst image decides).
CLI: .venv\Scripts\python.exe -B tools\render_critic.py IMAGE [IMAGE ...]
     [--out DIR] [--subject-box x,y,w,h | --subject-mask MASK.png] [--text-box x,y,w,h,chars ...] [--refs DIR]
     (boxes are in pixels of the original image; a mask is any PNG/JPG, non-black = subject, resized to the image.)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import warnings

import numpy as np
from scipy import ndimage
from scipy.cluster.vq import kmeans2, vq
from scipy.stats import wasserstein_distance

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

BRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the repository folder
DEFAULT_OUT = os.path.join(BRAIN, "work", "render_critic")
WORK_LONG = 1280          # working resolution (long side, px); full resolution is used only for clipping
SAL_LONG = 480            # saliency resolution (long side, px)
THUMB = (320, 180)        # squint / text-floor test size (w, h): OUR test size, not a YouTube display size (TR A19)
SIL_BLUR = 0.02           # blur (fraction of the short side) before Otsu for silhouettes: merges dot fields. Not sourced.
SQUINT_SIGMA = 0.01       # squint blur, fraction of the 320x180 diagonal. Parameter not sourced (DF 11: "a slight blur").
REF_MAX_BYTES = 60 * 1024 * 1024
REF_MAX_FILES = 12
MAX_PIXELS = 100_000_000  # any image above 100 MP is rejected after decode (decode itself is not capped)
REF_EXT = (".png", ".jpg", ".jpeg")
P = "provisional, no source yet"
DF, TR, PL = "DF", "TR", "PL"   # source code prefixes; each "DF n" / "TR An" / "PL n" resolves through SOURCE_URLS
_WCAG = "https://www.w3.org/TR/WCAG22/"
_WCAG_TXT = "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html"
_WCAG_NT = "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html"
_NNG = "https://www.nngroup.com/articles/visual-hierarchy-ux-definition/"
SOURCE_URLS = {
    "DF 1": _WCAG, "DF 2": _WCAG, "DF 3": _WCAG, "DF 5": f"{_WCAG} ; {_WCAG_NT}", "DF 7": f"{_WCAG_TXT} ; {_WCAG_NT}",
    "DF 8": f"{_WCAG_TXT} ; {_WCAG_NT}", "DF 9": _NNG, "DF 10": _NNG, "DF 11": _NNG,
    "DF 23": "https://hasler.ece.gatech.edu/Courses/MachineLearning/FoundationalPapers/Itti_Koch_Neiber1998.pdf",
    "DF 26": "https://www.gutenberg.org/cache/epub/45410/pg45410.txt (A. W. Dow, Composition)",
    "DF 27": "https://www.virtualartacademy.com/notan/ (community)",
    "DF 37": "https://openlab.citytech.cuny.edu/woolley-comd3313sp2019/category/reading",
    "DF 38": "https://www.pbs.org/hanshofmann/for_teachers_lesson_1_001.html",
    "TR A14": _WCAG_TXT,
    "TR A16": "https://legge.dl8.umn.edu/sites/legge.psych.umn.edu/files/2020-08/Legge%20Cheung%202004%20Psychophysics%20of%20reading-%20Implications%20for%20displaying%20text.pdf",
    "TR A19": "arithmetic on TR A16 (a 3840x2160 or 1280x720 frame shown at 320x180)",
    "PL 13": "https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html",
    "PL 22": "https://broncolor.swiss/news/how-to-set-up-lights-for-stunning-black-on-black-product-photography",
    "PL 23": "https://broncolor.swiss/news/how-to-photographing-pulso-l",
    "PL 24": "https://www.profoto.com/ie/products/light-shaping-tools/softboxes/rfi-softbox-strip",
}
HOUSE = ("house rule (WCAG exempts picture text and logotypes; measured on rendered pixels, stricter than WCAG's "
         "source-colour method)")

# Each metric: pass / fail value, "better": "high" or "low", "src": source (verified file + row) or the provisional marker.
# "floor": True = a floor, never a pass criterion: below "fail" FAILs the whole image, at or above it scores nothing.
THRESHOLDS = {
    # 1 value structure (notan: 2, 3 or 4 values can pass - DF 26 Dow, DF 27 community)
    "value_range_p2_p98":   {"pass": 60.0, "fail": 35.0, "better": "high", "src": P},   # L* units
    "value_notan_r2":       {"pass": 0.85, "fail": 0.65, "better": "high",
                             "src": f"metric at the smallest k in 2..4 that reaches it (DF 26, 27); the 0.85 / 0.65 "
                                    f"lines are {P}"},
    "value_notan_min_gap":  {"pass": 20.0, "fail": 10.0, "better": "high",
                             "src": f"gap between occupied value groups at the notan k (DF 26, 27); numbers {P}"},
    "value_midtone_share":  {"pass": 0.55, "fail": 0.80, "better": "low",  "src": P},   # share of L* in 30..70 (muddy)
    "value_black_clip_pct": {"pass": 1.0,  "fail": 8.0,  "better": "low",  "src": P},   # % pixels with R=G=B=0
    "value_white_clip_pct": {"pass": 0.5,  "fail": 3.0,  "better": "low",  "src": P},   # % pixels with R=G=B=max
    # 2 focal point and hierarchy
    "focal_dominance":      {"pass": 1.5,  "fail": 1.15, "better": "high",
                             "src": f"single-peak idea from Itti-Koch normalisation (DF 23, derived use, no threshold "
                                    f"in source); numbers {P}"},
    "focal_big_elements":   {"pass": 2.0,  "fail": 4.0,  "better": "low",
                             "src": f"pass = at most 2 big elements, NN/g 'Limit how many elements are big to a maximum of 2' "
                                    f"(DF 10, written for UI design); the fail line 4 and the 'big' size cut-offs are "
                                    f"{P}"},
    "focal_peak_in_subject": {"pass": 1.0, "fail": 0.5,  "better": "high", "src": P},   # 1 = inside, 0 = outside
    "focal_saliency_lift":  {"pass": 1.5,  "fail": 1.0,  "better": "high", "src": P},   # mean saliency subject / frame
    "focal_contrast_holder": {"pass": 1.0, "fail": 0.8,  "better": "high", "src": P},   # p99.5 local contrast in / out
    # 3 squint (method: DF 11 "squint or apply a slight blur"; SQUINT_SIGMA not sourced)
    "squint_contrast_ratio": {"pass": 3.0, "fail": 1.5,  "better": "high",
                              "src": f"3:1 = WCAG 2.2 SC 1.4.11 non-text contrast for graphics (DF 5), {HOUSE}; the "
                                     f"1.5 fail line is {P}"},
    "squint_contrast_survival": {"pass": 0.6, "fail": 0.35, "better": "high", "src": P},  # log ratio squint / full
    "squint_share_drift":   {"pass": 0.25, "fail": 0.50, "better": "low",  "src": P},   # L1 of 3-group shares
    "squint_subject_coherence": {"pass": 0.55, "fail": 0.30, "better": "high", "src": P},  # silhouette / box area
    # 4 edge separation
    "edge_band_ratio":      {"pass": 3.0,  "fail": 1.5,  "better": "high",
                             "src": f"3:1 = WCAG 2.2 SC 1.4.11 for edges / rims (DF 5), {HOUSE}; the 1.5 fail line "
                                    f"is {P}"},
    "edge_coverage":        {"pass": 0.70, "fail": 0.40, "better": "high", "src": P},  # share of edge px >= local min
    "edge_local_min_ratio": {"value": 3.0,
                             "src": f"3:1 = WCAG 2.2 SC 1.4.11 (DF 5), {HOUSE}"},  # local ratio that counts as held
    # 5 text (only with --text-box)
    "text_contrast_ratio":  {"pass": 4.5,  "fail": 3.0,  "better": "high",
                             "src": f"4.5:1 = WCAG 2.2 SC 1.4.3 text (DF 3, TR A14), {HOUSE}; the 3.0 fail line "
                                    f"(WCAG's large-text figure) is {P}"},
    "text_px_per_char_320": {"pass": 4.0,  "fail": 4.0,  "better": "high", "floor": True,
                             "src": f"floor: at least 4 px per character in each axis at 320x180, Legge and Cheung 2004 "
                                    f"'4x4 samples per character' (TR A16, A19); below = FAIL, never a pass "
                                    f"criterion; 320x180 is our test size, not a YouTube display size"},
    # 6 references (distance to the NEAREST reference)
    "ref_hist_wasserstein": {"pass": 8.0,  "fail": 20.0, "better": "low",  "src": P},   # L* units
    "ref_share_l1":         {"pass": 0.20, "fail": 0.45, "better": "low",  "src": P},
    "ref_contrast_diff":    {"pass": 5.0,  "fail": 12.0, "better": "low",  "src": P},   # |std L* difference|
    "ref_dominance_logdiff": {"pass": 0.25, "fail": 0.60, "better": "low", "src": P},   # |ln dominance ratio|
    # 7 overall
    "overall_score":        {"pass": 75.0, "fail": 55.0, "better": "high", "src": P},
}
WEIGHTS = {"value": 0.27, "focal": 0.18, "squint": 0.18, "edge": 0.14, "text": 0.10, "refs": 0.13}   # provisional, no source yet

LIMITS = [
    "A proxy, not taste: it measures value, contrast and saliency statistics; it cannot judge idea, story, mood, style, "
    "drawing, anatomy, likeness, colour harmony, material believability or whether the image is interesting.",
    "Low-key and high-key images are legitimate styles; the value thresholds are one-size-fits-all and mostly provisional.",
    "Saliency is a low-level proxy (spectral residual + centre-surround contrast); it ignores faces, text and meaning, "
    "which dominate where real viewers look.",
    "The automatic subject (no --subject-box / --subject-mask) is Otsu on the blurred frame: on cluttered or low-contrast "
    "frames it can pick the wrong region, and the 'peak in subject' and 'holds the contrast' metrics are then not scored.",
    "Every silhouette not given as --subject-mask is a light/dark mass, not the object: a chiaroscuro subject whose shadow "
    "side merges with the background is outlined by its lit part only, and the edge check then measures the terminator.",
    "Calibration is thin: in the first calibration a plain halftone graphic scored within 2 points of a reference thumbnail "
    "used as the quality floor (86.3 vs 88.1, auto subject), because simple bright-on-black graphics pass value and focal "
    "statistics easily; a high score is not 'good art'.",
    "Text is not detected: the text check runs only on --text-box regions, and its 4.5:1 / 3:1 contrast lines are a house "
    "rule (WCAG exempts picture text and logotypes) measured on rendered pixels.",
    "'Big elements' are value masses after a blur, not semantic objects; the 'at most 2' line comes from UI design guidance.",
    "Rule-of-thirds distance is reported only; it is a convention, not a quality measure. Warm/cool is not judged (a depth "
    "cue only in the verified sources).",
    "Reference distance says 'different from these images', not 'worse': a good image can be far from the references.",
    "Alpha is composited over black; colour management is assumed sRGB (an AgX/Filmic PNG is display-referred sRGB).",
]


# ---------------------------------------------------------------- image helpers
def read_image(path: str) -> tuple[np.ndarray, dict]:
    """-> float RGB in 0..1 (H, W, 3) and info (alpha composited over black). Raises ValueError when unreadable."""
    import open3d as o3d  # lazy: slow import
    if not os.path.isfile(path):
        raise ValueError(f"not a file: {path}")
    if path.isascii():
        arr = np.asarray(o3d.io.read_image(path))
    else:   # open3d cannot open non-ASCII paths on Windows: read a byte copy under an ASCII temp name, then delete it
        import shutil
        import tempfile
        fd, tmp = tempfile.mkstemp(suffix=os.path.splitext(path)[1].lower() or ".png")
        os.close(fd)
        try:
            shutil.copyfile(path, tmp)
            arr = np.asarray(o3d.io.read_image(tmp))
        finally:
            os.remove(tmp)
    if arr.size == 0:
        raise ValueError(f"open3d could not read: {path}")
    if arr.shape[0] * arr.shape[1] > MAX_PIXELS:
        raise ValueError(f"image over {MAX_PIXELS} px, skipped: {path}")
    info = {"shape": list(arr.shape), "dtype": str(arr.dtype)}
    peak = 65535.0 if arr.dtype == np.uint16 else 255.0
    if arr.ndim == 2:
        arr = np.repeat(arr[:, :, None], 3, axis=2)
    if arr.shape[2] == 4:
        a = arr[:, :, 3].astype(np.float64) / peak
        info["alpha_below_1_pct"] = round(float((a < 0.999).mean() * 100), 3)
        rgb_raw = arr[:, :, :3]
        rgb = rgb_raw.astype(np.float64) / peak * a[:, :, None]
    else:
        rgb_raw = arr[:, :, :3]
        rgb = rgb_raw.astype(np.float64) / peak
    # clip counts on the alpha-composited values: transparent pixels count as black
    comp = np.round(rgb * peak)
    info["black_clip_pct"] = round(float((comp <= 0).all(axis=2).mean() * 100), 4)
    info["white_clip_pct"] = round(float((comp >= peak).all(axis=2).mean() * 100), 4)
    info["any_channel_255_pct"] = round(float((rgb_raw >= peak).any(axis=2).mean() * 100), 4)
    return np.clip(rgb, 0.0, 1.0), info


def write_png(path: str, img01: np.ndarray) -> None:
    import open3d as o3d
    a = np.clip(np.round(img01 * 255.0), 0, 255).astype(np.uint8)
    if a.ndim == 2:
        a = np.repeat(a[:, :, None], 3, axis=2)
    if not o3d.io.write_image(path, o3d.geometry.Image(np.ascontiguousarray(a))):
        raise OSError(f"open3d could not write {path}")


def resize(img: np.ndarray, oh: int, ow: int, order: int = 1) -> np.ndarray:
    """area-aware resize: Gaussian prefilter on downscale, then sampling at pixel centres (exact output shape)"""
    h, w = img.shape[:2]
    fy, fx = h / oh, w / ow
    src = img.astype(np.float64)
    if order > 0 and (fy > 1 or fx > 1):
        sig = [max(0.0, (fy - 1) / 2), max(0.0, (fx - 1) / 2)] + ([0.0] if img.ndim == 3 else [])
        src = ndimage.gaussian_filter(src, sig, mode="nearest")
    yy = (np.arange(oh) + 0.5) * fy - 0.5
    xx = (np.arange(ow) + 0.5) * fx - 0.5
    gy, gx = np.meshgrid(yy, xx, indexing="ij")
    if img.ndim == 2:
        return ndimage.map_coordinates(src, [gy, gx], order=order, mode="nearest")
    return np.stack([ndimage.map_coordinates(src[:, :, c], [gy, gx], order=order, mode="nearest")
                     for c in range(img.shape[2])], axis=2)


def fit_size(h: int, w: int, box_w: int, box_h: int) -> tuple[int, int]:
    s = min(box_w / w, box_h / h, 1.0)
    return max(1, int(round(h * s))), max(1, int(round(w * s)))


def srgb_to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def rel_luminance(rgb: np.ndarray) -> np.ndarray:
    return lin_luminance(srgb_to_linear(rgb))


def lin_luminance(lin: np.ndarray) -> np.ndarray:
    return lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722


def to_work(rgb_srgb: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """resize to the working size IN LINEAR LIGHT (averaging like the eye and a lens do), -> (linear, sRGB-encoded)"""
    h, w = rgb_srgb.shape[:2]
    wh, ww = fit_size(h, w, WORK_LONG, WORK_LONG)
    lin = resize(srgb_to_linear(rgb_srgb), wh, ww)
    return lin, linear_to_srgb(lin)


def lstar(y: np.ndarray) -> np.ndarray:
    d = 6 / 29
    f = np.where(y > d ** 3, np.cbrt(np.maximum(y, 0)), y / (3 * d * d) + 4 / 29)
    return 116 * f - 16


def lstar_to_y(l: np.ndarray) -> np.ndarray:
    d = 6 / 29
    f = (np.asarray(l, dtype=np.float64) + 16) / 116
    return np.where(f > d, f ** 3, 3 * d * d * (f - 4 / 29))


def wcag(y1: float, y2: float) -> float:
    hi, lo = max(y1, y2), min(y1, y2)
    return (hi + 0.05) / (lo + 0.05)


def otsu(values: np.ndarray, lo: float = 0.0, hi: float = 100.0) -> float:
    hist, edges = np.histogram(values, 256, (lo, hi))
    c = (edges[:-1] + edges[1:]) / 2
    p = hist / max(1, hist.sum())
    om = np.cumsum(p)
    mu = np.cumsum(p * c)
    with np.errstate(divide="ignore", invalid="ignore"):
        sb = (mu[-1] * om - mu) ** 2 / (om * (1 - om))
    sb = np.nan_to_num(sb, nan=0.0, posinf=0.0)
    return float(c[int(np.argmax(sb))])


# ---------------------------------------------------------------- 1 value structure
def kmeans_l(l: np.ndarray, k: int) -> dict:
    flat = l.ravel()
    step = max(1, flat.size // 300_000)
    sample = flat[::step].astype(np.float64)
    total_var = float(sample.var())
    lo, hi = np.percentile(sample, [1, 99])
    if total_var < 1e-6 or hi - lo < 1e-6:
        centres = np.full(k, float(sample.mean()))
    else:
        # deterministic start: centres evenly spaced between p1 and p99 (a quantile start collapses on poster images)
        init = np.linspace(lo, hi, k).reshape(-1, 1)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")      # an empty cluster is expected on poster images; it is handled below
            cb, _ = kmeans2(sample.reshape(-1, 1), init, iter=40, minit="matrix", missing="warn")
        centres = np.sort(cb.ravel())
    lab, _ = vq(flat.reshape(-1, 1).astype(np.float64), centres.reshape(-1, 1))
    shares = np.bincount(lab, minlength=k) / flat.size
    within = float(np.sum((flat - centres[lab]) ** 2) / flat.size)
    full_var = float(flat.var())
    r2 = 0.0 if full_var < 1e-6 else max(0.0, 1.0 - within / full_var)
    occupied = centres[shares >= 0.005]          # a group under 0.5 % of the frame is not a value group
    gaps = np.diff(occupied)
    return {"k": k, "centres_lstar": [round(float(c), 2) for c in centres], "shares": [round(float(s), 4) for s in shares],
            "r2": round(r2, 4), "min_gap": round(float(gaps.min()) if gaps.size else 0.0, 2), "_labels": lab.reshape(l.shape)}


def value_check(l: np.ndarray, info: dict) -> tuple[dict, dict]:
    p2, p98 = np.percentile(l, [2, 98])
    km = {k: kmeans_l(l, k) for k in (2, 3, 4, 5)}
    # notan: 2, 3 or 4 values can pass (DF 26, DF 27): the smallest k in 2..4 that reaches the R^2 pass line, else the best
    r2_pass = THRESHOLDS["value_notan_r2"]["pass"]
    reach = [k for k in (2, 3, 4) if km[k]["r2"] >= r2_pass]
    nk = reach[0] if reach else max((2, 3, 4), key=lambda k: (km[k]["r2"], -k))
    mid = float(((l >= 30) & (l <= 70)).mean())
    mean_l = float(l.mean())
    key = "low-key" if mean_l < 35 else ("high-key" if mean_l > 65 else "mid-key")
    metrics = {
        "value_range_p2_p98": round(float(p98 - p2), 2),
        "value_notan_r2": km[nk]["r2"],
        "value_notan_min_gap": km[nk]["min_gap"],
        "value_midtone_share": round(mid, 4),
        "value_black_clip_pct": info["black_clip_pct"],
        "value_white_clip_pct": info["white_clip_pct"],
    }
    extra = {"mean_lstar": round(mean_l, 2), "key": key, "p2": round(float(p2), 2), "p98": round(float(p98), 2),
             "std_lstar": round(float(l.std()), 2), "any_channel_255_pct": info["any_channel_255_pct"],
             "notan_k": nk, "notan_shares": km[nk]["shares"], "notan_centres_lstar": km[nk]["centres_lstar"],
             "one_value_over_half": bool(max(km[nk]["shares"]) > 0.5),
             "one_value_over_half_note": f"reported, not scored: community-only rule (DF 27)",
             "kmeans": {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")} for k, v in km.items()}}
    return metrics, {"extra": extra, "labels3": km[nk]["_labels"], "centres3": km[nk]["centres_lstar"],
                     "shares3": km[3]["shares"]}


# ---------------------------------------------------------------- 2 saliency / focal point
def saliency(rgb: np.ndarray, l: np.ndarray) -> np.ndarray:
    h, w = l.shape
    sh, sw = fit_size(h, w, SAL_LONG, SAL_LONG)
    ls = resize(l, sh, sw)
    cs = resize(rgb, sh, sw)
    short = min(sh, sw)
    if ls.std() < 0.5 and cs.std(axis=(0, 1)).max() < 0.005:
        return np.zeros((h, w))     # a flat frame has no attention structure (FFT noise would invent peaks)
    # (a) spectral residual
    F = np.fft.fft2(ls)
    amp = np.log(np.abs(F) + 1e-9)
    res = amp - ndimage.uniform_filter(amp, 3, mode="nearest")
    sr = np.abs(np.fft.ifft2(np.exp(res + 1j * np.angle(F)))) ** 2
    sr = ndimage.gaussian_filter(sr, 0.03 * short)
    # (b) centre-surround on L* and opponent colour (sRGB-encoded x100 so units are comparable with L*)
    rg = (cs[..., 0] - cs[..., 1]) * 100
    by = (cs[..., 2] - (cs[..., 0] + cs[..., 1]) / 2) * 100
    csm = np.zeros_like(ls)
    for frac in (0.01, 0.02, 0.04):
        sc = max(1.0, frac * short)
        for ch in (ls, rg, by):
            csm += np.abs(ndimage.gaussian_filter(ch, sc) - ndimage.gaussian_filter(ch, 4 * sc))
    out = np.zeros_like(ls)
    for m in (sr, csm):
        mx = float(m.max())
        if mx > 0:
            out += m / mx
    out = ndimage.gaussian_filter(out, 0.02 * math.hypot(sh, sw))
    return resize(out, h, w)


def local_rms(l: np.ndarray, sigma: float) -> np.ndarray:
    m = ndimage.gaussian_filter(l, sigma)
    m2 = ndimage.gaussian_filter(l * l, sigma)
    return np.sqrt(np.maximum(m2 - m * m, 0))


def dominance(sal: np.ndarray) -> tuple[float, tuple[float, int, int], tuple[float, int, int]]:
    """peak1 = global max; its blob = connected region where saliency >= 0.5 x peak1, grown by 2 % of the short side;
    peak2 = the strongest saliency OUTSIDE that blob (the competing area). dominance = peak1 / peak2 (capped at 10)."""
    h, w = sal.shape
    i1 = int(np.argmax(sal))
    y1, x1 = divmod(i1, w)
    v1 = float(sal[y1, x1])
    if v1 <= 0:
        return 1.0, (0.0, y1, x1), (0.0, -1, -1)
    lab, _ = ndimage.label(sal >= 0.5 * v1)
    blob = lab == lab[y1, x1]
    grow = max(1.0, 0.02 * min(h, w))
    blob = ndimage.distance_transform_edt(~blob) <= grow
    if blob.all():
        return 10.0, (v1, y1, x1), (0.0, -1, -1)
    out = np.where(blob, -np.inf, sal)
    i2 = int(np.argmax(out))
    y2, x2 = divmod(i2, w)
    v2 = float(sal[y2, x2])
    dom = 10.0 if v2 <= 0 else min(10.0, v1 / v2)
    return dom, (v1, y1, x1), (v2, y2, x2)


def big_elements(l: np.ndarray) -> tuple[int, list]:
    """Hierarchy proxy (DF 10: at most 2 big elements). Foreground = the Otsu class of blurred L* (SIL_BLUR) that does NOT
    own most of the frame border; big = a connected foreground mass of >= 1 % of the frame and >= 25 % of the largest mass
    (both cut-offs provisional, no source yet). -> (count, boxes as normalised [x, y, w, h])."""
    h, w = l.shape
    if l.std() < 1.0:
        return 0, []
    sq = ndimage.gaussian_filter(l, SIL_BLUR * min(h, w))
    t = otsu(sq)
    border = np.concatenate([sq[0, :], sq[-1, :], sq[:, 0], sq[:, -1]])
    fg = sq <= t if (border > t).mean() > 0.5 else sq > t
    lab, n = ndimage.label(fg)
    if n == 0:
        return 0, []
    area = np.bincount(lab.ravel(), minlength=n + 1)[1:].astype(np.float64)
    big = np.nonzero((area >= 0.01 * h * w) & (area >= 0.25 * area.max()))[0]
    boxes = []
    for sl in ndimage.find_objects(lab):
        boxes.append(sl)
    out = []
    for j in big:
        ys, xs = boxes[j]
        out.append([round(xs.start / w, 3), round(ys.start / h, 3), round((xs.stop - xs.start) / w, 3),
                    round((ys.stop - ys.start) / h, 3)])
    return len(big), out


def focal_check(rgb, l, sal, subj, subj_given) -> tuple[dict, dict]:
    h, w = l.shape
    dom, (v1, y1, x1), (v2, y2, x2) = dominance(sal)
    nx, ny = x1 / max(1, w - 1), y1 / max(1, h - 1)
    diag = math.hypot(w, h)
    thirds = min(math.hypot((nx - a) * w, (ny - b) * h) for a in (1 / 3, 2 / 3) for b in (1 / 3, 2 / 3)) / diag
    flat = sal.ravel()
    top = np.sort(flat)[::-1]
    conc = float(top[: max(1, flat.size // 20)].sum() / max(1e-12, flat.sum()))
    n_big, big_boxes = big_elements(l)
    metrics = {"focal_dominance": round(dom, 3)}
    if n_big >= 1:      # no foreground mass at all is not "few big elements": then the metric is not scored
        metrics["focal_big_elements"] = float(n_big)
    extra = {"big_elements": n_big, "big_element_boxes_norm_xywh": big_boxes,
             "peak1_xy_work": [x1, y1], "peak1_xy_norm": [round(nx, 3), round(ny, 3)],
             "peak2_xy_work": [x2, y2] if x2 >= 0 else None,
             "peak2_xy_norm": [round(x2 / max(1, w - 1), 3), round(y2 / max(1, h - 1), 3)] if x2 >= 0 else None,
             "thirds_distance_diag": round(thirds, 4), "centre_distance_diag":
             round(math.hypot((nx - 0.5) * w, (ny - 0.5) * h) / diag, 4),
             "saliency_mass_top5pct": round(conc, 4), "scored_subject_metrics": bool(subj_given)}
    if subj is not None and subj.any() and subj_given:
        metrics["focal_peak_in_subject"] = 1.0 if subj[y1, x1] else 0.0
        metrics["focal_saliency_lift"] = round(float(sal[subj].mean() / max(1e-12, sal.mean())), 3)
        rms = local_rms(l, max(1.0, 0.02 * min(h, w)))
        if (~subj).any():
            metrics["focal_contrast_holder"] = round(float(np.percentile(rms[subj], 99.5) /
                                                           max(1e-9, np.percentile(rms[~subj], 99.5))), 3)
    return metrics, extra


# ---------------------------------------------------------------- subject mask
def subject_mask(l: np.ndarray, sal: np.ndarray, args, orig_hw):
    """-> (silhouette or None, stated region or None, description). The stated region (mask or box) is what the focal
    metrics test; the silhouette is what the squint and edge checks use (a box is refined to the value mass inside it)."""
    h, w = l.shape
    oh, ow = orig_hw
    if args.subject_mask:
        m_rgb, _ = read_image(args.subject_mask)
        m = resize(m_rgb.max(axis=2), h, w, order=0) > 0.5
        if not m.any() or m.all():
            raise ValueError(f"subject mask is empty or covers the whole frame: {args.subject_mask}")
        return m, m, f"mask {args.subject_mask}"
    if args.subject_box:
        x, y, bw, bh = [float(v) for v in args.subject_box.split(",")]
        sx, sy = w / ow, h / oh
        box = np.zeros((h, w), bool)
        box[max(0, int(y * sy)):min(h, int((y + bh) * sy)), max(0, int(x * sx)):min(w, int((x + bw) * sx))] = True
        if not box.any():
            raise ValueError(f"--subject-box {args.subject_box} lies outside the image ({ow} x {oh})")
        m, t = silhouette(l, sal, box)
        if m is None:
            return box, box, f"box {args.subject_box} (original px; no silhouette found inside, the box itself is used)"
        return m, box, (f"box {args.subject_box} (original px) refined to a silhouette: Otsu L* {t:.1f} on the "
                        f"blurred frame inside the box")
    m, t = silhouette(l, sal, None)
    if m is None:
        return None, None, "auto: no separable subject (no component of 0.2 % .. 60 % of the frame off the frame edges)"
    return m, None, (f"auto: Otsu L* {t:.1f} on the blurred frame, the component with the most saliency that touches at "
                     f"most one frame edge, holes filled")


def silhouette(l: np.ndarray, sal: np.ndarray, region: np.ndarray | None) -> tuple[np.ndarray | None, float]:
    """Otsu on L* blurred by SIL_BLUR (inside region if given). The class owning most of the region/frame border is taken as
    background; among the connected components of the other class pick the one with the largest saliency mass (fall back
    to the background class only when the other has no valid component). Auto mode: area 0.2 % .. 60 % of the frame and
    touching at most one frame edge. Region mode: area >= 5 % of the region. The outline is then refined (refine())."""
    h, w = l.shape
    sq = ndimage.gaussian_filter(l, SIL_BLUR * min(h, w))
    t = otsu(sq[region] if region is not None else sq)
    area_ref = float(region.sum()) if region is not None else float(h * w)
    # the background is the class that owns most of the region's (or frame's) border: try the other class first
    reg = region if region is not None else np.ones((h, w), bool)
    border = reg & (ndimage.distance_transform_edt(reg) <= 1.0)
    bright_border_share = float((sq[border] > t).mean()) if border.any() else 0.5
    classes = [sq > t, sq <= t] if bright_border_share <= 0.5 else [sq <= t, sq > t]
    for cls in classes:
        best, best_score = None, 0.0
        c = cls & region if region is not None else cls
        lab, n = ndimage.label(c)
        if n == 0:
            continue
        flat = lab.ravel()
        area = np.bincount(flat, minlength=n + 1)[1:].astype(np.float64)
        mass = np.bincount(flat, weights=sal.ravel(), minlength=n + 1)[1:]
        ok = np.ones(n, bool)
        if region is None:
            touch = np.zeros(n, int)
            for edge in (lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]):
                ids = np.unique(edge[edge > 0]) - 1
                touch[ids] += 1
            ok &= (touch <= 1) & (area >= 0.002 * area_ref) & (area <= 0.60 * area_ref)
        else:
            ok &= area >= 0.05 * area_ref
        if not ok.any():
            continue
        score = np.where(ok, mass + 1e-9 * area, -1.0)
        j = int(np.argmax(score))
        if score[j] > best_score:
            best_score, best = float(score[j]), lab == j + 1
        if best is not None:
            bright = bool(sq[best].mean() > t)
            return refine(l, best, t, bright, region), t
    return None, t


def refine(l: np.ndarray, comp: np.ndarray, t: float, bright: bool, region: np.ndarray | None) -> np.ndarray:
    """The blurred component's outline sits up to ~SIL_BLUR away from the true edge (measured on the 3-value control: the
    inner band landed in the background). Re-threshold a lightly blurred L* (sigma 1 px) near the component, then close
    with radius r = 2 x SIL_BLUR (merges dot fields into one mass, keeps a solid shape's true edge) and fill holes."""
    h, w = l.shape
    r = 2.0 * SIL_BLUR * min(h, w)
    sharp = ndimage.gaussian_filter(l, 1.0)
    cls = sharp > t if bright else sharp <= t
    near = ndimage.distance_transform_edt(~comp) <= r
    x = cls & near
    if region is not None:
        x &= region
    if not x.any():
        return ndimage.binary_fill_holes(comp)
    dil = ndimage.distance_transform_edt(~x) <= r
    closed = ndimage.distance_transform_edt(dil) > r
    out = ndimage.binary_fill_holes(closed | x)
    if region is not None:
        out &= region
    lab, n = ndimage.label(out)
    if n > 1:   # keep the piece that overlaps the chosen component most
        ov = np.bincount(lab[comp], minlength=n + 1)
        ov[0] = 0
        out = lab == int(np.argmax(ov))
    return out if out.any() else ndimage.binary_fill_holes(comp)


# ---------------------------------------------------------------- 3 squint
def ring(mask: np.ndarray, frac: float) -> np.ndarray:
    r = max(2, int(frac * min(mask.shape)))
    rg = ~mask & (ndimage.distance_transform_edt(~mask) <= r)
    return rg if rg.any() else ~mask


def squint_check(lin, l, y, subj, km_shares, region=None) -> tuple[dict, dict]:
    """lin = working image in LINEAR light; the downscale and the blur happen in linear light, saved images are sRGB."""
    h, w = l.shape
    th, tw = fit_size(h, w, *THUMB)
    thumb_lin = resize(lin, th, tw)
    sig = SQUINT_SIGMA * math.hypot(th, tw)     # parameter not sourced (DF 11: "squint or apply a slight blur")
    sq_lin = ndimage.gaussian_filter(thumb_lin, [sig, sig, 0], mode="nearest")
    ysq = lin_luminance(sq_lin)
    lsq = lstar(ysq)
    thumb, sq = linear_to_srgb(thumb_lin), linear_to_srgb(sq_lin)
    km = kmeans_l(lsq, 3)
    drift = float(np.abs(np.array(km["shares"]) - np.array(km_shares)).sum())
    # a frame with no value structure cannot "keep" it: drift is only scored when the frame has some (std L* >= 2)
    metrics = {"squint_share_drift": round(drift, 4)} if l.std() >= 2.0 else {}
    extra = {"thumb_size": [tw, th], "blur_sigma_px": round(sig, 2), "squint_k3": {kk: vv for kk, vv in km.items()
                                                                                  if not kk.startswith("_")}}
    if region is not None and subj is not None and region is not subj:
        # box mode: how much of the stated subject box reads as ONE value mass (the refined silhouette)
        metrics["squint_subject_coherence"] = round(float((subj & region).sum() / max(1, region.sum())), 4)
    if subj is not None:
        rg_full = ring(subj, 0.08)
        yin, yout = float(y[subj].mean()), float(y[rg_full].mean())
        cf = wcag(yin, yout)
        ms = resize(subj.astype(np.float64), th, tw, order=0) > 0.5
        if ms.any() and (~ms).any():
            rg_s = ring(ms, 0.08)
            cs = wcag(float(ysq[ms].mean()), float(ysq[rg_s].mean()))
            metrics["squint_contrast_ratio"] = round(cs, 3)
            if math.log(cf) > 0.05:
                metrics["squint_contrast_survival"] = round(math.log(cs) / math.log(cf), 3)
            extra.update({"full_contrast_ratio": round(cf, 3), "subject_lstar_std_full": round(float(l[subj].std()), 2),
                          "subject_lstar_std_squint": round(float(lsq[ms].std()), 2),
                          "subject_mean_lstar_squint": round(float(lsq[ms].mean()), 2),
                          "ring_mean_lstar_squint": round(float(lsq[rg_s].mean()), 2)})
        else:
            metrics["squint_contrast_ratio"] = 1.0
    else:
        metrics["squint_contrast_ratio"] = 1.0
        extra["note"] = "no separable subject: contrast ratio set to 1.0"
    return metrics, {"extra": extra, "thumb": thumb, "squint": sq}


# ---------------------------------------------------------------- 4 edge separation
def edge_check(y, subj) -> tuple[dict, dict]:
    if subj is None or not subj.any() or subj.all():
        return {"edge_band_ratio": 1.0, "edge_coverage": 0.0}, {"note": "no separable subject silhouette"}
    h, w = y.shape
    band = max(2, int(round(0.006 * min(h, w))))
    d_in = ndimage.distance_transform_edt(subj)
    d_out = ndimage.distance_transform_edt(~subj)
    # the bands skip the 1-2 px next to the outline (anti-aliasing and the +-1 px threshold position mix both sides)
    inner = subj & (d_in > 1.5) & (d_in <= band + 1.5)
    outer = ~subj & (d_out > 1.5) & (d_out <= band + 1.5)
    if not inner.any() or not outer.any():
        return {"edge_band_ratio": 1.0, "edge_coverage": 0.0}, {"note": "band empty"}
    yin, yout = float(y[inner].mean()), float(y[outer].mean())
    ratio = wcag(yin, yout)
    win = 4 * band + 1
    fi = inner.astype(np.float64)
    fo = outer.astype(np.float64)
    min_i = ndimage.uniform_filter(fi, win)
    min_o = ndimage.uniform_filter(fo, win)
    mi = ndimage.uniform_filter(y * fi, win) / np.maximum(min_i, 1e-9)
    mo = ndimage.uniform_filter(y * fo, win) / np.maximum(min_o, 1e-9)
    edge = subj & (d_in <= 1.0)
    ok = edge & (min_i > 1e-6) & (min_o > 1e-6)
    hi, lo = np.maximum(mi, mo), np.minimum(mi, mo)
    loc = (hi + 0.05) / (lo + 0.05)
    need = THRESHOLDS["edge_local_min_ratio"]["value"]
    held = ok & (loc >= need)
    cov = float(held.sum() / max(1, ok.sum()))
    cy, cx = ndimage.center_of_mass(subj)
    ys, xs = np.nonzero(ok)
    ang = np.degrees(np.arctan2(-(ys - cy), xs - cx))   # 0 = right, 90 = top
    side = np.select([(ang >= 45) & (ang < 135), (ang >= -45) & (ang < 45), (ang >= -135) & (ang < -45)],
                     ["top", "right", "bottom"], "left")
    lost = ~held[ys, xs]
    per_side = {s: round(float(lost[side == s].mean()), 3) if (side == s).any() else None
                for s in ("top", "right", "bottom", "left")}
    worst = max((s for s in per_side if per_side[s] is not None), key=lambda s: per_side[s], default=None)
    return ({"edge_band_ratio": round(ratio, 3), "edge_coverage": round(cov, 4)},
            {"band_px_work": band, "inside_mean_lstar": round(float(lstar(np.array(yin))), 2),
             "outside_mean_lstar": round(float(lstar(np.array(yout))), 2), "lost_share_by_side": per_side,
             "worst_side": worst, "edge_px": int(ok.sum()), "inside_brighter": yin > yout})


def text_check(rgb_full: np.ndarray, boxes: list[str]) -> tuple[dict, dict]:
    """--text-box x,y,w,h,chars (original px). Contrast on ORIGINAL pixels: Otsu on L* inside the box splits glyphs from
    their ground; WCAG ratio of the two classes' mean Y (house rule 4.5:1, DF 3 / TR A14). Pixels per character at the
    320x180 test size in each axis (height = box h, width = box w / chars) against the 4 px floor (TR A16, A19).
    The worst box decides each metric."""
    if not boxes:
        return {}, {"note": "no --text-box given; the tool does not detect text, so text is not checked"}
    oh, ow = rgb_full.shape[:2]
    s = min(THUMB[0] / ow, THUMB[1] / oh, 1.0)
    rows = []
    for b in boxes:
        x, y, bw, bh, ch = [float(v) for v in b.split(",")]
        x0, y0 = max(0, int(x)), max(0, int(y))
        x1, y1 = min(ow, int(x + bw)), min(oh, int(y + bh))
        if x1 - x0 < 2 or y1 - y0 < 2:
            raise ValueError(f"--text-box {b} lies outside the image ({ow} x {oh})")
        crop = rgb_full[y0:y1, x0:x1]
        yy = rel_luminance(crop)
        ll = lstar(yy)
        t = otsu(ll)
        hi, lo = yy[ll > t], yy[ll <= t]
        ratio = wcag(float(hi.mean()), float(lo.mean())) if hi.size and lo.size else 1.0
        px_h, px_w = bh * s, bw * s / max(1.0, ch)
        rows.append({"box": b, "contrast_ratio": round(ratio, 3), "px_per_char_h_320": round(px_h, 2),
                     "px_per_char_w_320": round(px_w, 2), "glyph_share": round(float(min(hi.size, lo.size) / ll.size), 3)})
    metrics = {"text_contrast_ratio": min(r["contrast_ratio"] for r in rows),
               "text_px_per_char_320": min(min(r["px_per_char_h_320"], r["px_per_char_w_320"]) for r in rows)}
    return metrics, {"boxes": rows, "scale_to_320x180": round(s, 5),
                     "note": "glyph/ground split by Otsu inside each box (the minority class is taken as the glyphs)"}


def band_shares(l: np.ndarray) -> np.ndarray:
    """share of pixels in fixed absolute value bands: dark L* < 33, mid 33..66, light > 66 (comparable across images,
    unlike k-means groups whose centres move with each image)"""
    return np.array([(l < 33).mean(), ((l >= 33) & (l <= 66)).mean(), (l > 66).mean()], dtype=np.float64)


# ---------------------------------------------------------------- 5 references
def features(path: str) -> dict:
    rgb_full, _ = read_image(path)
    lin, rgb = to_work(rgb_full)
    l = lstar(lin_luminance(lin))
    km = kmeans_l(l, 3)
    sal = saliency(rgb, l)
    dom = dominance(sal)[0]
    hist, edges = np.histogram(l, 100, (0, 100))
    return {"hist": hist / max(1, hist.sum()), "centres": (edges[:-1] + edges[1:]) / 2, "shares": band_shares(l),
            "std": float(l.std()), "dom": dom}


def list_refs(d: str) -> tuple[list[str], list[str]]:
    """PNG/JPG files in d and its direct subfolders (one folder per reference is a convenient way to file them). Nothing
    else in the folder is opened: the folder is untrusted data and only image pixels are read."""
    keep, skipped = [], []
    if not d or not os.path.isdir(d):
        return keep, skipped
    cand = []
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if os.path.isdir(p) and not os.path.islink(p):
            cand += [os.path.join(p, n) for n in sorted(os.listdir(p))]
        else:
            cand.append(p)
    for p in cand:
        if not os.path.isfile(p) or os.path.islink(p) or not p.lower().endswith(REF_EXT):
            continue
        if os.path.getsize(p) > REF_MAX_BYTES:
            skipped.append(f"{p} (over {REF_MAX_BYTES} bytes)")
            continue
        keep.append(p)
    if len(keep) > REF_MAX_FILES:
        skipped += [f"{p} (over {REF_MAX_FILES} files)" for p in keep[REF_MAX_FILES:]]
        keep = keep[:REF_MAX_FILES]
    return keep, skipped


def refs_check(me: dict, ref_paths: list[str], cache: dict) -> tuple[dict, dict]:
    rows = []
    for p in ref_paths:
        try:
            f = cache[p] if p in cache else cache.setdefault(p, features(p))
        except ValueError as e:
            rows.append({"ref": p, "error": str(e)})
            continue
        d = {"ref_hist_wasserstein": float(wasserstein_distance(me["centres"], f["centres"], me["hist"], f["hist"])),
             "ref_share_l1": float(np.abs(me["shares"] - f["shares"]).sum()),
             "ref_contrast_diff": abs(me["std"] - f["std"]),
             "ref_dominance_logdiff": abs(math.log(me["dom"] / f["dom"]))}
        norm = {k: v / THRESHOLDS[k]["fail"] for k, v in d.items()}
        rows.append({"ref": p, **{k: round(v, 4) for k, v in d.items()}, "mean_norm": round(sum(norm.values()) / 4, 4),
                     "most_off": max(norm, key=norm.get), "ref_std_lstar": round(f["std"], 2),
                     "ref_dominance": round(f["dom"], 3), "ref_shares": [round(float(s), 4) for s in f["shares"]]})
    good = [r for r in rows if "error" not in r]
    if not good:
        return {}, {"rows": rows, "note": "no readable reference image"}
    best = min(good, key=lambda r: r["mean_norm"])
    metrics = {k: best[k] for k in ("ref_hist_wasserstein", "ref_share_l1", "ref_contrast_diff", "ref_dominance_logdiff")}
    return metrics, {"rows": rows, "nearest": best["ref"], "most_off_metric": best["most_off"]}


# ---------------------------------------------------------------- scoring and fixes
def score_metric(name: str, v: float) -> tuple[float, str]:
    t = THRESHOLDS[name]
    pv, fv = t["pass"], t["fail"]
    high = t["better"] == "high"
    good = (v - fv) / (pv - fv) if high else (fv - v) / (fv - pv)
    if good >= 1:
        return 100.0, "pass"
    if good >= 0:
        return 40 + 60 * good, "warn"
    return max(0.0, 40 * (1 + good)), "fail"


def fix_text(name: str, v: float, ctx: dict) -> str:
    side = ctx.get("worst_side") or "weakest"
    p2 = ctx.get("peak2_norm")
    p2s = f" (second peak at x {p2[0]:.2f}, y {p2[1]:.2f} of the frame)" if p2 else ""
    key = ctx.get("key", "")
    texts = {
        "value_range_p2_p98": f"Widen the value range (L* p2..p98 is {v:.0f}): put the darkest accent and the brightest lit "
                              f"plane of the subject at least 60 L* apart, for example raise the key light on the subject and "
                              f"lower the world/fill so the background sits clearly darker (or lighter) than the subject.",
        "value_notan_r2": f"Simplify the values into 2, 3 or 4 clear groups (best R^2 {v:.2f}; notan, DF 26-27): give the "
                          f"background, the subject's shadow side and its lit side one value each, and remove gradients and "
                          f"texture noise that fill the space between them (check the _values.png map).",
        "value_notan_min_gap": f"Separate the value groups (closest centres only {v:.0f} L* apart): push the two nearest groups "
                               f"apart by at least 20 L*, usually by darkening the background or the shadow group.",
        "focal_big_elements": f"{v:.0f} big value masses compete (hierarchy: at most 2 big elements, DF 10): merge, shrink "
                              f"or darken the extra masses (boxes in the JSON focal details) so one leads and at most one "
                              f"supports it.",
        "text_contrast_ratio": f"Text is too close to its ground (worst box {v:.2f}:1; house rule 4.5:1, WCAG text figure, "
                               f"DF 3): add a dark plate or stroke behind light text (or the reverse) until glyph and ground "
                               f"differ by at least 4.5:1.",
        "text_px_per_char_320": f"Text is below the legibility floor at 320x180 ({v:.1f} px per character, floor 4 px in each "
                                f"axis, TR A16/A19): enlarge the text or shorten the line; at 4 px it is only the floor for "
                                f"tiny letters, larger letters need more.",
        "value_midtone_share": f"Cut the muddy midtones ({v:.0%} of pixels sit at L* 30..70): commit large areas to a clear "
                               f"dark or light value and keep midtones for transitions on the subject.",
        "value_black_clip_pct": f"Lift crushed blacks ({v:.1f}% of pixels are pure 0,0,0): add a weak fill or bounce, or raise "
                                f"the colour-management Exposure (in stops, PL 13) slightly, so shadow shapes keep detail; a "
                                f"black part on a black ground can instead be separated by a graded rim light (PL 22).",
        "value_white_clip_pct": f"Recover blown highlights ({v:.1f}% of pixels are at full scale on all channels): lower the "
                                f"key or emission strength, or the colour-management Exposure (in stops, PL 13), until the "
                                f"brightest areas keep texture.",
        "focal_dominance": f"Give the eye one winner (focal dominance {v:.2f}): reduce contrast, saturation or sharpness at the "
                           f"competing area{p2s}, or add contrast at the subject so its peak is at least 1.5x the next.",
        "focal_peak_in_subject": f"The strongest attention point is outside the subject: move the "
                                 f"brightest highlight and the hardest light/dark edge onto the subject, and darken or defocus "
                                 f"the area that currently wins.",
        "focal_saliency_lift": f"The subject draws only {v:.2f}x the frame's average attention: light the subject harder than "
                               f"its surroundings (or darken the surroundings) and keep busy texture out of the background.",
        "focal_contrast_holder": f"The strongest local contrast in the frame lies outside the subject (ratio {v:.2f}): tame the "
                                 f"background's hardest edges or brightest specks, or sharpen the subject's key edges.",
        "squint_contrast_ratio": f"The subject dissolves when squinted (contrast ratio {v:.2f}:1 at 320x180 blur, target 3:1): "
                                 f"its average value must differ from its surroundings, not only its fine detail; make the "
                                 f"subject read as one lighter (or darker) mass, for example a glow or a lit backing plate "
                                 f"behind dot-type detail.",
        "squint_contrast_survival": f"Only {v:.0%} of the subject/background contrast survives the squint: the separation "
                                    f"lives in fine detail; add a large-scale value change (light falloff, backlight, gradient "
                                    f"behind the subject).",
        "squint_subject_coherence": f"Only {v:.0%} of the stated subject box reads as one value mass (red outline in "
                                    f"_values.png): the subject breaks into a bright part and parts that fall into the "
                                    f"background group; even out the light or emission across the whole subject so it "
                                    f"reads as one shape.",
        "squint_share_drift": f"The value pattern changes when squinted (share drift {v:.2f}): the big shapes are carried by "
                              f"fine texture; group the texture into larger shapes of one value.",
        "edge_band_ratio": f"The silhouette merges with the background (edge contrast {v:.2f}:1, house target 3:1): add a "
                           f"rim light, for example a narrow strip source (PL 24) with graded falloff (PL 22), or a discreet "
                           f"dark-grey halo behind a dark subject (PL 23); weakest on the {side} side.",
        "edge_coverage": f"The edge is lost along {1 - v:.0%} of the silhouette (local contrast under 3:1), mostly on the "
                         f"{side} side: add a rim light or a background gradient on that side (PL 22-24) so the outline "
                         f"reads all the way round.",
        "ref_hist_wasserstein": f"The value distribution is far from the nearest reference ({v:.1f} L*, "
                                f"Wasserstein): compare the dark / mid / light shares in the JSON refs rows and shift this "
                                f"{key} image's balance toward the reference.",
        "ref_share_l1": f"The dark / mid / light areas (L* below 33, 33..66, above 66) differ from the nearest reference "
                        f"(L1 {v:.2f}; both share triples are in the JSON refs rows): match how much of the frame is "
                        f"dark, mid and light.",
        "ref_contrast_diff": f"Global contrast differs from the nearest reference by {v:.1f} L* std: match the reference's "
                             f"overall contrast.",
        "ref_dominance_logdiff": f"Focal dominance differs from the nearest reference (|ln ratio| {v:.2f}): match how strongly "
                                 f"the reference isolates its one focal point.",
    }
    return texts.get(name, f"{name} = {v}")


def critique(path: str, args, ref_paths: list[str], ref_cache: dict) -> dict:
    t0 = time.perf_counter()
    timing = {}
    rgb_full, info = read_image(path)
    oh, ow = rgb_full.shape[:2]
    lin, rgb = to_work(rgb_full)
    wh, ww = rgb.shape[:2]
    tm, tx = text_check(rgb_full, getattr(args, "text_box", None) or [])
    del rgb_full
    y = lin_luminance(lin)
    l = lstar(y)
    timing["load_resize"] = time.perf_counter() - t0
    t = time.perf_counter()
    vm, vx = value_check(l, info)
    timing["value"] = time.perf_counter() - t
    t = time.perf_counter()
    sal = saliency(rgb, l)
    subj, region, subj_src = subject_mask(l, sal, args, (oh, ow))
    subj_given = region is not None
    fm, fx = focal_check(rgb, l, sal, region, subj_given)
    timing["focal"] = time.perf_counter() - t
    t = time.perf_counter()
    sm, sx = squint_check(lin, l, y, subj, vx["shares3"], region)
    timing["squint"] = time.perf_counter() - t
    t = time.perf_counter()
    em, ex = edge_check(y, subj)
    timing["edge"] = time.perf_counter() - t
    t = time.perf_counter()
    rm, rx = {}, {"note": "no --refs given or no readable images; check not scored"}
    if ref_paths:
        hist, edges = np.histogram(l, 100, (0, 100))
        me = {"hist": hist / hist.sum(), "centres": (edges[:-1] + edges[1:]) / 2, "shares": band_shares(l),
              "std": float(l.std()), "dom": fm["focal_dominance"]}
        rm, rx = refs_check(me, ref_paths, ref_cache)
    timing["refs"] = time.perf_counter() - t

    ctx = {"worst_side": ex.get("worst_side"), "peak2_norm": fx.get("peak2_xy_norm"), "key": vx["extra"]["key"]}
    checks = {}
    floor_broken = []
    for cname, mets in (("value", vm), ("focal", fm), ("squint", sm), ("edge", em), ("text", tm), ("refs", rm)):
        rows = {}
        for m, v in mets.items():
            th = THRESHOLDS[m]
            if th.get("floor"):
                # a floor is never a pass criterion: below it the image FAILs; at or above it, nothing is scored
                broken = v < th["fail"]
                rows[m] = {"value": v, "pass": None, "fail": th["fail"], "better": th["better"], "floor": True,
                           "score": 0.0 if broken else None, "verdict": "fail" if broken else "floor met (not a pass)",
                           "source": th["src"], "fix": fix_text(m, v, ctx) if broken else ""}
                if broken:
                    floor_broken.append(m)
                continue
            sc, verdict = score_metric(m, v)
            rows[m] = {"value": v, "pass": th["pass"], "fail": th["fail"], "better": th["better"], "score": round(sc, 1),
                       "verdict": verdict, "source": th["src"],
                       "fix": fix_text(m, v, ctx) if verdict != "pass" else ""}
        scored = [r for r in rows.values() if r["score"] is not None]
        if scored:
            vs = [r["verdict"] for r in rows.values()]
            checks[cname] = {"score": round(float(np.mean([r["score"] for r in scored])), 1),
                             "verdict": "fail" if "fail" in vs else ("warn" if "warn" in vs else "pass"),
                             "weight": WEIGHTS[cname], "metrics": rows}
        else:
            checks[cname] = {"score": None, "verdict": "not scored", "weight": WEIGHTS[cname], "metrics": rows}
    used = {k: c for k, c in checks.items() if c["score"] is not None}
    wsum = sum(c["weight"] for c in used.values())
    overall = sum(c["score"] * c["weight"] for c in used.values()) / wsum
    any_fail = any(c["verdict"] == "fail" for c in used.values())
    any_warn = any(c["verdict"] == "warn" for c in used.values())
    th = THRESHOLDS["overall_score"]
    if overall < th["fail"] or floor_broken:
        verdict = "FAIL"
    elif overall < th["pass"] or any_fail:
        verdict = "WARN"
    else:
        verdict = "WARN" if any_warn else "PASS"
    fixes = []
    for cname, c in used.items():
        n = max(1, sum(1 for r in c["metrics"].values() if r["score"] is not None))
        for m, r in c["metrics"].items():
            if r["verdict"] in ("warn", "fail"):
                pr = 1000.0 if r.get("floor") else round(c["weight"] / wsum * (100 - r["score"]) / n, 2)
                fixes.append({"check": cname, "metric": m, "verdict": r["verdict"], "priority": pr, "fix": r["fix"]})
    fixes.sort(key=lambda f: (f["verdict"] != "fail", -f["priority"]))   # fails (floors first) before warns
    timing["total"] = time.perf_counter() - t0
    return {"image": path, "size_px": [ow, oh], "work_size_px": [ww, wh], "read_info": info, "subject": subj_src,
            "subject_area_share": round(float(subj.mean()), 4) if subj is not None else None,
            "overall_score": round(overall, 1), "verdict": verdict, "checks": checks, "fixes": fixes,
            "details": {"value": vx["extra"], "focal": fx, "squint": sx["extra"], "edge": ex, "text": tx, "refs": rx},
            "floors_broken": floor_broken,
            "weights_used": {k: round(c["weight"] / wsum, 4) for k, c in used.items()},
            "timing_s": {k: round(v, 3) for k, v in timing.items()}, "limits": LIMITS,
            "_images": {"thumb": sx["thumb"], "squint": sx["squint"], "labels3": vx["labels3"],
                        "centres3": vx["centres3"], "subj": subj}}


def write_outputs(rep: dict, out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(rep["image"]))[0]
    imgs = rep.pop("_images")
    paths = {k: os.path.join(out_dir, f"{stem}{suf}") for k, suf in
             (("json", "_critic.json"), ("md", "_critic.md"), ("thumb", "_320x180.png"), ("squint", "_squint.png"),
              ("values", "_values.png"))}
    write_png(paths["thumb"], imgs["thumb"])
    write_png(paths["squint"], imgs["squint"])
    grey = linear_to_srgb(lstar_to_y(np.array(imgs["centres3"])))
    vimg = grey[imgs["labels3"]]
    if imgs["subj"] is not None:   # mark the subject silhouette used by the edge check in red
        e = imgs["subj"] & (ndimage.distance_transform_edt(imgs["subj"]) <= 1.5)
        vimg = np.repeat(vimg[:, :, None], 3, axis=2)
        vimg[e] = (1.0, 0.0, 0.0)
    write_png(paths["values"], vimg)
    rep["outputs"] = paths
    with open(paths["json"], "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    with open(paths["md"], "w", encoding="utf-8") as fh:
        fh.write(markdown(rep))
    return paths


def markdown(rep: dict) -> str:
    L = [f"# Render critic: {os.path.basename(rep['image'])}", "",
         f"Image: `{rep['image']}` ({rep['size_px'][0]} x {rep['size_px'][1]} px, analysed at {rep['work_size_px'][0]} x "
         f"{rep['work_size_px'][1]})", f"Subject: {rep['subject']} (area share {rep['subject_area_share']})",
         f"Key: {rep['details']['value']['key']} (mean L* {rep['details']['value']['mean_lstar']})", "",
         f"**Overall score {rep['overall_score']} / 100 - {rep['verdict']}** (weights used: {rep['weights_used']}; "
         f"thresholds are provisional, no source yet, except where a source is named in the JSON)", "",
         "| Check | Metric | Value | Pass | Fail | Score | Verdict |", "|---|---|---|---|---|---|---|"]
    for cname, c in rep["checks"].items():
        if not c["metrics"]:
            L.append(f"| {cname} | - | - | - | - | - | {c['verdict']} |")
        for m, r in c["metrics"].items():
            ps = "floor only" if r.get("floor") else r["pass"]
            L.append(f"| {cname} ({c['score']}, {c['verdict']}) | {m} | {r['value']} | {ps} | {r['fail']} | "
                     f"{r['score'] if r['score'] is not None else '-'} | {r['verdict']} |")
    L += ["", "## Ranked fixes", ""]
    L += [f"{i}. [{f['check']} / {f['metric']}, {f['verdict']}] {f['fix']}" for i, f in enumerate(rep["fixes"][:8], 1)] \
        or ["None: every scored metric passed (this is a proxy; a human look is still required)."]
    fd = rep["details"]["focal"]
    ed = rep["details"]["edge"]
    L += ["", "## Details", "",
          f"- Focal peak at x {fd['peak1_xy_norm'][0]}, y {fd['peak1_xy_norm'][1]} of the frame; second peak "
          f"{fd['peak2_xy_norm']}; rule-of-thirds distance {fd['thirds_distance_diag']} of the diagonal (reported, not scored).",
          f"- Edge: {ed.get('note', '')}inside mean L* {ed.get('inside_mean_lstar')}, outside {ed.get('outside_mean_lstar')}, "
          f"lost share by side {ed.get('lost_share_by_side')}.",
          f"- Squint: {json.dumps({k: v for k, v in rep['details']['squint'].items() if k != 'squint_k3'})}",
          f"- Notan: {rep['details']['value']['notan_k']} value groups, shares {rep['details']['value']['notan_shares']}; "
          f"one value over half the frame: {rep['details']['value']['one_value_over_half']} (reported, not scored: "
          f"community-only rule). Big elements: {fd['big_elements']}.",
          f"- Text: {json.dumps(rep['details']['text'])}",
          f"- References: {rep['details']['refs'].get('nearest', rep['details']['refs'].get('note'))}; most off: "
          f"{rep['details']['refs'].get('most_off_metric')} (only derived numbers are reported; reference images are for "
          f"local comparison only and are not copied or embedded)",
          f"- Timing (s): {rep['timing_s']}", "",
          "## Sources", "",
          *[f"- {k}: {v}" for k, v in SOURCE_URLS.items()],
          "- Every threshold's source string is in the JSON (`checks.<check>.metrics.<metric>.source`).", "",
          "## Outputs", ""]
    L += [f"- `{p}`" for p in rep["outputs"].values()]
    L += ["", "## What this tool cannot judge", ""] + [f"- {x}" for x in rep["limits"]] + [""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Objective, scored critique of a render (proxy, not taste).")
    ap.add_argument("images", nargs="+")
    ap.add_argument("--out", default=DEFAULT_OUT)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--subject-box", help="x,y,w,h in original image pixels")
    g.add_argument("--subject-mask", help="PNG/JPG, non-black = subject")
    ap.add_argument("--text-box", action="append", help="x,y,w,h,chars of one text line in original pixels (repeatable)")
    ap.add_argument("--refs", help="folder of professional reference images (PNG/JPG in it and its direct subfolders; "
                                   "untrusted data, only image bytes are read)")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 3 if e.code else 0
    if args.subject_box:
        try:
            vals = [float(v) for v in args.subject_box.split(",")]
            if len(vals) != 4 or vals[2] <= 0 or vals[3] <= 0:
                raise ValueError
        except ValueError:
            print("bad --subject-box, expected x,y,w,h with w,h > 0", file=sys.stderr)
            return 3
    for tb in args.text_box or []:
        try:
            vals = [float(v) for v in tb.split(",")]
            if len(vals) != 5 or vals[2] <= 0 or vals[3] <= 0 or vals[4] < 1:
                raise ValueError
        except ValueError:
            print(f"bad --text-box {tb}, expected x,y,w,h,chars with w,h > 0 and chars >= 1", file=sys.stderr)
            return 3
    try:
        import open3d  # noqa: F401  (optional dependency: image reading and writing)
    except ImportError:
        print("render_critic needs the optional package open3d: install requirements-optional.txt into .venv", file=sys.stderr)
        return 3
    ref_paths, skipped = list_refs(args.refs) if args.refs else ([], [])
    if args.refs and not ref_paths:
        print(f"refs: no PNG/JPG in {args.refs}; reference check not scored")
    for s in skipped:
        print(f"refs skipped: {s}")
    worst = 0
    cache: dict = {}
    for p in args.images:
        try:
            rep = critique(p, args, ref_paths, cache)
        except (ValueError, OSError) as e:
            print(f"ERROR {p}: {e}", file=sys.stderr)
            worst = 3
            continue
        paths = write_outputs(rep, args.out)
        code = {"PASS": 0, "WARN": 1, "FAIL": 2}[rep["verdict"]]
        worst = max(worst, code) if worst != 3 else 3
        print(f"{rep['verdict']} {rep['overall_score']:5.1f}  {p}  ({rep['timing_s']['total']:.2f} s) -> {paths['md']}")
        for f in rep["fixes"][:3]:
            print(f"   - [{f['check']}/{f['metric']}] {f['fix']}")
    return worst


if __name__ == "__main__":
    sys.exit(main())
