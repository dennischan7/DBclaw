---
source: MySQL 8.0 Reference
title: 00_Overview
---

The global value of the system variable replica\_transaction\_retries (from MySQL 8.0.26) or slave\_transaction\_retries (before MySQL 8.0.26) sets the maximum number of times for applier threads on a single-threaded or multithreaded replica to automatically retry failed transactions before stopping. Transactions are automatically retried when the SQL thread fails to execute them because of an InnoDB deadlock, or when the transaction's execution time exceeds the InnoDB innodb\_lock\_wait\_timeout value. If a transaction has a non-temporary error that prevents it from succeeding, it is not retried.

The default setting for replica\_transaction\_retries or slave\_transaction\_retries is 10, meaning that a failing transaction with an apparently temporary error is retried 10 times before the applier thread stops. Setting the variable to 0 disables automatic retrying of transactions. On a multithreaded replica, the specified number of transaction retries can take place on all applier threads of all channels. The Performance Schema table replication\_applier\_status shows the total number of transaction retries that took place on each replication channel, in the COUNT\_TRANSACTIONS\_RETRIES column.

The process of retrying transactions can cause lag on a replica or on a Group Replication group member, which can be configured as a single-threaded or multithreaded replica. The Performance Schema table replication\_applier\_status\_by\_worker shows detailed information on transaction retries by the applier threads on a single-threaded or multithreaded replica. This data includes timestamps showing how long it took the applier thread to apply the last transaction from start to finish (and when the transaction currently in progress was started), and how long this was after the commit on the original source and the immediate source. The data also shows the number of retries for the last transaction and the transaction currently in progress, and enables you to identify the transient errors that caused the transactions to be retried. You can use this information to see whether transaction retries are the cause of replication lag, and investigate the root cause of the failures that led to the retries.

# <span id="page-68-0"></span>**19.5.1.33 Replication and Time Zones**

By default, source and replica servers assume that they are in the same time zone. If you are replicating between servers in different time zones, the time zone must be set on both source and replica. Otherwise, statements depending on the local time on the source are not replicated properly, such as statements that use the NOW() or FROM\_UNIXTIME() functions.

Verify that your combination of settings for the system time zone (system\_time\_zone), server current time zone (the global value of time\_zone), and per-session time zones (the session value of time\_zone) on the source and replica is producing the correct results. In particular, if the time\_zone system variable is set to the value SYSTEM, indicating that the server time zone is the same as the system time zone, this can cause the source and replica to apply different time zones. For example, a source could write the following statement in the binary log:

```
SET @@session.time_zone='SYSTEM';
```

If this source and its replica have a different setting for their system time zones, this statement can produce unexpected results on the replica, even if the replica's global time\_zone value has been set to match the source's. For an explanation of MySQL Server's time zone settings, and how to change them, see Section 7.1.15, "MySQL Server Time Zone Support".

