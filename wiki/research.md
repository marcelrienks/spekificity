# Spekificity Adoption Research

**Status:** Research Complete (2026-05-18)  
**Sources:** B.9 (claude-code-memory-setup), B.10 (SDD Framework Comparison), B.8.1-B.8.4 (Architectural Specs)  
**Purpose:** Synthesize adoption recommendations from session research for user decision-making

---

## Overview

This document lists **patterns, features, and enhancements** identified during B.1-B.11 architectural specification research. Each adoption is categorized by priority, includes rationale, implementation effort, and dependency information.

**Goal:** Enable informed decision-making about which adoptions to implement in B.12+ (implementation phase).

---

## SHOULD Adopt (High Priority)

These are **strongly recommended** based on production validation and alignment with core Spekificity design.

### S1. Zettelkasten Conventions for Vault Notes

**From:** B.9 (claude-code-memory-setup, 659⭐, active open-source project)

**What it is:**
- Mandatory YAML frontmatter on vault notes (title, tags, created, updated, status, type)
- Dense wikilinks (minimum 2 per note)
- Atomic notes (one concept per file)
- Kebab-case filenames

**Why adopt:**
- ✅ Informed by production examples that report large token savings
- ✅ Enables graph navigation in Obsidian
- ✅ Makes lessons discoverable by future `/spek.context` loads
- ✅ Zero conflicts with current design (B.8.2 vault already uses metadata)

**Implementation:**
- Update `vault/decision.md`, `vault/patterns.md`, `vault/lessons/` with frontmatter template
- Add wikilink generation logic to `/spek.post` Step 3 (Generate Lessons)
- Document in `.spekificity/guides/vault-conventions.md`

**Effort:** 3-4 hours

**Affected files:**
- `specs/b8-4-prepare-and-post-skills.md` (enhance Step 3)
- `.spekificity/guides/vault-conventions.md` (new)
- Implementation: `/spek.post` skill

**Dependencies:** None (can be done immediately)

---

### S2. Auto-Tagging + Auto-Wikilink-Insertion for Lessons

**From:** B.9 (chat import pipeline pattern)

**What it is:**
- Extract keywords from generated lessons
- Map to existing vault items (patterns, decisions, lessons)
- Auto-insert `[[wikilink]]` references
- Auto-generate tags (domain, tech stack, methodology)

**Why adopt:**
- ✅ Reduces manual linking work (~70% of linking could be automated)
- ✅ Creates natural interconnection in vault
- ✅ Enables knowledge discovery across features
- ✅ Validates lessons against prior patterns

**Implementation:**
1. Create KEYWORD_TAG_MAP in `.spekificity/config.yaml`
   ```yaml
   keyword_tag_map:
     # Architecture patterns
     "singleton": ["pattern/singleton", "design-pattern"]
     "dependency-injection": ["pattern/di", "architecture"]
     "state-management": ["pattern/state", "frontend"]
     
     # Tech stack
     "react": ["tech/react", "frontend"]
     "typescript": ["tech/typescript", "backend"]
     
     # Methodology
     "tdd": ["method/tdd", "testing"]
     "mutation-testing": ["method/mutation", "testing"]
   ```

2. Enhance `/spek.post` Step 3 with auto-linking logic:
   - Scan lesson for keywords
   - Query `vault/pattern.md`, `vault/decision.md`, `vault/lessons/` for matches
   - Insert wikilinks programmatically
   - Add tags to YAML frontmatter

3. Document in `.spekificity/guides/auto-linking.md`

**Effort:** 4-6 hours

**Affected files:**
- `.spekificity/config.yaml` (add KEYWORD_TAG_MAP)
- `specs/b8-4-prepare-and-post-skills.md` (enhance Step 3)
- Implementation: `/spek.post` skill

**Dependencies:** S1 (Zettelkasten conventions)

---

### S3. 3-Layer Query Rule Documentation & Enforcement

**From:** B.9 (claude-code-memory-setup, 71x token savings)

**What it is:**
```
Layer 1: Query graph.json (structure, connections) — 280 tokens
Layer 2: Query vault (decisions, patterns, lessons) — 500 tokens
Layer 3: Read raw code files (only when needed) — 5000+ tokens
```

