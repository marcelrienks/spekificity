# CLI Command Contracts

**Version:** 1.0  
**Created:** 2026-06-08  
**Feature:** Complete Spekificity Framework CLI Implementation (spec 001)

---

## Overview

Five command contracts define the interface between CLI entry points and core functionality. All commands accept POSIX-style arguments and return structured output (Markdown or JSON).

---

## Command: `spek init`

Initialize Spekificity in a Git-managed project.

**Entry Point:** `spekificity/cli/main.py::init()`

**Usage:**
```bash
spek init
```

**Arguments:**
- None (runs in current directory)

**Preconditions:**
- Current directory must be a Git repository (`git status` succeeds)
- `.specify/` directory must not already exist (or user confirms overwrite)

**Postconditions:**
- `.specify/` directory created with standard structure:
  - `.specify/memory/constitution.md` (copy from template)
  - `.specify/templates/` (copy spec, plan, task templates)
  - `.specify/logs/` (empty, for progress tracking)
  - `.specify/extensions.yml` (extension configuration)
- `vault/` directory created with structure:
  - `vault/decisions.md` (copy from template)
  - `vault/patterns.md` (copy from template)
  - `vault/lessons/` (empty)
- `specs/` directory created (empty)
- `.github/copilot-instructions.md` written with skill registrations
- `.lat/` directory initialized (lat.md index)
- SpecKit per-project setup run (`speckit init .`)

**Output (stdout):**
```
❯ Initializing Spekificity...
  ✓ Created .specify/ directory
  ✓ Created vault/ directory
  ✓ Created specs/ directory
  ✓ Initialized lat.md index
  ✓ Initialized SpecKit per-project configuration
  ✓ Registered /spek.* skills in .github/copilot-instructions.md

Ready! Run: spek prepare "your feature name"
```

**Error Handling:**
- Exit code 1 if not in a Git repository: `Error: Not in a git repository`
- Exit code 1 if `.specify/` already exists: `Error: .specify/ already exists. Use --force to overwrite`

**Test Criteria:**
- `spek init` in clean Git repo creates all directories with correct files
- Subsequent `spek prepare` can execute (no missing dependencies)
- Rerunning `spek init` prompts for overwrite confirmation

---

## Command: `spek prepare [FEATURE]`

Load prior context, index codebase, generate navigation guide.

**Entry Point:** `spekificity/cli/main.py::prepare()`

**Usage:**
```bash
spek prepare "Your feature name"
spek prepare                          # Use current branch name
```

**Arguments:**
- `FEATURE` (optional): Feature name or description (3-100 chars)

**Preconditions:**
- Must be in a project initialized with `spek init`
- Git working directory must be clean (or use `--force`)

**Postconditions:**
- Vault loaded (decisions, patterns, lessons)
- Codebase indexed via lat.md (or fallback to semantic_search)
- Navigation guide generated

**Output (stdout):**
```
❯ Preparing feature context...

## Prior Decisions
- dec-001: Use SpecKit for spec-driven workflows
- dec-002: Vault stored in Git for version control

## Relevant Patterns
- pat-cli-001: SpecKit command wrapper pattern
- pat-testing-001: Fixture-based testing for vault

## Codebase Overview
- Total files: 847
- Key directories: spekificity/core, spekificity/integrations, spekificity/skills
- Relevant files (by intent):
  1. spekificity/core/vault.py (Vault class)
  2. spekificity/cli/main.py (CLI router)
  3. spekificity/integrations/speckit.py (SpecKit wrapper)

## Navigation Guide
To modify feature behavior, start with:
- spec.md: Define what you're building
- plan.md: Define how you'll build it
- tasks.md: Execute tasks in order

## Context Summary
- Decisions loaded: 3
- Patterns loaded: 5
- Files indexed: 847
- Estimated context tokens: 15000
- Estimated prep time: 22s

Ready to plan or implement. Next: spek plan
```

**Error Handling:**
- Exit code 1 if not in initialized project: `Error: Not in a Spekificity project. Run 'spek init' first`
- Exit code 1 if working directory not clean: `Error: Git working directory not clean. Commit changes or use --force`
- Exit code 1 if lat.md index fails: `Warning: lat.md indexing failed, using fallback semantic search (slower)`

**Options:**
- `--force`: Skip git clean check
- `--no-index`: Skip lat.md indexing (faster, less context)
- `--compressed`: Use Caveman mode for output

**Test Criteria:**
- Runs in <30 seconds for typical project
- Loads decisions/patterns from vault
- Generates accurate file list via lat.md
- Handles missing lat.md gracefully (falls back)
- Outputs structured, readable report

---

## Command: `spek plan [FEATURE]`

Generate specification, plan, and tasks from feature description.

**Entry Point:** `spekificity/cli/main.py::plan()`

**Usage:**
```bash
spek plan "User authentication with OAuth2 integration"
spek plan --spec ./specs/001-auth/spec.md  # Reference existing spec
```

