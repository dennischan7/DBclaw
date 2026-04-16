---
source: MySQL 8.0 Reference
title: 00_Overview
---

A mutex is a synchronization mechanism used in the code to enforce that only one thread at a given time can have access to a common resource. When two or more threads executing in the server need to access the same resource, the threads compete against each other. The first thread to obtain a lock on the mutex causes the other threads to wait until the lock is released.

For InnoDB mutexes that are instrumented, mutex waits can be monitored using Performance Schema. Wait event data collected in Performance Schema tables can help identify mutexes with the most waits or the greatest total wait time, for example.

The following example demonstrates how to enable InnoDB mutex wait instruments, how to enable associated consumers, and how to query wait event data.

1. To view available InnoDB mutex wait instruments, query the Performance Schema setup\_instruments table. All InnoDB mutex wait instruments are disabled by default.

| mysql> SELECT *<br>FROM performance_schema.setup_instruments |                 |    |
|--------------------------------------------------------------|-----------------|----|
| WHERE NAME LIKE '%wait/synch/mutex/innodb%';                 |                 |    |
| ++++<br>  NAME                                               | ENABLED   TIMED |    |
| ++++<br>  wait/synch/mutex/innodb/commit_cond_mutex          | NO              | NO |
| wait/synch/mutex/innodb/innobase_share_mutex                 | NO              | NO |
| wait/synch/mutex/innodb/autoinc_mutex                        | NO              | NO |
| wait/synch/mutex/innodb/autoinc_persisted_mutex              | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_flush_state_mutex           | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_LRU_list_mutex              | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_free_list_mutex             | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_zip_free_mutex              | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_zip_hash_mutex              | NO              | NO |
| wait/synch/mutex/innodb/buf_pool_zip_mutex                   | NO              | NO |
| wait/synch/mutex/innodb/cache_last_read_mutex                | NO              | NO |
| wait/synch/mutex/innodb/dict_foreign_err_mutex               | NO              | NO |
| wait/synch/mutex/innodb/dict_persist_dirty_tables_mutex   NO |                 | NO |
| wait/synch/mutex/innodb/dict_sys_mutex                       | NO              | NO |
| wait/synch/mutex/innodb/recalc_pool_mutex                    | NO              | NO |
| wait/synch/mutex/innodb/fil_system_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/flush_list_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/fts_bg_threads_mutex                 | NO              | NO |
| wait/synch/mutex/innodb/fts_delete_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/fts_optimize_mutex                   | NO              | NO |
| wait/synch/mutex/innodb/fts_doc_id_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/log_flush_order_mutex                | NO              | NO |
| wait/synch/mutex/innodb/hash_table_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/ibuf_bitmap_mutex                    | NO              | NO |
| wait/synch/mutex/innodb/ibuf_mutex                           | NO              | NO |
| wait/synch/mutex/innodb/ibuf_pessimistic_insert_mutex        | NO              | NO |
| wait/synch/mutex/innodb/log_sys_mutex                        | NO              | NO |
| wait/synch/mutex/innodb/log_sys_write_mutex                  | NO              | NO |
| wait/synch/mutex/innodb/mutex_list_mutex                     | NO              | NO |
| wait/synch/mutex/innodb/page_zip_stat_per_index_mutex        | NO              | NO |
| wait/synch/mutex/innodb/purge_sys_pq_mutex                   | NO              | NO |
| wait/synch/mutex/innodb/recv_sys_mutex                       | NO              | NO |
| wait/synch/mutex/innodb/recv_writer_mutex                    | NO              | NO |
| wait/synch/mutex/innodb/redo_rseg_mutex                      | NO              | NO |
| wait/synch/mutex/innodb/noredo_rseg_mutex                    | NO              | NO |
| wait/synch/mutex/innodb/rw_lock_list_mutex                   | NO              | NO |
| wait/synch/mutex/innodb/rw_lock_mutex                        | NO              | NO |
| wait/synch/mutex/innodb/srv_dict_tmpfile_mutex               | NO              | NO |
| wait/synch/mutex/innodb/srv_innodb_monitor_mutex             | NO              | NO |
| wait/synch/mutex/innodb/srv_misc_tmpfile_mutex               | NO              | NO |
| wait/synch/mutex/innodb/srv_monitor_file_mutex               | NO              | NO |

