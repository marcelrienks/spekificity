# Feature Specification: Full Platform Implementation

**Feature Branch**: `003-full-platform-impl`

**Created**: 2026-06-11

**Status**: Draft

**Input**: User description: "use all of the information across all wiki documents, the feature is to fully implement all that the documentation outlines"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Package Installs and Prerequisites Are Verified (Priority: P1)

A developer installs the `spekificity` package globally and gets a working `spek` CLI. When they run `spek init` on a machine with a missing prerequisite (Python, uv, Node.js, or git), they get a clear error naming the missing tool and its install command — before any setup work begins.

**Why this priority**: Foundation. No other phase can be built or tested without the package structure and prerequisite checks in place.

**Independent Test**: Install the package with `uv tool install`, run `spek --version`, run `spek init` with a missing prerequisite and confirm the error output names the right tool.

**Acceptance Scenarios**:

1. **Given** the package is installed via `uv tool install spekificity`, **When** `spek --version` is run, **Then** a version string is printed and exit code is 0.

2. **Given** `uv` is not in PATH, **When** `spek init` runs, **Then** exit code is 1 and the error message names `uv` and provides its install URL.

3. **Given** all prerequisites are present, **When** `spek init` runs the prerequisite check, **Then** all checks pass silently and init proceeds to the next step.

---

### User Story 2 - Tool Integrations Install and Configure Correctly (Priority: P2)

A developer's project gets lat.md, Obsidian vault, and SpecKit set up correctly when `spek init` runs. Each tool is detected if already present and skipped, or installed if missing. Each integration produces its expected artifact: a lat index, a registered vault with content files, and an initialized `.specify/` directory.

**Why this priority**: The three integration modules are the core substance of what `spek init` does. They are independent of each other and can be built and verified in parallel. Each has clear, testable outputs.

**Independent Test**: Unit-test each module in isolation with mocked subprocess calls. Verify each module's idempotency check correctly detects the "already done" condition.

**Acceptance Scenarios**:

1. **Given** `lat` is not in PATH, **When** the lat.md module runs, **Then** `npm install -g lat.md` is executed, `lat init` initializes the code index, `lat init --docs` initializes the doc index, the MCP config is written to the integration-specific file, and the git post-commit hook contains `lat update`.

2. **Given** Obsidian is not installed, **When** the vault module runs on macOS, **Then** `brew install --cask obsidian` runs; if `obsidian` is then in PATH, vault setup completes; if not, init halts with exit code 2 and CLI registration instructions are printed.

3. **Given** `obsidian` is in PATH and vault is not yet registered, **When** the vault module runs, **Then** `.spek/vault/` is created with `lessons/`, `decisions.md`, and `patterns.md`; the vault is registered in Obsidian via `obsidian open-vault`.

4. **Given** `specify` is not in PATH, **When** the speckit module runs, **Then** `uv tool install specify-cli` runs, `specify init` creates `.specify/`, and `.spek/config.yaml` is written with the correct integration and tool configuration.

5. **Given** all three tools are already installed and initialized, **When** each module runs again, **Then** all steps are skipped and `[SKIP]` is reported for each — no reinstalls, no file overwrites.

---

### User Story 3 - Agent Skills Are Correct and Distributed (Priority: P3)

A developer whose project has been initialized opens their agent (Claude Code, Copilot, Cursor, etc.) and finds all seven `/spek.*` skill files installed in the correct location. Each file is valid plain markdown they can invoke immediately. The skills correctly describe the full 4-stage workflow and the supplementary commands.

**Why this priority**: The skill files ARE the user-facing product — the documented workflow instructions the agent reads. They can be authored and reviewed independently of the Python CLI.

**Independent Test**: Inspect each of the 7 skill files for correct markdown structure (Prerequisites, Steps, Output, Exit Criteria), absence of agent-specific syntax, and correct content per the wiki documentation. Run `skills_install/` copy logic against each integration type and verify destination paths.

**Acceptance Scenarios**:

1. **Given** skill files are installed for the `claude` integration, **When** `.claude/commands/` is listed, **Then** all 7 `spek-*.md` files are present as flat `.md` files.

2. **Given** skill files are installed for the `cursor-agent` integration, **When** `.cursor/skills/spek-prepare/` is checked, **Then** `SKILL.md` exists at the subfolder path.

