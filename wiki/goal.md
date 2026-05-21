# Spekificity: The Complete Goal

> **Purpose:** Single source of truth for what Spekificity is, what it delivers, and how it operates when fully implemented.
>
> **Read Time:** 10 minutes  
> **For:** Anyone trying to understand the complete vision and end state

---

## The Problem

AI agents often produce code without clear, durable specifications. **Four critical problems emerge:**

| Problem | Impact |
|---------|--------|
| **Token Bloat** | Context is re-scanned for every query. Grep + file reads wasteful. Same code analyzed repeatedly. |
| **Shallow Planning** | Features are coded without specs. Decisions are made ad-hoc. No clear success criteria. Scope creep inevitable. |
| **Context Loss** | Session ends → all context forgotten. Next session rebuilds from scratch. Patterns discovered once, never reused. Lessons lost. |
| **Low Autonomy** | Agents need hand-holding. Work requires constant human guidance. Hard to delegate. Cannot run overnight. |

**Consequence:** Features take longer than they should. Cost more tokens than necessary. Knowledge dies between sessions.

---

## The Solution: Spekificity

Spekificity is a **specification-driven agent development framework** built around four pillars:

### 1. Token Efficiency
**Every token counts. Agent queries should be pre-indexed, not re-scanned.**

- **CodeGraph MCP:** Real-time indexed code analysis (pre-indexed, no file scanning)
  - Pre-indexed SQLite database auto-syncs when files change
  - Supports multiple languages via AST parsing
  - Tools: `codegraph_symbols()`, `codegraph_references()`, `codegraph_impact()`, `codegraph_definition()`

- **Scoped Context Loading:** Vault loaded once per session, not per query
  - Specs, decisions, patterns stored and referenced repeatedly
  - Memory architecture (3-layer: user, session, repo) prevents redundant loads

- **Caveman Compression:** Response format cuts token usage 75-90%
  - Concrete, active voice, no filler
  - Same technical accuracy with 1/4 the tokens

### 2. Determinism
**Repeatable workflows. No guessing. No drift.**

- **Spec-First Workflow:** All work starts with a structured specification
  - Defines *what* and *why* before implementation
  - Success Criteria, Assumptions, Risk Assessment documented upfront
  - No code without a spec

- **SpecKit Pipeline:** Deterministic sequence
  - Prepare (workspace ready, git clean, graph fresh)
  - Specify (enriched spec generation)
  - Plan (task breakdown with impact analysis)
  - Implement (execute tasks with full context)
  - Post (archive lessons, refresh state)

- **Reusable Skills:** `/spek.*` commands are composable and opinionated
  - `/spek.prepare` — Pre-flight checks
  - `/spek.plan` — SpecKit orchestration
  - `/spek.implement` — Task execution
  - `/spek.conclude` — Completion & vault sync

### 3. Persistence
**Knowledge outlives sessions.**

- **Obsidian Vault:** Git-backed markdown knowledge store
  - Specifications (what to build)
  - Plans (how to build it)
  - Decisions (why we chose this approach)
  - Patterns (reusable solutions)
  - Lessons (what we learned)
  - Architecture decisions (rationale)

- **Session Memory:** Three-layer architecture persists context
  - **User memory** (`vault/user/`) — Persistent user preferences in vault
  - **Session memory** (`vault/session/`) — Scoped to current session
  - **Repo memory** (`vault/repo/`) — Scoped to this project

- **CodeGraph Auto-Sync:** Never stale
  - File watches implemented
  - Incremental updates on file change
  - Query results always current

### 4. Autonomy
**Agents have clear boundaries and tools.**

- **Skill Reuse:** Patterns, decisions, lessons are indexed and retrievable
  - New agent joining mid-project can read vault and understand context
  - No need to re-discover what's been tried
  - Can suggest solutions based on captured patterns

- **Graph-Grounded Context:** CodeGraph provides pre-indexed facts
  - No agent reasoning about "where does this function live?"
  - No guessing about impact
  - Deterministic analysis, not emergent reasoning

- **Skill Chaining:** Multi-agent workflows are explicit, composable
  - Five core skills form a deterministic pipeline (see "Spekificity Skills" section for details)

---

## Spekificity Skills: The Complete Toolkit

