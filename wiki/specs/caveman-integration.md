# SPECIFICATION: Caveman Integration (C4.3)

**Status:** ATOMIC SPECIFICATION  
**Type:** Optimization — Caveman Compression Mode Integration  
**Version:** 2026-05-19  
**Depends On:** error-handling-and-recovery.md, lessons-format.md, post-command.md, post-processing.md  

---

## Overview

Caveman compression mode drastically reduces token usage (~75-90% reduction) by employing ultra-compressed, meaning-preserving communication. This spec defines how and when caveman compression is applied within Spekificity workflows, token impact validation, and user control mechanisms.

**Purpose:**
- Maintain full context richness while minimizing token overhead
- Enable autonomous workflows at scale (multiple features per session)
- Keep comprehensive audit trails (lessons) within token budgets
- Provide user control over compression/clarity tradeoff

---

## Caveman Compression Modes

### Mode 1: `lite` (Minimal Compression)

**Compression Level:** ~30% token reduction

**When Used:**
- First feature in a session (user prefers readability over efficiency)
- When documentation clarity is critical
- For complex architectural decisions
- When onboarding new team members to context

**Output Characteristics:**
- Full sentences, natural language
- Complete explanations
- Multiple examples
- All context preserved
- Effort: High (verbose)

**Example - Normal Text:**
```
## Decision: Use Obsidian for Vault

We chose Obsidian as the persistent knowledge store for the following reasons:
- Built-in graph visualization of notes and links
- YAML frontmatter support for structured metadata
- Excellent plugin ecosystem for integration (API, Git sync, etc.)
- Local-first storage (vault is a directory of markdown files)
- Wide adoption in knowledge management community

This enables the 3-layer memory model where decisions + patterns are permanently stored.
```

**Example - Lite Caveman:**
```
## Decision: Obsidian for Vault

Why: Graph visualization, YAML frontmatter, plugins, local storage, wide adoption.
Enables: 3-layer memory (decisions + patterns permanent storage).
```

---

### Mode 2: `full` (Default Compression)

**Compression Level:** ~75% token reduction

**When Used:**
- Standard feature workflow (prepare → post)
- Most lessons generated at feature end
- Subsequent features in same session (context already loaded)
- Token budget is tight

**Output Characteristics:**
- Caveman-style minimal syntax
- Meaning preserved, verbosity eliminated
- Single-line explanations
- List format instead of prose
- Code/commands preserved as-is
- Effort: Medium (terse but readable)

**Example - Caveman Full:**
```
## Decision: Obsidian for Vault
Reason: Graph viz, YAML, plugins, local-first storage, adoption.
Use: 3-layer memory (decisions, patterns archived).
```

---

### Mode 3: `ultra` (Maximum Compression)

**Compression Level:** ~90% token reduction

**When Used:**
- Token budget nearly exhausted
- Session closing (archive final lessons for next session)
- Context cleanup before session restart
- Non-critical artifacts (temporary notes, debug logs)

**Output Characteristics:**
- Extreme abbreviation (CJK-style density possible)
- Symbols replace words (→, ∴, ✓, etc.)
- Minimal prose, maximal information
- May require context to understand (use with caution)
- Effort: Low (minimal)

**Example - Caveman Ultra:**
```
## Decision: Obsidian Vault
→ Graph viz, YAML, plugins, local-first, adoption.
∴ 3-layer memory: decisions, patterns archival.
```

---

## Integration Points

### Integration Point 1: Post-Feature Lesson Generation (`/spek.post`)

**When:** Feature completed, lessons extracted

**Usage:**
```bash
# Default: Full compression
spek post

# Explicit: Lite compression (preserve detail)
spek post --caveman-mode=lite

# Aggressive: Ultra compression (token budget low)
spek post --caveman-mode=ultra

# Dry-run: Preview compression
spek post --caveman-mode=ultra --dry-run
```

**Workflow:**
1. Extract lessons from artifacts (spec, plan, tasks, execution)
2. Format per [Lessons Format](lessons-format.md)
3. Apply compression mode (`full` by default)
4. Write to `vault/lessons/<date>-<feature>-<name>.md`
5. Log compression ratio to feature state (e.g., "80% reduction via caveman full")

**Impact:**
- `lite`: ~200 lines per lesson (typical)
- `full`: ~50 lines per lesson (compressed)
- `ultra`: ~15 lines per lesson (ultra-compressed)

---

### Integration Point 2: Architectural Decisions Archival

**When:** New decisions captured during feature, archived to vault

**Spec:** [Architectural Decisions](architectural-decisions.md)

