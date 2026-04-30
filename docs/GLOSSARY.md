# spekificity — glossary

**version**: 1.0.0 | **last updated**: 2026-04-29

---

## terms

### ai agent
an ai-powered assistant integrated into a developer's editor or terminal (e.g., github copilot, claude code) that can read skill files, follow workflow instructions, and generate code or documentation.

### caveman mode / caveman skill
a skill (`/caveman`) that compresses ai prompts and responses into ultra-concise, technically accurate language, reducing token consumption by approximately 60–75% compared to default verbosity.

### decorator pattern
a design approach where spekificity skills add behaviour to standard speckit commands without modifying or replacing them. the underlying speckit command remains unchanged; the spekificity skill wraps it with additional context loading, graph queries, or output processing.

### graphify
a third-party tool that analyses source code and documentation to produce a dependency/relationship graph. in the spekificity workflow, graphify generates the data that populates the obsidian vault.

### graph map / codebase map
the output of running graphify against a project. represents source files and documentation as nodes, and their relationships (imports, references, dependencies) as edges.

### idempotent initialisation
the property of the spekificity init command whereby running it multiple times on the same project produces the same result — updating where necessary, but never duplicating or destroying existing configuration.

### lessons learnt entry
a structured markdown record created at the end of a speckit feature lifecycle. captures decisions made, problems encountered, patterns discovered, and recommendations for future features. stored in the obsidian vault.

### obsidian
a third-party knowledge management application that uses a local markdown vault. in the spekificity workflow, obsidian serves as the persistent context store — holding the graph map, lessons learnt, and ai context notes.

### obsidian vault
a local directory of markdown files and metadata managed by obsidian. in spekificity, the vault contains: the graphify-generated graph, lessons learnt entries, and persistent ai context notes.

### persistent context
ai-accessible information that survives across sessions. stored in the obsidian vault and loaded into the ai agent's context at session start via the context-load skill.

### skill
a markdown file containing structured instructions that an ai agent reads and executes. skills define: what they do, when they are triggered, what inputs they expect, what steps to follow, and what outputs they produce. analogous to a plugin or command for an ai agent.

### speckit / specify
a third-party cli tool (installed globally) that drives a spec-first, ai-guided software development lifecycle. speckit provides the core workflow commands (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`). specify is the package that installs speckit.

### spekificity
this project. a platform that connects graphify, obsidian, speckit, and caveman into a single ai development workflow. contains no application code — only skills, workflows, and setup documentation.

### spekificity custom layer
the set of skills, workflow documents, and setup guides that spekificity installs locally per-project. distinct from globally-installed speckit — this layer is project-scoped and can be updated independently.

### token efficiency
the property of minimising the number of ai tokens consumed to achieve a given outcome. spekificity improves token efficiency through graph-based context loading (replacing full file scans) and caveman-compressed interactions.

### workflow
a documented sequence of skill invocations with defined ordering, inputs, outputs, and branching conditions. workflows describe how skills compose to complete a multi-step task (e.g., the full speckit feature lifecycle).
