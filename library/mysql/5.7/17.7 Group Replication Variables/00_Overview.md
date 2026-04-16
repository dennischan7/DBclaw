---
source: MySQL 5.7 Reference
title: 00_Overview
---

The next two sections contain information about MySQL server system and server status variables which are specific to the Group Replication plugin.

**Table 17.4 Group Replication Variable and Option Summary**

| Name | Cmd-Line                                 | Option File                                              | System Var | Status Var | Var Scope | Dynamic |
|------|------------------------------------------|----------------------------------------------------------|------------|------------|-----------|---------|
|      | Yes                                      | group_replication_allow_local_disjoint_gtids_join<br>Yes | Yes        |            | Global    | Yes     |
|      | Yes                                      | group_replication_allow_local_lower_version_join<br>Yes  | Yes        |            | Global    | Yes     |
|      | Yes                                      | group_replication_auto_increment_increment<br>Yes        | Yes        |            | Global    | Yes     |
|      | group_replication_bootstrap_group<br>Yes | Yes                                                      | Yes        |            | Global    | Yes     |

| Name | Cmd-Line                                                  | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|-----------------------------------------------------------|-------------|------------|------------|-----------|---------|
|      | group_replication_components_stop_timeout<br>Yes          | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_compression_threshold<br>Yes            | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_enforce_update_everywhere_checks<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_exit_state_action<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_applier_threshold<br>Yes   | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_certifier_threshold<br>Yes | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_flow_control_mode<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_force_members<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_group_name<br>Yes                       | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_group_seeds<br>Yes                      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_gtid_assignment_block_size<br>Yes       | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_ip_whitelist<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_local_address<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_member_weight<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_poll_spin_loops<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_primary_member                          |             |            | Yes        | Global    | No      |
|      | group_replication_recovery_complete_at<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_reconnect_interval<br>Yes      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_retry_count<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_ca<br>Yes                  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_capath<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cert<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cipher<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crl<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crlpath<br>Yes             | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_key<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_verify_server_cert<br>Yes  | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_use_ssl<br>Yes                 | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_single_primary_mode<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_ssl_mode<br>Yes                         | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_start_on_boot<br>Yes                    | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_transaction_size_limit<br>Yes           | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_unreachable_majority_timeout<br>Yes     | Yes         | Yes        |            | Global    | Yes     |

# <span id="page-30-0"></span>**17.7.1 Group Replication System Variables**

This section lists the system variables that are specific to the Group Replication plugin.

The name of each Group Replication system variable is prefixed with group\_replication\_.

Most system variables for Group Replication are described as dynamic, and their values can be changed while the server is running. However, in most cases, the change only takes effect after you stop and restart Group Replication on the group member using a STOP GROUP\_REPLICATION statement followed by a START GROUP\_REPLICATION statement. Changes to the following system variables take effect without stopping and restarting Group Replication:

