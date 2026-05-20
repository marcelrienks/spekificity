# Spec: Persistent Memories and Lessons (extracted spec)

## Overview

**Problem:** Context is currently reloaded from scratch at session start (vault graph + decisions + lessons). There is no durable, incrementally-updated memory layer that captures *what was built* vs. *what was decided* vs. *what was learned*. Future sessions either re-read everything (expensive) or miss context (error-prone).

**Solution:** Define a coherent memory architecture with explicit granularity, ownership, persistence, and lifecycle for each memory type.

**Outcome:** Spekificity platform has a clear memory model that spans three layers: persisted vault (Obsidian), repo-scoped memories (copilot), and session-scoped context (ephemeral). Each layer has defined write triggers, read timing, and retention policy.

---

## Memory Architecture

### Three-Layer Model

```
Layer 1: Vault (Obsidian) — Persistent, Authoritative
├── vault/decision.md          [decisions, ranked by recency + importance]
├── vault/intention.md         [project vision, tenets, constraints]
├── vault/patterns.md          [reusable patterns from prior features]
└── vault/lessons/<YYYY-MM-DD>-<feature>-*.md  [one file per completed feature]

Layer 2: Repo Memory (Copilot) — Persistent, Project-Scoped
├── /memories/repo/codebase-map.md         [high-level codebase structure]
├── /memories/repo/architectural-decisions.md  [decisions with rationale + impact]
└── /memories/repo/patterns-index.md       [index of reusable patterns]

Layer 3: Session Memory (Copilot) — Ephemeral, Session-Scoped
├── /memories/session/context-loaded.md    [what was loaded at session start]
├── /memories/session/current-feature.md   [current feature state + progress]
└── /memories/session/scratchpad.md        [notes for current session]
```

---

## Memory Types and Lifecycle

### Type 1: Per-Feature Lessons (Vault)

**File:** `vault/lessons/<YYYY-MM-DD>-<feature-number>-<feature-name>.md`  
**Scope:** Persists across all sessions  
**Granularity:** One file per completed feature  
**Ownership:** Written by `/spek.post` at feature end; read by `/spek.context` at session start

**Write Trigger:**
- Feature complete: `/spek.post` step 3 → generate lessons → write to vault/lessons/

**Content (Template from B.3):**
```markdown
# Lesson: [Feature Name] ([Date], spec-[Number])

## What We Built
[2-3 sentence digest + key domain concepts]

## How We Built It
[Technical approach; key decisions with rationale]

## Key Tasks Executed
[Top 3-5 tasks; how long each took; any blockers]

## Decisions Made
[Major architectural or process decisions]

## Patterns Identified
[Reusable patterns from this feature]

## Lessons for Next Feature
[What would we do differently; what worked well]

## Metrics
[Token count, execution time, quality indicators]

## References
[Links to spec.md, plan.md, PR, decision.md entries]
```

**Read Trigger:**
- Session start: `/spek.context` reads recent 3-5 lesson files → includes in context briefing
- Via grep: `grep -l "pattern-name" vault/lessons/*.md` → find features that used a pattern

