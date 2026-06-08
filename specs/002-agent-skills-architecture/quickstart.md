# Quickstart: Agent Skills Architecture Validation

**Purpose**: Document runnable validation scenarios that prove the agent skills architecture works end-to-end.

---

## Prerequisites

- Spekificity project initialized (`spek init` completed)
- Claude Code environment available (for agent skill invocation)
- SpecKit v0.9.6+ installed (`uv tool install speckit`)
- lat.md code index available (optional; graceful degradation if not)
- Project vault with prior decisions/patterns (optional; works with empty vault)

---

## Scenario 1: CLI Init Command Works

**Purpose**: Verify that `spek init` CLI command initializes project structure correctly.

**Setup**: Fresh project directory without vault/

**Steps**:
```bash
$ cd /path/to/new-project
$ git init  # Initialize git repo first

$ spek --version
spek version X.Y.Z  # Should show version

$ spek init
✓ Spekificity initialized in /Users/example/project
  Created:
    - vault/              (decisions, patterns, lessons storage)
    - .spek/              (project configuration)
    - specs/              (feature specifications)
    - .specify/           (internal SpecKit working directory)
  Next: spek prepare [FEATURE]
```

**Expected Output**:
- Exit code: 0
- Files created:
  - `vault/` directory exists
  - `vault/decisions.md` file exists
  - `vault/patterns.md` file exists
  - `.spek/` directory exists
  - `specs/` directory exists
  - `.specify/` directory exists

**Success Criteria**: ✓ All directories created, no errors

---

## Scenario 2: CLI Deprecated Command Shows Error with Agent Skill Redirect

**Purpose**: Verify that running deprecated CLI commands shows helpful error message directing to agent skills.

**Setup**: Project initialized with vault/

**Steps**:
```bash
$ spek plan "Add authentication to API"

Error: 'spek plan' requires Claude Code agent context. Use the agent skill:

  /spek.plan "Add authentication to API"

This interactive workflow generates spec → clarification → plan → tasks with your input.
Documentation: wiki/skills.md#spek.plan
```

**Expected Output**:
- Exit code: 1 (error)
- Error message includes `/spek.plan` syntax
- Links to documentation

**Repeat for**:
- `spek implement` → error → `/spek.implement`
- `spek conclude` → error → `/spek.conclude`

**Success Criteria**: ✓ All three commands show helpful error messages

---

## Scenario 3: Agent Skill `/spek.prepare` Loads Context

**Purpose**: Verify that agent skill loads vault context and code index correctly.

**Setup**: Project initialized with prior decisions in vault/

**Pre-populate vault** (for realistic test):
```bash
# Add sample decisions to vault/decisions.md
cat >> vault/decisions.md << 'EOF'
## Decision: Use Python for CLI implementation

**Status**: Implemented | **Date**: 2026-06-01 | **Author**: Marcel

Use Click framework for CLI argument parsing and command routing.

**Rationale**: Click is lightweight, well-maintained, and perfect for Spekificity's simple CLI needs (only init command).

**Alternatives**: argparse (standard lib but verbose), typer (newer but less stable)

**Tags**: architecture, cli, python
EOF
```

**Steps (in Claude Code)**:
```
/spek.prepare "Add user authentication"
```

**Expected Output**:
```
## Spekificity Feature Preparation

Feature: Add user authentication

## Prior Decisions
- Use Python for CLI implementation (Tags: architecture, cli)

## Relevant Patterns
- Context Injection Pattern: Load vault before agent workflow

## Codebase Index
- spekificity/cli/main.py (CLI router entry point)
- spekificity/core/vault.py (Context loading)
- spekificity/core/context.py (Context formatting)

## Context Summary
- Decisions loaded: 1
- Patterns loaded: 1
- Estimated context tokens: ~5000-10000

Ready to plan or implement. Next: /spek.plan
```

**Verification**:
- ✓ Prior decisions displayed
- ✓ Relevant patterns shown
- ✓ Code files listed
- ✓ Token estimate provided
- ✓ Next step suggested

**Success Criteria**: ✓ Context loads and displays correctly

---

## Scenario 4: Agent Skill `/spek.plan` Generates Spec, Plan, Tasks

**Purpose**: Verify that agent skill generates complete spec + plan + tasks workflow.

**Setup**: Project initialized, `/spek.prepare` completed

**Steps (in Claude Code)**:
```
/spek.plan "Add basic authentication (username/password only)"
```