- [group\\_replication\\_exit\\_state\\_action](#page-35-1)
- [group\\_replication\\_flow\\_control\\_applier\\_threshold](#page-37-0)
- [group\\_replication\\_flow\\_control\\_certifier\\_threshold](#page-37-1)
- [group\\_replication\\_flow\\_control\\_hold\\_percent](#page-37-2)
- [group\\_replication\\_flow\\_control\\_max\\_quota](#page-37-3)
- [group\\_replication\\_flow\\_control\\_member\\_quota\\_percent](#page-38-0)
- [group\\_replication\\_flow\\_control\\_min\\_quota](#page-38-1)
- [group\\_replication\\_flow\\_control\\_min\\_recovery\\_quota](#page-39-2)
- [group\\_replication\\_flow\\_control\\_mode](#page-39-1)
- [group\\_replication\\_force\\_members](#page-39-0)
- [group\\_replication\\_member\\_weight](#page-43-0)
- [group\\_replication\\_transaction\\_size\\_limit](#page-48-0)
- [group\\_replication\\_unreachable\\_majority\\_timeout](#page-48-2)

Most system variables for Group Replication can have different values on different group members. For the following system variables, it is advisable to set the same value on all members of a group in order to avoid unnecessary rollback of transactions, failure of message delivery, or failure of message recovery:

- [group\\_replication\\_auto\\_increment\\_increment](#page-33-1)
- [group\\_replication\\_compression\\_threshold](#page-34-0)
- [group\\_replication\\_transaction\\_size\\_limit](#page-48-0)

Some system variables on a Group Replication group member, including some Group Replicationspecific system variables and some general system variables, are group-wide configuration settings. These system variables must have the same value on all group members, cannot be changed while Group Replication is running, and require a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-33-0)) in order for the value change to take effect. These conditions apply to the following system variables:

- [group\\_replication\\_single\\_primary\\_mode](#page-47-0)
- [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-35-0)
- [group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-41-1)
- [default\\_table\\_encryption](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.md#sysvar_default_table_encryption)
- lower\_case\_table\_names
- transaction\_write\_set\_extraction

![](_page_31_Picture_25.jpeg)

#### **Important**

• A number of system variables for Group Replication are not completely validated during server startup if they are passed as command line arguments to the server. These system variables include [group\\_replication\\_group\\_name](#page-40-1), [group\\_replication\\_single\\_primary\\_mode](#page-47-0), [group\\_replication\\_force\\_members](#page-39-0), the SSL variables, and the flow control system variables. They are only fully validated after the server has started.

• System variables for Group Replication that specify IP addresses or host names for group members are not validated until a START GROUP\_REPLICATION statement is issued. Group Replication's Group Communication System (GCS) is not available to validate the values until that point.

The system variables that are specific to the Group Replication plugin are as follows:

<span id="page-32-0"></span>• [group\\_replication\\_allow\\_local\\_disjoint\\_gtids\\_join](#page-32-0)

| Command-Line Format | group-replication-allow-local<br>disjoint-gtids-join[={OFF ON}] |  |
|---------------------|-----------------------------------------------------------------|--|
| Deprecated          | Yes                                                             |  |
| System Variable     | group_replication_allow_local_disjoint_gtids_join               |  |
| Scope               | Global                                                          |  |
| Dynamic             | Yes                                                             |  |
| Type                | Boolean                                                         |  |
| Default Value       | OFF                                                             |  |

Deprecated in version 5.7.21 and scheduled for removal in a future version. Allows the server to join the group even if it has local transactions that are not present in the group.

![](_page_32_Picture_7.jpeg)

### **Warning**

Use caution when enabling this option as incorrect usage can lead to conflicts in the group and rollback of transactions. The option should only be enabled as a last resort method to allow a server that has local transactions to join an existing group, and then only if the local transactions do not affect the data that is handled by the group (for example, an administrative action that was written to the binary log). The option should not be left enabled on all group members.

<span id="page-32-1"></span>• [group\\_replication\\_allow\\_local\\_lower\\_version\\_join](#page-32-1)

| Command-Line Format | group-replication-allow-local<br>lower-version-join[={OFF ON}] |  |
|---------------------|----------------------------------------------------------------|--|
| System Variable     | group_replication_allow_local_lower_version_join               |  |
| Scope               | Global                                                         |  |
| Dynamic             | Yes                                                            |  |
| Type                | Boolean                                                        |  |
| Default Value       | OFF                                                            |  |

Allows the current server to join the group even if it has a lower major version than the group. With the default setting OFF, servers are not permitted to join a replication group if they have a lower major version than the existing group members. For example, a MySQL 5.7 server cannot join a group that consists of MySQL 8.0 servers. This standard policy ensures that all members of a group are able to exchange messages and apply transactions. Set [group\\_replication\\_allow\\_local\\_lower\\_version\\_join](#page-32-1) to ON only in the following scenarios:

• A server must be added to the group in an emergency in order to improve the group's fault tolerance, and only older versions are available.

• You want to carry out a downgrade of the replication group members without shutting down the whole group and bootstrapping it again.

![](_page_33_Picture_2.jpeg)

#### **Warning**

Setting this option to ON does not make the new member compatible with the group, and allows it to join the group without any safeguards against incompatible behaviors by the existing members. To ensure the new member's correct operation, take both of the following precautions:

- 1. Before the server with the lower major version joins the group, stop all writes on that server.
- 2. From the point where the server with the lower major version joins the group, stop all writes on the other servers in the group.

Without these precautions, the server with the lower major version is likely to experience difficulties and terminate with an error.

<span id="page-33-1"></span>• [group\\_replication\\_auto\\_increment\\_increment](#page-33-1)

| Command-Line Format | group-replication-auto-increment<br>increment=# |  |
|---------------------|-------------------------------------------------|--|
| System Variable     | group_replication_auto_increment_increment      |  |
| Scope               | Global                                          |  |
| Dynamic             | Yes                                             |  |
| Type                | Integer                                         |  |
| Default Value       | 7                                               |  |
| Minimum Value       | 1                                               |  |
| Maximum Value       | 65535                                           |  |

Determines the interval between successive column values for transactions that execute on this server instance. This system variable should have the same value on all group members. When Group Replication is started on a server, the value of the server system variable auto\_increment\_increment is changed to this value, and the value of the server system variable auto\_increment\_offset is changed to the server ID. These settings avoid the selection of duplicate auto-increment values for writes on group members, which causes rollback of transactions. The changes are reverted when Group Replication is stopped. These changes are only made and reverted if auto\_increment\_increment and auto\_increment\_offset each have their default value of 1. If their values have already been modified from the default, Group Replication does not alter them.

The default value of 7 represents a balance between the number of usable values and the permitted maximum size of a replication group (9 members). If your group has more or fewer members, you can set this system variable to match the expected number of group members before Group Replication is started. You cannot change the setting while Group Replication is running.

![](_page_33_Picture_12.jpeg)

### **Important**

Setting group\_replication\_auto\_increment\_increment has no effect when [group\\_replication\\_single\\_primary\\_mode](#page-47-0) is ON.

<span id="page-33-0"></span>• [group\\_replication\\_bootstrap\\_group](#page-33-0)

| Command-Line Format | group-replication-bootstrap |
|---------------------|-----------------------------|
|                     | group[={OFF ON}]            |

| System Variable | group_replication_bootstrap_group |
|-----------------|-----------------------------------|
| Scope           | Global                            |
| Dynamic         | Yes                               |
| Type            | Boolean                           |
| Default Value   | OFF                               |

Configure this server to bootstrap the group. This option must only be set on one server and only when starting the group for the first time or restarting the entire group. After the group has been bootstrapped, set this option to OFF. It should be set to OFF both dynamically and in the configuration files. Starting two servers or restarting one server with this option set while the group is running may lead to an artificial split brain situation, where two independent groups with the same name are bootstrapped.

<span id="page-34-1"></span>• [group\\_replication\\_components\\_stop\\_timeout](#page-34-1)

| Command-Line Format | group-replication-components-stop<br>timeout=# |
|---------------------|------------------------------------------------|
| System Variable     | group_replication_components_stop_timeout      |
| Scope               | Global                                         |
| Dynamic             | Yes                                            |
| Type                | Integer                                        |
| Default Value       | 31536000                                       |
| Minimum Value       | 2                                              |
| Maximum Value       | 31536000                                       |
| Unit                | seconds                                        |

Timeout, in seconds, that Group Replication waits for each of the components when shutting down.

<span id="page-34-0"></span>• [group\\_replication\\_compression\\_threshold](#page-34-0)

| Command-Line Format | group-replication-compression<br>threshold=# |
|---------------------|----------------------------------------------|
| System Variable     | group_replication_compression_threshold      |
| Scope               | Global                                       |
| Dynamic             | Yes                                          |
| Type                | Integer                                      |
| Default Value       | 1000000                                      |
| Minimum Value       | 0                                            |
| Maximum Value       | 4294967295                                   |
| Unit                | bytes                                        |

The threshold value in bytes above which compression is applied to messages sent between group members. If this system variable is set to zero, compression is disabled. The value of [group\\_replication\\_compression\\_threshold](#page-34-0) should be the same on all group members.

Group Replication uses the LZ4 compression algorithm to compress messages sent in the group. Note that the maximum supported input size for the LZ4 compression algorithm is 2113929216 bytes. This limit is lower than the maximum possible value for the [group\\_replication\\_compression\\_threshold](#page-34-0) system variable, which is matched to the maximum message size accepted by XCom. With the LZ4 compression algorithm, do not set a value greater than 2113929216 bytes for [group\\_replication\\_compression\\_threshold](#page-34-0), because transactions above this size cannot be committed when message compression is enabled.

For more information, see [Section 17.9.7.2, "Message Compression"](#page-63-0).

<span id="page-35-0"></span>• [group\\_replication\\_enforce\\_update\\_everywhere\\_checks](#page-35-0)

| Command-Line Format | group-replication-enforce-update<br>everywhere-checks[={OFF ON}] |  |
|---------------------|------------------------------------------------------------------|--|
| System Variable     | group_replication_enforce_update_everywhere_checks               |  |
| Scope               | Global                                                           |  |
| Dynamic             | Yes                                                              |  |
| Type                | Boolean                                                          |  |
| Default Value       | OFF                                                              |  |

Enable or disable strict consistency checks for multi-primary update everywhere. The default is that checks are disabled. In single-primary mode, this option must be disabled on all group members. In multi-primary mode, when this option is enabled, statements are checked as follows to ensure they are compatible with multi-primary mode:

- If a transaction is executed under the SERIALIZABLE isolation level, then its commit fails when synchronizing itself with the group.
- If a transaction executes against a table that has foreign keys with cascading constraints, then the transaction fails to commit when synchronizing itself with the group.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-33-0)) in order for the value change to take effect.

<span id="page-35-1"></span>• [group\\_replication\\_exit\\_state\\_action](#page-35-1)

| Command-Line Format | group-replication-exit-state<br>action=value |
|---------------------|----------------------------------------------|
| System Variable     | group_replication_exit_state_action          |
| Scope               | Global                                       |
| Dynamic             | Yes                                          |
| Type                | Enumeration                                  |
| Default Value       | READ_ONLY                                    |
| Valid Values        | ABORT_SERVER                                 |
|                     | READ_ONLY                                    |

Configures how Group Replication behaves when a server instance leaves the group unintentionally, for example after encountering an applier error, or in the case of a loss of majority, or when another member of the group expels it due to a suspicion timing out. The timeout period for a member to leave the group in the case of a loss of majority is set by the [group\\_replication\\_unreachable\\_majority\\_timeout](#page-48-2) system variable. Note that an expelled group member does not know that it was expelled until it reconnects to the group, so the specified action is only taken if the member manages to reconnect, or if the member raises a suspicion on itself and expels itself.

When [group\\_replication\\_exit\\_state\\_action](#page-35-1) is set to ABORT\_SERVER, if the member exits the group unintentionally, the instance shuts down MySQL.

When [group\\_replication\\_exit\\_state\\_action](#page-35-1) is set to READ\_ONLY, if the member exits the group unintentionally, the instance switches MySQL to super read only mode (by setting the system variable super\_read\_only to ON). This setting is the default in MySQL 5.7.

![](_page_36_Picture_4.jpeg)

### **Important**

If a failure occurs before the member has successfully joined the group, the specified exit action is not taken. This is the case if there is a failure during the local configuration check, or a mismatch between the configuration of the joining member and the configuration of the group. In these situations, the super\_read\_only system variable is left with its original value, and the server does not shut down MySQL. To ensure that the server cannot accept updates when Group Replication did not start, we therefore recommend that super\_read\_only=ON is set in the server's configuration file at startup, which Group Replication changes to OFF on primary members after it has been started successfully. This safeguard is particularly important when the server is configured to start Group Replication on server boot ([group\\_replication\\_start\\_on\\_boot=ON](#page-48-1)), but it is also useful when Group Replication is started manually using a START GROUP\_REPLICATION command.

If a failure occurs after the member has successfully joined the group, the specified exit action is taken. This is the case if there is an applier error, if the member is expelled from the group, or if the member is set to time out in the event of an unreachable majority. In these situations, if READ\_ONLY is the exit action, the super\_read\_only system variable is set to ON, or if ABORT\_SERVER is the exit action, the server shuts down MySQL.

**Table 17.5 Exit actions in Group Replication failure situations**

| Failure situation                                          | Group Replication<br>started with START | Group Replication<br>started with            |
|------------------------------------------------------------|-----------------------------------------|----------------------------------------------|
|                                                            | GROUP_REPLICATION                       | group_replication_start_on_boot<br>=ON       |
| Member fails local configuration<br>check                  | super_read_only unchanged               | super_read_only unchanged                    |
|                                                            | MySQL continues running                 | MySQL continues running                      |
| OR                                                         | Set super_read_only=ON at               | Set super_read_only=ON                       |
| Mismatch between joining<br>member and group configuration | startup to prevent updates              | at startup to prevent updates<br>(Important) |
| Applier error on member                                    | super_read_only set to ON               | super_read_only set to ON                    |
| OR                                                         | OR                                      | OR                                           |
| Member expelled from group                                 | MySQL shuts down                        | MySQL shuts down                             |
| OR                                                         |                                         |                                              |
| Unreachable majority timeout                               |                                         |                                              |

<span id="page-37-0"></span>• [group\\_replication\\_flow\\_control\\_applier\\_threshold](#page-37-0)

| Command-Line Format | group-replication-flow-control<br>applier-threshold=# |  |
|---------------------|-------------------------------------------------------|--|
| System Variable     | group_replication_flow_control_applier_threshold      |  |
| Scope               | Global                                                |  |
| Dynamic             | Yes                                                   |  |
| Type                | Integer                                               |  |
| Default Value       | 25000                                                 |  |
| Minimum Value       | 0                                                     |  |
| Maximum Value       | 2147483647                                            |  |
| Unit                | transactions                                          |  |

Specifies the number of waiting transactions in the applier queue that trigger flow control. This variable can be changed without resetting Group Replication.

<span id="page-37-1"></span>• [group\\_replication\\_flow\\_control\\_certifier\\_threshold](#page-37-1)

| Command-Line Format | group-replication-flow-control<br>certifier-threshold=# |  |
|---------------------|---------------------------------------------------------|--|
| System Variable     | group_replication_flow_control_certifier_threshold      |  |
| Scope               | Global                                                  |  |
| Dynamic             | Yes                                                     |  |
| Type                | Integer                                                 |  |
| Default Value       | 25000                                                   |  |
| Minimum Value       | 0                                                       |  |
| Maximum Value       | 2147483647                                              |  |
| Unit                | transactions                                            |  |

Specifies the number of waiting transactions in the certifier queue that trigger flow control. This variable can be changed without resetting Group Replication.

<span id="page-37-2"></span>• [group\\_replication\\_flow\\_control\\_hold\\_percent](#page-37-2)

| Command-Line Format | group-replication-flow-control<br>hold-percent=# |
|---------------------|--------------------------------------------------|
| System Variable     | group_replication_flow_control_hold_percent      |
| Scope               | Global                                           |
| Dynamic             | Yes                                              |
| Type                | Integer                                          |
| Default Value       | 10                                               |
| Minimum Value       | 0                                                |
| Maximum Value       | 100                                              |
| Unit                | percentage                                       |

Defines what percentage of the group quota remains unused to allow a cluster under flow control to catch up on backlog. A value of 0 implies that no part of the quota is reserved for catching up on the work backlog.

<span id="page-37-3"></span>• [group\\_replication\\_flow\\_control\\_max\\_quota](#page-37-3)

| Command-Line Format | group-replication-flow-control<br>max-quota=# |
|---------------------|-----------------------------------------------|
| System Variable     | group_replication_flow_control_max_quota      |
| Scope               | Global                                        |
| Dynamic             | Yes                                           |
| Type                | Integer                                       |
| Default Value       | 0                                             |
| Minimum Value       | 0                                             |
| Maximum Value       | 2147483647                                    |

Defines the maximum flow control quota of the group, or the maximum available quota for any period while flow control is enabled. A value of 0 implies that there is no maximum quota set. Cannot be smaller than [group\\_replication\\_flow\\_control\\_min\\_quota](#page-38-1) and group\_replication\_flow\_control\_min\_recovery\_quota.

<span id="page-38-0"></span>• [group\\_replication\\_flow\\_control\\_member\\_quota\\_percent](#page-38-0)

| Command-Line Format | group-replication-flow-control<br>member-quota-percent=# |  |
|---------------------|----------------------------------------------------------|--|
| System Variable     | group_replication_flow_control_member_quota_percent      |  |
| Scope               | Global                                                   |  |
| Dynamic             | Yes                                                      |  |
| Type                | Integer                                                  |  |
| Default Value       | 0                                                        |  |
| Minimum Value       | 0                                                        |  |
| Maximum Value       | 100                                                      |  |
| Unit                | percentage                                               |  |

Defines the percentage of the quota that a member should assume is available for itself when calculating the quotas. A value of 0 implies that the quota should be split equally between members that were writers in the last period.

<span id="page-38-1"></span>• [group\\_replication\\_flow\\_control\\_min\\_quota](#page-38-1)

| Command-Line Format | group-replication-flow-control<br>min-quota=# |
|---------------------|-----------------------------------------------|
| System Variable     | group_replication_flow_control_min_quota      |
| Scope               | Global                                        |
| Dynamic             | Yes                                           |
| Type                | Integer                                       |
| Default Value       | 0                                             |
| Minimum Value       | 0                                             |
| Maximum Value       | 2147483647                                    |

Controls the lowest flow control quota that can be assigned to a member, independently of the calculated minimum quota executed in the last period. A value of 0 implies that there is no minimum quota. Cannot be larger than [group\\_replication\\_flow\\_control\\_max\\_quota](#page-37-3).

<span id="page-39-2"></span>• [group\\_replication\\_flow\\_control\\_min\\_recovery\\_quota](#page-39-2)

| Command-Line Format | group-replication-flow-control<br>min-recovery-quota=# |  |
|---------------------|--------------------------------------------------------|--|
| System Variable     | group_replication_flow_control_min_recovery_quota      |  |
| Scope               | Global                                                 |  |
| Dynamic             | Yes                                                    |  |
| Type                | Integer                                                |  |
| Default Value       | 0                                                      |  |
| Minimum Value       | 0                                                      |  |
| Maximum Value       | 2147483647                                             |  |

Controls the lowest quota that can be assigned to a member because of another recovering member in the group, independently of the calculated minimum quota executed in the last period. A value of 0 implies that there is no minimum quota. Cannot be larger than group\_replication\_flow\_control\_max\_quota.

<span id="page-39-1"></span>• [group\\_replication\\_flow\\_control\\_mode](#page-39-1)

| Command-Line Format | group-replication-flow-control<br>mode=value |
|---------------------|----------------------------------------------|
| System Variable     | group_replication_flow_control_mode          |
| Scope               | Global                                       |
| Dynamic             | Yes                                          |
| Type                | Enumeration                                  |
| Default Value       | QUOTA                                        |
| Valid Values        | DISABLED                                     |
|                     | QUOTA                                        |

Specifies the mode used for flow control. This variable can be changed without resetting Group Replication.

<span id="page-39-0"></span>• [group\\_replication\\_force\\_members](#page-39-0)

| Command-Line Format | group-replication-force<br>members=value |
|---------------------|------------------------------------------|
| System Variable     | group_replication_force_members          |
| Scope               | Global                                   |
| Dynamic             | Yes                                      |
| Type                | String                                   |

A list of peer addresses as a comma separated list such as host1:port1,host2:port2. This option is used to force a new group membership, in which the excluded members do not receive a new view and are blocked. (You need to manually kill the excluded servers.) Any invalid host

names in the list could cause this action to fail because they could block group membership. For a description of the procedure to follow, see [Section 17.5.3, "Network Partitioning"](#page-14-0).

You must specify the address or host name and port as they are given in the [group\\_replication\\_local\\_address](#page-42-0) option for each member. For example:

"198.51.100.44:33061,example.org:33061"

After you have used the [group\\_replication\\_force\\_members](#page-39-0) system variable to successfully force a new group membership and unblock the group, ensure that you clear the system variable. [group\\_replication\\_force\\_members](#page-39-0) must be empty in order to issue a START GROUP\_REPLICATION statement.

<span id="page-40-1"></span>• [group\\_replication\\_group\\_name](#page-40-1)

| Command-Line Format | group-replication-group-name=value |
|---------------------|------------------------------------|
| System Variable     | group_replication_group_name       |
| Scope               | Global                             |
| Dynamic             | Yes                                |
| Type                | String                             |

The name of the group which this server instance belongs to. Must be a valid UUID. This UUID is used internally when setting GTIDs for Group Replication events in the binary log.

![](_page_40_Picture_8.jpeg)

#### **Important**

A unique UUID must be used.

<span id="page-40-0"></span>• [group\\_replication\\_group\\_seeds](#page-40-0)

| Command-Line Format | group-replication-group<br>seeds=value |
|---------------------|----------------------------------------|
| System Variable     | group_replication_group_seeds          |
| Scope               | Global                                 |
| Dynamic             | Yes                                    |
| Type                | String                                 |

A list of group members to which a joining member can connect to obtain details of all the current group members. The joining member uses these details to select and connect to a group member to obtain the data needed for synchrony with the group. The list consists of the seed member's network addresses specified as a comma separated list, such as host1:port1,host2:port2.

![](_page_40_Picture_14.jpeg)

#### **Important**

These addresses must not be the member's SQL hostname and port.

Note that the value you specify for this variable is not validated until a START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

Usually this list consists of all members of the group, but you can choose a subset of the group members to be seeds. The list must contain at least one valid member address. Each address is validated when starting Group Replication. If the list does not contain any valid host names, issuing START GROUP\_REPLICATION fails.

<span id="page-41-1"></span>• [group\\_replication\\_gtid\\_assignment\\_block\\_size](#page-41-1)

| Command-Line Format              | group-replication-gtid-assignment<br>block-size=# |
|----------------------------------|---------------------------------------------------|
| System Variable                  | group_replication_gtid_assignment_block_size      |
| Scope                            | Global                                            |
| Dynamic                          | Yes                                               |
| Type                             | Integer                                           |
| Default Value                    | 1000000                                           |
| Minimum Value                    | 1                                                 |
| Maximum Value (64-bit platforms) | 9223372036854775807                               |
| Maximum Value (32-bit platforms) | 4294967295                                        |

The number of consecutive GTIDs that are reserved for each member. Each member consumes its blocks and reserves more when needed.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-33-0)) in order for the value change to take effect.

<span id="page-41-0"></span>• [group\\_replication\\_ip\\_whitelist](#page-41-0)

| Command-Line Format | group-replication-ip<br>whitelist=value |
|---------------------|-----------------------------------------|
| System Variable     | group_replication_ip_whitelist          |
| Scope               | Global                                  |
| Dynamic             | Yes                                     |
| Type                | String                                  |
| Default Value       | AUTOMATIC                               |

Specifies the allowlist of hosts that are permitted to connect to the group. The address that you specify for each group member in [group\\_replication\\_local\\_address](#page-42-0) must be allowlisted on the other servers in the replication group. Note that the value you specify for this variable is not validated until a START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

By default, this system variable is set to AUTOMATIC, which permits connections from private subnetworks active on the host. The group communication engine (XCom) automatically scans active interfaces on the host, and identifies those with addresses on private subnetworks. These addresses and the localhost IP address for IPv4 are used to create the Group Replication allowlist. For a list of the ranges from which addresses are automatically allowlisted, see [Section 17.6.1, "Group Replication IP Address Allowlisting"](#page-26-1).

The automatic allowlist of private addresses cannot be used for connections from servers outside the private network. For Group Replication connections between server instances that are on different machines, you must provide public IP addresses and specify these as an explicit allowlist. If you specify any entries for the allowlist, the private addresses are not added automatically, so if you use any of these, you must specify them explicitly. The localhost IP address is added automatically.

As the value of the [group\\_replication\\_ip\\_whitelist](#page-41-0) option, you can specify any combination of the following:

- IPv4 addresses with CIDR notation (for example, 192.0.2.21/24)
- Host names, from MySQL 5.7.21 (for example, example.org)
- Host names with CIDR notation, from MySQL 5.7.21 (for example, www.example.com/24)

IPv6 addresses, and host names that resolve to IPv6 addresses, are not supported in MySQL 5.7. You can use CIDR notation in combination with host names or IP addresses to allowlist a block of IP addresses with a particular network prefix, but do ensure that all the IP addresses in the specified subnet are under your control.

A comma must separate each entry in the allowlist. For example:

```
192.0.2.22,198.51.100.0/24,example.org,www.example.com/24
```

It is possible to configure different allowlists on different group members according to your security requirements, for example, in order to keep different subnets separate. However, this can cause issues when a group is reconfigured. If you do not have a specific security requirement to do otherwise, use the same allowlist on all members of a group. For more details, see [Section 17.6.1,](#page-26-1) ["Group Replication IP Address Allowlisting".](#page-26-1)

For host names, name resolution takes place only when a connection request is made by another server. A host name that cannot be resolved is not considered for allowlist validation, and a warning message is written to the error log. Forward-confirmed reverse DNS (FCrDNS) verification is carried out for resolved host names.

![](_page_42_Picture_9.jpeg)

#### **Warning**

Host names are inherently less secure than IP addresses in an allowlist. FCrDNS verification provides a good level of protection, but can be compromised by certain types of attack. Specify host names in your allowlist only when strictly necessary, and ensure that all components used for name resolution, such as DNS servers, are maintained under your control. You can also implement name resolution locally using the hosts file, to avoid the use of external components.

<span id="page-42-0"></span>• [group\\_replication\\_local\\_address](#page-42-0)

| Command-Line Format | group-replication-local         |
|---------------------|---------------------------------|
|                     | address=value                   |
| System Variable     | group_replication_local_address |
| Scope               | Global                          |
| Dynamic             | Yes                             |
| Type                | String                          |

The network address which the member provides for connections from other members, specified as a host:port formatted string. This address must be reachable by all members of the group because it is used by the group communication engine for Group Replication (XCom, a Paxos

variant) for TCP communication between remote XCom instances. Communication with the local instance is over an input channel using shared memory.

![](_page_43_Picture_2.jpeg)

#### **Warning**

Do not use this address for communication with the member.

Other Group Replication members contact this member through this host:port for all internal group communication. This is not the MySQL server SQL protocol host and port.

The address or host name that you specify in [group\\_replication\\_local\\_address](#page-42-0) is used by Group Replication as the unique identifier for a group member within the replication group. You can use the same port for all members of a replication group as long as the host names or IP addresses are all different, and you can use the same host name or IP address for all members as long as the ports are all different. The recommended port for [group\\_replication\\_local\\_address](#page-42-0) is 33061. Note that the value you specify for this variable is not validated until the START GROUP\_REPLICATION statement is issued and the Group Communication System (GCS) is available.

<span id="page-43-0"></span>• [group\\_replication\\_member\\_weight](#page-43-0)

| Command-Line Format | group-replication-member-weight=# |
|---------------------|-----------------------------------|
| System Variable     | group_replication_member_weight   |
| Scope               | Global                            |
| Dynamic             | Yes                               |
| Type                | Integer                           |
| Default Value       | 50                                |
| Minimum Value       | 0                                 |
| Maximum Value       | 100                               |
| Unit                | percentage                        |

A percentage weight that can be assigned to members to influence the chance of the member being elected as primary in the event of failover, for example when the existing primary leaves a singleprimary group. Assign numeric weights to members to ensure that specific members are elected, for example during scheduled maintenance of the primary or to ensure certain hardware is prioritized in the event of failover.

For a group with members configured as follows:

- member-1: group\_replication\_member\_weight=30, server\_uuid=aaaa
- member-2: group\_replication\_member\_weight=40, server\_uuid=bbbb
- member-3: group\_replication\_member\_weight=40, server\_uuid=cccc
- member-4: group\_replication\_member\_weight=40, server\_uuid=dddd

during election of a new primary the members above would be sorted as member-2, member-3, member-4, and member-1. This results in member-2 being chosen as the new primary in the event of failover. For more information, see [Section 17.5.1.1, "Single-Primary Mode"](#page-12-0).

<span id="page-43-1"></span>• [group\\_replication\\_poll\\_spin\\_loops](#page-43-1)

| Command-Line Format | group-replication-poll-spin<br>loops=# |
|---------------------|----------------------------------------|
| System Variable     | group_replication_poll_spin_loops      |

| Scope                            | Global               |
|----------------------------------|----------------------|
| Dynamic                          | Yes                  |
| Type                             | Integer              |
| Default Value                    | 0                    |
| Minimum Value                    | 0                    |
| Maximum Value (64-bit platforms) | 18446744073709551615 |
| Maximum Value (32-bit platforms) | 4294967295           |

The number of times the group communication thread waits for the communication engine mutex to be released before the thread waits for more incoming network messages.

<span id="page-44-2"></span>• [group\\_replication\\_recovery\\_complete\\_at](#page-44-2)

| Command-Line Format | group-replication-recovery<br>complete-at=value |
|---------------------|-------------------------------------------------|
| System Variable     | group_replication_recovery_complete_at          |
| Scope               | Global                                          |
| Dynamic             | Yes                                             |
| Type                | Enumeration                                     |
| Default Value       | TRANSACTIONS_APPLIED                            |
| Valid Values        | TRANSACTIONS_CERTIFIED                          |
|                     | TRANSACTIONS_APPLIED                            |

Recovery policies when handling cached transactions after state transfer. This option specifies whether a member is marked online after it has received all transactions that it missed before it joined the group (TRANSACTIONS\_CERTIFIED) or after it has received and applied them (TRANSACTIONS\_APPLIED).

<span id="page-44-0"></span>• [group\\_replication\\_recovery\\_retry\\_count](#page-44-0)

| Command-Line Format | group-replication-recovery-retry<br>count=# |
|---------------------|---------------------------------------------|
| System Variable     | group_replication_recovery_retry_count      |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |
| Type                | Integer                                     |
| Default Value       | 10                                          |
| Minimum Value       | 0                                           |
| Maximum Value       | 31536000                                    |

The number of times that the member that is joining tries to connect to the available donors before giving up.

<span id="page-44-1"></span>• [group\\_replication\\_recovery\\_reconnect\\_interval](#page-44-1)

| Command-Line Format | group-replication-recovery<br>reconnect-interval=# |  |
|---------------------|----------------------------------------------------|--|
| System Variable     | group_replication_recovery_reconnect_interval      |  |
| Scope               | Global<br>3017                                     |  |

| Dynamic       | Yes      |
|---------------|----------|
| Type          | Integer  |
| Default Value | 60       |
| Minimum Value | 0        |
| Maximum Value | 31536000 |
| Unit          | seconds  |

The sleep time, in seconds, between reconnection attempts when no donor was found in the group.

<span id="page-45-0"></span>• [group\\_replication\\_recovery\\_ssl\\_ca](#page-45-0)

| Command-Line Format | group-replication-recovery-ssl<br>ca=value |
|---------------------|--------------------------------------------|
| System Variable     | group_replication_recovery_ssl_ca          |
| Scope               | Global                                     |
| Dynamic             | Yes                                        |
| Type                | String                                     |

The path to a file that contains a list of trusted SSL certificate authorities.

<span id="page-45-1"></span>• [group\\_replication\\_recovery\\_ssl\\_capath](#page-45-1)

| Command-Line Format | group-replication-recovery-ssl<br>capath=value |  |
|---------------------|------------------------------------------------|--|
| System Variable     | group_replication_recovery_ssl_capath          |  |
| Scope               | Global                                         |  |
| Dynamic             | Yes                                            |  |
| Type                | String                                         |  |

The path to a directory that contains trusted SSL certificate authority certificates.

<span id="page-45-2"></span>• [group\\_replication\\_recovery\\_ssl\\_cert](#page-45-2)

| Command-Line Format | group-replication-recovery-ssl<br>cert=value |  |
|---------------------|----------------------------------------------|--|
| System Variable     | group_replication_recovery_ssl_cert          |  |
| Scope               | Global                                       |  |
| Dynamic             | Yes                                          |  |
| Type                | String                                       |  |

The name of the SSL certificate file to use for establishing a secure connection.

<span id="page-45-3"></span>• [group\\_replication\\_recovery\\_ssl\\_key](#page-45-3)

| Command-Line Format | group-replication-recovery-ssl<br>key=value |
|---------------------|---------------------------------------------|
| System Variable     | group_replication_recovery_ssl_key          |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |

| Type | String |
|------|--------|
|------|--------|

The name of the SSL key file to use for establishing a secure connection.

<span id="page-46-0"></span>• [group\\_replication\\_recovery\\_ssl\\_cipher](#page-46-0)

| Command-Line Format | group-replication-recovery-ssl<br>cipher=value |  |
|---------------------|------------------------------------------------|--|
| System Variable     | group_replication_recovery_ssl_cipher          |  |
| Scope               | Global                                         |  |
| Dynamic             | Yes                                            |  |
| Type                | String                                         |  |

The list of permissible ciphers for SSL encryption.

<span id="page-46-1"></span>• [group\\_replication\\_recovery\\_ssl\\_crl](#page-46-1)

| Command-Line Format | group-replication-recovery-ssl<br>crl=value |
|---------------------|---------------------------------------------|
| System Variable     | group_replication_recovery_ssl_crl          |
| Scope               | Global                                      |
| Dynamic             | Yes                                         |
| Type                | File name                                   |

The path to a directory that contains files containing certificate revocation lists.

<span id="page-46-2"></span>• [group\\_replication\\_recovery\\_ssl\\_crlpath](#page-46-2)

| Command-Line Format | group-replication-recovery-ssl<br>crlpath=value |  |
|---------------------|-------------------------------------------------|--|
| System Variable     | group_replication_recovery_ssl_crlpath          |  |
| Scope               | Global                                          |  |
| Dynamic             | Yes                                             |  |
| Type                | Directory name                                  |  |

The path to a directory that contains files containing certificate revocation lists.

<span id="page-46-3"></span>• [group\\_replication\\_recovery\\_ssl\\_verify\\_server\\_cert](#page-46-3)

| Command-Line Format | group-replication-recovery-ssl<br>verify-server-cert[={OFF ON}] |  |
|---------------------|-----------------------------------------------------------------|--|
| System Variable     | group_replication_recovery_ssl_verify_server_cert               |  |
| Scope               | Global                                                          |  |
| Dynamic             | Yes                                                             |  |
| Type                | Boolean                                                         |  |
| Default Value       | OFF                                                             |  |

Make the recovery process check the server's Common Name value in the donor sent certificate.

<span id="page-47-2"></span>• [group\\_replication\\_recovery\\_use\\_ssl](#page-47-2)

| Command-Line Format | group-replication-recovery-use<br>ssl[={OFF ON}] |
|---------------------|--------------------------------------------------|
| System Variable     | group_replication_recovery_use_ssl               |
| Scope               | Global                                           |
| Dynamic             | Yes                                              |
| Type                | Boolean                                          |
| Default Value       | OFF                                              |

Whether Group Replication recovery connection should use SSL or not.

<span id="page-47-0"></span>• [group\\_replication\\_single\\_primary\\_mode](#page-47-0)

| Command-Line Format | group-replication-single-primary<br>mode[={OFF ON}] |  |
|---------------------|-----------------------------------------------------|--|
| System Variable     | group_replication_single_primary_mode               |  |
| Scope               | Global                                              |  |
| Dynamic             | Yes                                                 |  |
| Type                | Boolean                                             |  |
| Default Value       | ON                                                  |  |

![](_page_47_Picture_6.jpeg)

#### **Note**

This system variable is a group-wide configuration setting, and a full reboot of the replication group is required for a change to take effect.

[group\\_replication\\_single\\_primary\\_mode](#page-47-0) instructs the group to pick a single server automatically to be the one that handles read/write workload. This server is the primary and all others are secondaries.

This system variable is a group-wide configuration setting. It must have the same value on all group members, cannot be changed while Group Replication is running, and requires a full reboot of the group (a bootstrap by a server with [group\\_replication\\_bootstrap\\_group=ON](#page-33-0)) in order for the value change to take effect. For instructions to safely bootstrap a group where transactions have been executed and certified, see [Section 17.5.4, "Restarting a Group".](#page-19-0)

If the group has a value set for this system variable, and a joining member has a different value set for the system variable, the joining member cannot join the group until the value is changed to match. If the group members have a value set for this system variable, and the joining member does not support the system variable, it cannot join the group.

Setting this variable ON causes any setting for [group\\_replication\\_auto\\_increment\\_increment](#page-33-1) to be ignored.

• [group\\_replication\\_ssl\\_mode](#page-47-1)

<span id="page-47-1"></span>

|      | Command-Line Format | group-replication-ssl-mode=value |  |
|------|---------------------|----------------------------------|--|
|      | System Variable     | group_replication_ssl_mode       |  |
|      | Scope               | Global                           |  |
|      | Dynamic             | Yes                              |  |
|      | Type                | Enumeration                      |  |
| 3020 | Default Value       | DISABLED                         |  |

| Valid Values | DISABLED        |
|--------------|-----------------|
|              | REQUIRED        |
|              | VERIFY_CA       |
|              | VERIFY_IDENTITY |

Specifies the security state of the connection between Group Replication members.

<span id="page-48-1"></span>• [group\\_replication\\_start\\_on\\_boot](#page-48-1)

| Command-Line Format | group-replication-start-on<br>boot[={OFF ON}] |
|---------------------|-----------------------------------------------|
| System Variable     | group_replication_start_on_boot               |
| Scope               | Global                                        |
| Dynamic             | Yes                                           |
| Type                | Boolean                                       |
| Default Value       | ON                                            |

Whether the server should start Group Replication or not during server start.

<span id="page-48-0"></span>• [group\\_replication\\_transaction\\_size\\_limit](#page-48-0)

| Command-Line Format | group-replication-transaction<br>size-limit=# |
|---------------------|-----------------------------------------------|
| System Variable     | group_replication_transaction_size_limit      |
| Scope               | Global                                        |
| Dynamic             | Yes                                           |
| Type                | Integer                                       |
| Default Value       | 150000000                                     |
| Minimum Value       | 0                                             |
| Maximum Value       | 2147483647                                    |
| Unit                | bytes                                         |

Configures the maximum transaction size in bytes which the replication group accepts. Transactions larger than this size are rolled back by the receiving member and are not broadcast to the group. Large transactions can cause problems for a replication group in terms of memory allocation, which can cause the system to slow down, or in terms of network bandwidth consumption, which can cause a member to be suspected of having failed because it is busy processing the large transaction.

When this system variable is set to 0, there is no limit to the size of transactions the group accepts. In releases up to and including MySQL 5.7.37, the default setting for this system variable is 0. From MySQL 5.7.38, and in MySQL 8.0, the default setting is 150000000 bytes (approximately 143 MB). Adjust the value of this system variable depending on the maximum message size that you need the group to tolerate, bearing in mind that the time taken to process a transaction is proportional to its size. The value of [group\\_replication\\_transaction\\_size\\_limit](#page-48-0) should be the same on all group members. For further mitigation strategies for large transactions, see [Section 17.3.2, "Group](#page-7-0) [Replication Limitations"](#page-7-0).

<span id="page-48-2"></span>• [group\\_replication\\_unreachable\\_majority\\_timeout](#page-48-2)

| Command-Line Format | group-replication-unreachable |
|---------------------|-------------------------------|
|                     | majority-timeout=#            |

| System Variable | group_replication_unreachable_majority_timeout |  |
|-----------------|------------------------------------------------|--|
| Scope           | Global                                         |  |
| Dynamic         | Yes                                            |  |
| Type            | Integer                                        |  |
| Default Value   | 0                                              |  |
| Minimum Value   | 0                                              |  |
| Maximum Value   | 31536000                                       |  |
| Unit            | seconds                                        |  |

Configures how long members that suffer a network partition and cannot connect to the majority wait before leaving the group.

In a group of 5 servers (S1,S2,S3,S4,S5), if there is a disconnection between (S1,S2) and (S3,S4,S5) there is a network partition. The first group (S1,S2) is now in a minority because it cannot contact more than half of the group. While the majority group (S3,S4,S5) remains running, the minority group waits for the specified time for a network reconnection. Any transactions processed by the minority group are blocked until Group Replication is stopped using STOP GROUP REPLICATION on the members of the minority. Note that [group\\_replication\\_unreachable\\_majority\\_timeout](#page-48-2) has no effect if it is set on the servers in the minority group after the loss of majority has been detected.

By default, this system variable is set to 0, which means that members that find themselves in a minority due to a network partition wait forever to leave the group. If configured to a number of seconds, members wait for this amount of time after losing contact with the majority of members before leaving the group. When the specified time elapses, all pending transactions processed by the minority are rolled back, and the servers in the minority partition move to the ERROR state. These servers then follow the action specified by the system variable [group\\_replication\\_exit\\_state\\_action](#page-35-1), which can be to set themselves to super read only mode or shut down MySQL.

![](_page_49_Picture_5.jpeg)

#### **Warning**

When you have a symmetric group, with just two members for example (S0,S2), if there is a network partition and there is no majority, after the configured timeout all members enter ERROR state.

# <span id="page-49-0"></span>**17.7.2 Group Replication Status Variables**

MySQL 5.7 supports one status variable providing information about Group Replication. This variable is described here:

• group\_replication\_primary\_member

Shows the primary member's UUID when the group is operating in single-primary mode. If the group is operating in multi-primary mode, shows an empty string. See [Section 17.5.1.3, "Finding the](#page-13-0) [Primary".](#page-13-0)