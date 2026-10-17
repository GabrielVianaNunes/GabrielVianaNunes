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


def santa_and_bells():
    """Rider coordinates: a red cap with a white band over the hat, and bells that jingle on the horse."""
    cap = Grid()
    cap.rect(5, -22, 5, 1, RED)
    cap.rect(5, -21, 5, 1, SNOW)
    cap.rect(5, -23, 4, 1, RED)
    cap.rect(6, -24, 3, 1, RED)
    cap.rect(7, -25, 2, 1, RED)
    cap.rect(9, -25, 2, 2, SNOW)
    bells = Grid()
    bells.set(11, -9, GOLD)
    bells.set(13, -8, GOLD)
    bells.set(10, -7, GOLD)
    return cap.paths() + '<g class="tw1">%s</g>' % bells.paths()


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
        ground = snow_ground(200, 9, 22) + tree(24, 27) + gift(36, 27, RED, GOLD) + gift(160, 28, "#2f8f55", RED)
        front = snow_layer(6, 18, 30, 9) + light_string(200, 0, 2, 8)
        return Layers(text="MERRY TRAILS", ground=ground, front=front, rider_extra=santa_and_bells(),
                      css=CSS + snow_css(30))

    def poster(self):
        def holly(x, y, flip=1):
            g = Grid()
            for dx, dy in ((0, 1), (1, 0), (2, 1), (3, 0), (4, 1), (1, 2), (3, 2)):
                g.set(x + flip * dx, y + dy, GREEN)
            for dx, dy in ((2, 2), (2, 3), (3, 3)):
                g.set(x + flip * dx, y + dy, RED)
            return g

        def draw(g):
            g.px.update(holly(3, 3, 1).px)
            g.px.update(holly(116, 3, -1).px)
            for x in range(8, 112, 3):                            # snow along the top border
                g.set(x, 2, SNOW)
                g.set(x + 1, 3, SNOW)
            cx, ox, oy = 29, 31, 35                               # a Santa cap on the portrait's hat
            g.rect(ox + cx - 6, oy + 2, 12, 1, RED)
            g.rect(ox + cx - 4, oy + 1, 8, 1, RED)
            g.rect(ox + cx - 2, oy + 0, 4, 1, RED)
            g.rect(ox + cx - 5, oy + 3, 10, 1, SNOW)
            g.rect(ox + cx + 2, oy - 1, 2, 2, SNOW)
        return Layers(draw=draw, css=SELF_CSS)

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
