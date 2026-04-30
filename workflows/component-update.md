# workflow: component update

## purpose

each component in the spekificity stack can be updated independently without re-initialising the entire project. this document provides step-by-step update procedures for each component and a compatibility reference table.

> **token efficiency tip**: activate `/caveman lite` before reading this document or having an ai agent follow an update procedure — it compresses confirmation messages without losing precision.

## component independence principle

spekificity is built on the principle of modular independence (constitution principle iii). updates to one tool must not require changes to another, except as explicitly noted below.

---

## version compatibility reference

| component | current tested version | minimum required | notes |
|-----------|----------------------|-----------------|-------|
| speckit/specify | 0.8.2 | 0.8.0 | extensions/hooks system required |
| graphify | ≥ 0.5.5 | 0.5.5 | `--obsidian` flag required |
| obsidian (app) | any | n/a | app is optional; vault is stable markdown |
| spekificity custom layer | per repo | — | update by `git pull` + skill re-copy |

---

## section 1 — updating speckit/specify

### when to update

- a new speckit version is released with new features or templates
- `/speckit.*` commands produce unexpected errors (may indicate a breaking change)
- speckit's `extensions.yml` hook format has changed

### update procedure

1. **upgrade the global speckit package**:
   ```bash
   uv tool upgrade specify-cli
   ```

2. **verify the upgrade**:
   ```bash
   specify --version
   # note the new version number
   ```

3. **refresh speckit infrastructure in your project**:
   ```bash
   specify init .
   ```
   this updates `.specify/scripts/`, `.specify/templates/`, and `.github/agents/` with the new speckit version's built-in files — without overwriting your constitution or custom configuration.

4. **check for breaking changes**: compare your `.specify/extensions.yml` hook names against speckit's changelog. hook names in `0.8.x+` are stable. if hook names changed, update the corresponding entries in `.specify/extensions.yml`.

### spekificity changes needed?

**usually none.** spekificity skills decorate speckit commands by name (e.g., `/speckit.specify`). as long as speckit command names do not change, no spekificity updates are needed.

**exception**: if speckit renames or removes a command that a spekificity enrich skill invokes, update the `invoke` step in the affected skill file:
- `skills/speckit-enrich/specify-enrich.md` → references `/speckit.specify`
- `skills/speckit-enrich/plan-enrich.md` → references `/speckit.plan`
- `skills/speckit-enrich/implement-enrich.md` → references `/speckit.implement`

### how to detect breaking changes

```bash
# check speckit changelog after upgrade:
uv tool run specify-cli --changelog 2>/dev/null || \
  echo "check https://github.com/github/spec-kit/releases for changelog"
```

---

## section 2 — updating graphify

### when to update

- a new graphify version is released
- `/map-codebase` produces errors (may indicate cli arg changes)
- new language support is needed

### update procedure

1. **upgrade the global graphify package**:
   ```bash
   uv tool upgrade graphifyy
   ```

2. **verify the upgrade**:
   ```bash
   graphify --version
   # note the new version number
   ```

3. **test with a dry run** (if concerned about breaking changes):
   ```bash
   graphify . --obsidian --output vault/graph/ --dry-run 2>/dev/null || \
     graphify . --obsidian --output vault/graph/
   ```

4. **refresh the vault** to pick up any improvements in the new version:
   ```bash
   # in ai session:
   /map-codebase --full
   ```

### spekificity changes needed?

**usually none.** the `/map-codebase` skill invokes `graphify . --obsidian --output vault/graph/`. as long as this command is valid, no changes are needed.

**exception**: if the graphify cli argument format changes (e.g., `--obsidian` is renamed), update `skills/map-codebase/skill.md` — specifically the command in step 3 of the steps section. then re-distribute the updated skill:
```bash
cp skills/map-codebase/skill.md .github/agents/map-codebase.agent.md
cp skills/map-codebase/skill.md .claude/commands/map-codebase.md
```

**vault integrity**: existing vault files remain intact across graphify upgrades. the vault is plain markdown — graphify updates the graph data but does not change the file format.

---

## section 3 — updating obsidian (desktop app)

### when to update

- a new obsidian version is available
- the obsidian app prompt indicates an update is available

### update procedure

**macos**:
1. open obsidian → settings → about → check for updates
2. or download the new `.dmg` from [obsidian.md/download](https://obsidian.md/download) and replace the app

**linux**:
1. download the new `.appimage` from [obsidian.md/download](https://obsidian.md/download)
2. replace the existing `.appimage`

### spekificity changes needed?

**none.** the obsidian vault format is stable markdown. obsidian app updates never affect the vault file structure. vault files written by spekificity skills remain fully compatible across all obsidian versions.

**note**: `.obsidian/workspace.json` may be regenerated on first open after an update. this is safe — it is already gitignored.

---

## section 4 — updating the spekificity custom layer

the spekificity custom layer is the set of `skills/`, `workflows/`, and `setup-guides/` files in this repository. when a new version is released, update by pulling and re-distributing.

### when to update

- you want new skills or workflow improvements from the spekificity project
- a skill is producing incorrect output (may have been fixed in a newer version)
- a new spekificity skill has been published

### update procedure

1. **pull the latest spekificity files**:
   ```bash
   # if you have spekificity as a git submodule or reference clone:
   cd /path/to/spekificity
   git pull origin main
   ```

   or download the updated files directly:
   ```bash
   # copy updated skills into your project
   cp -r /path/to/updated/spekificity/skills ./skills
   cp -r /path/to/updated/spekificity/workflows ./workflows
   cp -r /path/to/updated/spekificity/setup-guides ./setup-guides
   ```

2. **re-distribute updated skills to your ai agent directories**:

   **github copilot**:
   ```bash
   cp skills/map-codebase/skill.md .github/agents/map-codebase.agent.md
   cp skills/lessons-learnt/skill.md .github/agents/lessons-learnt.agent.md
   cp skills/context-load/skill.md .github/agents/context-load.agent.md
   cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
   cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
   cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
   ```

   **claude code**:
   ```bash
   cp skills/map-codebase/skill.md .claude/commands/map-codebase.md
   cp skills/lessons-learnt/skill.md .claude/commands/lessons-learnt.md
   cp skills/context-load/skill.md .claude/commands/context-load.md
   cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
   cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
   cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
   ```

3. **verify** the updated skills are active in your ai session by running `/context-load` — if it responds normally, the skills are loaded.

### speckit, graphify, and obsidian changes needed?

**none** for routine spekificity updates. spekificity skills interact with other tools only through stable cli interfaces and filesystem paths — all of which are documented in the individual skill files.

---

## quick reference: update impact matrix

| i'm updating... | must also update... | can skip... |
|-----------------|---------------------|-------------|
| speckit | re-run `specify init .` | vault, graphify, obsidian |
| graphify | `/map-codebase --full` to refresh vault | speckit, obsidian, spekificity skills |
| obsidian app | nothing | everything else |
| spekificity skills | re-copy to `.github/agents/` and `.claude/commands/` | speckit, graphify, obsidian |
