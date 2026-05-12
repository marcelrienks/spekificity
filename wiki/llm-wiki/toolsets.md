# LLM Wiki Toolset Ecosystem

## Overview

LLM Wiki isn't a single tool; it's an orchestration of specialized tools working together. This document catalogs all tools mentioned across the articles, groups them by function, and describes the workflows where they're combined.

---

## Tool Categories

### 1. Core Infrastructure

**Markdown**
- Purpose: Universal format for all wiki content, sources, and schema
- Used in: Every implementation
- Workflow: Write once, read anywhere (git, Obsidian, static HTML viewers, search engines)

**Git**
- Purpose: Version control and backup for wiki files
- Used in: All implementations that care about data safety
- Workflow: `git add . && git commit` after each ingestion; `git checkout` to revert mistakes
- Key capability: `git diff` shows what the agent changed; audit trail is free

**YAML Frontmatter**
- Purpose: Structured metadata for pages (title, type, tags, sources, dates, status)
- Used in: All implementations (obsidian-markdown skill documents this)
- Workflow: Every wiki page has frontmatter; enables querying via Dataview, filtering, custom workflows

**Wikilinks** (`[[Concept]]` syntax)
- Purpose: Bidirectional internal linking with graph topology awareness
- Used in: Obsidian-based workflows
- Limitation: Obsidian-specific; not portable to all markdown readers
- Alternative: Standard markdown links in non-Obsidian implementations

---

### 2. IDE & Visualization

**Obsidian**
- Purpose: IDE for reading, browsing, and navigating the wiki
- Core features:
  - Graph view: visualizes concept network, shows hubs and orphans
  - Full-text search: native markdown search
  - Daily notes: for personal journaling
  - Plugin ecosystem: Dataview, Marp, Web Clipper, Local REST API
- Cost: Free for personal use
- Workflow: Open Obsidian alongside Claude Code; watch agent edits in real-time; browse graph to discover connections

**Obsidian Web Clipper**
- Purpose: Browser extension to convert web articles to markdown
- Workflow: One-click clipping from any browser; saved to `raw/clippings/`; triggers ingestion
- Alternative: `curl` + manual markdown conversion

**Obsidian Plugins**

| Plugin | Purpose | Workflow |
|--------|---------|----------|
| **Graph View** (built-in) | Visualize concept network | After ingest: open graph, look for new clusters or orphans |
| **Dataview** | Query pages by frontmatter; generate dynamic tables | Create dynamic "all ADRs by status" view; "all sources by date" |
| **Marp** | Markdown slide decks | Query response generates `.marp.md` file; open in Obsidian to present |
| **Local REST API** | Expose vault to MCP servers | Advanced: enables agent to run Obsidian commands and queries |
| **Sync** (paid) | Cloud backup and multi-device sync | Optional; not required for LLM Wiki |

---

### 3. LLM Agents

**Claude Code** (Anthropic)
- Purpose: Agent that reads schema and maintains the wiki
- Skills available: obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle
- Cost: Included with Claude API subscription
- Workflow: `claude` in terminal; reads CLAUDE.md schema every session; executes /wiki-ingest, /wiki-query, /wiki-lint commands
- Used in: Obsidian-based setups; can run with local OR cloud models

**Codex CLI** (OpenAI)
- Purpose: Similar to Claude Code but for OpenAI
- Workflow: Use AGENTS.md instead of CLAUDE.md; same commands
- Less developed ecosystem than Claude Code

**Cursor** (IDE)
- Purpose: IDE with integrated LLM agent
- Workflow: Edit CLAUDE.md; use agent to maintain wiki alongside code editing
- Not as specialized as Claude Code for wiki operations

**Gemini CLI** (Google)
- Purpose: Google's LLM agent runner
- Status: Emerging; less mature than Claude Code

**Any LLM via MCP** (local or remote)
- Purpose: Run any model (local Ollama, vLLM) through Model Context Protocol
- Workflow: Configure MCP server to expose wiki as tools; agent reads/writes via MCP calls
- Advantage: Works with any LLM, including local models running Llama or Qwen

---

### 4. Local Model Infrastructure (Optional)

**Ollama**
- Purpose: Simple local model runner
- Setup: `brew install ollama` (macOS) or equivalent; `ollama pull qwen2.5:14b`
- Models available: Qwen2.5-14B (recommended), Llama-3.1-70B, Llama-3.1-8B
- Cost: Free; compute cost is GPU time
- Throughput: ~1–2 tokens/sec on consumer GPU
- Use case: Experimentation, privacy-sensitive work, offline-first
- Workflow: Start Ollama on port 11434; point Claude Code at `http://localhost:11434`

