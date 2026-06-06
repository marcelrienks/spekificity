# SpecKit Workflow: Quick Reference

SpecKit is the spec-driven development workflow engine that Spekificity wraps and enriches. This page shows the canonical SpecKit flow; for Spekificity integration details and full workflow context, see [workflow.md](workflow.md).

---

## Canonical SpecKit Flow

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

---

## Command Reference

| Command | Purpose | Input | Output | Re-runnable |
|---------|---------|-------|--------|------------|
| `/speckit.constitution` | Define project principles | Developer input | `.specify/memory/constitution.md` | Yes (updates, doesn't break) |
| `/speckit.specify` | Write feature spec | Feature description (what + why) | `specs/NNNN-feature.md` + feature branch | Yes (regenerates from prompt) |
| `/speckit.clarify` | Resolve spec ambiguities | Current spec | Updated spec | Yes |
| `/speckit.plan` | Create implementation plan | Spec + constitution | `plan.md`, `data-model.md`, `contracts/` | Yes (regenerates) |
| `/speckit.tasks` | Generate task list | Plan + data model | `tasks.md` (dependency-ordered) | Yes (regenerates) |
| `/speckit.analyze` | Cross-artifact consistency check | Spec + plan + tasks | Analysis report (ambiguities, gaps, risks) | Yes (non-blocking) |
| (manual remediation) | Fix artifacts in-place | Analyze report | Updated spec/plan/tasks | N/A (manual) |
| `/speckit.implement` | Execute all tasks | Tasks + plan + spec | Generated code | Yes (per-task execution) |

---

## Integration with Spekificity

Spekificity wraps SpecKit phases with context injection and enrichment:

```
/spek.plan (Spekificity wrapper)
    ├─ PRE: Load vault decisions + patterns + code graph (lat.md)
    ├─ CORE: /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze
    └─ POST: Validate output aligns with decisions; flag contradictions

/spek.implement (Spekificity wrapper)
    ├─ PRE: Load decisions + patterns + code graph
    ├─ CORE: /speckit.implement (per-task execution)
    └─ POST: Collect diff; validate against spec; log decisions
```

For detailed workflow including preparation, conclusion, and lessons extraction, see [workflow.md](workflow.md).

---

## Key Clarifications

**Analyze Output:** Non-blocking; `/speckit.analyze` identifies gaps but doesn't prevent `/speckit.implement`.

**Remediation:** Manual in-place editing (no automatic regeneration loop). After fixing, optionally re-run `/speckit.analyze` to verify.

**SpecKit Vanilla vs Spekificity:**
- Use `/speckit.*` directly for raw SpecKit workflow (no enrichment)
- Use `/spek.plan` and `/spek.implement` for Spekificity enriched workflow (context injection + validation)

---

## Resources

- **Full Workflow Guide:** [workflow.md](workflow.md)
- **SpecKit Official Docs:** https://github.com/github/spec-kit/
- **Design Decisions:** [decision.md](decision.md)
