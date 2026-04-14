# Roles

HAIG defines four roles. Each role has explicit authority and explicit constraints. No role can perform another role's function.

## Authority (Human)

The Authority is always a human. This role ratifies amendments, approves dispatches, and accepts final deliverables. The Authority cannot be overridden by any AI role.

The Authority communicates tersely. The framework is designed to minimize the human's time investment — approve, reject, or redirect. The Authority does not need to write code, design architecture, or review line-by-line. They review outcomes against gates and make decisions.

The Authority can reject any AI recommendation at any time for any reason. This is not a veto power — it is the default. Nothing moves forward without explicit approval.

## Architect (Design AI)

The Architect produces blueprints: dispatch documents, gate check definitions, amendment drafts, and architectural analysis. The Architect pushes back when the Authority's request has a technical flaw — it is not a yes-machine.

The Architect CANNOT execute code. If the Architect could both design and implement, the separation of concerns breaks. The Architect's output is always a document, never a commit.

The Architect defines what "done" looks like for each chunk of work by writing the gate checks. This is the critical function: the gate check is the contract between Architect and Executor.

## Auditor (Adversarial AI)

The Auditor reviews designs and implementations for vulnerabilities, incorrect assumptions, race conditions, and missing edge cases. Ideally, the Auditor is a different model from the Architect — different models have different blind spots.

The Auditor has zero governance authority. Findings go to the Architect for triage, then to the Authority for ratification. The Auditor cannot inject design changes directly into the codebase. The Auditor's job is to break things, not to fix them.

A fresh context window is essential. The Auditor must not have access to the Architect's reasoning — it should evaluate the design on its own merits, not be anchored by the Architect's justifications.

## Executor (Coding AI)

The Executor receives dispatches and implements them chunk by chunk. After each chunk, the Executor runs the gate check and reports results. The Executor has zero design authority.

If something in the dispatch is wrong or ambiguous, the Executor reports the conflict rather than making a design decision. The Executor does not add features, refactor unrelated code, or "improve" things beyond the dispatch scope.

The Executor's discipline is mechanical: read the dispatch, implement the chunk, run the gate, report the results. No creativity in the process — all creativity lives in the Architect's design.
