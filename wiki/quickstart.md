# Spekificity Quick Start Guide

> 
> **Skill Level:** Beginner  
> **Outcome:** Complete your first feature using the Spekificity workflow

---

## Welcome!

This guide walks you through building a **complete feature** using Spekificity's 5-phase workflow. By the end, you'll understand:

- How to prepare your workspace
- How to write specs that agents can understand
- How to plan implementation without guessing
- How to execute with full context
- How to capture lessons learned

**Prerequisites:**

Before starting, complete the setup in [setup.md](setup.md):
- ✅ Python 3.11+
- ✅ Git initialized
- ✅ SpecKit installed globally
- ✅ Spekificity initialized in project

See [setup.md](setup.md) for detailed prerequisite verification.

---

## Prepare Your Workspace

### Purpose

Validate that your workspace is ready: git is clean, vault is current, code analysis tools are fresh, and session context is loaded.

### Step 1a: Quick Verification

Use this quick checklist (detailed verification in [setup.md](setup.md)):

```bash
python3 --version   # 3.11 or higher
git status          # On main branch, working tree clean
specify --version   # Global SpecKit installed
```

### Step 1b: Run /spek.prepare

```bash
/spek.prepare
```

This command:
1. ✅ Checks git working tree (should be clean)
2. ✅ Pulls latest vault updates (from Obsidian sync)
3. ✅ Refreshes CodeGraph from current code
4. ✅ Loads session memory (decisions, patterns, lessons)

**Expected Output:**
```
✓ Git working tree clean
✓ Vault synced (updated from origin)
✓ CodeGraph refreshed (23 files indexed)
✓ Session context loaded
READY: Workspace prepared for feature development
```

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| `git status` shows uncommitted changes | Run `git add .` and `git commit -m "..."`, or `git stash` to save work |
| Vault sync fails | Ensure Obsidian is open and git plugin is enabled; pull manually: `git pull origin vault` |
| CodeGraph refresh fails | Reinstall CodeGraph MCP config; see [setup.md](setup.md) |
| Session memory not loading | Check `.cel/context.md` and `.specify/memory/` for syntax errors |

---

## Phase 2: Specify Your Feature

### Purpose

Write a detailed, structured specification that defines **what** you're building and **why**. This spec guides implementation and becomes project documentation.

### Step 2a: Choose a Feature

For this quickstart, let's use a simple example:

**Feature:** "Add user authentication API endpoint"

You can use any real feature from your project instead.

### Step 2b: Write the Feature Intent

Create a brief description of what you want to build:

```
Goal: Add a POST /auth/login endpoint that validates user credentials 
and returns a JWT token.

Why: Users need to authenticate before accessing protected resources.

Scope: Login endpoint only (registration, password reset are separate features).

Out of Scope: Multi-factor authentication, session management, OAuth integration.
```

### Step 2c: Generate Enriched Specification

Run the specify command:

```bash
/spek.automate --phase=specify --feature="Add user authentication API endpoint"
```

Or use the direct SpecKit command:

```bash
/speckit.specify
```

When prompted:
- **Feature name:** `user-auth-api`
- **Description:** `Add POST /auth/login endpoint with JWT token generation`

**What Happens Next:**

Spekificity enriches the basic spec by:
1. 🔍 Querying CodeGraph for existing auth-related code
2. 🔗 Linking to relevant decisions (e.g., "Use JWT tokens")
3. 📋 Pulling patterns from vault (e.g., API error handling)
4. ✅ Adding enrichment layers:
   - Success Criteria (how to verify it works)
   - Assumptions (what must be true)
   - Risk Assessment (what could break)
   - Dependencies (related tasks)
   - Resource Estimate (time, tokens, complexity)

**Expected Spec Output:**

```markdown
# Spec: Add user authentication API endpoint

## Feature
POST /auth/login endpoint with JWT token generation

## Success Criteria
- [ ] Endpoint returns 200 with JWT for valid credentials
- [ ] Endpoint returns 401 for invalid credentials
- [ ] Token includes user ID and email claims
- [ ] Token expiration: 24 hours
- [ ] All tests pass locally

## Assumptions
- User model exists with hashed password field
- Database is migrated with password column
- JWT library is installed (PyJWT or similar)

## Risk Assessment
- **Risk:** Weak password hashing breaks security
  - Mitigation: Use bcrypt/argon2, verify with security team
- **Risk:** Token exposure in logs
  - Mitigation: Never log full tokens, only prefixes

## Dependencies
- Upstream: Database schema migration (issue #42)
- Downstream: Protect other endpoints with @auth decorator

## Estimate
- Scope: Medium complexity
- Complexity: Medium

## Implementation Tasks
1. Define JWT token schema and claims
2. Implement login validation function
3. Add /auth/login endpoint
4. Add test cases
5. Update API documentation
```

