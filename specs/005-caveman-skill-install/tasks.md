# Tasks: Caveman Skill Install

**Input**: Design documents from `/specs/005-caveman-skill-install/`

**Branch**: `005-caveman-skill-install`

**Organization**: Tasks grouped by user story — each phase independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: User story label (US1/US2/US3) for traceability
- Exact file paths included in all descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the new `caveman` sub-package structure.

- [x] T001 Create `spekificity/caveman/__init__.py` (empty — marks package)
- [x] T002 Create `spekificity/caveman/install.py` with `CavemanInstallResult` dataclass and `_strip_jsonc()` helper

**T002 detail**: `CavemanInstallResult` fields: `tool: str`, `status: str`, `skill_status: str`, `hook_status: str`, `message: str`, `exit_code: int = 0`. `_strip_jsonc(src: str) -> str` removes `//` line comments, `/* */` block comments (string-aware), and trailing commas — mirrors caveman's `stripJsonComments()` in `bin/lib/settings.js`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared helper needed by all user stories.

**⚠️ CRITICAL**: US1 and US2 implementation both depend on this phase.

- [x] T003 Implement `_fetch_skill_content() -> bytes | None` in `spekificity/caveman/install.py`

**T003 detail**: Resolution order: (1) `Path.home() / ".claude/skills/caveman/SKILL.md"`, (2) scan `Path.home() / ".claude/plugins/cache/caveman/caveman/"` for latest SHA subdir → read `plugins/caveman/skills/caveman/SKILL.md`, (3) `urllib.request.urlopen("https://raw.githubusercontent.com/JuliusBrussee/caveman/main/plugins/caveman/skills/caveman/SKILL.md", timeout=10)`. Returns `None` if all fail; calls `print_status("WARN", ...)` before returning.

**Checkpoint**: Foundational complete — US1 and US2 can now proceed.

---

## Phase 3: User Story 1 — Install Caveman Skill File (Priority: P1) 🎯 MVP

**Goal**: `spek init` installs caveman skill file into integration's skills directory for all integrations.

**Independent Test**: Run `spek init --integration copilot --script sh` on a clean project; verify `<skills-dir>/caveman/SKILL.md` exists; re-run and verify `[SKIP]` reported with no overwrite. See quickstart.md Scenario 1.

### Implementation for User Story 1

- [x] T004 [P] [US1] Implement `_copy_skill(project_path, integration, content) -> str` in `spekificity/caveman/install.py`
- [x] T005 [US1] Implement `install_caveman(project_path, integration) -> CavemanInstallResult` entry point (fetch + copy path, no hooks yet) in `spekificity/caveman/install.py`
- [x] T006 [US1] Add Step 8 caveman install call to `spekificity/cli.py` after existing Step 7 (skills copy)
- [x] T007 [P] [US1] Write unit tests for `_fetch_skill_content()`: `test_skill_fetch_from_global_skills`, `test_skill_fetch_falls_back_to_plugin_cache`, `test_skill_fetch_falls_back_to_github`, `test_skill_fetch_all_fail_returns_none` in `tests/test_caveman_install.py`
- [x] T008 [P] [US1] Write unit tests for `_copy_skill()`: `test_copy_skill_flat_integration` (claude/copilot/generic → `caveman.md`), `test_copy_skill_subfolder_integration` (others → `caveman/SKILL.md`), `test_copy_skill_idempotent` (second call returns `"skipped"`, no overwrite) in `tests/test_caveman_install.py`
- [x] T009 [P] [US1] Write unit test `test_install_caveman_failure_non_fatal`: all fetch sources fail → `CavemanInstallResult.status == "failed"`, no exception raised in `tests/test_caveman_install.py`

