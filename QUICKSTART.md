# Spekificity Installation & Quick Start

## Prerequisites

- **Python 3.11+** — Check with `python3 --version`
- **Git** — Version control (check with `git --version`)
- **uv** — Fast Python package manager (install from [astral-sh/uv](https://github.com/astral-sh/uv))

## Installation

### Option 1: From GitHub (Recommended)

```bash
# Install Spekificity globally
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git

# Verify installation
spek --version
```

This automatically installs all dependencies:
- SpecKit (spec → plan → implement orchestration)
- Pydantic (type contracts)
- Click (CLI framework)
- GitPython (git operations)
- Obsidian CLI (vault operations)

### Option 2: From Source (Development)

```bash
git clone https://github.com/marcelrienks/spekificity.git
cd spekificity
pip install -e ".[dev]"
spek --version
```

## Per-Project Setup

Initialize Spekificity in your project:

```bash
cd /path/to/your/project
git init  # If not already a git repo
spek init
```

This creates:
- `vault/` — Knowledge vault (decisions, patterns, lessons)
- `.spek/` — Spekificity configuration and skills
- `specs/` — Feature specifications directory
- `.specify/` — SpecKit per-project configuration

## Quick Start Workflow

### 1. Prepare for Feature

```bash
spek prepare "User Authentication API"
```

Loads:
- Prior architectural decisions from vault
- Design patterns and conventions
- Current codebase state via lat.md index
- Relevant lessons from past features

Output: Onboarding report with navigation guide

### 2. Generate Specification & Plan

```bash
spek plan "Build JWT-based authentication for REST API"
```

Creates:
- `specs/001-auth-api/spec.md` — Feature specification
- `specs/001-auth-api/plan.md` — Implementation plan
- `specs/001-auth-api/tasks.md` — Task breakdown

Output: Spec + plan + tasks ready for implementation

### 3. Execute Tasks

```bash
spek implement T1.1
```

Injects context (decisions, patterns, code) and:
- Executes the task
- Tracks progress
- Logs decisions made
- Updates progress log

### 4. Conclude & Extract Lessons

```bash
spek conclude auth-api
```

Analyzes:
- What was built vs. what was planned
- Lessons learned
- New patterns discovered
- New architectural decisions

Updates vault with knowledge for next feature.

## Command Reference

### `spek --help`

Show help for all commands.

### `spek --version`

Show version and exit.

### `spek init`

Initialize Spekificity in current project.

**When to use:** Once per project, after `git init`

### `spek prepare [FEATURE_NAME]`

Onboard to feature and load prior context.

**Options:**
- `FEATURE_NAME` (optional) — Feature name or branch name

**Output:** Onboarding report with:
- Relevant prior decisions
- Design patterns
- Related code sections
- Token usage estimate

**SLA:** < 30 seconds

### `spek plan [FEATURE_DESCRIPTION]`

Generate specification, plan, and tasks.

**Options:**
- `FEATURE_DESCRIPTION` (optional) — Feature narrative

**Output:** spec.md + plan.md + tasks.md

**Process:**
1. Generate spec from description
2. Identify and clarify ambiguities
3. Generate implementation plan
4. Break down into tasks

**SLA:** < 3 minutes

### `spek implement [TASK_ID]`

Execute a task with context injection.

**Options:**
- `TASK_ID` (optional) — Task ID (e.g., T1.1)
- `--resume` — Resume interrupted task

**Output:** Task completion report

**Process:**
1. Load task context (decisions, patterns, code)
2. Inject context into agent session
3. Execute task
4. Log decisions made
5. Mark complete

**SLA:** < 30 minutes per task

### `spek conclude [FEATURE_NAME]`

Analyze outcomes, extract lessons, update vault.

**Options:**
- `FEATURE_NAME` (optional) — Feature name

**Output:** Lessons document + vault updates

**Process:**
1. Analyze actual outcomes vs. spec
2. Extract lessons learned
3. Identify new patterns
4. Update vault (decisions, patterns, lessons)
5. Refresh project state for next feature

**SLA:** < 5 minutes

## Vault Structure

```
vault/
├── decisions.md          # Architectural decisions (append-only)
├── patterns.md           # Reusable patterns & conventions
├── lessons.md            # Lessons learned summary
└── lessons/              # Individual lesson files (auto-created)
    ├── 2026-06-07-auth-api.md
    ├── 2026-06-14-user-service.md
    └── ...
```

### decisions.md

Records architectural decisions with:
- ID (dec-001, dec-002, ...)
- Title
- Status (approved, proposed, rejected)
- Problem & decision
- Rationale & implications
- Alternatives considered

Example:
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
- ...
```

### patterns.md

Reusable solutions to common problems:
- ID (pat-001, pat-002, ...)
- Category (Architecture, Workflow, Testing, etc.)
- Problem & solution
- Examples & usage guidelines

### lessons/ (Individual Feature Files)

Auto-created by `/spek.conclude`:
- Filename: `YYYY-MM-DD-feature-name.md`
- Contains outcomes, lessons, new patterns, new decisions

## Integration with SpecKit

Spekificity wraps SpecKit for:
- Spec generation (`speckit specify`)
- Planning (`speckit plan`)
- Task generation (`speckit tasks`)
- Implementation tracking (`speckit implement`)

SpecKit produces: `spec.md`, `plan.md`, `tasks.md`

Spekificity enriches SpecKit with:
- Vault context (prior decisions, patterns)
- Code context (relevant files, functions)
- Progress tracking & decision logging

## Integration with lat.md

Spekificity uses lat.md for:
- Code indexing (BM25 retrieval)
- File discovery (relevant files for feature)
- Impact analysis (callers, dependencies)
- Semantic search (fallback if lat.md unavailable)

### Manually Sync Code Index

```bash
# Refresh code index (automatic on /spek.prepare)
lat sync --project=.
```

## Integration with Obsidian

Spekificity uses Obsidian CLI for:
- Vault exports (markdown + metadata)
- Graph generation (visualize relationships)
- Automated syncs

### Optional: Visualize Vault

```bash
# Open vault in Obsidian Desktop (optional for visualization)
open vault/ -a Obsidian
```

## Troubleshooting

### "spek: command not found"

```bash
# Verify installation
uv tool list | grep spekificity

# Reinstall
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
# If it times out, Spekificity falls back to semantic search
# Manually sync if needed:
lat sync --project=. --full
```

## Examples

### Example 1: Simple Feature

```bash
# Prepare
spek prepare "Add dark mode toggle"

# Plan
spek plan "Add dark mode toggle to user settings"

# Implement
spek implement T1.1
spek implement T1.2
spek implement T1.3

# Conclude
spek conclude dark-mode
```

### Example 2: Complex Feature with Multiple Tasks

```bash
# Prepare with specific branch
spek prepare api-v2

# Plan in-depth
spek plan "Redesign REST API for v2.0"

# Review spec.md and plan.md manually before implementing

# Execute in phases
for task in T1.1 T1.2 T1.3 T1.4 T1.5; do
  spek implement $task
done

# Move to Phase 2
for task in T2.1 T2.2 T2.3; do
  spek implement $task
done

# Conclude and extract patterns
spek conclude api-v2
```

## Next Steps

1. **Install**: `uv tool install spekificity --from git+...`
2. **Initialize**: `cd /your/project && spek init`
3. **Start**: `spek prepare "Your Feature Name"`
4. **Review Documentation**: `spek --help`
5. **Read wiki/**: Architecture, patterns, decisions

---

**Documentation Status**: Phase 1 complete ✓  
**Last Updated**: 2026-06-07
