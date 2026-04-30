---
description: validate current branch follows feature branch naming conventions
---


<!-- extension: git -->
<!-- config: .specify/extensions/git/ -->
# validate feature branch

validate that the current git branch follows the expected feature branch naming conventions.

## prerequisites

- check if git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- if git is not available, output a warning and skip validation:
  ```
  [specify] warning: git repository not detected; skipped branch validation
  ```

## validation rules

get the current branch name:

```bash
git rev-parse --abbrev-ref head
```

the branch name must match one of these patterns:

1. **sequential**: `^[0-9]{3,}-` (e.g., `001-feature-name`, `042-fix-bug`, `1000-big-feature`)
2. **timestamp**: `^[0-9]{8}-[0-9]{6}-` (e.g., `20260319-143022-feature-name`)

## execution

if on a feature branch (matches either pattern):
- output: `✓ on feature branch: <branch-name>`
- check if the corresponding spec directory exists under `specs/`:
  - for sequential branches, look for `specs/<prefix>-*` where prefix matches the numeric portion
  - for timestamp branches, look for `specs/<prefix>-*` where prefix matches the `yyyymmdd-hhmmss` portion
- if spec directory exists: `✓ spec directory found: <path>`
- if spec directory missing: `⚠ no spec directory found for prefix <prefix>`

if not on a feature branch:
- output: `✗ not on a feature branch. current branch: <branch-name>`
- output: `feature branches should be named like: 001-feature-name or 20260319-143022-feature-name`

## graceful degradation

if git is not installed or the directory is not a git repository:
- check the `specify_feature` environment variable as a fallback
- if set, validate that value against the naming patterns
- if not set, skip validation with a warning