# Feature Development Workflow

**See also:** [architecture.md](architecture.md), [intention.md](intention.md), [integration-checklist.md](integration-checklist.md)

---

## Overview

Spekificity feature development follows a deterministic 5-phase workflow:
1. **Prepare** – Pre-flight checks and context loading
2. **Specify** – Write feature spec with enrichment layers
3. **Plan** – Break spec into tasks and validate dependencies
4. **Implement** – Execute tasks with full context
5. **Close** – Archive outcomes, extract lessons, refresh state

Each phase has clear entry/exit criteria and produces durable artifacts stored in the Obsidian vault.

---

## Phase 1: Feature Start & Preparation

### Command
```
/spek.prepare
```

### Purpose
Pre-flight checks before feature development begins. Ensures workspace is ready, vault is current, CodeGraph is fresh, and git state is clean.

### Sub-steps

| Step | Action | Validates | Output |
|------|--------|-----------|--------|
| Git Status | Check for uncommitted changes | No stale work left | Clean working tree |
| Vault Fresh | Pull latest from Obsidian git sync | No vault conflicts | Current specs/decisions |
| CodeGraph Sync | Refresh CodeGraph from latest code | Code index is current | Fresh `codegraph.db` |
| Session State | Initialize context (vault, repo memory, graph) | All context ready | Session context loaded |
| Feature Readiness | Verify no blocking issues | Prerequisites met | Ready to start |

### Output Artifacts
- Clean git working tree
- Loaded session context (vault, repo memory, CodeGraph)
- Ready-to-use project context (specs, decisions, lessons)

### Exit Criteria
- ✅ Git working tree clean (or staged changes approved)
- ✅ Vault synced with origin
- ✅ CodeGraph up-to-date
- ✅ Session context available

---

## Phase 2: Specification & Enrichment

### Commands
```
/spek.automate --phase=specify
# or directly:
/speckit.specify --feature="feature-name"
```

### Purpose
Create a detailed feature specification with enrichment layers (Success Criteria, Assumptions, Risk Assessment, Metrics).

### Workflow

```
FEATURE INTENT (user describes goal)
    ↓
/speckit.specify
    ├─ Generate base spec (what, why, scope)
    ├─ Query CodeGraph for affected areas
    ├─ Link to existing decisions/specs
    │
    └─ Apply Enrichment Layers:
       ├─ Success Criteria (how to measure done)
       ├─ Assumptions (what's true)
       ├─ Risk Assessment (what could go wrong)
       ├─ Dependencies (upstream/downstream)
       └─ Resource Estimate (tokens, time, complexity)
    ↓
SPEC DOCUMENT (vault + git commit)
```

### Enrichment Layers

Each spec includes structured enrichment:

| Layer | Content | Example |
|-------|---------|---------|
| **Success Criteria** | Measurable completion conditions | "API returns 200 for valid requests", "All tests pass locally" |
| **Assumptions** | Preconditions and facts | "User model exists", "Database schema is migrated" |
| **Risk Assessment** | Potential failures and mitigations | "Breaking change if existing clients depend on old field — need migration plan" |
| **Dependencies** | Upstream/downstream linked tasks | "Requires PR #123 merged first" |
| **Resource Estimate** | Time, tokens, complexity | "Est. 3–4 hours, ~10k tokens, Medium complexity" |
| **Metrics** | How to measure quality | "Code coverage > 80%", "Response time < 100ms" |

### Output Artifacts
- Specification document (Markdown, vault-stored)
- Enrichment layer details embedded in spec
- Links to CodeGraph impact analysis
- References to relevant decisions from [decision.md](decision.md)

### Exit Criteria
- ✅ Specification written and clear
- ✅ Success Criteria defined
- ✅ Assumptions documented
- ✅ Risk Assessment complete
- ✅ Spec committed to vault

---

## Phase 3: Planning & Task Breakdown

### Commands
```
/spek.automate --phase=plan
# or directly:
/speckit.plan --spec="feature-spec-id"
```

### Purpose
Convert specification into a detailed execution plan with task breakdown, dependencies, and resource allocation.

### Workflow

```
SPEC DOCUMENT
    ↓
/speckit.plan
    ├─ Analyze spec for task boundaries
    ├─ Identify dependencies (task A blocks B)
    ├─ Estimate per-task resources
    ├─ Query CodeGraph for change locations
    │
    └─ Apply Enrichment Layers:
       ├─ Task Breakdown (1-2 sentence per task)
       ├─ Dependency Graph (which tasks block others)
       ├─ Execution Order (critical path)
       ├─ Resource Breakdown (tokens per task)
       └─ Risk/Mitigation (task-level risks)
    ↓
PLAN DOCUMENT (vault + git commit)
```

