# Specificity Constitution

## Core Principles

### I. Skills and Workflows — Not Application Code
Specificity delivers markdown-based skills, workflow guides, and AI agent instructions. It contains no executable application code. Every contribution must be expressible as a skill file, a workflow document, or a setup guide. If something requires code, it belongs in a third-party tool, not in this project.

### II. Decorator Pattern — Never Replace, Always Extend
All Specificity skills MUST wrap and extend standard SpecKit commands without modifying or forking the underlying SpecKit installation. SpecKit remains the authoritative source of its own behaviour. Specificity adds a layer on top. Breaking this principle makes upstream SpecKit updates impossible to absorb.

### III. Modular Independence (NON-NEGOTIABLE)
Each component (Graphify, Obsidian, SpecKit, Specificity custom layer) MUST be independently updatable. No component may hard-wire assumptions about the internal structure of another. When a third-party tool changes, only the adapter skill for that tool should need updating.

### IV. Global SpecKit, Local Customisation
SpecKit/Specify MUST be installed globally so it receives upstream updates normally. Specificity's custom skills MUST be installed locally per-project. This separation ensures that `npm update -g specify` (or equivalent) never requires changes to project-level Specificity files.

### V. Graph-First Context Loading
AI agents interacting with a Specificity-enabled project MUST consult the Obsidian vault graph before reading source files or documentation directories directly. Direct recursive file scanning is the fallback of last resort, not the default. Skills that violate this principle waste tokens and defeat the primary value proposition.

### VI. Token Efficiency by Design
Every skill and workflow MUST consider token consumption. Prompts MUST be as concise as technically safe. Caveman mode integration MUST be available at every workflow step. Verbose context is a defect, not a feature.

### VII. AI-Executable Setup
Any setup step that cannot be fully automated via CLI MUST be documented as a step-by-step guide that an AI agent can execute without human interpretation. Ambiguous or hand-wavy setup instructions are unacceptable.

### VIII. Idempotent Initialisation
The init command MUST be safe to run multiple times. Re-running it on an already-initialised project MUST update without destroying or duplicating configuration. Partial failures MUST leave the project in a consistent, recoverable state.

---

## Supported Environments

- **Operating Systems**: macOS, Linux
- **AI Agents**: GitHub Copilot, Claude Code (initial version)
- **Skill Format**: Markdown (`.agent.md`, `.instructions.md`, `SKILL.md`) compatible with the `.agents/` directory convention
- **No GUI**: All interactions are terminal or AI-chat based

---

## Development Workflow

- All features follow the full SpecKit lifecycle: specify → plan → tasks → implement
- Every skill file MUST include a clear description, trigger conditions, and step-by-step instructions
- Workflow documents MUST specify the order of skill invocations, expected inputs, and expected outputs
- Lessons learnt from each feature MUST be appended to the Obsidian vault before the feature branch is merged

---

## Quality Standards

- A skill is complete only when it can be followed by an AI agent with no additional clarification from the developer
- Setup guides must be validated on a clean environment before being considered complete
- All Specificity skills MUST be tested against both supported AI agents before release
- No skill may assume the developer has knowledge beyond basic terminal usage and git

---

## Governance

This constitution supersedes all other project guidelines. Amendments require:
1. A documented rationale
2. An updated version number
3. A review of all skills and workflows affected by the change

All work on this project must verify compliance with these principles before merging.

**Version**: 1.0.0 | **Ratified**: 2026-04-29 | **Last Amended**: 2026-04-29
