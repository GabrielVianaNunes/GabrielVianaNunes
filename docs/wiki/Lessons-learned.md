# Lessons learned

Things that cost time on this project, so they do not cost it twice.

## GitHub and images

| What happened | Lesson |
|---|---|
| A fixed footer still showed the old dark image | GitHub caches images by file name. Rename the file to bust the cache |
| The visit counter showed a broken icon on phones | Third party images go through GitHub's image proxy, which gives up early. Slow services fail through it even if they work directly. Test through the proxy, not only directly |
| A separate Power BI icon looked huge on phones | The skillicons strip shrinks to fit the screen and a fixed size image does not. Put icons that sit together into one SVG so they scale together |
| A missing icon left a black gap | skillicons.dev has no Power BI icon and answers with an empty SVG, not an error. Check that every icon actually renders |
| A counter cannot count unique visitors | The image proxy hides the visitor, so a third party only sees the proxy. It counts loads, not people |

## Git and Actions

| What happened | Lesson |
|---|---|
| Protecting `main` with required pull requests blocked the workflows | GitHub does not allow the Actions app as a bypass actor on personal repositories. Publish generated files to a separate `output` branch |
| Two workflows ran at the same time and one push was rejected | Share a `concurrency` group and always fetch before pushing |
| `@latest` for a third party action | A compromised release would run with write access. Pin every action to a full commit SHA and let Dependabot propose updates |
| A workflow cannot be tried before it is on the default branch | Release the code first, then run the workflow manually |
| Merging a feature into `develop` did not change the profile | The profile only changes after `develop` is merged into `main` |
| A cherry picked hotfix conflicted later | Copying a commit duplicates work that conflicts when both sides change. Make a hotfix on `main` and merge `main` back into `develop` |
| Commits carried a personal email address | Set the repository email to the GitHub noreply address and turn on the setting that blocks pushes that expose an email |
| A stacked pull request got stuck as conflicting | A workflow that deletes the base branch does not make GitHub retarget the pull request. Point every pull request at `develop` and merge oldest first |

## Process

- **Show a rough preview of the final look before building the whole pipeline.** A pixel art 2D town was built end to end, tested and released, and then the owner preferred the original 3D graph. The data, layout and renderer were solid, but a one hour mock up would have shown the look sooner.
- Keep a pull request that changes the live look as a draft until the files it points to exist, and keep a one step way back (revert the pull request).
- Write the security rules as tests. The workflow guard tests fail if an action is unpinned or an untrusted expression reaches a shell script.
- Verify moving dates with independent algorithms and a day by day oracle, not with a sample table.
