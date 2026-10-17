import datetime
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import seasons as se  # noqa: E402

D = datetime.date
EASTER = {
    2023: D(2023, 4, 9), 2024: D(2024, 3, 31), 2025: D(2025, 4, 20), 2026: D(2026, 4, 5),
    2027: D(2027, 3, 28), 2028: D(2028, 4, 16), 2029: D(2029, 4, 1), 2030: D(2030, 4, 21),
    2031: D(2031, 4, 13), 2032: D(2032, 3, 28), 2033: D(2033, 4, 17), 2034: D(2034, 4, 9),
    2035: D(2035, 3, 25), 2036: D(2036, 4, 13), 2037: D(2037, 4, 5), 2038: D(2038, 4, 25),
    2039: D(2039, 4, 10), 2040: D(2040, 4, 1),
}


def cfg():
    return se.load_config()


def on(day):
    s = se.active_season(day, cfg())
    return s["id"] if s else None


class DateMath(unittest.TestCase):
    def test_easter_matches_the_known_table_for_2023_to_2040(self):
        for year, expected in EASTER.items():
            with self.subTest(year):
                self.assertEqual(se.easter_date(year), expected)

    def test_easter_is_always_a_sunday_in_march_or_april(self):
        for year in range(1900, 2200):
            e = se.easter_date(year)
            self.assertEqual(e.weekday(), 6)
            self.assertIn(e.month, (3, 4))

    def test_fourth_saturday_of_july(self):
        self.assertEqual(se.nth_weekday(2026, 7, 5, 4), D(2026, 7, 25))
        self.assertEqual(se.nth_weekday(2027, 7, 5, 4), D(2027, 7, 24))
        self.assertEqual(se.nth_weekday(2028, 7, 5, 4), D(2028, 7, 22))

    def test_fifth_weekday_can_be_missing(self):
        self.assertIsNone(se.nth_weekday(2027, 2, 0, 5))

    def test_day_256_is_13_sep_or_12_sep_in_leap_years(self):
        self.assertEqual(se.day_of_year(2027, 256), D(2027, 9, 13))
        self.assertEqual(se.day_of_year(2028, 256), D(2028, 9, 12))
        self.assertIsNone(se.day_of_year(2027, 366))
        self.assertEqual(se.day_of_year(2028, 366), D(2028, 12, 31))


class OwnerWindows(unittest.TestCase):
    def test_default_look_outside_any_window(self):
        for d in (D(2026, 1, 10), D(2026, 6, 15), D(2026, 10, 23), D(2026, 12, 26), D(2026, 12, 27),
                  D(2026, 12, 29), D(2026, 12, 30), D(2027, 1, 2)):
            with self.subTest(d):
                self.assertIsNone(on(d))

    def test_halloween_window(self):
        self.assertEqual(on(D(2026, 10, 24)), "halloween")
        self.assertEqual(on(D(2026, 10, 31)), "halloween")
        self.assertEqual(on(D(2026, 11, 2)), "halloween")

    def test_christmas_starts_when_halloween_ends_and_stops_on_the_25th(self):
        self.assertEqual(on(D(2026, 11, 3)), "christmas")
        self.assertEqual(on(D(2026, 12, 1)), "christmas")
        self.assertEqual(on(D(2026, 12, 25)), "christmas")

    def test_halloween_and_christmas_chain_without_a_gap(self):
        self.assertEqual((on(D(2026, 11, 2)), on(D(2026, 11, 3))), ("halloween", "christmas"))

    def test_birthday_is_only_the_28th(self):
        self.assertIsNone(on(D(2026, 12, 27)))
        self.assertEqual(on(D(2026, 12, 28)), "birthday")
        self.assertIsNone(on(D(2026, 12, 29)))

    def test_new_year_crosses_the_year_and_is_two_days(self):
        self.assertIsNone(on(D(2026, 12, 30)))
        self.assertEqual(on(D(2026, 12, 31)), "new-year")
        self.assertEqual(on(D(2027, 1, 1)), "new-year")
        self.assertIsNone(on(D(2027, 1, 2)))

    def test_easter_window_is_seven_days_centred_on_each_years_easter(self):
        for year, easter in EASTER.items():
            for offset in range(-6, 7):
                with self.subTest("%d %+d" % (year, offset)):
                    expected = "easter" if -3 <= offset <= 3 else None
                    self.assertEqual(on(easter + datetime.timedelta(days=offset)), expected)

    def test_easter_2027_is_25_to_31_march(self):
        self.assertIsNone(on(D(2027, 3, 24)))
        self.assertEqual(on(D(2027, 3, 25)), "easter")
        self.assertEqual(on(D(2027, 3, 31)), "easter")
        self.assertIsNone(on(D(2027, 4, 1)))

    def test_cowboy_day_week(self):
        self.assertIsNone(on(D(2027, 7, 20)))
        self.assertEqual(on(D(2027, 7, 21)), "cowboy-day")
        self.assertEqual(on(D(2027, 7, 24)), "cowboy-day")
        self.assertEqual(on(D(2027, 7, 27)), "cowboy-day")
        self.assertIsNone(on(D(2027, 7, 28)))

    def test_programmers_day_follows_the_leap_year(self):
        self.assertEqual([on(D(2027, 9, d)) for d in (11, 12, 13, 14, 15)],
                         [None, "programmers-day", "programmers-day", "programmers-day", None])
        self.assertEqual([on(D(2028, 9, d)) for d in (10, 11, 12, 13, 14)],
                         [None, "programmers-day", "programmers-day", "programmers-day", None])

    def test_every_day_of_several_years_resolves_without_error(self):
        day = D(2024, 1, 1)
        while day < D(2036, 1, 1):
            on(day)
            day += datetime.timedelta(days=1)

    def test_windows_of_year_lists_the_new_year_window_in_both_years(self):
        ids = [w[0] for w in se.windows_of_year(cfg(), 2027)]
        self.assertIn("new-year", ids)                 # the one that ends on 1 Jan 2027
        self.assertEqual(ids.count("new-year"), 2)     # and the one that starts on 31 Dec 2027


