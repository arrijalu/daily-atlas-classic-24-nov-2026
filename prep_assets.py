#!/usr/bin/env python3
"""Prepare the artwork that draw.py pastes onto the page.

Two jobs, both deterministic:

1. Featured art -- take the three winning Recraft scenes (1536x768) and
   produce assets/f1.jpg, f2.jpg, f3.jpg at exactly 314x157, the size the
   featured panels reserve. The source aspect is 2.000 and 314/157 is
   2.0003, so this is a pure downscale (LANCZOS), nothing cropped away.

2. Grid strips -- take each grid story's strip scene (wide) and produce a
   314-wide-friendly strip at 192x104, centre-cropped to the strip aspect.
   draw.py scales those down to the tile strip box. Before cropping, every
   artwork passes through clamp_foreign_hues, which rotates saturated reds
   to ochre and saturated blues to teal so the CLASSIC palette holds.

Run with the venv interpreter:
    .venv/bin/python prep_assets.py featured
    .venv/bin/python prep_assets.py strips
    .venv/bin/python prep_assets.py all
"""

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# Ochre A98A3E expressed in PIL's 0..255 hue scale: 41 deg * 255/360 = 29.
OCHRE_HUE_PIL = 29
# Teal 1F5E52 is 169 deg -> 169 * 255/360 = 120.
TEAL_HUE_PIL = 120

FEATURED_W, FEATURED_H = 314, 157
FEATURED_SOURCES = [
    ("f1-a.png", "f1.jpg"),
    ("f2-a.png", "f2.jpg"),
    ("f3-a.png", "f3.jpg"),
]

STRIP_W, STRIP_H = 192, 104
GRID_STRIPS = [
    ("g04.png", "s04.jpg"),
    ("g05.png", "s05.jpg"),
    ("g06.png", "s06.jpg"),
    ("g07.png", "s07.jpg"),
    ("g08.png", "s08.jpg"),
    ("g09.png", "s09.jpg"),
    ("g10.png", "s10.jpg"),
    ("g11.png", "s11.jpg"),
    ("g12.png", "s12.jpg"),
    ("g13.png", "s13.jpg"),
    ("g14.png", "s14.jpg"),
    ("g15.png", "s15.jpg"),
]


def centre_crop_to_aspect(im, tw, th):
    """Crop the centre of im to the tw:th aspect, without resizing yet."""
    want = tw / float(th)
    have = im.width / float(im.height)
    if have > want:                     # too wide -> trim left and right
        new_w = int(round(im.height * want))
        left = (im.width - new_w) // 2
        return im.crop((left, 0, left + new_w, im.height))
    if have < want:                     # too tall -> trim top and bottom
        new_h = int(round(im.width / want))
        top = (im.height - new_h) // 2
        return im.crop((0, top, im.width, top + new_h))
    return im


def do_featured():
    for src, dst in FEATURED_SOURCES:
        sp = os.path.join(ASSETS, src)
        dp = os.path.join(ASSETS, dst)
        im = Image.open(sp).convert("RGB")
        im, (n_red, n_blue) = clamp_foreign_hues(im)
        crop = centre_crop_to_aspect(im, FEATURED_W, FEATURED_H)
        crop = crop.resize((FEATURED_W, FEATURED_H), Image.LANCZOS)
        crop.save(dp, "JPEG", quality=92, optimize=True)
        print("%-16s %dx%d -> %-8s %dx%d  %d bytes  (red %d, blue %d px)"
              % (src, im.width, im.height, dst, FEATURED_W, FEATURED_H,
                 os.path.getsize(dp), n_red, n_blue))


def clamp_foreign_hues(im):
    """Pull stray saturated hues back into the CLASSIC palette.

    The page is PAPER / INK / TEAL / OCHRE / CREAM / LAND. Anything the
    model rendered in a saturated red (a medical cross, a warning stripe)
    or a saturated cobalt (window glass, night sea, screens) is a foreign
    hue: at page scale a cobalt quarter-panel reads as a different
    publication. Rather than hand-fix each image, rotate the offending
    pixels to the nearest palette hue and take some of the chroma out, so
    the shape survives and the colour stops arguing with the page.

      red  -> OCHRE hue (41 deg, 29/255)   chroma kept at 72%
      blue -> TEAL  hue (169 deg, 120/255) chroma kept at 62%

    Thresholds are deliberately narrow so pixels already in the palette
    family (ochre ~41 deg, teal ~169 deg, land green ~90 deg) are never
    touched. Returns (image, (red_px, blue_px)).
    """
    hsv = im.convert("HSV")
    h, s, v = hsv.split()
    hn = np.asarray(h, dtype=np.uint8)
    sn = np.asarray(s, dtype=np.uint8)
    vn = np.asarray(v, dtype=np.uint8)

    red_band = (hn >= 238) | (hn <= 16)
    red_hot = red_band & (sn > 110) & (vn > 60) & (vn < 230)

    # Cobalt and navy. Hue 130..190 covers the blue half of the wheel in
    # PIL's scale; the saturation floor keeps pale haze (which already
    # reads as paper grey) out of the rewrite.
    blue_hot = (hn >= 128) & (hn <= 192) & (sn > 85) & (vn > 40)

    n_red = int(red_hot.sum())
    n_blue = int(blue_hot.sum())
    if not n_red and not n_blue:
        return im, (0, 0)

    hn = hn.copy()
    sn = sn.copy()
    if n_red:
        hn[red_hot] = OCHRE_HUE_PIL
        sn[red_hot] = (sn[red_hot].astype(np.uint16) * 72 // 100).astype(np.uint8)
    if n_blue:
        hn[blue_hot] = TEAL_HUE_PIL
        sn[blue_hot] = (sn[blue_hot].astype(np.uint16) * 62 // 100).astype(np.uint8)

    out = Image.merge("HSV", (Image.fromarray(hn), Image.fromarray(sn), v))
    return out.convert("RGB"), (n_red, n_blue)


def do_strips():
    for src, dst in GRID_STRIPS:
        sp = os.path.join(ASSETS, src)
        dp = os.path.join(ASSETS, dst)
        if not os.path.exists(sp):
            print("MISSING %s -- skipped" % src)
            continue
        im = Image.open(sp).convert("RGB")
        im, (n_red, n_blue) = clamp_foreign_hues(im)
        crop = centre_crop_to_aspect(im, STRIP_W, STRIP_H)
        crop = crop.resize((STRIP_W, STRIP_H), Image.LANCZOS)
        crop.save(dp, "JPEG", quality=90, optimize=True)
        note = ""
        if n_red:
            note += "  (red->ochre %d px)" % n_red
        if n_blue:
            note += "  (blue->teal %d px)" % n_blue
        print("%-16s %dx%d -> %-8s %dx%d  %d bytes%s"
              % (src, im.width, im.height, dst, STRIP_W, STRIP_H,
                 os.path.getsize(dp), note))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("featured", "all"):
        do_featured()
    if what in ("strips", "all"):
        do_strips()


if __name__ == "__main__":
    main()
