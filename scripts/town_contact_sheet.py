"""Draws docs/town/sprites-sheet.svg: every sprite of the town, in daylight and at night.

Run from the repo root:  python scripts/town_contact_sheet.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_assets import Grid  # noqa: E402
from town_palette import SCENE, rules, variables  # noqa: E402
from town_sprites import SPRITES, build  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "town", "sprites-sheet.svg")

LABELS = {
    "cabin": "CABIN", "barn": "BARN", "stable": "STABLE", "shack": "SHACK", "townhouse": "HOUSE",
    "saloon": "SALOON", "store": "STORE", "blacksmith": "SMITH", "hotel": "HOTEL",
    "grand hotel": "GRAND", "sheriff": "LAW", "bank": "BANK", "church": "CHURCH",
    "cactus": "CACTUS", "post": "POST", "wagon": "WAGON", "barrels": "BARREL", "well": "WELL",
    "water tower": "TOWER",
}
CELL_W, ROW_H, PER_ROW = 42, 86, 10
BASE = 70


def block(theme, oy, scope):
    scene = SCENE[theme]
    kinds = list(SPRITES)
    rows = (len(kinds) + PER_ROW - 1) // PER_ROW
    h = rows * ROW_H
    w = CELL_W * PER_ROW
    parts = []
    bands = scene["sky"]
    bh = h // len(bands) + 1
    for i, c in enumerate(bands):
        parts.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (oy + i * h // len(bands), w, bh, c))
    labels = Grid()
    for i, kind in enumerate(kinds):
        r, c = divmod(i, PER_ROW)
        x = c * CELL_W + (CELL_W - 26) // 2
        base = oy + r * ROW_H + BASE
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' %
                     (c * CELL_W, base, CELL_W, 4, scene["ground"]))
        parts.append('<use href="#s-%s" x="%d" y="%d"/>' % (kind.replace(" ", "-"), x, base))
        text = LABELS[kind]
        lw = len(text) * 6 - 1
        labels.text(text, c * CELL_W + (CELL_W - lw) // 2, base + 6, "#ffffff" if theme == "night" else "#3b2414", 1)
    parts.append('<g>%s</g>' % labels.paths())
    return '<g class="%s">%s</g>' % (scope, "".join(parts)), h


def main():
    defs = []
    for kind in SPRITES:
        defs.append('<symbol id="s-%s" overflow="visible">%s</symbol>' % (kind.replace(" ", "-"), build(kind).paths()))
    day, h = block("day", 0, "d")
    night, _ = block("night", h, "n")
    w = CELL_W * PER_ROW
    total = 2 * h
    style = rules() + variables("day", ".d") + variables("night", ".n")
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
           'shape-rendering="crispEdges" role="img" aria-label="Western town sprites in daylight and at night">'
           '<title>Western town sprites</title><style>%s</style><defs>%s</defs>%s%s</svg>'
           % (w, total, w * 2, total * 2, style, "".join(defs), day, night))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.normpath(OUT), len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
