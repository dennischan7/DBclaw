# DBclaw v0.1.0

DBclaw 的首个公开版本。

DBclaw 是一个基于 Hermes 架构演化而来的数据库专家系统，面向 DBA、数据开发、数据治理和企业数据库运维场景。它的重点不是“让模型直接写 SQL”，而是先汇聚多类数据库官方文档、方言知识和运行上下文，再在这些基准之上生成候选 SQL，并继续走完安全流水线。

## 本版重点

- 文档基线驱动的 SQL 生成，而不是裸生成 SQL
- 自然语言请求先生成候选 SQL，再进入 DBA 安全流水线
- L0-L4 风险分级与五档安全模式
- 审批、审计、回滚、记忆、RAG、技能体系
- WebUI 支持 SQL 对话、仪表盘、审计日志、配置管理
- 查询结果支持聊天内表格预览与滚动增量加载

## 适合谁使用

- 希望把自然语言数据库交互落入真实运维流程的 DBA 团队
- 需要可审计、可审批、可回滚数据库 AI 助手的平台团队
- 需要私有化部署数据库专家系统的企业内部团队
- 希望基于 Hermes 工程基线继续做数据库垂直化演进的开发者

## 安装与启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .

$env:HERMES_ENABLE_PROJECT_PLUGINS = "true"
$env:DBA_SAFEGUARD_ENABLED = "true"

python -B webui/server.py
```

启动后默认访问：`http://127.0.0.1:8787`

## 需要注意

- 当前仓库只接入了部分数据库官方文档，后续还会继续补充更多语法与运维说明文档
- DBclaw 的公开版本线从 `v0.1.0` 开始计算
- 仓库中的旧 `RELEASE_v0.2.0` 到 `RELEASE_v0.9.0` 文档来自上游 Hermes 基线说明，不代表 DBclaw 自身历史版本
- 发布前请确认仓库中未提交真实数据库密码或 API Key

## 来源说明

DBclaw 基于 Hermes 的 MIT 开源工程基线继续演化而来，并在其之上增加数据库安全流水线、文档增强 SQL 生成、审批审计和 DBA 专用 WebUI 能力。对外发布时建议保留这一来源说明，以避免版本历史与项目归属产生误解。