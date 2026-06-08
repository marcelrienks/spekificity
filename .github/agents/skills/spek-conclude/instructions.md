# Instructions: /spek.conclude Skill

Wrap up feature development by analyzing outcomes and capturing lessons for future work.

## When to Use

- All feature tasks completed
- Implementation complete and tested
- Ready to close feature branch
- Want to document what was learned

## How It Works

1. **Analyze Outcomes** — Compare actual vs planned
2. **Extract Lessons** — What worked, what didn't
3. **Identify Patterns** — New patterns worth reusing
4. **Update Vault** — Add new decisions/patterns
5. **Generate Summary** — Feature completion report

## Workflow

```bash
# Complete all tasks first
/spek.implement --task T5.3 --mark-complete

# Then conclude feature
/spek.conclude --feature oauth2-auth

# Vault is updated with lessons and patterns
```

## Dry Run (Preview)

```bash
/spek.conclude --feature oauth2-auth --dry-run

# Shows what would be updated without writing
```

## Success = You Can...

- [ ] List all lessons learned from this feature
- [ ] Identify 2+ patterns worth reusing
- [ ] See outcomes vs planned success criteria
- [ ] Know what's new in vault for next feature

## Output Files

- `vault/lessons/2026-06-08-oauth2-auth.md` — Timestamped lessons
- Updated `vault/decisions.md` — New/refined decisions
- Updated `vault/patterns.md` — New patterns
- `specs/oauth2-auth/summary.md` — Feature summary

## Next Feature

After concluding:

```bash
/spek.prepare "Your next feature"
# Vault now includes lessons from completed feature
# Will inform decisions for next work
```

## Key Insight

Lessons from this feature benefit future work. By documenting patterns and decisions:
- Next feature builds on what you learned
- Avoid repeating mistakes
- Reuse proven patterns
