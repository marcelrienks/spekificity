# ATOMIC SPECIFICATION: Lessons Command (C4.6)


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Depends On:** lessons-format.md, memory-architecture.md, post-processing.md  
**Requires:** Obsidian CLI (recommended) for automated vault/lessons operations and persistent memory management
**Used By:** `/spek.conclude` (automatic), CLI entry point (manual queries)  

---


## Overview

`/spek.lessons` serves dual purpose: (1) automatic lesson generation called by `/spek.conclude` at feature end, and (2) manual query interface for searching + discovering past lessons. Lessons are extracted once at feature completion; immutable afterward.

---


## Success Criteria

- ✅ Automatic mode generates lessons quickly (embedded in `/spek.conclude` Step 3)
- ✅ Manual regenerate mode works (preview lessons during feature)
- ✅ Pattern query discovers relevant lessons (search by pattern name)
- ✅ Full-text search finds lessons by keyword (grep-based query)
- ✅ Lessons immutable after completion (no regenerate post-feature)
- ✅ Query results returned in readable format (excerpts + context)
- ✅ Integration seamless (modes invoked transparently)\n\n---\n\n### Mode 4: Full-Text Search (Search Lessons by Keyword)"}}]
- **Entry point:** User searches lessons for keyword
- **Syntax:**
- ```bash
- spek lessons --search=<keyword> [--limit=10] [--format=markdown]
- ```
- **Behavior:**
- Query vault/lessons/ for all files (via Obsidian CLI)
- Parse each lesson file (all sections)
- Search for keyword (case-insensitive, substring match)
- Rank by relevance (section weight: "Lessons for Next Feature" > "Decisions Made" > others)
- Return: Top N lessons (default 10)
- **Example:**
- $ spek lessons --search="cache" --limit=5
- === Lessons Matching "cache" ===
- vault/lessons/<date>-code-graph-indexing.md (managed via Obsidian CLI, relevance recorded)
- Section: How We Built It
- Excerpt: "... implemented SHA256 caching for incremental graph refresh ..."
- vault/lessons/<date>-spek-full-workflow-cli.md (managed via Obsidian CLI, relevance recorded)
- Section: Lessons for Next Feature
- Excerpt: "... beware: graph cache can become stale if git hooks fail ..."
- Total: recorded (omitted)
- **Output format:** Markdown (ranked list + excerpts)
- ## Detailed Syntax
- ### Command: `spek lessons`
- spek lessons [mode] [options]
- Modes:
- (automatic)           # No mode flag; called by /spek.conclude
- --regenerate          # Manual generation for current feature only
- --pattern=<name>      # Query lessons by pattern
- --search=<keyword>    # Full-text search
- Global Options:
- --dry-run             # Preview output without writing
- --format=<format>     # Output format (markdown only; default markdown)
- --limit=<n>           # Max results to return (default: 10 for search, all for pattern)
- --help, -h            # Show help
- ## Step Details
- ### Automatic Mode (Called by `/spek.conclude`)
- **Execution inside `/spek.conclude` Step 3:**
- Step 3: Generate lessons
- ├─ Collect artifacts (spec, plan, tasks, execution trace)
- ├─ Extract multiple sections (template-driven):
- │  1. Header & metadata
- │  2. What We Built
- │  3. How We Built It
- │  4. Key Tasks Executed
- │  5. Decisions Made
- │  6. Patterns Identified or Reused
- │  7. Lessons for Next Feature
- │  8. Metrics
- ├─ Compress with caveman mode (significant reduction)
- ├─ Write vault/lessons/<date>-<feature-id>-<name>.md
- ├─ Validate: self-contained checklist
- │  ✓ Self-contained (readable without spec/plan)
- │  ✓ Compressed (caveman format)
- │  ✓ Actionable (concrete, not vague)
- │  ✓ Specific (code examples, not general advice)
- └─ Return: success + filepath
- **See lessons-format.md for template + validation criteria**
- ### Manual Regeneration (During Feature Work)
- **Invocation:** `/spek.lessons --regenerate [--dry-run]`
- **Execution:**
- Check feature state
- ├─ Verify phase != "completing" (block if already done)
- ├─ Verify current feature is active
- └─ Read artifacts (spec, plan, tasks, trace)
- Generate lesson document
- ├─ Use same multi-section template
- ├─ Populate from current artifacts
- └─ Apply caveman compression
- Output preview
- ├─ If --dry-run: show preview, don't write
- ├─ Else: write to /tmp/spek-lesson-preview.md
- ├─ Display: "Preview saved. Review output above."
- └─ Guidance: "Run /spek.conclude to finalize + archive."
- Success
- └─ Exit 0 (preview generated)
- **Error Handling:**
- No current feature active → error: "No active feature. Run `/spek.prepare` first."
- Feature already completed → error: "Feature 003 already completed. Lessons immutable."
- Missing artifacts → error: "tasks.md not found. Run `/spek.plan` first."
- **Use Case Example:**
- Developer wants to validate lessons midway through feature 003:
- $ spek lessons --regenerate
- Feature: 003 - spek-full-workflow-cli
- Phase: implementing (progress recorded)
- Generated lesson preview (not yet saved):
- # Lesson: Spekificity Full Workflow CLI (Spec-003)
- ## What We Built
- Prepare + implement commands + feature state tracking.
- ... [full template sections follow] ...
- Action: Complete remaining tasks, then run /spek.conclude to finalize lessons.
- Exit: spek lessons --regenerate (saved to /tmp/spek-lesson-preview.md for review)
- ### Pattern Query
- **Invocation:** `/spek.lessons --pattern=<pattern-name>`
- Parse pattern name
- ├─ Validate: pattern exists in vault/patterns.md
- └─ Warn: "Pattern not found in library" if missing
- Query vault/lessons/
- ├─ Load all .md files (YYYY-MM-DD-*.md)
- ├─ Parse YAML frontmatter + content
- ├─ Search for pattern mentions (regex: "pattern-name" or wikilink)
- └─ Collect matches
- Format output (markdown)
- ├─ Header: "=== Lessons Matching Pattern: [name] ==="
- ├─ Per match:
- │  ├─ Lesson filename + date
- │  ├─ Excerpt (25 words max, context snippet)
- │  └─ Link to full lesson file
- └─ Footer: "Total: N lessons"
- Output to stdout
- **Example Output:**
- ```markdown
- === Lessons Matching Pattern: dependency-injection ===
- **vault/lessons/2026-05-18-003-spek-full-workflow-cli.md** (May 18, 2026)
- Excerpt: "... reused DI pattern from auth service, adapted for graph layer ..."
- [View full](file:///vault/lessons/2026-05-18-003-spek-full-workflow-cli.md)
- **vault/lessons/2026-05-12-001-persistent-memories.md** (May 12, 2026)
- Excerpt: "... introduced DI for vault access layer to enable mocking ..."
- [View full](file:///vault/lessons/2026-05-12-001-persistent-memories.md)
- Total: 2 lessons found
- ### Full-Text Search
- **Invocation:** `/spek.lessons --search=<keyword> [--limit=N]`
- Parse keyword
- ├─ Lowercase for case-insensitive search
- └─ Support wildcards: "cach*" matches "cache", "caching", etc.
- ├─ Load all .md files
- ├─ Parse each section separately
- ├─ Search for keyword (substring match)
- ├─ Rank by section relevance:
- │  ├─ 1.0x: "Lessons for Next Feature"
- │  ├─ 0.8x: "Decisions Made"
- │  ├─ 0.6x: "How We Built It"
- │  └─ 0.4x: others
- └─ Sort by relevance (descending)
- Limit results (default: 10)
- └─ Return top N by relevance
- ├─ Header: "=== Lessons Matching '[keyword]' ==="
- ├─ Per result:
- │  ├─ Rank + filename + date + relevance score
- │  ├─ Section where match found
- │  ├─ Excerpt (context, 30 words)
- │  └─ Link to full lesson
- └─ Footer: "Total: N lessons (showing top M)"
- vault/lessons/2026-05-15-002-code-graph-indexing.md (managed via Obsidian CLI, Relevance: 0.92)
- Excerpt: "... implemented SHA256 caching for incremental graph refresh, reducing rebuild time substantially ..."
- [View full](file:///vault/lessons/2026-05-15-002-code-graph-indexing.md)
- vault/lessons/2026-05-18-003-spek-full-workflow-cli.md (managed via Obsidian CLI, Relevance: 0.67)
- Excerpt: "... beware: graph cache can become stale if git hooks fail to run after commit ..."
- Total: 5 lessons found (showing top 2)
- ## Storage & Lifecycle
- **Lesson Files:**
- Location: `vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md` (managed via Obsidian CLI)
- Created by: `/spek.conclude` Step 3 (automatic)
- Immutable after creation (no updates)
- Retention: Permanent (archived if marked status=archived in frontmatter)
- **Lesson Frontmatter (YAML):**
- ```yaml
- title: "Lesson: [Feature Name]"
- date: YYYY-MM-DD
- feature_id: NNN
- feature_name: name-from-branch
- duration_days: X
- duration_sessions: Y
- spec_link: specs/NNN-feature-name.md
- branch: NNN-feature-name
- commit_range: abc123..def456
- **Immutability Rule:**
- Once feature phase transitions to `completing`, lesson file is locked
- Manual `--regenerate` before `completing` is allowed
- Manual `--regenerate` after `completing` is blocked (error message)
- ## Success Criteria
- ✅ Automatic: Lessons generated at `/spek.conclude` Step 3
- ✅ Manual: User can preview lessons before `/spek.conclude` with `--regenerate`
- ✅ Pattern query: Returns all lessons mentioning pattern
- ✅ Text search: Returns ranked results by relevance
- ✅ Output: Markdown format with links + excerpts
- ✅ Immutability: Once feature complete, lessons locked
- ## Integration Points
- **With `/spek.conclude`:**
- Called automatically at Step 3 (no manual invocation needed)
- Captures feature artifacts + writes lesson file
- Immutability enforced afterward
- **With Memory Architecture:**
- Writes to vault/lessons/ (permanent storage, via Obsidian CLI)
- Read by `/spek.context` at session start (recent lessons loaded)
- Indexed by code graph during `/spek.map` refresh
- **With Lessons Format (lessons-format.md):**
- Uses multi-section template
- Applies Zettelkasten conventions (tags, wikilinks)
- Compressed with caveman mode
- ## Error Handling
- Scenario | Error | Action | ----------|-------|-------- | No current feature | "No active feature" | Prompt: Run `/spek.prepare` first | Feature already done | "Lessons immutable" | Suggest: Review existing lesson | Missing artifacts | "tasks.md not found" | Prompt: Run `/spek.plan` first | Pattern not found | "Pattern '[X]' not in library" | Show: Available patterns | Search timeout | "Search timeout (short)" | Show: Partial results, suggest refinement
- ## Related Specifications
- [Lessons Format](021-lessons-format.md) — Template + validation
- [Memory Architecture](030-memory-architecture.md) — Lesson loading + lifecycle
- [Post Processing](post-processing.md) — Lesson generation workflow (Step 3)
- [Zettelkasten Conventions](020-zettelkasten-conventions.md) — Frontmatter + wikilinks


