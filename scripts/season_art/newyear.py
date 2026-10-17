"""New Year (31 Dec and 1 Jan): midnight in the western town.

A midnight sky with golden stars, fireworks that burst over the mesas, gold and silver confetti, a
grandfather clock striking twelve, a golden hat for the cowboy, a glittering poster frame and the
greeting with the number of the new year spelled on the bunting that replaces the divider.

The number is the year that starts: on 31 Dec it is the next year, on 1 Jan it is the current one.
"""
import datetime
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import build_assets as ba  # noqa: E402
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402
from .birthday import confetti_css, confetti_layer  # noqa: E402

GOLD = "#f2c14e"
DEEP_GOLD = "#c9961e"
SILVER = "#d9dde6"
NAVY = "#1e2a5a"
NAVY2 = "#2a3a7a"
PLUM = "#4a2a7a"
MIDNIGHT = "#0b1030"
WHITE = "#fff3d6"
BURST_COLORS = [GOLD, "#e84a4a", "#4ad8c8", WHITE, "#b084f0"]
CONFETTI = [GOLD, SILVER, WHITE, DEEP_GOLD, "#e84a4a"]

# Pixel letters for the bunting. A glyph can have any width, every row of one glyph has the same length.
GLYPHS = {
    "H": ("101", "101", "111", "101", "101"),
    "A": ("010", "101", "111", "101", "101"),
    "P": ("110", "101", "110", "100", "100"),
    "Y": ("101", "101", "010", "010", "010"),
    "N": ("1001", "1101", "1011", "1001", "1001"),
    "E": ("111", "100", "110", "100", "111"),
    "W": ("10001", "10001", "10101", "10101", "01010"),
    "R": ("110", "101", "110", "101", "101"),
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("110", "001", "010", "100", "111"),
    "3": ("110", "001", "110", "001", "110"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "110", "001", "110"),
    "6": ("011", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "110"),
}


def new_year_number(day):
    """The year that begins: the next year on 31 Dec, the current year on 1 Jan (and any other day)."""
    return day.year + 1 if (day.month, day.day) == (12, 31) else day.year


def bunting_layout(text, gap=4, width=160):
    """Where every flag of the bunting goes: (character, x) pairs, and the total width. Flags are the
    letter plus one pixel of margin on each side and one pixel between flags."""
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


def burst_frames(cx, cy, color, delay, radii=(3, 6, 9, 11, 13), n=18, cycle=3.6):
    """A firework as five frames that show one after the other: a flash, then a growing ring with a second,
    inner ring in another color, and finally the sparks fading out in white. Returns SVG."""
    out = []
    inner = BURST_COLORS[(BURST_COLORS.index(color) + 2) % len(BURST_COLORS)] if color in BURST_COLORS else GOLD
    for k, r in enumerate(radii):
        g = Grid()
        if k == 0:                                        # the flash where the rocket explodes
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                g.set(cx + dx, cy + dy, WHITE)
        for i in range(n):
            a = 2 * math.pi * i / n + (0.17 if k % 2 else 0)
            c = color if k < 3 else WHITE
            g.set(cx + int(round(r * math.cos(a))), cy + int(round(r * math.sin(a))), c)
            if k >= 1 and i % 2 == 0:                     # the inner ring, in a second color
                rr = r * 0.55
                g.set(cx + int(round(rr * math.cos(a))), cy + int(round(rr * math.sin(a))), inner if k < 3 else GOLD)
            if k >= 2 and i % 3 == 0:                     # sparks flying a little further out
                rr = r + 2
                g.set(cx + int(round(rr * math.cos(a + 0.1))), cy + int(round(rr * math.sin(a + 0.1))), GOLD)
        last = " fwlast" if k == len(radii) - 2 else ""
        out.append('<g class="fwf%s" style="animation-delay:%.2fs;animation-duration:%.1fs">%s</g>'
                   % (last, delay + k * 0.28, cycle, g.paths()))
    return "".join(out)


def fireworks(spec):
    """spec: list of (x, y, color index, delay)."""
    return "".join(burst_frames(x, y, BURST_COLORS[c % len(BURST_COLORS)], d) for x, y, c, d in spec)


def sparkles(seed, n, ymax, width=200):
    """Golden stars that twinkle in two groups, some of them as small plus signs."""
    rnd = random.Random(seed)
    groups = [Grid(), Grid()]
    for i in range(n):
        x, y = rnd.randrange(3, width - 3), rnd.randrange(1, ymax)
        g = groups[i % 2]
        g.set(x, y, GOLD)
        if i % 3 == 0:                                   # a plus shaped sparkle
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                g.set(x + dx, y + dy, "#f7dc8a")
    return '<g class="tw1">%s</g><g class="tw2">%s</g>' % (groups[0].paths(), groups[1].paths())


