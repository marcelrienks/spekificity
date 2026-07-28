---
name: spek-blind-review
description: 'Run a context-free quality pass by anonymizing AI attribution before reviewing.'
---

# /spek.blind-review

Run a context-free quality pass by anonymizing AI attribution before reviewing.

## Prerequisites

- Implementation complete; all tasks done
- Test suite passes (run tests before invoking this skill)
- Linter installed and configured (pylint, flake8, eslint, or equivalent)
- Test runner available (pytest, pytest-cov, jest, equivalent)

## Steps

0. **Caveman activation check**: Ensure Caveman compression is active. If not active in this session, run `/caveman full` to enable ~75% token reduction (valuable for verbose lint/review output).

0.5. **Pre-check**: Validate test runner available (e.g., `pytest`, `jest`, etc. — check in PATH). Validate linter installed (e.g., `pylint`, `flake8`, `eslint` — check in PATH). Validate linter config file exists (e.g., `.pylintrc`, `.flake8`, `.eslintrc`). If any tool missing, halt with error. Run test suite. If any tests fail, report failures and stop (do not proceed to linting). Exit with error status. Capture test output to `.spek/memory/last-test-output.log`. Caveman compression active reduces output size by ~75%.
1. Anonymize source files in working memory only: strip comments containing vendor or agent names (`claude`, `copilot`, `chatgpt`, `openai`, `anthropic`, `cursor`); replace service class names with generic aliases (e.g. AuthService → ServiceA, UserService → ServiceB); NEVER modify original files — all anonymization is in working memory only; originals remain unchanged.
2. Run configured linter on anonymized copy; capture all output; classify each finding as CRITICAL (security issues, unhandled errors, undefined behavior), WARNING (code quality, dead code, missing validation), or INFO (style, minor naming).
3. Check function complexity: flag functions exceeding 20 lines or cyclomatic complexity greater than 10 as WARNING with file:line and refactoring hint.
4. Report all findings with file:line references and remediation hints; print summary line: `CRITICAL: N | WARNING: N | INFO: N`; write full report to `.spek/memory/blind-review-YYYY-MM-DD.md`.

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