### Plan Structure

Example plan excerpt:

```markdown
## Task Breakdown

### Task 1: Auth Service Setup
- Description: Create authentication service with token validation
- Depends On: None (blocker for Tasks 2, 3)
- Est. Complexity: Medium
- Est. Tokens: 2500
- Files Affected: src/auth/service.ts, test/auth.test.ts

### Task 2: User Model Extension
- Description: Add OAuth fields to User model
- Depends On: Task 1 (auth service API must be defined)
- Est. Complexity: Low
- Est. Tokens: 1200
- Files Affected: src/models/user.ts, migration/001-oauth-fields.sql

### Task 3: Integration Tests
- Description: Write E2E tests for OAuth flow
- Depends On: Tasks 1, 2
- Est. Complexity: High
- Est. Tokens: 3200
- Files Affected: test/e2e/auth.test.ts, test/fixtures/oauth-mock.ts

## Dependency Graph

Task 1 (Auth Service)
  ├─→ Task 2 (User Model)
  └─→ Task 3 (Integration Tests) ← Task 2 also required
```

### Output Artifacts
- Plan document (Markdown, vault-stored)
- Task breakdown with dependencies
- Resource estimates per task
- Execution order (critical path)
- CodeGraph references for implementation

### Exit Criteria
- ✅ All tasks identified and documented
- ✅ Dependencies clearly mapped
- ✅ Resource estimates provided
- ✅ Execution order defined
- ✅ Plan committed to vault

---

## Phase 4: Implementation by Task

### Commands
```
/spek.implement --plan="feature-plan-id"
# Runs tasks in dependency order
```

### Purpose
Execute each task from the plan with full context (spec, plan, CodeGraph, enrichment).

### Workflow Per Task

```
FOR EACH TASK IN PLAN (in dependency order):
    ├─ Load Task Context
    │  ├─ Spec (what/why)
    │  ├─ Plan (dependencies, what this task does)
    │  ├─ CodeGraph (files to change, impact analysis)
    │  └─ Previous Task Outcomes (linking info)
    │
    ├─ Implement
    │  ├─ Write code per task spec
    │  ├─ Run local tests
    │  ├─ Validate against Success Criteria
    │  └─ Document changes (comments, docstrings)
    │
    ├─ Enrich Outcome
    │  ├─ Capture what changed (files, classes, functions)
    │  ├─ Validate Success Criteria for this task
    │  ├─ Document lessons learned (what worked, what didn't)
    │  └─ Flag any blockers or dependencies on future tasks
    │
    └─ Persist
       ├─ Commit code to git (with task ID in message)
       ├─ Update plan: mark task complete
       ├─ Add task outcome to plan document
       └─ Continue to next task

END FOR
```

### Implementation Context

Each task execution includes:

| Context | Source | Purpose |
|---------|--------|---------|
| **Feature Spec** | Vault | Why are we doing this? Success Criteria? |
| **Task Definition** | Plan | What exactly does this task do? |
| **CodeGraph** | Live analysis | What files need to change? Who calls what? |
| **Risk Assessment** | Plan + Spec | What could fail? How to mitigate? |
| **Previous Outcomes** | Vault (updated) | What did earlier tasks create? |

### Implementation Checklist (Per Task)

- [ ] Load task context from plan
- [ ] Read Success Criteria for this task
- [ ] Query CodeGraph for affected symbols/files
- [ ] Write code (implementation)
- [ ] Add docstrings to new functions/classes
- [ ] Write tests (or extend existing tests)
- [ ] Run tests locally (must pass)
- [ ] Validate against Success Criteria
- [ ] Commit with message `[Task X] description` (e.g., `[Task 1] Auth service token validation`)
- [ ] Update plan document: mark task complete + document outcome
- [ ] Document any lessons learned or blockers

### Output Artifacts (Per Task)
- Committed code changes (with task ID in commit message)
- Tests passing locally
- Updated plan document with task outcome
- Task-level lessons learned (stored in plan or vault)

### Exit Criteria (All Tasks)
- ✅ All tasks completed (in dependency order)
- ✅ All tests passing locally
- ✅ Success Criteria validated for each task
- ✅ Code committed with task references
- ✅ Plan marked as "Implementation Complete"

---

## Phase 5: Post-Feature Closeout

### Commands
```
/spek.post
# or explicitly:
/spek.lessons
```

