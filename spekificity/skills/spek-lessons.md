---
name: spek-lessons
description: 'Extract and store structured lessons. Callable standalone at any point, or auto-called inside spek.conclude.'
---

# /spek.lessons

Extract and store structured lessons. Callable standalone at any point, or auto-called as step 2 inside `/spek.conclude`.

## Prerequisites

- Implementation work completed or at a meaningful checkpoint

## Steps

1. Prompt for retrospective: what worked, what was difficult, what would you do differently.
2. Extract new patterns if workflow diverged from spec.
3. Log new decisions if architecture changed from original plan.
4. Write lessons to `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md` using the template below (include timestamp to prevent filename collisions on same-day features).
5. Run autolink enrichment: Validate `process_lesson()` function exists and callable in vault integration layer. If function exists, call with:
   - Generated lesson file path (`.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md`)
   - Vault root path (`.spek/vault/`)
   - Loaded config (from `.spek/config.yaml` `autolink` section)
   - Function inserts `[[wikilinks]]` for matched vault entries (decisions, patterns, prior lessons) and adds `tags:` array to frontmatter
   - Wikilink format: `[[Decision: async patterns]]` auto-resolved to `.spek/vault/decisions.md` section header
   - Tags array format: `tags: [#async, #error-handling, #performance]` for Obsidian auto-tagging
   - Skip gracefully if function unavailable or `autolink.enabled: false` in config.
6. Note token budget: read `token_budget.per_feature` from `.spek/config.yaml` (if file exists); print total estimated token cost for this feature cycle for retrospective context; skip silently if config missing or `token_budget.per_feature` not set.

## Output

Lessons file at `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md`:

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
---

## Feature: [Feature Name]
Date: YYYY-MM-DD
Status: Complete

### What went well
- [[Pattern: middleware composition]] worked well for request pipeline
- Reused [[Decision: Result type error handling]] pattern from prior feature

### What was difficult
- Discovering async boundary in [[module: database queries]] took longer than expected
- [[Anti-pattern: mixing callbacks and async/await]] nearly introduced bug; caught in review

### Patterns discovered
- New reusable pattern discovered: [[Pattern: late binding for async resources]]
- Architecture insight: [[Decision: prefer composition over inheritance for middleware]]

### Recommendations for future
- [[Decision: Result type]] should be documented with examples for new team members
- Consider automated enforcement of async/await vs callback choice (linting rule)

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

- Retrospective captured from user
- Lessons file written to `.spek/vault/lessons/` with timestamp in filename (no collisions)
- New patterns and decisions extracted and logged
- `[[wikilinks]]` inserted for all vault-matched keywords
- Tags generated from `keyword_tags` mapping and added to frontmatter
- PR link (if available) appended to Linked Artifacts section

