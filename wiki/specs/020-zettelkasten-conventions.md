# C.3.1 Zettelkasten Conventions for Vault Notes



**Priority:** High (Phase 1 recommended)  
**Effort:** team-estimated  
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
 - Graph query patterns (see B.11 lat.md Setup)

**Related specs:**
- C.3.2: Auto-tagging + auto-wikilink (uses frontmatter schema)
- C.3.5: Session logs as vault artifacts (applies Zettelkasten format)
- B.8.2: Persistent memories (vault architecture)

---


## Success Criteria

- ✅ Frontmatter schema enforced (all required fields present)
- ✅ Filename conventions followed (kebab-case, unique, <50 chars)
- ✅ Atomicity maintained (one concept per file)
- ✅ Wikilinks present (a small number of cross-references per note)
- ✅ Metadata searchable (tags enable discovery)
- ✅ Status tracking accurate (active/deprecated/superseded labels correct)
- ✅ Notes discoverable (grep + Obsidian search working)
- [ ] Concise but complete (project-defined length)
- [ ] Can be understood without reading related notes
- [ ] Wikilinks enhance (don't require) understanding
- [ ] Not a summary of multiple patterns or decisions
**Examples consolidated:** see [wiki/specs/examples/020-zettelkasten-conventions-examples.md](examples/020-zettelkasten-conventions-examples.md)
- ## Wikilink Density Requirements
- **Minimum density:** a small number of wikilinks per note (depending on length)
- **Guidelines:**
- **Short notes:** Minimum a couple of wikilinks
- **Medium notes:** Include a few wikilinks
- **Long notes:** Ensure sufficient wikilinks to enable discovery
- **Wikilink Types:**
- **Pattern Links:** `[[singleton-pattern]]` → related patterns
- **Decision Links:** `[[use-di-over-service-locator]]` → architectural decisions
- **Tech Links:** `[[react-hooks]]` → technology choices
- **Domain Links:** `[[state-management]]` → domain concepts
- **Wikilink Format:**
- ```markdown
- We decided to use [[dependency-injection]] over service locators
- because [[service-locator-anti-pattern]] violates testability constraints.
- ```
- **Validation Rule:** Every wikilink should reference an existing note in `wiki/vault/` (except external links, which use standard Markdown `[text](url)`).
- ## Vault Note Types
- ### 1. Decision Notes
- **Frontmatter:**
- ```yaml
- tags: ["decision", "<domain>", "<methodology>"]
- **Structure:**
- Title: Starts with action verb ("Use...", "Adopt...", "Reject...")
- Context: Why this decision was needed
- Decision: What was chosen
- Rationale: Why this choice (alternatives considered)
- Consequences: Impact on future work
- Related: Links to enabling patterns, impacted features
- **Example:** `use-dependency-injection-pattern.md`
- ### 2. Pattern Notes
- tags: ["pattern/<category>", "<tech-stack>", "<domain>"]
- Title: Pattern name + category ("Singleton Pattern", "Observer Pattern")
- Problem: What problem does this pattern solve?
- Solution: How does the pattern work?
- Implementation: Code sketch or pseudocode
- When to Use: Constraints, preconditions
- Alternatives: Other patterns that could be used instead
- Related: Links to decisions, other patterns
- **Example:** `singleton-pattern.md`, `observer-pattern-events.md`
- ### 3. Lesson Notes
- tags: ["lesson/<feature>", "<domain>", "<methodology>"]
- source: "<feature-name>"
- Title: "Lessons from [Feature]"
- What We Built: Feature digest (from spec)
- How We Built It: Technical approach (from plan)
- Key Tasks: Major deliverables
- Decisions Made: With rationale
- Patterns Used: Reused + newly discovered
- Lessons for Next: Actionable guidance
- Metrics: LOC, files, coverage, time
- **Example:** `lessons-from-auth-refactor.md`
- ### 4. Guide Notes (Optional)
- tags: ["guide/<topic>", "<domain>"]
- Title: "Guide: [Topic]"
- Purpose: Why this guide exists
- Prerequisites: What readers should know
- Steps: Numbered or bulleted instructions
- Examples: Code or walkthrough examples
- Troubleshooting: Common issues + fixes
- Related: Links to relevant patterns/decisions
- **Example:** `guide-vault-conventions.md`, `guide-context-loading.md`
- ## Implementation: /spek.conclude Integration
- ### Where Zettelkasten Format Applies
- **Artifact:** Lesson generation (Step 3 of `/spek.conclude`)
- **Current Spec Reference:** B.8.4 Post Command (Step 3: Generate Lessons)
- **Enhancement Points:**
- **Frontmatter Generation** (automatically in `/spek.conclude` Step 3)
- Extract feature name from `vault/session/`
- Generate title: "Lessons from [feature]"
- Populate frontmatter:
- type: "lesson"
- tags: [extract from feature domain + tech stack]
- status: "active"
- created: today's date
- updated: today's date
- source: feature name
- Add default `related` field (will be populated by S2 auto-linking)
- **Wikilink Validation** (Step 3, after content generation)
- Count wikilinks in generated lesson
- If count < minimum for length:
- Alert: "Lesson has [N] wikilinks; recommend [M]"
- Suggest related decisions/patterns to link
- Validate all wikilinks reference existing vault notes
- Report broken links to user
- **Filename Generation** (Step 3, before saving)
- Extract feature name + date
- Generate kebab-case filename: "<YYYY-MM-DD>-<feature>-lesson.md"
- Verify globally unique within vault/
- Save to wiki/vault/lessons/
- ### Validation Checklist
- When a lesson is generated in `/spek.conclude` Step 3:
- [ ] Frontmatter has all required fields (title, type, tags, status, created, updated, source)
- [ ] Filename follows kebab-case convention
- [ ] Note contains 2+ wikilinks (depending on length)
- [ ] All wikilinks reference existing vault notes
- [ ] Status set to "active"
- [ ] Tags include domain + methodology
- [ ] Content is self-contained (can be read independently)
- ## Validation & Enforcement
- ### Automated Validation (in `/spek.conclude`)
- After lesson generated:
- Parse frontmatter YAML
- Check required fields present
- Validate field formats (dates ISO 8601, enums valid, etc.)
- Count wikilinks; alert if below minimum
- Validate wikilink targets exist
- Save to vault with validation report
- ### Manual Audit
- Quarterly review of vault notes:
- Search for notes with broken wikilinks
- → Fix or remove invalid links
- Check for obsolete patterns/decisions
- → Update status: "active" → "deprecated" or "superseded"
- Verify filename consistency
- → Rename non-conformant files
- Refresh `updated` field on recent changes
- ### Query Validation (in `/spek.context`)
- When loading context, verify:
- [ ] All notes have valid frontmatter
- [ ] All wikilinks resolve
- [ ] No duplicate note titles (except in archive/)
- [ ] Tags are consistent (standardized vocabulary)
- ## Implementation Timeline
- ### Week 1: Setup
- [ ] Create Zettelkasten conventions guide (`.spek/guides/vault-conventions.md`)
- [ ] Document frontmatter schema in copilot-instructions.md
- [ ] Create template for each note type (decision, pattern, lesson, guide)
- ### Week 2: Integration into /spek.conclude
- [ ] Enhance `/spek.conclude` Step 3 to generate frontmatter automatically
- [ ] Add wikilink validation and alerting
- [ ] Add filename generation + uniqueness check
- [ ] Test lesson generation with full frontmatter
- ### Week 3: Vault Backfill & Testing
- [ ] Migrate existing vault notes to Zettelkasten format
- Add frontmatter to `wiki/vault/decision.md` entries
- Add frontmatter to `wiki/vault/patterns.md` entries
- [ ] Audit for atomicity violations
- [ ] Test wikilink generation + validation
- [ ] Test query patterns in `/spek.context`
- ### Week 4: Documentation & Launch
- [ ] Update wiki documentation with Zettelkasten schema
- [ ] Create training guide for future contributors
- [ ] Add Zettelkasten checklist to `/spek.conclude` acceptance criteria
- [ ] Launch with C.3.1 complete
- ## Success Criteria
- ✅ All vault lessons have valid frontmatter (title, tags, status, created, updated, source)
- ✅ All vault notes follow kebab-case filename convention
- ✅ All vault notes contain 2+ wikilinks (density validated)
- ✅ All wikilinks reference existing vault notes
- ✅ Notes are atomic (single concept per file)
- ✅ `/spek.conclude` Step 3 generates Zettelkasten frontmatter automatically
- ✅ Wikilink validation integrated into `/spek.conclude`
- ✅ Existing vault notes migrated to Zettelkasten format
- ✅ Vault is fully indexed and searchable in Obsidian
- ## Related Specifications
- **B.8.2:** Persistent Memories (vault architecture, 3-layer memory model)
- **B.8.4:** Prepare & Post Skills (Step 3 lesson generation integration)
- **C.3.2:** Auto-tagging + Auto-wikilinks (builds on Zettelkasten frontmatter)
- **C.3.5:** Session Logs as Vault Artifacts (applies Zettelkasten format)
- ## References
- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (external reference for token-efficient note conventions)
- **Zettelkasten Method:** https://zettelkasten.de/ (original methodology)
- **Obsidian Graph Navigation:** https://obsidian.md/features (wikilink navigation)


## Zettelkasten Schema


## Recommended YAML Frontmatter

All vault notes should include frontmatter with these fields to enable tooling and automation. Projects can adopt this progressively; tooling will function with partial metadata but automation (auto-tagging, graph exports, and reliable context extraction) works best when frontmatter is present.

```yaml
---
title: "<note-title>"
type: "decision|pattern|lesson|guide"
status: "active"
tags: ["<domain>", "<methodology>", "<tech-stack>"]
created: "<YYYY-MM-DD>"
updated: "<YYYY-MM-DD>"
source: "<feature-name|external-link|manual>"
related: ["[[note-name]]", "[[other-note]]"]
# Optional:
version: "1.0"  # optional semantic version or date
affects: ["spec-003-api-redesign"]  # optional list of affected features/components
---
```

**Field Definitions:**
Field | Required | Type | Description | Example | -------|----------|------|-------------|--------- | `title` | YES | string | Concise, unique note title | "Singleton Pattern for Service Management" | `type` | YES | enum | Classification: decision, pattern, lesson, guide | "pattern" | `tags` | YES | array | a small set of tags for searchability + organization | ["pattern/singleton", "architecture", "service-layer"] | `status` | YES | enum | active, deprecated, superseded, archived | "active" | `created` | YES | date | ISO 8601 creation date | "2026-05-10" | `updated` | YES | date | ISO 8601 last update date | "2026-05-19" | `source` | NO | string | Origin: feature name, external link, manual entry | "feature-auth-refactor" | `related` | NO | array | Wikilinks to related vault entries | ["[[dependency-injection]]", "[[service-patterns]]"]

## Filename Convention

**Format:** `<kebab-case-title>.md`

- **Rules:**
- Use lowercase letters, numbers, hyphens only
- Recommended maximum length (including extension)
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

