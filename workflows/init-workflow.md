# Workflow: First-Time Project Initialisation

## Purpose

Get a developer from zero to a fully operational Spekificity-enabled project. After completing this workflow, all tools are installed, all custom skills are active in the AI agent, and the developer can immediately begin a SpecKit feature lifecycle with graph-aware context.

**Time to complete**: ~10 minutes for tool installation; ~20–30 minutes total including first map build.

> **Token efficiency tip**: Activate `/caveman lite` before starting this workflow to compress AI confirmation messages without losing step accuracy.

## Prerequisites

Before starting, verify:

| Check | Command | Expected |
|-------|---------|----------|
| Python 3.11+ | `python3 --version` | `Python 3.11.x` or higher |
| `uv` installed | `uv --version` | any version string |
| `git` installed | `git --version` | any version string |
| AI agent active | (in editor) | GitHub Copilot or Claude Code connected |

If `uv` is not installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Step 1 — Install SpecKit/Specify (Global)

> **Idempotency check**: If `specify --version` already returns a version, skip to Step 2.

```bash
specify --version 2>/dev/null && echo "Already installed — skip to Step 2" || \
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Verify:
```bash
specify --version
# Expected: specify-cli X.X.X (≥ 0.8.0)
```

See [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for troubleshooting.

---

## Step 2 — Install Graphify (Global)

> **Idempotency check**: If `graphify --version` already returns a version, skip to Step 3.

```bash
graphify --version 2>/dev/null && echo "Already installed — skip to Step 3" || \
  uv tool install graphifyy
```

Verify:
```bash
graphify --version
# Expected: graphifyy X.X.X (≥ 0.5.5)
```

See [setup-guides/graphify-setup.md](../setup-guides/graphify-setup.md) for troubleshooting.

---

## Step 3 — Initialise SpecKit in Your Project

> **Idempotency check**: If `.specify/` already exists in your project, skip to Step 4.

```bash
cd /path/to/your/project

ls .specify/ 2>/dev/null && echo "Already initialised — skip to Step 4" || specify init .
```

When `specify init .` prompts:
- **AI assistant**: `copilot` (GitHub Copilot) or `claude` (Claude Code)
- **Script type**: `sh`

This creates `.specify/`, `.github/agents/`, and `.github/copilot-instructions.md`.

See [setup-guides/speckit-setup.md](../setup-guides/speckit-setup.md) for configuration details.

---

## Step 4 — Install Spekificity Custom Skills

> **Idempotency check**: Run the copy commands with `-n` (no-overwrite) to skip existing files, or `-f` to update.

**Copy skill library directories into your project**:
```bash
cp -r /path/to/spekificity/skills ./skills
cp -r /path/to/spekificity/workflows ./workflows
cp -r /path/to/spekificity/setup-guides ./setup-guides
```

**For GitHub Copilot** — distribute to agent directory:
```bash
mkdir -p .github/agents
cp skills/map-codebase/SKILL.md .github/agents/map-codebase.agent.md
cp skills/lessons-learnt/SKILL.md .github/agents/lessons-learnt.agent.md
cp skills/context-load/SKILL.md .github/agents/context-load.agent.md
cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
```

**For Claude Code** — distribute to commands directory:
```bash
mkdir -p .claude/commands
cp skills/map-codebase/SKILL.md .claude/commands/map-codebase.md
cp skills/lessons-learnt/SKILL.md .claude/commands/lessons-learnt.md
cp skills/context-load/SKILL.md .claude/commands/context-load.md
cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
```

Verify (Copilot example):
```bash
ls .github/agents/ | grep -E "map-codebase|lessons|context-load|speckit-enrich"
# Expected: 6 files listed
```

---

## Step 5 — Initialise the Vault Context Structure

> **Idempotency check**: If `vault/context/decisions.md` already exists, skip to Step 6.

Copy the vault context placeholder files:
```bash
cp -r /path/to/spekificity/vault/context ./vault/context
```

Or create them manually:
```bash
mkdir -p vault/context vault/lessons vault/graph/nodes
cp /path/to/spekificity/vault/context/decisions.md vault/context/decisions.md
cp /path/to/spekificity/vault/context/patterns.md vault/context/patterns.md
```

---

## Step 6 — Build the Initial Codebase Map

> **Skip if**: Your project has fewer than 5 source files or is brand new. Return to this step once you have meaningful source files.

In your AI chat session, invoke:
```
/map-codebase
```

The AI will run `graphify . --obsidian --output vault/graph/` and create:
- `vault/graph/index.md` — master node list
- `vault/graph/nodes/` — one file per code/doc node
- `vault/graph/GRAPH_REPORT.md` — human/AI-readable summary

See [workflows/map-refresh.md](map-refresh.md) for when to re-run this step.

---

## Step 7 — Verify Installation

Run each of the following checks:

```bash
# Tools
specify --version     # ≥ 0.8.0
graphify --version    # ≥ 0.5.5

# SpecKit
ls .specify/          # extensions.yml  memory/  scripts/  templates/

# Spekificity skills (choose your agent)
ls .github/agents/    # should include map-codebase.agent.md etc.
ls .claude/commands/  # should include map-codebase.md etc.

# Vault
ls vault/             # graph/  lessons/  context/
ls vault/context/     # decisions.md  patterns.md
```

In your AI chat session, verify the agent can read the skill:
```
/context-load
# Expected: "Context loaded. X graph nodes, Y decisions, Z patterns. Ready."
```

---

## Step 8 — Next Steps

Installation complete. Your enriched SpecKit workflow is ready:

```
/context-load                      ← Load vault context (run at start of every session)
/speckit-enrich-specify            ← Start a new feature (graph-aware spec)
/speckit-enrich-plan               ← Plan the feature (graph-aware plan)
/speckit.tasks                     ← Generate tasks (standard SpecKit)
/speckit-enrich-implement          ← Implement + auto-update vault + lessons
```

See [workflows/feature-lifecycle.md](feature-lifecycle.md) for the full enriched workflow.

---

## Decision Points

| Situation | Action |
|-----------|--------|
| `specify --version` already ≥ 0.8.0 | Skip Step 1 |
| `graphify --version` already ≥ 0.5.5 | Skip Step 2 |
| `.specify/` already exists | Skip Step 3 |
| Skill files already in `.github/agents/` | Skip/update Step 4 |
| Project has no source files yet | Skip Step 6; run `/map-codebase` later |
| Using Claude Code only | Skip Copilot copy commands in Step 4 |
| Using GitHub Copilot only | Skip Claude copy commands in Step 4 |

## Recovery from Partial Failures

- **Failure in Step 1–2 (install)**: Re-run the install command; `uv tool install` is idempotent
- **Failure in Step 3 (specify init)**: Run `specify init .` again; it will not overwrite your constitution
- **Failure in Step 4 (skill copy)**: Re-run the `cp` commands; use `-f` to overwrite stale copies
- **Failure in Step 6 (map-codebase)**: Check `graphify --version` first; see error handling in [skills/map-codebase/SKILL.md](../skills/map-codebase/SKILL.md)
