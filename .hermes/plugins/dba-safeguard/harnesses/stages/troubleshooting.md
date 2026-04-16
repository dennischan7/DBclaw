# 故障排查工作流 (Troubleshooting)

> 适用意图: `troubleshoot` — 死锁、锁等待、慢查询排查
> 风险等级: L0 (分析阶段)
> 审批要求: 无 (分析), 按操作类型审批 (修复)

## 执行流程

```
用户报告问题
  │
  ▼
┌─────────────────────┐
│ 1. 问题分类          │ → 识别问题类型
│    - 死锁/锁等待    │
│    - 慢查询         │
│    - 连接问题       │
│    - 复制延迟       │
│    - 空间不足       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 2. 知识库检索        │ → library_search(problem_type, db_type)
│    - 排查方法论      │    获取最佳排查步骤
│    - 已知问题模式    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 3. 诊断数据采集      │ → 只读查询采集状态
│    PG: pg_locks      │    当前锁信息
│    MySQL: SHOW ENGINE│    InnoDB状态
│    执行计划           │    慢查询执行计划
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. 问题分析          │ → 基于采集数据分析
│    - 根因定位        │    识别瓶颈/阻塞源
│    - 影响范围评估    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 5. 修复建议生成      │ → 生成修复方案
│    - KILL会话 (L3)   │    需审批
│    - 索引优化 (L2)   │    转入DDL工作流
│    - 配置调整        │    转入变更工作流
│    - 查询重写        │    建议方案
└─────────────────────┘
```

## 常见问题排查路径

| 问题类型 | PG 诊断查询 | MySQL 诊断查询 |
|---------|------------|---------------|
| 死锁 | `SELECT * FROM pg_locks WHERE NOT granted` | `SHOW ENGINE INNODB STATUS` |
| 慢查询 | `SELECT * FROM pg_stat_activity WHERE state='active' AND query_start < now()-'5s'::interval` | `SHOW FULL PROCESSLIST` |
| 连接满 | `SELECT count(*) FROM pg_stat_activity` | `SHOW STATUS LIKE 'Threads_connected'` |
| 表膨胀 | `SELECT pg_table_size(relid) FROM pg_stat_user_tables` | `SELECT data_length+index_length FROM information_schema.tables` |
