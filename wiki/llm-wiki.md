---
title: LLM Wiki
type: framework
tags: [meta, knowledge-management, pattern]
sources:
  - "raw/llm-wiki/"
  - "raw/articles/"
created: 2026-05-15
updated: 2026-05-15
---

# LLM Wiki: Persistent, Compounding Knowledge Management

## Overview

**LLM Wiki** is a pattern for building persistent, compounding knowledge bases where an AI agent reads source materials, extracts concepts, and maintains a structured markdown wiki that grows richer with each ingestion. It solves the fundamental problem that traditional knowledge management has never solved: **knowledge should compound, not evaporate**.

**Origin:** Andrej Karpathy's insight about building personal knowledge bases. The core shift is philosophical—**you rarely touch the wiki directly. It's the LLM's domain. Your job is to feed it sources and ask questions. The LLM organizes, cross-links, and maintains everything.**

---

## Vision & Philosophy

### What LLM Wiki Solves

1. **The Compounding Problem:** Traditional systems (RAG, chat history, note-taking) treat every interaction as stateless. LLM Wiki treats every interaction as an investment that strengthens the knowledge base permanently.

2. **The Maintenance Burden:** Humans abandon wikis because the maintenance cost grows faster than the value. LLMs can update cross-references, flag contradictions, and maintain consistency across dozens of pages in one pass.

3. **Synthesis at Scale:** RAG rediscovers knowledge from scratch on every query. LLM Wiki pre-compiles synthesis so that complex questions requiring five documents to piece together are already answered by the interconnected wiki.

4. **Portability Without Complexity:** Unlike enterprise knowledge management systems, this is intentionally personal, local, and portable—just markdown files, no vendor lock-in, no cloud dependency.

### Core Principles

1. **The Wiki is a Persistent, Compounding Artifact**
   - Knowledge is not ephemeral chat history that vanishes when the session ends.
   - It is a living asset that grows monotonically and becomes more valuable over time.

2. **Compilation Over Retrieval**
   - Heavy lifting happens at ingest time, not query time.
   - New sources are read, understood, integrated into existing knowledge, cross-references updated, contradictions flagged.

3. **Human Curates, LLM Maintains**
   - Human: curate sources, direct analysis, ask good questions, think about meaning.
   - LLM: summarize, cross-reference, file, keep consistent.
   - This division of labor is what allows scale.

4. **Files Over Apps**
   - The wiki is git-versioned plain markdown. No database. No vendor format. No lock-in.
   - Guarantees data sovereignty, portability, version control.

5. **Structure Emerges From Constraints**
   - A configuration document (schema, AGENTS.md, or CLAUDE.md) tells the LLM exactly how to behave.
   - This transforms a generic chatbot into a disciplined wiki maintainer.

6. **Knowledge Should Be Accessible to Reasoning**
   - A well-organized encyclopedia allows agents to reason effectively.
   - Information is pre-synthesized, cross-referenced, organized by topic, not by vector similarity.

---

## Implementation Schema

### Directory Structure

```
wiki/                              # LLM Wiki (root-level artifact)
├── raw/                           # Curated sources (immutable)
│   ├── articles/                  # Web articles, blog posts
│   ├── papers/                    # PDFs, research papers, transcripts
│   ├── clippings/                 # Web-clipped content
│   ├── books/                     # Book chapters, excerpts
│   └── projects/                  # Project docs, proposals
│
├── llm-wiki.md                    # This file (framework documentation)
├── architecture.md                # Single-word lowercase files (flat)
├── intention.md
├── workflow.md
└── specs/                         # Specification documents
```

**Key Semantics:**

| Location | Purpose | Written by | Mutability |
|----------|---------|-----------|-----------|
| `wiki/raw/` | Curated sources | Human | Immutable |
| `wiki/*.md` | Knowledge base | Agent (LLM) | LLM-maintained (human approves) |

**Note:** `index.md` and `log.md` (optional master catalog and activity log) are maintained automatically by agents and live in the wiki/ root.

### File Conventions

#### Frontmatter (YAML)

Every page includes frontmatter:

```yaml
---
title: My Page Title
type: concept | synthesis | comparison | analysis | reference
tags: [tag1, tag2, kebab-case]
sources: 
  - "raw/articles/source-1.md"
  - "raw/papers/source-2.pdf"
created: 2026-05-15
updated: 2026-05-15
contradictions: []
---
```

**Fields:**
- `sources:` Lists which raw files contributed to this page
- `type:` Indicates page category (conceptual; no separate directories by type)
- `contradictions:` Array of flagged contradictions (see below)
- Tool-agnostic: Readable by Obsidian, plain editors, git, static viewers

#### File Naming

**Convention:** All lowercase; single-word names preferred; hyphens allowed for multi-word concepts.

