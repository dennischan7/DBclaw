---
source: MySQL 8.0 Reference
title: 00_Overview
---

MySQL supports FIPS mode when a supported OpenSSL library and FIPS Object Module are available on the host system.

FIPS mode on the server side applies to cryptographic operations performed by the server. This includes replication (source/replica and Group Replication) and X Plugin, which run within the server. FIPS mode also applies to attempts by clients to connect to the server.

The following sections describe FIPS mode and how to take advantage of it within MySQL:

• [FIPS Overview](#page-194-0)

- [System Requirements for FIPS Mode in MySQL](#page-194-1)
- [Enabling FIPS Mode in MySQL](#page-195-0)

## <span id="page-194-0"></span>**FIPS Overview**

Federal Information Processing Standards 140-2 (FIPS 140-2) describes a security standard that can be required by Federal (US Government) agencies for cryptographic modules used to protect sensitive or valuable information. To be considered acceptable for such Federal use, a cryptographic module must be certified for FIPS 140-2. If a system intended to protect sensitive data lacks the proper FIPS 140-2 certificate, Federal agencies cannot purchase it.

Products such as OpenSSL can be used in FIPS mode, although the OpenSSL library itself is not validated for FIPS. Instead, the OpenSSL library is used with the OpenSSL FIPS Object Module to enable OpenSSL-based applications to operate in FIPS mode.

For general information about FIPS and its implementation in OpenSSL, these references may be helpful:

- [National Institute of Standards and Technology FIPS PUB 140-2](https://doi.org/10.6028/NIST.FIPS.140-2)
- [OpenSSL FIPS 140-2 Security Policy](https://csrc.nist.gov/csrc/media/projects/cryptographic-module-validation-program/documents/security-policies/140sp1747.pdf)
- [fips\\_module manual page](https://www.openssl.org/docs/man3.0/man7/fips_module.md)

![](_page_194_Picture_10.jpeg)

#### **Important**

FIPS mode imposes conditions on cryptographic operations such as restrictions on acceptable encryption algorithms or requirements for longer key lengths. For OpenSSL, the exact FIPS behavior depends on the OpenSSL version.

# <span id="page-194-1"></span>**System Requirements for FIPS Mode in MySQL**

For MySQL to support FIPS mode, these system requirements must be satisfied:

- 1. MySQL must be compiled with an OpenSSL version that is certified for use with FIPS. OpenSSL 1.0.2 and OpenSSL 3.0 are certified, but OpenSSL 1.1.1 is not. Binary distributions for recent versions of MySQL are compiled using OpenSSL 3.0 on some platforms, which means they are not certified for FIPS. This means you have the following options, depending on system and MySQL configuration:
  - Use a system that has OpenSSL 3.0 and the required FIPS object module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL 3.0, or compile MySQL from source using OpenSSL 3.0.

For general information about upgrading to OpenSSL 3.0, see [OpenSSL 3.0 Migration Guide](https://www.openssl.org/docs/man3.0/man7/migration_guide.md).

- Use a system that has OpenSSL 1.1.1 or higher. In this case, you can install MySQL using binary packages, and you can use the TLS v1.3 protocol and ciphersuites, in addition to other already supported TLS protocols. However, you cannot enable FIPS mode for MySQL.
- Use a system that has OpenSSL 1.0.2 and the required FIPS Object Module. In this case, you can enable FIPS mode for MySQL if you use a binary distribution compiled using OpenSSL 1.0.2, or compile MySQL from source using OpenSSL 1.0.2. In this case, you cannot use the TLS v1.3 protocol or ciphersuites, which require OpenSSL 1.1.1 or 3.0. In addition, you should be aware that OpenSSL 1.0.2 reached end of life status in 2019, and that all operating platforms embedding OpenSSL 1.1.1 reach their end of life in 2024.
- 2. At runtime, the OpenSSL library and OpenSSL FIPS Object Module must be available as shared (dynamically linked) objects.

## <span id="page-195-0"></span>**Enabling FIPS Mode in MySQL**

![](_page_195_Picture_2.jpeg)

#### **Note**

In MySQL 8.0.34 and later, the server-side and client-side configuration described at the end of this section is no longer required.

To determine whether MySQL is running on a system with FIPS mode enabled, check the value of the ssl\_fips\_mode server system variable using an SQL statement such as SHOW VARIABLES LIKE '%fips%' or SELECT @@ssl\_fips\_mode. If the value of this variable is 1 (ON) or 2 (STRICT), FIPS mode is enabled for OpenSSL; if it is 0 (OFF), FIPS mode is not available.

![](_page_195_Picture_6.jpeg)

## **Important**

In general, STRICT imposes more restrictions than ON, but MySQL itself has no FIPS-specific code other than to specify the FIPS mode value to OpenSSL. The exact behavior of FIPS mode for ON or STRICT depends on the OpenSSL version. For details, refer to the fips\_module manpage (see [FIPS Overview\)](#page-194-0).

FIPS mode on the server side applies to cryptographic operations performed by the server, including those performed by MySQL Replication (including Group Replication) and X Plugin, which run within the server.

FIPS mode also applies to attempts by clients to connect to the server. When enabled, on either the client or server side, it restricts which of the supported encryption ciphers can be chosen. However, enabling FIPS mode does not require that an encrypted connection must be used, or that user credentials must be encrypted. For example, if FIPS mode is enabled, stronger cryptographic algorithms are required. In particular, MD5 is restricted, so trying to establish an encrypted connection using an encryption cipher such as RC4-MD5 does not work. But there is nothing about FIPS mode that prevents establishing an unencrypted connection. (To do that, you can use the REQUIRE clause for CREATE USER or ALTER USER for specific user accounts, or set the require\_secure\_transport system variable to affect all accounts.)

If FIPS mode is required, it is recommended to use an operating platform that includes it; if it does, you can (and should) use it. If your platform does not include FIPS, you have two options:

- Migrate to a platform which has FIPS OpenSSL support.
- Build the OpenSSL library and FIPS object module from source, using the instructions from the fips\_module manpage (see [FIPS Overview\)](#page-194-0).

**MySQL 8.0.34 and earlier**: Control of FIPS mode on the server side and the client side was accomplished using the system variables listed here:

- The ssl\_fips\_mode system variable controls whether the server operates in FIPS mode.
- The --ssl-fips-mode client option controls whether a given MySQL client operates in FIPS mode.

The ssl\_fips\_mode system variable and --ssl-fips-mode client option permit these values:

- OFF: Disable FIPS mode.
- ON: Enable FIPS mode.
- STRICT: Enable "strict" FIPS mode.

![](_page_195_Picture_21.jpeg)

## **Note**

If the OpenSSL FIPS Object Module is not available, the only permitted value for ssl\_fips\_mode and --ssl-fips-mode is OFF. An error occurs for attempts to set the FIPS mode to a different value.

# Chapter 9 Backup and Recovery

# **Table of Contents**

| 9.1 Backup and Recovery Types 1768                              |      |
|-----------------------------------------------------------------|------|
| 9.2 Database Backup Methods 1771                                |      |
| 9.3 Example Backup and Recovery Strategy 1773                   |      |
| 9.3.1 Establishing a Backup Policy                              | 1773 |
| 9.3.2 Using Backups for Recovery 1775                           |      |
| 9.3.3 Backup Strategy Summary 1776                              |      |
| 9.4 Using mysqldump for Backups 1776                            |      |
| 9.4.1 Dumping Data in SQL Format with mysqldump 1777            |      |
| 9.4.2 Reloading SQL-Format Backups 1778                         |      |
| 9.4.3 Dumping Data in Delimited-Text Format with mysqldump 1778 |      |
| 9.4.4 Reloading Delimited-Text Format Backups 1779              |      |
| 9.4.5 mysqldump Tips 1780                                       |      |
| 9.5 Point-in-Time (Incremental) Recovery 1782                   |      |
| 9.5.1 Point-in-Time Recovery Using Binary Log 1782              |      |
| 9.5.2 Point-in-Time Recovery Using Event Positions 1783         |      |
| 9.6 MyISAM Table Maintenance and Crash Recovery 1785            |      |
| 9.6.1 Using myisamchk for Crash Recovery 1785                   |      |
| 9.6.2 How to Check MyISAM Tables for Errors 1786                |      |
| 9.6.3 How to Repair MyISAM Tables 1787                          |      |
| 9.6.4 MyISAM Table Optimization 1789                            |      |
| 9.6.5 Setting Up a MyISAM Table Maintenance Schedule 1789       |      |
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
- NDB Cluster provides a high-availability, high-redundancy version of MySQL adapted for the distributed computing environment. See Chapter 25, MySQL NDB Cluster 8.0, which provides information about MySQL NDB Cluster 8.0.

# <span id="page-197-0"></span>**9.1 Backup and Recovery Types**

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

## **Online Versus Offline Backups**

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

Data integrity can be compromised if tables become corrupt. For InnoDB tables, this is not a typical issue. For programs to check MyISAM tables and repair them if problems are found, see Section 9.6, "MyISAM Table Maintenance and Crash Recovery".

# **Backup Scheduling, Compression, and Encryption**

Backup scheduling is valuable for automating backup procedures. Compression of backup output reduces space requirements, and encryption of the output provides better security against unauthorized access of backed-up data. MySQL itself does not provide these capabilities. The MySQL Enterprise Backup product can compress InnoDB backups, and compression or encryption of backup output can be achieved using file system utilities. Other third-party solutions may be available.

# <span id="page-0-0"></span>**9.2 Database Backup Methods**

This section summarizes some general methods for making backups.

## **Making a Hot Backup with MySQL Enterprise Backup**

Customers of MySQL Enterprise Edition can use the MySQL Enterprise Backup product to do physical backups of entire instances or selected databases, tables, or both. This product includes features for incremental and compressed backups. Backing up the physical database files makes restore much faster than logical techniques such as the mysqldump command. InnoDB tables are copied using a hot backup mechanism. (Ideally, the InnoDB tables should represent a substantial majority of the data.) Tables from other storage engines are copied using a warm backup mechanism. For an overview of the MySQL Enterprise Backup product, see Section 32.1, "MySQL Enterprise Backup Overview".

# **Making Backups with mysqldump**

The mysqldump program can make backups. It can back up all kinds of tables. (See [Section 9.4,](#page-5-0) ["Using mysqldump for Backups".](#page-5-0))

For InnoDB tables, it is possible to perform an online backup that takes no locks on tables using the - single-transaction option to mysqldump. See [Section 9.3.1, "Establishing a Backup Policy"](#page-2-0).

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

Another way to create text data files (along with files containing CREATE TABLE statements for the backed up tables) is to use mysqldump with the --tab option. See [Section 9.4.3, "Dumping Data in](#page-7-0) [Delimited-Text Format with mysqldump".](#page-7-0)

To reload a delimited-text data file, use LOAD DATA or mysqlimport.

## **Making Incremental Backups by Enabling the Binary Log**

MySQL supports incremental backups using the binary log. The binary log files provide you with the information you need to replicate changes to the database that are made subsequent to the point at which you performed a backup. Therefore, to allow a server to be restored to a point-in-time, binary logging must be enabled on it, which is the default setting for MySQL 8.0 ; see Section 7.4.4, "The Binary Log".

At the moment you want to make an incremental backup (containing all changes that happened since the last full or incremental backup), you should rotate the binary log by using FLUSH LOGS. This done, you need to copy to the backup location all binary logs which range from the one of the moment of the last full or incremental backup to the last but one. These binary logs are the incremental backup; at restore time, you apply them as explained in [Section 9.5, "Point-in-Time \(Incremental\) Recovery".](#page-11-0) The next time you do a full backup, you should also rotate the binary log using FLUSH LOGS or mysqldump --flush-logs. See Section 6.5.4, "mysqldump — A Database Backup Program".

# **Making Backups Using Replicas**

If you have performance problems with a server while making backups, one strategy that can help is to set up replication and perform backups on the replica rather than on the source. See Section 19.4.1, "Using Replication for Backups".

If you are backing up a replica, you should back up its connection metadata repository and applier metadata repository (see Section 19.2.4, "Relay Log and Replication Metadata Repositories") when you back up the replica's databases, regardless of the backup method you choose. This information is always needed to resume replication after you restore the replica's data. If your replica is replicating LOAD DATA statements, you should also back up any SQL\_LOAD-\* files that exist in the directory that the replica uses for this purpose. The replica needs these files to resume replication of any interrupted LOAD DATA operations. The location of this directory is the value of the system variable replica\_load\_tmpdir (from MySQL 8.0.26) or slave\_load\_tmpdir (before MySQL 8.0.26). If the server was not started with that variable set, the directory location is the value of the tmpdir system variable.

# **Recovering Corrupt Tables**

If you have to restore MyISAM tables that have become corrupt, try to recover them using REPAIR TABLE or myisamchk -r first. That should work in 99.9% of all cases. If myisamchk fails, see [Section 9.6, "MyISAM Table Maintenance and Crash Recovery".](#page-14-0)

# **Making Backups Using a File System Snapshot**

If you are using a Veritas file system, you can make a backup like this:

- 1. From a client program, execute FLUSH TABLES WITH READ LOCK.
- 2. From another shell, execute mount vxfs snapshot.
- 3. From the first client, execute UNLOCK TABLES.
- 4. Copy files from the snapshot.
- 5. Unmount the snapshot.

Similar snapshot capabilities may be available in other file systems, such as LVM or ZFS.