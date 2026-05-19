# SPECIFICATION: spek.automate — SpecKit Workflow Orchestration (C.2.0)

**Status:** ATOMIC SPECIFICATION  
**Type:** Skill — Autonomous SpecKit Workflow Orchestration  
**Version:** 2026-05-19  
**Depends On:** speckit-integration-contract.md, error-handling-and-recovery.md, context-layer.md  
**Related:** cli-orchestration.md (lower-level CLI commands)

---

## Overview

`spek.automate` is a single entry point that autonomously orchestrates the **full SpecKit workflow** without requiring the user to manually invoke individual SpecKit skills.

**Key Design Principle:** `spek.automate` does **not hardcode** which SpecKit skills to call. Instead, it:
1. **Discovers** the currently installed SpecKit version
2. **Queries** the SpecKit registry to determine available skills and recommended workflow
3. **Orchestrates** skills in order, handling user input, remediation, and error recovery
4. **Adapts** automatically to future SpecKit updates (no code changes required)

**Purpose:**
- Enable hands-off feature development using SpecKit
- Surface user decisions at natural points (spec clarifications, plan validations)
- Handle remediation automatically (re-run skills if issues detected)
- Work seamlessly with any SpecKit version (past, present, future)

---

## Architecture

### Layer 1: Initialization
```
spek.automate <feature-description>
├─ Step 1: Load workspace context (via /spek.context)
├─ Step 2: Discover SpecKit version + available skills
├─ Step 3: Query recommended workflow from SpecKit registry
├─ Step 4: Initialize feature state tracking
└─ Ready: Begin skill orchestration
```

### Layer 2: Dynamic Workflow Discovery
```
For each step in SpecKit recommended workflow:
  ├─ Query registry: What is this step?
  ├─ Load: Input requirements (prerequisites, context)
  ├─ Load: Typical failure modes (validation, recovery)
  ├─ Load: Success criteria (what makes step complete)
  └─ Prepare: User prompts if input needed
```

### Layer 3: Skill Execution
```
For each discovered skill in workflow:
  ├─ Pre-execution: Collect inputs
  │   ├─ Surface cached values (offer user to keep or change)
  │   ├─ Prompt for missing inputs
  │   └─ Validate inputs before passing to skill
  ├─ Execute: Call skill via its documented interface
  │   └─ Capture output, errors, execution trace
  ├─ Post-execution: Validate output
  │   ├─ Check success criteria
  │   ├─ Detect common failure modes
  │   └─ Suggest remediation if needed
  └─ Decision: Continue or remediate?
```

### Layer 4: Remediation & Recovery
```
If validation fails:
  ├─ Classify failure: Input error, execution error, output validation error
  ├─ Suggest fix: Re-run with different inputs, manual editing, etc.
  ├─ Offer manual intervention: Edit artifact (spec.md, plan.md, etc.)
  ├─ Re-run validation: Confirm fix worked
  ├─ Continue or abort: Proceed to next step or stop
  └─ Log remediation: Add to error log for future reference
```

### Layer 5: Completion
```
After all skills complete successfully:
  ├─ Generate lessons learned (via /spek.post)
  ├─ Update vault (decisions, patterns)
  ├─ Refresh code graph
  ├─ Archive feature state
  └─ Report completion + next steps
```

---

## Step 1: SpecKit Discovery

### 1.1 Query SpecKit Version

```bash
# Get installed SpecKit version
spek.automate --discover-version
  → Output: speckit version X.Y.Z
  → Query: ~/.speckit/registry/ OR /usr/local/lib/speckit/ OR global npm/pip installation
```

**Implementation:**
- Try multiple locations: local project, user home, global install
- Fallback: `speckit --version` CLI command
- Parse version string to extract major.minor.patch

---

### 1.2 Query SpecKit Registry

```bash
# Get available skills for this SpecKit version
spek.automate --discover-skills
  → Query: ~/.speckit/registry/skills.json OR equivalent
  → Discover: [specify, clarify, plan, analyze, tasks, implement]
  → Return: Structured list with metadata per skill
```