```
| wait/synch/mutex/innodb/buf_dblwr_mutex | NO | NO |
| wait/synch/mutex/innodb/trx_undo_mutex | NO | NO |
| wait/synch/mutex/innodb/trx_pool_mutex | NO | NO |
| wait/synch/mutex/innodb/trx_pool_manager_mutex | NO | NO |
| wait/synch/mutex/innodb/srv_sys_mutex | NO | NO |
| wait/synch/mutex/innodb/lock_mutex | NO | NO |
| wait/synch/mutex/innodb/lock_wait_mutex | NO | NO |
| wait/synch/mutex/innodb/trx_mutex | NO | NO |
| wait/synch/mutex/innodb/srv_threads_mutex | NO | NO |
| wait/synch/mutex/innodb/rtr_active_mutex | NO | NO |
| wait/synch/mutex/innodb/rtr_match_mutex | NO | NO |
| wait/synch/mutex/innodb/rtr_path_mutex | NO | NO |
| wait/synch/mutex/innodb/rtr_ssn_mutex | NO | NO |
| wait/synch/mutex/innodb/trx_sys_mutex | NO | NO |
| wait/synch/mutex/innodb/zip_pad_mutex | NO | NO |
| wait/synch/mutex/innodb/master_key_id_mutex | NO | NO |
+---------------------------------------------------------+---------+-------+
```

2. Some InnoDB mutex instances are created at server startup and are only instrumented if the associated instrument is also enabled at server startup. To ensure that all InnoDB mutex instances are instrumented and enabled, add the following performance-schema-instrument rule to your MySQL configuration file:

```
performance-schema-instrument='wait/synch/mutex/innodb/%=ON'
```

If you do not require wait event data for all InnoDB mutexes, you can disable specific instruments by adding additional performance-schema-instrument rules to your MySQL configuration file. For example, to disable InnoDB mutex wait event instruments related to full-text search, add the following rule:

performance-schema-instrument='wait/synch/mutex/innodb/fts%=OFF'

![](_page_114_Picture_6.jpeg)

#### **Note**

Rules with a longer prefix such as wait/synch/mutex/innodb/fts% take precedence over rules with shorter prefixes such as wait/synch/ mutex/innodb/%.

After adding the performance-schema-instrument rules to your configuration file, restart the server. All the InnoDB mutexes except for those related to full text search are enabled. To verify, query the setup\_instruments table. The ENABLED and TIMED columns should be set to YES for the instruments that you enabled.

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE '%wait/synch/mutex/innodb%';
+-------------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------------------------------------------------+---------+-------+
| wait/synch/mutex/innodb/commit_cond_mutex | YES | YES |
| wait/synch/mutex/innodb/innobase_share_mutex | YES | YES |
| wait/synch/mutex/innodb/autoinc_mutex | YES | YES |
...
| wait/synch/mutex/innodb/master_key_id_mutex | YES | YES |
+-------------------------------------------------------+---------+-------+
49 rows in set (0.00 sec)
```

3. Enable wait event consumers by updating the setup\_consumers table. Wait event consumers are disabled by default.

```
mysql> UPDATE performance_schema.setup_consumers
 SET enabled = 'YES'
 WHERE name like 'events_waits%';
