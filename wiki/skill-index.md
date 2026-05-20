# Spekificity Skills Index: Command Reference

**Last Updated:** 2026-05-20  
**Version:** 1.0.0-alpha.1  
**Status:** ATOMIC SPECIFICATION

---

## Overview

Spekificity exposes a set of CLI skills and AI agent commands for specification-driven development. All skills follow the decorator pattern — they wrap SpecKit base commands without replacing them.

**Quick Reference:**
- Workflow commands: `/spek.*` namespace
- Context commands: `/context.*` namespace
- Analysis commands: `/cg.*` (CodeGraph) namespace
- Compression: `/caveman` mode commands

---

## Workflow Skills: `/spek.*` Namespace

### `/spek.prepare`

**Purpose:** Prepare for new feature development  
**Usage:** `/spek.prepare [feature-name]`

**What it does:**
1. Load vault context (3-layer memory model)
2. Index code state via CodeGraph
3. List available specs for feature selection
4. Load prior decisions + patterns relevant to feature
5. Present onboarding summary (5 min read)

**Output:**
- Feature context + related specs
- Dependency map (blockers)
- Related patterns (quick-ref links)
- Previous lessons learned (if feature attempted before)

**Spec Reference:** [spek-lessons-command.md](../specs/spek-lessons-command.md) (preparation phase)

---

### `/spek.plan`

**Purpose:** Convert specification into implementation plan  
**Usage:** `/spek.plan [spec-file]`

**What it does:**
1. Parse spec Success Criteria
2. Generate task list (granular, implementable)
3. Identify code sections to modify (CodeGraph impact analysis)
4. Estimate token budget per task
5. Suggest related patterns + decision references

**Output:**
- Step-by-step implementation plan
- Code sections affected (with line ranges)
- Suggested patterns to use
- Decision tree path (if decisions needed)
- Token allocation per phase

**Spec Reference:** [spek-automate-workflow.md](../specs/spek-automate-workflow.md) (plan phase)

---

### `/spek.automate`

**Purpose:** Automated spec generation, planning, and validation  
**Usage:** `/spek.automate --mode [specify|plan|validate]`

**Modes:**

#### Mode 1: `specify` (Generate Specs from Feature Proposal)
- Parse feature description
- Generate candidate specs following existing format
- Validate against existing specs (no duplication)
- Generate Success Criteria from requirements
- Suggest dependencies + related specs

#### Mode 2: `plan` (Auto-generate Implementation Plan)
- Parse existing spec
- Break Success Criteria into tasks
- Map tasks to code sections (CodeGraph)
- Estimate effort + token cost per task
- Order tasks by dependency

#### Mode 3: `validate` (Verify Spec Completeness)
- Check for required metadata (Status, Version, Success Criteria)
- Validate all "Depends On" references exist
- Check for circular dependencies
- Verify link validity (cross-references)
- Test Success Criteria completeness

**Output:** Varies by mode (candidate specs, plan, or validation report)  
**Spec Reference:** [spek-automate-workflow.md](../specs/spek-automate-workflow.md)

---

### `/spek.implement`

**Purpose:** Execute implementation against spec + plan  
**Usage:** `/spek.implement [feature-name|spec-file] --steps N`

**What it does:**
1. Load spec + plan
2. Execute tasks sequentially (or jump to step N)
3. After each step: log to vault, query CodeGraph for context
4. Track token usage against budget
5. Capture new decisions + lessons as they emerge
6. Mark steps complete

**Interactive:**
- Ask for confirmation before major code changes
- Suggest alternative approaches if token budget exceeded
- Offer pattern suggestions based on code context
- Record any deviations from spec for post-mortem

**Output:**
- Implementation progress (step N/M complete)
- Code changes committed (with spec + plan linkage)
- Decisions logged (new or referenced)
- Token usage to date
- Estimated completion

**Spec Reference:** [spek-implement-workflow.md](../specs/spek-implement-workflow.md)

---

### `/spek.lessons`

**Purpose:** Archive lessons learned + extract patterns + update vault  
**Usage:** `/spek.lessons [feature-name|feature-complete]`

**What it does:**
1. Prompt for retrospective (What went well? What to improve?)
2. Extract new patterns if workflow diverged from spec
3. Log new decisions if architecture changed
4. Update Success Criteria if spec changed
5. Generate post-mortem summary
6. Archive to vault/lessons/YYYY-MM-DD-feature-name.md

