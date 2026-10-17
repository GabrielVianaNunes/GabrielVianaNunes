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
        self.assertIsNone(season_art.get("easter"))
        self.assertIsNone(season_art.get("easter", drafts=True))

    def test_a_draft_can_be_previewed_but_is_never_live(self):
        season_art.DRAFT_MODULES["draft-test"] = "christmas"            # stands in for a design waiting for approval
        try:
            self.assertIsNone(season_art.get("draft-test"))                     # not approved: never built
            self.assertEqual(season_art.get("draft-test", drafts=True).id, "christmas")
            self.assertFalse(set(season_art.MODULES) & set(season_art.DRAFT_MODULES))
        finally:
            del season_art.DRAFT_MODULES["draft-test"]
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


if __name__ == "__main__":
    unittest.main()
