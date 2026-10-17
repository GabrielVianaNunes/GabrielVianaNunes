# Releasing the seasonal decorations

The seasonal files live on the `output` branch and the README points to them. The order below means the
profile never shows a broken image, and the look does not change until a window opens.

## Before you start

- The season build pull request is merged into `develop` and the Tests workflow is green.
- The pull request that switches the README is still a draft and still unmerged.

## Steps

### 1. Release the code, not the README

Open a pull request from `develop` to `main` and merge it. The new workflow now exists on `main` (workflows
only run from the default branch). The profile does not change.

### 2. Try it without touching anything live

In Actions open "Seasonal assets", choose Run workflow, set target to `output-preview` and season to
`halloween`. Expected: all steps green and a branch `output-preview` with four files, `banner.svg`,
`footer.svg`, `wanted.svg` and `divider-town.svg`, all with the Halloween decoration.

Check the four raw files in a browser: the banner has the orange moon and the skeleton rider, the divider is
the garland, and nothing covers the name and role text.

### 3. Publish today's real files

Run "Seasonal assets" again with target `output` and the season field empty. Outside a window these four files
are exactly the current look, so nothing changes visually.

### 4. Switch the README

Mark the draft pull request "Show the seasonal assets in the profile" as ready, merge it into `develop`, then
release `develop` into `main`. Refresh the profile on desktop and on a phone. It should look exactly as before.

### 5. The season turns on by itself

From then on the workflow runs every day at 03:05 UTC, which is 00:05 in America/Sao_Paulo. On 24 Oct the
Halloween decoration appears, on 3 Nov it disappears, and so on for every season in `data/seasons.json`.

Then delete the `output-preview` branch.

## If something goes wrong

| Symptom | What to do |
|---|---|
| A broken image on the profile | Revert the README pull request on `main`. The previous look returns |
| The workflow fails | Nothing was published, the previous files stay live. Read the failing step |
| The wrong season shows | Check `python scripts/seasons.py --date YYYY-MM-DD`, then fix `data/seasons.json` |
| An old image still shows | GitHub caches images for a few minutes. Wait, or hard refresh |
| A decoration looks wrong | Preview with the workflow target `output-preview` and the season field, fix on a `feature/` branch |
