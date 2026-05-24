```
Step 1: Check for existing vault/session/
  ├─ Not found: New feature workflow (normal prepare)
  ├─ Found: Resume workflow (steps 2-5 below)

Step 2: Validate Feature State
  ├─ Parse YAML frontmatter (feature-id, phase, progress, last-checkpoint)
  ├─ Check Git state: Feature branch still exists? On correct branch?
  ├─ Check Feature artifacts: Spec + plan files exist in vault?
  ├─ Status: Valid state | Invalid (corrupted or stale) | Completed

Step 3a: Valid State → Resume Detected
  ├─ Restore context:
  │  ├─ Reload vault decisions + patterns from disk
  │  ├─ Load spec + plan from vault/specs/ and vault/plans/
  │  ├─ Query code graph for current code state (no cache; fresh)
  │  └─ Update vault/session/ with "resumed" timestamp
  ├─ Report: "Feature resumed: add-logging (phase: implementing, task 2 of 3)"
  └─ Ready: Return to caller for next step (/spek.implement --resume)

Step 3b: Invalid State → Error Handling
  ├─ Corrupted YAML: Notify user, suggest --reset (dangerous!)
  ├─ Missing feature branch: Notify user, suggest creating branch
  ├─ Missing spec/plan: Notify user, suggest re-running /spek.prepare (new feature)
  ├─ Feature marked "complete": Notify user (can't resume completed feature)
  └─ Recover: Ask user: retry resume | reset | new feature?

Step 3c: Completed Feature → Error
  ├─ Phase = "complete": Feature already finished
  ├─ Suggestion: "Start new feature with /spek.prepare <new-name>"
  └─ Abort: Exit with code 1
```
