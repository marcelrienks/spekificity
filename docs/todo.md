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

- **prepare**: explicitly invoke caveman mode at start of session to reduce token consumption throughout the workflow; confirm graphify graph is fresh (not just present); load obsidian vault decisions + patterns + recent lessons before any speckit step.
- **post**: invoke caveman to compress session output before writing; run graphify in incremental mode *after* lessons are written (so new lesson files are included in the graph); update obsidian vault context (decisions.md / patterns.md) with anything new surfaced during the feature.
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
- If graphify does not provide persistent/incremental context across sessions: evaluate whether `cel.docs.read` (which analyses docs and persists a context map to avoid redundant re-reading) should be incorporated into `spek prepare` to fill this gap.
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
- Clarify: does `cel.docs.simplify` operate on the full `docs/` directory, or can it be scoped to files modified in the current feature branch? Prefer scoped operation if possible to avoid unintended rewrites.
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

**Why it matters**: inconsistent naming across `spek.*`, `speckit.*`, and `speckit-enrich.*` creates confusion about what is spekificity-owned vs. speckit-owned vs. glue code. Settling conventions before 003 implementation prevents a naming refactor later.

---

## [ ] 8. High-level concepts to confirm before full implementation

Four foundational areas that need to be thought through and specced before the full platform is built. Each has a corresponding spec in `specs/`.

### 8a. Code and document maps (`specs/004-code-and-document-maps/`)

**Question**: How should the vault graph represent both code topology and documentation topology?

- Currently graphify is assumed to map only source code. Confirm whether it can also index markdown directories (`docs/`, `specs/`, `skills/`).
- If not: decide whether obsidian native wikilinks are sufficient for docs, or whether a separate map-building step is needed.
- Define what a "document map" looks like in the vault and how skills consume it.
- Outcome: `spek.map-codebase` (or a new `spek.map-docs`) produces a combined graph covering both code and documentation, readable by `spek prepare` and speckit enrichment wrappers.

### 8b. Persistent memory and lessons (`specs/005-persistent-memory-and-lessons/`)

**Question**: What is the persistence model for context across AI sessions?

- Graphify nodes are a point-in-time snapshot — they do not accumulate knowledge across sessions.
- Vault lessons are written but not loaded systematically on session start.
- Decide: is `cel.docs.read` needed as a persistent context cache layer, or can vault lessons + decisions fill this role?
- Define the lesson schema so entries are self-contained enough to avoid re-reading full specs in future sessions.
- Outcome: `spek prepare` loads a known set of memory artefacts; `spek post` writes a structured lesson that replaces the need to re-read the spec.

### 8c. Leveraging speckit as it is intended (`specs/006-speckit-workflow-integration/`)

**Question**: What is the canonical speckit lifecycle and how does spekificity wrap it correctly?

- The full flow (specify → plan → tasks → analyze → remediate → implement) is partially understood but the re-entry semantics after remediation are unclear.
- Decide: does `spek automate` re-run `speckit.specify` after remediation, or are spec edits done in place?
- Confirm whether `speckit.implement` expects a prior clean `speckit.analyze` pass.
- Understand `speckit.clarify` and `speckit.checklist` — are they part of the canonical flow or optional utilities?
- Outcome: a confirmed step sequence that `spek automate` implements, with no ambiguity about re-entry or hand-off points.

### 8d. Prepare and post custom skills (`specs/007-prepare-and-post-skills/`)

**Question**: What exactly should `spek prepare` and `spek post` do, step by step?

- Both commands are currently underspecified. The skill definitions need concrete, ordered step lists with configuration points.
- `spek prepare` must: activate caveman (or prompt), verify/refresh graph, load vault context (decisions + patterns + recent lessons), surface summary.
- `spek post` must: write a rich structured lesson, run incremental graph refresh, run `cel.docs.simplify` on modified docs, update vault decisions/patterns if new ones emerged.
- Decide: should caveman be auto-activated by `spek prepare`, or left to the developer?
- Outcome: fully specified skill definitions for both commands that can be directly implemented.
