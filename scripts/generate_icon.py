#!/usr/bin/env python3
"""Generate a 512x512 Play Store icon from adaptive icon XML layers."""

import io
from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "store-assets" / "icon-512.png"

SIZE = 512
VIEWPORT = 108  # Android adaptive icon viewport


def build_background_svg() -> str:
    """Background layer: solid #0D1117 filling the viewport."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 {VIEWPORT} {VIEWPORT}" width="{SIZE}" height="{SIZE}">
      <rect width="{VIEWPORT}" height="{VIEWPORT}" fill="#0D1117"/>
    </svg>"""


def build_foreground_svg() -> str:
    """Foreground layer: grid + LF monogram strokes."""
    paths = []

    # Grid — outer boundary
    paths.append(
        '<path d="M29,29 L79,29 L79,79 L29,79 Z" '
        'stroke="#30363D" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" fill="none"/>'
    )
    # Grid dividers
    for d in ["M46,29 L46,79", "M62,29 L62,79", "M29,46 L79,46", "M29,62 L79,62"]:
        paths.append(
            f'<path d="{d}" stroke="#30363D" stroke-width="2" '
            f'stroke-linecap="round" fill="none"/>'
        )
    # L — vertical + horizontal
    paths.append(
        '<path d="M31,36 L31,72" stroke="#00B4D8" stroke-width="4" '
        'stroke-linecap="round" fill="none"/>'
    )
    paths.append(
        '<path d="M31,72 L48,72" stroke="#00B4D8" stroke-width="4" '
        'stroke-linecap="round" fill="none"/>'
    )
    # F — vertical + top + middle
    paths.append(
        '<path d="M56,36 L56,72" stroke="#E6EDF3" stroke-width="4" '
        'stroke-linecap="round" fill="none"/>'
    )
    paths.append(
        '<path d="M56,36 L77,36" stroke="#E6EDF3" stroke-width="4" '
        'stroke-linecap="round" fill="none"/>'
    )
    paths.append(
        '<path d="M56,53 L73,53" stroke="#E6EDF3" stroke-width="4" '
        'stroke-linecap="round" fill="none"/>'
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 {VIEWPORT} {VIEWPORT}" width="{SIZE}" height="{SIZE}">
      {"".join(paths)}
    </svg>"""


def render_layer(svg: str) -> Image.Image:
    """Render SVG string to a Pillow RGBA image."""
    png_data = cairosvg.svg2png(bytestring=svg.encode(), output_width=SIZE, output_height=SIZE)
    with Image.open(io.BytesIO(png_data)) as img:
        return img.convert("RGBA")


def main() -> None:
    bg = render_layer(build_background_svg())
    fg = render_layer(build_foreground_svg())
    composite = Image.alpha_composite(bg, fg)
    # Flatten to RGB — Play Store requires opaque icon
    final = Image.new("RGB", composite.size, (13, 17, 23))  # #0D1117
    final.paste(composite, mask=composite.split()[3])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    final.save(OUTPUT, "PNG")
    print(f"Icon saved: {OUTPUT} ({final.size[0]}x{final.size[1]})")


if __name__ == "__main__":
    main()
