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
- Every row returned by the ongoing communication view is in scope for the default Gmail sync, regardless of `Status` or `Collaboration`, with no default record-count cap. Apply field filters or `--limit` only when the user explicitly requests a narrower batch.
- Use `--dry-run` before batch Feishu writes. Communication Thread email history and `Next Draft` blocks are append-only.
- Existing Communication Thread docs must never be rebuilt or replaced. Sync only Gmail messages not already present, using Gmail message IDs with legacy content matching for older docs, so human highlights and their source text remain intact. Sync may update only the top managed snapshot paragraphs under `对接概括`, `Responce`, and `Next Step`; it must never patch message or draft blocks.
- `对接概括` and `Responce` are automated summaries. `Next Step` is human-authored and must never be overwritten in Base; its managed Thread snapshot mirrors the current Base value.
- Gmail sync must not generate an outbound draft automatically. `$draft-backlink-reply` is manual-only and appends `Next Draft` at the end of the Communication Thread.
- Template approval uses human-highlighted fragments inside outgoing Communication Thread emails. There are no `Context: yes/no` markers. Every contiguous highlighted fragment is independent evidence and must produce its own context and reusable template, even when several highlights occur in one email or thread. Unhighlighted text is context only.
- When the partner adds our link, the destination must be a relevant non-FAQ Milvus or Zilliz page. Never propose Zilliz AI FAQ, Milvus AI Quick Reference, or another FAQ/reference-style page for that side; Milvus AI Quick Reference is allowed only as our placement inventory when we add the partner's link.

## Evaluation Contract

`BACKGROUND.md` is the project-level business contract. The installed evaluation subskills implement that contract; do not create a second local template or alternate decision flow.

## Change Log

- Before every push that contains new repository commits, update `CHANGELOG.md` in the same batch. One entry may summarize multiple commits in that push.
- Use `YYYY-MM-DD — short topic` headings and only the applicable `Added`, `Changed`, `Fixed`, `Removed`, or `Security` categories.
- Describe user-visible functionality, runtime behavior, workflow rules, or important fixes. Do not use the Change Log as a file-by-file activity list.
- Do not claim a live result or production verification unless it was actually checked during that change.

## Current Status

As of 2026-07-30, the active local runtime is `scripts/sync_gmail_threads_to_feishu.py`, with focused regression coverage in `tests/test_sync_gmail.py`. Default batch scope is every row returned by the built-in ongoing communication view, without implicit `Status`, `Collaboration`, or record-count filters. The last whole-view read-only check on 2026-07-25 returned seven rows.

Existing Communication Thread docs now refresh only the top managed `对接概括`, `Responce`, and `Next Step` snapshot while Gmail messages and `Next Draft` remain append-only. A targeted live sync verified one new Gmail message append plus successful refresh of all three managed snapshot fields; a follow-up read confirmed the snapshot was current and unchanged on replanning.

The Feishu template Wiki is the reusable-email template source of truth. Regression coverage verifies that every contiguous outgoing highlight remains independent evidence and that snapshot refresh never targets message or draft blocks.
