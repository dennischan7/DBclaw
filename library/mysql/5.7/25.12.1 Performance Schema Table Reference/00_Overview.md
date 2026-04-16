---
source: MySQL 5.7 Reference
title: 00_Overview
---

The following table summarizes all available Performance Schema tables. For greater detail, see the individual table descriptions.

**Table 25.1 Performance Schema Tables**

| Table Name                                                      | Description                                                                                              | Deprecated |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|------------|
| accounts                                                        | Connection statistics per client<br>account                                                              |            |
| cond_instances                                                  | Synchronization object instances                                                                         |            |
| events_stages_current                                           | Current stage events                                                                                     |            |
| events_stages_history                                           | Most recent stage events per<br>thread                                                                   |            |
| events_stages_history_longMost recent stage events overall      |                                                                                                          |            |
| events_stages_summary_by_account_by_event_name                  | Stage events per account and<br>event name                                                               |            |
| events_stages_summary_by_host_by_event_name                     | Stage events per host name and<br>event name                                                             |            |
| events_stages_summary_by_thread_by_event_name                   | Stage waits per thread and event<br>name                                                                 |            |
| events_stages_summary_by_user_by_event_name                     | Stage events per user name and<br>event name                                                             |            |
| events_stages_summary_global_by_event_name                      | Stage waits per event name                                                                               |            |
| events_statements_current Current statement events              |                                                                                                          |            |
| events_statements_history Most recent statement events          | per thread                                                                                               |            |
| events_statements_history_long Most recent statement events     | overall                                                                                                  |            |
|                                                                 | Statement events per account<br>events_statements_summary_by_account_by_event_name<br>and event name     |            |
| events_statements_summary_by_digest                             | Statement events per schema<br>and digest value                                                          |            |
| events_statements_summary_by_host_by_event_name                 | Statement events per host name<br>and event name                                                         |            |
| events_statements_summary_by_program                            | Statement events per stored<br>program                                                                   |            |
| events_statements_summary_by_thread_by_event_name               | Statement events per thread and<br>event name                                                            |            |
| events_statements_summary_by_user_by_event_name                 | Statement events per user name<br>and event name                                                         |            |
| events_statements_summary_global_by_event_name                  | Statement events per event<br>name                                                                       |            |
| events_transactions_currentCurrent transaction events           |                                                                                                          |            |
| events_transactions_historyMost recent transaction events       | per thread                                                                                               |            |
| events_transactions_history_long Most recent transaction events | overall                                                                                                  |            |
|                                                                 | Transaction events per account<br>events_transactions_summary_by_account_by_event_name<br>and event name |            |

| Table Name                                                | Description                                                                                            | Deprecated |
|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------|------------|
| events_transactions_summary_by_host_by_event_name         | Transaction events per host<br>name and event name                                                     |            |
|                                                           | Transaction events per thread<br>events_transactions_summary_by_thread_by_event_name<br>and event name |            |
| events_transactions_summary_by_user_by_event_name         | Transaction events per user<br>name and event name                                                     |            |
| events_transactions_summary_global_by_event_name          | Transaction events per event<br>name                                                                   |            |
| events_waits_current                                      | Current wait events                                                                                    |            |
| events_waits_history                                      | Most recent wait events per<br>thread                                                                  |            |
| events_waits_history_long Most recent wait events overall |                                                                                                        |            |
| events_waits_summary_by_account_by_event_name             | Wait events per account and<br>event name                                                              |            |
| events_waits_summary_by_host_by_event_name                | Wait events per host name and<br>event name                                                            |            |
| events_waits_summary_by_instance Wait events per instance |                                                                                                        |            |
| events_waits_summary_by_thread_by_event_name              | Wait events per thread and event<br>name                                                               |            |
| events_waits_summary_by_user_by_event_name                | Wait events per user name and<br>event name                                                            |            |
| events_waits_summary_global_by_event_name                 | Wait events per event name                                                                             |            |
| file_instances                                            | File instances                                                                                         |            |
| file_summary_by_event_nameFile events per event name      |                                                                                                        |            |
| file_summary_by_instance                                  | File events per file instance                                                                          |            |
| global_status                                             | Global status variables                                                                                |            |
| global_variables                                          | Global system variables                                                                                |            |
| host_cache                                                | Information from internal host<br>cache                                                                |            |
| hosts                                                     | Connection statistics per client<br>host name                                                          |            |
| memory_summary_by_account_by_event_name                   | Memory operations per account<br>and event name                                                        |            |
| memory_summary_by_host_by_event_name                      | Memory operations per host and<br>event name                                                           |            |
| memory_summary_by_thread_by_event_name                    | Memory operations per thread<br>and event name                                                         |            |
| memory_summary_by_user_by_event_name                      | Memory operations per user and<br>event name                                                           |            |
| memory_summary_global_by_event_name                       | Memory operations globally per<br>event name                                                           |            |
| metadata_locks                                            | Metadata locks and lock<br>requests                                                                    |            |
| mutex_instances                                           | Mutex synchronization object<br>instances                                                              |            |
| objects_summary_global_by_type Object summaries           |                                                                                                        |            |

