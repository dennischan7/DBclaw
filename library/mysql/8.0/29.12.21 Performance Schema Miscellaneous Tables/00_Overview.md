---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following sections describe tables that do not fall into the table categories discussed in the preceding sections:

- [component\\_scheduler\\_tasks](#page-87-0): The current status of each scheduled task.
- [error\\_log](#page-88-0): The most recent events written to the error log.
- [host\\_cache](#page-91-0): Information from the internal host cache.
- [innodb\\_redo\\_log\\_files](#page-94-0): Information about InnoDB redo log files.
- [log\\_status](#page-94-1): Information about server logs for backup purposes.
- [performance\\_timers](#page-95-0): Which event timers are available.
- [processlist](#page-96-0): Information about server processes.
- [threads](#page-99-0): Information about server threads.
- [tls\\_channel\\_status](#page-104-0): TLS context properties for connection interfaces.
- [user\\_defined\\_functions](#page-105-0): Loadable functions registered by a component, plugin, or CREATE FUNCTION statement.

## <span id="page-87-0"></span>**29.12.21.1 The component\_scheduler\_tasks Table**

The component\_scheduler\_tasks table contains a row for each scheduled task. Each row contains information about the ongoing progress of a task that applications, components, and plugins can implement, optionally, using the scheduler component (see Section 7.5.5, "Scheduler Component"). For example, the audit\_log server plugin utilizes the scheduler component to run a regular, recurring flush of its memory cache:

```
mysql> select * from performance_schema.component_scheduler_tasks\G
*************************** 1. row ***************************
 NAME: plugin_audit_log_flush_scheduler
 STATUS: WAITING
 COMMENT: Registered by the audit log plugin. Does a periodic refresh of the audit log 
 in-memory rules cache by calling audit_log_flush
INTERVAL_SECONDS: 100
 TIMES_RUN: 5
 TIMES_FAILED: 0
1 row in set (0.02 sec)
```

The component\_scheduler\_tasks table has the following columns:

• NAME

The name supplied during the registration.

• STATUS

The values are:

• RUNNING if the task is active and being executed.

- WAITING if the task is idle and waiting for the background thread to pick it up or waiting for the next time it needs to be run to arrive.
- COMMENT

A compile-time comment provided by an application, component, or plugin. In the previous example, MySQL Enterprise Audit provides the comment using a server plugin named audit\_log.

• INTERVAL\_SECONDS

The time in seconds to run a task, which an application, component, or plugin provides. MySQL Enterprise Audit enables you to specify this value using the audit\_log\_flush\_interval\_seconds system variable.

• TIMES\_RUN

A counter that increments by one every time the task runs successfully. It wraps around.

• TIMES\_FAILED

A counter that increments by one every time the execution of the task fails. It wraps around.

## <span id="page-88-0"></span>**29.12.21.2 The error\_log Table**

Of the logs the MySQL server maintains, one is the error log to which it writes diagnostic messages (see Section 7.4.2, "The Error Log"). Typically, the server writes diagnostics to a file on the server host or to a system log service. As of MySQL 8.0.22, depending on error log configuration, the server can also write the most recent error events to the Performance Schema [error\\_log](#page-88-0) table. Granting the SELECT privilege for the [error\\_log](#page-88-0) table thus gives clients and applications access to error log contents using SQL queries, enabling DBAs to provide access to the log without the need to permit direct file system access on the server host.

The [error\\_log](#page-88-0) table supports focused queries based on its more structured columns. It also includes the full text of error messages to support more free-form analysis.

The table implementation uses a fixed-size, in-memory ring buffer, with old events automatically discarded as necessary to make room for new ones.

Example [error\\_log](#page-88-0) contents:

```
mysql> SELECT * FROM performance_schema.error_log\G
*************************** 1. row ***************************
 LOGGED: 2020-08-06 09:25:00.338624
 THREAD_ID: 0
 PRIO: System
ERROR_CODE: MY-010116
 SUBSYSTEM: Server
 DATA: mysqld (mysqld 8.0.23) starting as process 96344
*************************** 2. row ***************************
 LOGGED: 2020-08-06 09:25:00.363521
 THREAD_ID: 1
 PRIO: System
ERROR_CODE: MY-013576
 SUBSYSTEM: InnoDB
 DATA: InnoDB initialization has started.
...
*************************** 65. row ***************************
 LOGGED: 2020-08-06 09:25:02.936146
 THREAD_ID: 0
 PRIO: Warning
ERROR_CODE: MY-010068
 SUBSYSTEM: Server
 DATA: CA certificate /var/mysql/sslinfo/cacert.pem is self signed.
...
*************************** 89. row ***************************
 LOGGED: 2020-08-06 09:25:03.112801
```

```
 THREAD_ID: 0
 PRIO: System
ERROR_CODE: MY-013292
 SUBSYSTEM: Server
 DATA: Admin interface ready for connections, address: '127.0.0.1' port: 33062
```

The [error\\_log](#page-88-0) table has the following columns. As indicated in the descriptions, all but the DATA column correspond to fields of the underlying error event structure, which is described in Section 7.4.2.3, "Error Event Fields".

### • LOGGED

The event timestamp, with microsecond precision. LOGGED corresponds to the time field of error events, although with certain potential differences:

- time values in the error log are displayed according to the log\_timestamps system variable setting; see Early-Startup Logging Output Format.
- The LOGGED column stores values using the TIMESTAMP data type, for which values are stored in UTC but displayed when retrieved in the current session time zone; see Section 13.2.2, "The DATE, DATETIME, and TIMESTAMP Types".

To display LOGGED values in the same time zone as displayed in the error log file, first set the session time zone as follows:

```
SET @@session.time_zone = @@global.log_timestamps;
```

If the log\_timestamps value is UTC and your system does not have named time zone support installed (see Section 7.1.15, "MySQL Server Time Zone Support"), set the time zone like this:

```
SET @@session.time_zone = '+00:00';
```

• THREAD\_ID

The MySQL thread ID. THREAD\_ID corresponds to the thread field of error events.

Within the Performance Schema, the THREAD\_ID column in the [error\\_log](#page-88-0) table is most similar to the PROCESSLIST\_ID column of the [threads](#page-99-0) table:

- For foreground threads, THREAD\_ID and PROCESSLIST\_ID represent a connection identifier. This is the same value displayed in the ID column of the INFORMATION\_SCHEMA PROCESSLIST table, displayed in the Id column of SHOW PROCESSLIST output, and returned by the CONNECTION\_ID() function within the thread.
- For background threads, THREAD\_ID is 0 and PROCESSLIST\_ID is NULL.

Many Performance Schema tables other than [error\\_log](#page-88-0) has a column named THREAD\_ID, but in those tables, the THREAD\_ID column is a value assigned internally by the Performance Schema.

• PRIO

The event priority. Permitted values are System, Error, Warning, Note. The PRIO column is based on the label field of error events, which itself is based on the underlying numeric prio field value.

• ERROR\_CODE

The numeric event error code. ERROR\_CODE corresponds to the error\_code field of error events.

• SUBSYSTEM

The subsystem in which the event occurred. SUBSYSTEM corresponds to the subsystem field of error events.

### • DATA

The text representation of the error event. The format of this value depends on the format produced by the log sink component that generates the [error\\_log](#page-88-0) row. For example, if the log sink is log\_sink\_internal or log\_sink\_json, DATA values represent error events in traditional or JSON format, respectively. (See Section 7.4.2.9, "Error Log Output Format".)

Because the error log can be reconfigured to change the log sink component that supplies rows to the [error\\_log](#page-88-0) table, and because different sinks produce different output formats, it is possible for rows written to the [error\\_log](#page-88-0) table at different times to have different DATA formats.

The [error\\_log](#page-88-0) table has these indexes:

- Primary key on (LOGGED)
- Index on (THREAD\_ID)
- Index on (PRIO)
- Index on (ERROR\_CODE)
- Index on (SUBSYSTEM)

TRUNCATE TABLE is not permitted for the [error\\_log](#page-88-0) table.

### **Implementation and Configuration of the error\_log Table**

The Performance Schema [error\\_log](#page-88-0) table is populated by error log sink components that write to the table in addition to writing formatted error events to the error log. Performance Schema support by log sinks has two parts:

- A log sink can write new error events to the [error\\_log](#page-88-0) table as they occur.
- A log sink can provide a parser for extraction of previously written error messages. This enables a server instance to read messages written to an error log file by the previous instance and store them in the [error\\_log](#page-88-0) table. Messages written during shutdown by the previous instance may be useful for diagnosing why shutdown occurred.

Currently, the traditional-format log\_sink\_internal and JSON-format log\_sink\_json sinks support writing new events to the [error\\_log](#page-88-0) table and provide a parser for reading previously written error log files.

The log\_error\_services system variable controls which log components to enable for error logging. Its value is a pipeline of log filter and log sink components to be executed in left-to-right order when error events occur. The log\_error\_services value pertains to populating the [error\\_log](#page-88-0) table as follows:

- At startup, the server examines the log\_error\_services value and chooses from it the leftmost log sink that satisfies these conditions:
  - A sink that supports the [error\\_log](#page-88-0) table and provides a parser.
  - If none, a sink that supports the [error\\_log](#page-88-0) table but provides no parser.

If no log sink satisfies those conditions, the [error\\_log](#page-88-0) table remains empty. Otherwise, if the sink provides a parser and log configuration enables a previously written error log file to be found, the server uses the sink parser to read the last part of the file and writes the old events it contains to the table. The sink then writes new error events to the table as they occur.

• At runtime, if the value of log\_error\_services changes, the server again examines it, this time looking for the leftmost enabled log sink that supports the [error\\_log](#page-88-0) table, regardless of whether it provides a parser.

If no such log sink exists, no additional error events are written to the [error\\_log](#page-88-0) table. Otherwise, the newly configured sink writes new error events to the table as they occur.

Any configuration that affects output written to the error log affects [error\\_log](#page-88-0) table contents. This includes settings such as those for verbosity, message suppression, and message filtering. It also applies to information read at startup from a previous log file. For example, messages not written during a previous server instance configured with low verbosity do not become available if the file is read by a current instance configured with higher verbosity.

The [error\\_log](#page-88-0) table is a view on a fixed-size, in-memory ring buffer, with old events automatically discarded as necessary to make room for new ones. As shown in the following table, several status variables provide information about ongoing [error\\_log](#page-88-0) operation.

| Status Variable           | Meaning                     |  |
|---------------------------|-----------------------------|--|
| Error_log_buffered_bytes  | Bytes used in table         |  |
| Error_log_buffered_events | Events present in table     |  |
| Error_log_expired_events  | Events discarded from table |  |
| Error_log_latest_write    | Time of last write to table |  |

### <span id="page-91-0"></span>**29.12.21.3 The host\_cache Table**

The MySQL server maintains an in-memory host cache that contains client host name and IP address information and is used to avoid Domain Name System (DNS) lookups. The [host\\_cache](#page-91-0) table exposes the contents of this cache. The host\_cache\_size system variable controls the size of the host cache, as well as the size of the [host\\_cache](#page-91-0) table. For operational and configuration information about the host cache, see Section 7.1.12.3, "DNS Lookups and the Host Cache".

Because the [host\\_cache](#page-91-0) table exposes the contents of the host cache, it can be examined using SELECT statements. This may help you diagnose the causes of connection problems.

The [host\\_cache](#page-91-0) table has these columns:

• IP

The IP address of the client that connected to the server, expressed as a string.

• HOST

The resolved DNS host name for that client IP, or NULL if the name is unknown.

• HOST\_VALIDATED

Whether the IP-to-host name-to-IP DNS resolution was performed successfully for the client IP. If HOST\_VALIDATED is YES, the HOST column is used as the host name corresponding to the IP so that additional calls to DNS can be avoided. While HOST\_VALIDATED is NO, DNS resolution is attempted for each connection attempt, until it eventually completes with either a valid result or a permanent error. This information enables the server to avoid caching bad or missing host names during temporary DNS failures, which would negatively affect clients forever.

• SUM\_CONNECT\_ERRORS

The number of connection errors that are deemed "blocking" (assessed against the max\_connect\_errors system variable). Only protocol handshake errors are counted, and only for hosts that passed validation (HOST\_VALIDATED = YES).

Once SUM\_CONNECT\_ERRORS for a given host reaches the value of max\_connect\_errors, new connections from that host are blocked. The SUM\_CONNECT\_ERRORS value can exceed the max\_connect\_errors value because multiple connection attempts from a host can occur simultaneously while the host is not blocked. Any or all of them can fail, independently incrementing SUM\_CONNECT\_ERRORS, possibly beyond the value of max\_connect\_errors.

Suppose that max\_connect\_errors is 200 and SUM\_CONNECT\_ERRORS for a given host is 199. If 10 clients attempt to connect from that host simultaneously, none of them are blocked because SUM\_CONNECT\_ERRORS has not reached 200. If blocking errors occur for five of the clients, SUM\_CONNECT\_ERRORS is increased by one for each client, for a resulting SUM\_CONNECT\_ERRORS value of 204. The other five clients succeed and are not blocked because the value of SUM\_CONNECT\_ERRORS when their connection attempts began had not reached 200. New connections from the host that begin after SUM\_CONNECT\_ERRORS reaches 200 are blocked.

• COUNT\_HOST\_BLOCKED\_ERRORS

The number of connections that were blocked because SUM\_CONNECT\_ERRORS exceeded the value of the max\_connect\_errors system variable.

• COUNT\_NAMEINFO\_TRANSIENT\_ERRORS

The number of transient errors during IP-to-host name DNS resolution.

• COUNT\_NAMEINFO\_PERMANENT\_ERRORS

The number of permanent errors during IP-to-host name DNS resolution.

• COUNT\_FORMAT\_ERRORS

The number of host name format errors. MySQL does not perform matching of Host column values in the mysql.user system table against host names for which one or more of the initial components of the name are entirely numeric, such as 1.2.example.com. The client IP address is used instead. For the rationale why this type of matching does not occur, see Section 8.2.4, "Specifying Account Names".

• COUNT\_ADDRINFO\_TRANSIENT\_ERRORS

The number of transient errors during host name-to-IP reverse DNS resolution.

• COUNT\_ADDRINFO\_PERMANENT\_ERRORS

The number of permanent errors during host name-to-IP reverse DNS resolution.

• COUNT\_FCRDNS\_ERRORS

The number of forward-confirmed reverse DNS errors. These errors occur when IP-to-host name-to-IP DNS resolution produces an IP address that does not match the client originating IP address.

• COUNT\_HOST\_ACL\_ERRORS

The number of errors that occur because no users are permitted to connect from the client host. In such cases, the server returns [ER\\_HOST\\_NOT\\_PRIVILEGED](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.md#error_er_host_not_privileged) and does not even ask for a user name or password.

• COUNT\_NO\_AUTH\_PLUGIN\_ERRORS

The number of errors due to requests for an unavailable authentication plugin. A plugin can be unavailable if, for example, it was never loaded or a load attempt failed.

• COUNT\_AUTH\_PLUGIN\_ERRORS

The number of errors reported by authentication plugins.

An authentication plugin can report different error codes to indicate the root cause of a failure. Depending on the type of error, one of these columns is

incremented: COUNT\_AUTHENTICATION\_ERRORS, COUNT\_AUTH\_PLUGIN\_ERRORS, COUNT\_HANDSHAKE\_ERRORS. New return codes are an optional extension to the existing plugin API. Unknown or unexpected plugin errors are counted in the COUNT\_AUTH\_PLUGIN\_ERRORS column.

• COUNT\_HANDSHAKE\_ERRORS

The number of errors detected at the wire protocol level.

• COUNT\_PROXY\_USER\_ERRORS

The number of errors detected when proxy user A is proxied to another user B who does not exist.

• COUNT\_PROXY\_USER\_ACL\_ERRORS

The number of errors detected when proxy user A is proxied to another user B who does exist but for whom A does not have the PROXY privilege.

• COUNT\_AUTHENTICATION\_ERRORS

The number of errors caused by failed authentication.

• COUNT\_SSL\_ERRORS

The number of errors due to SSL problems.

• COUNT\_MAX\_USER\_CONNECTIONS\_ERRORS

The number of errors caused by exceeding per-user connection quotas. See Section 8.2.21, "Setting Account Resource Limits".

• COUNT\_MAX\_USER\_CONNECTIONS\_PER\_HOUR\_ERRORS

The number of errors caused by exceeding per-user connections-per-hour quotas. See Section 8.2.21, "Setting Account Resource Limits".

• COUNT\_DEFAULT\_DATABASE\_ERRORS

The number of errors related to the default database. For example, the database does not exist or the user has no privileges to access it.

• COUNT\_INIT\_CONNECT\_ERRORS

The number of errors caused by execution failures of statements in the init\_connect system variable value.

• COUNT\_LOCAL\_ERRORS

The number of errors local to the server implementation and not related to the network, authentication, or authorization. For example, out-of-memory conditions fall into this category.

• COUNT\_UNKNOWN\_ERRORS

The number of other, unknown errors not accounted for by other columns in this table. This column is reserved for future use, in case new error conditions must be reported, and if preserving the backward compatibility and structure of the [host\\_cache](#page-91-0) table is required.

• FIRST\_SEEN

The timestamp of the first connection attempt seen from the client in the IP column.

• LAST\_SEEN

The timestamp of the most recent connection attempt seen from the client in the IP column.

• FIRST\_ERROR\_SEEN

The timestamp of the first error seen from the client in the IP column.

• LAST\_ERROR\_SEEN

The timestamp of the most recent error seen from the client in the IP column.

The [host\\_cache](#page-91-0) table has these indexes:

- Primary key on (IP)
- Index on (HOST)

TRUNCATE TABLE is permitted for the [host\\_cache](#page-91-0) table. It requires the DROP privilege for the table. Truncating the table flushes the host cache, which has the effects described in Flushing the Host Cache.

# <span id="page-94-0"></span>**29.12.21.4 The innodb\_redo\_log\_files Table**

The innodb\_redo\_log\_files table contains a row for each active InnoDB redo log file. This table was introduced in MySQL 8.0.30.

The innodb\_redo\_log\_files table has the following columns:

• FILE\_ID

The ID of the redo log file. The value corresponds to the redo log file number.

• FILE\_NAME

The path and file name of the redo log file.

• START\_LSN

The log sequence number of the first block in the redo log file.

• END\_LSN

The log sequence number after the last block in the redo log file.

• SIZE\_IN\_BYTES

The size of the redo log data in the file, in bytes. Data size is measured from the END\_LSN to the start >START\_LSN. The redo log file size on disk is slightly larger due to the file header (2048 bytes), which is not included in the value reported by this column.

• IS\_FULL

Whether the redo log file is full. A value of 0 indicates that free space in the file. A value of 1 indicates that the file is full.

• CONSUMER\_LEVEL

Reserved for future use.

### <span id="page-94-1"></span>**29.12.21.5 The log\_status Table**

The [log\\_status](#page-94-1) table provides information that enables an online backup tool to copy the required log files without locking those resources for the duration of the copy process.

When the [log\\_status](#page-94-1) table is queried, the server blocks logging and related administrative changes for just long enough to populate the table, then releases the resources. The [log\\_status](#page-94-1) table informs the online backup which point it should copy up to in the source's binary log and gtid\_executed record, and the relay log for each replication channel. It also provides relevant information for individual storage engines, such as the last log sequence number (LSN) and the LSN of the last checkpoint taken for the InnoDB storage engine.

The log\_status table has these columns:

### • SERVER\_UUID

The server UUID for this server instance. This is the generated unique value of the read-only system variable server\_uuid.

### • LOCAL

The log position state information from the source, provided as a single JSON object with the following keys:

| binary_log_file     | The name of the current binary log file.                                                                                                                                                                    |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| binary_log_position | The current binary log position at the time the log_status table<br>was accessed.                                                                                                                           |
| gtid_executed       | The current value of the global server variable gtid_executed<br>at the time the log_status table was accessed. This<br>information is consistent with the binary_log_file and<br>binary_log_position keys. |

### • REPLICATION

A JSON array of channels, each with the following information:

| channel_name   | The name of the replication channel. The default replication<br>channel's name is the empty string (""). |
|----------------|----------------------------------------------------------------------------------------------------------|
| relay_log_file | The name of the current relay log file for the replication channel.                                      |
| relay_log_pos  | The current relay log position at the time the log_status table<br>was accessed.                         |

### • STORAGE\_ENGINES

Relevant information from individual storage engines, provided as a JSON object with one key for each applicable storage engine.

The [log\\_status](#page-94-1) table has no indexes.

The BACKUP\_ADMIN privilege, as well as the SELECT privilege, is required for access to the [log\\_status](#page-94-1) table.

TRUNCATE TABLE is not permitted for the [log\\_status](#page-94-1) table.

### <span id="page-95-0"></span>**29.12.21.6 The performance\_timers Table**

The [performance\\_timers](#page-95-0) table shows which event timers are available:

|                                |                                | mysql> SELECT * FROM performance_schema.performance_timers;<br>+++++ |              |
|--------------------------------|--------------------------------|----------------------------------------------------------------------|--------------|
|                                |                                | TIMER_NAME   TIMER_FREQUENCY   TIMER_RESOLUTION   TIMER_OVERHEAD     |              |
| CYCLE<br>  NANOSECOND          | <br>2389029850  <br>1000000000 | +++++<br>1  <br>1                                                    | 72  <br>112  |
| MICROSECOND  <br>  MILLISECOND | 1000000  <br>1036              | 1  <br>1                                                             | 136  <br>168 |

```
| THREAD_CPU | 339101694 | 1 | 798 |
+-------------+-----------------+------------------+----------------+
```

If the values associated with a given timer name are NULL, that timer is not supported on your platform. For an explanation of how event timing occurs, see Section 29.4.1, "Performance Schema Event Timing".

The [performance\\_timers](#page-95-0) table has these columns:

• TIMER\_NAME

The timer name.

• TIMER\_FREQUENCY

The number of timer units per second. For a cycle timer, the frequency is generally related to the CPU speed. For example, on a system with a 2.4GHz processor, the CYCLE may be close to 2400000000.

• TIMER\_RESOLUTION

Indicates the number of timer units by which timer values increase. If a timer has a resolution of 10, its value increases by 10 each time.

• TIMER\_OVERHEAD

The minimal number of cycles of overhead to obtain one timing with the given timer. The Performance Schema determines this value by invoking the timer 20 times during initialization and picking the smallest value. The total overhead really is twice this amount because the instrumentation invokes the timer at the start and end of each event. The timer code is called only for timed events, so this overhead does not apply for nontimed events.

The [performance\\_timers](#page-95-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [performance\\_timers](#page-95-0) table.

### <span id="page-96-0"></span>**29.12.21.7 The processlist Table**

The MySQL process list indicates the operations currently being performed by the set of threads executing within the server. The [processlist](#page-96-0) table is one source of process information. For a comparison of this table with other sources, see Sources of Process Information.

The [processlist](#page-96-0) table can be queried directly. If you have the PROCESS privilege, you can see all threads, even those belonging to other users. Otherwise (without the PROCESS privilege), nonanonymous users have access to information about their own threads but not threads for other users, and anonymous users have no access to thread information.

![](_page_96_Picture_17.jpeg)

### **Note**

If the [performance\\_schema\\_show\\_processlist](#page-129-1) system variable is enabled, the [processlist](#page-96-0) table also serves as the basis for an alternative implementation underlying the SHOW PROCESSLIST statement. For details, see later in this section.

The [processlist](#page-96-0) table contains a row for each server process:

```
mysql> SELECT * FROM performance_schema.processlist\G
*************************** 1. row ***************************
 ID: 5
 USER: event_scheduler
 HOST: localhost
 DB: NULL
COMMAND: Daemon
```

```
 TIME: 137
 STATE: Waiting on empty queue
 INFO: NULL
*************************** 2. row ***************************
 ID: 9
 USER: me
 HOST: localhost:58812
 DB: NULL
COMMAND: Sleep
 TIME: 95
 STATE:
 INFO: NULL
*************************** 3. row ***************************
 ID: 10
 USER: me
 HOST: localhost:58834
 DB: test
COMMAND: Query
 TIME: 0
 STATE: executing
 INFO: SELECT * FROM performance_schema.processlist
...
```

The [processlist](#page-96-0) table has these columns:

• ID

The connection identifier. This is the same value displayed in the Id column of the SHOW PROCESSLIST statement, displayed in the PROCESSLIST\_ID column of the Performance Schema [threads](#page-99-0) table, and returned by the CONNECTION\_ID() function within the thread.

• USER

The MySQL user who issued the statement. A value of system user refers to a nonclient thread spawned by the server to handle tasks internally, for example, a delayed-row handler thread or an I/O or SQL thread used on replica hosts. For system user, there is no host specified in the Host column. unauthenticated user refers to a thread that has become associated with a client connection but for which authentication of the client user has not yet occurred. event\_scheduler refers to the thread that monitors scheduled events (see Section 27.4, "Using the Event Scheduler").

![](_page_97_Picture_7.jpeg)

### **Note**

A USER value of system user is distinct from the SYSTEM\_USER privilege. The former designates internal threads. The latter distinguishes the system user and regular user account categories (see Section 8.2.11, "Account Categories").

• HOST

The host name of the client issuing the statement (except for system user, for which there is no host). The host name for TCP/IP connections is reported in host\_name:client\_port format to make it easier to determine which client is doing what.

• DB

The default database for the thread, or NULL if none has been selected.

• COMMAND

The type of command the thread is executing on behalf of the client, or Sleep if the session is idle. For descriptions of thread commands, see Section 10.14, "Examining Server Thread (Process) Information". The value of this column corresponds to the COM\_xxx commands of the client/server protocol and Com\_xxx status variables. See Section 7.1.10, "Server Status Variables"

• TIME

The time in seconds that the thread has been in its current state. For a replica SQL thread, the value is the number of seconds between the timestamp of the last replicated event and the real time of the replica host. See Section 19.2.3, "Replication Threads".

### • STATE

An action, event, or state that indicates what the thread is doing. For descriptions of STATE values, see Section 10.14, "Examining Server Thread (Process) Information".

Most states correspond to very quick operations. If a thread stays in a given state for many seconds, there might be a problem that needs to be investigated.

### • INFO

The statement the thread is executing, or NULL if it is executing no statement. The statement might be the one sent to the server, or an innermost statement if the statement executes other statements. For example, if a CALL statement executes a stored procedure that is executing a SELECT statement, the INFO value shows the SELECT statement.

• EXECUTION\_ENGINE

The query execution engine. The value is either PRIMARY or SECONDARY. For use with MySQL HeatWave Service and MySQL HeatWave, where the PRIMARY engine is InnoDB and the SECONDARY engine is MySQL HeatWave (RAPID). For MySQL Community Edition Server, MySQL Enterprise Edition Server (on-premise), and MySQL HeatWave Service without MySQL HeatWave, the value is always PRIMARY. This column was added in MySQL 8.0.29.

The [processlist](#page-96-0) table has these indexes:

• Primary key on (ID)

TRUNCATE TABLE is not permitted for the [processlist](#page-96-0) table.

As mentioned previously, if the [performance\\_schema\\_show\\_processlist](#page-129-1) system variable is enabled, the [processlist](#page-96-0) table serves as the basis for an alternative implementation of other process information sources:

- The SHOW PROCESSLIST statement.
- The mysqladmin processlist command (which uses SHOW PROCESSLIST statement).

The default SHOW PROCESSLIST implementation iterates across active threads from within the thread manager while holding a global mutex. This has negative performance consequences, particularly on busy systems. The alternative SHOW PROCESSLIST implementation is based on the Performance Schema [processlist](#page-96-0) table. This implementation queries active thread data from the Performance Schema rather than the thread manager and does not require a mutex.

MySQL configuration affects [processlist](#page-96-0) table contents as follows:

- Minimum required configuration:
  - The MySQL server must be configured and built with thread instrumentation enabled. This is true by default; it is controlled using the DISABLE\_PSI\_THREAD CMake option.
  - The Performance Schema must be enabled at server startup. This is true by default; it is controlled using the [performance\\_schema](#page-112-1) system variable.

With that configuration satisfied, [performance\\_schema\\_show\\_processlist](#page-129-1) enables or disables the alternative SHOW PROCESSLIST implementation. If the minimum configuration is not satisfied, the [processlist](#page-96-0) table (and thus SHOW PROCESSLIST) may not return all data.

- Recommended configuration:
  - To avoid having some threads ignored:
    - Leave the [performance\\_schema\\_max\\_thread\\_instances](#page-127-1) system variable set to its default or set it at least as great as the max\_connections system variable.
    - Leave the [performance\\_schema\\_max\\_thread\\_classes](#page-126-0) system variable set to its default.
  - To avoid having some STATE column values be empty, leave the [performance\\_schema\\_max\\_stage\\_classes](#page-124-1) system variable set to its default.

The default for those configuration parameters is -1, which causes the Performance Schema to autosize them at server startup. With the parameters set as indicated, the [processlist](#page-96-0) table (and thus SHOW PROCESSLIST) produce complete process information.

The preceding configuration parameters affect the contents of the processlist table. For a given configuration, however, the [processlist](#page-96-0) contents are unaffected by the [performance\\_schema\\_show\\_processlist](#page-129-1) setting.

The alternative process list implementation does not apply to the INFORMATION\_SCHEMA PROCESSLIST table or the COM\_PROCESS\_INFO command of the MySQL client/server protocol.

### <span id="page-99-0"></span>**29.12.21.8 The threads Table**

The [threads](#page-99-0) table contains a row for each server thread. Each row contains information about a thread and indicates whether monitoring and historical event logging are enabled for it:

```
mysql> SELECT * FROM performance_schema.threads\G
*************************** 1. row ***************************
 THREAD_ID: 1
 NAME: thread/sql/main
 TYPE: BACKGROUND
 PROCESSLIST_ID: NULL
 PROCESSLIST_USER: NULL
 PROCESSLIST_HOST: NULL
 PROCESSLIST_DB: mysql
 PROCESSLIST_COMMAND: NULL
 PROCESSLIST_TIME: 418094
 PROCESSLIST_STATE: NULL
 PROCESSLIST_INFO: NULL
 PARENT_THREAD_ID: NULL
 ROLE: NULL
 INSTRUMENTED: YES
 HISTORY: YES
 CONNECTION_TYPE: NULL
 THREAD_OS_ID: 5856
 RESOURCE_GROUP: SYS_default
 EXECUTION_ENGINE: PRIMARY
 CONTROLLED_MEMORY: 1456
MAX_CONTROLLED_MEMORY: 67480
 TOTAL_MEMORY: 1270430
 MAX_TOTAL_MEMORY: 1307317
 TELEMETRY_ACTIVE: NO
...
```

When the Performance Schema initializes, it populates the [threads](#page-99-0) table based on the threads in existence then. Thereafter, a new row is added each time the server creates a thread.

The INSTRUMENTED and HISTORY column values for new threads are determined by the contents of the setup\_actors table. For information about how to use the setup\_actors table to control these columns, see Section 29.4.6, "Pre-Filtering by Thread".

Removal of rows from the [threads](#page-99-0) table occurs when threads end. For a thread associated with a client session, removal occurs when the session ends. If a client has auto-reconnect enabled and

the session reconnects after a disconnect, the session becomes associated with a new row in the [threads](#page-99-0) table that has a different PROCESSLIST\_ID value. The initial INSTRUMENTED and HISTORY values for the new thread may be different from those of the original thread: The setup\_actors table may have changed in the meantime, and if the INSTRUMENTED or HISTORY value for the original thread was changed after the row was initialized, the change does not carry over to the new thread.

You can enable or disable thread monitoring (that is, whether events executed by the thread are instrumented) and historical event logging. To control the initial INSTRUMENTED and HISTORY values for new foreground threads, use the setup\_actors table. To control these aspects of existing threads, set the INSTRUMENTED and HISTORY columns of [threads](#page-99-0) table rows. (For more information about the conditions under which thread monitoring and historical event logging occur, see the descriptions of the INSTRUMENTED and HISTORY columns.)

For a comparison of the [threads](#page-99-0) table columns with names having a prefix of PROCESSLIST\_ to other process information sources, see Sources of Process Information.

![](_page_100_Picture_4.jpeg)

### **Important**

For thread information sources other than the [threads](#page-99-0) table, information about threads for other users is shown only if the current user has the PROCESS privilege. That is not true of the [threads](#page-99-0) table; all rows are shown to any user who has the SELECT privilege for the table. Users who should not be able to see threads for other users by accessing the [threads](#page-99-0) table should not be given the SELECT privilege for it.

The [threads](#page-99-0) table has these columns:

• THREAD\_ID

A unique thread identifier.

• NAME

The name associated with the thread instrumentation code in the server. For example, thread/ sql/one\_connection corresponds to the thread function in the code responsible for handling a user connection, and thread/sql/main stands for the main() function of the server.

• TYPE

The thread type, either FOREGROUND or BACKGROUND. User connection threads are foreground threads. Threads associated with internal server activity are background threads. Examples are internal InnoDB threads, "binlog dump" threads sending information to replicas, and replication I/O and SQL threads.

• PROCESSLIST\_ID

For a foreground thread (associated with a user connection), this is the connection identifier. This is the same value displayed in the ID column of the INFORMATION\_SCHEMA PROCESSLIST table, displayed in the Id column of SHOW PROCESSLIST output, and returned by the CONNECTION\_ID() function within the thread.

For a background thread (not associated with a user connection), PROCESSLIST\_ID is NULL, so the values are not unique.

• PROCESSLIST\_USER

The user associated with a foreground thread, NULL for a background thread.

• PROCESSLIST\_HOST

The host name of the client associated with a foreground thread, NULL for a background thread.

Unlike the HOST column of the INFORMATION\_SCHEMA PROCESSLIST table or the Host column of SHOW PROCESSLIST output, the PROCESSLIST\_HOST column does not include the port number for TCP/IP connections. To obtain this information from the Performance Schema, enable the socket instrumentation (which is not enabled by default) and examine the socket\_instances table:

```
mysql> SELECT NAME, ENABLED, TIMED
 FROM performance_schema.setup_instruments
 WHERE NAME LIKE 'wait/io/socket%';
+----------------------------------------+---------+-------+
| NAME | ENABLED | TIMED |
+----------------------------------------+---------+-------+
| wait/io/socket/sql/server_tcpip_socket | NO | NO |
| wait/io/socket/sql/server_unix_socket | NO | NO |
| wait/io/socket/sql/client_connection | NO | NO |
+----------------------------------------+---------+-------+
3 rows in set (0.01 sec)
mysql> UPDATE performance_schema.setup_instruments
 SET ENABLED='YES'
 WHERE NAME LIKE 'wait/io/socket%';
Query OK, 3 rows affected (0.00 sec)
Rows matched: 3 Changed: 3 Warnings: 0
mysql> SELECT * FROM performance_schema.socket_instances\G
*************************** 1. row ***************************
 EVENT_NAME: wait/io/socket/sql/client_connection
OBJECT_INSTANCE_BEGIN: 140612577298432
 THREAD_ID: 31
 SOCKET_ID: 53
 IP: ::ffff:127.0.0.1
 PORT: 55642
 STATE: ACTIVE
...
```

• PROCESSLIST\_DB

The default database for the thread, or NULL if none has been selected.

• PROCESSLIST\_COMMAND

For foreground threads, the type of command the thread is executing on behalf of the client, or Sleep if the session is idle. For descriptions of thread commands, see Section 10.14, "Examining Server Thread (Process) Information". The value of this column corresponds to the COM\_xxx commands of the client/server protocol and Com\_xxx status variables. See Section 7.1.10, "Server Status Variables"

Background threads do not execute commands on behalf of clients, so this column may be NULL.

• PROCESSLIST\_TIME

The time in seconds that the thread has been in its current state. For a replica SQL thread, the value is the number of seconds between the timestamp of the last replicated event and the real time of the replica host. See Section 19.2.3, "Replication Threads".

• PROCESSLIST\_STATE

An action, event, or state that indicates what the thread is doing. For descriptions of PROCESSLIST\_STATE values, see Section 10.14, "Examining Server Thread (Process) Information". If the value if NULL, the thread may correspond to an idle client session or the work it is doing is not instrumented with stages.

Most states correspond to very quick operations. If a thread stays in a given state for many seconds, there might be a problem that bears investigation.

• PROCESSLIST\_INFO

The statement the thread is executing, or NULL if it is executing no statement. The statement might be the one sent to the server, or an innermost statement if the statement executes other statements. For example, if a CALL statement executes a stored procedure that is executing a SELECT statement, the PROCESSLIST\_INFO value shows the SELECT statement.

• PARENT\_THREAD\_ID

If this thread is a subthread (spawned by another thread), this is the THREAD\_ID value of the spawning thread.

• ROLE

Unused.

• INSTRUMENTED

Whether events executed by the thread are instrumented. The value is YES or NO.

• For foreground threads, the initial INSTRUMENTED value is determined by whether the user account associated with the thread matches any row in the setup\_actors table. Matching is based on the values of the PROCESSLIST\_USER and PROCESSLIST\_HOST columns.

If the thread spawns a subthread, matching occurs again for the [threads](#page-99-0) table row created for the subthread.

- For background threads, INSTRUMENTED is YES by default. setup\_actors is not consulted because there is no associated user for background threads.
- For any thread, its INSTRUMENTED value can be changed during the lifetime of the thread.

For monitoring of events executed by the thread to occur, these things must be true:

- The thread\_instrumentation consumer in the setup\_consumers table must be YES.
- The threads.INSTRUMENTED column must be YES.
- Monitoring occurs only for those thread events produced from instruments that have the ENABLED column set to YES in the setup\_instruments table.
- HISTORY

Whether to log historical events for the thread. The value is YES or NO.

• For foreground threads, the initial HISTORY value is determined by whether the user account associated with the thread matches any row in the setup\_actors table. Matching is based on the values of the PROCESSLIST\_USER and PROCESSLIST\_HOST columns.

If the thread spawns a subthread, matching occurs again for the [threads](#page-99-0) table row created for the subthread.

- For background threads, HISTORY is YES by default. setup\_actors is not consulted because there is no associated user for background threads.
- For any thread, its HISTORY value can be changed during the lifetime of the thread.

For historical event logging for the thread to occur, these things must be true:

• The appropriate history-related consumers in the setup\_consumers table must be enabled. For example, wait event logging in the events\_waits\_history and events\_waits\_history\_long tables requires the corresponding events\_waits\_history and events\_waits\_history\_long consumers to be YES.

- The threads.HISTORY column must be YES.
- Logging occurs only for those thread events produced from instruments that have the ENABLED column set to YES in the setup\_instruments table.
- CONNECTION\_TYPE

The protocol used to establish the connection, or NULL for background threads. Permitted values are TCP/IP (TCP/IP connection established without encryption), SSL/TLS (TCP/IP connection established with encryption), Socket (Unix socket file connection), Named Pipe (Windows named pipe connection), and Shared Memory (Windows shared memory connection).

• THREAD\_OS\_ID

The thread or task identifier as defined by the underlying operating system, if there is one:

- When a MySQL thread is associated with the same operating system thread for its lifetime, THREAD\_OS\_ID contains the operating system thread ID.
- When a MySQL thread is not associated with the same operating system thread for its lifetime, THREAD\_OS\_ID contains NULL. This is typical for user sessions when the thread pool plugin is used (see Section 7.6.3, "MySQL Enterprise Thread Pool").

For Windows, THREAD\_OS\_ID corresponds to the thread ID visible in Process Explorer ([https://](https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx) [technet.microsoft.com/en-us/sysinternals/bb896653.aspx](https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)).

For Linux, THREAD\_OS\_ID corresponds to the value of the gettid() function. This value is exposed, for example, using the perf or ps -L commands, or in the proc file system (/ proc/[pid]/task/[tid]). For more information, see the perf-stat(1), ps(1), and proc(5) man pages.

• RESOURCE\_GROUP

The resource group label. This value is NULL if resource groups are not supported on the current platform or server configuration (see Resource Group Restrictions).

• EXECUTION\_ENGINE

The query execution engine. The value is either PRIMARY or SECONDARY. For use with MySQL HeatWave Service and MySQL HeatWave, where the PRIMARY engine is InnoDB and the SECONDARY engine is MySQL HeatWave (RAPID). For MySQL Community Edition Server, MySQL Enterprise Edition Server (on-premise), and MySQL HeatWave Service without MySQL HeatWave, the value is always PRIMARY. This column was added in MySQL 8.0.29.

• CONTROLLED\_MEMORY

Amount of controlled memory used by the thread.

This column was added in MySQL 8.0.31.

• MAX\_CONTROLLED\_MEMORY

Maximum value of CONTROLLED\_MEMORY seen during the thread execution.

This column was added in MySQL 8.0.31.

• TOTAL\_MEMORY

The current amount of memory, controlled or not, used by the thread.

This column was added in MySQL 8.0.31.

• MAX TOTAL MEMORY

The maximum value of TOTAL MEMORY seen during the thread execution.

This column was added in MySQL 8.0.31.

• TELEMETRY ACTIVE

Whether the thread has an active telemetry seesion attached. The value is YES or NO.

This column was added in MySQL 8.0.33.

The threads table has these indexes:

- Primary key on (THREAD ID)
- Index on (NAME)
- Index on (PROCESSLIST ID)
- Index on (PROCESSLIST USER, PROCESSLIST HOST)
- Index on (PROCESSLIST HOST)
- Index on (THREAD OS ID)
- Index on (RESOURCE GROUP)

TRUNCATE TABLE is not permitted for the threads table.

## <span id="page-104-0"></span>29.12.21.9 The tls\_channel\_status Table

Connection interface TLS properties are set at server startup, and can be updated at runtime using the ALTER INSTANCE RELOAD TLS statement. See Server-Side Runtime Configuration and Monitoring for Encrypted Connections.

The tls\_channel\_status table (available as of MySQL 8.0.21) provides information about connection interface TLS properties:

```
mysql> SELECT * FROM performance schema.tls channel status\G
                   ***** 1. row *****
CHANNEL: mysql main
PROPERTY: Enabled
 VALUE: Yes
                  ****** 2. row ***************
CHANNEL: mysql main
PROPERTY: ssl accept renegotiates
 VALUE: 0
                 ****** 3. row ***************
CHANNEL: mysql main
PROPERTY: Ssl_accepts
  VALUE: 2
**************************************
CHANNEL: mysql admin
PROPERTY: Enabled
 VALUE: No
                 ***** 30. row **************
CHANNEL: mysql admin
PROPERTY: ssl_accept_renegotiates
         ************* 31. row *************
CHANNEL: mysql admin
PROPERTY: Ssl accepts
  VALUE: 0
```

The tls\_channel\_status table has these columns:

### • CHANNEL

The name of the connection interface to which the TLS property row applies. mysql\_main and mysql\_admin are the channel names for the main and administrative connection interfaces, respectively. For information about the different interfaces, see Section 7.1.12.1, "Connection Interfaces".

### • PROPERTY

The TLS property name. The row for the Enabled property indicates overall interface status, where the interface and its status are named in the CHANNEL and VALUE columns, respectively. Other property names indicate particular TLS properties. These often correspond to the names of TLSrelated status variables.

### • VALUE

The TLS property value.

The properties exposed by this table are not fixed and depend on the instrumentation implemented by each channel.

For each channel, the row with a PROPERTY value of Enabled indicates whether the channel supports encrypted connections, and other channel rows indicate TLS context properties:

• For mysql\_main, the Enabled property is yes or no to indicate whether the main interface supports encrypted connections. Other channel rows display TLS context properties for the main interface.

For the main interface, similar status information can be obtained using these statements:

```
SHOW GLOBAL STATUS LIKE 'current_tls%';
SHOW GLOBAL STATUS LIKE 'ssl%';
```

• For mysql\_admin, the Enabled property is no if the administrative interface is not enabled or it is enabled but does not support encrypted connections. Enabled is yes if the interface is enabled and supports encrypted connections.

When Enabled is yes, the other mysql\_admin rows indicate channel properties for the administrative interface TLS context only if some nondefault TLS parameter value is configured for that interface. (This is the case if any admin\_tls\_xxx or admin\_ssl\_xxx system variable is set to a value different from its default.) Otherwise, the administrative interface uses the same TLS context as the main interface.

The [tls\\_channel\\_status](#page-104-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [tls\\_channel\\_status](#page-104-0) table.

### <span id="page-105-0"></span>**29.12.21.10 The user\_defined\_functions Table**

The [user\\_defined\\_functions](#page-105-0) table contains a row for each loadable function registered automatically by a component or plugin, or manually by a CREATE FUNCTION statement. For information about operations that add or remove table rows, see Section 7.7.1, "Installing and Uninstalling Loadable Functions".

![](_page_105_Picture_18.jpeg)

### **Note**

The name of the [user\\_defined\\_functions](#page-105-0) table stems from the terminology used at its inception for the type of function now known as a loadable function (that is, user-defined function, or UDF).

The [user\\_defined\\_functions](#page-105-0) table has these columns:

• UDF\_NAME

The function name as referred to in SQL statements. The value is NULL if the function was registered by a CREATE FUNCTION statement and is in the process of unloading.

• UDF\_RETURN\_TYPE

The function return value type. The value is one of int, decimal, real, char, or row.

• UDF\_TYPE

The function type. The value is one of function (scalar) or aggregate.

• UDF\_LIBRARY

The name of the library file containing the executable function code. The file is located in the directory named by the plugin\_dir system variable. The value is NULL if the function was registered by a component or plugin rather than by a CREATE FUNCTION statement.

• UDF\_USAGE\_COUNT

The current function usage count. This is used to tell whether statements currently are accessing the function.

The [user\\_defined\\_functions](#page-105-0) table has these indexes:

• Primary key on (UDF\_NAME)

TRUNCATE TABLE is not permitted for the [user\\_defined\\_functions](#page-105-0) table.

The mysql.func system table also lists installed loadable functions, but only those installed using CREATE FUNCTION. The [user\\_defined\\_functions](#page-105-0) table lists loadable functions installed using CREATE FUNCTION as well as loadable functions installed automatically by components or plugins. This difference makes [user\\_defined\\_functions](#page-105-0) preferable to mysql.func for checking which loadable functions are installed.

# <span id="page-106-0"></span>**29.13 Performance Schema Option and Variable Reference**

**Table 29.18 Performance Schema Variable Reference**

| Name                                                             | Cmd-Line                                | Option File | System Var | Status Var | Var Scope | Dynamic |
|------------------------------------------------------------------|-----------------------------------------|-------------|------------|------------|-----------|---------|
| performance_schema Yes                                           |                                         | Yes         | Yes        |            | Global    | No      |
|                                                                  | Performance_schema_accounts_lost        |             |            | Yes        | Global    | No      |
|                                                                  | performance_schema_accounts_size<br>Yes | Yes         | Yes        |            | Global    | No      |
|                                                                  | Performance_schema_cond_classes_lost    |             |            | Yes        | Global    | No      |
|                                                                  | Performance_schema_cond_instances_lost  |             |            | Yes        | Global    | No      |
| performance<br>schema<br>consumer<br>events<br>stages<br>current | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>stages<br>history | Yes                                     | Yes         |            |            |           |         |
| performance<br>schema                                            | Yes                                     | Yes         |            |            |           |         |

| Name                                                                        | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
|-----------------------------------------------------------------------------|----------|-------------|------------|------------|-----------|---------|
| consumer<br>events<br>stages<br>history-long                                |          |             |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>cpu            | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>current        | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>history        | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>statements<br>history-long   | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>transactions<br>current      | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>transactions<br>history      | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events<br>transactions<br>history-long | Yes      | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>events-waits<br>current                | Yes      | Yes         |            |            |           |         |
| performance<br>schema                                                       | Yes      | Yes         |            |            |           |         |

| Name                                                              | Cmd-Line                                                        | Option File | System Var | Status Var | Var Scope | Dynamic |
|-------------------------------------------------------------------|-----------------------------------------------------------------|-------------|------------|------------|-----------|---------|
| consumer<br>events-waits<br>history                               |                                                                 |             |            |            |           |         |
| performance<br>schema<br>consumer<br>events-waits<br>history-long | Yes                                                             | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>global<br>instrumentation    | Yes                                                             | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>statements<br>digest         | Yes                                                             | Yes         |            |            |           |         |
| performance<br>schema<br>consumer<br>thread<br>instrumentation    | Yes                                                             | Yes         |            |            |           |         |
|                                                                   | Performance_schema_digest_lost                                  |             |            | Yes        | Global    | No      |
|                                                                   | performance_schema_digests_size<br>Yes                          | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_stages_history_long_size<br>Yes       | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_stages_history_size<br>Yes            | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_statements_history_long_size<br>Yes   | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_statements_history_size<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_transactions_history_long_size<br>Yes | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_transactions_history_size<br>Yes      | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_waits_history_long_size<br>Yes        | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_events_waits_history_size<br>Yes             | Yes         | Yes        |            | Global    | No      |
|                                                                   | Performance_schema_file_classes_lost                            |             |            | Yes        | Global    | No      |
|                                                                   | Performance_schema_file_handles_lost                            |             |            | Yes        | Global    | No      |
|                                                                   | Performance_schema_file_instances_lost                          |             |            | Yes        | Global    | No      |
|                                                                   | Performance_schema_hosts_lost                                   |             |            | Yes        | Global    | No      |
|                                                                   | performance_schema_hosts_size<br>Yes                            | Yes         | Yes        |            | Global    | No      |
| performance<br>schema<br>instrument                               | Yes                                                             | Yes         |            |            |           |         |
|                                                                   | Performance_schema_locker_lost                                  |             |            | Yes        | Global    | No      |
|                                                                   | performance_schema_max_cond_classes<br>Yes                      | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_max_cond_instances<br>Yes                    | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_max_digest_length<br>Yes                     | Yes         | Yes        |            | Global    | No      |
|                                                                   | performance_schema_max_file_classes<br>Yes                      | Yes         | Yes        |            | Global    | No      |

| Name | Cmd-Line                                                    | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|-------------------------------------------------------------|-------------|------------|------------|-----------|---------|
|      | performance_schema_max_file_handles<br>Yes                  | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_file_instances<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_memory_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_metadata_locks<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_mutex_classes<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_mutex_instances<br>Yes               | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_prepared_statements_instances<br>Yes | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_program_instances<br>Yes             | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_rwlock_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_rwlock_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_socket_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_socket_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_stage_classes<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_statement_classes<br>Yes             | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_statement_stack<br>Yes               | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_table_handles<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_table_instances<br>Yes               | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_thread_classes<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_max_thread_instances<br>Yes              | Yes         | Yes        |            | Global    | No      |
|      | Performance_schema_memory_classes_lost                      |             |            | Yes        | Global    | No      |
|      | Performance_schema_metadata_lock_lost                       |             |            | Yes        | Global    | No      |
|      | Performance_schema_mutex_classes_lost                       |             |            | Yes        | Global    | No      |
|      | Performance_schema_mutex_instances_lost                     |             |            | Yes        | Global    | No      |
|      | Performance_schema_nested_statement_lost                    |             |            | Yes        | Global    | No      |
|      | Performance_schema_prepared_statements_lost                 |             |            | Yes        | Global    | No      |
|      | Performance_schema_program_lost                             |             |            | Yes        | Global    | No      |
|      | Performance_schema_rwlock_classes_lost                      |             |            | Yes        | Global    | No      |
|      | Performance_schema_rwlock_instances_lost                    |             |            | Yes        | Global    | No      |
|      | Performance_schema_session_connect_attrs_lost               |             |            | Yes        | Global    | No      |
|      | performance_schema_session_connect_attrs_size<br>Yes        | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_setup_actors_size<br>Yes                 | Yes         | Yes        |            | Global    | No      |
|      | performance_schema_setup_objects_size<br>Yes                | Yes         | Yes        |            | Global    | No      |
|      | Performance_schema_socket_classes_lost                      |             |            | Yes        | Global    | No      |
|      | Performance_schema_socket_instances_lost                    |             |            | Yes        | Global    | No      |
|      | Performance_schema_stage_classes_lost                       |             |            | Yes        | Global    | No      |
|      | Performance_schema_statement_classes_lost                   |             |            | Yes        | Global    | No      |
|      | Performance_schema_table_handles_lost                       |             |            | Yes        | Global    | No      |
|      | Performance_schema_table_instances_lost                     |             |            | Yes        | Global    | No      |
|      | Performance_schema_thread_classes_lost                      |             |            | Yes        | Global    | No      |
|      | Performance_schema_thread_instances_lost                    |             |            | Yes        | Global    | No      |
|      | Performance_schema_users_lost                               |             |            | Yes        | Global    | No      |

| Name | Cmd-Line                             | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|--------------------------------------|-------------|------------|------------|-----------|---------|
|      | performance_schema_users_size<br>Yes | Yes         | Yes        |            | Global    | No      |