import datetime
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_seasonal as bs  # noqa: E402
import seasons  # noqa: E402

D = datetime.date


def decorated_as(day):
    config = seasons.load_config()
    sid = bs.choose(config, "", day)
    files, deco = bs.build(sid, day)
    return sid, deco is not None


class EasterWindowsThroughTheWholeBuild(unittest.TestCase):
    """The decoration follows Easter itself, which moves every year, not a fixed date."""

    def test_the_window_is_three_days_before_to_three_days_after_easter_for_many_years(self):
        for year in list(range(2026, 2041)) + [2050, 2077, 2099]:
            easter = seasons.easter_date(year)
            for offset in range(-5, 6):
                day = easter + datetime.timedelta(days=offset)
                sid, art = decorated_as(day)
                with self.subTest("%d %+d" % (year, offset)):
                    if -3 <= offset <= 3:
                        self.assertEqual((sid, art), ("easter", True))
                    else:
                        self.assertNotEqual(sid, "easter")

    def test_the_window_of_2027_is_25_to_31_march(self):
        self.assertEqual(decorated_as(D(2027, 3, 24))[0], None)
        for d in range(25, 32):
            self.assertEqual(decorated_as(D(2027, 3, d)), ("easter", True))
        self.assertEqual(decorated_as(D(2027, 4, 1))[0], None)

    def test_the_footer_says_happy_easter_and_the_rider_is_lowered(self):
        with tempfile.TemporaryDirectory() as d:
            config = seasons.load_config()
            files, _ = bs.build("easter", D(2027, 3, 28))
            self.assertIn("Happy easter", files["footer.svg"])
            self.assertIn("translate(100 24)", files["footer.svg"])


if __name__ == "__main__":
    unittest.main()
