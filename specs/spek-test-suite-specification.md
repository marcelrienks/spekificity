# Spekificity Test Suite & Validation Strategy

**Status:** COMPLETE  
**Date:** 2026-05-20  
**Coverage Target:** 80% (good baseline)  
**Test Fixtures:** Small synthetic project (faster, controlled)  
**Mocking Strategy:** Full mocks for unit + integration (isolated, fast)  
**CI/CD:** GitHub Actions on PR + local pre-commit hooks  
**Framework:** pytest (Python primary), jest (JavaScript if CLI tools needed)

---

## 1. Test Architecture & Layers

### 1.1 Three-Layer Test Pyramid

```
     E2E Tests (5 scenarios)
        10% of tests
    
  Integration Tests (15 scenarios)
      30% of tests
    
   Unit Tests (40+ scenarios)
      60% of tests
```

### 1.2 Test Organization by Component

```
tests/
├── unit/                          # 60% of tests, fastest, fully mocked
│   ├── test_enrichment_layer.py
│   ├── test_memory_layer.py
│   ├── test_feature_state.py
│   ├── test_decorator_wrapper.py
│   ├── test_context_injection.py
│   └── test_compression.py
│
├── integration/                    # 30% of tests, medium speed, mocked externals
│   ├── test_prepare_workflow.py
│   ├── test_specify_workflow.py
│   ├── test_plan_workflow.py
│   ├── test_implement_workflow.py
│   ├── test_post_workflow.py
│   └── test_full_pipeline.py
│
├── e2e/                           # 10% of tests, slowest, synthetic fixtures
│   ├── test_full_workflow.py
│   ├── test_error_scenarios.py
│   ├── test_multi_feature.py
│   ├── test_state_persistence.py
│   └── test_performance_baseline.py
│
├── fixtures/                      # Shared test data & synthetic projects
│   ├── synthetic_project/        # Small 5-file repo for E2E testing
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── utils.py
│   │   │   └── config.py
│   │   ├── tests/
│   │   │   └── test_main.py
│   │   └── .spekificity/
│   │       └── config.yaml
│   │
│   ├── mock_specs/               # Pre-built spec JSONs for fixtures
│   │   ├── complete_spec.json
│   │   ├── partial_spec.json
│   │   └── invalid_spec.json
│   │
│   ├── mock_plans/               # Pre-built plan JSONs
│   │   ├── complete_plan.json
│   │   └── error_plan.json
│   │
│   └── conftest.py              # pytest fixtures (mocks, temp dirs, etc.)
│
└── ci/                           # CI/CD configuration
    ├── .github/workflows/
    │   ├── test-pr.yaml         # Run on PR, full suite
    │   ├── test-local.yaml      # Optional GitHub-hosted runner job
    │   └── performance.yaml     # Performance tracking (monthly)
    │
    └── pre-commit-hooks/
        ├── run-unit-tests.sh    # Local pre-commit hook (unit tests only)
        └── run-quick-tests.sh   # Local quick check (< 5s, critical path)
```

---

## 2. Unit Tests (60% Coverage)

### 2.1 Enrichment Layer Unit Tests

**File:** `tests/unit/test_enrichment_layer.py`

**Scope:** Load context from vault, merge patterns, inject into input

**Fixtures:** 
- `mock_vault`: MockVault with 3 pre-built decision.md + patterns.md
- `mock_codegraph`: MockCodeGraph with 50 sample symbols
- `mock_context`: Empty enrichment context

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-E1 | Load vault decision | Mock vault with 2 decisions | context["decisions"] = 2 items |
| U-E2 | Load vault patterns | Mock vault with 5 patterns | context["patterns"] = 5 items |
| U-E3 | Query CodeGraph symbols | Mock CodeGraph with 50 symbols | context["symbols"] returns 50 (unfiltered) |
| U-E4 | Filter CodeGraph by type | Mock CodeGraph, query by type "function" | returns only functions (~30 of 50) |
| U-E5 | Merge context layers | 2 decisions + 3 patterns + 20 symbols | merged output = 25 items, no duplicates |
| U-E6 | Handle vault not found | Mock vault missing patterns.md | raise FileNotFoundError w/ clear message |
| U-E7 | Handle CodeGraph timeout | Mock CodeGraph timeout (3s) | raise TimeoutError, continue without graph |
| U-E8 | Handle CodeGraph error | Mock CodeGraph returns error | log warning, continue w/ vault only |
| U-E9 | Token estimate | Merge 100 items | tokens ~= 100 * 3 (conservative estimate) |
| U-E10 | Compression flag | Inject context w/ compress=True | output compressed (caveman format, ~75% reduction) |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ No network calls (fully mocked)
- ✅ < 100ms per test (total < 1s)
- ✅ Coverage: enrichment_layer.py = 95%+

---

### 2.2 Memory Layer Unit Tests

**File:** `tests/unit/test_memory_layer.py`

**Scope:** Read/write vault, repo memory, session memory; handle conflicts

