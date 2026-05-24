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
