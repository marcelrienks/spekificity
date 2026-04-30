# feature specification: [feature name]

**feature branch**: `[###-feature-name]`  
**created**: [date]  
**status**: draft  
**input**: user description: "$arguments"

## user scenarios & testing *(mandatory)*

<!--
  important: user stories should be prioritized as user journeys ordered by importance.
  each user story/journey must be independently testable - meaning if you implement just one of them,
  you should still have a viable mvp (minimum viable product) that delivers value.
  
  assign priorities (p1, p2, p3, etc.) to each story, where p1 is the most critical.
  think of each story as a standalone slice of functionality that can be:
  - developed independently
  - tested independently
  - deployed independently
  - demonstrated to users independently
-->

### user story 1 - [brief title] (priority: p1)

[describe this user journey in plain language]

**why this priority**: [explain the value and why it has this priority level]

**independent test**: [describe how this can be tested independently - e.g., "can be fully tested by [specific action] and delivers [specific value]"]

**acceptance scenarios**:

1. **given** [initial state], **when** [action], **then** [expected outcome]
2. **given** [initial state], **when** [action], **then** [expected outcome]

---

### user story 2 - [brief title] (priority: p2)

[describe this user journey in plain language]

**why this priority**: [explain the value and why it has this priority level]

**independent test**: [describe how this can be tested independently]

**acceptance scenarios**:

1. **given** [initial state], **when** [action], **then** [expected outcome]

---

### user story 3 - [brief title] (priority: p3)

[describe this user journey in plain language]

**why this priority**: [explain the value and why it has this priority level]

**independent test**: [describe how this can be tested independently]

**acceptance scenarios**:

1. **given** [initial state], **when** [action], **then** [expected outcome]

---

[add more user stories as needed, each with an assigned priority]

### edge cases

<!--
  action required: the content in this section represents placeholders.
  fill them out with the right edge cases.
-->

- what happens when [boundary condition]?
- how does system handle [error scenario]?

## requirements *(mandatory)*

<!--
  action required: the content in this section represents placeholders.
  fill them out with the right functional requirements.
-->

### functional requirements

- **fr-001**: system must [specific capability, e.g., "allow users to create accounts"]
- **fr-002**: system must [specific capability, e.g., "validate email addresses"]  
- **fr-003**: users must be able to [key interaction, e.g., "reset their password"]
- **fr-004**: system must [data requirement, e.g., "persist user preferences"]
- **fr-005**: system must [behavior, e.g., "log all security events"]

*example of marking unclear requirements:*

- **fr-006**: system must authenticate users via [needs clarification: auth method not specified - email/password, sso, oauth?]
- **fr-007**: system must retain user data for [needs clarification: retention period not specified]

### key entities *(include if feature involves data)*

- **[entity 1]**: [what it represents, key attributes without implementation]
- **[entity 2]**: [what it represents, relationships to other entities]

## success criteria *(mandatory)*

<!--
  action required: define measurable success criteria.
  these must be technology-agnostic and measurable.
-->

### measurable outcomes

- **sc-001**: [measurable metric, e.g., "users can complete account creation in under 2 minutes"]
- **sc-002**: [measurable metric, e.g., "system handles 1000 concurrent users without degradation"]
- **sc-003**: [user satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **sc-004**: [business metric, e.g., "reduce support tickets related to [x] by 50%"]

## assumptions

<!--
  action required: the content in this section represents placeholders.
  fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- [assumption about target users, e.g., "users have stable internet connectivity"]
- [assumption about scope boundaries, e.g., "mobile support is out of scope for v1"]
- [assumption about data/environment, e.g., "existing authentication system will be reused"]
- [dependency on existing system/service, e.g., "requires access to the existing user profile api"]
