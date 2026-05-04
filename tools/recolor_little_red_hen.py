"""
Recolor checkerboard "black" squares on the Little Red Hen artwork to site accent red.

The sprite aliases outline blacks (near #040304) onto checker blacks; tight regions keep the
circle and plumage contours, with a softer halo mid-tones and a narrow tail extension for apron fill.
"""

from pathlib import Path

from PIL import Image

ACCENT = (179, 45, 56)  # --color-accent #b32d38

SCRIPT = Path(__file__).resolve()
ROOT = SCRIPT.parent.parent
SRC = ROOT / "_assets_upload" / "little-red-hen-source.png"
OUT = ROOT / "images" / "little-red-hen-edition.png"

EXACT_REMAP = {
    (13, 16, 16): ACCENT,
    (23, 20, 22): ACCENT,
    (37, 39, 39): ACCENT,
}

MASKED_REMAP = {
    (38, 27, 28): ACCENT,
    (50, 38, 26): ACCENT,
    (53, 51, 52): ACCENT,
    (91, 19, 30): ACCENT,
    (114, 9, 24): ACCENT,
    (72, 49, 50): ACCENT,
    (77, 33, 33): ACCENT,
    (54, 11, 13): ACCENT,
    (81, 7, 16): ACCENT,
    (62, 61, 62): ACCENT,
    (103, 34, 46): ACCENT,
    (87, 66, 46): ACCENT,
    (70, 68, 68): ACCENT,
    (116, 21, 36): ACCENT,
}

OUTLINE_BLACK = (4, 3, 4)


def in_outline_checker_replace(x: int, y: int) -> bool:
    """Hat + apron + apron tail where pure-black overlaps checker (not circle outer ring)."""
    hat = (12 <= y <= 46) and (32 <= x <= 61)
    apron = (44 <= y <= 88) and (22 <= x <= 58)
    apron_tail_outline = (55 <= y <= 90) and (22 <= x <= 63)
    return hat or apron or apron_tail_outline


def in_checker_soft_halo(x: int, y: int) -> bool:
    hat = (10 <= y <= 48) and (28 <= x <= 62)
    apron = (42 <= y <= 94) and (17 <= x <= 76)
    return hat or apron


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source image: {SRC}")
    img = Image.open(SRC).convert("RGBA")
    px = img.load()
    w, h = img.size
    replaced = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            tup = (r, g, b)

            if tup == OUTLINE_BLACK and in_outline_checker_replace(x, y):
                px[x, y] = (*ACCENT, a)
                replaced += 1
                continue

            if tup in EXACT_REMAP and in_outline_checker_replace(x, y):
                px[x, y] = (*EXACT_REMAP[tup], a)
                replaced += 1
                continue

            if tup not in MASKED_REMAP:
                continue

            halo = in_checker_soft_halo(x, y)
            apron_tail = y >= 59 and tup == (50, 38, 26)
            if halo or apron_tail:
                px[x, y] = (*MASKED_REMAP[tup], a)
                replaced += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, optimize=True)
    print(f"Wrote {OUT} ({replaced} px recolored)")


if __name__ == "__main__":
    main()
