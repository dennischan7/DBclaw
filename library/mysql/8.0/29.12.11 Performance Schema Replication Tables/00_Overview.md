---
source: MySQL 8.0 Reference
title: 00_Overview
---

The Performance Schema provides tables that expose replication information. This is similar to the information available from the SHOW REPLICA STATUS statement, but representation in table form is more accessible and has usability benefits:

- SHOW REPLICA STATUS output is useful for visual inspection, but not so much for programmatic use. By contrast, using the Performance Schema tables, information about replica status can be searched using general SELECT queries, including complex WHERE conditions, joins, and so forth.
- Query results can be saved in tables for further analysis, or assigned to variables and thus used in stored procedures.
- The replication tables provide better diagnostic information. For multithreaded replica operation, SHOW REPLICA STATUS reports all coordinator and worker thread errors using the Last\_SQL\_Errno and Last\_SQL\_Error fields, so only the most recent of those errors is visible and information can be lost. The replication tables store errors on a per-thread basis without loss of information.
- The last seen transaction is visible in the replication tables on a per-worker basis. This is information not available from SHOW REPLICA STATUS.
- Developers familiar with the Performance Schema interface can extend the replication tables to provide additional information by adding rows to the tables.

## **Replication Table Descriptions**

The Performance Schema provides the following replication-related tables:

- Tables that contain information about the connection of the replica to the source:
  - [replication\\_connection\\_configuration](#page-21-0): Configuration parameters for connecting to the source
  - [replication\\_connection\\_status](#page-24-0): Current status of the connection to the source
  - [replication\\_asynchronous\\_connection\\_failover](#page-19-0): Source lists for the asynchronous connection failover mechanism

- Tables that contain general (not thread-specific) information about the transaction applier:
  - [replication\\_applier\\_configuration](#page-11-0): Configuration parameters for the transaction applier on the replica.
  - [replication\\_applier\\_status](#page-13-0): Current status of the transaction applier on the replica.
- Tables that contain information about specific threads responsible for applying transactions received from the source:
  - [replication\\_applier\\_status\\_by\\_coordinator](#page-13-1): Status of the coordinator thread (empty unless the replica is multithreaded).
  - [replication\\_applier\\_status\\_by\\_worker](#page-15-0): Status of the applier thread or worker threads if the replica is multithreaded.
- Tables that contain information about channel based replication filters:
  - [replication\\_applier\\_filters](#page-18-0): Provides information about the replication filters configured on specific replication channels.
  - [replication\\_applier\\_global\\_filters](#page-18-1): Provides information about global replication filters, which apply to all replication channels.
- Tables that contain information about Group Replication members:
  - [replication\\_group\\_members](#page-29-0): Provides network and status information for group members.
  - [replication\\_group\\_member\\_stats](#page-28-0): Provides statistical information about group members and transactions in which they participate.

For more information see Section 20.4, "Monitoring Group Replication".

The following Performance Schema replication tables continue to be populated when the Performance Schema is disabled:

- [replication\\_connection\\_configuration](#page-21-0)
- [replication\\_connection\\_status](#page-24-0)
- [replication\\_asynchronous\\_connection\\_failover](#page-19-0)
- [replication\\_applier\\_configuration](#page-11-0)
- [replication\\_applier\\_status](#page-13-0)
- [replication\\_applier\\_status\\_by\\_coordinator](#page-13-1)
- [replication\\_applier\\_status\\_by\\_worker](#page-15-0)

The exception is local timing information (start and end timestamps for transactions) in the replication tables [replication\\_connection\\_status](#page-24-0), [replication\\_applier\\_status\\_by\\_coordinator](#page-13-1), and [replication\\_applier\\_status\\_by\\_worker](#page-15-0). This information is not collected when the Performance Schema is disabled.

The following sections describe each replication table in more detail, including the correspondence between the columns produced by SHOW REPLICA STATUS and the replication table columns in which the same information appears.

The remainder of this introduction to the replication tables describes how the Performance Schema populates them and which fields from SHOW REPLICA STATUS are not represented in the tables.

## **Replication Table Life Cycle**

The Performance Schema populates the replication tables as follows:

- Prior to execution of CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO, the tables are empty.
- After CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO, the configuration parameters can be seen in the tables. At this time, there are no active replication threads, so the THREAD\_ID columns are NULL and the SERVICE\_STATE columns have a value of OFF.
- After START REPLICA (or before MySQL 8.0.22, START SLAVE), non-NULL THREAD\_ID values can be seen. Threads that are idle or active have a SERVICE\_STATE value of ON. The thread that connects to the source has a value of CONNECTING while it establishes the connection, and ON thereafter as long as the connection lasts.
- After STOP REPLICA, the THREAD\_ID columns become NULL and the SERVICE\_STATE columns for threads that no longer exist have a value of OFF.
- The tables are preserved after STOP REPLICA or threads stopping due to an error.
- The [replication\\_applier\\_status\\_by\\_worker](#page-15-0) table is nonempty only when the replica is operating in multithreaded mode. That is, if the replica\_parallel\_workers or slave\_parallel\_workers system variable is greater than 0, this table is populated when START REPLICA is executed, and the number of rows shows the number of workers.

## **Replica Status Information Not In the Replication Tables**

The information in the Performance Schema replication tables differs somewhat from the information available from SHOW REPLICA STATUS because the tables are oriented toward use of global transaction identifiers (GTIDs), not file names and positions, and they represent server UUID values, not server ID values. Due to these differences, several SHOW REPLICA STATUS columns are not preserved in the Performance Schema replication tables, or are represented a different way:

• The following fields refer to file names and positions and are not preserved:

```
Master_Log_File
Read_Master_Log_Pos
Relay_Log_File
Relay_Log_Pos
Relay_Master_Log_File
Exec_Master_Log_Pos
Until_Condition
Until_Log_File
Until_Log_Pos
```

- The Master\_Info\_File field is not preserved. It refers to the master.info file used for the replica's source metadata repository, which has been superseded by the use of crash-safe tables for the repository.
- The following fields are based on server\_id, not server\_uuid, and are not preserved:

```
Master_Server_Id
Replicate_Ignore_Server_Ids
```

- The Skip\_Counter field is based on event counts, not GTIDs, and is not preserved.
- These error fields are aliases for Last\_SQL\_Errno and Last\_SQL\_Error, so they are not preserved:

```
Last_Errno
Last_Error
```

In the Performance Schema, this error information is available in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns of the [replication\\_applier\\_status\\_by\\_worker](#page-15-0) table

(and [replication\\_applier\\_status\\_by\\_coordinator](#page-13-1) if the replica is multithreaded). Those tables provide more specific per-thread error information than is available from Last\_Errno and Last\_Error.

• Fields that provide information about command-line filtering options is not preserved:

```
Replicate_Do_DB
Replicate_Ignore_DB
Replicate_Do_Table
Replicate_Ignore_Table
Replicate_Wild_Do_Table
Replicate_Wild_Ignore_Table
```

- The Replica\_IO\_State and Replica\_SQL\_Running\_State fields are not preserved. If needed, these values can be obtained from the process list by using the THREAD\_ID column of the appropriate replication table and joining it with the ID column in the INFORMATION\_SCHEMA PROCESSLIST table to select the STATE column of the latter table.
- The Executed\_Gtid\_Set field can show a large set with a great deal of text. Instead, the Performance Schema tables show GTIDs of transactions that are currently being applied by the replica. Alternatively, the set of executed GTIDs can be obtained from the value of the gtid\_executed system variable.
- The Seconds\_Behind\_Master and Relay\_Log\_Space fields are in to-be-decided status and are not preserved.

## **Replication Channels**

The first column of the replication Performance Schema tables is CHANNEL\_NAME. This enables the tables to be viewed per replication channel. In a non-multisource replication setup there is a single default replication channel. When you are using multiple replication channels on a replica, you can filter the tables per replication channel to monitor a specific replication channel. See Section 19.2.2, "Replication Channels" and Section 19.1.5.8, "Monitoring Multi-Source Replication" for more information.