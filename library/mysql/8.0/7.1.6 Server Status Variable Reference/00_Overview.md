---
source: MySQL 8.0 Reference
title: 00_Overview
---

The following table lists all status variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting and using the variables. Where appropriate, direct links to further information about the items are provided.

**Table 7.3 Status Variable Summary**

| Variable Name                               | Variable Type | Variable Scope |
|---------------------------------------------|---------------|----------------|
| Aborted_clients                             | Integer       | Global         |
| Aborted_connects                            | Integer       | Global         |
| Acl_cache_items_count                       | Integer       | Global         |
| Audit_log_current_size                      | Integer       | Global         |
| Audit_log_event_max_drop_size               | Integer       | Global         |
| Audit_log_events                            | Integer       | Global         |
| Audit_log_events_filtered                   | Integer       | Global         |
| Audit_log_events_lost                       | Integer       | Global         |
| Audit_log_events_written                    | Integer       | Global         |
| Audit_log_total_size                        | Integer       | Global         |
| Audit_log_write_waits                       | Integer       | Global         |
| Authentication_ldap_sasl_supported_methods  | String        | Global         |
| Binlog_cache_disk_use                       | Integer       | Global         |
| Binlog_cache_use                            | Integer       | Global         |
| Binlog_stmt_cache_disk_use                  | Integer       | Global         |
| Binlog_stmt_cache_use                       | Integer       | Global         |
| Bytes_received                              | Integer       | Both           |
| Bytes_sent                                  | Integer       | Both           |
| Caching_sha2_password_rsa_public_key String |               | Global         |
| Com_admin_commands                          | Integer       | Both           |
| Com_alter_db                                | Integer       | Both           |
| Com_alter_event                             | Integer       | Both           |
| Com_alter_function                          | Integer       | Both           |

| Variable Name                 | Variable Type | Variable Scope |
|-------------------------------|---------------|----------------|
| Com_alter_procedure           | Integer       | Both           |
| Com_alter_resource_group      | Integer       | Global         |
| Com_alter_server              | Integer       | Both           |
| Com_alter_table               | Integer       | Both           |
| Com_alter_tablespace          | Integer       | Both           |
| Com_alter_user                | Integer       | Both           |
| Com_alter_user_default_role   | Integer       | Global         |
| Com_analyze                   | Integer       | Both           |
| Com_assign_to_keycache        | Integer       | Both           |
| Com_begin                     | Integer       | Both           |
| Com_binlog                    | Integer       | Both           |
| Com_call_procedure            | Integer       | Both           |
| Com_change_db                 | Integer       | Both           |
| Com_change_master             | Integer       | Both           |
| Com_change_repl_filter        | Integer       | Both           |
| Com_change_replication_source | Integer       | Both           |
| Com_check                     | Integer       | Both           |
| Com_checksum                  | Integer       | Both           |
| Com_clone                     | Integer       | Global         |
| Com_commit                    | Integer       | Both           |
| Com_create_db                 | Integer       | Both           |
| Com_create_event              | Integer       | Both           |
| Com_create_function           | Integer       | Both           |
| Com_create_index              | Integer       | Both           |
| Com_create_procedure          | Integer       | Both           |
| Com_create_resource_group     | Integer       | Global         |
| Com_create_role               | Integer       | Global         |
| Com_create_server             | Integer       | Both           |
| Com_create_table              | Integer       | Both           |
| Com_create_trigger            | Integer       | Both           |
| Com_create_udf                | Integer       | Both           |
| Com_create_user               | Integer       | Both           |
| Com_create_view               | Integer       | Both           |
| Com_dealloc_sql               | Integer       | Both           |
| Com_delete                    | Integer       | Both           |
| Com_delete_multi              | Integer       | Both           |
| Com_do                        | Integer       | Both           |
| Com_drop_db                   | Integer       | Both           |
| Com_drop_event                | Integer       | Both           |
| Com_drop_function             | Integer       | Both           |
| Com_drop_index                | Integer       | Both           |

| Variable Name               | Variable Type | Variable Scope |
|-----------------------------|---------------|----------------|
| Com_drop_procedure          | Integer       | Both           |
| Com_drop_resource_group     | Integer       | Global         |
| Com_drop_role               | Integer       | Global         |
| Com_drop_server             | Integer       | Both           |
| Com_drop_table              | Integer       | Both           |
| Com_drop_trigger            | Integer       | Both           |
| Com_drop_user               | Integer       | Both           |
| Com_drop_view               | Integer       | Both           |
| Com_empty_query             | Integer       | Both           |
| Com_execute_sql             | Integer       | Both           |
| Com_explain_other           | Integer       | Both           |
| Com_flush                   | Integer       | Both           |
| Com_get_diagnostics         | Integer       | Both           |
| Com_grant                   | Integer       | Both           |
| Com_grant_roles             | Integer       | Global         |
| Com_group_replication_start | Integer       | Global         |
| Com_group_replication_stop  | Integer       | Global         |
| Com_ha_close                | Integer       | Both           |
| Com_ha_open                 | Integer       | Both           |
| Com_ha_read                 | Integer       | Both           |
| Com_help                    | Integer       | Both           |
| Com_insert                  | Integer       | Both           |
| Com_insert_select           | Integer       | Both           |
| Com_install_component       | Integer       | Global         |
| Com_install_plugin          | Integer       | Both           |
| Com_kill                    | Integer       | Both           |
| Com_load                    | Integer       | Both           |
| Com_lock_tables             | Integer       | Both           |
| Com_optimize                | Integer       | Both           |
| Com_preload_keys            | Integer       | Both           |
| Com_prepare_sql             | Integer       | Both           |
| Com_purge                   | Integer       | Both           |
| Com_purge_before_date       | Integer       | Both           |
| Com_release_savepoint       | Integer       | Both           |
| Com_rename_table            | Integer       | Both           |
| Com_rename_user             | Integer       | Both           |
| Com_repair                  | Integer       | Both           |
| Com_replace                 | Integer       | Both           |
| Com_replace_select          | Integer       | Both           |
| Com_replica_start           | Integer       | Both           |
| Com_replica_stop            | Integer       | Both           |

