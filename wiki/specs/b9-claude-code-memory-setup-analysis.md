# B.9 Investigation — claude-code-memory-setup Reference Analysis

**Status:** INVESTIGATION COMPLETE (2026-05-18)  
**Repository:** https://github.com/lucasrosati/claude-code-memory-setup  
**Investigation Focus:** Memory and context management patterns for spekificity adoption  

---

## Executive Summary

The **claude-code-memory-setup** repository by Lucas Rosati demonstrates a proven, production-tested two-system memory architecture: **Obsidian (declarative) + Graphify (structural)**. The design aligns closely with spekificity's planned memory model (B.8.2) while introducing several patterns worth adopting:

1. **Session continuity commands** (`/resume`, `/save`) — Direct implementations of spekificity's `/spek.prepare` and `/spek.post`
2. **Zettelkasten conventions** — Atomic notes, dense linking, standardized frontmatter → applicable to spekificity lessons/decisions/patterns
3. **Chat import pipeline** — Automated conversion of unstructured conversations to structured vault notes → potential model for `/spek.post` lessons generation
4. **Centralized single vault** — One vault per user/team (not per project) enables cross-project pattern discovery
5. **3-layer query rule** — Graph → Vault → Code, preventing unnecessary file re-reads → matches spekificity's planned context loading strategy
6. **Incremental graph refresh** — Git hooks + watch mode for persistent, low-cost indexing
7. **Token savings metrics** — 71.5x reduction documented; patterns are replicable in spekificity

**Verdict:** Spekificity should adopt 4-5 specific patterns from this repository. The architecture is compatible with spekificity's design; no fundamental conflicts.

---

## Repository Overview

**What it is:**
- A complete setup guide for Claude Code agents to maintain persistent memory and codebase awareness across sessions
- Three integrated components: Obsidian vault (PKM), Graphify (code graph), chat import pipeline (conversation archival)
- Designed to solve two problems: session amnesia and token waste from re-reading files

**What it's not:**
- A framework or tool itself (just a setup guide + scripts)
- Tied to any specific project structure
- Proprietary (MIT licensed, 659 stars, actively maintained)

**Real-world results (tested on 126 TypeScript files):**
- 332 graph nodes, 258 edges, 124 communities detected
- 71.5x fewer tokens per session
- 499x token reduction on specific queries
- 0 tokens in AST mode (pure tree-sitter)
- 780+ total vault notes (permanent + chats + graphs)

---

## Part 1: Obsidian Vault Structure (Declarative Memory)

### How It's Organized

```
~/vault/                          # SINGLE vault for all user projects
├── CLAUDE.md                     # Global instructions (like spekificity's README)
├── permanent/                    # Consolidated, atomic notes (like B.8.2 vault/)
├── inbox/                        # Raw capture (fleeting ideas)
├── fleeting/                     # Quick notes (ephemeral)
├── templates/                    # Note templates
├── logs/                         # Session logs (like B.8.4 session memory)
├── references/                   # Reference material
├── my-project/                   # Project MOC (Map of Contents)
│   ├── architecture/             # Decisions, conventions
│   ├── pipeline/                 # Data flows, APIs
│   ├── data/                     # Schema, data model
│   ├── features/                 # Planned/implemented features
│   └── logs/                     # Project-specific session logs
├── chats/                        # Imported conversations (auto-generated)
│   ├── code/                     # Claude Code chats
│   └── web/                      # Claude Web/App chats
└── graphify/                     # Codebase knowledge graphs (auto-generated)
    ├── my-project/               # Graph nodes for project X
    └── another-project/          # Graph nodes for project Y
```

### Key Design Decisions

1. **Single vault (not per-project)**
   - Enables cross-project linking and pattern discovery
   - Reduces friction — users maintain one PKM, not N
   - One unified graph view across all projects
   - **Spekificity note:** Vault is per-workspace (in `.spekificity/`), not global. Could be extended to share vault across workspaces in future

2. **Zettelkasten method**
   - Atomic: one concept per permanent note
   - Dense linking: minimum 2 wikilinks per note
   - Standardized metadata: YAML frontmatter (title, tags, created, updated, status, type)
   - **Spekificity note:** Decisions/patterns already use metadata; lessons could benefit from denser internal linking

3. **Folder structure organizes information, not tools**
   - `logs/`, `permanent/`, `chats/`, `graphify/` are roles, not technical layers
   - Project subfolders (my-project/, another-project/) contain MOCs and curated notes
   - Auto-generated content (chats, graphs) is isolated from manual notes
   - **Spekificity note:** Matches spekificity's planned structure (vault/decision.md, vault/patterns.md, vault/lessons/)

