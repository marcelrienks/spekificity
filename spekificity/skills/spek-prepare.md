---
name: spek-prepare
description: 'Initialize third-party tools and load context before feature development.'
---

# /spek.prepare

Initialize third-party tools and load context before feature development.

## Prerequisites

- `.spek/vault/` initialized (`spek init` complete)
- `lat` in PATH
- Obsidian running and vault registered

## Steps

1. Run `lat init` to build or refresh the code index (symbols, definitions, call graphs). Output stored in `.spek/lat.md/`.
2. Run `lat init --docs` to build or refresh the documentation index (wiki, vault, markdown). Output stored in `.spek/lat.md/`.
3. Load vault decisions (`decisions.md`), patterns (`patterns.md`), and prior lessons from `.spek/vault/lessons/` into agent session.
3.5. **Vault Sync Guidance**: If using Obsidian Desktop for vault browsing/editing:
   - Pull latest vault changes from git: `git pull origin main` (ensures decisions/patterns from other features loaded)
   - Open `.spek/vault/` folder in Obsidian Desktop (if not already open)
   - Obsidian will detect backlinks and wikilinks from prior lessons
   - Do NOT push Obsidian-generated metadata files (`.obsidian/`) to git (add to .gitignore)
4. Load workspace facts from `.spek/memory/` into session.
5. Verify `.spek/memory/constitution.md` exists. If missing, invoke `/speckit-constitution` to create it interactively. Once complete, extract Core Principles section and use it to populate:
   - `CLAUDE.md` — Claude agent rules derived from constitution principles
   - `.cursor/rules.md` — Cursor agent equivalent (if .cursor/ exists)
   - `.windsurf/rules.md` — Windsurf agent equivalent (if .windsurf/ exists)
   - Other agent-specific config files as needed
6. Validate tooling: Check that `lat` command available in PATH (run `which lat` or equivalent). If not found, halt with error.
7. Validate Obsidian CLI: Check that Obsidian CLI accessible (run `osascript` or `which obsidian` on macOS, equivalent on Linux/Windows). If not found, print warning but continue (vault operations may still work via file ops).
8. Validate write access: Check directories writable — `.spek/vault/`, `.spek/memory/`, project root for `CLAUDE.md`. If any lack write access, halt with error.
9. Check token budget: read `token_budget.per_feature` from `.spek/config.yaml` (if file exists); print `[WARN] token budget: check remaining before starting` if `per_feature` is set; skip silently if config missing or `per_feature: null`.

## Output

- lat.md code index current in `.spek/lat.md/code/`
- lat.md doc index current in `.spek/lat.md/docs/`
- Vault context (decisions, patterns, lessons) loaded into session from git (latest from all prior features)
- Constitution confirmed present at `.spek/memory/constitution.md`
- Agent config files populated from constitution principles:
  - `CLAUDE.md` — Claude agent rules
  - `.cursor/rules.md` — Cursor agent rules (if applicable)
  - `.windsurf/rules.md` — Windsurf agent rules (if applicable)
- Obsidian Desktop vault synced (if used) and ready for optional manual editing
- Ready to call `/spek.plan` or `/spek.map` next

## See Also

- `/spek.workflow` — Complete workflow diagram and calling sequence
- `/spek.context` — Load vault context without refreshing lat.md (use when switching between concurrent features)

## Exit Criteria

- lat.md code index initialized and current in `.spek/lat.md/code/` and `.spek/lat.md/docs/`
- Vault context (decisions, patterns, lessons) loaded from git
- Constitution present and core principles extracted from `.spek/memory/constitution.md`
- Agent config files (CLAUDE.md, .cursor/rules.md, .windsurf/rules.md, etc.) populated from constitution
- Obsidian Desktop vault synchronized (latest decisions/patterns from prior features)
- Token budget checked (or skipped if not configured)
