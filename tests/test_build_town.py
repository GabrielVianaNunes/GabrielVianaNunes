import json
import os
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_town as bt  # noqa: E402
import town_layout as tl  # noqa: E402

SVG = "{http://www.w3.org/2000/svg}"


def fixture_weeks():
    with open(os.path.join(ROOT, "data", "contributions-fixture.json"), encoding="utf-8") as f:
        return json.load(f)["weeks"]


def weeks(totals):
    return [{"start": "2025-01-%02d" % (i + 1), "total": t} for i, t in enumerate(totals)]


class RenderReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.layout = tl.build_layout(fixture_weeks())
        cls.svgs = {t: bt.render(cls.layout, t) for t in ("day", "night")}

    def test_valid_xml_with_the_right_canvas(self):
        for theme, svg in self.svgs.items():
            with self.subTest(theme):
                root = ET.fromstring(svg)
                self.assertEqual(root.tag, SVG + "svg")
                self.assertEqual(root.get("viewBox"), "0 0 %d %d" % (bt.W, bt.H))

    def test_stays_inside_the_size_budget(self):
        for theme, svg in self.svgs.items():
            with self.subTest(theme):
                self.assertLess(len(svg.encode("utf-8")), bt.MAX_BYTES)

    def test_no_scripts_external_references_or_foreign_content(self):
        for theme, svg in self.svgs.items():
            with self.subTest(theme):
                self.assertIsNone(re.search(r"<script|<image|<foreignObject|https?://(?!www\.w3\.org)|xlink:href|javascript:", svg))
                for el in ET.fromstring(svg).iter():
                    for name, value in el.attrib.items():
                        if name.endswith("href"):
                            self.assertTrue(value.startswith("#"), value)

    def test_every_use_points_to_a_defined_symbol(self):
        for theme, svg in self.svgs.items():
            with self.subTest(theme):
                root = ET.fromstring(svg)
                ids = {el.get("id") for el in root.iter(SVG + "symbol")}
                for use in root.iter(SVG + "use"):
                    self.assertIn(use.get("href")[1:], ids)

    def test_all_kinds_in_the_layout_are_defined_and_used(self):
        kinds = {lot["kind"].replace(" ", "-") for lot in self.layout["lots"]} | {"water-tower"}
        for theme, svg in self.svgs.items():
            with self.subTest(theme):
                for k in kinds:
                    self.assertIn('id="s-%s"' % k, svg)
                    self.assertIn('href="#s-%s"' % k, svg)

    def test_accessible_label_has_the_numbers(self):
        for svg in self.svgs.values():
            root = ET.fromstring(svg)
            label = root.get("aria-label")
            self.assertIn(str(self.layout["total"]), label)
            self.assertIn(str(len(self.layout["lots"])), label)
            self.assertEqual(root.get("role"), "img")

    def test_themes_differ_but_share_the_sprites(self):
        day, night = self.svgs["day"], self.svgs["night"]
        self.assertNotEqual(day, night)
        self.assertIn("--glass:#7fb8d6", day)
        self.assertIn("--glass:#f7b867", night)
        self.assertIn(".flick{opacity:0}", day)                  # no flicker by day
        self.assertIn("animation:flick", night)

    def test_animations_and_reduced_motion(self):
        for svg in self.svgs.values():
            self.assertIn("prefers-reduced-motion: reduce", svg)
            self.assertIn("animation:none!important", svg)
            for cls in ("ride", "weed", "cloud", "lamp"):
                self.assertIn('class="%s"' % cls, svg)

    def test_mirrored_lots_are_flipped_and_text_buildings_are_not(self):
        svg = self.svgs["day"]
        self.assertRegex(svg, r"scale\(-")
        texty = {lot["kind"] for lot in self.layout["lots"] if lot["mirror"]}
        self.assertFalse(texty & {"saloon", "store", "hotel", "grand hotel", "bank"})

    def test_deterministic(self):
        self.assertEqual(self.svgs["night"], bt.render(self.layout, "night"))


class EdgeCases(unittest.TestCase):
    def test_all_empty_year(self):
        for theme in ("day", "night"):
            ET.fromstring(bt.render(tl.build_layout(weeks([0] * 20)), theme))

    def test_no_weeks_at_all(self):
        ET.fromstring(bt.render(tl.build_layout([]), "day"))

    def test_one_active_week(self):
        ET.fromstring(bt.render(tl.build_layout(weeks([0, 0, 9, 0])), "night"))

    def test_the_busiest_possible_year_still_fits_the_budget(self):
        layout = tl.build_layout(weeks([(i * 37) % 300 + 1 for i in range(60)]))
        for theme in ("day", "night"):
            self.assertLess(len(bt.render(layout, theme).encode("utf-8")), bt.MAX_BYTES)


class Cli(unittest.TestCase):
    def test_writes_both_files(self):
        with tempfile.TemporaryDirectory() as d:
            code = bt.main(["--input", os.path.join(ROOT, "data", "contributions-fixture.json"), "--out", d])
            self.assertEqual(code, 0)
            self.assertEqual(sorted(os.listdir(d)), ["western-town-day.svg", "western-town-night.svg"])


if __name__ == "__main__":
    unittest.main()
