"""Programmers' Day (day 256 of the year): the western town goes online.

Glowing binary digits that fall like fireflies, a lit sign that reads 256 with a blinking cursor, a rubber duck waiting
to hear about your bug, a terminal cursor that types after the cowboy's job title, a steaming coffee mug in the
cowboy's hand, glasses and code braces on the poster, and a terminal line that says HELLO WORLD in place of the
divider. The cowboy keeps his hat and the horse is untouched.
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import build_assets as ba  # noqa: E402
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402
from .kit import COMMON_CSS, GLYPHS, REDUCED, fall_css, outlined, sprite  # noqa: E402

GREEN = "#4be37a"
BRIGHT = "#9dffb8"
DIM = "#2bbf63"
SCREEN = "#0d1a14"
BORDER = "#1f6b3a"
WHITE = "#ffffff"
COFFEE = "#6b3a1e"
DUCK = (".yy...", ".yko.", "yyyoo.", "yyyyy.", ".yyyy.")
DUCK_COL = {"y": "#ffe14d", "k": "#1a0f1c", "o": "#f28a2e"}


def digits_pixels(grid, text, x, y, color):
    """Draws the text in the 3 by 5 pixel alphabet. Returns the width used."""
    cx = x
    for ch in text:
        glyph = GLYPHS.get(ch)
        if glyph is None:
            cx += 3
            continue
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "1":
                    grid.set(cx + c, y + r, color)
        cx += len(glyph[0]) + 1
    return cx - x


def binary_rain(seed, n, height, duration, delay=0, columns=((150, 196),)):
    """Binary digits falling slowly, in shades of green, in two stacked copies so the loop has no gap. They only
    fall in the given x ranges, so they never cross the name, the role or the footer text."""
    rnd = random.Random(seed)
    g = Grid()
    for _ in range(n):
        x0, x1 = rnd.choice(columns)
        digits_pixels(g, rnd.choice("01"), rnd.randrange(x0, x1 - 3), rnd.randrange(0, height), rnd.choice([DIM, GREEN, BRIGHT]))
    return ('<g class="dr%d" opacity="0.8" style="animation-duration:%ds;animation-delay:-%ds">%s'
            '<g transform="translate(0 -%d)">%s</g></g>' % (height, duration, delay, g.paths(), height, g.paths()))


def lit_sign(x, y_bottom):
    """A wooden post with a dark screen that reads 256 in green and a blinking cursor. Returns (static, blinking) SVG."""
    g = Grid()
    top = y_bottom - 16
    g.rect(x + 11, top + 11, 3, 6, "#5a3a1c")                      # the post
    g.rect(x, top, 25, 11, BORDER)                                  # frame
    g.rect(x + 1, top + 1, 23, 9, SCREEN)                           # screen
    text = Grid()
    text.text("256", x + 2, top + 2, GREEN, 1)
    cursor = Grid()
    cursor.rect(x + 21, top + 2, 2, 7, BRIGHT)
    return outlined(g).paths() + '<g class="tw1">%s</g>' % text.paths(), '<g class="blink">%s</g>' % cursor.paths()


def duck(x, y_bottom):
    return outlined(sprite(DUCK, DUCK_COL, x, y_bottom))


def coffee_extra():
    """A coffee mug in the cowboy's hand with steam rising, in rider coordinates. It stays at or below row -21."""
    mug = Grid()
    mug.rect(12, -17, 3, 3, WHITE)
    mug.rect(12, -17, 3, 1, COFFEE)
    mug.set(15, -16, WHITE)
    steam = Grid()
    steam.set(13, -19, "#e8e8f0")
    steam.set(14, -21, "#e8e8f0")
    return mug.paths() + '<g class="steam">%s</g>' % steam.paths()


def glasses(g):
    """Round glasses on the poster portrait, in absolute poster pixels, around the eyes at x 55 to 57 and 62 to 64."""
    dark = "#1a0f1c"
    for x0 in (53, 60):
        g.rect(x0, 55, 7, 1, dark)
        g.rect(x0, 59, 7, 1, dark)
        g.rect(x0, 55, 1, 5, dark)
        g.rect(x0 + 6, 55, 1, 5, dark)
    g.rect(60, 57, 1, 1, dark)                       # the bridge
    g.set(54, 56, "#bfe3ff")                         # a little shine on each lens
    g.set(61, 56, "#bfe3ff")


def braces_and_sticker(g):
    """Code braces in the top corners."""
    digits_pixels(g, "{", 3, 4, "#2a6b45")
    digits_pixels(g, "}", 115, 4, "#2a6b45")


def terminal_strip():
    """HELLO WORLD on a terminal line that replaces the divider, exactly its size (160 by 10)."""
    g = Grid()
    g.rect(1, 1, 158, 8, BORDER)
    g.rect(2, 2, 156, 6, SCREEN)
    text = "> HELLO WORLD"
    width = 0
    for ch in text:
        width += (len(GLYPHS[ch][0]) + 1) if ch in GLYPHS else 3
    x0 = (160 - width - 4) // 2
    used = digits_pixels(g, text, x0, 3, GREEN)
    cursor = Grid()
    cursor.rect(x0 + used + 1, 3, 2, 5, BRIGHT)
    for i, bit in enumerate("10110100"):             # dim binary digits at both ends, four each, never touching the text
        x = 8 + i * 8 if i < 4 else x0 + used + 12 + (i - 4) * 8
        digits_pixels(g, bit, x, 3, "#1b5a35")
    return g, cursor


CSS = COMMON_CSS + """
.blink{animation:blink 1s steps(1) infinite}
.steam{animation:steam 1.6s steps(1) infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
@keyframes steam{0%{transform:translateY(0);opacity:.9}50%{transform:translateY(-1px);opacity:.5}}
"""
SELF_CSS = CSS + REDUCED


class ProgrammersDay(Decor):
    id = "programmers-day"
    name = "Programmers' Day"
    status = "approved"

    def banner(self):
        sign, cursor = lit_sign(58, 58)
        ground = sign + cursor + duck(92, 58).paths()
        sky = binary_rain(71, 10, 60, 16, columns=((152, 196),)) + binary_rain(72, 4, 60, 11, 4, columns=((152, 196),))
        type_cursor = Grid()
        type_cursor.rect(112, 21, 3, 7, BRIGHT)                    # right after SOFTWARE ENGINEER, like someone typing
        front = '<g class="blink">%s</g>' % type_cursor.paths()
        return Layers(ground=ground, sky=sky, front=front, rider_extra=coffee_extra(),
                      css=CSS + fall_css(60, "dr"),
                      label="Programmers' Day decoration: falling binary digits, a lit 256 sign, a rubber duck and a blinking cursor")

    def footer(self):
        sign, cursor = lit_sign(173, 29)
        ground = sign + cursor + duck(30, 28).paths()
        sky = binary_rain(73, 5, 30, 12, columns=((3, 28),))
        return Layers(text="HAPPY PROGRAMMERS DAY", ground=ground, sky=sky, rider_extra=coffee_extra(),
                      css=CSS + fall_css(30, "dr"))

    def poster(self):
        def draw(g):
            glasses(g)
            braces_and_sticker(g)

        return Layers(draw=draw, css=SELF_CSS)

    def strip(self):
        g, cursor = terminal_strip()
        body = g.paths() + '<g class="blink">%s</g>' % cursor.paths()
        return Layers(width=160, height=10, scale=5, body=body, css=SELF_CSS, label="Terminal line that says hello world")


DECOR = ProgrammersDay()
