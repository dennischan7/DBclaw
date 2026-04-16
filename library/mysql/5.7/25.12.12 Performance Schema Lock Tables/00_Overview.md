---
source: MySQL 5.7 Reference
title: 00_Overview
---

The Performance Schema exposes lock information through these tables:

- [metadata\\_locks](#page-67-0): Metadata locks held and requested
- [table\\_handles](#page-70-0): Table locks held and requested

The following sections describe these tables in more detail.

## <span id="page-67-0"></span>**25.12.12.1 The metadata\_locks Table**

MySQL uses metadata locking to manage concurrent access to database objects and to ensure data consistency; see Section 8.11.4, "Metadata Locking". Metadata locking applies not just to tables, but also to schemas, stored programs (procedures, functions, triggers, scheduled events), tablespaces, user locks acquired with the GET\_LOCK() function (see Section 12.14, "Locking Functions"), and locks acquired with the locking service described in Section 5.5.6.1, "The Locking Service".

The Performance Schema exposes metadata lock information through the [metadata\\_locks](#page-67-0) table:

- Locks that have been granted (shows which sessions own which current metadata locks).
- Locks that have been requested but not yet granted (shows which sessions are waiting for which metadata locks).
- Lock requests that have been killed by the deadlock detector.
- Lock requests that have timed out and are waiting for the requesting session's lock request to be discarded.

This information enables you to understand metadata lock dependencies between sessions. You can see not only which lock a session is waiting for, but which session currently holds that lock.

The [metadata\\_locks](#page-67-0) table is read only and cannot be updated. It is autosized by default; to configure the table size, set the [performance\\_schema\\_max\\_metadata\\_locks](#page-116-0) system variable at server startup.

Metadata lock instrumentation uses the wait/lock/metadata/sql/mdl instrument, which is disabled by default.

To control metadata lock instrumentation state at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='wait/lock/metadata/sql/mdl=ON'
```

• Disable:

```
[mysqld]
performance-schema-instrument='wait/lock/metadata/sql/mdl=OFF'
```

To control metadata lock instrumentation state at runtime, update the [setup\\_instruments](#page-13-0) table:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME = 'wait/lock/metadata/sql/mdl';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
WHERE NAME = 'wait/lock/metadata/sql/mdl';
```

The Performance Schema maintains [metadata\\_locks](#page-67-0) table content as follows, using the LOCK\_STATUS column to indicate the status of each lock:

- When a metadata lock is requested and obtained immediately, a row with a status of GRANTED is inserted.
- When a metadata lock is requested and not obtained immediately, a row with a status of PENDING is inserted.
- When a metadata lock previously requested is granted, its row status is updated to GRANTED.
- When a metadata lock is released, its row is deleted.
- When a pending lock request is canceled by the deadlock detector to break a deadlock ([ER\\_LOCK\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_lock_deadlock)), its row status is updated from PENDING to VICTIM.
- When a pending lock request times out ([ER\\_LOCK\\_WAIT\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md#error_er_lock_wait_timeout)), its row status is updated from PENDING to TIMEOUT.

- When granted lock or pending lock request is killed, its row status is updated from GRANTED or PENDING to KILLED.
- The VICTIM, TIMEOUT, and KILLED status values are brief and signify that the lock row is about to be deleted.
- The PRE\_ACQUIRE\_NOTIFY and POST\_RELEASE\_NOTIFY status values are brief and signify that the metadata locking subsubsystem is notifying interested storage engines while entering lock acquisition operations or leaving lock release operations. These status values were added in MySQL 5.7.11.

The [metadata\\_locks](#page-67-0) table has these columns:

• OBJECT\_TYPE

The type of lock used in the metadata lock subsystem. The value is one of GLOBAL, SCHEMA, TABLE, FUNCTION, PROCEDURE, TRIGGER (currently unused), EVENT, COMMIT, USER LEVEL LOCK, TABLESPACE, or LOCKING SERVICE.

A value of USER LEVEL LOCK indicates a lock acquired with GET\_LOCK(). A value of LOCKING SERVICE indicates a lock acquired with the locking service described in Section 5.5.6.1, "The Locking Service".

• OBJECT\_SCHEMA

The schema that contains the object.

• OBJECT\_NAME

The name of the instrumented object.

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the instrumented object.

• LOCK\_TYPE

The lock type from the metadata lock subsystem. The value is one of INTENTION\_EXCLUSIVE, SHARED, SHARED\_HIGH\_PRIO, SHARED\_READ, SHARED\_WRITE, SHARED\_UPGRADABLE, SHARED\_NO\_WRITE, SHARED\_NO\_READ\_WRITE, or EXCLUSIVE.

• LOCK\_DURATION

The lock duration from the metadata lock subsystem. The value is one of STATEMENT, TRANSACTION, or EXPLICIT. The STATEMENT and TRANSACTION values signify locks that are released implicitly at statement or transaction end, respectively. The EXPLICIT value signifies locks that survive statement or transaction end and are released by explicit action, such as global locks acquired with FLUSH TABLES WITH READ LOCK.

• LOCK\_STATUS

The lock status from the metadata lock subsystem. The value is one of PENDING, GRANTED, VICTIM, TIMEOUT, KILLED, PRE\_ACQUIRE\_NOTIFY, or POST\_RELEASE\_NOTIFY. The Performance Schema assigns these values as described previously.

• SOURCE

The name of the source file containing the instrumented code that produced the event and the line number in the file at which the instrumentation occurs. This enables you to check the source to determine exactly what code is involved.

• OWNER\_THREAD\_ID

The thread requesting a metadata lock.

• OWNER\_EVENT\_ID

The event requesting a metadata lock.

TRUNCATE TABLE is not permitted for the [metadata\\_locks](#page-67-0) table.

## <span id="page-70-0"></span>**25.12.12.2 The table\_handles Table**

The Performance Schema exposes table lock information through the [table\\_handles](#page-70-0) table to show the table locks currently in effect for each opened table handle. [table\\_handles](#page-70-0) reports what is recorded by the table lock instrumentation. This information shows which table handles the server has open, how they are locked, and by which sessions.

The [table\\_handles](#page-70-0) table is read only and cannot be updated. It is autosized by default; to configure the table size, set the [performance\\_schema\\_max\\_table\\_handles](#page-121-0) system variable at server startup.

Table lock instrumentation uses the wait/lock/table/sql/handler instrument, which is enabled by default.

To control table lock instrumentation state at server startup, use lines like these in your my.cnf file:

• Enable:

```
[mysqld]
performance-schema-instrument='wait/lock/table/sql/handler=ON'
```

• Disable:

```
[mysqld]
performance-schema-instrument='wait/lock/table/sql/handler=OFF'
```

To control table lock instrumentation state at runtime, update the [setup\\_instruments](#page-13-0) table:

• Enable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'YES', TIMED = 'YES'
WHERE NAME = 'wait/lock/table/sql/handler';
```

• Disable:

```
UPDATE performance_schema.setup_instruments
SET ENABLED = 'NO', TIMED = 'NO'
WHERE NAME = 'wait/lock/table/sql/handler';
```

The [table\\_handles](#page-70-0) table has these columns:

• OBJECT\_TYPE

The table opened by a table handle.

• OBJECT\_SCHEMA

The schema that contains the object.

• OBJECT\_NAME

The name of the instrumented object.

• OBJECT\_INSTANCE\_BEGIN

The table handle address in memory.

• OWNER\_THREAD\_ID

The thread owning the table handle.

• OWNER\_EVENT\_ID

The event which caused the table handle to be opened.

• INTERNAL\_LOCK

The table lock used at the SQL level. The value is one of READ, READ WITH SHARED LOCKS, READ HIGH PRIORITY, READ NO INSERT, WRITE ALLOW WRITE, WRITE CONCURRENT INSERT, WRITE LOW PRIORITY, or WRITE. For information about these lock types, see the include/ thr\_lock.h source file.

• EXTERNAL\_LOCK

The table lock used at the storage engine level. The value is one of READ EXTERNAL or WRITE EXTERNAL.

TRUNCATE TABLE is not permitted for the [table\\_handles](#page-70-0) table.

# <span id="page-71-0"></span>**25.12.13 Performance Schema System Variable Tables**

![](_page_71_Picture_12.jpeg)

#### **Note**

The value of the show\_compatibility\_56 system variable affects the information available from the tables described here. For details, see the description of that variable in Section 5.1.7, "Server System Variables".

The MySQL server maintains many system variables that indicate how it is configured (see Section 5.1.7, "Server System Variables"). System variable information is available in these Performance Schema tables:

- [global\\_variables](#page-71-0): Global system variables. An application that wants only global values should use this table.
- [session\\_variables](#page-71-0): System variables for the current session. An application that wants all system variable values for its own session should use this table. It includes the session variables for its session, as well as the values of global variables that have no session counterpart.
- [variables\\_by\\_thread](#page-71-0): Session system variables for each active session. An application that wants to know the session variable values for specific sessions should use this table. It includes session variables only, identified by thread ID.

The session variable tables ([session\\_variables](#page-71-0), [variables\\_by\\_thread](#page-71-0)) contain information only for active sessions, not terminated sessions.

The [global\\_variables](#page-71-0) and [session\\_variables](#page-71-0) tables have these columns:

• VARIABLE\_NAME

The system variable name.

• VARIABLE\_VALUE

The system variable value. For [global\\_variables](#page-71-0), this column contains the global value. For [session\\_variables](#page-71-0), this column contains the variable value in effect for the current session.

The [variables\\_by\\_thread](#page-71-0) table has these columns:

• THREAD\_ID

The thread identifier of the session in which the system variable is defined.

• VARIABLE\_NAME

The system variable name.

• VARIABLE\_VALUE

The session variable value for the session named by the THREAD\_ID column.

The [variables\\_by\\_thread](#page-71-0) table contains system variable information only about foreground threads. If not all threads are instrumented by the Performance Schema, this table may miss some rows. In this case, the [Performance\\_schema\\_thread\\_instances\\_lost](#page-128-0) status variable is greater than zero.

TRUNCATE TABLE is not supported for Performance Schema system variable tables.

# <span id="page-72-0"></span>**25.12.14 Performance Schema Status Variable Tables**

![](_page_72_Picture_10.jpeg)

#### **Note**

The value of the show\_compatibility\_56 system variable affects the information available from the tables described here. For details, see the description of that variable in Section 5.1.7, "Server System Variables".

The MySQL server maintains many status variables that provide information about its operation (see Section 5.1.9, "Server Status Variables"). Status variable information is available in these Performance Schema tables:

- [global\\_status](#page-72-0): Global status variables. An application that wants only global values should use this table.
- [session\\_status](#page-72-0): Status variables for the current session. An application that wants all status variable values for its own session should use this table. It includes the session variables for its session, as well as the values of global variables that have no session counterpart.
- [status\\_by\\_thread](#page-72-0): Session status variables for each active session. An application that wants to know the session variable values for specific sessions should use this table. It includes session variables only, identified by thread ID.

There are also summary tables that provide status variable information aggregated by account, host name, and user name. See [Section 25.12.15.10, "Status Variable Summary Tables".](#page-92-0)

The session variable tables ([session\\_status](#page-72-0), [status\\_by\\_thread](#page-72-0)) contain information only for active sessions, not terminated sessions.

The Performance Schema collects statistics for global status variables only for threads for which the INSTRUMENTED value is YES in the [threads](#page-100-0) table. Statistics for session status variables are always collected, regardless of the INSTRUMENTED value.

The Performance Schema does not collect statistics for Com\_xxx status variables in the status variable tables. To obtain global and per-session statement execution counts, use the [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-78-0) and [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-78-0) tables, respectively. For example:

```
SELECT EVENT_NAME, COUNT_STAR
FROM performance_schema.events_statements_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'statement/sql/%';
```

The [global\\_status](#page-72-0) and [session\\_status](#page-72-0) tables have these columns:

• VARIABLE\_NAME

The status variable name.

• VARIABLE\_VALUE

The status variable value. For [global\\_status](#page-72-0), this column contains the global value. For [session\\_status](#page-72-0), this column contains the variable value for the current session.

The [status\\_by\\_thread](#page-72-0) table contains the status of each active thread. It has these columns:

• THREAD\_ID

The thread identifier of the session in which the status variable is defined.

• VARIABLE\_NAME

The status variable name.

• VARIABLE\_VALUE

The session variable value for the session named by the THREAD\_ID column.

The [status\\_by\\_thread](#page-72-0) table contains status variable information only about foreground threads. If the [performance\\_schema\\_max\\_thread\\_instances](#page-122-0) system variable is not autoscaled (signified by a value of −1) and the maximum permitted number of instrumented thread objects is not greater than the number of background threads, the table is empty.

The Performance Schema supports TRUNCATE TABLE for status variable tables as follows:

- [global\\_status](#page-72-0): Resets thread, account, host, and user status. Resets global status variables except those that the server never resets.
- [session\\_status](#page-72-0): Not supported.
- [status\\_by\\_thread](#page-72-0): Aggregates status for all threads to the global status and account status, then resets thread status. If account statistics are not collected, the session status is added to host and user status, if host and user status are collected.

Account, host, and user statistics are not collected if the [performance\\_schema\\_accounts\\_size](#page-110-2), [performance\\_schema\\_hosts\\_size](#page-113-1), and [performance\\_schema\\_users\\_size](#page-125-0) system variables, respectively, are set to 0.

FLUSH STATUS adds the session status from all active sessions to the global status variables, resets the status of all active sessions, and resets account, host, and user status values aggregated from disconnected sessions.