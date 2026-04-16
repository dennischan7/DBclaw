---
source: MySQL 8.4 Reference
title: 00_Overview
---

Replication can be controlled through the SQL interface using the statements described in this section. Statements are split into a group which controls source servers, a group which controls replica servers, and a group which can be applied to any replication servers.

# <span id="page-144-1"></span>**15.4.1 SQL Statements for Controlling Source Servers**

This section discusses statements for managing replication source servers. [Section 15.4.2, "SQL](#page-147-0) [Statements for Controlling Replica Servers"](#page-147-0), discusses statements for managing replica servers.

In addition to the statements described here, the following SHOW statements are used with source servers in replication. For information about these statements, see Section 15.7.7, "SHOW Statements".

- SHOW BINARY LOGS
- SHOW BINLOG EVENTS
- SHOW BINARY LOG STATUS (replaces SHOW MASTER STATUS, which is no longer supported)
- SHOW REPLICAS

## <span id="page-144-0"></span>**15.4.1.1 PURGE BINARY LOGS Statement**

```
PURGE BINARY LOGS {
 TO 'log_name'
 | BEFORE datetime_expr
}
```

The binary log is a set of files that contain information about data modifications made by the MySQL server. The log consists of a set of binary log files, plus an index file (see Section 7.4.4, "The Binary Log").

The [PURGE BINARY LOGS](#page-144-0) statement deletes all the binary log files listed in the log index file prior to the specified log file name or date. Deleted log files also are removed from the list recorded in the index file, so that the given log file becomes the first in the list.

[PURGE BINARY LOGS](#page-144-0) requires the BINLOG\_ADMIN privilege. This statement has no effect if the server was not started with the --log-bin option to enable binary logging.

#### Examples:

```
PURGE BINARY LOGS TO 'mysql-bin.010';
PURGE BINARY LOGS BEFORE '2019-04-02 22:46:26';
```

The BEFORE variant's datetime\_expr argument should evaluate to a DATETIME value (a value in 'YYYY-MM-DD hh:mm:ss' format).

[PURGE BINARY LOGS](#page-144-0) is safe to run while replicas are replicating. You need not stop them. If you have an active replica that currently is reading one of the log files you are trying to delete, this statement does not delete the log file that is in use or any log files later than that one, but it deletes any earlier

log files. A warning message is issued in this situation. However, if a replica is not connected and you happen to purge one of the log files it has yet to read, the replica cannot replicate after it reconnects.

[PURGE BINARY LOGS](#page-144-0) cannot be issued while a [LOCK INSTANCE FOR BACKUP](#page-130-0) statement is in effect for the instance, because it contravenes the rules of the backup lock by removing files from the server.

To safely purge binary log files, follow this procedure:

- 1. On each replica, use SHOW REPLICA STATUS to check which log file it is reading.
- 2. Obtain a listing of the binary log files on the source with SHOW BINARY LOGS.
- 3. Determine the earliest log file among all the replicas. This is the target file. If all the replicas are up to date, this is the last log file on the list.
- 4. Make a backup of all the log files you are about to delete. (This step is optional, but always advisable.)
- 5. Purge all log files up to but not including the target file.

PURGE BINARY LOGS TO and PURGE BINARY LOGS BEFORE both fail with an error when binary log files listed in the .index file had been removed from the system by some other means (such as using rm on Linux). (Bug #18199, Bug #18453) To handle such errors, edit the .index file (which is a simple text file) manually to ensure that it lists only the binary log files that are actually present, then run again the [PURGE BINARY LOGS](#page-144-0) statement that failed.

Binary log files are automatically removed after the server's binary log expiration period. Removal of the files can take place at startup and when the binary log is flushed. The default binary log expiration period is 30 days. You can specify an alternative expiration period using the binlog\_expire\_logs\_seconds system variable. If you are using replication, you should specify an expiration period that is no lower than the maximum amount of time your replicas might lag behind the source.

## <span id="page-145-0"></span>**15.4.1.2 RESET BINARY LOGS AND GTIDS Statement**

![](_page_145_Picture_12.jpeg)

#### **Note**

This statement takes the place of the old RESET MASTER statement, which is no longer supported.

RESET BINARY LOGS AND GTIDS [TO binary\_log\_file\_index\_number]

![](_page_145_Picture_16.jpeg)

#### **Warning**

Use this statement with caution to ensure you do not lose any wanted binary log file data and GTID execution history.

RESET BINARY LOGS AND GTIDS requires the RELOAD privilege.

For a server where binary logging is enabled (log\_bin is ON), RESET BINARY LOGS AND GTIDS deletes all existing binary log files and resets the binary log index file, resetting the server to its state before binary logging was started. A new empty binary log file is created so that binary logging can be restarted.

For a server where GTIDs are in use (gtid\_mode is ON), issuing RESET BINARY LOGS AND GTIDS resets the GTID execution history. The value of the gtid\_purged system variable is set to an empty string (''), the global value (but not the session value) of the gtid\_executed system variable is set to an empty string, and the mysql.gtid\_executed table is cleared (see mysql.gtid\_executed Table). If the GTID-enabled server has binary logging enabled, RESET BINARY LOGS AND GTIDS also resets the binary log as described above. Note that RESET BINARY LOGS AND GTIDS is the method to reset the GTID execution history even if the GTID-enabled server is a replica where binary logging

is disabled; [RESET REPLICA](#page-162-0) has no effect on the GTID execution history. For more information on resetting the GTID execution history, see Resetting the GTID Execution History.

Issuing RESET BINARY LOGS AND GTIDS without the optional TO clause deletes all binary log files listed in the index file, resets the binary log index file to be empty, and creates a new binary log file starting at 1. Use the optional TO clause to start the binary log file index from a number other than 1 after the reset.

Check that you are using a reasonable value for the index number. If you enter an incorrect value, you can correct this by issuing another RESET BINARY LOGS AND GTIDS statement with or without the TO clause. If you do not correct a value that is out of range, the server cannot be restarted.

The following example demonstrates TO clause usage:

```
RESET BINARY LOGS AND GTIDS TO 1234;
SHOW BINARY LOGS;
+-------------------+-----------+-----------+
| Log_name | File_size | Encrypted |
+-------------------+-----------+-----------+
| source-bin.001234 | 154 | No |
+-------------------+-----------+-----------+
```

![](_page_146_Picture_6.jpeg)

#### **Important**

The effects of RESET BINARY LOGS AND GTIDS without the TO clause differ from those of [PURGE BINARY LOGS](#page-144-0) in 2 key ways:

- 1. RESET BINARY LOGS AND GTIDS removes all binary log files that are listed in the index file, leaving only a single, empty binary log file with a numeric suffix of .000001, whereas the numbering is not reset by [PURGE](#page-144-0) [BINARY LOGS](#page-144-0).
- 2. RESET BINARY LOGS AND GTIDS is not intended to be used while any replicas are running. The behavior of RESET BINARY LOGS AND GTIDS when used while replicas are running is undefined (and thus unsupported), whereas [PURGE BINARY LOGS](#page-144-0) may be safely used while replicas are running.

See also [Section 15.4.1.1, "PURGE BINARY LOGS Statement".](#page-144-0)

RESET BINARY LOGS AND GTIDS without the TO clause can prove useful when you first set up a source and replica, so that you can verify the setup as follows:

- 1. Start the source and replica, and start replication (see Section 19.1.2, "Setting Up Binary Log File Position Based Replication").
- 2. Execute a few test queries on the source.
- 3. Check that the queries were replicated to the replica.
- 4. When replication is running correctly, issue [STOP REPLICA](#page-168-0) followed by [RESET REPLICA](#page-162-0) (both on the replica), then verify that no unwanted data from the test queries exists on the replica. Following this, issue RESET BINARY LOGS AND GTIDS (also on the replica) to remove binary logs and and associated transaction IDs.
- 5. Remove the unwanted data from the source, then issue RESET BINARY LOGS AND GTIDS to purge any binary log entries and identifiers associated with it.

After verifying the setup, resetting the source and replica and ensuring that no unwanted data or binary log files generated by testing remain on the source or replica, you can start the replica and begin replicating.