| Variable Name             | Variable Type | Variable Scope |
|---------------------------|---------------|----------------|
| Com_reset                 | Integer       | Both           |
| Com_resignal              | Integer       | Both           |
| Com_restart               | Integer       | Both           |
| Com_revoke                | Integer       | Both           |
| Com_revoke_all            | Integer       | Both           |
| Com_revoke_roles          | Integer       | Global         |
| Com_rollback              | Integer       | Both           |
| Com_rollback_to_savepoint | Integer       | Both           |
| Com_savepoint             | Integer       | Both           |
| Com_select                | Integer       | Both           |
| Com_set_option            | Integer       | Both           |
| Com_set_resource_group    | Integer       | Global         |
| Com_set_role              | Integer       | Global         |
| Com_show_authors          | Integer       | Both           |
| Com_show_binlog_events    | Integer       | Both           |
| Com_show_binlogs          | Integer       | Both           |
| Com_show_charsets         | Integer       | Both           |
| Com_show_collations       | Integer       | Both           |
| Com_show_contributors     | Integer       | Both           |
| Com_show_create_db        | Integer       | Both           |
| Com_show_create_event     | Integer       | Both           |
| Com_show_create_func      | Integer       | Both           |
| Com_show_create_proc      | Integer       | Both           |
| Com_show_create_table     | Integer       | Both           |
| Com_show_create_trigger   | Integer       | Both           |
| Com_show_create_user      | Integer       | Both           |
| Com_show_databases        | Integer       | Both           |
| Com_show_engine_logs      | Integer       | Both           |
| Com_show_engine_mutex     | Integer       | Both           |
| Com_show_engine_status    | Integer       | Both           |
| Com_show_errors           | Integer       | Both           |
| Com_show_events           | Integer       | Both           |
| Com_show_fields           | Integer       | Both           |
| Com_show_function_code    | Integer       | Both           |
| Com_show_function_status  | Integer       | Both           |
| Com_show_grants           | Integer       | Both           |
| Com_show_keys             | Integer       | Both           |
| Com_show_master_status    | Integer       | Both           |
| Com_show_ndb_status       | Integer       | Both           |
| Com_show_open_tables      | Integer       | Both           |
| Com_show_plugins          | Integer       | Both           |

| Variable Name             | Variable Type | Variable Scope |
|---------------------------|---------------|----------------|
| Com_show_privileges       | Integer       | Both           |
| Com_show_procedure_code   | Integer       | Both           |
| Com_show_procedure_status | Integer       | Both           |
| Com_show_processlist      | Integer       | Both           |
| Com_show_profile          | Integer       | Both           |
| Com_show_profiles         | Integer       | Both           |
| Com_show_relaylog_events  | Integer       | Both           |
| Com_show_replica_status   | Integer       | Both           |
| Com_show_replicas         | Integer       | Both           |
| Com_show_slave_hosts      | Integer       | Both           |
| Com_show_slave_status     | Integer       | Both           |
| Com_show_status           | Integer       | Both           |
| Com_show_storage_engines  | Integer       | Both           |
| Com_show_table_status     | Integer       | Both           |
| Com_show_tables           | Integer       | Both           |
| Com_show_triggers         | Integer       | Both           |
| Com_show_variables        | Integer       | Both           |
| Com_show_warnings         | Integer       | Both           |
| Com_shutdown              | Integer       | Both           |
| Com_signal                | Integer       | Both           |
| Com_slave_start           | Integer       | Both           |
| Com_slave_stop            | Integer       | Both           |
| Com_stmt_close            | Integer       | Both           |
| Com_stmt_execute          | Integer       | Both           |
| Com_stmt_fetch            | Integer       | Both           |
| Com_stmt_prepare          | Integer       | Both           |
| Com_stmt_reprepare        | Integer       | Both           |
| Com_stmt_reset            | Integer       | Both           |
| Com_stmt_send_long_data   | Integer       | Both           |
| Com_truncate              | Integer       | Both           |
| Com_uninstall_component   | Integer       | Global         |
| Com_uninstall_plugin      | Integer       | Both           |
| Com_unlock_tables         | Integer       | Both           |
| Com_update                | Integer       | Both           |
| Com_update_multi          | Integer       | Both           |
| Com_xa_commit             | Integer       | Both           |
| Com_xa_end                | Integer       | Both           |
| Com_xa_prepare            | Integer       | Both           |
| Com_xa_recover            | Integer       | Both           |
| Com_xa_rollback           | Integer       | Both           |
| Com_xa_start              | Integer       | Both           |

