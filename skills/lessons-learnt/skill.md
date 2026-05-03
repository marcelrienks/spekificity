# lessons learnt

## description

captures structured lessons at the end of a speckit feature lifecycle and writes them to the obsidian vault. the entry records what worked, what was harder than expected, decisions made, and patterns identified — making this knowledge available to future ai sessions via `/context-load`.

run this skill after a feature implementation is complete (or at a meaningful checkpoint). it is invoked automatically by `/speckit-enrich-implement` at the end of each feature.

## trigger

invoked by the developer in the ai chat session:
```
/lessons-learnt
```

## prerequisites

- a speckit feature implementation is complete or at a meaningful checkpoint
- `vault/lessons/` directory exists (created by init workflow or `/map-codebase`); if absent, create it with `mkdir -p vault/lessons/`
- current feature branch name is accessible via git
- `.spekificity/config.json` exists if running in a `spek init`-enabled project (for vault path resolution)

## inputs

| input | description | required |
|-------|-------------|----------|
| feature branch | auto-detected from `git branch --show-current` or `workflow-state.json`.feature_branch | yes (auto) |
| feature dir | `workflow-state.json`.feature_dir (if available) — used to read spec/plan for AI inference | no |
| date | auto-detected (today's date, iso 8601) | yes (auto) |
| ai model name | name of ai agent and model (e.g., "github copilot / claude sonnet 4.6") | yes (auto-detected or ask) |
| developer reflection | answers to the 4 reflection questions (passed from `/spek.post` if invoked via automate) | no — AI infers if absent |

## steps

1. **resolve vault path**: read `vault.path` from `.spekificity/config.json`. if absent or unset, default to `vault/`. all writes below use this resolved path as `${VAULT_PATH}`.

2. **detect current git branch**:
   ```bash
   git branch --show-current
   ```
   if `.spekificity/workflow-state.json` exists, prefer `feature_branch` from there. extract the feature slug (e.g., `001-spekificity-platform` from `001-spekificity-platform`).

3. **developer reflection prompt** — if reflection answers were not passed (e.g., manual invocation), prompt the developer using `[spek] ❓` format:
   ```
   [spek] ❓ lessons reflection (feature: <feature_branch>)

   Please answer briefly:
   > 1. What decisions were made? (architectural, design, or process)
   > 2. What patterns emerged that could be reused?
   > 3. What was harder than expected?
   > 4. What worked particularly well?

   (press Enter to let the AI infer from the feature spec, plan, and tasks)
   ```
   if developer presses Enter without answering, infer answers from `<feature_dir>/spec.md`, `<feature_dir>/plan.md`, and `<feature_dir>/tasks.md`.

4. **ai reflection** — using developer answers or AI-inferred answers, synthesise responses to the four questions:
   - *what worked well?*
   - *what was harder than expected?*
   - *what decisions were made?*
   - *what patterns were identified?*

5. **write lessons entry** to `${VAULT_PATH}/lessons/<yyyy-mm-dd>-<feature-slug>.md` using this schema:

   **append-on-collision**: if `<yyyy-mm-dd>-<feature-slug>.md` already exists, append `-v2` to the filename (e.g., `2026-04-29-my-feature-v2.md`). increment suffix (`-v3`, `-v4`, etc.) until a free filename is found — never overwrite.


   ```markdown
   ---
   date: yyyy-mm-dd
   feature: <feature-slug>
   branch: <full-branch-name>
   ai_model: <model name>
   status: complete
   ---

   # lessons learnt: <feature name>

   ## what worked well
   - <bullet>

   ## what was harder than expected
   - <bullet>

   ## decisions made
   | decision | rationale | alternatives considered |
   |----------|-----------|------------------------|
   | <decision> | <why> | <what else was considered> |

   ## patterns identified
   - <bullet>

   ## changelog
   | version | change | detail |
   |---------|--------|--------|
   | 1.0 | initial | created by /lessons-learnt |
   ```

6. **append to `${VAULT_PATH}/context/patterns.md`**: for each new pattern identified, add a bullet:
   ```
   - yyyy-mm-dd [feature-slug]: <pattern summary>
   ```

7. **append to `${VAULT_PATH}/context/decisions.md`**: for each decision made, add a bullet:
   ```
   - yyyy-mm-dd [feature-slug]: <decision summary>
   ```

8. **report** to developer:
   ```
   [spek] ✓ lessons written to ${VAULT_PATH}/lessons/<filename>.md
   [spek] ✓ patterns and decisions updated
   ```

## outputs

| output | path | description |
|--------|------|-------------|
| lessons entry | `vault/lessons/<date>-<slug>.md` | full structured lessons record |
| updated patterns | `vault/context/patterns.md` | appended with new patterns |
| updated decisions | `vault/context/decisions.md` | appended with new decisions |

## error handling

- **`vault/lessons/` missing**: create the directory (`mkdir -p ${VAULT_PATH}/lessons`) and proceed.
- **git command fails** (not a git repo or detached head): ask the developer to provide the feature slug manually. do not halt.
- **duplicate entry** (same date + slug already exists): append `-v2` (then `-v3`, `-v4`, ...) to the filename — never overwrite.
- **developer reflection empty**: AI infers from spec, plan, and tasks. log `[spek] ℹ inferring reflection from feature artifacts`.

## notes

- this skill is invoked automatically at the end of `/speckit-enrich-implement`. you can also invoke it manually at any checkpoint.
- if caveman mode is active, reflect answers may be compressed — expand them before writing to the vault for future readability.
- future `/context-load` calls will surface this entry automatically.
- related: [skills/context-load/skill.md](../context-load/skill.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
