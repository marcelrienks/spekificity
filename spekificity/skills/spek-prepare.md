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
4. Load workspace facts from `.spek/memory/` into session.
5. Verify `.specify/memory/constitution.md` exists. If missing, invoke `/speckit-constitution` to create it interactively. Once complete, extract Core Principles section and use it to populate:
   - `CLAUDE.md` — Claude agent rules derived from constitution principles
   - `.cursor/rules.md` — Cursor agent equivalent (if .cursor/ exists)
   - `.windsurf/rules.md` — Windsurf agent equivalent (if .windsurf/ exists)
   - Other agent-specific config files as needed
6. Check token budget: read `token_budget.per_feature` from `.spek/config.yaml`; print `[WARN] token budget: check remaining before starting` if `per_feature` is set; skip silently if null.

## Output

- lat.md code index current in `.spek/lat.md/`
- lat.md doc index current in `.spek/lat.md/`
- Vault context (decisions, patterns, lessons) loaded into session
- Constitution confirmed present at `.specify/memory/constitution.md`
- Agent config files populated from constitution principles:
  - `CLAUDE.md` — Claude agent rules
  - `.cursor/rules.md` — Cursor agent rules (if applicable)
  - `.windsurf/rules.md` — Windsurf agent rules (if applicable)

## Exit Criteria

- lat.md code index initialized and current in `.spek/lat.md/`
- lat.md doc index initialized and current in `.spek/lat.md/`
- Vault context (decisions, patterns, lessons) loaded into session
- Constitution present and core principles extracted from `.specify/memory/constitution.md`
- Agent config files (CLAUDE.md, .cursor/rules.md, .windsurf/rules.md, etc.) populated from constitution
- Token budget checked (or skipped if not configured)
