# Examples for 121-cli-orchestration

Consolidated examples from `wiki/specs/121-cli-orchestration.md`.

## Example Exit Sequences
- `spek prepare` → Exit 0 → User runs `spek specify` → Exit 0 → Continue
- `spek prepare` → Exit 3 (git dirty) → User runs `git add .` → User runs `spek prepare` → Exit 0
- `spek specify` → Exit 1 (speckit error) → Run `spek specify` again (retry) → Exit 0

## Example Workflow Resume
- `/spek.prepare` → specify → plan → (pause) → prepare --skip-context → plan → tasks
