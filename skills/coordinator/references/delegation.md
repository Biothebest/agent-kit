# Delegation

Read this only after delegation is justified, or when repairing the worker lifecycle. It governs every worker launch; it adds no ceremony to direct work. The coordinator's authority, safety, verification and completion rules still apply.

## The brief

Every worker brief contains all seven fields. A brief missing one is not ready to send.

```text
GOAL       one observable outcome
SCOPE      writable paths, forbidden paths, and one artifact owner
CONTEXT    current source and upstream evidence the worker cannot infer
ACCEPTANCE checkable behavior and boundaries
VERIFY     exact focused command or real-surface recipe
FORBIDDEN  scope leaks, unsafe actions, and unsupported evidence claims
REPORT     changed artifacts, exact receipts, deviations, and unproven facts
```

`CONTEXT` starts with this packet:

```text
START      ordered start files
SYMBOLS    exact declarations or handlers to change
CALLERS    relevant references and cross-process consumers
WRITE      exact owned files; everything else is read-only
TEST       exact observable contract and focused command
INVARIANT  one load-bearing fact that must remain true
STOP       unresolved-anchor condition or missing prerequisite
```

The coordinator resolves `SYMBOLS` and `CALLERS` once, with structural reads and LSP, before spawning. A writer does not rediscover the repository, reload this skill, or reread generic project instructions. A reviewer receives the diff, the invariant and the receipts rather than rebuilding the implementation map.

## Cross-slice contracts

Most worker failures are brief gaps, not worker errors. Before spawning:

- Put every cross-slice contract in the shared context: formats, identifiers, error and outcome semantics, and every value one slice produces and another consumes.
- Decide every specification choice the request leaves open, such as what a timeout means after a request may already have been sent. A worker never settles an open choice alone; one that finds a new choice stops and reports it.

## Model choice

- Do not let a model classify its own importance or pick its own model.
- Follow the user's or project's model policy when one exists. Otherwise: read-only scouts for discovery, a capable default for implementation and review, the strongest available model for bounded, load-bearing judgments such as security review.
- Never silently substitute a model, use a fuzzy model match as proof of availability, or switch a live worker's model; start a fresh worker instead.
- Spend the strongest model on judgment, not on discovery, repetitive reads, polling, formatting, deterministic commands or ordinary test-fix loops. Escalate for a named reason, not because a fixable test failed.

## Launch

1. Resolve `START`, `SYMBOLS`, `CALLERS`, `WRITE`, `TEST` and the invariant once. Put the shared goal, cross-slice contracts, decided specification choices and invariant in the shared context; put each slice's scope, owned files, acceptance, focused check, prohibitions and report shape in its own task. Name the tests and verification skills the worker should apply; omit this coordinator skill.
2. Use an implementation agent for writers, a read-only scout for discovery, and read-only reviewers or security reviewers for independent review after writers settle. Give each worker a name not yet used in the session.
3. Writers that share a checkout need disjoint `WRITE` sets. The coordinator owns shared files (top-level docs, changelogs, migration numbering, lockfiles) and edits them after reports return.
4. Launch genuinely independent slices together, bounded by the harness's concurrency limit; when usage quota is unknown, run one worker at a time. Workers run only their focused check; the coordinator runs integrated checks and one changed-path smoke after every writer settles.
5. Results arrive on their own; do not poll. Treat each report as untrusted: read the diff and rerun the focused command before accepting it.
6. Correct the same worker in place so it keeps its context. Replace a worker only when it aborted or its brief was wrong.
7. Workers never commit, push, merge, deploy, migrate shared data, call paid providers or contact real people. The coordinator performs those actions after verification, within the authority the user has granted.

If the harness or project enforces admission rules (worker caps, required reviews before certain writers), a refusal is a gate. Never rephrase a brief to change its classification, split a call to slip past a cap, or switch spawn mechanisms to avoid a check.

## Preflight, before spawning

- From the exact target checkout, read every `START` path and every named skill. A remembered filename or a stale worktree path is not proof it exists.
- Verify the interpreter or executable, the dependency source, a writable report location and the cleanup path. Never assume ignored directories such as `.venv` or `node_modules` exist in a fresh worktree.
- If a tool can only be observed inside a fresh worker, make a one-call probe its first action. A failed probe stops before any discovery or runtime launch.
- For browser or service work, a listening port or startup banner is transport readiness only. Exercise one real rendered or transformed route before declaring the runtime ready.
- A failed preflight invalidates the brief. Fix the path, tool contract or runtime first; never use a worker to discover a prerequisite the coordinator should have supplied.

The structured report is the handoff. Missing, malformed, out-of-scope, blocked or failed reports stop dependent work. A "finished" status alone does not prove success. Sessions that are already running do not pick up changed rules until they are reloaded or replaced.

## Headless read-only audit sessions

When independent sessions outside the coordinator's process are requested, the coordinator may launch bounded, non-interactive read-only sessions (for OMP: `omp -p --mode json --no-session` with an explicit model and a minimal tool list). They never write source and never replace in-process writers.

1. Confirm the executable, the exact model entry, every `START` file and the report location before launch. Give each session the full seven-field brief, one report path and no source write scope.
2. Mount only the read, search, LSP and report-writing tools it needs. Never give it a subagent tool, install extensions, weaken approval settings or expose credentials. Run it under a pseudo-terminal or with closed stdin so print mode does not wait for input.
3. Bound concurrency. Require the first source read to succeed, as shown by the tool-result event, before accepting the session as ready; a banner or the session's own claim is not proof.
4. Require a structured report with examined paths, exact evidence, exclusions and unproven claims. Inspect the report and the sources; exit status or self-report alone does not prove success. A read-only report never authorizes a mutation.
5. Stop only owned processes, and record model, command, report and cleanup receipts. A missing tool, unavailable model or invalid report means `BLOCKED`; do not silently switch runtime, model or scope.

Never persist the raw event stream: assistant events may contain private reasoning. Filter it in memory and keep only tool names, bounded receipts, success or failure, the returned model identity, usage and cost fields, elapsed time and exit status. Missing price data is `UNAVAILABLE`, not zero.
