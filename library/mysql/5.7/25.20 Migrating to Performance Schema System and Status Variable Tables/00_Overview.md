---
source: MySQL 5.7 Reference
title: 00_Overview
---

The INFORMATION\_SCHEMA has tables that contain system and status variable information (see Section 24.3.11, "The INFORMATION\_SCHEMA GLOBAL\_VARIABLES and SESSION\_VARIABLES Tables", and Section 24.3.10, "The INFORMATION\_SCHEMA GLOBAL\_STATUS and SESSION\_STATUS Tables"). The Performance Schema also contains system and status variable tables (see [Section 25.12.13, "Performance Schema System Variable Tables"](#page-71-0), and [Section 25.12.14,](#page-72-0) ["Performance Schema Status Variable Tables"\)](#page-72-0). The Performance Schema tables are intended to replace the INFORMATION\_SCHEMA tables, which are deprecated as of MySQL 5.7.6 and are removed in MySQL 8.0.

This section describes the intended migration path away from the INFORMATION\_SCHEMA system and status variable tables to the corresponding Performance Schema tables. Application developers should use this information as guidance regarding the changes required to access system and status variables in MySQL 5.7.6 and up as the INFORMATION\_SCHEMA tables become deprecated and eventually are removed.

#### **MySQL 5.6**

In MySQL 5.6, system and status variable information is available from these SHOW statements:

```
SHOW VARIABLES
SHOW STATUS
```

And from these INFORMATION\_SCHEMA tables:

```
INFORMATION_SCHEMA.GLOBAL_VARIABLES
INFORMATION_SCHEMA.SESSION_VARIABLES
INFORMATION_SCHEMA.GLOBAL_STATUS
INFORMATION_SCHEMA.SESSION_STATUS
```

#### **MySQL 5.7**

As of MySQL 5.7.6, the Performance Schema includes these tables as new sources of system and status variable information:

```
performance_schema.global_variables
performance_schema.session_variables
performance_schema.variables_by_thread
```

```
performance_schema.global_status
performance_schema.session_status
performance_schema.status_by_thread
performance_schema.status_by_account
performance_schema.status_by_host
performance_schema.status_by_user
```

MySQL 5.7.6 also adds a show\_compatibility\_56 system variable to control how the server makes system and status variable information available.

When show\_compatibility\_56 is ON, compatibility with MySQL 5.6 is enabled. The older system and status variable sources (SHOW statements, INFORMATION\_SCHEMA tables) are available with semantics identical to MySQL 5.6. Applications should run as is, with no code changes, and should see the same variable names and values as in MySQL 5.6. Warnings occur under these circumstances:

- A deprecation warning is raised when selecting from the INFORMATION\_SCHEMA tables.
- In MySQL 5.7.6 and 5.7.7, a deprecation warning is raised when using a WHERE clause with the SHOW statements. This behavior does not occur as of MySQL 5.7.8.

When show\_compatibility\_56 is OFF, compatibility with MySQL 5.6 is disabled and several changes result. Applications must be revised as follows to run properly:

• Selecting from the INFORMATION\_SCHEMA tables produces an error. Applications that access the INFORMATION\_SCHEMA tables should be revised to use the corresponding Performance Schema tables instead.

Before MySQL 5.7.9, selecting from the INFORMATION\_SCHEMA tables produces an empty result set plus a deprecation warning. This was not sufficient notice to signal the need to migrate to the corresponding Performance Schema system and status variable tables for the case that show\_compatibility\_56=OFF. Producing an error in MySQL 5.7.9 and higher makes it more evident that an application is operating under conditions that require modification, as well as where the problem lies.

In MySQL 5.7.6 and 5.7.7, the Performance Schema [session\\_variables](#page-71-0) and [session\\_status](#page-72-0) tables do not fully reflect all variable values in effect for the current session; they include no rows for global variables that have no session counterpart. This is corrected in MySQL 5.7.8.

- Output for the SHOW statements is produced using the underlying Performance Schema tables. Applications written to use these statements can still use them, but it is best to use MySQL 5.7.8 or higher. In MySQL 5.7.6 and 5.7.7, the results may differ:
  - SHOW [SESSION] VARIABLES output does not include global variables that have no session counterpart.
  - Using a WHERE clause with the SHOW statements produces an error.
- These Slave\_xxx status variables become unavailable through SHOW STATUS:

```
Slave_heartbeat_period
Slave_last_heartbeat
Slave_received_heartbeats
Slave_retried_transactions
Slave_running
```

Applications that use these status variables should be revised to obtain this information using the replication-related Performance Schema tables. For details, see Effect of show\_compatibility\_56 on Slave Status Variables.

• The Performance Schema does not collect statistics for Com\_xxx status variables in the status variable tables. To obtain global and per-session statement execution counts, use the [events\\_statements\\_summary\\_global\\_by\\_event\\_name](#page-78-0) and [events\\_statements\\_summary\\_by\\_thread\\_by\\_event\\_name](#page-78-0) tables, respectively.

#### **Migration and Privileges**

Initially, with the introduction of Performance Schema system and status variable tables in MySQL 5.7.6, access to those tables required the SELECT privilege, just as for other Performance Schema tables. However, this had the consequence that when show\_compatibility\_56=OFF, the SHOW VARIABLES and SHOW STATUS statements also required the SELECT privilege: With compatibility disabled, output for those statements was taken from the Performance Schema [global\\_variables](#page-71-0), [session\\_variables](#page-71-0), [global\\_status](#page-72-0), and [session\\_status](#page-72-0) tables.

As of MySQL 5.7.9, those Performance Schema tables are world readable and accessible without the SELECT privilege. Consequently, SHOW VARIABLES and SHOW STATUS do not require privileges on the underlying Performance Schema tables from which their output is produced when show\_compatibility\_56=OFF.

#### **Beyond MySQL 5.7**

In a MySQL 8.0, the INFORMATION\_SCHEMA variable tables and the show\_compatibility\_56 system variable are removed, and output from the SHOW statements is always based on the underlying Performance Schema tables.

Applications that have been revised to work in MySQL 5.7 when show\_compatibility\_56=OFF should work without further changes, except that it is not possible to test or set show\_compatibility\_56 because it does not exist.