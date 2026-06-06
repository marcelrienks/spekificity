# File & Directory Naming Conventions

Lightweight guide to file/directory naming for Spekificity projects. For command naming and invocation, see [skills.md](skills.md).

---

## File & Directory Structure

**Skills Directory:**  
```
.github/agents/skills/
├── spek-prepare/       # Directory name matches command prefix
├── spek-plan/
├── context-load/
└── lat-query/
```

**Artifact Files (Project Root):**
- Specs: `specs/NNNN-feature-name.md` (kebab-case; numeric prefix for ordering)
- Plans: `specs/NNNN-feature-name-plan.md` (same directory as spec)
- Lessons: `vault/lessons/YYYY-MM-DD-feature-name.md` (date + feature name)
- Decisions: `vault/decision.md` (single file, append-only)
- Patterns: `vault/patterns.md` (single file)

---

## Naming Style

**Files & Directories:**
- Use kebab-case (lowercase, hyphens)
- Single-word or two-word names where possible
- Prefix with type indicator when needed (e.g., `NNNN-` for spec ordering, `YYYY-MM-DD-` for lessons)
- Example: `spek-prepare/`, `001-auth-api.md`, `2026-05-20-user-auth-api.md`

**Consistency:**
- Skill directory name matches command: `spek-context/` → `/spek.context`
- Wiki file names single-word lowercase: `architecture.md`, `workflow.md`, not `architecture-guide.md`
- Artifact specs use kebab-case feature names: `001-user-authentication.md`

---

## Implementation Approach

Choose based on project scale and automation needs:

**Agentic (.md + AGENTS.md):**
- Fast start, flexible iteration
- Best for small vaults (≈<200 docs)
- Use when discovery and prompt-tuning frequent

**Programmatic (package/pipeline):**
- Deterministic outputs, typed contracts
- CI-friendly, token-efficient at scale
- Use when reproducibility and audit trails required
