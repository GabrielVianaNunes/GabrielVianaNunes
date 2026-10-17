# Western town 3D roadmap

Goal: replace the generic 3D contribution graph with a pixel art western town built from real contributions.

Budget: about 2 to 3 hours per week, due 31 Dec 2026. The work was finished ahead of the plan and released. Only the README switch is still to be merged.

## Status

| Planned week | Issue | Estimate | Status |
|---|---|---|---|
| 19 Oct | 1. Spike: contribution data and mapping rules | 1 h | Done |
| 26 Oct | 2. Design the town: palette, building set and sizes | 3 h | Done |
| 2 Nov | 3. Fetch the contribution calendar through GraphQL | 2 h | Done |
| 9 Nov | 4. Layout engine: weeks to street plan | 3 h | Done |
| 16 Nov | 5. Draw the building sprites | 4 h | Done |
| 23 Nov | 6. Render the street as one SVG | 4 h | Done |
| 30 Nov | 7. Ambient animations | 3 h | Done |
| 7 Dec | 8. Workflow: daily build, publish to output | 1 h | Done |
| 14 Dec | 9. README integration and fallback | 1 h | Ready, waiting to be merged |
| 21 Dec | 10. Documentation and wiki | 2 h | Done |
| Not planned | Retire the old 3D workflow | | Cancelled: the owner keeps both views |

## How it ships

The town stayed on `develop` until it was verified, then followed `docs/town/RELEASE.md`: release the code, try the workflow with `output-preview`, check the result, go live. The classic graph stays under the town, collapsed.

## What the fallback means

If anything fails, nothing is published and the previous good files stay live. The README only changes in the last step.

## Future improvements (not in v1)

Cemetery, windmill, train on the horizon, a year selector for older towns and an isometric view. They are tracked as issues with the `future` label under the milestone "Western Town 3D later".

## Principles

- Pure layout function, easy to test with a fixture
- Static drawing first, animation after
- Keep the old graph until the new one is verified
- Keep each SVG under 120 KB
- Write security rules as tests
