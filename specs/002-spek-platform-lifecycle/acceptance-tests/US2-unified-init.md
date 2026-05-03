# Acceptance Tests: US2 — Unified Spekificity Initialization

**Feature**: US2: Unified spekificity initialization — `spek init` orchestration  
**Test Date**: 2026-05-03  
**Tester**: [AI Agent / Developer]

## Test Scenarios

### Scenario 1: Fresh project initialization (clean machine)

**Given**: Prerequisites installed, no `.spekificity/` directory

**When**: Run `spek init`

**Then**:
- [ ] `.spekificity/config.json` created with `spek_initialized = false` initially, then `true` on completion
- [ ] `.spekificity/skill-index.md` generated with all registered skills
- [ ] `.github/agents/` populated with speckit skills via `specify init`
- [ ] `.spekificity/skills/` populated with spek.* custom skills
- [ ] `.spekificity/workflows/` populated with init/setup/update/integration docs
- [ ] `.spekificity/guides/` populated with architecture/orchestration/skill-dev guides
- [ ] Exit code 0 (success)

**Evidence**:
```bash
ls -la .spekificity/
file .spekificity/config.json
jq .spek_initialized .spekificity/config.json
ls .spekificity/skills/ | grep spek.
```

---

### Scenario 2: Idempotent re-run (already initialized)

**Given**: `spek init` previously ran successfully, config has `spek_initialized = true`

**When**: Run `spek init` again

**Then**:
- [ ] Config state is preserved (no reset)
- [ ] Existing skill files are updated (not deleted)
- [ ] Tool integration status recorded without destroying state
- [ ] No errors or failures
- [ ] Summary shows "idempotent mode: updating state"
- [ ] Exit code 0

**Evidence**:
```bash
git diff .spekificity/config.json  # Check for preservation
jq .orchestration_history .spekificity/config.json | tail -5
```

---

### Scenario 3: Speckit skill invocation

**Given**: `spek init` completed successfully

**When**: AI agent runs `/speckit.specify` command

**Then**:
- [ ] Command is recognized and available
- [ ] Speckit initialize without errors
- [ ] `.specify/` directory structure created/verified
- [ ] Skill-index.md lists speckit skills correctly

**Evidence**:
```bash
ls .github/agents/ | grep speckit
file .specify/constitution.md  # verify speckit ran
```

---

### Scenario 4: Spekificity skill invocation

**Given**: `spek init` completed successfully

**When**: AI agent runs `/spek.context-load` command

**Then**:
- [ ] Command is recognized and available
- [ ] Vault context loads (if vault exists)
- [ ] Skill executes without errors
- [ ] Returns proper exit code

**Evidence**:
```bash
ls .spekificity/skills/ | grep spek.context-load
cat .spekificity/skill-index.md | grep context-load
```

---

### Scenario 5: Caveman skill optional availability

**Given**: `spek init` completed (caveman may or may not be installed)

**When**: Check caveman integration status

**Then**:
- [ ] Config records caveman availability (`true` if available, `false` otherwise)
- [ ] If available, caveman skill is usable
- [ ] If not available, project still fully functional (optional)
- [ ] No errors from missing caveman

**Evidence**:
```bash
jq .tools.caveman .spekificity/config.json
```

---

### Scenario 6: Obsidian optional (skip flag)

**Given**: Prerequisites installed

**When**: Run `spek init --skip-obsidian`

**Then**:
- [ ] Obsidian setup is skipped
- [ ] Project fully functional without Obsidian
- [ ] Config records `obsidian.initialized = false`
- [ ] Graphify fallback storage works
- [ ] Exit code 0

**Evidence**:
```bash
spek init --skip-obsidian
jq .tools.obsidian .spekificity/config.json
```

---

### Scenario 7: Partial failure recovery

**Given**: `spek init` started but interrupted mid-way (e.g., network error at step 3/7)

**When**: Run `spek init` again

**Then**:
- [ ] Partial failure detected from history
- [ ] Recovery guidance provided
- [ ] Initialization resumes (or completes cleanly on retry)
- [ ] Config remains valid
- [ ] Exit code 0 or clear error message

**Evidence**:
```bash
jq .orchestration_history .spekificity/config.json | grep failure
```

---

## Acceptance Criteria Summary

✅ **All scenarios pass** if:
1. Fresh init completes with correct file structure
2. Idempotent re-run preserves state
3. All skills (speckit, spekificity, caveman) are discoverable and functional
4. Optional tools (Obsidian, caveman) don't block initialization
5. Partial failures can be recovered or re-run safely

---

## Test Results

| Scenario | Status | Notes |
|----------|--------|-------|
| 1. Fresh init | [  ] PASS [  ] FAIL | |
| 2. Idempotent | [  ] PASS [  ] FAIL | |
| 3. Speckit skill | [  ] PASS [  ] FAIL | |
| 4. Spek skill | [  ] PASS [  ] FAIL | |
| 5. Caveman optional | [  ] PASS [  ] FAIL | |
| 6. Obsidian optional | [  ] PASS [  ] FAIL | |
| 7. Failure recovery | [  ] PASS [  ] FAIL | |

**Overall Result**: [  ] PASS — US2 ready for merge [  ] FAIL — Blockers found

**Blockers** (if any):
- 

**Next**: Move to T036 (end-to-end testing) or address blockers.
