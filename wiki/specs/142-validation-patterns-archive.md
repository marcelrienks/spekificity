# CONSOLIDATED: Validation & Reflection Patterns Library

**Status:** CONSOLIDATED SPECIFICATION ARCHIVE   | **Version:** 1.0.0-alpha.1 (2026-05-20)  
**Type:** Validation Patterns — AI Drift Prevention, Code Quality, Failure Learning, Alignment Verification  
**Consolidated From:** 4 separate specifications (C.3.6, C.3.7, C.3.8, C.3.9)  
**Used By:** `/spek.conclude` steps 3, 7, 8b; `/spek.plan` phases  

---

## Overview

Validation patterns are optional enhancements to Spekificity workflow that:
1. **Prevent AI drift** (anti-sycophancy rules, blind review)
2. **Learn from failures** (backprop reflex: test failures → vault)
3. **Verify alignment** (RARV: Reason-Act-Reflect-Verify)

This archive consolidates 4 related validation patterns with their adoption priority, effort estimates, and integration points.

---

## Pattern Index

| Pattern | Priority | Effort | Adoption Status | Purpose |
|---------|----------|--------|-----------------|---------|
| **[Section 1] Anti-Sycophancy Rules** | HIGH | 3-4h | Phase 2 | Flag AI drift before implementation |
| **[Section 2] Backprop Reflex** | HIGH | 3-4h | Phase 2 | Test failures → vault learning |
| **[Section 3] RARV Reflection Cycle** | HIGH | 4-5h | Phase 2 | Continuous alignment verification |
| **[Section 4] Blind Code Review** | MEDIUM | 4-5h | Phase 2 (optional) | Independent code quality check |

---

## SECTION 1: Anti-Sycophancy Validation Rules

**Status:** SPECIFICATION — Phase 2 implementation  
**Priority:** HIGH (solo dev critical)  
**Effort:** 3-4 hours  
**Source:** Loki Mode (930⭐), B.10 comparison  

### Purpose

Prevent AI drift by enforcing explicit validation rules that:
- Flag contradictions between new decisions and vault
- Alert when recent patterns suggest different approach
- Question scope/complexity increases without justification
- Prevent over-agreement with context

### Five Core Rules

#### Rule 1: Contradiction Detection

If spec contradicts vault decisions, flag conflict:

```
Vault Decision: "Use dependency injection pattern"
Spec Proposes: "Inject via service locator"
Alert Level: HIGH
Action: Justify deviation or align with decision
```

#### Rule 2: Complexity Increases

If spec complexity > 50% higher than similar features, question:

```
Recent Feature (auth): 1200 LOC, 2 components, 6 patterns
Current Spec (payment): 2000 LOC estimate, 5 components
Complexity increase: 67%
Alert: "Justify additional scope"
```

#### Rule 3: Pattern Consistency

If 3+ recent patterns suggest different approach, flag:

```
Vault Patterns (consensus): Observer, Singleton, Factory
Spec Proposes: Avoid Observer, use direct subscriptions
Alert: "Deviates from pattern consensus; justify"
```

#### Rule 4: Technology Stack Drift

If spec uses new tech not in vault, require justification:

```
Vault Stack: TypeScript, React, Node.js
Spec Proposes: Add Rust for performance
Alert: "New tech not in current stack; justify"
```

#### Rule 5: Scope Creep Detection

If scope grows during feature work, question:

```
Original Spec: "Password reset flow"
Implementation: "Add SMS + backup codes"
Scope Creep: 300%
Alert: "Scope grew; confirm intended"
```

### Validation Points

**During `/spek.plan` specify phase:**
- Check vault contradictions (Rule 1)
- Check complexity vs similar features (Rule 2)
- Check pattern suggestions (Rule 3)
- Check tech stack alignment (Rule 4)

**During `/spek.plan` plan phase:**
- Check architecture vs decisions (Rule 1)
- Check pattern alignment (Rule 3)
- Check scope complexity (Rule 2)

**During `/spek.implement`:**
- Monitor scope creep (Rule 5)
- Check tech choices vs stack (Rule 4)

