```
Validation Checklist (/spek.prepare --resume):

✓ vault/session/ exists?
  └─ No: New feature workflow

✓ YAML frontmatter valid?
  └─ No: Corrupted state file; suggest --reset

✓ Feature branch still exists in git?
  └─ No: Branch deleted; can't resume; create new feature

✓ Feature branch on correct revision?
  └─ Different: Warn user about branch drift

✓ Spec file exists in vault?
 └─ No: Missing artifact; can't resume; start over

✓ Plan file exists in vault?
  └─ No: Missing artifact; can't resume; start over

✓ Feature phase is not "complete"?
  └─ Is "complete": Can't resume finished feature; start new one

✓ Token usage is < 2x budget?
  └─ Much higher: Suggest investigating token tracking; may be corrupted

✓ Timestamps are sensible (checkpoint < now < started)?
  └─ No: Time travel detected; corrupted state; suggest --reset

All checks pass?
  └─ Status: VALID — Resume safe
  
Any check fails?
  └─ Status: INVALID — Error handling (see 3b above)
```
