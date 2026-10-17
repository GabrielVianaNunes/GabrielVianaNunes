# Regenerating assets

Requires Python 3.12 and nothing else.

## Pixel art

```bash
python scripts/build_assets.py
```

Writes banner, wanted poster, footer, divider, heading icons and the Power BI tile into `assets/`.

## Stack row

```bash
python scripts/build_stack.py
```

Downloads the skillicons strip once and adds the custom Power BI tile, writing `assets/stack-row.svg`. This is the only script that needs network access. Edit the `IDS` list to change the icons.

## Contribution data

```bash
GITHUB_TOKEN=... python scripts/fetch_contributions.py --user NAME --out data/contributions.json
python -m unittest discover -s tests
```

Writes a reduced weekly list (start date and total). `data/contributions-fixture.json` is a committed copy of real data, used by tests and for drawing without the network. The script exits with an error and writes nothing if the data fails validation.

## Quote card

```bash
python scripts/update_quote.py            # quote for the current week
python scripts/update_quote.py --index 3  # force one, useful for previews
```

The quote is picked by counting weeks since a fixed Monday, so none repeats until the list is exhausted.

## Adding a quote

Append an object with `text`, `author` and `context` to `data/quotes.json`. Check the attribution first.

## Previewing

Open an SVG in a browser. For the animated ones, load them through an `img` tag so the CSS animation runs.
