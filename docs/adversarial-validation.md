# Adversarial Validation

## Why

A single AI has blind spots. It cannot find its own wrong assumptions. The model that designed a system will defend that design when asked to review it — confirmation bias is not a human-only problem.

Adversarial validation uses a separate AI — ideally a different model — to attack the Architect's design. The attacker has no stake in the design being correct. Its job is to find every vulnerability, race condition, incorrect assumption, and missing edge case.

## How

1. Export the Architect's design document (the dispatch, the architecture, the amendment set)
2. Open a session with a different model — Gemini, GPT, a separate Claude instance, or any capable model
3. Provide the design document with no additional context about why decisions were made
4. Prompt: "You are a security auditor and adversarial reviewer. Find every vulnerability, race condition, incorrect assumption, and missing edge case in this design. For each finding: severity (critical/high/medium/low), exploit steps, and recommended fix."
5. Collect findings

## Triage Protocol

Findings do NOT go directly to the Executor. The Auditor has no authority to change code.

The flow is:

1. Auditor produces findings
2. Architect triages each finding: valid, invalid, or needs investigation
3. Valid findings are drafted as amendments
4. Authority ratifies which amendments become binding
5. Only then does the Executor implement fixes

This prevents the Auditor from injecting design changes. The Architect filters for technical validity. The Authority filters for project relevance.

## Practical Observations

Different models find different things. In practice:

- One model may find timing side-channels and protocol-level attacks
- Another may find namespace confusion and process-level exploits
- A third may miss the critical bug but produce useful structural analysis

Use at least two models for critical designs. The cost is one additional chat session. The value is catching the class of bug that your primary model cannot see.

## Fresh Context

The Auditor must operate in a fresh context window. It should not have access to the Architect's reasoning, design tradeoffs, or rejected alternatives. These create anchoring effects — the Auditor starts defending the design instead of attacking it.

A separate instance of the same model works if a different model is unavailable. The key is a clean context with no prior design reasoning.

## Context Control

The Auditor's effectiveness depends on what it does and does not see. Context control is not a suggestion — it is the mechanism that makes adversarial review actually adversarial.

**The Auditor receives ONLY:**

- The design document or architecture brief for the feature under review
- The amendment registry (binding rules the design must comply with)
- The specific dispatch being audited

**The Auditor does NOT receive:**

- Executor logs or implementation details
- The Architect's internal analysis, reasoning, or rejected alternatives
- Prior session context dumps
- DevOps reports from previous dispatches

**Why this matters:** If the Auditor sees the Architect's reasoning, it anchors on the same assumptions. The Auditor reads "I chose HMAC-SHA256 because X" and evaluates whether X is reasonable — instead of independently assessing whether HMAC-SHA256 is the right choice at all. The Architect's justification becomes the frame, and the Auditor validates instead of attacking.

The Authority controls what the Auditor sees. The Architect prepares a clean brief for Auditor consumption — the design and its constraints, stripped of the reasoning behind it. The Auditor attacks what was built, not why it was built that way.

Using a different model for the Auditor is recommended but not mandatory. What IS mandatory is context isolation. A same-model Auditor with a clean context is more effective than a different-model Auditor that has been anchored by the Architect's analysis.