### Configuration

Store per-project rules in `.spekificity/validation-rules.md`:

```yaml
# Validation Rules (Anti-Sycophancy)

## Spec Generation Rules

### Rule: No contradictions with vault decisions
- Trigger: Spec contradicts vault
- Action: ALERT (show vault rationale)
- Override: Allowed with justification

### Rule: Complexity within 50% of similar features
- Trigger: Estimated LOC > 1.5x similar feature
- Action: ALERT (question scope)
- Override: Allowed with stakeholder approval

### Rule: Use established patterns
- Trigger: Spec avoids consensus pattern
- Action: ALERT (suggest pattern + show usage)
- Override: Allowed with new-pattern-name justification

### Rule: Stay within tech stack
- Trigger: Spec introduces new technology
- Action: ALERT (show current stack)
- Override: Allowed with tech-evaluation document
```

### Success Criteria

- ✅ Contradiction detection identifies spec vs vault conflicts
- ✅ Complexity increase rule flags specs 50% above baseline
- ✅ Pattern consistency rule alerts when deviating from consensus
- ✅ Scope validation catches silent scope creep
- ✅ Configuration allows project-specific rules
- ✅ User override mechanism permits justified deviations
- ✅ All conflicts logged with rationale

---

## SECTION 2: Backprop Reflex: Test Failures → Vault Updates

**Status:** SPECIFICATION — Phase 2 implementation  
**Priority:** HIGH (post-launch critical)  
**Effort:** 3-4 hours  
**Source:** Cavekit (920⭐), B.10 comparison  

### Purpose

Automatically capture and learn from test failures by:
- Parsing test failure output (error messages, stack traces)
- Extracting failure patterns (common causes, recurring issues)
- Updating vault with warnings/notes to prevent future repeats
- Creating feedback loop: Test failures → Vault learnings → Better specs → Fewer failures

### Workflow

**When:** During `/spek.conclude` Step 3 (Generate Lessons)

```
/spek.post Step 3: Generate Lessons (Enhanced)
  1. Generate lesson markdown
  2. [NEW] Run test failure analysis
     a. Get last test run results
     b. Parse failure output
     c. Extract patterns + affected modules
     d. Create failure log (wiki/vault/failures/...)
     e. Update related decisions/patterns with warnings
  3. Tag lesson with failure patterns
  4. Auto-link + auto-tag
  5. Save lesson + failure log
```

### Failure Pattern Extraction

**Input:** Test output (JSON, TAP, or text format)

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
  5. Create failure record linking to related decisions/patterns
```

### Vault Integration: Failure Records

**New File:** `wiki/vault/failures/<YYYY-MM-DD>-<feature>-failures.md`

**Format:**

```markdown
---
title: "Test Failures: Auth Refactor Feature"
type: "failure-log"
tags: ["failure", "domain/authentication", "feature/auth-refactor"]
related_decisions: ["[[use-singleton-pattern]]", "[[token-lifecycle-decision]]"]
patterns_affected: ["concurrent-access", "async-performance"]
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

**Root Cause:** Singleton auth service received concurrent refresh requests; both tried simultaneously without lock

**Fix Applied:** Added mutex lock around refresh operation

**Future Prevention:**
- When using singleton pattern, always add locks
- Document in [[singleton-pattern]]: "WARNING: Not thread-safe by default"
- Consider linting rule for concurrent access

**Updated in Vault:**
- [[singleton-pattern]]: Added warning about concurrent access
- [[token-lifecycle-decision]]: Noted lock requirement
```

### Auto-Update to Related Decisions

When a failure is analyzed, backprop automatically updates related vault items with warnings:

```markdown
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

### Context Integration

When loading context for next feature, surface failure warnings:

```
/spek.context Step 3 [NEW]: Failure Warnings Check
  → Query wiki/vault/failures/ for recent failures
  → Filter by related domain/patterns
  → Alert user: "Previous auth feature had race conditions; review [[singleton-pattern]] warnings"
```

### Configuration

