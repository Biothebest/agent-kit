# agent-kit

One skill library for every coding-agent harness and every OMP profile.

Skills live once in `skills/`. `agent-kit link` symlinks them into each
harness's user skill directory, so a new [OMP](https://github.com/can1357/oh-my-pi)
profile, Codex and Claude Code all start with the same skills, and an edit here
reaches all of them at once. `profile/` holds a baseline for new OMP profiles.

| Harness | Reads | Linked by |
|---|---|---|
| OMP, every profile (including brand-new ones) | `~/.agents/skills` | `agent-kit link --harness agents` |
| Codex CLI / IDE | `~/.agents/skills` | same link |
| Claude Code | `~/.claude/skills` | `agent-kit link --harness claude` |

OMP keeps each `--profile` isolated: its settings, extensions, managed skills and
plugins live under `~/.omp/profiles/<name>/agent`. `~/.agents/skills` is one of the
few roots every profile reads without configuration, which is why the kit uses it.

## Install

```bash
git clone https://github.com/Biothebest/agent-kit.git ~/agent-kit
cd ~/agent-kit
./agent-kit link                  # all harnesses
./agent-kit profile init work     # optional: baseline for a new OMP profile
omp --profile work
```

Python 3.9+ standard library only. macOS and Linux (symlinks).

## Commands

| Command | Effect |
|---|---|
| `link [--harness agents\|claude]` | Symlink every valid kit skill into the harness directory. Unchanged links are left alone, kit links aimed at the wrong kit skill are repaired, links to skills removed from the kit are pruned. Any other entry with a skill's name, including a dangling symlink, is reported as a conflict and never replaced. |
| `unlink [--harness ...]` | Remove only symlinks that point into this kit. |
| `profile init <name>` | Create `~/.omp/profiles/<name>/agent/` (or `~/.omp/agent` for `default`) and copy any missing `profile/` file. Existing files are kept. |
| `doctor [--omp-profile NAME] [--cwd DIR]` | Validate skills, count links per harness, list each OMP profile's missing baseline files. With `--omp-profile`, ask OMP to resolve every kit skill in that profile: a missing skill fails; a skill shadowed by a higher-precedence same-named skill is reported. |
| `audit [--pre-push]` | Scan every publishable path, symlink target and file, plus every commit reachable from `HEAD` (author, message, tree). `--pre-push` reads git's pre-push ref updates on stdin and scans only the outgoing commits. Non-UTF-8 files count as findings. Exits non-zero on any finding. |

`link` refuses to run while any skill violates the
[Agent Skills specification](https://agentskills.io/specification): `name` must
match the directory, frontmatter keys are limited to `name`, `description`,
`license`, `compatibility`, `metadata` and `allowed-tools`.

## Profile baseline

`profile/config.yml` sets interface and task defaults and leaves model roles to
`/model`. `profile/models.yml` declares a local Ollama provider (Gemma chat and
EmbeddingGemma embeddings); delete entries you have not pulled. `profile/lsp.json`
widens LSP root markers so single files get language servers.

Credentials are never copied: log in once per profile with `omp --profile <name>`.

## Skills

| Skill | Use | Origin |
|---|---|---|
| `blast-radius` | Prove what a change could break outside its diff | cursor/plugins pstack (MIT) |
| `unslop` | Tighten prose without changing meaning | cursor/plugins pstack (MIT) |
| `task-contract` | Make scope, sources, acceptance and continuation explicit | original |
| `controlled-explanation` | Simpler or STE-inspired technical explanations | original |
| `diagram-explanation` | Explain flows and relationships as diagrams | original |
| `interactive-explanation` | Self-contained interactive HTML explainers | original |
| `grill-me` | Stress-test a plan through structured interview | mattpocock/skills (MIT) |
| `teach` | Multi-session course in a teaching workspace | mattpocock/skills (MIT) |
| `local-embeddinggemma` | Local embeddings and semantic search via Ollama | original |
| `local-whisper-transcribe` | Offline transcription with mlx-whisper on Apple silicon | original |
| `frontend-design` | Original composition or focal treatment for a web surface | anthropics/skills (Apache-2.0) |
| `impeccable` | Critique, polish, bolder, quieter, distill or delight pass | pbakaus/impeccable (Apache-2.0) |
| `better-ui` | Component surfaces, nested geometry, icons, state transitions | jakubkrehel/skills (MIT) |
| `better-layout` | Grouping, alignment, spacing, responsive recomposition | jakubkrehel/skills (MIT) |
| `better-typography` | Type hierarchy, measure, numerals, wrapping | jakubkrehel/skills (MIT) |
| `better-colors` | Semantic color, contrast, dark mode, forced colors | jakubkrehel/skills (MIT) |
| `better-accessibility` | Keyboard, focus, semantics, target size, reflow | jakubkrehel/skills (MIT) |
| `emil-design-eng` | Purposeful transitions, gestures, transient feedback | emilkowalski/skills (MIT) |
| `fixing-motion-performance` | Measured animation jank fixes | ibelick/ui-skills (MIT) |
| `web-design-guidelines` | Forms, focus, navigation, loading-state review | independently worded; checklist MIT (vercel-labs) |

Adapted skills keep their upstream license file and a provenance section naming
the exact upstream commit; each is modified from that upstream and is not an
upstream distribution or endorsement.

## Adding a skill

1. Create `skills/<name>/SKILL.md` with spec frontmatter. Put upstream terms in a
   `LICENSE*` file beside it and the upstream URL in `metadata.source`.
2. `python3 -m unittest discover tests` checks every shipped skill against the spec.
3. `./agent-kit link` exposes it everywhere; `./agent-kit doctor --omp-profile <name>`
   confirms OMP resolves it to this kit.

Codex-only display and invocation policy goes in `skills/<name>/agents/openai.yaml`.

## Publishing safety

`.githooks/pre-push` runs `agent-kit audit --pre-push`, so a push is refused while
any outgoing commit carries a leak, even if the working tree is already clean.
Enable it once per clone with `git config core.hooksPath .githooks`. Besides generic
patterns (home paths, non-noreply email addresses, private keys, common token
formats) it reads one regular expression per line from
`~/.config/agent-kit/private-terms.txt`, or the file named by
`AGENT_KIT_PRIVATE_TERMS`. That file stays on your machine; list the employer,
client and product names that must never appear here.

## License

Original content: MIT (see `LICENSE`). Adapted skills: the license file in each
skill directory.
