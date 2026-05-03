# Acceptance Tests: SC-002 — Automated Feature Lifecycle (≤5 Interactions)

**Scenario**: SC-002: Developer drives spec→implement in ≤5 developer interactions  
**Feature**: 003-spek-full-workflow-cli  
**Test Date**: [fill on execution]  
**Tester**: [AI Agent / Developer]

---

## Test Scenario 1: Full automated lifecycle run

**Given**:
- `spek setup` and `spek init` completed
- Clean git working tree on `main`
- A natural-language feature description ready

**When**: Developer runs:
```bash
spek automate "add rate limiting to the API"
```
then invokes `/spek.automate` in the AI session

**Then**:
- [ ] A feature branch `NNN-add-rate-limiting-to-the-api` is created and checked out
- [ ] `workflow-state.json` written with `status: "in-progress"` and `next_step: "spec"`
- [ ] `/spek.automate` drives spec → plan → tasks → analyse → remediation → implement sequentially
- [ ] Each step's completion is confirmed before moving to next
- [ ] `spec.md` created with `## requirements` section
- [ ] `plan.md` created with `## summary` section
- [ ] `tasks.md` created with at least one `- [ ]` task
- [ ] All tasks marked `[x]` after implement step
- [ ] Total developer interactions (keystrokes/prompts outside `/spek.automate`) ≤ 5
- [ ] `workflow-state.json` ends with `status: "complete"` after postflight

**Evidence**:
```bash
git branch --show-current
jq .status .spekificity/workflow-state.json
jq .completed_steps .spekificity/workflow-state.json
grep -c '\- \[x\]' specs/*/tasks.md
grep -c '\- \[ \]' specs/*/tasks.md   # should be 0
```

---

## Test Scenario 2: Resume after interruption

**Given**:
- `spek automate` previously ran and created `workflow-state.json` with `status: "in-progress"` and `next_step: "tasks"`

**When**: Developer runs:
```bash
spek automate --resume
```

**Then**:
- [ ] Shell prints resume point: `next step: tasks`
- [ ] No new branch created (existing branch reused)
- [ ] `/spek.automate` continues from `tasks` step, skipping `spec` and `plan`
- [ ] Exit code 0

**Evidence**:
```bash
spek automate --resume
jq .next_step .spekificity/workflow-state.json
jq .completed_steps .spekificity/workflow-state.json
```

---

## Test Scenario 3: Idempotency — resume after complete

**Given**: `workflow-state.json` has `status: "complete"`

**When**: Run `spek automate "any description"`

**Then**:
- [ ] Shell prints idempotency guard message
- [ ] No new branch created
- [ ] Exit code 0

**Evidence**:
```bash
spek automate "any description"
echo "exit: $?"
git branch --show-current   # unchanged
```

---

## Test Scenario 4: Branch conflict — suffix resolution

**Given**: Branch `003-add-rate-limiting` already exists

**When**: `spek automate` generates the same branch name

**Then**:
- [ ] Shell prompts: `reuse existing branch or create with suffix? [reuse/suffix]`
- [ ] Entering `suffix` creates `003-add-rate-limiting-2`
- [ ] Entering `reuse` checks out existing branch

**Evidence**:
```bash
git branch --list | grep 003-add-rate-limiting
```
