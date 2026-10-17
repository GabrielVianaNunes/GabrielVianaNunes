import os
import re
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import town_layout as tl  # noqa: E402
import town_palette as pal  # noqa: E402
import town_sprites as ts  # noqa: E402

MAX_BUILDING_H = 66


class Sprites(unittest.TestCase):
    def test_every_kind_the_layout_can_produce_has_a_sprite(self):
        kinds = set(tl.EMPTY_DECOR) | set(tl.TIER1) | set(tl.TIER2)
        kinds |= {"hotel", "grand hotel", "bank", "church", "sheriff"}
        self.assertEqual(kinds - set(ts.SPRITES), set())

    def test_sizes_fit_their_slot(self):
        for kind in ts.SPRITES:
            with self.subTest(kind):
                w, h = ts.build(kind).size()
                limit = 18 if kind == "water tower" else ts.SLOT_W
                self.assertLessEqual(w, limit)
                self.assertLessEqual(h, 56 if kind == "water tower" else MAX_BUILDING_H)
                self.assertGreaterEqual(h, 8)

    def test_nothing_is_drawn_below_the_ground_or_left_of_the_slot(self):
        for kind in ts.SPRITES:
            with self.subTest(kind):
                p = ts.build(kind)
                self.assertGreaterEqual(min(x for x, _ in p.px), 0)
                self.assertEqual(min(y for _, y in p.px), 0)

    def test_only_palette_classes_are_used(self):
        for kind in ts.SPRITES:
            with self.subTest(kind):
                self.assertLessEqual(set(ts.build(kind).px.values()), set(pal.PALETTE))

    def test_every_pixel_is_connected_to_the_ground(self):
        for kind in ts.SPRITES:
            with self.subTest(kind):
                p = ts.build(kind)
                seen = {(x, y) for (x, y) in p.px if y == 0}
                stack = list(seen)
                while stack:
                    x, y = stack.pop()
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            q = (x + dx, y + dy)
                            if q in p.px and q not in seen:
                                seen.add(q)
                                stack.append(q)
                self.assertEqual(len(seen), len(p.px), "%s has parts that float" % kind)

    def test_signs_carry_text(self):
        for kind in ("saloon", "store", "hotel", "grand hotel", "bank"):
            with self.subTest(kind):
                values = set(ts.build(kind).px.values())
                self.assertTrue({"signtxt", "brass"} & values)

    def test_unique_buildings_are_visibly_special(self):
        self.assertIn("brass", set(ts.build("sheriff").px.values()))      # star
        self.assertIn("iron", set(ts.build("church").px.values()))        # cross

    def test_text_font_has_every_letter_used(self):
        for word in ("SALOON", "STORE", "HOTEL", "BANK"):
            self.assertTrue(set(word) <= set(ts.FONT3), word)

    def test_markup_is_deterministic_and_has_no_external_references(self):
        for kind in ts.SPRITES:
            a, b = ts.build(kind).paths(), ts.build(kind).paths()
            self.assertEqual(a, b)
            self.assertIsNone(re.search(r"https?:|<script|<image|xlink:href", a))

    def test_palette_defines_both_themes_for_every_class(self):
        for cls in pal.PALETTE:
            for theme in ("day", "night"):
                self.assertRegex(pal.color(cls, theme), r"^#[0-9a-f]{6}$")
        self.assertNotEqual(pal.color("glass", "day"), pal.color("glass", "night"))


if __name__ == "__main__":
    unittest.main()
