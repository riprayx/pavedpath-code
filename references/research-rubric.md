# Evidence Rubric

Use this when deciding which evidence to trust and which candidate to recommend.

## Contents

- Hard gates
- Evidence tiers
- Ranking
- Fix status and how to confirm it
- Repository candidates
- Counting and freshness

## Hard gates

Check these before ranking. A candidate that fails a gate is rejected, not merely scored lower. Mention rejected candidates briefly if the user is likely to find them on their own.

| Gate | Reject when | When unknown |
| --- | --- | --- |
| Version | The fix targets a version range that excludes the user's, and nothing shows it carries over | Say which version you assumed |
| Platform and runtime | It needs an OS, runtime, architecture, or deployment target the user does not have | Ask, or state the assumption |
| Required capability | It depends on a feature, plan tier, permission, or service the user lacks | State the requirement |
| Safety | It disables TLS verification, authentication, sandboxing, or security checks; uses `curl \| sh` from an unknown source; widens permissions broadly; or leaks secrets | Never relax this gate silently |
| License | Its license conflicts with a use the user stated (for example, copyleft code inside proprietary distributed software) | Flag the license; do not reject |
| Maintenance (for adopting a dependency) | The project is archived, or abandoned with unpatched security advisories | Flag it |

## Evidence tiers

| Tier | Examples | How to use it |
| --- | --- | --- |
| **A, confirmed** | Maintainer-confirmed root cause with a merged and released fix; official documentation or official example; a test in the upstream repo that pins the behavior | Recommend directly |
| **B, strong** | A resolved issue on the same version with a fix confirmed by several independent users; a merged but unreleased fix; code in an active project that does exactly this | Recommend with the conditions stated |
| **C, plausible** | A nearby version; an open or unmerged PR; a workaround confirmed by one user; an older example that still compiles | Offer as an option and label it |
| **D, weak** | Speculation in comments; "+1" without details; tutorials that do not reproduce the same failure; unrelated popular repositories; awesome-lists; unattributed AI-generated answers | Do not rely on it |

Combine tiers with problem fit. A tier A fix for a different symptom loses to a tier B fix for the exact error.

## Ranking

Among candidates that pass the gates, order by:

1. **Problem fit**: the same error, API, version class, runtime, and failure mode.
2. **Evidence tier**: A, then B, then C.
3. **Local applicability**: it fits the user's versions, configuration, dependency policy, and risk tolerance.
4. **Adaptation cost**: the smallest change that is still correct wins.
5. **Maturity signals**: stars, forks, release cadence, issue response time. Use these only to break ties.

## Fix status and how to confirm it

| Status | Meaning | Evidence required |
| --- | --- | --- |
| **Proposed** | An open PR, a patch in a comment, a fork commit, or a workaround | A link to it |
| **Merged** | On the default branch, not in a published release | The merged PR, plus the absence of a containing release |
| **Released** | In a published version | The version number, from release notes, a changelog, the registry, or a tag comparison |
| **Verified** | Confirmed in the user's environment | The check that was run and its output |

Confirm that a merged PR shipped:

```bash
# 1. Find the merge commit
gh api repos/OWNER/REPO/pulls/123 --jq '{merged: .merged, sha: .merge_commit_sha, merged_at: .merged_at}'

# 2. Check whether a release tag contains it ("behind" or "identical" means yes; "ahead" or "diverged" means no)
gh api repos/OWNER/REPO/compare/v2.4.0...MERGE_SHA --jq .status

# 3. Find the first release published after the merge
gh api "repos/OWNER/REPO/releases?per_page=20" --jq '.[] | [.tag_name, .published_at] | @tsv'
```

Without API access, read the release notes or `CHANGELOG.md` for the PR number, or check the registry's version history. If you cannot establish a release, say **Merged, release not confirmed**.

Backports can put a fix into an older maintenance branch under a different commit. Check the release notes of the user's release line before telling them to upgrade across a major version.

## Repository candidates

When the user is choosing a library, tool, or reference project, capture for each serious candidate:

- link and one-line description of what it actually provides;
- fit: why it matches the stated need, and what it does not cover;
- license;
- last release date and release cadence;
- maintenance signal: recent maintainer responses to issues, open security advisories, archived status;
- adaptation cost: what must change in the user's code, data, authentication, or deployment;
- the main risk.

Read the README, at least one example, the latest release notes, and open issues about the user's use case before ranking. Stars measure attention, not fit or correctness.

## Counting and freshness

- Count independent sources only. The same issue cross-posted, quoted in a blog, or found by two subagents counts once.
- Use exact metadata (versions, dates, star counts) only when it was read during this session. Label anything older as possibly stale.
- Prefer the newest authoritative statement. A maintainer comment that a workaround is no longer needed outranks the original workaround.
