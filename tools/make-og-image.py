#!/usr/bin/env python3
"""Build the link-preview (Open Graph / Twitter / iMessage) image.

    python3 tools/make-og-image.py   ->   assets/og-image.jpg (1200x630)

The card is drawn from the same parts as the page it links to: the site's
night-to-dawn gradient, and the real device screenshots in frames built here.

Two earlier versions are worth not repeating.

The first cropped the phone pair out of the `05-pair-tight` poster. That poster
has its own painted sunrise behind the phones, so the crop carried a rectangle of
warm sky onto an ink card, and feathering the edges only turned the seam into a
murky halo. Nothing cropped out of a finished poster will sit cleanly on a
different background; the devices are drawn here instead, on transparency.

The second advertised a square og:image alongside this one. iMessage picked the
square, cropped it to its own card shape, and rendered a preview reading
"e Nudge" over a sliced headline. Advertise exactly one og:image. The major
platforms (iMessage, Twitter/X, Slack, Discord, Facebook, LinkedIn) all show a
1.91:1 image whole, which is why this is a left-right composition.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")
SCREENS = os.path.join(OUT, "screens")
ICON = os.path.join(OUT, "app-icon.png")
ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"

AMBER = (255, 182, 90)
MUTED = (198, 203, 234)
WHITE = (255, 255, 255)

W, H = 1200, 630
PAD = 70          # room around a device for its shadow


def font(size, weight="Bold"):
    f = ImageFont.truetype(ROUNDED, size)
    f.set_variation_by_name(weight)
    return f


def vgradient(size, top, bottom):
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    w, h = size
    for y in range(h):
        k = y / max(h - 1, 1)
        d.line([(0, y), (w, y)],
               fill=tuple(round(a + (b - a) * k) for a, b in zip(top, bottom)))
    return img


def sky():
    """The site's hero ground: the same stops as .hero__sky in style.css."""
    stops = [(0.00, (0x06, 0x08, 0x1A)), (0.28, (0x09, 0x0C, 0x22)),
             (0.58, (0x0E, 0x12, 0x36)), (0.82, (0x16, 0x1C, 0x49)),
             (1.00, (0x1C, 0x23, 0x58))]
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                d.line([(0, y), (W, y)],
                       fill=tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)))
                break

    # Dawn low and to the right, so it sits behind the devices.
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    cx, cy, r = W * 0.74, H * 1.10, W * 0.58
    for i in range(64, 0, -1):
        t = i / 64
        gd.ellipse((cx - r * t, cy - r * t * 0.70, cx + r * t, cy + r * t * 0.70),
                   fill=int(115 * (1 - t) ** 1.8))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    return Image.composite(Image.new("RGB", (W, H), (246, 140, 42)), img, glow)


def grain(img, opacity=0.022):
    """Stops the long gradient ramps banding on 8-bit displays.

    Generated at full resolution: scaling a small tile up leaves visible blocks,
    which read as dirt on the card rather than as grain.
    """
    random.seed(7)
    n = Image.new("L", (W, H))
    n.putdata([random.randint(96, 160) for _ in range(W * H)])
    return Image.blend(img, Image.merge("RGB", (n, n, n)), opacity)


def device(screenshot, screen_h, bezel, radius,
           body=((0x3B, 0x41, 0x76), (0x17, 0x1B, 0x41))):
    """A framed device on transparency, shadow baked in.

    Drawn rather than cropped, so it composites onto the card without dragging
    a background of its own along with it.
    """
    shot = Image.open(screenshot).convert("RGB")
    sw = round(shot.width * screen_h / shot.height)
    shot = shot.resize((sw, screen_h), Image.LANCZOS)

    bw, bh = sw + bezel * 2, screen_h + bezel * 2
    canvas = Image.new("RGBA", (bw + PAD * 2, bh + PAD * 2), (0, 0, 0, 0))

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (PAD, PAD + 22, PAD + bw, PAD + bh + 22), radius=radius,
        fill=(0, 0, 0, 165))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(28)))

    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw - 1, bh - 1),
                                           radius=radius, fill=255)
    canvas.paste(vgradient((bw, bh), *body), (PAD, PAD), mask)

    smask = Image.new("L", (sw, screen_h), 0)
    ImageDraw.Draw(smask).rounded_rectangle(
        (0, 0, sw - 1, screen_h - 1), radius=max(radius - bezel, 4), fill=255)
    canvas.paste(shot, (PAD + bezel, PAD + bezel), smask)
    return canvas


def place(card, art, x, y):
    """Paste a device by its frame's top-left, ignoring the shadow padding."""
    card.paste(art, (x - PAD, y - PAD), art)


def build():
    card = grain(sky())

    phone = device(os.path.join(SCREENS, "03-unlock.png"),
                   screen_h=534, bezel=11, radius=52)
    place(card, phone, 744, 48)

    watch = device(os.path.join(SCREENS, "watch-face.png"),
                   screen_h=124, bezel=8, radius=34,
                   body=((0x45, 0x4A, 0x80), (0x14, 0x18, 0x3C)))
    place(card, watch, 1012, 404)

    d = ImageDraw.Draw(card)

    x, icon_px = 80, 56
    icon = Image.open(ICON).convert("RGBA").resize((icon_px, icon_px), Image.LANCZOS)
    m = Image.new("L", (icon_px, icon_px), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, icon_px - 1, icon_px - 1),
                                        radius=int(icon_px * 0.225), fill=255)
    icon.putalpha(m)
    card.paste(icon, (x, 72), icon)
    d.text((x + icon_px + 18, 72 + icon_px / 2), "Nature Nudge",
           font=font(31), fill=WHITE, anchor="lm")

    for i, (text, colour) in enumerate([("Go outside", WHITE),
                                        ("to unlock", AMBER),
                                        ("your apps.", AMBER)]):
        d.text((x, 212 + i * 76), text, font=font(70, "Heavy"), fill=colour)

    d.text((x, H - 88), "On the App Store  ·  iPhone & Apple Watch",
           font=font(21, "Semibold"), fill=MUTED)
    return card


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "og-image.jpg")
    img = build()
    img.save(path, quality=90, optimize=True, progressive=True)
    print(f"og-image.jpg: {img.size}  {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    main()
