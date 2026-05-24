# ATOMIC SPECIFICATION: Patterns Library (C2.3)

**Depends On:** lessons-format.md  
**Used By:** /spek.context (read at session start), `/spek.plan` plan phase (suggest patterns during planning)   

---

## Overview

A patterns library captures reusable solutions discovered during feature work. Stored in `wiki/vault/patterns.md`, it enables future features to learn from and apply proven approaches, reducing design decisions and accelerating implementation.

---

## Vault Patterns (wiki/vault/patterns.md)

### Purpose
Permanent collection of reusable patterns from all features; queryable by domain and frequency of use.

### File Structure

```markdown
# Patterns Library

## [Pattern Name]

**First Used:** spec-[number] (date)  
**Last Used:** spec-[number] (date)  
**Frequency:** used in N features  
archived | experimental  

**Tags:** #domain-1, #domain-2 (for searchability)  

**Summary:** [1-2 sentence description of what the pattern solves]  

**When to Use:**
- **Context:** Situations where this pattern applies
- **Prerequisites:** What should be true for pattern to work
- **Benefits:** Why use this pattern over alternatives
- **Drawbacks:** When NOT to use; trade-offs

**Implementation:**

[Concrete steps, pseudo-code, or code example]

Example:
```
step 1: ...
step 2: ...
step 3: ...
```

**Related Patterns:**
- [Complementary pattern]
- [Similar pattern]
- [Alternative to pattern]

**Lessons Learned:**
- [What went well when using this pattern]
- [Watch out for ...]
- [Edge case: ...]

**References:**

Features using this:
- spec-003: wiki/vault/lessons/2026-05-18-003-*.md
- spec-001: vault/lessons/2026-05-10-001-*.md

Code examples:
- [File path with line numbers]
- [File path with line numbers]

---

## [Pattern Name 2]
...
```

### Template Fields

**Name:** Concise, memorable name
- Bad: "System for handling multiple types"
- Good: "Polymorphic Service Layer"

**First Used / Last Used:** Track history
- `spec-005` = Used in feature 005
- Date helps understand when pattern became relevant

**Frequency:** How many features use this?
- "used in 3 features" = medium maturity
- "used in 1 feature" = experimental

- `active` — Proven and recommended
- `archived` — Old, not recommended for new features
- `experimental` — New, still learning

**Tags:** Domain-specific tags for discovery
- `#api` — API design patterns
- `#database` — Database patterns
- `#testing` — Test patterns
- `#performance` — Performance optimization patterns
- `#memory` — Memory/caching patterns
- `#error-handling` — Error handling patterns
- `#workflow` — Workflow/orchestration patterns

**Summary:** 1-2 sentences answering "What problem does this solve?"

**When to Use:** 4 sub-sections:
- **Context:** Specific situations
- **Prerequisites:** What's already true
- **Benefits:** Why choose this pattern
- **Drawbacks:** When to choose alternative

**Implementation:** Concrete instructions
- Pseudo-code or narrative steps
- If language-specific, include example in 1-2 languages
- Reference actual code in vault if available

**Related Patterns:** Cross-references
- Complementary: "Use with [pattern X]"
- Alternative: "Instead of [pattern Y]"
- Similar: "Like [pattern Z], but..."

**Lessons Learned:** War stories
- What worked well
- Common mistakes
- Edge cases

**References:** Traceability
- Links to vault/lessons files that used this
- Links to actual code examples in codebase

## Success Criteria

