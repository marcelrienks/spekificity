# LLM Wiki Vision

## Overview

LLM Wiki is a pattern for building persistent, compounding knowledge bases where an AI agent reads source materials, extracts key concepts, and maintains a structured markdown wiki that grows richer with each new source added. It solves the fundamental problem that traditional knowledge management — both RAG systems and human-maintained wikis — has never solved: **knowledge should compound, not evaporate**.

---

## Intentions

**What LLM Wiki aims to do:**

- **Solve the compounding problem:** Traditional systems (RAG, chat history, note-taking) treat every interaction as stateless. LLM Wiki treats every interaction as an investment that strengthens the knowledge base permanently.

- **Eliminate the bookkeeping burden:** Humans abandon wikis because the maintenance cost grows faster than the value. LLMs can update cross-references, flag contradictions, and maintain consistency across dozens of pages in one pass. The system automates the tedious work that kills personal knowledge bases.

- **Enable synthesis at scale:** RAG rediscovers knowledge from scratch on every query. LLM Wiki pre-compiles synthesis so that complex questions requiring five documents to piece together are already answered by the interconnected wiki.

- **Make knowledge persistent without being cumbersome:** Unlike enterprise knowledge management systems, this is intentionally personal, local, and portable — just markdown files, no vendor lock-in, no cloud dependency.

---

## Philosophy

**Underlying principles:**

### 1. **The Wiki is a Persistent, Compounding Artifact**
Knowledge is not ephemeral chat history that vanishes when the session ends. It is a living asset that grows monotonically and becomes more valuable over time as new sources feed into it and connections deepen.

### 2. **Compilation Over Retrieval**
The heavy lifting happens at ingest time, not query time. When a new source enters the system, the LLM reads it, understands it, integrates it into existing knowledge, updates cross-references, and flags contradictions. By the time you ask a question, the synthesis is already baked in.

### 3. **Human Curates, LLM Maintains**
The human's job is to curate sources, direct analysis, ask good questions, and think about what it all means. The LLM's job is everything else: summarizing, cross-referencing, filing, bookkeeping, and keeping the wiki consistent. This division of labor is what makes the system scale.

### 4. **Files Over Apps**
The wiki is a git repository of plain markdown files. No database. No vendor-specific format. No API lock-in. This guarantees data sovereignty, portability, and version control for free.

### 5. **Structure Emerges From Constraints**
A configuration document (CLAUDE.md, AGENTS.md, or equivalent schema) tells the LLM exactly how to behave. This transforms a generic chatbot into a disciplined wiki maintainer. The schema is co-evolved with the domain; it improves as you use it.

### 6. **Knowledge Should Be Accessible to Reasoning**
The difference between a RAG system stuffing 50 random chunks into context and an LLM reading a well-organized encyclopedia is profound. The structured wiki allows the agent to reason effectively because the information is pre-synthesized, cross-referenced, and organized by topic, not by vector similarity.

---

## Methodology

**How it works:**

### Architecture: Three Layers

1. **Raw Sources** (immutable)
   - Your curated collection of original materials: articles, papers, PDFs, transcripts, notes, images.
   - The LLM reads from this layer but never modifies it.
   - This is the source of truth.

2. **The Wiki** (LLM-maintained)
   - A directory of markdown files: concept pages, entity pages, syntheses, comparisons, an index.
   - The LLM owns this layer entirely. It creates pages, updates them, maintains cross-references, keeps everything consistent.
   - You read it; the LLM writes it.
   - Pages are interlinked via wikilinks (`[[Concept]]`) so they form a navigation graph.

3. **The Schema** (configuration)
   - A single document (CLAUDE.md, AGENTS.md, or custom) that defines:
     - How the wiki is organized and structured
     - Naming conventions and page templates
     - Frontmatter format (YAML metadata)
     - Workflows for ingestion, querying, and maintenance
     - Tone, voice, and editorial guidelines
     - Rules about which zones the LLM can write to
   - This is the constitution the agent operates under.
   - It makes the LLM a disciplined wiki maintainer, not a generic chatbot.

### Three Operations

1. **Ingest**
   - You drop a new source into raw/ and tell the LLM to process it.
   - The LLM reads the source, discusses takeaways with you, writes a summary page, updates the index.
   - A single source typically touches 10–15 wiki pages simultaneously (existing concept pages get updated, new concepts get created).
   - The agent identifies new entities (people, companies, projects) and new concepts, then links them bidirectionally.
   - You review the ingestion plan before the agent writes; this is the human gate.

