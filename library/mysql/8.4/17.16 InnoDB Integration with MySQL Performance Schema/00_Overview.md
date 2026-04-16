---
source: MySQL 8.4 Reference
title: 00_Overview
---

This section provides a brief introduction to InnoDB integration with Performance Schema. For comprehensive Performance Schema documentation, see Chapter 29, MySQL Performance Schema.

You can profile certain internal InnoDB operations using the MySQL Performance Schema feature. This type of tuning is primarily for expert users who evaluate optimization strategies to overcome

performance bottlenecks. DBAs can also use this feature for capacity planning, to see whether their typical workload encounters any performance bottlenecks with a particular combination of CPU, RAM, and disk storage; and if so, to judge whether performance can be improved by increasing the capacity of some part of the system.

To use this feature to examine InnoDB performance:

- You must be generally familiar with how to use the Performance Schema feature. For example, you should know how enable instruments and consumers, and how to query performance\_schema tables to retrieve data. For an introductory overview, see Section 29.1, "Performance Schema Quick Start".
- You should be familiar with Performance Schema instruments that are available for InnoDB. To view InnoDB-related instruments, you can query the setup\_instruments table for instrument names that contain 'innodb'.

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%innodb%';
+-------------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------------------+---------+-------+
| wait/synch/mutex/innodb/commit_cond_mutex | NO | NO |
| wait/synch/mutex/innodb/innobase_share_mutex | NO | NO |
| wait/synch/mutex/innodb/autoinc_mutex | NO | NO |
| wait/synch/mutex/innodb/buf_pool_mutex | NO | NO |
| wait/synch/mutex/innodb/buf_pool_zip_mutex | NO | NO |
| wait/synch/mutex/innodb/cache_last_read_mutex | NO | NO |
| wait/synch/mutex/innodb/dict_foreign_err_mutex | NO | NO |
| wait/synch/mutex/innodb/dict_sys_mutex | NO | NO |
| wait/synch/mutex/innodb/recalc_pool_mutex | NO | NO |
...
| wait/io/file/innodb/innodb_data_file | YES | YES |
| wait/io/file/innodb/innodb_log_file | YES | YES |
| wait/io/file/innodb/innodb_temp_file | YES | YES |
| stage/innodb/alter table (end) | YES | YES |
| stage/innodb/alter table (flush) | YES | YES |
| stage/innodb/alter table (insert) | YES | YES |
| stage/innodb/alter table (log apply index) | YES | YES |
| stage/innodb/alter table (log apply table) | YES | YES |
| stage/innodb/alter table (merge sort) | YES | YES |
| stage/innodb/alter table (read PK and internal sort) | YES | YES |
| stage/innodb/buffer pool load | YES | YES |
| memory/innodb/buf_buf_pool | NO | NO |
| memory/innodb/dict_stats_bg_recalc_pool_t | NO | NO |
| memory/innodb/dict_stats_index_map_t | NO | NO |
| memory/innodb/dict_stats_n_diff_on_level | NO | NO |
| memory/innodb/other | NO | NO |
| memory/innodb/row_log_buf | NO | NO |
| memory/innodb/row_merge_sort | NO | NO |
| memory/innodb/std | NO | NO |
| memory/innodb/sync_debug_latches | NO | NO |
| memory/innodb/trx_sys_t::rw_trx_ids | NO | NO |
...
+-------------------------------------------------------+---------+-------+
155 rows in set (0.00 sec)
```

For additional information about the instrumented InnoDB objects, you can query Performance Schema instances tables, which provide additional information about instrumented objects. Instance tables relevant to InnoDB include:

- The mutex\_instances table
- The rwlock\_instances table
- The cond\_instances table
- The file\_instances table

![](_page_100_Picture_1.jpeg)

#### Note

Mutexes and RW-locks related to the  ${\tt Innode}$  buffer pool are not included in this coverage; the same applies to the output of the  ${\tt SHOW}$  ENGINE INNODE MUTEX statement.

For example, to view information about instrumented InnoDB file objects seen by the Performance Schema when executing file I/O instrumentation, you might issue the following query:

```
mysql> SELECT *
    FROM performance_schema.file_instances
    WHERE EVENT_NAME LIKE '%innodb%'\G

