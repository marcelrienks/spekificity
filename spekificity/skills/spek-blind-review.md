# /spek.blind-review

Run a context-free quality pass by anonymizing AI attribution before reviewing.

## Prerequisites

- Implementation complete; all tasks done
- Test suite passes (run tests before invoking this skill)
- Linter installed and configured (pylint, flake8, eslint, or equivalent)

## Steps

1. Anonymize source files in working memory only: strip comments containing vendor or agent names (`claude`, `copilot`, `chatgpt`, `openai`, `anthropic`, `cursor`); replace service class names with generic aliases (e.g. AuthService → ServiceA, UserService → ServiceB); NEVER modify original files — all anonymization is in working memory only; originals remain unchanged.
2. Run configured linter on anonymized copy; capture all output; classify each finding as CRITICAL (security issues, unhandled errors, undefined behavior), WARNING (code quality, dead code, missing validation), or INFO (style, minor naming).
3. Confirm all tests pass via `pytest` or configured test runner; report any failures as CRITICAL with file:line reference.
4. Check function complexity: flag functions exceeding 20 lines or cyclomatic complexity greater than 10 as WARNING with file:line and refactoring hint.
5. Report all findings with file:line references and remediation hints; print summary line: `CRITICAL: N | WARNING: N | INFO: N`; write full report to `.spek/memory/blind-review-YYYY-MM-DD.md`.

## Output

- Anonymized review report with severity-tagged findings (CRITICAL / WARNING / INFO)
- Per-finding remediation hints (what to fix and why)
- Summary count line: `CRITICAL: N | WARNING: N | INFO: N`
- Full report written to `.spek/memory/blind-review-YYYY-MM-DD.md`

## Exit Criteria

- All CRITICAL findings reviewed (each either fixed or explicitly accepted with written rationale)
- Full findings report written to `.spek/memory/`
- Original source files confirmed unchanged (no edits to non-memory paths)
- Summary count printed to output