Query OK, 3 rows affected (0.00 sec)
```

```
Rows matched: 3 Changed: 3 Warnings: 0
```

You can verify that wait event consumers are enabled by querying the setup\_consumers table. The events\_waits\_current, events\_waits\_history, and events\_waits\_history\_long consumers should be enabled.

```
mysql> SELECT * FROM performance_schema.setup_consumers;
+----------------------------------+---------+
| NAME | ENABLED |
+----------------------------------+---------+
| events_stages_current | NO |
| events_stages_history | NO |
| events_stages_history_long | NO |
| events_statements_current | YES |
| events_statements_history | YES |
| events_statements_history_long | NO |
| events_transactions_current | YES |
| events_transactions_history | YES |
| events_transactions_history_long | NO |
| events_waits_current | YES |
| events_waits_history | YES |
| events_waits_history_long | YES |
| global_instrumentation | YES |
| thread_instrumentation | YES |
| statements_digest | YES |
+----------------------------------+---------+
15 rows in set (0.00 sec)
```

4. Once instruments and consumers are enabled, run the workload that you want to monitor. In this example, the mysqlslap load emulation client is used to simulate a workload.

```
$> ./mysqlslap --auto-generate-sql --concurrency=100 --iterations=10 
 --number-of-queries=1000 --number-char-cols=6 --number-int-cols=6;
