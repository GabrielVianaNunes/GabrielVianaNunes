"""Renders the western town as two SVG files, one for daylight and one for dusk and night.

  python scripts/build_town.py --input data/contributions-fixture.json --out dist

writes dist/western-town-day.svg and dist/western-town-night.svg. The README chooses between
them with a <picture> element, so the town follows the viewer's GitHub theme.

Layout comes from town_layout.py and the sprites from town_sprites.py. Sprites are defined once
as <symbol>s and placed with <use>, colored through CSS variables, which keeps each file small.
Nothing external is referenced and there is no script.
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_assets import Grid, rider_group  # noqa: E402
from town_layout import build_layout  # noqa: E402
from town_palette import SCENE, rules, variables  # noqa: E402
from town_sprites import SLOT_W, build  # noqa: E402

W, H = 840, 220
PITCH = 30
BACK_BASE, FRONT_BASE = 150, 207
BACK_SCALE = 0.8
FRONT_X0, BACK_X0 = 15, 30
GROUND_TOP = 130
MAX_BYTES = 120000

ANIMATIONS = """
.fa{animation:fa .5s steps(1) infinite}
.fb{opacity:0;animation:fb .5s steps(1) infinite}
.bob{animation:bob .5s steps(1) infinite}
.dust{animation:dust .5s steps(1) infinite}
.ride{animation:ride 34s linear infinite}
.weed{animation:weed 17s linear infinite}
.cloud{animation-name:cloud;animation-timing-function:linear;animation-iteration-count:infinite}
.twinkle{animation:twinkle 3s steps(1) infinite}
.lamp{animation:lamp 2.4s ease-in-out infinite}
.smoke{animation:smoke 5s linear infinite}
@keyframes fa{0%{opacity:1}50%{opacity:0}}
@keyframes fb{0%{opacity:0}50%{opacity:1}}
@keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(-1px)}}
@keyframes dust{0%{opacity:.8}50%{opacity:.3}}
@keyframes ride{from{transform:translateX(-460px)}to{transform:translateX(460px)}}
@keyframes weed{from{transform:translateX(860px)}to{transform:translateX(-20px)}}
@keyframes cloud{from{transform:translateX(-30px)}to{transform:translateX(870px)}}
@keyframes twinkle{0%{opacity:1}50%{opacity:.25}}
@keyframes lamp{0%,100%{opacity:.55}50%{opacity:1}}
@keyframes smoke{0%{transform:translateY(0);opacity:.7}100%{transform:translateY(-12px);opacity:0}}
@keyframes flick{0%,62%{opacity:0}63%,72%{opacity:1}73%,100%{opacity:0}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""
NIGHT_ONLY = ".flick{animation:flick 7s steps(1) infinite}"
DAY_ONLY = ".flick{opacity:0}"


def lot_place(lot):
    """x, baseline y and scale of the lot's sprite."""
    if lot["row"] == "front":
        return FRONT_X0 + lot["col"] * PITCH + (PITCH - SLOT_W) // 2, FRONT_BASE, 1.0
    s = BACK_SCALE
    return BACK_X0 + lot["col"] * PITCH + (PITCH - SLOT_W * s) / 2, BACK_BASE, s


def f(v):
    """Short number formatting for attributes."""
    return ("%.2f" % v).rstrip("0").rstrip(".")


def sky_and_scene(scene, theme, rnd):
    parts = []
    bands = scene["sky"]
    for i, c in enumerate(bands):
        y0 = GROUND_TOP * i // len(bands)
        y1 = GROUND_TOP * (i + 1) // len(bands)
        parts.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, y1 - y0 + 1, c))
    # sun or moon
    g = Grid()
    cx, cy, r = W - 110, 32, 9
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                g.set(x, y, scene["celestial"])
    parts.append(g.paths())
    if theme == "night":
        for k, delay in enumerate(("0s", "-1.1s", "-2.2s")):
            s = Grid()
            for _ in range(10):
                s.set(rnd.randrange(4, W - 4), rnd.randrange(3, 70), "#f3e2c0")
            parts.append('<g class="twinkle" style="animation-delay:%s">%s</g>' % (delay, s.paths()))
    # clouds
    cloud_color = "#ffffff" if theme == "day" else "#7a2f5e"
    for y, dur, off in ((14, 150, 40), (40, 210, 120), (24, 260, 200)):
        c = Grid()
        c.rect(2, 0, 7, 1, cloud_color)
        c.rect(0, 1, 13, 1, cloud_color)
        c.rect(1, 2, 11, 1, cloud_color)
        parts.append('<g transform="translate(0 %d)" opacity="%s"><g class="cloud" style="animation-duration:%ds;'
                     'animation-delay:-%ds">%s</g></g>' % (y, "0.8" if theme == "day" else "0.6", dur, off, c.paths()))
    # mesas
    for color, lo, hi, rows in ((scene["far"], 28, 62, 1), (scene["near"], 10, 28, 1)):
        x = 0
        m = Grid()
        while x < W:
            w = rnd.randrange(50, 120)
            h = rnd.randrange(lo, hi)
            top = GROUND_TOP - h
            wd = min(w, W - x)
            m.rect(x, top, wd, h, color)
            m.rect(x + 8, top - 4, max(0, wd - 16), 4, color)
            x += w + rnd.randrange(0, 40)
        parts.append(m.paths())
    # ground, streets and pebbles
    ground = Grid()
    ground.rect(0, GROUND_TOP, W, H - GROUND_TOP, scene["ground"])
    ground.rect(0, BACK_BASE, W, 4, scene["street"])
    ground.rect(0, FRONT_BASE, W, H - FRONT_BASE, scene["street"])
    dark = "#00000022"
    for _ in range(90):
        ground.set(rnd.randrange(W), rnd.randrange(GROUND_TOP + 2, H), dark)
    parts.append(ground.paths())
    return "".join(parts)


