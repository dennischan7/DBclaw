# DB-SafeGuard Enterprise v2.0 — 开发进度跟踪

> **本文档实时记录每个开发任务的完成状态，断线重连后以此为准。**
> 最后更新: 2026-04-16

---

## 当前状态速览

| 项目 | 值 |
|---|---|
| **当前阶段** | 阶段0 ✅ → 阶段1 ✅ → 阶段2 ✅ |
| **Git 分支** | `dev` (开发中) |
| **最新提交** | Phase 2 commit (待提交) |
| **基线提交** | `64bfc36` Initial: Hermes v0.9.0 + DBSafeGuard docs and library |
| **测试数据库** | PostgreSQL 15 @ localhost:5437 (Docker: ent-health-postgres-kimi) |
| **总测试数** | 134 (Phase 1: 78 + Phase 2: 56) |

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

## 阶段1：SQL双层校验深化 ✅ 已完成

> **目标**: 将 sql_ast_validator.py 和 explain_analyzer.py 从骨架提升为
> 可通过真实数据库验证的生产级实现，跑通 `校验 → EXPLAIN → 风险定级` 完整链路。

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 1.1 | 安装 DBA 依赖 (sqlglot, sqlalchemy, psycopg2) | ✅ 已完成 | | sqlglot 30.4.3, sqlalchemy 2.0.48, psycopg2-binary |
| 1.2 | 配置测试 PostgreSQL 实例 (dba_config.yaml) | ✅ 已完成 | 6ee1678 | Docker: localhost:5437 |
| 1.3 | sql_ast_validator 单元测试 (纯离线) | ✅ 已完成 | | 31项测试全部通过 |
| 1.4 | sql_ast_validator PG 方言强化 | ✅ 已完成 | | ALTER TABLE子操作识别(ADD/DROP/MODIFY/RENAME) |
| 1.5 | db_connector → PostgreSQL 连接验证 | ✅ 已完成 | | UTF-8编码修复 + readonly SELECT 1通过 |
| 1.6 | explain_analyzer → 真实 EXPLAIN 验证 | ✅ 已完成 | | PG EXPLAIN (ANALYZE false, COSTS true, FORMAT TEXT) 通过 |
| 1.7 | metadata_reader → PG information_schema 验证 | ✅ 已完成 | | **新增**: columns(information_schema) + indexes(pg_indexes) + DDL重建 |
| 1.8 | risk_interceptor 集成测试 | ✅ 已完成 | | L0放行/L1通知/L2人工确认/L3-L4阻断 全链路 |
| 1.9 | library_search → PG 文档检索验证 | ✅ 已完成 | | 跨库隔离验证通过 |
| 1.10 | 端到端链路测试: validate → explain → risk → audit | ✅ 已完成 | | **78项测试全部通过** |

### Phase 1 关键修复

1. **sql_ast_validator**: 增强 `_identify_operation()` ALTER TABLE子操作检测(DROP/ADD/MODIFY/RENAME)，修复 `ALTER TABLE DROP COLUMN` 误分为L2的bug
2. **db_connector**: `load_config()` 添加 `encoding="utf-8"` 参数，修复Windows下中文注释YAML文件读取失败
3. **metadata_reader**: 新增PG支持 — `_read_columns()`(information_schema.columns + pg_description注释), `_read_indexes()`(pg_indexes), `_read_ddl()`(information_schema重建DDL含主键)
4. **risk_interceptor**: 修复相对导入问题，支持包内外两种导入方式

---

## 阶段2：核心工具层与安全沙箱 ✅ 已完成

> 对应开发计划"阶段2"，在阶段1校验链路跑通后继续深化。

| # | 任务 | 状态 | 提交 | 备注 |
|---|------|------|------|------|
| 2.1 | safe_executor 完整实现 (事务/超时/快照/审计) | ✅ 已完成 | | 事务封装L1+, statement_timeout PG/MySQL, L2+ UPDATE/DELETE快照, 自动审计 |
| 2.2 | rollback_generator 基于元数据生成精确回滚 | ✅ 已完成 | | sqlglot AST isinstance类型检测, INSERT→精确DELETE, ALTER ADD/DROP/RENAME, 元数据列定义获取 |
| 2.3 | audit_logger CSV 批量导出 + 测试隔离 | ✅ 已完成 | | set_audit_db_path()测试隔离, export_audit_csv()批量导出 |
| 2.4 | 连接池并发隔离测试 | ✅ 已完成 | | 5项: 并发连接/池复用/只读隔离/引擎分离/多线程 |
| 2.5 | MySQL 方言适配验证 | ✅ 已完成 | | SELECT/INSERT/UPDATE/DROP/ALTER/DELETE无WHERE 6项离线测试 |
| 2.6 | Oracle 方言适配验证 | ✅ 已完成 | | SELECT(ROWNUM)/INSERT/UPDATE/TRUNCATE/DROP 5项离线测试 |
| 2.7 | SQL Server (TSQL) 方言适配验证 | ✅ 已完成 | | SELECT TOP/INSERT/UPDATE/DROP 4项离线测试 |
| 2.8 | 工具层测试 56项 + 全回归134项 | ✅ 已完成 | | Phase2单独56项, 含跨方言回滚4项 |

### Phase 2 关键实现

**safe_executor.py** — 完整重写:
1. **事务封装**: L1+操作在显式`BEGIN/COMMIT/ROLLBACK`事务中执行
2. **超时控制**: `_set_statement_timeout()` — PG: `SET statement_timeout`, MySQL: `SET max_execution_time`
3. **执行前快照**: L2+ UPDATE/DELETE自动用`_snapshot_affected_rows()`转换为SELECT快照受影响行
4. **自动审计**: `_audit_execution()`每次执行前后写入audit_logger

**rollback_generator.py** — 元数据驱动精确回滚:
1. **INSERT精确回滚**: `_extract_insert_values()`从Schema.expressions提取Identifier列名+Values值→生成精确`DELETE WHERE col1=val1 AND col2=val2`
2. **ALTER回滚**: `isinstance(action, exp.ColumnDef)`→ADD, `isinstance(action, exp.Drop)`→DROP, `isinstance(action, exp.RenameColumn)`→RENAME，不再使用字符串匹配
3. **DROP回滚**: `_fetch_table_ddl()`通过metadata_reader获取完整DDL备份
4. **列定义获取**: `_fetch_column_definition()`从PG/MySQL information_schema实时查询列定义（类型+默认值+NOT NULL+注释）
5. **回滚语法验证**: `_validate_rollback_sql()`用sqlglot解析验证生成的回滚SQL

### Phase 2 关键修复

1. **sqlglot INSERT AST**: `Schema.expressions`是`Identifier`节点（不是`Column`），需直接遍历并用`.name`属性
2. **sqlglot ALTER AST**: actions是类型化对象 — `ColumnDef`(ADD), `Drop`(DROP), `RenameColumn`(RENAME)，不能用`action.sql().startswith("ADD")`
3. **ConnectionManager单例**: `safe_executor`通过`get_connection_manager()`获取模块级单例，测试fixture需配置同一单例而非创建新实例

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
| 2026-04-16 | `pending` | Phase 1 完成: SQL双层校验深化 — 78项测试全部通过, 4项关键修复 |
