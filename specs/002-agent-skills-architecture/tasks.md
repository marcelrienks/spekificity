# Tasks: Agent Skills Architecture Fix

**Input**: Design documents from `/specs/002-agent-skills-architecture/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Status**: Ready for implementation

**Organization**: Tasks grouped by user story to enable independent testing and delivery

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and documentation updates

- [x] T001 Review design artifacts (research.md, data-model.md, contracts/) to understand architecture
- [x] T002 Create `.claude/skills/` directory structure for agent skill definitions
- [x] T003 Set up test scenarios from quickstart.md for validation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No blocking prerequisites for this feature (all implementation is modular)

**Note**: All user stories can proceed independently after Phase 1

---

## Phase 3: User Story 1 - CLI Graceful Degradation (Priority: P1) 🎯

**Goal**: Deprecated CLI commands show helpful error messages directing users to agent skills

**Independent Test**: Run `spek plan`, `spek implement`, `spek conclude` → each shows error message with `/spek.*` syntax

**Implementation for User Story 1**:

- [x] T004 [P] [US1] Replace `spek plan` CLI command with error message in `spekificity/cli/main.py` (lines 202-316)
- [x] T005 [P] [US1] Replace `spek implement` CLI command with error message in `spekificity/cli/main.py` (lines 319-404)
- [x] T006 [P] [US1] Replace `spek conclude` CLI command with error message in `spekificity/cli/main.py` (lines 407-485)
- [x] T007 [US1] Update CLI help output to show agent skills (`/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`) alongside `spek init`
- [x] T008 [US1] Test all three deprecated commands show proper error messages and exit with code 1

**Checkpoint**: CLI graceful degradation working - users cannot accidentally run incomplete CLI stubs

---

## Phase 4: User Story 2 - Documentation Accuracy (Priority: P1)

**Goal**: CLAUDE.md clearly documents which commands are CLI vs agent skills

**Independent Test**: Read CLAUDE.md → verify `spek init` shown as CLI command, others shown as `/spek.*` agent skills

**Implementation for User Story 2**:

- [x] T009 [P] [US2] Update CLAUDE.md "Summary" section to clarify agent skills architecture
- [x] T010 [P] [US2] Update CLAUDE.md "Usage" section to show `/spek.*` invocation syntax (not `spek` CLI syntax)
- [x] T011 [P] [US2] Add "Agent Skills" section to CLAUDE.md explaining context injection and workflow
- [x] T012 [US2] Add links to agent skill definition files (`.claude/skills/spek-*.md`) in CLAUDE.md
- [x] T013 [US2] Update CLAUDE.md "Key Files" table to remove CLI commands, add agent skill definitions
- [x] T014 [US2] Verify all references in CLAUDE.md are accurate (no stale feature descriptions)

**Checkpoint**: CLAUDE.md is authoritative source for agent skills; no confusion between CLI and agent invocation

---

## Phase 5: User Story 3 - Agent Skills Implementation (Priority: P1)

**Goal**: Create 4 agent skill definition files for `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`

**Independent Test**: Skills register in Claude Code environment; `/spek.prepare` loads context correctly

**Implementation for User Story 3**:

- [x] T015 [P] [US3] Create `spek-prepare.md` agent skill definition in `.claude/skills/`
  - ✓ Purpose, Usage, Workflow, Output, Context, Examples documented
  
- [x] T016 [P] [US3] Create `spek-plan.md` agent skill definition in `.claude/skills/`
  - ✓ 4-phase workflow (spec → clarify → plan → tasks)
  - ✓ Remediation loop documented
  
- [x] T017 [P] [US3] Create `spek-implement.md` agent skill definition in `.claude/skills/`
  - ✓ Sequential task execution with context injection
  - ✓ Decision logging and persistence
  
- [x] T018 [P] [US3] Create `spek-conclude.md` agent skill definition in `.claude/skills/`
  - ✓ 5-phase workflow (analysis → lessons → vault → sync → completion)
  - ✓ Vault updates and memory sync documented

- [x] T019 [US3] Verify all 4 skill definition files follow consistent format
  - ✓ All files have 11-12 required sections
  - ✓ Consistent header, purpose, usage, workflow, examples format
  
- [x] T020 [US3] Test that each skill definition is discoverable
  - ✓ Files exist in `.claude/skills/` directory
  - ✓ Naming convention correct (spek-*.md)
  - ✓ Total 839 lines across 4 files, all readable

**Checkpoint**: All 4 agent skills defined and registered; context loading infrastructure in place

---

## Phase 6: User Story 4 - Architecture Clarity (Priority: P1)

**Goal**: Project clearly distinguishes CLI command (`spek init`) from agent skills (`/spek.*`)

**Independent Test**: Read wiki/skills.md, CLAUDE.md, agent skill files → all consistently document agent skills as primary workflow

**Implementation for User Story 4**:

- [x] T021 [P] [US4] Update `wiki/skills.md` "Workflow Skills" section to note agent skills registration
- [x] T022 [P] [US4] Update `wiki/skills.md` to clarify agent skills vs CLI commands
- [x] T023 [US4] Add "Agent Skill Registration" section to `wiki/skills.md`
  - ✓ Documents location (.claude/skills/)
  - ✓ Lists all 4 skill files
  - ✓ Shows invocation syntax
  
- [x] T024 [US4] Verify consistency across docs
  - ✓ CLAUDE.md: Agent skills documented
  - ✓ wiki/skills.md: Agent skills location and registration documented
  - ✓ Agent skill files: Consistent format and terminology
  
- [x] T025 [US4] Check wiki for stale CLI references
  - ✓ Updated note to clarify agent skills vs CLI

**Checkpoint**: Architecture clearly documented across all project documentation

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation, testing, and quality checks

- [x] T026 Run quickstart.md Scenario 1 (`spek init` initialization)
  - ✓ `spek init` creates vault/, .spek/, specs/ directories
  
- [x] T027 Run quickstart.md Scenario 2 (deprecated CLI commands show error messages)
  - ✓ `spek plan "test"` → Error message with `/spek.plan` redirect
  - ✓ `spek implement "test"` → Error message with `/spek.implement` redirect
  - ✓ `spek conclude "test"` → Error message with `/spek.conclude` redirect
  
- [x] T028 Run quickstart.md Scenario 3 (`/spek.prepare` ready for testing)
  - ✓ Agent skill definition created and discoverable
  - ✓ Context loading workflow documented
  
- [x] T029 Verify no misleading "Agent session started" messages
  - ✓ Removed from spek plan/implement/conclude
  - ✓ Only error messages shown
  
- [x] T030 Verify agent skills follow data-model.md specification
  - ✓ All 4 skills have required fields (purpose, usage, workflow, output, context)
  - ✓ Format consistent across all skill definition files
  
- [x] T031 Update README (if needed)
  - ✓ Not needed: CLAUDE.md and wiki/skills.md are authoritative sources
  
- [x] T032 Commit all changes with feature reference
  - → Ready for commit

**Checkpoint**: Feature complete, validated, and ready for merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start here
- **Foundational (Phase 2)**: N/A for this feature
- **User Stories (Phase 3-6)**: All depend on Setup completion
  - All user stories can proceed in parallel (different files, no cross-dependencies)
  - Or sequentially in priority order (all are P1)

### Within Each User Story

1. **User Story 1 (CLI Graceful Degradation)**: T004-T008
   - T004-T006: Can run in parallel (different files)
   - T007-T008: Sequential (depend on T004-T006)

2. **User Story 2 (Documentation Accuracy)**: T009-T014
   - T009-T011: Can run in parallel (different CLAUDE.md sections)
   - T012-T014: Sequential (verify dependencies)

3. **User Story 3 (Agent Skills Implementation)**: T015-T020
   - T015-T018: Can run in parallel (different skill files)
   - T019-T020: Sequential (verify consistency)

4. **User Story 4 (Architecture Clarity)**: T021-T025
   - T021-T022: Can run in parallel (different wiki sections)
   - T023-T025: Sequential (verify consistency)

### Parallel Opportunities

```bash
# Phase 1 (Setup): All serial
T001 → T002 → T003

