---
source: MySQL 8.4 Reference
title: 00_Overview
---

The InnoDB INFORMATION\_SCHEMA buffer pool tables provide buffer pool status information and metadata about the pages within the InnoDB buffer pool.

The InnoDB INFORMATION\_SCHEMA buffer pool tables include those listed below:

```
mysql> SHOW TABLES FROM INFORMATION_SCHEMA LIKE 'INNODB_BUFFER%';
+-----------------------------------------------+
| Tables_in_INFORMATION_SCHEMA (INNODB_BUFFER%) |
+-----------------------------------------------+
| INNODB_BUFFER_PAGE_LRU |
| INNODB_BUFFER_PAGE |
| INNODB_BUFFER_POOL_STATS |
+-----------------------------------------------+
```

## **Table Overview**

- INNODB\_BUFFER\_PAGE: Holds information about each page in the InnoDB buffer pool.
- INNODB\_BUFFER\_PAGE\_LRU: Holds information about the pages in the InnoDB buffer pool, in particular how they are ordered in the LRU list that determines which pages to evict from the buffer pool when it becomes full. The INNODB\_BUFFER\_PAGE\_LRU table has the same columns as the INNODB\_BUFFER\_PAGE table, except that the INNODB\_BUFFER\_PAGE\_LRU table has an LRU\_POSITION column instead of a BLOCK\_ID column.
- INNODB\_BUFFER\_POOL\_STATS: Provides buffer pool status information. Much of the same information is provided by SHOW ENGINE INNODB STATUS output, or may be obtained using InnoDB buffer pool server status variables.

![](_page_84_Picture_1.jpeg)

### **Warning**

Querying the INNODB\_BUFFER\_PAGE or INNODB\_BUFFER\_PAGE\_LRU table can affect performance. Do not query these tables on a production system unless you are aware of the performance impact and have determined it to be acceptable. To avoid impacting performance on a production system, reproduce the issue you want to investigate and query buffer pool statistics on a test instance.

#### **Example 17.6 Querying System Data in the INNODB\_BUFFER\_PAGE Table**

This query provides an approximate count of pages that contain system data by excluding pages where the TABLE\_NAME value is either NULL or includes a slash / or period . in the table name, which indicates a user-defined table.

```
mysql> SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NULL OR (INSTR(TABLE_NAME, '/') = 0 AND INSTR(TABLE_NAME, '.') = 0);
+----------+
| COUNT(*) |
+----------+
| 1516 |
+----------+
```

This query returns the approximate number of pages that contain system data, the total number of buffer pool pages, and an approximate percentage of pages that contain system data.

```
mysql> SELECT
 (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NULL OR (INSTR(TABLE_NAME, '/') = 0 AND INSTR(TABLE_NAME, '.') = 0)
 ) AS system_pages,
 (
 SELECT COUNT(*)
 FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 ) AS total_pages,
 (
 SELECT ROUND((system_pages/total_pages) * 100)
 ) AS system_page_percentage;
+--------------+-------------+------------------------+
| system_pages | total_pages | system_page_percentage |
+--------------+-------------+------------------------+
| 295 | 8192 | 4 |
+--------------+-------------+------------------------+
```

The type of system data in the buffer pool can be determined by querying the PAGE\_TYPE value. For example, the following query returns eight distinct PAGE\_TYPE values among the pages that contain system data:

```
mysql> SELECT DISTINCT PAGE_TYPE FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NULL OR (INSTR(TABLE_NAME, '/') = 0 AND INSTR(TABLE_NAME, '.') = 0);
+-------------------+
| PAGE_TYPE |
+-------------------+
| SYSTEM |
| IBUF_BITMAP |
| UNKNOWN |
| FILE_SPACE_HEADER |
| INODE |
| UNDO_LOG |
| ALLOCATED |
+-------------------+
```

### **Example 17.7 Querying User Data in the INNODB\_BUFFER\_PAGE Table**

This query provides an approximate count of pages containing user data by counting pages where the TABLE\_NAME value is NOT NULL and NOT LIKE '%INNODB\_TABLES%'.

```
mysql> SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NOT NULL AND TABLE_NAME NOT LIKE '%INNODB_TABLES%';
```

```
+----------+
| COUNT(*) |
+----------+
| 7897 |
+----------+
```

This query returns the approximate number of pages that contain user data, the total number of buffer pool pages, and an approximate percentage of pages that contain user data.

```
mysql> SELECT
 (SELECT COUNT(*) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NOT NULL AND (INSTR(TABLE_NAME, '/') > 0 OR INSTR(TABLE_NAME, '.') > 0)
 ) AS user_pages,
 (
 SELECT COUNT(*)
 FROM information_schema.INNODB_BUFFER_PAGE
 ) AS total_pages,
 (
 SELECT ROUND((user_pages/total_pages) * 100)
 ) AS user_page_percentage;
+------------+-------------+----------------------+
| user_pages | total_pages | user_page_percentage |
+------------+-------------+----------------------+
| 7897 | 8192 | 96 |
+------------+-------------+----------------------+
```

This query identifies user-defined tables with pages in the buffer pool:

