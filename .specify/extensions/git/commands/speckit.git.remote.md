---
description: "detect git remote url for github integration"
---

# detect git remote url

detect the git remote url for integration with github services (e.g., issue creation).

## prerequisites

- check if git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- if git is not available, output a warning and return empty:
  ```
  [specify] warning: git repository not detected; cannot determine remote url
  ```

## execution

run the following command to get the remote url:

```bash
git config --get remote.origin.url
```

## output

parse the remote url and determine:

1. **repository owner**: extract from the url (e.g., `github` from `https://github.com/github/spec-kit.git`)
2. **repository name**: extract from the url (e.g., `spec-kit` from `https://github.com/github/spec-kit.git`)
3. **is github**: whether the remote points to a github repository

supported url formats:
- https: `https://github.com/<owner>/<repo>.git`
- ssh: `git@github.com:<owner>/<repo>.git`

> [!caution]
> only report a github repository if the remote url actually points to github.com.
> do not assume the remote is github if the url format doesn't match.

## graceful degradation

if git is not installed, the directory is not a git repository, or no remote is configured:
- return an empty result
- do not error — other workflows should continue without git remote information
