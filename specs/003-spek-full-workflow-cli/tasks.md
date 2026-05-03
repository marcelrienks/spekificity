# tasks: spek — full workflow cli

**input**: `specs/003-spek-full-workflow-cli/`
**prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

## format: `[id] [p?] [story?] description — file path`

- **[p]**: can run in parallel (different files, no unmet dependencies)
- **[us1–us6]**: user story this task belongs to
- tests not included (not requested in spec)

---

## phase 1: setup

**purpose**: create project directory skeleton before any implementation begins

- [x] t001 create directory structure: `bin/`, `.spekificity/bin/`, `.spekificity/skills/` per plan.md runtime structure

---

## phase 2: foundational — cli entry point and shared utilities

**purpose**: core scaffolding that every sub-command depends on. must complete before any user story work begins.

⚠️ **critical**: no sub-command scripts can be implemented until `bin/spek` and `_lib.sh` exist

- [x] t002 create `bin/spek` bash entry point — parse `$1` sub-command and route to `.spekificity/bin/<cmd>.sh`, include `--version` and `--help` output, make executable (`chmod +x`)
- [x] t003 [p] create `.spekificity/bin/_lib.sh` — shared bash utilities: `print_spek()`, `print_speckit()`, `print_graphify()`, `read_config()`, `write_config()`, `check_initialized()`, `atomic_write_json()` (write to .tmp then mv)
- [x] t004 [p] create `.spekificity/version.txt` with initial platform version string `0.3.0`

**checkpoint**: foundation ready — sub-command scripts can now be implemented

---

## phase 3: user story 1 — spek setup (priority: p1) 🎯

**goal**: developer on a clean machine can run `spek setup` to detect and install all required tools, skip existing ones, and receive manual instructions for non-auto-installable tools

**independent test**: run `spek setup --dry-run` on a machine with some tools present; verify all tools are checked, status lines printed with `[spek]` prefix, required/optional classification displayed, exit code 0 if all required tools present

- [x] t005 [us1] define tool prerequisite array in `.spekificity/bin/setup.sh` — name, required/optional flag, detection command, install command, manual_url for each of: python3, uv, git, specify, graphify, gh, obsidian (per data-model.md ToolPrerequisite schema)
- [x] t006 [us1] implement tool detection loop in `.spekificity/bin/setup.sh` — iterate array, run detection command, capture version string, print `[spek] ✓ <tool> <version>` or `[spek] ✗ <tool> — not found`
- [x] t007 [us1] implement auto-install execution in `.spekificity/bin/setup.sh` — run install command for missing auto-installable tools, capture output with `[speckit]`/`[graphify]` prefix, verify installation succeeded
- [x] t008 [us1] implement obsidian manual-only instructions block in `.spekificity/bin/setup.sh` — print step-by-step download instructions, mark as `pending` in config
- [x] t009 [us1] implement `config.json` tool status write after setup completes in `.spekificity/bin/setup.sh` — call `write_config()` from `_lib.sh`, set `tools.<name>.installed`, `tools.<name>.version` per SpekConfig schema in data-model.md
- [x] t010 [us1] implement `--dry-run` flag in `.spekificity/bin/setup.sh` — detect tools and report status, skip all install commands, exit 0
- [x] t011 [us1] implement `--skip-optional` flag and idempotency check in `.spekificity/bin/setup.sh` — skip optional tools when flag set; skip any tool where detection command succeeds (already installed)

**checkpoint**: `spek setup` fully functional and idempotent

---

## phase 4: user story 2 — spek init (priority: p1)

**goal**: running `spek init` in a project produces a complete `.spekificity/` with all tools initialised, all skills installed, and `skill-index.md` listing all discoverable commands

**independent test**: run `spek init` in an empty project; verify `skill-index.md` lists 6 `/spek.*` skills and all speckit skills; `spek status` reports all tools active; `spek init` can be run a second time without error

