"""Generate the MediServ logo SVGs (heart + pulse line icon, Inter Bold wordmark).

The wordmark is converted to outlines so the SVGs render identically without the font.
Usage: python3 scripts/build_logo.py [path/to/Inter-Bold.otf]
"""
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
OUT = Path(__file__).resolve().parent.parent / "logo"

CORAL_TOP, CORAL_BOTTOM = "#FF6B6B", "#E63950"
NAVY = "#1E2A4A"

HEART = ("M50 90 C22 70 6 54 6 34 C6 19 17 8 31 8 C40 8 46 13 50 20 "
         "C54 13 60 8 69 8 C83 8 94 19 94 34 C94 54 78 70 50 90 Z")
PULSE = "M18 50 H31 L38 36 L47 66 L56 26 L64 56 L69 50 H82"

FONT_SIZE = 62
TRACKING = -1.2  # units per letter, tightens the display wordmark slightly


def text_paths(font, text, x, baseline, size):
    """Return a list of SVG path strings for `text`, plus the advance end x."""
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    paths = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set)
        # Flip y: font units are y-up, SVG is y-down.
        glyph_set[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        paths.append(pen.getCommands())
        x += glyph_set[name].width * scale + TRACKING
    return paths, x - TRACKING


def icon(gradient_id):
    return (f'<path d="{HEART}" fill="url(#{gradient_id})"/>\n'
            f'  <path d="{PULSE}" fill="none" stroke="#FFFFFF" stroke-width="6" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def gradient(gradient_id):
    return (f'<linearGradient id="{gradient_id}" x1="0" y1="0" x2="0" y2="1">\n'
            f'      <stop offset="0" stop-color="{CORAL_TOP}"/>\n'
            f'      <stop offset="1" stop-color="{CORAL_BOTTOM}"/>\n'
            '    </linearGradient>')


def svg(width, height, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" '
            f'width="{width:g}" height="{height:g}" role="img" aria-label="{title}">\n'
            f'  <title>{title}</title>\n{body}\n</svg>\n')


def main():
    font = TTFont(FONT)
    baseline = 50 + 0.727 * FONT_SIZE / 2  # vertically centre cap height on the icon
    medi, end = text_paths(font, "Medi", 110, baseline, FONT_SIZE)
    serv, end = text_paths(font, "Serv", end + TRACKING, baseline, FONT_SIZE)
    width = round(end + 6)

    def wordmark(medi_color, serv_color):
        return (f'  <path fill="{medi_color}" d="{" ".join(medi)}"/>\n'
                f'  <path fill="{serv_color}" d="{" ".join(serv)}"/>')

    variants = {
        "mediserv-logo.svg": (wordmark(NAVY, CORAL_BOTTOM), "heart"),
        "mediserv-logo-white.svg": (wordmark("#FFFFFF", "#FFFFFF"), "heart-w"),
    }
    for name, (words, gid) in variants.items():
        body = f"  <defs>\n    {gradient(gid)}\n  </defs>\n  {icon(gid)}\n{words}"
        (OUT / name).write_text(svg(width, 100, body, "MediServ"))

    body = f"  <defs>\n    {gradient('heart-i')}\n  </defs>\n  {icon('heart-i')}"
    (OUT / "mediserv-icon.svg").write_text(svg(100, 100, body, "MediServ icon"))
    print(f"wrote logo SVGs to {OUT} (wordmark width {width})")


if __name__ == "__main__":
    main()
