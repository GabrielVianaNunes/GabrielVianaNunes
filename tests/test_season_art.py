import datetime
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_assets as ba  # noqa: E402
import season_art  # noqa: E402
from season_art import Layers  # noqa: E402

MAX_BYTES = 150000


def committed(name):
    with open(os.path.join(ROOT, "assets", name), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def parse(svg):
    return ET.fromstring(svg)


class DefaultLookIsUntouched(unittest.TestCase):
    """With no season the builders must give exactly what is committed, so the profile never changes by accident."""

    def test_banner(self):
        self.assertEqual(ba.build_banner(), committed("banner.svg"))
        self.assertEqual(ba.build_banner(None), committed("banner.svg"))

    def test_footer(self):
        self.assertEqual(ba.build_footer(), committed("footer-dusk.svg"))

    def test_poster(self):
        self.assertEqual(ba.build_wanted(), committed("wanted.svg"))

    def test_the_town_divider_is_the_normal_divider_without_a_season(self):
        self.assertEqual(ba.build_strip(None), committed("divider.svg"))

    def test_a_season_with_no_layers_changes_nothing(self):
        class Quiet(season_art.Decor):
            pass
        self.assertEqual(ba.build_banner(Quiet()), committed("banner.svg"))
        self.assertEqual(ba.build_footer(Quiet()), committed("footer-dusk.svg"))
        self.assertEqual(ba.build_wanted(Quiet()), committed("wanted.svg"))


class Registry(unittest.TestCase):
    def test_known_and_unknown_seasons(self):
        self.assertEqual(season_art.get("halloween").id, "halloween")
        self.assertIsNone(season_art.get("no-such-season"))
        self.assertIsNone(season_art.get("no-such-season", drafts=True))

    def test_a_draft_can_be_previewed_but_is_never_live(self):
        class Fake(season_art.Decor):                                   # stands in for a design waiting for approval
            id = "draft-test"
        season_art._load()["draft-test"] = Fake()
        try:
            self.assertEqual(Fake.status, "draft")                              # the default is the safe one
            self.assertIsNone(season_art.get("draft-test"))                     # not approved: never built
            self.assertEqual(season_art.get("draft-test", drafts=True).id, "draft-test")
            self.assertIn("draft-test", season_art.ids("draft"))
        finally:
            del season_art._load()["draft-test"]

    def test_the_approved_seasons_are_exactly_the_ones_the_owner_approved(self):
        self.assertEqual(season_art.ids("approved"), ["birthday", "christmas", "easter", "halloween", "new-year"])

    def test_every_season_with_art_is_a_season_in_the_calendar(self):
        import seasons
        calendar_ids = {s["id"] for s in seasons.load_config()["seasons"]}
        self.assertLessEqual(set(season_art.ids()), calendar_ids)
        self.assertIsNone(season_art.get("nope"))

    def test_layers_reject_unknown_fields(self):
        with self.assertRaises(TypeError):
            Layers(colour="red")


class HalloweenAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = season_art.get("halloween")
        cls.svgs = {"banner": ba.build_banner(d), "footer": ba.build_footer(d),
                    "poster": ba.build_wanted(d), "strip": ba.build_strip(d)}

    def test_every_asset_is_valid_xml_and_within_budget(self):
        for name, svg in self.svgs.items():
            with self.subTest(name):
                parse(svg)
                self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)

    def test_no_scripts_or_external_references(self):
        for name, svg in self.svgs.items():
            with self.subTest(name):
                self.assertIsNone(re.search(r"<script|<image|<foreignObject|https?://(?!www\.w3\.org)|javascript:|xlink:href", svg))

    def test_motion_stops_with_reduced_motion(self):
        for name, svg in self.svgs.items():
            with self.subTest(name):
                self.assertIn("prefers-reduced-motion: reduce", svg)

    def test_each_asset_really_differs_from_the_default(self):
        self.assertNotEqual(self.svgs["banner"], committed("banner.svg"))
        self.assertNotEqual(self.svgs["footer"], committed("footer-dusk.svg"))
        self.assertNotEqual(self.svgs["poster"], committed("wanted.svg"))
        self.assertNotEqual(self.svgs["strip"], committed("divider.svg"))

    def test_the_banner_keeps_its_name_and_role_text(self):
        # the decoration must not cover the identity: the title paths are the same in both versions
        default = committed("banner.svg")
        title = re.findall(r'<path fill="#fff3d6"[^>]*/>', default)
        self.assertTrue(title)
        for path in title:
            self.assertIn(path, self.svgs["banner"])

    def test_the_footer_text_and_label_change(self):
        self.assertIn("Spooky trails", self.svgs["footer"])
        self.assertIn("Halloween decoration", self.svgs["banner"])

    def test_the_banner_has_the_moon_bats_pumpkins_and_the_ghost_rider(self):
        b = self.svgs["banner"]
        self.assertIn('class="bat"', b)
        self.assertIn('class="flk"', b)          # glowing jack o'lanterns
        self.assertIn("#ffa63d", b)              # the harvest moon and the glowing horse eye
        self.assertIn("#f3ead2", b)              # the skull of the skeleton rider

    def test_the_strip_has_exactly_the_size_of_the_divider_it_replaces(self):
        strip, divider = parse(self.svgs["strip"]), parse(committed("divider.svg"))
        for attr in ("width", "height", "viewBox"):
            self.assertEqual(strip.get(attr), divider.get(attr))

    def test_deterministic(self):
        d = season_art.get("halloween")
        self.assertEqual(self.svgs["banner"], ba.build_banner(d))
        self.assertEqual(self.svgs["poster"], ba.build_wanted(d))


class ChristmasDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import season_art.christmas as xm
        cls.xm = xm
        cls.deco = season_art.get("christmas", drafts=True)

    def test_the_santa_cap_is_never_cut_off_by_the_top_of_the_footer(self):
        cap = self.xm.santa_cap()
        # the rider stands at y 22 in the 30 pixel high footer, so row -22 is the top row, row 0
        self.assertGreaterEqual(min(y for _, y in cap.px), -23)

    def test_the_cap_stays_inside_the_footer_in_both_frames_of_the_bob_animation(self):
        """The rider moves up 1 pixel on every other step (the bob keyframes), so check that frame too."""
        import re as _re
        css = ba.STYLE_COMMON
        bob = int(_re.search(r"@keyframes bob\{0%\{transform:translateY\(0\)\}50%\{transform:translateY\((-?\d+)px\)", css).group(1))
        dy = self.deco.footer().rider_dy
        top = 22 + dy + min(y for _, y in self.xm.santa_cap().px) + bob       # topmost pixel row, raised frame
        self.assertGreaterEqual(top, 0)
        self.assertLessEqual(22 + dy, 24)                                     # and the hooves are at most 2 pixels into the sand

    def test_the_default_footer_rider_does_not_move(self):
        self.assertIn('translate(100 22)', ba.build_footer())
        self.assertIn('translate(100 24)', ba.build_footer(self.deco))

    def test_the_cap_replaces_the_cowboy_hat_instead_of_sitting_on_it(self):
        common = ba.rider()[0]
        hat_pixels = {(x, y) for (x, y), c in common.px.items() if c == ba.INK and -22 <= y <= -20 and 4 <= x <= 10}
        self.assertTrue(hat_pixels)
        self.assertLessEqual(hat_pixels - set(self.xm.santa_cap().px), set())      # every hat pixel is covered

    def test_the_portrait_hat_is_replaced_with_a_santa_cap(self):
        default, santa = ba.Grid(), ba.Grid()
        ba.draw_cowboy(default, 31, 35)
        ba.draw_cowboy(santa, 31, 35, headwear=self.xm.portrait_headwear)
        tip = (31 + 29 - 19, 35 + 13)                      # the upturned left tip of the cowboy hat's brim
        self.assertEqual(default.px[tip], "#5a3a22")
        self.assertNotEqual(santa.px[tip], "#5a3a22")
        reds = [1 for c in santa.px.values() if c == self.xm.RED]
        self.assertGreater(len(reds), 40)

    def test_the_poster_has_a_garland_on_all_four_edges(self):
        g, lights = self.xm.pine_garland_border(120, 156)
        greens = {c for c in (self.xm.GREEN, self.xm.DARK_GREEN)}

        def has_green(x0, x1, y0, y1):
            return any(g.px.get((x, y)) in greens for x in range(x0, x1) for y in range(y0, y1))
        self.assertTrue(has_green(40, 80, 0, 6))            # top
        self.assertTrue(has_green(40, 80, 150, 156))        # bottom
        self.assertTrue(has_green(0, 6, 60, 100))           # left
        self.assertTrue(has_green(114, 120, 60, 100))       # right
        self.assertIn("tw1", lights)

    def test_the_garland_leaves_the_text_and_the_portrait_alone(self):
        g, _ = self.xm.pine_garland_border(120, 156)
        for (x, y) in g.px:
            inside_text_or_portrait = 12 <= x <= 107 and 12 <= y <= 144
            self.assertFalse(inside_text_or_portrait, (x, y))

    def test_the_christmas_assets_are_valid_and_the_footer_text_changes(self):
        footer = ba.build_footer(self.deco)
        parse(footer)
        self.assertIn("Merry trails", footer)
        for svg in (ba.build_banner(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            parse(svg)
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)


class BirthdayDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import season_art.birthday as bd
        cls.bd = bd
        cls.deco = season_art.get("birthday", drafts=True)

    def test_it_is_an_approved_season_now(self):
        self.assertEqual(season_art.get("birthday").id, "birthday")
        self.assertIsNotNone(self.deco)

    def test_the_crown_replaces_the_hat_and_stays_inside_the_footer_in_the_raised_frame(self):
        crown, _ = self.bd.crown_and_horse_hat()
        common = ba.rider()[0]
        hat_pixels = {(x, y) for (x, y), c in common.px.items() if c == ba.INK and -22 <= y <= -20 and 4 <= x <= 10}
        self.assertEqual(hat_pixels - set(crown.px), set())
        dy = self.deco.footer().rider_dy
        self.assertGreaterEqual(22 + dy + min(y for _, y in crown.px) - 1, 0)      # -1 is the raised frame of the bob

    def test_the_strip_has_the_size_of_the_divider_and_spells_the_greeting(self):
        strip, divider = parse(ba.build_strip(self.deco)), parse(committed("divider.svg"))
        for attr in ("width", "height", "viewBox"):
            self.assertEqual(strip.get(attr), divider.get(attr))
        svg = ba.build_strip(self.deco)
        for color in self.bd.FLAGS:
            self.assertIn(color, svg)

    def test_the_footer_says_happy_birthday(self):
        self.assertIn("Happy birthday", ba.build_footer(self.deco))

    def test_privacy_no_year_or_age_in_any_text_of_any_asset(self):
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            texts = re.findall(r'aria-label="([^"]*)"', svg) + re.findall(r"<title>([^<]*)</title>", svg)
            for text in texts:
                self.assertIsNone(re.search(r"\d", text), text)

    def test_the_poster_balloons_stay_in_the_free_left_margin(self):
        for x, y, color, string_to, delay in self.bd.POSTER_BALLOONS:
            px = self.bd.balloon(x, y, color, string_to).px
            self.assertLessEqual(max(px_x for px_x, _ in px), 8)                    # the text starts at x 9

    def test_there_is_a_touch_of_christmas(self):
        banner = ba.build_banner(self.deco)
        self.assertIn("#2f6b3f", banner)                                          # the tree
        self.assertIn("#f4f8ff", banner)                                          # snow on the ground

    def test_every_asset_is_valid_and_within_budget(self):
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            parse(svg)
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)


class NewYearDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import season_art.newyear as ny
        cls.ny = ny
        cls.deco = season_art.get("new-year", drafts=True).with_date(datetime.date(2026, 12, 31))

    def test_it_is_an_approved_season_now(self):
        self.assertEqual(season_art.get("new-year").id, "new-year")
        self.assertIsNotNone(season_art.get("new-year", drafts=True))

    def test_the_number_is_the_year_that_begins(self):
        n = self.ny.new_year_number
        D = datetime.date
        self.assertEqual(n(D(2026, 12, 31)), 2027)
        self.assertEqual(n(D(2027, 1, 1)), 2027)
        self.assertEqual(n(D(2099, 12, 31)), 2100)
        self.assertEqual(n(D(2030, 6, 15)), 2030)

    def test_the_date_reaches_the_art_without_touching_the_shared_object(self):
        proto = season_art.get("new-year", drafts=True)
        a = proto.with_date(datetime.date(2026, 12, 31))
        b = proto.with_date(datetime.date(2027, 1, 1))
        self.assertEqual((a.year, b.year), (2027, 2027))
        c = proto.with_date(datetime.date(2099, 12, 31))
        self.assertEqual(c.year, 2100)
        self.assertEqual(a.year, 2027)                                          # an earlier copy is not changed

    def test_the_year_is_written_in_the_assets(self):
        self.assertIn("2027", self.deco.strip().label)
        self.assertIn("2027", self.deco.banner().label)
        self.assertGreater(len(self.ny.digits_grid(2027, 172, 4, self.ny.GOLD).px), 40)
        self.assertLessEqual(172 + 4 * 6 - 1, 199)                                  # the number fits inside the banner

    def test_every_glyph_is_rectangular_and_the_bunting_fits_the_divider(self):
        for ch, rows in self.ny.GLYPHS.items():
            self.assertEqual(len(rows), 5, ch)
            self.assertEqual(len({len(r) for r in rows}), 1, ch)
        for year in (2027, 2100, 2999):
            items, total = self.ny.bunting_layout("HAPPY NEW YEAR %d" % year)
            self.assertLessEqual(total, 150)
            self.assertGreaterEqual(items[0][1], 2)
            self.assertEqual(len(items), len("HAPPYNEWYEAR") + 4)

    def test_the_gold_hat_replaces_the_cowboy_hat_and_stays_inside_the_footer(self):
        hat, spark = self.ny.golden_hat_extra()
        common = ba.rider()[0]
        hat_pixels = {(x, y) for (x, y), c in common.px.items() if c == ba.INK and -22 <= y <= -20 and 4 <= x <= 10}
        self.assertEqual(hat_pixels - set(hat.px), set())
        dy = self.deco.footer().rider_dy
        lowest_row = min(y for _, y in list(hat.px) + list(spark.px))
        self.assertGreaterEqual(22 + dy + lowest_row - 1, 0)                         # the raised frame of the bob

    def test_the_poster_portrait_gets_a_top_hat_instead_of_the_cowboy_hat(self):
        default, ny = ba.Grid(), ba.Grid()
        ba.draw_cowboy(default, 31, 35)
        ba.draw_cowboy(ny, 31, 35, headwear=self.ny.top_hat_headwear)
        tip = (31 + 29 - 19, 35 + 13)
        self.assertEqual(default.px[tip], "#5a3a22")
        self.assertNotEqual(ny.px[tip], "#5a3a22")

    def test_the_strip_has_the_size_of_the_divider(self):
        strip, divider = parse(ba.build_strip(self.deco)), parse(committed("divider.svg"))
        for attr in ("width", "height", "viewBox"):
            self.assertEqual(strip.get(attr), divider.get(attr))

    def test_every_burst_has_five_frames_one_of_them_kept_for_reduced_motion(self):
        svg = self.ny.fireworks([(24, 36, 0, 0)])
        self.assertEqual(svg.count('class="fwf'), 5)
        self.assertEqual(svg.count("fwlast"), 1)

    def test_the_footer_says_happy_new_year_and_everything_is_valid(self):
        self.assertIn("Happy new year", ba.build_footer(self.deco))
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            parse(svg)
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)


