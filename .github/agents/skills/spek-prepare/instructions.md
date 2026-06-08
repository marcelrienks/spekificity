# Instructions: /spek.prepare Skill

## Purpose

Prepare a developer for feature work by loading prior architectural decisions, design patterns, lessons learned, and indexing the codebase to provide relevant file locations and context.

## When to Use

- Starting work on a new feature
- Resuming work after context loss
- Need quick overview of relevant decisions and code structure
- Want to avoid re-reading entire codebase

## How It Works

### 1. Check Project State
- Verify Spekificity initialized (`vault/` directory exists)
- Check git working directory (warn if uncommitted changes)

### 2. Load Vault Context
- Read `vault/decisions.md` (prior architectural decisions)
- Read `vault/patterns.md` (reusable design patterns)
- Read `vault/lessons/` (lessons from completed features)
- Filter by feature relevance using keyword matching

### 3. Index Codebase
- Sync lat.md index (if installed)
- Query for relevant files by feature intent
- Query for relevant functions/methods
- Fall back to semantic search if lat.md unavailable

### 4. Generate Navigation Guide
- List relevant code files (by relevance score)
- Show file purposes and modification points
- Estimate token overhead for context loading
- Suggest next steps (usually `spek plan`)

## Output Format

Structured Markdown report with:
- Feature name
- Prior decisions section (bulleted list)
- Patterns section (bulleted list)
- Codebase overview (metrics)
- Navigation guide (prioritized file list)
- Context summary (token/time estimates)
- Next steps

## Common Options

```bash
# Prepare for feature with description
/spek.prepare "Add webhook support for payment notifications"

# Skip indexing (faster if just need vault context)
/spek.prepare "Refactor auth module" --no-index

# Force skip git check (if working directory has staged changes)
/spek.prepare "my feature" --force
```

## Success = You Can...

- [ ] List 2+ prior decisions affecting this feature
- [ ] Identify 2+ relevant design patterns
- [ ] Name 3+ files you'll modify for this feature
- [ ] Understand the context without re-reading codebase docs
- [ ] Proceed to `/spek.plan` with clear context

## If It Fails

| Error | Solution |
|-------|----------|
| "Not in Spekificity project" | Run `spek init` in project root |
| "Not in git repository" | Run `git init` first |
| "Git working directory not clean" | Commit changes or use `--force` |
| "lat.md sync failed" | Continue with semantic search (slower but works) |
| "Vault is empty" | Run `/spek.plan` to generate initial decisions |

## Integration with Workflow

```
spek init
   ↓
/spek.prepare → Load context
   ↓
/spek.plan → Generate spec/plan/tasks
   ↓
/spek.implement --task T1.1 → Execute
   ↓
/spek.conclude → Extract lessons
```

## Next Steps After Prepare

Usually: `/spek.plan "Your feature description"`

This generates formal specification, plan, and task breakdown based on the context you just loaded.
