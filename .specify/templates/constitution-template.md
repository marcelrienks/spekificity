# [project_name] constitution
<!-- example: spec constitution, taskflow constitution, etc. -->

## core principles

### [principle_1_name]
<!-- example: i. library-first -->
[principle_1_description]
<!-- example: every feature starts as a standalone library; libraries must be self-contained, independently testable, documented; clear purpose required - no organizational-only libraries -->

### [principle_2_name]
<!-- example: ii. cli interface -->
[principle_2_description]
<!-- example: every library exposes functionality via cli; text in/out protocol: stdin/args → stdout, errors → stderr; support json + human-readable formats -->

### [principle_3_name]
<!-- example: iii. test-first (non-negotiable) -->
[principle_3_description]
<!-- example: tdd mandatory: tests written → user approved → tests fail → then implement; red-green-refactor cycle strictly enforced -->

### [principle_4_name]
<!-- example: iv. integration testing -->
[principle_4_description]
<!-- example: focus areas requiring integration tests: new library contract tests, contract changes, inter-service communication, shared schemas -->

### [principle_5_name]
<!-- example: v. observability, vi. versioning & breaking changes, vii. simplicity -->
[principle_5_description]
<!-- example: text i/o ensures debuggability; structured logging required; or: major.minor.build format; or: start simple, yagni principles -->

## [section_2_name]
<!-- example: additional constraints, security requirements, performance standards, etc. -->

[section_2_content]
<!-- example: technology stack requirements, compliance standards, deployment policies, etc. -->

## [section_3_name]
<!-- example: development workflow, review process, quality gates, etc. -->

[section_3_content]
<!-- example: code review requirements, testing gates, deployment approval process, etc. -->

## governance
<!-- example: constitution supersedes all other practices; amendments require documentation, approval, migration plan -->

[governance_rules]
<!-- example: all prs/reviews must verify compliance; complexity must be justified; use [guidance_file] for runtime development guidance -->

**version**: [constitution_version] | **ratified**: [ratification_date] | **last amended**: [last_amended_date]
<!-- example: version: 2.1.1 | ratified: 2025-06-13 | last amended: 2025-07-16 -->
