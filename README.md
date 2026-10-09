# PavedPath Code

**PavedPath Code** is a reusable AI agent Skill for researching software engineering problems through GitHub and open-source evidence. It identifies implementation paths that have already been tried, evaluates whether they fit the user's environment, and recommends the smallest verifiable local adaptation.

[![Reusable Skill](https://img.shields.io/badge/Reusable-Skill-111827?style=flat-square)](SKILL.md)
[![GitHub CLI first](https://img.shields.io/badge/GitHub%20CLI-first-0969da?style=flat-square)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

> **Current status:** This is an instruction-based Skill, not a standalone search engine, autonomous code fixer, or MCP server. Its current research instructions prefer the GitHub CLI. A chat-first, tool-adaptive workflow for ChatGPT Chat and Claude Chat is planned in [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md); the roadmap is not yet implemented.

## Purpose and scope

PavedPath Code helps coding agents avoid reinventing solutions to problems that may already have a documented fix or implementation pattern in GitHub repositories, issues, pull requests, discussions, code examples, tests, and release notes.

Use it for:

- Runtime errors, build failures, failing tests, packaging problems, and deployment failures.
- Dependency conflicts, SDK integration problems, framework behavior, and API usage.
- Feature implementation blockers where a proven example or upstream fix may exist.
- Researching engineering tools or open-source projects for a specific capability.
- Comparing evidence and adapting a proven solution to the constraints of a local codebase.

Do not use it for general life decisions, consumer shopping, creative writing, social-media workflows, study methods, or unrelated broad research. Avoid external searches when the user's codebase already provides the answer or the user has prohibited web research. Do not inspect private repositories without explicit authorization and a bounded scope.

## What the Skill provides

| Capability | Current behavior | Important limitation |
| --- | --- | --- |
| Problem-first investigation | Identifies the symptom, environment, version, constraints, and reproduction path | An incomplete error report may require local inspection |
| GitHub evidence research | Searches repositories, issues, PRs, code, examples, documentation, and releases | The current Skill prefers `gh`; it does not bundle a search engine |
| Repository evaluation | Checks fit, Stars, forks, license, activity, example quality, and adaptation cost | Popularity is not proof that a solution works |
| Evidence ranking | Prioritizes confirmed fixes, released changes, official examples, and reproducible code | A merged PR is not automatically a released fix |
| Conditional subagents | Delegates independent, read-only research only when that adds value | No agent orchestration infrastructure is bundled |
| Local adaptation | Preserves proven patterns and limits changes to necessary local differences | No guarantee of autonomous code changes |
| Verification | Requires a suitable test, build, reproduction, request, or inspection | The agent must actually run a check before claiming success |

## Installation

### Ask an agent to install the Skill

Copy this prompt into a coding agent with access to the required files and tools:

> Install or integrate the reusable Skill from https://github.com/Jia-Ethan/pavedpath-code. Read README.md, SKILL.md, MIGRATION.md, and references/ first. Its scope is software engineering problems, not general-purpose research. Identify the active Skills or instructions directory for the current runtime. Before writing files, show the exact destination and backup plan and wait for my approval. Do not leave both pavedpath-code and the retired github-solution-research active under different directories. Preserve existing customizations, do not store credentials, and verify that the Skill is discoverable after installation.

### Install manually in a terminal-based agent

Use the active Skill directory appropriate for your agent. The following location is an example for Codex:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Jia-Ethan/pavedpath-code.git ~/.codex/skills/pavedpath-code
```

To update an existing Git checkout that has no conflicting local changes:

```bash
git -C ~/.codex/skills/pavedpath-code pull --ff-only
```

The Skill instructions currently prefer GitHub CLI (`gh`) when available. Authentication and installation requirements depend on the selected GitHub access method. Never paste credentials into prompts or documentation.

### ChatGPT Chat and Claude Chat

The project includes an agent-readable `SKILL.md` and ChatGPT metadata in `agents/openai.yaml`. Import the Skill using the feature supported by your chat product and plan, and authorize any needed GitHub tools separately. Support for uploads, connectors, remote MCP, browsing, and file execution depends on the platform and session.

**Important:** Importing a Skill does not grant GitHub access or make a terminal available. The current `gh`-first design is being reconsidered specifically for chat-based use. See the [development plan](DEVELOPMENT_PLAN.md) for proposed tool discovery, fallbacks, and platform tests.

## Research workflow

1. Define the concrete engineering problem and identify constraints.
2. Choose evidence sources: issues and PRs for regressions; code and examples for API usage; repositories for reusable capabilities.
3. Decide whether independent subagents can improve research coverage.
4. Search using precise error messages, API names, versions, configuration keys, and relevant environment details.
5. Compare problem fit, evidence strength, local applicability, actionability, and repository maturity.
6. Read strong matches in detail, including fixes, tests, release status, and warnings.
7. Extract what should be reused, what must change locally, and what should be avoided.
8. Verify with tests, builds, real requests, logs, or appropriate manual checks.

See [the evidence rubric](references/research-rubric.md) and [the extraction playbook](references/extraction-playbook.md) for details.

## GitHub CLI examples

Search repository candidates:

```bash
gh search repos "browser automation agent" --archived=false --sort stars --order desc --limit 10 \
  --json fullName,url,description,stargazersCount,forksCount,language,license,pushedAt,isArchived,openIssuesCount
```

Find matching issues:

```bash
gh search issues '"Cannot find module" "Node.js 22"' --repo owner/repo \
  --sort updated --order desc --limit 10 \
  --json title,url,state,updatedAt,commentsCount,repository,body
```

Inspect merged pull requests:

```bash
gh search prs '"ERR_PACKAGE_PATH_NOT_EXPORTED" vite plugin' --repo owner/repo \
  --merged --sort updated --order desc --limit 10 \
  --json title,url,state,updatedAt,commentsCount,repository,body
```

Read repository metadata:

```bash
gh repo view owner/repo \
  --json nameWithOwner,url,description,stargazerCount,forkCount,licenseInfo,primaryLanguage,pushedAt,repositoryTopics,homepageUrl
```

## Output expectations

When open-source research materially informs a recommendation, provide:

- A short problem profile and relevant environment constraints.
- Direct links to issues, PRs, code, tests, releases, or official documentation.
- A clear reason each evidence item applies, including important version conditions.
- A minimal recommendation: reuse, adapt, avoid, and verify.
- Relevant risks, rejected alternatives, and uncertainty when evidence is weak.

Only include repository comparison tables when choosing among actual projects. Only include a subagent trace when subagents were used. Never substitute a list of links or Star counts for evidence.

## Safety and limits

- Public GitHub content is the default research scope. Private content requires authorization.
- Never put tokens, cookies, credentials, private source, internal context, sensitive logs, or production data into search queries, outputs, saved files, or subagent prompts.
- Cross-check security, payment, authentication, infrastructure, and production operations against current official documentation.
- Prefer public APIs, configuration patterns, examples, and tests over copying large sections of third-party source code. Respect licenses.
- Treat unverified advice as a candidate solution, not a demonstrated fix.

The next development phase proposes explicit safeguards against prompt injection in repository content and secret-bearing search queries.

## Development and maintenance

The [development plan](DEVELOPMENT_PLAN.md) describes a chat-first roadmap for ChatGPT Chat and Claude Chat, including tool-independent research, release-state checks, security hardening, compact answers, regression tests, and English-only project documentation. Planned items must not be represented as shipped features.

The legacy Skill name was `github-solution-research`. See [MIGRATION.md](MIGRATION.md) before changing an existing installation, and preserve customized files before any replacement.

Project documents and Skill metadata are maintained in English.

## Community and license

Community feedback: [LINUX DO](https://linux.do/).

This project is licensed under the [MIT License](LICENSE).
