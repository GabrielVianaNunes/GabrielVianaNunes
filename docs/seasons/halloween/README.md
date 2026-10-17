# Halloween design (for approval)

Issue 45. The default western look stays. This only adds a ghost town mood on top of it.

Window: 24 Oct to 2 Nov (decided by the owner).

## What is added

| Asset | Decoration |
|---|---|
| Banner | A big orange harvest moon with craters, three bats flying across with flapping wings, glowing jack o'lanterns (one large, four small) that flicker, two tombstones, low drifting fog, a cobweb in the top right corner, a spider that climbs up and down its thread, and a skeleton cowboy on a horse with a glowing eye and a pale ghostly trail |
| Footer | "SPOOKY TRAILS" instead of "HAPPY TRAILS", two bats, two glowing pumpkins and the same skeleton rider |
| Wanted poster | A cobweb in the top left corner, a spider on a thread, and a glowing jack o'lantern sitting on the corner of the portrait frame |
| Divider above "The town" | A garland of orange, purple and bone colored flags with two glowing lanterns and a cobweb at each end. It replaces the normal divider and has exactly its size, so the layout does not move. This is the "strip" of the design preview, made the same size as the divider and with small lanterns instead of pumpkins |

What does not change: the name and role text, the cowboy portrait, the dusk sky, the colors of the rest of the page and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py halloween --out docs/seasons/halloween
```

Open the SVGs in a browser, through an `img` tag, so the animation runs.

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB (the banner is about 65 KB).

## Approval

- [x] Owner reviewed the preview
- [x] Owner approved on issue 45
- [x] Window confirmed: 24 Oct to 2 Nov

Built in issue 46: the season is wired to the calendar engine and to the daily workflow `Seasonal assets`.
