"""Generates the pixel art SVGs used by the profile README.

Run from the repo root:  python scripts/build_assets.py
Everything is drawn from code on a pixel grid, so colors and shapes are easy to tweak.
"""
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

FONT = {
    " ": ["00000"] * 7,
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00000", "00100"],
    ",": ["00000", "00000", "00000", "00000", "00100", "00100", "01000"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}


def text_width(s, scale=1):
    return len(s) * 6 * scale - scale


class Grid:
    def __init__(self):
        self.px = {}

    def set(self, x, y, c):
        self.px[(x, y)] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px[(xx, yy)] = c

    def text(self, s, x, y, c, scale=1):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for r, row in enumerate(glyph):
                for k, bit in enumerate(row):
                    if bit == "1":
                        self.rect(cx + k * scale, y + r * scale, scale, scale, c)
            cx += 6 * scale

    def paths(self):
        by_color = {}
        for (x, y), c in self.px.items():
            by_color.setdefault(c, []).append((y, x))
        out = []
        for c, pts in by_color.items():
            pts.sort()
            d = []
            i = 0
            while i < len(pts):
                y, x = pts[i]
                j = i
                while j + 1 < len(pts) and pts[j + 1][0] == y and pts[j + 1][1] == pts[j][1] + 1:
                    j += 1
                n = j - i + 1
                d.append(f"M{x} {y}h{n}v1h-{n}z")
                i = j + 1
            out.append(f'<path fill="{c}" d="{"".join(d)}"/>')
        return "\n".join(out)


INK = "#1a0f1c"
SCARF = "#b4372f"
SAND = "#e6b36a"


def rider():
    """Returns (common, frame_a, frame_b, dust). Origin is the hoof line, y grows downward."""
    common = Grid()
    # horse body
    common.rect(2, -10, 11, 4, INK)
    common.rect(1, -10, 2, 3, INK)
    common.rect(12, -13, 3, 5, INK)
    common.rect(14, -13, 5, 2, INK)
    common.rect(18, -12, 1, 2, INK)
    common.set(15, -14, INK)
    common.set(16, -14, INK)
    # tail
    common.rect(-1, -10, 2, 1, INK)
    for x, y in [(-2, -9), (-2, -8), (-3, -7), (-3, -6)]:
        common.set(x, y, INK)
    # rider
    common.rect(6, -16, 3, 6, INK)
    common.rect(6, -19, 3, 3, INK)
    common.rect(4, -20, 7, 1, INK)
    common.rect(5, -22, 5, 2, INK)
    common.rect(8, -15, 4, 1, INK)
    common.rect(6, -16, 3, 1, SCARF)
    common.set(5, -15, SCARF)
    common.set(4, -14, SCARF)

    a = Grid()
    for x, y in [(12, -6), (13, -5), (14, -4), (15, -3), (16, -2), (17, -1),
                 (11, -6), (12, -5), (13, -4), (14, -3), (15, -2),
                 (3, -6), (2, -5), (1, -4), (0, -3), (-1, -2), (-2, -1),
                 (4, -6), (3, -5), (2, -4), (1, -3), (0, -2)]:
        a.set(x, y, INK)

    b = Grid()
    b.rect(4, -6, 1, 4, INK)
    b.rect(6, -6, 1, 3, INK)
    b.rect(10, -6, 1, 3, INK)
    b.rect(12, -6, 1, 4, INK)
    b.rect(13, -3, 1, 1, INK)
    b.rect(3, -2, 1, 1, INK)

    dust = Grid()
    for x, y in [(-6, -2), (-9, -1), (-8, -3), (-12, -2), (-14, -1)]:
        dust.set(x, y, SAND)
    return common, a, b, dust


STYLE_COMMON = """
.fa{animation:fa .5s steps(1) infinite}
.fb{opacity:0;animation:fb .5s steps(1) infinite}
.bob{animation:bob .5s steps(1) infinite}
.dust{animation:dust .5s steps(1) infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}
@keyframes fb{0%{opacity:0}50%{opacity:1}}
@keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(-1px)}}
@keyframes dust{0%{opacity:.8}50%{opacity:.3}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def rider_group(extra_class="ride", extra=""):
    """The riding cowboy. `extra` is optional seasonal markup drawn on top, moving with the rider."""
    common, a, b, dust = rider()
    return (
        f'<g class="{extra_class}"><g class="bob">'
        f'<g class="dust">{dust.paths()}</g>'
        f'{common.paths()}'
        f'<g class="fa">{a.paths()}</g><g class="fb">{b.paths()}</g>'
        f'{extra}'
        f'</g></g>'
    )


def wrap_svg(w, h, scale, body, style, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w * scale}" height="{h * scale}" shape-rendering="crispEdges" '
        f'role="img" aria-label="{label}">\n<title>{label}</title>\n'
        f'<style>{style}</style>\n{body}\n</svg>\n'
    )


# ---------------------------------------------------------------- banner
def build_banner(deco=None):
    """The banner. `deco` is an optional seasonal decoration (see season_art), None gives the default look."""
    L = deco.banner() if deco else None
    W, H = 200, 60
    rnd = random.Random(7)
    bg = Grid()

    bands = [(0, "#1b1030"), (8, "#2a1745"), (14, "#46225a"), (20, "#7a2f5e"),
             (26, "#b8465a"), (32, "#e0675a"), (38, "#f0905a"), (44, "#f7b867"), (48, "#fbd48a")]
    for y in range(0, 51):
        idx = max(i for i, (s, _) in enumerate(bands) if s <= y)
        color = bands[idx][1]
        for x in range(W):
            c = color
            if idx > 0 and y == bands[idx][0] and x % 2 == 0:
                c = bands[idx - 1][1]
            if idx + 1 < len(bands) and y == bands[idx + 1][0] - 1 and x % 2 == 1:
                c = bands[idx + 1][1]
            bg.set(x, y, c)

    # sun (a season may swap it, for example for a big orange moon)
    sx, sy, r, core, ring = (L.sun if L and L.sun else (150, 41, 10, "#ffe29a", "#f9c27a"))
    for y in range(sy - r - 3, 51):
        for x in range(sx - r - 3, sx + r + 4):
            d = (x - sx) ** 2 + (y - sy) ** 2
            if d <= r * r:
                bg.set(x, y, core)
            elif d <= (r + 2) ** 2 and (x + y) % 2 == 0:
                bg.set(x, y, ring)
    if L and L.sun_details:
        L.sun_details(bg)

    far = [(0, 22, 43), (22, 27, 41), (27, 48, 44), (60, 85, 42), (85, 92, 44), (92, 120, 45),
           (130, 150, 42), (150, 175, 44), (175, 200, 43)]
    near = [(0, 14, 47), (14, 20, 45), (20, 36, 47), (70, 78, 46), (78, 100, 48),
            (120, 128, 47), (128, 160, 48), (160, 172, 46), (172, 200, 47)]
    for x0, x1, top in far:
        bg.rect(x0, top, x1 - x0, 51 - top, "#6a2f62")
    for x0, x1, top in near:
        bg.rect(x0, top, x1 - x0, 51 - top, "#4a2358")

    # tiny western town on the horizon
    town = "#2e1640"
    bg.rect(96, 45, 6, 6, town); bg.rect(97, 43, 4, 2, town)
    bg.rect(103, 47, 5, 4, town)
    bg.rect(109, 44, 7, 7, town); bg.rect(110, 42, 5, 2, town)
    bg.rect(119, 43, 4, 3, town); bg.rect(119, 46, 1, 5, town); bg.rect(122, 46, 1, 5, town)
    bg.rect(125, 47, 6, 4, town)
    for x, y in [(98, 47), (111, 46), (113, 46), (105, 49), (127, 49)]:
        bg.set(x, y, "#f7b867")

    # ground
    for y in range(51, 60):
        base = "#e6b36a" if y == 51 else ("#c98b4a" if y < 55 else "#a6692f")
        for x in range(W):
            c = base
            roll = rnd.random()
            if y > 51 and roll < 0.05:
                c = "#8a5624"
            elif y > 51 and roll > 0.97:
                c = "#e0a85e"
            bg.set(x, y, c)

    # cacti
    def saguaro(x, base, h):
        dark, light = "#2a4d34", "#3b6b47"
        bg.rect(x, base - h, 2, h, dark)
        bg.rect(x, base - h, 1, h, light)
        bg.rect(x - 3, base - h + 5, 3, 1, dark)
        bg.rect(x - 3, base - h + 2, 1, 4, dark)
        bg.rect(x + 2, base - h + 3, 3, 1, dark)
        bg.rect(x + 4, base - h, 1, 4, dark)

    saguaro(18, 51, 13)
    saguaro(181, 51, 10)
    saguaro(88, 51, 7)

    body = [bg.paths()]
    if L and L.ground:
        body.append(L.ground)

    # stars
    for n, delay in ((0, "0s"), (1, "1.1s")):
        g = Grid()
        for _ in range(9):
            g.set(rnd.randrange(2, 198), rnd.randrange(1, 19), "#f3e2c0")
        body.append(f'<g class="star" style="animation-delay:{delay}">{g.paths()}</g>')

    # clouds
    def cloud(y, delay, dur):
        g = Grid()
        g.rect(2, 0, 6, 1, "#e58aa0"); g.rect(0, 1, 12, 1, "#e58aa0"); g.rect(1, 2, 10, 1, "#d9738f")
        return (f'<g transform="translate(0 {y})"><g class="cloud" '
                f'style="animation-duration:{dur}s;animation-delay:-{delay}s">{g.paths()}</g></g>')

    body += [cloud(10, 18, 70), cloud(31, 40, 95), cloud(5, 55, 120)]
    if L and L.sky:
        body.append(L.sky)

    # name and role
    title = Grid()
    title.text("GABRIEL NUNES", 9, 7, "#1b1030", 2)
    title.text("GABRIEL NUNES", 8, 6, "#fff3d6", 2)
    title.text("SOFTWARE ENGINEER", 9, 22, "#1b1030", 1)
    title.text("SOFTWARE ENGINEER", 8, 21, "#f7b867", 1)
    body.append(title.paths())

    # tumbleweed (opposite direction to the rider)
    t1, t2 = Grid(), Grid()
    ring = [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3), (1, 4), (2, 4), (3, 4)]
    for x, y in ring:
        t1.set(x, y, "#8a5624"); t2.set(x, y, "#8a5624")
    for x, y in [(2, 1), (2, 2), (2, 3), (1, 2), (3, 2)]:
        t1.set(x, y, "#c98b4a")
    for x, y in [(1, 1), (3, 3), (2, 2), (3, 1), (1, 3)]:
        t2.set(x, y, "#c98b4a")
    body.append(
        '<g transform="translate(0 51)"><g class="weed"><g class="fa">'
        + t1.paths() + '</g><g class="fb">' + t2.paths() + '</g></g></g>'
    )

    # rider
    body.append(f'<g transform="translate(100 51)">{rider_group("ride", L.rider_extra if L else "")}</g>')
    if L and L.front:
        body.append(L.front)

    style = STYLE_COMMON + """
.ride{animation:ride 18s linear infinite}
.weed{animation:weed 11s linear infinite}
.cloud{animation-name:cloud;animation-timing-function:linear;animation-iteration-count:infinite}
.star{animation:star 2.4s steps(1) infinite}
@keyframes ride{from{transform:translateX(-130px)}to{transform:translateX(115px)}}
@keyframes weed{from{transform:translateX(212px)}to{transform:translateX(-14px)}}
@keyframes cloud{from{transform:translateX(-14px)}to{transform:translateX(214px)}}
@keyframes star{0%{opacity:1}50%{opacity:.25}}
""" + (L.css if L else "")
    label = "Pixel art banner: a cowboy riding a horse across a desert at sunset"
    if L and L.label:
        label += ". " + L.label
    return wrap_svg(W, H, 5, "\n".join(body), style, label)


# ---------------------------------------------------------------- wanted poster
def draw_cowboy(g, ox, oy, iw=58, ih=58):
    """Pixel art bust of the cowboy facing the viewer, drawn inside an iw x ih frame at (ox, oy).

    The figure is symmetric around the vertical line between columns cx-1 and cx.
    """
    cx = iw // 2

    def r(x, y, w, h, c):
        g.rect(ox + x, oy + y, w, h, c)

    def p(x, y, c):
        g.set(ox + x, oy + y, c)

    # palette
    skin, skin_sh = "#c98b5e", "#a86f48"
    dark = "#2a1a10"
    hat, hat_hi, hat_sh = "#5a3a22", "#7a5230", "#3b2414"
    vest, vest_hi = "#5a3a22", "#7a5230"
    shirt, shirt_hi, shirt_sh = "#b3a56c", "#cdbf86", "#8a7d4c"
    kerchief, kerchief_hi = "#1a1418", "#3a3038"

    # scenery behind him: sky bands, ground, fence
    r(0, 0, iw, ih, "#ecd8a3")
    r(0, 14, iw, 14, "#e8cf95")
    r(0, 28, iw, 30, "#e3c88f")
    r(0, 48, iw, 10, "#b58f56")
    for x in (4, 12, 51, 54):
        r(x, 44, 1, 8, "#8a5a3a")
    r(2, 46, 14, 1, "#8a5a3a")
    r(42, 46, 14, 1, "#8a5a3a")

    # shirt and sleeves
    for y in range(36, ih):
        half = {36: 10, 37: 14, 38: 18, 39: 21}.get(y, 24)
        r(cx - half, y, half * 2, 1, shirt)
        r(cx - half, y, 2, 1, shirt_hi)
        r(cx + half - 3, y, 3, 1, shirt_sh)
    for y in (46, 50, 54):
        r(cx - 23, y, 6, 1, shirt_sh)
        r(cx + 17, y, 6, 1, shirt_sh)

    # vest with a V opening, running to the bottom edge of the portrait
    r(cx - 13, 42, 26, ih - 42, vest)
    r(cx - 13, 42, 2, ih - 42, vest_hi)
    for y in range(42, 52):
        half = 6 - (y - 42) * 6 // 10
        r(cx - half, y, half * 2, 1, shirt)
        p(cx - half - 1, y, vest_hi)
        p(cx + half, y, hat_sh)
    for y in (53, 56):
        r(cx - 1, y, 2, 1, "#d9b873")

    # neck
    r(cx - 4, 32, 8, 6, skin_sh)

    # neckerchief: wide at the collar, tapering to a point, with a knot
    for y in range(35, 46):
        half = max(1, 8 - (y - 35) * 7 // 10)
        r(cx - half, y, half * 2, 1, kerchief)
    r(cx - 2, 38, 4, 3, kerchief_hi)
    r(cx - 1, 39, 2, 1, kerchief)

    # head, facing the viewer
    r(cx - 7, 18, 14, 14, skin)
    r(cx - 7, 18, 14, 2, skin_sh)       # shade under the brim
    r(cx - 9, 22, 2, 5, skin_sh)        # ears
    r(cx + 7, 22, 2, 5, skin_sh)

    # eyes: white with a centered pupil, brows above
    for x0 in (cx - 5, cx + 2):
        r(x0, 22, 3, 2, "#f3e8d0")
        r(x0 + 1, 22, 1, 2, dark)
    r(cx - 6, 20, 4, 1, dark)
    r(cx + 2, 20, 4, 1, dark)
    # nose
    r(cx - 1, 23, 1, 4, skin_sh)
    p(cx - 2, 26, skin_sh)
    p(cx + 1, 26, skin_sh)

    # sideburns, mustache and beard
    r(cx - 7, 18, 1, 9, dark)
    r(cx + 6, 18, 1, 9, dark)
    r(cx - 6, 27, 12, 2, dark)
    p(cx - 7, 28, dark)
    p(cx + 6, 28, dark)
    r(cx - 6, 29, 12, 3, dark)
    r(cx - 5, 32, 10, 1, dark)
    r(cx - 3, 33, 6, 1, dark)
    r(cx - 2, 29, 4, 1, "#7a3b2b")      # mouth

    # hat: crown, band, wide curved brim
    r(cx - 9, 6, 18, 9, hat)
    r(cx - 8, 5, 16, 1, hat)
    r(cx - 7, 4, 14, 1, hat)
    r(cx - 5, 3, 10, 1, hat)
    r(cx - 9, 6, 3, 9, hat_hi)
    r(cx + 5, 6, 4, 9, hat_sh)
    r(cx - 1, 4, 2, 4, hat_sh)          # crease
    r(cx - 9, 12, 18, 2, dark)          # band
    r(cx - 17, 15, 34, 2, hat_sh)       # brim
    r(cx - 15, 14, 30, 1, hat)
    r(cx - 19, 13, 3, 2, hat)           # upturned tips
    r(cx + 16, 13, 3, 2, hat)
    r(cx - 19, 12, 1, 1, hat)
    r(cx + 18, 12, 1, 1, hat)
    r(cx - 15, 17, 30, 1, hat_sh)       # brim underside


def build_wanted(deco=None):
    """The wanted poster. `deco` is an optional seasonal decoration, None gives the default look."""
    L = deco.poster() if deco else None
    W, H = 120, 156
    g = Grid()
    paper, edge, ink = "#e9d5a1", "#6b4423", "#3b2412"
    g.rect(0, 0, W, H, paper)
    # torn corners
    for cx, cy in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]:
        g.rect(cx - (0 if cx == 0 else 1), cy - (0 if cy == 0 else 1), 2, 2, "#00000000")
    g.rect(0, 0, W, 2, edge); g.rect(0, H - 2, W, 2, edge)
    g.rect(0, 0, 2, H, edge); g.rect(W - 2, 0, 2, H, edge)
    g.rect(5, 5, W - 10, 1, "#a8803f"); g.rect(5, H - 6, W - 10, 1, "#a8803f")
    g.rect(5, 5, 1, H - 10, "#a8803f"); g.rect(W - 6, 5, 1, H - 10, "#a8803f")
    # nails
    for x, y in [(9, 9), (W - 11, 9)]:
        g.rect(x, y, 2, 2, "#4a3a2a")

    def center(s, y, c, scale=1):
        g.text(s, (W - text_width(s, scale)) // 2, y, c, scale)

    center("WANTED", 12, ink, 3)
    # portrait frame (inner area 58 x 58)
    g.rect(30, 34, 60, 60, edge)
    draw_cowboy(g, 31, 35)

    center("GABRIEL NUNES", 101, ink)
    center("SOFTWARE ENGINEER", 111, ink)
    g.rect(20, 121, 80, 1, "#a8803f")
    center("REWARD:", 127, "#a8322a")
    center("ONE CLEAN MERGE", 138, ink)

    if L and L.draw:
        L.draw(g)
    body = g.paths().replace('fill="#00000000"', 'fill="none"')
    if L and L.front:
        body += L.front
    return wrap_svg(W, H, 3, body, (L.css if L else ""), "Wanted poster for Gabriel Nunes, software engineer")


# ---------------------------------------------------------------- footer
def build_footer(deco=None):
    """The footer. `deco` is an optional seasonal decoration, None gives the default look."""
    L = deco.footer() if deco else None
    W, H = 200, 30
    bg = Grid()
    for y0, y1, c in [(0, 6, "#46225a"), (6, 12, "#7a2f5e"), (12, 17, "#b8465a"),
                      (17, 21, "#e0675a"), (21, 22, "#f0905a")]:
        bg.rect(0, y0 - 0, W, y1 - y0, c)       # dusk sky, light enough for the dark rider
    for y in range(22, 30):
        bg.rect(0, y, W, 1, "#c98b4a" if y < 24 else "#a6692f")
    rnd = random.Random(3)
    for _ in range(40):
        bg.set(rnd.randrange(W), rnd.randrange(24, 30), "#8a5624")
    txt = (L.text if L and L.text else "HAPPY TRAILS")
    bg.text(txt, (W - text_width(txt, 1)) // 2 + 1, 9, "#1b1030", 1)
    bg.text(txt, (W - text_width(txt, 1)) // 2, 8, "#fff3d6", 1)
    body = [bg.paths()]
    if L and L.ground:
        body.append(L.ground)
    if L and L.sky:
        body.append(L.sky)
    body.append(f'<g transform="translate(100 22)">{rider_group("ride", L.rider_extra if L else "")}</g>')
    if L and L.front:
        body.append(L.front)
    style = STYLE_COMMON + """
.ride{animation:ride 22s linear infinite}
@keyframes ride{from{transform:translateX(-130px)}to{transform:translateX(115px)}}
""" + (L.css if L else "")
    label = "A cowboy rides away. " + ("Happy trails." if not (L and L.text) else L.text.capitalize() + ".")
    return wrap_svg(W, H, 5, "\n".join(body), style, label)


# ---------------------------------------------------------------- seasonal strip
def build_strip(deco=None):
    """A slim decorative strip above the 3D graph. Empty (one transparent pixel) when no season is active."""
    L = deco.strip() if deco else None
    if not L:
        return wrap_svg(1, 1, 1, "", "", "")
    return wrap_svg(L.width, L.height, L.scale, L.body, L.css, L.label)


# ---------------------------------------------------------------- divider
def build_divider():
    W, H = 160, 10
    g = Grid()
    c = "#c98b4a"
    for x in range(10, 70, 4):
        g.set(x, 5, c)
    for x in range(92, 152, 4):
        g.set(x, 5, c)
    # small cactus in the middle
    g.rect(79, 1, 2, 8, "#3b6b47")
    g.rect(76, 4, 3, 1, "#3b6b47"); g.rect(76, 2, 1, 3, "#3b6b47")
    g.rect(81, 3, 3, 1, "#3b6b47"); g.rect(83, 1, 1, 3, "#3b6b47")
    return wrap_svg(W, H, 5, g.paths(), "", "Divider")


# ---------------------------------------------------------------- holster icon
def build_holster():
    """An empty leather holster hanging from a belt with cartridge loops (no gun)."""
    m = Grid()
    leather, leather_dk, leather_hi = "#7a5230", "#5a3a22", "#a67444"
    belt, belt_hi = "#3b2414", "#5a3a22"
    brass, brass_dk, mouth, thread = "#e0b95e", "#b8873a", "#120a0e", "#e8d5a0"

    # belt
    m.rect(1, 1, 22, 5, belt)
    m.rect(1, 1, 22, 1, belt_hi)
    for x in range(2, 21, 2):
        m.set(x, 5, "#c98b4a")           # stitching along the belt
    # cartridge loops
    for x in (2, 5, 8, 11):
        m.rect(x, 2, 2, 1, brass_dk)
        m.rect(x, 3, 2, 2, brass)
    # buckle
    m.rect(17, 1, 5, 5, brass)
    m.rect(18, 2, 3, 3, belt)
    m.set(19, 3, brass)

    # holster body, narrowing toward the bottom
    def span(y):
        if y <= 10:
            return 7, 17
        if y <= 14:
            return 8, 17
        if y <= 17:
            return 8, 16
        if y <= 19:
            return 9, 15
        return 10, 14

    for y in range(6, 22):
        x0, x1 = span(y)
        m.rect(x0, y, x1 - x0 + 1, 1, leather)
        m.set(x0, y, leather_dk)
        m.set(x0 + 1, y, leather_hi)
        m.set(x1, y, leather_dk)
    x0, x1 = span(6)
    m.rect(x0, 6, x1 - x0 + 1, 1, leather_hi)       # rim
    for y in range(7, 10):                           # empty opening
        x0, x1 = span(y)
        m.rect(x0 + 2, y, x1 - x0 - 3, 1, mouth)
    for y in range(11, 20, 2):                       # stitching
        x0, x1 = span(y)
        m.set(x0 + 2, y, "#c98b4a")
        m.set(x1 - 1, y, "#c98b4a")
    # rivets
    m.set(8, 10, brass)
    m.set(16, 10, brass)
    # side strap and stud
    m.rect(19, 6, 2, 8, leather_dk)
    m.set(19, 9, brass)
    m.set(20, 9, brass_dk)
    # tie down string
    m.rect(11, 22, 2, 2, thread)
    m.set(10, 24, thread)
    m.set(13, 24, thread)

    outline = Grid()
    for (x, y) in list(m.px):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in m.px:
                outline.set(q[0], q[1], "#1d1008")
    for k, v in m.px.items():
        outline.px[k] = v
    return wrap_svg(24, 26, 2, outline.paths(), "", "An empty leather holster on a belt with cartridge loops")


# ---------------------------------------------------------------- heading icons
def outlined(m, color="#1d1008"):
    out = Grid()
    for (x, y) in list(m.px):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in m.px:
                out.set(q[0], q[1], color)
    out.px.update(m.px)
    return out


def build_sheriff():
    """Sheriff star with ball tips, for the 'The brand' heading."""
    import math
    m = Grid()
    brass, brass_hi, brass_dk = "#e0b95e", "#f3dc94", "#b8873a"
    cx, cy, R, r = 12.0, 12.5, 10.5, 4.6
    pts = []
    for k in range(10):
        ang = math.radians(-90 + 36 * k)
        rad = R if k % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))

    def inside(px, py):
        c = False
        j = len(pts) - 1
        for i in range(len(pts)):
            xi, yi = pts[i]
            xj, yj = pts[j]
            if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                c = not c
            j = i
        return c

    for y in range(24):
        for x in range(24):
            if inside(x + 0.5, y + 0.5):
                m.set(x, y, brass_dk if x + 0.5 > cx + 1 else brass)
    for k in range(0, 10, 2):
        tx, ty = pts[k]
        for y in range(24):
            for x in range(24):
                if (x + 0.5 - tx) ** 2 + (y + 0.5 - ty) ** 2 <= 2.1 ** 2:
                    m.set(x, y, brass_hi)
    for y in range(24):
        for x in range(24):
            d = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            if d <= 2.6 ** 2:
                m.set(x, y, "#7a5230")
            elif d <= 3.6 ** 2:
                m.set(x, y, brass_hi)
    return wrap_svg(24, 24, 2, outlined(m).paths(), "", "Sheriff star")


def build_saloon():
    """Old west saloon facade, for the 'The town' heading."""
    m = Grid()
    wood, wood_dk, wood_hi = "#a6692f", "#7a4a22", "#c98b4a"
    roof, light = "#5a3a22", "#f7b867"
    m.rect(3, 6, 18, 2, roof)                   # false front, top
    m.rect(7, 4, 10, 2, roof)
    m.rect(9, 2, 6, 2, roof)
    m.rect(3, 8, 18, 14, wood)
    for x in (6, 9, 12, 15, 18):                # planks
        m.rect(x, 8, 1, 14, wood_dk)
    m.rect(3, 8, 18, 1, wood_hi)
    m.rect(5, 9, 14, 3, "#e8d5a0")              # sign board
    for x in range(6, 18, 2):
        m.set(x, 10, "#5a3a22")
    m.rect(1, 13, 22, 2, roof)                  # porch roof
    m.rect(1, 15, 1, 7, wood_dk)
    m.rect(22, 15, 1, 7, wood_dk)
    m.rect(4, 16, 4, 4, light)                  # windows
    m.rect(16, 16, 4, 4, light)
    m.rect(5, 16, 1, 4, "#7a4a22")
    m.rect(17, 16, 1, 4, "#7a4a22")
    m.rect(9, 16, 6, 6, "#1d1008")              # doorway
    m.rect(9, 17, 3, 4, wood_dk)                # swinging doors
    m.rect(12, 17, 3, 4, wood)
    m.rect(0, 22, 24, 2, "#c98b4a")             # boardwalk
    return wrap_svg(24, 24, 2, outlined(m).paths(), "", "Old west saloon")


def build_signpost():
    """Wooden signpost with two arrows, for the 'Words to ride by' heading."""
    m = Grid()
    wood, wood_dk, wood_hi = "#a6692f", "#7a4a22", "#c98b4a"
    m.rect(11, 4, 3, 19, wood_dk)
    m.rect(11, 4, 1, 19, wood)
    m.rect(8, 22, 9, 2, "#c98b4a")              # base mound
    # arrow pointing right
    m.rect(3, 5, 14, 5, wood)
    for i in range(3):
        m.rect(17 + i, 5 + i, 1, 5 - 2 * i, wood)
    m.rect(3, 5, 14, 1, wood_hi)
    for x in (5, 7, 9, 11):
        m.set(x, 7, "#3b2414")
    # arrow pointing left
    m.rect(8, 13, 14, 5, wood)
    for i in range(3):
        m.rect(7 - i, 13 + i, 1, 5 - 2 * i, wood)
    m.rect(8, 13, 14, 1, wood_hi)
    for x in (12, 14, 16, 18):
        m.set(x, 15, "#3b2414")
    m.set(12, 6, "#d9b873")
    m.set(12, 14, "#d9b873")
    return wrap_svg(24, 24, 2, outlined(m).paths(), "", "Wooden signpost")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("banner.svg", build_banner), ("wanted.svg", build_wanted),
                     ("footer-dusk.svg", build_footer), ("divider.svg", build_divider),
                     ("holster.svg", build_holster), ("sheriff.svg", build_sheriff),
                     ("saloon.svg", build_saloon), ("signpost.svg", build_signpost)]:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", name)