**Fixtures:**
- `mock_vault_dir`: Temporary Obsidian vault (3 docs + 2 patterns)
- `mock_repo_memory`: Temporary /memories/repo/ files
- `mock_session_memory`: Temporary /memories/session/ files

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-M1 | Write vault decision | Empty vault | decision.md created w/ correct format |
| U-M2 | Read vault decision | Vault w/ 2 decisions | returns both, parsed correctly |
| U-M3 | Write vault lesson | Feature complete | lessons/<date>-<id>-<name>.md created |
| U-M4 | Read repo memory | /memories/repo/ w/ 3 files | returns all 3 compressed summaries |
| U-M5 | Write repo memory | New compressed summary | overwrites old if exists |
| U-M6 | Read session memory | /memories/session/ w/ 2 files | returns session-scoped files only |
| U-M7 | Clear session on exit | End of session | /memories/session/ files deleted |
| U-M8 | Conflict: vault duplicate pattern | Try write duplicate pattern name | raise NameConflictError w/ suggestion |
| U-M9 | Conflict: repo memory overwrite | Try overwrite different summary | prompt for overwrite vs. keep old |
| U-M10 | Token estimate vault read | Read 100-item decision.md | tokens ~= 300 (3x for JSON parse overhead) |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ No disk writes to real vault (temp dirs only)
- ✅ < 50ms per test (total < 500ms)
- ✅ Coverage: memory_layer.py = 95%+

---

### 2.3 Feature State Unit Tests

**File:** `tests/unit/test_feature_state.py`

**Scope:** Track feature lifecycle (not_started → specifying → specified → planning → planned → implementing → completing → complete)

**Fixtures:**
- `mock_feature`: Feature w/ initial state
- `mock_state_file`: Temporary feature-state.json

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-FS1 | Initialize feature state | New feature | phase="not_started", % = 0 |
| U-FS2 | Transition to specifying | state.transition("specifying") | phase="specifying", % = 10 |
| U-FS3 | Transition to specified | state.transition("specified") | phase="specified", % = 20 |
| U-FS4 | Transition to planning | state.transition("planning") | phase="planning", % = 30 |
| U-FS5 | Transition to planned | state.transition("planned") | phase="planned", % = 40 |
| U-FS6 | Transition to implementing | state.transition("implementing") | phase="implementing", % = 50 |
| U-FS7 | Transition to completing | state.transition("completing") | phase="completing", % = 90 |
| U-FS8 | Finalize feature | state.transition("complete") | phase="complete", % = 100 |
| U-FS9 | Invalid transition | Try transition "completing" → "planning" | raise InvalidTransitionError |
| U-FS10 | Persist state | Write state to file, reload | state identical after reload |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ < 50ms per test (total < 500ms)
- ✅ Coverage: feature_state.py = 95%+

---

### 2.4 Decorator Wrapper Unit Tests

**File:** `tests/unit/test_decorator_wrapper.py`

**Scope:** Wrap SpecKit commands (prepare, specify, plan, implement) with pre/core/post enrichment

**Fixtures:**
- `mock_speckit`: MockSpecKit (5 command stubs)
- `mock_enrichment`: MockEnrichment context
- `mock_wrapper`: Decorator wrapper instance

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-D1 | Wrap prepare command | speckit.prepare → wrapper.prepare | core called, pre/post skipped (prepare=entry) |
| U-D2 | Wrap specify command | speckit.specify → wrapper.specify | pre (load context) → core → post (save spec) |
| U-D3 | Wrap plan command | speckit.plan → wrapper.plan | pre (inject context) → core → post (save plan) |
| U-D4 | Wrap implement command | speckit.implement → wrapper.implement | pre (inject context) → core → post (collect artifacts) |
| U-D5 | Wrap post command | speckit.post → wrapper.post | pre (skip) → core → post (create lesson) |
| U-D6 | Pre-hook injection | enrichment context injected before core | core receives injected context in args |
| U-D7 | Post-hook collection | core returns dict → post-hook collects | artifacts saved to feature state |
| U-D8 | Error in pre-hook | pre-hook raises error | error logged, core NOT called, wrap returns error |
| U-D9 | Error in core | core raises error → post-hook called? | error in core, post still called (cleanup) |
| U-D10 | Conditional skip | Skip pre-hook if feature already specified | pre-hook skipped, core called directly |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ < 100ms per test (total < 1s)
- ✅ Coverage: decorator_wrapper.py = 95%+

---

### 2.5 Context Injection Unit Tests

**File:** `tests/unit/test_context_injection.py`

**Scope:** Build context strings for injection into SpecKit prompts

**Fixtures:**
- `mock_vault`: Vault w/ 3 decisions, 5 patterns
- `mock_codegraph`: CodeGraph w/ 50 symbols
- `mock_feature_state`: Feature in "planning" phase

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-C1 | Build context for specify | Feature new → context includes goals | context contains project vision + goals |
| U-C2 | Build context for plan | Feature specified → context includes spec | context contains spec + decisions |
| U-C3 | Build context for implement | Feature planned → context includes plan | context contains plan + relevant patterns + code symbols |
| U-C4 | Rank patterns by relevance | 5 patterns + feature topic | top 2 patterns ranked first (by similarity score) |
| U-C5 | Filter symbols by scope | 50 symbols + affected modules | returns ~15 relevant symbols only |
| U-C6 | Token estimate context | Build full context for implement | estimate ~500 tokens |
| U-C7 | Compress context | Build context w/ compress=True | output caveman format, ~75% reduction (~125 tokens) |
| U-C8 | Context too large | Attempt build 2000-token context | warn, truncate to 1500, log warning |
| U-C9 | Missing decisions | Vault empty → context includes fallback | fallback text = "No prior decisions" |
| U-C10 | Format for inject | Build context → ready for prompt injection | output = clean markdown, no escape chars |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ < 100ms per test (total < 1s)
- ✅ Coverage: context_injection.py = 95%+

