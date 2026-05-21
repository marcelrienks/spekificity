# C.3.2 Auto-Tagging + Auto-Wikilink Insertion for Lessons

**Status:** Specification   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Priority:** MUST (Phase 1)  
**Effort:** 4-6 hours  
**Adoption Source:** B.9 (claude-code-memory-setup, chat import pipeline pattern)  
**Depends On:** C.3.1 Zettelkasten Conventions

---

## Purpose

Automate the process of:
1. **Extracting keywords** from generated lessons (technical concepts, frameworks, patterns)
2. **Mapping keywords to existing vault items** (decisions, patterns, lessons)
3. **Auto-inserting wikilinks** to create interconnection without manual work
4. **Auto-generating tags** for domain, tech stack, and methodology
5. **Validating lessons** against prior patterns to prevent redundancy

**Goal:** Reduce manual linking effort (~70% automation), enable knowledge discovery across features, validate lessons against vault.

---

## Scope & Relationships

**What this spec covers:**
- Keyword extraction from lesson content
- Keyword → vault item mapping logic
- Auto-wikilink insertion algorithm
- Auto-tag generation strategy
- Tag + keyword mapping configuration
- Validation logic to catch redundancy

**What this spec does NOT cover:**
- Vault schema (see C.3.1 Zettelkasten)
- Lesson content generation (see B.8.4 Post Command Step 3)
- Graph queries (see B.11 Codegraph Setup)
- Manual linking workflows (assume auto-linking handles 70%)

---

## Success Criteria

- ✅ Keyword extraction achieves 70%+ automation (manual linking drops significantly)
- ✅ Keyword-to-vault mapping detects relevant decisions/patterns with >75% accuracy
- ✅ Auto-wikilinks inserted without manual intervention (links appear in generated lessons)
- ✅ Auto-tags generated for domain, tech stack, methodology (frontmatter enriched)
- ✅ Redundancy detection alerts when lesson duplicates vault pattern (prevents duplication)
- ✅ Missing pattern detection flags lessons that should reference vault items
- ✅ Tag + keyword mapping configurable per project (customizable in config.yaml)

---

## Related Specs

- C.3.1: Zettelkasten conventions (MUST exist first; defines frontmatter)
- B.8.4: Post Command (Step 3 lesson generation; where auto-linking is integrated)
- B.8.2: Persistent Memories (vault structure; source of linking targets)

---

## Configuration: Keyword-Tag Mapping

### Setup File: `.spekificity/config.yaml`

Add new section to configure keyword extraction + mapping:

```yaml
auto_linking:
  enabled: true
  
  # Keyword extraction settings
  extraction:
    min_keyword_length: 3  # Minimum characters
    max_keywords_per_lesson: 15  # Limit extracted keywords
    exclude_stopwords: true  # Filter common words (the, a, and, etc.)
    
  # Mapping strategy
  mapping:
    strategy: "longest-match"  # "longest-match" or "exact-match"
    case_sensitive: false
    score_threshold: 0.75  # Confidence threshold for matches (0-1)
  
  # Output behavior
  output:
    auto_insert_wikilinks: true
    auto_generate_tags: true
    alert_on_redundancy: true
    alert_on_missing_pattern: true
  
  # Keyword tag mappings
  keyword_tag_map:
    # Architecture patterns
    "singleton": 
      tags: ["pattern/singleton", "design-pattern"]
      vault_link: "singleton-pattern"
    "dependency-injection":
      tags: ["pattern/di", "architecture"]
      vault_link: "dependency-injection-pattern"
    "service-locator":
      tags: ["anti-pattern", "architecture"]
      vault_link: "service-locator-anti-pattern"
    
    # State management
    "state-management":
      tags: ["pattern/state", "frontend", "complexity"]
      vault_link: "state-management-patterns"
    "redux":
      tags: ["tech/redux", "state-management"]
      vault_link: "redux-store-implementation"
    "context-api":
      tags: ["tech/react", "state-management"]
      vault_link: "react-context-api"
    
    # Testing patterns
    "unit-test":
      tags: ["method/testing", "qa"]
      vault_link: "unit-testing-strategy"
    "integration-test":
      tags: ["method/testing", "qa"]
      vault_link: "integration-testing-strategy"
    "mutation-testing":
      tags: ["method/mutation-testing", "qa", "advanced"]
      vault_link: "mutation-testing-coverage"
    
    # Error handling
    "error-handling":
      tags: ["pattern/error", "reliability"]
      vault_link: "error-handling-recovery"
    "circuit-breaker":
      tags: ["pattern/resilience", "error-handling"]
      vault_link: "circuit-breaker-pattern"
    "exponential-backoff":
      tags: ["pattern/retry", "resilience"]
      vault_link: "exponential-backoff-strategy"
    
    # Tech stack
    "react":
      tags: ["tech/react", "frontend"]
      vault_link: "react-best-practices"
    "typescript":
      tags: ["tech/typescript", "type-safety"]
      vault_link: "typescript-patterns"
    "node.js":
      tags: ["tech/nodejs", "backend"]
      vault_link: "nodejs-event-loop"
    
    # Architecture
    "microservices":
      tags: ["architecture/microservices", "scalability"]
      vault_link: "microservices-patterns"
    "monolith":
      tags: ["architecture/monolith", "simplicity"]
      vault_link: "monolithic-architecture"
    "event-driven":
      tags: ["architecture/event-driven", "async"]
      vault_link: "event-driven-architecture"
    
    # Domain-specific
    "authentication":
      tags: ["domain/auth", "security"]
      vault_link: "authentication-patterns"
    "authorization":
      tags: ["domain/auth", "security"]
      vault_link: "authorization-patterns"
    "api-design":
      tags: ["domain/api", "contract"]
      vault_link: "api-design-principles"
```

