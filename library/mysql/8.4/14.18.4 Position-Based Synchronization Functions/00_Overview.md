---
source: MySQL 8.4 Reference
title: 00_Overview
---

The functions listed in this section are used for controlling position-based synchronization of source and replica servers in MySQL Replication.

**Table 14.28 Positional Synchronization Functions**

| Name              | Description                                                                                 | Deprecated |
|-------------------|---------------------------------------------------------------------------------------------|------------|
| MASTER_POS_WAIT() | Block until the replica has read<br>and applied all updates up to the<br>specified position | Yes        |
| SOURCE_POS_WAIT() | Block until the replica has read<br>and applied all updates up to the<br>specified position |            |

<span id="page-6-0"></span>• [MASTER\\_POS\\_WAIT\(](#page-6-0)log\_name,log\_pos[,timeout][,channel])

Deprecated alias for [SOURCE\\_POS\\_WAIT\(\)](#page-6-1).

<span id="page-6-1"></span>• [SOURCE\\_POS\\_WAIT\(](#page-6-1)log\_name,log\_pos[,timeout][,channel])

This function is for control of source-replica synchronization. It blocks until the replica has read and applied all updates up to the specified position in the source's binary log.

The return value is the number of log events the replica had to wait for to advance to the specified position. The function returns NULL if the replication SQL thread is not started, the replica's source information is not initialized, the arguments are incorrect, or an error occurs. It returns -1 if the timeout has been exceeded. If the replication SQL thread stops while [SOURCE\\_POS\\_WAIT\(\)](#page-6-1) is waiting, the function returns NULL. If the replica is past the specified position, the function returns immediately.

If the binary log file position has been marked as invalid, the function waits until a valid file position is known. The binary log file position can be marked as invalid when the CHANGE REPLICATION SOURCE TO option GTID\_ONLY is set for the replication channel, and the server is restarted or replication is stopped. The file position becomes valid after a transaction is successfully applied past the given file position. If the applier does not reach the stated position, the function waits until the timeout. Use a SHOW REPLICA STATUS statement to check if the binary log file position has been marked as invalid.

On a multithreaded replica, the function waits until expiry of the limit set by the replica\_checkpoint\_group or replica\_checkpoint\_period system variable, when the checkpoint operation is called to update the status of the replica. Depending on the setting for the system variables, the function might therefore return some time after the specified position was reached.

If binary log transaction compression is in use and the transaction payload at the specified position is compressed (as a Transaction\_payload\_event), the function waits until the whole transaction has been read and applied, and the positions have updated.

If a timeout value is specified, [SOURCE\\_POS\\_WAIT\(\)](#page-6-1) stops waiting when timeout seconds have elapsed. timeout must be greater than or equal to 0. (When the server is running in strict SQL

mode, a negative timeout value is immediately rejected with [ER\\_WRONG\\_ARGUMENTS](https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.md#error_er_wrong_arguments); otherwise the function returns NULL, and raises a warning.)

The optional channel value enables you to name which replication channel the function applies to. See Section 19.2.2, "Replication Channels" for more information.

This function is unsafe for statement-based replication. A warning is logged if you use this function when binlog\_format is set to STATEMENT.