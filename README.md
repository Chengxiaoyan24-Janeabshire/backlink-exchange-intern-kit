# Backlink Exchange Agent

## 1. 整个 Agent 的逻辑

```text
用户请求
   │
   ├─ 外链合作评估
   │   └─ $evaluate-backlink-exchange
   │       ├─ 评估公司服务、DA/DR、流量和内容相关度
   │       ├─ 找到对方 5 篇适合插入 Milvus/Zilliz 链接的 Blog
   │       ├─ 匹配我方 1–2 篇 Blog + 3 篇 Milvus AI Quick Reference
   │       └─ 创建 Feishu Evaluation Doc，并把链接写入 Evaluation 字段
   │
   ├─ Gmail 邮件同步
   │   └─ $sync-backlink-gmail
   │       ├─ 读取 Organic Exchange 中的沟通记录
   │       ├─ 搜索并同步对应 Gmail Thread
   │       ├─ 清除回复中重复引用的历史邮件
   │       ├─ 更新 对接概括 和 Responce，保留人工 Next Step
   │       ├─ 追加完整 Communication Thread
   │       └─ 将每个黄色高亮片段分别沉淀为模板 Wiki 中的 Context + Template
   │
   └─ 起草下一封回复
       └─ $draft-backlink-reply
           ├─ 读取人工填写的 Next Step
           ├─ 读取完整 Communication Thread
           ├─ 匹配模板 Wiki 中的 Context
           └─ 在 Thread 末尾追加 Next Draft
```

三条流程相互独立：Evaluation 不同步 Gmail；Gmail sync 不生成回复；Next Draft 只能人工触发。

## 2. Skills 与触发方式

| Skill | 功能 | 直接触发 | 自然语言触发示例 |
|---|---|---|---|
| `evaluate-backlink-exchange` | 完整评估合作方并写入 Feishu Evaluation Doc | `$evaluate-backlink-exchange` | “给这个网站跑外链 evaluation”“重新评估这个 Organic Exchange 合作方” |
| `assess-backlink-health` | 只评估公司服务、Authority、流量和内容相关度 | `$assess-backlink-health` | “只看这个网站的 backlink health”“比较它和 Milvus、Zilliz 的 DA 和流量” |
| `find-partner-blog-pages` | 找到对方 5 篇适合插入我方链接的 Blog | `$find-partner-blog-pages` | “找对方 5 篇适合放 Milvus 链接的文章” |
| `match-our-placement-pages` | 匹配我方 1–2 篇 Blog 和 3 篇 Milvus AI Quick Reference | `$match-our-placement-pages` | “找我们这边适合放对方链接的页面” |
| `sync-backlink-gmail` | 同步 Gmail、更新 Feishu 字段和 Thread，并沉淀高亮模板 | `$sync-backlink-gmail` | “同步最新的外链邮件”“刷新 Organic Exchange Gmail Thread” |
| `draft-backlink-reply` | 根据 Next Step、完整 Thread 和模板 Wiki 生成 Next Draft | `$draft-backlink-reply` | “根据 Next Step 起草下一封回复”“给这个 Thread 写 Next Draft” |
