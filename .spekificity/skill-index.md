# Spekificity Skill Index

> **Complete reference for all `/spek.*` and `/speckit.*` commands**  
> **Updated:** 2026-05-20  
> **Status:** Current

---

## Quick Navigation

| Phase | Commands | Purpose |
|-------|----------|---------|
| **Prepare** | `/spek.prepare` | Workspace validation + context loading |
| **Specify** | `/spek.automate --phase=specify`, `/speckit.specify` | Spec generation with enrichment |
| **Plan** | `/spek.automate --phase=plan`, `/speckit.plan` | Task planning + dependency mapping |
| **Implement** | `/spek.implement`, `/spek.implement --next` | Task execution |
| **Close** | `/spek.post` | Lessons capture + vault update |

---

## Phase 1: Prepare

### `/spek.prepare`

**Purpose:** Pre-flight checks and context loading before feature development

**Command Syntax:**
```bash
/spek.prepare
/spek.prepare --force-codegraph-refresh  # Full graph rebuild
/spek.prepare --feature="feature-name"   # (Optional) pre-set feature
```

**Input:**
- Project must be Git-initialized
- Vault must exist (`.specify/` and `wiki/`)
- CodeGraph MCP must be configured

**Output:**
- ✅ Git working tree validation
- ✅ Vault freshness check
- ✅ CodeGraph sync complete
- ✅ Session context loaded
- ✅ Ready signal

**Expected Output Example:**
```
✓ Git working tree clean
✓ Vault synced (updated from origin)
✓ CodeGraph refreshed (23 files indexed, 156 functions)
✓ Session context loaded (5 decisions, 12 patterns, 3 lessons)
READY: Workspace prepared for feature development
```

**Error Handling:**

| Error | Cause | Fix |
|-------|-------|-----|
| `git: working tree not clean` | Uncommitted changes | `git add .` + `git commit` or `git stash` |
| `vault: not synced` | Obsidian changes not pulled | `git pull origin main` in vault |
| `codegraph: database locked` | Another process using graph | Wait 30s or restart |
| `session: context load failed` | Corrupt YAML in .specify/memory/ | Edit file or delete + regenerate |

**Estimated Time:** 5 minutes  
**Token Cost:** ~2,000 (one-time per session)

