---
source: MySQL 8.0 Reference
title: 00_Overview
---

When upgrading an online group you should consider the following points:

- Regardless of the way which you upgrade your group, it is important to disable any writes to group members until they are ready to rejoin the group.
- When a member is stopped, the super\_read\_only variable is set to on automatically, but this change is not persisted.
- When MySQL 5.7.22 or MySQL 8.0.11 tries to join a group running MySQL 5.7.21 or lower it fails to join the group because MySQL 5.7.21 does not send its value of lower\_case\_table\_names.

# <span id="page-199-1"></span>**20.8.3.2 Upgrading a Group Replication Member**

This section explains the steps required for upgrading a member of a group. This procedure is part of the methods described at Section 20.8.3.3, "Group Replication Online Upgrade Methods". The process of upgrading a member of a group is common to all methods and is explained first. The way which you join upgraded members can depend on which method you are following, and other factors such as whether the group is operating in single-primary or multi-primary mode. How you upgrade the server instance, using either the in-place or provision approach, does not impact on the methods described here.

The process of upgrading a member consists of removing it from the group, following your chosen method of upgrading the member, and then rejoining the upgraded member to a group. The recommended order of upgrading members in a single-primary group is to upgrade all secondaries, and then upgrade the primary last. If the primary is upgraded before a secondary, a new primary using the older MySQL version is chosen, but there is no need for this step.

To upgrade a member of a group:

- Connect a client to the group member and issue STOP GROUP\_REPLICATION. Before proceeding, ensure that the member's status is OFFLINE by monitoring the replication\_group\_members table.
- Disable Group Replication from starting up automatically so that you can safely connect to the member after upgrading and configure it without it rejoining the group by setting group\_replication\_start\_on\_boot=0.

![](_page_199_Picture_16.jpeg)

#### **Important**

If an upgraded member has group\_replication\_start\_on\_boot=1 then it could rejoin the group before you can perform the MySQL upgrade procedure and could result in issues. For example, if the upgrade fails and the server restarts again, then a possibly broken server could try to join the group.