3. **Given** any of the 7 skill files, **When** the content is inspected, **Then** it starts with `# /spek.COMMAND`, contains Prerequisites/Steps/Output/Exit Criteria sections, uses imperative-mood steps, and contains no `@workspace`, `#file:`, or `[[wikilink]]` syntax.

4. **Given** a skill file already exists at the destination, **When** `skills_install/copy.py` runs again, **Then** the existing file is not overwritten (idempotent).

---

### User Story 4 - `spek init` Works End-to-End (Priority: P4)

A developer runs `spek init` in a clean project and gets a fully initialized Spekificity workspace in a single command. They can pass flags for non-interactive use. Re-running the command on an already-initialized project produces no errors and no side effects.

**Why this priority**: The CLI is the integrating layer that wires all prior phases together. Verified last because it depends on P1–P3 being complete.

**Independent Test**: Run `spek init --integration claude --script sh` in a clean git repo with all prerequisites met. Verify all output artifacts. Re-run and verify idempotency.

**Acceptance Scenarios**:

1. **Given** a clean project with all prerequisites met, **When** `spek init --integration claude --script sh` completes, **Then** `.spek/vault/`, `.spek/memory/`, `.spek/lat/`, `.spek/config.yaml`, `.claude/commands/spek-*.md` (7 files), `.mcp.json` (with lat entry), `.specify/`, and `.git/hooks/post-commit` all exist.

2. **Given** a fully initialized project, **When** `spek init` is run again, **Then** exit code is 0, every line of output is `[SKIP]`, and no files are modified.

3. **Given** `--no-git-hooks` flag is passed (or `.spek/.disable-git-hooks` exists), **When** `spek init` completes, **Then** `.git/hooks/post-commit` is not created.

4. **Given** `spek init` is run interactively without flags, **When** prompts appear, **Then** the user is asked for integration type and script type; accepted values are any valid `specify integration list` value.

---

### Edge Cases

- Obsidian installed but CLI never registered (binary missing from PATH after install) → exit code 2, not 1; registration instructions printed.
- Any module returning exit code 1 halts `spek init` immediately (fail-fast). Vault exit code 2 is different: it halts only vault remaining steps — lat.md, SpecKit, and skills-install steps complete normally before the halt.
- `.spek/` partially exists (e.g. prior failed run) → idempotency: skip existing, complete missing.
- Integration type not in known list → fall back to `.agents/skills/` subfolder format; print manual MCP config instructions; no error.
- `specify init` fails mid-run → surface error, halt; re-run is idempotent and retries only missing steps.
- Existing MCP config entries must be preserved → parse JSON, merge `lat` entry, write back; never clobber other entries.
- Linux Obsidian → print download URL, continue remaining steps without vault setup.

## Requirements *(mandatory)*

### Functional Requirements

**P1 — Foundation**
- **FR-001**: Package MUST install as `spek` CLI via `uv tool install spekificity`
- **FR-002**: `spek init` MUST verify Python 3.11+, `uv`, Node.js 22+, and `git` are in PATH before any setup work. Version validation is required for Python (≥3.11) and Node.js (≥22); `uv` and `git` require only PATH presence.
- **FR-003**: Each failed prerequisite check MUST name the missing tool and provide its install command
- **FR-004**: Package MUST declare `skills/*.md` as package data so skill files are bundled in the distribution
- **FR-005**: A shared `utils.py` MUST provide the subprocess runner and `[OK]/[SKIP]/[WARN]/[ERROR]` output formatter used by all modules

**P2 — Integration Modules**
- **FR-006**: lat.md module MUST detect `lat` in PATH; if absent, install via `npm install -g lat.md`
- **FR-007**: lat.md module MUST run `lat init` (code index) and `lat init --docs` (doc index)
- **FR-008**: lat.md module MUST write the lat MCP server entry to the integration-specific config file without clobbering existing entries
- **FR-009**: lat.md module MUST install a git post-commit hook containing `lat update`
- **FR-010**: Vault module MUST detect Obsidian; if absent, install via `brew` (macOS), `winget` (Windows), or print URL (Linux)
- **FR-011**: Vault module MUST implement two-phase Obsidian flow: install → check `obsidian` in PATH → halt exit code 2 if not found → complete vault setup on re-run. Halt output MUST print to stderr the CLI registration instructions **verbatim** from `wiki/setup.md` "Phase 1 halt — warning output" block (the `⚠  Obsidian installed...` block ending with `spek init will complete all remaining setup autonomously.`)
- **FR-012**: Vault module MUST create `.spek/vault/` (with `lessons/`, `decisions.md` (`# Decisions`), `patterns.md` (`# Patterns`), `lessons/.keep`), `.spek/memory/`, and `.spek/lat/` directories
- **FR-013**: Vault module MUST register and open the vault in Obsidian via `obsidian open-vault`
- **FR-014**: SpecKit module MUST detect `specify` in PATH; if absent, install via `uv tool install specify-cli`
- **FR-015**: SpecKit module MUST run `specify init` to create `.specify/`
- **FR-016**: SpecKit module MUST write `.spek/config.yaml` with integration, script type, and tool configuration
- **FR-017**: All three integration modules MUST be idempotent — each step checks its "already done" condition before acting

