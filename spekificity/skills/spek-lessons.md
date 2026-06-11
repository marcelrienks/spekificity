# /spek.lessons

Extract and store structured lessons. Callable standalone at any point, or auto-called as step 2 inside `/spek.conclude`.

## Prerequisites

- Implementation work completed or at a meaningful checkpoint

## Steps

1. Prompt for retrospective: what worked, what was difficult, what would you do differently.
2. Extract new patterns if workflow diverged from spec.
3. Log new decisions if architecture changed from original plan.
4. Write lessons to `.spek/vault/lessons/YYYY-MM-DD-feature-name.md` using the template below.

## Output

Lessons file at `.spek/vault/lessons/YYYY-MM-DD-feature-name.md`:

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
```

## Exit Criteria

- Retrospective captured from user
- Lessons file written to `.spek/vault/lessons/`
- New patterns and decisions extracted and logged