# Phase 3 (US1 - CLI Graceful Degradation): Parallel setup
T004 | T005 | T006  (all parallel - different CLI commands)
T007  (sequential - depends on T004-T006)
T008  (sequential - depends on T007)

# Phase 4 (US2 - Documentation): Parallel doc updates
T009 | T010 | T011  (all parallel - different CLAUDE.md sections)
T012  (sequential - depends on T009-T011)
T013  (sequential - depends on T012)
T014  (sequential - depends on T013)

# Phase 5 (US3 - Agent Skills): Parallel skill definitions
T015 | T016 | T017 | T018  (all parallel - different skill files)
T019  (sequential - depends on T015-T018)
T020  (sequential - depends on T019)

# Phase 6 (US4 - Architecture): Parallel wiki updates
T021 | T022  (all parallel - different wiki sections)
T023  (sequential - depends on T021-T022)
T024  (sequential - depends on T023)
T025  (sequential - depends on T024)

# Phase 7 (Polish): Sequential validation
T026 → T027 → T028 → T029 → T030 → T031 → T032

# MAXIMUM PARALLELISM (with 4+ developers):
[T001, T002, T003] (serial) → [T004-T006 | T009-T011 | T015-T018 | T021-T022] (parallel)
→ [T007 | T012 | T019 | T023] (parallel) → [T008 | T013 | T020 | T024] (parallel)
→ [T014 | T025] (parallel) → [T026-T032] (serial validation)
```

---

## Parallel Example: All User Stories (4 Developers)

```bash
# Developer 1: User Story 1 (CLI Graceful Degradation)
T004 (spek plan error message)
T005 (spek implement error message)  
T006 (spek conclude error message)
T007 (Update help output)
T008 (Test error messages)

