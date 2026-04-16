---
source: MySQL 8.4 Reference
title: 00_Overview
---

The following sections describe tables associated with the Telemetry services:

### <span id="page-141-0"></span>**29.12.21.1 The setup\_meters Table**

The [setup\\_meters](#page-141-0) table lists the registered meters:

```
mysql> select * from performance_schema.setup_meters;
+------------------------+-----------+---------+-------------------------------------------+
| NAME | FREQUENCY | ENABLED | DESCRIPTION |
```

```
+------------------------+-----------+---------+-------------------------------------------+
| mysql.inno | 10 | YES | MySql InnoDB metrics |
| mysql.inno.buffer_pool | 10 | YES | MySql InnoDB buffer pool metrics |
| mysql.inno.data | 10 | YES | MySql InnoDB data metrics |
| mysql.x | 10 | YES | MySql X plugin metrics |
| mysql.x.stmt | 10 | YES | MySql X plugin statement statistics |
| mysql.stats | 10 | YES | MySql core metrics |
| mysql.stats.com | 10 | YES | MySql command stats |
| mysql.stats.connection | 10 | YES | MySql connection stats |
| mysql.stats.handler | 10 | YES | MySql handler stats |
| mysql.stats.ssl | 10 | YES | MySql TLS related stats |
| mysql.myisam | 10 | YES | MySql MyISAM storage engine stats |
| mysql.perf_schema | 10 | YES | MySql performance_schema lost instruments |
+------------------------+-----------+---------+-------------------------------------------+
```

- NAME: Name of the meter.
- FREQUENCY: Frequency in seconds of metric export. Default is every 10 seconds. This value can be edited for registered meters.
- ENABLED: Whether the meter is enabled. The value is YES or NO. A disabled meter exports no metrics. This column can be modified
- DESCRIPTION: A string describing the meter.

FREQUENCY and ENABLED can be edited.

### <span id="page-142-0"></span>**29.12.21.2 The setup\_metrics Table**

The [setup\\_metrics](#page-142-0) table lists the available metrics:

```
mysql> select * from performance_schema.setup_metrics\G
*************************** 34. row ***************************
 NAME: undo_tablespaces_active
 METER: mysql.inno
METRIC_TYPE: ASYNC GAUGE COUNTER
 NUM_TYPE: INTEGER
 UNIT: 
DESCRIPTION: Number of active undo tablespaces, including implicit and explicit tablespaces (innodb_undo_tablespaces_active)
...
*************************** 48. row ***************************
 NAME: wait_free
 METER: mysql.inno.buffer_pool
METRIC_TYPE: ASYNC COUNTER
 NUM_TYPE: INTEGER
 UNIT: 
DESCRIPTION: Number of times waited for free buffer (innodb_buffer_pool_wait_free)
...
*************************** 55. row ***************************
 NAME: reads
 METER: mysql.inno.data
METRIC_TYPE: ASYNC COUNTER
 NUM_TYPE: INTEGER
 UNIT: 
DESCRIPTION: Number of reads initiated (innodb_data_reads)
...
*************************** 101. row ***************************
 NAME: ssl_finished_accepts
 METER: mysql.x
METRIC_TYPE: ASYNC COUNTER
 NUM_TYPE: INTEGER
 UNIT: 
DESCRIPTION: The number of successful SSL connections to the server (Mysqlx_ssl_finished_accepts)
...
*************************** 115. row ***************************
 NAME: list_clients
```

```
METER: mysql.x.stmt
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
    UNTT:
DESCRIPTION: The number of list client statements received (Mysqlx stmt list clients)
*********************** 162. row ****************
     NAME: slow_queries
    METER: mvsql.stats
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
     UNIT:
DESCRIPTION: The number of queries that have taken more than long_query_time seconds (Slow_queries)
           ********** 346. row **************
     NAME: stmt reprepare
    METER: mysql.stats.com
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
      IINITT.
DESCRIPTION: Number of times corresponding command statement has been executed.
**************************************
     NAME: errors tcpwrap
     METER: mysgl.stats.connection
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
     UNIT:
DESCRIPTION: The number of connections refused by the libwrap library (Connection errors topwrap)
**************************************
     NAME: update
    METER: mysql.stats.handler
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
     UNIT:
DESCRIPTION: The number of requests to update a row in a table (Handler update)
*********************** 384. row ****************
     NAME: callback cache_hits
    METER: mysql.stats.ssl
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
      UNIT:
DESCRIPTION: The number of accepted SSL connections (Ssl_callback_cache_hits)
**************************************
     NAME: key writes
    METER: mysql.myisam
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
     UNIT:
DESCRIPTION: The number of physical writes of a key block from the MyISAM key cache to disk (Key writes)
**************************************
     NAME: users lost
     METER: mysql.perf schema
METRIC TYPE: ASYNC COUNTER
  NUM TYPE: INTEGER
      UNIT:
DESCRIPTION: The number of times a row could not be added to the users table because it was full (Performan
```

The setup metrics table has the following columns:

• NAME: Name of the metric.

- METER: Name of the meter group of the metric.
- METRIC\_TYPE: The OpenTelemetry metric type.
- NUM\_TYPE: The numeric type. INTEGER or DOUBLE.
- DESCRIPTION: A string describing the metric's purpose.