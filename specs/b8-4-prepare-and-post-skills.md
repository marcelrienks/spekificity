# B.8.4 — Prepare and Post Skills Specifications

**Status:** SPECIFICATION (2026-05-18)  
**Feature:** spekificity feature 003 — Full Workflow CLI  
**Related:** [B.8.3 Integration Contract](b8-3-speckit-integration-contract.md), [B.8.2 Memory Architecture](b8-2-persistent-memories-and-lessons.md), [B.2 Skills Definitions](../wiki/skills/)

---

## Overview

This spec defines the exact ordered sequences, inputs/outputs, dependencies, and success criteria for two critical spekificity skills:

1. **`/spek.prepare`** — Workspace preparation and feature initialization (entry point for feature work)
2. **`/spek.post`** — Feature completion, lessons extraction, and vault synchronization (exit point for feature work)

Together, they bracket the feature lifecycle and ensure consistent context loading, workspace validation, lessons capture, and knowledge persistence.

---

## `/spek.prepare` — Workspace Preparation & Feature Initialization

### Purpose

Prepare the workspace for feature work by verifying git state, checking code graph freshness, loading context, and creating feature state tracking.

### Invocation

```bash
/spek.prepare [--feature-name="..."] [--skip-context] [--force-graph-refresh]
```

**Parameters:**
- `--feature-name` (optional): Explicit feature name (if not provided, infer from branch or prompt)
- `--skip-context` (optional): Skip `/spek.context` call (for resume scenarios)
- `--force-graph-refresh` (optional): Force code graph re-index regardless of freshness

**Common scenarios:**
- First time: `spek.prepare` (interactive, loads context)
- Resume after break: `spek.prepare --skip-context` (reuse context, verify git)
- Resume same session: `spek.prepare --skip-context` (no-op if already prepared)
- Force fresh graph: `spek.prepare --force-graph-refresh` (reindex all code)

### Execution Sequence

#### Step 1: Verify Git State (PRE-EXECUTION)

**Objective:** Ensure workspace is clean and on a feature branch

**Inputs:**
- Current git working directory
- Current git branch

**Process:**
1. Check if git repo exists
   - If not: Report error "Not a git repository", halt
2. Check if working directory is clean (no uncommitted changes)
   - If dirty: Ask user to commit or stash
   - If user declines: Halt with reminder
3. Check if on a feature branch
   - If on main/develop: Warn "You are on main/develop. Feature branches recommended."
   - Allow user to continue or create feature branch

**Output:**
- Git status: clean ✓
- Branch name: `<feature-branch>`
- Staging area: empty ✓

**Success Criteria:**
- Working directory is clean
- Branch exists (feature branch or main for new features)
- No untracked files that would interfere

**Error Handling:**
- If repo doesn't exist → Report "Not a git repository" + halt
- If working dir is dirty → Prompt to stash, allow override (--force-dirty)
- If on main + has uncommitted → Recommend feature branch creation

---

#### Step 2: Load Feature Name (if not provided)

**Objective:** Determine the feature name for this session

**Inputs:**
- `--feature-name` parameter (optional)
- Current branch name
- User interaction (if needed)

**Process:**
1. If `--feature-name` provided
   - Use provided name
   - Validate: alphanumeric + hyphens only, max 50 chars
2. Else if branch matches feature naming pattern (e.g., `feature/003-spek-full-workflow-cli`)
   - Extract feature number and name from branch
3. Else
   - Prompt user: "What is the feature name? (e.g., '003-spek-full-workflow-cli')"
   - Validate input

**Output:**
- Feature name: `<feature-name>`
- Feature ID (if present): `<feature-number>`

**Success Criteria:**
- Feature name is non-empty and valid
- Feature name matches project naming conventions
- Feature name can be used in file paths

**Error Handling:**
- If invalid name provided → Prompt again
- If user declines → Ask if resuming previous feature → use previous name or halt

---

#### Step 3: Check Code Graph Freshness (OPTIONAL, unless forced)

**Objective:** Verify code graph is reasonably fresh; offer refresh if stale

