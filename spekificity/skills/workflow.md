---
name: spek-workflow
description: 'Complete workflow guide for SpecKit feature development pipeline.'
---

# /spek.workflow

Complete workflow guide: when to call each skill, correct sequencing, error recovery, approval signoffs.

## Correct Calling Sequence

```
┌─────────────────────────────────────────────────────────────────┐
│ FEATURE DEVELOPMENT WORKFLOW                                    │
└─────────────────────────────────────────────────────────────────┘

1. PREPARE PHASE
   └─► /spek.prepare
       - Initialize lat.md indexes (code + docs)
       - Load vault decisions, patterns, lessons
       - Validate constitution exists
       - Check token budget
       ✓ Ready: lat.md current, vault context loaded

2. SPECIFICATION PHASE
   └─► /spek.plan
       - Runs /speckit-specify (writes spec.md)
       - Runs /speckit-plan (writes plan.md)
       - Runs /speckit-tasks (writes tasks.md)
       - Optional: validate lat.md sections
       - Anti-sycophancy check
       ✓ Ready: spec/plan/tasks drafted
       
   └─► User reviews & approves
       - Mark spec.md frontmatter: approved_by, approved_date
       - Mark plan.md frontmatter: approved_by, approved_date
       - Mark tasks.md frontmatter: approved_by, approved_date
       ✓ Ready: artifacts approved for implementation

3. MAPPING PHASE (Optional - call if complex dependencies)
   └─► /spek.map [topic]
       - Query code dependencies for affected areas
       - Identify blockers and critical paths
       - Output for reference during implement
       ✓ Ready: dependency map built (for reference)

4. IMPLEMENTATION PHASE
   └─► /spek.implement [--steps N]
       - Validates approval tokens in spec/plan/tasks
       - Executes tasks in dependency order
       - Per-task: code → tests → validate → commit
       - Updates plan with task completion status
       - Test output saved to .spek/memory/last-test-output.log
       ✓ Ready: all tasks complete, tests passing

5. ANALYSIS & ARCHIVAL PHASE
   └─► /spek.conclude
       - Run /speckit-analyze (spec drift check)
       - Run /spek.lessons (extract patterns, decisions)
       - Run Backprop Reflex (learn from test failures)
       - Generate lat.md drift report (symbols added/removed)
       - Archive spec/plan/tasks to vault
       - Refresh lat.md indexes
       - Commit vault + memory changes (specs, decisions, patterns, drift report)
       ✓ Ready: feature documented, lessons extracted, codebase indexed

6. QUALITY REVIEW (Optional - call if code quality concerns)
   └─► /spek.blind-review (SEPARATE from step 5)
       - Pre-check: linter + tests + test output file
       - Anonymize code, run linter
       - Report critical/warning/info findings
       - Do NOT combine with /spek.rarv in same conclude call
       ✓ Ready: quality findings addressed

7. DRIFT RESOLUTION (Optional - call if architectural changes)
   └─► /spek.rarv (SEPARATE from step 5)
       - Pre-check: spec file, lat.md current, vault clean
       - Load original spec, compare vs implementation
       - Identify deviations (additions/omissions/changes)
       - User resolves: fix code (A), justify (B), or defer (C)
       - Do NOT combine with /spek.blind-review in same conclude call
       ✓ Ready: spec/impl gaps resolved

8. POST-CONCLUSION
   └─► If not yet done: tag feature branch with release label
   └─► Open PR or merge-request to main
   └─► Run CI/CD pipeline verification
   └─► Merge and delete feature branch
   └─► Archive PR link in feature's .spek/vault/lessons/ file
```

---

## Tool Roles & Leverage

### Obsidian Vault (`~/.spek/vault/`)

**Purpose**: Central knowledge base for architectural decisions, reusable patterns, and learned lessons

**Read Access** (via skills):
- spek-plan queries `decisions.md` + `patterns.md` to inform spec/plan generation
- spek-rarv loads decisions to detect contradictions before user choices
- spek-lessons reads existing patterns to avoid duplication
- Autolink enrichment queries vault for keyword matches when writing new lessons

**Write Access** (manual or programmatic):
- User manually edits `decisions.md` when new architectural decisions emerge (during or after implement)
- User manually edits `patterns.md` when reusable patterns discovered (after lessons extracted)
- spek-lessons auto-writes to `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature.md`
- spek-conclude auto-writes updates to `decisions.md` and `patterns.md` (if new patterns found)
- spek-rarv may update vault files if Option B chosen (justify deviation)