```
mysql> SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME IS NOT NULL AND (INSTR(TABLE_NAME, '/') > 0 OR INSTR(TABLE_NAME, '.') > 0)
 AND TABLE_NAME NOT LIKE '`mysql`.`innodb_%';
+-------------------------+
| TABLE_NAME |
+-------------------------+
| `employees`.`salaries` |
| `employees`.`employees` |
+-------------------------+
```

### **Example 17.8 Querying Index Data in the INNODB\_BUFFER\_PAGE Table**

For information about index pages, query the INDEX\_NAME column using the name of the index. For example, the following query returns the number of pages and total data size of pages for the emp\_no index that is defined on the employees.salaries table:

```
mysql> SELECT INDEX_NAME, COUNT(*) AS Pages,
ROUND(SUM(IF(COMPRESSED_SIZE = 0, @@GLOBAL.innodb_page_size, COMPRESSED_SIZE))/1024/1024)
AS 'Total Data (MB)'
FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
WHERE INDEX_NAME='emp_no' AND TABLE_NAME = '`employees`.`salaries`';
+------------+-------+-----------------+
| INDEX_NAME | Pages | Total Data (MB) |
+------------+-------+-----------------+
| emp_no | 1609 | 25 |
+------------+-------+-----------------+
```

This query returns the number of pages and total data size of pages for all indexes defined on the employees.salaries table:

```
mysql> SELECT INDEX_NAME, COUNT(*) AS Pages,
 ROUND(SUM(IF(COMPRESSED_SIZE = 0, @@GLOBAL.innodb_page_size, COMPRESSED_SIZE))/1024/1024)
 AS 'Total Data (MB)'
 FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE
 WHERE TABLE_NAME = '`employees`.`salaries`'
 GROUP BY INDEX_NAME;
+------------+-------+-----------------+
| INDEX_NAME | Pages | Total Data (MB) |
+------------+-------+-----------------+
| emp_no | 1608 | 25 |
| PRIMARY | 6086 | 95 |
+------------+-------+-----------------+
```

### **Example 17.9 Querying LRU\_POSITION Data in the INNODB\_BUFFER\_PAGE\_LRU Table**

The INNODB\_BUFFER\_PAGE\_LRU table holds information about the pages in the InnoDB buffer pool, in particular how they are ordered that determines which pages to evict from the buffer pool when it becomes full. The definition for this page is the same as for INNODB\_BUFFER\_PAGE, except this table has an LRU\_POSITION column instead of a BLOCK\_ID column.

This query counts the number of positions at a specific location in the LRU list occupied by pages of the employees.employees table.

```
mysql> SELECT COUNT(LRU_POSITION) FROM INFORMATION_SCHEMA.INNODB_BUFFER_PAGE_LRU
 WHERE TABLE_NAME='`employees`.`employees`' AND LRU_POSITION < 3072;
+---------------------+
| COUNT(LRU_POSITION) |
+---------------------+
| 548 |
+---------------------+
```

#### **Example 17.10 Querying the INNODB\_BUFFER\_POOL\_STATS Table**

The INNODB\_BUFFER\_POOL\_STATS table provides information similar to SHOW ENGINE INNODB STATUS and InnoDB buffer pool status variables.

```
mysql> SELECT * FROM information_schema.INNODB_BUFFER_POOL_STATS \G
*************************** 1. row ***************************
 POOL_ID: 0
 POOL_SIZE: 8192
 FREE_BUFFERS: 1
 DATABASE_PAGES: 8173
 OLD_DATABASE_PAGES: 3014
 MODIFIED_DATABASE_PAGES: 0
 PENDING_DECOMPRESS: 0
 PENDING_READS: 0
 PENDING_FLUSH_LRU: 0
 PENDING_FLUSH_LIST: 0
 PAGES_MADE_YOUNG: 15907
 PAGES_NOT_MADE_YOUNG: 3803101
 PAGES_MADE_YOUNG_RATE: 0
 PAGES_MADE_NOT_YOUNG_RATE: 0
 NUMBER_PAGES_READ: 3270
 NUMBER_PAGES_CREATED: 13176
 NUMBER_PAGES_WRITTEN: 15109
 PAGES_READ_RATE: 0
 PAGES_CREATE_RATE: 0
 PAGES_WRITTEN_RATE: 0
 NUMBER_PAGES_GET: 33069332
 HIT_RATE: 0
 YOUNG_MAKE_PER_THOUSAND_GETS: 0
NOT_YOUNG_MAKE_PER_THOUSAND_GETS: 0
 NUMBER_PAGES_READ_AHEAD: 2713
 NUMBER_READ_AHEAD_EVICTED: 0
 READ_AHEAD_RATE: 0
 READ_AHEAD_EVICTED_RATE: 0
 LRU_IO_TOTAL: 0
 LRU_IO_CURRENT: 0
 UNCOMPRESS_TOTAL: 0
 UNCOMPRESS_CURRENT: 0
