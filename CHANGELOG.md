# Changelog

本文件记录 DBclaw 自有版本线的正式变更。

旧的 `RELEASE_v0.2.0` 到 `RELEASE_v0.9.0` 文档来自上游 Hermes 基线说明，已归档到 `docs/upstream-notes/`，不计入 DBclaw 的产品版本历史。

## v0.1.0 - 2026-04-22

首个公开版本。

### Highlights

- 正式确立 DBclaw 品牌与独立版本线
- 基于多数据库官方文档、方言知识和运行上下文生成候选 SQL
- 自然语言数据库请求先生成候选 SQL，再进入 DBA 安全流水线
- 提供 L0-L4 风险分级与五档安全模式
- 提供审批、审计、回滚、记忆、RAG 和 DBA 技能体系
- WebUI 支持 SQL 对话、仪表盘、审计日志、配置管理和查询结果表格分页预览

### Release Engineering

- 项目元信息切换为 `DBclaw v0.1.0`
- 新增 `dbclaw` CLI 别名
- 新增首版发布检查清单与 GitHub Release 草稿
- 归档上游 Hermes 历史 release 文档

### Security

- 移除示例配置中的明文数据库账号密码
- 将示例环境变量与测试文档改为安全占位凭据
- 保留基于环境变量的数据库凭据注入方式