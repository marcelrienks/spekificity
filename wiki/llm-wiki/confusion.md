# LLM Wiki: Areas of Contradiction & Confusion

## Overview

While all six articles agree on the core **pattern** (persistent wiki maintained by LLM), they diverge significantly on **scope, scale, implementation, and positioning**. This document captures the substantive disagreements and tensions.

---

## 1. Is RAG Dead? Or Just Different?

### Contradiction

**Position A (Strong):** "RAG is dead. Karpathy's LLM Wiki is the future."
- Article: *Karpathy's LLM Wiki is the future* — title frames RAG as obsolete.
- Reasoning: LLM Wiki solves the fundamental problems RAG has (chunking destroys context, stateless rediscovery, no accumulation).

**Position B (Pragmatic):** "RAG and LLM Wiki are different tools for different scales and use cases."
- Articles: *Andrej Karpathy Killed RAG. Or Did He?* and *LLM Wiki — Andrej Karpathy's Idea*
- Reasoning: RAG works well for enterprise (millions of documents, unpredictable queries, real-time data, multi-tenant security). LLM Wiki works best at personal scale (hundreds to low thousands). Both useful; neither kills the other.

**Position C (Skeptical):** "Karpathy just renamed the cache layer and gave it a fancier name."
- Article: *Andrej Karpathy Killed RAG. Or Did He?*
- Reasoning: Caching and deduplication are not new; LLM Wiki is clever bookkeeping, not a paradigm shift.

### Resolution Issue
- **For practitioners:** Which positioning is correct determines whether you bet on LLM Wiki for your company's knowledge system or keep using enterprise RAG infrastructure.
- **For positioning:** The "RAG is dead" framing is marketing; the pragmatic view is technically more honest but less exciting.

---

## 2. Enterprise Scalability: Acknowledged Gap or Solved Problem?

### Contradiction

