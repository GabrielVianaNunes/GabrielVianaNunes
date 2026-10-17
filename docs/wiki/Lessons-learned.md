# Lessons learned

Things that cost time on this project, so they do not cost it twice.

## GitHub and images

| What happened | Lesson |
|---|---|
| A fixed footer still showed the old dark image | GitHub caches images by file name. Rename the file to bust the cache |
| The visit counter showed a broken icon on phones | Third party images go through GitHub's image proxy, which gives up early. Slow services fail through it even if they work directly. Test through the proxy, not only directly |
| A separate Power BI icon looked huge on phones | The skillicons strip shrinks to fit the screen and a fixed size image does not. Put icons that sit together into one SVG so they scale together |
| A missing icon left a black gap | skillicons.dev has no Power BI icon and answers with an empty SVG, not an error. Check that every icon actually renders |

## SVG

| What happened | Lesson |
|---|---|
| Sprites came out black in a contact sheet | CSS selectors with a scope such as `.d .wood` do not reach inside `<symbol>` clones. CSS variables inherit into `<use>`, so color with variables |
| A pixel by pixel drawing weighed 246 KB | Define each building once as a `<symbol>` and place it with `<use>`. The whole town is about 95 KB |
| Light colored buildings vanished against the day sky | Add a one pixel dark outline to every sprite |
| `prefers-color-scheme` inside an SVG follows the system, not GitHub's theme | Publish two files and let a `<picture>` element choose, because GitHub applies its own theme to `<picture>` |

## Git and Actions

| What happened | Lesson |
|---|---|
| Protecting `main` with required pull requests blocked the workflows | GitHub does not allow the Actions app as a bypass actor on personal repositories. Publish generated files to a separate `output` branch |
| Two workflows ran at the same time and one push was rejected | Share a `concurrency` group and always fetch before pushing |
| `@latest` for a third party action | A compromised release would run with write access. Pin every action to a full commit SHA and let Dependabot propose updates |
| A workflow cannot be tried before it is on the default branch | Release the code first, then run the workflow with the `output-preview` target |
| Merging a feature into `develop` did not change the profile | The profile only changes after `develop` is merged into `main` |
| Commits carried a personal email address | Set the repository email to the GitHub noreply address and turn on the setting that blocks pushes that expose an email |

## Data

| What happened | Lesson |
|---|---|
| A linear height scale would make one tower and many invisible shacks | Use quartiles of the non empty weeks |
| The Action token might not see private contributions | It does: the owner total and the anonymous graph total were identical, because the profile shows private activity as anonymous counts |
| One year of data is mostly empty weeks | Make empty lots look good on purpose (cactus, wagon, barrels, well) instead of leaving gaps |

## Process

- Stack branches (each issue from the previous one) when the next piece needs the last one, but point every pull request at `develop` from the start. A pull request whose base branch is deleted by a workflow is NOT retargeted by GitHub (only its own auto delete does that) and gets stuck as conflicting. Merge them oldest first.
- Keep the pull request that switches the README as a draft until the files it points to exist.
- Write the security rules as tests. The workflow guard tests fail if an action is unpinned or an untrusted expression reaches a shell script.
