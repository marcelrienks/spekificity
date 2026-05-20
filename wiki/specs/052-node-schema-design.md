# Spec: Node Schema Design

**Status:** ATOMIC SPECIFICATION (2026-05-18)   | **Version:** 1.0.0-alpha.1 (2026-05-20)
**Concern:** JSON schema for code and documentation nodes in the knowledge graph  
**Extracted from:** extracted spec Questions 1 & 4  
**Used by:** obsidian-graph-export, graph-merge-integration, graph-storage-structure  

---

## Overview

**Problem:** Code nodes (from graphify) and documentation nodes (from Obsidian export) need a unified schema so they can be merged, queried, and indexed together.

**Solution:** Define explicit JSON schemas for code nodes, doc nodes (heading-level and file-level), and skill nodes. All stored in common JSONL format.

**Outcome:** Unified vault/graph/nodes.jsonl with queryable nodes of multiple types, enabling agent to discover code symbols, architectural decisions, patterns, and lessons in one query.

---

## Node Types Overview

| Type | Source | Granularity | Frequency | Count (Est.) |
|------|--------|-------------|-----------|--------------|
| **code** | graphify | Symbol (function/class/var) | Per file | 1000-5000 |
| **doc** | Obsidian | Heading or file | Per feature | 100-500 |
| **skill** | Obsidian/SpecKit | File | Per workflow | 20-50 |

---

## Code Node Schema

**Source:** Graphify AST analysis  
**Granularity:** Symbol-level (function, class, interface, variable, const)  
**Example ID:** `src/prepare/prepare.ts:Prepare` (file:symbol)

```typescript
interface CodeNode {
  type: "code";
  
  // Identity
  id: string;                          // e.g., "src/prepare/prepare.ts:Prepare"
  file: string;                        // relative path to source
  symbol: string;                      // function/class/const name
  
  // Classification
  symbolType: "function" | "class" | "interface" | "type" | "variable" | "const" | "enum";
  language: string;                    // "typescript" | "python" | "javascript" | etc.
  
  // Documentation
  description: string;                 // JSDoc or leading comment
  signature?: string;                  // e.g., "prepare(feature: string): void"
  
  // Location
  lineRange: [start: number, end: number];  // Line numbers in file
  
  // Dependencies
  imports: string[];                   // e.g., ["@module/foo", "./helper"]
  exports: string[];                   // Symbols exported from this node
  
  // Graph Relationships
  calls: string[];                     // Code nodes this function calls
  calledBy: string[];                  // Code nodes that call this (computed)
  usedBy: string[];                    // Code nodes that use this variable/type
  uses: string[];                      // Types/classes this depends on
  
  // Metadata
  tags: string[];                      // Implicit: ["code", "source", language]
  references: string[];                // Links to docs or other code
  referencedBy: string[];              // Reverse references (computed)
  
  // Index Metadata
  indexed_at: string;                  // ISO timestamp (2026-05-18T15:00:00Z)
  hash: string;                        // SHA256 of source code for change detection
}
```

### Code Node Example

```json
{
  "type": "code",
  "id": "src/skills/spek-prepare/prepare.ts:PrepareSkill",
  "file": "src/skills/spek-prepare/prepare.ts",
  "symbol": "PrepareSkill",
  "symbolType": "class",
  "language": "typescript",
  "description": "Prepares workspace for feature work. Verifies git state, loads context, checks graph freshness.",
  "signature": "class PrepareSkill { prepare(featureName: string): Promise<void> }",
  "lineRange": [10, 150],
  "imports": ["./context-loader", "git", "../vault/vault-reader"],
  "exports": ["PrepareSkill"],
  "calls": ["context_loader.load", "vault_reader.read", "git.status"],
  "calledBy": [],
  "usedBy": ["src/cli/automate.ts:runFeature"],
  "uses": ["ContextLoader", "VaultReader"],
  "tags": ["code", "source", "typescript", "skill", "workflow"],
  "references": ["vault/decision.md#git-workflow", ".github/agents/skills/spek-prepare/SKILL.md"],
  "referencedBy": ["src/cli/automate.ts", "tests/prepare.test.ts"],
  "indexed_at": "2026-05-18T15:00:00Z",
  "hash": "a1b2c3d4e5f6..."
}
```

## Success Criteria