**How to Extend:** Add new keywords + mappings as they emerge:
1. User encounters new pattern/tech
2. Lesson generated with new keyword
3. Auto-linking alerts: "New keyword 'X' found; add to mapping"
4. User adds mapping to config
5. Future lessons auto-link to 'X'

---

## Keyword Extraction Algorithm

### Step 1: Extract Candidate Keywords

```
Input: Generated lesson content (plain text)
Output: List of candidate keywords

Algorithm:
  1. Tokenize lesson into words
  2. Filter by length (>= min_keyword_length from config)
  3. Remove stopwords (the, a, and, is, etc.) if enabled
  4. Remove duplicates
  5. Score each keyword by frequency (appear multiple times = higher score)
  6. Sort by score, keep top N (max_keywords_per_lesson)
```

**Example:**

```
Input lesson excerpt:
"We implemented dependency injection to solve tight coupling 
in our service layer. This follows the singleton pattern for 
factory creation. Dependency injection enables better testing 
and mocking."

Candidate keywords (after stopword removal + frequency):
  - "dependency-injection" (freq: 2, score: 0.95)
  - "service" (freq: 2, score: 0.85)
  - "singleton" (freq: 1, score: 0.60)
  - "testing" (freq: 1, score: 0.55)
  - "factory" (freq: 1, score: 0.50)
```

### Step 2: Match Keywords to Vault Items

```
Input: Candidate keywords
Output: Matched vault items + confidence scores

Algorithm:
  1. For each keyword:
     a. Lookup in keyword_tag_map
     b. If exact match found:
        - confidence = 1.0
        - vault_link = mapped link
     c. If no exact match:
        - Search vault notes for semantic match (fuzzy matching)
        - Calculate confidence score (0-1, based on string similarity)
        - If score >= threshold: include match
     d. If no match found:
        - Alert: "Unknown keyword 'X'; suggest mapping in config"
  2. Deduplicate (remove if same vault item matched multiple times)
  3. Sort by confidence (highest first)
  4. Return matched items
```

**Example Continuation:**

```
Keyword "dependency-injection":
  - Exact match in keyword_tag_map
  - confidence: 1.0
  - vault_link: "dependency-injection-pattern"

Keyword "singleton":
  - Exact match in keyword_tag_map
  - confidence: 1.0
  - vault_link: "singleton-pattern"

Keyword "service":
  - No exact match
  - Fuzzy search vault for "service"
  - Found: "service-layer-pattern", "microservices-patterns"
  - confidence: 0.72 for "service-layer-pattern"
  - Include if score >= threshold (0.75)? NO, just under threshold
  - Alert: "Keyword 'service' matched with low confidence"

Keyword "testing":
  - No exact match
  - Fuzzy search vault for "testing"
  - Found: "unit-testing-strategy", "integration-testing-strategy"
  - confidence: 0.80 for "unit-testing-strategy"
  - Include if score >= threshold? YES
  - vault_link: "unit-testing-strategy"

Result (after filtering + dedup):
  - [[dependency-injection-pattern]] (confidence: 1.0)
  - [[singleton-pattern]] (confidence: 1.0)
  - [[unit-testing-strategy]] (confidence: 0.80)
```

### Step 3: Auto-Insert Wikilinks

