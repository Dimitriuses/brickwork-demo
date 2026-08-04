#!/usr/bin/env python3
"""
Generates the site's two brand images from code, so their provenance is unambiguous
and the repo's MIT license can cover them honestly:

  shared/assets/images/hero.jpg   abstract gradient-wave hero background
  shared/assets/images/logo.png   running-bond brick-wall mark

This is a dev-time tool. It is NOT part of `npm run build` -- the images it emits
are committed. Re-run it only when you want to change the artwork.

    pip install pillow numpy
    python tools/generate-brand-assets.py [output_dir]

Both images replaced third-party stock artwork of unknown license. Keep it that way:
generate, don't download.
"""

import os
import sys

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------


def hex_rgb(s):
    """'#0a0058' -> (10, 0, 88) as float array."""
    s = s.lstrip("#")
    return np.array([int(s[i : i + 2], 16) for i in (0, 2, 4)], dtype=float)


def catmull_rom(points, samples=2000):
    """Smooth curve through `points` (list of (x, y) in 0..1). Returns (xs, ys)."""
    p = np.asarray(points, dtype=float)
    # Duplicate endpoints so the spline actually reaches the first/last control point.
    p = np.vstack([p[0], p, p[-1]])
    xs, ys = [], []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i], p[i + 1], p[i + 2], p[i + 3]
        t = np.linspace(0, 1, samples // (len(p) - 3) + 1)[:, None]
        # Standard Catmull-Rom basis.
        seg = 0.5 * (
            (2 * p1)
            + (-p0 + p2) * t
            + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2
            + (-p0 + 3 * p1 - 3 * p2 + p3) * t**3
        )
        xs.append(seg[:, 0])
        ys.append(seg[:, 1])
    xs, ys = np.concatenate(xs), np.concatenate(ys)
    order = np.argsort(xs)
    return xs[order], ys[order]


def linear_gradient(shape, c0, c1, angle_vec, offset=0.0, scale=1.0):
    """
    Diagonal two-stop gradient over an (h, w) grid.
    `angle_vec` is (wx, wy) weighting normalised x and y.
    """
    h, w = shape
    yn, xn = np.mgrid[0:h, 0:w]
    xn = xn / max(w - 1, 1)
    yn = yn / max(h - 1, 1)
    t = np.clip((angle_vec[0] * xn + angle_vec[1] * yn + offset) * scale, 0.0, 1.0)[..., None]
    return c0 * (1.0 - t) + c1 * t


# --------------------------------------------------------------------------------------
# hero
# --------------------------------------------------------------------------------------

# Palette sampled from the design this replaces: deep indigo field, violet and
# magenta wave masses. Blue channel stays low throughout, which is what gives the
# original its saturated, almost neon feel.
HERO_W, HERO_H = 2700, 1200  # 2.25:1, same aspect as the 9000x4000 original

HERO_BG = ("#0a0058", "#04149e")  # dark indigo -> blue, brightest toward top-right

# Each wave: control points (x, y in 0..1) for its top edge, then a two-stop fill.
# Listed back to front; every layer fills everything *below* its curve.
HERO_WAVES = [
    dict(  # deep violet mass, sits furthest back
        points=[(-0.05, 0.63), (0.22, 0.55), (0.5, 0.60), (0.78, 0.50), (1.05, 0.42)],
        c0="#1b0473",
        c1="#4a0aa0",
        vec=(0.9, 0.15),
        off=-0.05,
    ),
    dict(  # magenta-pink crest on the left, diving away to the right
        points=[(-0.05, 0.52), (0.16, 0.40), (0.36, 0.47), (0.6, 0.70), (0.85, 0.95), (1.05, 1.08)],
        c0="#c0208a",
        c1="#7d0eb2",
        vec=(0.75, 0.45),
        off=-0.05,
    ),
    dict(  # bright violet foreground: long rise to a crest right of centre
        points=[(-0.05, 1.0), (0.18, 0.86), (0.42, 0.70), (0.63, 0.56), (0.82, 0.50), (1.05, 0.55)],
        c0="#5a10b4",
        c1="#9b16bd",
        vec=(0.85, -0.2),
        off=0.12,
    ),
    dict(  # magenta accent clipping the bottom-right corner
        points=[(0.46, 1.14), (0.7, 0.94), (0.87, 0.80), (1.05, 0.72)],
        c0="#8e1a86",
        c1="#c2249a",
        vec=(1.0, 0.0),
        off=-0.3,
    ),
]


def build_hero(w=HERO_W, h=HERO_H):
    canvas = linear_gradient((h, w), hex_rgb(HERO_BG[0]), hex_rgb(HERO_BG[1]), (0.8, -0.35), offset=0.3)

    yy = np.arange(h)[:, None].astype(float)
    x_pix = np.arange(w) / (w - 1)

    for wave in HERO_WAVES:
        cx, cy = catmull_rom(wave["points"])
        edge = np.interp(x_pix, cx, cy) * (h - 1)  # curve's y, in pixels, per column
        # Soft 1.5px edge so the shapes antialias instead of stair-stepping.
        mask = np.clip((yy - edge[None, :]) / 1.5 + 0.5, 0.0, 1.0)[..., None]
        fill = linear_gradient((h, w), hex_rgb(wave["c0"]), hex_rgb(wave["c1"]), wave["vec"], wave["off"])
        canvas = canvas * (1.0 - mask) + fill * mask

    # A touch of noise. Large smooth gradients band badly under JPEG quantisation;
    # sub-1-level dither costs nothing visually and kills the banding.
    rng = np.random.default_rng(20260805)
    canvas = canvas + rng.normal(0.0, 1.1, canvas.shape)

    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8), "RGB")


