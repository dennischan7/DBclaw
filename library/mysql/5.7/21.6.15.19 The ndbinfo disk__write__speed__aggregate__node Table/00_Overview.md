---
source: MySQL 5.7 Reference
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

# <span id="page-44-0"></span>**21.6.15.20 The ndbinfo diskpagebuffer Table**

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
```

```
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

![](_page_45_Picture_5.jpeg)

### **Note**

A change in DiskPageBufferMemory requires a rolling restart of all of the cluster's data nodes before it takes effect.

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the [threadblocks](#page-85-0) table. Using this information, you can obtain information about disk page buffer metrics relating to individual threads; an example query using LIMIT 1 to limit the output to a single thread is shown here:

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

# <span id="page-45-0"></span>**21.6.15.21 The ndbinfo error\_messages Table**

The error\_messages table provides information about

The error\_messages table contains the following columns:

• error\_code

Numeric error code

• error\_description

### Description of error

• error\_status

### Error status code

• error\_classification

Error classification code

### **Notes**

error\_code is a numeric NDB error code. This is the same error code that can be supplied to ndb\_perror or perror --ndb.

error\_description provides a basic description of the condition causing the error.

The error\_status column provides status information relating to the error. Possible values for this column are listed here:

- No error
- Illegal connect string
- Illegal server handle
- Illegal reply from server
- Illegal number of nodes
- Illegal node status
- Out of memory
- Management server not connected
- Could not connect to socket
- Start failed
- Stop failed
- Restart failed
- Could not start backup
- Could not abort backup
- Could not enter single user mode
- Could not exit single user mode
- Failed to complete configuration change
- Failed to get configuration
- Usage error
- Success
- Permanent error
- Temporary error

- Unknown result
- Temporary error, restart node
- Permanent error, external action needed
- Ndbd file system error, restart node initial
- Unknown

The error\_classification column shows the error classification. See [NDB Error Classifications](https://dev.mysql.com/doc/ndbapi/en/ndb-error-classifications.md), for information about classification codes and their meanings.

The error\_messages table was added in NDB 7.6.

# <span id="page-47-0"></span>**21.6.15.22 The ndbinfo locks\_per\_fragment Table**

The locks\_per\_fragment table provides information about counts of lock claim requests, and the outcomes of these requests on a per-fragment basis, serving as a companion table to [operations\\_per\\_fragment](#page-66-0) and [memory\\_per\\_fragment](#page-53-0). This table also shows the total time spent waiting for locks successfully and unsuccessfully since fragment or table creation, or since the most recent restart.

The locks\_per\_fragment table contains the following columns:

• fq\_name

Fully qualified table name

• parent\_fq\_name

Fully qualified name of parent object

• type

Table type; see text for possible values

• table\_id

Table ID

• node\_id

Reporting node ID

• block\_instance

LDM instance ID

• fragment\_num

Fragment identifier

• ex\_req

Exclusive lock requests started

• ex\_imm\_ok

Exclusive lock requests immediately granted

• ex\_wait\_ok

Exclusive lock requests granted following wait

• ex\_wait\_fail

Exclusive lock requests not granted

• sh\_req

Shared lock requests started

• sh\_imm\_ok

Shared lock requests immediately granted

• sh\_wait\_ok

Shared lock requests granted following wait

• sh\_wait\_fail

Shared lock requests not granted

• wait\_ok\_millis

Time spent waiting for lock requests that were granted, in milliseconds

• wait\_fail\_millis

Time spent waiting for lock requests that failed, in milliseconds

### **Notes**

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the [threadblocks](#page-85-0) table.

fq\_name is a fully qualified database object name in database/schema/name format, such as test/ def/t1 or sys/def/10/b\$unique.

parent\_fq\_name is the fully qualified name of this object's parent object (table).

table\_id is the table's internal ID generated by NDB. This is the same internal table ID shown in other ndbinfo tables; it is also visible in the output of ndb\_show\_tables.

The type column shows the type of table. This is always one of System table, User table, Unique hash index, Hash index, Unique ordered index, Ordered index, Hash index trigger, Subscription trigger, Read only constraint, Index trigger, Reorganize trigger, Tablespace, Log file group, Data file, Undo file, Hash map, Foreign key definition, Foreign key parent trigger, Foreign key child trigger, or Schema transaction.

The values shown in all of the columns ex\_req, ex\_req\_imm\_ok, ex\_wait\_ok, ex\_wait\_fail, sh\_req, sh\_req\_imm\_ok, sh\_wait\_ok, and sh\_wait\_fail represent cumulative numbers of requests since the table or fragment was created, or since the last restart of this node, whichever of these occurred later. This is also true for the time values shown in the wait\_ok\_millis and wait\_fail\_millis columns.

Every lock request is considered either to be in progress, or to have completed in some way (that is, to have succeeded or failed). This means that the following relationships are true:

```
ex_req >= (ex_req_imm_ok + ex_wait_ok + ex_wait_fail)
```

```
sh_req >= (sh_req_imm_ok + sh_wait_ok + sh_wait_fail)
```

The number of requests currently in progress is the current number of incomplete requests, which can be found as shown here:

```
[exclusive lock requests in progress] =
 ex_req - (ex_req_imm_ok + ex_wait_ok + ex_wait_fail)
[shared lock requests in progress] =
 sh_req - (sh_req_imm_ok + sh_wait_ok + sh_wait_fail)
```

A failed wait indicates an aborted transaction, but the abort may or may not be caused by a lock wait timeout. You can obtain the total number of aborts while waiting for locks as shown here:

```
[aborts while waiting for locks] = ex_wait_fail + sh_wait_fail
```

The locks\_per\_fragment table was added in NDB 7.5.3.

# <span id="page-49-1"></span>**21.6.15.23 The ndbinfo logbuffers Table**

The logbuffer table provides information on NDB Cluster log buffer usage.

The logbuffers table contains the following columns:

• node\_id

The ID of this data node.

• log\_type

Type of log. In NDB 7.5, one of: REDO or DD-UNDO. In NDB 7.6, one of: REDO, DD-UNDO, BACKUP-DATA, or BACKUP-LOG.

• log\_id

The log ID; for Disk Data undo log files, this is the same as the value shown in the LOGFILE\_GROUP\_NUMBER column of the Information Schema FILES table as well as the value shown for the log\_id column of the ndbinfo [logspaces](#page-49-0) table

• log\_part

The log part number

• total

Total space available for this log

• used

Space used by this log

### **Notes**

NDB 7.6.6 makes available logbuffers table rows reflecting two additional log types when performing an NDB backup. One of these rows has the log type BACKUP-DATA, which shows the amount of data buffer used during backup to copy fragments to backup files. The other row has the log type BACKUP-LOG, which displays the amount of log buffer used during the backup to record changes made after the backup has started. One each of these log\_type rows is shown in the logbuffers table for each data node in the cluster. These rows are not present unless an NDB backup is currently being performed. (Bug #25822988)

# <span id="page-49-0"></span>**21.6.15.24 The ndbinfo logspaces Table**

This table provides information about NDB Cluster log space usage.

The logspaces table contains the following columns:

• node\_id

The ID of this data node.

• log\_type

Type of log; one of: REDO or DD-UNDO.

• log\_id

The log ID; for Disk Data undo log files, this is the same as the value shown in the LOGFILE\_GROUP\_NUMBER column of the Information Schema FILES table as well as the value shown for the log\_id column of the ndbinfo [logbuffers](#page-49-1) table

• log\_part

The log part number.

• total

Total space available for this log.

• used

Space used by this log.

# <span id="page-50-0"></span>**21.6.15.25 The ndbinfo membership Table**

The membership table describes the view that each data node has of all the others in the cluster, including node group membership, president node, arbitrator, arbitrator successor, arbitrator connection states, and other information.

The membership table contains the following columns:

• node\_id

This node's node ID

• group\_id

Node group to which this node belongs

• left node

Node ID of the previous node

• right\_node

Node ID of the next node

• president

President's node ID

• successor

Node ID of successor to president

• succession\_order

Order in which this node succeeds to presidency

- Conf\_HB\_order
  - -
- arbitrator

Node ID of arbitrator

• arb\_ticket

Internal identifier used to track arbitration

• arb\_state

Arbitration state

• arb\_connected

Whether this node is connected to the arbitrator; either of Yes or No

• connected\_rank1\_arbs

Connected arbitrators of rank 1

• connected\_rank2\_arbs

Connected arbitrators of rank 1

### **Notes**

The node ID and node group ID are the same as reported by ndb\_mgm -e "SHOW".

left\_node and right\_node are defined in terms of a model that connects all data nodes in a circle, in order of their node IDs, similar to the ordering of the numbers on a clock dial, as shown here:

**Figure 21.8 Circular Arrangement of NDB Cluster Nodes**

![](_page_51_Picture_20.jpeg)

In this example, we have 8 data nodes, numbered 5, 6, 7, 8, 12, 13, 14, and 15, ordered clockwise in a circle. We determine "left" and "right" from the interior of the circle. The node to the left of node 5 is node 15, and the node to the right of node 5 is node 6. You can see all these relationships by running the following query and observing the output:

```
mysql> SELECT node_id,left_node,right_node
 -> FROM ndbinfo.membership;
+---------+-----------+------------+
| node_id | left_node | right_node |
```

|  |                          | ++++ |    |
|--|--------------------------|------|----|
|  | 5                        | 15   | 6  |
|  | 6                        | 5    | 7  |
|  | 7                        | 6    | 8  |
|  | 8                        | 7    | 12 |
|  | 12                       | 8    | 13 |
|  | 13                       | 12   | 14 |
|  | 14                       | 13   | 15 |
|  | 15                       | 14   | 5  |
|  |                          | ++++ |    |
|  | 8 rows in set (0.00 sec) |      |    |

The designations "left" and "right" are used in the event log in the same way.

The president node is the node viewed by the current node as responsible for setting an arbitrator (see [NDB Cluster Start Phases\)](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-start-phases.md). If the president fails or becomes disconnected, the current node expects the node whose ID is shown in the successor column to become the new president. The succession\_order column shows the place in the succession queue that the current node views itself as having.

In a normal NDB Cluster, all data nodes should see the same node as president, and the same node (other than the president) as its successor. In addition, the current president should see itself as 1 in the order of succession, the successor node should see itself as 2, and so on.

All nodes should show the same arb\_ticket values as well as the same arb\_state values. Possible arb\_state values are ARBIT\_NULL, ARBIT\_INIT, ARBIT\_FIND, ARBIT\_PREP1, ARBIT\_PREP2, ARBIT\_START, ARBIT\_RUN, ARBIT\_CHOOSE, ARBIT\_CRASH, and UNKNOWN.

arb\_connected shows whether this node is connected to the node shown as this node's arbitrator.

The connected\_rank1\_arbs and connected\_rank2\_arbs columns each display a list of 0 or more arbitrators having an ArbitrationRank equal to 1, or to 2, respectively.

![](_page_52_Picture_8.jpeg)

# **Note**

Both management nodes and API nodes are eligible to become arbitrators.

# <span id="page-52-0"></span>**21.6.15.26 The ndbinfo memoryusage Table**

Querying this table provides information similar to that provided by the ALL REPORT MemoryUsage command in the ndb\_mgm client, or logged by [ALL DUMP 1000](https://dev.mysql.com/doc/ndb-internals/en/dump-command-1000.md).

The memoryusage table contains the following columns:

• node\_id

The node ID of this data node.

• memory\_type

One of Data memory, Index memory, or Long message buffer.

• used

Number of bytes currently used for data memory or index memory by this data node.

• used\_pages

Number of pages currently used for data memory or index memory by this data node; see text.

• total

Total number of bytes of data memory or index memory available for this data node; see text.

• total\_pages

Total number of memory pages available for data memory or index memory on this data node; see text.

### **Notes**

The total column represents the total amount of memory in bytes available for the given resource (data memory or index memory) on a particular data node. This number should be approximately equal to the setting of the corresponding configuration parameter in the config.ini file.

Suppose that the cluster has 2 data nodes having node IDs 5 and 6, and the config.ini file contains the following:

```
[ndbd default]
DataMemory = 1G
IndexMemory = 1G
```

Suppose also that the value of the LongMessageBuffer configuration parameter is allowed to assume its default (64 MB).

The following query shows approximately the same values:

```
mysql> SELECT node_id, memory_type, total
 > FROM ndbinfo.memoryusage;
+---------+---------------------+------------+
| node_id | memory_type | total |
+---------+---------------------+------------+
| 5 | Data memory | 1073741824 |
| 5 | Index memory | 1074003968 |
| 5 | Long message buffer | 67108864 |
| 6 | Data memory | 1073741824 |
| 6 | Index memory | 1074003968 |
| 6 | Long message buffer | 67108864 |
+---------+---------------------+------------+
6 rows in set (0.00 sec)
```

In this case, the total column values for index memory are slightly higher than the value set of IndexMemory due to internal rounding.

For the used\_pages and total\_pages columns, resources are measured in pages, which are 32K in size for DataMemory and 8K for IndexMemory. For long message buffer memory, the page size is 256 bytes.

# <span id="page-53-0"></span>**21.6.15.27 The ndbinfo memory\_per\_fragment Table**

- [memory\\_per\\_fragment Table: Notes](#page-55-0)
- [memory\\_per\\_fragment Table: Examples](#page-57-0)

The memory\_per\_fragment table provides information about the usage of memory by individual fragments. See the [Notes](#page-55-0) later in this section to see how you can use this to find out how much memory is used by NDB tables.

The memory\_per\_fragment table contains the following columns:

• fq\_name

Name of this fragment

• parent\_fq\_name

Name of this fragment's parent

• type

Dictionary object type ([Object::Type](https://dev.mysql.com/doc/ndbapi/en/ndb-object.md#ndb-object-type), in the NDB API) used for this fragment; one of System table, User table, Unique hash index, Hash index, Unique ordered index, Ordered index, Hash index trigger, Subscription trigger, Read only constraint, Index trigger, Reorganize trigger, Tablespace, Log file group, Data file, Undo file, Hash map, Foreign key definition, Foreign key parent trigger, Foreign key child trigger, or Schema transaction.

You can also obtain this list by executing [TABLE](https://dev.mysql.com/doc/refman/8.0/en/table.md) [ndbinfo.dict\\_obj\\_types](#page-41-0) in the mysql client.

• table\_id

Table ID for this table

• node\_id

Node ID for this node

• block\_instance

NDB kernel block instance ID; you can use this number to obtain information about specific threads from the [threadblocks](#page-85-0) table.

• fragment\_num

Fragment ID (number)

• fixed\_elem\_alloc\_bytes

Number of bytes allocated for fixed-sized elements

• fixed\_elem\_free\_bytes

Free bytes remaining in pages allocated to fixed-size elements

• fixed\_elem\_size\_bytes

Length of each fixed-size element in bytes

• fixed\_elem\_count

Number of fixed-size elements

• fixed\_elem\_free\_count

Number of free rows for fixed-size elements

• var\_elem\_alloc\_bytes

Number of bytes allocated for variable-size elements

• var\_elem\_free\_bytes

Free bytes remaining in pages allocated to variable-size elements

• var\_elem\_count

Number of variable-size elements

• hash\_index\_alloc\_bytes

Number of bytes allocated to hash indexes

### <span id="page-55-0"></span>**memory\_per\_fragment Table: Notes**

The memory\_per\_fragment table contains one row for every table fragment replica and every index fragment replica in the system; this means that, for example, when NoOfReplicas=2, there are normally two fragment replicas for each fragment. This is true as long as all data nodes are running and connected to the cluster; for a data node that is missing, there are no rows for the fragment replicas that it hosts.

The columns of the memory\_per\_fragment table can be grouped according to their function or purpose as follows:

- Key columns: fq\_name, type, table\_id, node\_id, block\_instance, and fragment\_num
- Relationship column: parent\_fq\_name
- Fixed-size storage columns: fixed\_elem\_alloc\_bytes, fixed\_elem\_free\_bytes, fixed\_elem\_size\_bytes, fixed\_elem\_count, and fixed\_elem\_free\_count
- Variable-sized storage columns: var\_elem\_alloc\_bytes, var\_elem\_free\_bytes, and var\_elem\_count
- Hash index column: hash\_index\_alloc\_bytes

The parent\_fq\_name and fq\_name columns can be used to identify indexes associated with a table. Similar schema object hierarchy information is available in other ndbinfo tables.

Table and index fragment replicas allocate DataMemory in 32KB pages. These memory pages are managed as listed here:

- Fixed-size pages: These store the fixed-size parts of rows stored in a given fragment. Every row has a fixed-size part.
- Variable-sized pages: These store variable-sized parts for rows in the fragment. Every row having one or more variable-sized, one or more dynamic columns (or both) has a variable-sized part.
- Hash index pages: These are allocated as 8 KB subpages, and store the primary key hash index structure.

Each row in an NDB table has a fixed-size part, consisting of a row header, and one or more fixed-size columns. The row may also contain one or more variable-size part references, one or more disk part references, or both. Each row also has a primary key hash index entry (corresponding to the hidden primary key that is part of every NDB table).

From the foregoing we can see that each table fragment and index fragment together allocate the amount of DataMemory calculated as shown here:

```
DataMemory =
 (number_of_fixed_pages + number_of_var_pages) * 32KB
 + number_of_hash_pages * 8KB
```

Since fixed\_elem\_alloc\_bytes and var\_elem\_alloc\_bytes are always multiples of 32768 bytes, we can further determine that number\_of\_fixed\_pages = fixed\_elem\_alloc\_bytes / 32768 and number\_of\_var\_pages = var\_elem\_alloc\_bytes / 32768. hash\_index\_alloc\_bytes is always a multiple of 8192 bytes, so number\_of\_hash\_pages = hash\_index\_alloc\_bytes / 8192.

A fixed size page has an internal header and a number of fixed-size slots, each of which can contain one row's fixed-size part. The size of a given row's fixed size part is schema-dependent, and is provided by the fixed\_elem\_size\_bytes column; the number of fixed-size slots per page can be determined by calculating the total number of slots and the total number of pages, like this:

```
fixed_slots = fixed_elem_count + fixed_elem_free_count
fixed_pages = fixed_elem_alloc_bytes / 32768
slots_per_page = total_slots / total_pages
```

fixed\_elem\_count is in effect the row count for a given table fragment, since each row has 1 fixed element, fixed\_elem\_free\_count is the total number of free fixed-size slots across the allocated pages. fixed\_elem\_free\_bytes is equal to fixed\_elem\_free\_count \* fixed\_elem\_size\_bytes.

A fragment can have any number of fixed-size pages; when the last row on a fixed-size page is deleted, the page is released to the DataMemory page pool. Fixed-size pages can be fragmented, with more pages allocated than is required by the number of fixed-size slots in use. You can check whether this is the case by comparing the pages required to the pages allocated, which you can calculate like this:

```
fixed_pages_required = 1 + (fixed_elem_count / slots_per_page)
fixed_page_utilization = fixed_pages_required / fixed_pages
```

A variable-sized page has an internal header and uses the remaining space to store one or more variable-sized row parts; the number of parts stored depends on the schema and the actual data stored. Since not all schemas or rows have a variable-sized part, var\_elem\_count can be less than fixed\_elem\_count. The total free space available on all variable-sized pages in the fragment is shown by the var\_elem\_free\_bytes column; because this space may be spread over multiple pages, it cannot necessarily be used to store an entry of a particular size. Each variable-sized page is reorganized as needed to fit the changing size of variable-sized row parts as they are inserted, updated, and deleted; if a given row part grows too large for the page it is in, it can be moved to a different page.

Variable-sized page utilisation can be calculated as shown here:

```
var_page_used_bytes = var_elem_alloc_bytes - var_elem_free_bytes
var_page_utilisation = var_page_used_bytes / var_elem_alloc_bytes
avg_row_var_part_size = var_page_used_bytes / fixed_elem_count
```

We can obtain the average variable part size per row like this:

```
avg_row_var_part_size = var_page_used_bytes / fixed_elem_count
```

Secondary unique indexes are implemented internally as independent tables with the following schema:

- Primary key: Indexed columns in base table.
- Values: Primary key columns from base table.

These tables are distributed and fragmented as normal. This means that their fragment replicas use fixed, variable, and hash index pages as with any other NDB table.

Secondary ordered indexes are fragmented and distributed in the same way as the base table. Ordered index fragments are T-tree structures which maintain a balanced tree containing row references in the order implied by the indexed columns. Since the tree contains references rather than actual data, the T-tree storage cost is not dependent on the size or number of indexed columns, but is rather a function of the number of rows. The tree is constructed using fixed-size node structures, each of which may contain a number of row references; the number of nodes required depends on the number of rows in the table, and the tree structure necessary to represent the ordering. In the memory\_per\_fragment table, we can see that ordered indexes allocate only fixed-size pages, so as usual the relevant columns from this table are as listed here:

- fixed\_elem\_alloc\_bytes: This is equal to 32768 times the number of fixed-size pages.
- fixed\_elem\_count: The number of T-tree nodes in use.
- fixed\_elem\_size\_bytes: The number of bytes per T-tree node.
- fixed\_elem\_free\_count: The number of T-tree node slots available in the pages allocated.
- fixed\_elem\_free\_bytes: This is equal to fixed\_elem\_free\_count \* fixed\_elem\_size\_bytes.

If free space in a page is fragmented, the page is defragmented. OPTIMIZE TABLE can be used to defragment a table's variable-sized pages; this moves row variable-sized parts between pages so that some whole pages can be freed for re-use.

# <span id="page-57-0"></span>**memory\_per\_fragment Table: Examples**

- [Getting general information about fragments and memory usage](#page-58-0)
- [Finding a table and its indexes](#page-58-1)
- [Finding the memory allocated by schema elements](#page-59-0)
- [Finding the memory allocated for a table and all indexes](#page-59-1)
- [Finding the memory allocated per row](#page-60-0)
- [Finding the total memory in use per row](#page-60-1)
- [Finding the memory allocated per element](#page-60-2)
- [Finding the average memory allocated per row, by element](#page-61-0)
- [Finding the average memory allocated per row](#page-61-1)
- [Finding the average memory allocated per row for a table](#page-62-0)
- [Finding the memory in use by each schema element](#page-62-1)
- [Finding the average memory in use by each schema element](#page-63-0)
- [Finding the average memory in use per row, by element](#page-63-1)
- [Finding the total average memory in use per row](#page-64-1)

For the following examples, we create a simple table with three integer columns, one of which has a primary key, one having a unique index, and one with no indexes, as well as one VARCHAR column with no indexes, as shown here:

```
mysql> CREATE DATABASE IF NOT EXISTS test;
Query OK, 1 row affected (0.06 sec)
mysql> USE test;
Database changed
mysql> CREATE TABLE t1 (
 -> c1 BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 -> c2 INT,
 -> c3 INT UNIQUE,
 -> ) ENGINE=NDBCLUSTER;
Query OK, 0 rows affected (0.27 sec)
```

Following creation of the table, we insert 50,000 rows containing random data; the precise method of generating and inserting these rows makes no practical difference, and we leave the method of accomplishing as an exercise for the user.

### <span id="page-58-0"></span>**Getting general information about fragments and memory usage**

This query shows general information about memory usage for each fragment:

```
mysql> SELECT
 -> fq_name, node_id, block_instance, fragment_num, fixed_elem_alloc_bytes,
 -> fixed_elem_free_bytes, fixed_elem_size_bytes, fixed_elem_count,
 -> fixed_elem_free_count, var_elem_alloc_bytes, var_elem_free_bytes,
 -> var_elem_count
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = "test/def/t1"\G
*************************** 1. row ***************************
 fq_name: test/def/t1
 node_id: 5
 block_instance: 1
 fragment_num: 0
fixed_elem_alloc_bytes: 1114112
 fixed_elem_free_bytes: 11836
 fixed_elem_size_bytes: 44
 fixed_elem_count: 24925
 fixed_elem_free_count: 269
 var_elem_alloc_bytes: 1245184
 var_elem_free_bytes: 32552
 var_elem_count: 24925
*************************** 2. row ***************************
 fq_name: test/def/t1
 node_id: 5
 block_instance: 1
 fragment_num: 1
fixed_elem_alloc_bytes: 1114112
 fixed_elem_free_bytes: 5236
 fixed_elem_size_bytes: 44
 fixed_elem_count: 25075
 fixed_elem_free_count: 119
 var_elem_alloc_bytes: 1277952
 var_elem_free_bytes: 54232
 var_elem_count: 25075
*************************** 3. row ***************************
 fq_name: test/def/t1
 node_id: 6
 block_instance: 1
 fragment_num: 0
fixed_elem_alloc_bytes: 1114112
 fixed_elem_free_bytes: 11836
 fixed_elem_size_bytes: 44
 fixed_elem_count: 24925
 fixed_elem_free_count: 269
 var_elem_alloc_bytes: 1245184
 var_elem_free_bytes: 32552
 var_elem_count: 24925
*************************** 4. row ***************************
 fq_name: test/def/t1
 node_id: 6
 block_instance: 1
 fragment_num: 1
fixed_elem_alloc_bytes: 1114112
 fixed_elem_free_bytes: 5236
 fixed_elem_size_bytes: 44
 fixed_elem_count: 25075
 fixed_elem_free_count: 119
 var_elem_alloc_bytes: 1277952
 var_elem_free_bytes: 54232
 var_elem_count: 25075
4 rows in set (0.12 sec)
```

### <span id="page-58-1"></span>**Finding a table and its indexes**

This query can be used to find a specific table and its indexes:

```
mysql> SELECT fq_name
 -> FROM ndbinfo.memory_per_fragment
```

```
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+
| fq_name |
+----------------------+
| test/def/t1 |
| sys/def/13/PRIMARY |
| sys/def/13/c3 |
| sys/def/13/c3$unique |
+----------------------+
4 rows in set (0.13 sec)
mysql> SELECT COUNT(*) FROM t1;
+----------+
| COUNT(*) |
+----------+
| 50000 |
+----------+
1 row in set (0.00 sec)
```

### <span id="page-59-0"></span>**Finding the memory allocated by schema elements**

This query shows the memory allocated by each schema element (in total across all replicas):

```
mysql> SELECT
 -> fq_name AS Name,
 -> SUM(fixed_elem_alloc_bytes) AS Fixed,
 -> SUM(var_elem_alloc_bytes) AS Var,
 -> SUM(hash_index_alloc_bytes) AS Hash,
 -> SUM(fixed_elem_alloc_bytes+var_elem_alloc_bytes+hash_index_alloc_bytes) AS Total
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+---------+---------+---------+----------+
| Name | Fixed | Var | Hash | Total |
+----------------------+---------+---------+---------+----------+
| test/def/t1 | 4456448 | 5046272 | 1425408 | 10928128 |
| sys/def/13/PRIMARY | 1966080 | 0 | 0 | 1966080 |
| sys/def/13/c3 | 1441792 | 0 | 0 | 1441792 |
| sys/def/13/c3$unique | 3276800 | 0 | 1425408 | 4702208 |
+----------------------+---------+---------+---------+----------+
4 rows in set (0.11 sec)
```

### <span id="page-59-1"></span>**Finding the memory allocated for a table and all indexes**

The sum of memory allocated for the table and all its indexes (in total across all replicas) can be obtained using the query shown here:

```
mysql> SELECT
 -> SUM(fixed_elem_alloc_bytes) AS Fixed,
 -> SUM(var_elem_alloc_bytes) AS Var,
 -> SUM(hash_index_alloc_bytes) AS Hash,
 -> SUM(fixed_elem_alloc_bytes+var_elem_alloc_bytes+hash_index_alloc_bytes) AS Total
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+----------+---------+---------+----------+
| Fixed | Var | Hash | Total |
+----------+---------+---------+----------+
| 11141120 | 5046272 | 2850816 | 19038208 |
+----------+---------+---------+----------+
1 row in set (0.12 sec)
```

This is an abbreviated version of the previous query which shows only the total memory used by the table:

```
mysql> SELECT
 -> SUM(fixed_elem_alloc_bytes+var_elem_alloc_bytes+hash_index_alloc_bytes) AS Total
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+----------+
```

```
| Total |
+----------+
| 19038208 |
+----------+
1 row in set (0.12 sec)
```

### <span id="page-60-0"></span>**Finding the memory allocated per row**

The following query shows the total memory allocated per row (across all replicas):

```
mysql> SELECT
 -> SUM(fixed_elem_alloc_bytes+var_elem_alloc_bytes+hash_index_alloc_bytes)
 -> /
 -> SUM(fixed_elem_count) AS Total_alloc_per_row
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1';
+---------------------+
| Total_alloc_per_row |
+---------------------+
| 109.2813 |
+---------------------+
1 row in set (0.12 sec)
```

### <span id="page-60-1"></span>**Finding the total memory in use per row**

To obtain the total memory in use per row (across all replicas), we need the total memory used divided by the row count, which is the fixed\_elem\_count for the base table like this:

```
mysql> SELECT
 -> SUM(
 -> (fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> + (var_elem_alloc_bytes - var_elem_free_bytes)
 -> + hash_index_alloc_bytes
 -> )
 -> /
 -> SUM(fixed_elem_count)
 -> AS total_in_use_per_row
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1';
+----------------------+
| total_in_use_per_row |
+----------------------+
| 107.2042 |
+----------------------+
1 row in set (0.12 sec)
```

### <span id="page-60-2"></span>**Finding the memory allocated per element**

The memory allocated by each schema element (in total across all replicas) can be found using the following query:

```
mysql> SELECT
 -> fq_name AS Name,
 -> SUM(fixed_elem_alloc_bytes) AS Fixed,
 -> SUM(var_elem_alloc_bytes) AS Var,
 -> SUM(hash_index_alloc_bytes) AS Hash,
 -> SUM(fixed_elem_alloc_bytes + var_elem_alloc_bytes + hash_index_alloc_bytes)
 -> AS Total_alloc
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+---------+---------+---------+-------------+
| Name | Fixed | Var | Hash | Total_alloc |
+----------------------+---------+---------+---------+-------------+
| test/def/t1 | 4456448 | 5046272 | 1425408 | 10928128 |
| sys/def/13/PRIMARY | 1966080 | 0 | 0 | 1966080 |
| sys/def/13/c3 | 1441792 | 0 | 0 | 1441792 |
| sys/def/13/c3$unique | 3276800 | 0 | 1425408 | 4702208 |
```

```
+----------------------+---------+---------+---------+-------------+
4 rows in set (0.11 sec)
```

### <span id="page-61-0"></span>**Finding the average memory allocated per row, by element**

To obtain the average memory allocated per row by each schema element (in total across all replicas), we use a subquery to get the base table fixed element count each time to get an average per row since fixed\_elem\_count for the indexes is not necessarily the same as for the base table, as shown here:

```
mysql> SELECT
 -> fq_name AS Name,
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Table_rows,
 ->
 -> SUM(fixed_elem_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Avg_fixed_alloc,
 ->
 -> SUM(var_elem_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') as Avg_var_alloc,
 ->
 -> SUM(hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') as Avg_hash_alloc,
 ->
 -> SUM(fixed_elem_alloc_bytes+var_elem_alloc_bytes+hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') as Avg_total_alloc
 ->
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' or parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+------------+-----------------+---------------+----------------+-----------------+
| Name | Table_rows | Avg_fixed_alloc | Avg_var_alloc | Avg_hash_alloc | Avg_total_alloc |
+----------------------+------------+-----------------+---------------+----------------+-----------------+
| test/def/t1 | 100000 | 44.5645 | 50.4627 | 14.2541 | 109.2813 |
| sys/def/13/PRIMARY | 100000 | 19.6608 | 0.0000 | 0.0000 | 19.6608 |
| sys/def/13/c3 | 100000 | 14.4179 | 0.0000 | 0.0000 | 14.4179 |
| sys/def/13/c3$unique | 100000 | 32.7680 | 0.0000 | 14.2541 | 47.0221 |
+----------------------+------------+-----------------+---------------+----------------+-----------------+
4 rows in set (0.70 sec)
```

### <span id="page-61-1"></span>**Finding the average memory allocated per row**

Average memory allocated per row (in total across all replicas):

```
mysql> SELECT
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Table_rows,
 ->
 -> SUM(fixed_elem_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Avg_fixed_alloc,
 ->
 -> SUM(var_elem_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
```

```
 -> WHERE fq_name='test/def/t1') AS Avg_var_alloc,
 ->
 -> SUM(hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Avg_hash_alloc,
 ->
 -> SUM(fixed_elem_alloc_bytes + var_elem_alloc_bytes + hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS Avg_total_alloc
 ->
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+------------+-----------------+---------------+----------------+-----------------+
| Table_rows | Avg_fixed_alloc | Avg_var_alloc | Avg_hash_alloc | Avg_total_alloc |
+------------+-----------------+---------------+----------------+-----------------+
| 100000 | 111.4112 | 50.4627 | 28.5082 | 190.3821 |
+------------+-----------------+---------------+----------------+-----------------+
1 row in set (0.71 sec)
```

### <span id="page-62-0"></span>**Finding the average memory allocated per row for a table**

To get the average amount of memory allocated per row for the entire table across all replicas, we can use the query shown here:

```
mysql> SELECT
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS table_rows,
 ->
 -> SUM(fixed_elem_alloc_bytes + var_elem_alloc_bytes + hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_total_alloc
 ->
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+------------+-----------------+
| table_rows | avg_total_alloc |
+------------+-----------------+
| 100000 | 190.3821 |
+------------+-----------------+
1 row in set (0.33 sec)
```

### <span id="page-62-1"></span>**Finding the memory in use by each schema element**

To obtain the memory in use per schema element across all replicas, we need to sum the difference between allocated and free memory for each element, like this:

```
mysql> SELECT
 -> fq_name AS Name,
 -> SUM(fixed_elem_alloc_bytes - fixed_elem_free_bytes) AS fixed_inuse,
 -> SUM(var_elem_alloc_bytes-var_elem_free_bytes) AS var_inuse,
 -> SUM(hash_index_alloc_bytes) AS hash_memory,
 -> SUM( (fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> + (var_elem_alloc_bytes - var_elem_free_bytes)
 -> + hash_index_alloc_bytes) AS total_alloc
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+-------------+-----------+---------+-------------+
| fq_name | fixed_inuse | var_inuse | hash | total_alloc |
+----------------------+-------------+-----------+---------+-------------+
| test/def/t1 | 4422304 | 4872704 | 1425408 | 10720416 |
| sys/def/13/PRIMARY | 1950848 | 0 | 0 | 1950848 |
| sys/def/13/c3 | 1428736 | 0 | 0 | 1428736 |
```

```
| sys/def/13/c3$unique | 3212800 | 0 | 1425408 | 4638208 |
+----------------------+-------------+-----------+---------+-------------+
4 rows in set (0.13 sec)
```

### <span id="page-63-0"></span>**Finding the average memory in use by each schema element**

This query gets the average memory in use per schema element across all replicas:

```
mysql> SELECT
 -> fq_name AS Name,
 ->
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS table_rows,
 ->
 -> SUM(fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_fixed_inuse,
 ->
 -> SUM(var_elem_alloc_bytes - var_elem_free_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_var_inuse,
 ->
 -> SUM(hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_hash,
 ->
 -> SUM(
 -> (fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> + (var_elem_alloc_bytes - var_elem_free_bytes) + hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_total_inuse
 ->
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1'
 -> GROUP BY fq_name;
+----------------------+------------+-----------------+---------------+----------+-----------------+
| Name | table_rows | avg_fixed_inuse | avg_var_inuse | avg_hash | avg_total_inuse |
+----------------------+------------+-----------------+---------------+----------+-----------------+
| test/def/t1 | 100000 | 44.2230 | 48.7270 | 14.2541 | 107.2042 |
| sys/def/13/PRIMARY | 100000 | 19.5085 | 0.0000 | 0.0000 | 19.5085 |
| sys/def/13/c3 | 100000 | 14.2874 | 0.0000 | 0.0000 | 14.2874 |
| sys/def/13/c3$unique | 100000 | 32.1280 | 0.0000 | 14.2541 | 46.3821 |
+----------------------+------------+-----------------+---------------+----------+-----------------+
4 rows in set (0.72 sec)
```

### <span id="page-63-1"></span>**Finding the average memory in use per row, by element**

This query gets the average memory in use per row, by element, across all replicas:

```
mysql> SELECT
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS table_rows,
 ->
 -> SUM(fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_fixed_inuse,
 ->
 -> SUM(var_elem_alloc_bytes - var_elem_free_bytes)
 -> /
```

```
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_var_inuse,
 ->
 -> SUM(hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_hash,
 ->
 -> SUM(
 -> (fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> + (var_elem_alloc_bytes - var_elem_free_bytes)
 -> + hash_index_alloc_bytes)
 -> /
 -> ( SELECT SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_total_inuse
 ->
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+------------+-----------------+---------------+----------+-----------------+
| table_rows | avg_fixed_inuse | avg_var_inuse | avg_hash | avg_total_inuse |
+------------+-----------------+---------------+----------+-----------------+
| 100000 | 110.1469 | 48.7270 | 28.5082 | 187.3821 |
+------------+-----------------+---------------+----------+-----------------+
1 row in set (0.68 sec)
```

### <span id="page-64-1"></span>**Finding the total average memory in use per row**

This query obtains the total average memory in use, per row:

```
mysql> SELECT
 -> SUM(
 -> (fixed_elem_alloc_bytes - fixed_elem_free_bytes)
 -> + (var_elem_alloc_bytes - var_elem_free_bytes)
 -> + hash_index_alloc_bytes)
 -> /
 -> ( SELECT
 -> SUM(fixed_elem_count)
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name='test/def/t1') AS avg_total_in_use
 -> FROM ndbinfo.memory_per_fragment
 -> WHERE fq_name = 'test/def/t1' OR parent_fq_name='test/def/t1';
+------------------+
| avg_total_in_use |
+------------------+
| 187.3821 |
+------------------+
1 row in set (0.24 sec)
```

# <span id="page-64-0"></span>**21.6.15.28 The ndbinfo nodes Table**

This table contains information on the status of data nodes. For each data node that is running in the cluster, a corresponding row in this table provides the node's node ID, status, and uptime. For nodes that are starting, it also shows the current start phase.

The nodes table contains the following columns:

• node\_id

The data node's unique node ID in the cluster.

• uptime

Time since the node was last started, in seconds.

• status

Current status of the data node; see text for possible values.

• start\_phase

If the data node is starting, the current start phase.

• config\_generation

The version of the cluster configuration file in use on this data node.

### **Notes**

The uptime column shows the time in seconds that this node has been running since it was last started or restarted. This is a BIGINT value. This figure includes the time actually needed to start the node; in other words, this counter starts running the moment that ndbd or ndbmtd is first invoked; thus, even for a node that has not yet finished starting, uptime may show a nonzero value.

The status column shows the node's current status. This is one of: NOTHING, CMVMI, STARTING, STARTED, SINGLEUSER, STOPPING\_1, STOPPING\_2, STOPPING\_3, or STOPPING\_4. When the status is STARTING, you can see the current start phase in the start\_phase column (see later in this section). SINGLEUSER is displayed in the status column for all data nodes when the cluster is in single user mode (see Section 21.6.6, "NDB Cluster Single User Mode"). Seeing one of the STOPPING states does not necessarily mean that the node is shutting down but can mean rather that it is entering a new state. For example, if you put the cluster in single user mode, you can sometimes see data nodes report their state briefly as STOPPING\_2 before the status changes to SINGLEUSER.

The start\_phase column uses the same range of values as those used in the output of the ndb\_mgm client node\_id STATUS command (see Section 21.6.1, "Commands in the NDB Cluster Management Client"). If the node is not currently starting, then this column shows 0. For a listing of NDB Cluster start phases with descriptions, see Section 21.6.4, "Summary of NDB Cluster Start Phases".

The config\_generation column shows which version of the cluster configuration is in effect on each data node. This can be useful when performing a rolling restart of the cluster in order to make changes in configuration parameters. For example, from the output of the following SELECT statement, you can see that node 3 is not yet using the latest version of the cluster configuration (6) although nodes 1, 2, and 4 are doing so:

```
mysql> USE ndbinfo;
Database changed
mysql> SELECT * FROM nodes;
+---------+--------+---------+-------------+-------------------+
| node_id | uptime | status | start_phase | config_generation |
+---------+--------+---------+-------------+-------------------+
| 1 | 10462 | STARTED | 0 | 6 |
| 2 | 10460 | STARTED | 0 | 6 |
| 3 | 10457 | STARTED | 0 | 5 |
| 4 | 10455 | STARTED | 0 | 6 |
+---------+--------+---------+-------------+-------------------+
2 rows in set (0.04 sec)
```

Therefore, for the case just shown, you should restart node 3 to complete the rolling restart of the cluster.

Nodes that are stopped are not accounted for in this table. Suppose that you have an NDB Cluster with 4 data nodes (node IDs 1, 2, 3 and 4), and all nodes are running normally, then this table contains 4 rows, 1 for each data node:

```
mysql> USE ndbinfo;
Database changed
mysql> SELECT * FROM nodes;
+---------+--------+---------+-------------+-------------------+
| node_id | uptime | status | start_phase | config_generation |
+---------+--------+---------+-------------+-------------------+
```

```
| 1 | 11776 | STARTED | 0 | 6 |
| 2 | 11774 | STARTED | 0 | 6 |
| 3 | 11771 | STARTED | 0 | 6 |
| 4 | 11769 | STARTED | 0 | 6 |
+---------+--------+---------+-------------+-------------------+
4 rows in set (0.04 sec)
```

If you shut down one of the nodes, only the nodes that are still running are represented in the output of this SELECT statement, as shown here:

```
ndb_mgm> 2 STOP
Node 2: Node shutdown initiated
Node 2: Node shutdown completed.
Node 2 has shutdown.
```

```
mysql> SELECT * FROM nodes;
+---------+--------+---------+-------------+-------------------+
| node_id | uptime | status | start_phase | config_generation |
+---------+--------+---------+-------------+-------------------+
| 1 | 11807 | STARTED | 0 | 6 |
| 3 | 11802 | STARTED | 0 | 6 |
| 4 | 11800 | STARTED | 0 | 6 |
+---------+--------+---------+-------------+-------------------+
3 rows in set (0.02 sec)
```

# <span id="page-66-0"></span>**21.6.15.29 The ndbinfo operations\_per\_fragment Table**

The operations\_per\_fragment table provides information about the operations performed on individual fragments and fragment replicas, as well as about some of the results from these operations.

The operations\_per\_fragment table contains the following columns:

• fq\_name

Name of this fragment

• parent\_fq\_name

Name of this fragment's parent

• type

Type of object; see text for possible values

• table\_id

Table ID for this table

• node\_id

Node ID for this node

• block\_instance

Kernel block instance ID

• fragment\_num

Fragment ID (number)

• tot\_key\_reads

Total number of key reads for this fragment replica

• tot\_key\_inserts

Total number of key inserts for this fragment replica

• tot\_key\_updates

total number of key updates for this fragment replica

• tot\_key\_writes

Total number of key writes for this fragment replica

• tot\_key\_deletes

Total number of key deletes for this fragment replica

• tot\_key\_refs

Number of key operations refused

• tot\_key\_attrinfo\_bytes

Total size of all attrinfo attributes

• tot\_key\_keyinfo\_bytes

Total size of all keyinfo attributes

• tot\_key\_prog\_bytes

Total size of all interpreted programs carried by attrinfo attributes

• tot\_key\_inst\_exec

Total number of instructions executed by interpreted programs for key operations

• tot\_key\_bytes\_returned

Total size of all data and metadata returned from key read operations

• tot\_frag\_scans

Total number of scans performed on this fragment replica

• tot\_scan\_rows\_examined

Total number of rows examined by scans

• tot\_scan\_rows\_returned

Total number of rows returned to client

• tot\_scan\_bytes\_returned

Total size of data and metadata returned to the client

• tot\_scan\_prog\_bytes

Total size of interpreted programs for scan operations

• tot\_scan\_bound\_bytes

Total size of all bounds used in ordered index scans

• tot\_scan\_inst\_exec

Total number of instructions executed for scans

• tot\_qd\_frag\_scans

Number of times that scans of this fragment replica have been queued

• conc\_frag\_scans

Number of scans currently active on this fragment replica (excluding queued scans)

• conc\_qd\_frag\_scans

Number of scans currently queued for this fragment replica

• tot\_commits

Total number of row changes committed to this fragment replica

### **Notes**

The fq\_name contains the fully qualified name of the schema object to which this fragment replica belongs. This currently has the following formats:

- Base table: DbName/def/TblName
- BLOB table: DbName/def/NDB\$BLOB\_BaseTblId\_ColNo
- Ordered index: sys/def/BaseTblId/IndexName
- Unique index: sys/def/BaseTblId/IndexName\$unique

The \$unique suffix shown for unique indexes is added by mysqld; for an index created by a different NDB API client application, this may differ, or not be present.

The syntax just shown for fully qualified object names is an internal interface which is subject to change in future releases.

Consider a table t1 created and modified by the following SQL statements:

```
CREATE DATABASE mydb;
USE mydb;
CREATE TABLE t1 (
 a INT NOT NULL,
 b INT NOT NULL,
 t TEXT NOT NULL,
 PRIMARY KEY (b)
) ENGINE=ndbcluster;
CREATE UNIQUE INDEX ix1 ON t1(b) USING HASH;
```

If t1 is assigned table ID 11, this yields the fq\_name values shown here:

- Base table: mydb/def/t1
- BLOB table: mydb/def/NDB\$BLOB\_11\_2
- Ordered index (primary key): sys/def/11/PRIMARY
- Unique index: sys/def/11/ix1\$unique

For indexes or BLOB tables, the parent\_fq\_name column contains the fq\_name of the corresponding base table. For base tables, this column is always NULL.

The type column shows the schema object type used for this fragment, which can take any one of the values System table, User table, Unique hash index, or Ordered index. BLOB tables are shown as User table.

The table\_id column value is unique at any given time, but can be reused if the corresponding object has been deleted. The same ID can be seen using the ndb\_show\_tables utility.

The block\_instance column shows which LDM instance this fragment replica belongs to. You can use this to obtain information about specific threads from the [threadblocks](#page-85-0) table. The first such instance is always numbered 0.

Since there are typically two replicas, and assuming that this is so, each fragment\_num value should appear twice in the table, on two different data nodes from the same node group.

Since NDB does not use single-key access for ordered indexes, the counts for tot\_key\_reads, tot\_key\_inserts, tot\_key\_updates, tot\_key\_writes, and tot\_key\_deletes are not incremented by ordered index operations.

![](_page_69_Picture_6.jpeg)

### **Note**

When using tot\_key\_writes, you should keep in mind that a write operation in this context updates the row if the key exists, and inserts a new row otherwise. (One use of this is in the NDB implementation of the REPLACE SQL statement.)

The tot\_key\_refs column shows the number of key operations refused by the LDM. Generally, such a refusal is due to duplicate keys (inserts), Key not found errors (updates, deletes, and reads), or the operation was rejected by an interpreted program used as a predicate on the row matching the key.

The attrinfo and keyinfo attributes counted by the tot\_key\_attrinfo\_bytes and tot\_key\_keyinfo\_bytes columns are attributes of an LQHKEYREQ signal (see [The NDB](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndb-protocol.md) [Communication Protocol\)](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndb-protocol.md) used to initiate a key operation by the LDM. An attrinfo typically contains tuple field values (inserts and updates) or projection specifications (for reads); keyinfo contains the primary or unique key needed to locate a given tuple in this schema object.

The value shown by tot\_frag\_scans includes both full scans (that examine every row) and scans of subsets. Unique indexes and BLOB tables are never scanned, so this value, like other scan-related counts, is 0 for fragment replicas of these.

tot\_scan\_rows\_examined may display less than the total number of rows in a given fragment replica, since ordered index scans can limited by bounds. In addition, a client may choose to end a scan before all potentially matching rows have been examined; this occurs when using an SQL statement containing a LIMIT or EXISTS clause, for example. tot\_scan\_rows\_returned is always less than or equal to tot\_scan\_rows\_examined.

tot\_scan\_bytes\_returned includes, in the case of pushed joins, projections returned to the [DBSPJ](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbspj.md) block in the NDB kernel.

tot\_qd\_frag\_scans can be effected by the setting for the MaxParallelScansPerFragment data node configuration parameter, which limits the number of scans that may execute concurrently on a single fragment replica.

# <span id="page-69-0"></span>**21.6.15.30 The ndbinfo processes Table**

This table contains information about NDB Cluster node processes; each node is represented by the row in the table. Only nodes that are connected to the cluster are shown in this table. You can obtain information about nodes that are configured but not connected to the cluster from the [nodes](#page-64-0) and [config\\_nodes](#page-31-0) tables.

The processes table contains the following columns:

• node\_id

The node's unique node ID in the cluster

• node\_type

Type of node (management, data, or API node; see text)

• node\_version

Version of the NDB software program running on this node.

• process\_id

This node's process ID

• angel\_process\_id

Process ID of this node's angel process

• process\_name

Name of the executable

• service\_URI

Service URI of this node (see text)

### **Notes**

node\_id is the ID assigned to this node in the cluster.

The node\_type column displays one of the following three values:

- MGM: Management node.
- NDB: Data node.
- API: API or SQL node.

For an executable shipped with the NDB Cluster distribution, node\_version shows the two-part MySQL NDB Cluster version string, such as 5.7.44-ndb-7.5.36 or 5.7.44-ndb-7.6.36, that it was compiled with. See Version strings used in NDB Cluster software, for more information.

process\_id is the node executable's process ID as shown by the host operating system using a process display application such as top on Linux, or the Task Manager on Windows platforms.

angel\_process\_id is the system process ID for the node's angel process, which ensures that a data node or SQL is automatically restarted in cases of failures. For management nodes and API nodes other than SQL nodes, the value of this column is NULL.

The process\_name column shows the name of the running executable. For management nodes, this is ndb\_mgmd. For data nodes, this is ndbd (single-threaded) or ndbmtd (multithreaded). For SQL nodes, this is mysqld. For other types of API nodes, it is the name of the executable program connected to the cluster; NDB API applications can set a custom value for this using [Ndb\\_cluster\\_connection::set\\_name\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.md#ndb-ndb-cluster-connection-set-name).

service\_URI shows the service network address. For management nodes and data nodes, the scheme used is ndb://. For SQL nodes, this is mysql://. By default, API nodes other than SQL nodes use ndb:// for the scheme; NDB API applications can set this to a custom value using Ndb\_cluster\_connection::set\_service\_uri(). regardless of the node type, the scheme is followed by the IP address used by the NDB transporter for the node in question. For management nodes and SQL nodes, this address includes the port number (usually 1186 for management nodes and 3306 for SQL nodes). If the SQL node was started with the bind\_address system variable set, this address is used instead of the transporter address, unless the bind address is set to \*, 0.0.0.0, or ::.

Additional path information may be included in the service\_URI value for an SQL node reflecting various configuration options. For example, mysql://198.51.100.3/tmp/mysql.sock indicates that the SQL node was started with the skip\_networking system variable enabled, and mysql://198.51.100.3:3306/?server-id=1 shows that replication is enabled for this SQL node.

The processes table was added in NDB 7.5.7.