| Variable Name                              | Variable Type  | Variable Scope |
|--------------------------------------------|----------------|----------------|
| Compression                                | Integer        | Session        |
| Compression_algorithm                      | String         | Global         |
| Compression_level                          | Integer        | Global         |
| Connection_control_delay_generated Integer |                | Global         |
| Connection_errors_accept                   | Integer        | Global         |
| Connection_errors_internal                 | Integer        | Global         |
| Connection_errors_max_connections Iteger   |                | Global         |
| Connection_errors_peer_address Integer     |                | Global         |
| Connection_errors_select                   | Integer        | Global         |
| Connection_errors_tcpwrap                  | Integer        | Global         |
| Connections                                | Integer        | Global         |
| Created_tmp_disk_tables                    | Integer        | Both           |
| Created_tmp_files                          | Integer        | Global         |
| Created_tmp_tables                         | Integer        | Both           |
| Current_tls_ca                             | File name      | Global         |
| Current_tls_capath                         | Directory name | Global         |
| Current_tls_cert                           | File name      | Global         |
| Current_tls_cipher                         | String         | Global         |
| Current_tls_ciphersuites                   | String         | Global         |
| Current_tls_crl                            | File name      | Global         |
| Current_tls_crlpath                        | Directory name | Global         |
| Current_tls_key                            | File name      | Global         |
| Current_tls_version                        | String         | Global         |
| Delayed_errors                             | Integer        | Global         |
| Delayed_insert_threads                     | Integer        | Global         |
| Delayed_writes                             | Integer        | Global         |
| dragnet.Status                             | String         | Global         |
| Error_log_buffered_bytes                   | Integer        | Global         |
| Error_log_buffered_events                  | Integer        | Global         |
| Error_log_expired_events                   | Integer        | Global         |
| Error_log_latest_write                     | Integer        | Global         |
| Firewall_access_denied                     | Integer        | Global         |
| Firewall_access_granted                    | Integer        | Global         |
| Firewall_access_suspicious                 | Integer        | Global         |
| Firewall_cached_entries                    | Integer        | Global         |
| Flush_commands                             | Integer        | Global         |
| Global_connection_memory                   | Integer        | Global         |
| group_replication_primary_memberString     |                | Global         |
| Handler_commit                             | Integer        | Both           |
| Handler_delete                             | Integer        | Both           |
| Handler_discover                           | Integer        | Both           |

| Variable Name                                 | Variable Type | Variable Scope |
|-----------------------------------------------|---------------|----------------|
| Handler_external_lock                         | Integer       | Both           |
| Handler_mrr_init                              | Integer       | Both           |
| Handler_prepare                               | Integer       | Both           |
| Handler_read_first                            | Integer       | Both           |
| Handler_read_key                              | Integer       | Both           |
| Handler_read_last                             | Integer       | Both           |
| Handler_read_next                             | Integer       | Both           |
| Handler_read_prev                             | Integer       | Both           |
| Handler_read_rnd                              | Integer       | Both           |
| Handler_read_rnd_next                         | Integer       | Both           |
| Handler_rollback                              | Integer       | Both           |
| Handler_savepoint                             | Integer       | Both           |
| Handler_savepoint_rollback                    | Integer       | Both           |
| Handler_update                                | Integer       | Both           |
| Handler_write                                 | Integer       | Both           |
| Innodb_buffer_pool_bytes_data                 | Integer       | Global         |
| Innodb_buffer_pool_bytes_dirty                | Integer       | Global         |
| Innodb_buffer_pool_dump_status String         |               | Global         |
| Innodb_buffer_pool_load_status                | String        | Global         |
| Innodb_buffer_pool_pages_data                 | Integer       | Global         |
| Innodb_buffer_pool_pages_dirty                | Integer       | Global         |
| Innodb_buffer_pool_pages_flushedInteger       |               | Global         |
| Innodb_buffer_pool_pages_free                 | Integer       | Global         |
| Innodb_buffer_pool_pages_latchedInteger       |               | Global         |
| Innodb_buffer_pool_pages_misc                 | Integer       | Global         |
| Innodb_buffer_pool_pages_total                | Integer       | Global         |
| Innodb_buffer_pool_read_ahead                 | Integer       | Global         |
| Innodb_buffer_pool_read_ahead_evicted Integer |               | Global         |
| Innodb_buffer_pool_read_ahead_rndInteger      |               | Global         |
| Innodb_buffer_pool_read_requestsInteger       |               | Global         |
| Innodb_buffer_pool_reads                      | Integer       | Global         |
| Innodb_buffer_pool_resize_status String       |               | Global         |
| Innodb_buffer_pool_resize_status_code Integer |               | Global         |
| Innodb_buffer_pool_resize_status_progress     | Integer       | Global         |
| Innodb_buffer_pool_wait_free                  | Integer       | Global         |
| Innodb_buffer_pool_write_requestsInteger      |               | Global         |
| Innodb_data_fsyncs                            | Integer       | Global         |
| Innodb_data_pending_fsyncs                    | Integer       | Global         |
| Innodb_data_pending_reads                     | Integer       | Global         |
| Innodb_data_pending_writes                    | Integer       | Global         |
| Innodb_data_read                              | Integer       | Global         |

