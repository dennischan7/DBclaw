---
source: MySQL 5.7 Reference
title: 00_Overview
---

Replication can be controlled through the SQL interface using the statements described in this section. Statements are split into a group which controls replication source servers, a group which controls replica servers, and a group which can be applied to any servers in a replication topology.

# <span id="page-29-1"></span>**13.4.1 SQL Statements for Controlling Replication Source Servers**

This section discusses statements for managing replication source servers. [Section 13.4.2, "SQL](#page-32-1) [Statements for Controlling Replica Servers"](#page-32-1), discusses statements for managing replica servers.

In addition to the statements described here, the following [SHOW](#page-134-0) statements are used with source servers in replication. For information about these statements, see [Section 13.7.5, "SHOW](#page-134-0) [Statements".](#page-134-0)

- [SHOW BINARY LOGS](#page-135-0)
- [SHOW BINLOG EVENTS](#page-135-1)
- [SHOW MASTER STATUS](#page-156-0)
- [SHOW SLAVE HOSTS](#page-166-0)

## <span id="page-29-0"></span>**13.4.1.1 PURGE BINARY LOGS Statement**

```
PURGE { BINARY | MASTER } LOGS {
 TO 'log_name'
```

```
 | BEFORE datetime_expr
}
```

The binary log is a set of files that contain information about data modifications made by the MySQL server. The log consists of a set of binary log files, plus an index file (see Section 5.4.4, "The Binary Log").

The [PURGE BINARY LOGS](#page-29-0) statement deletes all the binary log files listed in the log index file prior to the specified log file name or date. BINARY and MASTER are synonyms. Deleted log files also are removed from the list recorded in the index file, so that the given log file becomes the first in the list.

[PURGE BINARY LOGS](#page-29-0) requires the [BINLOG\\_ADMIN](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.md#priv_binlog-admin) privilege. This statement has no effect if the server was not started with the --log-bin option to enable binary logging.

### Examples:

```
PURGE BINARY LOGS TO 'mysql-bin.010';
PURGE BINARY LOGS BEFORE '2019-04-02 22:46:26';
```

The BEFORE variant's datetime\_expr argument should evaluate to a DATETIME value (a value in 'YYYY-MM-DD hh:mm:ss' format).

This statement is safe to run while replicas are replicating. You need not stop them. If you have an active replica that currently is reading one of the log files you are trying to delete, this statement does not delete the log file that is in use or any log files later than that one, but it deletes any earlier log files. A warning message is issued in this situation. However, if a replica is not connected and you happen to purge one of the log files it has yet to read, the replica cannot replicate after it reconnects.

To safely purge binary log files, follow this procedure:

- 1. On each replica, use [SHOW SLAVE STATUS](#page-167-0) to check which log file it is reading.
- 2. Obtain a listing of the binary log files on the replication source server with [SHOW BINARY LOGS](#page-135-0).
- 3. Determine the earliest log file among all the replicas. This is the target file. If all the replicas are up to date, this is the last log file on the list.
- 4. Make a backup of all the log files you are about to delete. (This step is optional, but always advisable.)
- 5. Purge all log files up to but not including the target file.

You can also set the expire\_logs\_days system variable to expire binary log files automatically after a given number of days (see Section 5.1.7, "Server System Variables"). If you are using replication, you should set the variable no lower than the maximum number of days your replicas might lag behind the source.

PURGE BINARY LOGS TO and PURGE BINARY LOGS BEFORE both fail with an error when binary log files listed in the .index file had been removed from the system by some other means (such as using rm on Linux). (Bug #18199, Bug #18453) To handle such errors, edit the .index file (which is a simple text file) manually to ensure that it lists only the binary log files that are actually present, then run again the [PURGE BINARY LOGS](#page-29-0) statement that failed.

## <span id="page-30-0"></span>**13.4.1.2 RESET MASTER Statement**

RESET MASTER

![](_page_30_Picture_19.jpeg)

#### **Warning**

Use this statement with caution to ensure you do not lose any wanted binary log file data and GTID execution history.

[RESET MASTER](#page-30-0) requires the RELOAD privilege.

For a server where binary logging is enabled (log\_bin is ON), RESET MASTER deletes all existing binary log files and resets the binary log index file, resetting the server to its state before binary logging was started. A new empty binary log file is created so that binary logging can be restarted.

For a server where GTIDs are in use (gtid\_mode is ON), issuing RESET MASTER resets the GTID execution history. The value of the gtid\_purged system variable is set to an empty string (''), the global value (but not the session value) of the gtid\_executed system variable is set to an empty string, and the mysql.gtid\_executed table is cleared (see mysql.gtid\_executed Table). If the GTIDenabled server has binary logging enabled, [RESET MASTER](#page-30-0) also resets the binary log as described above. Note that [RESET MASTER](#page-30-0) is the method to reset the GTID execution history even if the GTIDenabled server is a replica where binary logging is disabled; [RESET SLAVE](#page-40-0) has no effect on the GTID execution history. For more information on resetting the GTID execution history, see Resetting the GTID Execution History.

![](_page_31_Picture_4.jpeg)

### **Important**

The effects of [RESET MASTER](#page-30-0) differ from those of [PURGE BINARY LOGS](#page-29-0) in 2 key ways:

- 1. [RESET MASTER](#page-30-0) removes all binary log files that are listed in the index file, leaving only a single, empty binary log file with a numeric suffix of .000001, whereas the numbering is not reset by [PURGE BINARY LOGS](#page-29-0).
- 2. [RESET MASTER](#page-30-0) is not intended to be used while any replicas are running. The behavior of [RESET MASTER](#page-30-0) when used while replicas are running is undefined (and thus unsupported), whereas [PURGE BINARY LOGS](#page-29-0) may be safely used while replicas are running.

See also [Section 13.4.1.1, "PURGE BINARY LOGS Statement".](#page-29-0)

[RESET MASTER](#page-30-0) can prove useful when you first set up the source and the replica, so that you can verify the setup as follows:

- 1. Start the source and replica, and start replication (see Section 16.1.2, "Setting Up Binary Log File Position Based Replication").
- 2. Execute a few test queries on the source.
- 3. Check that the queries were replicated to the replica.
- 4. When replication is running correctly, issue [STOP SLAVE](#page-46-0) followed by [RESET SLAVE](#page-40-0) on the replica, then verify that any unwanted data no longer exists on the replica.
- 5. Issue [RESET MASTER](#page-30-0) on the source to clean up the test queries.

After verifying the setup, resetting the source and replica and ensuring that no unwanted data or binary log files generated by testing remain on source or replica, you can start the replica and begin replicating.