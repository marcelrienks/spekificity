# Spekificity Architecture

**See also:** [vision.md](vision.md) (philosophy) → [intention.md](intention.md) (principles) → [workflow.md](workflow.md) (process)

**Note:** This document covers technical architecture only. For philosophical foundations and design principles, see [vision.md](vision.md) and [intention.md](intention.md).

---

## Overview

Spekificity is a **specification-driven agent development framework** that ties project knowledge (Obsidian vault), code analysis (CodeGraph), workflow automation (SpecKit), and skill execution (Agent Skills) into a coherent pipeline.

**Core Goal:** Enable rapid, deterministic feature development with minimal token overhead and maximum context reuse.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SPEKIFICITY SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │  wiki/Vault      │   │   CodeGraph MCP  │                │
│  │  (Knowledge)     │   │   (Code Intel)   │                │
│  └────────┬─────────┘   └────────┬─────────┘                │
│           │                      │                          │
│           └──────────┬───────────┘                          │
│                      │                                      │
│              ┌───────▼────────┐                            │
│              │   Context      │                            │
│              │   Layer        │                            │
│              └───────┬────────┘                            │
│                      │                                      │
│           ┌──────────┴──────────┐                          │
│           │                     │                          │
│     ┌─────▼──────┐       ┌─────▼──────┐                   │
│     │  SpecKit   │       │  Agent     │                   │
│     │  Workflow  │       │  Skills    │                   │
│     │  Engine    │       │  (/spek.*) │                   │
│     └─────┬──────┘       └──────┬─────┘                   │
│           │                     │                          │
│           └──────────┬──────────┘                          │
│                      │                                      │
│              ┌───────▼────────┐                            │
│              │   Feature Out  │                            │
│              │   (Code + Docs)│                            │
│              └────────────────┘                            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
START FEATURE
    │
    ├─ /spek.prepare ─────────────► Workspace Ready
    │  (Git state, wiki/vault fresh, graph synced)
    │
    ├─ /spek.automate ────────────────┐
    │  (Orchestrate SpecKit)           │
    │                                  │
    │  ├─ /speckit.specify ──────────► Spec Created
    │  │  (+ enrichment layer)         (Success Criteria,
    │  │                                Assumptions, etc.)
    │  │
    │  ├─ /speckit.plan ──────────────► Plan Created
    │  │  (+ enrichment layer)         (Tasks, Deps,
    │  │                                Resource Est.)
    │  │
    │  └─ /speckit.analyze ──────────► Readiness Check
    │     (Validation, Risk Assessment)
    │
    ├─ /spek.implement ───────────────► Features Coded
    │  (Per-task execution)            (Tests, Docs)
    │
    ├─ /spek.post ────────────────────► Outcomes Archived
    │  (Archive, Lessons, Refresh)     (wiki/Vault + Graph Updated)
    │
    ├─ /spek.lessons ─────────────────► Lessons Extracted
    │  (Structured capture)            (wiki/Vault + Session Updated)
    │
    END FEATURE