**Sync Strategy**:
- Vault changes committed to git by spek-conclude (step 7: `git add .spek/vault/ && git commit`)
- NOT pushed to Obsidian live sync (if using Obsidian Desktop, pull after feature concludes)
- Obsidian Desktop app reads vault locally for browsing/editing
- Each developer runs `git pull` before starting new feature to load latest decisions/patterns

**Workflow**:
1. **Before spek-plan**: Run `git pull` to ensure latest decisions/patterns loaded
2. **During spek-plan**: Skills query vault automatically (no manual Obsidian interaction needed)
3. **After spek-implement**: Optionally open Obsidian and update `decisions.md` manually if new decisions emerged
4. **After spek-conclude**: Skills auto-commit vault updates; run `git push` to publish
5. **Next feature**: Next developer runs `git pull` to sync decisions/patterns

### lat.md Code Index (`~/.spek/lat.md/`)

**Purpose**: Live map of codebase symbols, definitions, call graphs, and dependencies

**Structure**:
- `.spek/lat.md/code/` — code symbols, definitions, callers, call trees
- `.spek/lat.md/docs/` — documentation index (wiki, vault, markdown)

**Build** (via spek-prepare):
```bash
lat init          # generates .spek/lat.md/code/ (symbols, call graphs)
lat init --docs   # generates .spek/lat.md/docs/ (doc index)
```

**Query** (via skills):
- spek-plan queries lat.md to ground spec/plan in actual codebase architecture
- spek-map queries lat.md to identify blockers and critical paths
- spek-implement queries lat.md to validate task symbols exist (fail if symbols not in index)
- spek-rarv queries lat.md to compare spec requirements vs actual implementation

**Refresh Strategy**:
- spek-plan step 0.5 checks freshness (mtime vs git HEAD); auto-refreshes if stale
- spek-implement drift detection queries lat.md to find symbols added/removed
- spek-conclude step 6.5 runs `lat init` after all commits (reflects newly committed code)

**Drift Detection**:
- If implementation adds symbols not in lat.md (new code not yet indexed): document in `.spek/memory/lat-drift.md`
- If implementation removes symbols from lat.md (refactored/deleted code): document in `.spek/memory/lat-drift.md`
- spek-conclude generates drift report for next team review

### Integration Points

| Skill | Reads Vault? | Reads lat.md? | Writes Vault? | Writes lat.md? |
|-------|-------------|--------------|---------------|---------------|
| spek-prepare | No | — (builds) | No | ✓ Build ||
| spek-plan | ✓ decisions, patterns | ✓ Query | No | — |
| spek-map | ✓ specs | ✓ Query | No | — |
| spek-implement | No | ✓ Validate + drift | No | No (read-only) |
| spek-conclude | No | ✓ Compare | ✓ Update patterns/decisions | ✓ Refresh |
| spek-rarv | ✓ decisions, patterns (validate contradictions) | ✓ Compare spec vs impl | ✓ Update (Option B) | — |
| spek-lessons | ✓ keywords for autolink | No | ✓ Write to lessons/ | — |

---

## Valid Subsequences

### Fast Path (Simple Feature)
```
prepare → plan → implement → conclude
```

### With Dependency Analysis
```
prepare → plan → map → implement → conclude
```

### With Quality Gate
```
prepare → plan → implement → conclude → blind-review
(address findings, run tests, commit fixes, then proceed to release)
```

### With Architectural Review
```
prepare → plan → implement → conclude → rarv
(resolve spec drift, return to implement if Option A chosen, then release)
```

### Full Rigor (Complex Feature)
```
prepare → context → plan → map → implement → conclude → blind-review OR rarv
(choose one optional step, not both in same flow)
```

## Invalid Sequences (Will Fail)

❌ `implement` without `prepare` (lat.md missing)
❌ `plan` without `prepare` (vault context missing)
❌ `conclude` without `implement` (no tasks completed)
❌ `blind-review` + `rarv` same conclude call (output conflict)
❌ `map` without `prepare` (lat.md missing)
❌ `rarv` without `conclude` (spec not finalized for comparison)

---

## Approval Mechanism

Each artifact (spec.md, plan.md, tasks.md) includes frontmatter:

```yaml
---
feature: [feature-name]
status: draft | approved | implemented | concluded
approved_by: [agent/user name]
approved_date: YYYY-MM-DD
lat_md_version: [timestamp of lat.md used]
---
```

**spek-implement Pre-check**: Verify `status: approved` in all three files. Fail if any remain `draft`.

**spek-plan Post-step**: After user review, update frontmatter to `status: approved` and populate `approved_by`, `approved_date`.