| Variable Name                               | Variable Type | Variable Scope |
|---------------------------------------------|---------------|----------------|
| Innodb_data_reads                           | Integer       | Global         |
| Innodb_data_writes                          | Integer       | Global         |
| Innodb_data_written                         | Integer       | Global         |
| Innodb_dblwr_pages_written                  | Integer       | Global         |
| Innodb_dblwr_writes                         | Integer       | Global         |
| Innodb_have_atomic_builtins                 | Integer       | Global         |
| Innodb_log_waits                            | Integer       | Global         |
| Innodb_log_write_requests                   | Integer       | Global         |
| Innodb_log_writes                           | Integer       | Global         |
| Innodb_num_open_files                       | Integer       | Global         |
| Innodb_os_log_fsyncs                        | Integer       | Global         |
| Innodb_os_log_pending_fsyncs                | Integer       | Global         |
| Innodb_os_log_pending_writes                | Integer       | Global         |
| Innodb_os_log_written                       | Integer       | Global         |
| Innodb_page_size                            | Integer       | Global         |
| Innodb_pages_created                        | Integer       | Global         |
| Innodb_pages_read                           | Integer       | Global         |
| Innodb_pages_written                        | Integer       | Global         |
| Innodb_redo_log_capacity_resizedInteger     |               | Global         |
| Innodb_redo_log_checkpoint_lsn Integer      |               | Global         |
| Innodb_redo_log_current_lsn                 | Integer       | Global         |
| Innodb_redo_log_enabled                     | Boolean       | Global         |
| Innodb_redo_log_flushed_to_disk_lsn Integer |               | Global         |
| Innodb_redo_log_logical_size                | Integer       | Global         |
| Innodb_redo_log_physical_size               | Boolean       | Global         |
| Innodb_redo_log_read_only                   | Boolean       | Global         |
| Innodb_redo_log_resize_status               | String        | Global         |
| Innodb_redo_log_uuid                        | Integer       | Global         |
| Innodb_row_lock_current_waits               | Integer       | Global         |
| Innodb_row_lock_time                        | Integer       | Global         |
| Innodb_row_lock_time_avg                    | Integer       | Global         |
| Innodb_row_lock_time_max                    | Integer       | Global         |
| Innodb_row_lock_waits                       | Integer       | Global         |
| Innodb_rows_deleted                         | Integer       | Global         |
| Innodb_rows_inserted                        | Integer       | Global         |
| Innodb_rows_read                            | Integer       | Global         |
| Innodb_rows_updated                         | Integer       | Global         |
| Innodb_system_rows_deleted                  | Integer       | Global         |
| Innodb_system_rows_inserted                 | Integer       | Global         |
| Innodb_system_rows_read                     | Integer       | Global         |
| Innodb_system_rows_updated                  | Integer       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Innodb_truncated_status_writes               | Integer       | Global         |
| Innodb_undo_tablespaces_active Integer       |               | Global         |
| Innodb_undo_tablespaces_explicitInteger      |               | Global         |
| Innodb_undo_tablespaces_implicitInteger      |               | Global         |
| Innodb_undo_tablespaces_total                | Integer       | Global         |
| Key_blocks_not_flushed                       | Integer       | Global         |
| Key_blocks_unused                            | Integer       | Global         |
| Key_blocks_used                              | Integer       | Global         |
| Key_read_requests                            | Integer       | Global         |
| Key_reads                                    | Integer       | Global         |
| Key_write_requests                           | Integer       | Global         |
| Key_writes                                   | Integer       | Global         |
| Last_query_cost                              | Numeric       | Session        |
| Last_query_partial_plans                     | Integer       | Session        |
| Locked_connects                              | Integer       | Global         |
| Max_execution_time_exceeded                  | Integer       | Both           |
| Max_execution_time_set                       | Integer       | Both           |
| Max_execution_time_set_failed                | Integer       | Both           |
| Max_used_connections                         | Integer       | Global         |
| Max_used_connections_time                    | Datetime      | Global         |
| mecab_charset                                | String        | Global         |
| Mysqlx_aborted_clients                       | Integer       | Global         |
| Mysqlx_address                               | String        | Global         |
| Mysqlx_bytes_received                        | Integer       | Both           |
| Mysqlx_bytes_received_compressed_payload     | Integer       | Both           |
| Mysqlx_bytes_received_uncompressed_frame     | Integer       | Both           |
| Mysqlx_bytes_sent                            | Integer       | Both           |
| Mysqlx_bytes_sent_compressed_payload Integer |               | Both           |
| Mysqlx_bytes_sent_uncompressed_frame Integer |               | Both           |
| Mysqlx_compression_algorithm                 | String        | Session        |
| Mysqlx_compression_level                     | String        | Session        |
| Mysqlx_connection_accept_errorsInteger       |               | Both           |
| Mysqlx_connection_errors                     | Integer       | Both           |
| Mysqlx_connections_accepted                  | Integer       | Global         |
| Mysqlx_connections_closed                    | Integer       | Global         |
| Mysqlx_connections_rejected                  | Integer       | Global         |
| Mysqlx_crud_create_view                      | Integer       | Both           |
| Mysqlx_crud_delete                           | Integer       | Both           |
| Mysqlx_crud_drop_view                        | Integer       | Both           |
| Mysqlx_crud_find                             | Integer       | Both           |
| Mysqlx_crud_insert                           | Integer       | Both           |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Mysqlx_crud_modify_view                      | Integer       | Both           |
| Mysqlx_crud_update                           | Integer       | Both           |
| Mysqlx_cursor_close                          | Integer       | Both           |
| Mysqlx_cursor_fetch                          | Integer       | Both           |
| Mysqlx_cursor_open                           | Integer       | Both           |
| Mysqlx_errors_sent                           | Integer       | Both           |
| Mysqlx_errors_unknown_message_type Integer   |               | Both           |
| Mysqlx_expect_close                          | Integer       | Both           |
| Mysqlx_expect_open                           | Integer       | Both           |
| Mysqlx_init_error                            | Integer       | Both           |
| Mysqlx_messages_sent                         | Integer       | Both           |
| Mysqlx_notice_global_sent                    | Integer       | Both           |
| Mysqlx_notice_other_sent                     | Integer       | Both           |
| Mysqlx_notice_warning_sent                   | Integer       | Both           |
| Mysqlx_notified_by_group_replication Integer |               | Both           |
| Mysqlx_port                                  | String        | Global         |
| Mysqlx_prep_deallocate                       | Integer       | Both           |
| Mysqlx_prep_execute                          | Integer       | Both           |
| Mysqlx_prep_prepare                          | Integer       | Both           |
| Mysqlx_rows_sent                             | Integer       | Both           |
| Mysqlx_sessions                              | Integer       | Global         |
| Mysqlx_sessions_accepted                     | Integer       | Global         |
| Mysqlx_sessions_closed                       | Integer       | Global         |
| Mysqlx_sessions_fatal_error                  | Integer       | Global         |
| Mysqlx_sessions_killed                       | Integer       | Global         |
| Mysqlx_sessions_rejected                     | Integer       | Global         |
| Mysqlx_socket                                | String        | Global         |
| Mysqlx_ssl_accept_renegotiates               | Integer       | Global         |
| Mysqlx_ssl_accepts                           | Integer       | Global         |
| Mysqlx_ssl_active                            | Integer       | Both           |
| Mysqlx_ssl_cipher                            | Integer       | Both           |
| Mysqlx_ssl_cipher_list                       | Integer       | Both           |
| Mysqlx_ssl_ctx_verify_depth                  | Integer       | Both           |
| Mysqlx_ssl_ctx_verify_mode                   | Integer       | Both           |
| Mysqlx_ssl_finished_accepts                  | Integer       | Global         |
| Mysqlx_ssl_server_not_after                  | Integer       | Global         |
| Mysqlx_ssl_server_not_before                 | Integer       | Global         |
| Mysqlx_ssl_verify_depth                      | Integer       | Global         |
| Mysqlx_ssl_verify_mode                       | Integer       | Global         |
| Mysqlx_ssl_version                           | Integer       | Both           |
| Mysqlx_stmt_create_collection                | Integer       | Both           |

