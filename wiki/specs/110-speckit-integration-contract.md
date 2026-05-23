---
title: "SpecKit Integration Contract"
status: "SPECIFICATION"
version: "1.0.0-alpha.1"
date: "2026-05-18"
---

# extracted spec — SpecKit Integration Contract

**Status:** SPECIFICATION (2026-05-18) | **Version:** 1.0.0-alpha.1 (2026-05-20)  
**Feature:** spekificity feature 003 — Full Workflow CLI  
**Related:** [Spekificity Workflow](../workflow.md), [Memory Architecture](030-memory-architecture.md)

---

## Overview

This contract defines how **spekificity** enriches the canonical **SpecKit** workflow. SpecKit is responsible for spec-driven feature development (constitution → specify → plan → tasks → implement). Spekificity adds three layers:

1. **Context Layer** — Load vault context before starting feature (`/spek.context`)
2. **Workflow Orchestration Layer** — Use `/spek.plan` to orchestrate specify/clarify/plan/analyze/remediate/tasks, then `/spek.implement` for execution
3. **Conclusion Layer** — Extract lessons and update vault after feature end (`/spek.conclude`)

The contract clarifies:
- **Who owns what** (speckit vs. spekificity responsibilities)
- **Integration pattern** (workflow orchestration plus targeted execution wrapper)
- **Data flow** (artifacts, context, outputs)
- **Error handling** (validation, retry, fallback)
- **Configuration** (where settings live, precedence)

---

## SpecKit Canonical Workflow

From [workflow.md](../workflow.md), the canonical feature development flow is:

```
constitution
    ↓
specify
    ↓
clarify? (optional, human Q&A)
    ↓
plan
    ↓
tasks
    ↓
analyze? (optional, cross-artifact consistency)
    ↓
remediate? (optional, in-place fixes)
    ↓
implement
```

**Key SpecKit Principles:**
- **Declarative input** — Human writes in natural language
- **Progressive refinement** — Each step builds on prior outputs
- **Optional gates** — clarify, analyze, remediate are non-blocking
- **File-based artifacts** — spec.md, plan.md, tasks.md, constitutional constraints, traceable task IDs
- **Remediation in-place** — No re-entry loop; fixes are direct edits

## Success Criteria

