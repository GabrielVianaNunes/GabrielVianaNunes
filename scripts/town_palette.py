"""Colors of the western town, for daylight and for the dusk and night version.

Sprites only use CSS class names. The renderer writes one <style> block per theme, so the same
sprites serve both the light and the dark version of the README.
"""

# class: (day color, night color or None to darken the day color)
PALETTE = {
    "wood1": ("#a6692f", None),
    "wood2": ("#c98b4a", None),
    "wood3": ("#d9a85a", None),
    "plank": ("#7a4a22", None),
    "roof": ("#5a3a22", None),
    "roofhi": ("#7a4a22", None),
    "trim": ("#f3ead2", None),
    "trimdk": ("#cfc3a4", None),
    "red": ("#a8322a", None),
    "reddk": ("#7a2420", None),
    "stone": ("#d9c9a8", None),
    "stonedk": ("#b5a688", None),
    "door": ("#3b2414", None),
    "glass": ("#7fb8d6", "#f7b867"),
    "brass": ("#e0b95e", "#c99a40"),
    "green": ("#3b6b47", None),
    "greenlt": ("#4f8a5b", None),
    "hay": ("#e6c870", None),
    "iron": ("#4a4a56", None),
    "glow": ("#ff8a3a", "#ff8a3a"),
    "signtxt": ("#f3e2c0", "#f3e2c0"),
    "edge": ("#2a1a10", "#0e0709"),
}

NIGHT_DIM = 0.6

SCENE = {
    "day": {
        "sky": ["#7fb8d6", "#9cc8de", "#bcd6d8", "#e0dcc0", "#f6dcae"],
        "far": "#c98b6a", "near": "#a8664c", "ground": "#e6b36a", "street": "#d9a25a",
        "celestial": "#fff3c4", "pole": "#5a3a22", "haze": "#f6dcae",
    },
    "night": {
        "sky": ["#1b1030", "#2a1745", "#46225a", "#7a2f5e", "#b8465a", "#f0905a"],
        "far": "#4a2358", "near": "#37193f", "ground": "#8a5624", "street": "#6f4420",
        "celestial": "#f3e2c0", "pole": "#2a1a10", "haze": "#b8465a",
    },
}


def darken(hex_color, k):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * k), int(g * k), int(b * k))


def color(cls, theme):
    day, night = PALETTE[cls]
    if theme == "day":
        return day
    return night or darken(day, NIGHT_DIM)


def rules():
    """Class rules that read their fill from a CSS variable.

    Variables inherit into <use> clones, so one set of sprites can be recolored by whichever
    element carries the variables (the svg root for a single theme file, or a wrapper group).
    """
    return "".join(".%s{fill:var(--%s)}" % (cls, cls) for cls in PALETTE)


def variables(theme, selector="svg"):
    """The variable definitions of one theme, for example svg{--wood1:#a6692f;...}."""
    return "%s{%s}" % (selector, "".join("--%s:%s;" % (cls, color(cls, theme)) for cls in PALETTE))
