# Multi-Developer & Concurrent Feature Work Strategy

**Status:** COMPLETE  
**Date:** 2026-05-20  
**Scope:** Team coordination patterns for 2+ developers + future scaling  
**Current Model:** Solo developer (defer full concurrency; use foundation pattern)  
**Future Model:** Async team with merge-based conflict resolution  
**Git Strategy:** Feature branches + async checkins  
**Vault Conflict Resolution:** Manual review merge (safe default)

---

## 1. Current State: Solo Developer Model

### 1.1 Solo Workflow (No Concurrent Features)

**Assumption:** One developer, one feature at a time, sequential feature work.

**Feature Lifecycle:**
```
1. /spek.prepare
   ├─ Git: create feature branch (spek-<feature>)
   ├─ Vault: load vault context (decisions, patterns)
   └─ Memory: create vault/session/

2. /spek.plan
   ├─ Feature work (specify → plan → implement)
   └─ Memory: update vault/session/

3. /spek.post
   ├─ Lessons: generate vault/lessons/<date>-<feature>.md
   ├─ Vault: append decisions + patterns to vault/decision.md + vault/patterns.md
   ├─ Git: commit "Feature: <name>" to feature branch
   └─ Memory: archive vault/session/ → vault/sessions/

4. Git: merge feature branch → main (or squash)
```

**Vault Conflict Risk:** NONE (solo developer, sequential features)

**State Isolation:** AUTOMATIC (feature branches separate changes; memory is session-scoped)

**Coordination Overhead:** MINIMAL (just follow the 4-step workflow)

---

### 1.2 Solo Developer Success Criteria

✅ Feature isolation via git feature branches  
✅ No vault conflicts (sequential changes, manual review before merge)  
✅ Session memory ephemeral (archived post-feature)  
✅ Vault grows incrementally (one feature → lesson + decisions + patterns per cycle)  
✅ Repo memory updated post-feature (compressed summaries)

---

## 2. Future State: Team Model (2+ Developers)

### 2.1 Team Workflow: Feature Branches + Async Checkins

**Assumption:** Multiple developers, potentially overlapping feature work, async coordination via git + vault.

**Feature Lifecycle (Team Version):**
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
3. /spek.post
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

**State Per Developer:**
```
Repo (main):
├─ vault/decision.md (shared, grows per feature)
├─ vault/patterns.md (shared, grows per feature)
├─ vault/lessons/<feature>.md (per feature, merged after approval)
├─ vault/coordination/checkins.md (async team log)
└─ vault/repo/ (compressed summaries, updated post-feature)

Feature Branch (spek-<feature>-<initials>):
├─ Code changes (feature implementation)
├─ vault/lessons/<date>-<feature>-<initials>.md (generated during /spek.post)
├─ vault-update-draft.md (proposed decisions + patterns)
└─ vault/session/current-feature-<initials>.md (local, deleted post-merge)
```

---

## 3. Vault Conflict Resolution Strategy

### 3.1 Conflict Types

#### 3.1.1 Type A: New Decision in Parallel (Low Risk)

**Scenario:** Developer A adds decision D1 while Developer B adds D2 (unrelated topics).

**Resolution:** ACCEPT BOTH
- Merge both decisions into vault/decision.md
- No annotation needed
- Both decisions stand

**Example:**
```
Developer A: "Use CodeGraph over Graphify for code intelligence"
Developer B: "Implement caveman compression for lessons"
Result: Both added to vault/decision.md (no conflict)
```

---

#### 3.1.2 Type B: Contradicting Decisions (Medium Risk)

**Scenario:** Developer A says "Use pattern X", Developer B says "Avoid pattern X".