class EasterDraft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import season_art.easter as ea
        import season_art.kit as kit
        cls.ea, cls.kit = ea, kit
        cls.deco = season_art.get("easter", drafts=True)

    def test_it_is_an_approved_season_now(self):
        self.assertEqual(self.deco.status, "approved")
        self.assertEqual(season_art.get("easter").id, "easter")

    def test_the_bonnet_replaces_the_cowboy_hat_and_stays_inside_the_footer_in_the_raised_frame(self):
        hat, garland = self.ea.bonnet_and_garland()
        self.assertEqual(self.kit.covers_hat(hat.px, ba.rider()[0], ba.INK), set())
        dy = self.deco.footer().rider_dy
        top = min(y for _, y in list(hat.px) + list(garland.px))
        self.assertGreaterEqual(22 + dy + top - 1, 0)                              # the raised frame of the bob animation

    def test_the_horse_keeps_its_own_ears_and_only_gets_a_garland_on_its_neck(self):
        """The owner wants the standard ears (no long bunny ears) and kept the flower garland on the neck."""
        hat, garland = self.ea.bonnet_and_garland()
        self.assertEqual({(x, y) for x, y in hat.px if x >= 11}, set())                  # the bonnet stays on the rider
        head_zone = {(x, y) for x in range(14, 20) for y in range(-19, -13)}              # where the ears are and were
        self.assertEqual(head_zone & set(garland.px), set())                              # nothing covers or replaces the ears
        self.assertTrue(garland.px)
        self.assertTrue(all(12 <= x <= 14 and -12 <= y <= -8 for x, y in garland.px))     # only on the neck
        common = ba.rider()[0]
        for ear in ((15, -14), (16, -14)):
            self.assertEqual(common.px[ear], ba.INK)                                       # the default ear pixels remain

    def test_the_poster_portrait_gets_a_bonnet_instead_of_the_cowboy_hat(self):
        default, easter = ba.Grid(), ba.Grid()
        ba.draw_cowboy(default, 31, 35)
        ba.draw_cowboy(easter, 31, 35, headwear=self.ea.bonnet_headwear)
        tip = (31 + 29 - 19, 35 + 13)
        self.assertEqual(default.px[tip], "#5a3a22")
        self.assertNotEqual(easter.px[tip], "#5a3a22")

    def test_the_poster_decorations_stay_clear_of_the_text(self):
        for x, yb, base, accent, style in ((2, 118, self.ea.PINK, self.ea.LILAC, "stripe"), (3, 125, self.ea.BLUE, self.ea.YELLOW, "dots"),
                                           (2, 132, self.ea.MINT, self.ea.PINK, "zig")):
            self.assertLessEqual(max(px for px, _ in self.ea.egg(x, yb, base, accent, style).px), 8)      # the text starts at x 9
        chick = self.ea.chick(82, 98).px
        self.assertLess(max(y for _, y in chick), 101)                                  # the first line of text starts at y 101

    def test_the_strip_has_the_size_of_the_divider_and_spells_the_greeting(self):
        strip, divider = parse(ba.build_strip(self.deco)), parse(committed("divider.svg"))
        for attr in ("width", "height", "viewBox"):
            self.assertEqual(strip.get(attr), divider.get(attr))
        items, total = self.kit.text_layout("HAPPY EASTER")
        self.assertEqual(len(items), 11)
        self.assertLessEqual(total, 150)

    def test_every_glyph_used_exists_and_is_rectangular(self):
        for ch in "HAPY EST R":
            if ch != " ":
                rows = self.kit.GLYPHS[ch]
                self.assertEqual(len(rows), 5)
                self.assertEqual(len({len(r) for r in rows}), 1)

    def test_the_footer_says_happy_easter_and_everything_is_valid(self):
        self.assertIn("Happy easter", ba.build_footer(self.deco))
        for svg in (ba.build_banner(self.deco), ba.build_footer(self.deco), ba.build_wanted(self.deco), ba.build_strip(self.deco)):
            parse(svg)
            self.assertLess(len(svg.encode("utf-8")), MAX_BYTES)
            self.assertIsNone(re.search(r"<script|<image|https?://(?!www\.w3\.org)", svg))

    def test_the_build_uses_it_inside_its_window(self):
        import build_seasonal as bs
        files, deco = bs.build("easter", datetime.date(2027, 3, 28))
        self.assertIsNotNone(deco)
        self.assertNotEqual(files["banner.svg"], committed("banner.svg"))


if __name__ == "__main__":
    unittest.main()
