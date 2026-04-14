# Session Continuity

## The Problem

AI chat sessions are ephemeral. When a session ends, the context is gone. The next session starts from zero — the AI has no memory of what was built, what was decided, or what failed.

For small tasks this does not matter. For multi-session projects — anything that takes more than one sitting — context loss is the primary failure mode. The AI repeats mistakes, contradicts earlier decisions, and re-investigates solved problems.

## Context Dumps

A context dump is a structured markdown file that captures the full project state at the end of a session. The next session starts by ingesting this file. The AI reads it and resumes with full context.

A context dump contains:

- **What was done** — bullet list of completed work
- **Current state** — table of components and their status
- **Metrics** — test count, LOC, dependencies, build status
- **Pending actions** — prioritized list of what comes next
- **Key decisions** — decisions made this session and their rationale
- **Key learnings** — discoveries that affect future work (bugs found, patterns that failed, performance characteristics)
- **How to resume** — exact instructions for the next session

## For Long Projects

Projects spanning many sessions benefit from persistent tracking files:

- **STATE.md** — current project state, updated every session. Always reflects the latest metrics and component status.
- **DECISIONS.md** — append-only decision log. Each entry: date, context, decision, rationale, status. Never edit old entries.
- **Per-session context dumps** — one file per session, archived chronologically.

The next session reads STATE.md and DECISIONS.md first, then the most recent context dump for detailed resumption context.

## Key Principles

Context dumps are internal documents. They are detailed and unpolished. Their purpose is continuity, not presentation. Include raw command output, exact file paths, and specific line numbers. The more precise the dump, the faster the next session resumes.

Write context dumps as if explaining to a competent developer who has never seen the project. Avoid pronouns that reference prior conversation ("as we discussed"). State facts directly.

## Template

Use `templates/context-dump-template.md` to create session context dumps. Fill in every section — incomplete dumps lead to incomplete resumption.