**Inputs:**
- `vault/graph/config.json` (refresh threshold)
- `vault/graph/nodes.jsonl` (last modified timestamp)
- Current timestamp

**Configuration:**
- `GRAPH_REFRESH_THRESHOLD` (default: 1 hour) — Time before graph considered stale
- `GRAPH_FORCE_REFRESH` (from `--force-graph-refresh` flag)

**Process:**
1. If `--force-graph-refresh` set
   - Skip freshness check; go to step 4 (refresh)
2. Else check graph age
   - `age = now() - vault/graph/nodes.jsonl.mtime`
   - If `age < GRAPH_REFRESH_THRESHOLD`
     - Graph is fresh ✓; skip refresh
   - If `age >= GRAPH_REFRESH_THRESHOLD`
     - Graph is stale; offer refresh
     - Prompt user: "Code graph is [X hours] old. Refresh? (y/n)"
     - If user says yes: go to step 4 (refresh)
     - If no: continue with old graph

**Output (if stale & user accepts):**
- Go to Step 4 (Refresh Code Graph)

**Output (if fresh or user declines):**
- Graph status: stale / fresh
- Last sync: `<timestamp>`
- Next: Continue to Step 5 (Load Context)

**Success Criteria:**
- User is aware of graph age
- User can force refresh if desired
- Decision is logged for debugging

**Error Handling:**
- If graph doesn't exist → Warn "No code graph found; run `/spek.map` after session start"
- If config.json missing → Use default threshold
- If user input invalid → Prompt again

---

#### Step 4: Refresh Code Graph (CONDITIONAL)

**Objective:** Re-index code and documentation if graph is stale or user forced refresh

**Inputs:**
- `--force-graph-refresh` flag (if set)
- Vault and code directory paths

**Process:**
1. Call `/spek.map` (which runs both code and doc graph passes)
   - Code pass: Run graphify, output to `vault/graph/nodes-code.jsonl`
   - Doc pass: Export from Obsidian, output to `vault/graph/nodes-docs.jsonl`
   - Merge: Combine both, output to `vault/graph/nodes.jsonl`
2. Validate merged output
   - Check file size > 0
   - Check valid JSONL format
   - Check node count >= threshold (e.g., 50 nodes)
3. If validation fails
   - Halt with error message
   - Suggest running `/spek.map` manually to debug

**Output:**
- `vault/graph/nodes.jsonl` (refreshed)
- Graph stats: `<N> code nodes, <M> doc nodes, <N+M> total`
- Refresh timestamp: `<timestamp>`

**Success Criteria:**
- Graph file exists and has valid content
- Node count is reasonable (not empty, not corrupted)
- Merge operation succeeded
- Timestamp is updated

**Error Handling:**
- If graphify fails → Report error from graphify, suggest manual fix
- If Obsidian export fails → Warn but continue (use stale export)
- If merge fails → Report corruption, suggest manual fix

---

#### Step 5: Load Context (`/spek.context` call)

**Objective:** Load all relevant context from vault, repo memory, and code graph

**Inputs:**
- `--skip-context` flag (if set, skip this step)
- Feature name (from Step 2)
- Code graph (from Step 4 or skipped if fresh)

**Process:**
1. If `--skip-context` flag set
   - Skip this step; reuse existing /memories/session/context-loaded.md
2. Else call `/spek.context`
   - Reads vault (decisions, patterns, recent lessons)
   - Reads repo memory (compressed context)
   - Queries code graph (recent symbols, files)
   - Summarizes with caveman (lite mode)
   - Writes to /memories/session/context-loaded.md
   - Cost: ~3-5K tokens
3. Read written context to confirm
   - Verify file exists and is non-empty

**Output:**
- `/memories/session/context-loaded.md` (created or reused)
- Context summary displayed to user (decisions, patterns, relevant lessons)

**Success Criteria:**
- Context file exists
- Context file is well-formed (YAML frontmatter + markdown)
- Context is not empty
- Relevant items (decisions, patterns) are present

**Error Handling:**
- If context loading fails → Log error but continue (context is optional)
- If context is empty → Warn user but continue
- If file write fails → Fall back to in-memory context

