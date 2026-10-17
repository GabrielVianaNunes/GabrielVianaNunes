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
        self.assertIsNone(season_art.get("christmas"))
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


if __name__ == "__main__":
    unittest.main()
