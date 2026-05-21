# Enrichment Layer: Context Injection Into SpecKit Workflow

**Status:** ATOMIC SPECIFICATION   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Type:** Integration Layer — Context injection across all enrichment phases  
**Replaces:** specify-enrichment.md, plan-enrichment.md, implement-enrichment.md  
**Used By:** `/spek.plan` (all phases)

---

## Overview

The enrichment layer injects project context (decisions, patterns, code structure) into SpecKit commands to guide spec generation, planning, and implementation toward existing project constraints and patterns. This spec covers the three enrichment phases that wrap SpecKit's core commands:

1. **Specify Enrichment** — Context injection into `/speckit.specify`
2. **Plan Enrichment** — Context + code graph injection into `/speckit.plan`
3. **Implement Enrichment** — Artifact collection after `/speckit.implement`

All three follow the same pattern: **PRE → CORE → POST** execution sequence.

---

## Enrichment Pattern (All Phases)

Each enrichment phase follows this structure:

```
/spek.plan [feature-description]
   └─ <phase> phase
      ├─ PRE: Load context
      │  ├─ Load decisions + patterns from session memory
      │  ├─ Construct enrichment prompt
      │  └─ Output: enriched context (string)
      ├─ CORE: Call SpecKit command
      │  ├─ Inject context into SpecKit prompt
      │  ├─ Run /speckit.<command>
      │  ├─ Capture output
      │  └─ Output: <artifact>.md
      ├─ POST: Validate + Update memory
      │  ├─ Validate output is well-formed
      │  ├─ Check output aligns with decisions
      │  ├─ Update session memory
      │  └─ Output: Completion report
      └─ Return: Artifact + status
```

---

## Phase 1: Specify Enrichment

Specifies what to build, guided by project decisions and patterns.

### Execution Sequence

```
/spek.plan [feature-description]
   └─ specify phase
      ├─ PRE: Load context
      ├─ CORE: Call `/speckit.specify`
      ├─ POST: Validate
      └─ Return: spec.md
```

### Pre-Execution: Context Injection

**Process:**
1. Load decisions + patterns from vault/session/
2. Format as prompt injection:
   ```
   IMPORTANT: Adhere to these project decisions:
   - [Decision 1]: [rationale]
   - [Decision 2]: [rationale]
   
   Consider these proven patterns:
   - [Pattern 1]: [when to use]
   - [Pattern 2]: [when to use]
   ```
3. Prepend to feature description before calling SpecKit

**Context Used:**
- Recent decisions (top 5, active only)
- Recent patterns (top 3, active only)

**Goal:** Guide spec toward existing constraints without over-constraining

## Success Criteria

- ✅ Context injection adds decisions + patterns without overwhelming LLM (context <10K tokens)
- ✅ Generated artifacts are more context-aware than vanilla SpecKit (improvement visible in review)
- ✅ Specify phase generates specs aligned with architectural decisions
- ✅ Plan phase generates plans that consider existing code structure
- ✅ Implementation phase generates code that follows established patterns
- ✅ Output quality measurable (specs complete, plans coherent, tasks achievable)
- ✅ Fallback behavior works (if context missing, enrichments skip injection and continue)

---

### Core Execution

**Command:** `/speckit.specify [enriched-feature-description]`

**Process:**
- SpecKit reads feature description (with injected context)
- SpecKit reads constitution.md (if exists)
- SpecKit calls Claude model
- Claude generates spec.md

**Model Settings:**
- Model: Claude Opus (high-quality spec generation)
- Temperature: 0.3 (consistent + focused)
- Max tokens: 4000

**Output:** spec.md (created in current directory)

### Post-Execution: Validation

**Validation Checks:**
1. spec.md exists and is non-empty
2. Markdown is well-formed (parseable)
3. Required sections present (requirements, acceptance criteria)
4. Spec doesn't contradict recent decisions (warn if it does)

**Update Memory:**
- Mark vault/session/ phase as "specifying"
- Set completion to 25%
- Add session log entry: "[SPECIFIED] spec.md created"

**Output:**
- Completion report: "✓ Spec created. Phase: specifying (25% complete)"

### Error Handling

**If context load fails:**
- Continue with partial context (or no context)
- Log warning "Some context unavailable"
- SpecKit might generate weaker spec, but still valid

**If /speckit.specify fails:**
- Catch exception
- Return empty spec template (user fills in manually)
- Report: "Spec generation failed. Using template."

**If validation fails:**
- Log warnings about specific failures
- Still return spec.md (might be usable)
- Report: "Spec created but has issues (see warnings)"

---

## Phase 2: Plan Enrichment

Creates technical implementation plan, guided by spec, decisions, patterns, and code structure.

### Execution Sequence

```
/spek.plan
   └─ plan phase
      ├─ PRE: Load context + code graph
      ├─ CORE: Call `/speckit.plan`
      ├─ POST: Validate
      └─ Return: plan.md
```

### Pre-Execution: Context + Code Graph Injection

**Context Injection (same as specify):**
- Recent decisions (top 5)
- Recent patterns (top 3)

**Code Graph Injection (NEW):**
1. Read spec.md (identify affected modules)
2. Query wiki/vault/graph/nodes.jsonl for affected modules
3. Extract code structure:
   - List existing modules in affected areas
   - Show recently changed files (might be relevant)
   - Extract dependencies
4. Format for injection:
   ```
   CODE STRUCTURE (affected areas):
   - Module A: [existing code for X]
   - Module B: [existing code for Y]
   - Consider reusing: [components]
   ```

**Goal:** Prevent duplicate work; reuse existing code where possible

### Core Execution

**Command:** `/speckit.plan`

**Input:** spec.md + injected context + code graph

**Model:** Claude Opus (high-quality architecture)  
**Temperature:** 0.3  
**Max tokens:** 5000

