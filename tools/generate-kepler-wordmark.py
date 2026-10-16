#!/usr/bin/env python3
"""Deterministic KeplerLLM wordmark generator (Browser Extension).

Regenerates src/media/kepler-llm.png from the original upstream
"Anything LLM" 634x99 asset (white text for dark background) with the
text swapped to 'Kepler LLM', preserving the infinity-mark icon pixels
verbatim.

Validated recipe (per rebrand task):
  - Font: tools/fonts/PlusJakartaSans.ttf (Regular), size 86,
    stroke_width=2
  - Icon: pixels originais preservados (crop((0, 0, 99+5, H)))
  - Text: single 'Kepler LLM' monochrome WHITE=(255,255,255,255),
    anchor='lt'
  - Position: x = 123 - bbox_first[0], y = 16 - bbox_full[1]
    (bbox_first = textbbox of first char 'K', bbox_full = textbbox of
    full text, both with anchor='lt' + stroke_width=2)
  - Canvas 634x99; asserts de geometria
  - Verify by compositing over black background (white text needs dark
    bg to be visible).

Reference geometry (measured from upstream asset):
  - canvas 634x99; icon bbox (0,16)-(97,79) within 0..104 crop
  - original text bbox (123,22)-(627,98); new text bbox (123,16)-(571,102)
  - gap 98..122 empty; text_start=123, orig_top(icon)=16

Determinism: no timestamps, no randomness; PNG saved with default
encoder settings. Re-running on the same Pillow version yields
byte-identical files.

Requires: Pillow (pip install pillow). Run from repo root:
  python3 tools/generate-kepler-wordmark.py
"""

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_PATH = ROOT / "tools/fonts/PlusJakartaSans.ttf"
DST_PATH = ROOT / "src/media/kepler-llm.png"

TEXT = "Kepler LLM"
SIZE = 86
STROKE = 2
ICON_END = 99  # crop x 0..99+5 (104px) preserves icon + margin
TEXT_X = 123
TEXT_Y = 16  # align text top with icon top (icon bbox top=16)
CANVAS = (634, 99)

WHITE = (255, 255, 255, 255)


def load_reference() -> Image.Image:
    # Post `git mv`, DST already holds the old bytes on first generation
    # (icon region identical), so it works as reference; later re-runs
    # are idempotent (icon preserved, text redrawn identically).
    if DST_PATH.exists():
        return Image.open(DST_PATH).convert("RGBA")
    raise FileNotFoundError(f"{DST_PATH} missing")


def load_font(size: int) -> ImageFont.FreeTypeFont:
    # Regular weight + stroke (validated recipe); no variation axes.
    return ImageFont.truetype(str(FONT_PATH), size)


def build_wordmark(ref_image: Image.Image, color: tuple) -> Image.Image:
    w, h = ref_image.size
    assert (w, h) == CANVAS, f"reference size {ref_image.size} != {CANVAS}"
    font = load_font(SIZE)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # Icon pixels preserved verbatim from the original asset.
    icon = ref_image.crop((0, 0, ICON_END + 5, h))
    assert icon.size == (ICON_END + 5, h), icon.size
    canvas.alpha_composite(icon, (0, 0))
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    full = tmp.textbbox((0, 0), TEXT, font=font, stroke_width=STROKE, anchor="lt")
    first = tmp.textbbox((0, 0), TEXT[0], font=font, stroke_width=STROKE, anchor="lt")
    x = TEXT_X - first[0]
    y = TEXT_Y - full[1]
    # Geometry asserts (lock validated recipe; Pillow-dependent).
    assert (x, y) == (125, 18), f"unexpected text origin {(x, y)}"
    draw = ImageDraw.Draw(canvas)
    draw.text(
        (x, y),
        TEXT,
        font=font,
        fill=color,
        stroke_width=STROKE,
        stroke_fill=color,
        anchor="lt",
    )
    return canvas


def assert_icon_preserved(out: Image.Image, ref: Image.Image) -> None:
    # Icon pixels preserved verbatim: RGBA must match wherever alpha>0;
    # fully transparent pixels are visually identical regardless of RGB
    # (Pillow normalizes transparent white to transparent black on
    # alpha_composite), so only alpha==0 is required there.
    out_icon = out.crop((0, 0, ICON_END + 5, CANVAS[1]))
    ref_icon = ref.crop((0, 0, ICON_END + 5, CANVAS[1]))
    assert out_icon.size == ref_icon.size, (out_icon.size, ref_icon.size)
    o_px, r_px = out_icon.load(), ref_icon.load()
    w, h = out_icon.size
    for yy in range(h):
        for xx in range(w):
            o, r = o_px[xx, yy], r_px[xx, yy]
            if r[3] == 0:
                assert o[3] == 0, f"icon alpha changed at {(xx, yy)}: {o} vs {r}"
            else:
                assert o == r, f"icon pixel changed at {(xx, yy)}: {o} vs {r}"


def main() -> int:
    ref = load_reference()
    assert ref.size == CANVAS, ref.size
    out = build_wordmark(ref, WHITE)
    assert out.size == CANVAS, out.size
    assert_icon_preserved(out, ref)
    # Geometry asserts: vector bbox (recipe) + raster sanity.
    # Vector bbox for 'Kepler LLM' at (125,18) lt stroke 2 is
    # (123,16,571,102): left=123 (TEXT_X), top=16 (TEXT_Y), right=571
    # (fits 634 with 63px margin), bottom=102 (3px descender overflow,
    # clipped to canvas H=99 on save).
    font = load_font(SIZE)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    vec = probe.textbbox(
        (125, 18), TEXT, font=font, stroke_width=STROKE, anchor="lt"
    )
    assert vec == (123, 16, 571, 102), vec
    # Raster check (composing over transparent): top must be 16;
    # left is 131 for 'K' (8px empty bearing in vector box, unlike 'A'),
    # right must fit canvas, bottom clips at 99.
    text_area = out.crop((TEXT_X, 0, CANVAS[0], CANVAS[1]))
    bbox = text_area.getbbox()
    assert bbox is not None, "text area empty"
    assert bbox[1] == 16, bbox
    assert bbox[2] <= CANVAS[0] - TEXT_X, bbox
    out.save(DST_PATH)
    data = DST_PATH.read_bytes()
    print(f"{hashlib.md5(data).hexdigest()}  src/media/kepler-llm.png")
    print(f"size={out.size} text_origin=(125,18) text_bbox_abs=(123,16,571,102)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