- ✅ SpecKit responsibilities clear (spec generation, model selection, constitution precedence)
- ✅ Spekificity responsibilities clear (context injection, validation, memory update)
- ✅ Integration seamless (user doesn't know workflows are enriched)
- ✅ Data flow correct (context flows in, artifacts flow out, memory updated)
- ✅ Error handling consistent (validation errors caught, fallbacks work)
- ✅ Configuration clear (settings location, precedence rules documented)
- ✅ Contract testable (success conditions measurable)
- **Optional gates** — clarify, analyze, remediate are non-blocking
- **File-based artifacts** — spec.md, plan.md, tasks.md, constitution.md
- **Remediation in-place** — No re-entry loop; fixes are direct edits
- **Output:** spec.md, plan.md, tasks.md, constitutional constraints, traceable task IDs

---

## Spekificity Integration Layers

### Layer 1: Context Layer (`/spek.context`)

**Purpose:** Load all contextual knowledge before starting feature work

**Input:**
- Session state (first time? resume?)
- Optional feature name (for specific query)

**Process:**
1. Read vault (decisions, patterns, recent lessons)
2. Read repo memory (compressed context)
3. Query code graph (vault/graph/nodes.jsonl)
4. Summarize in caveman format
5. Write to vault/session/

**Output:**
- vault/session/ (3-5K tokens)
- Context loaded into agent context
- User-visible summary of relevant lessons/decisions/patterns

**When invoked:**
- **Mandatory at session start** (before `/spek.prepare`)
- **Optional during feature** (if context refresh needed)

**Dependencies:**
- Vault (vault/decision.md, vault/patterns.md, vault/lessons/)
- Repo memory (vault/repo/*)
- Code graph (vault/graph/nodes.jsonl)

---

### Layer 2: Workflow Orchestration Layer

#### 2a. Feature Preparation (`/spek.prepare`)

**Purpose:** Prepare workspace for feature work (not a SpecKit command)

**Invoked:** At feature start, after `/spek.context`

**Owned by:** Spekificity (no SpecKit equivalent)

**Steps:**
1. Verify git state (clean working dir, feature branch)
2. Activate caveman mode (lite)
3. Load vault context via `/spek.context`
4. Verify code graph freshness (last sync < 1hr?)
5. Report ready state

**Output:**
- vault/session/ (created)
- Confirmed working directory state
- Verified code graph freshness
- User-visible readiness report

---

#### 2b. Automated Specify Phase (`/spek.plan`)

**Pattern:** Internal phase inside `/spek.plan`, wrapping `/speckit.specify`

```
/spek.plan
    └── specify phase
├── Load current context (vault/session/)
├── Inject context into speckit prompt (decisions, patterns, lessons)
├── Run /speckit.specify
│   ├── Read feature description
│   ├── Read constitution.md (or create if missing)
│   ├── Generate spec.md (claude models configured in .specify/)
│   └── Output: spec.md
├── Validate output consistency
└── Update vault/session/
```

**Responsibility Division:**
- **SpecKit owns:** Spec generation logic, constitution precedence, model selection
- **Spekificity adds:** Context injection, consistency validation, memory update

**Input:**
- Feature description (natural language)
- Optional: specific patterns to follow (injected from vault)

**Output:**
- spec.md (created or updated)
- vault/session/ (updated)

**Error Handling:**
- If spec is empty or malformed → Retry with clarification
- If spec violates recent decisions → Flag and ask for confirm
- If spec is missing sections → Warn but proceed (clarify can fix)

---

#### 2c. Automated Plan Phase (`/spek.plan`)

**Pattern:** Internal phase inside `/spek.plan`, wrapping `/speckit.plan`

```
/spek.plan
    └── plan phase
├── Load current context (vault/session/)
├── Read spec.md (validate freshness)
├── Inject context into speckit prompt
│   ├── Recent decisions (vault/decision.md)
│   ├── Proven patterns (vault/patterns.md)
│   └── Code graph (vault/graph/nodes.jsonl — affected symbols, files)
├── Run /speckit.plan
│   ├── Read spec.md
│   ├── Read constitution.md (if not already read)
│   ├── Generate plan.md (with design, architecture, key components)
│   └── Output: plan.md
├── Validate output (design clarity, task granularity, feasibility)
└── Update vault/session/
```

**Responsibility Division:**
- **SpecKit owns:** Plan generation, design rationale, task breakdown
- **Spekificity adds:** Context injection, architectural alignment validation, code graph integration, memory update

**Input:**
- spec.md (must exist and be recent)
- Current context (decisions, patterns, code graph)

**Output:**
- plan.md (created or updated)
- vault/session/ (updated)

**Error Handling:**
- If plan is too vague → Suggest more detailed design
- If plan contradicts recent decisions → Flag for confirmation
- If plan references non-existent code → Validate with code graph

---

#### 2d. Tasks Phase (`/speckit.tasks` inside `/spek.plan`)

**Pattern:** Direct SpecKit command (no spekificity wrapper)

`/spek.plan` calls `/speckit.tasks` directly because:
- Task generation is fully SpecKit's responsibility
- No architectural enrichment needed (context is already in plan.md)
- Direct invocation simpler and more transparent

**Process:**
```
/speckit.tasks
├── Read spec.md + plan.md
├── Generate tasks.md with:
│   ├── Ordered dependency graph
│   ├── Individual task IDs
│   ├── Acceptance criteria
│   └── Estimated effort
└── Output: tasks.md
```

**When invoked:**
- After plan.md is finalized
- If spec/plan change → regenerate tasks

---

#### 2e. Optional: Analyze & Remediate (SpecKit canonical)

**Analyze** (`/speckit.analyze`):
- Cross-artifact consistency check (spec → plan → tasks)
- Optional, non-blocking
- Outputs analysis report (no file changes)

**Remediate** (`/speckit.remediate`):
- In-place fixes to spec/plan/tasks based on analysis
- Optional, non-blocking
- Updates files directly (no re-entry loop)

**Spekificity role:** Read-only; no wrapper. If user wants to run analyze/remediate, they invoke directly.

---

#### 2f. Enriched Implement (`/spek.implement`)

**Pattern:** Decorator wrapper around `/speckit.implement`

```
/spek.implement
├── Load current context (vault/session/)
├── Read tasks.md (validate completeness)
├── Run /speckit.implement
│   ├── Execute all tasks (task 1, 2, 3, ...)
│   ├── Generate execution trace
│   └── Output: code changes, execution log
├── Collect artifacts
│   ├── code changes
│   ├── execution trace
│   ├── errors/warnings
│   └── completion status
└── Update vault/session/
```

**Responsibility Division:**
- **SpecKit owns:** Task execution, model orchestration, code generation
- **Spekificity adds:** Context awareness during execution, artifact collection, memory update

**Input:**
- tasks.md (must exist and be complete)
- Current context

**Output:**
- Code changes (files modified in workspace)
- Execution trace (log of what ran, what succeeded/failed)
- vault/session/ (marked as completed or partially completed)

**Error Handling:**
- If task fails → Log error, continue (partial completion is valid)
- If code has syntax errors → Report but don't block (developer will fix)
- If execution trace is incomplete → Warn and archive as-is

---

### Layer 3: Conclusion Layer (`/spek.conclude`)

**Purpose:** Extract lessons and update vault after feature end

**Owned by:** Spekificity (no SpecKit equivalent)

**Invoked:** At feature end, after `/spek.implement` (whether completed, partial, or abandoned)

**Steps:**
1. Collect artifacts (spec.md, plan.md, tasks.md, execution trace)
2. Activate caveman mode (configurable: lite, full, or ultra)
3. Generate lessons
   - Create vault/lessons/<date>-<feature>-<name>.md
   - Extract What/How/Tasks/Decisions/Patterns/Lessons/Metrics/References
   - Compress in caveman format
4. Update vault
   - Append new decisions → vault/decision.md
   - Refine patterns → vault/patterns.md
5. Incremental code graph sync (`/spek.map`)
6. Sync recent items to repo memory
7. Archive session memory
8. Report completion

**Output:**
- vault/lessons/<date>-<feature>-<name>.md (archived)
- vault/decision.md (updated)
- vault/patterns.md (updated)
- vault/repo/architectural-decisions.md (synced)
- vault/repo/patterns-index.md (synced)
- Code graph updated (vault/graph/nodes.jsonl)

**Dependencies:**
- All artifacts from `/spek.implement`
- Vault structure
- Caveman mode for compression

---

### Layer 4: Orchestration (`/spek.plan`)

**Purpose:** Run pre-implementation workflow in sequence, then hand off to `/spek.implement`

**Pattern:** Sequential invocation with error handling

```
/spek.plan [--feature-name="..."] [--skip-clarify] [--skip-analyze]
├── /spek.context (load context)
├── /spek.prepare (verify workspace)
├── /speckit.specify (generate spec)
├── /speckit.clarify (optional, if --skip-clarify not set)
├── /speckit.plan (generate plan)
├── /speckit.analyze (optional, if --skip-analyze not set)
├── remediate in-place if needed
└── /speckit.tasks (generate tasks)
```

**When to use:**
- Feature is straightforward and well-understood
- No major blockers expected
- Want one-shot automation

**When NOT to use:**
- Feature is complex or ambiguous → Run manually step-by-step
- Want human review gates → Run manually
- Need to tweak spec/plan mid-flow → Run manually

---

## Integration Pattern: Orchestrator + Targeted Wrapper

Spekificity uses an orchestration pattern for `/spek.plan` and a targeted execution wrapper for `/spek.implement`:

```
/spek.plan
├── Pre-execution
│   ├── Load context
│   ├── Validate inputs
│   ├── Inject enrichment
├── Core workflow execution
│   ├── Call /speckit.specify / clarify / plan / analyze / tasks
│   └── Capture artifacts + findings
└── Post-execution
    ├── Validate outputs
    ├── Update memory
    └── Hand off to /spek.implement
```

**Why decorator, not hooks?**
- Cleaner separation of concerns
- No modification of SpecKit internals
- Easy to debug (trace each layer)
- Works with any SpecKit version (interface stable)
- Explicit data flow (no hidden dependencies)

**Why not pre/post hooks?**
- Would require SpecKit to implement hook system (out of scope)
- Decorator is framework-agnostic
- Easier to document and test

---

## Division of Responsibility

| Concern | SpecKit Owns | Spekificity Adds | Notes |
|---------|--------------|------------------|-------|
| **Spec generation** | ✓ Core logic | ✓ Context injection | Decisions/patterns guide options |
| **Plan generation** | ✓ Core logic | ✓ Context injection | Architecture alignment check |
| **Task generation** | ✓ Full ownership | — | No enrichment needed |
| **Implementation** | ✓ Core logic | ✓ Artifact collection | Execution tracing, error reporting |
| **Context loading** | — | ✓ Full ownership | Pre-session, mid-feature refresh |
| **Workspace prep** | — | ✓ Full ownership | Git state, graph freshness |
| **Lessons extraction** | — | ✓ Full ownership | Template, compression, vault update |
| **Vault management** | — | ✓ Full ownership | Decisions, patterns, lessons |
| **Memory management** | — | ✓ Full ownership | Session, repo, vault sync |
| **Code graph** | — | ✓ Full ownership | Index creation, incremental sync |
| **Token compression** | — | ✓ Full ownership | Caveman mode activation |
| **Orchestration** | — | ✓ Optional | `/spek.plan` command |

---

## Data Flow Through Complete Lifecycle

### Session Start
```
User invokes: /spek.context
├── Reads vault/decision.md, vault/patterns.md, vault/lessons/ (last 3-5)
├── Reads vault/repo/architectural-decisions.md, vault/repo/patterns-index.md
├── Queries vault/graph/nodes.jsonl
├── Compresses with caveman (lite)
└── Writes vault/session/
```

### Feature Start
```
User invokes: /spek.prepare
├── Verifies git state
├── Activates caveman mode
├── Calls /spek.context (if not already done)
├── Verifies code graph freshness
├── Creates vault/session/
└── Reports ready state
```

### Spec Generation
```
User invokes: /spek.plan [feature description]
├── Enter specify phase
├── Reads vault/session/
├── Injects context into speckit prompt
├── Calls /speckit.specify
│   ├── Reads constitution.md (if exists)
│   ├── Calls claude-model (via .specify/config)
│   └── Generates spec.md
├── Validates spec consistency
├── Updates vault/session/
└── Reports spec created
```

### Plan Generation
```
User remains inside /spek.plan
├── Enter plan phase
├── Reads vault/session/
├── Reads spec.md (validates recency)
├── Queries vault/graph/nodes.jsonl (affected code)
├── Injects context + code graph into speckit prompt
├── Calls /speckit.plan
│   ├── Reads spec.md + constitution.md
│   ├── Calls claude-model (via .specify/config)
│   └── Generates plan.md
├── Validates plan vs. recent decisions
├── Updates vault/session/
└── Reports plan created
```

### Task Generation
```
User invokes: /speckit.tasks
├── Reads spec.md + plan.md
├── Generates tasks.md with:
│   ├── Ordered task list
│   ├── Task IDs
│   ├── Acceptance criteria
│   └── Dependencies
└── Reports tasks generated
```

### Implementation
```
User invokes: /spek.implement
├── Reads vault/session/
├── Reads tasks.md (validates completeness)
├── Calls /speckit.implement
│   ├── Executes each task (sequentially or parallel)
│   ├── Generates code changes
│   └── Captures execution trace
├── Collects artifacts (changes, trace, errors)
├── Updates vault/session/ (mark as done/partial)
└── Reports implementation status
```

### Feature End
```
User invokes: /spek.conclude
├── Collects all artifacts
│   ├── spec.md, plan.md, tasks.md
│   ├── execution trace, code changes
│   └── vault/session/
├── Activates caveman mode (full or ultra)
├── Generates vault/lessons/<date>-<feature>-<name>.md
├── Updates vault
│   ├── Appends decisions → vault/decision.md
│   ├── Refines patterns → vault/patterns.md
├── Syncs repo memory
│   ├── Compress recent decisions → vault/repo/architectural-decisions.md
│   ├── Update patterns index → vault/repo/patterns-index.md
├── Runs /spek.map (incremental code graph sync)
├── Archives vault/session/
└── Reports feature complete
```

---

## Error Handling & Validation

### Validation Layers

**Input validation** (before core execution):
- Spec exists and is well-formed? (for plan, tasks, implement)
- Plan exists and has design section? (for tasks, implement)
- Tasks exist and are complete? (for implement)
- Git workspace is clean? (for implement)

**Output validation** (after core execution):
- Spec matches constitution constraints?
- Plan has clear architecture and design decisions?
- Tasks are ordered and have clear dependencies?
- Implementation produced code changes?

**Cross-artifact validation**:
- Spec, plan, tasks form coherent story?
- No contradictions between layers?
- All assumptions documented?

### Retry & Fallback

**If spec generation fails:**
1. Log error
2. Suggest `/speckit.clarify` to refine inputs
3. Retry specify phase inside `/spek.plan` with clarifications

**If plan generation fails:**
1. Log error
2. Check if spec is too vague → suggest clarify
3. Check if architecture is infeasible → suggest spec revision
4. Retry plan phase inside `/spek.plan` with adjustments

**If implementation fails:**
1. Log failed task(s)
2. Continue with remaining tasks (partial completion valid)
3. Report summary of successes/failures
4. Proceed to `/spek.conclude` anyway (lessons even from partial work)

**If vault update fails:**
1. Log error
2. Archive artifacts for manual inspection
3. Report blockers and recovery steps

### Fallback Patterns

- If caveman compression fails → Use uncompressed format
- If code graph sync fails → Use last-known state
- If vault read fails → Use repo memory fallback
- If file write fails → Report error, don't proceed

---

## Configuration Management

### SpecKit Configuration (in `.specify/`)

SpecKit's own config files:

```
.specify/
├── config.yaml           # Model, temperature, max_tokens
├── constitution.md       # Project constraints (optional)
├── .speckit-templates/   # Custom templates for spec/plan/tasks (optional)
└── .speckit-hooks/       # Pre/post-processing hooks (optional, if supported)
```

**Controlled by:** SpecKit itself; spekificity reads but does not modify

**Precedence:**
1. `.specify/config.yaml` (highest priority)
2. SpecKit defaults
3. Copilot defaults (lowest)

### Spekificity Configuration (in `.spekificity/`)

Spekificity-specific settings:

```
.spekificity/
├── config.yaml           # Caveman mode settings, graph thresholds, vault paths
├── skills/               # Skill definitions (/spek.context, /spek.prepare, etc.)
├── guides/               # User guides, quickstart
└── bin/                  # Setup and status scripts
```

**Controlled by:** Spekificity; user can customize

**Precedence:**
1. `.spekificity/config.yaml` (highest priority)
2. Spekificity defaults
3. Vault settings (if defined)

### Memory Configuration (in `vault/graph/`)

Memory paths and graph config:

```
vault/
├── graph/
│   ├── config.json       # Graph generation settings (paths, granularity, refresh policy)
│   ├── nodes.jsonl       # Merged code + doc nodes
	│   ├── nodes-code.jsonl  # Code symbols (from CodeGraph)
│   └── nodes-docs.jsonl  # Doc headings (from Obsidian export)
└── decision.md, patterns.md, ...
```

**Controlled by:** Spekificity (`/spek.map` updates this)

**Precedence:**
1. `vault/graph/config.json` (highest)
2. Vault defaults
3. System defaults

---

## Success Criteria

### Criteria for Contract Fulfillment

✅ **Clear responsibility division:** Each concern is owned by exactly one actor (SpecKit or Spekificity)

✅ **Workflow pattern used:** `/spek.plan` owns orchestration; `/spek.implement` owns execution

✅ **Context flows through layers:** Context injected at each step, updated in session memory

✅ **Error handling documented:** Each command has defined retry, fallback, and error reporting

✅ **Data flow is explicit:** All intermediate artifacts documented (spec.md → plan.md → tasks.md → code)

✅ **Configuration precedence clear:** If ambiguity arises, we know which config wins

✅ **No tight coupling:** Spekificity does not depend on SpecKit internals; works with any SpecKit version

✅ **Integration points identified:** 9 clear touch points (specify, plan, implement, context, prepare, post, memory, graph, artifacts)

### Integration Test Checklist

1. ✅ `/spek.context` loads and summarizes context (caveman format, 3-5K tokens)
2. ✅ `/spek.prepare` verifies git state and graph freshness
3. ✅ `/spek.plan` specify phase injects context, calls speckit, validates output
4. ✅ `/spek.plan` plan phase injects context + code graph, calls speckit, validates output
5. ✅ `/speckit.tasks` generates tasks without spekificity wrapper
6. ✅ `/spek.implement` calls speckit, collects artifacts, updates memory
7. ✅ `/spek.conclude` generates lessons, updates vault, syncs to repo memory
8. ✅ `/spek.plan` orchestrates entire flow sequentially
9. ✅ Error handling works: retry, fallback, partial completion, recovery

---

## References

**Related specs:**
- [Spekificity Workflow](../workflow.md)
- [extracted spec Code and Document Maps](code-and-document-maps.md)
- [extracted spec Memory Architecture](memory-architecture.md)

**SpecKit canonical documentation:**
- [SpecKit GitHub](https://github.com/github/spec-kit)
- [Workflow](../workflow.md#canonical-workflow)

**Spekificity skill definitions:**
- [/spek.context spec](context-layer.md)
- [/spek.prepare spec](prepare-command.md)
- [/spek.conclude spec](conclude-command.md)

**Architectural decisions:**
- Decorator pattern over hook system (this spec)
- Two-tool system: Obsidian (knowledge) + CodeGraph (code analysis) (extracted spec)
- Three-layer memory: Vault + Repo + Session (extracted spec)

