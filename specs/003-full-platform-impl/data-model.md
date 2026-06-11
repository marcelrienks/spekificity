# Data Model: Full Platform Implementation

**Feature**: Full Platform Implementation
**Branch**: `003-full-platform-impl`
**Date**: 2026-06-11

## Entities

### `InitOptions`

Captures all configuration for a `spek init` run. Populated from CLI flags, prompts, and config file.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `path` | `Path` | Target project directory | Must exist as a directory |
| `integration` | `str` | Agent integration type (e.g. `claude`, `copilot`) | Non-empty string; validated against known list at runtime |
| `script_type` | `Literal["sh", "ps"]` | Script type for hooks | One of `sh` or `ps` |
| `no_git_hooks` | `bool` | Skip git hook installation | Default `False` |

---

### `PrerequisiteResult`

Result of checking one prerequisite tool.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Tool name (e.g. `python`, `uv`, `node`, `git`) |
| `present` | `bool` | Whether tool was found in PATH |
| `version` | `str \| None` | Version string if found |
| `install_hint` | `str` | Human-readable install instruction if missing |

**State transitions**: `present=False` → init fails with descriptive error message citing `install_hint`.

---

### `ToolInstallResult`

Result of installing (or detecting) a single third-party tool.

| Field | Type | Description |
|-------|------|-------------|
| `tool` | `Literal["speckit", "lat_md", "obsidian"]` | Which tool |
| `status` | `Literal["installed", "already_present", "skipped", "needs_user_action"]` | What happened |
| `message` | `str` | Human-readable status message |
| `exit_code` | `int` | Exit code to use if halting (2 for Obsidian CLI registration) |

**State transitions for Obsidian**:
1. App absent → install → `obsidian` in PATH → `installed`, continue
2. App absent → install → `obsidian` NOT in PATH → `needs_user_action`, halt with exit code 2
3. App present, `obsidian` in PATH → `already_present`, proceed to vault setup
4. App present, `obsidian` NOT in PATH → `needs_user_action`, halt with exit code 2

---

### `ScaffoldResult`

Result of creating the `.spek/` directory structure.

| Field | Type | Description |
|-------|------|-------------|
| `created_dirs` | `list[Path]` | Directories newly created |
| `skipped_dirs` | `list[Path]` | Directories already present (idempotent) |

**Required directories**:
- `.spek/vault/lessons/`
- `.spek/memory/`
- `.spek/lat/`

**Required files**:
- `.spek/vault/decisions.md` (initial content: `# Decisions`)
- `.spek/vault/patterns.md` (initial content: `# Patterns`)
- `.spek/vault/lessons/.keep` (empty)
- `.spek/config.yaml` (see Config Schema)

---

### `SkillInstallResult`

Result of copying skill files to the integration's skills directory.

| Field | Type | Description |
|-------|------|-------------|
| `integration` | `str` | Integration type |
| `skills_dir` | `Path` | Destination skills directory |
| `installed` | `list[str]` | Skill file names newly copied |
| `skipped` | `list[str]` | Skill file names already present (not overwritten) |

**Required skill files** (7 total):
- `spek-prepare.md`
- `spek-plan.md`
- `spek-implement.md`
- `spek-conclude.md`
- `spek-lessons.md`
- `spek-context.md`
- `spek-map.md`

---

### `McpConfigResult`

Result of writing the lat.md MCP server entry.

| Field | Type | Description |
|-------|------|-------------|
| `integration` | `str` | Integration type |
| `config_file` | `Path \| None` | Config file written (None if generic/unknown) |
| `status` | `Literal["written", "already_present", "skipped", "printed_instructions"]` | What happened |

---

### `InitResult`

Aggregated result of a complete `spek init` run.

| Field | Type | Description |
|-------|------|-------------|
| `options` | `InitOptions` | The resolved options used |
| `prerequisites` | `list[PrerequisiteResult]` | All prerequisite check results |
| `tools` | `list[ToolInstallResult]` | All tool install results |
| `scaffold` | `ScaffoldResult` | Directory scaffold result |
| `skills` | `SkillInstallResult` | Skill file install result |
| `mcp_config` | `McpConfigResult` | MCP config write result |
| `speckit_initialized` | `bool` | Whether `specify init` was run |
| `git_hook_installed` | `bool` | Whether post-commit hook was written |
| `exit_code` | `int` | Final exit code (0, 1, or 2) |

---

### `SpekConfig`

Structure of `.spek/config.yaml`. Written by `spek init`.

| Field | Type | Description |
|-------|------|-------------|
| `integration` | `str` | Agent integration type |
| `script_type` | `str` | `sh` or `ps` |
| `tools.speckit.enabled` | `bool` | Always `true` |
| `tools.lat_md.enabled` | `bool` | Always `true` |
| `tools.lat_md.index_path` | `str` | `.spek/lat/` |
| `tools.vault.enabled` | `bool` | Always `true` |
| `tools.vault.path` | `str` | `.spek/vault/` |
| `tools.vault.obsidian_vault_name` | `str` | `vault` |
| `context_loading.cache_expiry_minutes` | `int` | `60` |
| `token_limits.standard` | `int` | `3500` |
| `token_limits.lite` | `int` | `2000` |
| `token_limits.ultra` | `int` | `1000` |

---

## Integration Mappings

### Skills Directory Mapping

```python
FLAT_INTEGRATIONS = {"claude", "copilot", "generic"}

INTEGRATION_SKILLS_DIR = {
    "claude": ".claude/commands",
    "copilot": ".github/agents/skills",
    "generic": ".agents/skills",
    "gemini": ".gemini/skills",
    "cursor-agent": ".cursor/skills",
    "windsurf": ".windsurf/skills",
    "cline": ".cline/skills",
    "codex": ".codex/skills",
    "kiro-cli": ".kiro/skills",
    "amp": ".amp/skills",
    "qwen": ".qwen/skills",
    # unknown values → ".agents/skills"
}
```

### MCP Config Mapping

```python
INTEGRATION_MCP_CONFIG = {
    "claude": (".mcp.json", "mcpServers", {}),
    "cursor-agent": (".cursor/mcp.json", "mcpServers", {}),
    "copilot": (".vscode/mcp.json", "servers", {"type": "stdio"}),
    "windsurf": (".windsurf/mcp.json", "mcpServers", {}),
    "cline": (".vscode/settings.json", "cline.mcpServers", {}),
    "gemini": (".gemini/settings.json", "mcpServers", {}),
    "codex": (".codex/mcp.json", "mcpServers", {}),
    "kiro-cli": (".kiro/mcp.json", "mcpServers", {}),
    "amp": (".amp/mcp.json", "mcpServers", {}),
    "qwen": (".qwen/mcp.json", "mcpServers", {}),
    # generic and unknown → print instructions, no file
}
```