**Why adopt:**
- ✅ Can reduce token waste substantially when done correctly
- ✅ Prioritizes cached/indexed data over expensive file re-reads
- ✅ Already planned in B.8.2 memory model; just needs explicit documentation
- ✅ Supported by external examples that report large savings in real usage

**Implementation:**
1. Create `.spekificity/guides/context-navigation.md` with:
   - Explanation of 3-layer model
   - When to query each layer
   - Example queries
   - Token cost breakdown

2. Add to `copilot-instructions.md`:
   ```markdown
   ## Context Navigation (3-Layer Query Rule)
   
   When gathering context, follow this priority:
   1. Query graph first (fast, indexed, cached)
   2. Query vault second (searchable, compiled)
   3. Read code only if layers 1-2 insufficient
   
   This reduces token cost by ~20x.
   ```

3. Implement in `/spek.context` skill:
   - Query graph first → fall back to vault → fall back to code
   - Log which layers were queried for transparency

**Effort:** 2-3 hours

**Affected files:**
- `.spekificity/guides/context-navigation.md` (new)
- `copilot-instructions.md` (enhance)
- Implementation: `/spek.context` skill

**Dependencies:** None (B.11 graph setup already specifies query contracts)

---

### S4. Graphify Git Hooks Integration

**From:** B.9 (claude-code-memory-setup), B.11 (Codegraph setup spec)

**What it is:**
- `graphify hook install` → auto-rebuild code graph on post-commit
- `graphify . --update` → incremental refresh with SHA256 caching
- Optional watch mode for interactive dev

**Why adopt:**
- ✅ Already planned in B.8.4 `/spek.post` Step 6
- ✅ Keeps graph fresh without manual intervention
- ✅ Prevents stale graph queries (saves debugging time)
- ✅ Zero additional effort (B.11 spec already covers this)

**Implementation:**
- Integrate into `.spekificity/bin/spek setup` script:
  ```bash
  # During setup:
  graphify hook install  # Auto-install post-commit hook
  ```
- Document in `.spekificity/guides/quickstart.md`
- Add optional config flag:
  ```yaml
  graphify:
    refresh:
      enable_git_hook: true  # Auto-sync on commits
  ```

**Effort:** 1 hour (already specified in B.11)

**Affected files:**
- `.spekificity/bin/spek setup` (add hook installation)
- `.spekificity/guides/quickstart.md` (document)

**Dependencies:** B.11 (Codegraph setup spec)

---

### S5. Session Logs as Explicit Vault Artifacts

**From:** B.9 (claude-code-memory-setup)

**What it is:**
- Archive `/memories/session/current-feature.md` to `vault/lessons/<date>-<feature>-*.md`
- Extract structured sections (What Was Done, Decisions, Patterns, Pending)
- Add wikilinks during archival
- Make session logs searchable + linkable

**Why adopt:**
- ✅ Provides audit trail of feature development
- ✅ Enables cross-feature pattern discovery
- ✅ Already partially implemented in B.8.4 `/spek.post` Step 9 (Archive Session Memory)
- ✅ Enhances lessons with execution context

**Implementation:**
- Enhance `/spek.post` Step 9 (Archive Session Memory):
  1. Extract sections from `/memories/session/current-feature.md`
  2. Map to `vault/lessons/<date>-<feature>-session.md`
  3. Add structured YAML frontmatter
  4. Insert wikilinks to related decisions/patterns
  5. Commit to vault

**Effort:** 2-3 hours

**Affected files:**
- `specs/b8-4-prepare-and-post-skills.md` (enhance Step 9)
- Implementation: `/spek.post` skill

**Dependencies:** S1 (Zettelkasten conventions), S2 (Auto-linking)

---

## COULD Adopt (Medium Priority)

These are **recommended for future phases** based on proven patterns, but not required for initial implementation.

### C1. Backprop Reflex (Test Failures → Vault Updates)

**From:** B.10 (Cavekit, 920⭐)

**What it is:**
- Automatic feedback from test failures
- Failures parsed and added to vault/decision.md or vault/patterns.md
- Future features query vault and avoid same mistakes

**Flow:**
```
Feature implementation
  ↓
Run tests
  ↓ Test fails
Parse failure → Extract pattern → Add to vault
  ↓
Suggest updated pattern for next feature
```

