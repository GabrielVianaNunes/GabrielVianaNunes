# New Year design (for approval)

Issue 51. The default western look stays. This only adds midnight on top of it.

Window: 31 Dec and 1 Jan only (decided by the owner). 29 and 30 Dec, and 2 Jan, use the default look.

## The number of the year

The number is calculated from the date: on 31 Dec it shows the year that is about to begin, on 1 Jan the current one. The previews in this folder were built for 31 Dec and show the next year. Tests check the 31 Dec to 1 Jan change, and that an earlier copy of the art is never changed by a later date.

## What is added

| Asset | Decoration |
|---|---|
| Banner | The sky darkens into midnight with golden twinkling stars, fireworks burst over the mesas in four places (a white flash, then two rings of colored sparks that fade), gold and silver confetti falls, a grandfather clock striking twelve glows on the ground with its pendulum swinging, the number of the new year shines in gold in the top right corner, and the cowboy wears a gold hat (it replaces the cowboy hat) with a sparkle on top |
| Footer | "HAPPY NEW YEAR" instead of "HAPPY TRAILS", a midnight sky, two fireworks, confetti, the clock and the gold hat rider (2 pixels lower than the default, so the hat stays inside the picture) |
| Wanted poster | A gold top hat with a navy band replaces the cowboy hat in the portrait, gold and silver confetti in the free spaces, and a glittering frame that twinkles along the whole border |
| Divider above "The town" | "HAPPY NEW YEAR" and the number of the year in gold letters on navy and plum bunting, with confetti along the string and a golden star at each end. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the portrait, and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets, built for 31 Dec (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py new-year --date 2026-12-31 --out docs/seasons/new-year
```

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- It was a draft until the owner approved it.
- No scripts and no external references. Animation stops with reduced motion, and one frame of each firework stays visible.
- Every file is under 150 KB.

## Approval

- [x] Owner reviewed the preview
- [x] Owner approved on issue 51
- [x] Window confirmed: 31 Dec and 1 Jan

Built in issue 52: registered as an approved season, with the number of the year calculated from the date.
