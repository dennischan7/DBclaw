---
source: MySQL 8.0 Reference
title: 00_Overview
---

![](_page_48_Picture_17.jpeg)

### **Note**

The Performance Schema tables described here are available as of MySQL 8.0.14. Prior to MySQL 8.0.14, use the corresponding INFORMATION\_SCHEMA tables instead; see Section 28.5, "INFORMATION\_SCHEMA Thread Pool Tables".

The following sections describe the Performance Schema tables associated with the thread pool plugin (see Section 7.6.3, "MySQL Enterprise Thread Pool"). They provide information about thread pool operation:

- [tp\\_thread\\_group\\_state](#page-49-0): Information about thread pool thread group states.
- [tp\\_thread\\_group\\_stats](#page-50-0): Thread group statistics.
- [tp\\_thread\\_state](#page-52-0): Information about thread pool thread states.

Rows in these tables represent snapshots in time. In the case of [tp\\_thread\\_state](#page-52-0), all rows for a thread group comprise a snapshot in time. Thus, the MySQL server holds the mutex of the thread

group while producing the snapshot. But it does not hold mutexes on all thread groups at the same time, to prevent a statement against [tp\\_thread\\_state](#page-52-0) from blocking the entire MySQL server.

The Performance Schema thread pool tables are implemented by the thread pool plugin and are loaded and unloaded when that plugin is loaded and unloaded (see Section 7.6.3.2, "Thread Pool Installation"). No special configuration step for the tables is needed. However, the tables depend on the thread pool plugin being enabled. If the thread pool plugin is loaded but disabled, the tables are not created.

### <span id="page-49-0"></span>**29.12.16.1 The tp\_thread\_group\_state Table**

![](_page_49_Picture_4.jpeg)

### **Note**

The Performance Schema table described here is available as of MySQL 8.0.14. Prior to MySQL 8.0.14, use the corresponding INFORMATION\_SCHEMA table instead; see Section 28.5.2, "The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATE Table".

The [tp\\_thread\\_group\\_state](#page-49-0) table has one row per thread group in the thread pool. Each row provides information about the current state of a group.

The [tp\\_thread\\_group\\_state](#page-49-0) table has these columns:

• TP\_GROUP\_ID

The thread group ID. This is a unique key within the table.

• CONSUMER THREADS

The number of consumer threads. There is at most one thread ready to start executing if the active threads become stalled or blocked.

• RESERVE\_THREADS

The number of threads in the reserved state. This means that they are not started until there is a need to wake a new thread and there is no consumer thread. This is where most threads end up when the thread group has created more threads than needed for normal operation. Often a thread group needs additional threads for a short while and then does not need them again for a while. In this case, they go into the reserved state and remain until needed again. They take up some extra memory resources, but no extra computing resources.

• CONNECT\_THREAD\_COUNT

The number of threads that are processing or waiting to process connection initialization and authentication. There can be a maximum of four connection threads per thread group; these threads expire after a period of inactivity.

• CONNECTION\_COUNT

The number of connections using this thread group.

• QUEUED\_QUERIES

The number of statements waiting in the high-priority queue.

• QUEUED\_TRANSACTIONS

The number of statements waiting in the low-priority queue. These are the initial statements for transactions that have not started, so they also represent queued transactions.

• STALL\_LIMIT

The value of the thread\_pool\_stall\_limit system variable for the thread group. This is the same value for all thread groups.

• PRIO\_KICKUP\_TIMER

The value of the thread\_pool\_prio\_kickup\_timer system variable for the thread group. This is the same value for all thread groups.

• ALGORITHM

The value of the thread\_pool\_algorithm system variable for the thread group. This is the same value for all thread groups.

• THREAD\_COUNT

The number of threads started in the thread pool as part of this thread group.

• ACTIVE\_THREAD\_COUNT

The number of threads active in executing statements.

• STALLED\_THREAD\_COUNT

The number of stalled statements in the thread group. A stalled statement could be executing, but from a thread pool perspective it is stalled and making no progress. A long-running statement quickly ends up in this category.

• WAITING\_THREAD\_NUMBER

If there is a thread handling the polling of statements in the thread group, this specifies the thread number within this thread group. It is possible that this thread could be executing a statement.

• OLDEST\_QUEUED

How long in milliseconds the oldest queued statement has been waiting for execution.

• MAX\_THREAD\_IDS\_IN\_GROUP

The maximum thread ID of the threads in the group. This is the same as MAX(TP\_THREAD\_NUMBER) for the threads when selected from the [tp\\_thread\\_state](#page-52-0) table. That is, these two queries are equivalent:

```
SELECT TP_GROUP_ID, MAX_THREAD_IDS_IN_GROUP
FROM tp_thread_group_state;
SELECT TP_GROUP_ID, MAX(TP_THREAD_NUMBER)
FROM tp_thread_state GROUP BY TP_GROUP_ID;
```

The [tp\\_thread\\_group\\_state](#page-49-0) table has these indexes:

• Unique index on (TP\_GROUP\_ID)

TRUNCATE TABLE is not permitted for the [tp\\_thread\\_group\\_state](#page-49-0) table.

### <span id="page-50-0"></span>**29.12.16.2 The tp\_thread\_group\_stats Table**

![](_page_50_Picture_23.jpeg)

#### **Note**

The Performance Schema table described here is available as of MySQL 8.0.14. Prior to MySQL 8.0.14, use the corresponding INFORMATION\_SCHEMA table instead; see Section 28.5.3, "The INFORMATION\_SCHEMA TP\_THREAD\_GROUP\_STATS Table".

The [tp\\_thread\\_group\\_stats](#page-50-0) table reports statistics per thread group. There is one row per group.

The [tp\\_thread\\_group\\_stats](#page-50-0) table has these columns:

• TP\_GROUP\_ID

The thread group ID. This is a unique key within the table.

• CONNECTIONS\_STARTED

The number of connections started.

• CONNECTIONS\_CLOSED

The number of connections closed.

• QUERIES\_EXECUTED

The number of statements executed. This number is incremented when a statement starts executing, not when it finishes.

• QUERIES\_QUEUED

The number of statements received that were queued for execution. This does not count statements that the thread group was able to begin executing immediately without queuing, which can happen under the conditions described in Section 7.6.3.3, "Thread Pool Operation".

• THREADS\_STARTED

The number of threads started.

• PRIO\_KICKUPS

The number of statements that have been moved from low-priority queue to high-priority queue based on the value of the thread\_pool\_prio\_kickup\_timer system variable. If this number increases quickly, consider increasing the value of that variable. A quickly increasing counter means that the priority system is not keeping transactions from starting too early. For InnoDB, this most likely means deteriorating performance due to too many concurrent transactions..

• STALLED\_QUERIES\_EXECUTED

The number of statements that have become defined as stalled due to executing for longer than the value of the thread\_pool\_stall\_limit system variable.

• BECOME\_CONSUMER\_THREAD

The number of times thread have been assigned the consumer thread role.

• BECOME\_RESERVE\_THREAD

The number of times threads have been assigned the reserve thread role.

• BECOME\_WAITING\_THREAD

The number of times threads have been assigned the waiter thread role. When statements are queued, this happens very often, even in normal operation, so rapid increases in this value are normal in the case of a highly loaded system where statements are queued up.

• WAKE\_THREAD\_STALL\_CHECKER

The number of times the stall check thread decided to wake or create a thread to possibly handle some statements or take care of the waiter thread role.

• SLEEP\_WAITS

The number of THD\_WAIT\_SLEEP waits. These occur when threads go to sleep (for example, by calling the SLEEP() function).

• DISK\_IO\_WAITS

The number of THD\_WAIT\_DISKIO waits. These occur when threads perform disk I/O that is likely to not hit the file system cache. Such waits occur when the buffer pool reads and writes data to disk, not for normal reads from and writes to files.

• ROW\_LOCK\_WAITS

The number of THD\_WAIT\_ROW\_LOCK waits for release of a row lock by another transaction.

• GLOBAL\_LOCK\_WAITS

The number of THD\_WAIT\_GLOBAL\_LOCK waits for a global lock to be released.

• META\_DATA\_LOCK\_WAITS

The number of THD\_WAIT\_META\_DATA\_LOCK waits for a metadata lock to be released.

• TABLE\_LOCK\_WAITS

The number of THD\_WAIT\_TABLE\_LOCK waits for a table to be unlocked that the statement needs to access.

• USER\_LOCK\_WAITS

The number of THD\_WAIT\_USER\_LOCK waits for a special lock constructed by the user thread.

• BINLOG\_WAITS

The number of THD\_WAIT\_BINLOG\_WAITS waits for the binary log to become free.

• GROUP\_COMMIT\_WAITS

The number of THD\_WAIT\_GROUP\_COMMIT waits. These occur when a group commit must wait for the other parties to complete their part of a transaction.

• FSYNC\_WAITS

The number of THD\_WAIT\_SYNC waits for a file sync operation.

The [tp\\_thread\\_group\\_stats](#page-50-0) table has these indexes:

• Unique index on (TP\_GROUP\_ID)

TRUNCATE TABLE is not permitted for the [tp\\_thread\\_group\\_stats](#page-50-0) table.

### <span id="page-52-0"></span>**29.12.16.3 The tp\_thread\_state Table**

![](_page_52_Picture_24.jpeg)

### **Note**

The Performance Schema table described here is available as of MySQL 8.0.14. Prior to MySQL 8.0.14, use the corresponding INFORMATION\_SCHEMA table instead; see Section 28.5.4, "The INFORMATION\_SCHEMA TP\_THREAD\_STATE Table".

The [tp\\_thread\\_state](#page-52-0) table has one row per thread created by the thread pool to handle connections.

The [tp\\_thread\\_state](#page-52-0) table has these columns:

• TP\_GROUP\_ID

The thread group ID.

• TP\_THREAD\_NUMBER

The ID of the thread within its thread group. TP\_GROUP\_ID and TP\_THREAD\_NUMBER together provide a unique key within the table.

• PROCESS\_COUNT

The 10ms interval in which the statement that uses this thread is currently executing. 0 means no statement is executing, 1 means it is in the first 10ms, and so forth.

• WAIT\_TYPE

The type of wait for the thread. NULL means the thread is not blocked. Otherwise, the thread is blocked by a call to thd\_wait\_begin() and the value specifies the type of wait. The xxx\_WAIT columns of the [tp\\_thread\\_group\\_stats](#page-50-0) table accumulate counts for each wait type.

The WAIT\_TYPE value is a string that describes the type of wait, as shown in the following table.

**Table 29.6 tp\_thread\_state Table WAIT\_TYPE Values**

| Wait Type               | Meaning                   |
|-------------------------|---------------------------|
| THD_WAIT_SLEEP          | Waiting for sleep         |
| THD_WAIT_DISKIO         | Waiting for Disk IO       |
| THD_WAIT_ROW_LOCK       | Waiting for row lock      |
| THD_WAIT_GLOBAL_LOCK    | Waiting for global lock   |
| THD_WAIT_META_DATA_LOCK | Waiting for metadata lock |
| THD_WAIT_TABLE_LOCK     | Waiting for table lock    |
| THD_WAIT_USER_LOCK      | Waiting for user lock     |
| THD_WAIT_BINLOG         | Waiting for binlog        |
| THD_WAIT_GROUP_COMMIT   | Waiting for group commit  |
| THD_WAIT_SYNC           | Waiting for fsync         |

• TP\_THREAD\_TYPE

The type of thread. The value shown in this column is one of CONNECTION\_HANDLER\_WORKER\_THREAD, LISTENER\_WORKER\_THREAD, QUERY\_WORKER\_THREAD, or TIMER\_WORKER\_THREAD.

This column was added in MySQL 8.0.32.

• THREAD\_ID

This thread's unique identifier. The value is the same as that used in the THREAD\_ID column of the Performance Schema [threads](#page-99-0) table.

This column was added in MySQL 8.0.32.

The [tp\\_thread\\_state](#page-52-0) table has these indexes:

• Unique index on (TP\_GROUP\_ID, TP\_THREAD\_NUMBER)

TRUNCATE TABLE is not permitted for the [tp\\_thread\\_state](#page-52-0) table.