The framework is implemented through a set of reusable, composable skills. All skills are prefixed with `/spek.` and follow a deterministic pattern.

### Core Skills (Usage Order)

These five skills form the primary workflow. Each is required; each has a specific place in the cycle:

| Order | Skill | Purpose | Input | Output |
|-------|-------|---------|-------|--------|
| 1️⃣ | `/spek.prepare` | Pre-flight checks | Workspace state | Clean workspace + vault synced + CodeGraph fresh |
| 2️⃣ | `/spek.plan --phase=specify` | Enriched spec generation | Feature intent | `wiki/specs/NNN-feature-name.md` with enrichment layers |
| 3️⃣ | `/spek.plan --phase=plan` | Task breakdown & validation | Specification | `wiki/specs/NNN-feature-plan.md` with dependencies |
| 4️⃣ | `/spek.implement` | Execute tasks with full context | Tasks from plan | Code + tests + docs in git |
| 5️⃣ | `/spek.conclude` | Archive & vault sync | Execution artifacts | Lessons in vault + decisions logged + CodeGraph refreshed |

**Bookend Principle:** Skills 1 & 5 are semantic opposites:
- `/spek.prepare` prepares the workspace FOR work
- `/spek.conclude` completes the work and persists knowledge

**The Complete Workflow:**
```
┌─────────────────────────────────────────────────────────────┐
│ Feature Development Cycle (Fully Deterministic)             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  /spek.prepare                                               │
│  ├─ Pre-flight checks (git clean, vault synced)             │
│  ├─ CodeGraph refresh (indexed queries ready)               │
│  └─ Session context loaded                                  │
│       ↓                                                      │
│  /spek.plan --phase=specify                                 │
│  ├─ Feature intent enriched                                 │
│  ├─ Success criteria defined                                │
│  ├─ Assumptions documented                                  │
│  ├─ Risks assessed                                          │
│  └─ Spec stored in wiki/specs/                              │
│       ↓                                                      │
│  /spek.plan --phase=plan                                    │
│  ├─ Tasks broken down                                       │
│  ├─ Dependencies analyzed                                   │
│  ├─ Impact mapped (CodeGraph)                               │
│  └─ Plan stored in wiki/specs/                              │
│       ↓                                                      │
│  /spek.implement                                            │
│  ├─ Tasks executed sequentially/parallel                    │
│  ├─ Code written per spec                                   │
│  ├─ Tests written (95%+ coverage)                           │
│  ├─ Docs updated                                            │
│  └─ Changes committed to git                                │
│       ↓                                                      │
│  /spek.conclude                                             │
│  ├─ Lessons extracted & stored                              │
│  ├─ Decisions logged with rationale                         │
│  ├─ Patterns indexed for reuse                              │
│  ├─ CodeGraph updated                                       │
│  └─ Session archived → ready for next feature               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Optional/Enhancement Skills

These skills augment the core workflow. Use them when the situation calls for it:

| Skill | When to Use | Purpose |
|-------|------------|---------|
| `/spek.context` | Start of session | Load persisted vault (decisions, patterns, lessons) |
| `/spek.map` | During planning | Generate visual code map + impact analysis |
| `/spek.lessons` | During conclude | Enhanced lesson extraction with guided prompts |

**Placement in Workflow:**
- `/spek.context` — Optional enhancement to `/spek.prepare` (load vault context)
- `/spek.map` — Optional enhancement to `/spek.plan` phases (visualize code structure)
- `/spek.lessons` — Optional enhancement to `/spek.conclude` Step 3 (generate richer lessons)

### Skill Reuse Patterns

**Single Feature Workflow:**
```
/spek.prepare → /spek.plan --phase=specify → /spek.plan --phase=plan 
→ /spek.implement → /spek.conclude
```

**Multi-Session Feature (resume):**
```
Session 1: /spek.prepare → /spek.plan (both phases) → /spek.implement (partial)
[Interrupted]
Session 2: /spek.prepare → /spek.implement (continue) → /spek.conclude
```

**Multi-Developer Coordination:**
```
Dev A: /spek.prepare → /spek.plan --phase=specify → [Review checkpoint]
Dev B: /spek.plan --phase=plan → /spek.implement → /spek.conclude
       (Uses spec from Dev A; Dev A reviews plan before implementing)
