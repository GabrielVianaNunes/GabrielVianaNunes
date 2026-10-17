"""Halloween: a western ghost town. Orange harvest moon, bats, glowing jack o'lanterns, tombstones,
fog, cobwebs, a hanging spider, and a skeleton cowboy on a horse with glowing eyes."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from build_assets import Grid  # noqa: E402

from .base import Decor, Layers  # noqa: E402

BAT_UP = ("1.....1", "11...11", ".11111.", "..1.1..")
BAT_DOWN = ("..111..", "1111111", "1.111.1", "...1...")
SPIDER = ("1.1.1", ".111.", "1.1.1")
TOMB = ("..gggg..", ".gggggg.", "gggxxggg", "ggxxxxgg", "gggxxggg", "gggxxggg", "gggggggg", "gggggggg")
PUMPKIN = ("...g...", ".hoood.", "hoooood", "hoooood", "hoooood", ".doooo.")
COL = {"o": "#f28a1f", "h": "#ffb347", "d": "#c9610f", "g": "#3b6b47"}
TOMB_COL = {"g": "#8d8da0", "x": "#5a5a6e"}
BAT_COLOR = "#0e0709"
GLOW = "#ffe29a"
WEB = "#d9d2e6"


def sprite(rows, colors, x, y_bottom, k=1):
    """Pixel art from an ascii picture. The bottom row sits on y_bottom, k scales every pixel."""
    g = Grid()
    top = y_bottom - len(rows) * k + 1
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in colors:
                g.rect(x + c * k, top + r * k, k, k, colors[ch])
    return g


def pumpkin(x, y_bottom, k=1):
    """A glowing jack o'lantern: (body, glowing face) as separate drawings so the face can flicker."""
    body = sprite(PUMPKIN, COL, x, y_bottom, k)
    face = Grid()
    top = y_bottom - len(PUMPKIN) * k + 1
    for cx, cy in ((2, 2), (4, 2), (2, 4), (3, 4), (4, 4)):
        face.rect(x + cx * k, top + cy * k, k, k, GLOW)
    return body, face


def pumpkins(spec):
    """spec: list of (x, y_bottom, k, flicker delay). Returns SVG."""
    out = []
    for x, yb, k, delay in spec:
        body, face = pumpkin(x, yb, k)
        out.append(body.paths())
        out.append('<g class="flk" style="animation-delay:%ss">%s</g>' % (delay, face.paths()))
    return "".join(out)


def bat_group(y, duration, delay, scale_x=1):
    up, down = Grid(), Grid()
    for r, row in enumerate(BAT_UP):
        for c, ch in enumerate(row):
            if ch == "1":
                up.set(c, r, BAT_COLOR)
    for r, row in enumerate(BAT_DOWN):
        for c, ch in enumerate(row):
            if ch == "1":
                down.set(c, r, BAT_COLOR)
    return ('<g transform="translate(0 %d)"><g class="bat" style="animation-duration:%ds;animation-delay:-%ds">'
            '<g class="bw1">%s</g><g class="bw2">%s</g></g></g>' % (y, duration, delay, up.paths(), down.paths()))


