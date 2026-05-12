# workflow: enriched speckit feature lifecycle

## purpose

the complete spekificity-enriched speckit feature lifecycle. each speckit step is decorated with graph-aware context from the obsidian vault, and lessons are automatically persisted at the end. use this workflow for every feature in a spekificity-enabled project.

> **token efficiency**: see the [token efficiency](#token-efficiency) section for caveman invocation guidance at each step.

## prerequisites

- spekificity initialised (see [init-workflow.md](init-workflow.md))
- vault graph built (`vault/graph/index.md` exists) — if not, run [map-refresh.md](map-refresh.md) first
- speckit installed (`specify --version` succeeds)
- ai agent session open (github copilot or claude code)

---

## decision: is the vault mapped?

```
vault/graph/index.md exists?
├── yes → proceed to step 1
└── no  → run /map-codebase first (see workflows/map-refresh.md), then return here
```

---

## step 1 — load context

**skill**: `/context-load` (see [skills/context-load/skill.md](../skills/context-load/skill.md))  
**input**: none (reads vault automatically)  
**output**: ai working memory primed with graph, decisions, patterns, recent lessons

```
/context-load
```

**expected state after step 1**: ai confirms "context loaded. [n] graph nodes, [m] decisions, [k] patterns. ready."

**on failure**: if vault is missing, run init workflow step 5. if vault is empty, proceed — context-load continues gracefully.

---

## step 2 — write the spec (graph-aware)

**skill**: `/speckit-enrich-specify` (see [skills/speckit-enrich/specify-enrich.md](../skills/speckit-enrich/specify-enrich.md))  
**input**: feature description (your words)  
**output**: `specs/<feature-dir>/spec.md` enriched with graph cross-references

```
/speckit-enrich-specify
```

provide your feature description when prompted. the skill enriches it with related graph nodes before passing it to `/speckit.specify`.

**expected state after step 2**: `specs/<feature-dir>/spec.md` exists and contains related component references in assumptions.

**on failure**: if graph enrichment fails, speckit still runs. check `spec.md` for completeness.

---

## step 3 — write the plan (graph-aware)

**skill**: `/speckit-enrich-plan` (see [skills/speckit-enrich/plan-enrich.md](../skills/speckit-enrich/plan-enrich.md))  
**input**: current `spec.md` (read automatically)  
**output**: `specs/<feature-dir>/plan.md` with impacted graph nodes in technical context

```
/speckit-enrich-plan
```

**expected state after step 3**: `specs/<feature-dir>/plan.md` exists and technical context lists impacted graph nodes.

**on failure**: if plan enrichment fails, speckit still runs. manually review plan for missing component references.

---

## step 4 — generate tasks

**skill**: `/speckit.tasks` (standard speckit — no spekificity enrichment needed)  
**input**: `spec.md` and `plan.md` (read automatically by speckit)  
**output**: `specs/<feature-dir>/tasks.md`

```
/speckit.tasks
```

**expected state after step 4**: `specs/<feature-dir>/tasks.md` exists with a complete, dependency-ordered task list.

---

## step 5 — implement (graph-aware, with auto lessons + map)

**skill**: `/speckit-enrich-implement` (see [skills/speckit-enrich/implement-enrich.md](../skills/speckit-enrich/implement-enrich.md))  
**input**: `tasks.md` (read automatically)  
**output**: all tasks completed + lessons entry written + vault graph updated

```
/speckit-enrich-implement
```

this skill automatically invokes `/lessons-learnt` and `/map-codebase` when implementation completes.

**expected state after step 5**: all tasks `[x]`; `vault/lessons/<date>-<slug>.md` exists; `vault/graph/index.md` timestamp is current.

**on failure mid-task**: speckit will report the failing task. resolve it, then continue with `/speckit.implement` (standard). when complete, manually run `/lessons-learnt` and `/map-codebase`.

---

## step 6 — verify lessons and graph

after step 5, confirm:

```bash
ls vault/lessons/       # should contain a new entry for this feature
cat vault/graph/index.md | head -10  # last_updated should be today
```

in your ai session:
```
/context-load
# verify the new lessons entry appears in the summary
```

---

## step 7 — (optional) archive or close feature

standard git workflow:
```bash
git add -a
git commit -m "feat(001-feature-name): implement feature"
git push
# open pr / merge
```

---

## full sequence summary

```
session start
    │
    ▼
/context-load                        ← step 1: load vault context
    │
    ▼
/speckit-enrich-specify              ← step 2: write spec (graph-aware)
    │
    ▼
/speckit-enrich-plan                 ← step 3: write plan (graph-aware)
    │
    ▼
/speckit.tasks                       ← step 4: generate tasks (standard speckit)
    │
    ▼
/speckit-enrich-implement            ← step 5: implement + auto-lessons + auto-map
    │                   │
    │              /lessons-learnt   ← auto-invoked at completion
    │              /map-codebase     ← auto-invoked at completion
    ▼
feature complete
```

---

## recovery instructions

| failure point | recovery action |
|---------------|----------------|
| step 1 — vault missing | run `workflows/init-workflow.md` step 5 |
| step 1 — vault empty | proceed; context-load is graceful with empty vault |
| step 2 — spec enrichment fails | run `/speckit.specify` directly; manually add graph refs |
| step 3 — plan enrichment fails | run `/speckit.plan` directly; manually add impacted nodes |
| step 4 — task generation fails | check `spec.md` and `plan.md` exist; re-run `/speckit.tasks` |
| step 5 — task fails mid-way | fix the failing task; re-run `/speckit.implement`; run `/lessons-learnt` manually |
| step 5 — `/lessons-learnt` fails | run `/lessons-learnt` manually after implementation |
| step 5 — `/map-codebase` fails | run `/map-codebase` manually after implementation |

---

## token efficiency

see notes at each step for caveman recommendations. summary:

| step | recommended caveman mode | why |
|------|--------------------------|-----|
| step 1 (context-load) | `/caveman lite` | structured summary output — lite avoids over-compression |
| step 2 (specify) | `/caveman lite` | spec requires structured content — lite preserves formatting |
| step 3 (plan) | `/caveman lite` | same as specify |
| step 4 (tasks) | `/caveman lite` | task list format must stay precise |
| step 5 (implement) | `/caveman` (full) | implementation narration benefits from full compression |
| step 6 (verify) | off or `/caveman lite` | short verification step |

activate at session start:
```
/caveman lite
```

switch to full mode before implementation:
```
/caveman
```
