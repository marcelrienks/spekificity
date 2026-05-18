# B.7: Naming Conventions for Skills and Workflows

## Status: RESOLVED (2026-05-18, Corrected Intent)

## Design Principle

**Keep `spek.*` prefix always. Simplify command portion to one-word wherever possible.**

This ensures:
- Namespace is always clear: `spek.*` = Spekificity, `speckit.*` = SpecKit
- Command portions are short and memorable (`prepare`, `post`, `context`, `map`, `lessons`)
- Invocation is easy to type and remember
- Prefix provides consistent visual/organizational grouping

---

## Naming Convention by Category

### 1. Spekificity Core Skills (`spek.*` prefix)

**Format:** `/spek.oneword` or `/spek.hyphenated` (only when one word insufficient)  
**Prefix:** `spek.` (always)  
**Pattern:** Action-noun or noun

| Skill | Command | Purpose |
|-------|---------|---------|
| Context loading | `/spek.context` | Load vault (decisions, patterns, lessons) |
| Code mapping | `/spek.map` | Index source code into graph |
| Preparation | `/spek.prepare` | Pre-feature setup (caveman, git, vault, graph) |
| Post-processing | `/spek.post` | Post-feature finalization (lessons, vault, graph, docs) |
| Lessons capture | `/spek.lessons` | Extract structured lessons from feature |
| Full automation | `/spek.automate` | End-to-end workflow (spec → implement → post) |

**Rationale:**
- All commands keep `spek.` prefix for namespace consistency
- Command portions simplified: single words where possible (`context`, `map`, `lessons`, `prepare`, `post`, `automate`)
- Hyphenation avoided; if compound needed, use single word or acceptable hyphen (e.g., `/spek.load-context` would only if `context` alone insufficient, but `context` is clear)

---

### 2. SpecKit Integration (Keep Vanilla Namespace)

**Format:** `speckit.*` (unchanged; distinct namespace)  
**Pattern:** `speckit.command`

| Skill | Command | Purpose | Wrapper Available |
|-------|---------|---------|-------------------|
| Constitution | `/speckit.constitution` | Define project principles | No |
| Specification | `/speckit.specify` | Create feature spec | `/specify-enrich` |
| Clarification | `/speckit.clarify` | Resolve spec ambiguities | No |
| Planning | `/speckit.plan` | Create implementation plan | `/plan-enrich` |
| Task generation | `/speckit.tasks` | Generate task list | No |
| Analysis | `/speckit.analyze` | Cross-artifact consistency check | No |
| Implementation | `/speckit.implement` | Execute tasks | `/implement-enrich` |
| Task-to-issues | `/speckit.taskstoissues` | Convert tasks to GitHub issues | No |

**Rationale:**
- Vanilla SpecKit commands use `speckit.*` namespace for clarity (SpecKit-owned tools, not Spekificity)
- Distinction is intentional and visible in command name
- No aliasing needed; namespace distinction is primary signal

---

### 3. Enriched Wrappers (`spek.*` prefix with enrich)

**Format:** `/spek.enrich.verb` or `/spek.verb` (unified with core if not ambiguous)  
**Prefix:** `spek.` (consistent)  
**Pattern:** `spek.verb` (same as core, or `spek.enrich.verb` if distinction needed)

| Skill | Command | Wraps | Purpose |
|-------|---------|-------|---------|
| Enrich spec | `/spek.specify` | `/speckit.specify` | Inject context (related symbols, prior decisions) |
| Enrich plan | `/spek.plan` | `/speckit.plan` | Inject impact analysis + patterns |
| Enrich implement | `/spek.implement` | `/speckit.implement` | Execute with code map + context |

**Rationale:**
- Keep `spek.` prefix for namespace consistency
- Use same command names as SpecKit base (`specify`, `plan`, `implement`) to reduce cognitive load
- Users invoke either `/spek.specify` (enriched) or `/speckit.specify` (vanilla) based on context/docs
- Clear that `spek.` version is Spekificity-enhanced version of SpecKit base
- Avoids command proliferation; same verb, different prefix = different implementation

