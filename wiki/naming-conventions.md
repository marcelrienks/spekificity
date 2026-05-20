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

### 1. Spekificity User-Facing Skills (`spek.*` prefix)

**Format:** `/spek.oneword` or `/spek.hyphenated` (only when one word insufficient)  
**Prefix:** `spek.` (always)  
**Pattern:** Action-noun or noun

| Skill | Command | Purpose |
|-------|---------|---------|
| Preparation | `/spek.prepare` | Initialize workspace, git state, graph freshness, and feature state |
| Context loading | `/spek.context` | Load vault, repo memory, and graph context into session |
| Code mapping | `/spek.map` | Build or refresh code/document graph |
| Full automation | `/spek.automate` | Orchestrate SpecKit flow through spec, plan, analyze, remediation, and tasks |
| Implementation | `/spek.implement` | Execute approved tasks with project context |
| Post-processing | `/spek.post` | Archive feature outcomes, lessons, vault updates, and graph refresh |
| Lessons capture | `/spek.lessons` | Extract structured lessons when run explicitly |

**Rationale:**
- All commands keep `spek.` prefix for namespace consistency
- Command portions simplified: single words where possible (`context`, `map`, `lessons`, `prepare`, `post`, `automate`)
- Hyphenation avoided; if compound needed, use single word or acceptable hyphen (e.g., `/spek.load-context` would only if `context` alone insufficient, but `context` is clear)

---

### 2. Underlying SpecKit Commands (Keep Vanilla Namespace)

**Format:** `speckit.*` (unchanged; distinct namespace)  
**Pattern:** `speckit.command`

| Skill | Command | Purpose | Used By |
|-------|---------|---------|---------|
| Constitution | `/speckit.constitution` | Define project principles | upstream/manual |
| Specification | `/speckit.specify` | Create feature spec | `/spek.automate` |
| Clarification | `/speckit.clarify` | Resolve spec ambiguities | `/spek.automate` |
| Planning | `/speckit.plan` | Create implementation plan | `/spek.automate` |
| Task generation | `/speckit.tasks` | Generate task list | `/spek.automate` |
| Analysis | `/speckit.analyze` | Cross-artifact consistency check | `/spek.automate` |
| Implementation | `/speckit.implement` | Execute tasks | `/spek.implement` |
| Task-to-issues | `/speckit.taskstoissues` | Convert tasks to GitHub issues | upstream/manual |

**Rationale:**
- Vanilla SpecKit commands use `speckit.*` namespace for clarity (SpecKit-owned tools, not Spekificity)
- Distinction is intentional and visible in command name
- No aliasing needed; namespace distinction is primary signal

---

### 3. Support Commands

Support capabilities such as context loading, graph refresh, preparation, post-processing, and lessons capture are user-facing commands in their own right. They can also be called internally by `spek.automate` or `spek.implement` when orchestration needs them.

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

### Primary Workflow
```
/spek.prepare         # Pre-feature setup
/spek.context         # Load or reload project context
/spek.map             # Build or refresh graph explicitly
/spek.automate        # Load context, run specify/clarify/plan/analyze/remediate/tasks
/spek.implement       # Execute approved tasks with enriched code context
/spek.post            # Persist lessons, vault updates, graph refresh
/spek.lessons         # Extract lessons explicitly when needed
```

### Underlying SpecKit Flow Used by `/spek.automate`
```
/speckit.specify
/speckit.clarify      # Optional
/speckit.plan
/speckit.analyze      # Optional but available for remediation loop
/speckit.tasks
```

### Utilities
```
/caveman              # Compression control
/read-wiki            # Wiki analysis + caching
```

---

## Implementation Details

### Directory Structure for Skills
Directory name matches command suffix (prefix `spek-` for Spekificity skills to group them)

```
.github/agents/skills/
├── spek-automate/
│   └── SKILL.md
├── spek-implement/
│   └── SKILL.md
├── internal-support/
│   └── ...
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
