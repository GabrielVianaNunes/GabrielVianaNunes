# Security and privacy

This repository is public, its Action logs are public and anything written to the `output` branch is public. The rules below keep private information out of all three.

## What is public on purpose

| Item | Detail |
|---|---|
| Weekly contribution totals | Counts and dates only, the same numbers the profile graph already shows |
| Quotes, pixel art, scripts | Content and code of this repository |
| Commit author name | Gabriel Nunes, with the GitHub noreply address |

## What must never become public

- Names, URLs or descriptions of private repositories
- Titles of private issues, pull requests or commits
- Raw API responses that include restricted fields
- Tokens, keys and any value from a secret store
- A personal email address in commit metadata

## Rules for the western town data

The fetch step (issue 3) must follow these rules:

1. Ask the GraphQL API only for `contributionCalendar` (dates and counts). Never request repositories, issue titles or commit messages.
2. Never print the API response or the token in logs. Print totals only.
3. Do not commit raw API responses. Only the reduced weekly list may be stored, and only as a fixture.
4. Use the built in `GITHUB_TOKEN` first. If private contributions are not visible, use a fine grained personal access token with the minimum read permission, stored as a repository secret.
5. Run only on `schedule` and `workflow_dispatch`. No `pull_request_target`, no fork triggered runs, so a stranger can never reach the secret.
6. Validate the data before drawing: expect integers from 0 up to a sane limit and fail closed if not.

## Supply chain

| Control | State |
|---|---|
| Third party actions pinned to a full commit SHA | Done in all workflows, the version is kept in a comment |
| Dependabot updates for GitHub Actions | Weekly, targeting `develop`, reviewed in a pull request |
| Secret scanning and push protection | Enabled on the repository |
| Least privilege `permissions` in workflows | `contents: write` only where a branch is pushed |
| Untrusted values in shell | Passed through `env`, never interpolated into the script |

## Guarded by tests

The rules above are enforced by `tests/test_workflows.py`, which fails the build if:

- any action is not pinned to a full commit SHA
- a workflow uses `pull_request_target` or `workflow_run`
- permissions are missing or broader than needed
- an expression such as event data or an input is placed inside a shell script instead of an environment variable
- the town workflow could push to `main` or `develop`, or publish before the tests, fetch and build have run
- the token is given to any step other than the fetch step

The fetch script has its own tests: it rejects out of range values, extra keys and non consecutive weeks, never includes the token or the response body in an error, and keeps the previous file on failure.

## Safe testing before release

The town workflow has a manual target `output-preview`. It publishes to a separate branch, so the live files are never touched while testing. Any failing step stops the run before anything is published.

## Visitor privacy

Images are served through GitHub's image proxy, so third party services such as the visit counter only see the proxy and not the visitor's address or browser.

## Commit identity

Commits are authored with `132621864+GabrielVianaNunes@users.noreply.github.com`. Before 2026-10-15 some commits used a personal email address. They are still in the history. Options are listed in the next section.

## Audit of 2026-10-15

| Check | Result |
|---|---|
| Secrets in files and history | None found |
| Personal data in tracked files | None found |
| Workflow triggers from forks | None |
| Third party actions unpinned | 1 found (`@latest`), fixed |
| Personal email in commit history | 16 commits, new commits fixed, history needs a decision |

## Decisions that belong to the owner

1. Turn on "Block command line pushes that expose my email" in the GitHub email settings so a personal address can never be pushed again.
2. Decide whether to rewrite the history of the 16 old commits. It needs a force push on `main` and `develop`, changes every commit hash and also applies to the wiki repository. The risk it removes is mild (the address is visible, not a credential), so leaving it is acceptable.
3. Optionally enable Dependabot alerts in the repository security settings.
