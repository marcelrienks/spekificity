---
description: convert existing tasks into actionable, dependency-ordered github issues for the feature based on available design artifacts.
tools: ['github/github-mcp-server/issue_write']
---

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## pre-execution checks

**check for extension hooks (before tasks-to-issues conversion)**:
- check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.before_taskstoissues` key
- if the yaml cannot be parsed or is invalid, skip hook checking silently and continue normally
- filter out hooks where `enabled` is explicitly `false`. treat hooks without an `enabled` field as enabled by default.
- for each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - if the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - if the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the hookexecutor implementation
- for each executable hook, output the following based on its `optional` flag:
  - **optional hook** (`optional: true`):
    ```
    ## extension hooks

    **optional pre-hook**: {extension}
    command: `/{command}`
    description: {description}

    prompt: {prompt}
    to execute: `/{command}`
    ```
  - **mandatory hook** (`optional: false`):
    ```
    ## extension hooks

    **automatic pre-hook**: {extension}
    executing: `/{command}`
    execute_command: {command}

    wait for the result of the hook command before proceeding to the outline.
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## outline

1. run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse feature_dir and available_docs list. all paths must be absolute. for single quotes in args like "i'm groot", use escape syntax: e.g 'i'\''m groot' (or double-quote if possible: "i'm groot").
1. from the executed script, extract the path to **tasks**.
1. get the git remote by running:

```bash
git config --get remote.origin.url
```

> [!caution]
> only proceed to next steps if the remote is a github url

1. for each task in the list, use the github mcp server to create a new issue in the repository that is representative of the git remote.

> [!caution]
> under no circumstances ever create issues in repositories that do not match the remote url

## post-execution checks

**check for extension hooks (after tasks-to-issues conversion)**:
check if `.specify/extensions.yml` exists in the project root.
- if it exists, read it and look for entries under the `hooks.after_taskstoissues` key
- if the yaml cannot be parsed or is invalid, skip hook checking silently and continue normally
- filter out hooks where `enabled` is explicitly `false`. treat hooks without an `enabled` field as enabled by default.
- for each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - if the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - if the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the hookexecutor implementation
- for each executable hook, output the following based on its `optional` flag:
  - **optional hook** (`optional: true`):
    ```
    ## extension hooks

    **optional hook**: {extension}
    command: `/{command}`
    description: {description}

    prompt: {prompt}
    to execute: `/{command}`
    ```
  - **mandatory hook** (`optional: false`):
    ```
    ## extension hooks

    **automatic hook**: {extension}
    executing: `/{command}`
    execute_command: {command}
    ```
- if no hooks are registered or `.specify/extensions.yml` does not exist, skip silently
