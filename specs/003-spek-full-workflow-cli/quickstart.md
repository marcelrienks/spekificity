# quickstart: spek — full workflow cli

**for**: first-time setup and your first automated feature
**time**: ~20 minutes (excluding obsidian install)

---

## prerequisites before you start

- macOS or Linux terminal
- internet connection (for tool installation)
- a project repository (git initialised)

---

## step 1: install spek

from your project root, add `bin/spek` to your PATH:

```bash
# option a: project-local (no sudo required)
echo 'export PATH="$PWD/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# option b: system-wide (available in all projects)
sudo cp bin/spek /usr/local/bin/spek
chmod +x /usr/local/bin/spek

# verify
spek --version
```

expected output:
```
spek 0.3.0 (spekificity platform)
```

---

## step 2: run setup

`spek setup` detects and installs all prerequisites.

```bash
spek setup
```

expected output:
```
[spek] checking prerequisites...
[spek] ✓ python3 3.11.9 — ok
[spek] ✓ git 2.43.0 — ok
[spek] ✗ uv — not found, installing...
[spek] ✓ uv 0.4.18 — installed
[spek] ✗ specify — not found, installing...
[speckit] installing specify...
[spek] ✓ specify 0.8.0 — installed
[spek] ⚠ obsidian — manual install required
[spek]   download from: https://obsidian.md
[spek]   (optional — spek works without obsidian)
[spek] ⚠ gh — not found
[spek]   install: brew install gh  (optional — needed for automatic PR creation)
[spek] setup complete. required tools: 4/4 ✓ | optional tools: 1/3
[spek] run: spek init
```

**if a required tool fails to install**: follow the on-screen manual installation instructions, then re-run `spek setup`. it is safe to re-run — already-installed tools are skipped.

---

## step 3: initialise the project

`spek init` orchestrates all tool initialisation and installs all skills.

```bash
spek init
```

expected output:
```
[spek] initialising spekificity platform...
[spek] checking prerequisites... ✓
[speckit] initialising specify...
[speckit] .specify/ directory created
[speckit] templates installed
[spek] speckit initialised ✓
[graphify] configuring graphify...
[spek] graphify configured ✓
[spek] creating obsidian vault structure at vault/ ...
[spek] vault/ created ✓
[spek] installing skills...
[spek]   ✓ spek.context-load
[spek]   ✓ spek.map-codebase
[spek]   ✓ spek.lessons-learnt
[spek]   ✓ spek.prepare
[spek]   ✓ spek.automate
[spek]   ✓ spek.post
[spek] skill index written to .spekificity/skill-index.md ✓
[spek] init complete.
[spek] run: spek status  to verify  |  spek prepare  to begin feature work
```

**verify the init**:
```bash
spek status
```

you should see all 6 skills active and all required tools confirmed.

---

## step 4: verify and prepare

before starting feature work, run `spek prepare` to load project context.

```bash
spek prepare
```

on first run, there is no existing graph, so graphify builds from scratch:

```
[spek] starting preparation phase...
[spek] checking graph state... absent
[spek] building graph (first run — this may take 1-2 minutes)...
[graphify] scanning source files...
[graphify] graph built: 47 nodes
[spek] graph built ✓
[spek] loading vault context...
[spek] no lessons learnt entries yet — vault is fresh
[spek] preparation complete. ai session is ready for feature work.
```

subsequent `spek prepare` runs complete in under 60 seconds if the graph is fresh.

---

## step 5: run your first automated feature

now run the full automated lifecycle for a real feature:

```bash
spek automate "add a user settings page with theme toggle and notification preferences"
```

### what happens next

**preflight** (~5 seconds):
```
[spek] starting automated feature lifecycle...
[spek] preflight: checking working tree... ✓ clean
[spek] preflight: creating branch 003-user-settings-page... ✓
```

**spec step** (~2 minutes — ai is writing your spec):
```
[spek] --- step 1/6: spec ---
[speckit] generating feature specification...
[spek] spec complete ✓ (specs/003-user-settings-page/spec.md)
```

**clarification question** (you may be asked 1-3 questions):
```
[spek] ❓ clarification needed (step: spec)
[spek] question: should the theme toggle apply globally or per-session?
> globally, persisted to user profile
[spek] answer recorded. continuing...
```

**plan, tasks, analyse** (~3-5 minutes):
```
[spek] --- step 2/6: plan ---
...
[spek] plan complete ✓
[spek] --- step 3/6: tasks ---
...
[spek] tasks complete ✓ (12 tasks generated)
[spek] --- step 4/6: analyse ---
...
[spek] analyse complete ✓ (no critical issues found)
```

**implementation** (~10-20 minutes depending on feature size):
```
[spek] --- step 6/6: implement ---
[speckit] executing task 1/12: create settings route...
[speckit] executing task 2/12: build theme toggle component...
...
[speckit] all tasks complete ✓
```

**post-flight**:
```
[spek] post-flight: writing lessons learnt...
[spek] ❓ any key decisions or patterns from this feature to record?
> used CSS variables for theme tokens — recommend as standard pattern
[spek] lessons written to vault/lessons/2026-05-03-user-settings-page.md ✓
[spek] post-flight: refreshing graph (incremental)...
[graphify] 8 new nodes added
[spek] graph refreshed ✓
[spek] post-flight: creating pull request...
[spek] PR created: https://github.com/your-org/your-repo/pull/15
[spek] automate complete ✓
```

---

## handling interruptions

if `spek automate` is interrupted (network drop, ctrl-c, session timeout):

```bash
# resume from where it stopped
spek automate --resume
```

the resume command reads `.spekificity/workflow-state.json` and continues from the last completed step. no work is repeated.

---

## after the feature: verify results

```bash
# check the pr was created
gh pr view

# view the new lessons entry
cat vault/lessons/2026-05-03-user-settings-page.md

# check graph was updated
spek status
```

---

## day-to-day usage

| task | command |
|------|---------|
| start a new feature (full auto) | `spek automate "<description>"` |
| start a feature manually (step-by-step) | `spek prepare` then run speckit commands individually |
| capture lessons after manual work | `spek post` |
| check platform health | `spek status` |
| update spekificity skills | `spek update` |
| rebuild codebase graph | `spek prepare --force-refresh` |

---

## troubleshooting

**`spek: command not found`**: PATH not set up. run `export PATH="$PWD/bin:$PATH"` or follow step 1.

**`specify: command not found` during init**: run `spek setup` first. if setup reported specify as installed, check that `~/.local/bin` or the pip install path is in your PATH.

**`vault/graph/ not found` during prepare**: first run of prepare will build the graph from scratch. this is expected.

**pr creation fails**: install and authenticate `gh` with `gh auth login`, then re-run `spek post` or `spek automate --resume`.

**automate halts mid-implementation**: run `spek automate --resume`. if it halts again at the same point, inspect the error in the terminal output and check `specs/<feature>/*.md` for any malformed content.

---

## next steps

- read [docs/guide.md](../../docs/guide.md) for the manual speckit workflow
- read [docs/architecture.md](../../docs/architecture.md) to understand how the components fit together
- read [vault/context/decisions.md](../../vault/context/decisions.md) to see existing architectural decisions
