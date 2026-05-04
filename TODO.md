---

## [ ] 12. Investigate `Alexanderdunlop/skills` `test-interrogate` skill for inclusion

**Repository**: https://github.com/Alexanderdunlop/skills/blob/main/skills/development/test-interrogate/SKILL.md

**Question**: Should the `test-interrogate` skill be adopted into spekificity's `skills/development/` bucket?

The `test-interrogate` skill from `Alexanderdunlop/skills` implements a structured, interview-driven approach to unit test planning. It walks through a diff one question at a time, documents agreed test cases into `docs/test-plans/<NNN>-<short-description>.md`, and enforces a strict separation between the interrogation phase and the implementation phase — no test code is written until all questions are resolved and the user confirms.

**Evaluate**:

- Does the interrogation-first, implement-all-at-once model fit the spekificity workflow, particularly alongside speckit's specify → plan → tasks → implement flow?
- Is the `docs/test-plans/` output location consistent with spekificity's documentation conventions, or should it be mapped to a different path (e.g. `specs/` or `vault/`)?
- Does the skill's reliance on `git diff main...HEAD` align with how spekificity feature branches are structured?
- Could this skill integrate naturally with `speckit.implement` — e.g. invoked after implement to verify coverage — or does it belong earlier in the flow (post-plan, pre-implement)?
- Are there any rules or behaviours in the skill that conflict with spekificity's existing patterns (e.g. caveman mode, vault context, lessons-learnt)?

**Why it matters**: Test coverage is a gap in the current spekificity workflow. The `test-interrogate` skill offers a proven, disciplined pattern for surfacing test cases collaboratively. If it fits, it belongs in `skills/development/` and should be referenced in the main `README.md` and the development bucket `README.md`.