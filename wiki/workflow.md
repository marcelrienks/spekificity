# Feature Development Workflow

## Overview

Spekificity implements a deterministic, 4-stage feature development workflow:

- **Prepare** – Initialize third-party tools (lat.md code + doc indexes, Obsidian vault) and load context
- **Plan** – Orchestrate SpecKit: specify → plan → tasks (with remediations)
- **Implement** – Execute tasks via SpecKit implement
- **Conclude** – All post-implementation: analysis, lessons, vault archive, state refresh

**All stages are agent skills, not CLI commands.** Run them inside your agent (Claude Code, Copilot, etc.). Only `spek init` is a CLI command.

**Artifacts stored in `.spek/vault/`** (not `vault/` at project root).

---

## Preparation

### Command
```
/spek.prepare
```

### Purpose
Initialize all third-party tools and load context before feature development. `/spek.prepare` does not just check workspace state — it actively builds and stores the indexes that all subsequent skills depend on.

### Sub-steps

| Step | Action | Output |
|------|--------|--------|
| lat.md Code Index | Initialize/refresh lat.md index of source code (symbols, definitions, call graphs) | Code index ready in `.spek/lat/` |
| lat.md Doc Index | Initialize/refresh lat.md index of documentation (wiki, vault, markdown files) — **separate index** | Doc index ready in `.spek/lat/` |
| Vault Storage | Store both indexes in Obsidian vault (`.spek/vault/`) for persistent context | Indexes persisted |
| Context Load | Load vault decisions, patterns, prior lessons into agent session | Session context ready |
| Constitution Check | Verify `.specify/memory/constitution.md` exists. If missing, invoke `/speckit.constitution` to create it (one-time, interactive). Constitution defines project principles SpecKit embeds into all spec/plan generation. | Constitution present |

**Why two separate indexes:** Code index answers "where is X defined / what calls it." Doc index answers "what decisions or patterns relate to topic X." Merging them degrades both queries.

### Output Artifacts
- lat.md code index (fresh, stored in `.spek/lat/`)
- lat.md doc index (fresh, stored in `.spek/lat/`)
- Vault context loaded (decisions, patterns, lessons in agent session)
- Project constitution verified

### Exit Criteria
- ✅ lat.md code index initialized and current
- ✅ lat.md doc index initialized and current
- ✅ Vault context loaded into session
- ✅ Constitution exists

---

## Plan

### Command
```
/spek.plan [feature-name]
```

### Purpose
Orchestrate full SpecKit planning pipeline in sequence, with user review and remediation at each step.

### Workflow

```
FEATURE INTENT
    ↓
STEP 1: /speckit.specify
    ├─ Generate spec (what, why, scope, success criteria)
    ├─ Query lat.md doc index for related decisions + patterns
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run step 1]
STEP 2: /speckit.plan
    ├─ Generate implementation plan from approved spec
    ├─ Query lat.md code index for affected areas
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run step 2 (or step 1 if spec was wrong)]
STEP 3: /speckit.tasks
    ├─ Break plan into dependency-ordered executable tasks
    └─ Surface to user for approval
    ↓ [if remediation needed: fix + re-run from affected step]
COMPLETE: spec.md + plan.md + tasks.md (stored where SpecKit dictates; archived to .spek/vault/ via Obsidian)
```

**Remediation loop:** After each step, surface output to user. If user requests changes, apply and reprocess from that step forward. Continue until all three outputs are approved.

### Output Artifacts
- `spec.md` — Feature specification with success criteria (SpecKit manages path; archived to `.spek/vault/` via Obsidian)
- `plan.md` — Architecture, tech choices, affected code areas (SpecKit manages path; archived to `.spek/vault/` via Obsidian)
- `tasks.md` — Dependency-ordered tasks with IDs (SpecKit manages path; archived to `.spek/vault/` via Obsidian)

### Exit Criteria
- ✅ Spec approved by user
- ✅ Plan approved by user
- ✅ Task list approved by user
- ✅ All artifacts archived to `.spek/vault/` via Obsidian CLI

---

## Implementation

### Command
```
/spek.implement [--steps N]
```

### Purpose
Execute approved tasks by wrapping `/speckit.implement`. `/spek.implement` is intentionally thin — it loads context (spec, plan, tasks from `.spek/vault/`) then delegates execution entirely to SpecKit.

### Workflow

```
LOAD context from .spek/vault/ (spec + plan + tasks)
    ↓
/speckit.implement
    ├─ Executes all tasks in dependency order
    ├─ SpecKit owns per-task execution, code generation, step tracking
    └─ Use --steps N to jump to a specific task (resume)
    ↓
IMPLEMENTATION COMPLETE
```

