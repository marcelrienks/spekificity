# docs/validation.md

## purpose

validation methodology for the two quantitative success criteria defined in the spekificity platform spec.

---

## sc-002: vault graph eliminates redundant context queries

**target**: ≥40% reduction in token usage for cross-cutting "where is x" queries when vault graph is available vs. unavailable.

### methodology

token counts are obtained via ai provider token counting. for github copilot: use the copilot token counter in the vs code extension or count programmatically. for claude code: use the context window usage displayed in the session.

**procedure**:

1. select 5 representative cross-cutting queries from the table below.
2. for each query, run two ai sessions:
   - **without vault** (`vault/graph/index.md` absent or empty): query the ai directly with no vault context.
   - **with vault** (`/context-load` run first): same query, with vault primed.
3. record the input token count for each session in the log table.
4. compute reduction percentage: `(tokens_without - tokens_with) / tokens_without * 100`

**reference queries**:

| # | query |
|---|-------|
| 1 | "which files define the entity model?" |
| 2 | "where is authentication handled?" |
| 3 | "list all api endpoints" |
| 4 | "what decisions were made about the database schema?" |
| 5 | "which files will be affected if i change the user entity?" |

**log table** (fill in during validation):

| query | tokens without vault | tokens with vault | reduction (%) | pass (≥40%)? |
|-------|---------------------|-------------------|---------------|--------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| **average** | | | | |

**validation result**: if the average reduction is ≥40%, sc-002 passes.

---

## sc-003: caveman mode reduces ai response verbosity

**target**: ≥60% reduction in character count for ai explanatory responses when caveman mode is active vs. inactive.

### methodology

character counts are measured on ai responses (not user prompts). use a word count / character count tool or simply count characters in the response text.

**procedure**:

1. select 3 representative ai explanation requests from the table below.
2. for each request, run two ai sessions:
   - **without caveman** (no `/caveman` invocation): ask the question normally.
   - **with caveman** (`/caveman` activated): ask the same question.
3. record the character count of the ai response in the log table.
4. compute reduction percentage: `(chars_without - chars_with) / chars_without * 100`

**reference requests**:

| # | request |
|---|---------|
| 1 | "explain what the vault/context/decisions.md file is used for" |
| 2 | "walk me through what /speckit-enrich-implement does" |
| 3 | "describe the spekificity decorator pattern" |

**log table** (fill in during validation):

| request | chars without caveman | chars with caveman | reduction (%) | pass (≥60%)? |
|---------|-----------------------|--------------------|---------------|--------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| **average** | | | | |

**validation result**: if the average reduction is ≥60%, sc-003 passes.

---

## how to log validation results

when you have completed a validation run, update this file with results in the log tables. commit the updated file to make the validation record durable.

```bash
git add docs/validation.md
git commit -m "docs(validation): record sc-002/sc-003 validation results"
```