### Step 2d: Review & Approve Spec

✅ **Read through the generated spec.** Ask yourself:

- Does this spec describe what I want to build?
- Are success criteria clear and measurable?
- Are assumptions stated explicitly?
- Are risks identified and mitigated?
- Are dependencies listed?

**If spec is good:** Proceed to Phase 3.

**If spec needs changes:** Edit the spec file in vault, then commit:

```bash
git add wiki/specs/user-auth-api.md
git commit -m "Update auth spec: clarify token expiration and claims"
```

**Spec Location:**

Spec is saved in your vault (typically `wiki/specs/user-auth-api.md`). It's version-controlled and becomes part of your project documentation.

---

## Phase 3: Plan Your Implementation

### Purpose

Break the specification into **concrete tasks** with clear dependencies. This plan guides implementation and ensures nothing is missed.

### Step 3a: Generate Implementation Plan

```bash
/spek.automate --phase=plan --feature="user-auth-api"
```

Or directly:

```bash
/speckit.plan
```

**What Happens:**

Spekificity creates a detailed plan by:
1. 📌 Breaking spec into atomic tasks
2. 🔗 Mapping dependencies (which tasks block others)
3. 📊 Using CodeGraph to estimate impact (affected files, functions)
4. ⏱️ Sequencing tasks for efficient execution

**Expected Plan Output:**

```markdown
# Plan: Add user authentication API endpoint

## Task Sequence

### Task 1: Prepare environment
- Description: Install JWT library, add configuration
- Files affected: requirements.txt, config/auth.py
- Scope: Straightforward
- Depends on: (none)
- Blocks: Tasks 2–5

### Task 2: Design token schema
- Description: Define JWT claims, expiration, signing key
- Files affected: config/auth.py, models/token.py
- Est. time: 20 min
- Depends on: Task 1
- Blocks: Task 3

### Task 3: Implement login validation
- Description: Hash password, verify credentials
- Files affected: services/auth_service.py
- Est. time: 30 min
- Depends on: Task 2
- Blocks: Task 4

### Task 4: Add /auth/login endpoint
- Description: Create Flask/FastAPI route, return token
- Files affected: api/routes/auth.py
- Est. time: 20 min
- Depends on: Task 3
- Blocks: Task 5

### Task 5: Test and document
- Description: Unit tests, integration tests, API docs
- Files affected: tests/test_auth.py, docs/api.md
- Est. time: 30 min
- Depends on: Task 4
- Blocks: (none)

## Execution Order

1. Task 1 → 2 → 3 → 4 → 5 (linear; no parallelization possible)
2. Total estimated time: ~2 hours
3. Expected tokens with context: ~10k

## Impact Analysis

Files that will change:
```
api/routes/auth.py (new file)
services/auth_service.py (modify)
config/auth.py (create)
models/token.py (create)
tests/test_auth.py (new)
requirements.txt (add PyJWT)
docs/api.md (add endpoint)
```

Potential breaking changes: None (new endpoint, no existing API changes)
Dependent features: /protected/* endpoints (will need @auth decorator)
```

### Step 3b: Review Plan

✅ **Does the plan look right?**

- Are tasks in a sensible order?
- Are dependencies clear?
- Is the time estimate reasonable?
- Have high-risk tasks been flagged?

**If plan is good:** Proceed to Phase 4.

**If plan needs refinement:** Edit the plan file and commit:

```bash
git add wiki/plans/user-auth-api-plan.md
git commit -m "Refine plan: split Task 4 into two tasks"
```

---

## Phase 4: Implement (Execute Task Sequence)

### Purpose

Execute the plan with full context. Spekificity automatically:
- Loads relevant code (CodeGraph queries)
- Injects architectural decisions and patterns
- Provides task-by-task scaffolding
- Tracks what's done and what remains

