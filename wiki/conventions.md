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

- **Full words over abbreviations:** Tab-complete discovers faster; still short to type.
- **`speckit.*` namespace distinction:** Intentional vendor separation; prevents confusion about tool ownership.
- **`spek.*` prefix always:** Prevents collisions, groups commands in shell history, reinforces Spekificity ownership.

---

## Implementation Patterns

All commands follow this pattern (full invocation guide in [setup.md](setup.md#command-invocation-style)):

```bash
/spek.commandname [target] [--flags]
```

Standard flags: `--verbose`, `--format [text|json|mermaid]`, `--dry-run`, `--quiet`.

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
- Specs: `specs/NNNN-feature-name.md` (project root; kebab-case; numeric prefix for ordering)
- Plans: `specs/NNNN-feature-name-plan.md` (same directory as spec)
- Lessons: `vault/lessons/YYYY-MM-DD-feature-name.md`
- Decisions: `vault/decision.md` (single file, append-only)
- Patterns: `vault/patterns.md` (single file)

## Implementation choice heuristic

- **Agentic (.md + AGENTS.md):** Fast to start, flexible for iteration, best for personal/small-team vaults (≈<200 docs). Use when discovery and prompt-tuning are frequent.
- **Programmatic (package/pipeline):** Deterministic outputs, typed contracts, content-addressable IDs, CI-friendly, token-efficient at scale. Use when corpus large, reproducibility and audit trails required, or pipeline feeds downstream automation.


**For full command reference, see:** [skills.md](skills.md)

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

See [workflow.md](workflow.md) integration checklist for implementation tasks. Key: update skill names, configs, tests.

---

## Long-Term Benefit

- **Consistent `spek.*` prefix** — All Spekificity commands grouped under `/spek.*` vs `/speckit.*` (SpecKit base).
- **Simplified command portions** — One-word commands (`context`, `map`, `lessons`) easier to type and remember.
- **Namespace ownership visible** — Prefix immediately shows ownership (Spekificity vs SpecKit).
- **Workflow-first experience** — `/spek.plan` orchestrates spec-through-task; `/spek.implement` stays separate.

Result: Commands are memorable, discoverable, and self-documenting.
