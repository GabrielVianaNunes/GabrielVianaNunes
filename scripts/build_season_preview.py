"""Builds the decorated assets of one season so they can be reviewed before anything goes live.

  python scripts/build_season_preview.py halloween --out docs/seasons/halloween

Writes banner.svg, footer.svg, wanted.svg and strip.svg, plus the default look for comparison
under default/. Nothing here touches assets/ or the output branch.
"""
import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_assets as ba  # noqa: E402
import season_art  # noqa: E402


def build_all(deco):
    return {
        "banner.svg": ba.build_banner(deco),
        "footer.svg": ba.build_footer(deco),
        "wanted.svg": ba.build_wanted(deco),
        "strip.svg": ba.build_strip(deco),
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("season")
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", help="YYYY-MM-DD for seasons whose art depends on the date (for example the New Year)")
    args = ap.parse_args(argv)
    deco = season_art.get(args.season, drafts=True)
    if deco is None:
        print("error: no art for season %r" % args.season, file=sys.stderr)
        return 1
    if args.date:
        deco = deco.with_date(datetime.date.fromisoformat(args.date))
    for sub, d in (("", deco), ("default", None)):
        folder = os.path.join(args.out, sub)
        os.makedirs(folder, exist_ok=True)
        for name, svg in build_all(d).items():
            if sub == "default" and name == "strip.svg":
                continue
            with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
            print("wrote", os.path.join(folder, name), len(svg) // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