**vLLM**
- Purpose: High-throughput local inference
- Setup: `pip install vllm`; `vllm serve Qwen/Qwen2.5-14B-Instruct --max-model-len 131072`
- Models: Same as Ollama, but with PagedAttention optimization
- Cost: Free; higher compute cost (GPU utilization)
- Throughput: 3x better than Ollama; 6x lower latency under concurrent load
- Use case: Batch ingestion, parallel research, production wikis
- Workflow: Spin up vLLM on port 8000; configure agent to point to OpenAI-compatible endpoint

**Specific Models**

| Model | Context | Best For | VRAM | Throughput |
|-------|---------|----------|------|------------|
| **Qwen2.5-14B-Instruct** | 128K | All-rounder | 16GB | Balanced |
| **Llama-3.1-70B-Instruct** | 128K | Complex reasoning | 48GB | Best quality, slower |
| **Qwen2.5-1M** | 1M tokens | Very long docs (entire books) | 80GB+ | For vLLM with chunked prefill |
| **Llama-3.1-8B** | 128K | Low VRAM (8GB) | 8GB | Fast but lower quality |

---

### 5. Cloud LLM APIs (Alternative to Local)

| Provider | Model | Cost | Data Privacy | Setup |
|----------|-------|------|--------------|-------|
| **Anthropic** | Claude 3.5 Sonnet | $3/$15 per M input/output tokens | TOS says input used for safety; check DPA | API key in env |
| **OpenAI** | GPT-4o, GPT-4-turbo | $5/$15 per M tokens | Data retention policy; can request deletion | API key |
| **Google** | Gemini 1.5 Pro/Flash | $1.50/$0.075 per M tokens | Depends on project; check DPA | OAuth + API key |

---

### 6. Search & Navigation (At Scale)

**qmd** (Local Search Engine)
- Purpose: BM25/vector hybrid search over markdown wiki with LLM re-ranking
- Setup: `npm install -g qmd` or build from source
- Interfaces: CLI (agent can shell out) or MCP server (native tool integration)
- Cost: Free and self-hosted
- When to use: Wiki grows past 500 pages; index.md alone becomes slow
- Workflow: `qmd search "vector database"` returns ranked results; agent reads top 5, synthesizes answer

**Obsidian's native search**
- Purpose: Full-text search built into Obsidian
- When to use: Small to medium wikis (~500 pages)
- Workflow: Ctrl+F in Obsidian; no agent involvement

**Vector Search** (optional, not used in base pattern)
- Tools: Pinecone, Weaviate, Milvus
- When to use: If you want semantic search on top of LLM Wiki
- Trade-off: Adds infrastructure; increases complexity; not necessary at small scale

---

### 7. Skill Infrastructure

**Steph Ango's Official Obsidian Skills** (in `.claude/skills/`)

| Skill | Purpose | Used by |
|-------|---------|---------|
| **obsidian-markdown** | Teaches wikilinks, callouts, YAML frontmatter, embeds, canvas | Every Obsidian-based setup |
| **obsidian-bases** | Databases and views via `.base` format | Dynamic tables, filters, sorts |
| **json-canvas** | Infinite canvas whiteboards with nodes and edges | Mind maps, relationship visualizations |
| **obsidian-cli** | Command-line operations via `obsdmd` | Automation scripts, batch operations |
| **defuddle** | Clean HTML-to-markdown extraction from URLs | Web clipping pipeline |

**Custom Skills** (you create for your domain)

| Skill | Purpose | Example from Tutorial |
|-------|---------|-----|
| **adr-writing** | ADR structure, numbering, status flow | Defines ADR-NNNN format, frontmatter, required sections |
| **debrief-writing** | Post-mortem structure, root cause analysis | Defines incident date, severity, action items, generalizable learning |
| **project-management** | (example) Track project notes, dependencies | Could define project hierarchy, phase gates |

---

### 8. Code & Development Tools

**Node.js / Express / React / Vite / Tailwind** (FreeBirdsCrew WhatsApp Bot)
- Purpose: Full-stack example of LLM Wiki backing a consumer application
- Components:
  - Backend (Express): Handles WhatsApp messages, queries wiki, returns responses
  - Frontend (React + Vite + Tailwind): Dashboard showing real-time bot conversations
  - Database (SQLite): Logs conversations
