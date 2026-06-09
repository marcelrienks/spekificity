# Spekificity Architecture Specification

## Four Design Pillars

Token Efficiency, Determinism, Persistence, Autonomy. See [vision.md](vision.md) for descriptions.

**Component Mapping:** Vault (persistence + determinism), lat.md index (token efficiency + determinism), SpecKit (deterministic orchestration), Caveman (token efficiency).

---

## Execution Model

Spekificity operates in two distinct layers: a CLI for project scaffolding, and agent skills for workflow execution.

**CLI Layer: `spek` command**

The `spek` CLI has exactly one command: `spek init`. There are no CLI commands for prepare, plan, implement, or conclude. All workflow operations are agentic skills, not shell commands.

**Step 1: Global Install (Package Only)**
- `uv tool install spekificity --from git+...` installs the `spek` CLI tool
- Verifies Python 3.11+, git, uv in PATH

**Step 2: Per-Project Init (`spek init`)**
- One-time per project
- **Auto-detects and installs missing dependencies:** SpecKit, lat.md, Obsidian CLI (if not already installed)
- Initializes lat.md code index + documentation index
- Prompts for AI agent integration type (Claude, Copilot, Gemini, generic)
- Prompts for script type (sh, ps)
- Creates `.spek/` directory structure (vault, memory, config)
- **Installs agentic skill files** in the format required by the selected agent integration
- Runs `specify init .` for SpecKit per-project configuration
- Does NOT create a `specs/` directory at project root — specs are stored inside `.spek/vault/`

**Agent Skill Layer: `/spek.*` commands**

All workflow commands are agent skills installed by `spek init` into the project. They run inside the agent environment (Claude Code, Copilot, Gemini, etc.), not the terminal. Skill file location depends on integration type selected at init:

| Integration | Skill File Location |
|-------------|-------------------|
| Claude | `.claude/commands/` |
| Copilot | `.github/agents/skills/` |
| Gemini | agent-specific directory |
| Generic | `.spek/skills/` |

**Outcome:** `spek init` scaffolds infrastructure and installs skill files. All feature development then happens through agent skills (`/spek.prepare` → `/spek.plan` → `/spek.implement` → `/spek.conclude`), not the CLI.

**See also:** [setup.md](setup.md) (detailed setup specification), [workflow.md](workflow.md) (4-stage workflow), [patterns.md](patterns.md) (reusable patterns)

---

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

Retrieval guidance (Canonical Architecture)

Spekificity uses **lat.md as the sole code analysis tool**. Alternatives are not supported; all architecture assumes lat.md's pre-indexed MCP interface.

- lat.md provides lexical (BM25) retrieval for codebase queries: transparent, cost-effective, fast
- Incremental sync + file watcher ensure index freshness  
- MCP tool interface optimized for agent workflows

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

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SPEKIFICITY SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │  Obsidian Vault  │   │   lat.md MCP     │                │
│  │  .spek/vault/    │   │   lat.md Index   │                │
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
    │  (Git state, .spek/vault/ fresh, lat.md index synced)
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
- Git-tracked for version control and collaboration (commit via `git add vault/; git commit`)

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

**Deterministic, repeatable workflow steps. All run inside agent environment — not CLI.**

- `spek.prepare`: Initialize third-party tools (lat.md code index, lat.md doc index, store results in Obsidian vault)
- `spek.plan`: Wrap SpecKit pipeline in order — `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` — with remediations at each step
- `spek.implement`: Wrap `/speckit.implement` for task execution
- `spek.conclude`: All post-implementation functions — analysis, vault archive, lessons extraction (via `/spek.lessons` as sub-step), lat.md refresh
- `spek.context`: Load session context (vault, repo memory, graph state) — optional enhancement
- `spek.map`: Analyze dependencies + impact — optional enhancement

**Note:** `/spek.lessons` is called by `/spek.conclude` as a sub-step. It can also be invoked independently at any point.

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
4. **Populate Session State:** Assemble context for SpecKit engine or skill execution, enable downstream commands

### Command Execution (Example: `/spek.plan`)

**Enrichment Layer — What It Is:**

The "enrichment layer" is the mechanism by which Spekificity's skill files add context to SpecKit before it runs. Concretely: the skill file instructs the agent to read relevant vault decisions + patterns and include that content in the conversation context **before** invoking a SpecKit skill. SpecKit then operates with that context available.

This is not a programmatic API — it is **prompt-level context injection**. The agent skill file contains explicit instructions like:
1. "Read `.spek/vault/decisions.md` and identify decisions relevant to this feature"
2. "Read `.spek/vault/patterns.md` and identify patterns applicable here"
3. "Query lat.md for code symbols affected by this feature"
4. "Now invoke `/speckit.specify` with this context available"

SpecKit generates a richer, more accurate spec because the agent already has project decisions and code structure in context when it invokes SpecKit.

**Three-phase execution:**

1. **PRE (Context Injection):**
   - Agent reads vault decisions + patterns relevant to the feature
   - Agent queries lat.md code index for affected symbols and files
   - Agent holds this context — no separate "enrichment prompt" sent; context is in the conversation

2. **Core (SpecKit Invocation):**
   - `/speckit.specify`: Agent invokes with vault context already loaded
   - `/speckit.plan`: Agent invokes with code graph context from lat.md
   - `/speckit.tasks`: Agent invokes, tasks reference code files found via lat.md

3. **POST (Storage):**
   - Archive spec/plan/tasks to `.spek/vault/` (git commit)
   - Compress output if Caveman mode active

---

## Data Persistence Model

| Layer | Storage | Sync | Lifetime |
|-------|---------|------|----------|
| **Knowledge Vault** | Git (`.spek/vault/` directory) | Manual (user commits) after /spek.conclude | Persistent (feature cycle + beyond) |
| **Repo Memory** | `.spek/memory/` (YAML) | Manual after /spek.conclude | Persistent (workspace lifetime) |
| **lat.md** | Index directory in `.spek/lat/` (non-human-readable) | Manual via `/lat.sync` | Persistent (session lifetime) |
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
