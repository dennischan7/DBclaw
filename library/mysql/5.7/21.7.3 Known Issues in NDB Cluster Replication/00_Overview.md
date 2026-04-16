---
source: MySQL 5.7 Reference
title: 00_Overview
---

This section discusses known problems or issues when using replication with NDB Cluster.

**Loss of connection between source and replica.** A loss of connection can occur either between the source cluster SQL node and the replica cluster SQL node, or between the source SQL node and the data nodes of the source cluster. In the latter case, this can occur not only as a result of loss of physical connection (for example, a broken network cable), but due to the overflow of data node event buffers; if the SQL node is too slow to respond, it may be dropped by the cluster (this is controllable to some degree by adjusting the MaxBufferedEpochs and TimeBetweenEpochs configuration parameters). If this occurs, it is entirely possible for new data to be inserted into the source cluster without being recorded in the source SQL node's binary log. For this reason, to guarantee high availability, it is extremely important to maintain a backup replication channel, to monitor the primary channel, and to fail over to the secondary replication channel when necessary to keep the replica cluster synchronized with the source. NDB Cluster is not designed to perform such monitoring on its own; for this, an external application is required.

 The source SQL node issues a "gap" event when connecting or reconnecting to the source cluster. (A gap event is a type of "incident event," which indicates an incident that occurs that affects the contents of the database but that cannot easily be represented as a set of changes. Examples of incidents are server failures, database resynchronization, some software updates, and some hardware changes.) When the replica encounters a gap in the replication log, it stops with an error message. This message is available in the output of SHOW SLAVE STATUS, and indicates that the SQL thread has stopped due to an incident registered in the replication stream, and that manual intervention is required. See [Section 21.7.8, "Implementing Failover with NDB Cluster Replication",](#page-126-0) for more information about what to do in such circumstances.

![](_page_109_Picture_5.jpeg)

### **Important**

Because NDB Cluster is not designed on its own to monitor replication status or provide failover, if high availability is a requirement for the replica server or cluster, then you must set up multiple replication lines, monitor the source mysqld on the primary replication line, and be prepared fail over to a secondary line if and as necessary. This must be done manually, or possibly by means of a third-party application. For information about implementing this type of setup, see [Section 21.7.7, "Using Two Replication Channels for NDB Cluster](#page-125-0) [Replication",](#page-125-0) and [Section 21.7.8, "Implementing Failover with NDB Cluster](#page-126-0) [Replication".](#page-126-0)

If you are replicating from a standalone MySQL server to an NDB Cluster, one channel is usually sufficient.

**Circular replication.** NDB Cluster Replication supports circular replication, as shown in the next example. The replication setup involves three NDB Clusters numbered 1, 2, and 3, in which Cluster 1 acts as the replication source for Cluster 2, Cluster 2 acts as the source for Cluster 3, and Cluster 3 acts as the source for Cluster 1, thus completing the circle. Each NDB Cluster has two SQL nodes, with SQL nodes A and B belonging to Cluster 1, SQL nodes C and D belonging to Cluster 2, and SQL nodes E and F belonging to Cluster 3.

Circular replication using these clusters is supported as long as the following conditions are met:

- The SQL nodes on all source and replica clusters are the same.
- All SQL nodes acting as sources and replicas are started with the log\_slave\_updates system variable enabled.

This type of circular replication setup is shown in the following diagram:

![](_page_110_Figure_1.jpeg)

**Figure 21.13 NDB Cluster Circular Replication With All Sources As Replicas**

In this scenario, SQL node A in Cluster 1 replicates to SQL node C in Cluster 2; SQL node C replicates to SQL node E in Cluster 3; SQL node E replicates to SQL node A. In other words, the replication line (indicated by the curved arrows in the diagram) directly connects all SQL nodes used as sources and replicas.

It should also be possible to set up circular replication in which not all source SQL nodes are also replicas, as shown here:

![](_page_111_Figure_1.jpeg)

**Figure 21.14 NDB Cluster Circular Replication Where Not All Sources Are Replicas**

In this case, different SQL nodes in each cluster are used as sources and replicas. However, you must not start any of the SQL nodes with the log\_slave\_updates system variable enabled. This type of circular replication scheme for NDB Cluster, in which the line of replication (again indicated by the curved arrows in the diagram) is discontinuous, should be possible, but it should be noted that it has not yet been thoroughly tested and must therefore still be considered experimental.

![](_page_111_Picture_4.jpeg)

### **Note**

The NDB storage engine uses idempotent execution mode, which suppresses duplicate-key and other errors that otherwise break circular replication of NDB Cluster. This is equivalent to setting the global slave\_exec\_mode system variable to IDEMPOTENT, although this is not necessary in NDB Cluster replication, since NDB Cluster sets this variable automatically and ignores any attempts to set it explicitly.

**NDB Cluster replication and primary keys.** In the event of a node failure, errors in replication of NDB tables without primary keys can still occur, due to the possibility of duplicate rows being inserted in such cases. For this reason, it is highly recommended that all NDB tables being replicated have explicit primary keys.

**NDB Cluster Replication and Unique Keys.** In older versions of NDB Cluster, operations that updated values of unique key columns of NDB tables could result in duplicate-key errors when replicated. This issue is solved for replication between NDB tables by deferring unique key checks until after all table row updates have been performed.

Deferring constraints in this way is currently supported only by NDB. Thus, updates of unique keys when replicating from NDB to a different storage engine such as InnoDB or MyISAM are still not supported.

The problem encountered when replicating without deferred checking of unique key updates can be illustrated using NDB table such as t, is created and populated on the source (and transmitted to a replica that does not support deferred unique key updates) as shown here:

```
CREATE TABLE t (
 p INT PRIMARY KEY,
 c INT,
 UNIQUE KEY u (c)
) ENGINE NDB;
INSERT INTO t
 VALUES (1,1), (2,2), (3,3), (4,4), (5,5);
```

The following UPDATE statement on t succeeds on the source, since the rows affected are processed in the order determined by the ORDER BY option, performed over the entire table:

```
UPDATE t SET c = c - 1 ORDER BY p;
```

The same statement fails with a duplicate key error or other constraint violation on the replica, because the ordering of the row updates is performed for one partition at a time, rather than for the table as a whole.

![](_page_112_Picture_9.jpeg)

### **Note**

Every NDB table is implicitly partitioned by key when it is created. See [Section 22.2.5, "KEY Partitioning"](#page-175-0), for more information.

**GTIDs not supported.** Replication using global transaction IDs is not compatible with the NDB storage engine, and is not supported. Enabling GTIDs is likely to cause NDB Cluster Replication to fail.

**Multithreaded replicas not supported.** NDB Cluster does not support multithreaded replicas. This is because the replica may not be able to separate transactions occurring in one database from those in another if they are written within the same epoch. In addition, every transaction handled by the NDB storage engine involves at least two databases—the target database and the mysql system database —due to the requirement for updating the mysql.ndb\_apply\_status table (see [Section 21.7.4,](#page-115-0) ["NDB Cluster Replication Schema and Tables"](#page-115-0)). This in turn breaks the requirement for multithreading that the transaction is specific to a given database.

Prior to NDB 7.5.7 and NDB 7.6.3, setting any system variables relating to multithreaded slaves such as slave\_parallel\_workers and slave\_checkpoint\_group (or the equivalent mysqld startup options) was completely ignored, and had no effect.

Beginning with NDB 7.5.7 and NDB 7.6.3, slave\_parallel\_workers is always 0. If set to any other value on startup, NDB changes it to 0, and writes a message to the mysqld server log file.

**Restarting with --initial.** Restarting the cluster with the --initial option causes the sequence of GCI and epoch numbers to start over from 0. (This is generally true of NDB Cluster and not limited to replication scenarios involving Cluster.) The MySQL servers involved in replication should in this case

be restarted. After this, you should use the RESET MASTER and RESET SLAVE statements to clear the invalid ndb\_binlog\_index and ndb\_apply\_status tables, respectively.

<span id="page-113-0"></span>**Replication from NDB to other storage engines.** It is possible to replicate an NDB table on the source to a table using a different storage engine on the replica, taking into account the restrictions listed here:

- Multi-source and circular replication are not supported (tables on both the source and the replica must use the NDB storage engine for this to work).
- Using a storage engine which does not perform binary logging for tables on the replica requires special handling.
- Use of a nontransactional storage engine for tables on the replica also requires special handling.
- The source mysqld must be started with --ndb-log-update-as-write=0 or --ndb-logupdate-as-write=OFF.

The next few paragraphs provide additional information about each of the issues just described.

**Multiple sources not supported when replicating NDB to other storage engines.** For replication from NDB to a different storage engine, the relationship between the two databases must be one-toone. This means that bidirectional or circular replication is not supported between NDB Cluster and other storage engines.

In addition, it is not possible to configure more than one replication channel when replicating between NDB and a different storage engine. (An NDB Cluster database can simultaneously replicate to multiple NDB Cluster databases.) If the source uses NDB tables, it is still possible to have more than one MySQL Server maintain a binary log of all changes, but for the replica to change sources (fail over), the new source-replica relationship must be explicitly defined on the replica.

**Replicating NDB tables to a storage engine that does not perform binary logging.** If you attempt to replicate from an NDB Cluster to a replica that uses a storage engine that does not handle its own binary logging, the replication process aborts with the error Binary logging not possible ... Statement cannot be written atomically since more than one engine involved and at least one engine is self-logging (Error 1595). It is possible to work around this issue in one of the following ways:

- **Turn off binary logging on the replica.** This can be accomplished by setting sql\_log\_bin = 0.
- **Change the storage engine used for the mysql.ndb\_apply\_status table.** Causing this table to use an engine that does not handle its own binary logging can also eliminate the conflict. This can be done by issuing a statement such as ALTER TABLE mysql.ndb\_apply\_status ENGINE=MyISAM on the replica. It is safe to do this when using a storage engine other than NDB on the replica, since you do not need to worry about keeping multiple replicas synchronized.
- **Filter out changes to the mysql.ndb\_apply\_status table on the replica.** This can be done by starting the replica with --replicate-ignore-table=mysql.ndb\_apply\_status. If you need for other tables to be ignored by replication, you might wish to use an appropriate --replicatewild-ignore-table option instead.

![](_page_113_Picture_14.jpeg)

### **Important**

You should not disable replication or binary logging of mysql.ndb\_apply\_status or change the storage engine used for this table when replicating from one NDB Cluster to another. See [Replication and binary](#page-114-0) [log filtering rules with replication between NDB Clusters,](#page-114-0) for details.

<span id="page-113-1"></span>**Replication from NDB to a nontransactional storage engine.** When replicating from NDB to a nontransactional storage engine such as MyISAM, you may encounter unnecessary duplicate key

errors when replicating INSERT ... ON DUPLICATE KEY UPDATE statements. You can suppress these by using --ndb-log-update-as-write=0, which forces updates to be logged as writes, rather than as updates.

<span id="page-114-0"></span>**Replication and binary log filtering rules with replication between NDB Clusters.** If you are using any of the options --replicate-do-\*, --replicate-ignore-\*, --binlog-do-db, or - binlog-ignore-db to filter databases or tables being replicated, you must take care not to block replication or binary logging of the mysql.ndb\_apply\_status, which is required for replication between NDB Clusters to operate properly. In particular, you must keep in mind the following:

1. Using --replicate-do-db=db\_name (and no other --replicate-do-\* or --replicateignore-\* options) means that only tables in database db\_name are replicated. In this case, you should also use --replicate-do-db=mysql, --binlog-do-db=mysql, or --replicatedo-table=mysql.ndb\_apply\_status to ensure that mysql.ndb\_apply\_status is populated on replicas.

Using --binlog-do-db=db\_name (and no other --binlog-do-db options) means that changes only to tables in database db\_name are written to the binary log. In this case, you should also use --replicate-do-db=mysql, --binlog-do-db=mysql, or --replicate-dotable=mysql.ndb\_apply\_status to ensure that mysql.ndb\_apply\_status is populated on replicas.

2. Using --replicate-ignore-db=mysql means that no tables in the mysql database are replicated. In this case, you should also use --replicate-dotable=mysql.ndb\_apply\_status to ensure that mysql.ndb\_apply\_status is replicated.

Using --binlog-ignore-db=mysql means that no changes to tables in the mysql database are written to the binary log. In this case, you should also use --replicate-dotable=mysql.ndb\_apply\_status to ensure that mysql.ndb\_apply\_status is replicated.

You should also remember that each replication rule requires the following:

- 1. Its own --replicate-do-\* or --replicate-ignore-\* option, and that multiple rules cannot be expressed in a single replication filtering option. For information about these rules, see Section 16.1.6, "Replication and Binary Logging Options and Variables".
- 2. Its own --binlog-do-db or --binlog-ignore-db option, and that multiple rules cannot be expressed in a single binary log filtering option. For information about these rules, see Section 5.4.4, "The Binary Log".

If you are replicating an NDB Cluster to a replica that uses a storage engine other than NDB, the considerations just given previously may not apply, as discussed elsewhere in this section.

**NDB Cluster Replication and IPv6.** While the NDB API and MGM API (and thus data nodes and management nodes) do not support IPv6 in NDB 7.5 and 7.6, MySQL Servers—including those acting as SQL nodes in an NDB Cluster—can use IPv6 to contact other MySQL Servers. This means that you can replicate between NDB Clusters using IPv6 to connect the source and replica SQL nodes as shown by the dotted arrow in the following diagram:

![](_page_115_Figure_1.jpeg)

**Figure 21.15 Replication Between SQL Nodes Connected Using IPv6**

All connections originating within the NDB Cluster —represented in the preceding diagram by solid arrows—must use IPv4. In other words, all NDB Cluster data nodes, management servers, and management clients must be accessible from one another using IPv4. In addition, SQL nodes must use IPv4 to communicate with the cluster.

Since there is currently no support in the NDB and MGM APIs for IPv6, any applications written using these APIs must also make all connections using IPv4.

**Attribute promotion and demotion.** NDB Cluster Replication includes support for attribute promotion and demotion. The implementation of the latter distinguishes between lossy and non-lossy type conversions, and their use on the replica can be controlled by setting the slave\_type\_conversions global server system variable.

For more information about attribute promotion and demotion in NDB Cluster, see Row-based replication: attribute promotion and demotion.

NDB, unlike InnoDB or MyISAM, does not write changes to virtual columns to the binary log; however, this has no detrimental effects on NDB Cluster Replication or replication between NDB and other storage engines. Changes to stored generated columns are logged.

# <span id="page-115-0"></span>**21.7.4 NDB Cluster Replication Schema and Tables**

- [ndb\\_apply\\_status Table](#page-116-0)
- [ndb\\_binlog\\_index Table](#page-116-1)
- [ndb\\_replication Table](#page-118-0)

Replication in NDB Cluster makes use of a number of dedicated tables in the mysql database on each MySQL Server instance acting as an SQL node in both the cluster being replicated and in the replica. This is true regardless of whether the replica is a single server or a cluster.

The ndb\_binlog\_index and ndb\_apply\_status tables are created in the mysql database. They should not be explicitly replicated by the user. User intervention is normally not required to create or maintain either of these tables, since both are maintained by the NDB binary log (binlog) injector thread. This keeps the source mysqld process updated to changes performed by the NDB storage engine.

The NDB binlog injector thread receives events directly from the NDB storage engine. The NDB injector is responsible for capturing all the data events within the cluster, and ensures that all events which change, insert, or delete data are recorded in the ndb\_binlog\_index table. The replica I/O thread transfers the events from the source's binary log to the replica's relay log.

The ndb\_replication table must be created manually. This table can be updated by the user to perform filtering by database or table. See [ndb\\_replication Table,](#page-118-0) for more information. ndb\_replication is also used in NDB Replication conflict detection and resolution for conflict resolution control; see [Conflict Resolution Control.](#page-140-0)

Even though ndb\_binlog\_index and ndb\_apply\_status are created and maintained automatically, it is advisable to check for the existence and integrity of these tables as an initial step in preparing an NDB Cluster for replication. It is possible to view event data recorded in the binary log by querying the mysql.ndb\_binlog\_index table directly on the source. This can be also be accomplished using the SHOW BINLOG EVENTS statement on either the source or replica SQL node. (See Section 13.7.5.2, "SHOW BINLOG EVENTS Statement".)

You can also obtain useful information from the output of SHOW ENGINE NDB STATUS.

![](_page_116_Picture_5.jpeg)

### **Note**

When performing schema changes on NDB tables, applications should wait until the ALTER TABLE statement has returned in the MySQL client connection that issued the statement before attempting to use the updated definition of the table.

# <span id="page-116-0"></span>**ndb\_apply\_status Table**

ndb\_apply\_status is used to keep a record of the operations that have been replicated from the source to the replica. If the ndb\_apply\_status table does not exist on the replica, ndb\_restore recreates it.

Unlike the case with ndb\_binlog\_index, the data in this table is not specific to any one SQL node in the (replica) cluster, and so ndb\_apply\_status can use the NDBCLUSTER storage engine, as shown here:

```
CREATE TABLE `ndb_apply_status` (
 `server_id` INT(10) UNSIGNED NOT NULL,
 `epoch` BIGINT(20) UNSIGNED NOT NULL,
 `log_name` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
 `start_pos` BIGINT(20) UNSIGNED NOT NULL,
 `end_pos` BIGINT(20) UNSIGNED NOT NULL,
 PRIMARY KEY (`server_id`) USING HASH
) ENGINE=NDBCLUSTER DEFAULT CHARSET=latin1;
```

The ndb\_apply\_status table is populated only on replicas, which means that, on the source, this table never contains any rows; thus, there is no need to allot any DataMemory to ndb\_apply\_status there.

Because this table is populated from data originating on the source, it should be allowed to replicate; any replication filtering or binary log filtering rules that inadvertently prevent the replica from updating ndb\_apply\_status, or that prevent the source from writing into the binary log may prevent replication between clusters from operating properly. For more information about potential problems arising from such filtering rules, see [Replication and binary log filtering rules with replication between](#page-114-0) [NDB Clusters.](#page-114-0)

0 in the epoch column of this table indicates a transaction originating from a storage engine other than NDB.

# <span id="page-116-1"></span>**ndb\_binlog\_index Table**

NDB Cluster Replication uses the ndb\_binlog\_index table for storing the binary log's indexing data. Since this table is local to each MySQL server and does not participate in clustering, it uses the InnoDB storage engine. This means that it must be created separately on each mysqld participating in the source cluster. (The binary log itself contains updates from all MySQL servers in the cluster.) This table is defined as follows:

```
CREATE TABLE `ndb_binlog_index` (
 `Position` BIGINT(20) UNSIGNED NOT NULL,
 `File` VARCHAR(255) NOT NULL,
 `epoch` BIGINT(20) UNSIGNED NOT NULL,
 `inserts` INT(10) UNSIGNED NOT NULL,
 `updates` INT(10) UNSIGNED NOT NULL,
 `deletes` INT(10) UNSIGNED NOT NULL,
 `schemaops` INT(10) UNSIGNED NOT NULL,
 `orig_server_id` INT(10) UNSIGNED NOT NULL,
 `orig_epoch` BIGINT(20) UNSIGNED NOT NULL,
 `gci` INT(10) UNSIGNED NOT NULL,
 `next_position` bigint(20) unsigned NOT NULL,
 `next_file` varchar(255) NOT NULL,
 PRIMARY KEY (`epoch`,`orig_server_id`,`orig_epoch`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

![](_page_117_Picture_3.jpeg)

### **Note**

Prior to NDB 7.5.2, this table always used the MyISAM storage engine. If you are upgrading from an earlier release, you can use mysql\_upgrade with the --force and --upgrade-system-tables options after starting the server.) The system table upgrade causes an ALTER TABLE ... ENGINE=INNODB statement to be executed for this table. Use of the MyISAM storage engine for this table continues to be supported for backward compatibility.

ndb\_binlog\_index may require additional disk space after being converted to InnoDB. If this becomes an issue, you may be able to conserve space by using an InnoDB tablespace for this table, changing its ROW\_FORMAT to COMPRESSED, or both. For more information, see Section 13.1.19, "CREATE TABLESPACE Statement", and Section 13.1.18, "CREATE TABLE Statement", as well as Section 14.6.3, "Tablespaces".

The size of the ndb\_binlog\_index table is dependent on the number of epochs per binary log file and the number of binary log files. The number of epochs per binary log file normally depends on the amount of binary log generated per epoch and the size of the binary log file, with smaller epochs resulting in more epochs per file. You should be aware that empty epochs produce inserts to the ndb\_binlog\_index table, even when the --ndb-log-empty-epochs option is OFF, meaning that the number of entries per file depends on the length of time that the file is in use; this relationship can be represented by the formula shown here:

```
[number of epochs per file] = [time spent per file] / TimeBetweenEpochs
```

A busy NDB Cluster writes to the binary log regularly and presumably rotates binary log files more quickly than a quiet one. This means that a "quiet" NDB Cluster with --ndb-log-empty-epochs=ON can actually have a much higher number of ndb\_binlog\_index rows per file than one with a great deal of activity.

When mysqld is started with the --ndb-log-orig option, the orig\_server\_id and orig\_epoch columns store, respectively, the ID of the server on which the event originated and the epoch in which the event took place on the originating server, which is useful in NDB Cluster replication setups employing multiple sources. The SELECT statement used to find the closest binary log position to the highest applied epoch on the replica in a multi-source setup (see [Section 21.7.10, "NDB Cluster](#page-134-0) [Replication: Bidirectional and Circular Replication"\)](#page-134-0) employs these two columns, which are not indexed. This can lead to performance issues when trying to fail over, since the query must perform a table scan, especially when the source has been running with --ndb-log-empty-epochs=ON. You can improve multi-source failover times by adding an index to these columns, as shown here:

```
ALTER TABLE mysql.ndb_binlog_index
 ADD INDEX orig_lookup USING BTREE (orig_server_id, orig_epoch);
```

Adding this index provides no benefit when replicating from a single source to a single replica, since the query used to get the binary log position in such cases makes no use of orig\_server\_id or orig\_epoch.

See [Section 21.7.8, "Implementing Failover with NDB Cluster Replication"](#page-126-0), for more information about using the next\_position and next\_file columns.

The following figure shows the relationship of the NDB Cluster replication source server, its binary log injector thread, and the mysql.ndb\_binlog\_index table.

**Figure 21.16 The Replication Source Cluster**

# <span id="page-118-0"></span>**ndb\_replication Table**

The ndb\_replication table is used to control binary logging and conflict resolution, and acts on a per-table basis. Each row in this table corresponds to a table being replicated, determines how to log changes to the table and, if a conflict resolution function is specified, and determines how to resolve conflicts for that table.

Unlike the ndb\_apply\_status and ndb\_replication tables, the ndb\_replication table must be created manually, using the SQL statement shown here:

```
CREATE TABLE mysql.ndb_replication (
 db VARBINARY(63),
 table_name VARBINARY(63),
 server_id INT UNSIGNED,
 binlog_type INT UNSIGNED,
 conflict_fn VARBINARY(128),
 PRIMARY KEY USING HASH (db, table_name, server_id)
) ENGINE=NDB
PARTITION BY KEY(db,table_name);
```

The columns of this table are listed here, with descriptions:

• db column

The name of the database containing the table to be replicated.

You may employ either or both of the wildcards \_ and % as part of the database name. (See [Matching with wildcards,](#page-121-0) later in this section.)

• table\_name column

The name of the table to be replicated.

The table name may include either or both of the wildcards \_ and %. See [Matching with wildcards](#page-121-0), later in this section.

• server\_id column

The unique server ID of the MySQL instance (SQL node) where the table resides.

0 in this column acts like a wildcard equivalent to %, and matches any server ID. (See [Matching with](#page-121-0) [wildcards,](#page-121-0) later in this section.)

• binlog\_type column

The type of binary logging to be employed. See text for values and descriptions.

• conflict\_fn column

The conflict resolution function to be applied; one of [NDB\\$OLD\(\)](#page-140-1), [NDB\\$MAX\(\),](#page-141-0) [NDB](#page-141-1) [\\$MAX\\_DELETE\\_WIN\(\)](#page-141-1), [NDB\\$EPOCH\(\),](#page-141-2) [NDB\\$EPOCH\\_TRANS\(\),](#page-143-0) [NDB\\$EPOCH2\(\),](#page-143-1) [NDB](#page-144-0) [\\$EPOCH2\\_TRANS\(\);](#page-144-0) NULL indicates that conflict resolution is not used for this table.

See [Conflict Resolution Functions](#page-140-2), for more information about these functions and their uses in NDB Replication conflict resolution.

Some conflict resolution functions (NDB\$OLD(), NDB\$EPOCH(), NDB\$EPOCH\_TRANS()) require the use of one or more user-created exceptions tables. See [Conflict Resolution Exceptions Table.](#page-144-1)

To enable conflict resolution with NDB Replication, it is necessary to create and populate this table with control information on the SQL node or nodes on which the conflict should be resolved. Depending on the conflict resolution type and method to be employed, this may be the source, the replica, or both servers. In a simple source-replica setup where data can also be changed locally on the replica this is typically the replica. In a more complex replication scheme, such as bidirectional replication, this is usually all of the sources involved. See [Section 21.7.11, "NDB Cluster Replication Conflict Resolution",](#page-138-0) for more information.

The ndb\_replication table allows table-level control over binary logging outside the scope of conflict resolution, in which case conflict\_fn is specified as NULL, while the remaining column values are used to control binary logging for a given table or set of tables matching a wildcard expression. By setting the proper value for the binlog\_type column, you can make logging for a given table or tables use a desired binary log format, or disabling binary logging altogether. Possible values for this column, with values and descriptions, are shown in the following table:

**Table 21.64 binlog\_type values, with values and descriptions**

| Value | Description                                                                                                                      |
|-------|----------------------------------------------------------------------------------------------------------------------------------|
| 0     | Use server default                                                                                                               |
| 1     | Do not log this table in the binary log (same effect<br>as sql_log_bin = 0, but applies to one or more<br>specified tables only) |
| 2     | Log updated attributes only; log these as WRITE_ROW<br>events                                                                    |
| 3     | Log full row, even if not updated (MySQL server default<br>behavior)                                                             |

| Value | Description                                                                                                                                                                                                          |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 6     | Use updated attributes, even if values are unchanged                                                                                                                                                                 |
| 7     | Log full row, even if no values are changed; log<br>updates as UPDATE_ROW events                                                                                                                                     |
| 8     | Log update as UPDATE_ROW; log only primary key<br>columns in before image, and only updated columns<br>in after image (same effect asndb-log-update<br>minimal, but applies to one or more specified tables<br>only) |
| 9     | Log update as UPDATE_ROW; log only primary key<br>columns in before image, and all columns other than<br>primary key columns in after image                                                                          |

![](_page_120_Picture_2.jpeg)

### **Note**

binlog\_type values 4 and 5 are not used, and so are omitted from the table just shown, as well as from the next table.

Several binlog\_type values are equivalent to various combinations of the mysqld logging options --ndb-log-updated-only, --ndb-log-update-as-write, and --ndb-log-updateminimal, as shown in the following table:

**Table 21.65 binlog\_type values with equivalent combinations of NDB logging options**

| Value | ndb-log-updated-only<br>Value | ndb-log-update-as<br>write Value | ndb-log-update<br>minimal Value |
|-------|-------------------------------|----------------------------------|---------------------------------|
| 0     |                               |                                  |                                 |
| 1     |                               |                                  |                                 |
| 2     | ON                            | ON                               | OFF                             |
| 3     | OFF                           | ON                               | OFF                             |
| 6     | ON                            | OFF                              | OFF                             |
| 7     | OFF                           | OFF                              | OFF                             |
| 8     | ON                            | OFF                              | ON                              |
| 9     | OFF                           | OFF                              | ON                              |

Binary logging can be set to different formats for different tables by inserting rows into the ndb\_replication table using the appropriate db, table\_name, and binlog\_type column values. The internal integer value shown in the preceding table should be used when setting the binary logging format. The following two statements set binary logging to logging of full rows ( value 3) for table test.a, and to logging of updates only ( value 2) for table test.b:

```
# Table test.a: Log full rows
INSERT INTO mysql.ndb_replication VALUES("test", "a", 0, 3, NULL);
# Table test.b: log updates only
INSERT INTO mysql.ndb_replication VALUES("test", "b", 0, 2, NULL);
```

To disable logging for one or more tables, use 1 for binlog\_type, as shown here:

```
# Disable binary logging for table test.t1
INSERT INTO mysql.ndb_replication VALUES("test", "t1", 0, 1, NULL);
# Disable binary logging for any table in 'test' whose name begins with 't'
INSERT INTO mysql.ndb_replication VALUES("test", "t%", 0, 1, NULL);
```

Disabling logging for a given table is the equivalent of setting sql\_log\_bin = 0, except that it applies to one or more tables individually. If an SQL node is not performing binary logging for a given table, it is not sent the row change events for those tables. This means that it is not receiving all changes and discarding some, but rather it is not subscribing to these changes.

Disabling logging can be useful for a number of reasons, including those listed here:

- Not sending changes across the network generally saves bandwidth, buffering, and CPU resources.
- Not logging changes to tables with very frequent updates but whose value is not great is a good fit for transient data (such as session data) that may be relatively unimportant in the event of a complete failure of the cluster.
- Using a session variable (or sql\_log\_bin) and application code, it is also possible to log (or not to log) certain SQL statements or types of SQL statements; for example, it may be desirable in some cases not to record DDL statements on one or more tables.
- Splitting replication streams into two (or more) binary logs can be done for reasons of performance, a need to replicate different databases to different places, use of different binary logging types for different databases, and so on.

<span id="page-121-0"></span>**Matching with wildcards.** In order not to make it necessary to insert a row in the ndb\_replication table for each and every combination of database, table, and SQL node in your replication setup, NDB supports wildcard matching on the this table's db, table\_name, and server\_id columns. Database and table names used in, respectively, db and table\_name may contain either or both of the following wildcards:

- \_ (underscore character): matches zero or more characters
- % (percent sign): matches a single character

(These are the same wildcards as supported by the MySQL LIKE operator.)

The server\_id column supports 0 as a wildcard equivalent to \_ (matches anything). This is used in the examples shown previously.

A given row in the ndb\_replication table can use wildcards to match any of the database name, table name, and server ID in any combination. Where there are multiple potential matches in the table, the best match is chosen, according to the table shown here, where W represents a wildcard match, E an exact match, and the greater the value in the Quality column, the better the match:

**Table 21.66 Weights of different combinations of wildcard and exact matches on columns in the mysql.ndb\_replication table**

| db | table_name | server_id | Quality |
|----|------------|-----------|---------|
| W  | W          | W         | 1       |
| W  | W          | E         | 2       |
| W  | E          | W         | 3       |
| W  | E          | E         | 4       |
| E  | W          | W         | 5       |
| E  | W          | E         | 6       |
| E  | E          | W         | 7       |
| E  | E          | E         | 8       |

Thus, an exact match on database name, table name, and server ID is considered best (strongest), while the weakest (worst) match is a wildcard match on all three columns. Only the strength of the match is considered when choosing which rule to apply; the order in which the rows occur in the table has no effect on this determination.

**Logging Full or Partial Rows.** There are two basic methods of logging rows, as determined by the setting of the --ndb-log-updated-only option for mysqld:

- Log complete rows (option set to ON)
- Log only column data that has been updated—that is, column data whose value has been set, regardless of whether or not this value was actually changed. This is the default behavior (option set to OFF).

It is usually sufficient—and more efficient—to log updated columns only; however, if you need to log full rows, you can do so by setting --ndb-log-updated-only to 0 or OFF.

**Logging Changed Data as Updates.** The setting of the MySQL Server's --ndb-log-updateas-write option determines whether logging is performed with or without the "before" image.

Because conflict resolution for updates and delete operations is done in the MySQL Server's update handler, it is necessary to control the logging performed by the replication source such that updates are updates and not writes; that is, such that updates are treated as changes in existing rows rather than the writing of new rows, even though these replace existing rows.

This option is turned on by default; in other words, updates are treated as writes. That is, updates are by default written as write\_row events in the binary log, rather than as update\_row events.

To disable the option, start the source mysqld with --ndb-log-update-as-write=0 or --ndblog-update-as-write=OFF. You must do this when replicating from NDB tables to tables using a different storage engine; see [Replication from NDB to other storage engines,](#page-113-0) and [Replication from](#page-113-1) [NDB to a nontransactional storage engine,](#page-113-1) for more information.

# <span id="page-122-0"></span>**21.7.5 Preparing the NDB Cluster for Replication**

Preparing the NDB Cluster for replication consists of the following steps:

- 1. Check all MySQL servers for version compatibility (see [Section 21.7.2, "General Requirements for](#page-107-0) [NDB Cluster Replication"](#page-107-0)).
- 2. Create a replication account on the source Cluster with the appropriate privileges, using the following two SQL statements:

```
mysqlS> CREATE USER 'replica_user'@'replica_host'
 -> IDENTIFIED BY 'replica_password';
mysqlS> GRANT REPLICATION SLAVE ON *.*
 -> TO 'replica_user'@'replica_host';
```

In the previous statement, replica\_user is the replication account user name, replica\_host is the host name or IP address of the replica, and replica\_password is the password to assign to this account.

For example, to create a replica user account with the name myreplica, logging in from the host named replica-host, and using the password 53cr37, use the following CREATE USER and GRANT statements:

```
mysqlS> CREATE USER 'myreplica'@'replica-host'
 -> IDENTIFIED BY '53cr37';
mysqlS> GRANT REPLICATION SLAVE ON *.*
 -> TO 'myreplica'@'replica-host';
```

For security reasons, it is preferable to use a unique user account—not employed for any other purpose—for the replication account.

3. Set up the replica to use the source. Using the mysql client, this can be accomplished with the following CHANGE MASTER TO statement:

```
mysqlR> CHANGE MASTER TO
 -> MASTER_HOST='source_host',
```

```
 -> MASTER_PORT=source_port,
 -> MASTER_USER='replica_user',
 -> MASTER_PASSWORD='replica_password';
```

In the previous statement, source\_host is the host name or IP address of the replication source, source\_port is the port for the replica to use when connecting to the source, replica\_user is the user name set up for the replica on the source, and replica\_password is the password set for that user account in the previous step.

For example, to tell the replica to use the MySQL server whose host name is rep-source with the replication account created in the previous step, use the following statement:

```
mysqlR> CHANGE MASTER TO
 -> MASTER_HOST='rep-source',
 -> MASTER_PORT=3306,
 -> MASTER_USER='myreplica',
 -> MASTER_PASSWORD='53cr37';
```

For a complete list of options that can be used with this statement, see Section 13.4.2.1, "CHANGE MASTER TO Statement".

To provide replication backup capability, you also need to add an --ndb-connectstring option to the replica's my.cnf file prior to starting the replication process. See [Section 21.7.9, "NDB](#page-128-0) [Cluster Backups With NDB Cluster Replication"](#page-128-0), for details.

For additional options that can be set in my.cnf for replicas, see Section 16.1.6, "Replication and Binary Logging Options and Variables".

4. If the source cluster is already in use, you can create a backup of the source and load this onto the replica to cut down on the amount of time required for the replica to synchronize itself with the source. If the replica is also running NDB Cluster, this can be accomplished using the backup and restore procedure described in [Section 21.7.9, "NDB Cluster Backups With NDB Cluster](#page-128-0) [Replication".](#page-128-0)

```
ndb-connectstring=management_host[:port]
```

In the event that you are not using NDB Cluster on the replica, you can create a backup with this command on the source:

```
shellS> mysqldump --master-data=1
```

Then import the resulting data dump onto the replica by copying the dump file over to it. After this, you can use the mysql client to import the data from the dumpfile into the replica database as shown here, where dump\_file is the name of the file that was generated using mysqldump on the source, and db\_name is the name of the database to be replicated:

```
shellR> mysql -u root -p db_name < dump_file
```

For a complete list of options to use with mysqldump, see Section 4.5.4, "mysqldump — A Database Backup Program".

![](_page_123_Picture_15.jpeg)

### **Note**

If you copy the data to the replica in this fashion, you should make sure that the replica is started with the --skip-slave-start option on the command line, or else include skip-slave-start in the replica's my.cnf file to keep it from trying to connect to the source to begin replicating before all the data has been loaded. Once the data loading has completed, follow the additional steps outlined in the next two sections.

5. Ensure that each MySQL server acting as a replication source is assigned a unique server ID, and has binary logging enabled, using the row-based format. (See Section 16.2.1, "Replication Formats".) In addition, we recommend enabling the slave\_allow\_batching system variable; beginning with NDB 7.6.23, a warning is issued if this variable is set to OFF. You should also consider increasing the values used with the --ndb-batch-size and --ndb-blob-writebatch-bytes options as well. All of these options can be set either in the source server's my.cnf file, or on the command line when starting the source mysqld process. See [Section 21.7.6,](#page-124-0) ["Starting NDB Cluster Replication \(Single Replication Channel\)"](#page-124-0), for more information.

# <span id="page-124-0"></span>**21.7.6 Starting NDB Cluster Replication (Single Replication Channel)**

This section outlines the procedure for starting NDB Cluster replication using a single replication channel.

1. Start the MySQL replication source server by issuing this command, where id is this server's unique ID (see [Section 21.7.2, "General Requirements for NDB Cluster Replication"\)](#page-107-0):

```
shellS> mysqld --ndbcluster --server-id=id \
 --log-bin --ndb-log-bin &
```

This starts the server's mysqld process with binary logging enabled using the proper logging format.

![](_page_124_Picture_7.jpeg)

### **Note**

You can also start the source with --binlog-format=MIXED, in which case row-based replication is used automatically when replicating between clusters. Statement-based binary logging is not supported for NDB Cluster Replication (see [Section 21.7.2, "General Requirements for NDB Cluster](#page-107-0) [Replication"\)](#page-107-0).

2. Start the MySQL replica server as shown here:

```
shellR> mysqld --ndbcluster --server-id=id &
```

In the command just shown, id is the replica server's unique ID. It is not necessary to enable logging on the replica.

![](_page_124_Picture_13.jpeg)

### **Note**

You should use the --skip-slave-start option with this command or else you should include skip-slave-start in the replica server's my.cnf file, unless you want replication to begin immediately. With the use of this option, the start of replication is delayed until the appropriate START SLAVE statement has been issued, as explained in Step 4 below.

3. It is necessary to synchronize the replica server with the source server's replication binary log. If binary logging has not previously been running on the source, run the following statement on the replica:

```
mysqlR> CHANGE MASTER TO
 -> MASTER_LOG_FILE='',
 -> MASTER_LOG_POS=4;
```

This instructs the replica to begin reading the source server's binary log from the log's starting point. Otherwise—that is, if you are loading data from the source using a backup—see [Section 21.7.8,](#page-126-0) ["Implementing Failover with NDB Cluster Replication"](#page-126-0), for information on how to obtain the correct values to use for MASTER\_LOG\_FILE and MASTER\_LOG\_POS in such cases.

4. Finally, instruct the replica to begin applying replication by issuing this command from the mysql client on the replica:

```
mysqlR> START SLAVE;
```

This also initiates the transmission of data and changes from the source to the replica.

It is also possible to use two replication channels, in a manner similar to the procedure described in the next section; the differences between this and using a single replication channel are covered in [Section 21.7.7, "Using Two Replication Channels for NDB Cluster Replication".](#page-125-0)

It is also possible to improve cluster replication performance by enabling batched updates. This can be accomplished by setting the slave\_allow\_batching system variable on the replicas' mysqld processes. Normally, updates are applied as soon as they are received. However, the use of batching causes updates to be applied in batches of 32 KB each; this can result in higher throughput and less CPU usage, particularly where individual updates are relatively small.

![](_page_125_Picture_3.jpeg)

### **Note**

Batching works on a per-epoch basis; updates belonging to more than one transaction can be sent as part of the same batch.

All outstanding updates are applied when the end of an epoch is reached, even if the updates total less than 32 KB.

Batching can be turned on and off at runtime. To activate it at runtime, you can use either of these two statements:

```
SET GLOBAL slave_allow_batching = 1;
SET GLOBAL slave_allow_batching = ON;
```

If a particular batch causes problems (such as a statement whose effects do not appear to be replicated correctly), batching can be deactivated using either of the following statements:

```
SET GLOBAL slave_allow_batching = 0;
SET GLOBAL slave_allow_batching = OFF;
```

You can check whether batching is currently being used by means of an appropriate SHOW VARIABLES statement, like this one:

```
mysql> SHOW VARIABLES LIKE 'slave%';
+---------------------------+-------+
| Variable_name | Value |
+---------------------------+-------+
| slave_allow_batching | ON |
| slave_compressed_protocol | OFF |
| slave_load_tmpdir | /tmp |
| slave_net_timeout | 3600 |
| slave_skip_errors | OFF |
| slave_transaction_retries | 10 |
+---------------------------+-------+
6 rows in set (0.00 sec)
```

# <span id="page-125-0"></span>**21.7.7 Using Two Replication Channels for NDB Cluster Replication**

In a more complete example scenario, we envision two replication channels to provide redundancy and thereby guard against possible failure of a single replication channel. This requires a total of four replication servers, two source servers on the source cluster and two replica servers on the replica cluster. For purposes of the discussion that follows, we assume that unique identifiers are assigned as shown here:

**Table 21.67 NDB Cluster replication servers described in the text**

| Server ID | Description                                 |
|-----------|---------------------------------------------|
| 1         | Source - primary replication channel (S)    |
| 2         | Source - secondary replication channel (S') |
| 3         | Replica - primary replication channel (R)   |

| Server ID | Description                                  |
|-----------|----------------------------------------------|
| 4         | replica - secondary replication channel (R') |

Setting up replication with two channels is not radically different from setting up a single replication channel. First, the mysqld processes for the primary and secondary replication source servers must be started, followed by those for the primary and secondary replicas. The replication processes can be initiated by issuing the START SLAVE statement on each of the replicas. The commands and the order in which they need to be issued are shown here:

1. Start the primary replication source:

```
shellS> mysqld --ndbcluster --server-id=1 \
 --log-bin &
```

2. Start the secondary replication source:

```
shellS'> mysqld --ndbcluster --server-id=2 \
 --log-bin &
```

3. Start the primary replica server:

```
shellR> mysqld --ndbcluster --server-id=3 \
 --skip-slave-start &
```

4. Start the secondary replica server:

```
shellR'> mysqld --ndbcluster --server-id=4 \
 --skip-slave-start &
```

5. Finally, initiate replication on the primary channel by executing the START SLAVE statement on the primary replica as shown here:

```
mysqlR> START SLAVE;
```

![](_page_126_Picture_13.jpeg)

### **Warning**

Only the primary channel must be started at this point. The secondary replication channel needs to be started only in the event that the primary replication channel fails, as described in [Section 21.7.8, "Implementing](#page-126-0) [Failover with NDB Cluster Replication"](#page-126-0). Running multiple replication channels simultaneously can result in unwanted duplicate records being created on the replicas.

As mentioned previously, it is not necessary to enable binary logging on the replicas.

# <span id="page-126-0"></span>**21.7.8 Implementing Failover with NDB Cluster Replication**

In the event that the primary Cluster replication process fails, it is possible to switch over to the secondary replication channel. The following procedure describes the steps required to accomplish this.

1. Obtain the time of the most recent global checkpoint (GCP). That is, you need to determine the most recent epoch from the ndb\_apply\_status table on the replica cluster, which can be found using the following query:

```
mysqlR'> SELECT @latest:=MAX(epoch)
 -> FROM mysql.ndb_apply_status;
```

In a circular replication topology, with a source and a replica running on each host, when you are using ndb\_log\_apply\_status=1, NDB Cluster epochs are written in the replicas' binary logs. This means that the ndb\_apply\_status table contains information for the replica on this host as well as for any other host which acts as a replica of the replication source server running on this host.

In this case, you need to determine the latest epoch on this replica to the exclusion of any epochs from any other replicas in this replica's binary log that were not listed in the IGNORE\_SERVER\_IDS options of the CHANGE MASTER TO statement used to set up this replica. The reason for excluding such epochs is that rows in the mysql.ndb\_apply\_status table whose server IDs have a match in the IGNORE\_SERVER\_IDS list from the CHANGE MASTER TO statement used to prepare this replicas's source are also considered to be from local servers, in addition to those having the replica's own server ID. You can retrieve this list as Replicate\_Ignore\_Server\_Ids from the output of SHOW SLAVE STATUS. We assume that you have obtained this list and are substituting it for ignore\_server\_ids in the query shown here, which like the previous version of the query, selects the greatest epoch into a variable named @latest:

```
mysqlR'> SELECT @latest:=MAX(epoch)
 -> FROM mysql.ndb_apply_status
 -> WHERE server_id NOT IN (ignore_server_ids);
```

In some cases, it may be simpler or more efficient (or both) to use a list of the server IDs to be included and server\_id IN server\_id\_list in the WHERE condition of the preceding query.

2. Using the information obtained from the query shown in Step 1, obtain the corresponding records from the ndb\_binlog\_index table on the source cluster.

You can use the following query to obtain the needed records from the ndb\_binlog\_index table on the source:

```
mysqlS'> SELECT
 -> @file:=SUBSTRING_INDEX(next_file, '/', -1),
 -> @pos:=next_position
 -> FROM mysql.ndb_binlog_index
 -> WHERE epoch = @latest;
```

These are the records saved on the source since the failure of the primary replication channel. We have employed a user variable @latest here to represent the value obtained in Step 1. Of course, it is not possible for one mysqld instance to access user variables set on another server instance directly. These values must be "plugged in" to the second query manually or by an application.

![](_page_127_Picture_8.jpeg)

### **Important**

You must ensure that the replica mysqld is started with --slave-skiperrors=ddl\_exist\_errors before executing START SLAVE. Otherwise, replication may stop with duplicate DDL errors.

3. Now it is possible to synchronize the secondary channel by running the following query on the secondary replica server:

```
mysqlR'> CHANGE MASTER TO
 -> MASTER_LOG_FILE='@file',
 -> MASTER_LOG_POS=@pos;
```

Again we have employed user variables (in this case @file and @pos) to represent the values obtained in Step 2 and applied in Step 3; in practice these values must be inserted manually or using an application that can access both of the servers involved.

![](_page_127_Picture_14.jpeg)

# **Note**

@file is a string value such as '/var/log/mysql/replicationsource-bin.00001', and so must be quoted when used in SQL or application code. However, the value represented by @pos must not be quoted. Although MySQL normally attempts to convert strings to numbers, this case is an exception.

4. You can now initiate replication on the secondary channel by issuing the appropriate statement on the secondary replica mysqld:

```
mysqlR'> START SLAVE;
```

Once the secondary replication channel is active, you can investigate the failure of the primary and effect repairs. The precise actions required to do this depend upon the reasons for which the primary channel failed.

![](_page_128_Picture_3.jpeg)

### **Warning**

The secondary replication channel is to be started only if and when the primary replication channel has failed. Running multiple replication channels simultaneously can result in unwanted duplicate records being created on the replicas.

If the failure is limited to a single server, it should in theory be possible to replicate from S to R', or from S' to R.

# <span id="page-128-0"></span>**21.7.9 NDB Cluster Backups With NDB Cluster Replication**

This section discusses making backups and restoring from them using NDB Cluster replication. We assume that the replication servers have already been configured as covered previously (see [Section 21.7.5, "Preparing the NDB Cluster for Replication"](#page-122-0), and the sections immediately following). This having been done, the procedure for making a backup and then restoring from it is as follows:

- 1. There are two different methods by which the backup may be started.
  - **Method A.** This method requires that the cluster backup process was previously enabled on the source server, prior to starting the replication process. This can be done by including the following line in a [mysql\_cluster] section in the my.cnf file, where management\_host is the IP address or host name of the NDB management server for the source cluster, and port is the management server's port number:

ndb-connectstring=management\_host[:port]

![](_page_128_Picture_12.jpeg)

### **Note**

The port number needs to be specified only if the default port (1186) is not being used. See Section 21.3.3, "Initial Configuration of NDB Cluster", for more information about ports and port allocation in NDB Cluster.

In this case, the backup can be started by executing this statement on the replication source:

```
shellS> ndb_mgm -e "START BACKUP"
```

• **Method B.** If the my.cnf file does not specify where to find the management host, you can start the backup process by passing this information to the NDB management client as part of the START BACKUP command. This can be done as shown here, where management\_host and port are the host name and port number of the management server:

```
shellS> ndb_mgm management_host:port -e "START BACKUP"
```

In our scenario as outlined earlier (see [Section 21.7.5, "Preparing the NDB Cluster for](#page-122-0) [Replication"\)](#page-122-0), this would be executed as follows:

```
shellS> ndb_mgm rep-source:1186 -e "START BACKUP"
```

2. Copy the cluster backup files to the replica that is being brought on line. Each system running an ndbd process for the source cluster has cluster backup files located on it, and all of these files must be copied to the replica to ensure a successful restore. The backup files can be copied into any directory on the computer where the replica's management host resides, as long as the MySQL and NDB binaries have read permissions in that directory. In this case, we assume that these files have been copied into the directory /var/BACKUPS/BACKUP-1.

While it is not necessary that the replica cluster have the same number of ndbd processes (data nodes) as the source, it is highly recommended this number be the same. It is necessary that the replica be started with the --skip-slave-start option, to prevent premature startup of the replication process.

3. Create any databases on the replica cluster that are present on the source cluster and that are to be replicated.

![](_page_129_Picture_3.jpeg)

### **Important**

A CREATE DATABASE (or CREATE SCHEMA) statement corresponding to each database to be replicated must be executed on each SQL node in the replica cluster.

4. Reset the replica cluster using this statement in the mysql client:

```
mysqlR> RESET SLAVE;
```

5. You can now start the cluster restoration process on the replica using the ndb\_restore command for each backup file in turn. For the first of these, it is necessary to include the -m option to restore the cluster metadata, as shown here:

```
shellR> ndb_restore -c replica_host:port -n node-id \
 -b backup-id -m -r dir
```

dir is the path to the directory where the backup files have been placed on the replica. For the ndb\_restore commands corresponding to the remaining backup files, the -m option should not be used.

For restoring from a source cluster with four data nodes (as shown in the figure in [Section 21.7,](#page-105-0) ["NDB Cluster Replication"](#page-105-0)) where the backup files have been copied to the directory /var/ BACKUPS/BACKUP-1, the proper sequence of commands to be executed on the replica might look like this:

```
shellR> ndb_restore -c replica-host:1186 -n 2 -b 1 -m \
 -r ./var/BACKUPS/BACKUP-1
shellR> ndb_restore -c replica-host:1186 -n 3 -b 1 \
 -r ./var/BACKUPS/BACKUP-1
shellR> ndb_restore -c replica-host:1186 -n 4 -b 1 \
 -r ./var/BACKUPS/BACKUP-1
shellR> ndb_restore -c replica-host:1186 -n 5 -b 1 -e \
 -r ./var/BACKUPS/BACKUP-1
```

![](_page_129_Picture_13.jpeg)

### **Important**

The -e (or --restore-epoch) option in the final invocation of ndb\_restore in this example is required to make sure that the epoch is written to the replica's mysql.ndb\_apply\_status table. Without this information, the replica cannot synchronize properly with the source. (See Section 21.5.24, "ndb\_restore — Restore an NDB Cluster Backup".)

6. Now you need to obtain the most recent epoch from the ndb\_apply\_status table on the replica (as discussed in [Section 21.7.8, "Implementing Failover with NDB Cluster Replication"](#page-126-0)):

```
mysqlR> SELECT @latest:=MAX(epoch)
 FROM mysql.ndb_apply_status;
```

7. Using @latest as the epoch value obtained in the previous step, you can obtain the correct starting position @pos in the correct binary log file @file from the mysql.ndb\_binlog\_index table on the source. The query shown here gets these from the next\_position and next\_file columns from the last epoch applied before the logical restore position:

```
mysqlS> SELECT
```

```
 -> @file:=SUBSTRING_INDEX(next_file, '/', -1),
 -> @pos:=next_position
 -> FROM mysql.ndb_binlog_index
 -> WHERE epoch > @latest
 -> ORDER BY epoch ASC LIMIT 1;
```

In the event that there is currently no replication traffic, you can get similar information by running SHOW MASTER STATUS on the source and using the value shown in the Position column of the output for the file whose name has the suffix with the greatest value for all files shown in the File column. In this case, you must determine which file this is and supply the name in the next step manually or by parsing the output with a script.

8. Using the values obtained in the previous step, you can now issue the appropriate CHANGE MASTER TO statement in the replica's mysql client:

```
mysqlR> CHANGE MASTER TO
 -> MASTER_LOG_FILE='@file',
 -> MASTER_LOG_POS=@pos;
```

9. Now that the replica knows from what point in which binary log file to start reading data from the source, you can cause the replica to begin replicating with this statement:

```
mysqlR> START SLAVE;
```

To perform a backup and restore on a second replication channel, it is necessary only to repeat these steps, substituting the host names and IDs of the secondary source and replica for those of the primary source and replica servers where appropriate, and running the preceding statements on them.

For additional information on performing Cluster backups and restoring Cluster from backups, see Section 21.6.8, "Online Backup of NDB Cluster".