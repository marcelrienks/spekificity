# Code vs Documentation Gaps

**Last Reviewed:** 2026-06-08  
**Status:** Implementation incomplete. Most promised workflow stages are scaffolding only.

---

## Critical Gaps (Blocking Workflow)

### 1. Skills Not Exposed as CLI Commands
**Severity:** 🔴 CRITICAL — Workflow unusable

| Item | Status |
|------|--------|
| Documented | `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`, `/spek.lessons` as runnable commands |
| Implemented | Python modules in `spekificity/skills/` |
| Problem | **CLI only registers `spek init`** (main.py:44). Skills exist as importable functions, not CLI commands. Users cannot run workflow. |

**Evidence:**
- setup.md:26-28: "`spek prepare`, `spek plan`, `spek implement`" — runnable
- workflow.md:51-53: "4-stage workflow" with `/spek.prepare` through `/spek.conclude`
- **Code:** main.py only has `@cli.command()` for `init`

**Fix:** Wire skills to CLI. Add `@cli.command()` decorators in main.py for prepare, plan, implement, conclude, lessons.

---

### 2. Vault Location Changed, Docs Not Updated
**Severity:** 🔴 CRITICAL — Setup instructions wrong

| File | Says | Reality | Status |
|------|------|---------|--------|
| setup.md:165-174 | `vault/` at project root | `.spek/vault/` | ❌ Stale |
| init.py echo | `ls -la vault/` | Actually `.spek/vault/` | ❌ Wrong in CLI message |
| vault.py:14 | default `.spek/vault` | ✓ Correct | ✓ Code correct |
| context.py:18 | default `.spek/vault` | ✓ Correct | ✓ Code correct |
| CLAUDE.md | "vault at .spek/vault" | ✓ Documented | ✓ Memory correct |

**History:**
- Commit 0eb1b89: "refactor: move vault into .spek directory"
- Commit d39bebf: "docs: update CLAUDE.md to reflect vault location"
- But setup.md, workflow.md still reference `vault/` at root

**Fix:** Update all docs to `.spek/vault`. Replace all `vault/` references in setup.md, workflow.md, architecture.md.

---

### 3. Missing `/spek.lessons` as Standalone Skill
**Severity:** 🔴 CRITICAL — Feature promised, not delivered

| Item | Status |
|------|--------|
| Documented | `/spek.lessons --deep` (workflow.md:337-340) for explicit reflection |
| Implemented | Embedded in `conclude.py` only (line 115) |
| Problem | No standalone skill module. Lessons only via `/spek.conclude`. Cannot run independently. |

**Evidence:**
- workflow.md:337-340: "`/spek.lessons --deep` available for explicit, detailed reflection"
- architecture.md:269: "`spek.lessons` (learn)" as separate skill
- **Code:** No `spekificity/skills/lessons.py` file

**Fix:** Create `spekificity/skills/lessons.py`. Extract lesson logic from conclude.py. Wire to CLI.

---

### 4. SpecKit Integration Wrapper Incomplete
**Severity:** 🔴 CRITICAL — Spec/plan generation not functional

| Item | Status |
|------|--------|
| Documented | `/spek.plan` wraps `/speckit.specify` + `/speckit.plan` + `/speckit.tasks` |
| Implemented | `speckit_wrapper.py` exists with stubbed functions |
| Problem | Functions `run_specify()`, `run_plan()` are placeholders. No subprocess calls to actual `specify` CLI. Spec/plan/task generation not working. |

**Evidence:**
- workflow.md:813: Spekificity wraps SpecKit phases
- **Code:** speckit_wrapper.py has empty function stubs

**Fix:** Implement subprocess calls to `specify` CLI. Generate actual spec/plan/tasks.

---

### 5. lat.md Integration Not Wired
**Severity:** 🔴 CRITICAL — Code analysis not functional

| Item | Status |
|------|--------|
| Documented | lat.md queries during `/spek.plan` (workflow.md:66) and `/spek.implement` |
| Implemented | `LatMdIndex` class exists (integrations/lat_md.py) but incomplete |
| Problem | **MCP interface not wired**. Queries not actually invoked. No file-watcher. No incremental sync. |

**Evidence:**
- workflow.md:299: "lat.md integration: lat.md reflects all new code"
- architecture.md:106-110: "lat.md as sole code analysis tool," "BM25 retrieval," "incremental sync + file watcher"
- **Code:** `LatMdIndex.__init__()` and `ensure_structure()` only; no query methods

