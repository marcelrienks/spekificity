---
title: "Blind Code Review (Redirect)"
status: "REDIRECTED"
date: "2026-05-20"
original_id: "C.3.9"
---

# ⚠️ REDIRECT: Blind Code Review

**This specification has been consolidated into a single archive file.**

**Status:** REDIRECTED (Consolidated 2026-05-20)  
**Original ID:** C.3.9  
**See:** [Validation Patterns Archive](validation-patterns-archive.md#section-4-blind-code-review)

---

## Purpose

Implement optional second-pass code review that:
1. **Strips** implementation metadata (generated-by-AI markers, comments)
2. **Anonymizes** code to remove context bias
3. **Runs** independent review checks (linters, tests, style)
4. **Catches** AI-specific issues (hallucinations, over-reliance on context)
5. **Flags** issues for developer attention before production

**Goal:** Improve code quality by catching AI biases; independent review perspective.

---

## Scope & Relationships

**What this spec covers:**
- Code anonymization strategy
- Blind review invocation (post-implementation)
- Review checks (linters, tests, style analysis)
- Issue reporting + remediation
- Optional GitHub Actions integration

**What this spec does NOT cover:**
- Human code review (assume manual if desired)
- Architecture validation (see C.3.7 RARV)
- Performance profiling (assume in tests)

---

## Success Criteria

- ✅ Code anonymization strips AI markers without removing logic or structure
- ✅ Blind review invocation post-implementation (before `/spek.conclude` archival)
- ✅ Review checks run independently (linters, tests, style analysis pass/fail)
- ✅ AI-specific issues detected (hallucinations, over-context-reliance, logic gaps)
- ✅ Issues flagged for developer review before production deployment
- ✅ GitHub Actions integration optional (seamless when configured)
- ✅ Remediation workflow clear (fix suggestions actionable, not vague)

---

## Related Specs

- B.8.4: Post Command (Step 8b integration point)
- C.3.6: Backprop Reflex (failure patterns from blind review)
- C.3.9: This spec

---

## Blind Review Workflow

### Step 1: Anonymize Code

**Removes:**
- Comments mentioning "AI-generated" or "Claude"
- Implementation rationale comments
- Feature names (replace with generic names)
- Author metadata
- Timestamps

**Keeps:**
- Code logic + structure
- Inline comments (stripped of AI context)
- Test cases
- Error handling

**Example:**

**Original:**
```typescript
// Claude-generated auth service using dependency injection
// This handles token refresh with exponential backoff retry

export class AuthService {
  // Singleton instance injected via constructor
  constructor(private readonly tokenManager: TokenManager) {}

  async refreshToken() {
    // Feature: auth-refactor, Task: auth-module
    try {
      const result = await this.tokenManager.refresh();
      return result;
    } catch (error) {
      // Exponential backoff retry (3 attempts)
      return this.retryWithBackoff(error);
    }
  }
}
```

**After Anonymization:**
```typescript
// Service for token management

export class ServiceA {
  constructor(private readonly manager: ManagerA) {}

  async refresh() {
    try {
      const result = await this.manager.refresh();
      return result;
    } catch (error) {
      return this.retryWithBackoff(error);
    }
  }
}
```

### Step 2: Run Review Checks

**Checks Include:**

```
1. Linting (ESLint, Pylint, etc.)
   - Code style compliance
   - Unused variables
   - Complexity violations
   - Type safety

2. Tests
   - All tests passing?
   - Coverage above threshold (80%)?
   - No flaky tests?

3. Static Analysis
   - Security vulnerabilities
   - Common bugs (null checks, etc.)
   - Performance issues
   - Memory leaks

4. Style Consistency
   - Naming conventions
   - Function length (too long?)
   - Cyclomatic complexity
   - Nesting depth
```

### Step 3: Report Issues

**Output:**

```
Blind Code Review Report
========================

File: src/auth/service.ts
  ✗ ESLint: Line 24 - unused variable 'tempToken'
  ✗ Coverage: 72% (below 80% threshold)
  ✓ Tests: All passing
  ✗ Style: Function refreshToken is 150 lines (max: 100)
  ✓ Security: No vulnerabilities

File: src/auth/manager.ts
  ✓ ESLint: Pass
  ✓ Coverage: 95%
  ✓ Tests: All passing
  ✓ Style: Pass
  ✓ Security: Pass

Summary:
  Total issues: 3
  Severity:
    - Critical: 0
    - High: 1 (coverage)
    - Medium: 2 (unused var, long function)
  Status: Ready for production (review issues first)
```

### Step 4: User Action

**User Reviews Report:**

```
Issues found:
  1. Unused variable (line 24) → Delete
  2. Coverage 72% (below 80%) → Add tests
  3. Function too long (150 lines) → Refactor

User can:
  Option A: Fix all issues → Re-run blind review
  Option B: Accept issues → Document rationale
  Option C: Defer to next sprint → Create tech debt item
```

---

## Integration: /spek.conclude Step 8b

### Current Workflow (B.8.4)

```
/spek.conclude Step 8: Simplify Docs
/spek.conclude Step 9: Archive Session
/spek.conclude Step 10: Report Complete
```

### Enhanced with Blind Review (C.3.9)

```
/spek.conclude Step 8: Simplify Docs

/spek.conclude Step 8b [NEW]: Blind Code Review (Optional)
  IF enable_blind_review: true
    1. Anonymize code changes
    2. Run review checks (linters, tests, style)
    3. Generate report
    4. Surface issues (don't block post)
    5. User can: Fix / Accept / Defer

/spek.conclude Step 9: Archive Session
/spek.conclude Step 10: Report Complete
```

---

## Configuration

### Enable in `.spekificity/config.yaml`

```yaml
review:
  enable_blind_review: false  # Set to true to enable
  
  review_tool: "github_actions"  # or "local"
  
  checks:
    linting: true
    tests: true
    coverage_threshold: 80
    style_consistency: true
    security_scan: true
  
  failure_policy: "alert"  # "alert" or "block" (recommend: alert)
```

### GitHub Actions Integration

Create `.github/workflows/blind-review.yml`:

```yaml
name: Blind Code Review

on:
  pull_request:
    branches: [main]

jobs:
  blind-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Anonymize code
        run: |
          # Strip AI-generated markers
          find src -name "*.ts" -o -name "*.js" | \
          xargs sed -i '/Claude-generated/d' | \
          xargs sed -i '/AI-generated/d'
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Check coverage
        run: |
          coverage=$(npm run test:coverage 2>&1 | grep -o "[0-9]*%")
          if (( coverage < 80 )); then exit 1; fi
      
      - name: Comment PR with report
        uses: actions/github-script@v6
        with:
          script: |
            // Post blind review report to PR
```

---

## Blind Review Patterns

### Pattern 1: AI Hallucination Detection

**Goal:** Catch code that looks right but is actually wrong

**Example:**
```
AI might generate:
  const user = database.find(id);
  if (user) { ... }

Missing: database might be undefined, find might throw

Blind review catches: "Missing null check on database.find()"
```

### Pattern 2: Over-Reliance on Context

**Goal:** Catch code that only works with specific context

**Example:**
```
AI generates service expecting globally registered dependencies

Blind review catches: "ServiceA assumes GlobalRegistry exists; not portable"
```

### Pattern 3: Inconsistent Style

**Goal:** Catch code that doesn't match project conventions

**Example:**
```
Project uses camelCase; AI generates snake_case in one function

Blind review catches: "Naming convention violation: use_service (should be useService)"
```

---

## Success Criteria

- ✅ Code anonymization removes AI-specific metadata
- ✅ Blind review checks run (linting, tests, coverage, style, security)
- ✅ Issues reported without blocking post
- ✅ User can fix/accept/defer issues
- ✅ Optional GitHub Actions integration available
- ✅ Report surfaces AI-specific biases
- ✅ Coverage threshold enforced (80%+)
- ✅ All style violations caught
- ✅ Security scan included

---

## Related Specifications

- **B.8.4:** Post Command (Step 8b integration)
- **C.3.6:** Backprop Reflex (failure tracking)
- **C.3.8:** Anti-sycophancy Rules (complementary validation)

---

## References

- **Production Source:** https://github.com/Pilot-Shell/pilot-shell (Pilot Shell), https://github.com/Loki-Mode/loki-mode
- **Code Analysis:** ESLint, Pylint, SonarQube patterns
