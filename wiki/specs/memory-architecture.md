# Memory Architecture: Persistent Memories, Session Context, and Load Lifecycle

**Status:** ATOMIC SPECIFICATION  
**Type:** Memory Layer — Three-layer model with lifecycle  
**Replaces:** context-load-lifecycle.md, session-memory.md, persistent-memories-and-lessons.md  
**Used By:** /spek.context, /spek.prepare, /spek.post (all enrichment layers read context)  

---

## Overview

Spekificity defines a coherent memory architecture with three layers: persisted vault (Obsidian), repo-scoped memories (Copilot), and session-scoped context (ephemeral). Each layer has explicit granularity, ownership, persistence, and lifecycle. This spec covers:

- **What** each memory layer stores and why
- **When** memory is read (load lifecycle) and written (write lifecycle)
- **How much** each operation costs (tokens, latency)
- **Caching** strategy to minimize token usage
- **Fallback** behavior when parts fail

---

## Three-Layer Memory Model

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

**Content (Template from specifications):**
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

**Write Trigger:** Feature complete: `/spek.post` step 3 → generate lessons → write to vault/lessons/

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

## Recent Active Decisions (Last 3 Features)

[Most impactful 5-10 decisions with 1-line summary each]
```

**Write Trigger:** Feature end: `/spek.post` step 4 → extract decisions from lessons → append to vault/decision.md and sync to repo memory

**Read Trigger:**
- Session start: `/spek.context` reads recent decisions → includes in context
- Spec writing: Agent queries "are there existing decisions about [topic]?" → grep vault/decision.md

**Retention Policy:**
- Vault: Keep all decisions (mark deprecated, don't delete)
- Repo Memory: Keep only top N recent decisions (e.g., last 3 features) to keep /memories/repo/ lean

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
```

**Write Trigger:** Feature end: `/spek.post` step 4 → identify new/refined patterns from lessons → append to vault/patterns.md with "Last Used" updated

**Read Trigger:**
- Spec writing: Agent queries "patterns for [domain]" → grep vault/patterns.md for tags
- Plan writing: Agent browses patterns → considers applicability to current feature

