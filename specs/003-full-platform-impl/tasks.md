# Tasks: Full Platform Implementation

**Input**: Design documents from `specs/003-full-platform-impl/`

**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared-state dependency)
- **[Story]**: Which user story ([US1], [US2], [US3], [US4])
- Exact file paths in all descriptions

---

## Phase 1: Setup

**Purpose**: Package infrastructure — entry point, dependencies, package data declaration

- [X] T001 Update `pyproject.toml` — add `click>=8.0` runtime dep, `pytest` dev dep, `package-data` for `spekificity/skills/*.md` (hatchling auto-includes but add explicit entry), entry point `spek = spekificity.cli:main`
- [X] T002 Create `spekificity/__init__.py` with `__version__ = "0.1.0"`

---

## Phase 2: Foundational (Blocking Prerequisite for All Modules)

**Purpose**: `utils.py` is the shared subprocess runner and `[OK]/[SKIP]/[WARN]/[ERROR]` formatter — every integration module imports it

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete

- [X] T003 Implement `spekificity/utils.py` — `run_command(cmd: list[str], description: str) -> subprocess.CompletedProcess` (no `shell=True`, `check=True`, capture stderr, `FileNotFoundError` → `RuntimeError`) + `print_status(tag: str, message: str)` formatter for `[OK]`/`[SKIP]`/`[WARN]`/`[ERROR]`
- [X] T004 [P] Write `tests/unit/test_utils.py` — unit tests for `run_command` success/failure/not-found paths and `print_status` output format

**Checkpoint**: Foundation ready — US1, US2, US3 can begin in parallel

---

## Phase 3: User Story 1 — Package Installs and Prerequisites Are Verified (Priority: P1) 🎯 MVP

**Goal**: `spek` CLI installable via `uv tool install spekificity`; prerequisite check fails fast naming the missing tool and its install command before any setup work begins

**Independent Test**: `uv tool install spekificity --from .`; run `spek --version`; remove `uv` from PATH and confirm error message names `uv` with install URL; exit code 1

- [X] T005 [P] [US1] Implement `spekificity/prerequisites.py` — `PrerequisiteResult` dataclass (`name`, `present`, `version`, `install_hint`); `check_prerequisites() -> list[PrerequisiteResult]` checks Python 3.11+, `uv`, Node.js 22+, `git` via `shutil.which`; halts on first missing tool with exit code 1 printing `install_hint`
- [X] T006 [P] [US1] Write `tests/unit/test_prerequisites.py` — one test per tool (present and absent cases); mock `shutil.which` via `unittest.mock.patch`; verify `install_hint` non-empty on failure

**Checkpoint**: US1 complete — package installs and prerequisite checks independently testable

---

## Phase 4: User Story 2 — Tool Integrations Install and Configure Correctly (Priority: P2)

**Goal**: lat.md, Obsidian vault, and SpecKit each detect/install/configure correctly with full idempotency; each module independently unit-tested with mocked subprocess calls

**Independent Test**: Run each module's unit test suite in isolation; verify "already done" conditions produce `[SKIP]` and no side effects

### lat.md Integration

