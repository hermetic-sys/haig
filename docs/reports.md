# Reports — Documenting Every Step

Every dispatch execution produces a DevOps report. Reports are not optional paperwork. They are the evidence trail that proves governance happened and the primary input for the Architect's next dispatch.

## Why Reports Exist

Without reports, knowledge lives in chat logs that nobody reads. The Architect writes the next dispatch based on memory, not evidence. Mistakes repeat because nobody recorded what went wrong last time.

Reports break this cycle. Every dispatch produces a structured record: what was built, what deviated from plan, what the gates found, and what was learned. The Architect reads prior reports before writing new dispatches. The Authority reads them to verify governance compliance.

## What a Report Contains

1. **Summary**: LOC added/removed, files modified, tests added, gate results, duration
2. **What was delivered**: prose description of completed work
3. **Deviations**: any point where implementation diverged from the dispatch, with explanation
4. **Gate results**: per-check pass/fail with actual output
5. **Files modified**: exact file list with line counts and purpose
6. **Issues encountered**: build failures, dependency problems, ambiguities in the dispatch

## SA Verification Section

For critical features — security, authentication, cryptography, access control, data handling — the report includes a section where the Architect reviews the actual code the Executor wrote, not just the gate results.

Gates catch structural violations: missing functions, unwrap calls, test failures. They do not catch semantic bugs: checking the wrong variable, using the wrong algorithm, missing a race condition. The Architect's code review catches what gates cannot.

This is not a full code review. The Architect focuses on:

- Does the code do what the dispatch specified, semantically?
- Are the security-critical paths correct in logic, not just structure?
- Are there assumptions in the code that the gates don't verify?

## The Report Chain

Reports form a chain. Each report references its dispatch. The Architect reads the chain before writing a new dispatch:

```
Dispatch-001 → Report-001 (auth system, 3 chunks, 12 gates PASS)
Dispatch-002 → Report-002 (rate limiting, 2 chunks, deviation: changed API)
Dispatch-003 → Report-003 (session hardening, from AM-044)
```

The chain is the project's execution history. Combined with the amendment registry, it provides a complete governance record: what was decided, what was built, and whether the build matched the decision.

## Report Template

Use `templates/devops-report-template.md` for every report. Fill in every section — incomplete reports break the chain.

## When to Write Reports

- After completing all chunks of a dispatch (final report)
- After completing each chunk of a multi-session dispatch (interim report)
- When a dispatch is abandoned or blocked (incident report)
- At the end of every session, even if the dispatch is incomplete (session report — this overlaps with the context dump)