**Why adopt (medium priority):**
- ✅ Reduces repeat mistakes across features
- ✅ Informed by Cavekit usage in active projects
- ✅ Elegant, minimal implementation
- ⚠️ Depends on automated testing infrastructure (not all teams have this)

**Implementation:**
1. In `/spek.post` Step 3 (Generate Lessons), add test analysis:
   ```
   If test failures detected:
     1. Parse failure output
     2. Extract failure pattern
     3. Identify related decision/pattern in vault
     4. Add warning/note to vault/decision.md
     5. Tag future specs with this decision
   ```

2. In `/spek.context` Step 3, surface recent failures:
   ```
   When loading context, check for recent test failures
   Alert: "Previous feature had failures in X; consider pattern Y"
   ```

**Effort:** 3-4 hours

**Timeline:** Post B.12 (after basic skills working)

**Affected files:**
- Implementation: `/spek.post` skill (enhance Step 3)
- Implementation: `/spek.context` skill (enhance Step 3)

**Dependencies:** S1, S2 (Zettelkasten + auto-linking), automated test runner

---

### C2. RARV Reflection Cycles (Reason-Act-Reflect-Verify)

**From:** B.10 (Loki Mode, 930⭐)

**What it is:**
```
After implementation:
  Reason: Did code match spec?
  Act: Fix any deviations
  Reflect: Compare against original decisions
  Verify: Run validation
  → Loop if issues found
```

**Why adopt (medium priority):**
- ✅ Continuous alignment between spec and code
- ✅ Proven in multi-agent systems (Loki Mode)
- ✅ Reduces regressions and spec drift
- ⚠️ Requires loop-back from `/spek.implement` to `/spek.post` (orchestration complexity)

**Implementation:**
1. Add post-implementation reflection to `/spek.post`:
   - Compare code against original spec (auto-diff)
   - Identify deviations
   - Update decisions/patterns if justified
   - Flag unresolved gaps

2. Add feedback loop option:
   - If significant deviations found, offer to re-run plan
   - Iterate until aligned

**Effort:** 4-5 hours (orchestration + comparison logic)

**Timeline:** Post B.14 (after integration testing works)

**Affected files:**
- Implementation: `/spek.post` skill (add reflection phase)
- Possibly: CLI orchestration layer

**Dependencies:** S1, S2, test infrastructure

---

### C3. Anti-Sycophancy Validation Rules

**From:** B.10 (Loki Mode, 930⭐)

**What it is:**
- Explicit rules prevent agent from over-agreeing with earlier decisions
- Flags contradictions and decision conflicts
- Examples:
  - "If 3+ recent patterns suggest different approach, flag conflict"
  - "If test coverage drops >5%, alert"
  - "If complexity increases without justification, question"

**Why adopt (medium priority):**
- ✅ Prevents AI drift from architectural decisions
- ✅ Catches over-reliance on recent context
- ✅ Proven in enterprise systems (Loki)
- ⚠️ Requires defining rules per project (one-time setup)

**Implementation:**
1. Create `.spekificity/validation-rules.md` (default rules):
   ```markdown
   ## Validation Rules (Anti-Sycophancy)
   
   ### Specification Phase (inside `/spek.automate`)
   - Rule: If spec contradicts vault/decision.md entries, flag conflict
   - Rule: If spec complexity > 50% higher than similar past features, question
   
   ### Planning Phase (inside `/spek.automate`)
   - Rule: If plan ignores code graph insights (e.g., known bottleneck), flag
   - Rule: If plan deviates from architectural patterns, justify deviation
   
   ### Implementation (/spek.implement)
   - Rule: If code violates vault/decision.md architectural decisions, require justification
   - Rule: If test coverage drops >5% from project baseline, fail implementation
   ```

2. Add validation checks to workflow phases:
   - `/spek.automate` specify phase: Compare spec against vault decisions
   - `/spek.automate` plan phase: Compare plan against code graph + decisions
   - `/spek.implement`: Validate against test coverage + architectural constraints

**Effort:** 3-4 hours

**Timeline:** Post B.13 (after skills stabilize)

**Affected files:**
- `.spekificity/validation-rules.md` (new)
- Implementation: workflow phases inside `/spek.automate`, plus `/spek.implement`

