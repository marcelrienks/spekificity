# ATOMIC SPECIFICATION: Architectural Decisions (C2.2)

**Status:** ATOMIC SPECIFICATION  
**Type:** Memory Layer 2 — Architectural Decisions  
**Depends On:** lessons-format.md, context-load-lifecycle.md  
**Used By:** /spek.context (read at session start), /spek.post (write at feature end)  

---

## Overview

Architectural decisions are explicit, documented choices about system design, constraints, and rationale. They persist in two places:
1. **Vault (authoritative):** `vault/decision.md` — Full, permanent archive
2. **Repo Memory (cached):** `/memories/repo/architectural-decisions.md` — Recent, compressed summary

This spec defines the structure, lifecycle, and sync strategy for both.

---

## Vault Decisions (vault/decision.md)

### Purpose
Permanent archive of all architectural decisions; source of truth for understanding project constraints and rationale.

### File Structure

```markdown
# Architectural Decisions Index

## [Decision 1 Title]

**Date:** YYYY-MM-DD  
**Feature:** spec-[number] or "architecture"  
**Status:** active | deprecated | superseded-by-[link]  

**Context:** Why this decision was needed  

**Options Considered:**
- Option A: [description, pros, cons]
- Option B: [description, pros, cons]
- Option C: [description, pros, cons]

**Decision:** [Option chosen] because [rationale]  

**Impact:** [affected systems, future constraints, ripple effects]  

**Related Decisions:**
- [Link to related decision]
- [Link to related decision]

---

## [Decision 2 Title]
...
```

### Template Fields

**Date:** When decision was made (ISO format: YYYY-MM-DD)

**Feature:** Which feature/context this came from
- "spec-003" = Decision from feature 003 spec phase
- "architecture" = Foundational architecture decision
- "pattern-xyz" = Decision about a specific pattern

**Status:** One of:
- `active` — Currently constrains behavior
- `deprecated` — Old but kept for context
- `superseded-by-[link]` — Replaced by newer decision

**Context:** 1-3 sentences explaining:
- Why this decision was necessary
- What problem it solved
- What triggered deliberation

**Options Considered:** 2-4 options, each with:
- Brief description
- Pros (1-2 bullets)
- Cons (1-2 bullets)

**Decision:** 1-2 sentences stating:
- Which option was chosen
- Why (rationale)
- Trade-offs accepted

**Impact:** How this decision affects:
- Other systems
- Future features
- Performance / token budget
- Testing strategy
- Development workflow

**Related Decisions:** Cross-references to:
- Decisions that depend on this one
- Decisions this supersedes
- Complementary decisions

### Query Patterns

**"What are active decisions?"**
```bash
grep -B2 "status: active" vault/decision.md | grep "##"
```

**"What decisions affect [system]?"**
```bash
grep -l "[system-name]" vault/decision.md
```

**"What was decided in feature 003?"**
```bash
grep -B5 "spec-003" vault/decision.md | grep "##"
```

---

## Repo Memory Decisions (/memories/repo/architectural-decisions.md)

### Purpose
Compressed, recent-only summary of active decisions. Used for session startup context and quick lookup.

### File Structure

```markdown
# Architectural Decisions (Compressed Summary)

**Last Sync:** YYYY-MM-DD HH:MM (synced from vault/decision.md)  
**Coverage:** Last 3 features (specs [N-2], [N-1], [N])  
**Full Archive:** See vault/decision.md (permanent)  

## Recent Active Decisions (Last 3 Features)

| Feature | Decision | Rationale | Impact |
|---------|----------|-----------|--------|
| spec-003 | [title] | [1-line rationale] | [high/medium/low] |
| spec-002 | [title] | [1-line rationale] | [high/medium/low] |
| spec-001 | [title] | [1-line rationale] | [high/medium/low] |

## Decision Details (Compressed)

### [Decision Title 1]

**Status:** active  
**Feature:** spec-003  
**Rationale:** [1-2 sentence compressed rationale]  
**Impact:** [1 line compressed impact]  

---

### [Decision Title 2]

**Status:** active  
**Feature:** spec-002  
**Rationale:** [1-2 sentence compressed rationale]  
**Impact:** [1 line compressed impact]  

---

## Superseded Decisions

See vault/decision.md for full history. Recent supersessions:
- [Superseded decision name] → [new decision name] (when)

---

## Categories

**Core Architecture:**
- [List of core decisions by category]

**Integration Constraints:**
- [List of integration decisions]

**Performance Decisions:**
- [List of performance-related decisions]

**Development Workflow:**
- [List of process decisions]
```

