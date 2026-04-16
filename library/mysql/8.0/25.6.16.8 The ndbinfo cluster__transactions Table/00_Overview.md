---
source: MySQL 8.0 Reference
title: 00_Overview
---

The cluster\_transactions table shows information about all ongoing transactions in an NDB Cluster.

The cluster\_transactions table contains the following columns:

• node\_id

Node ID of transaction coordinator

• block\_instance

TC block instance

• transid

Transaction ID

• state

Operation state (see text for possible values)

• count\_operations

Number of stateful primary key operations in transaction (includes reads with locks, as well as DML operations)

• outstanding\_operations

Operations still being executed in local data management blocks

• inactive\_seconds

Time spent waiting for API

• client\_node\_id

Client node ID

• client\_block\_ref

### Client block reference

# **Notes**

The transaction ID is a unique 64-bit number which can be obtained using the NDB API's [getTransactionId\(\)](https://dev.mysql.com/doc/ndbapi/en/ndb-ndbtransaction.md#ndb-ndbtransaction-gettransactionid) method. (Currently, the MySQL Server does not expose the NDB API transaction ID of an ongoing transaction.)

block\_instance refers to an instance of a kernel block. Together with the block name, this number can be used to look up a given instance in the threadblocks table.

The state column can have any one of the values CS\_ABORTING, CS\_COMMITTING, CS\_COMMIT\_SENT, CS\_COMPLETE\_SENT, CS\_COMPLETING, CS\_CONNECTED, CS\_DISCONNECTED, CS\_FAIL\_ABORTED, CS\_FAIL\_ABORTING, CS\_FAIL\_COMMITTED, CS\_FAIL\_COMMITTING, CS\_FAIL\_COMPLETED, CS\_FAIL\_PREPARED, CS\_PREPARE\_TO\_COMMIT, CS\_RECEIVING, CS\_REC\_COMMITTING, CS\_RESTART, CS\_SEND\_FIRE\_TRIG\_REQ, CS\_STARTED, CS\_START\_COMMITTING, CS\_START\_SCAN, CS\_WAIT\_ABORT\_CONF, CS\_WAIT\_COMMIT\_CONF, CS\_WAIT\_COMPLETE\_CONF, CS\_WAIT\_FIRE\_TRIG\_REQ. (If the MySQL Server is running with ndbinfo\_show\_hidden enabled, you can view this list of states by selecting from the ndb \$dbtc\_apiconnect\_state table, which is normally hidden.)

In client\_node\_id and client\_block\_ref, client refers to an NDB Cluster API or SQL node (that is, an NDB API client or a MySQL Server attached to the cluster).

The tc\_block\_instance column provides the [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) block instance number. You can use this along with the block name to obtain information about specific threads from the threadblocks table.

# <span id="page-138-0"></span>**25.6.16.9 The ndbinfo config\_nodes Table**

The config\_nodes table shows nodes configured in an NDB Cluster config.ini file. For each node, the table displays a row containing the node ID, the type of node (management node, data node, or API node), and the name or IP address of the host on which the node is configured to run.