**Output:**
- Post-mortem document (vault/lessons/)
- New patterns proposed (for review + wiki/patterns.md)
- New decisions logged (for wiki/decision.md)
- Spec version incremented (if changes made)

**Spec Reference:** [spek-lessons-command.md](../specs/spek-lessons-command.md)

---

### `/spek.map`

**Purpose:** Generate impact analysis + dependency map  
**Usage:** `/spek.map [spec-file] [--show-impact|--show-deps|--show-all]`

**Flags:**
- `--show-impact`: What code + specs are affected by changes to this spec?
- `--show-deps`: What specs does this depend on?
- `--show-all`: Full dependency graph (specs + code)

**What it does:**
1. Query CodeGraph for code references to spec topic
2. Query wiki/decision.md for related decisions
3. Query wiki/specs/ for dependent + related specs
4. Generate visual dependency graph (text or Mermaid)
5. Highlight blockers + critical paths

**Output:**
- Dependency diagram (text or Mermaid format)
- Blocked features (if dependencies unmet)
- Critical path (longest sequence of dependencies)

**Spec Reference:** [spek-map-command.md](../specs/spek-map-command.md)

---

## Context Skills: `/context.*` Namespace

### `/context.load`

**Purpose:** Load vault context for current session  
**Usage:** `/context.load [--scope user|session|repo]`

**Scopes:**
- `user`: Personal preferences + patterns (persistent across projects)
- `session`: Task-specific context (cleared at session end)
- `repo`: Project-specific vault (decisions + lessons from this project)

**What it does:**
1. Read memory files from specified scope
2. Parse YAML frontmatter (if present)
3. Index into CodeGraph for quick querying
4. Make context available to all downstream commands
5. Track token usage (context loading cost amortized over session)