def midnight_overlay(width, height, opacity=0.42):
    return '<rect x="0" y="0" width="%d" height="%d" fill="%s" opacity="%s"/>' % (width, height, MIDNIGHT, opacity)


def grandfather_clock(x, y_bottom):
    """A clock striking twelve: both hands up. The pendulum swings and the face glows."""
    g = Grid()
    top = y_bottom - 13
    g.rect(x, top + 2, 7, 11, "#6b4423")              # case
    g.rect(x + 1, top, 5, 2, "#6b4423")               # hood
    g.rect(x + 3, top - 1, 1, 1, GOLD)                # finial
    g.rect(x + 1, top + 3, 5, 5, WHITE)               # face
    g.rect(x + 3, top + 4, 1, 2, "#1a0f1c")           # minute hand pointing up
    g.set(x + 3, top + 5, "#1a0f1c")                  # hour hand, also up: midnight
    g.set(x + 3, top + 6, "#1a0f1c")
    g.rect(x + 1, top + 9, 5, 3, "#4a2d14")           # door
    g.rect(x - 1, y_bottom, 9, 1, "#3b2414")          # base
    pend = Grid()
    pend.rect(x + 3, top + 9, 1, 2, GOLD)
    pend.rect(x + 2, top + 11, 3, 1, GOLD)
    glow = Grid()
    glow.rect(x + 1, top + 3, 5, 5, "#fff3d6")
    return (g.paths() + '<g class="glow">%s</g><g class="swing">%s</g>' % (glow.paths(), pend.paths()))


def golden_hat_extra():
    """The gold hat REPLACES the cowboy hat: it covers the hat's pixels exactly (crown x5 to 9 on rows -22
    and -21, brim x4 to 10 on row -20) and stays at or below row -23. Rider coordinates."""
    hat = Grid()
    hat.rect(5, -22, 5, 2, GOLD)
    hat.rect(4, -20, 7, 1, DEEP_GOLD)
    hat.set(5, -22, "#f7dc8a")
    hat.set(5, -21, "#f7dc8a")
    spark = Grid()
    spark.set(7, -23, WHITE)
    return hat, spark


def rider_extra():
    hat, spark = golden_hat_extra()
    return hat.paths() + '<g class="tw1">%s</g>' % spark.paths()


def digits_grid(number, x, y, color):
    """The year in the 5 by 7 pixel font of the banner."""
    g = Grid()
    g.text(str(number), x, y, color, 1)
    return g


def top_hat_headwear(r, p, cx):
    """Replaces the cowboy hat in the poster portrait with a gold top hat with a navy band."""
    r(cx - 8, 15, 16, 3, "#2a1a10")                  # hair
    r(cx - 6, 2, 12, 12, GOLD)                        # crown
    r(cx - 6, 2, 2, 12, "#f7dc8a")                    # shine
    r(cx + 4, 2, 2, 12, DEEP_GOLD)
    r(cx - 6, 10, 12, 3, NAVY)                        # band
    r(cx - 3, 11, 1, 1, GOLD)                         # buckle
    r(cx - 11, 14, 22, 2, DEEP_GOLD)                  # brim
    r(cx - 11, 14, 22, 1, GOLD)


CSS = """
.tw1{animation:tw 1.4s steps(1) infinite}
.tw2{animation:tw 1.4s steps(1) infinite;animation-delay:.7s}
.fwf{opacity:0;animation:fwf 3.6s steps(1) infinite}
.glow{animation:glw 2.4s ease-in-out infinite}
.swing{transform-box:fill-box;transform-origin:50% 0;animation:swg 2s ease-in-out infinite}
@keyframes tw{0%{opacity:1}50%{opacity:.15}}
@keyframes fwf{0%{opacity:1}7.8%{opacity:0}100%{opacity:0}}
@keyframes glw{0%,100%{opacity:.15}50%{opacity:.55}}
@keyframes swg{0%,100%{transform:rotate(-14deg)}50%{transform:rotate(14deg)}}
@media (prefers-reduced-motion: reduce){.fwlast{opacity:.9!important}}
"""
SELF_CSS = CSS + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n"


