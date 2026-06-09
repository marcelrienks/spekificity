# Feature Development Workflow

## Overview

Spekificity implements a deterministic, 4-stage feature development workflow:

- **Prepare** – Initialize third-party tools (lat.md code + doc indexes, Obsidian vault) and load context
- **Plan** – Orchestrate SpecKit: specify → plan → tasks (with remediations)
- **Implement** – Execute tasks via SpecKit implement
- **Conclude** – All post-implementation: analysis, lessons, vault archive, state refresh

**All stages are agent skills, not CLI commands.** Run them inside your agent (Claude Code, Copilot, etc.). Only `spek init` is a CLI command.

**Artifacts stored in `.spek/vault/`** (not `vault/` at project root).

---

## Preparation

### Command
```
/spek.prepare
```

### Purpose
Initialize all third-party tools and load context before feature development. `/spek.prepare` does not just check workspace state — it actively builds and stores the indexes that all subsequent skills depend on.

### Sub-steps

| Step | Action | Output |
|------|--------|--------|
| lat.md Code Index | Initialize/refresh lat.md index of source code (symbols, definitions, call graphs) | Code index ready in `.spek/lat/` |
| lat.md Doc Index | Initialize/refresh lat.md index of documentation (wiki, vault, markdown files) — **separate index** | Doc index ready in `.spek/lat/` |
| Vault Storage | Store both indexes in Obsidian vault (`.spek/vault/`) for persistent context | Indexes persisted |
| Context Load | Load vault decisions, patterns, prior lessons into agent session | Session context ready |
| Constitution Check | Verify `.specify/memory/constitution.md` exists. If missing, invoke `/speckit.constitution` to create it (one-time, interactive). Constitution defines project principles SpecKit embeds into all spec/plan generation. | Constitution present |

**Why two separate indexes:** Code index answers "where is X defined / what calls it." Doc index answers "what decisions or patterns relate to topic X." Merging them degrades both queries.

### Output Artifacts
- lat.md code index (fresh, stored in `.spek/lat/`)
- lat.md doc index (fresh, stored in `.spek/lat/`)
- Vault context loaded (decisions, patterns, lessons in agent session)
- Project constitution verified

### Exit Criteria
- ✅ lat.md code index initialized and current
- ✅ lat.md doc index initialized and current
- ✅ Vault context loaded into session
- ✅ Constitution exists

---

## Plan

### Command
```
/spek.plan [feature-name]
```

### Purpose
Orchestrate full SpecKit planning pipeline in sequence, with user review and remediation at each step.

### Workflow

```
FEATURE INTENT
    ↓
STEP 1: /speckit.specify
    ├─ Generate spec (what, why, scope, success criteria)
    ├─ Query lat.md doc index for related decisions + patterns
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run step 1]
STEP 2: /speckit.plan
    ├─ Generate implementation plan from approved spec
    ├─ Query lat.md code index for affected areas
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run step 2 (or step 1 if spec was wrong)]
STEP 3: /speckit.tasks
    ├─ Break plan into dependency-ordered executable tasks
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run from affected step]
COMPLETE: spec.md + plan.md + tasks.md (stored in .spek/vault/)
```

**Remediation loop:** After each step, surface output to user. If user requests changes, apply and reprocess from that step forward. Continue until all three outputs are approved.

### Output Artifacts
- `spec.md` — Feature specification with success criteria (stored in `.spek/vault/`)
- `plan.md` — Architecture, tech choices, affected code areas (stored in `.spek/vault/`)
- `tasks.md` — Dependency-ordered tasks with IDs (stored in `.spek/vault/`)

### Exit Criteria
- ✅ Spec approved by user
- ✅ Plan approved by user
- ✅ Task list approved by user
- ✅ All artifacts committed to `.spek/vault/`

---

## Implementation

### Command
```
/spek.implement [--steps N]
```

### Purpose
Execute approved tasks by wrapping `/speckit.implement`. `/spek.implement` is intentionally thin — it loads context (spec, plan, tasks from `.spek/vault/`) then delegates execution entirely to SpecKit.

### Workflow

```
LOAD context from .spek/vault/ (spec + plan + tasks)
    ↓
/speckit.implement
    ├─ Executes all tasks in dependency order
    ├─ SpecKit owns per-task execution, code generation, step tracking
    └─ Use --steps N to jump to a specific task (resume)
    ↓
IMPLEMENTATION COMPLETE
```

SpecKit handles all per-task detail (code writing, test running, commits). Spekificity's role is context loading before the call, not wrapping each step.

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
- [ ] `/spek.plan` produced valid spec (specify step)
- [ ] `/spek.plan` produced valid plan (plan step)
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

### Command
```
/spek.conclude
```

### Purpose
All post-implementation functions. `/spek.conclude` is the only conclude command — it handles analysis, lessons, vault archive, and state refresh in a single skill. `/spek.lessons` is called as a sub-step inside conclude; it can also be invoked independently at any point.

### Workflow