- [x] t012 [us2] create `.spekificity/bin/init.sh` scaffold — check prerequisites via `check_initialized()`, print `[spek]` prefixed progress lines, sequence: speckit → graphify → vault dirs → skills → index write
- [x] t013 [us2] implement `specify init` call in `.spekificity/bin/init.sh` — run `specify init`, prefix output with `[speckit]`, check exit code, print `[spek] speckit initialised ✓`
- [x] t014 [us2] implement vault directory creation in `.spekificity/bin/init.sh` — create `vault/`, `vault/context/`, `vault/graph/`, `vault/lessons/` with `mkdir -p`, skip if already present
- [x] t015 [us2] implement skill installation loop in `.spekificity/bin/init.sh` — copy each source skill file from `skills/*/skill.md` and new `.spekificity/skills/spek.*.md` to `.spekificity/skills/`, skip if destination is newer
- [x] t016 [us2] implement `skill-index.md` auto-generation in `.spekificity/bin/init.sh` — scan `.spekificity/skills/` for `spek.*` skills, scan `.github/agents/` for `speckit.*` skills, write formatted markdown table with command/file/description/status columns per data-model.md SkillIndex format
- [x] t017 [us2] implement idempotency guards for all init steps in `.spekificity/bin/init.sh` — check `config.json` for `initialized_at`; re-run if `--force` passed, otherwise verify and skip completed steps
- [x] t018 [p] [us2] create `.spekificity/bin/status.sh` — read `config.json` via `read_config()`, print platform version, `initialized_at`, tool versions and ✓/✗/⚠ status, skill count, graph state (call `compute_graph_state()`), active workflow from `workflow-state.json`
- [x] t019 [p] [us2] create `.spekificity/bin/update.sh` — check current `version.txt` against source, copy updated skills from source to `.spekificity/skills/`, re-run skill-index.md generation, print what was updated

**checkpoint**: `spek init` and `spek status` fully functional; all 6 spek.* skills discoverable via `skill-index.md`

---

## phase 5: user story 3 — spek prepare (priority: p2)

**goal**: `spek prepare` loads vault context, checks graph currency, and refreshes graph if stale — leaving the ai session primed with full codebase context before feature work

**independent test**: run `spek prepare` on project with stale graph (git commit after last graph build); verify graph is rebuilt, vault context loaded, lessons surfaced, all within 60 seconds

- [x] t020 [us3] add `compute_graph_state()` to `.spekificity/bin/_lib.sh` — compare `git log -1 --format=%ct HEAD` vs `stat` mtime on `vault/graph/index.md`, handle absent/stale/fresh tri-state, cross-platform `stat` (Darwin vs Linux)
- [x] t021 [us3] create `.spekificity/bin/prepare.sh` — call `compute_graph_state()`, trigger `graphify` if stale/absent, invoke `/spek.prepare` skill, support `--force-refresh` flag (skip freshness check)
- [x] t022 [us3] create `.spekificity/skills/spek.prepare.md` — ai skill: first read `VAULT_PATH` from `.spekificity/config.json` via `read_config()` to construct all vault file paths; then read `${VAULT_PATH}/context/decisions.md` + `${VAULT_PATH}/context/patterns.md`, list most recent 3 files from `${VAULT_PATH}/lessons/` and summarise, confirm readiness message, log `[spek] preparation complete`
- [x] t023 [p] [us3] update `skills/context-load/skill.md` — add step to check `workflow-state.json` for active feature context, read vault path from `config.json` rather than hardcoded `vault/`
- [x] t024 [p] [us3] update `skills/map-codebase/skill.md` — add incremental vs full-rebuild mode (use `--incremental` flag when graph exists), add `[graphify]` output prefix instructions, add staleness state parameter as input

**checkpoint**: `spek prepare` functional; vault context loads correctly; graph rebuilt when stale

---

## phase 6: user story 4 — spek automate (priority: p1)

**goal**: `spek automate "<description>"` drives the full speckit lifecycle (spec → plan → tasks → analyse → remediation → implement → postflight) autonomously, surfaces questions interactively, saves state after each step, and creates a PR on completion

**independent test**: run `spek automate "add a simple counter feature"` on initialised+prepared project; verify feature branch created, each step's output file appears in sequence, all `tasks.md` tasks end as `[x]`, PR opened (or terminal description printed)

