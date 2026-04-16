---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports delayed replication such that a replica server deliberately executes transactions later than the source by at least a specified amount of time. This section describes how to configure a replication delay on a replica, and how to monitor replication delay.

In MySQL 8.4, the method of delaying replication depends on two timestamps, immediate\_commit\_timestamp and original\_commit\_timestamp (see [Replication Delay](#page-175-0) [Timestamps](#page-175-0)); delayed replication is measured using these timestamps. If either the immediate source or replica is not using these timestamps, the implementation of delayed replication from MySQL 5.7 is used (see [Delayed Replication\)](https://dev.mysql.com/doc/refman/5.7/en/replication-delayed.md). This section describes delayed replication between servers which are all using these timestamps.

The default replication delay is 0 seconds. Use a CHANGE REPLICATION SOURCE TO SOURCE\_DELAY=N statement to set the delay to N seconds. A transaction received from the source is not executed until at least N seconds later than its commit on the immediate source. The delay happens per transaction (not event as in previous MySQL versions) and the actual delay is imposed only on gtid\_log\_event or anonymous\_gtid\_log\_event. The other events in the transaction always follow these events without any waiting time imposed on them.

![](_page_174_Picture_18.jpeg)

#### **Note**

START REPLICA and STOP REPLICA take effect immediately and ignore any delay. RESET REPLICA resets the delay to 0.

The replication\_applier\_configuration Performance Schema table contains the DESIRED\_DELAY column which shows the delay configured using the SOURCE\_DELAY option. The replication\_applier\_status Performance Schema table contains the REMAINING\_DELAY column which shows the number of delay seconds remaining.

Delayed replication can be used for several purposes:

- To protect against user mistakes on the source. With a delay you can roll back a delayed replica to the time just before the mistake.
- To test how the system behaves when there is a lag. For example, in an application, a lag might be caused by a heavy load on the replica. However, it can be difficult to generate this load level. Delayed replication can simulate the lag without having to simulate the load. It can also be used to debug conditions related to a lagging replica.
- To inspect what the database looked like in the past, without having to reload a backup. For example, by configuring a replica with a delay of one week, if you then need to see what the database looked like before the last few days' worth of development, the delayed replica can be inspected.

## <span id="page-175-0"></span>**Replication Delay Timestamps**

MySQL 8.4 provides a new method for measuring delay (also referred to as replication lag) in replication topologies that depends on the following timestamps associated with the GTID of each transaction (instead of each event) written to the binary log.

- original\_commit\_timestamp: the number of microseconds since epoch when the transaction was written (committed) to the binary log of the original source.
- immediate\_commit\_timestamp: the number of microseconds since epoch when the transaction was written (committed) to the binary log of the immediate source.

The output of mysqlbinlog displays these timestamps in two formats, microseconds from epoch and also TIMESTAMP format, which is based on the user defined time zone for better readability. For example:

```
#170404 10:48:05 server id 1 end_log_pos 233 CRC32 0x016ce647 GTID last_committed=0
\ sequence_number=1 original_committed_timestamp=1491299285661130 immediate_commit_timestamp=1491299285843771
# original_commit_timestamp=1491299285661130 (2017-04-04 10:48:05.661130 WEST)
# immediate_commit_timestamp=1491299285843771 (2017-04-04 10:48:05.843771 WEST)
 /*!80001 SET @@SESSION.original_commit_timestamp=1491299285661130*//*!*/;
 SET @@SESSION.GTID_NEXT= 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa:1'/*!*/;
# at 233
```

As a rule, the original\_commit\_timestamp is always the same on all replicas where the transaction is applied. In source-replica replication, the original\_commit\_timestamp of a transaction in the (original) source's binary log is always the same as its immediate\_commit\_timestamp. In the replica's relay log, the original\_commit\_timestamp and immediate\_commit\_timestamp of the transaction are the same as in the source's binary log; whereas in its own binary log, the transaction's immediate\_commit\_timestamp corresponds to when the replica committed the transaction.

In a Group Replication setup, when the original source is a member of a group, the original\_commit\_timestamp is generated when the transaction is ready to be committed. In other words, when it finished executing on the original source and its write set is ready to be sent to all members of the group for certification. When the original source is a server outside the group, the original\_commit\_timestamp is preserved. The same original\_commit\_timestamp for a particular transaction is replicated to all servers in the group, and to any replica outside the group that is replicating from a member. Each recipient of the transaction also stores the local commit time in its binary log using immediate\_commit\_timestamp.

View change events, which are exclusive to Group Replication, are a special case. Transactions containing these events are generated by each group member but share the same GTID (so, they are not first executed in a source and then replicated to the group, but all members of the group execute and apply the same transaction). Group members set local timestamp values for transactions associated with view change events.

## **Monitoring Replication Delay**

One of the most common ways to monitor replication delay (lag) in previous MySQL versions was by relying on the Seconds\_Behind\_Master field in the output of SHOW REPLICA STATUS. However, this metric is not suitable when using replication topologies more complex than the traditional sourcereplica setup, such as Group Replication. The addition of immediate\_commit\_timestamp and original\_commit\_timestamp to MySQL 8 provides a much finer degree of information about replication delay. The recommended method to monitor replication delay in a topology that supports these timestamps is using the following Performance Schema tables.

- replication\_connection\_status: current status of the connection to the source, provides information on the last and current transaction the connection thread queued into the relay log.
- replication\_applier\_status\_by\_coordinator: current status of the coordinator thread that only displays information when using a multithreaded replica, provides information on the last transaction buffered by the coordinator thread to a worker's queue, as well as the transaction it is currently buffering.
- replication\_applier\_status\_by\_worker: current status of the thread(s) applying transactions received from the source, provides information about the transactions applied by the replication SQL thread, or by each worker thread when using a multithreaded replica.

Using these tables you can monitor information about the last transaction the corresponding thread processed and the transaction that thread is currently processing. This information comprises:

- a transaction's GTID
- a transaction's original\_commit\_timestamp and immediate\_commit\_timestamp, retrieved from the replica's relay log
- the time a thread started processing a transaction
- for the last processed transaction, the time the thread finished processing it

In addition to the Performance Schema tables, the output of SHOW REPLICA STATUS has three fields that show:

- SQL\_Delay: A nonnegative integer indicating the replication delay configured using CHANGE REPLICATION SOURCE TO SOURCE\_DELAY=N, where N is measured in seconds.
- SQL\_Remaining\_Delay: When Replica\_SQL\_Running\_State is Waiting until SOURCE\_DELAY seconds after master executed event, this field contains an integer indicating the number of seconds left of the delay. At other times, this field is NULL.
- Replica\_SQL\_Running\_State: A string indicating the state of the SQL thread (analogous to Replica\_IO\_State). The value is identical to the State value of the SQL thread as displayed by SHOW PROCESSLIST.

When the replication SQL thread is waiting for the delay to elapse before executing an event, SHOW PROCESSLIST displays its State value as Waiting until SOURCE\_DELAY seconds after master executed event.