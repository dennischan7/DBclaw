# DB-SafeGuard Enterprise — 人工测试指引

> 本指引覆盖 Phase 0–7 所有功能点，帮助你逐项验证系统在真实环境中的行为。
> 建议按顺序执行，后续模块依赖前置模块的环境准备。

---

## 0. 环境准备

### 0.1 启动 PostgreSQL 容器

```bash
# 启动已有容器
docker start ent-health-postgres-kimi

# 或首次创建
docker run -d --name ent-health-postgres-kimi \
  -e POSTGRES_USER=dbclaw_test_user \
  -e POSTGRES_PASSWORD=dbclaw_test_password \
  -e POSTGRES_DB=health_db_kimi \
  -p 5437:5432 \
  postgres:15

# 验证
docker ps --filter name=ent-health-postgres-kimi   # Status: Up ... (healthy)
```

### 0.2 设置环境变量

```bash
# Windows PowerShell
$env:DBA_PG_TEST_RO_USER = "dbclaw_test_user"
$env:DBA_PG_TEST_RO_PASS = "dbclaw_test_password"
$env:DBA_PG_TEST_ADMIN_USER = "dbclaw_test_user"
$env:DBA_PG_TEST_ADMIN_PASS = "dbclaw_test_password"
$env:DBA_SAFEGUARD_ENABLED = "true"
$env:HERMES_ENABLE_PROJECT_PLUGINS = "true"

# Linux/macOS
export DBA_PG_TEST_RO_USER=dbclaw_test_user
export DBA_PG_TEST_RO_PASS=dbclaw_test_password
export DBA_PG_TEST_ADMIN_USER=dbclaw_test_user
export DBA_PG_TEST_ADMIN_PASS=dbclaw_test_password
```

### 0.3 运行自动化测试（基线对照）

```bash
cd H:\DBClaw2
python -m pytest .hermes/plugins/dba-safeguard/tests/ -v -o "addopts=" --tb=short
# 预期: 392 passed, 0 failed, 0 skipped
```

### 0.4 准备测试表

```sql
-- 连接 PG (psql -h localhost -p 5437 -U dbclaw_test_user -d health_db_kimi)
CREATE TABLE IF NOT EXISTS test_manual (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    status INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
INSERT INTO test_manual (name, status) VALUES ('alpha', 1), ('beta', 2), ('gamma', 3);
CREATE INDEX IF NOT EXISTS idx_test_manual_status ON test_manual(status);
```

---

## 1. SQL校验与风险分级 (Phase 1 + 7)

### 1.1 AST离线校验

| # | 操作 | 预期结果 | ✓ |
|---|------|---------|---|
| 1 | 向Hermes发送: "验证SQL: `SELECT * FROM test_manual`" | 返回: valid=true, risk_level=L0 (READONLY) | ☐ |
| 2 | "验证SQL: `INSERT INTO test_manual (name) VALUES ('test')`" | valid=true, risk_level=L1 (LOW_DML) | ☐ |
| 3 | "验证SQL: `UPDATE test_manual SET status=0 WHERE id=1`" | valid=true, risk_level=L2 (MEDIUM_BATCH) | ☐ |
| 4 | "验证SQL: `DELETE FROM test_manual`" (无WHERE) | risk_level=**L4** (CATASTROPHIC)，硬编码升级 | ☐ |
| 5 | "验证SQL: `DROP TABLE test_manual`" | risk_level=**L4** (CATASTROPHIC) | ☐ |
| 6 | "验证SQL: `TRUNCATE TABLE test_manual`" | risk_level=L3 (HIGH_DESTRUCTIVE) | ☐ |
| 7 | "验证SQL: `ALTER TABLE test_manual ADD COLUMN remark TEXT`" | risk_level=L2 | ☐ |
| 8 | "验证SQL: `ALTER TABLE test_manual DROP COLUMN remark`" | risk_level=**L3** | ☐ |
| 9 | 发送语法错误SQL: `SELCT * FORM table` | valid=false, 报告语法错误 | ☐ |