- [X] T007 [P] [US2] Create `spekificity/lat_md/__init__.py` and implement `spekificity/lat_md/install.py` — `install_lat() -> ToolInstallResult`: detect `lat` via `shutil.which`; run `npm install -g lat.md` if absent; return `already_present` status if already in PATH
- [X] T008 [P] [US2] Implement `spekificity/lat_md/index.py` — `run_lat_index(project_path: Path) -> None`: run `lat init` (code index) then `lat init --docs` (doc index) via `utils.run_command`; idempotent check via `.spek/lat/` existence
- [X] T009 [P] [US2] Implement `spekificity/lat_md/mcp_config.py` — `write_mcp_config(config_path: Path, servers_key: str, extra_fields: dict) -> McpConfigResult`: read existing JSON (or `{}`), merge `lat` entry under `servers_key`, write back; skip if `lat` already present; create parent dirs; copilot gets `"type": "stdio"` via `extra_fields`
- [X] T010 [P] [US2] Implement `spekificity/lat_md/git_hook.py` — `write_git_hook(project_path: Path, skip: bool) -> None`: write `#!/bin/sh\nlat update` to `.git/hooks/post-commit`; `os.chmod` +x; skip if `skip=True`, `--no-git-hooks` flag, or `.spek/.disable-git-hooks` exists; idempotent (skip if hook already present)
- [X] T011 [P] [US2] Write `tests/unit/lat_md/test_install.py` — mock `shutil.which` and `subprocess.run`; test present path returns `already_present`; test absent path runs `npm install -g lat.md`
- [X] T012 [P] [US2] Write `tests/unit/lat_md/test_index.py` — mock `utils.run_command`; test both `lat init` calls made; test idempotency via `tmp_path` `.spek/lat/` presence
- [X] T013 [P] [US2] Write `tests/unit/lat_md/test_mcp_config.py` — test merge into existing JSON (existing entry preserved); test skip-if-present; test create-if-missing; test copilot extra fields; use `tmp_path`
- [X] T014 [P] [US2] Write `tests/unit/lat_md/test_git_hook.py` — test hook written with correct content; test skip when `.spek/.disable-git-hooks` present; test idempotency; use `tmp_path`

### Vault Integration

- [X] T015 [P] [US2] Create `spekificity/vault/__init__.py` and implement `spekificity/vault/install.py` — `install_obsidian() -> ToolInstallResult`: check `obsidian` in PATH first; dispatch `sys.platform`: `darwin` → `brew install --cask obsidian`, `win32` → `winget install -e --id Obsidian.Obsidian`, `linux` → print download URL and return `skipped`; after install attempt re-check `obsidian` in PATH → if absent return `needs_user_action` with `exit_code=2` and print CLI registration instructions
- [X] T016 [P] [US2] Implement `spekificity/vault/scaffold.py` — `scaffold_vault(project_path: Path) -> ScaffoldResult`: create `.spek/vault/lessons/`, `.spek/memory/`, `.spek/lat/` with `mkdir(parents=True, exist_ok=True)`; write `.spek/vault/decisions.md` (`# Decisions`), `.spek/vault/patterns.md` (`# Patterns`), `.spek/vault/lessons/.keep` (empty) if not exist; track created vs skipped in `ScaffoldResult`
- [X] T017 [P] [US2] Implement `spekificity/vault/init.py` — `init_vault(project_path: Path) -> None`: run `obsidian open-vault .spek/vault` via `utils.run_command`; `obsidian open-vault` is idempotent per `wiki/setup.md` (re-opening a registered vault is a no-op); always call if `obsidian` in PATH — no separate registration-state check required
- [X] T018 [P] [US2] Write `tests/unit/vault/test_install.py` — test `darwin`/`win32`/`linux` dispatch; test two-phase halt (install succeeds but `obsidian` still not in PATH → `needs_user_action`); mock `shutil.which`, `subprocess.run`, `sys.platform`
- [X] T019 [P] [US2] Write `tests/unit/vault/test_scaffold.py` — test all dirs and files created on first run; test idempotency (existing dirs/files → `skipped`); verify `decisions.md` content; use `tmp_path`
- [X] T020 [P] [US2] Write `tests/unit/vault/test_init.py` — mock `utils.run_command`; verify `obsidian open-vault` called with correct path; use `tmp_path`

### SpecKit Integration

