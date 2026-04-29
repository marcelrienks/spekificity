# Setup Guide: SpecKit / Specify

## Overview

SpecKit (installed via the `specify-cli` package) is the spec-driven development workflow engine that Spekificity is built on top of. It provides the `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` commands that structure the AI development lifecycle. Spekificity wraps these commands with graph-aware context — it does not replace them.

## Install Mode

**Global** — installed per machine via `uv tool install`. Spekificity custom skills are installed per project (layered on top).

## Prerequisites

- Python 3.11+
- `uv` installed (`uv --version` returns a version)
- `git` installed (`git --version` returns a version)
- Internet access for initial install

## Installation Steps

1. Install SpecKit globally:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. Confirm the `specify` command is on your PATH:
   ```bash
   which specify
   # Expected: /Users/<you>/.local/bin/specify or similar
   ```

3. Initialise SpecKit in your project:
   ```bash
   cd /path/to/your/project
   specify init .
   ```

   When prompted:
   - **AI assistant**: Select `copilot` (GitHub Copilot) or `claude` (Claude Code)
   - **Script type**: Select `sh`

   This creates:
   - `.specify/` — SpecKit configuration, templates, scripts, extensions
   - `.github/agents/` — Agent skill files (Copilot)
   - `.github/copilot-instructions.md` — Copilot context pointer

## Verification

```bash
specify --version
# Expected output: specify-cli X.X.X
```

After `specify init .`:
```bash
ls .specify/
# Expected: extensions.yml  memory/  scripts/  templates/
```

## Configuration

SpecKit configuration lives in `.specify/`:

- **`.specify/extensions.yml`** — Hook definitions for `before_specify`, `before_plan`, `before_implement`, etc. Spekificity enrichment skills can be registered here.
- **`.specify/memory/constitution.md`** — Project constitution. Edit this to add project-specific principles.
- **`.specify/templates/`** — Override SpecKit default templates for spec, plan, and tasks.

## Version Compatibility

| SpecKit Version | Spekificity Compatible | Notes |
|----------------|----------------------|-------|
| ≥ 0.8.0 | ✓ | Extensions/hooks system required |
| 0.7.x | ⚠ | No extensions.yml; enrichment skills must be invoked manually |
| < 0.7.0 | ✗ | Unsupported |

## The `specify init .` Workflow

Running `specify init .` is **idempotent** — safe to run multiple times:
- If SpecKit is already initialised, it updates templates and scripts without overwriting your constitution or custom configuration.
- New SpecKit versions: run `uv tool upgrade specify-cli` then re-run `specify init .` to pick up new templates.

## Troubleshooting

- **Symptom**: `specify: command not found` → **Fix**: Run the install command above; ensure `~/.local/bin` is in your `PATH`
- **Symptom**: `specify init .` fails with git error → **Fix**: Ensure the project folder is a git repository (`git init` first) or create it first
- **Symptom**: Hooks in `extensions.yml` not firing → **Fix**: Check `enabled: true` and `optional: false` for mandatory hooks; confirm you are using SpecKit ≥ 0.8.0
- **Symptom**: Templates not applied → **Fix**: Check `.specify/templates/` for overrides; run `specify init .` again to refresh
