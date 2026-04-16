---
source: MySQL 8.4 Reference
title: 00_Overview
---

In addition to the built-in asynchronous replication, MySQL 8.4 supports an interface to semisynchronous replication that is implemented by plugins. This section discusses what semisynchronous replication is and how it works. The following sections cover the administrative interface to semisynchronous replication and how to install, configure, and monitor it.

MySQL replication by default is asynchronous. The source writes events to its binary log and replicas request them when they are ready. The source does not know whether or when a replica has retrieved and processed the transactions, and there is no guarantee that any event ever reaches any replica. With asynchronous replication, if the source crashes, transactions that it has committed might not have been transmitted to any replica. Failover from source to replica in this case might result in failover to a server that is missing transactions relative to the source.

With fully synchronous replication, when a source commits a transaction, all replicas have also committed the transaction before the source returns to the session that performed the transaction. Fully synchronous replication means failover from the source to any replica is possible at any time. The drawback of fully synchronous replication is that there might be a lot of delay to complete a transaction.

Semisynchronous replication falls between asynchronous and fully synchronous replication. The source waits until at least one replica has received and logged the events (the required number of replicas is configurable), and then commits the transaction. The source does not wait for all replicas to acknowledge receipt, and it requires only an acknowledgement from the replicas, not that the events have been fully executed and committed on the replica side. Semisynchronous replication therefore guarantees that if the source crashes, all the transactions that it has committed have been transmitted to at least one replica.

Compared to asynchronous replication, semisynchronous replication provides improved data integrity, because when a commit returns successfully, it is known that the data exists in at least two places. Until a semisynchronous source receives acknowledgment from the required number of replicas, the transaction is on hold and not committed.

Compared to fully synchronous replication, semisynchronous replication is faster, because it can be configured to balance your requirements for data integrity (the number of replicas acknowledging receipt of the transaction) with the speed of commits, which are slower due to the need to wait for replicas.

![](_page_169_Picture_9.jpeg)

#### **Important**

With semisynchronous replication, if the source crashes and a failover to a replica is carried out, the failed source should not be reused as the replication source, and should be discarded. It could have transactions that were not acknowledged by any replica, which were therefore not committed before the failover.

If your goal is to implement a fault-tolerant replication topology where all the servers receive the same transactions in the same order, and a server that crashes can rejoin the group and be brought up to date automatically, you can use Group Replication to achieve this. For information, see Chapter 20, Group Replication.

The performance impact of semisynchronous replication compared to asynchronous replication is the tradeoff for increased data integrity. The amount of slowdown is at least the TCP/IP roundtrip time to send the commit to the replica and wait for the acknowledgment of receipt by the replica. This means that semisynchronous replication works best for close servers communicating over fast networks, and worst for distant servers communicating over slow networks. Semisynchronous replication also places a rate limit on busy sessions by constraining the speed at which binary log events can be sent from source to replica. When one user is too busy, this slows it down, which can be useful in some deployment situations.

Semisynchronous replication between a source and its replicas operates as follows:

- A replica indicates whether it is semisynchronous-capable when it connects to the source.
- If semisynchronous replication is enabled on the source side and there is at least one semisynchronous replica, a thread that performs a transaction commit on the source blocks and waits until at least one semisynchronous replica acknowledges that it has received all events for the transaction, or until a timeout occurs.
- The replica acknowledges receipt of a transaction's events only after the events have been written to its relay log and flushed to disk.
- If a timeout occurs without any replica having acknowledged the transaction, the source reverts to asynchronous replication. When at least one semisynchronous replica catches up, the source returns to semisynchronous replication.
- Semisynchronous replication must be enabled on both the source and replica sides. If semisynchronous replication is disabled on the source, or enabled on the source but on no replicas, the source uses asynchronous replication.

