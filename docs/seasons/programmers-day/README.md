# Programmers' Day design (approved)

Issue 58. The default western look stays. This only adds a night where the town goes online. The cowboy keeps his hat and the horse is untouched.

Window: 3 days, day 256 of the year with 1 day either side, calculated every year (12 to 14 Sep in 2027). This is a proposal, to be confirmed here.

## What is added

| Asset | Decoration |
|---|---|
| Banner | Green binary digits falling slowly on the right side of the sky, a wooden sign with a lit screen that reads 256 and a blinking cursor, a rubber duck on the ground and a steaming coffee mug in the cowboy's hand |
| Footer | "HAPPY PROGRAMMERS DAY" instead of "HAPPY TRAILS", binary digits falling on the left, the 256 sign on the right, a rubber duck and the coffee rider (2 pixels lower than the default, like the other seasons) |
| Wanted poster | Round glasses on the cowboy and code braces in the top corners |
| Divider above "The town" | A terminal line that reads "> HELLO WORLD" with a blinking cursor and dim binary digits at both ends. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the dusk sky, the horse and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py programmers-day --out docs/seasons/programmers-day --date 2027-09-13
```

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- It is approved: the daily build uses it only inside its window (a test checks it).
- The horse is untouched. Everything on the rider stays inside the footer in the raised frame of the bob animation.
- Falling digits stay in the free areas and never cross the name, the role or the footer text.
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB.

## Approval

- [x] Owner reviewed the preview
- [x] Owner commented "approved" on issue 58, or asked for changes
- [x] Window confirmed: day 256 with 1 day either side
