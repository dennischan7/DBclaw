---
source: MySQL 8.0 Reference
title: 00_Overview
---

From MySQL 8.0.26, Group Replication has the capability to set actions for the members of a group to take in specified situations. Member actions can be enabled and disabled individually using functions. The member actions configuration for a server can also be reset to the default after it has left the group.

Administrators (with the GROUP\_REPLICATION\_ADMIN privilege) can configure a member action on the group's primary using the group\_replication\_enable\_member\_action or group\_replication\_disable\_member\_action function. The member actions configuration, consisting of all the member actions and whether they are enabled or disabled, is then propagated to other group members and joining members using Group Replication's group messages. All group members therefore have the same member actions configuration. You can also configure member actions on a server that is not part of a group, as long as the Group Replication plugin is installed. In that case, the member actions configuration is not propagated to any other servers.

If the server where you use the functions to configure a member action is part of a group, it must be the current primary in a group in single-primary mode, and it must be part of the majority. The configuration change is tracked internally by Group Replication, but it is not given a GTID and is not written to the binary log, so it is not propagated to any servers outside the group, such as downstream replicas. Group Replication increments the version number for its member actions configuration each time a member action is enabled or disabled.

The member actions configuration is propagated to members as follows:

- When starting a group, the member actions configuration of the server that bootstraps the group becomes the configuration for the group.
- If a group's lowest MySQL Server version supports member actions, joining members receive the group's member actions configuration during the state exchange process that takes place when they join. In that case, the joining member replaces its own member actions configuration with the group's.

• If a joining member that supports member actions joins a group where the lowest MySQL Server version does not support member actions, it does not receive a member actions configuration when it joins. In that case, the joining member resets its own configuration to the default.

A member that does not support member actions cannot join a group that has a member actions configuration, because its MySQL Server version is lower than the lowest version that the existing group members are running.

The Performance Schema table replication\_group\_member\_actions lists the member actions that are available in the configuration, the events that trigger them, and whether or not they are currently enabled. Member actions have a priority from 1 to 100, with lower values being actioned first. If an error occurs when the member action is being carried out, the failure of the member action can be logged but otherwise ignored. If the failure of the member action is considered critical, it can be handled according to the policy specified by the group\_replication\_exit\_state\_action system variable.

The mysql.replication\_group\_configuration\_version table, which can be viewed using the Performance Schema table replication\_group\_configuration\_version, records the current version of the member actions configuration. Whenever a member action is enabled or disabled using the functions, the version number is incremented.

The group\_replication\_reset\_member\_actions function can only be used on a server that is not part of a group. It resets the member actions configuration to the default settings, and resets its version number to 1. The server must be writeable (with the read\_only system variable set to OFF) and have the Group Replication plugin installed. You can use this function to remove the member actions configuration that a server used when it was part of a group, if you intend to use it as a standalone server with no member actions or different member actions.

# **Member action: mysql\_disable\_super\_read\_only\_if\_primary**

The member action mysql\_disable\_super\_read\_only\_if\_primary can be configured to make a group in single-primary mode stay in super read-only mode when a new primary is elected, so that the group only accepts replicated transactions and does not accept any direct writes from clients. This setup means that when a group's purpose is to provide a secondary backup to another group for disaster tolerance, you can ensure that the secondary group remains synchronized with the first.

By default, super read-only mode is disabled on the primary when it is elected, so that the primary becomes read-write, and accepts updates from a replication source server and from clients. This is the situation when the member action mysql\_disable\_super\_read\_only\_if\_primary is enabled, which is its default setting. If you set the action to disabled using the group\_replication\_disable\_member\_action function, the primary remains in super read-only mode after election. In this state, it does not accept updates from any clients, even users who have the CONNECTION\_ADMIN or SUPER privilege. It does continue to accept updates performed by replication threads.

# <span id="page-126-0"></span>**20.5.2 Restarting a Group**

Group Replication is designed to ensure that the database service is continuously available, even if some of the servers that form the group are currently unable to participate in it due to planned maintenance or unplanned issues. As long as the remaining members are a majority of the group they can elect a new primary and continue to function as a group. However, if every member of a replication group leaves the group, and Group Replication is stopped on every member by a STOP GROUP\_REPLICATION statement or system shutdown, the group now only exists in theory, as a configuration on the members. In that situation, to re-create the group, it must be started by bootstrapping as if it was being started for the first time.

