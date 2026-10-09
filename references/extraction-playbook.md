# Extraction Playbook

Use this after the search has found candidates. It turns issues, PRs, code, and projects into a local recommendation.

## Contents

- Read in this order
- Extract what matters
- Translate to local work
- Detailed report (only on request)
- Failure modes

## Read in this order

**Errors and regressions**

1. The matching issue thread, end to end, including the last comments.
2. The linked or fixing PR: its description, the diff, and the tests it adds.
3. Release notes or the changelog, to find the first version that contains the fix.
4. Duplicate or follow-up issues that report a regression after the fix.

**API usage and integration**

1. The official documentation for the user's version.
2. The official examples or templates.
3. Tests in the upstream repository that exercise the API.
4. Issues about the same usage, for known edge cases.

**Choosing a project**

1. The README: what it provides, its stated limits, and its license.
2. One example close to the user's need.
3. The latest release notes and open issues about that need.
4. Architecture or source code, only when the project itself is the solution being adopted.

## Extract what matters

For each piece of evidence that will influence the answer, write down:

- **source**: the link and its type (issue, PR, release, docs, code, repository);
- **match**: why it is the same problem, and under which versions and conditions;
- **root cause or pattern**: what actually fails, or what the implementation does;
- **fix status**: Proposed, Merged, Released (with version), or Verified;
- **change**: the patch, configuration, version change, or API usage it implies;
- **risk**: breaking changes, maintainer warnings, security or license concerns;
- **verification**: the test, command, or request that would prove it locally.

## Translate to local work

- **Reuse**: keep the upstream approach, API, or configuration shape where it fits.
- **Adapt**: change only what the user's versions, interfaces, data, authentication, or deployment require.
- **Avoid**: workarounds superseded by a released fix, broad rewrites, unsafe shortcuts, and large verbatim copies.
- **Verify**: one concrete check with an expected result. Prefer the narrowest one: a single test, one request, one build target.

Prefer upgrading to a released fix over carrying a workaround. Prefer a workaround over a fork dependency. When you recommend a workaround, add the condition for removing it later (for example, "remove after upgrading to 3.2").

## Detailed report (only on request)

Use this structure when the user asks for a full write-up, or when subagents were used:

```markdown
## Problem profile
Goal, symptom, versions, environment, constraints.

## Search path
Tools available, queries run, surfaces searched, and what was not reachable.

## Evidence
| Source | Match | Fix status | Applies to | Risk |

## Rejected candidates
Each with the gate it failed or the reason it ranked lower.

## Recommendation
Reuse / adapt / avoid, with the smallest change.

## Verification
Exact check and expected result; what was verified in this session.

## Uncertainty
What remains unconfirmed.
```

## Failure modes

- Treating a similar keyword as a match without checking version, API, and environment.
- Citing the first workaround in a thread when a later comment replaced it.
- Recommending an upgrade to a version that does not exist yet.
- Recommending a workaround when a released fix exists.
- Copying a patch without checking its license and compatibility.
- Rewriting a mature solution instead of adapting its public interface.
- Claiming open-source evidence without a direct link to it.
