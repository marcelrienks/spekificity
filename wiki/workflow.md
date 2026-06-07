# Feature Development Workflow

## Overview

Spekificity implements a deterministic, 4-stage feature development workflow:

- **Prepare** – Pre-flight checks and workspace setup
- **Plan** – Write feature spec, generate implementation plan & tasks (2 sub-stages: Specification, Task Breakdown)
- **Implement** – Execute tasks with full context
- **Conclude** – Archive outcomes, extract lessons, sync vault, update graph

**Design:** Optional enhancements (context loading, dependency analysis, retrospectives) available at any stage. Each stage produces durable artifacts stored in the vault.

---

## Preparation

### Command
```
/spek.prepare
```

### Purpose
Perform pre-flight checks before feature development begins. Ensures workspace is ready, vault is current, lat.md index is fresh, and git state is clean.

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

## Specification (Sub-Stage: Plan Phase)

### Commands
```
/spek.plan --phase=specify
# or directly:
/speckit.specify --feature="feature-name"
```

### Purpose
Create detailed feature specification with enrichment layers (Success Criteria, Assumptions, Risk Assessment, Metrics).

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

## Task Breakdown (Sub-Stage: Plan Phase)

### Commands
```
/spek.plan --phase=plan
# or separately:
/speckit.plan --spec="feature-spec-id"
/speckit.tasks --plan="feature-plan-id"
```

### Purpose
Convert specification into detailed execution plan (architecture + tech choices), break plan into dependency-ordered executable tasks. Part of Plan stage (along with spec generation).

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
    ├─ Access Task Context (loaded once at /spek.prepare, reused)
    │  ├─ Spec (what/why)
    │  ├─ Plan (dependencies, what this task does)
    │  ├─ lat.md (files to change, impact analysis from prepare)
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
- [ ] Feature ready for archive and conclude

---

## Conclude: Feature Conclusion

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
    ├─ Extract lessons learned (Automatic)
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

### lessons learned Structure

Lessons stored in vault with template:

```markdown
## Feature: [Feature Name]
Date: 2026-05-20
Status: Complete

### What went well
- [pattern/approach/tool that worked]
- [pattern/approach/tool that worked]

### What was difficult
- [challenge/blocker]
- [mitigation used]

### Patterns discovered
- [reusable pattern]
- [architectural insight]

### Recommendations for future
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
- Runs as part of standard conclude workflow
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

## Timeline Diagram (4 Stages)

```
DAY 1
├─ Morning: /spek.prepare          [short setup]
├─ Morning: /spek.plan (spec)      [feature spec + enrichment]
├─ Afternoon: /spek.plan (task)    [plan + task breakdown]
├─ Late: Review & Approve          [stakeholder sign-off]
│
DAY 2-3
├─ /spek.implement                 [execute tasks]
├─ Local testing + fixes           [validation]
│
DAY 4
├─ Morning: Final validation       [final integration check]
├─ Afternoon: /spek.conclude       [archive + lessons + graph refresh]
│
TOTAL: multi-day effort (4 stages)
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

---

## Example: User Authentication Feature

This section walks through a complete feature cycle using the workflow above.

### Prepare Workspace

**Command:** `/spek.prepare`

```
✓ Git working tree clean
✓ Vault synced from origin
✓ lat.md index refreshed
✓ Session context loaded
READY: Workspace prepared for feature development
```

**What happened:**
- Git verified clean (no uncommitted work)
- Vault pulled (latest specs/decisions/lessons from vault/)
- lat.md queried for affected files
- Session memory loaded (decisions, patterns from vault/)
- Feature state file created

### Specify Feature

**Command:** `/spek.plan --phase=specify --feature="user-auth-api"`

```
SPEC GENERATION
├─ Feature Intent: "POST /auth/login endpoint validates credentials, returns JWT"
├─ Query lat.md:
│  ├─ Found existing: auth/models.py (user model)
│  ├─ Found existing: auth/tokens.py (jwt utilities)
│  └─ Impact: several existing files touch auth system
│
├─ Enrich with layers:
│  ├─ Success Criteria:
│  │  - ✓ POST /auth/login accepts email + password
│  │  - ✓ Valid credentials return JWT token
│  │  - ✓ Invalid credentials return 401
│  │  - ✓ JWT validates on protected endpoints
│  │  - ✓ high test coverage on new code
│  │
│  ├─ Assumptions:
│  │  - User model exists (✓ verified in lat.md)
│  │  - JWT utilities exist (✓ verified in lat.md)
│  │  - Passwords already hashed (✓ verified in auth/models.py)
│  │
│  ├─ Risk Assessment:
│  │  - 🔴 HIGH: SQL injection if not parameterized (mitigation: ORM only)
│  │  - 🟡 MEDIUM: Token expiry not configurable (mitigation: add ENV var)
│  │  - 🟢 LOW: Rate limiting not implemented (mitigation: future feature)
│  │
│  └─ Resource Estimate:
│     - Complexity: Medium (multiple files touched; existing patterns reused)
│     - Tokens: not specified
│     - Time: not specified
│
└─ Output: vault/specs/150-user-auth-api.md (CREATED)
   └─ Ready for planning phase
```

