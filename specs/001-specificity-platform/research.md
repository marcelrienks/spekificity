# research: spekificity platform — core project foundation

**phase**: 0 — pre-design research  
**date**: 2026-04-29  
**feature**: 001-spekificity-platform

all needs clarification items from the technical context have been resolved below.

---

## 1. graphify

**decision**: use `graphifyy` (python package) installed via `uv tool install graphifyy` (global, per-machine)  
**rationale**: graphify is a headless cli tool with a built-in `--obsidian` flag that directly generates an obsidian vault structure. it performs ast-based code extraction locally (no api cost) and supports 25+ languages. the `--obsidian` flag eliminates the need to build a custom vault-write layer.  
**alternatives considered**:  
- rolling a custom ast parser: rejected — unnecessary complexity, graphify already does this well  
- a local vs code extension: rejected — not headless, requires gui context  

**key facts**:  
- install: `uv tool install graphifyy` (or `pipx install graphifyy`)  
- cli command: `/graphify .` maps the current directory  
- cli command: `/graphify . --obsidian` generates vault files directly  
- output: `graph.json` (networkx graph), `graph_report.md` (plain-language summary), `graph.html` (interactive), optional `graph.svg`  
- code extraction is local (tree-sitter ast); documentation/media semantic extraction requires claude api  
- incremental refresh: re-run `/graphify .`; graphify diffs the ast to update changed nodes  
- already ships as a native skill for claude code, github copilot cli, cursor, and 12+ other agents — meaning the `map-codebase` skill can invoke it directly by name  
- **install mode**: global (`uv tool install`) — must be treated as a prerequisite, not a local dependency

---

## 2. obsidian

**decision**: use obsidian vault as a pure filesystem artefact (plain markdown); write vault content directly via filesystem without requiring the obsidian app  
**rationale**: obsidian vaults are plain `.md` files in a directory. no obsidian app is needed to read or write them. the graph backlink index (`.obsidian/cache.json`) regenerates automatically when the app next opens. ai agents can read the vault directly. this means spekificity can write vault entries using filesystem operations (markdown writes) with zero dependency on the obsidian app being installed or running.  
**alternatives considered**:  
- obsidian cli (`obsidian create`, `obsidian read`): rejected — requires obsidian app to be running; not reliably headless  
- obsidian headless sync (subscription): rejected — paid feature, overkill for a local vault  
- third-party obsidian api wrappers: rejected — introduce fragile dependencies  

**key facts**:  
- vault format: folder of `.md` files + `.obsidian/` config dir (json settings; no binary format)  
- write approach: direct filesystem writes (no app required)  
- graph index: regenerates on vault open; ai reads raw markdown directly without needing the index  
- portability: vault is a plain folder, fully git-committable  
- **install mode**: optional — obsidian desktop app is useful for human visualization but is not required for the spekificity workflow. document as an optional enhancement.  

---

## 3. speckit / specify

**decision**: use `specify-cli` installed via `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` (global)  
**rationale**: speckit is the authoritative workflow engine. spekificity wraps it via the extensions/hooks system, never modifying it.  
**alternatives considered**:  
- npm typescript port (`@oakoliver/specify-cli`): considered but the official python package is the canonical source  
- forking speckit: rejected — violates constitution principle ii  

**key facts**:  
- version: 0.8.0+ (currently 0.8.2 in production)  
- extension/hook points in `.specify/extensions.yml`: `before_specify`, `after_specify`, `before_plan`, `after_plan`, `before_implement`, `after_implement`, `before_tasks`, `after_tasks`  
- templates overridable in `.specify/templates/` — spekificity can ship enriched templates  
- skill file locations per agent:  
  - github copilot: `.github/agents/` (`.agent.md`) + `.github/prompts/`  
  - claude code: `.claude/commands/` (markdown)  
  - codex / generic: `.agents/skills/` (`skill.md`)  
- `specify init` auto-generates agent skill files for the selected integration  

---

## 4. caveman skill

**decision**: no installation action required. caveman is already globally installed in the developer's `~/.agents/skills/caveman/` directory. spekificity workflow documents reference `/caveman` by command name only.  
**rationale**: constitution principle vi mandates token efficiency throughout. caveman is the mechanism. since it is already global, spekificity only needs to document when and how to invoke it.  
**key facts**:  
- invoked as `/caveman` in any ai chat session  
- supports intensity levels: lite, full (default), ultra  
- reduces ai verbosity ≥60–75% by character count  
- spekificity skills should recommend `/caveman lite` for workflow steps that produce structured output (to avoid over-compression of technical content)  

---

## 5. ai agent skill integration

**decision**: ship skills in `.agents/skills/` as `skill.md` files (generic convention), with agent-specific symlinks/copies for copilot (`.github/agents/`) and claude (`.claude/commands/`)  
**rationale**: both target agents support the skill.md convention. using `.agents/skills/` as the canonical location keeps the spekificity custom layer independent of agent-specific directories, satisfying modular independence (principle iii).  
**key facts**:  
- copilot reads `.github/agents/` — spekificity provides a copy or symlink there  
- claude code reads `.claude/commands/` — same approach  
- both agents support markdown skill files with a description header and step list  
- the `specify init` command already populates `.github/agents/` for the speckit workflow; spekificity adds alongside those files  

---

## 6. init mechanism

**decision**: spekificity init is delivered as an ai-executable setup guide (not a compiled cli binary)  
**rationale**: building a compiled cli (`spekificity init`) would introduce application code, violating constitution principle i. instead, a structured markdown guide (`setup-guides/init-workflow.md`) gives an ai agent exact, ordered steps to execute. a developer says "run spekificity init" and the ai follows the guide. this satisfies fr-001 through fr-004 and fr-012.  
**alternatives considered**:  
- shell script: partially viable, but cannot handle the ai-agent skill installation step (which requires the ai to be active). shell scripts also drift out of sync with the markdown guides. decision: shell script for prerequisite checks only (an optional helper), markdown guide as the authoritative source.  
- `specify` extension plugin: considered for future v2 but out of scope for v1.  

---

## 7. vault commit strategy

**decision**: commit vault to git by default; provide a `.gitignore` snippet to exclude `vault/graph/` on large repos  
**rationale**: lessons learnt, decisions, and patterns are long-lived project artefacts. version-controlling them preserves history. the `graph/` subdirectory is regeneratable from source, so excluding it on large repos is safe.  

---

## open questions resolved

| question | answer |
|----------|--------|
| can graphify be installed locally? | no — global install via `uv tool install graphifyy`. treat as prerequisite. |
| does obsidian require the gui for vault writes? | no — filesystem writes work without the app. app is optional for visualization. |
| what is the preferred vault commit strategy? | commit vault; optionally gitignore `vault/graph/` on large repos. |
| should caveman be opt-in or always-on? | opt-in per session (invoked with `/caveman`); recommended at session start. |
