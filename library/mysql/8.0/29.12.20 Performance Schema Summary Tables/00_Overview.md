---
source: MySQL 8.0 Reference
title: 00_Overview
---

Summary tables provide aggregated information for terminated events over time. The tables in this group summarize event data in different ways.

Each summary table has grouping columns that determine how to group the data to be aggregated, and summary columns that contain the aggregated values. Tables that summarize events in similar ways often have similar sets of summary columns and differ only in the grouping columns used to determine how events are aggregated.

Summary tables can be truncated with TRUNCATE TABLE. Generally, the effect is to reset the summary columns to 0 or NULL, not to remove rows. This enables you to clear collected values and restart aggregation. That might be useful, for example, after you have made a runtime configuration change. Exceptions to this truncation behavior are noted in individual summary table sections.

# **Wait Event Summaries**

**Table 29.7 Performance Schema Wait Event Summary Tables**

| Table Name                                                                           | Description              |
|--------------------------------------------------------------------------------------|--------------------------|
| events_waits_summary_by_account_by_event_name Wait events per account and event name |                          |
| events_waits_summary_by_host_by_event_name Wait events per host name and event name  |                          |
| events_waits_summary_by_instance                                                     | Wait events per instance |
| events_waits_summary_by_thread_by_event_name Wait events per thread and event name   |                          |
| events_waits_summary_by_user_by_event_name Wait events per user name and event name  |                          |
| events_waits_summary_global_by_event_name Wait events per event name                 |                          |

## **Stage Summaries**

**Table 29.8 Performance Schema Stage Event Summary Tables**

| Table Name                                                                            | Description                             |
|---------------------------------------------------------------------------------------|-----------------------------------------|
| events_stages_summary_by_account_by_event_name                                        | Stage events per account and event name |
| events_stages_summary_by_host_by_event_name Stage events per host name and event name |                                         |
| events_stages_summary_by_thread_by_event_name Stage waits per thread and event name   |                                         |
| events_stages_summary_by_user_by_event_name Stage events per user name and event name |                                         |
| events_stages_summary_global_by_event_name Stage waits per event name                 |                                         |

## **Statement Summaries**

**Table 29.9 Performance Schema Statement Event Summary Tables**

| Table Name                                         | Description                                         |  |
|----------------------------------------------------|-----------------------------------------------------|--|
| events_statements_histogram_by_digest              | Statement histograms per schema and digest<br>value |  |
| events_statements_histogram_global                 | Statement histogram summarized globally             |  |
| events_statements_summary_by_account_by_event_name | Statement events per account and event name         |  |
| events_statements_summary_by_digest                | Statement events per schema and digest value        |  |
| events_statements_summary_by_host_by_event_name    | Statement events per host name and event name       |  |
| events_statements_summary_by_program               | Statement events per stored program                 |  |
| events_statements_summary_by_thread_by_event_name  | Statement events per thread and event name          |  |
| events_statements_summary_by_user_by_event_name    | Statement events per user name and event name       |  |
| events_statements_summary_global_by_event_name     | Statement events per event name                     |  |
| prepared_statements_instances                      | Prepared statement instances and statistics         |  |

## **Transaction Summaries**

**Table 29.10 Performance Schema Transaction Event Summary Tables**

| Table Name                                           | Description                                        |
|------------------------------------------------------|----------------------------------------------------|
| events_transactions_summary_by_account_by_event_name | Transaction events per account and event name      |
| events_transactions_summary_by_host_by_event_name    | Transaction events per host name and event<br>name |
| events_transactions_summary_by_thread_by_event_name  | Transaction events per thread and event name       |
| events_transactions_summary_by_user_by_event_name    | Transaction events per user name and event<br>name |
| events_transactions_summary_global_by_event_name     | Transaction events per event name                  |

### **Object Wait Summaries**

**Table 29.11 Performance Schema Object Event Summary Tables**

| Table Name                     | Description      |
|--------------------------------|------------------|
| objects_summary_global_by_type | Object summaries |

## **File I/O Summaries**

**Table 29.12 Performance Schema File I/O Event Summary Tables**

| Table Name                 | Description                   |
|----------------------------|-------------------------------|
| file_summary_by_event_name | File events per event name    |
| file_summary_by_instance   | File events per file instance |

### **Table I/O and Lock Wait Summaries**

**Table 29.13 Performance Schema Table I/O and Lock Wait Event Summary Tables**

| Table Name                            | Description               |
|---------------------------------------|---------------------------|
| table_io_waits_summary_by_index_usage | Table I/O waits per index |

| Table Name                        | Description                |
|-----------------------------------|----------------------------|
| table_io_waits_summary_by_table   | Table I/O waits per table  |
| table_lock_waits_summary_by_table | Table lock waits per table |

# **Socket Summaries**

**Table 29.14 Performance Schema Socket Event Summary Tables**

| Table Name                   | Description                         |
|------------------------------|-------------------------------------|
| socket_summary_by_event_name | Socket waits and I/O per event name |
| socket_summary_by_instance   | Socket waits and I/O per instance   |

## **Memory Summaries**

**Table 29.15 Performance Schema Memory Operation Summary Tables**

| Table Name                                                                          | Description                               |
|-------------------------------------------------------------------------------------|-------------------------------------------|
| memory_summary_by_account_by_event_nameMemory operations per account and event name |                                           |
| memory_summary_by_host_by_event_name                                                | Memory operations per host and event name |
| memory_summary_by_thread_by_event_nameMemory operations per thread and event name   |                                           |
| memory_summary_by_user_by_event_name                                                | Memory operations per user and event name |
| memory_summary_global_by_event_name                                                 | Memory operations globally per event name |

### **Error Summaries**

**Table 29.16 Performance Schema Error Summary Tables**

| Table Name                                                                  | Description           |
|-----------------------------------------------------------------------------|-----------------------|
| events_errors_summary_by_account_by_error Errors per account and error code |                       |
| events_errors_summary_by_host_by_errorErrors per host and error code        |                       |
| events_errors_summary_by_thread_by_errorErrors per thread and error code    |                       |
| events_errors_summary_by_user_by_errorErrors per user and error code        |                       |
| events_errors_summary_global_by_error                                       | Errors per error code |

### **Status Variable Summaries**

**Table 29.17 Performance Schema Error Status Variable Summary Tables**

| Table Name        | Description                            |
|-------------------|----------------------------------------|
| status_by_account | Session status variables per account   |
| status_by_host    | Session status variables per host name |
| status_by_user    | Session status variables per user name |

### <span id="page-61-0"></span>**29.12.20.1 Wait Event Summary Tables**

The Performance Schema maintains tables for collecting current and recent wait events, and aggregates that information in summary tables. Section 29.12.4, "Performance Schema Wait Event Tables" describes the events on which wait summaries are based. See that discussion for information about the content of wait events, the current and recent wait event tables, and how to control wait event collection, which is disabled by default.

Example wait event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_waits_summary_global_by_event_name\G
...
*************************** 6. row ***************************
 EVENT_NAME: wait/synch/mutex/sql/BINARY_LOG::LOCK_index
 COUNT_STAR: 8
SUM_TIMER_WAIT: 2119302
MIN_TIMER_WAIT: 196092
AVG_TIMER_WAIT: 264912
MAX_TIMER_WAIT: 569421
...
*************************** 9. row ***************************
 EVENT_NAME: wait/synch/mutex/sql/hash_filo::lock
 COUNT_STAR: 69