### Purpose
Archive outcomes, extract lessons learned, refresh state for future features.

### Workflow

```
IMPLEMENTATION COMPLETE
    ↓
/spek.post
    ├─ Archive Feature Artifacts
    │  ├─ Spec → Archive folder (vault)
    │  ├─ Plan → Archive folder (vault)
    │  ├─ Outcomes → Session memory
    │  └─ Task commits → Summarized
    │
    ├─ Extract Lessons Learned
    │  ├─ What worked well?
    │  ├─ What was difficult?
    │  ├─ Patterns discovered?
    │  ├─ Future recommendations?
    │  └─ Link to specs/decisions (why/how)
    │
    ├─ Refresh State
    │  ├─ Rebuild CodeGraph (fresh index)
    │  ├─ Update repo memory (project facts)
    │  ├─ Clean session context
    │  └─ Prepare for next feature
    │
    └─ Commit
       ├─ Archive specs/plans to vault
       ├─ Commit lessons to vault
       ├─ Update repo memory
       └─ Tag feature as complete (git tag?)
    ↓
FEATURE ARCHIVED, LESSONS CAPTURED, READY FOR NEXT FEATURE
```

### Lessons Learned Structure

Lessons stored in vault with template:

```markdown
## Feature: [Feature Name]
Date: 2026-05-20
Status: Complete

### What Went Well
- [pattern/approach/tool that worked]
- [pattern/approach/tool that worked]

### What Was Difficult
- [challenge/blocker]
- [mitigation used]

### Patterns Discovered
- [reusable pattern]
- [architectural insight]

### Recommendations for Future
- [suggestion for similar features]
- [process improvement]

### Linked Artifacts
- Spec: [link to archived spec]
- Plan: [link to archived plan]
- Decisions Made: [link to decision entries]
- Pull Requests: [GitHub PR links]
```

### Output Artifacts
- Archived spec (vault)
- Archived plan (vault)
- Lessons learned document (vault)
- Updated CodeGraph (fresh)
- Updated repo memory
- Feature complete (tagged in git)

### Exit Criteria
- ✅ Feature artifacts archived in vault
- ✅ Lessons learned extracted and committed
- ✅ CodeGraph refreshed
- ✅ Repo memory updated
- ✅ Session context cleaned

---

## Timeline Diagram

```
DAY 1
├─ Morning: /spek.prepare          [~5 min]
├─ Morning: /spek.automate         [~30 min: spec + plan review]
├─ Afternoon: Review & Approve     [~15 min: stakeholder sign-off]
│
DAY 2
├─ Morning: /spek.implement        [~2–4 hours: Task 1–2]
├─ Afternoon: /spek.implement      [~1–2 hours: Task 3]
├─ Late: Local testing + fixes     [~30 min]
│
DAY 3
├─ Morning: Final validation       [~15 min]
├─ Afternoon: /spek.post           [~15 min: archive + lessons]
│
TOTAL: ~24 hours across 3 days
```

---

## Error Handling & Recovery

### Spec Issues
- **Problem:** Spec is ambiguous or incomplete
- **Recovery:** `/speckit.clarify` (request clarifications)
- **Outcome:** Updated spec document

### Plan Issues
- **Problem:** Task dependencies are incorrect or blocking
- **Recovery:** `/speckit.plan --revise` (replan)
- **Outcome:** Revised plan document

### Implementation Failure
- **Problem:** Task fails Success Criteria
- **Recovery:** `/spek.implement --task=X --retry` (retry single task)
- **Outcome:** Code correction + test validation

### Lessons Not Captured
- **Problem:** `/spek.post` completes but lessons are shallow
- **Recovery:** `/spek.lessons --deep` (explicit, detailed extraction)
- **Outcome:** Richer lessons in vault

---

## Cross-Phase Context Reuse

```
Spec defines WHAT + WHY
    ↓ (used by)
Plan breaks into tasks + HOW
    ↓ (used by)
Implementation executes per task + VALIDATES against spec
    ↓ (used by)
Lessons capture WHAT WORKED + WHAT DIDN'T
    ↓ (reused in)
Next Feature Spec (pattern reference) + Next Feature Plan (estimate refinement)
```

---

## References

- **Architecture:** [architecture.md](architecture.md)
- **Naming & Commands:** [naming-conventions.md](naming-conventions.md)
- **Integration Checklist:** [integration-checklist.md](integration-checklist.md)
- **Decision Log:** [decision.md](decision.md)
- **Pattern Library:** [patterns/](patterns/)