def poles(scene):
    """Telegraph poles and wires between the two streets."""
    g = Grid()
    xs = list(range(45, W, 150))
    for x in xs:
        g.rect(x, BACK_BASE - 28, 2, 28, scene["pole"])
        g.rect(x - 3, BACK_BASE - 28, 8, 1, scene["pole"])
    wire = Grid()
    for a, b in zip(xs, xs[1:]):
        mid = (a + b) // 2
        for x in range(a + 4, b - 1):
            sag = int(3 * (1 - ((x - mid) / ((b - a) / 2.0)) ** 2))
            wire.set(x, BACK_BASE - 27 + sag, scene["pole"])
    return g.paths() + wire.paths()


def tumbleweed():
    t1, t2 = Grid(), Grid()
    ring = [(1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3), (1, 4), (2, 4), (3, 4)]
    for x, y in ring:
        t1.set(x, y, "#8a5624")
        t2.set(x, y, "#8a5624")
    for x, y in [(2, 1), (2, 2), (2, 3), (1, 2), (3, 2)]:
        t1.set(x, y, "#c98b4a")
    for x, y in [(1, 1), (3, 3), (2, 2), (3, 1), (1, 3)]:
        t2.set(x, y, "#c98b4a")
    return ('<g transform="translate(0 %d)"><g class="weed"><g class="fa">%s</g><g class="fb">%s</g></g></g>'
            % (H - 6, t1.paths(), t2.paths()))


def caption(layout, theme):
    text = "%d CONTRIBUTIONS IN %d WEEKS" % (layout["total"], len(layout["lots"]))
    g = Grid()
    shadow = "#000000" if theme == "night" else "#ffffff"
    ink = "#ffffff" if theme == "night" else "#3b2414"
    g.text(text, 9, 9, shadow, 1)
    g.text(text, 8, 8, ink, 1)
    return g.paths()


