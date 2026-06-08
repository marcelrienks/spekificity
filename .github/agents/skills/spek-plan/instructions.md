# Instructions: /spek.plan Skill

## Purpose

Convert a natural language feature description into a formal, testable specification and implementation plan with prioritized, independent tasks.

## When to Use

- After `/spek.prepare` (context loaded)
- Have a clear feature intent/description
- Need to define scope before coding
- Want to identify ambiguities upfront

## How It Works

### 1. Generate Specification
- Load vault context (prior decisions, patterns)
- Invoke SpecKit specify command with enriched intent
- Generate `spec.md` with:
  - User stories (P1-P3 priorities)
  - Functional requirements (FR-xxx)
  - Success criteria (SC-xxx)
  - Assumptions documented

### 2. Clarify Ambiguities
- Identify 1-3 ambiguous points in feature intent
- Prompt developer interactively for each
- Encode answers into Assumptions section
- Re-validate spec after clarifications

### 3. Generate Plan
- Invoke SpecKit plan command
- Generate `plan.md` with:
  - Architecture overview (concepts only, no code)
  - Technology stack with rationale
  - Sequencing and dependency graph
  - Risk assessment and mitigations
  - Estimated effort (hours, tokens)

### 4. Generate Tasks
- Invoke SpecKit tasks generation
- Generate `tasks.md` with:
  - 10-30 independent tasks
  - Priorities and dependencies
  - Success criteria per task
  - Estimates

## Output Organization

All outputs stored in `specs/{feature-slug}/`:
```
specs/
├── oauth2-auth/
│   ├── spec.md (specification)
│   ├── plan.md (architecture + sequencing)
│   └── tasks.md (task breakdown)
└── [other-features]/
```

## Validation Performed

Before returning success:
- ✓ All requirements are testable (no vague language)
- ✓ All success criteria are measurable (have metrics/thresholds)
- ✓ All requirements traceable to user stories
- ✓ All tasks have independent success criteria
- ✓ No circular task dependencies
- ✓ Architecture is concepts-only (no code snippets)

## Common Flows

### Standard Flow
```bash
/spek.prepare "OAuth2 authentication"
# ↓ Load context
/spek.plan "Add OAuth2 support with Google and GitHub providers"
# ↓ Get prompted for ambiguities
# ↓ Specification, plan, tasks generated
```

### Skip Prepare
```bash
/spek.plan "Feature description" --skip-prepare
# Useful if context already loaded
```

### Skip Clarification
```bash
/spek.plan "Feature" --no-clarify
# Use defaults; don't prompt for ambiguities (faster)
```

## Ambiguity Clarification

You'll be asked 1-3 targeted questions:

Example:
```
? (1/3) Should login sessions persist across browser restarts?
  Answer: [yes/no + rationale]

? (2/3) Should 2FA be mandatory or optional?
  Answer: [describe requirement]

? (3/3) Which payment processors to support?
  Answer: [list options]
```

Answer clearly; answers are encoded in spec Assumptions.

## Success = You Can...

- [ ] Read spec.md and understand ALL user stories
- [ ] Read plan.md and explain architecture at high level
- [ ] Read tasks.md and estimate total effort
- [ ] Identify dependencies between tasks
- [ ] Start implementing T1.1 without confusion
- [ ] Know success criteria for each task

## If It Fails

| Error | Solution |
|-------|----------|
| "SpecKit not installed" | Run: `uv tool install speckit>=0.9.6` |
| "Feature too vague" | Provide at least 10 words, be specific |
| "Not in Spekificity project" | Run `spek init` first |
| "Validation failed" | Review spec.md; fix vague requirements |

## Dependencies

- ✓ SpecKit v0.9.6+ installed
- ✓ Spekificity initialized
- ✓ Feature context loaded (from `/spek.prepare`)

## Next Steps

After plan is generated:

1. **Review** — Read spec.md, plan.md, tasks.md carefully
2. **Clarify** — Ask questions if requirements unclear
3. **Implement** — Run `/spek.implement --task T1.1` to start
4. **Track** — Progress logged to `.specify/logs/`
5. **Conclude** — Run `/spek.conclude` when all tasks done
