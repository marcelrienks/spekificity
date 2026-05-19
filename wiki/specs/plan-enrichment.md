# ATOMIC SPECIFICATION: Plan Enrichment (C3.4)

**Status:** ATOMIC SPECIFICATION  
**Type:** Integration Layer 2b — /spek.plan Wrapper  
**Depends On:** decorator-wrapper-pattern.md, graph-merge-integration.md  

---

## Overview

`/spek.plan` wraps `/speckit.plan` with context injection (decisions, patterns, code graph, impact analysis) to guide architecture decisions toward project constraints and avoid duplicating existing code.

---

## Execution Sequence

```
/spek.plan
├─ PRE: Load context + code graph
│  ├─ Load decisions + patterns
│  ├─ Query code graph: affected modules, existing code
│  ├─ Analyze impact: what code will change?
│  └─ Output: enriched_context
├─ CORE: Call SpecKit
│  ├─ Inject context + code graph into /speckit.plan prompt
│  ├─ Run /speckit.plan
│  ├─ Capture plan.md
│  └─ Output: plan.md
├─ POST: Validate + Update
│  ├─ Check plan aligns with decisions
│  ├─ Check plan doesn't duplicate existing code
│  ├─ Update /memories/session/current-feature.md
│  └─ Report: plan created
└─ Return: plan.md
```

---

## Pre-Execution: Context + Code Graph Injection

**Context Injection (same as specify):**
- Recent decisions (top 5)
- Recent patterns (top 3)

**Code Graph Injection (NEW):**
1. Read spec.md (identify affected modules)
2. Query vault/graph/nodes.jsonl for affected modules
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

---

## Core Execution

**Command:** `/speckit.plan`

**Input:** spec.md + injected context + code graph

**Model:** Claude Opus (high-quality architecture)
**Temperature:** 0.3
**Max tokens:** 5000

**Output:** plan.md (architecture, design decisions, component breakdown)

---

## Post-Execution: Validation

**Validation Checks:**
1. plan.md exists and is non-empty
2. Architecture is clearly described
3. Design decisions are documented
4. Plan doesn't contradict recent decisions (warn if it does)
5. Plan doesn't duplicate existing code (warn if it does)

**Update Memory:**
- Mark /memories/session/current-feature.md phase as "planning"
- Set completion to 50%
- Log: "[PLANNED] plan.md created"

---

## Error Handling

Same as specify (graceful degradation, fallback template).

---

## Success Criteria

✅ Context + code graph injected into plan generation  
✅ Plan considers existing code structure  
✅ Plan aligns with recent decisions  
✅ Memory updated with progress  

---

## Implementation Checklist

- [ ] Require spec.md to exist (precondition)
- [ ] Query code graph for affected modules
- [ ] Format code structure for injection
- [ ] Call /speckit.plan with enriched context
- [ ] Validate plan against decisions + code graph
- [ ] Update /memories/session/current-feature.md

---

## References

**Related Specs:**
- [specify-enrichment.md](specify-enrichment.md) — Context injection pattern
- [graph-merge-integration.md](graph-merge-integration.md) — Code graph structure
- [architectural-decisions.md](architectural-decisions.md) — Decisions injected

**External:**
- [extracted spec Layer 2b](speckit-integration-contract.md#2c-enriched-plan-spekplan) — Original spec
