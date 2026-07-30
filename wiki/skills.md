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

## Skill File Format

Skill files are plain markdown. No frontmatter, no agent-specific syntax. Any agent (Claude Code, Copilot, Gemini, Cursor, etc.) reads them as instruction sets.

### Template

```markdown
# /spek.COMMAND

One-line description of what this skill does.

## Prerequisites
- [condition that must be true before running]
- [tool or state that must exist]

## Steps

1. **[Action] [Object]**
   [Specific instruction. What to do, what to check, what to call.]
   Command: `example-command --flag`

2. **[Action] [Object]**
   [Instruction.]

3. **[Action] [Object]**
   [Instruction. If step depends on prior step output, say so explicitly.]

## Output
- [artifact or state created by this skill]
- [file path if applicable]

## Exit Criteria
- [ ] [verifiable condition — something checkable, not vague]
- [ ] [verifiable condition]
```

### Rules

- **Imperative mood** — "Read the vault", not "You should read the vault"
- **No agent syntax** — no `@workspace`, `#file:`, `[[wikilink]]`, or tool-use markup in instructions
- **Commands literal** — wrap shell/CLI calls in backticks; agent runs them verbatim
- **One action per step** — compound steps split into separate numbered items
- **Exit criteria checkable** — each criterion must be verifiable (file exists, command exits 0, output matches pattern)
- **No prose padding** — skip motivation/rationale; keep only what the agent must do

### Example

```markdown
# /spek.prepare

Initialize workspace tools and load context before feature development.

## Prerequisites
- `.spek/config.yaml` exists (run `spek init` if missing)
- Obsidian desktop is running
- `lat` and `obsidian` are in PATH

## Steps

1. **Refresh lat.md code index**
   Run: `lat init`
   Verify exit code 0 before continuing.

2. **Refresh lat.md doc index**
   Run: `lat init --docs`

3. **Load vault context**
   Run: `obsidian read file=decisions vault=vault`
   Run: `obsidian read file=patterns vault=vault`
   Hold content in session — downstream skills depend on it.

4. **Verify constitution**
   Check `.specify/memory/constitution.md` exists.
   If missing: invoke `/speckit.constitution` now (interactive, one-time).

## Output
- lat.md code index refreshed (`.spek/lat.md/`)
- lat.md doc index refreshed (`.spek/lat.md/`)
- Vault decisions and patterns loaded into session
- Constitution present

## Exit Criteria
- [ ] `lat init` exited 0
- [ ] Vault decisions loaded (non-empty content returned)
- [ ] `.specify/memory/constitution.md` exists
```

---

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
- Approved spec (stored in `.spek/vault/` with approval frontmatter)
- Approved implementation plan (stored in `.spek/vault/` with approval frontmatter)
- Approved task list with dependency order (stored in `.spek/vault/` with approval frontmatter)

---

### `/spek.implement`

**Purpose:** Execute implementation by wrapping `/speckit.implement`  
**Usage:** `/spek.implement [--steps N]`

**What it does:**

Wraps a single SpecKit skill:

1. Load approved spec + plan + task list from `.spek/vault/` (vault is the single source of truth for approved artifacts)
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

**Purpose:** All post-implementation functions — analysis, vault persistence (git commit), lessons, state refresh  
**Usage:** `/spek.conclude`  
**Requires:** Obsidian CLI (all vault operations)

**What it does:**

`/spek.conclude` owns all post-implementation work. It calls `/spek.lessons` as a sub-step (you can also invoke `/spek.lessons` independently at any point).

1. **Analysis:**
   - Execute `/speckit.analyze` — validate implementation against spec
   - Compare Success Criteria vs actual outcomes
   - Flag spec drift or deviations

2. **Lessons (sub-step: calls `/spek.lessons`):**
   - Prompt for retrospective (what worked, what was difficult, patterns, recommendations)
   - Extract new patterns if workflow diverged from spec
   - Log new decisions if architecture changed
   - Generate lessons document (`.spek/vault/lessons/YYYY-MM-DD-feature-name.md`)
   - Autolink enrichment runs inside `/spek.lessons` — wikilinks and tags added to lesson file

