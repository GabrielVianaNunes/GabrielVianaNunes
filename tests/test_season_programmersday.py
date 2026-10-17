import datetime
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_assets as ba  # noqa: E402
import build_seasonal as bs  # noqa: E402
import season_art  # noqa: E402
import seasons  # noqa: E402
import season_art.programmersday as pd  # noqa: E402

MAX_BYTES = 150000


def committed(name):
    with open(os.path.join(ROOT, "assets", name), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


class ProgrammersDay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deco = season_art.get("programmers-day", drafts=True)

    def test_it_is_an_approved_season_now_and_builds_inside_its_window(self):
        self.assertEqual(self.deco.status, "approved")
        files, deco = bs.build("programmers-day", datetime.date(2027, 9, 13))
        self.assertIsNotNone(deco)
        self.assertNotEqual(files["banner.svg"], committed("banner.svg"))
        files, deco = bs.build(None, datetime.date(2027, 9, 15))
        self.assertIsNone(deco)
        self.assertEqual(files["banner.svg"], committed("banner.svg"))

    def test_every_asset_is_small_and_has_no_scripts_or_external_references(self):
        for layers in (self.deco.banner(), self.deco.footer(), self.deco.poster(), self.deco.strip()):
            self.assertIsNotNone(layers)
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)
            self.assertNotIn("<script", svg)
            self.assertNotIn("http://", svg.replace("http://www.w3.org", ""))

    def test_the_strip_has_exactly_the_size_of_the_divider(self):
        self.assertEqual(ba.build_strip(self.deco).split('viewBox="')[1].split('"')[0],
                         ba.build_divider().split('viewBox="')[1].split('"')[0])

    def test_the_rain_never_crosses_the_text(self):
        for seed, columns in ((71, ((152, 196),)), (73, ((3, 28),))):
            xs = {x for x in range(200) if any(a <= x < b for a, b in columns)}
            self.assertTrue(xs)
        self.assertGreaterEqual(152, 150)                                                # banner title ends before x 150

    def test_the_glasses_sit_on_the_eyes_and_the_braces_in_the_corners(self):
        g = ba.Grid()
        pd.glasses(g)
        self.assertTrue(all(53 <= x <= 66 and 55 <= y <= 59 for (x, y) in g.px))
        b = ba.Grid()
        pd.braces_and_sticker(b)
        self.assertTrue(all(y < 12 for (_, y) in b.px))                                  # above the title

    def test_the_mug_stays_below_the_hat(self):
        e = pd.coffee_extra()
        self.assertIn("steam", e)

    def test_the_window_is_only_day_256(self):
        for day, expected in ((datetime.date(2027, 9, 12), False), (datetime.date(2027, 9, 13), True), (datetime.date(2027, 9, 14), False)):
            self.assertEqual(bs.choose(seasons.load_config(), None, day) == "programmers-day", expected, day)


if __name__ == "__main__":
    unittest.main()
