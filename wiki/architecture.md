# Architectural Principles: Token Efficiency, Determinism, Persistence, Autonomy

**Date:** 2026-05-21

## 1. Token Efficiency
- All source code and wiki documents are pre-indexed using CodeGraph.
- Context injection is performed by querying CodeGraph for only the most relevant nodes (functions, patterns, lessons, decisions, etc.).
- Caveman skill is used to compress context (lessons, vault, session) for minimal token usage during agent operations.
- This approach ensures that only the most essential information is loaded into the agent’s context window, optimizing for both speed and cost.

## 2. Determinism
- SpecKit’s workflow (specify, clarify, plan, implement) is the backbone for all feature and skill orchestration.
- All agent actions are driven by explicit, spec-driven processes, ensuring repeatability and traceability.
- Skillsets are extended as needed, but always within the deterministic SpecKit orchestration model.
- This guarantees that outcomes are reproducible and auditable.

## 3. Persistence
- Obsidian CLI is the recommended runtime interface for automated vault and persistent memory operations. Spekificity uses the Obsidian CLI to perform scripted vault syncs, exports, and metadata extractions that enable automated context loading and lesson extraction; see `setup.sh` for verification and install instructions. If the Obsidian CLI is not available, manual vault workflows (git-backed markdown, manual export) are supported but will reduce automation.
- All session states, decisions, patterns, lessons, and architectural context (from CodeGraph source and wiki indexing) are managed and stored in the Obsidian vault.
- The vault serves as the single source of truth for all project knowledge, ensuring long-term durability and accessibility.

## 4. Autonomy
- CodeGraph enables autonomous extraction of context, impact analysis, and knowledge mapping.
- Agents can operate with minimal manual intervention, leveraging the indexed knowledge base for decision-making and workflow execution.
- This supports agentic workflows and continuous improvement.

---

## Architectural Viability
- The above principles are enforced in the project’s specifications, implementation roadmap, and workflow documentation.
- All critical dependencies (CodeGraph, SpecKit, Obsidian CLI, Caveman skill) are recommended and integrated at the architectural level to enable full automation and the four-pillar guarantees. Alternative tools may be used where constraints require them; see the decision matrix in `decision.md` for guidance and migration paths.
- This structure ensures the project’s goals of efficiency, determinism, persistence, and autonomy are met.

---

**This section should be referenced in architectural reviews and onboarding.**

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
│  │  vault/          │   │   CodeGraph MCP  │                │
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
    │  (Git state, vault/ fresh, graph synced)
    │
    ├─ /spek.plan ────────────────┐
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
    ├─ /spek.conclude ─────────────→ Outcomes Archived
    │  (Archive, Lessons, Refresh)     (vault/ + Graph Updated)
    │
    ├─ /spek.lessons ─────────────────► Lessons Extracted
    │  (Structured capture)            (vault/ + Session Updated)
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

- Receives spec document from vault/
- Generates execution plan with dependencies and task breakdown
- Routes tasks to agent for implementation
- Collects analysis (risk, metrics, dependencies)

### Agent Skills Layer (`/spek.*` commands)

**Deterministic, repeatable workflow steps.**

- `spek.prepare`: Pre-flight checks (workspace state, graph freshness, vault ready)
- `spek.plan`: Invoke SpecKit pipeline (specify → plan → analyze)
- `spek.implement`: Execute approved tasks with full context
- `spek.conclude`: Archive outcomes, update vault, refresh graph
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
│  ├─ spek.plan           (orchestrate)            │
│  ├─ spek.implement      (execute)                │
│  ├─ spek.conclude           (wrap-up)                │
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
│  ├─ vault/ (persistent knowledge)           │
│  ├─ CodeGraph MCP (real-time code analysis)      │
│  ├─ Git (version control)                        │
│  └─ Session State (temp context)                 │
└──────────────────────────────────────────────────┘
```

---

## Execution Context

### Session Initialization

When a user invokes `/spek.context` or any `/spek.*` command:

1. **Load Vault Context:** Fetch specs, plans, decisions from vault/
2. **Load Repo Memory:** Read `.git/spek-memory/` for workspace-scoped facts
3. **Refresh CodeGraph:** Sync latest code changes via MCP
4. **Populate Session State:** Assemble context for SpecKit engine or skill execution

### Command Execution (Example: `/spek.plan`)

1. **Preparation:** Run pre-flight checks (`spek.prepare` substeps)
2. **Orchestration:** Call SpecKit pipeline
   - `/speckit.specify`: Generate feature spec with enrichments
   - `/speckit.plan`: Break spec into tasks
   - `/speckit.analyze`: Validate plan (risk, feasibility, token budget)
3. **Storage:** Archive spec/plan in vault/ (Git commit)
4. **Return:** Hand off to `spek.implement` for task execution

---

## Data Persistence Model

| Layer | Storage | Sync | Lifetime |
|-------|---------|------|----------|
| **Knowledge Vault** | Git (vault/ sync) | Manual (user commits) + Auto (post/lessons) | Persistent (feature cycle + beyond) |
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
/spek.plan
    ├→ /speckit.specify (reads vault, writes spec)
    ├→ /speckit.plan (reads spec, writes plan)
    ├→ /speckit.analyze (queries CodeGraph, validates)
    │
/spek.implement
    ├→ Read plan from vault
    ├→ Query CodeGraph for context (callers, definitions)
    ├→ Generate + execute code changes
    │
/spek.conclude
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
- **Naming & Namespacing:** [conventions.md](conventions.md)
