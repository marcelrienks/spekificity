# Integration Checklist: Pre-Shipping Verification

**Use this checklist before marking a feature complete and closing the loop.**

**See also:** [workflow.md](workflow.md), [architecture.md](architecture.md), [naming-conventions.md](naming-conventions.md)

---

## Code Quality

### Documentation & Clarity
- [ ] All functions have docstrings (purpose, args, return)
- [ ] All classes have docstrings (purpose, key methods)
- [ ] Complex logic has inline comments explaining *why*, not just *what*
- [ ] README or setup guide exists for the feature area
- [ ] No TODO/FIXME comments without a follow-up task

### Testing
- [ ] Unit tests pass locally (< 5 minutes)
- [ ] Integration tests pass locally (< 10 minutes)
- [ ] Edge cases covered (null, empty, invalid input)
- [ ] Error paths tested (exceptions, boundary conditions)
- [ ] Test coverage > 80% for new code

### Code Standards
- [ ] Code follows project style guide (linting passes)
- [ ] No console.log or debug statements in production code
- [ ] No hardcoded values (magic numbers, strings; use constants)
- [ ] No unused imports or variables
- [ ] Naming is clear and consistent (follows [naming-conventions.md](naming-conventions.md))

### Performance
- [ ] No N+1 queries (verified via CodeGraph analysis)
- [ ] No unnecessary loops or recursion
- [ ] API responses < 100ms for simple queries
- [ ] Memory usage reasonable (no obvious leaks)

---

## Documentation