- [X] T021 [P] [US2] Create `spekificity/speckit/__init__.py` and implement `spekificity/speckit/install.py` — `install_speckit() -> ToolInstallResult`: detect `specify` via `shutil.which`; run `uv tool install specify-cli` if absent; return `already_present` if already in PATH
- [X] T022 [P] [US2] Implement `spekificity/speckit/init.py` — `run_specify_init(project_path: Path) -> None`: check if `.specify/` dir exists (idempotent); run `specify init` via `utils.run_command` if not
- [X] T023 [P] [US2] Implement `spekificity/speckit/config.py` — `write_spek_config(project_path: Path, options: InitOptions) -> None`: write `.spek/config.yaml` using inline YAML string template (no PyYAML dep) matching `SpekConfig` schema; idempotent (skip if file exists)
- [X] T024 [P] [US2] Write `tests/unit/speckit/test_install.py` — mock `shutil.which` and `subprocess.run`; test present/absent paths; verify `uv tool install specify-cli` command when absent
- [X] T025 [P] [US2] Write `tests/unit/speckit/test_init.py` — mock `utils.run_command`; test `.specify/` idempotency check; test `specify init` called when dir absent; use `tmp_path`
- [X] T026 [P] [US2] Write `tests/unit/speckit/test_config.py` — test YAML output matches full `SpekConfig` schema (all required fields); test idempotency (skip if `.spek/config.yaml` exists); use `tmp_path`

**Checkpoint**: US2 complete — all three integration modules independently unit-tested

---

## Phase 5: User Story 3 — Agent Skills Are Correct and Distributed (Priority: P3)

**Goal**: All 7 skill files bundled as package data; `skills_install/` copies them to correct per-integration path in flat or subfolder format; idempotent

**Independent Test**: Inspect each of 7 skill files for `# /spek.COMMAND` heading + required sections + no agent syntax; run copy logic for `claude` and `cursor-agent` integrations, verify destination paths

### Skills Distribution Infrastructure

- [X] T027 [P] [US3] Create `spekificity/skills_install/__init__.py` and implement `spekificity/skills_install/integrations.py` — `FLAT_INTEGRATIONS: set[str]` (`{"claude", "copilot", "generic"}`); `INTEGRATION_SKILLS_DIR: dict[str, str]` (all 11 known integrations + fallback); `INTEGRATION_MCP_CONFIG: dict` (per contracts/mcp-config-schemas.md); `get_skills_config(integration: str) -> tuple[str, bool]` returns `(skills_dir, use_subfolder)` with fallback to `.agents/skills/` + subfolder for unknown
- [X] T028 [US3] Implement `spekificity/skills_install/copy.py` — `copy_skills(project_path: Path, integration: str) -> SkillInstallResult`: use `importlib.resources.files("spekificity") / "skills"` to iterate source files; flat integrations: copy to `<skills_dir>/spek-*.md`; subfolder integrations: copy to `<skills_dir>/spek-*/SKILL.md`; never overwrite existing files (`dest.exists()` check); create parent dirs; return `SkillInstallResult` (depends on T027 for `get_skills_config`)
- [X] T029 [P] [US3] Write `tests/unit/skills_install/test_integrations.py` — test all 11 known integrations return correct dir and format; test unknown integration falls back to `.agents/skills/` with subfolder; test `FLAT_INTEGRATIONS` membership
- [X] T030 [P] [US3] Write `tests/unit/skills_install/test_copy.py` — test flat copy produces `spek-prepare.md` at root of skills dir; test subfolder copy produces `spek-prepare/SKILL.md`; test no-overwrite when file already exists; use `tmp_path` with stub skill files

### Skill Files (all 7 — fully independent, can be authored in parallel)

