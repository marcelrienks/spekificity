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
Recovery Flow: Async retry with increasing intervals

Example:
  Warning: Vault inaccessible (permission denied: vault/decision.md)
  Fallback: Using cached decisions from /memories/repo/...
  Retry: Vault access will be attempted with backoff
```

### Category 3: Graph/Code Index Errors

**Errors:**
- Code graph corrupted
- lat.md index refresh fails
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

I'll continue creating the remaining files similarly. Next I'll copy the remaining pattern files into `wiki/specs/patterns` and then delete the originals. This keeps changes consistent. If you'd prefer I update internal links in specs too, I can do that afterwards.