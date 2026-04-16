---
source: MySQL 8.0 Reference
title: 00_Overview
---

A MySQL pluggable storage engine is the component in the MySQL database server that is responsible for performing the actual data I/O operations for a database as well as enabling and enforcing certain feature sets that target a specific application need. A major benefit of using specific storage engines is that you are only delivered the features needed for a particular application, and therefore you have less system overhead in the database, with the end result being more efficient and higher database performance. This is one of the reasons that MySQL has always been known to have such high performance, matching or beating proprietary monolithic databases in industry standard benchmarks.

From a technical perspective, what are some of the unique supporting infrastructure components that are in a storage engine? Some of the key feature differentiations include:

- Concurrency: Some applications have more granular lock requirements (such as row-level locks) than others. Choosing the right locking strategy can reduce overhead and therefore improve overall performance. This area also includes support for capabilities such as multi-version concurrency control or "snapshot" read.
- Transaction Support: Not every application needs transactions, but for those that do, there are very well defined requirements such as ACID compliance and more.
- Referential Integrity: The need to have the server enforce relational database referential integrity through DDL defined foreign keys.
- Physical Storage: This involves everything from the overall page size for tables and indexes as well as the format used for storing data to physical disk.
- Index Support: Different application scenarios tend to benefit from different index strategies. Each storage engine generally has its own indexing methods, although some (such as B-tree indexes) are common to nearly all engines.
- Memory Caches: Different applications respond better to some memory caching strategies than others, so although some memory caches are common to all storage engines (such as those used for user connections), others are uniquely defined only when a particular storage engine is put in play.
- Performance Aids: This includes multiple I/O threads for parallel operations, thread concurrency, database checkpointing, bulk insert handling, and more.
- Miscellaneous Target Features: This may include support for geospatial operations, security restrictions for certain data manipulation operations, and other similar features.

Each set of the pluggable storage engine infrastructure components are designed to offer a selective set of benefits for a particular application. Conversely, avoiding a set of component features helps reduce unnecessary overhead. It stands to reason that understanding a particular application's set of requirements and selecting the proper MySQL storage engine can have a dramatic impact on overall system efficiency and performance.

# Chapter 19 Replication

# **Table of Contents**

| 19.1 Configuring Replication 3579                                                |      |
|----------------------------------------------------------------------------------|------|
| 19.1.1 Binary Log File Position Based Replication Configuration Overview 3579    |      |
| 19.1.2 Setting Up Binary Log File Position Based Replication 3580                |      |
| 19.1.3 Replication with Global Transaction Identifiers 3591                      |      |
| 19.1.4 Changing GTID Mode on Online Servers 3615                                 |      |
| 19.1.5 MySQL Multi-Source Replication 3621                                       |      |
| 19.1.6 Replication and Binary Logging Options and Variables                      | 3628 |
| 19.1.7 Common Replication Administration Tasks 3743                              |      |
| 19.2 Replication Implementation 3750                                             |      |
| 19.2.1 Replication Formats 3750                                                  |      |
| 19.2.2 Replication Channels 3758                                                 |      |
| 19.2.3 Replication Threads 3762                                                  |      |
| 19.2.4 Relay Log and Replication Metadata Repositories 3764                      |      |
| 19.2.5 How Servers Evaluate Replication Filtering Rules 3771                     |      |
| 19.3 Replication Security 3780                                                   |      |
| 19.3.1 Setting Up Replication to Use Encrypted Connections 3780                  |      |
| 19.3.2 Encrypting Binary Log Files and Relay Log Files 3783                      |      |
| 19.3.3 Replication Privilege Checks 3786                                         |      |
| 19.4 Replication Solutions 3793                                                  |      |
| 19.4.1 Using Replication for Backups 3793                                        |      |
| 19.4.2 Handling an Unexpected Halt of a Replica 3797                             |      |
| 19.4.3 Monitoring Row-based Replication 3799                                     |      |
| 19.4.4 Using Replication with Different Source and Replica Storage Engines 3800  |      |
| 19.4.5 Using Replication for Scale-Out 3801                                      |      |
| 19.4.6 Replicating Different Databases to Different Replicas 3803                |      |
| 19.4.7 Improving Replication Performance 3804                                    |      |
| 19.4.8 Switching Sources During Failover 3805                                    |      |
| 19.4.9 Switching Sources and Replicas with Asynchronous Connection Failover 3807 |      |
| 19.4.10 Semisynchronous Replication 3811                                         |      |
| 19.4.11 Delayed Replication 3817                                                 |      |
| 19.5 Replication Notes and Tips 3820                                             |      |
| 19.5.1 Replication Features and Issues 3820                                      |      |
| 19.5.2 Replication Compatibility Between MySQL Versions 3847                     |      |
| 19.5.3 Upgrading a Replication Topology 3848                                     |      |
| 19.5.4 Troubleshooting Replication                                               | 3850 |
| 19.5.5 How to Report Replication Bugs or Problems 3851                           |      |

