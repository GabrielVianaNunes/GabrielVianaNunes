"""Easter: spring comes to the western town. Pastel mood, flowers and grass, painted eggs hidden around, a basket,
chicks, a bunny hopping across, butterflies, falling petals, an Easter bonnet for the cowboy and a small flower
garland on the horse's neck (its ears stay as they are), and HAPPY EASTER on pastel bunting that replaces the divider."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402
from .kit import COMMON_CSS, REDUCED, bunting, confetti_layer, fall_css, scatter_on_string, sprite  # noqa: E402

PINK = "#f7a8c4"
BLUE = "#9cc8f0"
YELLOW = "#ffe58a"
LILAC = "#c9a8f0"
MINT = "#a8e6c4"
WHITE = "#ffffff"
GREEN = "#5fae6a"
DKGREEN = "#3b8a4e"
ORANGE = "#f28a2e"
PLUM = "#5a3a6a"
PASTELS = [PINK, BLUE, YELLOW, LILAC, MINT]

EGG = (".bb.", "bbbb", "bbbb", "bbbb", ".bb.")
CHICK = (".yy.", "ykyo", "yyy.", ".o.o")
BUNNY = ("..w.w..", "..p.p..", "..w.w..", ".wwwww.", ".wkwkw.", ".wwnww.", "wwwwwww", "ww...ww")
BASKET = ("..p.l.y..", ".wwwwwww.", "wbwbwbwbw", "bwbwbwbwb", ".wwwwwww.")
BASKET_COL = {"p": PINK, "l": BLUE, "y": YELLOW, "w": "#c98b4a", "b": "#a6692f"}


def flower(x, y, color):
    """A small flower, top left corner at (x, y): petals, a yellow heart, a stem and a leaf."""
    g = Grid()
    for dx, dy in ((1, 0), (0, 1), (2, 1), (1, 2)):
        g.set(x + dx, y + dy, color)
    g.set(x + 1, y + 1, "#ffd23f")
    g.set(x + 1, y + 3, GREEN)
    g.set(x + 1, y + 4, GREEN)
    g.set(x + 2, y + 4, DKGREEN)
    return g


def egg(x, y_bottom, base, accent, style):
    g = sprite(EGG, {"b": base}, x, y_bottom)
    top = y_bottom - 4
    if style == "stripe":
        for c in range(4):
            g.set(x + c, top + 2, accent)
    elif style == "dots":
        g.set(x + 1, top + 1, accent)
        g.set(x + 2, top + 3, accent)
    else:                                              # zigzag
        for c, r in ((0, 2), (1, 3), (2, 2), (3, 3)):
            g.set(x + c, top + r, accent)
    if style != "dots":
        g.set(x + 1, top + 1, WHITE)                    # a little shine
    return g


def chick(x, y_bottom):
    return sprite(CHICK, {"y": "#ffe14d", "k": "#1a0f1c", "o": ORANGE}, x, y_bottom)


def bunny(x, y_bottom):
    return sprite(BUNNY, {"w": WHITE, "p": PINK, "k": "#1a0f1c", "n": "#f28ab0"}, x, y_bottom)


def spring_ground(seed, count_flowers, count_tufts, x_range=(0, 200), ybase=(55, 58)):
    rnd = random.Random(seed)
    g = Grid()
    for _ in range(count_tufts):
        x = rnd.randrange(*x_range)
        for dx, dy in ((0, 0), (1, -1), (2, 0)):
            g.set(x + dx, 51 + dy + 1, GREEN)
    for i in range(count_flowers):
        x = rnd.randrange(x_range[0], x_range[1] - 3)
        y = rnd.randrange(*ybase) - 4
        g.px.update(flower(x, y, PASTELS[i % 5]).px)
    return g


def pastel_overlay(width, height, opacity=0.2):
    return '<rect x="0" y="0" width="%d" height="%d" fill="#ffd6e8" opacity="%s"/>' % (width, height, opacity)


def cloud(y, dur, delay):
    g = Grid()
    g.rect(2, 0, 7, 1, WHITE)
    g.rect(0, 1, 13, 1, WHITE)
    g.rect(1, 2, 11, 1, "#f0e8f8")
    return ('<g transform="translate(0 %d)" opacity="0.9"><g class="ecloud" style="animation-duration:%ds;'
            'animation-delay:-%ds">%s</g></g>' % (y, dur, delay, g.paths()))


def butterfly(y, color, dur, delay):
    up, down = Grid(), Grid()
    for x, yy in ((0, 0), (1, 0), (4, 0), (5, 0), (0, 1), (1, 1), (4, 1), (5, 1), (2, 1), (3, 1)):
        up.set(x, yy, color)
    for x, yy in ((1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (4, 2)):
        down.set(x, yy, color)
    up.set(2, 2, "#3b2414")
    up.set(3, 2, "#3b2414")
    return ('<g transform="translate(0 %d)"><g class="bfly" style="animation-duration:%ds;animation-delay:-%ds">'
            '<g class="bw1">%s</g><g class="bw2">%s</g></g></g>' % (y, dur, delay, up.paths(), down.paths()))


def hopping(sprite_grid, name, dur, delay=0):
    return ('<g class="%s" style="animation-duration:%ds;animation-delay:-%ds"><g class="hop">%s</g></g>'
            % (name, dur, delay, sprite_grid.paths()))


def bonnet_and_garland():
    """The Easter bonnet REPLACES the cowboy hat (covers its pixels exactly, never above row -23). The horse keeps
    its own ears and only gets a small flower garland on its neck. Rider coordinates."""
    hat = Grid()
    hat.rect(5, -22, 5, 2, "#ffe9a8")
    hat.rect(4, -20, 7, 1, "#f7d27a")
    hat.rect(5, -21, 5, 1, PINK)                       # the ribbon
    for x, c in ((5, PINK), (7, BLUE), (9, LILAC)):    # flowers on top
        hat.set(x, -23, c)
    garland = Grid()
    for i, (x, y) in enumerate(((12, -12), (13, -11), (14, -10), (13, -9), (12, -8))):
        garland.set(x, y, PASTELS[i % 5])
    return hat, garland


def rider_extra():
    hat, garland = bonnet_and_garland()
    return hat.paths() + garland.paths()


def bonnet_headwear(r, p, cx):
    """Replaces the cowboy hat in the poster portrait with a straw Easter bonnet with a ribbon and flowers."""
    r(cx - 8, 15, 16, 3, "#2a1a10")                    # hair
    r(cx - 7, 5, 14, 9, "#ffe9a8")                      # crown
    r(cx - 7, 5, 3, 9, "#fff3c8")
    r(cx - 7, 11, 14, 2, PINK)                          # ribbon
    r(cx - 13, 14, 26, 2, "#f7d27a")                    # wide brim
    r(cx - 11, 13, 22, 1, "#ffe9a8")
    for dx, c in ((-4, LILAC), (0, BLUE), (4, PINK)):   # flowers on the ribbon
        r(cx + dx - 1, 9, 3, 3, c)
        r(cx + dx, 10, 1, 1, "#ffd23f")
    r(cx + 8, 12, 4, 2, PINK)                           # a bow end


CSS = COMMON_CSS + """
.ecloud{animation:ecloud 90s linear infinite}
.bfly{animation:bfly 28s linear infinite}
.bw1{animation:fa .35s steps(1) infinite}
.bw2{opacity:0;animation:fb .35s steps(1) infinite}
.bunny{animation:brun 18s linear infinite}
.hop{animation:hop .6s steps(1) infinite}
.chick{animation:chk 1.6s steps(1) infinite}
@keyframes ecloud{from{transform:translateX(-14px)}to{transform:translateX(214px)}}
@keyframes bfly{0%{transform:translate(-8px,0)}25%{transform:translate(48px,-4px)}50%{transform:translate(104px,2px)}75%{transform:translate(160px,-3px)}100%{transform:translate(216px,0)}}
@keyframes brun{from{transform:translateX(-10px)}to{transform:translateX(212px)}}
@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes chk{0%,100%{transform:translateY(0)}40%{transform:translateY(-2px)}70%{transform:translateY(0)}}
@keyframes fa{0%{opacity:1}50%{opacity:0}}
@keyframes fb{0%{opacity:0}50%{opacity:1}}
"""
SELF_CSS = COMMON_CSS + REDUCED


class Easter(Decor):
    status = "approved"
    id = "easter"
    name = "Easter"

    def banner(self):
        ground_px = spring_ground(3, 20, 26).paths()
        eggs = Grid()
        spec = [(24, 58, PINK, LILAC, "stripe"), (53, 57, BLUE, YELLOW, "dots"), (70, 58, YELLOW, PINK, "zig"),
                (118, 58, LILAC, MINT, "stripe"), (141, 57, MINT, PINK, "dots"), (164, 58, PINK, BLUE, "zig"),
                (176, 58, BLUE, WHITE, "stripe")]
        for x, yb, base, accent, style in spec:
            eggs.px.update(egg(x, yb, base, accent, style).px)
        basket = sprite(BASKET, BASKET_COL, 36, 58)
        chick_groups = "".join('<g class="chick" style="animation-delay:-%ds">%s</g>' % (d, chick(x, yb).paths())
                               for x, yb, d in ((46, 58, 0), (127, 58, 1), (152, 57, 0), (179, 39, 1)))
        ground = (pastel_overlay(200, 51) + ground_px + eggs.paths() + basket.paths() + chick_groups
                  + hopping(bunny(0, 58), "bunny", 18, 5))
        sky = cloud(8, 90, 10) + cloud(28, 120, 60) + butterfly(30, PINK, 28, 4) + butterfly(38, BLUE, 34, 16)
        front = confetti_layer(51, 22, 60, 12, [PINK, WHITE, "#ffe0ec"], name="pt")
        return Layers(ground=ground, sky=sky, front=front, rider_extra=rider_extra(),
                      css=CSS + fall_css(60, "pt"),
                      label="Easter decoration: spring flowers, painted eggs, chicks, a bunny and butterflies")

    def footer(self):
        eggs = Grid()
        for x, yb, base, accent, style in ((40, 28, PINK, LILAC, "stripe"), (110, 27, BLUE, YELLOW, "dots"),
                                           (150, 28, MINT, PINK, "zig")):
            eggs.px.update(egg(x, yb, base, accent, style).px)
        ground = (pastel_overlay(200, 22, 0.18) + spring_ground(8, 9, 14, ybase=(26, 29)).paths() + eggs.paths()
                  + '<g class="chick">%s</g>' % chick(60, 28).paths() + hopping(bunny(0, 28), "bunny", 20, 8))
        front = confetti_layer(52, 12, 30, 10, [PINK, WHITE, "#ffe0ec"], name="pt")
        return Layers(text="HAPPY EASTER", ground=ground, front=front, rider_extra=rider_extra(), rider_dy=2,
                      css=CSS + fall_css(30, "pt"))

    def poster(self):
        rnd = random.Random(71)
        allowed = [(2, 12, 12, 100), (108, 118, 36, 150), (12, 29, 36, 96), (90, 108, 36, 96), (12, 108, 94, 100)]

        def draw(g):
            for x, y, c in ((2, 2, PINK), (6, 5, BLUE), (110, 2, LILAC), (113, 6, PINK), (2, 146, YELLOW),
                            (6, 144, MINT), (110, 146, PINK), (114, 144, BLUE)):
                g.px.update(flower(x, y - 1, c).px)                        # flowers in the corners
            for i, (x, yb, base, accent, style) in enumerate(((2, 118, PINK, LILAC, "stripe"), (3, 125, BLUE, YELLOW, "dots"),
                                                               (2, 132, MINT, PINK, "zig"))):
                g.px.update(egg(x, yb, base, accent, style).px)           # eggs in the left margin
            g.px.update(chick(82, 98).px)                                  # a chick on the frame's bottom edge
            for _ in range(36):
                x0, x1, y0, y1 = rnd.choice(allowed)
                g.set(rnd.randrange(x0, x1), rnd.randrange(y0, y1), rnd.choice(PASTELS))

        return Layers(draw=draw, headwear=bonnet_headwear, css=SELF_CSS)

    def strip(self):
        """HAPPY EASTER on pastel bunting that replaces the divider, exactly its size (160 by 10)."""
        g, first, last, pts = bunting("HAPPY EASTER", PASTELS, PLUM)
        rnd = random.Random(12)
        scatter_on_string(g, pts, rnd, first, last, PASTELS + [WHITE], 22)
        for cx, c in ((4, PINK), (155, BLUE)):                    # a flower at each end
            g.px.update(flower(cx - 1, pts[cx][1] + 1, c).px)
        for cx, base in ((14, LILAC), (146, MINT)):                        # and an egg on the string
            e = sprite(("bb", "bb", "bb"), {"b": base}, cx, pts[cx][1] + 4)
            g.px.update(e.px)
        return Layers(width=160, height=10, scale=5, body=g.paths(), css=SELF_CSS,
                      label="Happy Easter bunting with pastel flags")


DECOR = Easter()
