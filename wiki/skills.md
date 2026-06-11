# Spekificity Skills Index: Command Reference

## Overview

Spekificity exposes agent skills and commands for specification-driven development. All skills follow the decorator pattern — they wrap SpecKit base commands without replacing them.

**Command Notation:**
- All Spekificity workflow commands use `/spek.*` prefix (agent skill identifier)
- Context commands: `/spek.context`, `/spek.map`, `/spek.lessons`
- Analysis commands: `/lat.query`, `/lat.sync` (lat.md MCP tools)
- Compression: `/caveman` mode commands

**`/spek.lessons` is both a first-class standalone skill AND called as a sub-step by `/spek.conclude`.** Running `/spek.conclude` invokes lessons extraction automatically. You can also run `/spek.lessons` independently — for example, mid-feature to capture an insight, or to re-run lessons extraction after conclude.

**Critical distinction:** Slash-prefixed forms (`/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`) are **agent skills** that run inside the agent environment. These are NOT CLI commands. Only `spek init` is a CLI command. Attempting `spek prepare` or `spek plan` from the terminal will fail.

## Workflow Skills: `/spek.*` Namespace

### `/spek.prepare`

**Purpose:** Initialize all third-party tools and load context before feature development  
**Usage:** `/spek.prepare`

**What it does:**
1. Initialize lat.md index for **source code** (symbols, definitions, call graphs)
2. Initialize lat.md index for **documentation** (wiki, vault, markdown files) — separate index from code
3. Store both indexes in Obsidian vault (`.spek/vault/`) for persistent context
4. Load vault context (decisions, patterns, prior lessons) into agent session
5. Verify `.specify/memory/constitution.md` exists; if missing, invoke `/speckit.constitution` to create it (one-time, interactive)

**Why separate code + doc indexes:** Code symbols and documentation serve different query purposes. Code index answers "where is this function defined / what calls it." Doc index answers "what decisions or patterns are relevant to this topic."

**Output:**
- lat.md code index initialized and fresh
- lat.md doc index initialized and fresh
- Vault context loaded (decisions, patterns, lessons)
- Agent session ready for planning

---

### `/spek.plan`

**Purpose:** Orchestrate full SpecKit planning pipeline: spec → plan → tasks  
**Usage:** `/spek.plan [feature-name]`

**What it does:**

Wraps these SpecKit skills in order, performing remediations at each step before proceeding:

1. **`/speckit.specify`** — Write initial spec from feature intent
   - Surface spec + success criteria to user
   - Request confirmation or revisions
   - If remediation required: apply fixes, re-run `/speckit.specify`
   - Continue until spec is approved
   
2. **`/speckit.plan`** — Generate implementation plan from approved spec
   - Use lat.md code index to identify affected code sections
   - Surface plan to user for review + approval
   - If remediation required: apply fixes, re-run `/speckit.plan`
   - Continue until plan is approved
   
3. **`/speckit.tasks`** — Granular task breakdown from approved plan
   - Generate implementable tasks (one action per task) with dependency order
   - Surface task list to user for review
   - If remediation required: apply fixes, re-run `/speckit.tasks`
   - Continue until tasks are approved

**Remediation:** Each phase loops until approved. If a phase requires fixes that invalidate a prior phase (e.g., tasks reveal a flaw in the plan), loop back to the affected phase and reprocess forward.

**What `/spek.plan` does NOT do:** It does not call `/speckit.clarify` or `/speckit.analyze` automatically. Those are optional and can be invoked manually if needed.

**Output:**
- Approved spec (SpecKit-managed path; archived to `.spek/vault/` via Obsidian)
- Approved implementation plan (SpecKit-managed path; archived to `.spek/vault/` via Obsidian)
- Approved task list with dependency order (SpecKit-managed path; archived to `.spek/vault/` via Obsidian)

---

### `/spek.implement`

**Purpose:** Execute implementation by wrapping `/speckit.implement`  
**Usage:** `/spek.implement [--steps N]`

**What it does:**

Wraps a single SpecKit skill:

1. Load approved spec + plan + task list from SpecKit-managed paths (archived copies available in `.spek/vault/`)
2. Execute **`/speckit.implement`** — actions all tasks sequentially
   - `/speckit.implement` handles per-task execution, code generation, and step tracking
   - Jump to specific step with `--steps N` if resuming

`/spek.implement` is intentionally thin. SpecKit owns implementation execution. Spekificity's role is context loading (vault + lat.md) before invoking SpecKit, not duplicating SpecKit's task runner.

**Output:**
- Code changes from `/speckit.implement`
- Task completion status

---

### `/spek.lessons`

**Purpose:** Extract structured lessons from feature work and write to vault  
**Usage:** `/spek.lessons [feature-name]`  
**Requires:** Obsidian CLI (vault write)

