---
source: MySQL 8.4 Reference
title: 00_Overview
---

The functions described in the following sections are used with MySQL Replication.

**Table 14.24 Replication Functions**

| Name                                              | Description                                                                                            | Deprecated |
|---------------------------------------------------|--------------------------------------------------------------------------------------------------------|------------|
| asynchronous_connection_failover_add_managed()    | Add group member source<br>server configuration information<br>to a replication channel source<br>list |            |
| asynchronous_connection_failover_add_source()     | Add source server configuration<br>information server to a replication<br>channel source list          |            |
| asynchronous_connection_failover_delete_managed() | Remove a managed group from<br>a replication channel source list                                       |            |
| asynchronous_connection_failover_delete_source()  | Remove a source server from a<br>replication channel source list                                       |            |
| asynchronous_connection_failover_reset()          | Remove all settings relating to<br>group replication asynchronous<br>failover                          |            |
| group_replication_disable_member_action()         | Disable member action for event<br>specified                                                           |            |
| group_replication_enable_member_action()          | Enable member action for event<br>specified                                                            |            |
| group_replication_get_communication_protocol()    | Get version of group replication<br>communication protocol currently<br>in use                         |            |
| group_replication_get_write_concurrency()         | Get maximum number of<br>consensus instances currently<br>set for group                                |            |
| group_replication_reset_member_actions()          | Reset all member actions to<br>defaults and configuration<br>version number to 1                       |            |
| group_replication_set_as_primary()                | Make a specific group member<br>the primary                                                            |            |
| group_replication_set_communication_protocol()    | Set version for group replication<br>communication protocol to use                                     |            |

| Name                                                         | Description                                                                                 | Deprecated |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------------|------------|
| group_replication_set_write_concurrency()                    | Set maximum number of<br>consensus instances that can be<br>executed in parallel            |            |
| group_replication_switch_to_multi_primary_mode()             | Changes the mode of a group<br>running in single-primary mode<br>to multi-primary mode      |            |
| group_replication_switch_to_single_primary_mode()            | Changes the mode of a group<br>running in multi-primary mode to<br>single-primary mode      |            |
| MASTER_POS_WAIT()                                            | Block until the replica has read<br>and applied all updates up to the<br>specified position | Yes        |
| SOURCE_POS_WAIT()                                            | Block until the replica has read<br>and applied all updates up to the<br>specified position |            |
| WAIT_FOR_EXECUTED_GTID_SET() Wait until the given GTIDs have | executed on the replica.                                                                    |            |