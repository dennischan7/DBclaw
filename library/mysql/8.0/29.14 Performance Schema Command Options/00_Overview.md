---
source: MySQL 8.0 Reference
title: 00_Overview
---

Performance Schema parameters can be specified at server startup on the command line or in option files to configure Performance Schema instruments and consumers. Runtime configuration is also possible in many cases (see Section 29.4, "Performance Schema Runtime Configuration"), but startup configuration must be used when runtime configuration is too late to affect instruments that have already been initialized during the startup process.

Performance Schema consumers and instruments can be configured at startup using the following syntax. For additional details, see Section 29.3, "Performance Schema Startup Configuration".

<span id="page-110-10"></span>• [--performance-schema-consumer-](#page-110-10)consumer\_name=value

Configure a Performance Schema consumer. Consumer names in the setup\_consumers table use underscores, but for consumers set at startup, dashes and underscores within the name are equivalent. Options for configuring individual consumers are detailed later in this section.

<span id="page-110-9"></span>• [--performance-schema-instrument=](#page-110-9)instrument\_name=value

Configure a Performance Schema instrument. The name may be given as a pattern to configure instruments that match the pattern.

The following items configure individual consumers:

- <span id="page-110-0"></span>• [--performance-schema-consumer-events-stages-current=value](#page-110-0)
  - Configure the events-stages-current consumer.
- <span id="page-110-1"></span>• [--performance-schema-consumer-events-stages-history=value](#page-110-1)

Configure the events-stages-history consumer.

- <span id="page-110-2"></span>• [--performance-schema-consumer-events-stages-history-long=value](#page-110-2)
  - Configure the events-stages-history-long consumer.
- <span id="page-110-3"></span>• [--performance-schema-consumer-events-statements-cpu=value](#page-110-3)

Configure the events-statements-cpu consumer.

<span id="page-110-4"></span>• [--performance-schema-consumer-events-statements-current=value](#page-110-4)

Configure the events-statements-current consumer.

<span id="page-110-5"></span>• [--performance-schema-consumer-events-statements-history=value](#page-110-5)

Configure the events-statements-history consumer.

- <span id="page-110-6"></span>• [--performance-schema-consumer-events-statements-history-long=value](#page-110-6)
  - Configure the events-statements-history-long consumer.
- <span id="page-110-7"></span>• [--performance-schema-consumer-events-transactions-current=value](#page-110-7)

Configure the Performance Schema events-transactions-current consumer.

<span id="page-110-8"></span>• [--performance-schema-consumer-events-transactions-history=value](#page-110-8)

Configure the Performance Schema events-transactions-history consumer.

<span id="page-111-0"></span>• [--performance-schema-consumer-events-transactions-history-long=value](#page-111-0)

Configure the Performance Schema events-transactions-history-long consumer.

<span id="page-111-1"></span>• [--performance-schema-consumer-events-waits-current=value](#page-111-1)

Configure the events-waits-current consumer.

<span id="page-111-2"></span>• [--performance-schema-consumer-events-waits-history=value](#page-111-2)

Configure the events-waits-history consumer.

<span id="page-111-3"></span>• [--performance-schema-consumer-events-waits-history-long=value](#page-111-3)

Configure the events-waits-history-long consumer.

<span id="page-111-4"></span>• [--performance-schema-consumer-global-instrumentation=value](#page-111-4)

Configure the global-instrumentation consumer.

<span id="page-111-5"></span>• [--performance-schema-consumer-statements-digest=value](#page-111-5)

Configure the statements-digest consumer.

• [--performance-schema-consumer-thread-instrumentation=value](#page-111-6)

Configure the thread-instrumentation consumer.

# <span id="page-111-6"></span>**29.15 Performance Schema System Variables**

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
| performance_schema_max_mutex_classes | 350 |
| performance_schema_max_mutex_instances | -1 |
| performance_schema_max_prepared_statements_instances | -1 |
| performance_schema_max_program_instances | -1 |
| performance_schema_max_rwlock_classes | 40 |
| performance_schema_max_rwlock_instances | -1 |
| performance_schema_max_socket_classes | 10 |
| performance_schema_max_socket_instances | -1 |
| performance_schema_max_sql_text_length | 1024 |
| performance_schema_max_stage_classes | 150 |
```

```
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

Performance Schema system variables can be set at server startup on the command line or in option files, and many can be set at runtime. See [Section 29.13, "Performance Schema Option and Variable](#page-106-0) [Reference"](#page-106-0).

The Performance Schema automatically sizes the values of several of its parameters at server startup if they are not set explicitly. For more information, see Section 29.3, "Performance Schema Startup Configuration".

Performance Schema system variables have the following meanings:

<span id="page-112-1"></span>• [performance\\_schema](#page-112-1)

| Command-Line Format  | performance-schema[={OFF ON}] |
|----------------------|-------------------------------|
| System Variable      | performance_schema            |
| Scope                | Global                        |
| Dynamic              | No                            |
| SET_VAR Hint Applies | No                            |
| Type                 | Boolean                       |
| Default Value        | ON                            |

The value of this variable is ON or OFF to indicate whether the Performance Schema is enabled. By default, the value is ON. At server startup, you can specify this variable with no value or a value of ON or 1 to enable it, or with a value of OFF or 0 to disable it.

Even when the Performance Schema is disabled, it continues to populate the [global\\_variables](#page-42-0), [session\\_variables](#page-42-0), [global\\_status](#page-47-0), and [session\\_status](#page-47-0) tables. This occurs as necessary to permit the results for the SHOW VARIABLES and SHOW STATUS statements to be drawn from those tables. The Performance Schema also populates some of the replication tables when disabled.

<span id="page-112-0"></span>• [performance\\_schema\\_accounts\\_size](#page-112-0)

| Command-Line Format  | performance-schema-accounts-size=#                              |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_accounts_size                                |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The number of rows in the [accounts](#page-0-0) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [accounts](#page-0-0) table or status variable information in the [status\\_by\\_account](#page-86-0) table.

<span id="page-113-0"></span>• [performance\\_schema\\_digests\\_size](#page-113-0)

| Command-Line Format  | performance-schema-digests-size=#                               |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_digests_size                                 |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of rows in the [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table. If this maximum is exceeded such that a digest cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_digest\\_lost](#page-130-3) status variable.

For more information about statement digesting, see Section 29.10, "Performance Schema Statement Digests and Sampling".

<span id="page-113-2"></span>• [performance\\_schema\\_error\\_size](#page-113-2)

| Command-Line Format  | performance-schema-error-size=# |
|----------------------|---------------------------------|
| System Variable      | performance_schema_error_size   |
| Scope                | Global                          |
| Dynamic              | No                              |
| SET_VAR Hint Applies | No                              |
| Type                 | Integer                         |
| Default Value        | number of server error codes    |
| Minimum Value        | 0                               |
| Maximum Value        | 1048576                         |

The number of instrumented server error codes. The default value is the actual number of server error codes. Although the value can be set anywhere from 0 to its maximum, the intended use is to set it to either its default (to instrument all errors) or 0 (to instrument no errors).

Error information is aggregated in summary tables; see [Section 29.12.20.11, "Error Summary](#page-84-0) [Tables"](#page-84-0). If an error occurs that is not instrumented, information for the occurrence is aggregated to the NULL row in each summary table; that is, to the row with ERROR\_NUMBER=0, ERROR\_NAME=NULL, and SQLSTATE=NULL.

<span id="page-113-1"></span>• [performance\\_schema\\_events\\_stages\\_history\\_long\\_size](#page-113-1)

| Command-Line Format | performance-schema-events-stages<br>history-long-size=# |
|---------------------|---------------------------------------------------------|
| System Variable     | performance_schema_events_stages_history_long_size      |

| Scope                | Global                                                          |
|----------------------|-----------------------------------------------------------------|
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The number of rows in the events\_stages\_history\_long table.

<span id="page-114-0"></span>• [performance\\_schema\\_events\\_stages\\_history\\_size](#page-114-0)

| Command-Line Format  | performance-schema-events-stages<br>history-size=#              |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_events_stages_history_size                   |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1024                                                            |

The number of rows per thread in the events\_stages\_history table.

<span id="page-114-1"></span>• [performance\\_schema\\_events\\_statements\\_history\\_long\\_size](#page-114-1)

| Command-Line Format  | performance-schema-events<br>statements-history-long-size=#     |  |
|----------------------|-----------------------------------------------------------------|--|
| System Variable      | performance_schema_events_statements_history_long_size          |  |
| Scope                | Global                                                          |  |
| Dynamic              | No                                                              |  |
| SET_VAR Hint Applies | No                                                              |  |
| Type                 | Integer                                                         |  |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value        | 1048576                                                         |  |

The number of rows in the events\_statements\_history\_long table.

<span id="page-114-2"></span>• [performance\\_schema\\_events\\_statements\\_history\\_size](#page-114-2)

| Command-Line Format | performance-schema-events |
|---------------------|---------------------------|
|                     | statements-history-size=# |

| System Variable      | performance_schema_events_statements_history_size               |
|----------------------|-----------------------------------------------------------------|
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1024                                                            |

The number of rows per thread in the events\_statements\_history table.

<span id="page-115-0"></span>• [performance\\_schema\\_events\\_transactions\\_history\\_long\\_size](#page-115-0)

| Command-Line Format  | performance-schema-events<br>transactions-history-long-size=#   |  |
|----------------------|-----------------------------------------------------------------|--|
| System Variable      | performance_schema_events_transactions_history_long_size        |  |
| Scope                | Global                                                          |  |
| Dynamic              | No                                                              |  |
| SET_VAR Hint Applies | No                                                              |  |
| Type                 | Integer                                                         |  |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value        | 1048576                                                         |  |
|                      |                                                                 |  |

The number of rows in the events\_transactions\_history\_long table.

<span id="page-115-1"></span>• [performance\\_schema\\_events\\_transactions\\_history\\_size](#page-115-1)

| Command-Line Format  | performance-schema-events<br>transactions-history-size=#        |  |
|----------------------|-----------------------------------------------------------------|--|
| System Variable      | performance_schema_events_transactions_history_size             |  |
| Scope                | Global                                                          |  |
| Dynamic              | No                                                              |  |
| SET_VAR Hint Applies | No                                                              |  |
| Type                 | Integer                                                         |  |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Maximum Value        | 1024                                                            |  |
|                      |                                                                 |  |

The number of rows per thread in the events\_transactions\_history table.

<span id="page-116-1"></span>• [performance\\_schema\\_events\\_waits\\_history\\_long\\_size](#page-116-1)

| Command-Line Format  | performance-schema-events-waits<br>history-long-size=#          |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_events_waits_history_long_size               |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The number of rows in the events\_waits\_history\_long table.

<span id="page-116-2"></span>• [performance\\_schema\\_events\\_waits\\_history\\_size](#page-116-2)

| Command-Line Format  | performance-schema-events-waits<br>history-size=#               |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_events_waits_history_size                    |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1024                                                            |

The number of rows per thread in the events\_waits\_history table.

<span id="page-116-0"></span>• [performance\\_schema\\_hosts\\_size](#page-116-0)

| Command-Line Format  | performance-schema-hosts-size=#                                 |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_hosts_size                                   |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |

| Maximum Value | 1048576 |
|---------------|---------|
|               |         |

The number of rows in the [hosts](#page-1-0) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [hosts](#page-1-0) table or status variable information in the [status\\_by\\_host](#page-86-0) table.

<span id="page-117-0"></span>• [performance\\_schema\\_max\\_cond\\_classes](#page-117-0)

| Command-Line Format  | performance-schema-max-cond<br>classes=# |
|----------------------|------------------------------------------|
| System Variable      | performance_schema_max_cond_classes      |
| Scope                | Global                                   |
| Dynamic              | No                                       |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Default Value        | 150                                      |
| Minimum Value        | 0                                        |
| Maximum Value        | 1024                                     |

The maximum number of condition instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-117-1"></span>• [performance\\_schema\\_max\\_cond\\_instances](#page-117-1)

| Command-Line Format  | performance-schema-max-cond<br>instances=#                      |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_cond_instances                           |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of instrumented condition objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-117-2"></span>• [performance\\_schema\\_max\\_digest\\_length](#page-117-2)

| Command-Line Format  | performance-schema-max-digest<br>length=# |
|----------------------|-------------------------------------------|
| System Variable      | performance_schema_max_digest_length      |
| Scope                | Global                                    |
| Dynamic              | No                                        |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 1024                                      |

| Minimum Value | 0       |
|---------------|---------|
| Maximum Value | 1048576 |
| Unit          | bytes   |

The maximum number of bytes of memory reserved per statement for computation of normalized statement digest values in the Performance Schema. This variable is related to max\_digest\_length; see the description of that variable in Section 7.1.8, "Server System Variables".

For more information about statement digesting, including considerations regarding memory use, see Section 29.10, "Performance Schema Statement Digests and Sampling".

<span id="page-118-1"></span>• [performance\\_schema\\_max\\_digest\\_sample\\_age](#page-118-1)

| Command-Line Format  | performance-schema-max-digest<br>sample-age=# |
|----------------------|-----------------------------------------------|
| System Variable      | performance_schema_max_digest_sample_age      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 60                                            |
| Minimum Value        | 0                                             |
| Maximum Value        | 1048576                                       |
| Unit                 | seconds                                       |

This variable affects statement sampling for the [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table. When a new table row is inserted, the statement that produced the row digest value is stored as the current sample statement associated with the digest. Thereafter, when the server sees other statements with the same digest value, it determines whether to use the new statement to replace the current sample statement (that is, whether to resample). Resampling policy is based on the comparative wait times of the current sample statement and new statement and, optionally, the age of the current sample statement:

- Resampling based on wait times: If the new statement wait time has a wait time greater than that of the current sample statement, it becomes the current sample statement.
- Resampling based on age: If the [performance\\_schema\\_max\\_digest\\_sample\\_age](#page-118-1) system variable has a value greater than zero and the current sample statement is more than that many seconds old, the current statement is considered "too old" and the new statement replaces it. This occurs even if the new statement wait time is less than that of the current sample statement.

For information about statement sampling, see Section 29.10, "Performance Schema Statement Digests and Sampling".

<span id="page-118-0"></span>• [performance\\_schema\\_max\\_file\\_classes](#page-118-0)

| Command-Line Format  | performance-schema-max-file<br>classes=# |
|----------------------|------------------------------------------|
| System Variable      | performance_schema_max_file_classes      |
| Scope                | Global                                   |
| Dynamic              | No                                       |
| SET_VAR Hint Applies | No                                       |

### Performance Schema System Variables

| Type          | Integer |
|---------------|---------|
| Default Value | 80      |
| Minimum Value | 0       |
| Maximum Value | 1024    |

The maximum number of file instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-119-0"></span>• [performance\\_schema\\_max\\_file\\_handles](#page-119-0)

| Command-Line Format  | performance-schema-max-file<br>handles=# |
|----------------------|------------------------------------------|
| System Variable      | performance_schema_max_file_handles      |
| Scope                | Global                                   |
| Dynamic              | No                                       |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Default Value        | 32768                                    |
| Minimum Value        | 0                                        |
| Maximum Value        | 1048576                                  |

The maximum number of opened file objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

The value of [performance\\_schema\\_max\\_file\\_handles](#page-119-0) should be greater than the value of open\_files\_limit: open\_files\_limit affects the maximum number of open file handles the server can support and [performance\\_schema\\_max\\_file\\_handles](#page-119-0) affects how many of these file handles can be instrumented.

<span id="page-119-1"></span>• [performance\\_schema\\_max\\_file\\_instances](#page-119-1)

| Command-Line Format  | performance-schema-max-file<br>instances=#                      |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_file_instances                           |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of instrumented file objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

• [performance\\_schema\\_max\\_index\\_stat](#page-119-2)

<span id="page-119-2"></span>

|      | Command-Line Format | performance-schema-max-index |
|------|---------------------|------------------------------|
| 5290 |                     | stat=#                       |

| System Variable      | performance_schema_max_index_stat                               |
|----------------------|-----------------------------------------------------------------|
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of indexes for which the Performance Schema maintains statistics. If this maximum is exceeded such that index statistics are lost, the Performance Schema increments the [Performance\\_schema\\_index\\_stat\\_lost](#page-131-12) status variable. The default value is autosized using the value of [performance\\_schema\\_max\\_table\\_instances](#page-126-1).

<span id="page-120-1"></span>• [performance\\_schema\\_max\\_memory\\_classes](#page-120-1)

| Command-Line Format  | performance-schema-max-memory<br>classes=# |
|----------------------|--------------------------------------------|
| System Variable      | performance_schema_max_memory_classes      |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 450                                        |
| Minimum Value        | 0                                          |
| Maximum Value        | 1024                                       |

The maximum number of memory instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-120-0"></span>• [performance\\_schema\\_max\\_metadata\\_locks](#page-120-0)

| Command-Line Format  | performance-schema-max-metadata<br>locks=#                      |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_metadata_locks                           |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 10485760                                                        |

The maximum number of metadata lock instruments. This value controls the size of the [metadata\\_locks](#page-39-0) table. If this maximum is exceeded such that a metadata lock cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_metadata\\_lock\\_lost](#page-131-4) status variable.

<span id="page-121-0"></span>• [performance\\_schema\\_max\\_mutex\\_classes](#page-121-0)

| Command-Line Format  | performance-schema-max-mutex<br>classes=# |
|----------------------|-------------------------------------------|
| System Variable      | performance_schema_max_mutex_classes      |
| Scope                | Global                                    |
| Dynamic              | No                                        |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 350                                       |
| Minimum Value        | 0                                         |
| Maximum Value        | 1024                                      |

The maximum number of mutex instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-121-1"></span>• [performance\\_schema\\_max\\_mutex\\_instances](#page-121-1)

| Command-Line Format  | performance-schema-max-mutex<br>instances=#                     |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_mutex_instances                          |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 104857600                                                       |

The maximum number of instrumented mutex objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-121-2"></span>• [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-121-2)

| Command-Line Format  | performance-schema-max-prepared<br>statements-instances=#       |  |
|----------------------|-----------------------------------------------------------------|--|
| System Variable      | performance_schema_max_prepared_statements_instances            |  |
| Scope                | Global                                                          |  |
| Dynamic              | No                                                              |  |
| SET_VAR Hint Applies | No                                                              |  |
| Type                 | Integer                                                         |  |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |  |

| Maximum Value | 4194304 |
|---------------|---------|
|---------------|---------|

The maximum number of rows in the prepared\_statements\_instances table. If this maximum is exceeded such that a prepared statement cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_prepared\\_statements\\_lost](#page-131-8) status variable. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

The default value of this variable is autosized based on the value of the max\_prepared\_stmt\_count system variable.

<span id="page-122-1"></span>• [performance\\_schema\\_max\\_rwlock\\_classes](#page-122-1)

| Command-Line Format  | performance-schema-max-rwlock<br>classes=# |
|----------------------|--------------------------------------------|
| System Variable      | performance_schema_max_rwlock_classes      |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 100                                        |
| Minimum Value        | 0                                          |
| Maximum Value        | 1024                                       |

The maximum number of rwlock instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-122-0"></span>• [performance\\_schema\\_max\\_program\\_instances](#page-122-0)

| Command-Line Format  | performance-schema-max-program<br>instances=#                   |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_program_instances                        |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of stored programs for which the Performance Schema maintains statistics. If this maximum is exceeded, the Performance Schema increments the [Performance\\_schema\\_program\\_lost](#page-131-9) status variable. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-122-2"></span>• [performance\\_schema\\_max\\_rwlock\\_instances](#page-122-2)

| Command-Line Format | performance-schema-max-rwlock<br>instances=# |
|---------------------|----------------------------------------------|
| System Variable     | performance_schema_max_rwlock_instances      |

| Scope                | Global                                                         |
|----------------------|----------------------------------------------------------------|
| Dynamic              | No                                                             |
| SET_VAR Hint Applies | No                                                             |
| Type                 | Integer                                                        |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autosizing; do not assign this literal<br>value) |
| Maximum Value        | 104857600                                                      |

The maximum number of instrumented rwlock objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-123-0"></span>• [performance\\_schema\\_max\\_socket\\_classes](#page-123-0)

| Command-Line Format  | performance-schema-max-socket<br>classes=# |
|----------------------|--------------------------------------------|
| System Variable      | performance_schema_max_socket_classes      |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 10                                         |
| Minimum Value        | 0                                          |
| Maximum Value        | 1024                                       |

The maximum number of socket instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-123-1"></span>• [performance\\_schema\\_max\\_socket\\_instances](#page-123-1)

| Command-Line Format  | performance-schema-max-socket<br>instances=#                    |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_socket_instances                         |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of instrumented socket objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-124-0"></span>• [performance\\_schema\\_max\\_sql\\_text\\_length](#page-124-0)

| Command-Line Format  | performance-schema-max-sql-text<br>length=# |
|----------------------|---------------------------------------------|
| System Variable      | performance_schema_max_sql_text_length      |
| Scope                | Global                                      |
| Dynamic              | No                                          |
| SET_VAR Hint Applies | No                                          |
| Type                 | Integer                                     |
| Default Value        | 1024                                        |
| Minimum Value        | 0                                           |
| Maximum Value        | 1048576                                     |
| Unit                 | bytes                                       |

The maximum number of bytes used to store SQL statements. The value applies to storage required for these columns:

- The SQL\_TEXT column of the events\_statements\_current, events\_statements\_history, and events\_statements\_history\_long statement event tables.
- The QUERY\_SAMPLE\_TEXT column of the [events\\_statements\\_summary\\_by\\_digest](#page-65-0) summary table.

Any bytes in excess of [performance\\_schema\\_max\\_sql\\_text\\_length](#page-124-0) are discarded and do not appear in the column. Statements differing only after that many initial bytes are indistinguishable in the column.

Decreasing the [performance\\_schema\\_max\\_sql\\_text\\_length](#page-124-0) value reduces memory use but causes more statements to become indistinguishable if they differ only at the end. Increasing the value increases memory use but permits longer statements to be distinguished.

<span id="page-124-1"></span>• [performance\\_schema\\_max\\_stage\\_classes](#page-124-1)

| Command-Line Format  | performance-schema-max-stage<br>classes=# |
|----------------------|-------------------------------------------|
| System Variable      | performance_schema_max_stage_classes      |
| Scope                | Global                                    |
| Dynamic              | No                                        |
| SET_VAR Hint Applies | No                                        |
| Type                 | Integer                                   |
| Default Value        | 175                                       |
| Minimum Value        | 0                                         |
| Maximum Value        | 1024                                      |

The maximum number of stage instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-124-2"></span>• [performance\\_schema\\_max\\_statement\\_classes](#page-124-2)

| Command-Line Format | performance-schema-max-statement |      |
|---------------------|----------------------------------|------|
|                     | classes=#                        | 5295 |

| System Variable      | performance_schema_max_statement_classes |
|----------------------|------------------------------------------|
| Scope                | Global                                   |
| Dynamic              | No                                       |
| SET_VAR Hint Applies | No                                       |
| Type                 | Integer                                  |
| Minimum Value        | 0                                        |
| Maximum Value        | 256                                      |

The maximum number of statement instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

The default value is calculated at server build time based on the number of commands in the client/ server protocol and the number of SQL statement types supported by the server.

This variable should not be changed, unless to set it to 0 to disable all statement instrumentation and save all memory associated with it. Setting the variable to nonzero values other than the default has no benefit; in particular, values larger than the default cause more memory to be allocated then is needed.

<span id="page-125-1"></span>• [performance\\_schema\\_max\\_statement\\_stack](#page-125-1)

| Command-Line Format  | performance-schema-max-statement<br>stack=# |
|----------------------|---------------------------------------------|
| System Variable      | performance_schema_max_statement_stack      |
| Scope                | Global                                      |
| Dynamic              | No                                          |
| SET_VAR Hint Applies | No                                          |
| Type                 | Integer                                     |
| Default Value        | 10                                          |
| Minimum Value        | 1                                           |
| Maximum Value        | 256                                         |

The maximum depth of nested stored program calls for which the Performance Schema maintains statistics. When this maximum is exceeded, the Performance Schema increments the [Performance\\_schema\\_nested\\_statement\\_lost](#page-131-7) status variable for each stored program statement executed.

<span id="page-125-0"></span>• [performance\\_schema\\_max\\_table\\_handles](#page-125-0)

| Command-Line Format  | performance-schema-max-table<br>handles=#                       |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_table_handles                            |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |

The maximum number of opened table objects. This value controls the size of the [table\\_handles](#page-41-0) table. If this maximum is exceeded such that a table handle cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_table\\_handles\\_lost](#page-132-6) status variable. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-126-1"></span>• [performance\\_schema\\_max\\_table\\_instances](#page-126-1)

| Command-Line Format  | performance-schema-max-table<br>instances=#                     |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_table_instances                          |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of instrumented table objects. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-126-2"></span>• [performance\\_schema\\_max\\_table\\_lock\\_stat](#page-126-2)

| Command-Line Format  | performance-schema-max-table-lock<br>stat=#                     |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_table_lock_stat                          |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of tables for which the Performance Schema maintains lock statistics. If this maximum is exceeded such that table lock statistics are lost, the Performance Schema increments the [Performance\\_schema\\_table\\_lock\\_stat\\_lost](#page-132-9) status variable.

<span id="page-126-0"></span>• [performance\\_schema\\_max\\_thread\\_classes](#page-126-0)

| Command-Line Format | performance-schema-max-thread<br>classes=# |
|---------------------|--------------------------------------------|
| System Variable     | performance_schema_max_thread_classes      |
| Scope               | Global<br>5297                             |

| Dynamic              | No      |
|----------------------|---------|
| SET_VAR Hint Applies | No      |
| Type                 | Integer |
| Default Value        | 100     |
| Minimum Value        | 0       |
| Maximum Value        | 1024    |

The maximum number of thread instruments. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

<span id="page-127-1"></span>• [performance\\_schema\\_max\\_thread\\_instances](#page-127-1)

| Command-Line Format  | performance-schema-max-thread<br>instances=#                    |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_max_thread_instances                         |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value        | 1048576                                                         |

The maximum number of instrumented thread objects. The value controls the size of the [threads](#page-99-0) table. If this maximum is exceeded such that a thread cannot be instrumented, the Performance Schema increments the [Performance\\_schema\\_thread\\_instances\\_lost](#page-133-0) status variable. For information about how to set and use this variable, see Section 29.7, "Performance Schema Status Monitoring".

The max\_connections system variable affects how many threads can run in the server. [performance\\_schema\\_max\\_thread\\_instances](#page-127-1) affects how many of these running threads can be instrumented.

The [variables\\_by\\_thread](#page-42-0) and [status\\_by\\_thread](#page-47-0) tables contain system and status variable information only about foreground threads. If not all threads are instrumented by the Performance Schema, this table misses some rows. In this case, the [Performance\\_schema\\_thread\\_instances\\_lost](#page-133-0) status variable is greater than zero.

<span id="page-127-0"></span>• [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0)

| Command-Line Format  | performance-schema-session<br>connect-attrs-size=#             |  |
|----------------------|----------------------------------------------------------------|--|
| System Variable      | performance_schema_session_connect_attrs_size                  |  |
| Scope                | Global                                                         |  |
| Dynamic              | No                                                             |  |
| SET_VAR Hint Applies | No                                                             |  |
| Type                 | Integer                                                        |  |
| Default Value        | -1 (signifies autosizing; do not assign this literal<br>value) |  |

| Minimum Value | -1 (signifies autosizing; do not assign this literal<br>value) |
|---------------|----------------------------------------------------------------|
| Maximum Value | 1048576                                                        |
| Unit          | bytes                                                          |

The amount of preallocated memory per thread reserved to hold connection attribute keyvalue pairs. If the aggregate size of connection attribute data sent by a client is larger than this amount, the Performance Schema truncates the attribute data, increments the [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-132-1) status variable, and writes a message to the error log indicating that truncation occurred if the log\_error\_verbosity system variable is greater than 1. A \_truncated attribute is also added to the session attributes with a value indicating how many bytes were lost, if the attribute buffer has sufficient space. This enables the Performance Schema to expose per-connection truncation information in the connection attribute tables. This information can be examined without having to check the error log.

The default value of [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) is autosized at server startup. This value may be small, so if truncation occurs ([Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-132-1) becomes nonzero), you may wish to set [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) explicitly to a larger value.

Although the maximum permitted [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-127-0) value is 1MB, the effective maximum is 64KB because the server imposes a limit of 64KB on the aggregate size of connection attribute data it accepts. If a client attempts to send more than 64KB of attribute data, the server rejects the connection. For more information, see [Section 29.12.9, "Performance](#page-2-0) [Schema Connection Attribute Tables"](#page-2-0).

<span id="page-128-0"></span>• [performance\\_schema\\_setup\\_actors\\_size](#page-128-0)

| Command-Line Format  | performance-schema-setup-actors<br>size=#                       |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_setup_actors_size                            |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autosizing; do not assign this literal<br>value)  |
| Maximum Value        | 1048576                                                         |

The number of rows in the setup\_actors table.

<span id="page-128-1"></span>• [performance\\_schema\\_setup\\_objects\\_size](#page-128-1)

| Command-Line Format  | performance-schema-setup-objects<br>size=# |
|----------------------|--------------------------------------------|
| System Variable      | performance_schema_setup_objects_size      |
| Scope                | Global                                     |
| Dynamic              | No                                         |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |

| Default Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
|---------------|-----------------------------------------------------------------|
| Minimum Value | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Maximum Value | 1048576                                                         |

The number of rows in the setup\_objects table.

<span id="page-129-1"></span>• [performance\\_schema\\_show\\_processlist](#page-129-1)

| Command-Line Format  | performance-schema-show<br>processlist[={OFF ON}] |  |
|----------------------|---------------------------------------------------|--|
| Deprecated           | Yes                                               |  |
| System Variable      | performance_schema_show_processlist               |  |
| Scope                | Global                                            |  |
| Dynamic              | Yes                                               |  |
| SET_VAR Hint Applies | No                                                |  |
| Type                 | Boolean                                           |  |
| Default Value        | OFF                                               |  |

The SHOW PROCESSLIST statement provides process information by collecting thread data from all active threads. The [performance\\_schema\\_show\\_processlist](#page-129-1) variable determines which SHOW PROCESSLIST implementation to use:

- The default implementation iterates across active threads from within the thread manager while holding a global mutex. This has negative performance consequences, particularly on busy systems.
- The alternative SHOW PROCESSLIST implementation is based on the Performance Schema [processlist](#page-96-0) table. This implementation queries active thread data from the Performance Schema rather than the thread manager and does not require a mutex.

To enable the alternative implementation, enable the [performance\\_schema\\_show\\_processlist](#page-129-1) system variable. To ensure that the default and alternative implementations yield the same information, certain configuration requirements must be met; see [Section 29.12.21.7, "The](#page-96-0) [processlist Table"](#page-96-0).

<span id="page-129-0"></span>• [performance\\_schema\\_users\\_size](#page-129-0)

| Command-Line Format  | performance-schema-users-size=#                                 |
|----------------------|-----------------------------------------------------------------|
| System Variable      | performance_schema_users_size                                   |
| Scope                | Global                                                          |
| Dynamic              | No                                                              |
| SET_VAR Hint Applies | No                                                              |
| Type                 | Integer                                                         |
| Default Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |
| Minimum Value        | -1 (signifies autoscaling; do not assign this literal<br>value) |

| Maximum Value | 1048576 |
|---------------|---------|
|---------------|---------|

The number of rows in the [users](#page-1-1) table. If this variable is 0, the Performance Schema does not maintain connection statistics in the [users](#page-1-1) table or status variable information in the [status\\_by\\_user](#page-86-0) table.