# Birthday design (for approval)

Issue 49. The default western look stays. This only adds a party on top of it, with a touch of Christmas.

Window: only 28 Dec (decided by the owner). 26 and 27 Dec use the default look.

## Privacy

The decoration shows the greeting and nothing else. It never shows a year or an age, and a test checks that no text of any asset contains a digit. It does make the day and month of the birthday public, which the owner confirmed is fine.

## What is added

| Asset | Decoration |
|---|---|
| Banner | Seven balloons tied to piles of presents, swaying gently, a birthday cake with flickering candles, colored confetti falling, and the cowboy wearing a gold paper crown with jewels (it replaces the cowboy hat) while the horse wears a little party hat. The touch of Christmas: a decorated tree, presents and snow on the ground |
| Footer | "HAPPY BIRTHDAY" instead of "HAPPY TRAILS", balloons, a cake, confetti, a tree with presents and the crowned rider (2 pixels lower than the default, so the crown stays inside the picture) |
| Wanted poster | A striped party hat with a gold pompom replaces the cowboy hat in the portrait, confetti in the free spaces, three balloons in the left margin and a sprig of holly in each top corner. The balloons stay clear of the text |
| Divider above "The town" | "HAPPY BIRTHDAY" spelled on colorful bunting, with confetti along the string and holly at both ends. It replaces the normal divider and has exactly its size, so the layout does not move |

What does not change: the name and role text, the dusk sky and the layout.

## Files

| File | What |
|---|---|
| `banner.svg`, `footer.svg`, `wanted.svg`, `strip.svg` | The decorated assets (the strip becomes `divider-town.svg` on `output`) |
| `default/` | The default banner, footer and poster, for comparison |

Regenerate with:

```bash
python scripts/build_season_preview.py birthday --out docs/seasons/birthday
```

## Rules followed

- With no season the builders return exactly the current assets (a test checks it).
- It is a draft: the daily build ignores it until the owner approves.
- No scripts and no external references, all animation stops with reduced motion.
- Every file is under 150 KB.

## Approval

- [x] The owner confirmed that publishing the day and month is fine
- [ ] Owner reviewed the preview
- [ ] Owner commented "approved" on issue 49, or asked for changes
- [ ] Window confirmed: 28 Dec only
