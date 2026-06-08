# Agent Skills Registration Contract

**Purpose**: Define the format and interface for registering agent skills with Claude Code. All four workflow commands (`prepare`, `plan`, `implement`, `conclude`) are defined as agent skills in `.claude/skills/` directory.

---

## File Structure & Location

**Location**: `.claude/skills/` (project root)

**Naming Convention**: kebab-case with `spek-` prefix
- `spek-prepare.md`
- `spek-plan.md`
- `spek-implement.md`
- `spek-conclude.md`

**File Format**: Markdown with YAML frontmatter (optional) + descriptive sections

---

## Skill Definition Template

Each agent skill file follows this structure:

```markdown
# Skill: [Display Name]

**Invocation**: `/spek.[name]`

## Purpose
One-line purpose statement

## Usage
/spek.[name] [args] [options]

## What It Does
1. Step 1: Detailed action
2. Step 2: Detailed action
3. Step 3: Detailed action

## Workflow Details

### Phase 1: Context Loading
- Load vault (decisions, patterns, lessons)
- Load code index (lat.md)
- Load constitution (principles)
- Format context for agent

### Phase 2: [Phase Name]
- Detailed workflow step

### Phase N: Output & Persistence
- Generate artifacts
- Log decisions to vault
- Update code index if needed

## Output
- `artifact1.md` — Description
- `artifact2.md` — Description

## Context Requirements
- vault: decisions, patterns, lessons
- code-index: lat.md graph
- constitution: project principles

## Related Skills
- `/spek.related-skill` — How this skill relates

## Examples

### Example 1: Basic Usage
\`\`\`
/spek.prepare "Add authentication to API"
\`\`\`

Expected output:
- Feature context loaded
- Related decisions displayed
- Recommended files listed

## Invocation Variants

### With Options
\`\`\`
/spek.prepare --compressed --no-index
\`\`\`

### Chaining
\`\`\`
/spek.prepare "Auth" → /spek.plan → /spek.implement → /spek.conclude
\`\`\`

## Documentation
See [wiki/skills.md](../../wiki/skills.md#spek.name) for full specification.
```

---

## Individual Skill Contracts

### Skill 1: `/spek.prepare`

**File**: `spek-prepare.md`

**Invocation**: `/spek.prepare [feature-name]`

**Purpose**: Load prior context, index codebase, present onboarding summary

**Required Context**:
- `vault`: decisions, patterns, lessons
- `code-index`: lat.md graph (optional; graceful if unavailable)
- `constitution`: project principles

**Workflow**:
1. Load vault (decisions, patterns, lessons)
2. Load code index via lat.md (or fallback to semantic search)
3. Load constitution
4. Format context for presentation
5. Display onboarding summary:
   - Prior decisions (first 3)
   - Relevant patterns (first 3)
   - Relevant code files (first 3)
   - Context summary (token estimate)
6. Suggest next step: `/spek.plan`

**Output**:
- Console: Formatted context display
- No artifacts created (preparation only)

**Artifacts Generated**: None (preparation phase)

**Decisions Logged**: None (passive phase)

---

### Skill 2: `/spek.plan`

**File**: `spek-plan.md`

**Invocation**: `/spek.plan [feature-name|spec-file]`

**Purpose**: Generate spec, identify ambiguities, plan implementation

**Required Context**:
- `vault`: decisions, patterns for enrichment
- `code-index`: lat.md for impact analysis
- `constitution`: principles

**Workflow**:
1. Load vault context
2. Load code index
3. Load constitution
4. **Phase 1: Specification**
   - Run `/speckit.specify` with context enrichment
   - Present spec to user for review/correction
   - Request approval or revisions
5. **Phase 2: Clarification** (interactive)
   - Identify ambiguities in spec
   - Ask clarification questions (up to 5)
   - Collect user answers
   - Update spec with clarifications
   - Loop until no ambiguities remain
6. **Phase 3: Planning**
   - Run `/speckit.plan` with enriched spec
   - Identify code sections to modify (lat.md analysis)
   - Estimate token budget per phase
   - Present plan to user for review
   - Request approval or revision