**What was produced:**
- `/wiki/specs/150-user-auth-api.md` — Complete spec with enrichment layers
- Linked to existing patterns (JWT handling, error handling)
- Cross-referenced with existing decisions (why we use JWT not sessions)
- Risk assessment documented
- Success criteria crystal clear

### Create Plan

**Command:** `/spek.plan --phase=plan`

```
TASK BREAKDOWN
├─ Spec parsed: 150-user-auth-api.md
├─ lat.md queried: affected files and functions identified
│
├─ Dependencies analyzed:
│  ├─ Upstream: User model (EXISTS, no changes needed)
│  ├─ Upstream: JWT utilities (EXISTS, extend token generation)
│  └─ Downstream: Protected endpoints (WILL use new endpoint)
│
├─ Tasks generated:
│  │
│  ├─ Task 1: Add login route handler
│  │  ├─ File: auth/routes.py
│  │  ├─ Depends: User model, JWT utils
│  │  └─ Success: Handler accepts email + password, returns JWT or 401
│  │
│  ├─ Task 2: Add unit tests (login handler)
│  │  ├─ File: tests/auth/test_routes.py
│  │  ├─ Depends: Task 1
│  │  └─ Success: Comprehensive coverage, all cases covered (valid, invalid, expired)
│  │
│  ├─ Task 3: Add integration tests (full auth flow)
│  │  ├─ File: tests/integration/test_auth_flow.py
│  │  ├─ Depends: Task 1, Task 2
│  │  └─ Success: End-to-end flow works (login → token → protected endpoint)
│  │
│  └─ Task 4: Update docs
│     ├─ File: docs/API.md
│     ├─ Depends: Task 1
│     └─ Success: Login endpoint documented with examples
```

**What was produced:**
- `/wiki/specs/151-user-auth-plan.md` — Detailed task breakdown
- Dependencies validated (no blocking issues)
- Sequence determined (tasks 2/3 depend on task 1, can parallelize after)
- Ready to implement

### Execute Implementation

**Command:** `/spek.implement --task=1 --task=2 --task=3 --task=4`

For each task:

```
IMPLEMENTING TASK 1: Add login route handler

INPUT:
├─ Task spec (150-user-auth-api.md + 151-user-auth-plan.md)
├─ lat.md results (where to add code, what exists, what to reuse)
├─ Existing patterns (JWT handling, error responses)
└─ Session memory (decisions from previous features)

EXECUTION:
├─ Agent reads task spec
├─ Agent queries lat.md for:
│  ├─ User model location + interface
│  ├─ JWT utilities location + interface
│  ├─ Existing error handling patterns
│  └─ Where to add route (app.py, routes.py, etc.)
│
├─ Agent writes code:
│  ├─ Adds POST /auth/login handler
│  ├─ Validates input (email, password)
│  ├─ Queries user by email
│  ├─ Checks password (using bcrypt)
│  ├─ Generates JWT token
│  └─ Returns token or 401
│
├─ Agent writes comprehensive tests
│  ├─ Valid credentials → token returned
│  ├─ Invalid email → 401
│  ├─ Invalid password → 401
│  ├─ Expired token rejected
│  └─ Protected endpoint requires valid token
│
└─ OUTPUT:
   ├─ auth/routes.py (NEW)
   ├─ tests/auth/test_routes.py (NEW)
   ├─ .git diff (tracked)
   └─ Session trace (what was tried, what worked)
```

Tasks 2, 3, 4 follow same pattern. By end of implementation phase:

```
✓ Task 1: Login handler written + unit tested (DONE)
✓ Task 2: Unit tests all passing (DONE)
✓ Task 3: Integration tests passing (DONE)
✓ Task 4: API docs updated (DONE)

Code changes committed to git.
Ready for closing phase.
```

### Archive & Close

**Command:** `/spek.conclude --caveman-mode=full`