Add to `.spekificity/config.yaml`:

```yaml
backprop:
  enabled: true
  
  test_frameworks:
    - jest
    - pytest
    - mocha
  
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

### Success Criteria

- ✅ Test failure parsing + pattern extraction working
- ✅ Failure logs created in `wiki/vault/failures/` with Zettelkasten format
- ✅ Related decisions/patterns auto-updated with failure warnings
- ✅ Lessons tagged with failure patterns
- ✅ `/spek.context` surfaces past failure warnings
- ✅ ~70% of failure patterns auto-categorized
- ✅ Zero test failures slip past without vault record
- ✅ Future features query vault and avoid repeating mistakes

---

## SECTION 3: RARV Reflection Cycle: Reason-Act-Reflect-Verify

**Status:** SPECIFICATION — Phase 2 implementation  
**Priority:** HIGH (post-launch critical)  
**Effort:** 4-5 hours  
**Source:** Loki Mode (930⭐), B.10 comparison  

### Purpose

Implement continuous alignment verification loop that:
- **Reasons:** Did implementation match spec?
- **Acts:** Fix any spec/plan/code deviations
- **Reflects:** Update decisions if justified
- **Verifies:** Re-validate against original decisions

**Goal:** Prevent spec drift; ensure code aligns with architectural decisions; catch misalignments early.

### Four Phases

#### Phase 1: REASON — Code vs. Spec Comparison

After `/spek.implement` completes, compare:
- Spec requirements → Implemented features
- Plan architecture → Actual structure
- Feature scope → Delivered code

**Output:**

```yaml
reason_results:
  spec_coverage: 95%
  scope_changes: [
    { type: "addition", item: "batch token refresh", reason: "not in spec, added for perf" },
    { type: "omission", item: "audit logging", reason: "deferred to v2" }
  ]
  architecture_alignment: 92%
  deviations: [
    { plan_says: "singleton", code_does: "factory", impact: "medium" }
  ]
```

#### Phase 2: ACT — Fix Deviations

User reviews REASON output and chooses per deviation:

- **Option A:** Fix code to match spec (re-implement)
- **Option B:** Update spec to justify deviation (accept)
- **Option C:** Defer to next feature (tech debt)

**Example:**

```
Deviation: Code uses factory pattern, plan says singleton

User choice: Accept (Option B)
Rationale: "Factory provides better testability"

Action:
  1. Update plan.md: "Use factory pattern"
  2. Update decisions: "Why factory: testability > simplicity"
  3. Continue to Phase 3
```

#### Phase 3: REFLECT — Update Decisions

After deviations resolved (or accepted):
- Compare final implementation against vault decisions
- For each changed decision, document rationale
- Update vault with decision changes
- Add new patterns discovered

**Output:**

```yaml
reflect_results:
  decisions_verified: 7
  decisions_changed: 2
  new_patterns_discovered: 1
  
  changed_decisions:
    - decision: "use singleton for auth service"
      change: "use factory instead"
      rationale: "better testability, lower coupling"
      action: "update wiki/vault/decision-auth-service-pattern.md"
```

#### Phase 4: VERIFY — Re-Validate Alignment

After Phase 3 changes applied:
- Re-run decision checks
- Verify new/updated decisions are consistent
- Check for conflicts between decisions
- Verify code still passes tests

**Output:**

```yaml
verify_results:
  all_decisions_aligned: true
  code_tests_passing: true
  no_conflicts_detected: true
  alignment_score: 98%
  status: "✓ RARV complete; implementation aligned"
```

### RARV Loop Patterns

**Simple 1-Pass (Most Features):**

```
Spec → Plan → Implement → RARV (1 pass) → Post
```

**Multi-Pass (Complex Features):**

```
Spec → Plan → Implement (Phase 1)
  → RARV: Reason shows issues
  → ACT: Fix code/spec
  → Implement (Phase 2)
  → RARV again: Aligned
  → REFLECT + VERIFY
  → Post
```

**Mid-Feature (Optional):**

```
User: "I'm uncertain about service pattern"
  → /spek.rarv --partial
  → See deviations so far
  → Adjust + continue
  → Full RARV at end confirms alignment