## Execution Modes


## Mode 1: Automatic (Called by `/spek.conclude` Step 3)

**Entry point:** `/spek.conclude` internally invokes lesson generation (no user flag needed)

**Behavior:**
```
/spek.conclude step 3
  ├─ Collect artifacts (spec, plan, tasks, execution trace)
  ├─ Call /spek.lessons (internally, no user visibility)
   │  ├─ Generate multi-section lesson document
  │  ├─ Compress with caveman mode
   │  ├─ Write to vault/lessons/<YYYY-MM-DD>-<feature-id>-<name>.md (via Obsidian CLI)
  │  └─ Return: lesson file path + validation
  └─ Continue to Step 4 (vault update)
```

**Not a separate command invocation; embedded in `/spek.conclude` flow.**

---


## Mode 2: Manual Lesson Generation (Current Feature Only)

**Entry point:** User calls `/spek.lessons --regenerate` during feature work

**Syntax:**
```bash
spek lessons --regenerate [--dry-run]
```

**Behavior:**
1. Check current feature state (`vault/session/`)
2. Verify feature is NOT yet completed (phase < completing)
3. Read current artifacts (spec, plan, tasks, execution trace if exists)
4. Generate lesson document (same multi-section template as auto mode)
5. Write to temporary file (e.g., `/tmp/spek-lesson-preview.md`)
6. Output: Preview + "Lesson ready; run `/spek.conclude` to finalize"

