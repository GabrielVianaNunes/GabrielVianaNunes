import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_gallery as gallery  # noqa: E402
import season_art  # noqa: E402
import seasons  # noqa: E402


def text(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


class Gallery(unittest.TestCase):
    def test_the_committed_previews_match_the_current_art(self):
        for sid in season_art.ids("approved"):
            with tempfile.TemporaryDirectory() as d:
                import contextlib
                import io
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(gallery.preview_files(sid, d), 0)
                for name in ("banner.svg", "footer.svg", "wanted.svg", "strip.svg", "default/wanted.svg"):
                    with self.subTest("%s %s" % (sid, name)):
                        self.assertEqual(text(os.path.join(d, name)), text(os.path.join(ROOT, "docs", "seasons", sid, name)),
                                         "run python scripts/build_gallery.py")

    def test_the_pages_list_every_approved_season_and_are_up_to_date(self):
        config = seasons.load_config()
        ids = sorted(season_art.ids("approved"), key=lambda s: [x["id"] for x in config["seasons"]].index(s))
        self.assertEqual(text(os.path.join(ROOT, "docs/seasons/GALLERY.md")), gallery.page("", config, ids))
        self.assertEqual(text(os.path.join(ROOT, "docs/wiki/Seasonal-gallery.md")), gallery.page(gallery.RAW, config, ids))

    def test_the_gallery_changes_nothing_about_when_the_profile_is_decorated(self):
        config = seasons.load_config()
        for sid, expected in (("cowboy-day", "2027-07-24"), ("programmers-day", "2027-09-13")):
            wins = [w for w in seasons.windows_of_year(config, 2027) if w[0] == sid]
            self.assertEqual([(w[1].isoformat(), w[2].isoformat()) for w in wins], [(expected, expected)])


if __name__ == "__main__":
    unittest.main()
