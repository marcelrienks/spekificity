---
title: "lat.md Setup & Integration (C5.0)"
status: "ATOMIC SPECIFICATION"
version: "2026-05-23"
---

# ATOMIC SPECIFICATION: lat.md Setup & Integration (C5.0)

**Status:** ATOMIC SPECIFICATION  
**Type:** Infrastructure — lat.md Installation, Configuration, and `/spek.map` Integration  
**Version:** 2026-05-23  
**Replaces:** legacy graph installation spec (archived)
**Depends On:** spek-map-command.md, graph-refresh-strategy.md, node-schema-design.md  
**Used By:** `/spek.prepare` (freshness check), `/spek.conclude` (incremental sync), `/spek.plan` (context queries)

## Success Criteria

- ✅ lat.md installed and verified
- ✅ Configuration file updated (.spek/config.yaml references `lat.md`)
- ✅ Indexing operational for Markdown + selected source languages
- ✅ Incremental sync functional (file watcher detects changes, incremental updates)
- ✅ Performance reasonable for development use (incremental updates in seconds)
- ✅ Documentation (vault) indexing integrated with code metadata

---

## Executive Summary

`lat.md` is the project's canonical indexing tool: Markdown-first, pluggable extractors for source metadata, incremental refresh, and an agent-friendly query interface. This spec documents installation, configuration, refresh strategy, and how `/spek.map` orchestrates lat.md operations.

---

## Part 1: lat.md Overview

### What Is lat.md?

**lat.md** is a Markdown-native indexing and linkage tool that:
- Indexes Markdown (frontmatter, headings, wikilinks) and extracts metadata from source files
- Produces a unified, queryable knowledge layer that links docs and code
- Supports incremental refresh and watch mode for fast updates during development
- Provides a small agent-friendly query surface (MCP tool or HTTP API)
- Is extensible via plug-in extractors for additional languages or metadata

**Key Advantage:** It gives a document-first graph that ties specs and vault content to source artifacts, enabling agents to reason from high-quality project intent and decisions.

---

## Part 2: Installation & Configuration

### Prerequisites

- **Python 3.11+** — Check with `python3 --version`
- **Git** — Check with `git --version`
- **Project folder** initialized as a git repository

> Install lat.md following its official installation instructions for your platform (package manager or release artifact). Verify the installation using the tool's provided verification method (CLI `--version` or equivalent).

### Step 1: Install lat.md

Follow vendor installation docs. Typical verification steps:

```bash
# Example verification (standardized CLI name)
lat --version
```

If your environment requires a package manager, prefer installing lat.md globally or in a project-managed environment so `/spek.map` can invoke it.

### Step 2: Create lat.md Configuration

Update `.spek/config.yaml` to declare `lat.md` as the indexing tool and provide index settings. Example:

```yaml
# lat.md Configuration for Spekificity

project_name: "spekificity"
project_root: "."

lat:
  enabled: true
  # Languages and file types to index
  languages:
    - markdown
    - python
    - typescript
    - javascript
    - yaml
  include_paths:
    - src/
    - lib/
    - wiki/
    - wiki/specs/
  exclude_paths:
    - node_modules/
    - .git/
    - __pycache__/
  parse_options:
    parse_frontmatter: true
    extract_wikilinks: true
    extract_headings: true
    extract_docstrings: true

# Index Storage & Cache (format/tool-specific)
lat_storage:
  # Non-human-readable index storage: keep machine data out of the human
  # readable `wiki/` folder. Store lat.md on-disk index and caches under
  # the hidden `.spek/` runtime folder by default so `wiki/` remains
  # human-browseable and git-friendly.
  path: ".spek/lat/"
  cache_ttl_seconds: 3600

# Refresh strategy
refresh_strategy:
  auto_refresh_on_git_commit: true
  auto_refresh_interval_seconds: 3600
  watch_enabled: true
  watch_debounce_ms: 500

# Agent integration
agent_integration:
  enabled: true
  api_timeout_seconds: 5
  tools:
    - lat_symbols
    - lat_definition
    - lat_references
    - lat_impact
    - lat_query

# MCP / Adapter guidance
# If your environment does not expose lat's MCP tools directly, implement a small adapter layer
# that translates MCP tool calls into one of these invocation modes: local CLI wrapper (`lat`),
# HTTP bridge (lat HTTP API), or a language-specific wrapper (Python package that shells out).
# This adapter should enforce the `api_timeout_seconds` and a simple retry/backoff policy
# (e.g., 2 retries with exponential backoff starting at 250ms) so agent callers can depend on
# consistent timeout semantics.

# Obsidian fallback
# Automated vault exports rely on Obsidian tooling. If Obsidian CLI/plugins are not available,
# provide an alternative export path (dataview plugin export, Obsidian cache.json, or a manual
# JSONL export) and document CI behavior when Obsidian is absent (skip doc-merge or fail-fast
# depending on policy).
```

