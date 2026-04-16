---
source: MySQL 8.4 Reference
title: 00_Overview
---

Views are always replicated to replicas. Views are filtered by their own name, not by the tables they refer to. This means that a view can be replicated to the replica even if the view contains a table that would normally be filtered out by replication-ignore-table rules. Care should therefore be taken to ensure that views do not replicate table data that would normally be filtered for security reasons.

Replication from a table to a same-named view is supported using statement-based logging, but not when using row-based logging. Trying to do so when row-based logging is in effect causes an error.

# <span id="page-3-0"></span>**19.5.2 Replication Compatibility Between MySQL Versions**

MySQL supports replication from an older source to a newer replica for version combinations where we support upgrades from the source version to the replica version as described at Section 1.3, "MySQL Releases: Innovation and LTS" and Section 3.2, "Upgrade Paths". However, you might encounter difficulties when replicating from an older source to a newer replica if the source uses statements or relies on behavior no longer supported in the version of MySQL used on the replica.

The use of more than two MySQL Server versions is not supported in replication setups involving multiple sources, regardless of the number of source or replica MySQL servers. For example, if you are using a chained or circular replication setup, you cannot use MySQL X.Y.1, MySQL X.Y.2, and MySQL X.Y.3 concurrently, although you could use any two of these releases together.

![](_page_3_Picture_8.jpeg)

#### **Important**

It is strongly recommended to use the most recent release available within a given MySQL release series because replication (and other) capabilities are continually being improved. It is also recommended to upgrade sources and replicas that use early releases of a release series of MySQL to GA (production) releases when the latter become available for that release series.

The server version is recorded in the binary log for each transaction for the server that originally committed the transaction (original\_server\_version), and for the server that is the immediate source of the current server in the replication topology (immediate\_server\_version).

Replication from newer sources to older replicas might be possible, but is generally not supported. This is due to a number of factors:

• **Binary log format changes.** The binary log format can change between major releases. While we attempt to maintain backward compatibility, this is not always possible. A source might also have optional features enabled that are not understood by older replicas, such as binary log transaction compression, where the resulting compressed transaction payloads cannot be read by a replica from a release prior to MySQL 8.0.20.

This also has significant implications for upgrading replication servers; see [Section 19.5.3,](#page-4-0) ["Upgrading or Downgrading a Replication Topology",](#page-4-0) for more information.

• **SQL incompatibilities.** You cannot replicate from a newer source to an older replica using statement-based replication if the statements to be replicated use SQL features available on the source but not on the replica.

However, if both the source and the replica support row-based replication, and there are no data definition statements to be replicated that depend on SQL features found on the source but not on the replica, you can use row-based replication to replicate the effects of data modification statements even if the DDL run on the source is not supported on the replica.

For more information about row-based replication, see Section 19.2.1, "Replication Formats".

For more information on potential replication issues, see Section 19.5.1, "Replication Features and Issues".

# <span id="page-4-0"></span>**19.5.3 Upgrading or Downgrading a Replication Topology**

When you upgrade servers that participate in a replication topology, you need to take into account each server's role in the topology and look out for issues specific to replication. For general information and instructions for upgrading a MySQL Server instance, see Chapter 3, Upgrading MySQL.

As explained in [Section 19.5.2, "Replication Compatibility Between MySQL Versions",](#page-3-0) MySQL supports replication from an older source to a newer replica for version combinations where we support upgrades from the source version to the replica version as described at Section 1.3, "MySQL Releases: Innovation and LTS" and Section 3.2, "Upgrade Paths", but does not support replication from a source running a later release to a replica running an earlier release. A replica at an earlier release might not have the required capability to process transactions that can be handled by the source at a later release. You must therefore upgrade all of the replicas in a replication topology to the target MySQL Server release, before you upgrade the source server to the target release. In this way you will never be in the situation where a replica still at the earlier release is attempting to handle transactions from a source at the later release.

In a replication topology where there are multiple sources (multi-source replication), the use of more than two MySQL Server versions is not supported, regardless of the number of source or replica MySQL servers. For example, you cannot use MySQL X.Y.1, MySQL X.Y.2, and MySQL X.Y.3 concurrently in such a setup, although you could use any two of these releases together.

## **Pre-Check Servers before Upgrade**

It is possible to encounter replication difficulties when replicating from a source at an earlier release that has not yet been upgraded, to a replica at a later release that has been upgraded. This can happen if the source uses statements or relies on behavior that is no longer supported in the later release installed on the replica. You can use the MySQL Shell upgrade checker utility util.checkForServerUpgrade() to check MySQL 8.0 server instances for upgrade to a MySQL 8.4 release. This utility identifies configuration and stored data that is known to potentially cause upgrade problems, including features and behaviors that are no longer available in the later release. See [Upgrade Checker Utility](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-upgrade.md) for information on the upgrade checker utility.

# **Standard Upgrade Procedure**

To upgrade a replication topology, follow the instructions in Chapter 3, Upgrading MySQL for each individual MySQL Server instance, using this overall procedure:

- 1. Upgrade the replicas first. On each replica instance:
  - Carry out the preliminary checks and steps described in Section 3.6, "Preparing Your Installation for Upgrade".
  - Shut down MySQL Server.
  - Upgrade the MySQL Server binaries or packages.
  - Restart MySQL Server.
  - MySQL Server performs the entire MySQL upgrade procedure automatically, disabling binary logging during the upgrade.
  - Restart replication using a START REPLICA.
- 2. If there are multiple layers of replicas (replicas-of-replicas) start upgrading the replicas that are farthest away from the source, performing the upgrade in a bottom-up fashion.

3. When all replicas have upgraded and only the source remains, perform a switch-over to one of the replicas. In other words, stop client updates on the source, wait for at least one replica to apply all changes, reconfigure the replication topology so that replica becomes the source and that the source is left outside the replication topology. Upgrade the old source according to the procedure for a single server, and then reinsert it into the topology.

If you need to downgrade the servers in a replication topology, the source must be downgraded before the replicas are downgraded. On the replicas, you must ensure that the binary log and relay log have been fully processed, and purge them before proceeding with the downgrade.

### **Rolling Downgrade Procedure**

- 1. Stop the updates.
- 2. Wait for replicas to receive all updates. It is not necessary to wait for them to apply all changes. If they have not applied all changes, leave their applier running so they can process the received transactions in the background.
- 3. Downgrade the source server, following the instructions for single server downgrade.
- 4. Insert the downgraded source server in the topology again.
- 5. Allow updates again.
- 6. Wait until all replicas have applied all remaining transactions from the previous primary.
- 7. For each replica, take out the replica from the topology, wait for it to apply all its relay log, downgrade it following the instructions for a single server downgrade, and reinsert it back into the topology. If there are multiple levels of replicas (replicas-of-replicas) then downgrade top-down starting with the replicas nearest to the source server.