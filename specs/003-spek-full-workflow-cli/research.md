# research: spek — full workflow cli

**feature**: `003-spek-full-workflow-cli`
**phase**: 0 — pre-design research
**date**: 2026-05-03
**status**: complete — all unknowns resolved

---

## r-001: spek cli distribution and installation

**unknown**: how should `spek` be installed as a terminal command on macOS and Linux without requiring a package manager or compiled binary?

**research findings**:
- bash/zsh scripts are the established delivery format in this codebase (see `.specify/scripts/bash/`)
- `chmod +x bin/spek && sudo cp bin/spek /usr/local/bin/spek` is the standard unix approach for single-file cli tools
- `curl -fsSL <url> | bash` installer scripts are widely used (homebrew, oh-my-zsh, rvm) and ai-executable
- path-based approaches (add `bin/` to `$PATH` in `.bashrc`/`.zshrc`) avoid requiring sudo and are better for project-local tools

**decision**: ship `spek` as a single executable bash script at `bin/spek`. installation instructions offer two paths: (a) system-wide via `sudo cp` to `/usr/local/bin/`, (b) project-local via `export PATH="$PWD/bin:$PATH"` in shell rc. installer script at `.spekificity/install.sh` automates the system-wide path.

**rationale**: zero runtime dependencies. bash is available on every macOS and Linux system. consistent with existing script conventions. no build step required for users.

**alternatives considered**:
- python cli with pip install: adds python version dependency, pip environment management, and requires `pip` to be installed. rejected.
- npm global package: requires node. rejected — node is not a current project dependency.
- compiled go binary: portable, fast, but requires a build pipeline and binary distribution. over-engineered for this use case. rejected.
- homebrew formula: good for wide distribution but overkill for a project-local tool. deferred to post-v1.

---

## r-002: speckit programmatic invocation

**unknown**: how can `spek automate` programmatically invoke speckit lifecycle steps (spec → plan → tasks → analyse → implement) without requiring manual developer commands?

**research findings**:
- speckit is an ai skill system — commands like `/speckit.specify` are instructions for an ai agent (copilot, claude code), not executable binaries
- there is no speckit cli binary to subprocess-call
- the ai agent is the "runtime" for speckit commands
- the pattern established in `speckit-enrich/` (e.g., `plan-enrich.md`) shows that one skill can orchestrate another by issuing instructions that the ai follows in sequence
- `spek.automate` therefore functions as a meta-skill: the ai reads the skill and executes the speckit lifecycle steps in order

**decision**: `/spek.automate` is a markdown ai agent skill that instructs the ai to: (1) invoke `/speckit.specify` with the provided description, (2) wait for completion detection (r-003), (3) invoke `/speckit.plan`, (4) continue through each lifecycle step in order. the ai is the execution engine. no subprocess orchestration is needed.

**rationale**: aligns with the existing decorator pattern. `/speckit-enrich-implement` in `skills/speckit-enrich/implement-enrich.md` already demonstrates multi-skill orchestration in a single markdown skill. the same pattern applies here.

**alternatives considered**:
- parse speckit cli tool output (if one existed): would need a stable machine-readable output format. speckit has no cli binary. rejected.
- use speckit's internal api/library: speckit is not a library, it is a set of ai skills. rejected.
- have the ai issue shell commands that trigger ai sessions: shell commands cannot start new ai sessions. the ai must orchestrate within its own session. confirmed approach is the only viable path.

---

## r-003: speckit step completion detection

**unknown**: how does `/spek.automate` know when a speckit lifecycle step (spec, plan, tasks, analyse, implement) is complete so it can proceed to the next step?

**research findings**:
- speckit writes predictable output files to `specs/<feature-dir>/` — `spec.md`, `plan.md`, `tasks.md`
- `tasks.md` uses checkboxes (`- [ ]` / `- [x]`) to track task completion — when all are `[x]`, implementation is complete
- the ai can read the output file after each step to verify it exists and has required content
- "analyse" step completion: the ai agent running `/speckit.analyze` completes when it returns its analysis report (no output file — completion is in-session)
- "implement" completion: all tasks in `tasks.md` are checked `[x]` — verifiable by reading the file
- halt detection: if speckit stops mid-implementation, tasks remain `[ ]` — the ai detects this and re-invokes the implement skill with "continue from last incomplete task"

**decision**: step completion detection is file-based for spec/plan/tasks steps (file exists + has minimum content), and checkbox-based for implement (all `[x]` in tasks.md). the ai reads the file after each step. if completion is not confirmed, the ai re-runs the step.

**rationale**: file-based detection is robust, verifiable, and does not depend on speckit output format changes. all speckit output files are already defined in existing specs.

**alternatives considered**:
- timeout-based: assume step is complete after N seconds. unreliable and fragile. rejected.
- output marker injection: require speckit to write a `STEP_COMPLETE` marker. this would require modifying speckit internals. rejected (violates constitution principle ii).
- speckit api query: no api exists. rejected.

---

## r-004: graph staleness detection

**unknown**: how does `spek prepare` determine whether the graphify graph is stale (i.e., codebase has changed since last graph build)?

