---
source: MySQL 8.4 Reference
title: 00_Overview
---

MySQL supports FIPS mode when a supported OpenSSL library and FIPS Object Module are available on the host system.

FIPS mode on the server side applies to cryptographic operations performed by the server. This includes replication (source/replica and Group Replication) and X Plugin, which run within the server. FIPS mode also applies to attempts by clients to connect to the server.

The following sections describe FIPS mode and how to take advantage of it within MySQL:

- [FIPS Overview](#page-36-0)
- [System Requirements for FIPS Mode in MySQL](#page-36-1)
- [Enabling FIPS Mode in MySQL](#page-37-0)

# <span id="page-36-0"></span>**FIPS Overview**

Federal Information Processing Standards 140-2 (FIPS 140-2) describes a security standard that can be required by Federal (US Government) agencies for cryptographic modules used to protect sensitive or valuable information. To be considered acceptable for such Federal use, a cryptographic module must be certified for FIPS 140-2. If a system intended to protect sensitive data lacks the proper FIPS 140-2 certificate, Federal agencies cannot purchase it.

Products such as OpenSSL can be used in FIPS mode, although the OpenSSL library itself is not validated for FIPS. Instead, the OpenSSL library is used with the OpenSSL FIPS Object Module to enable OpenSSL-based applications to operate in FIPS mode.

For general information about FIPS and its implementation in OpenSSL, these references may be helpful:

- [National Institute of Standards and Technology FIPS PUB 140-2](https://doi.org/10.6028/NIST.FIPS.140-2)
- [OpenSSL FIPS 140-2 Security Policy](https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp1747.pdf)
- [fips\\_module manual page](https://www.openssl.org/docs/man3.0/man7/fips_module.md)

![](_page_36_Picture_13.jpeg)

#### **Important**

FIPS mode imposes conditions on cryptographic operations such as restrictions on acceptable encryption algorithms or requirements for longer key lengths. For OpenSSL, the exact FIPS behavior depends on the OpenSSL version.

# <span id="page-36-1"></span>**System Requirements for FIPS Mode in MySQL**

For MySQL to support FIPS mode, these system requirements must be satisfied:

- 1. MySQL must be compiled with an OpenSSL version that is certified for use with FIPS. OpenSSL 1.0.2 and OpenSSL 3.0 are certified, but OpenSSL 1.1.1 is not. Binary distributions for recent versions of MySQL are compiled using OpenSSL 3.0 on some platforms, which means they are not certified for FIPS. This means you have the following options, depending on system and MySQL configuration:
  - Use a system that has OpenSSL 3.0 and the required FIPS object module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL 3.0, or compile MySQL from source using OpenSSL 3.0.

For general information about upgrading to OpenSSL 3.0, see [OpenSSL 3.0 Migration Guide](https://www.openssl.org/docs/man3.0/man7/migration_guide.md).

- Use a system that has OpenSSL 1.1.1 or higher. In this case, you can install MySQL using binary packages, and you can use the TLS v1.3 protocol and ciphersuites, in addition to other already supported TLS protocols. However, you cannot enable FIPS mode for MySQL.
- Use a system that has OpenSSL 1.0.2 and the required FIPS Object Module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL

1.0.2, or compile MySQL from source using OpenSSL 1.0.2. In this case, you cannot use the TLS v1.3 protocol or ciphersuites, which require OpenSSL 1.1.1 or 3.0. In addition, you should be aware that OpenSSL 1.0.2 reached end of life status in 2019, and that all operating platforms embedding OpenSSL 1.1.1 reach their end of life in 2024.

2. At runtime, the OpenSSL library and OpenSSL FIPS Object Module must be available as shared (dynamically linked) objects.

## <span id="page-37-0"></span>**Enabling FIPS Mode in MySQL**

To determine whether MySQL is running on a system with FIPS mode enabled, check the value of the ssl\_fips\_mode server system variable using an SQL statement such as SHOW VARIABLES LIKE '%fips%' or SELECT @@ssl\_fips\_mode. If the value of this variable is 1 (ON) or 2 (STRICT), FIPS mode is enabled for OpenSSL; if it is 0 (OFF), FIPS mode is not available.

![](_page_37_Picture_5.jpeg)

#### **Important**

In general, STRICT imposes more restrictions than ON, but MySQL itself has no FIPS-specific code other than to specify the FIPS mode value to OpenSSL. The exact behavior of FIPS mode for ON or STRICT depends on the OpenSSL version. For details, refer to the fips\_module manpage (see [FIPS Overview\)](#page-36-0).

FIPS mode on the server side applies to cryptographic operations performed by the server, including those performed by MySQL Replication (including Group Replication) and X Plugin, which run within the server.

FIPS mode also applies to attempts by clients to connect to the server. When enabled, on either the client or server side, it restricts which of the supported encryption ciphers can be chosen. However, enabling FIPS mode does not require that an encrypted connection must be used, or that user credentials must be encrypted. For example, if FIPS mode is enabled, stronger cryptographic algorithms are required. In particular, MD5 is restricted, so trying to establish an encrypted connection using an encryption cipher such as RC4-MD5 does not work. But there is nothing about FIPS mode that prevents establishing an unencrypted connection. (To do that, you can use the REQUIRE clause for CREATE USER or ALTER USER for specific user accounts, or set the require\_secure\_transport system variable to affect all accounts.)

If FIPS mode is required, it is recommended to use an operating platforms that includes it; if it does, you can (and should) use it. If your platform does not include FIPS, you have two options:

- Migrate to a platform which has FIPS OpenSSL support.
- Build the OpenSSL library and FIPS object module from source, using the instructions from the fips\_module manpage (see [FIPS Overview\)](#page-36-0).

![](_page_37_Picture_13.jpeg)

#### **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for ssl\_fips\_mode and --ssl-fips-mode is OFF. An error occurs for attempts to set the FIPS mode to a different value.

If FIPS mode is required, it is recommended to use an operating platform that includes it; if it does, you can (and should) use it. If your platform does not include FIPS, you have two options:

- Migrate to a platform which has FIPS OpenSSL support.
- Build the OpenSSL library and FIPS object module from source, using the instructions from the fips\_module manpage (see [FIPS Overview\)](#page-36-0).

# Chapter 9 Backup and Recovery

# **Table of Contents**

| 9.1 Backup and Recovery Types 1610                              |      |
|-----------------------------------------------------------------|------|
| 9.2 Database Backup Methods 1613                                |      |
| 9.3 Example Backup and Recovery Strategy 1615                   |      |
| 9.3.1 Establishing a Backup Policy                              | 1615 |
| 9.3.2 Using Backups for Recovery 1617                           |      |
| 9.3.3 Backup Strategy Summary 1618                              |      |
| 9.4 Using mysqldump for Backups 1618                            |      |
| 9.4.1 Dumping Data in SQL Format with mysqldump 1619            |      |
| 9.4.2 Reloading SQL-Format Backups 1620                         |      |
| 9.4.3 Dumping Data in Delimited-Text Format with mysqldump 1620 |      |
| 9.4.4 Reloading Delimited-Text Format Backups 1621              |      |
| 9.4.5 mysqldump Tips 1622                                       |      |
| 9.5 Point-in-Time (Incremental) Recovery 1624                   |      |
| 9.5.1 Point-in-Time Recovery Using Binary Log 1624              |      |
| 9.5.2 Point-in-Time Recovery Using Event Positions 1625         |      |
| 9.6 MyISAM Table Maintenance and Crash Recovery 1627            |      |
| 9.6.1 Using myisamchk for Crash Recovery 1627                   |      |
| 9.6.2 How to Check MyISAM Tables for Errors 1628                |      |
| 9.6.3 How to Repair MyISAM Tables 1629                          |      |
| 9.6.4 MyISAM Table Optimization 1631                            |      |
| 9.6.5 Setting Up a MyISAM Table Maintenance Schedule 1631       |      |
|                                                                 |      |

It is important to back up your databases so that you can recover your data and be up and running again in case problems occur, such as system crashes, hardware failures, or users deleting data by mistake. Backups are also essential as a safeguard before upgrading a MySQL installation, and they can be used to transfer a MySQL installation to another system or to set up replica servers.

MySQL offers a variety of backup strategies from which you can choose the methods that best suit the requirements for your installation. This chapter discusses several backup and recovery topics with which you should be familiar:

- Types of backups: Logical versus physical, full versus incremental, and so forth.
- Methods for creating backups.
- Recovery methods, including point-in-time recovery.
- Backup scheduling, compression, and encryption.
- Table maintenance, to enable recovery of corrupt tables.

## **Additional Resources**

Resources related to backup or to maintaining data availability include the following:

- Customers of MySQL Enterprise Edition can use the MySQL Enterprise Backup product for backups. For an overview of the MySQL Enterprise Backup product, see Section 32.1, "MySQL Enterprise Backup Overview".
- A forum dedicated to backup issues is available at [https://forums.mysql.com/list.php?28.](https://forums.mysql.com/list.php?28)
- Details for mysqldump can be found in Chapter 6, MySQL Programs.
- The syntax of the SQL statements described here is given in Chapter 15, SQL Statements.

- For additional information about InnoDB backup procedures, see Section 17.18.1, "InnoDB Backup".
- Replication enables you to maintain identical data on multiple servers. This has several benefits, such as enabling client query load to be distributed over servers, availability of data even if a given server is taken offline or fails, and the ability to make backups with no impact on the source by using a replica. See Chapter 19, Replication.
- MySQL InnoDB Cluster is a collection of products that work together to provide a high availability solution. A group of MySQL servers can be configured to create a cluster using MySQL Shell. The cluster of servers has a single source, called the primary, which acts as the read-write source. Multiple secondary servers are replicas of the source. A minimum of three servers are required to create a high availability cluster. A client application is connected to the primary via MySQL Router. If the primary fails, a secondary is automatically promoted to the role of primary, and MySQL Router routes requests to the new primary.
- NDB Cluster provides a high-availability, high-redundancy version of MySQL adapted for the distributed computing environment. See Chapter 25, MySQL NDB Cluster 8.4, which provides information about MySQL NDB Cluster 8.4.7.

# <span id="page-39-0"></span>**9.1 Backup and Recovery Types**

This section describes the characteristics of different types of backups.

## **Physical (Raw) Versus Logical Backups**

Physical backups consist of raw copies of the directories and files that store database contents. This type of backup is suitable for large, important databases that need to be recovered quickly when problems occur.

Logical backups save information represented as logical database structure (CREATE DATABASE, CREATE TABLE statements) and content (INSERT statements or delimited-text files). This type of backup is suitable for smaller amounts of data where you might edit the data values or table structure, or recreate the data on a different machine architecture.

Physical backup methods have these characteristics:

- The backup consists of exact copies of database directories and files. Typically this is a copy of all or part of the MySQL data directory.
- Physical backup methods are faster than logical because they involve only file copying without conversion.
- Output is more compact than for logical backup.
- Because backup speed and compactness are important for busy, important databases, the MySQL Enterprise Backup product performs physical backups. For an overview of the MySQL Enterprise Backup product, see Section 32.1, "MySQL Enterprise Backup Overview".
- Backup and restore granularity ranges from the level of the entire data directory down to the level of individual files. This may or may not provide for table-level granularity, depending on storage engine. For example, InnoDB tables can each be in a separate file, or share file storage with other InnoDB tables; each MyISAM table corresponds uniquely to a set of files.
- In addition to databases, the backup can include any related files such as log or configuration files.
- Data from MEMORY tables is tricky to back up this way because their contents are not stored on disk. (The MySQL Enterprise Backup product has a feature where you can retrieve data from MEMORY tables during a backup.)
- Backups are portable only to other machines that have identical or similar hardware characteristics.

- Backups can be performed while the MySQL server is not running. If the server is running, it is necessary to perform appropriate locking so that the server does not change database contents during the backup. MySQL Enterprise Backup does this locking automatically for tables that require it.
- Physical backup tools include the mysqlbackup of MySQL Enterprise Backup for InnoDB or any other tables, or file system-level commands (such as cp, scp, tar, rsync) for MyISAM tables.
- For restore:
  - MySQL Enterprise Backup restores InnoDB and other tables that it backed up.
  - ndb\_restore restores NDB tables.
  - Files copied at the file system level can be copied back to their original locations with file system commands.

Logical backup methods have these characteristics:

- The backup is done by querying the MySQL server to obtain database structure and content information.
- Backup is slower than physical methods because the server must access database information and convert it to logical format. If the output is written on the client side, the server must also send it to the backup program.
- Output is larger than for physical backup, particularly when saved in text format.
- Backup and restore granularity is available at the server level (all databases), database level (all tables in a particular database), or table level. This is true regardless of storage engine.
- The backup does not include log or configuration files, or other database-related files that are not part of databases.
- Backups stored in logical format are machine independent and highly portable.
- Logical backups are performed with the MySQL server running. The server is not taken offline.
- Logical backup tools include the mysqldump program and the SELECT ... INTO OUTFILE statement. These work for any storage engine, even MEMORY.
- To restore logical backups, SQL-format dump files can be processed using the mysql client. To load delimited-text files, use the LOAD DATA statement or the mysqlimport client.

# **Online Versus Offline Backups**

Online backups take place while the MySQL server is running so that the database information can be obtained from the server. Offline backups take place while the server is stopped. This distinction can also be described as "hot" versus "cold" backups; a "warm" backup is one where the server remains running but locked against modifying data while you access database files externally.

Online backup methods have these characteristics:

- The backup is less intrusive to other clients, which can connect to the MySQL server during the backup and may be able to access data depending on what operations they need to perform.
- Care must be taken to impose appropriate locking so that data modifications do not take place that would compromise backup integrity. The MySQL Enterprise Backup product does such locking automatically.

Offline backup methods have these characteristics:

• Clients can be affected adversely because the server is unavailable during backup. For that reason, such backups are often taken from a replica that can be taken offline without harming availability.

• The backup procedure is simpler because there is no possibility of interference from client activity.

A similar distinction between online and offline applies for recovery operations, and similar characteristics apply. However, it is more likely for clients to be affected by online recovery than by online backup because recovery requires stronger locking. During backup, clients might be able to read data while it is being backed up. Recovery modifies data and does not just read it, so clients must be prevented from accessing data while it is being restored.

## **Local Versus Remote Backups**

A local backup is performed on the same host where the MySQL server runs, whereas a remote backup is done from a different host. For some types of backups, the backup can be initiated from a remote host even if the output is written locally on the server. host.

- mysqldump can connect to local or remote servers. For SQL output (CREATE and INSERT statements), local or remote dumps can be done and generate output on the client. For delimited-text output (with the --tab option), data files are created on the server host.
- SELECT ... INTO OUTFILE can be initiated from a local or remote client host, but the output file is created on the server host.
- Physical backup methods typically are initiated locally on the MySQL server host so that the server can be taken offline, although the destination for copied files might be remote.

## **Snapshot Backups**

Some file system implementations enable "snapshots" to be taken. These provide logical copies of the file system at a given point in time, without requiring a physical copy of the entire file system. (For example, the implementation may use copy-on-write techniques so that only parts of the file system modified after the snapshot time need be copied.) MySQL itself does not provide the capability for taking file system snapshots. It is available through third-party solutions such as Veritas, LVM, or ZFS.

# **Full Versus Incremental Backups**

A full backup includes all data managed by a MySQL server at a given point in time. An incremental backup consists of the changes made to the data during a given time span (from one point in time to another). MySQL has different ways to perform full backups, such as those described earlier in this section. Incremental backups are made possible by enabling the server's binary log, which the server uses to record data changes.

# **Full Versus Point-in-Time (Incremental) Recovery**

A full recovery restores all data from a full backup. This restores the server instance to the state that it had when the backup was made. If that state is not sufficiently current, a full recovery can be followed by recovery of incremental backups made since the full backup, to bring the server to a more up-todate state.

Incremental recovery is recovery of changes made during a given time span. This is also called pointin-time recovery because it makes a server's state current up to a given time. Point-in-time recovery is based on the binary log and typically follows a full recovery from the backup files that restores the server to its state when the backup was made. Then the data changes written in the binary log files are applied as incremental recovery to redo data modifications and bring the server up to the desired point in time.

## **Table Maintenance**

Data integrity can be compromised if tables become corrupt. For InnoDB tables, this is not a typical issue. For programs to check MyISAM tables and repair them if problems are found, see [Section 9.6,](#page-56-0) ["MyISAM Table Maintenance and Crash Recovery"](#page-56-0).

## **Backup Scheduling, Compression, and Encryption**

Backup scheduling is valuable for automating backup procedures. Compression of backup output reduces space requirements, and encryption of the output provides better security against unauthorized access of backed-up data. MySQL itself does not provide these capabilities. The MySQL Enterprise Backup product can compress InnoDB backups, and compression or encryption of backup output can be achieved using file system utilities. Other third-party solutions may be available.

# <span id="page-42-0"></span>**9.2 Database Backup Methods**

This section summarizes some general methods for making backups.

## **Making a Hot Backup with MySQL Enterprise Backup**

Customers of MySQL Enterprise Edition can use the MySQL Enterprise Backup product to do physical backups of entire instances or selected databases, tables, or both. This product includes features for incremental and compressed backups. Backing up the physical database files makes restore much faster than logical techniques such as the mysqldump command. InnoDB tables are copied using a hot backup mechanism. (Ideally, the InnoDB tables should represent a substantial majority of the data.) Tables from other storage engines are copied using a warm backup mechanism. For an overview of the MySQL Enterprise Backup product, see Section 32.1, "MySQL Enterprise Backup Overview".

## **Making Backups with mysqldump**

The mysqldump program can make backups. It can back up all kinds of tables. (See [Section 9.4,](#page-47-1) ["Using mysqldump for Backups".](#page-47-1))

For InnoDB tables, it is possible to perform an online backup that takes no locks on tables using the - single-transaction option to mysqldump. See [Section 9.3.1, "Establishing a Backup Policy"](#page-44-1).

# **Making Backups by Copying Table Files**

MyISAM tables can be backed up by copying table files (\*.MYD, \*.MYI files, and associated \*.sdi files). To get a consistent backup, stop the server or lock and flush the relevant tables:

```
FLUSH TABLES tbl_list WITH READ LOCK;
```

You need only a read lock; this enables other clients to continue to query the tables while you are making a copy of the files in the database directory. The flush is needed to ensure that the all active index pages are written to disk before you start the backup. See Section 15.3.6, "LOCK TABLES and UNLOCK TABLES Statements", and Section 15.7.8.3, "FLUSH Statement".

You can also create a binary backup simply by copying the table files, as long as the server is not updating anything. (But note that table file copying methods do not work if your database contains InnoDB tables. Also, even if the server is not actively updating data, InnoDB may still have modified data cached in memory and not flushed to disk.)

For an example of this backup method, refer to the export and import example in Section 15.2.6, "IMPORT TABLE Statement".

# **Making Delimited-Text File Backups**

To create a text file containing a table's data, you can use SELECT \* INTO OUTFILE 'file\_name' FROM tbl\_name. The file is created on the MySQL server host, not the client host. For this statement, the output file cannot already exist because permitting files to be overwritten constitutes a security risk. See Section 15.2.13, "SELECT Statement". This method works for any kind of data file, but saves only table data, not the table structure.

Another way to create text data files (along with files containing CREATE TABLE statements for the backed up tables) is to use mysqldump with the --tab option. See [Section 9.4.3, "Dumping Data in](#page-49-1) [Delimited-Text Format with mysqldump".](#page-49-1)

To reload a delimited-text data file, use LOAD DATA or mysqlimport.

## **Making Incremental Backups by Enabling the Binary Log**

MySQL supports incremental backups using the binary log. The binary log files provide you with the information you need to replicate changes to the database that are made subsequent to the point at which you performed a backup. Therefore, to allow a server to be restored to a point-in-time, binary logging must be enabled on it, which is the default setting for MySQL 8.4 ; see Section 7.4.4, "The Binary Log".

At the moment you want to make an incremental backup (containing all changes that happened since the last full or incremental backup), you should rotate the binary log by using FLUSH LOGS. This done, you need to copy to the backup location all binary logs which range from the one of the moment of the last full or incremental backup to the last but one. These binary logs are the incremental backup; at restore time, you apply them as explained in [Section 9.5, "Point-in-Time \(Incremental\) Recovery".](#page-53-0) The next time you do a full backup, you should also rotate the binary log using FLUSH LOGS or mysqldump --flush-logs. See Section 6.5.4, "mysqldump — A Database Backup Program".

## **Making Backups Using Replicas**

If you have performance problems with a server while making backups, one strategy that can help is to set up replication and perform backups on the replica rather than on the source. See Section 19.4.1, "Using Replication for Backups".

If you are backing up a replica, you should back up its connection metadata repository and applier metadata repository (see Section 19.2.4, "Relay Log and Replication Metadata Repositories") when you back up the replica's databases, regardless of the backup method you choose. This information is always needed to resume replication after you restore the replica's data. If your replica is replicating LOAD DATA statements, you should also back up any SQL\_LOAD-\* files that exist in the directory that the replica uses for this purpose. The replica needs these files to resume replication of any interrupted LOAD DATA operations. The location of this directory is the value of the system variable replica\_load\_tmpdir. If the server was not started with that variable set, the directory location is the value of the tmpdir system variable.

# **Recovering Corrupt Tables**

If you have to restore MyISAM tables that have become corrupt, try to recover them using REPAIR TABLE or myisamchk -r first. That should work in 99.9% of all cases. If myisamchk fails, see [Section 9.6, "MyISAM Table Maintenance and Crash Recovery".](#page-56-0)

# **Making Backups Using a File System Snapshot**

If you are using a Veritas file system, you can make a backup like this:

- 1. From a client program, execute FLUSH TABLES WITH READ LOCK.
- 2. From another shell, execute mount vxfs snapshot.
- 3. From the first client, execute UNLOCK TABLES.
- 4. Copy files from the snapshot.
- 5. Unmount the snapshot.

Similar snapshot capabilities may be available in other file systems, such as LVM or ZFS.

# <span id="page-44-0"></span>**9.3 Example Backup and Recovery Strategy**

This section discusses a procedure for performing backups that enables you to recover data after several types of crashes:

- Operating system crash
- Power failure
- File system crash
- Hardware problem (hard drive, motherboard, and so forth)

The example commands do not include options such as --user and --password for the mysqldump and mysql client programs. You should include such options as necessary to enable client programs to connect to the MySQL server.

Assume that data is stored in the InnoDB storage engine, which has support for transactions and automatic crash recovery. Assume also that the MySQL server is under load at the time of the crash. If it were not, no recovery would ever be needed.

For cases of operating system crashes or power failures, we can assume that MySQL's disk data is available after a restart. The InnoDB data files might not contain consistent data due to the crash, but InnoDB reads its logs and finds in them the list of pending committed and noncommitted transactions that have not been flushed to the data files. InnoDB automatically rolls back those transactions that were not committed, and flushes to its data files those that were committed. Information about this recovery process is conveyed to the user through the MySQL error log. The following is an example log excerpt:

```
InnoDB: Database was not shut down normally.
InnoDB: Starting recovery from log files...
InnoDB: Starting log scan based on checkpoint at
InnoDB: log sequence number 0 13674004
InnoDB: Doing recovery: scanned up to log sequence number 0 13739520
InnoDB: Doing recovery: scanned up to log sequence number 0 13805056
InnoDB: Doing recovery: scanned up to log sequence number 0 13870592
InnoDB: Doing recovery: scanned up to log sequence number 0 13936128
...
InnoDB: Doing recovery: scanned up to log sequence number 0 20555264
InnoDB: Doing recovery: scanned up to log sequence number 0 20620800
InnoDB: Doing recovery: scanned up to log sequence number 0 20664692
InnoDB: 1 uncommitted transaction(s) which must be rolled back
InnoDB: Starting rollback of uncommitted transactions
InnoDB: Rolling back trx no 16745
InnoDB: Rolling back of trx no 16745 completed
InnoDB: Rollback of uncommitted transactions completed
InnoDB: Starting an apply batch of log records to the database...
InnoDB: Apply batch completed
InnoDB: Started
mysqld: ready for connections
```

For the cases of file system crashes or hardware problems, we can assume that the MySQL disk data is not available after a restart. This means that MySQL fails to start successfully because some blocks of disk data are no longer readable. In this case, it is necessary to reformat the disk, install a new one, or otherwise correct the underlying problem. Then it is necessary to recover our MySQL data from backups, which means that backups must already have been made. To make sure that is the case, design and implement a backup policy.

# <span id="page-44-1"></span>**9.3.1 Establishing a Backup Policy**

To be useful, backups must be scheduled regularly. A full backup (a snapshot of the data at a point in time) can be done in MySQL with several tools. For example, MySQL Enterprise Backup can perform a physical backup of an entire instance, with optimizations to minimize overhead and avoid disruption

when backing up InnoDB data files; mysqldump provides online logical backup. This discussion uses mysqldump.

Assume that we make a full backup of all our InnoDB tables in all databases using the following command on Sunday at 1 p.m., when load is low:

```
$> mysqldump --all-databases --source-data --single-transaction > backup_sunday_1_PM.sql
```

The resulting .sql file produced by mysqldump contains a set of SQL INSERT statements that can be used to reload the dumped tables at a later time.

This backup operation acquires a global read lock on all tables at the beginning of the dump (using FLUSH TABLES WITH READ LOCK). As soon as this lock has been acquired, the binary log coordinates are read and the lock is released. If long updating statements are running when the FLUSH statement is issued, the backup operation may stall until those statements finish. After that, the dump becomes lock-free and does not disturb reads and writes on the tables.

It was assumed earlier that the tables to back up are InnoDB tables, so --single-transaction uses a consistent read and guarantees that data seen by mysqldump does not change. (Changes made by other clients to InnoDB tables are not seen by the mysqldump process.) If the backup operation includes nontransactional tables, consistency requires that they do not change during the backup. For example, for the MyISAM tables in the mysql database, there must be no administrative changes to MySQL accounts during the backup.

Full backups are necessary, but it is not always convenient to create them. They produce large backup files and take time to generate. They are not optimal in the sense that each successive full backup includes all data, even that part that has not changed since the previous full backup. It is more efficient to make an initial full backup, and then to make incremental backups. The incremental backups are smaller and take less time to produce. The tradeoff is that, at recovery time, you cannot restore your data just by reloading the full backup. You must also process the incremental backups to recover the incremental changes.

To make incremental backups, we need to save the incremental changes. In MySQL, these changes are represented in the binary log, so the MySQL server should always be started with the --log-bin option to enable that log. With binary logging enabled, the server writes each data change into a file while it updates data. Looking at the data directory of a MySQL server that has been running for some days, we find these MySQL binary log files:

```
-rw-rw---- 1 guilhem guilhem 1277324 Nov 10 23:59 gbichot2-bin.000001
-rw-rw---- 1 guilhem guilhem 4 Nov 10 23:59 gbichot2-bin.000002
-rw-rw---- 1 guilhem guilhem 79 Nov 11 11:06 gbichot2-bin.000003
-rw-rw---- 1 guilhem guilhem 508 Nov 11 11:08 gbichot2-bin.000004
-rw-rw---- 1 guilhem guilhem 220047446 Nov 12 16:47 gbichot2-bin.000005
-rw-rw---- 1 guilhem guilhem 998412 Nov 14 10:08 gbichot2-bin.000006
-rw-rw---- 1 guilhem guilhem 361 Nov 14 10:07 gbichot2-bin.index
```

Each time it restarts, the MySQL server creates a new binary log file using the next number in the sequence. While the server is running, you can also tell it to close the current binary log file and begin a new one manually by issuing a FLUSH LOGS SQL statement or with a mysqladmin flush-logs command. mysqldump also has an option to flush the logs. The .index file in the data directory contains the list of all MySQL binary logs in the directory.

The MySQL binary logs are important for recovery because they form the set of incremental backups. If you make sure to flush the logs when you make your full backup, the binary log files created afterward contain all the data changes made since the backup. Let's modify the previous mysqldump command a bit so that it flushes the MySQL binary logs at the moment of the full backup, and so that the dump file contains the name of the new current binary log:

```
$> mysqldump --single-transaction --flush-logs --source-data=2 \
 --all-databases > backup_sunday_1_PM.sql
```

After executing this command, the data directory contains a new binary log file, gbichot2 bin.000007, because the --flush-logs option causes the server to flush its logs. The --sourcedata option causes mysqldump to write binary log information to its output, so the resulting .sql dump file includes these lines:

```
-- Position to start replication or point-in-time recovery from
-- CHANGE REPLICATION SOURCE TO SOURCE_LOG_FILE='gbichot2-bin.000007',SOURCE_LOG_POS=4;
```

Because the mysqldump command made a full backup, those lines mean two things:

- The dump file contains all changes made before any changes written to the gbichot2 bin.000007 binary log file or higher.
- All data changes logged after the backup are not present in the dump file, but are present in the gbichot2-bin.000007 binary log file or higher.

On Monday at 1 p.m., we can create an incremental backup by flushing the logs to begin a new binary log file. For example, executing a mysqladmin flush-logs command creates gbichot2 bin.000008. All changes between the Sunday 1 p.m. full backup and Monday 1 p.m. are written in gbichot2-bin.000007. This incremental backup is important, so it is a good idea to copy it to a safe place. (For example, back it up on tape or DVD, or copy it to another machine.) On Tuesday at 1 p.m., execute another mysqladmin flush-logs command. All changes between Monday 1 p.m. and Tuesday 1 p.m. are written in gbichot2-bin.000008 (which also should be copied somewhere safe).

The MySQL binary logs take up disk space. To free up space, purge them from time to time. One way to do this is by deleting the binary logs that are no longer needed, such as when we make a full backup:

```
$> mysqldump --single-transaction --flush-logs --source-data=2 \
 --all-databases --delete-source-logs > backup_sunday_1_PM.sql
```

![](_page_46_Picture_9.jpeg)

### **Note**

Deleting the MySQL binary logs with mysqldump --delete-sourcelogs can be dangerous if your server is a replication source server, because replicas might not yet fully have processed the contents of the binary log. The description for the PURGE BINARY LOGS statement explains what should be verified before deleting the MySQL binary logs. See Section 15.4.1.1, "PURGE BINARY LOGS Statement".

# <span id="page-46-0"></span>**9.3.2 Using Backups for Recovery**

Now, suppose that we have a catastrophic unexpected exit on Wednesday at 8 a.m. that requires recovery from backups. To recover, first we restore the last full backup we have (the one from Sunday 1 p.m.). The full backup file is just a set of SQL statements, so restoring it is very easy:

```
$> mysql < backup_sunday_1_PM.sql
```

At this point, the data is restored to its state as of Sunday 1 p.m.. To restore the changes made since then, we must use the incremental backups; that is, the gbichot2-bin.000007 and gbichot2 bin.000008 binary log files. Fetch the files if necessary from where they were backed up, and then process their contents like this:

```
$> mysqlbinlog gbichot2-bin.000007 gbichot2-bin.000008 | mysql
```

We now have recovered the data to its state as of Tuesday 1 p.m., but still are missing the changes from that date to the date of the crash. To not lose them, we would have needed to have the MySQL server store its MySQL binary logs into a safe location (RAID disks, SAN, ...) different from the place where it stores its data files, so that these logs were not on the destroyed disk. (That is, we can start the server with a --log-bin option that specifies a location on a different physical device from the one on which the data directory resides. That way, the logs are safe even if the device containing the directory is lost.) If we had done this, we would have the gbichot2-bin.000009 file (and any

subsequent files) at hand, and we could apply them using mysqlbinlog and mysql to restore the most recent data changes with no loss up to the moment of the crash:

```
$> mysqlbinlog gbichot2-bin.000009 ... | mysql
```

For more information about using mysqlbinlog to process binary log files, see [Section 9.5, "Point-in-](#page-53-0)[Time \(Incremental\) Recovery"](#page-53-0).

## <span id="page-47-0"></span>**9.3.3 Backup Strategy Summary**

In case of an operating system crash or power failure, InnoDB itself does all the job of recovering data. But to make sure that you can sleep well, observe the following guidelines:

- Always tun the MySQL server with binary logging enabled (that is the default setting for MySQL 8.4). If you have such safe media, this technique can also be good for disk load balancing (which results in a performance improvement).
- Make periodic full backups, using the mysqldump command shown earlier in [Section 9.3.1,](#page-44-1) ["Establishing a Backup Policy"](#page-44-1), that makes an online, nonblocking backup.
- Make periodic incremental backups by flushing the logs with FLUSH LOGS or mysqladmin flushlogs.

# <span id="page-47-1"></span>**9.4 Using mysqldump for Backups**

![](_page_47_Picture_10.jpeg)

#### **Tip**

Consider using the [MySQL Shell dump utilities,](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.md) which provide parallel dumping with multiple threads, file compression, and progress information display, as well as cloud features such as Oracle Cloud Infrastructure Object Storage streaming, and MySQL HeatWave compatibility checks and modifications. Dumps can be easily imported into a MySQL Server instance or a MySQL HeatWave DB System using the [MySQL Shell load dump utilities.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-load-dump.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md)

This section describes how to use mysqldump to produce dump files, and how to reload dump files. A dump file can be used in several ways:

- As a backup to enable data recovery in case of data loss.
- As a source of data for setting up replicas.
- As a source of data for experimentation:
  - To make a copy of a database that you can use without changing the original data.
  - To test potential upgrade incompatibilities.

mysqldump produces two types of output, depending on whether the --tab option is given:

- Without --tab, mysqldump writes SQL statements to the standard output. This output consists of CREATE statements to create dumped objects (databases, tables, stored routines, and so forth), and INSERT statements to load data into tables. The output can be saved in a file and reloaded later using mysql to recreate the dumped objects. Options are available to modify the format of the SQL statements, and to control which objects are dumped.
- With --tab, mysqldump produces two output files for each dumped table. The server writes one file as tab-delimited text, one line per table row. This file is named tbl\_name.txt in the output directory. The server also sends a CREATE TABLE statement for the table to mysqldump, which writes it as a file named tbl\_name.sql in the output directory.

## <span id="page-48-0"></span>**9.4.1 Dumping Data in SQL Format with mysqldump**

This section describes how to use mysqldump to create SQL-format dump files. For information about reloading such dump files, see [Section 9.4.2, "Reloading SQL-Format Backups"](#page-49-0).

By default, mysqldump writes information as SQL statements to the standard output. You can save the output in a file:

```
$> mysqldump [arguments] > file_name
```

To dump all databases, invoke mysqldump with the --all-databases option:

```
$> mysqldump --all-databases > dump.sql
```

To dump only specific databases, name them on the command line and use the --databases option:

```
$> mysqldump --databases db1 db2 db3 > dump.sql
```

The --databases option causes all names on the command line to be treated as database names. Without this option, mysqldump treats the first name as a database name and those following as table names.

With --all-databases or --databases, mysqldump writes CREATE DATABASE and USE statements prior to the dump output for each database. This ensures that when the dump file is reloaded, it creates each database if it does not exist and makes it the default database so database contents are loaded into the same database from which they came. If you want to cause the dump file to force a drop of each database before recreating it, use the --add-drop-database option as well. In this case, mysqldump writes a DROP DATABASE statement preceding each CREATE DATABASE statement.

To dump a single database, name it on the command line:

```
$> mysqldump --databases test > dump.sql
```

In the single-database case, it is permissible to omit the --databases option:

```
$> mysqldump test > dump.sql
```

The difference between the two preceding commands is that without --databases, the dump output contains no CREATE DATABASE or USE statements. This has several implications:

- When you reload the dump file, you must specify a default database name so that the server knows which database to reload.
- For reloading, you can specify a database name different from the original name, which enables you to reload the data into a different database.
- If the database to be reloaded does not exist, you must create it first.
- Because the output contains no CREATE DATABASE statement, the --add-drop-database option has no effect. If you use it, it produces no DROP DATABASE statement.

To dump only specific tables from a database, name them on the command line following the database name:

```
$> mysqldump test t1 t3 t7 > dump.sql
```

By default, if GTIDs are in use on the server where you create the dump file (gtid\_mode=ON), mysqldump includes a SET @@GLOBAL.gtid\_purged statement in the output to add the GTIDs from the gtid\_executed set on the source server to the gtid\_purged set on the target server. If you are dumping only specific databases or tables, it is important to note that the value that is included by mysqldump includes the GTIDs of all transactions in the gtid\_executed set on the source server, even those that changed suppressed parts of the database, or other databases on the server that

were not included in the partial dump. If you only replay one partial dump file on the target server, the extra GTIDs do not cause any problems with the future operation of that server. However, if you replay a second dump file on the target server that contains the same GTIDs (for example, another partial dump from the same source server), any SET @@GLOBAL.gtid\_purged statement in the second dump file fails. To avoid this issue, either set the mysqldump option --set-gtid-purged to OFF or COMMENTED to output the second dump file without an active SET @@GLOBAL.gtid\_purged statement, or remove the statement manually before replaying the dump file.

## <span id="page-49-0"></span>**9.4.2 Reloading SQL-Format Backups**

To reload a dump file written by mysqldump that consists of SQL statements, use it as input to the mysql client. If the dump file was created by mysqldump with the --all-databases or - databases option, it contains CREATE DATABASE and USE statements and it is not necessary to specify a default database into which to load the data:

```
$> mysql < dump.sql
```

Alternatively, from within mysql, use a source command:

```
mysql> source dump.sql
```

If the file is a single-database dump not containing CREATE DATABASE and USE statements, create the database first (if necessary):

```
$> mysqladmin create db1
```

Then specify the database name when you load the dump file:

```
$> mysql db1 < dump.sql
```

Alternatively, from within mysql, create the database, select it as the default database, and load the dump file:

```
mysql> CREATE DATABASE IF NOT EXISTS db1;
mysql> USE db1;
mysql> source dump.sql
```

![](_page_49_Picture_13.jpeg)

#### **Note**

For Windows PowerShell users: Because the "<" character is reserved for future use in PowerShell, an alternative approach is required, such as using quotes cmd.exe /c "mysql < dump.sql".

# <span id="page-49-1"></span>**9.4.3 Dumping Data in Delimited-Text Format with mysqldump**

This section describes how to use mysqldump to create delimited-text dump files. For information about reloading such dump files, see [Section 9.4.4, "Reloading Delimited-Text Format Backups"](#page-50-0).

If you invoke mysqldump with the --tab=dir\_name option, it uses dir\_name as the output directory and dumps tables individually in that directory using two files for each table. The table name is the base name for these files. For a table named t1, the files are named t1.sql and t1.txt. The .sql file contains a CREATE TABLE statement for the table. The .txt file contains the table data, one line per table row.

The following command dumps the contents of the db1 database to files in the /tmp database:

```
$> mysqldump --tab=/tmp db1
```

The .txt files containing table data are written by the server, so they are owned by the system account used for running the server. The server uses SELECT ... INTO OUTFILE to write the files, so you must have the FILE privilege to perform this operation, and an error occurs if a given .txt file already exists.

The server sends the CREATE definitions for dumped tables to mysqldump, which writes them to .sql files. These files therefore are owned by the user who executes mysqldump.

It is best that --tab be used only for dumping a local server. If you use it with a remote server, the --tab directory must exist on both the local and remote hosts, and the .txt files are written by the server in the remote directory (on the server host), whereas the .sql files are written by mysqldump in the local directory (on the client host).

For mysqldump --tab, the server by default writes table data to .txt files one line per row with tabs between column values, no quotation marks around column values, and newline as the line terminator. (These are the same defaults as for SELECT ... INTO OUTFILE.)

To enable data files to be written using a different format, mysqldump supports these options:

• --fields-terminated-by=str

The string for separating column values (default: tab).

• --fields-enclosed-by=char

The character within which to enclose column values (default: no character).

• --fields-optionally-enclosed-by=char

The character within which to enclose non-numeric column values (default: no character).

• --fields-escaped-by=char

The character for escaping special characters (default: no escaping).

• --lines-terminated-by=str

The line-termination string (default: newline).

Depending on the value you specify for any of these options, it might be necessary on the command line to quote or escape the value appropriately for your command interpreter. Alternatively, specify the value using hex notation. Suppose that you want mysqldump to quote column values within double quotation marks. To do so, specify double quote as the value for the --fields-enclosed-by option. But this character is often special to command interpreters and must be treated specially. For example, on Unix, you can quote the double quote like this:

```
--fields-enclosed-by='"'
```

On any platform, you can specify the value in hex:

```
--fields-enclosed-by=0x22
```

It is common to use several of the data-formatting options together. For example, to dump tables in comma-separated values format with lines terminated by carriage-return/newline pairs (\r\n), use this command (enter it on a single line):

```
$> mysqldump --tab=/tmp --fields-terminated-by=,
 --fields-enclosed-by='"' --lines-terminated-by=0x0d0a db1
```

Should you use any of the data-formatting options to dump table data, you need to specify the same format when you reload data files later, to ensure proper interpretation of the file contents.

# <span id="page-50-0"></span>**9.4.4 Reloading Delimited-Text Format Backups**

For backups produced with mysqldump --tab, each table is represented in the output directory by an .sql file containing the CREATE TABLE statement for the table, and a .txt file containing the table data. To reload a table, first change location into the output directory. Then process the .sql file with mysql to create an empty table and process the .txt file to load the data into the table:

```
$> mysql db1 < t1.sql
$> mysqlimport db1 t1.txt
```

An alternative to using mysqlimport to load the data file is to use the LOAD DATA statement from within the mysql client:

```
mysql> USE db1;
mysql> LOAD DATA INFILE 't1.txt' INTO TABLE t1;
```

If you used any data-formatting options with mysqldump when you initially dumped the table, you must use the same options with mysqlimport or LOAD DATA to ensure proper interpretation of the data file contents:

```
$> mysqlimport --fields-terminated-by=,
 --fields-enclosed-by='"' --lines-terminated-by=0x0d0a db1 t1.txt
```

Or:

```
mysql> USE db1;
mysql> LOAD DATA INFILE 't1.txt' INTO TABLE t1
 FIELDS TERMINATED BY ',' FIELDS ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n';
```

## <span id="page-51-0"></span>**9.4.5 mysqldump Tips**

This section surveys techniques that enable you to use mysqldump to solve specific problems:

- How to make a copy a database
- How to copy a database from one server to another
- How to dump stored programs (stored procedures and functions, triggers, and events)
- How to dump definitions and data separately