- [X] T031 [P] [US3] Create `spekificity/skills/spek-prepare.md` — heading `# /spek.prepare`; imperative mood; no agent syntax; content from `wiki/workflow.md` "Preparation" section (sub-steps: lat.md code index, lat.md doc index, vault storage, context load, constitution check; exit criteria: indexes current, vault loaded, constitution present)
- [X] T032 [P] [US3] Create `spekificity/skills/spek-plan.md` — heading `# /spek.plan`; content from `wiki/workflow.md` "Plan" section (steps: /speckit-specify → user approval → /speckit-plan → user approval → /speckit-tasks → user approval; remediation loop; archive to `.spek/vault/`)
- [X] T033 [P] [US3] Create `spekificity/skills/spek-implement.md` — heading `# /spek.implement`; content from `wiki/workflow.md` "Implementation" section (steps: load vault context, run /speckit-implement, per-task checklist from Implementation Checklist; optional `--steps N` flag)
- [X] T034 [P] [US3] Create `spekificity/skills/spek-conclude.md` — heading `# /spek.conclude`; content from `wiki/workflow.md` "Conclude" section (steps: /speckit-analyze, /spek.lessons sub-step, vault archive, lat init state refresh, git commit; lessons template format)
- [X] T035 [P] [US3] Create `spekificity/skills/spek-lessons.md` — heading `# /spek.lessons`; content from `wiki/workflow.md` Conclude sub-step 2 and `wiki/architecture.md` supplementary skills section (steps: prompt retrospective, extract patterns/decisions, write to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`; callable standalone or auto-called by /spek.conclude)
- [X] T036 [P] [US3] Create `spekificity/skills/spek-context.md` — heading `# /spek.context`; content from `wiki/architecture.md` "/spek.context" section (steps: load vault decisions/patterns/lessons into session, read `.spek/memory/` workspace facts, populate session state for downstream commands)
- [X] T037 [P] [US3] Create `spekificity/skills/spek-map.md` — heading `# /spek.map`; content from `wiki/architecture.md` "/spek.map" section (steps: query lat.md for code references to spec topic, query vault for related decisions, generate dependency graph, highlight blockers and critical paths)

**Checkpoint**: US3 complete — all skill files authored and distribution logic tested

---

## Phase 6: User Story 4 — `spek init` Works End-to-End (Priority: P4)

**Goal**: `spek init` orchestrates P1–P3 modules in order; supports `--integration`, `--script`, `--no-git-hooks` flags and interactive prompts; idempotent re-run exits 0 with only `[SKIP]`; correct exit codes 0/1/2

**Independent Test**: `spek init --integration claude --script sh` in clean git repo; verify all artifacts from quickstart.md Scenario 1; re-run verifies Scenario 2 (idempotency)

- [X] T038 [US4] Implement `spekificity/cli.py` — `@click.group()` with `--version` (from `__version__`); `@cli.command() def init(path, integration, script, no_git_hooks)`: prompt for `integration` and `script` if not provided; instantiate `InitOptions`; call in order: `check_prerequisites()` → `install_lat()` + `run_lat_index()` → `install_obsidian()` + `scaffold_vault()` + `init_vault()` → `install_speckit()` + `run_specify_init()` + `write_spek_config()` → `write_mcp_config()` → `write_git_hook()` → `copy_skills()`; collect results into `InitResult`; error handling: exit-code-1 errors are fail-fast (halt immediately); Obsidian `needs_user_action` (exit code 2) skips vault sub-steps but continues lat.md, SpecKit, and skills-install before halting with `sys.exit(2)`; all steps use `print_status` from `utils`
- [X] T039 [US4] Write `tests/integration/test_init_flow.py` — use `click.testing.CliRunner` with `tmp_path` as project root; mock all subprocess calls (`npm install`, `lat init`, `obsidian`, `uv tool install`, `specify init`); (a) run `spek init --integration claude --script sh` — assert all artifacts exist (`.spek/vault/`, `.spek/memory/`, `.spek/lat/`, `.spek/config.yaml`, `.claude/commands/spek-prepare.md` and 6 others, `.mcp.json` with `lat` entry, `.specify/`, `.git/hooks/post-commit`); (b) re-run — assert all output lines contain `[SKIP]`, exit code 0; (c) run `spek init /tmp/other-dir --integration claude --script sh` with a separate `tmp_path` — assert artifacts land under `/tmp/other-dir`, not CWD (tests FR-025 non-default path)

**Checkpoint**: US4 complete — full end-to-end flow verified

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T040 [P] Run quickstart.md validation — execute Scenarios 1–7 from `specs/003-full-platform-impl/quickstart.md` manually; confirm all expected outcomes match; document any deviations
- [X] T041 [P] Verify pytest configuration — ensure all test subdirectories are discovered (`tests/unit/lat_md/`, `tests/unit/vault/`, `tests/unit/speckit/`, `tests/unit/skills_install/`, `tests/integration/`); add `__init__.py` files only if pytest config requires them; run full test suite and confirm green

---

## Phase 8: Gap Fixes (FR-002, FR-011, FR-020)

**Source**: Post-implementation review identified three FR violations. All independent; can run in parallel.

- [X] T042 [P] Fix `spekificity/prerequisites.py` — add version validation for Python ≥3.11 and Node.js ≥22; parse `python --version` / `node --version` output via regex; `sys.exit(1)` with descriptive message if version too low; `uv` and `git` remain PATH-presence-only checks; update `tests/unit/test_prerequisites.py` to cover version-too-low cases for Python and Node

- [X] T043 [P] Fix `spekificity/vault/install.py` — replace `_print_registration_instructions()` body with verbatim text from `wiki/setup.md` "Phase 1 halt — warning output" block (`⚠  Obsidian installed...` through `spek init will complete all remaining setup autonomously.`); update `tests/unit/vault/test_install.py` to assert the verbatim block appears in stderr on `needs_user_action` result

- [X] T044 [P] Rewrite all 7 skill files (`spekificity/skills/spek-*.md`) to use required H2 section structure in order: `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria`; content from existing files preserved and reorganized; steps use imperative mood; no new agent syntax introduced

---

## Phase 9: Gap Fixes (Analysis-Review — P6)

**Source**: Code correctness audit identified two runtime bugs. Both independent; can run in parallel.

- [X] T045 [P] Fix `spekificity/cli.py` — add `elif obsidian_result.status == "skipped"` guard (Linux path) before `else: init_vault()` so `init_vault` is never called when obsidian not available; fixes RuntimeError on Linux where `obsidian open-vault` is not in PATH
- [X] T046 [P] Fix `spekificity/lat_md/mcp_config.py` + `spekificity/skills_install/integrations.py` — add `flat_key: bool` field to `INTEGRATION_MCP_CONFIG` tuples; pass to `write_mcp_config`; when `flat_key=True` skip `split(".")` navigation and use literal key directly; set `flat_key=True` for `cline`; add test `test_cline_writes_flat_key` to `tests/unit/lat_md/test_mcp_config.py`

---

## Phase 10: Gap Fixes (Wiki-Compliance — P7)

**Source**: Wiki vs implementation audit identified five gaps. I1 and I2 HIGH; I3–I5 MEDIUM.

- [X] T047 [P] Fix `spekificity/speckit/init.py` — add `integration: str` param to `run_specify_init`; change command to `["specify", "init", "--integration", integration]`; update `spekificity/cli.py` call site to pass `integration`; update `tests/unit/speckit/test_init.py` to assert `--integration` flag present in mocked command
- [X] T048 [P] Fix `spekificity/speckit/install.py` — add `"--from", "git+https://github.com/github/spec-kit.git"` to install command; update `tests/unit/speckit/test_install.py` to assert full command including `--from` arg
- [X] T049 [P] Fix `spekificity/prerequisites.py` — after all tool PATH checks pass, run `git rev-parse --git-dir` via `subprocess.run`; if non-zero exit, print `[ERROR] Not in a git repository. Run: git init` and `sys.exit(1)`; add test in `tests/unit/test_prerequisites.py` for both valid and invalid git repo cases
- [X] T050 [P] Fix `spekificity/vault/init.py` — change `["obsidian", "open-vault", str(vault_path)]` to `["obsidian", "open-vault", f"path={vault_path}"]` (named arg per `wiki/setup.md`); update `tests/unit/vault/test_init.py` to assert named-arg form
- [X] T051 Fix `spekificity/vault/scaffold.py` and `spekificity/vault/init.py` — move initial file creation (`decisions.md`, `patterns.md`, `lessons/.keep`) out of `scaffold_vault` and into `init_vault`; in `init_vault` create files via `obsidian create` CLI calls (not filesystem writes); `scaffold_vault` creates dirs only; update `tests/unit/vault/test_scaffold.py` (dirs only, no file assertions) and `tests/unit/vault/test_init.py` (assert `obsidian create` called for each missing file); T051 depends on T050

---

## P8: Auto-Tagging & Auto-Wikilink Insertion (gap from decision.md)

**Source**: Gap audit — `decision.md` documents auto-tagging as active in `/spek.conclude`; no implementation existed.

- [X] T052 [US5] Implement `spekificity/vault/autolink.py` — `AutolinkResult` dataclass (`links_inserted: int`, `tags_added: list[str]`, `skipped: bool`); `_build_vault_index(vault_path: Path) -> dict[str, Path]` scans `.spek/vault/` recursively for `.md` files, keys are normalized stems (lowercase, hyphens/underscores → spaces, strip `.md`); `_extract_keywords(text: str) -> list[str]` strips markdown syntax via regex, tokenizes, removes hardcoded English stopwords, deduplicates; `_match_keywords(keywords, vault_index, threshold) -> list[tuple[str, Path]]` uses `difflib.SequenceMatcher(None, kw, key).ratio()` per (keyword, vault-key) pair, returns matches ≥ threshold; `_insert_wikilinks(text, matches) -> tuple[str, int]` replaces bare keyword occurrence (not already inside `[[...]]`) with `[[keyword]]`, returns `(updated_text, count)`; `_add_frontmatter_tags(text, tags) -> str` merges tags into YAML frontmatter block (create `---\ntags: [...]\n---\n` if absent, extend existing `tags:` list if present, no-op if `tags` empty); `process_lesson(lesson_path, vault_path, config) -> AutolinkResult` orchestrates all steps, skips with `[SKIP]` if `config["autolink"]["enabled"]` is False (default True), calls `print_status` for `[OK]`/`[SKIP]`; stdlib only (`re`, `difflib`, `pathlib`)
- [X] T053 [P] [US5] Write `tests/unit/vault/test_autolink.py` — test `_build_vault_index` returns normalized stem keys for all `.md` files in tmp vault; test `_extract_keywords` removes stopwords ("the", "and", etc.) and strips markdown headers/bullets; test `_match_keywords` returns match above threshold=0.8 for close keyword and skips below; test `_insert_wikilinks` wraps bare "decisions" → `[[decisions]]` but leaves existing `[[decisions]]` untouched; test `_insert_wikilinks` count return matches actual insertions; test `_add_frontmatter_tags` creates YAML block when absent; test `_add_frontmatter_tags` merges new tags into existing block without duplicates; test `process_lesson` returns `skipped=True` when `autolink.enabled=False`; test `process_lesson` idempotency (second call with already-linked text produces same count=0); use `tmp_path`
- [X] T054 [P] [US5] Update `spekificity/speckit/config.py` — add `autolink` block to YAML template string after `token_limits` section: `autolink:\n  enabled: true\n  threshold: 0.8\n  keyword_tags: {}`; update `tests/unit/speckit/test_config.py` to assert output YAML contains `autolink:`, `enabled: true`, and `threshold: 0.8` fields
- [X] T055 [P] [US5] Update `spekificity/skills/spek-lessons.md` — add Step 5 under `## Steps`: `Run autolink enrichment: call process_lesson() with the generated lesson path, .spek/vault/, and loaded config; inserts [[wikilinks]] for matched vault entries and adds generated tags to frontmatter`; add two exit criteria: `[[wikilinks]] inserted for all vault-matched keywords` and `tags generated from keyword_tags mapping`; keep all existing content
- [X] T056 [P] [US5] Update `spekificity/skills/spek-conclude.md` — in Step 2 (lessons sub-step) add parenthetical note: `(autolink enrichment runs automatically inside /spek.lessons — wikilinks and tags added to lesson file)`; keep all existing content

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user story phases
- **US1 (Phase 3)**: Depends on Phase 2 — no story dependencies
- **US2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1 after Phase 2
- **US3 (Phase 5)**: Depends on Phase 2 — can run in parallel with US1/US2 after Phase 2
- **US4 (Phase 6)**: Depends on US1 + US2 + US3 all complete
- **Polish (Phase 7)**: Depends on US4

### User Story Dependencies

- **US1 (P1)**: Independent after Foundational. No story deps.
- **US2 (P2)**: Independent after Foundational. No story deps. lat_md, vault, and speckit subgroups fully parallel with each other.
- **US3 (P3)**: Independent after Foundational. No story deps. All 7 skill files fully parallel. T028 depends on T027 only.
- **US4 (P4)**: Depends on all three prior stories. CLI is the integration layer.

### Within Each Story

- All tasks marked [P] can run in parallel (different files, no shared state)
- T028 (copy.py) depends on T027 (imports `get_skills_config`)
- T038 (cli.py) depends on T005–T037 (all modules it orchestrates)
- T039 (integration test) depends on T038

---

## Parallel Opportunities

```bash
# After Phase 2 (T003-T004), three story phases can launch in parallel:

# US1 parallel group (T005-T006):
T005: spekificity/prerequisites.py
T006: tests/unit/test_prerequisites.py

# US2 lat_md parallel group (T007-T014):
T007: spekificity/lat_md/install.py    T011: tests/unit/lat_md/test_install.py
T008: spekificity/lat_md/index.py      T012: tests/unit/lat_md/test_index.py
T009: spekificity/lat_md/mcp_config.py T013: tests/unit/lat_md/test_mcp_config.py
T010: spekificity/lat_md/git_hook.py   T014: tests/unit/lat_md/test_git_hook.py

# US2 vault parallel group (T015-T020):
T015: spekificity/vault/install.py     T018: tests/unit/vault/test_install.py
T016: spekificity/vault/scaffold.py    T019: tests/unit/vault/test_scaffold.py
T017: spekificity/vault/init.py        T020: tests/unit/vault/test_init.py

# US2 speckit parallel group (T021-T026):
T021: spekificity/speckit/install.py   T024: tests/unit/speckit/test_install.py
T022: spekificity/speckit/init.py      T025: tests/unit/speckit/test_init.py
T023: spekificity/speckit/config.py    T026: tests/unit/speckit/test_config.py

# US3 parallel group (T027-T037):
T027: spekificity/skills_install/integrations.py
T029: tests/unit/skills_install/test_integrations.py
T030: tests/unit/skills_install/test_copy.py
T031: spekificity/skills/spek-prepare.md
T032: spekificity/skills/spek-plan.md
T033: spekificity/skills/spek-implement.md
T034: spekificity/skills/spek-conclude.md
T035: spekificity/skills/spek-lessons.md
T036: spekificity/skills/spek-context.md
T037: spekificity/skills/spek-map.md
# T028 after T027
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004)
3. Complete Phase 3: US1 (T005-T006)
4. **STOP and VALIDATE**: `uv tool install`, `spek --version`, prerequisite error test
5. Ship if ready

### Incremental Delivery

1. Setup + Foundational → foundation ready
2. + US1 → package installable, prereqs checked (P1 deliverable)
3. + US2 → integrations install and configure (P2 deliverable)
4. + US3 → skill files bundled and distributed (P3 deliverable)
5. + US4 → full `spek init` end-to-end (P4 deliverable — ship!)

---

## Notes

- [P] = different files, no shared-state dependency — safe to execute concurrently
- [US1/US2/US3/US4] maps each task to its user story for traceability
- Tests are deliverables per plan.md; no TDD required but tests cover idempotency and mock subprocess
- `utils.py` (T003) is the only cross-story shared module — complete before any story
- `cli.py` (T038) is intentionally thin: reads flags/prompts, calls modules, handles exit codes — no business logic
- Never use `shell=True` in subprocess calls (injection risk per research.md Decision 3)
- All submodule `__init__.py` files expose the primary public function for import convenience (e.g., `from spekificity.lat_md import install_lat`); empty `__init__.py` is acceptable if no public API is needed
- Skill files: no frontmatter, no `@workspace`/`#file:`/`[[wikilink]]` syntax (FR-019)
- MCP config writes: always parse → merge → write; never clobber existing entries (Decision 6)
- Obsidian two-phase halt: exit code 2 (not 1) signals "user action required" to scripts/CI (Decision 8)