**Specification:** [specs/prepare-command.md](../specs/prepare-command.md)  
**See Also:** [quickstart.md Phase 1](quickstart.md#phase-1-prepare-your-workspace-5-min)

---

### `/spek.init`

**Purpose:** Initialize Spekificity framework in a new project

**Command Syntax:**
```bash
/spek.init
/spek.init --template=full    # Full structure with patterns
/spek.init --template=minimal # Bare minimum
```

**Input:**
- Project folder (must be Git-initialized)
- SpecKit installed globally

**Output:**
- `.specify/` directory created
- `wiki/` structure created
- `.spekificity/` config created
- `codesearch.db` (CodeGraph) created

**Expected Output:**
```
✓ .specify/ initialized
✓ wiki/ structure created
✓ .spekificity/ config initialized
✓ CodeGraph database created
Ready to use: /spek.prepare
```

**Estimated Time:** 2 minutes  
**Token Cost:** 0 (command-line only)

**See Also:** [setup.md](setup.md), [quickstart.md](quickstart.md)

---

## Phase 2: Specify

### `/spek.automate --phase=specify`

**Purpose:** Generate enriched feature specification with context from vault

**Command Syntax:**
```bash
/spek.automate --phase=specify --feature="feature-name"
/spek.automate --phase=specify  # Interactive prompt for feature name
/spek.automate --spec --feature="name"  # Short form
```

**Input:**
- Feature description or intent (user-provided)
- Vault context (decisions, patterns, lessons loaded)
- CodeGraph index (code analysis available)

**Output:**
- Specification document (Markdown)
- Enrichment layers applied:
  - Success Criteria
  - Assumptions
  - Risk Assessment
  - Dependencies
  - Resource Estimate
- Linked to relevant decisions/patterns in vault
- Git-staged for review

**Expected Enrichment:**

```markdown
# Spec: Feature Name

## Success Criteria
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2

## Assumptions
- Assumption A (must be true)
- Assumption B (validated with team)

## Risk Assessment
- Risk 1: Problem description
  - Mitigation: How to prevent/resolve

## Dependencies
- Upstream: Task must complete first
- Downstream: Other features depend on this

## Resource Estimate
- Time: X–Y hours
- Tokens: ~Z (with context)
- Complexity: Low/Medium/High
```

**Enrichment Process:**

```
Feature Intent (user)
  ↓
[Load Vault Context]
  ├─ Query: All decisions (what have we committed to?)
  ├─ Query: All patterns (what solutions do we reuse?)
  ├─ Query: Lessons learned (what did we learn last time?)
  └─ Query: Naming conventions (how do we name things?)
  ↓
[Query CodeGraph]
  ├─ Affected areas (which files/functions relate?)
  ├─ Existing code (what's already there?)
  └─ Impact scope (how much will this touch?)
  ↓
[Generate Spec]
  ├─ Apply project conventions
  ├─ Link to existing decisions
  ├─ Reference relevant patterns
  └─ Add enrichment layers
  ↓
Enriched Spec (vault-stored)
```

**Error Handling:**

| Error | Cause | Fix |
|-------|-------|-----|
| `feature name unclear` | Intent too vague | Rephrase with specific goal + scope |
| `no relevant decisions found` | Vault is empty | Add decisions manually or proceed without context |
| `codegraph: query timeout` | Large codebase | Reduce scope or run on smaller feature |
| `spec generation failed` | API/LLM error | Check internet connection, retry |

**Token Cost:** ~5,000–8,000 (enrichment + spec generation)  
**Estimated Time:** 15 minutes

**Comparison:** `/speckit.specify` (no enrichment)

**See Also:** [quickstart.md Phase 2](quickstart.md#phase-2-specify-your-feature-15-min), [architecture.md#enrichment-layer](architecture.md#enrichment-layer)

---

### `/speckit.specify`

**Purpose:** Generate raw feature specification (no enrichment)

**Command Syntax:**
```bash
/speckit.specify
# (Interactive prompt for feature details)
```

**Input:**
- Feature description (prompted interactively)
- No vault context (uses only user input)

**Output:**
- Basic specification (what, why, scope, out-of-scope)
- No enrichment layers
- No decision/pattern links
- Ready for manual enrichment

**When to Use:**

- ✅ You don't have a vault yet (new project)
- ✅ You want minimal AI assistance
- ✅ Feature is simple enough that enrichment isn't needed
- ❌ You want full Spekificity benefits (use `/spek.automate --phase=specify` instead)

**Token Cost:** ~2,000 (raw generation only)  
**Estimated Time:** 10 minutes

**Comparison:** `/spek.automate --phase=specify` (with enrichment)

**See Also:** [specs/3layer-query-rule.md](../specs/3layer-query-rule.md) (enrichment architecture)

---

## Phase 3: Plan

### `/spek.automate --phase=plan`

**Purpose:** Break spec into tasks, map dependencies, and validate feasibility

**Command Syntax:**
```bash
/spek.automate --phase=plan --feature="feature-name"
/spek.automate --plan
# Uses current feature from context
```

**Input:**
- Specification (from Phase 2)
- CodeGraph analysis (code structure, dependencies)
- Vault context (patterns, lessons from similar features)

**Output:**
- Detailed plan with task sequence
- Dependency graph (what blocks what)
- Task-level details:
  - Description
  - Files affected (from CodeGraph)
  - Estimated time per task
  - Dependencies (upstream/downstream)
- Impact analysis (how many files will change)
- Execution order (sequential or parallelizable)

**Expected Plan Output:**

```markdown
# Plan: Feature Name

## Task Sequence

### Task 1: Setup
- Description: ...
- Files affected: [from CodeGraph]
- Est. time: 15 min
- Depends on: (none)
- Blocks: Tasks 2–5

### Task 2: Implementation
- Description: ...
- Files affected: [from CodeGraph]
- Est. time: 30 min
- Depends on: Task 1
- Blocks: Task 4

... (more tasks)

## Execution Order
1 → 2 → 3 (parallel: 4, 5) → 6

## Impact Analysis
Files changed: 7
Functions added: 3
Breaking changes: None (new endpoint)
```

**CodeGraph Integration:**

```
[Query: Which files implement related logic?]
  → Files affected list
  
[Query: What functions will be called?]
  → Callers graph
  
[Query: What depends on this code?]
  → Dependents list
  
[Query: Which tasks can run in parallel?]
  → Dependency graph → parallelizable tasks
```

**Error Handling:**

| Error | Cause | Fix |
|-------|-------|-----|
| `spec not found` | Phase 2 (Specify) not run | Run `/spek.automate --phase=specify` first |
| `cyclic dependencies detected` | Task A blocks B, B blocks A | Reorder tasks or break into smaller tasks |
| `codegraph: impact analysis failed` | Large impact scope | Reduce feature scope |

**Token Cost:** ~4,000–6,000 (impact analysis + planning)  
**Estimated Time:** 10 minutes

**See Also:** [quickstart.md Phase 3](quickstart.md#phase-3-plan-your-implementation-10-min)

---

### `/speckit.plan`

**Purpose:** Generate raw plan (no enrichment or impact analysis)

**Command Syntax:**
```bash
/speckit.plan
# Uses spec from context
```

**Input:**
- Specification
- No CodeGraph (no impact analysis)
- No vault context

**Output:**
- Basic task list
- No dependency graph
- No impact analysis
- Manual sequencing needed

**When to Use:**
- ✅ You don't have CodeGraph configured yet
- ✅ Simple features (few tasks)
- ❌ Complex features (use `/spek.automate --phase=plan`)

**Token Cost:** ~1,500  
**Estimated Time:** 5 minutes

---

## Phase 4: Implement

### `/spek.implement`

**Purpose:** Execute implementation tasks with full context

**Command Syntax:**
```bash
/spek.implement
# Start from task 1 interactively

/spek.implement --task=2
# Jump to specific task

/spek.implement --next
# Move to next task (after completing current)

/spek.implement --resume feature-name
# Resume from last completed task

/spek.implement --restart
# Restart entire feature (clear progress)

/spek.implement --caveman
# Enable Caveman mode (compressed output, ~75% fewer tokens)

/spek.implement --metrics
# Show time/token metrics for each task
```

**Input:**
- Plan (from Phase 3)
- CodeGraph code context (full, scoped queries)
- Vault patterns and decisions (for reference)

**Output:**
- Per-task scaffolding (code templates)
- Contextual guidance (what to do, what to test)
- Progress tracking (which tasks complete)
- Git commits (one per task)

**Expected Task Output:**

```
═════════════════════════════════════════
 IMPLEMENTATION: feature-name
═════════════════════════════════════════

CURRENT TASK: Task 2/5 — Implement validation

Description:
  Create password validation function using bcrypt

Files you'll modify:
  ✓ services/auth_service.py
  ✓ tests/test_auth.py

Code Context (from CodeGraph):
─────────────────────────────────────────
# Existing similar function:
def validate_api_key(key: str) -> bool:
    return db.keys.find_one({"key": key})

# Existing test pattern:
@pytest.mark.asyncio
async def test_validate_something():
    assert validate_something(...) == True
─────────────────────────────────────────

Scaffold for services/auth_service.py:
─────────────────────────────────────────
import bcrypt

async def validate_credentials(username: str, password: str) -> bool:
    user = await db.users.find_one({"username": username})
    if not user:
        return False
    return bcrypt.checkpw(password.encode(), user.password_hash)
─────────────────────────────────────────

Next steps:
1. Implement the function
2. Add tests
3. Test locally: pytest tests/test_auth.py
4. Commit when ready
5. Type: /spek.implement --next
```

**Context Injection:**

```
[Load Task Details]
  ├─ Description
  ├─ Files affected (from Plan)
  └─ Estimated time
  ↓
[Query CodeGraph]
  ├─ Relevant existing code (similar patterns)
  ├─ File structure
  └─ Function signatures
  ↓
[Load from Vault]
  ├─ Error handling pattern
  ├─ Testing conventions
  └─ Naming rules
  ↓
[Generate Scaffold]
  ├─ Template + examples
  ├─ Links to patterns
  └─ Expected tests
  ↓
[Display Task]
```

**Commands During Implementation:**

| Command | Purpose |
|---------|---------|
| `/spek.implement --next` | Mark current task done, move to next |
| `/spek.implement --restart-task=2` | Undo and restart specific task |
| `/spek.implement --status` | Show progress (completed/remaining) |
| `/spek.implement --metrics` | Show time/token metrics |
| `/spek.implement --context` | Reload context (if code changed) |
| `/spek.implement --abort` | Cancel entire feature |

**Error Handling:**

| Scenario | Action |
|----------|--------|
| Task takes longer than estimated | Enable `--caveman` or checkpoint in new session |
| Code change invalidates task | Edit plan, restart task |
| Out of tokens | Checkpoint and continue in new session |
| Test failure | Debug, fix code, continue |

**Token Cost:** ~8,000–15,000 (highly variable by task complexity)  
**Estimated Time:** 1–4 hours (per feature)

**Session Continuity:**
- Tasks are checkpointed after each git commit
- Can resume in new session with `/spek.implement --resume feature-name`
- Full context reloaded (CodeGraph, vault, git history)

**See Also:** [quickstart.md Phase 4](quickstart.md#phase-4-implement-execute-task-sequence), [specs/spek-implement-workflow.md](../specs/spek-implement-workflow.md)

---

## Phase 5: Close

### `/spek.post`

**Purpose:** Archive feature, capture lessons, update vault, refresh state

**Command Syntax:**
```bash
/spek.post
# Finalize current feature

/spek.post --feature="feature-name"
# Finalize specific feature (if resuming)

/spek.post --abort
# Cancel entire feature (rollback to start)
```

**Input:**
- Completed implementation (all tasks done)
- Git history (commits for each task)
- Session notes (what went well/poorly)

**Output:**
- ✅ Task completion validation
- ✅ Lessons learned (captured from session)
- ✅ Vault updates (new decisions, patterns)
- ✅ CodeGraph refresh (fresh index)
- ✅ Summary statistics
- ✅ Ready-to-push commit

**Expected Output:**

```
═════════════════════════════════════════
 CLOSE: feature-name
═════════════════════════════════════════

Task Completion Check:
✓ Task 1/5: Prepare environment
✓ Task 2/5: Design token schema
✓ Task 3/5: Implement validation
✓ Task 4/5: Add endpoint
✓ Task 5/5: Test and document

Summary Statistics:
─────────────────────────────────────────
Time spent: 2h 15min (est. 2h 10min) ✓
Actual tokens: 9,200 (est. 10k) ✓
Files changed: 7
Commits: 5
Tests added: 8
Test pass rate: 100% ✓

Lessons Learned:
─────────────────────────────────────────
✓ What worked: CodeGraph context was accurate
✓ What was hard: JWT claims schema design (took extra 10 min)
✓ What to reuse: Error handling pattern
✓ For next time: Pre-validate token expiration earlier

Vault Updates:
─────────────────────────────────────────
✓ New decision: Use JWT tokens (Decision 12)
✓ New pattern: Auth endpoint pattern added
✓ Lessons archived to wiki/todo.md

CodeGraph Refresh:
─────────────────────────────────────────
✓ Rebuilt (47 files indexed, 23 functions added)

Ready to commit:
─────────────────────────────────────────
git push origin main
```

**Automatic Captures:**

- 📝 **Lessons learned** (extracted from your notes during implementation)
- 🔗 **New decisions** (if you made choices during implementation)
- 📚 **Patterns** (reusable code patterns identified)
- 📊 **Metrics** (time, tokens, quality metrics)

**Error Handling:**

| Error | Action |
|-------|--------|
| `not all tasks complete` | Verify all tasks done: `/spek.implement --status` |
| `git: nothing to commit` | Some work may not be staged: `git add .` |
| `vault: update failed` | Merge conflict: resolve manually then retry |

**Token Cost:** ~2,000–3,000  
**Estimated Time:** 5 minutes

**Abort Option:**
```bash
/spek.post --abort
# Rolls back spec, plan, implementation to initial state
# Removes feature branch
```

**See Also:** [specs/spek-lessons-command.md](../specs/spek-lessons-command.md)

---

## Utility Commands

### `/spek.status`

**Purpose:** Check current session state and metrics

**Command Syntax:**
```bash
/spek.status
# Show overall status

/spek.status --tokens
# Show token usage

/spek.status --git
# Show git state

/spek.status --feature
# Show current feature
```

**Output:**
```
Status: READY (workspace is prepared)
Feature: user-auth-api (task 2/5)
Tokens: 9,200 / 50,000 (18% remaining) ⚠
Git: main branch, working tree clean
Vault: 5 decisions, 12 patterns, 3 lessons loaded
CodeGraph: 156 functions indexed
```

---

### `/spek.help`

**Purpose:** Display command reference

**Command Syntax:**
```bash
/spek.help
# Show all commands

/spek.help prepare
# Show help for /spek.prepare

/spek.help skills
# Show all available skills
```

---

## Dependency Graph

```
┌──────────────────┐
│  /spek.init      │
│  Initialize      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  /spek.prepare   │
│  Per-session     │
└────────┬─────────┘
         │
         ▼
    ┌────────────────────────┐
    │ Choose Phase:          │
    └────┬──────┬────────┬───┘
         │      │        │
         ▼      ▼        ▼
    ┌────────────────┐ ┌──────────────────┐
    │ /spek.automate │ │ /speckit.specify │
    │ --phase=specify│ │ (no enrichment)  │
    └────────┬───────┘ └────────┬─────────┘
             │                  │
             └────────┬─────────┘
                      ▼
          ┌──────────────────────┐
          │ Spec Complete?       │
          │ Review + Approve     │
          └────────┬─────────────┘
                   │
                   ▼
    ┌─────────────────────────┐ ┌──────────────────┐
    │ /spek.automate          │ │ /speckit.plan    │
    │ --phase=plan            │ │ (no enrichment)  │
    └────────┬────────────────┘ └────────┬─────────┘
             │                          │
             └────────┬─────────────────┘
                      ▼
          ┌──────────────────────┐
          │ Plan Complete?       │
          │ Review + Approve     │
          └────────┬─────────────┘
                   │
                   ▼
          ┌──────────────────────┐
          │  /spek.implement     │
          │  Task 1 → 2 → ... → N│
          └────────┬─────────────┘
                   │
                   ▼
          ┌──────────────────────┐
          │ All Tasks Done?      │
          └────────┬─────────────┘
                   │
                   ▼
          ┌──────────────────────┐
          │  /spek.post          │
          │  Close & Lessons     │
          └────────┬─────────────┘
                   │
                   ▼
          ┌──────────────────────┐
          │ Feature Complete! 🎉 │
          │ git push             │
          └──────────────────────┘
```

---

## Quick Reference: When to Use Which Command

| Scenario | Command | Reason |
|----------|---------|--------|
| Starting new feature | `/spek.prepare` | Always safe, validates state |
| First time on project | `/spek.init` | One-time setup |
| Generating spec | `/spek.automate --phase=specify` | Get context from vault |
| Simple spec (no vault) | `/speckit.specify` | Faster, minimal overhead |
| Creating plan | `/spek.automate --phase=plan` | Includes CodeGraph impact analysis |
| Simple plan (no graph) | `/speckit.plan` | Works without CodeGraph |
| Implementing | `/spek.implement` | Full context, task scaffolding |
| Finishing feature | `/spek.post` | Captures lessons, updates vault |
| Checking progress | `/spek.status` | See what's done, tokens remaining |
| Need help | `/spek.help` | Command reference |

---

## Skill Chaining (Advanced)

Multiple skills can be chained in sequence:

**Full automation:**
```bash
/spek.prepare && \
/spek.automate --phase=specify --feature="my-feature" && \
/spek.automate --phase=plan && \
echo "Ready to implement: /spek.implement"
```

**Partial automation:**
```bash
/spek.prepare && \
/spek.automate --phase=specify && \
# Manual review of spec
/spek.automate --phase=plan && \
# Manual review of plan
/spek.implement
```

**See also:** [specs/cli-orchestration.md](../specs/cli-orchestration.md)

---

## Configuration

All skills read configuration from:

| File | Purpose |
|------|---------|
| `.specify/config.yml` | SpecKit configuration |
| `.specify/extensions.yml` | Skill hooks (before/after phases) |
| `.spekificity/` | Spekificity-specific config |

---

## Further Reading

- [quickstart.md](../wiki/quickstart.md) — Step-by-step first feature
- [workflow.md](../wiki/workflow.md) — Detailed phases and workflows
- [specs/](../specs/) — Full specifications for each skill
- [patterns/](../wiki/patterns/) — Common patterns and quick-refs

---

**Last Updated:** 2026-05-20  
**Maintainer:** Spekificity Team  
**Questions?** See [faq.md](../wiki/faq.md)
