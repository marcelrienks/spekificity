# ATOMIC SPECIFICATION: Lessons Command (C4.6)

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Skill — /spek.lessons (manual lesson extraction + query interface)  
**Depends On:** lessons-format.md, memory-architecture.md, post-processing.md  
**Used By:** `/spek.post` (automatic), CLI entry point (manual queries)  

---

## Overview

`/spek.lessons` serves dual purpose: (1) automatic lesson generation called by `/spek.post` at feature end, and (2) manual query interface for searching + discovering past lessons. Lessons are extracted once at feature completion; immutable afterward.

---

## Execution Modes

### Mode 1: Automatic (Called by `/spek.post` Step 3)

**Entry point:** `/spek.post` internally invokes lesson generation (no user flag needed)

**Behavior:**
```
/spek.post step 3
  ├─ Collect artifacts (spec, plan, tasks, execution trace)
  ├─ Call /spek.lessons (internally, no user visibility)
  │  ├─ Generate 8-section lesson document
  │  ├─ Compress with caveman mode
  │  ├─ Write to vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md
  │  └─ Return: lesson file path + validation
  └─ Continue to Step 4 (vault update)
```

**Not a separate command invocation; embedded in `/spek.post` flow.**

---

### Mode 2: Manual Lesson Generation (Current Feature Only)

**Entry point:** User calls `/spek.lessons --regenerate` during feature work

**Syntax:**
```bash
spek lessons --regenerate [--dry-run]
```

**Behavior:**
1. Check current feature state (`vault/session/`)
2. Verify feature is NOT yet completed (phase < completing)
3. Read current artifacts (spec, plan, tasks, execution trace if exists)
4. Generate lesson document (same 8-section format as auto mode)
5. Write to temporary file (e.g., `/tmp/spek-lesson-preview.md`)
6. Output: Preview + "Lesson ready; run `/spek.post` to finalize"

**Use case:** Mid-feature validation (verify lessons will be comprehensive before `/spek.post`)

**Immutability rule:** Once `/spek.post` runs and feature moves to `completing`, `/spek.lessons --regenerate` is blocked (use error: "Feature already completed; lessons immutable").

---

### Mode 3: Pattern Query (Search Lessons by Pattern)

**Entry point:** User queries lessons containing specific pattern

**Syntax:**
```bash
spek lessons --pattern=<pattern-name> [--format=markdown]
```

**Behavior:**
1. Query vault/lessons/ for all files
2. Parse each lesson file (YAML frontmatter + content)
3. Search for pattern references (in "Patterns Identified" section + elsewhere)
4. Return: List of matching lessons (filename + excerpt)

**Example:**
```bash
$ spek lessons --pattern="dependency-injection"

=== Lessons Matching Pattern: dependency-injection ===

1. vault/lessons/2026-05-18-003-spek-full-workflow-cli.md
   Excerpt: "... reused dependency injection pattern from auth service, adapted for graph queries ..."

2. vault/lessons/2026-05-12-001-persistent-memories.md
   Excerpt: "... introduced dependency injection for vault access layer ..."

Total: 2 lessons
```

**Output format:** Markdown (list of matched lessons + excerpts)

## Success Criteria

- ✅ Automatic mode generates lessons in <10s (embedded in `/spek.post` Step 3)
- ✅ Manual regenerate mode works (preview lessons during feature)
- ✅ Pattern query discovers relevant lessons (search by pattern name)
- ✅ Full-text search finds lessons by keyword (grep-based query)
- ✅ Lessons immutable after completion (no regenerate post-feature)
- ✅ Query results returned in readable format (excerpts + context)
- ✅ Integration seamless (modes invoked transparently)\n\n---\n\n### Mode 4: Full-Text Search (Search Lessons by Keyword)"}}]

**Entry point:** User searches lessons for keyword

**Syntax:**
```bash
spek lessons --search=<keyword> [--limit=10] [--format=markdown]
```

**Behavior:**
1. Query vault/lessons/ for all files
2. Parse each lesson file (all sections)
3. Search for keyword (case-insensitive, substring match)
4. Rank by relevance (section weight: "Lessons for Next Feature" > "Decisions Made" > others)
5. Return: Top N lessons (default 10)

**Example:**
```bash
$ spek lessons --search="cache" --limit=5

=== Lessons Matching "cache" ===

1. vault/lessons/2026-05-15-002-code-graph-indexing.md (relevance: 0.92)
   Section: How We Built It
   Excerpt: "... implemented SHA256 caching for incremental graph refresh ..."

2. vault/lessons/2026-05-18-003-spek-full-workflow-cli.md (relevance: 0.67)
   Section: Lessons for Next Feature
   Excerpt: "... beware: graph cache can become stale if git hooks fail ..."

Total: 5 lessons (showing top 5)
```

