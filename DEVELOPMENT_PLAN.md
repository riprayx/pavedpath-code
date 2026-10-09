# Development Plan

**Status (2026-10-09):** Version 1.0.0 implements the full chat-first roadmap in instructions, tooling, and packaging. What remains is acceptance: running the evaluation set on real platforms and recording the results. Until those results exist, platform behavior is **unverified**.

## Goal

Help a user research a concrete software engineering problem with whatever GitHub and web tools the current session provides. Find proven fixes and implementations, show why they apply, and report uncertainty accurately. The Skill must work in a chat with no terminal and no repository checkout.

## Principles

- **Keep it simple:** a small, dependable workflow beats an orchestration framework.
- **Measure first:** add instructions, scripts, or services only for failures observed in evaluations.
- **One source of truth:** each rule lives in exactly one file. `SKILL.md` links to every reference directly.
- **Evidence before confidence:** separate what the sources establish from inference.
- **Tool independence:** adapt to available capabilities; never assume a tool exists.
- **Safety by default:** never expose secrets or obey instructions embedded in retrieved content.

## Done in 1.0.0

| Area | Result | Where |
| --- | --- | --- |
| Runtime tool selection | Connector or MCP, `gh` with REST fallbacks, web, or none; error handling that tells rate limits apart from policy blocks | `SKILL.md` step 2, `references/tool-selection.md` |
| Evidence quality | Hard gates before ranking, four evidence tiers, Stars as tie-break only | `SKILL.md` step 4, `references/research-rubric.md` |
| Fix status | Proposed, Merged, Released (with version), Verified, plus commands to confirm a release | `SKILL.md` step 5, `references/research-rubric.md` |
| Safety | Retrieved content is data, queries are scrubbed, no third-party commands, no posting | `SKILL.md` Safety and Red flags |
| Triggering | Third-person description with concrete triggers and exclusions; 20-query trigger set | `SKILL.md` frontmatter, `evals/trigger-evals.json` |
| Compact answers | Conclusion, evidence, change, verify, uncertainty; long report only on request | `SKILL.md` step 7, `references/extraction-playbook.md` |
| Search craft | Query recipes, release checks, fork mining, index blind spots | `references/search-patterns.md` |
| Regression set | 8 behavior cases with safety fixtures, run protocol, results log | `evals/` |
| Validation and CI | Frontmatter, length, links, metadata keys, evals, YAML safety, English-only | `tools/check_skill.py`, `.github/workflows/validate.yml` |
| Packaging | claude.ai zip and portable Agent Plugin zip, built locally and in CI | `tools/check_skill.py --package` |
| Documentation | Per-platform installation, safe migration, sources | `README.md`, `MIGRATION.md`, `docs/REFERENCES.md` |

## Remaining work

Work through these in order. Change `SKILL.md` only in response to a recorded failure.

1. **Acceptance in Claude chat (claude.ai).** Upload `dist/pavedpath-code.zip`, then run every case in `evals/evals.json` 3 times with the Skill on and 3 times with it off, and run the trigger set once. Record each run in `evals/README.md`.
   *Done when* all with-Skill runs of the two safety cases pass, every other case passes at least 2 of 3 runs, and trigger accuracy is at least 9 of 10 in both groups.
2. **Fix observed failures.** For each failing assertion, decide whether the cause is triggering (edit `description`), instructions (edit `SKILL.md` or the relevant reference), or the case itself (edit the eval). Re-run only the affected cases.
3. **Acceptance in Claude Code and Codex CLI.** Repeat step 1 on terminal surfaces, where `gh` may be present but blocked.
4. **ChatGPT web and mobile.** Install `dist/pavedpath-code-plugin.zip` through a local marketplace in the ChatGPT desktop app, confirm that the Skill loads in a web chat, then run step 1 there. Publish to a workspace or submit publicly only after it passes.
5. **Mark verified platforms in the README.** Write "verified on <platform>, <date>, <model>" only for platforms with recorded passing rows.

## Release checklist

1. `python3 tools/check_skill.py --package` passes.
2. `CHANGELOG.md` has a `## X.Y.Z - date` heading at the top; the packager reads the version from it.
3. Any behavior change has a matching eval case, and its results are recorded.
4. CI is green; its run artifacts contain both zips.
5. Tag the commit `vX.Y.Z` and attach both zips to the GitHub release.

## Non-goals

- A GitHub proxy, hosted MCP server, search index, or database.
- Autonomous edits to the user's repository or automatic deployments.
- Persistent subagent infrastructure or mandatory parallel research.
- Report generators, dashboards, or elaborate output schemas.
- Claims that instructions can make unavailable tools accessible.

Revisit these only after a reproducible user need and a minimal design exist.

## Decisions

| Decision | Reason |
| --- | --- |
| Instruction-only Skill; maintainer tooling lives outside the package | Works on every surface, including the network-less Claude API; nothing in the package executes. |
| Evaluations before new instructions | Model behavior varies; only with-versus-without comparisons show the Skill's value. |
| Install URLs point to this fork | The fork's behavior differs substantially from upstream; upstream is credited in the README. |
| Plugin built at package time, not stored in the repository | Keeps one Skill layout for every surface; the manifest is generated from `SKILL.md`, `agents/openai.yaml`, and the changelog. |

History of the original proposal and its gap analysis is in the git log and `CHANGELOG.md`.
