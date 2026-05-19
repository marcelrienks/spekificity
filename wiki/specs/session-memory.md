# ATOMIC SPECIFICATION: Session Memory (C2.4)

**Status:** ATOMIC SPECIFICATION  
**Type:** Memory Layer 3 — Session-Scoped Ephemeral Context  
**Depends On:** context-load-lifecycle.md  
**Used By:** /spek.context (write at session start), /spek.prepare (use during prep), agent (read throughout session)  

---

## Overview

Session memory stores temporary, session-scoped context that aids the agent during current work but is discarded at session end. Two ephemeral files track current feature state and provide continuity across turns.

---

## /memories/session/context-loaded.md

### Purpose
Summary of what was loaded into context at session start (decisions, patterns, lessons, code structure).

### File Structure

```markdown
---
session_date: YYYY-MM-DD HH:MM
context_load_timestamp: YYYY-MM-DDTHH:MM:SSZ
session_duration_minutes: 0
token_budget_used: 0
cache_hit: boolean
---

# Session Context Load

**Session Start:** YYYY-MM-DD HH:MM  
**Feature:** spec-XXX (if resuming) or "new feature"  
**Branch:** feature-branch-name  
**Phase:** prepared | specifying | planning | implementing | completing  

---

## Recent Decisions Loaded (Last 3 Features)

| Feature | Decision | Rationale | Impact |
|---------|----------|-----------|--------|
| spec-003 | [title] | [1-line rationale] | [high/medium/low] |
| spec-002 | [title] | [1-line rationale] | [high/medium/low] |

[Full decision summaries]

---

## Recent Patterns Available (Last 3 Features)

- **Decorator Wrapper Pattern** (5 uses) — SpecKit integration layer
- **Lesson-Based Documentation** (3 uses) — Feature capture
- **Post-Processing Automation** (3 uses) — Vault synchronization

[Full pattern descriptions]

---

## Code Structure Summary

**Code Graph Freshness:** synced 45 mins ago ✓  
**Total Symbols:** 423 code nodes, 45 doc nodes  
**Primary Languages:** python (67%), typescript (21%), markdown (12%)  

**Key Modules:**
- `src/services/` — Business logic (45 modules)
- `src/api/` — API handlers (12 modules)
- `src/database/` — Data access (8 modules)
- `wiki/specs/` — Specifications (25 specs)
- `vault/` — Knowledge base (decisions, patterns, lessons)

**Recent Changes:** Last 5 files modified
- src/services/auth.py (2 days ago)
- .spekificity/config.yaml (5 days ago)
- wiki/decision.md (1 week ago)

---

## Lessons Quick Reference

**Most Relevant Lessons:**
- [Lesson 1 from spec-003]: Key takeaway
- [Lesson 2 from spec-002]: Key takeaway
- [Lesson 3 from spec-001]: Key takeaway

---

## Important Constraints

- [Active decision that limits design space]
- [Performance requirement or limitation]
- [Team convention or standard]

---

## Session Goals

[Goals for this session, loaded from feature state or user input]

---

## Helpful Commands

- `/spek.context [query]` — Refresh context on specific topic
- `/spek.map` — Refresh code graph if needed
- See wiki/memory-queries.md for query patterns
```

### Template Fields

**YAML Frontmatter:**
- `session_date` — When session started
- `context_load_timestamp` — ISO timestamp of /spek.context call
- `session_duration_minutes` — Updated at session end (for metrics)
- `token_budget_used` — Total tokens used in session (for optimization)
- `cache_hit` — Did we reuse context from previous session?

**Session Start:** When session began (ISO format)

**Feature:** Which feature we're working on (or "new feature" if starting fresh)

**Branch:** Git branch name

**Phase:** Where in the workflow (prepared, specifying, planning, implementing, completing)

**Recent Decisions / Patterns / Code Structure:** Compressed summaries from vault/decision.md, vault/patterns.md, vault/graph/

**Lessons Quick Reference:** Most relevant lessons from last 3 features

**Important Constraints:** Active decisions that constrain design

**Session Goals:** What we're trying to accomplish this session

---

## /memories/session/current-feature.md

### Purpose
Progress tracking for the feature currently being worked on (spans multiple sessions if feature is long).

### File Structure

```markdown
---
feature_name: "<feature-name>"
feature_id: "<feature-number>"
status: "initialized | specifying | planning | implementing | completing | abandoned"
session_start: YYYY-MM-DDTHH:MM:SSZ
session_count: 1
phase: "prepared | specifying | planning | implementing | completing"
completion: 0
---

# Feature [Number]: [Name]

**Status:** initialized  
**Branch:** feature-XXX-name  
**Current Session:** Session 1  
**Total Sessions:** 1  

---

## Feature Description

[1-3 sentence overview of what this feature does]

---

## Goals

- [ ] Goal 1: [specific, measurable]
- [ ] Goal 2: [specific, measurable]
- [ ] Goal 3: [specific, measurable]

---

## Current Phase: Prepared

Ready for `/spek.specify` to generate spec.

---

## Progress by Phase

### Specifying (0% complete)
- [ ] Spec draft
- [ ] Spec validated
- [ ] Decisions documented

### Planning (0% complete)
- [ ] Plan draft
- [ ] Plan reviewed
- [ ] Architecture agreed

### Implementing (0% complete)
- [ ] Tasks generated
- [ ] Task 1 complete
- [ ] Task 2 in progress
- [ ] Task 3 not started

### Completing (0% complete)
- [ ] All tasks done
- [ ] Tests passing
- [ ] Lessons extracted
- [ ] Vault updated

---

## Decisions Made This Feature

- [Decision 1: rationale]
- [Decision 2: rationale]

---

## Patterns Applied

- [Pattern 1: where/how applied]
- [Pattern 2: where/how applied]

---

## Artifacts

- **spec.md** — Feature specification (created/updated HH:MM)
- **plan.md** — Implementation plan (created/updated HH:MM)
- **tasks.md** — Task list (created/updated HH:MM)

---

## Session Log

**Session 1 (2026-05-19 10:00-11:30):**
- [PREPARED] Workspace verified, context loaded
- Ready for spec generation

**Session 2 (TBD):**
- [TBD]

---

## Known Blockers

- [Blocker 1: impact, workaround]

---

## Next Steps

1. Run `/spek.specify [feature description]` to generate spec
2. Review spec for completeness
3. Run `/spek.plan` to generate plan
4. Proceed to implementation

---

## Notes

[Scratch notes, ideas, concerns]
```

