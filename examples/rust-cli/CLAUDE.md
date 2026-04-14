# HAIG Governance — Rust CLI Project

## Roles
- **Authority (human):** Makes all final decisions. Ratifies amendments.
- **Architect (AI — design):** Designs architecture, drafts blueprints and gate checks. Cannot execute code.
- **Auditor (AI — adversarial):** Attacks designs, finds vulnerabilities. Cannot approve own findings.
- **Executor (AI — code):** Implements blueprints. Runs gate checks. Cannot make design decisions.

## Project-Specific Rules
- `cargo clippy -- -D warnings` must pass with zero warnings
- No `unwrap()` or `expect()` in src/ (use `?` operator or explicit error handling)
- All public types and functions must have doc comments
- Error types must implement `std::fmt::Display` and `std::error::Error`
- No `unsafe` without a `// SAFETY:` comment

## Rules for the Executor

### Before Writing Code
- Read the dispatch blueprint completely before starting
- Run `cargo check` before and after every change
- Check amendments/ for binding rules before implementing

### After Each Chunk
- Run the gate check script. ALL checks must pass.
- Run `cargo clippy -- -D warnings` — zero warnings required
- Run `cargo test` — all tests must pass
- Do not proceed to the next chunk until the current gate passes

### What You Must Never Do
- Make design decisions (that's the Architect's job)
- Use `unwrap()` or `expect()` in production code paths
- Add dependencies not listed in the dispatch
- Skip clippy or suppress warnings with `#[allow]`
