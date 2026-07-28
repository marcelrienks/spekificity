---
name: spek-map
description: 'Query lat.md and vault to map code dependencies for a spec topic.'
---

# /spek.map

Query lat.md and vault to map code dependencies for a spec topic.

## When to Call This Skill

**Use `/spek.map` to understand existing code dependencies BEFORE writing spec or plan**:
- Call after `/spek.prepare` but before `/spek.plan` if feature touches complex codebase
- Recommended for features with architectural changes, cross-subsystem refactoring, or unclear ownership
- Output serves as reference during `/spek.plan` to inform design decisions
- Also useful mid-feature to identify blockers that must be resolved first

**Skip this skill if**:
- Feature is isolated and doesn't affect existing code (new module, new CLI command)
- You've already mapped dependencies manually or have institutional knowledge

## Prerequisites

- `/spek.prepare` completed (lat.md indexes current, vault context loaded)
- Topic or feature area to map provided
- Recommended: Run before `/spek.plan` starts (not after)

## Steps

0. **Validation**: Require explicit topic parameter. If topic not provided, halt with error and prompt user to provide feature area or topic name. Validate lat.md code index exists in `.spek/lat.md/code/` before querying. Pre-check: load vault decisions to flag any blockers already documented.
1. Query lat.md MCP for code references to the spec topic: symbols, callers, definitions, and call graphs.
2. Query `.spek/vault/` for related decisions and dependent specs that touch the same topic. Also check if any prior patterns apply to this topic.
3. Generate dependency graph: list files, symbols, specs, and patterns related to the topic.
4. Highlight blockers (items that must change before this topic can be modified, including decisions that constrain design choices) and critical paths.
5. Document findings in `.spek/memory/map-[topic].md` for reference during spek-plan (so spec/plan author has dependency context).

## Output

- Dependency graph: files, symbols, specs, and patterns related to the topic
- Blockers list: items that must change first (including architectural constraints from decisions)
- Critical paths: sequence of changes required
- Findings documented in `.spek/memory/map-[topic].md` for spec/plan author reference

## Exit Criteria

- lat.md queried for all references to the topic
- Vault (decisions, prior specs) queried for related decisions and blockers
- Patterns queried to identify reusable solutions
- Dependency graph generated with blockers, critical paths, and pattern recommendations identified
- Map findings documented for spec/plan author
