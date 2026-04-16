---
source: MySQL 5.7 Reference
title: 00_Overview
---

Instance tables document what types of objects are instrumented. They provide event names and explanatory notes or status information:

- [cond\\_instances](#page-16-0): Condition synchronization object instances
- [file\\_instances](#page-17-0): File instances
- [mutex\\_instances](#page-17-1): Mutex synchronization object instances
- [rwlock\\_instances](#page-18-0): Lock synchronization object instances
- [socket\\_instances](#page-19-0): Active connection instances

These tables list instrumented synchronization objects, files, and connections. There are three types of synchronization objects: cond, mutex, and rwlock. Each instance table has an EVENT\_NAME or NAME column to indicate the instrument associated with each row. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

The mutex\_instances.LOCKED\_BY\_THREAD\_ID and rwlock\_instances.WRITE\_LOCKED\_BY\_THREAD\_ID columns are extremely important for investigating performance bottlenecks or deadlocks. For examples of how to use them for this purpose, see [Section 25.19, "Using the Performance Schema to Diagnose Problems"](#page-129-0)

## <span id="page-16-0"></span>**25.12.3.1 The cond\_instances Table**

The [cond\\_instances](#page-16-0) table lists all the conditions seen by the Performance Schema while the server executes. A condition is a synchronization mechanism used in the code to signal that a specific event has happened, so that a thread waiting for this condition can resume work.

When a thread is waiting for something to happen, the condition name is an indication of what the thread is waiting for, but there is no immediate way to tell which other threads cause the condition to happen.

The [cond\\_instances](#page-16-0) table has these columns:

• NAME

The instrument name associated with the condition.

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the instrumented condition.

TRUNCATE TABLE is not permitted for the [cond\\_instances](#page-16-0) table.

## <span id="page-17-0"></span>**25.12.3.2 The file\_instances Table**

The [file\\_instances](#page-17-0) table lists all the files seen by the Performance Schema when executing file I/ O instrumentation. If a file on disk has never been opened, it is not in [file\\_instances](#page-17-0). When a file is deleted from the disk, it is also removed from the [file\\_instances](#page-17-0) table.

The [file\\_instances](#page-17-0) table has these columns:

• FILE\_NAME

The file name.

• EVENT\_NAME

The instrument name associated with the file.

• OPEN\_COUNT

The count of open handles on the file. If a file was opened and then closed, it was opened 1 time, but OPEN\_COUNT is 0. To list all the files currently opened by the server, use WHERE OPEN\_COUNT > 0.

TRUNCATE TABLE is not permitted for the [file\\_instances](#page-17-0) table.

## <span id="page-17-1"></span>**25.12.3.3 The mutex\_instances Table**

The [mutex\\_instances](#page-17-1) table lists all the mutexes seen by the Performance Schema while the server executes. A mutex is a synchronization mechanism used in the code to enforce that only one thread at a given time can have access to some common resource. The resource is said to be "protected" by the mutex.

When two threads executing in the server (for example, two user sessions executing a query simultaneously) do need to access the same resource (a file, a buffer, or some piece of data), these two threads compete against each other, so that the first query to obtain a lock on the mutex causes the other query to wait until the first is done and unlocks the mutex.

The work performed while holding a mutex is said to be in a "critical section," and multiple queries do execute this critical section in a serialized way (one at a time), which is a potential bottleneck.

The [mutex\\_instances](#page-17-1) table has these columns:

• NAME

The instrument name associated with the mutex.

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the instrumented mutex.

• LOCKED\_BY\_THREAD\_ID

When a thread currently has a mutex locked, LOCKED\_BY\_THREAD\_ID is the THREAD\_ID of the locking thread, otherwise it is NULL.

TRUNCATE TABLE is not permitted for the [mutex\\_instances](#page-17-1) table.

For every mutex instrumented in the code, the Performance Schema provides the following information.

- The [setup\\_instruments](#page-13-0) table lists the name of the instrumentation point, with the prefix wait/ synch/mutex/.
- When some code creates a mutex, a row is added to the [mutex\\_instances](#page-17-1) table. The OBJECT\_INSTANCE\_BEGIN column is a property that uniquely identifies the mutex.
- When a thread attempts to lock a mutex, the [events\\_waits\\_current](#page-23-0) table shows a row for that thread, indicating that it is waiting on a mutex (in the EVENT\_NAME column), and indicating which mutex is waited on (in the OBJECT\_INSTANCE\_BEGIN column).
- When a thread succeeds in locking a mutex:
  - [events\\_waits\\_current](#page-23-0) shows that the wait on the mutex is completed (in the TIMER\_END and TIMER\_WAIT columns)
  - The completed wait event is added to the [events\\_waits\\_history](#page-25-0) and [events\\_waits\\_history\\_long](#page-26-0) tables
  - [mutex\\_instances](#page-17-1) shows that the mutex is now owned by the thread (in the THREAD\_ID column).
- When a thread unlocks a mutex, [mutex\\_instances](#page-17-1) shows that the mutex now has no owner (the THREAD\_ID column is NULL).
- When a mutex object is destroyed, the corresponding row is removed from [mutex\\_instances](#page-17-1).

By performing queries on both of the following tables, a monitoring application or a DBA can detect bottlenecks or deadlocks between threads that involve mutexes:

- [events\\_waits\\_current](#page-23-0), to see what mutex a thread is waiting for
- [mutex\\_instances](#page-17-1), to see which other thread currently owns a mutex

## <span id="page-18-0"></span>**25.12.3.4 The rwlock\_instances Table**

The [rwlock\\_instances](#page-18-0) table lists all the rwlock (read write lock) instances seen by the Performance Schema while the server executes. An rwlock is a synchronization mechanism used in the code to enforce that threads at a given time can have access to some common resource following certain rules. The resource is said to be "protected" by the rwlock. The access is either shared (many threads can have a read lock at the same time), exclusive (only one thread can have a write lock at a given time), or shared-exclusive (a thread can have a write lock while permitting inconsistent reads by other threads). Shared-exclusive access is otherwise known as an sxlock and optimizes concurrency and improves scalability for read-write workloads.

Depending on how many threads are requesting a lock, and the nature of the locks requested, access can be either granted in shared mode, exclusive mode, shared-exclusive mode or not granted at all, waiting for other threads to finish first.

The [rwlock\\_instances](#page-18-0) table has these columns:

• NAME

The instrument name associated with the lock.

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the instrumented lock.

• WRITE\_LOCKED\_BY\_THREAD\_ID

When a thread currently has an rwlock locked in exclusive (write) mode, WRITE\_LOCKED\_BY\_THREAD\_ID is the THREAD\_ID of the locking thread, otherwise it is NULL.

• READ\_LOCKED\_BY\_COUNT

When a thread currently has an rwlock locked in shared (read) mode, READ\_LOCKED\_BY\_COUNT is incremented by 1. This is a counter only, so it cannot be used directly to find which thread holds a read lock, but it can be used to see whether there is a read contention on an rwlock, and see how many readers are currently active.

TRUNCATE TABLE is not permitted for the [rwlock\\_instances](#page-18-0) table.

By performing queries on both of the following tables, a monitoring application or a DBA may detect some bottlenecks or deadlocks between threads that involve locks:

- [events\\_waits\\_current](#page-23-0), to see what rwlock a thread is waiting for
- [rwlock\\_instances](#page-18-0), to see which other thread currently owns an rwlock

There is a limitation: The [rwlock\\_instances](#page-18-0) can be used only to identify the thread holding a write lock, but not the threads holding a read lock.

## <span id="page-19-0"></span>**25.12.3.5 The socket\_instances Table**

The [socket\\_instances](#page-19-0) table provides a real-time snapshot of the active connections to the MySQL server. The table contains one row per TCP/IP or Unix socket file connection. Information available in this table provides a real-time snapshot of the active connections to the server. (Additional information is available in socket summary tables, including network activity such as socket operations and number of bytes transmitted and received; see [Section 25.12.15.8, "Socket Summary Tables"](#page-87-0)).

```
mysql> SELECT * FROM performance_schema.socket_instances\G
*************************** 1. row ***************************
 EVENT_NAME: wait/io/socket/sql/server_unix_socket
OBJECT_INSTANCE_BEGIN: 4316619408
 THREAD_ID: 1
 SOCKET_ID: 16
 IP:
 PORT: 0
 STATE: ACTIVE
*************************** 2. row ***************************
 EVENT_NAME: wait/io/socket/sql/client_connection
OBJECT_INSTANCE_BEGIN: 4316644608
 THREAD_ID: 21
 SOCKET_ID: 39
 IP: 127.0.0.1
 PORT: 55233
 STATE: ACTIVE
*************************** 3. row ***************************
 EVENT_NAME: wait/io/socket/sql/server_tcpip_socket
OBJECT_INSTANCE_BEGIN: 4316699040
 THREAD_ID: 1
 SOCKET_ID: 14
 IP: 0.0.0.0
 PORT: 50603
 STATE: ACTIVE
```

Socket instruments have names of the form wait/io/socket/sql/socket\_type and are used like this:

- 1. The server has a listening socket for each network protocol that it supports. The instruments associated with listening sockets for TCP/IP or Unix socket file connections have a socket\_type value of server\_tcpip\_socket or server\_unix\_socket, respectively.
- 2. When a listening socket detects a connection, the server transfers the connection to a new socket managed by a separate thread. The instrument for the new connection thread has a socket\_type value of client\_connection.
- 3. When a connection terminates, the row in [socket\\_instances](#page-19-0) corresponding to it is deleted.

The [socket\\_instances](#page-19-0) table has these columns:

• EVENT\_NAME

The name of the wait/io/socket/\* instrument that produced the event. This is a NAME value from the [setup\\_instruments](#page-13-0) table. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

• OBJECT\_INSTANCE\_BEGIN

This column uniquely identifies the socket. The value is the address of an object in memory.

• THREAD\_ID

The internal thread identifier assigned by the server. Each socket is managed by a single thread, so each socket can be mapped to a thread which can be mapped to a server process.

• SOCKET\_ID

The internal file handle assigned to the socket.

• IP

The client IP address. The value may be either an IPv4 or IPv6 address, or blank to indicate a Unix socket file connection.

• PORT

The TCP/IP port number, in the range from 0 to 65535.

• STATE

The socket status, either IDLE or ACTIVE. Wait times for active sockets are tracked using the corresponding socket instrument. Wait times for idle sockets are tracked using the idle instrument.

A socket is idle if it is waiting for a request from the client. When a socket becomes idle, the event row in [socket\\_instances](#page-19-0) that is tracking the socket switches from a status of ACTIVE to IDLE. The EVENT\_NAME value remains wait/io/socket/\*, but timing for the instrument is suspended. Instead, an event is generated in the [events\\_waits\\_current](#page-23-0) table with an EVENT\_NAME value of idle.

When the next request is received, the idle event terminates, the socket instance switches from IDLE to ACTIVE, and timing of the socket instrument resumes.

TRUNCATE TABLE is not permitted for the [socket\\_instances](#page-19-0) table.

The IP:PORT column combination value identifies the connection. This combination value is used in the OBJECT\_NAME column of the events\_waits\_xxx tables, to identify the connection from which socket events come:

- For the Unix domain listener socket (server\_unix\_socket), the port is 0, and the IP is ''.
- For client connections via the Unix domain listener (client\_connection), the port is 0, and the IP is ''.
- For the TCP/IP server listener socket (server\_tcpip\_socket), the port is always the master port (for example, 3306), and the IP is always 0.0.0.0.
- For client connections via the TCP/IP listener (client\_connection), the port is whatever the server assigns, but never 0. The IP is the IP of the originating host (127.0.0.1 or ::1 for the local host)

# <span id="page-21-0"></span>**25.12.4 Performance Schema Wait Event Tables**

The Performance Schema instruments waits, which are events that take time. Within the event hierarchy, wait events nest within stage events, which nest within statement events, which nest within transaction events.

These tables store wait events:

- [events\\_waits\\_current](#page-23-0): The current wait event for each thread.
- [events\\_waits\\_history](#page-25-0): The most recent wait events that have ended per thread.
- [events\\_waits\\_history\\_long](#page-26-0): The most recent wait events that have ended globally (across all threads).

The following sections describe the wait event tables. There are also summary tables that aggregate information about wait events; see [Section 25.12.15.1, "Wait Event Summary Tables".](#page-76-0)

For more information about the relationship between the three wait event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

## **Configuring Wait Event Collection**

To control whether to collect wait events, set the state of the relevant instruments and consumers:

- The [setup\\_instruments](#page-13-0) table contains instruments with names that begin with wait. Use these instruments to enable or disable collection of individual wait event classes.
- The [setup\\_consumers](#page-12-0) table contains consumer values with names corresponding to the current and historical wait event table names. Use these consumers to filter collection of wait events.

Some wait instruments are enabled by default; others are disabled. For example:

```
mysql> SELECT * FROM performance_schema.setup_instruments
 WHERE NAME LIKE 'wait/io/file/innodb%';
+--------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+--------------------------------------+---------+-------+
| wait/io/file/innodb/innodb_data_file | YES | YES |
| wait/io/file/innodb/innodb_log_file | YES | YES |
| wait/io/file/innodb/innodb_temp_file | YES | YES |
+--------------------------------------+---------+-------+
mysql> SELECT *
 FROM performance_schema.setup_instruments WHERE
 NAME LIKE 'wait/io/socket/%';
+----------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+----------------------------------------+---------+-------+
| wait/io/socket/sql/server_tcpip_socket | NO | NO |
| wait/io/socket/sql/server_unix_socket | NO | NO |
| wait/io/socket/sql/client_connection | NO | NO |
+----------------------------------------+---------+-------+
```

The wait consumers are disabled by default:

```
mysql> SELECT *
 FROM performance_schema.setup_consumers
 WHERE NAME LIKE 'events_waits%';
+---------------------------+---------+
| NAME | ENABLED |
+---------------------------+---------+
| events_waits_current | NO |
| events_waits_history | NO |
| events_waits_history_long | NO |
+---------------------------+---------+
```

To control wait event collection at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='wait/%=ON'
performance-schema-consumer-events-waits-current=ON
performance-schema-consumer-events-waits-history=ON
performance-schema-consumer-events-waits-history-long=ON
```

• Disable:

```
[mysqld]
performance-schema-instrument='wait/%=OFF'
performance-schema-consumer-events-waits-current=OFF
performance-schema-consumer-events-waits-history=OFF
performance-schema-consumer-events-waits-history-long=OFF
```

To control wait event collection at runtime, update the [setup\\_instruments](#page-13-0) and [setup\\_consumers](#page-12-0) tables:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'wait/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_waits%';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
WHERE NAME LIKE 'wait/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'NO'
WHERE NAME LIKE 'events_waits%';
```

To collect only specific wait events, enable only the corresponding wait instruments. To collect wait events only for specific wait event tables, enable the wait instruments but only the wait consumers corresponding to the desired tables.

The [setup\\_timers](#page-15-0) table contains a row with a NAME value of wait that indicates the unit for wait event timing. The default unit is CYCLE:

```
mysql> SELECT *
 FROM performance_schema.setup_timers
 WHERE NAME = 'wait';
+------+------------+
| NAME | TIMER_NAME |
+------+------------+
| wait | CYCLE |
+------+------------+
```

To change the timing unit, modify the TIMER\_NAME value:

```
UPDATE performance_schema.setup_timers
SET TIMER_NAME = 'NANOSECOND'
WHERE NAME = 'wait';
```

For additional information about configuring event collection, see Section 25.3, "Performance Schema Startup Configuration", and Section 25.4, "Performance Schema Runtime Configuration".

## <span id="page-23-0"></span>**25.12.4.1 The events\_waits\_current Table**

The [events\\_waits\\_current](#page-23-0) table contains current wait events. The table stores one row per thread showing the current status of the thread's most recent monitored wait event, so there is no system variable for configuring the table size.

Of the tables that contain wait event rows, [events\\_waits\\_current](#page-23-0) is the most fundamental. Other tables that contain wait event rows are logically derived from the current events. For example, the [events\\_waits\\_history](#page-25-0) and [events\\_waits\\_history\\_long](#page-26-0) tables are collections of the most recent wait events that have ended, up to a maximum number of rows per thread and globally across all threads, respectively.

For more information about the relationship between the three wait event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect wait events, see [Section 25.12.4, "Performance](#page-21-0) [Schema Wait Event Tables".](#page-21-0)

The [events\\_waits\\_current](#page-23-0) table has these columns:

• THREAD\_ID, EVENT\_ID

The thread associated with the event and the thread current event number when the event starts. The THREAD\_ID and EVENT\_ID values taken together uniquely identify the row. No two rows have the same pair of values.

• END\_EVENT\_ID

This column is set to NULL when the event starts and updated to the thread current event number when the event ends.

• EVENT\_NAME

The name of the instrument that produced the event. This is a NAME value from the [setup\\_instruments](#page-13-0) table. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

• SOURCE

The name of the source file containing the instrumented code that produced the event and the line number in the file at which the instrumentation occurs. This enables you to check the source to determine exactly what code is involved. For example, if a mutex or lock is being blocked, you can check the context in which this occurs.

• TIMER\_START, TIMER\_END, TIMER\_WAIT

Timing information for the event. The unit for these values is picoseconds (trillionths of a second). The TIMER\_START and TIMER\_END values indicate when event timing started and ended. TIMER\_WAIT is the event elapsed time (duration).

If an event has not finished, TIMER\_END is the current timer value and TIMER\_WAIT is the time elapsed so far (TIMER\_END − TIMER\_START).

If an event is produced from an instrument that has TIMED = NO, timing information is not collected, and TIMER\_START, TIMER\_END, and TIMER\_WAIT are all NULL.

For discussion of picoseconds as the unit for event times and factors that affect time values, see Section 25.4.1, "Performance Schema Event Timing".

• SPINS

For a mutex, the number of spin rounds. If the value is NULL, the code does not use spin rounds or spinning is not instrumented.

• OBJECT\_SCHEMA, OBJECT\_NAME, OBJECT\_TYPE, OBJECT\_INSTANCE\_BEGIN

These columns identify the object "being acted on." What that means depends on the object type.

For a synchronization object (cond, mutex, rwlock):

- OBJECT\_SCHEMA, OBJECT\_NAME, and OBJECT\_TYPE are NULL.
- OBJECT\_INSTANCE\_BEGIN is the address of the synchronization object in memory.

#### For a file I/O object:

- OBJECT\_SCHEMA is NULL.
- OBJECT\_NAME is the file name.
- OBJECT\_TYPE is FILE.
- OBJECT\_INSTANCE\_BEGIN is an address in memory.

#### For a socket object:

- OBJECT\_NAME is the IP:PORT value for the socket.
- OBJECT\_INSTANCE\_BEGIN is an address in memory.

#### For a table I/O object:

- OBJECT\_SCHEMA is the name of the schema that contains the table.
- OBJECT\_NAME is the table name.
- OBJECT\_TYPE is TABLE for a persistent base table or TEMPORARY TABLE for a temporary table.
- OBJECT\_INSTANCE\_BEGIN is an address in memory.

An OBJECT\_INSTANCE\_BEGIN value itself has no meaning, except that different values indicate different objects. OBJECT\_INSTANCE\_BEGIN can be used for debugging. For example, it can be used with GROUP BY OBJECT\_INSTANCE\_BEGIN to see whether the load on 1,000 mutexes (that protect, say, 1,000 pages or blocks of data) is spread evenly or just hitting a few bottlenecks. This can help you correlate with other sources of information if you see the same object address in a log file or another debugging or performance tool.

• INDEX\_NAME

The name of the index used. PRIMARY indicates the table primary index. NULL means that no index was used.

• NESTING\_EVENT\_ID

The EVENT\_ID value of the event within which this event is nested.

• NESTING\_EVENT\_TYPE

The nesting event type. The value is TRANSACTION, STATEMENT, STAGE, or WAIT.

• OPERATION

The type of operation performed, such as lock, read, or write.

• NUMBER\_OF\_BYTES

The number of bytes read or written by the operation. For table I/O waits (events for the wait/ io/table/sql/handler instrument), NUMBER\_OF\_BYTES indicates the number of rows. If the value is greater than 1, the event is for a batch I/O operation. The following discussion describes the difference between exclusively single-row reporting and reporting that reflects batch I/O.

MySQL executes joins using a nested-loop implementation. The job of the Performance Schema instrumentation is to provide row count and accumulated execution time per table in the join. Assume a join query of the following form that is executed using a table join order of t1, t2, t3:

```
SELECT ... FROM t1 JOIN t2 ON ... JOIN t3 ON ...
```

Table "fanout" is the increase or decrease in number of rows from adding a table during join processing. If the fanout for table t3 is greater than 1, the majority of row-fetch operations are for that table. Suppose that the join accesses 10 rows from t1, 20 rows from t2 per row from t1, and 30 rows from t3 per row of table t2. With single-row reporting, the total number of instrumented operations is:

```
10 + (10 * 20) + (10 * 20 * 30) = 6210
```

A significant reduction in the number of instrumented operations is achievable by aggregating them per scan (that is, per unique combination of rows from t1 and t2). With batch I/O reporting, the Performance Schema produces an event for each scan of the innermost table t3 rather than for each row, and the number of instrumented row operations reduces to:

```
10 + (10 * 20) + (10 * 20) = 410
```

That is a reduction of 93%, illustrating how the batch-reporting strategy significantly reduces Performance Schema overhead for table I/O by reducing the number of reporting calls. The tradeoff is lesser accuracy for event timing. Rather than time for an individual row operation as in per-row reporting, timing for batch I/O includes time spent for operations such as join buffering, aggregation, and returning rows to the client.

For batch I/O reporting to occur, these conditions must be true:

- Query execution accesses the innermost table of a query block (for a single-table query, that table counts as innermost)
- Query execution does not request a single row from the table (so, for example, eq\_ref access prevents use of batch reporting)
- Query execution does not evaluate a subquery containing table access for the table
- FLAGS

Reserved for future use.

TRUNCATE TABLE is permitted for the [events\\_waits\\_current](#page-23-0) table. It removes the rows.

## <span id="page-25-0"></span>**25.12.4.2 The events\_waits\_history Table**

The [events\\_waits\\_history](#page-25-0) table contains the N most recent wait events that have ended per thread. Wait events are not added to the table until they have ended. When the table contains the maximum number of rows for a given thread, the oldest thread row is discarded when a new row for that thread is added. When a thread ends, all its rows are discarded.

The Performance Schema autosizes the value of N during server startup. To set the number of rows per thread explicitly, set the [performance\\_schema\\_events\\_waits\\_history\\_size](#page-113-0) system variable at server startup.

The [events\\_waits\\_history](#page-25-0) table has the same columns as [events\\_waits\\_current](#page-23-0). See [Section 25.12.4.1, "The events\\_waits\\_current Table"](#page-23-0).

TRUNCATE TABLE is permitted for the [events\\_waits\\_history](#page-25-0) table. It removes the rows.

For more information about the relationship between the three wait event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect wait events, see [Section 25.12.4, "Performance](#page-21-0) [Schema Wait Event Tables".](#page-21-0)

## <span id="page-26-0"></span>**25.12.4.3 The events\_waits\_history\_long Table**

The [events\\_waits\\_history\\_long](#page-26-0) table contains N the most recent wait events that have ended globally, across all threads. Wait events are not added to the table until they have ended. When the table becomes full, the oldest row is discarded when a new row is added, regardless of which thread generated either row.

The Performance Schema autosizes the value of N during server startup. To set the table size explicitly, set the [performance\\_schema\\_events\\_waits\\_history\\_long\\_size](#page-112-0) system variable at server startup.

The [events\\_waits\\_history\\_long](#page-26-0) table has the same columns as [events\\_waits\\_current](#page-23-0). See [Section 25.12.4.1, "The events\\_waits\\_current Table"](#page-23-0).

TRUNCATE TABLE is permitted for the [events\\_waits\\_history\\_long](#page-26-0) table. It removes the rows.

For more information about the relationship between the three wait event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect wait events, see [Section 25.12.4, "Performance](#page-21-0) [Schema Wait Event Tables".](#page-21-0)

# <span id="page-26-1"></span>**25.12.5 Performance Schema Stage Event Tables**

The Performance Schema instruments stages, which are steps during the statement-execution process, such as parsing a statement, opening a table, or performing a filesort operation. Stages correspond to the thread states displayed by SHOW PROCESSLIST or that are visible in the Information Schema PROCESSLIST table. Stages begin and end when state values change.

Within the event hierarchy, wait events nest within stage events, which nest within statement events, which nest within transaction events.

These tables store stage events:

- [events\\_stages\\_current](#page-30-0): The current stage event for each thread.
- [events\\_stages\\_history](#page-31-0): The most recent stage events that have ended per thread.
- [events\\_stages\\_history\\_long](#page-31-1): The most recent stage events that have ended globally (across all threads).

The following sections describe the stage event tables. There are also summary tables that aggregate information about stage events; see [Section 25.12.15.2, "Stage Summary Tables"](#page-77-0).

For more information about the relationship between the three stage event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

- [Configuring Stage Event Collection](#page-27-0)
- [Stage Event Progress Information](#page-29-0)

## <span id="page-27-0"></span>**Configuring Stage Event Collection**

To control whether to collect stage events, set the state of the relevant instruments and consumers:

- The [setup\\_instruments](#page-13-0) table contains instruments with names that begin with stage. Use these instruments to enable or disable collection of individual stage event classes.
- The [setup\\_consumers](#page-12-0) table contains consumer values with names corresponding to the current and historical stage event table names. Use these consumers to filter collection of stage events.

Other than those instruments that provide statement progress information, the stage instruments are disabled by default. For example:

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE NAME RLIKE 'stage/sql/[a-c]';
+----------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+----------------------------------------------------+---------+-------+
| stage/sql/After create | NO | NO |
| stage/sql/allocating local table | NO | NO |
| stage/sql/altering table | NO | NO |
| stage/sql/committing alter table to storage engine | NO | NO |
| stage/sql/Changing master | NO | NO |
| stage/sql/Checking master version | NO | NO |
| stage/sql/checking permissions | NO | NO |
| stage/sql/checking privileges on cached query | NO | NO |
| stage/sql/checking query cache for query | NO | NO |
| stage/sql/cleaning up | NO | NO |
| stage/sql/closing tables | NO | NO |
| stage/sql/Connecting to master | NO | NO |
| stage/sql/converting HEAP to MyISAM | NO | NO |
| stage/sql/Copying to group table | NO | NO |
| stage/sql/Copying to tmp table | NO | NO |
| stage/sql/copy to tmp table | NO | NO |
| stage/sql/Creating sort index | NO | NO |
| stage/sql/creating table | NO | NO |
| stage/sql/Creating tmp table | NO | NO |
+----------------------------------------------------+---------+-------+
```

Stage event instruments that provide statement progress information are enabled and timed by default:

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE ENABLED='YES' AND NAME LIKE "stage/%";
+------------------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+------------------------------------------------------+---------+-------+
| stage/sql/copy to tmp table | YES | YES |
| stage/innodb/alter table (end) | YES | YES |
| stage/innodb/alter table (flush) | YES | YES |
| stage/innodb/alter table (insert) | YES | YES |
| stage/innodb/alter table (log apply index) | YES | YES |
| stage/innodb/alter table (log apply table) | YES | YES |
| stage/innodb/alter table (merge sort) | YES | YES |
| stage/innodb/alter table (read PK and internal sort) | YES | YES |
| stage/innodb/buffer pool load | YES | YES |
+------------------------------------------------------+---------+-------+
```

The stage consumers are disabled by default:

```
mysql> SELECT *
```

```
 FROM performance_schema.setup_consumers
 WHERE NAME LIKE 'events_stages%';
+----------------------------+---------+
| NAME | ENABLED |
+----------------------------+---------+
| events_stages_current | NO |
| events_stages_history | NO |
| events_stages_history_long | NO |
+----------------------------+---------+
```

To control stage event collection at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='stage/%=ON'
performance-schema-consumer-events-stages-current=ON
performance-schema-consumer-events-stages-history=ON
performance-schema-consumer-events-stages-history-long=ON
```

• Disable:

```
[mysqld]
performance-schema-instrument='stage/%=OFF'
performance-schema-consumer-events-stages-current=OFF
performance-schema-consumer-events-stages-history=OFF
performance-schema-consumer-events-stages-history-long=OFF
```

To control stage event collection at runtime, update the [setup\\_instruments](#page-13-0) and [setup\\_consumers](#page-12-0) tables:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'stage/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_stages%';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
WHERE NAME LIKE 'stage/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'NO'
WHERE NAME LIKE 'events_stages%';
```

To collect only specific stage events, enable only the corresponding stage instruments. To collect stage events only for specific stage event tables, enable the stage instruments but only the stage consumers corresponding to the desired tables.

The [setup\\_timers](#page-15-0) table contains a row with a NAME value of stage that indicates the unit for stage event timing. The default unit is NANOSECOND:

```
mysql> SELECT *
 FROM performance_schema.setup_timers
 WHERE NAME = 'stage';
+-------+------------+
| NAME | TIMER_NAME |
+-------+------------+
| stage | NANOSECOND |
+-------+------------+
```

To change the timing unit, modify the TIMER\_NAME value:

```
UPDATE performance_schema.setup_timers
```

```
SET TIMER_NAME = 'MICROSECOND'
WHERE NAME = 'stage';
```

For additional information about configuring event collection, see Section 25.3, "Performance Schema Startup Configuration", and Section 25.4, "Performance Schema Runtime Configuration".

## <span id="page-29-0"></span>**Stage Event Progress Information**

The Performance Schema stage event tables contain two columns that, taken together, provide a stage progress indicator for each row:

- WORK\_COMPLETED: The number of work units completed for the stage
- WORK\_ESTIMATED: The number of work units expected for the stage

Each column is NULL if no progress information is provided for an instrument. Interpretation of the information, if it is available, depends entirely on the instrument implementation. The Performance Schema tables provide a container to store progress data, but make no assumptions about the semantics of the metric itself:

- A "work unit" is an integer metric that increases over time during execution, such as the number of bytes, rows, files, or tables processed. The definition of "work unit" for a particular instrument is left to the instrumentation code providing the data.
- The WORK\_COMPLETED value can increase one or many units at a time, depending on the instrumented code.
- The WORK\_ESTIMATED value can change during the stage, depending on the instrumented code.

Instrumentation for a stage event progress indicator can implement any of the following behaviors:

• No progress instrumentation

This is the most typical case, where no progress data is provided. The WORK\_COMPLETED and WORK\_ESTIMATED columns are both NULL.

• Unbounded progress instrumentation

Only the WORK\_COMPLETED column is meaningful. No data is provided for the WORK\_ESTIMATED column, which displays 0.

By querying the [events\\_stages\\_current](#page-30-0) table for the monitored session, a monitoring application can report how much work has been performed so far, but cannot report whether the stage is near completion. Currently, no stages are instrumented like this.

• Bounded progress instrumentation

The WORK\_COMPLETED and WORK\_ESTIMATED columns are both meaningful.

This type of progress indicator is appropriate for an operation with a defined completion criterion, such as the table-copy instrument described later. By querying the [events\\_stages\\_current](#page-30-0) table for the monitored session, a monitoring application can report how much work has been performed so far, and can report the overall completion percentage for the stage, by computing the WORK\_COMPLETED / WORK\_ESTIMATED ratio.

The stage/sql/copy to tmp table instrument illustrates how progress indicators work. During execution of an ALTER TABLE statement, the stage/sql/copy to tmp table stage is used, and this stage can execute potentially for a long time, depending on the size of the data to copy.

The table-copy task has a defined termination (all rows copied), and the stage/sql/copy to tmp table stage is instrumented to provided bounded progress information: The work unit used is number of rows copied, WORK\_COMPLETED and WORK\_ESTIMATED are both meaningful, and their ratio indicates task percentage complete.

To enable the instrument and the relevant consumers, execute these statements:

```
UPDATE performance_schema.setup_instruments
SET ENABLED='YES'
WHERE NAME='stage/sql/copy to tmp table';
UPDATE performance_schema.setup_consumers
SET ENABLED='YES'
WHERE NAME LIKE 'events_stages_%';
```

To see the progress of an ongoing ALTER TABLE statement, select from the [events\\_stages\\_current](#page-30-0) table.

## <span id="page-30-0"></span>**25.12.5.1 The events\_stages\_current Table**

The [events\\_stages\\_current](#page-30-0) table contains current stage events. The table stores one row per thread showing the current status of the thread's most recent monitored stage event, so there is no system variable for configuring the table size.

Of the tables that contain stage event rows, [events\\_stages\\_current](#page-30-0) is the most fundamental. Other tables that contain stage event rows are logically derived from the current events. For example, the [events\\_stages\\_history](#page-31-0) and [events\\_stages\\_history\\_long](#page-31-1) tables are collections of the most recent stage events that have ended, up to a maximum number of rows per thread and globally across all threads, respectively.

For more information about the relationship between the three stage event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect stage events, see [Section 25.12.5, "Performance](#page-26-1) [Schema Stage Event Tables"](#page-26-1).

The [events\\_stages\\_current](#page-30-0) table has these columns:

• THREAD\_ID, EVENT\_ID

The thread associated with the event and the thread current event number when the event starts. The THREAD\_ID and EVENT\_ID values taken together uniquely identify the row. No two rows have the same pair of values.

• END\_EVENT\_ID

This column is set to NULL when the event starts and updated to the thread current event number when the event ends.

• EVENT\_NAME

The name of the instrument that produced the event. This is a NAME value from the [setup\\_instruments](#page-13-0) table. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

• SOURCE

The name of the source file containing the instrumented code that produced the event and the line number in the file at which the instrumentation occurs. This enables you to check the source to determine exactly what code is involved.

• TIMER\_START, TIMER\_END, TIMER\_WAIT

Timing information for the event. The unit for these values is picoseconds (trillionths of a second). The TIMER\_START and TIMER\_END values indicate when event timing started and ended. TIMER\_WAIT is the event elapsed time (duration).

If an event has not finished, TIMER\_END is the current timer value and TIMER\_WAIT is the time elapsed so far (TIMER\_END − TIMER\_START).

If an event is produced from an instrument that has TIMED = NO, timing information is not collected, and TIMER\_START, TIMER\_END, and TIMER\_WAIT are all NULL.

For discussion of picoseconds as the unit for event times and factors that affect time values, see Section 25.4.1, "Performance Schema Event Timing".

• WORK\_COMPLETED, WORK\_ESTIMATED

These columns provide stage progress information, for instruments that have been implemented to produce such information. WORK\_COMPLETED indicates how many work units have been completed for the stage, and WORK\_ESTIMATED indicates how many work units are expected for the stage. For more information, see [Stage Event Progress Information.](#page-29-0)

• NESTING\_EVENT\_ID

The EVENT\_ID value of the event within which this event is nested. The nesting event for a stage event is usually a statement event.

• NESTING\_EVENT\_TYPE

The nesting event type. The value is TRANSACTION, STATEMENT, STAGE, or WAIT.

TRUNCATE TABLE is permitted for the [events\\_stages\\_current](#page-30-0) table. It removes the rows.

## <span id="page-31-0"></span>**25.12.5.2 The events\_stages\_history Table**

The [events\\_stages\\_history](#page-31-0) table contains the N most recent stage events that have ended per thread. Stage events are not added to the table until they have ended. When the table contains the maximum number of rows for a given thread, the oldest thread row is discarded when a new row for that thread is added. When a thread ends, all its rows are discarded.

The Performance Schema autosizes the value of N during server startup. To set the number of rows per thread explicitly, set the [performance\\_schema\\_events\\_stages\\_history\\_size](#page-111-0) system variable at server startup.

The [events\\_stages\\_history](#page-31-0) table has the same columns as [events\\_stages\\_current](#page-30-0). See [Section 25.12.5.1, "The events\\_stages\\_current Table"](#page-30-0).

TRUNCATE TABLE is permitted for the [events\\_stages\\_history](#page-31-0) table. It removes the rows.

For more information about the relationship between the three stage event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect stage events, see [Section 25.12.5, "Performance](#page-26-1) [Schema Stage Event Tables"](#page-26-1).

## <span id="page-31-1"></span>**25.12.5.3 The events\_stages\_history\_long Table**

The [events\\_stages\\_history\\_long](#page-31-1) table contains the N most recent stage events that have ended globally, across all threads. Stage events are not added to the table until they have ended. When the table becomes full, the oldest row is discarded when a new row is added, regardless of which thread generated either row.

The Performance Schema autosizes the value of N during server startup. To set the table size explicitly, set the [performance\\_schema\\_events\\_stages\\_history\\_long\\_size](#page-110-1) system variable at server startup.

The [events\\_stages\\_history\\_long](#page-31-1) table has the same columns as [events\\_stages\\_current](#page-30-0). See [Section 25.12.5.1, "The events\\_stages\\_current Table".](#page-30-0)

TRUNCATE TABLE is permitted for the [events\\_stages\\_history\\_long](#page-31-1) table. It removes the rows.

For more information about the relationship between the three stage event tables, see [Section 25.9,](#page-1-0) ["Performance Schema Tables for Current and Historical Events"](#page-1-0).

For information about configuring whether to collect stage events, see [Section 25.12.5, "Performance](#page-26-1) [Schema Stage Event Tables"](#page-26-1).

# <span id="page-32-0"></span>**25.12.6 Performance Schema Statement Event Tables**

The Performance Schema instruments statement execution. Statement events occur at a high level of the event hierarchy. Within the event hierarchy, wait events nest within stage events, which nest within statement events, which nest within transaction events.

These tables store statement events:

- [events\\_statements\\_current](#page-36-0): The current statement event for each thread.
- [events\\_statements\\_history](#page-39-0): The most recent statement events that have ended per thread.
- [events\\_statements\\_history\\_long](#page-39-1): The most recent statement events that have ended globally (across all threads).
- [prepared\\_statements\\_instances](#page-40-0): Prepared statement instances and statistics

The following sections describe the statement event tables. There are also summary tables that aggregate information about statement events; see [Section 25.12.15.3, "Statement Summary Tables"](#page-78-0).

For more information about the relationship between the three events\_statements\_xxx event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

- [Configuring Statement Event Collection](#page-32-1)
- [Statement Monitoring](#page-34-0)

## <span id="page-32-1"></span>**Configuring Statement Event Collection**

To control whether to collect statement events, set the state of the relevant instruments and consumers:

- The [setup\\_instruments](#page-13-0) table contains instruments with names that begin with statement. Use these instruments to enable or disable collection of individual statement event classes.
- The [setup\\_consumers](#page-12-0) table contains consumer values with names corresponding to the current and historical statement event table names, and the statement digest consumer. Use these consumers to filter collection of statement events and statement digesting.

The statement instruments are enabled by default, and the events\_statements\_current, events\_statements\_history, and statements\_digest statement consumers are enabled by default:

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE 'statement/%';
+---------------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+---------------------------------------------+---------+-------+
| statement/sql/select | YES | YES |
| statement/sql/create_table | YES | YES |
| statement/sql/create_index | YES | YES |
...
| statement/sp/stmt | YES | YES |
```

```
| statement/sp/set | YES | YES |
| statement/sp/set_trigger_field | YES | YES |
| statement/scheduler/event | YES | YES |
| statement/com/Sleep | YES | YES |
| statement/com/Quit | YES | YES |
| statement/com/Init DB | YES | YES |
...
| statement/abstract/Query | YES | YES |
| statement/abstract/new_packet | YES | YES |
| statement/abstract/relay_log | YES | YES |
+---------------------------------------------+---------+-------+
```

```
mysql> SELECT *
 FROM performance_schema.setup_consumers
 WHERE NAME LIKE '%statements%';
+--------------------------------+---------+
| NAME | ENABLED |
+--------------------------------+---------+
| events_statements_current | YES |
| events_statements_history | YES |
| events_statements_history_long | NO |
| statements_digest | YES |
+--------------------------------+---------+
```

To control statement event collection at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='statement/%=ON'
performance-schema-consumer-events-statements-current=ON
performance-schema-consumer-events-statements-history=ON
performance-schema-consumer-events-statements-history-long=ON
performance-schema-consumer-statements-digest=ON
```

• Disable:

```
[mysqld]
performance-schema-instrument='statement/%=OFF'
performance-schema-consumer-events-statements-current=OFF
performance-schema-consumer-events-statements-history=OFF
performance-schema-consumer-events-statements-history-long=OFF
performance-schema-consumer-statements-digest=OFF
```

To control statement event collection at runtime, update the [setup\\_instruments](#page-13-0) and [setup\\_consumers](#page-12-0) tables:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME LIKE 'statement/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE '%statements%';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
WHERE NAME LIKE 'statement/%';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'NO'
WHERE NAME LIKE '%statements%';
```

To collect only specific statement events, enable only the corresponding statement instruments. To collect statement events only for specific statement event tables, enable the statement instruments but only the statement consumers corresponding to the desired tables.

The [setup\\_timers](#page-15-0) table contains a row with a NAME value of statement that indicates the unit for statement event timing. The default unit is NANOSECOND:

```
mysql> SELECT *
 FROM performance_schema.setup_timers
 WHERE NAME = 'statement';
+-----------+------------+
| NAME | TIMER_NAME |
+-----------+------------+
| statement | NANOSECOND |
+-----------+------------+
```

To change the timing unit, modify the TIMER\_NAME value:

```
UPDATE performance_schema.setup_timers
SET TIMER_NAME = 'MICROSECOND'
WHERE NAME = 'statement';
```

For additional information about configuring event collection, see Section 25.3, "Performance Schema Startup Configuration", and Section 25.4, "Performance Schema Runtime Configuration".

## <span id="page-34-0"></span>**Statement Monitoring**

Statement monitoring begins from the moment the server sees that activity is requested on a thread, to the moment when all activity has ceased. Typically, this means from the time the server gets the first packet from the client to the time the server has finished sending the response. Statements within stored programs are monitored like other statements.

When the Performance Schema instruments a request (server command or SQL statement), it uses instrument names that proceed in stages from more general (or "abstract") to more specific until it arrives at a final instrument name.

Final instrument names correspond to server commands and SQL statements:

- Server commands correspond to the COM\_xxx codes defined in the mysql\_com.h header file and processed in sql/sql\_parse.cc. Examples are COM\_PING and COM\_QUIT. Instruments for commands have names that begin with statement/com, such as statement/com/Ping and statement/com/Quit.
- SQL statements are expressed as text, such as DELETE FROM t1 or SELECT \* FROM t2. Instruments for SQL statements have names that begin with statement/sql, such as statement/sql/delete and statement/sql/select.

Some final instrument names are specific to error handling:

- statement/com/Error accounts for messages received by the server that are out of band. It can be used to detect commands sent by clients that the server does not understand. This may be helpful for purposes such as identifying clients that are misconfigured or using a version of MySQL more recent than that of the server, or clients that are attempting to attack the server.
- statement/sql/error accounts for SQL statements that fail to parse. It can be used to detect malformed queries sent by clients. A query that fails to parse differs from a query that parses but fails due to an error during execution. For example, SELECT \* FROM is malformed, and the statement/sql/error instrument is used. By contrast, SELECT \* parses but fails with a No tables used error. In this case, statement/sql/select is used and the statement event contains information to indicate the nature of the error.

A request can be obtained from any of these sources:

- As a command or statement request from a client, which sends the request as packets
- As a statement string read from the relay log on a replica

• As an event from the Event Scheduler

The details for a request are not initially known and the Performance Schema proceeds from abstract to specific instrument names in a sequence that depends on the source of the request.

For a request received from a client:

- 1. When the server detects a new packet at the socket level, a new statement is started with an abstract instrument name of statement/abstract/new\_packet.
- 2. When the server reads the packet number, it knows more about the type of request received, and the Performance Schema refines the instrument name. For example, if the request is a COM\_PING packet, the instrument name becomes statement/com/Ping and that is the final name. If the request is a COM\_QUERY packet, it is known to correspond to an SQL statement but not the particular type of statement. In this case, the instrument changes from one abstract name to a more specific but still abstract name, statement/abstract/Query, and the request requires further classification.
- 3. If the request is a statement, the statement text is read and given to the parser. After parsing, the exact statement type is known. If the request is, for example, an INSERT statement, the Performance Schema refines the instrument name from statement/abstract/Query to statement/sql/insert, which is the final name.

For a request read as a statement from the relay log on a replica:

- 1. Statements in the relay log are stored as text and are read as such. There is no network protocol, so the statement/abstract/new\_packet instrument is not used. Instead, the initial instrument is statement/abstract/relay\_log.
- 2. When the statement is parsed, the exact statement type is known. If the request is, for example, an INSERT statement, the Performance Schema refines the instrument name from statement/ abstract/Query to statement/sql/insert, which is the final name.

The preceding description applies only for statement-based replication. For row-based replication, table I/O done on the replica as it processes row changes can be instrumented, but row events in the relay log do not appear as discrete statements.

For a request received from the Event Scheduler:

The event execution is instrumented using the name statement/scheduler/event. This is the final name.

Statements executed within the event body are instrumented using statement/sql/\* names, without use of any preceding abstract instrument. An event is a stored program, and stored programs are precompiled in memory before execution. Consequently, there is no parsing at runtime and the type of each statement is known by the time it executes.

Statements executed within the event body are child statements. For example, if an event executes an INSERT statement, execution of the event itself is the parent, instrumented using statement/ scheduler/event, and the INSERT is the child, instrumented using statement/sql/insert. The parent/child relationship holds between separate instrumented operations. This differs from the sequence of refinement that occurs within a single instrumented operation, from abstract to final instrument names.

For statistics to be collected for statements, it is not sufficient to enable only the final statement/ sql/\* instruments used for individual statement types. The abtract statement/abstract/\* instruments must be enabled as well. This should not normally be an issue because all statement instruments are enabled by default. However, an application that enables or disables statement instruments selectively must take into account that disabling abstract instruments also disables statistics collection for the individual statement instruments. For example, to collect statistics for INSERT statements, statement/sql/insert must be enabled, but also statement/abstract/ new\_packet and statement/abstract/Query. Similarly, for replicated statements to be instrumented, statement/abstract/relay\_log must be enabled.

No statistics are aggregated for abstract instruments such as statement/abstract/Query because no statement is ever classified with an abstract instrument as the final statement name.

## <span id="page-36-0"></span>**25.12.6.1 The events\_statements\_current Table**

The [events\\_statements\\_current](#page-36-0) table contains current statement events. The table stores one row per thread showing the current status of the thread's most recent monitored statement event, so there is no system variable for configuring the table size.

Of the tables that contain statement event rows, [events\\_statements\\_current](#page-36-0) is the most fundamental. Other tables that contain statement event rows are logically derived from the current events. For example, the [events\\_statements\\_history](#page-39-0) and [events\\_statements\\_history\\_long](#page-39-1) tables are collections of the most recent statement events that have ended, up to a maximum number of rows per thread and globally across all threads, respectively.

For more information about the relationship between the three events\_statements\_xxx event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect statement events, see [Section 25.12.6,](#page-32-0) ["Performance Schema Statement Event Tables".](#page-32-0)

The [events\\_statements\\_current](#page-36-0) table has these columns:

• THREAD\_ID, EVENT\_ID

The thread associated with the event and the thread current event number when the event starts. The THREAD\_ID and EVENT\_ID values taken together uniquely identify the row. No two rows have the same pair of values.

• END\_EVENT\_ID

This column is set to NULL when the event starts and updated to the thread current event number when the event ends.

• EVENT\_NAME

The name of the instrument from which the event was collected. This is a NAME value from the [setup\\_instruments](#page-13-0) table. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

For SQL statements, the EVENT\_NAME value initially is statement/com/Query until the statement is parsed, then changes to a more appropriate value, as described in [Section 25.12.6, "Performance](#page-32-0) [Schema Statement Event Tables".](#page-32-0)

• SOURCE

The name of the source file containing the instrumented code that produced the event and the line number in the file at which the instrumentation occurs. This enables you to check the source to determine exactly what code is involved.

• TIMER\_START, TIMER\_END, TIMER\_WAIT

Timing information for the event. The unit for these values is picoseconds (trillionths of a second). The TIMER\_START and TIMER\_END values indicate when event timing started and ended. TIMER\_WAIT is the event elapsed time (duration).

If an event has not finished, TIMER\_END is the current timer value and TIMER\_WAIT is the time elapsed so far (TIMER\_END − TIMER\_START).

If an event is produced from an instrument that has TIMED = NO, timing information is not collected, and TIMER\_START, TIMER\_END, and TIMER\_WAIT are all NULL.

For discussion of picoseconds as the unit for event times and factors that affect time values, see Section 25.4.1, "Performance Schema Event Timing".

• LOCK\_TIME

The time spent waiting for table locks. This value is computed in microseconds but normalized to picoseconds for easier comparison with other Performance Schema timers.

• SQL\_TEXT

The text of the SQL statement. For a command not associated with an SQL statement, the value is NULL.

The maximum space available for statement display is 1024 bytes by default. To change this value, set the [performance\\_schema\\_max\\_sql\\_text\\_length](#page-119-0) system variable at server startup.

• DIGEST

The statement digest MD5 value as a string of 32 hexadecimal characters, or NULL if the statements\_digest consumer is no. For more information about statement digesting, see [Section 25.10, "Performance Schema Statement Digests".](#page-2-0)

• DIGEST\_TEXT

The normalized statement digest text, or NULL if the statements\_digest consumer is no. For more information about statement digesting, see [Section 25.10, "Performance Schema Statement](#page-2-0) [Digests".](#page-2-0)

The [performance\\_schema\\_max\\_digest\\_length](#page-114-0) system variable determines the maximum number of bytes available per session for digest value storage. However, the display length of statement digests may be longer than the available buffer size due to encoding of statement elements such as keywords and literal values in digest buffer. Consequently, values selected from the DIGEST\_TEXT column of statement event tables may appear to exceed the [performance\\_schema\\_max\\_digest\\_length](#page-114-0) value.

• CURRENT\_SCHEMA

The default database for the statement, NULL if there is none.

• OBJECT\_SCHEMA, OBJECT\_NAME, OBJECT\_TYPE

For nested statements (stored programs), these columns contain information about the parent statement. Otherwise they are NULL.

• OBJECT\_INSTANCE\_BEGIN

This column identifies the statement. The value is the address of an object in memory.

• MYSQL\_ERRNO

The statement error number, from the statement diagnostics area.

• RETURNED\_SQLSTATE

The statement SQLSTATE value, from the statement diagnostics area.

• MESSAGE\_TEXT

The statement error message, from the statement diagnostics area.

• ERRORS

Whether an error occurred for the statement. The value is 0 if the SQLSTATE value begins with 00 (completion) or 01 (warning). The value is 1 is the SQLSTATE value is anything else.

• WARNINGS

The number of warnings, from the statement diagnostics area.

• ROWS\_AFFECTED

The number of rows affected by the statement. For a description of the meaning of "affected," see [mysql\\_affected\\_rows\(\).](https://dev.mysql.com/doc/c-api/5.7/en/mysql-affected-rows.md)

• ROWS\_SENT

The number of rows returned by the statement.

• ROWS\_EXAMINED

The number of rows examined by the server layer (not counting any processing internal to storage engines).

• CREATED\_TMP\_DISK\_TABLES

Like the Created\_tmp\_disk\_tables status variable, but specific to the statement.

• CREATED\_TMP\_TABLES

Like the Created\_tmp\_tables status variable, but specific to the statement.

• SELECT\_FULL\_JOIN

Like the Select\_full\_join status variable, but specific to the statement.

• SELECT\_FULL\_RANGE\_JOIN

Like the Select\_full\_range\_join status variable, but specific to the statement.

• SELECT\_RANGE

Like the Select\_range status variable, but specific to the statement.

• SELECT\_RANGE\_CHECK

Like the Select\_range\_check status variable, but specific to the statement.

• SELECT\_SCAN

Like the Select\_scan status variable, but specific to the statement.

• SORT\_MERGE\_PASSES

Like the Sort\_merge\_passes status variable, but specific to the statement.

• SORT\_RANGE

Like the Sort\_range status variable, but specific to the statement.

• SORT\_ROWS

Like the Sort\_rows status variable, but specific to the statement.

• SORT\_SCAN

Like the Sort\_scan status variable, but specific to the statement.

• NO\_INDEX\_USED

1 if the statement performed a table scan without using an index, 0 otherwise.

• NO\_GOOD\_INDEX\_USED

1 if the server found no good index to use for the statement, 0 otherwise. For additional information, see the description of the Extra column from EXPLAIN output for the Range checked for each record value in Section 8.8.2, "EXPLAIN Output Format".

• NESTING\_EVENT\_ID, NESTING\_EVENT\_TYPE, NESTING\_EVENT\_LEVEL

These three columns are used with other columns to provide information as follows for top-level (unnested) statements and nested statements (executed within a stored program).

For top level statements:

```
OBJECT_TYPE = NULL
OBJECT_SCHEMA = NULL
OBJECT_NAME = NULL
NESTING_EVENT_ID = NULL
NESTING_EVENT_TYPE = NULL
NESTING_LEVEL = 0
```

#### For nested statements:

```
OBJECT_TYPE = the parent statement object type
OBJECT_SCHEMA = the parent statement object schema
OBJECT_NAME = the parent statement object name
NESTING_EVENT_ID = the parent statement EVENT_ID
NESTING_EVENT_TYPE = 'STATEMENT'
NESTING_LEVEL = the parent statement NESTING_LEVEL plus one
```

TRUNCATE TABLE is permitted for the [events\\_statements\\_current](#page-36-0) table. It removes the rows.

## <span id="page-39-0"></span>**25.12.6.2 The events\_statements\_history Table**

The [events\\_statements\\_history](#page-39-0) table contains the N most recent statement events that have ended per thread. Statement events are not added to the table until they have ended. When the table contains the maximum number of rows for a given thread, the oldest thread row is discarded when a new row for that thread is added. When a thread ends, all its rows are discarded.

The Performance Schema autosizes the value of N during server startup. To set the number of rows per thread explicitly, set the [performance\\_schema\\_events\\_statements\\_history\\_size](#page-111-1) system variable at server startup.

The [events\\_statements\\_history](#page-39-0) table has the same columns as [events\\_statements\\_current](#page-36-0). See [Section 25.12.6.1, "The events\\_statements\\_current Table".](#page-36-0)

TRUNCATE TABLE is permitted for the [events\\_statements\\_history](#page-39-0) table. It removes the rows.

For more information about the relationship between the three events\_statements\_xxx event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect statement events, see [Section 25.12.6,](#page-32-0) ["Performance Schema Statement Event Tables".](#page-32-0)

## <span id="page-39-1"></span>**25.12.6.3 The events\_statements\_history\_long Table**

The [events\\_statements\\_history\\_long](#page-39-1) table contains the N most recent statement events that have ended globally, across all threads. Statement events are not added to the table until they have

ended. When the table becomes full, the oldest row is discarded when a new row is added, regardless of which thread generated either row.

The value of N is autosized at server startup. To set the table size explicitly, set the [performance\\_schema\\_events\\_statements\\_history\\_long\\_size](#page-111-2) system variable at server startup.

The [events\\_statements\\_history\\_long](#page-39-1) table has the same columns as [events\\_statements\\_current](#page-36-0). See [Section 25.12.6.1, "The events\\_statements\\_current Table".](#page-36-0)

TRUNCATE TABLE is permitted for the [events\\_statements\\_history\\_long](#page-39-1) table. It removes the rows.

For more information about the relationship between the three events\_statements\_xxx event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect statement events, see [Section 25.12.6,](#page-32-0) ["Performance Schema Statement Event Tables".](#page-32-0)

# <span id="page-40-0"></span>**25.12.6.4 The prepared\_statements\_instances Table**

The Performance Schema provides instrumentation for prepared statements, for which there are two protocols:

• The binary protocol. This is accessed through the MySQL C API and maps onto underlying server commands as shown in the following table.

| C API Function       | Corresponding Server Command |
|----------------------|------------------------------|
| mysql_stmt_prepare() | COM_STMT_PREPARE             |
| mysql_stmt_execute() | COM_STMT_EXECUTE             |
| mysql_stmt_close()   | COM_STMT_CLOSE               |

• The text protocol. This is accessed using SQL statements and maps onto underlying server commands as shown in the following table.

| SQL Statement                    | Corresponding Server Command |
|----------------------------------|------------------------------|
| PREPARE                          | SQLCOM_PREPARE               |
| EXECUTE                          | SQLCOM_EXECUTE               |
| DEALLOCATE PREPARE, DROP PREPARE | SQLCOM_DEALLOCATE PREPARE    |

Performance Schema prepared statement instrumentation covers both protocols. The following discussion refers to the server commands rather than the C API functions or SQL statements.

Information about prepared statements is available in the [prepared\\_statements\\_instances](#page-40-0) table. This table enables inspection of prepared statements used in the server and provides aggregated statistics about them. To control the size of this table, set the [performance\\_schema\\_max\\_prepared\\_statements\\_instances](#page-117-1) system variable at server startup.

Collection of prepared statement information depends on the statement instruments shown in the following table. These instruments are enabled by default. To modify them, update the [setup\\_instruments](#page-13-0) table.

| Instrument            | Server Command   |
|-----------------------|------------------|
| statement/com/Prepare | COM_STMT_PREPARE |
| statement/com/Execute | COM_STMT_EXECUTE |

| Instrument                | Server Command |
|---------------------------|----------------|
| statement/sql/prepare_sql | SQLCOM_PREPARE |
| statement/sql/execute_sql | SQLCOM_EXECUTE |

The Performance Schema manages the contents of the [prepared\\_statements\\_instances](#page-40-0) table as follows:

#### • Statement preparation

A COM\_STMT\_PREPARE or SQLCOM\_PREPARE command creates a prepared statement in the server. If the statement is successfully instrumented, a new row is added to the [prepared\\_statements\\_instances](#page-40-0) table. If the statement cannot be instrumented, [Performance\\_schema\\_prepared\\_statements\\_lost](#page-126-2) status variable is incremented.

#### • Prepared statement execution

Execution of a COM\_STMT\_EXECUTE or SQLCOM\_PREPARE command for an instrumented prepared statement instance updates the corresponding [prepared\\_statements\\_instances](#page-40-0) table row.

#### • Prepared statement deallocation

Execution of a COM\_STMT\_CLOSE or SQLCOM\_DEALLOCATE\_PREPARE command for an instrumented prepared statement instance removes the corresponding [prepared\\_statements\\_instances](#page-40-0) table row. To avoid resource leaks, removal occurs even if the prepared statement instruments described previously are disabled.

The [prepared\\_statements\\_instances](#page-40-0) table has these columns:

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the instrumented prepared statement.

• STATEMENT\_ID

The internal statement ID assigned by the server. The text and binary protocols both use statement IDs.

• STATEMENT\_NAME

For the binary protocol, this column is NULL. For the text protocol, this column is the external statement name assigned by the user. For example, for the following SQL statement, the name of the prepared statement is stmt:

```
PREPARE stmt FROM 'SELECT 1';
```

• SQL\_TEXT

The prepared statement text, with ? placeholder markers.

• OWNER\_THREAD\_ID, OWNER\_EVENT\_ID

These columns indicate the event that created the prepared statement.

• OWNER\_OBJECT\_TYPE, OWNER\_OBJECT\_SCHEMA, OWNER\_OBJECT\_NAME

For a prepared statement created by a client session, these columns are NULL. For a prepared statement created by a stored program, these columns point to the stored program. A typical user error is forgetting to deallocate prepared statements. These columns can be used to find stored programs that leak prepared statements:

SELECT

```
 OWNER_OBJECT_TYPE, OWNER_OBJECT_SCHEMA, OWNER_OBJECT_NAME,
 STATEMENT_NAME, SQL_TEXT
FROM performance_schema.prepared_statements_instances
WHERE OWNER_OBJECT_TYPE IS NOT NULL;
```

• TIMER\_PREPARE

The time spent executing the statement preparation itself.

• COUNT\_REPREPARE

The number of times the statement was reprepared internally (see Section 8.10.4, "Caching of Prepared Statements and Stored Programs"). Timing statistics for repreparation are not available because it is counted as part of statement execution, not as a separate operation.

• COUNT\_EXECUTE, SUM\_TIMER\_EXECUTE, MIN\_TIMER\_EXECUTE, AVG\_TIMER\_EXECUTE, MAX\_TIMER\_EXECUTE

Aggregated statistics for executions of the prepared statement.

• SUM\_xxx

The remaining SUM\_xxx columns are the same as for the statement summary tables (see [Section 25.12.15.3, "Statement Summary Tables"\)](#page-78-0).

TRUNCATE TABLE resets the statistics columns of the [prepared\\_statements\\_instances](#page-40-0) table.

# <span id="page-42-0"></span>**25.12.7 Performance Schema Transaction Tables**

The Performance Schema instruments transactions. Within the event hierarchy, wait events nest within stage events, which nest within statement events, which nest within transaction events.

These tables store transaction events:

- [events\\_transactions\\_current](#page-46-0): The current transaction event for each thread.
- [events\\_transactions\\_history](#page-49-0): The most recent transaction events that have ended per thread.
- [events\\_transactions\\_history\\_long](#page-49-1): The most recent transaction events that have ended globally (across all threads).

The following sections describe the transaction event tables. There are also summary tables that aggregate information about transaction events; see [Section 25.12.15.4, "Transaction Summary](#page-81-0) [Tables"](#page-81-0).

For more information about the relationship between the three transaction event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

- [Configuring Transaction Event Collection](#page-43-0)
- [Transaction Boundaries](#page-44-0)
- [Transaction Instrumentation](#page-45-0)
- [Transactions and Nested Events](#page-45-1)
- [Transactions and Stored Programs](#page-46-1)
- [Transactions and Savepoints](#page-46-2)
- [Transactions and Errors](#page-46-3)

## <span id="page-43-0"></span>**Configuring Transaction Event Collection**

To control whether to collect transaction events, set the state of the relevant instruments and consumers:

- The [setup\\_instruments](#page-13-0) table contains an instrument named transaction. Use this instrument to enable or disable collection of individual transaction event classes.
- The [setup\\_consumers](#page-12-0) table contains consumer values with names corresponding to the current and historical transaction event table names. Use these consumers to filter collection of transaction events.

The transaction instrument and the transaction consumers are disabled by default:

```
mysql> SELECT *
 FROM performance_schema.setup_instruments
 WHERE NAME = 'transaction';
+-------------+---------+-------+
| NAME | ENABLED | TIMED |
+-------------+---------+-------+
| transaction | NO | NO |
+-------------+---------+-------+
mysql> SELECT *
 FROM performance_schema.setup_consumers
 WHERE NAME LIKE 'events_transactions%';
+----------------------------------+---------+
| NAME | ENABLED |
+----------------------------------+---------+
| events_transactions_current | NO |
| events_transactions_history | NO |
| events_transactions_history_long | NO |
+----------------------------------+---------+
```

To control transaction event collection at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='transaction=ON'
performance-schema-consumer-events-transactions-current=ON
performance-schema-consumer-events-transactions-history=ON
performance-schema-consumer-events-transactions-history-long=ON
```

• Disable:

```
[mysqld]
performance-schema-instrument='transaction=OFF'
performance-schema-consumer-events-transactions-current=OFF
performance-schema-consumer-events-transactions-history=OFF
performance-schema-consumer-events-transactions-history-long=OFF
```

To control transaction event collection at runtime, update the [setup\\_instruments](#page-13-0) and [setup\\_consumers](#page-12-0) tables:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME = 'transaction';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'YES'
WHERE NAME LIKE 'events_transactions%';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
```

```
WHERE NAME = 'transaction';
UPDATE performance_schema.setup_consumers
SET ENABLED = 'NO'
WHERE NAME LIKE 'events_transactions%';
```

To collect transaction events only for specific transaction event tables, enable the transaction instrument but only the transaction consumers corresponding to the desired tables.

The [setup\\_timers](#page-15-0) table contains a row with a NAME value of transaction that indicates the unit for transaction event timing. The default unit is NANOSECOND:

```
mysql> SELECT *
 FROM performance_schema.setup_timers
 WHERE NAME = 'transaction';
+-------------+------------+
| NAME | TIMER_NAME |
+-------------+------------+
| transaction | NANOSECOND |
+-------------+------------+
```

To change the timing unit, modify the TIMER\_NAME value:

```
UPDATE performance_schema.setup_timers
SET TIMER_NAME = 'MICROSECOND'
WHERE NAME = 'transaction';
```

For additional information about configuring event collection, see Section 25.3, "Performance Schema Startup Configuration", and Section 25.4, "Performance Schema Runtime Configuration".

## <span id="page-44-0"></span>**Transaction Boundaries**

In MySQL Server, transactions start explicitly with these statements:

```
START TRANSACTION | BEGIN | XA START | XA BEGIN
```

Transactions also start implicitly. For example, when the autocommit system variable is enabled, the start of each statement starts a new transaction.

When autocommit is disabled, the first statement following a committed transaction marks the start of a new transaction. Subsequent statements are part of the transaction until it is committed.

Transactions explicitly end with these statements:

```
COMMIT | ROLLBACK | XA COMMIT | XA ROLLBACK
```

Transactions also end implicitly, by execution of DDL statements, locking statements, and server administration statements.

In the following discussion, references to START TRANSACTION also apply to BEGIN, XA START, and XA BEGIN. Similarly, references to COMMIT and ROLLBACK apply to XA COMMIT and XA ROLLBACK, respectively.

The Performance Schema defines transaction boundaries similarly to that of the server. The start and end of a transaction event closely match the corresponding state transitions in the server:

- For an explicitly started transaction, the transaction event starts during processing of the START TRANSACTION statement.
- For an implicitly started transaction, the transaction event starts on the first statement that uses a transactional engine after the previous transaction has ended.
- For any transaction, whether explicitly or implicitly ended, the transaction event ends when the server transitions out of the active transaction state during the processing of COMMIT or ROLLBACK.

There are subtle implications to this approach:

- Transaction events in the Performance Schema do not fully include the statement events associated with the corresponding START TRANSACTION, COMMIT, or ROLLBACK statements. There is a trivial amount of timing overlap between the transaction event and these statements.
- Statements that work with nontransactional engines have no effect on the transaction state of the connection. For implicit transactions, the transaction event begins with the first statement that uses a transactional engine. This means that statements operating exclusively on nontransactional tables are ignored, even following START TRANSACTION.

To illustrate, consider the following scenario:

```
1. SET autocommit = OFF;
2. CREATE TABLE t1 (a INT) ENGINE = InnoDB;
3. START TRANSACTION; -- Transaction 1 START
4. INSERT INTO t1 VALUES (1), (2), (3);
5. CREATE TABLE t2 (a INT) ENGINE = MyISAM; -- Transaction 1 COMMIT
 -- (implicit; DDL forces commit)
6. INSERT INTO t2 VALUES (1), (2), (3); -- Update nontransactional table
7. UPDATE t2 SET a = a + 1; -- ... and again
8. INSERT INTO t1 VALUES (4), (5), (6); -- Write to transactional table
 -- Transaction 2 START (implicit)
9. COMMIT; -- Transaction 2 COMMIT
```

From the perspective of the server, Transaction 1 ends when table t2 is created. Transaction 2 does not start until a transactional table is accessed, despite the intervening updates to nontransactional tables.

From the perspective of the Performance Schema, Transaction 2 starts when the server transitions into an active transaction state. Statements 6 and 7 are not included within the boundaries of Transaction 2, which is consistent with how the server writes transactions to the binary log.

## <span id="page-45-0"></span>**Transaction Instrumentation**

Three attributes define transactions:

- Access mode (read only, read write)
- Isolation level (SERIALIZABLE, REPEATABLE READ, and so forth)
- Implicit (autocommit enabled) or explicit (autocommit disabled)

To reduce complexity of the transaction instrumentation and to ensure that the collected transaction data provides complete, meaningful results, all transactions are instrumented independently of access mode, isolation level, or autocommit mode.

To selectively examine transaction history, use the attribute columns in the transaction event tables: ACCESS\_MODE, ISOLATION\_LEVEL, and AUTOCOMMIT.

The cost of transaction instrumentation can be reduced various ways, such as enabling or disabling transaction instrumentation according to user, account, host, or thread (client connection).

## <span id="page-45-1"></span>**Transactions and Nested Events**

The parent of a transaction event is the event that initiated the transaction. For an explicitly started transaction, this includes the START TRANSACTION and COMMIT AND CHAIN statements. For an implicitly started transaction, it is the first statement that uses a transactional engine after the previous transaction ends.

In general, a transaction is the top-level parent to all events initiated during the transaction, including statements that explicitly end the transaction such as COMMIT and ROLLBACK. Exceptions are

statements that implicitly end a transaction, such as DDL statements, in which case the current transaction must be committed before the new statement is executed.

## <span id="page-46-1"></span>**Transactions and Stored Programs**

Transactions and stored program events are related as follows:

#### • Stored Procedures

Stored procedures operate independently of transactions. A stored procedure can be started within a transaction, and a transaction can be started or ended from within a stored procedure. If called from within a transaction, a stored procedure can execute statements that force a commit of the parent transaction and then start a new transaction.

If a stored procedure is started within a transaction, that transaction is the parent of the stored procedure event.

If a transaction is started by a stored procedure, the stored procedure is the parent of the transaction event.

#### • Stored Functions

Stored functions are restricted from causing an explicit or implicit commit or rollback. Stored function events can reside within a parent transaction event.

#### • Triggers

Triggers activate as part of a statement that accesses the table with which it is associated, so the parent of a trigger event is always the statement that activates it.

Triggers cannot issue statements that cause an explicit or implicit commit or rollback of a transaction.

#### • Scheduled Events

The execution of the statements in the body of a scheduled event takes place in a new connection. Nesting of a scheduled event within a parent transaction is not applicable.

## <span id="page-46-2"></span>**Transactions and Savepoints**

Savepoint statements are recorded as separate statement events. Transaction events include separate counters for SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT statements issued during the transaction.

## <span id="page-46-3"></span>**Transactions and Errors**

Errors and warnings that occur within a transaction are recorded in statement events, but not in the corresponding transaction event. This includes transaction-specific errors and warnings, such as a rollback on a nontransactional table or GTID consistency errors.

## <span id="page-46-0"></span>**25.12.7.1 The events\_transactions\_current Table**

The [events\\_transactions\\_current](#page-46-0) table contains current transaction events. The table stores one row per thread showing the current status of the thread's most recent monitored transaction event, so there is no system variable for configuring the table size. For example:

```
mysql> SELECT *
 FROM performance_schema.events_transactions_current LIMIT 1\G
*************************** 1. row ***************************
 THREAD_ID: 26
 EVENT_ID: 7
 END_EVENT_ID: NULL
 EVENT_NAME: transaction
```

```
 STATE: ACTIVE
 TRX_ID: NULL
 GTID: 3E11FA47-71CA-11E1-9E33-C80AA9429562:56
 XID: NULL
 XA_STATE: NULL
 SOURCE: transaction.cc:150
 TIMER_START: 420833537900000
 TIMER_END: NULL
 TIMER_WAIT: NULL
 ACCESS_MODE: READ WRITE
 ISOLATION_LEVEL: REPEATABLE READ
 AUTOCOMMIT: NO
 NUMBER_OF_SAVEPOINTS: 0
NUMBER_OF_ROLLBACK_TO_SAVEPOINT: 0
 NUMBER_OF_RELEASE_SAVEPOINT: 0
 OBJECT_INSTANCE_BEGIN: NULL
 NESTING_EVENT_ID: 6
 NESTING_EVENT_TYPE: STATEMENT
```

Of the tables that contain transaction event rows, [events\\_transactions\\_current](#page-46-0) is the most fundamental. Other tables that contain transaction event rows are logically derived from the current events. For example, the [events\\_transactions\\_history](#page-49-0) and [events\\_transactions\\_history\\_long](#page-49-1) tables are collections of the most recent transaction events that have ended, up to a maximum number of rows per thread and globally across all threads, respectively.

For more information about the relationship between the three transaction event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect transaction events, see [Section 25.12.7,](#page-42-0) ["Performance Schema Transaction Tables"](#page-42-0).

The [events\\_transactions\\_current](#page-46-0) table has these columns:

• THREAD\_ID, EVENT\_ID

The thread associated with the event and the thread current event number when the event starts. The THREAD\_ID and EVENT\_ID values taken together uniquely identify the row. No two rows have the same pair of values.

• END\_EVENT\_ID

This column is set to NULL when the event starts and updated to the thread current event number when the event ends.

• EVENT\_NAME

The name of the instrument from which the event was collected. This is a NAME value from the [setup\\_instruments](#page-13-0) table. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions".

• STATE

The current transaction state. The value is ACTIVE (after START TRANSACTION or BEGIN), COMMITTED (after COMMIT), or ROLLED BACK (after ROLLBACK).

• TRX\_ID

Unused.

• GTID

The GTID column contains the value of gtid\_next, which can be one of ANONYMOUS, AUTOMATIC, or a GTID using the format UUID:NUMBER. For transactions that use gtid\_next=AUTOMATIC,

which is all normal client transactions, the GTID column changes when the transaction commits and the actual GTID is assigned. If gtid\_mode is either ON or ON\_PERMISSIVE, the GTID column changes to the transaction's GTID. If gtid\_mode is either OFF or OFF\_PERMISSIVE, the GTID column changes to ANONYMOUS.

• XID\_FORMAT\_ID, XID\_GTRID, and XID\_BQUAL

The elements of the XA transaction identifier. They have the format described in Section 13.3.7.1, "XA Transaction SQL Statements".

• XA\_STATE

The state of the XA transaction. The value is ACTIVE (after XA START), IDLE (after XA END), PREPARED (after XA PREPARE), ROLLED BACK (after XA ROLLBACK), or COMMITTED (after XA COMMIT).

On a replica, the same XA transaction can appear in the [events\\_transactions\\_current](#page-46-0) table with different states on different threads. This is because immediately after the XA transaction is prepared, it is detached from the replication applier thread, and can be committed or rolled back by any thread on the replica. The [events\\_transactions\\_current](#page-46-0) table displays the current status of the most recent monitored transaction event on the thread, and does not update this status when the thread is idle. So the XA transaction can still be displayed in the PREPARED state for the original applier thread, after it has been processed by another thread. To positively identify XA transactions that are still in the PREPARED state and need to be recovered, use the XA RECOVER statement rather than the Performance Schema transaction tables.

• SOURCE

The name of the source file containing the instrumented code that produced the event and the line number in the file at which the instrumentation occurs. This enables you to check the source to determine exactly what code is involved.

• TIMER\_START, TIMER\_END, TIMER\_WAIT

Timing information for the event. The unit for these values is picoseconds (trillionths of a second). The TIMER\_START and TIMER\_END values indicate when event timing started and ended. TIMER\_WAIT is the event elapsed time (duration).

If an event has not finished, TIMER\_END is the current timer value and TIMER\_WAIT is the time elapsed so far (TIMER\_END − TIMER\_START).

If an event is produced from an instrument that has TIMED = NO, timing information is not collected, and TIMER\_START, TIMER\_END, and TIMER\_WAIT are all NULL.

For discussion of picoseconds as the unit for event times and factors that affect time values, see Section 25.4.1, "Performance Schema Event Timing".

• ACCESS\_MODE

The transaction access mode. The value is READ WRITE or READ ONLY.

• ISOLATION\_LEVEL

The transaction isolation level. The value is REPEATABLE READ, READ COMMITTED, READ UNCOMMITTED, or SERIALIZABLE.

• AUTOCOMMIT

Whether autcommit mode was enabled when the transaction started.

• NUMBER\_OF\_SAVEPOINTS, NUMBER\_OF\_ROLLBACK\_TO\_SAVEPOINT, NUMBER\_OF\_RELEASE\_SAVEPOINT

The number of SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT statements issued during the transaction.

• OBJECT\_INSTANCE\_BEGIN

Unused.

• NESTING\_EVENT\_ID

The EVENT\_ID value of the event within which this event is nested.

• NESTING\_EVENT\_TYPE

The nesting event type. The value is TRANSACTION, STATEMENT, STAGE, or WAIT. (TRANSACTION does not appear because transactions cannot be nested.)

TRUNCATE TABLE is permitted for the [events\\_transactions\\_current](#page-46-0) table. It removes the rows.

## <span id="page-49-0"></span>**25.12.7.2 The events\_transactions\_history Table**

The [events\\_transactions\\_history](#page-49-0) table contains the N most recent transaction events that have ended per thread. Transaction events are not added to the table until they have ended. When the table contains the maximum number of rows for a given thread, the oldest thread row is discarded when a new row for that thread is added. When a thread ends, all its rows are discarded.

The Performance Schema autosizes the value of N during server startup. To set the number of rows per thread explicitly, set the [performance\\_schema\\_events\\_transactions\\_history\\_size](#page-112-1) system variable at server startup.

The [events\\_transactions\\_history](#page-49-0) table has the same columns as [events\\_transactions\\_current](#page-46-0). See [Section 25.12.7.1, "The events\\_transactions\\_current Table".](#page-46-0)

TRUNCATE TABLE is permitted for the [events\\_transactions\\_history](#page-49-0) table. It removes the rows.

For more information about the relationship between the three transaction event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect transaction events, see [Section 25.12.7,](#page-42-0) ["Performance Schema Transaction Tables"](#page-42-0).

## <span id="page-49-1"></span>**25.12.7.3 The events\_transactions\_history\_long Table**

The [events\\_transactions\\_history\\_long](#page-49-1) table contains the N most recent transaction events that have ended globally, across all threads. Transaction events are not added to the table until they have ended. When the table becomes full, the oldest row is discarded when a new row is added, regardless of which thread generated either row.

The Performance Schema autosizes the value of N is autosized at server startup. To set the table size explicitly, set the [performance\\_schema\\_events\\_transactions\\_history\\_long\\_size](#page-112-2) system variable at server startup.

The [events\\_transactions\\_history\\_long](#page-49-1) table has the same columns as [events\\_transactions\\_current](#page-46-0). See [Section 25.12.7.1, "The events\\_transactions\\_current Table".](#page-46-0)

TRUNCATE TABLE is permitted for the [events\\_transactions\\_history\\_long](#page-49-1) table. It removes the rows.

For more information about the relationship between the three transaction event tables, see [Section 25.9, "Performance Schema Tables for Current and Historical Events".](#page-1-0)

For information about configuring whether to collect transaction events, see [Section 25.12.7,](#page-42-0) ["Performance Schema Transaction Tables"](#page-42-0).

# <span id="page-50-0"></span>**25.12.8 Performance Schema Connection Tables**

When a client connects to the MySQL server, it does so under a particular user name and from a particular host. The Performance Schema provides statistics about these connections, tracking them per account (user and host combination) as well as separately per user name and host name, using these tables:

- [accounts](#page-51-0): Connection statistics per client account
- [hosts](#page-52-0): Connection statistics per client host name
- [users](#page-52-1): Connection statistics per client user name

The meaning of "account" in the connection tables is similar to its meaning in the MySQL grant tables in the mysql system database, in the sense that the term refers to a combination of user and host values. They differ in that, for grant tables, the host part of an account can be a pattern, whereas for Performance Schema tables, the host value is always a specific nonpattern host name.

Each connection table has CURRENT\_CONNECTIONS and TOTAL\_CONNECTIONS columns to track the current and total number of connections per "tracking value" on which its statistics are based. The tables differ in what they use for the tracking value. The [accounts](#page-51-0) table has USER and HOST columns to track connections per user and host combination. The [users](#page-52-1) and [hosts](#page-52-0) tables have a USER and HOST column, respectively, to track connections per user name and host name.

The Performance Schema also counts internal threads and threads for user sessions that failed to authenticate, using rows with USER and HOST column values of NULL.

Suppose that clients named user1 and user2 each connect one time from hosta and hostb. The Performance Schema tracks the connections as follows:

- The [accounts](#page-51-0) table has four rows, for the user1/hosta, user1/hostb, user2/hosta, and user2/hostb account values, each row counting one connection per account.
- The [hosts](#page-52-0) table has two rows, for hosta and hostb, each row counting two connections per host name.
- The [users](#page-52-1) table has two rows, for user1 and user2, each row counting two connections per user name.

When a client connects, the Performance Schema determines which row in each connection table applies, using the tracking value appropriate to each table. If there is no such row, one is added. Then the Performance Schema increments by one the CURRENT\_CONNECTIONS and TOTAL\_CONNECTIONS columns in that row.

When a client disconnects, the Performance Schema decrements by one the CURRENT\_CONNECTIONS column in the row and leaves the TOTAL\_CONNECTIONS column unchanged.

TRUNCATE TABLE is permitted for connection tables. It has these effects:

- Rows are removed for accounts, hosts, or users that have no current connections (rows with CURRENT\_CONNECTIONS = 0).
- Nonremoved rows are reset to count only current connections: For rows with CURRENT\_CONNECTIONS > 0, TOTAL\_CONNECTIONS is reset to CURRENT\_CONNECTIONS.
- Summary tables that depend on the connection table are implicitly truncated, as described later in this section.

The Performance Schema maintains summary tables that aggregate connection statistics for various event types by account, host, or user. These tables have \_summary\_by\_account, \_summary\_by\_host, or \_summary\_by\_user in the name. To identify them, use this query:

```
mysql> SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
 WHERE TABLE_SCHEMA = 'performance_schema'
 AND TABLE_NAME REGEXP '_summary_by_(account|host|user)'
 ORDER BY TABLE_NAME;
+------------------------------------------------------+
| TABLE_NAME |
+------------------------------------------------------+
| events_stages_summary_by_account_by_event_name |
| events_stages_summary_by_host_by_event_name |
| events_stages_summary_by_user_by_event_name |
| events_statements_summary_by_account_by_event_name |
| events_statements_summary_by_host_by_event_name |
| events_statements_summary_by_user_by_event_name |
| events_transactions_summary_by_account_by_event_name |
| events_transactions_summary_by_host_by_event_name |
| events_transactions_summary_by_user_by_event_name |
| events_waits_summary_by_account_by_event_name |
| events_waits_summary_by_host_by_event_name |
| events_waits_summary_by_user_by_event_name |
| memory_summary_by_account_by_event_name |
| memory_summary_by_host_by_event_name |
| memory_summary_by_user_by_event_name |
+------------------------------------------------------+
```

For details about individual connection summary tables, consult the section that describes tables for the summarized event type:

- Wait event summaries: [Section 25.12.15.1, "Wait Event Summary Tables"](#page-76-0)
- Stage event summaries: [Section 25.12.15.2, "Stage Summary Tables"](#page-77-0)
- Statement event summaries: [Section 25.12.15.3, "Statement Summary Tables"](#page-78-0)
- Transaction event summaries: [Section 25.12.15.4, "Transaction Summary Tables"](#page-81-0)
- Memory event summaries: [Section 25.12.15.9, "Memory Summary Tables"](#page-88-0)

TRUNCATE TABLE is permitted for connection summary tables. It removes rows for accounts, hosts, or users with no connections, and resets the summary columns to zero for the remaining rows. In addition, each summary table that is aggregated by account, host, user, or thread is implicitly truncated by truncation of the connection table on which it depends. The following table describes the relationship between connection table truncation and implicitly truncated tables.

**Table 25.2 Implicit Effects of Connection Table Truncation**

| Truncated Connection Table | Implicitly Truncated Summary Tables    |
|----------------------------|----------------------------------------|
| accounts                   | Tables with names containing           |
|                            | _summary_by_account,                   |
|                            | _summary_by_thread                     |
| hosts                      | Tables with names containing           |
|                            | _summary_by_account, _summary_by_host, |
|                            | _summary_by_thread                     |
| users                      | Tables with names containing           |
|                            | _summary_by_account, _summary_by_user, |
|                            | _summary_by_thread                     |

Truncating a \_summary\_global summary table also implicitly truncates its corresponding connection and thread summary tables. For example, truncating [events\\_waits\\_summary\\_global\\_by\\_event\\_name](#page-76-0) implicitly truncates the wait event summary tables that are aggregated by account, host, user, or thread.

## <span id="page-51-0"></span>**25.12.8.1 The accounts Table**

The [accounts](#page-51-0) table contains a row for each account that has connected to the MySQL server. For each account, the table counts the current and total number of connections. The table size is autosized at server startup. To set the table size explicitly, set the [performance\\_schema\\_accounts\\_size](#page-110-2) system variable at server startup. To disable account statistics, set this variable to 0.

The [accounts](#page-51-0) table has the following columns. For a description of how the Performance Schema maintains rows in this table, including the effect of TRUNCATE TABLE, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

• USER

The client user name for the connection. This is NULL for an internal thread, or for a user session that failed to authenticate.

• HOST

The host from which the client connected. This is NULL for an internal thread, or for a user session that failed to authenticate.

• CURRENT\_CONNECTIONS

The current number of connections for the account.

• TOTAL\_CONNECTIONS

The total number of connections for the account.

## <span id="page-52-0"></span>**25.12.8.2 The hosts Table**

The [hosts](#page-52-0) table contains a row for each host from which clients have connected to the MySQL server. For each host name, the table counts the current and total number of connections. The table size is autosized at server startup. To set the table size explicitly, set the [performance\\_schema\\_hosts\\_size](#page-113-1) system variable at server startup. To disable host statistics, set this variable to 0.

The [hosts](#page-52-0) table has the following columns. For a description of how the Performance Schema maintains rows in this table, including the effect of TRUNCATE TABLE, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

• HOST

The host from which the client connected. This is NULL for an internal thread, or for a user session that failed to authenticate.

• CURRENT\_CONNECTIONS

The current number of connections for the host.

• TOTAL\_CONNECTIONS

The total number of connections for the host.

## <span id="page-52-1"></span>**25.12.8.3 The users Table**

The [users](#page-52-1) table contains a row for each user who has connected to the MySQL server. For each user name, the table counts the current and total number of connections. The table size is autosized at server startup. To set the table size explicitly, set the [performance\\_schema\\_users\\_size](#page-125-0) system variable at server startup. To disable user statistics, set this variable to 0.

The [users](#page-52-1) table has the following columns. For a description of how the Performance Schema maintains rows in this table, including the effect of TRUNCATE TABLE, see [Section 25.12.8,](#page-50-0) ["Performance Schema Connection Tables".](#page-50-0)

• USER

The client user name for the connection. This is NULL for an internal thread, or for a user session that failed to authenticate.

• CURRENT\_CONNECTIONS

The current number of connections for the user.

• TOTAL\_CONNECTIONS

The total number of connections for the user.

# <span id="page-53-1"></span>**25.12.9 Performance Schema Connection Attribute Tables**

Connection attributes are key-value pairs that application programs can pass to the server at connect time. For applications based on the C API implemented by the libmysqlclient client library, the [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-options.md) and [mysql\\_options4\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-options4.md) functions define the connection attribute set. Other MySQL Connectors may provide their own attribute-definition methods.

These Performance Schema tables expose attribute information:

- [session\\_account\\_connect\\_attrs](#page-55-0): Connection attributes for the current session, and other sessions associated with the session account
- [session\\_connect\\_attrs](#page-55-1): Connection attributes for all sessions

Attribute names that begin with an underscore (\_) are reserved for internal use and should not be created by application programs. This convention permits new attributes to be introduced by MySQL without colliding with application attributes, and enables application programs to define their own attributes that do not collide with internal attributes.

- [Available Connection Atrributes](#page-53-0)
- [Connection Atrribute Limits](#page-54-0)

# <span id="page-53-0"></span>**Available Connection Atrributes**

The set of connection attributes visible within a given connection varies depending on factors such as your platform, MySQL Connector used to establish the connection, or client program.

The libmysqlclient client library sets these attributes:

- \_client\_name: The client name (libmysql for the client library).
- \_client\_version: The client library version.
- \_os: The operating system (for example, Linux, Win64).
- \_pid: The client process ID.
- \_platform: The machine platform (for example, x86\_64).
- \_thread: The client thread ID (Windows only).

Other MySQL Connectors may define their own connection attributes.

MySQL Connector/J defines these attributes:

- \_client\_license: The connector license type.
- \_runtime\_vendor: The Java runtime environment (JRE) vendor.

• \_runtime\_version: The Java runtime environment (JRE) version.

MySQL Connector/NET defines these attributes:

- \_client\_version: The client library version.
- \_os: The operating system (for example, Linux, Win64).
- \_pid: The client process ID.
- \_platform: The machine platform (for example, x86\_64).
- \_program\_name: The client name.
- \_thread: The client thread ID (Windows only).

PHP defines attributes that depend on how it was compiled:

- Compiled using libmysqlclient: The standard libmysqlclient attributes, described previously.
- Compiled using mysqlnd: Only the \_client\_name attribute, with a value of mysqlnd.

Many MySQL client programs set a program\_name attribute with a value equal to the client name. For example, mysqladmin and mysqldump set program\_name to mysqladmin and mysqldump, respectively.

Some MySQL client programs define additional attributes:

- mysqlbinlog:
  - \_client\_role: binary\_log\_listener
- Replica connections:
  - program\_name: mysqld
  - \_client\_role: binary\_log\_listener
  - \_client\_replication\_channel\_name: The channel name.
- FEDERATED storage engine connections:
  - program\_name: mysqld
  - \_client\_role: federated\_storage

## <span id="page-54-0"></span>**Connection Atrribute Limits**

There are limits on the amount of connection attribute data transmitted from client to server:

- A fixed limit imposed by the client prior to connect time.
- A fixed limit imposed by the server at connect time.
- A configurable limit imposed by the Performance Schema at connect time.

For connections initiated using the C API, the libmysqlclient library imposes a limit of 64KB on the aggregate size of connection attribute data on the client side: Calls to [mysql\\_options\(\)](https://dev.mysql.com/doc/c-api/5.7/en/mysql-options.md) that cause this limit to be exceeded produce a [CR\\_INVALID\\_PARAMETER\\_NO](https://dev.mysql.com/doc/mysql-errors/5.7/en/client-error-reference.md#error_cr_invalid_parameter_no) error. Other MySQL Connectors may impose their own client-side limits on how much connection attribute data can be transmitted to the server.

On the server side, these size checks on connection attribute data occur:

- The server imposes a limit of 64KB on the aggregate size of connection attribute data it can accept. If a client attempts to send more than 64KB of attribute data, the server rejects the connection.
- For accepted connections, the Performance Schema checks aggregate attribute size against the value of the [performance\\_schema\\_session\\_connect\\_attrs\\_size](#page-123-1) system variable. If attribute size exceeds this value, these actions take place:
  - The Performance Schema truncates the attribute data and increments the [Performance\\_schema\\_session\\_connect\\_attrs\\_lost](#page-127-0) status variable, which indicates the number of connections for which attribute truncation occurred.
  - The Performance Schema writes a message to the error log if the log\_error\_verbosity system variable is greater than 1:

[Warning] Connection attributes of length N were truncated

## <span id="page-55-0"></span>**25.12.9.1 The session\_account\_connect\_attrs Table**

Application programs can provide key-value connection attributes to be passed to the server at connect time. For descriptions of common attributes, see [Section 25.12.9, "Performance Schema Connection](#page-53-1) [Attribute Tables"](#page-53-1).

The [session\\_account\\_connect\\_attrs](#page-55-0) table contains connection attributes only for the current session, and other sessions associated with the session account. To see connection attributes for all sessions, use the [session\\_connect\\_attrs](#page-55-1) table.

The [session\\_account\\_connect\\_attrs](#page-55-0) table has these columns:

• PROCESSLIST\_ID

The connection identifier for the session.

• ATTR\_NAME

The attribute name.

• ATTR\_VALUE

The attribute value.

• ORDINAL\_POSITION

The order in which the attribute was added to the set of connection attributes.

TRUNCATE TABLE is not permitted for the [session\\_account\\_connect\\_attrs](#page-55-0) table.

## <span id="page-55-1"></span>**25.12.9.2 The session\_connect\_attrs Table**

Application programs can provide key-value connection attributes to be passed to the server at connect time. For descriptions of common attributes, see [Section 25.12.9, "Performance Schema Connection](#page-53-1) [Attribute Tables"](#page-53-1).

The [session\\_connect\\_attrs](#page-55-1) table contains connection attributes for all sessions. To see connection attributes only for the current session, and other sessions associated with the session account, use the [session\\_account\\_connect\\_attrs](#page-55-0) table.

The [session\\_connect\\_attrs](#page-55-1) table has these columns:

• PROCESSLIST\_ID

The connection identifier for the session.

• ATTR\_NAME

The attribute name.

• ATTR\_VALUE

The attribute value.

• ORDINAL\_POSITION

The order in which the attribute was added to the set of connection attributes.

TRUNCATE TABLE is not permitted for the [session\\_connect\\_attrs](#page-55-1) table.

# <span id="page-56-0"></span>**25.12.10 Performance Schema User-Defined Variable Tables**

The Performance Schema provides a [user\\_variables\\_by\\_thread](#page-56-0) table that exposes user-defined variables. These are variables defined within a specific session and include a @ character preceding the name; see Section 9.4, "User-Defined Variables".

The [user\\_variables\\_by\\_thread](#page-56-0) table has these columns:

• THREAD\_ID

The thread identifier of the session in which the variable is defined.

• VARIABLE\_NAME

The variable name, without the leading @ character.

• VARIABLE\_VALUE

The variable value.

TRUNCATE TABLE is not permitted for the [user\\_variables\\_by\\_thread](#page-56-0) table.