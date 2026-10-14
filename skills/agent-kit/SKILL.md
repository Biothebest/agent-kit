---
name: agent-kit
description: Use when creating a new OMP profile, adding or changing a skill that should be available in every profile and harness (OMP, Codex, Claude Code), or when an expected shared skill is missing or shadowed. Covers the agent-kit CLI.
---

# agent-kit

The shared skill library is a git checkout, usually `~/agent-kit`. Its `skills/`
directory is symlinked into `~/.agents/skills` (read by every OMP profile and by
Codex) and `~/.claude/skills` (Claude Code). Editing a skill there changes it for
every harness at once. Locate the checkout with
`dirname "$(dirname "$(readlink ~/.agents/skills/agent-kit)")"` and run commands from its root.

## Tasks

- **New OMP profile:** `./agent-kit profile init <name>`, then `omp --profile <name>`
  and log in. Shared skills need no setup; they already resolve in the new profile.
- **Add a reusable skill:** create `skills/<name>/SKILL.md` with spec frontmatter
  (`name` equal to the directory; only `name`, `description`, `license`,
  `compatibility`, `metadata`, `allowed-tools`). Keep it free of employer, client,
  product, personal and machine-specific details: the repository is public. Put
  project-specific workflow skills in that project's own skill directory instead.
  Then `python3 -m unittest discover -s tests`, `./agent-kit link`.
- **Adapt an upstream skill:** copy its license file beside `SKILL.md`, set
  `metadata.source` to the pinned upstream URL, and add a provenance note that the
  copy is modified.
- **Skill missing or wrong in a profile:** `./agent-kit doctor --omp-profile <name>`.
  `MISSING` means discovery failed; `shadowed` names the higher-precedence file that
  wins (for example a project custom directory). A profile can hide the kit's
  namespaced duplicate with `disabledExtensions: [skill:agents/<name>]`; exact names
  only, globs are not matched.

## Publishing

Commit, then push. The `.githooks/pre-push` audit scans outgoing commits for the
local private-term list and credential shapes and refuses the push on any finding.
Never bypass it with `--no-verify`; remove the leak from the commit instead. If the
hook did not run, enable it with `git config core.hooksPath .githooks`.
