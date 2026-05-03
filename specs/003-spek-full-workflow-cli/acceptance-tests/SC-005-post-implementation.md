# Acceptance Tests: SC-005 — Post-Implementation (≤3 Minutes)

**Scenario**: SC-005: `spek post` completes lessons + graph refresh in ≤3 minutes  
**Feature**: 003-spek-full-workflow-cli  
**Test Date**: [fill on execution]  
**Tester**: [AI Agent / Developer]

---

## Test Scenario 1: Full `spek post` run

**Given**:
- Feature implementation complete (all tasks `[x]` in `tasks.md`)
- `vault/` exists with `lessons/`, `context/` directories
- graphify available (`which graphify`)

**When**: Developer runs `spek post` and then invokes `/spek.post` in the AI session

**Then**:
- [ ] AI prompts for developer reflection using `[spek] ❓` format
- [ ] `vault/lessons/YYYY-MM-DD-<feature-slug>.md` created with full schema
- [ ] `vault/context/patterns.md` updated (new entry appended)
- [ ] `vault/context/decisions.md` updated (new entry appended)
- [ ] `vault/graph/` updated via graphify incremental run
- [ ] `workflow-state.json` fields set: `postflight.lessons_written: true`, `postflight.graph_refreshed: true`
- [ ] Total wall-clock time ≤ 3 minutes (excluding developer thinking time)
- [ ] Exit code 0

**Evidence**:
```bash
time spek post  # shell portion only
ls -la vault/lessons/
tail -5 vault/context/patterns.md
tail -5 vault/context/decisions.md
jq .postflight .spekificity/workflow-state.json
```

---

## Test Scenario 2: `--no-lessons` flag

**Given**: Feature complete

**When**: Run `spek post --no-lessons` and invoke `/spek.post`

**Then**:
- [ ] AI session output contains: `[spek] ⚠ --no-lessons set — skipping lesson capture`
- [ ] No new file created in `vault/lessons/`
- [ ] Graph refresh still runs (unless `--no-graph` also set)

**Evidence**:
```bash
COUNT_BEFORE=$(ls vault/lessons/ | wc -l)
spek post --no-lessons
COUNT_AFTER=$(ls vault/lessons/ | wc -l)
[ "$COUNT_BEFORE" -eq "$COUNT_AFTER" ] && echo "PASS: no new lesson file" || echo "FAIL"
```

---

## Test Scenario 3: `--no-graph` flag

**Given**: Feature complete

**When**: Run `spek post --no-graph` and invoke `/spek.post`

**Then**:
- [ ] AI session output contains: `[spek] ⚠ --no-graph set — skipping graph refresh`
- [ ] `vault/graph/` modification time unchanged
- [ ] Lessons still written (unless `--no-lessons` also set)

**Evidence**:
```bash
MTIME_BEFORE=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
spek post --no-graph
MTIME_AFTER=$(stat -f %m vault/graph/index.md 2>/dev/null || stat -c %Y vault/graph/index.md)
[ "$MTIME_BEFORE" -eq "$MTIME_AFTER" ] && echo "PASS: graph unchanged" || echo "FAIL"
```

---

## Test Scenario 4: Duplicate lessons — append-on-collision

**Given**: `vault/lessons/YYYY-MM-DD-<slug>.md` already exists from a previous run

**When**: `/spek.post` writes lessons for the same feature on the same date

**Then**:
- [ ] New file created as `YYYY-MM-DD-<slug>-v2.md` (not overwriting existing)
- [ ] Both files exist in `vault/lessons/`

**Evidence**:
```bash
ls vault/lessons/ | grep <slug>
```