- [x] t025 [us4] create `.spekificity/bin/automate.sh` — parse feature description arg, check git working tree clean (`git status --porcelain`), generate branch name (`NNN-kebab-case`): scan `specs/` for highest existing `NNN-` prefix and increment by 1 (zero-padded to 3 digits, start at `001` if no specs exist), convert description to kebab-case; error with exit code 2 if uncommitted changes
- [x] t026 [us4] implement feature branch creation in `.spekificity/bin/automate.sh` — `git checkout -b <branch>`, detect existing branch conflict (ask reuse/suffix), write `feature_branch` and `feature_dir` to initial `workflow-state.json`
- [x] t027 [us4] implement initial `workflow-state.json` write on fresh start in `.spekificity/bin/automate.sh` — use `atomic_write_json()` from `_lib.sh`, set schema per data-model.md WorkflowState, `status: "in-progress"`, `next_step: "spec"`, `completed_steps: ["preflight"]`
- [x] t028 [us4] implement `--resume` flag and completed-workflow guard in `.spekificity/bin/automate.sh` — (a) on fresh run: if `workflow-state.json` already exists with `status: "complete"`, print completion summary and exit 0 (idempotency guard for SC-007); (b) on `--resume`: read `workflow-state.json`, validate `status` is `in-progress` or `halted` (print error and exit if `complete`), print resume point, pass `next_step` and `completed_steps` to skill invocation
- [x] t029 [us4] implement PR creation in `.spekificity/bin/automate.sh` — check `command -v gh && gh auth status`, run `gh pr create --title "..." --body "$(head -30 specs/.../spec.md)" --base main`, set `postflight.pr_created: true` and `postflight.pr_url` in `workflow-state.json`
- [x] t030 [us4] implement PR terminal fallback in `.spekificity/bin/automate.sh` — if `gh` unavailable or unauthenticated, print formatted PR title, body, and `gh auth login` instructions; set `postflight.pr_created: false`
- [x] t031 [us4] create `.spekificity/skills/spek.automate.md` — skill header section: inputs (feature_description, feature_branch, feature_dir, workflow_state), step sequence diagram, output conventions
- [x] t032 [us4] add spec step to `.spekificity/skills/spek.automate.md` — read `VAULT_PATH` from `.spekificity/config.json` via `read_config()` at skill start; read `${VAULT_PATH}/context/decisions.md` + `${VAULT_PATH}/context/patterns.md`, find relevant graph nodes from `${VAULT_PATH}/graph/` matching feature keywords, inject as context prefix, invoke `/speckit.specify`, completion check: `<feature_dir>/spec.md` exists with `## requirements`
- [x] t033 [us4] add plan step to `.spekificity/skills/spek.automate.md` — read `VAULT_PATH` from `.spekificity/config.json` via `read_config()` at skill start; read `${VAULT_PATH}/context/decisions.md` + impacted graph nodes from `${VAULT_PATH}/graph/` (matching spec entities), inject as context prefix, invoke `/speckit.plan`, completion check: `<feature_dir>/plan.md` exists with `## summary`
- [x] t034 [us4] add tasks + analyse + remediation steps to `.spekificity/skills/spek.automate.md` — tasks: invoke `/speckit.tasks`, check `tasks.md` has `- [ ]` items; analyse: invoke `/speckit.analyze`; remediation: surface items with `[spek]` prefix, approval gate, high-risk threshold (>30% tasks or breaking changes)
- [x] t035 [us4] add implement step to `.spekificity/skills/spek.automate.md` — invoke `/speckit.implement`, after each invocation read `tasks.md` and count `- [ ]` tasks, if any remain re-invoke with "continue from last incomplete task", max 10 retries, halt with exit code 3 if limit reached
- [x] t036 [us4] add QA interface section to `.spekificity/skills/spek.automate.md` — `[spek] ❓` prompt format, instructions to write question to `workflow-state.json` pending_questions with `answer: null`, collect developer answer, write answer, re-invoke speckit step with answer as context
- [x] t037 [us4] add `workflow-state.json` update instructions to `.spekificity/skills/spek.automate.md` — after each step: add step to `completed_steps`, set `next_step` to following step, use `atomic_write_json()` pattern, set `status: "complete"` only after postflight
- [x] t038 [us4] add resume logic to `.spekificity/skills/spek.automate.md` — instructions to read `next_step` from `workflow-state.json` on resume, skip all steps listed in `completed_steps`, validate `status` before starting

**checkpoint**: `spek automate` drives full lifecycle; resume works after interruption; PR created or terminal fallback printed

---

## phase 7: user story 5 — spek post (priority: p2)

**goal**: `spek post` after a completed feature writes a structured lessons entry to `vault/lessons/` and runs incremental graph refresh within 3 minutes

**independent test**: complete any feature, run `spek post`; verify `vault/lessons/YYYY-MM-DD-<feature>.md` created with correct format, graph node count increases after refresh, both within 3 minutes

- [x] t039 [us5] create `.spekificity/skills/spek.post.md` — ai skill: prompt developer for key decisions + patterns, invoke `/spek.lessons-learnt` with `feature_branch` and `feature_dir` context, invoke `/spek.map-codebase` (incremental mode), write completion summary
- [x] t040 [us5] create `.spekificity/bin/post.sh` — check init, support `--no-lessons` and `--no-graph` flags, print `[spek]` prefixed progress, invoke `/spek.post` skill
- [x] t041 [p] [us5] update `skills/lessons-learnt/skill.md` — add vault write format instructions (`vault/lessons/YYYY-MM-DD-<feature>.md` per vault-integration-contract.md w-1), add append-on-collision behaviour, add developer prompt for decisions/patterns
- [x] t042 [us5] add postflight section to `.spekificity/skills/spek.automate.md` — first update `status: draft` → `status: complete` in `<feature_dir>/spec.md` front-matter; then invoke `/spek.post`, set `postflight.lessons_written: true`, `postflight.graph_refreshed: true` in `workflow-state.json` after each post sub-task; invoke PR creation last

