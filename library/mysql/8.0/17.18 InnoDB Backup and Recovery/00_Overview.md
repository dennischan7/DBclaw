---
source: MySQL 8.0 Reference
title: 00_Overview
---

This section covers topics related to InnoDB backup and recovery.

- For information about backup techniques applicable to InnoDB, see [Section 17.18.1, "InnoDB](#page-123-0) [Backup".](#page-123-0)
- For information about point-in-time recovery, recovery from disk failure or corruption, and how InnoDB performs crash recovery, see [Section 17.18.2, "InnoDB Recovery"](#page-124-0).

## <span id="page-123-0"></span>**17.18.1 InnoDB Backup**

The key to safe database management is making regular backups. Depending on your data volume, number of MySQL servers, and database workload, you can use these backup techniques, alone or in combination: hot backup with MySQL Enterprise Backup; cold backup by copying files while the MySQL server is shut down; logical backup with mysqldump for smaller data volumes or to record the structure of schema objects. Hot and cold backups are physical backups that copy actual data files, which can be used directly by the mysqld server for faster restore.

Using MySQL Enterprise Backup is the recommended method for backing up InnoDB data.

![](_page_123_Picture_13.jpeg)

#### **Note**

InnoDB does not support databases that are restored using third-party backup tools.

## **Hot Backups**

The mysqlbackup command, part of the MySQL Enterprise Backup component, lets you back up a running MySQL instance, including InnoDB tables, with minimal disruption to operations while producing a consistent snapshot of the database. When mysqlbackup is copying InnoDB tables, reads and writes to InnoDB tables can continue. MySQL Enterprise Backup can also create compressed backup files, and back up subsets of tables and databases. In conjunction with the MySQL binary log, users can perform point-in-time recovery. MySQL Enterprise Backup is part of the MySQL Enterprise subscription. For more details, see Section 32.1, "MySQL Enterprise Backup Overview".

## **Cold Backups**

If you can shut down the MySQL server, you can make a physical backup that consists of all files used by InnoDB to manage its tables. Use the following procedure:

- 1. Perform a slow shutdown of the MySQL server and make sure that it stops without errors.
- 2. Copy all InnoDB data files (ibdata files and .ibd files) into a safe place.
- 3. Copy all InnoDB redo log files (#ib\_redoN files in MySQL 8.0.30 and higher or ib\_logfile files in earlier releases) to a safe place.

4. Copy your my.cnf configuration file or files to a safe place.

## **Logical Backups Using mysqldump**

In addition to physical backups, it is recommended that you regularly create logical backups by dumping your tables using mysqldump. A binary file might be corrupted without you noticing it. Dumped tables are stored into text files that are human-readable, so spotting table corruption becomes easier. Also, because the format is simpler, the chance for serious data corruption is smaller. mysqldump also has a --single-transaction option for making a consistent snapshot without locking out other clients. See Section 9.3.1, "Establishing a Backup Policy".

Replication works with InnoDB tables, so you can use MySQL replication capabilities to keep a copy of your database at database sites requiring high availability. See [Section 17.19, "InnoDB and MySQL](#page-126-1) [Replication".](#page-126-1)

## <span id="page-124-0"></span>**17.18.2 InnoDB Recovery**

This section describes InnoDB recovery. Topics include:

- [Point-in-Time Recovery](#page-124-1)
- [Recovery from Data Corruption or Disk Failure](#page-124-2)
- [InnoDB Crash Recovery](#page-124-3)
- [Tablespace Discovery During Crash Recovery](#page-126-0)

## <span id="page-124-1"></span>**Point-in-Time Recovery**

To recover an InnoDB database to the present from the time at which the physical backup was made, you must run MySQL server with binary logging enabled, even before taking the backup. To achieve point-in-time recovery after restoring a backup, you can apply changes from the binary log that occurred after the backup was made. See Section 9.5, "Point-in-Time (Incremental) Recovery".

## <span id="page-124-2"></span>**Recovery from Data Corruption or Disk Failure**

If your database becomes corrupted or disk failure occurs, you must perform the recovery using a backup. In the case of corruption, first find a backup that is not corrupted. After restoring the base backup, do a point-in-time recovery from the binary log files using mysqlbinlog and mysql to restore the changes that occurred after the backup was made.

In some cases of database corruption, it is enough to dump, drop, and re-create one or a few corrupt tables. You can use the CHECK TABLE statement to check whether a table is corrupt, although CHECK TABLE naturally cannot detect every possible kind of corruption.

In some cases, apparent database page corruption is actually due to the operating system corrupting its own file cache, and the data on disk may be okay. It is best to try restarting the computer first. Doing so may eliminate errors that appeared to be database page corruption. If MySQL still has trouble starting because of InnoDB consistency problems, see [Section 17.21.3, "Forcing InnoDB Recovery"](#page-163-0) for steps to start the instance in recovery mode, which permits you to dump the data.

## <span id="page-124-3"></span>**InnoDB Crash Recovery**

To recover from an unexpected MySQL server exit, the only requirement is to restart the MySQL server. InnoDB automatically checks the logs and performs a roll-forward of the database to the present. InnoDB automatically rolls back uncommitted transactions that were present at the time of the crash.

InnoDB crash recovery consists of several steps:

• Tablespace discovery

Tablespace discovery is the process that InnoDB uses to identify tablespaces that require redo log application. See [Tablespace Discovery During Crash Recovery.](#page-126-0)

### • Redo log application

Redo log application is performed during initialization, before accepting any connections. If all changes are flushed from the buffer pool to the tablespaces (ibdata\* and \*.ibd files) at the time of the shutdown or crash, redo log application is skipped. InnoDB also skips redo log application if redo log files are missing at startup.

• The current maximum auto-increment counter value is written to the redo log each time the value changes, which makes it crash-safe. During recovery, InnoDB scans the redo log to collect counter value changes and applies the changes to the in-memory table object.

For more information about how InnoDB handles auto-increment values, see Section 17.6.1.6, "AUTO\_INCREMENT Handling in InnoDB", and InnoDB AUTO\_INCREMENT Counter Initialization.

- When encountering index tree corruption, InnoDB writes a corruption flag to the redo log, which makes the corruption flag crash-safe. InnoDB also writes in-memory corruption flag data to an engine-private system table on each checkpoint. During recovery, InnoDB reads corruption flags from both locations and merges results before marking in-memory table and index objects as corrupt.
- Removing redo logs to speed up recovery is not recommended, even if some data loss is acceptable. Removing redo logs should only be considered after a clean shutdown, with [innodb\\_fast\\_shutdown](#page-22-2) set to 0 or 1.
- Roll back of incomplete transactions

Incomplete transactions are any transactions that were active at the time of unexpected exit or fast shutdown. The time it takes to roll back an incomplete transaction can be three or four times the amount of time a transaction is active before it is interrupted, depending on server load.

You cannot cancel transactions that are being rolled back. In extreme cases, when rolling back transactions is expected to take an exceptionally long time, it may be faster to start InnoDB with an [innodb\\_force\\_recovery](#page-30-0) setting of 3 or greater. See [Section 17.21.3, "Forcing InnoDB](#page-163-0) [Recovery".](#page-163-0)

## • Change buffer merge

Applying changes from the change buffer (part of the system tablespace) to leaf pages of secondary indexes, as the index pages are read to the buffer pool.

## • Purge

Deleting delete-marked records that are no longer visible to active transactions.

The steps that follow redo log application do not depend on the redo log (other than for logging the writes) and are performed in parallel with normal processing. Of these, only rollback of incomplete transactions is special to crash recovery. The insert buffer merge and the purge are performed during normal processing.

After redo log application, InnoDB attempts to accept connections as early as possible, to reduce downtime. As part of crash recovery, InnoDB rolls back transactions that were not committed or in XA PREPARE state when the server exited. The rollback is performed by a background thread, executed in parallel with transactions from new connections. Until the rollback operation is completed, new connections may encounter locking conflicts with recovered transactions.

In most situations, even if the MySQL server was killed unexpectedly in the middle of heavy activity, the recovery process happens automatically and no action is required of the DBA. If a hardware

failure or severe system error corrupted InnoDB data, MySQL might refuse to start. In this case, see [Section 17.21.3, "Forcing InnoDB Recovery"](#page-163-0).

For information about the binary log and InnoDB crash recovery, see Section 7.4.4, "The Binary Log".

## <span id="page-126-0"></span>**Tablespace Discovery During Crash Recovery**

If, during recovery, InnoDB encounters redo logs written since the last checkpoint, the redo logs must be applied to affected tablespaces. The process that identifies affected tablespaces during recovery is referred to as tablespace discovery.

Tablespace discovery relies on the [innodb\\_directories](#page-19-0) setting, which defines the directories to scan at startup for tablespace files. The [innodb\\_directories](#page-19-0) default setting is NULL, but the directories defined by [innodb\\_data\\_home\\_dir](#page-16-1), [innodb\\_undo\\_directory](#page-73-0), and datadir are always appended to the [innodb\\_directories](#page-19-0) argument value when InnoDB builds a list of directories to scan at startup. These directories are appended regardless of whether an [innodb\\_directories](#page-19-0) setting is specified explicitly. Tablespace files defined with an absolute path or that reside outside of the directories appended to the [innodb\\_directories](#page-19-0) setting should be added to the [innodb\\_directories](#page-19-0) setting. Recovery is terminated if any tablespace file referenced in a redo log has not been discovered previously.

# <span id="page-126-1"></span>**17.19 InnoDB and MySQL Replication**

It is possible to use replication in a way where the storage engine on the replica is not the same as the storage engine on the source. For example, you can replicate modifications to an InnoDB table on the source to a MyISAM table on the replica. For more information see, Section 19.4.4, "Using Replication with Different Source and Replica Storage Engines".

For information about setting up a replica, see Section 19.1.2.6, "Setting Up Replicas", and Section 19.1.2.5, "Choosing a Method for Data Snapshots". To make a new replica without taking down the source or an existing replica, use the MySQL Enterprise Backup product.

Transactions that fail on the source do not affect replication. MySQL replication is based on the binary log where MySQL writes SQL statements that modify data. A transaction that fails (for example, because of a foreign key violation, or because it is rolled back) is not written to the binary log, so it is not sent to replicas. See Section 15.3.1, "START TRANSACTION, COMMIT, and ROLLBACK Statements".

**Replication and CASCADE.** Cascading actions for InnoDB tables on the source are executed on the replica only if the tables sharing the foreign key relation use InnoDB on both the source and replica. This is true whether you are using statement-based or row-based replication. Suppose that you have started replication, and then create two tables on the source, where InnoDB is defined as the default storage engine, using the following CREATE TABLE statements:

```
CREATE TABLE fc1 (
 i INT PRIMARY KEY,
 j INT
);
CREATE TABLE fc2 (
 m INT PRIMARY KEY,
 n INT,
 FOREIGN KEY ni (n) REFERENCES fc1 (i)
 ON DELETE CASCADE
);
```

If the replica has MyISAM defined as the default storage engine, the same tables are created on the replica, but they use the MyISAM storage engine, and the FOREIGN KEY option is ignored. Now we insert some rows into the tables on the source:

```
source> INSERT INTO fc1 VALUES (1, 1), (2, 2);
```

```
Query OK, 2 rows affected (0.09 sec)
Records: 2 Duplicates: 0 Warnings: 0
source> INSERT INTO fc2 VALUES (1, 1), (2, 2), (3, 1);
Query OK, 3 rows affected (0.19 sec)
Records: 3 Duplicates: 0 Warnings: 0
```

At this point, on both the source and the replica, table fc1 contains 2 rows, and table fc2 contains 3 rows, as shown here:

```
source> SELECT * FROM fc1;
+---+------+
| i | j |
+---+------+
| 1 | 1 |
| 2 | 2 |
+---+------+
2 rows in set (0.00 sec)
source> SELECT * FROM fc2;
+---+------+
| m | n |
+---+------+
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
+---+------+
3 rows in set (0.00 sec)
replica> SELECT * FROM fc1;
+---+------+
| i | j |
+---+------+
| 1 | 1 |
| 2 | 2 |
+---+------+
2 rows in set (0.00 sec)
replica> SELECT * FROM fc2;
+---+------+
| m | n |
+---+------+
| 1 | 1 |
| 2 | 2 |
| 3 | 1 |
+---+------+
3 rows in set (0.00 sec)
```

Now suppose that you perform the following DELETE statement on the source:

```
source> DELETE FROM fc1 WHERE i=1;
Query OK, 1 row affected (0.09 sec)
```

Due to the cascade, table fc2 on the source now contains only 1 row:

```
source> SELECT * FROM fc2;
+---+---+
| m | n |
+---+---+
| 2 | 2 |
+---+---+
1 row in set (0.00 sec)
```

However, the cascade does not propagate on the replica because on the replica the DELETE for fc1 deletes no rows from fc2. The replica's copy of fc2 still contains all of the rows that were originally inserted:

```
replica> SELECT * FROM fc2;
+---+---+
| m | n |
```

```
+---+---+
| 1 | 1 |
| 3 | 1 |
| 2 | 2 |
+---+---+
3 rows in set (0.00 sec)
```

This difference is due to the fact that the cascading deletes are handled internally by the InnoDB storage engine, which means that none of the changes are logged.