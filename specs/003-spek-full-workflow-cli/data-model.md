# data model: spek — full workflow cli

**feature**: `003-spek-full-workflow-cli`
**phase**: 1 — design
**date**: 2026-05-03

---

## overview

five primary entities govern the `spek` platform state. all are stored as files (json or markdown) in `.spekificity/` or `vault/`. no database or runtime service is required.

---

## entity 1: SpekConfig

**file**: `.spekificity/config.json`
**purpose**: tracks platform initialisation state, installed tool versions, and enabled integrations. written by `spek init`, read by `spek status` and all other commands.

### schema

```json
{
  "schema_version": "1.0",
  "spekificity_version": "string",
  "initialized_at": "ISO-8601 timestamp",
  "last_updated": "ISO-8601 timestamp",
  "tools": {
    "speckit": {
      "installed": true,
      "version": "string",
      "detection_command": "specify --version"
    },
    "graphify": {
      "installed": true,
      "version": "string",
      "detection_command": "graphify --version",
      "optional": true
    },
    "obsidian": {
      "installed": false,
      "manual_only": true,
      "manual_confirmed": false,
      "optional": true
    },
    "caveman": {
      "installed": true,
      "optional": true
    },
    "gh": {
      "installed": true,
      "authenticated": true,
      "optional": true,
      "detection_command": "gh auth status"
    }
  },
  "skills": {
    "installed": ["spek.context-load", "spek.map-codebase", "spek.lessons-learnt", "spek.prepare", "spek.automate", "spek.post"],
    "skill_index_path": ".spekificity/skill-index.md"
  },
  "vault": {
    "path": "vault/",
    "graph_path": "vault/graph/index.md",
    "lessons_path": "vault/lessons/",
    "context_path": "vault/context/"
  }
}
```

### field descriptions

| field | type | description |
|-------|------|-------------|
| `schema_version` | string | config schema version — used for migration |
| `spekificity_version` | string | version of the spekificity platform installed |
| `initialized_at` | ISO-8601 | when `spek init` was first run |
| `last_updated` | ISO-8601 | when config was last written |
| `tools.*` | object | per-tool install state, version, and detection command |
| `tools.*.optional` | bool | if true, setup may complete without this tool |
| `tools.*.manual_only` | bool | if true, tool cannot be auto-installed (e.g., obsidian gui) |
| `tools.*.manual_confirmed` | bool | if true, developer has confirmed manual installation is complete; set via `spek setup --confirm-manual <tool>` |
| `tools.gh.authenticated` | bool | whether `gh auth status` passes — set at init time |
| `skills.installed` | string[] | list of installed skill names |
| `vault.*` | object | paths to vault components — may be customised |

### validation rules
- `schema_version` must be `"1.0"` for current implementation
- `initialized_at` must be set before any other `spek` command runs
- if `tools.speckit.installed` is false, `spek init` must halt with error
- `tools.*.optional: true` tools may have `installed: false` without blocking init

---

## entity 2: WorkflowState

**file**: `.spekificity/workflow-state.json`
**purpose**: tracks the current `spek automate` session. enables resume after interruption. written atomically after each completed step. read by `spek automate --resume`.

### schema

```json
{
  "schema_version": "1.0",
  "feature_description": "string",
  "feature_branch": "string",
  "feature_dir": "string",
  "started_at": "ISO-8601 timestamp",
  "last_updated": "ISO-8601 timestamp",
  "status": "in-progress | halted | complete",
  "current_step": "string",
  "next_step": "string",
  "completed_steps": ["string"],
  "pending_questions": [
    {
      "step": "string",
      "question": "string",
      "answer": "string | null"
    }
  ],
  "preflight": {
    "branch_created": true,
    "clean_working_tree": true
  },
  "postflight": {
    "lessons_written": false,
    "graph_refreshed": false,
    "pr_created": false,
    "pr_url": "string | null"
  }
}
```

### step values (ordered)

```text
preflight → spec → plan → tasks → analyse → remediation → implement → postflight → complete
```

### field descriptions

| field | type | description |
|-------|------|-------------|
| `feature_description` | string | the natural-language description passed to `spek automate` |
| `feature_branch` | string | git branch created for this feature (e.g., `003-add-user-login`) |
| `feature_dir` | string | specs directory for this feature (e.g., `specs/003-add-user-login/`) |
| `status` | enum | overall session status |
| `current_step` | string | the step currently executing |
| `next_step` | string | the step to begin on resume |
| `completed_steps` | string[] | ordered list of steps that have finished successfully |
| `pending_questions` | object[] | questions surfaced during this session and developer answers |
| `preflight.branch_created` | bool | whether the feature branch was created successfully |
| `postflight.*` | bool | completion flags for each post-flight task |

### validation rules
- `next_step` must be one of the defined step values
- `status` is set to `complete` only when `next_step` is `complete` and all steps are in `completed_steps`
- write is atomic: write to `.spekificity/workflow-state.json.tmp` then `mv` to final path
- only one workflow-state.json exists at a time — concurrent automate runs are not supported (fr-015 / assumption: single active feature)

### resume logic
on `spek automate --resume`:
1. read `workflow-state.json`
2. verify `status` is `in-progress` or `halted` (not `complete`)
3. pass `next_step` and `completed_steps` to the `/spek.automate` skill
4. skill begins execution from `next_step`, skipping all steps in `completed_steps`

