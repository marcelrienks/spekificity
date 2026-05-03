# Contract: Skill Installation & Discovery

**Version**: 1.0.0  
**Namespace**: spekificity-skills  
**Status**: Active

## Purpose

Define contract for skill discovery, installation, indexing, and invocation in spekificity.

---

## Skill File Format

All skills are markdown files following this structure:

```markdown
# Skill: [Readable Name]

**Command**: `/namespace.skill-name`
**Namespace**: `namespace.*`
**Version**: 1.0.0
**Status**: active | experimental

## Description
[One sentence describing what the skill does]

## Prerequisites
[What must be true for skill to work]

## Usage
[How to invoke]

## Implementation
[What the skill does]

## Error Handling
[How errors are handled]
```

### Naming Convention

**Spekificity Skills**:
- File: `.spekificity/skills/spek.<name>.md`
- Command: `/spek.<name>`
- Example: `/spek.context-load`

**Speckit Skills**:
- File: `.github/agents/speckit.<name>.md`
- Command: `/speckit.<name>`
- Example: `/speckit.specify`

**System Skills** (caveman, etc.):
- Command: `/<name>`
- Example: `/caveman`

---

## Function: `discover_spekificity_skills()`

### Contract

```bash
discover_spekificity_skills() -> array<skill_info>
```

### Behavior

1. **Scan**: `.spekificity/skills/spek.*.md`
2. **Parse**: Extract metadata from skill files
   - Command name
   - Description
   - Version
   - Status

3. **Return**: Array of skill info objects

```bash
[
  {
    "namespace": "spek",
    "command": "spek.context-load",
    "file": ".spekificity/skills/spek.context-load.md",
    "version": "1.0.0",
    "status": "active"
  },
  ...
]
```

### Error Handling

- If skill file malformed → Log warning, skip skill
- If directory missing → Return empty array

---

## Function: `discover_speckit_skills()`

### Contract

```bash
discover_speckit_skills() -> array<skill_info>
```

### Behavior

1. **Scan**: `.github/agents/speckit.*.md`
2. **Parse**: Extract metadata
3. **Return**: Array of speckit skill info

```bash
[
  {
    "namespace": "speckit",
    "command": "speckit.specify",
    "file": ".github/agents/speckit.specify.md",
    "version": "0.1.0",
    "status": "active"
  },
  ...
]
```

---

## Function: `check_caveman_availability()`

### Contract

```bash
check_caveman_availability() -> object
```

### Behavior

1. **Check**: Is caveman command available in environment?
2. **Return**: Availability status

```bash
{
  "available": true/false,
  "version": "1.0.0" | null,
  "command": "/caveman"
}
```

---

## Function: `generate_skill_index()`

### Contract

```bash
generate_skill_index() -> file_written
```

### Behavior

1. **Discover**: All skills (spekificity, speckit, caveman)
2. **Merge**: Combine into unified index
3. **Format**: Markdown table
4. **Write**: `.spekificity/skill-index.md`

### Output Format

```markdown
# Spekificity Unified Skill Index

**Last Updated**: 2026-05-03

## Spekificity Custom Skills

| Namespace | Command | Description | Status |
|-----------|---------|-------------|--------|
| spek | `/spek.context-load` | Load vault context | active |
| ... |

## Speckit Skills

| Namespace | Command | Description | Status |
|-----------|---------|-------------|--------|
| speckit | `/speckit.specify` | Create feature spec | active |
| ... |

## Optional Skills

| Namespace | Command | Description | Status |
|-----------|---------|-------------|--------|
| caveman | `/caveman` | Token compression | available |
```

### Error Handling

- If directory missing → Create `.spekificity/` first
- If no skills found → Generate empty index with headers

---

## Function: `install_spek_skills()`

### Contract

```bash
install_spek_skills() -> array<file_path>
```

### Behavior

1. **Create**: `.spekificity/skills/` directory
2. **Install**: Standard spekificity skills:
   - `spek.context-load.md`
   - `spek.map-codebase.md`
   - `spek.lessons-learnt.md`
3. **Return**: Array of installed file paths

```bash
[
  ".spekificity/skills/spek.context-load.md",
  ".spekificity/skills/spek.map-codebase.md",
  ".spekificity/skills/spek.lessons-learnt.md"
]
```