---

### 2.6 Compression Unit Tests

**File:** `tests/unit/test_compression.py`

**Scope:** Caveman compression (lite, full, ultra modes)

**Fixtures:**
- `mock_text`: 1000-word markdown document
- `mock_code`: 500-line Python file with comments

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| U-CP1 | Compress lite | markdown → lite mode | output ~70% original size, readable |
| U-CP2 | Compress full | markdown → full mode | output ~25% original size, technical accuracy preserved |
| U-CP3 | Compress ultra | markdown → ultra mode | output ~10% original size, caveman format (extreme) |
| U-CP4 | Preserve code | compress code w/ full mode | code blocks untouched, comments reduced |
| U-CP5 | Preserve URLs | compress w/ links | URLs preserved, anchor text reduced if possible |
| U-CP6 | Preserve structure | compress markdown w/ headers | header hierarchy preserved, content under each reduced |
| U-CP7 | Round-trip compression | compress → decompress | original meaning recoverable (not exact text) |
| U-CP8 | Multi-compress | compress already-compressed | idempotent (no further reduction) |
| U-CP9 | Empty input | compress "" → lite | output = "" (no error) |
| U-CP10 | Estimate tokens | original ~300 tokens → full mode | output ~75 tokens (75% reduction) |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ < 50ms per test (total < 500ms)
- ✅ Coverage: compression.py = 95%+
- ✅ Preserved correctness: 100% (no meaning loss, code intact, URLs alive)

---

## 3. Integration Tests (30% Coverage)

### 3.1 Test Organization

Integration tests use real Spekificity code but mock external tools (SpecKit, CodeGraph, vault file I/O). Each test exercises one complete workflow step.

**File:** `tests/integration/test_prepare_workflow.py`

### 3.2 Prepare Workflow Integration Test

**Scope:** /spek.prepare command (entry point, no enrichment)

**Fixtures:**
- `mock_speckit`: Real prepare logic, mocked I/O
- `mock_vault`: Empty vault (init)
- `mock_state`: New feature state

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-PR1 | Prepare creates feature state | Run prepare on new feature | feature-state.json created, phase="not_started" |
| I-PR2 | Prepare creates vault dir | Run prepare | vault/decisions/ created, vault/patterns/ created |
| I-PR3 | Prepare initializes config | Run prepare | .spekificity/config.yaml created w/ defaults |
| I-PR4 | Prepare initializes CodeGraph | Run prepare w/ codegraph=true | codegraph init called, DB created |
| I-PR5 | Prepare exits cleanly | All prep steps succeed | exit code 0, success message |

**Success Criteria:**
- ✅ All 5 tests pass
- ✅ < 500ms per test (total < 3s)
- ✅ Coverage: prepare_workflow.py = 90%+

---

### 3.3 Specify Workflow Integration Test

**File:** `tests/integration/test_specify_workflow.py`

**Scope:** /spek.specify command (loads context, calls SpecKit, saves spec)

**Fixtures:**
- `mock_speckit.specify`: Returns mock spec JSON
- `mock_enrichment`: Context loaded from vault + CodeGraph
- `mock_state`: Feature in "not_started" phase
- `mock_spec_output`: Expected spec.json structure

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-SP1 | Specify loads vault context | spec.specify() called | vault decisions + patterns loaded |
| I-SP2 | Specify queries CodeGraph | spec.specify() called | CodeGraph queried for project symbols |
| I-SP3 | Specify injects context | context injected into SpecKit prompt | SpecKit receives enriched prompt |
| I-SP4 | Specify saves spec | SpecKit returns spec JSON | spec saved to vault/specs/<feature>.json |
| I-SP5 | Specify updates state | Spec saved | feature state phase → "specified", % → 20 |
| I-SP6 | Specify handles CodeGraph error | CodeGraph timeout | spec still generated (vault-only context) |
| I-SP7 | Specify compresses context if enabled | feature.compress=true | context injected in caveman format |
| I-SP8 | Specify exits with code 0 | All steps succeed | exit code 0 |

**Success Criteria:**
- ✅ All 8 tests pass
- ✅ < 1s per test (total < 8s, note: SpecKit calls are slow)
- ✅ Coverage: specify_workflow.py = 90%+

---

### 3.4 Plan Workflow Integration Test

**File:** `tests/integration/test_plan_workflow.py`

**Scope:** /spek.plan command (loads spec + context, calls SpecKit, saves plan)

**Fixtures:**
- `mock_spec`: Spec JSON from prior specify
- `mock_speckit.plan`: Returns mock plan JSON
- `mock_enrichment`: Context loaded from vault + CodeGraph + spec
- `mock_state`: Feature in "specified" phase

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-PL1 | Plan loads spec | plan called | spec.json loaded from vault |
| I-PL2 | Plan loads vault context | plan called | vault decisions + patterns loaded |
| I-PL3 | Plan queries CodeGraph by topic | plan called | CodeGraph filtered by affected modules |
| I-PL4 | Plan injects enriched context | context injected | SpecKit receives spec + decisions + patterns + symbols |
| I-PL5 | Plan saves plan | SpecKit returns plan JSON | plan saved to vault/plans/<feature>.json |
| I-PL6 | Plan updates state | Plan saved | feature state phase → "planned", % → 40 |
| I-PL7 | Plan handles spec missing | spec.json not found | raise MissingArtifactError w/ clear message |
| I-PL8 | Plan exits with code 0 | All steps succeed | exit code 0 |