---

## lat.md Freshness Management

**Problem**: User runs `prepare` (lat.md generated). Then edits code. Then runs `plan`. Plan analyzes stale lat.md.

**Solution**: spek-plan step 0 checks lat.md mtime vs git HEAD timestamp. If lat.md older than most recent commit, prints:
```
[WARN] lat.md is stale (last commit: 2 hours ago, lat.md: 4 hours ago)
[WARN] Run 'lat init' to refresh before proceeding? (Y/n)
```

If user chooses Y, auto-run `lat init` and continue.
If user chooses N, continue with stale data (user accepts risk).

---

## Test Output Convention

All skills that run tests (spek-implement, spek-blind-review) must capture output to:
```
.spek/memory/last-test-output.log
```

Format:
```
=== Test Run: YYYY-MM-DD HH:MM:SS ===
Command: [command that ran]
Exit Code: [0 or non-zero]
Stdout: [full output]
```

spek-conclude step 3 (Backprop Reflex) reads this file. If missing or empty, skips gracefully.

---

## Task ID Format

spek-plan output (tasks.md) specifies tasks with format:

```
## Task 1: [description]
- Success Criteria: [...]

## Task 2: [description]
- Success Criteria: [...]
```

Numeric ID only (1, 2, 3...). spek-implement `--steps N` expects integer within this range.

---

## Git Commit Strategy

| Skill | Commits? | What | When |
|-------|----------|------|------|
| **spek-prepare** | No | — | — |
| **spek-plan** | No | — | — |
| **spek-map** | No | — | — |
| **spek-implement** | Yes | `[Task X] description` | Per task, after tests pass |
| **spek-conclude** | Yes | `.spek/vault/ + .spek/memory/` | Once at end (step 7) |
| **spek-blind-review** | No | — | — |
| **spek-rarv** | No | — | (but updates vault files that must be committed separately) |
| **spek-lessons** | No | — | (but writes to vault—spek-conclude commits it) |

**Implication**: After spek-implement completes, feature branch has multiple commits (one per task). After spek-conclude, vault archive is single commit. After spek-blind-review (if run), fix commits are additional. Git history is chronological, not squashed.

---

## Error Recovery

### If spek-plan lat.md validation fails (step 4)
1. Halt and report validation error with file:line
2. User manually reviews lat.md or runs `lat init --docs` to refresh doc index
3. Re-run spek-plan from start

### If spek-implement test fails (mid-task)
1. Fix code locally, run test again
2. Resume with `/spek.implement --steps [N]` where N = current task
3. Do NOT re-run from task 1

### If spek-conclude /speckit-analyze fails
1. Address spec drift errors manually
2. Re-run /spek.lessons standalone if needed
3. Manually commit vault updates
4. Resume post-conclude workflow

### If spek-blind-review finds CRITICAL issues
1. Do NOT merge or release
2. Fix issues locally
3. Re-run tests + blind-review
4. Once all CRITICAL resolved, proceed to release

### If spek-rarv detects contradictions in vault
1. Run `/speckit-constitution` interactively to resolve
2. Re-run spek-rarv from step 1

---

## Post-Conclusion Workflow

After `/spek.conclude` (and optional blind-review/rarv), feature is documented and lessons extracted. Next steps:

1. **Tag Feature Branch** (optional but recommended):
   ```
   git tag -a vX.Y.Z-feature-[name] -m "Feature: [name]"
   ```

2. **Open Pull Request**:
   - Title: `[Feature] name — description`
   - Link to `.spek/vault/lessons/` file in PR description
   - Reference task IDs that were completed
   - Attach blind-review findings (if run) to PR comments

3. **Code Review** (by team):
   - Review commits, test coverage
   - Reference blind-review report for code quality context
   - Approve or request changes

4. **CI/CD Verification**:
   - Ensure all checks pass on feature branch
   - Run integration tests
   - Performance benchmarks (if applicable)

5. **Merge to Main**:
   - Merge with commit message referencing feature ID or spec file
   - Example: `Merge feature/005 (Authentication Redesign) — spec: .spek/vault/specs/005-spec.md`

6. **Archive PR Link**:
   - Update feature's lessons file with PR link:
     ```
     ### Linked Artifacts
     - PR: https://github.com/org/repo/pull/123
     ```
   - Commit this update to vault

7. **Delete Feature Branch**:
   ```
   git branch -d feature/005
   ```

8. **Release (if applicable)**:
   - Bump version in pyproject.toml or package.json
   - Update CHANGELOG with feature summary
   - Tag main: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
   - Push tags
   - Publish to PyPI, npm, or equivalent

