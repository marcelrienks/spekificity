# File & Directory Naming Conventions

Lightweight guide to file/directory naming for Spekificity projects. For command naming and invocation, see [skills.md](skills.md).

---

## File & Directory Structure

**Skills Directory (location depends on agent integration selected at `spek init`):**

| Integration | Agent | Location | Example |
|-------------|-------|----------|---------|
| `claude` | Claude Code | `.claude/commands/` | `.claude/commands/spek-prepare.md` |
| `copilot` | GitHub Copilot | `.github/agents/skills/` | `.github/agents/skills/spek-prepare.md` |
| `gemini` | Gemini CLI | `.gemini/skills/` | `.gemini/skills/spek-prepare/SKILL.md` |
| `cursor-agent` | Cursor | `.cursor/skills/` | `.cursor/skills/spek-prepare/SKILL.md` |
| `windsurf` | Windsurf | `.windsurf/skills/` | `.windsurf/skills/spek-prepare/SKILL.md` |
| `cline` | Cline | `.cline/skills/` | `.cline/skills/spek-prepare/SKILL.md` |
| `codex` | Codex CLI | `.codex/skills/` | `.codex/skills/spek-prepare/SKILL.md` |
| `kiro-cli` | Kiro (AWS) | `.kiro/skills/` | `.kiro/skills/spek-prepare/SKILL.md` |
| `amp` | Amp (Sourcegraph) | `.amp/skills/` | `.amp/skills/spek-prepare/SKILL.md` |
| `qwen` | Qwen Code | `.qwen/skills/` | `.qwen/skills/spek-prepare/SKILL.md` |
| `generic` | Any / tool-agnostic | `.agents/skills/` | `.agents/skills/spek-prepare.md` |
| *(other specify values)* | — | `.agents/skills/` | `.agents/skills/spek-prepare.md` |

Integration values must match `specify`'s supported list exactly — the same value is passed to both `spek init` (for skill file placement) and `specify init`. Run `specify integration list` for the full list of ~30 supported values.

Skill file name matches command (dot replaced with hyphen): `/spek.prepare` → `spek-prepare.md`

Note: `.agents/skills/` is recognised as an alias by Cursor, Codex, Gemini CLI, and Goose — `generic` works as a multi-agent fallback.

**Artifact Files (all inside `.spek/vault/`):**
- Specs: `.spek/vault/specs/NNNN-feature-name.md` (kebab-case; numeric prefix for ordering)
- Plans: `.spek/vault/specs/NNNN-feature-name-plan.md` (same directory as spec)
- Lessons: `.spek/vault/lessons/YYYY-MM-DD-feature-name.md` (date + feature name)
- Decisions: `.spek/vault/decisions.md` (single file, append-only)
- Patterns: `.spek/vault/patterns.md` (single file)

**No `specs/` directory at project root.** All artifacts live inside `.spek/vault/`.

---

## Naming Style

**Files & Directories:**
- Use kebab-case (lowercase, hyphens)
- Single-word or two-word names where possible
- Prefix with type indicator when needed (e.g., `NNNN-` for spec ordering, `YYYY-MM-DD-` for lessons)
- Example: `spek-prepare/`, `001-auth-api.md`, `2026-05-20-user-auth-api.md`

**Spec numbering:** Sequential integers, zero-padded to 4 digits, global across all features in the project (not reset per feature). Start at `0001`. Example: first feature = `0001-feature-name.md`, second = `0002-feature-name.md`. The plan for a spec uses the same number with `-plan` suffix: `0001-feature-name-plan.md`.

**Consistency:**
- Skill directory name matches command: `spek-context/` → `/spek.context`
- Wiki file names single-word lowercase: `architecture.md`, `workflow.md`, not `architecture-guide.md`
- Artifact specs use kebab-case feature names: `001-user-authentication.md`

