---
source: MySQL 8.0 Reference
title: 00_Overview
---

The Performance Schema implements several status variables that provide information about instrumentation that could not be loaded or created due to memory constraints:

```
mysql> SHOW STATUS LIKE 'perf%';
+-------------------------------------------+-------+
| Variable_name | Value |
+-------------------------------------------+-------+
| Performance_schema_accounts_lost | 0 |
| Performance_schema_cond_classes_lost | 0 |
| Performance_schema_cond_instances_lost | 0 |
| Performance_schema_file_classes_lost | 0 |
| Performance_schema_file_handles_lost | 0 |
| Performance_schema_file_instances_lost | 0 |
| Performance_schema_hosts_lost | 0 |
| Performance_schema_locker_lost | 0 |
| Performance_schema_mutex_classes_lost | 0 |
| Performance_schema_mutex_instances_lost | 0 |
| Performance_schema_rwlock_classes_lost | 0 |
| Performance_schema_rwlock_instances_lost | 0 |
| Performance_schema_socket_classes_lost | 0 |
| Performance_schema_socket_instances_lost | 0 |
| Performance_schema_stage_classes_lost | 0 |
| Performance_schema_statement_classes_lost | 0 |
| Performance_schema_table_handles_lost | 0 |
| Performance_schema_table_instances_lost | 0 |
| Performance_schema_thread_classes_lost | 0 |
| Performance_schema_thread_instances_lost | 0 |
| Performance_schema_users_lost | 0 |
+-------------------------------------------+-------+
```

For information on using these variables to check Performance Schema status, see Section 29.7, "Performance Schema Status Monitoring".

Performance Schema status variables have the following meanings:

