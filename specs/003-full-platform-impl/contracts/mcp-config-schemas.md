# MCP Config Schemas: lat.md Per Integration

**Feature**: Full Platform Implementation
**Date**: 2026-06-11

## Overview

`spek init` writes a lat.md MCP server entry to the integration-specific config file. For `generic` and unknown integrations, manual instructions are printed instead.

## Fully Specified Formats

### `claude` → `.mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `cursor-agent` → `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `copilot` → `.vscode/mcp.json`

```json
{
  "servers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"],
      "type": "stdio"
    }
  }
}
```

## Inferred Formats (verify against vendor docs before finalizing)

### `windsurf` → `.windsurf/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `cline` → `.vscode/settings.json`

```json
{
  "cline.mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `gemini` → `.gemini/settings.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `codex` → `.codex/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `kiro-cli` → `.kiro/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `amp` → `.amp/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

### `qwen` → `.qwen/mcp.json`

```json
{
  "mcpServers": {
    "lat": {
      "command": "lat",
      "args": ["mcp"]
    }
  }
}
```

## `generic` and Unknown Integrations — Print Instructions

No config file is written. Print to stdout:

```
lat.md MCP server not auto-configured for this integration.
Add the following to your agent's MCP config manually:

  server name: lat
  command:     lat
  args:        mcp
  type:        stdio
```

## Merge Behaviour Contract

1. If config file exists: parse JSON, add `lat` entry under the correct key, write back. Do NOT clobber existing entries.
2. If `lat` entry already present under that key: skip (idempotent).
3. If config file does not exist: create it with only the `lat` entry.
4. Parent directories are created if missing (`mkdir -p` equivalent).