### 1.2 多方言离线校验

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 10 | MySQL语法: `` SELECT `name` FROM test_manual LIMIT 10 `` | valid=true (MySQL dialect) | ☐ |
| 11 | Oracle语法: `SELECT name FROM test_manual WHERE ROWNUM <= 10` | valid=true (Oracle dialect) | ☐ |
| 12 | T-SQL语法: `SELECT TOP 10 name FROM test_manual` | valid=true (TSQL dialect) | ☐ |

### 1.3 硬编码兜底规则 (Phase 7)

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 13 | `UPDATE test_manual SET status=0` (无WHERE) | 强制升级到L4，不可通过配置降级 | ☐ |
| 14 | `DROP DATABASE health_db_kimi` | 强制L4，不可降级 | ☐ |
| 15 | 添加自定义规则后重试#13 | 硬编码规则优先，仍为L4 | ☐ |

### 1.4 自定义风险规则

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 16 | 添加规则: pattern=`.*sensitive_table.*`, escalate_to=L3 | 规则入库成功 | ☐ |
| 17 | 验证: `SELECT * FROM sensitive_table` | 风险从L0升级到L3 | ☐ |
| 18 | 删除该规则 | 恢复原始L0评估 | ☐ |

---

## 2. 数据库连接与元数据 (Phase 1)

### 2.1 连接管理

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 19 | "连接到 pg_test 实例" | 建立只读+管理连接，返回连接信息 | ☐ |
| 20 | "断开 pg_test" | 连接关闭确认 | ☐ |
| 21 | 未设置DBA_PG_TEST_RO_PASS时连接 | 返回明确错误，不崩溃 | ☐ |
| 22 | 设置错误密码后连接 | 返回连接失败错误 | ☐ |

### 2.2 元数据读取

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 23 | "列出 pg_test 的所有表" | 返回表列表 (含test_manual) | ☐ |
| 24 | "查看 test_manual 的结构" | 返回列名、类型、约束 | ☐ |
| 25 | "查看 test_manual 的索引" | 返回idx_test_manual_status等 | ☐ |
| 26 | "生成 test_manual 的DDL" | 返回CREATE TABLE完整语句 | ☐ |

### 2.3 EXPLAIN分析

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 27 | "分析执行计划: `SELECT * FROM test_manual WHERE id = 1`" | 返回Index Scan，标记高效 | ☐ |
| 28 | "分析执行计划: `SELECT * FROM test_manual WHERE name LIKE '%test%'`" | 返回Seq Scan，标记⚠️全表扫描 | ☐ |
| 29 | "分析执行计划: `SELECT * FROM test_manual WHERE status = 1`" | 返回Index Scan (有索引) | ☐ |

---

## 3. 安全执行与回滚 (Phase 2)

### 3.1 只读连接安全性

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 30 | 通过只读连接执行INSERT | 被拒绝，返回权限错误 | ☐ |
| 31 | 通过只读连接执行SELECT | 正常返回结果 | ☐ |

### 3.2 回滚脚本生成

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 32 | 为INSERT生成回滚 | 生成精确的DELETE WHERE条件 | ☐ |
| 33 | 为ALTER ADD COLUMN生成回滚 | 生成ALTER DROP COLUMN | ☐ |
| 34 | 为ALTER DROP COLUMN生成回滚 | 含元数据的ALTER ADD还原 | ☐ |
| 35 | 为DROP TABLE生成回滚 | 含完整DDL的CREATE TABLE | ☐ |
| 36 | 为TRUNCATE生成回滚 | 标记为"不可回滚" | ☐ |

