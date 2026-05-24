# Spec: Per-Feature Lessons Format


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
**Concern:** Template and lifecycle for lessons learned files written at feature end  
**Extracted from:** extracted spec Type 1 (Per-Feature Lessons)  
**Used by:** conclude-command, /spek.conclude skill  

---


## Overview

**Problem:** After each feature completes, context is lost. Next feature requires re-reading spec/plan/tasks. Solution: capture "what was built + how + decisions" in self-contained lesson file.

**Solution:** Define a multi-section lesson template, write to wiki/vault/lessons/ after feature, and compress with caveman mode for token efficiency.

**Outcome:** wiki/vault/lessons/<date>-<number>-<name>.md files that can be loaded by the next feature session, reducing context reload cost significantly.

---


## Success Criteria

- ✅ Lesson format self-contained (readable without spec.md/plan.md)
- ✅ Compression effective (significant token reduction vs. normal prose)
- ✅ Lessons actionable (next feature can apply recommendations immediately)
- ✅ Content specific + concrete (code examples, not vague advice)
- ✅ Template sections complete (all template sections filled or N/A marked)
- ✅ Wikilinks present (cross-references recorded)
- ✅ Metrics captured (values recorded; quantitative details omitted)
- ### Section 3: How We Built It (Technical Approach)
- ```markdown
- ## How We Built It
- **Architecture Decisions:**
- Decision 1: [brief rationale]
- Decision 2: [brief rationale]
- **Key Design Patterns:**
- Pattern 1: [where applied]
- Pattern 2: [where applied]
- **Implementation Approach:**
- [Step 1]
- [Step 2]
- [Step 3]
- **Tech Stack Used:**
- [Language/Framework 1]
- [Tool/Library 2]
- [Service/Platform 3]
- ```
- **Rationale:**
- Documents architectural decisions for future reference
- Explains why (not just what)
- Lists patterns used (for reuse in similar features)
- **Caveman Mode Example:**
- Architecture decisions:
- Decorator pattern over hooks (vs modifying SpecKit; cleaner coupling)
- Vault single source of truth (code graph derived; vault authoritative)
- Three-layer memory (ephemeral session → persistent repo → archive vault)
- Key patterns:
- Decorator wrapper (pre/core/post layers)
- Graph-based context queries (order-of-magnitude token reduction vs repeated file reads)
- Incremental update (SHA256 caching; only changed files re-indexed)
- Implementation:
- Define orchestration/enrichment pattern for `/spek.plan` phases and `/spek.implement`
- Implement /spek.context loader (vault → session memory)
- Implement /spek.prepare + /spek.conclude workflows
- Integrate lat.md + Obsidian export into /spek.map
- Create caveman compression at prepare + post steps
- Tech stack:
- TypeScript (cli + skills)
- Python (graph merge scripts)
- Obsidian (vault storage)
- lat.md (code indexing)
- ### Section 4: Key Tasks Executed
- ## Key Tasks Executed
- Task | Status | Duration | Notes | ------|--------|----------|------- | Task 1: [description] | ✓ done | duration recorded (omitted) | [blockers/learnings] | Task 2: [description] | ✓ done | duration recorded (omitted) | [blockers/learnings] | Task 3: [description] | ✓ done | duration recorded (omitted) | [blockers/learnings] | Task 4: [description] | ✗ partial | duration recorded (omitted) | [why not complete]
- **Total Feature Time:** recorded (omitted)
- **Blocker Resolution:** [Any major blockers encountered and how resolved]
- Track actual execution vs planned estimate
- Identify recurring blockers
- Data for future estimation
- ### Section 5: Decisions Made
- ## Decisions Made
- **Decision 1: [Decorator Pattern over Hooks]**
- Context: SpecKit doesn't expose hooks; need clean integration point
- Options: (a) modify SpecKit, (b) decorator wrapper, (c) fork SpecKit
- Chosen: (b) Decorator
- Rationale: No coupling to SpecKit internals; works with any version
- Impact: Cleaner code, easier to test, maintainable across updates
- **Decision 2: [Vault as Single Source of Truth]**
- Context: Graph is expensive to compute; code is fast-changing
- Options: (a) sync vault to graph, (b) vault authoritative + derived graph
- Chosen: (b) Vault authoritative
- Rationale: Obsidian is proven tool; graph is derived from vault on demand
- Impact: Simpler consistency model; Obsidian as system of record
- ... (additional decisions)
- Captures "why" for future reference
- Flags design trade-offs
- Helps avoid re-deciding same question
- ### Section 6: Patterns Identified or Reused
- ## Patterns Identified or Reused
- **Reused Patterns:**
- Workflow Enrichment: Applied to `/spek.plan` phases and `/spek.implement` (context injection pattern from prior features)
- Three-Layer Memory: Applied to vault/repo/session layers (from claude-code-memory-setup reference)
- Incremental Updates: Applied to graph refresh via SHA256 caching (proven in feature 002)
- **Newly Discovered Patterns:**
- Graph Merge Strategy: Discovered unification of code + doc nodes improves discovery (could apply to future agent systems)
- Caveman Compression Activation: Auto-activate at feature boundaries for token efficiency (reusable strategy)
- **Patterns NOT Useful This Feature:**
- Multi-tier memory (episodic/semantic/procedural) from Pilot Shell — too complex for this scope
- Builds reusable pattern library
- Tracks anti-patterns (what doesn't work)
- Enables pattern-based planning in future
- ### Section 7: Lessons for Next Feature
- ## Lessons for Next Feature
- **What Worked Well:**
- Decorator pattern made integration clean and testable
- Splitting specs into atomic concerns enabled parallel work
- Vault-first approach kept Obsidian as UX tool (didn't require plugin rewrites)
- **What to Do Differently:**
- Graph merge took longer than estimated — next time allocate 2x time for validation + edge cases
- Link discovery heuristics were fragile — consider manual linking for critical docs
- Caveman mode slowed output iteration — use full mode for drafting, compress at end
- **Edge Cases to Watch:**
- Heading ID conversion edge cases (special chars, multiple words with hyphens)
- Symlinks in code paths (may cause duplicates or conflicts)
- Multi-language files (TypeScript + Python mixed in single file)
- **Next Steps Enabled by This Feature:**
- Phase 1 ✓ (Architectural specs B.1-graph-setup)
- Phase 2 (Agent skill creation; /spek.context, /spek.prepare, /spek.conclude skills)
- Phase 3 (CLI orchestration; /spek.plan entry point)
- Actionable guidance for similar future features
- Highlights process improvements
- Lists technical debt / known issues
- ### Section 8: Metrics & References
- ## Metrics
- **Execution Metrics:**
- Token Efficiency: meaningful reduction via decorator pattern + memory layering
- Execution Time: recorded (omitted)
- Code Quality: recorded (omitted)
- Documentation: recorded (omitted)
- **Team Metrics:**
- Author(s): [Name]
- Reviewers: [Names]
- Code Review Rounds: recorded (omitted)
- External Dependencies: recorded (omitted)
- ## References
- **Specification Documents:**
- [Feature Spec](specs/00spek-full-workflow-cli.md)
- [Plan](specs/00plan.md)
- [Implementation Tasks](specs/00tasks.md)
- **Architectural Decisions:**
- [Decorator Pattern Decision](wiki/vault/decision.md#decorator-pattern-integration)
- [Vault Single Source Decision](wiki/vault/decision.md#vault-single-source)
- **Related Lessons:**
- [Feature 002: Persistent Memories](wiki/vault/lessons/2026-05-12-00persistent-memories.md)
- [Feature 001: Initial Setup](wiki/vault/lessons/2026-05-10-00initial-setup.md)
- **Code Artifacts:**
- Pull Request: [github.com/owner/repo/pull/XXX](https://github.com/marcelrienks/spekificity/pull/XXX)
- Main Commits: [commit1](https://github.com/marcelrienks/spekificity/commit/abc123) ... [commitN](https://github.com/marcelrienks/spekificity/commit/def456)
- ## Quality Checklist
- Before writing to wiki/vault/lessons/, validate:
- [ ] **Self-Contained:** Can a developer understand feature without reading spec.md/plan.md?
- [ ] **Compressed:** Caveman format applied; no fluff; concrete language
- [ ] **Actionable:** Next feature can apply these lessons immediately
- [ ] **Specific:** Concrete examples, not vague advice ("Use decorator pattern [example]" not "Write clean code")
- [ ] **Complete:** All 8 sections filled (or explicitly marked N/A)
- [ ] **Metrics Included:** Token savings, duration, code quality tracked
- [ ] **Linked:** References to spec.md, decisions, related lessons included
- [ ] **Consistent:** Writing style matches caveman mode (lite/full as configured)
- ## Retention Policy
- **Keep indefinitely:** All lessons stored in vault (permanent archive)
- -- **Archive inactive:** After a configured period of inactivity, mark `status: archived` (but don't delete)
- -- **Index recent:** Repo memory keeps recent lessons for quick access
- **Search:** `/spek.context` loads 3-5 most recent lessons at session start
- ## Integration with /spek.conclude
- **In `/spek.conclude` workflow (Step 3):**
- /spek.conclude
- ├── Collect artifacts (spec.md, plan.md, tasks.md, execution trace)
- ├── Activate caveman mode (lite for drafting, full for final compression)
- ├── Generate lessons document
- │   ├── Read spec/plan/tasks
- │   ├── Extract What/How/Tasks/Decisions/Patterns/Lessons/Metrics/References
- │   ├── Compress with caveman mode
- │   └── Write to wiki/vault/lessons/<date>-<number>-<name>.md
- └── Report: "Lessons written to wiki/vault/lessons/"
- ## Success Criteria
- [x] Lesson template covers scope, decisions, learnings, and metrics (template-driven)
- [x] File naming is consistent (date placeholder + number + name)
- [x] Quality checklist ensures self-contained, actionable lessons
- [x] Retention policy defined (keep and archive per policy)
- [x] Caveman compression reduces token cost (significant reduction)
- [x] Lessons are linked to original spec, decisions, related lessons
- [x] Integration point with /spek.conclude is clear
- **Used by:** /spek.conclude skill, /spek.context skill (loads lessons at session start)
- **Related:** architectural-decisions, patterns-library, memory-architecture
- **Caveman mode:** Compression applied at write time (caveman lite/full as configured)


## File Naming Convention

**Pattern:** `<date>-<number>-<feature-name>.md`

**Examples:**
- `wiki/vault/lessons/<date>-<feature>-spek-full-workflow-cli.md`
- `wiki/vault/lessons/<date>-<feature>-persistent-memories.md`
- `wiki/vault/lessons/<date>-<feature>-initial-setup.md`

**Rationale:**
- Date: Sort by recency (newest first)
- Feature number: Ties lesson to original feature spec
- Feature name: Human-readable context

---


## Lesson Template (multi-section)


## Section 1: Header & Metadata

```markdown
# Lesson: [Feature Name] (Spec-[Number], [Date])

partial | abandoned  
**Date Completed:** YYYY-MM-DD  
**Duration:** X days / Y sessions  
**Feature Spec:** specs/NNN-feature-name.md  
**Code Branch:** NNN-feature-name  
**Commit Range:** [commit1..commit2]
```

**Metadata Rationale:**
- `Status`: Was feature fully completed or partial?
- `Duration`: How long did feature take? (for future estimation)
- `Feature Spec`: Link to original spec.md (for full details)
- `Code Branch`: Which branch to check out (for code review)
- `Commit Range`: Which commits make up this feature

---


## Section 2: What We Built (brief summary)

```markdown

## What We Built

[2-3 sentence digest of feature + key domain concepts]

**Core Changes:**
- [Major change 1]
- [Major change 2]
- [Major change 3]

**Files Modified:** count omitted — list if small
**Lines of Code:** recorded (omitted)
**Test Coverage:** recorded (omitted)
```

**Rationale:**
- Next developer can understand feature scope quickly
- Digest without reading full spec.md
- Metrics for estimation (duration + LOC)

**Caveman Mode Example:**
```
Spekificity prep + post skills (feature orchestration). Verifies git state. Loads context.
Collects lessons. Updates vault. Incremental graph sync. Caveman activation built-in.

Core changes:
- /spek.prepare command (workflow)
- /spek.conclude command (workflow)
- Vault sync (decisions, patterns, code graph)
- Caveman compression at each step

Files/LOC/test-coverage: recorded (omitted)
```

