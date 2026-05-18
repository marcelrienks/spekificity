# Skill: `/spek.lessons`

## Purpose

Extract and capture structured lessons learned from a completed feature into persistent vault storage. Lessons must be self-contained — future sessions should understand the feature without re-reading spec.md or tasks.md.

**Outcome:** Structured lesson entry written to `vault/lessons/<date>-<feature>-<name>.md` with feature digest, implementation summary, decisions, and patterns.

---

## Overview

Lessons learned serve as the vault's memory system. They distill feature work into a compressed, queryable format that:
- Summarizes what was built (feature purpose + scope)
- Documents how it was built (architecture + key tasks)
- Captures decisions and rationale
- Identifies reusable patterns
- Provides practical guidance for similar future features

**Key principle:** If a future developer/agent loads this lesson and reads nothing else about the feature, they should have enough context to understand it, reuse its patterns, and avoid its pitfalls.

---

## Lesson Entry Structure

**File naming:** `vault/lessons/<YYYY-MM-DD>-<feature-number>-<feature-name>.md`  
**Example:** `vault/lessons/2026-05-18-003-authentication.md`

### Lesson Template

```markdown
# Lesson: [Feature Name] ([Date], spec-[Number])

## What We Built

[2-3 sentence digest of feature purpose and scope]

- [Key domain concept 1]
- [Key domain concept 2]
- [Key domain concept 3]

*Context: This section replaces the need to read spec.md. Distill the feature into its essence.*

---

## How We Built It

[Technical approach; distilled from plan.md]

- **Architecture decision 1**: [Context] → [Rationale] → [Outcome]
- **Tech stack choice**: [Why chosen over alternatives]
- **Integration point**: [What this feature connects to in the codebase]
- **Key constraint**: [Any non-functional requirement that shaped design]

*Context: This section explains the technical reasoning without requiring the reader to parse plan.md.*

---

## Key Tasks Executed

- **[Task 1 title]**: [What it delivered; 1-2 lines]
- **[Task 2 title]**: [What it delivered; 1-2 lines]
- **[Critical task if any]**: [Why this task was harder/important than others]

*Context: Future developers should see which tasks made up the feature and what each produced.*

---

## Decisions Made (Linked to Implementation)

| Decision | Context | Outcome | Alternative Considered |
|----------|---------|---------|------------------------|
| [Decision 1] | [Why it arose] | [What it enabled] | [What we rejected and why] |
| [Decision 2] | [Why it arose] | [What it enabled] | [What we rejected and why] |

*Context: Explicit decisions prevent re-litigating the same choices in future features.*

---

## Patterns Identified or Reused

### Patterns Reused
- **[Pattern name]**: Reused from spec-[X], adapted for [what changed]
  - Key characteristics: [Why this pattern worked here]
  - Applicable context: [When to use this pattern again]

### Patterns Discovered
- **[New pattern name]**: Emerged from [task/decision], generalizable to [domain]
  - Key characteristics: [What makes this pattern useful]
  - Where to document: Add to vault/patterns.md

### Anti-patterns Avoided
- **[What NOT to do]**: Discovered through [failed attempt or avoided mistake]
  - Cost if ignored: [Concrete consequence if pattern is violated]
  - Future reference: [When you encounter similar scenarios, remember this]

*Context: Future features should inherit both successes and lessons from this feature's patterns.*

---

## Lessons for Next Feature

- If you need to [similar task], [concrete advice based on what we learned]
- For features involving [domain], [what approach worked well or what to avoid]
- Watch out for [specific gotcha/subtlety]; [why it matters]
- Next time we do [similar work], [what we'd do differently / what to repeat]

*Context: Practical wisdom for future feature teams; should be actionable.*

---

## Metrics

- **Lines of code**: [Total code written]
- **Files modified**: [N files changed/created]
- **Test coverage**: [% of code covered]
- **Time spent**: [HH:MM, total]
- **Complexity**: [Simple/Moderate/Complex] ([justification])

*Context: Helps estimate similar features; informs complexity budgeting.*

---

## References

- **Full spec**: specs/[number]-[name]/spec.md
- **Implementation plan**: specs/[number]-[name]/plan.md
- **Tasks**: specs/[number]-[name]/tasks.md
- **Related lessons**: [Link to 1-2 prior features if relevant]

*Context: Pointers to full artifacts for deep dives, but not required reading.*

---

*Captured [DATE] via caveman compression. Compressed format saves 60% of reading time while preserving technical content.*
```

---

## Self-Contained Validation Checklist

Before writing a lesson entry, verify it passes this checklist:

- [ ] **What We Built section**: Can someone unfamiliar with the codebase understand the feature's purpose in 2-3 sentences?
- [ ] **How We Built It section**: Are the architecture decisions documented with rationale?
- [ ] **Key Tasks**: Are the major components/deliverables clear?
- [ ] **Decisions Made**: Can a future developer understand why this was chosen over alternatives?
- [ ] **Patterns**: Are reusable patterns identified and described?
- [ ] **Lessons for Next Feature**: Do the lessons provide actionable guidance?
- [ ] **Metrics**: Are complexity, size, and effort captured for future estimation?

**Red flags indicating a lesson is NOT self-contained:**
- References "see spec.md for details" without summarizing the detail
- Lists tasks without explaining what they delivered
- Mentions a decision without explaining the rationale
- Uses acronyms or jargon without brief definitions