### Update Rules

**Sync Trigger:** After each feature (`/spek.post` step 4)

**Sync Process:**
1. Read vault/decision.md
2. Filter to active decisions from last 3 features
3. Compress each decision to 1-2 sentences (caveman mode)
4. Create table of recent decisions
5. Write to /memories/repo/architectural-decisions.md

**Compression Rules (Caveman Format):**
- Active voice: "We chose X because Y" not "X was considered and ultimately selected"
- Concrete: "Decorator pattern prevents tight coupling to SpecKit" not "A flexible approach was taken"
- Short: 1-2 sentences max per decision
- Specific: Name the decision, not "important choice"

**Keep:** All active decisions from last 3 features

**Remove:** Decisions older than 3 features (still in vault, just removed from repo memory)

---

## Lifecycle

### Write Triggers

**During feature work:**
- When major architectural choice needs documentation → Add to `/memories/session/current-feature.md` (decisions made this feature)
- Mark for inclusion in lessons when feature completes

**At feature end (`/spek.post` step 4):**
- Extract decisions from lessons → Append to vault/decision.md
- De-duplicate (check if decision already exists)
- Mark status and feature source
- Sync recent decisions to /memories/repo/architectural-decisions.md

### Read Triggers

**Session start (`/spek.context`):**
- Read /memories/repo/architectural-decisions.md (compressed, fast)
- Include recent decisions in context briefing
- Load into agent context

**During spec/plan writing:**
- Query vault/decision.md for decisions about [topic]
- Use past decisions to inform new choices
- Cite related decisions in new spec/plan

**Before implementing:**
- Review vault/decision.md to understand constraints
- Check if implementation would violate any active decision

### Retention Policy

**Vault (vault/decision.md):**
- Keep all decisions indefinitely (permanent archive)
- Mark old ones as `deprecated` but don't delete

**Repo Memory (/memories/repo/architectural-decisions.md):**
- Sync after each feature
- Keep only recent active decisions (last 3 features)
- Prune older decisions to keep file size <10KB

---

## Integration with Other Systems

### Lessons Format (lessons-format.md)

Decisions made during a feature are extracted in the "Decisions Made" section of vault/lessons/ files. The post-processing phase (post-command.md) converts these to formal decision entries.

### Context Loading (context-load-lifecycle.md)

Decision context is loaded at session start via `/spek.context`, compressed, and added to /memories/session/context-loaded.md for agent awareness.

### SpecKit Integration (specify-enrichment.md, plan-enrichment.md)

Recent decisions are injected into `/spek.specify` and `/spek.plan` prompts to guide spec/plan generation toward existing constraints.

---

## Success Criteria

✅ All architectural decisions captured with context, options, rationale  
✅ Decisions distinguish between active / deprecated / superseded  
✅ Vault is permanent archive; repo memory is compressed cache  
✅ Sync happens automatically at feature end  
✅ Decisions are queryable (grep-friendly format)  
✅ Related decisions are cross-referenced  
✅ Compression follows caveman format (active voice, concrete, short, specific)  

---

## Implementation Checklist

- [ ] Create vault/decision.md template
- [ ] Implement decision extraction in /spek.post
- [ ] Implement decision sync to /memories/repo/
- [ ] Update /spek.context to load recent decisions
- [ ] Add decision query patterns to wiki guide
- [ ] Document decision-making process in project wiki

---

## References

**Related Specs:**
- [lessons-format.md](lessons-format.md) — Decisions captured here first
- [context-load-lifecycle.md](context-load-lifecycle.md) — Decisions loaded at session start
- [specify-enrichment.md](specify-enrichment.md) — Decisions injected into spec generation
- [plan-enrichment.md](plan-enrichment.md) — Decisions injected into plan generation
- [post-command.md](post-command.md) — Decisions synced to vault here

**External:**
- [extracted spec Persistent Memories](persistent-memories-and-lessons.md#type-2-architectural-decisions-vault--repo-memory) — Original spec
