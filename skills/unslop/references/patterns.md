# Deep unslop pattern catalog

Use this catalog for substantial prose or an explicit deep pass. It is diagnostic, not a reason to rewrite accurate text for style alone.

## Empty content

- **Puffery.** Delete phrases such as `pivotal moment`, `testament to`, `evolving landscape`, and `setting the stage`. State the event and consequence.
- **Promotional adjectives.** Replace `groundbreaking`, `renowned`, `stunning`, or `vibrant` with a measurable or sourced property.
- **Vague attribution.** Replace `experts believe`, `industry reports suggest`, or `critics argue` with the named source and claim. Delete it when no source exists.
- **Formulaic challenge framing.** Replace `despite challenges, the project continues to thrive` with the actual constraint and outcome.
- **Generic conclusion.** Replace `the future looks bright` with the next approved action, or cut it.
- **Name-dropping.** Do not list companies, publications, tools, or models without explaining the relevant evidence.

## Inflated language

- Replace `utilize` with `use`, `facilitate` with `help`, `numerous` with `many`, and `in order to` with `to`.
- Replace fancy forms of `is` or `has`, such as `serves as`, `stands as`, `boasts`, and `features`, when the plain verb is accurate.
- Delete `it is important to note`, `it is worth mentioning`, `needless to say`, and similar throat-clearing.
- Replace abstract technical metaphors with the mechanism. Common offenders include `substrate`, `wedge`, `vector`, `locus`, `nexus`, `bedrock`, `flywheel`, `north star`, `endgame`, `scaffolding`, and `ratchet` when no actual ratchet exists.
- Do not use `leverage` to mean `use`.

## Formulaic sentence shapes

- Replace `not just X, but Y` with the actual point.
- Do not force a list into three items. Use the natural count.
- Avoid false ranges such as `from security to performance` when the endpoints have no meaningful scale.
- Remove superficial trailing participles such as `highlighting`, `ensuring`, `showcasing`, or `fostering` when they merely restate the sentence.
- Avoid mirror sentences that repeat the same contrast in reverse.
- Do not end with a tidy slogan that adds no new fact.

## Naming and precision

- Use one name for each concept. Do not rotate between `record`, `item`, `entry`, and `object` for variety.
- Put `only`, `not`, and other limiting words next to the phrase they modify.
- Repeat the noun when `it`, `this`, `they`, or `which` could refer to more than one thing.
- Break long noun strings into clauses. `Provider callback authorization check` may become `the check that authorizes provider callbacks`.
- Preserve articles when they disambiguate: `the client and the host`, not `the client and host`, when those are separate actors.
- Name the concrete symbol, route, file, command, or field when it carries the meaning.

## Sentence mechanics

- Prefer active voice when the actor matters: `the server validates the tenant`, not `the tenant is validated`.
- Passive voice is correct when the actor is unknown, intentionally irrelevant, or must not be implied.
- Split a sentence that contains two instructions or two independent conclusions.
- Put a condition or warning before the action it governs.
- Cut adverbs that stand in for evidence. Replace `significantly faster` with the measured delta.
- Keep a longer sentence when it carries one coherent thought. Uniformly short prose also sounds generated.

## Formatting tells

- Use sentence-case headings.
- Remove decorative emoji unless the product voice or user requests them.
- Do not bold every noun, acronym, or lead-in.
- Avoid repeated `**Label:** sentence` bullets when ordinary prose or a table is clearer.
- Use a colon before a real list or example, not as a repeated connector in every paragraph.
- Avoid repeated em dashes, parenthetical detours, or hyphen substitutes. Use a period when the second thought stands alone.
- Use numbered lists for order and bullets for parallel items. Do not convert prose into a list merely to look organized.

## Chat and agent tells

- Delete `Of course`, `Certainly`, `Great question`, `You're absolutely right`, `I hope this helps`, and `Let me know if` when they add no task information.
- Do not announce the structure before delivering it: `Let's dive in`, `Here is a comprehensive breakdown`, or `We will explore`.
- Do not claim a `smoking gun` unless the evidence directly isolates the mechanism.
- Do not narrate obvious tool use or congratulate the user.
- State uncertainty once, at the claim it qualifies. Do not blanket the answer in hedges.

## Evidence and safety

- Never unslop away `may`, `appears`, `locally verified`, `mocked`, `unproven`, or another evidence qualifier unless stronger evidence now exists.
- Never turn a recommendation into authorization.
- Never shorten a security, privacy, tenant, approval, provider, or deletion boundary until every protected condition remains explicit.
- Keep exact error text, protocol terms, legal names, and user quotations unchanged unless the task specifically edits them.
- If a sentence is awkward because the underlying decision is unclear, flag the ambiguity. Style cannot repair a missing decision.
