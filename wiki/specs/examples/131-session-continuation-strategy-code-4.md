```
Signal Handler (Ctrl+C):

Step 1: Catch Interrupt Signal
  ├─ Save current state immediately
  └─ Stop execution (no partial writes)

Step 2: Save Checkpoint
  ├─ Update vault/session/:
  │  ├─ last-checkpoint = NOW
  │  ├─ phase = current phase (specify|plan|implement|post)
  │  ├─ progress = best estimate based on completed steps
  │  └─ interrupted = true
  ├─ Flush to disk (ensure written)
  └─ Status: Checkpoint saved

Step 3: Clean Up Resources
  ├─ Close open files
  ├─ Cancel any in-flight API calls (to SpecKit, lat.md)
  ├─ Release locks (git, vault writes)
  └─ Status: Resources cleaned

Step 4: Notify User
  ├─ Print: "⚠️  Feature interrupted and saved"
  ├─ Print: "Feature state: phase=implementing, task 2 of 3"
  ├─ Print: "Resume with: spek.prepare --resume"
  └─ Exit code: 130 (SIGINT received)

Step 5: Exit Gracefully
  ├─ No data loss
  ├─ No corrupted state files
  ├─ Ready for resume next session
  └─ Session can be inspected for diagnostics
```
