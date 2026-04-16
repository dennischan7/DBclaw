---
source: MySQL 5.7 Reference
title: 00_Overview
---

The restart\_info table contains information about node restart operations. Each entry in the table corresponds to a node restart status report in real time from a data node with the given node ID. Only the most recent report for any given node is shown.

The restart\_info table contains the following columns:

• node\_id

Node ID in the cluster

• node\_restart\_status

Node status; see text for values. Each of these corresponds to a possible value of node\_restart\_status\_int.

• node\_restart\_status\_int

Node status code; see text for values.

• secs\_to\_complete\_node\_failure

Time in seconds to complete node failure handling

• secs\_to\_allocate\_node\_id

Time in seconds from node failure completion to allocation of node ID

• secs\_to\_include\_in\_heartbeat\_protocol

Time in seconds from allocation of node ID to inclusion in heartbeat protocol

• secs\_until\_wait\_for\_ndbcntr\_master

Time in seconds from being included in heartbeat protocol until waiting for [NDBCNTR](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-ndbcntr.md) master began

• secs\_wait\_for\_ndbcntr\_master

Time in seconds spent waiting to be accepted by [NDBCNTR](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-ndbcntr.md) master for starting

• secs\_to\_get\_start\_permitted

Time in seconds elapsed from receiving of permission for start from master until all nodes have accepted start of this node

• secs\_to\_wait\_for\_lcp\_for\_copy\_meta\_data

Time in seconds spent waiting for LCP completion before copying metadata

• secs\_to\_copy\_meta\_data

Time in seconds required to copy metadata from master to newly starting node

• secs\_to\_include\_node

Time in seconds waited for GCP and inclusion of all nodes into protocols

• secs\_starting\_node\_to\_request\_local\_recovery

Time in seconds that the node just starting spent waiting to request local recovery

• secs\_for\_local\_recovery

Time in seconds required for local recovery by node just starting

• secs\_restore\_fragments

Time in seconds required to restore fragments from LCP files

• secs\_undo\_disk\_data

Time in seconds required to execute undo log on disk data part of records

• secs\_exec\_redo\_log

Time in seconds required to execute redo log on all restored fragments

• secs\_index\_rebuild

Time in seconds required to rebuild indexes on restored fragments

• secs\_to\_synchronize\_starting\_node

Time in seconds required to synchronize starting node from live nodes

• secs\_wait\_lcp\_for\_restart

Time in seconds required for LCP start and completion before restart was completed

• secs\_wait\_subscription\_handover

Time in seconds spent waiting for handover of replication subscriptions

• total\_restart\_secs

Total number of seconds from node failure until node is started again

# **Notes**

The following list contains values defined for the node\_restart\_status\_int column with their internal status names (in parentheses), and the corresponding messages shown in the node\_restart\_status column:

• 0 (ALLOCATED\_NODE\_ID)

```
Allocated node id
• 1 (INCLUDED_IN_HB_PROTOCOL)
 Included in heartbeat protocol
• 2 (NDBCNTR_START_WAIT)
 Wait for NDBCNTR master to permit us to start
• 3 (NDBCNTR_STARTED)
 NDBCNTR master permitted us to start
• 4 (START_PERMITTED)
 All nodes permitted us to start
• 5 (WAIT_LCP_TO_COPY_DICT)
 Wait for LCP completion to start copying metadata
• 6 (COPY_DICT_TO_STARTING_NODE)
 Copying metadata to starting node
• 7 (INCLUDE_NODE_IN_LCP_AND_GCP)
 Include node in LCP and GCP protocols
• 8 (LOCAL_RECOVERY_STARTED)
 Restore fragments ongoing
• 9 (COPY_FRAGMENTS_STARTED)
 Synchronizing starting node with live nodes
• 10 (WAIT_LCP_FOR_RESTART)
 Wait for LCP to ensure durability
• 11 (WAIT_SUMA_HANDOVER)
 Wait for handover of subscriptions
• 12 (RESTART_COMPLETED)
 Restart completed
• 13 (NODE_FAILED)
 Node failed, failure handling in progress
• 14 (NODE_FAILURE_COMPLETED)
 Node failure handling completed
• 15 (NODE_GETTING_PERMIT)
 All nodes permitted us to start
• 16 (NODE_GETTING_INCLUDED)
```

