---
name: haig
description: Apply HAIG governance to this project. Use when the user asks to create dispatches, amendments, gate checks, context dumps, or any governance artifact. Also use when the user says "dispatch", "amendment", "gate check", "context dump", or references HAIG roles (Authority, Architect, Auditor, Executor).
---

# HAIG Governance Skill

## When to Use
- User asks to create a dispatch, amendment, gate, or context dump
- User references HAIG roles or governance workflow
- User asks for a structured implementation plan with verification

## What to Do
1. Read the relevant template from templates/
2. Fill in project-specific details
3. For dispatches: include per-chunk gates
4. For amendments: include enforcement location and gate check
5. For context dumps: capture all session state

## Templates
- `templates/dispatch-template.md` — Implementation blueprints
- `templates/amendment-template.md` — Binding decisions
- `templates/gate-template.sh` — Verification scripts
- `templates/context-dump-template.md` — Session state capture
- `templates/devops-report-template.md` — Post-execution reports
- `templates/decision-log-template.md` — Decision tracking
