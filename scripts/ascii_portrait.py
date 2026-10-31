#!/usr/bin/env python3
"""Photo -> ASCII portrait lines.  Usage: ascii_portrait.py photo.jpg [cols]"""
import sys
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageChops

RAMP = " .,:;i1tfLCG08@"
INVERT = True
GAMMA = 1.0          # short, clean ramp: light -> dense

def to_lines(path, cols=96, crop=(0, 0, 1, 1)):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.crop((int(w*crop[0]), int(h*crop[1]), int(w*crop[2]), int(h*crop[3])))
    g = ImageOps.grayscale(im)

    # 1) backdrop mask by flood-filling (magenta marker) from the top corners; won't leak into the white shirt
    m = im.filter(ImageFilter.GaussianBlur(2)).copy()
    for seed in [(1, 1), (m.width-2, 1), (1, m.height//3), (m.width-2, m.height//3), (m.width-2, m.height-2)]:
        if m.getpixel(seed) != (255, 0, 255):
            ImageDraw.floodfill(m, seed, (255, 0, 255), thresh=34)
    bg = m.point(lambda v: v).convert("RGB")
    r, gch, b = bg.split()
    bg = ImageChops.multiply(r.point(lambda v: 255 if v == 255 else 0), gch.point(lambda v: 255 if v == 0 else 0))

    # 2) tone: stretch contrast on the subject only (percentile clip), then gamma to open up the face
    subj = ImageChops.invert(bg)
    vals = sorted(v for v, mk in zip(g.getdata(), subj.getdata()) if mk)
    lo, hi = vals[int(len(vals)*0.02)], vals[int(len(vals)*0.985)]
    eq = g.point(lambda v: max(0, min(255, int((v - lo) * 255 / max(1, hi - lo)))))
    eq = eq.filter(ImageFilter.UnsharpMask(radius=2, percent=220, threshold=2))

    rows = int(cols * (im.height / im.width) * 0.5)
    eq = eq.resize((cols, rows), Image.LANCZOS)
    bg = bg.resize((cols, rows), Image.BILINEAR)

    out = []
    for y in range(rows):
        s = ""
        for x in range(cols):
            if bg.getpixel((x, y)) > 140:
                s += " "; continue
            v = eq.getpixel((x, y)) / 255.0                 # 0 dark .. 1 light
            idx = 1 + int(((1 - v) if INVERT else v) ** GAMMA * (len(RAMP) - 2))    # subject never fully blank
            s += RAMP[min(idx, len(RAMP)-1)]
        out.append(s.rstrip())
    return out

if __name__ == "__main__":
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 96
    print("\n".join(to_lines(sys.argv[1], cols)))
