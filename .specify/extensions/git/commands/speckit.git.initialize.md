---
description: "initialize a git repository with an initial commit"
---

# initialize git repository

initialize a git repository in the current project directory if one does not already exist.

## execution

run the appropriate script from the project root:

- **bash**: `.specify/extensions/git/scripts/bash/initialize-repo.sh`
- **powershell**: `.specify/extensions/git/scripts/powershell/initialize-repo.ps1`

if the extension scripts are not found, fall back to:
- **bash**: `git init && git add . && git commit -m "initial commit from specify template"`
- **powershell**: `git init; git add .; git commit -m "initial commit from specify template"`

the script handles all checks internally:
- skips if git is not available
- skips if already inside a git repository
- runs `git init`, `git add .`, and `git commit` with an initial commit message

## customization

replace the script to add project-specific git initialization steps:
- custom `.gitignore` templates
- default branch naming (`git config init.defaultbranch`)
- git lfs setup
- git hooks installation
- commit signing configuration
- git flow initialization

## output

on success:
- `✓ git repository initialized`

## graceful degradation

if git is not installed:
- warn the user
- skip repository initialization
- the project continues to function without git (specs can still be created under `specs/`)

if git is installed but `git init`, `git add .`, or `git commit` fails:
- surface the error to the user
- stop this command rather than continuing with a partially initialized repository
