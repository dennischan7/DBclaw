---
source: MySQL 8.0 Reference
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

```
• 0 (ALLOCATED_NODE_ID)
```

Allocated node id

• 1 (INCLUDED\_IN\_HB\_PROTOCOL)

Included in heartbeat protocol

• 2 (NDBCNTR\_START\_WAIT)

```
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
 Include node in LCP and GCP protocols
• 17 (NODE_GETTING_SYNCHED)
 Synchronizing starting node with live nodes
• 18 (NODE_GETTING_LCP_WAITED)
```

### [none]

• 19 (NODE\_ACTIVE)

Restart completed

• 20 (NOT\_DEFINED\_IN\_CLUSTER)

[none]

• 21 (NODE\_NOT\_RESTARTED\_YET)

Initial state

Status numbers 0 through 12 apply on master nodes only; the remainder of those shown in the table apply to all restarting data nodes. Status numbers 13 and 14 define node failure states; 20 and 21 occur when no information about the restart of a given node is available.

See also [Section 25.6.4, "Summary of NDB Cluster Start Phases"](#page-77-0).