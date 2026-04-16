---
source: MySQL 5.7 Reference
title: 00_Overview
---

The Performance Schema provides tables that expose replication information. This is similar to the information available from the SHOW SLAVE STATUS statement, but representation in table form is more accessible and has usability benefits:

- SHOW SLAVE STATUS output is useful for visual inspection, but not so much for programmatic use. By contrast, using the Performance Schema tables, information about replica status can be searched using general SELECT queries, including complex WHERE conditions, joins, and so forth.
- Query results can be saved in tables for further analysis, or assigned to variables and thus used in stored procedures.
- The replication tables provide better diagnostic information. For multithreaded replica operation, SHOW SLAVE STATUS reports all coordinator and worker thread errors using the Last\_SQL\_Errno and Last\_SQL\_Error fields, so only the most recent of those errors is visible and information can be lost. The replication tables store errors on a per-thread basis without loss of information.
- The last seen transaction is visible in the replication tables on a per-worker basis. This is information not avilable from SHOW SLAVE STATUS.
- Developers familiar with the Performance Schema interface can extend the replication tables to provide additional information by adding rows to the tables.

## **Replication Table Descriptions**

The Performance Schema provides the following replication-related tables:

- Tables that contain information about the connection of a replica to the replication source server:
  - [replication\\_connection\\_configuration](#page-59-0): Configuration parameters for connecting to the source
  - [replication\\_connection\\_status](#page-61-0): Current status of the connection to the source
- Tables that contain general (not thread-specific) information about the transaction applier:
  - [replication\\_applier\\_configuration](#page-62-0): Configuration parameters for the transaction applier on the replica.
  - [replication\\_applier\\_status](#page-63-0): Current status of the transaction applier on the replica.
- Tables that contain information about specific threads responsible for applying transactions received from the source:
  - [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1): Status of the coordinator thread (empty unless the replica is multithreaded).
  - [replication\\_applier\\_status\\_by\\_worker](#page-64-0): Status of the applier thread or worker threads if the replica is multithreaded.
- Tables that contain information about replication group members:
  - [replication\\_group\\_members](#page-66-1): Provides network and status information for group members.
  - [replication\\_group\\_member\\_stats](#page-66-0): Provides statistical information about group members and transaction in which they participate.

The following sections describe each replication table in more detail, including the correspondence between the columns produced by SHOW SLAVE STATUS and the replication table columns in which the same information appears.

The remainder of this introduction to the replication tables describes how the Performance Schema populates them and which fields from SHOW SLAVE STATUS are not represented in the tables.

## **Replication Table Life Cycle**

The Performance Schema populates the replication tables as follows:

- Prior to execution of CHANGE MASTER TO, the tables are empty.
- After CHANGE MASTER TO, the configuration parameters can be seen in the tables. At this time, there are no active replica threads, so the THREAD\_ID columns are NULL and the SERVICE\_STATE columns have a value of OFF.
- After START SLAVE, non-NULL THREAD\_ID values can be seen. Threads that are idle or active have a SERVICE\_STATE value of ON. The thread that connects to the source has a value of CONNECTING while it establishes the connection, and ON thereafter as long as the connection lasts.
- After STOP SLAVE, the THREAD\_ID columns become NULL and the SERVICE\_STATE columns for threads that no longer exist have a value of OFF.
- The tables are preserved after STOP SLAVE or threads dying due to an error.
- The [replication\\_applier\\_status\\_by\\_worker](#page-64-0) table is nonempty only when the replica is operating in multithreaded mode. That is, if the slave\_parallel\_workers system variable is

greater than 0, this table is populated when START SLAVE is executed, and the number of rows shows the number of workers.

## **SHOW SLAVE STATUS Information Not In the Replication Tables**

The information in the Performance Schema replication tables differs somewhat from the information available from SHOW SLAVE STATUS because the tables are oriented toward use of global transaction identifiers (GTIDs), not file names and positions, and they represent server UUID values, not server ID values. Due to these differences, several SHOW SLAVE STATUS columns are not preserved in the Performance Schema replication tables, or are represented a different way:

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

- The Master\_Info\_File field is not preserved. It refers to the master.info file, which has been superseded by crash-safe tables.
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

In the Performance Schema, this error information is available in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns of the [replication\\_applier\\_status\\_by\\_worker](#page-64-0) table (and [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) if the replica is multithreaded). Those tables provide more specific per-thread error information than is available from Last\_Errno and Last\_Error.

• Fields that provide information about command-line filtering options is not preserved:

```
Replicate_Do_DB
Replicate_Ignore_DB
Replicate_Do_Table
Replicate_Ignore_Table
Replicate_Wild_Do_Table
Replicate_Wild_Ignore_Table
```

- The Slave\_IO\_State and Slave\_SQL\_Running\_State fields are not preserved. If needed, these values can be obtained from the process list by using the THREAD\_ID column of the appropriate replication table and joining it with the ID column in the INFORMATION\_SCHEMA PROCESSLIST table to select the STATE column of the latter table.
- The Executed\_Gtid\_Set field can show a large set with a great deal of text. Instead, the Performance Schema tables show GTIDs of transactions that are currently being applied by the replica. Alternatively, the set of executed GTIDs can be obtained from the value of the gtid\_executed system variable.
- The Seconds\_Behind\_Master and Relay\_Log\_Space fields are in to-be-decided status and are not preserved.

## **Status Variables Moved to Replication Tables**

As of MySQL version 5.7.5, the following status variables (previously monitored using SHOW STATUS) were moved to the Perfomance Schema replication tables:

- Slave\_retried\_transactions
- Slave\_last\_heartbeat
- Slave\_received\_heartbeats
- Slave\_heartbeat\_period
- Slave\_running

These status variables are now only relevant when a single replication channel is being used because they only report the status of the default replication channel. When multiple replication channels exist, use the Performance Schema replication tables described in this section, which report these variables for each existing replication channel.

## **Replication Channels**

The first column of the replication Performance Schema tables is CHANNEL\_NAME. This enables the tables to be viewed per replication channel. In a non-multisource replication setup there is a single default replication channel. When you are using multiple replication channels on a replica, you can filter the tables per replication channel to monitor a specific replication channel. See Section 16.2.2, "Replication Channels" and Section 16.1.5.8, "Multi-Source Replication Monitoring" for more information.

## <span id="page-59-0"></span>**25.12.11.1 The replication\_connection\_configuration Table**

This table shows the configuration parameters used by the replica for connecting to the source. Parameters stored in the table can be changed at runtime with the CHANGE MASTER TO statement, as indicated in the column descriptions.

Compared to the [replication\\_connection\\_status](#page-61-0) table, [replication\\_connection\\_configuration](#page-59-0) changes less frequently. It contains values that define how the replica connects to the source and that remain constant during the connection, whereas [replication\\_connection\\_status](#page-61-0) contains values that change during the connection.

The [replication\\_connection\\_configuration](#page-59-0) table has the following columns. The column descriptions indicate the corresponding CHANGE MASTER TO options from which the column values are taken, and the table given later in this section shows the correspondence between [replication\\_connection\\_configuration](#page-59-0) columns and SHOW SLAVE STATUS columns.

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information. (CHANGE MASTER TO option: FOR CHANNEL)

• HOST

The replication source server that the replica is connected to. (CHANGE MASTER TO option: MASTER\_HOST)

• PORT

The port used to connect to the replication source server. (CHANGE MASTER TO option: MASTER\_PORT)

• USER

The user name of the account used to connect to the replication source server. (CHANGE MASTER TO option: MASTER\_USER)

• NETWORK\_INTERFACE

The network interface that the replica is bound to, if any. (CHANGE MASTER TO option: MASTER\_BIND)

• AUTO\_POSITION

1 if autopositioning is in use; otherwise 0. (CHANGE MASTER TO option: MASTER\_AUTO\_POSITION)

• SSL\_ALLOWED, SSL\_CA\_FILE, SSL\_CA\_PATH, SSL\_CERTIFICATE, SSL\_CIPHER, SSL\_KEY, SSL\_VERIFY\_SERVER\_CERTIFICATE, SSL\_CRL\_FILE, SSL\_CRL\_PATH

These columns show the SSL parameters used by the replica to connect to the replication source server, if any.

SSL\_ALLOWED has these values:

- Yes if an SSL connection to the source is permitted
- No if an SSL connection to the source is not permitted
- Ignored if an SSL connection is permitted but the replica does not have SSL support enabled

CHANGE MASTER TO options for the other SSL columns: MASTER\_SSL\_CA, MASTER\_SSL\_CAPATH, MASTER\_SSL\_CERT, MASTER\_SSL\_CIPHER, MASTER\_SSL\_CRL, MASTER\_SSL\_CRLPATH, MASTER\_SSL\_KEY, MASTER\_SSL\_VERIFY\_SERVER\_CERT.

• CONNECTION\_RETRY\_INTERVAL

The number of seconds between connect retries. (CHANGE MASTER TO option: MASTER\_CONNECT\_RETRY)

• CONNECTION\_RETRY\_COUNT

The number of times the replica can attempt to reconnect to the source in the event of a lost connection. (CHANGE MASTER TO option: MASTER\_RETRY\_COUNT)

• HEARTBEAT\_INTERVAL

The replication heartbeat interval on a replica, measured in seconds. (CHANGE MASTER TO option: MASTER\_HEARTBEAT\_PERIOD)

• TLS\_VERSION

The TLS version used on the source. For TLS version information, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers". (CHANGE MASTER TO option: MASTER\_TLS\_VERSION)

This column was added in MySQL 5.7.10.

TRUNCATE TABLE is not permitted for the [replication\\_connection\\_configuration](#page-59-0) table.

#### The following table shows the correspondence between

[replication\\_connection\\_configuration](#page-59-0) columns and SHOW SLAVE STATUS columns.

| replication_connection_configuration<br>Column | SHOW SLAVE STATUS Column |
|------------------------------------------------|--------------------------|
| CHANNEL_NAME                                   | Channel_name             |
| HOST                                           | Master_Host              |

| replication_connection_configuration<br>Column | SHOW SLAVE STATUS Column      |
|------------------------------------------------|-------------------------------|
| PORT                                           | Master_Port                   |
| USER                                           | Master_User                   |
| NETWORK_INTERFACE                              | Master_Bind                   |
| AUTO_POSITION                                  | Auto_Position                 |
| SSL_ALLOWED                                    | Master_SSL_Allowed            |
| SSL_CA_FILE                                    | Master_SSL_CA_File            |
| SSL_CA_PATH                                    | Master_SSL_CA_Path            |
| SSL_CERTIFICATE                                | Master_SSL_Cert               |
| SSL_CIPHER                                     | Master_SSL_Cipher             |
| SSL_KEY                                        | Master_SSL_Key                |
| SSL_VERIFY_SERVER_CERTIFICATE                  | Master_SSL_Verify_Server_Cert |
| SSL_CRL_FILE                                   | Master_SSL_Crl                |
| SSL_CRL_PATH                                   | Master_SSL_Crlpath            |
| CONNECTION_RETRY_INTERVAL                      | Connect_Retry                 |
| CONNECTION_RETRY_COUNT                         | Master_Retry_Count            |
| HEARTBEAT_INTERVAL                             | None                          |
| TLS_VERSION                                    | Master_TLS_Version            |

## <span id="page-61-0"></span>**25.12.11.2 The replication\_connection\_status Table**

This table shows the current status of the replication I/O thread that handles the replica's connection to the source.

Compared to the [replication\\_connection\\_configuration](#page-59-0) table, [replication\\_connection\\_status](#page-61-0) changes more frequently. It contains values that change during the connection, whereas [replication\\_connection\\_configuration](#page-59-0) contains values which define how the replica connects to the source and that remain constant during the connection.

The [replication\\_connection\\_status](#page-61-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

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

Issuing RESET MASTER or RESET SLAVE resets the values shown in these columns.

• LAST\_ERROR\_TIMESTAMP

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent I/O error took place.

• LAST\_HEARTBEAT\_TIMESTAMP

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent heartbeat signal was received by a replica.

• COUNT\_RECEIVED\_HEARTBEATS

The total number of heartbeat signals that a replica received since the last time it was restarted or reset, or a CHANGE MASTER TO statement was issued.

TRUNCATE TABLE is not permitted for the [replication\\_connection\\_status](#page-61-0) table.

The following table shows the correspondence between [replication\\_connection\\_status](#page-61-0) columns and SHOW SLAVE STATUS columns.

| replication_connection_status Column | SHOW SLAVE STATUS Column |
|--------------------------------------|--------------------------|
| SOURCE_UUID                          | Master_UUID              |
| THREAD_ID                            | None                     |
| SERVICE_STATE                        | Slave_IO_Running         |
| RECEIVED_TRANSACTION_SET             | Retrieved_Gtid_Set       |
| LAST_ERROR_NUMBER                    | Last_IO_Errno            |
| LAST_ERROR_MESSAGE                   | Last_IO_Error            |
| LAST_ERROR_TIMESTAMP                 | Last_IO_Error_Timestamp  |

## <span id="page-62-0"></span>**25.12.11.3 The replication\_applier\_configuration Table**

This table shows the configuration parameters that affect transactions applied by the replica. Parameters stored in the table can be changed at runtime with the CHANGE MASTER TO statement, as indicated in the column descriptions.

The [replication\\_applier\\_configuration](#page-62-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

• DESIRED\_DELAY

The number of seconds that the replica must lag the source. (CHANGE MASTER TO option: MASTER\_DELAY)

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_configuration](#page-62-0) table.

The following table shows the correspondence between [replication\\_applier\\_configuration](#page-62-0)  columns and SHOW SLAVE STATUS columns.

| replication_applier_configuration<br>Column | SHOW SLAVE STATUS Column |
|---------------------------------------------|--------------------------|
| DESIRED_DELAY                               | SQL_Delay                |

## <span id="page-63-0"></span>**25.12.11.4 The replication\_applier\_status Table**

This table shows the current general transaction execution status on the replica. The table provides information about general aspects of transaction applier status that are not specific to any thread involved. Thread-specific status information is available in the [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) table (and [replication\\_applier\\_status\\_by\\_worker](#page-64-0) if the replica is multithreaded).

The [replication\\_applier\\_status](#page-63-0) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

• SERVICE\_STATE

Shows ON when the replication channel's applier threads are active or idle, OFF means that the applier threads are not active.

• REMAINING\_DELAY

If the replica is waiting for DESIRED\_DELAY seconds to pass since the source applied an event, this field contains the number of delay seconds remaining. At other times, this field is NULL. (The DESIRED\_DELAY value is stored in the [replication\\_applier\\_configuration](#page-62-0) table.)

• COUNT\_TRANSACTIONS\_RETRIES

Shows the number of retries that were made because the replication SQL thread failed to apply a transaction. The maximum number of retries for a given transaction is set by the slave\_transaction\_retries system variable.

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_status](#page-63-0) table.

The following table shows the correspondence between [replication\\_applier\\_status](#page-63-0) columns and SHOW SLAVE STATUS columns.

| replication_applier_status Column | SHOW SLAVE STATUS Column |
|-----------------------------------|--------------------------|
| SERVICE_STATE                     | None                     |
| REMAINING_DELAY                   | SQL_Remaining_Delay      |

## <span id="page-63-1"></span>**25.12.11.5 The replication\_applier\_status\_by\_coordinator Table**

For a multithreaded replica, the replica uses multiple worker threads and a coordinator thread to manage them, and this table shows the status of the coordinator thread. For a single-threaded replica, this table is empty. For a multithreaded replica, the [replication\\_applier\\_status\\_by\\_worker](#page-64-0) table shows the status of the worker threads.

The [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

• THREAD\_ID

The SQL/coordinator thread ID.

• SERVICE\_STATE

ON (thread exists and is active or idle) or OFF (thread no longer exists).

• LAST\_ERROR\_NUMBER, LAST\_ERROR\_MESSAGE

The error number and error message of the most recent error that caused the SQL/coordinator thread to stop. An error number of 0 and message which is an empty string means "no error". If the LAST\_ERROR\_MESSAGE value is not empty, the error values also appear in the replica's error log.

Issuing RESET MASTER or RESET SLAVE resets the values shown in these columns.

All error codes and messages displayed in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns correspond to error values listed in [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

• LAST\_ERROR\_TIMESTAMP

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent SQL/coordinator error occurred.

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) table.

The following table shows the correspondence between

[replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) columns and SHOW SLAVE STATUS columns.

| replication_applier_status_by_coordinator<br>Column | SHOW SLAVE STATUS Column |
|-----------------------------------------------------|--------------------------|
| THREAD_ID                                           | None                     |
| SERVICE_STATE                                       | Slave_SQL_Running        |
| LAST_ERROR_NUMBER                                   | Last_SQL_Errno           |
| LAST_ERROR_MESSAGE                                  | Last_SQL_Error           |
| LAST_ERROR_TIMESTAMP                                | Last_SQL_Error_Timestamp |

## <span id="page-64-0"></span>**25.12.11.6 The replication\_applier\_status\_by\_worker Table**

If the replica is not multithreaded, this table shows the status of the applier thread. Otherwise, the replica uses multiple worker threads and a coordinator thread to manage them, and this table shows the status of the worker threads. For a multithreaded replica, the [replication\\_applier\\_status\\_by\\_coordinator](#page-63-1) table shows the status of the coordinator thread.

The replication\_applier\_status\_by\_worker table has these columns:

• CHANNEL\_NAME

The replication channel which this row is displaying. There is always a default replication channel, and more replication channels can be added. See Section 16.2.2, "Replication Channels" for more information.

• WORKER\_ID

The worker identifier (same value as the id column in the mysql.slave\_worker\_info table). After STOP SLAVE, the THREAD\_ID column becomes NULL, but the WORKER\_ID value is preserved.

• THREAD\_ID

The worker thread identifier.

• SERVICE\_STATE

ON (thread exists and is active or idle) or OFF (thread no longer exists).

• LAST\_SEEN\_TRANSACTION

The transaction that the worker has last seen. The worker has not necessarily applied this transaction because it could still be in the process of doing so.

If the gtid\_mode system variable value is OFF, this column is ANONYMOUS, indicating that transactions do not have global transaction identifiers (GTIDs) and are identified by file and position only.

If gtid\_mode is ON, the column value is defined as follows:

- If no transaction has executed, the column is empty.
- When a transaction has executed, the column is set from gtid\_next as soon as gtid\_next is set. From this moment, the column always shows a GTID.
- The GTID is preserved until the next transaction is executed. If an error occurs, the column value is the GTID of the transaction being executed by the worker when the error occurred. The following statement shows whether or not that transaction has been committed:

```
SELECT GTID_SUBSET(LAST_SEEN_TRANSACTION, @@GLOBAL.GTID_EXECUTED)
FROM performance_schema.replication_applier_status_by_worker;
```

If the statement returns zero, the transaction has not yet been committed, either because it is still being processed, or because the worker thread was stopped while it was being processed. If the statement returns nonzero, the transaction has been committed.

• LAST\_ERROR\_NUMBER, LAST\_ERROR\_MESSAGE

The error number and error message of the most recent error that caused the worker thread to stop. An error number of 0 and message of the empty string mean "no error". If the LAST\_ERROR\_MESSAGE value is not empty, the error values also appear in the replica's error log.

Issuing RESET MASTER or RESET SLAVE resets the values shown in these columns.

All error codes and messages displayed in the LAST\_ERROR\_NUMBER and LAST\_ERROR\_MESSAGE columns correspond to error values listed in [Server Error Message Reference.](https://dev.mysql.com/doc/mysql-errors/5.7/en/server-error-reference.md)

• LAST\_ERROR\_TIMESTAMP

A timestamp in YYMMDD hh:mm:ss format that shows when the most recent worker error occurred.

TRUNCATE TABLE is not permitted for the [replication\\_applier\\_status\\_by\\_worker](#page-64-0) table.

The following table shows the correspondence between

replication\_applier\_status\_by\_worker columns and SHOW SLAVE STATUS columns.

| replication_applier_status_by_worker<br>Column | SHOW SLAVE STATUS Column |
|------------------------------------------------|--------------------------|
| WORKER_ID                                      | None                     |

| replication_applier_status_by_worker<br>Column | SHOW SLAVE STATUS Column |
|------------------------------------------------|--------------------------|
| THREAD_ID                                      | None                     |
| SERVICE_STATE                                  | None                     |
| LAST_SEEN_TRANSACTION                          | None                     |
| LAST_ERROR_NUMBER                              | Last_SQL_Errno           |
| LAST_ERROR_MESSAGE                             | Last_SQL_Error           |
| LAST_ERROR_TIMESTAMP                           | Last_SQL_Error_Timestamp |

## <span id="page-66-0"></span>**25.12.11.7 The replication\_group\_member\_stats Table**

This table shows statistical information for MySQL Group Replication members. It is populated only when Group Replication is running.

The replication\_group\_member\_stats table has these columns:

• CHANNEL\_NAME

Name of the Group Replication channel.

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

TRUNCATE TABLE is not permitted for the [replication\\_group\\_member\\_stats](#page-66-0) table.

## <span id="page-66-1"></span>**25.12.11.8 The replication\_group\_members Table**

This table shows network and status information for replication group members. The network addresses shown are the addresses used to connect clients to the group, and should not be confused with the member's internal group communication address specified by group\_replication\_local\_address.

The replication\_group\_members table has these columns:

• CHANNEL\_NAME

Name of the Group Replication channel.

• MEMBER\_ID

Identifier for this member; the same as the server UUID.

• MEMBER\_HOST

Network address of this member (host name or IP address). Retrieved from the member's hostname variable.

• MEMBER\_PORT

Port on which the server is listening. Retrieved from the member's port variable.

• MEMBER\_STATE

Current state of this member; can be any one of the following:

- OFFLINE: The Group Replication plugin is installed but has not been started.
- RECOVERING: The server has joined a group from which it is retrieving data.
- ONLINE: The member is in a fully functioning state.
- ERROR: The member has encountered an error, either during applying transactions or during the recovery phase, and is not participating in the group's transactions.
- UNREACHABLE: The failure detection process suspects that this member cannot be contacted, because the group messages have timed out.

TRUNCATE TABLE is not permitted for the [replication\\_group\\_members](#page-66-1) table.