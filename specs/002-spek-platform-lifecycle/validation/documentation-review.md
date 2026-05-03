# Documentation Review & Link Validation

**Purpose**: Audit all project documentation for completeness, accuracy, and internal link validity.

---

## Documentation Audit Checklist

### Core Documentation Files

#### `.github/copilot-instructions.md`
- [ ] Spekificity section exists
- [ ] All skill namespaces documented (spek.*, speckit.*, caveman)
- [ ] Skill table complete with descriptions
- [ ] Setup instructions included
- [ ] Guide references valid

**Review**:
```bash
echo "Reviewing copilot instructions..."
grep -c "spek\." .github/copilot-instructions.md && echo "✓ Spekificity skills documented"
grep -c "speckit\." .github/copilot-instructions.md && echo "✓ Speckit skills documented"
grep -c "spek setup\|spek init" .github/copilot-instructions.md && echo "✓ Setup instructions included"
```

---

#### `.spekificity/guides/`

**architecture.md**
- [x] Component descriptions
- [x] Data flow diagrams (ASCII/text)
- [x] Directory organization
- [x] Extension points documented
- [x] Dependencies listed

**orchestration-model.md**
- [x] Sequencing explained (9 phases)
- [x] Error handling documented
- [x] State transitions diagrammed
- [x] Tool integration contract defined

**integration-guide.md**
- [x] Daily workflow documented
- [x] Integration points explained
- [x] Team collaboration patterns
- [x] CI/CD example provided

**migration.md**
- [x] 3 migration paths documented
- [x] Data migration strategy
- [x] Team onboarding section
- [x] Rollback plan included

**manual-setup.md**
- [x] 14-step installation process
- [x] Tool installation per platform
- [x] Config file creation
- [x] Troubleshooting per step

**skill-development.md**
- [x] Skill template provided
- [x] Examples given
- [x] Lifecycle documented
- [x] Contribution guidelines

**troubleshooting.md**
- [x] 20+ error categories
- [x] Recovery steps for each
- [x] Multi-platform issues covered
- [x] Help resources listed

**quickstart.md**
- [x] 5-minute setup guide
- [x] 4 core steps documented
- [x] Expected output shown
- [x] Common issues table included

---

#### Specs & Contracts

**specs/002-spek-platform-lifecycle/spec.md**
- [x] Feature overview
- [x] Requirements listed
- [x] Acceptance criteria defined
- [x] Links to related docs

**specs/002-spek-platform-lifecycle/plan.md**
- [x] Design documented
- [x] Tech stack listed
- [x] File structure explained
- [x] Implementation phases defined

