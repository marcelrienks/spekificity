# Skill: /spek.plan

Generate formal specification, clarify ambiguities, create implementation plan and task breakdown.

## Input

```
/spek.plan "FEATURE_DESCRIPTION"
```

## Arguments

- `FEATURE_DESCRIPTION` (required): Feature description (10-1000 chars)

## Output

Three markdown artifacts in `specs/{feature-slug}/`:
1. **spec.md** — Formal specification with user stories, requirements, success criteria
2. **plan.md** — Architecture overview, technology stack, sequencing, risks
3. **tasks.md** — Prioritized, independent tasks with success criteria

Plus interactive prompts for ambiguity clarification (1-3 questions).

## Example

```
/spek.plan "Add two-factor authentication with SMS delivery"
```

Returns:

```
❯ Planning feature implementation...

## Specification Generation
  Loading vault context...
    - 5 prior decisions
    - 8 design patterns
  Running SpecKit specify command...
  ✓ Specification generated: specs/2fa-sms/spec.md

## Ambiguity Clarification
? (1/2) Should 2FA be mandatory for all users or optional?
  Your answer: Optional for now, admin can enforce per user
? (2/2) Which SMS providers to support (Twilio, AWS SNS, other)?
  Your answer: Twilio primary, AWS SNS as fallback

## Plan Generation
  Running SpecKit plan command...
  ✓ Plan generated: specs/2fa-sms/plan.md
  ✓ Tasks generated: specs/2fa-sms/tasks.md

✓ Feature planning complete
  Output: specs/2fa-sms/
    - spec.md (5 user stories, 12 requirements, 6 success criteria)
    - plan.md (3-week critical path, 4 risks identified)
    - tasks.md (18 tasks, P1/P2 priorities)

Next: /spek.implement --task T1.1
```

## Preconditions

- Must have run `/spek.prepare` first (or use `--skip-prepare`)
- SpecKit v0.9.6+ must be installed
- Feature description required (min 10 words)

## Artifacts Produced

### spec.md
- User scenarios with priorities (P1-P3)
- Functional requirements (FR-xxx)
- Non-functional requirements
- Success criteria (SC-xxx), measurable
- Key entities, assumptions

### plan.md
- Architecture overview (concepts, no code)
- Technology stack rationale
- Sequence and dependencies
- Risk assessment and mitigations
- Estimated hours and tokens

### tasks.md
- 10-30 independent tasks (T1.1, T2.3, etc.)
- Priorities (P0-P2)
- Success criteria per task
- Estimated hours/tokens
- Dependencies between tasks

## Error Cases

- ❌ SpecKit not installed: "Install with: uv tool install speckit>=0.9.6"
- ❌ Feature description too vague: "Provide at least 10 words"
- ❌ Not in Spekificity project: "Run 'spek init' first"

## Success Criteria

- ✓ spec.md generated with testable requirements
- ✓ plan.md generated with clear architecture
- ✓ tasks.md generated with independent, prioritized tasks
- ✓ All requirements traceable to user stories
- ✓ No circular task dependencies
- ✓ All success criteria measurable
