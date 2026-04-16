---
source: MySQL 5.7 Reference
title: 00_Overview
---

Summary tables provide aggregated information for terminated events over time. The tables in this group summarize event data in different ways.

Each summary table has grouping columns that determine how to group the data to be aggregated, and summary columns that contain the aggregated values. Tables that summarize events in similar ways often have similar sets of summary columns and differ only in the grouping columns used to determine how events are aggregated.

Summary tables can be truncated with TRUNCATE TABLE. Generally, the effect is to reset the summary columns to 0 or NULL, not to remove rows. This enables you to clear collected values and restart aggregation. That might be useful, for example, after you have made a runtime configuration change. Exceptions to this truncation behavior are noted in individual summary table sections.

## **Wait Event Summaries**

**Table 25.3 Performance Schema Wait Event Summary Tables**

| Table Name                                                                           | Description              |
|--------------------------------------------------------------------------------------|--------------------------|
| events_waits_summary_by_account_by_event_name Wait events per account and event name |                          |
| events_waits_summary_by_host_by_event_name Wait events per host name and event name  |                          |
| events_waits_summary_by_instance                                                     | Wait events per instance |
| events_waits_summary_by_thread_by_event_name Wait events per thread and event name   |                          |
| events_waits_summary_by_user_by_event_name Wait events per user name and event name  |                          |
| events_waits_summary_global_by_event_name Wait events per event name                 |                          |

## **Stage Summaries**

**Table 25.4 Performance Schema Stage Event Summary Tables**

| Table Name                                                                            | Description                             |
|---------------------------------------------------------------------------------------|-----------------------------------------|
| events_stages_summary_by_account_by_event_name                                        | Stage events per account and event name |
| events_stages_summary_by_host_by_event_name Stage events per host name and event name |                                         |
| events_stages_summary_by_thread_by_event_name Stage waits per thread and event name   |                                         |
| events_stages_summary_by_user_by_event_name Stage events per user name and event name |                                         |
| events_stages_summary_global_by_event_name Stage waits per event name                 |                                         |

## **Statement Summaries**

**Table 25.5 Performance Schema Statement Event Summary Tables**

| Table Name                                         | Description                                   |
|----------------------------------------------------|-----------------------------------------------|
| events_statements_summary_by_account_by_event_name | Statement events per account and event name   |
| events_statements_summary_by_digest                | Statement events per schema and digest value  |
| events_statements_summary_by_host_by_event_name    | Statement events per host name and event name |
| events_statements_summary_by_program               | Statement events per stored program           |
| events_statements_summary_by_thread_by_event_name  | Statement events per thread and event name    |
| events_statements_summary_by_user_by_event_name    | Statement events per user name and event name |
| events_statements_summary_global_by_event_name     | Statement events per event name               |
| prepared_statements_instances                      | Prepared statement instances and statistics   |

## **Transaction Summaries**

**Table 25.6 Performance Schema Transaction Event Summary Tables**

| Table Name                                           | Description                                        |
|------------------------------------------------------|----------------------------------------------------|
| events_transactions_summary_by_account_by_event_name | Transaction events per account and event name      |
| events_transactions_summary_by_host_by_event_name    | Transaction events per host name and event<br>name |
| events_transactions_summary_by_thread_by_event_name  | Transaction events per thread and event name       |
| events_transactions_summary_by_user_by_event_name    | Transaction events per user name and event<br>name |

| Table Name                                       | Description                       |
|--------------------------------------------------|-----------------------------------|
| events_transactions_summary_global_by_event_name | Transaction events per event name |

## **Object Wait Summaries**

#### **Table 25.7 Performance Schema Object Event Summary Tables**

| Table Name                     | Description      |
|--------------------------------|------------------|
| objects_summary_global_by_type | Object summaries |

## **File I/O Summaries**

#### **Table 25.8 Performance Schema File I/O Event Summary Tables**