**Output format:** Markdown (ranked list + excerpts)

---

## Detailed Syntax

### Command: `spek lessons`

```bash
spek lessons [mode] [options]

Modes:
  (automatic)           # No mode flag; called by /spek.post
  --regenerate          # Manual generation for current feature only
  --pattern=<name>      # Query lessons by pattern
  --search=<keyword>    # Full-text search

Global Options:
  --dry-run             # Preview output without writing
  --format=<format>     # Output format (markdown only; default markdown)
  --limit=<n>           # Max results to return (default: 10 for search, all for pattern)
  --help, -h            # Show help
```

---

## Step Details

### Automatic Mode (Called by `/spek.post`)

**Execution inside `/spek.post` Step 3:**

```
Step 3: Generate lessons
├─ Collect artifacts (spec, plan, tasks, execution trace)
├─ Extract 8 sections:
│  1. Header & metadata
│  2. What We Built
│  3. How We Built It
│  4. Key Tasks Executed
│  5. Decisions Made
│  6. Patterns Identified or Reused
│  7. Lessons for Next Feature
│  8. Metrics
├─ Compress with caveman mode (75% reduction)
├─ Write vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md
├─ Validate: self-contained checklist
│  ✓ Self-contained (readable without spec/plan)
│  ✓ Compressed (caveman format)
│  ✓ Actionable (concrete, not vague)
│  ✓ Specific (code examples, not general advice)
└─ Return: success + filepath
```

**See lessons-format.md for template + validation criteria**

---

### Manual Regeneration (During Feature Work)

**Invocation:** `/spek.lessons --regenerate [--dry-run]`

**Execution:**
```
1. Check feature state
   ├─ Verify phase != "completing" (block if already done)
   ├─ Verify current feature is active
   └─ Read artifacts (spec, plan, tasks, trace)

2. Generate lesson document
   ├─ Use same 8-section template
   ├─ Populate from current artifacts
   └─ Apply caveman compression

3. Output preview
   ├─ If --dry-run: show preview, don't write
   ├─ Else: write to /tmp/spek-lesson-preview.md
   ├─ Display: "Preview saved. Review output above."
   └─ Guidance: "Run /spek.post to finalize + archive."

4. Success
   └─ Exit 0 (preview generated)
```

**Error Handling:**
- No current feature active → error: "No active feature. Run `/spek.prepare` first."
- Feature already completed → error: "Feature 003 already completed. Lessons immutable."
- Missing artifacts → error: "tasks.md not found. Run `/spek.plan` first."

**Use Case Example:**
Developer wants to validate lessons midway through feature 003:
```bash
$ spek lessons --regenerate
Feature: 003 - spek-full-workflow-cli
Phase: implementing (1 of 5 tasks complete)

Generated lesson preview (not yet saved):
# Lesson: Spekificity Full Workflow CLI (Spec-003, 2026-05-20)
## What We Built
  Prepare + implement commands + feature state tracking. 
  ... [full 8 sections follow] ...

Action: Complete remaining tasks, then run /spek.post to finalize lessons.
Exit: spek lessons --regenerate (saved to /tmp/spek-lesson-preview.md for review)
```

---

### Pattern Query

**Invocation:** `/spek.lessons --pattern=<pattern-name>`

**Execution:**
```
1. Parse pattern name
   ├─ Validate: pattern exists in vault/patterns.md
   └─ Warn: "Pattern not found in library" if missing

2. Query vault/lessons/
   ├─ Load all .md files (YYYY-MM-DD-*.md)
   ├─ Parse YAML frontmatter + content
   ├─ Search for pattern mentions (regex: "pattern-name" or wikilink)
   └─ Collect matches

3. Format output (markdown)
   ├─ Header: "=== Lessons Matching Pattern: [name] ==="
   ├─ Per match:
   │  ├─ Lesson filename + date
   │  ├─ Excerpt (25 words max, context snippet)
   │  └─ Link to full lesson file
   └─ Footer: "Total: N lessons"

4. Output to stdout
```

**Example Output:**
```markdown
=== Lessons Matching Pattern: dependency-injection ===

1. **vault/lessons/2026-05-18-003-spek-full-workflow-cli.md** (May 18, 2026)
   Excerpt: "... reused DI pattern from auth service, adapted for graph layer ..."
   [View full](file:///vault/lessons/2026-05-18-003-spek-full-workflow-cli.md)

2. **vault/lessons/2026-05-12-001-persistent-memories.md** (May 12, 2026)
   Excerpt: "... introduced DI for vault access layer to enable mocking ..."
   [View full](file:///vault/lessons/2026-05-12-001-persistent-memories.md)

Total: 2 lessons found
```

