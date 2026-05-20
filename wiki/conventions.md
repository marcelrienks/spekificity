# Naming Conventions: Brief Style Guide

**See also:** [skill-index.md](skill-index.md) (primary command reference), [workflow.md](workflow.md), [architecture.md](architecture.md)

---

## Quick Reference

**Command Prefixes:**
- `spek.*` — Spekificity user-facing commands (prepare, specify, plan, implement, post, lessons)
- `speckit.*` — SpecKit wrapped commands (constitution, specify, clarify, plan, tasks, analyze)
- `context.*` — Context loading and injection (load, inject)
- `cg.*` — CodeGraph queries (query, sync)
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
/spek.automate --phase=specify             # Run spec phase
/spek.implement feature-name --verbose     # Verbose output
/cg.query symbol my_function               # Query code graph
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
├── spek-automate/
├── context-load/
└── cg-query/
```

**Artifact Files:**
- Specs: `wiki/specs/feature-name.md` (kebab-case)
- Plans: `wiki/specs/feature-name-plan.md`
- Lessons: `wiki/vault/lessons/YYYY-MM-DD-feature-name.md`
- Decisions: `wiki/vault/decisions.md` (single file, append-only)
- Patterns: `wiki/vault/patterns.md` (single file)

---

**For full command reference, see:** [skill-index.md](skill-index.md)

**Copilot-instructions.md will document:**

```markdownspek.*` prefix)
Spekificity-owned skills for orchestration, context, and enhancement.
- `/spek.prepare` — Pre-feature setup
- `/spek.post` — Post-feature finalization
- `/spek.context` — Load vault context
- `/spek.map` — Index source code
- `/spek.lessons` — Extract lessons learned
- `/spek.automate` — Full automation workflow

### SpecKit Vanilla (`speckit.*` prefix)
Spec-driven framework commands (unchanged; distinct namespace for clarity).
- `/speckit.specify` — Create spec (vanilla SpecKit)
- `/speckit.plan` — Create plan (vanilla SpecKit)
- `/speckit.implement` — Execute tasks (vanilla SpecKit)

### Spekificity Workflow Commands (`spek.*` prefix)
Spekificity exposes workflow-level commands rather than one wrapper per SpecKit phase.
- `/spek.automate` — Orchestrates specify → clarify → plan → analyze → remediate → tasks
- `/spek.implement` — Runs implementation after workflow artifacts are approved

**User mental model:** 
- Use `/spek.*` commands (enriched, full feature workflow)
- Use `/speckit.*` commands only if vanilla SpecKit workflow needed
- Prefix indicates ownership: `spek` = Spekificity, `speckit` = SpecKit

### Auxiliary (No prefix, system-level
- `/implement-enrich` — Wrap /speckit.implement

### Auxiliary (`/command` or `/command-hyphen`)
Support utilities.
- `/caveman` — Compression mode
- `/read-wiki` — Wiki analysis
- `/simplify-docs` — Docs consolidation
```
spek.context-load` | `spek.context` | Keep prefix; simplify command portion |
| `spek.map-codebase` | `spek.map` | Keep prefix; simplify command portion |
| `spek.lessons-learnt` | `spek.lessons` | Keep prefix; simplify command portion |
| `spek.prepare` | `spek.prepare` | **UNCHANGED** (already simple) |
| `spek.post` | `spek.post` | **UNCHANGED** (already simple) |
| `spek.automate` | `spek.automate` | **UNCHANGED** (already simple) |
| `speckit-enrich-specify` | `spek.automate` | Collapse wrapper into workflow orchestrator |
| `speckit-enrich-plan` | `spek.automate` | Collapse wrapper into workflow orchestrator |
| `speckit-enrich-implement` | `spek.implement` | Keep separate enriched execution command |
| `/speckit.specify` | `/speckit.specify` | **UNCHANGED** (vanilla SpecKit, distinct namespace) |
| `/speckit.plan` | `/speckit.plan` | **UNCHANGED** (vanilla SpecKit, distinct namespace) |
| `/speckit.implement` | `/speckit.implement` | **UNCHANGED** (vanilla SpecKit, distinct namespace) |
| `/speckit.specify` | `/speckit.specify` | **UNCHANGED** (keep namespace for clarity) |
| Keep `spek.*` prefix? | **Yes, always** | Clear namespace ownership; visual grouping in invocation |
| Simplify command portion? | **One word when possible** | Shorter to type; easier to remember |
| Use hyphenation in commands? | **Only if one word insufficient** | Prefer single words (e.g., `context` not `load-context`); hyphens acceptable if needed |
| Namespace prefix for SpecKit skills? | **Yes (`speckit.*`), unchanged** | Intentional distinction; SpecKit-owned tools |
| Namespace prefix for workflow commands? | **Yes (`spek.*`)** | `spek.automate` and `spek.implement` remain distinct from upstream SpecKit commands |
| Should skill directories use prefix? | **Yes (`spek-` prefix in directory name)** | Groups all Spekificity skills together in filesystem; easy to scan |
| Should directory suffix match command? | **Yes, exactly** | Directory `spek-context/` → command `/spek.context` → remove ambiguity
| Question | Decision | Rationale |
|----------|----------|-----------|
| One word or hyphenated? | **One word when possible, hyphenated when needed** | Shorter invocation; user preference |
| Use dot notation? | **No** | User prefers hyphens; dots reserved for namespace distinction (speckit.*) |
| Namespace prefix for spekificity skills? | **No** | Global scope; namespace clarity via documentation |
| Namespace prefix for SpecKit skills? | **Yes (`speckit.*`)** | Intentional distinction; SpecKit-owned tools |
| Namespace prefix for enriched wrappers? | **No, but use `-enrich` suffix** | Suffix signals wrapper; no prefix needed |
| Should skill directories match command names? | **Yes, exactly** | Remove ambiguity; directory reflects invocation |
| Should enriched wrappers be prefixed? | **No; use `-enrich` suffix instead** | Suffix is more meaningful than prefix |

---

## Success Criteria

- [x] User-facing Spekificity workflow commands reduced to `/spek.automate` and `/spek.implement`
- [x] SpecKit vanilla commands use `speckit.*` namespace (unchanged, intentional distinction)
- [x] Spekificity does not mirror every SpecKit phase as separate primary commands
- [x] Directory names match command invocations
- [x] Namespace distinctions documented in copilot-instructions.md
- [x] Migration path clear for current users

---

#spek.prepare               # Pre-feature setup
/spek.context               # Load vault context independently

# Workflow
/spek.automate              # Orchestrate spec -> plan -> analyze -> remediate -> tasks

# Implement
/spek.implement             # Execute implementation after workflow artifacts are approved
```

**Compare to old naming:**
```
/spek.prepare
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
/speckit.tasks
/speckit.implement
```

**Key improvements:**
- All Spekificity commands keep `spek.*` prefix (namespace clarity)
- Command portions simplified: `context-load` → `context`, `lessons-learnt` → `lessons`, `map-codebase` → `map`
- Spekificity exposes workflow-level orchestration instead of phase-by-phase wrappers
- Easier to type and remember while maintaining namespace distinction
```

**New naming is 40% shorter and more memorable.**

---

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
- **Workflow-first experience** — `/spek.automate` owns spec-through-task orchestration; `/spek.implement` stays separate so execution does not happen automatically

Result: Commands are memorable, discoverable, namespace-awarfix immediately communicates "this wraps a SpecKit command"

Result: Commands are memorable, discoverable, and self-documenting.
