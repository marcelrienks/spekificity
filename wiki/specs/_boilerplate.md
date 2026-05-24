<!-- Shared boilerplate for spec files. Refer to this from individual specs. -->

# Spec Boilerplate


See [Spec Boilerplate](./_boilerplate.md) for shared templates and conventions.
This document contains shared templates and conventions referenced by individual spec files in this directory. Do not edit the per-spec copies of these sections directly; update this file and then propagate changes.


## Frontmatter Schema

Recommended frontmatter fields (if used outside `wiki/specs/`):

- `title`: Human-friendly title
- `status`: active | draft | archived
- `version`: semantic version or date
- `date`: YYYY-MM-DD
- `type`: spec | pattern | skill | guide

Note: Spec files in `wiki/specs/` are maintained without frontmatter by project convention.


## Cross-cutting Error Handling Rules (summary)

- Fail safely, not silently: always log errors and show actionable messages.
- Provide actionable guidance with suggested commands or next steps.
- Retry transient operations with exponential backoff (configurable retries).
- Use graceful degradation: fallbacks to cached or minimal state where possible.

For the full, project-specific error handling details, see the relevant spec(s) (e.g., error-handling-and-recovery.md).


## Logging Structure (recommended)

Log format (markdown summary):

```

## Error: {Category}
**Time:** 2026-05-19 14:32:15 UTC
**Operator:** /spek.prepare
**Severity:** HIGH
**Error Message:** {text}
**Context:** {file paths, git status}
**Action Taken:** {fallback|retry|fail + guidance}
```


## Spec File Template

Recommended section order (non-normative):

1. Title / H1
2. Short summary line
3. `Dependencies` (compact list)
4. `Overview`
5. `Purpose`
6. `Scope & Relationships`
7. `Examples` (or link to `examples/`)
8. `Success Criteria`
9. `References`

Keep specs self-contained and preserve all code examples and operational commands.