<span id="page-130-0"></span>• [Performance\\_schema\\_accounts\\_lost](#page-130-0)

The number of times a row could not be added to the [accounts](#page-0-0) table because it was full.

<span id="page-130-1"></span>• [Performance\\_schema\\_cond\\_classes\\_lost](#page-130-1)

How many condition instruments could not be loaded.

<span id="page-130-2"></span>• [Performance\\_schema\\_cond\\_instances\\_lost](#page-130-2)

How many condition instrument instances could not be created.

<span id="page-130-3"></span>• [Performance\\_schema\\_digest\\_lost](#page-130-3)

The number of digest instances that could not be instrumented in the [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table. This can be nonzero if the value of [performance\\_schema\\_digests\\_size](#page-113-0) is too small.

<span id="page-130-4"></span>• [Performance\\_schema\\_file\\_classes\\_lost](#page-130-4)

How many file instruments could not be loaded.

<span id="page-130-5"></span>• [Performance\\_schema\\_file\\_handles\\_lost](#page-130-5)

How many file instrument instances could not be opened.

<span id="page-131-0"></span>• [Performance\\_schema\\_file\\_instances\\_lost](#page-131-0)

How many file instrument instances could not be created.

<span id="page-131-1"></span>• [Performance\\_schema\\_hosts\\_lost](#page-131-1)

The number of times a row could not be added to the [hosts](#page-1-0) table because it was full.

<span id="page-131-12"></span>• [Performance\\_schema\\_index\\_stat\\_lost](#page-131-12)

The number of indexes for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_index\\_stat](#page-119-2) is too small.

<span id="page-131-2"></span>• [Performance\\_schema\\_locker\\_lost](#page-131-2)

How many events are "lost" or not recorded, due to the following conditions:

- Events are recursive (for example, waiting for A caused a wait on B, which caused a wait on C).
- The depth of the nested events stack is greater than the limit imposed by the implementation.

Events recorded by the Performance Schema are not recursive, so this variable should always be 0.

<span id="page-131-3"></span>• [Performance\\_schema\\_memory\\_classes\\_lost](#page-131-3)

The number of times a memory instrument could not be loaded.

<span id="page-131-4"></span>• [Performance\\_schema\\_metadata\\_lock\\_lost](#page-131-4)

The number of metadata locks that could not be instrumented in the [metadata\\_locks](#page-39-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_metadata\\_locks](#page-120-0) is too small.

<span id="page-131-5"></span>• [Performance\\_schema\\_mutex\\_classes\\_lost](#page-131-5)

How many mutex instruments could not be loaded.

<span id="page-131-6"></span>• [Performance\\_schema\\_mutex\\_instances\\_lost](#page-131-6)

How many mutex instrument instances could not be created.

<span id="page-131-7"></span>• [Performance\\_schema\\_nested\\_statement\\_lost](#page-131-7)

The number of stored program statements for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_statement\\_stack](#page-125-1) is too small.

<span id="page-131-8"></span>• [Performance\\_schema\\_prepared\\_statements\\_lost](#page-131-8)

The number of prepared statements that could not be instrumented in the prepared\_statements\_instances table. This can be nonzero if the value of [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-121-2) is too small.

<span id="page-131-9"></span>• [Performance\\_schema\\_program\\_lost](#page-131-9)

The number of stored programs for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_program\\_instances](#page-122-0) is too small.

<span id="page-131-10"></span>• [Performance\\_schema\\_rwlock\\_classes\\_lost](#page-131-10)

How many rwlock instruments could not be loaded.

<span id="page-131-11"></span>• [Performance\\_schema\\_rwlock\\_instances\\_lost](#page-131-11)

How many rwlock instrument instances could not be created.

<span id="page-132-0"></span>• [Performance\\_schema\\_session\\_connect\\_attrs\\_longest\\_seen](#page-132-0)

In addition to the connection attribute size-limit check performed by the Performance Schema against the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) system variable, the server performs a preliminary check, imposing a limit of 64KB on the aggregate size of connection attribute data it accepts. If a client attempts to send more than 64KB of attribute data, the server rejects the connection. Otherwise, the server considers the attribute buffer valid and tracks the size of the longest such buffer in the [Performance\\_schema\\_session\\_connect\\_attrs\\_longest\\_seen](#page-132-0) status variable. If this value is larger than [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0), DBAs may wish to increase the latter value, or, alternatively, investigate which clients are sending large amounts of attribute data.

For more information about connection attributes, see [Section 29.12.9, "Performance Schema](#page-2-0) [Connection Attribute Tables".](#page-2-0)

<span id="page-132-1"></span>• [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-132-1)

The number of connections for which connection attribute truncation has occurred. For a given connection, if the client sends connection attribute key-value pairs for which the aggregate size is larger than the reserved storage permitted by the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) system variable, the Performance Schema truncates the attribute data and increments [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-132-1). If this value is nonzero, you may wish to set [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) to a larger value.

For more information about connection attributes, see [Section 29.12.9, "Performance Schema](#page-2-0) [Connection Attribute Tables".](#page-2-0)

<span id="page-132-2"></span>• [Performance\\_schema\\_socket\\_classes\\_lost](#page-132-2)

How many socket instruments could not be loaded.

<span id="page-132-3"></span>• [Performance\\_schema\\_socket\\_instances\\_lost](#page-132-3)

How many socket instrument instances could not be created.

<span id="page-132-4"></span>• [Performance\\_schema\\_stage\\_classes\\_lost](#page-132-4)

How many stage instruments could not be loaded.

<span id="page-132-5"></span>• [Performance\\_schema\\_statement\\_classes\\_lost](#page-132-5)

How many statement instruments could not be loaded.

<span id="page-132-6"></span>• [Performance\\_schema\\_table\\_handles\\_lost](#page-132-6)

How many table instrument instances could not be opened. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_handles](#page-125-0) is too small.

<span id="page-132-7"></span>• [Performance\\_schema\\_table\\_instances\\_lost](#page-132-7)

How many table instrument instances could not be created.

<span id="page-132-9"></span>• [Performance\\_schema\\_table\\_lock\\_stat\\_lost](#page-132-9)

The number of tables for which lock statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_lock\\_stat](#page-126-2) is too small.

<span id="page-132-8"></span>• [Performance\\_schema\\_thread\\_classes\\_lost](#page-132-8)

How many thread instruments could not be loaded.

<span id="page-133-0"></span>• [Performance\\_schema\\_thread\\_instances\\_lost](#page-133-0)

The number of thread instances that could not be instrumented in the [threads](#page-99-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_thread\\_instances](#page-127-1) is too small.

• [Performance\\_schema\\_users\\_lost](#page-133-1)

The number of times a row could not be added to the [users](#page-1-1) table because it was full.

# <span id="page-133-1"></span>**29.17 The Performance Schema Memory-Allocation Model**

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

To see how much memory the Performance Schema is using, check the instruments designed for that purpose. The Performance Schema allocates memory internally and associates each buffer with a dedicated instrument so that memory consumption can be traced to individual buffers. Instruments named with the prefix memory/performance\_schema/ expose how much memory is allocated for these internal buffers. The buffers are global to the server, so the instruments are displayed only in the [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0) table, and not in other memory\_summary\_by\_xxx\_by\_event\_name tables.

This query shows the information associated with the memory instruments:

```
SELECT * FROM performance_schema.memory_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'memory/performance_schema/%';
```