**Success Criteria:**
- ✅ All 8 tests pass
- ✅ < 1s per test (total < 8s)
- ✅ Coverage: plan_workflow.py = 90%+

---

### 3.5 Implement Workflow Integration Test

**File:** `tests/integration/test_implement_workflow.py`

**Scope:** /spek.implement command (per-task pre/core/post, continue-on-error, code diff collection)

**Fixtures:**
- `mock_plan`: Plan JSON w/ 3 tasks
- `mock_speckit.implement`: Per-task implementation (1 success, 1 fail, 1 success)
- `mock_git`: Mock git diff output
- `mock_state`: Feature in "planned" phase

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-IM1 | Implement loads plan | implement called | plan.json loaded from vault |
| I-IM2 | Implement iterates tasks | plan w/ 3 tasks | core called 3 times (once per task) |
| I-IM3 | Implement task 1 success | Task 1 succeeds | output: "Task 1/3 complete ✓" |
| I-IM4 | Implement task 2 fail | Task 2 fails | output: "Task 2/3 failed (continue)", core not called for task 3? No—**continue-on-error mode** |
| I-IM5 | Implement continue-on-error | Task 2 fails → Task 3 called | Task 3 still executed (skip failed, proceed) |
| I-IM6 | Implement task 3 success | Task 3 succeeds after task 2 fail | output: "Task 3/3 complete ✓" |
| I-IM7 | Implement collects git diff | All tasks done → git diff called | execution trace includes code diffs in JSON format |
| I-IM8 | Implement updates state partial | 2 of 3 succeed | feature state phase → "completing", % → 90 |
| I-IM9 | Implement exit code 1 | Some tasks fail | exit code 1 (partial completion) |
| I-IM10 | Implement exit code 0 | All tasks succeed | exit code 0 (full completion) |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ < 2s per test (total < 20s, note: implement is slowest)
- ✅ Coverage: implement_workflow.py = 90%+
- ✅ Error resilience verified: continue-on-error semantics confirmed

---

### 3.6 Post Workflow Integration Test

**File:** `tests/integration/test_post_workflow.py`

**Scope:** /spek.post command (create lessons, finalize feature state)

**Fixtures:**
- `mock_plan`: Plan JSON from prior implement
- `mock_codegraph`: CodeGraph w/ executed code symbols
- `mock_state`: Feature in "completing" phase

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-PT1 | Post loads feature artifacts | post called | spec + plan loaded from vault |
| I-PT2 | Post calls lessons command | post → /spek.lessons | lesson generation triggered |
| I-PT3 | Post saves lesson | lesson generated | lesson.md saved to vault/lessons/ |
| I-PT4 | Post compresses lesson | lesson compressed flag set | lesson output in caveman format (~75% reduction) |
| I-PT5 | Post updates state final | Lesson saved | feature state phase → "complete", % → 100 |
| I-PT6 | Post locks feature | Feature complete | feature state immutable (no re-open) |
| I-PT7 | Post git commit | Feature complete → git commit | commit message auto-generated from feature name |
| I-PT8 | Post exit code 0 | All steps succeed | exit code 0 |

**Success Criteria:**
- ✅ All 8 tests pass
- ✅ < 1s per test (total < 8s)
- ✅ Coverage: post_workflow.py = 90%+

---

### 3.7 Full Pipeline Integration Test

**File:** `tests/integration/test_full_pipeline.py`

**Scope:** All 5 workflows in sequence (prepare → specify → plan → implement → post)

**Fixtures:**
- `mock_speckit`: All 5 commands
- `mock_vault`: Empty at start, populated by workflow
- `mock_state`: Feature lifecycle from not_started → complete

**Test Cases:**

| Test ID | Test Name | Setup | Assertion |
|---------|-----------|-------|-----------|
| I-FP1 | Full pipeline prepare | Start: fresh dir | End: feature state created, phase="not_started" |
| I-FP2 | Full pipeline specify | Start: phase="not_started" | End: spec.json saved, phase="specified" |
| I-FP3 | Full pipeline plan | Start: phase="specified" | End: plan.json saved, phase="planned" |
| I-FP4 | Full pipeline implement | Start: phase="planned" | End: code changes, phase="completing" |
| I-FP5 | Full pipeline post | Start: phase="completing" | End: lesson saved, phase="complete" |
| I-FP6 | Full pipeline idempotent | Run pipeline twice on same feature | Second run recognizes phase, skips to next (or re-does current) |
| I-FP7 | Full pipeline artifact consistency | Feature complete → artifacts exist | spec.json, plan.json, lesson.md all present, consistent |
| I-FP8 | Full pipeline state consistent | Feature complete → state file | feature-state.json = complete, % = 100, all phases recorded |

**Success Criteria:**
- ✅ All 8 tests pass
- ✅ < 10s per test (total < 80s for full pipeline)
- ✅ Coverage: integration of all workflows = 95%+
- ✅ End-to-end validation: feature lifecycle complete, no data loss

---

