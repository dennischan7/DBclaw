---
source: MySQL 8.0 Reference
title: 00_Overview
---

Views are always replicated to replicas. Views are filtered by their own name, not by the tables they refer to. This means that a view can be replicated to the replica even if the view contains a table that would normally be filtered out by replication-ignore-table rules. Care should therefore

be taken to ensure that views do not replicate table data that would normally be filtered for security reasons.

Replication from a table to a same-named view is supported using statement-based logging, but not when using row-based logging. Trying to do so when row-based logging is in effect causes an error.

# <span id="page-76-0"></span>**19.5.2 Replication Compatibility Between MySQL Versions**

MySQL supports replication from one release series to the next higher release series. For example, you can replicate from a source running MySQL 5.6 to a replica running MySQL 5.7, from a source running MySQL 5.7 to a replica running MySQL 8.0, and so on. However, you might encounter difficulties when replicating from an older source to a newer replica if the source uses statements or relies on behavior no longer supported in the version of MySQL used on the replica. For example, foreign key names longer than 64 characters are no longer supported from MySQL 8.0.

The use of more than two MySQL Server versions is not supported in replication setups involving multiple sources, regardless of the number of source or replica MySQL servers. This restriction applies not only to release series, but to version numbers within the same release series as well. For example, if you are using a chained or circular replication setup, you cannot use MySQL 8.0.22, MySQL 8.0.24, and MySQL 8.0.28 concurrently, although you could use any two of these releases together.

![](_page_76_Picture_6.jpeg)

#### **Important**

It is strongly recommended to use the most recent release available within a given MySQL release series because replication (and other) capabilities are continually being improved. It is also recommended to upgrade sources and replicas that use early releases of a release series of MySQL to GA (production) releases when the latter become available for that release series.

From MySQL 8.0.14, the server version is recorded in the binary log for each transaction for the server that originally committed the transaction (original\_server\_version), and for the server that is the immediate source of the current server in the replication topology (immediate\_server\_version).

Replication from newer sources to older replicas might be possible, but is generally not supported. This is due to a number of factors:

• **Binary log format changes.** The binary log format can change between major releases. While we attempt to maintain backward compatibility, this is not always possible. A source might also have optional features enabled that are not understood by older replicas, such as binary log transaction compression, where the resulting compressed transaction payloads cannot be read by a replica at a release before MySQL 8.0.20.