| Variable Name                                 | Variable Type | Variable Scope |
|-----------------------------------------------|---------------|----------------|
| Mysqlx_stmt_create_collection_index Integer   |               | Both           |
| Mysqlx_stmt_disable_notices                   | Integer       | Both           |
| Mysqlx_stmt_drop_collection                   | Integer       | Both           |
| Mysqlx_stmt_drop_collection_indexInteger      |               | Both           |
| Mysqlx_stmt_enable_notices                    | Integer       | Both           |
| Mysqlx_stmt_ensure_collection                 | String        | Both           |
| Mysqlx_stmt_execute_mysqlx                    | Integer       | Both           |
| Mysqlx_stmt_execute_sql                       | Integer       | Both           |
| Mysqlx_stmt_execute_xplugin                   | Integer       | Both           |
| Mysqlx_stmt_get_collection_optionsInteger     |               | Both           |
| Mysqlx_stmt_kill_client                       | Integer       | Both           |
| Mysqlx_stmt_list_clients                      | Integer       | Both           |
| Mysqlx_stmt_list_notices                      | Integer       | Both           |
| Mysqlx_stmt_list_objects                      | Integer       | Both           |
| Mysqlx_stmt_modify_collection_options Integer |               | Both           |
| Mysqlx_stmt_ping                              | Integer       | Both           |
| Mysqlx_worker_threads                         | Integer       | Global         |
| Mysqlx_worker_threads_active                  | Integer       | Global         |
| Ndb_api_adaptive_send_deferred_count Integer  |               | Global         |
| Ndb_api_adaptive_send_deferred_count_replica  | Integer       | Global         |
| Ndb_api_adaptive_send_deferred_count_session  | Integer       | Global         |
| Ndb_api_adaptive_send_deferred_count_slave    | Integer       | Global         |
| Ndb_api_adaptive_send_forced_count Integer    |               | Global         |
| Ndb_api_adaptive_send_forced_count_replica    | Integer       | Global         |
| Ndb_api_adaptive_send_forced_count_session    | Integer       | Global         |
| Ndb_api_adaptive_send_forced_count_slave      | Integer       | Global         |
| Ndb_api_adaptive_send_unforced_count Integer  |               | Global         |
| Ndb_api_adaptive_send_unforced_count_replica  | Integer       | Global         |
| Ndb_api_adaptive_send_unforced_count_session  | Integer       | Global         |
| Ndb_api_adaptive_send_unforced_count_slave    | Integer       | Global         |
| Ndb_api_bytes_received_count                  | Integer       | Global         |
| Ndb_api_bytes_received_count_replica Integer  |               | Global         |
| Ndb_api_bytes_received_count_session Integer  |               | Session        |
| Ndb_api_bytes_received_count_slave Intger     |               | Global         |
| Ndb_api_bytes_sent_count                      | Integer       | Global         |
| Ndb_api_bytes_sent_count_replicaInteger       |               | Global         |
| Ndb_api_bytes_sent_count_sessionIteger        |               | Session        |
| Ndb_api_bytes_sent_count_slave Integer        |               | Global         |
| Ndb_api_event_bytes_count                     | Integer       | Global         |
| Ndb_api_event_bytes_count_injector Integer    |               | Global         |
| Ndb_api_event_data_count                      | Integer       | Global         |

