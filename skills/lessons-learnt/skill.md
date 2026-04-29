# Lessons Learnt

## Description

Captures structured lessons at the end of a SpecKit feature lifecycle and writes them to the Obsidian vault. The entry records what worked, what was harder than expected, decisions made, and patterns identified — making this knowledge available to future AI sessions via `/context-load`.

Run this skill after a feature implementation is complete (or at a meaningful checkpoint). It is invoked automatically by `/speckit-enrich-implement` at the end of each feature.

## Trigger

Invoked by the developer in the AI chat session:
```
/lessons-learnt
```

## Prerequisites

- A SpecKit feature implementation is complete or at a meaningful checkpoint
- `vault/lessons/` directory exists (created by init workflow or `/map-codebase`)
- Current feature branch name is accessible via git

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| Feature branch | Auto-detected from `git branch --show-current` | Yes (auto) |
| Date | Auto-detected (today's date, ISO 8601) | Yes (auto) |
| AI model name | Name of AI agent and model (e.g., "GitHub Copilot / Claude Sonnet 4.6") | Yes (auto-detected or ask) |

## Steps

1. **Detect current git branch**:
   ```bash
   git branch --show-current
   ```
   Extract the feature slug (e.g., `001-spekificity-platform` from `001-spekificity-platform`).

2. **AI reflection** — ask the AI to answer these four questions based on what happened during the feature:
   - *What worked well?* (approaches, tools, patterns that saved time or produced quality output)
   - *What was harder than expected?* (blockers, surprises, things that required rework)
   - *What decisions were made?* (architectural, design, or process choices made during this feature)
   - *What patterns were identified?* (reusable approaches worth applying in future features)

3. **Write lessons entry** to `vault/lessons/<YYYY-MM-DD>-<feature-slug>.md` using this schema:

   ```markdown
   ---
   date: YYYY-MM-DD
   feature: <feature-slug>
   branch: <full-branch-name>
   ai_model: <model name>
   status: complete
   ---

   # Lessons Learnt: <Feature Name>

   ## What Worked Well
   - <bullet>

   ## What Was Harder Than Expected
   - <bullet>

   ## Decisions Made
   | Decision | Rationale | Alternatives Considered |
   |----------|-----------|------------------------|
   | <decision> | <why> | <what else was considered> |

   ## Patterns Identified
   - <bullet>

   ## Changelog
   | Version | Change | Detail |
   |---------|--------|--------|
   | 1.0 | Initial | Created by /lessons-learnt |
   ```

4. **Append to `vault/context/patterns.md`**: For each new pattern identified, add a bullet:
   ```
   - YYYY-MM-DD [feature-slug]: <pattern summary>
   ```

5. **Append to `vault/context/decisions.md`**: For each decision made, add a bullet:
   ```
   - YYYY-MM-DD [feature-slug]: <decision summary>
   ```

6. **Report** to developer: "Lessons written to `vault/lessons/<filename>.md`. Patterns and decisions updated."

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| Lessons entry | `vault/lessons/<date>-<slug>.md` | Full structured lessons record |
| Updated patterns | `vault/context/patterns.md` | Appended with new patterns |
| Updated decisions | `vault/context/decisions.md` | Appended with new decisions |

## Error Handling

- **`vault/lessons/` missing**: Create the directory (`mkdir -p vault/lessons`) and proceed.
- **git command fails** (not a git repo or detached HEAD): Ask the developer to provide the feature slug manually. Do not halt.
- **Duplicate entry** (same date + slug already exists): Append `-v2` to the filename (e.g., `2026-04-29-my-feature-v2.md`) rather than overwriting.

## Notes

- This skill is invoked automatically at the end of `/speckit-enrich-implement`. You can also invoke it manually at any checkpoint.
- If Caveman mode is active, reflect answers may be compressed — expand them before writing to the vault for future readability.
- Future `/context-load` calls will surface this entry automatically.
- Related: [skills/context-load/SKILL.md](../context-load/SKILL.md), [workflows/feature-lifecycle.md](../../workflows/feature-lifecycle.md)
