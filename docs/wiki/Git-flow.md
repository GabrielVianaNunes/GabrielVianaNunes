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

## Generated files

Workflows publish to `output`. `develop` does not need them.