```

For comparison, SHOW ENGINE INNODB STATUS output and InnoDB buffer pool status variable output is shown below, based on the same data set.

For more information about SHOW ENGINE INNODB STATUS output, see [Section 17.17.3, "InnoDB](#page-108-0) [Standard Monitor and Lock Monitor Output"](#page-108-0).

```
mysql> SHOW ENGINE INNODB STATUS\G
...
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 137428992
```

```
Dictionary memory allocated 579084
Buffer pool size 8192
Free buffers 1
Database pages 8173
Old database pages 3014
Modified db pages 0
Pending reads 0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 15907, not young 3803101
0.00 youngs/s, 0.00 non-youngs/s
Pages read 3270, created 13176, written 15109
0.00 reads/s, 0.00 creates/s, 0.00 writes/s
No buffer pool page gets since the last printout
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
LRU len: 8173, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
...
```

For status variable descriptions, see Section 7.1.10, "Server Status Variables".

```
mysql> SHOW STATUS LIKE 'Innodb_buffer%';
+---------------------------------------+-------------+
| Variable_name | Value |
+---------------------------------------+-------------+
| Innodb_buffer_pool_dump_status | not started |
| Innodb_buffer_pool_load_status | not started |
| Innodb_buffer_pool_resize_status | not started |
| Innodb_buffer_pool_pages_data | 8173 |
| Innodb_buffer_pool_bytes_data | 133906432 |
| Innodb_buffer_pool_pages_dirty | 0 |
| Innodb_buffer_pool_bytes_dirty | 0 |
| Innodb_buffer_pool_pages_flushed | 15109 |
| Innodb_buffer_pool_pages_free | 1 |
| Innodb_buffer_pool_pages_misc | 18 |
| Innodb_buffer_pool_pages_total | 8192 |
| Innodb_buffer_pool_read_ahead_rnd | 0 |
| Innodb_buffer_pool_read_ahead | 2713 |
| Innodb_buffer_pool_read_ahead_evicted | 0 |
| Innodb_buffer_pool_read_requests | 33069332 |
| Innodb_buffer_pool_reads | 558 |
| Innodb_buffer_pool_wait_free | 0 |
| Innodb_buffer_pool_write_requests | 11985961 |
+---------------------------------------+-------------+
```

# <span id="page-87-0"></span>**17.15.6 InnoDB INFORMATION\_SCHEMA Metrics Table**

The INNODB\_METRICS table provides information about InnoDB performance and resource-related counters.

INNODB\_METRICS table columns are shown below. For column descriptions, see Section 28.4.21, "The INFORMATION\_SCHEMA INNODB\_METRICS Table".

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts" \G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 46273
 MAX_COUNT: 46273
 MIN_COUNT: NULL
 AVG_COUNT: 492.2659574468085
 COUNT_RESET: 46273
MAX_COUNT_RESET: 46273
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
 TIME_ENABLED: 2014-11-28 16:07:53
 TIME_DISABLED: NULL
 TIME_ELAPSED: 94
 TIME_RESET: NULL
 STATUS: enabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

## **Enabling, Disabling, and Resetting Counters**

You can enable, disable, and reset counters using the following variables:

• [innodb\\_monitor\\_enable](#page-36-1): Enables counters.

```
SET GLOBAL innodb_monitor_enable = [counter-name|module_name|pattern|all];
```

• [innodb\\_monitor\\_disable](#page-36-0): Disables counters.

```
SET GLOBAL innodb_monitor_disable = [counter-name|module_name|pattern|all];
```

• [innodb\\_monitor\\_reset](#page-36-2): Resets counter values to zero.

```
SET GLOBAL innodb_monitor_reset = [counter-name|module_name|pattern|all];
```

• [innodb\\_monitor\\_reset\\_all](#page-37-0): Resets all counter values. A counter must be disabled before using [innodb\\_monitor\\_reset\\_all](#page-37-0).

```
SET GLOBAL innodb_monitor_reset_all = [counter-name|module_name|pattern|all];
```

Counters and counter modules can also be enabled at startup using the MySQL server configuration file. For example, to enable the log module, metadata\_table\_handles\_opened and metadata\_table\_handles\_closed counters, enter the following line in the [mysqld] section of the MySQL server configuration file.

```
[mysqld]
innodb_monitor_enable = log,metadata_table_handles_opened,metadata_table_handles_closed
```

When enabling multiple counters or modules in a configuration file, specify the [innodb\\_monitor\\_enable](#page-36-1) variable followed by counter and module names separated by a comma, as shown above. Only the [innodb\\_monitor\\_enable](#page-36-1) variable can be used in a configuration file. The [innodb\\_monitor\\_disable](#page-36-0) and [innodb\\_monitor\\_reset](#page-36-2) variables are supported on the command line only.

![](_page_88_Picture_14.jpeg)

### **Note**

Because each counter adds a degree of runtime overhead, use counters conservatively on production servers to diagnose specific issues or monitor specific functionality. A test or development server is recommended for more extensive use of counters.

## **Counters**

The list of available counters is subject to change. Query the Information Schema INNODB\_METRICS table for counters available in your MySQL server version.

The counters enabled by default correspond to those shown in SHOW ENGINE INNODB STATUS output. Counters shown in SHOW ENGINE INNODB STATUS output are always enabled at a system level but can be disabled for the INNODB\_METRICS table. Counter status is not persistent. Unless configured otherwise, counters revert to their default enabled or disabled status when the server is restarted.

If you run programs that would be affected by the addition or removal of counters, it is recommended that you review the releases notes and query the INNODB\_METRICS table to identify those changes as part of your upgrade process.

```
mysql> SELECT name, subsystem, status FROM INFORMATION_SCHEMA.INNODB_METRICS ORDER BY NAME;
+---------------------------------------------+---------------------+----------+
| name | subsystem | status |
+---------------------------------------------+---------------------+----------+
| adaptive_hash_pages_added | adaptive_hash_index | disabled |
| adaptive_hash_pages_removed | adaptive_hash_index | disabled |
| adaptive_hash_rows_added | adaptive_hash_index | disabled |
| adaptive_hash_rows_deleted_no_hash_entry | adaptive_hash_index | disabled |
| adaptive_hash_rows_removed | adaptive_hash_index | disabled |
```

```
| adaptive_hash_rows_updated | adaptive_hash_index | disabled |
| adaptive_hash_searches | adaptive_hash_index | enabled |
| adaptive_hash_searches_btree | adaptive_hash_index | enabled |
| buffer_data_reads | buffer | enabled |
| buffer_data_written | buffer | enabled |
| buffer_flush_adaptive | buffer | disabled |
| buffer_flush_adaptive_avg_pass | buffer | disabled |
| buffer_flush_adaptive_avg_time_est | buffer | disabled |
| buffer_flush_adaptive_avg_time_slot | buffer | disabled |
| buffer_flush_adaptive_avg_time_thread | buffer | disabled |
| buffer_flush_adaptive_pages | buffer | disabled |
| buffer_flush_adaptive_total_pages | buffer | disabled |
| buffer_flush_avg_page_rate | buffer | disabled |
| buffer_flush_avg_pass | buffer | disabled |
| buffer_flush_avg_time | buffer | disabled |
| buffer_flush_background | buffer | disabled |
| buffer_flush_background_pages | buffer | disabled |
| buffer_flush_background_total_pages | buffer | disabled |
| buffer_flush_batches | buffer | disabled |
| buffer_flush_batch_num_scan | buffer | disabled |
| buffer_flush_batch_pages | buffer | disabled |
| buffer_flush_batch_scanned | buffer | disabled |
| buffer_flush_batch_scanned_per_call | buffer | disabled |
| buffer_flush_batch_total_pages | buffer | disabled |
| buffer_flush_lsn_avg_rate | buffer | disabled |
| buffer_flush_neighbor | buffer | disabled |
| buffer_flush_neighbor_pages | buffer | disabled |
| buffer_flush_neighbor_total_pages | buffer | disabled |
| buffer_flush_n_to_flush_by_age | buffer | disabled |
| buffer_flush_n_to_flush_by_dirty_page | buffer | disabled |
| buffer_flush_n_to_flush_requested | buffer | disabled |
| buffer_flush_pct_for_dirty | buffer | disabled |
| buffer_flush_pct_for_lsn | buffer | disabled |
| buffer_flush_sync | buffer | disabled |
| buffer_flush_sync_pages | buffer | disabled |
| buffer_flush_sync_total_pages | buffer | disabled |
| buffer_flush_sync_waits | buffer | disabled |
| buffer_LRU_batches_evict | buffer | disabled |
| buffer_LRU_batches_flush | buffer | disabled |
| buffer_LRU_batch_evict_pages | buffer | disabled |
| buffer_LRU_batch_evict_total_pages | buffer | disabled |
| buffer_LRU_batch_flush_avg_pass | buffer | disabled |
| buffer_LRU_batch_flush_avg_time_est | buffer | disabled |
| buffer_LRU_batch_flush_avg_time_slot | buffer | disabled |
| buffer_LRU_batch_flush_avg_time_thread | buffer | disabled |
| buffer_LRU_batch_flush_pages | buffer | disabled |
| buffer_LRU_batch_flush_total_pages | buffer | disabled |
| buffer_LRU_batch_num_scan | buffer | disabled |
| buffer_LRU_batch_scanned | buffer | disabled |
| buffer_LRU_batch_scanned_per_call | buffer | disabled |
| buffer_LRU_get_free_loops | buffer | disabled |
| buffer_LRU_get_free_search | Buffer | disabled |
| buffer_LRU_get_free_waits | buffer | disabled |
| buffer_LRU_search_num_scan | buffer | disabled |
| buffer_LRU_search_scanned | buffer | disabled |
| buffer_LRU_search_scanned_per_call | buffer | disabled |
| buffer_LRU_single_flush_failure_count | Buffer | disabled |
| buffer_LRU_single_flush_num_scan | buffer | disabled |
| buffer_LRU_single_flush_scanned | buffer | disabled |
| buffer_LRU_single_flush_scanned_per_call | buffer | disabled |
| buffer_LRU_unzip_search_num_scan | buffer | disabled |
| buffer_LRU_unzip_search_scanned | buffer | disabled |
| buffer_LRU_unzip_search_scanned_per_call | buffer | disabled |
| buffer_pages_created | buffer | enabled |
| buffer_pages_read | buffer | enabled |
| buffer_pages_written | buffer | enabled |
| buffer_page_read_blob | buffer_page_io | disabled |
| buffer_page_read_fsp_hdr | buffer_page_io | disabled |
| buffer_page_read_ibuf_bitmap | buffer_page_io | disabled |
| buffer_page_read_ibuf_free_list | buffer_page_io | disabled |
| buffer_page_read_index_ibuf_leaf | buffer_page_io | disabled |
| buffer_page_read_index_ibuf_non_leaf | buffer_page_io | disabled |
```

```
| buffer_page_read_index_inode | buffer_page_io | disabled |
| buffer_page_read_index_leaf | buffer_page_io | disabled |
| buffer_page_read_index_non_leaf | buffer_page_io | disabled |
| buffer_page_read_other | buffer_page_io | disabled |
| buffer_page_read_rseg_array | buffer_page_io | disabled |
| buffer_page_read_system_page | buffer_page_io | disabled |
| buffer_page_read_trx_system | buffer_page_io | disabled |
| buffer_page_read_undo_log | buffer_page_io | disabled |
| buffer_page_read_xdes | buffer_page_io | disabled |
| buffer_page_read_zblob | buffer_page_io | disabled |
| buffer_page_read_zblob2 | buffer_page_io | disabled |
| buffer_page_written_blob | buffer_page_io | disabled |
| buffer_page_written_fsp_hdr | buffer_page_io | disabled |
| buffer_page_written_ibuf_bitmap | buffer_page_io | disabled |
| buffer_page_written_ibuf_free_list | buffer_page_io | disabled |
| buffer_page_written_index_ibuf_leaf | buffer_page_io | disabled |
| buffer_page_written_index_ibuf_non_leaf | buffer_page_io | disabled |
| buffer_page_written_index_inode | buffer_page_io | disabled |
| buffer_page_written_index_leaf | buffer_page_io | disabled |
| buffer_page_written_index_non_leaf | buffer_page_io | disabled |
| buffer_page_written_on_log_no_waits | buffer_page_io | disabled |
| buffer_page_written_on_log_waits | buffer_page_io | disabled |
| buffer_page_written_on_log_wait_loops | buffer_page_io | disabled |
| buffer_page_written_other | buffer_page_io | disabled |
| buffer_page_written_rseg_array | buffer_page_io | disabled |
| buffer_page_written_system_page | buffer_page_io | disabled |
| buffer_page_written_trx_system | buffer_page_io | disabled |
| buffer_page_written_undo_log | buffer_page_io | disabled |
| buffer_page_written_xdes | buffer_page_io | disabled |
| buffer_page_written_zblob | buffer_page_io | disabled |
| buffer_page_written_zblob2 | buffer_page_io | disabled |
| buffer_pool_bytes_data | buffer | enabled |
| buffer_pool_bytes_dirty | buffer | enabled |
| buffer_pool_pages_data | buffer | enabled |
| buffer_pool_pages_dirty | buffer | enabled |
| buffer_pool_pages_free | buffer | enabled |
| buffer_pool_pages_misc | buffer | enabled |
| buffer_pool_pages_total | buffer | enabled |
| buffer_pool_reads | buffer | enabled |
| buffer_pool_read_ahead | buffer | enabled |
| buffer_pool_read_ahead_evicted | buffer | enabled |
| buffer_pool_read_requests | buffer | enabled |
| buffer_pool_size | server | enabled |
| buffer_pool_wait_free | buffer | enabled |
| buffer_pool_write_requests | buffer | enabled |
| compression_pad_decrements | compression | disabled |
| compression_pad_increments | compression | disabled |
| compress_pages_compressed | compression | disabled |
| compress_pages_decompressed | compression | disabled |
| cpu_n | cpu | disabled |
| cpu_stime_abs | cpu | disabled |
| cpu_stime_pct | cpu | disabled |
| cpu_utime_abs | cpu | disabled |
| cpu_utime_pct | cpu | disabled |
| dblwr_async_requests | dblwr | disabled |
| dblwr_flush_requests | dblwr | disabled |
| dblwr_flush_wait_events | dblwr | disabled |
| dblwr_sync_requests | dblwr | disabled |
| ddl_background_drop_tables | ddl | disabled |
| ddl_log_file_alter_table | ddl | disabled |
| ddl_online_create_index | ddl | disabled |
| ddl_pending_alter_table | ddl | disabled |
| ddl_sort_file_alter_table | ddl | disabled |
| dml_deletes | dml | enabled |
| dml_inserts | dml | enabled |
| dml_reads | dml | disabled |
| dml_system_deletes | dml | enabled |
| dml_system_inserts | dml | enabled |
| dml_system_reads | dml | enabled |
| dml_system_updates | dml | enabled |
| dml_updates | dml | enabled |
| file_num_open_files | file_system | enabled |
```

```
| ibuf_merges | change_buffer | enabled |
| ibuf_merges_delete | change_buffer | enabled |
| ibuf_merges_delete_mark | change_buffer | enabled |
| ibuf_merges_discard_delete | change_buffer | enabled |
| ibuf_merges_discard_delete_mark | change_buffer | enabled |
| ibuf_merges_discard_insert | change_buffer | enabled |
| ibuf_merges_insert | change_buffer | enabled |
| ibuf_size | change_buffer | enabled |
| icp_attempts | icp | disabled |
| icp_match | icp | disabled |
| icp_no_match | icp | disabled |
| icp_out_of_range | icp | disabled |
| index_page_discards | index | disabled |
| index_page_merge_attempts | index | disabled |
| index_page_merge_successful | index | disabled |
| index_page_reorg_attempts | index | disabled |
| index_page_reorg_successful | index | disabled |
| index_page_splits | index | disabled |
| innodb_activity_count | server | enabled |
| innodb_background_drop_table_usec | server | disabled |
| innodb_dblwr_pages_written | server | enabled |
| innodb_dblwr_writes | server | enabled |
| innodb_dict_lru_count | server | disabled |
| innodb_dict_lru_usec | server | disabled |
| innodb_ibuf_merge_usec | server | disabled |
| innodb_master_active_loops | server | disabled |
| innodb_master_idle_loops | server | disabled |
| innodb_master_purge_usec | server | disabled |
| innodb_master_thread_sleeps | server | disabled |
| innodb_mem_validate_usec | server | disabled |
| innodb_page_size | server | enabled |
| innodb_rwlock_sx_os_waits | server | enabled |
| innodb_rwlock_sx_spin_rounds | server | enabled |
| innodb_rwlock_sx_spin_waits | server | enabled |
| innodb_rwlock_s_os_waits | server | enabled |
| innodb_rwlock_s_spin_rounds | server | enabled |
| innodb_rwlock_s_spin_waits | server | enabled |
| innodb_rwlock_x_os_waits | server | enabled |
| innodb_rwlock_x_spin_rounds | server | enabled |
| innodb_rwlock_x_spin_waits | server | enabled |
| lock_deadlocks | lock | enabled |
| lock_deadlock_false_positives | lock | enabled |
| lock_deadlock_rounds | lock | enabled |
| lock_rec_grant_attempts | lock | enabled |
| lock_rec_locks | lock | disabled |
| lock_rec_lock_created | lock | disabled |
| lock_rec_lock_removed | lock | disabled |
| lock_rec_lock_requests | lock | disabled |
| lock_rec_lock_waits | lock | disabled |
| lock_rec_release_attempts | lock | enabled |
| lock_row_lock_current_waits | lock | enabled |
| lock_row_lock_time | lock | enabled |
| lock_row_lock_time_avg | lock | enabled |
| lock_row_lock_time_max | lock | enabled |
| lock_row_lock_waits | lock | enabled |
| lock_schedule_refreshes | lock | enabled |
| lock_table_locks | lock | disabled |
| lock_table_lock_created | lock | disabled |
| lock_table_lock_removed | lock | disabled |
| lock_table_lock_waits | lock | disabled |
| lock_threads_waiting | lock | enabled |
| lock_timeouts | lock | enabled |
| log_checkpoints | log | disabled |
| log_concurrency_margin | log | disabled |
| log_flusher_no_waits | log | disabled |
| log_flusher_waits | log | disabled |
| log_flusher_wait_loops | log | disabled |
| log_flush_avg_time | log | disabled |
| log_flush_lsn_avg_rate | log | disabled |
| log_flush_max_time | log | disabled |
| log_flush_notifier_no_waits | log | disabled |
| log_flush_notifier_waits | log | disabled |
```

```
| log_flush_notifier_wait_loops | log | disabled |
| log_flush_total_time | log | disabled |
| log_free_space | log | disabled |
| log_full_block_writes | log | disabled |
| log_lsn_archived | log | disabled |
| log_lsn_buf_dirty_pages_added | log | disabled |
| log_lsn_buf_pool_oldest_approx | log | disabled |
| log_lsn_buf_pool_oldest_lwm | log | disabled |
| log_lsn_checkpoint_age | log | disabled |
| log_lsn_current | log | disabled |
| log_lsn_last_checkpoint | log | disabled |
| log_lsn_last_flush | log | disabled |
| log_max_modified_age_async | log | disabled |
| log_max_modified_age_sync | log | disabled |
| log_next_file | log | disabled |
| log_on_buffer_space_no_waits | log | disabled |
| log_on_buffer_space_waits | log | disabled |
| log_on_buffer_space_wait_loops | log | disabled |
| log_on_file_space_no_waits | log | disabled |
| log_on_file_space_waits | log | disabled |
| log_on_file_space_wait_loops | log | disabled |
| log_on_flush_no_waits | log | disabled |
| log_on_flush_waits | log | disabled |
| log_on_flush_wait_loops | log | disabled |
| log_on_recent_closed_wait_loops | log | disabled |
| log_on_recent_written_wait_loops | log | disabled |
| log_on_write_no_waits | log | disabled |
| log_on_write_waits | log | disabled |
| log_on_write_wait_loops | log | disabled |
| log_padded | log | disabled |
| log_partial_block_writes | log | disabled |
| log_waits | log | enabled |
| log_writer_no_waits | log | disabled |
| log_writer_on_archiver_waits | log | disabled |
| log_writer_on_file_space_waits | log | disabled |
| log_writer_waits | log | disabled |
| log_writer_wait_loops | log | disabled |
| log_writes | log | enabled |
| log_write_notifier_no_waits | log | disabled |
| log_write_notifier_waits | log | disabled |
| log_write_notifier_wait_loops | log | disabled |
| log_write_requests | log | enabled |
| log_write_to_file_requests_interval | log | disabled |
| metadata_table_handles_closed | metadata | disabled |
| metadata_table_handles_opened | metadata | disabled |
| metadata_table_reference_count | metadata | disabled |
| module_cpu | cpu | disabled |
| module_dblwr | dblwr | disabled |
| module_page_track | page_track | disabled |
| os_data_fsyncs | os | enabled |
| os_data_reads | os | enabled |
| os_data_writes | os | enabled |
| os_log_bytes_written | os | enabled |
| os_log_fsyncs | os | enabled |
| os_log_pending_fsyncs | os | enabled |
| os_log_pending_writes | os | enabled |
| os_pending_reads | os | disabled |
| os_pending_writes | os | disabled |
| page_track_checkpoint_partial_flush_request | page_track | disabled |
| page_track_full_block_writes | page_track | disabled |
| page_track_partial_block_writes | page_track | disabled |
| page_track_resets | page_track | disabled |
| purge_del_mark_records | purge | disabled |
| purge_dml_delay_usec | purge | disabled |
| purge_invoked | purge | disabled |
| purge_resume_count | purge | disabled |
| purge_stop_count | purge | disabled |
| purge_truncate_history_count | purge | disabled |
| purge_truncate_history_usec | purge | disabled |
| purge_undo_log_pages | purge | disabled |
| purge_upd_exist_or_extern_records | purge | disabled |
| sampled_pages_read | sampling | disabled |
```

```
| sampled_pages_skipped | sampling | disabled |
| trx_active_transactions | transaction | disabled |
| trx_allocations | transaction | disabled |
| trx_commits_insert_update | transaction | disabled |
| trx_nl_ro_commits | transaction | disabled |
| trx_on_log_no_waits | transaction | disabled |
| trx_on_log_waits | transaction | disabled |
| trx_on_log_wait_loops | transaction | disabled |
| trx_rollbacks | transaction | disabled |
| trx_rollbacks_savepoint | transaction | disabled |
| trx_rollback_active | transaction | disabled |
| trx_ro_commits | transaction | disabled |
| trx_rseg_current_size | transaction | disabled |
| trx_rseg_history_len | transaction | enabled |
| trx_rw_commits | transaction | disabled |
| trx_undo_slots_cached | transaction | disabled |
| trx_undo_slots_used | transaction | disabled |
| undo_truncate_count | undo | disabled |
| undo_truncate_done_logging_count | undo | disabled |
| undo_truncate_start_logging_count | undo | disabled |
| undo_truncate_usec | undo | disabled |
+---------------------------------------------+---------------------+----------+
314 rows in set (0.00 sec)
```

## **Counter Modules**

Each counter is associated with a particular module. Module names can be used to enable, disable, or reset all counters for a particular subsystem. For example, use module\_dml to enable all counters associated with the dml subsystem.

```
mysql> SET GLOBAL innodb_monitor_enable = module_dml;
mysql> SELECT name, subsystem, status FROM INFORMATION_SCHEMA.INNODB_METRICS
 WHERE subsystem ='dml';