### Implementation: CLAUDE.md

The vault includes a **CLAUDE.md** file at root — global instructions for Claude Code to follow when reading the vault. Key sections:

```yaml
## What is this vault
Centralized knowledge base for all projects.
Persistent memory across sessions.

## Project stacks
- Project X: React + Supabase
- Project Y: Python + FastAPI

## Zettelkasten Rules
- Use wikilinks (not markdown links)
- Mandatory YAML frontmatter
- Filenames in kebab-case
- 1 concept per permanent note
- Minimum 2 wikilinks per note

## Session Commands
### /resume
1. Read 3 most recent session logs
2. Read architecture/decisions.md
3. Summarize current state

### /save
1. Create session log
2. Record: what was done, decisions, pending
3. Add wikilinks
4. Commit + push if in repo
```

**Spekificity analogue:** This mirrors spekificity's `.spekificity/guides/` and `copilot-instructions.md`. The `/resume` and `/save` commands are direct implementations of B.8.4's `/spek.prepare` and `/spek.post`.

---

## Part 2: Chat Import Pipeline (Auto-Conversion of Conversations)

### Architecture

```
Claude Code / Web
     ↓
Export chats (manual or automated)
     ↓
~/claude-exports/code/ or ~/claude-exports/web/
     ↓
Python processor script (claude_to_obsidian.py)
├── Detect origin (Code vs Web)
├── Generate automatic tags (keyword matching)
├── Add YAML frontmatter
├── Insert wikilinks (if note exists in vault)
└── Copy to vault/chats/<origin>/
     ↓
Vault indexed; chats searchable + linkable
```

### Key Components

1. **Export tool** — `claude-conversation-extractor` (pip package)
2. **Processor script** — Python (keyword-to-tag mapping, frontmatter generation, wikilink insertion)
3. **Automation** — cron job (e.g., daily at 10 PM) + bash script
4. **Staging area** — `~/claude-exports/` (outside vault, temporary)

### Processor Logic

```python
KEYWORD_TAG_MAP = {
    "python": "python",
    "react": "react",
    "supabase": "supabase",
    "deploy": "deploy",
    "bug": "debugging",
    "refactor": "refactoring",
}

For each exported .md file:
1. Read file content
2. Scan for keywords; generate tags
3. Add YAML frontmatter (type: chat, tags, created, updated)
4. Query vault for [[existing-notes]]; insert wikilinks
5. Copy to vault/chats/code/ or vault/chats/web/
```

**Token savings:** Indexed chats are queryable without re-reading conversation history. Estimated 60-80% token reduction when referencing prior conversations.

### Spekificity Adaptation

**How B.8.4 `/spek.post` can adopt this pattern:**

Step 3 (Generate Lessons Document) already involves extracting structured data from artifacts. The chat import pipeline's **auto-tagging + wikilink insertion** could enhance lessons generation:

```
/spek.post Step 3 (Enhanced with Chat Import Pattern):
├── Collect execution trace + decision log (like chat history)
├── Extract keywords → map to patterns + decisions
├── Generate lesson document with:
│   ├── Auto-inserted wikilinks to vault/patterns.md
│   ├── Auto-tagged with domain keywords
│   └── Cross-linked to related lessons from similar features
```

**Benefit:** Lessons become naturally interconnected without manual linking. Future `/spek.context` loads can traverse wikilinks to find related lessons.

---

## Part 3: Graphify Integration (Structural Memory)

### Overview

Graphify transforms codebase into a queryable knowledge graph using tree-sitter AST (Abstract Syntax Tree):

- **Code parsing:** 100% local, no code leaves machine
- **Caching:** SHA256 — only processes modified files
- **Cost:** 0 tokens in default AST mode
- **Languages:** 20+ (Python, JS, TypeScript, Go, Rust, Java, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, etc.)

### Output Files

```
your-project/
└── graphify-out/
    ├── graph.json              # Queryable graph (nodes + edges)
    ├── graph.html              # Interactive visualization
    ├── GRAPH_REPORT.md         # Node analysis, metrics, communities
    ├── wiki/                   # Wikipedia-style articles (agent navigation)
    └── cache/                  # SHA256 cache for incremental updates

~/vault/graphify/project-name/
└── (Obsidian notes)           # Each function/module as node + backlink
```