```

**With Enrichment Layers:**
```
/spek.prepare 
→ /spek.context (load vault)
→ /spek.plan --phase=specify (enrich with patterns/decisions from context)
→ /spek.map (visualize code impact)
→ /spek.plan --phase=plan
→ /spek.implement
→ /spek.lessons (enhanced lesson generation)
→ /spek.conclude
```

---

## The End Product: What Exists When Fully Implemented

When you complete one feature cycle with Spekificity, **the system produces:**

### In Your Git Repository

```
project/
├─ src/
│  └─ [NEW FEATURE CODE]
│  └─ [TESTS: unit + integration + e2e]
│  └─ [DOCUMENTATION: docstrings, examples]
│
└─ wiki/
   ├─ specs/
   │  └─ [FEATURE SPEC: NNN-feature-name.md]
   │
   └─ vault/
      ├─ Architectural decisions recorded
      ├─ Patterns discovered and indexed
      └─ lessons/
         └─ [LESSONS LEARNED: YYYY-MM-DD-feature-name-topic.md]
            └─ [What worked, what didn't, why, for future reference]
```

### In Obsidian Vault (All Persistent Memory)

```
vault/
├─ user/
│  └─ preferences.md
│     └─ User preferences, projects, tools
│
├─ session/
│  ├─ [feature-name]-state.yaml
│  │  └─ Feature state, progress, decisions made
│  │
│  └─ decisions.yaml
│     └─ Current session decisions
│
├─ repo/
│  ├─ intention.md
│  │  └─ Project vision, tenets, constraints
│  │
│  ├─ patterns.md
│  │  └─ Reusable patterns indexed by feature/tool
│  │
│  ├─ decision.md
│  │  └─ Architectural decisions recorded
│  │
│  └─ architectural-decisions.md
│     └─ Compressed version for reuse across projects
│
└─ lessons/
   └─ [YYYY-MM-DD-feature-name-topic.md]
      └─ Lessons learned for future reference
```

### In CodeGraph

```
codegraph.db (updated)
├─ All symbols indexed
├─ All references mapped
├─ Impact chains calculated
└─ Ready for next query in < 100ms
```

### In Vault Metadata

```
wiki/vault/
├─ Current feature state (COMPLETED)
├─ All decisions documented
├─ All patterns captured
├─ Session lessons stored
└─ Graph fresh and ready
```

**Total Outcome:** Clean code + passing tests + architectural knowledge captured + lessons indexed + next developer can read vault and understand what happened and why.

---

## How It Operates: Typical Feature Cycle

### Step-by-Step: Building a User Authentication Feature (Example)

#### Prepare Workspace

**Command:** `/spek.prepare`

```
✓ Git working tree clean
✓ Vault synced from origin
✓ CodeGraph refreshed
✓ Session context loaded
READY: Workspace prepared for feature development
```

**What happened:**
- Git verified clean (no uncommitted work)
- Vault pulled (latest specs/decisions/lessons from wiki/vault/)
├─ CodeGraph queried for affected files
- Session memory loaded (decisions, patterns from wiki/vault/)
- Feature state file created

#### Specify Feature

**Command:** `/spek.plan --phase=specify --feature="user-auth-api"`

```
SPEC GENERATION
├─ Feature Intent: "POST /auth/login endpoint validates credentials, returns JWT"
├─ Query CodeGraph:
│  ├─ Found existing: auth/models.py (user model)
│  ├─ Found existing: auth/tokens.py (jwt utilities)
│  └─ Impact: 3 existing files touch auth system
│
├─ Enrich with layers:
│  ├─ Success Criteria:
│  │  - ✓ POST /auth/login accepts email + password
│  │  - ✓ Valid credentials return JWT token
│  │  - ✓ Invalid credentials return 401
│  │  - ✓ JWT validates on protected endpoints
│  │  - ✓ 95%+ test coverage on new code
│  │
│  ├─ Assumptions:
│  │  - User model exists (✓ verified in CodeGraph)
│  │  - JWT utilities exist (✓ verified in CodeGraph)
│  │  - Passwords already hashed (✓ verified in auth/models.py)
│  │
│  ├─ Risk Assessment:
│  │  - 🔴 HIGH: SQL injection if not parameterized (mitigation: ORM only)
│  │  - 🟡 MEDIUM: Token expiry not configurable (mitigation: add ENV var)
│  │  - 🟢 LOW: Rate limiting not implemented (mitigation: future feature)
│  │
│  └─ Resource Estimate:
│     - Complexity: Medium (3 files touched, 1 existing pattern reused)
│     - Tokens: ~2,000-3,000 for full cycle
│     - Time: 1-2 hours
│
└─ Output: wiki/vault/specs/150-user-auth-api.md (CREATED)
   └─ Ready for planning phase
```

**What was produced:**
- `/wiki/specs/150-user-auth-api.md` — Complete spec with enrichment layers
- Linked to existing patterns (JWT handling, error handling)
- Cross-referenced with existing decisions (why we use JWT not sessions)
- Risk assessment documented
- Success criteria crystal clear

#### Create Plan

**Command:** `/spek.plan --phase=plan`

```
TASK BREAKDOWN
├─ Spec parsed: 150-user-auth-api.md
├─ CodeGraph queried: 3 files affected, 12 functions touched
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

#### Execute Implementation

**Command:** `/spek.implement --task=1 --task=2 --task=3 --task=4`

For each task:

```
IMPLEMENTING TASK 1: Add login route handler

INPUT:
├─ Task spec (150-user-auth-api.md + 151-user-auth-plan.md)
├─ CodeGraph results (where to add code, what exists, what to reuse)
├─ Existing patterns (JWT handling, error responses)
└─ Session memory (decisions from previous features)

EXECUTION:
├─ Agent reads task spec
├─ Agent queries CodeGraph for:
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

#### Archive & Close

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
│  - CodeGraph impact analysis reduced manual code review effort
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
└─ Output: wiki/vault/lessons/2026-05-20-user-auth-api-implementation.md (CREATED)

Step 4-5: Update Vault
├─ wiki/vault/decision.md (append new architectural decisions)
├─ wiki/vault/patterns.md (log pattern usage + frequency)
└─ Feature marked as COMPLETED

Step 6-7: Sync Repo Memory
├─ vault/repo/architectural-decisions.md (updated)
├─ vault/repo/patterns-index.md (updated)
└─ Ready for next project to use

Step 8: Refresh CodeGraph
├─ Scan new code (auth/routes.py, tests/)
├─ Update index with new functions/classes
└─ Graph now includes login handler, tests

Step 9: Archive Feature State
├─ Move vault/session/current-feature.md to wiki/vault/archive/
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
- CodeGraph updated and ready
- Session memory archived
- Repository ready for next feature

---

## The Value: What You Get

### For Individual Developers

| Benefit | How Spekificity Enables It |
|---------|---------------------------|
| **Build faster** | Specs clarify intent upfront; CodeGraph prevents hand-tracing code |
| **Make better decisions** | Decisions logged with rationale; future code can reference why choices were made |
| **Reduce debugging** | Enrichment layers (assumptions, risk assessment) catch issues early |
| **Learn from the past** | Lessons captured in vault; patterns indexed for reuse |
| **Work offline** | Session memory persists; can resume without rebuilding context |

### For Teams

| Benefit | How Spekificity Enables It |
|---------|---------------------------|
| **Async coordination** | Specs are artifacts that can be reviewed, debated, approved before code |
| **Prevent conflicts** | CodeGraph shows what code touches what; explicit dependency tracking prevents collisions |
| **Share knowledge** | Vault is Git-backed; decisions, patterns, lessons visible to entire team |
| **Reduce ramp-up time** | New developer reads vault, understands what's been tried and why |
| **Replicate success** | Patterns are documented; next feature can reference and reuse |

### For Long-Term Projects

| Benefit | How Spekificity Enables It |
|---------|---------------------------|
| **Sustainability** | Knowledge persists; no "only Bob understands this" |
| **Auditability** | Every decision logged with date, feature, rationale |
| **Pattern evolution** | Patterns tracked over time; can see what's working, what's not |
| **Context preservation** | Session interruptions don't lose context; memory survives |

---

## Comparison: Without vs. With Spekificity

### Feature Development Timeline: User Authentication

#### WITHOUT Spekificity

```
Day 1 (Morning):
├─ Developer starts feature
├─ Searches codebase for existing auth code (15 min)
├─ Reads 5 files to understand structure
├─ Misses JWT utilities in separate module
└─ Starts coding without spec

Day 1 (Afternoon):
├─ Code written without success criteria
├─ Tests incomplete; coverage 60%
├─ Realizes JWT utilities exist; refactors
└─ Lost 2 hours

Day 2 (Morning):
├─ Code review: reviewer asks "why JWT not sessions?"
├─ Developer has no documented reason
├─ Meeting called; decision remade
└─ Lost 1 hour

Day 2 (Afternoon):
├─ Tests passing, code merged
├─ No lessons documented
├─ Same patterns reinvented on next feature
└─ Total: 2.5 days, 8,000+ tokens, no knowledge captured

KNOWLEDGE DEBT: Next time, developer repeats same analysis
```

#### WITH Spekificity

```
Day 1 (Morning - 30 min):
├─ /spek.prepare (CodeGraph shows JWT utilities exist)
├─ /spek.plan --phase=specify (spec written with enrichment)
├─ Success criteria clear, assumptions documented
├─ Spec reviewed + approved by team
└─ Ready to implement

Day 1 (Afternoon - 2 hours):
├─ /spek.plan --phase=plan (tasks broken down, dependencies checked)
├─ /spek.implement (code written per task spec)
├─ Tests written (95%+ coverage)
├─ Decisions logged: "JWT chosen for statelessness"
└─ /spek.conclude (lessons captured, patterns indexed)

TOTAL: 2.5 hours active work, 3,200 tokens, knowledge captured

KNOWLEDGE GAIN: Vault now contains:
├─ Spec (for next similar feature)
├─ Decisions (why JWT)
├─ Patterns (JWT generation, error responses)
└─ Lessons (what worked, edge cases found)

NEXT TIME: Developer reads vault, reuses pattern, saves 1.5 hours
```

---

## Success Criteria: How to Know It's Working

Spekificity is working when:

✅ **Specs exist before code** — Developers write spec first, not as documentation after  
✅ **CodeGraph answers code questions** — "Where is X used?" answered via pre-indexed queries, not manual scanning  
✅ **Decisions are documented** — Vault grows; decisions logged with rationale  
✅ **Patterns are reused** — Each feature references 2-3 patterns from vault  
✅ **Lessons are captured** — Each feature adds to lessons archive  
✅ **Context survives sessions** — Developer can close editor, come back tomorrow, resume without rebuilding context  
✅ **Token usage is predictable** — Feature tokens estimated accurately; no surprises  
✅ **Onboarding is faster** — New developer can read vault and understand project in 1 hour  

---

## Implementation Status

**When Fully Implemented, Spekificity Provides:**

- ✅ 5-phase workflow (Prepare → Specify → Plan → Implement → Close)
- ✅ CodeGraph integration (pre-indexed queries, multiple languages)
- ✅ SpecKit orchestration (deterministic pipeline)
- ✅ Obsidian vault (Git-backed knowledge store)
- ✅ Memory architecture (3-layer persistence)
- ✅ Caveman compression (75-90% token reduction)
- ✅ Lesson extraction (automatic from execution trace)
- ✅ Pattern indexing (reusable solutions tracked)
- ✅ Decision logging (archived with rationale)
- ✅ Multi-developer coordination (async + sync workflows)
- ✅ Session continuation (resume across interruptions)
- ✅ Test strategy (135+ tests across 3-layer pyramid)

**Ready to Use:**
- ✅ All 41 specifications (010-189 phase-based sequencing)
- ✅ Full wiki documentation (vision, intention, architecture, workflow)
- ✅ Quick start guide (30-min first feature walkthrough)
- ✅ Skill framework (`/spek.*` commands)

---

## Quick Links

| Document | Read For |
|----------|----------|
| [wiki/vision.md](../vision.md) | Why Spekificity exists (problems + philosophy) |
| [wiki/intention.md](../intention.md) | Core principles and design tenets |
| [wiki/architecture.md](../architecture.md) | Technical architecture and components |
| [wiki/workflow.md](../workflow.md) | 5-phase workflow details (reference during development) |
| [wiki/quickstart.md](../quickstart.md) | Hands-on walkthrough of first feature (30 min tutorial) |

---

**Status:** Complete. End product fully specified. Spekificity ready to enable rapid, deterministic, token-efficient AI agent development.
