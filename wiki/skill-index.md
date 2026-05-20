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

**Spec Reference:** [spek-plan-workflow.md](../specs/spek-plan-workflow.md) (plan phase)

---

### `/spek.plan`

**Purpose:** Automated spec generation, planning, and validation  
**Usage:** `/spek.plan --mode [specify|plan|validate]`

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
**Spec Reference:** [spek-plan-workflow.md](../specs/spek-plan-workflow.md)

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

### `/spek.conclude`

**Purpose:** Archive feature outcomes, extract lessons, update vault + refresh CodeGraph  
**Usage:** `/spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]`

**What it does:**
1. Collect implementation artifacts (spec, plan, tasks, execution trace, code changes)
2. Generate lessons document from artifacts
3. Document architectural decisions and rationale
4. Update vault/patterns.md with new patterns
5. Sync repo memory (architectural decisions, pattern index)
6. Refresh CodeGraph via /spek.map (incremental)
7. Archive current feature session state
8. Report completion

**Output:**
- Lessons document (vault/lessons/YYYY-MM-DD-feature-name.md)
- Decisions and patterns documented
- Synced repo memory + graph refreshed
- Completion report

**Spec Reference:** [conclude-command.md](../specs/102-conclude-command.md)

---

## Optional Enhancements: Context & Analysis

The following commands are **first-class and fully documented**, but **not required** for basic feature development. Use them to enhance context loading, verify dependencies, or analyze impact.

### `/spek.context` — Load Project Context

**Purpose:** Load vault context (decisions, patterns, lessons) into current session  
**Usage:** `/spek.context [--scope user|session|repo]`

**When to use:**
- Before starting implementation to review past decisions
- During planning to find related patterns
- At any point to inject project knowledge

**What it does:**
1. Read memory files from specified scope
2. Parse YAML frontmatter (if present)
3. Index into CodeGraph for quick querying
4. Make context available to all downstream commands

