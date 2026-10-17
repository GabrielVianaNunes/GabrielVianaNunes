import json
import os
import random
import sys
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import town_layout as tl  # noqa: E402


def weeks(totals):
    return [{"start": "2025-01-%02d" % (i + 1), "total": t} for i, t in enumerate(totals)]


def count(layout, kind):
    return sum(1 for lot in layout["lots"] if lot["kind"] == kind)


def check_rules(tc, layout):
    tc.assertLessEqual(count(layout, "sheriff"), 1)
    tc.assertLessEqual(count(layout, "bank"), 1)
    tc.assertLessEqual(count(layout, "church"), 2)
    for lot in layout["lots"]:
        tc.assertEqual(lot["tier"] == 0, lot["kind"] in tl.EMPTY_DECOR)


class Thresholds(unittest.TestCase):
    def test_uses_only_non_empty_weeks(self):
        self.assertEqual(tl.thresholds([0, 0, 0, 0, 10, 20, 30, 40]), (20, 30, 40))

    def test_all_zero(self):
        self.assertEqual(tl.thresholds([0, 0]), (0, 0, 0))

    def test_tiers(self):
        th = (10, 39, 73)
        got = [tl.tier_of(t, th) for t in (0, 1, 10, 11, 39, 40, 73, 74, 238)]
        self.assertEqual(got, [0, 1, 1, 2, 2, 3, 3, 4, 4])


class RealData(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "data", "contributions-fixture.json"), encoding="utf-8") as f:
            self.weeks = json.load(f)["weeks"]
        self.layout = tl.build_layout(self.weeks)

    def test_one_lot_per_week_oldest_first(self):
        self.assertEqual(len(self.layout["lots"]), len(self.weeks))
        self.assertEqual([l["start"] for l in self.layout["lots"]], [w["start"] for w in self.weeks])

    def test_rows_split_older_half_back_newer_front(self):
        rows = [l["row"] for l in self.layout["lots"]]
        self.assertEqual(rows.count("back"), len(self.weeks) // 2)
        self.assertEqual(rows, sorted(rows, key=lambda r: r == "front"))

    def test_unique_rules_and_exact_counts(self):
        check_rules(self, self.layout)
        self.assertEqual(count(self.layout, "sheriff"), 1)
        self.assertEqual(count(self.layout, "bank"), 1)
        self.assertGreaterEqual(count(self.layout, "church"), 1)

    def test_peak_is_the_busiest_week_and_current_is_last(self):
        totals = [w["total"] for w in self.weeks]
        self.assertEqual(totals[self.layout["peak"]], max(totals))
        self.assertEqual(self.layout["current"], len(self.weeks) - 1)

    def test_deterministic(self):
        self.assertEqual(tl.build_layout(self.weeks), tl.build_layout(self.weeks))

    def test_busy_weeks_are_never_plain_houses(self):
        for lot in self.layout["lots"]:
            if lot["tier"] >= 3:
                self.assertNotIn(lot["kind"], ("cabin", "townhouse", "barn", "stable", "shack"))

    def test_mirrored_lots_have_no_text(self):
        for lot in self.layout["lots"]:
            if lot["mirror"]:
                self.assertIn(lot["kind"], tl.MIRRORABLE)


class EdgeCases(unittest.TestCase):
    def test_all_empty(self):
        lay = tl.build_layout(weeks([0] * 10))
        self.assertIsNone(lay["peak"])
        check_rules(self, lay)
        self.assertTrue(all(l["tier"] == 0 for l in lay["lots"]))

    def test_no_weeks(self):
        lay = tl.build_layout([])
        self.assertEqual(lay["lots"], [])
        self.assertIsNone(lay["current"])

    def test_single_active_week_does_not_crash(self):
        lay = tl.build_layout(weeks([0, 0, 7, 0]))
        check_rules(self, lay)
        self.assertEqual(lay["peak"], 2)

    def test_equal_weeks_follow_the_rules_and_have_no_bank(self):
        # every week is tier 1, so nothing was "big" enough to deserve a bank
        lay = tl.build_layout(weeks([5] * 12))
        check_rules(self, lay)
        self.assertEqual(count(lay, "bank"), 0)
        self.assertTrue(all(l["tier"] == 1 for l in lay["lots"]))

    def test_caps_the_number_of_lots(self):
        lay = tl.build_layout(weeks([1] * 100))
        self.assertEqual(len(lay["lots"]), tl.MAX_LOTS)

    def test_rules_hold_for_many_random_years(self):
        rnd = random.Random(2026)
        for _ in range(400):
            n = rnd.randrange(1, 61)
            totals = [rnd.choice([0, 0, 0, rnd.randrange(1, 300)]) for _ in range(n)]
            check_rules(self, tl.build_layout(weeks(totals)))


if __name__ == "__main__":
    unittest.main()
