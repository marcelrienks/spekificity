# Spekificity Architecture Specification

## Four Design Pillars

Token Efficiency, Determinism, Persistence, Autonomy.

**Component Mapping:** Obsidian Vault (persistence + determinism), lat.md index (token efficiency + determinism), SpecKit (deterministic orchestration), Caveman (token efficiency).

---

## Execution Model

Spekificity operates in two distinct layers: a CLI for project scaffolding, and agent skills for workflow execution.

**CLI Layer: `spek` command**

The `spek` CLI has exactly one command: `spek init`. There are no CLI commands for prepare, plan, implement, or conclude. All workflow operations are agentic skills, not shell commands.

**Step 1: Global Install (Package + Runtime Prerequisites)**
- `uv tool install spekificity --from git+...` installs the `spek` CLI tool
- **Verifies and installs runtime prerequisites** required to run `spek init`: Python 3.10+, uv 0.1+, Node.js 18+, git 2.0+
- Does NOT install project-level 3rd party tools (SpecKit, lat.md, Obsidian CLI) — that is `spek init`'s responsibility

**Step 2: Per-Project Init (`spek init [path]`)**
- One-time per project
- Uses supplied path, or . for present working directory
- **Verifies runtime prerequisites are present** (installed in Step 1); fails with descriptive error if any are missing
- **Detects and installs missing 3rd party project tools:** SpecKit (`specify` via uv), lat.md (`lat` via npm), Obsidian desktop (via brew/winget); if `obsidian` binary not in PATH after install, outputs CLI registration instructions (one-time manual step: Obsidian Settings → General → Enable CLI) and halts
- Initializes lat.md code index + documentation index
- Prompts for AI agent integration type — any value from `specify integration list` (e.g. `claude`, `copilot`, `gemini`, `cursor-agent`, `windsurf`, `cline`, `codex`, `kiro-cli`, `amp`, `qwen`, `generic`) — assigns to variable used by both skill file placement and `specify init`
- Prompts for script type (sh, ps) and assigns to variable
- Creates `.spek/` directory structure (vault, memory, config)
- **Copies bundled skill files** from `spekificity/skills/` (package source) to the integration's skills directory — no code-side generation or string templating
- **Installs Caveman compression skill** — fetches `SKILL.md` from the `github:JuliusBrussee/caveman` package and places it in the integration's skills directory; for `claude` integration, also writes `SessionStart` and `UserPromptSubmit` hooks to the project's `.claude/settings.json` for automatic per-session activation
- Runs `specify init` for the given path, or . for present working directory, and supplies the AI agent and script type variables

**Agent Skill Layer: `/spek.*` commands**

All workflow commands are agent skills installed by `spek init` into the project. They run inside the agent environment (Claude Code, Copilot, Gemini, Cursor, Windsurf, Cline, Codex, Kiro, etc.), not the terminal. Skill file location depends on integration type selected at init:

| Integration | Agent | Skill File Location |
|-------------|-------|---------------------|
| `claude` | Claude Code | `.claude/commands/` |
| `copilot` | GitHub Copilot | `.github/skills/` |
| `gemini` | Gemini CLI | `.gemini/skills/` |
| `cursor-agent` | Cursor | `.cursor/skills/` |
| `windsurf` | Windsurf | `.windsurf/skills/` |
| `cline` | Cline | `.cline/skills/` |
| `codex` | Codex CLI | `.codex/skills/` |
| `kiro-cli` | Kiro (AWS) | `.kiro/skills/` |
| `amp` | Amp (Sourcegraph) | `.amp/skills/` |
| `qwen` | Qwen Code | `.qwen/skills/` |
| `generic` | Any / tool-agnostic | `.agents/skills/` (default) |
| *(all other specify values)* | — | `.agents/skills/` (fallback) |