---

### Full-Text Search

**Invocation:** `/spek.lessons --search=<keyword> [--limit=N]`

**Execution:**
```
1. Parse keyword
   ├─ Lowercase for case-insensitive search
   └─ Support wildcards: "cach*" matches "cache", "caching", etc.

2. Query vault/lessons/
   ├─ Load all .md files
   ├─ Parse each section separately
   ├─ Search for keyword (substring match)
   ├─ Rank by section relevance:
   │  ├─ 1.0x: "Lessons for Next Feature"
   │  ├─ 0.8x: "Decisions Made"
   │  ├─ 0.6x: "How We Built It"
   │  └─ 0.4x: others
   └─ Sort by relevance (descending)

3. Limit results (default: 10)
   └─ Return top N by relevance

4. Format output (markdown)
   ├─ Header: "=== Lessons Matching '[keyword]' ==="
   ├─ Per result:
   │  ├─ Rank + filename + date + relevance score
   │  ├─ Section where match found
   │  ├─ Excerpt (context, 30 words)
   │  └─ Link to full lesson
   └─ Footer: "Total: N lessons (showing top M)"

5. Output to stdout
```

**Example Output:**
```markdown
=== Lessons Matching "cache" ===

1. vault/lessons/2026-05-15-002-code-graph-indexing.md (Relevance: 0.92)
   Section: How We Built It
   Excerpt: "... implemented SHA256 caching for incremental graph refresh, reducing rebuild time from 60s to 3s ..."
   [View full](file:///vault/lessons/2026-05-15-002-code-graph-indexing.md)

2. vault/lessons/2026-05-18-003-spek-full-workflow-cli.md (Relevance: 0.67)
   Section: Lessons for Next Feature
   Excerpt: "... beware: graph cache can become stale if git hooks fail to run after commit ..."
   [View full](file:///vault/lessons/2026-05-18-003-spek-full-workflow-cli.md)

Total: 5 lessons found (showing top 2)
```

---

## Storage & Lifecycle

**Lesson Files:**
- Location: `vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md`
- Created by: `/spek.post` Step 3 (automatic)
- Immutable after creation (no updates)
- Retention: Permanent (archived if marked status=archived in frontmatter)

**Lesson Frontmatter (YAML):**
```yaml
---
title: "Lesson: [Feature Name]"
date: YYYY-MM-DD
feature_id: NNN
feature_name: name-from-branch
status: complete | archived
duration_days: X
duration_sessions: Y
spec_link: specs/NNN-feature-name.md
branch: NNN-feature-name
commit_range: abc123..def456
---
```

**Immutability Rule:**
- Once feature phase transitions to `completing`, lesson file is locked
- Manual `--regenerate` before `completing` is allowed
- Manual `--regenerate` after `completing` is blocked (error message)

---

## Success Criteria

✅ Automatic: Lessons generated at `/spek.post` Step 3  
✅ Manual: User can preview lessons before `/spek.post` with `--regenerate`  
✅ Pattern query: Returns all lessons mentioning pattern  
✅ Text search: Returns ranked results by relevance  
✅ Output: Markdown format with links + excerpts  
✅ Immutability: Once feature complete, lessons locked  

---

## Integration Points

**With `/spek.post`:**
- Called automatically at Step 3 (no manual invocation needed)
- Captures feature artifacts + writes lesson file
- Immutability enforced afterward

**With Memory Architecture:**
- Writes to vault/lessons/ (permanent storage)
- Read by `/spek.context` at session start (recent 3-5 lessons loaded)
- Indexed by code graph during `/spek.map` refresh

**With Lessons Format (lessons-format.md):**
- Uses 8-section template
- Applies Zettelkasten conventions (tags, wikilinks)
- Compressed with caveman mode

---

## Error Handling

| Scenario | Error | Action |
|----------|-------|--------|
| No current feature | "No active feature" | Prompt: Run `/spek.prepare` first |
| Feature already done | "Lessons immutable" | Suggest: Review existing lesson |
| Missing artifacts | "tasks.md not found" | Prompt: Run `/spek.plan` first |
| Pattern not found | "Pattern '[X]' not in library" | Show: Available patterns |
| Search timeout | "Search timeout (>5s)" | Show: Partial results, suggest refinement |

---

## Related Specifications

- [Lessons Format](lessons-format.md) — Template + validation
- [Memory Architecture](memory-architecture.md) — Lesson loading + lifecycle
- [Post Processing](post-processing.md) — Lesson generation workflow (Step 3)
- [Zettelkasten Conventions](zettelkasten-conventions.md) — Frontmatter + wikilinks
