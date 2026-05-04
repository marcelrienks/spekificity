# TODO

Personal action items to investigate and incorporate before implementing feature 003.

---

## [ ] 1. Understand the proper full speckit workflow

**Question**: What is the intended end-to-end speckit flow, including post-remediation?

After running `/speckit.analyze` and applying remediations manually, there appears to be no obvious skill to re-generate or refresh the spec via the VS Code extension. Clarify:

- Does speckit expect the spec to be regenerated after remediation, or does remediation happen *in place* (directly editing spec.md)?
- What does the full canonical flow look like: specify → plan → tasks → analyze → remediate → implement → ???
- Are there any re-entry points (e.g. re-run `/speckit.specify` after remediation to reconcile, or is the spec simply edited and tasks re-generated)?
- Does `/speckit.implement` expect a clean analyze pass before proceeding?

**Why it matters**: The `spek automate` step sequence (and the remediation step in particular) needs to match speckit's actual intended flow, not an assumed one.

---

## [ ] 2. Expand `spek prepare` and `spek post` — leverage caveman, graphify, and obsidian fully

**Current state**: Minimum tasks defined (prepare: context load + graph check; post: lessons-learnt + map refresh).

**Required expansions**:

- **prepare**: explicitly invoke caveman mode at start of session to reduce token consumption throughout the workflow; confirm graphify graph is fresh (not just present); load obsidian vault decisions and patterns, not just the graph index.
- **post**: invoke caveman to compress session output before writing; run graphify in incremental mode *after* lessons are written (so new lesson files are included in the graph); update obsidian vault context and decisions entries.
- Ensure both skills explicitly document their caveman activation step.
- Consider whether `spek prepare` should activate caveman automatically or prompt the developer.

---

## [ ] 3. Ensure graphify maps documentation as well as code

**Current state**: graphify is used only to map source code files into the vault graph.

**Required investigation**:

- Does graphify support indexing markdown/docs directories (e.g. `docs/`, `specs/`, `skills/`)?
- If yes: update `spek.map-codebase` skill to include docs and specs directories in the graph build, not just source code.
- If no / limited: explore whether a separate graphify run with a different target path achieves this, or whether obsidian's own linking is sufficient for docs.
- Goal: the obsidian vault graph should reflect both code *and* documentation topology so that `spek automate` spec/plan steps can reference existing docs as well as code components.

---

## [ ] 4. Understand graphify + speckit persistent context — or expand `cel.docs.read`

**Question**: Does the normal graphify + speckit workflow provide a persistent context mechanism across sessions, or does context need to be reloaded each time?

- Investigate whether graphify's output (vault graph nodes) is sufficient as a persistent context layer, or whether it only provides a point-in-time snapshot.
- If graphify does not provide persistent/incremental context across sessions: evaluate whether `cel.docs.read` (which analyses docs and persists a context map to avoid redundant re-reading) should be incorporated into `spek prepare`.
- If `cel.docs.read` is useful here: define where its context map is stored, how it interacts with the vault, and when it should be refreshed vs. reused.
- Outcome: decide whether `spek prepare` should call `cel.docs.read` as part of its skill sequence.

---

## [ ] 5. Ensure `spek post` creates structured lessons learnt from spec + implementation steps

**Current state**: `/spek.lessons-learnt` is invoked, but it is not clear whether the lesson entry captures enough detail to replace reading the spec in future sessions.

**Required expansion**:

- The lessons learnt entry written to `vault/lessons/` must include at minimum:
  - A summary of what the feature *was* (distilled from spec.md — not a copy, a digest)
  - The key implementation steps taken (derived from tasks.md — which tasks, what they built)
  - Any decisions made during the feature (extracted from spec assumptions + plan decisions)
  - Patterns identified or reused
- Goal: after `spek post` runs, future sessions should be able to load lessons without needing to read spec.md or tasks.md — the lesson entry should be self-contained enough to provide full context.
- Update the `spek.post` skill definition and `spek.lessons-learnt` instructions accordingly.

---

## [ ] 6. Incorporate `cel.docs.simplify` into `spek post`

**Current state**: `spek post` invokes lessons-learnt and map refresh only.

**Required**:

- Add a `cel.docs.simplify` step to `spek post` — after lessons are written and graph is refreshed, run `cel.docs.simplify` to audit and consolidate any documentation that grew or was modified during the feature.
- This ensures that docs do not accumulate redundancy over time as features are added.
- Clarify: does `cel.docs.simplify` operate on the full `docs/` directory, or can it be scoped to files modified in the current feature branch? Prefer scoped operation if possible to avoid unintended changes.
- Document the invocation pattern in the `spek.post` skill.

---

*Items above should be resolved before implementing `specs/003-spek-full-workflow-cli/tasks.md`.*

---

## [ ] 7. Define naming conventions for custom skills and workflows

**Question**: What should custom skills and workflows be called, and should speckit's own skill names be prefixed too?

