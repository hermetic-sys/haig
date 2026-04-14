# Dispatch Pipeline

A dispatch is a self-contained execution blueprint. It tells the Executor exactly what to build, in what order, and how to verify each step.

## Dispatch Structure

Every dispatch follows this format:

- **Goal** — one sentence describing what this dispatch delivers
- **Prerequisites** — what must exist before execution begins
- **File map** — every file to create or modify, with purpose and estimated LOC
- **Chunks** — ordered implementation steps, each with its own gate
- **Rules** — binding constraints for the Executor
- **Prohibitions** — explicit things the Executor must not do

## Chunks

A dispatch is divided into chunks. Each chunk is a self-contained unit of work that builds on the previous chunk. Chunks are implemented in order — the Executor does not skip ahead.

Each chunk contains:

- **Goal** — what this specific chunk delivers
- **Implementation** — pseudocode or step-by-step instructions (not line-by-line code — the Executor translates to actual implementation)
- **Gate** — a bash script that verifies the chunk is complete

## Gate Checks

The gate is a bash script. It starts with `set -e` so any failure stops execution. Each check is a `grep`, `test`, compilation command, or test runner that exits non-zero on failure.

```bash
#!/bin/bash
set -e
echo '--- 1. Config struct exists ---'
grep -q 'pub struct Config' src/config.rs
echo 'PASS'
```

The Executor runs the gate after completing each chunk. All checks must pass before proceeding to the next chunk. If a gate fails, the Executor fixes the code and reruns — it does not skip, comment out, or weaken the gate check.

## Final Gate

After all chunks are complete, a final gate covers the entire dispatch. This gate combines the critical checks from all chunk gates plus any integration-level verifications.

## Dispatch Template

Use `templates/dispatch-template.md` as the starting point for every dispatch. Fill in the placeholders, define the chunks, write the gates. The template enforces the structure — you provide the content.

## Key Principle

The dispatch is a contract. The Architect writes it. The Authority ratifies it. The Executor implements it. If the dispatch is wrong, the fix goes through the Architect — the Executor does not improvise.
