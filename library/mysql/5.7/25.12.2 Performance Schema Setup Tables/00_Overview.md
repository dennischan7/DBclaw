---
source: MySQL 5.7 Reference
title: 00_Overview
---

The setup tables provide information about the current instrumentation and enable the monitoring configuration to be changed. For this reason, some columns in these tables can be changed if you have the UPDATE privilege.

The use of tables rather than individual variables for setup information provides a high degree of flexibility in modifying Performance Schema configuration. For example, you can use a single statement with standard SQL syntax to make multiple simultaneous configuration changes.

These setup tables are available:

- [setup\\_actors](#page-11-0): How to initialize monitoring for new foreground threads
- [setup\\_consumers](#page-12-0): The destinations to which event information can be sent and stored
- [setup\\_instruments](#page-13-0): The classes of instrumented objects for which events can be collected
- [setup\\_objects](#page-14-0): Which objects should be monitored
- [setup\\_timers](#page-15-0): The current event timer

## <span id="page-11-0"></span>**25.12.2.1 The setup\_actors Table**

The [setup\\_actors](#page-11-0) table contains information that determines whether to enable monitoring and historical event logging for new foreground server threads (threads associated with client connections). This table has a maximum size of 100 rows by default. To change the table size, modify the [performance\\_schema\\_setup\\_actors\\_size](#page-123-0) system variable at server startup.

For each new foreground thread, the Performance Schema matches the user and host for the thread against the rows of the [setup\\_actors](#page-11-0) table. If a row from that table matches, its ENABLED and HISTORY column values are used to set the INSTRUMENTED and HISTORY columns, respectively, of the [threads](#page-100-0) table row for the thread. This enables instrumenting and historical event logging to be applied selectively per host, user, or account (user and host combination). If there is no match, the INSTRUMENTED and HISTORY columns for the thread are set to NO.

For background threads, there is no associated user. INSTRUMENTED and HISTORY are YES by default and [setup\\_actors](#page-11-0) is not consulted.

The initial contents of the [setup\\_actors](#page-11-0) table match any user and host combination, so monitoring and historical event collection are enabled by default for all foreground threads:

![](_page_12_Picture_2.jpeg)

For information about how to use the [setup\\_actors](#page-11-0) table to affect event monitoring, see Section 25.4.6, "Pre-Filtering by Thread".

Modifications to the [setup\\_actors](#page-11-0) table affect only foreground threads created subsequent to the modification, not existing threads. To affect existing threads, modify the INSTRUMENTED and HISTORY columns of [threads](#page-100-0) table rows.

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

TRUNCATE TABLE is permitted for the [setup\\_actors](#page-11-0) table. It removes the rows.

## <span id="page-12-0"></span>**25.12.2.2 The setup\_consumers Table**

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
| events_transactions_current | NO |
| events_transactions_history | NO |
| events_transactions_history_long | NO |
| events_waits_current | NO |
| events_waits_history | NO |
| events_waits_history_long | NO |
| global_instrumentation | YES |
| thread_instrumentation | YES |
| statements_digest | YES |
```

+----------------------------------+---------+

The consumer settings in the [setup\\_consumers](#page-12-0) table form a hierarchy from higher levels to lower. For detailed information about the effect of enabling different consumers, see Section 25.4.7, "Pre-Filtering by Consumer".

Modifications to the [setup\\_consumers](#page-12-0) table affect monitoring immediately.

The [setup\\_consumers](#page-12-0) table has these columns:

• NAME

The consumer name.

• ENABLED

Whether the consumer is enabled. The value is YES or NO. This column can be modified. If you disable a consumer, the server does not spend time adding event information to it.

TRUNCATE TABLE is not permitted for the [setup\\_consumers](#page-12-0) table.

## <span id="page-13-0"></span>**25.12.2.3 The setup\_instruments Table**

The [setup\\_instruments](#page-13-0) table lists classes of instrumented objects for which events can be collected:

| mysql> SELECT * FROM performance_schema.setup_instruments;                                 |                 |              |      |
|--------------------------------------------------------------------------------------------|-----------------|--------------|------|
| ++++<br>  NAME                                                                             | ENABLED   TIMED |              |      |
| ++++<br>                                                                                   |                 |              |      |
| stage/sql/end                                                                              | NO              | NO           |      |
| stage/sql/executing                                                                        | NO              | NO           |      |
| stage/sql/init                                                                             | NO              | NO           |      |
| stage/sql/insert                                                                           | NO              | NO           |      |
|                                                                                            |                 |              |      |
| statement/sql/load                                                                         | YES             | YES          |      |
| statement/sql/grant                                                                        | YES             | YES          |      |
| statement/sql/check                                                                        | YES             | YES          |      |
| statement/sql/flush                                                                        | YES             | YES          |      |
|                                                                                            |                 |              |      |
| wait/synch/mutex/sql/LOCK_global_read_lock                                                 | YES             | YES          |      |
| wait/synch/mutex/sql/LOCK_global_system_variables   YES                                    |                 | YES          |      |
| wait/synch/mutex/sql/LOCK_lock_db                                                          | YES             | YES          |      |
| wait/synch/mutex/sql/LOCK_manager                                                          | YES             | YES          |      |
|                                                                                            |                 |              |      |
| wait/synch/rwlock/sql/LOCK_grant                                                           | YES             | YES          |      |
| wait/synch/rwlock/sql/LOGGER::LOCK_logger<br>  wait/synch/rwlock/sql/LOCK_sys_init_connect | YES<br>  YES    | YES<br>  YES | <br> |
| wait/synch/rwlock/sql/LOCK_sys_init_slave                                                  | YES             | YES          |      |
|                                                                                            |                 |              |      |
| wait/io/file/sql/binlog                                                                    | YES             | YES          |      |
| wait/io/file/sql/binlog_index                                                              | YES             | YES          |      |
| wait/io/file/sql/casetest                                                                  | YES             | YES          |      |
| wait/io/file/sql/dbopt                                                                     | YES             | YES          |      |
|                                                                                            |                 |              |      |
|                                                                                            |                 |              |      |

Each instrument added to the source code provides a row for the [setup\\_instruments](#page-13-0) table, even when the instrumented code is not executed. When an instrument is enabled and executed, instrumented instances are created, which are visible in the xxx\_instances tables, such as [file\\_instances](#page-17-0) or [rwlock\\_instances](#page-18-0).

Modifications to most [setup\\_instruments](#page-13-0) rows affect monitoring immediately. For some instruments, modifications are effective only at server startup; changing them at runtime has no effect. This affects primarily mutexes, conditions, and rwlocks in the server, although there may be other instruments for which this is true.

For more information about the role of the [setup\\_instruments](#page-13-0) table in event filtering, see Section 25.4.3, "Event Pre-Filtering".

The [setup\\_instruments](#page-13-0) table has these columns:

#### • NAME

The instrument name. Instrument names may have multiple parts and form a hierarchy, as discussed in Section 25.6, "Performance Schema Instrument Naming Conventions". Events produced from execution of an instrument have an EVENT\_NAME value that is taken from the instrument NAME value. (Events do not really have a "name," but this provides a way to associate events with instruments.)

#### • ENABLED

Whether the instrument is enabled. The value is YES or NO. A disabled instrument produces no events. This column can be modified, although setting ENABLED has no effect for instruments that have already been created.

#### • TIMED

Whether the instrument is timed. The value is YES or NO. This column can be modified, although setting TIMED has no effect for instruments that have already been created.

For memory instruments, the TIMED column in [setup\\_instruments](#page-13-0) is ignored because memory operations are not timed.

If an enabled instrument is not timed, the instrument code is enabled, but the timer is not. Events produced by the instrument have NULL for the TIMER\_START, TIMER\_END, and TIMER\_WAIT timer values. This in turn causes those values to be ignored when calculating the sum, minimum, maximum, and average time values in summary tables.

TRUNCATE TABLE is not permitted for the [setup\\_instruments](#page-13-0) table.

## <span id="page-14-0"></span>**25.12.2.4 The setup\_objects Table**

The [setup\\_objects](#page-14-0) table controls whether the Performance Schema monitors particular objects. This table has a maximum size of 100 rows by default. To change the table size, modify the [performance\\_schema\\_setup\\_objects\\_size](#page-124-0) system variable at server startup.

The initial [setup\\_objects](#page-14-0) contents look like this:

| mysql> SELECT * FROM performance_schema.setup_objects;<br>++++++ |                                       |                               |     |         |  |  |
|------------------------------------------------------------------|---------------------------------------|-------------------------------|-----|---------|--|--|
|                                                                  | OBJECT_TYPE   OBJECT_SCHEMA<br>++++++ | OBJECT_NAME   ENABLED   TIMED |     |         |  |  |
| EVENT                                                            | mysql                                 | %                             | NO  | NO<br>  |  |  |
| EVENT                                                            | performance_schema   %                |                               | NO  | NO<br>  |  |  |
| EVENT                                                            | information_schema   %                |                               | NO  | NO<br>  |  |  |
| EVENT                                                            | %                                     | %                             | YES | YES<br> |  |  |
| FUNCTION                                                         | mysql                                 | %                             | NO  | NO<br>  |  |  |
| FUNCTION                                                         | performance_schema   %                |                               | NO  | NO<br>  |  |  |
| FUNCTION                                                         | information_schema   %                |                               | NO  | NO<br>  |  |  |
| FUNCTION                                                         | %                                     | %                             | YES | YES<br> |  |  |
| PROCEDURE                                                        | mysql                                 | %                             | NO  | NO<br>  |  |  |
| PROCEDURE                                                        | performance_schema   %                |                               | NO  | NO<br>  |  |  |
| PROCEDURE                                                        | information_schema   %                |                               | NO  | NO<br>  |  |  |
| PROCEDURE                                                        | %                                     | %                             | YES | YES<br> |  |  |
| TABLE                                                            | mysql                                 | %                             | NO  | NO<br>  |  |  |
| TABLE                                                            | performance_schema   %                |                               | NO  | NO<br>  |  |  |
| TABLE                                                            | information_schema   %                |                               | NO  | NO<br>  |  |  |
| TABLE                                                            | %                                     | %                             | YES | YES<br> |  |  |
| TRIGGER                                                          | mysql                                 | %                             | NO  | NO<br>  |  |  |
| TRIGGER                                                          | performance_schema   %                |                               | NO  | NO<br>  |  |  |
| TRIGGER                                                          | information_schema   %                |                               | NO  | NO<br>  |  |  |
| TRIGGER                                                          | %                                     | %                             | YES | YES<br> |  |  |

+-------------+--------------------+-------------+---------+-------+

Modifications to the [setup\\_objects](#page-14-0) table affect object monitoring immediately.

For object types listed in [setup\\_objects](#page-14-0), the Performance Schema uses the table to how to monitor them. Object matching is based on the OBJECT\_SCHEMA and OBJECT\_NAME columns. Objects for which there is no match are not monitored.

The effect of the default object configuration is to instrument all tables except those in the mysql, INFORMATION\_SCHEMA, and performance\_schema databases. (Tables in the INFORMATION\_SCHEMA database are not instrumented regardless of the contents of [setup\\_objects](#page-14-0); the row for information\_schema.% simply makes this default explicit.)

When the Performance Schema checks for a match in [setup\\_objects](#page-14-0), it tries to find more specific matches first. For example, with a table db1.t1, it looks for a match for 'db1' and 't1', then for 'db1' and '%', then for '%' and '%'. The order in which matching occurs matters because different matching [setup\\_objects](#page-14-0) rows can have different ENABLED and TIMED values.

Rows can be inserted into or deleted from [setup\\_objects](#page-14-0) by users with the INSERT or DELETE privilege on the table. For existing rows, only the ENABLED and TIMED columns can be modified, by users with the UPDATE privilege on the table.

For more information about the role of the [setup\\_objects](#page-14-0) table in event filtering, see Section 25.4.3, "Event Pre-Filtering".

The [setup\\_objects](#page-14-0) table has these columns:

• OBJECT\_TYPE

The type of object to instrument. The value is one of 'EVENT' (Event Scheduler event), 'FUNCTION' (stored function), 'PROCEDURE' (stored procedure), 'TABLE' (base table), or 'TRIGGER' (trigger).

TABLE filtering affects table I/O events (wait/io/table/sql/handler instrument) and table lock events (wait/lock/table/sql/handler instrument).

• OBJECT\_SCHEMA

The schema that contains the object. This should be a literal name, or '%' to mean "any schema."

• OBJECT\_NAME

The name of the instrumented object. This should be a literal name, or '%' to mean "any object."

• ENABLED

Whether events for the object are instrumented. The value is YES or NO. This column can be modified.

• TIMED

Whether events for the object are timed. The value is YES or NO. This column can be modified.

TRUNCATE TABLE is permitted for the [setup\\_objects](#page-14-0) table. It removes the rows.

## <span id="page-15-0"></span>**25.12.2.5 The setup\_timers Table**

The [setup\\_timers](#page-15-0) table shows the currently selected event timers:

```
mysql> SELECT * FROM performance_schema.setup_timers;
+-------------+-------------+
| NAME | TIMER_NAME |
+-------------+-------------+
| idle | MICROSECOND |
```

| wait                     | CYCLE      |  |
|--------------------------|------------|--|
| stage                    | NANOSECOND |  |
| statement                | NANOSECOND |  |
| transaction   NANOSECOND |            |  |
| +++                      |            |  |

![](_page_16_Picture_2.jpeg)

#### **Note**

As of MySQL 5.7.21, the Performance Schema [setup\\_timers](#page-15-0) table is deprecated and is removed in MySQL 8.0, as is the TICKS row in the [performance\\_timers](#page-96-0) table.

The setup\_timers.TIMER\_NAME value can be changed to select a different timer. The value can be any of the values in the performance\_timers.TIMER\_NAME column. For an explanation of how event timing occurs, see Section 25.4.1, "Performance Schema Event Timing".

Modifications to the [setup\\_timers](#page-15-0) table affect monitoring immediately. Events already in progress may use the original timer for the begin time and the new timer for the end time. To avoid unpredictable results after you make timer changes, use TRUNCATE TABLE to reset Performance Schema statistics.

The [setup\\_timers](#page-15-0) table has these columns:

• NAME

The type of instrument the timer is used for.

• TIMER\_NAME

The timer that applies to the instrument type. This column can be modified.

TRUNCATE TABLE is not permitted for the [setup\\_timers](#page-15-0) table.