### Custom spekificity skills (`spek.*`)

Current naming uses `spek.` as the namespace prefix for spekificity-owned skills:
- `spek.context-load`, `spek.map-codebase`, `spek.lessons-learnt`
- `spek.prepare`, `spek.post`, `spek.automate` (planned for 003)

Decide and document:
- Is `spek.` the canonical namespace for all spekificity platform skills? (yes/no — commit to it)
- Should workflow-level commands (prepare, post, automate) use the same `spek.` prefix, or a separate one (e.g. `spek.workflow.*` or just `spek.*` flat)?
- Should skill file names match the command name exactly (e.g. `skills/spek.prepare/SKILL.md`) or use a short slug (e.g. `skills/prepare/SKILL.md`) with the prefix only in the invocation?

### speckit skills (`speckit.*`)

speckit already uses its own `speckit.` prefix (e.g. `speckit.specify`, `speckit.plan`, `speckit.tasks`, `speckit.implement`).

Decide:
- Leave speckit skill names exactly as they are (do not re-prefix or alias them) — rely on the namespace distinction (`spek.*` vs `speckit.*`) to communicate ownership.
- Or: introduce local aliases (e.g. `spek.specify` → calls `speckit.specify`) so all commands in the `spek automate` flow share one namespace. Consider whether this adds clarity or unnecessary indirection.
- Recommended default: **leave speckit skills unchanged**; document the two-namespace model explicitly in `copilot-instructions.md` and the skill index so the distinction is intentional and visible.

### Enriched wrappers (`speckit-enrich.*`)

Current enriched wrappers use `speckit-enrich.*` (e.g. `speckit-enrich-specify`, `speckit-enrich-plan`, `speckit-enrich-implement`). This diverges from the dot-namespace pattern.

Decide:
- Rename to `spek.enrich.*` (e.g. `spek.enrich.specify`) to align with the `spek.*` namespace and dot-separator convention.
- Or keep `speckit-enrich.*` as-is since they are thin decorators over speckit and the name communicates that relationship.
- Consider: are these wrappers user-invoked commands or internal orchestration? If internal, they may not need a user-facing name at all.

### General conventions to document

- Separator style: dots (`.`) for namespacing, hyphens (`-`) within a word segment (e.g. `spek.context-load`, not `spek.contextLoad` or `spek.context_load`).
- Casing: all lowercase.
- Verb-noun order for action skills: `spek.map-codebase`, `spek.lessons-learnt` — or noun-verb? Decide and apply consistently.
- Where to record the canonical list: update `.spekificity/skill-index.md` and `copilot-instructions.md` once naming is settled.

**Why it matters**: inconsistent naming across `spek.*`, `speckit.*`, and `speckit-enrich.*` creates confusion about what is spekificity-owned vs. speckit-owned vs. glue code. Settling conventions now prevents the naming debt from compounding as more skills are added in 003.

---

## [ ] 8. High-level concepts to confirm and spec out individually

These are cross-cutting concerns that need deliberate thought before or alongside feature 003. Each is likely large enough to warrant its own spec.

### 8.1 Code and Document maps

- **What**: the vault graph currently targets source code. The question is whether the graph should uniformly cover both code *and* documentation (specs, docs, skills, workflows).
- **Think about**: what does it mean to "map" a markdown document — is it file-level nodes, heading-level nodes, or link-graph topology? How does graphify handle non-code files? Should a separate mapping pass exist for docs?
- **Why it matters**: every AI-assisted step (specify, plan, implement) benefits from knowing what documentation already exists. Without doc-level graph nodes, specs can duplicate or contradict existing docs silently.
- **Likely outcome**: a spec for unified code + documentation mapping, including graphify configuration, vault node schema, and how `spek.map-codebase` invokes both passes.

### 8.2 Persistent memories and lessons

- **What**: across sessions, context is currently reloaded from scratch (vault graph + decisions + lessons). There is no durable, incrementally-updated memory layer that summarises *what was built* and *why*.
- **Think about**: what is the right granularity — per-feature lessons, per-session decisions, per-pattern entries? How does this interact with the copilot `/memories/repo/` scope? Should spekificity maintain its own memory index separate from the vault?
- **Relationship to todo items 4 and 5 above**: this is the generalisation of those two items into a coherent memory architecture.
- **Why it matters**: without a deliberate memory model, future sessions either re-read everything (slow, expensive) or miss context (error-prone). The model should define what is written, when, by which skill, and how it is read back.
- **Likely outcome**: a spec for the spekificity memory model — covering vault/lessons, vault/context, copilot repo memory, and the load/write lifecycle for each.

### 8.3 Leveraging speckit as it is intended