**What it does:**
1. Prompt for retrospective (what worked, what was difficult, patterns discovered, recommendations)
2. Extract new patterns if workflow diverged from spec
3. Log new decisions if architecture changed
4. Write lessons document to vault via Obsidian CLI: `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`
5. Update `.spek/vault/patterns.md` with any new patterns
6. Update `.spek/vault/decisions.md` with any new decisions

**When to invoke:**
- Automatically: called as sub-step inside `/spek.conclude`
- Standalone: run independently to capture lessons mid-feature, or to re-run extraction after conclude

**Output:**
- `.spek/vault/lessons/YYYY-MM-DD-feature-name.md` (new file via Obsidian CLI)
- Updated `.spek/vault/patterns.md` (if new patterns)
- Updated `.spek/vault/decisions.md` (if new decisions)

---

### `/spek.conclude`

**Purpose:** All post-implementation functions — analysis, archive, lessons, state refresh  
**Usage:** `/spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]`  
**Requires:** Obsidian CLI (all vault operations)

**What it does:**

`/spek.conclude` owns all post-implementation work. It calls `/spek.lessons` as a sub-step (you can also invoke `/spek.lessons` independently at any point).

1. **Analysis:**
   - Execute `/speckit.analyze` — validate implementation against spec
   - Compare Success Criteria vs actual outcomes
   - Identify spec drift or deviations

2. **Lessons (sub-step: calls `/spek.lessons`):**
   - Prompt for retrospective (what worked, what was difficult, patterns, recommendations)
   - Extract new patterns if workflow diverged from spec
   - Log new decisions if architecture changed
   - Generate lessons document (`vault/lessons/YYYY-MM-DD-feature-name.md`)

3. **Vault Archive:**
   - Archive spec + plan + tasks to `.spek/vault/`
   - Update `.spek/vault/patterns.md` with new patterns
   - Update `.spek/vault/decisions.md` with new decisions

4. **State Refresh:**
   - Refresh lat.md index: `lat init` (reflects new code)
   - Sync repo memory to `.spek/memory/`
   - Obsidian vault graph updates automatically when notes are written via CLI

5. **Completion:**
   - Commit vault changes to git
   - Report analysis + lessons + synced artifacts

**Output:**
- Analysis report (spec drift, outcomes vs criteria)
- Lessons document (`.spek/vault/lessons/YYYY-MM-DD-feature-name.md`)
- Updated patterns + decisions (`.spek/vault/`)
- Repo memory synced (`.spek/memory/`)
- lat.md indexes refreshed (code + docs)
- Completion report

**Note:** `/spek.lessons` is both a first-class skill AND a sub-step of `/spek.conclude`. Conclude calls it automatically. You can also invoke it independently at any point.

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

---

## lat.md: Native CLI and MCP Tools

`lat.md` is a 3rd party tool installed by `spek init`. These are **not generated skill files** — they are native lat.md commands and MCP tools available after installation.

### CLI Commands (run in terminal or git hooks)

| Command | Purpose |
|---------|---------|
| `lat init` | Initialize or rebuild index in current project |
| `lat locate <symbol>` | Locate where a symbol is defined |
| `lat refs <symbol>` | Find all references to a symbol |
| `lat search <query>` | Search codebase by query |
| `lat mcp` | Start MCP server for agent session |

### MCP Tools (used by agent skills during workflow)

Agent skills access lat.md via its MCP server (started with `lat mcp`). Confirm exact MCP tool names against lat.md documentation — the server exposes tools for symbol lookup, reference traversal, and code search. Skills should reference these tools by their actual MCP-registered names.

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
| *Optional (also auto-called by conclude)* | `/spek.lessons` | Capture lessons, patterns, decisions to vault |

**Design:** All commands keep `spek.` prefix for namespace consistency. Single-word command portions for ergonomics. Required commands form minimal viable path; optional commands enhance without blocking workflow.

---

### SpecKit Underlying Commands (`speckit.*` namespace)

**Pattern:** `/speckit.oneword` — wrapped by Spekificity enrichment layer

| Command | Purpose | Invoked By |
|---------|---------|-----------|
| `/speckit.constitution` | Define project principles | Manual or on first `/spek.prepare` if missing |
| `/speckit.specify` | Create feature spec | `/spek.plan` (step 1) |
| `/speckit.clarify` | Resolve spec ambiguities | Manual (optional) |
| `/speckit.plan` | Create implementation plan | `/spek.plan` (step 2) |
| `/speckit.tasks` | Generate task list | `/spek.plan` (step 3) |
| `/speckit.analyze` | Cross-artifact consistency check | `/spek.conclude` (step 1), or manual |
| `/speckit.implement` | Execute all tasks | `/spek.implement` |

**Design:** Vanilla SpecKit commands use `speckit.*` namespace. Spekificity wraps these (decorator pattern) to inject enrichment layers (vault decisions, lat.md context, pattern references) without modifying SpecKit internals.

---

