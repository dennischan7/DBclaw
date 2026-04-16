---
source: MySQL 8.4 Reference
title: 00_Overview
---

The setup tables provide information about the current instrumentation and enable the monitoring configuration to be changed. For this reason, some columns in these tables can be changed if you have the UPDATE privilege.

The use of tables rather than individual variables for setup information provides a high degree of flexibility in modifying Performance Schema configuration. For example, you can use a single statement with standard SQL syntax to make multiple simultaneous configuration changes.

These setup tables are available:

- [setup\\_actors](#page-11-0): How to initialize monitoring for new foreground threads
- [setup\\_consumers](#page-12-0): The destinations to which event information can be sent and stored
- [setup\\_instruments](#page-13-0): The classes of instrumented objects for which events can be collected
- [setup\\_objects](#page-17-0): Which objects should be monitored
- [setup\\_threads](#page-18-0): Instrumented thread names and attributes

### <span id="page-11-0"></span>**29.12.2.1 The setup\_actors Table**

The [setup\\_actors](#page-11-0) table contains information that determines whether to enable monitoring and historical event logging for new foreground server threads (threads associated with client connections). This table has a maximum size of 100 rows by default. To change the table size, modify the [performance\\_schema\\_setup\\_actors\\_size](#page-186-0) system variable at server startup.

For each new foreground thread, the Performance Schema matches the user and host for the thread against the rows of the [setup\\_actors](#page-11-0) table. If a row from that table matches, its ENABLED and HISTORY column values are used to set the INSTRUMENTED and HISTORY columns, respectively, of the [threads](#page-156-0) table row for the thread. This enables instrumenting and historical event logging to be applied selectively per host, user, or account (user and host combination). If there is no match, the INSTRUMENTED and HISTORY columns for the thread are set to NO.

For background threads, there is no associated user. INSTRUMENTED and HISTORY are YES by default and [setup\\_actors](#page-11-0) is not consulted.

The initial contents of the [setup\\_actors](#page-11-0) table match any user and host combination, so monitoring and historical event collection are enabled by default for all foreground threads:

```
mysql> SELECT * FROM performance_schema.setup_actors;
+------+------+------+---------+---------+
| HOST | USER | ROLE | ENABLED | HISTORY |
+------+------+------+---------+---------+
| % | % | % | YES | YES |
+------+------+------+---------+---------+
```

For information about how to use the [setup\\_actors](#page-11-0) table to affect event monitoring, see Section 29.4.6, "Pre-Filtering by Thread".

Modifications to the [setup\\_actors](#page-11-0) table affect only foreground threads created subsequent to the modification, not existing threads. To affect existing threads, modify the INSTRUMENTED and HISTORY columns of [threads](#page-156-0) table rows.

The [setup\\_actors](#page-11-0) table has these columns:

• HOST

The host name. This should be a literal name, or '%' to mean "any host."

• USER

The user name. This should be a literal name, or '%' to mean "any user."

• ROLE

Unused.

• ENABLED

Whether to enable instrumentation for foreground threads matched by the row. The value is YES or NO.

• HISTORY

Whether to log historical events for foreground threads matched by the row. The value is YES or NO.

The [setup\\_actors](#page-11-0) table has these indexes:

• Primary key on (HOST, USER, ROLE)

TRUNCATE TABLE is permitted for the [setup\\_actors](#page-11-0) table. It removes the rows.

### <span id="page-12-0"></span>**29.12.2.2 The setup\_consumers Table**

The [setup\\_consumers](#page-12-0) table lists the types of consumers for which event information can be stored and which are enabled:

```
mysql> SELECT * FROM performance_schema.setup_consumers;
+----------------------------------+---------+
| NAME | ENABLED |
+----------------------------------+---------+
| events_stages_current | NO |
| events_stages_history | NO |
| events_stages_history_long | NO |
| events_statements_current | YES |
| events_statements_history | YES |
| events_statements_history_long | NO |
| events_transactions_current | YES |
| events_transactions_history | YES |
| events_transactions_history_long | NO |
| events_waits_current | NO |
| events_waits_history | NO |
| events_waits_history_long | NO |
| global_instrumentation | YES |
| thread_instrumentation | YES |
| statements_digest | YES |
+----------------------------------+---------+
```

The consumer settings in the <code>setup\_consumers</code> table form a hierarchy from higher levels to lower. For detailed information about the effect of enabling different consumers, see Section 29.4.7, "Pre-Filtering by Consumer".

Modifications to the setup\_consumers table affect monitoring immediately.

The setup consumers table has these columns:

• NAME

The consumer name.

• ENABLED

Whether the consumer is enabled. The value is YES or NO. This column can be modified. If you disable a consumer, the server does not spend time adding event information to it.

The setup consumers table has these indexes:

Primary key on (NAME)

TRUNCATE TABLE is not permitted for the setup consumers table.

### <span id="page-13-0"></span>29.12.2.3 The setup\_instruments Table

The setup\_instruments table lists classes of instrumented objects for which events can be collected:

```
mysql> SELECT * FROM performance_schema.setup_instruments\G
      ***************** 1. row *******
      NAME: wait/synch/mutex/pfs/LOCK pfs share list
     ENABLED: NO
      TIMED: NO
  PROPERTIES: singleton
      FLAGS. NIII.I.
  VOLATILITY: 1
DOCUMENTATION: Components can provide their own performance schema tables.
This lock protects the list of such tables definitions.
************************* 410. row ****************
       NAME: stage/sql/executing
     ENABLED: NO
      TIMED: NO
  PROPERTIES:
      FLAGS: NULL
  VOLATILITY: 0
DOCUMENTATION: NULL
************************ 733. row ***************
       NAME: statement/abstract/Query
     ENABLED: YES
      TIMED. YES
  PROPERTIES: mutable
      FLAGS: NULL
  VOLATILITY: 0
DOCUMENTATION: SQL query just received from the network.
At this point, the real statement type is unknown, the type
will be refined after SQL parsing.
**************************************
       NAME: memory/performance_schema/mutex_instances
     ENABLED: YES
      TIMED: NULL
  PROPERTIES: global statistics
  VOLATILITY · 1
DOCUMENTATION: Memory used for table performance schema.mutex instances
**************************************
```

```
 NAME: memory/sql/Prepared_statement::infrastructure
 ENABLED: YES
 TIMED: NULL
 PROPERTIES: controlled_by_default
 FLAGS: controlled
 VOLATILITY: 0
DOCUMENTATION: Map infrastructure for prepared statements per session.
...
```

Each instrument added to the source code provides a row for the [setup\\_instruments](#page-13-0) table, even when the instrumented code is not executed. When an instrument is enabled and executed, instrumented instances are created, which are visible in the xxx\_instances tables, such as [file\\_instances](#page-21-0) or [rwlock\\_instances](#page-22-0).

Modifications to most [setup\\_instruments](#page-13-0) rows affect monitoring immediately. For some instruments, modifications are effective only at server startup; changing them at runtime has no effect. This affects primarily mutexes, conditions, and rwlocks in the server, although there may be other instruments for which this is true.

For more information about the role of the [setup\\_instruments](#page-13-0) table in event filtering, see Section 29.4.3, "Event Pre-Filtering".

The [setup\\_instruments](#page-13-0) table has these columns:

### • NAME

The instrument name. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 29.6, "Performance Schema Instrument Naming Conventions". Events produced from execution of an instrument have an EVENT\_NAME value that is taken from the instrument NAME value. (Events do not really have a "name," but this provides a way to associate events with instruments.)

### • ENABLED

Whether the instrument is enabled. The value is YES or NO. A disabled instrument produces no events. This column can be modified, although setting ENABLED has no effect for instruments that have already been created.

### • TIMED

Whether the instrument is timed. The value is YES, NO, or NULL. This column can be modified, although setting TIMED has no effect for instruments that have already been created.

A TIMED value of NULL indicates that the instrument does not support timing. For example, memory operations are not timed, so their TIMED column is NULL.

Setting TIMED to NULL for an instrument that supports timing has no effect, as does setting TIMED to non-NULL for an instrument that does not support timing.

If an enabled instrument is not timed, the instrument code is enabled, but the timer is not. Events produced by the instrument have NULL for the TIMER\_START, TIMER\_END, and TIMER\_WAIT timer values. This in turn causes those values to be ignored when calculating the sum, minimum, maximum, and average time values in summary tables.

### • PROPERTIES

The instrument properties. This column uses the SET data type, so multiple flags from the following list can be set per instrument:

- controlled\_by\_default: memory is collected by default for this instrument.
- global\_statistics: The instrument produces only global summaries. Summaries for finer levels are unavailable, such as per thread, account, user, or host. For example, most memory instruments produce only global summaries.

- mutable: The instrument can "mutate" into a more specific one. This property applies only to statement instruments.
- progress: The instrument is capable of reporting progress data. This property applies only to stage instruments.
- singleton: The instrument has a single instance. For example, most global mutex locks in the server are singletons, so the corresponding instruments are as well.
- user: The instrument is directly related to user workload (as opposed to system workload). One such instrument is wait/io/socket/sql/client\_connection.

### • FLAGS

Whether the instrument's memory is controlled.

This flag is supported for non-global memory instruments, only, and can be set or unset. For example:

```
 SQL> UPDATE PERFORMANCE_SCHEMA.SETUP_INTRUMENTS SET FLAGS="controlled" WHERE NAME='memory/sql/NET::buff';
```

![](_page_15_Picture_9.jpeg)

#### **Note**

Attempting to set FLAGS = controlled on non-memory instruments, or on global memory instruments, fails silently.

### • VOLATILITY

The instrument volatility. Volatility values range from low to high. The values correspond to the PSI\_VOLATILITY\_xxx constants defined in the mysql/psi/psi\_base.h header file:

```
#define PSI_VOLATILITY_UNKNOWN 0
#define PSI_VOLATILITY_PERMANENT 1
#define PSI_VOLATILITY_PROVISIONING 2
#define PSI_VOLATILITY_DDL 3
#define PSI_VOLATILITY_CACHE 4
#define PSI_VOLATILITY_SESSION 5
#define PSI_VOLATILITY_TRANSACTION 6
#define PSI_VOLATILITY_QUERY 7
#define PSI_VOLATILITY_INTRA_QUERY 8
```

The VOLATILITY column is purely informational, to provide users (and the Performance Schema code) some hint about the instrument runtime behavior.

Instruments with a low volatility index (PERMANENT = 1) are created once at server startup, and never destroyed or re-created during normal server operation. They are destroyed only during server shutdown.

For example, the wait/synch/mutex/pfs/LOCK\_pfs\_share\_list mutex is defined with a volatility of 1, which means it is created once. Possible overhead from the instrumentation itself

(namely, mutex initialization) has no effect for this instrument then. Runtime overhead occurs only when locking or unlocking the mutex.

Instruments with a higher volatility index (for example, SESSION = 5) are created and destroyed for every user session. For example, the wait/synch/mutex/sql/THD::LOCK\_query\_plan mutex is created each time a session connects, and destroyed when the session disconnects.

This mutex is more sensitive to Performance Schema overhead, because overhead comes not only from the lock and unlock instrumentation, but also from mutex create and destroy instrumentation, which is executed more often.

Another aspect of volatility concerns whether and when an update to the ENABLED column actually has some effect:

- An update to ENABLED affects instrumented objects created subsequently, but has no effect on instruments already created.
- Instruments that are more "volatile" use new settings from the [setup\\_instruments](#page-13-0) table sooner.

For example, this statement does not affect the LOCK\_query\_plan mutex for existing sessions, but does have an effect on new sessions created subsequent to the update:

```
UPDATE performance_schema.setup_instruments
SET ENABLED=value
WHERE NAME = 'wait/synch/mutex/sql/THD::LOCK_query_plan';
```

This statement actually has no effect at all:

```
UPDATE performance_schema.setup_instruments
SET ENABLED=value
WHERE NAME = 'wait/synch/mutex/pfs/LOCK_pfs_share_list';
```

This mutex is permanent, and was created already before the update is executed. The mutex is never created again, so the ENABLED value in [setup\\_instruments](#page-13-0) is never used. To enable or disable this mutex, use the [mutex\\_instances](#page-21-1) table instead.

• DOCUMENTATION

A string describing the instrument purpose. The value is NULL if no description is available.

The [setup\\_instruments](#page-13-0) table has these indexes:

• Primary key on (NAME)

TRUNCATE TABLE is not permitted for the [setup\\_instruments](#page-13-0) table.

To assist monitoring and troubleshooting, the Performance Schema instrumentation is used to export names of instrumented threads to the operating system. This enables utilities that display thread names, such as debuggers and the Unix ps command, to display distinct mysqld thread names rather than "mysqld". This feature is supported only on Linux, macOS, and Windows.

Suppose that mysqld is running on a system that has a version of ps that supports this invocation syntax:

```
ps -C mysqld H -o "pid tid cmd comm"
```

Without export of thread names to the operating system, the command displays output like this, where most COMMAND values are mysqld:

```
 PID TID CMD COMMAND
 1377 1377 /usr/sbin/mysqld mysqld
 1377 1528 /usr/sbin/mysqld mysqld
 1377 1529 /usr/sbin/mysqld mysqld
 1377 1530 /usr/sbin/mysqld mysqld
```

```
 1377 1531 /usr/sbin/mysqld mysqld
 1377 1534 /usr/sbin/mysqld mysqld
 1377 1535 /usr/sbin/mysqld mysqld
 1377 1588 /usr/sbin/mysqld xpl_worker1
 1377 1589 /usr/sbin/mysqld xpl_worker0
 1377 1590 /usr/sbin/mysqld mysqld
 1377 1594 /usr/sbin/mysqld mysqld
 1377 1595 /usr/sbin/mysqld mysqld
```

With export of thread names to the operating system, the output looks like this, with threads having a name similar to their instrument name:

```
 PID TID CMD COMMAND
27668 27668 /usr/sbin/mysqld mysqld
27668 27671 /usr/sbin/mysqld ib_io_ibuf
27668 27672 /usr/sbin/mysqld ib_io_log
27668 27673 /usr/sbin/mysqld ib_io_rd-1
27668 27674 /usr/sbin/mysqld ib_io_rd-2
27668 27677 /usr/sbin/mysqld ib_io_wr-1
27668 27678 /usr/sbin/mysqld ib_io_wr-2
27668 27699 /usr/sbin/mysqld xpl_worker-2
27668 27700 /usr/sbin/mysqld xpl_accept-1
27668 27710 /usr/sbin/mysqld evt_sched
27668 27711 /usr/sbin/mysqld sig_handler
27668 27933 /usr/sbin/mysqld connection
```

Different thread instances within the same class are numbered to provide distinct names where that is feasible. Due to constraints on name lengths with respect to potentially large numbers of connections, connections are named simply connection.

## <span id="page-17-0"></span>**29.12.2.4 The setup\_objects Table**

The [setup\\_objects](#page-17-0) table controls whether the Performance Schema monitors particular objects. This table has a maximum size of 100 rows by default. To change the table size, modify the [performance\\_schema\\_setup\\_objects\\_size](#page-186-1) system variable at server startup.

The initial [setup\\_objects](#page-17-0) contents look like this:

| mysql> SELECT * FROM performance_schema.setup_objects;<br>++++++ |                                       |                               |     |         |
|------------------------------------------------------------------|---------------------------------------|-------------------------------|-----|---------|
|                                                                  | OBJECT_TYPE   OBJECT_SCHEMA<br>++++++ | OBJECT_NAME   ENABLED   TIMED |     |         |
| EVENT                                                            | mysql                                 | %                             | NO  | NO<br>  |
| EVENT                                                            | performance_schema   %                |                               | NO  | NO<br>  |
| EVENT                                                            | information_schema   %                |                               | NO  | NO<br>  |
| EVENT                                                            | %                                     | %                             | YES | YES<br> |
| FUNCTION                                                         | mysql                                 | %                             | NO  | NO<br>  |
| FUNCTION                                                         | performance_schema   %                |                               | NO  | NO<br>  |
| FUNCTION                                                         | information_schema   %                |                               | NO  | NO<br>  |
| FUNCTION                                                         | %                                     | %                             | YES | YES<br> |
| PROCEDURE                                                        | mysql                                 | %                             | NO  | NO<br>  |
| PROCEDURE                                                        | performance_schema   %                |                               | NO  | NO<br>  |
| PROCEDURE                                                        | information_schema   %                |                               | NO  | NO<br>  |
| PROCEDURE                                                        | %                                     | %                             | YES | YES<br> |
| TABLE                                                            | mysql                                 | %                             | NO  | NO<br>  |
| TABLE                                                            | performance_schema   %                |                               | NO  | NO<br>  |
| TABLE                                                            | information_schema   %                |                               | NO  | NO<br>  |
| TABLE                                                            | %                                     | %                             | YES | YES<br> |
| TRIGGER                                                          | mysql                                 | %                             | NO  | NO<br>  |
| TRIGGER                                                          | performance_schema   %                |                               | NO  | NO<br>  |
| TRIGGER                                                          | information_schema   %                |                               | NO  | NO<br>  |
| TRIGGER                                                          | %                                     | %                             | YES | YES<br> |
|                                                                  | ++++++                                |                               |     |         |

Modifications to the [setup\\_objects](#page-17-0) table affect object monitoring immediately.

For object types listed in [setup\\_objects](#page-17-0), the Performance Schema uses the table to how to monitor them. Object matching is based on the OBJECT\_SCHEMA and OBJECT\_NAME columns. Objects for which there is no match are not monitored.

The effect of the default object configuration is to instrument all tables except those in the mysql, INFORMATION\_SCHEMA, and performance\_schema databases. (Tables in the INFORMATION\_SCHEMA database are not instrumented regardless of the contents of [setup\\_objects](#page-17-0); the row for information\_schema.% simply makes this default explicit.)

When the Performance Schema checks for a match in [setup\\_objects](#page-17-0), it tries to find more specific matches first. For example, with a table db1.t1, it looks for a match for 'db1' and 't1', then for 'db1' and '%', then for '%' and '%'. The order in which matching occurs matters because different matching [setup\\_objects](#page-17-0) rows can have different ENABLED and TIMED values.

Rows can be inserted into or deleted from [setup\\_objects](#page-17-0) by users with the INSERT or DELETE privilege on the table. For existing rows, only the ENABLED and TIMED columns can be modified, by users with the UPDATE privilege on the table.

For more information about the role of the [setup\\_objects](#page-17-0) table in event filtering, see Section 29.4.3, "Event Pre-Filtering".

The [setup\\_objects](#page-17-0) table has these columns:

• OBJECT\_TYPE

```
The type of object to instrument. The value is one of 'EVENT' (Event Scheduler event),
'FUNCTION' (stored function), 'PROCEDURE' (stored procedure), 'TABLE' (base table), or
'TRIGGER' (trigger).
```

TABLE filtering affects table I/O events (wait/io/table/sql/handler instrument) and table lock events (wait/lock/table/sql/handler instrument).

• OBJECT\_SCHEMA

The schema that contains the object. This should be a literal name, or '%' to mean "any schema."

• OBJECT\_NAME

The name of the instrumented object. This should be a literal name, or '%' to mean "any object."

• ENABLED

Whether events for the object are instrumented. The value is YES or NO. This column can be modified.

• TIMED

Whether events for the object are timed. This column can be modified.

The [setup\\_objects](#page-17-0) table has these indexes:

• Index on (OBJECT\_TYPE, OBJECT\_SCHEMA, OBJECT\_NAME)

TRUNCATE TABLE is permitted for the [setup\\_objects](#page-17-0) table. It removes the rows.

### <span id="page-18-0"></span>**29.12.2.5 The setup\_threads Table**

The [setup\\_threads](#page-18-0) table lists instrumented thread classes. It exposes thread class names and attributes:

```
mysql> SELECT * FROM performance_schema.setup_threads\G
*************************** 1. row ***************************
 NAME: thread/performance_schema/setup
 ENABLED: YES
 HISTORY: YES
 PROPERTIES: singleton
 VOLATILITY: 0
```

```
DOCUMENTATION: NULL
**************************************
      NAME: thread/sql/main
    ENABLED: YES
    HISTORY: YES
  PROPERTIES: singleton
  VOLATILITY: 0
DOCUMENTATION. NULL.
   **************************************
      NAME: thread/sql/one_connection
    ENABLED: YES
    HISTORY: YES
  PROPERTIES. HEAR
  VOLATILITY: 0
DOCUMENTATION: NULL
**************************************
       NAME: thread/sql/event scheduler
    ENABLED: YES
    HISTORY. YES
  PROPERTIES: singleton
  VOLATILITY: 0
DOCUMENTATION: NULL
```

The setup threads table has these columns:

#### • NAME

The instrument name. Thread instruments begin with thread (for example, thread/sql/parser service or thread/performance schema/setup).

#### • ENABLED

Whether the instrument is enabled. The value is YES or NO. This column can be modified, although setting ENABLED has no effect for threads that are already running.

For background threads, setting the ENABLED value controls whether INSTRUMENTED is set to YES or NO for threads that are subsequently created for this instrument and listed in the threads table. For foreground threads, this column has no effect; the setup actors table takes precedence.

#### • HISTORY

Whether to log historical events for the instrument. The value is YES or NO. This column can be modified, although setting HISTORY has no effect for threads that are already running.

For background threads, setting the <code>HISTORY</code> value controls whether <code>HISTORY</code> is set to <code>YES</code> or <code>NO</code> for threads that are subsequently created for this instrument and listed in the <code>threads</code> table. For foreground threads, this column has no effect; the <code>setup</code> <code>actors</code> table takes precedence.

#### • PROPERTIES

The instrument properties. This column uses the SET data type, so multiple flags from the following list can be set per instrument:

- singleton: The instrument has a single instance. For example, there is only one thread for the thread/sql/main instrument.
- user: The instrument is directly related to user workload (as opposed to system workload). For example, threads such as thread/sql/one\_connection executing a user session have the user property to differentiate them from system threads.

### • VOLATILITY

The instrument volatility. This column has the same meaning as in the <code>setup\_instruments</code> table. See Section 29.12.2.3, "The <code>setup\_instruments</code> Table".

• DOCUMENTATION

A string describing the instrument purpose. The value is NULL if no description is available.

The [setup\\_threads](#page-18-0) table has these indexes:

• Primary key on (NAME)

TRUNCATE TABLE is not permitted for the [setup\\_threads](#page-18-0) table.