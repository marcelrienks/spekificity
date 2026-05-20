# Feature Development Workflow

**See also:** [intention.md](intention.md) (principles) → [architecture.md](architecture.md) (technical) → [quickstart.md](quickstart.md) (howto)

---

## Overview

Spekificity feature development follows a deterministic workflow with four required stages:

1. **Prepare** – Pre-flight checks and workspace setup
2. **Specify & Plan** – Write feature spec, generate implementation plan
3. **Implement** – Execute tasks with full context
4. **Post** – Archive outcomes, sync vault, update graph

Optional enhancements (context loading, dependency analysis, retrospectives) can be applied at any stage. Each stage produces durable artifacts stored in the vault.

---

## Stage 1: Preparation & Workspace Setup

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
| CodeGraph Sync | Refresh CodeGraph from latest code (incremental update) | Code index reflects current state | Fresh `codegraph.db` |
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

## Stage 2: Specification & Planning

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
| **Resource Estimate** | Effort scope, complexity level | "Medium complexity, involves database schema changes" |
| **Metrics** | How to measure quality | "Code coverage comprehensive", "API endpoints working" |

### Output Artifacts
- Specification document (Markdown, vault-stored)
- Enrichment layer details embedded in spec
- Links to CodeGraph impact analysis
- Links to relevant architectural decisions

### Exit Criteria
- ✅ Specification written and clear
- ✅ Success Criteria defined
- ✅ Assumptions documented
- ✅ Risk Assessment complete
- ✅ Spec committed to vault

---

## Stage 3: Planning & Task Breakdown

### Commands
```
/spek.automate --phase=plan
# or directly (two-step):
/speckit.plan --spec="feature-spec-id"
/speckit.tasks --plan="feature-plan-id"
```

### Purpose
Convert specification into detailed execution plan (architecture + tech choices) and task list (dependency-ordered executable tasks).

### Workflow

```
SPEC DOCUMENT
    ↓
/speckit.plan (Step 1: Architecture)
    ├─ Analyze spec requirements
    ├─ Design architecture + tech choices
    ├─ Query CodeGraph for affected areas
    └─ Produce: plan.md (rationale, architecture decisions)
    ↓
/speckit.tasks (Step 2: Task Breakdown)
    ├─ Read plan.md
    ├─ Identify task boundaries
    ├─ Determine dependencies (task A blocks B)
    ├─ Estimate per-task resources
    ├─ Query CodeGraph for file locations
    └─ Produce: tasks.md (ordered, IDs, dependencies, risk mitigation)
    ↓
PLAN + TASKS DOCUMENTS (vault + git commit)
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
- `plan.md` — Architecture, tech choices, rationale, research (Markdown, vault-stored)
- `tasks.md` — Dependency-ordered executable tasks with IDs, resource estimates, critical path (Markdown, vault-stored)
- CodeGraph references for implementation
- Record architectural decisions and rationale

### Exit Criteria
- ✅ Architecture documented in plan.md
- ✅ Tech choices justified in plan.md
- ✅ All tasks identified and documented in tasks.md
- ✅ Dependencies clearly mapped in tasks.md
- ✅ Resource estimates provided per task
- ✅ Execution order (critical path) defined
- ✅ Both plan.md and tasks.md committed to vault

---

## Stage 4: Implementation by Task

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

### Pre-Shipping Integration Checklist

Before moving to the final stage, verify all quality gates:

**Code Quality**
- [ ] All functions have docstrings (purpose, args, return)
- [ ] All classes have docstrings (purpose, key methods)
- [ ] Complex logic has inline comments explaining *why*
- [ ] No console.log or debug statements in production code
- [ ] No unused imports or variables
- [ ] Code follows project style guide (linting passes)

**Testing**
- [ ] Unit tests pass locally (< 5 minutes)
- [ ] Integration tests pass locally (< 10 minutes)
- [ ] Edge cases covered (null, empty, invalid input)
- [ ] Error paths tested (exceptions, boundary conditions)
- [ ] Test coverage > 80% for new code
- [ ] Existing tests still pass (no breaking changes)
- [ ] Full test suite runs locally < 5 minutes

**CodeGraph Integration**
- [ ] CodeGraph reflects all new code (symbols, functions, classes)
- [ ] Impact analysis shows affected downstream components
- [ ] CodeGraph queries used during implementation (not file grep)

**Vault Integration**
- [ ] Spec stored in vault with correct metadata
- [ ] Plan stored in vault with task linkage
- [ ] All artifacts committed to git (no uncommitted changes)

**Spekificity Workflow**
- [ ] `/spek.prepare` passed pre-flight checks
- [ ] `/spek.automate --phase=specify` produced valid spec
- [ ] `/spek.automate --phase=plan` produced valid plan
- [ ] `/spek.implement` executed all tasks
- [ ] All `/spek.*` commands worked end-to-end

**Performance**
- [ ] Token budget not exceeded (if one was set)
- [ ] CodeGraph queries working correctly
- [ ] API responses working (if applicable)
- [ ] No N+1 queries or unnecessary loops

**Sign-Off**
- [ ] Code reviewed (if applicable)
- [ ] All Integration Checklist items checked
- [ ] Feature ready for archive and closeout

---

## Stage 5: Post-Feature Archival

### Commands
```
/spek.post
# Includes: archive, lessons extraction (automatic), state refresh

# Optional (for deeper analysis):
/spek.lessons --deep
# Explicit, detailed lesson extraction (runs separately from /spek.post)
```

### Purpose
Archive outcomes, extract lessons learned (automatic), refresh state for future features. `/spek.lessons --deep` available for explicit, detailed reflection.

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
    ├─ Extract Lessons Learned (Automatic)
    │  ├─ What worked well?
    │  ├─ What was difficult?
    │  ├─ Patterns discovered?
    │  ├─ Future recommendations?
    │  └─ Link to specs/decisions (why/how)
    │
    ├─ Refresh State
    │  ├─ Rebuild CodeGraph (full index incorporating feature changes)
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

### Lesson Extraction Details

**Automatic (via `/spek.post`):**
- Lightweight, structured format
- Runs as part of standard closeout workflow
- Suitable for most features
- Captured: what worked, what was difficult, patterns, recommendations

**Explicit/Deep (via `/spek.lessons --deep`):**
- Detailed reflection and analysis
- Cross-references specs, plans, code, and decisions
- Optional, for complex features or research projects
- Runs independently after `/spek.post`
- Produces: comprehensive feature retrospective with architectural insights

**When to use:**
- Standard feature: `/spek.post` (automatic lessons)
- Complex refactor or architectural change: `/spek.post` + `/spek.lessons --deep`
- Research/experimental work: `/spek.lessons --deep` for thorough analysis

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
- **Architecture Notes** — Key decisions and rationale
- **Pattern Library:** [patterns/](patterns/)
