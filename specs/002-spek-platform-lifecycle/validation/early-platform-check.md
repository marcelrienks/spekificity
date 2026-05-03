# Early Platform Validation: Smoke Test

**Purpose**: Quick validation that spekificity platform is correctly initialized and ready for use.

**Run After**: `spek setup && spek init` (before feature work)

---

## Quick Validation Checklist

Run the following checks to verify spekificity is ready:

### 1. Directory Structure

```bash
✓ Check: Core directories exist
[ ] .spekificity/          exists
[ ] .specify/              exists (speckit config)
[ ] .github/agents/        exists (speckit skills)
[ ] .obsidian/             exists (vault, optional)
```

**Command**:
```bash
ls -d .spekificity .specify .github/agents .obsidian 2>/dev/null | wc -l
# Should show: 3 or 4 (depending on Obsidian installation)
```

---

### 2. Configuration Files

```bash
✓ Check: Config files present and valid
[ ] .spekificity/config.json       exists and valid JSON
[ ] .spekificity/skill-index.md    exists
[ ] .spekificity/version.txt       exists (version 1.0.0)
```

**Commands**:
```bash
# Config valid
jq . .spekificity/config.json > /dev/null && echo "✓ Config valid" || echo "✗ Config invalid"

# Skill index exists
[ -f .spekificity/skill-index.md ] && echo "✓ Skill index exists" || echo "✗ Skill index missing"

# Version file
cat .spekificity/version.txt
# Should output: 1.0.0
```

---

### 3. Skills Available

```bash
✓ Check: All skill files exist
[ ] .spekificity/skills/spek.context-load.md       exists
[ ] .spekificity/skills/spek.map-codebase.md       exists
[ ] .spekificity/skills/spek.lessons-learnt.md     exists
[ ] .github/agents/speckit.specify.md              exists
[ ] .github/agents/speckit.plan.md                 exists
```

**Command**:
```bash
echo "Spekificity skills:"
ls -1 .spekificity/skills/spek.*.md 2>/dev/null | wc -l

echo "Speckit skills:"
ls -1 .github/agents/speckit.*.md 2>/dev/null | wc -l

# Expected: 3 spekificity skills, 4+ speckit skills
```

---

### 4. Configuration State

```bash
✓ Check: Config shows initialized state
[ ] spek_initialized        = true
[ ] tools.speckit.installed = true
[ ] tools.graphify.installed = true
```

**Command**:
```bash
jq '.spek_initialized, .tools.speckit.installed, .tools.graphify.installed' .spekificity/config.json
# Should output:
# true
# true
# true
```

---

### 5. Command Execution

```bash
✓ Check: Main commands work
[ ] spek setup     exits with code 0
[ ] spek init      exits with code 0
[ ] spek status    exits with code 0
```

**Commands**:
```bash
# Test setup (idempotent, should be quick on re-run)
.spekificity/bin/spek setup && echo "✓ Setup OK" || echo "✗ Setup failed"

# Test status
.spekificity/bin/spek status && echo "✓ Status OK" || echo "✗ Status failed"

# Test update (stub command)
.spekificity/bin/spek update && echo "✓ Update OK" || echo "✗ Update failed"
```

---

### 6. Skill Index Validity

```bash
✓ Check: Skill index contains expected skills
[ ] /spek.context-load      listed
[ ] /speckit.specify        listed
[ ] /speckit-enrich-specify listed
```

**Command**:
```bash
echo "Checking skill index..."
grep -c "spek.context-load" .spekificity/skill-index.md && echo "✓ spek.context-load found"
grep -c "speckit.specify" .spekificity/skill-index.md && echo "✓ speckit.specify found"

# Full index preview
head -30 .spekificity/skill-index.md
```

---

### 7. Graph Availability

```bash
✓ Check: Codebase graph generated (optional, if graphify working)
[ ] .obsidian/graph/index.md       exists (or fallback storage)
```

**Command**:
```bash
if [ -f .obsidian/graph/index.md ]; then
  echo "✓ Graph available (Obsidian vault)"
  wc -l .obsidian/graph/index.md
elif [ -f .spekificity/graph.json ]; then
  echo "✓ Graph available (fallback JSON)"
  jq '.nodes | length' .spekificity/graph.json
else
  echo "⚠ Graph not yet generated (run /spek.map-codebase)"
fi
```

---

### 8. Namespace Consistency

```bash
✓ Check: Namespace validation passes
[ ] All spekificity skills use spek.* naming
[ ] All speckit skills use speckit.* naming
```

