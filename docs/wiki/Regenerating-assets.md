# Regenerating assets

Requires Python 3.12. Only `build_stack.py` and `fetch_contributions.py` need the network.

## Run the tests

```bash
python -m unittest discover -s tests
```

## Pixel art for the profile

```bash
python scripts/build_assets.py
```

Writes banner, wanted poster, footer, divider and the heading icons into `assets/`.

## Stack row

```bash
python scripts/build_stack.py
```

Downloads the skillicons strip once and adds the custom Power BI tile, writing `assets/stack-row.svg`. Edit the `IDS` list to change the icons.

## Quote card

```bash
python scripts/update_quote.py            # quote for the current week
python scripts/update_quote.py --index 3  # force one, useful for previews
```

To add a quote, append an object with `text`, `author` and `context` to `data/quotes.json` and check the attribution first.

## Western town

```bash
# 1. fetch real data (needs a token, never print it)
GITHUB_TOKEN=... python scripts/fetch_contributions.py --user NAME --out data/contributions.json

# 2. build both SVGs from any weekly file, the committed fixture works offline
python scripts/build_town.py --input data/contributions-fixture.json --out dist

# 3. look at the sprites and the design
python scripts/town_contact_sheet.py     # docs/town/sprites-sheet.svg
python scripts/town_design_sheet.py      # docs/town/design-sheet.svg
```

Open the SVGs in a browser. Load animated ones through an `img` tag so the CSS animation runs.

## Changing the town

| I want to change | Edit |
|---|---|
| How weeks become buildings | `scripts/town_layout.py` and its tests |
| How a building looks | `scripts/town_sprites.py`, then regenerate the contact sheet |
| Colors | `scripts/town_palette.py` |
| Scenery or animation | `scripts/build_town.py` |

Always run the tests. They check the unique building rules, the size budget (120 KB per file), that no sprite floats, that the files have no external references and that reduced motion is respected.

## Trying the daily workflow safely

In Actions, run "Western town" with target `output-preview`. See `docs/town/RELEASE.md` for the full procedure.
