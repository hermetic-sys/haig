# Amendments

An amendment is a binding decision with an enforcement location. It encodes a rule that was learned, discovered, or decided during the project — and makes it permanent.

## Amendment Structure

Every amendment has:

- **ID** — sequential identifier (e.g., SEC-001, CLI-003). Never renumber. If an amendment is revoked, the ID is retired.
- **Status** — DRAFT (proposed), RATIFIED (binding), or REVOKED (no longer applies)
- **Date** — when the amendment was ratified
- **Trigger** — what finding, bug, incident, or decision prompted the amendment
- **Binding text** — the rule itself, using MUST/MUST NOT/MAY language
- **Enforcement location** — the file and approximate line range where the rule is implemented
- **Gate check** — a command that verifies compliance. Returns 0 if compliant, non-zero if violated.

## Why Amendments Matter

Without amendments, lessons are learned and forgotten. A bug is fixed, but the class of bug is not prevented. A design decision is made in a chat session, but the next session has no record of it.

Amendments are the project's institutional memory. They accumulate over the project's lifetime. The Executor checks the `amendments/` directory before implementing any dispatch. If new code would violate an existing amendment, the Executor stops and reports the conflict.

## Lifecycle

1. A finding, bug, or decision triggers the need for a rule
2. The Architect drafts the amendment (status: DRAFT)
3. The Authority reviews and ratifies (status: RATIFIED)
4. The Executor checks amendments before every implementation
5. If the rule no longer applies, the Authority revokes it (status: REVOKED)

Revoked amendments keep their ID. They are not deleted — they remain in the amendments directory with REVOKED status. This preserves the decision history.

## Rationale Field

Every amendment includes a rationale: why does this rule exist? What goes wrong without it? This context is critical for future decisions about whether an amendment should be modified or revoked.

## Template

Use `templates/amendment-template.md` to create new amendments. The template enforces the required fields.
