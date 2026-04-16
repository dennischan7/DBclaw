---
source: MySQL 8.4 Reference
title: 00_Overview
---

When upgrading an online group you should consider the following points:

• Regardless of the way which you upgrade your group, it is important to disable any writes to group members until they are ready to rejoin the group.

• When a member is stopped, the super\_read\_only variable is set to on automatically, but this change is not persisted.

# <span id="page-120-0"></span>**20.8.3.2 Upgrading a Group Replication Member**

This section explains the steps required for upgrading a member of a group. This procedure is part of the methods described at [Section 20.8.3.3, "Group Replication Online Upgrade Methods".](#page-121-0) The process of upgrading a member of a group is common to all methods and is explained first. The way which you join upgraded members can depend on which method you are following, and other factors such as whether the group is operating in single-primary or multi-primary mode. How you upgrade the server instance, using either the in-place or provision approach, does not impact on the methods described here.

The process of upgrading a member consists of removing it from the group, following your chosen method of upgrading the member, and then rejoining the upgraded member to a group. The recommended order of upgrading members in a single-primary group is to upgrade all secondaries, and then upgrade the primary last. If the primary is upgraded before a secondary, a new primary using the older MySQL version is chosen, but there is no need for this step.

To upgrade a member of a group:

- Connect a client to the group member and issue STOP GROUP\_REPLICATION. Before proceeding, ensure that the member's status is OFFLINE by monitoring the replication\_group\_members table.
- Disable Group Replication from starting up automatically so that you can safely connect to the member after upgrading and configure it without it rejoining the group by setting [group\\_replication\\_start\\_on\\_boot=0](#page-164-0).

![](_page_120_Picture_8.jpeg)

#### **Important**

If an upgraded member has [group\\_replication\\_start\\_on\\_boot=1](#page-164-0) then it could rejoin the group before you can perform the MySQL upgrade procedure and could result in issues. For example, if the upgrade fails and the server restarts again, then a possibly broken server could try to join the group.

- Stop the member, for example using mysqladmin shutdown or the SHUTDOWN statement. Any other members in the group continue running.
- Upgrade the member, using the in-place or provisioning approach. See Chapter 3, Upgrading MySQL for details. When restarting the upgraded member, because [group\\_replication\\_start\\_on\\_boot](#page-164-0) is set to 0, Group Replication does not start on the instance, and therefore it does not rejoin the group.
- Once the MySQL upgrade procedure has been performed on the member, [group\\_replication\\_start\\_on\\_boot](#page-164-0) must be set to 1 to ensure Group Replication starts correctly after restart. Restart the member.
- Connect to the upgraded member and issue START GROUP\_REPLICATION. This rejoins the member to the group. The Group Replication metadata is in place on the upgraded server, therefore there is usually no need to reconfigure Group Replication. The server has to catch up with any transactions processed by the group while the server was offline. Once it has caught up with the group, it becomes an online member of the group.

![](_page_120_Picture_15.jpeg)

# **Note**

The longer it takes to upgrade a server, the more time that member is offline and therefore the more time it takes for the server to catch up when added back to the group.

When an upgraded member joins a group which has any member running an earlier MySQL Server version, the upgraded member joins with super\_read\_only=on. This ensures that no writes are made to upgraded members until all members are running the newer version. In a multi-primary mode group, when the upgrade has been completed successfully and the group is ready to process transactions, members that are intended as writeable primaries must be set to read/write mode. When all members of a group have been upgraded to the same release, they all change back to read/write mode automatically.

## <span id="page-121-0"></span>**20.8.3.3 Group Replication Online Upgrade Methods**

Choose one of the following methods of upgrading a Group Replication group:

### **Rolling In-Group Upgrade**

This method is supported provided that servers running a newer version are not generating workload to the group while there are still servers with an older version in it. In other words servers with a newer version can join the group only as secondaries. In this method there is only ever one group, and each server instance is removed from the group, upgraded and then rejoined to the group.

This method is well suited to single-primary groups. When the group is operating in single-primary mode, if you require the primary to remain the same throughout (except when it is being upgraded itself), it should be the last member to be upgraded. The primary cannot remain as the primary unless it is running the lowest MySQL Server version in the group. After the primary has been upgraded, you can use the group\_replication\_set\_as\_primary() function to reappoint it as the primary. If you do not mind which member is the primary, the members can be upgraded in any order. The group elects a new primary whenever necessary from among the members running the lowest MySQL Server version, following the election policies described in [Section 20.1.3.1, "Single-Primary Mode"](#page-14-1).

For groups operating in multi-primary mode, during a rolling in-group upgrade the number of primaries is decreased, causing a reduction in write availability. This is because if a member joins a group when it is running a higher MySQL Server version than the lowest version that the existing group members are running, it automatically remains in read-only mode (super\_read\_only=ON).

For full information on version compatibility in a group and how this influences the behavior of a group during an upgrade process, see [Section 20.8.1, "Combining Different Member Versions in a Group"](#page-117-1) .

### **Rolling Migration Upgrade**

In this method you remove members from the group, upgrade them and then create a second group using the upgraded members. For groups operating in multi-primary mode, during this process the number of primaries is decreased, causing a reduction in write availability. This does not impact groups operating in single-primary mode.

Because the group running the older version is online while you are upgrading the members, you need the group running the newer version to catch up with any transactions executed while the members were being upgraded. Therefore one of the servers in the new group is configured as a replica of a primary from the older group. This ensures that the new group catches up with the older group. Because this method relies on an asynchronous replication channel which is used to replicate data from one group to another, it is supported under the same assumptions and requirements of asynchronous source-replica replication, see Chapter 19, Replication. For groups operating in singleprimary mode, the asynchronous replication connection to the old group must send data to the primary in the new group, for a multi-primary group the asynchronous replication channel can connect to any primary.

#### The process is to:

• remove members from the original group running the older server version one by one, see [Section 20.8.3.2, "Upgrading a Group Replication Member"](#page-120-0)

- upgrade the server version running on the member, see Chapter 3, Upgrading MySQL. You can either follow an in-place or provision approach to upgrading.
- create a new group with the upgraded members, see Chapter 20, [Group Replication](#page-8-0). In this case you need to configure a new group name on each member (because the old group is still running and using the old name), bootstrap an initial upgraded member, and then add the remaining upgraded members.
- set up an asynchronous replication channel between the old group and the new group, see Section 19.1.3.4, "Setting Up Replication Using GTIDs". Configure the older primary to function as the asynchronous replication source server and the new group member as a GTID-based replica.

Before you can redirect your application to the new group, you must ensure that the new group has a suitable number of members, for example so that the group can handle the failure of a member. Issue SELECT \* FROM performance\_schema.replication\_group\_members and compare the initial group size and the new group size. Wait until all data from the old group is propagated to the new group and then drop the asynchronous replication connection and upgrade any missing members.

### **Rolling Duplication Upgrade**

In this method you create a second group consisting of members which are running the newer version, and the data missing from the older group is replicated to the newer group. This assumes that you have enough servers to run both groups simultaneously. Due to the fact that during this process the number of primaries is not decreased, for groups operating in multi-primary mode there is no reduction in write availability. This makes rolling duplication upgrade well suited to groups operating in multiprimary mode. This does not impact groups operating in single-primary mode.

Because the group running the older version is online while you are provisioning the members in the new group, you need the group running the newer version to catch up with any transactions executed while the members were being provisioned. Therefore one of the servers in the new group is configured as a replica of a primary from the older group. This ensures that the new group catches up with the older group. Because this method relies on an asynchronous replication channel which is used to replicate data from one group to another, it is supported under the same assumptions and requirements of asynchronous source-replica replication, see Chapter 19, Replication. For groups operating in single-primary mode, the asynchronous replication connection to the old group must send data to the primary in the new group, for a multi-primary group the asynchronous replication channel can connect to any primary.

The process is to:

- deploy a suitable number of members so that the group running the newer version can handle failure of a member
- take a backup of the existing data from a member of the group
- use the backup from the older member to provision the members of the new group, see [Section 20.8.3.4, "Group Replication Upgrade with mysqlbackup"](#page-123-1) for one method.

![](_page_122_Picture_12.jpeg)

#### **Note**

You must restore the backup to the same version of MySQL which the backup was taken from, and then perform an in-place upgrade. For instructions, see Chapter 3, Upgrading MySQL.

- create a new group with the upgraded members, see Chapter 20, [Group Replication](#page-8-0). In this case you need to configure a new group name on each member (because the old group is still running and using the old name), bootstrap an initial upgraded member, and then add the remaining upgraded members.
- set up an asynchronous replication channel between the old group and the new group, see Section 19.1.3.4, "Setting Up Replication Using GTIDs". Configure the older primary to function as the asynchronous replication source server and the new group member as a GTID-based replica.

Once the ongoing data missing from the newer group is small enough to be quickly transferred, you must redirect write operations to the new group. Wait until all data from the old group is propagated to the new group and then drop the asynchronous replication connection.

## <span id="page-123-1"></span>**20.8.3.4 Group Replication Upgrade with mysqlbackup**

As part of a provisioning approach you can use MySQL Enterprise Backup to copy and restore the data from a group member to new members. However you cannot use this technique to directly restore a backup taken from a member running an older version of MySQL to a member running a newer version of MySQL. The solution is to restore the backup to a new server instance which is running the same version of MySQL as the member which the backup was taken from, and then upgrade the instance. This process consists of:

- Take a backup from a member of the older group using mysqlbackup. See [Section 20.5.6, "Using](#page-73-0) [MySQL Enterprise Backup with Group Replication".](#page-73-0)
- Deploy a new server instance, which must be running the same version of MySQL as the older member where the backup was taken.
- Restore the backup from the older member to the new instance using mysqlbackup.
- Upgrade MySQL on the new instance, see Chapter 3, Upgrading MySQL.

Repeat this process to create a suitable number of new instances, for example to be able to handle a failover. Then join the instances to a group based on the [Section 20.8.3.3, "Group Replication Online](#page-121-0) [Upgrade Methods".](#page-121-0)`

# <span id="page-123-0"></span>**20.9 Group Replication Variables**

The next two sections contain information about MySQL server system and server status variables which are specific to the Group Replication plugin.

**Table 20.4 Group Replication Variable and Option Summary**

| Name | Cmd-Line                                         | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|--------------------------------------------------|-------------|------------|------------|-----------|---------|
|      | Gr_all_consensus_proposals_count                 |             |            | Yes        | Both      | No      |
|      | Gr_all_consensus_time_sum                        |             |            | Yes        | Both      | No      |
|      | Gr_certification_garbage_collector_count         |             |            | Yes        | Both      | No      |
|      | Gr_certification_garbage_collector_time_sum      |             |            | Yes        | Both      | No      |
|      | Gr_consensus_bytes_received_sum                  |             |            | Yes        | Both      | No      |
|      | Gr_consensus_bytes_sent_sum                      |             |            | Yes        | Both      | No      |
|      | Gr_control_messages_sent_bytes_sum               |             |            | Yes        | Both      | No      |
|      | Gr_control_messages_sent_count                   |             |            | Yes        | Both      | No      |
|      | Gr_control_messages_sent_roundtrip_time_sum      |             |            | Yes        | Both      | No      |
|      | Gr_data_messages_sent_bytes_sum                  |             |            | Yes        | Both      | No      |
|      | Gr_data_messages_sent_count                      |             |            | Yes        | Both      | No      |
|      | Gr_data_messages_sent_roundtrip_time_sum         |             |            | Yes        | Both      | No      |
|      | Gr_empty_consensus_proposals_count               |             |            | Yes        | Both      | No      |
|      | Gr_extended_consensus_count                      |             |            | Yes        | Both      | No      |
|      | Gr_flow_control_throttle_active_count            |             |            | Yes        | Global    | No      |
|      | Gr_flow_control_throttle_count                   |             |            | Yes        | Global    | No      |
|      | Gr_flow_control_throttle_last_throttle_timestamp |             |            | Yes        | Global    | No      |
|      | Gr_flow_control_throttle_time_sum                |             |            | Yes        | Global    | No      |
|      | Gr_last_consensus_end_timestamp                  |             |            | Yes        | Both      | No      |

| Name | Cmd-Line                                                   | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|------------------------------------------------------------|-------------|------------|------------|-----------|---------|
|      | Gr_total_messages_sent_count                               |             |            | Yes        | Both      | No      |
|      | Gr_transactions_consistency_after_sync_count               |             |            | Yes        | Both      | No      |
|      | Gr_transactions_consistency_after_sync_time_sum            |             |            | Yes        | Both      | No      |
|      | Gr_transactions_consistency_after_termination_count        |             |            | Yes        | Both      | No      |
|      | Gr_transactions_consistency_after_termination_time_sum Yes |             |            |            | Both      | No      |
|      | Gr_transactions_consistency_before_begin_count             |             |            | Yes        | Both      | No      |
|      | Gr_transactions_consistency_before_begin_time_sum          |             |            | Yes        | Both      | No      |
|      | group_replication_advertise_recovery_endpoints<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_allow_local_lower_version_join<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_auto_increment_increment<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_autorejoin_tries<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_bootstrap_group<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_clone_threshold<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_communication_debug_options<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_communication_max_message_size<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_communication_stack                      |             | Yes        |            | Global    | Yes     |
|      | group_replication_components_stop_timeout<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_compression_threshold<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_consistency<br>Yes                       | Yes         | Yes        |            | Both      | Yes     |
|      | group_replication_enforce_update_everywhere_checks<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_exit_state_action<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_applier_threshold<br>Yes    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_certifier_threshold<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_hold_percent<br>Yes         | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_max_quota<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_member_quota_percent<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_min_quota<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_min_recovery_quota<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_mode<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_period<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_release_percent<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_force_members<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_group_name<br>Yes                        | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_group_seeds<br>Yes                       | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_gtid_assignment_block_size<br>Yes        | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_ip_allowlist<br>Yes                      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_local_address<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_member_expel_timeout<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_member_weight<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_message_cache_size<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_paxos_single_leader<br>Yes               | Yes         | Yes        |            | Global    | Yes     |

| Name | Cmd-Line                                                              | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|-----------------------------------------------------------------------|-------------|------------|------------|-----------|---------|
|      | group_replication_poll_spin_loops<br>Yes                              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_preemptive_garbage_collection<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_preemptive_garbage_collection_rows_threshold<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_get_public_key<br>Yes                      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_public_key_path<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_reconnect_interval<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_retry_count<br>Yes                         | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_ca<br>Yes                              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_capath<br>Yes                          | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cert<br>Yes                            | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cipher<br>Yes                          | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crl<br>Yes                             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crlpath<br>Yes                         | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_key<br>Yes                             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_verify_server_cert<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_tls_ciphersuites<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_tls_version<br>Yes                         | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_use_ssl<br>Yes                             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_single_primary_mode<br>Yes                          | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_ssl_mode<br>Yes                                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_start_on_boot<br>Yes                                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_transaction_size_limit<br>Yes                       | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_unreachable_majority_timeout<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_view_change_uuid<br>Yes                             | Yes         | Yes        |            | Global    | Yes     |

# <span id="page-125-0"></span>**20.9.1 Group Replication System Variables**

This section lists the system variables that are specific to the Group Replication plugin.

The name of each Group Replication system variable is prefixed with group\_replication\_.

![](_page_125_Picture_5.jpeg)

#### **Note**

InnoDB Cluster uses Group Replication, but the default values of the Group Replication system variables may differ from the defaults documented in this section. For example, in InnoDB Cluster, the default value of [group\\_replication\\_communication\\_stack](#page-134-0) is MYSQL, not XCOM as it is for a default Group Replication implementation.

For more information, see [MySQL InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster.md).

Some system variables on a Group Replication group member, including some Group Replicationspecific system variables and some general system variables, are group-wide configuration settings. These system variables must have the same value on all group members, and require a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to reboot a group where every member has been stopped, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If a running group has a value set for a group-wide configuration setting, and a joining member has a different value set for that system variable, the joining member cannot join the group until the value is changed to match. If the group has a value set for one of these system variables, and the joining member does not support the system variable, it cannot join the group.

The following system variables are group-wide configuration settings:

- [group\\_replication\\_single\\_primary\\_mode](#page-162-0)
- [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-137-0)
- [group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-146-0)
- [group\\_replication\\_view\\_change\\_uuid](#page-166-0) (deprecated)
- [group\\_replication\\_paxos\\_single\\_leader](#page-152-0)
- [group\\_replication\\_communication\\_stack](#page-134-0) (a special case not policed by Group Replication's own checks; see the system variable description for details)
- default\_table\_encryption
- lower\_case\_table\_names

Group-wide configuration settings cannot be changed by the usual methods while Group Replication is running, but it is possible to use the group\_replication\_switch\_to\_single\_primary\_mode() and group\_replication\_switch\_to\_multi\_primary\_mode() functions to change the values of [group\\_replication\\_single\\_primary\\_mode](#page-162-0) and [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-137-0) while the group is still running. For more information, see [Section 20.5.1.2, "Changing the Group Mode".](#page-46-0)

Most system variables for Group Replication can have different values on different group members. For the following system variables, it is advisable to set the same value on all members of a group in order to avoid unnecessary rollback of transactions, failure of message delivery, or failure of message recovery:

- [group\\_replication\\_auto\\_increment\\_increment](#page-129-0)
- [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0)
- [group\\_replication\\_compression\\_threshold](#page-135-0)
- [group\\_replication\\_message\\_cache\\_size](#page-151-0)
- [group\\_replication\\_transaction\\_size\\_limit](#page-165-0)

The value of [group\\_replication\\_preemptive\\_garbage\\_collection](#page-153-1) must be the same on all group members.

Most system variables for Group Replication are described as dynamic, and their values can be changed while the server is running. However, in most cases, the change takes effect only after you stop and restart Group Replication on the group member using a STOP GROUP\_REPLICATION statement followed by a START GROUP\_REPLICATION statement. Changes to the following system variables take effect without stopping and restarting Group Replication:

- [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0)
- [group\\_replication\\_autorejoin\\_tries](#page-130-0)
- [group\\_replication\\_consistency](#page-136-0)
- [group\\_replication\\_exit\\_state\\_action](#page-138-0)
- [group\\_replication\\_flow\\_control\\_applier\\_threshold](#page-140-0)
- [group\\_replication\\_flow\\_control\\_certifier\\_threshold](#page-140-1)

- [group\\_replication\\_flow\\_control\\_hold\\_percent](#page-140-2)
- [group\\_replication\\_flow\\_control\\_max\\_quota](#page-141-0)
- [group\\_replication\\_flow\\_control\\_member\\_quota\\_percent](#page-141-1)
- [group\\_replication\\_flow\\_control\\_min\\_quota](#page-142-0)
- [group\\_replication\\_flow\\_control\\_min\\_recovery\\_quota](#page-142-1)
- [group\\_replication\\_flow\\_control\\_mode](#page-142-2)
- [group\\_replication\\_flow\\_control\\_period](#page-143-0)
- [group\\_replication\\_flow\\_control\\_release\\_percent](#page-143-1)
- [group\\_replication\\_force\\_members](#page-144-0)
- [group\\_replication\\_ip\\_allowlist](#page-146-1)
- [group\\_replication\\_member\\_expel\\_timeout](#page-149-0)
- [group\\_replication\\_member\\_weight](#page-150-0)
- [group\\_replication\\_transaction\\_size\\_limit](#page-165-0)
- [group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1)

When you change the values of any Group Replication system variables, bear in mind that if there is a point where Group Replication is stopped on every member at once by a STOP GROUP\_REPLICATION statement or system shutdown, the group must be restarted by bootstrapping as if it was being started for the first time. For instructions on doing this safely, see [Section 20.5.2, "Restarting a Group"](#page-50-0). In the case of group-wide configuration settings, this is required, but if you are changing other settings, try to ensure that at least one member is running at all times.

![](_page_127_Picture_16.jpeg)

### **Important**

- A number of system variables for Group Replication are not completely validated during server startup if they are passed as command line arguments to the server. These system variables include [group\\_replication\\_group\\_name](#page-145-0), [group\\_replication\\_single\\_primary\\_mode](#page-162-0), [group\\_replication\\_force\\_members](#page-144-0), the SSL variables, and the flow control system variables. They are fully validated only after the server has started.
- System variables for Group Replication that specify IP addresses or host names for group members are not validated until a START GROUP\_REPLICATION statement is issued. Group Replication's Group Communication System (GCS) is not available to validate the values until that point.

Server system variables specific to the Group Replication plugin, along with descriptions of their function or purpose, are listed here:

<span id="page-127-0"></span>• [group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0)

| Command-Line Format | group-replication-advertise<br>recovery-endpoints=value |  |
|---------------------|---------------------------------------------------------|--|
| System Variable     | group_replication_advertise_recovery_endpoints          |  |
| Scope               | Global                                                  |  |
| Dynamic             | Yes                                                     |  |

| SET_VAR Hint Applies | No      |
|----------------------|---------|
| Type                 | String  |
| Default Value        | DEFAULT |

The value of this system variable can be changed while Group Replication is running. The change takes effect immediately on the member. However, a joining member that already received the previous value of the system variable continues to use that value. Only members that join after the value change receive the new value.

[group\\_replication\\_advertise\\_recovery\\_endpoints](#page-127-0) specifies how a joining member can establish a connection to an existing member for state transfer for distributed recovery. The connection is used for both remote cloning operations and state transfer from the donor's binary log.

A value of DEFAULT, which is the default setting, means joining members use the existing member's standard SQL client connection, as specified by MySQL Server's hostname and port system variables. If an alternative port number is specified by the report\_port system variable, that one is used instead. The Performance Schema table replication\_group\_members shows this connection's address and port number in the MEMBER\_HOST and MEMBER\_PORT columns.

Instead of DEFAULT, you can specify one or more distributed recovery endpoints, which the existing member advertises to joining members for them to use. Offering distributed recovery endpoints lets administrators control distributed recovery traffic separately from regular MySQL client connections to the group members. Joining members try each of the endpoints in turn in the order they are specified on the list.

Specify the distributed recovery endpoints as a comma-separated list of IP addresses and port numbers, for example:

```
group_replication_advertise_recovery_endpoints= "127.0.0.1:3306,127.0.0.1:4567,[::1]:3306,localhost:3306"
```

IPv4 and IPv6 addresses and host names can be used in any combination. IPv6 addresses must be specified in square brackets. Host names must resolve to a local IP address. Wildcard address formats cannot be used, and you cannot specify an empty list. Note that the standard SQL client connection is not automatically included on a list of distributed recovery endpoints. If you want to use it as an endpoint, you must include it explicitly on the list.

For details of how to select IP addresses and ports as distributed recovery endpoints, and how joining members use them, see [Selecting addresses for distributed recovery endpoints](#page-60-0). A summary of the requirements is as follows:

- The IP addresses do not have to be configured for MySQL Server, but they do have to be assigned to the server.
- The ports do have to be configured for MySQL Server using the port, report\_port, or admin\_port system variable.
- Appropriate permissions are required for the replication user for distributed recovery if the admin\_port is used.
- The IP addresses do not need to be added to the Group Replication allowlist specified by the [group\\_replication\\_ip\\_allowlist](#page-146-1) system variable.
- The SSL requirements for the connection are as specified by the group\_replication\_recovery\_ssl\_\* options.
- <span id="page-128-0"></span>• [group\\_replication\\_allow\\_local\\_lower\\_version\\_join](#page-128-0)

| Command-Line Format | group-replication-allow-local |
|---------------------|-------------------------------|
|                     | lower-version-join[={OFF ON}] |

| Deprecated           | Yes                                              |  |
|----------------------|--------------------------------------------------|--|
| System Variable      | group_replication_allow_local_lower_version_join |  |
| Scope                | Global                                           |  |
| Dynamic              | Yes                                              |  |
| SET_VAR Hint Applies | No                                               |  |
| Type                 | Boolean                                          |  |
| Default Value        | OFF                                              |  |

[group\\_replication\\_allow\\_local\\_lower\\_version\\_join](#page-128-0) allows the current server to join the group even if it is running a lower MySQL Server version than the group. With the default setting OFF, servers are not permitted to join a replication group if they are running a lower version than the existing group members. This standard policy ensures that all members of a group are able to exchange messages and apply transactions.

Set [group\\_replication\\_allow\\_local\\_lower\\_version\\_join](#page-128-0) to ON only in the following scenarios:

- A server must be added to the group in an emergency in order to improve the group's fault tolerance, and only older versions are available.
- You want to roll back an upgrade for one or more replication group members without shutting down the whole group and bootstrapping it again.

![](_page_129_Picture_7.jpeg)

#### **Warning**

Setting this option to ON does not make the new member compatible with the group, and allows it to join the group without any safeguards against incompatible behaviors by the existing members. To ensure the new member's correct operation, take both of the following precautions:

- 1. Before the server running the lower version joins the group, stop all writes on that server.
- 2. From the point where the server running the lower version joins the group, stop all writes on the other servers in the group.

Without these precautions, the server running the lower version is likely to experience difficulties and terminate with an error.

<span id="page-129-0"></span>• [group\\_replication\\_auto\\_increment\\_increment](#page-129-0)

| Command-Line Format  | group-replication-auto-increment<br>increment=# |  |
|----------------------|-------------------------------------------------|--|
| System Variable      | group_replication_auto_increment_increment      |  |
| Scope                | Global                                          |  |
| Dynamic              | Yes                                             |  |
| SET_VAR Hint Applies | No                                              |  |
| Type                 | Integer                                         |  |
| Default Value        | 7                                               |  |
| Minimum Value        | 1                                               |  |

| Maximum Value | 65535 |  |
|---------------|-------|--|
|---------------|-------|--|

This system variable should have the same value on all group members. You cannot change the value of this system variable while Group Replication is running. You must stop Group Replication, change the value of the system variable, then restart Group Replication, on each of the group members. During this process, the value of the system variable is permitted to differ between group members, but some transactions on group members might be rolled back.

[group\\_replication\\_auto\\_increment\\_increment](#page-129-0) determines the interval between successive values for auto-incremented columns for transactions that execute on this server instance. Adding an interval avoids the selection of duplicate auto-increment values for writes on group members, which causes rollback of transactions. The default value of 7 represents a balance between the number of usable values and the permitted maximum size of a replication group (9 members). If your group has more or fewer members, you can set this system variable to match the expected number of group members before Group Replication is started.

![](_page_130_Picture_4.jpeg)

#### **Important**

Setting group\_replication\_auto\_increment\_increment has no effect when [group\\_replication\\_single\\_primary\\_mode](#page-162-0) is ON.

When Group Replication is started on a server instance, the value of the server system variable auto\_increment\_increment is changed to this value, and the value of the server system variable auto\_increment\_offset is changed to the server ID. The changes are reverted when Group Replication is stopped. These changes are only made and reverted if auto\_increment\_increment and auto\_increment\_offset each have their default value of 1. If their values have already been modified from the default, Group Replication does not alter them. The system variables are also not modified when Group Replication is in single-primary mode, where only one server writes.

<span id="page-130-0"></span>• [group\\_replication\\_autorejoin\\_tries](#page-130-0)

| Command-Line Format  | group-replication-autorejoin<br>tries=# |
|----------------------|-----------------------------------------|
| System Variable      | group_replication_autorejoin_tries      |
| Scope                | Global                                  |
| Dynamic              | Yes                                     |
| SET_VAR Hint Applies | No                                      |
| Type                 | Integer                                 |
| Default Value        | 3                                       |
| Minimum Value        | 0                                       |
| Maximum Value        | 2016                                    |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. The system variable's current value is read when an issue occurs that means the behavior is needed.

[group\\_replication\\_autorejoin\\_tries](#page-130-0) specifies the number of tries that a member makes to automatically rejoin the group if it is expelled, or if it is unable to contact a majority of the group before the [group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1) setting is reached. When the member's expulsion or unreachable majority timeout is reached, it makes an attempt to rejoin (using the current plugin option values), then continues to make further autorejoin attempts up to the specified number of tries. After an unsuccessful auto-rejoin attempt, the member waits 5 minutes before the next try. If the specified number of tries is exhausted without the member rejoining or being stopped, the member proceeds to the action specified by the [group\\_replication\\_exit\\_state\\_action](#page-138-0) system variable.

During and between auto-rejoin attempts, a member remains in super read only mode and does not accept writes, but reads can still be made on the member, with an increasing likelihood of stale reads over time. If you cannot tolerate the possibility of stale reads for any period of time, set [group\\_replication\\_autorejoin\\_tries](#page-130-0) to 0. For more information on the auto-rejoin feature, and considerations when choosing a value for this option, see [Section 20.7.7.3, "Auto-Rejoin"](#page-101-1).

<span id="page-131-0"></span>• [group\\_replication\\_bootstrap\\_group](#page-131-0)

| Command-Line Format  | group-replication-bootstrap<br>group[={OFF ON}] |
|----------------------|-------------------------------------------------|
| System Variable      | group_replication_bootstrap_group               |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Boolean                                         |
| Default Value        | OFF                                             |

[group\\_replication\\_bootstrap\\_group](#page-131-0) configures this server to bootstrap the group. This system variable must only be set on one server, and only when starting the group for the first time or restarting the entire group. After the group has been bootstrapped, set this option to OFF. It should be set to OFF both dynamically and in the configuration files. Starting two servers or restarting one server with this option set while the group is running may lead to an artificial split brain situation, where two independent groups with the same name are bootstrapped.

For instructions to bootstrap a group for the first time, see [Section 20.2.1.5, "Bootstrapping the](#page-29-0) [Group"](#page-29-0). For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group"](#page-50-0).

<span id="page-131-1"></span>• [group\\_replication\\_clone\\_threshold](#page-131-1)

| Command-Line Format  | group-replication-clone<br>threshold=# |
|----------------------|----------------------------------------|
| System Variable      | group_replication_clone_threshold      |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Integer                                |
| Default Value        | 9223372036854775807                    |
| Minimum Value        | 1                                      |
| Maximum Value        | 9223372036854775807                    |
| Unit                 | transactions                           |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_clone\\_threshold](#page-131-1) specifies the transaction gap, as a number of transactions, between the existing member (donor) and the joining member (recipient) that triggers the use of a remote cloning operation for state transfer to the joining member during the distributed recovery process. If the transaction gap between the joining member and a suitable donor exceeds the threshold, Group Replication begins distributed recovery with a remote cloning operation. If the

transaction gap is below the threshold, or if the remote cloning operation is not technically possible, Group Replication proceeds directly to state transfer from a donor's binary log.

![](_page_132_Picture_2.jpeg)

#### **Warning**

Do not use a low setting for [group\\_replication\\_clone\\_threshold](#page-131-1) in an active group. If a number of transactions above the threshold takes place in the group while the remote cloning operation is in progress, the joining member triggers a remote cloning operation again after restarting, and could continue this indefinitely. To avoid this situation, ensure that you set the threshold to a number higher than the number of transactions that you would expect to occur in the group during the time taken for the remote cloning operation.

To use this function, both the donor and the joining member must be set up beforehand to support cloning. For instructions, see [Section 20.5.4.2, "Cloning for Distributed Recovery"](#page-62-0). When a remote cloning operation is carried out, Group Replication manages it for you, including the required server restart, provided that [group\\_replication\\_start\\_on\\_boot=ON](#page-164-0) is set. If not, you must restart the server manually. The remote cloning operation replaces the existing data dictionary on the joining member, but Group Replication checks and does not proceed if the joining member has additional transactions that are not present on the other group members, because these transactions would be erased by the cloning operation.

The default setting (which is the maximum permitted sequence number for a transaction in a GTID) means that state transfer from a donor's binary log is virtually always attempted rather than cloning. However, note that Group Replication always attempts to execute a cloning operation, regardless of your threshold, if state transfer from a donor's binary log is impossible, for example because the transactions needed by the joining member are not available in the binary logs on any existing group member. If you do not want to use cloning at all in your replication group, do not install the clone plugin on the members.

<span id="page-132-0"></span>• [group\\_replication\\_communication\\_debug\\_options](#page-132-0)

| Command-Line Format  | group-replication-communication<br>debug-options=value |
|----------------------|--------------------------------------------------------|
| System Variable      | group_replication_communication_debug_options          |
| Scope                | Global                                                 |
| Dynamic              | Yes                                                    |
| SET_VAR Hint Applies | No                                                     |
| Type                 | String                                                 |
| Default Value        | GCS_DEBUG_NONE                                         |
| Valid Values         | GCS_DEBUG_NONE                                         |
|                      | GCS_DEBUG_BASIC                                        |
|                      | GCS_DEBUG_TRACE                                        |
|                      | XCOM_DEBUG_BASIC                                       |
|                      | XCOM_DEBUG_TRACE                                       |

GCS\_DEBUG\_ALL

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_communication\\_debug\\_options](#page-132-0) configures the level of debugging messages to provide for the different Group Replication components, such as the Group Communication System (GCS) and the group communication engine (XCom, a Paxos variant). The debug information is stored in the GCS\_DEBUG\_TRACE file in the data directory.

The set of available options, specified as strings, can be combined. The following options are available:

- GCS\_DEBUG\_NONE disables all debugging levels for both GCS and XCom.
- GCS\_DEBUG\_BASIC enables basic debugging information in GCS.
- GCS\_DEBUG\_TRACE enables trace information in GCS.
- XCOM\_DEBUG\_BASIC enables basic debugging information in XCom.
- XCOM\_DEBUG\_TRACE enables trace information in XCom.
- GCS\_DEBUG\_ALL enables all debugging levels for both GCS and XCom.

Setting the debug level to GCS\_DEBUG\_NONE only has an effect when provided without any other option. Setting the debug level to GCS\_DEBUG\_ALL overrides all other options.

<span id="page-133-0"></span>• [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0)

| Command-Line Format  | group-replication-communication                  |
|----------------------|--------------------------------------------------|
|                      | max-message-size=#                               |
| System Variable      | group_replication_communication_max_message_size |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Integer                                          |
| Default Value        | 10485760                                         |
| Minimum Value        | 0                                                |
| Maximum Value        | 1073741824                                       |
| Unit                 | bytes                                            |
|                      |                                                  |

This system variable should have the same value on all group members. You cannot change the value of this system variable while Group Replication is running. You must stop Group Replication, change the value of the system variable, then restart Group Replication, on each of the group members. During this process, the value of the system variable is permitted to differ between group members, but some transactions on group members might be rolled back.

[group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0) specifies a maximum message size for Group Replication communications. Messages greater than this size are automatically split into fragments that are sent separately and reassembled by the recipients. For more information, see [Section 20.7.5, "Message Fragmentation".](#page-96-0)

A maximum message size of 10485760 bytes (10 MiB) is set by default, which means that fragmentation is used by default. The greatest permitted value is the same as the maximum value of the replica\_max\_allowed\_packet system variable, which is 1073741824 bytes (1 GB). [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0) must be less than replica\_max\_allowed\_packet, because the applier thread cannot handle message fragments larger than the maximum permitted packet size. To switch off fragmentation, set [group\\_replication\\_communication\\_max\\_message\\_size](#page-133-0) to 0.

In order for members of a replication group to use fragmentation, the group's communication protocol version must be 8.0.16 or later. Use the group\_replication\_get\_communication\_protocol() function to view the group's communication protocol version. If a lower version is in use, group members do not fragment messages. You can use the group\_replication\_set\_communication\_protocol() function to set the group's communication protocol to a higher version if all group members support it. For more information, see [Section 20.5.1.4, "Setting a Group's Communication Protocol Version"](#page-47-0).

<span id="page-134-0"></span>• [group\\_replication\\_communication\\_stack](#page-134-0)

| System Variable      | group_replication_communication_stack |
|----------------------|---------------------------------------|
| Scope                | Global                                |
| Dynamic              | Yes                                   |
| SET_VAR Hint Applies | No                                    |
| Type                 | String                                |
| Default Value        | XCOM                                  |
| Valid Values         | XCOM                                  |
|                      | MYSQL                                 |

![](_page_134_Picture_5.jpeg)

### **Note**

This system variable is effectively a group-wide configuration setting; although it can be set at runtime, a full reboot of the replication group is required for any change to take effect.

[group\\_replication\\_communication\\_stack](#page-134-0) specifies whether the XCom communication stack or the MySQL communication stack is to be used to establish group communication connections between members. The XCom communication stack is Group Replication's own implementation, and does not support authentication or network namespaces. The MySQL communication stack is MySQL Server's native implementation, with support for authentication and network namespaces, and access to new security functions immediately on release. All members of a group must use the same communication stack.

When you use the MySQL communication stack in place of XCom, MySQL Server establishes each connection between group members using its own authentication and encryption protocols.

![](_page_134_Picture_10.jpeg)

### **Note**

If you are using InnoDB Cluster, the default value of [group\\_replication\\_communication\\_stack](#page-134-0) is MYSQL.

For more information, see [MySQL InnoDB Cluster](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster.md).

Additional configuration is required when you set up a group to use MySQL's communication stack; see [Section 20.6.1, "Communication Stack for Connection Security Management"](#page-79-1).

[group\\_replication\\_communication\\_stack](#page-134-0) is effectively a group-wide configuration setting, and the setting must be the same on all group members. However, this is not policed by Group Replication's own checks for group-wide configuration settings. A member with a different value from the rest of the group cannot communicate with the other members at all, because the communication protocols are incompatible, so it cannot exchange information about its configuration settings.

This means that although the value of the system variable can be changed while Group Replication is running, and takes effect after you restart Group Replication on the group member, the member still cannot rejoin the group until the setting has been changed on all the members. You must therefore stop Group Replication on all of the members and change the value of the system variable on them all before you can restart the group. Because all of the members are stopped, a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) is required in order for the value change to take effect. For instructions to migrate from one communication stack to another, see [Section 20.6.1, "Communication Stack for Connection Security](#page-79-1) [Management".](#page-79-1)

<span id="page-135-1"></span>• [group\\_replication\\_components\\_stop\\_timeout](#page-135-1)

| Command-Line Format  | group-replication-components-stop<br>timeout=# |
|----------------------|------------------------------------------------|
| System Variable      | group_replication_components_stop_timeout      |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | Integer                                        |
| Default Value        | 300                                            |
| Minimum Value        | 2                                              |
| Maximum Value        | 31536000                                       |
| Unit                 | seconds                                        |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

group\_replication\_components\_stop\_timeout specifies the time, in seconds, for which Group Replication waits for each of its modules to complete ongoing processes while shutting down. The component timeout applies after a STOP GROUP\_REPLICATION statement is issued, which happens automatically during server restart or auto-rejoin.

The timeout is used to resolve situations in which Group Replication components cannot be stopped normally, which might happen if a member is expelled from the group while it is in an error state, or while a process such as MySQL Enterprise Backup is holding a global lock on tables on the member. In such situations, the member cannot stop the applier thread or complete the distributed recovery process to rejoin. STOP GROUP\_REPLICATION does not complete until either the situation is resolved (for example, by the lock being released), or the component timeout expires and the modules are shut down regardless of their status.

The default value is 300 seconds, so that Group Replication components are stopped after 5 minutes if the situation is not resolved before that time, allowing the member to be restarted and to rejoin.

<span id="page-135-0"></span>• [group\\_replication\\_compression\\_threshold](#page-135-0)

| Command-Line Format  | group-replication-compression<br>threshold=# |
|----------------------|----------------------------------------------|
| System Variable      | group_replication_compression_threshold      |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |

| Type          | Integer    |
|---------------|------------|
| Default Value | 1000000    |
| Minimum Value | 0          |
| Maximum Value | 4294967295 |
| Unit          | bytes      |

The threshold value in bytes above which compression is applied to messages sent between group members. If this system variable is set to zero, compression is disabled. The value of [group\\_replication\\_compression\\_threshold](#page-135-0) should be the same on all group members.

Group Replication uses the LZ4 compression algorithm to compress messages sent in the group. Note that the maximum supported input size for the LZ4 compression algorithm is 2113929216 bytes. This limit is lower than the maximum possible value for the [group\\_replication\\_compression\\_threshold](#page-135-0) system variable, which is matched to the maximum message size accepted by XCom. With the LZ4 compression algorithm, do not set a value greater than 2113929216 bytes for [group\\_replication\\_compression\\_threshold](#page-135-0), because transactions above this size cannot be committed when message compression is enabled.

For more information, see [Section 20.7.4, "Message Compression".](#page-94-0)

<span id="page-136-0"></span>• [group\\_replication\\_consistency](#page-136-0)

| Command-Line Format  | group-replication<br>consistency=value |
|----------------------|----------------------------------------|
| System Variable      | group_replication_consistency          |
| Scope                | Global, Session                        |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | Enumeration                            |
| Default Value        | BEFORE_ON_PRIMARY_FAILOVER             |
| Valid Values         | EVENTUAL                               |
|                      | BEFORE_ON_PRIMARY_FAILOVER             |
|                      | BEFORE                                 |
|                      | AFTER                                  |
|                      | BEFORE_AND_AFTER                       |

[group\\_replication\\_consistency](#page-136-0) is a server system variable rather than a Group Replication plugin-specific variable, so a restart of Group Replication is not required for the change to take effect. Changing the session value of the system variable takes effect immediately, and changing the global value takes effect for new sessions that start after the change. The GROUP\_REPLICATION\_ADMIN privilege is required to change the global setting for this system variable.

group\_replication\_consistency determines the transaction consistency guarantee which a group provides; this can done globally, or per transaction. group\_replication\_consistency also determines the fencing mechanism used by newly elected primaries in single primary groups. The effect of the variable must be considered both for read-only and for read/write transactions. The following list shows the possible values of this variable, in order of increasing transaction consistency guarantee:

#### • EVENTUAL

Neither read-only nor read/write transactions wait for preceding transactions to be applied before executing. (Before this variables was added, this was the default behavior.) A read/write transaction does not wait for other members to apply a transaction. This means that a transaction can be externalized on one member before the others. This also means that, in the event of a primary failover, the new primary can accept new read-only transactions before the previous primary transactions have all been applied, though read/write transactions are not allowed.

### • BEFORE\_ON\_PRIMARY\_FAILOVER

New read-only or read/write transactions with a newly elected primary that is applying a backlog from the old primary are not applied until any backlog has been applied. This ensures that, in the event of primary failover, clients always see the latest value on the primary, regardless of whether the failover is intentional. This guarantees consistency, but means that clients must be able to handle the delay in the event that a backlog is being applied. The length of this delay depends on the size of the backlog being processed, but is usually not great.

#### • BEFORE

A read/write transaction waits for all preceding transactions to complete before being applied. A read-only transaction waits for all preceding transactions to complete before being executed. This ensures that this transaction reads the latest value by affecting only the latency of the transaction. This reduces any overhead from synchronization, by ensuring it is used on read-only transactions only. This consistency level also includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

# • AFTER

A read/write transaction waits until its changes have been applied to all of the other members. This value has no effect on read-only transactions, and ensures that, when a transaction is committed on the local member, any subsequent transaction reads the value written or a more recent value on any group member. This means that read-only transactions on the other members remain uncommitted until all preceding transactions are committed, increasing the latency of the affected transaction.

Use this mode with a group that is intended primarily for read-only operations to ensure that any read/write transactions are applied everywhere once they commit. This can be used by your application to ensure that subsequent reads fetch the latest data, including the latest writes. This reduces any overhead from synchronization, by ensuring that synchronization is used for read/ write transactions only.

AFTER includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

#### • BEFORE\_AND\_AFTER

A read/write transaction waits for all preceding transactions to complete, and for all its changes to be applied on all other members, before being applied. A read-only transaction waits for all preceding transactions to complete before execution takes place. This consistency level also includes the consistency guarantees provided by BEFORE\_ON\_PRIMARY\_FAILOVER.

For more information, see [Section 20.5.3, "Transaction Consistency Guarantees".](#page-51-0)

<span id="page-137-0"></span>• [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-137-0)

| Command-Line Format | group-replication-enforce-update |
|---------------------|----------------------------------|
|                     | everywhere-checks[={OFF ON}]     |

| System Variable      | group_replication_enforce_update_everywhere_checks |  |
|----------------------|----------------------------------------------------|--|
| Scope                | Global                                             |  |
| Dynamic              | Yes                                                |  |
| SET_VAR Hint Applies | No                                                 |  |
| Type                 | Boolean                                            |  |
| Default Value        | OFF                                                |  |

![](_page_138_Picture_2.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-137-0) enables or disables strict consistency checks for multi-primary update everywhere. The default is that checks are disabled. In single-primary mode, this option must be disabled on all group members. In multi-primary mode, when this option is enabled, statements are checked as follows to ensure they are compatible with multi-primary mode:

- If a transaction is executed under the SERIALIZABLE isolation level, then its commit fails when synchronizing itself with the group.
- If a transaction executes against a table that has foreign keys with cascading constraints, then the transaction fails to commit when synchronizing itself with the group.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

Use the group\_replication\_switch\_to\_single\_primary\_mode() and group\_replication\_switch\_to\_multi\_primary\_mode() functions to change the value of this system variable while the group is still running. For more information, see [Section 20.5.1.2,](#page-46-0) ["Changing the Group Mode"](#page-46-0).

<span id="page-138-0"></span>• [group\\_replication\\_exit\\_state\\_action](#page-138-0)

| Command-Line Format  | group-replication-exit-state<br>action=value |
|----------------------|----------------------------------------------|
| System Variable      | group_replication_exit_state_action          |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Enumeration                                  |
| Default Value        | OFFLINE_MODE                                 |
| Valid Values         | ABORT_SERVER                                 |
|                      | OFFLINE_MODE                                 |
|                      | READ_ONLY                                    |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. The system variable's current value is read when an issue occurs that means the behavior is needed.

[group\\_replication\\_exit\\_state\\_action](#page-138-0) configures how Group Replication behaves when this server instance leaves the group unintentionally, for example after encountering an applier error, or in the case of a loss of majority, or when another member of the group expels it due to a suspicion timing out. The timeout period for a member to leave the group in the case of a loss of majority is set by the [group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1) system variable, and the timeout period for suspicions is set by the [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) system variable. Note that an expelled group member does not know that it was expelled until it reconnects to the group, so the specified action is only taken if the member manages to reconnect, or if the member raises a suspicion on itself and expels itself.

When a group member is expelled due to a suspicion timing out or a loss of majority, if the member has the [group\\_replication\\_autorejoin\\_tries](#page-130-0) system variable set to specify a number of auto-rejoin attempts, it first makes the specified number of attempts while in super read only mode, and then follows the action specified by group\_replication\_exit\_state\_action. Auto-rejoin attempts are not made in case of an applier error, because these are not recoverable.

When group\_replication\_exit\_state\_action is set to READ\_ONLY, if the member exits the group unintentionally or exhausts its auto-rejoin attempts, the instance switches MySQL to super read only mode (by setting the system variable super\_read\_only to ON).

When group\_replication\_exit\_state\_action is set to OFFLINE\_MODE, if the member exits the group unintentionally or exhausts its auto-rejoin attempts, the instance switches MySQL to offline mode (by setting the system variable offline\_mode to ON). In this mode, connected client users are disconnected on their next request and connections are no longer accepted, with the exception of client users that have the CONNECTION\_ADMIN privilege (or the deprecated SUPER privilege). Group Replication also sets the system variable super\_read\_only to ON, so clients cannot make any updates, even if they have connected with the CONNECTION\_ADMIN or SUPER privilege.

When group\_replication\_exit\_state\_action is set to ABORT\_SERVER, if the member exits the group unintentionally or exhausts its auto-rejoin attempts, the instance shuts down MySQL.

![](_page_139_Picture_7.jpeg)

#### **Important**

If a failure occurs before the member has successfully joined the group, the specified exit action is not taken. This is the case if there is a failure during the local configuration check, or a mismatch between the configuration of the joining member and the configuration of the group. In these situations, the super\_read\_only system variable is left with its original value, connections continue to be accepted, and the server does not shut down MySQL. To ensure that the server cannot accept updates when Group Replication did not start, we therefore recommend that super\_read\_only=ON is set in the server's configuration file at startup, which Group Replication changes to OFF on primary members after it has been started successfully. This safeguard is particularly important when the server is configured to start Group Replication on server boot ([group\\_replication\\_start\\_on\\_boot=ON](#page-164-0)), but it is also useful when Group Replication is started manually using a START GROUP\_REPLICATION statement.

For more information on using this option, and the full list of situations in which the exit action is taken, see [Section 20.7.7.4, "Exit Action".](#page-101-0)

<span id="page-140-0"></span>• [group\\_replication\\_flow\\_control\\_applier\\_threshold](#page-140-0)

| Command-Line Format  | group-replication-flow-control<br>applier-threshold=# |
|----------------------|-------------------------------------------------------|
| System Variable      | group_replication_flow_control_applier_threshold      |
| Scope                | Global                                                |
| Dynamic              | Yes                                                   |
| SET_VAR Hint Applies | No                                                    |
| Type                 | Integer                                               |
| Default Value        | 25000                                                 |
| Minimum Value        | 0                                                     |
| Maximum Value        | 2147483647                                            |
| Unit                 | transactions                                          |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_applier\\_threshold](#page-140-0) specifies the number of waiting transactions in the applier queue that trigger flow control.

<span id="page-140-1"></span>• [group\\_replication\\_flow\\_control\\_certifier\\_threshold](#page-140-1)

| Unit                 | transactions                                            |  |
|----------------------|---------------------------------------------------------|--|
| Maximum Value        | 2147483647                                              |  |
| Minimum Value        | 0                                                       |  |
| Default Value        | 25000                                                   |  |
| Type                 | Integer                                                 |  |
| SET_VAR Hint Applies | No                                                      |  |
| Dynamic              | Yes                                                     |  |
| Scope                | Global                                                  |  |
| System Variable      | group_replication_flow_control_certifier_threshold      |  |
| Command-Line Format  | group-replication-flow-control<br>certifier-threshold=# |  |
|                      |                                                         |  |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_certifier\\_threshold](#page-140-1) specifies the number of waiting transactions in the certifier queue that trigger flow control.

<span id="page-140-2"></span>• [group\\_replication\\_flow\\_control\\_hold\\_percent](#page-140-2)

| Command-Line Format  | group-replication-flow-control<br>hold-percent=# |
|----------------------|--------------------------------------------------|
| System Variable      | group_replication_flow_control_hold_percent      |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Integer                                          |

3711

| Default Value | 10         |
|---------------|------------|
| Minimum Value | 0          |
| Maximum Value | 100        |
| Unit          | percentage |

[group\\_replication\\_flow\\_control\\_hold\\_percent](#page-140-2) defines what percentage of the group quota remains unused to allow a cluster under flow control to catch up on backlog. A value of 0 implies that no part of the quota is reserved for catching up on the work backlog.

<span id="page-141-0"></span>• [group\\_replication\\_flow\\_control\\_max\\_quota](#page-141-0)

| Command-Line Format  | group-replication-flow-control<br>max-quota=# |
|----------------------|-----------------------------------------------|
| System Variable      | group_replication_flow_control_max_quota      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 0                                             |
| Minimum Value        | 0                                             |
| Maximum Value        | 2147483647                                    |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_max\\_quota](#page-141-0) defines the maximum flow control quota of the group, or the maximum available quota for any period while flow control is enabled. A value of 0 implies that there is no maximum quota set. The value of this system variable cannot be smaller than [group\\_replication\\_flow\\_control\\_min\\_quota](#page-142-0) and group\_replication\_flow\_control\_min\_recovery\_quota.

<span id="page-141-1"></span>• [group\\_replication\\_flow\\_control\\_member\\_quota\\_percent](#page-141-1)

| Command-Line Format  | group-replication-flow-control<br>member-quota-percent=# |  |
|----------------------|----------------------------------------------------------|--|
| System Variable      | group_replication_flow_control_member_quota_percent      |  |
| Scope                | Global                                                   |  |
| Dynamic              | Yes                                                      |  |
| SET_VAR Hint Applies | No                                                       |  |
| Type                 | Integer                                                  |  |
| Default Value        | 0                                                        |  |
| Minimum Value        | 0                                                        |  |
| Maximum Value        | 100                                                      |  |
|                      |                                                          |  |

| Unit | percentage |
|------|------------|
|------|------------|

[group\\_replication\\_flow\\_control\\_member\\_quota\\_percent](#page-141-1) defines the percentage of the quota that a member should assume is available for itself when calculating the quotas. A value of 0 implies that the quota should be split equally between members that were writers in the last period.

<span id="page-142-0"></span>• [group\\_replication\\_flow\\_control\\_min\\_quota](#page-142-0)

| Command-Line Format  | group-replication-flow-control<br>min-quota=# |
|----------------------|-----------------------------------------------|
| System Variable      | group_replication_flow_control_min_quota      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 0                                             |
| Minimum Value        | 0                                             |
| Maximum Value        | 2147483647                                    |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_min\\_quota](#page-142-0) controls the lowest flow control quota that can be assigned to a member, independently of the calculated minimum quota executed in the last period. A value of 0 implies that there is no minimum quota. The value of this system variable cannot be larger than [group\\_replication\\_flow\\_control\\_max\\_quota](#page-141-0).

<span id="page-142-1"></span>• [group\\_replication\\_flow\\_control\\_min\\_recovery\\_quota](#page-142-1)

| Command-Line Format  | group-replication-flow-control<br>min-recovery-quota=# |
|----------------------|--------------------------------------------------------|
| System Variable      | group_replication_flow_control_min_recovery_quota      |
| Scope                | Global                                                 |
| Dynamic              | Yes                                                    |
| SET_VAR Hint Applies | No                                                     |
| Type                 | Integer                                                |
| Default Value        | 0                                                      |
| Minimum Value        | 0                                                      |
| Maximum Value        | 2147483647                                             |
|                      |                                                        |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_min\\_recovery\\_quota](#page-142-1) controls the lowest quota that can be assigned to a member because of another recovering member in the group, independently of the calculated minimum quota executed in the last period. A value of 0 implies that there is no minimum quota. The value of this system variable cannot be larger than group\_replication\_flow\_control\_max\_quota.

<span id="page-142-2"></span>• [group\\_replication\\_flow\\_control\\_mode](#page-142-2)

| Command-Line Format  | group-replication-flow-control<br>mode=value |
|----------------------|----------------------------------------------|
| System Variable      | group_replication_flow_control_mode          |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |
| Type                 | Enumeration                                  |
| Default Value        | QUOTA                                        |
| Valid Values         | DISABLED                                     |
|                      | QUOTA                                        |

[group\\_replication\\_flow\\_control\\_mode](#page-142-2) specifies the mode used for flow control.

<span id="page-143-0"></span>• [group\\_replication\\_flow\\_control\\_period](#page-143-0)

| Command-Line Format  | group-replication-flow-control<br>period=# |
|----------------------|--------------------------------------------|
| System Variable      | group_replication_flow_control_period      |
| Scope                | Global                                     |
| Dynamic              | Yes                                        |
| SET_VAR Hint Applies | No                                         |
| Type                 | Integer                                    |
| Default Value        | 1                                          |
| Minimum Value        | 1                                          |
| Maximum Value        | 60                                         |
| Unit                 | seconds                                    |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately.

[group\\_replication\\_flow\\_control\\_period](#page-143-0) defines how many seconds to wait between flow control iterations, in which flow control messages are sent and flow control management tasks are run.

<span id="page-143-1"></span>• [group\\_replication\\_flow\\_control\\_release\\_percent](#page-143-1)

| Command-Line Format  | group-replication-flow-control<br>release-percent=# |  |
|----------------------|-----------------------------------------------------|--|
| System Variable      | group_replication_flow_control_release_percent      |  |
| Scope                | Global                                              |  |
| Dynamic              | Yes                                                 |  |
| SET_VAR Hint Applies | No                                                  |  |
| Type                 | Integer                                             |  |
| Default Value        | 50                                                  |  |
| Minimum Value        | 0                                                   |  |

| Maximum Value | 1000       |
|---------------|------------|
| Unit          | percentage |

[group\\_replication\\_flow\\_control\\_release\\_percent](#page-143-1) defines how the group quota should be released when flow control no longer needs to throttle the writer members, with this percentage being the quota increase per flow control period. A value of 0 implies that once the flow control thresholds are within limits the quota is released in a single flow control iteration. The range allows the quota to be released at up to 10 times current quota, as that allows a greater degree of adaptation, mainly when the flow control period is large and the quotas are very small.

<span id="page-144-0"></span>• [group\\_replication\\_force\\_members](#page-144-0)

| Command-Line Format  | group-replication-force<br>members=value |
|----------------------|------------------------------------------|
| System Variable      | group_replication_force_members          |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | String                                   |

This system variable is used to force a new group membership. The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. You only need to set the value of the system variable on one of the group members that is to remain in the group. For details of the situation in which you might need to force a new group membership, and a procedure to follow when using this system variable, see [Section 20.7.8, "Handling a Network](#page-103-0) [Partition and Loss of Quorum"](#page-103-0).

[group\\_replication\\_force\\_members](#page-144-0) specifies a list of peer addresses as a comma separated list, such as host1:port1,host2:port2. Any existing members that are not included in the list do not receive a new view of the group and are blocked. For each existing member that is to continue as a member, you must include the IP address or host name and the port, as they are given in the [group\\_replication\\_local\\_address](#page-148-0) system variable for each member. An IPv6 address must be specified in square brackets. For example:

```
"198.51.100.44:33061,[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061,example.org:33061"
```

The group communication engine for Group Replication (XCom) checks that the supplied IP addresses are in a valid format, and checks that you have not included any group members that are currently unreachable. Otherwise, the new configuration is not validated, so you must be careful to include only online servers that are reachable members of the group. Any incorrect values or invalid host names in the list could cause the group to be blocked with an invalid configuration.

It is important before forcing a new membership configuration to ensure that the servers to be excluded have been shut down. If they are not, shut them down before proceeding. Group members that are still online can automatically form new configurations, and if this has already taken place, forcing a further new configuration could create an artificial split-brain situation for the group.

After you have used the [group\\_replication\\_force\\_members](#page-144-0) system variable to successfully force a new group membership and unblock the group, ensure that you clear the system variable. [group\\_replication\\_force\\_members](#page-144-0) must be empty in order to issue a START GROUP\_REPLICATION statement.

<span id="page-145-0"></span>• [group\\_replication\\_group\\_name](#page-145-0)

| Command-Line Format  | group-replication-group-name=value |
|----------------------|------------------------------------|
| System Variable      | group_replication_group_name       |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | String                             |

The value of this system variable cannot be changed while Group Replication is running.

[group\\_replication\\_group\\_name](#page-145-0) specifies the name of the group which this server instance belongs to, which must be a valid UUID. This UUID forms part of the GTIDs that are used when transactions received by group members from clients, and view change events that are generated internally by the group members, are written to the binary log.

![](_page_145_Picture_5.jpeg)

# **Important**

A unique UUID must be used.

<span id="page-145-1"></span>• [group\\_replication\\_group\\_seeds](#page-145-1)

| Command-Line Format  | group-replication-group<br>seeds=value |
|----------------------|----------------------------------------|
| System Variable      | group_replication_group_seeds          |
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | String                                 |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_group\\_seeds](#page-145-1) is a list of group members to which a joining member can connect to obtain details of all the current group members. The joining member uses these details to select and connect to a group member to obtain the data needed for synchrony with the group. The list consists of a single internal network address or host name for each included seed member, as configured in the seed member's [group\\_replication\\_local\\_address](#page-148-0) system variable (not the seed member's SQL client connection, as specified by MySQL Server's hostname and port system variables). The addresses of the seed members are specified as a comma separated list, such as host1:port1,host2:port2. An IPv6 address must be specified in square brackets. For example:

```
group_replication_group_seeds= "198.51.100.44:33061,[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061, example.org:33061"
```

Note that the value you specify for this variable is not validated until a START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

Usually this list consists of all members of the group, but you can choose a subset of the group members to be seeds. The list must contain at least one valid member address. Each address is validated when starting Group Replication. If the list does not contain any valid member addresses, issuing START GROUP\_REPLICATION fails.

When a server is joining a replication group, it attempts to connect to the first seed member listed in its [group\\_replication\\_group\\_seeds](#page-145-1) system variable. If the connection is refused, the joining member tries to connect to each of the other seed members in the list in order. If the joining member 3716 connects to a seed member but does not get added to the replication group as a result (for example, because the seed member does not have the joining member's address in its allowlist and closes the connection), the joining member continues to try the remaining seed members in the list in order.

A joining member must communicate with the seed member using the same protocol (IPv4 or IPv6) that the seed member advertises in the [group\\_replication\\_group\\_seeds](#page-145-1) option. For the purpose of IP address permissions for Group Replication, the allowlist on the seed member must include an IP address for the joining member for the protocol offered by the seed member, or a host name that resolves to an address for that protocol. This address or host name must be set up and permitted in addition to the joining member's [group\\_replication\\_local\\_address](#page-148-0) if the protocol for that address does not match the seed member's advertised protocol. If a joining member does not have a permitted address for the appropriate protocol, its connection attempt is refused. For more information, see [Section 20.6.4, "Group Replication IP Address Permissions".](#page-88-0)

<span id="page-146-0"></span>• [group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-146-0)

| Command-Line Format              | group-replication-gtid-assignment<br>block-size=# |
|----------------------------------|---------------------------------------------------|
| System Variable                  | group_replication_gtid_assignment_block_size      |
| Scope                            | Global                                            |
| Dynamic                          | Yes                                               |
| SET_VAR Hint Applies             | No                                                |
| Type                             | Integer                                           |
| Default Value                    | 1000000                                           |
| Minimum Value                    | 1                                                 |
| Maximum Value (64-bit platforms) | 9223372036854775807                               |
| Maximum Value (32-bit platforms) | 4294967295                                        |

![](_page_146_Picture_5.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-146-0) specifies the number of consecutive GTIDs that are reserved for each group member. Each member consumes its own blocks and reserves more when needed.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

<span id="page-146-1"></span>• [group\\_replication\\_ip\\_allowlist](#page-146-1)

| Command-Line Format | group-replication-ip<br>allowlist=value |
|---------------------|-----------------------------------------|
| System Variable     | group_replication_ip_allowlist          |
| Scope               | Global                                  |

| Dynamic              | Yes       |
|----------------------|-----------|
| SET_VAR Hint Applies | No        |
| Type                 | String    |
| Default Value        | AUTOMATIC |

[group\\_replication\\_ip\\_allowlist](#page-146-1) specifies which hosts are permitted to connect to the group. When the XCom communication stack is in use for the group ([group\\_replication\\_communication\\_stack=XCOM](#page-134-0)), the allowlist is used to control access to the group. When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack=MYSQL](#page-134-0)), user authentication is used to control access to the group, and the allowlist is not used and is ignored if set.

The address that you specify for each group member in [group\\_replication\\_local\\_address](#page-148-0) must be permitted on the other servers in the replication group. Note that the value you specify for this variable is not validated until a START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

By default, this system variable is set to AUTOMATIC, which permits connections from private subnetworks active on the host. The group communication engine for Group Replication (XCom) automatically scans active interfaces on the host, and identifies those with addresses on private subnetworks. These addresses and the localhost IP address for IPv4 and IPv6 are used to create the Group Replication allowlist. For a list of the ranges from which addresses are automatically permitted, see [Section 20.6.4, "Group Replication IP Address Permissions"](#page-88-0).

The automatic allowlist of private addresses cannot be used for connections from servers outside the private network. For Group Replication connections between server instances that are on different machines, you must provide public IP addresses and specify these as an explicit allowlist. If you specify any entries for the allowlist, the private addresses are not added automatically, so if you use any of these, you must specify them explicitly. The localhost IP addresses are added automatically.

As the value of the [group\\_replication\\_ip\\_allowlist](#page-146-1) option, you can specify any combination of the following:

- IPv4 addresses (for example, 198.51.100.44)
- IPv4 addresses with CIDR notation (for example, 192.0.2.21/24)
- IPv6 addresses (for example, 2001:db8:85a3:8d3:1319:8a2e:370:7348)
- IPv6 addresses using CIDR notation (for example, 2001:db8:85a3:8d3::/64)
- Host names (for example, example.org)
- Host names with CIDR notation (for example, www.example.com/24)

Host names can resolve to IPv4 addresses, IPv6 addresses, or both. If a host name resolves to both an IPv4 and an IPv6 address, the IPv4 address is always used for Group Replication connections. You can use CIDR notation in combination with host names or IP addresses to permit a block of IP addresses with a particular network prefix, but you should ensure that all the IP addresses in the specified subnet are under your control.

A comma must separate each entry in the allowlist. For example:

```
"192.0.2.21/24,198.51.100.44,203.0.113.0/24,2001:db8:85a3:8d3:1319:8a2e:370:7348,example.org,www.example.com/24"
```

If any of the seed members for the group are listed in the [group\\_replication\\_group\\_seeds](#page-145-1) option with an IPv6 address when a joining member has an IPv4 [group\\_replication\\_local\\_address](#page-148-0), or the reverse, you must also set up and permit an

alternative address for the joining member for the protocol offered by the seed member (or a host name that resolves to an address for that protocol). For more information, see [Section 20.6.4, "Group](#page-88-0) [Replication IP Address Permissions".](#page-88-0)

It is possible to configure different allowlists on different group members according to your security requirements, for example, in order to keep different subnets separate. However, this can cause issues when a group is reconfigured. If you do not have a specific security requirement to do otherwise, use the same allowlist on all members of a group. For more details, see [Section 20.6.4,](#page-88-0) ["Group Replication IP Address Permissions".](#page-88-0)

For host names, name resolution takes place only when a connection request is made by another server. A host name that cannot be resolved is not considered for allowlist validation, and a warning message is written to the error log. Forward-confirmed reverse DNS (FCrDNS) verification is carried out for resolved host names.

![](_page_148_Picture_4.jpeg)

#### **Warning**

Host names are inherently less secure than IP addresses in an allowlist. FCrDNS verification provides a good level of protection, but can be compromised by certain types of attack. Specify host names in your allowlist only when strictly necessary, and ensure that all components used for name resolution, such as DNS servers, are maintained under your control. You can also implement name resolution locally using the hosts file, to avoid the use of external components.

<span id="page-148-0"></span>• [group\\_replication\\_local\\_address](#page-148-0)

| Command-Line Format  | group-replication-local<br>address=value |
|----------------------|------------------------------------------|
| System Variable      | group_replication_local_address          |
| Scope                | Global                                   |
| Dynamic              | Yes                                      |
| SET_VAR Hint Applies | No                                       |
| Type                 | String                                   |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_local\\_address](#page-148-0) sets the network address which the member provides for connections from other members, specified as a host:port formatted string. This address must be reachable by all members of the group because it is used by the group communication engine for Group Replication (XCom, a Paxos variant) for TCP communication between remote XCom instances. If you are using the MySQL communication stack to establish group communication connections between members ([group\\_replication\\_communication\\_stack](#page-134-0) = MYSQL), the address must be one of the IP addresses and ports where MySQL Server is listening on, as specified by the bind\_address system variable for the server.

![](_page_148_Picture_11.jpeg)

#### **Warning**

Do not use this address to query or administer the databases on the member. This is not the SQL client connection host and port.

The address or host name that you specify in [group\\_replication\\_local\\_address](#page-148-0) is used by Group Replication as the unique identifier for a group member within the replication group. You can use the same port for all members of a replication group as long as the host names or IP addresses are all different, and you can use the same host name or IP address for all members as long as the ports are all different. The recommended port for [group\\_replication\\_local\\_address](#page-148-0)

is 33061. Note that the value you specify for this variable is not validated until the START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

The network address configured by [group\\_replication\\_local\\_address](#page-148-0) must be resolvable by all group members. For example, if each server instance is on a different machine with a fixed network address, you could use the IP address of the machine, such as 10.0.0.1. If you use a host name, you must use a fully qualified name, and ensure it is resolvable through DNS, correctly configured /etc/hosts files, or other name resolution processes. An IPv6 address must be specified in square brackets in order to distinguish the port number, for example:

```
group_replication_local_address= "[2001:db8:85a3:8d3:1319:8a2e:370:7348]:33061"
```

If a host name specified as the Group Replication local address for a server instance resolves to both an IPv4 and an IPv6 address, the IPv4 address is always used for Group Replication connections. For more information on Group Replication support for IPv6 networks and on replication groups with a mix of members using IPv4 and members using IPv6, see [Section 20.5.5, "Support For IPv6 And](#page-72-0) [For Mixed IPv6 And IPv4 Groups".](#page-72-0)

If you are using the XCom communication stack to establish group communication connections between members ([group\\_replication\\_communication\\_stack = XCOM](#page-134-0)), the address that you specify for each group member in [group\\_replication\\_local\\_address](#page-148-0) must be added to the list for the [group\\_replication\\_ip\\_allowlist](#page-146-1) system variable on the other servers in the replication group. When the XCom communication stack is in use for the group, the allowlist is used to control access to the group. When the MySQL communication stack is in use for the group, user authentication is used to control access to the group, and the allowlist is not used and is ignored if set. If any of the seed members for the group are listed in [group\\_replication\\_group\\_seeds](#page-145-1) with an IPv6 address when this member has an IPv4 [group\\_replication\\_local\\_address](#page-148-0), or the reverse, you must also set up and permit an alternative address for this member for the required protocol (or a host name that resolves to an address for that protocol). For more information, see [Section 20.6.4, "Group Replication IP Address Permissions"](#page-88-0).

<span id="page-149-0"></span>• [group\\_replication\\_member\\_expel\\_timeout](#page-149-0)

| Command-Line Format  | group-replication-member-expel<br>timeout=# |
|----------------------|---------------------------------------------|
| System Variable      | group_replication_member_expel_timeout      |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | Integer                                     |
| Default Value        | 5                                           |
| Minimum Value        | 0                                           |
| Maximum Value        | 3600                                        |
| Unit                 | seconds                                     |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. The current value of the system variable is read whenever Group Replication checks the timeout. It is not mandatory for all members of a group to have the same setting, but it is recommended in order to avoid unexpected expulsions.

[group\\_replication\\_member\\_expel\\_timeout](#page-149-0) specifies the period of time in seconds that a Group Replication group member waits after creating a suspicion, before expelling from the group the member suspected of having failed. The initial 5-second detection period before a suspicion is created does not count as part of this time. The value of

[group\\_replication\\_member\\_expel\\_timeout](#page-149-0) defaults to 5, meaning that a suspected member is liable for expulsion 5 seconds after the 5-second detection period.

Changing the value of [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) on a group member takes effect immediately for existing as well as future suspicions on that group member. You can therefore use this as a method to force a suspicion to time out and expel a suspected member, allowing changes to the group configuration. For more information, see [Section 20.7.7.1, "Expel Timeout"](#page-99-0).

Increasing the value of [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) can help to avoid unnecessary expulsions on slower or less stable networks, or in the case of expected transient network outages or machine slowdowns. If a suspect member becomes active again before the suspicion times out, it applies all the messages that were buffered by the remaining group members and enters ONLINE state, without operator intervention. You can specify a timeout value up to a maximum of 3600 seconds (1 hour). It is important to ensure that XCom's message cache is sufficiently large to contain the expected volume of messages in your specified time period, plus the initial 5-second detection period, otherwise members are unable to reconnect. You can adjust the cache size limit using the [group\\_replication\\_message\\_cache\\_size](#page-151-0) system variable. For more information, see [Section 20.7.6, "XCom Cache Management"](#page-96-1).

If the timeout is exceeded, the suspect member is liable for expulsion immediately after the suspicion times out. If the member is able to resume communications and receives a view where it is expelled, and the member has the [group\\_replication\\_autorejoin\\_tries](#page-130-0) system variable set to specify a number of auto-rejoin attempts, it proceeds to make the specified number of attempts to rejoin the group while in super read only mode. If the member does not have any auto-rejoin attempts specified, or if it has exhausted the specified number of attempts, it follows the action specified by the system variable [group\\_replication\\_exit\\_state\\_action](#page-138-0).

For more information on using the [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) setting, see [Section 20.7.7.1, "Expel Timeout"](#page-99-0). For alternative mitigation strategies to avoid unnecessary expulsions where this system variable is not available, see [Section 20.3.2, "Group Replication](#page-38-0) [Limitations"](#page-38-0).

<span id="page-150-0"></span>• [group\\_replication\\_member\\_weight](#page-150-0)

| Command-Line Format  | group-replication-member-weight=# |
|----------------------|-----------------------------------|
| System Variable      | group_replication_member_weight   |
| Scope                | Global                            |
| Dynamic              | Yes                               |
| SET_VAR Hint Applies | No                                |
| Type                 | Integer                           |
| Default Value        | 50                                |
| Minimum Value        | 0                                 |
| Maximum Value        | 100                               |
| Unit                 | percentage                        |

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. The system variable's current value is read when a failover situation occurs.

[group\\_replication\\_member\\_weight](#page-150-0) specifies a percentage weight that can be assigned to members to influence the chance of the member being elected as primary in the event of failover, for example when the existing primary leaves a single-primary group. Assign numeric weights to members to ensure that specific members are elected, for example during scheduled maintenance of the primary or to ensure certain hardware is prioritized in the event of failover.

For a group with members configured as follows:

- member-1: group\_replication\_member\_weight=30, server\_uuid=aaaa
- member-2: group\_replication\_member\_weight=40, server\_uuid=bbbb
- member-3: group\_replication\_member\_weight=40, server\_uuid=cccc
- member-4: group\_replication\_member\_weight=40, server\_uuid=dddd

during election of a new primary the members above would be sorted as member-2, member-3, member-4, and member-1. This results in member-2 being chosen as the new primary in the event of failover. For more information, see [Section 20.1.3.1, "Single-Primary Mode"](#page-14-1).

<span id="page-151-0"></span>• [group\\_replication\\_message\\_cache\\_size](#page-151-0)

| Command-Line Format              | group-replication-message-cache<br>size=# |
|----------------------------------|-------------------------------------------|
| System Variable                  | group_replication_message_cache_size      |
| Scope                            | Global                                    |
| Dynamic                          | Yes                                       |
| SET_VAR Hint Applies             | No                                        |
| Type                             | Integer                                   |
| Default Value                    | 1073741824 (1 GB)                         |
| Minimum Value                    | 134217728 (128 MB)                        |
| Maximum Value (64-bit platforms) | 18446744073709551615 (16 EiB)             |
| Maximum Value (32-bit platforms) | 315360004294967295 (4 GB)                 |
| Unit                             | bytes                                     |

This system variable should have the same value on all group members. The value of this system variable can be changed while Group Replication is running. The change takes effect on each group member after you stop and restart Group Replication on the member. During this process, the value of the system variable is permitted to differ between group members, but members might be unable to reconnect in the event of a disconnection.

[group\\_replication\\_message\\_cache\\_size](#page-151-0) sets the maximum amount of memory that is available for the message cache in the group communication engine for Group Replication (XCom). The XCom message cache holds messages (and their metadata) that are exchanged between the group members as a part of the consensus protocol. Among other functions, the message cache is used for recovery of missed messages by members that reconnect with the group after a period where they were unable to communicate with the other group members.

The [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) system variable determines the waiting period (up to an hour) that is allowed in addition to the initial 5-second detection period for members to return to the group rather than being expelled. The size of the XCom message cache should be set with reference to the expected volume of messages in this time period, so that it contains all the missed messages required for members to return successfully. The default is a 5-second waiting period after the 5-second detection period, for a total time period of 10 seconds.

Ensure that sufficient memory is available on your system for your chosen cache size limit, considering the size of the server's other caches and object pools. The default setting is 1073741824 bytes (1 GB). The minimum setting of 134217728 bytes (128 MB) enables deployment on a host that has a restricted amount of available memory, and good network connectivity to minimize the frequency and duration of transient losses of connectivity for group members. Note that the limit set

using [group\\_replication\\_message\\_cache\\_size](#page-151-0) applies only to the data stored in the cache, and the cache structures require an additional 50 MB of memory.

The cache size limit can be increased or reduced dynamically at runtime. If you reduce the cache size limit, XCom removes the oldest entries that have been decided and delivered until the current size is below the limit. Group Replication's Group Communication System (GCS) alerts you, by a warning message, when a message that is likely to be needed for recovery by a member that is currently unreachable is removed from the message cache. For more information on tuning the message cache size, see [Section 20.7.6, "XCom Cache Management".](#page-96-1)

<span id="page-152-0"></span>• [group\\_replication\\_paxos\\_single\\_leader](#page-152-0)

| Command-Line Format  | group-replication-paxos-single<br>leader[={OFF ON}] |
|----------------------|-----------------------------------------------------|
| System Variable      | group_replication_paxos_single_leader               |
| Scope                | Global                                              |
| Dynamic              | Yes                                                 |
| SET_VAR Hint Applies | No                                                  |
| Type                 | Boolean                                             |
| Default Value        | OFF                                                 |

![](_page_152_Picture_5.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_paxos\\_single\\_leader](#page-152-0) enables the group communication engine to operate with a single consensus leader when the group is in single-primary mode. With the default setting OFF, this behavior is disabled, and every member of the group is used as a leader, which is the behavior in releases before this system variable was available. When this variable is set to ON, the group communication engine can use a single leader to drive consensus. Operating with a single consensus leader improves performance and resilience in single-primary mode, particularly when some of the group's secondary members are currently unreachable. For more information, see [Section 20.7.3, "Single Consensus Leader".](#page-93-0)

In order for the group communication engine to use a single consensus leader, the group's communication protocol version must be MySQL 8.0.27 or later. Use group\_replication\_get\_communication\_protocol() to obtain the group's communication protocol version. If a lower version is in use, the group cannot use this behavior. You can use group\_replication\_set\_communication\_protocol() to set the communication protocol to a higher version if all group members support it. For more information, see [Section 20.5.1.4, "Setting](#page-47-0) [a Group's Communication Protocol Version".](#page-47-0)

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

The WRITE\_CONSENSUS\_SINGLE\_LEADER\_CAPABLE column of the Performance Schema table replication\_group\_communication\_information shows whether the group supports the use of a single leader, even if [group\\_replication\\_paxos\\_single\\_leader](#page-152-0) is currently set to OFF on the queried member. The column value is 1 if the group was started with [group\\_replication\\_paxos\\_single\\_leader](#page-152-0) set to ON, and its communication protocol version is MySQL 8.0.27 or later.

<span id="page-153-0"></span>• [group\\_replication\\_poll\\_spin\\_loops](#page-153-0)

| Command-Line Format              | group-replication-poll-spin<br>loops=# |
|----------------------------------|----------------------------------------|
| System Variable                  | group_replication_poll_spin_loops      |
| Scope                            | Global                                 |
| Dynamic                          | Yes                                    |
| SET_VAR Hint Applies             | No                                     |
| Type                             | Integer                                |
| Default Value                    | 0                                      |
| Minimum Value                    | 0                                      |
| Maximum Value (64-bit platforms) | 18446744073709551615                   |
| Maximum Value (32-bit platforms) | 4294967295                             |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_poll\\_spin\\_loops](#page-153-0) specifies the number of times the group communication thread waits for the communication engine mutex to be released before the thread waits for more incoming network messages.

<span id="page-153-1"></span>• [group\\_replication\\_preemptive\\_garbage\\_collection](#page-153-1)

| Command-Line Format  | group-replication-preemptive<br>garbage-collection[=ON OFF] |  |
|----------------------|-------------------------------------------------------------|--|
| System Variable      | group_replication_preemptive_garbage_collection             |  |
| Scope                | Global                                                      |  |
| Dynamic              | Yes                                                         |  |
| SET_VAR Hint Applies | No                                                          |  |
| Type                 | Boolean                                                     |  |
| Default Value        | OFF                                                         |  |

Enable preemptive garbage collection in single-primary mode (only), keeping only the write sets for those transactions that have not yet been committed in the database.

In single-primary mode it is possible to clean up write sets for a given transaction earlier than in multi-primary mode; this is because conflicts are detected and handled by the database lock manager in the server while transactions are executing; thus, the write sets are useful only for calculating dependencies between transactions, and not for conflict detection. This means that write sets can be cleaned up as soon as the transaction to which they belong is tracked in the Group Replication transaction dependency and conflict detection module.

The aggressive purging of write sets which is performed when group\_replication\_preemptive\_garbage\_collection is enabled has the following effects:

- Reduction in memory used to keep write sets in memory
- Reduction of the impact of lagging secondaries on the tracking of write sets on the primary

3724

• Reduction of the amount of time that the write set database lock is held per round of write set deletion, and thus a reduction of its impact on throughput

The value of group\_replication\_preemptive\_garbage\_collection can be changed only when Group Replication is not running, and has no effect on a group running in multi-primary mode. In addition, when this system variable is enabled, it is not possible to change between multi-primary mode and single-primary mode (see [Section 20.5.1.2, "Changing the Group Mode"](#page-46-0)).

group\_replication\_preemptive\_garbage\_collection must be set to the same value on all group members. A new joiner's group\_replication\_preemptive\_garbage\_collection value must be the same as those of all the group's current members, else it cannot join.

A group member running a version of MySQL previous to 8.4.0 sends no group\_replication\_preemptive\_garbage\_collection value; in such cases, the value is considered to be OFF.

<span id="page-154-1"></span>• [group\\_replication\\_preemptive\\_garbage\\_collection\\_rows\\_threshold](#page-154-1)

| Command-Line Format  | group-replication-preemptive<br>garbage-collection-rows-threshold=# |  |
|----------------------|---------------------------------------------------------------------|--|
| System Variable      | group_replication_preemptive_garbage_collection_rows_threshold      |  |
| Scope                | Global                                                              |  |
| Dynamic              | Yes                                                                 |  |
| SET_VAR Hint Applies | No                                                                  |  |
| Type                 | Integer                                                             |  |
| Default Value        | 100000                                                              |  |
| Minimum Value        | 10000                                                               |  |
| Maximum Value        | 100000000                                                           |  |

When preemptive garbage collection in single-primary mode is enabled ([group\\_replication\\_preemptive\\_garbage\\_collection](#page-153-1) is ON), this is the number of rows of certification information needed to trigger its use.

This variable has no effect on a group running in multi-primary mode.

<span id="page-154-0"></span>• [group\\_replication\\_recovery\\_compression\\_algorithms](#page-154-0)

| Command-Line Format  | group-replication-recovery<br>compression-algorithms=value |
|----------------------|------------------------------------------------------------|
| System Variable      | group_replication_recovery_compression_algorithms          |
| Scope                | Global                                                     |
| Dynamic              | Yes                                                        |
| SET_VAR Hint Applies | No                                                         |
| Type                 | Set                                                        |
| Default Value        | uncompressed                                               |
| Valid Values         | zlib                                                       |
|                      | zstd                                                       |
|                      | uncompressed                                               |

group\_replication\_recovery\_compression\_algorithms specifies the compression algorithms permitted for Group Replication distributed recovery connections for state

transfer from a donor's binary log. The available algorithms are the same as for the protocol\_compression\_algorithms system variable. For more information, see Section 6.2.8, "Connection Compression Control".

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

This setting does not apply if the server has been set up to support cloning (see [Section 20.5.4.2,](#page-62-0) ["Cloning for Distributed Recovery"\)](#page-62-0) and a remote cloning operation is used during distributed recovery. For this method of state transfer, the clone plugin's clone\_enable\_compression setting applies.

<span id="page-155-1"></span>• [group\\_replication\\_recovery\\_get\\_public\\_key](#page-155-1)

| Command-Line Format  | group-replication-recovery-get<br>public-key[={OFF ON}] |  |
|----------------------|---------------------------------------------------------|--|
| System Variable      | group_replication_recovery_get_public_key               |  |
| Scope                | Global                                                  |  |
| Dynamic              | Yes                                                     |  |
| SET_VAR Hint Applies | No                                                      |  |
| Type                 | Boolean                                                 |  |
| Default Value        | OFF                                                     |  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_get\\_public\\_key](#page-155-1) specifies whether to request from the source the public key required for RSA key pair-based password exchange. If [group\\_replication\\_recovery\\_public\\_key\\_path](#page-155-0) is set to a valid public key file, it takes precedence over [group\\_replication\\_recovery\\_get\\_public\\_key](#page-155-1). This variable applies if you are not using SSL for distributed recovery over the group\_replication\_recovery channel ([group\\_replication\\_recovery\\_use\\_ssl=ON](#page-161-0)), and the replication user account for Group Replication authenticates with the caching\_sha2\_password plugin (the default). For more details, see [Replication User With The Caching SHA-2 Authentication Plugin](#page-85-1).

<span id="page-155-0"></span>• [group\\_replication\\_recovery\\_public\\_key\\_path](#page-155-0)

| Command-Line Format  | group-replication-recovery-public<br>key-path=file_name |  |
|----------------------|---------------------------------------------------------|--|
| System Variable      | group_replication_recovery_public_key_path              |  |
| Scope                | Global                                                  |  |
| Dynamic              | Yes                                                     |  |
| SET_VAR Hint Applies | No                                                      |  |
| Type                 | File name                                               |  |
| Default Value        | empty string                                            |  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_public\\_key\\_path](#page-155-0) specifies the path name to a file containing a replica-side copy of the public key required by the source for RSA key pair-based password exchange. The file must be in PEM format. If [group\\_replication\\_recovery\\_public\\_key\\_path](#page-155-0) is set to a valid public key file, it takes precedence over [group\\_replication\\_recovery\\_get\\_public\\_key](#page-155-1). This variable applies

if you are not using SSL for distributed recovery over the group\_replication\_recovery channel (so [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) is set to OFF), and the replication user account for Group Replication authenticates with the caching\_sha2\_password plugin (the default) or the sha256\_password plugin (deprecated). (For sha256\_password, setting group\_replication\_recovery\_public\_key\_path applies only if MySQL was built using OpenSSL.) For more details, see [Replication User With The Caching SHA-2 Authentication Plugin.](#page-85-1)

<span id="page-156-2"></span>• [group\\_replication\\_recovery\\_reconnect\\_interval](#page-156-2)

| Command-Line Format  | group-replication-recovery<br>reconnect-interval=# |  |
|----------------------|----------------------------------------------------|--|
| System Variable      | group_replication_recovery_reconnect_interval      |  |
| Scope                | Global                                             |  |
| Dynamic              | Yes                                                |  |
| SET_VAR Hint Applies | No                                                 |  |
| Type                 | Integer                                            |  |
| Default Value        | 60                                                 |  |
| Minimum Value        | 0                                                  |  |
| Maximum Value        | 31536000                                           |  |
| Unit                 | seconds                                            |  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_reconnect\\_interval](#page-156-2) specifies the sleep time, in seconds, between reconnection attempts when no suitable donor was found in the group for distributed recovery.

<span id="page-156-1"></span>• [group\\_replication\\_recovery\\_retry\\_count](#page-156-1)

| group-replication-recovery-retry<br>count=# |
|---------------------------------------------|
| group_replication_recovery_retry_count      |
| Global                                      |
| Yes                                         |
| No                                          |
| Integer                                     |
| 10                                          |
| 0                                           |
| 31536000                                    |
|                                             |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_retry\\_count](#page-156-1) specifies the number of times that the member that is joining tries to connect to the available donors for distributed recovery before giving up.

<span id="page-156-0"></span>• [group\\_replication\\_recovery\\_ssl\\_ca](#page-156-0)

| Command-Line Format | group-replication-recovery-ssl<br>ca=value |
|---------------------|--------------------------------------------|
| System Variable     | group_replication_recovery_ssl_ca          |

| Scope                | Global |
|----------------------|--------|
| Dynamic              | Yes    |
| SET_VAR Hint Applies | No     |
| Type                 | String |

[group\\_replication\\_recovery\\_ssl\\_ca](#page-156-0) specifies the path to a file that contains a list of trusted SSL certificate authorities for distributed recovery connections. See [Section 20.6.2, "Securing Group](#page-82-0) [Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

If this server has been set up to support cloning (see [Section 20.5.4.2, "Cloning for Distributed](#page-62-0) [Recovery"\)](#page-62-0), and you have set [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) to ON, Group Replication automatically configures the setting for the clone SSL option clone\_ssl\_ca to match your setting for [group\\_replication\\_recovery\\_ssl\\_ca](#page-156-0).

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-157-1"></span>• [group\\_replication\\_recovery\\_ssl\\_capath](#page-157-1)

| Command-Line Format  | group-replication-recovery-ssl<br>capath=value |
|----------------------|------------------------------------------------|
| System Variable      | group_replication_recovery_ssl_capath          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_ssl\\_capath](#page-157-1) specifies the path to a directory that contains trusted SSL certificate authority certificates for distributed recovery connections. See [Section 20.6.2,](#page-82-0) ["Securing Group Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-157-0"></span>• [group\\_replication\\_recovery\\_ssl\\_cert](#page-157-0)

| Command-Line Format  | group-replication-recovery-ssl<br>cert=value |
|----------------------|----------------------------------------------|
| System Variable      | group_replication_recovery_ssl_cert          |
| Scope                | Global                                       |
| Dynamic              | Yes                                          |
| SET_VAR Hint Applies | No                                           |

| Type | String |
|------|--------|
|------|--------|

[group\\_replication\\_recovery\\_ssl\\_cert](#page-157-0) specifies the name of the SSL certificate file to use for establishing a secure connection for distributed recovery. See [Section 20.6.2, "Securing Group](#page-82-0) [Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

If this server has been set up to support cloning (see [Section 20.5.4.2, "Cloning for Distributed](#page-62-0) [Recovery"\)](#page-62-0), and you have set [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) to ON, Group Replication automatically configures the setting for the clone SSL option clone\_ssl\_cert to match your setting for [group\\_replication\\_recovery\\_ssl\\_cert](#page-157-0).

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-158-1"></span>• [group\\_replication\\_recovery\\_ssl\\_cipher](#page-158-1)

| Command-Line Format  | group-replication-recovery-ssl<br>cipher=value |
|----------------------|------------------------------------------------|
| System Variable      | group_replication_recovery_ssl_cipher          |
| Scope                | Global                                         |
| Dynamic              | Yes                                            |
| SET_VAR Hint Applies | No                                             |
| Type                 | String                                         |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_ssl\\_cipher](#page-158-1) specifies the list of permissible ciphers for SSL encryption. See [Section 20.6.2, "Securing Group Communication Connections with Secure Socket](#page-82-0) [Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-158-0"></span>• [group\\_replication\\_recovery\\_ssl\\_crl](#page-158-0)

| Command-Line Format  | group-replication-recovery-ssl<br>crl=value |
|----------------------|---------------------------------------------|
| System Variable      | group_replication_recovery_ssl_crl          |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | File name                                   |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group

([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-159-2"></span>• [group\\_replication\\_recovery\\_ssl\\_crlpath](#page-159-2)

| Command-Line Format  | group-replication-recovery-ssl<br>crlpath=value |
|----------------------|-------------------------------------------------|
| System Variable      | group_replication_recovery_ssl_crlpath          |
| Scope                | Global                                          |
| Dynamic              | Yes                                             |
| SET_VAR Hint Applies | No                                              |
| Type                 | Directory name                                  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_ssl\\_crlpath](#page-159-2) specifies the path to a directory that contains files containing certificate revocation lists. See [Section 20.6.2, "Securing Group Communication](#page-82-0) [Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group

([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-159-0"></span>• [group\\_replication\\_recovery\\_ssl\\_key](#page-159-0)

| Command-Line Format  | group-replication-recovery-ssl<br>key=value |
|----------------------|---------------------------------------------|
| System Variable      | group_replication_recovery_ssl_key          |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | String                                      |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_ssl\\_key](#page-159-0) specifies the name of the SSL key file to use for establishing a secure connection. See [Section 20.6.2, "Securing Group Communication Connections](#page-82-0) [with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

If this server has been set up to support cloning (see [Section 20.5.4.2, "Cloning for Distributed](#page-62-0) [Recovery"\)](#page-62-0), and you have set [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) to ON, Group Replication automatically configures the setting for the clone SSL option clone\_ssl\_key to match your setting for [group\\_replication\\_recovery\\_ssl\\_key](#page-159-0).

When the MySQL communication stack is in use for the group

([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-159-1"></span>• [group\\_replication\\_recovery\\_ssl\\_verify\\_server\\_cert](#page-159-1)

| Command-Line Format  | group-replication-recovery-ssl<br>verify-server-cert[={OFF ON}] |  |
|----------------------|-----------------------------------------------------------------|--|
| System Variable      | group_replication_recovery_ssl_verify_server_cert               |  |
| Scope                | Global                                                          |  |
| Dynamic              | Yes                                                             |  |
| SET_VAR Hint Applies | No                                                              |  |
| Type                 | Boolean                                                         |  |
| Default Value        | OFF                                                             |  |

[group\\_replication\\_recovery\\_ssl\\_verify\\_server\\_cert](#page-159-1) specifies whether the distributed recovery connection should check the server's Common Name value in the certificate sent by the donor. See [Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer](#page-82-0) [\(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-160-1"></span>• [group\\_replication\\_recovery\\_tls\\_ciphersuites](#page-160-1)

| Command-Line Format  | group-replication-recovery-tls<br>ciphersuites=value |  |
|----------------------|------------------------------------------------------|--|
| System Variable      | group_replication_recovery_tls_ciphersuites          |  |
| Scope                | Global                                               |  |
| Dynamic              | Yes                                                  |  |
| SET_VAR Hint Applies | No                                                   |  |
| Type                 | String                                               |  |
| Default Value        | NULL                                                 |  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_tls\\_ciphersuites](#page-160-1) specifies a colon-separated list of one or more permitted ciphersuites when TLSv1.3 is used for connection encryption for the distributed recovery connection, and this server instance is the client in the distributed recovery connection, that is, the joining member. If this system variable is set to NULL when TLSv1.3 is used (which is the default if you do not set the system variable), the ciphersuites that are enabled by default are allowed, as listed in Section 8.3.2, "Encrypted Connection TLS Protocols and Ciphers". If this system variable is set to the empty string, no cipher suites are allowed, and TLSv1.3 is therefore not used. See [Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer \(SSL\)",](#page-82-0) for information on configuring SSL for distributed recovery.

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

<span id="page-160-0"></span>• [group\\_replication\\_recovery\\_tls\\_version](#page-160-0)

| Command-Line Format | group-replication-recovery-tls |
|---------------------|--------------------------------|
|                     | version=value                  |

| System Variable      | group_replication_recovery_tls_version |
|----------------------|----------------------------------------|
| Scope                | Global                                 |
| Dynamic              | Yes                                    |
| SET_VAR Hint Applies | No                                     |
| Type                 | String                                 |
| Default Value        | TLSv1.2,TLSv1.3                        |

[group\\_replication\\_recovery\\_tls\\_version](#page-160-0) specifies a comma-separated list of one or more permitted TLS protocols for connection encryption when this server instance is the client in the distributed recovery connection, that is, the joining member. The group members involved in each distributed recovery connection as the client (joining member) and server (donor) negotiate the highest protocol version that they are both set up to support.

When the MySQL communication stack is in use for the group ([group\\_replication\\_communication\\_stack = MYSQL](#page-134-0)), this setting is used for the TLS/SSL configuration for group communication connections, as well as for distributed recovery connections.

The default is "TLSv1.2,TLSv1.3". Ensure that the specified protocol versions are contiguous, with no versions numbers skipped from the middle of the sequence.

![](_page_161_Picture_6.jpeg)

#### **Important**

- Support for the TLSv1 and TLSv1.1 connection protocols was deprecated in and later removed from MySQL in MySQL 8.0. See Removal of Support for the TLSv1 and TLSv1.1 Protocols for more information.
- Support for the TLSv1.3 protocol is available in MySQL 8.4, provided that MySQL was compiled using OpenSSL 1.1.1. The server checks the version of OpenSSL at startup, and if it is lower than 1.1.1, TLSv1.3 is removed from the default value for the system variable. In that case, the default is TLSv1.2.
- Group Replication supports TLSv1.3 with support for ciphersuite selection. See [Section 20.6.2, "Securing Group Communication Connections with](#page-82-0) [Secure Socket Layer \(SSL\)"](#page-82-0) for more information.

See [Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

<span id="page-161-0"></span>• [group\\_replication\\_recovery\\_use\\_ssl](#page-161-0)

| Command-Line Format  | group-replication-recovery-use<br>ssl[={OFF ON}] |
|----------------------|--------------------------------------------------|
| System Variable      | group_replication_recovery_use_ssl               |
| Scope                | Global                                           |
| Dynamic              | Yes                                              |
| SET_VAR Hint Applies | No                                               |
| Type                 | Boolean                                          |

| Default Value | OFF |  |
|---------------|-----|--|
|---------------|-----|--|

[group\\_replication\\_recovery\\_use\\_ssl](#page-161-0) specifies whether Group Replication distributed recovery connections between group members should use SSL or not. See [Section 20.6.2,](#page-82-0) ["Securing Group Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for distributed recovery.

If this server has been set up to support cloning (see [Section 20.5.4.2, "Cloning for Distributed](#page-62-0) [Recovery"\)](#page-62-0), and you set this option to ON, Group Replication uses SSL for remote cloning operations as well as for state transfer from a donor's binary log. If you set this option to OFF, Group Replication does not use SSL for remote cloning operations.

<span id="page-162-1"></span>• [group\\_replication\\_recovery\\_zstd\\_compression\\_level](#page-162-1)

| Command-Line Format  | group-replication-recovery-zstd<br>compression-level=# |
|----------------------|--------------------------------------------------------|
| System Variable      | group_replication_recovery_zstd_compression_level      |
| Scope                | Global                                                 |
| Dynamic              | Yes                                                    |
| SET_VAR Hint Applies | No                                                     |
| Type                 | Integer                                                |
| Default Value        | 3                                                      |
| Minimum Value        | 1                                                      |
| Maximum Value        | 22                                                     |
|                      |                                                        |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_recovery\\_zstd\\_compression\\_level](#page-162-1) specifies the compression level to use for Group Replication distributed recovery connections that use the zstd compression algorithm. The permitted levels are from 1 to 22, with larger values indicating increasing levels of compression. The default zstd compression level is 3. For distributed recovery connections that do not use zstd compression, this variable has no effect.

For more information, see Section 6.2.8, "Connection Compression Control".

<span id="page-162-0"></span>• [group\\_replication\\_single\\_primary\\_mode](#page-162-0)

| Command-Line Format  | group-replication-single-primary<br>mode[={OFF ON}] |
|----------------------|-----------------------------------------------------|
| System Variable      | group_replication_single_primary_mode               |
| Scope                | Global                                              |
| Dynamic              | Yes                                                 |
| SET_VAR Hint Applies | No                                                  |
| Type                 | Boolean                                             |
| Default Value        | ON                                                  |

![](_page_162_Picture_12.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_single\\_primary\\_mode](#page-162-0) instructs the group to pick a single server automatically to be the one that handles read/write workload. This server is the primary and all others are secondaries.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

Setting this variable ON causes any setting for [group\\_replication\\_auto\\_increment\\_increment](#page-129-0) to be ignored.

Use the functions group\_replication\_switch\_to\_single\_primary\_mode() and group\_replication\_switch\_to\_multi\_primary\_mode() to change the value of this system variable while the group is still running. For more information, see [Section 20.5.1.2, "Changing the](#page-46-0) [Group Mode".](#page-46-0)

<span id="page-163-0"></span>• [group\\_replication\\_ssl\\_mode](#page-163-0)

| Command-Line Format  | group-replication-ssl-mode=value |
|----------------------|----------------------------------|
| System Variable      | group_replication_ssl_mode       |
| Scope                | Global                           |
| Dynamic              | Yes                              |
| SET_VAR Hint Applies | No                               |
| Type                 | Enumeration                      |
| Default Value        | DISABLED                         |
| Valid Values         | DISABLED                         |
|                      | REQUIRED                         |
|                      | VERIFY_CA                        |
|                      | VERIFY_IDENTITY                  |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_ssl\\_mode](#page-163-0) sets the security state of group communication connections between Group Replication members. The possible values are as follows:

DISABLED Establish an unencrypted connection (the default).

REQUIRED Establish a secure connection if the server supports secure

connections.

VERIFY\_CA Like REQUIRED, but additionally verify the server TLS certificate

against the configured Certificate Authority (CA) certificates.

VERIFY\_IDENTITY Like VERIFY\_CA, but additionally verify that the server certificate matches the host to which the connection is attempted.

This variable should have the same value on all members of the group; otherwise, new members may be unable to join.

See [Section 20.6.2, "Securing Group Communication Connections with Secure Socket Layer \(SSL\)"](#page-82-0) for information on configuring SSL for group communication.

<span id="page-164-0"></span>• [group\\_replication\\_start\\_on\\_boot](#page-164-0)

| Command-Line Format  | group-replication-start-on<br>boot[={OFF ON}] |
|----------------------|-----------------------------------------------|
| System Variable      | group_replication_start_on_boot               |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Boolean                                       |
| Default Value        | ON                                            |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_start\\_on\\_boot](#page-164-0) specifies whether the server should start Group Replication automatically (ON) or not (OFF) during server start. When you set this option to ON, Group Replication restarts automatically after a remote cloning operation is used for distributed recovery.

To start Group Replication automatically during server start, the user credentials for distributed recovery must be stored in the replication metadata repositories on the server using the CHANGE REPLICATION SOURCE TO statement. If you prefer to specify user credentials as part of START GROUP\_REPLICATION, which stores the user credentials in memory only, ensure that [group\\_replication\\_start\\_on\\_boot](#page-164-0) is set to OFF.

<span id="page-164-1"></span>• [group\\_replication\\_tls\\_source](#page-164-1)

| Command-Line Format  | group-replication-tls-source=value |
|----------------------|------------------------------------|
| System Variable      | group_replication_tls_source       |
| Scope                | Global                             |
| Dynamic              | Yes                                |
| SET_VAR Hint Applies | No                                 |
| Type                 | Enumeration                        |
| Default Value        | mysql_main                         |
| Valid Values         | mysql_main                         |
|                      | mysql_admin                        |

The value of this system variable can be changed while Group Replication is running, but the change takes effect only after you stop and restart Group Replication on the group member.

[group\\_replication\\_tls\\_source](#page-164-1) specifies the source of TLS material for Group Replication.

<span id="page-165-0"></span>• [group\\_replication\\_transaction\\_size\\_limit](#page-165-0)

| Command-Line Format  | group-replication-transaction<br>size-limit=# |
|----------------------|-----------------------------------------------|
| System Variable      | group_replication_transaction_size_limit      |
| Scope                | Global                                        |
| Dynamic              | Yes                                           |
| SET_VAR Hint Applies | No                                            |
| Type                 | Integer                                       |
| Default Value        | 150000000                                     |
| Minimum Value        | 0                                             |
| Maximum Value        | 2147483647                                    |
| Unit                 | bytes                                         |

This system variable should have the same value on all group members. The value of this system variable can be changed while Group Replication is running. The change takes effect immediately on the group member, and applies from the next transaction started on that member. During this process, the value of the system variable is permitted to differ between group members, but some transactions might be rejected.

[group\\_replication\\_transaction\\_size\\_limit](#page-165-0) configures the maximum transaction size in bytes which the replication group accepts. Transactions larger than this size are rolled back by the receiving member and are not broadcast to the group. Large transactions can cause problems for a replication group in terms of memory allocation, which can cause the system to slow down, or in terms of network bandwidth consumption, which can cause a member to be suspected of having failed because it is busy processing the large transaction.

When this system variable is set to 0 there is no limit to the size of transactions the group accepts. The default is 150000000 bytes (approximately 143 MB). Adjust the value of this system variable depending on the maximum message size that you need the group to tolerate, bearing in mind that the time taken to process a transaction is proportional to its size. The value of [group\\_replication\\_transaction\\_size\\_limit](#page-165-0) should be the same on all group members. For further mitigation strategies for large transactions, see [Section 20.3.2, "Group Replication](#page-38-0) [Limitations"](#page-38-0).

<span id="page-165-1"></span>• [group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1)

| Command-Line Format  | group-replication-unreachable<br>majority-timeout=# |  |
|----------------------|-----------------------------------------------------|--|
| System Variable      | group_replication_unreachable_majority_timeout      |  |
| Scope                | Global                                              |  |
| Dynamic              | Yes                                                 |  |
| SET_VAR Hint Applies | No                                                  |  |
| Type                 | Integer                                             |  |
| Default Value        | 0                                                   |  |
| Minimum Value        | 0                                                   |  |
| Maximum Value        | 31536000                                            |  |
|                      |                                                     |  |

| Unit | seconds |
|------|---------|
|------|---------|

The value of this system variable can be changed while Group Replication is running, and the change takes effect immediately. The current value of the system variable is read when an issue occurs that means the behavior is needed.

[group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1) specifies a number of seconds for which members that suffer a network partition and cannot connect to the majority wait before leaving the group. In a group of 5 servers (S1,S2,S3,S4,S5), if there is a disconnection between (S1,S2) and (S3,S4,S5) there is a network partition. The first group (S1,S2) is now in a minority because it cannot contact more than half of the group. While the majority group (S3,S4,S5) remains running, the minority group waits for the specified time for a network reconnection. For a detailed description of this scenario, see [Section 20.7.8, "Handling a Network Partition and Loss of Quorum".](#page-103-0)

By default, [group\\_replication\\_unreachable\\_majority\\_timeout](#page-165-1) is set to 0, which means that members that find themselves in a minority due to a network partition wait forever to leave the group. If you set a timeout, when the specified time elapses, all pending transactions processed by the minority are rolled back, and the servers in the minority partition move to the ERROR state. If a member has the [group\\_replication\\_autorejoin\\_tries](#page-130-0) system variable set to specify a number of auto-rejoin attempts, it proceeds to make the specified number of attempts to rejoin the group while in super read only mode. If the member does not have any auto-rejoin attempts specified, or if it has exhausted the specified number of attempts, it follows the action specified by the system variable [group\\_replication\\_exit\\_state\\_action](#page-138-0).

![](_page_166_Picture_5.jpeg)

### **Warning**

When you have a symmetric group, with just two members for example (S0,S2), if there is a network partition and there is no majority, after the configured timeout all members enter the ERROR state.

For more information on using this option, see [Section 20.7.7.2, "Unreachable Majority Timeout"](#page-100-0).

<span id="page-166-0"></span>• [group\\_replication\\_view\\_change\\_uuid](#page-166-0)

| Command-Line Format  | group-replication-view-change<br>uuid=value |
|----------------------|---------------------------------------------|
| Deprecated           | Yes                                         |
| System Variable      | group_replication_view_change_uuid          |
| Scope                | Global                                      |
| Dynamic              | Yes                                         |
| SET_VAR Hint Applies | No                                          |
| Type                 | String                                      |
| Default Value        | AUTOMATIC                                   |

![](_page_166_Picture_11.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_view\\_change\\_uuid](#page-166-0) specifies an alternative UUID to use as the UUID part of the identifier in the GTIDs for view change events generated by the group. The alternative UUID makes these internally generated transactions easy to distinguish from transactions received by the group from clients. This can be useful if your setup allows for failover between groups, and you need to identify and discard transactions that were specific to the backup group. The default value for this system variable is AUTOMATIC, meaning that the GTIDs for view change events use the group name specified by the [group\\_replication\\_group\\_name](#page-145-0) system variable, as transactions from clients

do. Group members at a release that does not have this system variable are treated as having the value AUTOMATIC.

The alternative UUID must be different from the group name specified by the [group\\_replication\\_group\\_name](#page-145-0) system variable, and it must be different from the server UUID of any group member. It must also be different from any UUIDs used in the GTIDs that are applied to anonymous transactions on replication channels anywhere in this topology, using the ASSIGN\_GTIDS\_TO\_ANONYMOUS\_TRANSACTIONS option of the CHANGE REPLICATION SOURCE TO statement.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-131-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 20.5.2, "Restarting a Group".](#page-50-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

Logging of view change events is replaced by sharing of recovery metadata; thus, this variable is deprecated, and subject to removal in a future version of MySQL.

# <span id="page-167-0"></span>**20.9.2 Group Replication Status Variables**

This section describes the status variables providing information about Group Replication.

The status variables and their meanings are listed here:

<span id="page-167-1"></span>• [Gr\\_all\\_consensus\\_proposals\\_count](#page-167-1)

Sum of all proposals that were initiated and terminated on this node.

<span id="page-167-2"></span>• [Gr\\_all\\_consensus\\_time\\_sum](#page-167-2)

The total elapsed time for all consensus rounds started and finished on this node. By comparing this value with [Gr\\_all\\_consensus\\_proposals\\_count](#page-167-1), we can determine whether a given consensus time has an upward trend, which may signal a problem.

<span id="page-167-3"></span>• [Gr\\_certification\\_garbage\\_collector\\_count](#page-167-3)

The number of times certification garbage collection has been run.

<span id="page-167-4"></span>• [Gr\\_certification\\_garbage\\_collector\\_time\\_sum](#page-167-4)

Sum of the times in microseconds taken by certification garbage collection.

<span id="page-167-5"></span>• [Gr\\_consensus\\_bytes\\_received\\_sum](#page-167-5)

The sum of all socket-level bytes received from group nodes having this node as a destination.

<span id="page-167-6"></span>• [Gr\\_consensus\\_bytes\\_sent\\_sum](#page-167-6)

Sum of all socket-level bytes originating on this node that were sent to all (other) group nodes. More data is reported here than for sent messages, since they are multiplexed and sent to each member.

For example, if we have a group with three members and we send a 100-byte message, this value accounts for 300 bytes, since we send 100 bytes to each node.

<span id="page-167-7"></span>• [Gr\\_control\\_messages\\_sent\\_count](#page-167-7)

Number of control messages sent by this member.

<span id="page-168-0"></span>• [Gr\\_control\\_messages\\_sent\\_bytes\\_sum](#page-168-0)

Sum of the number of bytes used in control messages sent by this member; this is the on-the-wire size.

<span id="page-168-1"></span>• [Gr\\_control\\_messages\\_sent\\_roundtrip\\_time\\_sum](#page-168-1)

Sum of the round-trip times in microseconds for control messages sent by this member; a round trip is measured between the sending and the delivery of the message on the sender. This should provide the time between sending and delivery of control messages for the majority of the members of the group, including the sender.

<span id="page-168-2"></span>• [Gr\\_data\\_messages\\_sent\\_bytes\\_sum](#page-168-2)

Sum in bytes used by data messages sent by this member; this is the on-the-wire size.

<span id="page-168-3"></span>• [Gr\\_data\\_messages\\_sent\\_count](#page-168-3)

This is the nmber of transaction data messages sent by this member.

<span id="page-168-4"></span>• [Gr\\_data\\_messages\\_sent\\_roundtrip\\_time\\_sum](#page-168-4)

Sum of the round-trip times in microseconds for data messages sent by this member; a round trip is measured between the sending and the delivery of the message on the sender. This should provide the time between sending and delivery of data messages for the majority of the members of the group, including the sender.

<span id="page-168-5"></span>• [Gr\\_empty\\_consensus\\_proposals\\_count](#page-168-5)

Sum of all empty proposal rounds that were initiated and terminated on this node.

<span id="page-168-6"></span>• [Gr\\_extended\\_consensus\\_count](#page-168-6)

The number of full 3-phase rounds that this node has initiated. If this number grows over time, it means that at least one node is having problems answering to proposals, either due to something it to run slowly, or to network issues. Use this value together with the count\_member\_failure\_suspicions column of the Performance Schema replication\_group\_communication\_information table when diagnosing such issues.

<span id="page-168-7"></span>• [Gr\\_last\\_consensus\\_end\\_timestamp](#page-168-7)

The time when the last consensus proposal was approved, in a timestamp format. This can be an indicator whether the group is making slow progress, or has halted.

<span id="page-168-8"></span>• [Gr\\_total\\_messages\\_sent\\_count](#page-168-8)

The number of high-level messages sent by this node to the group. These are the messages received from the API for proposing to the group. The XCom batching mechanism batches these messages and proposes them all together. The value shown for this variable reflects the number of messages prior to batching.

<span id="page-168-9"></span>• [Gr\\_transactions\\_consistency\\_after\\_sync\\_count](#page-168-9)

Number of transactions on secondaries that waited to start, while waiting for transactions from the primary with [group\\_replication\\_consistency](#page-136-0) equal to AFTER or BEFORE\_AND\_AFTER to be committed.

<span id="page-168-10"></span>• [Gr\\_transactions\\_consistency\\_after\\_sync\\_time\\_sum](#page-168-10)

Sum of the times in microseconds that transactions on secondaries waited on transactions from the primary with [group\\_replication\\_consistency](#page-136-0) equal to AFTER or BEFORE\_AND\_AFTER to be committed, before starting.

<span id="page-169-1"></span>• [Gr\\_transactions\\_consistency\\_after\\_termination\\_count](#page-169-1)

The number of transactions executed with [group\\_replication\\_consistency](#page-136-0) equal to AFTER or BEFORE\_AND\_AFTER.

<span id="page-169-2"></span>• [Gr\\_transactions\\_consistency\\_after\\_termination\\_time\\_sum](#page-169-2)

Sum of the time in microseconds between delivery of the transaction executed with [group\\_replication\\_consistency](#page-136-0) equal to AFTER or BEFORE\_AND\_AFTER, and acknowledgement by the other group members that the transaction is prepared.

This value does not include transaction send roundtrip time.

<span id="page-169-3"></span>• [Gr\\_transactions\\_consistency\\_before\\_begin\\_count](#page-169-3)

Number of transactions executed with [group\\_replication\\_consistency](#page-136-0) equal to BEFORE or BEFORE\_AND\_AFTER.

<span id="page-169-4"></span>• [Gr\\_transactions\\_consistency\\_before\\_begin\\_time\\_sum](#page-169-4)

Sum of the time in microseconds that the member waited until its group replication applier channel was consumed before executing the transaction with [group\\_replication\\_consistency](#page-136-0) equal to BEFORE or BEFORE\_AND\_AFTER.

These status variables all have member scope since they reflect what the local member observes. They are reset on group bootstrap, joining of a new member, automatic rejoin of an existing member, and server restart.

# <span id="page-169-0"></span>**20.10 Frequently Asked Questions**

This section provides answers to frequently asked questions.

# **What is the maximum number of MySQL servers in a group?**

A group can consist of maximum 9 servers. Attempting to add another server to a group with 9 members causes the request to join to be refused. This limit has been identified from testing and benchmarking as a safe boundary where the group performs reliably on a stable local area network.

# **How are servers in a group connected?**

Servers in a group connect to the other servers in the group by opening a peer-topeer TCP connection. These connections are only used for internal communication and message passing between servers in the group. This address is configured by the [group\\_replication\\_local\\_address](#page-148-0) variable.

# **What is the group\_replication\_bootstrap\_group option used for?**

The bootstrap flag instructs a member to create a group and act as the initial seed server. The second member joining the group needs to ask the member that bootstrapped the group to dynamically change the configuration in order for it to be added to the group.

A member needs to bootstrap the group in two scenarios. When the group is originally created, or when shutting down and restarting the entire group.

# **How do I set credentials for the distributed recovery process?**

You can set the user credentials permanently as the credentials for the group\_replication\_recovery channel, using a CHANGE REPLICATION SOURCE TO statement. You can specify them in the START GROUP\_REPLICATION statement each time Group Replication is started.

User credentials set using CHANGE REPLICATION SOURCE TO are stored in plain text in the replication metadata repositories on the server, but user credentials specified on START GROUP\_REPLICATION are saved in memory only, and are removed by a STOP GROUP\_REPLICATION statement or server shutdown. Using START GROUP\_REPLICATION to specify the user credentials therefore helps to secure the Group Replication servers against unauthorized access. However, this method is not compatible with starting Group Replication automatically, as specified by the [group\\_replication\\_start\\_on\\_boot](#page-164-0) system variable. For more information, see [Section 20.6.3.1,](#page-85-0) ["Secure User Credentials for Distributed Recovery".](#page-85-0)

# **Can I scale-out my write-load using Group Replication?**

Not directly, but MySQL Group replication is a shared nothing full replication solution, where all servers in the group replicate the same amount of data. Therefore if one member in the group writes N bytes to storage as the result of a transaction commit operation, then roughly N bytes are written to storage on other members as well, because the transaction is replicated everywhere.

However, given that other members do not have to do the same amount of processing that the original member had to do when it originally executed the transaction, they apply the changes faster. Transactions are replicated in a format that is used to apply row transformations only, without having to re-execute transactions again (row-based format).

Furthermore, given that changes are propagated and applied in row-based format, this means that they are received in an optimized and compact format, and likely reducing the number of IO operations required when compared to the originating member.

To summarize, you can scale-out processing, by spreading conflict free transactions throughout different members in the group. And you can likely scale-out a small fraction of your IO operations, since remote servers receive only the necessary changes to read-modify-write changes to stable storage.

# **Does Group Replication require more network bandwidth and CPU, when compared to simple replication and under the same workload?**

Some additional load is expected because servers need to be constantly interacting with each other for synchronization purposes. It is difficult to quantify how much more data. It also depends on the size of the group (three servers puts less stress on the bandwidth requirements than nine servers in the group).

Also the memory and CPU footprint are larger, because more complex work is done for the server synchronization part and for the group messaging.

# **Can I deploy Group Replication across wide-area networks?**

Yes, but the network connection between each member must be reliable and have suitable performance. Low latency, high bandwidth network connections are a requirement for optimal performance.

If network bandwidth alone is an issue, then [Section 20.7.4, "Message Compression"](#page-94-0) can be used to lower the bandwidth required. However, if the network drops packets, leading to re-transmissions and higher end-to-end latency, throughput and latency are both negatively affected.

![](_page_170_Picture_14.jpeg)

#### **Warning**

When the network round-trip time (RTT) between any group members is 5 seconds or more you could encounter problems as the built-in failure detection mechanism could be incorrectly triggered.

# **Do members automatically rejoin a group in case of temporary connectivity problems?**

This depends on the reason for the connectivity problem. If the connectivity problem is transient and the reconnection is quick enough that the failure detector is not aware of it, then the server may not be removed from the group. If it is a "long" connectivity problem, then the failure detector eventually suspects a problem and the server is removed from the group.

Two settings are available to increase the chances of a member remaining in or rejoining a group:

- [group\\_replication\\_member\\_expel\\_timeout](#page-149-0) increases the time between the creation of a suspicion (which happens after an initial 5-second detection period) and the expulsion of the member. You can set a waiting period of up to 1 hour. A waiting period of 5 seconds is set by default.
- [group\\_replication\\_autorejoin\\_tries](#page-130-0) makes a member try to rejoin the group after an expulsion or unreachable majority timeout. The member makes the specified number of auto-rejoin attempts five minutes apart. This feature is active by default; the member makes three auto-rejoin attempts.

If a server is expelled from the group and any auto-rejoin attempts do not succeed, you need to join it back again. In other words, after a server is removed explicitly from the group you need to rejoin it manually (or have a script doing it automatically).

# **When is a member excluded from a group?**

If the member becomes silent, the other members remove it from the group configuration. In practice this may happen when the member has crashed or there is a network disconnection.

The failure is detected after a given timeout elapses for a given member and a new configuration without the silent member in it is created.

# **What happens when one node is significantly lagging behind?**

There is no method for defining policies for when to expel members automatically from the group. You need to find out why a member is lagging behind and fix that or remove the member from the group. Otherwise, if the server is so slow that it triggers the flow control, then the entire group slows down as well. The flow control can be configured according to the your needs.

# **Upon suspicion of a problem in the group, is there a special member responsible for triggering a reconfiguration?**

No, there is no special member in the group in charge of triggering a reconfiguration.

Any member can suspect that there is a problem. All members need to (automatically) agree that a given member has failed. One member is in charge of expelling it from the group, by triggering a reconfiguration. Which member is responsible for expelling the member is not something you can control or set.

# **Can I use Group Replication for sharding?**

Group Replication is designed to provide highly available replica sets; data and writes are duplicated on each member in the group. For scaling beyond what a single system can provide, you need an orchestration and sharding framework built around a number of Group Replication sets, where each replica set maintains and manages a given shard or partition of your total dataset. This type of setup, often called a "sharded cluster", allows you to scale reads and writes linearly and without limit.

# **How do I use Group Replication with SELinux?**

If SELinux is enabled, which you can verify using sestatus -v, then you need to enable the use of the Group Replication communication port. See Setting the TCP Port Context for Group Replication.

# **How do I use Group Replication with iptables?**

If iptables is enabled, then you need to open up the Group Replication port for communication between the machines. To see the current rules in place on each machine, issue iptables -L. Assuming the port configured is 33061, enable communication over the necessary port by issuing iptables -A INPUT -p tcp --dport 33061 -j ACCEPT.

# **How do I recover the relay log for a replication channel used by a group member?**

The replication channels used by Group Replication behave in the same way as replication channels used in asynchronous source to replica replication, and as such rely on the relay log. In the event of a change of the relay\_log variable, or when the option is not set and the host name changes, there is a chance of errors. See Section 19.2.4.1, "The Relay Log" for a recovery procedure in this situation. Alternatively, another way of fixing the issue specifically in Group Replication is to issue a STOP GROUP\_REPLICATION statement and then a START GROUP\_REPLICATION statement to restart the instance. The Group Replication plugin creates the group\_replication\_applier channel again.

# **Why does Group Replication use two bind addresses?**

Group Replication uses two bind addresses in order to split network traffic between the SQL address, used by clients to communicate with the member, and the [group\\_replication\\_local\\_address](#page-148-0), used internally by the group members to communicate. For example, assume a server with two network interfaces assigned to the network addresses 203.0.113.1 and 198.51.100.179. In such a situation you could use 203.0.113.1:33061 for the internal group network address by setting [group\\_replication\\_local\\_address=203.0.113.1:33061](#page-148-0). Then you could use 198.51.100.179 for hostname and 3306 for the port. Client SQL applications would then connect to the member at 198.51.100.179:3306. This enables you to configure different rules on the different networks. Similarly, the internal group communication can be separated from the network connection used for client applications, for increased security.

# **How does Group Replication use network addresses and hostnames?**

Group Replication uses network connections between members and therefore its functionality is directly impacted by how you configure hostnames and ports. For example, Group Replication's distributed recovery process creates a connection to an existing group member using the server's hostname and port. When a member joins a group it receives the group membership information, using the network address information that is listed at performance\_schema.replication\_group\_members. One of the members listed in that table is selected as the donor of the missing data from the group to the joining member.

This means that any value you configure using a hostname, such as the SQL network address or the group seeds address, must be a fully qualified name and resolvable by each member of the group. You can ensure this for example through DNS, or correctly configured /etc/hosts files, or other local processes. If a you want to configure the MEMBER\_HOST value on a server, specify it using the - report-host option on the server before joining it to the group.

![](_page_172_Picture_10.jpeg)

#### **Important**

The assigned value is used directly and is not affected by the skip\_name\_resolve system variable.

To configure MEMBER\_PORT on a server, specify it using the report\_port system variable.

# **Why did the auto increment setting on the server change?**

When Group Replication is started on a server, the value of auto\_increment\_increment is changed to the value of [group\\_replication\\_auto\\_increment\\_increment](#page-129-0), which defaults to 7, and the value of auto\_increment\_offset is changed to the server ID. The changes are reverted when Group Replication is stopped. These settings avoid the selection of duplicate auto-increment values for writes on group members, which causes rollback of transactions. The default auto increment value of 7 for Group Replication represents a balance between the number of usable values and the permitted maximum size of a replication group (9 members).

The changes are made and reverted only if auto\_increment\_increment and auto\_increment\_offset each has its default value (1 in both cases). If their values have already been modified from the default, Group Replication does not alter them. The system variables are also not modified when Group Replication is in single-primary mode, where only one server writes.

# **How do I find the primary?**

If the group is operating in single-primary mode, it can be useful to find out which member is the primary. See [Finding the Primary](#page-16-1)

# Chapter 21 MySQL Shell

MySQL Shell is an advanced client and code editor for MySQL Server. In addition to the provided SQL functionality, similar to mysql, MySQL Shell provides scripting capabilities for JavaScript and Python and includes APIs for working with MySQL. MySQL Shell is a component that you can install separately.

The following discussion briefly describes MySQL Shell's capabilities. For more information, see the MySQL Shell manual, available at [https://dev.mysql.com/doc/mysql-shell/en/.](https://dev.mysql.com/doc/mysql-shell/en/)

MySQL Shell includes the following APIs implemented in JavaScript and Python which you can use to develop code that interacts with MySQL.

- The X DevAPI enables developers to work with both relational and document data when MySQL Shell is connected to a MySQL server using the X Protocol. This enables you to use MySQL as a Document Store, sometimes referred to as "using NoSQL". For more information, see [Chapter 22,](#page-176-0) [Using MySQL as a Document Store](#page-176-0). For documentation on the concepts and usage of X DevAPI, which is implemented in MySQL Shell, see [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/).
- The AdminAPI enables database administrators to work with InnoDB Cluster, which provides an integrated solution for high availability and scalability using InnoDB based MySQL databases, without requiring advanced MySQL expertise. The AdminAPI also includes support for InnoDB ReplicaSet, which enables you to administer a set of MySQL instances running asynchronous GTID-based replication in a similar way to InnoDB Cluster. Additionally, the AdminAPI makes administration of MySQL Router easier, including integration with both InnoDB Cluster and InnoDB ReplicaSet. See [MySQL AdminAPI](https://dev.mysql.com/doc/mysql-shell/8.4/en/admin-api-userguide.md).

MySQL Shell is available in two editions, the Community Edition and the Commercial Edition. The Community Edition is available free of charge. The Commercial Edition provides additional Enterprise features at low cost.

# <span id="page-176-0"></span>Chapter 22 Using MySQL as a Document Store

# **Table of Contents**

| 22.1 Interfaces to a MySQL Document Store                               | 3748 |
|-------------------------------------------------------------------------|------|
| 22.2 Document Store Concepts 3748                                       |      |
| 22.3 JavaScript Quick-Start Guide: MySQL Shell for Document Store 3749  |      |
| 22.3.1 MySQL Shell 3750                                                 |      |
| 22.3.2 Download and Import world_x Database 3751                        |      |
| 22.3.3 Documents and Collections 3752                                   |      |
| 22.3.4 Relational Tables 3762                                           |      |
| 22.3.5 Documents in Tables 3768                                         |      |
| 22.4 Python Quick-Start Guide: MySQL Shell for Document Store 3769      |      |
| 22.4.1 MySQL Shell 3769                                                 |      |
| 22.4.2 Download and Import world_x Database 3771                        |      |
| 22.4.3 Documents and Collections 3771                                   |      |
| 22.4.4 Relational Tables 3782                                           |      |
| 22.4.5 Documents in Tables 3788                                         |      |
| 22.5 X Plugin 3789                                                      |      |
| 22.5.1 Checking X Plugin Installation 3789                              |      |
| 22.5.2 Disabling X Plugin 3789                                          |      |
| 22.5.3 Using Encrypted Connections with X Plugin 3789                   |      |
| 22.5.4 Using X Plugin with the Caching SHA-2 Authentication Plugin 3790 |      |
| 22.5.5 Connection Compression with X Plugin 3791                        |      |
| 22.5.6 X Plugin Options and Variables 3794                              |      |
| 22.5.7 Monitoring X Plugin                                              | 3814 |
|                                                                         |      |

This chapter introduces an alternative way of working with MySQL as a document store, sometimes referred to as "using NoSQL". If your intention is to use MySQL in a traditional (SQL) way, this chapter is probably not relevant to you.

Traditionally, relational databases such as MySQL have usually required a schema to be defined before documents can be stored. The features described in this section enable you to use MySQL as a document store, which is a schema-less, and therefore schema-flexible, storage system for documents. For example, when you create documents describing products, you do not need to know and define all possible attributes of any products before storing and operating with the documents. This differs from working with a relational database and storing products in a table, when all columns of the table must be known and defined before adding any products to the database. The features described in this chapter enable you to choose how you configure MySQL, using only the document store model, or combining the flexibility of the document store model with the power of the relational model.

To use MySQL as a document store, you use the following server features:

- X Plugin enables MySQL Server to communicate with clients using X Protocol, which is a prerequisite for using MySQL as a document store. X Plugin is enabled by default in MySQL Server as of MySQL 8.4. For instructions to verify X Plugin installation and to configure and monitor X Plugin, see Section 22.5, "X Plugin".
- X Protocol supports both CRUD and SQL operations, authentication via SASL, allows streaming (pipelining) of commands and is extensible on the protocol and the message layer. Clients compatible with X Protocol include MySQL Shell and MySQL 8.4 Connectors.
- Clients that communicate with a MySQL Server using X Protocol can use X DevAPI to develop applications. X DevAPI offers a modern programming interface with a simple yet powerful design which provides support for established industry standard concepts. This chapter explains how to get started using either the JavaScript or Python implementation of X DevAPI in MySQL Shell as a client. See [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/) for in-depth tutorials on using X DevAPI.

# <span id="page-177-0"></span>**22.1 Interfaces to a MySQL Document Store**

To work with MySQL as a document store, you use dedicated components and a choice of clients that support communicating with the MySQL server to develop document based applications.

- The following MySQL products support X Protocol and enable you to use X DevAPI in your chosen language to develop applications that communicate with a MySQL Server functioning as a document store:
  - MySQL Shell (which provides implementations of X DevAPI in JavaScript and Python)
  - Connector/C++
  - Connector/J
  - Connector/Node.js
  - Connector/NET
  - Connector/Python
- MySQL Shell is an interactive interface to MySQL supporting JavaScript, Python, or SQL modes. You can use MySQL Shell to prototype applications, execute queries and update data. [Installing](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md) [MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md) has instructions to download and install MySQL Shell.
- The quick-start guides (tutorials) in this chapter help you to get started using MySQL Shell with MySQL as a document store.

The quick-start guide for JavaScript is here: [Section 22.3, "JavaScript Quick-Start Guide: MySQL](#page-178-0) [Shell for Document Store"](#page-178-0).

The quick-start guide for Python is here: [Section 22.4, "Python Quick-Start Guide: MySQL Shell for](#page-198-0) [Document Store".](#page-198-0)

• The MySQL Shell User Guide at [MySQL Shell 8.4](https://dev.mysql.com/doc/mysql-shell/8.4/en/) provides detailed information about configuring and using MySQL Shell.

# <span id="page-177-1"></span>**22.2 Document Store Concepts**

This section explains the concepts introduced as part of using MySQL as a document store.

- [JSON Document](#page-177-2)
- [Collection](#page-178-1)
- [CRUD Operations](#page-178-2)

# <span id="page-177-2"></span>**JSON Document**

A JSON document is a data structure composed of key-value pairs and is the fundamental structure for using MySQL as document store. For example, the world\_x schema (installed later in this chapter) contains this document:

```
{
 "GNP": 4834,
 "_id": "00005de917d80000000000000023",
 "Code": "BWA",
 "Name": "Botswana",
 "IndepYear": 1966,
 "geography": {
 "Region": "Southern Africa",
 "Continent": "Africa",
```

```
 "SurfaceArea": 581730
 },
 "government": {
 "HeadOfState": "Festus G. Mogae",
 "GovernmentForm": "Republic"
 },
 "demographics": {
 "Population": 1622000,
 "LifeExpectancy": 39.29999923706055
 }
}
```

This document shows that the values of keys can be simple data types, such as integers or strings, but can also contain other documents, arrays, and lists of documents. For example, the geography key's value consists of multiple key-value pairs. A JSON document is represented internally using the MySQL binary JSON object, through the JSON MySQL datatype.

The most important differences between a document and the tables known from traditional relational databases are that the structure of a document does not have to be defined in advance, and a collection can contain multiple documents with different structures. Relational tables on the other hand require that their structure be defined, and all rows in the table must contain the same columns.

# <span id="page-178-1"></span>**Collection**

A collection is a container that is used to store JSON documents in a MySQL database. Applications usually run operations against a collection of documents, for example to find a specific document.

# <span id="page-178-2"></span>**CRUD Operations**

The four basic operations that can be issued against a collection are Create, Read, Update and Delete (CRUD). In terms of MySQL this means:

- Create a new document (insertion or addition)
- Read one or more documents (queries)
- Update one or more documents
- Delete one or more documents

# <span id="page-178-0"></span>**22.3 JavaScript Quick-Start Guide: MySQL Shell for Document Store**

This quick-start guide provides instructions to begin prototyping document store applications interactively with MySQL Shell. The guide includes the following topics:

- Introduction to MySQL functionality, MySQL Shell, and the world\_x example schema.
- Operations to manage collections and documents.
- Operations to manage relational tables.
- Operations that apply to documents within tables.

To follow this quick-start guide you need a MySQL server with X Plugin installed, the default in 8.4, and MySQL Shell to use as the client. [MySQL Shell 8.4](https://dev.mysql.com/doc/mysql-shell/8.4/en/) provides more in-depth information about MySQL Shell. The Document Store is accessed using X DevAPI, and MySQL Shell provides this API in both JavaScript and Python.

# **Related Information**

• [MySQL Shell 8.4](https://dev.mysql.com/doc/mysql-shell/8.4/en/) provides more in-depth information about MySQL Shell.

- See [Installing MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install.md) and Section 22.5, "X Plugin" for more information about the tools used in this quick-start guide.
- [X DevAPI User Guide](https://dev.mysql.com/doc/x-devapi-userguide/en/) provides more examples of using X DevAPI to develop applications which use Document Store.
- A [Python](#page-198-0) quick-start guide is also available.

# <span id="page-179-0"></span>**22.3.1 MySQL Shell**

This quick-start guide assumes a certain level of familiarity with MySQL Shell. The following section is a high level overview, see the MySQL Shell documentation for more information. MySQL Shell is a unified scripting interface to MySQL Server. It supports scripting in JavaScript and Python. SQL is the default processing mode.

# **Start MySQL Shell**

After you have installed and started MySQL server, connect MySQL Shell to the server instance. You need to know the address of the MySQL server instance you plan to connect to. To be able to use the instance as a Document Store, the server instance must have X Plugin installed and you should connect to the server using X Protocol. For example to connect to the instance ds1.example.com on the default X Protocol port of 33060 use the network string user@ds1.example.com:33060.

![](_page_179_Picture_8.jpeg)

#### **Tip**

If you connect to the instance using classic MySQL protocol, for example by using the default port of 3306 instead of the mysqlx\_port, you cannot use the Document Store functionality shown in this tutorial. For example the db global object is not populated. To use the Document Store, always connect using X Protocol.

If MySQL Shell is not already running, open a terminal window and issue:

```
mysqlsh user@ds1.example.com:33060/world_x
```

Alternatively, if MySQL Shell is already running use the \connect command by issuing:

```
\connect user@ds1.example.com:33060/world_x
```

You need to specify the address of the MySQL server instance which you want to connect MySQL Shell to. For example in the previous example:

- user represents the user name of your MySQL account.
- ds1.example.com is the hostname of the server instance running MySQL. Replace this with the hostname of the MySQL server instance you are using as a Document Store.
- The default schema for this session is world\_x. For instructions on setting up the world\_x schema, see [Section 22.3.2, "Download and Import world\\_x Database"](#page-180-0).

For more information, see Section 6.2.5, "Connecting to the Server Using URI-Like Strings or Key-Value Pairs".

Once MySQL Shell opens, the mysql-js> prompt indicates that the active language for this session is SQL.

MYSQL SQL>

MySQL Shell supports input-line editing as follows:

• **left-arrow** and **right-arrow** keys move horizontally within the current input line.

- **up-arrow** and **down-arrow** keys move up and down through the set of previously entered lines.
- **Backspace** deletes the character before the cursor and typing new characters enters them at the cursor position.
- **Enter** sends the current input line to the server.

# **Get Help for MySQL Shell**

Type mysqlsh --help at the prompt of your command interpreter for a list of command-line options.

```
mysqlsh --help
```

Type \help at the MySQL Shell prompt for a list of available commands and their descriptions.

```
mysql-js> \help
```

Type \help followed by a command name for detailed help about an individual MySQL Shell command. For example, to view help on the \connect command, issue:

```
mysql-js> \help \connect
```

## **Quit MySQL Shell**

To quit MySQL Shell, issue the following command:

```
mysql-js> \quit
```

# **Related Information**

- See [Interactive Code Execution](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-interactive-code-execution.md) for an explanation of how interactive code execution works in MySQL Shell.
- See [Getting Started with MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-getting-started.md) to learn about session and connection alternatives.

# <span id="page-180-0"></span>**22.3.2 Download and Import world\_x Database**

As part of this quick-start guide, an example schema is provided which is referred to as the world\_x schema. Many of the examples demonstrate Document Store functionality using this schema. Start your MySQL server so that you can load the world\_x schema, then follow these steps:

- 1. Download [world\\_x-db.zip.](http://downloads.mysql.com/docs/world_x-db.zip)
- 2. Extract the installation archive to a temporary location such as /tmp/. Unpacking the archive results in a single file named world\_x.sql.
- 3. Import the world\_x.sql file to your server. You can either:
  - Start MySQL Shell in SQL mode and import the file by issuing:

```
mysqlsh -u root --sql --file /tmp/world_x-db/world_x.sql
Enter password: ****
```

• Set MySQL Shell to SQL mode while it is running and source the schema file by issuing:

```
\sql
Switching to SQL mode... Commands end with ;
\source /tmp/world_x-db/world_x.sql
```

Replace /tmp/ with the path to the world\_x.sql file on your system. Enter your password if prompted. A non-root account can be used as long as the account has privileges to create new schemas.

## **The world\_x Schema**

The world\_x example schema contains the following JSON collection and relational tables:

- Collection
  - countryinfo: Information about countries in the world.
- Tables
  - country: Minimal information about countries of the world.
  - city: Information about some of the cities in those countries.
  - countrylanguage: Languages spoken in each country.

# **Related Information**

• [MySQL Shell Sessions](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-sessions.md) explains session types.

# <span id="page-181-0"></span>**22.3.3 Documents and Collections**

When you are using MySQL as a Document Store, collections are containers within a schema that you can create, list, and drop. Collections contain JSON documents that you can add, find, update, and remove.

The examples in this section use the countryinfo collection in the world\_x schema. For instructions on setting up the world\_x schema, see [Section 22.3.2, "Download and Import world\\_x](#page-180-0) [Database"](#page-180-0).

# **Documents**

In MySQL, documents are represented as JSON objects. Internally, they are stored in an efficient binary format that enables fast lookups and updates.

• Simple document format for JavaScript:

```
{field1: "value", field2 : 10, "field 3": null}
```

An array of documents consists of a set of documents separated by commas and enclosed within [ and ] characters.

• Simple array of documents for JavaScript:

```
[{"Name": "Aruba", "Code:": "ABW"}, {"Name": "Angola", "Code:": "AGO"}]
```

MySQL supports the following JavaScript value types in JSON documents:

- numbers (integer and floating point)
- strings
- boolean (False and True)
- null
- arrays of more JSON values
- nested (or embedded) objects of more JSON values

# **Collections**

Collections are containers for documents that share a purpose and possibly share one or more indexes. Each collection has a unique name and exists within a single schema.

The term schema is equivalent to a database, which means a group of database objects as opposed to a relational schema, used to enforce structure and constraints over data. A schema does not enforce conformity on the documents in a collection.

In this quick-start guide:

• Basic objects include:

| Object form         | Description                                                                                                                                                                                                         |  |  |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|
| db                  | db is a global variable assigned to the current<br>active schema. When you want to run operations<br>against the schema, for example to retrieve a<br>collection, you use methods available for the db<br>variable. |  |  |
| db.getCollections() | db.getCollections() returns a list of collections<br>in the schema. Use the list to get references to<br>collection objects, iterate over them, and so on.                                                          |  |  |

• Basic operations scoped by collections include:

| Operation form   | Description                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| db.name.add()    | The add() method inserts one document or a list<br>of documents into the named collection.    |
| db.name.find()   | The find() method returns some or all documents<br>in the named collection.                   |
| db.name.modify() | The modify() method updates documents in the<br>named collection.                             |
| db.name.remove() | The remove() method deletes one document or a<br>list of documents from the named collection. |

## **Related Information**

- See [Working with Collections](https://dev.mysql.com/doc/x-devapi-userguide/en/devapi-users-working-with-collections.md) for a general overview.
- [CRUD EBNF Definitions](https://dev.mysql.com/doc/x-devapi-userguide/en/mysql-x-crud-ebnf-definitions.md) provides a complete list of operations.