The difference between bootstrapping a group for the first time and doing it for the second or subsequent times is that in the latter situation, the members of a group that was shut down might have different transaction sets from each other, depending on the order in which they were stopped or failed. A member cannot join a group if it has transactions that are not present on the other group members.

For Group Replication, this includes both transactions that have been committed and applied, which are in the gtid\_executed GTID set, and transactions that have been certified but not yet applied, which are in the group\_replication\_applier channel. The exact point at which a transaction is committed depends on the transaction consistency level that is set for the group (see [Section 20.5.3,](#page-128-0) ["Transaction Consistency Guarantees"](#page-128-0)). However, a Group Replication group member never removes a transaction that has been certified, which is a declaration of the member's intent to commit the transaction.

The replication group must therefore be restarted beginning with the most up to date member, that is, the member that has the most transactions executed and certified. The members with fewer transactions can then join and catch up with the transactions they are missing through distributed recovery. It is not correct to assume that the last known primary member of the group is the most up to date member of the group, because a member that was shut down later than the primary might have more transactions. You must therefore restart each member to check the transactions, compare all the transaction sets, and identify the most up to date member. This member can then be used to bootstrap the group.

Follow this procedure to restart a replication group safely after every member shuts down.

- 1. For each group member in turn, in any order:
  - a. Connect a client to the group member. If Group Replication is not already stopped, issue a STOP GROUP\_REPLICATION statement and wait for Group Replication to stop.
  - b. Edit the MySQL Server configuration file (typically named my.cnf on Linux and Unix systems, or my.ini on Windows systems) and set the system variable group\_replication\_start\_on\_boot=OFF. This setting prevents Group Replication from starting when MySQL Server is started, which is the default.
    - If you cannot change that setting on the system, you can just allow the server to attempt to start Group Replication, which will fail because the group has been fully shut down and not yet bootstrapped. If you take that approach, do not set group\_replication\_bootstrap\_group=ON on any server at this stage.
  - c. Start the MySQL Server instance, and verify that Group Replication has not been started (or has failed to start). Do not start Group Replication at this stage.
  - d. Collect the following information from the group member:
    - The contents of the gtid\_executed GTID set. You can get this by issuing the following statement:

```
mysql> SELECT @@GLOBAL.GTID_EXECUTED
```

• The set of certified transactions on the group\_replication\_applier channel. You can get this by issuing the following statement:

```
mysql> SELECT received_transaction_set FROM \
 performance_schema.replication_connection_status WHERE \
 channel_name="group_replication_applier";
```

- 2. When you have collected the transaction sets from all the group members, compare them to find which member has the biggest transaction set overall, including both the executed transactions (gtid\_executed) and the certified transactions (on the group\_replication\_applier channel). You can do this manually by looking at the GTIDs, or you can compare the GTID sets using stored functions, as described in Section 19.1.3.8, "Stored Function Examples to Manipulate GTIDs".
- 3. Use the member that has the biggest transaction set to bootstrap the group, by connecting a client to the group member and issuing the following statements:

```
mysql> SET GLOBAL group_replication_bootstrap_group=ON;
```

```
mysql> START GROUP_REPLICATION;
mysql> SET GLOBAL group_replication_bootstrap_group=OFF;
```

It is important not to store the setting group\_replication\_bootstrap\_group=ON in the configuration file, otherwise when the server is restarted again, a second group with the same name is set up.

4. To verify that the group now exists with this founder member in it, issue this statement on the member that bootstrapped it:

```
mysql> SELECT * FROM performance_schema.replication_group_members;
```

5. Add each of the other members back into the group, in any order, by issuing a START GROUP\_REPLICATION statement on each of them:

```
mysql> START GROUP_REPLICATION;
```

6. To verify that each member has joined the group, issue this statement on any member:

```
mysql> SELECT * FROM performance_schema.replication_group_members;
```

7. When the members have rejoined the group, if you edited their configuration files to set group\_replication\_start\_on\_boot=OFF, you can edit them again to set ON (or remove the system variable, since ON is the default).

# <span id="page-128-0"></span>**20.5.3 Transaction Consistency Guarantees**

One of the major implications of a distributed system such as Group Replication is the consistency guarantees that it provides as a group. In other words, the consistency of the global synchronization of transactions distributed across the members of the group. This section describes how Group Replication handles consistency guarantees depending on the events that occur in a group, and how to best configure your group's consistency guarantees.