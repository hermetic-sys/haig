# DISPATCH-001: TOML Config Parser

## Goal
Build a TOML configuration file parser with validation, error handling, and CLI integration.

## Prerequisites
- Rust project initialized with `cargo init`
- `serde`, `toml`, `clap` in Cargo.toml

## Files
| File | Action | LOC | Purpose |
|------|--------|-----|---------|
| src/config.rs | CREATE | ~80 | Config struct + deserialization + validation |
| src/error.rs | CREATE | ~40 | Error types with Display + Error impl |
| src/main.rs | MODIFY | ~30 | CLI integration with --config flag |
| tests/config_test.rs | CREATE | ~60 | Config parsing and validation tests |
| fixtures/valid.toml | CREATE | ~10 | Test fixture: valid config |
| fixtures/invalid.toml | CREATE | ~5 | Test fixture: missing required fields |

## Chunk 1: Config Struct + Deserialization

### Goal
Define the Config struct with serde and implement TOML deserialization with proper error handling.

### Implementation
1. Create `src/error.rs` with:
   - `enum ConfigError` with variants: `IoError(std::io::Error)`, `ParseError(toml::de::Error)`, `ValidationError(String)`
   - Implement `std::fmt::Display` and `std::error::Error` for ConfigError
   - Implement `From<std::io::Error>` and `From<toml::de::Error>`
2. Create `src/config.rs` with:
   - `struct Config` with fields: `name: String`, `version: String`, `port: u16`, `database_url: String`, `log_level: Option<String>`
   - Derive `serde::Deserialize` and `Debug`
   - `pub fn load(path: &Path) -> Result<Config, ConfigError>` — read file, parse TOML, return Config
3. All error paths return `Result` — no `unwrap()` or `expect()`

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 1 GATE ==='

echo '--- 1. Config struct exists ---'
grep -q 'pub struct Config' src/config.rs
echo 'PASS'

echo '--- 2. Error type exists with Display ---'
grep -q 'enum ConfigError' src/error.rs
grep -q 'impl.*Display.*ConfigError' src/error.rs
echo 'PASS'

echo '--- 3. No unwrap/expect in src/ ---'
! grep -rn 'unwrap()\|expect(' src/ | grep -v '#\[test\]\|#\[cfg(test)\]'
echo 'PASS'

echo '--- 4. Compiles ---'
cargo check
echo 'PASS'

echo 'GATE: 4/4 PASS'
```

## Chunk 2: Validation + Error Handling

### Goal
Add config validation rules and comprehensive error handling.

### Implementation
1. Add `pub fn validate(&self) -> Result<(), ConfigError>` to Config:
   - Port must be > 0 and < 65536
   - Name must not be empty
   - Database URL must start with "postgres://" or "sqlite://"
   - Log level, if present, must be one of: "debug", "info", "warn", "error"
2. Update `load()` to call `validate()` after deserialization
3. Create test fixtures:
   - `fixtures/valid.toml` — all required fields, valid values
   - `fixtures/invalid.toml` — missing required field (database_url)

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 2 GATE ==='

echo '--- 1. Validate function exists ---'
grep -q 'fn validate' src/config.rs
echo 'PASS'

echo '--- 2. No unwrap/expect in src/ ---'
! grep -rn 'unwrap()\|expect(' src/ | grep -v '#\[test\]\|#\[cfg(test)\]'
echo 'PASS'

echo '--- 3. Fixtures exist ---'
test -f fixtures/valid.toml
test -f fixtures/invalid.toml
echo 'PASS'

echo '--- 4. Clippy clean ---'
cargo clippy -- -D warnings
echo 'PASS'

echo 'GATE: 4/4 PASS'
```

## Chunk 3: CLI Integration + Tests

### Goal
Add `--config` CLI flag and comprehensive tests.

### Implementation
1. Update `src/main.rs`:
   - Add clap `--config` argument with default value "config.toml"
   - `fn main() -> Result<(), Box<dyn std::error::Error>>` — no `unwrap()` in main
   - Load config, print parsed values, exit 0 on success
2. Create `tests/config_test.rs` with:
   - Test: valid config parses successfully
   - Test: missing file returns IoError
   - Test: invalid TOML returns ParseError
   - Test: missing required field returns ValidationError
   - Test: invalid port returns ValidationError
   - Test: invalid log level returns ValidationError

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 3 GATE ==='

echo '--- 1. CLI --config flag ---'
grep -q 'config' src/main.rs
echo 'PASS'

echo '--- 2. main returns Result ---'
grep -q 'fn main.*Result' src/main.rs
echo 'PASS'

echo '--- 3. No unwrap/expect in src/ ---'
! grep -rn 'unwrap()\|expect(' src/ | grep -v '#\[test\]\|#\[cfg(test)\]'
echo 'PASS'

echo '--- 4. Tests exist ---'
test -f tests/config_test.rs
echo 'PASS'

echo '--- 5. All tests pass ---'
cargo test
echo 'PASS'

echo '--- 6. Clippy clean ---'
cargo clippy -- -D warnings
echo 'PASS'

echo 'GATE: 6/6 PASS'
```

## Rules
- All error paths must use `Result` — no panics in production code
- `cargo clippy -- -D warnings` must pass after every chunk
- Match existing Rust idioms (? operator, From impls, enum error types)

## Prohibitions
- Do NOT use `unwrap()` or `expect()` outside test code
- Do NOT add serde_json, serde_yaml, or other config formats — TOML only
- Do NOT add async/tokio — this is a synchronous CLI tool
- Do NOT add logging frameworks — use eprintln for errors in this dispatch
