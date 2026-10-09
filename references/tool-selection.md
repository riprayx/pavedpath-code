# Tool Selection

Use this when choosing how to reach GitHub and the web, or when a tool fails.

## Contents

- Pick by capability, not by tool name
- Capability map
- Platform notes
- Handling errors
- Limits and budget

## Pick by capability, not by tool name

Hosts expose GitHub in different ways: an MCP server, a built-in connector, the `gh` CLI, raw HTTP from a sandbox, or only web search and page fetch. Tool names differ between hosts, and so do their scopes. Before searching, check which of these capabilities you actually have:

- search issues and pull requests;
- search code;
- read a file, an issue thread, or a PR (description, comments, diff);
- list releases and tags;
- compare two commits or refs;
- general web search and page fetch.

Choose the option that covers the step in front of you. Mixing sources is fine: for example, use web search to find the issue and a connector to read the PR diff.

Importing this Skill does not grant GitHub access, private-repository access, OAuth scopes, network access, or a terminal. When a capability is missing, use the next option and say what could not be checked.

## Capability map

| Need | GitHub MCP or connector (names vary) | `gh` CLI | REST endpoint (`gh api` or HTTP) | Web only |
| --- | --- | --- | --- | --- |
| Search issues and PRs | `search_issues`, `search_pull_requests` | `gh search issues`, `gh search prs` | `GET /search/issues?q=...` | Web search with `site:github.com` plus the exact error |
| Search code | `search_code` | `gh search code` | `GET /search/code?q=...` (requires authentication) | grep.app, or web search |
| Read an issue or PR | `issue_read`, `pull_request_read` | `gh issue view N --comments`, `gh pr view N` | `GET /repos/O/R/issues/N`, `.../issues/N/comments`, `.../pulls/N`, `.../pulls/N/files` | Fetch the github.com page |
| Read a file | `get_file_contents` | `gh api repos/O/R/contents/PATH?ref=REF` | `GET /repos/O/R/contents/PATH` | Fetch `raw.githubusercontent.com/O/R/REF/PATH` |
| Repository metadata | `search_repositories` | `gh repo view O/R` | `GET /repos/O/R` | Fetch the repository page |
| Releases and tags | `list_releases`, `get_latest_release`, `list_tags` | `gh release list -R O/R`, `gh release view TAG -R O/R` | `GET /repos/O/R/releases`, `GET /repos/O/R/tags` | Fetch `/releases` or the changelog |
| Is a commit in a release? | not usually available | `gh api repos/O/R/compare/TAG...SHA --jq .status` | `GET /repos/O/R/compare/TAG...SHA` | Read the release notes and changelog |

Notes:

- In a test with `gh` 2.89, `gh repo view`, `gh search issues`, and `gh search prs` made GraphQL calls. Some sandboxes and proxies block GraphQL or the search endpoints. Fall back to the REST calls in the same row.
- When listing search results, do not request full issue bodies (`--json body`). Triage on titles, states, and dates, then open the two or three best matches.
- Official documentation sites, package registries (npm, PyPI, crates.io, Maven Central), and security advisory databases (GitHub Advisories, OSV) are first-class evidence. They often date a release more reliably than a GitHub search does.

## Platform notes

Re-check these against current vendor documentation before you rely on them.

- **Claude Code and Codex CLI**: full terminal and network access as configured by the user. `gh` may or may not be installed and authenticated.
- **claude.ai**: custom Skills need code execution enabled. Network access from the code sandbox can be full, partial, or none, depending on user and admin settings. Prefer the chat's own web search, web fetch, and connectors over HTTP calls from the sandbox.
- **Claude API**: Skills run in a container with no network access. External research works only through tools the application provides.
- **ChatGPT**: standalone Skills run in the ChatGPT desktop app, Codex CLI, and the IDE extension. ChatGPT web and mobile load Skills only when they are bundled in a plugin. Research then depends on the connectors and browsing enabled for that chat.

## Handling errors

| Signal | Likely cause | Do this |
| --- | --- | --- |
| 401, or "not authenticated" | No credentials | Continue with public sources. Mention that authenticated search was not available. Never ask for a token in chat. |
| 403 or 429 with `x-ratelimit-remaining: 0` or `retry-after` | Rate limit | Wait for the reset if it is short. Otherwise cut the number of queries and run the most specific ones first. |
| 403 with a policy message (for example "not available", "SAML", "resource not accessible") | The host, organization, or proxy blocks this endpoint | Do not retry and do not run `gh auth login`. Switch to another row of the capability map and report the gap. |
| 404 on a repository you expected to exist | It is private or you lack access, or the name is wrong | Do not conclude that it does not exist. Report it. |
| 422 on a search | The query syntax is too complex or too long | Simplify: fewer qualifiers, shorter phrases. |
| `incomplete_results: true` | The search timed out | Narrow by `repo:`, `org:`, `language:`, or `path:`, and treat the result as partial. |

## Limits and budget

- GitHub's search API allows roughly 30 requests per minute when authenticated. Code search allows about 10 per minute and needs authentication. Check the live headers rather than these numbers.
- Code search covers only the default branch. It skips large files (over about 350 KiB), very large repositories, and most forks. It returns a limited number of results. An empty code search is weak evidence.
- Issue and PR search covers all public repositories but ranks by text match. Add the repository and a version or date range before concluding that nothing exists.
- Budget: about 8 searches, then reassess the framing. Each extra query should test a new hypothesis, not rephrase the previous one.
