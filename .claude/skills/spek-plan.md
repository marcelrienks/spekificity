# Skill: Generate Specification & Implementation Plan

**Invocation**: `/spek.plan`

## Purpose

Convert feature description into specification, identify and resolve ambiguities, generate implementation plan with task breakdown.

## Usage

```
/spek.plan [feature-name|spec-file]
```

## What It Does

Executes SpecKit specification → clarification → planning → task breakdown sequence with user confirmation and remediation loops:

1. **Specification Phase**: Run `/speckit.specify` with vault context enrichment
   - Surface spec + success criteria + enrichment layers to user
   - Request confirmation or revisions

2. **Clarification Phase**: Identify gaps in specification
   - Surface clarification questions to user
   - Collect answers + integrate into spec
   - Loop until spec is unambiguous (no remediations needed)

3. **Planning Phase**: Generate implementation plan from enriched spec
   - Identify code sections to modify (lat.md impact analysis)
   - Estimate token budget per phase
   - Surface plan to user for review + approval
   - If remediation needed, flag issues to user + loop back

4. **Task Generation Phase**: Granular task breakdown from plan
   - Generate implementable tasks (one action per task)
   - Suggest related patterns + decision references
   - Surface task list to user for review
   - If remediation needed, re-process after user input

## Workflow Details

### Phase 1: Context Loading
- Load vault (decisions, patterns, lessons) for enrichment
- Load code index (lat.md) for impact analysis
- Load constitution (principles) for governance
- Format context for agent prompt

### Phase 2: Specification
- Run `/speckit.specify` with context enrichment
- Present generated spec to user
- Request approval or revisions
- Loop until approved

### Phase 3: Clarification (Interactive)
- Identify ambiguities in approved spec
- Ask clarification questions (max 5)
- Collect user answers
- Integrate answers into spec
- Loop until no ambiguities remain

### Phase 4: Planning
- Run `/speckit.plan` with enriched, clarified spec
- Identify impacted code sections
- Estimate token budget per phase
- Present plan for user review
- Request approval or revision

### Phase 5: Task Breakdown
- Run `/speckit.tasks` to generate task list
- Add pattern suggestions and decision references
- Present task list for final review
- Request approval or revision

### Phase 6: Persistence
- Write spec.md, plan.md, tasks.md to specs/{feature}/
- Log planning decisions to vault/decisions.md
- Update code index (if code changed during planning)

## Remediation Loop

After each phase, surface output to user for review:
- **Approved**: Continue to next phase
- **Revision Needed**: Apply fixes + reprocess from failure point
- **Stop**: User can halt at any checkpoint

## Output

**Artifacts Created**:
- `specs/{feature}/spec.md` — Feature specification with user scenarios + success criteria
- `specs/{feature}/plan.md` — Implementation architecture with phases + estimates
- `specs/{feature}/tasks.md` — Task list with IDs, dependencies, estimated complexity

**Decisions Logged** (if made during planning):
- Architecture decisions (if diverged from assumptions)
- Technology choices (if made during clarification)
- Clarifications resolved (in decision log)

**Console Output**:
- Phase progress (spec generation, clarification, planning, tasks)
- Clarification questions + user answers
- Approval checkpoints
- Output file paths

## Context Requirements

- `vault`: decisions, patterns, lessons (for spec enrichment)
- `code-index`: lat.md graph (for impact analysis)
- `constitution`: project principles (for governance validation)

## Related Skills

- `/spek.prepare` — Load prior context (prerequisite)
- `/spek.implement` — Execute generated tasks (next step)
- `/spek.conclude` — Analyze outcomes and extract lessons

## Examples

### Example 1: Basic Usage

```
/spek.plan "Add authentication"
```

Output:
```
## Spekificity Feature Planning

Feature: Add authentication

## Specification Generation
- Loading vault context for enrichment...
  - 5 prior decisions
  - 8 design patterns
- Running SpecKit specify command...
✓ Specification generated

## Ambiguity Clarification
- Identifying ambiguities...
- Question 1: Where should passwords be stored? (Database/Vault/File)
- Question 2: Should password reset be supported?
[User provides answers]
✓ Specification clarified

## Plan Generation
- Running SpecKit plan command...
✓ Plan generated with estimated token usage per phase

## Task Breakdown
- Running SpecKit tasks command...
✓ Tasks generated with dependencies and pattern suggestions

✓ Specification, plan, and tasks generated
  Output directory: specs/add-authentication/
    - spec.md: Feature specification
    - plan.md: Implementation architecture
    - tasks.md: Prioritized task list

Next: /spek.implement
```

### Example 2: With Existing Spec File

```
/spek.plan specs/add-auth/spec.md
```

Skips specification generation, starts with clarification phase on existing spec.

## Invocation Variants

### Quick Planning (Skip Clarification)

```
/spek.plan "Feature" --no-clarify
```

Skips ambiguity clarification phase, uses documented assumptions.

### Resume Planning

```
/spek.plan "Feature" --resume-from plan
```

Resume from a specific phase if interrupted.

## Implementation Notes

- **Interactive Loop**: After each phase, prompt user for approval before continuing
- **Remediation**: If user identifies issues, reprocess from that phase with updates
- **Vault Integration**: Log new decisions made during planning to vault/decisions.md
- **Context Efficiency**: Use vault + code-index to minimize context while maximizing relevance
- **Token Budgeting**: Estimate tokens per phase and warn if budget approached

## Documentation

See [wiki/skills.md#spek.plan](../../wiki/skills.md#spek.plan) for full specification.
