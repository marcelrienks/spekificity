# Instructions: /spek.implement Skill

Execute a single task with all required context pre-loaded.

## When to Use

- Have a task ID from `tasks.md`
- Ready to start coding/testing specific task
- Need context about relevant code and decisions
- Want to track progress

## How It Works

1. **Load Context** — Vault + code analysis for task
2. **Create Progress Log** — `.specify/logs/{task_id}.log`
3. **Inject Context** — Into agent session
4. **Execute Task** — Developer/agent implements
5. **Log Decisions** — Via @decision annotations
6. **Mark Complete** — `/spek.implement --task T1.1 --mark-complete`

## Workflow

```bash
# List all tasks
/spek.implement --list

# Start task
/spek.implement --task T1.1

# [Agent/developer implements task]
# [Log decisions: @decision "use pattern X because..."]

# Mark complete
/spek.implement --task T1.1 --mark-complete
```

## Task List Example

```
/spek.implement --list

Tasks for feature oauth2-auth:

T1.1: Add OAuth2 provider base class
  Status: Not Started
  Dependencies: none
  Estimated: 2h, 3000 tokens

T1.2: Implement Google OAuth2 provider
  Status: Not Started
  Dependencies: T1.1
  Estimated: 1.5h, 2500 tokens

T1.3: Add login UI flow
  Status: Not Started
  Dependencies: T1.2
  Estimated: 2h, 3000 tokens
```

## Success = You Can...

- [ ] Start task with clear context (no need to search codebase)
- [ ] Complete task per success criteria
- [ ] Mark task complete with timestamp
- [ ] See progress in `.specify/logs/{task_id}.log`
- [ ] Move to next task (T1.2) with learned context

## Next Steps

After marking complete:

```
/spek.implement --task T1.2
# Implement next task, context carries forward
```

After all tasks complete:

```
/spek.conclude --feature oauth2-auth
# Analyze outcomes, extract lessons, update vault
```
