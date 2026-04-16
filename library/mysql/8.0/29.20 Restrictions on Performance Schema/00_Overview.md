---
source: MySQL 8.0 Reference
title: 00_Overview
---

The Performance Schema avoids using mutexes to collect or produce data, so there are no guarantees of consistency and results can sometimes be incorrect. Event values in performance\_schema tables are nondeterministic and nonrepeatable.

If you save event information in another table, you should not assume that the original events remain available later. For example, if you select events from a performance\_schema table into a temporary table, intending to join that table with the original table later, there might be no matches.

mysqldump and BACKUP DATABASE ignore tables in the performance\_schema database.

Tables in the performance\_schema database cannot be locked with LOCK TABLES, except the setup\_xxx tables.

Tables in the performance\_schema database cannot be indexed.

Tables in the performance\_schema database are not replicated.

The types of timers might vary per platform. The [performance\\_timers](#page-95-0) table shows which event timers are available. If the values in this table for a given timer name are NULL, that timer is not supported on your platform.

Instruments that apply to storage engines might not be implemented for all storage engines. Instrumentation of each third-party engine is the responsibility of the engine maintainer.

# <span id="page-140-1"></span>Chapter 30 MySQL sys Schema

# **Table of Contents**

| 30.1 Prerequisites for Using the sys Schema 5311 |  |
|--------------------------------------------------|--|
| 30.2 Using the sys Schema 5312                   |  |
| 30.3 sys Schema Progress Reporting 5313          |  |
| 30.4 sys Schema Object Reference 5314            |  |
| 30.4.1 sys Schema Object Index 5314              |  |
| 30.4.2 sys Schema Tables and Triggers 5319       |  |
| 30.4.3 sys Schema Views 5321                     |  |
| 30.4.4 sys Schema Stored Procedures 5361         |  |
| 30.4.5 sys Schema Stored Functions 5379          |  |

MySQL 8.0 includes the [sys](#page-140-1) schema, a set of objects that helps DBAs and developers interpret data collected by the Performance Schema. [sys](#page-140-1) schema objects can be used for typical tuning and diagnosis use cases. Objects in this schema include:

- Views that summarize Performance Schema data into more easily understandable form.
- Stored procedures that perform operations such as Performance Schema configuration and generating diagnostic reports.
- Stored functions that query Performance Schema configuration and provide formatting services.

For new installations, the [sys](#page-140-1) schema is installed by default during data directory initialization if you use mysqld with the --initialize or --initialize-insecure option. If this is not desired, you can drop the [sys](#page-140-1) schema manually after initialization if it is unneeded.

The MySQL upgrade procedure produces an error if a [sys](#page-140-1) schema exists but has no [version](#page-187-0) view, on the assumption that absence of this view indicates a user-created sys schema. To upgrade in this case, remove or rename the existing [sys](#page-140-1) schema first.

[sys](#page-140-1) schema objects have a DEFINER of 'mysql.sys'@'localhost'. Use of the dedicated mysql.sys account avoids problems that occur if a DBA renames or removes the root account.

# <span id="page-140-0"></span>**30.1 Prerequisites for Using the sys Schema**

Before using the [sys](#page-140-1) schema, the prerequisites described in this section must be satisfied.

Because the [sys](#page-140-1) schema provides an alternative means of accessing the Performance Schema, the Performance Schema must be enabled for the [sys](#page-140-1) schema to work. See Section 29.3, "Performance Schema Startup Configuration".

For full access to the [sys](#page-140-1) schema, a user must have these privileges:

- SELECT on all [sys](#page-140-1) tables and views
- EXECUTE on all [sys](#page-140-1) stored procedures and functions
- INSERT and UPDATE for the [sys\\_config](#page-148-1) table, if changes are to be made to it
- Additional privileges for certain [sys](#page-140-1) schema stored procedures and functions, as noted in their descriptions (for example, the [ps\\_setup\\_save\(\)](#page-197-0) procedure)

It is also necessary to have privileges for the objects underlying the [sys](#page-140-1) schema objects:

- SELECT on any Performance Schema tables accessed by [sys](#page-140-1) schema objects, and UPDATE for any tables to be updated using [sys](#page-140-1) schema objects
- PROCESS for the INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE table

Certain Performance Schema instruments and consumers must be enabled and (for instruments) timed to take full advantage of [sys](#page-140-1) schema capabilities:

- All wait instruments
- All stage instruments
- All statement instruments
- xxx\_current and xxx\_history\_long consumers for all events

You can use the [sys](#page-140-1) schema itself to enable all of the additional instruments and consumers:

```
CALL sys.ps_setup_enable_instrument('wait');
CALL sys.ps_setup_enable_instrument('stage');
CALL sys.ps_setup_enable_instrument('statement');
CALL sys.ps_setup_enable_consumer('current');
CALL sys.ps_setup_enable_consumer('history_long');
```

![](_page_141_Picture_8.jpeg)

### **Note**

For many uses of the sys schema, the default Performance Schema is sufficient for data collection. Enabling all the instruments and consumers just mentioned has a performance impact, so it is preferable to enable only the additional configuration you need. Also, remember that if you enable additional configuration, you can easily restore the default configuration like this:

```
CALL sys.ps_setup_reset_to_default(TRUE);
```

# <span id="page-141-0"></span>**30.2 Using the sys Schema**

You can make the [sys](#page-140-1) schema the default schema so that references to its objects need not be qualified with the schema name:

```
mysql> USE sys;
Database changed
mysql> SELECT * FROM version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1 | 8.0.26-debug |
+-------------+---------------+
```

(The [version](#page-187-0) view shows the [sys](#page-140-1) schema and MySQL server versions.)

To access [sys](#page-140-1) schema objects while a different schema is the default (or simply to be explicit), qualify object references with the schema name:

```
mysql> SELECT * FROM sys.version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1 | 8.0.26-debug |
+-------------+---------------+
```

The sys schema contains many views that summarize Performance Schema tables in various ways. Most of these views come in pairs, such that one member of the pair has the same name as the other member, plus a x\$ prefix. For example, the [host\\_summary\\_by\\_file\\_io](#page-152-0) view summarizes file I/ O grouped by host and displays latencies converted from picoseconds to more readable values (with units);

```
mysql> SELECT * FROM sys.host_summary_by_file_io;
+------------+-------+------------+
| host | ios | io_latency |
+------------+-------+------------+
| localhost | 67570 | 5.38 s |
| background | 3468 | 4.18 s |
+------------+-------+------------+
```

The [x\\$host\\_summary\\_by\\_file\\_io](#page-152-0) view summarizes the same data but displays unformatted picosecond latencies:

```
mysql> SELECT * FROM sys.x$host_summary_by_file_io;
+------------+-------+---------------+
| host | ios | io_latency |
+------------+-------+---------------+
| localhost | 67574 | 5380678125144 |
| background | 3474 | 4758696829416 |
+------------+-------+---------------+
```

The view without the x\$ prefix is intended to provide output that is more user friendly and easier for humans to read. The view with the x\$ prefix that displays the same values in raw form is intended more for use with other tools that perform their own processing on the data. For additional information about the differences between non-x\$ and x\$ views, see [Section 30.4.3, "sys Schema Views".](#page-150-0)

To examine [sys](#page-140-1) schema object definitions, use the appropriate SHOW statement or INFORMATION\_SCHEMA query. For example, to examine the definitions of the [session](#page-177-0) view and format\_bytes() function, use these statements:

```
mysql> SHOW CREATE VIEW sys.session;
mysql> SHOW CREATE FUNCTION sys.format_bytes;
```

However, those statements display the definitions in relatively unformatted form. To view object definitions with more readable formatting, access the individual .sql files found under the scripts/ sys\_schema in MySQL source distributions. Prior to MySQL 8.0.18, the sources are maintained in a separate distribution available from the [sys](#page-140-1) schema development website at [https://github.com/mysql/](https://github.com/mysql/mysql-sys) [mysql-sys](https://github.com/mysql/mysql-sys).

Neither mysqldump nor mysqlpump dump the [sys](#page-140-1) schema by default. To generate a dump file, name the [sys](#page-140-1) schema explicitly on the command line using either of these commands:

```
mysqldump --databases --routines sys > sys_dump.sql
mysqlpump sys > sys_dump.sql
```

To reinstall the schema from the dump file, use this command:

```
mysql < sys_dump.sql
```

# <span id="page-142-0"></span>**30.3 sys Schema Progress Reporting**

The following [sys](#page-140-1) schema views provide progress reporting for long-running transactions:

```
processlist
session
x$processlist
x$session
```

Assuming that the required instruments and consumers are enabled, the progress column of these views shows the percentage of work completed for stages that support progress reporting.

Stage progress reporting requires that the events\_stages\_current consumer be enabled, as well as the instruments for which progress information is desired. Instruments for these stages currently support progress reporting:

```
stage/sql/Copying to tmp table
stage/innodb/alter table (end)
stage/innodb/alter table (flush)
stage/innodb/alter table (insert)
stage/innodb/alter table (log apply index)
stage/innodb/alter table (log apply table)
stage/innodb/alter table (merge sort)
stage/innodb/alter table (read PK and internal sort)
stage/innodb/buffer pool load
```

For stages that do not support estimated and completed work reporting, or if the required instruments or consumers are not enabled, the progress column is NULL.

# <span id="page-143-0"></span>**30.4 sys Schema Object Reference**

The [sys](#page-140-1) schema includes tables and triggers, views, and stored procedures and functions. The following sections provide details for each of these objects.

# <span id="page-143-1"></span>**30.4.1 sys Schema Object Index**

The following tables list [sys](#page-140-1) schema objects and provide a short description of each one.

**Table 30.1 sys Schema Tables and Triggers**

| Table or Trigger Name      | Description                            |  |
|----------------------------|----------------------------------------|--|
| sys_config                 | sys schema configuration options table |  |
| sys_config_insert_set_user | sys_config insert trigger              |  |
| sys_config_update_set_user | sys_config update trigger              |  |

### **Table 30.2 sys Schema Views**

| View Name                                                            | Description                                                       | Deprecated |
|----------------------------------------------------------------------|-------------------------------------------------------------------|------------|
| host_summary, x<br>\$host_summary                                    | Statement activity, file I/O, and<br>connections, grouped by host |            |
| host_summary_by_file_io,<br>x                                        | File I/O, grouped by host                                         |            |
| \$host_summary_by_file_io                                            |                                                                   |            |
| host_summary_by_file_io_type,<br>x                                   | File I/O, grouped by host and<br>event type                       |            |
| \$host_summary_by_file_io_type                                       |                                                                   |            |
| host_summary_by_stages, x<br>\$host_summary_by_stages                | Statement stages, grouped by<br>host                              |            |
| host_summary_by_statement_latency,<br>x                              | Statement statistics, grouped by<br>host                          |            |
| \$host_summary_by_statement_latency                                  |                                                                   |            |
| host_summary_by_statement_type,<br>x                                 | Statements executed, grouped<br>by host and statement             |            |
| \$host_summary_by_statement_type                                     |                                                                   |            |
| innodb_buffer_stats_by_schema,<br>x                                  | InnoDB buffer information,<br>grouped by schema                   |            |
| \$innodb_buffer_stats_by_schema                                      |                                                                   |            |
| innodb_buffer_stats_by_table,<br>x<br>\$innodb_buffer_stats_by_table | InnoDB buffer information,<br>grouped by schema and table         |            |
| innodb_lock_waits, x<br>\$innodb_lock_waits                          | InnoDB lock information                                           |            |
| io_by_thread_by_latency,<br>x                                        | I/O consumers, grouped by<br>thread                               |            |
| \$io_by_thread_by_latency                                            |                                                                   |            |
| io_global_by_file_by_bytes,<br>x                                     | Global I/O consumers, grouped<br>by file and bytes                |            |
| \$io_global_by_file_by_bytes                                         |                                                                   |            |
| io_global_by_file_by_latency,<br>x                                   | Global I/O consumers, grouped<br>by file and latency              |            |
| \$io_global_by_file_by_latency                                       |                                                                   |            |

| View Name                                              | Description                                 | Deprecated |
|--------------------------------------------------------|---------------------------------------------|------------|
| io_global_by_wait_by_bytes,                            | Global I/O consumers, grouped               |            |
| x                                                      | by bytes                                    |            |
| \$io_global_by_wait_by_bytes                           |                                             |            |
| io_global_by_wait_by_latency,<br>x                     | Global I/O consumers, grouped<br>by latency |            |
| \$io_global_by_wait_by_latency                         |                                             |            |
| latest_file_io, x                                      | Most recent I/O, grouped by file            |            |
| \$latest_file_io                                       | and thread                                  |            |
| memory_by_host_by_current_bytes,<br>x                  | Memory use, grouped by host                 |            |
| \$memory_by_host_by_current_bytes                      |                                             |            |
| memory_by_thread_by_current_bytes,                     | Memory use, grouped by thread               |            |
| x<br>\$memory_by_thread_by_current_bytes               |                                             |            |
| memory_by_user_by_current_bytes,                       | Memory use, grouped by user                 |            |
| x                                                      |                                             |            |
| \$memory_by_user_by_current_bytes                      |                                             |            |
| memory_global_by_current_bytes,<br>x                   | Memory use, grouped by<br>allocation type   |            |
| \$memory_global_by_current_bytes                       |                                             |            |
| memory_global_total, x<br>\$memory_global_total        | Total memory use                            |            |
| metrics                                                | Server metrics                              |            |
| processlist, x                                         | Processlist information                     |            |
| \$processlist                                          |                                             |            |
| ps_check_lost_instrumentation Variables that have lost | instruments                                 |            |
| schema_auto_increment_columns AUTO_INCREMENT column    | information                                 |            |
| schema_index_statistics,                               | Index statistics                            |            |
| x<br>\$schema_index_statistics                         |                                             |            |
| schema_object_overview                                 | Types of objects within each<br>schema      |            |
| schema_redundant_indexes                               | Duplicate or redundant indexes              |            |
| schema_table_lock_waits,                               | Sessions waiting for metadata               |            |
| x<br>\$schema_table_lock_waits                         | locks                                       |            |
| schema_table_statistics,                               | Table statistics                            |            |
| x                                                      |                                             |            |
| \$schema_table_statistics                              | Table statistics, including InnoDB          |            |
| schema_table_statistics_with_buffer,<br>x              | buffer pool statistics                      |            |
| \$schema_table_statistics_with_buffer                  |                                             |            |
| schema_tables_with_full_table_scans,                   | Tables being accessed with full             |            |
| x<br>\$schema_tables_with_full_table_scans             | scans                                       |            |
| schema_unused_indexes                                  | Indexes not in active use                   |            |
|                                                        |                                             |            |

| View Name                                                                        | Description                                           | Deprecated |
|----------------------------------------------------------------------------------|-------------------------------------------------------|------------|
| session, x\$session                                                              | Processlist information for user<br>sessions          |            |
| session_ssl_status                                                               | Connection SSL information                            |            |
| statement_analysis, x<br>\$statement_analysis                                    | Statement aggregate statistics                        |            |
| statements_with_errors_or_warnings,<br>x<br>\$statements_with_errors_or_warnings | Statements that have produced<br>errors or warnings   |            |
| statements_with_full_table_scans,<br>x<br>\$statements_with_full_table_scans     | Statements that have done full<br>table scans         |            |
| statements_with_runtimes_in_95th_percentile,<br>x                                | Statements with highest average<br>runtime            |            |
| \$statements_with_runtimes_in_95th_percentile                                    |                                                       |            |
| statements_with_sorting,<br>x                                                    | Statements that performed sorts                       |            |
| \$statements_with_sorting                                                        |                                                       |            |
| statements_with_temp_tables,<br>x                                                | Statements that used temporary<br>tables              |            |
| \$statements_with_temp_tables                                                    |                                                       |            |
| user_summary, x<br>\$user_summary                                                | User statement and connection<br>activity             |            |
| user_summary_by_file_io,                                                         | File I/O, grouped by user                             |            |
| x<br>\$user_summary_by_file_io                                                   |                                                       |            |
| user_summary_by_file_io_type,<br>x                                               | File I/O, grouped by user and<br>event                |            |
| \$user_summary_by_file_io_type                                                   |                                                       |            |
| user_summary_by_stages, x<br>\$user_summary_by_stages                            | Stage events, grouped by user                         |            |
| user_summary_by_statement_latency,                                               | Statement statistics, grouped by                      |            |
| x<br>\$user_summary_by_statement_latency                                         | user                                                  |            |
| user_summary_by_statement_type,<br>x                                             | Statements executed, grouped<br>by user and statement |            |
| \$user_summary_by_statement_type                                                 |                                                       |            |
| version                                                                          | Current sys schema and MySQL<br>server versions       | Yes        |
| wait_classes_global_by_avg_latency,                                              | Wait class average latency,                           |            |
| x<br>\$wait_classes_global_by_avg_latency                                        | grouped by event class                                |            |
| wait_classes_global_by_latency,<br>x<br>\$wait_classes_global_by_latency         | Wait class total latency, grouped<br>by event class   |            |
| waits_by_host_by_latency,<br>x                                                   | Wait events, grouped by host<br>and event             |            |
| \$waits_by_host_by_latency                                                       |                                                       |            |

| View Name                             | Description                      | Deprecated |
|---------------------------------------|----------------------------------|------------|
| waits_by_user_by_latency,             | Wait events, grouped by user     |            |
| x                                     | and event                        |            |
| \$waits_by_user_by_latency            |                                  |            |
| waits_global_by_latency,              | Wait events, grouped by event    |            |
| x                                     |                                  |            |
| \$waits_global_by_latency             |                                  |            |
| x                                     | Helper view for 95th-percentile  |            |
| \$ps_digest_95th_percentile_by_avg_us | views                            |            |
| x                                     | Helper view for 95th-percentile  |            |
| \$ps_digest_avg_latency_distribution  | views                            |            |
| x                                     | Helper view for table-statistics |            |
| \$ps_schema_table_statistics_io       | views                            |            |
| x\$schema_flattened_keys              | Helper view for                  |            |
|                                       | schema_redundant_indexes         |            |

#### **Table 30.3 sys Schema Stored Procedures**

| Procedure Name                        | Description                                            |  |
|---------------------------------------|--------------------------------------------------------|--|
| create_synonym_db()                   | Create synonym for schema                              |  |
| diagnostics()                         | Collect system diagnostic information                  |  |
| execute_prepared_stmt()               | Execute prepared statement                             |  |
| ps_setup_disable_background_threads() | Disable background thread instrumentation              |  |
| ps_setup_disable_consumer()           | Disable consumers                                      |  |
| ps_setup_disable_instrument()         | Disable instruments                                    |  |
| ps_setup_disable_thread()             | Disable instrumentation for thread                     |  |
| ps_setup_enable_background_threads()  | Enable background thread instrumentation               |  |
| ps_setup_enable_consumer()            | Enable consumers                                       |  |
| ps_setup_enable_instrument()          | Enable instruments                                     |  |
| ps_setup_enable_thread()              | Enable instrumentation for thread                      |  |
| ps_setup_reload_saved()               | Reload saved Performance Schema configuration          |  |
| ps_setup_reset_to_default()           | Reset saved Performance Schema configuration           |  |
| ps_setup_save()                       | Save Performance Schema configuration                  |  |
| ps_setup_show_disabled()              | Display disabled Performance Schema<br>configuration   |  |
| ps_setup_show_disabled_consumers()    | Display disabled Performance Schema consumers          |  |
| ps_setup_show_disabled_instruments()  | Display disabled Performance Schema<br>instruments     |  |
| ps_setup_show_enabled()               | Display enabled Performance Schema<br>configuration    |  |
| ps_setup_show_enabled_consumers()     | Display enabled Performance Schema consumers           |  |
| ps_setup_show_enabled_instruments()   | Display enabled Performance Schema<br>instruments      |  |
| ps_statement_avg_latency_histogram()  | Display statement latency histogram                    |  |
| ps_trace_statement_digest()           | Trace Performance Schema instrumentation for<br>digest |  |
| ps_trace_thread()                     | Dump Performance Schema data for thread                |  |

| Procedure Name                   | Description                                |
|----------------------------------|--------------------------------------------|
| ps_truncate_all_tables()         | Truncate Performance Schema summary tables |
| statement_performance_analyzer() | Report of statements running on server     |
| table_exists()                   | Whether a table exists                     |

### **Table 30.4 sys Schema Stored Functions**

| Function Name                                                    | Description                                                                | Deprecated |
|------------------------------------------------------------------|----------------------------------------------------------------------------|------------|
| extract_schema_from_file_name() Extract schema name part of file | name                                                                       |            |
| extract_table_from_file_name() Extract table name part of file   | name                                                                       |            |
| format_bytes()                                                   | Convert byte count to value with<br>units                                  | Yes        |
| format_path()                                                    | Replace directories in path name<br>with symbolic system variable<br>names |            |
| format_statement()                                               | Truncate long statement to fixed<br>length                                 |            |
| format_time()                                                    | Convert picoseconds time to<br>value with units                            | Yes        |
| list_add()                                                       | Add item to list                                                           |            |
| list_drop()                                                      | Remove item from list                                                      |            |
| ps_is_account_enabled()                                          | Whether Performance Schema<br>instrumentation for account is<br>enabled    |            |
| ps_is_consumer_enabled()                                         | Whether Performance Schema<br>consumer is enabled                          |            |
| ps_is_instrument_default_enabled()                               | Whether Performance Schema<br>instrument is enabled by default             |            |
| ps_is_instrument_default_timed() Whether Performance Schema      | instrument is timed by default                                             |            |
| ps_is_thread_instrumented()Whether Performance Schema            | instrumentation for connection ID<br>is enabled                            |            |
| ps_thread_account()                                              | Account associated with<br>Performance Schema thread ID                    |            |
| ps_thread_id()                                                   | Performance Schema thread ID<br>associated with connection ID              | Yes        |
| ps_thread_stack()                                                | Event information for connection<br>ID                                     |            |
| ps_thread_trx_info()                                             | Transaction information for<br>thread ID                                   |            |
| quote_identifier()                                               | Quote string as identifier                                                 |            |
| sys_get_config()                                                 | sys schema configuration option<br>value                                   |            |
| version_major()                                                  | MySQL server major version<br>number                                       |            |

| Function Name   | Description                                  | Deprecated |
|-----------------|----------------------------------------------|------------|
| version_minor() | MySQL server minor version<br>number         |            |
| version_patch() | MySQL server patch release<br>version number |            |

# <span id="page-148-0"></span>**30.4.2 sys Schema Tables and Triggers**

The following sections describe [sys](#page-140-1) schema tables and triggers.

### <span id="page-148-1"></span>**30.4.2.1 The sys\_config Table**

This table contains [sys](#page-140-1) schema configuration options, one row per option. Configuration changes made by updating this table persist across client sessions and server restarts.

The [sys\\_config](#page-148-1) table has these columns:

• variable

The configuration option name.

• value

The configuration option value.

• set\_time

The timestamp of the most recent modification to the row.

• set\_by

The account that made the most recent modification to the row. The value is NULL if the row has not been changed since the [sys](#page-140-1) schema was installed.

As an efficiency measure to minimize the number of direct reads from the [sys\\_config](#page-148-1) table, [sys](#page-140-1) schema functions that use a value from this table check for a user-defined variable with a corresponding name, which is the user-defined variable having the same name plus a @sys. prefix. (For example, the variable corresponding to the diagnostics.include\_raw option is @sys.diagnostics.include\_raw.) If the user-defined variable exists in the current session and is non-NULL, the function uses its value in preference to the value in the [sys\\_config](#page-148-1) table. Otherwise, the function reads and uses the value from the table. In the latter case, the calling function conventionally also sets the corresponding user-defined variable to the table value so that further references to the configuration option within the same session use the variable and need not read the table again.

For example, the statement\_truncate\_len option controls the maximum length of statements returned by the format\_statement() function. The default is 64. To temporarily change the value to 32 for your current session, set the corresponding @sys.statement\_truncate\_len user-defined variable:

```
mysql> SET @stmt = 'SELECT variable, value, set_time, set_by FROM sys_config';
mysql> SELECT sys.format_statement(@stmt);
+----------------------------------------------------------+
| sys.format_statement(@stmt) |
+----------------------------------------------------------+
| SELECT variable, value, set_time, set_by FROM sys_config |
+----------------------------------------------------------+
mysql> SET @sys.statement_truncate_len = 32;
mysql> SELECT sys.format_statement(@stmt);
+-----------------------------------+
| sys.format_statement(@stmt) |
+-----------------------------------+
```

```
| SELECT variabl ... ROM sys_config |
+-----------------------------------+
```

Subsequent invocations of format\_statement() within the session continue to use the user-defined variable value (32), rather than the value stored in the table (64).

To stop using the user-defined variable and revert to using the value in the table, set the variable to NULL within your session:

```
mysql> SET @sys.statement_truncate_len = NULL;
mysql> SELECT sys.format_statement(@stmt);
+----------------------------------------------------------+
| sys.format_statement(@stmt) |
+----------------------------------------------------------+
| SELECT variable, value, set_time, set_by FROM sys_config |
+----------------------------------------------------------+
```

Alternatively, end your current session (causing the user-defined variable to no longer exist) and begin a new session.

The conventional relationship just described between options in the [sys\\_config](#page-148-1) table and userdefined variables can be exploited to make temporary configuration changes that end when your session ends. However, if you set a user-defined variable and then subsequently change the corresponding table value within the same session, the changed table value is not used in that session as long as the user-defined variable exists with a non-NULL value. (The changed table value is used in other sessions in which the user-defined variable is not assigned.)

The following list describes the options in the [sys\\_config](#page-148-1) table and the corresponding user-defined variables:

• diagnostics.allow\_i\_s\_tables, @sys.diagnostics.allow\_i\_s\_tables

If this option is ON, the [diagnostics\(\)](#page-191-0) procedure is permitted to perform table scans on the Information Schema TABLES table. This can be expensive if there are many tables. The default is OFF.

• diagnostics.include\_raw, @sys.diagnostics.include\_raw

If this option is ON, the [diagnostics\(\)](#page-191-0) procedure includes the raw output from querying the [metrics](#page-165-1) view. The default is OFF.

• ps\_thread\_trx\_info.max\_length, @sys.ps\_thread\_trx\_info.max\_length

The maximum length for JSON output produced by the ps\_thread\_trx\_info() function. The default is 65535.

• statement\_performance\_analyzer.limit, @sys.statement\_performance\_analyzer.limit

The maximum number of rows to return for views that have no built-in limit. (For example, the [statements\\_with\\_runtimes\\_in\\_95th\\_percentile](#page-181-0) view has a built-in limit in the sense that it returns only statements with average execution time in the 95th percentile.) The default is 100.

• statement\_performance\_analyzer.view, @sys.statement\_performance\_analyzer.view

The custom query or view to be used by the statement\_performance\_analyzer() procedure (which is itself invoked by the [diagnostics\(\)](#page-191-0) procedure). If the option value contains a space, it is interpreted as a query. Otherwise, it must be the name of an existing view that queries the Performance Schema [events\\_statements\\_summary\\_by\\_digest](#page-65-0) table. There cannot be any LIMIT clause in the query or view definition if the statement\_performance\_analyzer.limit configuration option is greater than 0. The default is NULL (no custom view defined).

• statement\_truncate\_len, @sys.statement\_truncate\_len

The maximum length of statements returned by the format\_statement() function. Longer statements are truncated to this length. The default is 64.

Other options can be added to the [sys\\_config](#page-148-1) table. For example, the [diagnostics\(\)](#page-191-0) and [execute\\_prepared\\_stmt\(\)](#page-193-0) procedures use the debug option if it exists, but this option is not part of the [sys\\_config](#page-148-1) table by default because debug output normally is enabled only temporarily, by setting the corresponding @sys.debug user-defined variable. To enable debug output without having to set that variable in individual sessions, add the option to the table:

```
mysql> INSERT INTO sys.sys_config (variable, value) VALUES('debug', 'ON');
```

To change the debug setting in the table, do two things. First, modify the value in the table itself:

```
mysql> UPDATE sys.sys_config
 SET value = 'OFF'
 WHERE variable = 'debug';
```

Second, to also ensure that procedure invocations within the current session use the changed value from the table, set the corresponding user-defined variable to NULL:

```
mysql> SET @sys.debug = NULL;
```

## <span id="page-150-1"></span>**30.4.2.2 The sys\_config\_insert\_set\_user Trigger**

For rows added to the [sys\\_config](#page-148-1) table by INSERT statements, the [sys\\_config\\_insert\\_set\\_user](#page-150-1) trigger sets the set\_by column to the current user.

## <span id="page-150-2"></span>**30.4.2.3 The sys\_config\_update\_set\_user Trigger**

The [sys\\_config\\_update\\_set\\_user](#page-150-2) trigger for the [sys\\_config](#page-148-1) table is similar to the [sys\\_config\\_insert\\_set\\_user](#page-150-1) trigger, but for UPDATE statements.

# <span id="page-150-0"></span>**30.4.3 sys Schema Views**

The following sections describe [sys](#page-140-1) schema views.

The sys schema contains many views that summarize Performance Schema tables in various ways. Most of these views come in pairs, such that one member of the pair has the same name as the other member, plus a x\$ prefix. For example, the [host\\_summary\\_by\\_file\\_io](#page-152-0) view summarizes file I/ O grouped by host and displays latencies converted from picoseconds to more readable values (with units);

```
mysql> SELECT * FROM sys.host_summary_by_file_io;
+------------+-------+------------+
| host | ios | io_latency |
+------------+-------+------------+
| localhost | 67570 | 5.38 s |
| background | 3468 | 4.18 s |
+------------+-------+------------+
```

The [x\\$host\\_summary\\_by\\_file\\_io](#page-152-0) view summarizes the same data but displays unformatted picosecond latencies:

```
mysql> SELECT * FROM sys.x$host_summary_by_file_io;
+------------+-------+---------------+
| host | ios | io_latency |
+------------+-------+---------------+
| localhost | 67574 | 5380678125144 |
| background | 3474 | 4758696829416 |
+------------+-------+---------------+
```

The view without the x\$ prefix is intended to provide output that is more user friendly and easier to read. The view with the x\$ prefix that displays the same values in raw form is intended more for use with other tools that perform their own processing on the data.

Views without the x\$ prefix differ from the corresponding x\$ views in these ways:

- Byte counts are formatted with size units using format\_bytes().
- Time values are formatted with temporal units using format\_time().
- SQL statements are truncated to a maximum display width using format\_statement().
- Path name are shortened using format\_path().

## <span id="page-151-0"></span>**30.4.3.1 The host\_summary and x\$host\_summary Views**

These views summarize statement activity, file I/O, and connections, grouped by host.

The [host\\_summary](#page-151-0) and [x\\$host\\_summary](#page-151-0) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• statements

The total number of statements for the host.

• statement\_latency

The total wait time of timed statements for the host.

• statement\_avg\_latency

The average wait time per timed statement for the host.

• table\_scans

The total number of table scans for the host.

• file\_ios

The total number of file I/O events for the host.

• file\_io\_latency

The total wait time of timed file I/O events for the host.

• current\_connections

The current number of connections for the host.

• total\_connections

The total number of connections for the host.

• unique\_users

The number of distinct users for the host.

• current\_memory

The current amount of allocated memory for the host.

• total\_memory\_allocated

The total amount of allocated memory for the host.

# <span id="page-152-0"></span>**30.4.3.2 The host\_summary\_by\_file\_io and x\$host\_summary\_by\_file\_io Views**

These views summarize file I/O, grouped by host. By default, rows are sorted by descending total file I/ O latency.

The [host\\_summary\\_by\\_file\\_io](#page-152-0) and [x\\$host\\_summary\\_by\\_file\\_io](#page-152-0) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• ios

The total number of file I/O events for the host.

• io\_latency

The total wait time of timed file I/O events for the host.

# <span id="page-152-1"></span>**30.4.3.3 The host\_summary\_by\_file\_io\_type and x\$host\_summary\_by\_file\_io\_type Views**

These views summarize file I/O, grouped by host and event type. By default, rows are sorted by host and descending total I/O latency.

The [host\\_summary\\_by\\_file\\_io\\_type](#page-152-1) and [x\\$host\\_summary\\_by\\_file\\_io\\_type](#page-152-1) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• event\_name

The file I/O event name.

• total

The total number of occurrences of the file I/O event for the host.

• total\_latency

The total wait time of timed occurrences of the file I/O event for the host.

• max\_latency

The maximum single wait time of timed occurrences of the file I/O event for the host.

### <span id="page-152-2"></span>**30.4.3.4 The host\_summary\_by\_stages and x\$host\_summary\_by\_stages Views**

These views summarize statement stages, grouped by host. By default, rows are sorted by host and descending total latency.

The [host\\_summary\\_by\\_stages](#page-152-2) and [x\\$host\\_summary\\_by\\_stages](#page-152-2) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• event\_name

The stage event name.

• total

The total number of occurrences of the stage event for the host.

• total\_latency

The total wait time of timed occurrences of the stage event for the host.

• avg\_latency

The average wait time per timed occurrence of the stage event for the host.

# <span id="page-153-0"></span>**30.4.3.5 The host\_summary\_by\_statement\_latency and x \$host\_summary\_by\_statement\_latency Views**

These views summarize overall statement statistics, grouped by host. By default, rows are sorted by descending total latency.

The [host\\_summary\\_by\\_statement\\_latency](#page-153-0) and [x\\$host\\_summary\\_by\\_statement\\_latency](#page-153-0) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• total

The total number of statements for the host.

• total\_latency

The total wait time of timed statements for the host.

• max\_latency

The maximum single wait time of timed statements for the host.

• lock\_latency

The total time waiting for locks by timed statements for the host.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_sent

The total number of rows returned by statements for the host.

• rows\_examined

The total number of rows read from storage engines by statements for the host.

• rows\_affected

The total number of rows affected by statements for the host.

• full\_scans

The total number of full table scans by statements for the host.

# <span id="page-154-0"></span>**30.4.3.6 The host\_summary\_by\_statement\_type and x \$host\_summary\_by\_statement\_type Views**

These views summarize information about statements executed, grouped by host and statement type. By default, rows are sorted by host and descending total latency.

The [host\\_summary\\_by\\_statement\\_type](#page-154-0) and [x\\$host\\_summary\\_by\\_statement\\_type](#page-154-0) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• statement

The final component of the statement event name.

• total

The total number of occurrences of the statement event for the host.

• total\_latency

The total wait time of timed occurrences of the statement event for the host.

• max\_latency

The maximum single wait time of timed occurrences of the statement event for the host.

• lock\_latency

The total time waiting for locks by timed occurrences of the statement event for the host.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_sent

The total number of rows returned by occurrences of the statement event for the host.

• rows\_examined

The total number of rows read from storage engines by occurrences of the statement event for the host.

• rows\_affected

The total number of rows affected by occurrences of the statement event for the host.

• full\_scans

The total number of full table scans by occurrences of the statement event for the host.

# <span id="page-155-0"></span>**30.4.3.7 The innodb\_buffer\_stats\_by\_schema and x\$innodb\_buffer\_stats\_by\_schema Views**

These views summarize the information in the INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE table, grouped by schema. By default, rows are sorted by descending buffer size.

![](_page_155_Picture_3.jpeg)

#### **Warning**

Querying views that access the INNODB\_BUFFER\_PAGE table can affect performance. Do not query these views on a production system unless you are aware of the performance impact and have determined it to be acceptable. To avoid impacting performance on a production system, reproduce the issue you want to investigate and query buffer pool statistics on a test instance.

The [innodb\\_buffer\\_stats\\_by\\_schema](#page-155-0) and [x\\$innodb\\_buffer\\_stats\\_by\\_schema](#page-155-0) views have these columns:

• object\_schema

The schema name for the object, or InnoDB System if the table belongs to the InnoDB storage engine.

• allocated

The total number of bytes allocated for the schema.

• data

The total number of data bytes allocated for the schema.

• pages

The total number of pages allocated for the schema.

• pages\_hashed

The total number of hashed pages allocated for the schema.

• pages\_old

The total number of old pages allocated for the schema.

• rows\_cached

The total number of cached rows for the schema.

### <span id="page-155-1"></span>**30.4.3.8 The innodb\_buffer\_stats\_by\_table and x\$innodb\_buffer\_stats\_by\_table Views**

These views summarize the information in the INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE table, grouped by schema and table. By default, rows are sorted by descending buffer size.

![](_page_155_Picture_23.jpeg)

#### **Warning**

Querying views that access the INNODB\_BUFFER\_PAGE table can affect performance. Do not query these views on a production system unless you are aware of the performance impact and have determined it to be acceptable. To avoid impacting performance on a production system, reproduce the issue you want to investigate and query buffer pool statistics on a test instance.

The [innodb\\_buffer\\_stats\\_by\\_table](#page-155-1) and [x\\$innodb\\_buffer\\_stats\\_by\\_table](#page-155-1) views have these columns:

• object\_schema

The schema name for the object, or InnoDB System if the table belongs to the InnoDB storage engine.

• object\_name

The table name.

• allocated

The total number of bytes allocated for the table.

• data

The number of data bytes allocated for the table.

• pages

The total number of pages allocated for the table.

• pages\_hashed

The number of hashed pages allocated for the table.

• pages\_old

The number of old pages allocated for the table.

• rows\_cached

The number of cached rows for the table.

## <span id="page-156-0"></span>**30.4.3.9 The innodb\_lock\_waits and x\$innodb\_lock\_waits Views**

These views summarize the InnoDB locks that transactions are waiting for. By default, rows are sorted by descending lock age.

The [innodb\\_lock\\_waits](#page-156-0) and [x\\$innodb\\_lock\\_waits](#page-156-0) views have these columns:

• wait\_started

The time at which the lock wait started.

• wait\_age

How long the lock has been waited for, as a TIME value.

• wait\_age\_secs

How long the lock has been waited for, in seconds.

• locked\_table\_schema

The schema that contains the locked table.

• locked\_table\_name

The name of the locked table.

• locked\_table\_partition

The name of the locked partition, if any; NULL otherwise.

• locked\_table\_subpartition

The name of the locked subpartition, if any; NULL otherwise.

• locked\_index

The name of the locked index.

• locked\_type

The type of the waiting lock.

• waiting\_trx\_id

The ID of the waiting transaction.

• waiting\_trx\_started

The time at which the waiting transaction started.

• waiting\_trx\_age

How long the waiting transaction has been waiting, as a TIME value.

• waiting\_trx\_rows\_locked

The number of rows locked by the waiting transaction.

• waiting\_trx\_rows\_modified

The number of rows modified by the waiting transaction.

• waiting\_pid

The processlist ID of the waiting transaction.

• waiting\_query

The statement that is waiting for the lock.

• waiting\_lock\_id

The ID of the waiting lock.

• waiting\_lock\_mode

The mode of the waiting lock.

• blocking\_trx\_id

The ID of the transaction that is blocking the waiting lock.

• blocking\_pid

The processlist ID of the blocking transaction.

• blocking\_query

The statement the blocking transaction is executing. This field reports NULL if the session that issued the blocking query becomes idle. For more information, see Identifying a Blocking Query After the Issuing Session Becomes Idle.

• blocking\_lock\_id

The ID of the lock that is blocking the waiting lock.

• blocking\_lock\_mode

The mode of the lock that is blocking the waiting lock.

• blocking\_trx\_started

The time at which the blocking transaction started.

• blocking\_trx\_age

How long the blocking transaction has been executing, as a TIME value.

• blocking\_trx\_rows\_locked

The number of rows locked by the blocking transaction.

• blocking\_trx\_rows\_modified

The number of rows modified by the blocking transaction.

• sql\_kill\_blocking\_query

The KILL statement to execute to kill the blocking statement.

• sql\_kill\_blocking\_connection

The KILL statement to execute to kill the session running the blocking statement.

### <span id="page-158-0"></span>**30.4.3.10 The io\_by\_thread\_by\_latency and x\$io\_by\_thread\_by\_latency Views**

These views summarize I/O consumers to display time waiting for I/O, grouped by thread. By default, rows are sorted by descending total I/O latency.

The [io\\_by\\_thread\\_by\\_latency](#page-158-0) and [x\\$io\\_by\\_thread\\_by\\_latency](#page-158-0) views have these columns:

• user

For foreground threads, the account associated with the thread. For background threads, the thread name.

• total

The total number of I/O events for the thread.

• total\_latency

The total wait time of timed I/O events for the thread.

• min\_latency

The minimum single wait time of timed I/O events for the thread.

• avg\_latency

The average wait time per timed I/O event for the thread.

• max\_latency

The maximum single wait time of timed I/O events for the thread.

• thread\_id

The thread ID.

• processlist\_id

For foreground threads, the processlist ID of the thread. For background threads, NULL.

## <span id="page-159-0"></span>**30.4.3.11 The io\_global\_by\_file\_by\_bytes and x\$io\_global\_by\_file\_by\_bytes Views**

These views summarize global I/O consumers to display amount of I/O, grouped by file. By default, rows are sorted by descending total I/O (bytes read and written).

The [io\\_global\\_by\\_file\\_by\\_bytes](#page-159-0) and [x\\$io\\_global\\_by\\_file\\_by\\_bytes](#page-159-0) views have these columns:

• file

The file path name.

• count\_read

The total number of read events for the file.

• total\_read

The total number of bytes read from the file.

• avg\_read

The average number of bytes per read from the file.

• count\_write

The total number of write events for the file.

• total\_written

The total number of bytes written to the file.

• avg\_write

The average number of bytes per write to the file.

• total

The total number of bytes read and written for the file.

• write\_pct

The percentage of total bytes of I/O that were writes.

## <span id="page-159-1"></span>**30.4.3.12 The io\_global\_by\_file\_by\_latency and x\$io\_global\_by\_file\_by\_latency Views**

These views summarize global I/O consumers to display time waiting for I/O, grouped by file. By default, rows are sorted by descending total latency.

The [io\\_global\\_by\\_file\\_by\\_latency](#page-159-1) and [x\\$io\\_global\\_by\\_file\\_by\\_latency](#page-159-1) views have these columns:

• file

The file path name.

• total

The total number of I/O events for the file.

• total\_latency

The total wait time of timed I/O events for the file.

• count\_read

The total number of read I/O events for the file.

• read\_latency

The total wait time of timed read I/O events for the file.

• count\_write

The total number of write I/O events for the file.

• write\_latency

The total wait time of timed write I/O events for the file.

• count\_misc

The total number of other I/O events for the file.

• misc\_latency

The total wait time of timed other I/O events for the file.

### <span id="page-160-0"></span>**30.4.3.13 The io\_global\_by\_wait\_by\_bytes and x\$io\_global\_by\_wait\_by\_bytes Views**

These views summarize global I/O consumers to display amount of I/O and time waiting for I/O, grouped by event. By default, rows are sorted by descending total I/O (bytes read and written).

The [io\\_global\\_by\\_wait\\_by\\_bytes](#page-160-0) and [x\\$io\\_global\\_by\\_wait\\_by\\_bytes](#page-160-0) views have these columns:

• event\_name

The I/O event name, with the wait/io/file/ prefix stripped.

• total

The total number of occurrences of the I/O event.

• total\_latency

The total wait time of timed occurrences of the I/O event.

• min\_latency

The minimum single wait time of timed occurrences of the I/O event.

• avg\_latency

The average wait time per timed occurrence of the I/O event.

• max\_latency

The maximum single wait time of timed occurrences of the I/O event.

• count\_read

The number of read requests for the I/O event.

• total\_read

The number of bytes read for the I/O event.

• avg\_read

The average number of bytes per read for the I/O event.

• count\_write

The number of write requests for the I/O event.

• total\_written

The number of bytes written for the I/O event.

• avg\_written

The average number of bytes per write for the I/O event.

• total\_requested

The total number of bytes read and written for the I/O event.

## <span id="page-161-0"></span>**30.4.3.14 The io\_global\_by\_wait\_by\_latency and x\$io\_global\_by\_wait\_by\_latency Views**

These views summarize global I/O consumers to display amount of I/O and time waiting for I/O, grouped by event. By default, rows are sorted by descending total latency.

The [io\\_global\\_by\\_wait\\_by\\_latency](#page-161-0) and [x\\$io\\_global\\_by\\_wait\\_by\\_latency](#page-161-0) views have these columns:

• event\_name

The I/O event name, with the wait/io/file/ prefix stripped.

• total

The total number of occurrences of the I/O event.

• total\_latency

The total wait time of timed occurrences of the I/O event.

• avg\_latency

The average wait time per timed occurrence of the I/O event.

• max\_latency

The maximum single wait time of timed occurrences of the I/O event.

• read\_latency

The total wait time of timed read occurrences of the I/O event.

• write\_latency

The total wait time of timed write occurrences of the I/O event.

• misc\_latency

The total wait time of timed other occurrences of the I/O event.

• count\_read

The number of read requests for the I/O event.

• total\_read

The number of bytes read for the I/O event.

• avg\_read

The average number of bytes per read for the I/O event.

• count\_write

The number of write requests for the I/O event.

• total\_written

The number of bytes written for the I/O event.

• avg\_written

The average number of bytes per write for the I/O event.

## <span id="page-162-0"></span>**30.4.3.15 The latest\_file\_io and x\$latest\_file\_io Views**

These views summarize file I/O activity, grouped by file and thread. By default, rows are sorted with most recent I/O first.

The [latest\\_file\\_io](#page-162-0) and [x\\$latest\\_file\\_io](#page-162-0) views have these columns:

• thread

For foreground threads, the account associated with the thread (and port number for TCP/IP connections). For background threads, the thread name and thread ID

• file

The file path name.

• latency

The wait time of the file I/O event.

• operation

The type of operation.

• requested

The number of data bytes requested for the file I/O event.

# <span id="page-162-1"></span>**30.4.3.16 The memory\_by\_host\_by\_current\_bytes and x \$memory\_by\_host\_by\_current\_bytes Views**

These views summarize memory use, grouped by host. By default, rows are sorted by descending amount of memory used.

The [memory\\_by\\_host\\_by\\_current\\_bytes](#page-162-1) and [x\\$memory\\_by\\_host\\_by\\_current\\_bytes](#page-162-1) views have these columns:

• host

The host from which the client connected. Rows for which the HOST column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• current\_count\_used

The current number of allocated memory blocks that have not been freed yet for the host.

• current\_allocated

The current number of allocated bytes that have not been freed yet for the host.

• current\_avg\_alloc

The current number of allocated bytes per memory block for the host.

• current\_max\_alloc

The largest single current memory allocation in bytes for the host.

• total\_allocated

The total memory allocation in bytes for the host.

# <span id="page-163-0"></span>**30.4.3.17 The memory\_by\_thread\_by\_current\_bytes and x \$memory\_by\_thread\_by\_current\_bytes Views**

These views summarize memory use, grouped by thread. By default, rows are sorted by descending amount of memory used.

The [memory\\_by\\_thread\\_by\\_current\\_bytes](#page-163-0) and [x\\$memory\\_by\\_thread\\_by\\_current\\_bytes](#page-163-0) views have these columns:

• thread\_id

The thread ID.

• user

The thread user or thread name.

• current\_count\_used

The current number of allocated memory blocks that have not been freed yet for the thread.

• current\_allocated

The current number of allocated bytes that have not been freed yet for the thread.

• current\_avg\_alloc

The current number of allocated bytes per memory block for the thread.

• current\_max\_alloc

The largest single current memory allocation in bytes for the thread.

• total\_allocated

The total memory allocation in bytes for the thread.

# <span id="page-163-1"></span>**30.4.3.18 The memory\_by\_user\_by\_current\_bytes and x \$memory\_by\_user\_by\_current\_bytes Views**

These views summarize memory use, grouped by user. By default, rows are sorted by descending amount of memory used.

The [memory\\_by\\_user\\_by\\_current\\_bytes](#page-163-1) and [x\\$memory\\_by\\_user\\_by\\_current\\_bytes](#page-163-1) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• current\_count\_used

The current number of allocated memory blocks that have not been freed yet for the user.

• current\_allocated

The current number of allocated bytes that have not been freed yet for the user.

• current\_avg\_alloc

The current number of allocated bytes per memory block for the user.

• current\_max\_alloc

The largest single current memory allocation in bytes for the user.

• total\_allocated

The total memory allocation in bytes for the user.

# <span id="page-164-0"></span>**30.4.3.19 The memory\_global\_by\_current\_bytes and x \$memory\_global\_by\_current\_bytes Views**

These views summarize memory use, grouped by allocation type (that is, by event). By default, rows are sorted by descending amount of memory used.

The [memory\\_global\\_by\\_current\\_bytes](#page-164-0) and [x\\$memory\\_global\\_by\\_current\\_bytes](#page-164-0) views have these columns:

• event\_name

The memory event name.

• current\_count

The total number of occurrences of the event.

• current\_alloc

The current number of allocated bytes that have not been freed yet for the event.

• current\_avg\_alloc

The current number of allocated bytes per memory block for the event.

• high\_count

The high-water mark for number of memory blocks allocated for the event.

• high\_alloc

The high-water mark for number of bytes allocated for the event.

• high\_avg\_alloc

The high-water mark for average number of bytes per memory block allocated for the event.

### <span id="page-165-0"></span>**30.4.3.20 The memory\_global\_total and x\$memory\_global\_total Views**

These views summarize total memory use within the server.

The [memory\\_global\\_total](#page-165-0) and [x\\$memory\\_global\\_total](#page-165-0) views have these columns:

• total\_allocated

The total bytes of memory allocated within the server.

## <span id="page-165-1"></span>**30.4.3.21 The metrics View**

This view summarizes MySQL server metrics to show variable names, values, types, and whether they are enabled. By default, rows are sorted by variable type and name.

The [metrics](#page-165-1) view includes this information:

- Global status variables from the Performance Schema [global\\_status](#page-47-0) table
- InnoDB metrics from the INFORMATION\_SCHEMA INNODB\_METRICS table
- Current and total memory allocation, based on the Performance Schema memory instrumentation
- The current time (human readable and Unix timestamp formats)

There is some duplication of information between the [global\\_status](#page-47-0) and INNODB\_METRICS tables, which the [metrics](#page-165-1) view eliminates.

The [metrics](#page-165-1) view has these columns:

• Variable\_name

The metric name. The metric type determines the source from which the name is taken:

- For global status variables: The VARIABLE\_NAME column of the [global\\_status](#page-47-0) table
- For InnoDB metrics: The NAME column of the INNODB\_METRICS table
- For other metrics: A view-provided descriptive string
- Variable\_value

The metric value. The metric type determines the source from which the value is taken:

- For global status variables: The VARIABLE\_VALUE column of the [global\\_status](#page-47-0) table
- For InnoDB metrics: The COUNT column of the INNODB\_METRICS table
- For memory metrics: The relevant column from the Performance Schema [memory\\_summary\\_global\\_by\\_event\\_name](#page-80-0) table
- For the current time: The value of NOW(3) or UNIX\_TIMESTAMP(NOW(3))
- Type

The metric type:

- For global status variables: Global Status
- For InnoDB metrics: InnoDB Metrics %, where % is replaced by the value of the SUBSYSTEM column of the INNODB\_METRICS table
- For memory metrics: Performance Schema
- For the current time: System Time
- Enabled

Whether the metric is enabled:

- For global status variables: YES
- For InnoDB metrics: YES if the STATUS column of the INNODB\_METRICS table is enabled, NO otherwise
- For memory metrics: NO, YES, or PARTIAL (currently, PARTIAL occurs only for memory metrics and indicates that not all memory/% instruments are enabled; Performance Schema memory instruments are always enabled)
- For the current time: YES

### <span id="page-166-0"></span>**30.4.3.22 The processlist and x\$processlist Views**

The MySQL process list indicates the operations currently being performed by the set of threads executing within the server. The [processlist](#page-166-0) and [x\\$processlist](#page-166-0) views summarize process information. They provide more complete information than the SHOW PROCESSLIST statement and the INFORMATION\_SCHEMA PROCESSLIST table, and are also nonblocking. By default, rows are sorted by descending process time and descending wait time. For a comparison of process information sources, see Sources of Process Information.

The column descriptions here are brief. For additional information, see the description of the Performance Schema [threads](#page-99-0) table at [Section 29.12.21.8, "The threads Table".](#page-99-0)

The [processlist](#page-166-0) and [x\\$processlist](#page-166-0) views have these columns:

• thd\_id

The thread ID.

• conn\_id

The connection ID.

• user

The thread user or thread name.

• db

The default database for the thread, or NULL if there is none.

• command

For foreground threads, the type of command the thread is executing on behalf of the client, or Sleep if the session is idle.

• state

An action, event, or state that indicates what the thread is doing.

• time

The time in seconds that the thread has been in its current state.

• current\_statement

The statement the thread is executing, or NULL if it is not executing any statement.

• execution\_engine

The query execution engine. The value is either PRIMARY or SECONDARY. For use with MySQL HeatWave Service and MySQL HeatWave, where the PRIMARY engine is InnoDB and SECONDARY engine is MySQL HeatWave (RAPID). For MySQL Community Edition Server, MySQL Enterprise Edition Server (on-premise), and MySQL HeatWave Service without MySQL HeatWave, the value is always PRIMARY. This column was added in MySQL 8.0.29.

• statement\_latency

How long the statement has been executing.

• progress

The percentage of work completed for stages that support progress reporting. See [Section 30.3, "sys](#page-142-0) [Schema Progress Reporting".](#page-142-0)

• lock\_latency

The time spent waiting for locks by the current statement.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_examined

The number of rows read from storage engines by the current statement.

• rows\_sent

The number of rows returned by the current statement.

• rows\_affected

The number of rows affected by the current statement.

• tmp\_tables

The number of internal in-memory temporary tables created by the current statement.

• tmp\_disk\_tables

The number of internal on-disk temporary tables created by the current statement.

• full\_scan

The number of full table scans performed by the current statement.

• last\_statement

The last statement executed by the thread, if there is no currently executing statement or wait.

• last\_statement\_latency

How long the last statement executed.

• current\_memory

The number of bytes allocated by the thread.

• last\_wait

The name of the most recent wait event for the thread.

• last\_wait\_latency

The wait time of the most recent wait event for the thread.

• source

The source file and line number containing the instrumented code that produced the event.

• trx\_latency

The wait time of the current transaction for the thread.

• trx\_state

The state for the current transaction for the thread.

• trx\_autocommit

Whether autocommit mode was enabled when the current transaction started.

• pid

The client process ID.

• program\_name

The client program name.

# <span id="page-168-0"></span>**30.4.3.23 The ps\_check\_lost\_instrumentation View**

This view returns information about lost Performance Schema instruments, to indicate whether the Performance Schema is unable to monitor all runtime data.

The [ps\\_check\\_lost\\_instrumentation](#page-168-0) view has these columns:

• variable\_name

The Performance Schema status variable name indicating which type of instrument was lost.

• variable\_value

The number of instruments lost.

## <span id="page-168-1"></span>**30.4.3.24 The schema\_auto\_increment\_columns View**

This view indicates which tables have AUTO\_INCREMENT columns and provides information about those columns, such as the current and maximum column values and the usage ratio (ratio of used to possible values). By default, rows are sorted by descending usage ratio and maximum column value.

Tables in these schemas are excluded from view output: mysql, sys, INFORMATION\_SCHEMA, performance\_schema.

The [schema\\_auto\\_increment\\_columns](#page-168-1) view has these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table that contains the AUTO\_INCREMENT column.

• column\_name

The name of the AUTO\_INCREMENT column.

• data\_type

The data type of the column.

• column\_type

The column type of the column, which is the data type plus possibly other information. For example, for a column with a bigint(20) unsigned column type, the data type is just bigint.

• is\_signed

Whether the column type is signed.

• is\_unsigned

Whether the column type is unsigned.

• max\_value

The maximum permitted value for the column.

• auto\_increment

The current AUTO\_INCREMENT value for the column.

• auto\_increment\_ratio

The ratio of used to permitted values for the column. This indicates how much of the sequence of values is "used up."

### <span id="page-169-0"></span>**30.4.3.25 The schema\_index\_statistics and x\$schema\_index\_statistics Views**

These views provide index statistics. By default, rows are sorted by descending total index latency.

The [schema\\_index\\_statistics](#page-169-0) and [x\\$schema\\_index\\_statistics](#page-169-0) views have these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table that contains the index.

• index\_name

The name of the index.

• rows\_selected

The total number of rows read using the index.

• select\_latency

The total wait time of timed reads using the index.

• rows\_inserted

The total number of rows inserted into the index.

• insert\_latency

The total wait time of timed inserts into the index.

• rows\_updated

The total number of rows updated in the index.

• update\_latency

The total wait time of timed updates in the index.

• rows\_deleted

The total number of rows deleted from the index.

• delete\_latency

The total wait time of timed deletes from the index.

## <span id="page-170-0"></span>**30.4.3.26 The schema\_object\_overview View**

This view summarizes the types of objects within each schema. By default, rows are sorted by schema and object type.

![](_page_170_Picture_16.jpeg)

### **Note**

For MySQL instances with a large number of objects, this view might take a long time to execute.

The [schema\\_object\\_overview](#page-170-0) view has these columns:

• db

The schema name.

• object\_type

The object type: BASE TABLE, INDEX (index\_type), EVENT, FUNCTION, PROCEDURE, TRIGGER, VIEW.

• count

The number of objects in the schema of the given type.

## <span id="page-170-1"></span>**30.4.3.27 The schema\_redundant\_indexes and x\$schema\_flattened\_keys Views**

The [schema\\_redundant\\_indexes](#page-170-1) view displays indexes that duplicate other indexes or are made redundant by them. The [x\\$schema\\_flattened\\_keys](#page-170-1) view is a helper view for [schema\\_redundant\\_indexes](#page-170-1).

In the following column descriptions, the dominant index is the one that makes the redundant index redundant.

The [schema\\_redundant\\_indexes](#page-170-1) view has these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table that contains the index.

• redundant\_index\_name

The name of the redundant index.

• redundant\_index\_columns

The names of the columns in the redundant index.

• redundant\_index\_non\_unique

The number of nonunique columns in the redundant index.

• dominant\_index\_name

The name of the dominant index.

• dominant\_index\_columns

The names of the columns in the dominant index.

• dominant\_index\_non\_unique

The number of nonunique columns in the dominant index.

• subpart\_exists

Whether the index indexes only part of a column.

• sql\_drop\_index

The statement to execute to drop the redundant index.

The [x\\$schema\\_flattened\\_keys](#page-170-1) view has these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table that contains the index.

• index\_name

An index name.

• non\_unique

The number of nonunique columns in the index.

• subpart\_exists

Whether the index indexes only part of a column.

• index\_columns

The name of the columns in the index.

## <span id="page-172-0"></span>**30.4.3.28 The schema\_table\_lock\_waits and x\$schema\_table\_lock\_waits Views**

These views display which sessions are blocked waiting on metadata locks, and what is blocking them.

The column descriptions here are brief. For additional information, see the description of the Performance Schema [metadata\\_locks](#page-39-0) table at [Section 29.12.13.3, "The metadata\\_locks Table"](#page-39-0).

The [schema\\_table\\_lock\\_waits](#page-172-0) and [x\\$schema\\_table\\_lock\\_waits](#page-172-0) views have these columns:

• object\_schema

The schema containing the object to be locked.

• object\_name

The name of the instrumented object.

• waiting\_thread\_id

The thread ID of the thread that is waiting for the lock.

• waiting\_pid

The processlist ID of the thread that is waiting for the lock.

• waiting\_account

The account associated with the session that is waiting for the lock.

• waiting\_lock\_type

The type of the waiting lock.

• waiting\_lock\_duration

How long the waiting lock has been waiting.

• waiting\_query

The statement that is waiting for the lock.

• waiting\_query\_secs

How long the statement has been waiting, in seconds.

• waiting\_query\_rows\_affected

The number of rows affected by the statement.

• waiting\_query\_rows\_examined

The number of rows read from storage engines by the statement.

• blocking\_thread\_id

The thread ID of the thread that is blocking the waiting lock.

• blocking\_pid

The processlist ID of the thread that is blocking the waiting lock.

• blocking\_account

The account associated with the thread that is blocking the waiting lock.

• blocking\_lock\_type

The type of lock that is blocking the waiting lock.

• blocking\_lock\_duration

How long the blocking lock has been held.

• sql\_kill\_blocking\_query

The KILL statement to execute to kill the blocking statement.

• sql\_kill\_blocking\_connection

The KILL statement to execute to kill the session running the blocking statement.

### <span id="page-173-0"></span>**30.4.3.29 The schema\_table\_statistics and x\$schema\_table\_statistics Views**

These views summarize table statistics. By default, rows are sorted by descending total wait time (tables with most contention first).

These views user a helper view, x\$ps\_schema\_table\_statistics\_io.

The [schema\\_table\\_statistics](#page-173-0) and [x\\$schema\\_table\\_statistics](#page-173-0) views have these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table name.

• total\_latency

The total wait time of timed I/O events for the table.

• rows\_fetched

The total number of rows read from the table.

• fetch\_latency

The total wait time of timed read I/O events for the table.

• rows\_inserted

The total number of rows inserted into the table.

• insert\_latency

The total wait time of timed insert I/O events for the table.

• rows\_updated

The total number of rows updated in the table.

• update\_latency

The total wait time of timed update I/O events for the table.

• rows\_deleted

The total number of rows deleted from the table.

• delete\_latency

The total wait time of timed delete I/O events for the table.

• io\_read\_requests

The total number of read requests for the table.

• io\_read

The total number of bytes read from the table.

• io\_read\_latency

The total wait time of reads from the table.

• io\_write\_requests

The total number of write requests for the table.

• io\_write

The total number of bytes written to the table.

• io\_write\_latency

The total wait time of writes to the table.

• io\_misc\_requests

The total number of miscellaneous I/O requests for the table.

• io\_misc\_latency

The total wait time of miscellaneous I/O requests for the table.

# <span id="page-174-0"></span>**30.4.3.30 The schema\_table\_statistics\_with\_buffer and x \$schema\_table\_statistics\_with\_buffer Views**

These views summarize table statistics, including InnoDB buffer pool statistics. By default, rows are sorted by descending total wait time (tables with most contention first).

These views user a helper view, x\$ps\_schema\_table\_statistics\_io.

The [schema\\_table\\_statistics\\_with\\_buffer](#page-174-0) and [x](#page-174-0) [\\$schema\\_table\\_statistics\\_with\\_buffer](#page-174-0) views have these columns:

• table\_schema

The schema that contains the table.

• table\_name

The table name.

• rows\_fetched

The total number of rows read from the table.

• fetch\_latency

The total wait time of timed read I/O events for the table.

• rows\_inserted

The total number of rows inserted into the table.

• insert\_latency

The total wait time of timed insert I/O events for the table.

• rows\_updated

The total number of rows updated in the table.

• update\_latency

The total wait time of timed update I/O events for the table.

• rows\_deleted

The total number of rows deleted from the table.

• delete\_latency

The total wait time of timed delete I/O events for the table.

• io\_read\_requests

The total number of read requests for the table.

• io\_read

The total number of bytes read from the table.

• io\_read\_latency

The total wait time of reads from the table.

• io\_write\_requests

The total number of write requests for the table.

• io\_write

The total number of bytes written to the table.

• io\_write\_latency

The total wait time of writes to the table.

• io\_misc\_requests

The total number of miscellaneous I/O requests for the table.

• io\_misc\_latency

The total wait time of miscellaneous I/O requests for the table.

• innodb\_buffer\_allocated

The total number of InnoDB buffer bytes allocated for the table.

• innodb\_buffer\_data

The total number of InnoDB data bytes allocated for the table.

• innodb\_buffer\_free

The total number of InnoDB nondata bytes allocated for the table (innodb\_buffer\_allocated − innodb\_buffer\_data).

• innodb\_buffer\_pages

The total number of InnoDB pages allocated for the table.

• innodb\_buffer\_pages\_hashed

The total number of InnoDB hashed pages allocated for the table.

• innodb\_buffer\_pages\_old

The total number of InnoDB old pages allocated for the table.

• innodb\_buffer\_rows\_cached

The total number of InnoDB cached rows for the table.

# <span id="page-176-0"></span>**30.4.3.31 The schema\_tables\_with\_full\_table\_scans and x \$schema\_tables\_with\_full\_table\_scans Views**

These views display which tables are being accessed with full table scans. By default, rows are sorted by descending rows scanned.

The [schema\\_tables\\_with\\_full\\_table\\_scans](#page-176-0) and [x](#page-176-0) [\\$schema\\_tables\\_with\\_full\\_table\\_scans](#page-176-0) views have these columns:

• object\_schema

The schema name.

• object\_name

The table name.

• rows\_full\_scanned

The total number of rows scanned by full scans of the table.

• latency

The total wait time of full scans of the table.

### <span id="page-176-1"></span>**30.4.3.32 The schema\_unused\_indexes View**

These views display indexes for which there are no events, which indicates that they are not being used. By default, rows are sorted by schema and table.

This view is most useful when the server has been up and processing long enough that its workload is representative. Otherwise, presence of an index in this view may not be meaningful.

The [schema\\_unused\\_indexes](#page-176-1) view has these columns:

• object\_schema

The schema name.

• object\_name

The table name.

• index\_name

The unused index name.

## <span id="page-177-0"></span>**30.4.3.33 The session and x\$session Views**

These views are similar to [processlist](#page-166-0) and [x\\$processlist](#page-166-0), but they filter out background processes to display only user sessions. For descriptions of the columns, see [Section 30.4.3.22, "The](#page-166-0) [processlist and x\\$processlist Views"](#page-166-0).

## <span id="page-177-1"></span>**30.4.3.34 The session\_ssl\_status View**

For each connection, this view displays the SSL version, cipher, and count of reused SSL sessions.

The [session\\_ssl\\_status](#page-177-1) view has these columns:

• thread\_id

The thread ID for the connection.

• ssl\_version

The version of SSL used for the connection.

• ssl\_cipher

The SSL cipher used for the connection.

• ssl\_sessions\_reused

The number of reused SSL sessions for the connection.

## <span id="page-177-2"></span>**30.4.3.35 The statement\_analysis and x\$statement\_analysis Views**

These views list normalized statements with aggregated statistics. The content mimics the MySQL Enterprise Monitor Query Analysis view. By default, rows are sorted by descending total latency.

The [statement\\_analysis](#page-177-2) and [x\\$statement\\_analysis](#page-177-2) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• full\_scan

The total number of full table scans performed by occurrences of the statement.

• exec\_count

The total number of times the statement has executed.

• err\_count

The total number of errors produced by occurrences of the statement.

• warn\_count

The total number of warnings produced by occurrences of the statement.

• total\_latency

The total wait time of timed occurrences of the statement.

• max\_latency

The maximum single wait time of timed occurrences of the statement.

• avg\_latency

The average wait time per timed occurrence of the statement.

• lock\_latency

The total time waiting for locks by timed occurrences of the statement.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_sent

The total number of rows returned by occurrences of the statement.

• rows\_sent\_avg

The average number of rows returned per occurrence of the statement.

• rows\_examined

The total number of rows read from storage engines by occurrences of the statement.

• rows\_examined\_avg

The average number of rows read from storage engines per occurrence of the statement.

• rows\_affected

The total number of rows affected by occurrences of the statement.

• rows\_affected\_avg

The average number of rows affected per occurrence of the statement.

• tmp\_tables

The total number of internal in-memory temporary tables created by occurrences of the statement.

• tmp\_disk\_tables

The total number of internal on-disk temporary tables created by occurrences of the statement.

• rows\_sorted

The total number of rows sorted by occurrences of the statement.

• sort\_merge\_passes

The total number of sort merge passes by occurrences of the statement.

• max\_controlled\_memory

The maximum amount of controlled memory (bytes) used by the statement.

This column was added in MySQL 8.0.31

• max\_total\_memory

The maximum amount of memory (bytes) used by the statement.

This column was added in MySQL 8.0.31

• digest

The statement digest.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

# <span id="page-179-0"></span>**30.4.3.36 The statements\_with\_errors\_or\_warnings and x \$statements\_with\_errors\_or\_warnings Views**

These views display normalized statements that have produced errors or warnings. By default, rows are sorted by descending error and warning counts.

The [statements\\_with\\_errors\\_or\\_warnings](#page-179-0) and [x](#page-179-0) [\\$statements\\_with\\_errors\\_or\\_warnings](#page-179-0) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec\_count

The total number of times the statement has executed.

• errors

The total number of errors produced by occurrences of the statement.

• error\_pct

The percentage of statement occurrences that produced errors.

• warnings

The total number of warnings produced by occurrences of the statement.

• warning\_pct

The percentage of statement occurrences that produced warnings.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

# <span id="page-180-0"></span>**30.4.3.37 The statements\_with\_full\_table\_scans and x \$statements\_with\_full\_table\_scans Views**

These views display normalized statements that have done full table scans. By default, rows are sorted by descending percentage of time a full scan was done and descending total latency.

The [statements\\_with\\_full\\_table\\_scans](#page-180-0) and [x\\$statements\\_with\\_full\\_table\\_scans](#page-180-0) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec\_count

The total number of times the statement has executed.

• total\_latency

The total wait time of timed statement events for the statement.

• no\_index\_used\_count

The total number of times no index was used to scan the table.

• no\_good\_index\_used\_count

The total number of times no good index was used to scan the table.

• no\_index\_used\_pct

The percentage of the time no index was used to scan the table.

• rows\_sent

The total number of rows returned from the table.

• rows\_examined

The total number of rows read from the storage engine for the table.

• rows\_sent\_avg

The average number of rows returned from the table.

• rows\_examined\_avg

The average number of rows read from the storage engine for the table.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

# <span id="page-181-0"></span>**30.4.3.38 The statements\_with\_runtimes\_in\_95th\_percentile and x \$statements\_with\_runtimes\_in\_95th\_percentile Views**

These views list statements with runtimes in the 95th percentile. By default, rows are sorted by descending average latency.

Both views use two helper views, x\$ps\_digest\_avg\_latency\_distribution and x \$ps\_digest\_95th\_percentile\_by\_avg\_us.

The [statements\\_with\\_runtimes\\_in\\_95th\\_percentile](#page-181-0) and [x](#page-181-0) [\\$statements\\_with\\_runtimes\\_in\\_95th\\_percentile](#page-181-0) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• full\_scan

The total number of full table scans performed by occurrences of the statement.

• exec\_count

The total number of times the statement has executed.

• err\_count

The total number of errors produced by occurrences of the statement.

• warn\_count

The total number of warnings produced by occurrences of the statement.

• total\_latency

The total wait time of timed occurrences of the statement.

• max\_latency

The maximum single wait time of timed occurrences of the statement.

• avg\_latency

The average wait time per timed occurrence of the statement.

• rows\_sent

The total number of rows returned by occurrences of the statement.

• rows\_sent\_avg

The average number of rows returned per occurrence of the statement.

• rows\_examined

The total number of rows read from storage engines by occurrences of the statement.

• rows\_examined\_avg

The average number of rows read from storage engines per occurrence of the statement.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

### <span id="page-182-0"></span>**30.4.3.39 The statements\_with\_sorting and x\$statements\_with\_sorting Views**

These views list normalized statements that have performed sorts. By default, rows are sorted by descending total latency.

The [statements\\_with\\_sorting](#page-182-0) and [x\\$statements\\_with\\_sorting](#page-182-0) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec\_count

The total number of times the statement has executed.

• total\_latency

The total wait time of timed occurrences of the statement.

• sort\_merge\_passes

The total number of sort merge passes by occurrences of the statement.

• avg\_sort\_merges

The average number of sort merge passes per occurrence of the statement.

• sorts\_using\_scans

The total number of sorts using table scans by occurrences of the statement.

• sort\_using\_range

The total number of sorts using range accesses by occurrences of the statement.

• rows\_sorted

The total number of rows sorted by occurrences of the statement.

• avg\_rows\_sorted

The average number of rows sorted per occurrence of the statement.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

## <span id="page-183-0"></span>**30.4.3.40 The statements\_with\_temp\_tables and x\$statements\_with\_temp\_tables Views**

These views list normalized statements that have used temporary tables. By default, rows are sorted by descending number of on-disk temporary tables used and descending number of in-memory temporary tables used.

The [statements\\_with\\_temp\\_tables](#page-183-0) and [x\\$statements\\_with\\_temp\\_tables](#page-183-0) views have these columns:

• query

The normalized statement string.

• db

The default database for the statement, or NULL if there is none.

• exec\_count

The total number of times the statement has executed.

• total\_latency

The total wait time of timed occurrences of the statement.

• memory\_tmp\_tables

The total number of internal in-memory temporary tables created by occurrences of the statement.

• disk\_tmp\_tables

The total number of internal on-disk temporary tables created by occurrences of the statement.

• avg\_tmp\_tables\_per\_query

The average number of internal temporary tables created per occurrence of the statement.

• tmp\_tables\_to\_disk\_pct

The percentage of internal in-memory temporary tables that were converted to on-disk tables.

• first\_seen

The time at which the statement was first seen.

• last\_seen

The time at which the statement was most recently seen.

• digest

The statement digest.

## <span id="page-184-0"></span>**30.4.3.41 The user\_summary and x\$user\_summary Views**

These views summarize statement activity, file I/O, and connections, grouped by user. By default, rows are sorted by descending total latency.

The [user\\_summary](#page-184-0) and [x\\$user\\_summary](#page-184-0) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• statements

The total number of statements for the user.

• statement\_latency

The total wait time of timed statements for the user.

• statement\_avg\_latency

The average wait time per timed statement for the user.

• table\_scans

The total number of table scans for the user.

• file\_ios

The total number of file I/O events for the user.

• file\_io\_latency

The total wait time of timed file I/O events for the user.

• current\_connections

The current number of connections for the user.

• total\_connections

The total number of connections for the user.

• unique\_hosts

The number of distinct hosts from which connections for the user have originated.

• current\_memory

The current amount of allocated memory for the user.

• total\_memory\_allocated

The total amount of allocated memory for the user.

## <span id="page-184-1"></span>**30.4.3.42 The user\_summary\_by\_file\_io and x\$user\_summary\_by\_file\_io Views**

These views summarize file I/O, grouped by user. By default, rows are sorted by descending total file I/ O latency.

The [user\\_summary\\_by\\_file\\_io](#page-184-1) and [x\\$user\\_summary\\_by\\_file\\_io](#page-184-1) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• ios

The total number of file I/O events for the user.

• io\_latency

The total wait time of timed file I/O events for the user.

# <span id="page-185-0"></span>**30.4.3.43 The user\_summary\_by\_file\_io\_type and x\$user\_summary\_by\_file\_io\_type Views**

These views summarize file I/O, grouped by user and event type. By default, rows are sorted by user and descending total latency.

The [user\\_summary\\_by\\_file\\_io\\_type](#page-185-0) and [x\\$user\\_summary\\_by\\_file\\_io\\_type](#page-185-0) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• event\_name

The file I/O event name.

• total

The total number of occurrences of the file I/O event for the user.

• latency

The total wait time of timed occurrences of the file I/O event for the user.

• max\_latency

The maximum single wait time of timed occurrences of the file I/O event for the user.

### <span id="page-185-1"></span>**30.4.3.44 The user\_summary\_by\_stages and x\$user\_summary\_by\_stages Views**

These views summarize stages, grouped by user. By default, rows are sorted by user and descending total stage latency.

The [user\\_summary\\_by\\_stages](#page-185-1) and [x\\$user\\_summary\\_by\\_stages](#page-185-1) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• event\_name

The stage event name.

• total

The total number of occurrences of the stage event for the user.

• total\_latency

The total wait time of timed occurrences of the stage event for the user.

• avg\_latency

The average wait time per timed occurrence of the stage event for the user.

# <span id="page-186-0"></span>**30.4.3.45 The user\_summary\_by\_statement\_latency and x \$user\_summary\_by\_statement\_latency Views**

These views summarize overall statement statistics, grouped by user. By default, rows are sorted by descending total latency.

The [user\\_summary\\_by\\_statement\\_latency](#page-186-0) and [x\\$user\\_summary\\_by\\_statement\\_latency](#page-186-0) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• total

The total number of statements for the user.

• total\_latency

The total wait time of timed statements for the user.

• max\_latency

The maximum single wait time of timed statements for the user.

• lock\_latency

The total time waiting for locks by timed statements for the user.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_sent

The total number of rows returned by statements for the user.

• rows\_examined

The total number of rows read from storage engines by statements for the user.

• rows\_affected

The total number of rows affected by statements for the user.

• full\_scans

The total number of full table scans by statements for the user.

# <span id="page-186-1"></span>**30.4.3.46 The user\_summary\_by\_statement\_type and x \$user\_summary\_by\_statement\_type Views**

These views summarize information about statements executed, grouped by user and statement type. By default, rows are sorted by user and descending total latency.

The [user\\_summary\\_by\\_statement\\_type](#page-186-1) and [x\\$user\\_summary\\_by\\_statement\\_type](#page-186-1) views have these columns:

• user

The client user name. Rows for which the USER column in the underlying Performance Schema table is NULL are assumed to be for background threads and are reported with a host name of background.

• statement

The final component of the statement event name.

• total

The total number of occurrences of the statement event for the user.

• total\_latency

The total wait time of timed occurrences of the statement event for the user.

• max\_latency

The maximum single wait time of timed occurrences of the statement event for the user.

• lock\_latency

The total time waiting for locks by timed occurrences of the statement event for the user.

• cpu\_latency

The time spent on CPU for the current thread.

• rows\_sent

The total number of rows returned by occurrences of the statement event for the user.

• rows\_examined

The total number of rows read from storage engines by occurrences of the statement event for the user.

• rows\_affected

The total number of rows affected by occurrences of the statement event for the user.

• full\_scans

The total number of full table scans by occurrences of the statement event for the user.

## <span id="page-187-0"></span>**30.4.3.47 The version View**

This view provides the current [sys](#page-140-1) schema and MySQL server versions.

![](_page_187_Picture_27.jpeg)

## **Note**

As of MySQL 8.0.18, this view is deprecated and subject to removal in a future MySQL version. Applications that use it should be migrated to use an alternative instead. For example, use the VERSION() function to retrieve the MySQL server version.

The [version](#page-187-0) view has these columns:

• sys\_version

The [sys](#page-140-1) schema version.

• mysql\_version

The MySQL server version.

# <span id="page-188-0"></span>**30.4.3.48 The wait\_classes\_global\_by\_avg\_latency and x \$wait\_classes\_global\_by\_avg\_latency Views**

These views summarize wait class average latencies, grouped by event class. By default, rows are sorted by descending average latency. Idle events are ignored.

An event class is determined by stripping from the event name everything after the first three components. For example, the class for wait/io/file/sql/slow\_log is wait/io/file.

The [wait\\_classes\\_global\\_by\\_avg\\_latency](#page-188-0) and [x](#page-188-0) [\\$wait\\_classes\\_global\\_by\\_avg\\_latency](#page-188-0) views have these columns:

• event\_class

The event class.

• total

The total number of occurrences of events in the class.

• total\_latency

The total wait time of timed occurrences of events in the class.

• min\_latency

The minimum single wait time of timed occurrences of events in the class.

• avg\_latency

The average wait time per timed occurrence of events in the class.

• max\_latency

The maximum single wait time of timed occurrences of events in the class.

# <span id="page-188-1"></span>**30.4.3.49 The wait\_classes\_global\_by\_latency and x\$wait\_classes\_global\_by\_latency Views**

These views summarize wait class total latencies, grouped by event class. By default, rows are sorted by descending total latency. Idle events are ignored.

An event class is determined by stripping from the event name everything after the first three components. For example, the class for wait/io/file/sql/slow\_log is wait/io/file.

The [wait\\_classes\\_global\\_by\\_latency](#page-188-1) and [x\\$wait\\_classes\\_global\\_by\\_latency](#page-188-1) views have these columns:

• event\_class

The event class.

• total

The total number of occurrences of events in the class.

• total\_latency

The total wait time of timed occurrences of events in the class.

• min\_latency

The minimum single wait time of timed occurrences of events in the class.

• avg\_latency

The average wait time per timed occurrence of events in the class.

• max\_latency

The maximum single wait time of timed occurrences of events in the class.

## <span id="page-189-0"></span>**30.4.3.50 The waits\_by\_host\_by\_latency and x\$waits\_by\_host\_by\_latency Views**

These views summarize wait events, grouped by host and event. By default, rows are sorted by host and descending total latency. Idle events are ignored.

The [waits\\_by\\_host\\_by\\_latency](#page-189-0) and [x\\$waits\\_by\\_host\\_by\\_latency](#page-189-0) views have these columns:

• host

The host from which the connection originated.

• event

The event name.

• total

The total number of occurrences of the event for the host.

• total\_latency

The total wait time of timed occurrences of the event for the host.

• avg\_latency

The average wait time per timed occurrence of the event for the host.

• max\_latency

The maximum single wait time of timed occurrences of the event for the host.

## <span id="page-189-1"></span>**30.4.3.51 The waits\_by\_user\_by\_latency and x\$waits\_by\_user\_by\_latency Views**

These views summarize wait events, grouped by user and event. By default, rows are sorted by user and descending total latency. Idle events are ignored.

The [waits\\_by\\_user\\_by\\_latency](#page-189-1) and [x\\$waits\\_by\\_user\\_by\\_latency](#page-189-1) views have these columns:

• user

The user associated with the connection.

• event

The event name.

• total

The total number of occurrences of the event for the user.

• total\_latency

The total wait time of timed occurrences of the event for the user.

• avg\_latency

The average wait time per timed occurrence of the event for the user.

• max\_latency

The maximum single wait time of timed occurrences of the event for the user.

## <span id="page-190-1"></span>**30.4.3.52 The waits\_global\_by\_latency and x\$waits\_global\_by\_latency Views**

These views summarize wait events, grouped by event. By default, rows are sorted by descending total latency. Idle events are ignored.

The [waits\\_global\\_by\\_latency](#page-190-1) and [x\\$waits\\_global\\_by\\_latency](#page-190-1) views have these columns:

• events

The event name.

• total

The total number of occurrences of the event.

• total\_latency

The total wait time of timed occurrences of the event.

• avg\_latency

The average wait time per timed occurrence of the event.

• max\_latency

The maximum single wait time of timed occurrences of the event.

# <span id="page-190-0"></span>**30.4.4 sys Schema Stored Procedures**

The following sections describe [sys](#page-140-1) schema stored procedures.

### <span id="page-190-2"></span>**30.4.4.1 The create\_synonym\_db() Procedure**

Given a schema name, this procedure creates a synonym schema containing views that refer to all the tables and views in the original schema. This can be used, for example, to create a shorter name by which to refer to a schema with a long name (such as info rather than INFORMATION\_SCHEMA).

### **Parameters**

- in\_db\_name VARCHAR(64): The name of the schema for which to create the synonym.
- in\_synonym VARCHAR(64): The name to use for the synonym schema. This schema must not already exist.

### **Example**

```
mysql> SHOW DATABASES;
+--------------------+
| Database |
+--------------------+
| information_schema |
| mysql |
| performance_schema |
| sys |
| world |
+--------------------+
mysql> CALL sys.create_synonym_db('INFORMATION_SCHEMA', 'info');
+---------------------------------------+
| summary |
+---------------------------------------+
| Created 63 views in the info database |
+---------------------------------------+
mysql> SHOW DATABASES;
+--------------------+
| Database |
+--------------------+
| information_schema |
| info |
| mysql |
| performance_schema |
| sys |
| world |
+--------------------+
mysql> SHOW FULL TABLES FROM info;
+---------------------------------------+------------+
| Tables_in_info | Table_type |
+---------------------------------------+------------+
| character_sets | VIEW |
| collation_character_set_applicability | VIEW |
| collations | VIEW |
| column_privileges | VIEW |
| columns | VIEW |
...
```

### <span id="page-191-0"></span>**30.4.4.2 The diagnostics() Procedure**

Creates a report of the current server status for diagnostic purposes.

This procedure disables binary logging during its execution by manipulating the session value of the sql\_log\_bin system variable. That is a restricted operation, so the procedure requires privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

Data collected for [diagnostics\(\)](#page-191-0) includes this information:

- Information from the [metrics](#page-165-1) view (see [Section 30.4.3.21, "The metrics View"\)](#page-165-1)
- Information from other relevant sys schema views, such as the one that determines queries in the 95th percentile
- Information from the ndbinfo schema, if the MySQL server is part of NDB Cluster
- Replication status (both source and replica)

Some of the sys schema views are calculated as initial (optional), overall, and delta values:

- The initial view is the content of the view at the start of the [diagnostics\(\)](#page-191-0) procedure. This output is the same as the start values used for the delta view. The initial view is included if the diagnostics.include\_raw configuration option is ON.
- The overall view is the content of the view at the end of the [diagnostics\(\)](#page-191-0) procedure. This output is the same as the end values used for the delta view. The overall view is always included.

• The delta view is the difference from the beginning to the end of procedure execution. The minimum and maximum values are the minimum and maximum values from the end view, respectively. They do not necessarily reflect the minimum and maximum values in the monitored period. Except for the [metrics](#page-165-1) view, the delta is calculated only between the first and last outputs.

### **Parameters**

- in\_max\_runtime INT UNSIGNED: The maximum data collection time in seconds. Use NULL to collect data for the default of 60 seconds. Otherwise, use a value greater than 0.
- in\_interval INT UNSIGNED: The sleep time between data collections in seconds. Use NULL to sleep for the default of 30 seconds. Otherwise, use a value greater than 0.
- in\_auto\_config ENUM('current', 'medium', 'full'): The Performance Schema configuration to use. Permitted values are:
  - current: Use the current instrument and consumer settings.
  - medium: Enable some instruments and consumers.
  - full: Enable all instruments and consumers.

![](_page_192_Picture_9.jpeg)

#### **Note**

The more instruments and consumers enabled, the more impact on MySQL server performance. Be careful with the medium setting and especially the full setting, which has a large performance impact.

Use of the medium or full setting requires the SUPER privilege.

If a setting other than current is chosen, the current settings are restored at the end of the procedure.

### **Configuration Options**

[diagnostics\(\)](#page-191-0) operation can be modified using the following configuration options or their corresponding user-defined variables (see [Section 30.4.2.1, "The sys\\_config Table"](#page-148-1)):

• debug, @sys.debug

If this option is ON, produce debugging output. The default is OFF.

• diagnostics.allow\_i\_s\_tables, @sys.diagnostics.allow\_i\_s\_tables

If this option is ON, the [diagnostics\(\)](#page-191-0) procedure is permitted to perform table scans on the Information Schema TABLES table. This can be expensive if there are many tables. The default is OFF.

• diagnostics.include\_raw, @sys.diagnostics.include\_raw

If this option is ON, the [diagnostics\(\)](#page-191-0) procedure output includes the raw output from querying the [metrics](#page-165-1) view. The default is OFF.

• statement\_truncate\_len, @sys.statement\_truncate\_len

The maximum length of statements returned by the format\_statement() function. Longer statements are truncated to this length. The default is 64.

### **Example**

Create a diagnostics report that starts an iteration every 30 seconds and runs for at most 120 seconds using the current Performance Schema settings:

```
mysql> CALL sys.diagnostics(120, 30, 'current');
```

To capture the output from the diagnostics() procedure in a file as it runs, use the mysql client tee filename and notee commands (see Section 6.5.1.2, "mysql Client Commands"):

```
mysql> tee diag.out;
mysql> CALL sys.diagnostics(120, 30, 'current');
mysql> notee;
```

### <span id="page-193-0"></span>**30.4.4.3 The execute\_prepared\_stmt() Procedure**

Given an SQL statement as a string, executes it as a prepared statement. The prepared statement is deallocated after execution, so it is not subject to reuse. Thus, this procedure is useful primarily for executing dynamic statements on a one-time basis.

This procedure uses sys\_execute\_prepared\_stmt as the prepared statement name. If that statement name exists when the procedure is called, its previous content is destroyed.

### **Parameters**

• in\_query LONGTEXT CHARACTER SET utf8mb3: The statement string to execute.

### **Configuration Options**

[execute\\_prepared\\_stmt\(\)](#page-193-0) operation can be modified using the following configuration options or their corresponding user-defined variables (see [Section 30.4.2.1, "The sys\\_config Table"](#page-148-1)):

• debug, @sys.debug

If this option is ON, produce debugging output. The default is OFF.

### **Example**

```
mysql> CALL sys.execute_prepared_stmt('SELECT COUNT(*) FROM mysql.user');
+----------+
| COUNT(*) |
+----------+
| 15 |
+----------+
```

## <span id="page-193-1"></span>**30.4.4.4 The ps\_setup\_disable\_background\_threads() Procedure**

Disables Performance Schema instrumentation for all background threads. Produces a result set indicating how many background threads were disabled. Already disabled threads do not count.

### **Parameters**

None.

### **Example**

```
mysql> CALL sys.ps_setup_disable_background_threads();
+--------------------------------+
| summary |
+--------------------------------+
| Disabled 24 background threads |
+--------------------------------+
```

## <span id="page-193-2"></span>**30.4.4.5 The ps\_setup\_disable\_consumer() Procedure**

Disables Performance Schema consumers with names that contain the argument. Produces a result set indicating how many consumers were disabled. Already disabled consumers do not count.

### **Parameters**

• consumer VARCHAR(128): The value used to match consumer names, which are identified by using %consumer% as an operand for a LIKE pattern match.

A value of '' matches all consumers.

### **Example**

Disable all statement consumers:

```
mysql> CALL sys.ps_setup_disable_consumer('statement');
+----------------------+
| summary |
+----------------------+
| Disabled 4 consumers |
+----------------------+
```

## <span id="page-194-0"></span>**30.4.4.6 The ps\_setup\_disable\_instrument() Procedure**

Disables Performance Schema instruments with names that contain the argument. Produces a result set indicating how many instruments were disabled. Already disabled instruments do not count.

### **Parameters**

• in\_pattern VARCHAR(128): The value used to match instrument names, which are identified by using %in\_pattern% as an operand for a LIKE pattern match.

A value of '' matches all instruments.

### **Example**

Disable a specific instrument:

```
mysql> CALL sys.ps_setup_disable_instrument('wait/lock/metadata/sql/mdl');
+-----------------------+
| summary |
+-----------------------+
| Disabled 1 instrument |
+-----------------------+
```

Disable all mutex instruments:

```
mysql> CALL sys.ps_setup_disable_instrument('mutex');
+--------------------------+
| summary |
+--------------------------+
| Disabled 177 instruments |
+--------------------------+
```

### <span id="page-194-1"></span>**30.4.4.7 The ps\_setup\_disable\_thread() Procedure**

Given a connection ID, disables Performance Schema instrumentation for the thread. Produces a result set indicating how many threads were disabled. Already disabled threads do not count.

### **Parameters**

• in\_connection\_id BIGINT: The connection ID. This is a value of the type given in the PROCESSLIST\_ID column of the Performance Schema [threads](#page-99-0) table or the Id column of SHOW PROCESSLIST output.

### **Example**

Disable a specific connection by its connection ID:

```
mysql> CALL sys.ps_setup_disable_thread(225);
+-------------------+
| summary |
+-------------------+
| Disabled 1 thread |
+-------------------+
```

Disable the current connection:

```
mysql> CALL sys.ps_setup_disable_thread(CONNECTION_ID());
+-------------------+
| summary |
+-------------------+
| Disabled 1 thread |
+-------------------+
```

## <span id="page-195-0"></span>**30.4.4.8 The ps\_setup\_enable\_background\_threads() Procedure**

Enables Performance Schema instrumentation for all background threads. Produces a result set indicating how many background threads were enabled. Already enabled threads do not count.

## **Parameters**

None.

## **Example**

```
mysql> CALL sys.ps_setup_enable_background_threads();
+-------------------------------+
| summary |
+-------------------------------+
| Enabled 24 background threads |
+-------------------------------+
```

## <span id="page-195-1"></span>**30.4.4.9 The ps\_setup\_enable\_consumer() Procedure**

Enables Performance Schema consumers with names that contain the argument. Produces a result set indicating how many consumers were enabled. Already enabled consumers do not count.

### **Parameters**

• consumer VARCHAR(128): The value used to match consumer names, which are identified by using %consumer% as an operand for a LIKE pattern match.

A value of '' matches all consumers.

### **Example**

Enable all statement consumers:

```
mysql> CALL sys.ps_setup_enable_consumer('statement');
+---------------------+
| summary |
+---------------------+
| Enabled 4 consumers |
+---------------------+
```

## <span id="page-195-2"></span>**30.4.4.10 The ps\_setup\_enable\_instrument() Procedure**

Enables Performance Schema instruments with names that contain the argument. Produces a result set indicating how many instruments were enabled. Already enabled instruments do not count.

### **Parameters**

• in\_pattern VARCHAR(128): The value used to match instrument names, which are identified by using %in\_pattern% as an operand for a LIKE pattern match.

A value of '' matches all instruments.

### **Example**

Enable a specific instrument:

```
mysql> CALL sys.ps_setup_enable_instrument('wait/lock/metadata/sql/mdl');
+----------------------+
| summary |
+----------------------+
| Enabled 1 instrument |
+----------------------+
```

Enable all mutex instruments:

```
mysql> CALL sys.ps_setup_enable_instrument('mutex');
+-------------------------+
| summary |
+-------------------------+
| Enabled 177 instruments |
+-------------------------+
```

# <span id="page-196-0"></span>**30.4.4.11 The ps\_setup\_enable\_thread() Procedure**

Given a connection ID, enables Performance Schema instrumentation for the thread. Produces a result set indicating how many threads were enabled. Already enabled threads do not count.

## **Parameters**

• in\_connection\_id BIGINT: The connection ID. This is a value of the type given in the PROCESSLIST\_ID column of the Performance Schema [threads](#page-99-0) table or the Id column of SHOW PROCESSLIST output.

### **Example**

Enable a specific connection by its connection ID:

```
mysql> CALL sys.ps_setup_enable_thread(225);
+------------------+
| summary |
+------------------+
| Enabled 1 thread |
+------------------+
```

Enable the current connection:

```
mysql> CALL sys.ps_setup_enable_thread(CONNECTION_ID());
+------------------+
| summary |
+------------------+
| Enabled 1 thread |
+------------------+
```

## <span id="page-196-1"></span>**30.4.4.12 The ps\_setup\_reload\_saved() Procedure**

Reloads a Performance Schema configuration saved earlier within the same session using [ps\\_setup\\_save\(\)](#page-197-0). For more information, see the description of [ps\\_setup\\_save\(\)](#page-197-0).

This procedure disables binary logging during its execution by manipulating the session value of the sql\_log\_bin system variable. That is a restricted operation, so the procedure requires privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

### **Parameters**

None.

### <span id="page-197-1"></span>**30.4.4.13 The ps\_setup\_reset\_to\_default() Procedure**

Resets the Performance Schema configuration to its default settings.

### **Parameters**

• in\_verbose BOOLEAN: Whether to display information about each setup stage during procedure execution. This includes the SQL statements executed.

### **Example**

```
mysql> CALL sys.ps_setup_reset_to_default(TRUE)\G
*************************** 1. row ***************************
status: Resetting: setup_actors
DELETE
FROM performance_schema.setup_actors
WHERE NOT (HOST = '%' AND USER = '%' AND ROLE = '%')
*************************** 1. row ***************************
status: Resetting: setup_actors
INSERT IGNORE INTO performance_schema.setup_actors
VALUES ('%', '%', '%')
...
```

# <span id="page-197-0"></span>**30.4.4.14 The ps\_setup\_save() Procedure**

Saves the current Performance Schema configuration. This enables you to alter the configuration temporarily for debugging or other purposes, then restore it to the previous state by invoking the [ps\\_setup\\_reload\\_saved\(\)](#page-196-1) procedure.

To prevent other simultaneous calls to save the configuration, [ps\\_setup\\_save\(\)](#page-197-0) acquires an advisory lock named sys.ps\_setup\_save by calling the GET\_LOCK() function. [ps\\_setup\\_save\(\)](#page-197-0) takes a timeout parameter to indicate how many seconds to wait if the lock already exists (which indicates that some other session has a saved configuration outstanding). If the timeout expires without obtaining the lock, [ps\\_setup\\_save\(\)](#page-197-0) fails.

It is intended you call [ps\\_setup\\_reload\\_saved\(\)](#page-196-1) later within the same session as [ps\\_setup\\_save\(\)](#page-197-0) because the configuration is saved in TEMPORARY tables. [ps\\_setup\\_save\(\)](#page-197-0) drops the temporary tables and releases the lock. If you end your session without invoking [ps\\_setup\\_save\(\)](#page-197-0), the tables and lock disappear automatically.

This procedure disables binary logging during its execution by manipulating the session value of the sql\_log\_bin system variable. That is a restricted operation, so the procedure requires privileges sufficient to set restricted session variables. See Section 7.1.9.1, "System Variable Privileges".

### **Parameters**

• in\_timeout INT: How many seconds to wait to obtain the sys.ps\_setup\_save lock. A negative timeout value means infinite timeout.

### **Example**

```
mysql> CALL sys.ps_setup_save(10);
```

```
... make Performance Schema configuration changes ...
mysql> CALL sys.ps_setup_reload_saved();
```

## <span id="page-198-0"></span>**30.4.4.15 The ps\_setup\_show\_disabled() Procedure**

Displays all currently disabled Performance Schema configuration.

### **Parameters**

- in\_show\_instruments BOOLEAN: Whether to display disabled instruments. This might be a long list.
- in\_show\_threads BOOLEAN: Whether to display disabled threads.

### **Example**

```
mysql> CALL sys.ps_setup_show_disabled(TRUE, TRUE);
+----------------------------+
| performance_schema_enabled |
+----------------------------+
| 1 |
+----------------------------+
+---------------+
| enabled_users |
+---------------+
| '%'@'%' |
+---------------+
+-------------+----------------------+---------+-------+
| object_type | objects | enabled | timed |
+-------------+----------------------+---------+-------+
| EVENT | mysql.% | NO | NO |
| EVENT | performance_schema.% | NO | NO |
| EVENT | information_schema.% | NO | NO |
| FUNCTION | mysql.% | NO | NO |
| FUNCTION | performance_schema.% | NO | NO |
| FUNCTION | information_schema.% | NO | NO |
| PROCEDURE | mysql.% | NO | NO |
| PROCEDURE | performance_schema.% | NO | NO |
| PROCEDURE | information_schema.% | NO | NO |
| TABLE | mysql.% | NO | NO |
| TABLE | performance_schema.% | NO | NO |
| TABLE | information_schema.% | NO | NO |
| TRIGGER | mysql.% | NO | NO |
| TRIGGER | performance_schema.% | NO | NO |
| TRIGGER | information_schema.% | NO | NO |
+-------------+----------------------+---------+-------+
...
```

## <span id="page-198-1"></span>**30.4.4.16 The ps\_setup\_show\_disabled\_consumers() Procedure**

Displays all currently disabled Performance Schema consumers.

### **Parameters**

None.

### **Example**

```
mysql> CALL sys.ps_setup_show_disabled_consumers();
+----------------------------------+
| disabled_consumers |
+----------------------------------+
| events_stages_current |
| events_stages_history |
```

```
| events_stages_history_long |
| events_statements_history |
| events_statements_history_long |
| events_transactions_history |
| events_transactions_history_long |
| events_waits_current |
| events_waits_history |
| events_waits_history_long |
+----------------------------------+
```

## <span id="page-199-0"></span>**30.4.4.17 The ps\_setup\_show\_disabled\_instruments() Procedure**

Displays all currently disabled Performance Schema instruments. This might be a long list.

### **Parameters**

None.

## **Example**

```
mysql> CALL sys.ps_setup_show_disabled_instruments()\G
*************************** 1. row ***************************
disabled_instruments: wait/synch/mutex/sql/TC_LOG_MMAP::LOCK_tc
 timed: NO
*************************** 2. row ***************************
disabled_instruments: wait/synch/mutex/sql/THD::LOCK_query_plan
 timed: NO
*************************** 3. row ***************************
disabled_instruments: wait/synch/mutex/sql/MYSQL_BIN_LOG::LOCK_commit
 timed: NO
...
```

## <span id="page-199-1"></span>**30.4.4.18 The ps\_setup\_show\_enabled() Procedure**

Displays all currently enabled Performance Schema configuration.

## **Parameters**

- in\_show\_instruments BOOLEAN: Whether to display enabled instruments. This might be a long list.
- in\_show\_threads BOOLEAN: Whether to display enabled threads.

### **Example**

```
mysql> CALL sys.ps_setup_show_enabled(FALSE, FALSE);
+----------------------------+
| performance_schema_enabled |
+----------------------------+
| 1 |
+----------------------------+
1 row in set (0.01 sec)
+---------------+
| enabled_users |
+---------------+
| '%'@'%' |
+---------------+
1 row in set (0.01 sec)
+-------------+---------+---------+-------+
| object_type | objects | enabled | timed |
+-------------+---------+---------+-------+
| EVENT | %.% | YES | YES |
| FUNCTION | %.% | YES | YES |
| PROCEDURE | %.% | YES | YES |
| TABLE | %.% | YES | YES |
| TRIGGER | %.% | YES | YES |
```

```
+-------------+---------+---------+-------+
5 rows in set (0.02 sec)
+-----------------------------+
| enabled_consumers |
+-----------------------------+
| events_statements_current |
| events_statements_history |
| events_transactions_current |
| events_transactions_history |
| global_instrumentation |
| statements_digest |
| thread_instrumentation |
+-----------------------------+
```