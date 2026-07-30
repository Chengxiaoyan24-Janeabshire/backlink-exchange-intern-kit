import argparse
import base64
import importlib.util
from pathlib import Path
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_gmail_threads_to_feishu.py"
SPEC = importlib.util.spec_from_file_location("gmail_sync", MODULE_PATH)
gmail_sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(gmail_sync)


class GmailBodyTests(unittest.TestCase):
    def test_get_record_requests_rich_text_links(self):
        response = mock.Mock()
        response.json.return_value = {
            "code": 0,
            "data": {"record": {"record_id": "rec1", "fields": {}}},
        }
        with mock.patch.object(gmail_sync.requests, "get", return_value=response) as get:
            gmail_sync.get_record("token", "app", "table", "rec1")

        self.assertEqual(
            get.call_args.kwargs["params"],
            {"text_field_as_array": "true"},
        )

    def test_list_records_requests_rich_text_links(self):
        response = mock.Mock()
        response.json.return_value = {
            "code": 0,
            "data": {"items": [], "has_more": False},
        }
        with mock.patch.object(gmail_sync.requests, "get", return_value=response) as get:
            gmail_sync.list_records("token", "app", "table", "view")

        requested_url = get.call_args.args[0]
        self.assertIn("text_field_as_array=true", requested_url)

    def test_quote_wrapped_message_keeps_current_body(self):
        raw = (
            "> Hi Itamar,\n>\n> Here is our new proposal.\n>\n"
            "> On Thu, Jul 9, 2026 someone wrote:\n>> Old quoted history\n"
        )
        cleaned = gmail_sync.clean_email_body(raw)
        self.assertIn("Here is our new proposal.", cleaned)
        self.assertNotIn("Old quoted history", cleaned)

    def test_message_payload_with_quote_wrapped_plain_text_is_readable(self):
        body = "> Hi,\n>\n> Full message body\n"
        encoded = base64.urlsafe_b64encode(body.encode()).decode().rstrip("=")
        message = {
            "id": "msg-1",
            "internalDate": "1",
            "payload": {
                "headers": [{"name": "From", "value": "Jane <jane@zilliz.com>"}],
                "mimeType": "text/plain",
                "body": {"data": encoded},
            },
        }
        item = gmail_sync.message_to_item(message)
        self.assertIn("Full message body", item["body"])

    def test_html_gmail_quote_is_removed(self):
        raw = """
        <div>Thanks, this works for us.</div>
        <div class="gmail_attr">On Thu, Jul 23, 2026 Jane wrote:</div>
        <div class="gmail_quote"><blockquote>Previous email body</blockquote></div>
        """
        cleaned = gmail_sync.clean_email_body(gmail_sync.html_to_text(raw))
        self.assertIn("Thanks, this works for us.", cleaned)
        self.assertNotIn("Previous email body", cleaned)
        self.assertNotIn("Jane wrote", cleaned)

    def test_outlook_reply_header_and_previous_email_are_removed(self):
        raw = """Hi Jane,

Yes, please go ahead with the proposed page.

From: Jane Doe <jane@zilliz.com>
Sent: Wednesday, July 22, 2026 10:00 AM
To: Partner <partner@example.com>
Subject: Re: Link exchange

Here is the message I sent earlier.
"""
        cleaned = gmail_sync.clean_email_body(raw)
        self.assertIn("Yes, please go ahead", cleaned)
        self.assertNotIn("Here is the message I sent earlier", cleaned)
        self.assertNotIn("Sent: Wednesday", cleaned)

    def test_original_message_separator_is_removed(self):
        raw = """Approved, thank you.

-----Original Message-----
From: Jane Doe <jane@zilliz.com>
Old message body
"""
        cleaned = gmail_sync.clean_email_body(raw)
        self.assertEqual(cleaned, "Approved, thank you.")

    def test_wrapped_gmail_reply_header_is_removed(self):
        raw = """Hi Graham,

Thanks for the proposal.

On Thu, Jul 9, 2026 at 9:30 PM Graham Gillen <graham@example.com>
wrote:
Previous message body
"""
        cleaned = gmail_sync.clean_email_body(raw)
        self.assertEqual(cleaned, "Hi Graham,\n\nThanks for the proposal.")

    def test_thread_markdown_does_not_truncate_complete_body(self):
        long_body = "x" * 7000
        record = {"record_id": "rec1", "fields": {"Domain": "example.com"}}
        thread = {
            "id": "thread1",
            "messages": [
                {
                    "subject": "Subject",
                    "date": "Date",
                    "from": "Partner <p@example.com>",
                    "to": "Jane <jane@zilliz.com>",
                    "cc": "",
                    "body": long_body,
                }
            ],
        }
        markdown = gmail_sync.thread_markdown(
            record,
            "query",
            thread,
            connection_summary="summary",
            latest_response_summary="latest",
        )
        self.assertIn(long_body, markdown)
        self.assertNotIn("[Body truncated]", markdown)

    def test_thread_markdown_stores_gmail_message_id(self):
        record = {"record_id": "rec1", "fields": {"Domain": "example.com"}}
        thread = {
            "id": "thread1",
            "messages": [
                {
                    "id": "gmail-message-1",
                    "subject": "Subject",
                    "date": "Date",
                    "from": "Partner <p@example.com>",
                    "to": "Jane <jane@zilliz.com>",
                    "cc": "",
                    "body": "Message body",
                }
            ],
        }

        markdown = gmail_sync.thread_markdown(record, "query", thread)

        self.assertIn("Gmail message ID: gmail-message-1", markdown)

    def test_incremental_sync_selects_only_unseen_message_ids(self):
        messages = [
            {
                "id": "gmail-message-1",
                "date": "Date 1",
                "from": "Partner <p@example.com>",
                "to": "Jane <jane@zilliz.com>",
                "cc": "",
                "body": "First message",
            },
            {
                "id": "gmail-message-2",
                "date": "Date 2",
                "from": "Jane <jane@zilliz.com>",
                "to": "Partner <p@example.com>",
                "cc": "",
                "body": "Second message",
            },
        ]
        existing = "Message 1\nGmail message ID: gmail-message-1\nFirst message"

        new_messages = gmail_sync.select_new_messages(messages, existing)

        self.assertEqual([index for index, _ in new_messages], [2])
        self.assertEqual(new_messages[0][1]["id"], "gmail-message-2")

    def test_incremental_sync_recognizes_legacy_message_with_edited_body(self):
        message = {
            "id": "gmail-message-1",
            "date": "Thu, 9 Jul 2026 07:37:11 -0400",
            "from": "Jane Jiang <jane.jiang@zilliz.com>",
            "to": "Partner <partner@example.com>",
            "cc": "",
            "body": "A legacy message body that was written before IDs were stored.",
        }
        existing = """Message 1
Date: Thu, 9 Jul 2026 07:37:11 -0400
From: Jane Jiang <jane.jiang@zilliz.com>
To: Partner <partner@example.com>

This body was manually highlighted or edited after the original sync.
"""

        self.assertEqual(gmail_sync.select_new_messages([message], existing), [])

    def test_incremental_sync_recognizes_manually_pasted_body_without_headers(self):
        message = {
            "id": "gmail-message-1",
            "date": "Date",
            "from": "Jane <jane@zilliz.com>",
            "to": "Partner <partner@example.com>",
            "cc": "",
            "body": (
                "Hi Graham, thank you again for the thoughtful proposal. "
                "Once we receive the benchmark data and draft, our content team "
                "can review the best available placement and share feedback."
            ),
        }
        existing = (
            "Message 5\nHi Graham — thank you again for the thoughtful proposal.\n"
            "Once we receive the benchmark data and draft, our content team can "
            "review the best available placement and share feedback."
        )

        self.assertEqual(gmail_sync.select_new_messages([message], existing), [])

    def test_incremental_markdown_contains_only_new_messages(self):
        record = {"record_id": "rec1", "fields": {"Domain": "example.com"}}
        thread = {"id": "thread1", "messages": []}
        new_messages = [
            (
                3,
                {
                    "id": "gmail-message-3",
                    "date": "Date 3",
                    "from": "Partner <p@example.com>",
                    "to": "Jane <jane@zilliz.com>",
                    "cc": "",
                    "body": "Only the new message",
                },
            )
        ]

        markdown = gmail_sync.incremental_thread_markdown(
            record,
            "query",
            thread,
            new_messages,
        )

        self.assertIn("Message 3", markdown)
        self.assertIn("gmail-message-3", markdown)
        self.assertIn("Only the new message", markdown)
        self.assertNotIn("Message 1", markdown)

    def test_snapshot_refresh_updates_managed_blocks_and_inserts_missing_next_step(self):
        def block(block_id, text, block_type, parent_id="doc1", background_color=0):
            key = {2: "text", 4: "heading2", 5: "heading3"}[block_type]
            return {
                "block_id": block_id,
                "parent_id": parent_id,
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        highlighted_message = block(
            "message-body",
            "Approved reusable wording.",
            2,
            background_color=2,
        )
        blocks = [
            {"block_id": "doc1", "parent_id": "", "block_type": 1},
            block("summary-heading", "对接概括", 4),
            block("summary-value", "Old summary", 2),
            block("response-heading", "Responce（最新一封对方回复概括）", 4),
            block("response-value", "Old response", 2),
            block("next-step-heading", "Next Step（人工输入下一步目标）", 4),
            block("audit-heading", "Gmail Match Audit", 4),
            block("message-heading", "Message 1", 5),
            highlighted_message,
        ]
        fields = {
            "对接概括": "New summary",
            "Responce": "New response",
            "Next Step": "Human-authored next step",
        }

        plan = gmail_sync.plan_thread_snapshot_refresh(blocks, "doc1", fields)

        self.assertEqual(
            [(item["field"], item["action"]) for item in plan],
            [("对接概括", "update"), ("Responce", "update"), ("Next Step", "insert")],
        )
        self.assertEqual(plan[0]["block_id"], "summary-value")
        self.assertEqual(plan[1]["block_id"], "response-value")
        self.assertEqual(plan[2]["index"], 5)
        self.assertNotIn("message-body", {item.get("block_id") for item in plan})
        self.assertEqual(gmail_sync.rich_text_block(highlighted_message), ("Approved reusable wording.", True))

    def test_apply_snapshot_refresh_only_writes_planned_managed_blocks(self):
        response = mock.Mock()
        response.json.return_value = {"code": 0, "data": {}}
        plan = [
            {
                "field": "对接概括",
                "action": "update",
                "block_id": "summary-value",
                "text": "New summary",
            },
            {
                "field": "Responce",
                "action": "unchanged",
                "block_id": "response-value",
                "text": "Same response",
            },
            {
                "field": "Next Step",
                "action": "insert",
                "parent_block_id": "doc1",
                "index": 5,
                "text": "Human next step",
            },
        ]

        with mock.patch.object(gmail_sync.requests, "patch", return_value=response) as patch_request, mock.patch.object(
            gmail_sync.requests, "post", return_value=response
        ) as post_request:
            result = gmail_sync.apply_thread_snapshot_refresh("token", "doc1", plan)

        self.assertEqual(result["updated"], ["对接概括"])
        self.assertEqual(result["inserted"], ["Next Step"])
        self.assertEqual(result["unchanged"], ["Responce"])
        self.assertEqual(patch_request.call_count, 1)
        self.assertTrue(patch_request.call_args.args[0].endswith("/blocks/summary-value"))
        self.assertEqual(
            patch_request.call_args.kwargs["json"],
            {"update_text_elements": {"elements": gmail_sync.text_elements("New summary")}},
        )
        self.assertEqual(post_request.call_count, 1)
        self.assertTrue(post_request.call_args.args[0].endswith("/blocks/doc1/children"))
        self.assertEqual(post_request.call_args.kwargs["json"]["index"], 5)

    def test_snapshot_refresh_skips_values_that_already_match(self):
        def block(block_id, text, block_type):
            key = {2: "text", 4: "heading2"}[block_type]
            return {
                "block_id": block_id,
                "parent_id": "doc1",
                "block_type": block_type,
                key: {"elements": gmail_sync.text_elements(text)},
            }

        fields = {
            "对接概括": "Same summary",
            "Responce": "Same response",
            "Next Step": "Same next step",
        }
        blocks = [
            block("summary-heading", "对接概括", 4),
            block("summary-value", "Same summary", 2),
            block("response-heading", "Responce（最新一封对方回复概括）", 4),
            block("response-value", "Same response", 2),
            block("next-heading", "Next Step（人工输入下一步目标）", 4),
            block("next-value", "Same next step", 2),
        ]

        plan = gmail_sync.plan_thread_snapshot_refresh(blocks, "doc1", fields)

        self.assertTrue(all(item["action"] == "unchanged" for item in plan))


class HighlightAndQueryTests(unittest.TestCase):
    def test_extract_url_prefers_rich_link_target_over_display_text(self):
        value = [{"text": "Thread title", "link": "https://example.feishu.cn/docx/abc123"}]
        self.assertEqual(
            gmail_sync.extract_url(value),
            "https://example.feishu.cn/docx/abc123",
        )

    def test_only_highlighted_outgoing_reply_is_template_evidence(self):
        def block(text, block_type=2, background_color=0):
            key = {2: "text", 5: "heading3", 13: "ordered"}[block_type]
            return {
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        blocks = [
            block("Message 1", 5),
            block("From: partner@example.com"),
            block("Incoming context", background_color=2),
            block("Message 2", 5),
            block("From: Jane <jane@zilliz.com>"),
            block("Approved reusable wording.", background_color=2),
        ]
        sections = gmail_sync.extract_highlighted_email_sections(blocks)
        self.assertEqual(len(sections), 1)
        self.assertIn("Approved reusable wording", sections[0])
        self.assertNotIn("Incoming context", sections[0])

    def test_each_contiguous_highlight_becomes_independent_template_evidence(self):
        def block(text, block_type=2, background_color=0):
            key = {2: "text", 5: "heading3", 13: "ordered"}[block_type]
            return {
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        blocks = [
            block("Message 3", 5),
            block("From: Jane <jane@zilliz.com>"),
            block("Hi Graham,"),
            block("New content requires content-team review.", background_color=2),
            block("Please send a topic proposal."),
            block("Message 4", 5),
            block("From: Graham <graham@example.com>"),
            block("Incoming highlighted text must not become a template.", background_color=2),
            block("Message 5", 5),
            block("Hi Graham,"),
            block("To help us move forward, could you share more information?", background_color=2),
            block("What support would be useful from our team?", 13, background_color=2),
            block("Could you send us a brief outline?", 13, background_color=2),
            block("Would an existing-page link placement work as a backup?", 13, background_color=2),
            block("Best,\nJane"),
        ]

        sections = gmail_sync.extract_highlighted_email_sections(blocks)

        self.assertEqual(len(sections), 2)
        self.assertIn("Message 3", sections[0])
        self.assertIn("content-team review", sections[0])
        self.assertNotIn("topic proposal", sections[0])
        self.assertIn("Message 5", sections[1])
        self.assertIn("- Could you send us a brief outline?", sections[1])
        self.assertIn("existing-page link placement", sections[1])
        self.assertNotIn("Incoming highlighted", "\n".join(sections))

    def test_separated_highlights_in_one_email_are_two_evidence_items(self):
        def block(text, block_type=2, background_color=0):
            key = {2: "text", 5: "heading3"}[block_type]
            return {
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        sections = gmail_sync.extract_highlighted_email_sections(
            [
                block("Message 7", 5),
                block("From: Jane <jane@zilliz.com>"),
                block("First reusable fragment.", background_color=2),
                block("Unhighlighted bridge."),
                block("Second reusable fragment.", background_color=2),
            ]
        )

        self.assertEqual(len(sections), 2)
        self.assertIn("First reusable fragment", sections[0])
        self.assertIn("Second reusable fragment", sections[1])
        self.assertNotEqual(
            gmail_sync.template_evidence_id(sections[0]),
            gmail_sync.template_evidence_id(sections[1]),
        )

    def test_empty_paragraph_separates_highlights_in_one_email(self):
        def block(text, block_type=2, background_color=0):
            key = {2: "text", 5: "heading3"}[block_type]
            return {
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        sections = gmail_sync.extract_highlighted_email_sections(
            [
                block("Message 7", 5),
                block("From: Jane <jane@zilliz.com>"),
                block("First reusable fragment.", background_color=2),
                block(""),
                block("Second reusable fragment.", background_color=2),
            ]
        )

        self.assertEqual(len(sections), 2)
        self.assertIn("First reusable fragment", sections[0])
        self.assertIn("Second reusable fragment", sections[1])

    def test_mixed_highlight_runs_in_one_block_remain_independent(self):
        def block(text, block_type=2, background_color=0):
            key = {2: "text", 5: "heading3"}[block_type]
            return {
                "block_type": block_type,
                key: {
                    "elements": [
                        {
                            "text_run": {
                                "content": text,
                                "text_element_style": {"background_color": background_color},
                            }
                        }
                    ]
                },
            }

        mixed_block = block("")
        mixed_block["text"]["elements"] = [
            {
                "text_run": {
                    "content": "First reusable fragment.",
                    "text_element_style": {"background_color": 2},
                }
            },
            {
                "text_run": {
                    "content": " Unhighlighted bridge. ",
                    "text_element_style": {"background_color": 0},
                }
            },
            {
                "text_run": {
                    "content": "Second reusable fragment.",
                    "text_element_style": {"background_color": 2},
                }
            },
        ]

        sections = gmail_sync.extract_highlighted_email_sections(
            [
                block("Message 7", 5),
                block("From: Jane <jane@zilliz.com>"),
                mixed_block,
            ]
        )

        self.assertEqual(len(sections), 2)
        self.assertIn("First reusable fragment", sections[0])
        self.assertIn("Second reusable fragment", sections[1])
        self.assertNotIn("Unhighlighted bridge", "\n".join(sections))

    def test_heuristic_fallback_keeps_one_template_per_highlight(self):
        fragments = [
            "Message 3\nFrom: Jane <jane@zilliz.com>\nHighlighted excerpt:\n"
            "Please send a topic proposal for the co-created content so our content team can review it.",
            "Message 5\nDirection: outgoing (inferred from signature)\nHighlighted excerpt:\n"
            "Could you send us a brief outline for the benchmark and confirm whether an existing page works as a backup?",
        ]
        summary = gmail_sync.heuristic_pattern_summary(
            {"fields": {"Domain": "pureinsights.com"}},
            {"messages": []},
            fragments,
        )

        self.assertEqual(summary.count("Reusable template:"), 2)
        self.assertIn("Highlighted fragment 1", summary)
        self.assertIn("Highlighted fragment 2", summary)
        self.assertIn("brief outline", summary)
        self.assertIn("Milvus AI Quick Reference", summary)

    def test_thread_markdown_has_no_context_markers(self):
        record = {"record_id": "rec1", "fields": {"Domain": "example.com"}}
        thread = {
            "id": "thread1",
            "messages": [
                {
                    "subject": "Subject",
                    "date": "Date",
                    "from": "Jane <jane@zilliz.com>",
                    "to": "Partner <p@example.com>",
                    "cc": "",
                    "body": "Reply body",
                }
            ],
        }
        markdown = gmail_sync.thread_markdown(record, "query", thread)
        self.assertNotIn("Context:", markdown)

    def test_query_builder_returns_auditable_fallbacks(self):
        args = argparse.Namespace(gmail_query="", newer_than="2y")
        queries = gmail_sync.build_gmail_queries(
            {"Contact": "info@example.com", "Domain": "https://example.com/path"},
            args,
        )
        self.assertGreaterEqual(len(queries), 3)
        self.assertIn("from:info@example.com", queries[0])
        self.assertTrue(any("from:example.com" in query for query in queries))


class SyncScopeTests(unittest.TestCase):
    def test_default_cli_uses_view_membership_without_field_filters(self):
        with mock.patch(
            "sys.argv",
            ["sync_gmail_threads_to_feishu.py", "sync"],
        ):
            args = gmail_sync.parse_args()

        self.assertEqual(args.status, "")
        self.assertEqual(args.collaboration, "")
        self.assertEqual(args.limit, 0)

    def test_view_record_is_in_scope_regardless_of_status_or_collaboration(self):
        record = {
            "record_id": "rec1",
            "fields": {
                "Status": "等待内部确认",
                "Collaboration": "内容合作",
            },
        }
        args = argparse.Namespace(
            record_id=[],
            status="",
            collaboration="",
            require_guidance=False,
        )

        self.assertTrue(gmail_sync.should_process(record, args))

if __name__ == "__main__":
    unittest.main()
