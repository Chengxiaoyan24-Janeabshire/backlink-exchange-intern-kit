# Backlink Exchange Agent

> 基本规则
>
> - 评估规则：合作方健康度必须与完整的 `milvus.io` 和 `zilliz.com` 域名比较，不混用不同 SEO provider 的指标。
> - 对方页面规则：正好推荐 5 篇真实 Blog，优先 2025 或 2026 年内容，并给出 section、anchor 和句子级插入建议。
> - 对方链接目标规则：对方给我们加链接时，目标必须是相关的非 FAQ Milvus/Zilliz 页面；禁止使用 Zilliz AI FAQ、Milvus AI Quick Reference 或其他 FAQ/reference-style 页面。
> - 我方页面规则：推荐 1–2 篇 Zilliz/Milvus Blog，加正好 3 篇 Milvus AI Quick Reference。
> - Placement 规则：只接受 indexable、dofollow、正文内且语义自然的链接；拒绝 sponsored、nofollow、noindex、footer、sidebar 和目录页。
> - Gmail 规则：同步更新 Base 自动摘要并刷新 Thread 顶部受管快照；人工填写的 Base `Next Step`、邮件高亮来源和 `Next Draft` 不会被覆盖，也不会自动生成回复。
> - 模板规则：每个 outgoing email 中连续的人工高亮片段都是独立证据，分别生成自己的 Context 和 reusable Template。

## 1. 整个 Agent 的逻辑

```text
用户请求
   ├─ 完整评估合作方
   │   └─ evaluate-backlink-exchange
   │       ├─ assess-backlink-health
   │       ├─ find-partner-blog-pages
   │       ├─ match-our-placement-pages
   │       └─ 创建 Feishu Evaluation Doc 并写回 Evaluation 字段
   │
   ├─ 同步 Gmail 沟通
   │   └─ sync-backlink-gmail
   │       ├─ 匹配 Organic Exchange row 与 Gmail Thread
   │       ├─ 清理重复引用并追加 Communication Thread 邮件历史
   │       ├─ 更新 Base 的 对接概括 和 Responce，并刷新 Thread 顶部的 对接概括 / Responce / Next Step 镜像
   │       └─ 把每个新高亮片段分别沉淀到模板 Wiki
   │
   └─ 起草下一封回复
       └─ draft-backlink-reply
           ├─ 读取 Next Step 和完整 Thread
           ├─ 匹配模板 Wiki 中的 Context
           └─ 在 Communication Thread 末尾追加 Next Draft
```

Evaluation、Gmail sync 和 Next Draft 是三条独立流程：Evaluation 不同步 Gmail；Gmail sync 不生成 outbound draft；`Next Draft` 只能人工触发。

## 2. Skills 与触发方式

| Skill | 功能 | 输出 |
|---|---|---|
| `evaluate-backlink-exchange` | 运行完整合作方评估 | Feishu Evaluation Doc 和写回的 Evaluation 链接 |
| `assess-backlink-health` | 只评估公司服务、Authority、流量和内容相关度 | Backlink health 结论 |
| `find-partner-blog-pages` | 找到对方 5 篇可自然插入 Milvus/Zilliz 链接的 Blog | 5 条带 section、anchor 和插入建议的候选 |
| `match-our-placement-pages` | 匹配我方可放置对方链接的页面 | 1–2 篇 Blog 和 3 篇 AI Quick Reference |
| `sync-backlink-gmail` | 同步 Gmail、更新 Feishu 自动摘要、Thread 和模板证据 | 更新后的 row、Communication Thread 和模板 Wiki |
| `draft-backlink-reply` | 根据人工目标、Thread 和已批准模板生成回复 | Thread 末尾的 `Next Draft` |

自然语言示例：

- “给这个网站跑完整的 backlink evaluation” → `evaluate-backlink-exchange`
- “只比较这个合作方和 Milvus/Zilliz 的 domain health” → `assess-backlink-health`
- “找对方 5 篇适合加我们链接的 Blog” → `find-partner-blog-pages`
- “找我们这边可以放对方链接的页面” → `match-our-placement-pages`
- “同步最新的 Organic Exchange Gmail” → `sync-backlink-gmail`
- “根据 Next Step 起草下一封回复” → `draft-backlink-reply`

## 3. Feishu 字段是什么

| 字段 | 维护者 | 含义 |
|---|---|---|
| `对接概括` | Gmail sync 自动更新 | 完整沟通进展的简要概括 |
| `Responce` | Gmail sync 自动更新 | 最新一封合作方回复的概括；拼写与线上 Bitable 字段保持一致 |
| `Next Step` | 人工维护 | 下一封回复要达成的目标，自动化永远不能覆盖 Base 原值；Thread 顶部只做当前值镜像 |
| `Communication Thread` | Gmail sync 维护 | 顶部受管快照原位刷新；邮件历史、高亮来源和 Next Draft 只追加、不重写 |
| `Next Draft` | `draft-backlink-reply` 人工触发 | 根据 Next Step 和已验证 Thread 生成的下一封草稿 |
| `Evaluation` | 完整评估流程写入 | 合作方 Evaluation Doc 链接 |

