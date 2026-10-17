# Regenerating assets

Requires Python 3.12. Only `build_stack.py` needs the network.

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

## Seasons

```bash
python scripts/seasons.py                    # the season for today in America/Sao_Paulo
python scripts/seasons.py --date 2026-12-28  # for a given day
python scripts/seasons.py --year 2027        # every window of a year
```

To change a window, edit `data/seasons.json`. No code change is needed. The tests check the moving dates for every year up to 2099.

## Seasonal assets

```bash
python scripts/build_seasonal.py --out dist                     # today's season
python scripts/build_seasonal.py --out dist --date 2026-10-31   # a given day
python scripts/build_seasonal.py --out dist --season halloween  # force a season
python scripts/build_season_preview.py halloween --out docs/seasons/halloween  # design preview
```

Writes `banner.svg`, `footer.svg`, `wanted.svg` and `divider-town.svg`. Everything is checked before anything is written.

## Previewing

Open an SVG in a browser. Load animated ones through an `img` tag so the CSS animation runs.
