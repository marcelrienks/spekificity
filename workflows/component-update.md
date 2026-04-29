# Workflow: Component Update

## Purpose

Each component in the Spekificity stack can be updated independently without re-initialising the entire project. This document provides step-by-step update procedures for each component and a compatibility reference table.

> **Token efficiency tip**: Activate `/caveman lite` before reading this document or having an AI agent follow an update procedure — it compresses confirmation messages without losing precision.

## Component Independence Principle

Spekificity is built on the principle of modular independence (Constitution Principle III). Updates to one tool MUST NOT require changes to another, except as explicitly noted below.

---

## Version Compatibility Reference

| Component | Current Tested Version | Minimum Required | Notes |
|-----------|----------------------|-----------------|-------|
| SpecKit/Specify | 0.8.2 | 0.8.0 | Extensions/hooks system required |
| Graphify | ≥ 0.5.5 | 0.5.5 | `--obsidian` flag required |
| Obsidian (app) | any | N/A | App is optional; vault is stable markdown |
| Spekificity custom layer | per repo | — | Update by `git pull` + skill re-copy |

---

## Section 1 — Updating SpecKit/Specify

### When to update

- A new SpecKit version is released with new features or templates
- `/speckit.*` commands produce unexpected errors (may indicate a breaking change)
- SpecKit's `extensions.yml` hook format has changed

### Update procedure

1. **Upgrade the global SpecKit package**:
   ```bash
   uv tool upgrade specify-cli
   ```

2. **Verify the upgrade**:
   ```bash
   specify --version
   # Note the new version number
   ```

3. **Refresh SpecKit infrastructure in your project**:
   ```bash
   specify init .
   ```
   This updates `.specify/scripts/`, `.specify/templates/`, and `.github/agents/` with the new SpecKit version's built-in files — without overwriting your constitution or custom configuration.

4. **Check for breaking changes**: Compare your `.specify/extensions.yml` hook names against SpecKit's changelog. Hook names in `0.8.x+` are stable. If hook names changed, update the corresponding entries in `.specify/extensions.yml`.

### Spekificity changes needed?

**Usually none.** Spekificity skills decorate SpecKit commands by name (e.g., `/speckit.specify`). As long as SpecKit command names do not change, no Spekificity updates are needed.

**Exception**: If SpecKit renames or removes a command that a Spekificity enrich skill invokes, update the `invoke` step in the affected skill file:
- `skills/speckit-enrich/specify-enrich.md` → references `/speckit.specify`
- `skills/speckit-enrich/plan-enrich.md` → references `/speckit.plan`
- `skills/speckit-enrich/implement-enrich.md` → references `/speckit.implement`

### How to detect breaking changes

```bash
# Check SpecKit changelog after upgrade:
uv tool run specify-cli --changelog 2>/dev/null || \
  echo "Check https://github.com/github/spec-kit/releases for changelog"
```

---

## Section 2 — Updating Graphify

### When to update

- A new Graphify version is released
- `/map-codebase` produces errors (may indicate CLI arg changes)
- New language support is needed

### Update procedure

1. **Upgrade the global Graphify package**:
   ```bash
   uv tool upgrade graphifyy
   ```

2. **Verify the upgrade**:
   ```bash
   graphify --version
   # Note the new version number
   ```

3. **Test with a dry run** (if concerned about breaking changes):
   ```bash
   graphify . --obsidian --output vault/graph/ --dry-run 2>/dev/null || \
     graphify . --obsidian --output vault/graph/
   ```

4. **Refresh the vault** to pick up any improvements in the new version:
   ```bash
   # In AI session:
   /map-codebase --full
   ```

### Spekificity changes needed?

**Usually none.** The `/map-codebase` skill invokes `graphify . --obsidian --output vault/graph/`. As long as this command is valid, no changes are needed.

**Exception**: If the Graphify CLI argument format changes (e.g., `--obsidian` is renamed), update `skills/map-codebase/SKILL.md` — specifically the command in Step 3 of the Steps section. Then re-distribute the updated skill:
```bash
cp skills/map-codebase/SKILL.md .github/agents/map-codebase.agent.md
cp skills/map-codebase/SKILL.md .claude/commands/map-codebase.md
```

