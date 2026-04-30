---
description: "create a feature branch with sequential or timestamp numbering"
---

# create feature branch

create and switch to a new git feature branch for the given specification. this command handles **branch creation only** — the spec directory and files are created by the core `/speckit.specify` workflow.

## user input

```text
$arguments
```

you **must** consider the user input before proceeding (if not empty).

## environment variable override

if the user explicitly provided `git_branch_name` (e.g., via environment variable, argument, or in their request), pass it through to the script by setting the `git_branch_name` environment variable before invoking the script. when `git_branch_name` is set:
- the script uses the exact value as the branch name, bypassing all prefix/suffix generation
- `--short-name`, `--number`, and `--timestamp` flags are ignored
- `feature_num` is extracted from the name if it starts with a numeric prefix, otherwise set to the full branch name

## prerequisites

- verify git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- if git is not available, warn the user and skip branch creation

## branch numbering mode

determine the branch numbering strategy by checking configuration in this order:

1. check `.specify/extensions/git/git-config.yml` for `branch_numbering` value
2. check `.specify/init-options.json` for `branch_numbering` value (backward compatibility)
3. default to `sequential` if neither exists

## execution

generate a concise short name (2-4 words) for the branch:
- analyze the feature description and extract the most meaningful keywords
- use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- preserve technical terms and acronyms (oauth2, api, jwt, etc.)

run the appropriate script based on your platform:

- **bash**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`
- **bash (timestamp)**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --timestamp --short-name "<short-name>" "<feature description>"`
- **powershell**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -json -shortname "<short-name>" "<feature description>"`
- **powershell (timestamp)**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -json -timestamp -shortname "<short-name>" "<feature description>"`

**important**:
- do not pass `--number` — the script determines the correct next number automatically
- always include the json flag (`--json` for bash, `-json` for powershell) so the output can be parsed reliably
- you must only ever run this script once per feature
- the json output will contain `branch_name` and `feature_num`

## graceful degradation

if git is not installed or the current directory is not a git repository:
- branch creation is skipped with a warning: `[specify] warning: git repository not detected; skipped branch creation`
- the script still outputs `branch_name` and `feature_num` so the caller can reference them

## output

the script outputs json with:
- `branch_name`: the branch name (e.g., `003-user-auth` or `20260319-143022-user-auth`)
- `feature_num`: the numeric or timestamp prefix used
