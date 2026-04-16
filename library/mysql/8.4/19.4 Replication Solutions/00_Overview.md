---
source: MySQL 8.4 Reference
title: 00_Overview
---

Replication can be used in many different environments for a range of purposes. This section provides general notes and advice on using replication for specific solution types.

For information on using replication in a backup environment, including notes on the setup, backup procedure, and files to back up, see [Section 19.4.1, "Using Replication for Backups".](#page-152-0)

For advice and tips on using different storage engines on the source and replica, see [Section 19.4.4,](#page-158-0) ["Using Replication with Different Source and Replica Storage Engines"](#page-158-0).

Using replication as a scale-out solution requires some changes in the logic and operation of applications that use the solution. See [Section 19.4.5, "Using Replication for Scale-Out".](#page-159-0)

For performance or data distribution reasons, you may want to replicate different databases to different replicas. See [Section 19.4.6, "Replicating Different Databases to Different Replicas"](#page-161-0)

As the number of replicas increases, the load on the source can increase and lead to reduced performance (because of the need to replicate the binary log to each replica). For tips on improving your replication performance, including using a single secondary server as the source, see [Section 19.4.7, "Improving Replication Performance"](#page-162-0).

For guidance on switching sources, or converting replicas into sources as part of an emergency failover solution, see [Section 19.4.8, "Switching Sources During Failover".](#page-163-0)

For information on security measures specific to servers in a replication topology, see [Section 19.3,](#page-139-0) ["Replication Security"](#page-139-0).

# <span id="page-152-0"></span>**19.4.1 Using Replication for Backups**

To use replication as a backup solution, replicate data from the source to a replica, and then back up the replica. The replica can be paused and shut down without affecting the running operation of the source, so you can produce an effective snapshot of "live" data that would otherwise require the source to be shut down.

How you back up a database depends on its size and whether you are backing up only the data, or the data and the replica state so that you can rebuild the replica in the event of failure. There are therefore two choices:

- If you are using replication as a solution to enable you to back up the data on the source, and the size of your database is not too large, the mysqldump tool may be suitable. See [Section 19.4.1.1,](#page-152-1) ["Backing Up a Replica Using mysqldump"](#page-152-1).
- For larger databases, where mysqldump would be impractical or inefficient, you can back up the raw data files instead. Using the raw data files option also means that you can back up the binary and relay logs that make it possible to re-create the replica in the event of a replica failure. For more information, see [Section 19.4.1.2, "Backing Up Raw Data from a Replica"](#page-153-0).

Another backup strategy, which can be used for either source or replica servers, is to put the server in a read-only state. The backup is performed against the read-only server, which then is changed back to its usual read/write operational status. See [Section 19.4.1.3, "Backing Up a Source or Replica by](#page-154-0) [Making It Read Only".](#page-154-0)

## <span id="page-152-1"></span>**19.4.1.1 Backing Up a Replica Using mysqldump**

Using mysqldump to create a copy of a database enables you to capture all of the data in the database in a format that enables the information to be imported into another instance of MySQL Server (see Section 6.5.4, "mysqldump — A Database Backup Program"). Because the format of the information is SQL statements, the file can easily be distributed and applied to running servers in the event that you need access to the data in an emergency. However, if the size of your data set is very large, mysqldump may be impractical.

![](_page_152_Picture_11.jpeg)

#### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md)

When using mysqldump, you should stop replication on the replica before starting the dump process to ensure that the dump contains a consistent set of data:

1. Stop the replica from processing requests. You can stop replication completely on the replica using mysqladmin:

\$> **mysqladmin stop-replica**

Alternatively, you can stop only the replication SQL thread to pause event execution:

```
$> mysql -e 'STOP REPLICA SQL_THREAD;'
```

This enables the replica to continue to receive data change events from the source's binary log and store them in the relay logs using the replication receiver thread, but prevents the replica from executing these events and changing its data. Within busy replication environments, permitting the replication receiver thread to run during backup may speed up the catch-up process when you restart the replication applier thread.

2. Run mysqldump to dump your databases. You may either dump all databases or select databases to be dumped. For example, to dump all databases:

```
$> mysqldump --all-databases > fulldb.dump
```

3. Once the dump has completed, start replication again:

```
$> mysqladmin start-replica
```

In the preceding example, you may want to add login credentials (user name, password) to the commands, and bundle the process up into a script that you can run automatically each day.

If you use this approach, make sure you monitor the replication process to ensure that the time taken to run the backup does not affect the replica's ability to keep up with events from the source. See [Section 19.1.7.1, "Checking Replication Status".](#page-104-0) If the replica is unable to keep up, you may want to add another replica and distribute the backup process. For an example of how to configure this scenario, see [Section 19.4.6, "Replicating Different Databases to Different Replicas".](#page-161-0)

## <span id="page-153-0"></span>**19.4.1.2 Backing Up Raw Data from a Replica**

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
C:\> "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld"
```

Normally you should back up the entire data directory for the replica MySQL server. If you want to be able to restore the data and operate as a replica (for example, in the event of failure of the replica), in addition to the data, you need to have the replica's connection metadata repository and applier metadata repository, and the relay log files. These items are needed to resume replication after you restore the replica's data. Assuming tables have been used for the replica's connection metadata repository and applier metadata repository (see [Section 19.2.4, "Relay Log and Replication Metadata](#page-124-1) [Repositories"\)](#page-124-1), which is the default in MySQL 8.4, these tables are backed up along with the data directory. If files have been used for the repositories, which is deprecated, you must back these up separately. The relay log files must be backed up separately if they have been placed in a different location to the data directory.

If you lose the relay logs but still have the relay-log.info file, you can check it to determine how far the replication SQL thread has executed in the source's binary logs. Then you can use CHANGE REPLICATION SOURCE TO with the SOURCE\_LOG\_FILE and SOURCE\_LOG\_POS options to tell the replica to re-read the binary logs from that point. This requires that the binary logs still exist on the source server.

If your replica is replicating LOAD DATA statements, you should also back up any SQL\_LOAD-\* files that exist in the directory that the replica uses for this purpose. The replica needs these files to resume replication of any interrupted LOAD DATA operations. The location of this directory is the value of the system variable [replica\\_load\\_tmpdir](#page-46-0). If the server was not started with that variable set, the directory location is the value of the tmpdir system variable.

## <span id="page-154-0"></span>**19.4.1.3 Backing Up a Source or Replica by Making It Read Only**

It is possible to back up either source or replica servers in a replication setup by acquiring a global read lock and manipulating the read\_only system variable to change the read-only state of the server to be backed up:

- 1. Make the server read-only, so that it processes only retrievals and blocks updates.
- 2. Perform the backup.
- 3. Change the server back to its normal read/write state.

![](_page_154_Picture_9.jpeg)

#### **Note**

The instructions in this section place the server to be backed up in a state that is safe for backup methods that get the data from the server, such as mysqldump (see Section 6.5.4, "mysqldump — A Database Backup Program"). You should not attempt to use these instructions to make a binary backup by copying files directly because the server may still have modified data cached in memory and not flushed to disk.

The following instructions describe how to do this for a source and for a replica. For both scenarios discussed here, suppose that you have the following replication setup:

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
- Making a backup on R1 is not safe. This server is still running, and might be processing the binary log or update requests coming from client C2.

While S1 is read only, perform the backup. For example, you can use mysqldump.

After the backup operation on S1 completes, restore S1 to its normal operational state by executing these statements:

```
mysql> SET GLOBAL read_only = OFF;
mysql> UNLOCK TABLES;
```

Although performing the backup on S1 is safe (as far as the backup is concerned), it is not optimal for performance because clients of S1 are blocked from executing updates.

This strategy applies to backing up a source in a replication setup, but can also be used for a single server in a nonreplication setting.

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

After the replica is restored to normal operation, it again synchronizes to the source by catching up with any outstanding updates from the source's binary log.

# <span id="page-155-0"></span>**19.4.2 Handling an Unexpected Halt of a Replica**

In order for replication to be resilient to unexpected halts of the server (sometimes described as crashsafe) it must be possible for the replica to recover its state before halting. This section describes the impact of an unexpected halt of a replica during replication, and how to configure a replica for the best chance of recovery to continue replication.

After an unexpected halt of a replica, upon restart the replication SQL thread must recover information about which transactions have been executed already. The information required for recovery is stored

in the replica's applier metadata repository. This repository is created by default as an InnoDB table named mysql.slave\_relay\_log\_info. By using this transactional storage engine the information is always recoverable upon restart. Updates to the applier metadata repository are committed together with the transactions, meaning that the replica's progress information recorded in that repository is always consistent with what has been applied to the database, even in the event of an unexpected server halt. For more information on the applier metadata repository, see [Section 19.2.4, "Relay Log](#page-124-1) [and Replication Metadata Repositories"](#page-124-1).

DML transactions and also atomic DDL update the replication positions in the replica's applier metadata repository in the mysql.slave\_relay\_log\_info table together with applying the changes to the database, as an atomic operation. In all other cases, including DDL statements that are not fully atomic, and exempted storage engines that do not support atomic DDL, the mysql.slave\_relay\_log\_info table might be missing updates associated with replicated data if the server halts unexpectedly. Restoring updates in this case is a manual process. For details on atomic DDL support in MySQL 8.4, and the resulting behavior for the replication of certain statements, see Section 15.1.1, "Atomic Data Definition Statement Support".

The recovery process by which a replica recovers from an unexpected halt varies depending on the configuration of the replica. The details of the recovery process are influenced by the chosen method of replication, whether the replica is single-threaded or multithreaded, and the setting of relevant system variables. The overall aim of the recovery process is to identify what transactions had already been applied on the replica's database before the unexpected halt occurred, and retrieve and apply the transactions that the replica missed following the unexpected halt.

- For GTID-based replication, the recovery process needs the GTIDs of the transactions that were already received or committed by the replica. The missing transactions can be retrieved from the source using GTID auto-positioning, which automatically compares the source's transactions to the replica's transactions and identifies the missing transactions.
- For file position based replication, the recovery process needs an accurate replication SQL thread (applier) position showing the last transaction that was applied on the replica. Based on that position, the replication I/O thread (receiver) retrieves from the source's binary log all of the transactions that should be applied on the replica from that point on.

Using GTID-based replication makes it easiest to configure replication to be resilient to unexpected halts. GTID auto-positioning means the replica can reliably identify and retrieve missing transactions, even if there are gaps in the sequence of applied transactions.

The following information provides combinations of settings that are appropriate for different types of replica to guarantee recovery as far as this is under the control of replication.

![](_page_156_Picture_8.jpeg)

#### **Important**

Some factors outside the control of replication can have an impact on the replication recovery process and the overall state of replication after the recovery process. In particular, the settings that influence the recovery process for individual storage engines might result in transactions being lost in the event of an unexpected halt of a replica, and therefore unavailable to the replication recovery process. The innodb\_flush\_log\_at\_trx\_commit=1 setting mentioned in the list below is a key setting for a replication setup that uses InnoDB with transactions. However, other settings specific to InnoDB or to other storage engines, especially those relating to flushing or synchronization, can also have an impact. Always check for and apply recommendations made by your chosen storage engines about crash-safe settings.

The following combination of settings on a replica is the most resilient to unexpected halts:

• When GTID-based replication is in use ([gtid\\_mode=ON](#page-99-0)), set SOURCE\_AUTO\_POSITION=1, which activates GTID auto-positioning for the connection to the source to automatically identify and retrieve missing transactions. This option is set using a CHANGE REPLICATION SOURCE TO statement. If

the replica has multiple replication channels, you need to set this option for each channel individually. For details of how GTID auto-positioning works, see Section 19.1.3.3, "GTID Auto-Positioning". When file position based replication is in use, SOURCE\_AUTO\_POSITION=1 is not used, and instead the binary log position or relay log position is used to control where replication starts.

- When GTID-based replication is in use ([gtid\\_mode=ON](#page-99-0)), set GTID\_ONLY=1, which makes the replica use only GTIDs in the recovery process, and stop persisting binary log and relay log file names and file positions in the replication metadata repositories. This option is set using a CHANGE REPLICATION SOURCE TO statement. If the replica has multiple replication channels, you need to set this option for each channel individually. With GTID\_ONLY=1, during recovery, the file position information is ignored and GTID auto-skip is used to skip transactions that have already been supplied, rather than identifying the correct file position. This strategy is more efficient provided that you purge relay logs using the default setting for [relay\\_log\\_purge](#page-42-0), which means only one relay log file needs to be inspected.
- Set [sync\\_relay\\_log=1](#page-65-2), which instructs the replication receiver thread to synchronize the relay log to disk after each received transaction is written to it. This means the replica's record of the current position read from the source's binary log (in the applier metadata repository) is never ahead of the record of transactions saved in the relay log. Note that although this setting is the safest, it is also the slowest due to the number of disk writes involved. With sync\_relay\_log > 1, or sync\_relay\_log=0 (where synchronization is handled by the operating system), in the event of an unexpected halt of a replica there might be committed transactions that have not been synchronized to disk. Such transactions can cause the recovery process to fail if the recovering replica, based on the information it has in the relay log as last synchronized to disk, tries to retrieve and apply the transactions again instead of skipping them. Setting sync\_relay\_log=1 is particularly important for a multi-threaded replica, where the recovery process fails if gaps in the sequence of transactions cannot be filled using the information in the relay log. For a single-threaded replica, the recovery process only needs to use the relay log if the relevant information is not available in the applier metadata repository.
- Set innodb\_flush\_log\_at\_trx\_commit=1, which synchronizes the InnoDB logs to disk before each transaction is committed. This setting, which is the default, ensures that InnoDB tables and the InnoDB logs are saved on disk so that there is no longer a requirement for the information in the relay log regarding the transaction. Combined with the setting [sync\\_relay\\_log=1](#page-65-2), this setting further ensures that the content of the InnoDB tables and the InnoDB logs is consistent with the content of the relay log at all times, so that purging the relay log files cannot cause unfillable gaps in the replica's history of transactions in the event of an unexpected halt.
- Set [relay\\_log\\_info\\_repository = TABLE](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.md#sysvar_relay_log_info_repository), which stores the replication SQL thread position in the InnoDB table mysql.slave\_relay\_log\_info, and updates it together with the transaction commit to ensure a record that is always accurate. This setting is the default; FILE is deprecated. The system variable itself is also deprecated, so omit it and allow it to assume the default. If FILE is used, the information is stored in a file in the data directory that is updated after the transaction has been applied. This creates a risk of losing synchrony with the source depending at which stage of processing a transaction the replica halts at, or even corruption of the file itself. With [relay\\_log\\_info\\_repository = FILE](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.md#sysvar_relay_log_info_repository), recovery is not guaranteed.
- Set [relay\\_log\\_recovery = ON](#page-42-1), which enables automatic relay log recovery immediately following server startup. This global variable defaults to OFF and is read-only at runtime, but you can set it to ON with the [--relay-log-recovery](#page-42-1) option at replica startup following an unexpected halt of a replica. Note that this setting ignores the existing relay log files, in case they are corrupted or inconsistent. The relay log recovery process starts a new relay log file and fetches transactions from the source beginning at the replication SQL thread position recorded in the applier metadata repository. The previous relay log files are removed over time by the replica's normal purge mechanism.

For a multithreaded replica, setting [relay\\_log\\_recovery = ON](#page-42-1) automatically handles any inconsistencies and gaps in the sequence of transactions that have been executed from the relay log. These gaps can occur when file position based replication is in use. (For more details, see [Section 19.5.1.34, "Replication and Transaction Inconsistencies"](#page-196-0).) The relay log recovery process deals with gaps using the same method as the START REPLICA UNTIL SQL\_AFTER\_MTS\_GAPS statement would. When the replica reaches a consistent gap-free state, the relay log recovery process goes on to fetch further transactions from the source beginning at the replication SQL thread position. When GTID-based replication is in use, a multithreaded replica checks first whether SOURCE\_AUTO\_POSITION is set to ON, and if it is, omits the step of calculating the transactions that should be skipped or not skipped, so that the old relay logs are not required for the recovery process.