**Compression Rule:**
- Primary storage (`vault/decision.md`): `lite` (preserve full reasoning)
- Repo cache (`/memories/repo/architectural-decisions.md`): `full` (compressed index)
- Inline references: `ultra` (single-line summary)

**Example:**
```markdown
# vault/decision.md (LITE)
## Decision: Caveman Integration for Token Efficiency
Reasoning: Token usage was critical constraint in autonomous workflows...
[Full explanation, rationale, alternatives considered]

# /memories/repo/architectural-decisions.md (FULL)
## Decision: Caveman for Token Efficiency
Why: Token constraint in autonomous workflows.
Trade: Readability vs. efficiency (configurable).

# Reference in future feature spec (ULTRA):
Decisions applied: Caveman compression (lite/full/ultra modes).
```

---

### Integration Point 3: Patterns Library Updates

**When:** Reusable patterns captured during feature

**Spec:** [Patterns Library](patterns-library.md)

**Compression Rule:**
- Pattern definition: `lite` (clarify pattern for reuse)
- Pattern index entry: `full` (compressed reference)
- Inline uses: `ultra` (pointer to pattern)

**Example:**
```markdown
# vault/patterns.md (LITE)
## Pattern: Decorator for Workflow Enrichment
Description: Wrapper functions that inject context before calling external tools.
Example: Specify enrichment wraps /speckit.specify to load architectural decisions.
When: Used when adding contextual intelligence to stateless tools.

# /memories/repo/patterns-index.md (FULL)
## Pattern: Decorator for Enrichment
Def: Wrapper injects context before calling tool.
Ex: Specify enrichment → /speckit.specify with decisions.
Use: Contextual intelligence on stateless tools.

# Inline reference in feature (ULTRA)
Patterns: Use decorator-enrichment pattern for new tool.
```

---

### Integration Point 4: Session Cleanup (`/spek.post` finale)

**When:** Feature complete, session memory archived

**Compression Rule:**
- Archive feature state (`/memories/session/<feature>.archive`): `full`
- Retention for next session: `ultra` (summary only)

**Workflow:**
1. Archive current feature state (compressed via `full` mode)
2. Keep ultra-compressed summary in session history
3. Purge session memory (`/memories/session/current-feature.md` deleted)
4. Ready for next feature with fresh context (but access to archived summary)

---

### Integration Point 5: Error Logging

**When:** Errors logged during any skill execution

**Spec:** [Error Handling and Recovery](error-handling-and-recovery.md)

**Compression Rule:**
- Error log entry: `lite` (preserve full details for debugging)
- Error summary in reports: `full` (compressed for readability)

**Note:** Never use ultra compression for error logs (debuggability critical).

---

## User Control & Transparency

### Flag: `--caveman-mode`

**Options:**
- `--caveman-mode=lite` — Minimal compression (readable, higher tokens)
- `--caveman-mode=full` — Default compression (balanced)
- `--caveman-mode=ultra` — Maximum compression (extreme efficiency)

**Applied To:**
- `/spek.post --caveman-mode=lite` (feature lesson generation)
- `/spek.context --caveman-mode=full` (context loading)
- `/spek.map --caveman-mode=lite` (graph export/merge, typically not compressed)

**Default:**
- Post-feature: `full` (80% reduction)
- Context: No compression (load full quality)
- Map: No compression (preserve code metadata)

---

### Transparency & Reporting

**Feature State Reports Compression:**

```markdown
# Feature State (2026-05-19)
...
## Compression Applied
- Lesson: caveman-full (50 lines, 80% reduction from 250)
- Decisions: caveman-lite (vault) + caveman-full (cache)
- Patterns: caveman-lite (vault) + caveman-full (cache)
- Session archive: caveman-ultra (4 lines summary)
```

**Token Usage Tracking:**

```markdown
## Token Budget
- Context loaded: 8.2K tokens
- Lesson generation: 2.1K tokens
- Vault update: 1.5K tokens
- Total: 11.8K tokens
- Savings: 45K tokens via caveman compression (caveman-full mode)
```

---

## Quality Assurance

### Preservation Validation

**Rule:** Caveman compression preserves 100% of **information content**, even if reducing tokens by 90%.

**Example — Decision:**
```markdown
# Original (Readable, 500 tokens)
We chose Rust for the systems layer because it provides memory safety 
without garbage collection, enabling real-time performance. The steep 
learning curve is offset by the long-term benefits of preventing entire 
classes of bugs (null pointer dereferences, buffer overflows, use-after-free).

# Caveman Ultra (50 tokens, same info)
Chose Rust: Memory safety + no GC → Real-time perf.
Trade: Learning curve ↔ Prevent null ptr, buffer overflow, use-after-free bugs.
```