### Step 4a: Start Implementation

```bash
/spek.implement --feature="user-auth-api"
```

This command:
1. 🔄 Loads plan (task sequence)
2. 📂 Queries CodeGraph for affected files
3. 📖 Injects relevant code context
4. 📋 Displays next task and scaffold
5. ▶️ Waits for your input

**Expected Output:**

```
═════════════════════════════════════════
 IMPLEMENTATION: user-auth-api
═════════════════════════════════════════

Loaded Plan: 5 tasks, ~2 hours estimated

CURRENT TASK: Task 1/5 — Prepare environment

Description:
  Install JWT library, add configuration

Files you'll modify:
  ✓ requirements.txt (add PyJWT)
  ✓ config/auth.py (create new)

Context loaded:
  → Current requirements.txt (23 dependencies)
  → Existing config/ structure
  → Project naming conventions (from vault)

Scaffold for config/auth.py:
────────────────────────────────────────
# config/auth.py
import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-key-change-in-prod")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = timedelta(hours=24)
────────────────────────────────────────

Next Steps:
1. Copy scaffold into config/auth.py
2. Add PyJWT to requirements.txt
3. Run: pip install -r requirements.txt
4. When done, type: /spek.implement --next

Questions? See nearby patterns in vault:
  → wiki/patterns/error-categorization-pattern-quick-ref.md
  → wiki/patterns/decorator-wrapper-pattern-quick-ref.md
```

### Step 4b: Execute Each Task

For each task:

1. **Read the task description** (what, why, files affected)
2. **Review provided code context** (existing code, patterns, decisions)
3. **Write your code** using the scaffold as a starting point
4. **Test locally** before marking complete
5. **Commit to git** (one commit per task)
6. **Move to next task**

**Example Task 1 Execution:**

```bash
# 1. Create config/auth.py
cat > config/auth.py << 'EOF'
import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-key-change-in-prod")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = timedelta(hours=24)
EOF

# 2. Update requirements.txt
echo "PyJWT==2.8.1" >> requirements.txt

# 3. Install
pip install -r requirements.txt

# 4. Verify
python3 -c "import jwt; print(jwt.__version__)"

# 5. Commit
git add config/auth.py requirements.txt
git commit -m "Task 1: Prepare environment — add JWT config and library"

# 6. Move to next task
/spek.implement --next
```

### Step 4c: Token Budget Tracking

As you implement, Spekificity tracks token usage. If you're running low:

```bash
# Check token budget
/spek.status --tokens

# Expected output:
# Session tokens used: 23,400 / 50,000 (47%)
# Remaining: 26,600
# Estimated tokens needed for remaining tasks: ~8,000
# Status: ✓ GREEN (enough tokens remain)
```

If you're running low, enable Caveman mode to compress responses:

```bash
# Enable Caveman mode for remaining tasks
/spek.implement --caveman --next
```

---

## Phase 5: Close & Capture Lessons (5 min)

### Purpose

Archive implementation results, extract lessons learned, update project vault, and refresh code analysis.

### Step 5a: Run Post-Processing

When all tasks are complete:

```bash
/spek.post --feature="user-auth-api"
```

