# ATOMIC SPECIFICATION: Decorator Wrapper Pattern (C3.2)


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Depends On:** None (foundational pattern)  
**Used By:** enrichment-layer.md (all three phases: specify, plan, implement)  

---


## Overview

Decorator wrapper pattern structures spekificity enrichment as pre/core/post layers without modifying SpecKit internals. This spec defines the pattern, rationale, error handling, and testing strategy.

---


## Success Criteria

- ✅ Pre/core/post layers are independent and testable
- ✅ Context is loaded without modifying SpecKit
- ✅ Output is validated and memory updated
- ✅ Errors are caught and handled gracefully
- ✅ Fallback mechanism works when core fails
- ✅ Pattern works with any SpecKit version
- ## Implementation Checklist
- [ ] Implement decorator wrapper base class
- [ ] Implement pre-execution layer (context loading)
- [ ] Implement core execution layer (call SpecKit)
- [ ] Implement post-execution layer (validation + memory)
- [ ] Add error handling and retry logic
- [ ] Add fallback mechanisms
- [ ] Write unit tests for each layer
- [ ] Write integration tests for full wrapper
- [ ] Document in wrapper skill files
- ## References
- **Related Specs:**
- [context-layer.md](031-context-layer.md) — Context loading in pre-execution
- [enrichment-layer.md](032-enrichment-layer.md) — Specific wrappers for all phases
- **External:**
- [extracted spec Decorator Pattern](110-speckit-integration-contract.md#integration-pattern-decorator-wrapper) — Original spec
- Decorator Design Pattern — Gang of Four design patterns


## Pattern Structure

```python
def spek_enriched_command(command_name, *args, **kwargs):
    """
    Decorator wrapper around SpecKit command.
    
    Structure:
    1. Pre-execution: Load context, validate inputs
    2. Core: Call SpecKit command
    3. Post-execution: Validate output, update memory
    """
    
    try:
        # LAYER 1: PRE-EXECUTION
        context = load_context(command_name)
        enriched_inputs = validate_and_enrich_inputs(*args, context=context)
        
        # LAYER 2: CORE EXECUTION
        result = speckit_command(command_name, *enriched_inputs, **kwargs)
        
        # LAYER 3: POST-EXECUTION
        validated_result = validate_output(result)
        update_memory(validated_result)
        
        return validated_result
        
    except Exception as e:
        handle_error(e, command_name)
        return fallback_result(command_name)
```

---


## Why Decorator, Not Hooks?

**Rationale:**
- SpecKit doesn't provide hook system → Hooks out of scope
- Decorator doesn't require SpecKit changes → Vendor-independent
- Pre/Core/Post layers are explicit → Easy to trace and debug
- Works with any SpecKit version → No version coupling

**Alternative Considered: Hooks/Middleware**
- Pro: Could be lighter-weight
- Con: Requires SpecKit to implement hook system
- Con: Tight coupling to specific SpecKit version
- Con: Hidden dependencies (harder to debug)

**Decision:** Decorator pattern wins (independence + clarity + stability)

---


## Layer Responsibilities


## Pre-Execution Layer

**Responsibility:** Load context, validate inputs, enrich command

**Tasks:**
1. Load context (decisions, patterns, lessons, code graph)
2. Validate inputs are present and well-formed
3. Inject context into SpecKit command arguments
4. Check preconditions (e.g., spec should exist before plan)
5. Log command invocation

**Output:**
- Enriched inputs ready for core execution

**Error Handling:**
- Missing context → Log warning, continue with partial context
- Invalid inputs → Log error, raise exception (fail fast)
- Precondition not met → Log error, suggest remediation

---


## Core Execution Layer

**Responsibility:** Call SpecKit command unmodified

**Tasks:**
1. Invoke `/speckit.command` with enriched inputs
2. Capture output and execution trace
3. Catch any exceptions

**Output:**
- SpecKit output (spec.md, plan.md, etc.)
- Execution trace (logs, errors)

**Error Handling:**
- SpecKit command fails → Catch exception, pass to post-execution
- Output file missing → Log error, check permissions

---


## Post-Execution Layer

**Responsibility:** Validate output, update memory, report status

**Tasks:**
1. Validate output conforms to expected schema
2. Check for content coherence (plan consistent with spec, etc.)
3. Update feature state memory
4. Log completion
5. Report status to user

**Output:**
- Updated vault/session/
- User-visible completion report

**Error Handling:**
- Output invalid → Log error, report to user, continue (partial success)
- Memory update fails → Log error, continue (memory is optional)
- Status reporting fails → Log error, continue

---


## Error Handling Strategy


## Error Propagation

```
Pre-Execution Error
  → Log (context might be unavailable, that's OK)
  → Continue to core (with reduced context)
  
Core Execution Error
  → Catch exception
  → Pass to post-execution
  → Post decides: Retry? Partial? Fallback?
  
Post-Execution Error
  → Log error
  → Continue (post-execution is optional)
```


## Retry Strategy

**Pre-Execution Errors:** No retry (environment issue, not transient)

**Core Execution Errors:**
- LLM timeout → Retry once (may recover)
- File not found → Don't retry (structural issue)
- API error → Retry once (may be transient)

**Post-Execution Errors:** No retry (memory is optional)


## Fallback Strategy

**If Core Execution Fails:**

```python
if result is None or result is Error:
    # Try fallback
    if command_name == "specify":
        # Return empty spec template (user can fill in)
        return create_empty_spec_template()
    elif command_name == "plan":
        # Return empty plan template
        return create_empty_plan_template()
    elif command_name == "implement":
        # Return partial result (what succeeded)
        return partial_implementation_result()
```

---


## Testing Strategy


## Unit Tests (Test Each Layer Independently)

**Pre-Execution Tests:**
- Context loads successfully
- Context is injected into inputs
- Invalid inputs are caught
- Preconditions validated

**Core Execution Tests:**
- SpecKit command is called with correct args
- Output is captured correctly
- Exceptions are caught

**Post-Execution Tests:**
- Output is validated
- Memory is updated
- Status is reported


## Integration Tests (Test Full Wrapper)

**Scenario 1: Happy Path**
- Pre → Core → Post all succeed
- Result is valid and memory updated

**Scenario 2: Missing Context**
- Context load fails
- Core executes with partial context
- Result is valid (core is robust)

**Scenario 3: Core Fails**
- Pre succeeds, Core fails, Post handles it
- Fallback is used
- User is informed

**Scenario 4: Post Fails**
- Pre and Core succeed, Post fails
- Result is still returned (post is optional)
- Error is logged

---


## Configuration


## .spek/config.yaml

```yaml
decorator_wrapper:
  # Enable wrapper?
  enabled: true
  
  # Which commands to wrap?
  wrap_commands:
    specify: true
    plan: true
    implement: true
    post: true
  
  # Error handling
  error_handling:
    # Retry failed core execution?
    retry_core_errors: true
    retry_count: 1
    
    # Use fallback if core fails?
    use_fallback: true
    
    # Continue if post fails?
    continue_on_post_error: true
  
  # Logging
  logging:
    verbose: false
    log_all_layers: true
```

---

