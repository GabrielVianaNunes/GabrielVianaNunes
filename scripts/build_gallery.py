"""Rebuilds the season gallery: the preview files of every approved season and the page that shows them.

  python scripts/build_gallery.py

Writes docs/seasons/<id>/ (banner, footer, poster, divider, plus the default look) and two copies of the gallery page:
docs/seasons/GALLERY.md (relative images, for browsing the repository) and docs/wiki/Seasonal-gallery.md (absolute
images from main, for the wiki). The gallery only shows pictures. It never changes what the overview publishes,
which stays tied to each season's own window.
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_season_preview as bsp  # noqa: E402
import season_art  # noqa: E402
import seasons  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = "https://raw.githubusercontent.com/GabrielVianaNunes/GabrielVianaNunes/main/docs/seasons/"
# Seasons whose art depends on the date are previewed on a day inside their window.
PREVIEW_DAY = {"new-year": datetime.date(2026, 12, 31), "programmers-day": datetime.date(2027, 9, 13)}
YEAR = 2027
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def pretty(day):
    return "%d %s" % (day.day, MONTHS[day.month - 1])


def when(config, sid):
    wins = [w for w in seasons.windows_of_year(config, YEAR) if w[0] == sid and w[1].year == YEAR]
    if not wins:
        wins = [w for w in seasons.windows_of_year(config, YEAR) if w[0] == sid]
    _, start, end = wins[0]
    return pretty(start) if start == end else "%s to %s" % (pretty(start), pretty(end))


def preview_files(season_id, folder):
    args = [season_id, "--out", folder]
    if season_id in PREVIEW_DAY:
        args += ["--date", PREVIEW_DAY[season_id].isoformat()]
    return bsp.main(args)


def page(base, config, ids):
    lines = ["# Seasonal gallery", "",
             "How the overview looks on each special date, shown here at any time of the year. The pictures below are only "
             "previews. The profile itself wears a decoration only inside that date's own window, and looks normal every other day.", ""]
    for sid in ids:
        deco = season_art.get(sid)
        lines += ["## %s" % deco.name, "", "On the overview: %s (example for %d)." % (when(config, sid), YEAR), "",
                  '<img src="%s%s/banner.svg" alt="%s banner" width="100%%">' % (base, sid, deco.name), "",
                  '<img src="%s%s/footer.svg" alt="%s footer" width="100%%">' % (base, sid, deco.name), "",
                  '<img src="%s%s/strip.svg" alt="%s divider" width="100%%">' % (base, sid, deco.name), "",
                  '<img src="%s%s/default/wanted.svg" alt="Normal poster" width="240"> <img src="%s%s/wanted.svg" alt="%s poster" width="240">'
                  % (base, sid, base, sid, deco.name), ""]
    lines += ["Regenerate with `python scripts/build_gallery.py`.", ""]
    return "\n".join(lines)


def main():
    config = seasons.load_config()
    ids = sorted(season_art.ids("approved"), key=lambda s: [x["id"] for x in config["seasons"]].index(s))
    for sid in ids:
        if preview_files(sid, os.path.join(ROOT, "docs", "seasons", sid)):
            return 1
    for path, base in (("docs/seasons/GALLERY.md", ""), ("docs/wiki/Seasonal-gallery.md", RAW)):
        with open(os.path.join(ROOT, path), "w", encoding="utf-8", newline="\n") as f:
            f.write(page(base, config, ids))
        print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