**Expected Output** (condensed):
```
## Spekificity Feature Planning

## Specification Generation
- Loading vault context for enrichment...
  - 1 prior decisions
  - 2 design patterns
- Running SpecKit specify command...
✓ Specification generated: specs/add-auth/spec.md

## Ambiguity Clarification
- Identifying ambiguities in specification...
- Where should passwords be stored? (Database/Vault/File)
- Should password reset be supported?
- [User provides answers]
✓ Specification clarified

## Plan Generation
- Running SpecKit plan command...
✓ Plan generated: specs/add-auth/plan.md

## Task Breakdown
- Running SpecKit tasks command...
✓ Tasks generated: specs/add-auth/tasks.md

✓ Specification, plan, and tasks generated
  Output directory: specs/add-basic-auth/
    - spec.md: Feature specification
    - plan.md: Implementation architecture
    - tasks.md: Prioritized task list

Next: /spek.implement --task T1.1
```

**Verification**:
- ✓ spec.md exists with user scenarios + success criteria
- ✓ plan.md exists with architecture + phases
- ✓ tasks.md exists with prioritized, independent tasks
- ✓ Decisions logged (if any architecture choices made)

**Success Criteria**: ✓ All three artifacts generated and valid

---

## Scenario 5: Agent Skill `/spek.implement` Executes Task with Context

**Purpose**: Verify that agent skill injects context and executes implementation task.

**Setup**: Project with spec + plan + tasks generated

**Steps (in Claude Code)**:
```
/spek.implement --steps 1

# Executes Task T1.1 from tasks.md with injected context
# (e.g., "Create User model with name + email + password hash fields")
```

**Expected Output**:
```
## Implementing Task T1.1

Task: Create User model with name + email + password hash fields

## Task Context Loaded
- Relevant Patterns: 
  - "SQLAlchemy ORM pattern" (used in 3 other features)
  - "Password hashing with bcrypt" (example code available)
  
- Related Files:
  - models/ directory
  - existing User model (if any)
  
- Constitution Highlight:
  - Principle III (Spec-First): Implementation follows spec

## Context Injected
[Code examples, patterns, prior decisions displayed]

Proceed with implementation? (y/n): y

[Implementation executes...]

## Task Complete
✓ User model created with required fields
- Code committed to feature branch
- Decision logged: "Use SQLAlchemy ORM for database models"

Next: /spek.implement --steps 2
```

**Verification**:
- ✓ Context injected (patterns, related code, principles)
- ✓ User confirmation requested
- ✓ Code changes committed
- ✓ Decisions logged to vault
- ✓ Progress tracked

**Success Criteria**: ✓ Task executes with context injection

---

## Scenario 6: Agent Skill `/spek.conclude` Analyzes Outcomes

**Purpose**: Verify that agent skill analyzes implementation, extracts lessons, and updates vault.

**Setup**: Project with `/spek.implement` completed

**Steps (in Claude Code)**:
```
/spek.conclude --dry-run
```

**Expected Output**:
```
## Concluding Feature: Add Basic Authentication

## Outcomes Analysis
- Specification:
  ✓ All success criteria met
  ✓ 2/3 optional features implemented (password reset: deferred)
  
- Implementation:
  ✓ Code committed with spec linkage
  ✓ 5 decisions logged during development
  ✓ Token usage: 45k / 100k budget
  
- Test Coverage:
  ✓ Unit tests for User model
  ✓ Integration tests for login flow
  ✓ No end-to-end tests (out of scope)

## Lessons Extracted

What went well?
- SQLAlchemy ORM significantly simplified database layer
- Type checking caught 2 bugs before testing
- Reusing bcrypt library saved ~2 hours

What to improve?
- Password reset should have been in MVP (marked for next feature)
- Consider async password hashing for large user imports

## Vault Update (DRY-RUN)
[DRY-RUN: would update vault]
- New decisions would append to vault/decisions.md
- New patterns would append to vault/patterns.md
- Lessons would write to vault/lessons/2026-06-08-add-auth.md
- Code index would refresh via /lat.sync

Ready to conclude? (y/n):
```

**Verification**:
- ✓ Outcomes analyzed against success criteria
- ✓ Lessons extracted (what went well, what to improve)
- ✓ New decisions captured
- ✓ Vault updates previewed (dry-run mode)

**Success Criteria**: ✓ Conclusion workflow completes successfully

---

## Scenario 7: Context Flows from Vault → Agent → Back to Vault

**Purpose**: End-to-end test: Verify that decisions made during implementation are logged back to vault for future use.

**Setup**: Project with multiple completed features