---

### 4. Auxiliary Commands (Agent-Level, No Prefix)

**Format:** One-word command (no prefix needed; system-level utilities)  
**Pattern:** Domain-specific actions

| Skill | Command | Purpose |
|-------|---------|---------|
| Token compression | `/caveman` | Activate compression mode (lite/full/ultra) |
| Wiki reading | `/read-wiki` | Analyze wiki + persist context |
| Wiki simplification | `/simplify-docs` | Consolidate + audit documentation |
| Code review | `/review` | Review PR or code diff (caveman compressed) |

**Rationale:**
- Auxiliary commands are system-level utilities, not part of feature workflow
- No prefix needed; invocation simplicity prioritized
- Can optionally use prefix if confusion arises (e.g., `/spek.caveman`), but unprefixed is simpler

---

## Invocation Quick Reference

### Before Feature Start
`spek.prepare         # Git state, caveman, vault, graph
/spek.context         # Load vault independently
```

### During Feature (Core Workflow)
```
/spek.specify         # Enrich + execute /speckit.specify
/spek.plan            # Enrich + execute /speckit.plan
/speckit.tasks        # Vanilla task generation
/speckit.analyze      # Vanilla cross-artifact check
/spek.implement       # Enrich + execute /speckit.implement
```

### After Feature Complete
```
/spek.post            # Lessons, vault update, graph refresh, docs simplify
/spek.lessons         # Manual lessons capture
/simplify-docs        # Manual docs consolidation
```

### Utilities
```
/caveman              # Compression control
/read-wiki            # Wiki analysis + caching
/spek.map             # Manual code graph refresh
/spek.automate        # Full workflow: /spek.prepare → /spek.specify → /spek.plan → /speckit.tasks → /spek.implement → /spek.
/automate             # Full workflow: /prepare → specify → plan → tasks → implement → post
```

---

## Implementation Details

### Directory Structure for Skills
Directory name matches command suffix (prefix `spek-` for Spekificity skills to group them)

```
.github/agents/skills/
├── spek-prepare/
│   └── SKILL.md
├── spek-post/
│   └── SKILL.md
├── spek-context/
│   └── SKILL.md
├── spek-map/
│   └── SKILL.md
├── spek-lessons/
│   └── SKILL.md
├── spek-specify/
│   └── SKILL.md
├── spek-plan/
│   └── SKILL.md
├── spek-implement/
│   └── SKILL.md
├── spek-automate/
│   └── SKILL.md
└── [speckit skills managed by SpecKit, not in this structure]
```

**Rationale:** 
- Directory prefix `spek-` groups all Spekificity skills together in file system
- Suffix matches command portion (e.g., `spek-context/` → `/spek.context`)
- Easy to scan filesystem and see all Spekificity skills at a glance
**Rationale:** Skill directory name matches command name exactly; removes ambiguity.

---

### Namespace Distinctions (in Documentation)

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

