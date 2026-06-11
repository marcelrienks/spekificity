# Feature Specification: Caveman Skill Install

**Feature Branch**: `005-caveman-skill-install`

**Created**: 2026-06-11

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install Caveman During Init (Priority: P1)

A developer initializes a new project with `spek init` and, as part of the setup, the caveman skill is automatically installed alongside SpecKit, lat.md, and Obsidian. After init completes, the user can immediately invoke `/caveman` to activate compressed output mode within their agent.

**Why this priority**: Core install path — without this, no other story is possible. Caveman must be a first-class citizen of `spek init` to be usable.

**Independent Test**: Can be fully tested by running `spek init` on a clean project and verifying the caveman skill file exists in the integration's skills directory, then invoking `/caveman` in the agent and confirming compressed output.

**Acceptance Scenarios**:

1. **Given** a project directory with no prior `spek init`, **When** the user runs `spek init` and selects any integration, **Then** a caveman skill file is present in the integration's skills directory after init completes
2. **Given** caveman is already installed, **When** the user re-runs `spek init`, **Then** the existing caveman skill file is not overwritten and init reports it as skipped
3. **Given** caveman install fails (e.g., source unavailable), **When** `spek init` runs, **Then** init continues and reports caveman as failed without aborting the rest of setup

---

### User Story 2 - Auto-Activation for Claude Code (Priority: P2)

A Claude Code user runs `spek init` with the `claude` integration selected. Caveman mode is automatically enabled by default through project-level configuration so that every session in that project starts with compressed output — without the user needing to manually invoke `/caveman`.

**Why this priority**: The primary target agent is Claude Code. Auto-activation delivers value passively; the user benefits without changing their workflow.

**Independent Test**: Can be fully tested by running `spek init --integration claude` and verifying the project's `.claude/settings.json` contains a startup hook entry for caveman. Opening Claude Code in that project confirms caveman mode is active immediately.

**Acceptance Scenarios**:

1. **Given** `spek init` is run with the `claude` integration, **When** init completes, **Then** a caveman startup hook entry exists in the project's `.claude/settings.json`
2. **Given** a Claude Code session in the initialized project, **When** the user sends any message, **Then** the agent responds in caveman-compressed format without manual activation
3. **Given** `.claude/settings.json` already contains a caveman hook entry, **When** `spek init` is re-run, **Then** the hook is not duplicated and init reports it as skipped
4. **Given** `.claude/settings.json` does not exist, **When** `spek init` with `claude` integration runs, **Then** the file is created with the caveman hook entry

---

### User Story 3 - Caveman Available on Non-Claude Integrations (Priority: P3)

A developer using Copilot, Gemini, Cursor, or any other supported integration runs `spek init`. The caveman skill is installed as a manually-invocable skill file in the integration's skills directory. The user can invoke `/caveman` (or the equivalent for their agent) to activate compressed mode on demand.

**Why this priority**: Broadens value to all supported integrations. No auto-activation since hook mechanisms vary by agent; manual invocation is the universal fallback.

**Independent Test**: Can be fully tested by running `spek init` with a non-Claude integration and verifying the caveman skill file exists in the correct integration skills directory.

**Acceptance Scenarios**:

1. **Given** `spek init` is run with a non-Claude integration (e.g., `copilot`, `gemini`), **When** init completes, **Then** a caveman skill file is present in that integration's skills directory
2. **Given** the caveman skill file is installed for a non-Claude integration, **When** the user invokes `/caveman` in their agent, **Then** the agent activates compressed output mode
3. **Given** a non-Claude integration, **When** `spek init` completes, **Then** no auto-activation configuration is written (no hook injection for non-Claude agents)

---

### Edge Cases

- What happens when the caveman source (bundled or remote package) is unavailable during install?
- How does the system handle `.claude/settings.json` that already has a startup hooks section with conflicting entries?
- What if the integration's skills directory is read-only or permission-denied?
- What if the user has manually set a different caveman intensity level in an existing hook entry?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `spek init` MUST install caveman skill file(s) into the integration's designated skills directory as part of the standard init flow
- **FR-002**: The installed caveman skill MUST be invocable by users as `/caveman` (or integration-equivalent) after `spek init` completes
- **FR-003**: The caveman skill MUST support three intensity levels: `lite`, `full`, and `ultra`, with `full` as the default
- **FR-004**: For the `claude` integration, `spek init` MUST write a startup hook entry to the project's `.claude/settings.json` that activates caveman mode automatically on session start
- **FR-005**: For all non-Claude integrations, `spek init` MUST install the caveman skill file only — no auto-activation configuration is written
- **FR-006**: Caveman skill content MUST be fetched at install time from the caveman npm/PyPI package — the package version MUST be pinned or resolved to latest stable at install time, and `spek init` MUST fail gracefully if the caveman package is unavailable
- **FR-007**: Caveman installation MUST be idempotent — re-running `spek init` MUST NOT overwrite existing caveman skill files or duplicate hook entries
- **FR-008**: `spek init` MUST report caveman installation status (installed / skipped / failed) in its output alongside other tool statuses
- **FR-009**: If caveman installation fails, `spek init` MUST continue initializing remaining tools and report caveman failure without aborting the overall init process
- **FR-010**: The caveman startup hook for Claude Code MUST activate caveman at `full` intensity by default unless the project already has a caveman hook with a different intensity

### Key Entities

- **Caveman Skill File**: The markdown instruction set that defines caveman behavior for an agent. One file per integration format (flat `.md` or subfolder `SKILL.md`).
- **Caveman Hook Entry**: A configuration entry in `.claude/settings.json` that triggers caveman activation on session start. Specific to Claude Code integration.
- **Intensity Level**: The compression setting (`lite` / `full` / `ultra`) controlling how aggressively output is compressed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After `spek init` completes, users can activate caveman mode with a single command — no additional setup steps required
- **SC-002**: Claude Code users have caveman mode active by default in initialized projects without any manual configuration
- **SC-003**: All 10+ supported integrations have caveman skill accessible after `spek init`
- **SC-004**: Re-running `spek init` on an already-initialized project produces no duplicate skill files or hook entries
- **SC-005**: Caveman install failure does not block or abort `spek init` — remaining tools install successfully in 100% of caveman-failure scenarios

## Assumptions

- Caveman skill file content is agent-agnostic markdown — the same file works across all supported integrations
- The `full` intensity level is the correct default for most users; users can override by invoking `/caveman lite` or `/caveman ultra` manually after install
- Auto-activation scope is project-level (`.claude/settings.json` in the project root), not user-global (`~/.claude/settings.json`), keeping caveman opt-in per-project
- The Claude Code startup hook mechanism (e.g., `UserPromptSubmit` or `SessionStart` hook in `.claude/settings.json`) is the correct auto-activation vector
- Caveman install follows the same idempotency rules as existing skills in `copy.py` — never overwrites, always reports skip if already present
- Non-Claude integrations do not have a standardized hook/startup config format, so auto-activation is Claude-only for this feature