```
Include node in LCP and GCP protocols
• 17 (NODE_GETTING_SYNCHED)
 Synchronizing starting node with live nodes
• 18 (NODE_GETTING_LCP_WAITED)
 [none]
• 19 (NODE_ACTIVE)
 Restart completed
• 20 (NOT_DEFINED_IN_CLUSTER)
 [none]
• 21 (NODE_NOT_RESTARTED_YET)
 Initial state
```

Status numbers 0 through 12 apply on master nodes only; the remainder of those shown in the table apply to all restarting data nodes. Status numbers 13 and 14 define node failure states; 20 and 21 occur when no information about the restart of a given node is available.

See also Section 21.6.4, "Summary of NDB Cluster Start Phases".

# <span id="page-75-0"></span>**21.6.15.33 The ndbinfo server\_locks Table**

The server\_locks table is similar in structure to the cluster\_locks table, and provides a subset of the information found in the latter table, but which is specific to the SQL node (MySQL server) where it resides. (The cluster\_locks table provides information about all locks in the cluster.) More precisely, server\_locks contains information about locks requested by threads belonging to the current mysqld instance, and serves as a companion table to [server\\_operations](#page-77-0). This may be useful for correlating locking patterns with specific MySQL user sessions, queries, or use cases.

The server\_locks table contains the following columns:

• mysql\_connection\_id MySQL connection ID

• node\_id

ID of reporting node

• block\_instance

ID of reporting LDM instance

• tableid

ID of table containing this row

• fragmentid

ID of fragment containing locked row

• rowid

ID of locked row

• transid

Transaction ID

• mode

Lock request mode

• state

Lock state

• detail

Whether this is first holding lock in row lock queue

• op

Operation type

• duration\_millis

Milliseconds spent waiting or holding lock

• lock\_num

ID of lock object

• waiting\_for

Waiting for lock with this ID

### **Notes**

The mysql\_connection\_id column shows the MySQL connection or thread ID as shown by SHOW PROCESSLIST.

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the [threadblocks](#page-85-0) table.

The tableid is assigned to the table by NDB; the same ID is used for this table in other ndbinfo tables, as well as in the output of ndb\_show\_tables.

The transaction ID shown in the transid column is the identifier generated by the NDB API for the transaction requesting or holding the current lock.

The mode column shows the lock mode, which is always one of S (shared lock) or X (exclusive lock). If a transaction has an exclusive lock on a given row, all other locks on that row have the same transaction ID.

The state column shows the lock state. Its value is always one of H (holding) or W (waiting). A waiting lock request waits for a lock held by a different transaction.

The detail column indicates whether this lock is the first holding lock in the affected row's lock queue, in which case it contains a \* (asterisk character); otherwise, this column is empty. This information can be used to help identify the unique entries in a list of lock requests.

The op column shows the type of operation requesting the lock. This is always one of the values READ, INSERT, UPDATE, DELETE, SCAN, or REFRESH.

The duration\_millis column shows the number of milliseconds for which this lock request has been waiting or holding the lock. This is reset to 0 when a lock is granted for a waiting request.

The lock ID (lockid column) is unique to this node and block instance.

If the lock\_state column's value is W, this lock is waiting to be granted, and the waiting\_for column shows the lock ID of the lock object this request is waiting for. Otherwise, waiting\_for is empty. waiting\_for can refer only to locks on the same row (as identified by node\_id, block\_instance, tableid, fragmentid, and rowid).

The server\_locks table was added in NDB 7.5.3.

# <span id="page-77-0"></span>**21.6.15.34 The ndbinfo server\_operations Table**

The server\_operations table contains entries for all ongoing NDB operations that the current SQL node (MySQL Server) is currently involved in. It effectively is a subset of the [cluster\\_operations](#page-29-0) table, in which operations for other SQL and API nodes are not shown.

The server\_operations table contains the following columns:

• mysql\_connection\_id

MySQL Server connection ID

• node\_id

Node ID

• block\_instance

Block instance

• transid

Transaction ID

• operation\_type

Operation type (see text for possible values)

• state

Operation state (see text for possible values)

• tableid

Table ID

• fragmentid

Fragment ID

• client\_node\_id

Client node ID

• client\_block\_ref

Client block reference

• tc\_node\_id

Transaction coordinator node ID

• tc\_block\_no

Transaction coordinator block number

• tc\_block\_instance

Transaction coordinator block instance

### **Notes**

The mysql\_connection\_id is the same as the connection or session ID shown in the output of SHOW PROCESSLIST. It is obtained from the INFORMATION\_SCHEMA table NDB\_TRANSID\_MYSQL\_CONNECTION\_MAP.

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the [threadblocks](#page-85-0) table.

The transaction ID (transid) is a unique 64-bit number which can be obtained using the NDB API's [getTransactionId\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbtransaction.md#ndb-ndbtransaction-gettransactionid) method. (Currently, the MySQL Server does not expose the NDB API transaction ID of an ongoing transaction.)

The operation\_type column can take any one of the values READ, READ-SH, READ-EX, INSERT, UPDATE, DELETE, WRITE, UNLOCK, REFRESH, SCAN, SCAN-SH, SCAN-EX, or <unknown>.

The state column can have any one of the values ABORT\_QUEUED, ABORT\_STOPPED, COMMITTED, COMMIT\_QUEUED, COMMIT\_STOPPED, COPY\_CLOSE\_STOPPED, COPY\_FIRST\_STOPPED, COPY\_STOPPED, COPY\_TUPKEY, IDLE, LOG\_ABORT\_QUEUED, LOG\_COMMIT\_QUEUED, LOG\_COMMIT\_QUEUED\_WAIT\_SIGNAL, LOG\_COMMIT\_WRITTEN, LOG\_COMMIT\_WRITTEN\_WAIT\_SIGNAL, LOG\_QUEUED, PREPARED, PREPARED\_RECEIVED\_COMMIT, SCAN\_CHECK\_STOPPED, SCAN\_CLOSE\_STOPPED, SCAN\_FIRST\_STOPPED, SCAN\_RELEASE\_STOPPED, SCAN\_STATE\_USED, SCAN\_STOPPED, SCAN\_TUPKEY, STOPPED, TC\_NOT\_CONNECTED, WAIT\_ACC, WAIT\_ACC\_ABORT, WAIT\_AI\_AFTER\_ABORT, WAIT\_ATTR, WAIT\_SCAN\_AI, WAIT\_TUP, WAIT\_TUPKEYINFO, WAIT\_TUP\_COMMIT, or WAIT\_TUP\_TO\_ABORT. (If the MySQL Server is running with ndbinfo\_show\_hidden enabled, you can view this list of states by selecting from the ndb\$dblqh\_tcconnect\_state table, which is normally hidden.)

You can obtain the name of an NDB table from its table ID by checking the output of ndb\_show\_tables.

The fragid is the same as the partition number seen in the output of ndb\_desc --extrapartition-info (short form -p).

In client\_node\_id and client\_block\_ref, client refers to an NDB Cluster API or SQL node (that is, an NDB API client or a MySQL Server attached to the cluster).

The block\_instance and tc\_block\_instance column provide NDB kernel block instance numbers. You can use these to obtain information about specific threads from the [threadblocks](#page-85-0) table.