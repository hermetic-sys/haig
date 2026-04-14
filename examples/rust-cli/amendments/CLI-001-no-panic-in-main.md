# CLI-001: No Panic in Production Code

**Status:** RATIFIED
**Date:** 2026-04-01
**Trigger:** Architecture decision — CLI tools must not panic on user input

## Binding Text
`main()` MUST return `Result`. No `unwrap()` or `expect()` calls MAY appear in any production code path (src/ excluding test modules). All error conditions MUST propagate via `?` or explicit match arms with user-friendly error messages.

## Enforcement
**File:** src/ (all files)
**Line:** Every function that handles external input or I/O

## Gate Check
```bash
# No unwrap/expect in production code
! grep -rn 'unwrap()\|expect(' src/ | grep -v '#\[test\]\|#\[cfg(test)\]' || { echo "FAIL: unwrap/expect in production code"; exit 1; }

# main returns Result
grep -q 'fn main.*Result' src/main.rs || { echo "FAIL: main does not return Result"; exit 1; }
```

## Rationale
A CLI tool that panics on bad input (malformed config file, missing file, invalid argument) provides a poor user experience and no actionable error message. `Result` propagation ensures every error path produces a readable message. `unwrap()` in production code is a latent panic waiting for the right input to trigger it.