Both capture the same decision information; compression just removes verbosity.

---

### Test Cases

- [ ] Lesson generated in `lite` mode is more readable than `full`
- [ ] Lesson generated in `full` mode saves ~75% tokens vs `lite`
- [ ] Lesson generated in `ultra` mode saves ~90% tokens vs `lite`
- [ ] All three modes preserve all factual information (decision, why, trade-offs)
- [ ] Compressed decisions still usable for context injection into future features
- [ ] Compressed patterns still provide guidance for pattern reuse
- [ ] Ultra-compressed error logs still contain debugging info (maybe require decompression)
- [ ] Token savings correctly reported in feature state

---

## Implementation Checklist

- [ ] Implement caveman-lite renderer (light prose to minimal prose)
- [ ] Implement caveman-full renderer (lite → caveman syntax)
- [ ] Implement caveman-ultra renderer (full → extreme compression)
- [ ] Integrate `--caveman-mode` flag into `/spek.post`
- [ ] Integrate compression mode into lesson generation
- [ ] Integrate compression into decision archival (vault vs cache)
- [ ] Integrate compression into pattern library updates
- [ ] Add token savings calculation + reporting
- [ ] Add quality assurance tests (information preservation)
- [ ] Document compression modes in user guide
- [ ] Add examples of each mode in wiki

---

## Performance Impact

| Mode | Token Reduction | Readability | Use Case |
|------|-----------------|-------------|----------|
| `lite` | 30% | High | Onboarding, documentation |
| `full` | 75% | Medium | Standard workflow |
| `ultra` | 90% | Low | Token budget exhausted |

**Typical Session:**
- Feature 1 (fresh context): lite mode (30% reduction) → 15K tokens
- Feature 2-5 (reusing context): full mode (75% reduction) → 12K tokens each
- Feature 6+ (budget tight): ultra mode (90% reduction) → 10K tokens each
- Total for 6 features: ~75K tokens (would be ~250K without compression)

---

## Known Limitations

### Limitation 1: Ultra Mode Requires Context

**Issue:** Ultra-compressed lessons can be hard to understand without prior context

**Workaround:** Always use ultra mode in same session (context already loaded); regenerate at `lite` before archiving if needed

---

### Limitation 2: Search Difficulty

**Issue:** Ultra-compressed text harder to search/grep

**Workaround:** Compress stored lessons, decompress on retrieval (not yet implemented)

---

### Limitation 3: No Auto-Decompression

**Issue:** User must know which compression mode was used

**Workaround:** Always store mode in lesson metadata (`caveman-mode: full` in frontmatter)

---

## Related Specs

- [Lessons Format](lessons-format.md) — How lessons are structured
- [Post Processing](post-processing.md) — When lessons are generated
- [Architectural Decisions](architectural-decisions.md) — Decision archival
- [Patterns Library](patterns-library.md) — Pattern storage
- [Error Handling and Recovery](error-handling-and-recovery.md) — Error logging
- [Memory Architecture](memory-architecture.md) — 3-layer memory model

---

## Final Notes

Caveman compression is **optional but recommended** for Spekificity workflows. It enables:

- **Scalability** — Process many more features per session (token efficiency)
- **Autonomy** — Agent can operate independently without external token replenishment
- **Clarity** — Multiple compression modes give users control over readability/efficiency tradeoff
- **Determinism** — Compressed lessons still fully informative and reproducible

**Default workflow:**
1. First feature: `--caveman-mode=lite` (preserve detail during onboarding)
2. Subsequent features: `--caveman-mode=full` (standard compression)
3. If budget tight: `--caveman-mode=ultra` (extreme efficiency)
4. Before session end: Auto-archive with mode recorded in metadata

**Future improvements (Phase 2+):**
- Auto-decompression (decompress on retrieval)
- Search indexing of compressed text
- Mode inference (auto-select mode based on token budget)
- Compression statistics dashboard (show token savings over time)

---

## Success Criteria

- ✅ Compression modes implemented (lite/full/ultra working)
- ✅ Token reduction verified (30%/75%/90% targets achieved)
- ✅ Meaning preserved (ultra compression still understandable to agent)
- ✅ User control working (modes selectable per command/session)
- ✅ Application transparent (users don't notice when caveman is active)
- ✅ Integration seamless (applied to lessons, decisions, patterns)
- ✅ Toggle mechanism working (can switch modes mid-session)