Replication enables data from one MySQL database server (known as a source) to be copied to one or more MySQL database servers (known as replicas). Replication is asynchronous by default; replicas do not need to be connected permanently to receive updates from a source. Depending on the configuration, you can replicate all databases, selected databases, or even selected tables within a database.

Advantages of replication in MySQL include:

• Scale-out solutions - spreading the load among multiple replicas to improve performance. In this environment, all writes and updates must take place on the source server. Reads, however, may take place on one or more replicas. This model can improve the performance of writes (since the source is dedicated to updates), while dramatically increasing read speed across an increasing number of replicas.

- Data security because the replica can pause the replication process, it is possible to run backup services on the replica without corrupting the corresponding source data.
- Analytics live data can be created on the source, while the analysis of the information can take place on the replica without affecting the performance of the source.
- Long-distance data distribution you can use replication to create a local copy of data for a remote site to use, without permanent access to the source.

For information on how to use replication in such scenarios, see Section 19.4, "Replication Solutions".

MySQL 8.0 supports different methods of replication. The traditional method is based on replicating events from the source's binary log, and requires the log files and positions in them to be synchronized between source and replica. The newer method based on global transaction identifiers (GTIDs) is transactional and therefore does not require working with log files or positions within these files, which greatly simplifies many common replication tasks. Replication using GTIDs guarantees consistency between source and replica as long as all transactions committed on the source have also been applied on the replica. For more information about GTIDs and GTID-based replication in MySQL, see [Section 19.1.3, "Replication with Global Transaction Identifiers"](#page-20-0). For information on using binary log file position based replication, see [Section 19.1, "Configuring Replication"](#page-8-0).

Replication in MySQL supports different types of synchronization. The original type of synchronization is one-way, asynchronous replication, in which one server acts as the source, while one or more other servers act as replicas. This is in contrast to the synchronous replication which is a characteristic of NDB Cluster (see Chapter 25, MySQL NDB Cluster 8.0). In MySQL 8.0, semisynchronous replication is supported in addition to the built-in asynchronous replication. With semisynchronous replication, a commit performed on the source blocks before returning to the session that performed the transaction until at least one replica acknowledges that it has received and logged the events for the transaction; see Section 19.4.10, "Semisynchronous Replication". MySQL 8.0 also supports delayed replication such that a replica deliberately lags behind the source by at least a specified amount of time; see Section 19.4.11, "Delayed Replication". For scenarios where synchronous replication is required, use NDB Cluster (see Chapter 25, MySQL NDB Cluster 8.0).