SUM_TIMER_WAIT: 16848828
MIN_TIMER_WAIT: 0
AVG_TIMER_WAIT: 244185
MAX_TIMER_WAIT: 735345
...
```

Each wait event summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [events\\_waits\\_summary\\_by\\_account\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_waits\\_summary\\_by\\_host\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_waits\\_summary\\_by\\_instance](#page-61-0) has EVENT\_NAME and OBJECT\_INSTANCE\_BEGIN columns. Each row summarizes events for a given event name and object. If an instrument is used to create multiple instances, each instance has a unique OBJECT\_INSTANCE\_BEGIN value and is summarized separately in this table.
- [events\\_waits\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-61-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_waits\\_summary\\_by\\_user\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-61-0) has an EVENT\_NAME column. Each row summarizes events for a given event name. An instrument might be used to create multiple instances of the instrumented object. For example, if there is an instrument for a mutex that is created for each connection, there are as many instances as there are connections. The summary row for the instrument summarizes over all these instances.

Each wait event summary table has these summary columns containing aggregated values:

• COUNT\_STAR

The number of summarized events. This value includes all events, whether timed or nontimed.

• SUM\_TIMER\_WAIT

The total wait time of the summarized timed events. This value is calculated only for timed events because nontimed events have a wait time of NULL. The same is true for the other xxx\_TIMER\_WAIT values.

• MIN\_TIMER\_WAIT

The minimum wait time of the summarized timed events.

• AVG\_TIMER\_WAIT

The average wait time of the summarized timed events.

• MAX\_TIMER\_WAIT

The maximum wait time of the summarized timed events.

The wait event summary tables have these indexes:

- [events\\_waits\\_summary\\_by\\_account\\_by\\_event\\_name](#page-63-0):
  - Primary key on (USER, HOST, EVENT\_NAME)
- [events\\_waits\\_summary\\_by\\_host\\_by\\_event\\_name](#page-63-0):
  - Primary key on (HOST, EVENT\_NAME)
- [events\\_waits\\_summary\\_by\\_instance](#page-61-0):
  - Primary key on (OBJECT\_INSTANCE\_BEGIN)
  - Index on (EVENT\_NAME)
- [events\\_waits\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-61-0):
  - Primary key on (THREAD\_ID, EVENT\_NAME)
- [events\\_waits\\_summary\\_by\\_user\\_by\\_event\\_name](#page-63-0):
  - Primary key on (USER, EVENT\_NAME)
- [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-61-0):
  - Primary key on (EVENT\_NAME)

TRUNCATE TABLE is permitted for wait summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each wait summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-61-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

### <span id="page-63-0"></span>**29.12.20.2 Stage Summary Tables**

The Performance Schema maintains tables for collecting current and recent stage events, and aggregates that information in summary tables. Section 29.12.5, "Performance Schema Stage Event Tables" describes the events on which stage summaries are based. See that discussion for information about the content of stage events, the current and historical stage event tables, and how to control stage event collection, which is disabled by default.

Example stage event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_stages_summary_global_by_event_name\G
...
*************************** 5. row ***************************
```

```
 EVENT_NAME: stage/sql/checking permissions
 COUNT_STAR: 57
SUM_TIMER_WAIT: 26501888880
MIN_TIMER_WAIT: 7317456
AVG_TIMER_WAIT: 464945295
MAX_TIMER_WAIT: 12858936792
...
*************************** 9. row ***************************
 EVENT_NAME: stage/sql/closing tables
 COUNT_STAR: 37
SUM_TIMER_WAIT: 662606568
MIN_TIMER_WAIT: 1593864
AVG_TIMER_WAIT: 17907891
MAX_TIMER_WAIT: 437977248
...
```

