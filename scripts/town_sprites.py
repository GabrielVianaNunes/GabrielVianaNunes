"""Pixel art sprites for the western town, drawn from code.

Every sprite is painted on a pixel grid whose origin is the bottom left corner (x grows to the
right, y grows upward) and uses only palette class names, so one drawing serves day and night.
Buildings fit in 26 pixels of width, the water tower in 18.
"""

SLOT_W = 26

FONT3 = {
    "A": ("010", "101", "111", "101", "101"),
    "B": ("110", "101", "110", "101", "110"),
    "E": ("111", "100", "110", "100", "111"),
    "H": ("101", "101", "111", "101", "101"),
    "I": ("111", "010", "010", "010", "111"),
    "K": ("101", "101", "110", "101", "101"),
    "L": ("100", "100", "100", "100", "111"),
    "M": ("101", "111", "111", "101", "101"),
    "N": ("111", "101", "101", "101", "101"),
    "O": ("111", "101", "101", "101", "111"),
    "R": ("110", "101", "110", "101", "101"),
    "S": ("111", "100", "111", "001", "111"),
    "T": ("111", "010", "010", "010", "010"),
}

STAR = ("00100", "01110", "11111", "01110", "01010")


class Painter:
    def __init__(self):
        self.px = {}

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px[(xx, yy)] = c

    def pix(self, x, y, c):
        self.px[(x, y)] = c

    def roof(self, x0, y, w, c, rows):
        """Stepped triangular roof: each row is two pixels narrower than the one below."""
        for i in range(rows):
            self.rect(x0 + i, y + i, w - 2 * i, 1, c)

    def text(self, s, x, y, c):
        """3 by 5 pixel text, y is the bottom row."""
        cx = x
        for ch in s:
            for r, row in enumerate(FONT3[ch]):
                for k, bit in enumerate(row):
                    if bit == "1":
                        self.pix(cx + k, y + 4 - r, c)
            cx += 4

    def star(self, x, y, c):
        for r, row in enumerate(STAR):
            for k, bit in enumerate(row):
                if bit == "1":
                    self.pix(x + k, y + 4 - r, c)

    def window(self, x, y, w, h, cross=True):
        self.rect(x, y, w, h, "glass")
        if cross and w >= 4 and h >= 4:
            self.rect(x + w // 2, y, 1, h, "plank")
            self.rect(x, y + h // 2, w, 1, "plank")

    def size(self):
        xs = [p[0] for p in self.px]
        ys = [p[1] for p in self.px]
        return max(xs) + 1, max(ys) + 1

    def outline(self):
        """A one pixel dark edge around the sprite (never below the ground), for readability."""
        edge = {}
        for (x, y) in self.px:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in self.px and q[1] >= 0:
                    edge[q] = "edge"
        return edge

    def paths(self, outline=True):
        """SVG path markup, one <path> per class, with y flipped so the origin is the ground."""
        pixels = dict(self.outline()) if outline else {}
        pixels.update(self.px)
        by = {}
        for (x, y), c in pixels.items():
            by.setdefault(c, []).append((y, x))
        out = []
        for c in sorted(by):
            pts = sorted(by[c])
            d = []
            i = 0
            while i < len(pts):
                y, x = pts[i]
                j = i
                while j + 1 < len(pts) and pts[j + 1][0] == y and pts[j + 1][1] == pts[j][1] + 1:
                    j += 1
                n = j - i + 1
                d.append("M%d %dh%dv1h-%dz" % (x, -y - 1, n, n))
                i = j + 1
            out.append('<path class="%s" d="%s"/>' % (c, "".join(d)))
        return "".join(out)


# --------------------------------------------------------------------------- homes and farm

def cabin():
    p = Painter()
    p.rect(3, 0, 20, 14, "wood1")
    for y in (3, 6, 9, 12):
        p.rect(3, y, 20, 1, "plank")
    p.roof(1, 14, 24, "roof", 8)
    p.rect(1, 14, 24, 1, "roofhi")
    p.rect(18, 20, 4, 7, "stone")
    p.rect(18, 20, 1, 7, "stonedk")
    p.rect(11, 0, 5, 9, "door")
    p.pix(14, 4, "brass")
    p.window(5, 6, 4, 4)
    p.window(18, 6, 4, 4)
    p.rect(1, 0, 24, 1, "plank")
    p.rect(1, 1, 1, 8, "plank")
    p.rect(24, 1, 1, 8, "plank")
    return p


def barn():
    p = Painter()
    p.rect(2, 0, 22, 14, "red")
    for x in range(5, 23, 4):
        p.rect(x, 0, 1, 14, "reddk")
    p.roof(1, 14, 24, "reddk", 9)
    p.rect(8, 0, 10, 11, "reddk")
    p.rect(8, 0, 10, 1, "trim")
    p.rect(8, 10, 10, 1, "trim")
    p.rect(8, 0, 1, 11, "trim")
    p.rect(17, 0, 1, 11, "trim")
    for i in range(9):
        p.pix(9 + i, 1 + i, "trim")
        p.pix(16 - i, 1 + i, "trim")
    p.rect(11, 15, 4, 4, "door")
    p.rect(12, 15, 2, 2, "hay")
    return p


def stable():
    p = Painter()
    p.rect(1, 0, 24, 10, "wood1")
    for x in range(4, 24, 5):
        p.rect(x, 0, 1, 10, "plank")
    p.roof(0, 10, 26, "roof", 5)
    p.rect(4, 0, 6, 8, "door")
    p.rect(16, 0, 6, 8, "door")
    p.rect(6, 3, 3, 4, "wood3")            # a horse looking out of the left stall
    p.rect(5, 5, 2, 2, "wood3")
    p.pix(6, 6, "door")
    p.rect(11, 0, 4, 4, "hay")
    p.rect(11, 3, 4, 1, "wood3")
    return p


def shack():
    p = Painter()
    p.rect(4, 0, 18, 10, "wood1")
    for x in range(6, 22, 3):
        p.rect(x, 0, 1, 10, "plank")
    p.rect(2, 10, 22, 2, "roof")
    p.rect(4, 12, 18, 1, "roof")
    p.rect(9, 0, 5, 7, "door")
    p.rect(17, 4, 3, 3, "glass")
    p.rect(21, 0, 3, 3, "hay")
    return p


def townhouse():
    p = Painter()
    p.rect(2, 0, 22, 28, "wood2")
    p.rect(2, 15, 22, 1, "plank")
    p.rect(2, 27, 22, 1, "plank")
    p.roof(1, 28, 24, "roof", 6)
    p.rect(19, 33, 4, 7, "stone")
    p.rect(19, 33, 1, 7, "stonedk")
    for x in (4, 18):
        p.window(x, 19, 4, 6)
        p.rect(x - 1, 19, 1, 6, "green")
        p.rect(x + 4, 19, 1, 6, "green")
        p.window(x, 5, 4, 5)
    p.rect(11, 0, 5, 10, "door")
    p.pix(14, 4, "brass")
    p.rect(11, 17, 4, 9, "door")             # balcony door
    p.rect(8, 15, 10, 1, "plank")             # balcony
    p.rect(8, 16, 1, 3, "plank")
    p.rect(17, 16, 1, 3, "plank")
    p.rect(8, 18, 10, 1, "plank")
    return p


# --------------------------------------------------------------------------- trade and law

def saloon():
    p = Painter()
    p.rect(1, 0, 24, 22, "wood2")
    for x in range(4, 24, 4):
        p.rect(x, 0, 1, 22, "plank")
    p.rect(1, 22, 24, 2, "wood2")
    p.rect(5, 24, 16, 6, "wood2")
    p.rect(0, 22, 26, 2, "roof")
    p.rect(4, 30, 18, 2, "roof")
    p.window(8, 25, 4, 4)
    p.window(15, 25, 4, 4)
    p.rect(1, 15, 24, 7, "door")             # sign board
    p.text("SALOON", 2, 16, "signtxt")
    p.rect(0, 11, 26, 2, "roof")             # porch roof
    p.rect(0, 0, 1, 11, "plank")
    p.rect(25, 0, 1, 11, "plank")
    p.window(3, 3, 5, 6, cross=False)
    p.window(18, 3, 5, 6, cross=False)
    p.rect(9, 0, 8, 10, "door")              # swinging doors
    p.rect(9, 1, 3, 7, "wood3")
    p.rect(14, 1, 3, 7, "wood3")
    return p


def store():
    p = Painter()
    p.rect(1, 0, 24, 22, "wood3")
    p.rect(0, 22, 26, 3, "roof")
    p.rect(3, 25, 20, 1, "roof")
    p.rect(0, 12, 26, 4, "red")
    for x in range(0, 26, 4):
        p.rect(x, 12, 2, 4, "trim")
    p.rect(0, 11, 26, 1, "reddk")
    p.rect(2, 16, 22, 6, "door")
    p.text("STORE", 4, 17, "signtxt")
    p.window(3, 2, 7, 8, cross=False)
    p.window(16, 2, 7, 8, cross=False)
    p.rect(11, 0, 4, 9, "door")
    p.rect(0, 0, 2, 3, "hay")
    p.rect(24, 0, 2, 3, "hay")
    return p


def blacksmith():
    p = Painter()
    p.rect(1, 0, 24, 12, "plank")
    for i in range(5):
        p.rect(0, 12 + i, 26, 1, "roof")
    p.rect(19, 17, 4, 10, "stone")
    p.rect(19, 17, 1, 10, "stonedk")
    p.rect(18, 0, 6, 6, "stone")
    p.rect(19, 1, 4, 3, "glow")
    p.rect(0, 0, 2, 12, "wood1")
    p.rect(24, 0, 2, 12, "wood1")
    p.rect(6, 0, 6, 2, "iron")               # anvil
    p.rect(7, 2, 4, 2, "iron")
    p.rect(4, 4, 9, 2, "iron")
    p.rect(2, 8, 3, 3, "iron")               # horseshoe on the wall
    p.rect(3, 9, 1, 2, "plank")
    return p


def hotel():
    p = Painter()
    p.rect(1, 0, 24, 36, "wood3")
    for y in (12, 24):
        p.rect(1, y, 24, 1, "plank")
    p.rect(0, 36, 26, 2, "roof")
    p.rect(1, 38, 24, 8, "door")             # roof sign board
    p.text("HOTEL", 3, 40, "signtxt")
    p.rect(0, 12, 26, 1, "plank")            # balcony
    for x in range(0, 26, 5):
        p.rect(x, 13, 1, 3, "plank")
    p.rect(0, 16, 26, 1, "plank")
    for x in (4, 11, 18):
        p.window(x, 26, 4, 7)
        p.window(x, 17, 4, 6)
    p.window(3, 3, 5, 6, cross=False)
    p.window(18, 3, 5, 6, cross=False)
    p.rect(11, 0, 4, 9, "door")
    return p


def grand_hotel():
    p = Painter()
    p.rect(1, 0, 24, 48, "wood3")
    for y in (12, 24, 36):
        p.rect(1, y, 24, 1, "plank")
    p.rect(0, 48, 26, 3, "roof")
    p.rect(1, 51, 24, 8, "door")
    p.text("HOTEL", 3, 53, "signtxt")
    p.rect(13, 59, 1, 5, "iron")             # flag pole
    p.rect(14, 61, 5, 3, "red")
    for y in (14, 26, 38):
        for x in (3, 9, 15, 21):
            p.window(x, y, 3, 7, cross=False)
    p.window(3, 3, 5, 6, cross=False)
    p.window(18, 3, 5, 6, cross=False)
    p.rect(11, 0, 4, 10, "door")
    p.rect(9, 10, 8, 1, "brass")
    return p


def sheriff():
    p = Painter()
    p.rect(1, 0, 24, 22, "wood2")
    for x in range(4, 24, 4):
        p.rect(x, 0, 1, 22, "plank")
    p.rect(0, 22, 26, 3, "roof")
    p.rect(6, 25, 14, 7, "wood2")
    p.rect(5, 32, 16, 2, "roof")
    p.star(10, 26, "brass")
    p.rect(3, 8, 7, 8, "door")               # jail window with bars
    for x in (4, 6, 8):
        p.rect(x, 8, 1, 8, "iron")
    p.rect(11, 0, 5, 10, "door")
    p.pix(14, 4, "brass")
    p.rect(18, 5, 5, 7, "trim")              # wanted poster
    p.rect(19, 9, 3, 2, "door")
    p.rect(19, 6, 3, 1, "door")
    p.rect(0, 12, 26, 2, "roof")
    p.rect(0, 0, 1, 12, "plank")
    p.rect(25, 0, 1, 12, "plank")
    return p


def bank():
    p = Painter()
    p.rect(1, 0, 24, 44, "stone")
    p.rect(0, 0, 26, 2, "stonedk")
    p.rect(1, 38, 24, 6, "stonedk")          # frieze with the name
    p.text("BANK", 5, 39, "brass")
    for x in (3, 9, 15, 21):
        p.rect(x, 2, 2, 36, "trim")
    p.roof(1, 44, 24, "stonedk", 6)
    p.rect(11, 0, 4, 13, "door")
    p.rect(12, 13, 2, 1, "door")
    p.pix(14, 5, "brass")
    p.window(5, 6, 3, 10, cross=False)
    p.window(17, 6, 3, 10, cross=False)
    p.rect(13, 50, 1, 5, "iron")
    return p


def church():
    p = Painter()
    p.rect(1, 0, 24, 18, "trim")
    p.rect(1, 0, 24, 1, "trimdk")
    p.roof(1, 18, 24, "roof", 9)
    p.rect(8, 0, 10, 30, "trim")
    p.rect(8, 0, 1, 30, "trimdk")
    p.roof(8, 30, 10, "roof", 5)
    p.rect(12, 35, 2, 8, "iron")             # cross
    p.rect(10, 38, 6, 2, "iron")
    p.rect(11, 0, 4, 9, "door")
    p.rect(12, 9, 2, 1, "door")
    p.rect(11, 15, 4, 8, "glass")
    p.rect(12, 15, 2, 1, "red")
    p.rect(11, 25, 4, 4, "door")             # bell opening
    p.rect(3, 6, 3, 7, "glass")
    p.rect(20, 6, 3, 7, "glass")
    return p


# --------------------------------------------------------------------------- empty lots

def cactus():
    p = Painter()
    p.rect(9, 0, 3, 15, "green")
    p.rect(9, 0, 1, 15, "greenlt")
    p.rect(5, 6, 4, 2, "green")
    p.rect(5, 6, 2, 6, "green")
    p.rect(12, 4, 4, 2, "green")
    p.rect(14, 4, 2, 7, "green")
    p.rect(1, 0, 3, 2, "plank")
    p.rect(17, 0, 4, 1, "plank")
    return p


def post():
    p = Painter()
    p.rect(3, 0, 2, 9, "wood1")
    p.rect(19, 0, 2, 9, "wood1")
    p.rect(2, 6, 20, 2, "wood2")
    p.rect(2, 3, 20, 1, "wood2")
    p.rect(8, 0, 8, 3, "plank")
    p.rect(9, 2, 6, 1, "glass")
    return p


def wagon():
    p = Painter()
    p.rect(2, 7, 21, 4, "wood2")
    p.rect(2, 7, 21, 1, "plank")
    p.rect(4, 11, 17, 5, "trim")
    p.rect(6, 16, 13, 1, "trim")
    p.rect(4, 11, 1, 5, "trimdk")
    p.rect(20, 11, 1, 5, "trimdk")
    p.rect(21, 4, 4, 1, "plank")             # shaft
    for wx in (3, 15):
        p.rect(wx + 1, 0, 5, 1, "plank")
        p.rect(wx + 1, 6, 5, 1, "plank")
        p.rect(wx, 1, 1, 5, "plank")
        p.rect(wx + 6, 1, 1, 5, "plank")
        p.rect(wx + 3, 1, 1, 5, "wood1")
        p.rect(wx + 1, 3, 5, 1, "wood1")
    return p


def barrels():
    p = Painter()
    for x in (3, 10):
        p.rect(x, 0, 6, 8, "wood1")
        p.rect(x, 2, 6, 1, "iron")
        p.rect(x, 5, 6, 1, "iron")
    p.rect(6, 8, 6, 7, "wood2")
    p.rect(6, 10, 6, 1, "iron")
    p.rect(6, 13, 6, 1, "iron")
    p.rect(17, 0, 5, 5, "hay")
    p.rect(17, 4, 5, 1, "wood3")
    return p


def well():
    p = Painter()
    p.rect(5, 0, 16, 7, "stone")
    for y in (2, 4):
        p.rect(5, y, 16, 1, "stonedk")
    for x in (9, 14, 18):
        p.rect(x, 0, 1, 7, "stonedk")
    p.rect(6, 7, 2, 10, "wood1")
    p.rect(18, 7, 2, 10, "wood1")
    p.roof(4, 17, 18, "roof", 4)
    p.rect(12, 9, 1, 8, "plank")
    p.rect(11, 6, 3, 3, "wood2")
    return p


# --------------------------------------------------------------------------- landmark

def water_tower():
    p = Painter()
    for x in (2, 14):
        p.rect(x, 0, 2, 34, "wood1")
    for i in range(14):                       # cross bracing
        p.pix(4 + i // 2 * 1, 8 + i, "plank")
        p.pix(13 - i // 2 * 1, 8 + i, "plank")
    p.rect(0, 34, 18, 12, "wood2")
    p.rect(0, 36, 18, 1, "iron")
    p.rect(0, 41, 18, 1, "iron")
    p.rect(0, 34, 2, 12, "wood3")
    p.roof(1, 46, 16, "roof", 5)
    p.rect(8, 51, 2, 3, "iron")
    return p


SPRITES = {
    "cabin": cabin, "barn": barn, "stable": stable, "shack": shack, "townhouse": townhouse,
    "saloon": saloon, "store": store, "blacksmith": blacksmith, "hotel": hotel,
    "grand hotel": grand_hotel, "sheriff": sheriff, "bank": bank, "church": church,
    "cactus": cactus, "post": post, "wagon": wagon, "barrels": barrels, "well": well,
    "water tower": water_tower,
}


def build(kind):
    return SPRITES[kind]()