```
Input: Lesson content, matched vault items
Output: Lesson content with inserted wikilinks

Algorithm:
  1. For each matched vault item:
     a. Find first natural occurrence of keyword in lesson
     b. Wrap in wikilink: keyword → [[vault_link]]
     c. If no natural occurrence found:
        - Add wikilink to `related` field in frontmatter
  2. Validate wikilinks don't conflict (no double-wrapping)
  3. Return modified lesson content
```

**Example:**

```
Original: "We implemented dependency injection to solve..."
Modified: "We implemented [[dependency-injection-pattern]] to solve..."

Original: "This follows the singleton pattern for factory creation."
Modified: "This follows the [[singleton-pattern]] for factory creation."

If keyword not found in content, add to frontmatter:
related: 
  - "[[dependency-injection-pattern]]"
  - "[[singleton-pattern]]"
  - "[[unit-testing-strategy]]"
```

### Step 4: Auto-Generate Tags

```
Input: Matched vault items + keyword mappings
Output: Tag list for frontmatter

Algorithm:
  1. For each matched vault item:
     a. Lookup tags in keyword_tag_map
     b. Collect all tags
  2. Add domain tag (extract from feature name/context)
  3. Add methodology tag (if applicable)
  4. Deduplicate
  5. Sort alphabetically
  6. Return tag list
```

**Example:**

```
Matched items:
  - "dependency-injection-pattern" → tags: ["pattern/di", "architecture"]
  - "singleton-pattern" → tags: ["pattern/singleton", "design-pattern"]
  - "unit-testing-strategy" → tags: ["method/testing", "qa"]

Feature context: "auth-refactor" → domain: "security"

Final tags (sorted):
  - "architecture"
  - "design-pattern"
  - "domain/security"
  - "method/testing"
  - "pattern/di"
  - "pattern/singleton"
  - "qa"
```

---

## Validation: Catch Redundancy & Conflicts

### Redundancy Check

```
After auto-linking complete, check:
  1. Is this lesson similar to existing lessons?
     - Compare against all wiki/vault/lessons/*.md
     - Semantic similarity > 0.80?
     - Alert: "Similar lesson exists: [[existing-lesson]]; review for duplication"
  2. Do wikilinks form circular patterns?
     - Check for A→B, B→C, C→A cycles
     - Alert if cycle detected (likely indicates over-linking)
  3. Are all wikilinks valuable?
     - Confidence score < 0.70?
     - Alert: "Wikilink [[X]] has low confidence; consider removing"
```

### Pattern Detection

```
When lesson auto-links to multiple patterns:
  1. Check for conflicts (e.g., anti-pattern + pattern)
     - Alert if contradiction detected
  2. Check for missing context
     - If lesson mentions "service" but doesn't link to "service-patterns"?
     - Alert: "Suggest pattern [[service-patterns]] for context"
```

---

## Integration: /spek.conclude Step 3 Enhancement

### Current Workflow (B.8.4)

```
/spek.conclude Step 3: Generate Lessons
  1. Collect artifacts (spec, plan, tasks, trace)
  2. Generate lesson content (What/How/Tasks/Decisions/Patterns/Next/Metrics)
  3. Save to wiki/vault/lessons/<date>-<feature>-*.md
```

### Enhanced Workflow (with C.3.2)

```
/spek.conclude Step 3: Generate Lessons (Enhanced)
  1. Collect artifacts (spec, plan, tasks, trace)
  2. Generate lesson content (What/How/Tasks/Decisions/Patterns/Next/Metrics)
  3. [NEW] Auto-extract keywords from generated lesson
  4. [NEW] Match keywords to vault items
  5. [NEW] Auto-insert wikilinks into lesson content
  6. [NEW] Auto-generate tags for frontmatter
  7. [NEW] Run redundancy check; alert if issues
  8. Save to wiki/vault/lessons/<date>-<feature>-*.md
```

### Implementation Details

**In `/spek.conclude` Step 3 code:**

