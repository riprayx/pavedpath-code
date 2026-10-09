# Changelog

## 2026-10-09

Chat-first revision. Sources and reasoning: `docs/REFERENCES.md`.

### Changed

- `SKILL.md` rewritten. It is shorter and uses a copyable seven-step checklist. It picks research tools at runtime (connector or MCP, `gh` with REST fallbacks, web, or none) instead of requiring the GitHub CLI.
- The `description` was rewritten in the third person and lists concrete triggers (errors, build failures, version conflicts, "is this fixed upstream", library selection) plus exclusions.
- Ranking now applies hard gates (version, platform, required capability, safety, license) before ranking. A 4-tier evidence scale replaces the unused 100-point score. Stars only break ties.
- Fixes are labeled **Proposed**, **Merged**, **Released** (with a version), or **Verified**. The rubric includes commands to check that a merged PR actually shipped.
- Answers default to the compact shape: conclusion, evidence, change, verify, uncertainty. The detailed report template applies only on request or when subagents were used.
- Subagent guidance moved to a single file, `references/subagents.md`. It was previously repeated in four places.
- `agents/openai.yaml`: removed the non-standard `alias` key and the "gh first" default prompt.
- README: new installation paths for Claude Code, Codex (`~/.agents/skills`), and claude.ai (zip), plus a note that ChatGPT web and mobile need a plugin. Install URLs now point to this fork, with credit to upstream.
- `MIGRATION.md`: the `rm -rf` example is replaced by a dated backup, and the mislabeled alias line is removed.

### Added

- `references/tool-selection.md`: capability map across MCP, `gh`, REST, and web; per-platform runtime notes; error handling that tells rate limits apart from policy blocks; search limits and budget.
- `references/search-patterns.md`: query recipes, release checks, consumer-side searches, fork mining, and index blind spots.
- A safety section: retrieved content is data, queries are scrubbed, and no third-party commands run without approval. Also a red-flags list.
- `evals/`: 8 behavior cases (including prompt-injection and secret-leak fixtures), 20 trigger queries, and a run protocol with a results log.
- `tools/check_skill.py`: validates frontmatter limits, body length, links, references, `openai.yaml` keys, evals, and the English-only policy. With `--package`, it builds the claude.ai zip.
- `.github/workflows/validate.yml`: runs the validator in CI.
- `docs/REFERENCES.md`: research sources and prior art.

### Removed

- Out-of-scope rules: public platform data collection ("hot lists"), mandatory demo URLs for website templates, and a `page.evaluate` browser-scripting note.

## 2026-06-30

- Reframed README language from Codex-specific wording to a reusable, agent-agnostic Skill.
- Added a copy-to-agent installation prompt for Codex, Claude Code, Cursor Agent, ChatGPT Agent, or other agent runtimes.
- Renamed **GitHub Solution Research** to **PavedPath Code**.
- Changed the skill identifier from `github-solution-research` to `pavedpath-code`.
- Repositioned the project as the code-focused edition of PavedPath: a reusable Skill for finding proven implementation paths from GitHub and open-source evidence, then adapting them to local software engineering work.
- Preserved the previous behavior: problem-first framing, GitHub CLI-first research, evidence ranking, minimal local adaptation, and verification-first output.
- Added explicit boundaries that the future general-purpose PavedPath is out of scope for this repository.
