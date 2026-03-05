#!/usr/bin/env python3
"""Scale AAOS screenshots to phone-friendly dimensions for Play Store.

Since only the automotive system image is available, we crop the AAOS
screenshots to remove the system bars and scale to a phone-like 1080x1920
portrait layout with letterboxing on a dark background.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "docs" / "store-assets"

PHONE_W, PHONE_H = 1080, 1920
BG_COLOR = (13, 17, 23)  # #0D1117

AAOS_SCREENSHOTS = [
    ("aaos-screenshot-1-empty-board.png", "phone-screenshot-1-empty-board.png"),
    ("aaos-screenshot-2-game-in-progress.png", "phone-screenshot-2-game-in-progress.png"),
    ("aaos-screenshot-3-win-state.png", "phone-screenshot-3-win-state.png"),
    ("aaos-screenshot-4-two-player.png", "phone-screenshot-4-two-player.png"),
]


EXPECTED_W, EXPECTED_H = 1024, 768


def scale_to_phone(src: Path, dst: Path) -> None:
    """Crop AAOS system bars and center app content on phone canvas."""
    with Image.open(src) as img:
        w, h = img.size
        if (w, h) != (EXPECTED_W, EXPECTED_H):
            raise ValueError(
                f"Unexpected screenshot size for {src.name}: {w}x{h} "
                f"(expected {EXPECTED_W}x{EXPECTED_H})"
            )

        # AAOS 1024x768: status bar ~42px, app content ends ~696px, car nav below
        top_crop = 42
        bottom_crop = h - 696
        cropped = img.crop((0, top_crop, w, h - bottom_crop))

    # Scale to fill phone width
    cw, ch = cropped.size
    scale = PHONE_W / cw
    new_w = PHONE_W
    new_h = int(ch * scale)
    scaled = cropped.resize((new_w, new_h), Image.LANCZOS)

    # Center vertically on phone canvas
    canvas = Image.new("RGB", (PHONE_W, PHONE_H), BG_COLOR)
    y_offset = (PHONE_H - new_h) // 2
    canvas.paste(scaled, (0, y_offset))
    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst, "PNG")
    print(f"Phone screenshot saved: {dst.name} ({PHONE_W}x{PHONE_H})")


def main() -> None:
    for aaos_name, phone_name in AAOS_SCREENSHOTS:
        src = STORE / aaos_name
        dst = STORE / phone_name
        if src.exists():
            scale_to_phone(src, dst)
        else:
            print(f"Warning: {src} not found, skipping")


if __name__ == "__main__":
    main()
