---
title: "Zettelkasten Conventions for Vault Notes"
status: "Specification"
version: "1.0.0-alpha.1"
date: "2026-05-20"
priority: "High"
---

# C.3.1 Zettelkasten Conventions for Vault Notes

**Status:** Specification   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Priority:** High (Phase 1 recommended)  
**Effort:** 3-4 hours  
**Adoption Source:** B.9 (claude-code-memory-setup, production-validated)

---

## Purpose

Define and enforce Zettelkasten conventions for all vault notes (decisions, patterns, lessons) to enable:
- Atomic, self-contained notes (one concept per file)
- Searchable metadata via frontmatter (title, tags, created, updated, status, type)
- Dense interconnection via wikilinks (minimum 2 per note)
- Knowledge graph navigation in Obsidian
- Future discoverability via `/spek.context` loads

---

## Scope & Relationships

**What this spec covers:**
- YAML frontmatter schema for all vault notes
- Filename conventions (kebab-case)
- Minimum wikilink density requirements
- Note atomicity principles
- Frontmatter validation rules

**What this spec does NOT cover:**
- Content generation for lessons (see C.3.2 Auto-tagging)
- Vault directory structure (see B.8.2 Persistent Memories)
- Graph query patterns (see B.11 Codegraph Setup)

**Related specs:**
- C.3.2: Auto-tagging + auto-wikilink (uses frontmatter schema)
- C.3.5: Session logs as vault artifacts (applies Zettelkasten format)
- B.8.2: Persistent memories (vault architecture)

---

## Zettelkasten Schema


### Recommended YAML Frontmatter

All vault notes should include frontmatter with these fields to enable tooling and automation. Projects can adopt this progressively; tooling will function with partial metadata but automation (auto-tagging, graph exports, and reliable context extraction) works best when frontmatter is present.

```yaml
---
title: "<note-title>"
type: "<decision|pattern|lesson|guide>"
tags: ["<domain>", "<methodology>", "<tech-stack>"]
status: "<active|deprecated|superseded>"
created: "<YYYY-MM-DD>"
updated: "<YYYY-MM-DD>"
source: "<feature-name|external-link|manual>"
related: ["[[note-name]]", "[[other-note]]"]
---
```

**Field Definitions:**

| Field | Required | Type | Description | Example |
|-------|----------|------|-------------|---------|
| `title` | YES | string | Concise, unique note title | "Singleton Pattern for Service Management" |
| `type` | YES | enum | Classification: decision, pattern, lesson, guide | "pattern" |
| `tags` | YES | array | 2-5 tags for searchability + organization | ["pattern/singleton", "architecture", "service-layer"] |
| `status` | YES | enum | active, deprecated, superseded, archived | "active" |
| `created` | YES | date | ISO 8601 creation date | "2026-05-10" |
| `updated` | YES | date | ISO 8601 last update date | "2026-05-19" |
| `source` | NO | string | Origin: feature name, external link, manual entry | "feature-auth-refactor" |
| `related` | NO | array | Wikilinks to related vault entries | ["[[dependency-injection]]", "[[service-patterns]]"] |

### Filename Convention

**Format:** `<kebab-case-title>.md`

- **Rules:**
- Use lowercase letters, numbers, hyphens only
- Maximum 50 characters (including extension)
 - Should be globally unique within `wiki/vault/` directory
- Spaces → hyphens: "Singleton Pattern" → `singleton-pattern.md`
- Abbreviations OK: "DI Pattern" → `di-pattern.md`

**Examples:**
- ✅ `singleton-pattern.md` (good)
- ✅ `async-error-handling.md` (good)
- ❌ `Singleton Pattern.md` (spaces + capitals)
- ❌ `singleton_pattern_for_services.md` (too long + underscores)

---

## Atomicity Principle

**Definition:** Each vault note addresses ONE clear concept. Reader can understand the note independently without reading related notes (though wikilinks enable deeper discovery).

**Atomicity Checklist:**

- [ ] Note has single, clear title
- [ ] Content focuses on one concept/pattern/decision

## Success Criteria

