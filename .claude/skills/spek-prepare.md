# Skill: Prepare for Feature Development

**Invocation**: `/spek.prepare`

## Purpose

Load prior context (decisions, patterns, lessons), index codebase, and present onboarding summary to prepare developer for feature work.

## Usage

```
/spek.prepare [feature-name]
```

## What It Does

1. **Load vault context**
   - Read vault/decisions.md for prior architectural decisions
   - Read vault/patterns.md for design patterns used in project
   - Read vault/lessons/ for lessons learned from past features

2. **Load code index**
   - Query lat.md code graph for files relevant to feature
   - Use BM25 semantic search if lat.md unavailable
   - Return top 5 relevant files with line numbers

3. **Load constitution**
   - Read .specify/memory/constitution.md for project principles
   - Extract governance constraints applicable to feature

4. **Format context**
   - Present prior decisions as Markdown list with titles and rationales
   - Show relevant patterns with usage examples
   - List relevant code files with paths and purpose
   - Include constitution principles as highlights

5. **Display onboarding**
   - Prior decisions (first 3 most relevant)
   - Relevant patterns (first 3 most relevant)
   - Relevant code files (first 3 most relevant)
   - Context summary with token estimate
   - Suggest next step: `/spek.plan`

## Workflow Details

### Phase 1: Context Loading
- Load vault (decisions, patterns, lessons)
- Load code index (lat.md)
- Load constitution (principles)
- Format context for agent

### Phase 2: Context Filtering
- Filter decisions by relevance to feature intent
- Filter patterns by relevance to feature domain
- Filter code files by semantic relevance

### Phase 3: Context Formatting
- Format decisions as Markdown list
- Format patterns with examples
- Format code files with line ranges
- Include constitution highlights

### Phase 4: Display
- Show formatted context to developer
- Estimate token usage
- Suggest next workflow step

## Output

**Console Display**:
- Feature name
- Prior decisions (up to 3, sorted by relevance)
- Relevant patterns (up to 3, sorted by relevance)
- Relevant code files (up to 3, sorted by relevance)
- Context summary (decisions loaded, patterns loaded, token estimate)
- Next step suggestion

**No artifacts created** (preparation phase only)

## Context Requirements

- `vault`: decisions, patterns, lessons (required for context)
- `code-index`: lat.md graph (optional; graceful degradation to semantic search)
- `constitution`: project principles (required for governance context)

## Related Skills

- `/spek.plan` — Generate spec, plan, and tasks (next step)
- `/spek.implement` — Execute tasks with context injection
- `/spek.conclude` — Analyze outcomes and extract lessons

## Examples

### Example 1: Basic Usage

```
/spek.prepare "Add user authentication"
```

Output:
```
## Spekificity Feature Preparation

Feature: Add user authentication

## Prior Decisions
- Use Python for CLI implementation (Tags: architecture, cli)
- Vault stores architectural decisions (Tags: architecture, vault)

## Relevant Patterns
- Context Injection Pattern (usage: 5 examples in codebase)
- Decorator Pattern (usage: 3 examples in codebase)

## Relevant Code Files
- spekificity/cli/main.py — CLI router and command entry points
- spekificity/core/vault.py — Vault context loading and persistence
- spekificity/core/context.py — Context formatting utilities

## Context Summary
- Decisions loaded: 2
- Patterns loaded: 2
- Relevant files: 3
- Estimated context tokens: ~5000-10000

Ready to plan or implement. Next: /spek.plan
```

### Example 2: With Compressed Output

```
/spek.prepare "Add user auth" --caveman-mode=full
```

Output:
```
Feature: Add user auth

Prior Decisions:
- Python CLI (Click) — lightweight, maint'd
- Vault stores decisions — avoid repeating design trade-offs

Patterns:
- Context Injection: load vault before agent workflow
- Decorator: wrap SpecKit, don't rebuild

Code Files:
- cli/main.py: CLI router
- core/vault.py: Context loading
- core/context.py: Context formatting

Summary: 2 decisions, 2 patterns, 3 files, ~5k tokens

Next: /spek.plan
```

## Invocation Variants

### With Options

```
/spek.prepare "Feature name" --compressed --no-index
```

Options (if supported):
- `--compressed`: Compress output (caveman mode)
- `--no-index`: Skip code indexing (faster, less context)

### Chaining

```
/spek.prepare "Feature" → /spek.plan → /spek.implement → /spek.conclude
```

All skills can be chained sequentially to execute full feature workflow.

## Implementation Notes

- **Graceful Degradation**: If lat.md unavailable, use semantic search fallback
- **Token Efficiency**: Use vault context and code index to minimize context size
- **Relevance Filtering**: BM25 search to find most relevant context by feature intent
- **No Breaking Changes**: Existing vault, context, compression infrastructure unchanged

## Documentation

See [wiki/skills.md#spek.prepare](../../wiki/skills.md#spek.prepare) for full specification.
