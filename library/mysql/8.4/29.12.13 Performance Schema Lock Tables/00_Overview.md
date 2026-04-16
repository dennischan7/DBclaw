---
source: MySQL 8.4 Reference
title: 00_Overview
---

The Performance Schema exposes lock information through these tables:

- [data\\_locks](#page-88-0): Data locks held and requested
- [data\\_lock\\_waits](#page-90-0): Relationships between data lock owners and data lock requestors blocked by those owners
- [metadata\\_locks](#page-92-0): Metadata locks held and requested
- [table\\_handles](#page-94-0): Table locks held and requested

The following sections describe these tables in more detail.

### <span id="page-88-0"></span>**29.12.13.1 The data\_locks Table**

The [data\\_locks](#page-88-0) table shows data locks held and requested. For information about which lock requests are blocked by which held locks, see [Section 29.12.13.2, "The data\\_lock\\_waits Table".](#page-90-0)

Example data lock information:

```
mysql> SELECT * FROM performance_schema.data_locks\G
*************************** 1. row ***************************
 ENGINE: INNODB
 ENGINE_LOCK_ID: 139664434886512:1059:139664350547912
ENGINE_TRANSACTION_ID: 2569
 THREAD_ID: 46
 EVENT_ID: 12
 OBJECT_SCHEMA: test
 OBJECT_NAME: t1
 PARTITION_NAME: NULL
 SUBPARTITION_NAME: NULL
 INDEX_NAME: NULL
OBJECT_INSTANCE_BEGIN: 139664350547912
 LOCK_TYPE: TABLE
 LOCK_MODE: IX
 LOCK_STATUS: GRANTED
 LOCK_DATA: NULL
*************************** 2. row ***************************
 ENGINE: INNODB
 ENGINE_LOCK_ID: 139664434886512:2:4:1:139664350544872
ENGINE_TRANSACTION_ID: 2569
 THREAD_ID: 46
 EVENT_ID: 12
 OBJECT_SCHEMA: test
 OBJECT_NAME: t1
 PARTITION_NAME: NULL
 SUBPARTITION_NAME: NULL
 INDEX_NAME: GEN_CLUST_INDEX
OBJECT_INSTANCE_BEGIN: 139664350544872
 LOCK_TYPE: RECORD
 LOCK_MODE: X
 LOCK_STATUS: GRANTED
 LOCK_DATA: supremum pseudo-record
```

Unlike most Performance Schema data collection, there are no instruments for controlling whether data lock information is collected or system variables for controlling data lock table sizes. The Performance Schema collects information that is already available in the server, so there is no memory or CPU overhead to generate this information or need for parameters that control its collection.

Use the [data\\_locks](#page-88-0) table to help diagnose performance problems that occur during times of heavy concurrent load. For InnoDB, see the discussion of this topic at Section 17.15.2, "InnoDB INFORMATION\_SCHEMA Transaction and Locking Information".

The [data\\_locks](#page-88-0) table has these columns:

• ENGINE

The storage engine that holds or requested the lock.

• ENGINE\_LOCK\_ID

The ID of the lock held or requested by the storage engine. Tuples of (ENGINE\_LOCK\_ID, ENGINE) values are unique.

Lock ID formats are internal and subject to change at any time. Applications should not rely on lock IDs having a particular format.

• ENGINE\_TRANSACTION\_ID

The storage engine internal ID of the transaction that requested the lock. This can be considered the owner of the lock, although the lock might still be pending, not actually granted yet (LOCK\_STATUS='WAITING').

If the transaction has not yet performed any write operation (is still considered read only), the column contains internal data that users should not try to interpret. Otherwise, the column is the transaction ID.

For InnoDB, to obtain details about the transaction, join this column with the TRX\_ID column of the INFORMATION\_SCHEMA INNODB\_TRX table.

• THREAD\_ID

The thread ID of the session that created the lock. To obtain details about the thread, join this column with the THREAD\_ID column of the Performance Schema [threads](#page-156-0) table.

THREAD\_ID can be used together with EVENT\_ID to determine the event during which the lock data structure was created in memory. (This event might have occurred before this particular lock request occurred, if the data structure is used to store multiple locks.)

• EVENT\_ID

The Performance Schema event that caused the lock. Tuples of (THREAD\_ID, EVENT\_ID) values implicitly identify a parent event in other Performance Schema tables:

- The parent wait event in the events\_waits\_xxx tables
- The parent stage event in the events\_stages\_xxx tables
- The parent statement event in the events\_statements\_xxx tables
- The parent transaction event in the [events\\_transactions\\_current](#page-50-0) table

To obtain details about the parent event, join the THREAD\_ID and EVENT\_ID columns with the columns of like name in the appropriate parent event table. See [Section 29.19.2, "Obtaining Parent](#page-195-0) [Event Information".](#page-195-0)

• OBJECT\_SCHEMA

The schema that contains the locked table.

• OBJECT\_NAME

The name of the locked table.

• PARTITION\_NAME

The name of the locked partition, if any; NULL otherwise.

• SUBPARTITION\_NAME

The name of the locked subpartition, if any; NULL otherwise.

• INDEX\_NAME

The name of the locked index, if any; NULL otherwise.

In practice, InnoDB always creates an index (GEN\_CLUST\_INDEX), so INDEX\_NAME is non-NULL for InnoDB tables.

• OBJECT\_INSTANCE\_BEGIN

The address in memory of the lock.

• LOCK\_TYPE

The type of lock.

The value is storage engine dependent. For InnoDB, permitted values are RECORD for a row-level lock, TABLE for a table-level lock.

• LOCK\_MODE

How the lock is requested.

The value is storage engine dependent. For InnoDB, permitted values are S[,GAP], X[,GAP], IS[,GAP], IX[,GAP], AUTO\_INC, and UNKNOWN. Lock modes other than AUTO\_INC and UNKNOWN indicate gap locks, if present. For information about S, X, IS, IX, and gap locks, refer to Section 17.7.1, "InnoDB Locking".

• LOCK\_STATUS

The status of the lock request.

The value is storage engine dependent. For InnoDB, permitted values are GRANTED (lock is held) and WAITING (lock is being waited for).

• LOCK\_DATA

The data associated with the lock, if any. The value is storage engine dependent. For InnoDB, a value is shown if the LOCK\_TYPE is RECORD, otherwise the value is NULL. Primary key values of the locked record are shown for a lock placed on the primary key index. Secondary index values of the locked record are shown with primary key values appended for a lock placed on a secondary index. If there is no primary key, LOCK\_DATA shows either the key values of a selected unique index or the unique InnoDB internal row ID number, according to the rules governing InnoDB clustered index use (see Section 17.6.2.1, "Clustered and Secondary Indexes"). LOCK\_DATA reports "supremum pseudo-record" for a lock taken on a supremum pseudo-record. If the page containing the locked record is not in the buffer pool because it was written to disk while the lock was held, InnoDB does not fetch the page from disk. Instead, LOCK\_DATA reports NULL.

The [data\\_locks](#page-88-0) table has these indexes:

- Primary key on (ENGINE\_LOCK\_ID, ENGINE)
- Index on (ENGINE\_TRANSACTION\_ID, ENGINE)
- Index on (THREAD\_ID, EVENT\_ID)
- Index on (OBJECT\_SCHEMA, OBJECT\_NAME, PARTITION\_NAME, SUBPARTITION\_NAME)

TRUNCATE TABLE is not permitted for the [data\\_locks](#page-88-0) table.

# <span id="page-90-0"></span>**29.12.13.2 The data\_lock\_waits Table**

The [data\\_lock\\_waits](#page-90-0) table implements a many-to-many relationship showing which data lock requests in the [data\\_locks](#page-88-0) table are blocked by which held data locks in the [data\\_locks](#page-88-0) table. Held locks in [data\\_locks](#page-88-0) appear in [data\\_lock\\_waits](#page-90-0) only if they block some lock request.

This information enables you to understand data lock dependencies between sessions. The table exposes not only which lock a session or transaction is waiting for, but which session or transaction currently holds that lock.

Example data lock wait information:

```
mysql> SELECT * FROM performance_schema.data_lock_waits\G
*************************** 1. row ***************************
 ENGINE: INNODB
 REQUESTING_ENGINE_LOCK_ID: 140211201964816:2:4:2:140211086465800
REQUESTING_ENGINE_TRANSACTION_ID: 1555
 REQUESTING_THREAD_ID: 47
 REQUESTING_EVENT_ID: 5
REQUESTING_OBJECT_INSTANCE_BEGIN: 140211086465800
 BLOCKING_ENGINE_LOCK_ID: 140211201963888:2:4:2:140211086459880
 BLOCKING_ENGINE_TRANSACTION_ID: 1554
 BLOCKING_THREAD_ID: 46
 BLOCKING_EVENT_ID: 12
 BLOCKING_OBJECT_INSTANCE_BEGIN: 140211086459880
```

Unlike most Performance Schema data collection, there are no instruments for controlling whether data lock information is collected or system variables for controlling data lock table sizes. The Performance Schema collects information that is already available in the server, so there is no memory or CPU overhead to generate this information or need for parameters that control its collection.

Use the [data\\_lock\\_waits](#page-90-0) table to help diagnose performance problems that occur during times of heavy concurrent load. For InnoDB, see the discussion of this topic at Section 17.15.2, "InnoDB INFORMATION\_SCHEMA Transaction and Locking Information".

Because the columns in the [data\\_lock\\_waits](#page-90-0) table are similar to those in the [data\\_locks](#page-88-0) table, the column descriptions here are abbreviated. For more detailed column descriptions, see [Section 29.12.13.1, "The data\\_locks Table"](#page-88-0).

The [data\\_lock\\_waits](#page-90-0) table has these columns:

• ENGINE

The storage engine that requested the lock.

• REQUESTING\_ENGINE\_LOCK\_ID

The ID of the lock requested by the storage engine. To obtain details about the lock, join this column with the ENGINE\_LOCK\_ID column of the [data\\_locks](#page-88-0) table.

• REQUESTING\_ENGINE\_TRANSACTION\_ID

The storage engine internal ID of the transaction that requested the lock.

• REQUESTING\_THREAD\_ID

The thread ID of the session that requested the lock.

• REQUESTING\_EVENT\_ID

The Performance Schema event that caused the lock request in the session that requested the lock.

• REQUESTING\_OBJECT\_INSTANCE\_BEGIN

The address in memory of the requested lock.

• BLOCKING\_ENGINE\_LOCK\_ID

The ID of the blocking lock. To obtain details about the lock, join this column with the ENGINE\_LOCK\_ID column of the [data\\_locks](#page-88-0) table.

• BLOCKING\_ENGINE\_TRANSACTION\_ID

The storage engine internal ID of the transaction that holds the blocking lock.

• BLOCKING\_THREAD\_ID

The thread ID of the session that holds the blocking lock.

• BLOCKING\_EVENT\_ID

The Performance Schema event that caused the blocking lock in the session that holds it.

• BLOCKING\_OBJECT\_INSTANCE\_BEGIN

The address in memory of the blocking lock.

The [data\\_lock\\_waits](#page-90-0) table has these indexes:

- Index on (REQUESTING\_ENGINE\_LOCK\_ID, ENGINE)
- Index on (BLOCKING\_ENGINE\_LOCK\_ID, ENGINE)
- Index on (REQUESTING\_ENGINE\_TRANSACTION\_ID, ENGINE)
- Index on (BLOCKING\_ENGINE\_TRANSACTION\_ID, ENGINE)
- Index on (REQUESTING\_THREAD\_ID, REQUESTING\_EVENT\_ID)
- Index on (BLOCKING\_THREAD\_ID, BLOCKING\_EVENT\_ID)

TRUNCATE TABLE is not permitted for the [data\\_lock\\_waits](#page-90-0) table.

### <span id="page-92-0"></span>**29.12.13.3 The metadata\_locks Table**

MySQL uses metadata locking to manage concurrent access to database objects and to ensure data consistency; see Section 10.11.4, "Metadata Locking". Metadata locking applies not just to tables, but also to schemas, stored programs (procedures, functions, triggers, scheduled events), tablespaces, user locks acquired with the GET\_LOCK() function (see Section 14.14, "Locking Functions"), and locks acquired with the locking service described in Section 7.6.9.1, "The Locking Service".

The Performance Schema exposes metadata lock information through the [metadata\\_locks](#page-92-0) table:

- Locks that have been granted (shows which sessions own which current metadata locks).
- Locks that have been requested but not yet granted (shows which sessions are waiting for which metadata locks).
- Lock requests that have been killed by the deadlock detector.
- Lock requests that have timed out and are waiting for the requesting session's lock request to be discarded.

This information enables you to understand metadata lock dependencies between sessions. You can see not only which lock a session is waiting for, but which session currently holds that lock.

The [metadata\\_locks](#page-92-0) table is read only and cannot be updated. It is autosized by default; to configure the table size, set the [performance\\_schema\\_max\\_metadata\\_locks](#page-177-0) system variable at server startup.

Metadata lock instrumentation uses the wait/lock/metadata/sql/mdl instrument, which is enabled by default.

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

The Performance Schema maintains [metadata\\_locks](#page-92-0) table content as follows, using the LOCK\_STATUS column to indicate the status of each lock:

- When a metadata lock is requested and obtained immediately, a row with a status of GRANTED is inserted.
- When a metadata lock is requested and not obtained immediately, a row with a status of PENDING is inserted.
- When a metadata lock previously requested is granted, its row status is updated to GRANTED.
- When a metadata lock is released, its row is deleted.
- When a pending lock request is canceled by the deadlock detector to break a deadlock ([ER\\_LOCK\\_DEADLOCK](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_lock_deadlock)), its row status is updated from PENDING to VICTIM.
- When a pending lock request times out ([ER\\_LOCK\\_WAIT\\_TIMEOUT](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_lock_wait_timeout)), its row status is updated from PENDING to TIMEOUT.
- When granted lock or pending lock request is killed, its row status is updated from GRANTED or PENDING to KILLED.
- The VICTIM, TIMEOUT, and KILLED status values are brief and signify that the lock row is about to be deleted.
- The PRE\_ACQUIRE\_NOTIFY and POST\_RELEASE\_NOTIFY status values are brief and signify that the metadata locking subsubsystem is notifying interested storage engines while entering lock acquisition operations or leaving lock release operations.

The [metadata\\_locks](#page-92-0) table has these columns:

• OBJECT\_TYPE

The type of lock used in the metadata lock subsystem. The value is one of GLOBAL, SCHEMA, TABLE, FUNCTION, PROCEDURE, TRIGGER (currently unused), EVENT, COMMIT, USER LEVEL LOCK, TABLESPACE, BACKUP LOCK, or LOCKING SERVICE.

A value of USER LEVEL LOCK indicates a lock acquired with GET\_LOCK(). A value of LOCKING SERVICE indicates a lock acquired with the locking service described in Section 7.6.9.1, "The Locking Service".

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

The [metadata\\_locks](#page-92-0) table has these indexes:

- Primary key on (OBJECT\_INSTANCE\_BEGIN)
- Index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)
- Index on (OWNER\_THREAD\_ID, OWNER\_EVENT\_ID)

TRUNCATE TABLE is not permitted for the [metadata\\_locks](#page-92-0) table.

### <span id="page-94-0"></span>**29.12.13.4 The table\_handles Table**

The Performance Schema exposes table lock information through the [table\\_handles](#page-94-0) table to show the table locks currently in effect for each opened table handle. [table\\_handles](#page-94-0) reports what is recorded by the table lock instrumentation. This information shows which table handles the server has open, how they are locked, and by which sessions.

The [table\\_handles](#page-94-0) table is read only and cannot be updated. It is autosized by default; to configure the table size, set the [performance\\_schema\\_max\\_table\\_handles](#page-183-0) system variable at server startup.

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

The [table\\_handles](#page-94-0) table has these columns:

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

The [table\\_handles](#page-94-0) table has these indexes:

- Primary key on (OBJECT\_INSTANCE\_BEGIN)
- Index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)
- Index on (OWNER\_THREAD\_ID, OWNER\_EVENT\_ID)

TRUNCATE TABLE is not permitted for the [table\\_handles](#page-94-0) table.

# <span id="page-96-0"></span>**29.12.14 Performance Schema System Variable Tables**

The MySQL server maintains many system variables that indicate how it is configured (see Section 7.1.8, "Server System Variables"). System variable information is available in these Performance Schema tables:

- [global\\_variables](#page-96-0): Global system variables. An application that wants only global values should use this table.
- [session\\_variables](#page-96-0): System variables for the current session. An application that wants all system variable values for its own session should use this table. It includes the session variables for its session, as well as the values of global variables that have no session counterpart.
- [variables\\_by\\_thread](#page-96-0): Session system variables for each active session. An application that wants to know the session variable values for specific sessions should use this table. It includes session variables only, identified by thread ID.
- [persisted\\_variables](#page-97-0): Provides a SQL interface to the mysqld-auto.cnf file that stores persisted global system variable settings. See [Section 29.12.14.1, "Performance Schema](#page-97-0) [persisted\\_variables Table"](#page-97-0).
- [variables\\_info](#page-98-0): Shows, for each system variable, the source from which it was most recently set, and its range of values. See [Section 29.12.14.2, "Performance Schema variables\\_info Table"](#page-98-0).

The SENSITIVE\_VARIABLES\_OBSERVER privilege is required to view the values of sensitive system variables in these tables.

The session variable tables ([session\\_variables](#page-96-0), [variables\\_by\\_thread](#page-96-0)) contain information only for active sessions, not terminated sessions.

The [global\\_variables](#page-96-0) and [session\\_variables](#page-96-0) tables have these columns:

• VARIABLE\_NAME

The system variable name.

• VARIABLE\_VALUE

The system variable value. For [global\\_variables](#page-96-0), this column contains the global value. For [session\\_variables](#page-96-0), this column contains the variable value in effect for the current session.

The [global\\_variables](#page-96-0) and [session\\_variables](#page-96-0) tables have these indexes:

• Primary key on (VARIABLE\_NAME)

The [variables\\_by\\_thread](#page-96-0) table has these columns:

• THREAD\_ID

The thread identifier of the session in which the system variable is defined.

• VARIABLE\_NAME

The system variable name.

• VARIABLE\_VALUE

The session variable value for the session named by the THREAD\_ID column.

The [variables\\_by\\_thread](#page-96-0) table has these indexes:

• Primary key on (THREAD\_ID, VARIABLE\_NAME)

The [variables\\_by\\_thread](#page-96-0) table contains system variable information only about foreground threads. If not all threads are instrumented by the Performance Schema, this table misses some rows. In this case, the [Performance\\_schema\\_thread\\_instances\\_lost](#page-191-0) status variable is greater than zero.

TRUNCATE TABLE is not supported for Performance Schema system variable tables.

## <span id="page-97-0"></span>**29.12.14.1 Performance Schema persisted\_variables Table**

The [persisted\\_variables](#page-97-0) table provides an SQL interface to the mysqld-auto.cnf file that stores persisted global system variable settings, enabling the file contents to be inspected at runtime using SELECT statements. Variables are persisted using SET PERSIST or PERSIST\_ONLY statements; see Section 15.7.6.1, "SET Syntax for Variable Assignment". The table contains a row for each persisted system variable in the file. Variables not persisted do not appear in the table.

The SENSITIVE\_VARIABLES\_OBSERVER privilege is required to view the values of sensitive system variables in this table.

For information about persisted system variables, see Section 7.1.9.3, "Persisted System Variables".

Suppose that mysqld-auto.cnf looks like this (slightly reformatted):

```
{
 "Version": 1,
 "mysql_server": {
 "max_connections": {
 "Value": "1000",
 "Metadata": {
 "Timestamp": 1.519921706e+15,
 "User": "root",
 "Host": "localhost"
 }
 },
 "autocommit": {
 "Value": "ON",
 "Metadata": {
 "Timestamp": 1.519921707e+15,
 "User": "root",
 "Host": "localhost"
 }
 }
 }
}
```

Then [persisted\\_variables](#page-97-0) has these contents:

```
mysql> SELECT * FROM performance_schema.persisted_variables;
+-----------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+-----------------+----------------+
| autocommit | ON |
| max_connections | 1000 |
+-----------------+----------------+
```

The [persisted\\_variables](#page-97-0) table has these columns:

• VARIABLE\_NAME

The variable name listed in mysqld-auto.cnf.

• VARIABLE\_VALUE

The value listed for the variable in mysqld-auto.cnf.

[persisted\\_variables](#page-97-0) has these indexes:

• Primary key on (VARIABLE\_NAME)

TRUNCATE TABLE is not permitted for the [persisted\\_variables](#page-97-0) table.

### <span id="page-98-0"></span>**29.12.14.2 Performance Schema variables\_info Table**

The [variables\\_info](#page-98-0) table shows, for each system variable, the source from which it was most recently set, and its range of values.

The [variables\\_info](#page-98-0) table has these columns:

• VARIABLE\_NAME

The variable name.

• VARIABLE\_SOURCE

The source from which the variable was most recently set:

• COMMAND\_LINE

The variable was set on the command line.

• COMPILED

The variable has its compiled-in default value. COMPILED is the value used for variables not set any other way.

• DYNAMIC

The variable was set at runtime. This includes variables set within files specified using the init\_file system variable.

• EXPLICIT

The variable was set from an option file named with the --defaults-file option.

• EXTRA

The variable was set from an option file named with the --defaults-extra-file option.

• GLOBAL

The variable was set from a global option file. This includes option files not covered by EXPLICIT, EXTRA, LOGIN, PERSISTED, SERVER, or USER.

• LOGIN

The variable was set from a user-specific login path file (~/.mylogin.cnf).

• PERSISTED

The variable was set from a server-specific mysqld-auto.cnf option file. No row has this value if the server was started with persisted\_globals\_load disabled.

• SERVER

The variable was set from a server-specific \$MYSQL\_HOME/my.cnf option file. For details about how MYSQL\_HOME is set, see Section 6.2.2.2, "Using Option Files".

• USER

The variable was set from a user-specific ~/.my.cnf option file.

• VARIABLE\_PATH

If the variable was set from an option file, VARIABLE\_PATH is the path name of that file. Otherwise, the value is the empty string.

• MIN\_VALUE

The minimum permitted value for the variable. For a variable whose type is not numeric, this is always 0.

• MAX\_VALUE

The maximum permitted value for the variable. For a variable whose type is not numeric, this is always 0.

• SET\_TIME

The time at which the variable was most recently set. The default is the time at which the server initialized global system variables during startup.

• SET\_USER, SET\_HOST

The user name and host name of the client user that most recently set the variable. If a client connects as user17 from host host34.example.com using the account 'user17'@'%.example.com, SET\_USER and SET\_HOST are user17 and host34.example.com, respectively. For proxy user connections, these values correspond to the external (proxy) user, not the proxied user against which privilege checking is performed. The default for each column is the empty string, indicating that the variable has not been set since server startup.

The [variables\\_info](#page-98-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [variables\\_info](#page-98-0) table.

If a variable with a VARIABLE\_SOURCE value other than DYNAMIC is set at runtime, VARIABLE\_SOURCE becomes DYNAMIC and VARIABLE\_PATH becomes the empty string.

A system variable that has only a session value (such as debug\_sync) cannot be set at startup or persisted. For session-only system variables, VARIABLE\_SOURCE can be only COMPILED or DYNAMIC.

If a system variable has an unexpected VARIABLE\_SOURCE value, consider your server startup method. For example, mysqld\_safe reads option files and passes certain options it finds there as part of the command line that it uses to start mysqld. Consequently, some system variables that you set in option files might display in [variables\\_info](#page-98-0) as COMMAND\_LINE, rather than as GLOBAL or SERVER as you might otherwise expect.

Some sample queries that use the [variables\\_info](#page-98-0) table, with representative output:

• Display variables set on the command line:

```
mysql> SELECT VARIABLE_NAME
 FROM performance_schema.variables_info
 WHERE VARIABLE_SOURCE = 'COMMAND_LINE'
 ORDER BY VARIABLE_NAME;
+---------------+
| VARIABLE_NAME |
+---------------+
| basedir |
| datadir |
| log_error |
| pid_file |
| plugin_dir |
| port |
+---------------+
```

• Display variables set from persistent storage:

```
mysql> SELECT VARIABLE_NAME
 FROM performance_schema.variables_info
 WHERE VARIABLE_SOURCE = 'PERSISTED'
 ORDER BY VARIABLE_NAME;
+--------------------------+
| VARIABLE_NAME |
+--------------------------+
| event_scheduler |
| max_connections |
| validate_password.policy |
+--------------------------+
```

• Join [variables\\_info](#page-98-0) with the [global\\_variables](#page-96-0) table to display the current values of persisted variables, together with their range of values:

```
mysql> SELECT
 VI.VARIABLE_NAME, GV.VARIABLE_VALUE,
 VI.MIN_VALUE,VI.MAX_VALUE
 FROM performance_schema.variables_info AS VI
 INNER JOIN performance_schema.global_variables AS GV
 USING(VARIABLE_NAME)
 WHERE VI.VARIABLE_SOURCE = 'PERSISTED'
 ORDER BY VARIABLE_NAME;
+--------------------------+----------------+-----------+-----------+
| VARIABLE_NAME | VARIABLE_VALUE | MIN_VALUE | MAX_VALUE |
+--------------------------+----------------+-----------+-----------+
| event_scheduler | ON | 0 | 0 |
| max_connections | 200 | 1 | 100000 |
| validate_password.policy | STRONG | 0 | 0 |
+--------------------------+----------------+-----------+-----------+
```

# <span id="page-100-0"></span>**29.12.15 Performance Schema Status Variable Tables**

The MySQL server maintains many status variables that provide information about its operation (see Section 7.1.10, "Server Status Variables"). Status variable information is available in these Performance Schema tables:

- [global\\_status](#page-100-0): Global status variables. An application that wants only global values should use this table.
- [session\\_status](#page-100-0): Status variables for the current session. An application that wants all status variable values for its own session should use this table. It includes the session variables for its session, as well as the values of global variables that have no session counterpart.

• [status\\_by\\_thread](#page-100-0): Session status variables for each active session. An application that wants to know the session variable values for specific sessions should use this table. It includes session variables only, identified by thread ID.

There are also summary tables that provide status variable information aggregated by account, host name, and user name. See [Section 29.12.20.12, "Status Variable Summary Tables".](#page-140-0)

The session variable tables ([session\\_status](#page-100-0), [status\\_by\\_thread](#page-100-0)) contain information only for active sessions, not terminated sessions.

The Performance Schema collects statistics for global status variables only for threads for which the INSTRUMENTED value is YES in the [threads](#page-156-0) table. Statistics for session status variables are always collected, regardless of the INSTRUMENTED value.

The Performance Schema does not collect statistics for Com\_xxx status variables in the status variable tables. To obtain global and per-session statement execution counts, use the [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-120-0) and [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-120-0) tables, respectively. For example:

```
SELECT EVENT_NAME, COUNT_STAR
FROM performance_schema.events_statements_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'statement/sql/%';
```

The [global\\_status](#page-100-0) and [session\\_status](#page-100-0) tables have these columns:

• VARIABLE\_NAME

The status variable name.

• VARIABLE\_VALUE

The status variable value. For [global\\_status](#page-100-0), this column contains the global value. For [session\\_status](#page-100-0), this column contains the variable value for the current session.

The [global\\_status](#page-100-0) and [session\\_status](#page-100-0) tables have these indexes:

• Primary key on (VARIABLE\_NAME)

The [status\\_by\\_thread](#page-100-0) table contains the status of each active thread. It has these columns:

• THREAD\_ID

The thread identifier of the session in which the status variable is defined.

• VARIABLE\_NAME

The status variable name.

• VARIABLE\_VALUE

The session variable value for the session named by the THREAD\_ID column.

The [status\\_by\\_thread](#page-100-0) table has these indexes:

• Primary key on (THREAD\_ID, VARIABLE\_NAME)

The [status\\_by\\_thread](#page-100-0) table contains status variable information only about foreground threads. If the [performance\\_schema\\_max\\_thread\\_instances](#page-185-1) system variable is not autoscaled (signified by a value of −1) and the maximum permitted number of instrumented thread objects is not greater than the number of background threads, the table is empty.

The Performance Schema supports TRUNCATE TABLE for status variable tables as follows:

- [global\\_status](#page-100-0): Resets thread, account, host, and user status. Resets global status variables except those that the server never resets.
- [session\\_status](#page-100-0): Not supported.
- [status\\_by\\_thread](#page-100-0): Aggregates status for all threads to the global status and account status, then resets thread status. If account statistics are not collected, the session status is added to host and user status, if host and user status are collected.

Account, host, and user statistics are not collected if the [performance\\_schema\\_accounts\\_size](#page-169-0), [performance\\_schema\\_hosts\\_size](#page-173-2), and [performance\\_schema\\_users\\_size](#page-187-0) system variables, respectively, are set to 0.

FLUSH STATUS adds the session status from all active sessions to the global status variables, resets the status of all active sessions, and resets account, host, and user status values aggregated from disconnected sessions.