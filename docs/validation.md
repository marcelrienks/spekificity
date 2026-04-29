# docs/VALIDATION.md

## Purpose

Validation methodology for the two quantitative success criteria defined in the Spekificity platform spec.

---

## SC-002: Vault Graph Eliminates Redundant Context Queries

**Target**: ≥40% reduction in token usage for cross-cutting "where is X" queries when vault graph is available vs. unavailable.

### Methodology

Token counts are obtained via AI provider token counting. For GitHub Copilot: use the Copilot token counter in the VS Code extension or count programmatically. For Claude Code: use the context window usage displayed in the session.

**Procedure**:

1. Select 5 representative cross-cutting queries from the table below.
2. For each query, run two AI sessions:
   - **Without vault** (`vault/graph/index.md` absent or empty): Query the AI directly with no vault context.
   - **With vault** (`/context-load` run first): Same query, with vault primed.
3. Record the input token count for each session in the log table.
4. Compute reduction percentage: `(tokens_without - tokens_with) / tokens_without * 100`

**Reference queries**:

| # | Query |
|---|-------|
| 1 | "Which files define the entity model?" |
| 2 | "Where is authentication handled?" |
| 3 | "List all API endpoints" |
| 4 | "What decisions were made about the database schema?" |
| 5 | "Which files will be affected if I change the User entity?" |

**Log table** (fill in during validation):

| Query | Tokens without vault | Tokens with vault | Reduction (%) | Pass (≥40%)? |
|-------|---------------------|-------------------|---------------|--------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| **Average** | | | | |

**Validation result**: If the average reduction is ≥40%, SC-002 PASSES.

---

## SC-003: Caveman Mode Reduces AI Response Verbosity

**Target**: ≥60% reduction in character count for AI explanatory responses when Caveman mode is active vs. inactive.

### Methodology

Character counts are measured on AI responses (not user prompts). Use a word count / character count tool or simply count characters in the response text.

**Procedure**:

1. Select 3 representative AI explanation requests from the table below.
2. For each request, run two AI sessions:
   - **Without Caveman** (no `/caveman` invocation): Ask the question normally.
   - **With Caveman** (`/caveman` activated): Ask the same question.
3. Record the character count of the AI response in the log table.
4. Compute reduction percentage: `(chars_without - chars_with) / chars_without * 100`

**Reference requests**:

| # | Request |
|---|---------|
| 1 | "Explain what the vault/context/decisions.md file is used for" |
| 2 | "Walk me through what /speckit-enrich-implement does" |
| 3 | "Describe the Spekificity decorator pattern" |

**Log table** (fill in during validation):

| Request | Chars without Caveman | Chars with Caveman | Reduction (%) | Pass (≥60%)? |
|---------|-----------------------|--------------------|---------------|--------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| **Average** | | | | |

**Validation result**: If the average reduction is ≥60%, SC-003 PASSES.

---

## How to Log Validation Results

When you have completed a validation run, update this file with results in the log tables. Commit the updated file to make the validation record durable.

```bash
git add docs/VALIDATION.md
git commit -m "docs(validation): record SC-002/SC-003 validation results"
```