***********************************
```

- You should be familiar with performance\_schema tables that store InnoDB event data. Tables relevant to InnoDB-related events include:
  - The Wait Event tables, which store wait events.
  - The Summary tables, which provide aggregated information for terminated events over time.
     Summary tables include file I/O summary tables, which aggregate information about I/O operations.
  - Stage Event tables, which store event data for InnoDB ALTER TABLE and buffer pool load
    operations. For more information, see Section 17.16.1, "Monitoring ALTER TABLE Progress for
    InnoDB Tables Using Performance Schema", and Monitoring Buffer Pool Load Progress Using
    Performance Schema.

If you are only interested in InnoDB-related objects, use the clause WHERE EVENT\_NAME LIKE '%innodb%' or WHERE NAME LIKE '%innodb%' (as required) when querying these tables.

# <span id="page-100-0"></span>17.16.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema

You can monitor ALTER TABLE progress for InnoDB tables using Performance Schema.

There are seven stage events that represent different phases of ALTER TABLE. Each stage event reports a running total of WORK\_COMPLETED and WORK\_ESTIMATED for the overall ALTER TABLE operation as it progresses through its different phases. WORK\_ESTIMATED is calculated using a formula that takes into account all of the work that ALTER TABLE performs, and may be revised during ALTER TABLE processing. WORK\_COMPLETED and WORK\_ESTIMATED values are an abstract representation of all of the work performed by ALTER TABLE.

In order of occurrence, ALTER TABLE stage events include:

• stage/innodb/alter table (read PK and internal sort): This stage is active when ALTER TABLE is in the reading-primary-key phase. It starts with WORK\_COMPLETED=0 and WORK\_ESTIMATED set to the estimated number of pages in the primary key. When the stage is completed, WORK ESTIMATED is updated to the actual number of pages in the primary key.

- stage/innodb/alter table (merge sort): This stage is repeated for each index added by the ALTER TABLE operation.
- stage/innodb/alter table (insert): This stage is repeated for each index added by the ALTER TABLE operation.
- stage/innodb/alter table (log apply index): This stage includes the application of DML log generated while ALTER TABLE was running.
- stage/innodb/alter table (flush): Before this stage begins, WORK\_ESTIMATED is updated with a more accurate estimate, based on the length of the flush list.
- stage/innodb/alter table (log apply table): This stage includes the application of concurrent DML log generated while ALTER TABLE was running. The duration of this phase depends on the extent of table changes. This phase is instant if no concurrent DML was run on the table.
- stage/innodb/alter table (end): Includes any remaining work that appeared after the flush phase, such as reapplying DML that was executed on the table while ALTER TABLE was running.

![](_page_101_Picture_7.jpeg)

### **Note**

InnoDB ALTER TABLE stage events do not currently account for the addition of spatial indexes.

## **ALTER TABLE Monitoring Example Using Performance Schema**

The following example demonstrates how to enable the stage/innodb/alter table% stage event instruments and related consumer tables to monitor ALTER TABLE progress. For information about Performance Schema stage event instruments and related consumers, see Section 29.12.5, "Performance Schema Stage Event Tables".

1. Enable the stage/innodb/alter% instruments:

```
mysql> UPDATE performance_schema.setup_instruments
 SET ENABLED = 'YES'
 WHERE NAME LIKE 'stage/innodb/alter%';
Query OK, 7 rows affected (0.00 sec)
Rows matched: 7 Changed: 7 Warnings: 0
```

2. Enable the stage event consumer tables, which include events\_stages\_current, events\_stages\_history, and events\_stages\_history\_long.

```
mysql> UPDATE performance_schema.setup_consumers
 SET ENABLED = 'YES'
 WHERE NAME LIKE '%stages%';
Query OK, 3 rows affected (0.00 sec)
Rows matched: 3 Changed: 3 Warnings: 0
```

3. Run an ALTER TABLE operation. In this example, a middle\_name column is added to the employees table of the employees sample database.

```
mysql> ALTER TABLE employees.employees ADD COLUMN middle_name varchar(14) AFTER first_name;
Query OK, 0 rows affected (9.27 sec)
Records: 0 Duplicates: 0 Warnings: 0
```

4. Check the progress of the ALTER TABLE operation by querying the Performance Schema events\_stages\_current table. The stage event shown differs depending on which ALTER TABLE phase is currently in progress. The WORK\_COMPLETED column shows the work completed. The WORK\_ESTIMATED column provides an estimate of the remaining work.

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED
 FROM performance_schema.events_stages_current;
+------------------------------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+------------------------------------------------------+----------------+----------------+
```

```
| stage/innodb/alter table (read PK and internal sort) | 280 | 1245 |
+------------------------------------------------------+----------------+----------------+
1 row in set (0.01 sec)
```

The events\_stages\_current table returns an empty set if the ALTER TABLE operation has completed. In this case, you can check the events\_stages\_history table to view event data for the completed operation. For example:

```
mysql> SELECT EVENT_NAME, WORK_COMPLETED, WORK_ESTIMATED
 FROM performance_schema.events_stages_history;
+------------------------------------------------------+----------------+----------------+
| EVENT_NAME | WORK_COMPLETED | WORK_ESTIMATED |
+------------------------------------------------------+----------------+----------------+
| stage/innodb/alter table (read PK and internal sort) | 886 | 1213 |
| stage/innodb/alter table (flush) | 1213 | 1213 |
| stage/innodb/alter table (log apply table) | 1597 | 1597 |
| stage/innodb/alter table (end) | 1597 | 1597 |
| stage/innodb/alter table (log apply table) | 1981 | 1981 |
+------------------------------------------------------+----------------+----------------+
5 rows in set (0.00 sec)
```

As shown above, the WORK\_ESTIMATED value was revised during ALTER TABLE processing. The estimated work after completion of the initial stage is 1213. When ALTER TABLE processing completed, WORK\_ESTIMATED was set to the actual value, which is 1981.