```
IMPLEMENTATION COMPLETE
    ↓
/spek.conclude
    │
    ├─ 1. Analysis
    │  └─ /speckit.analyze — validate implementation against spec
    │     ├─ Compare Success Criteria vs actual outcomes
    │     └─ Flag spec drift or deviations
    │
    ├─ 2. Lessons (sub-step: /spek.lessons)
    │  ├─ Prompt for retrospective (what worked, what was difficult)
    │  ├─ Extract new patterns if workflow diverged from spec
    │  ├─ Log new decisions if architecture changed
    │  └─ Write lessons to .spek/vault/lessons/YYYY-MM-DD-feature-name.md
    │
    ├─ 3. Vault Archive
    │  ├─ Archive spec + plan + tasks to .spek/vault/
    │  ├─ Update .spek/vault/patterns.md
    │  └─ Update .spek/vault/decisions.md
    │
    ├─ 4. State Refresh
    │  ├─ /lat.sync — refresh lat.md code index (new code)
    │  ├─ /lat.sync — refresh lat.md doc index (vault updates)
    │  └─ Sync repo memory to .spek/memory/
    │
    └─ 5. Commit
       ├─ git add .spek/vault/ .spek/memory/
       └─ git commit
    ↓
FEATURE ARCHIVED, LESSONS CAPTURED, READY FOR NEXT FEATURE
```

### Lessons Template

Lessons stored at `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`:

```markdown
## Feature: [Feature Name]
Date: YYYY-MM-DD
Status: Complete

### What went well
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
- Spec: [link to spec in .spek/vault/]
- Plan: [link to plan in .spek/vault/]
- Decisions Made: [link to decision entries]
- Pull Requests: [GitHub PR links]
```

### Output Artifacts
- Analysis report (spec drift, outcomes vs criteria)
- Lessons document (`.spek/vault/lessons/YYYY-MM-DD-feature-name.md`)
- Archived spec + plan + tasks (`.spek/vault/`)
- Updated patterns + decisions (`.spek/vault/`)
- lat.md indexes refreshed (code + docs)
- Repo memory synced (`.spek/memory/`)

### Exit Criteria
- ✅ Analysis complete (spec drift documented)
- ✅ Lessons extracted and committed to vault
- ✅ Feature artifacts archived
- ✅ lat.md code + doc indexes refreshed
- ✅ Repo memory updated

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
- **Recovery:** Re-run `/spek.conclude` and provide more detailed retrospective input when prompted
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

**Command:** `/spek.plan "user-auth-api"` (runs specify → plan → tasks in sequence; example below shows specify step output)

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
└─ Output: .spek/vault/specs/150-user-auth-api.md (CREATED)
   └─ Ready for planning phase
```

**What was produced:**
- `.spek/vault/specs/150-user-auth-api.md` — Complete spec with enrichment layers
- Linked to existing patterns (JWT handling, error handling)
- Cross-referenced with existing decisions (why we use JWT not sessions)
- Risk assessment documented
- Success criteria crystal clear

### Create Plan

**Command:** (plan step within `/spek.plan` above — not a separate invocation)

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
- `.spek/vault/specs/151-user-auth-plan.md` — Detailed task breakdown
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
└─ Output: .spek/vault/lessons/2026-05-20-user-auth-api-implementation.md (CREATED)

Step 4-5: Update Vault
├─ .spek/vault/decisions.md (append new architectural decisions)
├─ .spek/vault/patterns.md (log pattern usage + frequency)
└─ Feature marked as COMPLETED

Step 6-7: Sync Repo Memory
├─ .spek/vault/repo/architectural-decisions.md (updated)
├─ .spek/vault/repo/patterns-index.md (updated)
└─ Ready for next project to use

Step 8: Refresh lat.md index
├─ Scan new code (auth/routes.py, tests/)
├─ Update index with new functions/classes
└─ Graph now includes login handler, tests

Step 9: Archive Feature State
├─ Move .spek/vault/session/current-feature.md to .spek/vault/archive/
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

Spekificity wraps SpecKit. The relationship:

```
/spek.plan
    ├─ Calls /speckit.specify (step 1, with user review + remediation loop)
    ├─ Calls /speckit.plan    (step 2, with user review + remediation loop)
    └─ Calls /speckit.tasks   (step 3, with user review + remediation loop)
    NOTE: /speckit.clarify and /speckit.analyze are NOT called automatically

/spek.implement
    └─ Calls /speckit.implement (delegates execution entirely)

/spek.conclude
    ├─ Calls /speckit.analyze  (step 1, analysis)
    └─ Runs /spek.lessons      (step 2, as sub-function — not a standalone command)
```

### Key Clarifications

**`/speckit.clarify` is optional:** Call it manually if spec ambiguities need resolution. `/spek.plan` does not auto-invoke it.

**`/speckit.analyze` is called by `/spek.conclude`:** Not by `/spek.plan`. It validates the completed implementation, not the plan.

**`/spek.lessons` is not standalone:** It runs as step 2 inside `/spek.conclude`. There is no separate `/spek.lessons` command in the workflow.

**SpecKit Vanilla vs Spekificity:**
- `/speckit.*` directly: raw SpecKit, no enrichment, no vault context
- `/spek.*`: Spekificity wrapper — loads vault context, drives user approval loops, persists to `.spek/vault/`

---

## References

- **Architecture:** [architecture.md](architecture.md) — technical design and component responsibilities
- **Naming & Commands:** [conventions.md](conventions.md) — command naming and file conventions
- **Patterns:** [patterns.md](patterns.md) — reusable patterns used throughout workflow
- **Decisions:** [decision.md](decision.md) — architectural decisions and rationale
- **Skills:** [skills.md](skills.md) — command reference and usage
