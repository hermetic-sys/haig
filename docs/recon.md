# Recon — Understanding the Codebase Before Acting

Every session starts with a recon script. No exceptions.

## Why Recon Exists

Dispatches are written by the Architect based on their understanding of the codebase at design time. But codebases drift. Files change between sessions. Dependencies update. Tests get added or removed. New patterns emerge.

If the Executor starts implementing a dispatch without checking what the codebase actually looks like right now, it will hit mismatches — wrong file paths, missing functions, incompatible APIs. These mismatches waste time and produce bad code.

Recon eliminates this. The Executor runs a standard script at the start of every session, before reading any dispatch. The output goes to both the Authority and the Architect. If the recon reveals that the dispatch's assumptions are wrong, the Executor stops and reports. The Architect amends the dispatch. The Executor does not improvise.

## What Recon Covers

- **Git state**: current branch, recent commits, uncommitted changes
- **Build status**: does the project compile/build cleanly right now
- **Test count**: how many tests exist, are any failing
- **Dependency check**: any new or changed dependencies since last session
- **Files in scope**: line counts and key patterns in the files the dispatch will modify

## The Rule

Recon output is a governance artifact. The Architect uses it to verify or amend the dispatch. The Authority uses it to understand the starting state. The Executor uses it to validate assumptions before writing code.

If recon reveals the dispatch's assumptions are wrong, the Executor MUST stop and report. The Architect amends the dispatch. The Executor does not improvise.

## Recon Template

Adapt this to your language and project:

```bash
#!/bin/bash
set -e
echo "=== RECON — $(date -Iseconds) ==="

echo ""
echo "=== GIT STATE ==="
git log --oneline -5
git diff --stat HEAD

echo ""
echo "=== BUILD ==="
# Replace with your build command:
# cargo check          (Rust)
# npm run build        (Node)
# go build ./...       (Go)
# python -m py_compile (Python)

echo ""
echo "=== TESTS ==="
# Replace with your test list command:
# cargo test -- --list 2>&1 | grep ': test$' | wc -l
# npm test -- --listTests | wc -l
# go test ./... -list '.*' | grep -c '^Test'

echo ""
echo "=== FILES IN SCOPE ==="
# List the files the dispatch will modify:
# wc -l src/auth.ts src/routes.ts src/middleware.ts
# grep -n 'key_function_name' src/target_file.rs

echo ""
echo "=== DEPENDENCIES ==="
# Check for changes:
# diff <(git show HEAD:package-lock.json | head -50) <(head -50 package-lock.json)
# cargo tree --depth 1

echo "=== RECON COMPLETE ==="
```

## When to Run Recon

- At the start of every session, before reading any dispatch
- After pulling changes from other contributors
- Before resuming a paused dispatch
- When the Architect requests updated codebase state

## What Happens When Recon Finds a Problem

If recon reveals that the dispatch's assumptions are wrong — a file doesn't exist, an API has changed, a dependency was removed, tests are failing — the Executor reports the mismatch with specifics:

1. What the dispatch assumed
2. What the code actually shows
3. The specific files and lines that differ

The Architect then produces either an amended dispatch or a deviation approval. The Executor cannot proceed without one of these artifacts.
