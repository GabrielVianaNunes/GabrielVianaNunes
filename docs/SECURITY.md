# Security and privacy

This repository is public, its Action logs are public and anything written to the `output` branch is public. The rules below keep private information out of all three.

## What is public on purpose

| Item | Detail |
|---|---|
| Pixel art, quotes, scripts, docs | Content and code of this repository |
| The 3D contribution graph | Counts and dates only, generated from the public contribution calendar |
| Commit author name | Gabriel Nunes, with the GitHub noreply address |
| Birthday decoration (planned) | Day and month only, never the year or the age, and only with the owner's explicit OK |

## What must never become public

- Names, URLs or descriptions of private repositories
- Titles of private issues, pull requests or commits
- Raw API responses that include restricted fields
- Tokens, keys and any value from a secret store
- A personal email address in commit metadata

## Supply chain

| Control | State |
|---|---|
| Third party actions pinned to a full commit SHA | Done in all workflows, the version is kept in a comment |
| Dependabot updates for GitHub Actions | Weekly, targeting `develop`, reviewed in a pull request |
| Secret scanning and push protection | Enabled on the repository |
| Least privilege `permissions` in workflows | `contents: write` only where a branch is pushed |
| Untrusted values in shell | Passed through `env`, never interpolated into the script |

## Guarded by tests

The rules are enforced by `tests/test_workflows.py`, which fails the build if:

- any action is not pinned to a full commit SHA
- a workflow uses `pull_request_target` or `workflow_run`
- permissions are missing or broader than needed
- an expression such as event data or an input is placed inside a shell script instead of an environment variable
- a workflow pushes anywhere other than the `output` branch

The season calendar validates its configuration and fails closed: a malformed `data/seasons.json` is an error, not a guess.

## Visitor privacy

Images are served through GitHub's image proxy, so third party services such as the visit counter only see the proxy and not the visitor's address or browser. For the same reason the counter counts image loads, not people, and nobody can be identified through it.

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