```
overview.md                 # Single-word lowercase (entry point)
architecture.md             # Single-word lowercase (majority)
llm-wiki.md                 # Hyphenated when needed
knowledge-synthesis.md      # Hyphens describe intent
contradiction-resolution.md # Multi-word concept
(subdirs only if grouping)  # Avoid deep nesting
```

**Why:** Flat structure is simple and navigable. Lowercase + hyphens are URL-friendly and portable. Single-word names prioritized for clarity.

#### Link Format (Tool-Agnostic)

Use standard markdown links, **NOT wikilinks**:

```markdown
# ❌ WRONG: Obsidian-specific
See [[LLM Wiki Concept]] for details.

# ✅ CORRECT: Portable
See [LLM Wiki Concept](llm-wiki.md) for details.
```

**Why:** Works in any markdown reader (GitHub, HTML, any editor). No Obsidian lock-in.

---

## Ingestion Workflow (Incremental & Supervised)

All ingestions follow this gate pattern:

```
Human: Upload source to wiki/raw/articles/
        ↓
Agent: Read source + extract concepts, entities, related pages
        ↓
Agent: Create INGESTION PLAN
        - Pages to create/update
        - Links to add/modify
        - Contradictions flagged
        ↓
Human: REVIEW & APPROVE PLAN
        ↓
        ├─ Approved? → Agent executes (writes to wiki/)
        │              Updates wiki/log.md
        │              Returns report
        │
        └─ Rejected/Modified? → Loop (revise plan)
```

**Key properties:**
1. Plan review is **mandatory**—agent never writes without human approval
2. **Incremental**—one source at a time (or small batches with individual reviews)
3. **Approval documented**—recorded in git commit and wiki/log.md

---

## Contradiction Policy

### Default: Conservative (Flag + Human Decides)

When agent detects conflicting claims:

1. **Stop execution.** Do not auto-resolve.
2. **Flag in frontmatter:**
   ```yaml
   contradictions:
     - claim: "LLM Wiki works best at 100–500 pages"
       source_a: "raw/articles/karpathy-idea.md"
       quote_a: "moderate scale (~100 sources)"
       source_b: "raw/articles/enterprise-guide.md"
       quote_b: "scales to 10,000+ pages"
       resolution_needed: true
   ```
3. **Notify human:** Report in plan review
4. **Wait for decision:** Human chooses which claim to use or synthesizes both
5. **Document decision:**
   ```yaml
   - claim: "..."
     resolution: "HUMAN_DECIDED: Use source_a; source_b is outdated"
     resolved_by: "human"
     resolved_at: 2026-05-15
   ```

### Optional: Aggressive (Auto-Resolve)

Can be enabled per-project with explicit rules:

```yaml
contradiction_policy: aggressive
resolution_rules:
  - rule: "Prefer newer sources by publication date"
    priority: 1
  - rule: "Prefer primary sources over secondary"
    priority: 2
```

If enabled, agent auto-resolves using rules and documents in frontmatter (auditable, reversible).

---

## Three Core Operations

Agents implementing LLM Wiki support these commands:

### /ingest <source>

```
Usage: /ingest wiki/raw/articles/my-source.md [--mode strict|permissive]
```

- Reads source from `wiki/raw/`
- Creates ingestion plan (pages to create/update, contradictions)
- Presents plan for human approval
- Executes upon approval (writes to `wiki/`)
- Updates wiki/log.md
- Returns execution report

### /query <question>

```
Usage: /query "How does LLM Wiki differ from RAG?" [--return-format prose|table|json]
```

- Reads wiki/index.md to find relevant pages
- Reads relevant wiki pages
- Synthesizes answer with citations
- Can file answer back as new page if approved

### /lint

```
Usage: /lint [--mode check|auto-fix|report]
```