```

---

## Component Responsibilities

### Obsidian Vault

**Persistent knowledge base for project context.**

- Stores specifications, plans, decisions, and lessons learned
- Enables human reasoning across sessions (spec remains stable across multiple agent invocations)
- Provides enrichment layers (Success Criteria, Assumptions, Risk Assessment, Metrics)
- Syncs to Git for version control and collaboration

### CodeGraph MCP

**Real-time code analysis and impact detection.**

- Indexes all project code (symbols, definitions, call chains)
- Provides impact analysis (who calls this? what does it affect?)
- Auto-syncs on file change (no manual refresh)
- Serves agent queries without file scanning (token-efficient)

### SpecKit Workflow Engine

**Specification → Plan → Tasks orchestration.**

- Receives spec document from wiki/vault
- Generates execution plan with dependencies and task breakdown
- Routes tasks to agent for implementation
- Collects analysis (risk, metrics, dependencies)

### Agent Skills Layer (`/spek.*` commands)

**Deterministic, repeatable workflow steps.**

- `spek.prepare`: Pre-flight checks (workspace state, graph freshness, vault ready)
- `spek.automate`: Invoke SpecKit pipeline (specify → plan → analyze)
- `spek.implement`: Execute approved tasks with full context
- `spek.post`: Archive outcomes, update vault, refresh graph
- `spek.lessons`: Structured lesson extraction (run standalone or post-feature)
- `spek.context`: Load session context (vault, repo memory, graph state)
- `spek.map`: Build/refresh code graph

---

## Layering: User → Skills → SpecKit → Core

```
┌──────────────────────────────────────────────────┐
│  USER INTENTION                                  │
│  (I want to build feature X)                     │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  SKILLS LAYER: /spek.* commands                  │
│  ├─ spek.prepare        (pre-flight)             │
│  ├─ spek.automate       (orchestrate)            │
│  ├─ spek.implement      (execute)                │
│  ├─ spek.post           (wrap-up)                │
│  ├─ spek.lessons        (learn)                  │
│  └─ spek.context        (load)                   │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  SPECKIT LAYER: /speckit.* commands              │
│  ├─ speckit.constitution (define principles)     │
│  ├─ speckit.specify      (write spec)            │
│  ├─ speckit.plan         (create tasks)          │
│  ├─ speckit.analyze      (risk/readiness)        │
│  └─ speckit.implement    (execute tasks)         │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  CORE LAYER: Knowledge + Analysis                │
│  ├─ wiki/Vault (persistent knowledge)           │
│  ├─ CodeGraph MCP (real-time code analysis)      │
│  ├─ Git (version control)                        │
│  └─ Session State (temp context)                 │
└──────────────────────────────────────────────────┘
```

---

## Execution Context

### Session Initialization

When a user invokes `/spek.context` or any `/spek.*` command:

1. **Load Vault Context:** Fetch specs, plans, decisions from wiki/vault
2. **Load Repo Memory:** Read `.git/spek-memory/` for workspace-scoped facts
3. **Refresh CodeGraph:** Sync latest code changes via MCP
4. **Populate Session State:** Assemble context for SpecKit engine or skill execution

### Command Execution (Example: `/spek.automate`)

1. **Preparation:** Run pre-flight checks (`spek.prepare` substeps)
2. **Orchestration:** Call SpecKit pipeline
   - `/speckit.specify`: Generate feature spec with enrichments
   - `/speckit.plan`: Break spec into tasks
   - `/speckit.analyze`: Validate plan (risk, feasibility, token budget)
3. **Storage:** Archive spec/plan in wiki/vault (Git commit)
4. **Return:** Hand off to `spek.implement` for task execution

---

## Data Persistence Model

| Layer | Storage | Sync | Lifetime |
|-------|---------|------|----------|
| **Knowledge Vault** | Git (wiki/vault sync) | Manual (user commits) + Auto (post/lessons) | Persistent (feature cycle + beyond) |
| **Repo Memory** | `.git/spek-memory/` (YAML) | Git hook + manual | Persistent (workspace lifetime) |
| **CodeGraph** | SQLite in `.codegraph/` | File watcher (auto) | Persistent (session lifetime) |
| **Session State** | In-memory + context window | Manual commits to memory | Temporary (single session) |

---

## Cross-Component Dependencies

```
User Intention
    ↓
/spek.prepare
    ↓ (invokes)
/spek.automate
    ├→ /speckit.specify (reads vault, writes spec)
    ├→ /speckit.plan (reads spec, writes plan)
    ├→ /speckit.analyze (queries CodeGraph, validates)
    │
/spek.implement
    ├→ Read plan from vault
    ├→ Query CodeGraph for context (callers, definitions)
    ├→ Generate + execute code changes
    │
/spek.post
    ├→ Archive spec/plan/outcomes in vault
    ├→ Refresh CodeGraph (commit changes)
    ├→ Update repo memory
    │
/spek.lessons
    ├→ Extract structured lessons
    └→ Commit vault + memory updates
```

---

## Design Patterns

See [patterns](patterns/) directory for detailed deep-dives:

- **Enrichment Layer Pattern:** How specs/plans gain context-specific layers (Success Criteria, Assumptions, etc.)
- **Context Injection Pattern:** Session initialization strategy
- **Error Categorization Pattern:** Handling failures deterministically
- **Feature State Tracking Pattern:** Tracking feature development progress

---

## References

- **Intention & Philosophy:** [intention.md](intention.md)
- **Workflow Details:** [workflow.md](workflow.md)
- **Naming & Namespacing:** [naming-conventions.md](naming-conventions.md)
