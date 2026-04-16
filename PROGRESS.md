# DB-SafeGuard Enterprise v2.0 — 开发进度跟踪

> **本文档实时记录每个开发任务的完成状态，断线重连后以此为准。**
> 最后更新: 2026-04-16

---

## 当前状态速览

| 项目 | 值 |
|---|---|
| **当前阶段** | 阶段0 ✅ → 阶段1 准备开始 |
| **Git 分支** | `dev` (开发中) |
| **最新提交** | `b7cd95b` feat: Phase 0 - DBA SafeGuard plugin skeleton |
| **基线提交** | `64bfc36` Initial: Hermes v0.9.0 + DBSafeGuard docs and library |
| **测试数据库** | PostgreSQL 15 @ localhost:5437 (Docker: ent-health-postgres-kimi) |

---

## 阶段0：项目基线与开发规范定版 ✅ 已完成

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 0.1 | Hermes v0.9.0 源码提取合并 | ✅ 完成 | `64bfc36` | 从 hermes-agent-2026.4.13.zip 解压合并 |
| 0.2 | Git 初始化 (main + dev 分支) | ✅ 完成 | `64bfc36` | main=稳定, dev=开发 |
| 0.3 | 插件目录骨架创建 | ✅ 完成 | `b7cd95b` | `.hermes/plugins/dba-safeguard/` |
| 0.4 | plugin.yaml 插件清单 | ✅ 完成 | `b7cd95b` | 12 tools, 5 hooks 声明 |
| 0.5 | `__init__.py` 插件入口 | ✅ 完成 | `b7cd95b` | register(ctx) 编排 |
| 0.6 | 8个工具模块骨架 | ✅ 完成 | `b7cd95b` | 含实际业务逻辑，非空桩 |
| 0.7 | 4个钩子模块骨架 | ✅ 完成 | `b7cd95b` | risk/context/audit/session hooks |
| 0.8 | DBAMemoryProvider (L2+L4) | ✅ 完成 | `b7cd95b` | SQLite FTS5 经验库 |
| 0.9 | CLI 子命令模块 | ✅ 完成 | `b7cd95b` | hermes dba {status,instances,audit,test-connect} |
| 0.10 | 配置文件 | ✅ 完成 | `b7cd95b` | hitl_matrix.yaml + dba_config.yaml |
| 0.11 | 5个 Skill MD 工作流 | ✅ 完成 | `b7cd95b` | sql-safe/ddl/health/index/troubleshooting |
| 0.12 | pyproject.toml [dba] 依赖组 | ✅ 完成 | `b7cd95b` | sqlglot/sqlalchemy/pymysql/psycopg2/cx_Oracle/pyodbc |
| 0.13 | .env.example DBA 变量 | ✅ 完成 | `b7cd95b` | HERMES_ENABLE_PROJECT_PLUGINS + DBA_SAFEGUARD_ENABLED |

**阶段0产出文件清单 (28 files, 3156 lines):**
```
.hermes/plugins/dba-safeguard/
├── __init__.py                          # 插件入口 register(ctx)
├── plugin.yaml                          # 插件清单
├── cli.py                               # CLI子命令
├── config/dba_config.yaml               # 数据库实例+角色配置
├── harnesses/
│   ├── __init__.py
│   ├── risk_interceptor.py              # pre_tool_call L0-L4拦截
│   ├── context_injector.py              # pre_llm_call DBA提示注入
│   ├── audit_hook.py                    # post_tool_call 审计记录
│   ├── session_hooks.py                 # 会话生命周期
│   ├── contracts/hitl_matrix.yaml       # HITL决策矩阵
│   ├── stages/                          # (待填充) 场景工作流
│   └── taxonomy/                        # (待填充) 意图分类规则
├── memory/
│   ├── __init__.py
│   └── dba_memory_provider.py           # L2工作记忆 + L4 FTS5经验库
├── skills/
│   ├── sql-safe-generation.md
│   ├── ddl-change-workflow.md
│   ├── health-check.md
│   ├── index-optimization.md
│   └── troubleshooting.md
├── tools/
│   ├── __init__.py
│   ├── db_connector.py                  # ConnectionManager (SQLAlchemy 2.x)
│   ├── sql_ast_validator.py             # sqlglot AST L0-L4风险分级
│   ├── explain_analyzer.py              # EXPLAIN执行计划分析
│   ├── metadata_reader.py               # 元数据读取 + 1h缓存
│   ├── rollback_generator.py            # AST回滚脚本生成
│   ├── safe_executor.py                 # 审批后安全执行
│   ├── audit_logger.py                  # SQLite审计日志
│   └── library_search.py               # RAG知识库检索
├── data/                                # 运行时数据目录
└── tests/                               # 测试目录
```

---

## 阶段1：SQL双层校验深化 🔜 即将开始

