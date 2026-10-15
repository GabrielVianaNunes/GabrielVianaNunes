"""Draws docs/town/design-sheet.svg: palette, sprite sizes and two rough mock streets.

The mock uses the real weekly contribution totals measured for issue 1, so it shows how
the town would actually look. Sprites here are placeholders: the final art comes in issue 5.

Run from the repo root:  python scripts/town_design_sheet.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_assets import FONT, Grid, text_width  # noqa: E402

DIGITS = {
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
FONT.update(DIGITS)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "town", "design-sheet.svg")

# Weekly totals of the last 53 weeks, oldest first (measured 2026-10-15, see issue 1).
WEEKS = [0] * 33 + [4, 0, 0, 6, 26, 79, 2, 61, 13, 1, 28, 95, 66, 79, 39, 0, 31, 238, 73, 69]

W, PANEL_H = 840, 215
PITCH, BODY_W = 30, 26
FLOOR_H = 14


def darken(hex_color, k):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * k), int(g * k), int(b * k))


DAY = dict(
    sky=["#7fb8d6", "#9cc8de", "#bcd6d8", "#e0dcc0", "#f6dcae"],
    far="#c98b6a", near="#a8664c", ground="#e6b36a", street="#d9a25a",
    glass="#7fb8d6", celestial="#fff3c4", dim=1.0,
)
NIGHT = dict(
    sky=["#1b1030", "#2a1745", "#46225a", "#7a2f5e", "#b8465a", "#f0905a"],
    far="#4a2358", near="#37193f", ground="#8a5624", street="#6f4420",
    glass="#f7b867", celestial="#f3e2c0", dim=0.62,
)
BODY = {1: "#a6692f", 2: "#c98b4a", 3: "#d9a85a", 4: "#d9c9a8"}


def sky(g, ox, oy, pal, h):
    n = len(pal["sky"])
    for i, c in enumerate(pal["sky"]):
        y0 = oy + i * h // n
        y1 = oy + (i + 1) * h // n
        g.rect(ox, y0, W, y1 - y0, c)


def mesas(g, oy, pal, base, rnd, color, lo, hi):
    x = 0
    while x < W:
        w = rnd.randrange(50, 120)
        top = base - rnd.randrange(lo, hi)
        g.rect(x, top, min(w, W - x), base - top, color)
        g.rect(x + 8, top - 4, max(0, min(w, W - x) - 16), 4, color)
        x += w + rnd.randrange(0, 40)


def cactus(g, x, base, pal):
    c = darken("#3b6b47", pal["dim"])
    g.rect(x + 11, base - 14, 3, 14, c)
    g.rect(x + 7, base - 9, 4, 2, c); g.rect(x + 7, base - 12, 2, 4, c)
    g.rect(x + 14, base - 7, 4, 2, c); g.rect(x + 16, base - 10, 2, 4, c)


def building(g, x, base, tier, pal, s, idx, kind=""):
    """Rough placeholder: body, roof, windows, door. Final sprites come in issue 5."""
    if tier == 0:
        cactus(g, x, base, pal)
        return
    heights = {1: 22, 2: 36, 3: 50, 4: 64}
    w = int(BODY_W * s)
    h = int(heights[tier] * s)
    body = darken(BODY[tier], pal["dim"])
    roof = darken("#5a3a22", pal["dim"])
    x0 = x + (PITCH - w) // 2
    g.rect(x0, base - h, w, h, body)
    g.rect(x0 - 1, base - h - 3, w + 2, 3, roof)
    if tier >= 2:                                  # false front
        g.rect(x0 + 3, base - h - 7, w - 6, 4, roof)
    if kind == "church":                           # steeple placeholder
        g.rect(x0 + w // 2 - 1, base - h - 14, 3, 11, roof)
    if kind in ("cabin", "townhouse"):             # chimney placeholder for old homes
        g.rect(x0 + w - 7, base - h - 9, 3, 7, darken("#7a4a22", pal["dim"]))
    if kind == "sheriff":                          # brass star placeholder
        g.rect(x0 + w // 2 - 1, base - h + 2, 3, 3, "#e0b95e")
    if kind == "bank":                             # columns placeholder
        for cx in (x0 + 3, x0 + w - 6):
            g.rect(cx, base - h + 8, 3, h - 16, darken("#f3ead2", pal["dim"]))
    floors = max(1, tier)
    for f in range(floors):
        wy = base - h + 5 + int(f * FLOOR_H * s)
        if f == floors - 1:
            wy = base - int(11 * s) - 4
        for wx in (x0 + 4, x0 + w - 8):
            g.rect(wx, wy, 4, 4, pal["glass"])
    g.rect(x0 + w // 2 - 2, base - int(8 * s), 4, int(8 * s), darken("#3b2414", pal["dim"]))


def tiers_for(weeks):
    nz = sorted(x for x in weeks if x)
    q = lambda p: nz[min(len(nz) - 1, int(p * len(nz)))]
    p25, p50, p75 = q(0.25), q(0.5), q(0.75)
    out = []
    for v in weeks:
        out.append(0 if v == 0 else 1 if v <= p25 else 2 if v <= p50 else 3 if v <= p75 else 4)
    return out, (p25, p50, p75)


def assign_types(tiers):
    """Building type for every lot, oldest first, following the uniqueness rules.

    Sheriff office 1, bank 1, church up to 2. Everything else may repeat.
    """
    n = len(tiers)
    kinds = [""] * n
    for i, t in enumerate(tiers):
        if t == 1:      # quiet weeks: mostly homes, plus barns and stables
            kinds[i] = ("cabin", "barn", "cabin", "stable", "cabin", "shack")[i % 6]
        elif t == 2:    # moderate weeks: townhouses mixed with trade buildings
            kinds[i] = ("townhouse", "saloon", "store", "townhouse", "blacksmith")[i % 5]
        elif t == 3:
            kinds[i] = "hotel"
        elif t == 4:
            kinds[i] = "grand hotel"
    t4 = [i for i, t in enumerate(tiers) if t == 4]
    if t4:
        kinds[t4[-1]] = "bank"
    t3 = [i for i, t in enumerate(tiers) if t == 3]
    if len(t3) >= 3:
        kinds[t3[0]] = "church"
        kinds[t3[-1]] = "church"
    elif t3:
        kinds[t3[0]] = "church"
    pool = [i for i in t3 if kinds[i] == "hotel"] or [i for i, t in enumerate(tiers) if t == 2]
    if pool:
        kinds[min(pool, key=lambda i: abs(i - n // 2))] = "sheriff"
    return kinds


def panel(g, oy, pal, label):
    rnd = random.Random(5)
    sky(g, 0, oy, pal, 130)
    g.rect(0, oy + 130, W, PANEL_H - 130, pal["ground"])
    g.rect(W - 120, oy + 22, 18, 18, pal["celestial"])             # sun or moon
    mesas(g, oy, pal, oy + 130, rnd, pal["far"], 40, 80)
    mesas(g, oy, pal, oy + 130, rnd, pal["near"], 18, 40)
    tiers, _ = tiers_for(WEEKS)
    kinds = assign_types(tiers)
    back, front = tiers[:26], tiers[26:]
    peak = WEEKS.index(max(WEEKS))
    g.rect(0, oy + 150, W, 4, pal["street"])
    g.rect(0, oy + 207, W, 8, pal["street"])
    for i, t in enumerate(back):
        building(g, 8 + i * PITCH + 2, oy + 150, t, pal, 0.8, i, kinds[i])
    for i, t in enumerate(front):
        building(g, i * PITCH, oy + 207, t, pal, 1.0, i, kinds[26 + i])
    # water tower at the busiest week (placeholder)
    px = (peak - 26) * PITCH + 20
    wood = darken("#7a4a22", pal["dim"])
    g.rect(px, oy + 207 - 52, 18, 12, wood)
    g.rect(px + 2, oy + 207 - 40, 2, 40, wood); g.rect(px + 14, oy + 207 - 40, 2, 40, wood)
    g.text(label, 8, oy + 6, "#ffffff", 1)


def legend(g, oy):
    g.rect(0, oy, W, 190, "#14101c")
    g.text("TIERS BY WEEKLY TOTAL, ROUGH SPRITES AT REAL SIZE", 10, oy + 8, "#f3e2c0", 1)
    names = [(0, "", "0 EMPTY", "CACTUS WELL"), (1, "cabin", "1 CABIN", "BARN STABLE SHACK"),
             (2, "townhouse", "2 TOWNHOUSE", "SALOON STORE SMITH"), (3, "hotel", "3 HOTEL", "CHURCH 2 SHERIFF 1"),
             (4, "bank", "4 BANK 1", "GRAND HOTEL")]
    x = 20
    for tier, kind, a, b in names:
        building(g, x, oy + 120, tier, DAY, 1.0, 2, kind)
        g.text(a, x - 4, oy + 130, "#f7b867", 1)
        if b:
            g.text(b, x - 4, oy + 142, "#c98b4a", 1)
        x += 160
    g.text("LOT 30 PX, BUILDING 26 PX, FLOOR 14 PX, CANVAS 840 BY 440", 10, oy + 165, "#e8d5a0", 1)


def main():
    g = Grid()
    g.rect(0, 0, W, 10, "#14101c")
    panel(g, 0, DAY, "DAY, LIGHT THEME")
    panel(g, PANEL_H + 5, NIGHT, "NIGHT, DARK THEME")
    legend(g, 2 * PANEL_H + 10)
    height = 2 * PANEL_H + 10 + 190
    body = g.paths()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" '
           f'height="{height}" shape-rendering="crispEdges" role="img" '
           f'aria-label="Western town design sheet: day and night mock streets and the building tiers">'
           f'<title>Western town design sheet</title>{body}</svg>')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.normpath(OUT), len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
