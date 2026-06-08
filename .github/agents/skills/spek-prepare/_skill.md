# Skill: /spek.prepare

Load prior context, index codebase, generate navigation guide for feature development.

## Input

```
/spek.prepare [FEATURE_NAME]
```

## Arguments

- `FEATURE_NAME` (optional): Feature name or description (3-100 chars)

## Output

Structured onboarding report including:
- Prior decisions from vault (2-5 items)
- Design patterns (2-5 items)
- Codebase overview (file count, key directories)
- Navigation guide (relevant files by intent)
- Context summary (decisions, patterns, token estimate)
- Next steps

## Example

```
/spek.prepare "Add OAuth2 authentication"
```

Returns:

```
❯ Preparing feature context...
  Feature: Add OAuth2 authentication

## Prior Decisions
- Use external auth providers for delegation
- Store credentials securely via env vars

## Relevant Patterns
- Provider adapter pattern for OAuth2
- Token refresh strategy

## Codebase Overview
- Total files: 847
- Key directories: auth/, api/, tests/

## Navigation Guide
To implement OAuth2:
1. auth/providers/oauth2.py (implement OAuth2Provider)
2. api/routes/auth.py (add /login endpoint)
3. tests/test_oauth2.py (add tests)

## Context Summary
- Decisions loaded: 3
- Patterns loaded: 5
- Files indexed: 847
- Estimated tokens: ~8000
- Estimated prep time: 18s

Ready to plan. Next: /spek.plan
```

## Preconditions

- Must be in a Spekificity-initialized project (`spek init` run)
- Git working directory should be clean (use `--force` to skip check)

## Error Cases

- ❌ Not in Spekificity project: "Run 'spek init' first"
- ❌ Git not initialized: "Not in a git repository"
- ⚠️ lat.md unavailable: Falls back to semantic search (slower)

## Success Criteria

- Completes in <30 seconds
- Returns valid Markdown report
- Loads ≥2 decisions and ≥2 patterns from vault
- Identifies ≥1 relevant code file