- Workflow: Edit wiki markdown files → Bot reads updated pages → Instant feature update
- Use case: Show that LLM Wiki can back production applications, not just personal notes

**Python / Matplotlib** (for chart generation)
- Purpose: Agents can generate visualizations as query responses
- Workflow: Query → Agent writes matplotlib code → Runs it → Saves PNG → Files to wiki → You view in Obsidian

**Marp** (markdown slide deck format)
- Purpose: Generate presentations from wiki content
- Workflow: Query triggers answer in Marp format → Saved as `.md` with Marp syntax → Open in Obsidian Marp plugin → Present
- Alternative: Hand off Marp file to keynote or PowerPoint conversion

---

### 9. Data Export & Portability

**Git** (already covered, but key for portability)
- Push to GitHub/GitLab/Forgejo: Your wiki becomes a git repository
- Public or private: Your choice
- Enables: Branching (experiment with different ingestions), collaboration (multiple people can contribute), archival (GitHub never deletes public repos)

**Static HTML Export** (Pratiyush/llm-wiki)
- Purpose: Generate browsable offline wiki without running LLM
- Workflow: `llmwiki build` → generates `/docs/` → serve with `http-server` or GitHub Pages
- Benefit: Shareable, no API keys needed, works offline

**JSON-LD / RSS** (Pratiyush/llm-wiki)
- Purpose: Machine-readable formats for federation and consumption by other systems
- Workflow: Export wiki as JSON-LD for semantic web; RSS for subscriptions
- Use case: Allow other agents to consume your wiki as input

---

## Workflows: Tool Combinations

### Workflow A: Personal Researcher (Offline-First)

**Tools:** Obsidian + Ollama (Qwen2.5-14B) + Claude Code + Git

**Steps:**
1. Find paper → Use Obsidian Web Clipper → Save to `raw/papers/`
2. Terminal: `claude`
3. In Claude: `/wiki-ingest raw/papers/transformer-attention.pdf`
4. Agent: Uses `defuddle` skill → Reads paper → Creates `wiki/concepts/Attention-Mechanism.md` → Updates `wiki/index.md` → Proposes plan
5. You: Review plan → Approve
6. Agent: Executes → Reports changes
7. Obsidian: Open graph view → See new connections
8. Terminal: `git add . && git commit -m "ingest: transformer paper"`
9. Query: `/wiki-query "how do transformers differ from RNNs?"`
10. Agent: Reads `[[Attention-Mechanism]]`, `[[Recurrent Neural Networks]]`, synthesizes answer with citations

**Toolset value:** Fully local (privacy), no API costs, discoverable knowledge graph, version history

---

### Workflow B: Team Knowledge Capture (Cloud + Supervision)

**Tools:** Obsidian + Claude Code (cloud API) + Git + Slack integration (hypothetical)

**Steps:**
1. Meeting happens → Transcript posted to Slack
2. Someone: `/wiki-ingest https://slack.com/archives/.../p123`
3. Agent: Fetches transcript → Identifies decisions → Creates `dev/adr/ADR-NNNN-decision.md` → Updates `wiki/syntheses/May-2026-Decisions.md`
4. Agent: Posts plan to Slack with diff
5. Team: Reviews in Slack thread → Approves
6. Agent: Commits changes to `team-wiki` repo
7. Weekly: `/wiki-query "what decisions did we make on auth this quarter?"`
8. Agent: Searches across `dev/adr/` → Synthesizes answer → Posts to wiki as new page

**Toolset value:** Centralized knowledge, audit trail, async review, compounding decisions

---

### Workflow C: Research Synthesis (Scale-Up)

**Tools:** vLLM (Qwen2.5-14B or Llama-3.1-70B) + Obsidian + Claude Code + qmd + Git

**Steps:**
1. Large batch of papers to ingest (~50 PDFs)
2. Terminal: `vllm serve Qwen/Qwen2.5-14B-Instruct --max-model-len 131072`
3. Terminal 2: `claude`
4. Agent: `/wiki-ingest raw/papers/batch-2026-05/*.pdf --parallel 5`
5. Agent: Uses vLLM parallelism → Ingests 5 papers simultaneously → Updates wiki systematically
6. Obsidian: Graph view shows emerging research clusters
7. Query: `/wiki-query "what are the three main approaches to agent reasoning?"`
8. Agent: Uses `qmd` search → Finds 20+ relevant pages → Synthesizes thesis → Creates `wiki/syntheses/Agent-Reasoning-Trends.md` with citations and comparison table
9. Generate presentation: Marp slide deck from synthesis
10. Git: Push to GitHub with clear commit message → Research becomes citable