| Variable Name                                | Variable Type | Variable Scope |
|----------------------------------------------|---------------|----------------|
| Ndb_api_event_data_count_injectorInteger     |               | Global         |
| Ndb_api_event_nondata_count                  | Integer       | Global         |
| Ndb_api_event_nondata_count_injector Integer |               | Global         |
| Ndb_api_pk_op_count                          | Integer       | Global         |
| Ndb_api_pk_op_count_replica                  | Integer       | Global         |
| Ndb_api_pk_op_count_session                  | Integer       | Session        |
| Ndb_api_pk_op_count_slave                    | Integer       | Global         |
| Ndb_api_pruned_scan_count                    | Integer       | Global         |
| Ndb_api_pruned_scan_count_replica Integer    |               | Global         |
| Ndb_api_pruned_scan_count_session Integer    |               | Session        |
| Ndb_api_pruned_scan_count_slaveInteger       |               | Global         |
| Ndb_api_range_scan_count                     | Integer       | Global         |
| Ndb_api_range_scan_count_replicaInteger      |               | Global         |
| Ndb_api_range_scan_count_sessionInteger      |               | Session        |
| Ndb_api_range_scan_count_slaveInteger        |               | Global         |
| Ndb_api_read_row_count                       | Integer       | Global         |
| Ndb_api_read_row_count_replica Integer       |               | Global         |
| Ndb_api_read_row_count_sessionInteger        |               | Session        |
| Ndb_api_read_row_count_slave                 | Integer       | Global         |
| Ndb_api_scan_batch_count                     | Integer       | Global         |
| Ndb_api_scan_batch_count_replicaInteger      |               | Global         |
| Ndb_api_scan_batch_count_sessionInteger      |               | Session        |
| Ndb_api_scan_batch_count_slaveInteger        |               | Global         |
| Ndb_api_table_scan_count                     | Integer       | Global         |
| Ndb_api_table_scan_count_replicaInteger      |               | Global         |
| Ndb_api_table_scan_count_sessionIteger       |               | Session        |
| Ndb_api_table_scan_count_slave Integer       |               | Global         |
| Ndb_api_trans_abort_count                    | Integer       | Global         |
| Ndb_api_trans_abort_count_replicaInteger     |               | Global         |
| Ndb_api_trans_abort_count_sessionInteger     |               | Session        |
| Ndb_api_trans_abort_count_slaveInteger       |               | Global         |
| Ndb_api_trans_close_count                    | Integer       | Global         |
| Ndb_api_trans_close_count_replicaInteger     |               | Global         |
| Ndb_api_trans_close_count_sessionInteger     |               | Session        |
| Ndb_api_trans_close_count_slaveInteger       |               | Global         |
| Ndb_api_trans_commit_count                   | Integer       | Global         |
| Ndb_api_trans_commit_count_replica Integer   |               | Global         |
| Ndb_api_trans_commit_count_session Integer   |               | Session        |
| Ndb_api_trans_commit_count_slaveInteger      |               | Global         |
| Ndb_api_trans_local_read_row_count Integer   |               | Global         |
| Ndb_api_trans_local_read_row_count_replica   | Integer       | Global         |

| Variable Name                                   | Variable Type | Variable Scope |
|-------------------------------------------------|---------------|----------------|
| Ndb_api_trans_local_read_row_count_session      | Integer       | Session        |
| Ndb_api_trans_local_read_row_count_slave        | Integer       | Global         |
| Ndb_api_trans_start_count                       | Integer       | Global         |
| Ndb_api_trans_start_count_replicaInteger        |               | Global         |
| Ndb_api_trans_start_count_sessionInteger        |               | Session        |
| Ndb_api_trans_start_count_slave Integer         |               | Global         |
| Ndb_api_uk_op_count                             | Integer       | Global         |
| Ndb_api_uk_op_count_replica                     | Integer       | Global         |
| Ndb_api_uk_op_count_session                     | Integer       | Session        |
| Ndb_api_uk_op_count_slave                       | Integer       | Global         |
| Ndb_api_wait_exec_complete_count Ieger          |               | Global         |
| Ndb_api_wait_exec_complete_count_replica        | Integer       | Global         |
| Ndb_api_wait_exec_complete_count_session        | Integer       | Session        |
| Ndb_api_wait_exec_complete_count_slave Integer  |               | Global         |
| Ndb_api_wait_meta_request_countInteger          |               | Global         |
| Ndb_api_wait_meta_request_count_replica Integer |               | Global         |
| Ndb_api_wait_meta_request_count_session         | Integer       | Session        |
| Ndb_api_wait_meta_request_count_slave Integer   |               | Global         |
| Ndb_api_wait_nanos_count                        | Integer       | Global         |
| Ndb_api_wait_nanos_count_replicaInteger         |               | Global         |
| Ndb_api_wait_nanos_count_sessionInteger         |               | Session        |
| Ndb_api_wait_nanos_count_slaveInteger           |               | Global         |
| Ndb_api_wait_scan_result_count Integer          |               | Global         |
| Ndb_api_wait_scan_result_count_replica Integer  |               | Global         |
| Ndb_api_wait_scan_result_count_session Integer  |               | Session        |
| Ndb_api_wait_scan_result_count_slave Integer    |               | Global         |
| Ndb_cluster_node_id                             | Integer       | Global         |
| Ndb_config_from_host                            | Integer       | Both           |
| Ndb_config_from_port                            | Integer       | Both           |
| Ndb_config_generation                           | Integer       | Global         |
| Ndb_conflict_fn_epoch                           | Integer       | Global         |
| Ndb_conflict_fn_epoch_trans                     | Integer       | Global         |
| Ndb_conflict_fn_epoch2                          | Integer       | Global         |
| Ndb_conflict_fn_epoch2_trans                    | Integer       | Global         |
| Ndb_conflict_fn_max                             | Integer       | Global         |
| Ndb_conflict_fn_max_del_win                     | Integer       | Global         |
| Ndb_conflict_fn_max_del_win_ins Integer         |               | Global         |
| Ndb_conflict_fn_max_ins                         | Integer       | Global         |
| Ndb_conflict_fn_old                             | Integer       | Global         |
| Ndb_conflict_last_conflict_epoch                | Integer       | Global         |
| Ndb_conflict_last_stable_epoch                  | Integer       | Global         |

