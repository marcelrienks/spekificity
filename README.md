# Spekificity

> ⚠️ **Status**: Under active development. APIs and documentation subject to change.

**An agentic focused toolset** that connects various tools like [Graphify](https://github.com/graphify/graphifyy), [Obsidian](https://obsidian.md), [SpecKit/Specify](https://github.com/github/spec-kit), and the [Caveman skill](https://github.com/marcelrienks/.agents/skills/caveman) together to create a persistent AI context, reduce excessive token consumption, and improve shallow feature planning. Delivered as markdown skills, workflows, and setup guides that AI agents execute to run enriched SpecKit feature lifecycles with persistent context.

Spekificity is **built for AI agents**. Every artefact is a skill or workflow that an AI agent reads and executes—enabling code generation, artifact creation, and automation through agentic orchestration.

---

## What it does

| Capability | How |
|------------|-----|
| Codebase mapping | Runs Graphify to build an Obsidian vault graph of all source files and docs |
| Graph-first context loading | Loads vault index at session start — AI answers cross-cutting questions without re-scanning all files |
| Enriched SpecKit lifecycle | Decorates `/speckit.specify`, `/speckit.plan`, `/speckit.implement` with graph-aware context |
| Persistent lessons learnt | Writes structured lessons to the vault after every feature; surfaced in future sessions |
| Token efficiency | Caveman mode integration at every workflow step |

---

## Prerequisites

| Tool | Install | Mode |
|------|---------|------|
| Python 3.11+ | [python.org](https://python.org) | system |
| `uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | global |
| git | OS package manager | global |
| SpecKit/Specify | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | global |
| Graphify | `uv tool install graphifyy` | global |
| GitHub Copilot or Claude Code | AI provider setup | editor |
| Obsidian (optional) | [obsidian.md](https://obsidian.md) | desktop, visualization only |

---

## Full Feature Lifecycle

For the complete enriched SpecKit workflow step-by-step, see [docs/guide.md](docs/guide.md).

---

## Design Principles

- **Decorator pattern**: Spekificity skills wrap, not replace, standard SpecKit commands
- **Modular independence**: Each component (Graphify, Obsidian, SpecKit, Spekificity layer) can be updated independently
- **Global SpecKit, local customisation**: SpecKit installs globally; Spekificity skills install locally per-project

---

## Documentation

- [docs/architecture.md](docs/architecture.md) — Directory structure, component roles, data flow, update strategy
- [docs/guide.md](docs/guide.md) — Full feature lifecycle workflow, enriched SpecKit lifecycle
- [docs/glossary.md](docs/glossary.md) — Terminology reference
- [docs/faq.md](docs/faq.md) — Troubleshooting and common questions
- [docs/validation.md](docs/validation.md) — Success criteria validation methodology

---

## Core Problems Solved

1. **Context loss between sessions** — AI agents have no persistent memory of past decisions. Spekificity stores decisions, patterns, and lessons in an Obsidian vault that agents can read at session start.
2. **High token consumption** — Agents typically read every file recursively to understand a codebase. Spekificity indexes the codebase as a graph, replacing recursive file scans with targeted vault queries (40%+ token savings).
3. **Shallow SpecKit lifecycle** — SpecKit lacks awareness of existing code structure. Spekificity decorates SpecKit steps with graph-aware skills that ground specs and plans in reality.
4. **Verbose AI interactions** — Agents are verbose by default. Caveman mode compresses responses 60%+ without losing technical accuracy.

---

## Session Start (Required)

> **Always run `/context-load` before any feature work.** This loads the Obsidian vault graph, architectural decisions, patterns, and recent lessons into working memory.

```
/context-load
```

---

## Available Skills

| Command | Description |
|---------|-------------|
| `/context-load` | Load vault context (graph, decisions, patterns, lessons) into AI session |
| `/map-codebase` | Run Graphify to build or refresh the Obsidian vault graph |
| `/lessons-learnt` | Write structured lessons to the vault at the end of a feature |
| `/speckit-enrich-specify` | Graph-aware decorator for `/speckit.specify` |
| `/speckit-enrich-plan` | Graph-aware decorator for `/speckit.plan` |
| `/speckit-enrich-implement` | Graph-aware decorator for `/speckit.implement` — automatically runs lessons + map update |

---

## Token Efficiency

Activate caveman mode to reduce response verbosity and token consumption:

```
/caveman lite      ← for spec/plan work (preserves structure)
/caveman           ← for implementation sessions (full compression)
```

---

## Getting Started (MVP v1.0.0)

The spekificity platform is now ready for use! Use the unified `spek` command for setup and initialization.

### 5-Minute Setup

```bash
# 1. Setup environment (check prerequisites)
.spekificity/bin/spek setup

# 2. Initialize platform (orchestrate all tools)
.spekificity/bin/spek init

# 3. Verify installation
.spekificity/bin/spek status

# 4. Load context (in AI chat)
/context-load

# 5. Start feature work
/speckit-enrich-specify
```

**See**: [.spekificity/guides/quickstart.md](.spekificity/guides/quickstart.md) for full 5-minute guide with expected output.

### For New Team Members

```bash
# Clone project
git clone <repo>
cd <project>

# One-time setup
.spekificity/bin/spek setup && .spekificity/bin/spek init

# Ready for feature work (~10 minutes total)
/context-load
```

### Available Commands

**Platform Management**:
| Command | Purpose |
|---------|---------|
| `spek setup` | Verify prerequisites and prepare environment |
| `spek init` | Initialize all tools (speckit, graphify, obsidian, caveman) |
| `spek status` | Show initialization status and tool versions |
| `spek update` | Update spekificity custom layer (Phase 6) |

**AI Skills** (in your chat):
| Command | Purpose |
|---------|---------|
| `/spek.context-load` | Load codebase graph and vault context |
| `/spek.map-codebase` | Update codebase analysis graph |
| `/spek.lessons-learnt` | Capture learning after feature completion |
| `/speckit.specify` | Create feature specification |
| `/speckit.plan` | Create implementation plan |
| `/speckit.tasks` | Generate actionable tasks |
| `/speckit.implement` | Execute implementation tasks |

---

## Documentation Guide

**Start here**: [README.md](README.md) (you are here)

### Getting Help
- **Quick setup**: [.spekificity/guides/quickstart.md](.spekificity/guides/quickstart.md) — 5 minutes
- **Troubleshooting**: [.spekificity/guides/troubleshooting.md](.spekificity/guides/troubleshooting.md) — Common errors & solutions
- **Manual setup**: [.spekificity/guides/manual-setup.md](.spekificity/guides/manual-setup.md) — Step-by-step for restricted environments
- **Integration**: [.spekificity/guides/integration-guide.md](.spekificity/guides/integration-guide.md) — Team workflows & CI/CD

### Learn More
- **Architecture**: [.spekificity/guides/architecture.md](.spekificity/guides/architecture.md) — Component design & extension points
- **Orchestration**: [.spekificity/guides/orchestration-model.md](.spekificity/guides/orchestration-model.md) — How tools are coordinated
- **Migration**: [.spekificity/guides/migration.md](.spekificity/guides/migration.md) — Adopting spekificity in existing projects
- **Skill Development**: [.spekificity/guides/skill-development.md](.spekificity/guides/skill-development.md) — Create custom skills
- **Feature Lifecycle**: [workflows/feature-lifecycle.md](workflows/feature-lifecycle.md) — Full workflow overview
- **Understand the project**: Read [docs/readme.md](docs/readme.md) (quick start, problems, goals)
- **Detailed workflows**: [docs/guide.md](docs/guide.md) — feature lifecycle and operations
- **Run into issues**: Check [docs/faq.md](docs/faq.md)

**Daily usage**: [workflows/feature-lifecycle.md](workflows/feature-lifecycle.md) — complete enriched SpecKit workflow

**Reference**: [docs/glossary.md](docs/glossary.md) — terminology, [docs/architecture.md](docs/architecture.md) — component design

---

## Project Structure

```
spekificity/
├── skills/                        ← AI skill files (agent-agnostic)
│   ├── map-codebase/SKILL.md
│   ├── lessons-learnt/SKILL.md
│   ├── context-load/SKILL.md
│   └── speckit-enrich/
│       ├── specify-enrich.md
│       ├── plan-enrich.md
│       └── implement-enrich.md
├── workflows/                     ← Multi-step workflow guides
│   ├── init-workflow.md
│   ├── feature-lifecycle.md
│   ├── map-refresh.md
│   └── component-update.md
├── setup-guides/                  ← Per-tool install guides
│   ├── graphify-setup.md
│   ├── speckit-setup.md
│   └── obsidian-setup.md
├── vault/                         ← Obsidian vault (runtime artefact)
│   ├── graph/                     ← Generated by /map-codebase
│   ├── lessons/                   ← Written by /lessons-learnt
│   └── context/                   ← Maintained by AI across sessions
│       ├── decisions.md
│       └── patterns.md
└── docs/                          ← Project documentation
    ├── readme.md
    ├── architecture.md
    ├── guide.md
    ├── glossary.md
    ├── faq.md
    └── validation.md
```

---

## Updating Components Independently

Each component can be updated without touching the others:

| Component | Update command | Spekificity changes needed? |
|-----------|---------------|----------------------------|
| SpecKit/Specify | `uv tool upgrade specify-cli` | Only if SpecKit command interface changes |
| Graphify | `uv tool upgrade graphifyy` | Only if CLI args change (update `skills/map-codebase/SKILL.md`) |
| Obsidian | Download new app version | None — vault format is stable markdown |
| Spekificity custom layer | `git pull` + re-copy skills | Re-copy to `.github/agents/` and `.claude/commands/` |

See [workflows/component-update.md](workflows/component-update.md) for full update procedures.

---

## Constitution

This project is governed by [.specify/memory/constitution.md](.specify/memory/constitution.md).  
Core principles: Skills-not-code · Decorator pattern · Modular independence · Graph-first context · Token efficiency by design.
