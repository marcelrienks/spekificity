# Skill: /spek.implement

Execute implementation task with context injection and progress tracking.

## Input

```
/spek.implement --task TASK_ID [--list] [--mark-complete] [--resume]
```

## Arguments

- `--task TASK_ID` (required): Task ID from tasks.md (e.g., T1.1, T2.3)
- `--list`: List all available tasks and their status
- `--mark-complete`: Mark task as complete without execution
- `--resume`: Resume interrupted task

## Output

Injects context into agent session:
- Relevant decisions from vault
- Relevant design patterns
- Relevant code files (via lat.md or semantic search)
- Progress log at `.specify/logs/{task_id}.log`
- Status message with next steps

## Example

```
/spek.implement --task T1.1
```

Returns:

```
❯ Implementing task T1.1: Add OAuth2 provider base class

## Task Context Loaded
- Decisions: 5 available
- Patterns: 8 available
- Relevant code files: 3 found via lat.md
  - spekificity/auth/providers/base.py
  - spekificity/tests/test_auth.py
  - spekificity/config.py

## Progress Log
File: .specify/logs/T1.1.log
Status: In Progress
Started: 2026-06-08 14:30:00 UTC

✓ Agent session started. Context injected.

When complete: /spek.implement --task T1.1 --mark-complete
```

## Preconditions

- Must be in Spekificity project (`spek init` run)
- Task must exist in `specs/{feature}/tasks.md`
- No task dependencies should be incomplete (warn, don't block)

## Context Injected

- **Decisions** — Prior decisions from vault relevant to this task
- **Patterns** — Design patterns applicable to this task
- **Code Files** — Relevant source files (top 5 by relevance)
- **Task Description** — Exact task text from tasks.md
- **Success Criteria** — Specific test conditions for completion

## Progress Tracking

- Progress log created at `.specify/logs/{task_id}.log`
- Developer can log decisions via agent annotations
- Task status updated in metadata

## Completion

Mark task complete when done:

```
/spek.implement --task T1.1 --mark-complete
```

Log entry:
```
✓ Task T1.1 marked complete
  Decisions logged: 2
  Time: 45 minutes
  Tokens: 3200
```

## Error Cases

- ❌ Task not found: "Task T1.1 not in tasks.md"
- ❌ Dependencies incomplete: "Blocking tasks not complete"
- ❌ Not in Spekificity project: "Run 'spek init' first"

## Success Criteria

- ✓ Context injected (decisions, patterns, code)
- ✓ Progress log created
- ✓ Task can be marked complete
- ✓ Decisions captured during implementation
