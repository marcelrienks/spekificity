# setup guide: speckit / specify

## overview

speckit (installed via the `specify-cli` package) is the spec-driven development workflow engine that spekificity is built on top of. it provides the `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` commands that structure the ai development lifecycle. spekificity wraps these commands with graph-aware context — it does not replace them.

## install mode

**global** — installed per machine via `uv tool install`. spekificity custom skills are installed per project (layered on top).

## prerequisites

- python 3.11+
- `uv` installed (`uv --version` returns a version)
- `git` installed (`git --version` returns a version)
- internet access for initial install

## installation steps

1. install speckit globally:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. confirm the `specify` command is on your path:
   ```bash
   which specify
   # expected: /users/<you>/.local/bin/specify or similar
   ```

3. initialise speckit in your project:
   ```bash
   cd /path/to/your/project
   specify init .
   ```

   when prompted:
   - **ai assistant**: select `copilot` (github copilot) or `claude` (claude code)
   - **script type**: select `sh`

   this creates:
   - `.specify/` — speckit configuration, templates, scripts, extensions
   - `.github/agents/` — agent skill files (copilot)
   - `.github/copilot-instructions.md` — copilot context pointer

## verification

```bash
specify --version
# expected output: specify-cli x.x.x
```

after `specify init .`:
```bash
ls .specify/
# expected: extensions.yml  memory/  scripts/  templates/
```

## configuration

speckit configuration lives in `.specify/`:

- **`.specify/extensions.yml`** — hook definitions for `before_specify`, `before_plan`, `before_implement`, etc. spekificity enrichment skills can be registered here.
- **`.specify/memory/constitution.md`** — project constitution. edit this to add project-specific principles.
- **`.specify/templates/`** — override speckit default templates for spec, plan, and tasks.

## version compatibility

| speckit version | spekificity compatible | notes |
|----------------|----------------------|-------|
| ≥ 0.8.0 | ✓ | extensions/hooks system required |
| 0.7.x | ⚠ | no extensions.yml; enrichment skills must be invoked manually |
| < 0.7.0 | ✗ | unsupported |

## the `specify init .` workflow

running `specify init .` is **idempotent** — safe to run multiple times:
- if speckit is already initialised, it updates templates and scripts without overwriting your constitution or custom configuration.
- new speckit versions: run `uv tool upgrade specify-cli` then re-run `specify init .` to pick up new templates.

## troubleshooting

- **symptom**: `specify: command not found` → **fix**: run the install command above; ensure `~/.local/bin` is in your `path`
- **symptom**: `specify init .` fails with git error → **fix**: ensure the project folder is a git repository (`git init` first) or create it first
- **symptom**: hooks in `extensions.yml` not firing → **fix**: check `enabled: true` and `optional: false` for mandatory hooks; confirm you are using speckit ≥ 0.8.0
- **symptom**: templates not applied → **fix**: check `.specify/templates/` for overrides; run `specify init .` again to refresh
