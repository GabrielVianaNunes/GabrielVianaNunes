"""Birthday (28 Dec): a party in the western town, with a touch of Christmas.

Balloons tied to presents, a birthday cake with flickering candles, confetti, a paper crown for the
cowboy and a little party hat for the horse, HAPPY BIRTHDAY spelled on the bunting that replaces the
divider, plus the Christmas touch: a tree, presents, snow on the ground and holly.

Privacy: the decoration only ever shows the greeting, never a year or an age.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402
from .christmas import GOLD, GREEN, DARK_GREEN, RED, SNOW, gift, snow_ground, tree  # noqa: E402

PINK = "#e84a8a"
TEAL = "#2ec4b6"
PURPLE = "#8e5bc0"
ORANGE = "#f28a1f"
BLUE = "#4a8fe7"
YELLOW = "#f7d154"
CONFETTI = [PINK, TEAL, PURPLE, ORANGE, BLUE, YELLOW, RED]
FLAGS = [PINK, TEAL, PURPLE, ORANGE, BLUE]

FONT3 = {
    "H": ("101", "101", "111", "101", "101"),
    "A": ("010", "101", "111", "101", "101"),
    "P": ("110", "101", "110", "100", "100"),
    "Y": ("101", "101", "010", "010", "010"),
    "B": ("110", "101", "110", "101", "110"),
    "I": ("111", "010", "010", "010", "111"),
    "R": ("110", "101", "110", "101", "101"),
    "T": ("111", "010", "010", "010", "010"),
    "D": ("110", "101", "101", "101", "110"),
}

BALLOON = (".bbb.", "bbbbb", "bbbbb", "bbbbb", ".bbb.", "..b..")
CAKE = ("..c.c.c..", "..w.w.w..", "..w.w.w..", ".ppppppp.", ".pwpwpwp.", "kkkkkkkkk", "kskykskyk", "eeeeeeeee")
CAKE_COL = {"c": "#ffe29a", "w": "#f4f8ff", "p": "#f7a8c4", "k": "#7a4a22", "s": PINK, "y": YELLOW, "e": "#e8e0d0"}


def sprite(rows, colors, x, y_bottom):
    g = Grid()
    top = y_bottom - len(rows) + 1
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                g.set(x + c, top + r, colors[ch])
    return g


def balloon(x, y, color, string_to=None):
    """A balloon whose top left corner is at (x, y), with a string down to string_to (or none)."""
    g = sprite(BALLOON, {"b": color}, x, y + len(BALLOON) - 1)
    g.set(x + 1, y + 1, "#ffffff")                          # a little shine
    if string_to is not None:
        for yy in range(y + len(BALLOON), string_to):
            g.set(x + 2, yy, "#d9d2e6")
    return g


def balloon_group(spec, duration=5):
    """spec: list of (x, y, color, string_to, delay). Each balloon sways up and down on its own rhythm."""
    out = []
    for x, y, color, string_to, delay in spec:
        out.append('<g class="bln" style="animation-duration:%ds;animation-delay:-%ds">%s</g>'
                   % (duration, delay, balloon(x, y, color, string_to).paths()))
    return "".join(out)


def cake(x, y_bottom):
    """The cake, and its candle flames as separate SVG so they can flicker."""
    body = sprite(CAKE, CAKE_COL, x, y_bottom)
    top = y_bottom - len(CAKE) + 1
    flames = Grid()
    for cx in (2, 4, 6):
        flames.set(x + cx, top, "#ff9a2e")
    return body.paths() + '<g class="tw1">%s</g>' % flames.paths()


def confetti_layer(seed, n, height, duration, delay=0, width=200, colors=None):
    """Colored confetti falling; two stacked copies so the loop has no gap."""
    rnd = random.Random(seed)
    g = Grid()
    palette = colors or CONFETTI
    for _ in range(n):
        g.set(rnd.randrange(1, width - 1), rnd.randrange(0, height), rnd.choice(palette))
    return ('<g class="cf%d" style="animation-duration:%ds;animation-delay:-%ds">%s'
            '<g transform="translate(0 -%d)">%s</g></g>' % (height, duration, delay, g.paths(), height, g.paths()))


def confetti_css(height):
    return ".cf%d{animation:cffall%d 9s linear infinite}@keyframes cffall%d{from{transform:translateY(0)}to{transform:translateY(%dpx)}}" % (height, height, height, height)


def crown_and_horse_hat():
    """The rider's paper crown REPLACES the cowboy hat (it covers the hat's pixels exactly and never goes above
    row -23), and the horse gets a small party hat. Rider coordinates."""
    crown = Grid()
    crown.rect(4, -20, 7, 1, GOLD)
    crown.rect(5, -21, 5, 1, GOLD)
    crown.rect(5, -22, 5, 1, GOLD)
    for x in (5, 7, 9):                              # the points of the crown
        crown.set(x, -23, GOLD)
    crown.set(7, -21, RED)                           # jewels
    crown.set(5, -21, PINK)
    crown.set(9, -21, TEAL)
    horse = Grid()
    horse.rect(15, -15, 2, 1, PINK)
    horse.set(16, -16, YELLOW)
    horse.set(16, -17, ORANGE)
    return crown, horse


def rider_extra():
    crown, horse = crown_and_horse_hat()
    return crown.paths() + horse.paths()


def holly(x, y, flip=1):
    g = Grid()
    for dx, dy in ((0, 1), (1, 0), (2, 1), (3, 0), (4, 1), (1, 2), (3, 2)):
        g.set(x + flip * dx, y + dy, GREEN)
    for dx, dy in ((2, 2), (2, 3), (3, 3)):
        g.set(x + flip * dx, y + dy, RED)
    return g


def party_portrait_hat(r, p, cx):
    """Replaces the cowboy hat in the poster portrait with a striped party hat and a gold pompom."""
    r(cx - 8, 15, 16, 3, "#2a1a10")                  # hair
    colors = [PINK, BLUE, YELLOW, TEAL]
    for y in range(3, 15):
        half = (y - 2) // 2 + 1
        c = colors[(y // 2) % 4]
        r(cx - half, y, half * 2, 1, c)
    r(cx - 8, 14, 16, 2, PINK)                       # brim of the cone
    r(cx - 8, 15, 16, 1, "#b8326a")
    r(cx - 2, 0, 4, 3, GOLD)                         # pompom
    r(cx - 1, 0, 2, 1, "#fff3d6")


# balloons in the free left margin of the poster, clear of the text that starts at x 9 (balloon is 5 wide)
POSTER_BALLOONS = [(2, 104, PINK, 152, 0), (3, 113, TEAL, 152, 2), (2, 122, YELLOW, 152, 4)]


class Birthday(Decor):
    status = "approved"
    id = "birthday"
    name = "Birthday"

    def banner(self):
        left_balloons = balloon_group([(18, 31, PINK, 52, 0), (24, 34, TEAL, 52, 2), (30, 30, YELLOW, 52, 4)], 5)
        right_balloons = balloon_group([(148, 30, PURPLE, 52, 1), (154, 33, ORANGE, 52, 3), (160, 30, BLUE, 52, 5),
                                        (166, 34, PINK, 52, 2)], 6)
        ground = (snow_ground(200, 5, 51) + tree(46, 58)                           # the touch of Christmas
                  + gift(20, 58, PINK, GOLD) + gift(26, 58, TEAL, "#ffffff") + gift(31, 58, PURPLE, YELLOW)
                  + gift(150, 58, ORANGE, "#ffffff") + gift(156, 58, BLUE, GOLD) + gift(162, 58, RED, GOLD)
                  + cake(84, 58)
                  + left_balloons + right_balloons)
        front = confetti_layer(21, 40, 60, 11) + confetti_layer(22, 26, 60, 8, 3)
        css = CSS + confetti_css(60)
        return Layers(ground=ground, front=front, rider_extra=rider_extra(), css=css,
                      label="Birthday decoration: balloons, a cake, confetti and presents")

    def footer(self):
        balloons = balloon_group([(150, 9, PINK, 24, 0), (156, 12, TEAL, 24, 2), (162, 8, YELLOW, 24, 4)], 5)
        ground = (snow_ground(200, 9, 22) + tree(22, 27) + gift(34, 27, PINK, GOLD) + gift(40, 28, TEAL, "#ffffff")
                  + cake(168, 28) + balloons)
        front = confetti_layer(23, 16, 30, 9)
        return Layers(text="HAPPY BIRTHDAY", ground=ground, front=front, rider_extra=rider_extra(), rider_dy=2,
                      css=CSS + confetti_css(30))

    def poster(self):
        rnd = random.Random(31)
        allowed = [(2, 12, 3, 150), (108, 118, 34, 150), (12, 29, 36, 96), (90, 108, 36, 96), (12, 108, 94, 100)]

        def draw(g):
            for _ in range(48):
                x0, x1, y0, y1 = rnd.choice(allowed)
                g.set(rnd.randrange(x0, x1), rnd.randrange(y0, y1), rnd.choice(CONFETTI))
            g.px.update(holly(3, 3, 1).px)                      # the touch of Christmas
            g.px.update(holly(116, 3, -1).px)

        balloons = balloon_group(POSTER_BALLOONS, 5)
        return Layers(draw=draw, headwear=party_portrait_hat, front=balloons, css=SELF_CSS,
                      label="Birthday balloons and a party hat on the portrait")

    def strip(self):
        """HAPPY BIRTHDAY on bunting that replaces the divider, exactly its size (160 by 10)."""
        g = Grid()
        w = 160
        pts = []
        for x in range(w):
            y = int(round(1.5 * math.sin(math.pi * x / (w - 1))))
            g.set(x, y, "#3b2414")
            pts.append((x, y))
        text = "HAPPY BIRTHDAY"
        letters = [ch for ch in text if ch != " "]
        gap = 4
        total = len(letters) * 6 + gap
        x0 = (w - total) // 2
        x = x0
        n = 0
        for ch in text:
            if ch == " ":
                x += gap
                continue
            top = pts[x + 2][1] + 1
            g.rect(x, top, 5, 7, FLAGS[n % 5])
            g.set(x + 2, top + 7, FLAGS[n % 5])                  # pennant tip
            for r, row in enumerate(FONT3[ch]):
                for c, bit in enumerate(row):
                    if bit == "1":
                        g.set(x + 1 + c, top + 1 + r, "#ffffff")
            x += 6
            n += 1
        rnd = random.Random(8)
        for _ in range(26):                                      # confetti along the string, away from the letters
            cx = rnd.choice(list(range(2, x0 - 3)) + list(range(x0 + total + 3, w - 2)))
            g.set(cx, pts[cx][1] + rnd.randrange(1, 5), rnd.choice(CONFETTI))
        g.px.update(holly(3, pts[3][1] + 1, 1).px)               # holly at both ends: the touch of Christmas
        g.px.update(holly(w - 4, pts[w - 4][1] + 1, -1).px)
        return Layers(width=w, height=10, scale=5, body=g.paths(), css=SELF_CSS,
                      label="Happy birthday bunting")


CSS = """
.bln{animation:bln 5s ease-in-out infinite}
.tw1{animation:tw 1.4s steps(1) infinite}
@keyframes bln{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}
@keyframes tw{0%{opacity:1}50%{opacity:.2}}
"""
SELF_CSS = CSS + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n"

DECOR = Birthday()
