# ⚠️ REDIRECT: Backprop Reflex: Test Failures → Vault Updates

**This specification has been consolidated into a single archive file.**

**Original ID:** C.3.6  
**See:** [Validation Patterns Archive](validation-patterns-archive.md#section-2-backprop-reflex-test-failures--vault-updates)

---

## Purpose

Automatically capture and learn from test failures by:
1. **Parsing** test failure output (error messages, stack traces, failed assertions)
2. **Extracting** failure patterns (common causes, recurring issues)
3. **Updating vault** with warnings/notes to prevent future repeats
4. **Tagging future specs** with lessons from past failures
5. **Creating feedback loop:** Test failures → Vault learnings → Better specs → Fewer failures

**Goal:** Reduce repeat mistakes across features; test failures become permanent knowledge, not temporary pain.

---

## Scope & Relationships

**What this spec covers:**
- Test failure detection + parsing
- Failure pattern extraction (semantic analysis)
- Vault update strategy (append to decision/pattern)
- Integration into `/spek.conclude` Step 3 (Generate Lessons)
- Integration into `/spek.context` Step 3 (surface warnings for current feature)
- Backward propagation logic

**What this spec does NOT cover:**
- Test runner configuration (assume Jest/Mocha/pytest available)
- CI/CD pipeline setup (assume GitHub Actions or similar)
- Failure categorization logic (can be extended per project)

---

## Success Criteria

- ✅ Test failures automatically parsed (error messages, stack traces extracted)
- ✅ Failure patterns extracted and classified (race condition, timeout, assertion, etc.)
- ✅ Vault updated with failure warnings (appended to decision/pattern records)
- ✅ Future specs tagged with failure pattern warnings (prevents repeats)
- ✅ Feedback loop: test failures → vault learnings → better specs → fewer failures
- ✅ Failure notes captured with context (full stack trace + test name + severity)
- ✅ Integration into `/spek.conclude` Step 3 seamless (user sees "Failure analysis complete")

---

## Related Specs

- B.8.4: Post Command (Step 3 lesson generation; where backprop integrates)
- C.3.1: Zettelkasten Conventions (vault format for failure records)
- C.3.2: Auto-tagging + Auto-wikilinks (tag failure notes)

---

## Backprop Workflow

### End-of-Feature Failure Analysis

**When:** During `/spek.conclude` Step 3 (Generate Lessons)

```
/spek.conclude Step 3: Generate Lessons
  1. Collect artifacts (spec, plan, tasks, trace)
  2. Generate lesson content
  3. [NEW] Run test failure analysis
     a. Get last test run results (from CI/CD or local)
     b. Parse failure output
     c. Extract patterns
     d. Update vault with warnings
     e. Tag lesson with failure patterns
  4. Auto-tag + auto-link (existing C.3.2)
  5. Save lesson to vault
```

### Test Failure Parsing

**Input:** Test output (JSON, TAP, or text format)

```json
{
  "testSuite": "auth.test.js",
  "failures": [
    {
      "test": "should handle token refresh timeout",
      "error": "AssertionError: expected 200 to equal 401",
      "stack": "at Object.<anonymous> (auth.test.js:42:15)",
      "type": "assertion_error"
    },
    {
      "test": "should prevent race condition in concurrent refresh",
      "error": "TimeoutError: Promise did not settle within 5000ms",
      "stack": "at Timeout._onTimeout (auth.test.js:67:8)",
      "type": "timeout_error"
    }
  ]
}
```

### Failure Pattern Extraction

**Algorithm:**

```
For each test failure:
  1. Extract failure type (AssertionError, TimeoutError, etc.)
  2. Extract failure message
  3. Match against known patterns:
     - "race condition" → pattern: concurrent-access
     - "timeout" → pattern: async-performance
     - "assertion mismatch" → pattern: state-consistency
  4. Extract affected module (from stack trace)
  5. Create failure record:
     {
       "type": "race_condition",
       "message": "concurrent token refresh",
       "module": "auth-service",
       "test": "prevent-race-condition",
       "date": "2026-05-15",
       "related_decision": "use-singleton-pattern"
     }
```

---

## Vault Integration: Failure Records

### New Vault Location

**File:** `wiki/vault/failures/<YYYY-MM-DD>-<feature>-failures.md`

**Purpose:** Persistent record of test failures + remediation

**Example:**
```
vault/failures/2026-05-15-auth-refactor-failures.md
```

### Failure Record Format

```markdown
---
title: "Test Failures: Auth Refactor Feature"
tags: ["failure", "domain/authentication", "feature/auth-refactor"]
created: "2026-05-15"
related_decisions: ["[[use-singleton-pattern]]", "[[token-lifecycle-decision]]"]
patterns_affected: ["concurrent-access", "async-performance"]
total_failures: 3
---

## Failure Summary

- **Total failures:** 3
- **Resolved:** 2
- **Unresolved:** 1

## Failures

### 1. Race Condition in Concurrent Token Refresh

**Test:** `should prevent race condition in concurrent refresh`  
**Error:** `TimeoutError: Promise did not settle within 5000ms`  
**Pattern:** Race condition (concurrent access)  
**Related Decision:** [[use-singleton-pattern]]

**Root Cause:**
- Singleton auth service received concurrent refresh requests
- Both tried to refresh token simultaneously
- Lock mechanism missing

**Fix Applied:**
- Added mutex lock around refresh operation
- Added timeout: 5 seconds per refresh
- Added queue for pending refresh requests

**Future Prevention:**
- When using singleton pattern, always add locks
- Document in [[singleton-pattern]]: "WARNING: Not thread-safe by default"
- Consider adding linting rule for concurrent access

**Updated in Vault:**
- [[singleton-pattern]]: Added warning about concurrent access
- [[token-lifecycle-decision]]: Noted lock requirement

### 2. State Inconsistency After Timeout

**Test:** `should handle token refresh timeout`  
**Error:** `AssertionError: expected 200 to equal 401`  
**Pattern:** State consistency (async errors)  
**Related Decision:** [[token-lifecycle-decision]]

**Root Cause:**
- Token refresh timed out
- Error handler didn't update token state
- Client retried with stale token

**Fix Applied:**
- Added error handler to clear token on timeout
- Added retry logic with exponential backoff
- Updated test timeout to 10 seconds

**Future Prevention:**
- Document in [[error-handling-recovery]]: timeout recovery strategy
- Add health check after timeout

**Updated in Vault:**
- [[error-handling-recovery]]: Added timeout recovery pattern

### 3. [UNRESOLVED] Race Condition in Parallel Test Execution

**Test:** `should handle parallel logout + refresh`  
**Error:** `AssertionError: token still valid after logout`  
**Investigation Needed:**
- Verify test isolation (parallel tests not interfering)
- Check if singleton state leaking between tests
- Consider test fixture reset strategy

**Blocking Issue:** Assigned to next sprint
```

### Auto-Update to Related Decisions

When a failure is analyzed, backprop automatically updates related vault items:

**Example: Update to [[singleton-pattern]]**

```markdown
---
title: "Singleton Pattern"
...
---

## Singleton Pattern

[existing content]

### ⚠️ Concurrency Warning (Added 2026-05-15)

**From failure analysis:** Race conditions observed in concurrent access  
**Issue:** Multiple threads accessing singleton instance simultaneously  
**Solution:** Add mutex lock or use thread-safe wrapper  
**Reference:** [[wiki/vault/failures/2026-05-15-auth-refactor-failures.md#race-condition]]

When using singleton pattern:
1. Document thread-safety assumptions
2. Add locks if concurrent access possible
3. Test under concurrent load
```

---

## Integration: /spek.conclude Step 3 Enhancement

### Current Workflow

```
/spek.conclude Step 3: Generate Lessons
  → Generate lesson markdown
  → Auto-link + auto-tag
  → Save lesson
```

### Enhanced with Backprop

```
/spek.conclude Step 3: Generate Lessons (Enhanced)
  1. Generate lesson markdown (existing)
  2. [NEW] Run test failure analysis
     a. Query last test run (CI/CD API or local)
     b. Parse failures
     c. Extract patterns + affected modules
     d. Create failure log (wiki/vault/failures/...)
     e. Update related decisions/patterns with warnings
  3. Tag lesson with failure patterns
     tags: ["lesson/auth-refactor", "failure/race-condition", ...]
  4. Auto-link + auto-tag (C.3.2)
  5. Save lesson + failure log
```

### Implementation Pseudocode

```python
def analyze_test_failures_for_feature(feature_name):
    """Analyze test failures and update vault (backprop)"""
    
    # Step 1: Get test results
    test_results = get_last_test_run()
    if not test_results.has_failures():
        return  # No failures, nothing to do
    
    # Step 2: Parse + Extract
    failures = []
    for test_failure in test_results.failures:
        pattern = classify_failure_pattern(test_failure.error_type)
        module = extract_module_from_stack(test_failure.stack_trace)
        failures.append({
            'test': test_failure.test_name,
            'error': test_failure.error_message,
            'pattern': pattern,
            'module': module,
            'resolved': test_failure.fixed_in_branch,
        })
    
    # Step 3: Create failure log
    failure_log_path = f"wiki/vault/failures/{date_slug}-{feature_name}-failures.md"
    failure_log = generate_failure_log(failures, feature_name)
    write_vault_file(failure_log_path, failure_log)
    
    # Step 4: Update related decisions + patterns
    for failure in failures:
        for affected_item in find_related_vault_items(failure['pattern']):
            add_failure_warning(affected_item, failure_log_path)
    
    # Step 5: Tag lesson with failures
    lesson_tags = [f"failure/{f['pattern']}" for f in failures]
    return lesson_tags
```

---

## Integration: /spek.context Step 3

When loading context for next feature, surface failure warnings:

```
/spek.context Step 3: Query Vault

[NEW] Failure Warnings Check:
  → Query wiki/vault/failures/ for recent failures
  → Filter by related domain/patterns
  → Alert user: "Previous auth feature had race conditions; review [[singleton-pattern]] warnings"
  
  Result: User aware of past pitfalls before starting similar work
```

---

## Query Patterns

### Find Failures in Specific Domain

```
vault search: tag:failure AND tag:domain/authentication
→ Returns all failure logs in auth domain
→ Helps understand "what goes wrong in auth?"
```

### Find Failures Related to Pattern

```
vault graph: backlinks to [[singleton-pattern]]
→ Shows all failure logs mentioning singleton
→ Helps understand "what problems does this pattern cause?"
```

### Find Recent Failures

```
vault search: type:failure-log created:>2026-05-01
→ Returns failures from last month
→ Helps identify "what's been problematic recently?"
```

---

## Configuration

### Test Failure Parsers

Add to `.spek/config.yaml`:

```yaml
backprop:
  enabled: true
  
  test_frameworks:
    - jest      # npm run test (Jest output)
    - pytest    # pytest (Python output)
    - mocha     # npm run test:mocha
  
  failure_patterns:
    "race_condition": ["race", "concurrent", "mutex", "lock"]
    "timeout_error": ["timeout", "settle", "promise"]
    "assertion_error": ["assertion", "expected", "to equal"]
    "state_inconsistency": ["state", "stale", "invalid"]
  
  vault_update:
    create_failure_log: true
    update_related_decisions: true
    update_related_patterns: true
    alert_on_new_pattern: true
```

---

## Success Criteria

- ✅ Test failure parsing + pattern extraction working
- ✅ Failure logs created in `wiki/vault/failures/` with Zettelkasten format
- ✅ Related decisions/patterns auto-updated with failure warnings
- ✅ Lessons tagged with failure patterns (failure/race-condition, etc.)
- ✅ `/spek.context` surfaces past failure warnings
- ✅ ~70% of failure patterns auto-categorized (config-driven)
- ✅ Zero test failures slip past without vault record
- ✅ Future features query vault and avoid repeating mistakes

---

## Related Specifications

- **B.8.4:** Post Command (Step 3 integration)
- **C.3.1:** Zettelkasten Conventions (failure log format)
- **C.3.2:** Auto-tagging + Auto-wikilinks (failure log tagging)
- **B.10:** SDD Framework Comparison (source: Cavekit backprop pattern)

---

## References

- **Production Source:** https://github.com/Cavekit/cavekit (920⭐, backprop pattern)
- **Test Failure Analysis:** BDD + failure categorization patterns