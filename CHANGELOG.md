# Change Log

本文件记录每次推送到 GitHub 的功能、行为、规则和重要修复。格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，但当前项目没有正式版本号，因此使用日期和简短主题组织记录。

## 维护规则

1. 每次准备 push 新 commit 前更新本文件；一次 push 包含多个 commit 时，可以合并为一条概括。
2. 标题使用 `YYYY-MM-DD — 简短主题`。
3. 按需要使用 `Added`、`Changed`、`Fixed`、`Removed` 或 `Security`；没有内容的分类不要保留。
4. 每条 bullet 说明新增或改变了什么能力、行为或用户结果，不写成文件名清单。
5. Change Log 与对应代码或文档放在同一批 commit 中，不能在功能推送后再补。

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