Each stage summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [events\\_stages\\_summary\\_by\\_account\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_stages\\_summary\\_by\\_host\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_stages\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-63-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_stages\\_summary\\_by\\_user\\_by\\_event\\_name](#page-63-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_stages\\_summary\\_global\\_by\\_event\\_name](#page-63-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.

Each stage summary table has these summary columns containing aggregated values: COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, and MAX\_TIMER\_WAIT. These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 29.12.20.1, "Wait Event Summary Tables"](#page-61-0)), except that the stage summary tables aggregate events from events\_stages\_current rather than events\_waits\_current.

The stage summary tables have these indexes:

- [events\\_stages\\_summary\\_by\\_account\\_by\\_event\\_name](#page-63-0):
  - Primary key on (USER, HOST, EVENT\_NAME)
- [events\\_stages\\_summary\\_by\\_host\\_by\\_event\\_name](#page-63-0):
  - Primary key on (HOST, EVENT\_NAME)
- [events\\_stages\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-63-0):
  - Primary key on (THREAD\_ID, EVENT\_NAME)
- [events\\_stages\\_summary\\_by\\_user\\_by\\_event\\_name](#page-63-0):
  - Primary key on (USER, EVENT\_NAME)
- [events\\_stages\\_summary\\_global\\_by\\_event\\_name](#page-63-0):
  - Primary key on (EVENT\_NAME)

TRUNCATE TABLE is permitted for stage summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each stage summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_stages\\_summary\\_global\\_by\\_event\\_name](#page-63-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

## <span id="page-65-0"></span>**29.12.20.3 Statement Summary Tables**

The Performance Schema maintains tables for collecting current and recent statement events, and aggregates that information in summary tables. Section 29.12.6, "Performance Schema Statement Event Tables" describes the events on which statement summaries are based. See that discussion for information about the content of statement events, the current and historical statement event tables, and how to control statement event collection, which is partially disabled by default.

Example statement event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_statements_summary_global_by_event_name\G
*************************** 1. row ***************************
 EVENT_NAME: statement/sql/select
 COUNT_STAR: 54
 SUM_TIMER_WAIT: 38860400000
 MIN_TIMER_WAIT: 52400000
 AVG_TIMER_WAIT: 719600000
 MAX_TIMER_WAIT: 12631800000
 SUM_LOCK_TIME: 88000000
 SUM_ERRORS: 0
 SUM_WARNINGS: 0
 SUM_ROWS_AFFECTED: 0
 SUM_ROWS_SENT: 60
 SUM_ROWS_EXAMINED: 120
SUM_CREATED_TMP_DISK_TABLES: 0
 SUM_CREATED_TMP_TABLES: 21
 SUM_SELECT_FULL_JOIN: 16
 SUM_SELECT_FULL_RANGE_JOIN: 0
 SUM_SELECT_RANGE: 0
 SUM_SELECT_RANGE_CHECK: 0
 SUM_SELECT_SCAN: 41
 SUM_SORT_MERGE_PASSES: 0
 SUM_SORT_RANGE: 0
 SUM_SORT_ROWS: 0
 SUM_SORT_SCAN: 0
 SUM_NO_INDEX_USED: 22
 SUM_NO_GOOD_INDEX_USED: 0
 SUM_CPU_TIME: 0
 MAX_CONTROLLED_MEMORY: 2028360
 MAX_TOTAL_MEMORY: 2853429
 COUNT_SECONDARY: 0
...
```

Each statement summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [events\\_statements\\_summary\\_by\\_account\\_by\\_event\\_name](#page-65-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_statements\\_summary\\_by\\_digest](#page-65-0) has SCHEMA\_NAME and DIGEST columns. Each row summarizes events per schema and digest value. (The DIGEST\_TEXT column contains the corresponding normalized statement digest text, but is neither a grouping nor a summary column.

The QUERY\_SAMPLE\_TEXT, QUERY\_SAMPLE\_SEEN, and QUERY\_SAMPLE\_TIMER\_WAIT columns also are neither grouping nor summary columns; they support statement sampling.)

The maximum number of rows in the table is autosized at server startup. To set this maximum explicitly, set the [performance\\_schema\\_digests\\_size](#page-113-0) system variable at server startup.

- [events\\_statements\\_summary\\_by\\_host\\_by\\_event\\_name](#page-65-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_statements\\_summary\\_by\\_program](#page-65-0) has OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME columns. Each row summarizes events for a given stored program (stored procedure or function, trigger, or event).
- [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-65-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_statements\\_summary\\_by\\_user\\_by\\_event\\_name](#page-65-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-65-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.
- prepared\_statements\_instances has an OBJECT\_INSTANCE\_BEGIN column. Each row summarizes events for a given prepared statement.

Each statement summary table has these summary columns containing aggregated values (with exceptions as noted):

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 29.12.20.1, "Wait Event Summary Tables"\)](#page-61-0), except that the statement summary tables aggregate events from events\_statements\_current rather than events\_waits\_current.

The prepared\_statements\_instances table does not have these columns.

• SUM\_xxx

The aggregate of the corresponding xxx column in the events\_statements\_current table. For example, the SUM\_LOCK\_TIME and SUM\_ERRORS columns in statement summary tables are the aggregates of the LOCK\_TIME and ERRORS columns in events\_statements\_current table.

• MAX\_CONTROLLED\_MEMORY

Reports the maximum amount of controlled memory used by a statement during execution.

This column was added in MySQL 8.0.31.

• MAX\_TOTAL\_MEMORY

Reports the maximum amount of memory used by a statement during execution.

This column was added in MySQL 8.0.31.

• COUNT\_SECONDARY

The number of times a query was processed on the SECONDARY engine. For use with MySQL HeatWave Service and MySQL HeatWave, where the PRIMARY engine is InnoDB and the SECONDARY engine is MySQL HeatWave (RAPID). For MySQL Community Edition Server, MySQL Enterprise Edition Server (on-premise), and MySQL HeatWave Service without MySQL HeatWave, queries are always processed on the PRIMARY engine, which means the value is always 0 on these MySQL Servers. The COUNT\_SECONDARY column was added in MySQL 8.0.29.

The [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table has these additional summary columns:

• FIRST\_SEEN, LAST\_SEEN

Timestamps indicating when statements with the given digest value were first seen and most recently seen.

• QUANTILE\_95: The 95th percentile of the statement latency, in picoseconds. This percentile is a high estimate, computed from the histogram data collected. In other words, for a given digest, 95% of the statements measured have a latency lower than QUANTILE\_95.

For access to the histogram data, use the tables described in [Section 29.12.20.4, "Statement](#page-69-0) [Histogram Summary Tables"](#page-69-0).

- QUANTILE\_99: Similar to QUANTILE\_95, but for the 99th percentile.
- QUANTILE\_999: Similar to QUANTILE\_95, but for the 99.9th percentile.

The [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table contains the following columns. These are neither grouping nor summary columns; they support statement sampling:

• QUERY\_SAMPLE\_TEXT

A sample SQL statement that produces the digest value in the row. This column enables applications to access, for a given digest value, a statement actually seen by the server that produces that digest. One use for this might be to run EXPLAIN on the statement to examine the execution plan for a representative statement associated with a frequently occurring digest.

When the QUERY\_SAMPLE\_TEXT column is assigned a value, the QUERY\_SAMPLE\_SEEN and QUERY\_SAMPLE\_TIMER\_WAIT columns are assigned values as well.

The maximum space available for statement display is 1024 bytes by default. To change this value, set the [performance\\_schema\\_max\\_sql\\_text\\_length](#page-124-0) system variable at server startup. (Changing this value affects columns in other Performance Schema tables as well. See Section 29.10, "Performance Schema Statement Digests and Sampling".)

For information about statement sampling, see Section 29.10, "Performance Schema Statement Digests and Sampling".

• QUERY\_SAMPLE\_SEEN

A timestamp indicating when the statement in the QUERY\_SAMPLE\_TEXT column was seen.

• QUERY\_SAMPLE\_TIMER\_WAIT

The wait time for the sample statement in the QUERY\_SAMPLE\_TEXT column.

The [events\\_statements\\_summary\\_by\\_program](#page-65-0) table has these additional summary columns:

• COUNT\_STATEMENTS, SUM\_STATEMENTS\_WAIT, MIN\_STATEMENTS\_WAIT, AVG\_STATEMENTS\_WAIT, MAX\_STATEMENTS\_WAIT

Statistics about nested statements invoked during stored program execution.

The prepared\_statements\_instances table has these additional summary columns:

• COUNT\_EXECUTE, SUM\_TIMER\_EXECUTE, MIN\_TIMER\_EXECUTE, AVG\_TIMER\_EXECUTE, MAX\_TIMER\_EXECUTE

Aggregated statistics for executions of the prepared statement.

The statement summary tables have these indexes:

- [events\\_transactions\\_summary\\_by\\_account\\_by\\_event\\_name](#page-71-0):
  - Primary key on (USER, HOST, EVENT\_NAME)
- [events\\_statements\\_summary\\_by\\_digest](#page-65-0):
  - Primary key on (SCHEMA\_NAME, DIGEST)
- [events\\_transactions\\_summary\\_by\\_host\\_by\\_event\\_name](#page-71-0):
  - Primary key on (HOST, EVENT\_NAME)
- [events\\_statements\\_summary\\_by\\_program](#page-65-0):
  - Primary key on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)
- [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-65-0):
  - Primary key on (THREAD\_ID, EVENT\_NAME)
- [events\\_transactions\\_summary\\_by\\_user\\_by\\_event\\_name](#page-71-0):
  - Primary key on (USER, EVENT\_NAME)
- [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-65-0):
  - Primary key on (EVENT\_NAME)

TRUNCATE TABLE is permitted for statement summary tables. It has these effects:

- For [events\\_statements\\_summary\\_by\\_digest](#page-65-0), it removes the rows.
- For other summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For other summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each statement summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-65-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

In addition, truncating [events\\_statements\\_summary\\_by\\_digest](#page-65-0) implicitly truncates [events\\_statements\\_histogram\\_by\\_digest](#page-69-0), and truncating [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-65-0) implicitly truncates [events\\_statements\\_histogram\\_global](#page-69-0).

### **Statement Digest Aggregation Rules**

If the statements\_digest consumer is enabled, aggregation into [events\\_statements\\_summary\\_by\\_digest](#page-65-0) occurs as follows when a statement completes. Aggregation is based on the DIGEST value computed for the statement.

- If a [events\\_statements\\_summary\\_by\\_digest](#page-65-0) row already exists with the digest value for the statement that just completed, statistics for the statement are aggregated to that row. The LAST\_SEEN column is updated to the current time.
- If no row has the digest value for the statement that just completed, and the table is not full, a new row is created for the statement. The FIRST\_SEEN and LAST\_SEEN columns are initialized with the current time.

• If no row has the statement digest value for the statement that just completed, and the table is full, the statistics for the statement that just completed are added to a special "catch-all" row with DIGEST = NULL, which is created if necessary. If the row is created, the FIRST\_SEEN and LAST\_SEEN columns are initialized with the current time. Otherwise, the LAST\_SEEN column is updated with the current time.

The row with DIGEST = NULL is maintained because Performance Schema tables have a maximum size due to memory constraints. The DIGEST = NULL row permits digests that do not match other rows to be counted even if the summary table is full, using a common "other" bucket. This row helps you estimate whether the digest summary is representative:

- A DIGEST = NULL row that has a COUNT\_STAR value that represents 5% of all digests shows that the digest summary table is very representative; the other rows cover 95% of the statements seen.
- A DIGEST = NULL row that has a COUNT\_STAR value that represents 50% of all digests shows that the digest summary table is not very representative; the other rows cover only half the statements seen. Most likely the DBA should increase the maximum table size so that more of the rows counted in the DIGEST = NULL row would be counted using more specific rows instead. By default, the table is autosized, but if this size is too small, set the [performance\\_schema\\_digests\\_size](#page-113-0) system variable to a larger value at server startup.

## **Stored Program Instrumentation Behavior**

For stored program types for which instrumentation is enabled in the setup\_objects table, [events\\_statements\\_summary\\_by\\_program](#page-65-0) maintains statistics for stored programs as follows:

- A row is added for an object when it is first used in the server.
- The row for an object is removed when the object is dropped.
- Statistics are aggregated in the row for an object as it executes.

See also Section 29.4.3, "Event Pre-Filtering".

## <span id="page-69-0"></span>**29.12.20.4 Statement Histogram Summary Tables**

The Performance Schema maintains statement event summary tables that contain information about minimum, maximum, and average statement latency (see [Section 29.12.20.3, "Statement Summary](#page-65-0) [Tables"](#page-65-0)). Those tables permit high-level assessment of system performance. To permit assessment at a more fine-grained level, the Performance Schema also collects histogram data for statement latencies. These histograms provide additional insight into latency distributions.

Section 29.12.6, "Performance Schema Statement Event Tables" describes the events on which statement summaries are based. See that discussion for information about the content of statement events, the current and historical statement event tables, and how to control statement event collection, which is partially disabled by default.

Example statement histogram information:

```
mysql> SELECT *
 FROM performance_schema.events_statements_histogram_by_digest
 WHERE SCHEMA_NAME = 'mydb' AND DIGEST = 'bb3f69453119b2d7b3ae40673a9d4c7c'
 AND COUNT_BUCKET > 0 ORDER BY BUCKET_NUMBER\G
*************************** 1. row ***************************
 SCHEMA_NAME: mydb
 DIGEST: bb3f69453119b2d7b3ae40673a9d4c7c
 BUCKET_NUMBER: 42
 BUCKET_TIMER_LOW: 66069344
 BUCKET_TIMER_HIGH: 69183097
 COUNT_BUCKET: 1
COUNT_BUCKET_AND_LOWER: 1
 BUCKET_QUANTILE: 0.058824
*************************** 2. row ***************************
```

```
 SCHEMA_NAME: mydb
 DIGEST: bb3f69453119b2d7b3ae40673a9d4c7c
 BUCKET_NUMBER: 43
 BUCKET_TIMER_LOW: 69183097
 BUCKET_TIMER_HIGH: 72443596
 COUNT_BUCKET: 1
COUNT_BUCKET_AND_LOWER: 2
 BUCKET_QUANTILE: 0.117647
*************************** 3. row ***************************
 SCHEMA_NAME: mydb
 DIGEST: bb3f69453119b2d7b3ae40673a9d4c7c
 BUCKET_NUMBER: 44
 BUCKET_TIMER_LOW: 72443596
 BUCKET_TIMER_HIGH: 75857757
 COUNT_BUCKET: 2
COUNT_BUCKET_AND_LOWER: 4
 BUCKET_QUANTILE: 0.235294
*************************** 4. row ***************************
 SCHEMA_NAME: mydb
 DIGEST: bb3f69453119b2d7b3ae40673a9d4c7c
 BUCKET_NUMBER: 45
 BUCKET_TIMER_LOW: 75857757
 BUCKET_TIMER_HIGH: 79432823
 COUNT_BUCKET: 6
COUNT_BUCKET_AND_LOWER: 10
 BUCKET_QUANTILE: 0.625000
...
```

For example, in row 3, these values indicate that 23.52% of queries run in under 75.86 microseconds:

```
BUCKET_TIMER_HIGH: 75857757
 BUCKET_QUANTILE: 0.235294
```

In row 4, these values indicate that 62.50% of queries run in under 79.44 microseconds:

```
BUCKET_TIMER_HIGH: 79432823
 BUCKET_QUANTILE: 0.625000
```

Each statement histogram summary table has one or more grouping columns to indicate how the table aggregates events:

- [events\\_statements\\_histogram\\_by\\_digest](#page-69-0) has SCHEMA\_NAME, DIGEST, and BUCKET\_NUMBER columns:
  - The SCHEMA\_NAME and DIGEST columns identify a statement digest row in the [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table.
  - The [events\\_statements\\_histogram\\_by\\_digest](#page-69-0) rows with the same SCHEMA\_NAME and DIGEST values comprise the histogram for that schema/digest combination.
  - Within a given histogram, the BUCKET\_NUMBER column indicates the bucket number.
- [events\\_statements\\_histogram\\_global](#page-69-0) has a BUCKET\_NUMBER column. This table summarizes latencies globally across schema name and digest values, using a single histogram. The BUCKET\_NUMBER column indicates the bucket number within this global histogram.

A histogram consists of N buckets, where each row represents one bucket, with the bucket number indicated by the BUCKET\_NUMBER column. Bucket numbers begin with 0.

Each statement histogram summary table has these summary columns containing aggregated values:

• BUCKET\_TIMER\_LOW, BUCKET\_TIMER\_HIGH

A bucket counts statements that have a latency, in picoseconds, measured between BUCKET\_TIMER\_LOW and BUCKET\_TIMER\_HIGH:

• The value of BUCKET\_TIMER\_LOW for the first bucket (BUCKET\_NUMBER = 0) is 0.

- The value of BUCKET\_TIMER\_LOW for a bucket (BUCKET\_NUMBER = k) is the same as BUCKET\_TIMER\_HIGH for the previous bucket (BUCKET\_NUMBER = k−1)
- The last bucket is a catchall for statements that have a latency exceeding previous buckets in the histogram.
- COUNT\_BUCKET

The number of statements measured with a latency in the interval from BUCKET\_TIMER\_LOW up to but not including BUCKET\_TIMER\_HIGH.

• COUNT\_BUCKET\_AND\_LOWER

The number of statements measured with a latency in the interval from 0 up to but not including BUCKET\_TIMER\_HIGH.

• BUCKET\_QUANTILE

The proportion of statements that fall into this or a lower bucket. This proportion corresponds by definition to COUNT\_BUCKET\_AND\_LOWER / SUM(COUNT\_BUCKET) and is displayed as a convenience column.

The statement histogram summary tables have these indexes:

- [events\\_statements\\_histogram\\_by\\_digest](#page-69-0):
  - Unique index on (SCHEMA\_NAME, DIGEST, BUCKET\_NUMBER)
- [events\\_statements\\_histogram\\_global](#page-69-0):
  - Primary key on (BUCKET\_NUMBER)

TRUNCATE TABLE is permitted for statement histogram summary tables. Truncation sets the COUNT\_BUCKET and COUNT\_BUCKET\_AND\_LOWER columns to 0.

In addition, truncating [events\\_statements\\_summary\\_by\\_digest](#page-65-0) implicitly truncates [events\\_statements\\_histogram\\_by\\_digest](#page-69-0), and truncating [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-65-0) implicitly truncates [events\\_statements\\_histogram\\_global](#page-69-0).

### <span id="page-71-0"></span>**29.12.20.5 Transaction Summary Tables**

The Performance Schema maintains tables for collecting current and recent transaction events, and aggregates that information in summary tables. Section 29.12.7, "Performance Schema Transaction Tables" describes the events on which transaction summaries are based. See that discussion for information about the content of transaction events, the current and historical transaction event tables, and how to control transaction event collection, which is disabled by default.

Example transaction event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_transactions_summary_global_by_event_name
 LIMIT 1\G
*************************** 1. row ***************************
 EVENT_NAME: transaction
 COUNT_STAR: 5
 SUM_TIMER_WAIT: 19550092000
 MIN_TIMER_WAIT: 2954148000
 AVG_TIMER_WAIT: 3910018000
 MAX_TIMER_WAIT: 5486275000
 COUNT_READ_WRITE: 5
SUM_TIMER_READ_WRITE: 19550092000
```

```
MIN_TIMER_READ_WRITE: 2954148000
AVG_TIMER_READ_WRITE: 3910018000
MAX_TIMER_READ_WRITE: 5486275000
 COUNT_READ_ONLY: 0
 SUM_TIMER_READ_ONLY: 0
 MIN_TIMER_READ_ONLY: 0
 AVG_TIMER_READ_ONLY: 0
 MAX_TIMER_READ_ONLY: 0
```

Each transaction summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [events\\_transactions\\_summary\\_by\\_account\\_by\\_event\\_name](#page-71-0) has USER, HOST, and EVENT\_NAME columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_transactions\\_summary\\_by\\_host\\_by\\_event\\_name](#page-71-0) has HOST and EVENT\_NAME columns. Each row summarizes events for a given host and event name.
- [events\\_transactions\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-71-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_transactions\\_summary\\_by\\_user\\_by\\_event\\_name](#page-71-0) has USER and EVENT\_NAME columns. Each row summarizes events for a given user and event name.
- [events\\_transactions\\_summary\\_global\\_by\\_event\\_name](#page-71-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.

Each transaction summary table has these summary columns containing aggregated values:

```
• COUNT_STAR, SUM_TIMER_WAIT, MIN_TIMER_WAIT, AVG_TIMER_WAIT, MAX_TIMER_WAIT
```

These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 29.12.20.1, "Wait Event Summary Tables"\)](#page-61-0), except that the transaction summary tables aggregate events from events\_transactions\_current rather than events\_waits\_current. These columns summarize read-write and read-only transactions.

```
• COUNT_READ_WRITE, SUM_TIMER_READ_WRITE, MIN_TIMER_READ_WRITE,
 AVG_TIMER_READ_WRITE, MAX_TIMER_READ_WRITE
```

These are similar to the COUNT\_STAR and xxx\_TIMER\_WAIT columns, but summarize read-write transactions only. The transaction access mode specifies whether transactions operate in read/write or read-only mode.

```
• COUNT_READ_ONLY, SUM_TIMER_READ_ONLY, MIN_TIMER_READ_ONLY,
 AVG_TIMER_READ_ONLY, MAX_TIMER_READ_ONLY
```

These are similar to the COUNT\_STAR and xxx\_TIMER\_WAIT columns, but summarize read-only transactions only. The transaction access mode specifies whether transactions operate in read/write or read-only mode.

The transaction summary tables have these indexes:

- [events\\_transactions\\_summary\\_by\\_account\\_by\\_event\\_name](#page-71-0):
  - Primary key on (USER, HOST, EVENT\_NAME)
- [events\\_transactions\\_summary\\_by\\_host\\_by\\_event\\_name](#page-71-0):
  - Primary key on (HOST, EVENT\_NAME)
- [events\\_transactions\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-71-0):

- Primary key on (THREAD\_ID, EVENT\_NAME)
- [events\\_transactions\\_summary\\_by\\_user\\_by\\_event\\_name](#page-71-0):
  - Primary key on (USER, EVENT\_NAME)
- [events\\_transactions\\_summary\\_global\\_by\\_event\\_name](#page-71-0):
  - Primary key on (EVENT\_NAME)

TRUNCATE TABLE is permitted for transaction summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each transaction summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_transactions\\_summary\\_global\\_by\\_event\\_name](#page-71-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

### **Transaction Aggregation Rules**

Transaction event collection occurs without regard to isolation level, access mode, or autocommit mode.

Transaction event collection occurs for all non-aborted transactions initiated by the server, including empty transactions.

Read-write transactions are generally more resource intensive than read-only transactions, therefore transaction summary tables include separate aggregate columns for read-write and read-only transactions.

Resource requirements may also vary with transaction isolation level. However, presuming that only one isolation level would be used per server, aggregation by isolation level is not provided.

### <span id="page-73-0"></span>**29.12.20.6 Object Wait Summary Table**

The Performance Schema maintains the [objects\\_summary\\_global\\_by\\_type](#page-73-0) table for aggregating object wait events.

Example object wait event summary information:

```
mysql> SELECT * FROM performance_schema.objects_summary_global_by_type\G
...
*************************** 3. row ***************************
 OBJECT_TYPE: TABLE
 OBJECT_SCHEMA: test
 OBJECT_NAME: t
 COUNT_STAR: 3
SUM_TIMER_WAIT: 263126976
MIN_TIMER_WAIT: 1522272
AVG_TIMER_WAIT: 87708678
MAX_TIMER_WAIT: 258428280
...
*************************** 10. row ***************************
 OBJECT_TYPE: TABLE
 OBJECT_SCHEMA: mysql
 OBJECT_NAME: user
 COUNT_STAR: 14
SUM_TIMER_WAIT: 365567592
```

```
MIN_TIMER_WAIT: 1141704
AVG_TIMER_WAIT: 26111769
MAX_TIMER_WAIT: 334783032
...
```

The [objects\\_summary\\_global\\_by\\_type](#page-73-0) table has these grouping columns to indicate how the table aggregates events: OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME. Each row summarizes events for the given object.

[objects\\_summary\\_global\\_by\\_type](#page-73-0) has the same summary columns as the events\_waits\_summary\_by\_xxx tables. See [Section 29.12.20.1, "Wait Event Summary Tables".](#page-61-0)

The [objects\\_summary\\_global\\_by\\_type](#page-73-0) table has these indexes:

• Primary key on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)

TRUNCATE TABLE is permitted for the object summary table. It resets the summary columns to zero rather than removing rows.

## <span id="page-74-0"></span>**29.12.20.7 File I/O Summary Tables**

The Performance Schema maintains file I/O summary tables that aggregate information about I/O operations.

Example file I/O event summary information:

```
mysql> SELECT * FROM performance_schema.file_summary_by_event_name\G
...
*************************** 2. row ***************************
 EVENT_NAME: wait/io/file/sql/binlog
 COUNT_STAR: 31
 SUM_TIMER_WAIT: 8243784888
 MIN_TIMER_WAIT: 0
 AVG_TIMER_WAIT: 265928484
 MAX_TIMER_WAIT: 6490658832
...
mysql> SELECT * FROM performance_schema.file_summary_by_instance\G
...
*************************** 2. row ***************************
 FILE_NAME: /var/mysql/share/english/errmsg.sys
 EVENT_NAME: wait/io/file/sql/ERRMSG
 EVENT_NAME: wait/io/file/sql/ERRMSG
 OBJECT_INSTANCE_BEGIN: 4686193384
 COUNT_STAR: 5
 SUM_TIMER_WAIT: 13990154448
 MIN_TIMER_WAIT: 26349624
 AVG_TIMER_WAIT: 2798030607
 MAX_TIMER_WAIT: 8150662536
...
```

Each file I/O summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [file\\_summary\\_by\\_event\\_name](#page-74-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.
- [file\\_summary\\_by\\_instance](#page-74-0) has FILE\_NAME, EVENT\_NAME, and OBJECT\_INSTANCE\_BEGIN columns. Each row summarizes events for a given file and event name.

Each file I/O summary table has the following summary columns containing aggregated values. Some columns are more general and have values that are the same as the sum of the values of more finegrained columns. In this way, aggregations at higher levels are available directly without the need for user-defined views that sum lower-level columns.

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns aggregate all I/O operations.

• COUNT\_READ, SUM\_TIMER\_READ, MIN\_TIMER\_READ, AVG\_TIMER\_READ, MAX\_TIMER\_READ, SUM\_NUMBER\_OF\_BYTES\_READ

These columns aggregate all read operations, including FGETS, FGETC, FREAD, and READ.

• COUNT\_WRITE, SUM\_TIMER\_WRITE, MIN\_TIMER\_WRITE, AVG\_TIMER\_WRITE, MAX\_TIMER\_WRITE, SUM\_NUMBER\_OF\_BYTES\_WRITE

These columns aggregate all write operations, including FPUTS, FPUTC, FPRINTF, VFPRINTF, FWRITE, and PWRITE.

• COUNT\_MISC, SUM\_TIMER\_MISC, MIN\_TIMER\_MISC, AVG\_TIMER\_MISC, MAX\_TIMER\_MISC

These columns aggregate all other I/O operations, including CREATE, DELETE, OPEN, CLOSE, STREAM\_OPEN, STREAM\_CLOSE, SEEK, TELL, FLUSH, STAT, FSTAT, CHSIZE, RENAME, and SYNC. There are no byte counts for these operations.

The file I/O summary tables have these indexes:

- [file\\_summary\\_by\\_event\\_name](#page-74-0):
  - Primary key on (EVENT\_NAME)
- [file\\_summary\\_by\\_instance](#page-74-0):
  - Primary key on (OBJECT\_INSTANCE\_BEGIN)
  - Index on (FILE\_NAME)
  - Index on (EVENT\_NAME)

TRUNCATE TABLE is permitted for file I/O summary tables. It resets the summary columns to zero rather than removing rows.

The MySQL server uses several techniques to avoid I/O operations by caching information read from files, so it is possible that statements you might expect to result in I/O events do not do so. You may be able to ensure that I/O does occur by flushing caches or restarting the server to reset its state.

### **29.12.20.8 Table I/O and Lock Wait Summary Tables**

The following sections describe the table I/O and lock wait summary tables:

- [table\\_io\\_waits\\_summary\\_by\\_index\\_usage](#page-76-0): Table I/O waits per index
- [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0): Table I/O waits per table
- [table\\_lock\\_waits\\_summary\\_by\\_table](#page-77-0): Table lock waits per table

### <span id="page-75-0"></span>**The table\_io\_waits\_summary\_by\_table Table**

The [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0) table aggregates all table I/O wait events, as generated by the wait/io/table/sql/handler instrument. The grouping is by table.

The [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0) table has these grouping columns to indicate how the table aggregates events: OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME. These columns have the same meaning as in the events\_waits\_current table. They identify the table to which the row applies.

[table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0) has the following summary columns containing aggregated values. As indicated in the column descriptions, some columns are more general and have values

that are the same as the sum of the values of more fine-grained columns. For example, columns that aggregate all writes hold the sum of the corresponding columns that aggregate inserts, updates, and deletes. In this way, aggregations at higher levels are available directly without the need for userdefined views that sum lower-level columns.

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns aggregate all I/O operations. They are the same as the sum of the corresponding xxx\_READ and xxx\_WRITE columns.

• COUNT\_READ, SUM\_TIMER\_READ, MIN\_TIMER\_READ, AVG\_TIMER\_READ, MAX\_TIMER\_READ

These columns aggregate all read operations. They are the same as the sum of the corresponding xxx\_FETCH columns.

• COUNT\_WRITE, SUM\_TIMER\_WRITE, MIN\_TIMER\_WRITE, AVG\_TIMER\_WRITE, MAX\_TIMER\_WRITE

These columns aggregate all write operations. They are the same as the sum of the corresponding xxx\_INSERT, xxx\_UPDATE, and xxx\_DELETE columns.

• COUNT\_FETCH, SUM\_TIMER\_FETCH, MIN\_TIMER\_FETCH, AVG\_TIMER\_FETCH, MAX\_TIMER\_FETCH

These columns aggregate all fetch operations.

• COUNT\_INSERT, SUM\_TIMER\_INSERT, MIN\_TIMER\_INSERT, AVG\_TIMER\_INSERT, MAX\_TIMER\_INSERT

These columns aggregate all insert operations.

• COUNT\_UPDATE, SUM\_TIMER\_UPDATE, MIN\_TIMER\_UPDATE, AVG\_TIMER\_UPDATE, MAX\_TIMER\_UPDATE

These columns aggregate all update operations.

• COUNT\_DELETE, SUM\_TIMER\_DELETE, MIN\_TIMER\_DELETE, AVG\_TIMER\_DELETE, MAX\_TIMER\_DELETE

These columns aggregate all delete operations.

The [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0) table has these indexes:

• Unique index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)

TRUNCATE TABLE is permitted for table I/O summary tables. It resets the summary columns to zero rather than removing rows. Truncating this table also truncates the [table\\_io\\_waits\\_summary\\_by\\_index\\_usage](#page-76-0) table.

## <span id="page-76-0"></span>**The table\_io\_waits\_summary\_by\_index\_usage Table**

The [table\\_io\\_waits\\_summary\\_by\\_index\\_usage](#page-76-0) table aggregates all table index I/O wait events, as generated by the wait/io/table/sql/handler instrument. The grouping is by table index.

The columns of [table\\_io\\_waits\\_summary\\_by\\_index\\_usage](#page-76-0) are nearly identical to [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0). The only difference is the additional group column, INDEX\_NAME, which corresponds to the name of the index that was used when the table I/O wait event was recorded:

- A value of PRIMARY indicates that table I/O used the primary index.
- A value of NULL means that table I/O used no index.

• Inserts are counted against INDEX\_NAME = NULL.

The [table\\_io\\_waits\\_summary\\_by\\_index\\_usage](#page-76-0) table has these indexes:

• Unique index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME, INDEX\_NAME)

TRUNCATE TABLE is permitted for table I/O summary tables. It resets the summary columns to zero rather than removing rows. This table is also truncated by truncation of the [table\\_io\\_waits\\_summary\\_by\\_table](#page-75-0) table. A DDL operation that changes the index structure of a table may cause the per-index statistics to be reset.

### <span id="page-77-0"></span>**The table\_lock\_waits\_summary\_by\_table Table**

The [table\\_lock\\_waits\\_summary\\_by\\_table](#page-77-0) table aggregates all table lock wait events, as generated by the wait/lock/table/sql/handler instrument. The grouping is by table.

This table contains information about internal and external locks:

• An internal lock corresponds to a lock in the SQL layer. This is currently implemented by a call to thr\_lock(). In event rows, these locks are distinguished by the OPERATION column, which has one of these values:

```
read normal
read with shared locks
read high priority
read no insert
write allow write
write concurrent insert
write delayed
write low priority
write normal
```

• An external lock corresponds to a lock in the storage engine layer. This is currently implemented by a call to handler::external\_lock(). In event rows, these locks are distinguished by the OPERATION column, which has one of these values:

```
read external
write external
```

The [table\\_lock\\_waits\\_summary\\_by\\_table](#page-77-0) table has these grouping columns to indicate how the table aggregates events: OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME. These columns have the same meaning as in the events\_waits\_current table. They identify the table to which the row applies.

[table\\_lock\\_waits\\_summary\\_by\\_table](#page-77-0) has the following summary columns containing aggregated values. As indicated in the column descriptions, some columns are more general and have values that are the same as the sum of the values of more fine-grained columns. For example, columns that aggregate all locks hold the sum of the corresponding columns that aggregate read and write locks. In this way, aggregations at higher levels are available directly without the need for user-defined views that sum lower-level columns.

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns aggregate all lock operations. They are the same as the sum of the corresponding xxx\_READ and xxx\_WRITE columns.

• COUNT\_READ, SUM\_TIMER\_READ, MIN\_TIMER\_READ, AVG\_TIMER\_READ, MAX\_TIMER\_READ

These columns aggregate all read-lock operations. They are the same as the sum of the corresponding xxx\_READ\_NORMAL, xxx\_READ\_WITH\_SHARED\_LOCKS, xxx\_READ\_HIGH\_PRIORITY, and xxx\_READ\_NO\_INSERT columns.

• COUNT\_WRITE, SUM\_TIMER\_WRITE, MIN\_TIMER\_WRITE, AVG\_TIMER\_WRITE, MAX\_TIMER\_WRITE

These columns aggregate all write-lock operations. They are the same as the sum of the corresponding xxx\_WRITE\_ALLOW\_WRITE, xxx\_WRITE\_CONCURRENT\_INSERT, xxx\_WRITE\_LOW\_PRIORITY, and xxx\_WRITE\_NORMAL columns.

• COUNT\_READ\_NORMAL, SUM\_TIMER\_READ\_NORMAL, MIN\_TIMER\_READ\_NORMAL, AVG\_TIMER\_READ\_NORMAL, MAX\_TIMER\_READ\_NORMAL

These columns aggregate internal read locks.

• COUNT\_READ\_WITH\_SHARED\_LOCKS, SUM\_TIMER\_READ\_WITH\_SHARED\_LOCKS, MIN\_TIMER\_READ\_WITH\_SHARED\_LOCKS, AVG\_TIMER\_READ\_WITH\_SHARED\_LOCKS, MAX\_TIMER\_READ\_WITH\_SHARED\_LOCKS

These columns aggregate internal read locks.

• COUNT\_READ\_HIGH\_PRIORITY, SUM\_TIMER\_READ\_HIGH\_PRIORITY, MIN\_TIMER\_READ\_HIGH\_PRIORITY, AVG\_TIMER\_READ\_HIGH\_PRIORITY, MAX\_TIMER\_READ\_HIGH\_PRIORITY

These columns aggregate internal read locks.

• COUNT\_READ\_NO\_INSERT, SUM\_TIMER\_READ\_NO\_INSERT, MIN\_TIMER\_READ\_NO\_INSERT, AVG\_TIMER\_READ\_NO\_INSERT, MAX\_TIMER\_READ\_NO\_INSERT

These columns aggregate internal read locks.

• COUNT\_READ\_EXTERNAL, SUM\_TIMER\_READ\_EXTERNAL, MIN\_TIMER\_READ\_EXTERNAL, AVG\_TIMER\_READ\_EXTERNAL, MAX\_TIMER\_READ\_EXTERNAL

These columns aggregate external read locks.

• COUNT\_WRITE\_ALLOW\_WRITE, SUM\_TIMER\_WRITE\_ALLOW\_WRITE, MIN\_TIMER\_WRITE\_ALLOW\_WRITE, AVG\_TIMER\_WRITE\_ALLOW\_WRITE, MAX\_TIMER\_WRITE\_ALLOW\_WRITE

These columns aggregate internal write locks.

• COUNT\_WRITE\_CONCURRENT\_INSERT, SUM\_TIMER\_WRITE\_CONCURRENT\_INSERT, MIN\_TIMER\_WRITE\_CONCURRENT\_INSERT, AVG\_TIMER\_WRITE\_CONCURRENT\_INSERT, MAX\_TIMER\_WRITE\_CONCURRENT\_INSERT

These columns aggregate internal write locks.

• COUNT\_WRITE\_LOW\_PRIORITY, SUM\_TIMER\_WRITE\_LOW\_PRIORITY, MIN\_TIMER\_WRITE\_LOW\_PRIORITY, AVG\_TIMER\_WRITE\_LOW\_PRIORITY, MAX\_TIMER\_WRITE\_LOW\_PRIORITY

These columns aggregate internal write locks.

• COUNT\_WRITE\_NORMAL, SUM\_TIMER\_WRITE\_NORMAL, MIN\_TIMER\_WRITE\_NORMAL, AVG\_TIMER\_WRITE\_NORMAL, MAX\_TIMER\_WRITE\_NORMAL

These columns aggregate internal write locks.

• COUNT\_WRITE\_EXTERNAL, SUM\_TIMER\_WRITE\_EXTERNAL, MIN\_TIMER\_WRITE\_EXTERNAL, AVG\_TIMER\_WRITE\_EXTERNAL, MAX\_TIMER\_WRITE\_EXTERNAL

These columns aggregate external write locks.

The [table\\_lock\\_waits\\_summary\\_by\\_table](#page-77-0) table has these indexes:

• Unique index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)

TRUNCATE TABLE is permitted for table lock summary tables. It resets the summary columns to zero rather than removing rows.

## <span id="page-79-0"></span>**29.12.20.9 Socket Summary Tables**

These socket summary tables aggregate timer and byte count information for socket operations:

- [socket\\_summary\\_by\\_event\\_name](#page-79-0): Aggregate timer and byte count statistics generated by the wait/io/socket/\* instruments for all socket I/O operations, per socket instrument.
- [socket\\_summary\\_by\\_instance](#page-79-0): Aggregate timer and byte count statistics generated by the wait/io/socket/\* instruments for all socket I/O operations, per socket instance. When a connection terminates, the row in [socket\\_summary\\_by\\_instance](#page-79-0) corresponding to it is deleted.

The socket summary tables do not aggregate waits generated by idle events while sockets are waiting for the next request from the client. For idle event aggregations, use the wait-event summary tables; see [Section 29.12.20.1, "Wait Event Summary Tables"](#page-61-0).

Each socket summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [socket\\_summary\\_by\\_event\\_name](#page-79-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.
- [socket\\_summary\\_by\\_instance](#page-79-0) has an OBJECT\_INSTANCE\_BEGIN column. Each row summarizes events for a given object.

Each socket summary table has these summary columns containing aggregated values:

- COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT These columns aggregate all operations.
- COUNT\_READ, SUM\_TIMER\_READ, MIN\_TIMER\_READ, AVG\_TIMER\_READ, MAX\_TIMER\_READ, SUM\_NUMBER\_OF\_BYTES\_READ

These columns aggregate all receive operations (RECV, RECVFROM, and RECVMSG).

• COUNT\_WRITE, SUM\_TIMER\_WRITE, MIN\_TIMER\_WRITE, AVG\_TIMER\_WRITE, MAX\_TIMER\_WRITE, SUM\_NUMBER\_OF\_BYTES\_WRITE

These columns aggregate all send operations (SEND, SENDTO, and SENDMSG).

• COUNT\_MISC, SUM\_TIMER\_MISC, MIN\_TIMER\_MISC, AVG\_TIMER\_MISC, MAX\_TIMER\_MISC

These columns aggregate all other socket operations, such as CONNECT, LISTEN, ACCEPT, CLOSE, and SHUTDOWN. There are no byte counts for these operations.

The [socket\\_summary\\_by\\_instance](#page-79-0) table also has an EVENT\_NAME column that indicates the class of the socket: client\_connection, server\_tcpip\_socket, server\_unix\_socket. This column can be grouped on to isolate, for example, client activity from that of the server listening sockets.

The socket summary tables have these indexes:

- [socket\\_summary\\_by\\_event\\_name](#page-79-0):
  - Primary key on (EVENT\_NAME)
- [socket\\_summary\\_by\\_instance](#page-79-0):
  - Primary key on (OBJECT\_INSTANCE\_BEGIN)
  - Index on (EVENT\_NAME)

TRUNCATE TABLE is permitted for socket summary tables. Except for [events\\_statements\\_summary\\_by\\_digest](#page-65-0), it resets the summary columns to zero rather than removing rows.

### <span id="page-80-0"></span>**29.12.20.10 Memory Summary Tables**

The Performance Schema instruments memory usage and aggregates memory usage statistics, detailed by these factors:

- Type of memory used (various caches, internal buffers, and so forth)
- Thread, account, user, host indirectly performing the memory operation

The Performance Schema instruments the following aspects of memory use

- Memory sizes used
- Operation counts
- Low and high water marks

Memory sizes help to understand or tune the memory consumption of the server.

Operation counts help to understand or tune the overall pressure the server is putting on the memory allocator, which has an impact on performance. Allocating a single byte one million times is not the same as allocating one million bytes a single time; tracking both sizes and counts can expose the difference.

Low and high water marks are critical to detect workload spikes, overall workload stability, and possible memory leaks.

Memory summary tables do not contain timing information because memory events are not timed.

For information about collecting memory usage data, see [Memory Instrumentation Behavior](#page-82-0).

Example memory event summary information:

```
mysql> SELECT *
 FROM performance_schema.memory_summary_global_by_event_name
 WHERE EVENT_NAME = 'memory/sql/TABLE'\G
*************************** 1. row ***************************
 EVENT_NAME: memory/sql/TABLE
 COUNT_ALLOC: 1381
 COUNT_FREE: 924
 SUM_NUMBER_OF_BYTES_ALLOC: 2059873
 SUM_NUMBER_OF_BYTES_FREE: 1407432
 LOW_COUNT_USED: 0
 CURRENT_COUNT_USED: 457
 HIGH_COUNT_USED: 461
 LOW_NUMBER_OF_BYTES_USED: 0
CURRENT_NUMBER_OF_BYTES_USED: 652441
 HIGH_NUMBER_OF_BYTES_USED: 669269
```

Each memory summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the setup\_instruments table:

- [memory\\_summary\\_by\\_account\\_by\\_event\\_name](#page-80-0) has USER, HOST, and EVENT\_NAME columns. Each row summarizes events for a given account (user and host combination) and event name.
- [memory\\_summary\\_by\\_host\\_by\\_event\\_name](#page-80-0) has HOST and EVENT\_NAME columns. Each row summarizes events for a given host and event name.
- [memory\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-80-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.

- [memory\\_summary\\_by\\_user\\_by\\_event\\_name](#page-80-0) has USER and EVENT\_NAME columns. Each row summarizes events for a given user and event name.
- [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.

Each memory summary table has these summary columns containing aggregated values:

• COUNT\_ALLOC, COUNT\_FREE

The aggregated numbers of calls to memory-allocation and memory-free functions.

• SUM\_NUMBER\_OF\_BYTES\_ALLOC, SUM\_NUMBER\_OF\_BYTES\_FREE

The aggregated sizes of allocated and freed memory blocks.

• CURRENT\_COUNT\_USED

The aggregated number of currently allocated blocks that have not been freed yet. This is a convenience column, equal to COUNT\_ALLOC − COUNT\_FREE.

• CURRENT\_NUMBER\_OF\_BYTES\_USED

The aggregated size of currently allocated memory blocks that have not been freed yet. This is a convenience column, equal to SUM\_NUMBER\_OF\_BYTES\_ALLOC − SUM\_NUMBER\_OF\_BYTES\_FREE.

• LOW\_COUNT\_USED, HIGH\_COUNT\_USED

The low and high water marks corresponding to the CURRENT\_COUNT\_USED column.

• LOW\_NUMBER\_OF\_BYTES\_USED, HIGH\_NUMBER\_OF\_BYTES\_USED

The low and high water marks corresponding to the CURRENT\_NUMBER\_OF\_BYTES\_USED column.

The memory summary tables have these indexes:

- [memory\\_summary\\_by\\_account\\_by\\_event\\_name](#page-80-0):
  - Primary key on (USER, HOST, EVENT\_NAME)
- [memory\\_summary\\_by\\_host\\_by\\_event\\_name](#page-80-0):
  - Primary key on (HOST, EVENT\_NAME)
- [memory\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-80-0):
  - Primary key on (THREAD\_ID, EVENT\_NAME)
- [memory\\_summary\\_by\\_user\\_by\\_event\\_name](#page-80-0):
  - Primary key on (USER, EVENT\_NAME)
- [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0):
  - Primary key on (EVENT\_NAME)

TRUNCATE TABLE is permitted for memory summary tables. It has these effects:

- In general, truncation resets the baseline for statistics, but does not change the server state. That is, truncating a memory table does not free memory.
- COUNT\_ALLOC and COUNT\_FREE are reset to a new baseline, by reducing each counter by the same value.

- Likewise, SUM\_NUMBER\_OF\_BYTES\_ALLOC and SUM\_NUMBER\_OF\_BYTES\_FREE are reset to a new baseline.
- LOW\_COUNT\_USED and HIGH\_COUNT\_USED are reset to CURRENT\_COUNT\_USED.
- LOW\_NUMBER\_OF\_BYTES\_USED and HIGH\_NUMBER\_OF\_BYTES\_USED are reset to CURRENT\_NUMBER\_OF\_BYTES\_USED.

In addition, each memory summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

### <span id="page-82-0"></span>**Memory Instrumentation Behavior**

Memory instruments are listed in the setup\_instruments table and have names of the form memory/code\_area/instrument\_name. Memory instrumentation is enabled by default.

Instruments named with the prefix memory/performance\_schema/ expose how much memory is allocated for internal buffers in the Performance Schema itself. The memory/performance\_schema/ instruments are built in, always enabled, and cannot be disabled at startup or runtime. Built-in memory instruments are displayed only in the [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0) table.

To control memory instrumentation state at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='memory/%=ON'
```

• Disable:

```
[mysqld]
performance-schema-instrument='memory/%=OFF'
```

To control memory instrumentation state at runtime, update the ENABLED column of the relevant instruments in the setup\_instruments table:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES'
WHERE NAME LIKE 'memory/%';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO'
WHERE NAME LIKE 'memory/%';
```

For memory instruments, the TIMED column in setup\_instruments is ignored because memory operations are not timed.

When a thread in the server executes a memory allocation that has been instrumented, these rules apply:

- If the thread is not instrumented or the memory instrument is not enabled, the memory block allocated is not instrumented.
- Otherwise (that is, both the thread and the instrument are enabled), the memory block allocated is instrumented.

For deallocation, these rules apply:

- If a memory allocation operation was instrumented, the corresponding free operation is instrumented, regardless of the current instrument or thread enabled status.
- If a memory allocation operation was not instrumented, the corresponding free operation is not instrumented, regardless of the current instrument or thread enabled status.

For the per-thread statistics, the following rules apply.

When an instrumented memory block of size N is allocated, the Performance Schema makes these updates to memory summary table columns:

- COUNT\_ALLOC: Increased by 1
- CURRENT\_COUNT\_USED: Increased by 1
- HIGH\_COUNT\_USED: Increased if CURRENT\_COUNT\_USED is a new maximum
- SUM\_NUMBER\_OF\_BYTES\_ALLOC: Increased by N
- CURRENT\_NUMBER\_OF\_BYTES\_USED: Increased by N
- HIGH\_NUMBER\_OF\_BYTES\_USED: Increased if CURRENT\_NUMBER\_OF\_BYTES\_USED is a new maximum

When an instrumented memory block is deallocated, the Performance Schema makes these updates to memory summary table columns:

- COUNT\_FREE: Increased by 1
- CURRENT\_COUNT\_USED: Decreased by 1
- LOW\_COUNT\_USED: Decreased if CURRENT\_COUNT\_USED is a new minimum
- SUM\_NUMBER\_OF\_BYTES\_FREE: Increased by N
- CURRENT\_NUMBER\_OF\_BYTES\_USED: Decreased by N
- LOW\_NUMBER\_OF\_BYTES\_USED: Decreased if CURRENT\_NUMBER\_OF\_BYTES\_USED is a new minimum

For higher-level aggregates (global, by account, by user, by host), the same rules apply as expected for low and high water marks.

- LOW\_COUNT\_USED and LOW\_NUMBER\_OF\_BYTES\_USED are lower estimates. The value reported by the Performance Schema is guaranteed to be less than or equal to the lowest count or size of memory effectively used at runtime.
- HIGH\_COUNT\_USED and HIGH\_NUMBER\_OF\_BYTES\_USED are higher estimates. The value reported by the Performance Schema is guaranteed to be greater than or equal to the highest count or size of memory effectively used at runtime.

For lower estimates in summary tables other than [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0), it is possible for values to go negative if memory ownership is transferred between threads.

Here is an example of estimate computation; but note that estimate implementation is subject to change:

Thread 1 uses memory in the range from 1MB to 2MB during execution, as reported by the LOW\_NUMBER\_OF\_BYTES\_USED and HIGH\_NUMBER\_OF\_BYTES\_USED columns of the [memory\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-80-0) table.

Thread 2 uses memory in the range from 10MB to 12MB during execution, as reported likewise.

When these two threads belong to the same user account, the per-account summary estimates that this account used memory in the range from 11MB to 14MB. That is, the LOW\_NUMBER\_OF\_BYTES\_USED for the higher level aggregate is the sum of each LOW\_NUMBER\_OF\_BYTES\_USED (assuming the worst case). Likewise, the HIGH\_NUMBER\_OF\_BYTES\_USED for the higher level aggregate is the sum of each HIGH\_NUMBER\_OF\_BYTES\_USED (assuming the worst case).

11MB is a lower estimate that can occur only if both threads hit the low usage mark at the same time.

14MB is a higher estimate that can occur only if both threads hit the high usage mark at the same time.

The real memory usage for this account could have been in the range from 11.5MB to 13.5MB.

For capacity planning, reporting the worst case is actually the desired behavior, as it shows what can potentially happen when sessions are uncorrelated, which is typically the case.

## <span id="page-84-0"></span>**29.12.20.11 Error Summary Tables**

The Performance Schema maintains summary tables for aggregating statistical information about server errors (and warnings). For a list of server errors, see [Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md).

Collection of error information is controlled by the error instrument, which is enabled by default. Timing information is not collected.

Each error summary table has three columns that identify the error:

- ERROR\_NUMBER is the numeric error value. The value is unique.
- ERROR\_NAME is the symbolic error name corresponding to the ERROR\_NUMBER value. The value is unique.
- SQLSTATE is the SQLSTATE value corresponding to the ERROR\_NUMBER value. The value is not necessarily unique.

For example, if ERROR\_NUMBER is 1050, ERROR\_NAME is [ER\\_TABLE\\_EXISTS\\_ERROR](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_table_exists_error) and SQLSTATE is 42S01.

Example error event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_errors_summary_global_by_error
 WHERE SUM_ERROR_RAISED <> 0\G
*************************** 1. row ***************************
 ERROR_NUMBER: 1064
 ERROR_NAME: ER_PARSE_ERROR
 SQL_STATE: 42000
 SUM_ERROR_RAISED: 1
SUM_ERROR_HANDLED: 0
 FIRST_SEEN: 2016-06-28 07:34:02
 LAST_SEEN: 2016-06-28 07:34:02
*************************** 2. row ***************************
 ERROR_NUMBER: 1146
 ERROR_NAME: ER_NO_SUCH_TABLE
 SQL_STATE: 42S02
 SUM_ERROR_RAISED: 2
SUM_ERROR_HANDLED: 0
 FIRST_SEEN: 2016-06-28 07:34:05
 LAST_SEEN: 2016-06-28 07:36:18
*************************** 3. row ***************************
 ERROR_NUMBER: 1317
 ERROR_NAME: ER_QUERY_INTERRUPTED
 SQL_STATE: 70100
 SUM_ERROR_RAISED: 1
SUM_ERROR_HANDLED: 0
 FIRST_SEEN: 2016-06-28 11:01:49
 LAST_SEEN: 2016-06-28 11:01:49
```

Each error summary table has one or more grouping columns to indicate how the table aggregates errors:

- [events\\_errors\\_summary\\_by\\_account\\_by\\_error](#page-84-0) has USER, HOST, and ERROR\_NUMBER columns. Each row summarizes events for a given account (user and host combination) and error.
- [events\\_errors\\_summary\\_by\\_host\\_by\\_error](#page-84-0) has HOST and ERROR\_NUMBER columns. Each row summarizes events for a given host and error.
- [events\\_errors\\_summary\\_by\\_thread\\_by\\_error](#page-84-0) has THREAD\_ID and ERROR\_NUMBER columns. Each row summarizes events for a given thread and error.
- [events\\_errors\\_summary\\_by\\_user\\_by\\_error](#page-84-0) has USER and ERROR\_NUMBER columns. Each row summarizes events for a given user and error.
- [events\\_errors\\_summary\\_global\\_by\\_error](#page-84-0) has an ERROR\_NUMBER column. Each row summarizes events for a given error.

Each error summary table has these summary columns containing aggregated values:

• SUM\_ERROR\_RAISED

This column aggregates the number of times the error occurred.

• SUM\_ERROR\_HANDLED

This column aggregates the number of times the error was handled by an SQL exception handler.

• FIRST\_SEEN, LAST\_SEEN

Timestamp indicating when the error was first seen and most recently seen.

A NULL row in each error summary table is used to aggregate statistics for all errors that lie out of range of the instrumented errors. For example, if MySQL Server errors lie in the range from M to N and an error is raised with number Q not in that range, the error is aggregated in the NULL row. The NULL row is the row with ERROR\_NUMBER=0, ERROR\_NAME=NULL, and SQLSTATE=NULL.

The error summary tables have these indexes:

- [events\\_errors\\_summary\\_by\\_account\\_by\\_error](#page-84-0):
  - Primary key on (USER, HOST, ERROR\_NUMBER)
- [events\\_errors\\_summary\\_by\\_host\\_by\\_error](#page-84-0):
  - Primary key on (HOST, ERROR\_NUMBER)
- [events\\_errors\\_summary\\_by\\_thread\\_by\\_error](#page-84-0):
  - Primary key on (THREAD\_ID, ERROR\_NUMBER)
- [events\\_errors\\_summary\\_by\\_user\\_by\\_error](#page-84-0):
  - Primary key on (USER, ERROR\_NUMBER)
- [events\\_errors\\_summary\\_global\\_by\\_error](#page-84-0):
  - Primary key on (ERROR\_NUMBER)

TRUNCATE TABLE is permitted for error summary tables. It has these effects:

• For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero or NULL rather than removing rows.

• For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero or NULL for the remaining rows.

In addition, each error summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_errors\\_summary\\_global\\_by\\_error](#page-84-0). For details, see Section 29.12.8, "Performance Schema Connection Tables".

## <span id="page-86-0"></span>**29.12.20.12 Status Variable Summary Tables**

The Performance Schema makes status variable information available in the tables described in [Section 29.12.15, "Performance Schema Status Variable Tables"](#page-47-0). It also makes aggregated status variable information available in summary tables, described here. Each status variable summary table has one or more grouping columns to indicate how the table aggregates status values:

- [status\\_by\\_account](#page-86-0) has USER, HOST, and VARIABLE\_NAME columns to summarize status variables by account.
- [status\\_by\\_host](#page-86-0) has HOST and VARIABLE\_NAME columns to summarize status variables by the host from which clients connected.
- [status\\_by\\_user](#page-86-0) has USER and VARIABLE\_NAME columns to summarize status variables by client user name.

Each status variable summary table has this summary column containing aggregated values:

• VARIABLE\_VALUE

The aggregated status variable value for active and terminated sessions.

The status variable summary tables have these indexes:

- [status\\_by\\_account](#page-86-0):
  - Primary key on (USER, HOST, VARIABLE\_NAME)
- [status\\_by\\_host](#page-86-0):
  - Primary key on (HOST, VARIABLE\_NAME)
- [status\\_by\\_user](#page-86-0):
  - Primary key on (USER, VARIABLE\_NAME)

The meaning of "account" in these tables is similar to its meaning in the MySQL grant tables in the mysql system database, in the sense that the term refers to a combination of user and host values. They differ in that, for grant tables, the host part of an account can be a pattern, whereas for Performance Schema tables, the host value is always a specific nonpattern host name.

Account status is collected when sessions terminate. The session status counters are added to the global status counters and the corresponding account status counters. If account statistics are not collected, the session status is added to host and user status, if host and user status are collected.

Account, host, and user statistics are not collected if the [performance\\_schema\\_accounts\\_size](#page-112-0), [performance\\_schema\\_hosts\\_size](#page-116-0), and [performance\\_schema\\_users\\_size](#page-129-0) system variables, respectively, are set to 0.

The Performance Schema supports TRUNCATE TABLE for status variable summary tables as follows; in all cases, status for active sessions is unaffected:

• [status\\_by\\_account](#page-86-0): Aggregates account status from terminated sessions to user and host status, then resets account status.

- [status\\_by\\_host](#page-86-0): Resets aggregated host status from terminated sessions.
- [status\\_by\\_user](#page-86-0): Resets aggregated user status from terminated sessions.

FLUSH STATUS adds the session status from all active sessions to the global status variables, resets the status of all active sessions, and resets account, host, and user status values aggregated from disconnected sessions.