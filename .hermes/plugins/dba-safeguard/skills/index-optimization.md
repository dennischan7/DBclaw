# Index Optimization Skill

## 目标
分析查询执行计划，识别缺失索引或冗余索引，给出优化建议。

## 工作流程

### 1. 收集慢查询
- 从用户提供的SQL或慢查询日志获取待优化SQL
- 确认目标数据库类型和版本

### 2. 执行计划分析
调用 `explain_analyze` 获取执行计划：
- 全表扫描 (type=ALL / Seq Scan)
- 文件排序 (Using filesort)
- 临时表 (Using temporary)
- 预估扫描行数

### 3. 现有索引检查
调用 `metadata_read` (info_type="indexes") 查看当前索引。

### 4. 索引建议生成
根据执行计划和现有索引：
- WHERE条件列 → 考虑单列/组合索引
- JOIN条件列 → 确保有索引
- ORDER BY/GROUP BY列 → 考虑覆盖索引
- 选择性低的列（如性别）→ 不建议单独建索引

### 5. 索引影响评估
- 索引对INSERT/UPDATE性能的影响
- 索引空间占用估算
- 是否存在冗余索引需要清理

### 6. 生成DDL
按 ddl-change-workflow 流程：
- 生成 CREATE INDEX 语句
- `sql_validate` 校验
- `rollback_generate` 生成 DROP INDEX 回滚
- 人工确认后执行

## MySQL索引建议公式
```
索引选择性 = COUNT(DISTINCT column) / COUNT(*)
选择性 > 0.1 → 适合建索引
选择性 < 0.01 → 不适合单独建索引
```

## 注意事项
- 组合索引遵循最左前缀原则
- 覆盖索引可避免回表
- 过多索引影响写入性能
- Online DDL (MySQL 5.6+) 支持在线建索引