**Arguments:**
- `FEATURE` (optional): Feature description (10-1000 chars)
- `--spec`: Path to existing spec.md to plan from

**Preconditions:**
- Must be in a project initialized with `spek init`
- Must have completed `spek prepare` in this session (or use `--skip-prepare`)

**Postconditions:**
- `specs/{feature-id}/spec.md` generated (via SpecKit)
- `specs/{feature-id}/plan.md` generated (via SpecKit)
- `specs/{feature-id}/tasks.md` generated (via SpecKit)
- Ambiguities identified and clarified interactively
- All artifacts validated (requirements testable, success criteria measurable)

**Output (stdout):**
```
❯ Planning feature implementation...

## Specification Generated
File: specs/001-auth/spec.md
- 3 user stories
- 12 functional requirements
- 6 success criteria
- 2 assumptions documented

## Ambiguities Detected (3)
? (1/3) Should OAuth2 support multiple providers (Google, GitHub, Okta)?
  Your answer: Yes, all three with configurable list

? (2/3) Should login sessions persist across browser restarts?
  Your answer: Yes, 30-day sliding expiry

? (3/3) Should 2FA be mandatory or optional?
  Your answer: Optional, user configurable

## Plan Generated
File: specs/001-auth/plan.md
- Architecture: Modular auth service with pluggable providers
- Tech stack: FastAPI, PyJWT, authlib, SQLAlchemy
- 4 risks identified with mitigations
- Critical path: 3 weeks

## Tasks Generated
File: specs/001-auth/tasks.md
- 15 tasks total
- Task breakdown:
  - Phase 1: Core infrastructure (T1.1-T1.4)
  - Phase 2: OAuth2 providers (T2.1-T2.3)
  - Phase 3: Testing & polish (T3.1-T3.8)
- Total estimated tokens: 85000
- Total estimated hours: 40

All requirements validated ✓
All tasks have independent success criteria ✓
No circular task dependencies ✓

Ready to implement. Next: spek implement --task T1.1
```

**Interactive Flow (Clarification):**
- For each ambiguity detected, prompt user with context-specific question
- Record answer in spec.md Assumptions section
- Re-validate spec after each answer

**Error Handling:**
- Exit code 1 if feature description is too vague: `Error: Feature too vague. Provide at least 10 words or existing spec.md`
- Exit code 1 if SpecKit unavailable: `Error: SpecKit not installed. Run 'spek install' first`
- Exit code 2 if validation fails: `Error: Generated plan has testability issues. Review specs/001-auth/plan.md`

**Options:**
- `--skip-prepare`: Don't run prepare first (faster if context already loaded)
- `--no-clarify`: Skip ambiguity clarification (use defaults)
- `--output-json`: Return spec/plan/tasks as JSON instead of Markdown

**Test Criteria:**
- Generates complete spec.md with user stories, requirements, success criteria
- Identifies 1-3 genuine ambiguities and clarifies interactively
- Validates all requirements are testable
- Validates all success criteria are measurable
- Generates independent, prioritized tasks
- All outputs saved to specs/{feature-id}/ directory

---

## Command: `spek implement [--task TASK_ID] [--resume]`

Execute implementation task with context injection and progress tracking.

**Entry Point:** `spekificity/cli/main.py::implement()`

**Usage:**
```bash
spek implement --task T1.1
spek implement --task T1.1 --resume    # Resume interrupted task
spek implement --list                  # List all tasks from current spec
```

**Arguments:**
- `--task TASK_ID`: Which task to execute (e.g., T1.1, T2.3)
- `--resume`: Resume interrupted task (skip context reload)
- `--list`: List all tasks and their status

**Preconditions:**
- Must be in a project initialized with `spek init`
- Must have completed `spek plan` (tasks.md exists)
- Task must be in tasks.md

**Postconditions:**
- Task context (decisions, patterns, code) injected into agent session
- Progress log created: `.specify/logs/{task_id}.log`
- Task marked In Progress
- Upon completion: task marked Complete + decision log written to vault

**Output (stdout):**
```
❯ Implementing task T1.1: Set up Python package structure...

## Task Context Loaded
- Relevant code files: 3 (spekificity/__init__.py, pyproject.toml, setup.cfg)
- Prior decisions: 2 (Use SpecKit, Store vault in Git)
- Relevant patterns: 1 (Python package structure pattern)
- Estimated context tokens: 5000

## Progress Log
File: .specify/logs/T1.1.log

Starting task at 2026-06-08 10:30:00 UTC
Task: Set up Python package structure, pyproject.toml, entry points
Description: Create Python 3.11+ compatible package, define dependencies (SpecKit, lat.md, Pydantic, GitPython), configure entry point `spek = spekificity.cli.main:main`
Success Criteria:
  ✓ pyproject.toml has all required dependencies
  ✓ Entry point configured and callable
  ✓ Package installs via `uv tool install -e .`

Agent session started. Inject this context:
[... context injected ...]

## Decision Logging
During implementation, log decisions via agent annotation:
@decision "Use dataclasses instead of Pydantic for CLI args; simpler for validation"

## Completion
When task complete, run: spek implement --task T1.1 --mark-complete
```