**Registry Query Returns:**
```json
{
  "speckit_version": "2.1.0",
  "available_skills": [
    {
      "name": "specify",
      "version": "2.1.0",
      "input_requirements": ["constitution", "feature_description"],
      "output_files": ["spec.md"],
      "typical_failure_modes": ["invalid_constitution", "missing_feature_description"],
      "success_criteria": ["spec.md_created", "spec.md_well_formed"]
    },
    {
      "name": "clarify",
      "version": "2.1.0",
      "optional": true,
      "input_requirements": ["spec.md"],
      "output_files": ["spec.md"],
      "suggested_when": ["spec_ambiguous", "user_requests_clarification"]
    },
    ...
  ],
  "recommended_workflow": ["specify", "clarify", "plan", "tasks", "analyze", "implement"],
  "optional_steps": ["clarify", "analyze"],
  "remediation_workflow": {
    "if_analyze_fails": ["manual_edit_tasks", "rerun_analyze", "skip_to_implement"],
    "if_implement_fails": ["manual_fix_code", "rerun_implement"]
  }
}
```

---

### 1.3 Workflow Sequencing

**Recommended workflow (from registry):**
```
specify → [clarify (optional)] → plan → tasks → [analyze (optional)] → implement
```

**Adaptive sequencing (based on registry):**
- If `clarify` not available: Skip it
- If `analyze` not available: Skip it (only check output)
- If new skill appears in future: Auto-include it in workflow
- If skill renamed: Use new name, not hardcoded name

---

## Step 2: User Input Collection

### 2.1 Pre-Workflow Prompts

**Before starting orchestration, collect:**

```
Prompt 1: Feature description (required for /specify)
  Input: "Implement user authentication system"
  
Prompt 2: Constitution file location (required for /specify)
  Offer: Auto-detect existing constitution.md OR use default
  Default: Use project constitution if exists
  
Prompt 3: Clarification needed? (offer after /specify)
  Question: "Is spec clear enough to plan? (yes/no/clarify)"
  If clarify: Offer /clarify skill
  If no: Skip to /plan
  
Prompt 4: Remediation preferences (for error handling)
  Question: "If remediation needed, auto-fix when possible? (yes/no)"
  yes: Auto-rerun skills with suggested fixes
  no: Stop and ask before each retry
```

### 2.2 Mid-Workflow Prompts

**As workflow executes, surface prompts from skills:**

```
Example 1: Spec validation question
  From: /specify skill
  Question: "Is authentication scoped to web OR mobile OR both?"
  User input: Required before /plan can start
  Action: Inject into plan phase context
  
Example 2: Analysis issue requiring decision
  From: /analyze skill
  Issue: "Tasks missing error handling for OAuth failure"
  Options: [a) Add tasks manually, b) Regenerate tasks, c) Skip analyze]
  User input: Choose remediation path
  Action: Execute user's choice
```

### 2.3 Input Validation

**Before passing input to SpecKit skill:**
```
- Check: Input file exists (spec.md, plan.md, etc.)
- Check: Input file well-formed (valid markdown, required sections)
- Check: Input values consistent with prior steps
- If validation fails: Offer repair (edit file, regenerate, etc.)
- Log: All input validation results to error log
```

---

## Step 3: Skill Execution

### 3.1 Pre-Execution Setup

```bash
For each skill in workflow:
  1. Load skill metadata from registry
  2. Collect required inputs (spec.md, plan.md, etc.)
  3. Validate inputs exist + are well-formed
  4. Inject Spekificity context (decisions, patterns, code graph)
  5. Set skill-specific environment variables
```

### 3.2 Execution

```bash
# Call SpecKit skill with full context
/speckit.<skill> <args> [--context-file=/memories/session/context-loaded.md]

# Capture output
  ├─ stdout/stderr
  ├─ Output files (spec.md, plan.md, tasks.md, etc.)
  ├─ Execution trace (timing, tokens used, models called)
  └─ Errors/warnings from skill

# Log execution
  └─ Add to /memories/session/execution-trace.md
```

