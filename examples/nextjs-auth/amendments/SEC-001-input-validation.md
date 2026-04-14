# SEC-001: Input Validation on All Endpoints

**Status:** RATIFIED
**Date:** 2026-04-01
**Trigger:** Code review found unvalidated user input reaching database queries in /api/auth/register

## Binding Text
All API endpoints MUST validate input length, type, and format before processing. Validation MUST occur in middleware, not inline in route handlers.

## Enforcement
**File:** src/middleware/validation.ts
**Line:** Applied via middleware chain in src/routes/

## Gate Check
```bash
# Every route file must import or reference validation
for f in src/routes/*.ts; do
    grep -q 'validateInput\|validation' "$f" || { echo "FAIL: $f missing validation"; exit 1; }
done
```

## Rationale
Unvalidated input reaches database queries, enabling injection attacks. Input validation at the middleware layer ensures every route is covered regardless of individual handler implementation. Without this amendment, new routes can be added without validation and pass code review.
