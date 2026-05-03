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
