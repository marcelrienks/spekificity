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
5. Run autolink enrichment: Validate `process_lesson()` function exists and callable. If function exists, call with generated lesson path, `.spek/vault/`, and loaded config; inserts `[[wikilinks]]` for matched vault entries and adds generated tags to frontmatter. Skip gracefully if function unavailable or `autolink.enabled: false` in `.spek/config.yaml`.
6. Note token budget: read `token_budget.per_feature` from `.spek/config.yaml` (if file exists); print total estimated token cost for this feature cycle for retrospective context; skip silently if config missing or `token_budget.per_feature` not set.

## Output

Lessons file at `.spek/vault/lessons/YYYY-MM-DD-HH-MM-SS-feature-name.md`:

```markdown
## Feature: [Feature Name]
Date: YYYY-MM-DD
Status: Complete

### What went well
- [pattern/approach/tool that worked]

### What was difficult
- [challenge/blocker]
- [mitigation used]

### Patterns discovered
- [reusable pattern]
- [architectural insight]

### Recommendations for future
- [suggestion for similar features]
- [process improvement]

### Linked Artifacts
- Spec: [link to spec in .spek/vault/]
- Plan: [link to plan in .spek/vault/]
- Decisions Made: [link to decision entries]
- Pull Requests: [GitHub PR links]
- Feature Status: [approved | implemented | concluded]
```

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