7. **Phase 4: Task Breakdown**
   - Run `/speckit.tasks` to generate task list
   - Add pattern suggestions and decision references
   - Present task list for review
   - Request approval or revision
8. **Persistence**:
   - Write spec.md, plan.md, tasks.md to `specs/{feature}/`
   - Log planning decisions to vault
   - Update code index (if code changed during planning)

**Output**:
- `specs/{feature-slug}/spec.md` — Feature specification
- `specs/{feature-slug}/plan.md` — Implementation plan
- `specs/{feature-slug}/tasks.md` — Task list
- Console: Phase progress, approval prompts, remediation guidance

**Artifacts Generated**:
- spec.md
- plan.md
- tasks.md

**Decisions Logged**:
- Architecture decisions (if diverged from assumptions)
- Technology choices (if made during planning)
- Clarifications resolved (in decision log)

**Remediation Loop**: After each phase, user can request revisions. If approved, continue to next phase. If revision needed, reprocess from failure point with updated input.

---

### Skill 3: `/spek.implement`

**File**: `spek-implement.md`

**Invocation**: `/spek.implement [feature-name|spec-file] [--steps N] [--resume]`

**Purpose**: Execute tasks with context injection, track progress, log decisions

**Required Context**:
- `vault`: decisions, patterns for task context
- `code-index`: lat.md for code recommendations
- `constitution`: principles

**Workflow**:
1. Load spec.md, plan.md, tasks.md from `specs/{feature}/`
2. Load vault context for task execution
3. Load code index for relevant code examples
4. Load constitution for principle references
5. **For each task** (or starting at --steps N):
   - Inject task context (decisions, patterns, code examples)
   - Ask for confirmation before major code changes
   - Log task progress to vault
   - Execute task implementation
   - Capture new decisions during implementation
   - Mark task complete or defer
6. **Progress Tracking**:
   - Track token usage against budget (warn if exceeded)
   - Prompt for alternative approaches if budget low
   - Suggest pattern references based on code context
   - Record deviations from spec in log
7. **Persistence**:
   - Commit code changes with spec/plan linkage
   - Append new decisions to vault/decisions.md
   - Update progress log for feature
   - Increment task completion status

**Output**:
- Modified source code (per tasks)
- Console: Task progress, context injection, confirmation prompts
- Progress log: Task status, decisions, deviations

**Artifacts Generated**: None (modifications to existing code)

**Decisions Logged**:
- New design decisions made during implementation
- Deviations from spec with rationale
- Tech stack decisions (if made during implementation)
- Pattern usage (if new patterns applied)

**Interactive Elements**:
- Confirmation before major changes
- Token budget warnings
- Pattern suggestions
- Decision capture prompts

---

### Skill 4: `/spek.conclude`

**File**: `spek-conclude.md`

**Invocation**: `/spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]`

**Purpose**: Analyze outcomes, extract lessons, update vault, refresh project state

**Required Context**:
- `vault`: existing decisions, patterns for comparison
- `code-index`: lat.md for code state analysis
- `constitution`: principles

**Workflow**:
1. Load vault (decisions, patterns, lessons)
2. Load code index (final state)
3. Load implementation logs from previous `/spek.implement` runs
4. **Phase 1: Analysis**
   - Run `/speckit.analyze` — validate implementation against spec
   - Compare success criteria vs actual outcomes
   - Identify any spec drift or deviations
   - Flag contradictions or risks
   - Generate analysis report
5. **Phase 2: Lessons Extraction** (interactive)
   - Prompt for retrospective: What went well?
   - Prompt for retrospective: What to improve?
   - Extract new patterns if workflow diverged from spec
   - Log new decisions if architecture changed
   - Update success criteria if spec changed during implementation
6. **Phase 3: Vault Updates**
   - Archive spec + plan + tasks + execution trace to `vault/archive/{date}-{feature}/`
   - Generate lessons document to `vault/lessons/{date}-{feature}.md`
   - Update `vault/patterns.md` with new patterns (if any)
   - Update `vault/decisions.md` with new decisions (if any)
