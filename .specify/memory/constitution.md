# specificity constitution

## core principles

### i. skills and workflows — not application code
specificity delivers markdown-based skills, workflow guides, and ai agent instructions. it contains no executable application code. every contribution must be expressible as a skill file, a workflow document, or a setup guide. if something requires code, it belongs in a third-party tool, not in this project.

### ii. decorator pattern — never replace, always extend
all specificity skills must wrap and extend standard speckit commands without modifying or forking the underlying speckit installation. speckit remains the authoritative source of its own behaviour. specificity adds a layer on top. breaking this principle makes upstream speckit updates impossible to absorb.

### iii. modular independence (non-negotiable)
each component (graphify, obsidian, speckit, specificity custom layer) must be independently updatable. no component may hard-wire assumptions about the internal structure of another. when a third-party tool changes, only the adapter skill for that tool should need updating.

### iv. global speckit, local customisation
speckit/specify must be installed globally so it receives upstream updates normally. specificity's custom skills must be installed locally per-project. this separation ensures that `npm update -g specify` (or equivalent) never requires changes to project-level specificity files.

### v. graph-first context loading
ai agents interacting with a specificity-enabled project must consult the obsidian vault graph before reading source files or documentation directories directly. direct recursive file scanning is the fallback of last resort, not the default. skills that violate this principle waste tokens and defeat the primary value proposition.

### vi. token efficiency by design
every skill and workflow must consider token consumption. prompts must be as concise as technically safe. caveman mode integration must be available at every workflow step. verbose context is a defect, not a feature.

### vii. ai-executable setup
any setup step that cannot be fully automated via cli must be documented as a step-by-step guide that an ai agent can execute without human interpretation. ambiguous or hand-wavy setup instructions are unacceptable.

### viii. idempotent initialisation
the init command must be safe to run multiple times. re-running it on an already-initialised project must update without destroying or duplicating configuration. partial failures must leave the project in a consistent, recoverable state.

---

## supported environments

- **operating systems**: macos, linux
- **ai agents**: github copilot, claude code (initial version)
- **skill format**: markdown (`.agent.md`, `.instructions.md`, `skill.md`) compatible with the `.agents/` directory convention
- **no gui**: all interactions are terminal or ai-chat based

---

## development workflow

- all features follow the full speckit lifecycle: specify → plan → tasks → implement
- every skill file must include a clear description, trigger conditions, and step-by-step instructions
- workflow documents must specify the order of skill invocations, expected inputs, and expected outputs
- lessons learnt from each feature must be appended to the obsidian vault before the feature branch is merged

---

## quality standards

- a skill is complete only when it can be followed by an ai agent with no additional clarification from the developer
- setup guides must be validated on a clean environment before being considered complete
- all specificity skills must be tested against both supported ai agents before release
- no skill may assume the developer has knowledge beyond basic terminal usage and git

---

## governance

this constitution supersedes all other project guidelines. amendments require:
1. a documented rationale
2. an updated version number
3. a review of all skills and workflows affected by the change

all work on this project must verify compliance with these principles before merging.

**version**: 1.0.0 | **ratified**: 2026-04-29 | **last amended**: 2026-04-29
