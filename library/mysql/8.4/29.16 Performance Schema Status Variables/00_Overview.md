---
source: MySQL 8.4 Reference
title: 00_Overview
---

The Performance Schema implements several status variables that provide information about instrumentation that could not be loaded or created due to memory constraints:

```
mysql> SHOW STATUS LIKE 'perf%';
+-------------------------------------------------------+-------+
| Variable_name | Value |
+-------------------------------------------------------+-------+
| Performance_schema_accounts_lost | 0 |
| Performance_schema_cond_classes_lost | 0 |
| Performance_schema_cond_instances_lost | 0 |
| Performance_schema_digest_lost | 0 |
| Performance_schema_file_classes_lost | 0 |
| Performance_schema_file_handles_lost | 0 |
| Performance_schema_file_instances_lost | 0 |
| Performance_schema_hosts_lost | 0 |
| Performance_schema_index_stat_lost | 0 |
| Performance_schema_locker_lost | 0 |
| Performance_schema_memory_classes_lost | 0 |
| Performance_schema_metadata_lock_lost | 0 |
| Performance_schema_meter_lost | 0 |
| Performance_schema_metric_lost | 0 |
| Performance_schema_mutex_classes_lost | 0 |
| Performance_schema_mutex_instances_lost | 0 |
| Performance_schema_nested_statement_lost | 0 |
| Performance_schema_prepared_statements_lost | 0 |
| Performance_schema_program_lost | 0 |
| Performance_schema_rwlock_classes_lost | 0 |
| Performance_schema_rwlock_instances_lost | 0 |
| Performance_schema_session_connect_attrs_longest_seen | 131 |
| Performance_schema_session_connect_attrs_lost | 0 |
| Performance_schema_socket_classes_lost | 0 |
| Performance_schema_socket_instances_lost | 0 |
| Performance_schema_stage_classes_lost | 0 |
| Performance_schema_statement_classes_lost | 0 |
| Performance_schema_table_handles_lost | 0 |
| Performance_schema_table_instances_lost | 0 |
| Performance_schema_table_lock_stat_lost | 0 |
| Performance_schema_thread_classes_lost | 0 |
| Performance_schema_thread_instances_lost | 0 |
| Performance_schema_users_lost | 0 |
+-------------------------------------------------------+-------+
```

For information on using these variables to check Performance Schema status, see Section 29.7, "Performance Schema Status Monitoring".

Performance Schema status variables have the following meanings:

<span id="page-188-0"></span>• [Performance\\_schema\\_accounts\\_lost](#page-188-0)

The number of times a row could not be added to the [accounts](#page-56-0) table because it was full.

<span id="page-188-1"></span>• [Performance\\_schema\\_cond\\_classes\\_lost](#page-188-1)

How many condition instruments could not be loaded.

<span id="page-188-2"></span>• [Performance\\_schema\\_cond\\_instances\\_lost](#page-188-2)

How many condition instrument instances could not be created.

<span id="page-188-3"></span>• [Performance\\_schema\\_digest\\_lost](#page-188-3)

The number of digest instances that could not be instrumented in the [events\\_statements\\_summary\\_by\\_digest](#page-120-0) table. This can be nonzero if the value of [performance\\_schema\\_digests\\_size](#page-170-0) is too small.

<span id="page-188-4"></span>• [Performance\\_schema\\_file\\_classes\\_lost](#page-188-4)

How many file instruments could not be loaded.

<span id="page-189-1"></span>• [Performance\\_schema\\_file\\_handles\\_lost](#page-189-1)

How many file instrument instances could not be opened.

<span id="page-189-2"></span>• [Performance\\_schema\\_file\\_instances\\_lost](#page-189-2)

How many file instrument instances could not be created.

<span id="page-189-3"></span>• [Performance\\_schema\\_hosts\\_lost](#page-189-3)

The number of times a row could not be added to the [hosts](#page-56-1) table because it was full.

<span id="page-189-12"></span>• [Performance\\_schema\\_index\\_stat\\_lost](#page-189-12)

The number of indexes for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_index\\_stat](#page-176-2) is too small.

<span id="page-189-4"></span>• [Performance\\_schema\\_locker\\_lost](#page-189-4)

How many events are "lost" or not recorded, due to the following conditions:

- Events are recursive (for example, waiting for A caused a wait on B, which caused a wait on C).
- The depth of the nested events stack is greater than the limit imposed by the implementation.

Events recorded by the Performance Schema are not recursive, so this variable should always be 0.

<span id="page-189-5"></span>• [Performance\\_schema\\_memory\\_classes\\_lost](#page-189-5)

The number of times a memory instrument could not be loaded.

<span id="page-189-6"></span>• [Performance\\_schema\\_metadata\\_lock\\_lost](#page-189-6)

The number of metadata locks that could not be instrumented in the [metadata\\_locks](#page-92-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_metadata\\_locks](#page-177-0) is too small.

<span id="page-189-7"></span>• [Performance\\_schema\\_meter\\_lost](#page-189-7)

Number of meter instruments that failed to be created.

<span id="page-189-8"></span>• [Performance\\_schema\\_metric\\_lost](#page-189-8)

Number of metric instruments that failed to be created.

<span id="page-189-9"></span>• [Performance\\_schema\\_mutex\\_classes\\_lost](#page-189-9)

How many mutex instruments could not be loaded.

<span id="page-189-10"></span>• [Performance\\_schema\\_mutex\\_instances\\_lost](#page-189-10)

How many mutex instrument instances could not be created.

<span id="page-189-11"></span>• [Performance\\_schema\\_nested\\_statement\\_lost](#page-189-11)

The number of stored program statements for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_statement\\_stack](#page-183-1) is too small.

<span id="page-189-0"></span>• [Performance\\_schema\\_prepared\\_statements\\_lost](#page-189-0)

The number of prepared statements that could not be instrumented in the [prepared\\_statements\\_instances](#page-44-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-179-0) is too small. <span id="page-190-2"></span>• [Performance\\_schema\\_program\\_lost](#page-190-2)

The number of stored programs for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_program\\_instances](#page-180-0) is too small.

<span id="page-190-3"></span>• [Performance\\_schema\\_rwlock\\_classes\\_lost](#page-190-3)

How many rwlock instruments could not be loaded.

<span id="page-190-4"></span>• [Performance\\_schema\\_rwlock\\_instances\\_lost](#page-190-4)

How many rwlock instrument instances could not be created.

<span id="page-190-0"></span>• [Performance\\_schema\\_session\\_connect\\_attrs\\_longest\\_seen](#page-190-0)

In addition to the connection attribute size-limit check performed by the Performance Schema against the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-185-0) system variable, the server performs a preliminary check, imposing a limit of 64KB on the aggregate size of connection attribute data it accepts. If a client attempts to send more than 64KB of attribute data, the server rejects the connection. Otherwise, the server considers the attribute buffer valid and tracks the size of the longest such buffer in the [Performance\\_schema\\_session\\_connect\\_attrs\\_longest\\_seen](#page-190-0) status variable. If this value is larger than [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-185-0), DBAs may wish to increase the latter value, or, alternatively, investigate which clients are sending large amounts of attribute data.

For more information about connection attributes, see [Section 29.12.9, "Performance Schema](#page-58-1) [Connection Attribute Tables".](#page-58-1)

<span id="page-190-1"></span>• [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-190-1)

The number of connections for which connection attribute truncation has occurred. For a given connection, if the client sends connection attribute key-value pairs for which the aggregate size is larger than the reserved storage permitted by the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-185-0) system variable, the Performance Schema truncates the attribute data and increments [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-190-1). If this value is nonzero, you may wish to set [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-185-0) to a larger value.

For more information about connection attributes, see [Section 29.12.9, "Performance Schema](#page-58-1) [Connection Attribute Tables".](#page-58-1)

<span id="page-190-5"></span>• [Performance\\_schema\\_socket\\_classes\\_lost](#page-190-5)

How many socket instruments could not be loaded.

<span id="page-190-6"></span>• [Performance\\_schema\\_socket\\_instances\\_lost](#page-190-6)

How many socket instrument instances could not be created.

<span id="page-190-7"></span>• [Performance\\_schema\\_stage\\_classes\\_lost](#page-190-7)

How many stage instruments could not be loaded.

<span id="page-190-8"></span>• [Performance\\_schema\\_statement\\_classes\\_lost](#page-190-8)

How many statement instruments could not be loaded.

<span id="page-190-9"></span>• [Performance\\_schema\\_table\\_handles\\_lost](#page-190-9)

How many table instrument instances could not be opened. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_handles](#page-183-0) is too small.

<span id="page-191-1"></span>• [Performance\\_schema\\_table\\_instances\\_lost](#page-191-1)

How many table instrument instances could not be created.

<span id="page-191-4"></span>• [Performance\\_schema\\_table\\_lock\\_stat\\_lost](#page-191-4)

The number of tables for which lock statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_lock\\_stat](#page-184-1) is too small.

<span id="page-191-2"></span>• [Performance\\_schema\\_thread\\_classes\\_lost](#page-191-2)

How many thread instruments could not be loaded.

<span id="page-191-0"></span>• [Performance\\_schema\\_thread\\_instances\\_lost](#page-191-0)

The number of thread instances that could not be instrumented in the [threads](#page-156-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_thread\\_instances](#page-185-1) is too small.

• [Performance\\_schema\\_users\\_lost](#page-191-3)

The number of times a row could not be added to the [users](#page-57-0) table because it was full.

# <span id="page-191-3"></span>**29.17 The Performance Schema Memory-Allocation Model**

The Performance Schema uses this memory allocation model:

- May allocate memory at server startup
- May allocate additional memory during server operation
- Never free memory during server operation (although it might be recycled)
- Free all memory used at shutdown

The result is to relax memory constraints so that the Performance Schema can be used with less configuration, and to decrease the memory footprint so that consumption scales with server load. Memory used depends on the load actually seen, not the load estimated or explicitly configured for.

Several Performance Schema sizing parameters are autoscaled and need not be configured explicitly unless you want to establish an explicit limit on memory allocation:

```
performance_schema_accounts_size
performance_schema_hosts_size
performance_schema_max_cond_instances
performance_schema_max_file_instances
performance_schema_max_index_stat
performance_schema_max_metadata_locks
performance_schema_max_mutex_instances
performance_schema_max_prepared_statements_instances
performance_schema_max_program_instances
performance_schema_max_rwlock_instances
performance_schema_max_socket_instances
performance_schema_max_table_handles
performance_schema_max_table_instances
performance_schema_max_table_lock_stat
performance_schema_max_thread_instances
performance_schema_users_size
```

For an autoscaled parameter, configuration works like this:

- With the value set to -1 (the default), the parameter is autoscaled:
  - The corresponding internal buffer is empty initially and no memory is allocated.
  - As the Performance Schema collects data, memory is allocated in the corresponding buffer. The buffer size is unbounded, and may grow with the load.

- With the value set to 0:
  - The corresponding internal buffer is empty initially and no memory is allocated.
- With the value set to N > 0:
  - The corresponding internal buffer is empty initially and no memory is allocated.
  - As the Performance Schema collects data, memory is allocated in the corresponding buffer, until the buffer size reaches N.
  - Once the buffer size reaches N, no more memory is allocated. Data collected by the Performance Schema for this buffer is lost, and any corresponding "lost instance" counters are incremented.

To see how much memory the Performance Schema is using, check the instruments designed for that purpose. The Performance Schema allocates memory internally and associates each buffer with a dedicated instrument so that memory consumption can be traced to individual buffers. Instruments named with the prefix memory/performance\_schema/ expose how much memory is allocated for these internal buffers. The buffers are global to the server, so the instruments are displayed only in the [memory\\_summary\\_global\\_by\\_event\\_name](#page-134-0) table, and not in other memory\_summary\_by\_xxx\_by\_event\_name tables.

This query shows the information associated with the memory instruments:

```
SELECT * FROM performance_schema.memory_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'memory/performance_schema/%';
```