7. **Phase 4: Repository State Sync**
   - Sync repo memory (architectural decisions, pattern index) to `.spek/memory/`
   - Refresh lat.md code graph via `/lat.sync` (incremental)
   - Update graph exports + metadata
   - Refresh Obsidian vault graph via CLI (if available)
8. **Phase 5: Completion**
   - Archive current feature session state
   - Report analysis + lessons + synced artifacts
   - Suggest next feature: `/spek.prepare [next-feature]`

**Output**:
- Console: Analysis report, lessons summary, sync status
- Artifacts: 
  - `vault/lessons/{date}-{feature}.md` — Lessons document
  - `vault/archive/{date}-{feature}/` — Archived spec/plan/tasks
  - Updated `vault/patterns.md` and `vault/decisions.md`
  - Updated `.spek/memory/` with synced state

**Artifacts Generated**:
- vault/lessons/{date}-{feature}.md
- vault/archive/{date}-{feature}/{spec,plan,tasks}.md
- Updated vault/patterns.md
- Updated vault/decisions.md

**Decisions Logged**:
- New patterns extracted (if workflow diverged)
- Architecture changes (if made during implementation)
- Success criteria updates (if spec changed)
- Lessons captured (non-structured, narrative form)

**Optional Features**:
- `--caveman-mode`: Compress all output (full/lite/ultra)
- `--dry-run`: Show what would be updated without persisting
- Obsidian CLI export (optional; graceful failure if unavailable)

---

## Context Injection Pattern

Each agent skill follows this pattern for context loading and formatting:

```python
# Pseudo-code for context injection in agent skill

# 1. Load context
vault = load_vault(project_root)
decisions = vault.load_decisions()
patterns = vault.load_patterns()
lessons = vault.load_lessons()

code_index = load_index(project_root)
relevant_files = code_index.query(feature_intent, max_results=10)

constitution = load_constitution(project_root)

# 2. Format context
context_text = format_context(
    decisions=decisions,
    patterns=patterns,
    lessons=lessons,
    relevant_files=relevant_files,
    constitution=constitution
)

# 3. Compress if requested
if caveman_mode:
    context_text = compress(context_text, caveman_mode)

# 4. Inject into agent prompt
prompt = f"""
{WORKFLOW_INSTRUCTIONS}

## Project Context

{context_text}

## User Input

{user_input}
"""

# 5. Capture decisions during workflow execution
captured_decisions = capture_decisions_from_execution()

# 6. Persist decisions to vault
vault.append_decisions(captured_decisions)
```

---

## Skill Discovery & Invocation

**How Claude Code discovers these skills**:
1. Reads `.claude/skills/` directory
2. Parses each `.md` file
3. Extracts skill name from filename (spek-prepare.md → spek-prepare)
4. Registers skill for invocation via `/spek-prepare` syntax

**User Invocation**:
```bash
# From Claude Code chat
/spek.prepare "Add authentication"
/spek.plan
/spek.implement --steps 2
/spek.conclude --dry-run
```

**Error Handling**:
- Skill not found → "Skill '/spek.unknown' not registered"
- Context loading fails → "Error loading vault context: [details]"
- SpecKit not installed → "SpecKit v0.9.6+ required. Install: uv tool install speckit"
- User cancels workflow → "Workflow cancelled. No changes persisted."

---

## Summary

Agent skills follow a consistent contract:
1. **Registration**: Markdown files in `.claude/skills/` with `spek-` prefix
2. **Context Loading**: Vault + code-index + constitution loaded before execution
3. **Workflow Execution**: Documented phases with user interaction points
4. **Decision Persistence**: New decisions logged to vault/decisions.md
5. **Error Handling**: Graceful degradation with helpful messages
6. **Chaining**: Skills are designed to chain (prepare → plan → implement → conclude)

Each skill is self-contained but shares the same context loading, formatting, and persistence infrastructure.
