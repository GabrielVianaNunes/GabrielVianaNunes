# Seasonal decorations

The default western look stays. On special dates the overview gets extra decoration that fits the western theme, for a window of days, and then goes back to the default.

Project board: https://github.com/users/GabrielVianaNunes/projects/8

## Calendar (proposed windows, the owner decides)

All dates are in the America/Sao_Paulo time zone.

| Season | Proposed window | Status |
|---|---|---|
| Halloween | 24 Oct to 2 Nov | Requested |
| Christmas | 1 Dec to 24 Dec | Requested |
| Christmas with birthday | 25 Dec to 29 Dec, peak on 28 Dec | Requested |
| New Year | 30 Dec to 3 Jan | Requested |
| Easter | Palm Sunday to Easter Monday, moves every year (about 21 to 29 Mar 2027) | Requested |
| Carnival | Carnival Saturday to Ash Wednesday, moves (6 to 10 Feb 2027) | Suggested |
| Festa Junina | 12 Jun to 29 Jun | Suggested |
| National Day of the Cowboy | Week of the 4th Saturday of July | Suggested |
| Programmers' Day | 12 Sep to 14 Sep (the 256th day of the year) | Suggested |

The requested seasons chain without gaps at the end of the year: Christmas, then Christmas with birthday, then New Year, then back to the default on 4 Jan.

## One time zone for everyone

A README is static, so it cannot know where the visitor is. Seasons are decided once a day in a fixed time zone and published as files. Everyone sees the same decoration, and it changes at midnight in Goiania. The daily workflow runs at 03:05 UTC, which is 00:05 in America/Sao_Paulo.

This is different from the day and night look of the town, which follows the viewer's GitHub theme (light or dark), not the clock.

## How it works

```
data/seasons.json -> scripts/seasons.py (which season is active today)
                  -> season modules add decoration layers
                  -> build_town / build_assets draw the default plus the layers
                  -> daily workflow publishes to the output branch -> README
```

- A season is a small module that adds layers on top of the default drawing. It never edits the default drawing.
- With no active season the output is identical to the default, and a test checks that.
- Windows live in `data/seasons.json`, so changing a date does not need code. Moving dates are computed.
- A season can be tried without going live: run the workflow with a `season` input and the `output-preview` target.

## Approval process

Every season has two issues, a design and a build, and they are approved separately:

1. **Design issue.** A preview sheet (day and night) is published in a pull request. The owner reviews it and comments "approved" or asks for changes. The window dates are confirmed here.
2. **Build issue.** Starts only after the approval. A preview run on `output-preview` is checked before going live.

## Privacy

The Christmas with birthday season makes the day and month of the birthday public. The year and the age are never shown. This needs the owner's explicit OK in the design issue.

## Issue map

| Group | Issues |
|---|---|
| Infrastructure | 40 calendar engine, 41 town layers, 42 banner footer poster, 43 daily workflow, 44 previews and docs |
| Halloween | 45 design, 46 build |
| Christmas | 47 design, 48 build |
| Christmas with birthday | 49 design, 50 build |
| New Year | 51 design, 52 build |
| Easter | 53 design, 54 build |
| Suggested ideas | 55 Carnival, 56 Festa Junina, 57 Cowboy Day, 58 Programmers' Day |
| Related future idea | 59 day and night by time |

## Schedule

About two to three hours per week of the owner's attention is enough: the owner only reviews designs and approves.

| When | What |
|---|---|
| 19 to 23 Oct 2026 | Infrastructure, Halloween design and build. Halloween only makes it this year if the design is approved by 21 Oct, otherwise it moves to 2027 |
| 10 to 24 Nov 2026 | Christmas design and build |
| 17 Nov to 1 Dec 2026 | Christmas with birthday |
| 24 Nov to 8 Dec 2026 | New Year |
| 2 Feb to 1 Mar 2027 | Easter |
