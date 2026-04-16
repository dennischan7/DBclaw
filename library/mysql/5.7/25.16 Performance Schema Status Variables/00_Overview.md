---
source: MySQL 5.7 Reference
title: 00_Overview
---

The Performance Schema implements several status variables that provide information about instrumentation that could not be loaded or created due to memory constraints:

| +++<br>  Variable_name<br>  Value  <br>+++<br>  Performance_schema_accounts_lost<br>  0<br>  Performance_schema_cond_classes_lost<br>  0 |
|------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                          |
|                                                                                                                                          |
|                                                                                                                                          |
|                                                                                                                                          |
| Performance_schema_cond_instances_lost<br>  0                                                                                            |
| Performance_schema_file_classes_lost<br>  0                                                                                              |
| Performance_schema_file_handles_lost<br>  0                                                                                              |
| Performance_schema_file_instances_lost<br>  0                                                                                            |
| Performance_schema_hosts_lost<br>  0                                                                                                     |
| Performance_schema_locker_lost<br>  0                                                                                                    |
| Performance_schema_mutex_classes_lost<br>  0                                                                                             |
| Performance_schema_mutex_instances_lost<br>  0                                                                                           |
| Performance_schema_rwlock_classes_lost<br>  0                                                                                            |
| Performance_schema_rwlock_instances_lost   0                                                                                             |
| Performance_schema_socket_classes_lost<br>  0                                                                                            |
| Performance_schema_socket_instances_lost   0                                                                                             |
| Performance_schema_stage_classes_lost<br>  0                                                                                             |
| Performance_schema_statement_classes_lost   0                                                                                            |
| Performance_schema_table_handles_lost<br>  0                                                                                             |
| Performance_schema_table_instances_lost<br>  0                                                                                           |
| Performance_schema_thread_classes_lost<br>  0                                                                                            |
| Performance_schema_thread_instances_lost   0                                                                                             |
| Performance_schema_users_lost<br>  0                                                                                                     |
| +++                                                                                                                                      |

For information on using these variables to check Performance Schema status, see Section 25.7, "Performance Schema Status Monitoring".

Performance Schema status variables have the following meanings:

<span id="page-125-1"></span>• [Performance\\_schema\\_accounts\\_lost](#page-125-1)

The number of times a row could not be added to the [accounts](#page-51-0) table because it was full.

<span id="page-125-2"></span>• [Performance\\_schema\\_cond\\_classes\\_lost](#page-125-2)

How many condition instruments could not be loaded.

<span id="page-126-3"></span>• [Performance\\_schema\\_cond\\_instances\\_lost](#page-126-3)

How many condition instrument instances could not be created.

<span id="page-126-4"></span>• [Performance\\_schema\\_digest\\_lost](#page-126-4)

The number of digest instances that could not be instrumented in the [events\\_statements\\_summary\\_by\\_digest](#page-78-0) table. This can be nonzero if the value of [performance\\_schema\\_digests\\_size](#page-110-0) is too small.

<span id="page-126-5"></span>• [Performance\\_schema\\_file\\_classes\\_lost](#page-126-5)

How many file instruments could not be loaded.

<span id="page-126-6"></span>• [Performance\\_schema\\_file\\_handles\\_lost](#page-126-6)

How many file instrument instances could not be opened.

<span id="page-126-7"></span>• [Performance\\_schema\\_file\\_instances\\_lost](#page-126-7)

How many file instrument instances could not be created.

<span id="page-126-8"></span>• [Performance\\_schema\\_hosts\\_lost](#page-126-8)

The number of times a row could not be added to the [hosts](#page-52-0) table because it was full.

<span id="page-126-13"></span>• [Performance\\_schema\\_index\\_stat\\_lost](#page-126-13)

The number of indexes for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_index\\_stat](#page-115-2) is too small.

<span id="page-126-9"></span>• [Performance\\_schema\\_locker\\_lost](#page-126-9)

How many events are "lost" or not recorded, due to the following conditions:

- Events are recursive (for example, waiting for A caused a wait on B, which caused a wait on C).
- The depth of the nested events stack is greater than the limit imposed by the implementation.

Events recorded by the Performance Schema are not recursive, so this variable should always be 0.

<span id="page-126-10"></span>• [Performance\\_schema\\_memory\\_classes\\_lost](#page-126-10)

The number of times a memory instrument could not be loaded.

<span id="page-126-11"></span>• [Performance\\_schema\\_metadata\\_lock\\_lost](#page-126-11)

The number of metadata locks that could not be instrumented in the [metadata\\_locks](#page-67-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_metadata\\_locks](#page-116-0) is too small.

<span id="page-126-0"></span>• [Performance\\_schema\\_mutex\\_classes\\_lost](#page-126-0)

How many mutex instruments could not be loaded.

<span id="page-126-1"></span>• [Performance\\_schema\\_mutex\\_instances\\_lost](#page-126-1)

How many mutex instrument instances could not be created.

<span id="page-126-12"></span>• [Performance\\_schema\\_nested\\_statement\\_lost](#page-126-12)

The number of stored program statements for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_statement\\_stack](#page-120-2) is too small.

<span id="page-126-2"></span>• [Performance\\_schema\\_prepared\\_statements\\_lost](#page-126-2)

The number of prepared statements that could not be instrumented in the [prepared\\_statements\\_instances](#page-40-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-117-1) is too small.

<span id="page-127-1"></span>• [Performance\\_schema\\_program\\_lost](#page-127-1)

The number of stored programs for which statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_program\\_instances](#page-118-0) is too small.

<span id="page-127-2"></span>• [Performance\\_schema\\_rwlock\\_classes\\_lost](#page-127-2)

How many rwlock instruments could not be loaded.

<span id="page-127-3"></span>• [Performance\\_schema\\_rwlock\\_instances\\_lost](#page-127-3)

How many rwlock instrument instances could not be created.

<span id="page-127-0"></span>• [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-127-0)

The number of connections for which connection attribute truncation has occurred. For a given connection, if the client sends connection attribute key-value pairs for which the aggregate size is larger than the reserved storage permitted by the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) system variable, the Performance Schema truncates the attribute data and increments [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-127-0). If this value is nonzero, you may wish to set [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) to a larger value.

For more information about connection attributes, see [Section 25.12.9, "Performance Schema](#page-53-1) [Connection Attribute Tables".](#page-53-1)

<span id="page-127-4"></span>• [Performance\\_schema\\_socket\\_classes\\_lost](#page-127-4)

How many socket instruments could not be loaded.

<span id="page-127-5"></span>• [Performance\\_schema\\_socket\\_instances\\_lost](#page-127-5)

How many socket instrument instances could not be created.

<span id="page-127-6"></span>• [Performance\\_schema\\_stage\\_classes\\_lost](#page-127-6)

How many stage instruments could not be loaded.

<span id="page-127-7"></span>• [Performance\\_schema\\_statement\\_classes\\_lost](#page-127-7)

How many statement instruments could not be loaded.

<span id="page-127-8"></span>• [Performance\\_schema\\_table\\_handles\\_lost](#page-127-8)

How many table instrument instances could not be opened. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_handles](#page-121-0) is too small.

<span id="page-127-9"></span>• [Performance\\_schema\\_table\\_instances\\_lost](#page-127-9)

How many table instrument instances could not be created.

<span id="page-127-11"></span>• [Performance\\_schema\\_table\\_lock\\_stat\\_lost](#page-127-11)

The number of tables for which lock statistics were lost. This can be nonzero if the value of [performance\\_schema\\_max\\_table\\_lock\\_stat](#page-121-2) is too small.

<span id="page-127-10"></span>• [Performance\\_schema\\_thread\\_classes\\_lost](#page-127-10)

How many thread instruments could not be loaded.

<span id="page-128-0"></span>• [Performance\\_schema\\_thread\\_instances\\_lost](#page-128-0)

The number of thread instances that could not be instrumented in the [threads](#page-100-0) table. This can be nonzero if the value of [performance\\_schema\\_max\\_thread\\_instances](#page-122-0) is too small.

• [Performance\\_schema\\_users\\_lost](#page-128-1)

The number of times a row could not be added to the [users](#page-52-1) table because it was full.

# <span id="page-128-1"></span>**25.17 The Performance Schema Memory-Allocation Model**

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

• Once the buffer size reaches N, no more memory is allocated. Data collected by the Performance Schema for this buffer is lost, and any corresponding "lost instance" counters are incremented.

To see how much memory the Performance Schema is using, check the instruments designed for that purpose. The Performance Schema allocates memory internally and associates each buffer with a dedicated instrument so that memory consumption can be traced to individual buffers. Instruments named with the prefix memory/performance\_schema/ expose how much memory is allocated for these internal buffers. The buffers are global to the server, so the instruments are displayed only in the [memory\\_summary\\_global\\_by\\_event\\_name](#page-88-0) table, and not in other memory\_summary\_by\_xxx\_by\_event\_name tables.

This query shows the information associated with the memory instruments:

```
SELECT * FROM performance_schema.memory_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'memory/performance_schema/%';
```