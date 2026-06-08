# Skill: /spek.conclude

Analyze outcomes, extract lessons, update vault with new decisions and patterns.

## Input

```
/spek.conclude --feature FEATURE_NAME [--dry-run] [--export-vault]
```

## Arguments

- `--feature FEATURE_NAME` (required): Feature branch or spec ID (e.g., oauth2-auth)
- `--dry-run`: Show what would be done without writing
- `--export-vault`: Export vault using Obsidian CLI (if installed)

## Output

- Analyzes implementation outcomes vs success criteria
- Extracts 2-5 lessons learned
- Identifies new patterns and refined decisions
- Updates vault with new knowledge
- Generates feature summary
- Returns completion report

## Example

```
/spek.conclude --feature oauth2-auth
```

Returns:

```
❯ Concluding feature oauth2-auth...

## Outcomes Analysis
Spec: OAuth2 Authentication Integration
Status: Complete (all 5 tasks done)

Success Criteria Validation:
- SC-001: Support Google and GitHub providers
  ✓ Both implemented and tested
- SC-002: Sessions persist for 30 days
  ✓ Actual: 30-day sliding expiry works
- SC-003: 2FA optional, admin-configurable
  ✓ Implemented as required

Implementation Summary:
- Actual tokens used: 12000 (estimated: 12500)
- Actual hours spent: 8.5 (estimated: 8)
- All 5 tasks completed on first attempt

## Lessons Extracted
File: vault/lessons/2026-06-08-oauth2-auth.md

### Key Learnings
1. OAuth2 provider pattern is reusable (can apply to other IdPs)
2. Token refresh strategy critical for user experience
3. Admin configuration via environment variables works well

### New Patterns
- pat-oauth2-provider: OAuth2 adapter pattern
- pat-token-refresh: Token refresh strategy

### Refined Decisions
- dec-auth-001: Use environment variables for config (APPROVED)
- dec-auth-002: Make 2FA optional (CONFIRMED)

## Vault Updated
✓ 2 new patterns appended to vault/patterns.md
✓ 1 new decision appended to vault/decisions.md
✓ Lessons file created: vault/lessons/2026-06-08-oauth2-auth.md

✓ Feature conclusion complete
Ready for next feature: /spek.prepare "next feature name"
```

## Preconditions

- Feature must be complete (all tasks marked complete)
- Progress logs must exist in `.specify/logs/`
- Implementation summary available

## Artifacts Produced

- **lessons.md** — Timestamped lesson file in `vault/lessons/`
- **Updated vault/decisions.md** — New decisions appended
- **Updated vault/patterns.md** — New patterns appended
- **summary.md** — Feature completion summary

## Error Cases

- ❌ Feature not found: "Feature oauth2-auth not found in specs/"
- ❌ Tasks not complete: "3 tasks incomplete, complete before concluding"
- ❌ Not in Spekificity project: "Run 'spek init' first"

## Success Criteria

- ✓ Outcomes analyzed vs success criteria
- ✓ 2+ lessons extracted and documented
- ✓ New patterns identified and added to vault
- ✓ Vault updated with new knowledge
- ✓ Feature summary generated
