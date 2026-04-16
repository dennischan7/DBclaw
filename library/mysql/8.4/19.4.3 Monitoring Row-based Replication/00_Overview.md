---
source: MySQL 8.4 Reference
title: 00_Overview
---

The current progress of the replication applier (SQL) thread when using row-based replication is monitored through Performance Schema instrument stages, enabling you to track the processing of operations and check the amount of work completed and work estimated. When these Performance Schema instrument stages are enabled the events\_stages\_current table shows stages for applier threads and their progress. For background information, see Section 29.12.5, "Performance Schema Stage Event Tables".

To track progress of all three row-based replication event types (write, update, delete):

• Enable the three Performance Schema stages by issuing:

```
mysql> UPDATE performance_schema.setup_instruments SET ENABLED = 'YES'
 -> WHERE NAME LIKE 'stage/sql/Applying batch of row changes%';
```

• Wait for some events to be processed by the replication applier thread and then check progress by looking into the events\_stages\_current table. For example to get progress for update events issue:

```
mysql> SELECT WORK_COMPLETED, WORK_ESTIMATED FROM performance_schema.events_stages_current
 -> WHERE EVENT_NAME LIKE 'stage/sql/Applying batch of row changes (update)'
```

• If [binlog\\_rows\\_query\\_log\\_events](#page-86-0) is enabled, information about queries is stored in the binary log and is exposed in the processlist\_info field. To see the original query that triggered this event:

```
mysql> SELECT db, processlist_state, processlist_info FROM performance_schema.threads
 -> WHERE processlist_state LIKE 'stage/sql/Applying batch of row changes%' AND thread_id = N;
```

# <span id="page-158-0"></span>**19.4.4 Using Replication with Different Source and Replica Storage Engines**

It does not matter for the replication process whether the original table on the source and the replicated table on the replica use different storage engine types. In fact, the default\_storage\_engine system variable is not replicated.

This provides a number of benefits in the replication process in that you can take advantage of different engine types for different replication scenarios. For example, in a typical scale-out scenario (see [Section 19.4.5, "Using Replication for Scale-Out"\)](#page-159-0), you want to use InnoDB tables on the source to take advantage of the transactional functionality, but use MyISAM on the replicas where transaction support is not required because the data is only read. When using replication in a data-logging environment you may want to use the Archive storage engine on the replica.

Configuring different engines on the source and replica depends on how you set up the initial replication process:

• If you used mysqldump to create the database snapshot on your source, you could edit the dump file text to change the engine type used on each table.

Another alternative for mysqldump is to disable engine types that you do not want to use on the replica before using the dump to build the data on the replica. For example, you can add the - skip-federated option on your replica to disable the FEDERATED engine. If a specific engine does not exist for a table to be created, MySQL uses the default engine type, usually InnoDB. (This requires that the NO\_ENGINE\_SUBSTITUTION SQL mode is not enabled.) If you want to disable

additional engines in this way, you may want to consider building a special binary to be used on the replica that supports only the engines you want.

- If you use raw data files (a binary backup) to set up the replica, it is not possible to change the initial table format. Instead, use ALTER TABLE to change the table types after the replica has been started.
- For new source/replica replication setups where there are currently no tables on the source, avoid specifying the engine type when creating new tables.

If you are already running a replication solution and want to convert your existing tables to another engine type, follow these steps:

1. Stop the replica from running replication updates:

```
mysql> STOP REPLICA;
```

This makes it possible to change engine types without interruption.

- 2. Execute an ALTER TABLE ... ENGINE='engine\_type' for each table to be changed.
- 3. Start the replication process again:

```
mysql> START REPLICA;
```

Although the default\_storage\_engine variable is not replicated, be aware that CREATE TABLE and ALTER TABLE statements that include the engine specification are replicated to the replica correctly. If, in the case of a CSV table, you execute this statement:

```
mysql> ALTER TABLE csvtable ENGINE='MyISAM';
```

This statement is replicated; the table's engine type on the replica is converted to InnoDB, even if you have previously changed the table type on the replica to an engine other than CSV. If you want to retain engine differences on the source and replica, you should be careful to use the default\_storage\_engine variable on the source when creating a new table. For example, instead of:

```
mysql> CREATE TABLE tablea (columna int) Engine=MyISAM;
```

Use this format:

```
mysql> SET default_storage_engine=MyISAM;
mysql> CREATE TABLE tablea (columna int);
```

When replicated, the default\_storage\_engine variable is ignored, and the CREATE TABLE statement executes on the replica using the replica's default engine.

# <span id="page-159-0"></span>**19.4.5 Using Replication for Scale-Out**

You can use replication as a scale-out solution; that is, where you want to split up the load of database queries across multiple database servers, within some reasonable limitations.

Because replication works from the distribution of one source to one or more replicas, using replication for scale-out works best in an environment where you have a high number of reads and low number of writes/updates. Most websites fit into this category, where users are browsing the website, reading articles, posts, or viewing products. Updates only occur during session management, or when making a purchase or adding a comment/message to a forum.

Replication in this situation enables you to distribute the reads over the replicas, while still enabling your web servers to communicate with the source when a write is required. You can see a sample replication layout for this scenario in [Figure 19.1, "Using Replication to Improve Performance During](#page-160-0) [Scale-Out".](#page-160-0)

<span id="page-160-0"></span>![](_page_160_Figure_1.jpeg)

**Figure 19.1 Using Replication to Improve Performance During Scale-Out**

If the part of your code that is responsible for database access has been properly abstracted/ modularized, converting it to run with a replicated setup should be very smooth and easy. Change the implementation of your database access to send all writes to the source, and to send reads to either the source or a replica. If your code does not have this level of abstraction, setting up a replicated system gives you the opportunity and motivation to clean it up. Start by creating a wrapper library or module that implements the following functions:

- safe\_writer\_connect()
- safe\_reader\_connect()
- safe\_reader\_statement()
- safe\_writer\_statement()

safe\_ in each function name means that the function takes care of handling all error conditions. You can use different names for the functions. The important thing is to have a unified interface for connecting for reads, connecting for writes, doing a read, and doing a write.

Then convert your client code to use the wrapper library. This may be a painful and scary process at first, but it pays off in the long run. All applications that use the approach just described are able to take advantage of a source/replica configuration, even one involving multiple replicas. The code is much easier to maintain, and adding troubleshooting options is trivial. You need modify only one or two functions (for example, to log how long each statement took, or which statement among those issued gave you an error).

If you have written a lot of code, you may want to automate the conversion task by writing a conversion script. Ideally, your code uses consistent programming style conventions. If not, then you are probably better off rewriting it anyway, or at least going through and manually regularizing it to use a consistent style.

# <span id="page-161-0"></span>**19.4.6 Replicating Different Databases to Different Replicas**

There may be situations where you have a single source server and want to replicate different databases to different replicas. For example, you may want to distribute different sales data to different departments to help spread the load during data analysis. A sample of this layout is shown in [Figure 19.2, "Replicating Databases to Separate Replicas"](#page-161-1).

**Figure 19.2 Replicating Databases to Separate Replicas**

<span id="page-161-1"></span>![](_page_161_Figure_6.jpeg)

You can achieve this separation by configuring the source and replicas as normal, and then limiting the binary log statements that each replica processes by using the [--replicate-wild-do-table](#page-35-1) configuration option on each replica.

![](_page_161_Picture_8.jpeg)

#### **Important**

You should not use [--replicate-do-db](#page-29-0) for this purpose when using statement-based replication, since statement-based replication causes this option's effects to vary according to the database that is currently selected. This applies to mixed-format replication as well, since this enables some updates to be replicated using the statement-based format.

However, it should be safe to use [--replicate-do-db](#page-29-0) for this purpose if you are using row-based replication only, since in this case the currently selected database has no effect on the option's operation.

For example, to support the separation as shown in [Figure 19.2, "Replicating Databases to Separate](#page-161-1) [Replicas",](#page-161-1) you should configure each replica as follows, before executing START REPLICA:

- Replica 1 should use --replicate-wild-do-table=databaseA.%.
- Replica 2 should use --replicate-wild-do-table=databaseB.%.
- Replica 3 should use --replicate-wild-do-table=databaseC.%.

Each replica in this configuration receives the entire binary log from the source, but executes only those events from the binary log that apply to the databases and tables included by the [-](#page-35-1) [replicate-wild-do-table](#page-35-1) option in effect on that replica.

If you have data that must be synchronized to the replicas before replication starts, you have a number of choices:

• Synchronize all the data to each replica, and delete the databases, tables, or both that you do not want to keep.

- Use mysqldump to create a separate dump file for each database and load the appropriate dump file on each replica.
- Use a raw data file dump and include only the specific files and databases that you need for each replica.

![](_page_162_Picture_3.jpeg)

#### **Note**

This does not work with InnoDB databases unless you use innodb\_file\_per\_table.

# <span id="page-162-0"></span>**19.4.7 Improving Replication Performance**

As the number of replicas connecting to a source increases, the load, although minimal, also increases, as each replica uses a client connection to the source. Also, as each replica must receive a full copy of the source's binary log, the network load on the source may also increase and create a bottleneck.

If you are using a large number of replicas connected to one source, and that source is also busy processing requests (for example, as part of a scale-out solution), then you may want to improve the performance of the replication process.

One way to improve the performance of the replication process is to create a deeper replication structure that enables the source to replicate to only one replica, and for the remaining replicas to connect to this primary replica for their individual replication requirements. A sample of this structure is shown in [Figure 19.3, "Using an Additional Replication Source to Improve Performance".](#page-162-1)

**Figure 19.3 Using an Additional Replication Source to Improve Performance**

<span id="page-162-1"></span>![](_page_162_Figure_11.jpeg)

For this to work, you must configure the MySQL instances as follows:

- Source 1 is the primary source where all changes and updates are written to the database. Binary logging is enabled on both source servers, which is the default.
- Source 2 is the replica to the server Source 1 that provides the replication functionality to the remainder of the replicas in the replication structure. Source 2 is the only machine permitted to connect to Source 1. Source 2 has the [--log-replica-updates](#page-90-0) option enabled (the default). With this option, replication instructions from Source 1 are also written to Source 2's binary log so that they can then be replicated to the true replicas.
- Replica 1, Replica 2, and Replica 3 act as replicas to Source 2, and replicate the information from Source 2, which actually consists of the upgrades logged on Source 1.

The above solution reduces the client load and the network interface load on the primary source, which should improve the overall performance of the primary source when used as a direct database solution.

If your replicas are having trouble keeping up with the replication process on the source, there are a number of options available:

- If possible, put the relay logs and the data files on different physical drives. To do this, set the [relay\\_log](#page-40-1) system variable to specify the location of the relay log.
- If heavy disk I/O activity for reads of the binary log file and relay log files is an issue, consider increasing the value of the [rpl\\_read\\_size](#page-55-1) system variable. This system variable controls the minimum amount of data read from the log files, and increasing it might reduce file reads and I/O stalls when the file data is not currently cached by the operating system. Note that a buffer the size of this value is allocated for each thread that reads from the binary log and relay log files, including dump threads on sources and coordinator threads on replicas. Setting a large value might therefore have an impact on memory consumption for servers.
- If the replicas are significantly slower than the source, you may want to divide up the responsibility for replicating different databases to different replicas. See [Section 19.4.6, "Replicating Different](#page-161-0) [Databases to Different Replicas".](#page-161-0)
- If your source makes use of transactions and you are not concerned about transaction support on your replicas, use MyISAM or another nontransactional engine on the replicas. See [Section 19.4.4,](#page-158-0) ["Using Replication with Different Source and Replica Storage Engines"](#page-158-0).
- If your replicas are not acting as sources, and you have a potential solution in place to ensure that you can bring up a source in the event of failure, then you can disable [log\\_replica\\_updates](#page-90-0). This prevents "dumb" replicas from also logging events they have executed into their own binary log.

# <span id="page-163-0"></span>**19.4.8 Switching Sources During Failover**

You can tell a replica to change to a new source using the CHANGE REPLICATION SOURCE TO statement. The replica does not check whether the databases on the source are compatible with those on the replica; it simply begins reading and executing events from the specified coordinates in the new source's binary log. In a failover situation, all the servers in the group are typically executing the same events from the same binary log file, so changing the source of the events should not affect the structure or integrity of the database, provided that you exercise care in making the change.

Replicas should be run with binary logging enabled (the [--log-bin](#page-69-0) option), which is the default. If you are not using GTIDs for replication, then the replicas should also be run with [--log-replica](#page-90-0)[updates=OFF](#page-90-0) (logging replica updates is the default). In this way, the replica is ready to become a source without restarting the replica mysqld. Assume that you have the structure shown in [Figure 19.4, "Redundancy Using Replication, Initial Structure".](#page-163-1)

<span id="page-163-1"></span>**Figure 19.4 Redundancy Using Replication, Initial Structure**

![](_page_163_Figure_10.jpeg)

In this diagram, the Source holds the source database, the Replica\* hosts are replicas, and the Web Client machines are issuing database reads and writes. Web clients that issue only reads (and would normally be connected to the replicas) are not shown, as they do not need to switch to a new server in the event of failure. For a more detailed example of a read/write scale-out replication structure, see [Section 19.4.5, "Using Replication for Scale-Out".](#page-159-0)

Each MySQL replica (Replica 1, Replica 2, and Replica 3) is a replica running with binary logging enabled, and with [--log-replica-updates=OFF](#page-90-0). Because updates received by a replica from the source are not written to the binary log when --log-replica-updates=OFF is specified, the binary log on each replica is initially empty. If for some reason Source becomes unavailable, you can pick one of the replicas to become the new source. For example, if you pick Replica 1, all Web Clients should be redirected to Replica 1, which writes the updates to its binary log. Replica 2 and Replica 3 should then replicate from Replica 1.

The reason for running the replica with [--log-replica-updates=OFF](#page-90-0) is to prevent replicas from receiving updates twice in case you cause one of the replicas to become the new source. If Replica 1 has --log-replica-updates enabled, which is the default, it writes any updates that it receives from Source in its own binary log. This means that, when Replica 2 changes from Source to Replica 1 as its source, it may receive updates from Replica 1 that it has already received from Source.

Make sure that all replicas have processed any statements in their relay log. On each replica, issue STOP REPLICA IO\_THREAD, then check the output of SHOW PROCESSLIST until you see Has read all relay log. When this is true for all replicas, they can be reconfigured to the new setup. On the replica Replica 1 being promoted to become the source, issue STOP REPLICA and RESET BINARY LOGS AND GTIDS.

On the other replicas Replica 2 and Replica 3, use STOP REPLICA and CHANGE REPLICATION SOURCE TO SOURCE\_HOST='Replica1' (where 'Replica1' represents the real host name of Replica 1). To use CHANGE REPLICATION SOURCE TO, add all information about how to connect to Replica 1 from Replica 2 or Replica 3 (user, password, port). When issuing the statement in this scenario, there is no need to specify the name of the Replica 1 binary log file or log position to read from, since the first binary log file and position 4 are the defaults. Finally, execute START REPLICA on Replica 2 and Replica 3.

Once the new replication setup is in place, you need to tell each Web Client to direct its statements to Replica 1. From that point on, all updates sent by Web Client to Replica 1 are written to the binary log of Replica 1, which then contains every update sent to Replica 1 since Source became unavailable.

The resulting server structure is shown in [Figure 19.5, "Redundancy Using Replication, After Source](#page-165-0) [Failure".](#page-165-0)

<span id="page-165-0"></span>![](_page_165_Figure_1.jpeg)

**Figure 19.5 Redundancy Using Replication, After Source Failure**

When Source becomes available again, you should make it a replica of Replica 1. To do this, issue on Source the same CHANGE REPLICATION SOURCE TO statement as that issued on Replica 2 and Replica 3 previously. Source then becomes a replica of Replica 1 and picks up the Web Client writes that it missed while it was offline.

To make Source a source again, use the preceding procedure as if Replica 1 were unavailable and Source were to be the new source. During this procedure, do not forget to run RESET BINARY LOGS AND GTIDS on Source before making Replica 1, Replica 2, and Replica 3 replicas of Source. If you fail to do this, the replicas may pick up stale writes from the Web Client applications dating from before the point at which Source became unavailable.

You should be aware that there is no synchronization between replicas, even when they share the same source, and thus some replicas might be considerably ahead of others. This means that in some cases the procedure outlined in the previous example might not work as expected. In practice, however, relay logs on all replicas should be relatively close together.

One way to keep applications informed about the location of the source is to have a dynamic DNS entry for the source host. With BIND, you can use nsupdate to update the DNS dynamically.