**Steps**:
```
1. Run /spek.prepare "New feature" 
   → Displays decisions from vault/decisions.md

2. Run /spek.plan
   → Uses those decisions for spec enrichment
   → Captures NEW decisions during planning
   → Logs to vault/decisions.md

3. Run /spek.implement
   → Uses both old AND new decisions for context
   → Captures NEW decisions during implementation
   → Logs to vault/decisions.md

4. Run /spek.conclude
   → Reads all decisions from vault
   → Extracts patterns/lessons
   → Updates vault for next feature

5. Run /spek.prepare [NEXT FEATURE]
   → Displays decisions from BOTH prior features
   → Context compounds over time ✓
```

**Verification**:
- ✓ vault/decisions.md grows with each feature
- ✓ Later features see decisions from earlier features
- ✓ `/spek.prepare` displays cumulative context
- ✓ No information lost between features

**Success Criteria**: ✓ Context flows persist correctly

---

## Scenario 8: Caveman Mode Compresses Context

**Purpose**: Verify that caveman compression reduces context size while preserving essence.

**Setup**: Project with vault context loaded

**Steps (in Claude Code)**:
```
# Without compression
/spek.prepare "New feature"
[Output: ~300 lines, ~8000 tokens]

# With compression (full mode)
/spek.prepare "New feature" --caveman-mode=full
[Output: ~150 lines, ~3500 tokens]

# With compression (ultra mode)
/spek.prepare "New feature" --caveman-mode=ultra
[Output: ~80 lines, ~2000 tokens]
```

**Expected Output Comparison**:
```
Normal:
## Prior Decisions
- **Use Python for CLI implementation**
  Rationale: Click framework is lightweight and well-maintained
  Tags: architecture, cli, python

Caveman (full):
- Python CLI (Click) — lightweight, well-maintained (arch/cli)

Caveman (ultra):
- Python CLI: Click (lite, maint'd)
```

**Verification**:
- ✓ Caveman modes reduce token count
- ✓ Information preserved (decisions still visible)
- ✓ Structure maintained (decisions, patterns, code sections)

**Success Criteria**: ✓ Compression works without losing essential information

---

## Scenario 9: Graceful Degradation if Context Missing

**Purpose**: Verify that agent skills work even if optional context is missing.

**Setup**: Project without lat.md code index, or with minimal vault

**Steps (in Claude Code)**:
```
/spek.prepare "New feature"
```

**Expected Output**:
```
## Spekificity Feature Preparation

Feature: New feature

⚠ Code index not available (lat.md missing or stale)
  Falling back to semantic search of vault context

## Prior Decisions
[Displays what's in vault, even if small]

## Relevant Patterns
[Displays what's in vault]

## Code Files
[Semantic search fallback instead of lat.md query]

Ready to plan or implement. Next: /spek.plan
```

**Verification**:
- ✓ Works with missing code index (graceful degradation)
- ✓ Works with minimal vault (empty okay)
- ✓ Shows warnings but doesn't fail
- ✓ Continues with fallback strategies

**Success Criteria**: ✓ Graceful degradation works

---

## Summary Checklist

- [ ] Scenario 1: `spek init` creates vault and directories
- [ ] Scenario 2: Deprecated CLI commands show error → agent skill redirect
- [ ] Scenario 3: `/spek.prepare` loads context from vault
- [ ] Scenario 4: `/spek.plan` generates spec + plan + tasks
- [ ] Scenario 5: `/spek.implement` injects context and executes task
- [ ] Scenario 6: `/spek.conclude` analyzes outcomes and extracts lessons
- [ ] Scenario 7: Context flows persist (vault → agent → vault → next feature)
- [ ] Scenario 8: Caveman mode compresses context
- [ ] Scenario 9: Graceful degradation if context missing

**All scenarios pass**: ✓ Agent skills architecture is working correctly

---

## Troubleshooting

### Issue: `/spek.prepare` shows no context
**Cause**: Vault exists but is empty (no decisions.md)  
**Fix**: Add sample decisions to vault/decisions.md or run `/spek.plan` to generate them

### Issue: `spek plan` command gives error about agent skills
**Expected Behavior**: This is correct! Use `/spek.plan` instead.  
**How to fix**: Invoke as agent skill: `/spek.plan "feature description"`

### Issue: lat.md index not found
**Expected Behavior**: Graceful degradation — uses semantic search instead  
**How to fix**: Run `/lat.sync` to create/refresh code index (optional enhancement)

### Issue: Decisions not persisting to vault
**Cause**: Agent skill execution may have failed silently  
**Fix**: Check agent logs; verify vault/decisions.md is writable

---

## Next Steps After Validation

Once all scenarios pass:
1. Update CLAUDE.md with agent skills documentation
2. Create agent skill definition files in `.claude/skills/`
3. Remove/deprecate old CLI command implementations
4. Update wiki/skills.md with agent skill details
5. Run integration tests to verify end-to-end workflow