**T004 detail**: Flat integrations (`claude`, `copilot`, `generic`) → `<skills-dir>/caveman.md`. Subfolder integrations → `<skills-dir>/caveman/SKILL.md`. If destination exists: return `"skipped"` + `print_status("SKIP", ...)`. If `content` is `None`: return `"failed"` + `print_status("WARN", ...)`. Otherwise write and return `"installed"` + `print_status("OK", ...)`.

**T005 detail**: Call `_fetch_skill_content()`, then `_copy_skill()`. `hook_status = "n/a"` at this stage. Return `CavemanInstallResult`.

**T006 detail**: Add after `copy_skills(project_path, integration)` (line 98):
```python
# --- Step 8: Caveman ---
from spekificity.caveman.install import install_caveman
install_caveman(project_path, integration)
```
Caveman failure must not set `needs_exit_2`.

**Checkpoint**: US1 complete. `spek init` installs caveman skill for all integrations. No hook writes yet.

---

## Phase 4: User Story 2 — Auto-Activation for Claude Code (Priority: P2)

**Goal**: `spek init --integration claude` writes `SessionStart` and `UserPromptSubmit` hooks to project `.claude/settings.json`.

**Independent Test**: Run `spek init --integration claude --script sh`; verify `.claude/settings.json` contains `caveman-activate` in `SessionStart` hooks and `caveman-mode-tracker` in `UserPromptSubmit` hooks; re-run and verify no duplicates. See quickstart.md Scenario 2.

### Implementation for User Story 2

- [x] T010 [US2] Implement `_ensure_global_hooks() -> bool` in `spekificity/caveman/install.py`
- [x] T011 [US2] Implement `_write_project_hooks(project_path) -> str` in `spekificity/caveman/install.py`
- [x] T012 [US2] Update `install_caveman()` in `spekificity/caveman/install.py` to call `_write_project_hooks()` when `integration == "claude"` and set `hook_status` on result
- [x] T013 [P] [US2] Write unit tests for `_write_project_hooks()`: `test_write_project_hooks_creates_settings_json` (settings.json absent → created with both hooks), `test_write_project_hooks_merges_existing` (existing non-caveman entries preserved), `test_write_project_hooks_idempotent` (second call returns `"skipped"`, no duplicate entries), `test_write_project_hooks_node_not_found` (node absent → returns `"failed"`, no exception) in `tests/test_caveman_install.py`

**T010 detail**: Check `Path.home() / ".claude/hooks/caveman-activate.js"` exists → return `True`. Else try `node <plugin-cache>/bin/install.js --skip-skills --non-interactive` (scan cache for latest SHA). Else try `subprocess.run(["npx", "-y", "github:JuliusBrussee/caveman", "--skip-skills", "--non-interactive"])`. Return `True` if hooks present after any attempt; `False` if all fail. Use `print_status("WARN", ...)` on failure.

**T011 detail**: (1) `node = shutil.which("node")` — return `"failed"` if None. (2) Call `_ensure_global_hooks()` — return `"failed"` if False. (3) Read `project_path / ".claude/settings.json"` via `_strip_jsonc()` + `json.loads()`; default to `{}` if absent. (4) Idempotency: if any `SessionStart` hook command contains `"caveman-activate"` → return `"skipped"`. (5) Add both hook entries per contract shape in [contracts/caveman-install-api.md](contracts/caveman-install-api.md). (6) Atomic write: `json.dumps(settings, indent=2)` → temp file → `os.replace()` → `print_status("OK", ...)`. Return `"installed"`.

**Checkpoint**: US2 complete. Claude Code sessions in initialized projects auto-activate caveman.

---

## Phase 5: User Story 3 — Non-Claude Integrations Explicit Validation (Priority: P3)

**Goal**: Confirm that non-Claude integrations receive skill file only — no `.claude/settings.json` written.

**Independent Test**: Run `spek init --integration gemini --script sh`; verify caveman skill installed in `.gemini/skills/caveman/SKILL.md`; verify no `.claude/settings.json` created. See quickstart.md Scenario 1 (any non-Claude integration).

