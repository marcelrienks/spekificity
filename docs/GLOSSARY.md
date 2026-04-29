# Spekificity — Glossary

**Version**: 1.0.0 | **Last Updated**: 2026-04-29

---

## Terms

### AI Agent
An AI-powered assistant integrated into a developer's editor or terminal (e.g., GitHub Copilot, Claude Code) that can read skill files, follow workflow instructions, and generate code or documentation.

### Caveman Mode / Caveman Skill
A skill (`/caveman`) that compresses AI prompts and responses into ultra-concise, technically accurate language, reducing token consumption by approximately 60–75% compared to default verbosity.

### Decorator Pattern
A design approach where Spekificity skills add behaviour to standard SpecKit commands without modifying or replacing them. The underlying SpecKit command remains unchanged; the Spekificity skill wraps it with additional context loading, graph queries, or output processing.

### Graphify
A third-party tool that analyses source code and documentation to produce a dependency/relationship graph. In the Spekificity workflow, Graphify generates the data that populates the Obsidian vault.

### Graph Map / Codebase Map
The output of running Graphify against a project. Represents source files and documentation as nodes, and their relationships (imports, references, dependencies) as edges.

### Idempotent Initialisation
The property of the Spekificity init command whereby running it multiple times on the same project produces the same result — updating where necessary, but never duplicating or destroying existing configuration.

### Lessons Learnt Entry
A structured markdown record created at the end of a SpecKit feature lifecycle. Captures decisions made, problems encountered, patterns discovered, and recommendations for future features. Stored in the Obsidian vault.

### Obsidian
A third-party knowledge management application that uses a local markdown vault. In the Spekificity workflow, Obsidian serves as the persistent context store — holding the graph map, lessons learnt, and AI context notes.

### Obsidian Vault
A local directory of markdown files and metadata managed by Obsidian. In Spekificity, the vault contains: the Graphify-generated graph, lessons learnt entries, and persistent AI context notes.

### Persistent Context
AI-accessible information that survives across sessions. Stored in the Obsidian vault and loaded into the AI agent's context at session start via the context-load skill.

### Skill
A markdown file containing structured instructions that an AI agent reads and executes. Skills define: what they do, when they are triggered, what inputs they expect, what steps to follow, and what outputs they produce. Analogous to a plugin or command for an AI agent.

### SpecKit / Specify
A third-party CLI tool (installed globally) that drives a spec-first, AI-guided software development lifecycle. SpecKit provides the core workflow commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`). Specify is the package that installs SpecKit.

### Spekificity
This project. A meta-tooling layer that connects Graphify, Obsidian, SpecKit, and Caveman into a unified AI development workflow. Contains no application code — only skills, workflows, and setup documentation.

### Spekificity Custom Layer
The set of skills, workflow documents, and setup guides that Spekificity installs locally per-project. Distinct from globally-installed SpecKit — this layer is project-scoped and can be updated independently.

### Token Efficiency
The property of minimising the number of AI tokens consumed to achieve a given outcome. Spekificity improves token efficiency through graph-based context loading (replacing full file scans) and Caveman-compressed interactions.

### Workflow
A documented sequence of skill invocations with defined ordering, inputs, outputs, and branching conditions. Workflows describe how skills compose to complete a multi-step task (e.g., the full SpecKit feature lifecycle).
