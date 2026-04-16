---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following sections describe the Performance Schema tables associated with the clone plugin (see Section 7.6.7, "The Clone Plugin"). The tables provide information about cloning operations.

- clone\_status: status information about the current or last executed cloning operation.
- clone\_progress: progress information about the current or last executed cloning operation.

The Performance Schema clone tables are implemented by the clone plugin and are loaded and unloaded when that plugin is loaded and unloaded (see Section 7.6.7.1, "Installing the Clone Plugin"). No special configuration step for the tables is needed. However, the tables depend on the clone plugin being enabled. If the clone plugin is loaded but disabled, the tables are not created.

The Performance Schema clone plugin tables are used only on the recipient MySQL server instance. The data is persisted across server shutdown and restart.

### <span id="page-112-0"></span>**29.12.19.1 The clone\_status Table**

The clone\_status table shows the status of the current or last executed cloning operation only. The table only ever contains one row of data, or is empty.

The clone\_status table has these columns:

• ID

A unique cloning operation identifier in the current MySQL server instance.

• PID

Process list ID of the session executing the cloning operation.

• STATE

Current state of the cloning operation. Values include Not Started, In Progress, Completed, and Failed.

• BEGIN\_TIME

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the cloning operation started.

• END\_TIME

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the cloning operation finished. Reports NULL if the operation has not ended.

• SOURCE

The donor MySQL server address in 'HOST:PORT' format. The column displays 'LOCAL INSTANCE' for a local cloning operation.

• DESTINATION

The directory being cloned to.

• ERROR\_NO

The error number reported for a failed cloning operation.

• ERROR\_MESSAGE

The error message string for a failed cloning operation.

• BINLOG\_FILE

The name of the binary log file up to which data is cloned.

• BINLOG\_POSITION

The binary log file offset up to which data is cloned.

• GTID\_EXECUTED

The GTID value for the last cloned transaction.

The clone\_status table is read-only. DDL, including TRUNCATE TABLE, is not permitted.

### <span id="page-113-0"></span>**29.12.19.2 The clone\_progress Table**

The clone\_progress table shows progress information for the current or last executed cloning operation only.

The stages of a cloning operation include DROP DATA, FILE COPY, PAGE\_COPY, REDO\_COPY, FILE\_SYNC, RESTART, and RECOVERY. A cloning operation produces a record for each stage. The table therefore only ever contains seven rows of data, or is empty.

The clone\_progress table has these columns:

• ID

A unique cloning operation identifier in the current MySQL server instance.

• STAGE

The name of the current cloning stage. Stages include DROP DATA, FILE COPY, PAGE\_COPY, REDO\_COPY, FILE\_SYNC, RESTART, and RECOVERY.

• STATE

The current state of the cloning stage. States include Not Started, In Progress, and Completed.

• BEGIN\_TIME

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the cloning stage started. Reports NULL if the stage has not started.

• END\_TIME

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the cloning stage finished. Reports NULL if the stage has not ended.

• THREADS

The number of concurrent threads used in the stage.

• ESTIMATE

The estimated amount of data for the current stage, in bytes.

• DATA

The amount of data transferred in current state, in bytes.

• NETWORK

The amount of network data transferred in the current state, in bytes.

• DATA\_SPEED

The current actual speed of data transfer, in bytes per second. This value may differ from the requested maximum data transfer rate defined by clone\_max\_data\_bandwidth.

• NETWORK\_SPEED

The current speed of network transfer in bytes per second.

The clone\_progress table is read-only. DDL, including TRUNCATE TABLE, is not permitted.