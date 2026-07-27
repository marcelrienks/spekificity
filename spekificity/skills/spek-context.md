---
name: spek-context
description: 'Load vault context and repo memory into the current agent session.'
---

# /spek.context

Load vault context and repo memory into the current agent session.

## Prerequisites

- `.spek/vault/` initialized (`spek init` complete)

## Steps

1. Read `.spek/vault/decisions.md` — load project decisions into session.
2. Read `.spek/vault/patterns.md` — load reusable patterns into session.
3. Read all files in `.spek/vault/lessons/` — load prior lessons into session.
4. Read `.spek/memory/` — load workspace-scoped facts into session.
5. Session state now populated. All downstream `/spek.*` commands have full context available.

## Output

- Project decisions, patterns, lessons, and workspace facts loaded into agent session

## Exit Criteria

- Vault decisions and patterns loaded
- Prior lessons loaded from `.spek/vault/lessons/`
- Workspace memory loaded from `.spek/memory/`
- Session ready for downstream `/spek.*` commands
