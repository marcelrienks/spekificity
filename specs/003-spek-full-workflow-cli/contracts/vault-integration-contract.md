# contract: vault integration

**feature**: `003-spek-full-workflow-cli`
**version**: 1.0
**date**: 2026-05-03

---

## overview

this contract defines how `spek` commands read from and write to the obsidian vault (`vault/`). the vault is plain markdown — no obsidian app api is used. reads are performed by the ai agent during skill execution. writes are performed by the ai or by shell scripts.

---

## vault directory structure

```text
vault/
├── context/
│   ├── decisions.md         ← architectural decisions — read by automate (spec + plan)
│   └── patterns.md          ← recurring patterns — read by automate (spec + plan)
├── graph/
│   ├── index.md             ← graphify graph entry point — freshness check target
│   └── nodes/               ← individual graph node files
├── lessons/
│   ├── <date>-<feature>.md  ← lessons entries — written by /spek.lessons-learnt
│   └── ...
└── (other vault dirs as needed)
```

---

## read operations

### r-1: context load (prepare step)

**who reads**: `/spek.prepare` skill and `/spek.context-load` skill
**what is read**:
- `vault/context/decisions.md` — full file
- `vault/context/patterns.md` — full file
- `vault/lessons/` — most recent 3 entries (sorted by filename date prefix)
- `vault/graph/index.md` — for staleness check (timestamp comparison, not content read)

**format requirement**: all context files must be valid markdown. no binary content.

**staleness check**: before reading, the ai shell script calls `compute_graph_state()` (defined in data-model.md). if `stale` or `absent`, the shell triggers graphify refresh before the ai reads context.

---

### r-2: vault context injection (automate — spec step)

**who reads**: `/spek.automate` skill, during spec invocation
**what is read**:
- `vault/context/patterns.md` — full file
- `vault/context/decisions.md` — full file
- `vault/graph/nodes/` — graph nodes matching keywords from `feature_description` (the ai scans the index for relevant nodes, then reads matching node files)

**injection**: the ai prepends the following block to the speckit specify invocation context:
```markdown
## vault context

### relevant decisions
<content from decisions.md filtered to relevant sections>

### relevant patterns
<content from patterns.md filtered to relevant sections>

### related codebase components
<relevant graph node summaries>
```

**no-vault fallback**: if `vault/context/` does not exist, the ai logs `[spek] ⚠ vault context not available — proceeding without codebase context` and continues without injection.

---

### r-3: vault context injection (automate — plan step)

**who reads**: `/spek.automate` skill, during plan invocation
**what is read**:
- `vault/context/decisions.md` — full file
- `vault/graph/nodes/` — nodes impacted by the feature (identified from spec.md entities)

**injection**: the ai prepends architectural decisions and impacted graph node summaries to the plan invocation context.

---

## write operations

### w-1: lessons learnt entry

**who writes**: `/spek.lessons-learnt` skill (called by `/spek.post`)
**target path**: `vault/lessons/<YYYY-MM-DD>-<feature-name>.md`
**filename format**: `2026-05-03-add-user-login.md` (date from `date +%Y-%m-%d`, feature name from `feature_branch` slug)

**file format**:
```markdown
# lessons learnt: <feature description>

**date**: <YYYY-MM-DD>
**feature branch**: <branch name>
**feature dir**: <feature dir>

## key decisions

- <decision 1>
- <decision 2>

## patterns applied

- <pattern 1>

## what worked

- <item>

## what to do differently

- <item>

## references

- [spec.md](<feature_dir>/spec.md)
- [plan.md](<feature_dir>/plan.md)
```

**write conditions**:
- always written during `spek post` invocation (manual or automated)
- if a lessons file for the same feature already exists (same filename), the ai appends a new section rather than overwriting
- the ai prompts the developer for key decisions and patterns before writing

---

### w-2: graph refresh

**who writes**: graphify cli (invoked by `/spek.map-codebase` skill)
**target paths**: `vault/graph/index.md` and `vault/graph/nodes/`
**invocation**:
```bash
# full rebuild (when graph is absent)
graphify --source . --output vault/graph/

# incremental refresh (when graph is stale)
graphify --source . --output vault/graph/ --incremental
```

**freshness update**: after graphify completes, `vault/graph/index.md` mtime is updated — this resets the staleness check.

**fallback**: if graphify is not installed, the ai writes a `[spek] ⚠ graphify not available — graph not refreshed` warning to output and records `postflight.graph_refreshed: false` in workflow-state.json.

---

### w-3: context updates (post-implementation)

**who writes**: ai agent (optional, if patterns or decisions were established during the feature)
**target paths**: `vault/context/decisions.md`, `vault/context/patterns.md`
**when**: only if `/spek.lessons-learnt` identifies new patterns or decisions worth persisting

**write format**: append a new dated section to the relevant file:
```markdown

---

## <YYYY-MM-DD>: <decision or pattern title>

<description>
```

---

## vault format requirements

- all vault files are plain markdown (`.md` extension)
- no proprietary obsidian syntax (dataview, kanban plugin syntax, etc.) is used in files read/written by spek
- file encoding: utf-8
- line endings: lf (unix)
- no binary files in `vault/context/` or `vault/lessons/`

---

## concurrency and safety

- vault writes from `spek post` are sequential — no concurrent writes
- the ai never deletes existing vault files
- if a write fails (disk full, permissions), the ai reports the error but does not halt the parent workflow (post tasks are non-blocking)

---

## summary table

| operation | skill/command | reads | writes | blocking? |
|-----------|--------------|-------|--------|-----------|
| r-1: context load | /spek.prepare, /spek.context-load | decisions, patterns, lessons, graph mtime | nothing | yes — required for prepare |
| r-2: spec context | /spek.automate (spec step) | decisions, patterns, graph nodes | nothing | no — continues if vault absent |
| r-3: plan context | /spek.automate (plan step) | decisions, graph nodes | nothing | no — continues if vault absent |
| w-1: lessons entry | /spek.lessons-learnt | (developer input) | vault/lessons/*.md | no — best-effort |
| w-2: graph refresh | /spek.map-codebase, graphify | source code | vault/graph/ | yes — required if stale before prepare |
| w-3: context updates | /spek.lessons-learnt | existing context files | vault/context/*.md | no — optional |
