# Quickstart: Spekificity Platform

**Date**: 2026-04-29  
**Time to complete**: ~20–30 minutes (first-time setup)

This guide gets you from zero to a running Spekificity-enabled project. Follow the steps in order. Each step is executable by an AI agent or a developer in a terminal.

---

## Prerequisites

Before starting, ensure the following are available:

| Tool | Install command | Verify |
|------|----------------|--------|
| Python 3.11+ | [python.org](https://python.org) | `python3 --version` |
| `uv` (Python package runner) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `uv --version` |
| git | OS package manager | `git --version` |
| GitHub Copilot or Claude Code | AI provider setup | Active in your editor |

---

## Step 1 — Install SpecKit/Specify (Global)

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Verify:
```bash
specify --version
# Expected: specify-cli X.X.X
```

See [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for troubleshooting.

---

## Step 2 — Install Graphify (Global)

```bash
uv tool install graphifyy
```

Verify:
```bash
graphify --version
# Expected: graphifyy X.X.X
```

See [setup-guides/graphify-setup.md](../setup-guides/graphify-setup.md) for troubleshooting.

---

## Step 3 — Initialise Your Project with Specify

Inside your project folder:

```bash
cd /path/to/your/project
specify init .
```

When prompted, select:
- AI assistant: `copilot` or `claude`
- Script type: `sh`

This installs the standard SpecKit workflow into `.github/agents/` and `.specify/`.

---

## Step 4 — Install Spekificity Custom Skills

Clone or copy the Spekificity `skills/` and `workflows/` directories into your project:

```bash
# If using Spekificity as a reference repo:
cp -r /path/to/spekificity/skills ./skills
cp -r /path/to/spekificity/workflows ./workflows
cp -r /path/to/spekificity/setup-guides ./setup-guides
```

For GitHub Copilot — copy skills to agent directory:
```bash
cp skills/map-codebase/SKILL.md .github/agents/map-codebase.agent.md
cp skills/lessons-learnt/SKILL.md .github/agents/lessons-learnt.agent.md
cp skills/context-load/SKILL.md .github/agents/context-load.agent.md
cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
```

For Claude Code — copy skills to commands directory:
```bash
mkdir -p .claude/commands
cp skills/map-codebase/SKILL.md .claude/commands/map-codebase.md
cp skills/lessons-learnt/SKILL.md .claude/commands/lessons-learnt.md
cp skills/context-load/SKILL.md .claude/commands/context-load.md
cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
```

---

## Step 5 — Build the Initial Codebase Map

In your AI chat session:

```
/map-codebase
```

The AI will run `graphify . --obsidian --output vault/graph/` and create:
- `vault/graph/index.md`
- `vault/graph/nodes/*.md`
- `vault/graph/GRAPH_REPORT.md`

For a brand-new empty project, skip this step — return to it once you have source files.

---

## Step 6 — Start a Feature Lifecycle

Your enriched SpecKit workflow is ready. Use these commands in order:

```
/context-load                      ← Load vault context into AI session
/speckit-enrich-specify            ← Write spec (graph-aware)
/speckit-enrich-plan               ← Write plan (graph-aware)
/speckit.tasks                     ← Generate tasks (standard SpecKit)
/speckit-enrich-implement          ← Implement + auto-update vault
```

Or use standard SpecKit commands directly — Spekificity is additive:
```
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
```

---

## Step 7 — Reduce Tokens with Caveman

At any point in a session, activate Caveman mode:
```
/caveman
```

For workflow steps that require structured output (specs, plans), use lite mode to avoid over-compression:
```
/caveman lite
```

---

## Updating Components Independently

| Component | Update Command | Spekificity changes needed |
|-----------|---------------|---------------------------|
| SpecKit | `uv tool upgrade specify-cli` | None (unless SpecKit command interface changed) |
| Graphify | `uv tool upgrade graphifyy` | Update `skills/map-codebase/SKILL.md` if CLI args changed |
| Obsidian app | Download from obsidian.md | None (vault is plain markdown) |
| Spekificity skills | `git pull` in Spekificity repo → re-copy skills | Run Step 4 again |

---

## Obsidian App (Optional)

Obsidian is **not required** for the Spekificity workflow. The vault is plain markdown — AI agents read it directly.

If you want a visual graph browser:
1. Download Obsidian from [obsidian.md](https://obsidian.md)
2. Open Obsidian → Open folder as vault → select your project's `vault/` directory
3. Use the Graph View to visualise node relationships

See [setup-guides/obsidian-setup.md](../setup-guides/obsidian-setup.md) for details.
