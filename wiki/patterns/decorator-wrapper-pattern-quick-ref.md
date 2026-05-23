# Decorator Wrapper Pattern — Quick Reference

**Category:** Architectural  
**Problem:** Extend SpecKit functionality without modifying internals  
**Solution:** Pre-Execution → Core → Post-Execution layers  
**Used in:** `/spek.plan` (all phases), `/spek.implement`  

---

## What It Is

Structure that adds functionality around a tool without changing the tool:

```
DECORATOR WRAPPER

Input
  ↓
┌─────────────────────────┐
│ PRE-EXECUTION           │
│ ├─ Load context         │
│ ├─ Validate inputs      │
│ └─ Enrich command       │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ CORE EXECUTION          │
│ └─ Call SpecKit command │
└─────────────────────────┘
  ↓
┌─────────────────────────┐
│ POST-EXECUTION          │
│ ├─ Validate output      │
│ └─ Update memory        │
└─────────────────────────┘
  ↓
Output
```

---

## Why Use It

- ✅ No vendor coupling (tool changes don't break decorator)
- ✅ Independent layers (each layer has clear responsibility)
- ✅ Extensible (add new layers without modifying core)
- ✅ Testable (can test each layer separately)
- ✅ Transparent (user sees enriched result, not wrapper)

---

## When to Use

✅ Extending third-party tools without coupling  
✅ Adding context/validation layers  
✅ Maintaining vendor independence  
✅ Multi-tool orchestration (same pattern for each tool)  

❌ When tool provides hooks (prefer hooks)  
❌ Simple wrapping with 1-2 lines (composition simpler)  
❌ Performance-critical code (wrapper adds minor overhead)  

---

## Example: Specify Phase Enrichment

```python
def specify_enriched(feature_description):
    """Decorator wrapper for /speckit.specify"""
    
    try:
        # PRE: Load decisions + patterns
        decisions = load_from_vault("vault/decision.md")
        patterns = load_from_vault("vault/patterns.md")
        
        # Validate inputs
        if not feature_description:
            raise ValueError("Feature description required")
        
        # Enrich input with decisions + patterns
        enriched_prompt = f"""
        {feature_description}
        
        IMPORTANT: Adhere to these project decisions:
        {format_decisions(decisions)}
        
        Consider these proven patterns:
        {format_patterns(patterns)}
        """
        
        # CORE: Call SpecKit
        spec = speckit_specify(enriched_prompt)
        
        # POST: Validate output
        assert "## Overview" in spec, "Spec missing Overview section"
        assert "## Success Criteria" in spec, "Spec missing Success Criteria"
        
        # Update memory
        save_to_session("spec.md", spec)
        
        return spec
        
    except Exception as e:
        log_error(e, phase="specify")
        return fallback_spec()
```

---

## Related Patterns

- **Context Injection Pattern** — What gets injected in PRE layer
- **Sequential Error Recovery** — Error handling structure
- **Enrichment Layer Pattern** — Specific application to SpecKit phases

---

## Where It's Used

- **Primary:** [decorator-wrapper-pattern.md](../specs/decorator-wrapper-pattern.md)
- **Applied in:**
  - [enrichment-layer.md](../specs/enrichment-layer.md)
  - [spek-automate-workflow.md](../specs/spek-automate-workflow.md)
  - [speckit-integration-contract.md](../specs/speckit-integration-contract.md)

---

## Quick Checklist

- [ ] Define PRE layer (what context to load?)
- [ ] Define CORE layer (which tool to call?)
- [ ] Define POST layer (what to validate?)
- [ ] Add error handling (try/except per layer)
- [ ] Add logging (debug troubleshooting)
- [ ] Add fallback (graceful degradation)
- [ ] Document layer responsibilities

---

## Notes on Resource Use

- Decorator wrappers introduce minor runtime and resource overhead; measure in your environment.
- Context loading and validation resource use depends on feature size and configured enrichment.

Keep budgeting and limits configurable rather than embedding fixed numeric estimates in documentation.