def render(layout, theme):
    assert theme in ("day", "night")
    scene = SCENE[theme]
    rnd = random.Random(11)
    lots = layout["lots"]
    kinds = sorted({lot["kind"] for lot in lots} | {"water tower"})
    symbols = {}
    for kind in kinds:
        symbols[kind] = build(kind)
    defs = "".join('<symbol id="s-%s" overflow="visible">%s</symbol>' % (k.replace(" ", "-"), symbols[k].paths())
                   for k in kinds)

    body = [sky_and_scene(scene, theme, rnd), poles(scene)]

    def place(lot, window_k):
        x, base, s = lot_place(lot)
        p = symbols[lot["kind"]]
        if lot["mirror"]:
            tf = "translate(%s %d) scale(%s %s)" % (f(x + SLOT_W * s), base, f(-s), f(s))
        else:
            tf = "translate(%s %d) scale(%s %s)" % (f(x), base, f(s), f(s))
        inner = '<use href="#s-%s"/>' % lot["kind"].replace(" ", "-")
        if p.windows and lot["index"] % 5 == 2:
            wx, wy, ww, wh = p.windows[0]
            inner += ('<rect class="flick" x="%d" y="%d" width="%d" height="%d" fill="#0e0709" '
                      'style="animation-delay:-%ds"/>' % (wx, -(wy + wh), ww, wh, window_k % 6))
        if "smoke" in p.marks and lot["index"] % 2 == 0:
            sx, sy = p.marks["smoke"]
            inner += ('<rect class="smoke" x="%d" y="%d" width="2" height="2" fill="%s" '
                      'style="animation-delay:-%ds"/>' % (sx, -sy, "#e8e0d0" if theme == "day" else "#9a8aa0",
                                                          lot["index"] % 5))
        return '<g transform="%s">%s</g>' % (tf, inner)

    # water tower behind the busiest week, standing on the back street
    if layout["peak"] is not None:
        lot = lots[layout["peak"]]
        x, _, s = lot_place(lot)
        ts = 1.0 if lot["row"] == "front" else BACK_SCALE
        body.append('<g transform="translate(%s %d) scale(%s)"><use href="#s-water-tower"/></g>'
                    % (f(x + 4), BACK_BASE, f(ts)))

    back = "".join(place(lot, i) for i, lot in enumerate(lots) if lot["row"] == "back")
    body.append('<g opacity="0.88">%s</g>' % back)
    body.append("".join(place(lot, i) for i, lot in enumerate(lots) if lot["row"] == "front"))

    # lantern next to the current week
    if layout["current"] is not None:
        lot = lots[layout["current"]]
        x, base, s = lot_place(lot)
        lx = int(x + SLOT_W * s) + 1
        lamp = Grid()
        lamp.rect(lx, base - 14, 1, 14, scene["pole"])
        lamp.rect(lx - 1, base - 18, 3, 4, "#ffd36a")
        body.append('<g class="lamp">%s</g>' % lamp.paths())

    body.append('<g transform="translate(%d %d)">%s</g>' % (W // 2, FRONT_BASE + 6, rider_group("ride")))
    body.append(tumbleweed())
    body.append(caption(layout, theme))

    label = ("Pixel art western town built from my last %d weeks of GitHub contributions, "
             "%d contributions in total. Busier weeks are bigger buildings." % (len(lots), layout["total"]))
    style = rules() + variables(theme, "svg") + ANIMATIONS + (NIGHT_ONLY if theme == "night" else DAY_ONLY)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
           'shape-rendering="crispEdges" role="img" aria-label="%s">'
           '<title>Western town of contributions</title><style>%s</style><defs>%s</defs>%s</svg>'
           % (W, H, W, H, label, style, defs, "".join(body)))
    return svg


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    with open(args.input, encoding="utf-8") as fh:
        data = json.load(fh)
    layout = build_layout(data["weeks"])
    os.makedirs(args.out, exist_ok=True)
    for theme in ("day", "night"):
        svg = render(layout, theme)
        if len(svg.encode("utf-8")) > MAX_BYTES:
            print("error: %s is %d bytes, over the %d byte budget" % (theme, len(svg), MAX_BYTES), file=sys.stderr)
            return 1
        path = os.path.join(args.out, "western-town-%s.svg" % theme)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print("wrote", path, len(svg) // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
