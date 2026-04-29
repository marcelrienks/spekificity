# Workflow: Enriched SpecKit Feature Lifecycle

## Purpose

The complete Spekificity-enriched SpecKit feature lifecycle. Each SpecKit step is decorated with graph-aware context from the Obsidian vault, and lessons are automatically persisted at the end. Use this workflow for every feature in a Spekificity-enabled project.

> **Token efficiency**: See the [Token Efficiency](#token-efficiency) section for Caveman invocation guidance at each step.

## Prerequisites

- Spekificity initialised (see [init-workflow.md](init-workflow.md))
- Vault graph built (`vault/graph/index.md` exists) — if not, run [map-refresh.md](map-refresh.md) first
- SpecKit installed (`specify --version` succeeds)
- AI agent session open (GitHub Copilot or Claude Code)

---

## Decision: Is the vault mapped?

```
vault/graph/index.md exists?
├── YES → proceed to Step 1
└── NO  → run /map-codebase first (see workflows/map-refresh.md), then return here
```

---

## Step 1 — Load Context

**Skill**: `/context-load` (see [skills/context-load/SKILL.md](../skills/context-load/SKILL.md))  
**Input**: none (reads vault automatically)  
**Output**: AI working memory primed with graph, decisions, patterns, recent lessons

```
/context-load
```

**Expected state after step 1**: AI confirms "Context loaded. [N] graph nodes, [M] decisions, [K] patterns. Ready."

**On failure**: If vault is missing, run init workflow Step 5. If vault is empty, proceed — context-load continues gracefully.

---

## Step 2 — Write the Spec (Graph-Aware)

**Skill**: `/speckit-enrich-specify` (see [skills/speckit-enrich/specify-enrich.md](../skills/speckit-enrich/specify-enrich.md))  
**Input**: Feature description (your words)  
**Output**: `specs/<feature-dir>/spec.md` enriched with graph cross-references

```
/speckit-enrich-specify
```

Provide your feature description when prompted. The skill enriches it with related graph nodes before passing it to `/speckit.specify`.

**Expected state after step 2**: `specs/<feature-dir>/spec.md` exists and contains related component references in Assumptions.

**On failure**: If graph enrichment fails, SpecKit still runs. Check `spec.md` for completeness.

---

## Step 3 — Write the Plan (Graph-Aware)

**Skill**: `/speckit-enrich-plan` (see [skills/speckit-enrich/plan-enrich.md](../skills/speckit-enrich/plan-enrich.md))  
**Input**: Current `spec.md` (read automatically)  
**Output**: `specs/<feature-dir>/plan.md` with impacted graph nodes in Technical Context

```
/speckit-enrich-plan
```

**Expected state after step 3**: `specs/<feature-dir>/plan.md` exists and Technical Context lists impacted graph nodes.

**On failure**: If plan enrichment fails, SpecKit still runs. Manually review plan for missing component references.

---

## Step 4 — Generate Tasks

**Skill**: `/speckit.tasks` (standard SpecKit — no Spekificity enrichment needed)  
**Input**: `spec.md` and `plan.md` (read automatically by SpecKit)  
**Output**: `specs/<feature-dir>/tasks.md`

```
/speckit.tasks
```

**Expected state after step 4**: `specs/<feature-dir>/tasks.md` exists with a complete, dependency-ordered task list.

---

## Step 5 — Implement (Graph-Aware, with Auto Lessons + Map)

**Skill**: `/speckit-enrich-implement` (see [skills/speckit-enrich/implement-enrich.md](../skills/speckit-enrich/implement-enrich.md))  
**Input**: `tasks.md` (read automatically)  
**Output**: All tasks completed + lessons entry written + vault graph updated

```
/speckit-enrich-implement
```

This skill automatically invokes `/lessons-learnt` and `/map-codebase` when implementation completes.

**Expected state after step 5**: All tasks `[X]`; `vault/lessons/<date>-<slug>.md` exists; `vault/graph/index.md` timestamp is current.

**On failure mid-task**: SpecKit will report the failing task. Resolve it, then continue with `/speckit.implement` (standard). When complete, manually run `/lessons-learnt` and `/map-codebase`.

---

## Step 6 — Verify Lessons and Graph

After step 5, confirm:

```bash
ls vault/lessons/       # should contain a new entry for this feature
cat vault/graph/index.md | head -10  # last_updated should be today
```

In your AI session:
```
/context-load
# Verify the new lessons entry appears in the summary
```

---

## Step 7 — (Optional) Archive or Close Feature

Standard git workflow:
```bash
git add -A
git commit -m "feat(001-feature-name): implement feature"
git push
# Open PR / merge
```

---

## Full Sequence Summary

```
Session start
    │
    ▼
/context-load                        ← Step 1: Load vault context
    │
    ▼
/speckit-enrich-specify              ← Step 2: Write spec (graph-aware)
    │
    ▼
/speckit-enrich-plan                 ← Step 3: Write plan (graph-aware)
    │
    ▼
/speckit.tasks                       ← Step 4: Generate tasks (standard SpecKit)
    │
    ▼
/speckit-enrich-implement            ← Step 5: Implement + auto-lessons + auto-map
    │                   │
    │              /lessons-learnt   ← auto-invoked at completion
    │              /map-codebase     ← auto-invoked at completion
    ▼
Feature complete
```

---

## Recovery Instructions

| Failure point | Recovery action |
|---------------|----------------|
| Step 1 — vault missing | Run `workflows/init-workflow.md` Step 5 |
| Step 1 — vault empty | Proceed; context-load is graceful with empty vault |
| Step 2 — spec enrichment fails | Run `/speckit.specify` directly; manually add graph refs |
| Step 3 — plan enrichment fails | Run `/speckit.plan` directly; manually add impacted nodes |
| Step 4 — task generation fails | Check `spec.md` and `plan.md` exist; re-run `/speckit.tasks` |
| Step 5 — task fails mid-way | Fix the failing task; re-run `/speckit.implement`; run `/lessons-learnt` manually |
| Step 5 — `/lessons-learnt` fails | Run `/lessons-learnt` manually after implementation |
| Step 5 — `/map-codebase` fails | Run `/map-codebase` manually after implementation |

---

## Token Efficiency

See notes at each step for Caveman recommendations. Summary:

| Step | Recommended Caveman mode | Why |
|------|--------------------------|-----|
| Step 1 (context-load) | `/caveman lite` | Structured summary output — lite avoids over-compression |
| Step 2 (specify) | `/caveman lite` | Spec requires structured content — lite preserves formatting |
| Step 3 (plan) | `/caveman lite` | Same as specify |
| Step 4 (tasks) | `/caveman lite` | Task list format must stay precise |
| Step 5 (implement) | `/caveman` (full) | Implementation narration benefits from full compression |
| Step 6 (verify) | off or `/caveman lite` | Short verification step |

Activate at session start:
```
/caveman lite
```

Switch to full mode before implementation:
```
/caveman
```