### SpecKit Enriched (`spek.*` prefix, same names)
Spekificity wrappers around SpecKit commands with graph context injection.
Invoked by users in place of vanilla SpecKit commands when Spekificity workflow active.
- `/spek.specify` — Enhanced /speckit.specify (context injection)
- `/spek.plan` — Enhanced /speckit.plan (pattern injection)
- `/spek.implement` — Enhanced /speckit.implement (code map injection)

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
| `speckit-enrich-specify` | `spek.specify` | Add prefix; simplify (enrich is implicit in `spek.` vs `speckit.`) |
| `speckit-enrich-plan` | `spek.plan` | Add prefix; simplify (enrich is implicit in `spek.` vs `speckit.`) |
| `speckit-enrich-implement` | `spek.implement` | Add prefix; simplify (enrich is implicit in `spek.` vs `speckit.`) |
| `/speckit.specify` | `/speckit.specify` | **UNCHANGED** (vanilla SpecKit, distinct namespace) |
| `/speckit.plan` | `/speckit.plan` | **UNCHANGED** (vanilla SpecKit, distinct namespace) |
| `/speckit.implement` | `/speckit.implement` | **UNCHANGED** (vanilla SpecKit, distinct namespacerb-first |
| `/spek.map-codebase` | `/map-code` | Drop `spek.` prefix; shorten noun |
| `/spek.lessons-learnt` | `/lessons` | Drop `spek.` prefix; shorten to noun |
| `/spek.automate` | `/automate` | Drop `spek.` prefix |
| `/speckit-enrich-specify` | `/specify-enrich` | Reverse to `command-enrich` pattern |
| `/speckit-enrich-plan` | `/plan-enrich` | Reverse to `command-enrich` pattern |
| `/speckit-enrich-implement` | `/implement-enrich` | Reverse to `command-enrich` pattern |
| `/speckit.specify` | `/speckit.specify` | **UNCHANGED** (keep namespace for clarity) |
| Keep `spek.*` prefix? | **Yes, always** | Clear namespace ownership; visual grouping in invocation |
| Simplify command portion? | **One word when possible** | Shorter to type; easier to remember |
| Use hyphenation in commands? | **Only if one word insufficient** | Prefer single words (e.g., `context` not `load-context`); hyphens acceptable if needed |
| Namespace prefix for SpecKit skills? | **Yes (`speckit.*`), unchanged** | Intentional distinction; SpecKit-owned tools |
| Namespace prefix for enriched wrappers? | **Yes (`spek.*`), same names as base** | Prefix signals "enriched Spekificity version"; same verb reduces cognitive load |
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

- [x] All spekificity core commands are one-word or hyphenated (no dots)
- [x] SpecKit vanilla commands use `speckit.*` namespace (unchanged, intentional distinction)
- [x] Enriched wrappers use `-enrich` suffix (signals wrapper pattern)
- [x] Directory names match command invocations
- [x] Namespace distinctions documented in copilot-instructions.md
- [x] Migration path clear for current users

---

#spek.prepare               # Pre-feature setup
/spek.context               # Load vault context independently

# Feature spec + planning
/spek.specify               # Enrich + execute spec (wraps /speckit.specify)
/spek.plan                  # Enrich + execute plan (wraps /speckit.plan)
/speckit.tasks              # Vanilla task generation (optional, if not using /spek.implement)
/speckit.analyze            # Vanilla cross-artifact check (optional, if needed)

# Implement
/spek.implement             # Enrich + execute implementation (wraps /speckit.implement)

# Finalization
/spek.post                  # Lessons, vault update, graph refresh, docs simplify
/spek.lessons               # Manual lessons capture (if needed)
```

**Compare to old naming:**
```
/spek.prepare
/spek.context-load
/speckit-enrich-specify
/speckit-enrich-plan
/speckit.tasks
/speckit.analyze
/speckit-enrich-implement
/spek.post
/spek.lessons-learnt
```

**Key improvements:**
- All Spekificity commands keep `spek.*` prefix (namespace clarity)
- Command portions simplified: `context-load` → `context`, `lessons-learnt` → `lessons`, `map-codebase` → `map`
- Enriched commands use same names as SpecKit base (`specify`, `plan`, `implement`) — prefix difference signals enriched version
- Easier to type and remember while maintaining namespace distinction
/speckit-enrich-implement
/spek.post
/spek.lessons-learnt
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
- **Unified enriched experience** — `/spek.specify`, `/spek.plan`, `/spek.implement` are the "default" Spekificity versions of SpecKit commands; users don't need to distinguish between vanilla and enriched at invocation time

Result: Commands are memorable, discoverable, namespace-awarfix immediately communicates "this wraps a SpecKit command"

Result: Commands are memorable, discoverable, and self-documenting.