This also has significant implications for upgrading replication servers; see [Section 19.5.3,](#page-77-0) ["Upgrading a Replication Topology"](#page-77-0), for more information.

- For more information about row-based replication, see Section 19.2.1, "Replication Formats".
- **SQL incompatibilities.** You cannot replicate from a newer source to an older replica using statement-based replication if the statements to be replicated use SQL features available on the source but not on the replica.

However, if both the source and the replica support row-based replication, and there are no data definition statements to be replicated that depend on SQL features found on the source but not on the replica, you can use row-based replication to replicate the effects of data modification statements even if the DDL run on the source is not supported on the replica.

In MySQL 8.0.26, incompatible changes were made to replication instrumentation names, including the names of thread stages, containing the terms "master", which is changed to "source", "slave", which is changed to "replica", and "mts" (for "multithreaded slave"), which is changed to "mta" (for "multithreaded applier"). Monitoring tools that work with these instrumentation names might be

impacted. If the incompatible changes have an impact for you, set the terminology\_use\_previous system variable to BEFORE\_8\_0\_26 to make MySQL Server use the old versions of the names for the objects specified in the previous list. This enables monitoring tools that rely on the old names to continue working until they can be updated to use the new names.

For more information on potential replication issues, see [Section 19.5.1, "Replication Features and](#page-49-0) [Issues"](#page-49-0).

# <span id="page-77-0"></span>**19.5.3 Upgrading a Replication Topology**

When you upgrade servers that participate in a replication topology, you need to take into account each server's role in the topology and look out for issues specific to replication. For general information and instructions for upgrading a MySQL Server instance, see Chapter 3, Upgrading MySQL.

As explained in [Section 19.5.2, "Replication Compatibility Between MySQL Versions",](#page-76-0) MySQL supports replication from a source running one release series to a replica running the next higher release series, but does not support replication from a source running a later release to a replica running an earlier release. A replica at an earlier release might not have the required capability to process transactions that can be handled by the source at a later release. You must therefore upgrade all of the replicas in a replication topology to the target MySQL Server release, before you upgrade the source server to the target release. In this way you will never be in the situation where a replica still at the earlier release is attempting to handle transactions from a source at the later release.

In a replication topology where there are multiple sources (multi-source replication), the use of more than two MySQL Server versions is not supported, regardless of the number of source or replica MySQL servers. This restriction applies not only to release series, but to version numbers within the same release series as well. For example, you cannot use MySQL 8.0.22, MySQL 8.0.24, and MySQL 8.0.28 concurrently in such a setup, although you could use any two of these releases together.

If you need to downgrade the servers in a replication topology, the source must be downgraded before the replicas are downgraded. On the replicas, you must ensure that the binary log and relay log have been fully processed, and remove them before proceeding with the downgrade.

# **Behavior Changes Between Releases**

Although this upgrade sequence is correct, it is possible to still encounter replication difficulties when replicating from a source at an earlier release that has not yet been upgraded, to a replica at a later release that has been upgraded. This can happen if the source uses statements or relies on behavior that is no longer supported in the later release installed on the replica. You can use MySQL Shell's upgrade checker utility util.checkForServerUpgrade() to check MySQL 5.7 server instances or MySQL 8.0 server instances for upgrade to a GA MySQL 8.0 release. The utility identifies anything that needs to be fixed for that server instance so that it does not cause an issue after the upgrade, including features and behaviors that are no longer available in the later release. See [Upgrade Checker Utility](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-utilities-upgrade.md) for information on the upgrade checker utility.

If you are upgrading an existing replication setup from a version of MySQL that does not support global transaction identifiers (GTIDs) to a version that does, only enable GTIDs on the source and the replicas when you have made sure that the setup meets all the requirements for GTID-based replication. See Section 19.1.3.4, "Setting Up Replication Using GTIDs" for information about converting binary log file position based replication setups to use GTID-based replication.

Changes affecting operations in strict SQL mode (STRICT\_TRANS\_TABLES or STRICT\_ALL\_TABLES) may result in replication failure on an upgraded replica. If you use statement-based logging (binlog\_format=STATEMENT), if a replica is upgraded before the source, the source executes statements which succeed there but which may fail on the replica and so cause replication to stop. To deal with this, stop all new statements on the source and wait until the replicas catch up, then upgrade the replicas. Alternatively, if you cannot stop new statements, temporarily change to rowbased logging on the source (binlog\_format=ROW) and wait until all replicas have processed all binary logs produced up to the point of this change, then upgrade the replicas.

The default character set has changed from latin1 to utf8mb4 in MySQL 8.0. In a replicated setting, when upgrading from MySQL 5.7 to 8.0, it is advisable to change the default character set back to the character set used in MySQL 5.7 before upgrading. After the upgrade is completed, the default character set can be changed to utf8mb4. Assuming that the previous defaults were used, one way to preserve them is to start the server with these lines in the my.cnf file:

```
[mysqld]
character_set_server=latin1
collation_server=latin1_swedish_ci
```

# **Standard Upgrade Procedure**

To upgrade a replication topology, follow the instructions in Chapter 3, Upgrading MySQL for each individual MySQL Server instance, using this overall procedure:

- 1. Upgrade the replicas first. On each replica instance:
  - Carry out the preliminary checks and steps described in Section 3.6, "Preparing Your Installation for Upgrade".
  - Shut down MySQL Server.
  - Upgrade the MySQL Server binaries or packages.
  - Restart MySQL Server.
  - If you have upgraded to a release earlier than MySQL 8.0.16, invoke mysql\_upgrade manually to upgrade the system tables and schemas. When the server is running with global transaction identifiers (GTIDs) enabled (gtid\_mode=ON), do not enable binary logging by mysql\_upgrade (so do not use the --write-binlog option). Then shut down and restart the server.
  - If you have upgraded to MySQL 8.0.16 or later, do not invoke mysql\_upgrade. From that release, MySQL Server performs the entire MySQL upgrade procedure, disabling binary logging during the upgrade.
  - Restart replication using a START REPLICA or START SLAVE statement.
- 2. When all the replicas have been upgraded, follow the same steps to upgrade and restart the source server, with the exception of the START REPLICA or START SLAVE statement. If you made a temporary change to row-based logging or to the default character set, you can revert the change now.

# **Upgrade Procedure With Table Repair Or Rebuild**

Some upgrades may require that you drop and re-create database objects when you move from one MySQL series to the next. For example, collation changes might require that table indexes be rebuilt. Such operations, if necessary, are detailed at Section 3.5, "Changes in MySQL 8.0". It is safest to perform these operations separately on the replicas and the source, and to disable replication of these operations from the source to the replica. To achieve this, use the following procedure:

- 1. Stop all the replicas and upgrade the binaries or packages. Restart them with the --skip-slavestart option, or from MySQL 8.0.24, the skip\_slave\_start system variable, so that they do not connect to the source. Perform any table repair or rebuilding operations needed to re-create database objects, such as use of REPAIR TABLE or ALTER TABLE, or dumping and reloading tables or triggers.
- 2. Disable the binary log on the source. To do this without restarting the source, execute a SET sql\_log\_bin = OFF statement. Alternatively, stop the source and restart it with the --skiplog-bin option. If you restart the source, you might also want to disallow client connections. For example, if all clients connect using TCP/IP, enable the skip\_networking system variable when you restart the source.

- 3. With the binary log disabled, perform any table repair or rebuilding operations needed to re-create database objects. The binary log must be disabled during this step to prevent these operations from being logged and sent to the replicas later.
- 4. Re-enable the binary log on the source. If you set sql\_log\_bin to OFF earlier, execute a SET sql\_log\_bin = ON statement. If you restarted the source to disable the binary log, restart it without --skip-log-bin, and without enabling the skip\_networking system variable so that clients and replicas can connect.
- 5. Restart the replicas, this time without the --skip-slave-start option or skip\_slave\_start system variable.