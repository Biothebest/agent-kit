---
name: grill-me
description: "Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases (grill me, grill this)."
---

Source: mattpocock/skills @ c55ee46073ed923f86ce59a5eb3b6d895095d1b7 (skills/productivity/grilling), MIT License, Copyright (c) 2026 Matt Pocock. The "Session discipline" section paraphrases the usage guidance in that repository's docs/productivity/grill-me.md and grilling.md at d81f3a183412e71a5b1e84ca21bc1a35eea03a60.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), find it yourself with read-only lookups; use a sub-agent only when one is available, and never ask the user for anything you could look up. Don't block on it: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Session discipline

- **Passivity is the failure mode.** If the user accepts several recommendations in a row without comment, say so once and ask which of them they would defend to someone who was not here. A plan the agent wrote and the user nodded at has decided nothing.
- **Ungrillable questions.** A question that needs something to react to (how a screen should look or feel, one page or three) cannot be settled by talking. Say so, propose a throwaway prototype, and park that branch instead of rephrasing it.
- **Scope too big.** If the tree keeps widening round after round, stop and propose splitting the work, then grill the pieces separately. Count rounds, not questions; there is no fixed question cap.
- **"I don't know" is an answer.** Record the branch as open and name what would settle it.
- **Recommendations answer the question as worded.** If your recommendation argues against the question, reword the question first so agreeing with you is not a hidden "no".
- **Late conflicts.** If an answer changes a question you already asked in the same round, say so and reopen that branch in the next round.
- **One at a time on request.** If the user asks for one question at a time, switch to that.
