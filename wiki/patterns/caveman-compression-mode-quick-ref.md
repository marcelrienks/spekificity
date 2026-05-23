# Caveman Compression Mode — Quick Reference

**Category:** Compression  
**Problem:** Lessons and vault updates can consume significant token budget; multi-feature sessions may hit limits  
**Solution:** Ultra-compressed communication (significant token reduction)  
**Used in:** `/spek.conclude` lessons generation, vault compression  

---

## What It Is

Extreme-compression writing style that preserves technical accuracy:

```
COMPRESSION LEVELS

Lite (modest reduction):
   Full sentences, natural language
   Use: First feature, complex decisions
  
Full (large reduction, DEFAULT):
   Caveman style, terse + clear
   Use: Standard workflow
  
Ultra (maximal reduction):
   Minimal syntax, abbreviations
   Use: Token-constrained sessions
```

---

## Why Use It

-- ✅ Token savings (substantial reduction)
- ✅ Meaning preserved (technical accuracy maintained)
- ✅ Multi-feature feasibility (multiple features per session)
- ✅ Vault still searchable (keywords preserved)
- ✅ User control (choose mode per-session)

---

## When to Use

✅ Lessons generation (integration point at `/spek.conclude`)  
✅ Vault compression (/memories/repo cache)  
✅ Multi-feature sessions (token budget tight)  

❌ First-time documentation (prefer clarity)  
❌ Code comments (readability critical)  
❌ User-facing docs (clarity required)  

---

## Modes: Examples

### Mode 1: Lite (modest reduction)

**Normal text:**
```
## Decision: Use Dependency Injection

We chose Dependency Injection (DI) as the service instantiation 
pattern for the following reasons:

**Pros:**
- Decoupling: Services don't know how to create dependencies
- Testability: Easy to inject mocks in tests
- Flexibility: Can change implementations without changing clients

**Cons:**
- Setup overhead: DI container configuration required
- Learning curve: Developers need to understand DI concepts
```

**Lite caveman:**
```
## Decision: Dependency Injection

Why: Decoupling, testability, flexibility.
Cons: Setup overhead, learning curve.
Recommendation: Worth it for medium+ projects.
```

**Reduction:** modest (still pretty verbose)

---

### Mode 2: Full (large reduction, DEFAULT)

**Normal text:**
```
## Lesson: Auth Refactor

### What We Built

We refactored the authentication module to use JWT tokens instead of 
session cookies. This enables stateless auth, easier horizontal scaling, 
and mobile app support.

Key changes:
- New JWT utility: `src/auth/jwt-utils.ts`
- Middleware integration: `src/middleware/auth-middleware.ts`
- Token refresh logic: 15-minute expiry, refresh endpoint

### How We Built It

We followed the decorator wrapper pattern established in spec-003, 
wrapping the auth service with context injection. This ensured consistency 
with prior auth work and made testing easier.

Task breakdown: tasks and sequencing described; durations not specified

### Key Decisions

1. JWT expiry: short expiry configured (security/UX balance)
   - Rationale: Balance security + UX
   
2. Refresh token storage: HttpOnly cookies (not localStorage)
   - Rationale: XSS protection
```

**Full caveman:**
```
## Lesson: Auth Refactor

### What Built
JWT tokens (stateless auth). Key files: jwt-utils.ts, auth-middleware.ts. 
Replaces session cookies. Enables scaling + mobile.

### How Built
Decorator wrapper pattern (spec-003). Pre/core/post layers. 
Tasks: Design schema (1h), implement JWT (3h), middleware (2h), tests (2h), 
debug race condition (1.5h).

### Decisions
1. JWT expiry: 15min (security/UX balance)
2. Refresh in HttpOnly cookies (XSS protection)

### Patterns
- Decorator wrapper (pre/core/post)
- Context injection (decisions informed implementation)
```

**Reduction:** large (terse but complete)

---

### Mode 3: Ultra (maximal reduction)

**Ultra caveman:**
```
## Lesson: Auth Refactor

What: JWT tokens, stateless auth. jwt-utils.ts, auth-middleware.ts.
How: Decorator wrapper (pre/core/post). Total measured effort recorded. Debugged race condition.
Decisions: JWT short expiry. Refresh in HttpOnly (XSS protection).
Patterns: Decorator, context injection.
```

