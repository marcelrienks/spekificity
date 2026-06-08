# Skill: Execute Tasks with Context Injection

**Invocation**: `/spek.implement`

## Purpose

Execute implementation tasks with injected context (vault decisions, code examples, patterns), track progress, log decisions made during development.

## Usage

```
/spek.implement [feature-name|spec-file] [--steps N] [--resume]
```

## What It Does

1. **Load Implementation Context**
   - Load spec.md, plan.md, tasks.md from `specs/{feature}/`
   - Load vault context (decisions, patterns) for task execution
   - Load code index (lat.md) for relevant code examples
   - Load constitution (principles) for governance reference

2. **Execute Tasks Sequentially**
   - Start at first task (or --steps N to resume)
   - For each task:
     - Inject relevant context (decisions, patterns, code examples)
     - Ask for confirmation before major code changes
     - Execute task implementation
     - Capture new decisions made during implementation
     - Mark task complete or defer
     - Log progress to vault

3. **Progress Tracking**
   - Track token usage against budget (warn if exceeded)
   - Prompt for alternative approaches if budget low
   - Suggest pattern references based on code context
   - Record deviations from spec in log

4. **Decision Persistence**
   - Capture new decisions made during implementation
   - Log to vault/decisions.md
   - Make available to future `/spek.prepare` runs

5. **Code Management**
   - Commit code changes with spec/plan linkage
   - Append new decisions to vault/decisions.md
   - Update progress log for feature
   - Increment task completion status

## Workflow Details

### Phase 1: Context Loading
- Load spec + plan + tasks from `specs/{feature}/`
- Load vault context (decisions, patterns)
- Load code index (lat.md)
- Load constitution (principles)
- Format context for task execution

### Phase 2: Task Execution Loop
**For each task** (sequential or starting at --steps N):
- Inject task context (relevant decisions, patterns, code examples)
- Ask for confirmation before major code changes
- Log task progress to vault
- Execute task implementation
- Capture new decisions during implementation
- Mark task complete or defer
- Move to next task

### Phase 3: Progress Tracking
- Track token usage against budget (warn if exceeded)
- Suggest alternative approaches if budget low
- Suggest pattern references based on code context
- Record deviations from spec with rationale

### Phase 4: Decision Logging
- Parse decisions made during task execution
- Append to vault/decisions.md
- Update progress log

### Phase 5: Code Persistence
- Commit code changes with spec/plan linkage
- Update vault (decisions, progress)
- Prepare for next task or `/spek.conclude`

## Output

**Artifacts Modified**:
- Source code files (per tasks)
- `vault/decisions.md` — Appended with new decisions
- Progress log: Task status, decisions, deviations

**Console Output**:
- Task progress (step N of M)
- Context injected (decisions, patterns, code examples)
- Confirmation prompts
- Token budget warnings
- Pattern suggestions
- Decision capture prompts

## Context Requirements

- `vault`: decisions, patterns for task context
- `code-index`: lat.md for code recommendations
- `constitution`: principles for governance reference

## Related Skills

- `/spek.prepare` — Load prior context (prerequisite)
- `/spek.plan` — Generate spec + plan + tasks (prerequisite)
- `/spek.conclude` — Analyze outcomes and extract lessons (next step)

## Examples

### Example 1: Execute All Tasks

```
/spek.implement "Add authentication"
```

Output (condensed):
```
## Implementing Tasks for: Add authentication

## Task 1: Create User model with fields

### Task Context Loaded
- Relevant Patterns:
  - "SQLAlchemy ORM pattern" (used in 3 other features)
  - "Password hashing with bcrypt" (example code available)
  
- Related Files:
  - models/ directory
  - Existing User model (if any)
  
- Constitution Highlight:
  - Principle III (Spec-First): Implementation follows spec

[Context injected - patterns, code examples, principles shown]

Proceed with implementation? (y/n): y

[Implementation executes...]

## Task 1 Complete
✓ User model created
- Code committed
- Decision logged: "Use SQLAlchemy ORM for database models"

## Task 2: Create authentication service
[Similar workflow...]

## Progress Summary
- Tasks completed: 2/5
- Token usage: 45k / 100k budget
- New decisions logged: 3
- Deviations from spec: 0

Next: /spek.implement --steps 3 (resume at task 3)
```

### Example 2: Resume Implementation

```
/spek.implement "Add auth" --steps 3
```

Resume at task 3, skipping completed tasks 1-2.

### Example 3: Check Progress

```
/spek.implement "Add auth" --list
```

List all tasks with completion status.

## Invocation Variants

### Resume from Specific Step

```
/spek.implement [feature] --steps N
```

Resume implementation starting at task N (skip 1 through N-1).

### Skip Context Injection

```
/spek.implement [feature] --skip-context
```

Execute without context injection (faster, less comprehensive).

### Mark Task Complete

```
/spek.implement [feature] --task T1.1 --mark-complete
```

Mark specific task as complete without executing.

## Interactive Elements

- **Confirmation Prompts**: Ask before major code changes
- **Token Budget Warnings**: Warn if approaching budget limit
- **Pattern Suggestions**: Recommend patterns based on code context
- **Decision Capture**: Prompt to capture design decisions made during implementation

## Implementation Notes

- **Sequential Execution**: Tasks run one at a time (respecting dependencies)
- **Context Injection**: Vault + code-index context loaded for each task
- **Graceful Degradation**: Works without code-index (uses semantic search fallback)
- **Progress Persistence**: Can resume interrupted implementation
- **Decision Logging**: New decisions captured and logged to vault automatically

## Documentation

See [wiki/skills.md#spek.implement](../../wiki/skills.md#spek.implement) for full specification.