- Stop the member, for example using mysqladmin shutdown or the SHUTDOWN statement. Any other members in the group continue running.
- Upgrade the member, using the in-place or provisioning approach. See Chapter 3, Upgrading MySQL for details. When restarting the upgraded member, because [group\\_replication\\_start\\_on\\_boot](#page-43-0) is set to 0, Group Replication does not start on the instance, and therefore it does not rejoin the group.
- Once the MySQL upgrade procedure has been performed on the member, [group\\_replication\\_start\\_on\\_boot](#page-43-0) must be set to 1 to ensure Group Replication starts correctly after restart. Restart the member.
- Connect to the upgraded member and issue START GROUP\_REPLICATION. This rejoins the member to the group. The Group Replication metadata is in place on the upgraded server, therefore there is usually no need to reconfigure Group Replication. The server has to catch up with any transactions processed by the group while the server was offline. Once it has caught up with the group, it becomes an online member of the group.

![](_page_0_Picture_5.jpeg)

#### **Note**

The longer it takes to upgrade a server, the more time that member is offline and therefore the more time it takes for the server to catch up when added back to the group.

When an upgraded member joins a group which has any member running an earlier MySQL Server version, the upgraded member joins with super\_read\_only=on. This ensures that no writes are made to upgraded members until all members are running the newer version. In a multi-primary mode group, when the upgrade has been completed successfully and the group is ready to process transactions, members that are intended as writeable primaries must be set to read-write mode. As of MySQL 8.0.17, when all members of a group have been upgraded to the same release, they all change back to read-write mode automatically. For earlier releases you must set each member manually to read-write mode. Connect to each member and issue:

**SET GLOBAL super\_read\_only=OFF;**

## <span id="page-0-0"></span>**20.8.3.3 Group Replication Online Upgrade Methods**

Choose one of the following methods of upgrading a Group Replication group:

#### **Rolling In-Group Upgrade**

This method is supported provided that servers running a newer version are not generating workload to the group while there are still servers with an older version in it. In other words servers with a newer version can join the group only as secondaries. In this method there is only ever one group, and each server instance is removed from the group, upgraded and then rejoined to the group.

This method is well suited to single-primary groups. When the group is operating in single-primary mode, if you require the primary to remain the same throughout (except when it is being upgraded itself), it should be the last member to be upgraded. The primary cannot remain as the primary unless it is running the lowest MySQL Server version in the group. After the primary has been upgraded, you can use the group\_replication\_set\_as\_primary() function to reappoint it as the primary. If you do not mind which member is the primary, the members can be upgraded in any order. The group elects a new primary whenever necessary from among the members running the lowest MySQL Server version, following the election policies described in Section 20.1.3.1, "Single-Primary Mode".

For groups operating in multi-primary mode, during a rolling in-group upgrade the number of primaries is decreased, causing a reduction in write availability. This is because if a member joins a group when it is running a higher MySQL Server version than the lowest version that the existing group members are running, it automatically remains in read-only mode (super\_read\_only=ON). Note that members running MySQL 8.0.17 or higher take into account the patch version of the release when checking this, but members running MySQL 8.0.16 or lower, or MySQL 5.7, only take into account the major version. When all members have been upgraded to the same release, from MySQL 8.0.17, they all change back to read-write mode automatically. For earlier releases, you must set super\_read\_only=OFF manually on each member that should function as a primary following the upgrade.

For full information on version compatibility in a group and how this influences the behavior of a group during an upgrade process, see Section 20.8.1, "Combining Different Member Versions in a Group" .

### **Rolling Migration Upgrade**

In this method you remove members from the group, upgrade them and then create a second group using the upgraded members. For groups operating in multi-primary mode, during this process the number of primaries is decreased, causing a reduction in write availability. This does not impact groups operating in single-primary mode.

Because the group running the older version is online while you are upgrading the members, you need the group running the newer version to catch up with any transactions executed while the members were being upgraded. Therefore one of the servers in the new group is configured as a replica of a primary from the older group. This ensures that the new group catches up with the older group. Because this method relies on an asynchronous replication channel which is used to replicate data from one group to another, it is supported under the same assumptions and requirements of asynchronous source-replica replication, see Chapter 19, Replication. For groups operating in singleprimary mode, the asynchronous replication connection to the old group must send data to the primary in the new group, for a multi-primary group the asynchronous replication channel can connect to any primary.

#### The process is to:

- remove members from the original group running the older server version one by one, see Section 20.8.3.2, "Upgrading a Group Replication Member"
- upgrade the server version running on the member, see Chapter 3, Upgrading MySQL. You can either follow an in-place or provision approach to upgrading.
- create a new group with the upgraded members, see Chapter 20, Group Replication. In this case you need to configure a new group name on each member (because the old group is still running and using the old name), bootstrap an initial upgraded member, and then add the remaining upgraded members.
- set up an asynchronous replication channel between the old group and the new group, see Section 19.1.3.4, "Setting Up Replication Using GTIDs". Configure the older primary to function as the asynchronous replication source server and the new group member as a GTID-based replica.

Before you can redirect your application to the new group, you must ensure that the new group has a suitable number of members, for example so that the group can handle the failure of a member. Issue SELECT \* FROM performance\_schema.replication\_group\_members and compare the initial group size and the new group size. Wait until all data from the old group is propagated to the new group and then drop the asynchronous replication connection and upgrade any missing members.

### **Rolling Duplication Upgrade**

In this method you create a second group consisting of members which are running the newer version, and the data missing from the older group is replicated to the newer group. This assumes that you have enough servers to run both groups simultaneously. Due to the fact that during this process the number of primaries is not decreased, for groups operating in multi-primary mode there is no reduction in write availability. This makes rolling duplication upgrade well suited to groups operating in multiprimary mode. This does not impact groups operating in single-primary mode.

Because the group running the older version is online while you are provisioning the members in the new group, you need the group running the newer version to catch up with any transactions executed while the members were being provisioned. Therefore one of the servers in the new group is configured as a replica of a primary from the older group. This ensures that the new group catches up with the older group. Because this method relies on an asynchronous replication channel which is used to replicate data from one group to another, it is supported under the same assumptions and requirements of asynchronous source-replica replication, see Chapter 19, Replication. For groups operating in single-primary mode, the asynchronous replication connection to the old group must send data to the primary in the new group, for a multi-primary group the asynchronous replication channel can connect to any primary.

The process is to:

- deploy a suitable number of members so that the group running the newer version can handle failure of a member
- take a backup of the existing data from a member of the group
- use the backup from the older member to provision the members of the new group, see [Section 20.8.3.4, "Group Replication Upgrade with mysqlbackup"](#page-2-0) for one method.

![](_page_2_Picture_6.jpeg)

#### **Note**

You must restore the backup to the same version of MySQL which the backup was taken from, and then perform an in-place upgrade. For instructions, see Chapter 3, Upgrading MySQL.

- create a new group with the upgraded members, see Chapter 20, Group Replication. In this case you need to configure a new group name on each member (because the old group is still running and using the old name), bootstrap an initial upgraded member, and then add the remaining upgraded members.
- set up an asynchronous replication channel between the old group and the new group, see Section 19.1.3.4, "Setting Up Replication Using GTIDs". Configure the older primary to function as the asynchronous replication source server and the new group member as a GTID-based replica.

Once the ongoing data missing from the newer group is small enough to be quickly transferred, you must redirect write operations to the new group. Wait until all data from the old group is propagated to the new group and then drop the asynchronous replication connection.

## <span id="page-2-0"></span>**20.8.3.4 Group Replication Upgrade with mysqlbackup**

As part of a provisioning approach you can use MySQL Enterprise Backup to copy and restore the data from a group member to new members. However you cannot use this technique to directly restore a backup taken from a member running an older version of MySQL to a member running a newer version of MySQL. The solution is to restore the backup to a new server instance which is running the same version of MySQL as the member which the backup was taken from, and then upgrade the instance. This process consists of:

- Take a backup from a member of the older group using mysqlbackup. See Section 20.5.6, "Using MySQL Enterprise Backup with Group Replication".
- Deploy a new server instance, which must be running the same version of MySQL as the older member where the backup was taken.
- Restore the backup from the older member to the new instance using mysqlbackup.
- Upgrade MySQL on the new instance, see Chapter 3, Upgrading MySQL.

Repeat this process to create a suitable number of new instances, for example to be able to handle a failover. Then join the instances to a group based on the [Section 20.8.3.3, "Group Replication Online](#page-0-0) [Upgrade Methods".](#page-0-0)`