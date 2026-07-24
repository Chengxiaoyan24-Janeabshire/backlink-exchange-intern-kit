import argparse
import base64
import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_gmail_threads_to_feishu.py"
SPEC = importlib.util.spec_from_file_location("gmail_sync", MODULE_PATH)
gmail_sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(gmail_sync)


class GmailBodyTests(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
