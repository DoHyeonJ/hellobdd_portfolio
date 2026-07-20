from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
ORANGE = "#f97316"
WHITE = "#ffffff"
MUTED = "#c8c8c8"
BG = "#0a0a0a"


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = (
        [r"C:\Windows\Fonts\malgunbd.ttf", r"C:\Windows\Fonts\malgun.ttf"]
        if bold
        else [r"C:\Windows\Fonts\malgun.ttf", r"C:\Windows\Fonts\malgunbd.ttf"]
    )
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_wh(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_center(draw: ImageDraw.ImageDraw, y: int, text: str, fnt: ImageFont.ImageFont, fill: str) -> int:
    tw, th = text_wh(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)
    return th


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    for x in range(0, W, 56):
        draw.line([(x, 0), (x, H)], fill="#151515", width=1)
    for y in range(0, H, 56):
        draw.line([(0, y), (W, y)], fill="#151515", width=1)

    # soft center glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(20):
        a = max(0, 16 - i)
        r = 80 + i * 18
        gd.ellipse(
            [W // 2 - r * 2, H // 2 - int(r * 0.7), W // 2 + r * 2, H // 2 + int(r * 0.7)],
            fill=(249, 115, 22, a),
        )
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1) Logo lockup
    lockup_path = os.path.join(ROOT, "img", "logo-lockup.png")
    logo_h = 0
    logo_y = 78
    if os.path.exists(lockup_path):
        logo = Image.open(lockup_path).convert("RGBA")
        target_w = 720
        ratio = target_w / logo.width
        logo = logo.resize((target_w, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS)
        lx = (W - logo.width) // 2
        img.paste(logo, (lx, logo_y), logo)
        draw = ImageDraw.Draw(img)
        logo_h = logo.height
    else:
        draw_center(draw, logo_y, "<HELLOBDD />", font(64), WHITE)
        logo_h = 64

    # 2) Main copy — two lines, large
    copy_f = font(46)
    line1 = "반복 업무는 자동화하고,"
    line2 = "팀은 핵심에 집중하세요"
    copy_gap = 10
    lh1 = text_wh(draw, line1, copy_f)[1]
    lh2 = text_wh(draw, line2, copy_f)[1]
    copy_block = lh1 + copy_gap + lh2

    # 3) Company name
    company_f = font(36)
    company = "헬로비디디"
    ch = text_wh(draw, company, company_f)[1]
    role_f = font(26, bold=False)
    role = "대행사 자동화 파트너"
    rh = text_wh(draw, role, role_f)[1]

    gap_logo_copy = 40
    gap_copy_company = 36
    gap_company_role = 12

    y = logo_y + logo_h + gap_logo_copy
    draw_center(draw, y, line1, copy_f, WHITE)
    y += lh1 + copy_gap
    draw_center(draw, y, line2, copy_f, WHITE)
    y += lh2 + gap_copy_company

    # thin divider
    div_w = 48
    draw.rectangle([(W - div_w) // 2, y, (W + div_w) // 2, y + 3], fill=ORANGE)
    y += 3 + gap_company_role + 8

    # company: 헬로 orange + 비디디 white
    prefix, rest = "헬로", "비디디"
    pw = text_wh(draw, prefix, company_f)[0]
    rw = text_wh(draw, rest, company_f)[0]
    x0 = (W - pw - rw) // 2
    draw.text((x0, y), prefix, font=company_f, fill=ORANGE)
    draw.text((x0 + pw, y), rest, font=company_f, fill=WHITE)
    y += ch + gap_company_role
    draw_center(draw, y, role, role_f, MUTED)

    out = os.path.join(ROOT, "img", "og.png")
    img.save(out, "PNG", optimize=True)
    print(f"saved {out} logo={logo_h}px copy={copy_block}px")


if __name__ == "__main__":
    main()
