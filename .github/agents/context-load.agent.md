# Context Load

## Description

Loads persistent context from the Obsidian vault into the AI agent's session at the start of a work session. This primes the AI with the current graph structure, architectural decisions, identified patterns, and recent lessons learnt — without requiring the AI to scan source files or read documentation directories directly.

Run this skill at the start of every AI session on a Spekificity-enabled project. It is the graph-first entry point mandated by Constitution Principle V.

## Trigger

Invoked by the developer in the AI chat session:
```
/context-load
```

Optional scope arguments:
```
/context-load graph-only      ← Load only the graph index (fastest)
/context-load lessons-only    ← Load only recent lessons entries
/context-load full            ← Load everything (default)
```

Optional feature filter (loads lessons relevant to a specific branch):
```
/context-load full my-feature-branch
```

## Prerequisites

- `vault/` directory exists at the project root
- `vault/graph/index.md` exists (run `/map-codebase` first if missing)

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| Scope | `full` (default), `graph-only`, or `lessons-only` | No |
| Feature filter | Branch name or feature slug to filter lessons context | No |

## Steps

1. **Read `vault/graph/index.md`**: Load the node list and key relationship summary. Note the total node count and any god nodes listed.

2. **Read `vault/context/decisions.md`**: Load all recorded architectural decisions.

3. **Read `vault/context/patterns.md`**: Load all identified patterns.

4. **Load relevant lessons** (skip if scope is `graph-only`):
   - Check `vault/lessons/` for entries matching the current feature (by branch name or feature slug if a filter was provided)
   - If no filter, load the most recent lessons entry (alphabetically last filename)
   - If `vault/lessons/` is empty, skip silently

5. **Summarise loaded context** in a brief header of ≤5 bullet points. If Caveman mode is active, use Caveman compression. Example:
   ```
   Context loaded:
   - Graph: 42 nodes, 3 god nodes (README.md, src/core.py, specs/)
   - Decisions: 7 recorded (latest: 2026-04-29 — decorator pattern chosen)
   - Patterns: 3 identified (latest: idempotent init guard)
   - Lessons: 1 entry loaded (001-spekificity-platform)
   - Ready.
   ```

6. **Confirm to developer**: Output the summary and confirm the AI is ready to work.

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Active context | AI working memory | Graph structure, decisions, patterns, lessons held in session |

## Error Handling

- **`vault/graph/index.md` missing**: Inform developer: "Vault graph not found. Run `/map-codebase` to build it first." Proceed with only decisions and patterns if they exist; do not halt.
- **`vault/` missing entirely**: Inform developer: "Vault not initialised. Run the init workflow (workflows/init-workflow.md) to create it." Halt.
- **Empty vault** (no meaningful content): Load silently with message: "Vault is empty — no prior context available. Ready."

## Notes

- This skill does not modify any files. It is read-only.
- Recommended to run at the very start of every AI session, before any `/speckit-enrich-*` command.
- For the fastest session start (large vaults), use `/context-load graph-only` and load full context on demand.
- If Caveman mode is active (`/caveman` or `/caveman lite`), the summary output will be compressed automatically.
- Related: [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
