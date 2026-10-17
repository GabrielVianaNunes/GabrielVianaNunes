"""Which seasonal decoration is active today, if any.

Windows live in data/seasons.json so a date can change without touching code. All dates are
decided in one fixed time zone (America/Sao_Paulo), so every visitor sees the same decoration and
it changes at midnight in Goiania.

  python scripts/seasons.py                      # the season for today
  python scripts/seasons.py --date 2026-12-28    # for a given day
  python scripts/seasons.py --year 2027          # every window of a year
"""
import argparse
import calendar
import datetime
import json
import os
import re
import sys

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "seasons.json")
WEEKDAYS = {name.lower(): i for i, name in enumerate(calendar.day_name)}
KINDS = ("range", "day", "easter", "nth_weekday", "day_of_year")
MAX_MARGIN = 14


class ConfigError(Exception):
    pass


# ------------------------------------------------------------------ date helpers

def easter_date(year):
    """Easter Sunday of the Gregorian calendar (Meeus, Jones and Butcher algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return datetime.date(year, month, day + 1)


def nth_weekday(year, month, weekday, n):
    """The n-th given weekday (0 is Monday) of a month, or None if the month has no such day."""
    first = datetime.date(year, month, 1)
    day = 1 + (weekday - first.weekday()) % 7 + 7 * (n - 1)
    if day > calendar.monthrange(year, month)[1]:
        return None
    return datetime.date(year, month, day)


def day_of_year(year, n):
    start = datetime.date(year, 1, 1)
    if n > (datetime.date(year + 1, 1, 1) - start).days:
        return None
    return start + datetime.timedelta(days=n - 1)


def parse_md(text):
    m = re.fullmatch(r"(\d{2})-(\d{2})", text or "")
    if not m:
        raise ConfigError("bad MM-DD value: %r" % (text,))
    month, day = int(m.group(1)), int(m.group(2))
    try:
        datetime.date(2024, month, day)          # 2024 is a leap year, so 02-29 is accepted
    except ValueError:
        raise ConfigError("not a real date: %r" % (text,))
    return month, day


def margin(rule, key):
    v = rule.get(key, 0)
    if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= MAX_MARGIN:
        raise ConfigError("%s must be an integer from 0 to %d" % (key, MAX_MARGIN))
    return datetime.timedelta(days=v)


# ------------------------------------------------------------------ windows

def windows_starting_in(rule, year):
    """The (start, end) dates, inclusive, of the windows of this rule that start in the given year."""
    kind = rule["kind"]
    if kind == "range":
        sm, sd = parse_md(rule["start"])
        em, ed = parse_md(rule["end"])
        start = datetime.date(year, sm, sd) if (sm, sd) != (2, 29) or calendar.isleap(year) else None
        if start is None:
            return []
        end_year = year if (em, ed) >= (sm, sd) else year + 1
        try:
            end = datetime.date(end_year, em, ed)
        except ValueError:
            return []
        return [(start, end)]
    if kind == "day":
        m, d = parse_md(rule["date"])
        try:
            day = datetime.date(year, m, d)
        except ValueError:
            return []
        return [(day, day)]
    before, after = margin(rule, "before"), margin(rule, "after")
    if kind == "easter":
        centre = easter_date(year)
    elif kind == "nth_weekday":
        if rule.get("weekday") not in WEEKDAYS or not isinstance(rule.get("n"), int) or not 1 <= rule["n"] <= 5:
            raise ConfigError("bad nth_weekday rule")
        if not isinstance(rule.get("month"), int) or not 1 <= rule["month"] <= 12:
            raise ConfigError("bad month")
        centre = nth_weekday(year, rule["month"], WEEKDAYS[rule["weekday"]], rule["n"])
    elif kind == "day_of_year":
        if not isinstance(rule.get("day"), int) or not 1 <= rule["day"] <= 366:
            raise ConfigError("bad day of year")
        centre = day_of_year(year, rule["day"])
    else:
        raise ConfigError("unknown rule kind: %r" % (kind,))
    if centre is None:
        return []
    return [(centre - before, centre + after)]


def validate(config):
    """Fails closed: raises ConfigError unless every season is well formed."""
    if not isinstance(config, dict) or not isinstance(config.get("seasons"), list):
        raise ConfigError("config needs a seasons list")
    seen = set()
    for s in config["seasons"]:
        if not isinstance(s, dict) or not re.fullmatch(r"[a-z0-9-]+", str(s.get("id", ""))):
            raise ConfigError("every season needs an id with lowercase letters, digits and dashes")
        if s["id"] in seen:
            raise ConfigError("duplicate season id: " + s["id"])
        seen.add(s["id"])
        if not isinstance(s.get("name"), str) or not s["name"]:
            raise ConfigError("season %s needs a name" % s["id"])
        if not isinstance(s.get("priority", 0), int) or isinstance(s.get("priority", 0), bool):
            raise ConfigError("priority must be an integer")
        rule = s.get("rule")
        if not isinstance(rule, dict) or rule.get("kind") not in KINDS:
            raise ConfigError("season %s has an unknown rule kind" % s["id"])
        windows_starting_in(rule, 2026)          # raises ConfigError on bad values
    return config


def load_config(path=CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return validate(json.load(f))


def windows_of_year(config, year):
    """Every window that touches the year, as (id, start, end), sorted by start."""
    out = []
    for s in config["seasons"]:
        for y in (year - 1, year):
            for start, end in windows_starting_in(s["rule"], y):
                if start.year == year or end.year == year:
                    out.append((s["id"], start, end))
    return sorted(out, key=lambda w: (w[1], w[0]))


def active_season(day, config):
    """The season active on the given date, or None for the default look.

    When windows overlap, the higher priority wins, then the later start, then the id.
    """
    best = None
    for s in config["seasons"]:
        for y in (day.year - 1, day.year, day.year + 1):
            for start, end in windows_starting_in(s["rule"], y):
                if start <= day <= end:
                    key = (s.get("priority", 0), start, s["id"])
                    if best is None or key > best[0]:
                        best = (key, s)
    return best[1] if best else None


# ------------------------------------------------------------------ time zone

def _zone(name):
    try:
        import zoneinfo
        return zoneinfo.ZoneInfo(name)
    except Exception:
        if name == "America/Sao_Paulo":     # no daylight saving since 2019, so a fixed offset is exact
            return datetime.timezone(datetime.timedelta(hours=-3))
        raise


def today_in_zone(config, now=None):
    """The current date in the configured time zone."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone aware")
    return now.astimezone(_zone(config.get("timezone", "America/Sao_Paulo"))).date()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD, default is today in the configured time zone")
    ap.add_argument("--year", type=int, help="list every window of this year")
    ap.add_argument("--config", default=CONFIG_PATH)
    args = ap.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.year:
            for sid, start, end in windows_of_year(config, args.year):
                print("%-16s %s to %s" % (sid, start.isoformat(), end.isoformat()))
            return 0
        day = datetime.date.fromisoformat(args.date) if args.date else today_in_zone(config)
    except (ConfigError, ValueError, OSError) as e:
        print("error:", e, file=sys.stderr)
        return 1
    season = active_season(day, config)
    print(season["id"] if season else "default")
    return 0


if __name__ == "__main__":
    sys.exit(main())