### 3.3 事务封装执行

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 37 | 执行INSERT并确认 | 在事务中执行，审计日志记录 | ☐ |
| 38 | 执行UPDATE WHERE id=1并确认 | 事务提交，行已更新 | ☐ |
| 39 | 执行错误SQL（语法错误） | 事务回滚，返回错误信息 | ☐ |

### 3.4 审计日志

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 40 | 执行几条SQL后查询审计日志 | 返回执行记录（时间、SQL、风险等级、结果） | ☐ |
| 41 | 按风险等级过滤审计日志 | 仅返回指定等级的记录 | ☐ |
| 42 | 按时间范围过滤 | 仅返回范围内记录 | ☐ |
| 43 | 导出CSV | 生成格式正确的CSV文件 | ☐ |

---

## 4. 意图路由与上下文注入 (Phase 3)

### 4.1 意图分类

在对话中发送以下自然语言，验证路由结果:

| # | 输入 | 预期意图 | 预期stage | ✓ |
|---|------|---------|-----------|---|
| 44 | "帮我查一下test_manual有多少条记录" | query_execution | query-execution.md | ☐ |
| 45 | "往test_manual插入一条新数据name=delta" | dml_execution | dml-execution.md | ☐ |
| 46 | "给test_manual添加一个email列" | ddl_change | ddl-change.md | ☐ |
| 47 | "分析一下test_manual的查询性能" | optimization | optimization.md | ☐ |
| 48 | "检查一下数据库的健康状况" | health_check | health-check.md | ☐ |
| 49 | "数据库有死锁怎么排查" | troubleshooting | troubleshooting.md | ☐ |

### 4.2 上下文注入

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 50 | 在连接pg_test后发送查询意图 | pre_llm_call注入当前实例信息、元数据 | ☐ |
| 51 | 检查LLM请求是否包含表结构上下文 | 系统提示中出现test_manual的结构信息 | ☐ |

### 4.3 配置热重载

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 52 | 修改dba_config.yaml的execution_timeout值 | 无需重启，新值生效 | ☐ |
| 53 | 修改intent_classification.yaml添加新关键词 | 热重载后新关键词可路由 | ☐ |

---

## 5. 闭环执行引擎 (Phase 4)

### 5.1 完整流水线

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 54 | 发送SELECT查询请求 | 9阶段流水线: 意图解析→预检→校验→EXPLAIN→(跳过回滚和审批)→执行→审计 | ☐ |
| 55 | 发送INSERT请求 | L1流水线: 含EXPLAIN和通知，跳过人工审批 | ☐ |
| 56 | 发送UPDATE WHERE请求 | L2流水线: 需人工确认→confirm后执行 | ☐ |
| 57 | 发送DROP TABLE请求 | L4流水线: 强制阻断，需管理员审批 | ☐ |

### 5.2 双校验

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 58 | 发送包含全表扫描的UPDATE | 性能校验器发出告警 | ☐ |
| 59 | 一票否决: 语法校验通过但性能否决 | 整体标记为需重写 | ☐ |

### 5.3 预检

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 60 | 对不存在的表执行操作 | 预检发现表不存在，提示用户 | ☐ |
| 61 | 权限不足的操作 | 预检检测到权限问题 | ☐ |

### 5.4 断点续跑

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 62 | 发起一个L2操作到审批阶段 | 任务暂停在审批阶段 | ☐ |
| 63 | 执行审批通过 | 从断点继续执行余下阶段 | ☐ |
| 64 | 查看任务状态 | 显示各阶段完成状态 | ☐ |

---

## 6. 多级记忆 (Phase 5)

### 6.1 L1 工作区记忆

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 65 | 在同一会话中多次查询 | 后续查询感知到前文(如上次查的表) | ☐ |
| 66 | 发送大量内容直到超过4000 token | 低优先级条目被淘汰，高优先级保留 | ☐ |

### 6.2 L2 会话记忆

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 67 | 结束会话后重新开始 | 搜索上一次会话记录可找到 | ☐ |
| 68 | 搜索"test_manual" | FTS5返回相关历史记录 | ☐ |

