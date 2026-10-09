# Search Patterns

Use this when building queries. The syntax below is GitHub search syntax. It works in the web UI, in `gh search ...` (as the query string), in the REST search API (`q=`), and in most GitHub MCP search tools.

## Contents

- From error message to query
- Issues and pull requests
- Releases and changelogs
- Code and real-world usage
- Repositories
- Forks that already fixed it
- When to stop

## From error message to query

1. Take the most distinctive constant fragment: the exception class plus the message, without values.
2. Remove anything that varies or is sensitive: absolute paths, line numbers, IDs, timestamps, ports, hostnames, user names, and tokens.
3. Quote it as one phrase, and add the package or framework name outside the quotes.
4. Add the version only after a first pass, as a filter or a sort.

Example:

```text
Raw:     Error: connect ECONNREFUSED 10.2.3.4:5432 at /home/alice/app/node_modules/pg/lib/client.js:132
Query:   "connect ECONNREFUSED" pg is:issue
```

## Issues and pull requests

| Goal | Query |
| --- | --- |
| Same error in the upstream repo, any state | `repo:OWNER/REPO "exact message"` |
| Closed issues with an answer | `repo:OWNER/REPO is:issue is:closed "exact message"` |
| A fix merged without an issue | `repo:OWNER/REPO is:pr is:merged "exact message"` or the function or config name |
| Recent activity only | add `updated:>2026-01-01` or sort by updated |
| A widespread problem | add `reactions:>10` or `comments:>5` |
| Users of a library reporting it in their own repos | `"library-name" "exact message" -repo:OWNER/REPO` |
| Maintainer statements | add `commenter:MAINTAINER` or `author:MAINTAINER` |

Read the whole thread before citing it. The accepted fix is often several comments below the first workaround, and later comments may say it regressed.

## Releases and changelogs

- Search release notes for the PR number, the issue number, or the error keyword (`gh release view TAG`, the `/releases` page, `CHANGELOG.md`).
- To check whether a merged commit is in a release, compare the release tag with the merge commit: status `behind` or `identical` means the tag contains it. See research-rubric.md.
- For packages, check the registry's version history too. A GitHub release can exist without a published package, and the other way round.

## Code and real-world usage

| Goal | Query |
| --- | --- |
| Exact API call or config key | `"createClient(" language:typescript` |
| Projects that depend on a library | `path:package.json "\"library-name\":"`, `path:go.mod "github.com/owner/lib"`, `path:pyproject.toml "library-name"` |
| Usage outside the library's own org | add `-org:OWNER` |
| Configuration files only | `path:.github/workflows "action-name"` |
| Tests that pin the behavior | add `path:test` or `path:spec` |

Code search results are ranked by relevance, not by stars or date. Take the repository names from the results and check maintenance separately.

## Repositories

- Describe the capability plus the stack: `"rate limiter" language:go`, `topic:oauth2 language:python`.
- Filter out noise: `archived:false`, `pushed:>2026-01-01`. Forks are excluded from repository search unless you add `fork:true`.
- Use `stars:>N` only to shrink a huge result set, then lower the threshold if the exact need is missing.
- For each candidate, open its README, examples, latest release, and open issues about your use case before ranking it.

## Forks that already fixed it

Use this when upstream is slow or abandoned and the bug is known:

1. List forks sorted by recent pushes: `gh api "repos/OWNER/REPO/forks?sort=newest&per_page=50" --jq '.[] | [.full_name, .pushed_at] | @tsv'`.
2. Keep forks that are ahead of upstream: `gh api repos/OWNER/REPO/compare/main...FORKOWNER:main --jq '{ahead: .ahead_by, behind: .behind_by}'`.
3. Read their commit messages and check for an open PR back to upstream.
4. Prefer applying the specific commit as a patch on a pinned upstream version over depending on the fork. Label the result **Proposed**.

## When to stop

- An empty result is weak evidence. Before concluding that nothing exists, run one control query for a string you know the repository contains.
- If about 8 queries produced nothing usable, reframe: is the error a symptom of a different root cause, or a known message from a dependency one level down?
- Record the queries you ran. They go in the **Uncertainty** part of the answer.