**Fix:** Implement MCP tool calls for `lat_symbols`, `lat_references`, `lat_callers`, `lat_impact`. Add file-watcher for incremental sync.

---

### 6. Enrichment Layers Not Implemented
**Severity:** 🔴 CRITICAL — Spec quality metrics missing

| Item | Status |
|------|--------|
| Documented | Success Criteria, Assumptions, Risk Assessment, Metrics (workflow.md:85-92) |
| Implemented | `EnrichmentFormatter` class exists (core/enrichment.py) but empty |
| Problem | Placeholder class only. No logic generates documented layers. |

**Evidence:**
- workflow.md:559-562: Risk levels with emoji (🔴🟡🟢)
- workflow.md:85-92: Enrichment layer table (Success Criteria, Assumptions, etc.)
- **Code:** enrichment.py has class stubs with no method implementations

**Fix:** Implement layer generation. Add logic to produce Success Criteria, Risk Assessment, Assumptions, Resource Estimate, Metrics.

---

## High-Priority Gaps (Feature-Incomplete)

### 7. spec/ Directory vs vault/ Structure Undefined
**Severity:** 🟡 HIGH — Unclear where specs live

| Item | Status |
|------|--------|
| Documented | setup.md:176-177: `specs/` directory for feature specs |
| Implemented | init.py doesn't create `specs/` |
| Problem | Spec storage location undefined. Docs reference `specs/` but code doesn't create it. |

**Evidence:**
- setup.md:176: `specs/` directory for feature specifications
- **Code:** init.py calls `create_vault_structure()` but no `specs/` creation

**Fix:** Define spec storage location (project root `specs/` or in vault?). Update init.py and docs consistently.

---

### 8. Vault Structure Incomplete
**Severity:** 🟡 HIGH — Missing vision.md

| Item | Expected | Actual |
|------|----------|--------|
| decisions.md | ✓ | ✓ |
| patterns.md | ✓ | ✓ |
| lessons/ | ✓ | ✓ |
| vision.md | ✓ | ❌ |

**Evidence:**
- setup.md:196: `vision.md` listed as standard vault file
- **Code:** init.py only creates decisions.md, patterns.md, lessons/

**Fix:** Add vision.md creation to `create_vault_structure()`.

---

### 9. Obsidian CLI Requirement Confusing
**Severity:** 🟡 HIGH — Conflicting documentation

| Section | States |
|---------|--------|
| setup.md:123 | "Obsidian CLI is required and provisioned" |
| setup.md:20, 163 | "Only needed for vault exports"; optional |
| setup.md:133 | "non-blocking" |
| architecture.md:74 | "Mandatory for `/spek.conclude`" |

**Problem:** Docs call it "required" but code treats it as optional. Unclear whether it's mandatory or optional.

**Evidence:**
- init.py warns if missing but continues (non-blocking)
- No code in spek init auto-installs Obsidian CLI
- "provisioned as part of spek init" (setup.md:123) is misleading

**Fix:** Clarify: Obsidian CLI is **optional**. Only needed for vault graph exports in `/spek.conclude`. Update docs to remove "required" language.

---

### 10. Task Commit Format Not Enforced
**Severity:** 🟡 HIGH — Convention documented, not implemented

| Item | Status |
|------|--------|
| Documented | workflow.md:261: `[Task X] description` commit format |
| Implemented | No enforcement in code |
| Problem | Convention documented but code doesn't enforce or generate commits with this format. |

**Fix:** Implement commit generation in `implement.py` with task ID in message.

---

## Medium-Priority Gaps (Incomplete Features)

### 11. Lesson Template Not Enforced
**Severity:** 🟡 MEDIUM

| Item | Status |
|------|--------|
| Documented | workflow.md:383-408: Full YAML + Markdown template |
| Implemented | `Vault.write_lesson()` takes simple dict |
| Problem | Template structure documented but not enforced in code. |

**Fix:** Enforce lesson structure with Pydantic model. Validate YAML frontmatter.

---

### 12. Risk Assessment Output Missing Emoji Levels
**Severity:** 🟡 MEDIUM

