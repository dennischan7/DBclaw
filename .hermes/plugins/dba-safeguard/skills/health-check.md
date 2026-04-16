# Health Check Skill

## 目标
对数据库实例执行健康检查，识别性能瓶颈和配置问题。

## 检查项目

### 1. 连接状态
- 调用 `db_connect` 测试连接
- 确认连接延迟

### 2. 慢查询分析 (MySQL)
```sql
-- 查看慢查询状态
SHOW VARIABLES LIKE 'slow_query%';
SHOW VARIABLES LIKE 'long_query_time';

-- 查看当前运行中的查询
SELECT * FROM information_schema.PROCESSLIST
WHERE TIME > 5 ORDER BY TIME DESC;
```

### 3. 表空间检查
```sql
-- MySQL: 查看数据库大小
SELECT TABLE_SCHEMA, 
       ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS size_mb
FROM information_schema.TABLES
GROUP BY TABLE_SCHEMA ORDER BY size_mb DESC;

-- 查看大表
SELECT TABLE_NAME, TABLE_ROWS,
       ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
       ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS index_mb
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY DATA_LENGTH DESC LIMIT 20;
```

### 4. 索引使用情况
```sql
-- MySQL: 未使用的索引
SELECT * FROM sys.schema_unused_indexes;

-- 重复索引
SELECT * FROM sys.schema_redundant_indexes;
```

### 5. 锁等待检查
```sql
-- MySQL 5.7+: 查看锁等待
SELECT * FROM information_schema.INNODB_LOCK_WAITS;
SELECT * FROM information_schema.INNODB_LOCKS;
```

## 工作流
1. 连接数据库
2. 按数据库类型选择对应检查SQL
3. 使用 `library_search` 确认SQL兼容性
4. 通过 `sql_validate` 校验
5. 通过 `db_execute` (L0只读) 执行
6. 汇总分析结果，给出优化建议