class Overlaps(unittest.TestCase):
    def config(self, a_priority, b_priority):
        return se.validate({"seasons": [
            {"id": "a", "name": "A", "priority": a_priority, "rule": {"kind": "range", "start": "05-01", "end": "05-10"}},
            {"id": "b", "name": "B", "priority": b_priority, "rule": {"kind": "day", "date": "05-05"}},
        ]})

    def test_higher_priority_wins(self):
        self.assertEqual(se.active_season(D(2027, 5, 5), self.config(1, 9))["id"], "b")
        self.assertEqual(se.active_season(D(2027, 5, 5), self.config(9, 1))["id"], "a")

    def test_outside_the_overlap_each_one_shows(self):
        self.assertEqual(se.active_season(D(2027, 5, 3), self.config(1, 9))["id"], "a")


class TimeZone(unittest.TestCase):
    def test_the_date_changes_at_midnight_in_sao_paulo_not_in_utc(self):
        utc = datetime.timezone.utc
        c = cfg()
        before = datetime.datetime(2026, 10, 24, 2, 59, tzinfo=utc)
        after = datetime.datetime(2026, 10, 24, 3, 0, tzinfo=utc)
        self.assertEqual(se.today_in_zone(c, before), D(2026, 10, 23))
        self.assertEqual(se.today_in_zone(c, after), D(2026, 10, 24))
        self.assertIsNone(se.active_season(se.today_in_zone(c, before), c))
        self.assertEqual(se.active_season(se.today_in_zone(c, after), c)["id"], "halloween")

    def test_naive_datetimes_are_rejected(self):
        with self.assertRaises(ValueError):
            se.today_in_zone(cfg(), datetime.datetime(2026, 1, 1))


class ConfigValidation(unittest.TestCase):
    def bad(self, season):
        with self.assertRaises(se.ConfigError):
            se.validate({"seasons": [season]})

    def test_rejects_malformed_seasons(self):
        ok = {"id": "x", "name": "X", "rule": {"kind": "day", "date": "01-01"}}
        self.assertEqual(se.validate({"seasons": [ok]})["seasons"][0]["id"], "x")
        self.bad(dict(ok, id="Bad Id"))
        self.bad(dict(ok, name=""))
        self.bad(dict(ok, rule={"kind": "magic"}))
        self.bad(dict(ok, rule={"kind": "day", "date": "13-40"}))
        self.bad(dict(ok, rule={"kind": "range", "start": "1-1", "end": "02-01"}))
        self.bad(dict(ok, rule={"kind": "easter", "before": 99}))
        self.bad(dict(ok, rule={"kind": "easter", "before": -1}))
        self.bad(dict(ok, rule={"kind": "nth_weekday", "month": 7, "weekday": "funday", "n": 1}))
        self.bad(dict(ok, rule={"kind": "day_of_year", "day": 400}))
        self.bad(dict(ok, priority="high"))

    def test_rejects_duplicate_ids_and_a_missing_list(self):
        s = {"id": "x", "name": "X", "rule": {"kind": "day", "date": "01-01"}}
        with self.assertRaises(se.ConfigError):
            se.validate({"seasons": [s, s]})
        with self.assertRaises(se.ConfigError):
            se.validate({})

    def test_changing_a_window_in_the_file_changes_the_result_without_code(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "s.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"seasons": [{"id": "party", "name": "Party",
                                        "rule": {"kind": "range", "start": "03-01", "end": "03-03"}}]}, f)
            c = se.load_config(path)
            self.assertEqual(se.active_season(D(2027, 3, 2), c)["id"], "party")
            self.assertIsNone(se.active_season(D(2027, 3, 4), c))


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = se.main(list(args))
        return code, buf.getvalue().strip()

    def test_prints_the_season_or_default(self):
        self.assertEqual(self.run_cli("--date", "2026-12-28"), (0, "birthday"))
        self.assertEqual(self.run_cli("--date", "2026-06-15"), (0, "default"))

    def test_year_listing(self):
        code, out = self.run_cli("--year", "2027")
        self.assertEqual(code, 0)
        self.assertIn("easter           2027-03-25 to 2027-03-31", out)
        self.assertIn("cowboy-day       2027-07-21 to 2027-07-27", out)

    def test_bad_input_is_an_error_not_a_crash(self):
        import io
        import contextlib
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(se.main(["--date", "nope"]), 1)
            self.assertEqual(se.main(["--config", "does-not-exist.json"]), 1)


if __name__ == "__main__":
    unittest.main()
