# Skill: Analyze Outcomes & Extract Lessons

**Invocation**: `/spek.conclude`

## Purpose

Analyze implementation outcomes against success criteria, extract lessons learned, update vault with new patterns and decisions, refresh project state for next feature.

## Usage

```
/spek.conclude [--caveman-mode=full|lite|ultra] [--dry-run]
```

## What It Does

1. **Analysis Phase**: Validate implementation against spec
   - Run `/speckit.analyze` — validate implementation vs spec
   - Compare success criteria vs actual outcomes
   - Identify any spec drift or deviations
   - Flag contradictions or risks
   - Generate analysis report

2. **Lessons Extraction** (Interactive):
   - Prompt for retrospective: What went well?
   - Prompt for retrospective: What to improve?
   - Extract new patterns if workflow diverged from spec
   - Log new decisions if architecture changed
   - Update success criteria if spec changed

3. **Vault Updates**:
   - Archive spec + plan + tasks + execution trace to `vault/archive/{date}-{feature}/`
   - Generate lessons document to `vault/lessons/{date}-{feature}.md`
   - Update `vault/patterns.md` with new patterns (if any)
   - Update `vault/decisions.md` with new decisions (if any)

4. **Repository State Sync**:
   - Sync repo memory (architectural decisions, pattern index) to `.spek/memory/`
   - Refresh lat.md code graph via `/lat.sync` (incremental)
   - Update graph exports + metadata
   - Refresh Obsidian vault graph via CLI (if available)

5. **Completion**:
   - Archive current feature session state
   - Report analysis + lessons + synced artifacts
   - Suggest next feature: `/spek.prepare [next-feature]`

## Workflow Details

### Phase 1: Context Loading
- Load vault (decisions, patterns, lessons)
- Load code index (lat.md)
- Load implementation logs from previous `/spek.implement` runs
- Load constitution (principles)

### Phase 2: Outcomes Analysis
- Run `/speckit.analyze` to validate implementation
- Compare success criteria vs actual outcomes
- Identify spec drift or deviations
- Flag contradictions or risks
- Generate analysis report

### Phase 3: Lessons Extraction (Interactive)
- Prompt user: "What went well?"
- Prompt user: "What to improve?"
- Extract new patterns if workflow diverged
- Log new decisions if architecture changed
- Update success criteria if spec changed

### Phase 4: Vault Updates
- Archive to `vault/archive/{date}-{feature}/`
- Write lessons to `vault/lessons/{date}-{feature}.md`
- Update `vault/patterns.md` with new patterns
- Append to `vault/decisions.md` with new decisions

### Phase 5: Repository Sync
- Sync `.spek/memory/` with latest vault state
- Run `/lat.sync` to refresh code index
- Update graph exports
- Refresh Obsidian vault (if available)

### Phase 6: Completion
- Archive feature session state
- Report summary
- Ready for next feature

## Output

**Artifacts Created**:
- `vault/lessons/{date}-{feature}.md` — Lessons document
- `vault/archive/{date}-{feature}/` — Archived spec/plan/tasks/trace
- Updated `vault/patterns.md` — New patterns (if any)
- Updated `vault/decisions.md` — New decisions (if any)
- Updated `.spek/memory/` — Synced project state

**Console Output**:
- Analysis report (outcomes vs criteria)
- Lessons summary (what went well, improvements)
- Vault update summary
- Sync status (files added/modified/removed)
- Completion report

## Context Requirements

- `vault`: existing decisions, patterns for comparison
- `code-index`: lat.md for final state analysis
- `constitution`: principles for governance context

## Related Skills

- `/spek.prepare` — Load context for next feature (next step)
- `/spek.plan` — Plan next feature (next step)
- `/spek.implement` — Implement next feature (next step)

## Examples

### Example 1: Conclude with Analysis

```
/spek.conclude
```

Output (condensed):
```
## Concluding Feature Implementation

## Outcomes Analysis
- Specification:
  ✓ All success criteria met
  ✓ 2/3 optional features implemented (feature X deferred)
  
- Implementation:
  ✓ Code committed with spec linkage
  ✓ 5 decisions logged
  ✓ Token usage: 45k / 100k budget
  
- Testing:
  ✓ Unit tests for User model
  ✓ Integration tests for login flow
  ⚠ No end-to-end tests (out of scope)

## Lessons Extracted

What went well?
- SQLAlchemy ORM significantly simplified database layer
- Type checking caught 2 bugs before testing
- Reusing bcrypt library saved ~2 hours

What to improve?
- Feature X should have been in MVP (marked for next iteration)
- Consider async password hashing for large user imports
- Add end-to-end tests in future features

## Vault Updates
- New decisions appended: 3
- New patterns extracted: 1
- Lessons written: vault/lessons/2026-06-08-add-auth.md
- Archive created: vault/archive/2026-06-08-add-auth/

## Repository Sync
- Memory synced: .spek/memory/
- Code index refreshed: lat.md
- Obsidian vault: updated (if available)

✓ Feature conclusion complete
  Lessons: vault/lessons/2026-06-08-add-auth.md
  Archive: vault/archive/2026-06-08-add-auth/
  
  Ready for next feature: /spek.prepare [next-feature]
```

### Example 2: Dry-Run (No Changes)

```
/spek.conclude --dry-run
```

Shows what would be updated without persisting changes.

### Example 3: Compressed Output

```
/spek.conclude --caveman-mode=full
```

Output in caveman compression (terse, token-efficient).

## Invocation Variants

### Analysis Only (No Vault Update)

```
/spek.conclude --analysis-only
```

Run analysis and extract lessons without updating vault.

### Dry-Run Mode

```
/spek.conclude --dry-run
```

Show what would be updated without persisting changes.

### Caveman Mode

```
/spek.conclude --caveman-mode=full|lite|ultra
```

Compress output for token efficiency.

## Interactive Elements

- **Retrospective Prompts**: Gather what went well and improvements
- **Pattern Extraction**: Ask if new patterns emerged
- **Decision Logging**: Capture new decisions made during feature
- **Vault Updates**: Confirm before updating vault (unless auto-confirm enabled)

## Optional Features

- **Obsidian CLI Export**: Refresh vault graph (optional; graceful failure if unavailable)
- **Advanced Metrics**: Token usage per task, velocity tracking (optional future enhancement)
- **Pattern Mining**: Automated pattern extraction from code changes (optional future enhancement)

## Implementation Notes

- **Non-Destructive**: Original spec/plan/tasks preserved in archive
- **Incremental Sync**: `/lat.sync` updates code index incrementally (fast)
- **Graceful Degradation**: Works without Obsidian CLI (optional enhancement only)
- **Vault Persistence**: All updates atomic (all succeed or all fail)
- **Knowledge Compounding**: Future `/spek.prepare` runs see all past decisions/patterns

## Documentation

See [wiki/skills.md#spek.conclude](../../wiki/skills.md#spek.conclude) for full specification.
