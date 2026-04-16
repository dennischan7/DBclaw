---
source: MySQL 8.4 Reference
title: 00_Overview
---

The Performance Schema avoids using mutexes to collect or produce data, so there are no guarantees of consistency and results can sometimes be incorrect. Event values in performance\_schema tables are nondeterministic and nonrepeatable.

If you save event information in another table, you should not assume that the original events remain available later. For example, if you select events from a performance\_schema table into a temporary table, intending to join that table with the original table later, there might be no matches.

mysqldump and BACKUP DATABASE ignore tables in the performance\_schema database.

Tables in the performance\_schema database cannot be locked with LOCK TABLES, except the setup\_xxx tables.

Tables in the performance\_schema database cannot be indexed.

Tables in the performance\_schema database are not replicated.

The types of timers might vary per platform. The [performance\\_timers](#page-152-0) table shows which event timers are available. If the values in this table for a given timer name are NULL, that timer is not supported on your platform.

Instruments that apply to storage engines might not be implemented for all storage engines. Instrumentation of each third-party engine is the responsibility of the engine maintainer.

# <span id="page-198-1"></span>Chapter 30 MySQL sys Schema

# **Table of Contents**

| 30.1 Prerequisites for Using the sys Schema 4969 |  |
|--------------------------------------------------|--|
| 30.2 Using the sys Schema 4970                   |  |
| 30.3 sys Schema Progress Reporting 4971          |  |
| 30.4 sys Schema Object Reference 4972            |  |
| 30.4.1 sys Schema Object Index 4972              |  |
| 30.4.2 sys Schema Tables and Triggers 4977       |  |
| 30.4.3 sys Schema Views 4979                     |  |
| 30.4.4 sys Schema Stored Procedures 5019         |  |
| 30.4.5 sys Schema Stored Functions 5037          |  |

MySQL 8.4 includes the [sys](#page-198-1) schema, a set of objects that helps DBAs and developers interpret data collected by the Performance Schema. [sys](#page-198-1) schema objects can be used for typical tuning and diagnosis use cases. Objects in this schema include:

- Views that summarize Performance Schema data into more easily understandable form.
- Stored procedures that perform operations such as Performance Schema configuration and generating diagnostic reports.
- Stored functions that query Performance Schema configuration and provide formatting services.

For new installations, the [sys](#page-198-1) schema is installed by default during data directory initialization if you use mysqld with the --initialize or --initialize-insecure option. If this is not desired, you can drop the [sys](#page-198-1) schema manually after initialization if it is unneeded.

The MySQL upgrade procedure produces an error if a [sys](#page-198-1) schema exists but has no version view, on the assumption that absence of this view indicates a user-created sys schema. To upgrade in this case, remove or rename the existing [sys](#page-198-1) schema first.

[sys](#page-198-1) schema objects have a DEFINER of 'mysql.sys'@'localhost'. Use of the dedicated mysql.sys account avoids problems that occur if a DBA renames or removes the root account.

# <span id="page-198-0"></span>**30.1 Prerequisites for Using the sys Schema**

Before using the [sys](#page-198-1) schema, the prerequisites described in this section must be satisfied.

Because the [sys](#page-198-1) schema provides an alternative means of accessing the Performance Schema, the Performance Schema must be enabled for the [sys](#page-198-1) schema to work. See Section 29.3, "Performance Schema Startup Configuration".

For full access to the [sys](#page-198-1) schema, a user must have these privileges:

- SELECT on all [sys](#page-198-1) tables and views
- EXECUTE on all [sys](#page-198-1) stored procedures and functions
- INSERT and UPDATE for the sys\_config table, if changes are to be made to it
- Additional privileges for certain [sys](#page-198-1) schema stored procedures and functions, as noted in their descriptions (for example, the ps\_setup\_save() procedure)

It is also necessary to have privileges for the objects underlying the [sys](#page-198-1) schema objects:

- SELECT on any Performance Schema tables accessed by [sys](#page-198-1) schema objects, and UPDATE for any tables to be updated using [sys](#page-198-1) schema objects
- PROCESS for the INFORMATION\_SCHEMA INNODB\_BUFFER\_PAGE table

Certain Performance Schema instruments and consumers must be enabled and (for instruments) timed to take full advantage of [sys](#page-198-1) schema capabilities:

- All wait instruments
- All stage instruments
- All statement instruments
- xxx\_current and xxx\_history\_long consumers for all events

You can use the [sys](#page-198-1) schema itself to enable all of the additional instruments and consumers:

```
CALL sys.ps_setup_enable_instrument('wait');
CALL sys.ps_setup_enable_instrument('stage');
CALL sys.ps_setup_enable_instrument('statement');
CALL sys.ps_setup_enable_consumer('current');
CALL sys.ps_setup_enable_consumer('history_long');
```

![](_page_199_Picture_8.jpeg)

#### **Note**

For many uses of the sys schema, the default Performance Schema is sufficient for data collection. Enabling all the instruments and consumers just mentioned has a performance impact, so it is preferable to enable only the additional configuration you need. Also, remember that if you enable additional configuration, you can easily restore the default configuration like this:

```
CALL sys.ps_setup_reset_to_default(TRUE);
```

# <span id="page-199-0"></span>**30.2 Using the sys Schema**

You can make the [sys](#page-198-1) schema the default schema so that references to its objects need not be qualified with the schema name:

```
mysql> USE sys;
Database changed
mysql> SELECT * FROM version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1 | 8.4.0-tr |
+-------------+---------------+
```

(The version view shows the [sys](#page-198-1) schema and MySQL server versions.)

To access [sys](#page-198-1) schema objects while a different schema is the default (or simply to be explicit), qualify object references with the schema name:

```
mysql> SELECT * FROM sys.version;
+-------------+---------------+
| sys_version | mysql_version |
+-------------+---------------+
| 2.1.1 | 8.4.0-tr |
+-------------+---------------+
```

The sys schema contains many views that summarize Performance Schema tables in various ways. Most of these views come in pairs, such that one member of the pair has the same name as the other member, plus a x\$ prefix. For example, the host\_summary\_by\_file\_io view summarizes file I/ O grouped by host and displays latencies converted from picoseconds to more readable values (with units);

```
mysql> SELECT * FROM sys.host_summary_by_file_io;
+------------+-------+------------+
| host | ios | io_latency |
+------------+-------+------------+
| localhost | 67570 | 5.38 s |
| background | 3468 | 4.18 s |
```

+------------+-------+------------+

The [x\\$host\\_summary\\_by\\_file\\_io](#page-10-0) view summarizes the same data but displays unformatted picosecond latencies:

```
mysql> SELECT * FROM sys.x$host_summary_by_file_io;
+------------+-------+---------------+
| host | ios | io_latency |
+------------+-------+---------------+
| localhost | 67574 | 5380678125144 |
| background | 3474 | 4758696829416 |
+------------+-------+---------------+
```

The view without the x\$ prefix is intended to provide output that is more user friendly and easier for humans to read. The view with the x\$ prefix that displays the same values in raw form is intended more for use with other tools that perform their own processing on the data. For additional information about the differences between non-x\$ and x\$ views, see [Section 30.4.3, "sys Schema Views".](#page-8-0)

To examine sys schema object definitions, use the appropriate SHOW statement or INFORMATION\_SCHEMA query. For example, to examine the definitions of the [session](#page-35-0) view and [format\\_bytes\(\)](#page-67-0) function, use these statements:

```
mysql> SHOW CREATE VIEW sys.session;
mysql> SHOW CREATE FUNCTION sys.format_bytes;
```

However, those statements display the definitions in relatively unformatted form. To view object definitions with more readable formatting, access the individual .sql files found under the scripts/ sys\_schema directory in MySQL source distributions.

mysqldump does not dump the sys schema by default. To generate a dump file, name the sys schema explicitly on the command line using either of these commands:

```
mysqldump --databases --routines sys > sys_dump.sql
```

To reinstall the schema from the dump file, use this command:

```
mysql < sys_dump.sql
```

# <span id="page-0-0"></span>**30.3 sys Schema Progress Reporting**

The following sys schema views provide progress reporting for long-running transactions:

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