### Implementation for User Story 3

- [x] T014 [P] [US3] Write unit test `test_install_caveman_non_claude_no_hooks`: call `install_caveman(project_path, "gemini")` → verify `hook_status == "n/a"`, no `.claude/settings.json` created in `tests/test_caveman_install.py`
- [x] T015 [P] [US3] Write unit test `test_install_caveman_non_claude_skill_installed`: call `install_caveman(project_path, "gemini")` → verify skill written to `.gemini/skills/caveman/SKILL.md` in `tests/test_caveman_install.py`

**Checkpoint**: All 3 user stories complete and independently testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Package wiring, validation, documentation.

- [x] T016 [P] Verify `spekificity/caveman/` package is included in wheel: check `pyproject.toml` `[tool.hatch.build.targets.wheel]` `packages` list — add `"spekificity/caveman"` if missing
- [x] T017 Run quickstart.md Scenario 1 end-to-end: `spek init --integration copilot` on clean project, verify skill file present and idempotency
- [x] T018 Run quickstart.md Scenario 2 end-to-end: `spek init --integration claude` on clean project, verify `settings.json` hooks and idempotency
- [x] T019 [P] Run full test suite: `python3 -m pytest tests/test_caveman_install.py -v` — all tests green

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — blocks Phase 3 and 4
- **US1 (Phase 3)**: Depends on Phase 2 — MVP deliverable
- **US2 (Phase 4)**: Depends on Phase 3 (needs `install_caveman()` entry point to update) — add hooks path
- **US3 (Phase 5)**: Depends on Phase 3 (needs `install_caveman()` to exist) — validation only
- **Polish (Phase 6)**: Depends on all story phases

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — no cross-story dependencies
- **US2 (P2)**: Can start after US1 complete (updates `install_caveman()`) — depends on US1 entry point
- **US3 (P3)**: Can start after US1 complete (validates non-Claude path) — no dependency on US2

### Within Each Phase

- T004 and T005 sequential within US1 (T005 calls T004)
- T010 and T011 sequential within US2 (T011 calls T010)
- All `[P]`-marked tasks within a phase can run in parallel
- Test tasks `[P]` within a phase can be written concurrently with each other

### Parallel Opportunities

Within Phase 3 (US1): T007, T008, T009 all write to `tests/test_caveman_install.py` — sequential by file, but logically independent test groups
Within Phase 4 (US2): T013 test cases are independent
Within Phase 5 (US3): T014 and T015 can run in parallel (different test functions)

---

## Parallel Example: Phase 3 (US1)

```
# Sequential core:
T004 → T005 → T006   (copy_skill → install_caveman → cli.py wire-up)

# Parallel after T005 exists (can be started once function signatures are stable):
T007: skill fetch tests
T008: copy skill tests
T009: failure test
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: Setup — create module skeleton
2. Phase 2: Foundational — implement `_fetch_skill_content()`
3. Phase 3: US1 — implement `_copy_skill()`, `install_caveman()`, wire into `cli.py`
4. **STOP and VALIDATE**: `spek init --integration copilot` on clean project; verify skill installed; verify idempotency
5. Ship US1 — caveman skill available in all integrations

### Incremental Delivery

1. MVP (US1) → all integrations get caveman skill
2. Add US2 → Claude Code users get auto-activation
3. Add US3 validation → explicit regression guard for non-Claude path
4. Polish → pyproject.toml check, quickstart validation, full test run

---

## Notes

- `[P]` tasks = different files or independent test functions — safe to parallelize
- Each user story phase ends with a `Checkpoint` — validate before moving to next phase
- `_strip_jsonc()` is critical for correctness — Claude Code writes commented `settings.json`
- Atomic write for `settings.json` (`os.replace()`) prevents corruption on partial writes
- `install_caveman()` must never raise — all errors go to `CavemanInstallResult.status`
- `spek init` exit code unaffected by caveman failures (FR-009)
