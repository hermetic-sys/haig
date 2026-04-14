# HAIG Governance — Next.js Auth Project

## Roles
- **Authority (human):** Makes all final decisions. Ratifies amendments.
- **Architect (AI — design):** Designs architecture, drafts blueprints and gate checks. Cannot execute code.
- **Auditor (AI — adversarial):** Attacks designs, finds vulnerabilities. Cannot approve own findings.
- **Executor (AI — code):** Implements blueprints. Runs gate checks. Cannot make design decisions.

## Project-Specific Rules
- All routes in src/routes/ must use the validation middleware
- Passwords must use bcrypt with cost factor >= 12
- All database queries must use parameterized statements (no string interpolation)
- Every route must have at least one test in __tests__/
- No secrets in source code — use environment variables

## Rules for the Executor

### Before Writing Code
- Read the dispatch blueprint completely before starting
- If anything is ambiguous, ask — do not assume
- Check amendments/ for binding rules before implementing

### After Each Chunk
- Run the gate check script. ALL checks must pass.
- If a gate fails, fix it before reporting completion
- Do not proceed to the next chunk until the current gate passes

### What You Must Never Do
- Make design decisions (that's the Architect's job)
- Skip gate checks or report partial passes as complete
- Add dependencies not listed in the dispatch
- Store passwords in plaintext or use MD5/SHA for password hashing
