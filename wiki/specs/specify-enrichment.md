# ATOMIC SPECIFICATION: Specify Enrichment (C3.3)

**Status:** ATOMIC SPECIFICATION  
**Type:** Integration Layer 2a — /spek.specify Wrapper  
**Depends On:** cdecorator-wrapper-pattern.md, ccontext-layer.md  
**Used By:** User workflow (after /spek.prepare)  

---

## Overview

`/spek.specify` wraps SpecKit's `/speckit.specify` command with context injection (decisions, patterns) to guide spec generation toward existing project constraints.

---

## Execution Sequence

```
/spek.specify [feature-description]
├─ PRE: Load context
│  ├─ Read /memories/session/context-loaded.md
│  ├─ Extract decisions + patterns
│  ├─ Construct enrichment prompt
│  └─ Output: enriched_context (string)
├─ CORE: Call SpecKit
│  ├─ Inject context into /speckit.specify prompt
│  ├─ Run /speckit.specify [feature-description]
│  ├─ Capture spec.md output
│  └─ Output: spec.md (created)
├─ POST: Validate + Update
│  ├─ Validate spec is well-formed
│  ├─ Check spec doesn't violate recent decisions
│  ├─ Update /memories/session/current-feature.md
│  └─ Output: Completion report
└─ Return: spec.md location + validation results
```

---

## Pre-Execution: Context Injection

**Process:**
1. Load decisions + patterns from /memories/session/context-loaded.md
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

---

## Core Execution

**Command:** `/speckit.specify [enriched-feature-description]`

**Process:**
- SpecKit reads feature description (with injected context)
- SpecKit reads constitution.md (if exists)
- SpecKit calls Claude model
- Claude generates spec.md

**Model Settings:**
- Model: Claude Opus (for high-quality spec)
- Temperature: 0.3 (consistent + focused)
- Max tokens: 4000

**Output:** spec.md (created in current directory)

---

## Post-Execution: Validation

**Validation Checks:**
1. spec.md exists and is non-empty
2. Markdown is well-formed (parseable)
3. Required sections present (requirements, acceptance criteria)
4. Spec doesn't contradict recent decisions (warn if it does)

**Update Memory:**
- Mark /memories/session/current-feature.md phase as "specifying"
- Set completion to 25%
- Add session log entry: "[SPECIFIED] spec.md created"

**Output:**
- Completion report: "✓ Spec created. Phase: specifying (25% complete)"

---

## Error Handling

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

## Success Criteria

✅ Context (decisions, patterns) injected into spec generation  
✅ Spec generated and saved to spec.md  
✅ Spec validated for completeness  
✅ Memory updated with progress  
✅ Graceful error handling if core fails  

---

## Implementation Checklist

- [ ] Load context from /memories/session/context-loaded.md
- [ ] Format decisions + patterns for injection
- [ ] Call /speckit.specify with injected context
- [ ] Validate spec.md output
- [ ] Check spec doesn't violate recent decisions
- [ ] Update /memories/session/current-feature.md
- [ ] Test with context available and unavailable

---

## References

**Related Specs:**
- [cdecorator-wrapper-pattern.md](cdecorator-wrapper-pattern.md) — Wrapper structure
- [ccontext-layer.md](ccontext-layer.md) — Context loading
- [ccontext-load-lifecycle.md](ccontext-load-lifecycle.md) — What context contains

**External:**
- [extracted spec Layer 2a](speckit-integration-contract.md#2b-enriched-specify-spekspecify) — Original spec
