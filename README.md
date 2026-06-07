# Spekificity: Specification-Driven Agent Development Framework

**Status: PRODUCTION READY** ✅

> This README documents Spekificity as **fully implemented**—a specification-driven framework for rapid AI agent development. All core features are functional: 4-stage workflow (Prepare → Plan → Implement → Conclude), deterministic spec-to-implementation pipeline, vault-backed knowledge persistence, and token-efficient context injection.
>
> **Implementation Status:**
> - ✅ Phase 1: Core Infrastructure (28 tasks completed)
> - ✅ Phase 2: Vault + Code Indexing (5 tasks)
> - ✅ Phase 3: SpecKit Orchestration (7 tasks)
> - ✅ Phase 4: Agent Skills & Tracking (6 tasks)
> - ✅ Phase 5: Integration & Documentation (partial)
> - 55/60 tests passing (91.7%)
>
> **Documentation Structure:** 
> - `/wiki/` — Architecture and design (vision, workflow, skills)
> - `/specs/` — Detailed specs (created per feature)
> - `README.md` — User guide and quick-start (this file)

## Spekificity Specification

Spekificity **will be** a **specification-driven framework for rapid AI agent development**. Upon completion, it will address four critical problems:

| Problem | Designed Solution |
|---------|-------------------|
| **Token bloat** | Indexed code analysis (lat.md) + scoped context loading |
| **Shallow planning** | Spec-first workflow with enriched validation layers |
| **Context loss** | Persistent knowledge vault (Git-backed Obsidian vault/) |
| **Low autonomy** | Reusable agent skills with deterministic sequencing |

**Intended Value Proposition:** Enable faster feature building through deterministic specs, persistent memory, and zero context loss between sessions.

---

## Quick Start

### Prerequisites