- ✅ Patterns discoverable (searchable by name + tags + domain)
- ✅ Reuse tracked (\"used in N features\" metric accurate)
- ✅ Status accurate (active/archived/experimental correctly labeled)
- ✅ Implementation clear (code examples concrete + tested)
- ✅ Lessons captured (watch outs + edge cases documented)
- ✅ Frequency data maintained (first/last used dates track maturity)
- ✅ Related patterns linked (wikilinks enable pattern discovery)

---

### Pattern Examples

**Example 1: Decorator Wrapper Pattern**
```markdown
## Decorator Wrapper Pattern

**First Used:** spec-002  
**Last Used:** spec-003  
**Frequency:** used in 5+ features  
**Tags:** #architecture, #integration, #workflow  

**Summary:** Wraps an existing service with pre/core/post processing layers without modifying the service itself. Enables flexible enhancement (logging, validation, context injection) while maintaining clean separation of concerns.

**When to Use:**
- Context: Want to enhance a service (SpecKit skills, API handlers) without modifying it
- Prerequisites: Service has stable interface; enhancement is orthogonal to core logic
- Benefits: Clean separation; works with any service version; easy to test layers independently
- Drawbacks: Extra function call overhead; layer ordering must be correct; debugging requires tracing through layers

**Implementation:**

Step 1: Define wrapper function
```
def wrapped_service(input):
  # Pre-processing layer
  enriched_input = load_context(input)
  
  # Core layer
  result = core_service(enriched_input)
  
  # Post-processing layer
  enriched_result = persist_artifacts(result)
  
  return enriched_result
```

Step 2: Test each layer independently
- Test pre-processing alone
- Test core service alone
- Test post-processing alone
- Test full wrapper

**Related Patterns:**
- Chain of Responsibility: Similar idea, but for chains of handlers
- Middleware Pattern: Similar in web frameworks; Decorator is broader

**Lessons Learned:**
- Pre-processing should be cheap (quick context load)
- Post-processing can be expensive (lessons extraction, artifact collection)
- Order matters: context must load before core runs
- Edge case: If core service fails, post-processing still runs (is this desired?)

**References:**
- Features: spec-002 (SpecKit integration), spec-003 (full CLI)
- Related specs: speckit-integration-contract.md, enrichment-layer.md
- Lesson: vault/lessons/2026-05-18-003-*.md#implementation
```

**Example 2: Lesson-Based Documentation Pattern**
```markdown
## Lesson-Based Documentation Pattern

**First Used:** spec-001  
**Last Used:** spec-003  
**Frequency:** used in 3 features  
**Tags:** #documentation, #memory, #workflow  

**Summary:** Capture structured lessons at feature end (what built, how built it, decisions, patterns, metrics) in vault/lessons/. This becomes permanent archive and feeds future features with proven approaches and cautions.

**When to Use:**
- Context: Feature is complete or abandoned; want to capture learnings
- Prerequisites: Have spec, plan, tasks, execution trace
- Benefits: Knowledge persists across sessions; patterns become discoverable; metrics inform future estimates
- Drawbacks: Lesson generation has token cost; requires discipline to write well; old lessons can become stale

**Implementation:**

Step 1: Collect artifacts (spec, plan, tasks, execution trace, git diff)

Step 2: Generate 8-section lesson document
- What We Built
- How We Built It
- Key Tasks Executed
- Decisions Made
- Patterns Identified
- Lessons for Next Feature
- Metrics
- References

Step 3: Compress using caveman mode (60% fewer tokens)

Step 4: Write to vault/lessons/<date>-<feature>-<name>.md

Step 5: Extract decisions → append to vault/decision.md

Step 6: Extract patterns → refine vault/patterns.md

**Related Patterns:**
- Post-Processing Layer: Often used with decorator to generate lessons
- Context Loading: Lessons are loaded at session start

**Lessons Learned:**
- Caveman compression is essential (lessons can get verbose without it)
- Template enforces structure; deviation makes future lookup harder
- Metrics section helps predict effort for similar features
- Lessons should be written while memory is fresh (at feature end, not later)

**References:**
- Features: spec-001, spec-002, spec-003
- Workflow spec: prepare-and-post-skills.md / post-command.md (lesson generation path)
- Lesson template: specs/lessons-format.md
```

---

## Repo Memory Pattern Index (vault/repo/patterns-index.md)

### Purpose
Compressed, recent-only index of top patterns. Used for quick lookup during planning.

### File Structure

```markdown
# Patterns Index (Recent)

**Last Sync:** YYYY-MM-DD HH:MM  
**Coverage:** Last 3 features  
**Full Archive:** See vault/patterns.md  

## Top Recent Patterns (By Usage)
Pattern | Frequency | Status | Tags | ---------|-----------|--------|------ | [Decorator Wrapper] | 5+ uses | active | #architecture, #integration | [Lesson-Based Documentation] | 3 uses | active | #documentation, #memory | [Pattern 3] | 2 uses | active | #testing
## Patterns by Domain

### #architecture
- [Decorator Wrapper Pattern](vault/patterns.md#decorator-wrapper-pattern)
- [Separation of Concerns](vault/patterns.md#separation-of-concerns)

### #documentation
- [Lesson-Based Documentation](vault/patterns.md#lesson-based-documentation-pattern)
- [Architectural Decision Records](vault/patterns.md#adr-pattern)

### #testing
- [Contract Testing](vault/patterns.md#contract-testing-pattern)

## Full Index

See vault/patterns.md (permanent archive with all patterns)
```

### Update Rules

**Sync Trigger:** After each feature (`/spek.conclude` step 4)

**Sync Process:**
1. Read vault/patterns.md
2. Extract patterns used in last 3 features
3. Count frequency for each pattern
4. Create summary index
5. Write to vault/repo/patterns-index.md

**Keep:** Top 10-15 recent patterns

**Remove:** Patterns not used in last 3 features (still in vault, just removed from repo memory)

---

## Query Patterns

**"What patterns exist for [domain]?"**
```bash
# Query repo memory (fast):
grep "#[domain]" vault/repo/patterns-index.md

# Query vault (complete):
grep -l "#[domain]" vault/patterns.md
```

**"Which patterns are used most?"**
```bash
# Query repo memory:
grep "| .*| " vault/repo/patterns-index.md | sort -t'|' -k2 -rn
```

**"What was learned from pattern X?"**
```bash
# Query vault:
grep -A20 "## Pattern X" vault/patterns.md | grep -A15 "Lessons Learned"
```

**"What patterns were used in feature 003?"**
```bash
# Query lessons:
grep "Patterns Applied" vault/lessons/2026-05-18-003-*.md
```

---

## Lifecycle

### Write Triggers

**During feature work:**
- When a pattern is discovered/applied → Note in `vault/session/`

**At feature end (`/spek.conclude` step 4):****
- Extract patterns from lessons
- Add new patterns to vault/patterns.md (with "First Used" = current feature)
- Update existing patterns (increment frequency, update "Last Used")
- Sync recent patterns to vault/repo/patterns-index.md

### Read Triggers

**Session start (`/spek.context`):**
- Load pattern index from vault/repo/patterns-index.md
- Include recent patterns in context briefing

**During planning (`/spek.plan` plan phase):**
- Query vault/patterns.md for patterns applicable to current feature
- Suggest patterns in plan generation prompt

**During implementation:**
- Reference patterns in implementation notes
- Document which pattern each implementation chunk follows

### Retention Policy

**Vault (vault/patterns.md):**
- Keep all patterns indefinitely (even archived ones, for historical context)

**Repo Memory (vault/repo/patterns-index.md):**
- Sync after each feature
- Keep top 10-15 recent patterns (used in last 3 features)
- Prune older patterns to keep file size <5KB

---

## Integration with Other Systems

### Lessons Format (lessons-format.md)

Patterns discovered during a feature are documented in the "Patterns Identified" section of vault/lessons/ files. The post-processing phase converts these to formal pattern entries.

### Context Loading (memory-architecture.md)

Pattern index is loaded at session start and included in context briefing for agent awareness.

### Enrichment (enrichment-layer.md)

Recent patterns are injected into `/spek.plan` plan prompts to guide architecture decisions toward proven approaches.

---

## Success Criteria

✅ Patterns capture reusable solutions with clear context and prerequisites  
✅ Patterns have frequency tracking (how many features use them)  
✅ Patterns distinguish between active / archived / experimental  
✅ Vault is permanent archive; repo memory is compressed recent index  
✅ Patterns are searchable by domain/tag  
✅ Related patterns are cross-referenced  
✅ "Lessons Learned" section captures edge cases and cautions  

---

## Implementation Checklist

- [ ] Create vault/patterns.md template
- [ ] Implement pattern extraction in /spek.conclude
- [ ] Implement pattern index sync to vault/repo/
- [ ] Update /spek.context to load recent patterns
- [ ] Add pattern query patterns to wiki guide
- [ ] Inject patterns into `/spek.plan` plan prompts

---

## References

**Related Specs:**
- [lessons-format.md](lessons-format.md) — Patterns captured here first
- [memory-architecture.md](memory-architecture.md) — Patterns loaded at session start
- [enrichment-layer.md](enrichment-layer.md) — Patterns injected into planning + specification
- [post-command.md](post-command.md) — Patterns synced to vault here

**External:**
- [extracted spec Memory Architecture](memory-architecture.md) — Original spec