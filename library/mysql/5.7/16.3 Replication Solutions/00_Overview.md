---
source: MySQL 5.7 Reference
title: 00_Overview
---

Replication can be used in many different environments for a range of purposes. This section provides general notes and advice on using replication for specific solution types.

For information on using replication in a backup environment, including notes on the setup, backup procedure, and files to back up, see [Section 16.3.1, "Using Replication for Backups".](#page-136-0)

For advice and tips on using different storage engines on the source and replicas, see [Section 16.3.3,](#page-141-0) ["Using Replication with Different Source and Replica Storage Engines"](#page-141-0).

Using replication as a scale-out solution requires some changes in the logic and operation of applications that use the solution. See [Section 16.3.4, "Using Replication for Scale-Out".](#page-142-0)

For performance or data distribution reasons, you may want to replicate different databases to different replicas. See [Section 16.3.5, "Replicating Different Databases to Different Replicas"](#page-144-0)

As the number of replicas increases, the load on the source can increase and lead to reduced performance (because of the need to replicate the binary log to each replica). For tips on improving your replication performance, including using a single secondary server as a replication source server, see [Section 16.3.6, "Improving Replication Performance"](#page-145-0).

For guidance on switching sources, or converting replicas into sources as part of an emergency failover solution, see [Section 16.3.7, "Switching Sources During Failover".](#page-146-0)

To secure your replication communication, you can encrypt the communication channel. For step-bystep instructions, see [Section 16.3.8, "Setting Up Replication to Use Encrypted Connections".](#page-148-0)

## <span id="page-136-0"></span>**16.3.1 Using Replication for Backups**

To use replication as a backup solution, replicate data from the source to a replica, and then back up the replica. The replica can be paused and shut down without affecting the running operation of the source, so you can produce an effective snapshot of "live" data that would otherwise require the source to be shut down.

How you back up a database depends on its size and whether you are backing up only the data, or the data and the replica state so that you can rebuild the replica in the event of failure. There are therefore two choices:

- If you are using replication as a solution to enable you to back up the data on the source, and the size of your database is not too large, the mysqldump tool may be suitable. See [Section 16.3.1.1,](#page-136-1) ["Backing Up a Replica Using mysqldump"](#page-136-1).
- For larger databases, where mysqldump would be impractical or inefficient, you can back up the raw data files instead. Using the raw data files option also means that you can back up the binary and relay logs that enable you to re-create the replica in the event of a replica failure. For more information, see [Section 16.3.1.2, "Backing Up Raw Data from a Replica"](#page-137-0).

Another backup strategy, which can be used for either source or replica servers, is to put the server in a read-only state. The backup is performed against the read-only server, which then is changed back to its usual read/write operational status. See [Section 16.3.1.3, "Backing Up a Source or Replica by](#page-137-1) [Making It Read Only".](#page-137-1)

## <span id="page-136-1"></span>**16.3.1.1 Backing Up a Replica Using mysqldump**

Using mysqldump to create a copy of a database enables you to capture all of the data in the database in a format that enables the information to be imported into another instance of MySQL Server (see Section 4.5.4, "mysqldump — A Database Backup Program"). Because the format of the information is SQL statements, the file can easily be distributed and applied to running servers in the event that you need access to the data in an emergency. However, if the size of your data set is very large, mysqldump may be impractical.

When using mysqldump, you should stop replication on the replica before starting the dump process to ensure that the dump contains a consistent set of data:

1. Stop the replica from processing requests. You can stop replication completely on the replica using mysqladmin:

```
$> mysqladmin stop-slave
```

Alternatively, you can stop only the replication SQL thread to pause event execution:

```
$> mysql -e 'STOP SLAVE SQL_THREAD;'
```

This enables the replica to continue to receive data change events from the source's binary log and store them in the relay logs using the I/O thread, but prevents the replica from executing these events and changing its data. Within busy replication environments, permitting the I/O thread to run during backup may speed up the catch-up process when you restart the replication SQL thread.

2. Run mysqldump to dump your databases. You may either dump all databases or select databases to be dumped. For example, to dump all databases:

```
$> mysqldump --all-databases > fulldb.dump
```

3. Once the dump has completed, start replica operations again:

```
$> mysqladmin start-slave
```

In the preceding example, you may want to add login credentials (user name, password) to the commands, and bundle the process up into a script that you can run automatically each day.

If you use this approach, make sure you monitor the replication process to ensure that the time taken to run the backup does not affect the replica's ability to keep up with events from the source. See [Section 16.1.7.1, "Checking Replication Status".](#page-104-0) If the replica is unable to keep up, you may want to add another replica and distribute the backup process. For an example of how to configure this scenario, see [Section 16.3.5, "Replicating Different Databases to Different Replicas".](#page-144-0)

## <span id="page-137-0"></span>**16.3.1.2 Backing Up Raw Data from a Replica**

To guarantee the integrity of the files that are copied, backing up the raw data files on your MySQL replica should take place while your replica server is shut down. If the MySQL server is still running, background tasks may still be updating the database files, particularly those involving storage engines with background processes such as InnoDB. With InnoDB, these problems should be resolved during crash recovery, but since the replica server can be shut down during the backup process without affecting the execution of the source it makes sense to take advantage of this capability.

To shut down the server and back up the files:

1. Shut down the replica MySQL server:

```
$> mysqladmin shutdown
```

2. Copy the data files. You can use any suitable copying or archive utility, including cp, tar or WinZip. For example, assuming that the data directory is located under the current directory, you can archive the entire directory as follows:

```
$> tar cf /tmp/dbbackup.tar ./data
```

3. Start the MySQL server again. Under Unix:

```
$> mysqld_safe &
```

Under Windows:

```
C:\> "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld"
```

Normally you should back up the entire data directory for the replica MySQL server. If you want to be able to restore the data and operate as a replica (for example, in the event of failure of the replica), then in addition to the replica's data, you should also back up the replica status files, the replication metadata repositories, and the relay log files. These files are needed to resume replication after you restore the replica's data.

If you lose the relay logs but still have the relay-log.info file, you can check it to determine how far the replication SQL thread has executed in the source's binary logs. Then you can use CHANGE MASTER TO with the MASTER\_LOG\_FILE and MASTER\_LOG\_POS options to tell the replica to re-read the binary logs from that point. This requires that the binary logs still exist on the source server.

If your replica is replicating LOAD DATA statements, you should also back up any SQL\_LOAD-\* files that exist in the directory that the replica uses for this purpose. The replica needs these files to resume replication of any interrupted LOAD DATA operations. The location of this directory is the value of the [slave\\_load\\_tmpdir](#page-67-0) system variable. If the server was not started with that variable set, the directory location is the value of the tmpdir system variable.

## <span id="page-137-1"></span>**16.3.1.3 Backing Up a Source or Replica by Making It Read Only**

It is possible to back up either source or replica servers in a replication setup by acquiring a global read lock and manipulating the read\_only system variable to change the read-only state of the server to be backed up:

1. Make the server read-only, so that it processes only retrievals and blocks updates.

- 2. Perform the backup.
- 3. Change the server back to its normal read/write state.

![](_page_138_Picture_3.jpeg)

#### **Note**

The instructions in this section place the server to be backed up in a state that is safe for backup methods that get the data from the server, such as mysqldump (see Section 4.5.4, "mysqldump — A Database Backup Program"). You should not attempt to use these instructions to make a binary backup by copying files directly because the server may still have modified data cached in memory and not flushed to disk.

The following instructions describe how to do this for a source server and for a replica server. For both scenarios discussed here, suppose that you have the following replication setup:

- A source server S1
- A replica server R1 that has S1 as its source
- A client C1 connected to S1
- A client C2 connected to R1

In either scenario, the statements to acquire the global read lock and manipulate the read\_only variable are performed on the server to be backed up and do not propagate to any replicas of that server.

#### **Scenario 1: Backup with a Read-Only Source**

Put the source S1 in a read-only state by executing these statements on it:

```
mysql> FLUSH TABLES WITH READ LOCK;
mysql> SET GLOBAL read_only = ON;
```

While S1 is in a read-only state, the following properties are true:

- Requests for updates sent by C1 to S1 block because the server is in read-only mode.
- Requests for query results sent by C1 to S1 succeed.
- Making a backup on S1 is safe.
- Making a backup on R1 is not safe. This server is still running, and might be processing the binary log or update requests coming from client C2

While S1 is read only, perform the backup. For example, you can use mysqldump.

After the backup operation on S1 completes, restore S1 to its normal operational state by executing these statements:

```
mysql> SET GLOBAL read_only = OFF;
mysql> UNLOCK TABLES;
```

Although performing the backup on S1 is safe (as far as the backup is concerned), it is not optimal for performance because clients of S1 are blocked from executing updates.

This strategy applies to backing up a source server in a replication setup, but can also be used for a single server in a nonreplication setting.

#### **Scenario 2: Backup with a Read-Only Replica**

Put the replica R1 in a read-only state by executing these statements on it:

```
mysql> FLUSH TABLES WITH READ LOCK;
mysql> SET GLOBAL read_only = ON;
```

While R1 is in a read-only state, the following properties are true:

- The source S1 continues to operate, so making a backup on the source is not safe.
- The replica R1 is stopped, so making a backup on the replica R1 is safe.

These properties provide the basis for a popular backup scenario: Having one replica busy performing a backup for a while is not a problem because it does not affect the entire network, and the system is still running during the backup. In particular, clients can still perform updates on the source server, which remains unaffected by backup activity on the replica.

While R1 is read only, perform the backup. For example, you can use mysqldump.

After the backup operation on R1 completes, restore R1 to its normal operational state by executing these statements:

```
mysql> SET GLOBAL read_only = OFF;
mysql> UNLOCK TABLES;
```

After the replica is restored to normal operation, it again synchronizes to the source by catching up with any outstanding updates from the binary log of the source.

## <span id="page-139-0"></span>**16.3.2 Handling an Unexpected Halt of a Replica**

In order for replication to be resilient to unexpected halts of the server (sometimes described as crashsafe) it must be possible for the replica to recover its state before halting. This section describes the impact of an unexpected halt of a replica during replication, and how to configure a replica for the best chance of recovery to continue replication.

After an unexpected halt of a replica, upon restart the replication SQL thread must recover information about which transactions have been executed already. The information required for recovery is stored in the replica's applier metadata repository. In older MySQL Server versions, this repository could only be created as a file in the data directory that was updated after the transaction had been applied. In MySQL 5.7 you can instead use an InnoDB table named mysql.slave\_relay\_log\_info to store the applier metadata repository. As a table, updates to the applier metadata repository are committed together with the transactions, meaning that the replica's progress information recorded in that repository is always consistent with what has been applied to the database, even in the event of an unexpected server halt. To configure MySQL 5.7 to store the applier metadata repository as an InnoDB table, set the system variable [relay\\_log\\_info\\_repository](#page-59-0) to TABLE. For more information on the applier metadata repository, see [Section 16.2.4, "Relay Log and Replication](#page-123-0) [Metadata Repositories"](#page-123-0).

The recovery process by which a replica recovers from an unexpected halt varies depending on the configuration of the replica. The details of the recovery process are influenced by the chosen method of replication, whether the replica is single-threaded or multithreaded, and the setting of relevant system variables. The overall aim of the recovery process is to identify what transactions had already been applied on the replica's database before the unexpected halt occurred, and retrieve and apply the transactions that the replica missed following the unexpected halt.

- For GTID-based replication, the recovery process needs the GTIDs of the transactions that were already received or committed by the replica. The missing transactions can be retrieved from the source using GTID auto-positioning, which automatically compares the source's transactions to the replica's transactions and identifies the missing transactions.
- For file position based replication, the recovery process needs an accurate replication SQL thread (applier) position showing the last transaction that was applied on the replica. Based on that position,

the replication I/O thread (receiver) retrieves from the source's binary log all of the transactions that should be applied on the replica from that point on.

Using GTID-based replication makes it easiest to configure replication to be resilient to unexpected halts. GTID auto-positioning means the replica can reliably identify and retrieve missing transactions, even if there are gaps in the sequence of applied transactions.

The following information provides combinations of settings that are appropriate for different types of replica to guarantee recovery as far as this is under the control of replication.

![](_page_140_Picture_4.jpeg)

## **Important**

Some factors outside the control of replication can have an impact on the replication recovery process and the overall state of replication after the recovery process. In particular, the settings that influence the recovery process for individual storage engines might result in transactions being lost in the event of an unexpected halt of a replica, and therefore unavailable to the replication recovery process. The innodb\_flush\_log\_at\_trx\_commit=1 setting mentioned in the list below is a key setting for a replication setup that uses InnoDB with transactions. However, other settings specific to InnoDB or to other storage engines, especially those relating to flushing or synchronization, can also have an impact. Always check for and apply recommendations made by your chosen storage engines about crash-safe settings.

The following combination of settings on a replica is the most resilient to unexpected halts:

- When GTID-based replication is in use ([gtid\\_mode=ON](#page-101-0)), set MASTER\_AUTO\_POSITION=1, which activates GTID auto-positioning for the connection to the source to automatically identify and retrieve missing transactions. This option is set using a CHANGE MASTER TO statement. If the replica has multiple replication channels, you need to set this option for each channel individually. For details of how GTID auto-positioning works, see [Section 16.1.3.3, "GTID Auto-Positioning".](#page-7-0) When file position based replication is in use, MASTER\_AUTO\_POSITION=1 is not used, and instead the binary log position or relay log position is used to control where replication starts.
- Set [sync\\_relay\\_log=1](#page-75-0), which instructs the replication I/O thread to synchronize the relay log to disk after each received transaction is written to it. This means the replica's record of the current position read from the source's binary log (in the source metadata repository) is never ahead of the record of transactions saved in the relay log. Note that although this setting is the safest, it is also the slowest due to the number of disk writes involved. With sync\_relay\_log > 1, or sync\_relay\_log=0 (where synchronization is handled by the operating system), in the event of an unexpected halt of a replica there might be committed transactions that have not been synchronized to disk. Such transactions can cause the recovery process to fail if the recovering replica, based on the information it has in the relay log as last synchronized to disk, tries to retrieve and apply the transactions again instead of skipping them. Setting sync\_relay\_log=1 is particularly important for a multi-threaded replica, where the recovery process fails if gaps in the sequence of transactions cannot be filled using the information in the relay log. For a single-threaded replica, the recovery process only needs to use the relay log if the relevant information is not available in the applier metadata repository.
- Set innodb\_flush\_log\_at\_trx\_commit=1, which synchronizes the InnoDB logs to disk before each transaction is committed. This setting, which is the default, ensures that InnoDB tables and the InnoDB logs are saved on disk so that there is no longer a requirement for the information in the relay log regarding the transaction. Combined with the setting [sync\\_relay\\_log=1](#page-75-0), this setting further ensures that the content of the InnoDB tables and the InnoDB logs is consistent with the content of the relay log at all times, so that purging the relay log files cannot cause unfillable gaps in the replica's history of transactions in the event of an unexpected halt.
- Set [relay\\_log\\_info\\_repository = TABLE](#page-59-0), which stores the replication SQL thread position in the InnoDB table mysql.slave\_relay\_log\_info, and updates it together with the transaction commit to ensure a record that is always accurate. This setting is not the default in MySQL 5.7. If the

default FILE setting is used, the information is stored in a file in the data directory that is updated after the transaction has been applied. This creates a risk of losing synchrony with the source depending at which stage of processing a transaction the replica halts at, or even corruption of the file itself. With the setting [relay\\_log\\_info\\_repository = FILE](#page-59-0), recovery is not guaranteed.

• Set [relay\\_log\\_recovery = ON](#page-60-1), which enables automatic relay log recovery immediately following server startup. This global variable defaults to OFF and is read-only at runtime, but you can set it to ON with the [--relay-log-recovery](#page-60-1) option at replica startup following an unexpected halt of a replica. Note that this setting ignores the existing relay log files, in case they are corrupted or inconsistent. The relay log recovery process starts a new relay log file and fetches transactions from the source beginning at the replication SQL thread position recorded in the applier metadata repository. The previous relay log files are removed over time by the replica's normal purge mechanism.

For a multithreaded replica, from MySQL 5.7.13, setting [relay\\_log\\_recovery = ON](#page-60-1) automatically handles any inconsistencies and gaps in the sequence of transactions that have been executed from the relay log. These gaps can occur when file position based replication is in use. (For more details, see [Section 16.4.1.32, "Replication and Transaction Inconsistencies"](#page-174-0).) The relay log recovery process deals with gaps using the same method as the START SLAVE UNTIL SQL\_AFTER\_MTS\_GAPS statement would. When the replica reaches a consistent gap-free state, the relay log recovery process goes on to fetch further transactions from the source beginning at the replication SQL thread position. In MySQL versions prior to MySQL 5.7.13, this process was not automatic and required starting the server with [relay\\_log\\_recovery = OFF](#page-60-1), starting the replica with START SLAVE UNTIL SQL\_AFTER\_MTS\_GAPS to fix any transaction inconsistencies, and then restarting the replica with [relay\\_log\\_recovery = ON](#page-60-1). When GTID-based replication is in use, from MySQL 5.7.28 a multithreaded replica checks first whether MASTER\_AUTO\_POSITION is set to ON, and if it is, omits the step of calculating the transactions that should be skipped or not skipped, so that the old relay logs are not required for the recovery process.

# <span id="page-141-0"></span>**16.3.3 Using Replication with Different Source and Replica Storage Engines**

It does not matter for the replication process whether the source table on the source and the replicated table on the replica use different engine types. In fact, the default\_storage\_engine system variable is not replicated.

This provides a number of benefits in the replication process in that you can take advantage of different engine types for different replication scenarios. For example, in a typical scale-out scenario (see [Section 16.3.4, "Using Replication for Scale-Out"\)](#page-142-0), you want to use InnoDB tables on the source to take advantage of the transactional functionality, but use MyISAM on the replicas where transaction support is not required because the data is only read. When using replication in a data-logging environment you may want to use the Archive storage engine on the replica.

Configuring different engines on the source and replica depends on how you set up the initial replication process:

• If you used mysqldump to create the database snapshot on your source, you could edit the dump file text to change the engine type used on each table.

Another alternative for mysqldump is to disable engine types that you do not want to use on the replica before using the dump to build the data on the replica. For example, you can add the - skip-federated option on your replica to disable the FEDERATED engine. If a specific engine does not exist for a table to be created, MySQL uses the default engine type, usually MyISAM. (This requires that the NO\_ENGINE\_SUBSTITUTION SQL mode is not enabled.) If you want to disable additional engines in this way, you may want to consider building a special binary to be used on the replica that supports only the engines you want.

• If you are using raw data files (a binary backup) to set up the replica, you cannot change the initial table format. Instead, use ALTER TABLE to change the table types after the replica has been started.

• For new source/replica replication setups where there are currently no tables on the source, avoid specifying the engine type when creating new tables.

If you are already running a replication solution and want to convert your existing tables to another engine type, follow these steps:

1. Stop the replica from running replication updates:

```
mysql> STOP SLAVE;
```

This enables you to change engine types without interruptions.

- 2. Execute an ALTER TABLE ... ENGINE='engine\_type' for each table to be changed.
- 3. Start the replication process again:

```
mysql> START SLAVE;
```

Although the default\_storage\_engine variable is not replicated, be aware that CREATE TABLE and ALTER TABLE statements that include the engine specification are correctly replicated to the replica. For example, if you have a CSV table and you execute:

```
mysql> ALTER TABLE csvtable Engine='MyISAM';
```

The previous statement is replicated to the replica and the engine type on the replica is converted to MyISAM, even if you have previously changed the table type on the replica to an engine other than CSV. If you want to retain engine differences on the source and replica, you should be careful to use the default\_storage\_engine variable on the source when creating a new table. For example, instead of:

```
mysql> CREATE TABLE tablea (columna int) Engine=MyISAM;
```

Use this format:

```
mysql> SET default_storage_engine=MyISAM;
mysql> CREATE TABLE tablea (columna int);
```

When replicated, the default\_storage\_engine variable will be ignored, and the CREATE TABLE statement executes on the replica using the replica's default engine.

# <span id="page-142-0"></span>**16.3.4 Using Replication for Scale-Out**

You can use replication as a scale-out solution; that is, where you want to split up the load of database queries across multiple database servers, within some reasonable limitations.

Because replication works from the distribution of one source to one or more replicas, using replication for scale-out works best in an environment where you have a high number of reads and low number of writes/updates. Most websites fit into this category, where users are browsing the website, reading articles, posts, or viewing products. Updates only occur during session management, or when making a purchase or adding a comment/message to a forum.

Replication in this situation enables you to distribute the reads over the replicas, while still enabling your web servers to communicate with the source when a write is required. You can see a sample replication layout for this scenario in [Figure 16.1, "Using Replication to Improve Performance During](#page-143-0) [Scale-Out".](#page-143-0)

<span id="page-143-0"></span>![](_page_143_Figure_1.jpeg)

**Figure 16.1 Using Replication to Improve Performance During Scale-Out**

If the part of your code that is responsible for database access has been properly abstracted/ modularized, converting it to run with a replicated setup should be very smooth and easy. Change the implementation of your database access to send all writes to the source, and to send reads to either the source or a replica. If your code does not have this level of abstraction, setting up a replicated system gives you the opportunity and motivation to clean it up. Start by creating a wrapper library or module that implements the following functions:

- safe\_writer\_connect()
- safe\_reader\_connect()
- safe\_reader\_statement()
- safe\_writer\_statement()

safe\_ in each function name means that the function takes care of handling all error conditions. You can use different names for the functions. The important thing is to have a unified interface for connecting for reads, connecting for writes, doing a read, and doing a write.

Then convert your client code to use the wrapper library. This may be a painful and scary process at first, but it pays off in the long run. All applications that use the approach just described are able to take advantage of a source/replica configuration, even one involving multiple replicas. The code is much easier to maintain, and adding troubleshooting options is trivial. You need modify only one or two functions (for example, to log how long each statement took, or which statement among those issued gave you an error).

If you have written a lot of code, you may want to automate the conversion task by using the replace utility that comes with standard MySQL distributions, or write your own conversion script. Ideally, your code uses consistent programming style conventions. If not, then you are probably better off rewriting it anyway, or at least going through and manually regularizing it to use a consistent style.

## <span id="page-144-0"></span>**16.3.5 Replicating Different Databases to Different Replicas**

There may be situations where you have a single source and want to replicate different databases to different replicas. For example, you may want to distribute different sales data to different departments to help spread the load during data analysis. A sample of this layout is shown in [Figure 16.2,](#page-144-1) ["Replicating Databases to Separate Replicas"](#page-144-1).

**Figure 16.2 Replicating Databases to Separate Replicas**

<span id="page-144-1"></span>![](_page_144_Figure_6.jpeg)

You can achieve this separation by configuring the source and replicas as normal, and then limiting the binary log statements that each replica processes by using the [--replicate-wild-do-table](#page-51-1) configuration option on each replica.

![](_page_144_Picture_8.jpeg)

#### **Important**

You should not use [--replicate-do-db](#page-47-0) for this purpose when using statement-based replication, since statement-based replication causes this option's effects to vary according to the database that is currently selected. This applies to mixed-format replication as well, since this enables some updates to be replicated using the statement-based format.

However, it should be safe to use [--replicate-do-db](#page-47-0) for this purpose if you are using row-based replication only, since in this case the currently selected database has no effect on the option's operation.

For example, to support the separation as shown in [Figure 16.2, "Replicating Databases to Separate](#page-144-1) [Replicas",](#page-144-1) you should configure each replica as follows, before executing START SLAVE:

- Replica 1 should use --replicate-wild-do-table=databaseA.%.
- Replica 2 should use --replicate-wild-do-table=databaseB.%.
- Replica 3 should use --replicate-wild-do-table=databaseC.%.

Each replica in this configuration receives the entire binary log from the source, but executes only those events from the binary log that apply to the databases and tables included by the [-](#page-51-1) [replicate-wild-do-table](#page-51-1) option in effect on that replica.

If you have data that must be synchronized to the replicas before replication starts, you have a number of choices:

• Synchronize all the data to each replica, and delete the databases, tables, or both that you do not want to keep.

- Use mysqldump to create a separate dump file for each database and load the appropriate dump file on each replica.
- Use a raw data file dump and include only the specific files and databases that you need for each replica.

![](_page_145_Picture_3.jpeg)

#### **Note**

This does not work with InnoDB databases unless you use innodb\_file\_per\_table.

## <span id="page-145-0"></span>**16.3.6 Improving Replication Performance**

As the number of replicas connecting to a source increases, the load, although minimal, also increases, as each replica uses a client connection to the source. Also, as each replica must receive a full copy of the source's binary log, the network load on the source may also increase and create a bottleneck.

If you are using a large number of replicas connected to one source, and that source is also busy processing requests (for example, as part of a scale-out solution), then you may want to improve the performance of the replication process.

One way to improve the performance of the replication process is to create a deeper replication structure that enables the source to replicate to only one replica, and for the remaining replicas to connect to this primary replica for their individual replication requirements. A sample of this structure is shown in [Figure 16.3, "Using an Additional Replication Source to Improve Performance".](#page-145-1)

**Figure 16.3 Using an Additional Replication Source to Improve Performance**

<span id="page-145-1"></span>![](_page_145_Figure_11.jpeg)

For this to work, you must configure the MySQL instances as follows:

- Source 1 is the primary source where all changes and updates are written to the database. Binary logging should be enabled on this machine.
- Source 2 is the replica of Source 1 that provides the replication functionality to the remainder of the replicas in the replication structure. Source 2 is the only machine permitted to connect to Source 1. Source 2 also has binary logging enabled, and the [log\\_slave\\_updates](#page-93-0) system variable enabled so that replication instructions from Source 1 are also written to Source 2's binary log so that they can then be replicated to the true replicas.
- Replica 1, Replica 2, and Replica 3 act as replicas to Source 2, and replicate the information from Source 2, which actually consists of the upgrades logged on Source 1.

The above solution reduces the client load and the network interface load on the primary source, which should improve the overall performance of the primary source when used as a direct database solution.

If your replicas are having trouble keeping up with the replication process on the source, there are a number of options available:

• If possible, put the relay logs and the data files on different physical drives. To do this, set the [relay\\_log](#page-57-1) system variable to specify the location of the relay log.

- If the replicas are significantly slower than the source, you may want to divide up the responsibility for replicating different databases to different replicas. See [Section 16.3.5, "Replicating Different](#page-144-0) [Databases to Different Replicas".](#page-144-0)
- If your source makes use of transactions and you are not concerned about transaction support on your replicas, use MyISAM or another nontransactional engine on the replicas. See [Section 16.3.3,](#page-141-0) ["Using Replication with Different Source and Replica Storage Engines"](#page-141-0).
- If your replicas are not acting as sources, and you have a potential solution in place to ensure that you can bring up a source in the event of failure, then you can disable the [log\\_slave\\_updates](#page-93-0) system variable on the replicas. This prevents "dumb" replicas from also logging events they have executed into their own binary log.

## <span id="page-146-0"></span>**16.3.7 Switching Sources During Failover**

You can tell a replica to change to a new source using the CHANGE MASTER TO statement. The replica does not check whether the databases on the source are compatible with those on the replica; it simply begins reading and executing events from the specified coordinates in the new source's binary log. In a failover situation, all the servers in the group are typically executing the same events from the same binary log file, so changing the source of the events should not affect the structure or integrity of the database, provided that you exercise care in making the change.

Replicas should be run with binary logging enabled (the [--log-bin](#page-77-0) option), which is the default. If you are not using GTIDs for replication, then the replicas should also be run with [--log-slave](#page-93-0)[updates=OFF](#page-93-0) (logging replica updates is the default). In this way, the replica is ready to become a source without restarting the replica mysqld. Assume that you have the structure shown in [Figure 16.4, "Redundancy Using Replication, Initial Structure".](#page-146-1)

<span id="page-146-1"></span>**Figure 16.4 Redundancy Using Replication, Initial Structure**

In this diagram, the Source holds the source database, the Replica\* hosts are replicas, and the Web Client machines are issuing database reads and writes. Web clients that issue only reads (and would normally be connected to the replicas) are not shown, as they do not need to switch to a new server in the event of failure. For a more detailed example of a read/write scale-out replication structure, see [Section 16.3.4, "Using Replication for Scale-Out".](#page-142-0)

Each MySQL replica (Replica 1, Replica 2, and Replica 3) is a replica running with binary logging enabled, and with [--log-slave-updates=OFF](#page-93-0). Because updates received by a replica from the source are not written to the binary log when [--log-slave-updates=OFF](#page-93-0) is specified, the binary log on each replica is initially empty. If for some reason Source becomes unavailable, you can pick one of the replicas to become the new source. For example, if you pick Replica 1, all Web Clients should be redirected to Replica 1, which writes the updates to its binary log. Replica 2 and Replica 3 should then replicate from Replica 1.

The reason for running the replica with [--log-slave-updates=OFF](#page-93-0) is to prevent replicas from receiving updates twice in case you cause one of the replicas to become the new source. If Replica 1 has [--log-slave-updates](#page-93-0) enabled, which is the default, it writes any updates that it receives from Source in its own binary log. This means that, when Replica 2 changes from Source to Replica 1 as its source, it may receive updates from Replica 1 that it has already received from Source.

Make sure that all replicas have processed any statements in their relay log. On each replica, issue STOP SLAVE IO\_THREAD, then check the output of SHOW PROCESSLIST until you see Has read all relay log. When this is true for all replicas, they can be reconfigured to the new setup. On the replica Replica 1 being promoted to become the source, issue STOP SLAVE and RESET MASTER.

On the other replicas Replica 2 and Replica 3, use STOP SLAVE and CHANGE MASTER TO MASTER\_HOST='Replica1' (where 'Replica1' represents the real host name of Replica 1). To use CHANGE MASTER TO, add all information about how to connect to Replica 1 from Replica 2 or Replica 3 (user, password, port). When issuing the statement in this scenario, there is no need to specify the name of the Replica 1 binary log file or log position to read from, since the first binary log file and position 4 are the defaults. Finally, execute START SLAVE on Replica 2 and Replica 3.

Once the new replication setup is in place, you need to tell each Web Client to direct its statements to Replica 1. From that point on, all updates sent by Web Client to Replica 1 are written to the binary log of Replica 1, which then contains every update sent to Replica 1 since Source became unavailable.

The resulting server structure is shown in [Figure 16.5, "Redundancy Using Replication, After Source](#page-147-0) [Failure".](#page-147-0)

<span id="page-147-0"></span>![](_page_147_Figure_7.jpeg)

**Figure 16.5 Redundancy Using Replication, After Source Failure**

When Source becomes available again, you should make it a replica of Replica 1. To do this, issue on Source the same CHANGE MASTER TO statement as that issued on Replica 2 and Replica 3 previously. Source then becomes a replica of Replica 1 and picks up the Web Client writes that it missed while it was offline.

To make Source a source again, use the preceding procedure as if Replica 1 were unavailable and Source were to be the new source. During this procedure, do not forget to run RESET MASTER on Source before making Replica 1, Replica 2, and Replica 3 replicas of Source. If you fail to do this, the replicas may pick up stale writes from the Web Client applications dating from before the point at which Source became unavailable.

You should be aware that there is no synchronization between replicas, even when they share the same source, and thus some replicas might be considerably ahead of others. This means that in some cases the procedure outlined in the previous example might not work as expected. In practice, however, relay logs on all replicas should be relatively close together.

One way to keep applications informed about the location of the source is to have a dynamic DNS entry for the source host. With BIND, you can use nsupdate to update the DNS dynamically.

## <span id="page-148-0"></span>**16.3.8 Setting Up Replication to Use Encrypted Connections**

To use an encrypted connection for the transfer of the binary log required during replication, both the source and the replica servers must support encrypted network connections. If either server does not support encrypted connections (because it has not been compiled or configured for them), replication through an encrypted connection is not possible.

Setting up encrypted connections for replication is similar to doing so for client/server connections. You must obtain (or create) a suitable security certificate that you can use on the source, and a similar certificate (from the same certificate authority) on each replica. You must also obtain suitable key files.

For more information on setting up a server and client for encrypted connections, see Section 6.3.1, "Configuring MySQL to Use Encrypted Connections".

To enable encrypted connections on the source, you must create or obtain suitable certificate and key files, and then add the following configuration parameters to the source's configuration within the [mysqld] section of the source's my.cnf file, changing the file names as necessary:

```
[mysqld]
ssl_ca=cacert.pem
ssl_cert=server-cert.pem
ssl_key=server-key.pem
```

The paths to the files may be relative or absolute; we recommend that you always use complete paths for this purpose.

The configuration parameters are as follows:

- ssl\_ca: The path name of the Certificate Authority (CA) certificate file. (--ssl-capath is similar but specifies the path name of a directory of CA certificate files.)
- ssl\_cert: The path name of the server public key certificate file. This certificate can be sent to the client and authenticated against the CA certificate that it has.
- ssl\_key: The path name of the server private key file.

To enable encrypted connections on the replica, use the CHANGE MASTER TO statement.

• To name the replica's certificate and SSL private key files using CHANGE MASTER TO, add the appropriate MASTER\_SSL\_xxx options, like this:

```
 -> MASTER_SSL_CA = 'ca_file_name',
 -> MASTER_SSL_CAPATH = 'ca_directory_name',
 -> MASTER_SSL_CERT = 'cert_file_name',
 -> MASTER_SSL_KEY = 'key_file_name',
```

These options correspond to the --ssl-xxx options with the same names, as described in Command Options for Encrypted Connections. For these options to take effect, MASTER\_SSL=1 must also be set. For a replication connection, specifying a value for either of MASTER\_SSL\_CA or MASTER\_SSL\_CAPATH corresponds to setting --ssl-mode=VERIFY\_CA. The connection attempt succeeds only if a valid matching Certificate Authority (CA) certificate is found using the specified information.

• To activate host name identity verification, add the MASTER\_SSL\_VERIFY\_SERVER\_CERT option:

```
 -> MASTER_SSL_VERIFY_SERVER_CERT=1,
```

This option corresponds to the --ssl-verify-server-cert option, which is deprecated as of MySQL 5.7.11 and removed in MySQL 8.0. For a replication connection, specifying MASTER\_SSL\_VERIFY\_SERVER\_CERT=1 corresponds to setting --sslmode=VERIFY\_IDENTITY, as described in Command Options for Encrypted Connections. For this option to take effect, MASTER\_SSL=1 must also be set. Host name identity verification does not work with self-signed certificates.

• To activate certificate revocation list (CRL) checks, add the MASTER\_SSL\_CRL or MASTER\_SSL\_CRLPATH option, as shown here:

```
 -> MASTER_SSL_CRL = 'crl_file_name',
 -> MASTER_SSL_CRLPATH = 'crl_directory_name',
```

These options correspond to the --ssl-xxx options with the same names, as described in Command Options for Encrypted Connections. If they are not specified, no CRL checking takes place.

• To specify lists of ciphers and encryption protocols permitted by the replica for the replication connection, add the MASTER\_SSL\_CIPHER and MASTER\_TLS\_VERSION options, like this:

```
 -> MASTER_SSL_CIPHER = 'cipher_list',
 -> MASTER_TLS_VERSION = 'protocol_list',
 -> SOURCE_TLS_CIPHERSUITES = 'ciphersuite_list',
```

The MASTER\_SSL\_CIPHER option specifies the list of ciphers permitted by the replica for the replication connection, with one or more cipher names separated by colons. The MASTER\_TLS\_VERSION option specifies the encryption protocols permitted by the replica for the replication connection. The format is like that for the tls\_version system variable, with one or more comma-separated protocol versions. The protocols and ciphers that you can use in these lists depend on the SSL library used to compile MySQL. For information about the formats and permitted values, see Section 6.3.2, "Encrypted Connection TLS Protocols and Ciphers".

• After the source information has been updated, start the replication process on the replica, like this:

```
mysql> START SLAVE;
```

You can use the SHOW SLAVE STATUS statement to confirm that an encrypted connection was established successfully.

• Requiring encrypted connections on the replica does not ensure that the source requires encrypted connections from replicas. If you want to ensure that the source only accepts replicas that connect using encrypted connections, create a replication user account on the source using the REQUIRE SSL option, then grant that user the REPLICATION SLAVE privilege. For example:

```
mysql> CREATE USER 'repl'@'%.example.com' IDENTIFIED BY 'password'
 -> REQUIRE SSL;
mysql> GRANT REPLICATION SLAVE ON *.*
 -> TO 'repl'@'%.example.com';
```

If you have an existing replication user account on the source, you can add REQUIRE SSL to it with this statement:

```
mysql> ALTER USER 'repl'@'%.example.com' REQUIRE SSL;
```