**Dependencies:** Vault populated with decisions/patterns, test infrastructure

---

### C4. Blind Code Review

**From:** B.10 (Pilot Shell, Loki Mode)

**What it is:**
- Code reviewed without context of how/why it was generated
- Catches AI-specific biases (hallucinations, over-reliance on context)
- Optional second-pass review

**Why adopt (medium priority):**
- ✅ Improves code quality (independent review)
- ✅ Catches AI-specific issues
- ✅ Proven in production (Pilot Shell)
- ⚠️ Requires code review infrastructure (GitHub Actions, diff tools)

**Implementation:**
1. Optional `/spek.post` Step 8b (Blind Review):
   ```
   If enable_blind_review: true
     1. Strip implementation comments/headers
     2. Format code for anonymous review
     3. Run review checks (linters, tests)
     4. If issues found, flag for developer attention
   ```

2. Config option:
   ```yaml
   review:
     enable_blind_review: false  # Optional
     review_tool: "github_actions"  # or "custom"
   ```

**Effort:** 4-5 hours

**Timeline:** Post B.13 (after code generation stabilizes)

**Affected files:**
- `.spekificity/config.yaml` (add review section)
- Implementation: `/spek.post` skill (add Step 8b)

**Dependencies:** Code review tool (GitHub Actions, etc.), test infrastructure

---

### C5. Token Budget Allocation Tracking

**From:** B.10 (Pilot Shell)

**What it is:**
- Allocate tokens per phase (Specify, Plan, Implement, Post)
- Track actual usage vs. budget
- Alert if any phase exceeds budget

**Example:**
```
Per-feature token budget:
  Specify:    2000 tokens (minimal)
  Plan:       3000 tokens (detailed design)
  Implement:  5000 tokens (code + testing)
  Post:       2000 tokens (lessons + archival)
  ──────────────────────
  Total:     12000 tokens / feature
```

**Why adopt (medium priority):**
- ✅ Prevents runaway token costs
- ✅ Encourages efficiency at each phase
- ✅ Easy to track (already using caveman compression)
- ⚠️ Requires monitoring infrastructure (token counter)

**Implementation:**
1. Add to `.spekificity/config.yaml`:
   ```yaml
   token_budget:
     per_feature: 12000
     specify_phase: 2000
     plan_phase: 3000
     implement_phase: 5000
     post_phase: 2000
     alert_threshold_percent: 80  # Alert at 80% of budget
   ```

2. Enhance `/spek.context`, `/spek.prepare`, `/spek.post` to track usage:
   - Log tokens at each phase
   - Alert if phase exceeds budget
   - Suggest compression if needed

3. Add report to `/spek.post` completion summary

**Effort:** 2-3 hours

**Timeline:** Can be added anytime (useful data point)

**Affected files:**
- `.spekificity/config.yaml` (add token_budget section)
- Implementation: monitoring in each skill

**Dependencies:** Token counting infrastructure (Claude API usage tracking)

---

## RECOMMENDED (Next-Phase Enhancement)

These are **not required** for initial implementation but add significant value post-launch.

### R1. Lesson Cross-Feature Discovery

**What it is:**
- Query vault/lessons/ across multiple features
- Surface related patterns and decisions
- Show patterns used in similar features

**Why recommend:**
- ✅ Enables organizational learning
- ✅ Improves code reuse
- ⚠️ Requires substantial lesson library to be valuable

**Implementation:** Post B.12 (after several features complete)

---

### R2. Cross-Project Vault (Future)

**From:** B.9 (claude-code-memory-setup future consideration)

**What it is:**
- Single global vault for all user/team projects (instead of per-workspace)
- Cross-project pattern discovery
- Unified lessons library

**Why recommend:**
- ✅ Enables organizational learning across projects
- ✅ Pattern discovery (what works in Project A might help Project B)
- ⚠️ Increases coupling; requires careful namespace management

**Timeline:** Post B.14 (after single-workspace implementation proven)

---

### R3. Watch Mode for Dev Workflow

**From:** B.9 (claude-code-memory-setup)

**What it is:**
- `graphify . --watch` auto-rebuilds code graph on file save
- Optional mode for interactive development

