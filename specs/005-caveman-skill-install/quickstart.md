# Quickstart Validation: Caveman Skill Install

## Prerequisites

- A clean test project directory with `git init`
- `spek` CLI installed (`uv tool install spekificity --from git+...`)
- Node.js 22+ in PATH
- Internet access (for GitHub raw skill fetch fallback)

---

## Scenario 1: Skill File Installed (All Integrations)

**Goal**: Validate FR-001, FR-002, FR-007, FR-008 — US1 acceptance scenarios 1 and 2.

### Steps

```bash
# 1. Init with any integration
mkdir /tmp/test-caveman && cd /tmp/test-caveman && git init
spek init /tmp/test-caveman --integration copilot --script sh
```

**Expected output includes**:
```
[OK]   caveman skill installed → .github/agents/skills/caveman/SKILL.md
```
or
```
[SKIP] caveman skill already present
```

```bash
# 2. Verify skill file exists
ls /tmp/test-caveman/.github/agents/skills/caveman/SKILL.md
# Should exit 0

# 3. Verify idempotency — re-run init
spek init /tmp/test-caveman --integration copilot --script sh
# Expected: [SKIP] caveman skill already present
# No duplicate file created
```

---

## Scenario 2: Claude Code Auto-Activation Hooks

**Goal**: Validate FR-004, FR-007, FR-010 — US2 acceptance scenarios 1, 3, 4.

### Steps

```bash
# 1. Init with claude integration
mkdir /tmp/test-caveman-claude && cd /tmp/test-caveman-claude && git init
spek init /tmp/test-caveman-claude --integration claude --script sh
```

**Expected output includes**:
```
[OK]   caveman skill installed → .claude/commands/caveman.md
[OK]   caveman hooks written → .claude/settings.json
```

```bash
# 2. Verify settings.json has both hooks
python3 -c "
import json
s = json.load(open('/tmp/test-caveman-claude/.claude/settings.json'))
hooks = s.get('hooks', {})
assert any('caveman-activate' in str(h) for h in hooks.get('SessionStart', [])), 'SessionStart hook missing'
assert any('caveman-mode-tracker' in str(h) for h in hooks.get('UserPromptSubmit', [])), 'UserPromptSubmit hook missing'
print('PASS: both hooks present')
"

# 3. Verify idempotency
spek init /tmp/test-caveman-claude --integration claude --script sh
# Expected:
# [SKIP] caveman skill already present
# [SKIP] caveman hooks already configured
# Verify no duplicate entries:
python3 -c "
import json
s = json.load(open('/tmp/test-caveman-claude/.claude/settings.json'))
ss = s.get('hooks', {}).get('SessionStart', [])
activate_count = sum(1 for e in ss if any('caveman-activate' in h.get('command','') for h in e.get('hooks',[])))
assert activate_count == 1, f'Expected 1 activate hook, found {activate_count}'
print('PASS: no duplicate hooks')
"
```

---

## Scenario 3: Graceful Failure (Source Unavailable)

**Goal**: Validate FR-009 — US1 acceptance scenario 3.

### Steps

```bash
# Simulate offline by temporarily blocking GitHub (or patch the source)
# This can be unit-tested by mocking the HTTP client

# Verify spek init still completes other steps
# Expected: [WARN] caveman skill fetch failed — manual install: /caveman in Claude Code
# Expected: all other tools (lat, obsidian, speckit) still complete
```

**Verification**: `spek init` exits 0 (or 2 for Obsidian needs_user_action), not 1.

---

## Manual Activation Test (Non-Claude Integrations)

After init with a non-Claude integration:

1. Open the agent (Copilot, Gemini, etc.)
2. Invoke `/caveman` (or the integration's equivalent)
3. Verify the agent responds in compressed format

**Signal**: The skill file content instructs the agent to switch to caveman mode — confirmation is behavioral, not automated.

---

## References

- Contract: [contracts/caveman-install-api.md](contracts/caveman-install-api.md)
- Data model: [data-model.md](data-model.md)
- Source spec: [spec.md](spec.md)
