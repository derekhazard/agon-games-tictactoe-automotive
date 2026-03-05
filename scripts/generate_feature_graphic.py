#!/usr/bin/env python3
"""Generate a 1024x500 Play Store feature graphic."""

import io
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "store-assets" / "feature-graphic-1024x500.png"

WIDTH, HEIGHT = 1024, 500
BG_COLOR = (13, 17, 23)  # #0D1117

# Logo viewport: 160x65, render at ~3x
LOGO_SCALE = 3
LOGO_W = 160 * LOGO_SCALE  # 480
LOGO_H = 65 * LOGO_SCALE   # 195


def build_logo_svg() -> str:
    """Translate logo_lf.xml to SVG with resolved @color/ refs."""
    # Color map: Android ARGB -> SVG
    accent = "#00B4D8"
    text_primary = "#E6EDF3"
    accent_60 = "rgba(0,180,216,0.6)"
    accent_30 = "rgba(0,180,216,0.3)"

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 160 65" width="{LOGO_W}" height="{LOGO_H}">
      <!-- L: vertical -->
      <path d="M 10,5 L 10,42" stroke="{accent}" stroke-width="5.5"
            stroke-linecap="round" fill="none"/>
      <!-- L: horizontal -->
      <path d="M 10,42 L 28,42" stroke="{accent}" stroke-width="5.5"
            stroke-linecap="round" fill="none"/>
      <!-- F: vertical -->
      <path d="M 36,5 L 36,42" stroke="{text_primary}" stroke-width="5.5"
            stroke-linecap="round" fill="none"/>
      <!-- F: top -->
      <path d="M 36,5 L 58,5" stroke="{text_primary}" stroke-width="5.5"
            stroke-linecap="round" fill="none"/>
      <!-- F: middle -->
      <path d="M 36,23 L 54,23" stroke="{text_primary}" stroke-width="5.5"
            stroke-linecap="round" fill="none"/>
      <!-- Flow line 1 -->
      <path d="M 8,50 L 120,50" stroke="{accent}" stroke-width="2.5"
            stroke-linecap="round" fill="none"/>
      <!-- Flow line 2 -->
      <path d="M 8,55 L 140,55" stroke="{accent_60}" stroke-width="2.5"
            stroke-linecap="round" fill="none"/>
      <!-- Flow line 3 -->
      <path d="M 8,60 L 158,60" stroke="{accent_30}" stroke-width="2.5"
            stroke-linecap="round" fill="none"/>
    </svg>"""


def render_logo() -> Image.Image:
    """Render logo SVG to Pillow RGBA image."""
    svg = build_logo_svg()
    png_data = cairosvg.svg2png(
        bytestring=svg.encode(), output_width=LOGO_W, output_height=LOGO_H
    )
    return Image.open(io.BytesIO(png_data)).convert("RGBA")


def main() -> None:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)

    # Paste logo centered horizontally, near top
    logo = render_logo()
    logo_x = (WIDTH - LOGO_W) // 2
    logo_y = 60
    canvas.paste(logo, (logo_x, logo_y), mask=logo.split()[3])

    draw = ImageDraw.Draw(canvas)

    # Try to load a nice font; fall back to default
    title_size = 48
    tagline_size = 24
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", title_size)
        tagline_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", tagline_size)
    except OSError:
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()

    # Title: "Tic-Tac-Toe"
    title = "Tic-Tac-Toe"
    title_y = logo_y + LOGO_H + 40
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((title_x, title_y), title, fill="#E6EDF3", font=title_font)

    # Tagline: "Designed for your car"
    tagline = "Designed for your car"
    tagline_y = title_y + title_size + 20
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((tagline_x, tagline_y), tagline, fill="#8B949E", font=tagline_font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, "PNG")
    print(f"Feature graphic saved: {OUTPUT} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