| Item | Status |
|------|--------|
| Documented | workflow.md:559-562: 🔴 HIGH, 🟡 MEDIUM, 🟢 LOW |
| Implemented | Risk assessment not generated at all |
| Problem | Enrichment layer promised but implementation missing. |

**Fix:** Implement risk assessment generation with severity levels.

---

### 13. Context Injection Not Wired
**Severity:** 🟡 MEDIUM

| Item | Status |
|------|--------|
| Documented | workflow.md:813: "PRE-Execution Enrichment: Load vault decisions + patterns + code graph" |
| Implemented | `ContextLoader` class exists but not called during skill execution |
| Problem | Context loading infrastructure built but not integrated into skills. |

**Fix:** Wire context loading into prepare, plan, implement phases.

---

### 14. Dependency Graph Analysis Missing
**Severity:** 🟡 MEDIUM

| Item | Status |
|------|--------|
| Documented | workflow.md:173-177: Dependency graph in plan output |
| Implemented | Task parsing exists but no dependency analysis |
| Problem | Dependencies documented as output but not generated. |

**Fix:** Implement dependency analysis in plan generation.

---

## Low-Priority Gaps (Documentation Issues)

### 15. init.py Echo Messages Incorrect
**Severity:** 🔵 LOW

| Message | Says | Should Say |
|---------|------|-----------|
| init.py | `ls -la vault/` | `ls -la .spek/vault/` |
| init.py | Review vault structure at `vault/` | Review vault structure at `.spek/vault/` |

**Fix:** Update echo messages in init.py to reference `.spek/vault/` correctly.

---

### 16. architecture.md References Non-Existent Features
**Severity:** 🔵 LOW

| Reference | Status |
|-----------|--------|
| "markdown-hero" (line 102) | Not in dependencies or code |
| "BM25 lexical retrieval" (line 109) | Promised but not implemented |
| "section-aware chunking" (line 100) | Not implemented |
| "repair agent" (line 101) | Not implemented |

**Fix:** Remove references to unimplemented features or mark as "future" in architecture.md.

---

### 17. setup.md Troubleshooting References Non-Existent Commands
**Severity:** 🔵 LOW

| Reference | Status |
|-----------|--------|
| "`lat.md --version`" (setup.md:257) | May not exist in installed tool |
| "`specify --version`" (setup.md:351) | Depends on SpecKit version |

**Fix:** Test commands before documenting or add version context.

---

## What Works ✅

- `spek init` creates `.spek/` structure correctly
- Vault paths correct in code (`.spek/vault`)
- Core classes exist (Vault, ContextLoader, PlanGenerator, Parser types)
- Git integration basics functional
- YAML parsing for vault files
- Type system (Pydantic models)
- Logging infrastructure

---

## What Doesn't Work ❌

- **All `/spek.*` CLI commands** except `init`
- **Spec/plan/task generation** (SpecKit wrapper stubbed)
- **lat.md queries** (MCP interface not wired)
- **Enrichment layers** (Success Criteria, Risk Assessment, Assumptions)
- **Lesson extraction** (hardcoded in conclude only)
- **Obsidian CLI automation** (not integrated)
- **File watcher for lat.md** (promised, not implemented)
- **Dependency analysis** (promised, not implemented)
- **Context injection** (infrastructure exists, not called)

---

## Remediation Roadmap

### Phase 1: CLI Exposure (Unblock workflow)
1. Wire all skills to CLI commands
2. Update vault path docs to `.spek/vault`
3. Create standalone `/spek.lessons` skill

### Phase 2: Core Functionality (Make skills functional)
1. Implement SpecKit wrapper (subprocess calls)
2. Implement lat.md query interface
3. Implement enrichment layer generation
4. Implement context injection in skills

### Phase 3: Quality (Polish and completeness)
1. Create `specs/` directory structure
2. Add vision.md to vault init
3. Enforce lesson template structure
4. Implement task commit formatting
5. Add dependency graph analysis

### Phase 4: Documentation (Align with reality)
1. Update all docs to `.spek/vault` paths
2. Clarify Obsidian CLI as optional
3. Remove references to unimplemented features
4. Fix init.py echo messages
5. Test all documented commands

---

## Notes

- Code structure is sound; feature-completeness is the blocker.
- Most gaps are implementation gaps, not design gaps.
- User memory (CLAUDE.md) correctly tracks vault location change.
- Project is **alpha**; documented features represent future roadmap, not current state.