+-------------+-----------+---------+
| name | subsystem | status |
+-------------+-----------+---------+
| dml_reads | dml | enabled |
| dml_inserts | dml | enabled |
| dml_deletes | dml | enabled |
| dml_updates | dml | enabled |
+-------------+-----------+---------+
```

Module names can be used with [innodb\\_monitor\\_enable](#page-36-1) and related variables.

Module names and corresponding SUBSYSTEM names are listed below.

```
• module_adaptive_hash (subsystem = adaptive_hash_index)
• module_buffer (subsystem = buffer)
• module_buffer_page (subsystem = buffer_page_io)
• module_compress (subsystem = compression)
• module_ddl (subsystem = ddl)
• module_dml (subsystem = dml)
• module_file (subsystem = file_system)
• module_ibuf_system (subsystem = change_buffer)
• module_icp (subsystem = icp)
• module_index (subsystem = index)
• module_innodb (subsystem = innodb)
```

• module\_lock (subsystem = lock)

```
• module_log (subsystem = log)
```

- module\_metadata (subsystem = metadata)
- module\_os (subsystem = os)
- module\_purge (subsystem = purge)
- module\_trx (subsystem = transaction)
- module\_undo (subsystem = undo)

### **Example 17.11 Working with INNODB\_METRICS Table Counters**

This example demonstrates enabling, disabling, and resetting a counter, and querying counter data in the INNODB\_METRICS table.

1. Create a simple InnoDB table:

```
mysql> USE test;
Database changed
mysql> CREATE TABLE t1 (c1 INT) ENGINE=INNODB;
Query OK, 0 rows affected (0.02 sec)
```

2. Enable the dml\_inserts counter.

```
mysql> SET GLOBAL innodb_monitor_enable = dml_inserts;
Query OK, 0 rows affected (0.01 sec)
```

A description of the dml\_inserts counter can be found in the COMMENT column of the INNODB\_METRICS table:

```
mysql> SELECT NAME, COMMENT FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts";
+-------------+-------------------------+
| NAME | COMMENT |
+-------------+-------------------------+
| dml_inserts | Number of rows inserted |
+-------------+-------------------------+
```

3. Query the INNODB\_METRICS table for the dml\_inserts counter data. Because no DML operations have been performed, the counter values are zero or NULL. The TIME\_ENABLED and TIME\_ELAPSED values indicate when the counter was last enabled and how many seconds have elapsed since that time.

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts" \G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 0
 MAX_COUNT: 0
 MIN_COUNT: NULL
 AVG_COUNT: 0
 COUNT_RESET: 0
MAX_COUNT_RESET: 0
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
 TIME_ENABLED: 2014-12-04 14:18:28
 TIME_DISABLED: NULL
 TIME_ELAPSED: 28
 TIME_RESET: NULL
 STATUS: enabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

4. Insert three rows of data into the table.

```
mysql> INSERT INTO t1 values(1);
Query OK, 1 row affected (0.00 sec)
```

```
mysql> INSERT INTO t1 values(2);
Query OK, 1 row affected (0.00 sec)
mysql> INSERT INTO t1 values(3);
Query OK, 1 row affected (0.00 sec)
```

5. Query the INNODB\_METRICS table again for the dml\_inserts counter data. A number of counter values have now incremented including COUNT, MAX\_COUNT, AVG\_COUNT, and COUNT\_RESET. Refer to the INNODB\_METRICS table definition for descriptions of these values.

```
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts"\G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 3
 MAX_COUNT: 3
 MIN_COUNT: NULL
 AVG_COUNT: 0.046153846153846156
 COUNT_RESET: 3