def web(cx, cy, sx, sy, size, color=WEB):
    """A cobweb in a corner. (cx, cy) is the corner pixel, sx and sy say which way the web opens."""
    g = Grid()
    for ang in (0, 22, 45, 68, 90):
        a = math.radians(ang)
        for t in range(size + 1):
            g.set(cx + sx * int(t * math.cos(a)), cy + sy * int(t * math.sin(a)), color)
    for r in (size // 3, 2 * size // 3, size):
        for ang in range(0, 91, 5):
            a = math.radians(ang)
            g.set(cx + sx * int(r * math.cos(a)), cy + sy * int(r * math.sin(a)), color)
    return g


def spider(x, thread_to, drop=7, duration=4, color="#1a0f1c", thread="#8d8da0"):
    """A spider that climbs up and down a thread. The thread is fixed, the spider moves along it."""
    t = Grid()
    for y in range(0, thread_to):
        t.set(x + 2, y, thread)
    s = Grid()
    for r, row in enumerate(SPIDER):
        for c, ch in enumerate(row):
            if ch == "1":
                s.set(x + c, thread_to + r, color)
    return ('<g>%s</g><g class="spd" style="animation-duration:%ds;--drop:%dpx">%s</g>'
            % (t.paths(), duration, drop, s.paths()))


CSS = """
.bat{animation:batfly 16s linear infinite}
.bw1{animation:fa .3s steps(1) infinite}
.bw2{opacity:0;animation:fb .3s steps(1) infinite}
.flk{animation:flk 1.6s steps(1) infinite}
.fog{animation:fog 40s linear infinite}
.spd{animation:spd 4s ease-in-out infinite}
.wisp{animation:wisp 2s steps(1) infinite}
@keyframes batfly{from{transform:translateX(-14px)}to{transform:translateX(214px)}}
@keyframes flk{0%,100%{opacity:1}30%{opacity:.55}55%{opacity:.9}75%{opacity:.5}}
@keyframes fog{from{transform:translateX(-60px)}to{transform:translateX(220px)}}
@keyframes spd{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}
@keyframes wisp{0%{opacity:.5}50%{opacity:.2}}
"""
# the poster and the strip do not include the shared rider keyframes, so they carry their own
SELF_CSS = """
.flk{animation:flk 1.6s steps(1) infinite}
.spd{animation:spd 4s ease-in-out infinite}
@keyframes flk{0%,100%{opacity:1}30%{opacity:.55}55%{opacity:.9}75%{opacity:.5}}
@keyframes spd{0%,100%{transform:translateY(0)}50%{transform:translateY(7px)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def moon_details(bg):
    for x, y in ((146, 33), (147, 33), (146, 34), (153, 37), (154, 37), (153, 38), (149, 43), (150, 43),
                 (156, 31), (143, 40), (143, 41)):
        bg.set(x, y, "#e8862a")


def fog_layer(width, ys, opacity=0.16):
    out = []
    for i, y in enumerate(ys):
        out.append('<g class="fog" style="animation-delay:-%ds"><rect x="0" y="%d" width="46" height="2" '
                   'fill="#d8c8e8" opacity="%s"/><rect x="20" y="%d" width="40" height="1" fill="#d8c8e8" '
                   'opacity="%s"/></g>' % (i * 17, y, opacity, y + 2, opacity))
    return "".join(out)


def tombstones(spec):
    g = Grid()
    for x, yb in spec:
        g.px.update(sprite(TOMB, TOMB_COL, x, yb).px)
    return g.paths()


def ghost_rider_extra():
    """A skull under the hat, glowing horse eyes and a pale trail. Coordinates are the rider's own."""
    skull = Grid()
    skull.rect(6, -19, 3, 3, "#f3ead2")
    skull.set(6, -18, "#1a0f1c")
    skull.set(8, -18, "#1a0f1c")
    skull.set(7, -17, "#1a0f1c")
    eye = Grid()
    eye.set(17, -13, "#ffa63d")
    trail = Grid()
    for x, y in ((-6, -12), (-9, -14), (-12, -11), (-15, -13), (-18, -12), (-21, -14)):
        trail.set(x, y, "#cfd6ff")
    return '%s%s<g class="wisp">%s</g>' % (skull.paths(), eye.paths(), trail.paths())


class Halloween(Decor):
    id = "halloween"
    name = "Halloween"

    def banner(self):
        ground = (fog_layer(200, (52, 55))
                  + tombstones([(44, 56), (122, 57)])
                  + pumpkins([(34, 56, 1, 0), (58, 58, 2, 0.4), (84, 56, 1, 0.9), (148, 56, 1, 0.2),
                              (166, 58, 1, 1.1)]))
        sky = bat_group(16, 17, 0) + bat_group(27, 21, 9) + bat_group(9, 25, 4)
        front = (web(199, 0, -1, 1, 15).paths().replace('fill="', 'opacity="0.55" fill="')
                 + spider(172, 8))
        return Layers(sun=(150, 38, 12, "#ffa63d", "#ff7a1a"), sun_details=moon_details, ground=ground, sky=sky,
                      front=front, rider_extra=ghost_rider_extra(), css=CSS,
                      label="Halloween decoration: a harvest moon, bats, jack o'lanterns, tombstones and a ghost rider")

    def footer(self):
        ground = pumpkins([(30, 27, 1, 0), (170, 28, 1, 0.8)])
        sky = bat_group(4, 18, 0) + bat_group(12, 23, 8)
        return Layers(text="SPOOKY TRAILS", ground=ground, sky=sky, rider_extra=ghost_rider_extra(), css=CSS)

    def poster(self):
        def draw(g):
            g.px.update(web(2, 2, 1, 1, 16, "#6b6478").px)
            body, face = pumpkin(86, 96)          # sits on the corner of the portrait frame
            g.px.update(body.px)
        _, face = pumpkin(86, 96)
        front = ('<g class="flk">%s</g>' % face.paths()) + spider(104, 12)
        return Layers(draw=draw, front=front, css=SELF_CSS)

    def strip(self):
        g = Grid()
        w = 168
        pts = []
        for x in range(w):
            y = 1 + int(round(3 * math.sin(math.pi * x / (w - 1))))
            g.set(x, y, "#3b2414")
            pts.append((x, y))
        colors = ["#f28a1f", "#8e5bc0", "#e8e0d0"]
        n = 0
        for x in range(12, w - 8, 9):
            y = pts[x][1] + 1
            c = colors[n % 3]
            n += 1
            for r, width in enumerate((5, 3, 1)):
                g.rect(x - width // 2 + 2 - 2, y + r, width, 1, c)
        lights = ""
        for x in (w // 4, 3 * w // 4):
            body, face = pumpkin(x, pts[x][1] + 8)
            g.px.update(body.px)
            lights += '<g class="flk">%s</g>' % face.paths()
        wl = web(0, 0, 1, 1, 12, "#8d8da0")
        wr = web(w - 1, 0, -1, 1, 12, "#8d8da0")
        body = g.paths() + lights + wl.paths() + wr.paths()
        return Layers(width=w, height=13, scale=5, body=body, css=SELF_CSS,
                      label="Halloween garland with flags, jack o'lanterns and cobwebs")


DECOR = Halloween()