## 4. End-to-End Tests (10% Coverage)

### 4.1 Test Organization

E2E tests use the synthetic project fixture (real file I/O, real CodeGraph queries, real Spekificity code). No mocks. Validate entire workflow on a small Python project.

**Fixture:** `tests/fixtures/synthetic_project/`

```
synthetic_project/
├── src/
│   ├── main.py (100 lines, 2 functions)
│   ├── utils.py (50 lines, 3 functions)
│   └── config.py (30 lines, 1 class)
├── tests/
│   └── test_main.py (20 lines)
├── README.md (short project description)
└── .spekificity/
    └── config.yaml (minimal)
```

**Setup:**
- Copy synthetic_project to temp dir for each E2E test
- Initialize CodeGraph on synthetic_project
- Run Spekificity workflows
- Verify outputs on real code

---

### 4.2 Full Workflow E2E Test

**File:** `tests/e2e/test_full_workflow.py`

**Scope:** All 5 workflows on synthetic project (prepare → specify → plan → implement → post)

**Test Cases:**

| Test ID | Test Name | Expected Outcome |
|---------|-----------|------------------|
| E-FW1 | Full workflow prepare | Feature state created for "add-logging" feature |
| E-FW2 | Full workflow specify | spec.json generated (real SpecKit call or mock?) |
| E-FW3 | Full workflow plan | plan.json generated w/ 3 tasks (add logging to main.py, utils.py, config.py) |
| E-FW4 | Full workflow implement | Tasks executed, code modified, 3 git diffs collected |
| E-FW5 | Full workflow post | lesson.md created w/ 8 sections, feature complete |
| E-FW6 | Full workflow artifacts | All files (spec, plan, lesson) saved to vault/ |
| E-FW7 | Full workflow state | feature-state.json shows phase="complete", all phases recorded |

**Success Criteria:**
- ✅ All 7 tests pass
- ✅ < 30s per test (total < 210s, note: real SpecKit calls are slow)
- ✅ Real code analysis on synthetic_project verified
- ✅ CodeGraph queries return real symbols from src/

---

### 4.3 Error Scenarios E2E Test

**File:** `tests/e2e/test_error_scenarios.py`

**Scope:** Handle errors gracefully (missing vault, CodeGraph timeout, git error, task fail)

**Test Cases:**

| Test ID | Test Name | Error | Expected Behavior |
|---------|-----------|-------|------------------|
| E-ES1 | Missing vault | vault/ dir doesn't exist | Auto-created, workflow continues |
| E-ES2 | Missing spec | Try implement without spec | Error: "Missing spec.json", exit code 2 |
| E-ES3 | Missing plan | Try implement without plan | Error: "Missing plan.json", exit code 2 |
| E-ES4 | Task fails | Task 1 fails → Task 2 should still run | Continue-on-error: Task 1 failed, Task 2 executed |
| E-ES5 | CodeGraph timeout | CodeGraph queries timeout (mock 3s) | Context loaded from vault only, workflow continues |
| E-ES6 | Git error | git diff fails | Warning logged, workflow continues (no diff in trace) |
| E-ES7 | State corruption | feature-state.json malformed JSON | Error: "Invalid state file", prompt user to reset |
| E-ES8 | Interrupt mid-workflow | Ctrl+C during implement | Feature state phase remains as-is, resume on next run |

**Success Criteria:**
- ✅ All 8 tests pass
- ✅ Errors handled gracefully (no crashes, clear messages, state preserved)
- ✅ Resume capability verified (partial state retrievable)

---

### 4.4 Multi-Feature E2E Test

**File:** `tests/e2e/test_multi_feature.py`

**Scope:** Run 2 features sequentially on same synthetic_project (state isolation, artifact mgmt)

**Test Cases:**

| Test ID | Test Name | Expected Outcome |
|---------|-----------|------------------|
| E-MF1 | Feature 1 complete | Feature "add-logging" phase="complete", lesson saved |
| E-MF2 | Feature 2 start | Feature "add-tests" phase="not_started" (new feature) |
| E-MF3 | Feature 2 complete | Feature "add-tests" phase="complete", separate lesson saved |
| E-MF4 | Feature isolation | Feature 1 & 2 specs/plans/lessons separate files, no cross-contamination |
| E-MF5 | State isolation | feature-state.json tracks both features independently |
| E-MF6 | Vault organization | vault/specs/, vault/plans/, vault/lessons/ organized by feature ID |

**Success Criteria:**
- ✅ All 6 tests pass
- ✅ Multi-feature state management verified
- ✅ No interference between concurrent feature work

---

### 4.5 State Persistence E2E Test

**File:** `tests/e2e/test_state_persistence.py`

**Scope:** Session restart (stop mid-workflow, reload state, resume)

**Test Cases:**

| Test ID | Test Name | Scenario | Expected Outcome |
|---------|-----------|----------|------------------|
| E-SP1 | Interrupt at specify | Run prepare → specify → Ctrl+C | Feature state phase="specified" persisted |
| E-SP2 | Resume from specify | Reload state, run plan | Workflow continues from planned phase (specify skipped) |
| E-SP3 | Interrupt at implement | Run plan → implement (task 1 done) → Ctrl+C | Feature state phase="implementing", % = ~50 |
| E-SP4 | Resume from implement | Reload state, run implement | Workflow resumes tasks (task 2+ executed) |
| E-SP5 | No state loss | Multiple interrupts + resumes | Artifact files (spec, plan, lessons) never lost |
| E-SP6 | Idempotent phases | Resume same phase twice | Phase recognized, workflow adapted (re-run or skip) |

