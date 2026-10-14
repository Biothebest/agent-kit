# Debugging

Read this before changing code for a bug, a flaky test, a failed gate, or behavior nobody can explain. Skip it for a feature, a refactor, or a fix whose cause is already observed; a loop built for a known one-line cause is ceremony.

Method adapted in new words from `diagnosing-bugs` in mattpocock/skills at `d81f3a183412e71a5b1e84ca21bc1a35eea03a60` (MIT, see `../LICENSE.mattpocock`). The redaction, delegation and stop rules are additions.

## 1. Build the loop before any theory

A loop is one named command you have run once and that fails because of this bug. It is the bug's receipt and the only thing that can later prove the fix. Write no hypothesis until it exists. Use the cheapest rung that reproduces the failure:

1. A focused failing test at the narrowest module that shows it.
2. A request through the real local route with a test client.
3. A sanitized fixture or captured provider payload replayed through the real parser or serializer.
4. For a real-time path (streaming, telephony, sockets), a synthetic local session or a disposable loopback server with external connections refused.
5. For browser-only behavior, a scripted run in a real browser.
6. A throwaway harness around the narrowest suspect, `git bisect run` over history, or the same input through old and new code.
7. A human-run script, only when nothing above can reproduce it.

Never build the loop from real personal data, live credentials or a paid provider call. Replay sanitized captures instead.

A flaky bug needs a higher failure rate before analysis: repeat the loop, add load, seed randomness, and pin or inject the clock. A 50% flake can be debugged; a 1% flake cannot.

Before choosing a rung, ask whether the inputs changed since the last pass. A gate, audit or test that fails with unchanged code and lockfile points at external state: advisory feeds, registries, clocks, quotas, expired credentials. Compare timestamps against the last green run and rerun the same command on the last green revision before touching code.

## 2. Minimize

Remove inputs, fields, steps and setup until every remaining element is load-bearing. A removal that keeps the failure is progress; one that loses it names a cause candidate.

## 3. Rank hypotheses, then probe one variable

Write three to five falsifiable hypotheses, most likely first, each as "if X is the cause, changing Y produces Z". Keep them in working notes or the worker report; do not block on the user unless a probe has an external side effect. Change one variable per probe. After three refuted hypotheses, re-check the loop and the minimization before ranking new ones.

## 4. Instrument and clean up

Tag every temporary log or print `[DEBUG-<4 hex>]` so cleanup is one search. Logs, captured payloads and notes never contain secrets, recorded speech, phone numbers or email addresses; redact or hash at capture. Before the fix is committed, `git grep -E '\[DEBUG-[0-9A-Fa-f]{4}\]'` returns nothing and scratch files are gone.

## 5. Fix at the right seam

Write the regression test first and confirm it fails for the intended reason. If the bug only appears across several modules and no honest seam expresses it, say so in the report instead of writing a test that does not exercise it.

## Delegated bug fixes

The brief's `TEST` field is the red loop command from step 1, not a description of one. The worker's `REPORT` carries the loop receipts before and after, the confirmed cause, and the hypotheses it refuted.

## Output

State the confirmed cause, the loop receipt before and after the fix, the refuted hypotheses, and the regression test or the reason no seam exists. When no loop could be built after the whole ladder, report the bug `UNPROVEN` with what was tried, and do not present a speculative change as a root-cause fix.