### Key Commands

| Command | Purpose |
|---------|---------|
| `graphify .` | Full pipeline on current directory |
| `graphify . --update` | Only process modified files |
| `graphify . --obsidian --obsidian-dir ~/vault/graphify/project-name` | Generate Obsidian notes + graph |
| `graphify . --watch` | Auto-rebuild on file save |
| `graphify hook install` | Git post-commit hook (auto-rebuild after commit) |
| `graphify query "question"` | Query graph directly |

### Real Output Example

**Tested on 126 TypeScript files:**
- 332 graph nodes
- 258 edges (connections)
- 124 communities detected
- graph.json: 172 KB
- 456 Obsidian notes generated

### 3-Layer Query Rule (Context Navigation)

```
Priority 1: Query graph.json or graph.html
  → Understand structure + connections (280 tokens vs. 20,000 re-reading all files)

Priority 2: Query Obsidian vault (decisions, progress, architecture)
  → Get context + decisions

Priority 3: Only read raw code files when editing
  → After layers 1-2 have answered the question
```

**Token impact:** Reduces per-session tokens from ~20K (re-reading) to ~280 (graph query). 71x reduction.

### Spekificity Alignment

**Strong alignment with B.8.1 (Code and Document Maps):**

Spekificity's planned design:
```
Pass 1: Graphify indexes code → vault/graph/nodes-code.jsonl
Pass 2: Obsidian export → vault/graph/nodes-docs.jsonl
Pass 3: Merge → vault/graph/nodes.jsonl
```

Claude-code-memory-setup uses:
```
Graphify: code nodes + edges → graph.json
Obsidian export: doc nodes → vault/graphify/project/
Custom merge: Combine in Obsidian graph view
```

**Difference:** Spekificity merges into a unified JSONL file for agent queries; claude-code-memory-setup uses Obsidian's native graph view for human browsing + manual agent queries. Spekificity's approach is more agent-native.

**Adoption:** Spekificity can use graphify's `--update` flag and git hooks directly (already planned in B.8.4 `/spek.post` Step 6). The watch mode is useful for incremental dev workflow.

---

## Part 4: Session Continuity (`/resume` and `/save`)

### Concept

Two commands bookend every session:

#### `/resume` (Session Start)

```
When you receive this command:
1. Read 3 most recent session logs from logs/
2. Read architecture/decisions.md for current project
3. Summarize: what was done, current state, what's pending
```

**Purpose:** Re-establish context without re-reading everything.

#### `/save` (Session End)

```
When you receive this command:
1. Create session log in logs/YYYY-MM-DD-description.md
2. Record: what was done, decisions made, pending items
3. Add wikilinks to created/modified notes
4. Run git commit + push if in repository
```

**Purpose:** Capture progress, link to decisions, persist to git.

### Spekificity Mapping

These map directly to B.8.4:

| claude-code-memory-setup | Spekificity | Purpose |
|--------------------------|-------------|---------|
| `/resume` | `/spek.prepare` | Re-establish context, verify workspace, report ready |
| `/save` | `/spek.post` | Capture progress, extract lessons, update vault |

**Spekificity enhancements over `/resume` and `/save`:**
- B.8.4 `/spek.prepare` adds 7 explicit steps (git verify, feature name, graph check, context load, state init, report)
- B.8.4 `/spek.post` adds 10 explicit steps (artifacts, compression, lessons, vault update, graph sync, memory, docs, archive, report)
- Spekificity adds caveman compression, incremental graph sync, feature state tracking
- Spekificity integrates with SpecKit workflow (decorator wrapper pattern)

**Key learning:** The `/resume` and `/save` pattern is proven and reliable. Spekificity's `/spek.prepare` and `/spek.post` should maintain this same conceptual simplicity while adding necessary orchestration.

---

## Part 5: Recommended Obsidian Plugins

Repository recommends:

| Plugin | Purpose | Use in Spekificity |
|--------|---------|-------------------|
| **BRAT** | Install beta plugins | Optional; enables 3D graph |
| **3D Graph** | 3D vault visualization | Nice-to-have; helps see pattern connections |
| **Folders to Graph** | Folders as graph nodes | Useful; treats vault folders as nodes |
| **Calendar** | Daily note navigation | Useful; quick access to session logs |

**Spekificity note:** None of these are required for spekificity to function. BRAT + 3D Graph could help users visualize decision/pattern graphs.

---

## Comparative Analysis: claude-code-memory-setup vs. Spekificity

