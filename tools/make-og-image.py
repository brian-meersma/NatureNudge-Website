#!/usr/bin/env python3
"""Build the link-preview (Open Graph / Twitter / iMessage) images.

Source art is the `05-pair-tight` hero from the Nature Nudge Hero 2 set. The
phone pair is cropped out of it and set on the site's own ink-and-sunrise
background, with the wordmark and headline alongside so the card stays readable
at thumbnail size.

    python3 tools/make-og-image.py

Writes assets/og-image.jpg (1200x630, the one nearly every platform uses) and
assets/og-image-square.jpg (1200x1200, for the few that prefer a square).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")

SOURCE = os.path.expanduser(
    "~/Downloads/Nature Nudge Hero 2/iPhone 6.9 (1290x2796)/05-pair-tight.png")
ICON = os.path.join(ROOT, "assets", "app-icon.png")
ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"

INK = (11, 14, 36)
AMBER = (255, 182, 90)
MUTED = (198, 203, 234)
WHITE = (255, 255, 255)

# The phone pair inside the source art, from its dark-pixel extents plus margin.
PHONES = (24, 940, 1266, 2200)

HEADLINE = [("Go outside", WHITE), ("to unlock", AMBER), ("your apps.", AMBER)]


def font(size, weight="Bold"):
    f = ImageFont.truetype(ROUNDED, size)
    f.set_variation_by_name(weight)
    return f


def background(w, h, glow_at):
    """The site's hero ground: ink with a warm sunrise bloom."""
    bg = Image.new("RGB", (w, h), INK)
    glow = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(glow)
    cx, cy = w * glow_at[0], h * glow_at[1]
    r = max(w, h) * 0.95
    for i in range(56, 0, -1):
        t = i / 56
        d.ellipse((cx - r * t, cy - r * t, cx + r * t, cy + r * t),
                  fill=int(64 * (1 - t) ** 1.7))
    return Image.composite(Image.new("RGB", (w, h), (245, 154, 46)), bg, glow)


def art(scale_px):
    """The phone pair, scaled to `scale_px` wide."""
    src = Image.open(SOURCE).convert("RGB").crop(PHONES)
    h = round(src.height * scale_px / src.width)
    return src.resize((scale_px, h), Image.LANCZOS)


def feather(img, left=0, top=0, bottom=0):
    """Alpha ramps on the given edges so the art melts into the background."""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 255)
    d = ImageDraw.Draw(mask)
    for x in range(left):
        d.line([(x, 0), (x, img.height)], fill=int(255 * (x / left) ** 1.5))
    for y in range(top):
        v = int(255 * (y / top) ** 1.5)
        for x in range(img.width):
            mask.putpixel((x, y), min(mask.getpixel((x, y)), v))
    for y in range(bottom):
        v = int(255 * (y / bottom) ** 1.5)
        yy = img.height - 1 - y
        for x in range(img.width):
            mask.putpixel((x, yy), min(mask.getpixel((x, yy)), v))
    img.putalpha(mask)
    return img


def wordmark(canvas, d, x, y, icon_px):
    icon = Image.open(ICON).convert("RGBA").resize((icon_px, icon_px), Image.LANCZOS)
    rounded = Image.new("L", (icon_px, icon_px), 0)
    ImageDraw.Draw(rounded).rounded_rectangle(
        (0, 0, icon_px - 1, icon_px - 1), radius=int(icon_px * 0.225), fill=255)
    icon.putalpha(rounded)
    canvas.paste(icon, (x, y), icon)
    d.text((x + icon_px + int(icon_px * 0.30), y + icon_px * 0.5), "Nature Nudge",
           font=font(int(icon_px * 0.52)), fill=WHITE, anchor="lm")


def headline(d, x, y, size):
    lh = round(size * 1.06)
    for text, colour in HEADLINE:
        d.text((x, y), text, font=font(size, "Heavy"), fill=colour)
        y += lh
    return y


def wide():
    """1200x630 — text column left, phone pair bleeding off the right."""
    w, h, pad = 1200, 630, 64
    canvas = background(w, h, glow_at=(0.74, 0.62))

    a = art(round(w * 0.60))
    a = feather(a, left=round(a.width * 0.38), bottom=round(a.height * 0.10))
    canvas.paste(a, (w - a.width + round(a.width * 0.06), -round(a.height * 0.05)), a)

    d = ImageDraw.Draw(canvas)
    wordmark(canvas, d, pad, pad - 4, 64)
    headline(d, pad, 218, 68)
    d.text((pad, h - pad - 20), "On the App Store  ·  iPhone & Apple Watch",
           font=font(20, "Semibold"), fill=MUTED)
    return canvas


def square():
    """1200x1200 — text block on top, phone pair filling the lower half."""
    w, h, pad = 1200, 1200, 84
    canvas = background(w, h, glow_at=(0.5, 0.86))

    a = art(round(w * 0.92))
    a = feather(a, top=round(a.height * 0.06))
    canvas.paste(a, ((w - a.width) // 2, 470), a)

    d = ImageDraw.Draw(canvas)
    wordmark(canvas, d, pad, pad, 76)
    headline(d, pad, 236, 78)
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, image in (("og-image.jpg", wide()),
                        ("og-image-square.jpg", square())):
        path = os.path.join(OUT, name)
        image.save(path, quality=88, optimize=True, progressive=True)
        print(f"{name}: {image.size}  {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    main()