**Outcome:** `spek init` scaffolds infrastructure and copies bundled skill files into the project. All feature development then happens through agent skills (`/spek.prepare` → `/spek.plan` → `/spek.implement` → `/spek.conclude`), not the CLI.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     SPEKIFICITY SYSTEM                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │  Obsidian Vault  │   │   lat.md MCP     │                │
│  │  .spek/vault/    │   │   lat.md Index   │                │
│  │  (Knowledge)     │   │   (Code Intel)   │                │
│  └────────┬─────────┘   └────────┬─────────┘                │
│           │                      │                          │
│           └──────────┬───────────┘                          │
│                      │                                      │
│              ┌───────▼────────┐                             │
│              │   Context      │                             │
│              │   Layer        │                             │
│              └───────┬────────┘                             │
│                      │                                      │
│           ┌──────────┴──────────┐                           │
│           │                     │                           │
│     ┌─────▼──────┐       ┌─────▼──────┐                     │
│     │  SpecKit   │       │  Agent     │                     │
│     │  Workflow  │       │  Skills    │                     │
│     │  Engine    │       │  (/spek.*) │                     │
│     └─────┬──────┘       └──────┬─────┘                     │
│           │                     │                           │
│           └──────────┬──────────┘                           │
│                      │                                      │
│              ┌───────▼────────┐                             │
│              │   Feature Out  │                             │
│              │   (Code + Docs)│                             │
│              └────────────────┘                             │
│                                                             │
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
    ├─ /spek.plan
    │  (Orchestrate SpecKit)
    │
    │  ├─ /speckit.specify ──────────► Spec Created
    │  │  (+ vault enrichment)         (Success Criteria,
    │  │                                Assumptions, etc.)
    │  │
    │  ├─ /speckit.plan ──────────────► Plan Created
    │  │  (+ lat.md enrichment)        (Tasks, Deps,
    │  │                                Affected Code)
    │  │
    │  ├─ /speckit.tasks ─────────────► Task List Created
    │  │                                (Dependency-ordered)
    │  │
    │  └─ Anti-Sycophancy ────────────► Violations Logged
    │     (validate_spec())             (.spek/memory/violations.md)
    │
    ├─ /spek.implement ───────────────► Features Coded
    │  (Per-task execution)            (Tests, Docs)
    │
    └─ /spek.conclude ─────────────► Outcomes Persisted
       │  (Commit to git)             (vault/ + lat.md index updated)
       ├─ /spek.lessons (sub-step) ─► Lessons Extracted
       │  (Structured capture)        (vault/lessons/ + memory updated)
       ├─ Backprop Reflex ──────────► Failure Patterns Captured
       │  (backprop_reflex())         (.spek/vault/patterns.md)
       ├─ /spek.blind-review ───────► Quality Report (optional)
       │  (context-free review)       (.spek/memory/blind-review-*.md)
       └─ /spek.rarv ───────────────► Spec Drift Resolved (optional)
          (RARV cycle)                (vault decisions updated)

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

#### Primary Workflow

Four skills form the core feature development cycle. Run in order for every feature: `prepare → plan → implement → conclude`.

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `spek.prepare` | Pre-flight: sync tools, verify constitution |
| 2 | `spek.plan` | Orchestrate spec → plan → tasks pipeline |
| 3 | `spek.implement` | Execute implementation tasks from plan |
| 4 | `spek.conclude` | Persist outcomes to git, refresh index, extract lessons |

**`/spek.prepare`**
- Initialize lat.md code + doc index; store references in vault
- Verify constitution exists — invoke `/speckit.constitution` if missing
- Confirm workspace is ready before planning begins

**`/spek.plan`**
- Invoke SpecKit pipeline in order: `/speckit.specify` → `/speckit.plan` → `/speckit.tasks`
- Enrich each step with vault context (decisions, patterns) and lat.md code graph
- Remediate and validate at each step before advancing

**`/spek.implement`**
- Wrap `/speckit.implement` for per-task execution
- Load task context from vault and lat.md before each task
- Execute, test, and document changes

**`/spek.conclude`**
- Persist spec, plan, and outcomes in `.spek/vault/` (git commit)
- Refresh lat.md index with committed changes
- Invoke `/spek.lessons` as sub-step to extract and store lessons

#### Supplementary Skills

Use these independently to enhance context or inspect state. Not required for every cycle.

**`/spek.lessons`**
- Extract structured lessons from the current session or implementation
- Commit findings to vault + repo memory (`.spek/memory/`)
- Called automatically by `/spek.conclude`; can also run standalone at any point

**`/spek.context`**
- Load vault context (decisions, patterns, lessons) into current session
- Read `.spek/memory/` for workspace-scoped facts
- Populate session state; makes context available to all downstream commands

**`/spek.map`**
- Query lat.md for code references to a spec topic
- Query vault for related decisions and dependent specs
- Generate dependency graph; highlight blockers and critical paths

