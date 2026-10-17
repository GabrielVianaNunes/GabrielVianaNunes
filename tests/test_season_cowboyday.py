import datetime
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_assets as ba  # noqa: E402
import build_seasonal as bs  # noqa: E402
import season_art  # noqa: E402
import season_art.cowboyday as cd  # noqa: E402
import season_art.kit as kit  # noqa: E402

MAX_BYTES = 150000


def committed(name):
    with open(os.path.join(ROOT, "assets", name), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


class CowboyDayDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deco = season_art.get("cowboy-day", drafts=True)

    def test_it_is_a_draft_until_approved_and_the_build_ignores_it(self):
        self.assertEqual(self.deco.status, "draft")
        self.assertIsNone(season_art.get("cowboy-day"))
        files, deco = bs.build("cowboy-day", datetime.date(2027, 7, 24))
        self.assertIsNone(deco)
        self.assertEqual(files["banner.svg"], committed("banner.svg"))

    def test_the_cowboy_keeps_his_hat_the_gold_band_only_recolors_part_of_it(self):
        common = ba.rider()[0]
        hat_pixels = {(x, y) for (x, y), c in common.px.items() if c == ba.INK and -22 <= y <= -20 and 4 <= x <= 10}
        band = cd.gold_band()
        self.assertTrue(band.px)
        self.assertLessEqual(set(band.px), hat_pixels)                                  # no pixel outside the hat

    def test_the_lasso_stays_inside_the_footer_in_the_raised_frame_and_only_gets_flatter(self):
        rope, loop = cd.rope_loop()
        dy = self.deco.footer().rider_dy
        top = min(y for _, y in list(rope.px) + list(loop.px))
        self.assertGreaterEqual(22 + dy + top - 1, 0)                                   # -1 is the raised frame of the bob
        scales = [float(s) for s in re.findall(r"scaleY\(([0-9.]+)\)", self.deco.banner().css)]
        self.assertTrue(scales)
        self.assertLessEqual(max(scales), 1.0)                                          # it never gets taller than at rest

    def test_the_poster_decorations_sit_where_they_should(self):
        g = ba.Grid()
        cd.star_and_rosette(g)
        inside_frame = lambda x, y: 31 <= x <= 88 and 35 <= y <= 92
        self.assertTrue(all(inside_frame(x, y) for (x, y) in g.px))                     # star and rosette inside the portrait frame
        b = ba.Grid()
        cd.poster_bunting(b)
        self.assertLess(max(y for _, y in b.px), 12)                                    # above the title, which starts at y 12
        for x, yb in ((3, 150), (113, 150)):
            self.assertGreater(min(y for _, y in cd.horseshoe(x, yb).px), 144)          # below the last line of text

    def test_the_strip_has_the_size_of_the_divider_and_spells_the_greeting_in_patriotic_colors(self):
        svg = ba.build_strip(self.deco)
        strip, divider = ET.fromstring(svg), ET.fromstring(committed("divider.svg"))
        for attr in ("width", "height", "viewBox"):
            self.assertEqual(strip.get(attr), divider.get(attr))
        items, total = kit.text_layout("HAPPY COWBOY DAY")
        self.assertEqual(len(items), 14)
        self.assertLessEqual(total, 150)
        for color in (cd.RED, cd.BLUE, cd.SNOW):
            self.assertIn(color, svg)

    def test_every_letter_used_exists(self):
        for ch in "HAPY COWBD":
            if ch != " ":
                self.assertIn(ch, kit.GLYPHS)

    def test_the_footer_says_happy_cowboy_day_with_the_rider_lowered(self):
        footer = ba.build_footer(self.deco)
        self.assertIn("Happy cowboy day", footer)
        self.assertIn("translate(100 24)", footer)

    def test_the_ground_objects_are_outlined_so_they_stand_out_from_the_ground(self):
        barrel = cd.barrel(68, 58)
        self.assertIn("#1d1008", set(barrel.px.values()))

    def test_every_asset_is_valid_small_and_safe(self):
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            ET.fromstring(svg)
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)
            self.assertIsNone(re.search(r"<script|<image|https?://(?!www\.w3\.org)", svg))
            self.assertIn("prefers-reduced-motion", svg)


if __name__ == "__main__":
    unittest.main()
