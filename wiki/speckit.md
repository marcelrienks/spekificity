---
title: speckit
type: guide
tags: []
---

# The Full SpecKit Workflow (B.1 Resolution)

## Canonical SpecKit Flow

```
/speckit.constitution
    ↓
/speckit.specify
    ↓
/speckit.clarify (optional; recommended before plan)
    ↓
/speckit.plan
    ↓
/speckit.tasks
    ↓
/speckit.analyze (optional; recommended after tasks, before implement)
    ↓
[FIX ARTIFACTS IN-PLACE IF NEEDED]
    ↓
/speckit.implement
    ↓
[FEATURE COMPLETE]
```

---

## Command Descriptions

### 1. `/speckit.constitution` — Establish Project Principles
**Input:** Developer defines project principles  
**Output:** `.specify/memory/constitution.md`  
**Purpose:** Create the architectural DNA governing all development  
**When to run:** Once per project, or when principles need revision  
**Can run again?** Yes; updates constitution without breaking dependent specs

---

### 2. `/speckit.specify` — Define What to Build
**Input:** Feature description (what + why, not how)  
**Output:**
- Auto-generated feature branch (e.g., `003-chat-system`)
- `specs/[feature]/spec.md` with structured requirements, user stories, acceptance criteria
- Automatic feature numbering

**Purpose:** Create executable specification; focus on requirements, not technology  
**Can run again?** Yes; re-running regenerates spec.md from the prompt. If you've edited spec.md directly, re-running will overwrite your edits (use with caution)

---

### 3. `/speckit.clarify` — Resolve Ambiguities (Optional)
**Input:** Reads current spec.md  
**Output:** Updated spec.md with clarifications  
**Purpose:** Identify and resolve underspecified areas before planning  
**Recommended?** Yes, before `/speckit.plan` to catch gaps early  
**Can run again?** Yes

---

### 4. `/speckit.plan` — Create Technical Implementation Plan
**Input:**
- `spec.md` (required)
- Project constitution

**Output:**
- `plan.md` (architecture, tech choices, rationale)
- `data-model.md` (entity definitions, schemas)
- `contracts/` (API contracts, data schemas, WebSocket events)
- `quickstart.md` (key validation scenarios)

**Purpose:** Translate business requirements into technical architecture  
**Constitutional gates:** Phase -1 gates enforce Simplicity (small project set) and Anti-Abstraction (direct framework use)  
**Can run again?** Yes; regenerates plan artifacts. Use with caution if you've edited them directly.

---

### 5. `/speckit.tasks` — Generate Executable Task List
**Input:**
- `plan.md` (required)
- `data-model.md` (if present)
- `contracts/` (if present)

**Output:** `tasks.md` with:
- Dependency-ordered tasks
- Parallelizable tasks marked `[P]`
- Safe parallel groupings
- Test-first task ordering (contract tests → integration → e2e → unit)

**Purpose:** Convert architecture into executable work  
**Can run again?** Yes; regenerates tasks.md from plan

---

### 6. `/speckit.analyze` — Cross-Artifact Consistency Check (Optional)
**Input:**
- `spec.md`
- `plan.md`
- `tasks.md`

**Output:** Analysis report identifying:
- Ambiguities in spec
- Contradictions between spec and plan
- Gaps in coverage
- Missing acceptance criteria
- Incomplete test plans

**Purpose:** Quality gate before implementation; catch issues early  
**Timing:** Recommended after `/speckit.tasks`, before `/speckit.implement`  
**Non-blocking?** Yes; issues identified but implementation can proceed

---

### 7. [REMEDIATION] — Fix Artifacts In-Place
**What:** Developer manually edits artifacts in response to analyze report  
**Where:** Edit `spec.md`, `plan.md`, `tasks.md`, or supporting documents directly  
**Mechanism:** No command; direct file editing  
**Re-entry:** After fixes, optionally re-run `/speckit.analyze` to verify improvements

**Workflow Decision:**
- **Analyze identifies issues** → You read the report
- **You edit artifacts directly** (in-place) to fix issues
- **Continue to implement** (no automatic regeneration loop)
- **Optional:** Re-run analyze if you made structural changes to verify; else proceed

---

### 8. `/speckit.implement` — Execute All Tasks
**Input:**
- `tasks.md`
- `plan.md`
- `spec.md`

**Output:** Generated code implementing all tasks  
**Prerequisites:**
- `tasks.md` must exist
- No explicit requirement for a clean analyze pass (optional, not mandatory)
- Recommended: address obvious analyze issues first, but not required

**Purpose:** Execute all tasks and build the feature according to the plan  
**Test-first enforced:** Article III mandates tests before implementation

---

## Key Clarifications for B.1

### Q1: Does remediation happen in-place or via re-run?
**A:** In-place. You edit `spec.md`, `plan.md`, `tasks.md` directly in response to `/speckit.analyze` report. No automatic re-generation.

### Q2: What does the full canonical flow look like?
**A:** Constitution → Specify → Clarify (optional) → Plan → Tasks → Analyze (optional) → [Fix in-place] → Implement

### Q3: Are there re-entry points?
**A:** No automatic re-entry, but optional re-runs are safe:
- `/speckit.analyze` can be re-run after fixing to verify improvements
- Each command (specify, plan, tasks) can be re-run to regenerate from upstream; use with caution if you've edited artifacts directly

### Q4: Does implement expect a clean analyze pass?
**A:** No. `/speckit.analyze` is optional and non-blocking. Implement can run regardless of analyze findings. However, best practice: address high-severity issues from analyze before implementing.

---

## Spekificity Integration: How Enrich-* Skills Fit

```
/spek.plan
    ↓ (loads context and orchestrates upstream SpecKit flow)
/speckit.specify
    ↓
/speckit.clarify (optional)
    ↓
/speckit.plan
    ↓
/speckit.analyze (optional)
    ↓
[REMEDIATE IN-PLACE IF NEEDED]
    ↓
/speckit.tasks
    ↓
/spek.implement
    ↓ (execute approved tasks with code map + spec + plan in scope)
/spek.conclude or lessons flow
    ↓ (capture feature summary + decisions + patterns)
```

**Key design:** Spekificity does not expose separate wrapper commands for every SpecKit phase. `spek.plan` owns spec-through-task orchestration; `spek.implement` stays separate so execution happens only after review.

---

## For `spek plan` Implementation

**Canonical sequencing (B.1 resolved):**

1. **Pre-flight:** Clean working tree, create feature branch
2. **Plan:** `/spek.plan` loads context (vault + doc index + code graph) and runs `/speckit.specify` → `/speckit.clarify` (optional) → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` (optional) → remediation loop
3. **Review & Fix:** Developer reviews analyze report and generated artifacts, edits in-place if needed (manual step)
4. **Implement:** `/spek.implement` with code map context
5. **Post-flight:** `/spek.conclude` writes outcomes to vault, graph refresh

**Context Loading:** `/spek.context` loads three independent indices:
- Obsidian vault (Layer 1 persistent memory)
- Documentation index (independent graph of all project docs)
-- lat.md (independent index of source code)

**Decision:** Analyze is **optional and non-blocking**. If findings are minor, skip remediation and proceed to implement. High-severity issues should be addressed before implement.

---

## References

- [SpecKit Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [SpecKit CLI Reference](https://github.github.io/spec-kit/reference/overview.html)
- [Core Commands Reference](https://github.github.io/spec-kit/reference/core.html)
