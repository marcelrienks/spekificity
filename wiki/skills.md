# Spekificity Skills Index: Command Reference

## Overview

Spekificity exposes agent skills and commands for specification-driven development. All skills follow the decorator pattern — they wrap SpecKit base commands without replacing them.

**Command Notation:**
- All Spekificity workflow commands use `/spek.*` prefix (agent skill identifier)
- Context commands: `/spek.context`, `/spek.map`, `/spek.lessons`
- Analysis commands: `/lat.query`, `/lat.sync` (lat.md MCP tools)
- Compression: `/caveman` mode commands

**Note:** Slash-prefixed forms (`/spek.prepare`, `/spek.plan`, etc.) are the canonical notation used in all documentation and agent prompts. When running commands via CLI directly, use the same form: `spek prepare`, `spek plan`, etc. (without slash).

---

## Workflow Skills: `/spek.*` Namespace

### `/spek.prepare`

**Purpose:** Prepare for new feature development  
**Usage:** `/spek.prepare [feature-name]`

**What it does:**
1. Ensure project constitution exists; create if missing via `/speckit.constitution`
2. Load vault context (3-layer memory model)
3. Index code state via lat.md
4. List available specs for feature selection
5. Load prior decisions + patterns relevant to feature
6. Present onboarding summary (short read)

**Output:**
- Feature context + related specs
- Dependency map (blockers)
- Related patterns (quick-ref links)
- Previous lessons learned (if feature attempted before)

**Reference:** [decision.md](../decision.md) (preparation phase)

---

### `/spek.plan`

**Purpose:** Convert specification into implementation plan  
**Usage:** `/spek.plan [spec-file]`

**What it does:**

Executes SpecKit specification → clarification → planning → task breakdown sequence in order:

1. **`/speckit.specify`** — Write initial spec from feature intent
   - Surface spec + success criteria + enrichment layers to user
   - Request confirmation or revisions
   
2. **`/speckit.clarify`** — Identify gaps in specification
   - Surface clarification questions to user
   - Collect answers + integrate into spec
   - Loop until spec is unambiguous (no remediations needed)
   
3. **`/speckit.plan`** — Generate implementation plan from spec
   - Identify code sections to modify (lat.md impact analysis)
   - Estimate token budget per phase
   - Surface plan to user for review + approval
   - If remediation required, flag issues to user + loop back to `/speckit.specify` if needed
   
4. **`/speckit.tasks`** — Granular task breakdown from plan
   - Generate implementable tasks (one action per task)
   - Suggest related patterns + decision references
   - Surface task list to user for review
   - If remediation required, re-process tasks after user input

**Remediation Loop:**
- After each phase, surface output to user for review
- Collect user input/approval/corrections
- If remediation needed: apply fixes + reprocess from failure point
- Continue until all phases complete with no further remediation required

**Output:**
- Approved spec + success criteria + enrichment layers
- Clarified specification (no ambiguities)
- Step-by-step implementation plan
- Code sections affected (with line ranges)
- Suggested patterns to use
- Granular, approved task list
- Token allocation per task
- Decision tree path (if decisions needed)

**Reference:** [workflow.md](../workflow.md) (plan phase)

---


---

### `/spek.implement`

**Purpose:** Execute implementation against spec + plan  
**Usage:** `/spek.implement [feature-name|spec-file] --steps N`

**What it does:**

1. Load spec + plan + task list
2. Execute `/speckit.implement` — action all tasks sequentially (or jump to step N)
   - After each step: log to vault, query lat.md for context
   - Track token usage against budget
   - Capture new decisions + lessons as they emerge
   - Mark steps complete
3. Commit code changes with spec + plan linkage

**Interactive:**
- Ask for confirmation before major code changes
- Suggest alternative approaches if token budget exceeded
- Offer pattern suggestions based on code context
- Record any deviations from spec for post-mortem

**Output:**
- Implementation progress (step status)
- Code changes committed (with spec + plan linkage)
- Decisions logged (new or referenced)
- Token usage to date
- Completion status summary