**Success Criteria:**
- ✅ All 6 tests pass
- ✅ State persistence across session restarts verified
- ✅ Resume capability tested and functional

---

### 4.6 Performance Baseline E2E Test

**File:** `tests/e2e/test_performance_baseline.py`

**Scope:** Measure & establish performance metrics (wall-clock time, token usage, memory)

**Test Cases:**

| Test ID | Test Name | Measurement | Expected Baseline |
|---------|-----------|-------------|-------------------|
| E-PB1 | Prepare time | Time to prepare | < 5s |
| E-PB2 | Specify time | Time to specify (no SpecKit call, mock) | < 500ms (context load + injection) |
| E-PB3 | Specify tokens | Tokens injected into SpecKit | ~300-500 tokens (uncompressed) |
| E-PB4 | Specify tokens compressed | Tokens injected w/ compress=true | ~75-125 tokens (75% reduction) |
| E-PB5 | Plan time | Time to plan | < 500ms (context load + injection) |
| E-PB6 | Implement time | Time to implement 3 tasks | < 2s (mock SpecKit.implement) |
| E-PB7 | Post time | Time to post (lesson generation) | < 1s |
| E-PB8 | Full pipeline time | Prepare → specify → plan → implement → post | < 10s (all mocks, real file I/O) |
| E-PB9 | CodeGraph perf | CodeGraph symbol query on synthetic_project | < 100ms (MCP tool call) |
| E-PB10 | Memory peak | Peak memory during implement | < 500MB |

**Success Criteria:**
- ✅ All 10 tests pass
- ✅ Baselines established (stored in test output for trending)
- ✅ No performance regression allowed in future runs (< 10% variance)

---

## 5. Mock Objects & Fixtures

### 5.1 Mock SpecKit

**File:** `tests/fixtures/conftest.py` → `mock_speckit` fixture

```python
class MockSpecKit:
    """Simulates SpecKit command responses for testing."""
    
    def prepare(self, feature_name, config):
        """Return success."""
        return {"status": "success", "feature": feature_name}
    
    def specify(self, constitution, enriched_context):
        """Return mock spec JSON."""
        return {
            "feature_name": "add-logging",
            "requirements": ["Add logging to main.py", "Add logging to utils.py"],
            "scope": "core",
            "status": "specified"
        }
    
    def plan(self, spec, enriched_context):
        """Return mock plan JSON (3 tasks)."""
        return {
            "feature_name": "add-logging",
            "tasks": [
                {"id": 1, "name": "Add logging imports", "file": "main.py"},
                {"id": 2, "name": "Add logging calls", "file": "utils.py"},
                {"id": 3, "name": "Update config", "file": "config.py"}
            ],
            "status": "planned"
        }
    
    def implement(self, task, enriched_context):
        """Return mock implementation result."""
        return {
            "task_id": task["id"],
            "status": "success",
            "code_generated": f"# Logging added to {task['file']}",
            "diff": "mock diff here"
        }
    
    def post(self, feature_state):
        """Return success."""
        return {"status": "success", "feature_complete": True}
```

---

### 5.2 Mock CodeGraph

**File:** `tests/fixtures/conftest.py` → `mock_codegraph` fixture

```python
class MockCodeGraph:
    """Simulates CodeGraph MCP tool responses."""
    
    def __init__(self):
        self.symbols = [
            {"name": "main", "type": "function", "file": "main.py", "line": 10},
            {"name": "log_output", "type": "function", "file": "utils.py", "line": 5},
            {"name": "Config", "type": "class", "file": "config.py", "line": 1},
            # ... 47 more mock symbols
        ]
    
    def codegraph_symbols(self, file_path):
        """Return symbols in file."""
        return [s for s in self.symbols if s["file"] == file_path]
    
    def codegraph_definition(self, symbol_name):
        """Return symbol definition."""
        sym = next((s for s in self.symbols if s["name"] == symbol_name), None)
        return sym or {"error": "Symbol not found"}
    
    def codegraph_references(self, symbol_name):
        """Return all references to symbol."""
        return [{"file": "main.py", "line": 15}, {"file": "utils.py", "line": 8}]
    
    def codegraph_impact(self, symbol_name):
        """Return impact radius (affected symbols)."""
        return {
            "direct": ["caller1", "caller2"],
            "transitive": ["indirect1", "indirect2"],
            "estimate_impact": "medium"
        }
    
    def codegraph_query(self, query):
        """Return results from free-form query."""
        if "timeout" in query:
            raise TimeoutError("Query timeout (3s)")
        return {"results": self.symbols[:5]}
```

---

### 5.3 Mock Vault

**File:** `tests/fixtures/conftest.py` → `mock_vault` fixture