While the source is blocking (waiting for acknowledgment from a replica), it does not return to the session that performed the transaction. When the block ends, the source returns to the session, which then can proceed to execute other statements. At this point, the transaction has committed on the source side, and receipt of its events has been acknowledged by at least one replica. The number of replica acknowledgments the source must receive per transaction before returning to the session is configurable, and defaults to one acknowledgement (see [Section 19.4.10.2, "Configuring](#page-172-0) [Semisynchronous Replication"](#page-172-0)).

Blocking also occurs after rollbacks that are written to the binary log, which occurs when a transaction that modifies nontransactional tables is rolled back. The rolled-back transaction is logged even though it has no effect for transactional tables because the modifications to the nontransactional tables cannot be rolled back and must be sent to replicas.

For statements that do not occur in transactional context (that is, when no transaction has been started with START TRANSACTION or SET autocommit = 0), autocommit is enabled and each statement commits implicitly. With semisynchronous replication, the source blocks for each such statement, just as it does for explicit transaction commits.

By default, the source waits for replica acknowledgment of the transaction receipt after syncing the binary log to disk, but before committing the transaction to the storage engine. As an alternative, you can configure the source so that the source waits for replica acknowledgment after committing the transaction to the storage engine, using the [rpl\\_semi\\_sync\\_source\\_wait\\_point](#page-26-1) system variable. This setting affects the replication characteristics and the data that clients can see on the source. For more information, see [Section 19.4.10.2, "Configuring Semisynchronous Replication"](#page-172-0).

You can improve the performance of semisynchronous replication by enabling the system variables [replication\\_sender\\_observe\\_commit\\_only](#page-53-1), which limits callbacks, and [replication\\_optimize\\_for\\_static\\_plugin\\_config](#page-53-0), which adds shared locks and avoids unnecessary lock acquisitions. These settings help as the number of replicas increases, because contention for locks can slow down performance. Semisynchronous replication source servers can also get performance benefits from enabling these system variables, because they use the same locking mechanisms as the replicas.

## <span id="page-170-0"></span>**19.4.10.1 Installing Semisynchronous Replication**

Semisynchronous replication is implemented using plugins, which must be installed on the source and on the replicas to make semisynchronous replication available on the instances. There are different plugins for a source and for a replica. After a plugin has been installed, you control it by means of the

system variables associated with it. These system variables are available only when the associated plugin has been installed.

This section describes how to install the semisynchronous replication plugins. For general information about installing plugins, see Section 7.6.1, "Installing and Uninstalling Plugins".

To use semisynchronous replication, the following requirements must be satisfied:

- The capability of installing plugins requires a MySQL server that supports dynamic loading. To verify this, check that the value of the have\_dynamic\_loading system variable is YES. Binary distributions should support dynamic loading.
- Replication must already be working, see Section 19.1, "Configuring Replication".
- There must not be multiple replication channels configured. Semisynchronous replication is only compatible with the default replication channel. See [Section 19.2.2, "Replication Channels"](#page-118-0).

MySQL 8.4 supplies versions of the plugins that implement semisynchronous replication—one for the source server and one for the replica—which replace the terms "master" and "slave" with "source" and "replica" in system variables and status variables; you can (and should) install these versions instead of the old ones (which are now deprecated, and thus subject to removal in a future MySQL release). You cannot have both the new and the old versions of the relevant plugin installed on an instance. If you use the new versions of the plugins, the new system variables and status variables are available but the old ones are not; if you use the old versions of the plugins, the old system variables and status variables are available but the new ones are not.

The file name suffix for the plugin library files differs per platform (for example, .so for Unix and Unixlike systems, and .dll for Windows). The plugin and library file names are as follows:

- Source server: rpl\_semi\_sync\_source plugin (semisync\_source.so or semisync\_source.dll library)
- Replica: rpl\_semi\_sync\_replica plugin (semisync\_replica.so or semisync\_replica.dll library)

To be usable by a source or replica server, the appropriate plugin library file must be located in the MySQL plugin directory (the directory named by the plugin\_dir system variable). If necessary, configure the plugin directory location by setting the value of plugin\_dir at server startup. The source plugin library file must be present in the plugin directory of the source server. The replica plugin library file must be present in the plugin directory of each replica server.

To set up semisynchronous replication, use the following instructions. The INSTALL PLUGIN, SET GLOBAL, STOP REPLICA, and START REPLICA statements mentioned here require the REPLICATION\_SLAVE\_ADMIN privilege (or the deprecated SUPER privilege).

To load the plugins, use the INSTALL PLUGIN statement on the source and on each replica that is to be semisynchronous, adjusting the .so suffix for your platform as necessary.

On the source:

```
INSTALL PLUGIN rpl_semi_sync_source SONAME 'semisync_source.so';
```

On each replica:

```
INSTALL PLUGIN rpl_semi_sync_replica SONAME 'semisync_replica.so';
```

If an attempt to install a plugin results in an error on Linux similar to that shown here, you must install libimf:

```
mysql> INSTALL PLUGIN rpl_semi_sync_source SONAME 'semisync_source.so';
ERROR 1126 (HY000): Can't open shared library
'/usr/local/mysql/lib/plugin/semisync_source.so'
(errno: 22 libimf.so: cannot open shared object file:
No such file or directory)
```

You can obtain libimf from<https://dev.mysql.com/downloads/os-linux.html>.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS statement (see Section 7.6.2, "Obtaining Server Plugin Information"). For example:

```
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
 FROM INFORMATION_SCHEMA.PLUGINS
 WHERE PLUGIN_NAME LIKE '%semi%';
+----------------------+---------------+
| PLUGIN_NAME | PLUGIN_STATUS |
+----------------------+---------------+
| rpl_semi_sync_source | ACTIVE |
+----------------------+---------------+
```

If a plugin fails to initialize, check the server error log for diagnostic messages.

After a semisynchronous replication plugin has been installed, it is disabled by default. The plugins must be enabled both on the source side and the replica side to enable semisynchronous replication. If only one side is enabled, replication is asynchronous. To enable the plugins, set the appropriate system variable either at runtime using SET GLOBAL, or at server startup on the command line or in an option file. For example:

```
SET GLOBAL rpl_semi_sync_source_enabled = 1;
SET GLOBAL rpl_semi_sync_replica_enabled = 1;
```

If you enable semisynchronous replication on a replica at runtime, you must also start the replication I/ O (receiver) thread (stopping it first if it is already running) to cause the replica to connect to the source and register as a semisynchronous replica:

```
STOP REPLICA IO_THREAD;
START REPLICA IO_THREAD;
```

If the replication I/O (receiver) thread is already running and you do not restart it, the replica continues to use asynchronous replication.

A setting listed in an option file takes effect each time the server starts. For example, you can set the variables in my.cnf files on the source and replica servers as follows. On the source:

```
[mysqld]
rpl_semi_sync_source_enabled=1
```

On each replica:

```
[mysqld]
rpl_semi_sync_replica_enabled=1
```

You can configure the behavior of the semisynchronous replication plugins using the system variables that become available when you install the plugins. For information on key system variables, see [Section 19.4.10.2, "Configuring Semisynchronous Replication".](#page-172-0)

## <span id="page-172-0"></span>**19.4.10.2 Configuring Semisynchronous Replication**

When you install the source and replica plugins for semisynchronous replication (see [Section 19.4.10.1, "Installing Semisynchronous Replication"](#page-170-0)), system variables become available to control plugin behavior.

To check the current values of the status variables for semisynchronous replication, use SHOW VARIABLES:

```
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
```

All the rpl\_semi\_sync\_xxx system variables are described at [Section 19.1.6.2, "Replication Source](#page-17-0) [Options and Variables"](#page-17-0) and [Section 19.1.6.3, "Replica Server Options and Variables"](#page-27-0). Some key system variables are:

- [rpl\\_semi\\_sync\\_source\\_enabled](#page-24-1) Controls whether semisynchronous replication is enabled on the source server. To enable or disable the plugin, set this variable to 1 or 0, respectively. The default is 0 (off).
- [rpl\\_semi\\_sync\\_replica\\_enabled](#page-56-0) Controls whether semisynchronous replication is enabled on the replica.
- [rpl\\_semi\\_sync\\_source\\_timeout](#page-24-2) A value in milliseconds that controls how long the source waits on a commit for acknowledgment from a replica before timing out and reverting to asynchronous replication. The default value is 10000 (10 seconds).
- [rpl\\_semi\\_sync\\_source\\_wait\\_for\\_replica\\_count](#page-25-1) Controls the number of replica acknowledgments the source must receive per transaction before returning to the session. The default is 1, meaning that the source only waits for one replica to acknowledge receipt of the transaction's events.

The [rpl\\_semi\\_sync\\_source\\_wait\\_point](#page-26-1) system variable controls the point at which a semisynchronous source server waits for replica acknowledgment of transaction receipt before returning a status to the client that committed the transaction. These values are permitted:

- AFTER\_SYNC (the default): The source writes each transaction to its binary log and the replica, and syncs the binary log to disk. The source waits for replica acknowledgment of transaction receipt after the sync. Upon receiving acknowledgment, the source commits the transaction to the storage engine and returns a result to the client, which then can proceed.
- AFTER\_COMMIT: The source writes each transaction to its binary log and the replica, syncs the binary log, and commits the transaction to the storage engine. The source waits for replica acknowledgment of transaction receipt after the commit. Upon receiving acknowledgment, the source returns a result to the client, which then can proceed.

The replication characteristics of these settings differ as follows:

- With AFTER\_SYNC, all clients see the committed transaction at the same time, which is after it has been acknowledged by the replica and committed to the storage engine on the source. Thus, all clients see the same data on the source.
  - In the event of source failure, all transactions committed on the source have been replicated to the replica (saved to its relay log). An unexpected exit of the source and failover to the replica is lossless because the replica is up to date. As noted above, the source should not be reused after the failover.
- With AFTER\_COMMIT, the client issuing the transaction gets a return status only after the server commits to the storage engine and receives replica acknowledgment. After the commit and before replica acknowledgment, other clients can see the committed transaction before the committing client.

If something goes wrong such that the replica does not process the transaction, then in the event of an unexpected source exit and failover to the replica, it is possible for such clients to see a loss of data relative to what they saw on the source.

You can improve the performance of semisynchronous replication by enabling the system variables [replication\\_sender\\_observe\\_commit\\_only](#page-53-1), which limits callbacks, and [replication\\_optimize\\_for\\_static\\_plugin\\_config](#page-53-0), which adds shared locks and avoids unnecessary lock acquisitions. These settings help as the number of replicas increases, because contention for locks can slow down performance. Semisynchronous replication source servers can also get performance benefits from enabling these system variables, because they use the same locking mechanisms as the replicas.