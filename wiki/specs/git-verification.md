# ATOMIC SPECIFICATION: Git Verification (C4.3)

**Status:** ATOMIC SPECIFICATION  
**Type:** Skill Component — Git State Validation  
**Depends On:** None  
**Used By:** /spek.prepare (Step 1), /spek.implement (precondition)  

---

## Overview

Validates git repository state (clean working dir, valid branch, repo exists).

---

## Validation Checks

### Check 1: Repository Exists
- `git rev-parse --git-dir`
- If fails: "Not a git repository" → halt

### Check 2: Working Directory Clean
- `git status --porcelain`
- If output non-empty: uncommitted changes exist
  - Prompt: "Uncommitted changes. Stash or commit? (y/n)"
  - If yes: `git stash`
  - If no: error, halt
- Option: `--force-dirty` flag to skip check

### Check 3: Valid Branch
- `git rev-parse --abbrev-ref HEAD`
- If "HEAD": detached HEAD → warn but allow
- If "main" or "develop": warn "On main/develop. Create feature branch? (y/n)"
  - If yes: prompt for branch name → create
  - If no: allow (for quick fixes on main)

### Check 4: No Conflicting Branches
- `git branch --list [feature-name]`
- If branch already exists: error or prompt

---

## Success Criteria

✅ Repo exists  
✅ Working directory clean (or stashed)  
✅ On valid branch  
✅ No conflicts  

---

## Implementation Checklist

- [ ] Check repo exists
- [ ] Check working dir clean
- [ ] Check valid branch
- [ ] Handle conflicts gracefully

---

## References

**Related Specs:**
- [prepare-command.md](prepare-command.md) — Used in Step 1
- [feature-state-tracking.md](feature-state-tracking.md) — Feature state after validation

**External:**
- [extracted spec Git State Verification](prepare-and-post-skills.md#step-1-verify-git-state)