```python
class MockVault:
    """Simulates Obsidian vault file I/O."""
    
    def __init__(self, temp_dir):
        self.root = temp_dir
        self.decisions = []
        self.patterns = []
        self.specs = {}
        self.plans = {}
        self.lessons = {}
    
    def read_decisions(self):
        """Return vault decisions."""
        return self.decisions
    
    def read_patterns(self):
        """Return vault patterns."""
        return self.patterns
    
    def write_spec(self, feature_id, spec_dict):
        """Save spec JSON."""
        self.specs[feature_id] = spec_dict
    
    def write_plan(self, feature_id, plan_dict):
        """Save plan JSON."""
        self.plans[feature_id] = plan_dict
    
    def write_lesson(self, feature_id, lesson_dict):
        """Save lesson markdown."""
        self.lessons[feature_id] = lesson_dict
    
    def file_not_found_error(self, path):
        """Raise error if file not found."""
        raise FileNotFoundError(f"Vault file not found: {path}")
```

---

### 5.4 Fixtures: Synthetic Project

**File:** `tests/fixtures/synthetic_project/src/main.py`

```python
"""Main module for synthetic project."""

def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b
```

**File:** `tests/fixtures/synthetic_project/src/utils.py`

```python
"""Utility functions."""

def format_output(value):
    """Format output."""
    return f"Result: {value}"

def validate_input(value):
    """Validate input."""
    return value is not None

def log_event(event):
    """Log event."""
    print(f"Event: {event}")
```

**File:** `tests/fixtures/synthetic_project/src/config.py`

```python
"""Configuration."""

class Config:
    """Application configuration."""
    DEBUG = True
    LOG_LEVEL = "INFO"
```

---

### 5.5 Fixtures: Pre-built Specs/Plans

**File:** `tests/fixtures/mock_specs/complete_spec.json`

```json
{
  "feature_name": "add-logging",
  "feature_id": "add-logging-001",
  "requirements": [
    "Add logging to main.py",
    "Add logging to utils.py",
    "Update config with log level"
  ],
  "scope": "core",
  "status": "specified",
  "created_at": "2026-05-20T10:00:00Z"
}
```

**File:** `tests/fixtures/mock_plans/complete_plan.json`

```json
{
  "feature_name": "add-logging",
  "feature_id": "add-logging-001",
  "tasks": [
    {
      "id": 1,
      "name": "Add logging imports to main.py",
      "description": "Import logging module",
      "file": "src/main.py",
      "priority": 1
    },
    {
      "id": 2,
      "name": "Add logging calls to main functions",
      "description": "Add logging.info() calls",
      "file": "src/main.py",
      "priority": 2
    },
    {
      "id": 3,
      "name": "Update config.py with log level",
      "description": "Add LOG_LEVEL = INFO",
      "file": "src/config.py",
      "priority": 3
    }
  ],
  "status": "planned",
  "created_at": "2026-05-20T10:30:00Z"
}
```

---

## 6. Test Execution & CI/CD

### 6.1 Local Test Execution

**Unit Tests:**
```bash
pytest tests/unit/ -v --cov=src --cov-report=html
# Expected: ~60 tests, < 10s, coverage 80%+
```

**Integration Tests:**
```bash
pytest tests/integration/ -v --cov=src --cov-report=html
# Expected: ~40 tests, < 60s, coverage 30%
```

**E2E Tests:**
```bash
pytest tests/e2e/ -v --cov=src --cov-report=html
# Expected: ~35 tests, < 300s, coverage 10%
```

**Full Suite:**
```bash
pytest tests/ -v --cov=src --cov-report=html
# Expected: ~135 tests, < 370s, coverage 80%+
```

**Quick Check (Pre-commit):**
```bash
pytest tests/unit/ tests/integration/test_full_pipeline.py -v
# Expected: < 70 tests, < 65s, fails fast on critical path
```

---

### 6.2 Local Pre-commit Hook

**File:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Run unit tests before commit
echo "Running unit tests..."
pytest tests/unit/ -q --tb=short
if [ $? -ne 0 ]; then
    echo "Unit tests failed. Commit aborted."
    exit 1
fi
echo "✓ Unit tests passed"
exit 0
```

**File:** `.git/hooks/pre-push`

```bash
#!/bin/bash
# Run full test suite before push (optional, slower)
echo "Running full test suite..."
pytest tests/ -q --tb=short
if [ $? -ne 0 ]; then
    echo "Some tests failed. Push aborted. (override with git push --no-verify)"
    exit 1
fi
echo "✓ All tests passed"
exit 0
```

---

### 6.3 GitHub Actions CI/CD

**File:** `.github/workflows/test-pr.yaml`

```yaml
name: Test on PR

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov pytest-mock
      
      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml
      
      - name: Run integration tests
        run: pytest tests/integration/ -v --cov=src --cov-report=xml --cov-append
      
      - name: Run E2E tests (quick subset)
        run: pytest tests/e2e/test_full_workflow.py -v --cov=src --cov-report=xml --cov-append
        timeout-minutes: 5
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: false
          flags: unittests
          name: codecov-umbrella
```

**File:** `.github/workflows/performance.yaml` (Monthly)

```yaml
name: Performance Baseline

on:
  schedule:
    - cron: '0 0 1 * *'  # Run on 1st of each month

jobs:
  perf:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-benchmark
      
      - name: Run performance tests
        run: pytest tests/e2e/test_performance_baseline.py -v --benchmark-only
      
      - name: Store baseline
        run: |
          mkdir -p perf-baselines
          cp .benchmarks/0001_*.json perf-baselines/$(date +%Y-%m-%d).json || true
      
      - name: Commit baseline
        run: |
          git config user.name "Performance Bot"
          git config user.email "bot@spekificity.dev"
          git add perf-baselines/ || true
          git commit -m "Perf baseline: $(date +%Y-%m-%d)" || true
          git push || true