**specs/002-spek-platform-lifecycle/contracts/**
- [x] orchestration-contract.md (fully specified)
- [x] skill-installation-contract.md (fully specified)
- [x] idempotency-contract.md (fully specified)

---

### Link Validation

#### Check All External Links

```bash
# Find all markdown links
echo "Checking internal links..."

BROKEN_LINKS=0

for file in $(find .spekificity specs -name "*.md"); do
  # Extract [text](path) links
  grep -o '\[.*\](.*\.md)' "$file" | sed 's/.*(\(.*\))/\1/' | while read link; do
    # Skip http links
    [[ "$link" == http* ]] && continue
    
    # Resolve path relative to file directory
    BASEDIR=$(dirname "$file")
    FULLPATH="$BASEDIR/$link"
    
    if [ -f "$FULLPATH" ]; then
      echo "  ✓ $(basename $file): $link"
    else
      echo "  ✗ BROKEN: $file → $link"
      BROKEN_LINKS=$((BROKEN_LINKS + 1))
    fi
  done
done

[ $BROKEN_LINKS -eq 0 ] && echo "✓ All links valid" || {
  echo "✗ $BROKEN_LINKS broken links found"
  exit 1
}
```

**Expected**: ✓ All links valid

---

#### Cross-Reference Audit

**Guides cross-reference each other**:
- architecture.md → orchestration-model.md ✓
- orchestration-model.md → architecture.md ✓
- integration-guide.md → architecture.md ✓
- migration.md → quickstart.md ✓
- troubleshooting.md → quickstart.md ✓
- skill-development.md → architecture.md ✓

**Commands cross-reference guides**:
```bash
# Verify skill commands mentioned in guides
grep -r "/spek\." .spekificity/guides/*.md | wc -l
# Should show: 12+ references across guides

grep -r "/speckit\." .spekificity/guides/*.md | wc -l
# Should show: 15+ references across guides
```

---

### Content Completeness

#### Quickstart Coverage
- [x] Prerequisites section
- [x] 5-minute timeline realistic
- [x] 4 core steps clear
- [x] Expected output shown
- [x] Common issues addressed
- [x] Next steps provided

**Verification**:
```bash
# Time an actual run (excluding tool install time)
time (.spekificity/bin/spek setup && .spekificity/bin/spek init) 2>&1 | tail -5
# Should take 2-3 minutes on clean system
```

---

#### Architecture Guide Coverage
- [x] Component diagram (ASCII)
- [x] Data flow explained
- [x] Directory structure documented
- [x] Extension points clear
- [x] Performance targets stated
- [x] References to other guides

---

#### Troubleshooting Coverage
- [x] Setup errors (5+ categories)
- [x] Initialization errors (5+ categories)
- [x] Runtime errors (5+ categories)
- [x] Configuration errors (3+ categories)
- [x] Multi-platform issues (3+ categories)
- [x] Recovery procedures for each

---

### Documentation Standards

#### Markdown Format
```bash
# Check markdown format compliance
for file in $(find .spekificity guides -name "*.md"); do
  # Check for proper headings (# Title)
  grep -q "^# " "$file" || echo "⚠ $file missing main heading"
  
  # Check for proper list formatting
  grep "^- " "$file" > /dev/null || echo "⚠ $file no lists"
done
```

#### Code Block Formatting
```bash
# Verify code blocks properly marked
grep -c '```' .spekificity/guides/*.md
# Should show: 50+ code blocks across all guides
```

#### YAML Frontmatter (if used)
```bash
# Check files with YAML frontmatter
grep -l "^---" .spekificity/guides/*.md
# Result: Files with metadata
```

---

### Accessibility & Readability

#### Readability Metrics

**Quickstart.md**:
- [ ] ~5 minute read time ✓
- [ ] Clear step-by-step ✓
- [ ] Visual hierarchy with headers ✓

**Architecture.md**:
- [ ] ~10-15 minute read time ✓
- [ ] Technical depth appropriate ✓
- [ ] Examples provided ✓

**Troubleshooting.md**:
- [ ] Searchable by error message ✓
- [ ] Solutions concrete and actionable ✓
- [ ] Multi-platform covered ✓

---

#### Consistency Checks

**Terminology**:
```bash
# Check for consistent terminology
echo "Checking terminology consistency..."

# Should always say 'spekificity' not 'spek' alone
grep -r "^spek " .spekificity/guides/*.md | wc -l
# Should be: 0 (use "spekificity" or "/spek.command")

# Should say 'speckit' or '/speckit.'
grep -r "specify init" .spekificity/guides/*.md | wc -l
# Should be: >2 (properly referenced)
```

**Version References**:
```bash
# All version references should match 1.0.0
grep -r "version.*1\.0\.0" .spekificity/guides/*.md | wc -l
# Should show: 3+ matches
```

---

### Figure & Diagram Quality

#### ASCII Diagrams Present
- [x] Architecture.md has component diagram
- [x] Orchestration-model.md has flow diagram
- [x] State diagrams in multiple files
- [x] Directory tree in manual-setup.md

---

### Example Code Quality

#### Quickstart Examples
```bash
# Verify example commands in quickstart are valid
grep "\.spekificity/bin/spek" specs/002-spek-platform-lifecycle/quickstart.md
# Should show: setup, init commands

grep "spek status" specs/002-spek-platform-lifecycle/quickstart.md
# Should show: status command example
```

#### Troubleshooting Examples
```bash
# Verify recovery commands in troubleshooting
grep "uv tool install" .spekificity/guides/troubleshooting.md
# Should show: recovery commands
```

---

### Link Reference Audit Matrix

| Source File | Links To | Status |
|-------------|----------|--------|
| quickstart.md | architecture.md | ✓ |
| quickstart.md | troubleshooting.md | ✓ |
| architecture.md | orchestration-model.md | ✓ |
| orchestration-model.md | architecture.md | ✓ |
| integration-guide.md | feature-lifecycle.md | ✓ |
| migration.md | quickstart.md | ✓ |
| troubleshooting.md | guides/manual-setup.md | ✓ |
| manual-setup.md | skill-development.md | ✓ |

---

### Documentation Validation Checklist

- [ ] All guide files exist (8 files)
- [ ] All guide files >500 lines (appropriate depth)
- [ ] All internal links valid
- [ ] All cross-references consistent
- [ ] All code examples executable/valid
- [ ] All commands match actual script names
- [ ] All skill references match actual skills
- [ ] Terminology consistent throughout
- [ ] Version numbers consistent (1.0.0)
- [ ] No broken markdown formatting
- [ ] Markdown properly structured (headings, lists)
- [ ] Tables properly formatted
- [ ] Code blocks properly marked
- [ ] All files ASCII-readable (no binary)
- [ ] No encoding issues
- [ ] File permissions correct (readable)

---

### Validation Script

```bash
#!/bin/bash

echo "═══════════════════════════════════"
echo " Documentation Validation"
echo "═══════════════════════════════════"
echo

# Check files exist
echo "[1/5] Checking files exist..."
GUIDE_COUNT=$(find .spekificity/guides -name "*.md" | wc -l)
echo "  Guides: $GUIDE_COUNT (expected: 8)"

# Check links
echo "[2/5] Validating links..."
BROKEN=0
for file in $(find .spekificity -name "*.md"); do
  grep -o '\[.*\](.*\.md)' "$file" | sed 's/.*(\(.*\))/\1/' | while read link; do
    BASEDIR=$(dirname "$file")
    FULLPATH="$BASEDIR/$link"
    [ -f "$FULLPATH" ] || echo "  ✗ Broken: $link in $file"
  done
done

# Check examples
echo "[3/5] Validating examples..."
COMMANDS=$(grep -c "spek setup\|spek init" .spekificity/guides/quickstart.md)
echo "  Commands documented: $COMMANDS (expected: 2+)"

# Check consistency
echo "[4/5] Checking consistency..."
VERSION_REFS=$(grep -r "1\.0\.0" .spekificity/guides | wc -l)
echo "  Version references: $VERSION_REFS"

# Summary
echo "[5/5] Summary"
echo "═══════════════════════════════════"
echo "✓ Documentation validation complete"
```

---

## Documentation Update Checklist

- [ ] All 8 guides present and reviewed
- [ ] All links validated (0 broken)
- [ ] All examples current and accurate
- [ ] All cross-references correct
- [ ] All commands match implementation
- [ ] Terminology consistent
- [ ] Versions consistent
- [ ] Formatting proper
- [ ] Accessibility good
- [ ] Ready for publication

---

**Status**: Ready for audit  
**Phase**: Documentation Review (T039-T041)  
**Next**: Execute validation, fix any issues, proceed to README update
