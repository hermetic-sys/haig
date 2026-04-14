# Plan Mode — Validate Before You Build

Before executing a dispatch, the Executor reads it and produces a plan. The plan is not implementation — it is a structured assessment of whether the dispatch can be executed as written.

## Why Plan Mode Exists

Dispatches are written by the Architect based on design-time understanding. The Executor has access to the actual codebase. These two perspectives often diverge.

Plan mode catches the divergence before any code is written. The Executor reads the dispatch, reads the codebase, and reports: "Here is what the dispatch says. Here is what the code actually looks like. Here are the mismatches."

Without plan mode, the Executor discovers mismatches mid-implementation and either improvises (violating role boundaries) or stops and waits (wasting time). Plan mode front-loads this discovery.

## What a Plan Contains

1. **Dispatch summary**: what the Executor understands the dispatch to require
2. **Codebase reality**: what the target files actually contain right now (from recon)
3. **Mismatches**: any assumptions in the dispatch that don't match reality
4. **Dependencies**: what must exist before each chunk can proceed
5. **Risk areas**: chunks where the implementation is ambiguous or has multiple valid approaches

## The Plan Review Cycle

1. Executor reads dispatch and codebase
2. Executor produces plan document
3. Authority reviews the plan
4. If mismatches exist, Architect amends the dispatch
5. If the plan is clean, Authority approves execution
6. Only after plan approval does implementation begin

## When Plan Mode Is Mandatory

Plan mode is mandatory for:

- Dispatches touching 3 or more files
- Dispatches with security implications (auth, crypto, access control)
- Dispatches modifying existing code (not greenfield creation)
- Dispatches where the Executor has not worked in this area of the codebase before

Plan mode is optional for:

- Single-file changes with clear, unambiguous instructions
- Documentation-only changes
- Configuration changes with no code impact

## The Key Constraint

The plan is a read-only assessment. The Executor does not write code during plan mode. It reads, analyzes, and reports. If the Executor starts coding before the plan is approved, it is violating role boundaries — building what it thinks is right instead of what the Authority has ratified.

## Plan Mode in Practice

The Executor's plan output looks like this:

```
PLAN: Dispatch-041 — Session Token TTL

Dispatch assumes:
  - state.rs has a DaemonState struct with session_tokens field
  - dispatch.rs has a token verification path

Codebase reality:
  - state.rs:50 — DaemonState exists, session_tokens is HashMap<String, TokenEntry>
  - dispatch.rs:211-255 — token verification uses verify_token()
  - TokenEntry has issued_at but NO ttl field (mismatch)

Mismatches:
  1. Dispatch says "add token_ttl field" — but TokenEntry is in attestation.rs, not state.rs
  2. Chunk 2 references dispatch.rs:verify_token — function is actually at line 377, not 211

Recommendation:
  Amend chunk 1 to modify attestation.rs instead of state.rs.
  Update line references in chunk 2.

Awaiting Architect amendment or Authority approval to proceed.
```

This plan caught two mismatches that would have caused implementation failures. The Architect amends, the Authority approves, and the Executor builds from accurate information.