### 3.3 Post-Execution Validation

```bash
For each skill output:
  ├─ Check: Output file created
  ├─ Check: Output file well-formed (valid markdown, required sections)
  ├─ Check: Output consistency with inputs
  ├─ Check: Success criteria met (from registry)
  ├─ Validate: Detected common failure modes (from registry)
  └─ Decide: Success or remediation needed?
```

---

## Step 4: Remediation & Recovery

### 4.1 Failure Classification

```
Failure Type 1: INPUT ERROR
  Cause: Missing required input file, or file not well-formed
  Detection: Pre-execution validation failed
  Recovery: [a] Create missing file, [b] Edit malformed file, [c] Regenerate from prior step
  
Failure Type 2: EXECUTION ERROR
  Cause: Skill crashed, timed out, or returned error
  Detection: Non-zero exit code from skill
  Recovery: [a] Retry with verbose logging, [b] Edit inputs and retry, [c] Skip step (if optional)
  
Failure Type 3: OUTPUT VALIDATION ERROR
  Cause: Output file created but validation failed (missing sections, etc.)
  Detection: Post-execution validation failed
  Recovery: [a] Manual edit to fix output, [b] Regenerate skill output, [c] Skip step (if optional)
  
Failure Type 4: CONSISTENCY ERROR
  Cause: Output contradicts prior steps or architectural decisions
  Detection: Consistency check failed
  Recovery: [a] Clarify decision with user, [b] Manually edit output, [c] Regenerate with different context
```

### 4.2 Remediation Flow

```
If validation fails:
  ├─ Classify failure type (using 4.1)
  ├─ Log failure: Add to error log with full details
  ├─ Offer remediation: Show user what failed + suggest fix
  │   ├─ Option A: Auto-fix (if remediation is obvious)
  │   ├─ Option B: Manual fix (edit artifact, then continue)
  │   ├─ Option C: Regenerate (rerun skill with adjusted context)
  │   └─ Option D: Skip (if step is optional)
  ├─ Wait for user choice (or use preference from --remediation flag)
  ├─ Execute remediation
  ├─ Re-validate: Confirm fix worked
  └─ Decide: Continue or abort?
```

### 4.3 Remediation Examples

**Example 1: Spec too ambiguous**
```
Validation: Spec analysis detects ambiguous language
Error: "Section 'Authentication' lacks specific failure handling requirements"
Offer:
  a) Regenerate spec (rerun /specify with clarification)
  b) Manually edit spec.md (fix ambiguity yourself)
  c) Clarify step (run /clarify skill if available)
User picks: a) Regenerate
Action: Rerun /specify with note "Prior spec had ambiguous language in auth section"
Trace: Added to error log: "Spec regeneration (attempt 1)"
```

**Example 2: Analyze detects missing error handling**
```
Validation: Analyze detects tasks missing error handling for OAuth
Error: "Tasks don't specify recovery from OAuth token expiration"
Offer:
  a) Add tasks manually (you edit tasks.md)
  b) Regenerate tasks (rerun /tasks with focus on OAuth error cases)
  c) Skip analyze, continue to implement (risky, not recommended)
User picks: b) Regenerate
Action: Rerun /tasks with context: "Prior analyze reported missing OAuth error handling"
Trace: Added to error log: "Tasks regeneration (attempt 1, reason: analyze feedback)"
```

**Example 3: Implement fails (code compilation error)**
```
Validation: Output code has syntax error
Error: "Python syntax error on line 42 of auth.py: missing colon in function def"
Offer:
  a) Fix manually (you edit the file, then continue)
  b) Regenerate implementation (rerun /implement with constraint "avoid line 42 pattern")
  c) Stop and debug (abort orchestration, investigate manually)
User picks: a) Fix manually
Action: User fixes file, then continue to next step
Trace: Added to error log: "Manual fix applied to auth.py"
```