### Template Fields

**YAML Frontmatter:**
- `feature_name` — User-friendly name (e.g., "spek-full-workflow-cli")
- `feature_id` — Sequential number (e.g., "003")
- `status` — One of: initialized, specifying, planning, implementing, completing, abandoned
- `session_start` — ISO timestamp when feature started
- `session_count` — How many sessions have worked on this feature
- `phase` — Where in lifecycle (aligns with status)
- `completion` — Percentage complete (0-100)

**Feature Description:** What this feature does (1-3 sentences)

**Goals:** Specific, measurable outcomes (checkboxes)

**Current Phase:** Which phase are we in? (updated per session)

**Progress by Phase:** Detailed checkpoint for each phase (updated as work progresses)

**Decisions Made This Feature:** Quick list (extracted to vault at feature end)

**Patterns Applied:** Which patterns were used and how (extracted to vault at feature end)

**Artifacts:** Links to spec/plan/tasks with timestamps

**Session Log:** Chronological record of what happened each session

**Known Blockers:** Issues that are blocking progress (with workarounds)

**Next Steps:** What to do next (for session continuity)

**Notes:** Scratch space for ideas, concerns, questions

---

## Lifecycle

### Write Triggers

**At feature start (`/spek.prepare` step 6):**
- Create current-feature.md with initialized status
- Write feature name, branch, phase
- Write goals (if provided)
- Write initial session log entry

**End of each session:**
- Update progress percentages
- Log what was accomplished
- Log blockers and next steps
- Update session_count

**End of feature (`/spek.post`):**
- Mark status as "completed" or "abandoned"
- Archive to /memories/session/archive/
- Convert to vault/lessons/ file

### Read Triggers

**Feature continuation (next session):**
- Agent reads at session start to understand current state
- Updates session_count, adds new session log entry

**During work:**
- Agent references to check progress, blockers, next steps
- Updates as work progresses

**At feature end:**
- Agent reads to collect all artifacts
- Passes to /spek.post for lessons extraction

### Retention Policy

**During feature:** Keep current-feature.md in /memories/session/

**At feature end:**
- Copy to /memories/session/archive/current-feature-<date>-<name>.md (for reference)
- Delete from /memories/session/ (or keep for immediate post-mortem)

**After feature:** Delete archive file after 30 days (or when vault/lessons file is confirmed stable)

---

## Session Memory Schemas

### Format Validation

Both files must have:
1. Valid YAML frontmatter (triple-dash delimited)
2. Valid markdown headings (H1, H2, etc.)
3. Parseable checkpoint lists (markdown checkboxes)

**Validation:**
```bash
# Check frontmatter
head -5 /memories/session/context-loaded.md | grep "^---"

# Check markdown
grep "^# " /memories/session/current-feature.md
```

---

## Error Handling

**If context-loaded.md is missing:**
- `/spek.context` can be re-run to regenerate it
- Context is embedded in agent context anyway

**If current-feature.md is missing:**
- `/spek.prepare --skip-context` can re-create it
- Or agent can create it manually with minimal template

**If files are corrupted (invalid YAML):**
- Log error but continue (context is nice-to-have, not critical)
- Agent can work with embedded context

---

## Success Criteria

✅ Session memory files are created at appropriate lifecycle points  
✅ Files have valid YAML frontmatter and markdown structure  
✅ Context-loaded summarizes decisions, patterns, code structure  
✅ Current-feature tracks progress through all phases  
✅ Session log provides chronological continuity  
✅ Files are ephemeral (deleted at appropriate time)  

---

## Implementation Checklist

- [ ] Create /memories/session/context-loaded.md template
- [ ] Create /memories/session/current-feature.md template
- [ ] Implement file creation in /spek.context (context-loaded)
- [ ] Implement file creation in /spek.prepare (current-feature)
- [ ] Implement file updates in /spek.post (completion, archive)
- [ ] Document session memory in wiki guide

---

## References

**Related Specs:**
- [context-load-lifecycle.md](context-load-lifecycle.md) — Context loading triggers file creation
- [feature-state-tracking.md](feature-state-tracking.md) — Feature state structure and updates
- [post-command.md](post-command.md) — Lessons extraction and archival

**External:**
- [extracted spec Persistent Memories](persistent-memories-and-lessons.md#type-4-current-session-context-ephemeral) — Original spec
