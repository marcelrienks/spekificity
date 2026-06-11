
<p align="center">
  <img src="spekificity/assets/logo.png" alt="Spekificity Logo" width="100%">
</p>

Spekificity is a spec-driven agent development framework that ties persistent knowledge (Obsidian vault), code analysis (lat.md), workflow automation (SpecKit), and skill execution into a cohesive system. It enables rapid, deterministic feature development by treating documentation as canonical memory, using a pre-indexed code graph for precise context, and orchestrating feature work with a spec-first workflow — eliminating context loss between sessions, token waste from file scanning, and work without durable specifications or lessons.

The heavy lifting comes from best-in-class tools. What we built is the **glue**: one setup, clear procedures, and an opinionated workflow that makes them work together instead of in silos.

---

## Quick Start (5 Minutes)

**Step 1: Install prerequisites** (manual — everything else is auto-installed by `spek init`)

- **Python 3.11+** — `python3 --version`
- **`uv`** — [astral.sh/uv](https://docs.astral.sh/uv/)
- **Node.js 22+** — [nodejs.org](https://nodejs.org/en/download/)
- **Git** — initialized in your project (`git init` if needed)

**Step 2: Install `spek` CLI (one time)**
```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

**Step 3: Initialize your project**
```bash
cd /path/to/your/project
spek init
# Select AI agent integration when prompted (claude, copilot, gemini, cursor-agent, windsurf, cline, codex, kiro-cli, amp, qwen, generic)
```

`spek init` auto-installs SpecKit, lat.md, and Obsidian if not already present.

**Step 4–7: Run in your AI agent** (Claude Code, Copilot, etc.)
```
/spek.prepare
/spek.plan "Your feature description"
/spek.implement
/spek.conclude
```

> **Note:** Steps 4–7 are agent skills, not CLI commands. `spek init` installs them into your project. Only `spek init` runs in the terminal.

**Next:** Read [wiki/workflow.md](wiki/workflow.md) for the 4-stage feature workflow.

---

## Key Features

- **Spec-Driven Workflow** — All work starts with structured specification
- **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault
- **Token Efficiency** — Pre-indexed code analysis (lat.md) + Caveman compression
- **Deterministic Sequencing** — 4-stage workflow (Prepare → Plan → Implement → Conclude)
- **Composable Skills** — `/spek.*` commands designed to be chainable or independently runnable
- **11 Agent Integrations** — Claude Code, Copilot, Gemini, Cursor, Windsurf, Cline, Codex, Kiro, Amp, Qwen, generic
- **Anti-Sycophancy Validation** — Detects spec contradictions and AI drift against vault history
- **Backprop Reflex** — Captures test failure patterns into vault automatically

---

## Requirements

Minimal prerequisites — all standard tools:

- **Python 3.11+** — Check with `python3 --version`
- **`uv` package manager** — [Quick install](https://docs.astral.sh/uv/)
- **Node.js 22+** — Required by lat.md; check with `node --version`
- **Git** — Initialized in your project (`git init` if needed)

All other dependencies (SpecKit, lat.md, Obsidian) are auto-installed by `spek init`.

---

## Installation

Global install (one-time):
```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

Per-project setup:
```bash
cd /path/to/your/project && spek init
```

**Detailed setup:** [wiki/setup.md](wiki/setup.md)

---

**Full workflow details and command reference:** See [wiki/workflow.md](wiki/workflow.md) and [wiki/skills.md](wiki/skills.md).

### All Available Skills

| Skill | When to use |
|-------|-------------|
| `/spek.prepare` | Start of every feature — sync indexes, load vault context |
| `/spek.plan` | Orchestrate spec → plan → tasks with user review |
| `/spek.implement` | Execute approved tasks; write code and tests |
| `/spek.conclude` | Post-implementation: lessons, vault archive, index refresh |
| `/spek.lessons` | Extract lessons at any checkpoint (also auto-called by conclude) |
| `/spek.context` | Load vault decisions, patterns, and memory into session |
| `/spek.map` | Query code graph and vault for a topic's dependencies |
| `/spek.blind-review` | Context-free quality pass (optional, run before archiving) |
| `/spek.rarv` | Detect and resolve spec drift (optional, for complex features) |

---

## Documentation

### First-Time Setup

1. **Install Globally:** `uv tool install spekificity --from git+...`
2. **Read:** [wiki/architecture.md](wiki/architecture.md) — How components fit together

### First Feature Development

1. **Workflow:** [wiki/workflow.md](wiki/workflow.md) — 4-stage workflow with entry/exit criteria
2. **Skills Reference:** [wiki/skills.md](wiki/skills.md) — `/spek.*` command reference

### Daily Reference

| Document | Use When |
|----------|----------|
| [wiki/workflow.md](wiki/workflow.md) | Executing a feature |
| [wiki/skills.md](wiki/skills.md) | Looking up `/spek.*` command syntax |
| [wiki/conventions.md](wiki/conventions.md) | Naming files, directories, specs |
| [wiki/decision.md](wiki/decision.md) | Understanding architectural choices |

---

## Next Steps

1. **Install prerequisites:** Python 3.11+, uv, Node.js 22+, git
2. **Install CLI:** `uv tool install spekificity --from git+...`
3. **Initialize:** `cd /your/project && spek init` (select agent integration type)
4. **Learn:** Read [wiki/workflow.md](wiki/workflow.md) and [wiki/skills.md](wiki/skills.md)
5. **Build:** Run `/spek.prepare` in your agent → 4-stage workflow begins
