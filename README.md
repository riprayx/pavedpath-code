# PavedPath Code

**PavedPath Code** is an Agent Skill for software engineering problems. It helps an agent find a path someone already walked (an upstream issue, a merged and released fix, an official example, a maintained library), check that it really applies to the user's versions and environment, and turn it into the smallest verifiable local change.

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-111827?style=flat-square)](SKILL.md)
[![Validate Skill](https://github.com/riprayx/pavedpath-code/actions/workflows/validate.yml/badge.svg)](.github/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Status:** Version 1.0.0. This is an instruction-only Skill. It is not a search engine, an MCP server, or an autonomous code fixer. It uses whatever research tools the host session provides. The [evaluation set](evals/README.md) defines the expected behavior, but no platform results have been recorded yet, so treat platform support as **unverified** until they are.

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
tools/check_skill.py         Validator and packager (Python standard library only)
docs/REFERENCES.md           Sources and prior art this fork is based on
DEVELOPMENT_PLAN.md          Status, remaining work, release checklist
CONTRIBUTING.md              Evaluation-first workflow and writing rules
```

## Use it in Claude chat (claude.ai)

1. **Get the package.** Download the `pavedpath-code-packages` artifact from the latest successful CI run and unzip it once to get `pavedpath-code.zip`, or build it yourself with `python3 tools/check_skill.py --package`, which writes `dist/pavedpath-code.zip`. The zip contains one folder, `pavedpath-code/`, with `SKILL.md`, `references/`, and `LICENSE`.
2. **Turn on code execution.** Custom Skills require it. On Free, Pro, and Max plans it is under **Settings > Capabilities** ("Code execution and file creation"). On Team and Enterprise plans, an owner enables it, together with Skills, in the organization settings.
3. **Upload the Skill.** Go to **Customize > Skills**, select **+**, then **Create skill > Upload a skill**, and choose the zip. Make sure the Skill is toggled on.
4. **Give it research tools.** Turn on **web search** in the chat. Optionally connect the **GitHub** integration so that Claude can read issues, pull requests, and code directly. Without either, the Skill says that it could not research and answers from local context only.
5. **Try it.** Start a new chat and paste a real error, for example:
   > my CRA app (react-scripts 4) won't start on node 18: `error:0308010C:digital envelope routines::unsupported`. what's the real fix?

   Claude should load **pavedpath-code**. Expand its reasoning to check. The answer should have the parts conclusion, evidence (with links), change, verify, and uncertainty. To force the Skill, start the message with "Use the pavedpath-code skill".

Skills you enable on claude.ai also sync to Claude Code when it is signed in with the same account (Claude Code v2.1.273 or later).

**Troubleshooting**

| Symptom | Fix |
| --- | --- |
| No Skills section, or Skills greyed out | Code execution is off. See step 2. |
| Upload rejected | The zip must contain the `pavedpath-code/` folder at its root, and the folder name must match `name` in `SKILL.md`. Rebuild it with the packager rather than zipping by hand. If the error mentions the description, shorten `description` in `SKILL.md` to 200 characters or fewer, rebuild, and report it in an issue. The Help Center states a 200-character limit, while the API documentation and the Agent Skills specification allow 1,024. |
| The Skill is not used | Check that the toggle is on, and that the message is about a concrete engineering problem. Name the Skill explicitly to force it. |
| "Could not research" | Web search is off and no GitHub connector is connected. See step 4. |

## Installation in other environments

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

### ChatGPT on the web and mobile

These surfaces load Skills only through plugins. `python3 tools/check_skill.py --package` also builds `dist/pavedpath-code-plugin.zip`: a portable Agent Plugin with `plugin.json` at the root and the Skill under `skills/pavedpath-code/`. Install it from a local marketplace in the ChatGPT desktop app, as described in OpenAI's plugin documentation. This package is **untested**; see the [development plan](DEVELOPMENT_PLAN.md).

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
python3 tools/check_skill.py             # validate
python3 tools/check_skill.py --package   # validate, then build dist/pavedpath-code.zip and dist/pavedpath-code-plugin.zip
```

CI runs the same command on every push and pull request and publishes both zips as a run artifact. See [CONTRIBUTING.md](CONTRIBUTING.md) for the evaluation-first workflow and writing rules, and the [development plan](DEVELOPMENT_PLAN.md) for status and remaining work.

## Credits and license

Originally created by Jia-Ethan ([upstream repository](https://github.com/Jia-Ethan/pavedpath-code); community: [LINUX DO](https://linux.do/)). Licensed under the [MIT License](LICENSE).