There are a number of solutions available for setting up replication between servers, and the best method to use depends on the presence of data and the engine types you are using. For more information on the available options, see [Section 19.1.2, "Setting Up Binary Log File Position Based](#page-9-0) [Replication".](#page-9-0)

There are two core types of replication format, Statement Based Replication (SBR), which replicates entire SQL statements, and Row Based Replication (RBR), which replicates only the changed rows. You can also use a third variety, Mixed Based Replication (MBR). For more information on the different replication formats, see [Section 19.2.1, "Replication Formats"](#page-179-1).

Replication is controlled through a number of different options and variables. For more information, see [Section 19.1.6, "Replication and Binary Logging Options and Variables".](#page-57-0) Additional security measures can be applied to a replication topology, as described in Section 19.3, "Replication Security".

You can use replication to solve a number of different problems, including performance, supporting the backup of different databases, and as part of a larger solution to alleviate system failures. For information on how to address these issues, see Section 19.4, "Replication Solutions".

For notes and tips on how different data types and statements are treated during replication, including details of replication features, version compatibility, upgrades, and potential problems and their resolution, see Section 19.5, "Replication Notes and Tips". For answers to some questions often asked by those who are new to MySQL Replication, see Section A.14, "MySQL 8.0 FAQ: Replication".

For detailed information on the implementation of replication, how replication works, the process and contents of the binary log, background threads and the rules used to decide how statements are recorded and replicated, see [Section 19.2, "Replication Implementation".](#page-179-0)

# <span id="page-8-0"></span>**19.1 Configuring Replication**

This section describes how to configure the different types of replication available in MySQL and includes the setup and configuration required for a replication environment, including step-by-step instructions for creating a new replication environment. The major components of this section are:

- For a guide to setting up two or more servers for replication using binary log file positions, [Section 19.1.2, "Setting Up Binary Log File Position Based Replication"](#page-9-0), deals with the configuration of the servers and provides methods for copying data between the source and replicas.
- For a guide to setting up two or more servers for replication using GTID transactions, [Section 19.1.3,](#page-20-0) ["Replication with Global Transaction Identifiers",](#page-20-0) deals with the configuration of the servers.
- Events in the binary log are recorded using a number of formats. These are referred to as statementbased replication (SBR) or row-based replication (RBR). A third type, mixed-format replication (MIXED), uses SBR or RBR replication automatically to take advantage of the benefits of both SBR and RBR formats when appropriate. The different formats are discussed in [Section 19.2.1,](#page-179-1) ["Replication Formats".](#page-179-1)
- Detailed information on the different configuration options and variables that apply to replication is provided in [Section 19.1.6, "Replication and Binary Logging Options and Variables"](#page-57-0).
- Once started, the replication process should require little administration or monitoring. However, for advice on common tasks that you may want to execute, see [Section 19.1.7, "Common Replication](#page-172-0) [Administration Tasks"](#page-172-0).

## <span id="page-8-1"></span>**19.1.1 Binary Log File Position Based Replication Configuration Overview**

This section describes replication between MySQL servers based on the binary log file position method, where the MySQL instance operating as the source (where the database changes take place) writes updates and changes as "events" to the binary log. The information in the binary log is stored in different logging formats according to the database changes being recorded. Replicas are configured to read the binary log from the source and to execute the events in the binary log on the replica's local database.

Each replica receives a copy of the entire contents of the binary log. It is the responsibility of the replica to decide which statements in the binary log should be executed. Unless you specify otherwise, all events in the source's binary log are executed on the replica. If required, you can configure the replica to process only events that apply to particular databases or tables.

![](_page_8_Picture_11.jpeg)

#### **Important**

You cannot configure the source to log only certain events.

Each replica keeps a record of the binary log coordinates: the file name and position within the file that it has read and processed from the source. This means that multiple replicas can be connected to the source and executing different parts of the same binary log. Because the replicas control this process, individual replicas can be connected and disconnected from the server without affecting the source's operation. Also, because each replica records the current position within the binary log, it is possible for replicas to be disconnected, reconnect and then resume processing.

The source and each replica must be configured with a unique ID (using the [server\\_id](#page-57-1) system variable). In addition, each replica must be configured with information about the source's host name, log file name, and position within that file. These details can be controlled from within a MySQL session using a CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) on the replica. The details are stored within the replica's connection metadata repository (see [Section 19.2.4, "Relay Log and Replication Metadata Repositories"](#page-193-0)).

## <span id="page-9-0"></span>**19.1.2 Setting Up Binary Log File Position Based Replication**

This section describes how to set up a MySQL server to use binary log file position based replication. There are a number of different methods for setting up replication, and the exact method to use depends on how you are setting up replication, and whether you already have data in the database on the source that you want to replicate.

![](_page_9_Picture_3.jpeg)

#### **Tip**

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster.md) which enables you to easily administer a group of MySQL server instances in [MySQL](https://dev.mysql.com/doc/mysql-shell/8.0/en/) [Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.0/en/) which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-replicaset.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

There are some generic tasks that are common to all setups:

- On the source, you must ensure that binary logging is enabled, and configure a unique server ID. This might require a server restart. See [Section 19.1.2.1, "Setting the Replication Source](#page-10-0) [Configuration".](#page-10-0)
- On each replica that you want to connect to the source, you must configure a unique server ID. This might require a server restart. See [Section 19.1.2.2, "Setting the Replica Configuration"](#page-10-1).
- Optionally, create a separate user for your replicas to use during authentication with the source when reading the binary log for replication. See [Section 19.1.2.3, "Creating a User for Replication"](#page-11-0).
- Before creating a data snapshot or starting the replication process, on the source you should record the current position in the binary log. You need this information when configuring the replica so that the replica knows where within the binary log to start executing events. See [Section 19.1.2.4,](#page-12-0) ["Obtaining the Replication Source Binary Log Coordinates"](#page-12-0).
- If you already have data on the source and want to use it to synchronize the replica, you need to create a data snapshot to copy the data to the replica. The storage engine you are using has an impact on how you create the snapshot. When you are using MyISAM, you must stop processing statements on the source to obtain a read-lock, then obtain its current binary log coordinates and dump its data, before permitting the source to continue executing statements. If you do not stop the execution of statements, the data dump and the source status information become mismatched, resulting in inconsistent or corrupted databases on the replicas. For more information on replicating a MyISAM source, see [Section 19.1.2.4, "Obtaining the Replication Source Binary Log Coordinates"](#page-12-0). If you are using InnoDB, you do not need a read-lock and a transaction that is long enough to transfer the data snapshot is sufficient. For more information, see Section 17.19, "InnoDB and MySQL Replication".
- Configure the replica with settings for connecting to the source, such as the host name, login credentials, and binary log file name and position. See [Section 19.1.2.7, "Setting the Source](#page-18-0) [Configuration on the Replica".](#page-18-0)
- Implement replication-specific security measures on the sources and replicas as appropriate for your system. See Section 19.3, "Replication Security".

![](_page_9_Picture_14.jpeg)

#### **Note**

Certain steps within the setup process require the SUPER privilege. If you do not have this privilege, it might not be possible to enable replication.

After configuring the basic options, select your scenario:

- To set up replication for a fresh installation of a source and replicas that contain no data, see [Setting](#page-16-0) [Up Replication with New Source and Replicas](#page-16-0).
- To set up replication of a new source using the data from an existing MySQL server, see [Setting Up](#page-16-1) [Replication with Existing Data.](#page-16-1)
- To add replicas to an existing replication environment, see [Section 19.1.2.8, "Adding Replicas to a](#page-18-1) [Replication Environment".](#page-18-1)

Before administering MySQL replication servers, read this entire chapter and try all statements mentioned in Section 15.4.1, "SQL Statements for Controlling Source Servers", and Section 15.4.2, "SQL Statements for Controlling Replica Servers". Also familiarize yourself with the replication startup options described in [Section 19.1.6, "Replication and Binary Logging Options and Variables"](#page-57-0).

## <span id="page-10-0"></span>**19.1.2.1 Setting the Replication Source Configuration**

To configure a source to use binary log file position based replication, you must ensure that binary logging is enabled, and establish a unique server ID.

Each server within a replication topology must be configured with a unique server ID, which you can specify using the [server\\_id](#page-57-1) system variable. This server ID is used to identify individual servers within the replication topology, and must be a positive integer between 1 and (232)−1. The default [server\\_id](#page-57-1) value from MySQL 8.0 is 1. You can change the [server\\_id](#page-57-1) value dynamically by issuing a statement like this:

```
SET GLOBAL server_id = 2;
```

How you organize and select the server IDs is your choice, so long as each server ID is different from every other server ID in use by any other server in the replication topology. Note that if a value of 0 (which was the default in earlier releases) was set previously for the server ID, you must restart the server to initialize the source with your new nonzero server ID. Otherwise, a server restart is not needed when you change the server ID, unless you make other configuration changes that require it.

Binary logging is required on the source because the binary log is the basis for replicating changes from the source to its replicas. Binary logging is enabled by default (the [log\\_bin](#page-156-0) system variable is set to ON). The [--log-bin](#page-134-0) option tells the server what base name to use for binary log files. It is recommended that you specify this option to give the binary log files a non-default base name, so that if the host name changes, you can easily continue to use the same binary log file names (see Section B.3.7, "Known Issues in MySQL"). If binary logging was previously disabled on the source using the [--skip-log-bin](#page-134-0) option, you must restart the server without this option to enable it.

![](_page_10_Picture_11.jpeg)

#### **Note**

The following options also have an impact on the source:

- For the greatest possible durability and consistency in a replication setup using InnoDB with transactions, you should use innodb\_flush\_log\_at\_trx\_commit=1 and sync\_binlog=1 in the source's my.cnf file.
- Ensure that the skip\_networking system variable is not enabled on the source. If networking has been disabled, the replica cannot communicate with the source and replication fails.

## <span id="page-10-1"></span>**19.1.2.2 Setting the Replica Configuration**

Each replica must have a unique server ID, as specified by the [server\\_id](#page-57-1) system variable. If you are setting up multiple replicas, each one must have a unique [server\\_id](#page-57-1) value that differs from that of the source and from any of the other replicas. If the replica's server ID is not already set, or the current value conflicts with the value that you have chosen for the source or another replica, you must change it.

The default [server\\_id](#page-57-1) value is 1. You can change the [server\\_id](#page-57-1) value dynamically by issuing a statement like this:

```
SET GLOBAL server_id = 21;
```

Note that a value of 0 for the server ID prevents a replica from connecting to a source. If that server ID value (which was the default in earlier releases) was set previously, you must restart the server to initialize the replica with your new nonzero server ID. Otherwise, a server restart is not needed when you change the server ID, unless you make other configuration changes that require it. For example, if binary logging was disabled on the server and you want it enabled for your replica, a server restart is required to enable this.

If you are shutting down the replica server, you can edit the [mysqld] section of the configuration file to specify a unique server ID. For example:

```
[mysqld]
server-id=21
```

Binary logging is enabled by default on all servers. A replica is not required to have binary logging enabled for replication to take place. However, binary logging on a replica means that the replica's binary log can be used for data backups and crash recovery. Replicas that have binary logging enabled can also be used as part of a more complex replication topology. For example, you might want to set up replication servers using this chained arrangement:

```
A -> B -> C
```

Here, A serves as the source for the replica B, and B serves as the source for the replica C. For this to work, B must be both a source and a replica. Updates received from A must be logged by B to its binary log, in order to be passed on to C. In addition to binary logging, this replication topology requires the system variable [log\\_replica\\_updates](#page-158-0) (from MySQL 8.0.26) or [log\\_slave\\_updates](#page-159-0) (before MySQL 8.0.26) to be enabled. With replica updates enabled, the replica writes updates that are received from a source and performed by the replica's SQL thread to the replica's own binary log. The [log\\_replica\\_updates](#page-158-0) or [log\\_slave\\_updates](#page-159-0) system variable is enabled by default.

If you need to disable binary logging or replica update logging on a replica, you can do this by specifying the [--skip-log-bin](#page-134-0) and [--log-replica-updates=OFF](#page-158-0) or [--log-slave](#page-159-0)[updates=OFF](#page-159-0) options for the replica. If you decide to re-enable these features on the replica, remove the relevant options and restart the server.

## <span id="page-11-0"></span>**19.1.2.3 Creating a User for Replication**

Each replica connects to the source using a MySQL user name and password, so there must be a user account on the source that the replica can use to connect. The user name is specified by the SOURCE\_USER | MASTER\_USER option of the CHANGE REPLICATION SOURCE TO statement (from MySQL 8.0.23) or CHANGE MASTER TO statement (before MySQL 8.0.23) when you set up a replica. Any account can be used for this operation, providing it has been granted the REPLICATION SLAVE privilege. You can choose to create a different account for each replica, or connect to the source using the same account for each replica.

Although you do not have to create an account specifically for replication, you should be aware that the replication user name and password are stored in plain text in the replica's connection metadata repository mysql.slave\_master\_info (see [Section 19.2.4.2, "Replication Metadata Repositories"](#page-195-0)). Therefore, you may want to create a separate account that has privileges only for the replication process, to minimize the possibility of compromise to other accounts.

To create a new account, use CREATE USER. To grant this account the privileges required for replication, use the GRANT statement. If you create an account solely for the purposes of replication, that account needs only the REPLICATION SLAVE privilege. For example, to set up a new user, repl, that can connect for replication from any host within the example.com domain, issue these statements on the source:

```
mysql> CREATE USER 'repl'@'%.example.com' IDENTIFIED BY 'password';
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%.example.com';
```

See Section 15.7.1, "Account Management Statements", for more information on statements for manipulation of user accounts.

![](_page_12_Picture_3.jpeg)

#### **Important**

To connect to the source using a user account that authenticates with the caching\_sha2\_password plugin, you must either set up a secure connection as described in Section 19.3.1, "Setting Up Replication to Use Encrypted Connections", or enable the unencrypted connection to support password exchange using an RSA key pair. The caching\_sha2\_password authentication plugin is the default for new users created from MySQL 8.0 (for details, see Section 8.4.1.2, "Caching SHA-2 Pluggable Authentication"). If the user account that you create or use for replication (as specified by the MASTER\_USER option) uses this authentication plugin, and you are not using a secure connection, you must enable RSA key pair-based password exchange for a successful connection.

## <span id="page-12-0"></span>**19.1.2.4 Obtaining the Replication Source Binary Log Coordinates**

To configure the replica to start the replication process at the correct point, you need to note the source's current coordinates within its binary log.

![](_page_12_Picture_8.jpeg)

#### **Warning**

This procedure uses FLUSH TABLES WITH READ LOCK, which blocks COMMIT operations for InnoDB tables.

If you are planning to shut down the source to create a data snapshot, you can optionally skip this procedure and instead store a copy of the binary log index file along with the data snapshot. In that situation, the source creates a new binary log file on restart. The source binary log coordinates where the replica must start the replication process are therefore the start of that new file, which is the next binary log file on the source following after the files that are listed in the copied binary log index file.

To obtain the source binary log coordinates, follow these steps:

1. Start a session on the source by connecting to it with the command-line client, and flush all tables and block write statements by executing the FLUSH TABLES WITH READ LOCK statement:

```
mysql> FLUSH TABLES WITH READ LOCK;
```

![](_page_12_Picture_15.jpeg)

#### **Warning**

Leave the client from which you issued the FLUSH TABLES statement running so that the read lock remains in effect. If you exit the client, the lock is released.

2. In a different session on the source, use the SHOW MASTER STATUS statement to determine the current binary log file name and position:

```
mysql> SHOW MASTER STATUS\G
*************************** 1. row ***************************
 File: mysql-bin.000003
 Position: 73
 Binlog_Do_DB: test
 Binlog_Ignore_DB: manual, mysql
Executed_Gtid_Set: 3E11FA47-71CA-11E1-9E33-C80AA9429562:1-5
1 row in set (0.00 sec)
```

The File column shows the name of the log file and the Position column shows the position within the file. In this example, the binary log file is mysql-bin.000003 and the position is 73.

Record these values. You need them later when you are setting up the replica. They represent the replication coordinates at which the replica should begin processing new updates from the source.

If the source has been running previously with binary logging disabled, the log file name and position values displayed by SHOW MASTER STATUS or mysqldump --master-data are empty. In that case, the values that you need to use later when specifying the source's binary log file and position are the empty string ('') and 4.

You now have the information you need to enable the replica to start reading from the source's binary log in the correct place to start replication.

The next step depends on whether you have existing data on the source. Choose one of the following options:

- If you have existing data that needs be to synchronized with the replica before you start replication, leave the client running so that the lock remains in place. This prevents any further changes being made, so that the data copied to the replica is in synchrony with the source. Proceed to [Section 19.1.2.5, "Choosing a Method for Data Snapshots".](#page-13-0)
- If you are setting up a new source and replica combination, you can exit the first session to release the read lock. See [Setting Up Replication with New Source and Replicas](#page-16-0) for how to proceed.

## <span id="page-13-0"></span>**19.1.2.5 Choosing a Method for Data Snapshots**

If the source database contains existing data it is necessary to copy this data to each replica. There are different ways to dump the data from the source database. The following sections describe possible options.

To select the appropriate method of dumping the database, choose between these options:

- Use the mysqldump tool to create a dump of all the databases you want to replicate. This is the recommended method, especially when using InnoDB.
- If your database is stored in binary portable files, you can copy the raw data files to a replica. This can be more efficient than using mysqldump and importing the file on each replica, because it skips the overhead of updating indexes as the INSERT statements are replayed. With storage engines such as InnoDB this is not recommended.
- Use MySQL Server's clone plugin to transfer all the data from an existing replica to a clone. For instructions to use this method, see Section 7.6.7.7, "Cloning for Replication".

![](_page_13_Picture_13.jpeg)

#### **Tip**

To deploy multiple instances of MySQL, you can use [InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-cluster.md) which enables you to easily administer a group of MySQL server instances in [MySQL](https://dev.mysql.com/doc/mysql-shell/8.0/en/) [Shell](https://dev.mysql.com/doc/mysql-shell/8.0/en/). InnoDB Cluster wraps MySQL Group Replication in a programmatic environment that enables you easily deploy a cluster of MySQL instances to achieve high availability. In addition, InnoDB Cluster interfaces seamlessly with [MySQL Router,](https://dev.mysql.com/doc/mysql-router/8.0/en/) which enables your applications to connect to the cluster without writing your own failover process. For similar use cases that do not require high availability, however, you can use [InnoDB ReplicaSet.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-innodb-replicaset.md) Installation instructions for MySQL Shell can be found [here.](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.md)

## **Creating a Data Snapshot Using mysqldump**

To create a snapshot of the data in an existing source database, use the mysqldump tool. Once the data dump has been completed, import this data into the replica before starting the replication process.

The following example dumps all databases to a file named dbdump.db, and includes the --masterdata option which automatically appends the CHANGE REPLICATION SOURCE TO | CHANGE MASTER TO statement required on the replica to start the replication process:

\$> **mysqldump --all-databases --master-data > dbdump.db**

![](_page_14_Picture_2.jpeg)

#### **Note**

If you do not use --master-data, then it is necessary to lock all tables in a separate session manually. See [Section 19.1.2.4, "Obtaining the Replication](#page-12-0) [Source Binary Log Coordinates"](#page-12-0).

It is possible to exclude certain databases from the dump using the mysqldump tool. If you want to choose which databases to include in the dump, do not use --all-databases. Choose one of these options:

- Exclude all the tables in the database using --ignore-table option.
- Name only those databases which you want dumped using the --databases option.

![](_page_14_Picture_8.jpeg)

#### **Note**

By default, if GTIDs are in use on the source ([gtid\\_mode=ON](#page-168-0)), mysqldump includes the GTIDs from the [gtid\\_executed](#page-167-0) set on the source in the dump output to add them to the [gtid\\_purged](#page-170-0) set on the replica. If you are dumping only specific databases or tables, it is important to note that the value that is included by mysqldump includes the GTIDs of all transactions in the [gtid\\_executed](#page-167-0) set on the source, even those that changed suppressed parts of the database, or other databases on the server that were not included in the partial dump. Check the description for mysqldump's --set-gtidpurged option to find the outcome of the default behavior for the MySQL Server versions you are using, and how to change the behavior if this outcome is not suitable for your situation.

For more information, see Section 6.5.4, "mysqldump — A Database Backup Program".

To import the data, either copy the dump file to the replica, or access the file from the source when connecting remotely to the replica.

#### **Creating a Data Snapshot Using Raw Data Files**

This section describes how to create a data snapshot using the raw files which make up the database. Employing this method with a table using a storage engine that has complex caching or logging algorithms requires extra steps to produce a perfect "point in time" snapshot: the initial copy command could leave out cache information and logging updates, even if you have acquired a global read lock. How the storage engine responds to this depends on its crash recovery abilities.

If you use InnoDB tables, you can use the mysqlbackup command from the MySQL Enterprise Backup component to produce a consistent snapshot. This command records the log name and offset corresponding to the snapshot to be used on the replica. MySQL Enterprise Backup is a commercial product that is included as part of a MySQL Enterprise subscription. See Section 32.1, "MySQL Enterprise Backup Overview" for detailed information.

This method also does not work reliably if the source and replica have different values for ft\_stopword\_file, ft\_min\_word\_len, or ft\_max\_word\_len and you are copying tables having full-text indexes.

Assuming the above exceptions do not apply to your database, use the cold backup technique to obtain a reliable binary snapshot of InnoDB tables: do a slow shutdown of the MySQL Server, then copy the data files manually.

To create a raw data snapshot of MyISAM tables when your MySQL data files exist on a single file system, you can use standard file copy tools such as cp or copy, a remote copy tool such as scp or rsync, an archiving tool such as zip or tar, or a file system snapshot tool such as dump. If you are replicating only certain databases, copy only those files that relate to those tables. For InnoDB, all tables in all databases are stored in the system tablespace files, unless you have the innodb\_file\_per\_table option enabled.

The following files are not required for replication:

- Files relating to the mysql database.
- The replica's connection metadata repository file master.info, if used; the use of this file is now deprecated (see [Section 19.2.4, "Relay Log and Replication Metadata Repositories"\)](#page-193-0).
- The source's binary log files, with the exception of the binary log index file if you are going to use this to locate the source binary log coordinates for the replica.
- Any relay log files.

Depending on whether you are using InnoDB tables or not, choose one of the following:

If you are using InnoDB tables, and also to get the most consistent results with a raw data snapshot, shut down the source server during the process, as follows:

- 1. Acquire a read lock and get the source's status. See [Section 19.1.2.4, "Obtaining the Replication](#page-12-0) [Source Binary Log Coordinates"](#page-12-0).
- 2. In a separate session, shut down the source server:

```
$> mysqladmin shutdown
```

3. Make a copy of the MySQL data files. The following examples show common ways to do this. You need to choose only one of them:

```
$> tar cf /tmp/db.tar ./data
$> zip -r /tmp/db.zip ./data
$> rsync --recursive ./data /tmp/dbdata
```

4. Restart the source server.

If you are not using InnoDB tables, you can get a snapshot of the system from a source without shutting down the server as described in the following steps:

- 1. Acquire a read lock and get the source's status. See [Section 19.1.2.4, "Obtaining the Replication](#page-12-0) [Source Binary Log Coordinates"](#page-12-0).
- 2. Make a copy of the MySQL data files. The following examples show common ways to do this. You need to choose only one of them:

```
$> tar cf /tmp/db.tar ./data
$> zip -r /tmp/db.zip ./data
$> rsync --recursive ./data /tmp/dbdata
```

3. In the client where you acquired the read lock, release the lock:

```
mysql> UNLOCK TABLES;
```

Once you have created the archive or copy of the database, copy the files to each replica before starting the replication process.