---

## Context Reloading

If switching between multiple concurrent features (not recommended):

- **Before spek-plan**: Run `/spek.context` to reload vault state (decisions, patterns, lessons may have changed in other feature)
- **Before spek-implement**: Run `/spek.context` if long time elapsed or other features concluded in parallel

Normally not needed within a single feature's workflow.

---

## Vault Update Patterns

### When to Manually Update decisions.md

Update `decisions.md` in `.spek/vault/` when:
- During spek-implement: A design choice emerges that's not in the spec (e.g., "use async/await vs callbacks")
- After spek-implement: A bloccker was discovered that changed architecture mid-feature
- During spek-rarv: Option B chosen (justify spec deviation by updating decision rationale)

Do NOT wait until spek-conclude to update decisions. Update immediately when decision is made (commit to branch, will be pulled into vault by spek-conclude).

### When to Manually Update patterns.md

Update `patterns.md` when:
- During spek-implement: A reusable pattern emerges (e.g., "error handling via Result type")
- Optionally: After spek-lessons (automate via backprop_reflex, which detects failure patterns)

spek-conclude auto-appends new patterns from lessons; do NOT duplicate.

### When to Update lessons/ files

- spek-lessons writes new lessons automatically → you add PR links + feedback (optional)
- Do NOT edit during feature (write only after conclude)
- Use wikilinks to link to decisions and patterns (autolink enrichment handles this)

---

## Obsidian.md Setup & Gitignore

### Initial Setup

1. **Clone project with `.spek/vault/` folder**
2. **In Obsidian Desktop**:
   - Click "Open folder as vault" → select `.spek/vault/`
   - Obsidian creates `.obsidian/` folder (settings, plugin data, cache)
3. **In project root `.gitignore`**, add:
   ```
   .obsidian/
   .spek/lat.md/.cache
   ```
   (Do NOT commit Obsidian metadata or lat.md cache files)

### Workflow in Obsidian

- **Browse vault**: Use graph view, wikilink navigation to explore decisions/patterns/lessons
- **Edit decisions/patterns**: Manually update during feature if needed (Obsidian syncs to disk; changes auto-detected by git)
- **Create backlinks**: Type `[[decision-title]]` in lesson files; autolink enrichment verifies links exist
- **View graph**: Use Obsidian's graph view to visualize decision dependencies before starting spek-plan
- **Do NOT commit**: `.obsidian/` folder is gitignored (each dev has their own Obsidian config)

---

## lat.md Drift Scenarios & Recovery

### Scenario 1: New Symbols Added (Feature Adds Code)

```
lat.md before implement: auth/authenticate_user() exists
implement adds: auth/refresh_token() (new function)
lat-drift.md: "Task 3 added auth/refresh_token (new)"
spek-conclude: 
  - Runs 'lat init' to refresh index
  - New symbol now in updated lat.md
  - Drift report shows addition (expected)
```

**Recovery**: None needed. New symbols are part of feature deliverable.

### Scenario 2: Stale lat.md Queried (Code Changed Before Plan)

```
Situation:
  - spek-prepare runs (lat.md current)
  - User edits code (new module added)
  - spek-plan runs (queries old lat.md)
  
spek-plan step 0.5 freshness check:
  - Detects lat.md mtime < git HEAD mtime
  - Offers: "lat.md stale. Refresh? (Y/n)"
  - User chooses Y → auto-runs 'lat init'
  - Continues with fresh lat.md
```

**Recovery**: Automatic via freshness check.

### Scenario 3: Symbol Removal (Refactoring Deletes Code)

```
lat.md: auth/deprecated_login() exists
implement: Delete deprecated_login()
lat-drift.md: "Task 2 removed auth/deprecated_login"
spek-conclude:
  - Runs 'lat init' to refresh
  - Symbol removed from updated lat.md
  - Drift report shows removal (expected)
  - Link removal to Success Criteria (was removal intentional?)
```

**Recovery**: If removal unintentional, spek-implement `--steps N` allows rerunning task to restore.

### Scenario 4: lat.md Query Finds No Symbols (Misnamed Module)

```
Task: "Implement payment module"
Query: lat.md for "payment" symbols
Result: None found (module doesn't exist yet OR misnamed as "checkout")

spek-implement step 4 halt:
  - "Symbol validation: payment module not found in lat.md"
  - Check: is module correctly named?
  - Check: is task description aligned with codebase structure?
  - Fix: update task description or code, re-run task
```

**Recovery**: Halt and clarify. Update task or code, then resume `--steps N`.



