---
name: spek-lessons
description: 'Extract and store structured lessons. Callable standalone at any point, or auto-called inside spek.conclude.'
---

# /spek.lessons

Extract and store structured lessons. Callable standalone at any point, or auto-called as step 2 inside `/spek.conclude`.

## Prerequisites

- Implementation work completed or at a meaningful checkpoint
- Current branch is a feature branch (to analyze git diff)
- Access to chat session context (for extraction of discussion, obstacles, decisions)
- spec.md, plan.md, and tasks.md available for context

## Data Sources

The skill synthesizes lessons from three primary sources:

1. **Git History**: `git diff <base-branch>..HEAD` captures all changes made during the feature
   - Identifies code patterns that emerged vs. those that failed or were reverted
   - Reveals scope changes (commits added/removed vs. original tasks.md)
   - Shows iteration cycles (multiple refactorings indicate difficulty areas)

2. **Implementation Artifacts**: spec.md, plan.md, tasks.md define original intent
   - Baseline for comparing what was planned vs. what actually happened
   - Original architectural decisions to validate against actual implementation

3. **Session Chat**: Current Copilot chat context
   - Obstacles encountered and how they were resolved (not visible in final code)
   - Pivots and decision points (why some approaches were rejected)
   - New patterns/insights discovered during collaborative problem-solving
   - Token budget context for estimating complexity of this feature

## Steps

0. **Caveman activation check**: Ensure Caveman compression is active. If not active in this session, run `/caveman full` to enable ~75% token reduction (valuable for synthesis and analysis phase).

1. **Analyze implementation context automatically**:
   - Read spec.md, plan.md, and tasks.md to understand original intent and planned approach
   - Run `git diff <base-branch>..HEAD` to capture all changes made during feature implementation
   - Parse the current chat session to extract discussion points, obstacles encountered, and discoveries made
   - Extract feature name from current branch or spec frontmatter

2. **Synthesize lessons from evidence** (not user input):
   - Compare original spec/plan vs. actual implementation (via git diff)
   - Identify patterns discovered during coding that weren't in original design
   - Extract decisions that diverged from the plan (and why they changed)
   - Note obstacles encountered and how they were resolved
   - Capture what worked well vs. what was difficult (from code changes + session chat)

3. **Extract new patterns** if workflow diverged from spec:
   - Review code changes for reusable patterns not originally planned
   - Cross-reference with existing vault patterns to avoid duplication

4. **Log new decisions** if architecture changed from original plan:
   - Document divergences from original design with rationale
   - Reference relevant decisions made during implementation

5. Write lessons to `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md` using the template below (include timestamp to prevent filename collisions on same-day features).

6. Run autolink enrichment: Validate `process_lesson()` function exists and callable in vault integration layer. If function exists, call with:
   - Generated lesson file path (`.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md`)
   - Vault root path (`.spek/vault/`)
   - Loaded config (from `.spek/config.yaml` `autolink` section)
   - Function inserts `[[wikilinks]]` for matched vault entries (decisions, patterns, prior lessons) and adds `tags:` array to frontmatter
   - Wikilink format: `[[Decision: async patterns]]` auto-resolved to `.spek/vault/decisions.md` section header
   - Tags array format: `tags: [#async, #error-handling, #performance]` for Obsidian auto-tagging
   - Skip gracefully if function unavailable or `autolink.enabled: false` in config.

7. Note token budget: read `token_budget.per_feature` from `.spek/config.yaml` (if file exists); print total estimated token cost for this feature cycle for retrospective context; skip silently if config missing or `token_budget.per_feature` not set.

## Output

Lessons file at `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md`:
Generated from git diff, implementation context (spec/plan/tasks), and session discussion.

```markdown
---
feature: [Feature Name]
status: complete
tags: [#async, #error-handling, #pattern-reuse]
linked_decisions:
  - [[Decision: async/await patterns]]
linked_patterns:
  - [[Pattern: Result type error handling]]
related_lessons:
  - [[2026-05-15-feature-auth]]
synthesized_from:
  - git_commits: [number of commits analyzed]
  - session_discussion: [key pivots/discussions from chat]
---

## Feature: [Feature Name]
Date: YYYY-MM-DD
Status: Complete
Synthesis Method: Analyzed git diff, spec/plan comparison, and session discussion

### What went well
- [[Pattern: middleware composition]] worked well for request pipeline (evidenced by minimal commits to that area)
- Reused [[Decision: Result type error handling]] pattern from prior feature (no refactoring needed)

### What was difficult
- Discovering async boundary in [[module: database queries]] took longer than expected (evidenced by multiple commit cycles and session discussion of debugging steps)
- [[Anti-pattern: mixing callbacks and async/await]] nearly introduced bug; caught in review (discussed in session, resolved without code impact)

### Patterns discovered
- New reusable pattern discovered: [[Pattern: late binding for async resources]] (emerged from implementation; not in original plan)
- Architecture insight: [[Decision: prefer composition over inheritance for middleware]] (decision made during implementation to handle unforeseen coupling issue)

### Deviations from original plan
- Original plan specified [X approach], but implementation discovered [Y approach] worked better because [Z reason]
- Scope adjustment: [task from tasks.md] was descoped due to [reason from session discussion]

### Recommendations for future
- [[Decision: Result type]] should be documented with examples for new team members
- Consider automated enforcement of async/await vs callback choice (linting rule)
- [Additional recommendation from session context]

### Linked Artifacts
- Spec: [link to spec in .spek/vault/]
- Plan: [link to plan in .spek/vault/]
- Decisions Made: [[Decision: async/await patterns]], [[Decision: middleware composition]]
- Pull Requests: [GitHub PR links]
- Feature Status: [approved | implemented | concluded]
```

**Wikilink Format:** `[[Section: Optional Context]]` — resolves to matching `## Section:` header in decisions.md or patterns.md.

**Tags Format:** `[#keyword]` — auto-linked to tags in Obsidian when vault opened in Obsidian Desktop.

## Approval Status Update

After `/spek.plan` approves spec/plan/tasks, each file includes frontmatter:

```yaml
---
feature: [feature-name]
status: approved
approved_by: [agent/user name]
approved_date: YYYY-MM-DD
lat_md_version: [timestamp when lat.md was current]
---
```

After implementation concludes, lessons file should reference these approval details.

```

## Exit Criteria

- Implementation context analyzed (spec, plan, git diff)
- Chat session parsed for discussion, obstacles, and discoveries
- Lessons synthesized from evidence (code changes + discussion)
- Lessons file written to `.spek/vault/lessons/` with timestamp in filename (no collisions)
- New patterns and decisions extracted and logged
- `[[wikilinks]]` inserted for all vault-matched keywords
- Tags generated from `keyword_tags` mapping and added to frontmatter
- PR link (if available) appended to Linked Artifacts section