## 4. Evaluation 与 Placement 标准

- Health assessment 比较完整的 `https://milvus.io/`、`https://zilliz.com/` 和合作方域名。
- Moz DA、Ahrefs DR、SEMrush Authority Score 等指标必须保留 provider 标签，不能当作同一个数值比较。
- 对方候选必须是可索引的真实 Blog 内容；不接受 homepage、product/service、company、contact、directory、partner 或 generic resource-list 页面。
- 对方在候选 Blog 中添加我们的链接时，链接目标必须是相关的非 FAQ Milvus/Zilliz 页面；Zilliz AI FAQ、Milvus AI Quick Reference 及其他 FAQ/reference-style 页面都不能作为这一侧的目标。
- 我方 Blog 候选只来自 `zilliz.com/blog/` 或 `milvus.io/blog/`，排除产品发布、功能公告、Featured collection 和 sponsored-style 内容。
- Milvus AI Quick Reference 候选只来自 `milvus.io/ai-quick-reference/`，仅用于我们给对方添加链接的一侧；Zilliz AI FAQ 不属于可用 inventory。
- Evaluation 输出不包含 Decision、Best Bilateral Placement、Missing Information 或 reply draft。

完整业务合同以 [`BACKGROUND.md`](BACKGROUND.md) 为准；已安装的 evaluation Skills 实现该合同，本仓库不维护第二套评估模板。

## 5. Gmail 同步与模板沉淀

- Sync 默认使用内置的 Organic Exchange table 和 ongoing communication view；不要借用相邻项目的 table/view ID。凡进入该 view 的记录都属于默认同步范围，不再按 `Status`、`Collaboration` 或默认条数上限二次过滤。
- 批量写入 Feishu 前先使用 `--dry-run`。
- 已有 Communication Thread 永不重建或替换。同步只原位刷新顶部 `对接概括`、`Responce`、`Next Step` 三个受管快照段落，并仅追加尚未写入的新 Gmail 消息。新写入消息保存 Gmail message ID，旧文档通过内容签名兼容去重；任何 `Message N` 邮件 block、人工高亮和 `Next Draft` 都不被 PATCH、删除或重建。
- Gmail Thread 写入 Communication Thread 时会去除回复里重复引用的历史邮件，保留可读的实际消息内容。
- 只有 outgoing email 中人工高亮的文字可以成为模板证据；incoming 高亮和未高亮文字不能成为 reusable phrasing。
- 每个连续高亮片段独立生成一份 Context 和 Template。同一封邮件中有多个分开的高亮，也不能合并。
- 完整邮件和 Thread 只用于推断高亮片段的适用场景，不能把未高亮措辞混入模板。
- 已沉淀的高亮证据通过稳定 evidence ID 去重，后续同步不会重复写入同一份模板。

## 6. 主要目录

| 路径 | 内容 |
|---|---|
| `scripts/sync_gmail_threads_to_feishu.py` | Gmail OAuth、Thread 匹配、Feishu 写入、自动摘要和模板沉淀 runtime |
| `tests/test_sync_gmail.py` | Gmail 正文清理、高亮提取、证据拆分和模板 fallback 的回归测试 |
| `BACKGROUND.md` | 外链评估与 placement 的项目级业务合同 |
| `AGENTS.md` | Agent 接手时必须遵守的运行与安全规则 |
| `.env.example` | 本地配置路径和可选环境变量示例，不包含真实 secrets |
| `CHANGELOG.md` | 每次推送的功能、行为和修复摘要 |

## 7. 本地运行

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

首次 Gmail 授权：

```bash
PYTHONUNBUFFERED=1 python3 scripts/sync_gmail_threads_to_feishu.py auth-gmail --no-browser
```

先 dry run，再执行写入：

```bash
python3 scripts/sync_gmail_threads_to_feishu.py sync --dry-run
python3 scripts/sync_gmail_threads_to_feishu.py sync
```

只有明确需要小批量处理时才额外传入 `--limit N`。

本地验证：

```bash
python3 -m unittest tests.test_sync_gmail
python3 -m py_compile scripts/sync_gmail_threads_to_feishu.py
```

Feishu 配置、Gmail OAuth client 和 token 必须保存在仓库外。默认路径与环境变量见 [`.env.example`](.env.example)。

## 8. Change Log 怎么维护

所有准备推送到 GitHub 的功能或行为变更，都要在同一次 push 中更新 [`CHANGELOG.md`](CHANGELOG.md)。一条 push 记录可以概括多个 commit，重点写用户或运行流程得到的变化，不要只列“修改了哪些文件”。

推荐分类：

- `Added`：新增能力、命令、字段或工作流。
- `Changed`：已有行为、规则或默认值发生变化。
- `Fixed`：修复错误或回归问题。
- `Removed`：删除已经不再支持的能力。
- `Security`：凭证、权限或数据保护相关修复。

本项目暂不使用版本号，因此用 `YYYY-MM-DD — 简短主题` 作为每次推送的标题。Commit message 同样使用简洁的动词开头，例如 `Document pipeline and add changelog policy`。
