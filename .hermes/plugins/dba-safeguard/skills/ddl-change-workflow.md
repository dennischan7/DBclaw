# DDL Change Workflow Skill

## 目标
安全执行数据库结构变更（DDL），确保回滚可行、影响可控。

## 工作流程

### 1. 变更评估
- 确认变更类型（加字段/改类型/加索引/删除字段/重命名等）
- 确认影响表的行数规模
- 确认是否有依赖此表的视图/存储过程/外键

### 2. 元数据检查
调用 `metadata_read` 获取：
- 当前表结构 (columns)
- 现有索引 (indexes)
- 表DDL (ddl)

### 3. SQL生成与校验
- 调用 `library_search` 确认DDL语法
- 生成DDL语句
- 调用 `sql_validate` 校验
- 确认风险等级（通常L2-L3）

### 4. 回滚脚本
**L2+必须生成回滚脚本**
调用 `rollback_generate` 生成：
- ALTER TABLE ADD → ALTER TABLE DROP COLUMN
- ALTER TABLE MODIFY → ALTER TABLE MODIFY（恢复原类型）
- CREATE INDEX → DROP INDEX
- ALTER TABLE RENAME → ALTER TABLE RENAME（恢复原名）

### 5. 执行计划
调用 `explain_analyze`（如适用）评估性能影响。

### 6. 审批与执行
- L2: 展示变更和回滚脚本，人工确认后执行
- L3: 展示变更和回滚脚本，管理员审批后执行
- L4: 强制阻断，需充分论证后管理员审批

### 7. 执行后验证
执行后调用 `metadata_read` 验证变更是否生效。

## 注意事项
- MySQL Online DDL: 大表ALTER考虑使用 `ALGORITHM=INPLACE` 或 pt-osc
- PostgreSQL: ALTER TABLE大多数操作不锁表
- Oracle: 注意 `ALTER TABLE MOVE` 会使索引失效
