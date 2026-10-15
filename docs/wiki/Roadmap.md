# Western town 3D roadmap

Goal: replace the generic 3D contribution graph with a pixel art western town built from real contributions.

Budget: about 2 to 3 hours per week, ten small issues, due 31 Dec 2026.

| Week | Issue | Estimate |
|---|---|---|
| 19 Oct | Spike: contribution data and mapping rules | 1 h |
| 26 Oct | Design the town: palette, building set and sizes | 3 h |
| 2 Nov | Fetch the contribution calendar through GraphQL | 2 h |
| 9 Nov | Layout engine: weeks to street plan | 3 h |
| 16 Nov | Draw the building sprites | 4 h |
| 23 Nov | Render the street as one SVG | 4 h |
| 30 Nov | Ambient animations | 3 h |
| 7 Dec | Workflow: daily build, publish to output | 1 h |
| 14 Dec | README integration and fallback | 1 h |
| 21 Dec | Documentation and wiki | 2 h |

About 24 hours in total, with the last ten days of December as buffer.

## Future improvements (not in v1)

Cemetery, windmill, train on the horizon, a year selector for older towns and an isometric view. They are tracked as issues with the `future` label under the milestone "Western Town 3D later".

## Principles

- Pure layout function, easy to test with a fixture
- Static drawing first, animation after
- Keep the old graph as a fallback until the new one is verified
- Keep the SVG under 300 KB

## Tracking

Issues live under the milestone "Western Town 3D v1" and the project "Western Town 3D".
