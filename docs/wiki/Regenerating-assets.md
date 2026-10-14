# Regenerating assets

Requires Python 3.12 and nothing else.

## Pixel art

```bash
python scripts/build_assets.py
```

Writes banner, wanted poster, footer, divider, heading icons and the Power BI tile into `assets/`.

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