2. **Query**
   - You ask a question against the wiki.
   - The LLM searches (or browses) relevant wiki pages, reads them, synthesizes an answer with citations.
   - The answer can take many forms: prose, a markdown page, a comparison table, a visualization.
   - Crucially: good answers are filed back into the wiki as new pages. Your explorations become permanent knowledge.

3. **Lint** (Maintenance)
   - Periodically, the LLM health-checks the entire wiki.
   - It looks for contradictions, stale claims superseded by newer sources, orphan pages, missing concepts, broken links, data gaps.
   - The agent suggests new questions and sources to investigate.
   - The wiki heals itself through this continuous maintenance cycle.

### Two Navigation Aids

- **index.md** — A content-oriented catalog. Every page listed with a link, a one-line summary, organized by category. Updated on every ingest. At moderate scale (~100 sources, ~hundreds of pages), the index is sufficient for LLM navigation without embedding-based search.

- **log.md** — An append-only chronological record. Each entry prefixed consistently (e.g., `## [2026-04-02] ingest | Article Title`). Helps the LLM understand what's been done recently and gives you a timeline of the wiki's evolution.

---

## Use Cases

**Where LLM Wiki fits best:**

### 1. Personal Knowledge Management
- Track goals, health, psychology, self-improvement.
- File journal entries, articles, podcast notes, research alongside each other.
- Build a structured picture of yourself over months and years.
- **Why it wins:** Scale is inherently personal (hundreds of documents, not millions). Value of compounding is highest when one user sees connections emerge over time.

### 2. Research Synthesis
- Read papers, articles, reports over weeks or months.
- Build a comprehensive wiki with an evolving thesis.
- Watch how new findings contradict, modify, or strengthen earlier claims.
- **Why it wins:** The wiki becomes your externalized understanding. The LLM never forgets to update cross-references or flag contradictions. This is the dream workflow for any researcher.

### 3. Reading a Book
- Build a companion wiki as you read, chapter by chapter.
- Create pages for characters, themes, plot threads, motifs, relationships.
- By the end, you have a rich, interconnected reference for the book.
- **Why it wins:** Similar to the Tolkien Gateway (thousands of fan wiki pages), but built by an LLM as you read, with all cross-references maintained automatically.

### 4. Business / Team Knowledge
- Feed the wiki with Slack threads, meeting transcripts, project documents, customer calls.
- Maintain an internal wiki that stays current because the AI does the maintenance nobody wants to do.
- Possibly with human review loops for high-stakes updates.
- **Limitation:** At enterprise scale (multi-tenant, 50 agents writing simultaneously, compliance requirements), this hits scalability gaps (no RBAC, no ACID transactions, no audit trails). But for small teams and startups, it's a superpower.

### 5. Developer's Second Brain
- Store ADRs (Architecture Decision Records), incident debriefs, project notes, technical reading, code snippets.
- The wiki synthesizes your decisions alongside your learning, so future "should we use pgvector?" queries find your prior analysis of the same trade-off.
- **Why it wins:** Decisions stop evaporating into Slack threads. Your thinking compounds in one place.

### 6. Competitive Analysis, Due Diligence, Trip Planning, Hobby Deep-Dives
- Anything where you're accumulating knowledge over time and want it organized rather than scattered across browser tabs, notebooks, and email.

---

## Architectures

**Structural patterns and implementations:**

### Physical Zone Separation

The vault/wiki is organized into distinct zones with different rules:

- **raw/** — You curate, LLM reads. Immutable.
- **wiki/** — LLM maintains. You rarely edit by hand.
- **dev/** (optional) — Collaborative. You and LLM work together (ADRs, debriefs, projects).

This separation prevents accidental data loss and enforces the contract: agent knows exactly what it can write to.

### File Structure Convention

- **Index file** (`wiki/index.md`) — Master catalog, updated on every ingest.
- **Log file** (`wiki/log.md`) — Chronological record of ingestions, queries, lint passes.
- **Concept pages** (`wiki/concepts/Concept-Name.md`) — Encyclopedia-style articles on key ideas.
- **Entity pages** (`wiki/entities/Person-Name.md`) — Pages for people, companies, projects.
- **Synthesis pages** (`wiki/syntheses/*.md`) — Higher-order compilations (comparisons, overviews, theses).
- **Source summaries** (`wiki/sources/*.md`) or inline in raw/ — Digests of ingested materials.

### Frontmatter Convention

Every page maintains YAML metadata:
```yaml
---
title: <Title>
type: concept | entity | synthesis | debrief | adr | project
tags: [tag1, tag2, kebab-case]
sources: 
  - "[[raw/clippings/...]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

This enables both human readability and machine queries (e.g., Obsidian Dataview plugins).

### Wikilink Convention

All internal links use **wikilinks** (`[[Page Name]]`), not standard markdown links. This:
- Enables bidirectional link detection (graph view shows what points to what).
- Allows graph visualization showing concept clusters and orphan pages.
- Makes navigation discoverable and visible.

### Implementation Patterns

Multiple reference implementations exist:

1. **Desktop app** (nashsu/llm_wiki) — GUI with knowledge graph visualization, multi-source support (PDF, DOCX, images, video, URLs).
2. **Agent plugin** (nvk/llm-wiki) — Works within Claude Code, Codex, or any agent via AGENTS.md; supports parallel multi-agent research.
3. **Transcript miner** (Pratiyush/llm-wiki) — Processes .jsonl chat transcripts into a browsable offline wiki; works without running a new LLM.
4. **MCP-powered** (lucasastorian/llmwiki) — Uses Model Context Protocol so Claude can auto-maintain the wiki as files change; treats filesystem as source of truth.

Each implementation is opinionated about different things (GUI vs CLI, cloud vs local, new vs archived), but the pattern itself is consistent.

### Tooling Ecosystem

- **Obsidian** — IDE for reading and browsing the wiki. Graph view reveals topology, Dataview enables queries, Web Clipper streamlines ingestion.
- **Claude Code / Codex / Gemini CLI** — Agents that read the schema and maintain the wiki.
- **Git** — Version control (free backup, history, branching).
- **qmd** (optional) — Local search engine for wiki pages with BM25/vector hybrid search.

---

## Key Insight: The Vannevar Bush Connection

Karpathy explicitly references Vannevar Bush's **Memex** (1945), which described a personal, curated knowledge store with "associative trails" linking related ideas across documents. Bush's vision was private, actively curated, with connections between documents as valuable as the documents themselves.

The problem Bush couldn't solve: **who does the maintenance?**

Humans abandon wikis because the bookkeeping burden grows faster than the value. LLMs don't get bored, don't forget cross-references, and can touch 15 files in one pass. An LLM Wiki makes Bush's 80-year-old vision finally practical by automating the maintenance work that no human wants to do.

---

## Why This Works

1. **No rediscovery:** Knowledge is compiled once and kept current, not re-derived on every query.
2. **No chunking destruction:** Unlike RAG, which fragments documents into lossy chunks, the wiki preserves structure and context.
3. **Maintenance is automated:** The cost of maintenance is near zero because the LLM does it.
4. **Synthesis is precompiled:** Complex multi-source questions are answered by the wiki's interconnections, not by the LLM's ability to juggle fragments in context.
5. **Knowledge compounds:** Each new source strengthens existing pages, enabling serendipitous connections and discovering gaps.
6. **Auditable and portable:** The wiki is just markdown files in git. You can see what changed, revert mistakes, and take your knowledge with you.

---

## Consensus Across Articles

All six articles agree on:

- **The core problem:** Traditional systems treat knowledge as stateless and ephemeral. LLM Wiki makes it persistent and compounding.
- **The solution:** An LLM agent that reads sources and maintains a structured markdown wiki with cross-references, flagged contradictions, and continuous synthesis.
- **The three layers:** Raw sources (immutable), wiki (LLM-maintained), schema (configuration).
- **The three operations:** Ingest (new sources), Query (answered by the wiki), Lint (maintenance and health-checking).
- **Why humans abandon wikis:** Maintenance burden. LLM solves this.
- **The philosophical foundation:** Vannevar Bush's Memex — finally practical with LLMs.
- **Scale limitations:** Works great at personal scale (100–500 sources, ~1–2 years of use). Enterprise scalability gaps exist (RBAC, ACID, audit trails) but are acknowledged, not fatal for small teams.
- **Practical implementations:** All agree on git + markdown + Obsidian as the foundation, with multiple agent-integration patterns viable.

