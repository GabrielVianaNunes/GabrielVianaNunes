# National Day of the Cowboy design (for approval)

Issue 57. The default western look stays. This only adds a rodeo night on top of it. The cowboy keeps his hat: it is his day.

Window: 1 day, the 4th Saturday of July, calculated every year (24 Jul in 2027). The owner changed it from 7 days to the exact day.

## What is added

| Asset | Decoration |
|---|---|
| Banner | Three spotlights sweeping the sky, red white and blue bunting between two wooden posts, a rodeo fence with a bull behind it, three barrel racing barrels, a hay bale, a gold trophy, lucky horseshoes that twinkle, red white blue and gold stars falling, and the cowboy with a gold band on his hat and a lasso that spins in his hand |
| Footer | "HAPPY COWBOY DAY" instead of "HAPPY TRAILS", a string of red white and blue flags along the top, two spotlights, barrels, hay, horseshoes, falling stars and the lasso rider (2 pixels lower than the default, so the lasso stays inside the picture) |
| Wanted poster | A gold sheriff star on one side of the chest and a blue ribbon rosette with red and white tails on the other side, bunting along the top edge, a lucky horseshoe in each bottom corner and a few stars in the free spaces. The hat is the cowboy's own |
| Divider above "The town" | "HAPPY COWBOY DAY" on red, white and blue bunting with gold and red confetti and a gold star at each end. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the dusk sky, the horse and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py cowboy-day --out docs/seasons/cowboy-day
```

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- It was a draft until the owner approved it.
- The horse is untouched. The lasso and everything on the rider stay inside the footer in the raised frame of the bob animation.
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB.

## Approval

- [x] Owner reviewed the preview
- [x] Owner approved on issue 57
- [x] Window confirmed: the 4th Saturday of July, that day only

Built in issue 62: registered as an approved season, so the daily workflow publishes it only on the 4th Saturday of July.