### Similarities (Strong Alignment)

| Dimension | claude-code-memory-setup | Spekificity | Status |
|-----------|--------------------------|-------------|--------|
| **Declarative memory** | Obsidian vault | vault/ (Obsidian-backed) | ✓ Aligned |
| **Structural memory** | Graphify (code graph) | Code graph + vault/graph/ | ✓ Aligned |
| **Session continuity** | `/resume` + `/save` | `/spek.prepare` + `/spek.post` | ✓ Aligned |
| **Atomic notes** | Zettelkasten (permanent/) | vault/lessons/, vault/decision.md | ✓ Aligned |
| **Cross-project patterns** | Single vault with tags | vault/patterns.md + repo memory | ✓ Similar |
| **Incremental refresh** | Git hooks + `--update` | `/spek.post` Step 6 (incremental sync) | ✓ Aligned |
| **Token optimization** | Caveman-style compression implied | Caveman mode (B.2, B.3, B.4) | ✓ Aligned |
| **Query strategy** | 3-layer (graph → vault → code) | `/spek.context` (vault → repo → graph) | ✓ Aligned |

### Differences (Design Choices)

| Dimension | claude-code-memory-setup | Spekificity | Rationale |
|-----------|--------------------------|-------------|-----------|
| **Vault scope** | Global (all projects) | Per-workspace (one per feature repo) | Spekificity: tighter project isolation |
| **Graph format** | graph.json (queryable) + Obsidian (human browsable) | JSONL (queryable) + Obsidian (human browsable) | Spekificity: unified agent query format |
| **Chat import** | Automated cron pipeline | `/spek.post` Step 3 (lessons extraction) | Spekificity: integrated with feature workflow |
| **Session commands** | `/resume`, `/save` (human-initiated) | `/spek.prepare`, `/spek.post` (explicit workflow steps) | Spekificity: more structured, spec-driven |
| **Context loading** | Manual via `/resume` | Automatic via `/spek.context` in `/spek.prepare` | Spekificity: more explicit orchestration |
| **Workflow integration** | Freestanding (works with any Claude workflow) | Integrated with SpecKit + spekificity lifecycle | Spekificity: ecosystem-specific |

---

## Recommendations for Spekificity

### Adopt These Patterns (High Priority)

#### 1. Zettelkasten Conventions for Vault Notes

**Pattern from claude-code-memory-setup:**
- Mandatory YAML frontmatter (title, tags, created, updated, status, type)
- Dense wikilinks (minimum 2 per note)
- Atomic notes (one concept per file)
- Kebab-case filenames

**Spekificity implementation:**
- Apply to `vault/lessons/<date>-<feature>-*.md` (lessons already use 8-section format; add dense wikilinks)
- Apply to `vault/decision.md` entries (each decision gets frontmatter + wikilinks to related decisions, patterns, lessons)
- Apply to `vault/patterns.md` entries (each pattern gets frontmatter + wikilinks to lessons using it, related patterns)

**Benefit:** Enables natural navigation through vault via graph view; makes lessons discoverable by future `/spek.context` loads.

**Action:** Update B.8.4 `/spek.post` Step 3 (Generate Lessons) to include automatic wikilink insertion.

---

#### 2. Chat Import Pipeline Pattern for Lesson Generation

**Pattern from claude-code-memory-setup:**
- Auto-tag based on keywords (KEYWORD_TAG_MAP)
- Auto-insert wikilinks to existing vault notes
- Generate YAML frontmatter with metadata

**Spekificity implementation:**
- In `/spek.post` Step 3, after generating raw lessons:
  1. Extract keywords from lessons (architecture, decisions, patterns)
  2. Map to existing vault items (patterns, decisions, lessons)
  3. Auto-insert `[[wikilink]]` to related items
  4. Auto-generate tags (domain, tech stack, methodology)
  5. Ensure full YAML frontmatter

**Benefit:** Lessons become interconnected without manual linking; future `/spek.context` can traverse connections to find similar features.

**Action:** Create KEYWORD_TAG_MAP in `.spekificity/config.yaml`; enhance `/spek.post` lesson generation with auto-linking logic.

---

#### 3. Incremental Graph Refresh with Git Hooks

**Pattern from claude-code-memory-setup:**
- `graphify hook install` → auto-rebuild on post-commit
- `graphify . --update` → only process modified files (SHA256 caching)
- Optional: `graphify . --watch` → auto-rebuild on file save