**P3 — Skill Files**
- **FR-018**: Seven skill files MUST exist in `spekificity/skills/`: `spek-prepare.md`, `spek-plan.md`, `spek-implement.md`, `spek-conclude.md`, `spek-lessons.md`, `spek-context.md`, `spek-map.md`
- **FR-019**: All seven skill files MUST be plain markdown with no agent-specific syntax (`@workspace`, `#file:`, `[[wikilink]]`)
- **FR-020**: Each skill file MUST contain exactly these H2 sections in order: `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`. Steps MUST use imperative mood.
- **FR-021**: `skills_install/` MUST copy flat `.md` files for `claude`, `copilot`, `generic`; subfolder `SKILL.md` for all others
- **FR-022**: Skill files already present at destination MUST NOT be overwritten

**P4 — CLI**
- **FR-023**: `spek init` MUST support interactive prompts for integration type and script type
- **FR-024**: `spek init` MUST support non-interactive mode via `--integration` and `--script` flags
- **FR-025**: `spek init` MUST accept an optional `[path]` argument to initialize a non-current directory
- **FR-026**: `spek init` MUST skip git hook installation if `.spek/.disable-git-hooks` exists or `--no-git-hooks` is passed
- **FR-027**: `spek init` MUST be idempotent — re-running on an initialized project exits 0 with only `[SKIP]` output

### Key Entities

- **`spek` CLI**: Python entry point (`spekificity.cli:main`), sole command is `init`
- **Integration modules**: `lat_md/`, `vault/`, `speckit/` — each owns one tool's install + configure lifecycle
- **Skill files**: `spekificity/skills/*.md` — canonical agent workflow definitions, bundled as package data
- **`skills_install/`**: Handles per-integration skill file distribution logic
- **`.spek/config.yaml`**: Per-project configuration written by SpecKit module at init time

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `spek --version` prints a version string; exit code 0
- **SC-002**: Every prerequisite failure produces output naming the missing tool with its install command; exit code 1
- **SC-003**: Each integration module's unit tests pass with mocked subprocess calls
- **SC-004**: `spek init` completes without errors on a clean project in under 5 minutes (excluding user interaction time for tool installs)
- **SC-005**: Re-running `spek init` on an initialized project produces exit code 0 and only `[SKIP]` output lines
- **SC-006**: Obsidian Phase 1 halt exits with code 2 and prints the CLI registration steps from `wiki/setup.md`
- **SC-007**: All 7 skill files are valid markdown with the correct section structure and zero agent-specific syntax
- **SC-008**: Skill files land in the correct path format for `claude`, `copilot`, `cursor-agent`, and `generic` integrations
- **SC-009**: The lat.md MCP entry is correctly written for `claude`, `copilot`, and `cursor-agent` without corrupting existing config
- **SC-010**: Given `obsidian` is in PATH and vault not yet initialized, when vault module runs, then `.spek/vault/` with required content exists and `obsidian open-vault` was called; exit code 0

## Assumptions

- Obsidian desktop v1.12.4+ required; older versions without the built-in CLI are out of scope
- Linux Obsidian install is manual; `spek init` prints download URL and skips vault setup on Linux
- `specify integration list` is available after SpecKit installs; integration validation uses it at runtime
- MCP config formats for `windsurf`, `cline`, `gemini`, `codex`, `kiro-cli`, `amp`, `qwen` are inferred from the `mcpServers` convention in `wiki/setup.md` and require vendor-doc verification before finalizing
- Skill files are written once and never regenerated on re-run; behavior changes require editing source and reinstalling
- Vault name in Obsidian matches the directory name (`vault`)
- `spek init` runs with user-level permissions; sudo not required