```
FEATURE COMPLETION & VAULT SYNC

Step 1: Collect Artifacts
├─ Feature state (user-auth-api)
├─ Spec (150-user-auth-api.md)
├─ Plan (151-user-auth-plan.md)
├─ Code changes (git diff)
├─ Execution trace (what was tried, what worked)
└─ Test results

Step 2: Activate Caveman Compression
├─ Active voice, concrete, no filler
└─ Compress output

Step 3: Generate Lessons
├─ What worked:
│  - JWT token generation pattern applied cleanly
│  - lat.md impact analysis reduced manual code review effort
│  - Unit test template from existing auth tests reused
│
├─ What didn't:
│  - Initial attempt at rate limiting too complex (deferred to future)
│  - Password validation edge cases found in integration testing
│
├─ Patterns discovered:
│  - "Error response pattern for 401/403 cases" (reusable)
│  - "JWT token generation and validation" (already captured)
│
├─ Decisions made:
│  - Why: JWT chosen over session for statelessness (scalability)
│  - Why: Token expiry set to 24h (balance security + UX)
│
└─ Output: vault/lessons/2026-05-20-user-auth-api-implementation.md (CREATED)

Step 4-5: Update Vault
├─ vault/decision.md (append new architectural decisions)
├─ vault/patterns.md (log pattern usage + frequency)
└─ Feature marked as COMPLETED

Step 6-7: Sync Repo Memory
├─ vault/repo/architectural-decisions.md (updated)
├─ vault/repo/patterns-index.md (updated)
└─ Ready for next project to use

Step 8: Refresh lat.md index
├─ Scan new code (auth/routes.py, tests/)
├─ Update index with new functions/classes
└─ Graph now includes login handler, tests

Step 9: Archive Feature State
├─ Move vault/session/current-feature.md to vault/archive/
├─ Clean up session temporary files
└─ Ready for next feature

Step 10: Report Completion
└─ FEATURE COMPLETE: user-auth-api
   ├─ Code added: auth/routes.py
   ├─ Tests added: Multiple test cases with comprehensive coverage
   ├─ Docs added: API.md updated
   ├─ Lessons: Patterns refined, decisions logged
   └─ Next feature can reuse patterns/decisions from vault
```

**What was produced:**
- Lessons documented and indexed in vault
- Decisions logged with rationale
- Patterns captured for reuse
- lat.md updated and ready
- Session memory archived
- Repository ready for next feature

---

---

## SpecKit Workflow Reference

SpecKit is the spec-driven development workflow engine that Spekificity wraps and enriches. This section shows the canonical SpecKit flow; for Spekificity integration details and full workflow context, see the main workflow section above.

### Canonical SpecKit Flow

```
/speckit.constitution
    ↓
/speckit.specify
    ↓
/speckit.clarify (optional)
    ↓
/speckit.plan
    ↓
/speckit.tasks
    ↓
/speckit.analyze (optional)
    ↓
[FIX ARTIFACTS IN-PLACE IF NEEDED]
    ↓
/speckit.implement
    ↓
[FEATURE COMPLETE]
```

### SpecKit Command Reference

| Command | Purpose | Input | Output | Re-runnable |
|---------|---------|-------|--------|------------|
| `/speckit.constitution` | Define project principles | Developer input | `.specify/memory/constitution.md` | Yes (updates, doesn't break) |
| `/speckit.specify` | Write feature spec | Feature description (what + why) | `specs/NNNN-feature.md` + feature branch | Yes (regenerates from prompt) |
| `/speckit.clarify` | Resolve spec ambiguities | Current spec | Updated spec | Yes |
| `/speckit.plan` | Create implementation plan | Spec + constitution | `plan.md`, `data-model.md`, `contracts/` | Yes (regenerates) |
| `/speckit.tasks` | Generate task list | Plan + data model | `tasks.md` (dependency-ordered) | Yes (regenerates) |
| `/speckit.analyze` | Cross-artifact consistency check | Spec + plan + tasks | Analysis report (ambiguities, gaps, risks) | Yes (non-blocking) |
| (manual remediation) | Fix artifacts in-place | Analyze report | Updated spec/plan/tasks | N/A (manual) |
| `/speckit.implement` | Execute all tasks | Tasks + plan + spec | Generated code | Yes (per-task execution) |

### SpecKit + Spekificity Integration

Spekificity wraps SpecKit phases with context injection and enrichment:

```
/spek.plan (Spekificity wrapper)
    ├─ PRE: Load vault decisions + patterns + code graph (lat.md)
    ├─ CORE: /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze
    └─ POST: Validate output aligns with decisions; flag contradictions

/spek.implement (Spekificity wrapper)
    ├─ PRE: Load decisions + patterns + code graph
    ├─ CORE: /speckit.implement (per-task execution)
    └─ POST: Collect diff; validate against spec; log decisions
```

### Key Clarifications

**Analyze Output:** Non-blocking; `/speckit.analyze` identifies gaps but doesn't prevent `/speckit.implement`.

**Remediation:** Manual in-place editing (no automatic regeneration loop). After fixing, optionally re-run `/speckit.analyze` to verify.

**SpecKit Vanilla vs Spekificity:**
- Use `/speckit.*` directly for raw SpecKit workflow (no enrichment)
- Use `/spek.plan` and `/spek.implement` for Spekificity enriched workflow (context injection + validation)

---

## References

- **Architecture:** [architecture.md](architecture.md) — technical design and component responsibilities
- **Naming & Commands:** [conventions.md](conventions.md) — command naming and file conventions
- **Patterns:** [patterns.md](patterns.md) — reusable patterns used throughout workflow
- **Decisions:** [decision.md](decision.md) — architectural decisions and rationale
- **Skills:** [skills.md](skills.md) — command reference and usage