```

- 5. Query the wait event data. In this example, wait event data is queried from the events\_waits\_summary\_global\_by\_event\_name table which aggregates data found in the events\_waits\_current, events\_waits\_history, and events\_waits\_history\_long tables. Data is summarized by event name (EVENT\_NAME), which is the name of the instrument that produced the event. Summarized data includes:
  - COUNT\_STAR

The number of summarized wait events.

• SUM\_TIMER\_WAIT

The total wait time of the summarized timed wait events.

• MIN\_TIMER\_WAIT

The minimum wait time of the summarized timed wait events.

• AVG\_TIMER\_WAIT

The average wait time of the summarized timed wait events.

• MAX\_TIMER\_WAIT

The maximum wait time of the summarized timed wait events.

The following query returns the instrument name (EVENT\_NAME), the number of wait events (COUNT\_STAR), and the total wait time for the events for that instrument (SUM\_TIMER\_WAIT). Because waits are timed in picoseconds (trillionths of a second) by default, wait times are divided by 1000000000 to show wait times in milliseconds. Data is presented in descending order, by the

number of summarized wait events (COUNT\_STAR). You can adjust the ORDER BY clause to order the data by total wait time.

| mysql> SELECT EVENT_NAME, COUNT_STAR, SUM_TIMER_WAIT/1000000000 SUM_TIMER_WAIT_MS<br>FROM performance_schema.events_waits_summary_global_by_event_name<br>WHERE SUM_TIMER_WAIT > 0 AND EVENT_NAME LIKE 'wait/synch/mutex/innodb/%'<br>ORDER BY COUNT_STAR DESC; |            |                                |  |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------------------------------|--|
| ++++<br>  EVENT_NAME<br>++++                                                                                                                                                                                                                                    |            | COUNT_STAR   SUM_TIMER_WAIT_MS |  |
| wait/synch/mutex/innodb/trx_mutex                                                                                                                                                                                                                               | <br>201111 | 23.4719                        |  |
| wait/synch/mutex/innodb/fil_system_mutex                                                                                                                                                                                                                        | <br>62244  | 9.6426                         |  |
| wait/synch/mutex/innodb/redo_rseg_mutex                                                                                                                                                                                                                         | <br>48238  | 3.1135                         |  |
| wait/synch/mutex/innodb/log_sys_mutex                                                                                                                                                                                                                           | <br>46113  | 2.0434                         |  |
| wait/synch/mutex/innodb/trx_sys_mutex                                                                                                                                                                                                                           | <br>35134  | 1068.1588                      |  |
| wait/synch/mutex/innodb/lock_mutex                                                                                                                                                                                                                              | <br>34872  | 1039.2589                      |  |
| wait/synch/mutex/innodb/log_sys_write_mutex                                                                                                                                                                                                                     | <br>17805  | 1526.0490                      |  |
| wait/synch/mutex/innodb/dict_sys_mutex                                                                                                                                                                                                                          | <br>14912  | 1606.7348                      |  |
| wait/synch/mutex/innodb/trx_undo_mutex                                                                                                                                                                                                                          | <br>10634  | 1.1424                         |  |
| wait/synch/mutex/innodb/rw_lock_list_mutex                                                                                                                                                                                                                      | <br>8538   | 0.1960                         |  |
| wait/synch/mutex/innodb/buf_pool_free_list_mutex                                                                                                                                                                                                                | <br>5961   | 0.6473                         |  |
| wait/synch/mutex/innodb/trx_pool_mutex                                                                                                                                                                                                                          | <br>4885   | 8821.7496                      |  |
| wait/synch/mutex/innodb/buf_pool_LRU_list_mutex                                                                                                                                                                                                                 | <br>4364   | 0.2077                         |  |
| wait/synch/mutex/innodb/innobase_share_mutex                                                                                                                                                                                                                    | <br>3212   | 0.2650                         |  |
| wait/synch/mutex/innodb/flush_list_mutex                                                                                                                                                                                                                        | <br>3178   | 0.2349                         |  |
| wait/synch/mutex/innodb/trx_pool_manager_mutex                                                                                                                                                                                                                  | <br>2495   | 0.1310                         |  |
| wait/synch/mutex/innodb/buf_pool_flush_state_mutex                                                                                                                                                                                                              | <br>1318   | 0.2161                         |  |
| wait/synch/mutex/innodb/log_flush_order_mutex                                                                                                                                                                                                                   | <br>1250   | 0.0893                         |  |
| wait/synch/mutex/innodb/buf_dblwr_mutex                                                                                                                                                                                                                         | <br>951    | 0.0918                         |  |
| wait/synch/mutex/innodb/recalc_pool_mutex                                                                                                                                                                                                                       | <br>670    | 0.0942                         |  |
| wait/synch/mutex/innodb/dict_persist_dirty_tables_mutex                                                                                                                                                                                                         | 345        | 0.0414                         |  |
| wait/synch/mutex/innodb/lock_wait_mutex                                                                                                                                                                                                                         | <br>303    | 0.1565                         |  |
| wait/synch/mutex/innodb/autoinc_mutex                                                                                                                                                                                                                           | <br>196    | 0.0213                         |  |
| wait/synch/mutex/innodb/autoinc_persisted_mutex                                                                                                                                                                                                                 | <br>196    | 0.0175                         |  |
| wait/synch/mutex/innodb/purge_sys_pq_mutex                                                                                                                                                                                                                      | <br>117    | 0.0308                         |  |
| wait/synch/mutex/innodb/srv_sys_mutex                                                                                                                                                                                                                           | <br>94     | 0.0077                         |  |
| wait/synch/mutex/innodb/ibuf_mutex                                                                                                                                                                                                                              | <br>22     | 0.0086                         |  |
| wait/synch/mutex/innodb/recv_sys_mutex                                                                                                                                                                                                                          | <br>12     | 0.0008                         |  |
| wait/synch/mutex/innodb/srv_innodb_monitor_mutex                                                                                                                                                                                                                | <br>4      | 0.0009                         |  |
| wait/synch/mutex/innodb/recv_writer_mutex                                                                                                                                                                                                                       | <br>1      | 0.0005                         |  |

![](_page_116_Picture_3.jpeg)

#### **Note**

The preceding result set includes wait event data produced during the startup process. To exclude this data, you can truncate the events\_waits\_summary\_global\_by\_event\_name table immediately after startup and before running your workload. However, the truncate operation itself may produce a negligible amount wait event data.

mysql> **TRUNCATE performance\_schema.events\_waits\_summary\_global\_by\_event\_name;**

# <span id="page-116-0"></span>**17.17 InnoDB Monitors**

InnoDB monitors provide information about the InnoDB internal state. This information is useful for performance tuning.