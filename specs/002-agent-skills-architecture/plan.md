# Implementation Plan: Agent Skills Architecture Fix

**Branch**: `main` | **Date**: 2026-06-08 | **Spec**: [specs/002-agent-skills-architecture/spec.md](spec.md)

**Input**: Feature specification from `/specs/002-agent-skills-architecture/spec.md`

## Summary

Fix architectural mismatch between intended agent skills and current CLI implementation. The four workflow commands (`prepare`, `plan`, `implement`, `conclude`) are documented as interactive agent workflows in wiki/skills.md but currently implemented as incomplete CLI stubs in spekificity/cli/main.py. This feature realigns implementation to design by removing misleading CLI commands and establishing proper agent skill registration and context injection.

## Technical Context

**Language/Version**: Python 3.11+ (existing)

**Primary Dependencies**: 
- Click (CLI framework) — for `spek init` only
- Claude Code agent skills framework — for `/spek.*` workflow commands
- SpecKit v0.9.6+ (existing)
- lat.md integration (existing)

**Storage**: File-based vault at `vault/` (existing)

**Testing**: pytest, agent skill invocation tests

**Target Platform**: Linux/macOS development environment

**Project Type**: CLI tool + agent skills framework

**Performance Goals**: Skill invocation < 2s context load time

**Constraints**: 
- Agent skills must follow Spekificity decoration pattern
- Context injection via vault + lat.md + constitution
- No breaking changes to existing 001-complete-framework outputs
- CLAUDE.md must remain source of truth for agent context

**Scale/Scope**: 4 agent skills, 1 CLI command, 1 documentation update

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I (Deterministic Workflows)**: ✓ PASS
- Fixing architectural misalignment improves workflow determinism by removing CLI stubs that cannot deliver promised interactive workflows

**Principle II (Persistent Knowledge)**: ✓ PASS  
- Agent skills will persist context through vault loading and decision logging (no change to vault schema)

**Principle III (Spec-First Quality)**: ✓ PASS
- This feature itself follows spec-first approach; implementation will be preceded by design artifacts (research.md, data-model.md, contracts, quickstart.md)

**Principle IV (Context Efficiency)**: ✓ PASS
- Agent skills delegate context loading to existing modules (vault, lat.md, constitution); no new indexing required

**Principle V (Simple, Composable Tooling)**: ✓ PASS  
- Removing misleading CLI stubs and establishing agent skill registration maintains modularity; agent skills follow decorator pattern

**Dual-Instance Clarity**: ✓ PASS
- This feature is development-instance work (building Spekificity itself); it updates the toolkit's skill registration, not product templates

## Project Structure

### Documentation (this feature)

```text
specs/002-agent-skills-architecture/
├── plan.md              # This file (speckit.plan output)
├── research.md          # Phase 0: Design decisions for agent skill architecture
├── data-model.md        # Phase 1: Agent skill contracts and context flow
├── quickstart.md        # Phase 1: Validation scenarios for agent skill invocation
├── contracts/           # Phase 1: CLI command contracts, agent skill registration
│   ├── cli-contracts.md     # CLI command interface (init only)
│   ├── agent-skills.md      # Agent skill registration format + context injection
│   └── context-flow.md      # Context flow from vault → agent → CLI
└── tasks.md             # Phase 2: speckit-tasks output (not created by speckit-plan)
```

### Source Code (repository root)

```text
spekificity/
├── cli/
│   ├── main.py          # MODIFY: `spek init` remains; graceful degradation for prepare/plan/implement/conclude
│   ├── init.py          # UNCHANGED
│   └── logging_config.py # UNCHANGED
├── core/
│   ├── vault.py         # UNCHANGED (context loading)
│   ├── context.py       # UNCHANGED (context formatting)
│   ├── speckit_wrapper.py # UNCHANGED (SpecKit orchestration)
│   ├── compression.py   # UNCHANGED (caveman mode)
│   └── progress.py      # UNCHANGED (progress tracking)
└── integrations/
    ├── lat_md.py        # UNCHANGED (code indexing)
    ├── speckit.py       # UNCHANGED (SpecKit integration)
    └── semantic_search.py # UNCHANGED

.claude/
├── skills/
│   ├── spek-prepare.md    # NEW: Agent skill definition
│   ├── spek-plan.md       # NEW: Agent skill definition
│   ├── spek-implement.md  # NEW: Agent skill definition
│   └── spek-conclude.md   # NEW: Agent skill definition
└── config/
    └── agent-context.md   # UPDATED: Link to plan.md and skill definitions

CLAUDE.md                 # UPDATED: Reflect agent skills, not CLI commands
```

**Structure Decision**: Single-project Python CLI with agent skill registration. CLI remains minimal (init only); all workflow commands are agent skills. Agent skill definitions stored in `.claude/skills/` following Claude Code conventions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
