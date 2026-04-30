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
- `vault/lessons/` directory exists (created by init workflow or `/map-codebase`)
- current feature branch name is accessible via git

## inputs

| input | description | required |
|-------|-------------|----------|
| feature branch | auto-detected from `git branch --show-current` | yes (auto) |
| date | auto-detected (today's date, iso 8601) | yes (auto) |
| ai model name | name of ai agent and model (e.g., "github copilot / claude sonnet 4.6") | yes (auto-detected or ask) |

## steps

1. **detect current git branch**:
   ```bash
   git branch --show-current
   ```
   extract the feature slug (e.g., `001-spekificity-platform` from `001-spekificity-platform`).

2. **ai reflection** — ask the ai to answer these four questions based on what happened during the feature:
   - *what worked well?* (approaches, tools, patterns that saved time or produced quality output)
   - *what was harder than expected?* (blockers, surprises, things that required rework)
   - *what decisions were made?* (architectural, design, or process choices made during this feature)
   - *what patterns were identified?* (reusable approaches worth applying in future features)

3. **write lessons entry** to `vault/lessons/<yyyy-mm-dd>-<feature-slug>.md` using this schema:

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

4. **append to `vault/context/patterns.md`**: for each new pattern identified, add a bullet:
   ```
   - yyyy-mm-dd [feature-slug]: <pattern summary>
   ```

5. **append to `vault/context/decisions.md`**: for each decision made, add a bullet:
   ```
   - yyyy-mm-dd [feature-slug]: <decision summary>
   ```

6. **report** to developer: "lessons written to `vault/lessons/<filename>.md`. patterns and decisions updated."

## outputs

| output | path | description |
|--------|------|-------------|
| lessons entry | `vault/lessons/<date>-<slug>.md` | full structured lessons record |
| updated patterns | `vault/context/patterns.md` | appended with new patterns |
| updated decisions | `vault/context/decisions.md` | appended with new decisions |

## error handling

- **`vault/lessons/` missing**: create the directory (`mkdir -p vault/lessons`) and proceed.
- **git command fails** (not a git repo or detached head): ask the developer to provide the feature slug manually. do not halt.
- **duplicate entry** (same date + slug already exists): append `-v2` to the filename (e.g., `2026-04-29-my-feature-v2.md`) rather than overwriting.

## notes

- this skill is invoked automatically at the end of `/speckit-enrich-implement`. you can also invoke it manually at any checkpoint.
- if caveman mode is active, reflect answers may be compressed — expand them before writing to the vault for future readability.
- future `/context-load` calls will surface this entry automatically.
- related: [skills/context-load/skill.md](../context-load/skill.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
