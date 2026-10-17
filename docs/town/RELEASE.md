# Releasing the western town

The town is built on `develop` and reaches the profile only when everything works. Releasing in this order means the profile never shows a broken image.

## Before you start

- All town pull requests are merged into `develop` (they were stacked, so merge them in order and GitHub retargets each one for you).
- The Tests workflow is green on `develop`.
- The draft pull request that switches the README is still a draft and still unmerged.

## Steps

### 1. Release the code, not the README

Open a pull request from `develop` to `main` and merge it. At this point `main` has the scripts, the workflow and the docs, but the README still shows the old 3D graph. Nothing changes on the profile.

If `develop` already contains the README switch by mistake, stop and revert that one commit first.

### 2. Try the workflow without touching anything live

In Actions, open "Western town", choose Run workflow, set target to `output-preview` and run it. Expected result: all steps green and a new branch `output-preview` with two files:

- `western-town-day.svg`
- `western-town-night.svg`

### 3. Look at the result

Open the two raw files in a browser and check:

- the day file looks like daylight, the night file like dusk with lit windows
- there is one sheriff office, one bank and at most two churches
- the water tower stands behind the busiest week
- the rider and the tumbleweed move, and nothing is cut off at the edges
- the caption shows the right number of contributions
- the files are under 120 KB each

### 4. Go live

1. Run "Western town" again with target `output`. The two files now exist on the `output` branch.
2. Mark the draft pull request "Show the western town in the profile" as ready, merge it into `develop`, then release `develop` into `main`.
3. Refresh the profile on desktop and on a phone, in light and in dark mode. Give GitHub a few minutes if an old image is cached.

### 5. After a week

If the daily workflow succeeded every day, do the cleanup issue: delete the old 3D workflow and the `profile-3d-contrib` folder on `output`.

## If something goes wrong

| Symptom | What to do |
|---|---|
| Broken image on the profile | Revert the README pull request on `main`. The old graph returns |
| Workflow fails | Nothing was published. Read the failing step. The previous files stay live |
| Town looks wrong | Fix on a `feature/` branch, merge into `develop`, run with `output-preview`, then release |
| The profile still shows an old image | GitHub caches images. Wait, or rename the file as a last resort |
