---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following table summarizes all available Performance Schema tables. For greater detail, see the individual table descriptions.

**Table 29.1 Performance Schema Tables**

| Table Name                                                                            | Description                                         |
|---------------------------------------------------------------------------------------|-----------------------------------------------------|
| accounts                                                                              | Connection statistics per client account            |
| binary_log_transaction_compression_statsBinary log transaction compression            |                                                     |
| clone_progress                                                                        | Clone operation progress                            |
| clone_status                                                                          | Clone operation status                              |
| component_scheduler_tasks                                                             | Status of scheduled tasks                           |
| cond_instances                                                                        | Synchronization object instances                    |
| data_lock_waits                                                                       | Data lock wait relationships                        |
| data_locks                                                                            | Data locks held and requested                       |
| error_log                                                                             | Server error log recent entries                     |
| events_errors_summary_by_account_by_error Errors per account and error code           |                                                     |
| events_errors_summary_by_host_by_errorErrors per host and error code                  |                                                     |
| events_errors_summary_by_thread_by_errorErrors per thread and error code              |                                                     |
| events_errors_summary_by_user_by_errorErrors per user and error code                  |                                                     |
| events_errors_summary_global_by_error                                                 | Errors per error code                               |
| events_stages_current                                                                 | Current stage events                                |
| events_stages_history                                                                 | Most recent stage events per thread                 |
| events_stages_history_long                                                            | Most recent stage events overall                    |
| events_stages_summary_by_account_by_event_name                                        | Stage events per account and event name             |
| events_stages_summary_by_host_by_event_name Stage events per host name and event name |                                                     |
| events_stages_summary_by_thread_by_event_name Stage waits per thread and event name   |                                                     |
| events_stages_summary_by_user_by_event_name Stage events per user name and event name |                                                     |
| events_stages_summary_global_by_event_name Stage waits per event name                 |                                                     |
| events_statements_current                                                             | Current statement events                            |
| events_statements_histogram_by_digest                                                 | Statement histograms per schema and digest<br>value |
| events_statements_histogram_global                                                    | Statement histogram summarized globally             |
| events_statements_history                                                             | Most recent statement events per thread             |
| events_statements_history_long                                                        | Most recent statement events overall                |
| events_statements_summary_by_account_by_event_name                                    | Statement events per account and event name         |
| events_statements_summary_by_digest                                                   | Statement events per schema and digest value        |
| events_statements_summary_by_host_by_event_name                                       | Statement events per host name and event name       |
| events_statements_summary_by_program                                                  | Statement events per stored program                 |
| events_statements_summary_by_thread_by_event_name                                     | Statement events per thread and event name          |
| events_statements_summary_by_user_by_event_name                                       | Statement events per user name and event name       |
| events_statements_summary_global_by_event_name                                        | Statement events per event name                     |
| events_transactions_current                                                           | Current transaction events                          |
| events_transactions_history                                                           | Most recent transaction events per thread           |
| events_transactions_history_long                                                      | Most recent transaction events overall              |
| events_transactions_summary_by_account_by_event_name                                  | Transaction events per account and event name       |

| Table Name                                                                           | Description                                          |
|--------------------------------------------------------------------------------------|------------------------------------------------------|
| events_transactions_summary_by_host_by_event_name                                    | Transaction events per host name and event<br>name   |
| events_transactions_summary_by_thread_by_event_name                                  | Transaction events per thread and event name         |
| events_transactions_summary_by_user_by_event_name                                    | Transaction events per user name and event<br>name   |
| events_transactions_summary_global_by_event_name                                     | Transaction events per event name                    |
| events_waits_current                                                                 | Current wait events                                  |
| events_waits_history                                                                 | Most recent wait events per thread                   |
| events_waits_history_long                                                            | Most recent wait events overall                      |
| events_waits_summary_by_account_by_event_name Wait events per account and event name |                                                      |
| events_waits_summary_by_host_by_event_name Wait events per host name and event name  |                                                      |
| events_waits_summary_by_instance                                                     | Wait events per instance                             |
| events_waits_summary_by_thread_by_event_name Wait events per thread and event name   |                                                      |
| events_waits_summary_by_user_by_event_name Wait events per user name and event name  |                                                      |
| events_waits_summary_global_by_event_name Wait events per event name                 |                                                      |
| file_instances                                                                       | File instances                                       |
| file_summary_by_event_name                                                           | File events per event name                           |
| file_summary_by_instance                                                             | File events per file instance                        |
| firewall_group_allowlist                                                             | Firewall in-memory data for group profile allowlists |
| firewall_groups                                                                      | Firewall in-memory data for group profiles           |
| firewall_membership                                                                  | Firewall in-memory data for group profile members    |
| global_status                                                                        | Global status variables                              |
| global_variables                                                                     | Global system variables                              |
| host_cache                                                                           | Information from internal host cache                 |
| hosts                                                                                | Connection statistics per client host name           |
| keyring_component_status                                                             | Status information for installed keyring component   |
| keyring_keys                                                                         | Metadata for keyring keys                            |
| log_status                                                                           | Information about server logs for backup purposes    |
| memory_summary_by_account_by_event_nameMemory operations per account and event name  |                                                      |
| memory_summary_by_host_by_event_name                                                 | Memory operations per host and event name            |
| memory_summary_by_thread_by_event_nameMemory operations per thread and event name    |                                                      |
| memory_summary_by_user_by_event_name                                                 | Memory operations per user and event name            |
| memory_summary_global_by_event_name                                                  | Memory operations globally per event name            |
| metadata_locks                                                                       | Metadata locks and lock requests                     |
| mutex_instances                                                                      | Mutex synchronization object instances               |
| ndb_sync_excluded_objects                                                            | NDB objects which cannot be synchronized             |
| ndb_sync_pending_objects                                                             | NDB objects waiting for synchronization              |
| objects_summary_global_by_type                                                       | Object summaries                                     |
| performance_timers                                                                   | Which event timers are available                     |
| persisted_variables                                                                  | Contents of mysqld-auto.cnf file                     |
| prepared_statements_instances                                                        | Prepared statement instances and statistics          |