**Retention Policy:**
- Keep all patterns indefinitely (archive unused ones with `status: archived`)
- Tag by domain (e.g., #api, #database, #testing)

---

## Context Load Lifecycle

**Timing:** Session start (`/spek.prepare` → `/spek.context`)  
**Total Duration:** ~10-20 seconds  
**Total Cost:** ~3.5K tokens (or 0 with cache)

### Phase 0: Preparation (OFFLINE)

**Duration:** < 1 second | **Tokens:** 0

**Process:**
1. User or system triggers `/spek.context`
2. Command parsed
3. Validate vault exists and is accessible

---

### Phase 1: Vault Read (LOCAL FILE I/O)

**Duration:** 1-2 seconds | **Tokens:** 0 (local file reads)

**Process:**
1. Read vault/decision.md (active decisions only)
   - Filter to `status: active` entries
   - Extract decision titles + rationale
2. Read vault/patterns.md (recent patterns)
   - Filter to `status: active` entries
   - Filter to patterns used in last 3 features
   - Extract pattern names + tags
3. Read vault/lessons/ (most recent)
   - List files, sort by date
   - Read 3-5 most recent files
   - Extract: What We Built, How We Built It, Key Patterns, Key Lessons
4. Read /memories/repo/ (if exists)
   - Read /memories/repo/architectural-decisions.md
   - Read /memories/repo/patterns-index.md

**Error Handling:**
- If vault/decision.md missing → Log warning, continue without decisions
- If vault/patterns.md missing → Log warning, continue without patterns
- If vault/lessons/ empty → Log info, continue without recent lessons
- If repo memory missing → Log info (created at first feature end)

---

### Phase 2: Code Graph Query (LOCAL FILE I/O)

**Duration:** 1-2 seconds | **Tokens:** 0 (local file reads)

**Process:**
1. Validate code graph freshness
   - Read vault/graph/config.json
   - Check last_incremental_sync timestamp
   - If age > GRAPH_REFRESH_THRESHOLD (default: 1 hour) → warn user
   - Proceed anyway (use old graph)
2. Read code graph summary
   - Read vault/graph/nodes.jsonl (first 50 lines or ~5KB)
   - Extract node types: function, class, module, document
   - Count by language
   - Identify most recently modified files
3. High-level structure summary
   - Extract top-level modules/packages
   - Extract recently changed files
   - Identify code hotspots (files with most connections)

**Error Handling:**
- If vault/graph/ missing → Log warning, proceed without code context
- If graph corrupted → Log error, attempt to recover or skip
- If graph very old (> 7 days) → Warn strongly

---

### Phase 3: Context Summarization (LLM CALL)

**Duration:** 5-15 seconds | **Tokens:** ~3-5K tokens (with compression)

**Process:**
1. Construct context briefing prompt with:
   - Recent decisions from Phase 1
   - Recent patterns from Phase 1
   - Code structure from Phase 2
   - Recent lessons from Phase 1

2. Call Claude Haiku (fast + cheap for summarization)
   - Temperature: 0.3 (low creativity; fact-focused)
   - Max tokens: 2000 (keep summary compact)
   - System: "You compress technical context into caveman mode (active voice, concrete, short)"

3. Receive summarized context

4. Compress to caveman format
   - Active voice: "We chose X" not "X was chosen"
   - Concrete: "Decorator pattern" not "a flexible approach"
   - Short: 1-2 sentences per item
   - Specific: "Use for SpecKit integration" not "use in many places"

**Cost Analysis:**
- Input tokens: ~2.5K (context briefing)
- Output tokens: ~1K (compressed summary)
- Total: ~3.5K tokens
- Latency: 5-15 seconds

**Error Handling:**
- If LLM call fails → Use uncompressed context (raw vault text)
- If response is empty → Retry once, then fallback
- If response corrupted → Use most recent cache

---

### Phase 4: Session Memory Write (LOCAL FILE I/O)

**Duration:** < 1 second | **Tokens:** 0

**Process:**
1. Create /memories/session/context-loaded.md
   - YAML frontmatter (session_date, timestamp, token usage)
   - Context summary (from Phase 3)
   - Decisions + patterns + code structure + lessons (raw)
   - Timestamps and cache hit info

2. Validate file created
   - Check file exists
   - Check file size > 100 bytes (not empty)
   - Check YAML is parseable

**Error Handling:**
- If file write fails → Log error, continue (context is in agent memory anyway)
- If file is empty → Log error, retry write

---

## Complete Load Lifecycle Flow

```
User: /spek.context
  ├─ Phase 0: Prepare (< 1s, 0 tokens)
  ├─ Phase 1: Vault Read (1-2s, 0 tokens)
  │  ├─ Read vault/decision.md
  │  ├─ Read vault/patterns.md
  │  ├─ Read vault/lessons/ (top 3-5)
  │  └─ Read /memories/repo/ (if exists)
  ├─ Phase 2: Code Graph Query (1-2s, 0 tokens)
  │  ├─ Validate graph freshness
  │  ├─ Read vault/graph/config.json
  │  ├─ Read first 50 lines of vault/graph/nodes.jsonl
  │  └─ Extract summary
  ├─ Phase 3: Summarization (5-15s, ~3.5K tokens)
  │  ├─ Construct briefing
  │  ├─ Call LLM (Claude Haiku)
  │  └─ Compress with caveman mode
  ├─ Phase 4: Session Write (< 1s, 0 tokens)
  │  ├─ Create /memories/session/context-loaded.md
  │  └─ Validate creation
  └─ Output: Context loaded summary (user visible)
     Total: ~10-20 seconds, ~3.5K tokens
```

---

## Caching Strategy

### Input Caching (Vault Reads)

**Cache Key:** Vault file modification times  
**Validation:** Check if vault/decision.md, vault/patterns.md, vault/lessons/ have changed

**Process:**
1. First `/spek.context` call → Read all vault files
2. Store hashes in /memories/session/context-cache.json
3. On next `/spek.context` call → Check current hashes
4. If hashes match → Reuse previous read (skip Phase 1)
5. If hashes differ → Re-read changed files

**Benefit:** Skip vault I/O if vault unchanged (speeds up context refresh mid-session)

---

### Output Caching (Summarization)

**Cache Key:** Vault content + code graph content  
**Validation:** Check if vault/code graph have changed

**Process:**
1. First `/spek.context` call → Summarize, store result
2. Compute cache key: `hash(vault_content + graph_content)`
3. On next `/spek.context` call → Check if key matches
4. If matches → Reuse previous summary (skip Phase 3, save ~3.5K tokens)
5. If differs → Re-summarize

**Benefit:** Skip LLM call if context unchanged (saves tokens and latency)

---

## Session Memory Files

### /memories/session/context-loaded.md

**Purpose:** Summary of what was loaded into context at session start (decisions, patterns, lessons, code structure).

**Structure:**
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

[Full decision summaries]

---

## Recent Patterns Available (Last 3 Features)

- **Decorator Wrapper Pattern** (5 uses) — SpecKit integration layer
- **Lesson-Based Documentation** (3 uses) — Feature capture

[Full pattern descriptions]

---

## Code Structure Summary

**Code Graph Freshness:** synced 45 mins ago ✓  
**Total Symbols:** 423 code nodes, 45 doc nodes  
**Primary Languages:** python (67%), typescript (21%), markdown (12%)  

[Module summaries]

---

## Lessons Quick Reference

**Most Relevant Lessons:**
- [Lesson 1 from spec-003]: Key takeaway
- [Lesson 2 from spec-002]: Key takeaway

---

## Important Constraints

- [Active decision that limits design space]
- [Performance requirement or limitation]
```

**Write Triggers:**
- Session start: `/spek.context` reads at feature start
- /spek.prepare step 5

**Read Triggers:**
- Throughout session for reference
- Between turns to maintain orientation

**Retention Policy:**
- Delete at session end (ephemeral)
- Or: Compress and archive to /memories/session/archive/ if valuable

---

### /memories/session/current-feature.md

**Purpose:** Progress tracking for the feature currently being worked on (spans multiple sessions if feature is long).

**Structure:**
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

---

## Feature Description

[1-3 sentence overview]

---

## Goals

- [ ] Goal 1: [specific, measurable]
- [ ] Goal 2: [specific, measurable]

---

## Progress by Phase

### Specifying (0% complete)
- [ ] Spec draft

### Planning (0% complete)
- [ ] Plan draft

### Implementing (0% complete)
- [ ] Tasks generated

### Completing (0% complete)
- [ ] All tasks done

---

## Decisions Made This Feature

- [Decision 1: rationale]
- [Decision 2: rationale]

---

## Patterns Applied

- [Pattern 1: where/how applied]

---

## Session Log

**Session 1 (2026-05-19 10:00-11:30):**
- [PREPARED] Workspace verified, context loaded

---

## Known Blockers

- [Blocker 1: impact, workaround]

---

## Next Steps

1. Run `/spek.automate [feature description]`
2. Review generated artifacts
3. Run `/spek.implement`
```

**Write Triggers:**
- Feature start: `/spek.prepare` creates with initialized status
- End of each session: Updates progress
- Feature end: `/spek.post` archives and converts to lessons

**Read Triggers:**
- Feature continuation: Agent reads at session start to resume work
- Between turns: Agent updates as work progresses

**Retention Policy:**
- Keep during feature work (spans multiple sessions)
- Archive to /memories/session/archive/ after feature completes
- Delete after N days (default: 30 days after feature ends)

---

## Load/Write Lifecycle Summary

### Load Lifecycle: `/spek.context` (Session Start)

```
Timeline: Session Start
├─ Step 1: Read Vault (Phase 1)
├─ Step 2: Read Repo Memory (Phase 1)
├─ Step 3: Query Code Graph (Phase 2)
├─ Step 4: Summarize & Compress (Phase 3)
└─ Step 5: Write Session Memory (Phase 4)
```

**Content:** Extracted decisions and patterns from prior features (read-only for session)

**Frequency:** Once per session (at `/spek.prepare` → `/spek.context`)

---

### Write Lifecycle: `/spek.post` (Feature End)

```
Timeline: Feature End
├─ Step 1: Collect Artifacts (spec, plan, tasks, execution trace)
├─ Step 2: Generate Lessons Learned
├─ Step 3: Update Vault (append decisions, patterns)
├─ Step 4: Sync to Repo Memory
├─ Step 5: Refresh Code Graph (incremental update)
├─ Step 6: Archive Session Memory
└─ Step 7: Report Completion
```

**Content:** Structured lessons learned from feature execution (written to vault)

**Frequency:** Once per feature (after implementation complete)

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
```

---

## Configuration

### .spekificity/config.yaml

```yaml
context_loading:
  # Enable caching?
  enable_cache: true
  cache_expiry_minutes: 60  # Re-summarize after this long
  
  # Model for summarization
  model: "claude-haiku-4.5"  # Fast + cheap
  temperature: 0.3  # Low creativity
  max_tokens_output: 2000
  
  # Token limits (by mode)
  token_limits:
    standard: 3500
    lite: 2000
    ultra: 1000
  
  # Graph freshness threshold
  graph_stale_threshold_hours: 1
  
  # How many items to include
  recent_decisions_count: 5
  recent_patterns_count: 5
  recent_lessons_count: 3
```

---

## Success Criteria

- [x] Memory architecture has three layers (vault, repo, session) with clear ownership
- [x] Per-feature lessons are self-contained and reusable
- [x] Per-decision entries capture rationale and impact
- [x] Load lifecycle is defined (what, when, how, costs)
- [x] Write lifecycle is defined (what, when, how)
- [x] Caching strategy minimizes token usage
- [x] Session memory files are ephemeral
- [x] Query patterns are documented
- [x] Fallback behavior is graceful

---

## References

**Related Specs:**
- [context-layer.md](context-layer.md) — Context composition and injection
- [decorator-wrapper-pattern.md](decorator-wrapper-pattern.md) — How enrichment wraps SpecKit
- [session-memory.md](session-memory.md) — (merged into this spec)
- [persistent-memories-and-lessons.md](persistent-memories-and-lessons.md) — (merged into this spec)
- [context-load-lifecycle.md](context-load-lifecycle.md) — (merged into this spec)

**External:**
- [Copilot docs](/memories/ scope definitions and retention policies
- [Caveman](caveman-integration.md) — Compression format for context summaries
