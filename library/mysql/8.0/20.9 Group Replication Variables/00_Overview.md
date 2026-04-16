---
source: MySQL 8.0 Reference
title: 00_Overview
---

The next two sections contain information about MySQL server system and server status variables which are specific to the Group Replication plugin.

**Table 20.4 Group Replication Variable and Option Summary**

| Name | Cmd-Line                                                   | Option File | System Var | Status Var | Var Scope | Dynamic |
|------|------------------------------------------------------------|-------------|------------|------------|-----------|---------|
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
|      | group_replication_ip_whitelist<br>Yes                      | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_local_address<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_member_expel_timeout<br>Yes              | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_member_weight<br>Yes                     | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_message_cache_size<br>Yes                | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_paxos_single_leader<br>Yes               | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_poll_spin_loops<br>Yes                   | Yes         | Yes        |            | Global    | Yes     |
|      | group_replication_primary_member                           |             |            | Yes        | Global    | No      |
|      | group_replication_recovery_complete_at<br>Yes              | Yes         | Yes        |            | Global    | Yes     |

| Name | Cmd-Line                                        | Option File                                              | System Var | Status Var | Var Scope | Dynamic |
|------|-------------------------------------------------|----------------------------------------------------------|------------|------------|-----------|---------|
|      | Yes                                             | group_replication_recovery_get_public_key<br>Yes         | Yes        |            | Global    | Yes     |
|      | Yes                                             | group_replication_recovery_public_key_path<br>Yes        | Yes        |            | Global    | Yes     |
|      | Yes                                             | group_replication_recovery_reconnect_interval<br>Yes     | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_retry_count<br>Yes   | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_ca<br>Yes        | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_capath<br>Yes    | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cert<br>Yes      | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_cipher<br>Yes    | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crl<br>Yes       | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_crlpath<br>Yes   | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_ssl_key<br>Yes       | Yes                                                      | Yes        |            | Global    | Yes     |
|      | Yes                                             | group_replication_recovery_ssl_verify_server_cert<br>Yes | Yes        |            | Global    | Yes     |
|      | Yes                                             | group_replication_recovery_tls_ciphersuites<br>Yes       | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_tls_version<br>Yes   | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_recovery_use_ssl<br>Yes       | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_single_primary_mode<br>Yes    | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_ssl_mode<br>Yes               | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_start_on_boot<br>Yes          | Yes                                                      | Yes        |            | Global    | Yes     |
|      | group_replication_transaction_size_limit<br>Yes | Yes                                                      | Yes        |            | Global    | Yes     |
|      | Yes                                             | group_replication_unreachable_majority_timeout<br>Yes    | Yes        |            | Global    | Yes     |
|      | group_replication_view_change_uuid<br>Yes       | Yes                                                      | Yes        |            | Global    | Yes     |