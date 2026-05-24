# C.3.3 3-Layer Query Rule: Documentation & Enforcement



**Priority:** RECOMMENDED (Phase 1)  
**Effort:** moderate (team-defined)  
**Adoption Source:** B.9 (claude-code-memory-setup, cited as motivation for large token savings)

---


## Purpose

Document and enforce the **3-Layer Query Rule** — a token-efficient context loading strategy that:
1. Queries the **code graph first** (indexed, cached, fast)
2. Falls back to **vault** (searchable, compiled summaries)
3. Only reads **raw code files** when layers 1-2 insufficient

**Goal:** Reduce token usage materially when context loading is done correctly, preventing expensive re-reads of code files.

**Reference Motivation:** external examples report large savings in real-world usage; exact results should be treated as directional unless validated locally.

---


## Scope & Relationships

**What this spec covers:**
- 3-layer query model definition
- When to query each layer
- Example queries for each layer
- Token cost breakdown
- Integration into `/spek.context` skill
- Documentation in copilot-instructions.md
- Enforcement rules

**What this spec does NOT cover:**
- Graph query syntax (see B.11 lat.md Setup)
- Vault structure (see B.8.2 Persistent Memories)
- Code reading strategies (assume needed only in Layer 3)

---


## Success Criteria

- ✅ Layer 1 (code graph) queries return results with low latency and minimal overhead
- ✅ Layer 2 (vault) queries return results with modest latency once architecture context is loaded
- ✅ Layer 3 (code files) only accessed when Layers 1-2 are insufficient (token savings observable)
- ✅ Token cost breakdown documented per layer (qualitative estimates recorded)
- ✅ Integration points in `/spek.context` and `/spek.conclude` follow 3-layer rule
- ✅ Documentation in copilot-instructions.md clearly lists all rules
- ✅ Enforcement rules prevent unnecessary code file reads (fallback only)
- ## Related Specs
- ## 3-Layer Query Model
- ### Layer 1: Code Graph (low token cost)
- **What's in Layer 1:**
- **When to Query Layer 1:**
- **Query Patterns:** Derived from successful context loading patterns in Obsidian + lat.md workflows
- ```
- Layer 1 Query: "Who calls the authenticate() function?"
- → Response: Code graph shows callers
- → Cost: low (qualitative)
- Layer 1 Query: "What does the UserService depend on?"
- → Response: Code graph shows dependencies
- Layer 1 Query: "What changed in the auth module in the last commit?"
- → Response: Code graph delta (before/after)
- **Cost Breakdown (Layer 1):**
- Symbol definitions: low
- Relationships: low
- Type info: low
- Deltas/changes: low
- **Total per query: low token cost (qualitative)**
- ### Layer 2: Vault (moderate token cost)
- **What's in Layer 2:**
- Architectural decisions (rationale, alternatives, consequences)
- Design patterns (when to use, examples, alternatives)
- Lessons learned (what worked, what didn't)
- Integration patterns (how components work together)
- Known issues / workarounds
- **When to Query Layer 2:**
- Need to understand architectural rationale
- Need to know if pattern was tried before
- Need to understand constraints/tradeoffs
- Need prior lessons from similar work
- Need to understand integration between modules
- **Example Queries:**
- Layer 2 Query: "Why did we choose dependency injection?"
- → Response: wiki/vault/decision-use-di.md
- → Rationale, alternatives considered, consequences
- → Cost: moderate (qualitative)
- Layer 2 Query: "What patterns work for state management?"
- → Response: wiki/vault/patterns/state-management-*.md
- → Multiple patterns, when to use each
- Layer 2 Query: "What did we learn from the auth feature?"
- → Response: wiki/vault/lessons/lessons-from-auth-feature.md
- → What worked, what failed, metrics
- **Cost Breakdown (Layer 2):**
- Single decision: moderate
- Pattern search (multiple): moderate
- Lessons document: moderate
- **Total per query: moderate token cost (qualitative)**
- ### Layer 3: Raw Code Files (high token cost)
- **What's in Layer 3:**
- Full source code (implementation details)
- Comments (inline documentation)
- Test cases (usage examples, edge cases)
- Error messages (debugging info)
- **When to Query Layer 3:**
- Need to understand specific implementation
- Need to debug why code behaves this way
- Need to understand all edge cases
- Need to review error handling
- Layer 1 & 2 insufficient
- **Cost of Layer 3:**
- Small targeted reads: moderate to high token cost (qualitative)
- Large file reads or multi-file scans: high token cost (qualitative)
- **WARNING:** Layer 3 is expensive! Only use when necessary.
- **Example Queries (avoid these):**
- ❌ BAD: "Show me the authenticate() function"
- → Response: Read entire authentication.js file
- → Cost: high (entire file read)
- → Should use Layer 1 first: code graph shows function definition
- ❌ BAD: "What's in the UserService class?"
- → Response: Read entire service file
- → Cost: high
- → Should use Layer 1: code graph shows all methods + callers
- ✅ GOOD: "Show me the error handling in retry logic"
- → Response: Read only retry.js (targeted read)
- → Cost: moderate (specific file)
- → Only after Layer 1-2 indicates likely location
- ## Notes on Resource Use
- Query: "How does authentication work in this codebase?"
- Bad Approach (Layer 3 only): reading multiple full files results in very high resource use and should be avoided for routine queries.
- Good Approach (3-Layer Rule):
- Query Layer 1 (code graph) to locate symbols and callers (low cost)
- Query Layer 2 (vault) for decisions and patterns (moderate cost)
- Only read specific files if still necessary (targeted, higher cost)
- Teams should avoid embedding fixed numeric budgets in public docs; configure per-project limits in configuration files and use qualitative guidance in documentation.
- ## Integration: /spek.context Skill
- ### Current Implementation (B.8.2)
- /spek.context loads context by:
- Read vault decisions
- Read vault patterns
- Read recent lessons
- Query code graph
- Summarize + compress
- Write to vault/session/context-loaded.md
- ### Enhanced with 3-Layer Rule (C.3.3)
- /spek.context loads context with enforced layer prioritization:
- [LAYER 1] Query code graph
- Recent changes in codebase
- Key symbols + dependencies
- Impact analysis (who calls what)
- Cost: low (qualitative)
- [LAYER 2] Query vault
- Active decisions (last updated)
- Relevant patterns (by domain)
- Recent lessons (last 5 features)
- Cost: moderate (qualitative)
- [Conditional] Read code only if necessary
- Specific file if decision/pattern references code
- Only if Layer 1-2 insufficient
- Cost: high (avoid when possible)
- Synthesize + Compress (caveman mode)
- Summarize all layers
- Remove redundancy
- Compress to caveman format
- Write session context
- Store at vault/session/context-loaded.md
- Timestamped
- Include which layers were queried
- Total: lower than full Layer 3 reads when rule applied; actual resource use depends on scope and team configuration.
- ### Implementation Pseudocode
- ```python
- def load_context_with_3layer_rule():
- """Load session context using 3-layer query rule"""
- context = {}
- # LAYER 1: Code Graph (low cost)
- print("Loading Layer 1: Code Graph...")
- graph = query_code_graph(
- include_recent_changes=True,
- include_key_symbols=True,
- include_dependencies=True
- )
- context['layer1_graph'] = graph
- log_tokens("layer1", label="low")
- # LAYER 2: Vault (moderate cost)
- print("Loading Layer 2: Vault...")
- vault = load_vault(
- decisions=get_active_decisions(),
- patterns=get_relevant_patterns(),
- lessons=get_recent_lessons(limit=5)
- context['layer2_vault'] = vault
- log_tokens("layer2", label="moderate")
- # LAYER 3: Code Files (conditional, high cost)
- if layer1_layer2_insufficient(context):
- print("Layer 1-2 insufficient; reading raw code...")
- # Only read specific files that were referenced in Layer 2
- code = read_referenced_code_files(context['layer2_vault'])
- context['layer3_code'] = code
- log_tokens("layer3", label="high")
- else:
- print("Layer 1-2 sufficient; skipping Layer 3")
- context['layer3_code'] = None
- log_tokens("layer3", label="none")
- # Synthesize all layers
- print("Synthesizing context...")
- synthesized = synthesize_context(context)
- # Compress
- print("Compressing (caveman mode)...")
- compressed = compress_caveman(synthesized)
- # Write session memory
- write_session_context(compressed)
- log_tokens("total", label="qualitative")
- return compressed
- ### Logging & Transparency
- When `/spek.context` completes, report:
- ✓ Context Loaded (session recorded; timestamps omitted)
- Layer 1 (Code Graph):
- • Recent changes: auth module (details recorded)
- • Key symbols: authenticate(), UserService, TokenManager
- • Dependencies: inbound/outbound counts recorded
- • Tokens: low (qualitative)
- Layer 2 (Vault):
- • Decisions: active decisions recorded (identifiers listed)
- • Patterns: relevant patterns identified
- • Lessons: recent lessons referenced
- • Tokens: moderate (qualitative)
- Layer 3 (Code Files):
- • Status: Skipped (Layer 1-2 sufficient)
- • Tokens: none (skipped)
- Compression:
- • Original: recorded (omitted)
- • Compressed (caveman): recorded (omitted)
- • Savings: substantial (qualitative)
- Total Context Load: recorded (qualitative)
- Stored at: vault/session/context-loaded.md
- ## Documentation: copilot-instructions.md
- Add this section to copilot-instructions.md for agent visibility:
- ```markdown
- ## Context Navigation: 3-Layer Query Rule
- When gathering context during feature work, follow this priority order:
- ### Layer 1: Query Code Graph (Fast, Indexed)
- Use when you need to understand:
- Code structure (who calls what)
- Dependencies (module relationships)
- Recent changes (git diff)
- Impact analysis (scope of change)
- Example queries:
- "Who calls the authenticate() function?"
- "What does UserService depend on?"
- "What changed in the auth module?"
- Cost: low per query (qualitative)
- ### Layer 2: Query Vault (Searchable, Compiled)
- Architectural rationale (why was this design chosen?)
- Design patterns (when to use, alternatives)
- "Why did we choose dependency injection?"
- "What state management patterns do we use?"
- "What did we learn from the auth feature?"
- Cost: moderate per query (qualitative)
- ### Layer 3: Read Raw Code Files (Expensive)
- Use ONLY when Layers 1-2 are insufficient:
- Need specific implementation details
- Cost: high per query (avoid when possible)
- ## Token Cost Comparison
- ### Query: "How does authentication work in this codebase?"
- **❌ Bad Approach (Layer 3 only):**
- Read multiple full source files to gather implementation details (high token cost).
- **✅ Good Approach (3-Layer Rule):**
- Query Layer 1 (code graph) to locate symbols and callers (low token cost)
- Query Layer 2 (vault) for decisions and patterns (moderate token cost)
- **Overall Savings:**
- Following the 3-layer rule provides substantial token savings compared to naïvely reading full source files; exact savings depend on local workload and should be measured in-context.
- ✓ Layer 1 check: Code graph loaded? Provide summary
- ✓ Layer 2 check: Vault loaded? Provide summary
- ✓ Layer 3 check: If code read, was it necessary? Report why
- ✓ Token tracking: Log tokens for each layer
- ✓ Transparency: Show user which layers were queried
- ## Success Criteria
- ✅ 3-layer query rule documented in copilot-instructions.md
- ✅ `/spek.context` enforces layer prioritization automatically
- ✅ Alerts shown when Layer 3 (code read) is triggered
- ✅ Token usage logged for each layer
- ✅ Session context reports which layers were queried
- ✅ Users see ~20x token savings in practice
- ✅ Team understands when to query each layer
- ✅ No expensive queries without justification
- ## Related Specifications
- **B.11:** lat.md Setup (Layer 1 implementation)
- **B.8.2:** Persistent Memories (Layer 2 implementation)
- **B.8.4:** Post Command (context injection pattern)
- **C.3.3:** This spec (3-layer enforcement)
- ## References
- **Production Source:** https://github.com/lucasrosati/claude-code-memory-setup (external reference for large token-savings patterns)
- **Cost Analysis:** Based on real-world token measurements from session data

