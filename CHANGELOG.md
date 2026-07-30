# Change Log

本文件记录每次推送到 GitHub 的功能、行为、规则和重要修复。格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，但当前项目没有正式版本号，因此使用日期和简短主题组织记录。

## 维护规则

1. 每次准备 push 新 commit 前更新本文件；一次 push 包含多个 commit 时，可以合并为一条概括。
2. 标题使用 `YYYY-MM-DD — 简短主题`。
3. 按需要使用 `Added`、`Changed`、`Fixed`、`Removed` 或 `Security`；没有内容的分类不要保留。
4. 每条 bullet 说明新增或改变了什么能力、行为或用户结果，不写成文件名清单。
5. Change Log 与对应代码或文档放在同一批 commit 中，不能在功能推送后再补。

## 2026-07-30 — Communication Thread 受管快照刷新

### Changed

- 已有 Communication Thread 会从当前 Base 记录原位刷新顶部 `对接概括`、`Responce` 和 `Next Step` 镜像；Gmail 邮件历史与 `Next Draft` 继续保持只追加。

### Fixed

- 修复增量同步后 Thread 顶部仍停留在初始总结和旧 Next Step 的问题。同步只更新三个受管段落，不修改、删除或重建任何邮件、高亮来源或 Draft block。

## 2026-07-29 — 链接目标与模板证据拆分

### Changed

- 对方给我们添加链接时，目标 URL 必须是相关的非 FAQ Milvus/Zilliz 页面；明确排除 Zilliz AI FAQ、Milvus AI Quick Reference 和其他 FAQ/reference-style 页面。Milvus AI Quick Reference 仅保留为我们给对方回链时的候选库存。

### Fixed

- 修复同一封 outgoing email 中由空白段落或未高亮文字隔开的多个高亮片段被合并的问题，确保每个连续人工高亮分别生成独立的模板证据。

## 2026-07-25 — Gmail 同步范围与增量写入

### Changed

- Gmail 批量同步改为处理 ongoing communication view 中的全部记录；不再设置默认条数上限，`Status`、`Collaboration` 和 `--limit` 仅在明确传参时才用于缩小范围。
- 已有 Communication Thread 改为只追加尚未出现的 Gmail 消息，不再重复追加完整 Thread；新消息保存稳定 Gmail message ID，并兼容旧文档内容签名去重。

### Fixed

- 修复已进入 ongoing communication view、但合作类型不是“外链交换”的记录被默认同步遗漏的问题。
- 修复重复写入完整 Thread 导致人工高亮来源难以保留和追踪的问题；旧文档无法读取时会安全跳过，而不是冒险写入。
- 修复飞书文档字段仅返回标题时被误判为无链接、继而新建替代 Communication Thread 的问题。

## 2026-07-24 — README 与变更记录规范

### Added

- 新增项目级 Change Log，并规定每次 GitHub push 都要概括本次功能、行为或修复内容。
- 在 README 中补充 Feishu 字段语义、Gmail 模板证据规则、本地运行命令和 Change Log 分类说明。

### Changed

- README 改为与 Medium Pipeline 一致的编号式信息架构，从基本规则依次说明流程、Skills、字段、标准、目录和运行方式。
- Agent handoff 增加推送前维护 Change Log 的要求，允许一条记录概括同一次 push 中的多个 commit。

## 2026-07-24 — Initial backlink exchange agent

### Added

- 建立完整的 backlink partner evaluation 业务规则，包括 domain health、对方 5 篇 Blog 和我方 Blog/AI Quick Reference placement inventory。
- 建立 Gmail-to-Feishu runtime，同步 Communication Thread、自动更新 `对接概括` 与 `Responce`，并保护人工填写的 `Next Step`。
- 支持从 outgoing emails 的每个连续人工高亮片段分别提取 reusable Context 和 Template，并对已沉淀证据去重。
- 增加 Gmail 正文清理、高亮拆分和模板 fallback 的专项回归测试。
