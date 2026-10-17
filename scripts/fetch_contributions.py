"""Fetches the weekly contribution totals of a GitHub user and writes them as a small JSON file.

Privacy rules (see docs/SECURITY.md):
  * only the contribution calendar is requested, never repositories, titles or messages
  * the API response and the token are never printed, only the totals
  * only the reduced weekly list is written to disk
  * the data is validated, and on any problem the script exits non zero WITHOUT writing,
    so a workflow keeps publishing the previous good output

Usage:
  GITHUB_TOKEN=... python scripts/fetch_contributions.py --user NAME --out data/contributions.json
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.github.com/graphql"
QUERY = (
    "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{"
    "totalContributions weeks{firstDay contributionDays{contributionCount}}}}}}"
)
MAX_WEEKS = 60
MAX_WEEK_TOTAL = 20000


class FetchError(Exception):
    """Raised for any problem. Messages never contain the token or the response body."""


def post_graphql(token, login, timeout=20):
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode("utf-8")
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json",
                 "User-Agent": "profile-readme-town"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise FetchError("GitHub API answered HTTP %d" % e.code)
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise FetchError("could not reach the GitHub API or the answer was not JSON")


def reduce_calendar(payload):
    """Turns the API payload into [{"start": "YYYY-MM-DD", "total": int}, ...]."""
    try:
        cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        weeks = cal["weeks"]
        out = []
        for w in weeks:
            out.append({"start": w["firstDay"],
                        "total": sum(d["contributionCount"] for d in w["contributionDays"])})
        declared = cal["totalContributions"]
    except (KeyError, TypeError):
        errs = payload.get("errors") if isinstance(payload, dict) else None
        kind = errs[0].get("type", "unknown") if errs and isinstance(errs[0], dict) else "shape"
        raise FetchError("unexpected API answer (%s)" % kind)
    return out, declared


def validate(weeks, declared=None):
    """Fails closed: raises FetchError unless the data looks like a real calendar."""
    if not isinstance(weeks, list) or not 1 <= len(weeks) <= MAX_WEEKS:
        raise FetchError("week count out of range")
    prev = None
    for w in weeks:
        if not isinstance(w, dict) or set(w) != {"start", "total"}:
            raise FetchError("bad week entry")
        t = w["total"]
        if not isinstance(t, int) or isinstance(t, bool) or not 0 <= t <= MAX_WEEK_TOTAL:
            raise FetchError("week total out of range")
        try:
            d = datetime.date.fromisoformat(w["start"])
        except (TypeError, ValueError):
            raise FetchError("bad date")
        if prev is not None and (d - prev).days != 7:
            raise FetchError("weeks are not consecutive")
        prev = d
    if declared is not None and declared != sum(w["total"] for w in weeks):
        raise FetchError("totals do not add up")
    return weeks


def fetch(login, token, post=post_graphql, retries=3, sleep=time.sleep):
    last = None
    for attempt in range(retries):
        try:
            weeks, declared = reduce_calendar(post(token, login))
            return validate(weeks, declared)
        except FetchError as e:
            last = e
            if attempt < retries - 1:
                sleep(2 ** attempt)
    raise last


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=os.environ.get("USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER"))
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token or not args.user:
        print("error: need a user and GITHUB_TOKEN (or GH_TOKEN)", file=sys.stderr)
        return 2
    try:
        weeks = fetch(args.user, token)
    except FetchError as e:
        print("error:", e, file=sys.stderr)
        return 1
    total = sum(w["total"] for w in weeks)
    data = {"generated": datetime.date.today().isoformat(), "total": total, "weeks": weeks}
    tmp = args.out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, args.out)
    print("ok: %d weeks, %d contributions" % (len(weeks), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