**Reduction:** maximal (minimal but sufficient for vault)

---

## Compression Rules (Full Mode)

```
Apply these rules to achieve strong reduction:

1. TENSE
   - Use present tense (faster, clearer)
   - ❌ "We decided that the system should use..."
   - ✓ "System uses dependency injection"

2. STRUCTURE
   - Bullets instead of prose (compact)
   - ❌ "The first step was to design the schema"
   - ✓ "1. Design schema"

3. SPECIFICITY
   - Provide succinct specifics when necessary (avoid verbose enumerations)
   - ❌ "We did some testing"
   - ✓ "Tests: unit + integration where applicable"

4. ABBREVIATIONS
   - OK to use abbreviations (DI, JWT, API, etc.)
   - OK to use shorthand (pre/core/post instead of pre-execution)

5. CONTEXT (KEEP)
   - DO keep technical concepts
   - DO keep decision rationale
   - DO keep related decisions
   - DO keep code references

6. VERBOSITY (REMOVE)
   - NO fluffy words ("quite", "really", "very")
   - NO extended explanations (assume reader knows domain)
   - NO hedging ("possibly", "might", "could")
```

---

## Compression Configuration

```yaml
caveman_mode:
  # Default mode for feature
  default: "full"
  
  # Enabled/disabled
  enabled: true
  
  # Compression rules
  rules:
    # Active voice (shorter)
    active_voice: true
    
    # Remove articles (a, an, the)
    remove_articles: true
    
    # Use abbreviations (DI, JWT, etc.)
    abbreviations: true
    
    # Remove redundant words
    remove_redundancy: true
    
    # Symbols instead of words (→ instead of "leads to")
    use_symbols: true
```

---

## Example: Compress a Lesson

**Before (Normal):**
```
## Lesson: Caching Strategy Refactor

### What We Built

We refactored the caching layer to use Redis instead of in-memory caches. 
This addresses scalability issues we encountered in production where cache 
hits weren't shared across server instances. The new architecture uses 
Redis as a centralized cache with local in-memory Layer 1 caches for 
frequently accessed items.

### How We Built It

Following the context injection pattern from spec-002, we wrapped cache 
operations with enrichment layer logic that validates cache alignment with 
architectural decisions. The process took a measured amount of time across sessions.

### Decisions Made

1. **Redis as primary cache**: Centralized, reliable, scales horizontally
2. **Two-layer caching**: Redis + local L1 for hot keys (performance optimization)
3. **Short TTL**: Balance between freshness and cache hits
```

**After (Full Caveman):**
```
## Lesson: Caching Strategy Refactor

### What Built
Redis → centralized cache (replaced in-memory). Issue: cache hits not shared 
cross-instance. Solution: Redis primary + L1 local cache (hot keys).

### How Built
Context injection pattern (spec-002). Pre/core/post validation. Total effort recorded.

### Decisions
1. Redis primary (centralized, scales horizontally)
2. Two-layer caching (Redis + L1 for hot keys)
3. 30min TTL (freshness vs. hit rate)
```

**Reduction:** 72% (from 200 words → 56 words)

---

## Related Patterns

- **Token Budget Tracking** — Monitors compression impact
- **Post-Processing** — Integration point (Step 2)
- **Lessons Format** — Template for compressed lessons

---

## Where It's Used

- **Primary:** [caveman-integration.md](../specs/caveman-integration.md)
- **Integration points:**
  - [post-command.md](../specs/post-command.md) (Step 2)
  - [post-processing.md](../specs/post-processing.md)
  - [lessons-format.md](../specs/lessons-format.md)

---

## Quick Checklist

- [ ] Mode selected (lite/full/ultra)?
- [ ] Compression rules applied (active voice, no fluff)?
- [ ] Technical accuracy preserved (concepts intact)?
- [ ] Searchability maintained (keywords preserved)?
- [ ] Cost calculation confirmed?
- [ ] Multi-feature feasibility verified (budget allows)?
- [ ] User preference configured (mode per-session)?

---

## Token Cost Impact

```
Token Cost Impact: Compression significantly reduces per-feature lesson size; plan and validate against your session budget.

Without compression: lessons and summaries are larger and may exhaust session budgets.

With compression: lessons are smaller and more features fit within the same budget.

Benefit: more features or more detail per session depending on compression level.
```