- ✅ Code node schema captures all symbol metadata (complete + queryable)
- ✅ Doc node schema captures heading-level structure (file + heading + level)
- ✅ Skill node schema captures workflow information (command + purpose + tags)
- ✅ Graph relationships captured (calls, calledBy, usedBy, uses, references, referencedBy)
- ✅ All nodes queryable via unified interface (jq + grep on nodes.jsonl)
- ✅ Schema extensible (new fields don't break existing queries)
- ✅ Type safety enforced (TypeScript interfaces + validation)

---

## Implementation Checklist

- [ ] Define code node schema (TypeScript types)
- [ ] Define doc node schema (TypeScript types)
- [ ] Define skill node schema (TypeScript types)
- [ ] Implement code node generation (from graphify output)
- [ ] Implement doc node generation (from Obsidian export)
- [ ] Implement skill node generation (from SKILL.md parsing)
- [ ] Implement node validation (schema conformance checks)
- [ ] Add tests (roundtrip: generate → validate → query)

---

## References

**Related Specs:**
- [spek-map-command.md](spek-map-command.md) — Graph generation command
- [graph-storage-structure.md](graph-storage-structure.md) — Storage format (nodes.jsonl)
- [obsidian-graph-export.md](obsidian-graph-export.md) — Doc node extraction
- [graph-query-patterns.md](graph-query-patterns.md) — Node querying strategies
}
```

---

## Documentation Node Schema (Heading-Level)

**Source:** Obsidian export (cache.json or dataview)  
**Granularity:** Heading level (h1-h6)  
**Example ID:** `vault/decision.md#api-versioning-strategy` (file#heading-id)

```typescript
interface DocNodeHeading {
  type: "doc";
  
  // Identity
  id: string;                          // e.g., "vault/decision.md#api-versioning-strategy"
  file: string;                        // e.g., "vault/decision.md"
  heading: string;                     // "API Versioning Strategy"
  level: 1 | 2 | 3 | 4 | 5 | 6;        // h1, h2, ... h6
  
  // Classification
  docType: "decision" | "spec" | "pattern" | "lesson" | "guide" | "skill" | "intention";
  status: "active" | "archived" | "draft";
  version?: string;                    // Optional semver (from frontmatter)
  
  // Documentation
  description: string;                 // First paragraph or custom summary
  
  // Hierarchy
  parent: string | null;               // Parent heading id (e.g., "vault/decision.md" for child headings)
  children: string[];                  // Child heading IDs (computed)
  
  // Metadata
  tags: string[];                      // From frontmatter + implicit from folder
  affects?: string[];                  // Features/components this decision affects
  relatedDecisions?: string[];         // Link to related decisions
  
  // Graph Relationships
  references: string[];                // Docs or code this references
  referencedBy: string[];              // Reverse references (computed)
  
  // Index Metadata
  indexed_at: string;                  // ISO timestamp
  hash: string;                        // SHA256 for change detection
}
```

### Doc Node Example (Heading-Level)

```json
{
  "type": "doc",
  "id": "vault/decision.md#api-versioning-strategy",
  "file": "vault/decision.md",
  "heading": "API Versioning Strategy",
  "level": 2,
  "docType": "decision",
  "status": "active",
  "version": "1.0",
  "description": "Decision to use semantic versioning for API endpoints, with deprecation warnings for N versions before removal.",
  "parent": "vault/decision.md",
  "children": [],
  "tags": ["api", "versioning", "architectural"],
  "affects": ["spec-003-api-redesign", "spec-002-client-sdk"],
  "relatedDecisions": ["vault/decision.md#backwards-compatibility"],
  "references": ["vault/patterns.md#deprecation-pattern", "specs/00api-redesign.md"],
  "referencedBy": ["specs/00api-redesign.md", "src/api/versioning.ts"],
  "indexed_at": "2026-05-18T15:00:00Z",
  "hash": "b2c3d4e5f6g7..."
}
```

---

## Documentation Node Schema (File-Level)

**Source:** Obsidian export  
**Granularity:** Entire file  
**Example ID:** `vault/intention.md` or `skills/spek-prepare/SKILL.md`

```typescript
interface DocNodeFile {
  type: "doc";
  
  // Identity
  id: string;                          // e.g., "vault/intention.md"
  file: string;                        // Same as id for file-level nodes
  level: "file";                       // Literal "file" (not 1-6 like heading-level)
  
  // Classification
  docType: "decision" | "spec" | "pattern" | "lesson" | "guide" | "skill" | "intention";
  status: "active" | "archived" | "draft";
  version?: string;
  
  // Documentation
  title: string;                       // First h1 or filename
  description: string;                 // Summary (first paragraph)
  
  // Metadata
  tags: string[];
  affects?: string[];                  // Features/components affected
  
  // Graph Relationships
  references: string[];                // Other docs or code referenced
  referencedBy: string[];              // Reverse references (computed)
  
  // Index Metadata
  indexed_at: string;
  hash: string;
}
```