| Variable Name                                      | Variable Type | Variable Scope |
|----------------------------------------------------|---------------|----------------|
| Ndb_conflict_reflected_op_discard_count Integer    |               | Global         |
| Ndb_conflict_reflected_op_prepare_count Integer    |               | Global         |
| Ndb_conflict_refresh_op_count                      | Integer       | Global         |
| Ndb_conflict_trans_conflict_commit_count Integer   |               | Global         |
| Ndb_conflict_trans_detect_iter_count Integer       |               | Global         |
| Ndb_conflict_trans_reject_count                    | Integer       | Global         |
| Ndb_conflict_trans_row_conflict_count Integer      |               | Global         |
| Ndb_conflict_trans_row_reject_count Integer        |               | Global         |
| Ndb_epoch_delete_delete_count Integer              |               | Global         |
| Ndb_execute_count                                  | Integer       | Global         |
| Ndb_fetch_table_stats                              | Integer       | Global         |
| Ndb_last_commit_epoch_server                       | Integer       | Global         |
| Ndb_last_commit_epoch_session Integer              |               | Session        |
| Ndb_metadata_detected_count                        | Integer       | Global         |
| Ndb_metadata_excluded_count                        | Integer       | Global         |
| Ndb_metadata_synced_count                          | Integer       | Global         |
| Ndb_cluster_node_id                                | Integer       | Global         |
| Ndb_number_of_data_nodes                           | Integer       | Global         |
| Ndb_pruned_scan_count                              | Integer       | Global         |
| Ndb_pushed_queries_defined                         | Integer       | Global         |
| Ndb_pushed_queries_dropped                         | Integer       | Global         |
| Ndb_pushed_queries_executed                        | Integer       | Global         |
| Ndb_pushed_reads                                   | Integer       | Global         |
| Ndb_scan_count                                     | Integer       | Global         |
| Ndb_slave_max_replicated_epochInteger              |               | Global         |
| Ndb_trans_hint_count_session                       | Integer       | Both           |
| Not_flushed_delayed_rows                           | Integer       | Global         |
| Ongoing_anonymous_gtid_violating_transaction_count | Integer       | Global         |
| Ongoing_anonymous_transaction_count Integer        |               | Global         |
| Ongoing_automatic_gtid_violating_transaction_count | Integer       | Global         |
| Open_files                                         | Integer       | Global         |
| Open_streams                                       | Integer       | Global         |
| Open_table_definitions                             | Integer       | Global         |
| Open_tables                                        | Integer       | Both           |
| Opened_files                                       | Integer       | Global         |
| Opened_table_definitions                           | Integer       | Both           |
| Opened_tables                                      | Integer       | Both           |
| Performance_schema_accounts_lost Integer           |               | Global         |
| Performance_schema_cond_classes_lost Integer       |               | Global         |
| Performance_schema_cond_instances_lost Integer     |               | Global         |
| Performance_schema_digest_lostInteger              |               | Global         |

| Variable Name                                         | Variable Type | Variable Scope |
|-------------------------------------------------------|---------------|----------------|
| Performance_schema_file_classes_lost Integer          |               | Global         |
| Performance_schema_file_handles_lost Integer          |               | Global         |
| Performance_schema_file_instances_lost Integer        |               | Global         |
| Performance_schema_hosts_lost Integer                 |               | Global         |
| Performance_schema_index_stat_lost Integer            |               | Global         |
| Performance_schema_locker_lostInteger                 |               | Global         |
| Performance_schema_memory_classes_lost                | Integer       | Global         |
| Performance_schema_metadata_lock_lost Integer         |               | Global         |
| Performance_schema_mutex_classes_lost Integer         |               | Global         |
| Performance_schema_mutex_instances_lost               | Integer       | Global         |
| Performance_schema_nested_statement_lost              | Integer       | Global         |
| Performance_schema_prepared_statements_lost           | Integer       | Global         |
| Performance_schema_program_lost Integer               |               | Global         |
| Performance_schema_rwlock_classes_lost Integer        |               | Global         |
| Performance_schema_rwlock_instances_lost              | Integer       | Global         |
| Performance_schema_session_connect_attrs_longest_seen | Integer       | Global         |
| Performance_schema_session_connect_attrs_lost         | Integer       | Global         |
| Performance_schema_socket_classes_lost Integer        |               | Global         |
| Performance_schema_socket_instances_lost              | Integer       | Global         |
| Performance_schema_stage_classes_lost Integer         |               | Global         |
| Performance_schema_statement_classes_lost             | Integer       | Global         |
| Performance_schema_table_handles_lost Integer         |               | Global         |
| Performance_schema_table_instances_lost Integer       |               | Global         |
| Performance_schema_table_lock_stat_lost Integer       |               | Global         |
| Performance_schema_thread_classes_lost Integer        |               | Global         |
| Performance_schema_thread_instances_lost              | Integer       | Global         |
| Performance_schema_users_lost Integer                 |               | Global         |
| Prepared_stmt_count                                   | Integer       | Global         |
| Queries                                               | Integer       | Both           |
| Questions                                             | Integer       | Both           |
| Replica_open_temp_tables                              | Integer       | Global         |
| Replica_rows_last_search_algorithm_used String        |               | Global         |
| Resource_group_supported                              | Boolean       | Global         |
| Rewriter_number_loaded_rules                          | Integer       | Global         |
| Rewriter_number_reloads                               | Integer       | Global         |
| Rewriter_number_rewritten_queriesInteger              |               | Global         |
| Rewriter_reload_error                                 | Boolean       | Global         |
| Rpl_semi_sync_master_clients                          | Integer       | Global         |
| Rpl_semi_sync_master_net_avg_wait_time Integer        |               | Global         |
| Rpl_semi_sync_master_net_wait_time Integer            |               | Global         |
| Rpl_semi_sync_master_net_waitsInteger                 |               | Global         |