---

#### Step 6: Create Feature State Tracker

**Objective:** Initialize session memory for tracking feature progress

**Inputs:**
- Feature name (from Step 2)
- Context loaded (from Step 5)

**Process:**
1. Create `/memories/session/current-feature.md`
2. Write YAML frontmatter
   ```yaml
   ---
   feature_name: "<feature-name>"
   feature_id: "<feature-number>" (if present)
   status: "initialized"
   session_start: "<timestamp>"
   phase: "prepared"
   completion: 0%
   ---
   ```
3. Write initial sections
   - Feature Description
   - Goals (from context, if available)
   - Current Phase: Prepared
   - Progress Log
     - `[PREPARED] <timestamp> — Workspace initialized, context loaded, ready for `/spek.specify``

**Output:**
- `/memories/session/current-feature.md` (created)
- File is well-formed and parseable

**Success Criteria:**
- File exists at correct path
- YAML frontmatter is valid
- Progress log has at least one entry
- File is readable by agent

**Error Handling:**
- If file write fails → Report error, attempt to create alternative location
- If YAML is malformed → Fix and retry

---

#### Step 7: Report Ready Status

**Objective:** Summarize prepare status and next steps

**Inputs:**
- All outputs from Steps 1-6

**Process:**
1. Display prepare summary
   ```
   ✓ Prepare Complete
   ├── Git state: clean
   ├── Feature: <feature-name>
   ├── Branch: <branch-name>
   ├── Code graph: fresh (synced <N> mins ago)
   ├── Context loaded: <N> decisions, <M> patterns, <K> lessons
   ├── Feature state: /memories/session/current-feature.md
   └── Next step: Run `/spek.specify [feature description]` to start spec generation
   ```
2. Display any warnings (e.g., "Code graph is old; run `/spek.map` to refresh")
3. Display helpful links
   - Link to wiki/speckit-workflow.md (canonical flow)
   - Link to /memories/session/context-loaded.md (loaded context)

**Output:**
- User-visible summary
- No file changes

**Success Criteria:**
- Summary is displayed clearly
- User understands next steps
- Warnings are visible

**Error Handling:**
- If summary generation fails → Display minimal status
- If links are invalid → Skip links

---

### Prepare Success Criteria (Overall)

✅ Git workspace is clean and on valid branch  
✅ Feature name is determined and valid  
✅ Code graph is either fresh or refreshed  
✅ Context is loaded (decisions, patterns, lessons)  
✅ Feature state tracker created and initialized  
✅ User understands next steps  

### Prepare Input/Output Summary

| Aspect | Input | Output |
|--------|-------|--------|
| **Command** | `/spek.prepare [options]` | User-visible ready status |
| **Git** | Working dir state | Verified clean branch |
| **Feature** | `--feature-name` or branch or prompt | Feature name + ID |
| **Graph** | `vault/graph/nodes.jsonl` age | Fresh graph or skipped check |
| **Context** | Vault, repo memory, code graph | `/memories/session/context-loaded.md` |
| **State** | Previous feature state (if any) | `/memories/session/current-feature.md` |
| **Dependencies** | `/spek.context`, `/spek.map` | Ready for `/spek.specify` |

---

## `/spek.post` — Feature Completion & Vault Synchronization

### Purpose

Extract lessons from completed feature work, update vault with decisions and patterns, synchronize repo memory, refresh code graph, and archive session state.

### Invocation

```bash
/spek.post [--caveman-mode=full|lite|ultra] [--feature-state-path="..."] [--dry-run]
```

**Parameters:**
- `--caveman-mode` (optional, default: `full`): Compression mode for lessons (lite, full, or ultra)
- `--feature-state-path` (optional): Explicit path to feature state file (if not `/memories/session/current-feature.md`)
- `--dry-run` (optional): Simulate post-processing without writing to vault