**Why recommend:**
- ✅ Real-time graph updates during coding
- ✅ Useful for long-running `/spek.implement` sessions
- ⚠️ Nice-to-have; not essential for core workflow

**Timeline:** Post B.12 (when core implementation working smoothly)

---

### R4. Steering Files / Project Rules

**From:** B.10 (Kiro)

**What it is:**
- `.spekificity/steering-rules.md` for project-scoped guidance
- Architectural constraints, tech stack rules, naming conventions
- Non-code way to steer agent behavior

**Why recommend:**
- ✅ Flexible per-project configuration
- ✅ Easy to update without touching code
- ⚠️ Requires project to define rules (one-time setup per team)

**Timeline:** Post B.12 (useful for team collaboration)

---

## DO NOT Adopt (Intentional Exclusions)

These are patterns from other frameworks that Spekificity **deliberately does not** adopt.

### X1. Heavy Python Dependency

**Why NOT:** Creates friction for non-Python teams. Spekificity keeps shell-agnostic where possible.

### X2. Rigid Mandatory Phase Gates

**Why NOT:** OpenSpec shows optional phases work better. All phases in Spekificity should be optional.

### X3. Single-Source-of-Truth Specs

**Why NOT:** Limits human review and editing. Spekificity keeps artifacts separate (spec.md, plan.md, tasks.md) for flexibility.

### X4. Vendor Lock-In

**Why NOT:** Spekificity wraps SpecKit (decorator pattern) to stay framework-agnostic and switching-friendly.

### X5. Cloud-Hosted Mandate

**Why NOT:** Self-hosted + git-backed for maximum user control and auditability.

---

## Implementation Roadmap

### Phase 1: Immediate (B.12 Skills Development)

**SHOULD adopt (required for core workflow):**
- ✅ S1: Zettelkasten conventions
- ✅ S2: Auto-tagging + auto-linking
- ✅ S3: 3-layer query rule documentation
- ✅ S4: Graphify git hooks
- ✅ S5: Session logs as vault artifacts

**Effort:** 12-15 hours (distributed across skill development)

**Timeline:** Integrate during B.12 (agent skills creation)

---

### Phase 2: Post-Launch (B.13-B.14)

**COULD adopt (medium priority, after basics working):**
- ⚠️ C1: Backprop reflex (requires test infrastructure)
- ⚠️ C2: RARV cycles (requires orchestration)
- ⚠️ C3: Anti-sycophancy rules (requires decision vault populated)
- ⚠️ C4: Blind code review (requires review tool)
- ⚠️ C5: Token budget tracking (quick win, any time)

**Effort:** 15-20 hours (distributed, iterative)

**Timeline:** After B.14 integration testing succeeds

---

### Phase 3: Future Enhancement (Post-Launch)

**RECOMMENDED (next phase after stable):**
- 🔮 R1: Cross-feature lesson discovery
- 🔮 R2: Cross-project vault
- 🔮 R3: Watch mode
- 🔮 R4: Steering rules

**Effort:** 20+ hours (based on user feedback)

**Timeline:** Q3 2026+

---

## Decision Matrix for User Review

| Adoption | Priority | Effort | Benefit | Dependencies | Recommend? |
|----------|----------|--------|---------|--------------|-----------|
| S1. Zettelkasten | HIGH | 3-4h | High (indexing) | None | **YES** |
| S2. Auto-linking | HIGH | 4-6h | High (discovery) | S1 | **YES** |
| S3. 3-Layer Rule | HIGH | 2-3h | High (token savings) | None | **YES** |
| S4. Git Hooks | HIGH | 1h | High (auto-refresh) | B.11 | **YES** |
| S5. Session Logs | HIGH | 2-3h | Medium (audit trail) | S1, S2 | **YES** |
| C1. Backprop | MEDIUM | 3-4h | Medium (learning) | Tests | Optional |
| C2. RARV | MEDIUM | 4-5h | Medium (alignment) | Tests | Optional |
| C3. Anti-Syco | MEDIUM | 3-4h | Medium (drift prevention) | Vault | Optional |
| C4. Blind Review | MEDIUM | 4-5h | Medium (QA) | Review tool | Optional |
| C5. Token Budget | MEDIUM | 2-3h | Low (monitoring) | None | Quick Win |
| R1. Cross-Feature | MEDIUM | TBD | Medium (learning) | S1, S2 | Future |
| R2. Cross-Project | LOW | TBD | Medium (scale) | Tests | Future |
| R3. Watch Mode | LOW | TBD | Low (nice-to-have) | B.11 | Future |
| R4. Steering Rules | LOW | TBD | Medium (guidance) | Tests | Future |