### 6.3 L3 经验蒸馏

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 69 | 完成一次完整操作后检查经验库 | 生成pending状态的经验条目 | ☐ |
| 70 | 确认该经验 | 状态变为confirmed，可被后续查询引用 | ☐ |
| 71 | 拒绝一条经验 | 状态变为rejected，不再出现 | ☐ |

### 6.4 L4 业务图谱

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 72 | 多次操作test_manual后查图谱 | 显示表关系和操作频率 | ☐ |
| 73 | 搜索业务字典 | FTS5返回业务术语定义 | ☐ |
| 74 | 查询用户画像 | 显示操作偏好和风险倾向 | ☐ |

---

## 7. 技能系统 (Phase 6)

### 7.1 内置技能

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 75 | 列出所有技能 | 返回5个内置技能 | ☐ |
| 76 | 查看sql-safe-generation技能详情 | 返回技能描述和触发条件 | ☐ |
| 77 | 触发health-check技能 | 按技能定义的流程执行健康检查 | ☐ |

### 7.2 权限过滤

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 78 | 以viewer角色列出技能 | 仅显示L0相关技能 | ☐ |
| 79 | 以editor角色列出技能 | 显示L0-L2技能 | ☐ |
| 80 | 以admin角色列出技能 | 显示全部技能 | ☐ |

### 7.3 技能管理

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 81 | 禁用一个技能 | 该技能不再被触发 | ☐ |
| 82 | 重新启用 | 恢复正常触发 | ☐ |
| 83 | 查看技能执行统计 | 显示调用次数、成功率 | ☐ |

---

## 8. 安全管控 (Phase 7)

### 8.1 五档安全模式

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 84 | 查看当前安全模式 | 显示MODERATE (默认档位2) | ☐ |
| 85 | 切换到ULTRA_CONSERVATIVE (档位1) | 切换成功，L1操作也需审批 | ☐ |
| 86 | 在档位1下执行INSERT | 需要人工确认（不再自动通过） | ☐ |
| 87 | 切换到AGGRESSIVE (档位3) | L2操作自动通过 | ☐ |
| 88 | 在档位3下执行UPDATE WHERE | 自动通过，无需确认 | ☐ |
| 89 | 切换到READONLY_AUDIT (档位0) | 所有写操作被阻止 | ☐ |
| 90 | 在档位0下执行INSERT | 被拒绝，提示只读模式 | ☐ |
| 91 | 切换到MADMAN (档位4) | 要求输入管理员密码 | ☐ |
| 92 | 输入错误密码 | 切换失败 | ☐ |
| 93 | 输入正确密码 | 切换成功，所有操作自动通过 | ☐ |

### 8.2 模式锁定

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 94 | 锁定当前模式 | 锁定成功 | ☐ |
| 95 | 尝试切换模式 | 被拒绝，提示已锁定 | ☐ |
| 96 | 解锁 | 解锁后可切换 | ☐ |

### 8.3 审批流程

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 97 | 触发L2操作，创建审批请求 | 返回request_id，状态=PENDING | ☐ |
| 98 | 审批通过 | 状态→APPROVED，SQL可执行 | ☐ |
| 99 | 触发另一个请求，驳回 | 要求填写驳回原因，状态→REJECTED | ☐ |
| 100 | 不填原因直接驳回 | 被拒绝，原因字段必填 | ☐ |
| 101 | 修改SQL后审批 | 只有SQL内容可修改，风险等级不可改 | ☐ |

### 8.4 审计留痕

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 102 | 查看审批记录 | 所有审批操作有迹可循，不可篡改 | ☐ |
| 103 | 查看审批统计 | 显示通过/拒绝/待处理数量 | ☐ |

---

## 9. 知识库检索 (Phase 1)