### Doc Node Example (File-Level)

```json
{
  "type": "doc",
  "id": "vault/intention.md",
  "file": "vault/intention.md",
  "level": "file",
  "docType": "intention",
  "status": "active",
  "title": "Spekificity: Project Intention",
  "description": "Project vision: agentic consolidation platform solving four foundational LLM agent problems via best-in-class tool orchestration.",
  "tags": ["vision", "architecture", "project"],
  "references": ["vault/decision.md", "wiki/architecture.md"],
  "referencedBy": ["README.md", "wiki/todo.md"],
  "indexed_at": "2026-05-18T15:00:00Z",
  "hash": "c3d4e5f6g7h8..."
}
```

---

## Skill Node Schema

**Source:** Obsidian export (special case of doc file-level)  
**Granularity:** File  
**Example ID:** `skills/spek-prepare/SKILL.md`

```typescript
interface SkillNode {
  type: "skill";              // Distinct type from "doc"
  
  // Identity
  id: string;                 // e.g., "skills/spek-prepare/SKILL.md"
  file: string;               // Same as id
  
  // Skill-specific
  command: string;            // e.g., "spek.prepare"
  purpose: string;            // What the skill does
  description: string;        // Full description from SKILL.md
  
  // Inputs/Outputs (optional, if documented)
  inputs?: string[];          // Expected input types
  outputs?: string[];         // Output types
  
  // Metadata
  tags: string[];             // e.g., ["workflow", "setup", "skill"]
  
  // Graph Relationships
  references: string[];       // Other skills or docs this calls
  referencedBy: string[];     // Reverse references
  
  // Index Metadata
  indexed_at: string;
  hash: string;
}
```

### Skill Node Example

```json
{
  "type": "skill",
  "id": "skills/spek-prepare/SKILL.md",
  "file": "skills/spek-prepare/SKILL.md",
  "command": "spek.prepare",
  "purpose": "Prime agent and environment for feature work",
  "description": "Verifies git state, loads context, checks code graph freshness, activates caveman mode.",
  "inputs": ["feature_name (optional)", "skip_context (bool)", "force_graph_refresh (bool)"],
  "outputs": ["feature_state (current-feature.md)", "readiness_report (string)"],
  "tags": ["workflow", "setup", "skill", "spekificity"],
  "references": ["skills/spek-context/SKILL.md", "skills/spek-map/SKILL.md"],
  "referencedBy": ["skills/spek-plan/SKILL.md"],
  "indexed_at": "2026-05-18T15:00:00Z",
  "hash": "d4e5f6g7h8i9..."
}
```

---

