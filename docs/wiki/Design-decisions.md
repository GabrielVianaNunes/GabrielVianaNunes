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
- Never put a fixed size image next to a scaling one: on phones the row shrinks and the fixed one looks huge, so related icons live in one SVG
- When an image must change and the cache holds on, give the file a new name

## Why an output branch

Protecting `main` with required pull requests blocks workflow pushes, and GitHub does not allow the Actions app as a bypass actor on personal repositories. Publishing to `output` avoids the problem.

## Quotes

Only encouraging or humorous lines, with attribution that is widely credited. Anonymous sayings are labelled as such.

## Western town 3D: data and mapping rules

Decided in issue 1 (spike), from the real contribution calendar.

### What the data looks like

Measured on 2026-10-15 for the last year:

| Fact | Value |
|---|---|
| Weeks returned by `contributionCalendar` | 53 (the last one is partial, 5 days) |
| Weeks with zero contributions | 36 of 53 |
| Busiest week | 238 |
| Median of the non empty weeks | 39 |
| Busiest single day | 84 |
| Daily levels available | `NONE`, `FIRST` to `FOURTH_QUARTILE` |

Consequences:

- The distribution is very skewed, so a linear height scale would make one tower and many invisible shacks.
- Most weeks are empty, so "empty" must look good on purpose.
- The calendar only has counts and dates. It carries no repository names, so private work never leaks.

### Decisions

1. **Unit:** one lot per week, oldest on the left, newest on the right. 53 lots.
2. **Height:** based on the quartiles of the non empty weeks, not on the maximum. This keeps a good mix of heights every year.
3. **Empty weeks:** an empty lot with a cactus or a hitching post. Never a gap.
4. **Types:** decided by height, with a stable rotation by week position so the street does not change shape from day to day. Sheriff office and bank are unique, churches at most two.
5. **Landmarks:** the busiest week gets the water tower, and the current week gets a lit window.

### Mapping table

| Week total | Floors | Building |
|---|---|---|
| 0 | 0 | Empty lot with a cactus or hitching post |
| 1 up to the 25th percentile | 1 | Shack, barn or stable (rotates by week position) |
| up to the 50th percentile | 2 | Saloon, general store or blacksmith |
| up to the 75th percentile | 3 | Hotel, with at most 2 churches and only 1 sheriff office |
| above the 75th percentile | 4 | Grand hotel, with only 1 bank |

Unique buildings: sheriff office 1, bank 1, church up to 2, water tower 1. See `docs/town/DESIGN.md` for where each one is placed.

Percentiles are computed from the non empty weeks only. With today's data they are about 10, 39 and 73.

### Open risks, to check in the fetch issue

- Private contributions are counted in the calendar only when the profile setting allows it. The token used by the Action may see a different total than a logged in user. If it does, the fallback is a personal access token stored as a secret.
- The first and last weeks are partial. Both are kept, since showing the current week is the point.
