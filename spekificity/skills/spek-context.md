---
name: spek-context
description: 'Load vault context and repo memory into the current agent session.'
---

# /spek.context

Load vault context and repo memory into the current agent session.

## Prerequisites

- `.spek/vault/` initialized (`spek init` complete)

## Steps

0. **Pre-check**: Validate vault structure exists. Check `.spek/vault/` directory exists. Check that `decisions.md` and `patterns.md` exist in vault; if missing, create empty stubs with minimal structure (e.g., `## Decisions` header for decisions.md). Check `.spek/memory/` exists; create if missing.
1. Read `.spek/vault/decisions.md` — load project decisions into session.
2. Read `.spek/vault/patterns.md` — load reusable patterns into session.
3. Read all files in `.spek/vault/lessons/` — load prior lessons into session (skip gracefully if lessons/ directory empty or missing).
4. Read `.spek/memory/` — load workspace-scoped facts into session.
5. Session state now populated. All downstream `/spek.*` commands have full context available.

## Output

- Project decisions, patterns, lessons, and workspace facts loaded into agent session

## Vault Schema Reference

### decisions.md Structure

When querying or updating `decisions.md`, follow this schema:

```markdown
## Decision: [Title]
Date: YYYY-MM-DD
Context: [Why this decision was needed; problem statement]
Resolution: [What we decided]
Rationale: [Why this is the right choice; trade-offs]
Alternatives: [What else we could have done and why we didn't]
Impact: [Modules/systems affected; breaking changes?]
Related Decisions: [[link to other decision in vault]]
Tags: [#architecture, #performance, #security, etc.]
```

**Querying**: Skills search for `^## Decision:` headers and extract context/resolution keywords.

### patterns.md Structure

When querying or updating `patterns.md`, follow this schema:

```markdown
## Pattern: [Reusable Pattern Name]
Context: [When/why this pattern applies]
Implementation: [How to use this pattern; pseudo-code or reference]
Trade-offs: [Pros and cons; performance vs readability, etc.]
Example Files: [Link to code that uses this pattern]
Anti-patterns: [What NOT to do; common mistakes]
Tags: [#async, #error-handling, #testing, etc.]
Related Patterns: [[link to other patterns in vault]]
```

**Querying**: Skills search for `^## Pattern:` headers and use tags + keywords for autolink enrichment.

### Autolink Keyword Mapping

Autolink looks for these keywords in lesson files and creates wikilinks:

```yaml
# In .spek/config.yaml (if using autolink):
autolink:
  enabled: true
  keyword_tags:
    "async": "#async"  # lesson mentions "async" → tag #async + link to patterns with #async
    "error-handling": "#error-handling"
    "testing": "#testing"
    "performance": "#performance"
    # custom project keywords:
    "authentication": "#security"
    "database": "#persistence"
```

## Exit Criteria

- Vault decisions and patterns loaded
- Prior lessons loaded from `.spek/vault/lessons/`
- Workspace memory loaded from `.spek/memory/`
- Vault schema understood (decisions + patterns structure)
- Session ready for downstream `/spek.*` commands
