"""National Day of the Cowboy: a rodeo night in the western town.

Spotlights sweeping the sky, red white and blue bunting between two posts, a bull behind a rodeo fence, barrel racing
barrels, a hay bale, a gold trophy, lucky horseshoes, falling stars, a gold band on the cowboy's hat and a lasso that
spins in his hand, a gold star and a blue ribbon rosette on the poster portrait, HAPPY COWBOY DAY on the bunting that
replaces the divider. The cowboy keeps his hat: it is his day.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402
from .kit import COMMON_CSS, REDUCED, bunting, confetti_layer, fall_css, outlined, scatter_on_string, sprite  # noqa: E402

RED = "#c8312b"
BLUE = "#2f5fc4"
SNOW = "#f4f8ff"
GOLD = "#f2c14e"
DEEP_GOLD = "#c9961e"
WOOD = "#8a5a2c"
DARK_WOOD = "#5a3a1c"
BROWN = "#4a2d14"
HAY = "#e6c65a"
PATRIOT = [RED, SNOW, BLUE]
CONFETTI = [RED, SNOW, BLUE, GOLD]

BULL = ("h............", "hb.......bb..", "bbbbbbbbbbbb.", "bbbbbbbbbbbbb", "bbbbbbbbbbbbb", ".bbbbbbbbbbb.", ".b.b.....b.b.", ".b.b.....b.b.")
BARREL = ("bbbbb", "iiiii", "bbbbb", "bbbbb", "iiiii", "bbbbb")
HORSESHOE = ("gg.gg", "g...g", "g...g", "gg.gg", ".ggg.")
TROPHY = ("g.ggg.g", "ggggggg", ".ggggg.", "..ggg..", "...g...", "..ggg..", ".bbbbb.")
STAR = ("..g..", ".ggg.", "ggggg", ".ggg.", ".g.g.")
STAR_X_MIRROR = 67      # the portrait is centered on x 59.5, so the mirror of the star (x 52) is 67
ROSETTE_Y = 80
HAYBALE = ("hhhhhhhh", "hdhdhdhd", "hhhhhhhh", "hdhdhdhd")


def barrel(x, yb):
    return outlined(sprite(BARREL, {"b": "#b8452e", "i": "#d0d4de"}, x, yb))


def horseshoe(x, yb):
    return outlined(sprite(HORSESHOE, {"g": GOLD}, x, yb))


def gold_star(x, yb):
    return outlined(sprite(STAR, {"g": GOLD}, x, yb))


def beam(x0, base_y, top_y, spread, sway, duration, delay=0, opacity=0.17):
    """A spotlight: a pale triangle from the ground up into the sky, swaying around its base."""
    pts = "%d,%d %d,%d %d,%d %d,%d" % (x0 - 1, base_y, x0 + 1, base_y, x0 + spread, top_y, x0 - spread, top_y)
    return ('<g class="sweep" style="transform-origin:%dpx %dpx;animation-duration:%ds;animation-delay:-%ds;'
            '--sw:%ddeg"><polygon points="%s" fill="#fff6c8" opacity="%s"/></g>'
            % (x0, base_y, duration, delay, sway, pts, opacity))


def bunting_between_posts(x0, x1, y0, sag, flags=22):
    """Red, white and blue pennants on a sagging string between two wooden posts. Returns SVG."""
    g = Grid()
    for x in (x0, x1):
        g.rect(x, y0, 2, 51 - y0, WOOD)
        g.rect(x, y0, 1, 51 - y0, "#a6733a")
    pts = []
    for x in range(x0 + 2, x1):
        y = y0 + int(round(sag * math.sin(math.pi * (x - x0 - 2) / (x1 - x0 - 3))))
        g.set(x, y, "#3b2414")
        pts.append((x, y))
    step = (len(pts) - 6) / float(flags)
    for i in range(flags):
        x, y = pts[int(3 + i * step)]
        color = PATRIOT[i % 3]
        g.rect(x, y + 1, 3, 2, color)
        g.set(x + 1, y + 3, color)
    return g.paths()


def rodeo_fence(x0, x1, ybase):
    g = Grid()
    for x in range(x0, x1, 8):
        g.rect(x, ybase - 7, 2, 8, DARK_WOOD)
    g.rect(x0, ybase - 6, x1 - x0 + 2, 1, WOOD)
    g.rect(x0, ybase - 3, x1 - x0 + 2, 1, WOOD)
    return g.paths()


def bull(x, yb):
    g = sprite(BULL, {"h": SNOW, "b": BROWN}, x, yb)
    g.set(x + 1, yb - 6, RED)                        # an angry red eye
    return outlined(g, "#e8d8b0")                    # a pale outline: the bull is dark like the ground


def rope_loop():
    """The cowboy's lasso: a rope from his hand to a loop that spins (it only ever gets flatter, never taller, so it
    stays inside the picture in the footer). Rider coordinates."""
    rope, loop = Grid(), Grid()
    for x, y in ((12, -16), (13, -17), (13, -18), (14, -19)):
        rope.set(x, y, "#e6d3a0")
    for deg in range(0, 360, 24):
        a = math.radians(deg)
        loop.set(16 + int(round(4 * math.cos(a))), -21 + int(round(1.6 * math.sin(a))), "#e6d3a0")
    return rope, loop


def gold_band():
    """A gold band on the hat: row -21 of the crown, x5 to 9. The hat itself stays the cowboy's own."""
    g = Grid()
    g.rect(5, -21, 5, 1, GOLD)
    g.set(7, -21, DEEP_GOLD)
    return g