**Resolution:** MANUAL REVIEW + ANNOTATE
- Reviewer decides which wins (or if both coexist)
- Add annotation to both decisions (timestamp + reasoning)
- Mark older decision as "superceded" (don't delete)

**Example:**
```
Developer A (Feature 1): "Use Builder pattern for config"
Developer B (Feature 2): "Avoid Builder pattern; too complex"

Merge Result:
wiki/vault/decision.md:
  1. Use Builder pattern for config (Feature 1, 2026-05-20) — SUPERCEDED
  2. Avoid Builder pattern; too complex (Feature 2, 2026-05-21, rationale: ...)
     Related: See Decision 1 (prior attempt, lessons learned)
```

---

#### 3.1.3 Type C: Pattern Discovery Overlap (Low-Medium Risk)

**Scenario:** Developer A discovers "Error Handling with Fallback", Developer B also discovers same pattern independently.

**Resolution:** DEDUPLICATE
- Merge into single pattern entry
- Add both feature contributions to "discovered in" field
- Tag as "verified across 2+ features"

**Example:**
```
Pattern: Error Handling with Fallback
Discovered in: Feature A (logging), Feature B (API calls)
Status: VERIFIED (applied in 2+ contexts)
Evidence: [link to code, link to code]
```

---

#### 3.1.4 Type D: Vault File Format Conflict (Rare)

**Scenario:** Developer A adds lessons to vault/lessons/, Developer B reorganizes vault/lessons/ structure.

**Resolution:** GIT MERGE CONFLICT
- Use git conflict markers + manual resolution
- Prefer structure (Developer B's reorganization) over content (Developer A's lesson)
- Reapply Developer A's lesson content to new structure

**Example:**
```
Before:
vault/lessons/
  2026-05-20-feature-a.md

Developer A → 2026-05-20-feature-a.md (new content)
Developer B → reorganize to vault/lessons/domain/2026-05-20-feature-a.md

Merge Result: Apply both changes
  vault/lessons/
    domain/
      2026-05-20-feature-a.md (with Developer A's content, new structure)
```

---

### 3.2 Conflict Detection & Prevention

#### 3.2.1 Pre-Merge Check (Async Pipeline)

**Before merging any feature branch to main:**

```bash
# 1. Detect vault files changed in feature branch
git diff main.. --name-only | grep vault/

# 2. If any vault files changed, run conflict check
spek check-conflicts main..

# 3. Report: no conflicts | merge-safe | manual-review-required
```

#### 3.2.2 Conflict Check Algorithm

```python
def check_conflicts(main_branch, feature_branch):
    """Detect vault conflicts before merge."""
    
    main_decisions = parse_decisions(f"{main_branch}/vault/decision.md")
    feature_decisions = parse_decisions(f"{feature_branch}/vault/decision.md")
    
    new_decisions = [d for d in feature_decisions if d not in main_decisions]
    
    for new_d in new_decisions:
        for existing_d in main_decisions:
            if contradicts(new_d, existing_d):
                report(f"CONFLICT: {new_d} contradicts {existing_d}")
                return "manual-review-required"
            if duplicates(new_d, existing_d):
                report(f"DUPLICATE: {new_d} (already exists as {existing_d})")
                return "merge-safe (deduplicate)"
    
    return "merge-safe"
```

#### 3.2.3 Communication: Coordination Checkins

**File:** `wiki/vault/coordination/checkins.md` (shared, human-readable log)

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
- New patterns: Mock strategy for SpecKit + CodeGraph
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

---

## 4. Git Strategy: Feature Branches & Merge

### 4.1 Branch Naming Convention

```
spek-<feature-name>-<developer-initials>

Examples:
- spek-add-logging-da (Developer A's logging feature)
- spek-add-tests-db (Developer B's tests feature)
- spek-codegraph-integration-mc (Developer MC's CodeGraph work)
```

**Branch Naming Rules:**
- Always include developer initials (enables `spek check-conflicts` to attribute conflicts)
- Feature name: kebab-case, descriptive, < 30 chars
- Example INVALID: `feature/logging` (missing initials), `add_logging` (wrong separator)

### 4.2 Branch Isolation

**Goal:** Minimize merge conflicts by isolating feature work.

**Best Practices:**

✅ **DO:**
- Work on feature branch; pull main occasionally (keep up-to-date)
- Commit frequently to feature branch (small, atomic commits)
- Use descriptive commit messages ("Add logging to main.py; document decision")
- Treat feature branch as safe sandbox

❌ **DON'T:**
- Push vault changes during feature work (merge at end only)
- Commit directly to main (all changes via PR/feature branch)
- Merge other features into your branch (rebase on latest main instead)
- Force-push to main (breaks team workflow)

### 4.3 Merge Workflow

#### 4.3.1 Merge to Main (Decision Point)

**Before merge, answer these questions:**

1. **Code Ready?** All tasks complete + implementation passes unit tests?
   - YES: proceed to step 2
   - NO: continue feature work; merge later

2. **Vault Conflicts?** Run `spek check-conflicts main..`
   - **No conflicts:** Proceed to step 3 (fast track)
   - **Merge-safe duplicates:** Deduplicate + proceed to step 3
   - **Manual review required:** Proceed to step 3b (conflict resolution)

3. **Fast Track (No Conflicts):**
   ```bash
   git checkout main
   git pull origin main
   git merge --squash spek-<feature>-<initials>
   git commit -m "Feature: <Feature Name> (by <Developer>)"
   git push origin main
   ```

3b. **Conflict Resolution Track:**
   ```bash
   # 1. Reviewer analyzes conflicts
   spek analyze-conflicts main spek-<feature>-<initials>
   # Output: detailed conflict report
   
   # 2. Resolve manually (or run auto-merge if low-risk)
   spek resolve-conflicts --strategy [accept-new|accept-existing|merge-manual] \
                          main spek-<feature>-<initials>
   
   # 3. Developer reviews conflict resolution
   # 4. Merge
   git merge spek-<feature>-<initials> -m "Feature: <Name> (conflicts resolved: ...)"
   ```

#### 4.3.2 Archive Feature Branch

**After merge:**

```bash
# Delete feature branch (cleanup)
git branch -d spek-<feature>-<initials>
git push origin --delete spek-<feature>-<initials>

# Vault: Move vault/session/ → vault/sessions/<date>-<feature>.md
# (Happens during /spek.post; confirmed during merge review)
```

---

## 5. Feature Plan/Spec Ownership

### 5.1 Isolation: Each Feature Owns Its Artifacts

**Principle:** Specs and plans are feature-scoped, not shared.

**Directory Structure:**

```
vault/
├─ specs/
│  ├─ feature-a-spec.md (Developer A)
│  ├─ feature-b-spec.md (Developer B)
│  └─ shared-reference-spec.md (architecture-only, read-only)
├─ plans/
│  ├─ feature-a-plan.md (Developer A)
│  ├─ feature-b-plan.md (Developer B)
│  └─ shared-reference-plan.md (architecture-only, read-only)
└─ decisions.md (shared, grows per feature)
```

**Why Isolation?**
- Specs are feature-specific; decisions + patterns are team-level
- Prevents merge conflicts on core artifacts
- Each feature's work is self-contained + reviewable
- Decisions/patterns are "stable"; specs are "working"

### 5.2 No Cross-Feature Plan Sharing

**Principle:** If features overlap, don't merge plans. Document dependency instead.

**Example: Overlapping Features**

```
Feature A: "Add logging"
├─ Spec: vault/specs/feature-a-spec.md
├─ Plan: vault/specs/feature-a-plan.md
└─ Affected files: main.py, utils.py

Feature B: "Add tests"
├─ Spec: vault/specs/feature-b-spec.md
├─ Plan: vault/specs/feature-b-plan.md
└─ Affected files: tests/, test_main.py

If Developer A finishes first:
- A merges to main (code + lessons)
- B continues on separate branch (may merge A's code first)
- At B's merge, A's code is already in main
- No plan merge; just document "depends on Feature A code"
```

**Dependency Notation in Specs:**

```markdown
## Feature B Specification

### Dependencies
- Feature A: "Add logging" (merged 2026-05-21)
  - Code dependency: Uses logging from main.py
  - Decision dependency: Respects "Logging Decision" from Feature A
  - Wikilink: [[feature-a-lessons]]
```

---

## 6. Decision Coordination: Async Checkins

### 6.1 Feature Checkins Ritual

**Timing:** Feature start + feature end (2 checkins per feature)

**Location:** `wiki/vault/coordination/checkins.md`

**Format:**

```markdown
## [DATE]

### Feature Start: "[Feature Name]" (Developer [Initials], branch: spek-...)
- Scope: [1-3 sentence summary]
- Estimated duration: [X-Y hours]
- Affected code areas: [main.py, utils.py, ...]
- Affected patterns: [List relevant patterns from vault/patterns.md]
- Link: [GitHub link to feature branch]
- Status: IN PROGRESS

### Feature Complete: "[Feature Name]" (Developer [Initials])
- Duration: [actual time]
- New decisions: [bullet list]
- New patterns: [bullet list]
- Code review: Pending / In Progress / Approved
- Lessons: vault/lessons/[date]-[feature]-[initials].md
- Status: AWAITING MERGE REVIEW / MERGED
```

**Optional: Mid-Feature Notifications**

If decision changes or conflict emerges mid-feature:
```markdown
### Decision Change (Developer [Initials], spek-[feature]-[initials])
- Old decision: [from decision.md]
- New decision: [updated rationale]
- Reason: [why changed]
- Impact: [which other features affected]
- Status: REVIEW NEEDED (before merge)
```

---

## 7. Scaling: 2→5+ Developers

### 7.1 Scaling Patterns

#### 7.1.1 Pair Features (2 Devs, Same Feature)

**Scenario:** Feature too large for one developer.

**Strategy:** One primary (owns spec + plan) + one contributor.

```
Feature "Add Comprehensive Logging"
├─ Primary: Developer A (spec, plan, overall)
├─ Contributor: Developer B (specific tasks, code review)
├─ Branch: spek-add-logging-da-db (combined initials)
├─ Decisions: All decisions attributed to primary (Developer A)
└─ Lessons: Capture both contributors' insights
```

**Process:**
1. Both work on same feature branch
2. Regular syncs (daily or EOD)
3. Code review within pair
4. One PR to main (attributed to primary)

#### 7.1.2 Dependent Features (Feature → Feature)

**Scenario:** Feature B depends on Feature A code.

**Strategy:** Chain features via main branch.

```
Timeline:
2026-05-20: Feature A merges to main
2026-05-21: Developer B pulls main (gets Feature A code), continues Feature B
2026-05-22: Feature B merges to main (includes Feature A + B)

Dependency Doc:
Feature B spec: "Depends on Feature A: Add Logging (merged 2026-05-20)"
```

#### 7.1.3 Conflict Escalation (3+ Conflicts)

**Scenario:** Multiple decisions contradict or 3+ devs contributing simultaneously.

**Strategy:** Sync meeting + decision record.

```
wiki/vault/coordination/team-sync-2026-05-22.md:
---
title: Team Sync - Conflict Resolution
date: 2026-05-22
attendees: [Developer A, B, C]
---

## Conflicts Discussed
1. Logging approach (A vs B) → Decision: Use approach A, annotate B's reasoning
2. Test coverage target (75% vs 80%) → Decision: 80%, defer lower later
3. Pattern conflict (Builder vs Factory) → Decision: Use Builder for config only

## Outcomes
- Decisions updated: 3 records
- Patterns updated: 1 record
- Merge order: Feature A → B → C (sequential to avoid churn)
```

---

## 8. Solo Developer (Current): Quick Reference

### 8.1 Workflow: 4 Steps

```
1. /spek.prepare
   → Git: spek-<feature>
   → Vault: load context
   → Memory: create session

2. /spek.plan → /spek.implement
   → Work on branch
   → Update memory

3. /spek.post
   → Lessons generated
   → Decisions drafted
   → Git commit

4. Git: merge to main
   → Code review (self)
   → Merge feature branch
```

### 8.2 Success Criteria (Solo)

✅ Feature branch naming: `spek-<feature>-<initials>`  
✅ No vault conflicts (solo, sequential)  
✅ Vault grows per feature (decisions + patterns + lessons)  
✅ Sessions archived post-feature  
✅ Main branch always stable

---

## 9. Team Coordination (Future): Quick Reference

### 9.1 Conflict Resolution Flow

```
Feature branch created
    ↓
Work isolated on branch
    ↓
/spek.post: generate lessons + draft decisions
    ↓
Git: PR to main
    ↓
Check: spek check-conflicts main..
    ↓
    ├─ No conflicts → Fast track merge
    ├─ Duplicates → Deduplicate + merge
    └─ Contradictions → Manual review + annotate
    ↓
Merged to main + vault updated
    ↓
vault/session/ → vault/sessions/
```

### 9.2 Team Success Criteria

✅ No vault conflicts (checked pre-merge)  
✅ All decisions annotated (new + superceded)  
✅ Patterns deduplicated + verified  
✅ Checkins logged (async coordination)  
✅ Branches deleted post-merge (cleanup)  
✅ Main always stable

---

## 10. Troubleshooting

### 10.1 "Two Devs Changed Same Decision"

**Symptom:** vault/decision.md merge conflict (text lines overlap).

**Solution:**
1. Analyze: Are they contradicting (Type B) or just rewording same idea?
2. If contradicting:
   - Accept both, add annotation
   - Mark older as "superceded"
3. If same idea:
   - Accept newer wording
   - Merge (no annotation needed)
4. Commit: Document decision in checkins.md

### 10.2 "Feature Branch Behind Main (Merge Churn)"

**Symptom:** Feature branch is 10+ commits behind main; risky merge.

**Solution:**
1. Minimize churn: Don't pull main into feature branch
2. Instead: Rebase feature on latest main (clean history)
   ```bash
   git fetch origin main
   git rebase origin/main
   ```
3. If conflicts: Resolve manually + continue rebase
4. Force-push to feature branch (safe; it's your branch)
   ```bash
   git push -f origin spek-<feature>-<initials>
   ```

### 10.3 "Vault Conflict Not Detected by spek check-conflicts"

**Symptom:** Merge tool missed a conflict; discovered post-merge.

**Solution:**
1. Revert merge: `git revert -m 1 <merge-commit>`
2. Re-analyze with more verbose logging:
   ```bash
   spek analyze-conflicts main spek-<feature>-<initials> --verbose
   ```
3. Investigate: Decision wording too different? Pattern deduplication missed?
4. Update conflict detection algorithm (improve patterns)

---

## 11. Integration with Spekificity Commands

### 11.1 Updated `/spek.prepare` (Team Mode)

```
Step 1: Git state verification + feature branch creation
  If solo:
    → spek-<feature>-<initials> (initials = user)
  If team:
    → spek-<feature>-<initials> (initials = dev's initials)
    → Also: spek check-conflicts origin/main..HEAD (ensure no surprises)

Step 2-7: [same as before]

Step 8: Notify (NEW)
  If team:
    → Post to vault/coordination/checkins.md "Feature Start: ..."
```

### 11.2 Updated `/spek.post` (Team Mode)

```
Step 1-3: [same as before]

Step 4: Vault Update Strategy (CHANGED)
  If solo:
    → Append to vault/decision.md + vault/patterns.md (as before)
  If team:
    → Create vault-update-draft.md (local, not merged yet)
    → Let merge process handle conflicts + annotations

Step 9: Archive + Notify (NEW)
  → vault/session/ → vault/sessions/
  → Post to vault/coordination/checkins.md "Feature Complete: ..."
  → Create git PR (if team mode) or direct merge (if solo)
```

### 11.3 New Command: `/spek check-conflicts`

```bash
spek check-conflicts [main_branch] [feature_branch]

Output:
- merge-safe: No conflicts detected
- merge-safe-deduplicate: Duplicates found; auto-deduplicate recommended
- manual-review-required: Contradictions detected; list with context
- conflict-details: Detailed analysis (--verbose)

Exit codes:
- 0: Safe to merge
- 1: Manual review needed
- 2: Conflicts detected; merge blocked
```

---

## 12. References

- **Feature State Tracking:** [specs/feature-state-tracking.md](../specs/040-feature-state-tracking.md)
- **Memory Architecture:** [specs/memory-architecture.md](../specs/030-memory-architecture.md)
- **Git Verification:** [specs/git-verification.md](../specs/012-git-verification.md)
- **Spek Conclude Command:** [specs/conclude-command.md](../specs/102-conclude-command.md)
- **Prepare Command:** [specs/prepare-command.md](../specs/100-prepare-command.md)

---

## 13. Success Criteria

✅ **Solo Developer (Current):**
- Feature isolation via git branches
- No vault conflicts (sequential work)
- Sessions archived post-feature
- Main always stable

✅ **Team Developer (Future):**
- Conflict detection via `spek check-conflicts`
- Manual review before vault merge
- Decisions annotated (new + superceded)
- Patterns deduplicated + verified
- Async coordination via checkins.md
- Branches cleaned up post-merge

✅ **Scaling (2→5+ Developers):**
- Pair features supported (combined initials)
- Dependent features chained via main
- Conflict escalation to sync meetings
- Decision records archived
- Patterns become team knowledge base