**Position A (Honest):** "This is a personal knowledge weapon, not an enterprise platform. Yet."
- Article: *Andrej Karpathy Killed RAG. Or Did He?*
- Details: No RBAC (can't restrict agents from sensitive data), no ACID transactions (race conditions when multiple agents write simultaneously), no audit trails (required by regulated industries), flat-file systems can't handle petabyte-scale data.
- Implication: Don't use at enterprise scale.

**Position B (Dismissive):** "Enterprise scalability is the elephant in the room, but it's acknowledged, not fatal."
- Article: *LLM Wiki Vision* (synthesis)
- Reasoning: Small teams and startups don't need RBAC or ACID. The pattern is opinionated but not broken.

**Position C (Practical):** The FreeBirdsCrew WhatsApp bot is described as a working production system.
- Article: *Karpathy's LLM Wiki is the future*
- Implication: It scales to at least "small deployed app" level, which is enterprise-ish.

### Resolution Issue
- **Unclear:** Does "production" mean "running on one person's device" or "serving 1000 users"?
- **Risk:** Building on LLM Wiki at scale and hitting ACID/RBAC constraints mid-project.

---

## 3. Simplicity vs. Complexity: "Just Markdown" vs. "Complex Ecosystem"

### Contradiction

**Position A (Simple):** LLM Wiki is intentionally minimal.
- Article: *LLM Wiki.md* (Karpathy gist) — "This document is intentionally abstract. It describes the idea, not a specific implementation."
- Implication: Just a folder of markdown files + a schema document. Setup is trivial.

**Position B (Complex):** Full implementation requires multiple layers of infrastructure.
- Article: *Building a Complete Personal Harness LLM Wiki + Developer's Second Brain in Obsidian*
- Details: Requires CLAUDE.md (detailed schema), four separate zones (raw, wiki, dev, schema), custom skills (adr-writing, debrief-writing), slash commands with allowed-tools, git versioning, Obsidian plugins, MCP servers.
- Setup time: "Block out an afternoon."
- Implication: "Just markdown" is misleading. Production use requires careful architecture.

**Position C (Pragmatic):** Simplicity is an aspiration, not reality.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next*
- Details: Discusses four different implementations (nashsu, nvk, Pratiyush, lucasastorian), each taking a different approach to tooling.
- Implication: "Just markdown" doesn't match any real implementation.

### Resolution Issue
- **For users:** Is the 5-minute setup or the afternoon-long setup the real ask?
- **For marketing:** "Files over apps" sounds simple but requires sophisticated orchestration in practice.

---

## 4. Zone Model: Three Layers or Four?

### Contradiction

**Position A (Karpathy):** Three layers only.
- Article: *LLM Wiki.md*
- Structure: Raw sources (immutable), Wiki (LLM-maintained), Schema (configuration).

**Position B (Tutorial Implementation):** Four zones needed.
- Article: *Building a Complete Personal Harness*
- Structure: Raw (curated, immutable), Wiki (LLM-maintained), Dev (collaborative — ADRs, debriefs, projects), Schema (configuration).
- Reasoning: Developers need a space to do work (ADRs, debriefs) that's separate from the synthesized wiki and separate from raw sources. The boundary prevents drift and maintains discipline.

### Resolution Issue
- **Design question:** Is the four-zone model a refinement of Karpathy's three, or a different pattern?
- **For teams:** Should developer work (ADRs, decisions) live in the wiki or in a separate zone?
- **No clear winner:** Both models work; the choice depends on your use case.

---

## 5. Obsidian: Essential or Optional?

### Contradiction

**Position A (Optional):** Obsidian is the human interface, but not mandatory.
- Article: *LLM Wiki.md* — "The right way to use this is to share it with your LLM agent and work together..."
- Implication: Obsidian is helpful but not required; you could use any markdown editor or even a static HTML viewer.

**Position B (Essential):** Obsidian's graph view and plugins are critical.
- Article: *Building a Complete Personal Harness* — describes Obsidian Web Clipper, graph view, Dataview plugin, Marp, local attachment handling.
- Implication: Without Obsidian, you lose visualization and query capabilities.

**Position C (Agnostic):** Multiple viewers, same wiki.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next*
- Details: Describes four implementations. Pratiyush's produces static HTML (no Obsidian needed). nashsu's desktop app has its own graph view (Obsidian not used).

### Resolution Issue
- **Portability claim:** If Obsidian is essential, "just markdown files" is less portable than claimed.
- **Lock-in:** Obsidian plugins create soft vendor lock-in (graph view, Dataview queries, Marp).

---

## 6. Ingestion Supervision: Batch or Incremental?

### Contradiction

**Position A (Incremental, supervised):** Ingest one source at a time with human review.
- Article: *LLM Wiki.md* — "Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize."
- Implication: Human in the loop for every ingestion; plan review before execution.

**Position B (Batch, less supervised):** Ingest many sources at once, trust the schema.
- Article: *LLM Wiki.md* — "But you could also batch-ingest many sources at once with less supervision."
- Implication: Human gates the strategy, not every source.

**Position C (Full automation):** "Ingest <URL>" just works; no plan review required.
- Article: *Building a Complete Personal Harness* — slash command `/wiki-ingest` automatically ingests and updates the wiki.
- Implication: Schema is trusted so much that automatic execution is safe.

### Resolution Issue
- **Safety vs. friction:** Does "present plan before executing" protect against mistakes or just add friction?
- **Real practice:** Which method do successful users actually adopt?

---

## 7. Query Workflow: Index Search vs. Direct Reasoning

### Contradiction

**Position A (Index first):** Queries start by reading the index.
- Article: *LLM Wiki.md* — "When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)."
- Implication: Index.md is sufficient for navigation; no embedding search required.

**Position B (Direct page reading):** The agent figures out what to read.
- Article: *Building a Complete Personal Harness* — `/wiki-query` uses `grep` to find relevant files, then reads them.
- Implication: Full-text search over the wiki is sufficient; index is optional.

**Position C (Search infrastructure optional):** At scale, add proper search.
- Article: *LLM Wiki.md* — "At small scale the index file is enough, but as the wiki grows you want proper search. qmd is a good option..."
- Implication: Index is a temporary measure; you'll need to build search infrastructure.

### Resolution Issue
- **Scalability:** What happens at 1000 pages? 10,000 pages? Index alone becomes inefficient.
- **Implementation burden:** None of the articles clearly document a query system that scales past ~500 pages.

---

## 8. Cloud APIs vs. Local Models: Cost & Dependency

### Contradiction

**Position A (Cloud assumed):** Uses Claude, OpenAI, Google, Anthropic APIs.
- Articles: *LLM Wiki.md*, *Building a Complete Personal Harness*, *FreeBirdsCrew WhatsApp bot*.
- Cost model: Pay per token; "free tier is more than enough" for small scale.
- Implication: Your wiki is processed by third-party servers.

**Position B (Local models recommended):** Run Ollama or vLLM locally.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next*
- Models: Qwen2.5-14B recommended for balance; Llama-3.1-70B for better reasoning; Qwen2.5-1M for huge documents.
- Implication: Infrastructure cost is compute (GPU), not tokens.

### Resolution Issue
- **Data sovereignty:** Cloud APIs send your wiki contents to external servers (see TOS). Local models keep data private.
- **Cost calculation:** Which is cheaper? Depends on usage volume and GPU availability.
- **Latency:** Cloud APIs slower (network round-trip) vs. local models (GPU throughput).

---

## 9. The Fine-Tuning Endgame: Mentioned But Undeveloped

### Contradiction

**Position A (Future possibility):** Generate synthetic training data from the wiki to fine-tune models.
- Article: *Andrej Karpathy Killed RAG. Or Did He?*
- Quote: "The knowledge moves from context window to model weights. Your personal wiki becomes a personal model."
- Implication: Long-term trajectory is wiki → dataset → fine-tuned model → improved reasoning.

**Position B (Not mentioned):** No other article discusses this.
- Articles: All others focus on wiki maintenance in-place, not generation of training data.
- Implication: This may be speculative or out of scope for current implementations.

### Resolution Issue
- **Unclear roadmap:** Is fine-tuning a real next step or a thought experiment?
- **Practical gap:** None of the implementations provide tools for synthetic data generation or fine-tuning workflows.

---

## 10. Ingestion Completion: When Is a Wiki "Done"?

### Contradiction

**Position A (Never done):** The wiki is perpetually incomplete.
- Article: *LLM Wiki.md* — Lint operation: "The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows."
- Implication: There's always more to synthesize, more gaps to fill, more questions to answer.

**Position B (Steady state):** A wiki reaches a stable state.
- Article: *Building a Complete Personal Harness* — Example flow shows ingestion → plan → approve → execute → report. Suggests completeness per ingestion.
- Implication: Each ingestion cycle has a clear endpoint.

### Resolution Issue
- **Psychological:** Is the goal to maintain a living system or to document a domain comprehensively?
- **Practical:** How do you know when to stop ingesting and start using the wiki?

---

## 11. Wikilinks vs. Standard Markdown Links

### Contradiction

**Position A (Wikilinks mandatory):** Always use `[[Concept]]` syntax.
- Article: *Building a Complete Personal Harness* — Obsidian markdown skill teaches wikilinks.
- Reasoning: Enables bidirectional link detection, graph view, navigation.
- Implication: Requires Obsidian or compatible tooling.

**Position B (Markdown-agnostic):** Use whatever your tool supports.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next* — Describes nashsu/llm_wiki (custom graph format), Pratiyush/llm-wiki (static HTML links), lucasastorian/llmwiki (filesystem links).
- Implication: Wikilinks are not universal; different implementations use different link formats.

### Resolution Issue
- **Portability:** If you commit to wikilinks, you're locked to Obsidian-compatible systems.
- **Standard:** No agreed-upon standard; each implementation invents its own.

---

## 12. LLM Wiki as "Pattern" vs. "Product"

### Contradiction

**Position A (Pattern):** LLM Wiki is an idea, not software.
- Article: *LLM Wiki.md* — "This document is intentionally abstract. It describes the idea, not a specific implementation."
- Article: *Andrej Karpathy Killed RAG. Or Did He?* — "Karpathy didn't ship a product. He shared an idea in a GitHub Gist."
- Implication: You build your own version; no canonical tool to install.

**Position B (Products exist):** Multiple concrete implementations are available and documented.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next* — Describes nashsu/llm_wiki (desktop app), nvk/llm-wiki (Claude Code plugin), Pratiyush/llm-wiki (transcript miner), lucasastorian/llmwiki (MCP-powered).
- Implication: The pattern has been instantiated; you can use off-the-shelf tools.

### Resolution Issue
- **For adopters:** Do I build from scratch or use an existing tool?
- **For ecosystem:** Which implementation should be considered the "reference" implementation?

---

## 13. Contradiction Flagging: Aggressive or Conservative?

### Contradiction

**Position A (Aggressive):** The LLM immediately flags contradictions between sources.
- Article: *LLM Wiki.md* — "noting where new data contradicts old claims."
- Implication: LLM is responsible for maintaining consistency and surfacing conflicts.

**Position B (Conservative):** Contradictions are noted but left for human judgment.
- Article: *Building a Complete Personal Harness* — Custom `adr-writing` skill: "If you find contradiction between two ADRs, DO NOT resolve alone. Report to Roan."
- Implication: LLM flags but doesn't auto-resolve.

### Resolution Issue
- **Authority:** When two sources disagree, who decides? The schema? The human? The LLM's "judgment"?
- **Safety:** Auto-resolution risks silently choosing the wrong source; manual resolution is slower but safer.

---

## 14. Git Versioning: Mandatory or Optional?

### Contradiction

**Position A (Strongly recommended):** Git is essential infrastructure.
- Article: *Building a Complete Personal Harness* — "Versioning the vault is the cheapest, most useful backup that exists... `git diff` shows exactly what changed; `git checkout` reverts."
- Implication: Without git, you're vulnerable to data loss and can't audit changes.

**Position B (Not mentioned in core pattern):** Karpathy's original gist doesn't emphasize versioning.
- Article: *LLM Wiki.md* — Git mentioned only as a tip: "The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free."
- Implication: Optional but convenient.

### Resolution Issue
- **Risk management:** Is git a safety requirement or a convenience?
- **Setup burden:** Adds complexity for non-technical users.

---

## 15. Query Output Forms: Markdown vs. Other Formats?

### Contradiction

**Position A (Markdown always):** Queries return markdown pages.
- Article: *LLM Wiki.md* — "Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas."
- Implication: Flexibility in output format.

**Position B (Structured output):** Some implementations support multiple formats.
- Article: *LLM Wiki — Andrej Karpathy's Idea — Is What Comes Next* — Describes nashsu/llm_wiki supporting PDF, DOCX, images, video; Pratiyush/llm-wiki exporting in llms.txt, JSON-LD, RSS.
- Implication: Queries can produce code, structured data, or multimedia.

### Resolution Issue
- **Compatibility:** If the wiki is "just markdown," can it really produce DOCX or PDF without external tools?
- **Maintenance:** How are non-markdown outputs kept in sync with the markdown source?

---

## Summary of Unresolved Tensions

| Tension | Position A | Position B | Position C | Impact |
|---------|-----------|-----------|-----------|--------|
| RAG status | Dead | Different tool | Cache layer | Strategic positioning |
| Enterprise scale | Not ready | Works for small teams | WhatsApp bot proves it | Investment decision |
| Complexity | Simple | Complex | Depends on implementation | Setup expectations |
| Zone model | 3 layers | 4 zones | — | Architecture choice |
| Obsidian | Optional | Essential | Agnostic | Tooling lock-in |
| Ingestion | Supervised | Batch | Automatic | Governance model |
| Query | Index first | Direct read | Search infrastructure | Scalability path |
| APIs | Cloud | Local | Depends | Cost & privacy |
| Fine-tuning | Future | Not mentioned | — | Long-term roadmap |
| Links | Wikilinks | Any format | — | Portability |
| Pattern vs. Product | Pattern | Products exist | — | Adoption friction |

---

## Recommendations for Resolvers

1. **Define target scale clearly:** The answers change at 10 articles vs. 1000.
2. **Specify governance model:** Who decides when sources conflict?
3. **Choose implementation:** Decide if you're building custom or adopting an existing tool.
4. **Document schema explicitly:** The CLAUDE.md or AGENTS.md becomes the source of truth for your variant.
5. **Audit assumptions:** Before committing to LLM Wiki, verify the implementation matches your risk tolerance (enterprise scalability, data privacy, cost).