**Use case:** Mid-feature validation (verify lessons will be comprehensive before `/spek.conclude`)

**Immutability rule:** Once `/spek.conclude` runs and feature moves to `completing`, `/spek.lessons --regenerate` is blocked (use error: "Feature already completed; lessons immutable").

---


## Mode 3: Pattern Query (Search Lessons by Pattern)

**Entry point:** User queries lessons containing specific pattern

**Syntax:**
```bash
spek lessons --pattern=<pattern-name> [--format=markdown]
```

**Behavior:**
1. Query vault/lessons/ for all files (via Obsidian CLI)
2. Parse each lesson file (YAML frontmatter + content)
3. Search for pattern references (in "Patterns Identified" section + elsewhere)
4. Return: List of matching lessons (filename + excerpt)

**Example:**
```bash
$ spek lessons --pattern="dependency-injection"

=== Lessons Matching Pattern: dependency-injection ===

- vault/lessons/<date>-<feature>-spek-full-workflow-cli.md (managed via Obsidian CLI)
   Excerpt: "... reused dependency injection pattern from auth service, adapted for graph queries ..."

- vault/lessons/<date>-<feature>-persistent-memories.md (managed via Obsidian CLI)
   Excerpt: "... introduced dependency injection for vault access layer ..."

Total: recorded (omitted)
```

**Output format:** Markdown (list of matched lessons + excerpts)

