# Philosophy

## The Collapse Problem

When a developer opens an AI coding tool, they get one agent that simultaneously designs architecture, writes code, reviews its own output, and decides what to build next. Every role collapses into a single chat window.

In human teams, this never happens. The architect does not write production code. The developer does not set system architecture. The security reviewer does not ship their own fixes. These boundaries exist because combining roles creates blind spots — the person who designed a system cannot objectively evaluate it.

AI collapses all of these into one context window. The same model that chose the architecture implements it, then reviews it, then declares it correct. The result is predictable: wrong assumptions propagate unchecked, scope creeps silently, and quality depends entirely on the model's self-assessment.

## Separation of Concerns

HAIG restores role separation for AI-assisted development. Four distinct roles — Authority, Architect, Auditor, Executor — each with explicit boundaries on what they can and cannot do.

The Architect designs but cannot execute. The Executor implements but cannot redesign. The Auditor attacks but cannot fix. The human Authority ratifies everything.

This is not bureaucracy. It is the same separation of concerns that makes modular code reliable, applied to the development process itself.

## Enforcement Over Suggestion

The default approach to AI governance is behavioral prompting: write instructions that tell the AI how to behave. "Be careful with security." "Don't overcomplicate things." "Follow best practices."

These instructions have no enforcement mechanism. The AI processes them as soft preferences, not hard constraints. There is no feedback loop — if the AI ignores the instruction, nothing happens.

HAIG replaces behavioral prompts with gate checks: bash scripts that define pass/fail criteria for every chunk of work. The gate runs after implementation. If it fails, the work is not done. The AI cannot argue with `grep`. Either the code contains the required pattern or it does not.

## The Human Remains Sovereign

AI proposes. The human disposes. Every design requires ratification. Every amendment requires approval. Every final deliverable requires acceptance. No AI role can override the human Authority.

The goal is not to slow down AI — it is to make AI output verifiable. HAIG lets you move fast with confidence, because every claim the AI makes is backed by an automated check that you can read, understand, and run yourself.