| Table Name                                                    | Description                                                          | Deprecated |
|---------------------------------------------------------------|----------------------------------------------------------------------|------------|
| performance_timers                                            | Which event timers are available                                     |            |
| prepared_statements_instances Prepared statement instances    | and statistics                                                       |            |
| replication_applier_configuration                             | Configuration parameters for<br>replication applier on replica       |            |
| replication_applier_statusCurrent status of replication       | applier on replica                                                   |            |
| replication_applier_status_by_coordinator                     | SQL or coordinator thread<br>applier status                          |            |
| replication_applier_status_by_worker                          | Worker thread applier status                                         |            |
| replication_connection_configuration                          | Configuration parameters for<br>connecting to source                 |            |
| replication_connection_status Current status of connection to | source                                                               |            |
| replication_group_member_stats Replication group member       | statistics                                                           |            |
| replication_group_members Replication group member            | network and status                                                   |            |
| rwlock_instances                                              | Lock synchronization object<br>instances                             |            |
| session_account_connect_attrs Connection attributes per for   | current session                                                      |            |
| session_connect_attrs                                         | Connection attributes for all<br>sessions                            |            |
| session_status                                                | Status variables for current<br>session                              |            |
| session_variables                                             | System variables for current<br>session                              |            |
| setup_actors                                                  | How to initialize monitoring for<br>new foreground threads           |            |
| setup_consumers                                               | Consumers for which event<br>information can be stored               |            |
| setup_instruments                                             | Classes of instrumented objects<br>for which events can be collected |            |
| setup_objects                                                 | Which objects should be<br>monitored                                 |            |
| setup_timers                                                  | Currently selected event timers                                      | Yes        |
| socket_instances                                              | Active connection instances                                          |            |
| socket_summary_by_event_name Socket waits and I/O per event   | name                                                                 |            |
| socket_summary_by_instanceSocket waits and I/O per            | instance                                                             |            |
| status_by_account                                             | Session status variables per<br>account                              |            |
| status_by_host                                                | Session status variables per host<br>name                            |            |

| Table Name                                                | Description                                   | Deprecated |
|-----------------------------------------------------------|-----------------------------------------------|------------|
| status_by_thread                                          | Session status variables per<br>session       |            |
| status_by_user                                            | Session status variables per user<br>name     |            |
| table_handles                                             | Table locks and lock requests                 |            |
| table_io_waits_summary_by_index_usage                     | Table I/O waits per index                     |            |
| table_io_waits_summary_by_table Table I/O waits per table |                                               |            |
| table_lock_waits_summary_by_table                         | Table lock waits per table                    |            |
| threads                                                   | Information about server threads              |            |
| user_variables_by_thread                                  | User-defined variables per<br>thread          |            |
| users                                                     | Connection statistics per client<br>user name |            |
| variables_by_thread                                       | Session system variables per<br>session       |            |