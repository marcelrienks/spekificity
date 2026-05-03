# Acceptance Tests: SC-001 — Setup and Initialization

**Scenario**: SC-001: User completes `spek setup` + `spek init` in ≤15 minutes  
**Feature**: 003-spek-full-workflow-cli  
**Test Date**: [fill on execution]  
**Tester**: [AI Agent / Developer]

---

## Test Scenario 1: First-time setup and initialization (SC-001)

**Given**: Clean machine with project cloned; `spek` installed to PATH via `cp bin/spek /usr/local/bin/spek`

**When**: Developer runs `spek setup` then `spek init` with no additional instructions

**Then**:
- [ ] `spek setup` completes without errors
- [ ] `spek setup --dry-run` prints what would be installed without executing
- [ ] `spek setup --skip-optional` skips optional tools and exits 0
- [ ] `spek init` creates `.spekificity/config.json` with valid JSON
- [ ] `spek init` creates `.spekificity/workflow-state.json` schema structure readable
- [ ] Total elapsed wall-clock time ≤ 15 minutes (including prerequisite installs)
- [ ] Exit codes are 0 for all commands

**Evidence**:
```bash
time spek setup
time spek init
jq . .spekificity/config.json
ls -la .spekificity/
```

---

## Test Scenario 2: Setup idempotency guard

**Given**: `spek setup` already ran successfully

**When**: Run `spek setup` again

**Then**:
- [ ] Previously installed tools are detected (not re-installed)
- [ ] Config values preserved (not overwritten)
- [ ] Exit code 0
- [ ] No "already exists" errors — graceful skip with status output

**Evidence**:
```bash
spek setup
spek status
```

---

## Test Scenario 3: `spek status` summary

**Given**: `spek init` completed

**When**: Run `spek status`

**Then**:
- [ ] Output includes component status for: graphify, obsidian, speckit, spekificity
- [ ] Exit code 0
- [ ] No stack traces or uncaught errors

**Evidence**:
```bash
spek status
echo "exit: $?"
```