---

## Compression Rules (Caveman Format)

When writing lessons using caveman mode:

| Aspect | Do | Don't |
|--------|-----|--------|
| Sentences | Short, direct (1-2 lines per concept) | Elaborate paragraphs |
| Verbs | Active voice, specific (e.g., "extracted", "refactored") | Passive voice, vague (e.g., "was done", "considered") |
| Nouns | Technical terms + brief definition | Unexplained acronyms |
| Examples | Concrete (e.g., "added JWT token expiry check") | Generic (e.g., "added security") |
| Structure | Bullet points, tables, clear hierarchy | Flowing prose |
| Metrics | Numbers (10 files, 300 LOC, 4 hours) | Vague ("many", "some", "took a while") |

**Example (caveman):**
```
Decision: JWT + refresh tokens over session cookies
Context: Stateless auth requirement for distributed services
Outcome: Simplified deployment, testability improved, client token management required
Alternative: Session cookies rejected due to server-side state coupling
```

**Example (verbose, NOT caveman):**
```
One key decision we made was to use JWT tokens with a refresh token pattern 
instead of the more traditional session cookies. This was important because 
our architecture requires stateless authentication across multiple service 
instances. By choosing JWTs, we were able to simplify deployment and improve 
testability, though it does require clients to manage token expiry, which we 
mitigated through automatic refresh logic. We considered session cookies but 
rejected that approach because it would have required server-side state, which 
doesn't scale well in our distributed setup.
```

---

## Integration with `spek.post`

`/spek.lessons-learnt` is called by `spek post` after feature implementation completes:

```
spek post
  → collect artifacts (spec, plan, tasks, execution trace)
  → activate caveman compression
  → /spek.lessons-learnt
     ├─ analyze artifacts
     ├─ extract feature summary
     ├─ extract decisions + patterns from implementation
     └─ write vault/lessons/<date>-<feature>.md
  → update vault context (decisions.md, patterns.md)
  → run code graph incremental sync
  → run cel.docs.simplify
```

Can also be run manually:

```bash
/spek.lessons-learnt --feature-number 003 --feature-name "authentication"
```

---

## Invocation Patterns

### Automatic (via spek post)

```bash
spek post
# Automatically invokes /spek.lessons-learnt as part of postflight
```

### Manual (after feature completion)

```bash
/spek.lessons-learnt
# Reads current feature branch; extracts and writes lessons
```

### Manual with options

```bash
/spek.lessons-learnt --feature-number 003 --feature-name "auth" --compression caveman-full
```

---

## Output Format

**File created:** `vault/lessons/2026-05-18-003-authentication.md`

**Append to vault context:**
- New entries added to `vault/decisions.md` (tagged with feature number)
- New entries added to `vault/patterns.md` (tagged with feature number)
- Graph index updated to reference lesson file

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Artifacts missing | Warn; offer to proceed with available data or cancel |
| Compression unavailable | Skip compression; write uncompressed (less ideal) |
| Vault structure missing | Create vault/lessons/ directory |
| Duplicate filename | Append timestamp (lessons will be re-run) |
| Extraction fails | Write template; ask user to fill in manually |

---

## Quality Indicators

A well-written lesson entry:

✓ Can be understood in 2-3 minutes of reading  
✓ Enables pattern reuse in future features (similar features don't repeat work)  
✓ Captures decisions so future developers don't re-litigate choices  
✓ Includes concrete metrics for effort estimation  
✓ References full artifacts (spec/plan/tasks) but doesn't duplicate them  
✓ Is written in compressed caveman format (60% fewer tokens to read)  
✓ Provides actionable guidance ("if you encounter X, do Y")  

---

## Related Skills

- `/spek.post` — Orchestrator skill that calls lessons-learnt
- `/context-load` — Loads lessons into session context
- `/caveman` — Token compression mode (auto-enabled for lessons writing)
- `/cel.wiki.read` — Vault context management

---

## Long-Term Value

Each lesson compounds:

```
Feature 1 → Lesson 1 (defines patterns)
            ↓
Feature 2 → /context-load (loads Lesson 1, patterns available)
            → Lesson 2 (reuses/refines patterns from Lesson 1)
            ↓
Feature 3 → /context-load (loads Lessons 1-2, richer patterns available)
            → Faster development (patterns pre-identified)
            → Lesson 3 (contributes new patterns)
            ↓
Feature 4+ → Compounding benefit: vault becomes project's externalized intelligence
```

**Result:** Lessons learned is not just documentation — it's the mechanism that makes each feature faster and more consistent than the last.

---

## Implementation Checklist

- [ ] Skill can extract feature summary from spec.md
- [ ] Skill can derive implementation steps from tasks.md
- [ ] Skill can extract decisions from plan.md + implementation context
- [ ] Skill can identify and categorize patterns (reused/discovered/avoided)
- [ ] Skill applies caveman compression automatically
- [ ] Skill validates lesson entry against self-contained checklist
- [ ] Skill writes to vault/lessons/ with correct filename format
- [ ] Skill updates vault/decisions.md + vault/patterns.md
- [ ] Skill handles errors gracefully
- [ ] Skill integrates with spek.post workflow
