# 🔧 Spekificity
**Specification-Driven Agent Development Framework** — Connects the tools you're already using.

It orchestrates **SpecKit** (structured planning) + **lat.md** (code indexing—no manual search) + **Obsidian vault** (decision history) + **Caveman** mode (token efficiency) into one workflow. 

**No new concepts.** Just less friction: setup in minutes, straightforward commands, spec-first procedures that eliminate context-switching.

The heavy lifting comes from best-in-class tools. What we built is the **glue**: one setup, clear procedures, and an opinionated workflow that makes them work together instead of in silos. 🧩

---

## Quick Start (5 Minutes)

```bash
# 1. Install globally (one time)
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# 2. Set up a project
cd /path/to/your/project
git init && spek init

# 3. Prepare for a feature
spek prepare "Your feature name"

# 4. Generate a plan
spek plan "Your feature description"

# 5. Start building
spek implement --task T1.1
```

**Next:** Read [Quick Start Workflow](#quick-start-workflow) for detailed walkthrough, or [wiki/vision.md](wiki/vision.md) for design philosophy.

---

## Key Features

- **Spec-Driven Workflow** — All work starts with structured specification
- **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault
- **Token Efficiency** — Pre-indexed code analysis (lat.md) + Caveman compression
- **Deterministic Sequencing** — 4-stage workflow (Prepare → Plan → Implement → Conclude)
- **Composable Skills** — `/spek.*` commands designed to be chainable or independently runnable

---

## Requirements

Minimal dependencies — all standard tools:

- **Python 3.11+** — Check with `python3 --version`
- **`uv` package manager** — [Quick install](https://docs.astral.sh/uv/)
- **Git** — Already initialized in your project
- **Obsidian CLI** — *(Optional)* Only needed for vault graph exports

All other dependencies install automatically via `uv tool install`.

---

## Installation

### Global Installation (One-Time)

```bash
# Install Spekificity globally (auto-installs all dependencies)
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# Verify installation
spek --version
spek --help
```

**Result:** All tools installed. Ready for per-project setup.

### Per-Project Setup (One-Time Per Project)

```bash
cd /path/to/your/project
git init  # If not already a git repo
spek init
```

**Creates:**
- `.specify/` — SpecKit per-project configuration
- `specs/` — Feature specifications directory
- `vault/` — Project knowledge store (decisions, patterns, lessons)
- `.lat/` — Code index directory
- `.github/agents/skills/` — Agent skill definitions

**Result:** Project ready for feature development.

### Alternative: Development Installation

```bash
git clone <repo-url>
cd spekificity
pip install -e .
cd /path/to/your/project
spek init
```

---

## Quick Start Workflow

### Stage 1: Prepare for Feature

```bash
spek prepare "User Authentication API"
```

**Output:** Onboarding report with:
- Relevant prior decisions from vault
- Design patterns and conventions
- Relevant code sections
- Token usage estimate

**SLA:** < 30 seconds

### Stage 2: Generate Specification & Plan

```bash
spek plan "Build JWT-based authentication for REST API"
```

**Creates:**
- `specs/001-auth-api/spec.md` — Feature specification
- `specs/001-auth-api/plan.md` — Implementation plan
- `specs/001-auth-api/tasks.md` — Task breakdown

**Process:**
1. Generate spec from description
2. Identify and clarify ambiguities
3. Generate implementation plan
4. Break down into tasks

**SLA:** < 3 minutes

### Stage 3: Execute Tasks

```bash
spek implement --task T1.1
```

**Process:**
1. Load task context (decisions, patterns, code)
2. Inject context into agent session
3. Execute task with progress tracking
4. Log decisions made
5. Mark task complete

**SLA:** < 30 minutes per task (with well-scoped task)

### Stage 4: Conclude & Extract Lessons

```bash
spek conclude --feature auth-api
```

**Process:**
1. Analyze actual outcomes vs. success criteria
2. Extract lessons learned
3. Identify new patterns
4. Update vault (decisions, patterns, lessons)
5. Refresh code index

**Output:** Lessons document, vault updates, feature archive

**SLA:** < 5 minutes

---

## Command Reference

### Installation & Setup

```bash
spek --version                 # Show version
spek --help                    # Show help for all commands
spek init                      # Initialize Spekificity in project
spek install                   # Verify dependencies
```

### Feature Workflow

```bash
spek prepare [FEATURE_NAME]              # Load context, index codebase
spek plan [FEATURE_DESCRIPTION]          # Generate spec, plan, tasks
spek implement --task TASK_ID             # Execute task with context
spek conclude --feature FEATURE_NAME      # Analyze, extract lessons, update vault
```

### Options

- `--verbose` — Detailed output
- `--debug` — Include stack traces
- `--color` — Colored output (default: auto)

---

## Vault Structure

```
vault/
├── decisions.md                # Architectural decisions (append-only)
├── patterns.md                 # Reusable patterns & conventions
├── lessons.md                  # Lessons learned summary
└── lessons/                    # Individual lesson files (auto-created)
    ├── 2026-06-07-auth-api.md
    ├── 2026-06-14-user-service.md
    └── ...
```

### decisions.md

Records architectural decisions:

```yaml
---
id: dec-001
title: Use JWT for authentication
status: approved
date: 2026-06-07
author: team
---

## Problem
Need scalable stateless auth for REST API.

## Decision
Use JWT tokens with HS256 signing.

## Rationale
- Stateless (scales to many servers)
- Standard (wide library support)

## Implications
- Must handle token expiration
- Requires refresh token strategy
```

### patterns.md

Reusable solutions:
- ID (pat-001, pat-002, ...)
- Category (Architecture, Workflow, Testing, etc.)
- Problem & solution
- Examples & usage guidelines

### lessons/ (Individual Feature Files)

Auto-created by `/spek.conclude`:
- Filename: `YYYY-MM-DD-feature-name.md`
- Contains outcomes, lessons, patterns, decisions

---

## Integrated Tool Stack

Spekificity integrates (not replaces) these tools:

- **SpecKit** — Spec-driven workflow engine
- **lat.md** — Code indexing and BM25 analysis
- **Obsidian Vault + CLI** — Knowledge store and graph generation
- **Caveman Mode** — Token-efficient output compression

---

## Design Pillars

Spekificity is built around four pillars:

| Pillar | Design Goal | Mechanism |
|---|---|---|
| **Token efficiency** | Spend tokens on reasoning, not file rediscovery | Indexed graph queries, scoped context loading, Caveman compression |
| **Determinism** | Keep feature work on repeatable, auditable track | SpecKit workflow: specify → plan → tasks → implement |
| **Persistence** | Preserve architectural context across sessions | Knowledge vault (markdown store for decisions, patterns, lessons) |
| **Autonomy** | Reduce developer hand-holding | Reusable project memory + graph-grounded context injection |

---

## Documentation

### First-Time Setup

1. **Install Globally:** `uv tool install spekificity --from git+...`
2. **Read:** [wiki/vision.md](wiki/vision.md) — Understand core design (four pillars, philosophy)
3. **Read:** [wiki/architecture.md](wiki/architecture.md) — How components fit together

### First Feature Development

1. **Workflow:** [wiki/workflow.md](wiki/workflow.md) — 4-stage workflow with entry/exit criteria
2. **Skills Reference:** [wiki/skills.md](wiki/skills.md) — `/spek.*` command reference
3. **Patterns:** [wiki/patterns.md](wiki/patterns.md) — Reusable patterns for common tasks

### Daily Reference

| Document | Use When |
|----------|----------|
| [wiki/workflow.md](wiki/workflow.md) | Executing a feature |
| [wiki/skills.md](wiki/skills.md) | Looking up `/spek.*` command syntax |
| [wiki/conventions.md](wiki/conventions.md) | Naming files, directories, specs |
| [wiki/patterns.md](wiki/patterns.md) | Finding a reusable pattern |
| [wiki/decision.md](wiki/decision.md) | Understanding architectural choices |

---

## Troubleshooting

### "spek: command not found"

```bash
# Verify installation
uv tool list | grep spekificity

# Reinstall
uv tool uninstall spekificity
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

### "Not a git repository"

```bash
# Initialize git first
cd /path/to/project
git init
git config user.email "you@example.com"
git config user.name "Your Name"
spek init
```

### "Module not found: click, pydantic, etc."

```bash
# Reinstall with dependencies
uv tool uninstall spekificity
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git --force
```

### lat.md queries timing out

```bash
# lat.md is optional for /spek.prepare
# Framework falls back to semantic search if timeout
# Manually sync if needed:
lat sync --project=. --full
```

---

## Examples

### Example 1: Simple Feature

```bash
# Prepare
spek prepare "Add dark mode toggle"

# Plan
spek plan "Add dark mode toggle to user settings"

# Implement tasks
spek implement --task T1.1
spek implement --task T1.2
spek implement --task T1.3

# Conclude
spek conclude dark-mode
```

### Example 2: Complex Feature

```bash
# Prepare with specific branch
spek prepare api-v2

# Plan in-depth
spek plan "Redesign REST API for v2.0"

# Execute tasks
for task in T1.1 T1.2 T1.3 T1.4 T1.5; do
  spek implement --task $task
done

# Conclude and extract patterns
spek conclude api-v2
```

---

## Repository Layout

```text
spekificity/
├── README.md                   # This file
├── LICENSE
├── CLAUDE.md                   # Project instructions
├── wiki/                       # Documentation
│   ├── architecture.md
│   ├── conventions.md
│   ├── decision.md
│   ├── patterns.md
│   ├── setup.md
│   ├── skills.md
│   ├── vision.md
│   └── workflow.md
├── specs/                      # Feature specifications
│   └── 001-complete-framework/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── spekificity/                # Python package
│   ├── __init__.py
│   ├── cli/                    # CLI commands
│   ├── core/                   # Core logic
│   ├── skills/                 # Agent skills
│   ├── integrations/           # External tool integrations
│   ├── templates/              # Default templates
│   └── tests/                  # Test suite
├── vault/                      # Project knowledge (decisions, patterns, lessons)
├── .spek/                      # Spekificity config
├── .github/
│   └── agents/
│       └── skills/             # Agent skill definitions
└── .git/
```

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

## Next Steps

1. **Install:** `uv tool install spekificity --from git+...`
2. **Initialize:** `cd /your/project && spek init`
3. **Start:** `spek prepare "Your Feature Name"`
4. **Learn:** Read [wiki/vision.md](wiki/vision.md) and [wiki/workflow.md](wiki/workflow.md)
5. **Build:** Execute your first feature using the 4-stage workflow

**Documentation Status**: Production ready ✓
**Last Updated**: 2026-06-07
