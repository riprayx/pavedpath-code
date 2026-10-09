# Research notes (fictional repository, for evaluation only)

Repository: example-org/tinyqueue (fictional)

## Issue #412 (closed)

Title: Worker crashes with "TypeError: Cannot read properties of undefined (reading 'ack')" when a job times out

- Reported against 3.8.1 and 3.8.2.
- Maintainer comment (2026-09-12): "Confirmed. Fixed by #418."
- Closed 2026-09-14 by PR #418.

## PR #418 (merged)

Title: Guard ack() when the job lease has already expired

- Merged into `main` on 2026-09-14.
- Merge commit: 9b1e7c2.
- Adds a regression test `test/timeout-ack.spec.ts`.

## Releases

| Tag | Published | Notes |
| --- | --- | --- |
| v3.8.2 | 2026-08-30 | Fix retry backoff overflow |
| v3.8.1 | 2026-08-02 | Docs and typing fixes |

No release has been published after 2026-08-30. The changelog's "Unreleased" section lists "#418 Guard ack() on expired lease".

## User environment

tinyqueue 3.8.2, Node.js 22, jobs with a 30 s timeout.
