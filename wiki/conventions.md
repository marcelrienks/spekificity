# Naming Conventions: Brief Style Guide

## Quick Reference

## Runtime Model

- `spek` CLI is primarily for installation/bootstrap (`spek init`) and diagnostics.
- `spek init` scaffolds `.spek/` skills/functions in a target directory.
- Generated `/spek.*` skills are the primary runtime interface for agents.
- Underlying tools (`specify`, `obsidian` CLI, `lat.md`, caveman) remain directly usable.

**Command Prefixes:**
- `spek` — setup/bootstrap CLI (`init` + diagnostics)
- `/spek.*` — generated skill commands under `.spek/` (agent execution surface)
- `speckit.*` — SpecKit wrapped commands (constitution, specify, clarify, plan, tasks, analyze)
- `context.*` — Context loading and injection (load, inject)
 - `lat.*` — Indexing queries (lat.md: query, sync)
- `caveman.*` — Compression mode (caveman, review)

**Style:**
- Single words where possible (`prepare` not `prep`, `context` not `ctx`)
- No hyphens in command names (ergonomic to type)
- Prefix is intentional; provides grouping and namespace clarity
- All commands are action-oriented (verbs)

---

## Core Naming Principles

1. **Namespace Clarity:** Prefix always present; `spek.*` = Spekificity, `speckit.*` = SpecKit, `context.*` = memory
2. **Simplicity:** Single-word command portions where possible (short, memorable, easy to type)
3. **Consistency:** All workflow commands use same pattern; easy to discover and learn
4. **Modularity:** Each command accepts same flags (`--verbose`, `--format`, `--dry-run`, `--quiet`)

---

## Naming Rationale

### Why `/spek.prepare` instead of `/spek.pre`?

- Full words are more discoverable (`/spek.` + tab-complete shows full meaning)
- Single word is still short enough to type comfortably
- Imperative verb (action) is clearer than abbreviation

### Why `speckit.*` instead of aliasing to `spek.*`?

- Namespace distinction is intentional; shows vendor separation
- No confusion about which tool owns a command
- Users understand SpecKit is underneath but separate
- Supports independent tool upgrades

### Why keep `spek.*` prefix for all Spekificity commands?

- Visual/organizational grouping in shell history and documentation
- Prevents collision with other tools (`context` alone would conflict)
- Reinforces that these are Spekificity-specific workflows

---

## Implementation Patterns

All commands follow:

```bash
# Invocation style
/spek.commandname [target] [--flags]

# Examples
/spek.prepare                              # Prepare for feature
/spek.plan --phase=specify             # Run spec phase
/spek.implement feature-name --verbose     # Verbose output
/lat.query symbol my_function               # Query index (lat.md)
```

**Flags Pattern:**
- `--verbose`: Expand explanations
- `--format [text|json|mermaid]`: Output format
- `--dry-run`: Show without making changes
- `--quiet`: Suppress non-essential output

---

## File & Directory Naming

**Skills Directory:**  
```
.github/agents/skills/
├── spek-prepare/       # Directory name matches command
├── spek-plan/
├── context-load/
└── lat-query/
```

**Artifact Files:**
- Specs: `wiki/specs/feature-name.md` (kebab-case)
- Plans: `wiki/specs/feature-name-plan.md`
- Lessons: `vault/lessons/YYYY-MM-DD-feature-name.md`
- Decisions: `vault/decision.md` (single file, append-only)
- Patterns: `vault/patterns.md` (single file)

## Markdown structural hygiene (required)

Generated Markdown must be structurally sound. Structural noise (duplicate H1s, broken YAML frontmatter, malformed tables, inconsistent heading nesting) corrupts downstream automation (chunking, dedupe, indexing). Follow these rules:

- No duplicate H1s in same file; headings must nest correctly.
- YAML frontmatter must be valid YAML; quote values containing colons or special characters.
- Tables must parse; ensure header and delimiter lines are present.
- Use section-aware chunking: chunk boundaries must not split inside a heading.
- Lint every generated page before merge; reject or flag pages that fail strict structural checks.
- Safe merging: dedupe headings (e.g., `dedupe_headings=True`) and prefer canonical slugs or content-addressable IDs when available.

Recommended tooling and checks:

- Use `markdown-hero` (or equivalent) for type-checked sections, section-aware chunking, canonicalization, and safe merges.
- Add pre-commit hooks for structural linting (YAML validation, markdownlint, custom section checks).
- Route structural failures to a repair agent or human review; do not auto-merge uncertain fixes.

## Implementation choice heuristic

- **Agentic (.md + AGENTS.md):** Fast to start, flexible for iteration, best for personal/small-team vaults (≈<200 docs). Use when discovery and prompt-tuning are frequent.
- **Programmatic (package/pipeline):** Deterministic outputs, typed contracts, content-addressable IDs, CI-friendly, token-efficient at scale. Use when corpus large, reproducibility and audit trails required, or pipeline feeds downstream automation.

## Pre-merge checklist (recommended)