```

### Integration: /spek.post Step 7

```
/spek.post Step 7: RARV Reflection Cycle (Enhanced)

  7.1. REASON: Compare code vs. spec
  7.2. ACT: Fix deviations (if any)
  7.3. REFLECT: Update decisions + patterns
  7.4. VERIFY: Re-validate alignment

→ If alignment < 90%: Alert user
→ If alignment >= 90%: Continue to Step 8
```

### Configuration

Add to `.spekificity/config.yaml`:

```yaml
rarv:
  enabled: true
  default_phase: "reason-verify"
  
  # Alignment thresholds
  min_alignment_score: 90
  alignment_definitions:
    scope_coverage: 0.4  # Spec requirements met
    architecture_match: 0.35  # Plan vs code
    decision_consistency: 0.25  # Decisions reflected
  
  # Options
  fail_on_deviation: false
  generate_alignment_report: true
  auto_regenerate_plan_on_major_deviation: false
```

### Success Criteria

- ✅ REASON phase compares code against spec with 80%+ accuracy
- ✅ ACT phase lets user choose: Fix/Accept/Defer
- ✅ REFLECT phase auto-updates vault decisions + patterns
- ✅ VERIFY phase confirms alignment > 90%
- ✅ Multi-pass loops supported
- ✅ Integrated into `/spek.post` Step 7
- ✅ Mid-feature `/spek.rarv` command available
- ✅ Alignment reports generated for every feature
- ✅ Decision drift prevented across features

---

## SECTION 4: Blind Code Review

**Status:** SPECIFICATION — Phase 2 (optional enhancement)  
**Priority:** MEDIUM (optional, quality improvement)  
**Effort:** 4-5 hours  
**Source:** Pilot Shell, Loki Mode  

### Purpose

Implement optional second-pass code review that:
- **Strips** implementation metadata (AI markers, comments)
- **Anonymizes** code to remove context bias
- **Runs** independent review checks (linters, tests, style)
- **Catches** AI-specific issues (hallucinations, over-reliance on context)
- **Flags** issues for developer attention before production

### Workflow

#### Step 1: Anonymize Code

**Removes:**
- Comments mentioning "AI-generated" or "Claude"
- Implementation rationale comments
- Feature names and author metadata

**Keeps:**
- Code logic + structure
- Inline comments (stripped of AI context)
- Test cases
- Error handling

**Example:**

**Original:**
```typescript
// Claude-generated auth service using dependency injection
// Task: auth-module

export class AuthService {
  constructor(private readonly tokenManager: TokenManager) {}
  async refreshToken() {
    // Exponential backoff retry (3 attempts)
    try {
      return await this.tokenManager.refresh();
    } catch (error) {
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
      return await this.manager.refresh();
    } catch (error) {
      return this.retryWithBackoff(error);
    }
  }
}
```

#### Step 2: Run Review Checks

**Checks Include:**

- **Linting:** ESLint, Pylint, etc. (style, unused vars, complexity)
- **Tests:** All tests passing? Coverage above threshold (80%)?
- **Static Analysis:** Security vulnerabilities, common bugs, memory leaks
- **Style Consistency:** Naming conventions, function length, cyclomatic complexity

#### Step 3: Report Issues

**Output:**

```
Blind Code Review Report
========================

File: src/auth/service.ts
  ✗ ESLint: Line 24 - unused variable 'tempToken'
  ✗ Coverage: 72% (below 80% threshold)
  ✓ Tests: All passing
  ✗ Style: Function too long (150 lines, max: 100)
  ✓ Security: No vulnerabilities

Summary:
  Total issues: 3
  Severity: High (1), Medium (2)
  Status: Review issues before production
```

#### Step 4: User Action

User reviews report and:
- **Option A:** Fix all issues → Re-run blind review
- **Option B:** Accept issues → Document rationale
- **Option C:** Defer to next sprint → Create tech debt item

### Integration: /spek.post Step 8b

```
/spek.post Step 8: Simplify Docs