def rider_extra():
    rope, loop = rope_loop()
    return gold_band().paths() + rope.paths() + '<g class="spinloop">%s</g>' % loop.paths()


def star_and_rosette(g):
    """On the poster portrait: a gold sheriff star on one side of the chest and a blue ribbon rosette on the other,
    in absolute poster pixels. The star is on the left of the neckerchief and the rosette mirrors it on the right."""
    g.px.update(gold_star(50, 85).px)                # centered on x 52
    cx, cy = STAR_X_MIRROR, ROSETTE_Y
    for dx, dy in ((-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (-3, -2), (3, -2), (-3, -1), (3, -1), (-3, 0), (3, 0),
                   (-3, 1), (3, 1), (-2, 2), (-1, 3), (0, 3), (1, 3), (2, 2), (-2, -2), (2, -2), (-2, 2)):
        g.set(cx + dx, cy + dy, "#3a6ad8")
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            g.set(cx + dx, cy + dy, "#3a6ad8")
    g.rect(cx - 1, cy - 1, 3, 3, GOLD)               # the gold center
    for dy in range(4, 10):                           # the two ribbon tails
        g.set(cx - 2, cy + dy, RED)
        g.set(cx - 1, cy + dy, RED)
        g.set(cx + 1, cy + dy, SNOW)
        g.set(cx + 2, cy + dy, SNOW)


def poster_bunting(g, x0=10, x1=110, y0=2):
    for x in range(x0, x1):
        g.set(x, y0, "#3b2414")
    for i, x in enumerate(range(x0 + 3, x1 - 4, 8)):
        color = PATRIOT[i % 3]
        g.rect(x, y0 + 1, 4, 2, color)
        g.set(x + 1, y0 + 3, color)
        g.set(x + 2, y0 + 3, color)


CSS = COMMON_CSS + """
.sweep{animation:sweep 5s ease-in-out infinite alternate}
.spinloop{transform-box:fill-box;transform-origin:center;animation:spin .5s steps(1) infinite}
.bull{animation:bullb 2s steps(1) infinite}
@keyframes sweep{from{transform:rotate(calc(var(--sw) * -1))}to{transform:rotate(var(--sw))}}
@keyframes spin{0%{transform:scaleY(1)}50%{transform:scaleY(.4)}}
@keyframes bullb{0%,100%{transform:translateY(0)}50%{transform:translateY(-1px)}}
"""
SELF_CSS = COMMON_CSS + REDUCED


class CowboyDay(Decor):
    id = "cowboy-day"
    name = "National Day of the Cowboy"

    def banner(self):
        beams = beam(36, 51, 0, 18, 16, 6) + beam(166, 51, 0, 18, 16, 7, 3) + beam(100, 51, 6, 14, 12, 8, 5, 0.12)
        post_bunting = bunting_between_posts(3, 196, 31, 5)
        trophy = outlined(sprite(TROPHY, {"g": GOLD, "b": DARK_WOOD}, 108, 58))
        bale = outlined(sprite(HAYBALE, {"h": HAY, "d": "#b89a3a"}, 50, 58))
        barrels = Grid()
        for x in (68, 76, 84):
            barrels.px.update(barrel(x, 58).px)
        shoes = Grid()
        for x, yb in ((20, 57), (130, 58), (148, 57)):
            shoes.px.update(horseshoe(x, yb).px)
        ground = (rodeo_fence(150, 198, 52) + '<g class="bull">%s</g>' % bull(170, 58).paths() + post_bunting
                  + bale.paths() + barrels.paths() + trophy.paths()
                  + '<g class="tw1">%s</g>' % shoes.paths())
        front = confetti_layer(61, 28, 60, 12, CONFETTI, name="st") + confetti_layer(62, 18, 60, 8, CONFETTI, 3, name="st")
        return Layers(ground=ground, sky=beams, front=front, rider_extra=rider_extra(),
                      css=CSS + fall_css(60, "st"),
                      label="National Day of the Cowboy decoration: spotlights, rodeo bunting, a bull, barrels and a trophy")

    def footer(self):
        beams = beam(40, 22, 0, 9, 14, 6, 0, 0.15) + beam(160, 22, 0, 9, 14, 7, 3, 0.15)
        flags = Grid()
        for x in range(0, 200):
            y = int(round(1.5 * math.sin(math.pi * (x % 40) / 39.0)))
            flags.set(x, y, "#3b2414")
        for i, x in enumerate(range(3, 197, 7)):
            y = int(round(1.5 * math.sin(math.pi * (x % 40) / 39.0)))
            color = PATRIOT[i % 3]
            flags.rect(x, y + 1, 3, 2, color)
        barrels = Grid()
        for x in (20, 27):
            barrels.px.update(barrel(x, 28).px)
        shoes = Grid()
        shoes.px.update(horseshoe(150, 28).px)
        shoes.px.update(horseshoe(176, 28).px)
        ground = (barrels.paths() + outlined(sprite(HAYBALE, {"h": HAY, "d": "#b89a3a"}, 36, 28)).paths()
                  + '<g class="tw1">%s</g>' % shoes.paths())
        sky = beams
        front = confetti_layer(63, 12, 30, 9, CONFETTI, name="st")
        return Layers(text="HAPPY COWBOY DAY", ground=ground + flags.paths(), sky=sky, front=front, rider_extra=rider_extra(),
                      rider_dy=2, css=CSS + fall_css(30, "st"))

    def poster(self):
        rnd = random.Random(81)
        allowed = [(2, 12, 12, 100), (108, 118, 36, 150), (12, 29, 36, 96), (90, 108, 36, 96)]

        def draw(g):
            star_and_rosette(g)
            poster_bunting(g)
            for x, yb in ((3, 150), (113, 150)):                       # lucky horseshoes in the bottom corners
                g.px.update(horseshoe(x, yb).px)
            for _ in range(24):                                       # stars and confetti in the free spaces
                x0, x1, y0, y1 = rnd.choice(allowed)
                g.set(rnd.randrange(x0, x1), rnd.randrange(y0, y1), rnd.choice(CONFETTI))

        return Layers(draw=draw, css=SELF_CSS)

    def strip(self):
        """HAPPY COWBOY DAY on red, white and blue bunting that replaces the divider, exactly its size (160 by 10)."""
        g, first, last, pts = bunting("HAPPY COWBOY DAY", [RED, SNOW, BLUE], [SNOW, BLUE, SNOW])
        rnd = random.Random(14)
        scatter_on_string(g, pts, rnd, first, last, [GOLD, RED, BLUE, SNOW], 24)
        for cx in (5, 154):                                         # a golden star at each end
            g.px.update(gold_star(cx - 2, pts[cx][1] + 7).px)
        return Layers(width=160, height=10, scale=5, body=g.paths(), css=SELF_CSS,
                      label="Happy Cowboy Day bunting in red white and blue")


DECOR = CowboyDay()
