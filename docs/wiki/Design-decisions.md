# Design decisions

## Identity

A quiet minimalist cowboy. The design talks, the text stays short. Western culture is the common thread: dusk palette, sand and leather tones.

## Palette

| Role | Color |
|---|---|
| Night sky | `#1b1030`, `#2a1745`, `#46225a` |
| Dusk | `#7a2f5e`, `#b8465a`, `#e0675a` |
| Horizon | `#f0905a`, `#f7b867`, `#fbd48a` |
| Sand and wood | `#e6b36a`, `#c98b4a`, `#a6692f`, `#5a3a22` |
| Brass | `#e0b95e`, `#b8873a` |

## Rules

- Pixel art is drawn from code on a grid, never hand edited
- Every animation respects `prefers-reduced-motion`
- Keep the page light: few sections, short text
- The holster is always empty

## Why an output branch

Protecting `main` with required pull requests blocks workflow pushes, and GitHub does not allow the Actions app as a bypass actor on personal repositories. Publishing to `output` avoids the problem.

## Quotes

Only encouraging or humorous lines, with attribution that is widely credited. Anonymous sayings are labelled as such.