---

## Step 5: Optimization: Sub-Agent Strategy

### When to Use Sub-Agents

**Use sub-agent for complex skill orchestration:**
- SpecKit skill is resource-intensive (long-running, high token usage)
- Skill output needs independent validation/review
- Multiple potential remediation paths (needs decision tree)
- Skill has unpredictable failure modes (needs debugging)

**Example: /implement skill might use sub-agent**
```
spek.automate calls: cavecrew-builder sub-agent to handle /implement
  ├─ Sub-agent runs /implement
  ├─ Sub-agent validates output (syntax check, imports resolved, tests pass)
  ├─ Sub-agent proposes remediation if issues detected
  ├─ Sub-agent returns compressed result to main agent
  └─ Main agent continues orchestration
```

**When NOT to use sub-agents:**
- Skill execution is simple (fast, low token usage)
- Output validation is straightforward (file exists, well-formed)
- Remediation is obvious (retry with different input)

**Examples: Simple skills (no sub-agents needed)**
- /specify: Usually straightforward (generate spec from description)
- /plan: Usually straightforward (generate plan from spec)
- /tasks: Usually straightforward (generate tasks from plan)

---

## Step 6: Version Adaptation

### How spek.automate Handles SpecKit Updates

**Scenario 1: New skill added in SpecKit v3.0**
```
Old workflow (v2.1): specify → clarify → plan → tasks → analyze → implement
New workflow (v3.0): specify → clarify → plan → validate → tasks → analyze → implement
                                                    ↑ NEW
Detection:
  1. spek.automate queries registry on startup
  2. Registry returns new workflow with 'validate' step
  3. spek.automate discovers 'validate' is new (not in prior runs)
  4. Offers user: "SpecKit v3.0 includes new 'validate' step. Run it? (yes/no)"
  5. If yes: Includes 'validate' in this run
  6. If no: Skips it (maintains backward compatibility)
```

**Scenario 2: Skill renamed in SpecKit v3.0**
```
Old name: /clarify
New name: /clarify-spec (same functionality, better name)
Detection:
  1. Registry query returns /clarify-spec (not /clarify)
  2. spek.automate uses new name when orchestrating
  3. Old hardcoded calls would break; dynamic discovery prevents this
```

**Scenario 3: Skill removed in SpecKit v3.0**
```
Removed skill: /analyze (integrated into /tasks instead)
Old workflow: specify → plan → tasks → analyze → implement
New workflow: specify → plan → tasks → implement
Detection:
  1. Registry query returns no /analyze skill
  2. spek.automate skips it (not hardcoded to require it)
  3. Workflow adapts automatically; no code change needed
```

**Implementation: Registry Query Mechanism**
```bash
# spek.automate checks registry on every run (or cache with TTL)
REGISTRY_PATH="$SPECKIT_HOME/registry.json"  # or query via API

if registry_modified_recently; then
  workflow=$(query_registry_for_workflow)  # Get latest
else
  workflow=$(use_cached_workflow)  # Cache TTL: 24 hours
fi

# Determine what skills are available
available_skills=$(query_registry_available_skills)

# Filter recommended workflow to only include available skills
active_workflow=$(filter_workflow_by_available_skills)
```

---

## Execution Flow (End-to-End)