**Toolset value:** Parallel ingestion (fast), sophisticated search (accurate), presentation-ready output, shareable

---

### Workflow D: Developer's Second Brain (ADRs + Debriefs + Research)

**Tools:** Obsidian + Claude Code + dev/ zone (4-zone model) + Dataview plugin + Git

**Ongoing:**
1. Write technical decision (ADR-0028-prefer-postgres-over-mongodb)
   - Create in `dev/adr/ADR-0028-...md`
   - Agent: Proposes wikilinks to related `[[ADR-0003]]`, `[[Performance-Tradeoffs]]`
   - You: Review + approve

2. Production incident (2026-05-10 database-lockup)
   - Create `dev/debriefs/2026-05-10-db-lockup.md`
   - Agent: Checks for related ADRs, surfaces lessons learned
   - You: Document root cause
   - Agent: Extracts "generalizable learning" and files as new page `wiki/concepts/Connection-Pool-Saturation.md`

3. Weekly: Use Dataview to create dashboard
   - Dataview query: `LIST WHERE type = "adr" AND status = "accepted"`
   - Shows all decisions grouped by project
   - Dataview query: `TABLE severity, created FROM "" WHERE type = "debrief"` 
   - Shows all incidents by severity

4. Query: "What was our reasoning for Postgres in ADR-0028?"
   - Agent: Finds ADR, returns decision + consequences + alternatives
   - You: Share with new team member as onboarding

**Toolset value:** Decisions are artifact, incidents become learning, knowledge is searchable, onboarding time drops

---

### Workflow E: Desktop App (Lowest Friction)

**Tools:** nashsu/llm_wiki (Tauri + React app) + Local LLM (Ollama or vLLM) + Git (optional)

**Steps:**
1. Install app: Download `.dmg` (macOS) / `.exe` (Windows) / `.AppImage` (Linux)
2. Settings: Point at Ollama (port 11434) or vLLM (port 8000)
3. Click "Ingest URL" → Paste link → App fetches, uses `defuddle`, displays preview
4. Approve → App creates wiki pages automatically
5. Open Knowledge Graph panel → Visualize connections
6. Search box: Type query → Results ranked
7. Export: Button to save as HTML static site or PDF

**Toolset value:** No terminal needed, GUI feedback loop, graph visualization immediate, beginner-friendly

---

### Workflow F: Transcript Miner (Passive Learning)

**Tools:** Pratiyush/llm-wiki + Chat transcript files (Claude Code, Cursor, Codex `.jsonl` files) + Static HTML viewer

**Setup (one-time):**
1. Copy tool: `pip install llm-wiki`
2. Point to transcript folder: `~/.config/cursor/history` or similar
3. Run: `llmwiki sync` → Processes all `.jsonl` files
4. Run: `llmwiki build` → Generates static HTML
5. Serve: `llmwiki serve` → Opens `http://localhost:8080`

**Ongoing:**
- Agent transcripts accumulate
- Weekly: `llmwiki sync && llmwiki build`
- Wiki auto-updates with all conversations
- Search conversations without re-running LLM
- No API costs for browsing

**Toolset value:** Zero setup friction after install, zero inference cost, captures history automatically, converts chat to knowledge

---

## Reference Implementations: Four LLM Wiki Projects

These are the four most mature GitHub implementations of the LLM Wiki pattern. Each takes a different architectural approach. Understanding their intent and trade-offs helps inform design decisions for your own implementation.

### 1. nashsu/llm_wiki — Desktop GUI with Knowledge Graph

**GitHub:** [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)

**Intent:** Make LLM Wiki accessible to non-technical users through a polished desktop application. Prioritize visual feedback and graph discovery over terminal-based workflows.

**Key Architecture:**
- **Frontend:** Tauri (Rust) + React 19 desktop app
- **Layout:** Three-column (Knowledge Tree | Chat | Live Preview)
- **Knowledge Graph:** Visual graph with community detection, relevance scoring
- **Multi-source:** PDFs, DOCX, PPTX, images, video, web URLs
- **Ingest workflow:** Two-step (analyze → generate) with every claim traced to source
- **Search:** Built-in ranked search; supports OpenAI, Anthropic, Google, Ollama, custom endpoints
- **Export:** HTML, static site, PDF
- **Extensions:** Chrome clipper for web pages

