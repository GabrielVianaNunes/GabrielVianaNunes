# Christmas design (for approval)

Issue 47. The default western look stays. This only adds a snowy Christmas at dusk on top of it.

Window: 3 Nov (right after the Halloween decoration ends) to 25 Dec (decided by the owner).

## What is added

| Asset | Decoration |
|---|---|
| Banner | Snow falling in two layers, snow on the mesas, on the roofs of the little town and on the ground, two Christmas trees with a gold star and twinkling ornaments, three presents, colored lights on the rooftops, a string of twinkling lights along the top edge, and the cowboy in a red Santa cap with jingling bells on the horse. The cap replaces the cowboy hat |
| Footer | "MERRY TRAILS" instead of "HAPPY TRAILS", falling snow, snow on the ground, a tree, two presents, a string of lights and the Santa cap rider. The rider sits 1 pixel lower than in the default footer, because it bobs up by 1 pixel on every step, so the cap stays fully inside the footer in both frames of the ride |
| Wanted poster | A pine garland all around the border of the poster with red, gold and blue ornaments, twinkling lights, snow on the top edge and a red bow in each corner. The cowboy portrait wears a full Santa cap instead of the cowboy hat. The garland stays on the border and never touches the text or the portrait |
| Divider above "The town" | A pine garland with red, gold and blue ornaments, twinkling lights, snow and a red bow at each end. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the cowboy portrait, the dusk sky, the colors of the rest of the page and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py christmas --out docs/seasons/christmas
```

Open the SVGs in a browser, through an `img` tag, so the animation runs.

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB (the banner is about 66 KB).

## Approval

- [ ] Owner reviewed the preview
- [ ] Owner commented "approved" on issue 47, or asked for changes
- [ ] Window confirmed: 3 Nov to 25 Dec
