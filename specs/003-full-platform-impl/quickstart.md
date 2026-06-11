# Quickstart Validation Guide: Full Platform Implementation

**Feature**: Full Platform Implementation
**Branch**: `003-full-platform-impl`
**Date**: 2026-06-11

This guide validates the feature works end-to-end after implementation. Run these scenarios to confirm all success criteria are met.

## Prerequisites

- Python 3.11+, `uv`, Node.js 22+, `git` in PATH
- macOS (for Obsidian brew path; Windows/Linux steps differ)
- A clean temporary project directory

## Scenario 1: Clean Install (US1 — P1)

### Setup

```bash
# Create and enter clean project dir
mkdir /tmp/spek-test && cd /tmp/spek-test
git init
```

### Steps

```bash
# Install package globally
uv tool install spekificity --from /path/to/local/spekificity

# Verify CLI is available
spek --version
# Expected: version string (e.g. 0.1.0)

# Run init (non-interactive)
spek init --integration claude --script sh
```

### Expected Outcomes

> **Timing note (SC-004):** Total wall-clock time should be under 5 minutes on a clean machine (excluding user interaction for Obsidian GUI install). Time the run with `time spek init ...` to verify.

- `[OK]` lines for each step that ran
- `.spek/vault/`, `.spek/memory/`, `.spek/lat/` directories exist
- `.spek/config.yaml` exists with `integration: claude` and `script_type: sh`
- `.claude/commands/spek-prepare.md` exists (and the other 6 skill files)
- `.mcp.json` exists with `mcpServers.lat` entry
- `.specify/` directory exists (from `specify init`)
- `.git/hooks/post-commit` exists and contains `lat update`

Verify with:
```bash
ls .spek/vault/ .spek/memory/ .spek/lat/
cat .spek/config.yaml
ls .claude/commands/spek-*.md | wc -l  # should print 7
cat .mcp.json
ls .specify/
cat .git/hooks/post-commit
```

---

## Scenario 2: Idempotency (US1 — P1, SC-003)

### Steps

```bash
# Re-run init in the same directory
spek init --integration claude --script sh
```

### Expected Outcomes

- Exit code `0`
- Only `[SKIP]` lines (no `[OK]` lines for previously done steps)
- No files overwritten
- No errors

---

## Scenario 3: Missing Prerequisite (US1 — P1, SC-002)

### Setup

```bash
# Temporarily hide uv from PATH (macOS/Linux)
PATH_WITHOUT_UV=$(echo "$PATH" | tr ':' '\n' | grep -v uv | tr '\n' ':')
```

### Steps

```bash
PATH="$PATH_WITHOUT_UV" spek init --integration claude --script sh
echo "Exit code: $?"
```

### Expected Outcomes

- Exit code `1`
- Error message names `uv` as missing and provides install command
- No partial init state left behind

---

## Scenario 4: Obsidian Phase 1 Halt (US1 — P1, SC-007)

*Requires: Obsidian not installed and PATH does not contain `obsidian`.*

### Steps

```bash
spek init --integration claude --script sh
echo "Exit code: $?"
```

### Expected Outcomes

- Exit code `2`
- Stdout contains Obsidian install confirmation
- Stderr contains CLI registration instructions block (matches `wiki/setup.md` wording)
- All other steps (up to Obsidian) completed normally

---

## Scenario 5: Skill Files in Correct Locations (US1 — P1, SC-004)

### Steps

```bash
# Test cursor-agent integration
mkdir /tmp/spek-cursor && cd /tmp/spek-cursor && git init
spek init --integration cursor-agent --script sh
ls .cursor/skills/spek-prepare/
# Expected: SKILL.md

# Test generic integration  
mkdir /tmp/spek-generic && cd /tmp/spek-generic && git init
spek init --integration generic --script sh
ls .agents/skills/
# Expected: spek-prepare.md (flat format)
```

---

## Scenario 6: MCP Config Merge (US1 — P1, SC-005)

### Setup

```bash
mkdir /tmp/spek-merge && cd /tmp/spek-merge && git init
# Pre-populate .mcp.json with an existing server
echo '{"mcpServers": {"existing-server": {"command": "foo", "args": []}}}' > .mcp.json
```

### Steps

```bash
spek init --integration claude --script sh
cat .mcp.json
```

### Expected Outcomes

- `.mcp.json` contains both `existing-server` AND `lat` entries
- `existing-server` entry is unchanged

---

## Scenario 7: `--no-git-hooks` Flag (US1 — P1, FR-019)

### Steps

```bash
mkdir /tmp/spek-nohooks && cd /tmp/spek-nohooks && git init
spek init --integration claude --script sh --no-git-hooks
ls .git/hooks/post-commit 2>/dev/null && echo "EXISTS" || echo "NOT PRESENT"
# Expected: NOT PRESENT
```

---

## Scenario 8: Skill Files Are Valid Markdown (US2 — P2, SC-006)

### Steps

```bash
cd /tmp/spek-test
# Check all 7 files exist and are non-empty markdown
for f in spek-prepare spek-plan spek-implement spek-conclude spek-lessons spek-context spek-map; do
  echo -n "$f.md: "
  head -1 .claude/commands/$f.md
done
```

### Expected Outcomes

- All 7 files exist
- Each starts with `# /spek.<command>` heading
- No `@workspace`, `#file:`, or `[[wikilink]]` syntax present

```bash
# Verify no agent-specific syntax
grep -r '@workspace\|#file:\|\[\[' .claude/commands/spek-*.md && echo "FOUND AGENT SYNTAX" || echo "CLEAN"
```

---

## Artifact Reference

- CLI contract: [contracts/cli-contract.md](contracts/cli-contract.md)
- Config schema: [contracts/config-schema.md](contracts/config-schema.md)
- MCP config schemas: [contracts/mcp-config-schemas.md](contracts/mcp-config-schemas.md)
- Data model: [data-model.md](data-model.md)