**Output:** plan.md (architecture, design decisions, component breakdown)

### Post-Execution: Validation

**Validation Checks:**
1. plan.md exists and is non-empty
2. Architecture is clearly described
3. Design decisions are documented
4. Plan doesn't contradict recent decisions (warn if it does)
5. Plan doesn't duplicate existing code (warn if it does)

**Update Memory:**
- Mark vault/session/ phase as "planning"
- Set completion to 50%
- Log: "[PLANNED] plan.md created"

### Error Handling

Same as specify (graceful degradation, fallback template).

---

## Phase 3: Implement Enrichment

Executes tasks and collects artifacts for post-processing.

### Execution Sequence

```
/spek.implement
├─ PRE: Validate preconditions
├─ CORE: Run `/speckit.implement`
├─ POST: Collect + Update
└─ Return: Artifacts + status
```

### Pre-Execution: Validation

**Preconditions:**
- tasks.md exists and is complete
- Git working directory is clean
- No uncommitted changes (or user stashed them)

**Process:**
- Validate preconditions
- Log feature state (what we're implementing)
- Report ready status

### Core Execution

**Command:** `/speckit.implement`

**Process:**
- SpecKit executes all tasks sequentially (or parallel if configured)
- Each task generates code changes
- Execution trace logged (task ID, status, duration, errors)

**Output:**
- Modified files (code changes)
- Execution trace (log of what ran)
- Errors/warnings (if any tasks failed)

### Post-Execution: Artifact Collection

**Collect:**
1. Code changes (git diff)
   - List of modified files
   - Lines added/deleted
   - Diff content
2. Execution trace
   - Task execution log
   - Task success/failure
   - Duration per task
   - Any errors/warnings
3. Test results (if tests run)
   - Pass/fail counts
   - Failed test names
4. Build output (if compiled)
   - Build success/failure
   - Warnings/errors

**Analyze:**
- Success rate: how many tasks completed?
- Partial completion: 60% complete vs. 100%?
- Error summary: what went wrong?

**Update Memory:**
- Mark vault/session/ phase as "implementing"
- Set completion % based on task success
- Log session entry: "[IMPLEMENTED] X/Y tasks complete"
- Note blockers (failed tasks)

**Report:**
- User-visible summary: "✓ Implementation complete (Y/Y tasks) or ⚠ Partial (X/Y tasks)"
- List of failures (if any)
- Next steps (fix failures or proceed to post)

### Error Handling

**If task fails:**
- Log error
- Continue with remaining tasks (partial completion is valid)
- Report summary of failures

**If git commit fails:**
- Don't block (implementation still succeeded)
- Suggest manual commit

**If multiple tasks fail:**
- Still continue
- Report summary

---

## Enrichment Success Criteria

### Specify Phase
- [x] Context (decisions, patterns) injected into spec generation
- [x] Spec generated and saved to spec.md
- [x] Spec validated for completeness
- [x] Memory updated with progress
- [x] Graceful error handling if core fails

### Plan Phase
- [x] Context + code graph injected into plan generation
- [x] Plan considers existing code structure
- [x] Plan aligns with recent decisions
- [x] Memory updated with progress
- [x] Code reuse is considered

### Implement Phase
- [x] Preconditions validated
- [x] All tasks executed (or partial completion tracked)
- [x] Artifacts collected (code, logs, errors)
- [x] Memory updated with progress
- [x] User informed of completion status

---

## Integration with Context Layer

Each enrichment phase reads from `vault/session/` (created by `/spek.context` at session start). This ensures:

- **Once per session:** Context is loaded once, cached for all phases
- **Consistent:** All phases use the same context
- **Efficient:** No redundant loads or LLM calls
- **Composable:** Each phase can be run independently or as part of the full workflow

See [context-layer.md](context-layer.md) for how context is composed and made available to enrichment phases.

---

## Decorator Pattern (Implementation Notes)

Enrichment is implemented via the decorator pattern:

```
/spek.plan
  └─ Decorator wrapper around SpecKit flow
     ├─ /spek.prepare (context loading, graph validation)
     ├─ Specify Enrichment (wraps /speckit.specify)
     ├─ Plan Enrichment (wraps /speckit.plan)
     ├─ Implement Enrichment (wraps /speckit.implement)
     └─ /spek.conclude (lessons extraction, vault sync)
```

**Key principle:** SpecKit commands are never modified. Enrichment is layered on top:
1. Load context (PRE)
2. Call SpecKit (CORE) with enriched input
3. Validate output (POST)

SpecKit remains independently upgradable; enrichment layer is separate.

---

## Configuration

### .spekificity/config.yaml

```yaml
enrichment:
  # Enable context injection?
  enabled: true
  
  # Which phases to enrich?
  phases:
    specify: true
    plan: true
    implement: true
  
  # Context to inject
  context:
    recent_decisions_count: 5
    recent_patterns_count: 3
    include_code_graph: true
  
  # Validation
  validation:
    check_decision_alignment: true
    check_code_reuse: true
    check_patterns: true
  
  # Error handling
  error_handling:
    fail_on_context_missing: false  # Continue if context unavailable
    fail_on_validation: false       # Continue even if validation fails
```

---

## References

**Related Specs:**
- [context-layer.md](context-layer.md) — Context composition and injection
- [decorator-wrapper-pattern.md](decorator-wrapper-pattern.md) — Wrapper structure
- [memory-architecture.md](memory-architecture.md) — Session memory containing loaded context
- [speckit-integration-contract.md](speckit-integration-contract.md) — Integration contract with SpecKit

*Note: This spec replaces specify-enrichment.md, plan-enrichment.md, and implement-enrichment.md (merged here)*

**External:**
- [SpecKit documentation](https://github.com/github/spec-kit)
