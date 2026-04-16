---
source: MySQL 8.0 Reference
title: 00_Overview
---

A number of types of statistical counters relating to actions performed by or affecting [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects are available. Such actions include starting and closing (or aborting) transactions; primary key and unique key operations; table, range, and pruned scans; threads blocked while waiting for the completion of various operations; and data and events sent and received by NDBCLUSTER. The counters are incremented inside the NDB kernel whenever NDB API calls are made or data is sent to or received

by the data nodes. mysqld exposes these counters as system status variables; their values can be read in the output of SHOW STATUS, or by querying the Performance Schema session\_status or global\_status table. By comparing the values before and after statements operating on NDB tables, you can observe the corresponding actions taken on the API level, and thus the cost of performing the statement.

You can list all of these status variables using the following SHOW STATUS statement:

| Variable_name<br>  Value<br> <br>+++<br>  Ndb_api_wait_exec_complete_count<br>  297<br> <br>  Ndb_api_wait_scan_result_count<br>  0<br>  Ndb_api_wait_meta_request_count<br>  321<br>  Ndb_api_wait_nanos_count<br>  Ndb_api_bytes_sent_count<br>  33988<br>  Ndb_api_bytes_received_count<br>  66236<br>  Ndb_api_trans_start_count<br>  148<br>  Ndb_api_trans_commit_count<br>  148<br>  Ndb_api_trans_abort_count<br>  0<br>  Ndb_api_trans_close_count<br>  148<br>  Ndb_api_pk_op_count<br>  151<br>  Ndb_api_uk_op_count<br>  0<br>  Ndb_api_table_scan_count<br>  0<br>  Ndb_api_range_scan_count<br>  0<br>  Ndb_api_pruned_scan_count<br>  0<br>  Ndb_api_scan_batch_count<br>  0<br>  Ndb_api_read_row_count<br>  147<br>  Ndb_api_trans_local_read_row_count<br>  37<br>  Ndb_api_adaptive_send_forced_count<br>  3<br>  Ndb_api_adaptive_send_unforced_count<br>  294<br>  Ndb_api_adaptive_send_deferred_count<br>  0<br>  Ndb_api_event_data_count<br>  0<br>  Ndb_api_event_nondata_count<br>  0<br>  Ndb_api_event_bytes_count<br>  0<br>  Ndb_api_wait_exec_complete_count_slave<br>  0<br>  Ndb_api_wait_scan_result_count_slave<br>  0<br>  Ndb_api_wait_meta_request_count_slave<br>  0<br>  Ndb_api_wait_nanos_count_slave<br>  0<br>  Ndb_api_bytes_sent_count_slave<br>  0<br>  Ndb_api_bytes_received_count_slave<br>  0<br>  Ndb_api_trans_start_count_slave<br>  0<br>  Ndb_api_trans_commit_count_slave<br>  0<br>  Ndb_api_trans_abort_count_slave<br>  0<br>  Ndb_api_trans_close_count_slave<br>  0<br>  Ndb_api_pk_op_count_slave<br>  0<br>  Ndb_api_uk_op_count_slave<br>  0<br>  Ndb_api_table_scan_count_slave<br>  0<br>  Ndb_api_range_scan_count_slave<br>  0<br>  Ndb_api_pruned_scan_count_slave<br>  0 |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <br>  228438645  <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br> <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Ndb_api_scan_batch_count_slave<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Ndb_api_read_row_count_slave<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Ndb_api_trans_local_read_row_count_slave<br>  0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <br>  Ndb_api_adaptive_send_forced_count_slave<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Ndb_api_adaptive_send_unforced_count_slave<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Ndb_api_adaptive_send_deferred_count_slave<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Ndb_api_wait_exec_complete_count_replica<br>  0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <br>  Ndb_api_wait_scan_result_count_replica<br>  0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| <br>  Ndb_api_wait_meta_request_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Ndb_api_wait_nanos_count_replica<br>  0<br> <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Ndb_api_bytes_sent_count_replica<br>  0<br>  Ndb_api_bytes_received_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Ndb_api_trans_start_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Ndb_api_trans_commit_count_replica<br>  0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| <br>  Ndb_api_trans_abort_count_replica<br>  0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| <br>  Ndb_api_trans_close_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Ndb_api_pk_op_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Ndb_api_uk_op_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Ndb_api_table_scan_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Ndb_api_range_scan_count_replica<br>  0<br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

```
| Ndb_api_pruned_scan_count_replica | 0 |
| Ndb_api_scan_batch_count_replica | 0 |
| Ndb_api_read_row_count_replica | 0 |
| Ndb_api_trans_local_read_row_count_replica | 0 |
| Ndb_api_adaptive_send_forced_count_replica | 0 |
| Ndb_api_adaptive_send_unforced_count_replica | 0 |
| Ndb_api_adaptive_send_deferred_count_replica | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+-----------+
90 rows in set (0.01 sec)
```

These status variables are also available from the Performance Schema session\_status and global\_status tables, as shown here:

```
mysql> SELECT * FROM performance_schema.session_status
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%';
+----------------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+----------------------------------------------+----------------+
| Ndb_api_wait_exec_complete_count | 617 |
| Ndb_api_wait_scan_result_count | 0 |
| Ndb_api_wait_meta_request_count | 649 |
| Ndb_api_wait_nanos_count | 335663491 |
| Ndb_api_bytes_sent_count | 65764 |
| Ndb_api_bytes_received_count | 86940 |
| Ndb_api_trans_start_count | 308 |
| Ndb_api_trans_commit_count | 308 |
| Ndb_api_trans_abort_count | 0 |
| Ndb_api_trans_close_count | 308 |
| Ndb_api_pk_op_count | 311 |
| Ndb_api_uk_op_count | 0 |
| Ndb_api_table_scan_count | 0 |
| Ndb_api_range_scan_count | 0 |
| Ndb_api_pruned_scan_count | 0 |
| Ndb_api_scan_batch_count | 0 |
| Ndb_api_read_row_count | 307 |
| Ndb_api_trans_local_read_row_count | 77 |
| Ndb_api_adaptive_send_forced_count | 3 |
| Ndb_api_adaptive_send_unforced_count | 614 |
| Ndb_api_adaptive_send_deferred_count | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
| Ndb_api_wait_exec_complete_count_slave | 0 |
| Ndb_api_wait_scan_result_count_slave | 0 |
| Ndb_api_wait_meta_request_count_slave | 0 |
| Ndb_api_wait_nanos_count_slave | 0 |
| Ndb_api_bytes_sent_count_slave | 0 |
| Ndb_api_bytes_received_count_slave | 0 |
```

```
| Ndb_api_trans_start_count_slave | 0 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_abort_count_slave | 0 |
| Ndb_api_trans_close_count_slave | 0 |
| Ndb_api_pk_op_count_slave | 0 |
| Ndb_api_uk_op_count_slave | 0 |
| Ndb_api_table_scan_count_slave | 0 |
| Ndb_api_range_scan_count_slave | 0 |
| Ndb_api_pruned_scan_count_slave | 0 |
| Ndb_api_scan_batch_count_slave | 0 |
| Ndb_api_read_row_count_slave | 0 |
| Ndb_api_trans_local_read_row_count_slave | 0 |
| Ndb_api_adaptive_send_forced_count_slave | 0 |
| Ndb_api_adaptive_send_unforced_count_slave | 0 |
| Ndb_api_adaptive_send_deferred_count_slave | 0 |
| Ndb_api_wait_exec_complete_count_replica | 0 |
| Ndb_api_wait_scan_result_count_replica | 0 |
| Ndb_api_wait_meta_request_count_replica | 0 |
| Ndb_api_wait_nanos_count_replica | 0 |
| Ndb_api_bytes_sent_count_replica | 0 |
| Ndb_api_bytes_received_count_replica | 0 |
| Ndb_api_trans_start_count_replica | 0 |
| Ndb_api_trans_commit_count_replica | 0 |
| Ndb_api_trans_abort_count_replica | 0 |
| Ndb_api_trans_close_count_replica | 0 |
| Ndb_api_pk_op_count_replica | 0 |
| Ndb_api_uk_op_count_replica | 0 |
| Ndb_api_table_scan_count_replica | 0 |
| Ndb_api_range_scan_count_replica | 0 |
| Ndb_api_pruned_scan_count_replica | 0 |
| Ndb_api_scan_batch_count_replica | 0 |
| Ndb_api_read_row_count_replica | 0 |
| Ndb_api_trans_local_read_row_count_replica | 0 |
| Ndb_api_adaptive_send_forced_count_replica | 0 |
| Ndb_api_adaptive_send_unforced_count_replica | 0 |
| Ndb_api_adaptive_send_deferred_count_replica | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+----------------+
90 rows in set (0.01 sec)
mysql> SELECT * FROM performance_schema.global_status
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%';
+----------------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+----------------------------------------------+----------------+
| Ndb_api_wait_exec_complete_count | 741 |
| Ndb_api_wait_scan_result_count | 0 |
| Ndb_api_wait_meta_request_count | 777 |
| Ndb_api_wait_nanos_count | 373888309 |
```

```
| Ndb_api_bytes_sent_count | 78124 |
| Ndb_api_bytes_received_count | 94988 |
| Ndb_api_trans_start_count | 370 |
| Ndb_api_trans_commit_count | 370 |
| Ndb_api_trans_abort_count | 0 |
| Ndb_api_trans_close_count | 370 |
| Ndb_api_pk_op_count | 373 |
| Ndb_api_uk_op_count | 0 |
| Ndb_api_table_scan_count | 0 |
| Ndb_api_range_scan_count | 0 |
| Ndb_api_pruned_scan_count | 0 |
| Ndb_api_scan_batch_count | 0 |
| Ndb_api_read_row_count | 369 |
| Ndb_api_trans_local_read_row_count | 93 |
| Ndb_api_adaptive_send_forced_count | 3 |
| Ndb_api_adaptive_send_unforced_count | 738 |
| Ndb_api_adaptive_send_deferred_count | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
| Ndb_api_wait_exec_complete_count_slave | 0 |
| Ndb_api_wait_scan_result_count_slave | 0 |
| Ndb_api_wait_meta_request_count_slave | 0 |
| Ndb_api_wait_nanos_count_slave | 0 |
| Ndb_api_bytes_sent_count_slave | 0 |
| Ndb_api_bytes_received_count_slave | 0 |
| Ndb_api_trans_start_count_slave | 0 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_abort_count_slave | 0 |
| Ndb_api_trans_close_count_slave | 0 |
| Ndb_api_pk_op_count_slave | 0 |
| Ndb_api_uk_op_count_slave | 0 |
| Ndb_api_table_scan_count_slave | 0 |
| Ndb_api_range_scan_count_slave | 0 |
| Ndb_api_pruned_scan_count_slave | 0 |
| Ndb_api_scan_batch_count_slave | 0 |
| Ndb_api_read_row_count_slave | 0 |
| Ndb_api_trans_local_read_row_count_slave | 0 |
| Ndb_api_adaptive_send_forced_count_slave | 0 |
| Ndb_api_adaptive_send_unforced_count_slave | 0 |
| Ndb_api_adaptive_send_deferred_count_slave | 0 |
| Ndb_api_wait_exec_complete_count_replica | 0 |
| Ndb_api_wait_scan_result_count_replica | 0 |
| Ndb_api_wait_meta_request_count_replica | 0 |
| Ndb_api_wait_nanos_count_replica | 0 |
| Ndb_api_bytes_sent_count_replica | 0 |
| Ndb_api_bytes_received_count_replica | 0 |
| Ndb_api_trans_start_count_replica | 0 |
| Ndb_api_trans_commit_count_replica | 0 |
| Ndb_api_trans_abort_count_replica | 0 |
| Ndb_api_trans_close_count_replica | 0 |
| Ndb_api_pk_op_count_replica | 0 |
| Ndb_api_uk_op_count_replica | 0 |
| Ndb_api_table_scan_count_replica | 0 |
| Ndb_api_range_scan_count_replica | 0 |
| Ndb_api_pruned_scan_count_replica | 0 |
| Ndb_api_scan_batch_count_replica | 0 |
| Ndb_api_read_row_count_replica | 0 |
| Ndb_api_trans_local_read_row_count_replica | 0 |
| Ndb_api_adaptive_send_forced_count_replica | 0 |
| Ndb_api_adaptive_send_unforced_count_replica | 0 |
| Ndb_api_adaptive_send_deferred_count_replica | 0 |
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_wait_exec_complete_count_session | 0 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 0 |
| Ndb_api_wait_nanos_count_session | 0 |
| Ndb_api_bytes_sent_count_session | 0 |
| Ndb_api_bytes_received_count_session | 0 |
| Ndb_api_trans_start_count_session | 0 |
```

```
| Ndb_api_trans_commit_count_session | 0 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 0 |
| Ndb_api_pk_op_count_session | 0 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 0 |
| Ndb_api_trans_local_read_row_count_session | 0 |
| Ndb_api_adaptive_send_forced_count_session | 0 |
| Ndb_api_adaptive_send_unforced_count_session | 0 |
| Ndb_api_adaptive_send_deferred_count_session | 0 |
+----------------------------------------------+----------------+
90 rows in set (0.01 sec)
```

Each [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object has its own counters. NDB API applications can read the values of the counters for use in optimization or monitoring. For multithreaded clients which use more than one [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object concurrently, it is also possible to obtain a summed view of counters from all [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects belonging to a given [Ndb\\_cluster\\_connection](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md).

Four sets of these counters are exposed. One set applies to the current session only; the other 3 are global. This is in spite of the fact that their values can be obtained as either session or global status variables in the mysql client. This means that specifying the SESSION or GLOBAL keyword with SHOW STATUS has no effect on the values reported for NDB API statistics status variables, and the value for each of these variables is the same whether the value is obtained from the equivalent column of the session\_status or the global\_status table.

• Session counters (session specific)

Session counters relate to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects in use by (only) the current session. Use of such objects by other MySQL clients does not influence these counts.

In order to minimize confusion with standard MySQL session variables, we refer to the variables that correspond to these NDB API session counters as "\_session variables", with a leading underscore.

• Replica counters (global)

This set of counters relates to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects used by the replica SQL thread, if any. If this mysqld does not act as a replica, or does not use NDB tables, then all of these counts are 0.

We refer to the related status variables as "\_slave variables" (with a leading underscore).

• Injector counters (global)

Injector counters relate to the [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) object used to listen to cluster events by the binary log injector thread. Even when not writing a binary log, mysqld processes attached to an NDB Cluster continue to listen for some events, such as schema changes.

We refer to the status variables that correspond to NDB API injector counters as "\_injector variables" (with a leading underscore).

• Server (Global) counters (global)

This set of counters relates to all [Ndb](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb.md) objects currently used by this mysqld. This includes all MySQL client applications, the replica SQL thread (if any), the binary log injector, and the NDB utility thread.

We refer to the status variables that correspond to these counters as "global variables" or "mysqldlevel variables".

You can obtain values for a particular set of variables by additionally filtering for the substring session, slave, or injector in the variable name (along with the common prefix Ndb\_api). For \_session variables, this can be done as shown here:

```
mysql> SHOW STATUS LIKE 'ndb_api%session';
+--------------------------------------------+---------+
| Variable_name | Value |
+--------------------------------------------+---------+
| Ndb_api_wait_exec_complete_count_session | 2 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 1 |
| Ndb_api_wait_nanos_count_session | 8144375 |
| Ndb_api_bytes_sent_count_session | 68 |
| Ndb_api_bytes_received_count_session | 84 |
| Ndb_api_trans_start_count_session | 1 |
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 1 |
| Ndb_api_pk_op_count_session | 1 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 1 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+---------+
18 rows in set (0.50 sec)
```

To obtain a listing of the NDB API mysqld-level status variables, filter for variable names beginning with ndb\_api and ending in \_count, like this:

```
mysql> SELECT * FROM performance_schema.session_status
 -> WHERE VARIABLE_NAME LIKE 'ndb_api%count';
+------------------------------------+----------------+
| VARIABLE_NAME | VARIABLE_VALUE |
+------------------------------------+----------------+
| NDB_API_WAIT_EXEC_COMPLETE_COUNT | 4 |
| NDB_API_WAIT_SCAN_RESULT_COUNT | 3 |
| NDB_API_WAIT_META_REQUEST_COUNT | 28 |
| NDB_API_WAIT_NANOS_COUNT | 53756398 |
| NDB_API_BYTES_SENT_COUNT | 1060 |
| NDB_API_BYTES_RECEIVED_COUNT | 9724 |
| NDB_API_TRANS_START_COUNT | 3 |
| NDB_API_TRANS_COMMIT_COUNT | 2 |
| NDB_API_TRANS_ABORT_COUNT | 0 |
| NDB_API_TRANS_CLOSE_COUNT | 3 |
| NDB_API_PK_OP_COUNT | 2 |
| NDB_API_UK_OP_COUNT | 0 |
| NDB_API_TABLE_SCAN_COUNT | 1 |
| NDB_API_RANGE_SCAN_COUNT | 0 |
| NDB_API_PRUNED_SCAN_COUNT | 0 |
| NDB_API_SCAN_BATCH_COUNT | 0 |
| NDB_API_READ_ROW_COUNT | 2 |
| NDB_API_TRANS_LOCAL_READ_ROW_COUNT | 2 |
| NDB_API_EVENT_DATA_COUNT | 0 |
| NDB_API_EVENT_NONDATA_COUNT | 0 |
| NDB_API_EVENT_BYTES_COUNT | 0 |
+------------------------------------+----------------+
21 rows in set (0.09 sec)
```

Not all counters are reflected in all 4 sets of status variables. For the event counters DataEventsRecvdCount, NondataEventsRecvdCount, and EventBytesRecvdCount, only \_injector and mysqld-level NDB API status variables are available:

```
mysql> SHOW STATUS LIKE 'ndb_api%event%';
+--------------------------------------+-------+
| Variable_name | Value |
+--------------------------------------+-------+
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
```

```
| Ndb_api_event_bytes_count_injector | 0 |
| Ndb_api_event_data_count | 0 |
| Ndb_api_event_nondata_count | 0 |
| Ndb_api_event_bytes_count | 0 |
+--------------------------------------+-------+
6 rows in set (0.00 sec)
```

\_injector status variables are not implemented for any other NDB API counters, as shown here:

```
mysql> SHOW STATUS LIKE 'ndb_api%injector%';
+--------------------------------------+-------+
| Variable_name | Value |
+--------------------------------------+-------+
| Ndb_api_event_data_count_injector | 0 |
| Ndb_api_event_nondata_count_injector | 0 |
| Ndb_api_event_bytes_count_injector | 0 |
+--------------------------------------+-------+
3 rows in set (0.00 sec)
```

The names of the status variables can easily be associated with the names of the corresponding counters. Each NDB API statistics counter is listed in the following table with a description as well as the names of any MySQL server status variables corresponding to this counter.

**Table 25.67 NDB API statistics counters**

| Counter Name          | Description                                                                               | Status Variables (by statistic<br>type):      |
|-----------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------|
|                       |                                                                                           | •<br>Session                                  |
|                       |                                                                                           | •<br>Slave (replica)                          |
|                       |                                                                                           | •<br>Injector                                 |
|                       |                                                                                           | •<br>Server                                   |
| WaitExecCompleteCount | Number of times thread has<br>been blocked while waiting                                  | •<br>Ndb_api_wait_exec_complete_count_session |
|                       | for execution of an operation                                                             | •<br>Ndb_api_wait_exec_complete_count_slave   |
|                       | to complete. Includes all<br>execute() calls as well                                      | •<br>[none]                                   |
|                       | as implicit executes for blob<br>operations and auto-increment<br>not visible to clients. | •<br>Ndb_api_wait_exec_complete_count         |
| WaitScanResultCount   | Number of times thread has                                                                | •<br>Ndb_api_wait_scan_result_count_session   |
|                       | been blocked while waiting for a<br>scan-based signal, such waiting                       | •<br>Ndb_api_wait_scan_result_count_slave     |
|                       | for additional results, or for a<br>scan to close.                                        | •<br>[none]                                   |
|                       |                                                                                           | •<br>Ndb_api_wait_scan_result_count           |
| WaitMetaRequestCount  | Number of times thread has<br>been blocked waiting for a                                  | •<br>Ndb_api_wait_meta_request_count_session  |
|                       | metadata-based signal; this can                                                           | •<br>Ndb_api_wait_meta_request_count_slave    |
|                       | occur when waiting for a DDL<br>operation or for an epoch to be                           | •<br>[none]                                   |
|                       | started (or ended).                                                                       | •<br>Ndb_api_wait_meta_request_count          |
| WaitNanosCount        | Total time (in nanoseconds)                                                               | •<br>Ndb_api_wait_nanos_count_session         |
|                       | spent waiting for some type of<br>signal from the data nodes.                             | •<br>Ndb_api_wait_nanos_count_slave           |
|                       |                                                                                           | •<br>[none]                                   |

| •<br>Session<br>•<br>Slave (replica)<br>•<br>Injector<br>•<br>Server<br>•<br>Ndb_api_wait_nanos_count<br>Amount of data (in bytes) sent to<br>•<br>BytesSentCount<br>Ndb_api_bytes_sent_count_session |  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
|                                                                                                                                                                                                       |  |
|                                                                                                                                                                                                       |  |
|                                                                                                                                                                                                       |  |
|                                                                                                                                                                                                       |  |
|                                                                                                                                                                                                       |  |
|                                                                                                                                                                                                       |  |
| the data nodes<br>•<br>Ndb_api_bytes_sent_count_slave                                                                                                                                                 |  |
| •<br>[none]                                                                                                                                                                                           |  |
| •<br>Ndb_api_bytes_sent_count                                                                                                                                                                         |  |
| Amount of data (in bytes)<br>•<br>BytesRecvdCount<br>Ndb_api_bytes_received_count_session                                                                                                             |  |
| received from the data nodes<br>•<br>Ndb_api_bytes_received_count_slave                                                                                                                               |  |
| •<br>[none]                                                                                                                                                                                           |  |
| •<br>Ndb_api_bytes_received_count                                                                                                                                                                     |  |
| Number of transactions started.<br>•<br>TransStartCount<br>Ndb_api_trans_start_count_session                                                                                                          |  |
| •<br>Ndb_api_trans_start_count_slave                                                                                                                                                                  |  |
| •<br>[none]                                                                                                                                                                                           |  |
| •<br>Ndb_api_trans_start_count                                                                                                                                                                        |  |
| Number of transactions<br>•<br>TransCommitCount<br>Ndb_api_trans_commit_count_session                                                                                                                 |  |
| committed.<br>•<br>Ndb_api_trans_commit_count_slave                                                                                                                                                   |  |
| •<br>[none]                                                                                                                                                                                           |  |
| •<br>Ndb_api_trans_commit_count                                                                                                                                                                       |  |
| Number of transactions aborted.<br>•<br>TransAbortCount<br>Ndb_api_trans_abort_count_session                                                                                                          |  |
| •<br>Ndb_api_trans_abort_count_slave                                                                                                                                                                  |  |
| •<br>[none]                                                                                                                                                                                           |  |
|                                                                                                                                                                                                       |  |
| •<br>Ndb_api_trans_abort_count                                                                                                                                                                        |  |
| Number of transactions aborted.<br>•<br>TransCloseCount<br>Ndb_api_trans_close_count_session                                                                                                          |  |
| (This value may be greater than<br>•<br>Ndb_api_trans_close_count_slave<br>the sum of TransCommitCount                                                                                                |  |
| and TransAbortCount.)<br>•<br>[none]                                                                                                                                                                  |  |
| •<br>Ndb_api_trans_close_count                                                                                                                                                                        |  |
| Number of operations based<br>•<br>PkOpCount<br>Ndb_api_pk_op_count_session                                                                                                                           |  |
| on or using primary keys. This<br>•<br>Ndb_api_pk_op_count_slave<br>count includes blob-part table                                                                                                    |  |

| Counter Name           | Description                                                                            | Status Variables (by statistic<br>type):                                       |
|------------------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
|                        |                                                                                        | •<br>Session                                                                   |
|                        |                                                                                        | •<br>Slave (replica)                                                           |
|                        |                                                                                        | •<br>Injector                                                                  |
|                        |                                                                                        | •<br>Server                                                                    |
|                        | operations, as well as primary<br>key operations normally visible to<br>MySQL clients. | •<br>Ndb_api_pk_op_count                                                       |
| UkOpCount              | Number of operations based on<br>or using unique keys.                                 | •<br>Ndb_api_uk_op_count_session                                               |
|                        |                                                                                        | •<br>Ndb_api_uk_op_count_slave                                                 |
|                        |                                                                                        | •<br>[none]                                                                    |
|                        |                                                                                        | •<br>Ndb_api_uk_op_count                                                       |
| TableScanCount         | Number of table scans that<br>have been started. This includes                         | •<br>Ndb_api_table_scan_count_session                                          |
|                        | scans of internal tables.                                                              | •<br>Ndb_api_table_scan_count_slave                                            |
|                        |                                                                                        | •<br>[none]                                                                    |
|                        |                                                                                        | •<br>Ndb_api_table_scan_count                                                  |
| RangeScanCount         | Number of range scans that have<br>been started.                                       | •<br>Ndb_api_range_scan_count_session                                          |
|                        |                                                                                        | •<br>Ndb_api_range_scan_count_slave                                            |
|                        |                                                                                        | •<br>[none]                                                                    |
|                        |                                                                                        | •<br>Ndb_api_range_scan_count                                                  |
| PrunedScanCount        | Number of scans that have been<br>pruned to a single partition.                        | •<br>Ndb_api_pruned_scan_count_session                                         |
|                        |                                                                                        | •<br>Ndb_api_pruned_scan_count_slave                                           |
|                        |                                                                                        | •<br>[none]                                                                    |
|                        |                                                                                        | •<br>Ndb_api_pruned_scan_count                                                 |
| ScanBatchCount         | Number of batches of rows<br>received. (A batch in this context                        | •<br>Ndb_api_scan_batch_count_session                                          |
|                        | is a set of scan results from a<br>single fragment.)                                   | •<br>Ndb_api_scan_batch_count_slave                                            |
|                        |                                                                                        | •<br>[none]                                                                    |
| ReadRowCount           | Total number of rows that have                                                         | •<br>Ndb_api_scan_batch_count<br>•<br>Ndb_api_read_row_count_session           |
|                        | been read. Includes rows read                                                          | •<br>Ndb_api_read_row_count_slave                                              |
|                        | using primary key, unique key,<br>and scan operations.                                 |                                                                                |
|                        |                                                                                        | •<br>[none]                                                                    |
| TransLocalReadRowCount | Number of rows read from the                                                           | •<br>Ndb_api_read_row_count<br>•<br>Ndb_api_trans_local_read_row_count_session |
|                        | data same node on which the<br>transaction was being run.                              | •<br>Ndb_api_trans_local_read_row_count_slave                                  |
|                        |                                                                                        |                                                                                |

| Counter Name            | Description                      |   | Status Variables (by statistic<br>type): |
|-------------------------|----------------------------------|---|------------------------------------------|
|                         |                                  | • | Session                                  |
|                         |                                  | • | Slave (replica)                          |
|                         |                                  | • | Injector                                 |
|                         |                                  | • | Server                                   |
|                         |                                  | • | [none]                                   |
|                         |                                  | • | Ndb_api_trans_local_read_row_count       |
| DataEventsRecvdCount    | Number of row change events      | • | [none]                                   |
|                         | received.                        | • | [none]                                   |
|                         |                                  | • | Ndb_api_event_data_count_injector        |
|                         |                                  | • | Ndb_api_event_data_count                 |
| NondataEventsRecvdCount | Number of events received, other | • | [none]                                   |
|                         | than row change events.          | • | [none]                                   |
|                         |                                  | • | Ndb_api_event_nondata_count_injector     |
|                         |                                  | • | Ndb_api_event_nondata_count              |
| EventBytesRecvdCount    | Number of bytes of events        | • | [none]                                   |
|                         | received.                        | • | [none]                                   |
|                         |                                  | • | Ndb_api_event_bytes_count_injector       |
|                         |                                  |   |                                          |

To see all counts of committed transactions—that is, all TransCommitCount counter status variables —you can filter the results of SHOW STATUS for the substring trans\_commit\_count, like this:

```
mysql> SHOW STATUS LIKE '%trans_commit_count%';
+------------------------------------+-------+
| Variable_name | Value |
+------------------------------------+-------+
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_commit_count_slave | 0 |
| Ndb_api_trans_commit_count | 2 |
+------------------------------------+-------+
3 rows in set (0.00 sec)
```

From this you can determine that 1 transaction has been committed in the current mysql client session, and 2 transactions have been committed on this mysqld since it was last restarted.

You can see how various NDB API counters are incremented by a given SQL statement by comparing the values of the corresponding \_session status variables immediately before and after performing the statement. In this example, after getting the initial values from SHOW STATUS, we create in the test database an NDB table, named t, that has a single column:

```
mysql> SHOW STATUS LIKE 'ndb_api%session%';
+--------------------------------------------+--------+
| Variable_name | Value |
+--------------------------------------------+--------+
| Ndb_api_wait_exec_complete_count_session | 2 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 3 |
```

```
| Ndb_api_wait_nanos_count_session | 820705 |
| Ndb_api_bytes_sent_count_session | 132 |
| Ndb_api_bytes_received_count_session | 372 |
| Ndb_api_trans_start_count_session | 1 |
| Ndb_api_trans_commit_count_session | 1 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 1 |
| Ndb_api_pk_op_count_session | 1 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 1 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+--------+
18 rows in set (0.00 sec)
mysql> USE test;
Database changed
mysql> CREATE TABLE t (c INT) ENGINE NDBCLUSTER;
Query OK, 0 rows affected (0.85 sec)
```

Now you can execute a new SHOW STATUS statement and observe the changes, as shown here (with the changed rows highlighted in the output):

```
mysql> SHOW STATUS LIKE 'ndb_api%session%';
+--------------------------------------------+-----------+
| Variable_name | Value |
+--------------------------------------------+-----------+
| Ndb_api_wait_exec_complete_count_session | 8 |
| Ndb_api_wait_scan_result_count_session | 0 |
| Ndb_api_wait_meta_request_count_session | 17 |
| Ndb_api_wait_nanos_count_session | 706871709 |
| Ndb_api_bytes_sent_count_session | 2376 |
| Ndb_api_bytes_received_count_session | 3844 |
| Ndb_api_trans_start_count_session | 4 |
| Ndb_api_trans_commit_count_session | 4 |
| Ndb_api_trans_abort_count_session | 0 |
| Ndb_api_trans_close_count_session | 4 |
| Ndb_api_pk_op_count_session | 6 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 0 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 2 |
| Ndb_api_trans_local_read_row_count_session | 1 |
+--------------------------------------------+-----------+
18 rows in set (0.00 sec)
```

Similarly, you can see the changes in the NDB API statistics counters caused by inserting a row into t: Insert the row, then run the same SHOW STATUS statement used in the previous example, as shown here:

```
mysql> INSERT INTO t VALUES (100);
Query OK, 1 row affected (0.00 sec)
mysql> SHOW STATUS LIKE 'ndb_api%session%';
+--------------------------------------------+-----------+
| Variable_name | Value |
+--------------------------------------------+-----------+
| Ndb_api_wait_exec_complete_count_session | 11 |
| Ndb_api_wait_scan_result_count_session | 6 |
| Ndb_api_wait_meta_request_count_session | 20 |
| Ndb_api_wait_nanos_count_session | 707370418 |
| Ndb_api_bytes_sent_count_session | 2724 |
| Ndb_api_bytes_received_count_session | 4116 |
| Ndb_api_trans_start_count_session | 7 |
| Ndb_api_trans_commit_count_session | 6 |
| Ndb_api_trans_abort_count_session | 0 |
```

```
| Ndb_api_trans_close_count_session | 7 |
| Ndb_api_pk_op_count_session | 8 |
| Ndb_api_uk_op_count_session | 0 |
| Ndb_api_table_scan_count_session | 1 |
| Ndb_api_range_scan_count_session | 0 |
| Ndb_api_pruned_scan_count_session | 0 |
| Ndb_api_scan_batch_count_session | 0 |
| Ndb_api_read_row_count_session | 3 |
| Ndb_api_trans_local_read_row_count_session | 2 |
+--------------------------------------------+-----------+
18 rows in set (0.00 sec)
```

We can make a number of observations from these results:

- Although we created t with no explicit primary key, 5 primary key operations were performed in doing so (the difference in the "before" and "after" values of Ndb\_api\_pk\_op\_count\_session, or 6 minus 1). This reflects the creation of the hidden primary key that is a feature of all tables using the NDB storage engine.
- By comparing successive values for Ndb\_api\_wait\_nanos\_count\_session, we can see that the NDB API operations implementing the CREATE TABLE statement waited much longer (706871709 - 820705 = 706051004 nanoseconds, or approximately 0.7 second) for responses from the data nodes than those executed by the INSERT (707370418 - 706871709 = 498709 ns or roughly .0005 second). The execution times reported for these statements in the mysql client correlate roughly with these figures.

On platforms without sufficient (nanosecond) time resolution, small changes in the value of the WaitNanosCount NDB API counter due to SQL statements that execute very quickly may not always be visible in the values of Ndb\_api\_wait\_nanos\_count\_session, Ndb\_api\_wait\_nanos\_count\_slave, or Ndb\_api\_wait\_nanos\_count.

• The INSERT statement incremented both the ReadRowCount and TransLocalReadRowCount NDB API statistics counters, as reflected by the increased values of Ndb\_api\_read\_row\_count\_session and Ndb\_api\_trans\_local\_read\_row\_count\_session.

# <span id="page-126-0"></span>**25.6.16 ndbinfo: The NDB Cluster Information Database**

ndbinfo is a database containing information specific to NDB Cluster.

This database contains a number of tables, each providing a different sort of data about NDB Cluster node status, resource usage, and operations. You can find more detailed information about each of these tables in the next several sections.

ndbinfo is included with NDB Cluster support in the MySQL Server; no special compilation or configuration steps are required; the tables are created by the MySQL Server when it connects to the cluster. You can verify that ndbinfo support is active in a given MySQL Server instance using SHOW PLUGINS; if ndbinfo support is enabled, you should see a row containing ndbinfo in the Name column and ACTIVE in the Status column, as shown here (emphasized text):

| mysql> SHOW PLUGINS;        |                 |                                    |      |                   |
|-----------------------------|-----------------|------------------------------------|------|-------------------|
| ++++++<br>  Name<br>++++++  | Status   Type   |                                    |      | Library   License |
| binlog                      |                 | ACTIVE   STORAGE ENGINE            | NULL | GPL<br>           |
| mysql_native_password       |                 | ACTIVE   AUTHENTICATION            | NULL | GPL<br>           |
| sha256_password             |                 | ACTIVE   AUTHENTICATION            | NULL | GPL<br>           |
| caching_sha2_password       |                 | ACTIVE   AUTHENTICATION            | NULL | GPL<br>           |
| sha2_cache_cleaner          | ACTIVE   AUDIT  |                                    | NULL | GPL<br>           |
| daemon_keyring_proxy_plugin | ACTIVE   DAEMON |                                    | NULL | GPL<br>           |
| CSV                         |                 | ACTIVE   STORAGE ENGINE            | NULL | GPL<br>           |
| MEMORY                      |                 | ACTIVE   STORAGE ENGINE            | NULL | GPL<br>           |
| InnoDB                      |                 | ACTIVE   STORAGE ENGINE            | NULL | GPL<br>           |
| INNODB_TRX                  |                 | ACTIVE   INFORMATION SCHEMA   NULL |      | GPL<br>           |
| INNODB_CMP                  |                 | ACTIVE   INFORMATION SCHEMA   NULL |      | GPL<br>           |
| INNODB_CMP_RESET            |                 | ACTIVE   INFORMATION SCHEMA   NULL |      | GPL<br>           |

```
| INNODB_CMPMEM | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMPMEM_RESET | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP_PER_INDEX | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CMP_PER_INDEX_RESET | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_PAGE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_PAGE_LRU | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_BUFFER_POOL_STATS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_TEMP_TABLE_INFO | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_METRICS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_DEFAULT_STOPWORD | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_DELETED | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_BEING_DELETED | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_CONFIG | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_INDEX_CACHE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_FT_INDEX_TABLE | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_TABLES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_TABLESTATS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_INDEXES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_TABLESPACES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_COLUMNS | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_VIRTUAL | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_CACHED_INDEXES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| INNODB_SESSION_TEMP_TABLESPACES | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| MyISAM | ACTIVE | STORAGE ENGINE | NULL | GPL |
| MRG_MYISAM | ACTIVE | STORAGE ENGINE | NULL | GPL |
| PERFORMANCE_SCHEMA | ACTIVE | STORAGE ENGINE | NULL | GPL |
| TempTable | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ARCHIVE | ACTIVE | STORAGE ENGINE | NULL | GPL |
| BLACKHOLE | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndbcluster | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndbinfo | ACTIVE | STORAGE ENGINE | NULL | GPL |
| ndb_transid_mysql_connection_map | ACTIVE | INFORMATION SCHEMA | NULL | GPL |
| ngram | ACTIVE | FTPARSER | NULL | GPL |
| mysqlx_cache_cleaner | ACTIVE | AUDIT | NULL | GPL |
| mysqlx | ACTIVE | DAEMON | NULL | GPL |
+----------------------------------+--------+--------------------+---------+---------+
47 rows in set (0.00 sec)
```

You can also do this by checking the output of SHOW ENGINES for a line including ndbinfo in the Engine column and YES in the Support column, as shown here (emphasized text):

```
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
 Engine: ndbcluster
 Support: YES
 Comment: Clustered, fault-tolerant tables
Transactions: YES
 XA: NO
 Savepoints: NO
*************************** 2. row ***************************
 Engine: CSV
 Support: YES
 Comment: CSV storage engine
Transactions: NO
 XA: NO
 Savepoints: NO
*************************** 3. row ***************************
 Engine: InnoDB
 Support: DEFAULT
 Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
 XA: YES
 Savepoints: YES
*************************** 4. row ***************************
 Engine: BLACKHOLE
 Support: YES
 Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
 XA: NO
 Savepoints: NO
*************************** 5. row ***************************
 Engine: MyISAM
```

```
Support: YES
    Comment: MyISAM storage engine
Transactions: NO
       XA: NO
 Savepoints: NO
       ************** 6. row **************
    Engine: MRG MYISAM
    Support: YES
    Comment: Collection of identical MyISAM tables
Transactions: NO
       XA: NO
 Savepoints: NO
            ******* 7. row ***************
    Engine: ARCHIVE
   Support: YES
    Comment: Archive storage engine
Transactions: NO
       XA: NO
 Savepoints: NO
      ***************** 8. row ***************
    Engine: ndbinfo
   Support: YES
    Comment: NDB Cluster system information storage engine
Transactions: NO
       XA: NO
 Savepoints: NO
      ************** 9. row **************
    Engine: PERFORMANCE SCHEMA
   Support: YES
    Comment: Performance Schema
Transactions: NO
       XA: NO
 Savepoints: NO
            ********* 10. row ***************
    Engine: MEMORY
   Support: YES
    Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
        XA: NO
 Savepoints: NO
10 rows in set (0.00 sec)
```

If ndbinfo support is enabled, then you can access ndbinfo using SQL statements in mysql or another MySQL client. For example, you can see ndbinfo listed in the output of SHOW DATABASES, as shown here (emphasized text):

```
mysql> SHOW DATABASES;
+------+
| Database
```

If the <code>mysqld</code> process was not started with the <code>--ndbcluster</code> option, <code>ndbinfo</code> is not available and is not displayed by <code>SHOW DATABASES</code>. If <code>mysqld</code> was formerly connected to an NDB Cluster but the cluster becomes unavailable (due to events such as cluster shutdown, loss of network connectivity, and so forth), <code>ndbinfo</code> and its tables remain visible, but an attempt to access any tables (other than <code>blocks or config\_params</code>) fails with <code>Got error 157 'Connection to NDB failed' from NDBINFO</code>.

With the exception of the blocks and config\_params tables, what we refer to as ndbinfo "tables" are actually views generated from internal NDB tables not normally visible to the MySQL Server. You can make these tables visible by setting the ndbinfo\_show\_hidden system variable to ON (or 1), but this is normally not necessary.

All ndbinfo tables are read-only, and are generated on demand when queried. Because many of them are generated in parallel by the data nodes while other are specific to a given SQL node, they are not guaranteed to provide a consistent snapshot.

In addition, pushing down of joins is not supported on ndbinfo tables; so joining large ndbinfo tables can require transfer of a large amount of data to the requesting API node, even when the query makes use of a WHERE clause.

ndbinfo tables are not included in the query cache. (Bug #59831)

You can select the ndbinfo database with a USE statement, and then issue a SHOW TABLES statement to obtain a list of tables, just as for any other database, like this:

```
mysql> USE ndbinfo;
Database changed
mysql> SHOW TABLES;
+---------------------------------+
| Tables_in_ndbinfo |
+---------------------------------+
| arbitrator_validity_detail |
| arbitrator_validity_summary |
| backup_id |
| blobs |
| blocks |
| cluster_locks |
| cluster_operations |
| cluster_transactions |
| config_nodes |
| config_params |
| config_values |
| counters |
| cpudata |
| cpudata_1sec |
| cpudata_20sec |
| cpudata_50ms |
| cpuinfo |
| cpustat |
| cpustat_1sec |
| cpustat_20sec |
| cpustat_50ms |
| dict_obj_info |
| dict_obj_tree |
| dict_obj_types |
| dictionary_columns |
| dictionary_tables |
| disk_write_speed_aggregate |
| disk_write_speed_aggregate_node |
| disk_write_speed_base |
| diskpagebuffer |
| diskstat |
| diskstats_1sec |
| error_messages |
| events |
| files |
| foreign_keys |
| hash_maps |
| hwinfo |
| index_columns |
| index_stats |
| locks_per_fragment |
| logbuffers |
| logspaces |
| membership |
| memory_per_fragment |
| memoryusage |
| nodes |
| operations_per_fragment |
| pgman_time_track_stats |
| processes |
```

```
| resources |
| restart_info |
| server_locks |
| server_operations |
| server_transactions |
| table_distribution_status |
| table_fragments |
| table_info |
| table_replicas |
| tc_time_track_stats |
| threadblocks |
| threads |
| threadstat |
| transporter_details |
| transporters |
+---------------------------------+
65 rows in set (0.00 sec)
```

All ndbinfo tables use the NDB storage engine; however, an ndbinfo entry still appears in the output of SHOW ENGINES and SHOW PLUGINS as described previously.

You can execute SELECT statements against these tables, just as you would normally expect:

```
mysql> SELECT * FROM memoryusage;
+---------+---------------------+--------+------------+------------+-------------+
| node_id | memory_type | used | used_pages | total | total_pages |
+---------+---------------------+--------+------------+------------+-------------+
| 5 | Data memory | 425984 | 13 | 2147483648 | 65536 |
| 5 | Long message buffer | 393216 | 1536 | 67108864 | 262144 |
| 6 | Data memory | 425984 | 13 | 2147483648 | 65536 |
| 6 | Long message buffer | 393216 | 1536 | 67108864 | 262144 |
| 7 | Data memory | 425984 | 13 | 2147483648 | 65536 |
| 7 | Long message buffer | 393216 | 1536 | 67108864 | 262144 |
| 8 | Data memory | 425984 | 13 | 2147483648 | 65536 |
| 8 | Long message buffer | 393216 | 1536 | 67108864 | 262144 |
+---------+---------------------+--------+------------+------------+-------------+
8 rows in set (0.09 sec)
```

More complex queries, such as the two following SELECT statements using the [memoryusage](#page-174-0) table, are possible:

```
mysql> SELECT SUM(used) as 'Data Memory Used, All Nodes'
 > FROM memoryusage
 > WHERE memory_type = 'Data memory';
+-----------------------------+
| Data Memory Used, All Nodes |
+-----------------------------+
| 6460 |
+-----------------------------+
1 row in set (0.09 sec)
mysql> SELECT SUM(used) as 'Long Message Buffer, All Nodes'
 > FROM memoryusage
 > WHERE memory_type = 'Long message buffer';
+-------------------------------------+
| Long Message Buffer Used, All Nodes |
+-------------------------------------+
| 1179648 |
+-------------------------------------+
1 row in set (0.08 sec)
```

ndbinfo table and column names are case-sensitive (as is the name of the ndbinfo database itself). These identifiers are in lowercase. Trying to use the wrong lettercase results in an error, as shown in this example:

```
mysql> SELECT * FROM nodes;
+---------+--------+---------+-------------+-------------------+
| node_id | uptime | status | start_phase | config_generation |
+---------+--------+---------+-------------+-------------------+
| 5 | 17707 | STARTED | 0 | 1 |
```

```
| 6 | 17706 | STARTED | 0 | 1 |
| 7 | 17705 | STARTED | 0 | 1 |
| 8 | 17704 | STARTED | 0 | 1 |
+---------+--------+---------+-------------+-------------------+
4 rows in set (0.06 sec)
mysql> SELECT * FROM Nodes;
ERROR 1146 (42S02): Table 'ndbinfo.Nodes' doesn't exist
```

mysqldump ignores the ndbinfo database entirely, and excludes it from any output. This is true even when using the --databases or --all-databases option.

NDB Cluster also maintains tables in the INFORMATION\_SCHEMA information database, including the FILES table which contains information about files used for NDB Cluster Disk Data storage, and the ndb\_transid\_mysql\_connection\_map table, which shows the relationships between transactions, transaction coordinators, and NDB Cluster API nodes. For more information, see the descriptions of the tables or Section 25.6.17, "INFORMATION\_SCHEMA Tables for NDB Cluster".