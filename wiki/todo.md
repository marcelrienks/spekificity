todo: lat.md
context:
The project debates tool choices and workflows for spec-driven AI development. Persistent project memory is stored as Markdown (Obsidian-style vault). We also rely on an indexing tool to make source code and documentation queryable to agents and to reduce token usage during context injection.

action:
Use `lat.md` as the canonical indexing tool across the repo. Ensure specs and wiki docs reference `lat.md` for indexing source code and project documentation and integrate it into Spekificity workflows (prepare, plan, map, conclude).

justification:
`lat.md` is chosen because it is Markdown-native and designed to index and interlink Markdown documentation and project source artifacts. Using `lat.md` lets us build an intentional, navigable knowledge layer from our specs and wiki before and during implementation, and provides agents with clear, document-first context when generating or modifying code.

notes:
-- Update configuration references (tool name in `.spek/config.yaml`) to `lat.md`.
- Ensure all workflows (`/spek.prepare`, `/spek.map`, `/spek.plan`, `/spek.conclude`) describe calling `lat.md` for indexing and queries.
