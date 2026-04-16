---
source: MySQL 8.4 Reference
title: 00_Overview
---

The Performance Schema provides tables that expose replication information. This is similar to the information available from the SHOW REPLICA STATUS statement, but representation in table form is more accessible and has usability benefits:

- SHOW REPLICA STATUS output is useful for visual inspection, but not so much for programmatic use. By contrast, using the Performance Schema tables, information about replica status can be searched using general SELECT queries, including complex WHERE conditions, joins, and so forth.
- Query results can be saved in tables for further analysis, or assigned to variables and thus used in stored procedures.
- The replication tables provide better diagnostic information. For multithreaded replica operation, SHOW REPLICA STATUS reports all coordinator and worker thread errors using the Last\_SQL\_Errno and Last\_SQL\_Error fields, so only the most recent of those errors is visible and information can be lost. The replication tables store errors on a per-thread basis without loss of information.
- The last seen transaction is visible in the replication tables on a per-worker basis. This is information not available from SHOW REPLICA STATUS.

• Developers familiar with the Performance Schema interface can extend the replication tables to provide additional information by adding rows to the tables.

### **Replication Table Descriptions**

The Performance Schema provides the following replication-related tables:

- Tables that contain information about the connection of the replica to the source:
  - [replication\\_connection\\_configuration](#page-77-0): Configuration parameters for connecting to the source
  - [replication\\_connection\\_status](#page-80-0): Current status of the connection to the source
  - [replication\\_asynchronous\\_connection\\_failover](#page-74-0): Source lists for the asynchronous connection failover mechanism
- Tables that contain general (not thread-specific) information about the transaction applier:
  - [replication\\_applier\\_configuration](#page-67-0): Configuration parameters for the transaction applier on the replica.
  - [replication\\_applier\\_status](#page-69-0): Current status of the transaction applier on the replica.
- Tables that contain information about specific threads responsible for applying transactions received from the source:
  - [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1): Status of the coordinator thread (empty unless the replica is multithreaded).
  - [replication\\_applier\\_status\\_by\\_worker](#page-71-0): Status of the applier thread or worker threads if the replica is multithreaded.
- Tables that contain information about channel based replication filters:
  - [replication\\_applier\\_filters](#page-68-0): Provides information about the replication filters configured on specific replication channels.
  - [replication\\_applier\\_global\\_filters](#page-68-1): Provides information about global replication filters, which apply to all replication channels.
- Tables that contain information about Group Replication members:
  - [replication\\_group\\_members](#page-84-0): Provides network and status information for group members.
  - [replication\\_group\\_member\\_stats](#page-83-0): Provides statistical information about group members and transactions in which they participate.

For more information see Section 20.4, "Monitoring Group Replication".

The following Performance Schema replication tables continue to be populated when the Performance Schema is disabled:

- [replication\\_connection\\_configuration](#page-77-0)
- [replication\\_connection\\_status](#page-80-0)
- [replication\\_asynchronous\\_connection\\_failover](#page-74-0)
- [replication\\_applier\\_configuration](#page-67-0)
- [replication\\_applier\\_status](#page-69-0)

- [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1)
- [replication\\_applier\\_status\\_by\\_worker](#page-71-0)

The exception is local timing information (start and end timestamps for transactions) in the replication tables [replication\\_connection\\_status](#page-80-0), [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1), and [replication\\_applier\\_status\\_by\\_worker](#page-71-0). This information is not collected when the Performance Schema is disabled.

The following sections describe each replication table in more detail, including the correspondence between the columns produced by SHOW REPLICA STATUS and the replication table columns in which the same information appears.

The remainder of this introduction to the replication tables describes how the Performance Schema populates them and which fields from SHOW REPLICA STATUS are not represented in the tables.

## **Replication Table Life Cycle**

The Performance Schema populates the replication tables as follows:

- Prior to execution of CHANGE REPLICATION SOURCE TO, the tables are empty.
- After CHANGE REPLICATION SOURCE TO, the configuration parameters can be seen in the tables. At this time, there are no active replication threads, so the THREAD\_ID columns are NULL and the SERVICE\_STATE columns have a value of OFF.
- After START REPLICA, non-null THREAD\_ID values can be seen. Threads that are idle or active have a SERVICE\_STATE value of ON. The thread that connects to the source has a value of CONNECTING while it establishes the connection, and ON thereafter as long as the connection lasts.
- After STOP REPLICA, the THREAD\_ID columns become NULL and the SERVICE\_STATE columns for threads that no longer exist have a value of OFF.
- The tables are preserved after STOP REPLICA or threads stopping due to an error.
- The [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table is nonempty only when the replica is operating in multithreaded mode. That is, if the replica\_parallel\_workers system variable is greater than 0, this table is populated when START REPLICA is executed, and the number of rows shows the number of workers.

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

• The Master\_Info\_File field is not preserved. It refers to the master.info file used for the replica's source metadata repository, which has been superseded by the use of crash-safe tables for the repository.

• The following fields are based on server\_id, not server\_uuid, and are not preserved:

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

In the Performance Schema, this error information is available in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns of the [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table (and [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) if the replica is multithreaded). Those tables provide more specific per-thread error information than is available from Last\_Errno and Last\_Error.

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

### **Replication Channels**

The first column of the replication Performance Schema tables is CHANNEL\_NAME. This enables the tables to be viewed per replication channel. In a non-multisource replication setup there is a single default replication channel. When you are using multiple replication channels on a replica, you can filter the tables per replication channel to monitor a specific replication channel. See Section 19.2.2, "Replication Channels" and Section 19.1.5.8, "Monitoring Multi-Source Replication" for more information.

### <span id="page-65-0"></span>**29.12.11.1 The binary\_log\_transaction\_compression\_stats Table**

This table shows statistical information for transaction payloads written to the binary log and relay log, and can be used to calculate the effects of enabling binary log transaction compression. For information on binary log transaction compression, see Section 7.4.4.5, "Binary Log Transaction Compression".

The binary\_log\_transaction\_compression\_stats table is populated only when the server instance has a binary log, and the system variable binlog\_transaction\_compression is set to ON. The statistics cover all transactions written to the binary log and relay log from the time the server was started or the table was truncated. Compressed transactions are grouped by the compression algorithm used, and uncompressed transactions are grouped together with the compression algorithm stated as NONE, so the compression ratio can be calculated.

The binary\_log\_transaction\_compression\_stats table has these columns:

• LOG\_TYPE

Whether these transactions were written to the binary log or relay log.

• COMPRESSION\_TYPE

The compression algorithm used to compress the transaction payloads. NONE means the payloads for these transactions were not compressed, which is correct in a number of situations (see Section 7.4.4.5, "Binary Log Transaction Compression").

• TRANSACTION\_COUNTER

The number of transactions written to this log type with this compression type.

• COMPRESSED\_BYTES

The total number of bytes that were compressed and then written to this log type with this compression type, counted after compression.

• UNCOMPRESSED\_BYTES

The total number of bytes before compression for this log type and this compression type.

• COMPRESSION\_PERCENTAGE

The compression ratio for this log type and this compression type, expressed as a percentage.

• FIRST\_TRANSACTION\_ID

The ID of the first transaction that was written to this log type with this compression type.

• FIRST\_TRANSACTION\_COMPRESSED\_BYTES

The total number of bytes that were compressed and then written to the log for the first transaction, counted after compression.

• FIRST\_TRANSACTION\_UNCOMPRESSED\_BYTES

The total number of bytes before compression for the first transaction.

• FIRST\_TRANSACTION\_TIMESTAMP

The timestamp when the first transaction was written to the log.

• LAST\_TRANSACTION\_ID

The ID of the most recent transaction that was written to this log type with this compression type.

• LAST\_TRANSACTION\_COMPRESSED\_BYTES

The total number of bytes that were compressed and then written to the log for the most recent transaction, counted after compression.

• LAST\_TRANSACTION\_UNCOMPRESSED\_BYTES

The total number of bytes before compression for the most recent transaction.

• LAST\_TRANSACTION\_TIMESTAMP

The timestamp when the most recent transaction was written to the log.

The binary\_log\_transaction\_compression\_stats table has no indexes.

TRUNCATE TABLE is permitted for the binary\_log\_transaction\_compression\_stats table.

## <span id="page-67-0"></span>**29.12.11.2 The replication\_applier\_configuration Table**

This table shows the configuration parameters that affect transactions applied by the replica. Parameters stored in the table can be changed at runtime with the CHANGE REPLICATION SOURCE TO statement.

The [replication\\_applier\\_configuration](#page-67-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information.

• DESIRED\_DELAY

The number of seconds that the replica must lag the source (CHANGE REPLICATION SOURCE TO option: SOURCE\_DELAY). See Section 19.4.11, "Delayed Replication" for more information.

• PRIVILEGE\_CHECKS\_USER

The user account that provides the security context for the channel (CHANGE REPLICATION SOURCE TO option: PRIVILEGE\_CHECKS\_USER). This is escaped so that it can be copied into an SQL statement to execute individual transactions. See Section 19.3.3, "Replication Privilege Checks" for more information.

• REQUIRE\_ROW\_FORMAT

Whether the channel accepts only row-based events (CHANGE REPLICATION SOURCE TO option: REQUIRE\_ROW\_FORMAT). See Section 19.3.3, "Replication Privilege Checks" for more information.

• REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK

Whether the channel requires primary keys always, never, or according to the source's setting (CHANGE REPLICATION SOURCE TO option: REQUIRE\_TABLE\_PRIMARY\_KEY\_CHECK). See Section 19.3.3, "Replication Privilege Checks" for more information.

• ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS\_TYPE

Whether the channel assigns a GTID to replicated transactions that do not already have one (CHANGE REPLICATION SOURCE TO option: ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS). OFF means no GTIDs are assigned. LOCAL means a GTID is assigned that includes the replica's own UUID (the server\_uuid setting). UUID means a GTID is assigned that includes a manually set UUID. See Section 19.1.3.6, "Replication From a Source Without GTIDs to a Replica With GTIDs" for more information.

• ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS\_VALUE

The UUID that is used as part of the GTIDs assigned to anonymous transactions (CHANGE REPLICATION SOURCE TO option: ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS). See Section 19.1.3.6, "Replication From a Source Without GTIDs to a Replica With GTIDs" for more information.

The [replication\\_applier\\_configuration](#page-67-0) table has these indexes:

• Primary key on (CHANNEL\_NAME)

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_configuration](#page-67-0) table.

The following table shows the correspondence between [replication\\_applier\\_configuration](#page-67-0)  columns and SHOW REPLICA STATUS columns.

| replication_applier_configuration<br>Column | SHOW REPLICA STATUS Column |
|---------------------------------------------|----------------------------|
| DESIRED_DELAY                               | SQL_Delay                  |

## <span id="page-68-0"></span>**29.12.11.3 The replication\_applier\_filters Table**

This table shows the replication channel specific filters configured on this replica. Each row provides information on a replication channel's configured type of filter. The replication\_applier\_filters table has these columns:

• CHANNEL\_NAME

The name of replication channel with a replication filter configured.

• FILTER\_NAME

The type of replication filter that has been configured for this replication channel.

• FILTER\_RULE

The rules configured for the replication filter type using either --replicate-\* command options or CHANGE REPLICATION FILTER.

• CONFIGURED\_BY

The method used to configure the replication filter, can be one of:

- CHANGE\_REPLICATION\_FILTER configured by a global replication filter using a CHANGE REPLICATION FILTER statement.
- STARTUP\_OPTIONS configured by a global replication filter using a --replicate-\* option.
- CHANGE\_REPLICATION\_FILTER\_FOR\_CHANNEL configured by a channel specific replication filter using a CHANGE REPLICATION FILTER FOR CHANNEL statement.
- STARTUP\_OPTIONS\_FOR\_CHANNEL configured by a channel specific replication filter using a replicate-\* option.
- ACTIVE\_SINCE

Timestamp of when the replication filter was configured.

• COUNTER

The number of times the replication filter has been used since it was configured.

### <span id="page-68-1"></span>**29.12.11.4 The replication\_applier\_global\_filters Table**

This table shows the global replication filters configured on this replica. The replication\_applier\_global\_filters table has these columns:

• FILTER\_NAME

The type of replication filter that has been configured.

• FILTER\_RULE

The rules configured for the replication filter type using either --replicate-\* command options or CHANGE REPLICATION FILTER.

• CONFIGURED\_BY

The method used to configure the replication filter, can be one of:

- CHANGE\_REPLICATION\_FILTER configured by a global replication filter using a CHANGE REPLICATION FILTER statement.
- STARTUP\_OPTIONS configured by a global replication filter using a --replicate-\* option.
- ACTIVE\_SINCE

Timestamp of when the replication filter was configured.

### <span id="page-69-0"></span>**29.12.11.5 The replication\_applier\_status Table**

This table shows the current general transaction execution status on the replica. The table provides information about general aspects of transaction applier status that are not specific to any thread involved. Thread-specific status information is available in the [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) table (and [replication\\_applier\\_status\\_by\\_worker](#page-71-0) if the replica is multithreaded).

The [replication\\_applier\\_status](#page-69-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information.

• SERVICE\_STATE

Shows ON when the replication channel's applier threads are active or idle, OFF means that the applier threads are not active.

• REMAINING\_DELAY

If the replica is waiting for DESIRED\_DELAY seconds to pass since the source applied a transaction, this field contains the number of delay seconds remaining. At other times, this field is NULL. (The DESIRED\_DELAY value is stored in the [replication\\_applier\\_configuration](#page-67-0) table.) See Section 19.4.11, "Delayed Replication" for more information.

• COUNT\_TRANSACTIONS\_RETRIES

Shows the number of retries that were made because the replication SQL thread failed to apply a transaction. The maximum number of retries for a given transaction is set by the system variable replica\_transaction\_retries. The [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table shows detailed information on transaction retries for a single-threaded or multithreaded replica.

The [replication\\_applier\\_status](#page-69-0) table has these indexes:

• Primary key on (CHANNEL\_NAME)

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_status](#page-69-0) table.

The following table shows the correspondence between [replication\\_applier\\_status](#page-69-0) columns and SHOW REPLICA STATUS columns.

| replication_applier_status Column | SHOW REPLICA STATUS Column |
|-----------------------------------|----------------------------|
| SERVICE_STATE                     | None                       |
| REMAINING_DELAY                   | SQL_Remaining_Delay        |

# <span id="page-69-1"></span>**29.12.11.6 The replication\_applier\_status\_by\_coordinator Table**

For a multithreaded replica, the replica uses multiple worker threads and a coordinator thread to manage them, and this table shows the status of the coordinator thread. For a single-threaded replica, this table is empty. For a multithreaded replica, the [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table shows the status of the worker threads. This table provides information about the last transaction which was buffered by the coordinator thread to a worker's queue, as well as the transaction it is currently buffering. The start timestamp refers to when this thread read the first event of the transaction from the relay log to buffer it to a worker's queue, while the end timestamp refers to when the last event finished buffering to the worker's queue.

The [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information.

• THREAD\_ID

The SQL/coordinator thread ID.

• SERVICE\_STATE

ON (thread exists and is active or idle) or OFF (thread no longer exists).

• LAST\_ERROR\_NUMBER, LAST\_ERROR\_MESSAGE

The error number and error message of the most recent error that caused the SQL/coordinator thread to stop. An error number of 0 and message which is an empty string means "no error". If the LAST\_ERROR\_MESSAGE value is not empty, the error values also appear in the replica's error log.

Issuing RESET BINARY LOGS AND GTIDS or RESET REPLICA resets the values shown in these columns.

All error codes and messages displayed in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns correspond to error values listed in [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md)

• LAST\_ERROR\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the most recent SQL/coordinator error occurred.

• LAST\_PROCESSED\_TRANSACTION

The global transaction ID (GTID) of the last transaction processed by this coordinator.

• LAST\_PROCESSED\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction processed by this coordinator was committed on the original source.

• LAST\_PROCESSED\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction processed by this coordinator was committed on the immediate source.

• LAST\_PROCESSED\_TRANSACTION\_START\_BUFFER\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when this coordinator thread started writing the last transaction to the buffer of a worker thread.

• LAST\_PROCESSED\_TRANSACTION\_END\_BUFFER\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction was written to the buffer of a worker thread by this coordinator thread.

• PROCESSING\_TRANSACTION

The global transaction ID (GTID) of the transaction that this coordinator thread is currently processing.

• PROCESSING\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the currently processing transaction was committed on the original source.

• PROCESSING\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the currently processing transaction was committed on the immediate source.

• PROCESSING\_TRANSACTION\_START\_BUFFER\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when this coordinator thread started writing the currently processing transaction to the buffer of a worker thread.

When the Performance Schema is disabled, local timing information is not collected, so the fields showing the start and end timestamps for buffered transactions are zero.

The [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) table has these indexes:

- Primary key on (CHANNEL\_NAME)
- Index on (THREAD\_ID)

The following table shows the correspondence between

[replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) columns and SHOW REPLICA STATUS columns.

| replication_applier_status_by_coordinator<br>Column | SHOW REPLICA STATUS Column |
|-----------------------------------------------------|----------------------------|
| THREAD_ID                                           | None                       |
| SERVICE_STATE                                       | Replica_SQL_Running        |
| LAST_ERROR_NUMBER                                   | Last_SQL_Errno             |
| LAST_ERROR_MESSAGE                                  | Last_SQL_Error             |
| LAST_ERROR_TIMESTAMP                                | Last_SQL_Error_Timestamp   |

## <span id="page-71-0"></span>**29.12.11.7 The replication\_applier\_status\_by\_worker Table**

This table provides details of the transactions handled by applier threads on a replica or Group Replication group member. For a single-threaded replica, data is shown for the replica's single applier thread. For a multithreaded replica, data is shown individually for each applier thread. The applier threads on a multithreaded replica are sometimes called workers. The number of applier threads on a replica or Group Replication group member is set by the replica\_parallel\_workers system variable, which is set to zero for a single-threaded replica. A multithreaded replica also has a coordinator thread to manage the applier threads, and the status of this thread is shown in the [replication\\_applier\\_status\\_by\\_coordinator](#page-69-1) table.

All error codes and messages displayed in the columns relating to errors correspond to error values listed in [Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md).

When the Performance Schema is disabled, local timing information is not collected, so the fields showing the start and end timestamps for applied transactions are zero. The start timestamps in this table refer to when the worker started applying the first event, and the end timestamps refer to when the last event of the transaction was applied.

When a replica is restarted by a START REPLICA statement, the columns beginning APPLYING\_TRANSACTION are reset.

The [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information.

• WORKER\_ID

The worker identifier (same value as the id column in the mysql.slave\_worker\_info table). After STOP REPLICA, the THREAD\_ID column becomes NULL, but the WORKER\_ID value is preserved.

• THREAD\_ID

The worker thread ID.

• SERVICE\_STATE

ON (thread exists and is active or idle) or OFF (thread no longer exists).

• LAST\_ERROR\_NUMBER, LAST\_ERROR\_MESSAGE

The error number and error message of the most recent error that caused the worker thread to stop. An error number of 0 and message of the empty string mean "no error". If the LAST\_ERROR\_MESSAGE value is not empty, the error values also appear in the replica's error log.

Issuing RESET BINARY LOGS AND GTIDS or RESET REPLICA resets the values shown in these columns.

• LAST\_ERROR\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the most recent worker error occurred.

• LAST\_APPLIED\_TRANSACTION

The global transaction ID (GTID) of the last transaction applied by this worker.

• LAST\_APPLIED\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction applied by this worker was committed on the original source.

• LAST\_APPLIED\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction applied by this worker was committed on the immediate source.

• LAST\_APPLIED\_TRANSACTION\_START\_APPLY\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when this worker started applying the last applied transaction.

• LAST\_APPLIED\_TRANSACTION\_END\_APPLY\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when this worker finished applying the last applied transaction.

• APPLYING\_TRANSACTION

The global transaction ID (GTID) of the transaction this worker is currently applying.

• APPLYING\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the transaction this worker is currently applying was committed on the original source.

• APPLYING\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the transaction this worker is currently applying was committed on the immediate source.

• APPLYING\_TRANSACTION\_START\_APPLY\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when this worker started its first attempt to apply the transaction that is currently being applied.

• LAST\_APPLIED\_TRANSACTION\_RETRIES\_COUNT

The number of times the last applied transaction was retried by the worker after the first attempt. If the transaction was applied at the first attempt, this number is zero.

• LAST\_APPLIED\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_NUMBER

The error number of the last transient error that caused the transaction to be retried.

• LAST\_APPLIED\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_MESSAGE

The message text for the last transient error that caused the transaction to be retried.

• LAST\_APPLIED\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format for the last transient error that caused the transaction to be retried.

• APPLYING\_TRANSACTION\_RETRIES\_COUNT

The number of times the transaction that is currently being applied was retried until this moment. If the transaction was applied at the first attempt, this number is zero.

• APPLYING\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_NUMBER

The error number of the last transient error that caused the current transaction to be retried.

• APPLYING\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_MESSAGE

The message text for the last transient error that caused the current transaction to be retried.

• APPLYING\_TRANSACTION\_LAST\_TRANSIENT\_ERROR\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format for the last transient error that caused the current transaction to be retried.

The [replication\\_applier\\_status\\_by\\_worker](#page-71-0) table has these indexes:

• Primary key on (CHANNEL\_NAME, WORKER\_ID)

• Index on (THREAD\_ID)

The following table shows the correspondence between

[replication\\_applier\\_status\\_by\\_worker](#page-71-0) columns and SHOW REPLICA STATUS columns.

| replication_applier_status_by_worker<br>Column | SHOW REPLICA STATUS Column |
|------------------------------------------------|----------------------------|
| WORKER_ID                                      | None                       |
| THREAD_ID                                      | None                       |
| SERVICE_STATE                                  | None                       |
| LAST_ERROR_NUMBER                              | Last_SQL_Errno             |
| LAST_ERROR_MESSAGE                             | Last_SQL_Error             |
| LAST_ERROR_TIMESTAMP                           | Last_SQL_Error_Timestamp   |

## <span id="page-74-0"></span>**29.12.11.8 The replication\_asynchronous\_connection\_failover Table**

This table holds the replica's source lists for each replication channel for the asynchronous connection failover mechanism. The asynchronous connection failover mechanism automatically establishes an asynchronous (source to replica) replication connection to a new source from the appropriate list after the existing connection from the replica to its source fails. When asynchronous connection failover is enabled for a group of replicas managed by Group Replication, the source lists are broadcast to all group members when they join, and also when the lists change.

You set and manage source lists using the asynchronous\_connection\_failover\_add\_source and asynchronous\_connection\_failover\_delete\_source functions to add and remove replication source servers from the source list for a replication channel. To add and remove managed groups of servers, use the asynchronous\_connection\_failover\_add\_managed and asynchronous\_connection\_failover\_delete\_managed functions instead.

For more information, see Section 19.4.9, "Switching Sources and Replicas with Asynchronous Connection Failover".

The [replication\\_asynchronous\\_connection\\_failover](#page-74-0) table has these columns:

• CHANNEL\_NAME

The replication channel for which this replication source server is part of the source list. If this channel's connection to its current source fails, this replication source server is one of its potential new sources.

• HOST

The host name for this replication source server.

• PORT

The port number for this replication source server.

• NETWORK\_NAMESPACE

The network namespace for this replication source server. If this value is empty, connections use the default (global) namespace.

• WEIGHT

The priority of this replication source server in the replication channel's source list. The weight is from 1 to 100, with 100 being the highest, and 50 being the default. When the asynchronous connection failover mechanism activates, the source with the highest weight setting among the alternative sources listed in the source list for the channel is chosen for the first connection attempt. If this

attempt does not work, the replica tries with all the listed sources in descending order of weight, then starts again from the highest weighted source. If multiple sources have the same weight, the replica orders them randomly.

• MANAGED\_NAME

The identifier for the managed group that the server is a part of. For the GroupReplication managed service, the identifier is the value of the group\_replication\_group\_name system variable.

The [replication\\_asynchronous\\_connection\\_failover](#page-74-0) table has these indexes:

• Primary key on (CHANNEL\_NAME, HOST, PORT, NETWORK\_NAMESPACE, MANAGED\_NAME)

TRUNCATE TABLE is not permitted for the [replication\\_asynchronous\\_connection\\_failover](#page-74-0) table.

## <span id="page-75-0"></span>**29.12.11.9 The replication\_asynchronous\_connection\_failover\_managed Table**

This table holds configuration information used by the replica's asynchronous connection failover mechanism to handle managed groups, including Group Replication topologies.

When you add a group member to the source list and define it as part of a managed group, the asynchronous connection failover mechanism updates the source list to keep it in line with membership changes, adding and removing group members automatically as they join or leave. When asynchronous connection failover is enabled for a group of replicas managed by Group Replication, the source lists are broadcast to all group members when they join, and also when the lists change.

The asynchronous connection failover mechanism fails over the connection if another available server on the source list has a higher priority (weight) setting. For a managed group, a source's weight is assigned depending on whether it is a primary or a secondary server. So assuming that you set up the managed group to give a higher weight to a primary and a lower weight to a secondary, when the primary changes, the higher weight is assigned to the new primary, so the replica changes over the connection to it. The asynchronous connection failover mechanism additionally changes connection if the currently connected managed source server leaves the managed group, or is no longer in the majority in the managed group. For more information, see Section 19.4.9, "Switching Sources and Replicas with Asynchronous Connection Failover".

The [replication\\_asynchronous\\_connection\\_failover\\_managed](#page-75-0) table has these columns:

• CHANNEL\_NAME

The replication channel where the servers for this managed group operate.

• MANAGED\_NAME

The identifier for the managed group. For the GroupReplication managed service, the identifier is the value of the group\_replication\_group\_name system variable.

• MANAGED\_TYPE

The type of managed service that the asynchronous connection failover mechanism provides for this group. The only value currently available is GroupReplication.

• CONFIGURATION

The configuration information for this managed group. For the GroupReplication managed service, the configuration shows the weights assigned to the group's primary server and to the group's secondary servers. For example: {"Primary\_weight": 80, "Secondary\_weight": 60}

• Primary\_weight: Integer between 0 and 100. Default value is 80.

• Secondary\_weight: Integer between 0 and 100. Default value is 60.

The [replication\\_asynchronous\\_connection\\_failover\\_managed](#page-75-0) table has these indexes:

• Primary key on (CHANNEL\_NAME, MANAGED\_NAME)

TRUNCATE TABLE is not permitted for the [replication\\_asynchronous\\_connection\\_failover\\_managed](#page-75-0) table.

## <span id="page-76-0"></span>**29.12.11.10 The replication\_group\_communication\_information Table**

This table shows group configuration options for the whole replication group. The table is available only when Group Replication is installed.

The replication\_group\_communication\_information table has these columns:

• WRITE\_CONCURRENCY

The maximum number of consensus instances that the group can execute in parallel. The default value is 10. See Section 20.5.1.3, "Using Group Replication Group Write Consensus".

• PROTOCOL\_VERSION

The Group Replication communication protocol version, which determines what messaging capabilities are used. This is set to accommodate the oldest MySQL Server version that you want the group to support. See Section 20.5.1.4, "Setting a Group's Communication Protocol Version".

• WRITE\_CONSENSUS\_LEADERS\_PREFERRED

The leader or leaders that Group Replication has instructed the group communication engine to use to drive consensus. For a group in single-primary mode with the group\_replication\_paxos\_single\_leader system variable set to ON and the communication protocol version set to 8.0.27 or later, the single consensus leader is the group's primary. Otherwise, all group members are used as leaders, so they are all shown here. See Section 20.7.3, "Single Consensus Leader".

• WRITE\_CONSENSUS\_LEADERS\_ACTUAL

The actual leader or leader that the group communication engine is using to drive consensus. If a single consensus leader is in use for the group, and the primary is currently unhealthy, the group communication selects an alternative consensus leader. In this situation, the group member specified here can differ from the preferred group member.

• WRITE\_CONSENSUS\_SINGLE\_LEADER\_CAPABLE

Whether the replication group is capable of using a single consensus leader. 1 means that the group was started with the use of a single leader enabled (group\_replication\_paxos\_single\_leader = ON), and this is still shown if the value of group\_replication\_paxos\_single\_leader has since been changed on this group member. 0 means that the group was started with single leader mode disabled (group\_replication\_paxos\_single\_leader = OFF), or has a Group Replication communication protocol version that does not support the use of a single consensus leader (prior to 8.0.27). This information is only returned for group members in ONLINE or RECOVERING state.

• MEMBER\_FAILURE\_SUSPICIONS\_COUNT

{

The address of each group member paired with the number of times this member has been seen as suspect by the local node. This information is displayed in JSON format. For a group with three members, the value of this column should appear similar to what is shown here:

4847

```
 "d57da302-e404-4395-83b5-ff7cf9b7e055": 0,
 "6ace9d39-a093-4fe0-b24d-bacbaa34c339": 10,
 "9689c7c5-c71c-402a-a3a1-2f57bfc2ca62": 0
}
```

The replication\_group\_communication\_information table has no indexes.

TRUNCATE TABLE is not permitted for the replication\_group\_communication\_information table.

## <span id="page-77-0"></span>**29.12.11.11 The replication\_connection\_configuration Table**

This table shows the configuration parameters used by the replica for connecting to the source. Parameters stored in the table can be changed at runtime with the CHANGE REPLICATION SOURCE TO statement.

Compared to the [replication\\_connection\\_status](#page-80-0) table, [replication\\_connection\\_configuration](#page-77-0) changes less frequently. It contains values that define how the replica connects to the source and that remain constant during the connection, whereas [replication\\_connection\\_status](#page-80-0) contains values that change during the connection.

The [replication\\_connection\\_configuration](#page-77-0) table has the following columns. The column descriptions indicate the corresponding CHANGE REPLICATION SOURCE TO options from which the column values are taken, and the table given later in this section shows the correspondence between [replication\\_connection\\_configuration](#page-77-0) columns and SHOW REPLICA STATUS columns.

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information. (CHANGE REPLICATION SOURCE TO option: FOR CHANNEL)

• HOST

The host name of the source that the replica is connected to. (CHANGE REPLICATION SOURCE TO option: SOURCE\_HOST)

• PORT

The port used to connect to the source. (CHANGE REPLICATION SOURCE TO option: SOURCE\_PORT)

• USER

The user name of the replication user account used to connect to the source. (CHANGE REPLICATION SOURCE TO option: SOURCE\_USER)

• NETWORK\_INTERFACE

The network interface that the replica is bound to, if any. (CHANGE REPLICATION SOURCE TO option: SOURCE\_BIND)

• AUTO\_POSITION

1 if GTID auto-positioning is in use; otherwise 0. (CHANGE REPLICATION SOURCE TO option: SOURCE\_AUTO\_POSITION)

• SSL\_ALLOWED, SSL\_CA\_FILE, SSL\_CA\_PATH, SSL\_CERTIFICATE, SSL\_CIPHER, SSL\_KEY, SSL\_VERIFY\_SERVER\_CERTIFICATE, SSL\_CRL\_FILE, SSL\_CRL\_PATH

These columns show the SSL parameters used by the replica to connect to the source, if any.

SSL\_ALLOWED has these values:

- Yes if an SSL connection to the source is permitted
- No if an SSL connection to the source is not permitted
- Ignored if an SSL connection is permitted but the replica does not have SSL support enabled

(CHANGE REPLICATION SOURCE TO options for the other SSL columns: SOURCE\_SSL\_CA, SOURCE\_SSL\_CAPATH, SOURCE\_SSL\_CERT, SOURCE\_SSL\_CIPHER, SOURCE\_SSL\_CRL, SOURCE\_SSL\_CRLPATH, SOURCE\_SSL\_KEY, SOURCE\_SSL\_VERIFY\_SERVER\_CERT)

• CONNECTION\_RETRY\_INTERVAL

The number of seconds between connect retries. (CHANGE REPLICATION SOURCE TO option: SOURCE\_CONNECT\_RETRY)

• CONNECTION\_RETRY\_COUNT

The number of times the replica can attempt to reconnect to the source in the event of a lost connection. (CHANGE REPLICATION SOURCE TO option: SOURCE\_RETRY\_COUNT)

• HEARTBEAT\_INTERVAL

The replication heartbeat interval on a replica, measured in seconds. (CHANGE REPLICATION SOURCE TO option: SOURCE\_HEARTBEAT\_PERIOD)

• TLS\_VERSION

The list of TLS protocol versions that are permitted by the replica for the replication connection. For TLS version information, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". (CHANGE REPLICATION SOURCE TO option: SOURCE\_TLS\_VERSION)

• TLS\_CIPHERSUITES

The list of ciphersuites that are permitted by the replica for the replication connection. For TLS ciphersuite information, see Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". (CHANGE REPLICATION SOURCE TO option: SOURCE\_TLS\_CIPHERSUITES)

• PUBLIC\_KEY\_PATH

The path name to a file containing a replica-side copy of the public key required by the source for RSA key pair-based password exchange. The file must be in PEM format. This column applies to replicas that authenticate with the sha256\_password (deprecated) or caching\_sha2\_password authentication plugin. (CHANGE REPLICATION SOURCE TO option: SOURCE\_PUBLIC\_KEY\_PATH)

If PUBLIC\_KEY\_PATH is given and specifies a valid public key file, it takes precedence over GET\_PUBLIC\_KEY.

• GET\_PUBLIC\_KEY

Whether to request from the source the public key required for RSA key pair-based password exchange. This column applies to replicas that authenticate with the caching\_sha2\_password authentication plugin. For that plugin, the source does not send the public key unless requested. (CHANGE REPLICATION SOURCE TO option: GET\_SOURCE\_PUBLIC\_KEY)

If PUBLIC\_KEY\_PATH is given and specifies a valid public key file, it takes precedence over GET\_PUBLIC\_KEY.

• NETWORK\_NAMESPACE

The network namespace name; empty if the connection uses the default (global) namespace. For information about network namespaces, see Section 7.1.14, "Network Namespace Support".

• COMPRESSION\_ALGORITHM

The permitted compression algorithms for connections to the source. (CHANGE REPLICATION SOURCE TO option: SOURCE\_COMPRESSION\_ALGORITHMS)

For more information, see Section 6.2.8, "Connection Compression Control".

• ZSTD\_COMPRESSION\_LEVEL

The compression level to use for connections to the source that use the zstd compression algorithm. (CHANGE REPLICATION SOURCE TO option: SOURCE\_ZSTD\_COMPRESSION\_LEVEL)

For more information, see Section 6.2.8, "Connection Compression Control".

• SOURCE\_CONNECTION\_AUTO\_FAILOVER

Whether the asynchronous connection failover mechanism is activated for this replication channel. (CHANGE REPLICATION SOURCE TO option: SOURCE\_CONNECTION\_AUTO\_FAILOVER)

For more information, see Section 19.4.9, "Switching Sources and Replicas with Asynchronous Connection Failover".

• GTID\_ONLY

Indicates if this channel only uses GTIDs for the transaction queueing and application process and for recovery, and does not persist binary log and relay log file names and file positions in the replication metadata repositories. (CHANGE REPLICATION SOURCE TO option: GTID\_ONLY)

For more information, see Section 20.4.1, "GTIDs and Group Replication".

The [replication\\_connection\\_configuration](#page-77-0) table has these indexes:

• Primary key on (CHANNEL\_NAME)

TRUNCATE TABLE is not permitted for the [replication\\_connection\\_configuration](#page-77-0) table.

#### The following table shows the correspondence between

[replication\\_connection\\_configuration](#page-77-0) columns and SHOW REPLICA STATUS columns.

| replication_connection_configuration<br>Column | SHOW REPLICA STATUS Column    |
|------------------------------------------------|-------------------------------|
| CHANNEL_NAME                                   | Channel_name                  |
| HOST                                           | Source_Host                   |
| PORT                                           | Source_Port                   |
| USER                                           | Source_User                   |
| NETWORK_INTERFACE                              | Source_Bind                   |
| AUTO_POSITION                                  | Auto_Position                 |
| SSL_ALLOWED                                    | Source_SSL_Allowed            |
| SSL_CA_FILE                                    | Source_SSL_CA_File            |
| SSL_CA_PATH                                    | Source_SSL_CA_Path            |
| SSL_CERTIFICATE                                | Source_SSL_Cert               |
| SSL_CIPHER                                     | Source_SSL_Cipher             |
| SSL_KEY                                        | Source_SSL_Key                |
| SSL_VERIFY_SERVER_CERTIFICATE                  | Source_SSL_Verify_Server_Cert |
| SSL_CRL_FILE                                   | Source_SSL_Crl                |

| replication_connection_configuration<br>Column | SHOW REPLICA STATUS Column |
|------------------------------------------------|----------------------------|
| SSL_CRL_PATH                                   | Source_SSL_Crlpath         |
| CONNECTION_RETRY_INTERVAL                      | Source_Connect_Retry       |
| CONNECTION_RETRY_COUNT                         | Source_Retry_Count         |
| HEARTBEAT_INTERVAL                             | None                       |
| TLS_VERSION                                    | Source_TLS_Version         |
| PUBLIC_KEY_PATH                                | Source_public_key_path     |
| GET_PUBLIC_KEY                                 | Get_source_public_key      |
| NETWORK_NAMESPACE                              | Network_Namespace          |
| COMPRESSION_ALGORITHM                          | [None]                     |
| ZSTD_COMPRESSION_LEVEL                         | [None]                     |
| GTID_ONLY                                      | [None]                     |

### <span id="page-80-1"></span>**29.12.11.12 The replication\_group\_configuration\_version Table**

This table displays the version of the member actions configuration for replication group members. The table is available only when Group Replication is installed. Whenever a member action is enabled or disabled using the group\_replication\_enable\_member\_action() and group\_replication\_disable\_member\_action() functions, the version number is incremented. You can reset the member actions configuration using the group\_replication\_reset\_member\_actions() function, which resets the member actions configuration to the default settings, and resets its version number to 1. For more information, see Section 20.5.1.5, "Configuring Member Actions".

The replication\_group\_configuration\_version table has these columns:

• NAME

The name of the configuration.

• VERSION

The version number of the configuration.

The replication\_group\_configuration\_version table has no indexes.

TRUNCATE TABLE is not permitted for the replication\_group\_configuration\_version table.

### <span id="page-80-0"></span>**29.12.11.13 The replication\_connection\_status Table**

This table shows the current status of the I/O thread that handles the replica's connection to the source, information on the last transaction queued in the relay log, and information on the transaction currently being queued in the relay log.

Compared to the [replication\\_connection\\_configuration](#page-77-0) table, [replication\\_connection\\_status](#page-80-0) changes more frequently. It contains values that change during the connection, whereas [replication\\_connection\\_configuration](#page-77-0) contains values which define how the replica connects to the source and that remain constant during the connection.

The [replication\\_connection\\_status](#page-80-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 19.2.2, "Replication Channels" for more information.

• GROUP\_NAME

If this server is a member of a group, shows the name of the group the server belongs to.

• SOURCE\_UUID

The server\_uuid value from the source.

• THREAD\_ID

The I/O thread ID.

• SERVICE\_STATE

ON (thread exists and is active or idle), OFF (thread no longer exists), or CONNECTING (thread exists and is connecting to the source).

• RECEIVED\_TRANSACTION\_SET

The set of global transaction IDs (GTIDs) corresponding to all transactions received by this replica. Empty if GTIDs are not in use. See GTID Sets for more information.

• LAST\_ERROR\_NUMBER, LAST\_ERROR\_MESSAGE

The error number and error message of the most recent error that caused the I/O thread to stop. An error number of 0 and message of the empty string mean "no error." If the LAST\_ERROR\_MESSAGE value is not empty, the error values also appear in the replica's error log.

Issuing RESET BINARY LOGS AND GTIDS or RESET REPLICA resets the values shown in these columns.

• LAST\_ERROR\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the most recent I/O error took place.

• LAST\_HEARTBEAT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the most recent heartbeat signal was received by a replica.

• COUNT\_RECEIVED\_HEARTBEATS

The total number of heartbeat signals that a replica received since the last time it was restarted or reset, or a CHANGE REPLICATION SOURCE TO statement was issued.

• LAST\_QUEUED\_TRANSACTION

The global transaction ID (GTID) of the last transaction that was queued to the relay log.

• LAST\_QUEUED\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction queued in the relay log was committed on the original source.

• LAST\_QUEUED\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction queued in the relay log was committed on the immediate source.

• LAST\_QUEUED\_TRANSACTION\_START\_QUEUE\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction was placed in the relay log queue by this I/O thread.

• LAST\_QUEUED\_TRANSACTION\_END\_QUEUE\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the last transaction was queued to the relay log files.

• QUEUEING\_TRANSACTION

The global transaction ID (GTID) of the currently queueing transaction in the relay log.

• QUEUEING\_TRANSACTION\_ORIGINAL\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the currently queueing transaction was committed on the original source.

• QUEUEING\_TRANSACTION\_IMMEDIATE\_COMMIT\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the currently queueing transaction was committed on the immediate source.

• QUEUEING\_TRANSACTION\_START\_QUEUE\_TIMESTAMP

A timestamp in 'YYYY-MM-DD hh:mm:ss[.fraction]' format that shows when the first event of the currently queueing transaction was written to the relay log by this I/O thread.

When the Performance Schema is disabled, local timing information is not collected, so the fields showing the start and end timestamps for queued transactions are zero.

The [replication\\_connection\\_status](#page-80-0) table has these indexes:

- Primary key on (CHANNEL\_NAME)
- Index on (THREAD\_ID)

The following table shows the correspondence between [replication\\_connection\\_status](#page-80-0) columns and SHOW REPLICA STATUS columns.

| replication_connection_status Column | SHOW REPLICA STATUS Column |
|--------------------------------------|----------------------------|
| SOURCE_UUID                          | Master_UUID                |
| THREAD_ID                            | None                       |
| SERVICE_STATE                        | Replica_IO_Running         |
| RECEIVED_TRANSACTION_SET             | Retrieved_Gtid_Set         |
| LAST_ERROR_NUMBER                    | Last_IO_Errno              |
| LAST_ERROR_MESSAGE                   | Last_IO_Error              |
| LAST_ERROR_TIMESTAMP                 | Last_IO_Error_Timestamp    |

### <span id="page-82-0"></span>**29.12.11.14 The replication\_group\_member\_actions Table**

This table lists the member actions that are included in the member actions configuration for replication group members. The table is available only when Group Replication is installed. You can reset the member actions configuration using the group\_replication\_reset\_member\_actions() function. For more information, see Section 20.5.1.5, "Configuring Member Actions".

The replication\_group\_member\_actions table has these columns:

• NAME

The name of the member action.

• EVENT

The event that triggers the member action.

• ENABLED

Whether the member action is currently enabled. Member actions can be enabled using the group\_replication\_enable\_member\_action() function and disabled using the group\_replication\_disable\_member\_action() function.

• TYPE

The type of member action. INTERNAL is an action that is provided by the Group Replication plugin.

• PRIORITY

The priority of the member action. Actions with lower priority values are actioned first.

• ERROR\_HANDLING

The action that Group Replication takes if an error occurs when the member action is being carried out. IGNORE means that an error message is logged to say that the member action failed, but no further action is taken. CRITICAL means that the member moves into ERROR state, and takes the action specified by the group\_replication\_exit\_state\_action system variable.

The replication\_group\_member\_actions table has no indexes.

TRUNCATE TABLE is not permitted for the replication\_group\_member\_actions table.

### <span id="page-83-0"></span>**29.12.11.15 The replication\_group\_member\_stats Table**

This table shows statistical information for replication group members. It is populated only when Group Replication is running.

The replication\_group\_member\_stats table has these columns:

• CHANNEL\_NAME

Name of the Group Replication channel

• VIEW\_ID

Current view identifier for this group.

• MEMBER\_ID

The member server UUID. This has a different value for each member in the group. This also serves as a key because it is unique to each member.

• COUNT\_TRANSACTIONS\_IN\_QUEUE

The number of transactions in the queue pending conflict detection checks. Once the transactions have been checked for conflicts, if they pass the check, they are queued to be applied as well.

• COUNT\_TRANSACTIONS\_CHECKED

The number of transactions that have been checked for conflicts.

• COUNT\_CONFLICTS\_DETECTED

The number of transactions that have not passed the conflict detection check.

• COUNT\_TRANSACTIONS\_ROWS\_VALIDATING

Number of transaction rows which can be used for certification, but have not been garbage collected. Can be thought of as the current size of the conflict detection database against which each transaction is certified.

• TRANSACTIONS\_COMMITTED\_ALL\_MEMBERS

The transactions that have been successfully committed on all members of the replication group, shown as GTID Sets. This is updated at a fixed time interval.

• LAST\_CONFLICT\_FREE\_TRANSACTION

The transaction identifier of the last conflict free transaction which was checked.

• COUNT\_TRANSACTIONS\_REMOTE\_IN\_APPLIER\_QUEUE

The number of transactions that this member has received from the replication group which are waiting to be applied.

• COUNT\_TRANSACTIONS\_REMOTE\_APPLIED

Number of transactions this member has received from the group and applied.

• COUNT\_TRANSACTIONS\_LOCAL\_PROPOSED

Number of transactions which originated on this member and were sent to the group.

• COUNT\_TRANSACTIONS\_LOCAL\_ROLLBACK

Number of transactions which originated on this member and were rolled back by the group.

The [replication\\_group\\_member\\_stats](#page-83-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [replication\\_group\\_member\\_stats](#page-83-0) table.

### <span id="page-84-0"></span>**29.12.11.16 The replication\_group\_members Table**

This table shows network and status information for replication group members. The network addresses shown are the addresses used to connect clients to the group, and should not be confused with the member's internal group communication address specified by group\_replication\_local\_address.

The [replication\\_group\\_members](#page-84-0) table has these columns:

• CHANNEL\_NAME

Name of the Group Replication channel.

• MEMBER\_ID

The member server UUID. This has a different value for each member in the group. This also serves as a key because it is unique to each member.

• MEMBER\_HOST

Network address of this member (host name or IP address). Retrieved from the member's hostname variable. This is the address which clients connect to, unlike the group\_replication\_local\_address which is used for internal group communication.

• MEMBER\_PORT

Port on which the server is listening. Retrieved from the member's port variable.

• MEMBER\_STATE

Current state of this member; can be any one of the following:

- ONLINE: The member is in a fully functioning state.
- RECOVERING: The server has joined a group from which it is retrieving data.
- OFFLINE: The group replication plugin is installed but has not been started.
- ERROR: The member has encountered an error, either during applying transactions or during the recovery phase, and is not participating in the group's transactions.
- UNREACHABLE: The failure detection process suspects that this member cannot be contacted, because the group messages have timed out.

See Section 20.4.2, "Group Replication Server States".

• MEMBER\_ROLE

Role of the member in the group, either PRIMARY or SECONDARY.

• MEMBER\_VERSION

MySQL version of the member.

• MEMBER\_COMMUNICATION\_STACK

The communication stack used for the group, either the XCOM communication stack or the MYSQL communication stack.

The [replication\\_group\\_members](#page-84-0) table has no indexes.

TRUNCATE TABLE is not permitted for the [replication\\_group\\_members](#page-84-0) table.