SpecKit handles all per-task detail (code writing, test running, commits). Spekificity's role is context loading before the call, not wrapping each step.

### Implementation Context

Each task execution includes:

| Context | Source | Purpose |
|---------|--------|---------|
| **Feature Spec** | `.spek/vault/` (Obsidian) | Why are we doing this? Success Criteria? |
| **Task Definition** | SpecKit plan output | What exactly does this task do? |
| **lat.md** | Live analysis | What files need to change? Who calls what? |
| **Risk Assessment** | Plan + Spec | What could fail? How to mitigate? |
| **Previous Outcomes** | Vault (updated) | What did earlier tasks create? |

### Implementation Checklist (Per Task)

- [ ] Load task context from plan
- [ ] Read Success Criteria for this task
- [ ] Query lat.md for affected symbols/files
- [ ] Write code (implementation)
- [ ] Add docstrings to new functions/classes
- [ ] Write tests (or extend existing tests)
- [ ] Run tests locally (must pass)
- [ ] Validate against Success Criteria
- [ ] Commit with message `[Task X] description` (e.g., `[Task 1] Auth service token validation`)
- [ ] Update plan document: mark task complete + document outcome
- [ ] Document any lessons learned or blockers

### Output Artifacts (Per Task)
- Committed code changes (with task ID in commit message)
- Tests passing locally
- Updated plan document with task outcome
- Task-level lessons learned (stored in plan or vault)

### Exit Criteria (All Tasks)
- ✅ All tasks completed (in dependency order)
- ✅ All tests passing locally
- ✅ Success Criteria validated for each task
- ✅ Code committed with task references
- ✅ Plan marked as "Implementation Complete"

## Conclude: Feature Conclusion

### Command
```
/spek.conclude
```

### Purpose
All post-implementation functions. `/spek.conclude` is the only conclude command — it handles analysis, lessons, vault archive, and state refresh in a single skill. `/spek.lessons` is called as a sub-step inside conclude; it can also be invoked independently at any point.

### Workflow

```
IMPLEMENTATION COMPLETE
    ↓
/spek.conclude
    │
    ├─ 1. Analysis
    │  └─ /speckit.analyze — validate implementation against spec
    │     ├─ Compare Success Criteria vs actual outcomes
    │     └─ Flag spec drift or deviations
    │
    ├─ 2. Lessons (sub-step: /spek.lessons)
    │  ├─ Prompt for retrospective (what worked, what was difficult)
    │  ├─ Extract new patterns if workflow diverged from spec
    │  ├─ Log new decisions if architecture changed
    │  ├─ Write lessons to .spek/vault/lessons/YYYY-MM-DD-feature-name.md
    │  └─ Autolink enrichment: wikilinks + tags inserted into lesson file
    │
    ├─ 3. Backprop Reflex
    │  ├─ Parse test failure output from last test run
    │  ├─ Append ⚠ blockquotes to .spek/vault/patterns.md for new failures
    │  └─ Skip if no test failures (idempotent)
    │
    ├─ 4. Vault Archive
    │  ├─ Archive spec + plan + tasks to .spek/vault/
    │  ├─ Update .spek/vault/patterns.md with new patterns
    │  └─ Update .spek/vault/decisions.md with new decisions
    │
    ├─ 5. Token Budget Summary
    │  ├─ Summarize total token usage for feature
    │  └─ Print [WARN] if usage exceeds token_budget.per_feature; skip if null
    │
    ├─ 6. State Refresh
    │  ├─ lat init — refresh lat.md index (reflects committed code)
    │  └─ Sync repo memory to .spek/memory/
    │
    ├─ 7. Commit
    │  ├─ git add .spek/vault/ .spek/memory/
    │  └─ git commit
    │
    ├─ 8. Blind Review (optional)
    │  └─ /spek.blind-review — context-free quality pass before archiving
    │
    └─ 9. RARV (optional)
       └─ /spek.rarv — detect and resolve spec drift
    ↓
FEATURE ARCHIVED, LESSONS CAPTURED, READY FOR NEXT FEATURE
```

### Lessons Template

Lessons stored at `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`:

```markdown
## Feature: [Feature Name]
Date: YYYY-MM-DD
Status: Complete

### What went well
- [pattern/approach/tool that worked]

### What was difficult
- [challenge/blocker]
- [mitigation used]

### Patterns discovered
- [reusable pattern]
- [architectural insight]

### Recommendations for future
- [suggestion for similar features]
- [process improvement]

### Linked Artifacts
- Spec: [link to spec in .spek/vault/]
- Plan: [link to plan in .spek/vault/]
- Decisions Made: [link to decision entries]
- Pull Requests: [GitHub PR links]
```

