# /spek.prepare

Initialize third-party tools and load context before feature development.

## Sub-steps

1. **lat.md Code Index**: Run `lat init` to build or refresh the code index (symbols, definitions, call graphs). Output stored in `.spek/lat/`.
2. **lat.md Doc Index**: Run `lat init --docs` to build or refresh the documentation index (wiki, vault, markdown). Separate from code index. Output stored in `.spek/lat/`.
3. **Vault Storage**: Store both indexes in `.spek/vault/` for persistent context.
4. **Context Load**: Load vault decisions (`decisions.md`), patterns (`patterns.md`), and prior lessons from `.spek/vault/lessons/` into agent session.
5. **Constitution Check**: Verify `.specify/memory/constitution.md` exists. If missing, invoke `/speckit-constitution` to create it interactively.

## Exit Criteria

- lat.md code index initialized and current in `.spek/lat/`
- lat.md doc index initialized and current in `.spek/lat/`
- Vault context (decisions, patterns, lessons) loaded into session
- Constitution present at `.specify/memory/constitution.md`