---

## Recommendation Summary

### For B.12 Implementation

**Implement all SHOULD adoptions (S1-S5):**
- These are production-validated patterns
- Zero conflicts with core design
- Effort ~12-15 hours (distributed across skills)
- High impact on usability + token efficiency

**Optional: S5 token budget tracking** (quick win)

### For B.13+ (After Initial Launch)

**Assess COULD adoptions (C1-C5) based on:**
- Team infrastructure (do you have automated tests?)
- Use cases (is preventing repeat mistakes important?)
- User feedback (what problems do teams encounter?)

### For Future (Post-Launch)

**Plan RECOMMENDED adoptions (R1-R4) based on:**
- Real-world usage patterns
- Team growth and cross-project collaboration
- Operational feedback

---

## How to Use This Document

1. **Review section by section** with team
2. **Mark decisions** (Adopt / Skip / Defer) in margin
3. **Create GitHub issues** for each "Adopt" decision
4. **Prioritize issues** into B.12 sprint
5. **Archive this document** as reference for implementation

---

## Questions for Team

1. **Automated testing:** Do you have CI/CD with test automation? (Affects C1, C2, C3, C4)
2. **Code review process:** Do you have GitHub Actions or similar for code review? (Affects C4)
3. **Team scale:** Are you solo, team, or enterprise? (Affects R2 cross-project vault)
4. **Token constraints:** Is token efficiency critical? (Affects priority of S3, C5)
5. **Learning culture:** Is capturing lessons important for your team? (Affects priority of S5, C1)

---

## Phased Implementation Plan (Action Items)

### Phase 1: SHOULD Adopt (B.12 - Core Workflow Implementation)

**Status:** Ready for implementation in separate session

Create specs and implement the following 5 high-value adoptions during B.12 agent skill development:

| ID | Item | Effort | Priority | Spec Item |
|----|------|--------|----------|-----------|
| S1 | Zettelkasten conventions for vault notes | 3-4h | **MUST** | C.3.1 |
| S2 | Auto-tagging + auto-wikilink insertion | 4-6h | **MUST** | C.3.2 |
| S3 | 3-Layer query rule documentation | 2-3h | **MUST** | C.3.3 |
| S4 | Graphify git hooks integration | 1h | **MUST** | C.3.4 |
| S5 | Session logs as vault artifacts | 2-3h | **MUST** | C.3.5 |

**Total Effort:** 12-15 hours (distributed across B.12 skill implementation)

**Integration Points:**
- S1, S2: Integrate into `/spek.post` Step 3 (Lesson Generation)
- S3: Integrate into `/spek.context` + `copilot-instructions.md`
- S4: Integrate into `.spekificity/bin/spek setup`
- S5: Integrate into `/spek.post` Step 9 (Archive Session Memory)

**Acceptance Criteria:**
- ✅ Vault lessons have frontmatter (title, tags, created, updated, status, type)
- ✅ Vault lessons auto-generate wikilinks to related decisions/patterns
- ✅ copilot-instructions.md documents 3-layer query rule
- ✅ Setup script installs graphify git hooks
- ✅ Session logs archived to vault with structured YAML frontmatter

---

### Phase 2: COULD Adopt (B.13-B.14 - Post-Launch Enhancements)

**Status:** Defer to after B.12 integration testing succeeds

Evaluate and implement these 5 medium-priority features based on team infrastructure:

| ID | Item | Effort | Depends On | Spec Item |
|----|------|--------|-----------|-----------|
| C1 | Backprop reflex (test failures → vault) | 3-4h | Tests | C.3.6 |
| C2 | RARV reflection cycles | 4-5h | Tests | C.3.7 |
| C3 | Anti-sycophancy validation rules | 3-4h | Vault | C.3.8 |
| C4 | Blind code review | 4-5h | Review tool | C.3.9 |
| C5 | Token budget allocation tracking | 2-3h | None | C.3.10 |