---

## entity 3: SkillIndex

**file**: `.spekificity/skill-index.md`
**purpose**: unified registry of all installed skills and commands. generated by `spek init`. read by ai agents for skill discovery. must be kept in sync when skills are added/updated.

### format

```markdown
# skill index

generated by `spek init` — do not edit manually.
last updated: <ISO-8601 timestamp>

## spekificity skills (/spek.*)

| command | file | description | status |
|---------|------|-------------|--------|
| /spek.context-load | .spekificity/skills/spek.context-load.md | load vault graph and context | active |
| /spek.map-codebase | .spekificity/skills/spek.map-codebase.md | build or refresh graphify graph | active |
| /spek.lessons-learnt | .spekificity/skills/spek.lessons-learnt.md | write lessons to vault | active |
| /spek.prepare | .spekificity/skills/spek.prepare.md | preparation phase skill | active |
| /spek.automate | .spekificity/skills/spek.automate.md | automated speckit lifecycle | active |
| /spek.post | .spekificity/skills/spek.post.md | post-implementation tasks | active |

## speckit skills (/speckit.*)

| command | file | description | status |
|---------|------|-------------|--------|
| /speckit.specify | .github/agents/speckit.specify.md | create feature spec | active |
| /speckit.plan | .github/agents/speckit.plan.md | create implementation plan | active |
| /speckit.tasks | .github/agents/speckit.tasks.md | generate tasks | active |
| /speckit.implement | .github/agents/speckit.implement.md | execute implementation | active |
| /speckit.analyze | .github/agents/speckit.analyze.md | cross-artifact analysis | active |

## caveman skills

| command | file | description | status |
|---------|------|-------------|--------|
| /caveman | ~/.agents/skills/caveman/SKILL.md | full token compression | active |
| /caveman lite | ~/.agents/skills/caveman/SKILL.md | lite token compression | active |
```

### field descriptions

| field | description |
|-------|-------------|
| `command` | the slash-command the ai uses to invoke the skill |
| `file` | path to the skill markdown file |
| `description` | one-line description for ai discovery |
| `status` | `active` or `disabled` — disabled skills are listed but not discoverable |

### validation rules
- file must exist at the listed path at time of `spek init`
- duplicate command names are not allowed
- `spek status` reports a warning for any skill with `status: active` where the file does not exist

---

## entity 4: GraphState

**type**: derived (not persisted as a file — computed at runtime)
**purpose**: represents the currency of the graphify graph relative to the codebase.

### states

| state | condition | action required |
|-------|-----------|-----------------|
| `absent` | `vault/graph/index.md` does not exist | run `/spek.map-codebase` (full build) |
| `stale` | git HEAD commit timestamp > graph file mtime | run `/spek.map-codebase` (incremental refresh) |
| `fresh` | git HEAD commit timestamp ≤ graph file mtime | no action required |

### detection logic (bash)

```bash
compute_graph_state() {
  local graph_file="${VAULT_PATH}/graph/index.md"
  if [ ! -f "$graph_file" ]; then
    echo "absent"; return
  fi
  local git_ts
  git_ts=$(git log -1 --format=%ct HEAD 2>/dev/null || echo 0)
  local graph_ts
  if [ "$(uname -s)" = "Darwin" ]; then
    graph_ts=$(stat -f %m "$graph_file")
  else
    graph_ts=$(stat -c %Y "$graph_file")
  fi
  [ "$git_ts" -gt "$graph_ts" ] && echo "stale" || echo "fresh"
}
```

---

## entity 5: ToolPrerequisite

**type**: static definition (not a persisted file — defined in `setup.sh`)
**purpose**: defines the set of tools `spek setup` must verify and optionally install.

### schema

```bash
# each tool is represented as a set of variables in setup.sh
# tool_name | required | detection_command | install_command | manual_url
TOOLS=(
  "python3|required|python3 --version|brew install python3 OR apt-get install python3|https://python.org"
  "uv|required|uv --version|curl -Lsf https://astral.sh/uv/install.sh | sh|https://github.com/astral-sh/uv"
  "git|required|git --version|brew install git OR apt-get install git|https://git-scm.com"
  "specify|required|specify --version|pip install specify|https://github.com/speckit/specify"
  "graphify|optional|graphify --version|pip install graphify|https://github.com/graphify/graphify"
  "gh|optional|gh --version|brew install gh OR apt-get install gh|https://cli.github.com"
  "obsidian|optional|manual_only|N/A|https://obsidian.md"
)
```

### field descriptions

| field | description |
|-------|-------------|
| `tool_name` | identifier used in SpekConfig `tools.*` |
| `required` | if `required`, setup fails if tool cannot be installed; if `optional`, setup continues with a warning |
| `detection_command` | command to check if tool is installed |
| `install_command` | command to auto-install (may be `N/A` for manual-only tools) |
| `manual_url` | url shown to developer if auto-install is unavailable |

### classification

**required** (setup fails without these):
- `python3` (3.11+)
- `uv`
- `git`
- `specify` (speckit cli)

**optional** (setup completes without these, with warning):
- `graphify`
- `gh` (pr creation falls back to terminal output)
- `obsidian` (manual install only — gui app)
- `caveman` (installed as a skill, not a system binary)