- **What**: spekificity wraps and extends speckit, but the integration points (enriched wrappers, automate sequence, remediation loop) were inferred rather than confirmed against speckit's own design intent.
- **Think about**: what is speckit's canonical flow? Where does it expect human intervention vs. automation? What does speckit assume about the agent running it — a human-in-the-loop or a fully automated pipeline?
- **Relationship to todo item 1 above**: this is the generalisation of that item — not just the post-remediation question but the entire integration contract.
- **Why it matters**: if spekificity fights against speckit's design, the workflow will be fragile. If it aligns, speckit upgrades are non-breaking.
- **Likely outcome**: a spec for the spekificity ↔ speckit integration contract — defining where spekificity adds value (context loading, graph awareness, lessons) vs. where speckit owns the flow.

### 8.4 Prep and post custom skills

- **What**: `spek prepare` and `spek post` are currently underspecified. They exist as placeholders more than deliberate, well-scoped skills.
- **Think about**: what is the exact ordered sequence of steps for each? What inputs does each step require? What outputs does each step produce? Which steps are mandatory vs. optional? How do prepare and post interact with the automate flow?
- **Relationship to todo items 2, 5, and 6 above**: those items each add a specific capability to prepare/post. This item is the architectural concern — the skill structure, invocation contract, and failure handling.
- **Why it matters**: prepare and post are the bookends of every feature session. If they are unclear or incomplete, every feature starts and ends with context loss or duplicated manual effort.
- **Likely outcome**: a spec for `spek.prepare` and a spec for `spek.post` — each defining the full step sequence, skill dependencies, inputs/outputs, and success criteria.

---

*Each sub-item above (8.1–8.4) should be reviewed, confirmed, and converted into a dedicated spec before or alongside 003 implementation. They are architectural decisions, not implementation details.*

---

## [ ] 9. Investigate `lucasrosati/claude-code-memory-setup` as a reference for memory and context patterns

**Repository**: https://github.com/lucasrosati/claude-code-memory-setup

**Question**: What memory and context management patterns does this repository implement, and what can spekificity adopt or take inspiration from?

- Review how `claude-code-memory-setup` structures persistent memory across sessions.
- Identify any patterns for storing, loading, and refreshing context that complement or improve upon the current spekificity vault + lessons approach.
- Compare its memory lifecycle (write triggers, read triggers, invalidation) against spekificity's planned model (see item 8.2 above).
- Note any tooling, file formats, or conventions that could be reused or adapted — particularly anything relevant to the `spek.prepare` / `spek.post` memory steps.

**Why it matters**: This repository was identified as a real-world example of Claude-based memory setup and may contain proven patterns that spekificity's memory architecture (item 8.2) can build on rather than reinvent.

---

## [ ] 10. Review spec-driven development framework comparison as a reference for speckit positioning

**Article**: https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-sdd-c052df529274

**Question**: How does speckit compare against the broader SDD landscape, and are there patterns or frameworks worth adopting or avoiding?

- Read the comparison of 15 spec-driven development frameworks to understand where speckit sits in the SDD ecosystem.
- Identify any frameworks with stronger remediation loops, persistent context, or automation pipelines that could inform spekificity's design.
- Note any frameworks whose spec → plan → implement flow differs significantly from speckit's — particularly around human-in-the-loop checkpoints (relevant to todo item 1 and 8.3).
- Extract any terminology, conventions, or structural patterns that could sharpen spekificity's own skill and workflow definitions.

**Why it matters**: spekificity extends speckit, but speckit itself exists within a broader SDD space. Understanding how other frameworks handle the same problems (context persistence, remediation, automation) prevents spekificity from solving already-solved problems poorly.

---

## [ ] 11. Investigate Obsidian's official AI skills and their integration potential

**Article**: https://kurtis-redux.medium.com/obsidians-official-skills-are-here-it-s-time-to-let-ai-plug-into-your-local-vault-6c149aae84f6

**Question**: What official skills has Obsidian released for AI integration, and how can spekificity leverage them to improve vault interaction?

- Read the article to understand what Obsidian's official AI skills provide — what operations they expose, what their invocation model looks like, and what access they grant to the local vault.
- Compare Obsidian's official skills against the current spekificity approach to vault interaction (reading decisions, lessons, and graph nodes via file reads and graphify output).
- Identify whether any official Obsidian skills could replace or augment the following spekificity operations:
  - Loading vault context in `spek.context-load`
  - Writing lessons to `vault/lessons/` in `spek.lessons-learnt`
  - Reading architectural decisions and patterns in `spek prepare`
  - Querying the vault graph in `spek.map-codebase`
- Determine whether official Obsidian skills expose a richer query interface (e.g. graph traversal, backlink resolution, dataview-style queries) that would give AI steps more precise vault context than raw file reads.
- Note any authentication, permission, or local-vs-remote constraints that affect whether the skills are usable in a CLI + Copilot agent workflow.

**Why it matters**: Obsidian is a core tool in the spekificity platform. If official AI skills now provide structured, sanctioned access to the vault, spekificity should use them rather than relying on ad-hoc file reads. This could significantly improve context quality for `spek prepare`, `spek post`, and the `spek.context-load` skill, and may resolve or inform items 2, 4, and 8.2 above.