**Use Case:** Best for:
- Users who prefer GUI over terminal/code
- Visual thinkers who benefit from knowledge graph exploration
- Teams wanting a "knowledge app" feel rather than markdown files
- Mixed-media research (PDFs + videos + web pages)

**Spekificity Context:** Could use nashsu/llm_wiki as the reference GUI for ingest/query workflows. The two-step ingest (analyze → generate) with approval gates matches the "present plan before execute" pattern described in your TODO.

---

### 2. nvk/llm-wiki — Agent Plugin for Parallel Research

**GitHub:** [nvk/llm-wiki](https://github.com/nvk/llm-wiki)

**Intent:** Embed LLM Wiki as a plugin into existing LLM agent environments (Claude Code, Codex). Enable "parallel multi-agent research" — spawn 5–10 concurrent agents investigating a topic from different angles, then synthesize into cross-referenced articles.

**Key Architecture:**
- **Integration:** Works as plugin for Claude Code, OpenAI Codex, or any LLM via AGENTS.md
- **Parallel research:** 5–10 concurrent agents with different "investigative angles"
- **Thesis-driven synthesis:** Evaluates arguments for/against each claim
- **Output formats:** Wiki pages, reports, slides, study guides, decision matrices
- **Zero dependencies:** Uses only agent's native file read/write and web fetch
- **Universal:** AGENTS.md pattern works with any LLM (local or cloud)

**Use Case:** Best for:
- Power users already in Claude Code or Codex wanting to research topics quickly
- Complex topics requiring multi-angle investigation (trade-offs, comparative analysis)
- Generating reports and presentations directly from research
- Anyone who wants agent-native workflow (no separate app)

**Spekificity Context:** The parallel research pattern is valuable for your own speckit workflow. When analyzing a topic (e.g., "compare RAG vs LLM Wiki"), you could spawn agents to investigate from different angles (implementation, performance, enterprise readiness, academic merit) simultaneously. The thesis-driven synthesis matches your desire to distill consensus vs. confusion.

---

### 3. Pratiyush/llm-wiki — Transcript Miner (Passive Knowledge Extraction)

**GitHub:** [Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)

**Intent:** Convert existing LLM conversation transcripts into a browsable, searchable knowledge base without needing to run a new LLM. Mine all past conversations (Claude Code, Cursor, Codex, Copilot, Obsidian) to extract accumulated learning.

**Key Architecture:**
- **Input:** `.jsonl` transcript files from Claude Code, Cursor, Codex CLI, Gemini CLI, Copilot, Obsidian
- **Processing:** Static HTML generation (no runtime LLM needed)
- **Page lifecycle:** draft → verified → stale → archived
- **Privacy:** Auto-redacts API keys and usernames before publishing
- **Interfaces:** Static HTML site, MCP server (with 12 tools), JSON-LD export, RSS feed
- **Search:** Offline browsing, no API key required
- **Versions:** Export in formats other agents can consume (llms.txt, JSON-LD, RSS)

**Use Case:** Best for:
- Developers with months of LLM agent conversation history that should be preserved as knowledge
- Creating an "institutional memory" from past research sessions
- Building a knowledge base without the overhead of active ingestion (passive extraction)
- Sharing research with others who don't have API keys
- Enabling other AI systems to learn from your historical research

**Spekificity Context:** As the spekificity project accumulates sessions (speckit.specify, speckit.plan, speckit.tasks runs), Pratiyush's approach could automatically extract lessons learned and decision reasoning from chat logs. This directly addresses your TODO item B.5 ("lessons learnt must capture enough detail to replace reading the spec in future sessions").

---

### 4. lucasastorian/llmwiki — MCP-Powered Auto-Maintenance

**GitHub:** [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki)

**Intent:** Use Model Context Protocol (MCP) to allow Claude to continuously maintain a wiki as files change. Treat the filesystem as the source of truth; the wiki is a generated, always-in-sync layer on top.

**Key Architecture:**
- **Input:** Any folder of documents (markdown, PDF, images, code, data files)
- **Model Context Protocol:** MCP server exposes wiki operations as native agent tools
- **Auto-sync:** Wiki pages update when underlying files change
- **Indexing:** Local SQLite index; no external search service required
- **OCR:** Optional Mistral integration for scanned PDFs and image text
- **Storage:** Python API backend + React web UI
- **Link maintenance:** Auto-updates links, summaries, and citations

**Use Case:** Best for:
- Researchers with large document collections who want Claude to organize them automatically
- Projects where the "source of truth" is files (not a database), but you want wiki navigation
- Developers who want tight integration with MCP ecosystem
- Anyone who wants the agent to keep the wiki in sync automatically (no manual sync steps)

**Spekificity Context:** lucasastorian/llmwiki's MCP approach aligns with your skill and agent architecture. Instead of manually calling `/wiki-ingest`, the agent could maintain the wiki continuously as new files appear in `specs/` or `skills/`. This matches your emphasis on automation and active maintenance.

---

## Design Decision Matrix: Which Reference Implementation to Follow

| Dimension | nashsu | nvk | Pratiyush | lucasastorian |
|-----------|--------|-----|-----------|---------------|
| **Entry barrier** | GUI (low) | Terminal/agent (medium) | CLI (medium) | MCP (high) |
| **Setup time** | 5 min | 10 min | 10 min | 1 hour |
| **Ongoing maintenance** | Click buttons | `/wiki` commands | `sync && build` | Auto |
| **Best for scale** | <1000 pages | <500 pages | <500 pages | Any |
| **Visualization** | Excellent | None | None | Basic |
| **Offline use** | No | Yes | Yes | No |
| **Multi-source** | Yes | No (markdown focus) | No | Yes |
| **Parallel workflows** | No | Yes | No | No |
| **Privacy** | Depends on LLM | Local or cloud | Local | Depends on LLM |

---

## Recommended Starter Toolkit

**For beginners:**
- Obsidian + Claude Code + Git
- Setup: 30 minutes
- Cost: Free
- Capability: 95% of use cases

**For researchers:**
- Add: Ollama (local Qwen2.5-14B) + qmd (when wiki hits 500 pages)
- Setup: 2 hours
- Cost: Free (GPU time only)
- Capability: offline, scale to 1000+ pages

**For teams:**
- Add: Slack integration + Git + Dataview plugin
- Setup: 1 day
- Cost: Depends on API usage; typically $10–50/month
- Capability: centralized decisions, async workflows

**For production:**
- Add: vLLM + MCP integration + monitoring + backup
- Setup: 1 week
- Cost: $50–500/month (API + infrastructure)
- Capability: reliable, auditable, enterprise-ready

---

## Tool Maturity Matrix

| Tool | Stability | Documentation | Community | Recommendation |
|------|-----------|----------------|-----------|-----------------|
| Obsidian | Stable | Excellent | Large | Use |
| Claude Code | Stable | Good | Growing | Use |
| Git | Stable | Excellent | Huge | Use |
| Ollama | Stable | Good | Growing | Use |
| vLLM | Stable | Good | Academic | Use if scaling |
| qmd | Alpha | Minimal | Small | Use if 500+ pages |
| nashsu/llm_wiki | Beta | Good | Small | Use if GUI preferred |
| nvk/llm-wiki | Beta | Minimal | Tiny | Use if already in Claude Code |
| Pratiyush/llm-wiki | Beta | Good | Small | Use for transcript mining |
| lucasastorian/llmwiki | Alpha | Minimal | Tiny | Use if MCP needed |

---

## Gaps & Opportunities

**Not yet well-solved:**
- Multi-agent write coordination (preventing race conditions in wiki/)
- Enterprise RBAC (restricting agents from sensitive zones)
- Semantic versioning of wiki pages (track when a concept "shifts meaning")
- Automated wiki health scoring (quantify "freshness" and "completeness")
- Cross-wiki federation (linking two separate wikis)
- LLM fine-tuning pipeline from wiki data (generate synthetic training data)

**Opportunities for tooling:**
1. **Wiki indexer + dashboard:** Metrics on ingest velocity, concept density, orphan detection
2. **MCP universal adapter:** Unified interface for all LLM agents (Claude, Codex, Gemini, open source)
3. **Collaborative edit tool:** Real-time wiki editing with conflict resolution
4. **Data exporter:** Convert wiki to structured formats (relational DB, knowledge graph, RDF)
5. **Fine-tuning pipeline:** Generate training datasets from wiki → Fine-tune domain models

