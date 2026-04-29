# Research: Spekificity Platform — Core Project Foundation

**Phase**: 0 — Pre-Design Research  
**Date**: 2026-04-29  
**Feature**: 001-spekificity-platform

All NEEDS CLARIFICATION items from the Technical Context have been resolved below.

---

## 1. Graphify

**Decision**: Use `graphifyy` (Python package) installed via `uv tool install graphifyy` (global, per-machine)  
**Rationale**: Graphify is a headless CLI tool with a built-in `--obsidian` flag that directly generates an Obsidian vault structure. It performs AST-based code extraction locally (no API cost) and supports 25+ languages. The `--obsidian` flag eliminates the need to build a custom vault-write layer.  
**Alternatives considered**:  
- Rolling a custom AST parser: rejected — unnecessary complexity, Graphify already does this well  
- A local VS Code extension: rejected — not headless, requires GUI context  

**Key facts**:  
- Install: `uv tool install graphifyy` (or `pipx install graphifyy`)  
- CLI command: `/graphify .` maps the current directory  
- CLI command: `/graphify . --obsidian` generates vault files directly  
- Output: `graph.json` (NetworkX graph), `GRAPH_REPORT.md` (plain-language summary), `graph.html` (interactive), optional `graph.svg`  
- Code extraction is local (tree-sitter AST); documentation/media semantic extraction requires Claude API  
- Incremental refresh: re-run `/graphify .`; Graphify diffs the AST to update changed nodes  
- Already ships as a native skill for Claude Code, GitHub Copilot CLI, Cursor, and 12+ other agents — meaning the `map-codebase` skill can invoke it directly by name  
- **Install mode**: Global (`uv tool install`) — must be treated as a prerequisite, not a local dependency

---

## 2. Obsidian

**Decision**: Use Obsidian vault as a pure filesystem artefact (plain markdown); write vault content directly via filesystem without requiring the Obsidian app  
**Rationale**: Obsidian vaults are plain `.md` files in a directory. No Obsidian app is needed to read or write them. The graph backlink index (`.obsidian/cache.json`) regenerates automatically when the app next opens. AI agents can read the vault directly. This means Spekificity can write vault entries using filesystem operations (markdown writes) with zero dependency on the Obsidian app being installed or running.  
**Alternatives considered**:  
- Obsidian CLI (`obsidian create`, `obsidian read`): rejected — requires Obsidian app to be running; not reliably headless  
- Obsidian Headless Sync (subscription): rejected — paid feature, overkill for a local vault  
- Third-party Obsidian API wrappers: rejected — introduce fragile dependencies  

**Key facts**:  
- Vault format: folder of `.md` files + `.obsidian/` config dir (JSON settings; no binary format)  
- Write approach: direct filesystem writes (no app required)  
- Graph index: regenerates on vault open; AI reads raw markdown directly without needing the index  
- Portability: vault is a plain folder, fully git-committable  
- **Install mode**: Optional — Obsidian desktop app is useful for human visualization but is NOT required for the Spekificity workflow. Document as an optional enhancement.  

---

## 3. SpecKit / Specify

**Decision**: Use `specify-cli` installed via `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (global)  
**Rationale**: SpecKit is the authoritative workflow engine. Spekificity wraps it via the extensions/hooks system, never modifying it.  
**Alternatives considered**:  
- npm TypeScript port (`@oakoliver/specify-cli`): considered but the official Python package is the canonical source  
- Forking SpecKit: rejected — violates Constitution Principle II  

**Key facts**:  
- Version: 0.8.0+ (currently 0.8.2 in production)  
- Extension/hook points in `.specify/extensions.yml`: `before_specify`, `after_specify`, `before_plan`, `after_plan`, `before_implement`, `after_implement`, `before_tasks`, `after_tasks`  
- Templates overridable in `.specify/templates/` — Spekificity can ship enriched templates  
- Skill file locations per agent:  
  - GitHub Copilot: `.github/agents/` (`.agent.md`) + `.github/prompts/`  
  - Claude Code: `.claude/commands/` (markdown)  
  - Codex / generic: `.agents/skills/` (`SKILL.md`)  
- `specify init` auto-generates agent skill files for the selected integration  

---

## 4. Caveman Skill

**Decision**: No installation action required. Caveman is already globally installed in the developer's `~/.agents/skills/caveman/` directory. Spekificity workflow documents reference `/caveman` by command name only.  
**Rationale**: Constitution Principle VI mandates token efficiency throughout. Caveman is the mechanism. Since it is already global, Spekificity only needs to document when and how to invoke it.  
**Key facts**:  
- Invoked as `/caveman` in any AI chat session  
- Supports intensity levels: lite, full (default), ultra  
- Reduces AI verbosity ≥60–75% by character count  
- Spekificity skills should recommend `/caveman lite` for workflow steps that produce structured output (to avoid over-compression of technical content)  

---

## 5. AI Agent Skill Integration

**Decision**: Ship skills in `.agents/skills/` as `SKILL.md` files (generic convention), with agent-specific symlinks/copies for Copilot (`.github/agents/`) and Claude (`.claude/commands/`)  
**Rationale**: Both target agents support the SKILL.md convention. Using `.agents/skills/` as the canonical location keeps the Spekificity custom layer independent of agent-specific directories, satisfying Modular Independence (Principle III).  
**Key facts**:  
- Copilot reads `.github/agents/` — Spekificity provides a copy or symlink there  
- Claude Code reads `.claude/commands/` — same approach  
- Both agents support markdown skill files with a description header and step list  
- The `specify init` command already populates `.github/agents/` for the SpecKit workflow; Spekificity adds alongside those files  

---

## 6. Init Mechanism

**Decision**: Spekificity init is delivered as an AI-executable setup guide (not a compiled CLI binary)  
**Rationale**: Building a compiled CLI (`spekificity init`) would introduce application code, violating Constitution Principle I. Instead, a structured markdown guide (`setup-guides/init-workflow.md`) gives an AI agent exact, ordered steps to execute. A developer says "run Spekificity init" and the AI follows the guide. This satisfies FR-001 through FR-004 and FR-012.  
**Alternatives considered**:  
- Shell script: partially viable, but cannot handle the AI-agent skill installation step (which requires the AI to be active). Shell scripts also drift out of sync with the markdown guides. Decision: shell script for prerequisite checks only (an optional helper), markdown guide as the authoritative source.  
- `specify` extension plugin: considered for future v2 but out of scope for v1.  

---

## 7. Vault Commit Strategy

**Decision**: Commit vault to git by default; provide a `.gitignore` snippet to exclude `vault/graph/` on large repos  
**Rationale**: Lessons learnt, decisions, and patterns are long-lived project artefacts. Version-controlling them preserves history. The `graph/` subdirectory is regeneratable from source, so excluding it on large repos is safe.  

---

## Open Questions Resolved

| Question | Answer |
|----------|--------|
| Can Graphify be installed locally? | No — global install via `uv tool install graphifyy`. Treat as prerequisite. |
| Does Obsidian require the GUI for vault writes? | No — filesystem writes work without the app. App is optional for visualization. |
| What is the preferred vault commit strategy? | Commit vault; optionally gitignore `vault/graph/` on large repos. |
| Should Caveman be opt-in or always-on? | Opt-in per session (invoked with `/caveman`); recommended at session start. |
