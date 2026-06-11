# Implementation Plan: Full Platform Implementation

**Branch**: `003-full-platform-impl` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/003-full-platform-impl/spec.md`

## Summary

Implement the complete Spekificity platform in four phases. Each phase has a distinct type of work and a clean review gate before the next begins.

| Phase | What | Deliverable |
|-------|------|-------------|
| **P1: Foundation** | Package infrastructure | `pyproject.toml` updates, `utils.py`, `prerequisites.py` |
| **P2: Integration modules** | Three independent Python modules + unit tests | `lat_md/`, `vault/`, `speckit/` |
| **P3: Skill files** | Markdown authoring + distribution logic | 7 `.md` files in `spekificity/skills/`, `skills_install/` module |
| **P4: CLI** | Orchestration + integration test | `cli.py`, `test_init_flow.py` |

P1 must land first — it provides shared utilities and unblocks testing of P2–P4. P2 modules are parallel within their phase (no dependencies between lat_md, vault, speckit). P3 can be authored in parallel with P2. P4 depends on all prior phases.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: `click>=8.0` (CLI framework), `shutil` (file copy), `importlib.resources` (package data access), `subprocess` (external tool invocation), `pathlib` (path handling), `json` (MCP config read/write); config write uses inline YAML string — no PyYAML dep needed

**Storage**: Filesystem only — `.spek/` directory tree, per-integration MCP config files, `.git/hooks/post-commit`, `.spek/config.yaml`

**Testing**: pytest; `tmp_path` fixture for isolated filesystem tests; `unittest.mock.patch` for subprocess mocking

**Target Platform**: macOS, Windows, Linux (cross-platform CLI)

**Project Type**: CLI tool / Python package (installable via `uv tool install`)

**Performance Goals**: `spek init` completes in under 5 minutes on a clean project (most time is 3rd-party tool install); no latency requirements on skill file reads

**Constraints**: Python 3.11+ only; requires `uv` and `git` in PATH before running; no sudo; must be idempotent

**Scale/Scope**: Single-developer CLI tool; no concurrency; ~7 skill files + ~12 Python modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-First Development | ✅ PASS | Spec exists, reviewed, and approved |
| II. Token Efficiency | ✅ PASS | Skill files use Caveman; lat.md pre-index avoids file scanning |
| III. Deterministic 4-Stage Workflow | ✅ PASS | Following Prepare → Plan → Implement → Conclude |
| IV. Persistent Memory | ✅ PASS | Plan archived to `.spek/vault/` on conclude |
| V. Simplicity & Composability | ✅ PASS | CLI does one thing; skill files are independent markdown |

All gates pass. No complexity violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/003-full-platform-impl/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   ├── cli-contract.md
│   ├── config-schema.md
│   └── mcp-config-schemas.md
└── tasks.md             # /speckit-tasks output — not created here
```

### Source Code (repository root)

```text
spekificity/
├── __init__.py
│
├── utils.py                        # P1: shared subprocess runner + [OK]/[SKIP]/[WARN]/[ERROR] formatter
├── prerequisites.py                # P1: verify Python 3.11+, uv, Node.js 22+, git in PATH
│
├── lat_md/                         # P2: lat.md integration module
│   ├── __init__.py
│   ├── install.py                  # detect/install lat.md via npm
│   ├── index.py                    # lat init (code) + lat init --docs (doc)
│   ├── mcp_config.py               # write lat MCP entry per integration, merge-safe
│   └── git_hook.py                 # write .git/hooks/post-commit (lat update)
│
├── vault/                          # P2: Obsidian vault module
│   ├── __init__.py
│   ├── install.py                  # detect/install Obsidian (brew/winget/URL); two-phase halt
│   ├── scaffold.py                 # mkdir .spek/vault/, lessons/, memory/, lat/; write decisions.md, patterns.md
│   └── init.py                     # obsidian open-vault; obsidian create initial files
│
├── speckit/                        # P2: SpecKit module
│   ├── __init__.py
│   ├── install.py                  # detect/install specify-cli via uv tool install
│   ├── init.py                     # run specify init
│   └── config.py                   # write .spek/config.yaml
│
├── skills_install/                 # P3: skill file distribution
│   ├── __init__.py
│   ├── integrations.py             # integration → (skills_dir, flat|subfolder) mapping + MCP config mapping
│   └── copy.py                     # copy spekificity/skills/ → target dir; idempotent (never overwrite)
│
├── skills/                         # P3: bundled agent skill files (package data)
│   ├── spek-prepare.md
│   ├── spek-plan.md
│   ├── spek-implement.md
│   ├── spek-conclude.md
│   ├── spek-lessons.md
│   ├── spek-context.md
│   └── spek-map.md
│
└── cli.py                          # P4: spek init command; orchestrates P1–P3 modules

tests/
├── unit/
│   ├── test_prerequisites.py       # P1
│   ├── test_utils.py               # P1
│   ├── lat_md/
│   │   ├── test_install.py         # P2
│   │   ├── test_index.py           # P2
│   │   ├── test_mcp_config.py      # P2
│   │   └── test_git_hook.py        # P2
│   ├── vault/
│   │   ├── test_install.py         # P2
│   │   ├── test_scaffold.py        # P2
│   │   └── test_init.py            # P2
│   ├── speckit/
│   │   ├── test_install.py         # P2
│   │   ├── test_init.py            # P2
│   │   └── test_config.py          # P2
│   └── skills_install/
│       ├── test_integrations.py    # P3
│       └── test_copy.py            # P3
└── integration/
    └── test_init_flow.py           # P4: full end-to-end spek init

pyproject.toml                      # P1: add pytest dev dep, package-data for skills/*.md
```

**Structure Decision**: Single project layout. Modules grouped by phase. `vault/scaffold.py` also owns `.spek/memory/` and `.spek/lat/` directory creation (all `.spek/` subdirs in one place). `skills_install/` is separate from `skills/` — content and distribution are different concerns. `cli.py` is intentionally thin: it reads flags/prompts, calls each module in order, and handles the exit code. No business logic in `cli.py`.

## P5: Gap Fixes (post-review)

Three gaps found in implementation review. All are self-contained fixes.

| Gap | File | Fix |
|-----|------|-----|
| FR-002: No version validation | `spekificity/prerequisites.py` | Parse `python --version` / `node --version` output; extract major.minor; `sys.exit(1)` if Python < 3.11 or Node < 22 |
| FR-011/SC-006: Wrong halt text | `spekificity/vault/install.py` | Replace `_print_registration_instructions()` body with verbatim text from `wiki/setup.md` "Phase 1 halt" block |
| FR-020: Wrong skill section headers | `spekificity/skills/*.md` (all 7) | Rewrite each file to use `## Prerequisites`, `## Steps`, `## Output`, `## Exit Criteria` in that order |

**Version parsing approach** (FR-002):
```python
import re, sys as _sys

def _check_version(cmd: str, min_major: int, min_minor: int) -> bool:
    raw = _get_version(cmd) or ""
    m = re.search(r"(\d+)\.(\d+)", raw)
    if not m:
        return False
    return (int(m.group(1)), int(m.group(2))) >= (min_major, min_minor)
```
Python check: `python --version` → parse `3.X.Y` → require `(3, 11)`.
Node check: `node --version` → parse `vX.Y.Z` → require `(22, 0)`.
`uv` and `git`: PATH presence only, no version constraint.

## Complexity Tracking

> No constitution violations to justify.
