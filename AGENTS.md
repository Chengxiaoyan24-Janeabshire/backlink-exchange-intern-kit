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
- Evaluation Docs and agent-generated Communication Thread content must use Chinese for document titles, headings, summaries, audit labels, and explanatory text. Preserve proper nouns, URLs, provider metric names, exact proposed English anchors/insertion copy, raw Gmail messages, and human-highlighted source wording in their original language.
- Every future Evaluation must include the following full-domain baseline under `外链健康度`, labeled `我方域名基准（用户提供，2026-08-04）`: Milvus — Moz DA 45, monthly organic visits 130.2K, referring domains 7K, backlinks 488.4K; Zilliz — Moz DA 36, monthly organic visits approximately 19.7K, referring domains 4.3K, backlinks 318K+. The traffic, referring-domain, and backlink provider was not specified, so do not invent one. If newer same-provider evidence replaces these values, preserve its source and snapshot date. Never treat Moz DA as directly equivalent to Ahrefs DR, SEMrush Authority Score, or another provider metric.
- The Organic Exchange Bitable field name `Responce` is intentionally misspelled to match the live field.
- The Gmail sync defaults belong to the built-in Organic Exchange table and ongoing communication view. Do not borrow adjacent-project table/view IDs.
- Every row returned by the ongoing communication view is in scope for the default Gmail sync, regardless of `Status` or `Collaboration`, with no default record-count cap. Apply field filters or `--limit` only when the user explicitly requests a narrower batch.
- An in-scope row with no usable Domain, Contact, or explicit Gmail query must be skipped before Gmail search; the freshness filter alone must never become a whole-mailbox query.
- Use `--dry-run` before batch Feishu writes. Communication Thread email history and `Next Draft` blocks are append-only.
- Existing Communication Thread docs must never be rebuilt or replaced. Sync only Gmail messages not already present, using Gmail message IDs with legacy content matching for older docs, so human highlights and their source text remain intact. Sync may update only the top managed snapshot paragraphs under `对接概括`, `对方最新回复概括（Responce）`, and `下一步（Next Step）`; it must never patch message or draft blocks. Legacy English-first headings remain readable for compatibility.
- `对接概括` and `Responce` are automated summaries. `Next Step` is human-authored and must never be overwritten in Base; its managed Thread snapshot mirrors the current Base value.
- Gmail sync writes `Last Touch` from the newest matched Gmail message timestamp, covering both incoming and outgoing mail. Do not use sync execution time as the field value.
- Gmail sync must not generate an outbound draft automatically. `$draft-backlink-reply` is manual-only and appends `Next Draft` at the end of the Communication Thread.
- Template approval uses human-highlighted fragments inside outgoing Communication Thread emails. There are no `Context: yes/no` markers. Every contiguous highlighted fragment is independent evidence and must produce its own context and reusable template, even when several highlights occur in one email or thread. Unhighlighted text is context only.
- The Feishu template Wiki at `https://zilliverse.feishu.cn/wiki/JBYOwqybWiYHQ8kcvxWcfR2oneb` defines the required format for all future template deposits. Append exactly one entry per highlighted fragment in this order: level-2 scenario title; bold-labeled `Scenario / context`; inline-code `Evidence ID`; bold-labeled linked `Source Communication Thread`; level-3 `Reusable reply template`; code-block template body.
- The reusable template body must be derived only from the exact human-highlighted source wording. Preserve its sentence structure, vocabulary, capitalization, punctuation, and line order. Do not add a greeting, sign-off, question, commitment, explanation, or any other unhighlighted wording. Generalize only core variable objects—such as names, companies, content titles, pages, URLs, anchors, sections, products, dates, times, deadlines, quantities, results, and locations—by replacing the exact source substring with a descriptive bracketed field such as `[Partner Company Name]` or `[confirmed date]`.
- Full emails and surrounding threads may be used only to infer the scenario title/context and identify variable objects. Any automated replacement proposal must name an exact substring that exists in the highlighted fragment; otherwise discard it. Never let an LLM generate or paraphrase the reusable template sentence itself.
- When the partner adds our link, the destination must be a relevant non-FAQ Milvus or Zilliz page. Never propose Zilliz AI FAQ, Milvus AI Quick Reference, or another FAQ/reference-style page for that side; Milvus AI Quick Reference is allowed only as our placement inventory when we add the partner's link.
- For tracker evaluations with a `Screenshot` attachment, transcribe only the visible authority and organic-traffic values into `Website Stat` using the existing compact format `DA:<value> OT:<value>`. The field's `DA` label is legacy tracker shorthand; the Evaluation Doc must still preserve the screenshot provider's real metric name, such as SEMrush Authority Score.
- Do not write the Milvus/Zilliz baseline into a partner row's `Website Stat`; that field remains partner-only and screenshot-derived.

## Evaluation Contract

`BACKGROUND.md` is the project-level business contract. The installed evaluation subskills implement that contract; do not create a second local template or alternate decision flow.

## Change Log

- Before every push that contains new repository commits, update `CHANGELOG.md` in the same batch. One entry may summarize multiple commits in that push.
- Use `YYYY-MM-DD — short topic` headings and only the applicable `Added`, `Changed`, `Fixed`, `Removed`, or `Security` categories.
- Describe user-visible functionality, runtime behavior, workflow rules, or important fixes. Do not use the Change Log as a file-by-file activity list.
- Do not claim a live result or production verification unless it was actually checked during that change.

## Current Status

As of 2026-08-03, the active local runtime is `scripts/sync_gmail_threads_to_feishu.py`, with focused regression coverage in `tests/test_sync_gmail.py`. Default batch scope is every row returned by the built-in ongoing communication view, without implicit `Status`, `Collaboration`, or record-count filters. A whole-view live sync read 14 rows: eight matched Gmail, four had no matching thread, and two blank-identifier rows were skipped before any Gmail search.

Existing Communication Thread docs refresh only the top managed `对接概括`, `对方最新回复概括（Responce）`, and `下一步（Next Step）` snapshot while Gmail messages and `Next Draft` remain append-only. The whole-view sync created initial Thread docs for `lyzr.ai`, `semaphoreui.com`, and `vectorize.io`, appended four Pureinsights messages and six OurCodeWorld messages, and refreshed the applicable managed snapshots. A post-write dry run found no new Gmail messages to append.

The Feishu template Wiki is the reusable-email template source of truth. Regression coverage verifies that every contiguous outgoing highlight remains independent evidence and that snapshot refresh never targets message or draft blocks. The runtime app received Feishu code `1770032` while appending one new template item; evidence `89c20351171e2ff8` was deposited through an authorized user identity and a follow-up dry run confirmed deduplication. Until the runtime app has edit access to that Wiki, future new evidence may require the same user-identity recovery.

Matched Gmail threads refresh `Last Touch` from the newest Gmail message's internal timestamp. All eight live values were read back exactly and were unchanged on the post-write dry run. Evaluation tracker rows use screenshot-derived `DA:<value> OT:<value>` compact stats while the Evaluation Doc retains provider-specific metric labels; the `lyzr.ai`, `semaphoreui.com`, and `vectorize.io` rows were written and read back successfully.

The `lyzr.ai`, `semaphoreui.com`, and `vectorize.io` Evaluation Docs and tracker link labels now use Chinese. Future Evaluation Docs and agent-generated Communication Thread scaffolding must also use Chinese while preserving exact English placement copy, raw Gmail messages, and highlighted source evidence.