See also [Section 19.5.1.14, "Replication and System Functions".](#page-57-0)

# <span id="page-69-0"></span>**19.5.1.34 Replication and Transaction Inconsistencies**

Inconsistencies in the sequence of transactions that have been executed from the relay log can occur depending on your replication configuration. This section explains how to avoid inconsistencies and solve any problems they cause.

The following types of inconsistencies can exist:

- Half-applied transactions. A transaction which updates non-transactional tables has applied some but not all of its changes.
- Gaps. A gap in the externalized transaction set appears when, given an ordered sequence of transactions, a transaction that is later in the sequence is applied before some other transaction that is prior in the sequence. Gaps can only appear when using a multithreaded replica.

To avoid gaps occurring on a multithreaded replica, set replica\_preserve\_commit\_order=ON (from MySQL 8.0.26) or slave\_preserve\_commit\_order=ON (before MySQL 8.0.26). From MySQL 8.0.27, this setting is the default, because all replicas are multithreaded by default from that release.

Up to and including MySQL 8.0.18, preserving the commit order requires that binary logging (log\_bin) and replica update logging (log\_replica\_updates or log\_slave\_updates) are also enabled, which are the default settings from MySQL 8.0. From MySQL 8.0.19, binary logging and replica update logging are not required on the replica to set replica\_preserve\_commit\_order=ON or slave\_preserve\_commit\_order=ON, and can be disabled if wanted.

In all releases, setting replica\_preserve\_commit\_order=ON or slave\_preserve\_commit\_order=ON requires that replica\_parallel\_type (from MySQL 8.0.26) or slave\_parallel\_type (before MySQL 8.0.26) is set to LOGICAL\_CLOCK. From MySQL 8.0.27 (but not for earlier releases), this is the default setting.

In some specific situations, as listed in the description for replica\_preserve\_commit\_order and slave\_preserve\_commit\_order, setting replica\_preserve\_commit\_order=ON or slave\_preserve\_commit\_order=ON cannot preserve commit order on the replica, so in these cases gaps might still appear in the sequence of transactions that have been executed from the replica's relay log.

Setting replica\_preserve\_commit\_order=ON or slave\_preserve\_commit\_order=ON does not prevent source binary log position lag.

• Source binary log position lag. Even in the absence of gaps, it is possible that transactions after Exec\_master\_log\_pos have been applied. That is, all transactions up to point N have been applied, and no transactions after N have been applied, but Exec\_master\_log\_pos has a value smaller than N. In this situation, Exec\_master\_log\_pos is a "low-water mark" of the transactions applied, and lags behind the position of the most recently applied transaction. This can only happen on multithreaded replicas. Enabling replica\_preserve\_commit\_order or slave\_preserve\_commit\_order does not prevent source binary log position lag.

The following scenarios are relevant to the existence of half-applied transactions, gaps, and source binary log position lag:

- 1. While replication threads are running, there may be gaps and half-applied transactions.
- 2. mysqld shuts down. Both clean and unclean shutdown abort ongoing transactions and may leave gaps and half-applied transactions.
- 3. KILL of replication threads (the SQL thread when using a single-threaded replica, the coordinator thread when using a multithreaded replica). This aborts ongoing transactions and may leave gaps and half-applied transactions.
- 4. Error in applier threads. This may leave gaps. If the error is in a mixed transaction, that transaction is half-applied. When using a multithreaded replica, workers which have not received an error complete their queues, so it may take time to stop all threads.
- 5. STOP REPLICA when using a multithreaded replica. After issuing STOP REPLICA, the replica waits for any gaps to be filled and then updates Exec\_master\_log\_pos. This ensures it never leaves gaps or source binary log position lag, unless any of the cases above applies, in other words, before STOP REPLICA completes, either an error happens, or another thread issues KILL, or the server restarts. In these cases, STOP REPLICA returns successfully.
- 6. If the last transaction in the relay log is only half-received and the multithreaded replica's coordinator thread has started to schedule the transaction to a worker, then STOP REPLICA waits up to 60 seconds for the transaction to be received. After this timeout, the coordinator gives up and aborts the transaction. If the transaction is mixed, it may be left half-completed.
- 7. STOP REPLICA when the ongoing transaction updates transactional tables only, in which case it is rolled back and STOP REPLICA stops immediately. If the ongoing transaction is mixed, STOP REPLICA waits up to 60 seconds for the transaction to complete. After this timeout, it aborts the transaction, so it may be left half-completed.

The global setting for the system variable rpl\_stop\_replica\_timeout (from MySQL 8.0.26) or rpl\_stop\_slave\_timeout (before MySQL 8.0.26) is unrelated to the process of stopping the replication threads. It only makes the client that issues STOP REPLICA return to the client, but the replication threads continue to try to stop.

If a replication channel has gaps, it has the following consequences:

- 1. The replica database is in a state that may never have existed on the source.
- 2. The field Exec\_master\_log\_pos in SHOW REPLICA STATUS is only a "low-water mark". In other words, transactions appearing before the position are guaranteed to have committed, but transactions after the position may have committed or not.
- 3. CHANGE REPLICATION SOURCE TO and CHANGE MASTER TO statements for that channel fail with an error, unless the applier threads are running and the statement only sets receiver options.
- 4. If mysqld is started with --relay-log-recovery, no recovery is done for that channel, and a warning is printed.
- 5. If mysqldump is used with --dump-replica or --dump-slave, it does not record the existence of gaps; thus it prints CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO with RELAY\_LOG\_POS set to the "low-water mark" position in Exec\_master\_log\_pos.

After applying the dump on another server, and starting the replication threads, transactions appearing after the position are replicated again. Note that this is harmless if GTIDs are enabled (however, in that case it is not recommended to use --dump-replica or --dump-slave).

If a replication channel has source binary log position lag but no gaps, cases 2 to 5 above apply, but case 1 does not.

The source binary log position information is persisted in binary format in the internal table mysql.slave\_worker\_info. START REPLICA [SQL\_THREAD] always consults this information so that it applies only the correct transactions. This remains true even if replica\_parallel\_workers or slave\_parallel\_workers has been changed to 0 before START REPLICA, and even if START REPLICA is used with UNTIL clauses. START REPLICA UNTIL SQL\_AFTER\_MTS\_GAPS only applies as many transactions as needed in order to fill in the gaps. If START REPLICA is used with UNTIL clauses that tell it to stop before it has consumed all the gaps, then it leaves remaining gaps.

![](_page_71_Picture_2.jpeg)

#### **Warning**

RESET REPLICA removes the relay logs and resets the replication position. Thus issuing RESET REPLICA on a multithreaded replica with gaps means the replica loses any information about the gaps, without correcting the gaps. In this situation, if binary log position based replication is in use, the recovery process fails.

When GTID-based replication is in use (GTID\_MODE=ON) and SOURCE\_AUTO\_POSITION is set for the replication channel using the CHANGE REPLICATION SOURCE TO statement, the old relay logs are not required for the recovery process. Instead, the replica can use GTID auto-positioning to calculate what transactions it is missing compared to the source. From MySQL 8.0.26, the process used for binary log position based replication to resolve gaps on a multithreaded replica is skipped entirely when GTID-based replication is in use. When the process is skipped, a START REPLICA UNTIL SQL\_AFTER\_MTS\_GAPS statement behaves differently, and does not attempt to check for gaps in the sequence of transactions. You can also issue CHANGE REPLICATION SOURCE TO statements, which are not permitted on a non-GTID replica where there are gaps.