**Common scenarios:**
- Normal completion: `spek.post` (compress lessons, update vault)
- Verbose output: `spek.post --caveman-mode=lite` (less compression)
- Test run: `spek.post --dry-run` (preview changes, don't write)

### Execution Sequence

#### Step 1: Collect Artifacts

**Objective:** Gather all feature work outputs

**Inputs:**
- Feature state file: `/memories/session/current-feature.md`
- Spec file: `spec.md`
- Plan file: `plan.md`
- Tasks file: `tasks.md`
- Execution trace (from `/spek.implement`)
- Code changes (git diff)

**Process:**
1. Read `/memories/session/current-feature.md`
   - Extract feature name, feature ID, status, phase, completion %
   - Validate file is well-formed
2. Check for required spec files
   - If `spec.md` missing → Warn but continue (may be partial feature)
   - If `plan.md` missing → Warn but continue
   - If `tasks.md` missing → Warn but continue
   - If none exist → Report "No spec/plan/tasks found; cannot extract lessons" + halt
3. Collect execution trace
   - Read task execution log (from `/spek.implement` output)
   - Extract task IDs, status (passed/failed/partial), timestamps
4. Collect code changes
   - Run `git diff --name-only` (list modified files)
   - Run `git diff` (actual code changes)
   - Count lines added/deleted
5. Collect any errors/warnings
   - Read stderr/exceptions from execution phase
   - Log file paths for reference

**Output:**
- Feature artifacts dictionary
  ```
  {
    "feature_name": "...",
    "feature_id": "...",
    "status": "...",
    "spec_file": "spec.md",
    "plan_file": "plan.md",
    "tasks_file": "tasks.md",
    "spec_content": "...",
    "plan_content": "...",
    "tasks_content": "...",
    "execution_trace": {...},
    "code_changes": {...},
    "errors": [...]
  }
  ```

**Success Criteria:**
- At least one artifact collected (spec or plan or tasks)
- Feature state is readable
- Code changes are accessible

**Error Handling:**
- If feature state missing → Prompt user to provide feature name
- If no artifacts → Report warning but continue
- If code diff fails → Log error, continue without code changes

---

#### Step 2: Activate Caveman Mode for Compression

**Objective:** Set up compression mode for lessons generation

**Inputs:**
- `--caveman-mode` parameter (default: `full`)
- Configuration from `.spekificity/config.yaml`

**Configuration:**
- `CAVEMAN_MODE_DEFAULT` (default: `full`) — lite, full, ultra, wenyan-lite, wenyan-full, wenyan-ultra
- `COMPRESSION_RULES` — Active voice, concrete, short, specific

**Process:**
1. Parse `--caveman-mode` parameter
   - If valid mode: use it
   - If invalid: warn and use default
2. Activate caveman mode in agent context
   - Load compression rules for chosen mode
   - Set token budget (e.g., ultra = 50% fewer tokens than full)
3. Log mode activation
   - "Caveman mode activated: <mode> (compression: ~<X>%)"

**Output:**
- Caveman mode active in agent context
- Compression rules loaded

**Success Criteria:**
- Mode is valid and supported
- Rules are loaded
- Mode setting is logged

**Error Handling:**
- If invalid mode → Warn and use default
- If caveman not installed → Continue without compression (log warning)

---

#### Step 3: Generate Lessons Document

**Objective:** Extract structured lessons from all artifacts

**Inputs:**
- Feature artifacts (from Step 1)
- Caveman mode (from Step 2)
- Lesson template: [B.3 Lessons Format](../specs/b3-structured-lessons.md)

**Process:**
1. Parse all artifacts into structured data
   - Spec: What were goals?
   - Plan: What was architecture?
   - Tasks: What were key tasks?
   - Execution: What was built?
   - Code: What files changed?
2. Generate 8-section lesson document (per B.3 template)
   - **What We Built** (1-2 paragraphs): Feature overview, goals, success criteria
   - **How We Built It** (1-2 paragraphs): Architecture, key design decisions
   - **Key Tasks** (bullet list): Top 3-5 most impactful tasks
   - **Decisions** (bullet list): Architectural or process decisions made
   - **Patterns** (bullet list): Reusable patterns discovered or applied
   - **Lessons for Next** (bullet list): What we'd do differently; cautions
   - **Metrics** (table): Effort estimate vs. actual, tests added, code change volume
   - **References** (bullet list): Spec file, plan file, tasks file, related issues/PRs
3. Compress using caveman mode
   - Apply compression rules (active voice, concrete, short, specific)
   - Target compression: lite (80% of original), full (60%), ultra (40%)
4. Create lesson file
   - File name: `vault/lessons/<YYYY-MM-DD>-<feature-id>-<feature-name>.md`
   - Example: `vault/lessons/2026-05-18-003-spek-full-workflow-cli.md`
   - Content: YAML frontmatter + 8 sections

**Output:**
- `vault/lessons/<date>-<feature-id>-<name>.md` (created)
- Lesson file is well-formed
- Token count reported (compressed vs. original)

**Success Criteria:**
- File exists at correct path
- All 8 sections are present
- Content is self-contained (readable in future without referring to spec files)
- Compression applied correctly

**Error Handling:**
- If artifact parsing fails → Log error, use partial data
- If compression fails → Continue with uncompressed
- If file write fails → Archive to alternative location

---

#### Step 4: Update Vault — Decisions

**Objective:** Extract and archive architectural decisions

**Inputs:**
- Feature artifacts (from Step 1)
- Lesson document (from Step 3)
- `vault/decision.md` (existing decisions)

**Process:**
1. Parse lessons for decisions
   - Look for "Decisions" section
   - Extract each decision statement
   - Add feature context (feature name, date, issue link if available)
2. For each decision, create entry
   - Status: active (default) or deprecated
   - Date: today
   - Feature: feature ID and name
   - Rationale: brief explanation
   - Impact: how it affects future work
   - Related: other decisions or patterns
3. Append new decisions to `vault/decision.md`
   - Group by date
   - Maintain chronological order
4. Validate merged file
   - Check YAML frontmatter
   - Check headings are unique
   - Check all entries have required fields

**Output:**
- `vault/decision.md` (updated)
- New decision entries appended
- File is well-formed

**Success Criteria:**
- All decisions from lesson are in vault
- No duplicates introduced
- File is readable
- Entry format is consistent

**Error Handling:**
- If decision already exists → Mark with "also seen in <feature>" instead of duplicate
- If vault/decision.md missing → Create it
- If file write fails → Log error, try backup location

---

#### Step 5: Update Vault — Patterns

**Objective:** Extract and refine reusable patterns

**Inputs:**
- Feature artifacts (from Step 1)
- Lesson document (from Step 3)
- `vault/patterns.md` (existing patterns)

**Process:**
1. Parse lessons for patterns
   - Look for "Patterns" section
   - Extract each pattern name
2. For each pattern:
   - Check if pattern already exists in vault
   - If exists: Update "Last Used", increment "Frequency"
   - If new: Create entry with "First Used" = today, "Frequency" = 1
3. Create or update pattern entry
   - Name: pattern name
   - First Used: date first seen
   - Last Used: today
   - Frequency: count of features using it
   - Summary: brief description
   - When to Use: conditions/scenarios
   - Implementation: code example or reference
   - Lessons Learned: what worked, what didn't
   - References: features that used this pattern
4. Append new patterns to `vault/patterns.md`
5. Validate merged file
   - Check YAML frontmatter
   - Check headings are unique
   - Check all entries have required fields

**Output:**
- `vault/patterns.md` (updated)
- New patterns added or existing patterns updated
- File is well-formed

**Success Criteria:**
- All patterns from lesson are in vault
- Existing patterns have "Last Used" updated
- Frequency count is accurate
- File is readable
- Entry format is consistent

**Error Handling:**
- If pattern already exists → Update existing entry (don't duplicate)
- If vault/patterns.md missing → Create it
- If file write fails → Log error, try backup location

---

#### Step 6: Incremental Code Graph Sync

**Objective:** Update code graph with newly written code

**Inputs:**
- Code changes (from Step 1)
- `vault/graph/config.json` (graph configuration)
- Existing `vault/graph/nodes.jsonl`

**Process:**
1. Extract affected files from code changes
   - Get list of modified files (from git diff)
2. Determine affected symbols
   - For each file: identify symbols (functions, classes, etc.) that changed
   - Use graphify to re-index only changed files
3. Run incremental graph pass
   - Code pass: Re-index only affected files; merge with existing nodes
   - Doc pass: Skip (docs unlikely to change during implementation)
   - Output: Updated `vault/graph/nodes.jsonl`
4. Validate merged graph
   - Check node count is reasonable (not dropped by >50%)
   - Check JSONL format is valid
   - Check references are consistent

**Output:**
- `vault/graph/nodes.jsonl` (updated)
- Graph stats: `<N> nodes updated, <M> new nodes`
- Sync timestamp updated

**Success Criteria:**
- Graph file is updated
- Changed symbols are indexed
- Graph is well-formed
- Node count is reasonable

**Error Handling:**
- If graphify fails → Log error but continue (graph is optional)
- If merge fails → Use old graph (don't corrupt)
- If validation fails → Restore previous version

---

#### Step 7: Sync Repo Memory

**Objective:** Update compressed project context in repo memory

**Inputs:**
- Decisions from vault (from Step 4)
- Patterns from vault (from Step 5)
- Codebase structure from code graph (from Step 6)

**Process:**
1. Update `/memories/repo/architectural-decisions.md`
   - Extract recent active decisions (last 3-5 features)
   - Compress summaries
   - Update last sync timestamp
2. Update `/memories/repo/patterns-index.md`
   - Extract top N patterns by frequency (default: top 20)
   - Include usage count and last used date
   - Update last sync timestamp
3. Update `/memories/repo/codebase-map.md`
   - Extract high-level code structure from graph
   - List main modules/packages
   - List recently changed symbols
   - Update last sync timestamp
4. Validate all three files
   - Check format is correct
   - Check content is non-empty

**Output:**
- `/memories/repo/architectural-decisions.md` (updated)
- `/memories/repo/patterns-index.md` (updated)
- `/memories/repo/codebase-map.md` (updated)

**Success Criteria:**
- All three files are updated
- Content is compressed and recent
- Files are readable
- Timestamps are current

**Error Handling:**
- If file write fails → Log error but continue
- If compression fails → Use uncompressed
- If no data to sync → Skip file

---

#### Step 8: Feature Documentation Simplification (Optional)

**Objective:** Run `/cel.docs.simplify` to consolidate feature-branch documentation

**Inputs:**
- Current feature branch name
- `wiki/` directory
- Feature-scoped docs (if created during implementation)

**Configuration:**
- `DOCS_SIMPLIFY_ENABLED` (default: true)
- `DOCS_SIMPLIFY_SCOPE` (default: feature-branch, options: feature-branch or full-wiki)

**Process:**
1. Check if docs simplification should run
   - If `DOCS_SIMPLIFY_ENABLED` = false: skip
   - If scope = full-wiki: warn (risky), require confirmation
2. Run `/cel.docs.simplify`
   - Feature-scoped: simplify docs created on this feature branch only
   - Target: eliminate redundancy, consolidate related docs
   - Output: Suggested changes (non-destructive review)
3. If `--dry-run` set
   - Display suggested changes, don't write
4. Else
   - Apply suggested changes
   - Log what was consolidated
   - Validate wiki is still well-formed

**Output:**
- Feature-scoped documentation simplified
- Log of changes made

**Success Criteria:**
- Docs are consolidated (if needed)
- Wiki remains well-formed
- No loss of content

**Error Handling:**
- If `/cel.docs.simplify` not available → Skip with warning
- If full-wiki scope requested → Require explicit confirmation
- If simplification fails → Log error but continue

---

#### Step 9: Archive Session Memory

**Objective:** Archive current feature state and prepare for next session

**Inputs:**
- `/memories/session/current-feature.md`
- `/memories/session/context-loaded.md`

**Process:**
1. Update current-feature.md
   - Set status: completed (or partial/abandoned)
   - Set phase: completed
   - Set completion: 100% (or actual %)
   - Add final entry to progress log: "[COMPLETED] <timestamp> — Feature archived"
2. Move (or copy) to archive
   - Archive location: `/memories/session/archive/<date>-<feature>.md`
   - Keep in session if user wants reference
   - Delete from session if cleanup desired
3. Delete context-loaded.md
   - User can reload on next session start
4. Log archival
   - Report what was archived

**Output:**
- `/memories/session/current-feature.md` archived or deleted
- `/memories/session/context-loaded.md` deleted
- Session cleaned up

**Success Criteria:**
- Feature state is preserved or deleted per user preference
- Session memory is cleaned up
- Archive location is clear

**Error Handling:**
- If file deletion fails → Log warning but continue
- If archive location doesn't exist → Create it

---

#### Step 10: Report Completion Status

**Objective:** Summarize post-processing results

**Inputs:**
- All outputs from Steps 1-9

**Process:**
1. Display post completion summary
   ```
   ✓ Post Complete
   ├── Lessons: vault/lessons/2026-05-18-003-spek-full-workflow-cli.md
   ├── Decisions: 3 new, 1 updated
   ├── Patterns: 2 new, 4 updated
   ├── Code graph: 47 nodes updated
   ├── Repo memory: synced (3 recent decisions, 20 patterns)
   ├── Docs simplified: 2 files consolidated
   └── Session archived: /memories/session/archive/2026-05-18-003.md
   ```
2. Display lessons summary
   - What was built
   - Key patterns identified
   - Lessons for next feature
3. Display next steps
   - "Ready for next feature: Run `/spek.prepare` to start"
   - Links to vault/lessons file, decisions, patterns

**Output:**
- User-visible completion summary
- No file changes

**Success Criteria:**
- Summary is clear and complete
- User understands what was captured
- User knows next steps

**Error Handling:**
- If summary generation fails → Display minimal status

---

### Post Success Criteria (Overall)

✅ All artifacts collected and validated  
✅ Lessons document created and compressed  
✅ Architectural decisions extracted and vaulted  
✅ Patterns identified and vaulted (or updated)  
✅ Code graph incremented with new symbols  
✅ Repo memory synced with recent context  
✅ Documentation simplified (optional)  
✅ Session memory archived  
✅ User understands what was captured  

### Post Input/Output Summary

| Aspect | Input | Output |
|--------|-------|--------|
| **Command** | `/spek.post [options]` | User-visible completion status |
| **Artifacts** | spec.md, plan.md, tasks.md, trace, code | Lesson document created |
| **Compression** | `--caveman-mode` | Compressed lessons (~50-75% reduction) |
| **Decisions** | Lesson decisions section | New entries in vault/decision.md |
| **Patterns** | Lesson patterns section | New/updated entries in vault/patterns.md |
| **Graph** | Code changes | Updated vault/graph/nodes.jsonl |
| **Memory** | Vault updates | Synced /memories/repo/* |
| **Docs** | Feature branch changes | Simplified wiki (feature-scoped) |
| **Session** | Feature state | Archived /memories/session/* |
| **Next** | Ready for next feature | Prompt to run `/spek.prepare` |

---

## Integration: Prepare ↔ Post Lifecycle

```
/spek.prepare (ENTRY)
├── Verify workspace (git, branch)
├── Load feature context (decisions, patterns)
├── Initialize feature state (/memories/session/current-feature.md)
└── Signal: Ready for /spek.specify
    ↓
/spek.specify → /spek.plan → /speckit.tasks → /spek.implement (FEATURE WORK)
├── Update feature state after each step
└── Collect execution artifacts
    ↓
/spek.post (EXIT)
├── Collect all artifacts
├── Generate lessons (compressed)
├── Update vault (decisions, patterns)
├── Sync repo memory
├── Archive session
└── Signal: Ready for next feature (/spek.prepare)
```

---

## Configuration & Customization

### .spekificity/config.yaml

```yaml
# Prepare Phase
prepare:
  graph_refresh_threshold_hours: 1
  require_feature_branch: true
  allow_dirty_working_dir: false
  auto_load_context: true

# Post Phase
post:
  caveman_mode_default: full
  caveman_modes:
    lite: 20%    # 20% compression (80% of original size)
    full: 40%    # 40% compression (60% of original size)
    ultra: 60%   # 60% compression (40% of original size)
  docs_simplify_enabled: true
  docs_simplify_scope: feature-branch  # feature-branch or full-wiki
  archive_session_memory: true
```

### vault/graph/config.json

```json
{
  "code_pass": {
    "enabled": true,
    "granularity": "symbol",
    "refresh_policy": "incremental"
  },
  "doc_pass": {
    "enabled": true,
    "granularity": "heading",
    "refresh_policy": "skip-on-post"
  },
  "merge": {
    "output_file": "vault/graph/nodes.jsonl",
    "validation": {
      "min_nodes": 50,
      "max_size_mb": 10
    }
  }
}
```

---

## Error Handling & Recovery

### Prepare Phase Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| Not a git repository | Working dir is not in a git repo | Guide user to init repo or change dir |
| Working directory dirty | Uncommitted changes exist | Prompt to commit/stash; allow override |
| Graph doesn't exist | `/spek.map` never run | Warn but continue; suggest `/spek.map` |
| Context load fails | Vault corrupt or unreachable | Continue without context; log error |
| Feature state write fails | Permissions or disk issue | Try alternative location or skip |

### Post Phase Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| No artifacts found | Feature never reached implement | Report warning; ask user to confirm |
| Lessons generation fails | Artifact parsing error | Log error; use partial data |
| Vault write fails | Permissions or corruption | Archive to alternative location |
| Graph sync fails | Graphify error | Log error; skip graph update |
| Caveman compression fails | Compression algorithm error | Continue without compression |
| Docs simplify fails | Wiki corruption | Skip; suggest manual review |

---

## Success Criteria & Validation

### Prepare Validation Checklist

- [ ] Git state verified (clean, valid branch)
- [ ] Feature name determined (and valid)
- [ ] Code graph freshness checked (and refreshed if needed)
- [ ] Context loaded (decisions, patterns, lessons)
- [ ] Feature state file created (well-formed)
- [ ] User reported ready status

### Post Validation Checklist

- [ ] Artifacts collected (spec, plan, tasks, trace, code)
- [ ] Lessons document created (8 sections, self-contained)
- [ ] Decisions extracted and vaulted
- [ ] Patterns identified/updated in vault
- [ ] Code graph incremented with new symbols
- [ ] Repo memory synced (decisions, patterns, codebase map)
- [ ] Documentation simplified (feature-scoped)
- [ ] Session memory archived
- [ ] Completion status reported to user

---

## Testing & Validation

### Test Prepare Phase

```bash
# Test 1: Fresh prepare (new feature)
/spek.prepare --feature-name="test-feature-001"
# Expected: context loaded, feature state created, ready status

# Test 2: Resume prepare (skip context)
/spek.prepare --skip-context
# Expected: git verified, graph checked, feature state updated, ready

# Test 3: Force graph refresh
/spek.prepare --force-graph-refresh
# Expected: code graph re-indexed, context reloaded
```

### Test Post Phase

```bash
# Test 1: Normal post (full compression)
/spek.post
# Expected: lessons generated, vault updated, repo memory synced

# Test 2: Dry run (no writes)
/spek.post --dry-run
# Expected: changes previewed, no vault modifications

# Test 3: Ultra compression
/spek.post --caveman-mode=ultra
# Expected: lessons highly compressed (~40% of original)
```

---

## References

**Related specs:**
- [B.8.3 Integration Contract](b8-3-speckit-integration-contract.md)
- [B.8.2 Memory Architecture](b8-2-persistent-memories-and-lessons.md)
- [B.8.1 Code and Document Maps](b8-1-code-and-document-maps.md)
- [B.3 Structured Lessons Format](../specs/b3-structured-lessons.md)

**Skill definitions:**
- [/spek.prepare skill](../wiki/skills/spek-prepare.md) (high-level)
- [/spek.post skill](../wiki/skills/spek-post.md) (high-level)
- [/spek.context](../wiki/skills/spek-context.md)

**Related systems:**
- SpecKit (external, canonical workflow)
- Caveman compression mode
- Obsidian vault system
- Code graph (via `/spek.map`)