```
User: spek.automate "Implement user authentication system"

Step 0: Initialize
  ├─ Load context (/spek.context)
  ├─ Discover SpecKit version (v2.1.0)
  ├─ Query registry: available skills, recommended workflow
  ├─ Initialize feature state tracking
  └─ Ready: Begin orchestration

Step 1: /specify (Required)
  ├─ Pre: Collect inputs (constitution, feature description)
  ├─ Pre: Inject context (decisions, patterns from vault)
  ├─ Exec: /speckit.specify → spec.md
  ├─ Post: Validate spec (well-formed, required sections)
  └─ Success: Continue

Step 2: /clarify (Optional, offered)
  ├─ Prompt: "Spec clear? (yes/no/clarify)"
  ├─ User: "clarify" (wants more clarity)
  ├─ Pre: Load spec.md as input to clarify
  ├─ Exec: /speckit.clarify → spec.md (updated)
  ├─ Post: Validate clarification helped
  └─ Success: Continue

Step 3: /plan (Required)
  ├─ Pre: Collect inputs (spec.md from prior steps)
  ├─ Pre: Inject context (code graph, architectural decisions)
  ├─ Exec: /speckit.plan → plan.md
  ├─ Post: Validate plan (well-formed, complete)
  └─ Success: Continue

Step 4: /tasks (Required)
  ├─ Pre: Collect inputs (spec.md, plan.md)
  ├─ Exec: /speckit.tasks → tasks.md
  ├─ Post: Validate tasks (well-formed, dependency-ordered)
  └─ Success: Continue

Step 5: /analyze (Optional, offered)
  ├─ Prompt: "Run analysis? (yes/no)"
  ├─ User: "yes"
  ├─ Exec: /speckit.analyze → analysis.json
  ├─ Post: Validate analysis
  ├─ Issues detected: "Tasks missing OAuth error handling"
  ├─ Offer: [a] Manual fix, [b] Regenerate tasks
  ├─ User: "Regenerate tasks"
  ├─ Rerun: /speckit.tasks (with analyze feedback as context)
  ├─ Post: Revalidate
  └─ Success: Continue

Step 6: /implement (Required)
  ├─ Pre: Collect inputs (spec.md, plan.md, tasks.md)
  ├─ Pre: Inject context (code graph, patterns)
  ├─ Exec: /speckit.implement → code changes
  ├─ Post: Validate output (syntax, imports, tests pass)
  └─ Success: Continue

Step 7: /spek.post (Spekificity)
  ├─ Extract lessons learned
  ├─ Update vault (decisions, patterns)
  ├─ Refresh code graph
  ├─ Archive feature state
  └─ Report completion

Final Output:
  ✓ Feature implemented
  ✓ Lessons archived
  ✓ Vault updated
  ✓ Ready for next feature
```

---

## CLI Interface

### Command

```bash
spek.automate <feature-description> [options]
```

### Options

```bash
--constitution <path>              # Path to constitution.md (default: auto-detect)
--remediation <auto|manual|ask>    # Remediation strategy (default: ask)
--skip-optional <yes|no>           # Skip optional steps (default: no)
--verbose                          # Verbose logging
--dry-run                          # Preview, don't execute
--max-retries <n>                  # Max remediation attempts per step (default: 3)
```

### Examples

```bash
# Full orchestration with prompts
spek.automate "Implement user authentication system"

# Auto-remediation, skip optional steps
spek.automate "Implement user auth" --remediation=auto --skip-optional=yes

# Dry-run preview
spek.automate "Implement user auth" --dry-run

# Verbose logging (for debugging)
spek.automate "Implement user auth" --verbose
```

---

## Output & Logging

### Feature State File (`/memories/session/orchestration-state.md`)

```markdown
# Orchestration State: user-auth feature

**Feature:** Implement user authentication system  
**Started:** 2026-05-19 10:00:00 UTC  
**Status:** IN PROGRESS  

## Workflow Steps

| Step | Skill | Status | Attempts | Time | Output |
|------|-------|--------|----------|------|--------|
| 1 | /specify | ✓ PASS | 1 | 45s | spec.md (234 lines) |
| 2 | /clarify | ✓ PASS | 1 | 30s | spec.md (updated, 250 lines) |
| 3 | /plan | ✓ PASS | 1 | 60s | plan.md (412 lines) |
| 4 | /tasks | ✓ PASS | 2 | 90s | tasks.md (8 tasks, regenerated due to analyze feedback) |
| 5 | /analyze | ✓ PASS | 1 | 45s | analysis.json (3 issues detected, all resolved) |
| 6 | /implement | ⏳ IN PROGRESS | 1 | — | — |

## Issues & Resolutions

**Issue 1:** Tasks missing OAuth error handling
- Detected by: /analyze
- Resolution: Regenerate /tasks with feedback
- Outcome: ✓ Resolved (tasks now include error handling)

**Issue 2:** [If any other issues]
- ...

## Logs

For detailed execution logs, see: `/memories/session/orchestration-trace.md`
```