**Retention Policy:**
- Keep all lessons indefinitely (permanent vault archive)
- Mark "archived" lessons with `status: archived` frontmatter (but don't delete)
- Index in `vault/patterns.md` for pattern discovery

**Quality Metrics:**
- [x] Self-contained (readable without spec.md/plan.md)
- [x] Compressed (caveman format: active voice, concrete, short)
- [x] Actionable (next feature can apply lessons immediately)
- [x] Specific (concrete code examples, not vague advice)

---

### Type 2: Architectural Decisions (Vault + Repo Memory)

**File (Vault):** `vault/decision.md`  
**File (Repo Memory):** `/memories/repo/architectural-decisions.md`  
**Scope:** Persists across all sessions  
**Granularity:** One entry per decision (heading per decision)  
**Ownership:** Written by `/spek.post` when decisions emerge; read by `/spek.context` at session start

**Vault Format:**
```markdown
# Decision Index

## [Decision Title]

**Date:** YYYY-MM-DD  
**Feature:** spec-[number]  
**Status:** active | deprecated | superceded-by-[link]

**Context:** Why this decision was needed

**Options Considered:**
- Option A: [description, pros, cons]
- Option B: [description, pros, cons]

**Decision:** [Option chosen] because [rationale]

**Impact:** [affected systems, patterns, future constraints]

**Related Decisions:** [links to other decisions]
```

**Repo Memory Format (Summary):**
```markdown
# Architectural Decisions

| Date | Feature | Decision | Status | Impact |
|------|---------|----------|--------|--------|
| 2026-05-18 | 003 | [title] | active | [high/medium/low] |
| 2026-05-15 | 002 | [title] | active | high |

## Recent Active Decisions (Last 3 Features)

[Most impactful 5-10 decisions with 1-line summary each]

## Superceded Decisions

[Link to vault/decision.md for full list]
```

**Write Trigger:**
- Feature end: `/spek.post` step 4 → extract decisions from lessons → append to vault/decision.md and sync to repo memory
- Alternatively: Dev manually adds decision during feature work → `/spek.post` collects and de-duplicates

**Read Trigger:**
- Session start: `/spek.context` reads recent decisions → includes in context
- Spec writing: Agent queries "are there existing decisions about [topic]?" → grep vault/decision.md

**Retention Policy:**
- Keep all decisions (mark deprecated, don't delete)
- Index by status: active (current constraints), deprecated (historical context)
- Prune repo memory to top N recent decisions (e.g., last 3 features) to keep /memories/repo/ lean

**Update Cadence:**
- Vault: after each feature (`/spek.post`)
- Repo Memory: after each feature, but only sync recent active decisions to keep file small

---

### Type 3: Patterns Library (Vault)

**File:** `vault/patterns.md`  
**Scope:** Persists across all sessions  
**Granularity:** One entry per pattern (heading per pattern)  
**Ownership:** Written by `/spek.post` when patterns emerge; read by `/spek.context` at session start and during planning

**Format:**
```markdown
# Patterns Library

## [Pattern Name]

**First Used:** spec-[number] (date)  
**Last Used:** spec-[number] (date)  
**Frequency:** used in N features

**Summary:** [1-2 sentence description]

**When to Use:**
- Context: [situations where this pattern applies]
- Prerequisites: [what must be true]
- Benefits: [why use this pattern]
- Drawbacks: [when NOT to use]

**Implementation:**
```
[Code example or high-level steps]
```

**Related Patterns:**
- [Link to similar pattern]
- [Link to complementary pattern]

**Lessons Learned:**
- [What went well when using this pattern]
- [What to watch out for]
- [Edge cases]

**References:**
- Lessons: [link to vault/lessons files that used this pattern]
- Code: [link to implementation in codebase]
```

**Write Trigger:**
- Feature end: `/spek.post` step 4 → identify new/refined patterns from lessons → append to vault/patterns.md with "Last Used" updated

**Read Trigger:**
- Spec writing: Agent queries "patterns for [domain]" → grep vault/patterns.md for tags
- Plan writing: Agent browses patterns → considers applicability to current feature

**Retention Policy:**
- Keep all patterns indefinitely (archive unused ones with `status: archived`)
- Tag by domain (e.g., #api, #database, #testing)
- Prune repo memory to top N recent patterns (e.g., last 20 used) for quick access

---

### Type 4: Current Session Context (Ephemeral)

**File:** `/memories/session/context-loaded.md`  
**Scope:** Session-scoped (cleared after session)  
**Granularity:** One entry per session  
**Ownership:** Written by `/spek.context` at session start; read throughout session for reference

**Format:**
```markdown
# Session [YYYY-MM-DD HH:MM] Context Load

## Feature Context
- **Feature:** spec-XXX
- **Branch:** NNN-feature-name
- **Status:** [starting | in-progress | completing]

## Recent Lessons Loaded
- [Lesson 1 summary]
- [Lesson 2 summary]
- [Lesson 3 summary]

## Recent Decisions Loaded
- [Decision 1]
- [Decision 2]
- [Decision 3]

## Patterns Available
- [Pattern 1 (frequency: N uses)]
- [Pattern 2 (frequency: M uses)]

## Code Structure
- [High-level codebase overview loaded from vault/graph/]
- [Key files and their purpose]

## Caveats and Notes
- [What changed since last feature]
- [Known issues or constraints]
```

**Write Trigger:**
- Session start: `/spek.context` command → read vault (lessons, decisions, patterns) → read graph → summarize → write session memory

**Read Trigger:**
- Throughout session: Agent can query context via `/spek.context [query]` (e.g., "what patterns exist for testing?")
- Between turns: Agent reads /memories/session/context-loaded.md to stay oriented

**Retention Policy:**
- Delete at session end (ephemeral)
- Or: Compress and archive to /memories/session/archive/ if valuable for future reference

---

### Type 5: Current Feature State (Ephemeral)

**File:** `/memories/session/current-feature.md`  
**Scope:** Session-scoped (cleared after feature complete)  
**Granularity:** One entry per feature (spans multiple sessions if feature is long)  
**Ownership:** Written by agent during work; read by agent across sessions for continuity

**Format:**
```markdown
# Feature [Number] In Progress

## Current Status
- **Phase:** [specifying | planning | implementing | testing | completing]
- **Completion:** X% (spec: done, plan: done, tasks: done, implement: 60%)

## Spec Summary
[1-2 sentences of feature scope]

## Plan Overview
[Architecture approach, key decisions]

## Tasks Progress
- [ ] Task 1 (done)
- [ ] Task 2 (in progress)
- [ ] Task 3 (blocked on X)
- [ ] Task 4 (not started)

## Decisions Made This Feature
- [Decision 1: rationale]
- [Decision 2: rationale]

## Patterns Applied
- [Pattern 1: where applied]
- [Pattern 2: where applied]

## Known Blockers
- [Blocker 1]
- [Blocker 2]

## Next Steps
- [Immediate next action]
- [What to do after that]

## Session Log
- Session 1 (2026-05-18): [what was done]
- Session 2 (2026-05-19): [what was done]
```

**Write Trigger:**
- Feature start: `/spek.prepare` → create current-feature.md with spec summary
- End of each session: Agent updates progress, blockers, next steps
- Feature end: `/spek.post` → move to vault/lessons/ (convert to lesson format)

**Read Trigger:**
- Feature continuation: Agent reads at session start to resume work
- Between turns: Agent updates as work progresses

**Retention Policy:**
- Keep during feature work (spans multiple sessions)
- Archive to /memories/session/archive/ after feature completes (for reference)
- Delete after N days (default: 30 days after feature ends)

---

## Load/Write Lifecycle

### Load Lifecycle: `/spek.context` (Session Start)

```
Timeline: Session Start
│
├─ Step 1: Read Vault
│  ├─ vault/decision.md (most recent, active decisions)
│  ├─ vault/patterns.md (top N recent patterns)
│  └─ vault/lessons/ (read 3-5 most recent lessons)
│
├─ Step 2: Read Repo Memory
│  ├─ /memories/repo/architectural-decisions.md
│  ├─ /memories/repo/patterns-index.md
│  └─ /memories/repo/codebase-map.md
│
├─ Step 3: Query Code Graph
│  ├─ vault/graph/nodes.jsonl (via /spek.map)
│  └─ High-level code structure summary
│
├─ Step 4: Summarize & Compress
│  ├─ Caveman mode: Compress all loaded context
│  └─ Output: concise context briefing
│
└─ Step 5: Write Session Memory
   └─ /memories/session/context-loaded.md
```

**Content:** Extracted decisions and patterns from prior features (read-only for session)

**Frequency:** Once per session (at `/spek.prepare` → `/spek.context`)

---

### Write Lifecycle: `/spek.post` (Feature End)

```
Timeline: Feature End
│
├─ Step 1: Collect Artifacts
│  ├─ spec.md (completed feature spec)
│  ├─ plan.md (implementation plan)
│  ├─ tasks.md (all tasks, marked complete)
│  └─ Execution trace (e.g., git log, test results)
│
├─ Step 2: Generate Lessons Learned
│  ├─ Extract: What We Built, How We Built It, Decisions, Patterns
│  └─ Output: vault/lessons/<date>-<feature>-<name>.md
│
├─ Step 3: Update Vault
│  ├─ Append new decisions → vault/decision.md
│  ├─ Add/refine patterns → vault/patterns.md
│  └─ Mark current feature lessons as complete
│
├─ Step 4: Sync to Repo Memory
│  ├─ Compress recent decisions → /memories/repo/architectural-decisions.md
│  ├─ Index recent patterns → /memories/repo/patterns-index.md
│  └─ Update codebase map → /memories/repo/codebase-map.md (if code structure changed)
│
├─ Step 5: Refresh Code Graph
│  └─ /spek.map (incremental: re-index changed files)
│
├─ Step 6: Archive Session Memory
│  └─ /memories/session/current-feature.md → archive (for reference)
│
└─ Step 7: Report Completion
   └─ "Feature complete. Lessons written to vault/lessons/. Decisions synced."
```

**Content:** Structured lessons learned from feature execution (written to vault)

**Frequency:** Once per feature (after implementation complete)

---

## Interaction with Copilot Memory Scopes

### User Memory (`/memories/`)

**Scope:** Persistent across all projects and sessions  
**Use Case:** User preferences, common patterns, lessons learned across projects

**Spekificity usage:**
- Copy patterns from one project's vault/patterns.md to user memory if broadly applicable
- User memory can reference vault patterns: "See spekificity vault/lessons/ for similar feature pattern"

**Example:**
```markdown
# /memories/patterns-across-projects.md

## Lesson-Based Documentation Pattern

Applied successfully in:
- spekificity project (feature 003): See vault/lessons/2026-05-18-003-*.md

Description: [pattern details]
```

### Session Memory (`/memories/session/`)

**Scope:** Current conversation only  
**Use Case:** Spekificity stores session context, feature progress, etc.

**Spekificity usage:**
- `/memories/session/context-loaded.md` — What was loaded at session start
- `/memories/session/current-feature.md` — Current feature progress
- `/memories/session/resolution.md` — Spec resolution notes (like this one)

### Repo Memory (`/memories/repo/`)

**Scope:** Project-persistent (survives session end, but only for this repo)  
**Use Case:** Spekificity stores compressed, frequently-accessed project context

**Spekificity usage:**
- `/memories/repo/architectural-decisions.md` — Active decisions (synced from vault after each feature)
- `/memories/repo/patterns-index.md` — Index of recent patterns
- `/memories/repo/codebase-map.md` — High-level code structure

**Retention Strategy:**
- Sync to repo memory after each feature (`/spek.post`)
- Keep only recent active context (e.g., last 3 features)
- Full archive stays in vault (vault/decision.md, vault/patterns.md, vault/lessons/)

---

## Query Patterns

### "What decisions are active?"

```bash
# Query repo memory (fast):
grep -A5 "^| .* | active |" /memories/repo/architectural-decisions.md

# Or query vault (complete):
grep -B2 "status.*active" vault/decision.md
```

### "What patterns exist for [topic]?"

```bash
# Query vault:
grep -l "[topic-tag]" vault/patterns.md

# Or query repo memory (recent only):
grep "[topic]" /memories/repo/patterns-index.md
```

### "What was learned from similar features?"

```bash
# Query lessons vault:
grep -l "[similar-domain]" vault/lessons/*.md | xargs cat

# Or query session memory (quick reminder):
grep -A10 "Patterns Applied" /memories/session/context-loaded.md
```

### "What's the current feature status?"

```bash
# Query session memory:
cat /memories/session/current-feature.md | grep -A5 "Current Status"
```

---

## Success Criteria

- [x] Memory architecture has three layers (vault, repo, session) with clear ownership
- [x] Per-feature lessons are self-contained and reusable
- [x] Per-decision entries capture rationale and impact
- [x] Patterns library is tagged and queryable
- [x] Load lifecycle is defined (what is read at session start, cost estimate)
- [x] Write lifecycle is defined (what is written at feature end, cost estimate)
- [x] Interaction with copilot memory scopes is clear
- [x] Granularity is explicit (per-feature, per-decision, per-pattern, per-session)
- [x] Retention policies are defined for each type
- [x] Query patterns are documented

---

## Implementation Checklist

- [ ] Update `/spek.context` skill to implement load lifecycle
- [ ] Update `/spek.post` skill to implement write lifecycle (already partially done in B.2/B.3)
- [ ] Create `/memories/repo/` template files (architectural-decisions.md, patterns-index.md, codebase-map.md)
- [ ] Create `/memories/session/` template files (context-loaded.md, current-feature.md)
- [ ] Document memory query patterns in a guide (wiki/memory-queries.md)
- [ ] Test memory lifecycle in a feature run (feature 003)

---

## Key Principles

1. **Single source of truth:** Vault is authoritative (Obsidian); repo memory is cached summary
2. **Explicit writes:** Memory is not auto-updated; `/spek.post` is the only write point
3. **Read-before-write:** `/spek.context` reads at session start; informed decisions follow
4. **Compression by default:** Session memory uses caveman format; repo memory keeps recent active only
5. **Granularity matters:** Per-feature, per-decision, per-pattern → queryable and specific
6. **Lifecycle is clear:** Define write trigger, read trigger, retention policy for each type
7. **Layering:** Ephemeral (session) → Repo (project) → Vault (authoritative)

---

## References

- **B.3:** Lessons learnt format (vault/lessons/ template)
- **extracted spec:** Code and document maps (vault/graph/, Obsidian export)
- **B.2/B.4:** `/spek.prepare` and `/spek.post` skills (write triggers)
- **Copilot docs:** /memories/ scope definitions and retention policies
- **Caveman:** Compression format for context summaries

---

## Future Enhancements

**Phase 2:**
- Semantic search across lessons (embeddings)
- Pattern recommendation: "This feature looks like pattern X, which was used in feature Y"
- Memory analytics: "Top 5 most-used patterns", "Most frequently changed decisions"
- Cross-project memory sync: Pull lessons from other projects via user memory

**Phase 3:**
- Interactive memory browser: CLI to query and visualize vault/graph/
- Memory conflict resolution: When decisions contradict, flag for review
- Automated pattern extraction: ML-based pattern discovery from implementation
