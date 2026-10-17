"""Christmas: a snowy western town at dusk. Falling snow, snow on the mesas, roofs and ground, Christmas
trees with twinkling ornaments and presents, a string of lights, a cowboy in a Santa cap with jingling
bells on the horse, holly on the poster and a pine garland as the divider."""
import math
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402

SNOW = "#f4f8ff"
SNOW_SHADE = "#dfe8f5"
RED = "#c8312b"
GOLD = "#f2c14e"
BLUE = "#5aa9e6"
GREEN = "#2f6b3f"
DARK_GREEN = "#1f4d2c"
TRUNK = "#6b4423"
BULBS = [RED, GOLD, BLUE, "#7ed08a"]

TREE = ("....y....", "...ggg...", "..ggggg..", "...ggg...", "..ggggg..", ".ggggggg.",
        "..ggggg..", ".ggggggg.", "ggggggggg", "....t....", "....t....")
TREE_COL = {"y": GOLD, "g": GREEN, "d": DARK_GREEN, "t": TRUNK}
ORNAMENTS = ((3, 5, RED), (5, 7, GOLD), (2, 8, BLUE), (6, 8, RED), (4, 3, GOLD), (5, 4, BLUE))
GIFT = ("rrrr", "rwrr", "wwww", "rwrr")


def sprite(rows, colors, x, y_bottom):
    g = Grid()
    top = y_bottom - len(rows) + 1
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                g.set(x + c, top + r, colors[ch])
    return g


def tree(x, y_bottom):
    """A tree and its twinkling ornaments as SVG."""
    body = sprite(TREE, TREE_COL, x, y_bottom)
    top = y_bottom - len(TREE) + 1
    snow = Grid()
    for cx, cy in ((3, 2), (6, 3), (2, 5), (7, 5), (1, 8)):       # a little snow on the branches
        snow.set(x + cx, top + cy, SNOW)
    lights = []
    for i, (cx, cy, color) in enumerate(ORNAMENTS):
        g = Grid()
        g.set(x + cx, top + cy, color)
        lights.append('<g class="tw%d">%s</g>' % (1 + i % 2, g.paths()))
    return body.paths() + snow.paths() + "".join(lights)


def gift(x, y_bottom, box, ribbon):
    colors = {"r": box, "w": ribbon}
    return sprite(GIFT, colors, x, y_bottom).paths()


def snow_layer(seed, n, height, duration, delay=0, width=200):
    """Falling snow. Two copies stacked one above the other so the loop has no gap."""
    rnd = random.Random(seed)
    g = Grid()
    for _ in range(n):
        g.set(rnd.randrange(1, width - 1), rnd.randrange(0, height), SNOW)
    return ('<g class="snow%d" style="animation-duration:%ds;animation-delay:-%ds">%s'
            '<g transform="translate(0 -%d)">%s</g></g>' % (height, duration, delay, g.paths(), height, g.paths()))


def snow_css(height):
    return ".snow%d{animation:snowfall%d 10s linear infinite}@keyframes snowfall%d{from{transform:translateY(0)}to{transform:translateY(%dpx)}}" % (height, height, height, height)


def snow_caps(spec):
    g = Grid()
    for x, y, w in spec:
        g.rect(x, y, w, 1, SNOW)
    return g.paths()


def snow_ground(width, seed, y0, rows=2):
    rnd = random.Random(seed)
    g = Grid()
    x = 0
    while x < width:
        w = rnd.randrange(5, 14)
        g.rect(x, y0, w, 1, SNOW)
        if rows > 1:
            g.rect(x + 1, y0 + 1, max(1, w - 2), 1, SNOW_SHADE)
        x += w + rnd.randrange(6, 20)
    return g.paths()


def light_string(width, y0=0, sag=3, step=6):
    """A string of bulbs along the top edge: the wire, then bulbs that twinkle in two groups."""
    wire, bulbs = Grid(), ["", ""]
    for x in range(width):
        y = y0 + int(round(sag * math.sin(math.pi * (x % 50) / 49.0)))
        wire.set(x, y, "#2a2a30")
    n = 0
    for x in range(3, width - 2, step):
        y = y0 + int(round(sag * math.sin(math.pi * (x % 50) / 49.0)))
        g = Grid()
        g.set(x, y + 1, BULBS[n % 4])
        g.set(x, y + 2, BULBS[n % 4])
        bulbs[n % 2] += g.paths()
        n += 1
    return wire.paths() + '<g class="tw1">%s</g><g class="tw2">%s</g>' % (bulbs[0], bulbs[1])