### Execution Trace (`/memories/session/orchestration-trace.md`)

```markdown
## Execution Trace: user-auth feature

### Step 1: /specify
**Time:** 2026-05-19 10:00:15 UTC  
**Duration:** 45s  
**Tokens:** 2340  
**Command:** /speckit.specify --constitution=.specify/constitution.md --description="Implement user authentication system"  
**Context injected:** 5 architectural decisions, 8 patterns, 2 recent lessons, 3421 code symbols  
**Output:** specs/spec.md (234 lines, 5 sections)  
**Status:** ✓ PASS (spec well-formed, all required sections present)  

### Step 2: /clarify
**Time:** 2026-05-19 10:01:00 UTC  
**Duration:** 30s  
**Tokens:** 1200  
**User choice:** Clarify  
**Command:** /speckit.clarify specs/spec.md  
**Output:** specs/spec.md (updated, 250 lines)  
**Status:** ✓ PASS  

... (more steps)
```

---

## Error Handling

All errors are handled per [error-handling-and-recovery.md](error-handling-and-recovery.md):

- **Category 6 (SpecKit Integration Errors)**: Retried with backoff; fallback to manual intervention
- **Category 5 (File I/O Errors)**: Logged with suggested fix
- **Category 7 (Memory Errors)**: Auto-compress if context too large
- **Cross-cutting rule: Fail Safely** — Never silent failures; always log and inform user

---

## Success Criteria

✓ Feature orchestration completes without user running individual SpecKit skills  
✓ All prompts surfaced at natural decision points  
✓ Remediation automatic (or user-controlled via --remediation flag)  
✓ Works with current SpecKit version + future versions (no code change)  
✓ Execution trace fully logged for debugging  
✓ All errors actionable (suggest fix, not just error code)  
✓ Feature state persisted (can resume if interrupted)  

---

## Implementation Notes

### Discovery Mechanism
- Query SpecKit registry on startup (cache with TTL: 24h)
- Handle registry not found gracefully (fallback to known skills)
- Log any registry queries for debugging

### Context Injection
- Load context at start (via `/spek.context`)
- Inject into each skill (via environment variable or file)
- Update context after /clarify step (if used)

### Sub-Agent Decision
- Use sub-agents for complex skills (per cavecrew guidance)
- Most skills don't need sub-agents (simple execution)
- Recommend: /implement use sub-agent for code validation

### Future-Proofing
- Never hardcode skill names or workflow order
- Always query registry at runtime
- Gracefully handle missing skills (skip with warning)
- Log any registry changes (for audit trail)

---

## Related Specs

- [speckit-integration-contract.md](speckit-integration-contract.md) — Integration pattern + responsibility division
- [cli-orchestration.md](cli-orchestration.md) — Lower-level CLI commands
- [error-handling-and-recovery.md](error-handling-and-recovery.md) — Cross-cutting error strategy
- [context-layer.md](context-layer.md) — Context injection mechanism
- [prepare-and-post-skills.md](prepare-and-post-skills.md) — Prepare/post skills

---

## Final Notes

`spek.automate` is the **primary user-facing entry point** for Spekificity. By dynamically discovering and orchestrating SpecKit skills, it:

- **Simplifies user experience** — One command instead of many
- **Handles complexity invisibly** — User sees prompts, not internals
- **Future-proofs** — Works with any SpecKit version
- **Logs everything** — Full audit trail for debugging

Implementation should follow this spec exactly, prioritizing:
1. **Dynamic discovery** (not hardcoded skill names)
2. **Graceful degradation** (skip missing skills)
3. **User prompts at natural points** (not overload)
4. **Comprehensive logging** (every decision logged)