```python
def generate_lesson_with_auto_linking(spec, plan, tasks, trace):
    # Step 1-2: Generate lesson content (existing)
    lesson_content = generate_lesson_from_artifacts(spec, plan, tasks, trace)
    
    # Step 3-7: New auto-linking logic
    
    # Step 3: Extract keywords
    keywords = extract_keywords(
        lesson_content,
        min_length=config.auto_linking.extraction.min_keyword_length,
        max_keywords=config.auto_linking.extraction.max_keywords_per_lesson
    )
    
    # Step 4: Match to vault items
    matches = match_keywords_to_vault(
        keywords,
        keyword_tag_map=config.auto_linking.keyword_tag_map,
        threshold=config.auto_linking.mapping.score_threshold
    )
    
    # Step 5: Insert wikilinks
    lesson_with_links = insert_wikilinks(lesson_content, matches)
    
    # Step 6: Generate tags
    auto_tags = generate_tags_from_matches(matches)
    
    # Step 7: Validate
    issues = validate_lesson(lesson_with_links, matches)
    if issues:
        alert_user(issues)  # Alert but don't block
    
    # Create frontmatter with auto-generated tags
    frontmatter = {
        "title": f"Lessons from {feature_name}",
        "type": "lesson",
        "tags": auto_tags,  # [NEW] Auto-generated
        "status": "active",
        "created": today(),
        "updated": today(),
        "source": feature_name,
        "related": [f"[[{link}]]" for link in matches.vault_links]  # [NEW]
    }
    
    # Save lesson with frontmatter
    save_lesson(frontmatter, lesson_with_links)
```

---

## Configuration Migration

### How to Set Up

1. **Initial Setup (.spekificity/config.yaml):**
   - Include default keyword_tag_map (see earlier in this spec)
   - Enable auto-linking: `auto_linking.enabled: true`

2. **Incremental Expansion:**
   - As users encounter new keywords, add to mapping
   - Config can be updated without code changes
   - `/spek.conclude` automatically uses updated mappings

3. **Team Collaboration:**
   - keyword_tag_map lives in config (tracked in git)
   - Team contributes new keywords + mappings
   - Standard vocabulary emerges naturally

---

## User Workflows

### Scenario A: Auto-Linking Succeeds (Happy Path)

```
1. /spek.conclude generates lesson
2. Auto-linking extracts keywords (dependency-injection, singleton, testing)
3. All keywords match vault items with high confidence
4. Wikilinks auto-inserted: [[dependency-injection-pattern]], etc.
5. Tags auto-generated: ["architecture", "pattern/di", "method/testing"]
6. User reviews lesson (looks good!)
7. Lesson saved with full frontmatter

Result: ✅ Fully interconnected lesson, zero manual work
```

### Scenario B: Partial Auto-Linking (Needs Review)

```
1. /spek.conclude generates lesson
2. Auto-linking extracts keywords (dependency-injection, custom-service-locator, testing)
3. "dependency-injection" matches perfectly
4. "custom-service-locator" has low confidence (0.65 < 0.75 threshold)
5. Alert: "Keyword 'custom-service-locator' has low confidence; consider adding to config"
6. User can:
   a. Add mapping to config: "custom-service-locator" → "service-locator-anti-pattern"
   b. Or manually review the wikilink suggestion
7. Lesson saved

Result: ✅ Mostly auto-linked; user enhances for future features
```

### Scenario C: New Pattern (Extension)

```
1. /spek.conclude generates lesson about "circuit breaker pattern"
2. Auto-linking extracts: circuit-breaker, resilience, retry, etc.
3. "circuit-breaker" not in keyword_tag_map
4. Alert: "Unknown keyword 'circuit-breaker'; suggest mapping in config"
5. User adds to config:
   "circuit-breaker":
     tags: ["pattern/resilience", "error-handling"]
     vault_link: "circuit-breaker-pattern"
6. User can manually add wikilink or wait for next feature
7. Future lessons auto-link to circuit-breaker-pattern

Result: ✅ Vault continuously enriched; no stale patterns
```

---

## Success Criteria

- ✅ Auto-linking enabled in `/spek.conclude` Step 3
- ✅ ~70% of wikilinks auto-generated (< 30% manual work)
- ✅ Confidence score > 0.75 for all auto-inserted links
- ✅ Auto-generated tags match manual tagging conventions
- ✅ No circular dependencies in wikilink graph
- ✅ Redundancy checks alert on duplicate lessons
- ✅ Config-driven keyword mappings (no code changes needed to add keywords)
- ✅ User alerted on low-confidence matches
- ✅ Vault interconnection density >= 2-4 wikilinks per lesson (validated)

---

## Related Specifications

- **C.3.1:** Zettelkasten Conventions (defines frontmatter + wikilink format)
- **B.8.2:** Persistent Memories (vault structure; source of matching targets)
- **B.8.4:** Post Command (Step 3 integration point)
- **B.9:** Claude Code Memory Setup (source of chat import pattern)

---

## References

- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (chat import pipeline pattern, 659⭐)
- **Keyword Extraction:** BM25 scoring (common in search/NLP)
- **Fuzzy Matching:** Levenshtein distance, Jaro-Winkler similarity
