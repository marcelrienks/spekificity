
<p align="center">
  <img src="spekificity/assets/logo.png" alt="Spekificity Logo" width="100%">
</p>

**Specification-Driven Agent Development Framework** — Connects the tools you're already using.

It orchestrates **SpecKit** (structured planning) + **lat.md** (code indexing—no manual search) + **Obsidian vault** (decision history) + **Caveman** mode (token efficiency) into one workflow. 

**No new concepts.** Just less friction: setup in minutes, straightforward commands, spec-first procedures that eliminate context-switching.

The heavy lifting comes from best-in-class tools. What we built is the **glue**: one setup, clear procedures, and an opinionated workflow that makes them work together instead of in silos. 🧩

---

## Quick Start (5 Minutes)

# 1. Install globally (one time)
```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```
# 2. Set up a project
```bash
cd /path/to/your/project
```
```bash
spek init
```
# 3. Prepare for a feature
```bash
spek prepare "Your feature name"
```
# 4. Generate a plan
```bash
spek plan "Your feature description"
```
# 5. Start building
```bash
spek implement --task T1.1
```

**Next:** Read [Quick Start Workflow](#quick-start-workflow) for detailed walkthrough, or [wiki/vision.md](wiki/vision.md) for design philosophy.

---

## Key Features

- **Spec-Driven Workflow** — All work starts with structured specification
- **Persistent Memory** — Decisions, patterns, lessons stored in Git-backed vault
- **Token Efficiency** — Pre-indexed code analysis (lat.md) + Caveman compression
- **Deterministic Sequencing** — 4-stage workflow (Prepare → Plan → Implement → Conclude)
- **Composable Skills** — `/spek.*` commands designed to be chainable or independently runnable

---

## Requirements

Minimal dependencies — all standard tools:

- **Python 3.11+** — Check with `python3 --version`
- **`uv` package manager** — [Quick install](https://docs.astral.sh/uv/)
- **Git** — Already initialized in your project
- **Obsidian CLI** — *(Optional)* Only needed for vault graph exports

All other dependencies install automatically via `uv tool install`.

---

## Installation

Global install (one-time):
```bash
uv tool install spekificity --from git+https://github.com/marcelrienks/spekificity.git
```

Per-project setup:
```bash
cd /path/to/your/project && spek init
```

**Detailed setup:** [wiki/setup.md](wiki/setup.md)

---

**Full workflow details, command reference, vault structure examples, and design philosophy:** See [wiki/workflow.md](wiki/workflow.md) and [wiki/vision.md](wiki/vision.md).

---

## Documentation

### First-Time Setup

1. **Install Globally:** `uv tool install spekificity --from git+...`
2. **Read:** [wiki/vision.md](wiki/vision.md) — Understand core design (four pillars, philosophy)
3. **Read:** [wiki/architecture.md](wiki/architecture.md) — How components fit together

### First Feature Development

1. **Workflow:** [wiki/workflow.md](wiki/workflow.md) — 4-stage workflow with entry/exit criteria
2. **Skills Reference:** [wiki/skills.md](wiki/skills.md) — `/spek.*` command reference
3. **Patterns:** [wiki/patterns.md](wiki/patterns.md) — Reusable patterns for common tasks

### Daily Reference

| Document | Use When |
|----------|----------|
| [wiki/workflow.md](wiki/workflow.md) | Executing a feature |
| [wiki/skills.md](wiki/skills.md) | Looking up `/spek.*` command syntax |
| [wiki/conventions.md](wiki/conventions.md) | Naming files, directories, specs |
| [wiki/patterns.md](wiki/patterns.md) | Finding a reusable pattern |
| [wiki/decision.md](wiki/decision.md) | Understanding architectural choices |

---

## Troubleshooting

**Full troubleshooting guide:** [wiki/troubleshooting.md](wiki/troubleshooting.md)

---

## Contributing

Contributions welcome! Please:

1. Create a feature branch from `main`
2. Submit specs and documentation following [wiki/conventions.md](wiki/conventions.md)
3. Include test cases and lessons learned

---

## License

MIT License — see [LICENSE](LICENSE) for details.

**Copyright © 2026 Marcel Rienks**

---

## Next Steps

1. **Install:** `uv tool install spekificity --from git+...`
2. **Initialize:** `cd /your/project && spek init`
3. **Start:** `spek prepare "Your Feature Name"`
4. **Learn:** Read [wiki/vision.md](wiki/vision.md) and [wiki/workflow.md](wiki/workflow.md)
5. **Build:** Execute your first feature using the 4-stage workflow

**Documentation Status**: Production ready ✓
**Last Updated**: 2026-06-07