**Output:**
- Context loaded summary (# decisions, # lessons, # patterns available)
- Context refresh timestamp

**Spec Reference:** [context-layer.md](../specs/context-layer.md)

---

### `/spek.map` — Analyze Dependencies & Impact

**Purpose:** Generate impact analysis + dependency map  
**Usage:** `/spek.map [spec-file] [--show-impact|--show-deps|--show-all]`

**When to use:**
- To verify what code/specs are affected by a change
- To identify blockers or dependencies before starting
- To understand critical paths in feature dependencies

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

## Context Injection: `/context.*` Namespace

For fine-grained context control at specific workflow points:

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

## Core Workflow: Minimal Path

**Essential only.** These commands form the required backbone:

```
/spek.prepare [feature-name]
  → Workspace ready, git clean, CodeGraph fresh
  ↓
/spek.plan --phase=specify
  → Feature specification generated
  ↓
/spek.plan --phase=plan
  → Implementation plan + task breakdown
  ↓
/spek.implement [feature-name]
  → Execute tasks
  ↓
/spek.conclude
  → Archive outcomes, refresh vault, sync graph
```

## Enhanced Workflows: Optional Additions

### Workflow A: Decision-Aware Implementation

```
/spek.context --scope repo
  → Load project decisions + patterns (OPTIONAL)
  ↓
[run core workflow above]
  ↓
/spek.lessons [feature-complete]
  → Explicit lesson extraction + vault update (OPTIONAL)
```

### Workflow B: Dependency Verification

```
/spek.map [spec-file] --show-all
  → Identify blockers + dependencies (OPTIONAL)
  ↓
[run core workflow above]
```

### Workflow C: Impact Analysis During Planning

```
/spek.plan --phase=plan
  → Generate implementation plan (REQUIRED)
  ↓
/cg.query impact [affected-code]
  → Verify impact on other systems (OPTIONAL)
  ↓
/spek.implement [feature-name]
  → Execute with full awareness
```

---

## Command Naming & Invocation

### Spekificity User-Facing Skills (`spek.*` prefix)

**Pattern:** `/spek.oneword` — action-oriented, imperative verbs

| Tier | Command | Purpose |
|------|---------|----------|
| **REQUIRED** | `/spek.prepare` | Initialize workspace, git state, CodeGraph |
| **REQUIRED** | `/spek.plan` | Generate specs, plans, task breakdown |
| **REQUIRED** | `/spek.implement` | Execute tasks with context |
| **REQUIRED** | `/spek.conclude` | Archive outcomes, update vault, sync graph |
| *Optional* | `/spek.context` | Load vault decisions, patterns, lessons |
| *Optional* | `/spek.map` | Analyze dependencies + impact |
| *Optional* | `/spek.lessons` | Explicit retrospective + pattern extraction |

**Design:** All commands keep `spek.` prefix for namespace consistency. Single-word command portions for ergonomics. Required commands form minimal viable path; optional commands enhance without blocking workflow.

---

### SpecKit Underlying Commands (`speckit.*` namespace)

**Pattern:** `/speckit.oneword` — wrapped by Spekificity enrichment layer

| Command | Purpose | Invoked By |
|---------|---------|-----------|
| `/speckit.constitution` | Define project principles | Manual or `/spek.plan` |
| `/speckit.specify` | Create feature spec | `/spek.plan --phase=specify` |
| `/speckit.clarify` | Resolve spec ambiguities | `/spek.plan --phase=clarify` (optional) |
| `/speckit.plan` | Create implementation plan | `/spek.plan --phase=plan` |
| `/speckit.tasks` | Generate task list | `/spek.plan --phase=plan` |
| `/speckit.analyze` | Cross-artifact consistency check | `/spek.plan --phase=analyze` (optional) |

**Design:** Vanilla SpecKit commands use `speckit.*` namespace. Spekificity wraps these (decorator pattern) to inject enrichment layers (vault decisions, CodeGraph context, pattern references) without modifying SpecKit internals.

---

### Support Command Namespaces

**Context Commands:** `/context.*`  
- `/context.load` — Load memory scope (user|session|repo)
- `/context.inject` — Inject context at workflow stages

**CodeGraph Queries:** `/cg.*`  
- `/cg.query` — Query code intelligence
- `/cg.sync` — Refresh code graph

**Compression:** `/caveman.*`  
- `/caveman` — Activate compression mode  
- `/caveman.review` — Compressed code review

**Utilities:** No prefix  
- `/help` — Get help on any command
- `/config` — View/modify configuration

---

### Invocation Quick Reference

**Core Workflow (Required):**
```
/spek.prepare         # Workspace ready
/spek.plan        # Spec → plan → tasks
/spek.implement       # Execute tasks
/spek.conclude            # Archive + sync
```

**Enhancements (Optional):**
```
/spek.context         # Load project knowledge
/spek.map             # Analyze dependencies
/spek.lessons         # Extract retrospective
/context.inject       # Stage-specific context
```

**Underlying SpecKit (via /spek.plan):**
```
/speckit.specify
/speckit.clarify      # Optional
/speckit.plan
/speckit.analyze      # Optional  
/speckit.tasks
```

**Context & Analysis:**
```
/context.load         # Load memory
/context.inject       # Stage-specific context
/cg.query            # Code intelligence
/cg.sync             # Refresh graph
```

**Compression & Utilities:**
```
/caveman             # Compression toggle
/caveman.review      # Compressed PR review
/help                # Command help
/config              # Configuration
```

---

### Naming Conventions: Design Principles

**Consistency:** All workflow commands use `spek.*` prefix. Namespace distinction is intentional and visible in command name (no aliasing needed).

**Simplicity:** Command portions are single words where possible (`prepare`, not `prep`; `context`, not `ctx`). Hyphenation avoided for ergonomics.

**Clarity:** Command name describes action (verb-oriented). Prefixes group related tools (`spek.*` = Spekificity, `speckit.*` = SpecKit, `context.*` = memory, `cg.*` = code analysis).

**Modularity:** Each command follows same patterns:
- Input: Feature name, spec file, or target item
- Output: Artifacts (specs, plans, tasks, lessons)
- Flags: `--verbose`, `--format`, `--dry-run`, `--quiet`
- Logging: All changes to vault; never silent failures

---

## Skill Status

- **Required Core (alpha.1):** `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`
- **Optional Enhancements (alpha.1):** `/spek.context`, `/spek.map`, `/spek.lessons`, `/context.inject`
- **Status:** All documented skills are available. Implementation proceeds per wiki/specs documentation.

---

## Resources

- **Full Skill Specifications:** [wiki/specs/](../specs/)
- **Workflow Guide:** [wiki/workflow.md](../workflow.md)
- **Quick Start:** [wiki/quickstart.md](../quickstart.md)

---

## Completeness Note

Spekificity is complete when all skills and specifications in `/wiki/specs/` are fully implemented. There is no MVP or partial delivery—the tool is dictated entirely by the wiki documentation. Development is driven by spec completion.
