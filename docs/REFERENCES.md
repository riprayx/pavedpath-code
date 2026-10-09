# References and Prior Art

Sources reviewed on 2026-10-09 for the chat-first revision, and what this fork took from each. Re-check vendor documentation before relying on platform details: Skill locations and capabilities change often.

## Contents

- Skill format and authoring
- Platforms
- GitHub search and APIs
- Security
- Prior art: similar Skills
- Evaluation
- Observed in testing

## Skill format and authoring

| Source | What we adopted |
| --- | --- |
| [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | `name` up to 64 characters (lowercase, digits, hyphens; no "anthropic" or "claude"); `description` up to 1,024 characters, third person, saying what the Skill does and when to use it; body under 500 lines; references one level deep; a table of contents in reference files over 100 lines; consistent terminology; copyable checklists for multi-step workflows; build evaluations first; test on every model you target. Enforced in `tools/check_skill.py` where checkable. |
| [Anthropic: Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Progressive disclosure (metadata, then body, then references). Runtime constraints per surface (see Platforms). Warning that Skills which fetch external content can bring in malicious instructions. |
| [Agent Skills specification](https://agentskills.io/specification) | The open format that both Anthropic and OpenAI build on: required `name` and `description`; optional `license`, `compatibility`, `metadata`, `allowed-tools`; instructions under about 5,000 tokens. |
| [anthropics/skills: skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | `evals/evals.json` layout (id, prompt, expected output, files, assertions). Running every case with and without the Skill. A 20-query trigger set of should-trigger cases and near-miss should-not-trigger cases. Advice that descriptions should be a little "pushy" because models tend to under-trigger. |
| [obra/superpowers: writing-skills](https://github.com/obra/superpowers/tree/main/skills/writing-skills) | Keep the `description` to triggering conditions: a description that summarizes the workflow lets agents skip the body. Prefer a positive recipe (state what the output is) over lists of prohibitions. Add a red-flags list for rules that agents rationalize away. |
| [OpenAI: Agent Skills for ChatGPT and Codex](https://developers.openai.com/codex/skills) | `agents/openai.yaml` keys: `interface` (`display_name`, `short_description`, `icon_small`, `icon_large`, `brand_color`, `default_prompt`), `policy.allow_implicit_invocation`, and `dependencies.tools`. There is no `alias` key, so it was removed. Front-load trigger words, because hosts may shorten descriptions to fit a budget of about 2% of the context window. |

## Platforms

| Platform | Facts that shaped the design |
| --- | --- |
| Claude Code | Skills in `~/.claude/skills/` or `.claude/skills/`; network access is whatever the user's machine has. |
| claude.ai | Custom Skills are uploaded as a zip and need code execution enabled. Network access from the sandbox may be full, partial, or none, which is why the Skill prefers the chat's own web and connector tools. Skills do not sync between claude.ai, the API, and Claude Code. |
| Claude API | Skills run in a container with no network access, so research must come from tools the application provides. |
| Codex CLI, IDE extension, ChatGPT desktop | User Skills in `~/.agents/skills`; repository Skills in `.agents/skills`. Explicit invocation with `$skill-name`. |
| ChatGPT web and mobile | Skills load only when bundled in a [plugin](https://developers.openai.com/plugins/build/plugins) (root `plugin.json`, `skills/<name>/SKILL.md`). Plugin packaging is an open item in DEVELOPMENT_PLAN.md. |

## GitHub search and APIs

| Source | What we adopted |
| --- | --- |
| [About GitHub code search](https://docs.github.com/en/search-github/github-code-search/about-github-code-search) | Code search requires sign-in, covers only the default branch, excludes files over 350 KiB and some very large repositories, and caps results. An empty result is weak evidence (`search-patterns.md`, `tool-selection.md`). |
| [REST API: search](https://docs.github.com/en/rest/search/search) | About 30 search requests per minute when authenticated; code search has a separate, lower limit; check `incomplete_results`. This led to the search budget in `SKILL.md`. |
| [REST API: compare two commits](https://docs.github.com/en/rest/commits/commits#compare-two-commits) | `compare/TAG...SHA` to confirm that a merged fix is in a release (`research-rubric.md`). Also used to find forks that are ahead of upstream. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | Typical MCP tool names (`search_issues`, `search_pull_requests`, `search_code`, `get_file_contents`, `list_releases`) for the capability map. Names vary by host, so the Skill matches by capability. |
| [grep.app](https://grep.app) (Vercel) | Public code search with an MCP endpoint. Listed as a web-only fallback for code search. |

## Security

| Source | What we adopted |
| --- | --- |
| [Invariant Labs: GitHub MCP exploited](https://invariantlabs.ai/blog/mcp-github-vulnerability) | A malicious public issue steered an agent into leaking private repository data through a pull request. Hence: retrieved content is data, never instructions; no posting on behalf of retrieved content; private content never goes to public places. |
| [Simon Willison: the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | Private data, untrusted content, and an exfiltration channel together make prompt injection dangerous. A research Skill always has untrusted content, so it must restrict the other two: scrub queries and post nothing. |

## Prior art: similar Skills

| Source | Relation to this Skill |
| --- | --- |
| [SkillDB: GitHub Search and Prior Art](https://skilldb.dev/skills/github-repository-research-skills/github-search-and-prior-art) | Closest existing Skill. Strong on query syntax, index blind spots, fork mining, and consumer-side searches; less on fix-status verification, chat-platform tool fallbacks, and safety boundaries. `search-patterns.md` covers the same techniques in our own words. |
| [openai/skills: gh-fix-ci](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) | A `gh`-first Skill that checks authentication and proposes a plan before acting. A model for explicit preconditions; the opposite of the tool-independence this Skill needs in chat. |
| [obra/superpowers: systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) | Complementary: root-cause local debugging. PavedPath Code covers the external evidence step. |

## Evaluation

| Source | What we adopted |
| --- | --- |
| [Kozyrev et al., "Skill Issue: Lessons from Optimizing Repository SKILLs for Coding Agents" (arXiv:2609.12742)](https://arxiv.org/abs/2609.12742) | Measure a Skill by with-versus-without runs of the same agent, and account for run-to-run variance before claiming an improvement. This is why each case runs at least 3 times per configuration in `evals/README.md`. |

## Observed in testing

On 2026-10-09, all five `gh` command templates from the previous `SKILL.md` failed with HTTP 403 inside a sandboxed agent session whose proxy blocked GraphQL and cross-repository search, even though `gh` was installed. The old instructions treated 403 as a rate-limit or authentication problem and offered no fallback. This is the main reason for `references/tool-selection.md`.