**Error Handling:**
- Exit code 1 if task not found: `Error: Task T1.1 not found in tasks.md`
- Exit code 1 if dependencies not met: `Error: Task T1.1 depends on T1.0. Complete that first`
- Exit code 1 if task already complete: `Error: Task T1.1 already complete. Use --force to re-run`

**Options:**
- `--mark-complete`: Mark task as complete without re-running
- `--mark-blocked`: Mark task as blocked (with reason)
- `--force`: Re-run task even if already complete
- `--skip-context`: Skip context injection (faster if context already loaded)

**Test Criteria:**
- Loads task context (decisions, patterns, code)
- Creates progress log at `.specify/logs/{task_id}.log`
- Injects context into agent session without errors
- Agent can log decisions via @decision annotations
- Task status updated in tasks.md

---

## Command: `spek conclude [--feature FEATURE] [--all]`

Analyze outcomes, extract lessons, update vault.

**Entry Point:** `spekificity/cli/main.py::conclude()`

**Usage:**
```bash
spek conclude --feature 001-complete-framework
spek conclude --all                    # Conclude all completed features
```

**Arguments:**
- `--feature FEATURE`: Feature branch or spec ID (e.g., 001-auth)
- `--all`: Conclude all features with all tasks marked complete

**Preconditions:**
- Must be in a project initialized with `spek init`
- Must have completed `spek implement` on all feature tasks
- All implementation progress logs exist

**Postconditions:**
- Lessons extracted and written to `vault/lessons/{date}-{feature}.md`
- New decisions appended to `vault/decisions.md`
- New patterns appended to `vault/patterns.md`
- Feature summary generated: `specs/{feature}/summary.md`
- Vault exported (if Obsidian CLI available)

**Output (stdout):**
```
❯ Concluding feature 001-complete-framework...

## Outcomes Analysis
Spec: Complete Spekificity Framework CLI Implementation
Status: Complete (all 15 tasks done)

### Success Criteria Validation
- SC-001: Users can install and initialize in <5 minutes
  ✓ Actual: 3 minutes (pre-reqs verified)
- SC-002: /spek.prepare completes in <30 seconds
  ✓ Actual: 22 seconds (with small vault)
- SC-003: All 3 skipped tests pass
  ✓ Actual: All 3 tests now pass

### Implementation Summary
- Actual tokens used: 187000 (estimated: 260-330K)
- Actual hours spent: 35 (estimated: 40-50)
- All 15 tasks completed on first attempt
- No major re-work required

## Lessons Extracted
File: vault/lessons/2026-06-08-001-complete-framework.md

### Key Learnings
1. Vault performance excellent at scale (100+ files loads <500ms)
2. lat.md MCP interface is stable but requires version pinning
3. SpecKit context enrichment works well with subprocess approach
4. Agent skill registration via .github/copilot-instructions.md is seamless

### New Patterns Identified
1. pat-orchestration-001: SpecKit wrapper pattern (how to inject context into SpecKit)
2. pat-testing-001: Fixture-based testing for vault + code index integration

### Refined Decisions
- dec-001: Use SpecKit for spec-driven workflows (APPROVED, confirmed in practice)
- dec-002: Vault stored in Git (APPROVED, performance excellent)

## Vault Updated
- 2 new decisions appended to vault/decisions.md
- 2 new patterns appended to vault/patterns.md
- Lessons file created: vault/lessons/2026-06-08-001-complete-framework.md

Ready for next feature. Run: spek prepare "next feature name"
```

**Error Handling:**
- Exit code 1 if feature not found: `Error: Feature 001-auth not found in specs/`
- Exit code 1 if not all tasks complete: `Error: 3 tasks not complete. Complete them before concluding`
- Exit code 2 if lessons extraction fails: `Error: Could not extract lessons. Check progress logs`

**Options:**
- `--export-vault`: Export vault using Obsidian CLI (if available)
- `--archive`: Archive completed feature to `archive/` directory
- `--dry-run`: Show what would be concluded without writing

**Test Criteria:**
- Analyzes outcomes vs success criteria
- Extracts 2+ lessons from implementation
- Identifies new patterns and refined decisions
- Writes lessons to vault/lessons/
- Updates vault/decisions.md and patterns.md
- Generates feature summary

---

## Summary: Command Contracts

| Command | Input | Output | Dependencies |
|---------|-------|--------|--------------|
| `spek init` | None | .specify/, vault/, specs/ | Git, Python 3.11+ |
| `spek prepare` | Feature name | Onboarding report | vault, lat.md |
| `spek plan` | Feature description | spec.md, plan.md, tasks.md | SpecKit, vault |
| `spek implement` | Task ID | Progress log, decision log | context, lat.md |
| `spek conclude` | Feature name | lessons.md, updated vault | Progress logs |

---

**CLI contracts complete. Ready for implementation.**
