"""Shared building blocks for season art: ascii sprites, a pixel alphabet, bunting and confetti.

Older seasons keep their own copies of these. New ones import from here.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

STRING = "#3b2414"

# A pixel alphabet, 5 rows high. A glyph may be any width, all rows of one glyph have the same length.
GLYPHS = {
    "A": ("010", "101", "111", "101", "101"), "B": ("110", "101", "110", "101", "110"),
    "C": ("011", "100", "100", "100", "011"), "D": ("110", "101", "101", "101", "110"),
    "E": ("111", "100", "110", "100", "111"), "F": ("111", "100", "110", "100", "100"),
    "G": ("011", "100", "101", "101", "011"), "H": ("101", "101", "111", "101", "101"),
    "I": ("111", "010", "010", "010", "111"), "J": ("001", "001", "001", "101", "010"),
    "K": ("101", "101", "110", "101", "101"), "L": ("100", "100", "100", "100", "111"),
    "M": ("10001", "11011", "10101", "10001", "10001"), "N": ("1001", "1101", "1011", "1001", "1001"),
    "O": ("010", "101", "101", "101", "010"), "P": ("110", "101", "110", "100", "100"),
    "R": ("110", "101", "110", "101", "101"), "S": ("011", "100", "010", "001", "110"),
    "T": ("111", "010", "010", "010", "010"), "U": ("101", "101", "101", "101", "111"),
    "V": ("101", "101", "101", "101", "010"), "W": ("10001", "10001", "10101", "10101", "01010"),
    "X": ("101", "101", "010", "101", "101"), "Y": ("101", "101", "010", "010", "010"),
    "Z": ("111", "001", "010", "100", "111"),
    "0": ("111", "101", "101", "101", "111"), "1": ("010", "110", "010", "010", "111"),
    "2": ("110", "001", "010", "100", "111"), "3": ("110", "001", "110", "001", "110"),
    "4": ("101", "101", "111", "001", "001"), "5": ("111", "100", "110", "001", "110"),
    "6": ("011", "100", "111", "101", "111"), "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"), "9": ("111", "101", "111", "001", "110"),
    "!": ("1", "1", "1", "0", "1"), ">": ("100", "010", "001", "010", "100"), "_": ("000", "000", "000", "000", "111"),
    "{": ("011", "010", "110", "010", "011"), "}": ("110", "010", "011", "010", "110"),
    "/": ("001", "001", "010", "100", "100"), "<": ("001", "010", "100", "010", "001"),
}


def sprite(rows, colors, x, y_bottom):
    """Pixel art from an ascii picture. The bottom row sits on y_bottom. Characters not in colors are empty."""
    g = Grid()
    top = y_bottom - len(rows) + 1
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                g.set(x + c, top + r, colors[ch])
    return g


def outlined(grid, color="#1d1008"):
    """The same sprite with a one pixel dark outline, so it stands out from ground of a similar color."""
    out = Grid()
    for (x, y) in list(grid.px):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in grid.px:
                out.set(q[0], q[1], color)
    out.px.update(grid.px)
    return out


def text_layout(text, gap=4, width=160):
    """Where each flag of a bunting goes: ([(char, x)], total width). A flag is the letter plus one pixel of
    margin on each side, with one pixel between flags."""
    x, items = 0, []
    for ch in text:
        if ch == " ":
            x += gap
            continue
        items.append((ch, x))
        x += len(GLYPHS[ch][0]) + 3
    total = x - 1
    x0 = (width - total) // 2
    return [(ch, x0 + dx) for ch, dx in items], total


def bunting(text, flag_colors, text_color, width=160, gap=4, string=STRING):
    """Flags with letters on a sagging string, sized for the 160 by 10 divider. text_color may be one color or a
    list that follows the flags, so red flags can carry white letters and white flags blue ones.
    Returns (grid, x of the first flag, x after the last flag, y of the string at each x)."""
    g = Grid()
    pts = []
    for x in range(width):
        y = int(round(1.0 * math.sin(math.pi * x / (width - 1))))
        g.set(x, y, string)
        pts.append((x, y))
    items, _ = text_layout(text, gap, width)
    text_colors = list(text_color) if isinstance(text_color, (list, tuple)) else [text_color]
    for n, (ch, x) in enumerate(items):
        glyph = GLYPHS[ch]
        gw = len(glyph[0])
        top = pts[x + 1][1] + 1
        color = flag_colors[n % len(flag_colors)]
        letter = text_colors[n % len(text_colors)]
        g.rect(x, top, gw + 2, 7, color)
        g.set(x + (gw + 2) // 2, top + 7, color)               # the pennant tip
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "1":
                    g.set(x + 1 + c, top + 1 + r, letter)
    first = items[0][1]
    last = items[-1][1] + len(GLYPHS[items[-1][0]][0]) + 2
    return g, first, last, pts


def scatter_on_string(g, pts, rnd, first, last, colors, count, width=160):
    """Confetti along the string, away from the letters."""
    spots = list(range(2, max(3, first - 3))) + list(range(last + 3, width - 2))
    for _ in range(count):
        x = rnd.choice(spots)
        g.set(x, pts[x][1] + rnd.randrange(1, 5), rnd.choice(colors))


def confetti_layer(seed, n, height, duration, colors, delay=0, width=200, name="cf"):
    """Pieces falling; two stacked copies so the loop has no gap. Needs fall_css(name, height)."""
    rnd = random.Random(seed)
    g = Grid()
    for _ in range(n):
        g.set(rnd.randrange(1, width - 1), rnd.randrange(0, height), rnd.choice(colors))
    return ('<g class="%s%d" style="animation-duration:%ds;animation-delay:-%ds">%s'
            '<g transform="translate(0 -%d)">%s</g></g>' % (name, height, duration, delay, g.paths(), height, g.paths()))


def fall_css(height, name="cf"):
    return (".%s%d{animation:%sfall%d 9s linear infinite}@keyframes %sfall%d{from{transform:translateY(0)}"
            "to{transform:translateY(%dpx)}}" % (name, height, name, height, name, height, height))


COMMON_CSS = """
.tw1{animation:tw 1.4s steps(1) infinite}
.tw2{animation:tw 1.4s steps(1) infinite;animation-delay:.7s}
@keyframes tw{0%{opacity:1}50%{opacity:.15}}
"""
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n"


def covers_hat(cover_pixels, rider_grid, ink):
    """The cowboy hat pixels (crown x5 to 9 on rows -22 and -21, brim x4 to 10 on row -20) that a hat
    replacement fails to cover. An empty set means the old hat is fully hidden."""
    hat = {(x, y) for (x, y), c in rider_grid.px.items() if c == ink and -22 <= y <= -20 and 4 <= x <= 10}
    return hat - set(cover_pixels)