## Common Fields (All Node Types)

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `type` | enum | ✓ | "code" \| "doc" \| "skill" |
| `id` | string | ✓ | Unique identifier (file:symbol or file#heading) |
| `file` | string | ✓ | Relative path to source file |
| `description` | string | ✓ | Human-readable summary |
| `tags` | string[] | ✓ | Searchable tags (implicit + explicit) |
| `references` | string[] | ✓ | Links to other nodes (outbound) |
| `referencedBy` | string[] | ✓ | Reverse links (inbound, computed) |
| `indexed_at` | string | ✓ | ISO timestamp of indexing |
| `hash` | string | ✓ | SHA256 for change detection |
| `status` | enum | — | "active" \| "archived" \| "draft" (docs only) |
| `version` | string | — | Semver or free-form version (optional) |

---

## Implicit Tags

**For all nodes:**
- `type` value: "code", "doc", "skill"
- Folder context: "src", "vault", "skill", "spec", etc.

**For code nodes:**
- Language: "typescript", "python", "javascript", etc.
- Symbol type: "function", "class", "interface", "variable", etc.

**For doc nodes:**
- From frontmatter: user-specified tags
- From folder: "decision", "pattern", "lesson", "guide", "spec", etc.
- From status: "active", "archived", "draft"

**Example implicit tags for `vault/decision.md#api-versioning`:**
```
["decision", "vault", "active", "architectural", "api"]  // explicit + implicit
```

---

## Node ID Convention

### Code Nodes: `file:symbol`

```
src/prepare/prepare.ts:PrepareSkill
src/cli/automate.ts:runFeature
utils/graph-reader.ts:readNodes
```

**Rationale:** Unique within file; symbol may appear in multiple files (disambiguated by file path)

**Edge case handling:**
- Nested classes: `src/api/controller.ts:ApiController.handleRequest` (dot notation)
- Exported types: `src/types/index.ts:FeatureConfig` (file where exported)
- Const exports: `src/config/vault.ts:VAULT_PATHS` (uppercase for constants)

### Doc Nodes (Heading): `file#heading-id`

```
wiki/vault/decision.md#api-versioning-strategy
wiki/vault/patterns.md#caching-pattern
specs/00api-redesign.md#implementation-approach
```

**Rationale:** Markdown heading IDs (lowercase, hyphens, no special chars)

**Heading ID conversion:**
- Input: `API Versioning Strategy` → ID: `api-versioning-strategy`
- Input: `How to Cache Data (2026)` → ID: `how-to-cache-data-2026`
- Input: `Why? & What's Next` → ID: `why--whats-next`

### Doc Nodes (File): `file` (no `#`)

```
vault/intention.md
vault/lessons/2026-05-18-00feature-name.md
skills/spek-prepare/SKILL.md
```

**Rationale:** File-level nodes use plain file path (no anchor)

---

## Query Patterns

### Find all decisions
```bash
grep '"type":"doc"' vault/graph/nodes.jsonl | grep '"docType":"decision"'
```

### Find all active decisions
```bash
grep '"type":"doc"' vault/graph/nodes.jsonl | grep '"docType":"decision"' | grep '"status":"active"'
```

### Find nodes tagged "api"
```bash
grep '"tags":.*"api"' vault/graph/nodes.jsonl
```

### Find all code nodes that reference a specific doc
```bash
grep '"vault/decision.md"' vault/graph/nodes.jsonl | grep '"type":"code"'
```

### Find all backreferences to a node
```bash
jq -r '.referencedBy[]' <<< '{"referencedBy":["src/api/v1.ts","tests/api.test.ts"]}'
```

---

## Validation Rules

**For all nodes:**
- [ ] `id` is unique across entire graph
- [ ] `file` exists in workspace
- [ ] `type` is one of: code, doc, skill
- [ ] `description` is non-empty
- [ ] `tags` is array of strings
- [ ] `indexed_at` is valid ISO timestamp
- [ ] `hash` is valid SHA256 hex string

**For code nodes:**
- [ ] `symbol` matches actual symbol in `file`
- [ ] `symbolType` is valid TypeScript/Python symbol type
- [ ] `language` matches file extension or is explicitly set

**For doc nodes:**
- [ ] `file` is markdown (.md)
- [ ] `docType` matches frontmatter `type` or inferred from folder
- [ ] `status` is one of: active, archived, draft
- [ ] If `level` != "file", then `heading` must match actual heading in file at line range

**For computed fields:**
- [ ] `referencedBy` mirrors `references` (bidirectional consistency)
- [ ] `children` mirrors `parent` (tree consistency)
- [ ] `calledBy` mirrors `calls` (for code nodes)

---

## Storage Format (JSONL)

**One node per line, no pretty-printing:**

```jsonl
{"type":"code","id":"src/prepare/prepare.ts:Prepare","file":"src/prepare/prepare.ts","symbol":"Prepare","symbolType":"class",...}
{"type":"doc","id":"vault/decision.md#api-versioning-strategy","file":"vault/decision.md","heading":"API Versioning Strategy",...}
{"type":"skill","id":"skills/spek-prepare/SKILL.md","file":"skills/spek-prepare/SKILL.md","command":"spek.prepare",...}
```

**Rationale:** Streaming-friendly format (read/write one node at a time, no full JSON parse)

---

## Success Criteria

- [x] Code node schema captures symbol identity + relationships + metadata
- [x] Doc node schemas (heading and file) capture document structure + references
- [x] Skill nodes are specialized doc nodes (not generic doc)
- [x] Node ID conventions are consistent and unambiguous
- [x] Implicit tags are documented (language, type, status, folder)
- [x] Common fields are shared across all node types
- [x] Validation rules are clear (what makes a valid node)
- [x] Query patterns shown (how to find nodes of interest)
- [x] JSONL format is space-efficient (no pretty-printing)

---

## References

- **Used by:** obsidian-graph-export, graph-merge-integration, graph-storage-structure
- **Related:** GraphQL schema design best practices, Obsidian graph API
- **Implementation:** Python script to validate nodes against this schema
