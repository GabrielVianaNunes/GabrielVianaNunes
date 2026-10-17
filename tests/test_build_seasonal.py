import contextlib
import datetime
import io
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_seasonal as bs  # noqa: E402
import seasons  # noqa: E402


def committed(name):
    with open(os.path.join(ROOT, "assets", name), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = bs.main(list(args))
    return code, out.getvalue(), err.getvalue()


def read(folder, name):
    with open(os.path.join(folder, name), encoding="utf-8", newline="") as f:
        return f.read()


class DefaultDays(unittest.TestCase):
    """Outside every window the four files are exactly the current look."""

    def test_a_plain_day_gives_the_committed_assets(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run("--out", d, "--date", "2026-06-15")
            self.assertEqual(code, 0)
            self.assertIn("default look", out)
            self.assertEqual(read(d, "banner.svg"), committed("banner.svg"))
            self.assertEqual(read(d, "footer.svg"), committed("footer-dusk.svg"))
            self.assertEqual(read(d, "wanted.svg"), committed("wanted.svg"))
            self.assertEqual(read(d, "divider-town.svg"), committed("divider.svg"))

    def test_an_active_season_without_art_still_gives_the_default_look(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run("--out", d, "--date", "2027-03-28")      # Easter has no art yet
            self.assertEqual(code, 0)
            self.assertIn("easter is active but has no art yet", out)
            self.assertEqual(read(d, "banner.svg"), committed("banner.svg"))


class HalloweenDays(unittest.TestCase):
    def test_the_window_edges(self):
        for day, expected in (("2026-10-23", False), ("2026-10-24", True), ("2026-10-31", True),
                              ("2026-11-02", True), ("2026-11-03", False)):
            with self.subTest(day), tempfile.TemporaryDirectory() as d:
                _, out, _ = run("--out", d, "--date", day)
                self.assertEqual("halloween decoration" in out, expected)

    def test_all_four_files_are_decorated_and_the_divider_keeps_its_size(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run("--out", d, "--date", "2026-10-31")
            self.assertEqual(code, 0)
            self.assertIn("halloween decoration", out)
            self.assertNotEqual(read(d, "footer.svg"), committed("footer-dusk.svg"))
            self.assertNotEqual(read(d, "wanted.svg"), committed("wanted.svg"))
            divider = read(d, "divider-town.svg")
            self.assertNotEqual(divider, committed("divider.svg"))
            self.assertIn('viewBox="0 0 160 10"', divider)
            self.assertIn('width="800"', divider)

    def test_the_same_day_always_gives_the_same_files(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            run("--out", a, "--date", "2026-10-31")
            run("--out", b, "--date", "2026-10-31")
            for name in bs.BUILDERS:
                self.assertEqual(read(a, name), read(b, name))


class ChristmasDays(unittest.TestCase):
    def decorated_as(self, day):
        with tempfile.TemporaryDirectory() as d:
            _, out, _ = run("--out", d, "--date", day)
            return out.splitlines()[0].split(": ", 1)[1]

    def test_the_window_from_halloween_to_the_25th(self):
        self.assertEqual(self.decorated_as("2026-11-02"), "halloween decoration")
        self.assertEqual(self.decorated_as("2026-11-03"), "christmas decoration")
        self.assertEqual(self.decorated_as("2026-12-01"), "christmas decoration")
        self.assertEqual(self.decorated_as("2026-12-25"), "christmas decoration")

    def test_the_default_look_returns_on_the_26th_and_27th(self):
        self.assertIn("default look", self.decorated_as("2026-12-26"))
        self.assertIn("default look", self.decorated_as("2026-12-27"))

    def test_the_christmas_footer_says_merry_trails_and_the_rider_is_lowered(self):
        with tempfile.TemporaryDirectory() as d:
            run("--out", d, "--date", "2026-12-10")
            footer = read(d, "footer.svg")
            self.assertIn("Merry trails", footer)
            self.assertIn("translate(100 24)", footer)
            self.assertIn("translate(100 22)", committed("footer-dusk.svg"))   # the default one is untouched


class BirthdayDays(unittest.TestCase):
    def decorated_as(self, day):
        with tempfile.TemporaryDirectory() as d:
            _, out, _ = run("--out", d, "--date", day)
            return out.splitlines()[0].split(": ", 1)[1]

    def test_only_the_28th_has_the_birthday_decoration(self):
        self.assertEqual(self.decorated_as("2026-12-28"), "birthday decoration")
        self.assertEqual(self.decorated_as("2027-12-28"), "birthday decoration")
        for day in ("2026-12-26", "2026-12-27", "2026-12-29", "2026-12-30"):
            with self.subTest(day):
                self.assertIn("default look", self.decorated_as(day))

    def test_the_29th_goes_back_to_the_default_look_not_to_christmas(self):
        with tempfile.TemporaryDirectory() as d:
            run("--out", d, "--date", "2026-12-29")
            self.assertEqual(read(d, "banner.svg"), committed("banner.svg"))

    def test_the_birthday_footer_says_happy_birthday_and_shows_no_digits_in_its_text(self):
        with tempfile.TemporaryDirectory() as d:
            run("--out", d, "--date", "2026-12-28")
            footer = read(d, "footer.svg")
            self.assertIn("Happy birthday", footer)
            self.assertIn("translate(100 24)", footer)


class Forcing(unittest.TestCase):
    def test_forcing_a_season_wins_over_the_date(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run("--out", d, "--date", "2026-06-15", "--season", "halloween")
            self.assertEqual(code, 0)
            self.assertNotEqual(read(d, "banner.svg"), committed("banner.svg"))

    def test_bad_season_ids_fail_without_writing_anything(self):
        for bad in ("nope", "Halloween", "halloween; rm -rf", "../x", "$(id)"):
            with self.subTest(bad), tempfile.TemporaryDirectory() as d:
                code, _, err = run("--out", os.path.join(d, "o"), "--season", bad)
                self.assertEqual(code, 1)
                self.assertFalse(os.path.exists(os.path.join(d, "o")))

    def test_a_bad_date_fails_without_writing(self):
        with tempfile.TemporaryDirectory() as d:
            code, _, _ = run("--out", os.path.join(d, "o"), "--date", "yesterday")
            self.assertEqual(code, 1)
            self.assertFalse(os.path.exists(os.path.join(d, "o")))


class FailsClosed(unittest.TestCase):
    def test_a_broken_asset_stops_the_whole_build(self):
        original = bs.BUILDERS["footer.svg"]
        bs.BUILDERS["footer.svg"] = lambda deco: "<svg><unclosed></svg>"
        try:
            with tempfile.TemporaryDirectory() as d:
                code, _, err = run("--out", os.path.join(d, "o"), "--date", "2026-06-15")
                self.assertEqual(code, 1)
                self.assertIn("not valid XML", err)
                self.assertFalse(os.path.exists(os.path.join(d, "o")))
        finally:
            bs.BUILDERS["footer.svg"] = original

    def test_scripts_and_external_references_are_refused(self):
        for bad in ("<svg xmlns='http://www.w3.org/2000/svg'><script>x</script></svg>",
                    "<svg xmlns='http://www.w3.org/2000/svg'><image href='https://evil.example/x.png'/></svg>"):
            with self.subTest(bad), self.assertRaises(bs.BuildError):
                bs.check("x.svg", bad)

    def test_the_size_budget_is_enforced(self):
        with self.assertRaises(bs.BuildError):
            bs.check("x.svg", "<svg xmlns='http://www.w3.org/2000/svg'>" + "<!--" + "a" * bs.MAX_BYTES + "--></svg>")


class EveryDayOfTheYearBuilds(unittest.TestCase):
    def test_each_season_window_builds_valid_assets(self):
        config = seasons.load_config()
        day = datetime.date(2027, 1, 1)
        seen = set()
        while day.year == 2027:
            sid = bs.choose(config, "", day)
            if sid not in seen:
                seen.add(sid)
                bs.build(sid)
            day += datetime.timedelta(days=1)
        self.assertGreaterEqual(len(seen), 8)              # default plus the seven seasons


if __name__ == "__main__":
    unittest.main()
