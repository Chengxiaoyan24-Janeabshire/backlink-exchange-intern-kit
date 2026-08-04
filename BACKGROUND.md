# Backlink Exchange Rules

## Business Goal

Earn natural, indexable, dofollow body links to Milvus or Zilliz while keeping the reciprocal placement contextually relevant and editorially defensible.

## Health Assessment

Compare the partner with the full domains:

- `https://milvus.io/`
- `https://zilliz.com/`

Keep Moz DA, Ahrefs DR, SEMrush Authority Score, and other provider metrics distinct. Assess authority, organic traffic, content relevance, and the company's service profile. Do not use Zilliz AI FAQ or Milvus AI Quick Reference subdirectories as health benchmarks.

Use this fixed full-domain context in every Evaluation under `外链健康度`, labeled `我方域名基准（用户提供，2026-08-04）`:

| Domain | Moz DA | Monthly organic visits | Referring domains | Backlinks |
|---|---:|---:|---:|---:|
| Milvus (`milvus.io`) | 45 | 130.2K | 7K | 488.4K |
| Zilliz (`zilliz.com`) | 36 | approximately 19.7K | 4.3K | 318K+ |

The user identified the authority values as DA, so label them Moz DA. The provider for organic visits, referring domains, and backlinks was not specified; preserve those values as user-provided context without inventing a provider. If newer same-provider evidence replaces this baseline, cite its source and snapshot date. When partner evidence comes from another provider, display it alongside this baseline with an explicit provider caveat instead of treating the numbers as directly equivalent.

## Partner Adds Our Link

- Recommend exactly five partner Blog articles.
- Prefer posts published in 2025 or 2026.
- Use older posts only when materially more relevant.
- Verify URL and publication date.
- Provide section, anchor, and sentence-level insertion recommendation.
- The destination URL for our link must be a relevant non-FAQ Milvus or Zilliz page. Never use Zilliz AI FAQ, Milvus AI Quick Reference, or any other FAQ/reference-style page as the destination on the partner's site.
- Reject homepage, product/service, company/contact, directory, partner, footer/sidebar, and generic resource-list placements.

## We Add Their Link

Recommend:

- One or two relevant articles from `zilliz.com/blog/` or `milvus.io/blog/`.
- Three relevant pages from `milvus.io/ai-quick-reference/`.

For Blog candidates, provide section, anchor, and insertion recommendation. AI Quick Reference candidates need only URL and topical-fit explanation.

Milvus AI Quick Reference is eligible only as our placement inventory for adding the partner's link. It is not eligible as the destination when the partner adds our link.

Exclude Zilliz AI FAQ and exclude Blog pages that are new product announcements/releases, Featured collections, launch or announcement content, promotional posts, or sponsored-style content.

## Placement Requirements

Accept only indexable, dofollow, in-body placements. Reject sponsored, nofollow, noindex, footer, sidebar, directory, generic resource list, or forced off-topic placements.

## Evaluation Output

The Evaluation contains `公司与服务概览`, `外链健康度`, `对方添加我方链接——5 篇博客候选`, `我方添加对方链接——1–2 篇博客 + 3 篇 AI Quick Reference`, and `链接放置要求`. It does not contain Decision, Best Bilateral Placement, Missing Information, or a reply draft.

Every Evaluation document must use Chinese for its title, section headings, table labels, analysis, and recommendations. Preserve proper nouns, URLs, SEO provider metric names, exact proposed English anchors, and sentence-level English insertion copy when those strings must remain operationally exact.

Every `外链健康度` section must include the Milvus/Zilliz full-domain baseline defined above. This context belongs only in the Evaluation document and must not be copied into the partner row's `Website Stat`.

When the tracker row includes an SEO screenshot, transcribe only visible authority and organic-traffic values into `Website Stat` as `DA:<value> OT:<value>`, matching the existing tracker convention. `DA` is legacy field shorthand; the Evaluation document must preserve the provider's actual metric label and must not present SEMrush Authority Score as Moz DA. Use `N/A` when the screenshot explicitly shows the value as unavailable.

## Communication and Templates

Every Communication Thread document must use Chinese for its document title and all agent-generated scaffolding, managed summaries, audit labels, and explanatory text. Raw Gmail messages, email headers/addresses, human-highlighted evidence, and outbound reply copy may remain in their original working language and must never be translated in place when doing so would alter source evidence or the actual message to be sent.

`Next Step` is human-authored. Gmail sync never overwrites it and does not create an outbound draft automatically.

Gmail sync updates `Last Touch` to the newest matched Gmail message timestamp across both incoming and outgoing mail. It must not use the sync execution time.

Existing Communication Thread documents must never be rebuilt or replaced. Gmail message history and `Next Draft` blocks are immutable append-only history. Sync may refresh only the top managed `对接概括`, `对方最新回复概括（Responce）`, and `下一步（Next Step）` snapshot paragraphs from the current Base row; legacy English-first headings remain readable for compatibility. It must not patch any message or draft block. This preserves manually highlighted template evidence and its source wording while keeping the Thread's current-state snapshot accurate.

To approve reusable template evidence, highlight the exact reusable fragment in an outgoing Communication Thread email. Each contiguous highlighted fragment becomes its own evidence item and its own context/template, including when one email or thread has several highlights. On the next Gmail sync, use the containing email and full thread only to infer the fragment's situation. There are no `Context: yes/no` markers.

The Feishu template Wiki is the formatting source of truth. Append each future evidence item as: a level-2 scenario title, bold-labeled `Scenario / context`, inline-code `Evidence ID`, a bold-labeled linked `Source Communication Thread`, a level-3 `Reusable reply template` heading, and a code-block template body. Do not append batch summaries, cross-thread synthesized patterns, or extra evidence sections around these entries.

Build the reusable template body from the exact highlighted source text, not from a generated rewrite. Preserve all non-variable wording, sentence structure, capitalization, punctuation, and line order. The only permitted edits are exact-substring replacements of core variable objects—such as a name, company, content title, page, URL, anchor, section, product, date, time, deadline, quantity, result, or location—with descriptive bracketed fields. Never add unhighlighted greetings, sign-offs, questions, explanations, promises, or recommendations. The surrounding thread is context only and must never supply reusable phrasing.

`$draft-backlink-reply` is manual-only. It reads `Next Step`, the complete Communication Thread, and the template Wiki. If a template context matches, reuse the approved fixed phrasing. If no context matches, still draft from `Next Step` and verified thread facts. Append the draft at the thread end under `Next Draft`.
