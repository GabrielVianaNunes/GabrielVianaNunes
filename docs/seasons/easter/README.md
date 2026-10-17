# Easter design (for approval)

Issue 53. The default western look stays. This only adds spring on top of it, in soft colors that still match the western palette.

Window: 7 days around Easter Sunday, from 3 days before to 3 days after, calculated for every year (the 2027 window is 25 to 31 Mar). Never a fixed date.

## What is added

| Asset | Decoration |
|---|---|
| Banner | A soft pastel tint over the dusk sky, drifting clouds and two butterflies, spring flowers and grass tufts along the ground, seven painted eggs (stripes, dots and zigzags), a wicker basket full of eggs, four chicks that hop (one sits on top of a cactus), a white bunny that hops across the whole scene, pink petals falling slowly, and the cowboy in a straw Easter bonnet with a pink ribbon and flowers (it replaces the cowboy hat) while the horse keeps its own ears and wears a small flower garland on its neck |
| Footer | "HAPPY EASTER" instead of "HAPPY TRAILS", pastel tint, flowers, three eggs, a chick, the hopping bunny, falling petals and the bonnet rider (2 pixels lower than the default, so the flowers on the bonnet stay inside the picture) |
| Wanted poster | A straw Easter bonnet with a ribbon and flowers replaces the cowboy hat in the portrait, flowers in the four corners, three painted eggs in the left margin, a chick sitting under the frame and pastel confetti in the free spaces. Everything stays clear of the text |
| Divider above "The town" | "HAPPY EASTER" on pastel bunting (pink, blue, yellow, lilac and mint flags), with flowers at both ends, two eggs on the string and confetti. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the dusk sky and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py easter --out docs/seasons/easter
```

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- It is a draft: the daily build ignores it until the owner approves (a test checks that too).
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB.

## Approval

- [ ] Owner reviewed the preview
- [ ] Owner commented "approved" on issue 53, or asked for changes
- [ ] Window confirmed: 7 days around Easter, calculated every year
