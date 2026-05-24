# Examples for 160-multi-developer-coordination

Consolidated branch-name examples from `wiki/specs/160-multi-developer-coordination.md`:

```
spek-<feature-name>-<developer-initials>

Examples:
- spek-add-logging-da (Developer A's logging feature)
- spek-add-tests-db (Developer B's tests feature)
- spek-latmd-integration-mc (Developer MC's lat.md work)
```

Invalid example:
- `feature/logging` (missing initials)
- `add_logging` (wrong separator)

---

## Source: 160-multi-developer-coordination-code-1.md

```markdown
# Team Coordination Checkins

## 2026-05-20

### Feature Start: "Add Logging" (Developer A, spek-add-logging-da)
- Scope: Core features (main.py, utils.py, config.py)
- Estimated duration: 3-4 hours
- Affected patterns: Error Handling, Code Organization
- Status: IN PROGRESS
- Link: https://github.com/...

### Feature Complete: "Add Tests" (Developer B, spek-add-tests-db)
- Scope: Test infrastructure (pytest setup)
- New decisions: Test coverage target = 80%
- New patterns: Mock strategy for SpecKit + lat.md
- Code review: Pending
- Status: AWAITING MERGE REVIEW
- Link: https://github.com/...

### Potential Conflicts Detected
- None flagged

---

## 2026-05-21

### Merge Complete: "Add Tests" (Developer B)
- Decisions merged: ✓ (test coverage 80% + mock strategy added)
- Patterns merged: ✓ (2 patterns + evidence links added)
- Lessons: vault/lessons/2026-05-21-add-tests-db.md
- Status: ✓ MERGED TO MAIN

### Feature In Progress: "Add Logging" (Developer A)
- Status: Awaiting implementation
- Code review ready: 2026-05-21 EOD expected
```

## Source: 160-multi-developer-coordination-code-2.md

```
Feature Start (Developer A):
1. /spek.prepare
	├─ Git: create feature branch (spek-<feature>-<dev-initials>)
	├─ Git: pull latest main (ensure fresh vault context)
	├─ Vault: load vault context (from main)
	├─ Memory: create vault/session/current-feature-a.md
	└─ Notification: Post feature start in vault/coordination/checkins.md

Feature Work (Developer A):
2. /spek.plan → /spek.implement
	├─ Work on feature branch (isolated from other devs)
	├─ Memory: update vault/session/current-feature-a.md
	└─ Vault: NO writes during feature (avoid conflicts)

Feature End (Developer A):
3. /spek.conclude
	├─ Lessons: generate vault/lessons/<date>-<feature>-a.md (LOCAL only, not in vault yet)
	├─ NEW: Draft decisions/patterns additions (vault-update-draft.md, LOCAL)
	└─ Git: commit everything to feature branch (branch contains: code + lessons + draft updates)

Feature Review + Merge (Team Lead or Async):
4a. Code review: `/spek.implement` output + code diff
4b. Vault review: Check draft decisions/patterns for conflicts
4c. Conflict resolution (if needed):
	- Manual review: Compare Developer A's new decisions vs. main's recent decisions
	- Merge strategy: Accept, reject, or modify + annotate
4d. Merge to main:
	- Git: squash feature branch → main
	- Git: also merge lessons + any draft updates → vault/
	- Vault: append new decisions/patterns (with conflict annotations if any)

Feature Archive:
5. vault/session/current-feature-a.md archived → vault/sessions/<date>-<feature>-a.md
```