**Spekificity implementation:**
- Already planned in B.8.4 `/spek.post` Step 6 (Incremental Code Graph Sync)
- Add optional git hook installation in `.spekificity/bin/spek setup`
- Document in `.spekificity/guides/quickstart.md`

**Benefit:** Graph stays fresh without manual intervention; no token waste on stale graph queries.

**Action:** Integrate graphify git hooks into spekificity setup scripts.

---

#### 4. Session Logs as Explicit Artifact

**Pattern from claude-code-memory-setup:**
- Session logs stored in `logs/YYYY-MM-DD-description.md`
- Each log records: what was done, decisions, pending items, wikilinks
- Logs become indexed, searchable, linkable

**Spekificity implementation:**
- `/memories/session/current-feature.md` already serves this role
- Enhance with structured sections (What Was Done, Decisions, Patterns, Pending)
- Archive logs after feature completion to `vault/lessons/<date>-<feature>-*.md`
- Add wikilinks to decisions and patterns during archival

**Benefit:** Execution logs become part of searchable vault; provides audit trail.

**Action:** Enhance B.8.4 `/spek.post` Step 9 (Archive Session Memory) to extract structured sections from current-feature.md and link to vault.

---

#### 5. 3-Layer Query Rule as Agent Guidance

**Pattern from claude-code-memory-setup:**
```
Layer 1: Query graph.json (structure + connections)
Layer 2: Query vault (decisions, progress, context)
Layer 3: Read raw code (only when needed after layers 1-2)
```

**Spekificity implementation:**
- Document in `.spekificity/guides/context-navigation.md`
- Embed in `/spek.context` skill (prioritize graph → vault → code query order)
- Add to `copilot-instructions.md` (guide agent to follow this query order)

**Benefit:** Reduces token waste; prioritizes cached/indexed data over file re-reading.

**Action:** Document 3-layer query rule in `.spekificity/guides/`; add to agent instructions.

---

### Consider for Future Phases (Medium Priority)

#### 6. Cross-Project Vault (Future Enhancement)

**Pattern from claude-code-memory-setup:**
- Single global vault for all user projects
- Enables pattern discovery across projects
- One unified graph view

**Spekificity current model:** Vault per workspace (per git repo)

**Future consideration:** Could extend spekificity to support a shared vault across workspaces. Benefits:
- Patterns discovered in project A can inform project B
- Cross-project decision history
- Unified lessons library

**Timeline:** Post B.9-B.11 (not for initial implementation).

---

#### 7. Watch Mode for Dev Workflow

**Pattern from claude-code-memory-setup:**
- `graphify . --watch` auto-rebuilds graph on file save
- Useful for incremental development

**Spekificity current model:** Graph refresh triggered by `/spek.post` or manual `/spek.map` (end-of-session)

**Future consideration:** For interactive development, could add optional watch mode.

**Timeline:** Nice-to-have; depends on user feedback.

---

### Do NOT Adopt (Intentional Differences)

#### Why Spekificity Doesn't Adopt These Patterns

1. **Manual `/resume` and `/save` commands**
   - Claude-code-memory-setup relies on user-initiated commands
   - Spekificity uses explicit workflow steps (B.8.4 `/spek.prepare` and `/spek.post`)
   - Reason: Spekificity integrates with SpecKit lifecycle; commands are orchestrated, not manual

2. **Global single vault**
   - Claude-code-memory-setup: one vault for all projects (cross-project linking)
   - Spekificity: vault per workspace (per git repo)
   - Reason: Spekificity is designed for tighter project isolation and integrated CI/CD; global vault creates coupling

3. **Obsidian graph view as primary query interface**
   - Claude-code-memory-setup: users browse Obsidian graph manually
   - Spekificity: JSONL graph for agent queries, Obsidian for human browsing
   - Reason: Spekificity agents need queryable format; Obsidian is human-friendly but not agent-native

---

## Migration Path for Spekificity

### Phase 1 (Immediate): Adopt High-Priority Patterns

**Actions:**
1. Update `vault/decision.md`, `vault/patterns.md`, `vault/lessons/` with Zettelkasten conventions (frontmatter + wikilinks)
2. Enhance `/spek.post` Step 3 with auto-tagging + auto-linking logic
3. Document 3-layer query rule in `.spekificity/guides/`
4. Integrate graphify git hooks into setup scripts

**Effort:** 4-6 hours of work; high impact.