- Scans entire `wiki/` for:
  - Broken links (referenced files that don't exist)
  - Orphaned pages (no incoming links)
  - Contradictions between pages
  - Missing concepts (referenced but no page created)
- `check`: Report issues only
- `auto-fix`: Fix simple issues
- `report`: Generate summary

---

## Confusion Resolution: Key Debates

The LLM Wiki literature contains several documented tensions. Here's how this implementation resolves them:

| Tension | Debate | Resolution |
|---------|--------|-----------|
| **RAG vs. LLM Wiki** | Is RAG dead? | Both useful at different scales. This is pure LLM Wiki. |
| **Scale** | Enterprise ready? | Personal scale (~100–500 pages). Enterprise scalability out of scope. |
| **Simplicity** | "Just markdown" or complex? | Structured (not minimal) but disciplined via schema. |
| **Obsidian** | Essential or optional? | Optional. Uses portable markdown links, not wikilinks. |
| **Ingestion** | Batch or incremental? | Incremental & supervised (mandatory plan review). |
| **Query system** | Index or search infra? | Index + grep for ~500 pages; scalable search (qmd) later if needed. |
| **Models** | Cloud APIs or local? | Schema-agnostic. Agents implement per their capabilities. |
| **Contradictions** | Auto-resolve or flag? | Conservative by default (flag + human); optional aggressive mode. |
| **Authority** | Who resolves disputes? | Human by default; audit trail via git. |

---

## Tool Ecosystem

### Core Infrastructure

| Tool | Purpose | Usage |
|------|---------|-------|
| **Markdown** | Universal format | All wiki content, sources, schema |
| **Git** | Version control | `git add . && git commit` after each ingestion; audit trail |
| **YAML Frontmatter** | Structured metadata | Every wiki page; enables querying and filtering |

### IDE & Visualization (Optional)

| Tool | Purpose | Role |
|------|---------|------|
| **Obsidian** | Wiki IDE (optional) | Graph view, search, plugins; not required |
| **Web Clipper** | Browser extension | Convert articles to markdown; save to `raw/clippings/` |
| **Obsidian Plugins** | Extensions | Dataview (dynamic tables), Marp (slides), Local REST API |

### LLM Agents

| Agent | Purpose | Notes |
|-------|---------|-------|
| **Claude Code** | Wiki maintainer (Anthropic) | Reads schema; executes /ingest, /query, /lint |
| **Any LLM via MCP** | Schema-agnostic implementation | Local Ollama, vLLM, or API-based models |

### Local Model Options (If Using Local)

| Model | Context | Use Case | VRAM |
|-------|---------|----------|------|
| **Qwen2.5-14B-Instruct** | 128K | Balanced all-rounder | 16GB |
| **Llama-3.1-70B-Instruct** | 128K | Complex reasoning | 48GB |
| **Llama-3.1-8B** | 128K | Low VRAM environments | 8GB |

**Infrastructure:** Ollama (simple) or vLLM (high-throughput).

### Search at Scale

| Tool | When to Use | Purpose |
|------|-------------|---------|
| **Index + grep** | ~500 pages | Sufficient for small wikis |
| **qmd** | >500 pages | BM25/vector hybrid search over wiki |

---

## Implementation Templates

### Seed Template: index.md

Master catalog of all wiki pages. Update after each ingestion:

```markdown
---
title: Knowledge Index
type: index
tags: [meta, catalog]
updated: 2026-05-15
---

# Knowledge Index

Master catalog of all wiki pages. Updated after each ingestion.

## Concepts

| Title | Summary | Sources | Status |
|-------|---------|---------|--------|
| [LLM Wiki](llm-wiki.md) | Pattern for persistent, compounded knowledge | raw/articles/ | approved |
| ... | ... | ... | ... |

## Syntheses

| Title | Summary | Sources |
|-------|---------|---------|
| [Getting Started](llm-wiki.md) | Quick start for implementing LLM Wiki | this file | approved |
| ... | ... | ... |

---

Last updated: 2026-05-15  
Total pages: N/A (count during first ingest)
```

### Seed Template: log.md

Chronological record of all ingestions, queries, and lint passes:

```markdown
---
title: Wiki Activity Log
type: log
tags: [meta, timeline]
updated: 2026-05-15
---

# Wiki Activity Log

Chronological record of all ingestions, queries, and lint passes.

## 2026-05

### 2026-05-15 | ingest | LLM Wiki Framework

- Source: `raw/articles/llm-wiki-setup.md`
- Plan: Create wiki structure + consolidate documentation
- Approved by: Human (manual)
- Status: ✅ Completed
- Changes: +1 framework page, directory scaffold

---

(Log entries added chronologically; most recent first)
```

### Agent Skill Example: /ingest Implementation

Agents implementing `/ingest` should follow this pattern:

**Behavior:**
1. Read source from `wiki/raw/`
2. Extract key takeaways, concepts, entities
3. Create **ingestion plan** listing:
   - New pages to create (with titles, summaries)
   - Existing pages to update (with specific edits)
   - Links to add/remove
   - Any contradictions flagged
4. Present plan for human approval
5. Upon approval, execute plan:
   - Create/update wiki/ files
   - Add frontmatter to all pages
   - Update wiki/index.md
   - Append entry to wiki/log.md
6. Return execution report

**Example plan output:**
```
[INGESTION PLAN]
Source: raw/articles/my-article.md

📝 NEW PAGES TO CREATE:
  - wiki/concept-one.md (summary: Main idea from source)
  - wiki/concept-two.md (summary: Secondary pattern)

🔗 EXISTING PAGES TO UPDATE:
  - wiki/overview.md: Add 2 new citations
  - wiki/comparison.md: Add this source to comparison table

⚠️ CONTRADICTIONS FLAGGED:
  - Claim: "LLM Wiki scales to enterprise"
  - Source A: "Personal scale only"
  - Source B: "Enterprise-ready with 10k+ pages"
  - Resolution: Awaiting human decision

[AWAITING APPROVAL]
Do you approve this plan? (yes/no)
```

---

## Testing & Validation

Before full agent implementation, validate the design with a mock ingest:

**Step 1: Create test structure**
```bash
mkdir -p wiki/{raw/articles,index,log}
```

**Step 2: Prepare test source**
- Copy a sample article to `wiki/raw/articles/test.md`
- Manually extract 2-3 key concepts from the article

**Step 3: Simulate agent plan creation**
- List pages to create (with frontmatter)
- List existing pages to update
- Flag any contradictions

**Step 4: Review the plan**
- Are concepts correctly identified?
- Are links properly formatted (markdown, not wikilinks)?
- Is contradiction detection working?
- Does frontmatter look correct?

**Step 5: Validate output**
- Can all pages be read in any markdown editor?
- Do links work (relative paths)?
- Is YAML frontmatter properly formatted?

**Success criteria:**
- ✅ All new pages created with proper frontmatter
- ✅ Existing pages updated correctly
- ✅ Links are portable markdown (not vendor-specific)
- ✅ index.md and log.md updated
- ✅ Contradictions flagged for human review

---

## Implementation Questions

These clarifications help agents implement the system correctly:

1. **Pre-populating index.md:** Should agents auto-generate index from existing raw/ articles, or start with manual seed?
2. **Link conversion:** For existing wiki pages, should agents auto-convert Obsidian wikilinks (`[[Foo]]`) to markdown links (`[Foo](foo.md)`)?
3. **Frontmatter migration:** Should agents add frontmatter to all existing wiki pages retroactively, or only to new pages going forward?
4. **Aggressive contradiction mode:** Enable by default per-project, or leave disabled until explicitly requested?

---

## Getting Started

### Phase 1: Understand the Design

Read this file to understand:
- Pattern, vision, and philosophy
- Directory structure and file conventions
- Ingestion workflow (plan review gate)
- Contradiction policy
- Three operations (/ingest, /query, /lint)
- Implementation templates above

### Phase 2: Set Up Directory Structure

```bash
# Create raw/ subdirectories (if not already present)
mkdir -p wiki/raw/{articles,papers,clippings,books,projects}

# Create seed files
touch wiki/index.md wiki/log.md

# Verify structure
ls -la wiki/
```

Your wiki/ should have:
- `raw/{articles/, papers/, clippings/, books/, projects/}`
- `llm-wiki.md` (this file)
- `index.md` (seed: master catalog)
- `log.md` (seed: activity log)
- `overview.md`, `architecture.md`, etc. (content pages)

### Phase 3: Agent Implementation

Agents implementing LLM Wiki should:
- Follow the `/ingest` behavior pattern above
- Use the file conventions from section 3
- Respect the contradiction policy from section 4
- Update `wiki/index.md` and `wiki/log.md` after each operation
- Reference this file as the single source of truth

### Phase 4: Start Ingesting

1. Drop a source into `wiki/raw/articles/`
2. Ask agent: `/ingest wiki/raw/articles/my-source.md`
3. Review the ingestion plan
4. Approve or request modifications
5. Agent executes and reports

---

## Key Decisions

1. **Tool-Agnostic:** The wiki is portable markdown. Obsidian is optional, not required.
2. **Human in the Loop:** Plan review gates all ingestions (no surprise mutations).
3. **Conservative by Default:** Contradictions are flagged for human decision, not auto-resolved.
4. **Schema as Authority:** Single source of truth for agent behavior (no distributed config).
5. **Files, Not Apps:** Git-versioned, portable, no vendor lock-in.

---

## When to Use LLM Wiki

✅ **Good fit:**
- Personal knowledge base (100–500 pages)
- Research synthesis (consolidating sources)
- Project memory (specs, decisions, lessons)
- Agent-maintained documentation

❌ **Not a fit:**
- Enterprise document management (no RBAC, audit, ACID)
- Real-time collaborative editing (git-based, eventually consistent)
- Very large wikis (>10k pages; needs specialized search)

---

## Related Reading

- [wiki/llm-wiki.md](llm-wiki.md) (this file) — Canonical reference for LLM Wiki pattern and implementation
- wiki/index.md — Master catalog of all wiki pages (seed template provided above)
- wiki/log.md — Chronological record of ingestions and queries (seed template provided above)
- [wiki/raw/](raw/) — Source material (articles, papers, clippings, books, projects)
