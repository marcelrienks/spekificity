# Spekificity Architecture & Vision

## Vision Statement

Spekificity is a spec-driven agent development framework that ties project knowledge (Obsidian vault), code analysis (lat.md), workflow automation (SpecKit), and skill execution (Agent Skills) into a single workflow. It solves four core problems: token efficiency, deterministic planning, persistent project memory, and agent autonomy.

**Core Problem & Core Solution:**
- Problem: AI-assisted development often loses context between sessions, wastes tokens re-reading files, and produces work without durable specifications or lessons.
- Solution: Treat documentation as canonical memory (markdown vault), use a code graph/index for precise context (lat.md), and orchestrate feature work with a spec-first engine (SpecKit) wrapped by Spekificity skills.

**Philosophy & Tenets:**
- Consolidation, not reinvention: integrate best-in-class tools (SpecKit, lat.md, Obsidian-style vault) rather than rebuilding them.
- Decorator pattern: Spekificity wraps SpecKit commands to inject context and enrichment, without modifying upstream tools.
- Modular independence: each component (vault, index, spec engine, compression) can be upgraded independently.
- Human-in-the-loop safety: agent actions are gated by plan reviews and contradiction flags; human decisions resolve conflicts.
- Token efficiency by default: graph queries + cached vault context replace repeated file scans; Caveman mode provides optional terse outputs.

---

## Four Pillars: Core Design Drivers

Spekificity rests on four pillars that guide all design decisions:

1. **Token Efficiency** — AI-assisted development often re-reads files repeatedly, wasting tokens. Solution: Pre-index code and docs; load only minimal, relevant context via lat.md queries and compressed outputs (Caveman mode). Ensures agents operate with significantly lower token overhead while maintaining full context precision.

2. **Determinism** — Unstructured agent workflows produce unreproducible outcomes. Solution: Enforce spec → plan → implement → conclude workflows via SpecKit, making outcomes reproducible and auditable. Specs serve as canonical records, enabling consistent decision-making across sessions.

3. **Persistence** — Project knowledge vanishes between sessions. Solution: Store all specs, decisions, and lessons in a Git-backed Obsidian-style markdown vault. Knowledge compounds across sessions, enabling agents to reference historical decisions and avoid repeated mistakes.

4. **Autonomy** — Agents often need hand-holding to navigate context. Solution: Equip agents with deterministic tools (lat.md index, SpecKit engine) and indexed context so they execute feature work with minimal human intervention, while maintaining human-in-the-loop safety through plan reviews and contradiction flags.

**Component Mapping:** Vault (persistence + determinism), lat.md index (token efficiency + determinism), SpecKit (deterministic orchestration), Caveman (token efficiency).

---

## Execution Model

Spekificity uses two-phase setup:

**Phase 1: Global Install (Dependency Resolution)**
- `uv tool install spekificity --from git+...` resolves ALL dependencies
- Automatically installs SpecKit (if missing)
- Automatically installs lat.md (if missing)
- Verifies Python 3.11+, git, uv in PATH
- Warns if Obsidian CLI missing (optional but recommended)

**Phase 2: Per-Project Init**
- `spek init` (one-time per project)
- Runs `specify init .` for SpecKit per-project configuration
- Creates vault structure, .spek/ skills, .lat/ index, specs/ directory
- References to `/spek.*` denote generated agent skills, not shell commands

**Result:** All tools installed globally; each project scaffolded locally. Ready for `/spek.prepare` → feature development.

**See also:** [setup.md](setup.md) (detailed install guide), [workflow.md](workflow.md) (4-stage process), [patterns.md](patterns.md) (reusable patterns)

---

## Principle Details

### 1. Token Efficiency Implementation
- All source code and wiki documents are pre-indexed using lat.md.
- Context injection performed by querying lat.md for only the most relevant nodes (functions, patterns, lessons, decisions).
- Caveman skill compresses context (lessons, vault, session) for minimal token usage during agent operations.
- Only essential information loaded into context window; optimizes for speed and cost.

### 2. Determinism Implementation
- SpecKit’s workflow (specify, clarify, plan, implement) is backbone for all feature and skill orchestration.
- All agent actions driven by explicit, spec-driven processes; ensures repeatability and traceability.
- Skillsets extended as needed, but always within deterministic SpecKit orchestration model.
- Outcomes are reproducible and auditable.

### 3. Persistence Implementation
**Obsidian CLI Required:** Automated vault operations (syncs, exports, metadata extractions) enable context loading and lesson extraction during `/spek.conclude`. Obsidian desktop app optional for visualization.

- All decisions, patterns, lessons, and architectural context stored in vault (single source of truth)
- Vault synced to Git for version control and team collaboration
- Obsidian CLI performs automated vault operations; desktop app optional for browsing

### 4. Autonomy Implementation
- lat.md enables autonomous extraction of context, impact analysis, and knowledge mapping.
- Agents operate with minimal manual intervention, leveraging indexed knowledge base for decision-making and workflow execution.
- Supports agentic workflows and continuous improvement.

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
- Git-tracked for version control and collaboration (manual commit via `git add vault/; git commit`)

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

**Two-phase enrichment:**

1. **PRE-Execution Enrichment (Context Injection):**
   - Load vault decisions + patterns
   - Load code graph via lat.md
   - Compose enrichment prompt
   - Prepend to SpecKit inputs

2. **Core Execution:**
   - `/speckit.specify`: Generate feature spec with injected context
   - `/speckit.plan`: Create architecture + tech choices (code graph injected)
   - `/speckit.tasks`: Break plan into executable tasks
   - `/speckit.analyze`: Validate completeness

3. **POST-Execution Enrichment (Compression & Storage):**
   - Compress output (caveman mode if configured)
   - Archive spec/plan/tasks in vault/ (Git commit)
   - Validate output aligns with injected context

4. **Return:** Hand off to `spek.implement` for task execution

---

## Data Persistence Model

| Layer | Storage | Sync | Lifetime |
|-------|---------|------|----------|
| **Knowledge Vault** | Git (vault/ directory) | Manual (user commits) after /spek.conclude | Persistent (feature cycle + beyond) |
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
    ├→ /speckit.specify (reads vault, writes spec with enrichments)
    ├→ /speckit.plan (reads spec, writes plan with code graph)
    ├→ /speckit.tasks (reads plan, writes dependency-ordered tasks)
    ├→ /speckit.analyze (queries lat.md, validates completeness)
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