- Git versioning enabled; require review before merging agent writes to `vault/`.
- Run structural lint (markdown-hero / yaml-lint / markdownlint) and frontmatter validation.
- Small-batch ingest tests (5–10 documents) before large runs.
- Ensure plan-before-execute gating is present in agent workflows.
- Store generated HTML artifacts under `wiki/artifacts/html/` and do not make them primary wiki pages.
- Require export-to-markdown or short canonical markdown summary for any HTML artifact that must be audited or edited; include this in PRs.
- Add CI rule to flag large HTML files and ensure export present; block merges when missing.

---

**For full command reference, see:** [skill-index.md](skill-index.md)

## Command Naming Decisions

| Old Name | New Name | Rationale |
|----------|----------|-----------|
| `spek.context-load` | `/spek.context` | Keep prefix; simplify command portion |
| `spek.map-codebase` | `/spek.map` | Keep prefix; simplify command portion |
| `spek.lessons-learnt` | `/spek.lessons` | Keep prefix; simplify command portion |
| `spek.prepare` | `/spek.prepare` | UNCHANGED (already simple) |
| `spek.plan` | `/spek.plan` | UNCHANGED (already simple) |
| `speckit-enrich-specify` | Via `/spek.plan` | Collapse into workflow orchestrator |
| `speckit-enrich-plan` | Via `/spek.plan` | Collapse into workflow orchestrator |
| `/speckit.specify` | `/speckit.specify` | UNCHANGED (vanilla SpecKit namespace) |
| `/speckit.plan` | `/speckit.plan` | UNCHANGED (vanilla SpecKit namespace) |
| `/speckit.implement` | `/speckit.implement` | UNCHANGED (vanilla SpecKit namespace) |

## Design Principles

| Question | Decision | Rationale |
|----------|----------|-----------|
| Keep `spek.*` prefix? | **Yes, always** | Clear namespace ownership; visual grouping |
| Simplify command portion? | **One word when possible** | Shorter to type; easier to remember |
| Use hyphenation in commands? | **Only if necessary** | Prefer single words (e.g., `context` not `load-context`) |
| Namespace for SpecKit skills? | **Yes (`speckit.*`)** | Intentional distinction; SpecKit-owned tools |
| Skill directories prefix? | **Yes (`spek-` prefix)** | Groups Spekificity skills together; easy to scan |
| Directory suffix match command? | **Yes, exactly** | Directory `spek-context/` → command `/spek.context` |

## User Mental Model

- Use `/spek.*` commands for full enriched workflow
- Use `/speckit.*` commands only for vanilla SpecKit workflow (when enrichment not needed)
- Prefix indicates ownership: `spek.*` = Spekificity, `speckit.*` = SpecKit, `context.*` = memory, `lat.*` = code analysis

## Success Criteria

- [x] User-facing Spekificity workflow commands streamlined (`/spek.prepare`, `/spek.plan`, `/spek.implement`, `/spek.conclude`)
- [x] SpecKit vanilla commands use `speckit.*` namespace (unchanged, intentional distinction)
- [x] Spekificity exposes workflow-level orchestration, not phase-by-phase wrappers
- [x] Directory names match command invocations exactly
- [x] Namespace distinctions clear and documented
- [x] Migration path clear for current users

---

## CLI Return-Code Policy (summary)

To make automation and CI predictable, Spekificity commands follow a small, standardized exit-code policy. The full policy is documented in `wiki/specs/153-cli-return-code-policy.md`.

- `0`: Success — all requested work completed with no errors.
- `1`: Partial success — non-fatal errors occurred (e.g., some tasks failed but workflow continued); artifacts may be produced.
- `2`: Missing artifact / precondition failure (e.g., `plan.json` missing); no destructive changes applied.
- `3`: Usage / invalid arguments.
- `4`: Unhandled runtime error (internal exception).
- `5`: Configuration or environment error (missing dependencies, adapter unavailable).

Tools and CI should interpret non-zero codes per this mapping; CLI callers may also request a machine-readable JSON outcome via `--output-file` which includes `exit_code`, `errors[]`, and `artifacts[]`.

## Implementation Checklist

- [ ] Update all skill command names in `.github/agents/skills/` directories
- [ ] Update all SKILL.md files with new command names
- [ ] Update copilot-instructions.md with namespace distinctions + new naming
- [ ] Update README.md "Entry Points" section with new commands
- [ ] Update all wiki skill definitions with new command names
- [ ] Update all todo.md references to old command names
- [ ] Broadcast migration guide to users
- [ ] Update .specify integration config if applicable
- [ ] Test that all commands are discoverable and invocable

---

## Long-Term Benefit
Consistent `spek.*` prefix** — All Spekificity commands start with `/spek.` (vs `/speckit.*` for SpecKit base)
- **Simplified command portions** — One-word commands easier to type and remember (`context`, `map`, `lessons`, `prepare`, `post`, `automate`)
- **Namespace ownership visible** — Prefix immediately communicates who owns the command (Spekificity vs SpecKit)
- **Filesystem organization** — Directory structure `spek-context/`, `spek-map/`, `spek-lessons/` groups all Spekificity skills together and clearly shows which commands exist
- **Workflow-first experience** — `/spek.plan` owns spec-through-task orchestration; `/spek.implement` stays separate so execution does not happen automatically

Result: Commands are memorable, discoverable, namespace-awarfix immediately communicates "this wraps a SpecKit command"

Result: Commands are memorable, discoverable, and self-documenting.
