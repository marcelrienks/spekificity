# Feature Development Workflow

## Overview

Spekificity feature development follows a deterministic, staged workflow:

- **Prepare** – Pre-flight checks and workspace setup
- **Plan** – Write feature spec, generate implementation plan
- **Implement** – Execute tasks with full context
- **Post** – Archive outcomes, sync vault, update graph

Optional enhancements (context loading, dependency analysis, retrospectives) can be applied at any stage. Each stage produces durable artifacts stored in the vault.

---

## Preparation

### Command
```
/spek.prepare
```

### Purpose
Pre-flight checks before feature development begins. Ensures workspace is ready, vault is current, lat.md index is fresh, and git state is clean.

### Sub-steps

| Step | Action | Validates | Output |
|------|--------|-----------|--------|
| Git Status | Check for uncommitted changes | No stale work left | Clean working tree |
| Vault Fresh | Pull latest from Obsidian git sync | No vault conflicts | Current specs/decisions |
| lat.md Sync | Refresh lat.md index from latest code (incremental update) | Code index reflects current state | Fresh `lat_index.db` |
| Session State | Initialize context (vault, repo memory, graph) | All context ready | Session context loaded |
| Feature Readiness | Verify no blocking issues | Prerequisites met | Ready to start |

### Output Artifacts
- Clean git working tree
- Loaded session context (vault, repo memory, lat.md)
- Ready-to-use project context (specs, decisions, lessons)

### Exit Criteria
- ✅ Git working tree clean (or staged changes approved)
- ✅ Vault synced with origin
- ✅ lat.md up-to-date
- ✅ Session context available

---

## Specification

### Commands
```
/spek.plan --phase=specify
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
    ├─ Query lat.md for affected areas
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
- Links to lat.md impact analysis
- Links to relevant architectural decisions

### Exit Criteria
- ✅ Specification written and clear
- ✅ Success Criteria defined
- ✅ Assumptions documented
- ✅ Risk Assessment complete
- ✅ Spec committed to vault

---

## Task Breakdown (Planning Phase: Part 2)

### Commands
```
/spek.plan --phase=plan
# or separately:
/speckit.plan --spec="feature-spec-id"
/speckit.tasks --plan="feature-plan-id"
```

### Purpose
Convert specification into detailed execution plan (architecture + tech choices), then break plan into dependency-ordered executable tasks.

### Workflow (Two-Step Process)

```
SPEC DOCUMENT
    ↓
STEP 1: /speckit.plan (Architecture & Tech Design)
    ├─ Analyze spec requirements
    ├─ Design architecture + tech choices
    ├─ Query lat.md for affected areas
    ├─ Document rationale and technology decisions
    └─ OUTPUT: plan.md (stored in vault)
    ↓
STEP 2: /speckit.tasks (Task Decomposition)
    ├─ Read plan.md
    ├─ Break plan into executable tasks
    ├─ Determine task dependencies (A blocks B)
    ├─ Estimate per-task resources
    ├─ Query lat.md for file locations
    └─ OUTPUT: tasks.md (ordered, IDs, dependencies, risk mitigation)
    ↓
COMPLETE: PLAN + TASKS ARTIFACTS (vault + git commit)
```

### Plan Structure

Example plan excerpt:

```markdown
## Task Breakdown

### Auth Service Setup
- Description: Create authentication service with token validation
- Depends On: None (blocks related tasks)
- Complexity: Medium
- Resource notes: Specify project-specific resource estimates in task metadata
- Files Affected: src/auth/service.ts, test/auth.test.ts

### User Model Extension
- Description: Add OAuth fields to User model
- Depends On: Auth Service (API must be defined)
- Complexity: Low
- Resource notes: Specify project-specific resource estimates in task metadata
- Files Affected: src/models/user.ts, migration/001-oauth-fields.sql

### Integration Tests
- Description: Write E2E tests for OAuth flow
- Depends On: Auth Service, User Model
- Complexity: High
- Resource notes: Specify project-specific resource estimates in task metadata
- Files Affected: test/e2e/auth.test.ts, test/fixtures/oauth-mock.ts

## Dependency Graph

Auth Service (Auth Service)
    ├─→ User Model (depends)
    └─→ Integration Tests (depends)