MAX_COUNT_RESET: 3
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
 TIME_ENABLED: 2014-12-04 14:18:28
 TIME_DISABLED: NULL
 TIME_ELAPSED: 65
 TIME_RESET: NULL
 STATUS: enabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

6. Reset the dml\_inserts counter and query the INNODB\_METRICS table again for the dml\_inserts counter data. The %\_RESET values that were reported previously, such as COUNT\_RESET and MAX\_RESET, are set back to zero. Values such as COUNT, MAX\_COUNT, and AVG\_COUNT, which cumulatively collect data from the time the counter is enabled, are unaffected by the reset.

```
mysql> SET GLOBAL innodb_monitor_reset = dml_inserts;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts"\G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 3
 MAX_COUNT: 3
 MIN_COUNT: NULL
 AVG_COUNT: 0.03529411764705882
 COUNT_RESET: 0
MAX_COUNT_RESET: 0
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: 0
 TIME_ENABLED: 2014-12-04 14:18:28
 TIME_DISABLED: NULL
 TIME_ELAPSED: 85
 TIME_RESET: 2014-12-04 14:19:44
 STATUS: enabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

7. To reset all counter values, you must first disable the counter. Disabling the counter sets the STATUS value to disabled.

```
mysql> SET GLOBAL innodb_monitor_disable = dml_inserts;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts"\G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
```

```
 COUNT: 3
 MAX_COUNT: 3
 MIN_COUNT: NULL
 AVG_COUNT: 0.030612244897959183
 COUNT_RESET: 0