**research findings**:
- `vault/graph/index.md` is the graphify graph entry point — its modification time reflects the last graph build
- `git log -1 --format=%ct HEAD` returns the epoch timestamp of the most recent commit
- `stat -f %m vault/graph/index.md` (macOS) / `stat -c %Y vault/graph/index.md` (Linux) returns the file's epoch modification time
- comparison: if git HEAD commit timestamp > graph file timestamp → stale
- portable comparison requires a cross-platform `stat` call — handled by detecting OS (`uname -s`) and using the appropriate flag
- "absent" state: if `vault/graph/index.md` does not exist, graph has never been built

**decision**:
```bash
# staleness check in prepare.sh
GRAPH_FILE="vault/graph/index.md"
if [ ! -f "$GRAPH_FILE" ]; then
  GRAPH_STATE="absent"
elif [ "$(uname -s)" = "Darwin" ]; then
  GRAPH_TS=$(stat -f %m "$GRAPH_FILE")
  GIT_TS=$(git log -1 --format=%ct HEAD 2>/dev/null || echo 0)
  [ "$GIT_TS" -gt "$GRAPH_TS" ] && GRAPH_STATE="stale" || GRAPH_STATE="fresh"
else
  GRAPH_TS=$(stat -c %Y "$GRAPH_FILE")
  GIT_TS=$(git log -1 --format=%ct HEAD 2>/dev/null || echo 0)
  [ "$GIT_TS" -gt "$GRAPH_TS" ] && GRAPH_STATE="stale" || GRAPH_STATE="fresh"
fi
```

**rationale**: git and stat are universally available on target platforms. no additional dependencies. the check is fast (< 100ms). handles the absent/stale/fresh tri-state required by the spec (US3 acceptance criteria).

**alternatives considered**:
- md5 hash of all source files vs stored hash: accurate but expensive for large codebases. deferred to v2 enhancement.
- count source files vs graph node count: misses file modifications without addition/deletion. rejected.
- always rebuild: ignores the sc-006 performance requirement (< 60s). rejected.

---

## r-005: pr creation

**unknown**: what is the best approach for `spek automate` to create a pull request after implementation completes?

**research findings**:
- `gh pr create` is the standard github cli command for pr creation from terminal
- `gh` is widely installed on macOS (`brew install gh`) and Linux
- `gh` requires authentication (`gh auth login`) — if not authenticated, `gh pr create` fails with a clear error
- fallback without `gh`: print formatted pr title, body, and source/target branch to terminal with instructions for manual creation
- pr description can be auto-generated from the feature spec overview + user story list
- `gh pr create --title "..." --body "..." --base main --head <branch>` creates pr non-interactively

**decision**: attempt `gh pr create` first (check `command -v gh && gh auth status`). if either check fails, print formatted pr description to terminal and suggest `gh auth login` for future runs. pr body is auto-generated from `spec.md` overview section.

**rationale**: `gh` is the official first-party tool for this operation. the terminal fallback ensures the workflow never hard-fails at the pr step. the developer can always create the pr manually from the printed output.

**alternatives considered**:
- github api direct (curl): requires manually managing personal access tokens in env vars. security risk. rejected.
- `hub` cli: less maintained, superseded by `gh`. rejected.
- open browser via `open` / `xdg-open`: opens a url with pre-filled pr content (github's compare url). viable fallback but not ai-executable. deferred to v2.

---

## r-006: workflow state serialization

**unknown**: how should `spek automate` persist its progress so that `spek automate --resume` can correctly re-enter the workflow after an interruption?

**research findings**:
- simple json file is the established pattern in this codebase (`.specify/feature.json`, `.spekificity/config.json`)
- workflow state needs: current feature branch, feature directory, completed steps, current step, any pending questions, timestamp
- json is human-readable (developer can inspect state), ai-readable (ai can read the file on resume), and editable by developers if needed
- atomic write: write to a temp file then `mv` to avoid partial writes on interruption
- the ai reads `.spekificity/workflow-state.json` at resume to determine next step, then continues the skill from that step

**decision**: persist state as `.spekificity/workflow-state.json` with the schema defined in `data-model.md`. write atomically. on `spek automate --resume`, the ai reads this file first and begins the `spek.automate` skill from the `next_step` field.

**rationale**: file-based state is the simplest, most portable approach. no database, no daemon, no background process. consistent with existing codebase patterns.

**alternatives considered**:
- environment variables: lost when the terminal session ends. does not survive ctrl-c or session timeout. rejected.
- sqlite: portable but requires sqlite to be installed. overkill. rejected.
- git notes / tags: clever but obscure — hard for developers to inspect or edit if needed. rejected.

---

## open questions (resolved)

| id | question | resolution |
|----|----------|------------|
| r-001 | how to distribute `spek` without a package manager? | bash script + path export or sudo cp |
| r-002 | how does spek programmatically drive speckit? | ai skill orchestration — ai reads `/spek.automate` and drives speckit steps in-session |
| r-003 | how to detect speckit step completion? | file existence + checkbox state for implement; ai verifies each step before proceeding |
| r-004 | how to detect graph staleness? | git HEAD timestamp vs graph file mtime — portable bash comparison |
| r-005 | how to create prs from terminal? | `gh pr create` with terminal fallback if gh unavailable/unauthenticated |
| r-006 | how to persist automate state across interruptions? | `.spekificity/workflow-state.json` json file, atomically written |

all unknowns resolved. phase 1 design can proceed.
