---
title: architecture
type: guide
tags: []
---

# Architectural Principles: Token Efficiency, Determinism, Persistence, Autonomy

## 1. Token Efficiency
- All source code and wiki documents are pre-indexed using lat.md.
- Context injection is performed by querying lat.md for only the most relevant nodes (functions, patterns, lessons, decisions, etc.).
- Caveman skill is used to compress context (lessons, vault, session) for minimal token usage during agent operations.
- This approach ensures that only the most essential information is loaded into the agent’s context window, optimizing for both speed and cost.

## 2. Determinism
- SpecKit’s workflow (specify, clarify, plan, implement) is the backbone for all feature and skill orchestration.
- All agent actions are driven by explicit, spec-driven processes, ensuring repeatability and traceability.
- Skillsets are extended as needed, but always within the deterministic SpecKit orchestration model.
- This guarantees that outcomes are reproducible and auditable.

## 3. Persistence
The `obsidian` CLI is the required runtime interface for automated vault and persistent memory operations. Spekificity uses the Obsidian CLI to perform scripted vault syncs, exports, and metadata extractions that enable automated context loading and lesson extraction; see `setup.sh` for verification and install instructions. The Obsidian desktop app is optional and may be used for visualization or interactive workflows; it is not a substitute for the required CLI.
- All session states, decisions, patterns, lessons, and architectural context (from lat.md source and wiki indexing) are managed and stored in the Obsidian vault.
- The vault serves as the single source of truth for all project knowledge, ensuring long-term durability and accessibility.

## 4. Autonomy

- lat.md enables autonomous extraction of context, impact analysis, and knowledge mapping.
- Agents can operate with minimal manual intervention, leveraging the indexed knowledge base for decision-making and workflow execution.
- This supports agentic workflows and continuous improvement.

## Implementation direction: Programmatic pipeline

Spekificity adopts the programmatic pipeline as the project architecture and operational default.

- **Primary architecture — Programmatic pipeline (package):** deterministic outputs, typed contracts (Pydantic), content-addressable IDs (e.g., SHA-256 of normalized body), integrated lint/repair agents, and structural Markdown enforcement (markdown-hero). BM25 lexical retrieval is the default. This path supports large corpora, scheduled runs, CI/CD, auditability, and downstream automation.

Rationale:

- Deterministic runs produce idempotent artifacts, simplify deduplication and merging, and enable robust testing and audit trails.
- Typed contracts and content-addressable IDs make ingestion, repair, and regression analysis reliable.
- Structural Markdown enforcement prevents downstream corruption of chunking/indexing and enables safe automated merges.

Markdown structural hygiene (mandatory):

- Enforce strict structural checks before merging generated pages (no duplicate H1s, valid YAML frontmatter, parseable tables, correct heading nesting).
- Use section-aware chunking to keep chunk windows inside headings.
- Prefer canonicalization and safe-merge strategies (dedupe_headings=True).
- Route structural failures to a repair agent or human review; structural noise breaks chunking, dedupe, and indexing.

Retrieval guidance

- Start with lexical/BM25 retrieval for wiki-scale corpora: transparent, cost-effective, fast to index and run.
- Add hybrid or vector layers when semantic synonymy, scale, or UX require it (large stable KBs, sub-second latency).
- Treat agent-as-retriever (just-in-time context loading) as an auxiliary technique for freshness-critical queries or development/testing, not as the architectural default.

Operational heuristics

- Use deterministic IDs and typed outputs for idempotence, simpler dedupe, and auditability.
- Run small-batch ingestion tests (5–10 documents) before scaling.
- Integrate markdown-hero (or equivalent) into Generator → Lint → Consolidate stages.
- Use git-backed vault with pre-commit structural lints and human approval gates for writes.

HTML artifact policy

- Store generated HTML artifacts outside primary wiki pages under `wiki/artifacts/html/`.
- Require each HTML artifact to embed or link an export-to-markdown feature that produces a canonical markdown record or a short 3-line summary suitable for PR reviews.
- Host artifacts on static site (S3/Vercel) where appropriate; link from canonical markdown/PR for review.
- CI: flag large HTML files and ensure export-to-markdown present when HTML is checked into repo; fail CI when export missing for audited artifacts.

## Exploratory note: Agentic instruction files

Agentic instruction files (AGENTS.md) remain supported as a lightweight experimental path for personal or small-team workflows. They are not the project architecture. Rules for exploratory use:

- Use only for experiments, discovery, or rapid iteration on small vaults.
- Conform to the same structural hygiene and pre-merge checks as programmatic pipelines.
- Include plan-before-execute gating and allowlists for tool surface.
- Do not use agentic path for production ingest, scheduled runs, or pipelines that require reproducibility.

---

## Architectural Viability
- The above principles are enforced in the project’s specifications, implementation roadmap, and workflow documentation.
- All critical dependencies (`lat.md`, `SpecKit`, `obsidian` CLI, `Caveman` skill) are required and integrated at the architectural level to enable the automation and the four-pillar guarantees. The Obsidian desktop app is optional for interactive use and visualization.
- This structure ensures the project’s goals of efficiency, determinism, persistence, and autonomy are met.

---

**This section should be referenced in architectural reviews and onboarding.**

# Spekificity Architecture

> **Execution model note:** Spekificity is init-first. Install globally via `uv`, then run `spek init` in a target project to scaffold `.spek` skills/functions. References in this document to `/spek.*` denote generated skills executed by an agent runtime, not direct shell subcommands.

**See also:** [vision.md](vision.md) (philosophy & principles) → [workflow.md](workflow.md) (process)

**Note:** This document covers technical architecture only. For philosophical foundations and design principles, see [vision.md](vision.md).

---

## Overview

Spekificity is a **specification-driven agent development framework** that ties project knowledge (Obsidian vault), code analysis (lat.md), workflow automation (SpecKit), and skill execution (Agent Skills) into a coherent pipeline.

**Core Goal:** Enable rapid, deterministic feature development with minimal token overhead and maximum context reuse.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SPEKIFICITY SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │  vault/          │   │   lat.md MCP     │                │
│  │  vault/          │   │   lat.md Index   │                │
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
    │  (Git state, vault/ fresh, lat.md index synced)
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
    │  (Archive, Lessons, Refresh)     (vault/ + lat.md index updated)
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

### lat.md index

**Real-time indexing and impact detection (lat.md).**

- Indexes project Markdown and extracts source metadata (symbols, definitions, call chains)
- Provides impact analysis via lat.md query tools
- Supports incremental refresh and optional watch mode
- Serves agent queries without full file scanning (token-efficient)

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
│  ├─ lat.md MCP (real-time index/analysis)        │
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
3. **Refresh lat.md index:** Sync latest code changes via MCP
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
| **lat.md** | Index directory in `.spek/lat/` (primary, non-human-readable) | File watcher (auto) | Persistent (session lifetime) |
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
    ├→ /speckit.analyze (queries lat.md, validates)
    │
/spek.implement
    ├→ Read plan from vault
    ├→ Query lat.md for context (callers, definitions)
    ├→ Generate + execute code changes
    │
/spek.conclude
    ├→ Archive spec/plan/outcomes in vault
    ├→ Refresh lat.md index (commit changes)
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

- **Intention & Philosophy:** [vision.md](vision.md)
- **Workflow Details:** [workflow.md](workflow.md)
- **Naming & Namespacing:** [conventions.md](conventions.md)
