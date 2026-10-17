import datetime
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import fetch_contributions as fc  # noqa: E402


def payload(totals, start=datetime.date(2025, 10, 12)):
    weeks = []
    for i, t in enumerate(totals):
        first = start + datetime.timedelta(days=7 * i)
        days = [{"contributionCount": t}] + [{"contributionCount": 0}] * 6
        weeks.append({"firstDay": first.isoformat(), "contributionDays": days})
    return {"data": {"user": {"contributionsCollection": {"contributionCalendar": {
        "totalContributions": sum(totals), "weeks": weeks}}}}}


class ReduceAndValidate(unittest.TestCase):
    def test_reduce_sums_days_per_week(self):
        weeks, declared = fc.reduce_calendar(payload([3, 0, 9]))
        self.assertEqual([w["total"] for w in weeks], [3, 0, 9])
        self.assertEqual(declared, 12)

    def test_reduced_data_has_only_start_and_total(self):
        weeks, _ = fc.reduce_calendar(payload([1, 2]))
        for w in weeks:
            self.assertEqual(set(w), {"start", "total"})

    def test_fixture_is_valid_and_minimal(self):
        with open(os.path.join(ROOT, "data", "contributions-fixture.json"), encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(set(data), {"generated", "total", "weeks"})
        fc.validate(data["weeks"], data["total"])

    def test_rejects_bad_data(self):
        good, _ = fc.reduce_calendar(payload([1, 2, 3]))
        bad_cases = {
            "empty": [],
            "too many": [{"start": "2025-10-12", "total": 0}] * 61,
            "negative": [dict(good[0], total=-1)],
            "huge": [dict(good[0], total=10 ** 9)],
            "bool": [dict(good[0], total=True)],
            "bad date": [dict(good[0], start="nope")],
            "extra key": [dict(good[0], repo="secret")],
            "gap": [good[0], dict(good[1], start="2030-01-01")],
        }
        for name, weeks in bad_cases.items():
            with self.subTest(name):
                with self.assertRaises(fc.FetchError):
                    fc.validate(weeks)

    def test_declared_total_must_match(self):
        good, _ = fc.reduce_calendar(payload([1, 2, 3]))
        with self.assertRaises(fc.FetchError):
            fc.validate(good, declared=999)

    def test_unexpected_shape_is_an_error_without_leaking_the_body(self):
        with self.assertRaises(fc.FetchError) as ctx:
            fc.reduce_calendar({"errors": [{"type": "NOT_FOUND", "message": "private detail"}]})
        self.assertIn("NOT_FOUND", str(ctx.exception))
        self.assertNotIn("private detail", str(ctx.exception))


class FetchRetry(unittest.TestCase):
    def test_retries_then_succeeds(self):
        calls = []

        def post(token, login):
            calls.append(1)
            if len(calls) < 3:
                raise fc.FetchError("temporary")
            return payload([5])

        weeks = fc.fetch("u", "TOKEN", post=post, sleep=lambda s: None)
        self.assertEqual(weeks[0]["total"], 5)
        self.assertEqual(len(calls), 3)

    def test_gives_up_and_error_never_contains_the_token(self):
        def post(token, login):
            raise fc.FetchError("GitHub API answered HTTP 502")

        with self.assertRaises(fc.FetchError) as ctx:
            fc.fetch("u", "SECRET_TOKEN_VALUE", post=post, sleep=lambda s: None)
        self.assertNotIn("SECRET_TOKEN_VALUE", str(ctx.exception))


class MainFailsClosed(unittest.TestCase):
    def test_no_token_means_no_file(self):
        old = {k: os.environ.pop(k, None) for k in ("GITHUB_TOKEN", "GH_TOKEN")}
        try:
            with tempfile.TemporaryDirectory() as d:
                out = os.path.join(d, "c.json")
                self.assertEqual(fc.main(["--user", "x", "--out", out]), 2)
                self.assertFalse(os.path.exists(out))
        finally:
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v

    def test_failure_keeps_the_previous_file(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "c.json")
            with open(out, "w", encoding="utf-8") as f:
                f.write("previous")
            original = fc.fetch
            fc.fetch = lambda *a, **k: (_ for _ in ()).throw(fc.FetchError("down"))
            os.environ["GITHUB_TOKEN"] = "x"
            try:
                self.assertEqual(fc.main(["--user", "x", "--out", out]), 1)
            finally:
                fc.fetch = original
                os.environ.pop("GITHUB_TOKEN", None)
            with open(out, encoding="utf-8") as f:
                self.assertEqual(f.read(), "previous")


if __name__ == "__main__":
    unittest.main()
