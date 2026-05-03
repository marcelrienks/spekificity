# context load

## description

loads persistent context from the obsidian vault into the ai agent's session at the start of a work session. this primes the ai with the current graph structure, architectural decisions, identified patterns, and recent lessons learnt — without requiring the ai to scan source files or read documentation directories directly.

run this skill at the start of every ai session on a spekificity-enabled project. it is the graph-first entry point mandated by constitution principle v.

## trigger

invoked by the developer in the ai chat session:
```
/context-load
```

optional scope arguments:
```
/context-load graph-only      ← load only the graph index (fastest)
/context-load lessons-only    ← load only recent lessons entries
/context-load full            ← load everything (default)
```

optional feature filter (loads lessons relevant to a specific branch):
```
/context-load full my-feature-branch
```

## prerequisites

- `vault/` directory exists at the project root
- `vault/graph/index.md` exists (run `/map-codebase` first if missing)
- `.spekificity/config.json` exists if running in a `spek init`-enabled project

## inputs

| input | description | required |
|-------|-------------|----------|
| scope | `full` (default), `graph-only`, or `lessons-only` | no |
| feature filter | branch name or feature slug to filter lessons context | no |

## steps

### step 0 — resolve vault path

if `.spekificity/config.json` exists, read `vault.path` from it to determine the vault root. if absent or unset, use the default `vault/`. use this as the base path for all vault file reads in steps 1–4.

### step 0b — check active workflow context

if `.spekificity/workflow-state.json` exists, read it. if `status` is `in-progress` or `halted`, extract the `feature_branch` and `current_step` and include them in the readiness summary: `[spek] ℹ active workflow: <feature_branch> at step <current_step>`. if `status` is `complete` or the file is absent, skip silently.

1. **read `${VAULT_PATH}/graph/index.md`**: load the node list and key relationship summary. note the total node count and any god nodes listed.

2. **read `vault/context/decisions.md`**: load all recorded architectural decisions.

3. **read `vault/context/patterns.md`**: load all identified patterns.

4. **load relevant lessons** (skip if scope is `graph-only`):
   - check `vault/lessons/` for entries matching the current feature (by branch name or feature slug if a filter was provided)
   - if no filter, load the most recent lessons entry (alphabetically last filename)
   - if `vault/lessons/` is empty, skip silently

5. **summarise loaded context** in a brief header of ≤5 bullet points. if caveman mode is active, use caveman compression. example:
   ```
   context loaded:
   - graph: 42 nodes, 3 god nodes (readme.md, src/core.py, specs/)
   - decisions: 7 recorded (latest: 2026-04-29 — decorator pattern chosen)
   - patterns: 3 identified (latest: idempotent init guard)
   - lessons: 1 entry loaded (001-spekificity-platform)
   - ready.
   ```

6. **confirm to developer**: output the summary and confirm the ai is ready to work.

## outputs

| output | location | description |
|--------|----------|-------------|
| active context | ai working memory | graph structure, decisions, patterns, lessons held in session |

## error handling

- **`vault/graph/index.md` missing**: inform developer: "vault graph not found. run `/map-codebase` to build it first." proceed with only decisions and patterns if they exist; do not halt.
- **`vault/` missing entirely**: inform developer: "vault not initialised. run the init workflow (workflows/init-workflow.md) to create it." halt.
- **empty vault** (no meaningful content): load silently with message: "vault is empty — no prior context available. ready."

## notes

- this skill does not modify any files. it is read-only.
- recommended to run at the very start of every ai session, before any `/speckit-enrich-*` command.
- for the fastest session start (large vaults), use `/context-load graph-only` and load full context on demand.
- if caveman mode is active (`/caveman` or `/caveman lite`), the summary output will be compressed automatically.
- related: [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