# --------------------------------------------------------------------------------------
# logo
# --------------------------------------------------------------------------------------

LOGO_SIZE = 800
BRICK_RADIUS = 11
SUPERSAMPLE = 4  # rounded corners are drawn at 4x then downsampled

# Two brick tones, each a left-to-right ramp across its own width.
BRICK_DARK = ("#68001b", "#88001b")
BRICK_LIT = ("#e33e1b", "#c2081b")

# Running bond: alternating courses offset by half a brick, so the right edge is
# ragged on the short courses. (x0, x1, dark?) per row, top to bottom.
LOGO_ROWS = [
    ((76, 196), [(17, 70, True), (81, 379, False), (390, 628, False)]),
    ((208, 328), [(17, 225, True), (236, 533, False), (544, 783, False)]),
    ((340, 460), [(17, 70, True), (81, 379, False), (390, 628, False)]),
    ((472, 592), [(17, 225, True), (236, 533, False), (544, 783, False)]),
    ((604, 724), [(17, 70, True), (81, 379, True), (390, 628, False)]),
]


def rounded_rect_mask(w, h, radius, ss=SUPERSAMPLE):
    """Antialiased rounded-rectangle coverage mask in 0..1, via supersampling."""
    W, H, r = w * ss, h * ss, radius * ss
    yy, xx = np.mgrid[0:H, 0:W].astype(float) + 0.5
    # Distance from the inner rectangle that the corner radius is inset from.
    dx = np.maximum(np.maximum(r - xx, xx - (W - r)), 0.0)
    dy = np.maximum(np.maximum(r - yy, yy - (H - r)), 0.0)
    inside = (np.hypot(dx, dy) <= r).astype(float)
    # Box-downsample the supersampled coverage back to target resolution.
    return inside.reshape(h, ss, w, ss).mean(axis=(1, 3))


def build_logo(size=LOGO_SIZE):
    rgb = np.zeros((size, size, 3), dtype=float)
    alpha = np.zeros((size, size), dtype=float)

    for (y0, y1), bricks in LOGO_ROWS:
        for x0, x1, dark in bricks:
            bw, bh = x1 - x0, y1 - y0
            c0, c1 = (BRICK_DARK if dark else BRICK_LIT)
            # Ramp runs across each brick individually, not across the whole wall.
            fill = linear_gradient((bh, bw), hex_rgb(c0), hex_rgb(c1), (1.0, 0.0))
            m = rounded_rect_mask(bw, bh, BRICK_RADIUS)

            sub_rgb = rgb[y0:y1, x0:x1]
            sub_a = alpha[y0:y1, x0:x1]
            # Bricks never overlap, so a straight source-over is enough.
            rgb[y0:y1, x0:x1] = sub_rgb * (1.0 - m[..., None]) + fill * m[..., None]
            alpha[y0:y1, x0:x1] = np.maximum(sub_a, m)

    out = np.dstack([np.clip(rgb, 0, 255), np.clip(alpha * 255.0, 0, 255)]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


# --------------------------------------------------------------------------------------


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("shared", "assets", "images")
    os.makedirs(out_dir, exist_ok=True)

    hero_path = os.path.join(out_dir, "hero.jpg")
    logo_path = os.path.join(out_dir, "logo.png")

    build_hero().save(hero_path, "JPEG", quality=90, optimize=True, progressive=True, subsampling=0)
    build_logo().save(logo_path, "PNG", optimize=True)

    for p in (hero_path, logo_path):
        print("wrote %-46s %8.1f KB" % (p, os.path.getsize(p) / 1024.0))


if __name__ == "__main__":
    main()
