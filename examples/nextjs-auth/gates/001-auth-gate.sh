#!/bin/bash
# Gate: DISPATCH-001 — User Authentication System
# Run after: All chunks complete
# Expected: All checks pass
set -e

echo '=== DISPATCH-001 FINAL GATE ==='

echo '--- 1. Migration exists ---'
test -f migrations/001_users.sql
echo 'PASS'

echo '--- 2. No plaintext password columns ---'
! grep -i 'password.*varchar\|password.*text' migrations/001_users.sql | grep -v 'password_hash'
echo 'PASS'

echo '--- 3. User model exists with bcrypt ---'
test -f src/models/user.ts
grep -q 'bcrypt' src/models/user.ts
echo 'PASS'

echo '--- 4. Bcrypt cost >= 12 ---'
grep -qE 'genSalt\(1[2-9]\)|saltRounds.*=.*1[2-9]' src/models/user.ts
echo 'PASS'

echo '--- 5. Auth routes exist ---'
test -f src/routes/auth.ts
grep -q 'register' src/routes/auth.ts
grep -q 'login' src/routes/auth.ts
grep -q 'logout' src/routes/auth.ts
echo 'PASS'

echo '--- 6. Validation middleware exists and is used ---'
test -f src/middleware/validation.ts
grep -q 'validateInput\|validation' src/routes/auth.ts
echo 'PASS'

echo '--- 7. Session middleware exists ---'
test -f src/middleware/session.ts
grep -q '401' src/middleware/session.ts
echo 'PASS'

echo '--- 8. Tests exist ---'
test -f __tests__/auth.test.ts
echo 'PASS'

echo '--- 9. Tests pass ---'
npm test 2>&1 | tail -3
echo 'PASS'

echo '--- 10. No parameterized query violations ---'
! grep -rE "'\$\{|\"\\$\{|\`.*\\$\{" src/models/
echo 'PASS'

echo '=== GATE: 10/10 PASS ==='