**Reference:** [workflow.md](../workflow.md)

---

### `/spek.lessons`

**Purpose:** Archive lessons learned + extract patterns + update vault  
**Usage:** `/spek.lessons [feature-name|feature-complete]`  
**Requires:** Obsidian CLI (for vault exports and graph generation)

**What it does:**
1. Prompt for retrospective (What went well? What to improve?)
2. Extract new patterns if workflow diverged from spec
3. Log new decisions if architecture changed
4. Update Success Criteria if spec changed
5. Generate post-mortem summary
6. Archive to `vault/lessons/<feature>.md`

**Output:**
- Post-mortem document (vault/lessons/)
- New patterns proposed (for review + wiki/patterns.md)
- New decisions logged (for wiki/decision.md)
- Spec version incremented (if changes made)

**Reference:** [decision.md](../decision.md)

---

### `/spek.conclude`

**Purpose:** Analyze implementation, extract lessons, update vault + refresh all project state  
**Usage:** `/spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]`  
**Requires:** Obsidian CLI (for vault exports and graph generation)

**What it does:**

1. **Analysis Phase:**
   - Execute `/speckit.analyze` — validate implementation against spec
   - Compare Success Criteria vs actual outcomes
   - Identify any spec drift or deviations
   - Flag contradictions or risks

2. **Lessons Extraction:**
   - Prompt for retrospective (What went well? What to improve?)
   - Extract new patterns if workflow diverged from spec
   - Log new decisions if architecture changed
   - Update Success Criteria if spec changed

3. **Vault Updates:**
   - Archive spec + plan + tasks + execution trace to vault
   - Generate lessons document (`vault/lessons/YYYY-MM-DD-feature-name.md`)
   - Update `vault/patterns.md` with new patterns
   - Update `vault/decisions.md` with new decisions

4. **Repository State Sync:**
   - Sync repo memory (architectural decisions, pattern index) to `.spek/memory/`
   - Refresh lat.md code graph index via `/lat.sync` (incremental)
   - Update graph exports + metadata
   - Refresh Obsidian vault graph via CLI

5. **Completion:**
   - Archive current feature session state
   - Report analysis + lessons + synced artifacts

**Output:**
- Analysis report (spec drift, outcomes vs criteria)
- Lessons document (`vault/lessons/YYYY-MM-DD-feature-name.md`)
- Updated patterns + decisions (vault + wiki)
- Repo memory synced (`.spek/memory/`)
- lat.md code graph refreshed
- Obsidian vault graph updated
- Completion report

