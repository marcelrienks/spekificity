# Spekificity

> **Status:** Init-first wrapper model. Spekificity is intended to be installed globally via `uv`, then initialized per-project with `spek init` which scaffolds `.spek` skills/functions and configures dependent tools.
>
> **Documentation Structure:** `/wiki/` contains philosophy, architecture, and workflow guidance. `/specs/` contains detailed specifications and implementation contracts.

## What is Spekificity?

Spekificity is a **specification-driven framework for rapid AI agent development**. It solves four critical problems:

| Problem | Solution |
|---------|----------|
| **Token bloat** | Indexed code analysis (lat.md) + scoped context loading |
| **Shallow planning** | Spec-first workflow with enriched validation layers |
| **Context loss** | Persistent knowledge vault (Git-backed Obsidian vault/) |
| **Low autonomy** | Reusable agent skills with deterministic sequencing |

**Value Proposition:** Build features **faster** with deterministic specs, persistent memory, and zero context loss between sessions.

---

## Quick Start


### Prerequisites

- Python 3.11+
- `uv` package manager ([install](https://docs.astral.sh/uv/))
-- **Obsidian CLI** (required for automation) — primary integration for vault automation: syncs, exports, and scripted operations that enable context loading, graph generation, and lesson extraction. Desktop app is optional (used for visualization only).
+    - Why: Spekificity performs scripted vault operations (pull/push, heading/frontmatter export, and JSON/graph exports). Having the `obsidian` CLI in PATH simplifies reliable automation in developer workflows and CI.
+    - Install / enable CLI: Register the `obsidian` command in your PATH. The CLI is typically provided by the Obsidian desktop app, but the CLI is the primary required integration point — the desktop app is optional (used for visualization and interactive workflows). See https://obsidian.md/help/cli and https://obsidian.md/help/headless for platform-specific guidance.

### Installation & Setup (Recommended)

```bash
# 1. Install Spekificity as a tool (installs all dependencies)
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# 2. Initialize your project (sets up infrastructure and runs specify init)
spek init

# 3. Verify installation
spek --help
spek --version
spek tools --list
```


Planned automatic steps:
- Install Spekificity CLI and configured dependencies (SpecKit, lat.md, etc.)
- Create project directories (`.spek/`, `vault/`, `wiki/`)
- Initialize lat.md index and invoke SpecKit initialization
- Verify `obsidian` CLI availability (the automation described here requires the `obsidian` CLI to be installed and registered in PATH)

### Alternative: Manual Installation

```bash
# Clone repository
git clone <repo-url>
cd spekificity

# Install in development mode
pip install -e .

# Initialize project
spek init
```

**Full guide:** See [wiki/setup.md](wiki/setup.md) for detailed setup options.

---

## Key Features

✅ **Spec-Driven Workflow** — All work starts with a structured specification  
✅ **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault  
✅ **Token Efficiency** — Pre-indexed code analysis (lat.md, canonical) + Caveman compression  
✅ **Deterministic Sequencing** — 4-stage workflow (Prepare → Specify & Plan → Implement → Close)  
✅ **Composable Skills** — `/spek.*` commands can be chained or run independently  

---

## Platform Model

Spekificity is built around four pillars:

| Pillar | Goal | Mechanism |
|---|---|---|
| **Token efficiency** | Spend tokens on reasoning, not file rediscovery | indexed graph queries, scoped context loading, Caveman compression |
| **Determinism** | Keep feature work on a repeatable track | SpecKit workflow: specify → plan → tasks → implement |
| **Persistence** | Preserve architectural context across sessions | knowledge vault (markdown store for decisions, patterns, lessons) |
| **Autonomy** | Reduce developer hand-holding | reusable project memory + graph-grounded context injection |

---


## Target Tool Stack

- **SpecKit / Specify** — Spec-driven workflow engine
- **lat.md** — Indexing and doc-code linkage (preferred)
- **Obsidian Vault (with Obsidian CLI)** — Required knowledge store and runtime interface for specs, decisions, patterns, and lessons. The `obsidian` CLI must be available in PATH for automation (vault syncs, metadata exports, graph generation). Desktop app is optional for visualization and interactive workflows.
- **Caveman Mode** — Response compression for token control

Spekificity defines how these tools work together—it doesn't replace them. **The toolset described (SpecKit, lat.md, Obsidian + Obsidian CLI, Caveman) is required for the intended automation and behavior described in this documentation.**

---

## Core Workflow (4 Main Stages)

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

## Documentation Roadmap

### **For First-Time Users**

Start with this reading order—each doc builds on the previous:

1. **[wiki/vision.md](wiki/vision.md)** — Why Spekificity exists and core philosophy (vision, principles, tenets)
2. **[wiki/architecture.md](wiki/architecture.md)** — How components fit together (technical architecture and data flow)
3. **[wiki/workflow.md](wiki/workflow.md)** — 4-stage feature development workflow and lifecycle

### **For Daily Work (Reference)**

| Document | Purpose |
|----------|---------|
| [wiki/workflow.md](wiki/workflow.md) | staged workflow details (reference during development) |
| [wiki/conventions.md](wiki/conventions.md) | Command naming and skill invocation |
| [.spek/skill-index.md](.spek/skill-index.md) | Complete `/spek.*` command reference |


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

## Next Steps

**New to Spekificity?** Start here:

1. Read [wiki/quickstart.md](wiki/quickstart.md)
2. Install globally via `uv tool install ... --from git+...`
3. Run `spek init` in your project directory to scaffold `.spek`
4. Run generated skills through your agent workflow

**Questions?** See [wiki/faq.md](wiki/faq.md).

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

## Current Repository State

This repository is ahead on architectural definition and behind on implementation.

Current state, based on the docs in `wiki/`:

- architecture and workflow intent are documented
- naming conventions for the new command surface are defined
- memory, graph, orchestration, and post-processing behavior are specified in atomic docs
- implementation of agent skills, CLI orchestration, and end-to-end validation is the next major phase

If you are evaluating the project today, treat this repository as the source for design contracts and planned behavior, not as a finished installable product.

## Start Here

Use these documents first:

- [wiki/vision.md](wiki/vision.md) — project vision, philosophy, architecture, and lifecycle framing
- [wiki/conventions.md](wiki/conventions.md) — current command names and directory conventions
- [wiki/workflow.md](wiki/workflow.md) — canonical workflow and Spekificity integration points

## Documentation Map

### Core docs

- [wiki/vision.md](wiki/vision.md)
- [wiki/architecture.md](wiki/architecture.md)
- [wiki/workflow.md](wiki/workflow.md)
- [wiki/conventions.md](wiki/conventions.md)

### Setup notes

- [wiki/setup.md](wiki/setup.md)

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


## Working Assumptions

The docs in this repository consistently assume:

- Workflow uses 4 main stages: Prepare → Plan (2 sub-stages: Specification, Task Breakdown) → Implement → Conclude
- Enriched command surface uses `/spek.*` prefix
- Spekificity wraps SpecKit (decorator pattern) rather than forking it
- Durable knowledge lives in markdown vault (`vault/`), version-controlled via Git
- **Obsidian CLI required for automation:** Vault syncs, metadata exports, graph generation, and lesson extraction depend on `obsidian` CLI in PATH. Desktop app is optional for visualization.
- Code intelligence via indexed graph (lat.md MCP tools) rather than file scans
- Post-feature lessons (captured in `/spek.conclude`) are part of the system, not optional

## Constitution

Project principles are governed by [.specify/memory/constitution.md](.specify/memory/constitution.md).
