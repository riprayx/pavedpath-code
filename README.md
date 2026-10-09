# PavedPath Code

**PavedPath Code** is an Agent Skill for software engineering problems. It helps an agent find a path someone already walked (an upstream issue, a merged and released fix, an official example, a maintained library), check that it really applies to the user's versions and environment, and turn it into the smallest verifiable local change.

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827?style=flat-square)](SKILL.md)
[![Validate Skill](https://github.com/riprayx/pavedpath-code/actions/workflows/validate.yml/badge.svg)](.github/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Status:** This is an instruction-only Skill. It is not a search engine, an MCP server, or an autonomous code fixer. It uses whatever research tools the host session provides. Cross-platform behavior is defined by the [evaluation set](evals/README.md), but recorded results are still pending, so treat platform support as **unverified** until results are logged.

This repository is a fork of [Jia-Ethan/pavedpath-code](https://github.com/Jia-Ethan/pavedpath-code).

## What it does

| Step | Behavior |
| --- | --- |
| Frame | Collects the exact error, versions, platform, and recent changes, then picks an evidence mode: error, API usage, or project selection. |
| Choose tools | Uses an authorized GitHub connector or MCP server, the `gh` CLI (with REST fallbacks), or web search, whichever the session actually has. It never requires a specific tool. |
| Search | Uses exact, scrubbed strings. Searches closed issues and merged PRs separately, and knows the search index's blind spots. |
| Reject, then rank | Applies hard gates (version, platform, safety, license) before ranking by fit and evidence tier. Stars only break ties. |
| Confirm fix status | Separates **Proposed**, **Merged**, **Released** (with a version), and **Verified**. It checks that a merged fix actually shipped. |
| Answer | Default shape: conclusion, evidence, change, verification, uncertainty. Longer reports only on request. |
| Stay safe | Treats retrieved content as data, scrubs secrets from queries, and runs nothing from READMEs or issues without approval. |

## Use it for

- Runtime errors, stack traces, failing builds or tests, packaging and deployment failures.
- Dependency and version conflicts, SDK and API integration problems, surprising framework behavior.
- "Is this already reported or fixed upstream?" and "Which release contains the fix?"
- Finding a maintained open-source library, tool, or reference implementation for a specific capability.

Not for non-software research, shopping, creative writing, or local refactors that the codebase already answers.

## Repository layout

```text
SKILL.md                     Core instructions (loaded when the Skill triggers)
references/
  tool-selection.md          Capability map, platform notes, error handling, rate limits
  search-patterns.md         Query recipes, release checks, fork mining, index blind spots
  research-rubric.md         Hard gates, evidence tiers, fix status, repository evaluation
  extraction-playbook.md     Reading order, what to extract, detailed report template
  subagents.md               When and how to delegate research
agents/openai.yaml           Display metadata for ChatGPT and Codex
evals/                       Behavior and trigger evaluations, fixtures, results log
tools/check_skill.py         Validator and zip packager (Python standard library only)
docs/REFERENCES.md           Sources and prior art this fork is based on
```

## Installation

The installable Skill is `SKILL.md`, `references/`, `agents/`, and `LICENSE`. The other files are for maintainers. Skill locations change between releases, so check the vendor documentation linked in [docs/REFERENCES.md](docs/REFERENCES.md) if a path below does not work.

### Claude Code

```bash
git clone https://github.com/riprayx/pavedpath-code.git ~/.claude/skills/pavedpath-code
```

Use `.claude/skills/pavedpath-code` inside a project instead to share it with that project.

### Codex CLI, the IDE extension, and the ChatGPT desktop app

```bash
git clone https://github.com/riprayx/pavedpath-code.git ~/.agents/skills/pavedpath-code
```

Current OpenAI documentation lists `~/.agents/skills` for user Skills and `.agents/skills` in a repository. Older Codex versions used `~/.codex/skills`.

### claude.ai

```bash
python3 tools/check_skill.py --package   # creates dist/pavedpath-code.zip
```

Upload the zip in the Skills section of claude.ai settings. Custom Skills require code execution to be enabled. For research, also enable web search or a GitHub connector: the code sandbox may have limited or no network access.

### ChatGPT on the web and mobile

Standalone Skills are not loaded there. ChatGPT web and mobile load Skills only when they are bundled in a plugin. Plugin packaging is on the [roadmap](DEVELOPMENT_PLAN.md) and is not provided yet.

### Any other agent

Ask the agent to install the Skill:

> Install the Agent Skill from https://github.com/riprayx/pavedpath-code into the active Skills directory for this runtime. Show me the destination path and a backup plan for any existing `pavedpath-code` or `github-solution-research` directory, and wait for my approval before writing. Do not store credentials. Afterwards, confirm that the Skill is discoverable.

### Updating

```bash
git -C <skill-directory> pull --ff-only
```

Coming from `github-solution-research`? See [MIGRATION.md](MIGRATION.md).

## Development

```bash
python3 tools/check_skill.py             # frontmatter limits, body length, links, metadata keys, evals, English-only
python3 tools/check_skill.py --package   # the same checks, then build dist/pavedpath-code.zip
```

CI runs the same command on every push and pull request.

Change behavior by evaluation, not by intuition: add or update a case in [evals/](evals/README.md), run it with and without the Skill, then edit the instructions. Keep `SKILL.md` short, and put detail in `references/`, each file linked directly from `SKILL.md`.

The [development plan](DEVELOPMENT_PLAN.md) tracks what is implemented and what is still open. Repository content is maintained in English.

## Credits and license

Originally created by Jia-Ethan ([upstream repository](https://github.com/Jia-Ethan/pavedpath-code); community: [LINUX DO](https://linux.do/)). Licensed under the [MIT License](LICENSE).