MAX_COUNT_RESET: 0
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: 0
 TIME_ENABLED: 2014-12-04 14:18:28
 TIME_DISABLED: 2014-12-04 14:20:06
 TIME_ELAPSED: 98
 TIME_RESET: NULL
 STATUS: disabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```

![](_page_96_Picture_2.jpeg)

#### **Note**

Wildcard match is supported for counter and module names. For example, instead of specifying the full dml\_inserts counter name, you can specify dml\_i%. You can also enable, disable, or reset multiple counters or modules at once using a wildcard match. For example, specify dml\_% to enable, disable, or reset all counters that begin with dml\_.

8. After the counter is disabled, you can reset all counter values using the [innodb\\_monitor\\_reset\\_all](#page-37-0) option. All values are set to zero or NULL.

```
mysql> SET GLOBAL innodb_monitor_reset_all = dml_inserts;
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT * FROM INFORMATION_SCHEMA.INNODB_METRICS WHERE NAME="dml_inserts"\G
*************************** 1. row ***************************
 NAME: dml_inserts
 SUBSYSTEM: dml
 COUNT: 0
 MAX_COUNT: NULL
 MIN_COUNT: NULL
 AVG_COUNT: NULL
 COUNT_RESET: 0
MAX_COUNT_RESET: NULL
MIN_COUNT_RESET: NULL
AVG_COUNT_RESET: NULL
 TIME_ENABLED: NULL
 TIME_DISABLED: NULL
 TIME_ELAPSED: NULL
 TIME_RESET: NULL
 STATUS: disabled
 TYPE: status_counter
 COMMENT: Number of rows inserted
```