3. **Backprop Reflex:**
   - Parse test failure output from last test run
   - Append `> ⚠ Backprop warning` blockquotes to `.spek/vault/patterns.md` for each new failure pattern
   - Skip if no test failures in output (idempotent — second call with same output adds 0 new warnings)

4. **Vault Persistence:**
   - Archive spec + plan + tasks to `.spek/vault/`
   - Update `.spek/vault/patterns.md` with newly discovered patterns
   - Update `.spek/vault/decisions.md` with new architectural decisions

5. **Token Budget Summary:**
   - Summarize total token usage for feature
   - Compare against `token_budget.per_feature` from `.spek/config.yaml`
   - Print `[WARN] token budget: feature exceeded budget` if over; skip if `per_feature: null`

6. **State Refresh:**
   - Refresh lat.md index: `lat init` (reflects committed code)
   - Sync repo memory to `.spek/memory/`

7. **Commit:**
   - `git add .spek/vault/ .spek/memory/` then `git commit`

8. **Blind Review (optional):**
   - Run `/spek.blind-review` for a context-free quality pass before archiving

9. **RARV (optional):**
   - Run `/spek.rarv` to detect and resolve spec drift (recommended for features with architectural changes)

**Output:**
- Analysis report (spec drift, outcomes vs criteria)
- Lessons document (`.spek/vault/lessons/YYYY-MM-DD-feature-name.md`)
- Updated patterns + decisions (`.spek/vault/`)
- Failure patterns from test run captured in vault (or none found)
- Token usage summary
- Repo memory synced (`.spek/memory/`)
- lat.md index refreshed

**Note:** `/spek.lessons` is both a first-class skill AND a sub-step of `/spek.conclude`. Conclude calls it automatically. You can also invoke it independently at any point.

---

## Optional Enhancements: Context & Analysis

The following commands are **first-class and fully documented**, but **not required** for basic feature development. Use them to enhance context loading, verify dependencies, or analyze impact.

### `/spek.context` — Load Project Context

**Purpose:** Load vault context (decisions, patterns, lessons) into current session  
**Usage:** `/spek.context`

**When to use:**
- Before starting implementation to review past decisions
- During planning to find related patterns
- At any point to inject project knowledge

**What it does:**
1. Read `.spek/vault/decisions.md` — load project decisions into session
2. Read `.spek/vault/patterns.md` — load reusable patterns into session
3. Read all files in `.spek/vault/lessons/` — load prior lessons into session
4. Read `.spek/memory/` — load workspace-scoped facts into session
5. Session state populated; all downstream `/spek.*` commands have full context available

**Output:**
- Project decisions, patterns, lessons, and workspace facts loaded into agent session

---

### `/spek.map` — Analyze Dependencies & Impact

**Purpose:** Query lat.md and vault to map code dependencies for a spec topic  
**Usage:** `/spek.map [topic]`

**When to use:**
- To verify what code/specs are affected by a change
- To identify blockers or dependencies before starting
- To understand critical paths in feature dependencies

**What it does:**
1. Query lat.md MCP for code references to the spec topic: symbols, callers, definitions, and call graphs
2. Query `.spek/vault/` for related decisions and dependent specs that touch the same topic
3. Generate dependency graph: list files, symbols, and specs related to the topic
4. Highlight blockers (items that must change before this topic can be modified) and critical paths

**Output:**
- Dependency graph: files, symbols, and specs related to the topic
- Blockers list: items that must change first
- Critical paths: sequence of changes required

---

### `/spek.blind-review` — Context-Free Quality Pass

**Purpose:** Run a linter + complexity check with AI attribution anonymized  
**Usage:** `/spek.blind-review`  
**Requires:** Linter installed and configured (pylint, flake8, eslint, or equivalent)

**When to use:**
- After implementation completes, before `/spek.conclude`
- When AI-generated code needs independent quality verification

