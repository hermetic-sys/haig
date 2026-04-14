# Getting Started

A 10-minute walkthrough to apply HAIG to any project. This works for Node, Python, Rust, Go, or any language — the framework is language-agnostic.

## Step 1: Add CLAUDE.md (1 minute)

Copy the HAIG CLAUDE.md to your project root:

```bash
curl -o CLAUDE.md https://raw.githubusercontent.com/hermetic-sys/haig/main/CLAUDE.md
```

This tells the AI coding tool about the four roles and the gate protocol. It is the minimum viable HAIG setup.

## Step 2: Create the governance directory (1 minute)

```bash
mkdir -p .haig/{dispatches,amendments,gates}
```

Or copy the full template set:

```bash
git clone https://github.com/hermetic-sys/haig.git /tmp/haig
cp -r /tmp/haig/templates/ .haig/templates/
```

## Step 3: Write your first amendment (2 minutes)

Pick one rule that matters to your project. Examples:

- "All API routes must have tests"
- "No `console.log` in production code"
- "Every public function must handle errors explicitly"
- "No `unwrap()` in non-test code"

Create `.haig/amendments/PROJ-001-your-rule.md` using the amendment template. Include the gate check — a command that verifies compliance.

## Step 4: Write your first dispatch (3 minutes)

Pick a small feature. Create `.haig/dispatches/001-feature-name.md` using the dispatch template.

Break it into 2-3 chunks. For each chunk, write a gate — a bash script with `set -e` that verifies the chunk is complete. Keep the first dispatch small: one new file, one modified file, a handful of checks.

## Step 5: Execute (2 minutes)

Give the dispatch to the Executor (your AI coding tool). It reads CLAUDE.md, sees the gate protocol, and implements chunk by chunk. After each chunk, it runs the gate.

## Step 6: Run the gate (30 seconds)

```bash
bash .haig/gates/001-feature-gate.sh
```

If it passes, the chunk is done. If it fails, the Executor fixes and reruns.

## Step 7: Adversarial review (1 minute)

Open a separate AI session. Paste your dispatch and the resulting code. Ask: "Find every bug, vulnerability, and incorrect assumption." Any valid finding becomes a new amendment.

## What You Have Now

- A CLAUDE.md that sets role boundaries
- An amendment that encodes a project rule with automated verification
- A dispatch that defines work as a verifiable contract
- A gate that enforces "done" as a boolean, not an opinion

Scale from here: more amendments as you learn, more dispatches as you build, adversarial reviews on critical features. The framework grows with your project.