**Output:**
- Context loaded summary (# decisions, # lessons, # patterns available)
- Token cost (one-time per session)
- Context refresh timestamp

**Spec Reference:** [context-layer.md](../specs/context-layer.md)

---

### `/context.inject`

**Purpose:** Inject context at specific points in workflow  
**Usage:** `/context.inject --at [stage] --focus [topic]`

**Stages:**
- `prepare`: Pre-feature context
- `plan`: Implementation plan stage
- `implement`: During coding
- `validate`: Validation stage
- `lessons`: Post-mortem stage

**Topics:** Feature name, code module, architectural layer, decision tree path

**What it does:**
1. Load core context (from `/context.load`)
2. Filter context by topic + stage relevance
3. Compress output (caveman style if requested)
4. Provide minimal-token-cost context injection

**Output:** Filtered context (decisions, patterns, lessons relevant to stage + topic)  
**Spec Reference:** [enrichment-layer.md](../specs/enrichment-layer.md)

---

## CodeGraph Skills: `/cg.*` Namespace

### `/cg.query`

**Purpose:** Query code graph for code intelligence  
**Usage:** `/cg.query [pattern|symbol|impact] [target]`

**Subcommands:**

#### `/cg.query pattern [pattern-name]`
- Find all uses of design pattern in codebase
- Return file + line ranges
- Suggest refactoring if pattern misapplied

#### `/cg.query symbol [symbol-name]`
- Find all references to function/class/module
- Return call graph (who calls this symbol?)
- Identify unused symbols

#### `/cg.query impact [file|symbol]`
- What specs + features depend on this code?
- What happens if we change this file/symbol?
- Identify breaking change risk

**Output:**
- Matching code references (file + line)
- Call/dependency graph
- Risk assessment (if impact query)

**Spec Reference:** [codegraph-setup-complete.md](../specs/codegraph-setup-complete.md)

---

### `/cg.sync`

**Purpose:** Synchronize code graph with current repository state  
**Usage:** `/cg.sync [--force]`

**What it does:**
1. Detect file changes since last sync
2. Update graph incrementally (not full rebuild)
3. Validate graph integrity (check for stale references)
4. Report coverage % (what % of codebase indexed)
5. Warn if manual rebuild recommended

**Output:**
- Sync complete (files added/modified/removed)
- Graph size (node + edge count)
- Coverage % of codebase
- Timestamp of last sync

**Spec Reference:** [codegraph-setup-complete.md](../specs/codegraph-setup-complete.md)

---

## Compression Skills: `/caveman.*` Namespace

### `/caveman`

**Purpose:** Activate caveman mode (terse, compressed output)  
**Usage:** `/caveman [--intensity lite|full|ultra]`

**Modes:**
- `lite`: 20% token reduction (remove explanations)
- `full`: 50% token reduction (terse format, abbreviations)
- `ultra`: 75% token reduction (caveman-speak, minimal prose)

**What it does:**
1. Enable terse output mode for current session
2. Compress responses at each workflow stage
3. Maintain technical accuracy (compress language, not substance)
4. Switch back to normal mode with `/caveman off`

**Output:** All subsequent commands respond in compressed format  
**Spec Reference:** [caveman-integration.md](../specs/caveman-integration.md)

---

### `/caveman.review`

**Purpose:** Compressed code review of PR/diff  
**Usage:** `/caveman.review [--pr number|--file path]`

**What it does:**
1. Parse PR or file diff
2. Generate ultra-compressed review comments
3. One line per issue: location, problem, fix
4. Skip obvious/minor issues (focus on impact)
5. Output ready for copy-paste into GitHub

**Output:**
- Compressed review comments (1-2 lines each)
- Summary line (overall quality assessment)
- Severity classification (critical/high/medium/low)

**Spec Reference:** [caveman-integration.md](../specs/caveman-integration.md)

---

## Helper Skills: Utilities

### `/help`

**Purpose:** Get help on any skill or command  
**Usage:** `/help [command-name]`

**Output:**
- Command signature + short description
- Usage examples
- Link to full spec documentation
- Related commands

---

### `/config`

**Purpose:** View or modify project configuration  
**Usage:** `/config [--show|--set key=value]`

**Keys:**
- `vault.scope`: Default memory scope (user|session|repo)
- `context.compression`: Default compression mode (caveman intensity)
- `cg.sync-interval`: Auto-sync interval (minutes)
- `token.budget`: Max tokens per feature (advisory)

---

## Command Chains: Typical Workflows

### Workflow 1: Start New Feature (15 min)

```
/spek.prepare [feature-name]
  → CodeGraph loads code state
  → Vault context injected
  ↓
/spek.plan [spec-file]
  → Plan generated from spec
  ↓
/spek.implement [feature-name]
  → Start implementation (step-by-step)
```

### Workflow 2: Verify Spec Completeness (5 min)

```
/spek.automate --mode validate [spec-file]
  → Checks format + cross-references
  ↓
/context.load --scope repo
  → Load project decisions + lessons
  ↓
/cg.query impact [affected-code]
  → What else does this spec touch?
```

### Workflow 3: End of Feature (20 min)

```
/spek.implement --status check
  → Verify all steps complete
  ↓
/cg.sync
  → Update code graph
  ↓
/spek.lessons [feature-complete]
  → Archive lessons + new patterns
  ↓
/context.inject --at lessons --focus [feature-name]
  → Load context for post-mortem notes
```

---

## Skill Conventions

### Naming Rules

- Workflow commands: `/spek.*` (feature lifecycle)
- Context commands: `/context.*` (memory + injection)
- Analysis commands: `/cg.*` (CodeGraph queries)
- Compression: `/caveman.*` (token reduction)
- Utilities: `/help`, `/config`

### Common Patterns

All skills accept:
- `--verbose`: Expand output (full explanations)
- `--format [text|json|mermaid]`: Output format
- `--dry-run`: Show what would happen (no changes)
- `--quiet`: Suppress non-essential output

### Error Handling

All skills follow:
1. Validate input (early exit if invalid)
2. Log all decisions + changes to vault
3. Provide recovery options on failure
4. Never delete files (archive instead)

---

## Skill Availability

- **Installed:** All skills above (alpha.1 baseline)
- **In Development (Phase 3):** Extended CLI integration
- **Future (Phase 4):** Custom skill registration
- **Future (Phase 5):** Automated skill discovery from codebase

---

## Resources

- **Full Skill Specifications:** [wiki/specs/](../specs/)
- **Workflow Guide:** [wiki/workflow.md](../workflow.md)
- **Quick Start:** [wiki/quickstart.md](../quickstart.md)
- **Pattern Library:** [wiki/patterns.md](../patterns.md)
- **Decision Tree:** [wiki/decision.md](../decision.md)

---

**Status:** ATOMIC SPECIFICATION | **Version:** 1.0.0-alpha.1 (2026-05-20)
