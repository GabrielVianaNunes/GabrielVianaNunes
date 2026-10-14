"""Builds assets/stack.svg: the whole tech stack as ONE image.

skillicons.dev has no Power BI icon, and a separate fixed size image next to the strip
looks out of proportion on phones, because the strip shrinks to fit and the extra icon does not.
Putting every icon in one SVG makes them scale together on any screen.

Needs network access (it downloads the strip once). The result is committed.
Run:  python scripts/build_stack.py
"""
import os
import re
import urllib.request

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stack-row.svg")
IDS = "java,spring,py,rust,ts,js,react,angular,nodejs,postgres,docker,git,githubactions,aws"
STEP = 300   # distance between icons in skillicons user units
SIZE = 256   # icon size in the same units


def powerbi_tile(x):
    k = SIZE / 48.0
    bars = [(11, 26, 7, 12, "#E8A800"), (20.5, 18, 7, 20, "#F2C811"), (30, 10, 7, 28, "#FFD84A")]
    parts = [f'<g transform="translate({x}, 0)">',
             f'<rect width="{SIZE}" height="{SIZE}" rx="{10 * k:.1f}" fill="#242938"/>']
    for bx, by, bw, bh, c in bars:
        parts.append(f'<rect x="{bx * k:.1f}" y="{by * k:.1f}" width="{bw * k:.1f}" '
                     f'height="{bh * k:.1f}" rx="{1.5 * k:.1f}" fill="{c}"/>')
    parts.append("</g>")
    return chr(10).join(parts)


def main():
    req = urllib.request.Request(f"https://skillicons.dev/icons?i={IDS}&theme=dark",
                                 headers={"User-Agent": "Mozilla/5.0"})
    svg = urllib.request.urlopen(req).read().decode("utf-8")
    n = len(IDS.split(","))
    total = STEP * (n + 1) - (STEP - SIZE)
    x = STEP * n
    width_px = round(total * 48 / SIZE, 2)
    head = (f'<svg width="{width_px}" height="48" viewBox="0 0 {total} {SIZE}" fill="none" '
            'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'role="img" aria-label="Tech stack">')
    inner = re.sub(r"^\s*<svg[^>]*>", "", svg.strip(), count=1)
    inner = re.sub(r"</svg>\s*$", "", inner)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(head + inner + chr(10) + powerbi_tile(x) + chr(10) + "</svg>" + chr(10))
    print("wrote", os.path.normpath(OUT), "icons:", n + 1, "width_px:", width_px)


if __name__ == "__main__":
    main()
