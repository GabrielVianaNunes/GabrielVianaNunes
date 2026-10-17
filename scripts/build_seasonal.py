"""Builds the four assets that change with the season and writes them to a folder.

  python scripts/build_seasonal.py --out dist                   # the season of today (America/Sao_Paulo)
  python scripts/build_seasonal.py --out dist --date 2026-10-31 # the season of a given day
  python scripts/build_seasonal.py --out dist --season halloween  # force one, for previews

Files: banner.svg, footer.svg, wanted.svg and divider-town.svg. With no season, or a season that has
no art yet, they are exactly the default look. Everything is built and checked before anything is
written, so a problem leaves the previous files untouched.
"""
import argparse
import datetime
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_assets as ba  # noqa: E402
import season_art  # noqa: E402
import seasons  # noqa: E402

MAX_BYTES = 150000
BUILDERS = {
    "banner.svg": ba.build_banner,
    "footer.svg": ba.build_footer,
    "wanted.svg": ba.build_wanted,
    "divider-town.svg": ba.build_strip,
}


class BuildError(Exception):
    pass


def choose(config, forced, day):
    """The season id to build, or None for the default look."""
    if forced:
        if not re.fullmatch(r"[a-z0-9-]+", forced):
            raise BuildError("bad season id")
        if forced not in {s["id"] for s in config["seasons"]}:
            raise BuildError("unknown season: " + forced)
        return forced
    season = seasons.active_season(day, config)
    return season["id"] if season else None


def check(name, svg):
    """Fails closed: the file must be valid SVG, small, and free of scripts and external references."""
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        raise BuildError("%s is not valid XML: %s" % (name, e))
    if len(svg.encode("utf-8")) > MAX_BYTES:
        raise BuildError("%s is over the %d byte budget" % (name, MAX_BYTES))
    if re.search(r"<script|<image|<foreignObject|https?://(?!www\.w3\.org)|javascript:|xlink:href", svg):
        raise BuildError("%s has scripts or external references" % name)


def build(season_id, day=None):
    deco = season_art.get(season_id) if season_id else None
    if deco is not None and day is not None:
        deco = deco.with_date(day)
    files = {name: fn(deco) for name, fn in BUILDERS.items()}
    for name, svg in files.items():
        check(name, svg)
    return files, deco


def describe(season_id, deco):
    if not season_id:
        return "default look (no active season)"
    if deco is None:
        return "%s is active but has no art yet, default look" % season_id
    return "%s decoration" % season_id


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--season", default="", help="force a season id instead of using the date")
    ap.add_argument("--date", help="YYYY-MM-DD, default is today in the configured time zone")
    args = ap.parse_args(argv)
    try:
        config = seasons.load_config()
        day = datetime.date.fromisoformat(args.date) if args.date else seasons.today_in_zone(config)
        season_id = choose(config, args.season, day)
        files, deco = build(season_id, day)
    except (BuildError, seasons.ConfigError, ValueError, OSError) as e:
        print("error:", e, file=sys.stderr)
        return 1
    os.makedirs(args.out, exist_ok=True)
    for name, svg in files.items():
        with open(os.path.join(args.out, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg)
    print("date %s: %s" % (day.isoformat(), describe(season_id, deco)))
    for name, svg in files.items():
        print("  %-17s %3d KB" % (name, len(svg.encode("utf-8")) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
