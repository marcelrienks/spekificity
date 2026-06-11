# /spek.context

Load vault context and repo memory into the current agent session.

## Steps

1. Read `.spek/vault/decisions.md` — load project decisions into session.
2. Read `.spek/vault/patterns.md` — load reusable patterns into session.
3. Read all files in `.spek/vault/lessons/` — load prior lessons into session.
4. Read `.spek/memory/` — load workspace-scoped facts into session.
5. Session state now populated. All downstream `/spek.*` commands have full context available.
