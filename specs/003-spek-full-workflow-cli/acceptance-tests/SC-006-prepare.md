# Acceptance Tests: SC-006 — Prepare Command (≤60 Seconds)

**Scenario**: SC-006: `spek prepare` completes vault readiness check in ≤60 seconds  
**Feature**: 003-spek-full-workflow-cli  
**Test Date**: [fill on execution]  
**Tester**: [AI Agent / Developer]

---

## Test Scenario 1: Fresh graph (no rebuild required)

**Given**:
- `vault/graph/index.md` exists and is newer than the latest git commit
- No changes since last graphify run

**When**: Run `spek prepare`

**Then**:
- [ ] Output includes: `graph state: fresh`
- [ ] graphify is NOT triggered (no `[graphify]` prefix lines in output)
- [ ] AI prompt printed: `invoke '/spek.prepare' in your AI session`
- [ ] Total elapsed time ≤ 10 seconds (no rebuild)
- [ ] Exit code 0

**Evidence**:
```bash
time spek prepare
```

---

## Test Scenario 2: Stale graph (rebuild triggered)

**Given**:
- `vault/graph/index.md` exists but is older than the latest git commit
- New files were committed since last graph build

**When**: Run `spek prepare`

**Then**:
- [ ] Output includes: `graph state: stale`
- [ ] graphify runs with `[graphify]` prefix on its output lines
- [ ] `vault/graph/index.md` modification time updated after rebuild
- [ ] Total elapsed time ≤ 60 seconds (incremental rebuild)
- [ ] Exit code 0

**Evidence**:
```bash
MTIME_BEFORE=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
time spek prepare
MTIME_AFTER=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
[ "$MTIME_AFTER" -gt "$MTIME_BEFORE" ] && echo "PASS: graph refreshed" || echo "FAIL"
```

---

## Test Scenario 3: Absent graph (full rebuild)

**Given**: `vault/graph/index.md` does not exist

**When**: Run `spek prepare`

**Then**:
- [ ] Output includes: `graph state: absent`
- [ ] graphify runs with `--full` flag (full build)
- [ ] `[graphify]` prefix appears on graphify output lines
- [ ] `vault/graph/index.md` created
- [ ] Total elapsed time ≤ 60 seconds
- [ ] Exit code 0

**Evidence**:
```bash
rm -f vault/graph/index.md
time spek prepare
ls -la vault/graph/index.md
```

---

## Test Scenario 4: Force refresh (`--force-refresh`)

**Given**: Graph is fresh (up-to-date)

**When**: Run `spek prepare --force-refresh`

**Then**:
- [ ] graphify runs regardless of graph state
- [ ] `[graphify]` prefix appears in output
- [ ] `vault/graph/index.md` modification time updated
- [ ] Exit code 0

**Evidence**:
```bash
MTIME_BEFORE=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
spek prepare --force-refresh
MTIME_AFTER=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
[ "$MTIME_AFTER" -ge "$MTIME_BEFORE" ] && echo "PASS" || echo "FAIL"
```

---

## Test Scenario 5: `/spek.prepare` skill — readiness summary

**Given**: `spek prepare` ran successfully, AI session started

**When**: Developer invokes `/spek.prepare` in the AI session

**Then**:
- [ ] Skill reads `vault/context/decisions.md`
- [ ] Skill reads `vault/context/patterns.md`
- [ ] Skill surfaces 3 most-recent entries from `vault/lessons/`
- [ ] Skill checks `workflow-state.json` for active session
- [ ] Readiness summary printed: lists vault context loaded, lessons referenced, active workflow (if any)
- [ ] Ends with recommendation to activate caveman mode

**Evidence**:
```bash
# Visual inspection in AI session — check for:
# - "[spek] ✓ vault context loaded"
# - "active workflow: ..." (if workflow-state.json exists with in-progress status)
# - "recommend: /caveman lite"
```