| # | 操作 | 预期 | ✓ |
|---|------|------|---|
| 104 | "PostgreSQL的窗口函数怎么用" | 检索library/postgres/下相关文档 | ☐ |
| 105 | "Hive如何创建分桶表" | 检索library/hive/下文档 | ☐ |
| 106 | "MySQL 8.0的JSON函数" | 检索library/mysql/8.0/下文档 | ☐ |
| 107 | 检索不存在的主题 | 返回空结果或提示未找到，不报错 | ☐ |
| 108 | 跨库查询隔离 | 指定PG时不返回MySQL文档 | ☐ |

---

## 10. 端到端场景验证

### 10.1 典型DBA日常操作

| # | 场景 | 步骤 | 预期 | ✓ |
|---|------|------|------|---|
| 109 | 查询数据 | 连接→SELECT→返回结果 | L0自动通过，有审计 | ☐ |
| 110 | 插入数据 | 连接→INSERT→确认→执行 | L1执行，有回滚脚本 | ☐ |
| 111 | 批量更新 | 连接→UPDATE(大量行)→审批→执行 | L2需确认，有回滚 | ☐ |
| 112 | 加字段 | 连接→ALTER ADD→审批→执行 | L2，回滚为DROP COLUMN | ☐ |
| 113 | 删字段 | 连接→ALTER DROP→管理员审批→执行 | L3，回滚含元数据 | ☐ |
| 114 | 删表 | 连接→DROP TABLE→强制阻断 | L4，需管理员+DDL备份 | ☐ |

### 10.2 异常场景

| # | 场景 | 预期 | ✓ |
|---|------|------|---|
| 115 | 容器宕机后重试 | 连接失败→明确错误→恢复后可重连 | ☐ |
| 116 | 超时场景(execution_timeout) | 超时后事务自动回滚 | ☐ |
| 117 | 并发操作 | 连接池正确分配，不混用 | ☐ |

### 10.3 安全边界

| # | 场景 | 预期 | ✓ |
|---|------|------|---|
| 118 | SQL注入: `'; DROP TABLE test_manual; --` | 被AST校验拦截，不执行 | ☐ |
| 119 | 绕过审批直接执行L3操作 | 被risk_interceptor拦截 | ☐ |
| 120 | 在READONLY模式下尝试所有写操作 | 全部被阻止 | ☐ |

---

## 11. CLI子命令 (`hermes dba`)

| # | 命令 | 预期 | ✓ |
|---|------|------|---|
| 121 | `hermes dba status` | 显示插件状态、当前安全模式、活跃连接 | ☐ |
| 122 | `hermes dba instances` | 列出dba_config.yaml中所有实例 | ☐ |
| 123 | `hermes dba audit` | 显示最近审计记录 | ☐ |
| 124 | `hermes dba test-connect pg_test` | 测试连接并报告结果 | ☐ |

---

## 检查清单汇总

| 模块 | 测试项 | 数量 |
|------|--------|------|
| SQL校验与风险分级 | #1–#18 | 18 |
| 数据库连接与元数据 | #19–#29 | 11 |
| 安全执行与回滚 | #30–#43 | 14 |
| 意图路由与上下文 | #44–#53 | 10 |
| 闭环执行引擎 | #54–#64 | 11 |
| 多级记忆 | #65–#74 | 10 |
| 技能系统 | #75–#83 | 9 |
| 安全管控 | #84–#103 | 20 |
| 知识库检索 | #104–#108 | 5 |
| 端到端场景 | #109–#120 | 12 |
| CLI子命令 | #121–#124 | 4 |
| **合计** | | **124** |

---

## 测试完成标准

- [ ] 124项人工测试全部通过 (✓)
- [ ] 392项自动化测试全部通过
- [ ] 安全边界场景无一绕过
- [ ] 审计日志完整记录所有操作
- [ ] 五档模式切换行为符合预期
- [ ] 断点续跑功能正常
- [ ] 知识库跨库隔离有效
