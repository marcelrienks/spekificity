# /spek.automate — automated speckit lifecycle skill

## description

drives the full speckit feature lifecycle — spec → plan → tasks → analyse → remediation → implement → postflight — without requiring the developer to issue each step manually. surfaces clarification questions interactively. saves workflow state after every step so `spek automate --resume` can recover from any interruption.

invoked after `spek automate "<description>"` completes preflight and writes the initial `workflow-state.json`.

## trigger

```
/spek.automate
```

## inputs

the skill reads all required context from files written by the shell script:

| input | source | description |
|-------|--------|-------------|
| `feature_description` | `workflow-state.json`.feature_description | natural-language feature description |
| `feature_branch` | `workflow-state.json`.feature_branch | git branch name (already created) |
| `feature_dir` | `workflow-state.json`.feature_dir | spec directory path (e.g. `specs/003-add-login/`) |
| `workflow_state` | `.spekificity/workflow-state.json` | full state including completed steps |
| vault context | `vault/context/` | decisions and patterns (loaded at spec + plan steps) |

## step sequence

```text
preflight (done by shell) → spec → plan → tasks → analyse → remediation → implement → postflight
```

---

## startup — read state

**always start by reading `.spekificity/workflow-state.json`.**

extract:
- `status` — must be `in-progress` or `halted`; if `complete`, output summary and halt
- `next_step` — the step to execute first
- `completed_steps[]` — steps already done; skip any step listed here
- `feature_branch`, `feature_dir`, `feature_description`

---

## step definitions

### step: spec

**vault context loading** (before invoking speckit):

1. read `VAULT_PATH` from `.spekificity/config.json` (key: `vault.path`, default: `vault/`)
2. read `${VAULT_PATH}/context/decisions.md` in full
3. read `${VAULT_PATH}/context/patterns.md` in full
4. scan `${VAULT_PATH}/graph/index.md` for node names that overlap with keywords in `feature_description` (fuzzy match — 2+ word overlap is sufficient)
5. for each matched node, read its node file from `${VAULT_PATH}/graph/nodes/`
6. build vault context prefix block:

```markdown
## vault context (injected by /spek.automate)

### architectural decisions
<relevant sections from decisions.md>

### patterns
<relevant sections from patterns.md>

### related codebase components
<matched graph node summaries>
```

if `vault/context/` does not exist or is empty: log `[spek] ⚠ vault context not available — proceeding without codebase context` and continue without the prefix.

**invoke speckit**:

invoke `/speckit.specify` with the vault context prefix prepended to the feature description prompt.

**completion check**: `<feature_dir>/spec.md` exists and contains a `## requirements` section.

**on halt**: re-invoke with "continue generating the spec from the last section completed."

**state write after spec completes**:
```json
{ "completed_steps": [..., "spec"], "next_step": "plan", "current_step": "spec", "last_updated": "<now>" }
```

---

### step: plan

**vault context loading**:

1. read `VAULT_PATH` from `.spekificity/config.json`
2. read `${VAULT_PATH}/context/decisions.md` in full
3. read entities listed in `<feature_dir>/spec.md` (under `### key entities`)
4. scan `${VAULT_PATH}/graph/nodes/` for nodes matching those entity names
5. build context prefix (same format as spec step but with entity-matched nodes)

**invoke speckit**: invoke `/speckit.plan` with the vault context prefix.

**completion check**: `<feature_dir>/plan.md` exists and contains a `## summary` section.

**on halt**: re-invoke with "continue generating the plan."

**state write after plan completes**:
```json
{ "completed_steps": [..., "plan"], "next_step": "tasks" }
```

---

### step: tasks

invoke `/speckit.tasks`.

**completion check**: `<feature_dir>/tasks.md` exists and contains at least one `- [ ]` task.

**on halt**: re-invoke `/speckit.tasks`.

**state write**:
```json
{ "completed_steps": [..., "tasks"], "next_step": "analyse" }
```

---

### step: analyse

invoke `/speckit.analyze`.

**completion check**: analysis report produced in-session (AI confirms all artifacts reviewed).

**on halt**: re-invoke `/speckit.analyze`.

**state write**:
```json
{ "completed_steps": [..., "analyse"], "next_step": "remediation" }
```

---

### step: remediation

after `/speckit.analyze`, surface all identified findings to the developer:

```
[spek] analyse found X remediation items:
  1. [<severity>] <item description>
  2. [<severity>] <item description>
[spek] proceed with automated remediation? [Y/n]
```

if developer approves (or presses enter):
- address each item in sequence using direct file edits
- for high-risk items (affecting >30% of tasks or introducing breaking changes): ask explicit per-item approval with impact scope before proceeding
- mark each item resolved with `[spek] ✓ resolved: <item>`

