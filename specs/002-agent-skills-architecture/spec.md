# Feature Specification: Agent Skills Architecture Fix

**Feature Branch**: `002-agent-skills-architecture`

**Created**: 2026-06-08

**Status**: Draft

**Summary**: Fix architectural mismatch between intended agent skills and current CLI implementation. `/spek.prepare`, `/spek.plan`, `/spek.implement`, and `/spek.conclude` are documented as interactive agent workflows in the wiki but implemented as incomplete CLI stubs. This feature realigns implementation to design.

## Problem Statement

The Spekificity framework has an architectural mismatch:

**Intended Design** (from wiki/skills.md):
- `/spek.prepare`: Load vault, index code, present interactive onboarding
- `/spek.plan`: Execute spec → clarify → plan → tasks sequence with user confirmation loops and remediation
- `/spek.implement`: Execute tasks with confirmation, track tokens, capture decisions interactively
- `/spek.conclude`: Interactive analysis, lessons extraction, vault sync

**Current Implementation** (CLI stubs in spekificity/cli/main.py):
- All four are Python CLI commands that print progress messages
- Missing interactive confirmations, remediation loops, and agent context injection
- Misleading output like "Agent session started" that doesn't actually start an agent
- No integration with Claude Code agent skills framework

**Impact**:
- Users cannot use these commands as documented
- The framework claims to be spec-driven but lacks the interactive workflows to support it
- CLAUDE.md incorrectly describes these as CLI commands instead of agent skills

## Success Criteria

1. **Architecture Clarity**: `spek init` is the ONLY true CLI command (project initialization). All workflow commands (`prepare`, `plan`, `implement`, `conclude`) are documented as agent skills (invoked as `/spek.prepare`, `/spek.plan`, etc.).

2. **Agent Skills Implementation**: Each agent skill follows the Spekificity pattern:
   - Loads context (vault, lat.md index, constitution)
   - Executes workflow with user interaction
   - Persists decisions and progress
   - No misleading "agent started" messages in pure-CLI fallbacks

3. **Documentation Accuracy**: CLAUDE.md updated to reflect:
   - `spek init` as CLI command
   - `/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude` as agent skills
   - Proper invocation notation (slash prefix for agent skills)
   - Context injection mechanism documented

4. **CLI Graceful Degradation**: If users try to run `spek prepare/plan/implement/conclude` from CLI without agent context, provide helpful error with `/spek.*` skill invocation instructions.

## Technical Context

- **Technology Stack**: Python CLI (Click), Claude Code agent skills, SpecKit integration
- **Dependencies**: 
  - `spekificity/cli/main.py` — current CLI implementation
  - `wiki/skills.md` — intended design
  - `CLAUDE.md` — documentation to update
  - `spekificity/core/speckit_wrapper.py` — SpecKit orchestration
  - `.specify/memory/constitution.md` — project principles

- **Existing Artifacts**:
  - Phase 1-5 of 001-complete-framework completed
  - CLI stubs functional but incomplete
  - Wiki documentation complete and accurate
  - Agent skill registration infrastructure in place

## Assumptions

1. Agent skills are the primary invocation path; CLI is fallback for project initialization only
2. `/spek.*` skills will be registered as Claude Code agent skills (not as CLI commands)
3. Context injection (vault + lat.md + constitution) is the responsibility of the agent skill, not the CLI
4. CLAUDE.md will be the authoritative documentation for agent context and invocation

## Out of Scope

- SpecKit internals or dependencies (treat as stable)
- lat.md integration beyond context loading
- Vault schema changes
- Test infrastructure beyond basic agent skill invocation

## Success Metrics

- [ ] CLAUDE.md clearly states which commands are CLI vs agent skills
- [ ] No more misleading "agent session started" messages from pure CLI
- [ ] All four workflow commands (`prepare`, `plan`, `implement`, `conclude`) are documented as agent skills
- [ ] Error message from CLI stubs directs users to `/spek.*` skill invocation
- [ ] Wiki documentation matches implementation approach