This command:
1. ✅ Validates all tasks completed
2. 📦 Stages git commit
3. 📝 Extracts lessons learned (what worked, what didn't)
4. 🗂️ Updates vault (decisions, patterns, outcomes)
5. 🔄 Refreshes CodeGraph
6. 📊 Generates completion summary

**Expected Output:**

```
═════════════════════════════════════════
 CLOSE: user-auth-api
═════════════════════════════════════════

Task Completion Check:
✓ Task 1: Prepare environment
✓ Task 2: Design token schema
✓ Task 3: Implement login validation
✓ Task 4: Add /auth/login endpoint
✓ Task 5: Test and document

Summary Statistics:
─────────────────────────────────────────
Time spent: Within expectations ✓
Token usage: Acceptable ✓
Files changed: 7
Commits: 5
Tests added: 8
Tests passing: 8/8 ✓

Lessons Learned:
─────────────────────────────────────────
✓ What worked: CodeGraph context was accurate; saved manual file scanning
✓ What was hard: Setting up JWT claims schema; took 10 min longer than planned
✓ What to reuse: Error handling pattern (see patterns/error-categorization-pattern-quick-ref.md)
✓ For next time: Pre-validate password hashing library choice earlier

Session Review:
─────────────────────────────────────────
1. Read vault for decisions → 2 min well spent
2. Plan was 90% accurate; one task reordered
3. Caveman mode after Task 3 saved ~30% tokens
4. CodeGraph impact analysis was correct

Updated Vault:
─────────────────────────────────────────
✓ Architectural decisions recorded
✓ Patterns documented
✓ Lessons captured

Refreshing CodeGraph:
✓ CodeGraph rebuilt (47 files indexed, 23 functions added)

Ready to commit:
─────────────────────────────────────────
7 files changed, 156 insertions(+), 12 deletions(-)

Type: git push
Or type: /spek.post --commit to stage automatically
```

### Step 5b: Commit & Push

```bash
# Review changes
git diff --stat

# Commit (auto-generated message includes lessons)
git commit -m "Feature: Add user authentication API endpoint

## What was built
- POST /auth/login endpoint with JWT token generation
- Token validation with user credentials
- 24-hour token expiration

## Lessons learned
- CodeGraph context eliminated manual file scanning
- JWT claims schema needs earlier validation
- Error handling pattern from vault proved reusable

## Metrics
- Time: Completed as planned
- Tokens: 9,200 (8% under budget)
- Tests: 8/8 passing"

# Push to remote
git push origin main
```

### Step 5c: Next Feature

Your first feature is complete! 🎉

**Ready for the next one?**

```bash
# Prepare workspace for next feature
/spek.prepare

# Start next feature
/spek.automate --phase=specify --feature="Add user password reset"
```

---

## Troubleshooting & Common Issues

### Issue: /spek.prepare fails with "vault not synced"

**Solution:**
```bash
# Manually sync vault
cd wiki
git pull origin main
cd ..

# Retry prepare
/spek.prepare
```

### Issue: Spec is too vague; tasks are unclear

**Solution:**
1. Edit spec file in vault
2. Add more detail to scope/constraints
3. Commit changes
4. Regenerate plan: `/spek.automate --phase=plan`

### Issue: CodeGraph context is out of date

**Solution:**
```bash
# Force refresh
/spek.prepare --force-codegraph-refresh

# This rebuilds the entire code graph from scratch
```

### Issue: Running out of tokens before implementation is done

**Solution:**
```bash
# Option 1: Enable Caveman mode
/spek.implement --caveman

# Option 2: Checkpoint and continue in new session
git commit -m "WIP: tasks 1-3 complete"
# (new session)
/spek.prepare
/spek.implement --resume user-auth-api
```

### Issue: Test fails; need to modify spec/plan

**Solution:**
1. Identify which task failed
2. Edit spec/plan if needed
3. Commit changes
4. Restart implementation from that task: `/spek.implement --restart-task=3`

---

## Key Concepts

### Enrichment Layers

**Enrichment = context injection from vault.** When you run `/spek.automate`, it:
1. Reads your feature intent
2. Queries vault for decisions, patterns, lessons
3. Injects that context into spec generation
4. Result: Spec is tailored to your project's conventions

### Caveman Mode

**Caveman = compressed responses.** Instead of verbose explanations, you get:
- Concise bullet points
- Direct commands
- No fluff
- ~75% fewer tokens

### Task Sequence & Dependencies

**Tasks are ordered by dependencies.** `/spek.implement` shows:
- Which task blocks which others
- What files each task affects
- Impact analysis from CodeGraph

---

## Next Steps

**Congratulations!** You've completed your first feature using Spekificity.

### Learn More

- [wiki/workflow.md](workflow.md) — Detailed phases and workflows
- [wiki/intention.md](intention.md) — Project philosophy
- [wiki/architecture.md](architecture.md) — Technical architecture
- [.spekificity/skill-index.md](../.spekificity/skill-index.md) — Complete command reference

### Tips for Success

1. **Keep specs short & clear** — Details go in enrichment layers
2. **Review plans before implementing** — Catch issues early
3. **Commit after each task** — Enables checkpointing and recovery
4. **Use Caveman mode strategically** — Enable when token budget is tight
5. **Capture lessons every feature** — Build project knowledge

### Questions?

See [wiki/faq.md](faq.md) for common questions, or open an issue in the repo.

---

**Happy building! 🚀**
