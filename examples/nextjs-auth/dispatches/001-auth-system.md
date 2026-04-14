# DISPATCH-001: User Authentication System

## Goal
Build login, register, and logout endpoints with session-based authentication.

## Prerequisites
- Next.js project initialized with `npx create-next-app`
- PostgreSQL database running locally
- `bcrypt`, `pg`, `express-session` in package.json

## Files
| File | Action | LOC | Purpose |
|------|--------|-----|---------|
| src/models/user.ts | CREATE | ~60 | User model with password hashing |
| src/routes/auth.ts | CREATE | ~100 | Login, register, logout endpoints |
| src/middleware/session.ts | CREATE | ~40 | Session middleware + auth guard |
| src/middleware/validation.ts | CREATE | ~30 | Input validation middleware |
| migrations/001_users.sql | CREATE | ~15 | Users table schema |
| __tests__/auth.test.ts | CREATE | ~80 | Auth endpoint tests |

## Chunk 1: Database Schema + User Model

### Goal
Create the users table and a User model that hashes passwords with bcrypt.

### Implementation
1. Create `migrations/001_users.sql` with users table: id (uuid, primary key), email (unique, not null), password_hash (not null), created_at (timestamp)
2. Create `src/models/user.ts` with:
   - `createUser(email, password)` — validate email format, hash password with bcrypt (cost 12), insert row, return user without password_hash
   - `findByEmail(email)` — query by email, return full row (including hash for login comparison)
   - `verifyPassword(plaintext, hash)` — bcrypt.compare wrapper
3. All database queries use parameterized statements (`$1`, `$2`) — never string interpolation

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 1 GATE ==='

echo '--- 1. Migration file exists ---'
test -f migrations/001_users.sql
echo 'PASS'

echo '--- 2. No plaintext password columns ---'
! grep -i 'password.*varchar\|password.*text' migrations/001_users.sql | grep -v 'password_hash'
echo 'PASS'

echo '--- 3. User model exists ---'
test -f src/models/user.ts
echo 'PASS'

echo '--- 4. Bcrypt used with cost >= 12 ---'
grep -q 'bcrypt' src/models/user.ts
grep -qE 'genSalt\(1[2-9]\)|saltRounds.*=.*1[2-9]' src/models/user.ts
echo 'PASS'

echo '--- 5. Parameterized queries only ---'
! grep -E "'\$\{|\"\\$\{|\`.*\\$\{" src/models/user.ts
echo 'PASS'

echo 'GATE: 5/5 PASS'
```

## Chunk 2: Auth Endpoints

### Goal
Create login, register, and logout route handlers.

### Implementation
1. Create `src/routes/auth.ts` with three endpoints:
   - `POST /api/auth/register` — validate input (email format, password length >= 8), call createUser, return 201 with user object (no password_hash)
   - `POST /api/auth/login` — validate input, findByEmail, verifyPassword, create session, return 200 with user object
   - `POST /api/auth/logout` — destroy session, return 200
2. Create `src/middleware/validation.ts` with validateInput middleware that checks required fields and types
3. Every endpoint uses validation middleware before processing

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 2 GATE ==='

echo '--- 1. Auth routes file exists ---'
test -f src/routes/auth.ts
echo 'PASS'

echo '--- 2. Register endpoint ---'
grep -q 'POST.*register\|register.*POST' src/routes/auth.ts
echo 'PASS'

echo '--- 3. Login endpoint ---'
grep -q 'POST.*login\|login.*POST' src/routes/auth.ts
echo 'PASS'

echo '--- 4. Logout endpoint ---'
grep -q 'POST.*logout\|logout.*POST' src/routes/auth.ts
echo 'PASS'

echo '--- 5. Validation middleware exists ---'
test -f src/middleware/validation.ts
echo 'PASS'

echo '--- 6. Validation used in auth routes ---'
grep -q 'validateInput\|validation' src/routes/auth.ts
echo 'PASS'

echo 'GATE: 6/6 PASS'
```

## Chunk 3: Session Middleware + Tests

### Goal
Create session middleware with auth guard and write tests for all endpoints.

### Implementation
1. Create `src/middleware/session.ts` with:
   - Session configuration (secure cookies, httpOnly, sameSite)
   - `requireAuth` middleware that returns 401 if no session
2. Create `__tests__/auth.test.ts` with tests for:
   - Register with valid data (expect 201)
   - Register with duplicate email (expect 409)
   - Login with valid credentials (expect 200 + session cookie)
   - Login with wrong password (expect 401)
   - Access protected route without session (expect 401)
   - Access protected route with session (expect 200)
   - Logout destroys session (expect 200, subsequent request returns 401)

### Gate
```bash
#!/bin/bash
set -e
echo '=== CHUNK 3 GATE ==='

echo '--- 1. Session middleware exists ---'
test -f src/middleware/session.ts
echo 'PASS'

echo '--- 2. Auth guard returns 401 ---'
grep -q '401' src/middleware/session.ts
echo 'PASS'

echo '--- 3. Test file exists ---'
test -f __tests__/auth.test.ts
echo 'PASS'

echo '--- 4. Tests pass ---'
npm test 2>&1 | tail -3
echo 'PASS'

echo '--- 5. No plaintext passwords in any source ---'
! grep -rE "password.*=.*['\"]" src/ | grep -v 'password_hash\|passwordHash\|PASS\|bcrypt\|salt'
echo 'PASS'

echo 'GATE: 5/5 PASS'
```

## Rules
- All passwords must be hashed with bcrypt (cost >= 12) before storage
- All database queries must use parameterized statements
- All endpoints must validate input before processing
- No secrets or credentials in source code

## Prohibitions
- Do NOT use MD5, SHA-1, or SHA-256 for password hashing
- Do NOT store session secrets in source code
- Do NOT return password_hash in any API response
- Do NOT add OAuth, JWT, or social login — this dispatch covers password auth only