- ✅ Frontmatter schema enforced (all required fields present)
- ✅ Filename conventions followed (kebab-case, unique, <50 chars)
- ✅ Atomicity maintained (one concept per file)
- ✅ Wikilinks present (minimum 2-3 cross-references per note)
- ✅ Metadata searchable (tags enable discovery)
- ✅ Status tracking accurate (active/deprecated/superseded labels correct)
- ✅ Notes discoverable (grep + Obsidian search working)
- [ ] 300-800 words (concise but complete)
- [ ] Can be understood without reading related notes
- [ ] Wikilinks enhance (don't require) understanding
- [ ] Not a summary of multiple patterns or decisions

**Bad Examples (violates atomicity):**
- "Service Layer Patterns and Error Handling" (two concepts)
- "All Architecture Decisions from 2026" (too broad)

**Good Examples (respects atomicity):**
- "Singleton Pattern for Service Management" (one pattern)
- "Use Dependency Injection over Service Locator" (one decision)
- "Async Error Recovery in Event Loops" (one pattern)

---

## Wikilink Density Requirements

**Minimum density:** 2-4 wikilinks per note (depending on length)

**Guidelines:**

- **Short notes (300-400 words):** Minimum 2 wikilinks
- **Medium notes (400-600 words):** Minimum 3 wikilinks
- **Long notes (600-800 words):** Minimum 4 wikilinks

**Wikilink Types:**

1. **Pattern Links:** `[[singleton-pattern]]` → related patterns
2. **Decision Links:** `[[use-di-over-service-locator]]` → architectural decisions
3. **Tech Links:** `[[react-hooks]]` → technology choices
4. **Domain Links:** `[[state-management]]` → domain concepts

**Wikilink Format:**

```markdown
We decided to use [[dependency-injection]] over service locators 
because [[service-locator-anti-pattern]] violates testability constraints.
```

**Validation Rule:** Every wikilink should reference an existing note in `wiki/vault/` (except external links, which use standard Markdown `[text](url)`).

---

## Vault Note Types

### 1. Decision Notes

**Frontmatter:**
```yaml
type: "decision"
tags: ["decision", "<domain>", "<methodology>"]
status: "active|superseded"
```

**Structure:**
- Title: Starts with action verb ("Use...", "Adopt...", "Reject...")
- Context: Why this decision was needed
- Decision: What was chosen
- Rationale: Why this choice (alternatives considered)
- Consequences: Impact on future work
- Related: Links to enabling patterns, impacted features

**Example:** `use-dependency-injection-pattern.md`

### 2. Pattern Notes

**Frontmatter:**
```yaml
type: "pattern"
tags: ["pattern/<category>", "<tech-stack>", "<domain>"]
status: "active|deprecated"
```

**Structure:**
- Title: Pattern name + category ("Singleton Pattern", "Observer Pattern")
- Problem: What problem does this pattern solve?
- Solution: How does the pattern work?
- Implementation: Code sketch or pseudocode
- When to Use: Constraints, preconditions
- Alternatives: Other patterns that could be used instead
- Related: Links to decisions, other patterns

**Example:** `singleton-pattern.md`, `observer-pattern-events.md`

### 3. Lesson Notes

**Frontmatter:**
```yaml
type: "lesson"
tags: ["lesson/<feature>", "<domain>", "<methodology>"]
status: "active"
source: "<feature-name>"
```

**Structure:**
- Title: "Lessons from [Feature]"
- What We Built: Feature digest (from spec)
- How We Built It: Technical approach (from plan)
- Key Tasks: Major deliverables
- Decisions Made: With rationale
- Patterns Used: Reused + newly discovered
- Lessons for Next: Actionable guidance
- Metrics: LOC, files, coverage, time

**Example:** `lessons-from-auth-refactor.md`

### 4. Guide Notes (Optional)

**Frontmatter:**
```yaml
type: "guide"
tags: ["guide/<topic>", "<domain>"]
status: "active"
```

**Structure:**
- Title: "Guide: [Topic]"
- Purpose: Why this guide exists
- Prerequisites: What readers should know
- Steps: Numbered or bulleted instructions
- Examples: Code or walkthrough examples
- Troubleshooting: Common issues + fixes
- Related: Links to relevant patterns/decisions

**Example:** `guide-vault-conventions.md`, `guide-context-loading.md`

---

## Implementation: /spek.conclude Integration

### Where Zettelkasten Format Applies

**Artifact:** Lesson generation (Step 3 of `/spek.conclude`)

**Current Spec Reference:** B.8.4 Post Command (Step 3: Generate Lessons)

**Enhancement Points:**

1. **Frontmatter Generation** (automatically in `/spek.conclude` Step 3)
   ```
   1. Extract feature name from `vault/session/`
   2. Generate title: "Lessons from [feature]"
   3. Populate frontmatter:
      - type: "lesson"
      - tags: [extract from feature domain + tech stack]
      - status: "active"
      - created: today's date
      - updated: today's date
      - source: feature name
   4. Add default `related` field (will be populated by S2 auto-linking)
   ```

2. **Wikilink Validation** (Step 3, after content generation)
   ```
   1. Count wikilinks in generated lesson
   2. If count < minimum for length:
      - Alert: "Lesson has [N] wikilinks; recommend [M]"
      - Suggest related decisions/patterns to link
   3. Validate all wikilinks reference existing vault notes
   4. Report broken links to user
   ```

3. **Filename Generation** (Step 3, before saving)
   ```
   1. Extract feature name + date
   2. Generate kebab-case filename: "<YYYY-MM-DD>-<feature>-lesson.md"
   3. Verify globally unique within vault/
   4. Save to wiki/vault/lessons/
   ```

### Validation Checklist

When a lesson is generated in `/spek.conclude` Step 3:

- [ ] Frontmatter has all required fields (title, type, tags, status, created, updated, source)
- [ ] Filename follows kebab-case convention
- [ ] Note contains 2+ wikilinks (depending on length)
- [ ] All wikilinks reference existing vault notes
- [ ] Status set to "active"
- [ ] Tags include domain + methodology
- [ ] Content is self-contained (can be read independently)

---

## Validation & Enforcement

### Automated Validation (in `/spek.conclude`)

```
After lesson generated:
  1. Parse frontmatter YAML
  2. Check required fields present
  3. Validate field formats (dates ISO 8601, enums valid, etc.)
  4. Count wikilinks; alert if below minimum
  5. Validate wikilink targets exist
  6. Save to vault with validation report
```

### Manual Audit

Quarterly review of vault notes:

```
1. Search for notes with broken wikilinks
   → Fix or remove invalid links
2. Check for obsolete patterns/decisions
   → Update status: "active" → "deprecated" or "superseded"
3. Verify filename consistency
   → Rename non-conformant files
4. Refresh `updated` field on recent changes
```

### Query Validation (in `/spek.context`)

When loading context, verify:
- [ ] All notes have valid frontmatter
- [ ] All wikilinks resolve
- [ ] No duplicate note titles (except in archive/)
- [ ] Tags are consistent (standardized vocabulary)

---

## Implementation Timeline

### Week 1: Setup
- [ ] Create Zettelkasten conventions guide (`.spekificity/guides/vault-conventions.md`)
- [ ] Document frontmatter schema in copilot-instructions.md
- [ ] Create template for each note type (decision, pattern, lesson, guide)

### Week 2: Integration into /spek.conclude
- [ ] Enhance `/spek.conclude` Step 3 to generate frontmatter automatically
- [ ] Add wikilink validation and alerting
- [ ] Add filename generation + uniqueness check
- [ ] Test lesson generation with full frontmatter

### Week 3: Vault Backfill & Testing
- [ ] Migrate existing vault notes to Zettelkasten format
  - Add frontmatter to `wiki/vault/decision.md` entries
  - Add frontmatter to `wiki/vault/patterns.md` entries
- [ ] Audit for atomicity violations
- [ ] Test wikilink generation + validation
- [ ] Test query patterns in `/spek.context`

### Week 4: Documentation & Launch
- [ ] Update wiki documentation with Zettelkasten schema
- [ ] Create training guide for future contributors
- [ ] Add Zettelkasten checklist to `/spek.conclude` acceptance criteria
- [ ] Launch with C.3.1 complete

---

## Success Criteria

- ✅ All vault lessons have valid frontmatter (title, tags, status, created, updated, source)
- ✅ All vault notes follow kebab-case filename convention
- ✅ All vault notes contain 2+ wikilinks (density validated)
- ✅ All wikilinks reference existing vault notes
- ✅ Notes are atomic (single concept per file)
- ✅ `/spek.conclude` Step 3 generates Zettelkasten frontmatter automatically
- ✅ Wikilink validation integrated into `/spek.conclude`
- ✅ Existing vault notes migrated to Zettelkasten format
- ✅ Vault is fully indexed and searchable in Obsidian

---

## Related Specifications

- **B.8.2:** Persistent Memories (vault architecture, 3-layer memory model)
- **B.8.4:** Prepare & Post Skills (Step 3 lesson generation integration)
- **C.3.2:** Auto-tagging + Auto-wikilinks (builds on Zettelkasten frontmatter)
- **C.3.5:** Session Logs as Vault Artifacts (applies Zettelkasten format)

---

## References

- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (external reference for token-efficient note conventions)
- **Zettelkasten Method:** https://zettelkasten.de/ (original methodology)
- **Obsidian Graph Navigation:** https://obsidian.md/features (wikilink navigation)