def santa_cap():
    """The rider's Santa cap, in the rider's own coordinates. It REPLACES the cowboy hat: it covers the
    hat's pixels exactly (crown x5 to 9 on rows -22 and -21, brim x4 to 10 on row -20). The pompom reaches
    row -23, so the footer rider is moved down 2 pixels to keep it inside the picture."""
    cap = Grid()
    cap.rect(4, -20, 8, 1, SNOW)         # white fur band, wider than the head like a real cap
    cap.rect(5, -21, 6, 1, RED)
    cap.rect(5, -22, 5, 1, RED)
    cap.rect(6, -23, 3, 2, SNOW)         # the white pompom on top of the cap, 3 wide and 2 tall
    return cap


def santa_and_bells():
    """The Santa cap and the bells that jingle on the horse."""
    bells = Grid()
    bells.set(11, -9, GOLD)
    bells.set(13, -8, GOLD)
    bells.set(10, -7, GOLD)
    return santa_cap().paths() + '<g class="tw1">%s</g>' % bells.paths()


def portrait_headwear(r, p, cx):
    """Replaces the cowboy hat in the poster portrait with a full Santa cap, hair and a fur band."""
    shade, light = "#a82520", "#e04a43"
    r(cx - 8, 15, 16, 3, "#2a1a10")                    # hair under the cap
    rows = {13: (-7, 6), 12: (-7, 6), 11: (-6, 7), 10: (-5, 8), 9: (-4, 9), 8: (-2, 10), 7: (0, 11),
            6: (3, 12), 5: (7, 13)}
    for y, (a, b) in rows.items():
        r(cx + a, y, b - a + 1, 1, RED)
        if y >= 10:
            r(cx + a, y, 2, 1, light)
            r(cx + b - 1, y, 2, 1, shade)
    r(cx - 9, 14, 18, 3, SNOW)                          # fur band
    r(cx - 9, 16, 18, 1, SNOW_SHADE)
    r(cx + 12, 2, 4, 4, SNOW)                           # pompom
    r(cx + 15, 3, 1, 3, SNOW_SHADE)


def pine_garland_border(w, h):
    """A pine garland running along all four edges of the poster, with ornaments, bows and twinkling lights.
    Returns (static pixels as a Grid, twinkling lights as SVG)."""
    g = Grid()

    def wave(i):
        return int(round(1.2 * math.sin(i * 0.35)))

    def needles(x, y, horizontal, i):
        g.set(x, y, GREEN)
        g.set(x + (0 if horizontal else 1), y + (1 if horizontal else 0), GREEN)
        g.set(x + (0 if horizontal else 2), y + (2 if horizontal else 0), DARK_GREEN)
        if i % 3 == 0:                                   # needles sticking out
            g.set(x + (0 if horizontal else -1), y + (-1 if horizontal else 0), GREEN)

    inset = 2
    for i in range(w):
        needles(i, inset + wave(i), True, i)                       # top
        needles(i, h - inset - 3 + wave(i), True, i)               # bottom
    for i in range(h):
        needles(inset + wave(i), i, False, i)                      # left
        needles(w - inset - 3 + wave(i), i, False, i)              # right
    # ornaments and lights, spaced along the four edges
    colors = [RED, GOLD, BLUE]
    for k, i in enumerate(range(10, w - 10, 13)):
        for (x, y) in ((i, inset + wave(i) + 1), (i, h - inset - 2 + wave(i))):
            g.rect(x, y, 2, 2, colors[k % 3])
    for k, i in enumerate(range(12, h - 12, 13)):
        for (x, y) in ((inset + wave(i) + 1, i), (w - inset - 2 + wave(i), i)):
            g.rect(x, y, 2, 2, colors[(k + 1) % 3])
    for x in range(6, w - 6, 5):                                    # snow on the top band
        g.set(x, inset + wave(x) - 1, SNOW)
    # twinkling lights as separate groups
    tw = [Grid(), Grid()]
    for k, i in enumerate(range(16, w - 14, 13)):
        tw[k % 2].set(i, inset + wave(i) + 3, BULBS[k % 4])
        tw[k % 2].set(i, h - inset - 3 + wave(i) - 1, BULBS[(k + 2) % 4])
    for k, i in enumerate(range(18, h - 14, 13)):
        tw[k % 2].set(inset + wave(i) + 3, i, BULBS[(k + 1) % 4])
        tw[k % 2].set(w - inset - 3 + wave(i) - 1, i, BULBS[(k + 3) % 4])
    for x, y in ((1, 1), (w - 9, 1), (1, h - 7), (w - 9, h - 7)):   # red bows in the corners
        g.rect(x, y + 1, 3, 3, RED)
        g.rect(x + 5, y + 1, 3, 3, RED)
        g.rect(x + 3, y + 1, 2, 3, GOLD)
        g.rect(x + 2, y + 4, 1, 2, RED)
        g.rect(x + 5, y + 4, 1, 2, RED)
    svg = '<g class="tw1">%s</g><g class="tw2">%s</g>' % (tw[0].paths(), tw[1].paths())
    return g, svg