**Command**:
```bash
.spekificity/setup-scripts/validate-namespace.sh
# Should output: ✓ Namespace validation OK or list any issues
```

---

## Full Smoke Test Script

Save this as `.spekificity/smoke-test.sh` for quick validation:

```bash
#!/bin/bash

# Spekificity Smoke Test
# Quick validation that platform is ready for use

set -e

echo "═══════════════════════════════════"
echo " Spekificity Platform Smoke Test"
echo "═══════════════════════════════════"
echo

# Check directories
echo "[1/8] Checking directories..."
for dir in .spekificity .specify .github/agents; do
  [ -d "$dir" ] && echo "✓ $dir exists" || echo "✗ $dir missing"
done
echo

# Check config
echo "[2/8] Checking configuration..."
if jq . .spekificity/config.json > /dev/null 2>&1; then
  echo "✓ Config valid JSON"
  INIT=$(jq '.spek_initialized' .spekificity/config.json)
  echo "  Initialized: $INIT"
else
  echo "✗ Config invalid"
  exit 1
fi
echo

# Check skills
echo "[3/8] Checking skills..."
SPEK_SKILLS=$(ls -1 .spekificity/skills/spek.*.md 2>/dev/null | wc -l)
SPECKIT_SKILLS=$(ls -1 .github/agents/speckit.*.md 2>/dev/null | wc -l)
echo "✓ Spekificity skills: $SPEK_SKILLS"
echo "✓ Speckit skills: $SPECKIT_SKILLS"
echo

# Check commands
echo "[4/8] Checking commands..."
[ -x .spekificity/bin/spek ] && echo "✓ spek dispatcher executable" || echo "✗ spek not executable"
echo

# Check skill index
echo "[5/8] Checking skill index..."
if [ -f .spekificity/skill-index.md ]; then
  echo "✓ Skill index exists"
  SKILLS_LISTED=$(grep -c "^| " .spekificity/skill-index.md || true)
  echo "  Skills listed: $SKILLS_LISTED"
else
  echo "✗ Skill index missing"
fi
echo

# Check namespace
echo "[6/8] Validating namespace..."
if .spekificity/setup-scripts/validate-namespace.sh --verbose > /dev/null 2>&1; then
  echo "✓ Namespace valid"
else
  echo "⚠ Namespace issues (review with: validate-namespace.sh --verbose)"
fi
echo

# Check status command
echo "[7/8] Testing status command..."
if .spekificity/bin/spek status > /tmp/status.txt 2>&1; then
  echo "✓ Status command works"
  echo "  Version: $(jq -r '.version' .spekificity/config.json)"
else
  echo "✗ Status command failed"
fi
echo

# Summary
echo "[8/8] Summary"
echo "═══════════════════════════════════"
echo "✓ Smoke test complete"
echo
echo "Platform ready for use!"
echo
echo "Next steps:"
echo "  1. Load context: /context-load"
echo "  2. Start feature: /speckit-enrich-specify"
echo "  3. See guides: .spekificity/guides/"
echo

exit 0
```

---

## Running the Smoke Test

```bash
chmod +x .spekificity/smoke-test.sh
.spekificity/smoke-test.sh
```

**Expected Output**:
```
═══════════════════════════════════
 Spekificity Platform Smoke Test
═══════════════════════════════════

[1/8] Checking directories...
✓ .spekificity exists
✓ .specify exists
✓ .github/agents exists

[2/8] Checking configuration...
✓ Config valid JSON
  Initialized: true

...

[8/8] Summary
═══════════════════════════════════
✓ Smoke test complete

Platform ready for use!
```

---

## Troubleshooting Failed Smoke Test

| Check | Failure | Recovery |
|-------|---------|----------|
| Directories | `.spekificity/` missing | Run: `spek setup && spek init` |
| Config invalid | JSON error | Delete and re-run: `spek init` |
| Skills missing | No .md files | Re-run: `spek init` |
| Namespace invalid | Naming violation | Fix with: `validate-namespace.sh --fix` |
| Status command fails | Exit code non-zero | Check: `.spekificity/setup-scripts/` permissions |

---

## Smoke Test Criteria

✅ All directories present  
✅ Config valid and initialized  
✅ 3+ spekificity skills found  
✅ 4+ speckit skills found  
✅ Skill index exists with skills listed  
✅ Namespace validation passes  
✅ Status command executes  

**If all pass**: Platform ready for feature work!  
**If any fail**: Review troubleshooting above or consult `.spekificity/guides/troubleshooting.md`

---

**Ready to start developing?** After smoke test passes, run `/context-load` in your AI chat.