```

---

## 7. Coverage & Success Criteria

### 7.1 Overall Coverage Target

| Layer | Target | Tests | Est. Time |
|-------|--------|-------|-----------|
| Unit | 80% | 60 | < 10s |
| Integration | 80% | 40 | < 60s |
| E2E | 80% | 35 | < 300s |
| **Total** | **80%** | **135** | **< 370s** |

### 7.2 Per-Module Coverage

| Module | Target | Tests |
|--------|--------|-------|
| enrichment_layer.py | 95% | 10 |
| memory_layer.py | 95% | 10 |
| feature_state.py | 95% | 10 |
| decorator_wrapper.py | 95% | 10 |
| context_injection.py | 95% | 10 |
| compression.py | 95% | 10 |
| prepare_workflow.py | 90% | 5 |
| specify_workflow.py | 90% | 8 |
| plan_workflow.py | 90% | 8 |
| implement_workflow.py | 90% | 10 |
| post_workflow.py | 90% | 8 |
| Full integration | 95% | 8 |
| E2E scenarios | 85% | 35 |

### 7.3 Success Criteria

✅ **All tests pass (135/135)**

✅ **Coverage ≥ 80% (overall line coverage)**

✅ **Performance baselines established & tracked:**
- Prepare: < 5s
- Specify: < 500ms (context load)
- Plan: < 500ms (context load)
- Implement: < 2s (per-task execution)
- Post: < 1s
- Full pipeline: < 10s

✅ **Error handling validated:**
- Missing artifacts → clear errors
- External tool timeouts → graceful degradation
- State corruption → recovery prompts
- Task failures → continue-on-error semantics verified

✅ **State persistence validated:**
- Session interruption → state saved
- Session resume → state loaded correctly
- Multi-feature isolation → no cross-contamination

✅ **No regressions:**
- Future runs must maintain baselines (< 10% variance)
- Coverage must not decrease

---

## 8. Test Maintenance & Evolution

### 8.1 Adding New Tests

When adding new Spekificity workflows:

1. **Add unit tests first** (mock externals, fast feedback)
2. **Add integration tests** (real code, mocked externals)
3. **Add E2E tests** (synthetic fixture, validate end-to-end)
4. **Measure performance** (establish baseline)
5. **Update this spec** (document new test cases)

### 8.2 Updating Mocks

When external tools (SpecKit, CodeGraph) change:

1. Update mock in `tests/fixtures/conftest.py`
2. Update corresponding unit/integration tests
3. Re-run full suite (should still pass)
4. Update this spec with new mock behavior

### 8.3 Baseline Regression Management

Monthly performance baseline runs (GitHub Actions) track:
- Wall-clock time (prepare, specify, plan, implement, post)
- Token usage (injected context)
- Memory peak usage
- CodeGraph query latency

If regression detected (> 10% variance):
- Alert sent to contributors
- Investigation required before merge
- Optimization opportunity logged

---

## 9. Quick Reference: Test Command Aliases

```bash
# Unit tests only (fast, pre-commit)
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v

# Full suite (all layers)
pytest tests/ -v --cov=src --cov-report=html

# Critical path (unit + integration pipeline)
pytest tests/unit/ tests/integration/test_full_pipeline.py -v

# With coverage report
pytest tests/ --cov=src --cov-report=html && open htmlcov/index.html

# GitHub-style check (fail fast)
pytest tests/ -x -q  # Stop on first failure, quiet output

# Performance baseline
pytest tests/e2e/test_performance_baseline.py -v --benchmark-only
```

---

## 10. Dependencies & Setup

### 10.1 Python Test Dependencies

```
pytest>=7.0
pytest-cov>=4.0
pytest-mock>=3.10
pytest-timeout>=2.1
pytest-benchmark>=4.0
```

### 10.2 Installation

```bash
pip install -e .[test]
# or
pip install pytest pytest-cov pytest-mock pytest-timeout pytest-benchmark
```

### 10.3 Project Root Structure for Tests

```
spekificity/
├── src/
│   ├── enrichment_layer.py
│   ├── memory_layer.py
│   ├── feature_state.py
│   ├── decorator_wrapper.py
│   ├── context_injection.py
│   ├── compression.py
│   ├── prepare_workflow.py
│   ├── specify_workflow.py
│   ├── plan_workflow.py
│   ├── implement_workflow.py
│   └── post_workflow.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── fixtures/
│   └── conftest.py
│
├── .github/workflows/
│   ├── test-pr.yaml
│   └── performance.yaml
│
└── setup.py
```

---

## References

- **Feature State Tracking:** [specs/feature-state-tracking.md](specs/feature-state-tracking.md)
- **Enrichment Layer:** [specs/enrichment-layer.md](specs/enrichment-layer.md)
- **Memory Architecture:** [specs/memory-architecture.md](specs/memory-architecture.md)
- **Spek Implement Workflow:** [specs/spek-implement-workflow.md](specs/spek-implement-workflow.md)
- **Spek Lessons Command:** [specs/spek-lessons-command.md](specs/spek-lessons-command.md)
- **CodeGraph Setup:** [specs/codegraph-setup-complete.md](specs/codegraph-setup-complete.md)