**Pre-Implementation Decision Gate:**
Before creating specs for C1-C5, answer these questions (from research.md "Questions for Team" section):

1. **Automated testing:** Do you have CI/CD with test automation?
   - YES → Proceed with C1, C2, C4 specs
   - NO → Skip C1, C2, C4; proceed with C3, C5 only

2. **Code review process:** Do you have GitHub Actions or similar for code review?
   - YES → Proceed with C4 spec
   - NO → Skip C4 spec

3. **Team scale:** Are you solo, team, or enterprise?
   - Solo → Focus on C3, C5 (personal discipline rules)
   - Team/Enterprise → Include C1, C2, C4 (team collaboration)

4. **Token constraints:** Is token efficiency critical?
   - YES → Prioritize C5 spec
   - NO → Lower priority on C5

5. **Learning culture:** Is capturing lessons important?
   - YES → Prioritize C1, C2 specs
   - NO → Lower priority

**Conditional Specs to Create:**
- If Tests + Team → Create C.3.6, C.3.7, C.3.9
- If Solo → Create C.3.8, C.3.10
- Always available → C.3.8, C.3.10

---

### Phase 3: RECOMMENDED (Post-Launch - Future Enhancement)

**Status:** Plan for Q3 2026+ based on real-world usage

Revisit after B.14 is stable and user feedback collected:

| ID | Item | Effort | Depends On | Spec Item |
|----|------|--------|-----------|-----------|
| R1 | Cross-feature lesson discovery | TBD | S1, S2 | C.3.11 |
| R2 | Cross-project vault (organizational scale) | TBD | S1, S2 | C.3.12 |
| R3 | Watch mode for dev workflow | TBD | B.11 | C.3.13 |
| R4 | Steering files / project rules | TBD | Tests | C.3.14 |

**Timeline:** Revisit after B.14 integration tests pass. Collect user feedback first.

---

### Phase 4: DO NOT Adopt (Intentional Exclusions)

**Status:** Confirmed out of scope

These patterns are explicitly NOT adopted due to design conflicts:

| ID | Item | Reason |
|----|------|--------|
| X1 | Heavy Python dependency | Shell-agnostic design |
| X2 | Rigid mandatory phase gates | All phases optional (SpecKit precedent) |
| X3 | Single-source-of-truth specs | Preserve separation (spec/plan/tasks) + human editing |
| X4 | Vendor lock-in | Decorator pattern keeps framework-agnostic |
| X5 | Cloud-hosted mandate | Self-hosted + git-backed for control |

**Decision:** No specs needed. Document exclusions in architecture.md rationale.

---

## Implementation Checklist

### Before B.12 Implementation Starts:

- [ ] User answers the 5 team infrastructure questions (Section: COULD Adopt)
- [ ] Team reviews Decision Matrix and marks Adopt/Skip/Defer for each item
- [ ] Create GitHub issues for Phase 1 (S1-S5) → integrate into B.12 sprint
- [ ] Archive this document as reference

### During B.12 Implementation:

- [ ] Integrate S1-S5 adoptions into agent skill specs
- [ ] Update `/spek.post`, `/spek.context`, setup scripts accordingly
- [ ] Test Zettelkasten frontmatter generation
- [ ] Test auto-wikilink insertion
- [ ] Test 3-layer query rule enforcement
- [ ] Verify git hooks installed during setup

### After B.13 Integration Testing:

- [ ] Review team answers to infrastructure questions
- [ ] Create specs for conditional C.3.x items
- [ ] Prioritize C1-C5 into B.13-B.14 sprints
- [ ] Implement based on priority + dependencies

### Post-Launch (Q3 2026+):

- [ ] Collect real-world usage patterns
- [ ] Create specs for R1-R4 based on user feedback
- [ ] Prioritize RECOMMENDED items
- [ ] Plan Phase 3 implementation

---

## Next Steps

1. **Answer the 5 team infrastructure questions** (in COULD Adopt section)
2. **Create todo items C.3.1-C.3.10** based on decisions
3. **Mark items** (Adopt / Skip / Defer) in todo.md
4. **Begin B.12 implementation** with Phase 1 (S1-S5 specs)
5. **Archive this document** as implementation reference
