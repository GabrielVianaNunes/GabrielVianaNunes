"""Builds assets/quote.svg with the quote of the week.

The quote is picked from data/quotes.json by counting weeks since a fixed date,
so every week gets the next quote and none repeats until the list is exhausted.

Usage:
  python scripts/update_quote.py            # quote for the current week
  python scripts/update_quote.py --index 3  # force a specific quote (preview)
"""
import argparse
import html
import json
import os
import textwrap
from datetime import date

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
START = date(2025, 1, 6)  # a Monday


def pick(quotes, index=None):
    if index is None:
        index = (date.today() - START).days // 7
    return quotes[index % len(quotes)]


def render(q):
    lines = textwrap.wrap(f"“{q['text']}”", width=58)
    line_h, top, pad = 34, 64, 48
    h = top + len(lines) * line_h + 70
    w = 1000
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{html.escape(q["text"] + " " + q["author"])}">',
        f'<title>{html.escape(q["text"])} ({html.escape(q["author"])})</title>',
        f'<rect width="{w}" height="{h}" fill="#3b2a1e"/>',
    ]
    for y in range(40, h, 40):
        out.append(f'<rect x="0" y="{y}" width="{w}" height="3" fill="#2e2017"/>')
    out.append(f'<rect x="0" y="0" width="{w}" height="8" fill="#c98b4a"/>')
    out.append(f'<rect x="0" y="{h - 8}" width="{w}" height="8" fill="#c98b4a"/>')
    out.append(f'<rect x="0" y="0" width="8" height="{h}" fill="#c98b4a"/>')
    out.append(f'<rect x="{w - 8}" y="0" width="8" height="{h}" fill="#c98b4a"/>')
    for x, y in [(24, 24), (w - 36, 24), (24, h - 36), (w - 36, h - 36)]:
        out.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="#e6b36a"/>')
    font = "font-family=\"'Courier New', Courier, monospace\""
    y = top
    for ln in lines:
        out.append(
            f'<text x="{pad + 20}" y="{y}" {font} font-size="24" font-weight="bold" '
            f'fill="#f3e2c0">{html.escape(ln)}</text>'
        )
        y += line_h
    out.append(
        f'<text x="{w - pad - 20}" y="{y + 20}" text-anchor="end" {font} font-size="20" '
        f'fill="#e0a85e">{html.escape(q["author"])}</text>'
    )
    out.append(
        f'<text x="{w - pad - 20}" y="{y + 46}" text-anchor="end" {font} font-size="15" '
        f'fill="#a6692f">{html.escape(q["context"])}</text>'
    )
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, default=None)
    args = ap.parse_args()
    with open(os.path.join(ROOT, "data", "quotes.json"), encoding="utf-8") as f:
        quotes = json.load(f)
    q = pick(quotes, args.index)
    with open(os.path.join(ROOT, "assets", "quote.svg"), "w", encoding="utf-8") as f:
        f.write(render(q))
    print("quote of the week:", q["author"], "|", q["text"][:60])
