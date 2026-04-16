---
source: MySQL 5.7 Reference
title: 00_Overview
---

The server\_transactions table is subset of the [cluster\\_transactions](#page-30-0) table, but includes only those transactions in which the current SQL node (MySQL Server) is a participant, while including the relevant connection IDs.

The server\_transactions table contains the following columns:

• mysql\_connection\_id

MySQL Server connection ID

• node\_id

Transaction coordinator node ID

• block\_instance

Transaction coordinator block instance

• transid

Transaction ID

• state

Operation state (see text for possible values)

• count\_operations

Number of stateful operations in the transaction

• outstanding\_operations

Operations still being executed by local data management layer (LQH blocks)

• inactive\_seconds

Time spent waiting for API

• client\_node\_id

Client node ID

• client\_block\_ref

Client block reference

## **Notes**

The mysql\_connection\_id is the same as the connection or session ID shown in the output of SHOW PROCESSLIST. It is obtained from the INFORMATION\_SCHEMA table NDB\_TRANSID\_MYSQL\_CONNECTION\_MAP.

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the [threadblocks](#page-85-0) table.

The transaction ID (transid) is a unique 64-bit number which can be obtained using the NDB API's [getTransactionId\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbtransaction.md#ndb-ndbtransaction-gettransactionid) method. (Currently, the MySQL Server does not expose the NDB API transaction ID of an ongoing transaction.)

The state column can have any one of the values CS\_ABORTING, CS\_COMMITTING, CS\_COMMIT\_SENT, CS\_COMPLETE\_SENT, CS\_COMPLETING, CS\_CONNECTED, CS\_DISCONNECTED, CS\_FAIL\_ABORTED, CS\_FAIL\_ABORTING, CS\_FAIL\_COMMITTED, CS\_FAIL\_COMMITTING, CS\_FAIL\_COMPLETED, CS\_FAIL\_PREPARED, CS\_PREPARE\_TO\_COMMIT, CS\_RECEIVING, CS\_REC\_COMMITTING, CS\_RESTART, CS\_SEND\_FIRE\_TRIG\_REQ, CS\_STARTED, CS\_START\_COMMITTING, CS\_START\_SCAN, CS\_WAIT\_ABORT\_CONF, CS\_WAIT\_COMMIT\_CONF, CS\_WAIT\_COMPLETE\_CONF, CS\_WAIT\_FIRE\_TRIG\_REQ. (If the MySQL Server is running with ndbinfo\_show\_hidden enabled, you can view this list of states by selecting from the ndb \$dbtc\_apiconnect\_state table, which is normally hidden.)

In client\_node\_id and client\_block\_ref, client refers to an NDB Cluster API or SQL node (that is, an NDB API client or a MySQL Server attached to the cluster).

The block\_instance column provides the [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) kernel block instance number. You can use this to obtain information about specific threads from the [threadblocks](#page-85-0) table.

# <span id="page-80-0"></span>**21.6.15.36 The ndbinfo table\_distribution\_status Table**

The table\_distribution\_status table provides information about the progress of table distribution for NDB tables.

The table\_distribution\_status table contains the following columns:

• node\_id

Node id

• table\_id

Table ID

• tab\_copy\_status

Status of copying of table distribution data to disk; one of IDLE, SR\_PHASE1\_READ\_PAGES, SR\_PHASE2\_READ\_TABLE, SR\_PHASE3\_COPY\_TABLE, REMOVE\_NODE, LCP\_READ\_TABLE, COPY\_TAB\_REQ, COPY\_NODE\_STATE, ADD\_TABLE\_MASTER, ADD\_TABLE\_SLAVE, INVALIDATE\_NODE\_LCP, ALTER\_TABLE, COPY\_TO\_SAVE, or GET\_TABINFO

• tab\_update\_status

Status of updating of table distribution data; one of IDLE, LOCAL\_CHECKPOINT, LOCAL\_CHECKPOINT\_QUEUED, REMOVE\_NODE, COPY\_TAB\_REQ, ADD\_TABLE\_MASTER, ADD\_TABLE\_SLAVE, INVALIDATE\_NODE\_LCP, or CALLBACK

• tab\_lcp\_status

Status of table LCP; one of ACTIVE (waiting for local checkpoint to be performed), WRITING\_TO\_FILE (checkpoint performed but not yet written to disk), or COMPLETED (checkpoint performed and persisted to disk)

• tab\_status

Table internal status; one of ACTIVE (table exists), CREATING (table is being created), or DROPPING (table is being dropped)

• tab\_storage

Table recoverability; one of NORMAL (fully recoverable with redo logging and checkpointing), NOLOGGING (recoverable from node crash, empty following cluster crash), or TEMPORARY (not recoverable)

• tab\_partitions

Number of partitions in table

• tab\_fragments

Number of fragments in table; normally same as tab\_partitions; for fully replicated tables equal to tab\_partitions \* [number of node groups]

• current\_scan\_count

Current number of active scans

• scan\_count\_wait

Current number of scans waiting to be performed before ALTER TABLE can complete.

• is\_reorg\_ongoing

Whether table is currently being reorganized (1 if true)

### **Notes**

The table\_distribution\_status table was added in NDB 7.5.4.

# <span id="page-81-0"></span>**21.6.15.37 The ndbinfo table\_fragments Table**

The table\_fragments table provides information about the fragmentation, partitioning, distribution, and (internal) replication of NDB tables.

The table\_fragments table contains the following columns:

• node\_id

Node ID ([DIH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdih.md) master)

• table\_id

Table ID

• partition\_id

Partition ID

• fragment\_id

Fragment ID (same as partition ID unless table is fully replicated)

• partition\_order

Order of fragment in partition

• log\_part\_id

Log part ID of fragment

• no\_of\_replicas

Number of fragment replicas

• current\_primary

Current primary node ID

• preferred\_primary

Preferred primary node ID

• current\_first\_backup

Current first backup node ID

• current\_second\_backup

Current second backup node ID

• current\_third\_backup

Current third backup node ID

• num\_alive\_replicas

Current number of live fragment replicas

• num\_dead\_replicas

Current number of dead fragment replicas

• num\_lcp\_replicas

Number of fragment replicas remaining to be checkpointed

### **Notes**

The table\_fragments table was added in NDB 7.5.4.

# <span id="page-82-0"></span>**21.6.15.38 The ndbinfo table\_info Table**

The table\_info table provides information about logging, checkpointing, distribution, and storage options in effect for individual NDB tables.

The table\_info table contains the following columns:

• table\_id

Table ID

• logged\_table

Whether table is logged (1) or not (0)

• row\_contains\_gci

Whether table rows contain GCI (1 true, 0 false)

• row\_contains\_checksum

Whether table rows contain checksum (1 true, 0 false)

• read\_backup

If backup fragment replicas are read this is 1, otherwise 0

• fully\_replicated

If table is fully replicated this is 1, otherwise 0

• storage\_type

Table storage type; one of MEMORY or DISK

• hashmap\_id

Hashmap ID

• partition\_balance

Partition balance (fragment count type) used for table; one of FOR\_RP\_BY\_NODE, FOR\_RA\_BY\_NODE, FOR\_RP\_BY\_LDM, or FOR\_RA\_BY\_LDM

• create\_gci

GCI in which table was created

### **Notes**

The table\_info table was added in NDB 7.5.4.

# <span id="page-83-0"></span>**21.6.15.39 The ndbinfo table\_replicas Table**

The table\_replicas table provides information about the copying, distribution, and checkpointing of NDB table fragments and fragment replicas.

The table\_replicas table contains the following columns:

• node\_id

ID of the node from which data is fetched ([DIH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdih.md) master)

• table\_id

Table ID

• fragment\_id

Fragment ID

• initial\_gci

Initial GCI for table

• replica\_node\_id

ID of node where fragment replica is stored

• is\_lcp\_ongoing

Is 1 if LCP is ongoing on this fragment, 0 otherwise

• num\_crashed\_replicas

Number of crashed fragment replica instances

• last\_max\_gci\_started

Highest GCI started in most recent LCP

• last\_max\_gci\_completed

Highest GCI completed in most recent LCP

• last\_lcp\_id

ID of most recent LCP

• prev\_lcp\_id

ID of previous LCP

• prev\_max\_gci\_started

Highest GCI started in previous LCP

• prev\_max\_gci\_completed

Highest GCI completed in previous LCP

• last\_create\_gci

Last Create GCI of last crashed fragment replica instance

• last\_replica\_gci

Last GCI of last crashed fragment replica instance

• is\_replica\_alive

1 if this fragment replica is alive, 0 otherwise

### **Notes**

The table\_replicas table was added in NDB 7.5.4.