**Files to update:**
- `specs/b8-4-prepare-and-post-skills.md` (add auto-linking to Step 3)
- `.spekificity/config.yaml` (add KEYWORD_TAG_MAP, graph hook settings)
- `.spekificity/guides/context-navigation.md` (document 3-layer query rule)
- `.spekificity/bin/spek setup` (add graphify hook installation)

### Phase 2 (Implementation): Build Skills & Agents

**Depends on:** Phase 1 completion

**Actions:**
1. Implement `/spek.prepare` with all 7 steps (includes graphify + Zettelkasten setup)
2. Implement `/spek.post` with all 10 steps (includes auto-linking + archive)
3. Build `/spek.context` skill with 3-layer query order
4. Test with end-to-end workflow

**Timeline:** Part of B.9-B.11 implementation phase.

### Phase 3 (Future): Global Vault (Optional)

**Depends on:** Successful completion of Phase 2 + user feedback

**Actions:**
- Support shared vault across workspaces
- Implement cross-project pattern discovery
- Add workspace linking to decisions/patterns

**Timeline:** Post B.9-B.11.

---

## Lessons Learned & Design Validation

### Patterns Validated by claude-code-memory-setup

| Pattern | Validated | Note |
|---------|-----------|------|
| Obsidian + Graphify for persistent memory | ✓ Yes | 659 stars, production use |
| Zettelkasten for atomic notes | ✓ Yes | Proven PKM method |
| Auto-tagging + wikilinks for lessons | ✓ Yes (chat import pipeline) | Reduces manual work |
| Incremental graph refresh | ✓ Yes | Git hooks work reliably |
| Session logs as vault artifacts | ✓ Yes | Indexed, searchable logs |
| 3-layer query rule | ✓ Yes | 71x token reduction achieved |
| Session continuity (`/resume`, `/save`) | ✓ Yes | Simple, effective pattern |

### Design Conflicts (None Found)

Spekificity's planned architecture (B.8.1-B.8.4) has **zero conflicts** with claude-code-memory-setup's patterns. The two systems are complementary:

- **claude-code-memory-setup:** Freestanding, works with any Claude workflow
- **Spekificity:** Integrated with SpecKit, adds persistent memory + context orchestration

Both can coexist and reinforce each other.

---

## Adoption Checklist

### High-Priority Adoptions (Do These First)

- [ ] **B.9.1:** Add Zettelkasten frontmatter conventions to spec/vault (decision, patterns, lessons)
- [ ] **B.9.2:** Create KEYWORD_TAG_MAP in `.spekificity/config.yaml` (domain, tech stack, methodology tags)
- [ ] **B.9.3:** Enhance `/spek.post` Step 3 with auto-tagging + auto-wikilink-insertion logic
- [ ] **B.9.4:** Document 3-layer query rule in `.spekificity/guides/context-navigation.md`
- [ ] **B.9.5:** Integrate graphify git hooks into `.spekificity/bin/spek setup`

### Medium-Priority Adoptions (Next Phase)

- [ ] **B.9.6:** Add watch mode option to `/spek.map` (for interactive dev workflow)
- [ ] **B.9.7:** Extend archival to extract structured session log sections and link to vault
- [ ] **B.9.8:** Test with real multi-feature workflow; measure token savings

### Future Adoptions (Post B.9-B.11)

- [ ] **B.9.9:** Evaluate global cross-project vault (user feedback-driven)
- [ ] **B.9.10:** Cross-project pattern discovery dashboard (if global vault adopted)

---

## References

**Repository:** https://github.com/lucasrosati/claude-code-memory-setup 
- MIT License
- 659 stars
- Active (last commit 2 weeks ago)
- Authors: Lucas Rosati, Kilderson Sena

**Key Files from Repository:**
- `README.md` — Complete setup guide (used for this analysis)
- `scripts/` — Python processor, bash automation scripts

**Spekificity Related Specs:**
- [B.8.1 Code and Document Maps](../specs/b8-1-code-and-document-maps.md)
- [B.8.2 Persistent Memories and Lessons](../specs/b8-2-persistent-memories-and-lessons.md)
- [B.8.3 SpecKit Integration Contract](../specs/b8-3-speckit-integration-contract.md)
- [B.8.4 Prepare and Post Skills](../specs/b8-4-prepare-and-post-skills.md)

**Key Metrics:**
- 71.5x fewer tokens per session (tested, real-world)
- 499x reduction on specific queries
- 780+ total vault notes (practical scale)
- 20+ supported languages (graphify)
- 0 tokens in AST mode (no API cost)