| Table Name                 | Description                   |
|----------------------------|-------------------------------|
| file_summary_by_event_name | File events per event name    |
| file_summary_by_instance   | File events per file instance |

## **Table I/O and Lock Wait Summaries**

#### **Table 25.9 Performance Schema Table I/O and Lock Wait Event Summary Tables**

| Table Name                            | Description                |
|---------------------------------------|----------------------------|
| table_io_waits_summary_by_index_usage | Table I/O waits per index  |
| table_io_waits_summary_by_table       | Table I/O waits per table  |
| table_lock_waits_summary_by_table     | Table lock waits per table |

## **Socket Summaries**

#### **Table 25.10 Performance Schema Socket Event Summary Tables**

| Table Name                   | Description                         |
|------------------------------|-------------------------------------|
| socket_summary_by_event_name | Socket waits and I/O per event name |
| socket_summary_by_instance   | Socket waits and I/O per instance   |

## **Memory Summaries**

#### **Table 25.11 Performance Schema Memory Operation Summary Tables**

| Table Name                                                                          | Description                               |
|-------------------------------------------------------------------------------------|-------------------------------------------|
| memory_summary_by_account_by_event_nameMemory operations per account and event name |                                           |
| memory_summary_by_host_by_event_name                                                | Memory operations per host and event name |
| memory_summary_by_thread_by_event_nameMemory operations per thread and event name   |                                           |
| memory_summary_by_user_by_event_name                                                | Memory operations per user and event name |
| memory_summary_global_by_event_name                                                 | Memory operations globally per event name |

# **Status Variable Summaries**

#### **Table 25.12 Performance Schema Error Status Variable Summary Tables**

| Table Name        | Description                            |
|-------------------|----------------------------------------|
| status_by_account | Session status variables per account   |
| status_by_host    | Session status variables per host name |

| Table Name     | Description                            |
|----------------|----------------------------------------|
| status_by_user | Session status variables per user name |

## <span id="page-76-0"></span>**25.12.15.1 Wait Event Summary Tables**

