# Agent Handoff

## Project

Backlink Exchange Intern Kit provides the rules and active Gmail-to-Feishu runtime used by the installed Organic Exchange skills.

## Run Commands

- Full evaluation: `$evaluate-backlink-exchange`
- Health only: `$assess-backlink-health`
- Partner pages only: `$find-partner-blog-pages`
- Our pages only: `$match-our-placement-pages`
- Manual next reply: `$draft-backlink-reply`
- Gmail only: `$sync-backlink-gmail`
- Gmail auth: `PYTHONUNBUFFERED=1 python3 scripts/sync_gmail_threads_to_feishu.py auth-gmail --no-browser`
- Sync validation: `python3 -m unittest tests.test_sync_gmail`
- Compile check: `python3 -m py_compile scripts/sync_gmail_threads_to_feishu.py`

## Stack

Python 3 plus `requests`; Google Gmail API client libraries are used by the sync runtime. Feishu document and Base operations are coordinated by the installed skills and `lark-cli` where applicable.

## Conventions

- Keep secrets and OAuth tokens outside the repo. Default local paths are documented in `.env.example`.
- The Organic Exchange Bitable field name `Responce` is intentionally misspelled to match the live field.
- The Gmail sync defaults belong to the built-in Organic Exchange table and ongoing communication view. Do not borrow adjacent-project table/view IDs.
- Use `--dry-run` before batch Feishu writes. Communication Thread docs are append-only.
- `对接概括` and `Responce` are automated summaries. `Next Step` is human-authored and must never be overwritten.
- Gmail sync must not generate an outbound draft automatically. `$draft-backlink-reply` is manual-only and appends `Next Draft` at the end of the Communication Thread.
- Template approval uses human-highlighted fragments inside outgoing Communication Thread emails. There are no `Context: yes/no` markers. Every contiguous highlighted fragment is independent evidence and must produce its own context and reusable template, even when several highlights occur in one email or thread. Unhighlighted text is context only.

## Evaluation Contract

`BACKGROUND.md` is the project-level business contract. The installed evaluation subskills implement that contract; do not create a second local template or alternate decision flow.

## Current Status

As of 2026-07-24, the active local runtime is `scripts/sync_gmail_threads_to_feishu.py`, with focused regression coverage in `tests/test_sync_gmail.py`. The Feishu template Wiki is the reusable-email template source of truth. Live verification against the Pureinsights thread detects separate Message 3 and Message 5 evidence.

On 2026-07-20, Gmail OAuth succeeded on this machine and matched threads were written for `bigdataboutique.com`, `pureinsights.com`, and `shiftasia.com`.