**Reference:** [workflow.md](../workflow.md#conclude-feature-conclusion)

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
3. Index into lat.md for quick querying
4. Make context available to all downstream commands

**Output:**
- Context loaded summary (decisions, lessons, patterns available)
- Context refresh timestamp

**Reference:** [architecture.md](../architecture.md)

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
1. Query lat.md for code references to spec topic
2. Query wiki/decision.md for related decisions
3. Query wiki/specs/ for dependent + related specs
4. Generate visual dependency graph (text or Mermaid)
5. Highlight blockers + critical paths

**Output:**
- Dependency diagram (text or Mermaid format)
- Blocked features (if dependencies unmet)
- Critical path (longest sequence of dependencies)

**Reference:** [architecture.md](../architecture.md)

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
**Reference:** [architecture.md](../architecture.md)

---

## lat.md Skills: `/lat.*` Namespace

### `/lat.query`

**Purpose:** Query code graph for code intelligence  
**Usage:** `/lat.query [pattern|symbol|impact] [target]`

**Subcommands:**

#### `/lat.query pattern [pattern-name]`
- Find all uses of design pattern in codebase
- Return file + line ranges
- Suggest refactoring if pattern misapplied

#### `/lat.query symbol [symbol-name]`
- Find all references to function/class/module
- Return call graph (who calls this symbol?)
- Identify unused symbols

#### `/lat.query impact [file|symbol]`
- What specs + features depend on this code?
- What happens if we change this file/symbol?
- Identify breaking change risk

**Output:**
- Matching code references (file + line)
- Call/dependency graph
- Risk assessment (if impact query)

**Reference:** [setup.md](../setup.md)

---

### `/lat.sync`

**Purpose:** Synchronize code graph with current repository state  
**Usage:** `/lat.sync [--force]`

**What it does:**
1. Detect file changes since last sync
2. Update graph incrementally (not full rebuild)
3. Validate graph integrity (check for stale references)
4. Report index coverage (qualitative completeness)
5. Warn if manual rebuild recommended

**Output:**
- Sync complete (files added/modified/removed)
- Graph size (nodes + edges)
- Coverage of codebase
- Timestamp of last sync

**Reference:** [setup.md](../setup.md)

---

## Compression Skills: `/caveman.*` Namespace

### `/caveman`

**Purpose:** Activate Caveman compression mode (terse, compressed output). Caveman is an internal skill/mode (no external install).
**Usage:** `/caveman [--intensity lite|full|ultra]`

**Modes:**
- `lite`: modest token reduction (remove explanations)
- `full`: significant token reduction (terse format, abbreviations) — DEFAULT
- `ultra`: maximal token reduction (minimal prose, lossy)

**What it does:**
1. Enable terse output mode for current session
2. Compress responses at each workflow stage where configured
3. Preserve technical accuracy and searchable keywords
4. Switch back to normal mode with `/caveman off`

**Output:** All subsequent commands respond in compressed format  
**Reference:** [decision.md](../decision.md#decision-3)

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

**Reference:** [decision.md](../decision.md#decision-3)

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
- `lat.sync-interval`: Auto-sync interval (minutes)
- `token.budget`: Max tokens per feature (advisory)

---

*For workflow diagrams and execution patterns, see [workflow.md](workflow.md).*

---

## Command Naming & Invocation

### Spekificity User-Facing Skills (`spek.*` prefix)

**Pattern:** `/spek.oneword` — action-oriented, imperative verbs

| Tier | Command | Purpose |
|------|---------|----------|
| **REQUIRED** | `/spek.prepare` | Initialize workspace, git state, lat.md index |
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

**Design:** Vanilla SpecKit commands use `speckit.*` namespace. Spekificity wraps these (decorator pattern) to inject enrichment layers (vault decisions, lat.md context, pattern references) without modifying SpecKit internals.

---

### Support Command Namespaces

**Context Commands:** `/context.*`  
- `/context.load` — Load memory scope (user|session|repo)
- `/context.inject` — Inject context at workflow stages

**lat.md Queries:** `/lat.*`  
- `/lat.query` — Query code/document index
- `/lat.sync` — Refresh lat.md index

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
/lat.query            # Code intelligence
/lat.sync             # Refresh graph
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

**Clarity:** Command name describes action (verb-oriented). Prefixes group related tools (`spek.*` = Spekificity, `speckit.*` = SpecKit, `context.*` = memory, `lat.*` = code analysis).

**Modularity:** Each command follows same patterns:
- Input: Feature name, spec file, or target item
- Output: Artifacts (specs, plans, tasks, lessons)
- Flags: `--verbose`, `--format`, `--dry-run`, `--quiet`
- Logging: All changes to vault; never silent failures

---

## Skill Status

- **Required Core:** `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`
- **Optional Enhancements:** `/spek.context`, `/spek.map`, `/spek.lessons`, `/context.inject`
- **Status:** All documented skills are available and functional.

---

## Resources

- **Full Skill Specifications:** [wiki/specs/](../specs/)
- **Workflow Guide:** [wiki/workflow.md](../workflow.md)
- **Quick Start:** [wiki/quickstart.md](../quickstart.md)

---

## Implementation Note

Spekificity implementation follows all skills and specifications in `/wiki/specs/`. The tool is defined entirely by the wiki documentation. Implementation status aligns with spec completion.