**`/spek.blind-review`**
- Anonymize AI attribution in working memory; run linter + complexity checks
- Report findings with severity tags (CRITICAL / WARNING / INFO)
- Write full report to `.spek/memory/blind-review-YYYY-MM-DD.md`
- Optional; run after implementation and before `/spek.conclude`

**`/spek.rarv`**
- Run Reason-Act-Reflect-Verify cycle to detect spec drift
- Compare original spec vs implemented artifacts
- For each deviation: fix code, justify in vault, or defer as tech debt
- Optional; run after `/spek.conclude` for features with architectural changes

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
│                                                  │
│  ── Primary Workflow ──────────────────────────  │
│  ├─ spek.prepare        (pre-flight)             │
│  ├─ spek.plan           (orchestrate)            │
│  ├─ spek.implement      (execute)                │
│  └─ spek.conclude       (wrap-up)                │
│                                                  │
│  ── Supplementary ─────────────────────────────  │
│  ├─ spek.lessons        (learn)                  │
│  ├─ spek.context        (load context)           │
│  ├─ spek.map            (dependencies)           │
│  ├─ spek.blind-review   (quality pass)           │
│  └─ spek.rarv           (spec drift)             │
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
│  ├─ vault/ (persistent knowledge)                │
│  ├─ lat.md MCP (real-time index/analysis)        │
│  ├─ Git (version control)                        │
│  └─ Session State (temp context)                 │
└──────────────────────────────────────────────────┘
```

---

## Execution Context

### Session Initialization

When any `/spek.*` command runs:

1. **Load Vault Context:** Fetch specs, plans, decisions from vault/
2. **Load Repo Memory:** Read `.spek/memory/` for workspace-scoped facts
3. **Refresh lat.md index:** Sync latest code changes via MCP
4. **Populate Session State:** Assemble context for SpecKit engine or skill execution, enable downstream commands

### Command Execution (Example: `/spek.plan`)

**Enrichment Layer — What It Is:**

The "enrichment layer" is the mechanism by which Spekificity's skill files add context to SpecKit before it runs. Concretely: the skill file instructs the agent to read relevant vault decisions + patterns and include that content in the conversation context **before** invoking a SpecKit skill. SpecKit then operates with that context available.

This is not a programmatic API — it is **prompt-level context injection**. The agent skill file contains explicit instructions like:
1. "Run `obsidian read file=decisions vault=vault` and identify decisions relevant to this feature"
2. "Run `obsidian read file=patterns vault=vault` and identify patterns applicable here"
3. "Query lat.md via MCP for code symbols affected by this feature"
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
| **lat.md** | Index directory in `.spek/lat.md/` (non-human-readable) | Manual via `/lat.sync` | Persistent (session lifetime) |
| **Session State** | In-memory + context window | Manual commits to memory | Temporary (single session) |

---

## Cross-Component Dependencies

Primary workflow only. Supplementary skills (`/spek.context`, `/spek.map`, `/spek.lessons` standalone) can be invoked at any point and are omitted from this flow.

```
User Intention
    ↓
/spek.prepare
    ↓ (invokes)
/spek.plan
    ├→ /speckit.specify (reads vault, writes spec to `.spek/vault/` with approval frontmatter)
    ├→ /speckit.plan (reads spec, writes plan to SpecKit-managed path; archived to .spek/vault/)
    └→ /speckit.tasks (reads plan, writes tasks to SpecKit-managed path; archived to .spek/vault/)
    │
/spek.implement
    ├→ Read plan from vault
    ├→ Query lat.md for context (callers, definitions)
    ├→ Generate + execute code changes
    │
/spek.conclude
    ├→ /speckit.analyze (queries lat.md, validates completeness)
    ├→ /spek.lessons (sub-step: extract + commit lessons)
    ├→ backprop_reflex() (parse test output; append to vault/patterns.md)
    ├→ Archive spec/plan/outcomes in vault
    ├→ Update vault/patterns.md + vault/decisions.md
    ├→ Refresh lat.md index (lat init)
    ├→ Update repo memory (.spek/memory/)
    ├→ git add .spek/vault/ .spek/memory/ && git commit
    ├→ /spek.blind-review (optional: context-free quality pass)
    └→ /spek.rarv (optional: spec drift detection + resolution)
```