**Vault integrity**: Existing vault files remain intact across Graphify upgrades. The vault is plain markdown — Graphify updates the graph data but does not change the file format.

---

## Section 3 — Updating Obsidian (Desktop App)

### When to update

- A new Obsidian version is available
- The Obsidian app prompt indicates an update is available

### Update procedure

**macOS**:
1. Open Obsidian → Settings → About → Check for updates
2. Or download the new `.dmg` from [obsidian.md/download](https://obsidian.md/download) and replace the app

**Linux**:
1. Download the new `.AppImage` from [obsidian.md/download](https://obsidian.md/download)
2. Replace the existing `.AppImage`

### Spekificity changes needed?

**None.** The Obsidian vault format is stable markdown. Obsidian app updates NEVER affect the vault file structure. Vault files written by Spekificity skills remain fully compatible across all Obsidian versions.

**Note**: `.obsidian/workspace.json` may be regenerated on first open after an update. This is safe — it is already gitignored.

---

## Section 4 — Updating the Spekificity Custom Layer

The Spekificity custom layer is the set of `skills/`, `workflows/`, and `setup-guides/` files in this repository. When a new version is released, update by pulling and re-distributing.

### When to update

- You want new skills or workflow improvements from the Spekificity project
- A skill is producing incorrect output (may have been fixed in a newer version)
- A new Spekificity skill has been published

### Update procedure

1. **Pull the latest Spekificity files**:
   ```bash
   # If you have Spekificity as a git submodule or reference clone:
   cd /path/to/spekificity
   git pull origin main
   ```

   Or download the updated files directly:
   ```bash
   # Copy updated skills into your project
   cp -r /path/to/updated/spekificity/skills ./skills
   cp -r /path/to/updated/spekificity/workflows ./workflows
   cp -r /path/to/updated/spekificity/setup-guides ./setup-guides
   ```

2. **Re-distribute updated skills to your AI agent directories**:

   **GitHub Copilot**:
   ```bash
   cp skills/map-codebase/SKILL.md .github/agents/map-codebase.agent.md
   cp skills/lessons-learnt/SKILL.md .github/agents/lessons-learnt.agent.md
   cp skills/context-load/SKILL.md .github/agents/context-load.agent.md
   cp skills/speckit-enrich/specify-enrich.md .github/agents/speckit-enrich-specify.agent.md
   cp skills/speckit-enrich/plan-enrich.md .github/agents/speckit-enrich-plan.agent.md
   cp skills/speckit-enrich/implement-enrich.md .github/agents/speckit-enrich-implement.agent.md
   ```

   **Claude Code**:
   ```bash
   cp skills/map-codebase/SKILL.md .claude/commands/map-codebase.md
   cp skills/lessons-learnt/SKILL.md .claude/commands/lessons-learnt.md
   cp skills/context-load/SKILL.md .claude/commands/context-load.md
   cp skills/speckit-enrich/specify-enrich.md .claude/commands/speckit-enrich-specify.md
   cp skills/speckit-enrich/plan-enrich.md .claude/commands/speckit-enrich-plan.md
   cp skills/speckit-enrich/implement-enrich.md .claude/commands/speckit-enrich-implement.md
   ```

3. **Verify** the updated skills are active in your AI session by running `/context-load` — if it responds normally, the skills are loaded.

### SpecKit, Graphify, and Obsidian changes needed?

**None** for routine Spekificity updates. Spekificity skills interact with other tools only through stable CLI interfaces and filesystem paths — all of which are documented in the individual skill files.

---

## Quick Reference: Update Impact Matrix

| I'm updating... | Must also update... | Can skip... |
|-----------------|---------------------|-------------|
| SpecKit | Re-run `specify init .` | Vault, Graphify, Obsidian |
| Graphify | `/map-codebase --full` to refresh vault | SpecKit, Obsidian, Spekificity skills |
| Obsidian app | Nothing | Everything else |
| Spekificity skills | Re-copy to `.github/agents/` and `.claude/commands/` | SpecKit, Graphify, Obsidian |
