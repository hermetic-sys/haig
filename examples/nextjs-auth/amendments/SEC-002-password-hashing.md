# SEC-002: Password Hashing with Bcrypt

**Status:** RATIFIED
**Date:** 2026-04-01
**Trigger:** Architecture review — establishing baseline security for credential storage

## Binding Text
Passwords MUST be stored using bcrypt with a cost factor of at least 12. Plaintext passwords MUST NOT be stored, logged, or returned in any API response. MD5, SHA-1, and SHA-256 MUST NOT be used for password hashing.

## Enforcement
**File:** src/models/user.ts
**Line:** createUser() function — bcrypt.hash() call

## Gate Check
```bash
# Bcrypt used in user model
grep -q 'bcrypt' src/models/user.ts || { echo "FAIL: bcrypt not found in user model"; exit 1; }

# Cost factor >= 12
grep -qE 'genSalt\(1[2-9]\)|saltRounds.*=.*1[2-9]' src/models/user.ts || { echo "FAIL: bcrypt cost < 12"; exit 1; }

# No plaintext password columns in schema
! grep -i 'password.*varchar' migrations/*.sql | grep -v 'password_hash' || { echo "FAIL: plaintext password column"; exit 1; }
```

## Rationale
Weak password hashing (MD5, SHA) is trivially crackable with modern hardware. Bcrypt with cost 12 provides approximately 100ms of computation per hash, making brute-force attacks impractical. The cost factor minimum ensures protection against future hardware improvements.