> **目标**: 将 sql_ast_validator.py 和 explain_analyzer.py 从骨架提升为
> 可通过真实数据库验证的生产级实现，跑通 `校验 → EXPLAIN → 风险定级` 完整链路。

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 1.1 | 安装 DBA 依赖 (sqlglot, sqlalchemy, psycopg2) | ⬜ 未开始 | | |
| 1.2 | 配置测试 PostgreSQL 实例 (dba_config.yaml) | ⬜ 未开始 | | Docker: localhost:5437 |
| 1.3 | sql_ast_validator 单元测试 (纯离线) | ⬜ 未开始 | | 覆盖 SELECT/INSERT/UPDATE/DELETE/DDL/各方言 |
| 1.4 | sql_ast_validator PG 方言强化 | ⬜ 未开始 | | 校验 PostgreSQL 15 特有语法 |
| 1.5 | db_connector → PostgreSQL 连接验证 | ⬜ 未开始 | | 通过测试容器连通 |
| 1.6 | explain_analyzer → 真实 EXPLAIN 验证 | ⬜ 未开始 | | 用 PG 真实表跑执行计划 |
| 1.7 | metadata_reader → PG information_schema 验证 | ⬜ 未开始 | | 读取真实表结构 |
| 1.8 | risk_interceptor 集成测试 | ⬜ 未开始 | | pre_tool_call → validate → HITL 链路 |
| 1.9 | library_search → PG 文档检索验证 | ⬜ 未开始 | | library/postgres/15/ 内容匹配 |
| 1.10 | 端到端链路测试: validate → explain → risk → audit | ⬜ 未开始 | | 全流程打通 |

---

## 阶段2：核心工具层与安全沙箱 ⬜ 未开始

> 对应开发计划"阶段2"，在阶段1校验链路跑通后继续深化。

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 2.1 | safe_executor 完整实现 (事务/超时/重试) | ⬜ | | |
| 2.2 | rollback_generator 基于元数据生成精确回滚 | ⬜ | | |
| 2.3 | audit_logger CSV 批量导出 | ⬜ | | |
| 2.4 | 连接池压测 (并发连接管理) | ⬜ | | |
| 2.5 | MySQL 方言适配验证 | ⬜ | | |
| 2.6 | Oracle 方言适配验证 | ⬜ | | |
| 2.7 | SQL Server 方言适配验证 | ⬜ | | |
| 2.8 | 工具层单元测试 ≥80% 覆盖率 | ⬜ | | |

---

## 阶段3：Harness规范引擎与意图路由 ⬜ 未开始

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 3.1 | RAG 知识库检索优化 (切片≤1000 token) | ⬜ | | |
| 3.2 | 意图分类 Prompt + 路由引擎 | ⬜ | | |
| 3.3 | harnesses/stages/ 场景工作流规范 | ⬜ | | |
| 3.4 | harnesses/taxonomy/ 意图分类规则 | ⬜ | | |
| 3.5 | 规范热重载机制 | ⬜ | | |

---

## 阶段4：闭环执行引擎与多智能体流水线 ⬜ 未开始

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 4.1 | DBA 主 Agent Loop (继承 AIAgent) | ⬜ | | |
| 4.2 | 双校验子 Agent (语法 + 性能, delegate_task) | ⬜ | | |
| 4.3 | 任务预检模块 | ⬜ | | |
| 4.4 | 断点续跑与状态管理 | ⬜ | | |

---

## 阶段5：企业级多级记忆中枢 ⬜ 未开始

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 5.1 | L1 工作区记忆 (4000 token 上限) | ⬜ | | |
| 5.2 | L2 情景会话记忆 (DBA 标签扩展) | ⬜ | | |
| 5.3 | L3 运维经验记忆 (向量化 + 人工确认) | ⬜ | | |
| 5.4 | L4 业务图谱与用户建模 | ⬜ | | |

---

## 阶段6：自进化DBA技能体系 ⬜ 未开始

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 6.1 | DBA 内置技能库完善 | ⬜ | | |
| 6.2 | 自主技能生成机制 | ⬜ | | |
| 6.3 | 技能自我优化 + 版本管理 | ⬜ | | |
| 6.4 | 技能权限管控 | ⬜ | | |

---

## 阶段7：零信任安全管控与五档人机协同 ⬜ 未开始

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 7.1 | L0-L4 风险分级体系完善 | ⬜ | | |
| 7.2 | 五档人机协同模式 | ⬜ | | |
| 7.3 | 人工审批流程 (SSE 推送) | ⬜ | | |

---

## 阶段8-10：前端/集成/测试 ⬜ 未开始

> 后续阶段待前面核心引擎完成后展开。

---

## 测试环境

| 实例名 | 类型 | 主机 | 端口 | 数据库 | 容器 | 状态 |
|--------|------|------|------|--------|------|------|
| pg_test | PostgreSQL 15 | localhost | 5437 | health_db_kimi | ent-health-postgres-kimi | ✅ 运行中 |

---

## 关键架构决策记录

| # | 决策 | 结果 | 日期 |
|---|------|------|------|
| D1 | 代码扩展方式 | Plugin模式 (不修改Hermes源码) | 2026-04-15 |
| D2 | 记忆体系 | 单一 MemoryProvider 实现 L1-L4 | 2026-04-15 |
| D3 | 上下文注入 | pre_llm_call 钩子注入 | 2026-04-15 |
| D4 | 风险拦截 | pre_tool_call 钩子拦截 | 2026-04-15 |
| D5 | 前端优先级 | CLI优先，UI后续 | 2026-04-15 |
| D6 | 双Agent校验 | delegate_task 子代理 | 2026-04-15 |
| D7 | 代码获取方式 | 克隆+断开远程 (实际zip下载) | 2026-04-15 |
| D8 | Hermes版本 | 锁定 v0.9.0 (v2026.4.13) | 2026-04-15 |
| D9 | Python版本 | 3.11 | 2026-04-15 |
| D10 | 开发模式 | 本地开发 | 2026-04-15 |

---

## 变更日志

| 日期 | 提交 | 内容 |
|------|------|------|
| 2026-04-15 | `64bfc36` | 初始提交: Hermes v0.9.0 + 项目文档 + library/ 知识库 |
| 2026-04-16 | `b7cd95b` | Phase 0 完成: DBA SafeGuard 插件骨架 (28文件, 3156行) |
