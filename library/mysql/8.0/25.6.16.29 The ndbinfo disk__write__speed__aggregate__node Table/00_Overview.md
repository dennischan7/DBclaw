---
source: MySQL 8.0 Reference
title: 00_Overview
---

The disk\_write\_speed\_aggregate\_node table provides aggregated information per node about the speed of disk writes during LCP, backup, and restore operations.

The disk\_write\_speed\_aggregate\_node table contains the following columns:

• node\_id

Node ID of this node

• backup\_lcp\_speed\_last\_sec

Number of bytes written to disk by backup and LCP processes in the last second

• redo\_speed\_last\_sec

Number of bytes written to the redo log in the last second

• backup\_lcp\_speed\_last\_10sec

Number of bytes written to disk by backup and LCP processes per second, averaged over the last 10 seconds

• redo\_speed\_last\_10sec

Number of bytes written to the redo log each second, averaged over the last 10 seconds

• backup\_lcp\_speed\_last\_60sec

Number of bytes written to disk by backup and LCP processes per second, averaged over the last 60 seconds

• redo\_speed\_last\_60sec

Number of bytes written to the redo log each second, averaged over the last 60 seconds

# <span id="page-160-0"></span>**25.6.16.30 The ndbinfo diskpagebuffer Table**

The diskpagebuffer table provides statistics about disk page buffer usage by NDB Cluster Disk Data tables.

The diskpagebuffer table contains the following columns:

• node\_id

The data node ID

• block\_instance

Block instance

• pages\_written

Number of pages written to disk.

• pages\_written\_lcp

Number of pages written by local checkpoints.

• pages\_read

Number of pages read from disk

• log\_waits

Number of page writes waiting for log to be written to disk

• page\_requests\_direct\_return

Number of requests for pages that were available in buffer

• page\_requests\_wait\_queue

Number of requests that had to wait for pages to become available in buffer

• page\_requests\_wait\_io

Number of requests that had to be read from pages on disk (pages were unavailable in buffer)

### **Notes**

You can use this table with NDB Cluster Disk Data tables to determine whether DiskPageBufferMemory is sufficiently large to allow data to be read from the buffer rather from disk; minimizing disk seeks can help improve performance of such tables.

You can determine the proportion of reads from DiskPageBufferMemory to the total number of reads using a query such as this one, which obtains this ratio as a percentage:

```
SELECT
 node_id,
 100 * page_requests_direct_return /
 (page_requests_direct_return + page_requests_wait_io)
 AS hit_ratio
FROM ndbinfo.diskpagebuffer;
```

The result from this query should be similar to what is shown here, with one row for each data node in the cluster (in this example, the cluster has 4 data nodes):

```
+---------+-----------+
| node_id | hit_ratio |
+---------+-----------+
| 5 | 97.6744 |
| 6 | 97.6879 |
| 7 | 98.1776 |
| 8 | 98.1343 |
+---------+-----------+
4 rows in set (0.00 sec)
```

hit\_ratio values approaching 100% indicate that only a very small number of reads are being made from disk rather than from the buffer, which means that Disk Data read performance is approaching an optimum level. If any of these values are less than 95%, this is a strong indicator that the setting for DiskPageBufferMemory needs to be increased in the config.ini file.

![](_page_161_Picture_8.jpeg)

### **Note**

A change in DiskPageBufferMemory requires a rolling restart of all of the cluster's data nodes before it takes effect.

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the threadblocks table. Using this information, you can obtain information about disk page buffer metrics relating to individual threads; an example query using LIMIT 1 to limit the output to a single thread is shown here:

```
mysql> SELECT
 > node_id, thr_no, block_name, thread_name, pages_written,
 > pages_written_lcp, pages_read, log_waits,
 > page_requests_direct_return, page_requests_wait_queue,
 > page_requests_wait_io
 > FROM ndbinfo.diskpagebuffer
 > INNER JOIN ndbinfo.threadblocks USING (node_id, block_instance)
 > INNER JOIN ndbinfo.threads USING (node_id, thr_no)
 > WHERE block_name = 'PGMAN' LIMIT 1\G
*************************** 1. row ***************************
 node_id: 1
 thr_no: 1
 block_name: PGMAN
 thread_name: rep
 pages_written: 0
 pages_written_lcp: 0
 pages_read: 1
 log_waits: 0
page_requests_direct_return: 4
 page_requests_wait_queue: 0
 page_requests_wait_io: 1
1 row in set (0.01 sec)
```

# <span id="page-161-0"></span>**25.6.16.31 The ndbinfo diskstat Table**

The diskstat table provides information about writes to Disk Data tablespaces during the past 1 second.

The diskstat table contains the following columns:

• node\_id

Node ID of this node

• block\_instance

ID of reporting instance of [PGMAN](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-pgman.md)

• pages\_made\_dirty

Number of pages made dirty during the past second

• reads\_issued

Reads issued during the past second

• reads\_completed

Reads completed during the past second

• writes\_issued

Writes issued during the past second

• writes\_completed

Writes completed during the past second

• log\_writes\_issued

Number of times a page write has required a log write during the past second

• log\_writes\_completed

Number of log writes completed during the last second

• get\_page\_calls\_issued

Number of get\_page() calls issued during the past second

• get\_page\_reqs\_issued

Number of times that a get\_page() call has resulted in a wait for I/O or completion of I/O already begun during the past second

• get\_page\_reqs\_completed

Number of get\_page() calls waiting for I/O or I/O completion that have completed during the past second

### **Notes**

Each row in this table corresponds to an instance of [PGMAN](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-pgman.md); there is one such instance per LDM thread plus an additional instance for each data node.

# <span id="page-162-0"></span>**25.6.16.32 The ndbinfo diskstats\_1sec Table**

The diskstats\_1sec table provides information about writes to Disk Data tablespaces over the past 20 seconds.

The diskstat table contains the following columns:

• node\_id

Node ID of this node

• block\_instance

ID of reporting instance of [PGMAN](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-pgman.md)

• pages\_made\_dirty

Pages made dirty during the designated 1-second interval

• reads\_issued

Reads issued during the designated 1-second interval

• reads\_completed

Reads completed during the designated 1-second interval

• writes\_issued

Writes issued during the designated 1-second interval

• writes\_completed

Writes completed during the designated 1-second interval

• log\_writes\_issued

Number of times a page write has required a log write during the designated 1-second interval

• log\_writes\_completed

Number of log writes completed during the designated 1-second interval

• get\_page\_calls\_issued

Number of get\_page() calls issued during the designated 1-second interval

• get\_page\_reqs\_issued

Number of times that a get\_page() call has resulted in a wait for I/O or completion of I/O already begun during the designated 1-second interval

• get\_page\_reqs\_completed

Number of get\_page() calls waiting for I/O or I/O completion that have completed during the designated 1-second interval

• seconds\_ago

Number of 1-second intervals in the past of the interval to which this row applies

### **Notes**

Each row in this table corresponds to an instance of [PGMAN](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-pgman.md) during a 1-second interval occurring from 0 to 19 seconds ago; there is one such instance per LDM thread plus an additional instance for each data node.