if no findings: log `[spek] ✓ no remediation needed — proceeding to implementation` and skip developer prompt.

**completion check**: all flagged items addressed or explicitly deferred.

**state write**:
```json
{ "completed_steps": [..., "remediation"], "next_step": "implement" }
```

---

### step: implement

invoke `/speckit.implement`.

**after each invocation**:
1. read `<feature_dir>/tasks.md`
2. count lines matching `- [ ]` (unchecked tasks)
3. if any unchecked tasks remain: log `[spek] ℹ <N> tasks remaining — continuing...` and re-invoke `/speckit.implement` with: *"continue implementing from the last incomplete task. all tasks marked [x] are complete."*
4. repeat until all tasks are `[x]` or retry limit reached

**retry limit**: 10 invocations. if limit reached: halt with `status: "halted"`, save state, log `[spek] ✗ implement retry limit reached (10). run 'spek automate --resume' after resolving blockers.`

**completion check**: all tasks in `tasks.md` are `[x]` (zero `- [ ]` lines).

**state write**:
```json
{ "completed_steps": [..., "implement"], "next_step": "postflight" }
```

---

### step: postflight

execute in order:

1. **update spec status**: in `<feature_dir>/spec.md` YAML front-matter, change `status: draft` → `status: complete`. if no front-matter exists, skip this sub-step.

2. **invoke `/spek.post`**: run the post-implementation skill (lessons + graph refresh). after completion:
   - write `postflight.lessons_written: true` to workflow-state.json
   - write `postflight.graph_refreshed: true` to workflow-state.json

3. **PR creation**: check `no_pr` field in workflow-state.json.
   - if `no_pr: false` (default): attempt `gh pr create`
   - if `no_pr: true`: skip PR, print instructions

   **PR with gh**:
   check `command -v gh && gh auth status`. if both pass:
   ```bash
   gh pr create \
     --title "feat(<NNN>): <feature_description>" \
     --body "$(head -40 <feature_dir>/spec.md)" \
     --base main
   ```
   write `postflight.pr_created: true` and `postflight.pr_url: <url>` to workflow-state.json.

   **PR terminal fallback** (if `gh` unavailable or unauthenticated):
   ```
   [spek] ⚠ gh cli not available — PR description for manual submission:

   Title: feat(<NNN>): <feature_description>

   Body:
   <first 40 lines of spec.md>

   To create manually: gh auth login, then re-run, or open a PR on GitHub.
   ```
   write `postflight.pr_created: false` to workflow-state.json.

4. **mark complete**: write final state:
   ```json
   { "status": "complete", "next_step": "complete", "completed_steps": [..., "postflight"] }
   ```

5. **print completion summary**:
   ```
   [spek] ✓ automate complete
     feature:   <feature_description>
     branch:    <feature_branch>
     spec:      <feature_dir>/spec.md (status: complete)
     pr:        <url or "not created — see instructions above">
     lessons:   written to vault/lessons/
     graph:     refreshed
   ```

---

## QA interface — question lifecycle

when speckit requests clarification at any step, surface it using this format:

```
[spek] ❓ clarification needed (step: <step_name>)
[spek] question: <question text>
>
```

the developer types their answer. the skill:

1. writes the question + answer to `workflow-state.json` under `pending_questions[]`:
   ```json
   { "step": "<step>", "question": "<text>", "answer": "<developer answer>" }
   ```
2. re-invokes the speckit step, providing the answer as additional context:
   *"The developer answered the following question: '<question>'. Answer: '<answer>'. Continue from where you left off."*
3. continues until the step reaches its completion condition

---

## workflow-state.json update protocol

after **every** step completes, atomically update workflow-state.json:

```json
{
  "last_updated": "<ISO-8601 now>",
  "current_step": "<just completed step>",
  "next_step": "<next step name>",
  "completed_steps": ["preflight", ..., "<just completed>"]
}
```

write to a temp file first (`.spekificity/.workflow-state.tmp`) then rename to `workflow-state.json` (atomic write — prevents partial state on interruption).

`status: "complete"` is written **only** after postflight step 4.

---

## resume logic

when reading workflow-state.json on startup:

1. if `status: "complete"` → print summary, exit (idempotency guard)
2. read `next_step`
3. skip all steps listed in `completed_steps`
4. begin execution from `next_step`
5. log: `[spek] resuming from step: <next_step> (completed: <list>)`

---

## error handling

| condition | action |
|-----------|--------|
| workflow-state.json missing | error — run `spek automate "<description>"` first |
| status is `complete` | print summary, exit 0 |
| speckit halt (no output file) | re-invoke with "continue" instruction |
| implement retry limit (10) | set status `halted`, save state, print resume instructions |
| postflight PR fails | print fallback description, mark `pr_created: false`, continue to complete |
| vault unavailable | log warning, skip vault context injection, continue |