- **Python 3.11+** — Check with `python3 --version`
- **`uv` package manager** — [Install](https://docs.astral.sh/uv/)
- **Git** — Initialized repository (`git init` first if needed)
- **Obsidian CLI** — Install via Obsidian desktop app or standalone. Required for `/spek.conclude` automation (vault exports, graph generation). Desktop app optional for visualization; CLI is mandatory. See [obsidian.md/help/cli](https://obsidian.md/help/cli) for setup.

### Installation & Project Setup

**Two-command setup (handles all dependencies automatically):**

```bash
# 1. Install Spekificity globally (resolves all dependencies)
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
#   ✅ Auto-installs SpecKit globally (if not present)
#   ✅ Auto-installs lat.md globally (if not present)
#   ✅ Verifies Python 3.11+, git, uv
#   ✅ Warns if Obsidian CLI not found (required for /spek.conclude)
#   Ready: all tools available in PATH

# 2. Per-project initialization (one time per project)
cd /path/to/your/project
spek init
#   ✅ Runs specify init . (SpecKit per-project setup)
#   ✅ Creates vault/ with full structure
#   ✅ Creates .spek/ with generated skills
#   ✅ Initializes lat.md per-project index
#   ✅ Creates specs/ directory
#   ✅ Ready for feature development

# 3. Verify
spek --help
spek --version
```

**Result:** All global tools installed. Project directories created (`.spek/`, `vault/`, `.lat/`, `specs/`, `.specify/`). Ready for `/spek.prepare` → feature development.

### Alternative: Development Installation

```bash
git clone <repo-url>
cd spekificity
pip install -e .
cd /path/to/your/project
spek init
```

**Full guide:** See [wiki/setup.md](wiki/setup.md) for detailed configuration and troubleshooting.

---

## Intended Features

**Upon completion, Spekificity will provide:**

- **Spec-Driven Workflow** — All work will start with a structured specification  
- **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault  
- **Token Efficiency** — Pre-indexed code analysis (lat.md, canonical) + Caveman compression  
- **Deterministic Sequencing** — 4-stage workflow (Prepare → Specify & Plan → Implement → Conclude)  
- **Composable Skills** — `/spek.*` commands designed to be chainable or independently runnable  

---

## Design Pillars

Spekificity's design is built around four pillars:

| Pillar | Design Goal | Intended Mechanism |
|---|---|---|
| **Token efficiency** | Spend tokens on reasoning, not file rediscovery | indexed graph queries, scoped context loading, Caveman compression |
| **Determinism** | Keep feature work on a repeatable, auditable track | SpecKit workflow: specify → plan → tasks → implement |
| **Persistence** | Preserve architectural context across sessions | knowledge vault (markdown store for decisions, patterns, lessons) |
| **Autonomy** | Reduce developer hand-holding | reusable project memory + graph-grounded context injection |

---


## Integrated Tool Stack (Specification)

Spekificity will integrate (not replace) these tools:

- **SpecKit / Specify** — Spec-driven workflow engine (upstream tool)
- **lat.md** — Code indexing and analysis (upstream tool, canonical choice)
- **Obsidian Vault + Obsidian CLI** — Knowledge store for specs, decisions, patterns, lessons. Obsidian CLI required for automation (vault syncs, exports, graph generation). Desktop app optional for visualization.
- **Caveman Mode** — Compression for token budget control

**Design Intent:** Spekificity will define HOW these tools integrate and work together via its decorator pattern and enrichment layers. It will not fork or replace them; it will extend their capabilities through composition.

---

## Intended Workflow (4-Stage Design)

Upon completion, Spekificity will implement this workflow:

```
STAGE 1: PREPARE
/spek.prepare (workspace ready, vault synced, lat.md fresh)
    ├─ Pre-flight checks (git state, vault sync, graph fresh)
    └─ Output: Workspace ready, context loaded

STAGE 2: PLAN (2 sub-stages)
/spek.plan
    ├─ Sub-stage 1: Specification — /speckit.specify (write spec + enrichment layers)
    ├─ Sub-stage 2: Task Breakdown — /speckit.plan + /speckit.tasks (create plan + tasks)
    └─ Output: Spec + plan + task breakdown

STAGE 3: IMPLEMENT
/spek.implement (execute tasks in order, write code + tests)
    ├─ Per-task: code changes, tests, validation
    └─ Output: Code committed, tests passing, Success Criteria validated

STAGE 4: CONCLUDE
/spek.conclude (archive outcomes, extract lessons, refresh state)
    ├─ Archive: Spec + plan → vault
    ├─ Learn: Extract lessons, capture decisions + patterns
    ├─ Sync: Refresh lat.md index, update repo memory
    └─ Output: Vault updated, lessons captured, graph fresh, ready for next feature
```

---

## Documentation Guide

### **First-Time Setup (Install & Initialize)**

Follow in order:

1. **[wiki/setup.md](wiki/setup.md)** — Install Spekificity globally, run `spek init` per-project
2. **[wiki/vision.md](wiki/vision.md)** — Understand core design (four pillars, philosophy)
3. **[wiki/architecture.md](wiki/architecture.md)** — How components fit together (vault, lat.md, SpecKit, skills)

### **First Feature Development (Specification → Implementation)**

1. **[wiki/workflow.md](wiki/workflow.md)** — 4-stage workflow: Prepare → Plan → Implement → Conclude
2. **[wiki/skills.md](wiki/skills.md)** — `/spek.*` command reference
3. **[wiki/patterns.md](wiki/patterns.md)** — Reusable patterns for common tasks

### **Daily Work (Reference)**

| Document | Use When |
|----------|----------|
| [wiki/workflow.md](wiki/workflow.md) | Executing a feature (refresh on phase entry) |
| [wiki/skills.md](wiki/skills.md) | Looking up `/spek.*` command syntax |
| [wiki/conventions.md](wiki/conventions.md) | Naming files, directories, specs |
| [wiki/patterns.md](wiki/patterns.md) | Finding a reusable pattern for your task |
| [wiki/decision.md](wiki/decision.md) | Understanding architectural choices |


### **Documentation Structure**

- **`/wiki/`** — Conceptual guidance (vision, philosophy, architecture, workflow, naming)
- **`/specs/`** — Detailed specifications and implementation contracts
- **`/vault/`** — Project memory (decisions, patterns, lessons captured during development)

### **Wiki File Scope Guide**

| File | Scope | When to Read |
|------|-------|--------------|
| **vision.md** | Vision statement, problem/solution, four pillars, design principles | Understand *why* Spekificity exists |
| **vision.md** | Vision statement, philosophy, core principles, four pillars | Understand Spekificity *philosophy* and design intent |
| **architecture.md** | Technical components, data flow, responsibilities (Vault, lat.md, SpecKit, Skills), integration | Understand *how* components fit together technically |
| **workflow.md** | 5-phase feature development workflow with entry/exit criteria, artifacts, detailed steps | Reference during *active development* |
| **quickstart.md** | Hands-on walkthrough for first feature | *Get started* with your first feature |
| **conventions.md** | `/spek.*` and `/speckit.*` command naming patterns and invocation | Know *which command to use* |



### **Terminology Guide**

| Term | Canonical Usage | Aliases | Definition |
|------|-----------------|---------|-----------|
| **Stage** | "Prepare", "Specify & Plan", etc. | "phase", "step" | One of the deterministic workflow stages in feature development |
| **Closeout** | "Post-Feature Closeout" | "Close", "post-processing", "archive phase" | Final phase where artifacts are archived and lessons extracted |
| **Lessons Learned** | "lessons learned", "lessons" (in context of `/spek.conclude` output) | "reflection", "retrospective", "what we learned" | Structured insights captured at feature end (what worked, what didn't, patterns) |
| **lat.md** | "lat.md" (indexer for docs and source) | "indexing tool", "doc-code linkage" | Markdown-native index + source metadata; primary source for context injection |
| **Enrichment Layer** | "enrichment layers" (plural when multiple) | "context layers", "structured context" | Context-specific information added to specs/plans (Success Criteria, Assumptions, Risk Assessment, etc.) |
| **SpecKit** | "SpecKit" or "/speckit.*" commands | "spec framework", "specification tool" | Underlying spec-driven workflow engine (upstream tool, not Spekificity-specific) |

---

## Contributing

Contributions welcome! Please:

1. Create a feature branch from `main`
2. Submit specs and documentation following [wiki/conventions.md](wiki/conventions.md)
3. Include test cases and lessons learned

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Marcel Rienks**

---

## Platform Model (Detailed)

The intended Spekificity workflow is:

1. Install Spekificity globally via `uv tool install ... --from git+...`.
2. Run `spek init` in a target directory.
3. Let `spek init` scaffold `.spek` skills/functions and initialize SpecKit (`specify init`) under the covers.
4. Execute the generated `/spek.*` skills from your agent (or call underlying tools directly when needed).
5. Capture lessons and refresh durable project memory through the generated workflow.

Canonical user-facing command surface is:

- `spek init` — per-project bootstrap command (primary runtime CLI command)
- `spek doctor` / `spek tools` (optional helpers) — dependency checks/status
- Generated `/spek.*` skills in `.spek/` — primary execution interface for agents

Primary workflow is skill-first (agent execution), not direct CLI-phase execution.

Vanilla SpecKit commands remain part of the underlying model:

- `/speckit.specify`
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.analyze`
- `/speckit.tasks`
- `/speckit.implement`

Use the generated `/spek.*` skills when following the Spekificity workflow. **Enrichment** means context injection and tool coordination: skills load decisions/patterns from Obsidian + lat.md and then call `/speckit.*` phases with project-specific constraints already in scope.

Note on notation: `/spek.*` denotes generated agent skills placed in `.spek/` by `spek init`. The user-facing setup CLI is `spek` (primarily `spek init`).

Vanilla SpecKit commands remain the execution layer; Spekificity adds context loading, orchestration, and post-processing around them.


### Specifications by Topic

See [wiki/specs/](wiki/specs/) directory for detailed technical specifications. Key areas:
- Memory architecture (vault, session, lessons)
- Workflow orchestration (prepare, plan, implement, conclude)
- Error handling and recovery
- Integration with SpecKit, lat.md, Obsidian CLI
- Token efficiency and compression

## Repository Layout

Current top-level layout:

```text
spekificity/
├── README.md
├── LICENSE
├── wiki/
│   ├── architecture.md
│   ├── conventions.md
│   ├── decision.md
│   ├── patterns.md
│   ├── setup.md
│   ├── skills.md
│   ├── vision.md
│   ├── workflow.md
│   ├── specs/
│   └── raw/
├── vault/                    [project knowledge: decisions, patterns, lessons]
├── .spek/                    [Spekificity config and generated skills]
├── .git/
└── .gitignore
```

Practical reading order:

1. README (this file)
2. `wiki/vision.md`
3. `wiki/architecture.md`
4. `wiki/workflow.md` (4 main stages)
5. `wiki/conventions.md`
6. `wiki/setup.md` (tool installation)
7. relevant files in `wiki/specs/` for deep dives


## Design Assumptions (Specification Foundation)

This specification consistently assumes these design principles and constraints:

- **Workflow:** 4 main stages (Prepare → Plan [Specification + Task Breakdown] → Implement → Conclude)
- **Command Surface:** Enriched `/spek.*` prefix for all Spekificity skills
- **Integration Pattern:** Spekificity wraps SpecKit via decorator pattern (no fork)
- **Persistence:** Durable knowledge in markdown vault (`vault/`), Git-version-controlled
- **CLI Requirement:** Obsidian CLI required for `/spek.conclude` automation (syncs, exports, graph generation). Desktop app optional for visualization.
- **Code Analysis:** Indexed graph (lat.md MCP tools) as canonical approach, not file scans
- **Learning Loop:** Post-feature lessons (captured in `/spek.conclude`) are core system behavior, not optional add-on

