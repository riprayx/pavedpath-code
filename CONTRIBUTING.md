# Contributing

## Workflow

1. **Start from a failure.** Reproduce the problem in a real session and add or update a case in `evals/evals.json`. Use a fixture in `evals/files/` when the case needs input.
2. **Run the case with and without the Skill** (see `evals/README.md`). If the baseline already passes, the Skill does not need a new instruction.
3. **Make the smallest instruction change** that fixes the failure. Put triggering changes in the `description`, workflow changes in `SKILL.md`, and details in the relevant file under `references/`.
4. **Validate:** `python3 tools/check_skill.py --package`.
5. **Record results** in the results log in `evals/README.md`, and add a `CHANGELOG.md` entry.

## Layout rules

- `SKILL.md` stays under 500 lines (it is far below that today; keep it that way). Every file in `references/` is linked directly from `SKILL.md`; references do not depend on each other.
- Reference files over 100 lines start with a `## Contents` section.
- One rule lives in one place. Link instead of repeating.
- The installable Skill is `SKILL.md`, `references/`, `agents/`, and `LICENSE`. Do not add scripts there unless an evaluation shows instructions alone cannot do the job.
- `description`: third person, what the Skill does and when to use it, up to 1,024 characters, on one line, unquoted, with no `: `, ` #`, or angle brackets. The validator enforces this.
- `agents/openai.yaml` uses only keys from OpenAI's documented schema.

## Writing style

- English only for every repository-authored file: Markdown, YAML, JSON, comments, examples, and changelog entries. Proper nouns and code identifiers are fine. The validator rejects CJK characters; reviewers catch other scripts.
- Use the terms defined in the Skill consistently: *hard gate*, *evidence tier*, *fix status* (Proposed, Merged, Released, Verified).
- Prefer a positive recipe ("the answer has these parts, in this order") over lists of prohibitions.
- Never commit real credentials, even in fixtures. Use obvious placeholders such as `EXAMPLE-not-a-real-key`.

## Versioning

The top `## X.Y.Z - date` heading in `CHANGELOG.md` is the release version, and the packager copies it into the plugin manifest. Bump the minor version for behavior changes and the patch version for wording or documentation fixes.