### Specification & Planning Artifacts
- [ ] Feature spec exists in vault (linked in this feature's metadata)
- [ ] Spec includes Success Criteria (all items checked off)
- [ ] Spec includes Assumptions (documented)
- [ ] Spec includes Risk Assessment (reviewed and mitigated)
- [ ] Plan exists in vault (all tasks completed)
- [ ] Plan includes task breakdown (each task has clear output)
- [ ] Dependencies documented (which tasks depend on others)

### Vault Updates
- [ ] Archived spec committed to vault
- [ ] Archived plan committed to vault
- [ ] Lessons learned document created and committed
- [ ] Links to related decisions added (if applicable)
- [ ] Lessons linked to future reusable patterns

### Code Documentation
- [ ] Commit messages reference spec/task IDs (e.g., `[Task 2] Implement auth service`)
- [ ] Pull request description links to spec/plan
- [ ] GitHub issues (if created) reference vault docs
- [ ] API documentation updated (if applicable)
- [ ] Configuration documentation updated (if new config added)

---

## Testing

### Unit Tests
- [ ] All new functions have unit tests
- [ ] All new classes have constructor/method tests
- [ ] Edge cases tested (empty input, null, boundaries)
- [ ] Error cases tested (invalid input, expected exceptions)
- [ ] Test names are descriptive (e.g., `test_user_creation_with_missing_email_fails`)

### Integration Tests
- [ ] Feature works end-to-end with existing code
- [ ] Database migrations (if any) work correctly
- [ ] API endpoints return correct status codes
- [ ] Error responses include helpful messages

### Regression Testing
- [ ] Existing tests still pass (no breaking changes)
- [ ] Backwards compatibility verified (if applicable)
- [ ] No new warnings in build output

### Test Suite Performance
- [ ] Full test suite runs locally < 5 minutes
- [ ] No flaky tests (tests pass consistently)
- [ ] CI/CD pipeline passes (if configured)

---

## Integration

### Spekificity Workflow Commands
- [ ] `/spek.prepare` passes pre-flight checks
- [ ] `/spek.automate --phase=specify` produced valid spec
- [ ] `/spek.automate --phase=plan` produced valid plan
- [ ] `/spek.implement --plan=...` executed all tasks
- [ ] `/spek.post` archived artifacts successfully
- [ ] `/spek.lessons` extracted meaningful lessons

### CodeGraph Integration
- [ ] CodeGraph reflects all new code (symbols, functions, classes)
- [ ] Impact analysis shows affected downstream components
- [ ] CodeGraph queries used during implementation (not file grep)
- [ ] Graph remains < 100ms query response time

### Vault Integration
- [ ] Spec stored in vault with correct metadata
- [ ] Plan stored in vault with task linkage
- [ ] Lessons stored in vault with tags for retrieval
- [ ] All artifacts committed to git (no uncommitted changes)

### Tooling Integration
- [ ] All `/spek.*` commands work end-to-end
- [ ] `/speckit.*` commands produce expected outputs
- [ ] Error handling works (commands fail gracefully, not silently)
- [ ] Session context loaded correctly for follow-on features

---

## Performance

### Token Efficiency
- [ ] Estimated tokens (from plan) vs. actual tokens (from session) logged
- [ ] Token budget not exceeded (if one was set)
- [ ] No re-reading of vault docs within a session (context reuse)
- [ ] CodeGraph used for analysis (not file scanning)

### Execution Time
- [ ] Feature workflow completed within planned time estimate
- [ ] No unexpected delays or bottlenecks
- [ ] Parallel task execution considered (if safe)
- [ ] No long-running blocking operations in user-facing commands

### Resource Usage
- [ ] CodeGraph query performance acceptable (< 100ms per query)
- [ ] Vault sync time acceptable (< 30 sec)
- [ ] Git operations fast (no large binary files added)
- [ ] Session memory reasonable (context not bloated)

---

## Feature-Specific Checklist

*Add items specific to this feature here. Examples:*

### If Adding API Endpoint
- [ ] Endpoint returns correct HTTP status codes (200, 400, 404, 500, etc.)
- [ ] Request validation works (required fields, types, ranges)
- [ ] Response format matches OpenAPI spec (if defined)
- [ ] Rate limiting applied (if needed)
- [ ] CORS headers correct (if applicable)

### If Adding Database Migration
- [ ] Migration is idempotent (can run multiple times safely)
- [ ] Migration includes rollback (down/revert)
- [ ] Data integrity validated (no duplicate keys, orphaned records)
- [ ] Indexes created on new columns (if queried frequently)

### If Adding CLI Command
- [ ] Help text complete (`--help` output is clear)
- [ ] All flags documented and tested
- [ ] Error messages helpful (not just "Error: 1")
- [ ] Exit codes correct (0 for success, non-zero for failure)

### If Adding Authentication/Authorization
- [ ] Token generation tested
- [ ] Token expiration enforced
- [ ] Permissions checked for all protected endpoints
- [ ] Security audit completed (if required)

---

## Sign-Off Checklist

### Code Review
- [ ] Code reviewed by at least one team member (if applicable)
- [ ] Review comments addressed
- [ ] No unresolved discussions in PR

### Testing Sign-Off
- [ ] QA tested manually (if applicable)
- [ ] All test suites passing
- [ ] No known bugs or workarounds

### Documentation Sign-Off
- [ ] Spec complete and approved
- [ ] Plan complete and executed
- [ ] Lessons captured and reviewed
- [ ] Vault artifacts correct and linked

### Feature Complete
- [ ] All Integration Checklist items checked
- [ ] Feature branch merged or ready to merge
- [ ] Feature tagged/released (if applicable)
- [ ] `/spek.post` successfully archived outcomes
- [ ] Ready for next feature (vault, repo memory, CodeGraph fresh)

---

## Troubleshooting

### Issue: Tests Fail Locally
**Resolution:**
1. Run full test suite: `npm test` (or project equivalent)
2. Check for environment setup issues (env vars, database seed, etc.)
3. See [workflow.md](workflow.md) error handling section

### Issue: CodeGraph Queries Slow
**Resolution:**
1. Refresh CodeGraph: `/spek.map`
2. Check CodeGraph size: `du -h .codegraph/`
3. If > 100MB, consider excluding non-code directories (via config)

### Issue: Vault Sync Conflict
**Resolution:**
1. Check git status: `git status`
2. Resolve conflicts manually in Obsidian or editor
3. Commit resolved changes: `git add . && git commit -m "Resolve vault sync conflict"`

### Issue: Spec/Plan Missing from Vault
**Resolution:**
1. Check if `/spek.automate` was actually run: grep logs
2. If not: Run `/spek.automate --phase=specify` again
3. If already run but not in vault: Check vault directory permissions

---

## Closure

Once all checklist items are ✅:

1. **Commit:** Ensure all code and docs committed to git
2. **Archive:** Run `/spek.post` to archive feature artifacts
3. **Tag:** Git tag the feature if using semantic versioning
4. **Notify:** Let team know feature is ready (if applicable)
5. **Next:** Start new feature with `/spek.prepare`

---

## References

- **Workflow:** [workflow.md](workflow.md)
- **Architecture:** [architecture.md](architecture.md)
- **Naming & Conventions:** [naming-conventions.md](naming-conventions.md)
- **Philosophy & Principles:** [intention.md](intention.md)
- **Decision Log:** [decision.md](decision.md)
