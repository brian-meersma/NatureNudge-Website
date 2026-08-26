#!/usr/bin/env python3
"""Build the link-preview (Open Graph / Twitter / iMessage) images.

Source art is the `05-pair-tight` hero from the Nature Nudge Hero 2 set. The
phone pair is cropped out of it and set on the site's own ink-and-sunrise
background, with the wordmark and headline alongside so the card stays readable
at thumbnail size.

    python3 tools/make-og-image.py

Writes assets/og-image.jpg (1200x630).

One image, and a centred composition. An earlier version offered a second square
og:image as well; iMessage picked the square, cropped its left edge off, and
rendered a card reading "e Nudge" over a sliced headline. Clients crop the
preview to whatever their card wants, so everything that matters lives inside the
centre square: the wordmark, the headline and the phones are all centred, and the
gradient is the only thing at the edges.
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


def feather(img, left=0, right=0, top=0, bottom=0):
    """Alpha ramps on the given edges so the art melts into the background.

    The source crop is a rectangle of painted sunrise, much lighter than the ink
    ground. Without ramps on every side that rectangle reads as a pasted box.
    """
    img = img.convert("RGBA")
    w, h = img.size
    mask = Image.new("L", img.size, 255)
    px = mask.load()

    def ramp(n, i):
        return int(255 * (i / n) ** 1.4)

    for x in range(left):
        v = ramp(left, x)
        for y in range(h):
            px[x, y] = min(px[x, y], v)
    for x in range(right):
        v = ramp(right, x)
        for y in range(h):
            px[w - 1 - x, y] = min(px[w - 1 - x, y], v)
    for y in range(top):
        v = ramp(top, y)
        for x in range(w):
            px[x, y] = min(px[x, y], v)
    for y in range(bottom):
        v = ramp(bottom, y)
        for x in range(w):
            px[x, h - 1 - y] = min(px[x, h - 1 - y], v)

    img.putalpha(mask)
    return img


def sink(img, strength=0.55):
    """Pull the art's own background down toward ink at its edges, so the warm
    painted sky inside the crop does not sit brighter than the card around it."""
    img = img.convert("RGBA")
    w, h = img.size
    ink = Image.new("RGB", (w, h), INK)
    fade = Image.new("L", (w, h), 0)
    px = fade.load()
    for x in range(w):
        # 1 at the outer edge, 0 across the middle 56%
        t = abs(x - w / 2) / (w / 2)
        v = 0.0 if t < 0.56 else ((t - 0.56) / 0.44) ** 1.6
        col = int(255 * v * strength)
        for y in range(h):
            px[x, y] = col
    blended = Image.composite(ink, img.convert("RGB"), fade)
    out = blended.convert("RGBA")
    out.putalpha(img.getchannel("A"))
    return out


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
    """1200x630, centre-composed so a square crop still reads."""
    w, h, pad = 1200, 630, 44
    canvas = background(w, h, glow_at=(0.5, 1.02))
    d = ImageDraw.Draw(canvas)

    # Phones rise from the bottom edge, centred.
    a = art(640)
    a = sink(a)
    a = feather(a, left=70, right=70, top=round(a.height * 0.10))
    canvas.paste(a, ((w - a.width) // 2, 262), a)

    # Wordmark, centred as a unit.
    icon_px, gap = 52, 16
    label_font = font(30)
    label_w = d.textlength("Nature Nudge", font=label_font)
    x = (w - (icon_px + gap + label_w)) / 2
    icon = Image.open(ICON).convert("RGBA").resize((icon_px, icon_px), Image.LANCZOS)
    rounded = Image.new("L", (icon_px, icon_px), 0)
    ImageDraw.Draw(rounded).rounded_rectangle(
        (0, 0, icon_px - 1, icon_px - 1), radius=int(icon_px * 0.225), fill=255)
    icon.putalpha(rounded)
    canvas.paste(icon, (round(x), pad), icon)
    d.text((x + icon_px + gap, pad + icon_px / 2), "Nature Nudge",
           font=label_font, fill=WHITE, anchor="lm")

    # Headline, centred, two lines so it stays inside the centre square.
    for i, (text, colour) in enumerate([("Go outside", WHITE),
                                        ("to unlock your apps.", AMBER)]):
        d.text((w / 2, 126 + i * 66), text, font=font(58, "Heavy"),
               fill=colour, anchor="ma")
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "og-image.jpg")
    image = wide()
    image.save(path, quality=88, optimize=True, progressive=True)
    print(f"og-image.jpg: {image.size}  {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    main()