### Output Artifacts
- Analysis report (spec drift, outcomes vs criteria)
- Lessons document (`.spek/vault/lessons/YYYY-MM-DD-feature-name.md`)
- Archived spec + plan + tasks (`.spek/vault/`)
- Updated patterns + decisions (`.spek/vault/`)
- Backprop warnings in `.spek/vault/patterns.md` (or none if no failures)
- lat.md index refreshed (code)
- Repo memory synced (`.spek/memory/`)

### Exit Criteria
- ✅ Analysis complete (spec drift documented)
- ✅ Lessons extracted and committed to vault
- ✅ Failure patterns from test run captured in vault (or none found)
- ✅ Feature artifacts archived
- ✅ Token usage summarized
- ✅ lat.md index refreshed
- ✅ Repo memory updated
- ✅ Vault changes committed to git

## Error Handling & Recovery

### Spec Issues
- **Problem:** Spec is ambiguous or incomplete
- **Recovery:** Return to step 1 of `/spek.plan`; revise and re-run `/speckit.specify`
- **Outcome:** Updated spec document

### Plan Issues
- **Problem:** Task dependencies incorrect or blocking
- **Recovery:** Return to step 2 of `/spek.plan`; revise and re-run `/speckit.plan`
- **Outcome:** Revised plan document

### Implementation Failure
- **Problem:** Task fails Success Criteria or tests fail
- **Recovery:** Re-run `/spek.implement [--steps N]` to resume from the failing task
- **Outcome:** Code correction + test validation

### Obsidian CLI Not Registered
- **Problem:** `spek init` exits with code 2 (Obsidian installed but CLI not registered)
- **Recovery:** Open Obsidian → Settings → General → Enable CLI; restart terminal; re-run `spek init`
- **Outcome:** Init completes; vault initialized

### Lessons Not Captured
- **Problem:** `/spek.conclude` completes but lessons are shallow
- **Recovery:** Run `/spek.lessons` standalone and provide a more detailed retrospective
- **Outcome:** Richer lessons in vault

---

## Cross-Phase Context Reuse

```
Spec defines WHAT + WHY
    ↓ (used by)
Plan breaks into tasks + HOW
    ↓ (used by)
Implementation executes per task + VALIDATES against spec
    ↓ (used by)
Lessons capture WHAT WORKED + WHAT DIDN'T
    ↓ (reused in)
Next Feature Spec (pattern reference) + Next Feature Plan (estimate refinement)
```

---

## SpecKit Workflow Reference

SpecKit is the spec-driven development workflow engine that Spekificity wraps and enriches. This section shows the canonical SpecKit flow; for Spekificity integration details and full workflow context, see the main workflow section above.

### Canonical SpecKit Flow

```
/speckit.constitution
    ↓
/speckit.specify
    ↓
/speckit.clarify (optional)
    ↓
/speckit.plan
    ↓
/speckit.tasks
    ↓
/speckit.analyze (optional)
    ↓
[FIX ARTIFACTS IN-PLACE IF NEEDED]
    ↓
/speckit.implement
    ↓
[FEATURE COMPLETE]
```

### SpecKit + Spekificity Integration

Spekificity wraps SpecKit. The relationship:

```
/spek.plan
    ├─ Calls /speckit.specify (step 1, with user review + remediation loop)
    ├─ Calls /speckit.plan    (step 2, with user review + remediation loop)
    └─ Calls /speckit.tasks   (step 3, with user review + remediation loop)
    NOTE: /speckit.clarify and /speckit.analyze are NOT called automatically

/spek.implement
    └─ Calls /speckit.implement (delegates execution entirely)

/spek.conclude
    ├─ Calls /speckit.analyze  (step 1, analysis)
    └─ Calls /spek.lessons     (step 2, as sub-step — also callable standalone)
```

### Key Clarifications

**`/speckit.clarify` is optional:** Call it manually if spec ambiguities need resolution. `/spek.plan` does not auto-invoke it.

**`/speckit.analyze` is called by `/spek.conclude`:** Not by `/spek.plan`. It validates the completed implementation, not the plan.

**`/spek.lessons` is standalone AND auto-called:** It runs as step 2 inside `/spek.conclude`, but can also be invoked independently at any point to capture lessons mid-feature or re-run extraction after conclude.

**SpecKit Vanilla vs Spekificity:**
- `/speckit.*` directly: raw SpecKit, no enrichment, no vault context
- `/spek.*`: Spekificity wrapper — loads vault context, drives user approval loops, persists to `.spek/vault/`

