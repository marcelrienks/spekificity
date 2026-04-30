---
description: auto-commit changes after a spec kit command completes
---


<!-- extension: git -->
<!-- config: .specify/extensions/git/ -->
# auto-commit changes

automatically stage and commit all changes after a spec kit command completes.

## behavior

this command is invoked as a hook after (or before) core commands. it:

1. determines the event name from the hook context (e.g., if invoked as an `after_specify` hook, the event is `after_specify`; if `before_plan`, the event is `before_plan`)
2. checks `.specify/extensions/git/git-config.yml` for the `auto_commit` section
3. looks up the specific event key to see if auto-commit is enabled
4. falls back to `auto_commit.default` if no event-specific key exists
5. uses the per-command `message` if configured, otherwise a default message
6. if enabled and there are uncommitted changes, runs `git add .` + `git commit`

## execution

determine the event name from the hook that triggered this command, then run the script:

- **bash**: `.specify/extensions/git/scripts/bash/auto-commit.sh <event_name>`
- **powershell**: `.specify/extensions/git/scripts/powershell/auto-commit.ps1 <event_name>`

replace `<event_name>` with the actual hook event (e.g., `after_specify`, `before_plan`, `after_implement`).

## configuration

in `.specify/extensions/git/git-config.yml`:

```yaml
auto_commit:
  default: false          # global toggle — set true to enable for all commands
  after_specify:
    enabled: true          # override per-command
    message: "[spec kit] add specification"
  after_plan:
    enabled: false
    message: "[spec kit] add implementation plan"
```

## graceful degradation

- if git is not available or the current directory is not a repository: skips with a warning
- if no config file exists: skips (disabled by default)
- if no changes to commit: skips with a message