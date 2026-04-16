# Troubleshooting Skill

## 目标
诊断和解决数据库常见故障，包括死锁、慢查询、连接耗尽、空间不足等。

## 故障诊断流程

### 1. 信息收集
- 确认故障现象（错误信息、响应时间、影响范围）
- 确认数据库类型和版本
- 调用 `db_connect` 确认连接状态

### 2. 常见问题诊断

#### 死锁
```sql
-- MySQL: 查看最近死锁信息
SHOW ENGINE INNODB STATUS;

-- PostgreSQL: 查看锁冲突
SELECT * FROM pg_locks WHERE NOT granted;
```

#### 慢查询
```sql
-- 当前长时间运行SQL
-- MySQL:
SELECT * FROM information_schema.PROCESSLIST WHERE TIME > 10;
-- PostgreSQL:
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity WHERE state != 'idle'
ORDER BY duration DESC;
```

#### 连接耗尽
```sql
-- MySQL: 查看连接数
SHOW STATUS LIKE 'Threads_connected';
SHOW VARIABLES LIKE 'max_connections';
-- PostgreSQL:
SELECT count(*) FROM pg_stat_activity;
SHOW max_connections;
```

#### 空间不足
```sql
-- MySQL: 查看表空间
SELECT TABLE_SCHEMA, ROUND(SUM(DATA_LENGTH + INDEX_LENGTH)/1024/1024, 2) AS MB
FROM information_schema.TABLES GROUP BY TABLE_SCHEMA;
```

### 3. 知识库参考
调用 `library_search` 搜索：
- 特定错误码的官方解释
- 配置参数的调优建议
- 版本特定的已知Bug

### 4. 经验库参考
调用 `dba_memory_search` 搜索：
- 历史类似问题的解决方案
- 该实例的历史故障记录

### 5. 解决方案
- 给出具体操作步骤
- 所有SQL经过 `sql_validate` 校验
- 写操作按风险等级走审批流程
- 记录解决过程到 `dba_memory_save`

## 安全准则
- 诊断查询全部为只读(L0)
- 修复操作严格按风险分级审批
- 生产环境操作必须确认回滚方案
- 所有操作自动审计记录
