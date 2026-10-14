---
name: unslop
description: Tighten prose without changing facts, intent, uncertainty, citations, commands, or contractual language. Use when the user explicitly asks to unslop or tighten writing, or when editing substantial docs, PR text, or customer-facing copy; not for routine code work or status replies.
license: MIT. LICENSE.pstack has complete terms
metadata:
  source: https://github.com/cursor/plugins/tree/46125561306434d8a1d7745d540d8932ab0cd2a2/pstack/skills/unslop
---

# Unslop

Remove machine-like filler and vague language while preserving the text's exact meaning and evidence. Clarity is the goal. A distinctive voice is useful only when the surface permits it.

## Fidelity contract

Never change:

- Facts, numbers, dates, names, identifiers, citations, or links.
- Requirements, approval gates, security boundaries, legal meaning, or uncertainty.
- Code, commands, file paths, API names, UI labels, error text, or quoted material unless the user asks.
- The document's audience or purpose.

Do not add claims, certainty, opinions, humor, emotion, or personal voice to technical, legal, safety, incident, compliance, or customer-evidence text. If the source lacks evidence, remove or label the claim rather than making it sound convincing.

## Scope

Use a quick pass for a paragraph, message, title, or short description. Read `references/patterns.md` in this skill's directory only for substantial prose, a full document, an explicit deep cleanup, or a disputed edit. This keeps ordinary work fast.

Do not run this skill automatically over routine tool updates, code, tests, generated files, or exact provider/user text.

## Quick pass

1. Lead with the actual conclusion or action.
2. Delete greetings, throat-clearing, repetition, generic conclusions, and words that do no work.
3. Replace vague praise, concern, attribution, and abstraction with a concrete fact, source, mechanism, or number. Delete the sentence when none exists.
4. Prefer the short ordinary word: `use`, `help`, `start`, `stop`, `change`, `delete`.
5. Name the actor and action. Prefer active voice when the actor matters.
6. Split sentences that carry two thoughts or force the reader to backtrack.
7. Use one stable name per concept. Do not cycle through synonyms.
8. Remove formatting tells: decorative emoji, excessive bold, forced groups of three, title-case headings, repeated inline labels, and dash-heavy sentence structure.
9. Keep natural variation in sentence length. Do not turn every sentence into a clipped fragment.
10. Read the result once for factual drift. Restore any qualifier or constraint whose removal changed meaning.

Treat stock AI vocabulary as a diagnostic trigger, especially `groundbreaking`, `pivotal`, `crucial`, `delve`, `enhance`, `evolving landscape`, `showcase`, `tapestry`, `testament`, `underscore`, `vibrant`, and `leverage` used to mean `use`. Keep one only when it is the exact sourced term or the sentence supplies a concrete mechanism.

Example:

```text
Before: It is important to note that our groundbreaking platform leverages numerous tools in order to enhance the evolving landscape.
After: Our platform uses many tools.
```

The removed purpose clause had no concrete target or evidence. Do not replace it with a smoother vague phrase such as `support the evolving landscape`.

## Document pass

Before editing a file, identify its mode:

- Tutorial: learning by doing.
- How-to: steps toward a work goal.
- Reference: facts for lookup.
- Explanation: understanding and rationale.

Do not mix modes merely to make a document look complete. Preserve the existing mode unless the user requested restructuring.

For each section:

1. State what the reader needs to know or do.
2. Keep conditions before the instruction they guard.
3. Use numbered lists only for real sequences and bullets for parallel facts.
4. Keep headings in sentence case and make them identify the section's actual purpose.
5. Make every pronoun point to one obvious noun.
6. Keep proof labels honest. Local, mocked, hosted, and provider evidence are different.

Use the deep pattern catalog only after this structural pass.

## Self-audit

Ask:

- Could this sentence appear unchanged in another project's document? If yes, it may say nothing.
- Did the edit remove a boundary, exception, uncertainty marker, or causal link?
- Did smoother wording make an unproven claim sound proven?
- Did I replace project terminology with a stylish synonym?
- Is any sentence present only to sound complete or polished?

Fix the issue or restore the source wording.

## Output

For an in-chat rewrite, return the revised text without a report unless the user asks for rationale. For a file edit, change only the requested prose and report any sentence left untouched because rewriting would alter technical or legal meaning.

## Provenance

Adapted from [cursor/plugins pstack](https://github.com/cursor/plugins/tree/46125561306434d8a1d7745d540d8932ab0cd2a2/pstack) at `46125561306434d8a1d7745d540d8932ab0cd2a2`; this copy is modified from the upstream and is not an upstream distribution or endorsement. See `LICENSE.pstack` for the upstream license.
