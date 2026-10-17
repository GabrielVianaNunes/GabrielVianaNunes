# Git flow

```
feature/name  ->  pull request to develop  ->  pull request from develop to main
```

## Steps

1. Update `develop` and branch from it: `feature/short-name`.
2. Commit small changes with clear messages.
3. Open a pull request into `develop` and merge it.
4. When ready to publish, open a pull request from `develop` into `main`.
5. Urgent fix: branch `hotfix/short-name` from `main`, merge into `main`, then into `develop`.

## Rules of thumb

- Never commit directly to `main` or `develop`
- One topic per branch
- Commit messages: short imperative title, optional body, no dashes
- Commits are authored by the owner only, no co author trailers

## Long running work

Larger pieces of work, like the western town, are built in small feature branches that merge into `develop`. They only go to `main` (and to `output`) when the whole thing is complete and verified. Until then the profile does not change.

## Stacked work

When one piece needs the previous one, branch from it but still open the pull request against `develop`, and merge oldest first. Never target another feature branch: the cleanup workflow deletes that branch after its merge and GitHub does not retarget the pull request, which then gets stuck.

## Branch cleanup

The workflow `delete-merged-branch.yml` deletes the head branch of a merged pull request when it starts with `feature/`, `hotfix/` or `bugfix/`. `develop`, `main` and `output` are never deleted.

## Generated files

Workflows publish to `output`. `develop` does not need them.
