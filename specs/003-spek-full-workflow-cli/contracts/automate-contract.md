# contract: /spek.automate skill

**feature**: `003-spek-full-workflow-cli`
**version**: 1.0
**date**: 2026-05-03

---

## overview

`/spek.automate` is an ai agent skill that drives the full speckit feature lifecycle — spec → plan → tasks → analyse → remediation → implement — without requiring the developer to issue each step manually. this contract defines the skill's required inputs, the step execution sequence, how it surfaces questions to the developer, and what constitutes completion.

---

## invocation

the skill is invoked in two modes:

### fresh start

triggered by `spek automate "<feature description>"` shell command. the shell script creates the feature branch and writes an initial `workflow-state.json`, then the ai reads `/spek.automate` skill.

the skill receives:
- `feature_description`: the natural-language description provided by the developer
- `feature_branch`: the git branch name created by the preflight step
- `feature_dir`: the spec directory for this feature (e.g., `specs/003-add-user-login/`)
- `workflow_state`: the current `workflow-state.json` contents

### resume

triggered by `spek automate --resume`. the ai reads `workflow-state.json` first, then reads `/spek.automate` skill beginning from `next_step`.

---

## step sequence

```text
preflight → spec → plan → tasks → analyse → remediation → implement → postflight
```

each step has:
- **completion condition**: the verifiable criterion the ai checks before advancing
- **on halt**: what the ai does if the underlying speckit command stops without completing

### step definitions

| step | skill invoked | completion condition | on halt |
|------|--------------|---------------------|---------|
| `preflight` | (shell script) | branch exists + working tree clean | error — do not proceed |
| `spec` | `/speckit.specify` | `<feature_dir>/spec.md` exists with `## requirements` section | re-invoke with "continue from last point" |
| `plan` | `/speckit.plan` | `<feature_dir>/plan.md` exists with `## summary` section | re-invoke with "continue from last point" |
| `tasks` | `/speckit.tasks` | `<feature_dir>/tasks.md` exists with at least one `- [ ]` task | re-invoke |
| `analyse` | `/speckit.analyze` | ai confirms analysis report produced (in-session) | re-invoke |
| `remediation` | inline ai | all flagged items addressed or explicitly deferred | surface to developer for input |
| `implement` | `/speckit.implement` | all tasks in `tasks.md` are `[x]` | re-invoke with "continue from last incomplete task" |
| `postflight` | `/spek.post` | `postflight.*` flags in workflow-state.json are true | individual step retry |

---

## question interface

when speckit requests clarification at any step, `/spek.automate` surfaces the question to the developer using this format:

```
[spek] ❓ clarification needed (step: <step_name>)
[spek] question: <question text>
> 
```

the developer types their answer. the skill records the answer in `workflow-state.json` under `pending_questions[]` and injects it back into the speckit invocation.

### question lifecycle

1. speckit produces a question during a step
2. ai writes question to `workflow-state.json` with `answer: null`
3. ai presents question to developer with `[spek] ❓` format
4. developer responds
5. ai records answer in `workflow-state.json`
6. ai re-invokes the speckit step, providing the answer as additional context
7. step proceeds to completion

### minimising questions

the skill must consult vault context before each step to pre-answer questions that can be resolved from existing patterns, decisions, or codebase structure. a well-configured vault should reduce developer interactions to ≤ 5 for a well-described feature (sc-002).

---

## vault context injection

before invoking the spec and plan steps, the skill reads vault context:

**for spec step**:
- read `vault/context/patterns.md` — inject into spec context
- read `vault/context/decisions.md` — inject into spec context
- read relevant graph nodes from `vault/graph/` — inject related components

**for plan step**:
- read `vault/context/decisions.md` — inject into plan context
- identify impacted graph nodes — reference in plan without re-reading source files

injection format: the skill prepends vault context to the speckit invocation as additional context that informs the output.

---

## remediation step

after the analyse step, if `/speckit.analyze` identifies cross-artifact inconsistencies or quality issues:

1. the skill surfaces all remediation items to the developer:
```
[spek] analyse found X remediation items:
  1. [medium] <item description>
  2. [high] <item description>
[spek] proceed with automated remediation? [Y/n]
```

2. if developer approves (or presses enter):
   - the ai addresses each item in sequence
   - high-risk items (affecting > 30% of tasks or introducing breaking changes) require explicit approval per item

3. if developer declines:
   - items are recorded in workflow-state.json as explicitly deferred
   - workflow continues to implement

---

## implementation halt detection

during the implement step, speckit may halt mid-task (context window limit, tool exit, etc.). the ai detects this by:

1. after each implement invocation, reading `tasks.md`
2. counting unchecked tasks (`- [ ]`)
3. if unchecked tasks remain, re-invoking `/speckit.implement` with: *"continue implementing from the last incomplete task. all tasks marked [x] are complete."*
4. repeat until all tasks are `[x]`

maximum retry attempts: 10. if limit reached, halt with exit code 3 and save state.

---

## workflow state writes

the ai must write to `workflow-state.json` after every step:

```
after spec completes → completed_steps: ["preflight", "spec"], next_step: "plan", current_step: "spec", status: "in-progress"
after plan completes → completed_steps: ["preflight", "spec", "plan"], next_step: "tasks"
...
after implement completes → completed_steps: [..., "implement"], next_step: "postflight"
after postflight → status: "complete", next_step: "complete"
```

all writes are atomic (write to temp file, then mv).

---

## completion criteria

the skill is complete when:

1. `status: "complete"` is written to `workflow-state.json`
2. all tasks in `tasks.md` are `[x]`
3. `postflight.pr_created` is `true` (or `--no-pr` was passed)
4. `postflight.lessons_written` is `true`
5. `postflight.graph_refreshed` is `true`

---

## error handling

| condition | action |
|-----------|--------|
| preflight fails (uncommitted changes) | halt, exit code 2, instruct developer to commit or stash |
| branch already exists | ask developer: reuse or create with suffix (suffix convention: append `-2`, incrementing — e.g. if `003-add-login` exists, create `003-add-login-2`, then `003-add-login-3`) |
| step retry limit exceeded | halt, save state, exit code 3, provide resume instructions |
| pr creation fails | print pr description to terminal, continue to complete |
| vault unavailable | continue without vault context injection (warn, do not halt) |