CSS = """
.tw1{animation:tw 1.4s steps(1) infinite}
.tw2{animation:tw 1.4s steps(1) infinite;animation-delay:.7s}
@keyframes tw{0%{opacity:1}50%{opacity:.15}}
"""
SELF_CSS = CSS + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n"


class Christmas(Decor):
    id = "christmas"
    name = "Christmas"

    def banner(self):
        # the horizon town: rooflines of the buildings, and the mesas, outside the town itself
        caps = [(97, 42, 4), (103, 46, 5), (110, 41, 5), (119, 42, 4), (125, 46, 6)]
        mesas = [(0, 22, 43), (22, 27, 41), (27, 48, 44), (60, 85, 42), (85, 92, 44), (130, 150, 42),
                 (150, 175, 44), (175, 200, 43), (0, 14, 47), (14, 20, 45), (20, 36, 47), (70, 78, 46)]
        for x0, x1, top in mesas:
            caps.append((x0, top, x1 - x0))
        roof_lights = Grid()
        for i, (x, y) in enumerate([(97, 43), (99, 43), (103, 47), (106, 47), (110, 42), (113, 42), (125, 47), (128, 47)]):
            roof_lights.set(x, y, BULBS[i % 4])
        ground = (snow_caps(caps) + snow_ground(200, 5, 51)
                  + tree(76, 58) + tree(38, 58)
                  + gift(88, 58, RED, GOLD) + gift(93, 58, "#2f8f55", RED)
                  + gift(28, 58, BLUE, SNOW)
                  + '<g class="tw1">%s</g>' % roof_lights.paths())
        front = (snow_layer(3, 45, 60, 11) + snow_layer(4, 30, 60, 8, 3)
                 + light_string(200))
        return Layers(ground=ground, front=front, rider_extra=santa_and_bells(),
                      css=CSS + snow_css(60),
                      label="Christmas decoration: falling snow, trees, presents, lights and a cowboy in a Santa cap")

    def footer(self):
        # the string of lights is drawn behind the rider, so it never covers the cap
        ground = (snow_ground(200, 9, 22) + tree(24, 27) + gift(36, 27, RED, GOLD) + gift(160, 28, "#2f8f55", RED)
                  + light_string(200, 0, 2, 8))
        front = snow_layer(6, 18, 30, 9)
        # the rider bobs 1 pixel up on every step, so it is moved 2 pixels down: the pompom on top of the cap
        # (row -23) then stays inside the 30 pixel footer in both frames of the animation
        return Layers(text="MERRY TRAILS", ground=ground, front=front, rider_extra=santa_and_bells(),
                      rider_dy=2, css=CSS + snow_css(30))

    POSTER_W, POSTER_H = 120, 156

    def poster(self):
        garland, lights = pine_garland_border(self.POSTER_W, self.POSTER_H)

        def draw(g):
            g.px.update(garland.px)

        return Layers(draw=draw, headwear=portrait_headwear, front=lights, css=SELF_CSS,
                      label="Christmas pine garland around the poster and a Santa cap on the portrait")

    def strip(self):
        """Replaces the divider above the 3D graph: a pine garland, exactly the divider's size (160 by 10)."""
        g = Grid()
        w = 160
        pts = []
        for x in range(w):
            y = 1 + int(round(2 * math.sin(math.pi * x / (w - 1))))
            g.set(x, y, GREEN)
            g.set(x, y + 1, DARK_GREEN)
            if x % 3 == 0:
                g.set(x, y + 2, GREEN)               # needles
            if x % 4 == 1:
                g.set(x, y - 1, GREEN)
            pts.append((x, y))
        twinkle = ["", ""]
        for i, x in enumerate(range(10, w - 6, 12)):
            y = pts[x][1] + 2
            color = [RED, GOLD, BLUE][i % 3]
            g.rect(x, y, 2, 2, color)                # ornaments
            b = Grid()
            b.set(x + 6, pts[x + 6][1] + 3, BULBS[i % 4])
            twinkle[i % 2] += b.paths()
        for x in range(4, w - 2, 7):
            g.set(x, pts[x][1] - 1, SNOW)            # snow on the garland
        for x0, d in ((0, 1), (w - 6, -1)):          # red bows at both ends
            g.rect(x0, 0, 6, 3, RED)
            g.rect(x0 + 2, 1, 2, 1, GOLD)
        body = g.paths() + '<g class="tw1">%s</g><g class="tw2">%s</g>' % (twinkle[0], twinkle[1])
        return Layers(width=w, height=10, scale=5, body=body, css=SELF_CSS,
                      label="Christmas pine garland with ornaments and lights")


DECOR = Christmas()
