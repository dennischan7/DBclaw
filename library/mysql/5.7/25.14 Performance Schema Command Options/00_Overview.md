---
source: MySQL 5.7 Reference
title: 00_Overview
---

Performance Schema parameters can be specified at server startup on the command line or in option files to configure Performance Schema instruments and consumers. Runtime configuration is also possible in many cases (see Section 25.4, "Performance Schema Runtime Configuration"), but startup configuration must be used when runtime configuration is too late to affect instruments that have already been initialized during the startup process.

Performance Schema consumers and instruments can be configured at startup using the following syntax. For additional details, see Section 25.3, "Performance Schema Startup Configuration".

<span id="page-107-1"></span>• [--performance-schema-consumer-](#page-107-1)consumer\_name=value

Configure a Performance Schema consumer. Consumer names in the [setup\\_consumers](#page-12-0) table use underscores, but for consumers set at startup, dashes and underscores within the name are equivalent. Options for configuring individual consumers are detailed later in this section.

<span id="page-107-0"></span>• [--performance-schema-instrument=](#page-107-0)instrument\_name=value

Configure a Performance Schema instrument. The name may be given as a pattern to configure instruments that match the pattern.

The following items configure individual consumers:

- <span id="page-108-0"></span>• [--performance-schema-consumer-events-stages-current=value](#page-108-0) Configure the events-stages-current consumer.
- <span id="page-108-1"></span>• [--performance-schema-consumer-events-stages-history=value](#page-108-1) Configure the events-stages-history consumer.
- <span id="page-108-2"></span>• [--performance-schema-consumer-events-stages-history-long=value](#page-108-2) Configure the events-stages-history-long consumer.
- <span id="page-108-3"></span>• [--performance-schema-consumer-events-statements-current=value](#page-108-3) Configure the events-statements-current consumer.
- <span id="page-108-4"></span>• [--performance-schema-consumer-events-statements-history=value](#page-108-4) Configure the events-statements-history consumer.
- <span id="page-108-5"></span>• [--performance-schema-consumer-events-statements-history-long=value](#page-108-5) Configure the events-statements-history-long consumer.
- <span id="page-108-6"></span>• [--performance-schema-consumer-events-transactions-current=value](#page-108-6) Configure the Performance Schema events-transactions-current consumer.
- <span id="page-108-7"></span>• [--performance-schema-consumer-events-transactions-history=value](#page-108-7) Configure the Performance Schema events-transactions-history consumer.
- <span id="page-108-8"></span>• [--performance-schema-consumer-events-transactions-history-long=value](#page-108-8) Configure the Performance Schema events-transactions-history-long consumer.
- <span id="page-108-9"></span>• [--performance-schema-consumer-events-waits-current=value](#page-108-9) Configure the events-waits-current consumer.
- <span id="page-108-10"></span>• [--performance-schema-consumer-events-waits-history=value](#page-108-10) Configure the events-waits-history consumer.
- <span id="page-108-11"></span>• [--performance-schema-consumer-events-waits-history-long=value](#page-108-11) Configure the events-waits-history-long consumer.
- <span id="page-108-12"></span>• [--performance-schema-consumer-global-instrumentation=value](#page-108-12) Configure the global-instrumentation consumer.
- <span id="page-108-13"></span>• [--performance-schema-consumer-statements-digest=value](#page-108-13) Configure the statements-digest consumer.
- [--performance-schema-consumer-thread-instrumentation=value](#page-108-14) Configure the thread-instrumentation consumer.

# <span id="page-108-14"></span>**25.15 Performance Schema System Variables**

The Performance Schema implements several system variables that provide configuration information:

```
mysql> SHOW VARIABLES LIKE 'perf%';
+----------------------------------------------------------+-------+
| Variable_name | Value |
+----------------------------------------------------------+-------+
| performance_schema | ON |
| performance_schema_accounts_size | -1 |
| performance_schema_digests_size | 10000 |
| performance_schema_events_stages_history_long_size | 10000 |
| performance_schema_events_stages_history_size | 10 |
| performance_schema_events_statements_history_long_size | 10000 |
| performance_schema_events_statements_history_size | 10 |
| performance_schema_events_transactions_history_long_size | 10000 |
| performance_schema_events_transactions_history_size | 10 |
| performance_schema_events_waits_history_long_size | 10000 |
| performance_schema_events_waits_history_size | 10 |
| performance_schema_hosts_size | -1 |
| performance_schema_max_cond_classes | 80 |
| performance_schema_max_cond_instances | -1 |
| performance_schema_max_digest_length | 1024 |
| performance_schema_max_file_classes | 50 |
| performance_schema_max_file_handles | 32768 |
| performance_schema_max_file_instances | -1 |
| performance_schema_max_index_stat | -1 |
| performance_schema_max_memory_classes | 320 |
| performance_schema_max_metadata_locks | -1 |
| performance_schema_max_mutex_classes | 200 |
| performance_schema_max_mutex_instances | -1 |
| performance_schema_max_prepared_statements_instances | -1 |
| performance_schema_max_program_instances | -1 |
| performance_schema_max_rwlock_classes | 40 |
| performance_schema_max_rwlock_instances | -1 |
| performance_schema_max_socket_classes | 10 |
| performance_schema_max_socket_instances | -1 |
| performance_schema_max_sql_text_length | 1024 |
| performance_schema_max_stage_classes | 150 |
| performance_schema_max_statement_classes | 192 |
| performance_schema_max_statement_stack | 10 |
| performance_schema_max_table_handles | -1 |
| performance_schema_max_table_instances | -1 |
| performance_schema_max_table_lock_stat | -1 |
| performance_schema_max_thread_classes | 50 |
| performance_schema_max_thread_instances | -1 |
| performance_schema_session_connect_attrs_size | 512 |
| performance_schema_setup_actors_size | -1 |
| performance_schema_setup_objects_size | -1 |
| performance_schema_users_size | -1 |
+----------------------------------------------------------+-------+
```

Performance Schema system variables can be set at server startup on the command line or in option files, and many can be set at runtime. See [Section 25.13, "Performance Schema Option and Variable](#page-104-0) [Reference"](#page-104-0).

The Performance Schema automatically sizes the values of several of its parameters at server startup if they are not set explicitly. For more information, see Section 25.3, "Performance Schema Startup Configuration".

Performance Schema system variables have the following meanings:

<span id="page-109-0"></span>• [performance\\_schema](#page-109-0)

| Command-Line Format | performance-schema[={OFF ON}] |
|---------------------|-------------------------------|
| System Variable     | performance_schema            |
| Scope               | Global                        |
| Dynamic             | No                            |
| Type                | Boolean                       |
| Default Value       | ON                            |

The value of this variable is ON or OFF to indicate whether the Performance Schema is enabled. By default, the value is ON. At server startup, you can specify this variable with no value or a value of ON or 1 to enable it, or with a value of OFF or 0 to disable it.

Even when the Performance Schema is disabled, it continues to populate the [global\\_variables](#page-71-0), [session\\_variables](#page-71-0), [global\\_status](#page-72-0), and [session\\_status](#page-72-0) tables. This occurs as necessary to permit the results for the SHOW VARIABLES and SHOW STATUS statements to be drawn from those tables, depending on the setting of the show\_compatibiliy\_56 system variable.

<span id="page-110-2"></span>• [performance\\_schema\\_accounts\\_size](#page-110-2)

| Command-Line Format | performance-schema-accounts-size=#                              |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_accounts_size                                |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The number of rows in the [accounts](#page-51-0) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [accounts](#page-51-0) table or status variable information in the [status\\_by\\_account](#page-92-0) table.

<span id="page-110-0"></span>• [performance\\_schema\\_digests\\_size](#page-110-0)

| Command-Line Format | performance-schema-digests-size=#                               |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_digests_size                                 |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of rows in the [events\\_statements\\_summary\\_by\\_digest](#page-78-0) table. If this maximum is exceeded such that a digest cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_digest\\_lost](#page-126-4) status variable.

For more information about statement digesting, see [Section 25.10, "Performance Schema](#page-2-0) [Statement Digests"](#page-2-0).

<span id="page-110-1"></span>• [performance\\_schema\\_events\\_stages\\_history\\_long\\_size](#page-110-1)

| Scope               | Global                                                  |  |
|---------------------|---------------------------------------------------------|--|
| System Variable     | performance_schema_events_stages_history_long_size      |  |
| Command-Line Format | performance-schema-events-stages<br>history-long-size=# |  |

| Dynamic       | No                                                              |
|---------------|-----------------------------------------------------------------|
| Type          | Integer                                                         |
| Default Value | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value | 1048576                                                         |

The number of rows in the [events\\_stages\\_history\\_long](#page-31-1) table.

<span id="page-111-0"></span>• [performance\\_schema\\_events\\_stages\\_history\\_size](#page-111-0)

| Command-Line Format | performance-schema-events-stages<br>history-size=#              |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_events_stages_history_size                   |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1024                                                            |

The number of rows per thread in the [events\\_stages\\_history](#page-31-0) table.

<span id="page-111-2"></span>• [performance\\_schema\\_events\\_statements\\_history\\_long\\_size](#page-111-2)

| Command-Line Format | performance-schema-events<br>statements-history-long-size=#     |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | performance_schema_events_statements_history_long_size          |  |
| Scope               | Global                                                          |  |
| Dynamic             | No                                                              |  |
| Type                | Integer                                                         |  |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value       | 1048576                                                         |  |
|                     |                                                                 |  |

The number of rows in the [events\\_statements\\_history\\_long](#page-39-1) table.

<span id="page-111-1"></span>• [performance\\_schema\\_events\\_statements\\_history\\_size](#page-111-1)

| Command-Line Format | performance-schema-events<br>statements-history-size=# |  |
|---------------------|--------------------------------------------------------|--|
| System Variable     | performance_schema_events_statements_history_size      |  |
| Scope               | Global                                                 |  |
| Dynamic             | No                                                     |  |
| Type                | Integer                                                |  |

| Default Value | -1 (signifies autosizing; do not assign this literal<br>value)  |
|---------------|-----------------------------------------------------------------|
| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value | 1024                                                            |

The number of rows per thread in the [events\\_statements\\_history](#page-39-0) table.

<span id="page-112-2"></span>• [performance\\_schema\\_events\\_transactions\\_history\\_long\\_size](#page-112-2)

| Command-Line Format | performance-schema-events<br>transactions-history-long-size=#   |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_events_transactions_history_long_size        |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |
|                     |                                                                 |

The number of rows in the [events\\_transactions\\_history\\_long](#page-49-1) table.

<span id="page-112-1"></span>• [performance\\_schema\\_events\\_transactions\\_history\\_size](#page-112-1)

| Command-Line Format | performance-schema-events<br>transactions-history-size=#        |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | performance_schema_events_transactions_history_size             |  |
| Scope               | Global                                                          |  |
| Dynamic             | No                                                              |  |
| Type                | Integer                                                         |  |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value       | 1024                                                            |  |
|                     |                                                                 |  |

The number of rows per thread in the [events\\_transactions\\_history](#page-49-0) table.

<span id="page-112-0"></span>• [performance\\_schema\\_events\\_waits\\_history\\_long\\_size](#page-112-0)

| Command-Line Format | performance-schema-events-waits<br>history-long-size=# |
|---------------------|--------------------------------------------------------|
| System Variable     | performance_schema_events_waits_history_long_size      |
| Scope               | Global                                                 |
| Dynamic             | No                                                     |
| Type                | Integer                                                |
| Default Value       | -1 (signifies autosizing; do not assign this literal   |
|                     | value)<br>4085                                         |

| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
|---------------|-----------------------------------------------------------------|
| Maximum Value | 1048576                                                         |

The number of rows in the [events\\_waits\\_history\\_long](#page-26-0) table.

<span id="page-113-0"></span>• [performance\\_schema\\_events\\_waits\\_history\\_size](#page-113-0)

| Command-Line Format | performance-schema-events-waits<br>history-size=#               |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | performance_schema_events_waits_history_size                    |  |
| Scope               | Global                                                          |  |
| Dynamic             | No                                                              |  |
| Type                | Integer                                                         |  |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value       | 1024                                                            |  |

The number of rows per thread in the [events\\_waits\\_history](#page-25-0) table.

<span id="page-113-1"></span>• [performance\\_schema\\_hosts\\_size](#page-113-1)

| Command-Line Format | performance-schema-hosts-size=#                                 |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_hosts_size                                   |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The number of rows in the [hosts](#page-52-0) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [hosts](#page-52-0) table or status variable information in the [status\\_by\\_host](#page-92-0) table.

<span id="page-113-2"></span>• [performance\\_schema\\_max\\_cond\\_classes](#page-113-2)

| Command-Line Format | performance-schema-max-cond<br>classes=# |
|---------------------|------------------------------------------|
| System Variable     | performance_schema_max_cond_classes      |
| Scope               | Global                                   |
| Dynamic             | No                                       |
| Type                | Integer                                  |
| Default Value       | 80                                       |
| Minimum Value       | 0                                        |
| Maximum Value       | 256                                      |

The maximum number of condition instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-114-1"></span>• [performance\\_schema\\_max\\_cond\\_instances](#page-114-1)

| Command-Line Format | performance-schema-max-cond<br>instances=#                      |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_cond_instances                           |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of instrumented condition objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-114-0"></span>• [performance\\_schema\\_max\\_digest\\_length](#page-114-0)

| Command-Line Format | performance-schema-max-digest<br>length=# |
|---------------------|-------------------------------------------|
| System Variable     | performance_schema_max_digest_length      |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Integer                                   |
| Default Value       | 1024                                      |
| Minimum Value       | 0                                         |
| Maximum Value       | 1048576                                   |
| Unit                | bytes                                     |

The maximum number of bytes of memory reserved per statement for computation of normalized statement digest values in the Performance Schema. This variable is related to max\_digest\_length; see the description of that variable in Section 5.1.7, "Server System Variables".

For more information about statement digesting, including considerations regarding memory use, see [Section 25.10, "Performance Schema Statement Digests".](#page-2-0)

<span id="page-114-2"></span>• [performance\\_schema\\_max\\_file\\_classes](#page-114-2)

| Command-Line Format | performance-schema-max-file<br>classes=# |
|---------------------|------------------------------------------|
| System Variable     | performance_schema_max_file_classes      |
| Scope               | Global                                   |
| Dynamic             | No                                       |
| Type                | Integer                                  |
| Default Value       | 80                                       |

#### Performance Schema System Variables

| Minimum Value | 0   |
|---------------|-----|
| Maximum Value | 256 |

The maximum number of file instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-115-0"></span>• [performance\\_schema\\_max\\_file\\_handles](#page-115-0)

| Command-Line Format | performance-schema-max-file<br>handles=# |
|---------------------|------------------------------------------|
| System Variable     | performance_schema_max_file_handles      |
| Scope               | Global                                   |
| Dynamic             | No                                       |
| Type                | Integer                                  |
| Default Value       | 32768                                    |
| Minimum Value       | 0                                        |
| Maximum Value       | 1048576                                  |

The maximum number of opened file objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

The value of [performance\\_schema\\_max\\_file\\_handles](#page-115-0) should be greater than the value of open\_files\_limit: open\_files\_limit affects the maximum number of open file handles the server can support and [performance\\_schema\\_max\\_file\\_handles](#page-115-0) affects how many of these file handles can be instrumented.

<span id="page-115-1"></span>• [performance\\_schema\\_max\\_file\\_instances](#page-115-1)

| Command-Line Format | performance-schema-max-file<br>instances=#                      |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_file_instances                           |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of instrumented file objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

• [performance\\_schema\\_max\\_index\\_stat](#page-115-2)

<span id="page-115-2"></span>

|      | Command-Line Format | performance-schema-max-index<br>stat=# |
|------|---------------------|----------------------------------------|
|      | System Variable     | performance_schema_max_index_stat      |
|      | Scope               | Global                                 |
|      | Dynamic             | No                                     |
| 4088 | Type                | Integer                                |

| Default Value | -1 (signifies autosizing; do not assign this literal<br>value)  |
|---------------|-----------------------------------------------------------------|
| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value | 1048576                                                         |

The maximum number of indexes for which the Performance Schema maintains statistics. If this maximum is exceeded such that index statistics are lost, the Performance Schema increments the [Performance\\_schema\\_index\\_stat\\_lost](#page-126-13) status variable. The default value is autosized using the value of [performance\\_schema\\_max\\_table\\_instances](#page-121-1).

<span id="page-116-1"></span>• [performance\\_schema\\_max\\_memory\\_classes](#page-116-1)

| Command-Line Format | performance-schema-max-memory<br>classes=# |
|---------------------|--------------------------------------------|
| System Variable     | performance_schema_max_memory_classes      |
| Scope               | Global                                     |
| Dynamic             | No                                         |
| Type                | Integer                                    |
| Default Value       | 320                                        |
| Minimum Value       | 0                                          |
| Maximum Value       | 1024                                       |

The maximum number of memory instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-116-0"></span>• [performance\\_schema\\_max\\_metadata\\_locks](#page-116-0)

| Command-Line Format | performance-schema-max-metadata<br>locks=#                      |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_metadata_locks                           |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 10485760                                                        |

The maximum number of metadata lock instruments. This value controls the size of the [metadata\\_locks](#page-67-0) table. If this maximum is exceeded such that a metadata lock cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_metadata\\_lock\\_lost](#page-126-11) status variable.

<span id="page-116-2"></span>• [performance\\_schema\\_max\\_mutex\\_classes](#page-116-2)

| Command-Line Format | performance-schema-max-mutex<br>classes=# |
|---------------------|-------------------------------------------|
| System Variable     | performance_schema_max_mutex_classes      |
| Scope               | Global<br>4089                            |

#### Performance Schema System Variables

| Dynamic       | No      |
|---------------|---------|
| Type          | Integer |
| Default Value | 200     |
| Minimum Value | 0       |
| Maximum Value | 256     |

The maximum number of mutex instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-117-0"></span>• [performance\\_schema\\_max\\_mutex\\_instances](#page-117-0)

| Command-Line Format | performance-schema-max-mutex<br>instances=#                     |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_mutex_instances                          |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 104857600                                                       |

The maximum number of instrumented mutex objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-117-1"></span>• [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-117-1)

| Command-Line Format | performance-schema-max-prepared<br>statements-instances=#       |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | performance_schema_max_prepared_statements_instances            |  |
| Scope               | Global                                                          |  |
| Dynamic             | No                                                              |  |
| Type                | Integer                                                         |  |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value       | 4194304                                                         |  |
|                     |                                                                 |  |

The maximum number of rows in the [prepared\\_statements\\_instances](#page-40-0) table. If this maximum is exceeded such that a prepared statement cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_prepared\\_statements\\_lost](#page-126-2) status variable. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

The default value of this variable is autosized based on the value of the max\_prepared\_stmt\_count system variable.

<span id="page-118-1"></span>• [performance\\_schema\\_max\\_rwlock\\_classes](#page-118-1)

| Command-Line Format | performance-schema-max-rwlock<br>classes=# |
|---------------------|--------------------------------------------|
| System Variable     | performance_schema_max_rwlock_classes      |
| Scope               | Global                                     |
| Dynamic             | No                                         |
| Type                | Integer                                    |
| Default Value       | 50                                         |
| Minimum Value       | 0                                          |
| Maximum Value       | 256                                        |

The maximum number of rwlock instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-118-0"></span>• [performance\\_schema\\_max\\_program\\_instances](#page-118-0)

| Command-Line Format | performance-schema-max-program<br>instances=#                   |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_program_instances                        |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of stored programs for which the Performance Schema maintains statistics. If this maximum is exceeded, the Performance Schema increments the [Performance\\_schema\\_program\\_lost](#page-127-1) status variable. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-118-2"></span>• [performance\\_schema\\_max\\_rwlock\\_instances](#page-118-2)

| Command-Line Format | performance-schema-max-rwlock<br>instances=#                   |
|---------------------|----------------------------------------------------------------|
| System Variable     | performance_schema_max_rwlock_instances                        |
| Scope               | Global                                                         |
| Dynamic             | No                                                             |
| Type                | Integer                                                        |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autosizing; do not assign this literal<br>value) |
| Maximum Value       | 104857600                                                      |

The maximum number of instrumented rwlock objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring". 4091 <span id="page-119-1"></span>• [performance\\_schema\\_max\\_socket\\_classes](#page-119-1)

| Command-Line Format | performance-schema-max-socket<br>classes=# |
|---------------------|--------------------------------------------|
| System Variable     | performance_schema_max_socket_classes      |
| Scope               | Global                                     |
| Dynamic             | No                                         |
| Type                | Integer                                    |
| Default Value       | 10                                         |
| Minimum Value       | 0                                          |
| Maximum Value       | 256                                        |

The maximum number of socket instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-119-2"></span>• [performance\\_schema\\_max\\_socket\\_instances](#page-119-2)

| Command-Line Format | performance-schema-max-socket<br>instances=#                    |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_socket_instances                         |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of instrumented socket objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-119-0"></span>• [performance\\_schema\\_max\\_sql\\_text\\_length](#page-119-0)

| Command-Line Format | performance-schema-max-sql-text<br>length=# |
|---------------------|---------------------------------------------|
| System Variable     | performance_schema_max_sql_text_length      |
| Scope               | Global                                      |
| Dynamic             | No                                          |
| Type                | Integer                                     |
| Default Value       | 1024                                        |
| Minimum Value       | 0                                           |
| Maximum Value       | 1048576                                     |
| Unit                | bytes                                       |

The maximum number of bytes used to store SQL statements in the SQL\_TEXT column of the [events\\_statements\\_current](#page-36-0), [events\\_statements\\_history](#page-39-0), and [events\\_statements\\_history\\_long](#page-39-1) statement event tables. Any bytes in excess of [performance\\_schema\\_max\\_sql\\_text\\_length](#page-119-0) are discarded and do not appear in the SQL\_TEXT column. Statements differing only after that many initial bytes are indistinguishable in this column.

Decreasing the [performance\\_schema\\_max\\_sql\\_text\\_length](#page-119-0) value reduces memory use but causes more statements to become indistinguishable if they differ only at the end. Increasing the value increases memory use but permits longer statements to be distinguished.

<span id="page-120-0"></span>• [performance\\_schema\\_max\\_stage\\_classes](#page-120-0)

| Command-Line Format | performance-schema-max-stage<br>classes=# |
|---------------------|-------------------------------------------|
| System Variable     | performance_schema_max_stage_classes      |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Integer                                   |
| Default Value       | 150                                       |
| Minimum Value       | 0                                         |
| Maximum Value       | 256                                       |

The maximum number of stage instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-120-1"></span>• [performance\\_schema\\_max\\_statement\\_classes](#page-120-1)

| Command-Line Format | performance-schema-max-statement<br>classes=# |
|---------------------|-----------------------------------------------|
| System Variable     | performance_schema_max_statement_classes      |
| Scope               | Global                                        |
| Dynamic             | No                                            |
| Type                | Integer                                       |
| Minimum Value       | 0                                             |
| Maximum Value       | 256                                           |

The maximum number of statement instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

The default value is calculated at server build time based on the number of commands in the client/ server protocol and the number of SQL statement types supported by the server.

This variable should not be changed, unless to set it to 0 to disable all statement instrumentation and save all memory associated with it. Setting the variable to nonzero values other than the default has no benefit; in particular, values larger than the default cause more memory to be allocated then is needed.

<span id="page-120-2"></span>• [performance\\_schema\\_max\\_statement\\_stack](#page-120-2)

| Command-Line Format | performance-schema-max-statement<br>stack=# |
|---------------------|---------------------------------------------|
| System Variable     | performance_schema_max_statement_stack      |
| Scope               | Global                                      |
| Dynamic             | No                                          |
| Type                | Integer<br>4093                             |

#### Performance Schema System Variables

| Default Value | 10  |
|---------------|-----|
| Minimum Value | 1   |
| Maximum Value | 256 |

The maximum depth of nested stored program calls for which the Performance Schema maintains statistics. When this maximum is exceeded, the Performance Schema increments the [Performance\\_schema\\_nested\\_statement\\_lost](#page-126-12) status variable for each stored program statement executed.

<span id="page-121-0"></span>• [performance\\_schema\\_max\\_table\\_handles](#page-121-0)

| Command-Line Format | performance-schema-max-table<br>handles=#                       |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_table_handles                            |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of opened table objects. This value controls the size of the [table\\_handles](#page-70-0) table. If this maximum is exceeded such that a table handle cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_table\\_handles\\_lost](#page-127-8) status variable. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-121-1"></span>• [performance\\_schema\\_max\\_table\\_instances](#page-121-1)

| Command-Line Format | performance-schema-max-table<br>instances=#                     |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_table_instances                          |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of instrumented table objects. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-121-2"></span>• [performance\\_schema\\_max\\_table\\_lock\\_stat](#page-121-2)

| Command-Line Format | performance-schema-max-table-lock<br>stat=# |
|---------------------|---------------------------------------------|
| System Variable     | performance_schema_max_table_lock_stat      |

| Scope         | Global                                                          |
|---------------|-----------------------------------------------------------------|
| Dynamic       | No                                                              |
| Type          | Integer                                                         |
| Default Value | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value | 1048576                                                         |

The maximum number of tables for which the Performance Schema maintains lock statistics. If this maximum is exceeded such that table lock statistics are lost, the Performance Schema increments the [Performance\\_schema\\_table\\_lock\\_stat\\_lost](#page-127-11) status variable.

<span id="page-122-1"></span>• [performance\\_schema\\_max\\_thread\\_classes](#page-122-1)

| Command-Line Format | performance-schema-max-thread<br>classes=# |
|---------------------|--------------------------------------------|
| System Variable     | performance_schema_max_thread_classes      |
| Scope               | Global                                     |
| Dynamic             | No                                         |
| Type                | Integer                                    |
| Default Value       | 50                                         |
| Minimum Value       | 0                                          |
| Maximum Value       | 256                                        |

The maximum number of thread instruments. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

<span id="page-122-0"></span>• [performance\\_schema\\_max\\_thread\\_instances](#page-122-0)

| Command-Line Format | performance-schema-max-thread<br>instances=#                    |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_max_thread_instances                         |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The maximum number of instrumented thread objects. The value controls the size of the [threads](#page-100-0) table. If this maximum is exceeded such that a thread cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_thread\\_instances\\_lost](#page-128-0) status variable. For information about how to set and use this variable, see Section 25.7, "Performance Schema Status Monitoring".

The max\_connections system variable affects how many threads can run in the server. [performance\\_schema\\_max\\_thread\\_instances](#page-122-0) affects how many of these running threads can be instrumented.

The [variables\\_by\\_thread](#page-71-0) and [status\\_by\\_thread](#page-72-0) tables contain system and status variable information only about foreground threads. If not all threads are instrumented by the Performance Schema, this table may miss some rows. In this case, the [Performance\\_schema\\_thread\\_instances\\_lost](#page-128-0) status variable is greater than zero.

<span id="page-123-1"></span>• [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1)

| Command-Line Format | performance-schema-session<br>connect-attrs-size=#             |  |
|---------------------|----------------------------------------------------------------|--|
| System Variable     | performance_schema_session_connect_attrs_size                  |  |
| Scope               | Global                                                         |  |
| Dynamic             | No                                                             |  |
| Type                | Integer                                                        |  |
| Default Value       | -1 (signifies autosizing; do not assign this literal<br>value) |  |
| Minimum Value       | -1 (signifies autosizing; do not assign this literal<br>value) |  |
| Maximum Value       | 1048576                                                        |  |
| Unit                | bytes                                                          |  |

The amount of preallocated memory per thread reserved to hold connection attribute keyvalue pairs. If the aggregate size of connection attribute data sent by a client is larger than this amount, the Performance Schema truncates the attribute data, increments the [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-127-0) status variable, and writes a message to the error log indicating that truncation occurred if the log\_error\_verbosity system variable value is greater than 1.

The default value of [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) is autosized at server startup. This value may be small, so if truncation occurs ([Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-127-0) becomes nonzero), you may wish to set [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) explicitly to a larger value.

Although the maximum permitted [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) value is 1MB, the effective maximum is 64KB because the server imposes a limit of 64KB on the aggregate size of connection attribute data it can accept. If a client attempts to send more than 64KB of attribute data, the server rejects the connection. For more information, see [Section 25.12.9,](#page-53-1) ["Performance Schema Connection Attribute Tables".](#page-53-1)

<span id="page-123-0"></span>• [performance\\_schema\\_setup\\_actors\\_size](#page-123-0)

| Command-Line Format | performance-schema-setup-actors<br>size=# |
|---------------------|-------------------------------------------|
| System Variable     | performance_schema_setup_actors_size      |
| Scope               | Global                                    |
| Dynamic             | No                                        |
| Type                | Integer                                   |

| Default Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
|---------------|-----------------------------------------------------------------|
| Minimum Value | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Maximum Value | 1048576                                                         |

The number of rows in the [setup\\_actors](#page-11-0) table.

<span id="page-124-0"></span>• [performance\\_schema\\_setup\\_objects\\_size](#page-124-0)

| Command-Line Format | performance-schema-setup-objects<br>size=#                      |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | performance_schema_setup_objects_size                           |  |
| Scope               | Global                                                          |  |
| Dynamic             | No                                                              |  |
| Type                | Integer                                                         |  |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value       | 1048576                                                         |  |

The number of rows in the [setup\\_objects](#page-14-0) table.

<span id="page-124-1"></span>• [performance\\_schema\\_show\\_processlist](#page-124-1)

| Command-Line Format | performance-schema-show<br>processlist[={OFF ON}] |
|---------------------|---------------------------------------------------|
| System Variable     | performance_schema_show_processlist               |
| Scope               | Global                                            |
| Dynamic             | Yes                                               |
| Type                | Boolean                                           |
| Default Value       | OFF                                               |

The SHOW PROCESSLIST statement provides process information by collecting thread data from all active threads. The [performance\\_schema\\_show\\_processlist](#page-124-1) variable determines which SHOW PROCESSLIST implementation to use:

- The default implementation iterates across active threads from within the thread manager while holding a global mutex. This has negative performance consequences, particularly on busy systems.
- The alternative SHOW PROCESSLIST implementation is based on the Performance Schema [processlist](#page-97-0) table. This implementation queries active thread data from the Performance Schema rather than the thread manager and does not require a mutex.

To enable the alternative implementation, enable the [performance\\_schema\\_show\\_processlist](#page-124-1) system variable. To ensure that the default and alternative implementations yield the same information, certain configuration requirements must be met; see [Section 25.12.16.3, "The](#page-97-0) [processlist Table"](#page-97-0).

<span id="page-125-0"></span>• [performance\\_schema\\_users\\_size](#page-125-0)

| Command-Line Format | performance-schema-users-size=#                                 |
|---------------------|-----------------------------------------------------------------|
| System Variable     | performance_schema_users_size                                   |
| Scope               | Global                                                          |
| Dynamic             | No                                                              |
| Type                | Integer                                                         |
| Default Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value       | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value       | 1048576                                                         |

The number of rows in the [users](#page-52-1) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [users](#page-52-1) table or status variable information in the [status\\_by\\_user](#page-92-0) table.