The Performance Schema maintains tables for collecting current and recent wait events, and aggregates that information in summary tables. [Section 25.12.4, "Performance Schema Wait Event](#page-21-0) [Tables"](#page-21-0) describes the events on which wait summaries are based. See that discussion for information about the content of wait events, the current and recent wait event tables, and how to control wait event collection, which is disabled by default.

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

Each wait event summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the [setup\\_instruments](#page-13-0) table:

- [events\\_waits\\_summary\\_by\\_account\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_waits\\_summary\\_by\\_host\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_waits\\_summary\\_by\\_instance](#page-76-0) has EVENT\_NAME and OBJECT\_INSTANCE\_BEGIN columns. Each row summarizes events for a given event name and object. If an instrument is used to create multiple instances, each instance has a unique OBJECT\_INSTANCE\_BEGIN value and is summarized separately in this table.
- [events\\_waits\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-76-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_waits\\_summary\\_by\\_user\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-76-0) has an EVENT\_NAME column. Each row summarizes events for a given event name. An instrument might be used to create multiple instances of the instrumented object. For example, if there is an instrument for a mutex that is created for each connection, there are as many instances as there are connections. The summary row for the instrument summarizes over all these instances.

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

TRUNCATE TABLE is permitted for wait summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each wait summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-76-0). For details, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

## <span id="page-77-0"></span>**25.12.15.2 Stage Summary Tables**

The Performance Schema maintains tables for collecting current and recent stage events, and aggregates that information in summary tables. [Section 25.12.5, "Performance Schema Stage Event](#page-26-1) [Tables"](#page-26-1) describes the events on which stage summaries are based. See that discussion for information about the content of stage events, the current and historical stage event tables, and how to control stage event collection, which is disabled by default.

Example stage event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_stages_summary_global_by_event_name\G
...
*************************** 5. row ***************************
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

Each stage summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the [setup\\_instruments](#page-13-0) table:

- [events\\_stages\\_summary\\_by\\_account\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_stages\\_summary\\_by\\_host\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_stages\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-77-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_stages\\_summary\\_by\\_user\\_by\\_event\\_name](#page-77-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_stages\\_summary\\_global\\_by\\_event\\_name](#page-77-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.

Each stage summary table has these summary columns containing aggregated values: COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, and MAX\_TIMER\_WAIT. These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 25.12.15.1, "Wait Event Summary Tables"](#page-76-0)), except that the stage summary tables aggregate events from [events\\_stages\\_current](#page-30-0) rather than [events\\_waits\\_current](#page-23-0).

TRUNCATE TABLE is permitted for stage summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each stage summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_stages\\_summary\\_global\\_by\\_event\\_name](#page-77-0). For details, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

## <span id="page-78-0"></span>**25.12.15.3 Statement Summary Tables**

The Performance Schema maintains tables for collecting current and recent statement events, and aggregates that information in summary tables. [Section 25.12.6, "Performance Schema Statement](#page-32-0) [Event Tables"](#page-32-0) describes the events on which statement summaries are based. See that discussion for information about the content of statement events, the current and historical statement event tables, and how to control statement event collection, which is partially disabled by default.

Example statement event summary information:

```
mysql> SELECT *
 FROM performance_schema.events_statements_summary_global_by_event_name\G
*************************** 1. row ***************************
 EVENT_NAME: statement/sql/select
 COUNT_STAR: 25
 SUM_TIMER_WAIT: 1535983999000
 MIN_TIMER_WAIT: 209823000
 AVG_TIMER_WAIT: 61439359000
 MAX_TIMER_WAIT: 1363397650000
 SUM_LOCK_TIME: 20186000000
 SUM_ERRORS: 0
 SUM_WARNINGS: 0
 SUM_ROWS_AFFECTED: 0
 SUM_ROWS_SENT: 388
 SUM_ROWS_EXAMINED: 370
SUM_CREATED_TMP_DISK_TABLES: 0
 SUM_CREATED_TMP_TABLES: 0
 SUM_SELECT_FULL_JOIN: 0
 SUM_SELECT_FULL_RANGE_JOIN: 0
```

```
 SUM_SELECT_RANGE: 0
 SUM_SELECT_RANGE_CHECK: 0
 SUM_SELECT_SCAN: 6
 SUM_SORT_MERGE_PASSES: 0
 SUM_SORT_RANGE: 0
 SUM_SORT_ROWS: 0
 SUM_SORT_SCAN: 0
 SUM_NO_INDEX_USED: 6
 SUM_NO_GOOD_INDEX_USED: 0
...
```

Each statement summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the [setup\\_instruments](#page-13-0) table:

- [events\\_statements\\_summary\\_by\\_account\\_by\\_event\\_name](#page-78-0) has EVENT\_NAME, USER, and HOST columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_statements\\_summary\\_by\\_digest](#page-78-0) has SCHEMA\_NAME and DIGEST columns. Each row summarizes events per schema and digest value. (The DIGEST\_TEXT column contains the corresponding normalized statement digest text, but is neither a grouping nor a summary column.)

The maximum number of rows in the table is autosized at server startup. To set this maximum explicitly, set the [performance\\_schema\\_digests\\_size](#page-110-0) system variable at server startup.

- [events\\_statements\\_summary\\_by\\_host\\_by\\_event\\_name](#page-78-0) has EVENT\_NAME and HOST columns. Each row summarizes events for a given host and event name.
- [events\\_statements\\_summary\\_by\\_program](#page-78-0) has OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME columns. Each row summarizes events for a given stored program (stored procedure or function, trigger, or event).
- [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-78-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.
- [events\\_statements\\_summary\\_by\\_user\\_by\\_event\\_name](#page-78-0) has EVENT\_NAME and USER columns. Each row summarizes events for a given user and event name.
- [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-78-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.
- [prepared\\_statements\\_instances](#page-40-0) has an OBJECT\_INSTANCE\_BEGIN column. Each row summarizes events for a given prepared statement.

Each statement summary table has these summary columns containing aggregated values (with exceptions as noted):

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 25.12.15.1, "Wait Event Summary Tables"\)](#page-76-0), except that the statement summary tables aggregate events from [events\\_statements\\_current](#page-36-0) rather than [events\\_waits\\_current](#page-23-0).

The [prepared\\_statements\\_instances](#page-40-0) table does not have these columns.

• SUM\_xxx

The aggregate of the corresponding xxx column in the [events\\_statements\\_current](#page-36-0) table. For example, the SUM\_LOCK\_TIME and SUM\_ERRORS columns in statement summary tables are the aggregates of the LOCK\_TIME and ERRORS columns in [events\\_statements\\_current](#page-36-0) table.

The [events\\_statements\\_summary\\_by\\_digest](#page-78-0) table has these additional summary columns:

• FIRST\_SEEN, LAST\_SEEN

Timestamps indicating when statements with the given digest value were first seen and most recently seen.

The [events\\_statements\\_summary\\_by\\_program](#page-78-0) table has these additional summary columns:

• COUNT\_STATEMENTS, SUM\_STATEMENTS\_WAIT, MIN\_STATEMENTS\_WAIT, AVG\_STATEMENTS\_WAIT, MAX\_STATEMENTS\_WAIT

Statistics about nested statements invoked during stored program execution.

The [prepared\\_statements\\_instances](#page-40-0) table has these additional summary columns:

• COUNT\_EXECUTE, SUM\_TIMER\_EXECUTE, MIN\_TIMER\_EXECUTE, AVG\_TIMER\_EXECUTE, MAX\_TIMER\_EXECUTE

Aggregated statistics for executions of the prepared statement.

TRUNCATE TABLE is permitted for statement summary tables. It has these effects:

- For [events\\_statements\\_summary\\_by\\_digest](#page-78-0), it removes the rows.
- For other summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For other summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each statement summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-78-0). For details, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

#### **Statement Digest Aggregation Rules**

If the statements\_digest consumer is enabled, aggregation into [events\\_statements\\_summary\\_by\\_digest](#page-78-0) occurs as follows when a statement completes. Aggregation is based on the DIGEST value computed for the statement.

- If a [events\\_statements\\_summary\\_by\\_digest](#page-78-0) row already exists with the digest value for the statement that just completed, statistics for the statement are aggregated to that row. The LAST\_SEEN column is updated to the current time.
- If no row has the digest value for the statement that just completed, and the table is not full, a new row is created for the statement. The FIRST\_SEEN and LAST\_SEEN columns are initialized with the current time.
- If no row has the statement digest value for the statement that just completed, and the table is full, the statistics for the statement that just completed are added to a special "catch-all" row with DIGEST = NULL, which is created if necessary. If the row is created, the FIRST\_SEEN and LAST\_SEEN columns are initialized with the current time. Otherwise, the LAST\_SEEN column is updated with the current time.

The row with DIGEST = NULL is maintained because Performance Schema tables have a maximum size due to memory constraints. The DIGEST = NULL row permits digests that do not match other rows to be counted even if the summary table is full, using a common "other" bucket. This row helps you estimate whether the digest summary is representative:

• A DIGEST = NULL row that has a COUNT\_STAR value that represents 5% of all digests shows that the digest summary table is very representative; the other rows cover 95% of the statements seen. • A DIGEST = NULL row that has a COUNT\_STAR value that represents 50% of all digests shows that the digest summary table is not very representative; the other rows cover only half the statements seen. Most likely the DBA should increase the maximum table size so that more of the rows counted in the DIGEST = NULL row would be counted using more specific rows instead. By default, the table is autosized, but if this size is too small, set the [performance\\_schema\\_digests\\_size](#page-110-0) system variable to a larger value at server startup.

### **Stored Program Instrumentation Behavior**

For stored program types for which instrumentation is enabled in the [setup\\_objects](#page-14-0) table, [events\\_statements\\_summary\\_by\\_program](#page-78-0) maintains statistics for stored programs as follows:

- A row is added for an object when it is first used in the server.
- The row for an object is removed when the object is dropped.
- Statistics are aggregated in the row for an object as it executes.

See also Section 25.4.3, "Event Pre-Filtering".

## <span id="page-81-0"></span>**25.12.15.4 Transaction Summary Tables**

The Performance Schema maintains tables for collecting current and recent transaction events, and aggregates that information in summary tables. [Section 25.12.7, "Performance Schema Transaction](#page-42-0) [Tables"](#page-42-0) describes the events on which transaction summaries are based. See that discussion for information about the content of transaction events, the current and historical transaction event tables, and how to control transaction event collection, which is disabled by default.

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
MIN_TIMER_READ_WRITE: 2954148000
AVG_TIMER_READ_WRITE: 3910018000
MAX_TIMER_READ_WRITE: 5486275000
 COUNT_READ_ONLY: 0
 SUM_TIMER_READ_ONLY: 0
 MIN_TIMER_READ_ONLY: 0
 AVG_TIMER_READ_ONLY: 0
 MAX_TIMER_READ_ONLY: 0
```

Each transaction summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the [setup\\_instruments](#page-13-0) table:

- [events\\_transactions\\_summary\\_by\\_account\\_by\\_event\\_name](#page-81-0) has USER, HOST, and EVENT\_NAME columns. Each row summarizes events for a given account (user and host combination) and event name.
- [events\\_transactions\\_summary\\_by\\_host\\_by\\_event\\_name](#page-81-0) has HOST and EVENT\_NAME columns. Each row summarizes events for a given host and event name.
- [events\\_transactions\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-81-0) has THREAD\_ID and EVENT\_NAME columns. Each row summarizes events for a given thread and event name.

- [events\\_transactions\\_summary\\_by\\_user\\_by\\_event\\_name](#page-81-0) has USER and EVENT\_NAME columns. Each row summarizes events for a given user and event name.
- [events\\_transactions\\_summary\\_global\\_by\\_event\\_name](#page-81-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.

Each transaction summary table has these summary columns containing aggregated values:

• COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT

These columns are analogous to the columns of the same names in the wait event summary tables (see [Section 25.12.15.1, "Wait Event Summary Tables"\)](#page-76-0), except that the transaction summary tables aggregate events from [events\\_transactions\\_current](#page-46-0) rather than [events\\_waits\\_current](#page-23-0). These columns summarize read-write and read-only transactions.

• COUNT\_READ\_WRITE, SUM\_TIMER\_READ\_WRITE, MIN\_TIMER\_READ\_WRITE, AVG\_TIMER\_READ\_WRITE, MAX\_TIMER\_READ\_WRITE

These are similar to the COUNT\_STAR and xxx\_TIMER\_WAIT columns, but summarize read-write transactions only. The transaction access mode specifies whether transactions operate in read/write or read-only mode.

• COUNT\_READ\_ONLY, SUM\_TIMER\_READ\_ONLY, MIN\_TIMER\_READ\_ONLY, AVG\_TIMER\_READ\_ONLY, MAX\_TIMER\_READ\_ONLY

These are similar to the COUNT\_STAR and xxx\_TIMER\_WAIT columns, but summarize read-only transactions only. The transaction access mode specifies whether transactions operate in read/write or read-only mode.

TRUNCATE TABLE is permitted for transaction summary tables. It has these effects:

- For summary tables not aggregated by account, host, or user, truncation resets the summary columns to zero rather than removing rows.
- For summary tables aggregated by account, host, or user, truncation removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows.

In addition, each transaction summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends, or truncation of [events\\_transactions\\_summary\\_global\\_by\\_event\\_name](#page-81-0). For details, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

#### **Transaction Aggregation Rules**

Transaction event collection occurs without regard to isolation level, access mode, or autocommit mode.

Transaction event collection occurs for all non-aborted transactions initiated by the server, including empty transactions.

Read-write transactions are generally more resource intensive than read-only transactions, therefore transaction summary tables include separate aggregate columns for read-write and read-only transactions.

Resource requirements may also vary with transaction isolation level. However, presuming that only one isolation level would be used per server, aggregation by isolation level is not provided.

## <span id="page-82-0"></span>**25.12.15.5 Object Wait Summary Table**

The Performance Schema maintains the [objects\\_summary\\_global\\_by\\_type](#page-82-0) table for aggregating object wait events.

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
MIN_TIMER_WAIT: 1141704
AVG_TIMER_WAIT: 26111769
MAX_TIMER_WAIT: 334783032
...
```

The [objects\\_summary\\_global\\_by\\_type](#page-82-0) table has these grouping columns to indicate how the table aggregates events: OBJECT\_TYPE, OBJECT\_SCHEMA, and OBJECT\_NAME. Each row summarizes events for the given object.

```
objects_summary_global_by_type has the same summary columns as the
events_waits_summary_by_xxx tables. See Section 25.12.15.1, "Wait Event Summary Tables".
```

TRUNCATE TABLE is permitted for the object summary table. It resets the summary columns to zero rather than removing rows.

## <span id="page-83-0"></span>**25.12.15.6 File I/O Summary Tables**

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

Each file I/O summary table has one or more grouping columns to indicate how the table aggregates events. Event names refer to names of event instruments in the [setup\\_instruments](#page-13-0) table:

- [file\\_summary\\_by\\_event\\_name](#page-83-0) has an EVENT\_NAME column. Each row summarizes events for a given event name.
- [file\\_summary\\_by\\_instance](#page-83-0) has FILE\_NAME, EVENT\_NAME, and OBJECT\_INSTANCE\_BEGIN columns. Each row summarizes events for a given file and event name.

Each file I/O summary table has the following summary columns containing aggregated values. Some columns are more general and have values that are the same as the sum of the values of more finegrained columns. In this way, aggregations at higher levels are available directly without the need for user-defined views that sum lower-level columns.

- COUNT\_STAR, SUM\_TIMER\_WAIT, MIN\_TIMER\_WAIT, AVG\_TIMER\_WAIT, MAX\_TIMER\_WAIT These columns aggregate all I/O operations.
- COUNT\_READ, SUM\_TIMER\_READ, MIN\_TIMER\_READ, AVG\_TIMER\_READ, MAX\_TIMER\_READ, SUM\_NUMBER\_OF\_BYTES\_READ

These columns aggregate all read operations, including FGETS, FGETC, FREAD, and READ.

• COUNT\_WRITE, SUM\_TIMER\_WRITE, MIN\_TIMER\_WRITE, AVG\_TIMER\_WRITE, MAX\_TIMER\_WRITE, SUM\_NUMBER\_OF\_BYTES\_WRITE

These columns aggregate all write operations, including FPUTS, FPUTC, FPRINTF, VFPRINTF, FWRITE, and PWRITE.

• COUNT\_MISC, SUM\_TIMER\_MISC, MIN\_TIMER\_MISC, AVG\_TIMER\_MISC, MAX\_TIMER\_MISC

These columns aggregate all other I/O operations, including CREATE, DELETE, OPEN, CLOSE, STREAM\_OPEN, STREAM\_CLOSE, SEEK, TELL, FLUSH, STAT, FSTAT, CHSIZE, RENAME, and SYNC. There are no byte counts for these operations.

TRUNCATE TABLE is permitted for file I/O summary tables. It resets the summary columns to zero rather than removing rows.

The MySQL server uses several techniques to avoid I/O operations by caching information read from files, so it is possible that statements you might expect to result in I/O events do not do so. You may be able to ensure that I/O does occur by flushing caches or restarting the server to reset its state.