| Table Name                                                                                     | Description                                                                                              |
|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| processlist                                                                                    | Process list information                                                                                 |
| replication_applier_configuration                                                              | Configuration parameters for replication applier on<br>replica                                           |
| replication_applier_filters                                                                    | Channel-specific replication filters on current<br>replica                                               |
| replication_applier_global_filters                                                             | Global replication filters on current replica                                                            |
| replication_applier_status                                                                     | Current status of replication applier on replica                                                         |
| replication_applier_status_by_coordinator SQL or coordinator thread applier status             |                                                                                                          |
| replication_applier_status_by_worker                                                           | Worker thread applier status                                                                             |
| replication_asynchronous_connection_failover Source lists for asynchronous connection failover | mechanism                                                                                                |
| replication_asynchronous_connection_failover_managed                                           | Managed source lists for asynchronous<br>connection failover mechanism                                   |
| replication_connection_configuration                                                           | Configuration parameters for connecting to source                                                        |
| replication_connection_status                                                                  | Current status of connection to source                                                                   |
| replication_group_communication_information Replication group configuration options            |                                                                                                          |
| replication_group_configuration_versionVersion of the member actions configuration for         | replication group members                                                                                |
| replication_group_member_actions                                                               | Member actions that are included in the member<br>actions configuration for replication group<br>members |
| replication_group_member_stats                                                                 | Replication group member statistics                                                                      |
| replication_group_members                                                                      | Replication group member network and status                                                              |
| rwlock_instances                                                                               | Lock synchronization object instances                                                                    |
| session_account_connect_attrs                                                                  | Connection attributes per for current session                                                            |
| session_connect_attrs                                                                          | Connection attributes for all sessions                                                                   |
| session_status                                                                                 | Status variables for current session                                                                     |
| session_variables                                                                              | System variables for current session                                                                     |
| setup_actors                                                                                   | How to initialize monitoring for new foreground<br>threads                                               |
| setup_consumers                                                                                | Consumers for which event information can be<br>stored                                                   |
| setup_instruments                                                                              | Classes of instrumented objects for which events<br>can be collected                                     |
| setup_objects                                                                                  | Which objects should be monitored                                                                        |
| setup_threads                                                                                  | Instrumented thread names and attributes                                                                 |
| socket_instances                                                                               | Active connection instances                                                                              |
| socket_summary_by_event_name                                                                   | Socket waits and I/O per event name                                                                      |
| socket_summary_by_instance                                                                     | Socket waits and I/O per instance                                                                        |
| status_by_account                                                                              | Session status variables per account                                                                     |
| status_by_host                                                                                 | Session status variables per host name                                                                   |
| status_by_thread                                                                               | Session status variables per session                                                                     |
| status_by_user                                                                                 | Session status variables per user name                                                                   |
| table_handles                                                                                  | Table locks and lock requests                                                                            |

| Table Name                            | Description                                 |
|---------------------------------------|---------------------------------------------|
| table_io_waits_summary_by_index_usage | Table I/O waits per index                   |
| table_io_waits_summary_by_table       | Table I/O waits per table                   |
| table_lock_waits_summary_by_table     | Table lock waits per table                  |
| threads                               | Information about server threads            |
| tls_channel_status                    | TLS status for each connection interface    |
| tp_thread_group_state                 | Thread pool thread group states             |
| tp_thread_group_stats                 | Thread pool thread group statistics         |
| tp_thread_state                       | Thread pool thread information              |
| user_defined_functions                | Registered loadable functions               |
| user_variables_by_thread              | User-defined variables per thread           |
| users                                 | Connection statistics per client user name  |
| variables_by_thread                   | Session system variables per session        |
| variables_info                        | How system variables were most recently set |