**What it does:**
1. Anonymize source files **in working memory only** — strip AI vendor names from comments, replace service class names with generic aliases; original files are never modified
2. Run configured linter on anonymized copy; classify findings as CRITICAL / WARNING / INFO
3. Confirm all tests pass; report failures as CRITICAL with file:line reference
4. Flag functions exceeding 20 lines or cyclomatic complexity > 10 as WARNING
5. Write full report to `.spek/memory/blind-review-YYYY-MM-DD.md`; print summary `CRITICAL: N | WARNING: N | INFO: N`

**Output:**
- Findings report with file:line references and remediation hints
- Summary count: `CRITICAL: N | WARNING: N | INFO: N`
- Full report at `.spek/memory/blind-review-YYYY-MM-DD.md`

---

### `/spek.rarv` — Spec Drift Detection & Resolution

**Purpose:** Detect and resolve spec drift via Reason-Act-Reflect-Verify cycle  
**Usage:** `/spek.rarv`  
**Requires:** `/spek.conclude` complete; lat.md index current; vault accessible

**When to use:**
- After `/spek.conclude` for features with architectural changes or complex deviations
- When spec and implementation may have diverged

**What it does:**
1. **REASON:** Load original spec from `.spek/vault/specs/`; query lat.md for implemented symbols and changed files; build spec vs implementation map; identify deviations (additions, omissions, architecture changes)
2. **ACT:** For each deviation, prompt user: Option A (fix code), Option B (update spec + vault), Option C (defer as tech debt)
3. **REFLECT:** If Option B chosen — update `.spek/vault/decisions.md` or `.spek/vault/patterns.md` with justification; if Option C chosen — append tech debt item to `.spek/vault/patterns.md`
4. **VERIFY:** Re-read updated vault decisions; confirm no new contradictions; print alignment summary

**Output:**
- Deviation report: spec vs implementation gaps
- Updated vault files where Option B chosen
- Tech debt entries where Option C chosen
- Alignment summary: `N resolved (A), N justified (B), N deferred (C)`

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

**Purpose:** Activate Caveman compression mode (terse, compressed output). Installed automatically by `spek init` from `github:JuliusBrussee/caveman`. For Claude Code, auto-activates on every session start via project-level hooks — no manual invocation needed.
**Usage:** `/caveman [lite|full|ultra]`

**Modes:**
- `lite`: modest token reduction (remove explanations)
- `full`: significant token reduction (terse format, abbreviations) — DEFAULT
- `ultra`: maximal token reduction (minimal prose, lossy)

**What it does:**
1. Enable terse output mode for current session
2. Compress responses at each workflow stage where configured
3. Preserve technical accuracy and searchable keywords
4. Switch back to normal mode with `/caveman off`

**Installation:** `spek init` installs the caveman skill file into the integration's skills directory and (for `claude` integration) writes `SessionStart` + `UserPromptSubmit` hooks to `.claude/settings.json` for automatic activation. See [setup.md](setup.md#caveman-skill-installation) for details.

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

*For workflow diagrams and execution patterns, see [workflow.md](workflow.md).*

---

## Command Naming & Invocation

### Spekificity User-Facing Skills (`spek.*` prefix)

**Pattern:** `/spek.oneword` — action-oriented, imperative verbs

| Tier | Command | Purpose |
|------|---------|----------|
| **REQUIRED** | `/spek.prepare` | Initialize workspace, lat.md indexes, vault context |
| **REQUIRED** | `/spek.plan` | Orchestrate spec → plan → tasks with anti-sycophancy check |
| **REQUIRED** | `/spek.implement` | Execute tasks with context |
| **REQUIRED** | `/spek.conclude` | Archive outcomes, backprop, lessons, index refresh |
| *Optional* | `/spek.context` | Load vault decisions, patterns, lessons |
| *Optional* | `/spek.map` | Query code graph + vault for topic dependencies |
| *Optional (also auto-called by conclude)* | `/spek.lessons` | Capture lessons, patterns, decisions to vault |
| *Optional* | `/spek.blind-review` | Context-free quality pass (linter + complexity) |
| *Optional* | `/spek.rarv` | Detect and resolve spec drift (RARV cycle) |

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

