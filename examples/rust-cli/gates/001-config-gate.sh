#!/bin/bash
# Gate: DISPATCH-001 — TOML Config Parser
# Run after: All chunks complete
# Expected: All checks pass
set -e

echo '=== DISPATCH-001 FINAL GATE ==='

echo '--- 1. Config struct exists ---'
grep -q 'pub struct Config' src/config.rs
echo 'PASS'

echo '--- 2. Error type with Display ---'
grep -q 'enum ConfigError' src/error.rs
grep -q 'impl.*Display.*ConfigError' src/error.rs
echo 'PASS'

echo '--- 3. Validation function ---'
grep -q 'fn validate' src/config.rs
echo 'PASS'

echo '--- 4. CLI --config flag ---'
grep -q 'config' src/main.rs
echo 'PASS'

echo '--- 5. main returns Result ---'
grep -q 'fn main.*Result' src/main.rs
echo 'PASS'

echo '--- 6. No unwrap/expect in production code ---'
! grep -rn 'unwrap()\|expect(' src/ | grep -v '#\[test\]\|#\[cfg(test)\]'
echo 'PASS'

echo '--- 7. Test fixtures exist ---'
test -f fixtures/valid.toml
test -f fixtures/invalid.toml
echo 'PASS'

echo '--- 8. All tests pass ---'
cargo test
echo 'PASS'

echo '--- 9. Clippy clean ---'
cargo clippy -- -D warnings
echo 'PASS'

echo '=== GATE: 9/9 PASS ==='