| Variable Name                                  | Variable Type | Variable Scope |
|------------------------------------------------|---------------|----------------|
| Rpl_semi_sync_master_no_times Integer          |               | Global         |
| Rpl_semi_sync_master_no_tx                     | Integer       | Global         |
| Rpl_semi_sync_master_status                    | Boolean       | Global         |
| Rpl_semi_sync_master_timefunc_failures Integer |               | Global         |
| Rpl_semi_sync_master_tx_avg_wait_time Integer  |               | Global         |
| Rpl_semi_sync_master_tx_wait_timeInteger       |               | Global         |
| Rpl_semi_sync_master_tx_waits                  | Integer       | Global         |
| Rpl_semi_sync_master_wait_pos_backtraverse     | Integer       | Global         |
| Rpl_semi_sync_master_wait_sessions Integer     |               | Global         |
| Rpl_semi_sync_master_yes_tx                    | Integer       | Global         |
| Rpl_semi_sync_replica_status                   | Boolean       | Global         |
| Rpl_semi_sync_slave_status                     | Boolean       | Global         |
| Rpl_semi_sync_source_clients                   | Integer       | Global         |
| Rpl_semi_sync_source_net_avg_wait_time Integer |               | Global         |
| Rpl_semi_sync_source_net_wait_time Integer     |               | Global         |
| Rpl_semi_sync_source_net_waits Integer         |               | Global         |
| Rpl_semi_sync_source_no_times Integer          |               | Global         |
| Rpl_semi_sync_source_no_tx                     | Integer       | Global         |
| Rpl_semi_sync_source_status                    | Boolean       | Global         |
| Rpl_semi_sync_source_timefunc_failures Integer |               | Global         |
| Rpl_semi_sync_source_tx_avg_wait_time Integer  |               | Global         |
| Rpl_semi_sync_source_tx_wait_timeInteger       |               | Global         |
| Rpl_semi_sync_source_tx_waits                  | Integer       | Global         |
| Rpl_semi_sync_source_wait_pos_backtraverse     | Integer       | Global         |
| Rpl_semi_sync_source_wait_sessions Integer     |               | Global         |
| Rpl_semi_sync_source_yes_tx                    | Integer       | Global         |
| Rsa_public_key                                 | String        | Global         |
| Secondary_engine_execution_count Integer       |               | Both           |
| Select_full_join                               | Integer       | Both           |
| Select_full_range_join                         | Integer       | Both           |
| Select_range                                   | Integer       | Both           |
| Select_range_check                             | Integer       | Both           |
| Select_scan                                    | Integer       | Both           |
| Slave_open_temp_tables                         | Integer       | Global         |
| Slave_rows_last_search_algorithm_used String   |               | Global         |
| Slow_launch_threads                            | Integer       | Both           |
| Slow_queries                                   | Integer       | Both           |
| Sort_merge_passes                              | Integer       | Both           |
| Sort_range                                     | Integer       | Both           |
| Sort_rows                                      | Integer       | Both           |
| Sort_scan                                      | Integer       | Both           |

| Variable Name                          | Variable Type | Variable Scope |
|----------------------------------------|---------------|----------------|
| Ssl_accept_renegotiates                | Integer       | Global         |
| Ssl_accepts                            | Integer       | Global         |
| Ssl_callback_cache_hits                | Integer       | Global         |
| Ssl_cipher                             | String        | Both           |
| Ssl_cipher_list                        | String        | Both           |
| Ssl_client_connects                    | Integer       | Global         |
| Ssl_connect_renegotiates               | Integer       | Global         |
| Ssl_ctx_verify_depth                   | Integer       | Global         |
| Ssl_ctx_verify_mode                    | Integer       | Global         |
| Ssl_default_timeout                    | Integer       | Both           |
| Ssl_finished_accepts                   | Integer       | Global         |
| Ssl_finished_connects                  | Integer       | Global         |
| Ssl_server_not_after                   | Integer       | Both           |
| Ssl_server_not_before                  | Integer       | Both           |
| Ssl_session_cache_hits                 | Integer       | Global         |
| Ssl_session_cache_misses               | Integer       | Global         |
| Ssl_session_cache_mode                 | String        | Global         |
| Ssl_session_cache_overflows            | Integer       | Global         |
| Ssl_session_cache_size                 | Integer       | Global         |
| Ssl_session_cache_timeout              | Integer       | Global         |
| Ssl_session_cache_timeouts             | Integer       | Global         |
| Ssl_sessions_reused                    | Integer       | Session        |
| Ssl_used_session_cache_entries Integer |               | Global         |
| Ssl_verify_depth                       | Integer       | Both           |
| Ssl_verify_mode                        | Integer       | Both           |
| Ssl_version                            | String        | Both           |
| Table_locks_immediate                  | Integer       | Global         |
| Table_locks_waited                     | Integer       | Global         |
| Table_open_cache_hits                  | Integer       | Both           |
| Table_open_cache_misses                | Integer       | Both           |
| Table_open_cache_overflows             | Integer       | Both           |
| Tc_log_max_pages_used                  | Integer       | Global         |
| Tc_log_page_size                       | Integer       | Global         |
| Tc_log_page_waits                      | Integer       | Global         |
| Telemetry_traces_supported             | Boolean       | Global         |
| Threads_cached                         | Integer       | Global         |
| Threads_connected                      | Integer       | Global         |
| Threads_created                        | Integer       | Global         |
| Threads_running                        | Integer       | Global         |
| Tls_library_version                    | String        | Global         |
| Uptime                                 | Integer       | Global         |

| Variable Name                                 | Variable Type | Variable Scope |
|-----------------------------------------------|---------------|----------------|
| Uptime_since_flush_status                     | Integer       | Global         |
| validate_password_dictionary_file_last_parsed | Datetime      | Global         |
| validate_password_dictionary_file_words_count | Integer       | Global         |
| validate_password.dictionary_file_last_parsed | Datetime      | Global         |
| validate_password.dictionary_file_words_count | Integer       | Global         |