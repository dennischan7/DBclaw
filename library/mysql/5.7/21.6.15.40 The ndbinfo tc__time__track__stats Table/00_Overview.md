---
source: MySQL 5.7 Reference
title: 00_Overview
---

The tc\_time\_track\_stats table provides time-tracking information obtained from the [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) block (TC) instances in the data nodes, through API nodes access NDB. Each TC instance tracks latencies for a set of activities it undertakes on behalf of API nodes or other data nodes; these activities include transactions, transaction errors, key reads, key writes, unique index operations, failed key operations of any type, scans, failed scans, fragment scans, and failed fragment scans.

A set of counters is maintained for each activity, each counter covering a range of latencies less than or equal to an upper bound. At the conclusion of each activity, its latency is determined and the appropriate counter incremented. tc\_time\_track\_stats presents this information as rows, with a row for each instance of the following:

- Data node, using its ID
- TC block instance
- Other communicating data node or API node, using its ID
- Upper bound value

### **Notes**

Each row contains a value for each activity type. This is the number of times that this activity occurred with a latency within the range specified by the row (that is, where the latency does not exceed the upper bound).

The tc\_time\_track\_stats table contains the following columns:

• node\_id

Requesting node ID

• block\_number

TC block number

• block\_instance

TC block instance number

• comm\_node\_id

Node ID of communicating API or data node

• upper\_bound

Upper bound of interval (in microseconds)

• scans

Based on duration of successful scans from opening to closing, tracked against the API or data nodes requesting them.

• scan\_errors

Based on duration of failed scans from opening to closing, tracked against the API or data nodes requesting them.

• scan\_fragments

Based on duration of successful fragment scans from opening to closing, tracked against the data nodes executing them

• scan\_fragment\_errors

Based on duration of failed fragment scans from opening to closing, tracked against the data nodes executing them

• transactions

Based on duration of successful transactions from beginning until sending of commit ACK, tracked against the API or data nodes requesting them. Stateless transactions are not included.

• transaction\_errors

Based on duration of failing transactions from start to point of failure, tracked against the API or data nodes requesting them.

• read\_key\_ops

Based on duration of successful primary key reads with locks. Tracked against both the API or data node requesting them and the data node executing them.

• write\_key\_ops

Based on duration of successful primary key writes, tracked against both the API or data node requesting them and the data node executing them.

• index\_key\_ops

Based on duration of successful unique index key operations, tracked against both the API or data node requesting them and the data node executing reads of base tables.

• key\_op\_errors

Based on duration of all unsuccessful key read or write operations, tracked against both the API or data node requesting them and the data node executing them.

The block\_instance column provides the [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) kernel block instance number. You can use this together with the block name to obtain information about specific threads from the [threadblocks](#page-85-0) table.

# <span id="page-85-0"></span>**21.6.15.41 The ndbinfo threadblocks Table**

The threadblocks table associates data nodes, threads, and instances of NDB kernel blocks.

The threadblocks table contains the following columns:

• node\_id

Node ID

• thr\_no

Thread ID

• block\_name

Block name

• block\_instance

Block instance number

### **Notes**

The value of the block\_name in this table is one of the values found in the block\_name column when selecting from the [ndbinfo.blocks](#page-27-0) table. Although the list of possible values is static for a given NDB Cluster release, the list may vary between releases.

The block\_instance column provides the kernel block instance number.

# <span id="page-86-0"></span>**21.6.15.42 The ndbinfo threads Table**

The threads table provides information about threads running in the NDB kernel.

The threads table contains the following columns:

• node\_id

ID of the node where the thread is running

• thr\_no

Thread ID (specific to this node)

• thread\_name

Thread name (type of thread)

• thread\_description

Thread (type) description

# **Notes**

Sample output from a 2-node example cluster, including thread descriptions, is shown here:

| mysql> SELECT * FROM threads;<br>+++++ |  |          |                                                                 |  |
|----------------------------------------|--|----------|-----------------------------------------------------------------|--|
|                                        |  |          | node_id   thr_no   thread_name   thread_description             |  |
| <br>5                                  |  | 0   main | +++++<br>  main thread, schema and distribution handling        |  |
| <br>5                                  |  | 1   rep  | rep thread, asynch replication and proxy block handling         |  |
| <br>5                                  |  | 2   ldm  | ldm thread, handling a set of data partitions                   |  |
| <br>5                                  |  | 3   recv | receive thread, performing receive and polling for new receives |  |
| <br>6                                  |  | 0   main | main thread, schema and distribution handling                   |  |
| <br>6                                  |  | 1   rep  | rep thread, asynch replication and proxy block handling         |  |

```
| 6 | 2 | ldm | ldm thread, handling a set of data partitions |
| 6 | 3 | recv | receive thread, performing receive and polling for new receives |
+---------+--------+-------------+------------------------------------------------------------------+
8 rows in set (0.01 sec)
```

This table was added in NDB 7.5.2.