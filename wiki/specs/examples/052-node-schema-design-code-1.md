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