```

### Output Artifacts
- `plan.md` — Architecture, tech choices, rationale, research (Markdown, vault-stored)
- `tasks.md` — Dependency-ordered executable tasks with IDs, resource estimates, critical path (Markdown, vault-stored)
- lat.md references for implementation
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

## Implementation

### Commands
```
/spek.implement --plan="feature-plan-id"
# Runs tasks in dependency order
```

### Purpose
Execute each task from the plan with full context (spec, plan, lat.md, enrichment).

### Workflow Per Task

```
FOR EACH TASK IN PLAN (in dependency order):
    ├─ Load Task Context
    │  ├─ Spec (what/why)
    │  ├─ Plan (dependencies, what this task does)
    │  ├─ lat.md (files to change, impact analysis)
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
| **lat.md** | Live analysis | What files need to change? Who calls what? |
| **Risk Assessment** | Plan + Spec | What could fail? How to mitigate? |
| **Previous Outcomes** | Vault (updated) | What did earlier tasks create? |

### Implementation Checklist (Per Task)

- [ ] Load task context from plan
- [ ] Read Success Criteria for this task
- [ ] Query lat.md for affected symbols/files
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
- [ ] Unit tests pass locally
- [ ] Integration tests pass locally
- [ ] Edge cases covered (null, empty, invalid input)
- [ ] Error paths tested (exceptions, boundary conditions)
- [ ] Test coverage is sufficient for new code
- [ ] Existing tests still pass (no breaking changes)
- [ ] Full test suite runs locally within acceptable time

**lat.md Integration**
- [ ] lat.md reflects all new code (symbols, functions, classes)
- [ ] Impact analysis shows affected downstream components
- [ ] lat.md queries used during implementation (not file grep)

**Vault Integration**
- [ ] Spec stored in vault with correct metadata
- [ ] Plan stored in vault with task linkage
- [ ] All artifacts committed to git (no uncommitted changes)

**Spekificity Workflow**
- [ ] `/spek.prepare` passed pre-flight checks
- [ ] `/spek.plan --phase=specify` produced valid spec
- [ ] `/spek.plan --phase=plan` produced valid plan
- [ ] `/spek.implement` executed all tasks
- [ ] All `/spek.*` commands worked end-to-end

**Performance**
- [ ] Token budget not exceeded (if one was set)
- [ ] lat.md queries working correctly
- [ ] API responses working (if applicable)
- [ ] No N+1 queries or unnecessary loops

**Sign-Off**
- [ ] Code reviewed (if applicable)
- [ ] All Integration Checklist items checked
- [ ] Feature ready for archive and closeout

---

## Stage 5: Feature Conclusion

### Commands
```
/spek.conclude
# Includes: archive, lessons extraction (automatic), state refresh

# Optional (for deeper analysis):
/spek.lessons --deep
# Explicit, detailed lesson extraction (runs separately from /spek.conclude)
```

### Purpose
Archive outcomes, extract lessons learned (automatic), refresh state for future features. `/spek.lessons --deep` available for explicit, detailed reflection.

### Workflow

```
IMPLEMENTATION COMPLETE
    ↓
/spek.conclude
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
    │  ├─ Rebuild lat.md index (full index incorporating feature changes)
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
- Updated lat.md index (fresh)
- Updated repo memory
- Feature complete (tagged in git)

### Exit Criteria
- ✅ Feature artifacts archived in vault
- ✅ Lessons learned extracted and committed
- ✅ lat.md refreshed
- ✅ Repo memory updated
- ✅ Session context cleaned

---

### Lesson Extraction Details

**Automatic (via `/spek.conclude`):**
- Lightweight, structured format
- Runs as part of standard closeout workflow
- Suitable for most features
- Captured: what worked, what was difficult, patterns, recommendations

**Explicit/Deep (via `/spek.lessons --deep`):**
- Detailed reflection and analysis
- Cross-references specs, plans, code, and decisions
- Optional, for complex features or research projects
- Runs independently after `/spek.conclude`
- Produces: comprehensive feature retrospective with architectural insights

**When to use:**
- Standard feature: `/spek.conclude` (automatic lessons)
- Complex refactor or architectural change: `/spek.conclude` + `/spek.lessons --deep`
- Research/experimental work: `/spek.lessons --deep` for thorough analysis

## Timeline Diagram

```
DAY 1
├─ Morning: /spek.prepare          [short setup]
├─ Morning: /spek.plan             [spec + plan review]
├─ Afternoon: Review & Approve     [stakeholder sign-off]
│
DAY 2
├─ Morning: /spek.implement        [implementation work]
├─ Afternoon: /spek.implement      [continued implementation]
├─ Late: Local testing + fixes     [testing and fixes]
│
DAY 3
├─ Morning: Final validation       [final validation]
├─ Afternoon: /spek.conclude       [archive + lessons]
│
TOTAL: multi-day effort
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
- **Problem:** `/spek.conclude` completes but lessons are shallow
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
- **Naming & Commands:** [conventions.md](conventions.md)
- **Integration Checklist:** [integration-checklist.md](integration-checklist.md)
- **Architecture Notes** — Key decisions and rationale
- **Pattern Library:** [patterns/](patterns/)