### Step 3: Initialize Index

Run the lat.md initialization step as documented by the tool. The goal is to create an on-disk index under the runtime folder (`.spek/lat/`) and ensure configuration validation passes. If human-readable exports are required, produce JSON/graph exports into `wiki/vault/graph/exports/` (optional) so the `wiki/` remains browseable.

Output expectations:

- Index directory created (e.g. `.spek/lat/`) with metadata
- Initial index build completes and reports file counts
- Validation checks for consistency and missing links

---

### Step 4: Optional Git Hook (Auto-Refresh)

If desired, add a lightweight `post-commit` hook that triggers an incremental lat.md refresh. Keep hooks optional and make them skippable via an environment flag.

Example (conceptual):

```bash
#!/bin/bash
# Auto-refresh lat.md index after each commit (optional)
if [ -z "$LAT_SKIP_HOOKS" ]; then
  lat.md index --incremental --config .spek/config.yaml || true
fi
```

Make executable: `chmod +x .git/hooks/post-commit`

---

## Part 3: `/spek.map` Command Integration

`/spek.map` orchestrates lat.md operations. Modes:

- `--full` — Full rebuild of the index (use after large refactor)
- `--incremental` — Sync only changed files (default; fast)
- `--watch` — Run in watch mode (continuous incremental updates)
- `--query` — Interactive query against the lat.md index
- `--validate` — Run consistency checks

Usage is intentionally tool-agnostic inside Spekificity; the command invokes lat.md under the hood according to the configured mode.

---

## Part 4: Agent Integration (Query Tools)

Spekificity exposes a small set of agent-callable tools backed by lat.md (MCP or HTTP bridging):

- `lat_symbols` — List symbols in a file or module
- `lat_definition` — Find where a symbol is defined
- `lat_references` — Find references to a symbol
- `lat_impact` — Estimate impact radius for a change
- `lat_query` — Free-form index query (tool-specific DSL)

These tools should be documented in the agent toolbox and expose guarded timeouts to avoid long-running queries.

---

## Refresh & Validation Strategy

- Prefer incremental refresh for normal development flows (seconds)
- Run full rebuild after large refactors or on CI nightly if desired
- Validate index after incremental updates for consistency (missing links, orphaned nodes)
- Keep watch mode optional for local development (debounce changes)

---

## Testing & Verification

- Unit test the indexer extractors where possible
- Validate agent queries return expected context for known symbols
- Add a CI step that performs an incremental index and runs basic validation checks

---

## Migration Notes

- Any previous legacy graph artifacts should be removed or migrated into the new `lat.md` index store. Update references across wiki/specs and code.
- Ensure `.spek/config.yaml` no longer references legacy tool names.

---

## See Also

- [spek-map-command.md](../specs/110-speckit-integration-contract.md) — Orchestration notes
- [graph-refresh-strategy.md](../specs/053-graph-refresh-strategy.md) — Refresh guidance (rename as needed)