class NewYear(Decor):
    status = "approved"
    id = "new-year"
    name = "New Year"

    def __init__(self, year=None):
        self.year = year or 2027

    def with_date(self, day):
        return NewYear(new_year_number(day))

    def banner(self):
        ground = (midnight_overlay(200, 51) + sparkles(11, 34, 42)
                  + grandfather_clock(104, 58))
        sky = fireworks([(24, 36, 0, 0), (100, 30, 1, 1.1), (176, 28, 2, 2.0), (60, 40, 3, 2.6)])
        front = (confetti_layer(41, 36, 60, 11, colors=CONFETTI) + confetti_layer(42, 24, 60, 8, 3, colors=CONFETTI)
                 + '<g class="tw1">%s</g>' % digits_grid(self.year, 172, 4, GOLD).paths())
        return Layers(ground=ground, sky=sky, front=front, rider_extra=rider_extra(),
                      css=CSS + confetti_css(60),
                      label="New Year decoration for %d: a midnight sky with fireworks, a clock striking twelve and confetti" % self.year)

    def footer(self):
        ground = midnight_overlay(200, 22, 0.35) + sparkles(12, 10, 20) + grandfather_clock(176, 29)
        sky = fireworks([(30, 12, 0, 0), (150, 10, 1, 1.4)])
        front = confetti_layer(43, 14, 30, 9, colors=CONFETTI)
        return Layers(text="HAPPY NEW YEAR", ground=ground, sky=sky, front=front, rider_extra=rider_extra(),
                      rider_dy=2, css=CSS + confetti_css(30))

    def poster(self):
        rnd = random.Random(61)
        allowed = [(2, 12, 3, 150), (108, 118, 34, 150), (12, 29, 36, 96), (90, 108, 36, 96), (12, 108, 94, 100)]

        def draw(g):
            for _ in range(40):                           # gold and silver confetti in the free spaces
                x0, x1, y0, y1 = rnd.choice(allowed)
                g.set(rnd.randrange(x0, x1), rnd.randrange(y0, y1), rnd.choice(CONFETTI))

        w, h = 120, 156
        ring = [Grid(), Grid()]
        pts = [(x, 2) for x in range(2, w - 2)] + [(x, h - 3) for x in range(2, w - 2)] \
              + [(2, y) for y in range(2, h - 2)] + [(w - 3, y) for y in range(2, h - 2)]
        for i, (x, y) in enumerate(pts):                  # a glittering frame along the border
            if i % 4 == 0:
                ring[(i // 4) % 2].set(x, y, GOLD if (i // 8) % 2 == 0 else WHITE)
        front = '<g class="tw1">%s</g><g class="tw2">%s</g>' % (ring[0].paths(), ring[1].paths())
        return Layers(draw=draw, headwear=top_hat_headwear, front=front, css=SELF_CSS)

    def strip(self):
        """The greeting and the year on bunting that replaces the divider, exactly its size (160 by 10)."""
        g = Grid()
        w = 160
        pts = []
        for x in range(w):
            y = int(round(1.0 * math.sin(math.pi * x / (w - 1))))
            g.set(x, y, "#3b2414")
            pts.append((x, y))
        text = "HAPPY NEW YEAR %d" % self.year
        items, _ = bunting_layout(text)
        colors = [NAVY, NAVY2, PLUM]
        for n, (ch, x) in enumerate(items):
            glyph = GLYPHS[ch]
            gw = len(glyph[0])
            top = pts[x + 1][1] + 1
            g.rect(x, top, gw + 2, 7, colors[n % 3])
            g.set(x + (gw + 2) // 2, top + 7, colors[n % 3])        # pennant tip
            for r, row in enumerate(glyph):
                for c, bit in enumerate(row):
                    if bit == "1":
                        g.set(x + 1 + c, top + 1 + r, GOLD)
        rnd = random.Random(9)
        first, last = items[0][1], items[-1][1] + len(GLYPHS[items[-1][0]][0]) + 2
        for _ in range(26):                               # gold and silver confetti along the string
            cx = rnd.choice(list(range(2, max(3, first - 3))) + list(range(last + 3, w - 2)))
            g.set(cx, pts[cx][1] + rnd.randrange(1, 5), rnd.choice(CONFETTI))
        for cx in (4, w - 5):                              # a golden star at each end
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                g.set(cx + dx, pts[cx][1] + 3 + dy, GOLD)
        return Layers(width=w, height=10, scale=5, body=g.paths(), css=SELF_CSS,
                      label="Happy New Year %d bunting" % self.year)


DECOR = NewYear()