**checkpoint**: `spek post` functional standalone and as automate postflight; lessons in vault after run

---

## phase 8: polish and cross-cutting (us6)

**purpose**: vault integration validation, docs update, skill-index source template

- [x] t043 [p] update `docs/guide.md` — add `spek` cli section with setup → init → prepare → automate → post workflow table, link to `specs/003-spek-full-workflow-cli/quickstart.md`
- [x] t044 [p] update `docs/readme.md` — add `spek` cli overview paragraph in features section, add quickstart reference link
- [x] t045 [p] update `docs/architecture.md` — add `.spekificity/bin/` component description, update directory tree to include `bin/spek` and `.spekificity/bin/*.sh`
- [x] t046 [p] create `specs/003-spek-full-workflow-cli/acceptance-tests/` with manual verification steps for: SC-001 (setup + init ≤15 min on clean machine), SC-002 (≤5 interactions during automate), SC-004 (spec/plan references ≥2 vault components), SC-005 (spek post ≤3 min), SC-006 (spek prepare ≤60 sec with current graph) — follow format from `specs/002-spek-platform-lifecycle/acceptance-tests/`

---

## dependencies

```text
t001 (dirs)
  └─ t002 (bin/spek) → all phase 3–8 tasks
  └─ t003 (_lib.sh) → t005–t011 (setup.sh), t012–t019 (init.sh), t020–t021 (prepare.sh), t025–t030 (automate.sh), t040 (post.sh)
  └─ t004 (version.txt) → t018 (status.sh reads version)

phase 3 (US1 — setup):
  t005 → t006 → t007 → t008 → t009 (sequential, same file)
  t009 → t010 (dry-run adds conditional branch)
  t009 → t011 (skip-optional + idempotency)

phase 4 (US2 — init):
  t012 (scaffold) → t013 → t014 → t015 → t016 → t017 (sequential, same file)
  t012 + t003 → t018 [p] (status.sh, separate file)
  t016 → t019 [p] (update.sh reuses index generation, separate file)

phase 5 (US3 — prepare):
  t003 → t020 (adds to _lib.sh) → t021 (prepare.sh calls compute_graph_state)
  t022 (prepare skill, independent file)
  t023, t024 [p] (separate skill files, independent of each other)

phase 6 (US4 — automate):
  t003 + t020 (atomic write + compute_graph_state) → t025 → t026 → t027 → t028 (sequential, automate.sh)
  t027 → t029 → t030 (PR section, same file)
  t031 → t032 → t033 → t034 → t035 (sequential sections of spek.automate.md)
  t036, t037, t038 add independent sections to spek.automate.md (after t031 scaffold)
  t042 adds postflight section to spek.automate.md (after t031)

phase 7 (US5 — post):
  t039 (spek.post.md skill, independent)
  t039 → t040 (post.sh invokes skill)
  t041 [p] (lessons-learnt skill update, independent file)
  t031 → t042 (adds to spek.automate.md, after scaffold created; includes spec status update)

phase 8 (US6 — polish):
  t043 + t044 + t045 + t046 [p] (four independent files/dirs)
```

## parallel execution examples

**within each story, independent pairs**:
- t018 + t019 (status.sh, update.sh — different files, both after init.sh scaffold)
- t023 + t024 (two separate skill file updates)
- t003 + t004 (different files, both foundational)
- t039 + t041 (different skill files, same story)
- t043 + t044 + t045 (three separate doc files)

**across stories** (after their story phases complete):
- phase 5 (US3) can begin as soon as phase 4 completes
- phase 7 (US5 — post shell + skill) can begin once phase 2 (foundational) is complete — it is independent of phases 5 and 6

---

## implementation strategy

### mvp scope (p1 stories only — phases 1–4, 6)

deliver phases 1, 2, 3, 4, 6 first:
- `spek setup` + `spek init` + `spek status` + `spek automate` (US1, US2, US4)
- this gives the complete automated feature lifecycle

### v1 completion (all stories — add phases 5, 7, 8)

add prepare + post + docs:
- `spek prepare` + `spek post` (US3, US5, US6)
- polish and cross-cutting vault integration

### task count summary

| phase | story | tasks | parallel opportunities |
|-------|-------|-------|------------------------|
| 1 setup | — | 1 | — |
| 2 foundational | — | 3 | t003 + t004 |
| 3 spek setup | us1 | 7 | — |
| 4 spek init | us2 | 8 | t018 + t019 |
| 5 spek prepare | us3 | 5 | t023 + t024 |
| 6 spek automate | us4 | 14 | t036 + t037 + t038 after t031 |
| 7 spek post | us5 | 4 | t039 + t041 |
| 8 polish | us6 | 4 | t043 + t044 + t045 + t046 |
| **total** | | **46** | |
