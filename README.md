# HAIG — Human-AI Integrated Governance

> Stop suggesting behavior. Start enforcing outcomes.

HAIG is a governance framework for AI-assisted software development. It separates concerns into four roles, enforces quality through automated gate checks, and tracks every decision as a ratified amendment.

Built by shipping 50,000 lines of production Rust in 60 days using AI as the execution agent. [hermeticsys.com](https://hermeticsys.com)

---

## The Problem

[Andrej Karpathy observed](https://x.com/karpathy/status/2015883857489522876): LLMs make wrong assumptions, overcomplicate code, and touch things they shouldn't.

The standard fix is a prompt file that says "be careful." This is a speed limit sign. Nobody enforces it. The AI reads it, nods, and does what it was going to do anyway.

HAIG doesn't ask the AI to be careful. It defines what "correct" looks like, automates the check, and blocks the code if the check fails.

## The Four Roles

| Role | Who | Authority | Constraint |
|------|-----|-----------|------------|
| **Authority** | Human | Ratifies all decisions | Cannot be overridden by any AI |
| **Architect** | AI (design) | Designs blueprints, drafts gates | Cannot execute code |
| **Auditor** | AI (adversarial) | Attacks designs, finds gaps | Cannot approve own findings |
| **Executor** | AI (code) | Implements blueprints | Cannot make design decisions |

No role can do another role's job. The Architect cannot run code. The Executor cannot choose architecture. The Auditor cannot ship fixes. The human decides what gets ratified.

## The Pipeline

```
Authority decides what to build
    |
Architect designs blueprint + gate checks
    |
Authority ratifies or rejects
    |
Executor implements chunk by chunk
    |
Gate checks pass or fail (automated)
    |
Auditor attacks the result
    |
Authority accepts final output
```

## Gate Checks: The Core Innovation

Every chunk of work ends with a bash script that defines pass/fail. The AI can't argue with `grep`. Either the code has the thing or it doesn't.

```bash
#!/bin/bash
set -e

echo '--- 1. Auth endpoint exists ---'
grep -r 'POST.*login' src/routes/
echo 'PASS'

echo '--- 2. Passwords use bcrypt ---'
grep -r 'bcrypt\|argon2' src/auth/
echo 'PASS'

echo '--- 3. No plaintext passwords ---'
! grep -r 'password.*varchar' src/schema/
echo 'PASS'

echo '--- 4. Tests pass ---'
npm test 2>&1 | tail -3
echo 'PASS'

echo 'GATE: 4/4 PASS'
```

If the gate fails, the chunk doesn't ship. No exceptions. No "I'll fix it later." The gate is the definition of done.

## Amendments: Decisions That Stick

When a bug is found or a quality rule is established, it becomes a binding amendment:

```markdown
## SEC-003: Input Validation

**Status:** RATIFIED
**Trigger:** Fuzzing found unvalidated input in /api/upload

**Binding:** All endpoints MUST validate input before processing.

**Enforcement:** src/middleware/validation.ts

**Gate:** grep -q 'validateInput' for every route file
```

The amendment is traceable: what triggered it, where it's enforced, how to verify it. This is what separates governance from a style guide.

## Adversarial Validation: Two AIs > One AI

Use a different AI to attack the first AI's work:

1. Export the Architect's design
2. Open a session with a different model (Gemini, GPT, a separate Claude)
3. Prompt: "Find every vulnerability, race condition, and wrong assumption"
4. Findings go to the Architect for triage — NOT directly to the Executor
5. The Authority decides which findings become amendments

In our experience: Claude found timing attacks and missing TTL. Gemini found namespace spoofing and debugger hijacking. GPT missed the critical bug but produced useful analysis. Different models find different things.

## Quick Start

**Option A: Drop-in CLAUDE.md (30 seconds)**

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/hermetic-sys/haig/main/CLAUDE.md
```

**Option B: Full framework (5 minutes)**

```bash
git clone https://github.com/hermetic-sys/haig.git
cp -r haig/templates/ your-project/.haig/
cp haig/CLAUDE.md your-project/
```

Then write your first dispatch using `templates/dispatch-template.md`.

## vs. Behavioral Prompts

| | Behavioral Prompts | HAIG |
|---|---|---|
| Enforcement | "Please be careful" | Bash gate: pass or fail |
| Role separation | One AI does everything | 4 roles, explicit boundaries |
| Adversarial testing | Not mentioned | Dedicated auditor protocol |
| Decision tracking | Lost in chat history | Ratified amendments with enforcement locations |
| Session continuity | Start over each time | Context dump protocol |
| Proven scale | Single-file advice | 50,000 LOC shipped in 60 days |

## Documentation

- [Philosophy](docs/philosophy.md) — Why role separation matters
- [Roles](docs/roles.md) — The four roles defined
- [Dispatch Pipeline](docs/dispatch-pipeline.md) — Blueprint to execution to verification
- [Amendments](docs/amendments.md) — Encoding decisions as binding rules
- [Adversarial Validation](docs/adversarial-validation.md) — Using a second AI to attack the first
- [Session Continuity](docs/session-continuity.md) — Maintaining context across sessions
- [Getting Started](docs/getting-started.md) — 10-minute walkthrough

## Examples

- [Next.js Auth System](examples/nextjs-auth/) — HAIG applied to building authentication
- [Rust CLI Tool](examples/rust-cli/) — HAIG applied to building a config parser

## License

MIT — use HAIG however you want.

Built by [The Hermetic Project](https://hermeticsys.com).