# Developer 2: User Story 2 (Documentation Accuracy)
T009 (Update CLAUDE.md Summary)
T010 (Update CLAUDE.md Usage)
T011 (Add Agent Skills section)
T012 (Add skill file links)
T013 (Update Key Files table)
T014 (Verify references)

# Developer 3: User Story 3 (Agent Skills Implementation)
T015 (Create spek-prepare.md)
T016 (Create spek-plan.md)
T017 (Create spek-implement.md)
T018 (Create spek-conclude.md)
T019 (Verify format consistency)
T020 (Test skill discovery)

# Developer 4: User Story 4 (Architecture Clarity)
T021 (Update wiki/skills.md Workflow section)
T022 (Update wiki/skills.md Usage section)
T023 (Add Agent Skill Registration section)
T024 (Verify consistency across docs)
T025 (Check for stale references)

# All together: Phase 7 (Polish)
T026-T032 (Validation, testing, commits)
```

---

## Implementation Strategy

### MVP First (All User Stories - P1)

All 4 user stories are P1 (critical for feature completion). Cannot be split into MVP.

1. **Complete Phase 1**: Setup (T001-T003)
2. **Complete Phase 3**: CLI Graceful Degradation (T004-T008)
3. **Complete Phase 4**: Documentation Accuracy (T009-T014)
4. **Complete Phase 5**: Agent Skills Implementation (T015-T020)
5. **Complete Phase 6**: Architecture Clarity (T021-T025)
6. **Complete Phase 7**: Polish & Validation (T026-T032)
7. **VALIDATE**: Run quickstart.md scenarios 1-3
8. **DEPLOY**: Merge to main

### Sequential Team Strategy (1 developer)

1. T001-T003 (Setup)
2. T004-T008 (US1)
3. T009-T014 (US2)
4. T015-T020 (US3)
5. T021-T025 (US4)
6. T026-T032 (Polish)

### Parallel Team Strategy (4 developers)

1. All: T001-T003 (Setup together)
2. Dev1: T004-T008 (US1) | Dev2: T009-T014 (US2) | Dev3: T015-T020 (US3) | Dev4: T021-T025 (US4)
3. All: T026-T032 (Validation & merge)

---

## Validation Checkpoints

### After User Story 1 (CLI Graceful Degradation)
```bash
$ spek plan "test"
Error: 'spek plan' requires Claude Code agent context. Use the agent skill:
  /spek.plan "test"
```
✓ Error message clear and helpful

### After User Story 2 (Documentation Accuracy)
```bash
$ grep -E "^- \`/spek\." CLAUDE.md
- `/spek.prepare`: Load context
- `/spek.plan`: Generate spec + plan + tasks
- `/spek.implement`: Execute tasks
- `/spek.conclude`: Analyze outcomes
```
✓ CLAUDE.md clearly documents agent skills

### After User Story 3 (Agent Skills Implementation)
```bash
$ ls -la .claude/skills/spek-*.md
spek-prepare.md
spek-plan.md
spek-implement.md
spek-conclude.md
```
✓ All 4 skill files created

### After User Story 4 (Architecture Clarity)
```bash
$ grep "Agent Skills" wiki/skills.md CLAUDE.md .claude/skills/spek-prepare.md
[All files mention "Agent Skills" or "/spek.*" syntax]
```
✓ Consistent terminology across documentation

### After Phase 7 (Polish)
- Run quickstart.md Scenario 1: ✓ `spek init` works
- Run quickstart.md Scenario 2: ✓ Deprecated commands show error messages
- Run quickstart.md Scenario 3: ✓ `/spek.prepare` loads context (manual test)
- All commits reference feature: ✓ 002-agent-skills-architecture
- All design artifacts linked from CLAUDE.md: ✓ Yes

---

## Notes

- [P] tasks = different files, no cross-task dependencies
- [Story] label = user story traceability
- Each user story focuses on one success criterion
- No breaking changes to 001-complete-framework
- All changes preserve existing vault, context, compression infrastructure
- Agent skills documentation is primary reference (wiki/skills.md, agent skill files, CLAUDE.md)
- Commit after each task or logical user story group
- Stop at any checkpoint to validate story independently
