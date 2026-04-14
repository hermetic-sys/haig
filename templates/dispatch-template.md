# DISPATCH-[NNN]: [Feature Name]

## Goal
[One sentence: what this dispatch builds]

## Prerequisites
[What must exist before this dispatch can execute]

## Files
| File | Action | LOC | Purpose |
|------|--------|-----|---------|
| [path/to/file] | CREATE/MODIFY | [est] | [purpose] |

## Chunk 1: [Name]

### Goal
[What this chunk delivers]

### Implementation
[Pseudocode or step-by-step instructions]

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 1 GATE ==='

echo '--- 1. [Check name] ---'
[verification command]
echo 'PASS'

echo '--- 2. [Check name] ---'
[verification command]
echo 'PASS'

echo 'GATE: X/X PASS'
```

## Rules
- [Binding rules for the Executor]

## Prohibitions
- Do NOT [thing the Executor must avoid]
