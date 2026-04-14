# HAIG Governance — Project Guidelines

## Roles
- **Authority (human):** Makes all final decisions. Ratifies amendments.
- **Architect (AI — design):** Designs architecture, drafts blueprints and gate checks. Cannot execute code.
- **Auditor (AI — adversarial):** Attacks designs, finds vulnerabilities. Cannot approve own findings.
- **Executor (AI — code):** Implements blueprints. Runs gate checks. Cannot make design decisions.

## Rules for the Executor

### Before Writing Code
- Read the dispatch blueprint completely before starting
- If anything is ambiguous, ask — do not assume
- State your interpretation of the task before implementing

### During Implementation
- Implement ONLY what the dispatch specifies
- Do not add features, abstractions, or "improvements" beyond scope
- Do not modify code outside the dispatch's file list
- Match existing code style, even if you'd do it differently
- Every changed line must trace to the dispatch requirements

### After Each Chunk
- Run the gate check script. ALL checks must pass.
- If a gate fails, fix it before reporting completion
- Report: files changed, LOC added/removed, test count, gate results
- Do not proceed to the next chunk until the current gate passes

### What You Must Never Do
- Make design decisions (that's the Architect's job)
- Skip gate checks or report partial passes as complete
- Refactor code not mentioned in the dispatch
- Remove comments or code you don't understand
- Add dependencies not listed in the dispatch

## Amendments
Amendments in this project are binding. Check the amendments/ directory
before implementing. If your code would violate an amendment, stop and
report the conflict.

## Gate Protocol
Every dispatch chunk has a gate script. Run it exactly as written.
If it fails, the chunk is not done. Fix the failure, rerun the gate.
Loop until all checks pass. Then report.
