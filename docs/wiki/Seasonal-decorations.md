# Seasonal decorations

The default western look stays. On special dates the overview gets extra decoration that fits the western theme and the old west era, for a window of days, and then goes back to the default.

Project board: https://github.com/users/GabrielVianaNunes/projects/8

## Calendar (decided by the owner)

All dates are in the America/Sao_Paulo time zone.

| Season | Window | Notes |
|---|---|---|
| Halloween | 24 Oct to 2 Nov | Fixed dates |
| Christmas | 3 Nov to 25 Dec | Starts when the Halloween decoration ends |
| Birthday | 28 Dec only | Only that day, with a touch of Christmas allowed. 26 and 27 Dec use the default look |
| New Year | 31 Dec and 1 Jan | 29 and 30 Dec use the default look, and so does 2 Jan |
| Easter | 7 days: 3 days before to 3 days after Easter Sunday | Computed for every year, never a fixed date |
| National Day of the Cowboy | 7 days: 4th Saturday of July, 3 days either side | Window is a proposal to confirm |
| Programmers' Day | 3 days: day 256 of the year, 1 day either side | 13 Sep, or 12 Sep in leap years. A proposal to confirm |

Declined by the owner: Carnival and Festa Junina.

For 2027 the moving dates are: Easter on 28 Mar (window 25 to 31 Mar), Cowboy Day on 24 Jul (window 21 to 27 Jul) and Programmers' Day on 13 Sep (window 12 to 14 Sep).

## One time zone for everyone

A README is static, so it cannot know where the visitor is. Seasons are decided once a day in a fixed time zone and published as files. Everyone sees the same decoration, and it changes at midnight in Goiania. The daily workflow runs at 03:05 UTC, which is 00:05 in America/Sao_Paulo.

## How it works

```
data/seasons.json -> scripts/seasons.py (which season is active today)
                  -> season modules add decoration layers
                  -> build_assets draws the default plus the layers
                  -> daily workflow publishes to the output branch -> README
```

- A season is a small module that adds layers on top of the default drawing. It never edits the default drawing.
- With no active season the output is identical to the default, and a test checks that.
- Windows live in `data/seasons.json`, so changing a date does not need code.
- Window kinds: date range, single day, range across the new year, relative to Easter, nth weekday of a month with a margin, and day of the year with a margin.
- Easter uses the Gregorian algorithm (Meeus, Jones and Butcher), exact for every year, and is tested against the known dates for 2025 to 2040.
- A season can be tried without going live: run the workflow "Seasonal assets" with a `season` input and the `output-preview` target.
- A season only decorates four files: `banner.svg`, `footer.svg`, `wanted.svg` and the divider above "The town" (`divider-town.svg`). That divider replaces the normal one and has exactly its size, so the layout never moves.
- A season with no art yet, or no season at all, gives the default look.

## Approval process

Every season has two issues, a design and a build, approved separately:

1. **Design issue.** A preview sheet (day and night) is published in a pull request. The owner reviews it and comments "approved" or asks for changes. The window dates are confirmed here.
2. **Build issue.** Starts only after the approval. A preview run on `output-preview` is checked before going live.

## Privacy

The birthday decoration makes the day and month of the birthday public. The year and the age are never shown. The design issue asks for the owner's explicit OK before it is built.

## Issue map

| Group | Issues |
|---|---|
| Infrastructure | 40 calendar engine, 41 layers for the banner, footer and poster, 42 divider above the 3D graph, 43 daily workflow, 44 previews and docs |
| Halloween | 45 design, 46 build |
| Christmas | 47 design, 48 build |
| Birthday | 49 design, 50 build |
| New Year | 51 design, 52 build |
| Easter | 53 design, 54 build |
| National Day of the Cowboy | 57 design, 62 build |
| Programmers' Day | 58 design, 63 build |

## Schedule

The owner only reviews designs and approves.

| When | What |
|---|---|
| 19 to 23 Oct 2026 | Infrastructure, Halloween design and build. Halloween only makes it this year if the design is approved by 21 Oct, otherwise it moves to 2027 |
| 28 Oct to 6 Nov 2026 | Christmas. It starts to show as soon as it is live, inside its window |
| 17 Nov to 1 Dec 2026 | Birthday |
| 24 Nov to 8 Dec 2026 | New Year |
| 2 Feb to 1 Mar 2027 | Easter |
| 1 Jun to 1 Jul 2027 | National Day of the Cowboy |
| 2 Aug to 30 Aug 2027 | Programmers' Day |

## Status

| Season | Design | Build |
|---|---|---|
| Halloween | Approved | Built, waiting for the release |
| Christmas | Not started | Not started |
| Birthday | Not started | Not started |
| New Year | Not started | Not started |
| Easter | Not started | Not started |
| National Day of the Cowboy | Not started | Not started |
| Programmers' Day | Not started | Not started |

How a release works, step by step: `docs/seasons/RELEASE.md`.