### Error Handling

- If file already exists → Skip (idempotent)
- If write permission denied → Log error, halt

---

## Skill Invocation Contract

When AI agent invokes skill command (e.g., `/spek.context-load`):

### Requirements

1. **Discovery**: Skill name must be in skill index
2. **File Exists**: Corresponding `.md` file must exist
3. **Format**: File must be valid markdown with skill structure
4. **Execution**: Skill implementation must complete without error

### Invocation Flow

```
/spek.context-load
    ↓
    Skill discovered in skill-index.md
    ↓
    Find file: .spekificity/skills/spek.context-load.md
    ↓
    Read and parse skill markdown
    ↓
    Execute skill implementation
    ↓
    Return output to AI (markdown formatted)
    ↓
    AI processes result
```

---

## Skill Lifecycle

### State: Discovered

**When**: Skill file exists in correct location with correct naming

```bash
.spekificity/skills/spek.my-skill.md
```

**Actions**:
- Discoverable by `discover_spekificity_skills()`
- Appears in unified index

### State: Active

**When**: Skill is enabled and invocable

```json
{
  "status": "active",
  "available": true
}
```

**Actions**:
- AI can invoke via `/spek.my-skill`
- Included in help and documentation

### State: Experimental

**When**: Skill is under development or testing

```json
{
  "status": "experimental",
  "available": true
}
```

**Actions**:
- AI can invoke, but marked as experimental
- Users warned of potential instability

### State: Deprecated

**When**: Skill is being phased out

```json
{
  "status": "deprecated",
  "available": false,
  "replacement": "/spek.new-skill"
}
```

**Actions**:
- Not discovered in active index
- Users directed to replacement

---

## Skill Index Persistence

### Update Triggers

1. **After `spek init`**: Index automatically regenerated
2. **After `spek update`**: Index updated if skills changed
3. **Manual**: `spek.setup-scripts/skill-discovery.sh generate_skill_index`

### Storage Location

```
.spekificity/skill-index.md
```

### Validation

```bash
# Verify index is current
grep "spek.context-load" .spekificity/skill-index.md

# Regenerate if missing
.spekificity/setup-scripts/skill-discovery.sh generate_skill_index
```

---

## Skill Namespace Enforcement

**Spekificity Namespace** (`spek.*`):
- Files: `.spekificity/skills/spek.*.md`
- Commands: `/spek.*`
- Config keys: `spek_*`, `spek.*`

**Speckit Namespace** (`speckit.*`):
- Files: `.github/agents/speckit.*.md`
- Commands: `/speckit.*`

**Validation** (in `validate-namespace.sh`):
- All `.spekificity/skills/` files match `spek.*.md`
- All `.github/agents/` files match `speckit.*.md`
- Config keys follow naming convention
- Auto-fix available via `--fix` flag

---

## Skill Discovery Data Structure

### Skill Info Object

```json
{
  "namespace": "spek",
  "command": "spek.context-load",
  "file": ".spekificity/skills/spek.context-load.md",
  "description": "Load vault context and graph",
  "version": "1.0.0",
  "status": "active",
  "prerequisites": [
    ".obsidian/graph/index.md exists",
    "spekificity initialized"
  ]
}
```

### Unified Index Data Structure

```json
{
  "generated_at": "2026-05-03T15:40:00Z",
  "total_skills": 7,
  "skills_by_namespace": {
    "spek": [ <skill_info>, ... ],
    "speckit": [ <skill_info>, ... ],
    "caveman": [ <skill_info>, ... ]
  },
  "all_skills": [ <skill_info>, ... ]
}
```

---

## Testing Criteria

- ✅ Skill discovery finds all `.spekificity/skills/spek.*.md` files
- ✅ Skill index generated with correct format and content
- ✅ Namespace validation enforces naming convention
- ✅ Skill invocation resolves correct file
- ✅ Index update is idempotent (re-run same result)
- ✅ All skills appear in AI chat interface
- ✅ Invalid skill files handled gracefully (skipped with warning)

---

## Dependencies

- `logging.sh`: Log discovery and validation
- `config-handler.sh`: Record skill installation state
- `validate-namespace.sh`: Enforce naming convention

---

**Status**: Ready for implementation  
**Last Updated**: 2026-05-03