This table does not indicate whether a given node is actually running, or whether it is currently connected to the cluster. Information about nodes connected to an NDB Cluster can be obtained from the [nodes](#page-186-0) and [processes](#page-192-1) table.

The config\_nodes table contains the following columns:

• node\_id

The node's ID

• node\_type

The type of node

• node\_hostname

The name or IP address of the host on which the node resides

### **Notes**

The node\_id column shows the node ID used in the config.ini file for this node; if none is specified, the node ID that would be assigned automatically to this node is displayed.

The node\_type column displays one of the following three values:

• MGM: Management node.

- NDB: Data node.
- API: API node; this includes SQL nodes.

The node\_hostname column shows the node host as specified in the config.ini file. This can be empty for an API node, if HostName has not been set in the cluster configuration file. If HostName has not been set for a data node in the configuration file, localhost is used here. localhost is also used if HostName has not been specified for a management node.

# <span id="page-139-1"></span>**25.6.16.10 The ndbinfo config\_params Table**

The config\_params table is a static table which provides the names and internal ID numbers of and other information about NDB Cluster configuration parameters. This table can also be used in conjunction with the [config\\_values](#page-139-0) table for obtaining realtime information about node configuration parameters.

The config\_params table contains the following columns:

• param\_number

The parameter's internal ID number

• param\_name

The name of the parameter

• param\_description

A brief description of the parameter

• param\_type

The parameter's data type

• param\_default

The parameter's default value, if any

• param\_min

The parameter's maximum value, if any

• param\_max

The parameter's minimum value, if any

• param\_mandatory

This is 1 if the parameter is required, otherwise 0

• param\_status

Currently unused

# **Notes**

This table is read-only.

Although this is a static table, its content can vary between NDB Cluster installations, since supported parameters can vary due to differences between software releases, cluster hardware configurations, and other factors.

# <span id="page-139-0"></span>**25.6.16.11 The ndbinfo config\_values Table**

The config\_values table provides information about the current state of node configuration parameter values. Each row in the table corresponds to the current value of a parameter on a given node.

The config\_values table contains the following columns:

• node\_id

ID of the node in the cluster

• config\_param

The parameter's internal ID number

• config\_value

Current value of the parameter

### **Notes**

This table's config\_param column and the [config\\_params](#page-139-1) table's param\_number column use the same parameter identifiers. By joining the two tables on these columns, you can obtain detailed information about desired node configuration parameters. The query shown here provides the current values for all parameters on each data node in the cluster, ordered by node ID and parameter name:

```
SELECT v.node_id AS 'Node Id',
 p.param_name AS 'Parameter',
 v.config_value AS 'Value'
FROM config_values v
JOIN config_params p
ON v.config_param=p.param_number
WHERE p.param_name NOT LIKE '\_\_%'
ORDER BY v.node_id, p.param_name;
```

Partial output from the previous query when run on a small example cluster used for simple testing:

```
+---------+------------------------------------------+----------------+
| Node Id | Parameter | Value |
+---------+------------------------------------------+----------------+
| 2 | Arbitration | 1 |
| 2 | ArbitrationTimeout | 7500 |
| 2 | BackupDataBufferSize | 16777216 |
| 2 | BackupDataDir | /home/jon/data |
| 2 | BackupDiskWriteSpeedPct | 50 |
| 2 | BackupLogBufferSize | 16777216 |
...
| 3 | TotalSendBufferMemory | 0 |
| 3 | TransactionBufferMemory | 1048576 |
| 3 | TransactionDeadlockDetectionTimeout | 1200 |
| 3 | TransactionInactiveTimeout | 4294967039 |
| 3 | TwoPassInitialNodeRestartCopy | 0 |
| 3 | UndoDataBuffer | 16777216 |
| 3 | UndoIndexBuffer | 2097152 |
+---------+------------------------------------------+----------------+
248 rows in set (0.02 sec)
```

The WHERE clause filters out parameters whose names begin with a double underscore (\_\_); these parameters are reserved for testing and other internal uses by the NDB developers, and are not intended for use in a production NDB Cluster.

You can obtain output that is more specific, more detailed, or both by issuing the proper queries. This example provides all types of available information about the NodeId, NoOfReplicas, HostName, DataMemory, IndexMemory, and TotalSendBufferMemory parameters as currently set for all data nodes in the cluster:

```
SELECT p.param name AS Name,
       v.node id AS Node,
       p.param type AS Type,
       p.param default AS 'Default',
       p.param min AS Minimum,
       p.param max AS Maximum,
       CASE p.param mandatory WHEN 1 THEN 'Y' ELSE 'N' END AS 'Required',
       v.config value AS Current
     config params p
JOIN
     config_values v
       p.param_number = v.config param
ON
WHERE p. param name
 IN ('NodeId', 'NoOfReplicas', 'HostName',
      'DataMemory', 'IndexMemory', 'TotalSendBufferMemory') \G
```

The output from this query when run on a small NDB Cluster with 2 data nodes used for simple testing is shown here:

```
**************************************
   Name: NodeId
   Node: 2
   Type: unsigned
Default:
Minimum: 1
Maximum: 144
Required: Y
Current: 2
************************* 2. row *****************
  Name: HostName
  Node: 2
   Type: string
Default: localhost
Minimum:
Maximum:
Required: N
Current: 127.0.0.1
**************************************
   Name: TotalSendBufferMemory
  Node: 2
   Type: unsigned
Default: 0
Minimum: 262144
Maximum: 4294967039
Required: N
Current: 0
                   ***** 4. row **************
  Name: NoOfReplicas
  Node: 2
   Type: unsigned
Default: 2
Minimum: 1
Maximum: 4
Required: N
Current: 2
        ************ 5. row ***************
  Name: DataMemory
  Node: 2
  Type: unsigned
Default: 102760448
Minimum: 1048576
Maximum: 1099511627776
Required: N
Current: 524288000
                ****** 6. row *************
  Name: NodeId
   Node: 3
   Type: unsigned
Default:
Minimum: 1
Maximum: 144
Required: Y
Current: 3
```

```
**************************************
   Name: HostName
   Node: 3
   Type: string
Default: localhost
Minimum:
Maximum:
Required: N
Current: 127.0.0.1
 **************************************
  Name: TotalSendBufferMemory
  Node: 3
   Type: unsigned
Default: 0
Minimum: 262144
Maximum: 4294967039
Required: N
Current: 0
         ************ 9. row **************
  Name: NoOfReplicas
  Node: 3
  Type: unsigned
Default: 2
Minimum: 1
Maximum: 4
Required: N
Current: 2
                 ***** 10. row **************
  Name: DataMemory
   Node: 3
   Type: unsigned
Default: 102760448
Minimum: 1048576
Maximum: 1099511627776
Required: N
Current: 524288000
10 rows in set (0.01 sec)
```

### <span id="page-142-0"></span>25.6.16.12 The ndbinfo counters Table

The counters table provides running totals of events such as reads and writes for specific kernel blocks and data nodes. Counts are kept from the most recent node start or restart; a node start or restart resets all counters on that node. Not all kernel blocks have all types of counters.

The counters table contains the following columns:

• node id

The data node ID

• block\_name

Name of the associated NDB kernel block (see NDB Kernel Blocks).

• block\_instance

Block instance

• counter\_id

The counter's internal ID number; normally an integer between 1 and 10, inclusive.

• counter\_name

The name of the counter. See text for names of individual counters and the NDB kernel block with which each counter is associated.

• val

The counter's value

# **Notes**

Each counter is associated with a particular NDB kernel block.

The OPERATIONS counter is associated with the [DBLQH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dblqh.md) (local query handler) kernel block. A primarykey read counts as one operation, as does a primary-key update. For reads, there is one operation in [DBLQH](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dblqh.md) per operation in [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md). For writes, there is one operation counted per fragment replica.

The ATTRINFO, TRANSACTIONS, COMMITS, READS, LOCAL\_READS, SIMPLE\_READS, WRITES, LOCAL\_WRITES, ABORTS, TABLE\_SCANS, and RANGE\_SCANS counters are associated with the [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) (transaction co-ordinator) kernel block.

LOCAL\_WRITES and LOCAL\_READS are primary-key operations using a transaction coordinator in a node that also holds the primary fragment replica of the record.

The READS counter includes all reads. LOCAL\_READS includes only those reads of the primary fragment replica on the same node as this transaction coordinator. SIMPLE\_READS includes only those reads in which the read operation is the beginning and ending operation for a given transaction. Simple reads do not hold locks but are part of a transaction, in that they observe uncommitted changes made by the transaction containing them but not of any other uncommitted transactions. Such reads are "simple" from the point of view of the TC block; since they hold no locks they are not durable, and once [DBTC](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbtc.md) has routed them to the relevant LQH block, it holds no state for them.

ATTRINFO keeps a count of the number of times an interpreted program is sent to the data node. See [NDB Protocol Messages,](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndb-protocol-messages.md) for more information about ATTRINFO messages in the NDB kernel.

The LOCAL\_TABLE\_SCANS\_SENT, READS\_RECEIVED, PRUNED\_RANGE\_SCANS\_RECEIVED, RANGE\_SCANS\_RECEIVED, LOCAL\_READS\_SENT, CONST\_PRUNED\_RANGE\_SCANS\_RECEIVED, LOCAL\_RANGE\_SCANS\_SENT, REMOTE\_READS\_SENT, REMOTE\_RANGE\_SCANS\_SENT, READS\_NOT\_FOUND, SCAN\_BATCHES\_RETURNED, TABLE\_SCANS\_RECEIVED, and SCAN\_ROWS\_RETURNED counters are associated with the [DBSPJ](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbspj.md) (select push-down join) kernel block.

The block\_name and block\_instance columns provide, respectively, the applicable NDB kernel block name and instance number. You can use these to obtain information about specific threads from the threadblocks table.

A number of counters provide information about transporter overload and send buffer sizing when troubleshooting such issues. For each LQH instance, there is one instance of each counter in the following list:

- LQHKEY\_OVERLOAD: Number of primary key requests rejected at the LQH block instance due to transporter overload
- LQHKEY\_OVERLOAD\_TC: Count of instances of LQHKEY\_OVERLOAD where the TC node transporter was overloaded
- LQHKEY\_OVERLOAD\_READER: Count of instances of LQHKEY\_OVERLOAD where the API reader (reads only) node was overloaded.
- LQHKEY\_OVERLOAD\_NODE\_PEER: Count of instances of LQHKEY\_OVERLOAD where the next backup data node (writes only) was overloaded
- LQHKEY\_OVERLOAD\_SUBSCRIBER: Count of instances of LQHKEY\_OVERLOAD where a event subscriber (writes only) was overloaded.
- LQHSCAN\_SLOWDOWNS: Count of instances where a fragment scan batch size was reduced due to scanning API transporter overload.