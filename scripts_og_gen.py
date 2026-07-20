from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\malgunbd.ttf",
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), "#0a0a0a")
    draw = ImageDraw.Draw(img)

    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill="#161616", width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill="#161616", width=1)

    # soft orange glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(28):
        a = max(0, 28 - i)
        r = 120 + i * 22
        gd.ellipse(
            [W // 2 - r * 2, H // 2 - int(r * 0.85), W // 2 + r * 2, H // 2 + int(r * 0.85)],
            fill=(249, 115, 22, a),
        )
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    lockup_path = os.path.join(ROOT, "img", "logo-lockup.png")
    text_top = 220
    if os.path.exists(lockup_path):
        logo = Image.open(lockup_path).convert("RGBA")
        lw = 460
        ratio = lw / logo.width
        logo = logo.resize((lw, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS)
        lx = (W - logo.width) // 2
        ly = 118
        img.paste(logo, (lx, ly), logo)
        draw = ImageDraw.Draw(img)
        text_top = ly + logo.height + 40
    else:
        brand = "헬로비디디"
        bf = font(68)
        bbox = draw.textbbox((0, 0), brand, font=bf)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, 170), brand, font=bf, fill="#ffffff")
        text_top = 270

    sub = "대행사 자동화 파트너"
    sf = font(30)
    bbox = draw.textbbox((0, 0), sub, font=sf)
    sw = bbox[2] - bbox[0]
    draw.text(((W - sw) // 2, text_top), sub, font=sf, fill="#f97316")

    line = "반복 업무는 자동화하고, 팀은 핵심에 집중하세요"
    tf = font(26)
    bbox = draw.textbbox((0, 0), line, font=tf)
    lw2 = bbox[2] - bbox[0]
    draw.text(((W - lw2) // 2, text_top + 54), line, font=tf, fill="#c8c8c8")

    draw.rectangle([0, H - 58, W, H], fill="#111111")
    df = font(22)
    dom = "pf.dainopick.com"
    bbox = draw.textbbox((0, 0), dom, font=df)
    dw = bbox[2] - bbox[0]
    draw.text(((W - dw) // 2, H - 42), dom, font=df, fill="#8a8a8a")

    out = os.path.join(ROOT, "img", "og.png")
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} {img.size}")


if __name__ == "__main__":
    main()