/spek.post Step 8b [NEW]: Blind Code Review (Optional)
  IF enable_blind_review: true
    1. Anonymize code changes
    2. Run review checks (linters, tests, style)
    3. Generate report
    4. Surface issues (don't block post)
    5. User can: Fix / Accept / Defer

/spek.post Step 9: Archive Session
```

### Configuration

Enable in `.spekificity/config.yaml`:

```yaml
review:
  enable_blind_review: false  # Set to true
  
  review_tool: "github_actions"  # or "local"
  
  checks:
    linting: true
    tests: true
    coverage_threshold: 80
    style_consistency: true
    security_scan: true
  
  failure_policy: "alert"  # or "block"
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
          find src -name "*.ts" -o -name "*.js" | \
          xargs sed -i '/Claude-generated/d' | \
          xargs sed -i '/AI-generated/d'
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Check coverage
        run: npm run test:coverage 2>&1 | grep -q "80%"
      
      - name: Comment PR with report
        uses: actions/github-script@v6
```

### Success Criteria

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

## Adoption Roadmap

### Phase 2 Implementation (Recommended Priority)

**HIGH Priority (Implement First):**
1. **Anti-Sycophancy Rules** — Prevents AI drift during planning
2. **Backprop Reflex** — Learns from test failures
3. **RARV Reflection** — Verifies code-spec alignment

**MEDIUM Priority (Nice-to-Have):**
4. **Blind Code Review** — Independent quality check (optional enhancement)

### Configuration Template

```yaml
# .spekificity/config.yaml

validation_patterns:
  anti_sycophancy:
    enabled: true
    rules:
      contradiction_detection: true
      complexity_increase: true
      pattern_consistency: true
      tech_stack_drift: true
      scope_creep_detection: true
  
  backprop_reflex:
    enabled: true
    test_frameworks: [jest, pytest, mocha]
    vault_update: true
  
  rarv_reflection:
    enabled: true
    min_alignment_score: 90
    fail_on_deviation: false
  
  blind_code_review:
    enabled: false  # Optional; set to true to enable
    coverage_threshold: 80
    checks: [linting, tests, style, security]
```

---

## Related Specifications

**Memory Architecture:**
- memory-architecture.md (vault storage for lessons, decisions, patterns)

**Command Specs:**
- spek-post-command.md (Step 3, 7, 8b integration)
- spek-conclude-command.md (Step 3, 7, 8b integration)
- spek-plan-workflow.md (specify/plan phase integration)

**Quality & Learning:**
- lessons-format.md (lesson document format)
- architectural-decisions.md (decision storage + sync)
- patterns-library.md (pattern discovery + reuse)
- error-handling-and-recovery.md (error strategy complementing validation)

**Framework Analysis:**
- sdd-framework-comparison-analysis.md (source: Loki Mode, Cavekit, Pilot Shell patterns)

---

## References

**Production Sources:**
- **Loki Mode** (930⭐): Anti-sycophancy rules, RARV reflection
- **Cavekit** (920⭐): Backprop reflex pattern
- **Pilot Shell:** Blind code review pattern
- **SDD Ecosystem:** Validation pattern analysis (B.10)

---

## Consolidated Notes

This file consolidates 4 validation pattern specifications (C.3.6, C.3.7, C.3.8, C.3.9) that were previously scattered across the specs/ directory. All 4 patterns share a common theme: **preventing AI drift and learning from failures** to create a feedback loop of continuous improvement.

**Why consolidated?**
- All 4 patterns serve similar purpose (validation + learning)
- Related status (Phase 2 implementation, post-launch features)
- Integration points overlap (/spek.post, /spek.plan, /spek.context)
- Users benefit from seeing all options in one place

**Original files (now archived):**
- `anti-sycophancy.md` (C.3.8)
- `blind-code-review.md` (C.3.9)
- `backprop-reflex.md` (C.3.6)
- `rarv-reflection.md` (C.3.7)

**Usage:** Refer to this file as primary reference. Original files may be removed in future consolidation pass.
