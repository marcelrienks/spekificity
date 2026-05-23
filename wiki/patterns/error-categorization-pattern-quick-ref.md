# Error Categorization Pattern — Quick Reference

**Category:** Error Handling  
**Problem:** Errors need different handling; one-size-fits-all doesn't work  
**Solution:** Categorize errors; apply category-specific recovery  
**Used in:** All skills (error handling)  

---

## What It Is

Error classification with tailored recovery strategies:

```
ERROR CATEGORIZATION

┌─ GIT STATE ERRORS
│  └─ Severity: HIGH
│  └─ Action: FAIL + GUIDE
│  └─ Recovery: User action required
│
├─ VAULT ACCESS ERRORS
│  └─ Severity: MEDIUM-HIGH
│  └─ Action: WARN + FALLBACK
│  └─ Recovery: Retry 30s intervals
│
├─ GRAPH/CODE INDEX ERRORS
│  └─ Severity: MEDIUM
│  └─ Action: WARN + FALLBACK
│  └─ Recovery: Re-trigger /spek.map
│
├─ LLM ERRORS
│  └─ Severity: MEDIUM
│  └─ Action: RETRY + FALLBACK
│  └─ Recovery: Exponential backoff
│
├─ SPECKIT ERRORS
│  └─ Severity: HIGH
│  └─ Action: FAIL + GUIDANCE
│  └─ Recovery: Manual intervention
│
└─ USER ERRORS
   └─ Severity: HIGH
   └─ Action: FAIL + GUIDANCE
   └─ Recovery: User re-runs with correct input
```

---

## Why Use It

- ✅ Appropriate recovery (don't retry permanent errors)
- ✅ User guidance (clear what to fix)
- ✅ Autonomous resilience (retries transient errors)
- ✅ Observable (categorized logging)
- ✅ Predictable (users know error behavior)

---

## When to Use

✅ Autonomous workflows (error recovery needed)  
✅ Production deployments (failures expected)  
✅ Multi-phase workflows (partial failures tolerated)  

❌ Script with no recovery ("fail fast" better)  
❌ Interactive debugging (manual intervention preferred)  

---

## Category Details

### Category 1: Git State Errors

**Errors:**
- `.git/` not found
- Working tree dirty (uncommitted changes)
- Feature branch not found
- Merge/rebase in progress
- Detached HEAD state

**Handling:**
```
Severity: HIGH
Default Action: FAIL + GUIDE
Recovery Flow: No auto-retry (requires user action)

Example:
  Error: Git working tree is dirty
    Unstaged changes: src/main.py, src/utils.py
  Action: git add . && git commit -m "checkpoint" OR git stash
  Then: /spek.prepare
```

### Category 2: Vault Access Errors

**Errors:**
- `vault/` directory not found
- `vault/decision.md` missing or corrupted
- JSON parse error
- Permission denied
- File locked (concurrent access)

**Handling:**
```
Severity: MEDIUM-HIGH
Default Action: WARN + FALLBACK
Recovery Flow: Async retry (30s intervals, max 3 retries)

Example:
  Warning: Vault inaccessible (permission denied: vault/decision.md)
  Fallback: Using cached decisions from /memories/repo/...
  Retry: Vault access will be attempted every 30s for 3 retries
```

### Category 3: Graph/Code Index Errors

**Errors:**
- Code graph corrupted
- CodeGraph index refresh fails
- Node index missing
- Edge computation failed

**Handling:**
```
Severity: MEDIUM
Default Action: WARN + FALLBACK
Recovery Flow: Re-trigger /spek.map on next run

Example:
  Warning: Graph cache corrupted (invalid nodes.jsonl)
  Fallback: Using grep-based queries (slower, 0 tokens)
  Recovery: Run '/spek.map --full' to rebuild graph
```

### Category 4: LLM Errors

**Errors:**
- API timeout (>30s)
- Rate limit exceeded
- Model unavailable
- API key invalid

**Handling:**
```
Severity: MEDIUM
Default Action: RETRY + FALLBACK
Recovery Flow: 3 retries with exponential backoff

Retry strategy:
  Retry 1: Wait 2s, then retry
  Retry 2: Wait 5s, then retry
  Retry 3: Wait 10s, then retry
  On all failures: Fallback to simpler prompt
```

### Category 5: SpecKit Errors

**Errors:**
- Spec generation failed
- Plan invalid or incomplete
- Tasks parsing failed
- Implementation artifact missing

**Handling:**
```
Severity: HIGH
Default Action: FAIL + GUIDANCE
Recovery Flow: Manual intervention required

Example:
  Error: /speckit.specify failed
  Details: Spec generation timed out after 60s
  Action: Increase timeout or simplify feature description
  Then: /spek.plan [revised-description]
```

### Category 6: User Errors

**Errors:**
- Missing required parameter
- Invalid feature name
- Conflicting flags
- Invalid input format

**Handling:**
```
Severity: HIGH
Default Action: FAIL + GUIDANCE
Recovery Flow: User re-runs with correct input

Example:
  Error: Invalid feature name: "my feature" (contains space)
  Fix: Use kebab-case: "my-feature"
  Then: /spek.prepare --feature-name="my-feature"
```

---

## Example: Error Handling

```python
def skill_with_categorization(inputs):
    try:
        # PRE-EXECUTION
        context = load_context()
    except FileNotFoundError as e:
        # Category: VAULT ACCESS ERROR
        category = "VAULT"
        log_error(e, category=category)
        # Attempt fallback + retry
        context = load_from_cache()
        retry_vault_access()  # Async
    except PermissionError as e:
        # Category: VAULT ACCESS ERROR
        category = "VAULT"
        log_error(e, category=category, action="Fix vault permissions")
        # Fallback + retry
        context = load_from_cache()
    
    try:
        # CORE EXECUTION
        result = core_execution(context, inputs)
    except APIError as e:
        if "timeout" in str(e):
            # Category: LLM ERROR (transient)
            log_error(e, category="LLM_TRANSIENT")
            result = retry_with_backoff(core_execution, max_retries=3)
        elif "rate_limit" in str(e):
            # Category: LLM ERROR (transient)
            log_error(e, category="LLM_RATE_LIMIT")
            result = retry_with_backoff(core_execution, max_retries=3)
        else:
            # Category: LLM ERROR (permanent)
            log_error(e, category="LLM_FATAL")
            raise
    except ValueError as e:
        # Category: USER ERROR
        log_error(e, category="USER", action=f"Check input: {e}")
        raise
    
    return result
```

---

## Related Patterns

- **Fallback Hierarchy** — Layered fallback strategies
- **Sequential Error Recovery** — Error handling structure
- **Feature Lifecycle** — Phase-specific error handling

---

## Where It's Used

- **Primary:** [error-handling-and-recovery.md](../specs/error-handling-and-recovery.md)
- **Applied in:** All workflow specs (prepare, automate, post, implement)

---

## Quick Checklist

- [ ] Error categories defined (6+ categories)?
- [ ] Severity levels assigned (HIGH/MEDIUM)?
- [ ] Default actions specified (FAIL/WARN)?
- [ ] Recovery flow clear (retry/fallback)?
- [ ] Logging structured (category + action)?
- [ ] User guidance clear (what to do?)?
- [ ] Monitoring/alerting configured?

---

## Token Cost

- **Error categorization:** ~50-100 tokens (one-time)
- **Error logging:** ~10 tokens per error
- **User guidance message:** ~50-100 tokens

Total: Minimal if errors are rare; adds ~1-2K tokens if many errors.
